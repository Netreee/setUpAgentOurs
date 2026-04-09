# 数据报告（原始数字，无解释）

生成时间：2026-04-03

---

## 一、OurSys withoutXPU 全量基准

**数据集**：329 个 GitHub Python 仓库（`data/python329.jsonl`），去掉 17 个无效后实跑 **312 个**。

| 状态 | 数量 |
|------|------|
| pass / not_guilty（合计） | **223** |
| guilty / fail | 5 |
| error（系统异常中止） | 41 |
| timeout（超步数/超时） | 43 |
| **总计** | **312** |

- **通过率（分母=全量 312）**：71.5%
- **通过率（分母=有裁决的 228）**：97.8%
- 平均步数（有结果的 repo）：16.3 步
- 平均耗时（有结果的 repo）：610.7 秒（约 10 分钟）

> 来源：`results/withoutXPU_manifest.json`

---

## 二、OurSys withXPU

**背景**：从 withoutXPU 的 timeout / guilty / error 中抽取子集（共 83 个），开启 XPU（知识库检索增强）重跑。**注意：这 83 个不是随机样本，是专门挑出来的困难/失败 repo，不能与 withoutXPU 通过率直接比较。**

| withXPU 状态 | 数量 |
|------|------|
| pass / not_guilty | **52** |
| timeout | 10 |
| error | 16 |
| no_result | 5 |
| **总计** | **83** |

按 withoutXPU 原始状态细分 XPU 的救回情况（48 个在 noxpu 有明确失败记录）：

| noxpu 原始状态 | XPU 救回（pass） | 仍失败 | 救回率 |
|--------------|----------------|------|------|
| error（系统异常，与模型能力无关） | 13 | 20 | 39% |
| timeout（真正困难） | 3 | 7 | 30% |
| guilty（配置失败） | 2 | 3 | 40% |
| **困难合计（timeout+guilty）** | **5** | **10** | **33%** |

> 来源：`results/withXPU_manifest.json`

---

## 三、benchmark_100 选取逻辑

**规模**：100 个 Python 仓库，构成两部分：

| 来源 | 数量 |
|------|------|
| ExecAgent 测试集（50 repo）∩ OurSys 已跑集合 | 50 |
| 额外补充（覆盖更多领域/复杂度） | 50 |
| **合计** | **100** |

**领域分布**：

| 领域 | 数量 |
|------|------|
| toolchain（构建/包管理工具） | 33 |
| ml_ai（机器学习/AI） | 29 |
| web_api（Web 框架/API） | 18 |
| science（科学计算） | 12 |
| iot_game（IoT/游戏/其他） | 8 |

**安装复杂度分布**：

| 复杂度 | 数量 |
|--------|------|
| low | 48 |
| medium | 32 |
| high | 20 |

> 来源：`results/benchmark_100.jsonl`

---

## 四、OurSys 在 benchmark_100 上的结果

### 4.1 withoutXPU（100 个 repo 全量）

| 状态 | 数量 |
|------|------|
| pass / not_guilty | **72** |
| guilty / fail | 3 |
| error | 13 |
| timeout | 12 |
| **总计** | **100** |

- **通过率（分母=100）**：72.0%
- **通过率（分母=有裁决的 75）**：96.0%

### 4.2 withXPU（benchmark_100 中的 30 个 repo）

| 状态 | 数量 |
|------|------|
| pass / not_guilty | **18** |
| error | 7 |
| timeout | 2 |
| no_result | 3 |
| **总计** | **30** |

- **通过率（分母=30）**：60.0%

---

## 五、EnvBench 在 benchmark_100 上的结果

### 5.1 EnvBench 自身评测结果（ground truth）

EnvBench 使用 qwen3.5-plus 模型生成安装脚本，用 pyright reportMissingImports 作为唯一评测标准（不跑 pytest）。

| pyright 结果 | 数量 |
|-------------|------|
| pyright = 0（pass） | **5** |
| pyright > 0（fail，有 missing import） | 88 |
| pyright 未运行（exit_code ≠ 0） | 7 |
| **总计** | **100** |

- **EnvBench 自身通过率**：5/93 = **5.4%**（分母排除 pyright 未运行的 7 个）

### 5.2 OurSys（Prosecutor+Judge）对 EnvBench 镜像的裁决

OurSys 对 EnvBench 预构建的 100 个 Docker 镜像运行 Prosecutor+Judge 独立评测。

| 我们的裁决 | 数量 |
|-----------|------|
| not_guilty | **49** |
| guilty | 42 |
| 无裁决（构建失败/超时） | 9 |
| **总计** | **100** |

### 5.3 与 EnvBench ground truth 的对比

排除 pyright 未运行的 7 个 + 我们裁决为 None 的 9 个，**有效比较样本 86 个**。

| 对比结果 | 数量 |
|---------|------|
| 双方均 pass（agree pass） | 3 |
| 双方均 fail（agree fail） | 37 |
| **冤案**（EnvBench pass，我们 guilty） | **2** |
| **失职**（EnvBench fail，我们 not_guilty） | **44** |
| **有效样本合计** | **86** |

- **冤案率**：2/86 = **2.3%**
- **失职率**：44/86 = **51.2%**

**冤案的 2 个 repo**：dj-stripe、mopidy（均为 EnvBench pyright=0，OurSys 误判 guilty）

**失职的 44 个 repo 中**：
- 44 个均为 EnvBench pyright > 0（有 missing import），OurSys 判 not_guilty
- pyright issues 范围：1 ～ 362

---

## 附：各评测系统覆盖情况汇总

| 系统 | 覆盖 repo 数 | 数据文件 |
|------|------------|---------|
| OurSys noxpu 全量 | 312 | `withoutXPU_manifest.json` |
| OurSys xpu（选跑） | 83 | `withXPU_manifest.json` |
| benchmark_100 noxpu | 100 | `benchmark_100.jsonl` |
| benchmark_100 xpu | 30 | `benchmark_100.jsonl` |
| EnvBench（对 benchmark_100 镜像） | 100 | `envbench_100_eval.json` |
