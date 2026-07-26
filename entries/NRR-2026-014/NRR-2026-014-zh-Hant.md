# NRR-2026-014: Spec Coding 被違反 — 翻譯管線全面偏離計劃

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-014 |
| **標題** | 框架自身主張 Spec Coding 但在翻譯管線中被全面違反——模型分工、檔案範圍、流程步驟全部偏離 |
| **領域** | workflow-orchestration |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | ai-collaboration-framework |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-06-23 |

---

## 實驗概述

### 原始假設

> 框架 §4 主張"有明確計劃時必須嚴格按計劃執行"。當翻譯管線有明確 Spec 時，預期執行嚴格遵守。

### 方法

三語言翻譯管線 Spec 明確規定了模型分工（OpenCC + Qwen 通讀 + Codex 校譯）、檔案範圍（2 份）、三階段流程。事後回顧將實際執行與 Spec 逐項對比。

### 預期結果

> 執行過程嚴格符合 Spec。

### 實際結果

**3/3 計劃承諾全部被違反：** 模型分工從"多模型+校譯"簡化為"單模型+自檢"、檔案範圍從 2 份擴大到 4 份且未經確認、三階段流程被壓縮為單階段。框架自身主張 Spec > Vibe，但操作者（同時是 Human Gate）在"效率優先"下跳過了 Gate。

| 指標 | 數值 |
|------|------|
| 效應量 | 3/3 計劃承諾被違反 |
| 樣本量 | 1 次翻譯執行 × 3 維度對比 |
| 使用的模型 | DeepSeek-V4-Pro, OpenCC, Qwen3.7-Max |

---

## 解讀與反思

Spec Coding 的最大敵人不是外部干擾——是操作者自己"走捷徑"的執行慣性。Human Gate 在操作者=Human Gate 的情境下形同虛設。

### 學到了什麼？

1. Spec Coding 的最大敵人是操作者自身的執行慣性
2. Human Gate 在操作者=Human Gate 的情境下形同虛設——需要外部強制力
3. 計劃中的模型分工是最容易被簡化的——"多模型+校譯"→"單模型+自檢"只需一個"這樣更快"的心理藉口
4. 事後誠實記錄違反 ≠ 事前防止違反

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | prompts, logs, raw-output |

> 回顧記錄在 [retrospect_2026-06-23.md](https://github.com/redamancy231-create/ai-collaboration-framework/blob/main/_reviews/retrospects/retrospect_2026-06-23.md)。

---

## 相關

### 後續是否成功？

這次失敗催生了專案啟動檢查清單的 §6 `spec_over_vibe` 強制檢查項。

### 相關連結

- [回顧記錄 — 2026-06-23](https://github.com/redamancy231-create/ai-collaboration-framework/blob/main/_reviews/retrospects/retrospect_2026-06-23.md)

### 標籤

`Spec Coding`, `翻译管道`, `计划违反`, `执行惯性`, `走捷径`, `Human Gate`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
