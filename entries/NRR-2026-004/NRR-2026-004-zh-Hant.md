# NRR-2026-004: mmdc 渲染 PNG 無 DPI 元資料 → python-docx 預設 72 DPI 致圖片 ~4 倍拉伸

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-004 |
| **標題** | mermaid-cli 渲染 PNG 不含 DPI 元資料，python-docx 預設 72 DPI 致圖片 ~4 倍拉伸截斷 |
| **領域** | document-generation |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | docx-pipeline |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-06-23 |

---

## 實驗概述

### 原始假設

> mermaid-cli（mmdc）是 Mermaid 圖表渲染的事實標準工具——預期其 PNG 輸出在 python-docx → DOCX 管線中可直接嵌入使用，無需額外 DPI 後處理。

### 方法

DOCX Pipeline 專案的 Mermaid → DOCX 管線（AI 輔助開發環境下發現的問題）：
1. 在 Markdown 中檢測 ` ```mermaid ` 程式碼區塊
2. 按設定的 DPI（預設 300）計算畫素寬度 → 呼叫 `mmdc --width <px>` 渲染為 PNG
3. 透過 python-docx（v1.2.0）的 `add_picture()` 將 PNG 嵌入 DOCX
4. 在 Word 中開啟驗證視覺效果

### 預期結果

> PNG 以預期尺寸（約頁面寬度 80-100%）嵌入 DOCX，Word 中正常顯示。

### 實際結果

PNG 在 DOCX 中顯示為 **~4 倍拉伸**——圖片超出頁面邊界，被截斷。根因鏈：

1. **mmdc 渲染的 PNG 不含 DPI 元資料**（mmdc 沒有 `--dpi` 參數，`--width` 只控制渲染寬度，不寫入 PNG 的 pHYs chunk）
2. **python-docx 對無 DPI 元資料的圖片預設按 72 DPI 計算嵌入尺寸**（不是 Word 的 96 DPI 螢幕密度——python-docx 寫入顯式 EMU 尺寸，Word 直接使用）
3. 300 DPI 的點陣圖 ÷ 72 DPI 尺寸計算 → 物理尺寸膨脹 ~4.17 倍（300/72）

| 指標 | 數值 |
|------|------|
| 效應量 | 物理尺寸膨脹 ~4.17×（300 DPI 畫素 ÷ 72 DPI python-docx 預設值） |
| 樣本量 | 所有含 Mermaid 圖表的 DOCX 檔案（專案初期 100% 重現） |
| 使用的工具 | mermaid-cli (mmdc), python-docx v1.2.0, Microsoft Word |

---

## 解讀與反思

### 為什麼會失敗？

**工具鏈多層互操作契約中相鄰環節的隱性假設不相容。** 不是任何一個工具的單點 bug——mmdc 正確地渲染了指定寬度的畫素（`--width` 控制渲染寬度），python-docx 正確地按 72 DPI 預設值計算了無元資料圖片的嵌入尺寸。問題出在兩個工具的契約之間缺少一個 DPI 注入步驟——而管線設計者預設了"mmdc PNG 輸出 = python-docx 可直接嵌入"。這是管線設計的方法論問題，不是單個工具的適用性問題。

### 學到了什麼？

1. **工具鏈的每個環節須做端到端互操作假設驗證**——"A 的輸出 = B 的輸入"這個預設假設在每個新工具組合中都必須驗證
2. **視覺驗證不可跳過**——純程式碼審查檢測不到 DPI 元資料缺失；必須開啟 Word 目視確認最終渲染效果
3. **隱性預設值是整合 bug 溫床**——mmdc 不寫 pHYs chunk 和 python-docx 預設 72 DPI 各自單獨合理，組合即成 bug
4. **修復只需一行 Pillow 程式碼**——`image.save(path, dpi=(300,300))`；但診斷靠目視發現而非程式碼審查，發現成本遠高於修復成本

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | code |

> **可重現條件**：需要 mmdc + python-docx v1.2.0 + Pillow 環境。python-docx 的預設 DPI 行為（72）在不同版本間一致，但不同版本的 `add_picture()` 對 DPI 缺失圖片的處理可能不同。修復程式碼在 [docx-pipeline](https://github.com/redamancy231-create/docx-pipeline) 的 `docx_pipeline/renderers/mermaid_renderer.py` 中（`_inject_dpi()` 方法）。

---

## 相關

### 後續是否成功？

✅ 修復成功。渲染後用 Pillow 讀取 PNG → `image.save(path, "PNG", dpi=(300, 300))` 寫入 pHYs chunk → python-docx 按 300 DPI 計算嵌入尺寸 → 圖片在 Word 中以正確尺寸顯示。

### 相關連結

- [DOCX Pipeline 倉庫](https://github.com/redamancy231-create/docx-pipeline)
- [LLM 審查三類盲區（含渲染效果盲區）](https://github.com/redamancy231-create/methodology-handbook) — 對應記憶 `methodology_llm_review_blind_spots_rendering_paths`

### 標籤

`docx-pipeline`, `mermaid-cli`, `mmdc`, `DPI`, `PNG`, `Word`, `工具链`, `元数据`, `端到端验证`, `视觉bug`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
