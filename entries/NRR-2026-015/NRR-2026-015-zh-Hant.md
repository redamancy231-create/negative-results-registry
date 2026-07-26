# NRR-2026-015: "零殘留"宣告三次被證偽

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-015 |
| **標題** | "零殘留"宣告三次被證偽——同一後端同一 grep pattern 掃 10 次也不會發現新盲區 |
| **領域** | code-review |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | ai-collaboration-framework |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-06-23 |

---

## 實驗概述

### 原始假設

> 發布清理完成後，使用自有 grep pattern 掃描可確認"零殘留"。

### 方法

框架發布準備——三次清理+自檢聲稱零殘留 → 三次 Codex 異後端獨立掃描逐次發現新殘留。

### 預期結果

> 第一次清理+自檢後即可達到零殘留。

### 實際結果

**三次聲稱"零殘留"，三次被證偽（100% 誤報率）：** (1) 絕對路徑/使用者名稱殘留 → (2) 四層路徑變體殘留 → (3) .gitignore 排除檔案殘留。根因：同一大腦同一 grep pattern 掃 10 次 = 同樣的盲區 ×10。

| 指標 | 數值 |
|------|------|
| 效應量 | 3/3 次"零殘留"聲稱被證偽（100% 誤報率） |
| 樣本量 | 3 輪清理+自檢 × 3 輪 Codex 獨立掃描 |
| 使用的模型 | DeepSeek-V4-Pro, GPT-5.5 |

---

## 解讀與反思

清理者自己宣佈"零殘留"是不可靠的——大腦在編輯過程中已建立"已處理"的認知，grep 只是確認這個認知。異後端獨立掃描使用不同搜尋策略，自然會命中操作者盲區。

### 學到了什麼？

1. 同一大腦同一 grep pattern 掃 10 次 = 同樣的盲區 ×10
2. 清理者自己宣佈"零殘留"是不可靠的——認知偏差
3. 異後端獨立掃描的必要性：不同的搜尋策略 = 不同的盲區覆蓋
4. 路徑清理存在四層變體——單一 grep 無法窮盡

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | logs, raw-output |

> 回顧記錄在 [retrospect_2026-06-23.md](https://github.com/redamancy231-create/ai-collaboration-framework/blob/main/_reviews/retrospects/retrospect_2026-06-23.md)。催生了 O7 `no_self_reported_zero_residue` 規則。

---

## 相關

### 後續是否成功？

第四次修復後 Codex 確認零殘留。O7 規則（"禁止自掃自誇零殘留"）源於這次失敗。

### 相關連結

- [回顧記錄 — 2026-06-23](https://github.com/redamancy231-create/ai-collaboration-framework/blob/main/_reviews/retrospects/retrospect_2026-06-23.md)

### 標籤

`零残留`, `清理`, `自扫`, `grep`, `盲区`, `异后端扫描`, `O7`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
