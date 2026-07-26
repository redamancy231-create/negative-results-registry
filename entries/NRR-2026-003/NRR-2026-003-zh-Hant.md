# NRR-2026-003: 方法論提取 — 22 個專案中 0 個模式達到 ≥3 來源穩定門檻

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-003 |
| **標題** | 22 個來源專案系統提取可複用方法論模式——無一達到 ≥3 來源穩定門檻 |
| **領域** | methodology-extraction |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | methodology-extraction-methodology |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-06-16 |

---

## 實驗概述

### 原始假設

> 從 22 個專案（11 個外部分析 + 7 個自建公開 + 4 個自建未公開）中系統提取 AI 協作的方法論模式。預期至少可識別 5–8 個跨 ≥3 來源專案的穩定模式，形成"方法論提取框架 v0.1"。

### 方法

八階段系統提取流程（Phase 0-7）：
- **來源專案**：22 個（11 外部開源/論文分析 + 11 自建）
- **提取方法**：每個專案獨立出證據卡 → 跨專案聚類 → 模式候選 → G5 追溯審計
- **穩定門檻**：≥3 個來源專案獨立出現
- **審查**：10 輪審查跨 GPT-5.5 / Kimi-K2.7 / Qwen3.7-Max / GLM-5.2 四種後端
- **元審查**：Kohli (2026-05) 獨立性框架 → 有效獨立視角約 2-3 個

### 預期結果

> 5-8 個方法論模式達到 ≥3 來源穩定門檻，形成可發布的"方法論提取框架 v0.1"。

### 實際結果

**G5 可追溯審計結論：所有 5 元件均未達到 ≥3 來源穩定門檻。** 22 個來源專案不足以支撐泛化的方法論模式提取。

| 指標 | 數值 |
|------|------|
| 效應量 | N/A（閾值未達到——0/5 元件通過） |
| 樣本量 | 22 個專案（11 外部 + 11 自建） |
| 使用的模型 | GPT-5.5, Kimi-K2.7, Qwen3.7-Max, GLM-5.2 |
| 審查發現 | Phase 5 雙輪正交審查 33 項發現 **0 重疊** |
| 有效獨立視角 | 約 2-3（按 Kohli 2026-05 框架） |

---

## 解讀與反思

### 為什麼會失敗？

三個系統性問題疊加：
1. **樣本同質性**：所有專案的提取和審查由同一操作者執行。來源專案雖涉及不同領域（量化金融、程式碼審查、檔案生成），但操作者的方法論自覺程度高度相關——沒有獨立的"對照樣本"
2. **n=22 太小**：提取跨專案模式需要的樣本量遠大於 22——尤其是專案差異性大（有的是幾萬行程式碼、有的是純檔案）
3. **穩定門檻定義過嚴**：≥3 個來源可能對方法論文獻提取來說門檻太高——學術文獻的跨研究模式提取通常需要 30-50 篇

### 學到了什麼？

1. **方法論提取比預期難一個數量級**——22 個專案看起來很多，實際遠遠不夠
2. **操作者獨立性是瓶頸**——如果所有來源專案的提取者是同一個人，模式發現會被這個人的認知偏好系統性約束
3. **"提取不出來"和"不存在"是兩回事**——22 專案 0 模式達標 ≠ 沒有可提取模式，可能是方法不夠好
4. **過程比結果有價值**——審查鏈（雙輪 33 發現 0 重疊 + 4 後端收斂實證）的學術價值超出了框架本身的產出
5. **誠實的陰性結果有獨立價值**——專案的核心交付物從"方法論提取框架"變成了"一篇關於'這件事有多難'的誠實報告"

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | prompts, logs, analysis-script, raw-output |

> 11 張公開證據卡在 [methodology-extraction-methodology/explorations/](https://github.com/redamancy231-create/methodology-extraction-methodology/tree/main/explorations)，10 輪審查報告在 `reviews/`，G5 審計在 `synthesis/phase4_traceability_audit.md`。11 個未公開來源專案的詳細證據卡不在公開倉庫中。

---

## 相關

### 後續是否成功？

無直接後續。專案在 v0.1 trial 狀態封存，結論是"我們證明了這件事有多難，但還沒有做到這件事該怎麼做"。框架本身作為一個"不可行性證明"（impossibility demonstration）有獨立價值。

### 相關連結

- [方法論提取方法論倉庫](https://github.com/redamancy231-create/methodology-extraction-methodology)
- [G5 可追溯審計](https://github.com/redamancy231-create/methodology-extraction-methodology/blob/main/synthesis/phase4_traceability_audit.md)
- [閉合後外部驗證附錄](https://github.com/redamancy231-create/methodology-extraction-methodology/blob/main/post-hoc-external-validation.md)
- [NRR-2026-001](../NRR-2026-001/NRR-2026-001.md) — Prompt-TDD A2（同操作者的另一個陰性結果）

### 標籤

`方法论提取`, `框架构建`, `跨项目模式`, `方法论失败`, `G5审计`, `审查链`, `22项目`, `不可行性证明`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
