# NRR-2026-005: Amdahl's Law — C++ 53× 加速塌縮至批次 2.2×

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-005 |
| **標題** | C++ 加速 53× 塌縮至批次 2.2×——Amdahl's Law 將端到端加速釘死在 ~2.25× 理論上限 |
| **領域** | tool-building |
| **分類** | ceiling-effect |
| **提交者** | Acerolaorion |
| **來源專案** | etf-pattern-match-pybind11 |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-07-12 |

---

## 實驗概述

### 原始假設

> 用 pybind11 + C++20 加速形態匹配 ETF 策略的純計算核心後，批次工作負載應獲得接近單次呼叫層級的端到端加速（預期 10-30×）。

### 方法

將 Python 純計算核心（DTW、形態匹配、技術指標）遷移至 C++，透過 pybind11 暴露。分別測量 (a) 單次呼叫 Python vs C++、(b) 100 時間點批次 Python vs C++ batch、(c) 100 次 C++ 單次 vs 1 次 C++ 批次。從 V3.3.py（3836 行）提取純計算模組，排除相依於 sklearn/scipy/pandas 的函式。

### 預期結果

> DTW 單次 ≥10×、形態匹配單次 ≥30×、批次端到端 ≥10×。

### 實際結果

DTW 單次 34×、形態匹配單次 53× 均超過預期。但 **批次端到端僅 2.2×**——遠低於單次加速比。根因：批次工作量僅 **~56% 可加速**（p≈0.556），44% 為序列額外負擔。理論加速上限 1/(1-p)≈2.25×，實測 2.2× 已逼近天花板。

| 指標 | 數值 |
|------|------|
| 效應量 | 單次 53× → 批次 2.2×（衰減 24×）；理論上限 ≈2.25× |
| 樣本量 | 100 次 warm-up + 100 次計時中位數 × 6 函式 |
| 序列比例 | 44%（Python 迴圈 15% + 資料轉換 15% + pybind11 呼叫 8% + 特徵計算 6%） |
| 使用的模型 | DeepSeek-V4-Pro, Kimi-K2.7-Code |

---

## 解讀與反思

### 為什麼會失敗？

**這是 Amdahl's Law 的教科書級範例。** 單次加速 53× 並非"錯誤"——53× 和 2.2× 都是準確測量，只是測量對象不同。53× 測的是純計算熱路徑（14.0ms→0.26ms），2.2× 測的是端到端批次吞吐（50ms→23ms，其中包含不可加速的編排、資料搬運、Python/C++ 邊界額外負擔）。這不是 bug——是架構天花板。

### 學到了什麼？

1. **Amdahl's Law 不是理論抽象**——實測 2.2× vs 上限 2.25× 證明在量化計算場景中數學建模與實際測量高度吻合
2. **"單次加速比"和"端到端加速比"是完全不同的指標**——前者表徵計算效率，後者表徵使用者可感知的吞吐提升
3. **44% 序列額外負擔精確分解為 4 類**（迴圈/轉換/呼叫/特徵），每類對應不同的最佳化策略
4. **達到 10× 端到端需 92% 可加速**——比 C++ 遷移更根本的可能是架構重構

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | fully-reproducible |
| **可用產物** | code, data, analysis-script, raw-output |

> 完整基準測試程式碼、Amdahl 數學推導和效能分析在 [etf-pattern-match-pybind11](https://github.com/redamancy231-create/etf-pattern-match-pybind11) 倉庫的 `docs/performance-analysis.md` 和 `benchmarks/` 中。

---

## 相關

### 後續是否成功？

單次呼叫加速 34-53× 是成功的——批次塌縮不否定單次加速的工程價值。可能的改進方向：將 Python for 迴圈和 NumPy 轉換移入 C++。

### 相關連結

- [ETF Pattern Match — pybind11 倉庫](https://github.com/redamancy231-create/etf-pattern-match-pybind11)
- [效能分析短文（含完整 Amdahl 數學推導）](https://github.com/redamancy231-create/etf-pattern-match-pybind11/blob/master/docs/performance-analysis.md)

### 標籤

`Amdahl`, `pybind11`, `C++`, `性能`, `加速塌缩`, `批量`, `理论上限`, `架构天花板`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
