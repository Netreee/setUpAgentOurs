# XPU 消融实验设计文档

## 实验目标

拆解 XPU 知识库系统的各组件贡献，回答三个问题：

1. XPU 整体是否有效？（A vs B）
2. RetrieverAgent 的两层检索比直接向量检索好多少？（B vs D）
3. 延迟审计机制是否有正向作用？（B vs C）

---

## XPU 系统架构

完整的 XPU 检索链路由三层组成：

```
Setup Agent 遇到错误
    │
    ▼
┌──────────────────────────────────────────────┐
│ RetrieverAgent（独立上下文，不污染主 Agent）    │
│                                              │
│  ① 向量粗筛：pgvector 余弦相似度，取 Top-10   │
│        │                                     │
│  ② LLM 精读筛选：从 10 条中选 Top-3           │
│        │                                     │
│  ③ 延迟审计：下次 retrieve() 时审计上次的      │
│     XPU 建议是否有效（success/failure/neutral）│
│     将审计结果写回 telemetry 供后续检索参考     │
└──────────────────────────────────────────────┘
    │
    ▼ 返回 Top-3 XPUSuggestion
Setup Agent 决策：采纳 XPU 建议 or 自行生成命令
```

当 RetrieverAgent 被禁用时，退化为：

```
Setup Agent 遇到错误
    │
    ▼ xpu.query(context)
VectorXPUClient 直接向量检索（无 LLM 精读，无审计）
    │
    ▼ 返回 Top-K XPUSuggestion
Setup Agent 决策
```

---

## 四组实验配置

### 配置 A：无 XPU（基线）

| 环境变量 | 值 |
|---------|---|
| `XPU_DISABLED` | `true` |
| `XPU_ENABLED` | `false` |
| `XPU_VECTOR_ENABLED` | `false` |

Setup Agent 纯靠 LLM 推理解决环境配置问题，没有任何外部知识库辅助。这是最纯净的基线。

**XPU 客户端**：`NoopXPUClient`（所有 query() 返回空列表）

### 配置 B：完整 XPU（RetrieverAgent + 延迟审计）

| 环境变量 | 值 |
|---------|---|
| `XPU_VECTOR_ENABLED` | `true` |
| `XPU_RETRIEVER_DISABLED` | `false` |
| `XPU_AUDIT_DISABLED` | `false` |

完整启用所有 XPU 组件：
- VectorXPUClient 连接 PostgreSQL+pgvector（421 条经验）
- RetrieverAgent 两层检索（向量粗筛 Top-10 → LLM 精读选 Top-3）
- 延迟审计：每次检索时顺便审计上一次 XPU 建议的效果，将 success/failure/neutral 写回 telemetry

**XPU 客户端**：`VectorXPUClient` → `RetrieverAgent`（完整链路）

### 配置 C：XPU + 禁用延迟审计

| 环境变量 | 值 |
|---------|---|
| `XPU_VECTOR_ENABLED` | `true` |
| `XPU_RETRIEVER_DISABLED` | `false` |
| `XPU_AUDIT_DISABLED` | `true` |

与配置 B 相同，但 RetrieverAgent 在 `retrieve()` 时跳过延迟审计步骤。具体来说：
- 向量粗筛 + LLM 精读正常执行
- `_do_delayed_audit()` 被跳过，不审计上次建议的效果，不写回 telemetry

**消融变量**：延迟审计。B 和 C 的差异 = 延迟审计的贡献。

**代码路径**（`src/retriever_agent.py` retrieve 方法）：
```python
# 配置 B：self._audit_disabled = False → 执行审计
# 配置 C：self._audit_disabled = True  → 跳过
if self._last_xpu_record and not self._audit_disabled:
    self._do_delayed_audit(history)
```

### 配置 D：XPU + 禁用 RetrieverAgent（直接向量检索）

| 环境变量 | 值 |
|---------|---|
| `XPU_VECTOR_ENABLED` | `true` |
| `XPU_RETRIEVER_DISABLED` | `true` |
| `XPU_AUDIT_DISABLED` | `false` |

VectorXPUClient 已创建（能连接向量数据库），但 RetrieverAgent 不初始化。Setup Agent 遇到错误时直接走 `xpu.query()` 回退路径：只做向量检索返回结果，没有 LLM 精读筛选，也没有延迟审计。

**消融变量**：RetrieverAgent（两层检索 + 审计）。B 和 D 的差异 = RetrieverAgent 的贡献。

**代码路径**（`src/agent.py` 初始化）：
```python
# 配置 B：retriever_disabled=False → 创建 RetrieverAgent
# 配置 D：retriever_disabled=True  → self._retriever = None，走 xpu.query() 回退
if isinstance(self._xpu, VectorXPUClient) and not get_config().xpu.retriever_disabled:
    self._retriever = RetrieverAgent(...)
```

**回退路径**（`src/agent.py` 检索阶段）：
```python
if self._retriever:
    # B/C：RetrieverAgent 两层检索
    suggestions = self._retriever.retrieve(situation=..., ...)
else:
    # D：直接向量检索，无 LLM 精读
    suggestions = self._xpu.query(context, exclude_ids=...)
```

---

## 实验矩阵

| 对比 | 消融变量 | 回答的问题 |
|------|---------|-----------|
| A vs B | 整个 XPU 系统 | XPU 知识库是否整体有效？ |
| B vs C | 延迟审计 | 审计机制是否改善了检索质量？ |
| B vs D | RetrieverAgent | LLM 精读筛选是否优于直接向量检索？ |
| A vs D | 向量检索本身 | 最简单的向量检索就已经比无 XPU 好多少？ |

---

## 实验参数

| 参数 | 值 |
|------|---|
| repo 数 | 30（从 benchmark_100 中选取有 XPU 历史结果的 repo） |
| 每个 repo 跑 4 种配置 | 共 120 次运行 |
| 最大步数 | 50 步 |
| 单次超时 | 3600 秒 |
| 并发 worker | 4 |
| LLM 模型 | ARK（字节火山引擎）—— 4 组配置使用同一模型 |
| XPU 知识库 | PostgreSQL+pgvector（xpu26 数据库，421 条经验） |
| repo 清单 | `data/ablation_30.jsonl` |

### repo 选取依据

从 benchmark_100 中选出**已有 XPU 结果的 30 个 repo**，这样可以和历史数据交叉验证。覆盖了不同的 noxpu 状态分布（pass/error/timeout/guilty），确保实验集包含简单和困难的 repo。

---

## 脚本与代码改动

### 新增文件

| 文件 | 用途 |
|------|------|
| `scripts/run_ablation.py` | 消融实验调度脚本 |
| `data/ablation_30.jsonl` | 30 个 repo 清单 |

### 代码改动

| 文件 | 改动 |
|------|------|
| `src/config.py` | `XPUConfig` 新增 `retriever_disabled` 和 `audit_disabled` 字段；`load_config()` 从环境变量读取 |
| `src/agent.py` | 初始化时检查 `retriever_disabled`，决定是否创建 RetrieverAgent |
| `src/retriever_agent.py` | 构造函数接受 `audit_disabled` 参数；`retrieve()` 中据此跳过延迟审计 |

所有改动均通过环境变量控制，默认值为 `false`（不影响现有行为）。
