# NRR-2026-010: 三件組同步不對稱漂移

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-010 |
| **標題** | 三件組同步不對稱漂移——.md→.json 定點修補 vs .md→.docx 完整重新生成，跨會話接力時 .json 系統性漏掉 prose 訂正 |
| **領域** | document-generation |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | ai-collaboration-framework |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-06-24 |

---

## 實驗概述

### 原始假設

> .md（權威源）→ .json + .docx 的三件組同步協議應保證三種格式的內容一致性。版本門（O6）PASS 即表示三件組一致。

### 方法

AI 協作框架 v1.6.4 發布前執行了 O6 版本門（`verify_version_consistency.py`），然後由 Codex（GPT-5.5）執行異後端三件組交叉審查——逐章節比對內容一致性。

### 預期結果

> 三件組內容完全一致，版本門 PASS。

### 實際結果

版本門 PASS（版本號"1.6.4"三個檔案一致）。但 Codex 內容級審查發現：**.json 遺漏了 .md 的 prose 修訂**（措辭修正、解釋性段落等），而 .docx 透過完整重新生成自動包含了這些修訂。根因：.json 走定點修補（手工在舊版 JSON 上打補丁），.docx 走完整重新生成（pandoc 從最新 .md 生成）。跨會話接力時，定點修補的維護者不知道 .md 中的 prose 變更。

| 指標 | 數值 |
|------|------|
| 效應量 | .json 與 .md 存在內容級不一致（版本門 O6 無法檢測） |
| 樣本量 | v1.6.4 發布前的一次三件組交叉審查 |
| 使用的模型 | DeepSeek-V4-Pro, GPT-5.5, Kimi-K2.7, Qwen3.7-Max |

---

## 解讀與反思

### 為什麼會失敗？

**同步協議的設計缺陷。** O6 版本門只驗證版本號一致性，無法檢測內容級漂移。兩種派生格式採用不對稱同步策略——.docx 完整重新生成（自然能防止漂移）、.json 定點修補（依賴操作者知道全部變更）。跨會話接力時，後者必然滯後。

### 學到了什麼？

1. **版本號一致性 ≠ 內容一致性**——O6 版本門 PASS 但 .json 與 .md 存在 prose 級漂移
2. **不對稱同步策略是設計缺陷**——定點修補 vs 完整重新生成在跨會話接力中必然暴露
3. **定點修補的前提是操作者知道 .md 中所有變更**——這在多會話接力場景中不成立
4. **根治方案：全部從 .md 完整重新生成**——消除所有手動同步路徑

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | logs, raw-output |

> 三件組交叉審查報告在 [ai-collaboration-framework/_reviews/](https://github.com/redamancy231-create/ai-collaboration-framework)。

---

## 相關

### 後續是否成功？

短期修復：發布前增加 Codex 異後端三件組交叉審查。長期方案（待實作）：將 .json 同步改為完整重新生成。

### 相關連結

- [AI 協作框架](https://github.com/redamancy231-create/ai-collaboration-framework)
- [三件組同步審查報告](https://github.com/redamancy231-create/ai-collaboration-framework/blob/main/_reviews/codex_review_v1.5.1_三件套同步审查.md)

### 標籤

`三件套同步`, `版本门`, `不对称漂移`, `定点补丁`, `全量重生成`, `内容一致性`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
