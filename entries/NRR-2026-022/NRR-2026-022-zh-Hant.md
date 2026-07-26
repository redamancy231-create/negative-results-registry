# NRR-2026-022: 提取者汙染製造虛假方法論訊號

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-022 |
| **標題** | "提取者汙染"——fork 作者附加的方法論檔案被誤歸因到來源專案，製造虛假方法論訊號 |
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

> 在對 fork 的來源專案進行方法論提取時，fork 倉庫中所有檔案應反映來源專案的方法論特徵。預期附加檔案能補充來源專案的方法論資訊。

### 方法

對 NPGS（baopinshui/NPGS）進行完整方法論提取。該倉庫被 fork 後，提取者新增了 CLAUDE.md、GitNexus 索引和分析報告，然後從 fork 倉庫執行提取。事後追溯哪些檔案來自來源作者、哪些來自提取者。

### 預期結果

> 至少部分附加檔案應反映或補充來源專案的方法論特徵。

### 實際結果

**CLAUDE.md、GitNexus 索引、分析報告 100% 來自 fork 提取者。** 來源專案方法論檔案=0。如果不區分兩者，提取者會把"自己編寫的唯一方法論檔案"誤歸因為"來源專案有方法論自覺"。

| 指標 | 數值 |
|------|------|
| 效應量 | 來源專案方法論檔案=0；fork 附加檔案 100% 來自提取者 |
| 樣本量 | 1 個專案 × 提取者 vs 來源作者檔案比對 |
| 使用的模型 | DeepSeek-V4-Pro, GPT-5.6-Sol, GitNexus |

---

## 解讀與反思

### 為什麼會失敗？

提取框架的 Phase 0 設計缺陷。當提取者也是倉庫中唯一方法論檔案的作者時，預設假設"倉庫檔案反映來源專案"會系統性高估來源專案的方法論自覺。

### 學到了什麼？

1. 提取者的檔案≠來源專案的方法論——製造虛假訊號
2. Phase 0 需要"提取者汙染"判別——檢查檔案作者 ≠ 來源專案作者時降低權重
3. fork 後新增的分析產物不應被當作來源專案方法論——觀察者效應
4. 來源專案檔案=0 是誠實訊號，不是提取失敗

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | logs, analysis-script |

> **第三方分析條目。** NPGS 來源倉庫和 fork 倉庫的差異可獨立核查。

---

## 相關

### 後續是否成功？

可修復的設計缺陷——Phase 0 新增提取者汙染判別即可過濾。不是框架結構性失敗。

### 相關連結

- [NPGS 來源倉庫 (baopinshui/NPGS)](https://github.com/baopinshui/NPGS)
- [NPGS 證據卡](https://github.com/redamancy231-create/methodology-extraction-methodology/blob/main/explorations/evidence_card_npgs_external.md)

### 標籤

`提取者污染`, `fork`, `NPGS`, `方法论归因`, `Phase0缺陷`, `虚假信号`, `第三方分析`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
