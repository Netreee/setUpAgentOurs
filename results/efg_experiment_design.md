# E/F/G 三组实验设计方案

---

## 实验目标

回答三个问题：
1. **E vs F**：审计积累的 telemetry 数据能否改善检索质量？（审计的数据价值，非运行时开销）
2. **G vs B**：用顶级模型提取更高质量的 XPU，能否在弱模型运行时获得更好结果？（知识质量 vs 运行时智能）

---

## 配置 E：裸库基线（telemetry 清零）

### 含义
知识库有 421 条 XPU 经验，但所有 telemetry 归零（hits=0, successes=0, failures=0）。模拟"刚导入知识库、从未被使用过"的冷启动状态。

### 配置

| 参数 | 值 |
|------|---|
| 数据库 | `xpu_cold`（从 xpu26 复制，telemetry 全清零） |
| RetrieverAgent | **开启** |
| 延迟审计 | **关闭**（`XPU_AUDIT_DISABLED=true`） |
| 模型 | 当前模型（qwen3.5-plus） |

### 实现

```bash
# 1. 创建冷启动库
psql -c "CREATE DATABASE xpu_cold;"
pg_dump xpu26 -t xpu_entries | psql xpu_cold
psql xpu_cold -c "UPDATE xpu_entries SET telemetry = '{}'::jsonb;"

# 2. 运行
dns=postgresql://postgres:password@localhost:5432/xpu_cold \
XPU_AUDIT_DISABLED=true \
.venv/bin/python scripts/run_ablation.py --configs B --list data/ablation_30.jsonl ...
```

### 对照意义
- E 的知识库内容和 F 完全相同，唯一区别是 telemetry
- 排除运行时审计（两组都关闭），纯粹测 telemetry 数据质量的影响
- composite_score 中的 `(1 + success_rate)` 和 `tier_boost` 在 E 中全部退化为 1.0，排序完全由向量相似度决定

---

## 配置 F：审计积累库

### 含义
同样 421 条 XPU，但经过大量 repo 运行积累了真实的 telemetry 数据（哪些经验真正有效、哪些经验经常失败）。检索时 composite_score 的 tier 加权和 success_rate 加权发挥作用。

### 配置

| 参数 | 值 |
|------|---|
| 数据库 | `xpu_audited`（从 xpu26 复制，经过积累阶段丰富 telemetry） |
| RetrieverAgent | **开启** |
| 延迟审计 | **关闭**（测试时关闭，积累阶段开启） |
| 模型 | 当前模型（qwen3.5-plus） |

### 实现：两阶段

**阶段 1：Telemetry 积累（在非 ablation 的 299 个 repo 上跑）**

```bash
# 创建积累库
psql -c "CREATE DATABASE xpu_audited;"
pg_dump xpu26 -t xpu_entries | psql xpu_audited
# 清零 telemetry（从零开始积累，确保公平）
psql xpu_audited -c "UPDATE xpu_entries SET telemetry = '{}'::jsonb;"

# 跑 299 个 repo，开启审计，积累 telemetry
dns=postgresql://postgres:password@localhost:5432/xpu_audited \
XPU_AUDIT_DISABLED=false \
.venv/bin/python scripts/run_repo_list.py \
  --list data/python329.jsonl \
  --workers 4 \
  --max-steps 50 \
  --skip-existing  # 跳过 ablation_30 中的 repo（需要过滤）
```

**关键**：积累阶段必须排除 ablation_30 中的 repo，避免数据泄漏。需要准备一个 `data/accumulation_299.jsonl`。

**阶段 2：测试（在 ablation_30 上跑）**

```bash
# 积累完成后，关闭运行时审计，纯粹用积累后的 telemetry
dns=postgresql://postgres:password@localhost:5432/xpu_audited \
XPU_AUDIT_DISABLED=true \
.venv/bin/python scripts/run_ablation.py --configs B --list data/ablation_30.jsonl ...
```

### 积累阶段的预期效果

299 个 repo 跑完后，telemetry 应该显示：
- 通用有效的 XPU（如"pip install Pillow"）→ hits 高、successes 高 → Golden tier（boost 1.5）
- 通用无效的 XPU（如过于泛化的建议）→ hits 高、failures 高 → Cold tier（boost 0.6）
- 冷门 XPU → hits 低 → Normal tier（boost 1.0）

这些 tier 信息直接影响 composite_score 排序，F 的检索质量应优于 E。

### 时间估算

积累阶段：299 repo × 平均 15 分钟 / 4 worker ≈ **18 小时**

---

## 配置 G：强模型提取 + 弱模型运行

### 含义
用顶级模型（如 Claude/GPT-4o）重新提取 XPU 经验（更准确的 advice、更精确的 signals），然后用当前弱模型（qwen3.5-plus）做 Setup Agent 和 RetrieverAgent。测试"知识质量投资"的 ROI。

### 假说
当前 XPU 是用 qwen/deepseek 提取的，可能存在：
- advice 不够精确（如 django-lfs 的 XPU 只提到 Django 配置，漏掉 Pillow）
- signals 关键词不够精准（导致检索命中率低）
- atoms 操作不够具体（命令不可直接执行）

用强模型重新提取，可能生成质量更高的 XPU，即使运行时模型不变，也能获得更好的检索结果。

### 配置

| 参数 | 值 |
|------|---|
| XPU 提取模型 | **Claude Sonnet 4.6 或 GPT-4o**（一次性成本） |
| 数据库 | `xpu_strong`（强模型提取的 XPU） |
| RetrieverAgent | **开启** |
| 延迟审计 | **关闭** |
| 运行时模型（Main Agent + Retriever） | **当前模型（qwen3.5-plus）**，不变 |

### 实现

**步骤 1：用强模型重新提取 XPU**

```bash
# 修改 extract 脚本的模型配置，指向强模型
XPU_EXTRACT_MODEL=claude-sonnet-4-6 \
XPU_EXTRACT_API_KEY_ENV=ANTHROPIC_API_KEY \
.venv/bin/python scripts/extract_xpu_offline.py \
  --status pass,not_guilty,guilty,timeout,error \
  --output results/xpu_strong_model.jsonl
```

或使用 GPT-4o：

```bash
XPU_EXTRACT_MODEL=gpt-4o \
OPENAI_API_KEY=sk-xxx \
OPENAI_BASE_URL=https://api.openai.com/v1 \
.venv/bin/python scripts/extract_xpu_offline.py \
  --output results/xpu_strong_model.jsonl
```

**步骤 2：入库**

```bash
psql -c "CREATE DATABASE xpu_strong;"
# 创建表结构
pg_dump xpu26 -t xpu_entries --schema-only | psql xpu_strong
# 用新的 JSONL 入库
dns=postgresql://postgres:password@localhost:5432/xpu_strong \
.venv/bin/python scripts/index_xpu_offline.py \
  --input results/xpu_strong_model.jsonl
```

**步骤 3：测试**

```bash
dns=postgresql://postgres:password@localhost:5432/xpu_strong \
XPU_AUDIT_DISABLED=true \
.venv/bin/python scripts/run_ablation.py --configs B D --list data/ablation_30.jsonl ...
```

### 对照实验矩阵

| 组 | XPU 提取模型 | 运行时模型 | RetrieverAgent | 对比意义 |
|----|------------|-----------|---------------|---------|
| B（原始） | qwen/deepseek | qwen | 开启（选择器） | 基线 |
| G-B | **强模型** | qwen | 开启（选择器） | 知识质量的提升 |
| G-D | **强模型** | qwen | 关闭（直接向量） | 强 XPU + 直接检索 |

G-B vs B = 强模型提取的增量
G-D vs D = 强 XPU 对直接向量检索的增量
G-B vs G-D = 强 XPU 下 RetrieverAgent 是否仍然无用

### 成本估算

XPU 提取：~329 个 repo × 每个 1 次 LLM 调用 ≈ 329 次 API 调用
- Claude Sonnet: ~$5-10（一次性）
- GPT-4o: ~$3-8（一次性）

### 时间估算

提取：329 repo × ~30 秒/个 ≈ 3 小时
入库：~10 分钟
测试：30 repo × 2 配置 / 4 worker ≈ 4 小时

---

## 完整实验矩阵

| 组 | 知识库 | 提取模型 | telemetry | RetrieverAgent | 运行时审计 | 运行时模型 |
|----|--------|---------|-----------|---------------|----------|-----------|
| A | — | — | — | — | — | qwen |
| B | xpu26 (421) | qwen/deepseek | 当前值 | 选择器 | 开启 | qwen |
| C | xpu26 (421) | qwen/deepseek | 当前值 | 选择器 | **关闭** | qwen |
| D | xpu26 (421) | qwen/deepseek | 当前值 | **关闭** | — | qwen |
| **E** | xpu_cold (421) | qwen/deepseek | **清零** | 选择器 | **关闭** | qwen |
| **F** | xpu_audited (421) | qwen/deepseek | **299 repo 积累** | 选择器 | **关闭** | qwen |
| **G-B** | xpu_strong (?) | **强模型** | 清零 | 选择器 | **关闭** | qwen |
| **G-D** | xpu_strong (?) | **强模型** | 清零 | **关闭** | — | qwen |

### 对比回答的问题

| 对比 | 问题 |
|------|------|
| E vs F | 审计积累的 telemetry 数据是否改善检索质量？ |
| E vs B | telemetry 清零 + 无运行时审计 vs 当前完整系统 |
| G-B vs B | 强模型 XPU 是否比弱模型 XPU 更有效？ |
| G-B vs G-D | 强 XPU 下 RetrieverAgent 是否有价值？ |
| G-D vs D | 纯知识质量提升对直接向量检索的增量 |

---

## 执行优先级

| 优先级 | 实验 | 耗时 | 理由 |
|--------|------|------|------|
| **P0** | G（强模型提取） | 提取 3h + 测试 4h = **7h** | 成本最低，一次性 API 费用，直接回答"知识质量是否是瓶颈" |
| **P1** | E（裸库基线） | 测试 **3h** | 只需创建库+清零，无积累阶段 |
| **P2** | F（审计积累库） | 积累 18h + 测试 3h = **21h** | 最耗时，但回答审计数据价值 |

**建议执行顺序**：先 E（3h），再 G（7h 可并行），最后 F（需要 18h 积累）。E 和 G 可以并行跑（不同数据库，不冲突）。

---

## 前置准备

### 1. 准备 accumulation_299.jsonl（F 用）

```bash
python3 -c "
import json
ablation = set(json.loads(l)['repo'] for l in open('data/ablation_30.jsonl'))
with open('data/accumulation_299.jsonl', 'w') as f:
    for l in open('data/python329.jsonl'):
        d = json.loads(l)
        repo = d.get('repository','').split('/')[-1]
        if repo not in ablation:
            f.write(l)
"
```

### 2. 创建三个数据库

```bash
for db in xpu_cold xpu_audited xpu_strong; do
    psql -c "CREATE DATABASE $db;"
    pg_dump xpu26 -t xpu_entries --schema-only | psql $db
    psql $db -c "CREATE EXTENSION IF NOT EXISTS vector;"
done

# E/F 用：复制数据并清零 telemetry
for db in xpu_cold xpu_audited; do
    pg_dump xpu26 -t xpu_entries --data-only --inserts | psql $db
    psql $db -c "UPDATE xpu_entries SET telemetry = '{}'::jsonb;"
done

# G 用：空库，等强模型提取后入库
```

### 3. 确认强模型 API 可用

需要 Claude API key 或 GPT-4o API key。确认 `scripts/extract_xpu_offline.py` 支持切换模型。
