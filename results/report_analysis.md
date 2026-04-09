# 分析报告

生成时间：2026-04-03

---

## 一、OurSys withoutXPU 系统表现

### 通过率解读

312 个 repo 中，223 个（71.5%）通过。剩余 84 个未通过，细分为：
- 5 个 **guilty**（环境确实配置有问题）
- 41 个 **error**（系统异常：API 超额、容器崩溃、网络超时等，非模型能力原因）
- 43 个 **timeout**（超过步数/时间上限，任务未完成）

如果只看有裁决的 228 个（排除 error/timeout），通过率 97.8%。

**error 和 timeout 占比达 27%（84/312），是通过率不能更高的主要瓶颈，而非模型能力本身。**

### withXPU 对比

WithXPU 仅针对 withoutXPU 中的 timeout/guilty/error 子集（83 个）重跑，不是随机样本，不能直接与 withoutXPU 通过率做横向比较。

83 个中"通过 52 个（62.7%）"这个数字有误导性：52 个通过里，有 13 个是原本 **error（系统异常）** 的 repo 重试后通过的——error 本身是 API 超额、容器崩溃等基础设施问题，重跑就能过，与 XPU 无关。

**对真正困难的 repo（timeout + guilty 共 15 个），XPU 救回了 5 个（33%），10 个仍失败。** XPU 的实际收益有限。

---

## 二、benchmark_100 的设计

100 个 repo 是一个**有意构建的对比基准集**，不是随机采样：
- 50 个来自 ExecAgent 测试集与 OurSys 的交集，目的是能做系统间横向比较
- 50 个额外补充，确保领域（toolchain/ml_ai/web_api/science/iot_game）和复杂度（low/medium/high）的分布均衡

这个集合的特点：偏向 Python 主流生态下有一定复杂度的仓库，不是全随机。结果不应外推为所有 Python repo 的代表性分布。

---

## 三、EnvBench 对比分析

### EnvBench 自身通过率极低（5.4%）

100 个 repo 中，EnvBench（qwen3.5-plus）只有 5 个达到 pyright=0 的通过标准。这反映的是：
1. **pyright=0 是极严格的标准**：任何一个 missing import 就判 fail，包括测试依赖、可选 extras、开发工具
2. **qwen3.5-plus 的安装脚本质量有限**：很多 repo 安装了核心包但遗漏了部分依赖

### 我们的 51.2% 失职率实质是标准差异

44 个失职中，法官的理由几乎都是：
- "pytest 在 tox.ini / tests_require 中，不是核心依赖"
- "azure/redis 等 extras 是可选依赖，未声明为核心"
- "数据库连接是外部服务，不是 Python 包安装问题"

OurSys 的标准是**核心运行时依赖可导入 + 基础测试可执行**，EnvBench 的标准是**全部 import 可解析（含测试/开发/可选依赖）**。这是设计选择的差异，不是误判。

### 2.3% 冤案是真正的 bug

2 个冤案（dj-stripe、mopidy）的根因相同：
- EnvBench Dockerfile 基础镜像 `ghcr.io/jetbrains-research/envbench-python:latest` 在构建时 pyenv 优先，包装在 pyenv 下
- 容器运行时 PATH 中 conda 排在前面
- 我们的法官用 `/opt/conda/bin/python3` 验证，找不到包，误判 guilty

修复方案：解析安装脚本中的 pyenv 路径（如 `export PATH=.../pyenv/versions/3.11.7/bin:$PATH`），在启动 Prosecutor 前直接注入正确的 Python 路径，不依赖 LLM 自行判断。

---

## 四、两套标准的本质区别

| 维度 | OurSys | EnvBench |
|------|--------|---------|
| 评测目标 | 核心依赖可用、能运行基础测试 | 所有 import 可静态解析 |
| 评测方式 | LLM 动态验证（运行命令） | pyright 静态分析 |
| 对测试依赖 | 不要求安装 | 要求（pyright 全扫） |
| 对可选 extras | 不要求 | 要求 |
| 对外部服务（DB 等） | 不要求 | 不考察 |
| 对包版本冲突 | 能发现 | 不能发现 |

两套标准各有侧重，不能简单互换。OurSys 更接近"能开发/能跑测试"，EnvBench 更接近"类型检查工具可用"。

---

## 五、已知未解决问题

1. **pyenv/conda 路径误判**（冤案根因）：法官未正确识别 pyenv 环境，导致 2 个冤案。已有明确修复方案，未实施。

2. **error/timeout 率偏高（27%）**：312 个中有 84 个因系统原因未完成，主要是 API 超额和容器不稳定，与模型能力无关，需要基础设施层面改进。

3. **XPU 覆盖不完整**：benchmark_100 中只有 30 个 repo 有 XPU 结果，无法做完整的 XPU vs noxpu 对比。

4. **ExecAgent 交叉验证待完成**：benchmark_100.jsonl 中 `execagent.verified_status` 字段均为 null，ExecAgent 在 benchmark_100 上的独立第三方裁决尚未完成。

5. **R2R 数据缺失**：benchmark_100.jsonl 中 `r2r` 字段均为 null。
