# NRR-2026-011: 多模型自修正系統的獨立性侷限

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-011 |
| **標題** | 多模型自修正系統的獨立性侷限——9 模型評審團有效獨立票僅 ~2（Kohli 2026） |
| **領域** | multi-model-collaboration |
| **分類** | ceiling-effect |
| **提交者** | Acerolaorion |
| **來源專案** | Kohli 2026 / CrossCheck |
| **來源作者** | Kohli |
| **分析者** | Acerolaorion |
| **日期** | 2026-07-23 |

---

## 實驗概述

### 原始假設

> 在 AI 編碼系統中引入多個不同 LLM 後端進行交叉審查和自修正，預期能實現真正的獨立驗證——審查者之間的發現應高度互補，且評審團整體優於任一單模型。

### 方法

對 CrossCheck（sburl/CrossCheck，多模型 AI 編碼自主迴圈系統）進行了方法論分析，結合 Kohli (2026-05) 論文（9 個尖端 LLM 評審團的獨立性量化）和 Kuai et al. (2026-04)（18 個 LLM 的行為糾纏分析）進行交叉驗證。本專案 Phase 5 雙輪審查（GPT-5.5 + Qwen3.7-Max）提供對照資料。

### 預期結果

> 多個不同後端的模型組成的評審團應提供接近 N 個獨立視角；預期有效獨立票數 ≥5（9 個模型中）。

### 實際結果

Kohli (2026-05)：**9 個尖端 LLM 評審團，有效獨立票僅 ~2 票。單一最佳評審的表現追平甚至超過整個評審團。** 本專案 Phase 5 雙輪審查：GPT-5.5 17 項 + Qwen 16 項 = 33 項中 0 重疊——互補但也提示邊際遞減。Kuai et al. (2026-04) 進一步證實 18 個 LLM 存在廣泛"行為糾纏"。

| 指標 | 數值 |
|------|------|
| 效應量 | 9→2 有效獨立票（Kohli）；本專案 5 模型有效獨立視角約 2-3 |
| 樣本量 | 9 個 LLM（Kohli）+ 本專案 5 模型 |
| 使用的模型 | GPT-5.5, Qwen3.7-Max, Kimi-K2.7, GLM-5.2, Claude Opus 4.8 |

---

## 解讀與反思

### 為什麼會失敗？

不是多模型審查無效——恰恰相反，33 項 0 重疊證明了互補性。但模型間共享訓練資料、蒸餾流程與對齊管線，因而產生了隱性相依性，使得"加更多模型"的邊際收益在 ~2-3 個有效獨立視角後急劇遞減。4-5 個不同供應商的模型可能已接近有效上限。

### 學到了什麼？

1. **9 個 LLM 評審團的有效獨立票僅 ~2**——模型間共享訓練資料和評估基準，會產生隱性相依性
2. **多模型審查的價值集中在前 2-3 個不同供應商的模型**——之後邊際收益急劇遞減
3. **"不同 CLI house"≠"獨立"**——即使不同公司提供的模型，也可能共享訓練資料和基準
4. **多模型審查的實證價值在於發現彼此互補的盲區**（33 發現 0 重疊），而非聲稱"全部獨立"

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | logs, analysis-script, raw-output |

> Kohli (2026-05) 論文在 [arxiv.org/abs/2605.29800](https://arxiv.org/abs/2605.29800)。本專案相關分析在 [methodology-extraction-methodology](https://github.com/redamancy231-create/methodology-extraction-methodology)。**這是第三方分析條目——原作者並非本登記冊的提交者。**

---

## 相關

### 後續是否成功？

多模型審查在 2-3 個有效獨立視角內仍然有效。關鍵在於不聲稱"全部獨立"，也不在邊際收益遞減區繼續追加模型。

### 相關連結

- [Kohli (2026-05) — Nine Judges, Two Effective Votes](https://arxiv.org/abs/2605.29800)
- [Kuai et al. (2026-04) — How Independent are LLMs?](https://arxiv.org/abs/2604.07650)
- [閉合後外部驗證附錄](https://github.com/redamancy231-create/methodology-extraction-methodology/blob/main/post-hoc-external-validation.md)

### 標籤

`多模型审查`, `独立性`, `Kohli2026`, `有效独立票`, `行为纠缠`, `边际递减`, `第三方分析`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
*分析來源：Kohli (2026-05), Kuai et al. (2026-04), CrossCheck (sburl/CrossCheck)*
