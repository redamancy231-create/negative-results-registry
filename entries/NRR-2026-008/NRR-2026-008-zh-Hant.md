# NRR-2026-008: LLM 程式碼審查系統性漏掉 3 類 bug

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-008 |
| **標題** | LLM 程式碼審查系統性漏掉 3 類 bug——渲染效果、預設路徑、終端機編碼全數躲過審查 |
| **領域** | code-review |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | docx-pipeline |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-07-17 |

---

## 實驗概述

### 原始假設

> 多輪 LLM 程式碼審查（跨 5 種後端 + 多維度審查 prompt）應能檢測到專案中的功能性 bug——預期覆蓋率接近 100%。

### 方法

對 docx-pipeline 專案進行了 5 輪跨模型審查（GPT-5.6-Sol 主審），覆蓋程式碼正確性、設定契約、安全性、檔案完整性等維度。事後透過人工端到端測試（目視驗證 + Windows Git Bash 真實環境執行）獨立檢測實際 bug。

### 預期結果

> LLM 審查應找出全部或幾乎全部功能性 bug；遺漏率預期 <10%。

### 實際結果

**LLM 審查（5 輪）完全漏掉了 3 個實際存在的 bug，遺漏率 100%：**

1. **渲染效果 bug**：Mermaid PNG 在 Word 中 ~4× 拉伸——程式碼審查只看畫素數量，看不到 DPI 元資料缺失
2. **預設路徑 bug**：空白範本預設值 `output/docx` 無副檔名，"init→convert"完整流程中斷——審查者看單點程式碼邏輯正確
3. **終端機編碼 bug**：gh CLI 中文檔名在 Windows Git Bash 下 GBK/UTF-8 轉換失敗——審查者看不到終端機環境

| 指標 | 數值 |
|------|------|
| 效應量 | 3/3 類 bug 全數躲過 LLM 審查（遺漏率 100%） |
| 樣本量 | 5 輪審查 × 1 個專案 × 3 類實測 bug |
| 使用的模型 | GPT-5.6-Sol, GPT-5.5, Kimi-K2.7, Claude Opus 4.8 |

---

## 解讀與反思

### 為什麼會失敗？

**LLM 審查存在三類系統性盲區，共享一個特徵：bug 不出現在原始碼的邏輯層面，而出現在相鄰工具鏈的互動契約中。** 渲染效果 bug 需要目視確認最終輸出、預設路徑 bug 需要端到端走完整流程、終端機編碼 bug 需要在真實作業系統環境中才能暴露。程式碼審查——無論多輪多模型——只能回答"程式碼說了什麼"，不能回答"程式碼在真實環境中做了什麼"。

### 學到了什麼？

1. **LLM 審查無法替代端到端目視驗證**——渲染效果、預設路徑、終端機編碼三類 bug 全部逃脫了 5 輪跨模型審查
2. **三類盲區的共性**：bug 不在原始碼邏輯層面，而在相鄰工具鏈的隱性互動契約中
3. **純程式碼審查覆蓋率 ≠ 真實 bug 檢測率**——審查者看到"程式碼說了什麼"，看不到"程式碼在真實環境中做了什麼"
4. **發現成本遠高於修復成本**——三個 bug 的修復總計不到 20 行程式碼，但診斷靠人工端到端測試而非 LLM 審查

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | logs, raw-output |

> 回顧分析記錄在 [docx-pipeline/_reviews/retrospect_2026-07-17.md](https://github.com/redamancy231-create/docx-pipeline/blob/main/_reviews/retrospect_2026-07-17.md)。重現需要相同工具鏈版本（mmdc, python-docx v1.2.0, Windows Git Bash）。

---

## 相關

### 後續是否成功？

三個 bug 事後全部修復。但核心啟示不變：AI 輔助開發的測試策略需要補充"執行環境端到端測試"，不能僅依靠 LLM 程式碼審查。

### 相關連結

- [DOCX Pipeline 倉庫](https://github.com/redamancy231-create/docx-pipeline)
- [回顧報告（含三類盲區詳細分析）](https://github.com/redamancy231-create/docx-pipeline/blob/main/_reviews/retrospect_2026-07-17.md)
- [LLM 審查三類盲區（methodology-handbook）](https://github.com/redamancy231-create/methodology-handbook)

### 標籤

`LLM审查盲区`, `代码审查`, `渲染bug`, `默认路径`, `终端编码`, `端到端验证`, `目视确认`, `审查覆盖率`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
