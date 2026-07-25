# 為什麼要記錄陰性結果？

[![中文](https://img.shields.io/badge/lang-中文-red)](../README.md)
[![English](https://img.shields.io/badge/lang-English-blue)](../en/methodology.md)

> 科學界有一個「檔案抽屜問題」（file drawer problem）：陽性結果發表，陰性結果塞進抽屜。結果是發表偏誤——我們從文獻中看到的永遠是「什麼有效」，很少看到「什麼無效」。
>
> AI 協作領域同樣如此。GitHub 上充斥著「我用 AI 做了 X」的展示，但幾乎沒有人記錄「我試了 X，失敗了」。

## 為什麼陰性結果有價值

### 1. 防止後來者重蹈覆轍

知道你走過一條死路，我就不會再去走。這在 AI 協作中尤其重要——許多「試了沒有效果」的實驗耗費了數小時甚至數天。

### 2. 陰性結果可能是「條件性陰性」

在某個模型版本／某種 prompt 寫法／某個任務類型下失敗，換個條件可能成功。記錄精確的失敗條件，比記錄成功更具資訊量。

### 3. 誠實建立信任

一個說自己「所有實驗都成功」的人要麼沒做過實驗，要麼在說謊。公開陰性結果展現了你對事實的忠誠度。

### 4. 方法論演進需要失敗資料

如果你的方法論框架只根據成功案例提煉，它會產生系統性偏差。知道什麼**不**work 和知道什麼 work 同等重要。

## 這個登記冊不是

- ❌ 不是學術期刊——不需要完整的論文格式
- ❌ 不是「失敗者俱樂部」——陰性結果是正常的研究產出
- ❌ 不要求統計顯著性——單一案例的誠實報告也歡迎
- ❌ 不限於「重大失敗」——小至「換了個 prompt 反而更差」也可以登記

## 這個登記冊是

- ✅ 一個結構化、可檢索的經驗資料庫
- ✅ 一張「別人踩過的坑」地圖
- ✅ 一項鼓勵誠實的社群實踐

---

## 分類體系

### 按領域（Domain）

| 代碼 | 領域 | 說明 |
|------|------|------|
| prompt-engineering | Prompt 工程 | Prompt 設計、對照實驗、結構最佳化 |
| code-review | 程式碼審查 | 多模型審查、bug 偵測、品質評估 |
| methodology-extraction | 方法論提取 | 從專案中提煉可複用模式 |
| workflow-orchestration | 工作流程編排 | 多 agent 編排、平行／管線策略 |
| document-generation | 文件生成 | MD→DOCX/PDF、多語言翻譯 |
| multi-model-collaboration | 多模型協作 | 模型角色分配、交叉驗證 |
| quantitative-research | 量化研究 | 因子／策略／回測／ML 模型 |
| academic-writing | 學術寫作 | 論文流水線、文獻回顧 |
| tool-building | 工具開發 | CLI 工具、Skill 開發 |
| skill-design | Skill 設計 | Claude Code Skill/Plugin |
| benchmarking | 基準測試 | 模型／工具效能比較 |
| other | 其他 | 不在以上分類 |

### 按陰性結果類型（Category）

| 代碼 | 類型 | 說明 |
|------|------|------|
| null-result | 零結果 | 實驗組和對照組無顯著差異 |
| ceiling-effect | 天花板效應 | 基線已經很好，改進空間為零 |
| worse-than-baseline | 劣於基線 | 新方法比基線還差 |
| failed-to-replicate | 重現失敗 | 無法重現先前有效的發現 |
| methodology-failure | 方法失敗 | 實驗設計／執行本身出了問題 |
| abandoned-dead-end | 死胡同 | 方向本身不可行，放棄 |
| hypothesis-falsified | 假設被證偽 | 明確推翻了原有假設 |
| tool-unfit-for-purpose | 工具不適用 | 所選的工具／模型不適合任務 |
| other | 其他 | 不在以上分類 |

---

## 與學術文獻的關係

2026 年已有幾篇論文為陰性結果的學術價值提供了外部支援：

- **Kohli (2026-05)**：9 個 LLM 評審團的有效獨立票僅約 2 票——增加模型數量可能沒有用，這是一個有量化證據的陰性結果
- **Kuai et al. (2026-04)**：18 個 LLM 存在廣泛的「行為糾纏」——模型並不像你以為的那樣獨立
- **Nájera et al. (2026-05)**：將多模型分歧重新定義為診斷訊號——「模型意見不一致」不是 bug

這些論文本身就是在發表「不符合直覺」的發現。本登記冊希望在更輕量的層面做同樣的事。

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-25*
