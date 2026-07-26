# NRR-2026-009: 框架 v1.3.2 草案被 Codex 駁回（4.3/10）

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-009 |
| **標題** | 框架 v1.3.2 草案被 Codex 駁回（4.3/10）——8 項結構性失敗，含 boost -= (-0.15) 符號錯誤 |
| **領域** | methodology-extraction |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | ai-collaboration-framework |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-06-14 |

---

## 實驗概述

### 原始假設

> 基於 v1.3 框架結構設計的 §3.7 訊號熵檢測器擴充草案，經作者自檢後預期可通過獨立審查（評分 ≥6/10）。

### 方法

基於 v1.3 主檔案結構編寫了 §3.7 擴充草案，引入 signal_entropy、boost 調整、auto-suppress/auto-explore 機制。提交給 Codex CLI（GPT-5.5）進行零涉入獨立審查，覆蓋 8 個檢查維度。

### 預期結果

> 獨立審查評分 ≥6/10，發現為 MODERATE 層級，可經過一輪修訂進入主檔案。

### 實際結果

**Codex 評分 4.3/10，駁回。** 8 項結構性失敗：

1. 版本錯位——草案基於過期 v1.3 結構，主檔案已為 v1.5
2. 自動干預違反核心約束——auto-suppress/auto-explore 違反"只觀測不阻斷"
3. **boost -= (-0.15) 符號錯誤**——負負得正，失敗反而加 0.15 分
4. 假去隱喻化——宣告"已去隱喻"但保留 Gene/Capsule/Event 等 9+ 術語
5. 4,590 證據膨脹——retained analyses 被包裝為"對照試驗"
6. REO schema 無形式化——僅有範例物件
7. A/B 測試設計無法執行——無樣本量/統計方法
8. 數值來源不可驗證——來自混淆程式碼（javascript-obfuscator）

| 指標 | 數值 |
|------|------|
| 效應量 | 評分 4.3/10（REJECTED）；8/8 檢查維度全部失敗 |
| 樣本量 | 1 個草案 × 1 獨立審查者 × 8 檢查維度 |
| 使用的模型 | DeepSeek-V4-Pro, GPT-5.5 |

---

## 解讀與反思

### 為什麼會失敗？

8 項失敗按根因分四類：(a) **流程性**——未同步主檔案版本就動手寫草案；(b) **概念性**——把"檢測"偷換為"自動干預"，違反框架核心約束；(c) **技術性**——符號錯誤（負負得正）；(d) **誠實性**——聲稱去隱喻化但術語殘留、retained analyses 包裝為 RCT、混淆程式碼數值當作可信參數。

### 學到了什麼？

1. **版本錯位是最低階的結構性失敗**——基於過期主檔案結構寫的草案，章節編號全部失效
2. **"只觀測不阻斷"是框架核心約束**——從"檢測"滑向"自動干預"只差一步
3. **boost -= (-0.15) 是符號錯誤的教科書案例**——負負得正，失敗反而加分
4. **來源品質獨立於提取品質**——混淆程式碼中的數值不可獨立審計
5. **聲稱與執行之間的差距**（"已去隱喻" vs 9+術語殘留）是最容易自我欺騙的失敗模式

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | prompts, logs, raw-output |

> 完整審查報告和修正路線圖在 [ai-collaboration-framework/_reviews/](https://github.com/redamancy231-create/ai-collaboration-framework) 和 `_research/drafts/`。

---

## 相關

### 後續是否成功？

修正後 v1.5.1 草案通過 Codex 第二輪審查（7.2/10, PASS WITH MODIFICATIONS）。boost 符號修正、自動干預改為 dry-run only。

### 相關連結

- [AI 協作框架](https://github.com/redamancy231-create/ai-collaboration-framework)
- [v1.3.2 Codex 審查報告（4.3/10）](https://github.com/redamancy231-create/ai-collaboration-framework/blob/main/_reviews/框架v1.3.2_Codex审查报告.md)

### 標籤

`驳回草案`, `Codex审查`, `符号错误`, `版本错位`, `去隐喻化`, `证据膨胀`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
