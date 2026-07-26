# NRR-2026-021: 方法論提取框架適用性梯度衰減

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-021 |
| **標題** | 方法論提取框架適用性隨專案方法論自覺梯度急速衰減——自有100%→有論文69%→純程式碼37.5% |
| **領域** | methodology-extraction |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | NPGS |
| **來源作者** | baopinshui |
| **分析者** | Acerolaorion |
| **日期** | 2026-07-23 |

---

## 實驗概述

### 原始假設

> 方法論提取框架應能從未知開源專案中提取有意義的方法論模式——即使專案沒有 AI 協作記錄，也應能從被動痕跡中提取可用訊號。預期最低梯度（純程式碼專案）可提取率 ≥50%。

### 方法

對三個梯度的專案執行完整 8 元件提取：自有專案（★★★★★）、ml-quant-trading（★★★，有論文+CI+測試）、NPGS（★，零方法論檔案）。

### 預期結果

> 三梯度可提取率漸進下降但保有一定基線——NPGS ≥50%（4/8）。

### 實際結果

**梯度 100%→69%→37.5%。** NPGS 5/8 元件空白。能提取的 3 個元件用 GitNexus 同樣可取得——框架在被動痕跡維度上**無增量價值**。

| 指標 | 數值 |
|------|------|
| 效應量 | 可提取率梯度 100%→69%→37.5%；NPGS 5/8 元件空白 |
| 樣本量 | 3 個專案 × 3 梯度 × 8 元件 |
| 使用的模型 | DeepSeek-V4-Pro, GitNexus, Codex GPT-5.5 |

---

## 解讀與反思

### 為什麼會失敗？

框架的隱含假設——"來源專案知道自己做了什麼並記錄了下來"——在絕大多數開源專案中不成立。框架不是"探測器"，是"整理器"——它不能發現不存在的資訊。

### 學到了什麼？

1. 框架適用對象極為狹窄——僅對 AI 協作自覺極強的專案有效
2. 可提取率與來源專案方法論自覺正相關（★★★★★=100%→★=37.5%）
3. 框架在被動痕跡維度無增量價值——能用 GitNexus 取得的不需要框架
4. 框架價值定位應從"發現"修正為"歸納"——它不是探測器，是整理器

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | logs, analysis-script, raw-output |

> **第三方分析條目。** NPGS 和 ml-quant-trading 證據卡在 methodology-extraction-methodology/explorations/。

---

## 相關

### 後續是否成功？

框架在自有專案群中可提取率接近 100%——證明框架設計有效，只是適用範圍比初始假設窄。

### 相關連結

- [NPGS 證據卡](https://github.com/redamancy231-create/methodology-extraction-methodology/blob/main/explorations/evidence_card_npgs_external.md)
- [ml-quant-trading 證據卡](https://github.com/redamancy231-create/methodology-extraction-methodology/blob/main/explorations/evidence_card_ml_quant_trading.md)

### 標籤

`方法论提取`, `框架适用性`, `梯度衰减`, `NPGS`, `被动痕迹`, `第三方分析`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
