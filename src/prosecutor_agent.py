"""
检察官 Agent（ReAct 风格）
职责：调查 Setup Agent 配置的环境是否存在实质性问题
- 有容器访问权，可执行命令取证
- 如果发现问题，提出带具体证据的指控
- 如果没有问题，选择不起诉
- 不安装包、不修改环境
"""

import json
import re

from .llm_engine import ARKClient, OpenAICompatibleClient
from .config import get_config
from .environment_manager import EnvironmentManager
from .logger import get_logger
from .models import ProsecutionResult

logger = get_logger("prosecutor")

MAX_STEPS = 30

SYSTEM_PROMPT = """\
你是检察官，核心任务是回答一个问题：**Setup Agent 配置的环境，能否满足该项目运行测试的基本要求？**

你不是审判 Verifier 的行为，你审判的是 Setup Agent 是否尽职。
你有容器访问权，可以执行命令取证，但不得安装任何包或修改环境。

## 强制调查流程（按顺序执行，不可跳过）

**第一步（必须）：验证核心依赖可导入**
从 pyproject.toml / setup.cfg / requirements.txt 读取项目的核心（非可选）依赖，
逐一验证是否可导入：
```
cd /workspace/repo && python3 -c "import 包名" 2>&1
```
重点检查：有无 `ImportError` / `ModuleNotFoundError`。
- **核心依赖不可导入 → Setup 失职，必须起诉**
- 可选依赖（`extras_require` / `[project.optional-dependencies]` 中的非默认组）不可导入 → 可免责

**第二步（必须）：亲自运行完整测试套件**
```
cd /workspace/repo && python3 -m pytest --tb=line -q --timeout=60 2>&1 | tail -60
```
或按项目标准方式（poetry run pytest、虚拟环境内 pytest 等）。
记录：通过数、失败数、错误类型、是否被 Killed（exit_code=137/124）。

**第三步：对每类失败逐一判责**

| 失败类型 | 判责 |
|----------|------|
| `ImportError`/`ModuleNotFoundError` + 包在核心依赖声明中 | **必须起诉**（Setup 失职） |
| 包已安装但版本与项目要求不兼容，导致 import 后即崩溃 | **必须起诉** |
| PYTHONPATH / 包路径错误，项目自身无法导入 | **必须起诉** |
| 完整套件被 Killed（exit_code=137/124）且**子集测试也有 ImportError** | **必须起诉** |
| 完整套件被 Killed，但运行小子集（10个测试）无 ImportError，仅资源超限 | 可免责 |
| 外部服务不可用（数据库、Redis、Elasticsearch、网络请求） | 可免责 |
| 纯测试逻辑断言失败（AssertionError 在业务逻辑内，非 import 阶段） | 可免责 |
| 可选 extra 未安装对应测试被跳过 | 可免责 |

**第四步：核查 Verifier 结论的可信度**
Verifier 声称 success=True，你的结果是否一致？
- 若 Verifier 使用了 `--ignore` 或 `-k` 过滤，你应关注：**被过滤掉的测试是否存在 ImportError？**
  - 有 ImportError 且对应包在核心依赖中 → 即使 Verifier 规避了，Setup Agent 仍应追责
  - 失败仅因外部服务不可用（如 Elasticsearch）→ Verifier 的规避合理，不追责 Setup Agent
- 若完整套件被 Killed，你应运行一个 10~20个测试的小子集来判断是否存在依赖缺失

## 起诉指控格式

每条指控必须包含：
- **指控对象**：Setup Agent 的哪个具体失职行为（如"未安装核心依赖 X"）
- **依赖声明证据**：该依赖在哪个文件的哪个字段中声明
- **取证命令和原始输出**：你亲自运行的命令 + 完整输出

## 工具

{"thought": "当前观察和下一步推理", "action": "exec_run", "args": {"command": "shell 命令"}}
{"thought": "调查完毕，所有失败均属免责情形", "action": "finish", "args": {"prosecute": false}}
{"thought": "发现可追责问题，提出指控", "action": "finish", "args": {
  "prosecute": true,
  "charges": [
    {"claim": "Setup Agent 未安装核心依赖 X（来源：pyproject.toml [project.dependencies]）",
     "evidence": "命令: python3 -c 'import X'\\n输出: ModuleNotFoundError: No module named 'X'"}
  ]
}}

## 硬性约束

- **不安装任何包**：禁止 pip install、apt install 等
- **不修改任何环境配置和项目文件**
- **指控对象是 Setup Agent，不是 Verifier**：Verifier 用 --ignore 跳过测试是它的判断，
  你关心的是 Setup Agent 有没有让核心依赖可用，而不是 Verifier 有没有走捷径
"""


class ProsecutorAgent:
    """检察官 ReAct sub-agent，有容器访问权"""

    def __init__(
        self,
        env: EnvironmentManager,
        setup_history: list[dict],
        verify_messages: list[dict],
    ):
        self._env = env
        self._setup_history = setup_history
        self._verify_messages = verify_messages
        self._llm = self._build_llm_client()

    def _build_llm_client(self):
        config = get_config()
        if config.llm_provider == "ark":
            return ARKClient(config.ark)
        elif config.llm_provider == "openai":
            if config.openai is None:
                raise ValueError("LLM_PROVIDER=openai 但未配置 OPENAI_API_KEY")
            return OpenAICompatibleClient(config.openai)
        else:
            raise ValueError(f"不支持的 LLM 提供商: {config.llm_provider}")

    def investigate(self) -> ProsecutionResult:
        """执行调查，返回 ProsecutionResult"""
        logger.info("检察官开始调查")

        # 构造调查背景
        setup_summary = self._format_setup_history()
        verify_summary = self._format_verify_messages()

        first_user_msg = (
            f"## Setup Agent 执行轨迹（最近20步）\n\n{setup_summary}\n\n"
            f"## in-loop Verifier 验证对话\n\n{verify_summary}\n\n"
            "请开始调查，判断 Setup Agent 配置的环境是否存在实质性问题。"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": first_user_msg},
        ]

        for step in range(1, MAX_STEPS + 1):
            logger.info(f"=== Prosecutor Step {step}/{MAX_STEPS} ===")

            try:
                raw = self._llm.chat(messages, json_mode=True)
            except Exception as e:
                logger.warning(f"Prosecutor LLM 调用失败（API 异常或超时）: {e}，跳过本步")
                continue
            logger.info(f"LLM 输出: {raw[:300]}")
            messages.append({"role": "assistant", "content": raw})

            try:
                parsed = self._parse_json(raw)
            except Exception as e:
                obs = f"JSON 解析失败: {e}，请重新输出合法 JSON。"
                logger.warning(obs)
                messages.append({"role": "user", "content": obs})
                continue

            action = parsed.get("action", "")
            args = parsed.get("args", {})
            thought = parsed.get("thought", "")
            logger.info(f"action={action}, thought={thought[:80]}")

            if action == "finish":
                prosecute = bool(args.get("prosecute", False))
                charges = args.get("charges", [])
                logger.info(f"调查完成: prosecute={prosecute}, 指控数={len(charges)}")
                self._llm.close()
                return ProsecutionResult(
                    prosecute=prosecute,
                    charges=charges,
                    messages=list(messages),
                )

            elif action == "exec_run":
                cmd = args.get("command", "")
                if not cmd:
                    obs = "错误：exec_run 缺少 command 参数"
                else:
                    result = self._env.exec_run(cmd)
                    obs = (
                        f"exit_code={result.exit_code}\n"
                        f"stdout:\n{result.stdout}\n"
                        f"stderr:\n{result.stderr}"
                    )
                    logger.debug(f"exec_run [{cmd}] → exit_code={result.exit_code}")
                messages.append({"role": "user", "content": f"命令结果:\n{obs}"})

            else:
                obs = f"未知 action='{action}'，只能使用 exec_run / finish"
                logger.warning(obs)
                messages.append({"role": "user", "content": obs})

        logger.warning("Prosecutor 达到最大步数，默认不起诉")
        self._llm.close()
        return ProsecutionResult(
            prosecute=False,
            charges=[],
            messages=list(messages),
        )

    def _format_setup_history(self) -> str:
        """格式化 Setup 历史（最近20步）"""
        recent = self._setup_history[-20:]
        lines = []
        for entry in recent:
            step = entry.get("step", "?")
            action = entry.get("action", {})
            result = entry.get("result", {})
            action_type = action.get("action_type", "?")
            content = action.get("content", {})
            thought = action.get("thought", "")[:100]
            exit_code = result.get("exit_code", "?")
            stdout = (result.get("stdout") or "")[:200]
            lines.append(
                f"[步骤{step}] {action_type} | thought: {thought}\n"
                f"  内容: {json.dumps(content, ensure_ascii=False)[:150]}\n"
                f"  结果: exit_code={exit_code}, stdout: {stdout}"
            )
        return "\n\n".join(lines) if lines else "（无历史）"

    def _format_verify_messages(self) -> str:
        """格式化 Verifier 对话"""
        if not self._verify_messages:
            return "（无 Verifier 对话记录）"
        lines = []
        for msg in self._verify_messages:
            role = msg.get("role", "?")
            content = (msg.get("content") or "")[:300]
            lines.append(f"[{role}] {content}")
        return "\n\n".join(lines)

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """宽松解析 LLM 输出中的 JSON"""
        raw = raw.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if m:
            return json.loads(m.group(1))
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise ValueError(f"无法提取 JSON: {raw[:200]}")
