"""
LLM 推理核心（按 blueprint 1.3 节定义）
支持 ARK 和 OpenAI 兼容接口，记录完整的输入输出日志
"""

import json
import re
from abc import ABC, abstractmethod
from typing import Any

import httpx

from .config import get_config, ARKConfig, OpenAIConfig
from .logger import get_logger
from .models import AgentAction, ActionType, XPUSuggestion

logger = get_logger("llm")


class LLMClientBase(ABC):
    """LLM 客户端抽象基类"""

    @abstractmethod
    def chat(self, messages: list[dict], json_mode: bool = False) -> str:
        """发送聊天请求"""
        pass


class ARKClient(LLMClientBase):
    """字节 ARK API 客户端"""

    def __init__(self, config: ARKConfig):
        self._config = config
        self._client = httpx.Client(timeout=120)

    def chat(self, messages: list[dict], json_mode: bool = False) -> str:
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": self._config.deployment,
            "messages": messages,
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        response = self._client.post(
            f"{self._config.base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def close(self) -> None:
        self._client.close()


class OpenAICompatibleClient(LLMClientBase):
    """OpenAI 兼容 API 客户端"""

    def __init__(self, config: OpenAIConfig):
        self._config = config
        self._client = httpx.Client(timeout=120)

    def chat(self, messages: list[dict], json_mode: bool = False) -> str:
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": self._config.model,
            "messages": messages,
            "max_tokens": 4096,
        }

        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        response = self._client.post(
            f"{self._config.base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()

        data = response.json()
        msg = data["choices"][0]["message"]
        # 兼容推理模型（如 glm-4.6）：优先取 content，若为空则取 reasoning_content
        content = msg.get("content")
        if not content:
            content = msg.get("reasoning_content", "")
        return content

    def close(self) -> None:
        self._client.close()


class LLMEngine:
    """LLM 推理引擎（按 blueprint 1.3 节定义）"""

    # System Prompt 模板（按 blueprint 3.2 节定义）
    SYSTEM_PROMPT_TEMPLATE = """You are an expert DevOps agent tailored for environment setup.
You have access to a Linux terminal and an external eXPerience Unit (XPU).

Current Status:
- WorkDir: {cwd}
- OS: {os_info}

XPU Suggestions (Proven solutions from history):
{formatted_xpu_suggestions}

## Action Types — Purpose and When to Use

### SHELL_COMMAND
Execute any shell command directly in the container.
- **Use for**: installing packages, setting PYTHONPATH, exploring repo structure, running
  diagnostic commands (e.g. `pytest --co -q` to inspect collection errors), fixing configs.
- **This is your default action.** Use it whenever you are still diagnosing or fixing.
- To check if dependencies are installed, run: `pip list | grep <pkg>` or `python -c "import X"`.
- To understand pytest errors without triggering full verification, run: `pytest --co -q 2>&1 | head -50`.

### TRY_XPU_SUGGESTION
Apply a proven fix from the XPU knowledge base inside a snapshot sandbox.
- **Use for**: applying an "Executable XPU Fix" whose commands are a precise match for the
  current error. The container is snapshotted before execution and auto-rolled back on failure.
- **Do NOT use** if the listed commands only partially match, or if you want to adapt the commands —
  in that case, write a SHELL_COMMAND yourself (referencing the XPU Reference Knowledge).
- **Do NOT use** if "Executable XPU Fixes" is absent from the XPU section (means commands are empty).

### SET_ENV
Persist an environment variable across all subsequent commands.
- **Use for**: setting variables like PYTHONPATH, JAVA_HOME that must survive across steps.
- Prefer this over `export VAR=...` in a SHELL_COMMAND, which only lasts for that single command.

### ROLLBACK_ENV
Roll the container back to the most recent snapshot.
- **Use for**: recovering from a broken environment state — e.g. after multiple failed attempts
  left the container in an inconsistent state, or after a bad TRY_XPU_SUGGESTION result.
- This is a recovery escape hatch, not a routine action. Use sparingly.

### VERIFY
Trigger the full pytest verification pipeline. This is an **expensive, final-stage action**:
it spins up a sub-agent that probes the project structure and runs `pytest --co -q` then
`pytest -x -q`. It is designed to confirm that setup is complete, NOT to diagnose problems.
- **ONLY call VERIFY when you genuinely believe all dependencies are installed and the
  environment is fully configured.**
- **NEVER call VERIFY to probe the environment, discover missing packages, or get pytest
  output for diagnosis.** Use `SHELL_COMMAND` with `pytest --co -q` for that purpose instead.
- If VERIFY succeeds → call FINISH immediately.
- If VERIFY fails → analyze the output and continue fixing with SHELL_COMMAND.

### FINISH
Signal that the task is complete. **ONLY call after a successful VERIFY.**

---

## Decision Instructions

1. Analyze the Last Error carefully before choosing an action.
2. Review "XPU Reference Knowledge" for diagnosis hints. You MAY use this knowledge
   to write a better SHELL_COMMAND — no need to pick TRY_XPU_SUGGESTION for this.
3. If "Executable XPU Fixes" lists a fix that directly matches the error, you MAY use
   TRY_XPU_SUGGESTION with its ID (snapshot-protected, auto-rollback on failure).
   **Each suggestion can only be used ONCE per run.** Once used (success or fail), it is
   removed from the list and cannot be retried. If you need to adapt the commands, write
   a SHELL_COMMAND yourself instead of repeating the same TRY_XPU_SUGGESTION ID.
   **IMPORTANT — verify preconditions before adopting any XPU suggestion:**
   XPU suggestions are retrieved by semantic similarity and may not perfectly match the
   current situation. Before acting on a suggestion, confirm its preconditions hold.
   For example: a suggestion about `poetry install` only applies if the project actually
   uses Poetry (check for `poetry.lock`); a suggestion about `pip install -e '.[all]'`
   only applies if `[project.optional-dependencies]` exists in pyproject.toml.
   If the precondition is not met, ignore the suggestion and use SHELL_COMMAND instead.
4. Default to SHELL_COMMAND when in doubt.
5. Only call VERIFY when you are confident the environment is ready. Until then, diagnose
   with SHELL_COMMAND.
6. Always explain WHY you chose the action in the "thought" field.
7. **避免重复失败**：如果同一条命令（或实质相同的命令）在最近2步内已执行过且失败，
   不要再重试。必须改变思路（换参数、换方案、或彻底放弃该路径）。

---

You MUST respond in JSON format with this schema:
{{
  "thought": "分析当前状态和错误原因，解释为什么选择该动作...",
  "action_type": "SHELL_COMMAND" | "TRY_XPU_SUGGESTION" | "SET_ENV" | "ROLLBACK_ENV" | "VERIFY" | "FINISH",
  "content": {{
    // 如果是 SHELL_COMMAND:
    "command": "pip install numpy",

    // 如果是 TRY_XPU_SUGGESTION:
    "xpu_suggestion_id": "suggestion_123",
    "reasoning": "XPU 建议降级 numpy 版本，这与报错信息高度吻合"

    // 如果是 SET_ENV:
    "env_key": "VAR_NAME",
    "env_value": "value"

    // 如果是 ROLLBACK_ENV:
    // （无需额外字段）

    // 如果是 VERIFY（hint 可选填）:
    "hint": "告知 Verifier 如何运行测试，如: 用 poetry run pytest 而不是 python3 -m pytest"

    // 如果是 FINISH:
    "message": "环境配置完成"
  }}
}}
"""

    SITUATION_PROMPT = (
        "你是环境配置 Agent 的情境感知模块。"
        "根据当前工作历史，用2-3句中文描述当前情境，内容要便于检索相关经验：\n"
        "1. 项目特征：语言、包管理器（pip/poetry/conda）、依赖文件类型\n"
        "2. 已完成的操作和当前卡点（有错误则描述错误类型，无错误则描述在做什么）\n"
        "3. 下一步意图\n"
        "只输出纯文本描述，不输出 JSON，不超过150字。\n"
        "【严格约束】只描述历史中实际执行过的命令和观察到的文件，禁止推断未见过的工具名。"
        "例如：只有在历史中确认运行过 poetry 命令或观察到 poetry.lock 时，才能写\"使用 Poetry\"；"
        "否则只写\"使用 pip\"或\"包管理器未知\"。"
    )

    def describe_situation(
        self,
        history: list[dict],
        cwd: str,
        os_info: str,
        last_error: str | None,
    ) -> str:
        """阶段A：生成当前情境描述，用于 XPU 向量检索"""
        recent = history[-5:]
        lines = []
        for entry in recent:
            if "action" in entry:
                a = entry["action"]
                lines.append(f"动作: {a.get('action_type','')} {a.get('command','')[:80]}")
            if "result" in entry:
                r = entry["result"]
                out = (r.get("stdout") or "")[:100]
                err = (r.get("stderr") or "")[:100]
                lines.append(f"结果(exit={r.get('exit_code','')}): {out or err}")

        history_text = "\n".join(lines) if lines else "（无历史记录，任务刚开始）"
        error_text = f"\n当前错误: {last_error[:200]}" if last_error else ""

        messages = [
            {"role": "system", "content": self.SITUATION_PROMPT},
            {"role": "user", "content": (
                f"工作目录: {cwd}\nOS: {os_info}{error_text}\n\n"
                f"最近操作历史:\n{history_text}"
            )},
        ]

        try:
            situation = self._client.chat(messages, json_mode=False).strip()
        except Exception as e:
            logger.warning(f"情境描述生成失败: {e}")
            situation = last_error[:150] if last_error else "python 项目环境配置"

        logger.info(f"[情境描述] {situation[:100]}")
        return situation

    def __init__(self):
        config = get_config()

        if config.llm_provider == "ark":
            self._client = ARKClient(config.ark)
            logger.info("使用 ARK LLM 客户端")
        elif config.llm_provider == "openai":
            if config.openai is None:
                raise ValueError("LLM_PROVIDER=openai 但未配置 OPENAI_API_KEY")
            self._client = OpenAICompatibleClient(config.openai)
            logger.info("使用 OpenAI 兼容 LLM 客户端")
        else:
            raise ValueError(f"不支持的 LLM 提供商: {config.llm_provider}")

    def _format_xpu_suggestions(
        self,
        suggestions: list[XPUSuggestion],
        failed_ids: set[str],
    ) -> str:
        """格式化 XPU 建议为两层文本：参考知识 + 可执行方案"""
        if not suggestions:
            return "No XPU knowledge available."

        ref_lines = []    # Layer 1：所有建议的自然语言参考（无论 commands 是否为空）
        exec_lines = []   # Layer 2：commands 非空的可执行建议

        for s in suggestions:
            if s.id in failed_ids:
                continue  # 跳过已失败的建议
            # Layer 1：自然语言参考知识
            # commands 非空时才显示 ID（否则显示 ID 会诱导 Agent 尝试 TRY_XPU_SUGGESTION）
            if s.commands:
                ref_lines.append(f"- [{s.id}] {s.description}")
            else:
                ref_lines.append(f"- {s.description}")
            # Layer 2：只有 commands 非空才展示为可执行选项
            if s.commands:
                exec_lines.append(
                    f"  [ID: {s.id}] Commands: {s.commands} (confidence: {s.confidence:.2f})"
                )

        parts = []
        if ref_lines:
            parts.append(
                "XPU Reference Knowledge (use to inform your SHELL_COMMAND):\n"
                + "\n".join(ref_lines)
            )
        if exec_lines:
            parts.append(
                "Executable XPU Fixes (use TRY_XPU_SUGGESTION, snapshot-protected):\n"
                + "\n".join(exec_lines)
            )
        return "\n\n".join(parts) if parts else "No applicable XPU knowledge."

    def generate_action(
        self,
        history: list[dict],
        xpu_suggestions: list[XPUSuggestion],
        cwd: str = "/workspace/repo",
        os_info: str = "Ubuntu 22.04",
        last_error: str | None = None,
        failed_suggestion_ids: set[str] | None = None,
    ) -> AgentAction:
        """生成下一步动作（按 blueprint 1.3 节定义）"""

        if failed_suggestion_ids is None:
            failed_suggestion_ids = set()

        # 构造 System Prompt
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(
            cwd=cwd,
            os_info=os_info,
            formatted_xpu_suggestions=self._format_xpu_suggestions(
                xpu_suggestions, failed_suggestion_ids
            ),
        )

        messages = [{"role": "system", "content": system_prompt}]

        # 添加历史记录
        for entry in history[-10:]:
            if "action" in entry:
                messages.append({
                    "role": "assistant",
                    "content": json.dumps(entry["action"], ensure_ascii=False),
                })
            if "result" in entry:
                result = entry["result"]
                content = f"命令执行结果:\n退出码: {result.get('exit_code', 'N/A')}\n"
                if result.get("stdout"):
                    content += f"输出: {result['stdout']}\n"
                if result.get("stderr"):
                    content += f"错误: {result['stderr']}\n"
                messages.append({"role": "user", "content": content})

        # 添加当前观测
        user_content = "请分析当前状态并决定下一步动作。"
        if last_error:
            user_content = f"Last Error:\n{last_error}\n\n请分析错误原因并决定下一步动作。"

        messages.append({"role": "user", "content": user_content})

        # ========== 记录 LLM 完整输入 ==========
        logger.info("=" * 60)
        logger.info("LLM 输入 (Full Prompt)")
        logger.info("=" * 60)
        for i, msg in enumerate(messages):
            logger.info(f"[{i}] role={msg['role']}")
            # 对于长消息进行截断显示
            content = msg["content"]
            if len(content) > 2000:
                logger.info(f"    content (truncated): {content[:1000]}...")
                logger.info(f"    ... ({len(content)} chars total)")
            else:
                logger.info(f"    content: {content}")
        logger.info("=" * 60)

        # 调用 LLM
        response = self._client.chat(messages, json_mode=True)

        # ========== 记录 LLM 完整输出 ==========
        logger.info("=" * 60)
        logger.info("LLM 输出 (Raw Response)")
        logger.info("=" * 60)
        logger.info(response)
        logger.info("=" * 60)

        # 解析响应
        return self._parse_response(response, xpu_suggestions)

    def _parse_response(
        self,
        response: str,
        xpu_suggestions: list[XPUSuggestion],
    ) -> AgentAction:
        """解析 LLM 响应为 AgentAction"""
        # 尝试提取 JSON
        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            # 尝试从 markdown 代码块中提取
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
            else:
                raise ValueError(f"无法解析 LLM 响应为 JSON: {response[:200]}")

        action_type_str = data.get("action_type", "SHELL_COMMAND")
        content = data.get("content", {})
        thought = data.get("thought", "")

        # 映射动作类型
        if action_type_str == "SHELL_COMMAND":
            return AgentAction(
                action_type=ActionType.SHELL_COMMAND,
                thought=thought,
                command=content.get("command"),
            )
        elif action_type_str == "TRY_XPU_SUGGESTION":
            return AgentAction(
                action_type=ActionType.TRY_XPU_SUGGESTION,
                thought=thought,
                xpu_suggestion_id=content.get("xpu_suggestion_id"),
                reasoning=content.get("reasoning"),
            )
        elif action_type_str == "FINISH":
            return AgentAction(
                action_type=ActionType.FINISH,
                thought=thought,
                message=content.get("message", "任务完成"),
            )
        elif action_type_str == "SET_ENV":
            return AgentAction(
                action_type=ActionType.SET_ENV,
                thought=thought,
                env_key=content.get("env_key"),
                env_value=content.get("env_value"),
            )
        elif action_type_str == "ROLLBACK_ENV":
            return AgentAction(
                action_type=ActionType.ROLLBACK_ENV,
                thought=thought,
            )
        elif action_type_str == "VERIFY":
            return AgentAction(
                action_type=ActionType.VERIFY,
                thought=thought,
                verify_hint=content.get("hint"),
            )
        else:
            # 默认作为 SHELL_COMMAND 处理
            logger.warning(f"未知动作类型: {action_type_str}，默认作为 SHELL_COMMAND")
            return AgentAction(
                action_type=ActionType.SHELL_COMMAND,
                thought=thought,
                command=content.get("command") or data.get("command"),
            )

    def close(self) -> None:
        """关闭 LLM 客户端"""
        if hasattr(self._client, "close"):
            self._client.close()
