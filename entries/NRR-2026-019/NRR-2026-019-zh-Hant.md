# NRR-2026-019: GitNexus CALLS 邊的同檔案覆蓋盲區

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-019 |
| **標題** | GitNexus CALLS 邊同一檔案內部方法呼叫擷取率僅 3/81+ 和 0/17——基於索引斷言模組內部耦合不可靠 |
| **領域** | benchmarking |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | GitNexus |
| **來源作者** | Abhigyan Patwari |
| **分析者** | Acerolaorion |
| **日期** | 2026-07-22 |

---

## 實驗概述

### 原始假設

> GitNexus 程式碼知識圖譜的 CALLS 邊應能可靠擷取方法間呼叫關係，包括同一檔案內部呼叫。預期索引覆蓋率 ≥80%，可用於斷言模組內部耦合度。

### 方法

對 docx-pipeline 專案兩個核心模組進行手動進行原始碼 grep 交叉驗證：PurePythonConverter（1,213行, 36個方法）和 MermaidRenderer（677行, 17個方法），對比 GitNexus 索引的 CALLS 邊數量與實際原始碼呼叫鏈。

### 預期結果

> GitNexus CALLS 邊覆蓋同一檔案內部呼叫的 ≥80%。

### 實際結果

PurePythonConverter：僅擷取 **3 條**同一檔案 CALLS 邊（覆蓋率 ≤3.7%）。MermaidRenderer：擷取 **0 條**同一檔案 CALLS 邊（覆蓋率 0%）。基於 GitNexus CALLS 邊斷言模組內部耦合度不可靠。

| 指標 | 數值 |
|------|------|
| 效應量 | PurePythonConverter ≤3.7%（3/81+）；MermaidRenderer 0%（0/17） |
| 樣本量 | 2 個模組 × 2 種檢測方法 |
| 使用的工具 | GitNexus |

---

## 解讀與反思

### 為什麼會失敗？

CALLS 邊在同一檔案內的索引策略與跨檔案呼叫使用不同檢測準確度。不是 bug——是索引策略在不同維度的精確度差異。但對方法論提取而言，盲目相信索引資料會導致對模組複雜度的系統性低估。

### 學到了什麼？

1. GitNexus CALLS 邊同檔案覆蓋率可低至 0%——不能基於 CALLS 邊數量斷言模組內部耦合度
2. AI 工具評估不能僅靠靜態原始碼分析——需要對照實驗才能發現盲區
3. 跨檔案 IMPORT/EXTENDS 邊比同一檔案 CALLS 邊可靠
4. 對任何分析工具的聲稱都需要交叉驗證——"3 條 CALLS"可能是真值的 3.7%

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | fully-reproducible |
| **可用產物** | code, logs |

> **第三方分析條目。** 重現步驟：在 docx-pipeline 倉庫執行 GitNexus 索引 → 對比 CALLS 邊數量 → 以 grep 手動統計。

---

## 相關

### 後續是否成功？

跨檔案 IMPORT/EXTENDS 邊置信度高於同一檔案 CALLS 邊。應對策略：跨檔案用 GitNexus，同一檔案內使用原始碼 grep。

### 相關連結

- [GitNexus 分析專案](https://github.com/redamancy231-create/methodology-extraction-methodology)
- [GitNexus CALLS 邊覆蓋盲區（methodology-handbook）](https://github.com/redamancy231-create/methodology-handbook)

### 標籤

`GitNexus`, `CALLS边`, `索引覆盖`, `代码知识图谱`, `源码交叉验证`, `第三方分析`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
