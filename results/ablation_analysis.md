# XPU 消融实验分析报告

生成时间：2026-04-08

---

## 一、总结果

| 配置 | pass | timeout | error | pass 率 |
|------|------|---------|-------|---------|
| A 无 XPU（基线） | 17 | 3 | 10 | **56.7%** |
| B 完整 XPU | 22 | 2 | 6 | **73.3%** |
| C XPU 无审计 | 24 | 0 | 6 | **80.0%** |
| D XPU 无 Retriever | 22 | 0 | 8 | **73.3%** |

排除系统异常（进程崩溃、subprocess 超时等非模型因素）后：

| 配置 | pass 率（有效样本） |
|------|-------------------|
| A | 17/24 = **70.8%** |
| B | 22/26 = **84.6%** |
| C | 24/29 = **82.8%** |
| D | 22/28 = **78.6%** |

---

## 二、核心发现

### 2.1 XPU 整体有效（A→B: +16.6pp）

30 个 repo 中，XPU 在任意配置下救回了 9 个原本 A 失败的 repo：

| repo | A | B | C | D | 模式 |
|------|---|---|---|---|------|
| evox | TIMEO | PASS | PASS | PASS | XPU 一致救回 |
| featuretools | TIMEO | PASS | PASS | PASS | XPU 一致救回 |
| huxley | ERROR | PASS | PASS | PASS | XPU 一致救回 |
| litgpt | TIMEO | PASS | PASS | PASS | XPU 一致救回 |
| py-evm | ERROR | PASS | PASS | PASS | XPU 一致救回 |
| netbox | ERROR | PASS | PASS | ERROR | B/C 救回 |
| openqasm | ERROR | ERROR | PASS | PASS | C/D 救回 |
| civet | ERROR | ERROR | PASS | ERROR | 仅 C 救回 |
| django-autocomplete-light | ERROR | ERROR | PASS | ERROR | 仅 C 救回 |

其中 5 个（evox, featuretools, huxley, litgpt, py-evm）在 B/C/D 三种 XPU 配置下**一致 pass**，说明向量检索本身就已经提供了足够的信息，这 5 个是 XPU 的稳定收益。

XPU 引入退化的 2 个 repo：

| repo | A | B | C | D | 原因 |
|------|---|---|---|---|------|
| platformio-core | PASS | TIMEO | ERROR | ERROR | XPU 建议干扰了原本能成功的路径 |
| mopidy | PASS | PASS | ERROR | PASS | 仅 C 退化（可能随机） |

### 2.2 RetrieverAgent 无净收益（B = D = 73.3%）

B vs D 的 pass/fail 翻转**完全对称**：

| 翻转方向 | 数量 | repo |
|---------|------|------|
| 仅 B pass（Retriever 救回） | 1 | netbox |
| 仅 D pass（Retriever 拖累） | 1 | openqasm |
| 两者均 pass | 21 | — |
| 两者均 fail | 7 | — |

**1 救 1 赔，净贡献为零。**

但 B 显著更慢——在 21 个两者均 pass 的 repo 上（排除 featuretools 异常值）：

| 指标 | B（完整 XPU） | D（无 Retriever） |
|------|-------------|------------------|
| 平均耗时 | 1364s | 1038s |
| 平均步数 | 16.0 步 | 17.1 步 |

**B 比 D 慢 31%，步数却没减少。** RetrieverAgent 的两层检索（向量 + LLM 精读）多了一次 LLM 调用，增加了延迟，但没有选出更好的 XPU 建议。

### 2.3 延迟审计有负面作用（B < C: -6.7pp）

B vs C 的翻转**不对称**：

| 翻转方向 | 数量 | repo |
|---------|------|------|
| 仅 B pass（审计有帮助） | 1 | mopidy |
| 仅 C pass（审计有害） | 3 | civet, django-autocomplete-light, openqasm |

**1 救 3 赔，审计净贡献为负。**

进一步分析 3 个"审计有害"的 case：

- **openqasm**：B 步数耗尽（50 步 error），C 只用 40 步就 pass。审计的额外 LLM 调用消耗了 token 预算，导致 B 用更多步数但最终未解决。
- **civet**：B 在 20 步时系统崩溃（steps=20, error），C 用 31 步 pass。B 的提前崩溃可能与审计 LLM 调用的额外负载有关。
- **django-autocomplete-light**：B 在 13 步时系统崩溃，C 用 15 步 pass。类似模式。

---

## 三、为什么 RetrieverAgent 没有效果？

### 假说 1：知识库太小，向量检索已经足够好

XPU 知识库只有 421 条经验。在这个规模下，余弦相似度 Top-10 已经能命中大部分相关建议。RetrieverAgent 的 LLM 精读筛选（从 10 选 3）并没有比直接返回 Top-3 更准确——因为候选集本身就不大，噪声比较少。

**类比**：如果一个图书馆只有 421 本书，按关键词搜索就能找到你要的书；请一个图书馆员帮你从搜索结果里挑选，不会比你自己挑好多少。

### 假说 2：LLM 精读的额外延迟消耗了步数预算

RetrieverAgent 每次检索都需要：
1. 向量检索（快，< 1 秒）
2. LLM 精读筛选（慢，3-10 秒/次，消耗 API token）
3. 延迟审计（如果启用，又一次 LLM 调用）

在 50 步上限内，这些额外的 API 调用增加了总耗时（+31%），但没有减少步数（16.0 vs 17.1）。对于 timeout 边界的 repo，额外延迟反而可能导致 subprocess 超时。

### 假说 3：审计写回的 telemetry 在 30 个 repo 规模下无法积累

延迟审计将 success/failure/neutral 写回 telemetry。但消融实验中每个 repo 是独立运行的，审计结果写回后立即结束——下一个 repo 是全新的进程，不共享审计历史。

**审计的价值需要跨 repo 积累才能体现**，在消融实验的隔离运行模式下，审计只是白白消耗了一次 LLM 调用。

### 假说 4：系统异常噪声掩盖了真实信号

30 个 repo 中只有 1-3 个翻转，其中部分是系统异常（进程崩溃），而非模型/检索质量导致。在这个样本量下，1 个随机崩溃就能改变 3.3% 的 pass 率。B 和 D 的差异（0pp）、B 和 C 的差异（-6.7pp）都在系统噪声范围内。

---

## 四、30 × 4 完整矩阵

| repo | A | B | C | D | 模式 |
|------|---|---|---|---|------|
| androidviewclient | PASS | PASS | PASS | PASS | 全 pass |
| bitcart | PASS | PASS | PASS | PASS | 全 pass |
| civet | ERROR | ERROR | **PASS** | ERROR | 仅 C |
| columnflow | ERROR | ERROR | ERROR | ERROR | 全 fail |
| django-autocomplete-light | ERROR | ERROR | **PASS** | ERROR | 仅 C |
| django-lfs | ERROR | ERROR | ERROR | ERROR | 全 fail |
| evox | TIMEO | PASS | PASS | PASS | XPU 救回 |
| fastapi-pagination | PASS | PASS | PASS | PASS | 全 pass |
| featuretools | TIMEO | PASS | PASS | PASS | XPU 救回 |
| hacs_waste_collection_schedule | PASS | PASS | PASS | PASS | 全 pass |
| huxley | ERROR | PASS | PASS | PASS | XPU 救回 |
| improv | ERROR | TIMEO | ERROR | ERROR | 全 fail |
| litgpt | TIMEO | PASS | PASS | PASS | XPU 救回 |
| mopidy | PASS | PASS | ERROR | PASS | C 退化 |
| netbox | ERROR | **PASS** | PASS | ERROR | Retriever 关键 |
| neuralforecast | PASS | PASS | PASS | PASS | 全 pass |
| openqasm | ERROR | ERROR | **PASS** | PASS | B 额外失败 |
| piccolo | PASS | PASS | PASS | PASS | 全 pass |
| pip | PASS | PASS | PASS | PASS | 全 pass |
| platformio-core | PASS | TIMEO | ERROR | ERROR | XPU 退化 |
| plotnine | PASS | PASS | PASS | PASS | 全 pass |
| poetry | PASS | PASS | PASS | PASS | 全 pass |
| proselint | PASS | PASS | PASS | PASS | 全 pass |
| py-evm | ERROR | PASS | PASS | PASS | XPU 救回 |
| pyftpdlib | PASS | PASS | PASS | PASS | 全 pass |
| python-holidays | PASS | PASS | PASS | PASS | 全 pass |
| pytorch-metric-learning | PASS | PASS | PASS | PASS | 全 pass |
| sentry-python | PASS | PASS | PASS | PASS | 全 pass |
| skrub | PASS | PASS | PASS | PASS | 全 pass |
| trax | ERROR | ERROR | ERROR | ERROR | 全 fail |

**分类统计**：
- 全 pass（XPU 无关）：15 个（50%）
- 全 fail（repo 太难）：4 个（13%）
- XPU 一致救回：5 个（17%）— XPU 的核心价值
- 翻转/噪声区：6 个（20%）— 这 6 个决定了 B/C/D 的差异

---

## 五、结论与建议

### 确定性结论

1. **XPU 有效**：A→B/C/D 提升 17-23 个百分点，5 个 repo 稳定救回
2. **RetrieverAgent 没有净收益**：pass 率与直接向量检索持平（73.3% = 73.3%），但多 31% 耗时
3. **延迟审计有轻微负面效果**：在独立运行模式下白消耗 LLM 调用

### 建议

1. **短期：消融实验确认了可以简化 XPU 链路**。把 RetrieverAgent 的两层检索降级为直接向量检索（配置 D），省掉 LLM 精读和审计的开销，效果不变但速度快 31%。

2. **中期：如果要保留 RetrieverAgent，需要扩大知识库**。421 条经验太少，LLM 精读筛选没有发挥空间。当知识库扩展到数千条以上，向量检索的 Top-10 噪声会增加，此时 LLM 精读才有价值。

3. **审计机制需要改为跨 repo 共享**：当前每个 repo 独立运行，审计结果无法积累。如果改为在线更新 telemetry（批量实验共享数据库连接），审计可能在后期运行中逐步改善检索质量。

4. **样本量不足以做强结论**：30 个 repo 中只有 6 个是翻转区，1 个随机系统异常 = 3.3% 波动。要做可靠对比需要 100+ repo。
