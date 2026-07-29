# 审查报告：NRR 多语言同步流程 + 翻译校对

> 审查模型: GPT-5.6-Sol (via Codex CLI)
> 审查日期: 2026-07-29

> **结论先行**：提示词中的“zh-CN 23 条、en/zh-Hant 22 条”是事故发生时的历史状态。本次打开的工作副本中，根目录与 `docs/` 下的三语 registry 均为 23 条，均包含 `NRR-2026-023`，对应文件字节一致；`python scripts/validate_ci.py --skip-external-links` 与 `python scripts/update_readme.py --check` 均通过。但这只能证明产物后来被补齐，不能证明流程已经消除漂移风险。当前 CI 仍没有把多语言 ID 集合、翻译覆盖和根目录/`docs/` 镜像一致性设为强制不变量。
>
> **阻断性问题**：冻结预登记 `etf-pattern-match-pyo3/docs/nrr_gate2_preregistration.md`（hash `454873aa…`）列出的 12 项指标不包含 GPU；NRR 中文长文第 83–85 行也明确写明 GPU 是 Phase 5 后新增、未预登记、判定“不适用”。然而 NRR JSON、英文和正體中文摘要都把 GPU 写成第四项“冻结预登记预期”。这是事实错误，不是纯翻译润色，定稿前必须统一修正。

## D1: 多语言 JSON 同步 — 方案评估

### 1. 现状诊断

当前流程的真正问题不是前端语言切换逻辑，而是**生成产物过多、入口分散、校验不闭环**：

1. `entries/*/*.json` 是中文结构化权威源；英文和正體中文正文又来自翻译 Markdown。
2. `generate_registry.py` 可分别生成三种 registry，并由 `write_registry()` 同时写根目录和 `docs/`，形成 3 种语言 × 2 个位置的 6 份产物。
3. 缺翻译文件或缺字段时，语言生成器会回退到中文，但目前主要是打印 warning；如果维护者根本没有运行对应 `--lang` 命令，旧语言文件不会自动变化。
4. `validate_ci.py` 只覆盖中文源 JSON、内部链接和根目录 `registry.json` 的部分一致性；没有验证 `registry-en.json`、`registry-zh-Hant.json`、`docs/` 镜像、翻译文件覆盖率或 locale 间 ID 集合相等。
5. 语言 registry 目前只替换 7 个正文字段。`effect_size`、`sample_size`、`tags`、`links.label` 等仍可能保留简体中文。因此项目需要先定义“完整本地化”的字段边界，不能把“正文七字段已翻译”等同于“整条记录已本地化”。
6. `scripts/add_nrr023.py` 这类硬编码总数、日期和完整语言对象的一次性补救脚本，说明当前流程允许绕开统一生成器；它不应成为后续条目的模板。

### 2. 四个方案评分

评分以 10 分为满分，综合单一权威源、漂移概率、用户体验、迁移成本、可测试性和长期维护成本。

| 方案 | 评分 | 优点 | 主要问题 | 结论 |
|---|---:|---|---|---|
| **A：保留三份语言 JSON + 自动化** | **7/10（短期）**；**5.5/10（长期）** | 迁移小，前端改动少，可快速消除“忘跑命令” | 仍保留 6 份镜像产物；把 registry 生成塞进 `update_readme.py` 会形成职责倒置；若 CI 不校验，仍会漂移 | 适合作为止血方案，但应由更高层入口编排，而不是让 README 脚本承担构建副作用 |
| **B：单一中文 JSON，语言只切 UI** | **3/10** | 数据最简单，条目数绝不会因 locale 不同 | 已有翻译资产失效；英文/正體中文界面却展示简体正文，产品承诺和用户预期倒退 | 仅在项目明确降级为“中文内容 + 多语言 UI”时可选，不推荐作为默认方向 |
| **C：单一 JSON + 嵌套 `i18n`，前端按 locale 选择** | **7.5/10** | 一个 entries 数组，语言切换不会改变条目数；结构比 `title_en` 等扁平字段清晰 | 若仍需人工同时改 JSON 与 Markdown，会制造新的双权威源；需要 schema、fallback 和翻译状态设计 | 数据模型可行；必须明确翻译到底在 JSON 还是 Markdown 中维护 |
| **D：构建时从翻译 Markdown 合并到单一 registry** | **9/10** | 保留 Markdown 审阅体验，同时只发布一个确定性产物；最容易在 CI 中证明一致 | 需要一次前端和 schema 迁移；单文件略大，但目前 23 条规模可忽略 | **长期推荐**；实现时应采用 C 的嵌套对象，而不是大量语言后缀扁平字段 |

### 3. 推荐：组合 D 的构建方式与 C 的数据模型

四个选项并非完全互斥。最稳妥的长期形态是：

- 中文 JSON/Markdown 与翻译 Markdown 继续作为可审阅源文件；
- 构建阶段解析翻译并合并；
- 只生成一个 canonical registry；
- 前端始终加载同一个 entries 数组，再按字段和 locale 选择译文；
- 缺译文时按字段回退中文，但必须暴露翻译状态，不能静默伪装成“已完整翻译”。

建议结构如下，而不是 `title_en`、`title_zh_Hant` 横向扩张：

```json
{
  "id": "NRR-2026-023",
  "title": "中文默认标题",
  "hypothesis": "中文默认正文",
  "i18n": {
    "en": {
      "title": "...",
      "hypothesis": "...",
      "method": "...",
      "expected_result": "...",
      "actual_result": "...",
      "interpretation": "...",
      "lessons_learned": ["..."]
    },
    "zh-Hant": {
      "title": "...",
      "hypothesis": "..."
    }
  },
  "translation_status": {
    "en": "reviewed",
    "zh-Hant": "partial"
  }
}
```

前端的核心规则应是字段级选择：`entry.i18n?.[lang]?.[field] ?? entry[field]`。这样无论某个 locale 是否完成翻译，条目 ID 集合和总数都由同一个数组决定。

### 4. 必须固化为测试的不变量

无论先采用 A 还是直接迁移到 D+C，都应在 CI 中强制以下规则：

1. **ID 集合一致**：所有展示语言的 ID 集合必须等于 `entries/` 源集合；缺翻译只能触发字段 fallback，不能少一条记录。
2. **确定性生成**：相同源文件生成完全相同的字节；排序、换行和元数据不可依赖运行机器的偶然状态。
3. **翻译完整性可见**：解析器应输出每个 locale 的缺失文件、缺失字段和 fallback 字段清单。对要求“reviewed”的翻译，CI 中 warning 应升级为错误。
4. **翻译新鲜度**：建议在翻译文件 front matter 或生成元数据中记录源内容 digest；中文源字段变化而译文 digest 未更新时，CI 应报告 stale translation。
5. **镜像一致**：在仍保留根目录和 `docs/` 双副本的过渡期，两者必须做字节级比较。长期最好只保留一个部署权威位置，另一个由发布步骤复制，而不是人工维护。
6. **原子写入**：先在内存或临时目录生成并完成全部校验，再一次性 replace；任何一步失败都不得留下“中文已更新、英文未更新”的半成品。
7. **本地化字段契约**：明确哪些字段是稳定 slug（如 `domain`、`category`），哪些由 UI 映射，哪些必须进入 `i18n`。当前含中文的 `effect_size`、`sample_size`、`tags` 和 `links.label` 需要明确处理。

## D2: README 自动更新 — 简化建议

### 推荐结论

**最少出错的方案是“单一 Python 编排入口 + CI 同入口检查”；Makefile 只做薄包装；pre-commit 只做可选的本地提醒。**

不建议让 `update_readme.py` 在末尾隐式调用多个 registry 生成命令。该脚本名称和职责应保持“根据已构建数据更新 README”；真正的一站式入口应位于更高层，例如：

```text
python scripts/build_all.py          # 生成/更新全部派生产物
python scripts/build_all.py --check  # 不修改工作区，只验证产物无漂移
```

### 建议执行顺序

`build_all.py` 应按一个事务完成：

1. 校验源 JSON schema、文件名/ID 一致性和 ID 唯一性；
2. 解析英文、正體中文 Markdown，并校验 7 个正文必需字段；
3. 根据翻译策略执行严格失败或显式 fallback；
4. 生成单一 registry；若暂时沿用 A，则一次生成三语 registry；
5. 校验 locale ID 集合、条目数、字段覆盖率以及根目录/`docs/` 镜像；
6. 从刚生成的 canonical 数据更新三语 README marker 区域；
7. 在临时目录完成 schema/语义校验后，原子替换目标文件；
8. `--check` 模式在临时目录重建并逐字节比较，任何 diff 返回非零状态。

### Makefile、pre-commit 与 CI 的角色

- **Makefile**：可以提供 `make build`、`make check`，但只调用 Python 入口，不承载业务逻辑。仓库和维护环境包含 Windows，不能把正确性依赖在本机一定安装 GNU Make 上。
- **pre-commit**：可运行快速的 `build_all.py --check`，但不能作为唯一保障；hook 可以被跳过，也可能因自动改写并重新暂存文件而产生混乱。默认建议“检查并失败”，而不是在提交时静默改文件。
- **CI**：必须是最终权威。最佳做法是调用同一个 `--check` 入口，并对生成结果执行 `git diff --exit-code` 或等价字节比较。
- **README marker**：现有 marker 定点更新思路可以保留；README 只从 canonical registry 读取，不再自行推导另一套统计口径。

### 立即可做的低成本止血

在完成单一 registry 迁移前，至少应：

1. 新增 `scripts/build_all.py`，顺序调用三种语言生成和 README 更新；
2. 扩展 `validate_ci.py`，断言六份 registry 的 ID 集合完全一致、对应根目录/`docs/` 文件字节一致；
3. 在 `CLAUDE.md` 的“添加新条目”流程中写明唯一命令，删除“靠记忆运行三条 `--lang` 命令”的操作要求；
4. 停止使用硬编码条目数的一次性 append 脚本。

## D3: NRR-2026-023-en.md 翻译校对

### 1. 先修事实，再修英语

冻结预登记的 12 项指标是 DTW、cosine、standardize、pattern matching、batch/multithreading、RSS、build time、binary size、unsafe/dependency audit 等，**没有 GPU**。因此以下英文内容需要事实性改写：

- `Four frozen pre-registration expectations` 不能把 GPU 列为第 4 项；
- `GPU speedup >1.0 at all batch sizes` 不能写入 preregistered expected result；
- GPU 结果应标为 `exploratory` / `not preregistered`；
- `4/12 expectations were overturned` 必须说明“四项”具体是哪四项。若指 binary size、DTW、`standardize`、`pattern_match_single` 四个冻结指标，可以保留“four of the 12 frozen metrics”，但不得把 GPU 算入分子；若无明确映射，建议删掉 `4/12`，改为逐项列名。

这项冲突也存在于中文 JSON 和正體中文摘要中，不能只改英文文件后结束。

### 2. 逐字段结论

| 字段/表达 | 审查结论 | 建议 |
|---|---|---|
| 标题中的 `from C++ vs Rust benchmark` | 缺冠词，且标题名词堆叠偏重 | 用 `from a C++–Rust benchmark` 或 `from the C++ vs. Rust benchmark`；全项目统一连字符/标点风格 |
| `binary size exceeded` | 比 `binary size oversized` 自然，但 `exceeded` 缺少宾语/阈值 | 用 `the binary-size target was missed` 或 `binary size exceeded the preregistered limit` |
| `direction prediction overturned` | 能懂，但未说明是什么方向 | 用 `preregistered performance-direction expectations were overturned` 或 `direction-of-effect expectations were overturned` |
| `sub-microsecond measurement failed` | 过强，容易理解为没有数据或整次实验失败；实际是计时分辨率不足、cosine 不可判定、结论降级 | 用 `sub-microsecond measurements were inconclusive`；正文补充 `the timing method could not resolve the difference` |
| `GPU small-batch speedup negative` | 不自然且数学上易误导。0.2×、0.7× 是正数，只是低于 1.0 | 用 `the GPU was slower at small batch sizes` 或 `GPU speedup fell below 1.0 at small batch sizes` |
| `hypothesis-falsified` | 这是 schema 中的机器可读 category slug，不是待翻译自然语言 | 保留原 slug；前端/README 显示为 `Hypothesis Falsified`。NRR-2026-022 的 `methodology-failure` 是不同类别，不应为“对齐措辞”而互换 |
| `2.6–3.5×` | 当前格式正确、专业且清晰 | 保留 Unicode en dash 和乘号。只有项目明确要求纯 ASCII 时才改为 `2.6x–3.5x` |
| `cupy` / `numpy` | 品牌/项目名称大小写错误 | 改为 `CuPy` / `NumPy` |
| `numpy bridging` | 可理解但略口语 | 用 `NumPy interoperability`；若特指转换层，可用 `NumPy-to-C++ conversion overhead` |
| `allocator and exception semantics` | 语法可改善，而且当前证据只把部分因素列为候选根因，不能写成已证实原因 | 用 `differences in allocation behavior and exception-handling semantics`，并加 `possible contributors include…` |
| `LTO/strip` | 工程师能懂，但正式正文略简写 | 用 `LTO and symbol stripping`；若指 Cargo 配置，可同时保留选项名 |
| `Criterion-style stats` | 基本自然，`stats` 略口语 | 用 `Criterion-style statistical analysis` |
| `wrapper-internal layer timing` | 名词堆叠 | 用 `timing inside the wrapper` 或 `wrapper-internal timing` |

### 3. 建议英文关键段落

以下版本以冻结预登记文件为事实基准：

**Title**

> Four negative findings from a C++–Rust benchmark: the binary-size target was missed, preregistered performance-direction expectations were overturned, sub-microsecond measurements were inconclusive, and the GPU was slower at small batch sizes

**Original Hypothesis**

> This entry focuses on three preregistered assumptions: (1) the Rust binary would be less than 1.5× the size of the C++ binary; (2) the single-threaded performance of DTW, `standardize`, and `pattern_match_single` would remain within the preregistered equivalence range; and (3) 100 timed samples would be sufficient to resolve a 10% performance difference. The GPU experiment was added later and had no preregistered threshold.

**Method**

> Following the NRR Gate 2 preregistration (hash `454873aa`), the C++–Rust benchmark used 20 synthetic-corpus groups and five edge-case corpus groups, five warm-up iterations, 100 timed iterations per case, timing inside the wrapper, and a ±10% equivalence threshold. A separate exploratory GPU test was run on an RTX 4060 Laptop GPU with CuPy 14.1.1 at N = 100, 500, 1,000, and 5,000.

**Expected Result**

> The relevant preregistered targets were a binary-size ratio below 1.5×, single-threaded results within the defined equivalence range, and sufficient timing resolution to distinguish a 10% difference. No GPU speedup threshold was preregistered.

**Actual Result**

> (1) The binary-size ratio was 1.94×, above the preregistered limit of 1.5×. (2) DTW ratios were 0.29–0.39 (Rust was 2.6–3.5× faster); `standardize` was 0.67 and `pattern_match_single` was 0.53, all well outside the expected range. (3) Both cosine medians were 0 ns because of 100 ns timer quantization, and CoV exceeded 5% for the core metrics, so the conclusions were downgraded to indicative. (4) In the exploratory GPU test, end-to-end speedup was 0.2× at N = 100 and 0.7× at N = 500, with break-even near N = 1,000.

### 4. 其余语言质量建议

- `single performance` 应改为 `single-threaded performance of DTW, standardization, and single-pattern matching`。
- `100 samples sufficient for 10% discrimination` 应改为 `100 samples would be sufficient to detect/resolve a 10% performance difference`。
- 函数或代码标识应统一使用代码样式，如 `standardize`、`pattern_match_single`、`cosine`。
- `systematically over-optimistic` 对单个项目的证据强度偏高，可改为 `overly confident in this cross-language benchmark`。
- “allocator、exception semantics、NumPy bridging 导致差异累积”目前更像候选解释而非已验证因果，应使用 `may`、`possible contributors` 等限定词。
- `GPU speedup being negative is a textbook fact` 建议改为更中性的 `fixed launch and transfer overhead commonly makes GPUs slower for small workloads`。

## D4: NRR-2026-023-zh-Hant.md 翻译校对

### 1. 事实一致性同样必须先修

正體中文版本把 GPU 写成“四項凍結預登記預期”之一，并写 `GPU 全批量加速比 >1.0`，与冻结预登记和中文长文第 83–85 行冲突。应改成“前三项为预登记假设，GPU 为后加入的探索性观察”，并同步检查 JSON、英文和正體中文，避免三种表述继续分叉。

### 2. OpenCC 与台湾术语审查

- **没有发现已知的严重过度转换**。当前没有把“核查”机械改成不自然的“覈查”，也没有把统计“回归”误写成“迴歸”。
- **`迴圈`** 符合台湾 CS 惯用语，不是错误的过度转换。
- **`亞微秒`** 可接受；`次微秒` 也有人使用，项目选一种后保持一致即可。
- **`採樣`** 可接受；若强调测量取样，`取樣` 也自然。不要在同一仓库混用三四种写法。
- **`二進位`** 比 `二進制` 更符合台湾语境；但本条具体指扩展模块/执行产物大小时，`執行檔大小` 或 `二進位檔大小` 更明确。
- `了解` 与 `瞭解` 都可见，不应只为“正體化”强制机械替换；重点是项目风格一致。

### 3. 逐字段结论

| 当前表达 | 问题 | 建议 |
|---|---|---|
| `C++ vs Rust benchmark` | 中英夹杂可接受，但台湾正式技术文档更自然的写法是中文主干 | `C++ 與 Rust 基準測試` |
| `二進位大小超標` | 基本正确，但“超标”偏简体行政用语，且没说明预登记门槛 | `執行檔大小未達預登記門檻` 或 `二進位檔大小超出預登記上限` |
| `預期方向被推翻` | 可理解，略泛 | `預登記效能方向遭推翻` |
| `亞微秒測量失效` | “失效”过强；实际为分辨率不足、无法判定 | `亞微秒量測無法判定` 或 `亞微秒量測方法不足以分辨差異` |
| `GPU 小批量加速比為負` | `小批量` 偏简体；0.2×/0.7× 不是负数 | `GPU 在小批次下反而變慢` 或 `小批次下 GPU 加速比低於 1` |
| `GPU 全批量加速比 >1.0` | `全批量` 会被理解为 full-batch，不等于“所有批次大小”；且本句事实层面应从预登记预期中删除 | 若只讨论语言应写 `所有批次大小下 GPU 加速比均 > 1.0`；本条最终应改为“GPU 無預登記門檻” |
| `20 組合成分組 + 5 組邊緣分組` | `合成分組` 丢失 corpus 语义，`邊緣` 容易被理解为 peripheral | `20 組合成語料群組 + 5 組邊界案例語料群組` |
| `按 NRR 門 2 預登記` | “门 2”是生硬直译 | `依 NRR Gate 2 預登記` 或 `依 NRR 第 2 道門檻的預登記` |
| `wrapper-internal 層計時` | 结构生硬 | `wrapper 內部計時` 或 `在 wrapper 內部層級進行計時` |
| `Criterion 型統計` | 能懂但略机械 | `Criterion 風格的統計分析` |
| `allocator、exception 語義、numpy 橋接` | 大小写、语言混杂且把候选因素写成确定因果 | `記憶體配置行為、例外處理語意與 NumPy 互通成本可能累積`，并保留“可能”限定 |
| `拐點 N≈1000` | `拐點` 偏大陆用法，且这里是 speedup = 1 的交叉点 | `損益平衡點約為 N = 1,000` 或 `臨界點約為 N = 1,000` |
| `LTO/strip` | 可读但偏命令速记 | `LTO 與符號剝除（symbol stripping）` |

### 4. 建议正體中文关键段落

**標題**

> C++ 與 Rust 基準測試中的四項陰性發現：執行檔大小未達預登記門檻、預登記效能方向遭推翻、亞微秒量測無法判定，以及 GPU 在小批次下反而變慢

**原始假設**

> 本條目聚焦三項預登記假設：(1) Rust 執行檔大小低於 C++ 的 1.5 倍；(2) DTW、`standardize` 與 `pattern_match_single` 的單執行緒效能落在預登記的等效範圍內；(3) 100 次計時取樣足以分辨 10% 的效能差異。GPU 實驗於後續階段新增，沒有預登記門檻。

**方法**

> 依 NRR Gate 2 預登記（雜湊值 `454873aa`）執行 C++ 與 Rust 基準測試：使用 20 組合成語料群組與 5 組邊界案例語料群組，每組預熱 5 次並正式計時 100 次，在 wrapper 內部進行計時，等效門檻為 ±10%。另以 RTX 4060 Laptop GPU 與 CuPy 14.1.1 進行探索性 GPU 測試，N = 100、500、1,000、5,000。

**預期結果**

> 相關的預登記目標為：執行檔大小比低於 1.5×、單執行緒結果落在既定等效範圍內，以及計時方法足以分辨 10% 的差異。GPU 沒有預登記的加速門檻。

**實際結果**

> (1) 執行檔大小比為 1.94×，未達低於 1.5× 的預登記門檻。(2) DTW 比值為 0.29–0.39（Rust 快 2.6–3.5 倍），`standardize` 為 0.67，`pattern_match_single` 為 0.53，皆明顯超出預期範圍。(3) cosine 的雙方中位數皆為 0 ns，受 100 ns 計時量化影響而無法判定；核心指標的 CoV 皆高於 5%，因此結論降級為傾向性。(4) 探索性 GPU 測試在 N = 100 時端到端加速比為 0.2×，N = 500 時為 0.7×，損益平衡點約為 N = 1,000。

### 5. 数字与标点

- `2.6–3.5×`、`0.90 ≤ ratio ≤ 1.10` 的符号本身没有问题；乘号 `×` 和 en dash `–` 建议保留。
- 中英文/数字之间的空格目前大体可读，但应制定仓库级样式：例如统一 `N < 1,000`，不要混用 `N<1000`、`N = 1000` 和 `N≈1000`。
- 中文正文优先使用全角标点；代码名、ratio、CoV、GPU 型号等保留半角。首次出现 CoV 时可写“變異係數（CoV）”。
- `CuPy`、`NumPy`、`PyO3` 等专名必须统一正确大小写。

## D5: 整体建议

### 1. 根本问题与最终取舍

根本问题不是“维护者少跑了一条命令”，而是系统把同一事实复制到多个可独立陈旧的产物中，却没有用一个原子构建和 CI 不变量把它们锁在一起。继续增加操作文档不能从根本上解决；应让“漏跑语言命令”在设计上不再可能。

**最终推荐：**

- **短期**：采用改良版 A——新增顶层 `build_all.py`，一次生成全部 registry 和 README，并扩展 CI 校验六份产物。
- **长期**：迁移到 **D+C**——构建时从翻译 Markdown 合并到单一、嵌套 `i18n` 的 registry，前端只加载一个文件，字段级 fallback。
- **不推荐 B**，除非维护者明确宣布英文/正體中文仅翻译 UI，不再提供条目正文翻译。

### 2. 三语架构是否过度设计

**三种语言本身不一定过度设计；当前“3 语言 × 2 位置 × 多个手工命令”的发布方式是过度设计。**

对于主要面向中文读者的项目，建议把多语言服务等级分层，而不是在“全部人工翻译”与“全部删除”之间二选一：

1. zh-CN 为必需且权威；
2. en/zh-Hant 始终展示同一条目集合，未翻译字段回退 zh-CN，并显示 `missing` / `machine-draft` / `reviewed` 状态；
3. 标题、摘要和关键结论优先翻译，长正文可按访问量、引用需求或维护者资源分批完成；
4. 正體中文与简体中文的转换成本较低，但技术术语仍需人工抽查；英文的事实校对和技术润色成本明显更高，应优先保证高价值条目，而不是追求表面 100% 覆盖；
5. 用访问量、外部引用和翻译维护时间评估 ROI。若长期几乎没有英文流量，再把英文降为标题/摘要级；不应因当前流水线脆弱就直接删除已有 23 条翻译资产。

### 3. 建议实施优先级

**P0 — 定稿前必须完成**

1. 以冻结预登记文件为准，删除 NRR-2026-023 中“GPU 是第四项冻结预登记预期”的说法；把 GPU 明确标为后加入的探索性结果。
2. 审核 `4/12` 的分子映射；若是 binary size、DTW、`standardize`、`pattern_match_single`，应直接列名，避免与“四项阴性发现”混淆。
3. 同步修正中文 JSON、英文 Markdown、正體中文 Markdown及重新生成的 registry，避免只修一个语言版本。
4. 修正 `CuPy`、`NumPy`、small-batch、speedup below 1.0 等术语。

**P1 — 防止同类事故再次发生**

1. 建立唯一的 `build_all.py` / `--check` 入口；
2. CI 强制比较所有 locale ID 集合、翻译字段覆盖、镜像字节和 README 漂移；
3. 写入改为临时生成 + 全量验证 + 原子替换；
4. 更新 `CLAUDE.md` 的新增条目流程，使维护者只需要记一个命令。

**P2 — 降低长期维护成本**

1. 迁移为单一 nested-`i18n` registry；
2. 删除或停止跟踪可由发布流程复制的重复 registry；
3. 为翻译增加状态与源 digest，检测陈旧译文；
4. 明确 `effect_size`、`sample_size`、`tags`、`links.label` 的本地化策略。

### 4. 额外数据质量旁注

- `NRR-2026-023.json` 的 `reproducibility.artifacts_available` 中 `"data"` 重复，应去重。
- 当前语言 registry 中存在非七个正文字段的简体中文残留。这不是翻译 Markdown 解析失败，而是 i18n 字段边界没有定义。
- 当前磁盘上的 registry `metadata.last_updated` 为 **2026-07-30**，晚于本报告日期 **2026-07-29**。应核对机器时钟、时区或快照来源；更根本地，生成元数据应来自确定性输入（例如最新条目日期或显式 `SOURCE_DATE_EPOCH`），不要无条件采用构建机墙钟时间。
- 现有两项检查均通过，但它们尚未覆盖上述多语言不变量，因此不能把“CI 绿”解释为“多语言同步流程已被证明正确”。

### 5. 最终审查结论

- **架构**：当前补丁恢复了 23/23/23 的表面一致性，但流程仍需修改；建议“短期 A、长期 D+C”。
- **README 自动化**：采用单一 Python 编排入口，Makefile 仅作别名，pre-commit 非权威，CI 使用同一 `--check`。
- **英文翻译**：需要修改；主要问题是 GPU 预登记事实错误、`failed`/`negative speedup` 语义过强或不准确，以及品牌大小写和若干名词堆叠。
- **正體中文翻译**：需要修改；OpenCC 没有明显灾难性过转换，但存在 `全批量`、`小批量`、`門 2`、`加速比為負` 等语义或台湾用语问题。
- **合并建议**：**Request changes**。先修复 NRR-2026-023 的事实一致性，再落地自动化不变量；不要仅靠再次手工补齐生成文件。