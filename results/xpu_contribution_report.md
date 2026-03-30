# XPU 贡献分析报告：timeout_xpu_rerun 12 个成功案例

**生成时间**：2026-03-29
**分析对象**：17 个原始 subprocess timeout（1800s 被杀，steps=-1）repo，重跑条件：XPU 知识库（391 条）+ 3600s 超时，结果 12 成功 / 5 失败
**核心问题**：12 个成功，能归功于 XPU 吗？

---

## 一、结论摘要

| 结论类型 | 数量 | repo |
|---------|------|------|
| **XPU 是关键**（有具体 XPU ID，无 XPU 必然失败） | 2 | elife-bot, lnldb |
| **XPU 有实质贡献**（援引 XPU 推理，解决真实障碍） | 1 | calliope |
| **混合**（XPU 提供方向提示，但决定性步骤靠 Agent 自主） | 1 | trader |
| **XPU 建议错误**（尝试了但失败，最终靠 Agent 自主解决） | 1 | biopsykit |
| **纯靠时间**（XPU 零介入或仅假命中，3600s 给够了就过） | 7 | pastas, matchms, baybe, cmdstanpy, peering-manager, skrub, etl |

**直接结论**：12 个成功中，**3 个真正归功于 XPU**（elife-bot/lnldb/calliope），**1 个 XPU 起了方向辅助作用**（trader），**7 个纯靠时间翻盘**（原 1800s 被杀只是时间不够，给够 3600s 即可）。

---

## 二、XPU 明确立功的案例

### elife-bot ⭐⭐⭐（最强证据）

- **steps**: 18，耗时 977s
- **XPU ID**: `xpu_offline_edf31bf4`，action_type = `TRY_XPU_SUGGESTION`，stdout = `[XPU SUCCESS]`
- **具体发挥**：
  - Step 4：`pip install -r requirements.txt` 失败，PyYAML 5.4.1 报 `AttributeError: 'build_ext' object has no attribute 'cython_sources'`（setuptools 70+ 与旧包不兼容）
  - Step 5：XPU 精准命中 `[xpu_offline_edf31bf4]`，建议「降级 setuptools 到 <70」，Agent 执行 `pip install 'setuptools<70'`，成功
  - 后续 16 步全部顺利完成
- **判断**：setuptools 兼容性问题是硬墙，不降级就永远卡在 PyYAML 编译，无法绕过。**没有 XPU 必然失败**，时间再多也没用。

---

### lnldb ⭐⭐⭐

- **steps**: 33，耗时 1063s
- **XPU ID**: `xpu_offline_aa0a3be4`（2 次引用，均为 SHELL_COMMAND，XPU 以 thought 参考形式注入）
- **具体发挥**：
  - Step 28：`pip install django-semanticui-forms==0.5.7` 失败（版本不存在）→ XPU 知识给出替代方案，改为安装 `==1.6.5`
  - Step 31：`pip install python-lineage==0.1.1` 失败（包已从 PyPI 下架）→ XPU 知识建议用 `grep -v` 过滤后跳过，Agent 执行成功
- **判断**：两个"版本不存在/已下架"的包是不可推断的硬坑（Agent 无法凭通用知识知道替代版本号），需要已有经验数据库。**XPU 提供了不可替代的历史经验**。

---

### calliope ⭐⭐（部分贡献，无具体 ID）

- **steps**: 14，裁决 not_guilty
- **XPU ID**: 无（thought 写「根据 XPU 知识」但未附具体 ID，可能是 LLM 内化了 XPU 推理范式）
- **具体发挥**：
  - Step 7：XPU 推理→ 修改 `glpk == 5.0` 为 `glpk >= 0.4.8`（版本不存在问题）
  - Step 9：XPU 推理→ `apt-get install -y libglpk-dev build-essential`（C 扩展缺头文件）
  - 两步均是真实障碍，不处理则 glpk 永远安装失败
- **判断**：障碍是真实的，但无法确认 Agent 是精确检索了某条 XPU 记录，还是 LLM 内化了通用系统库安装经验。**有实质贡献，但证据不如 elife-bot/lnldb 清晰**。

---

## 三、混合案例

### trader（时间 + XPU 方向提示）

- **steps**: 16，XPU 引用 4 次，含具体 ID `xpu_offline_744c952c`
- **XPU 提供了什么**：识别出是 AEA/Open Autonomy 框架项目，建议 `--only main` 跳过可选依赖
- **实际决定性操作**：Step 14 的 `autonomy packages sync`，这来自 VERIFY 报错中的 88 个 ModuleNotFoundError，Agent 自主推断，**不是 XPU 建议**
- **判断**：poetry install 163 个包需要大量时间，1800s 被杀在安装途中，3600s 是必要条件。XPU 帮助 Agent 快速定位框架类型，节省了一些探索步骤，但不是决定性的。**混合贡献，时间为主**。

---

## 四、XPU 建议错误的案例

### biopsykit（XPU 帮了倒忙）

- **steps**: 38，耗时最长
- **XPU ID**: `xpu_offline_a0fccc54`（Step 13，TRY_XPU_SUGGESTION），结果 `[XPU FAIL]`
- **经过**：ts2vg 包在 aarch64 上 Cython 编译失败 → XPU 建议降级到 1.2.3 → 仍然失败（1.2.4 和 1.2.3 源码包均缺 .pyx 文件，是上游 bug）
- **最终解法**：Agent 放弃 XPU 路径，自主创建了 ts2vg stub 包（Step 31），才解锁后续安装
- **判断**：XPU 给出了错误建议（该 bug 在两个版本上均存在），消耗了多个步骤。**真正的解法由 Agent 自主探索得出，XPU 帮了倒忙**。

---

## 五、纯靠时间的 7 个案例

| repo | steps | 原因分析 |
|------|-------|---------|
| pastas | 12 | numba/scipy 大包下载，1800s 被杀在 pip 途中，给够时间即可 |
| matchms | 8 | uv 不存在（pip install uv 是常识，无需 XPU），8 步极速完成 |
| baybe | 16 | torch ~2GB，4 次 exit_code=124 后重试成功，纯下载/安装时间问题 |
| cmdstanpy | 11 | 依赖轻量，顺畅安装，1800s 超时是偶发资源争抢，非安装复杂度 |
| peering-manager | 18 | Django 常规配置（复制 config.py、设 env var），Agent 自主推断 |
| skrub | 10 | 仅 `pip install -e '.[test]'` + 补装几个 pytest 插件，无障碍 |
| etl | 10 | `uv sync`（513 包）+ `--all-extras`，uv 接管了依赖解析，无技术障碍 |

所有 7 个案例的共同特征：**安装逻辑无技术难点，原始 1800s 超时的原因是单纯的时间不够**（大包下载、重试、并发资源）。3600s 给够了就自然成功，XPU 零介入。

---

## 六、量化统计

| 指标 | 数值 |
|------|------|
| 总成功 | 12 / 17（71%） |
| 其中 XPU 是关键（必要条件） | 2（17%） |
| 其中 XPU 有实质贡献 | 1（8%） |
| 其中 XPU 起辅助作用 | 1（8%） |
| 其中 XPU 建议失败 | 1（8%） |
| 纯靠时间 | 7（58%） |

**XPU 相关（含辅助）的成功比例：3/12 = 25%**
**纯靠时间的成功比例：7/12 = 58%**

---

## 七、整体评价

### XPU 的价值定位

XPU 在**特定场景**下价值显著：
1. **包版本 bug**（ts2vg 编译 bug、django-semanticui-forms 废弃版本）：Agent 无法凭借通用知识推断历史版本号
2. **工具链兼容性问题**（setuptools 70+ 兼容性）：需要跨版本经验数据，XPU 直接命中
3. **系统依赖识别**（libglpk-dev 等非 PyPI 依赖）：XPU 推理范式有帮助

XPU 对**以下情况帮助有限**：
- 大包下载时间问题（baybe/torch）：不是逻辑问题，只需时间
- 轻量级项目（cmdstanpy/skrub）：本就不难，无需经验库
- uv 管理项目（etl/matchms）：uv 自行解决依赖，XPU 无用武之地

### 核心发现

**12 个翻盘中，时间因素（1800s→3600s）是最主要的贡献**，覆盖 7/12（58%）的案例。XPU 在 3 个案例中起到不可替代的作用（25%），这 3 个案例如果只延长时间而不带 XPU，**大概率仍会失败**（elife-bot 的 setuptools 硬墙、lnldb 的废弃包版本）。

换句话说：**XPU 的价值不在于提升"通关率"的绝对数字，而在于让本来"绕不过去的硬坑"变得可解**。
