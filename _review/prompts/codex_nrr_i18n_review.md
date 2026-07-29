# 审查任务：NRR 条目新增流程 — 多语言同步 + 自动化改进 + 翻译校对

> **审查模型**: GPT-5.6-Sol (via Codex CLI)
> **审查角度**: 流程审查——现有方案是否有更好替代？翻译是否正确？
> **审查对象**: negative-results-registry 仓库的条目新增流程和 NRR-2026-023 翻译文件

## 一、背景

negative-results-registry 是一个 AI 协作阴性结果登记册，支持三语（zh-CN / EN / zh-Hant）。网站通过 `docs/index.html` 加载 JSON 数据渲染条目列表。

最近新增 NRR-2026-023 条目时出现了两个问题：
1. 切换语言后条目数量不同步（zh-CN 显示 23 条，en/zh-Hant 显示 22 条）
2. 需要手动维护 6 个 JSON 文件（根目录 + docs/ 各 3 个）+ 手动更新三语 README

## 二、当前架构

### 2.1 数据流

```
entries/NRR-YYYY-NNN/
├── NRR-YYYY-NNN.json          ← 中文权威数据
├── NRR-YYYY-NNN.md            ← 中文 Markdown
├── NRR-YYYY-NNN-en.md         ← 英文翻译 Markdown（可选）
└── NRR-YYYY-NNN-zh-Hant.md    ← 正體中文翻译 Markdown（可选）

scripts/generate_registry.py          ← 读取 entries/ → 生成 registry.json
scripts/generate_registry.py --lang en ← 读取翻译 Markdown → 生成 registry-en.json
scripts/generate_registry.py --lang zh-Hant

           write_registry() 双写 → 根目录 + docs/
```

新增一个条目需要跑 3 条命令，产出 6 个 JSON（3 语言 × 2 位置）。

### 2.2 前端语言切换

`docs/index.html` 第 476-483 行：

```javascript
function getDataSources() {
  var lang = state.lang;
  var base = lang === DEFAULT_LANG ? "registry.json" : "registry-" + lang + ".json";
  return [
    "./" + base,
    "../" + base,
    "https://raw.githubusercontent.com/redamancy231-create/negative-results-registry/main/" + base
  ];
}
```

每种语言加载不同的 JSON 文件。如果 `registry-en.json` 不存在或条目数不一致，切换语言后会显示不同数量。

### 2.3 当前解决方案

`generate_registry.py --lang en` 遇到缺少翻译 Markdown 的条目时，自动 fallback 到中文 JSON 原文（第 310-316 行）。但需要**记得**跑 `--lang` 命令——如果忘了，语言文件不会自动更新。

## 三、需要你审查的两份翻译文件

### 3.1 entries/NRR-2026-023/NRR-2026-023-en.md

```
# NRR-2026-023: Four negative findings from the C++ vs Rust benchmark

## Basic Information

| Field | Content |
|------|------|
| **Entry ID** | NRR-2026-023 |
| **Title** | Four negative findings from C++ vs Rust benchmark: binary size exceeded, direction prediction overturned, sub-microsecond measurement failed, GPU small-batch speedup negative |
| **Domain** | benchmarking |
| **Category** | hypothesis-falsified |
| **Submitter** | Acerolaorion |
| **Source Project** | etf-pattern-match-pyo3 |
| **Source Authors** | redamancy231-create |
| **Analyst** | Acerolaorion |
| **Date** | 2026-07-29 |

---

## Experiment Overview

### Original Hypothesis

> Four frozen pre-registration expectations: (1) Rust binary < C++ ×1.5, (2) single-thread DTW/standardize/pattern single performance within ±10%, (3) 100 samples sufficient to distinguish ±10% performance difference, (4) GPU cupy acceleration yields positive speedup at any batch size.

### Method

C++ vs Rust benchmark executed per NRR Gate 2 pre-registration (hash 454873aa): 20 synthetic corpus groups + 5 edge corpus groups, 5 warmup + 100 timed iterations, wrapper-internal layer timing, ±10% threshold. GPU testing on RTX 4060 Laptop + cupy 14.1.1, N = 100/500/1000/5000.

### Expected Result

> Binary <1.5×, single-thread performance within ±10% (0.90 ≤ ratio ≤ 1.10), 100 samples sufficient for 10% discrimination, GPU speedup >1.0 at all batch sizes.

### Actual Result

(1) Binary ratio 1.94×, does not satisfy <1.5×. (2) DTW ratio 0.29–0.39 (Rust 2.6–3.5× faster), standardize 0.67, pattern single 0.53—all far beyond ±10% tie range. (3) cosine median=0 ns (100 ns quantization), all core indicators CoV >5% → conclusions downgraded to indicative. (4) GPU N=100 end-to-end 0.2×, N=500 0.7×, break-even N≈1000.

### Why Did It Fail?

Pre-registration direction predictions were systematically over-optimistic in cross-language benchmarks—same algorithm ≠ same performance. Sub-microsecond measurement requires loop amplification, not independent sampling. GPU speedup being negative is a textbook fact, but seeing 0.2× firsthand remains educational.

### What Did We Learn?

1. Pre-registration is not prediction—it exposes blind spots: 4/12 expectations were overturned
2. In cross-language benchmarks, same algorithm ≠ same performance: Rust/C++ differences in allocator, exception semantics, and numpy bridging accumulate
3. Benchmark methodology needs tiering: millisecond-level (independent sampling), microsecond-level (loop amplification), sub-microsecond (Criterion-style stats)
4. GPU acceleration has a clear minimum data threshold: N<1000, kernel launch + PCIe transfer dominate and speedup can be negative
5. Binary size expectations must be set with tuning parameters in mind—should not assume Rust ≈ C++ size without LTO/strip
```

### 3.2 entries/NRR-2026-023/NRR-2026-023-zh-Hant.md

```
# NRR-2026-023: C++ vs Rust benchmark 中的四項陰性發現

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-023 |
| **標題** | C++ vs Rust benchmark 中的四項陰性發現：二進位大小超標、預期方向被推翻、亞微秒測量失效、GPU 小批量加速比為負 |
| **領域** | benchmarking |
| **類型** | hypothesis-falsified |
| **提交者** | Acerolaorion |
| **來源專案** | etf-pattern-match-pyo3 |
| **來源作者** | redamancy231-create |
| **分析師** | Acerolaorion |
| **日期** | 2026-07-29 |

---

## 實驗概述

### 原始假設

> 四項凍結預登記預期——(1) Rust 二進位 < C++ ×1.5，(2) DTW/standardize/pattern single 單執行緒效能打平（±10%），(3) 100 次採樣足夠區分 ±10% 效能差異，(4) GPU cupy 加速在任意批量下均有正向收益。

### 方法

按 NRR 門 2 預登記（hash 454873aa）執行 C++ vs Rust benchmark：20 組合成分組 + 5 組邊緣分組，預熱 5 次/計時 100 次，wrapper-internal 層計時，±10% 閾值。GPU 測試使用 RTX 4060 Laptop + cupy 14.1.1，N = 100/500/1000/5000。

### 預期結果

> 二進位 <1.5×，單執行緒效能打平（0.90 ≤ ratio ≤ 1.10），100 次採樣可區分 10% 差異，GPU 全批量加速比 >1.0。

### 實際結果

(1) 二進位 1.94×，不滿足 <1.5×。(2) DTW ratio 0.29–0.39（Rust 快 2.6–3.5 倍），standardize 0.67，pattern single 0.53——全部遠超出 ±10% 打平區間。(3) cosine median=0 ns（100 ns 量化），所有核心指標 CoV >5% 致結論降級為傾向性。(4) N=100 時 GPU 端到端 0.2×，N=500 時 0.7×，拐點 N≈1000。

### 為什麼會失敗？

預登記的方向預測在跨語言 benchmark 中系統性偏樂觀——同演算法不等於同效能。亞微秒測量需要迴圈放大而非獨立採樣。GPU 加速比為負是教科書級事實，但在實際專案中親眼看到 0.2× 仍具有教育意義。

### 學到了什麼？

1. 預登記不是預測——是暴露盲區：4/12 指標預期被推翻
2. 跨語言 benchmark 中同演算法不等同效能：Rust 和 C++ 在 allocator、exception 語義、numpy 橋接上的差異會累積
3. 基準測試方法需要分層：毫秒級（獨立採樣）、微秒級（迴圈放大）、亞微秒級（Criterion 型統計）
4. GPU 加速有明確資料規模下限：N<1000，kernel launch + PCIe 傳輸主導耗時，加速比可能為負
5. 二進位大小的預登記預期必須在了解調優參數的前提下設定——不應在未做 LTO/strip 時假設 Rust ≈ C++ 大小
```

## 四、审查问题

### D1: 架构改进 — 多语言 JSON 同步

当前方案：`registry.json` + `registry-en.json` + `registry-zh-Hant.json`（3 个独立 JSON，需手动同步）。出了两次问题（忘跑 `--lang`、语言文件条目数不一致）。

**请评估以下替代方案，给出推荐和理由：**

- **方案 A（当前+自动化）**: 保持 3 个 language-specific JSON，但在 `update_readme.py` 末尾自动调用 `generate_registry.py --lang en/zh-Hant`，形成一站式入口
- **方案 B（单一 JSON）**: `index.html` 永远只加载 `registry.json`，语言切换只改变 UI 标签文本和域名/分类翻译（`labelFor()`），条目正文统一显示中文。删除 `registry-en.json` 和 `registry-zh-Hant.json`
- **方案 C（前端运行时翻译）**: 保持单一 JSON，但在 `index.html` 中为可翻译字段（title/hypothesis/method 等）增加一个 `i18n` 嵌套对象，前端根据当前语言选择对应译文
- **方案 D（构建时合并）**: 脚本从翻译 Markdown 提取译文，直接写入主 `registry.json` 的每个条目中（每个条目增加 `title_en`/`hypothesis_en` 等字段），前端从一个 JSON 中选语言，不再需要多文件

### D2: 架构改进 — README 自动更新

当前方案：手动跑 `update_readme.py` 更新三语 README 的 badge 和条目表。新增条目后需要跑 4 条命令。

**请评估如何简化**：是否应该合并为一个 Makefile target / 单一脚本入口 / `pre-commit` hook？哪种方案最少出错？

### D3: 翻译校对 — NRR-2026-023-en.md

逐字段校对英文翻译是否准确、语法是否正确、术语是否一致：
- [ ] 标题翻译是否准确传达了四项阴性发现的语义？
- [ ] `binary size exceeded` 是否比 `binary size oversized` 更好？
- [ ] `sub-microsecond measurement failed` 是否准确描述了"亚微秒指标测量方法失效"？
- [ ] `direction prediction overturned` 是否准确表达了"预期方向被推翻"？
- [ ] `hypothesis-falsified` 作为 category 的翻译是否与现有条目（如 NRR-2026-022）一致？
- [ ] 数字 `2.6–3.5×` 是否应该写为 `2.6–3.5×` vs `2.6x–3.5x`？
- [ ] 技术术语（allocator, exception semantics, numpy bridging, LTO/strip）是否在英文语境下自然？

### D4: 翻译校对 — NRR-2026-023-zh-Hant.md

逐字段校对正體中文翻译：
- [ ] OpenCC 从简体到正體的转换是否有过度转换？（已知风险：了解→瞭解、核查→覈查、回归→迴歸）
- [ ] "亞微秒"、"迴圈"、"採樣"等术语是否符合台湾 CS/量化领域惯用表达？
- [ ] "二進位"是否比"二進制"更适合台湾语境？
- [ ] 数字格式和标点符号是否符合正體中文规范？

### D5: 整体建议

- [ ] 是否有更好的方法来解决"新增条目需要手动同步多种语言"这个根本问题？
- [ ] 当前 3 语言架构是否过度设计？对于一个主要面向中文读者的项目，en/zh-Hant 翻译的投资回报比如何？

## 输出格式

```markdown
# 审查报告：NRR 多语言同步流程 + 翻译校对

> 审查模型: GPT-5.6-Sol (via Codex CLI)
> 审查日期: 2026-07-29

## D1: 多语言 JSON 同步 — 方案评估
（对 A/B/C/D 四个方案打分并推荐）

## D2: README 自动更新 — 简化建议

## D3: NRR-2026-023-en.md 翻译校对

## D4: NRR-2026-023-zh-Hant.md 翻译校对

## D5: 整体建议
```

---

*提示词生成: DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-29*
