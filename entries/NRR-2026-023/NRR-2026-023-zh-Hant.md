# NRR-2026-023: C++ vs Rust benchmark 中的四項陰性發現

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-023 |
| **標題** | C++ vs Rust benchmark 中的四項陰性發現：二進位大小超標、預期方向被推翻、亞微秒測量失效、GPU 小批量加速比為負 |
| **領域** | benchmarking |
| **類型** | hypothesis-falsified |
| **提交者** | Acerolaorion |
| **來源專案** | etf-pattern-match-pyo3 |
| **來源作者** | redamancy231-create |
| **分析師** | Acerolaorion |
| **日期** | 2026-07-29 |

---

## 實驗概述

### 原始假設

> 四項凍結預登記預期——(1) Rust 二進位 < C++ ×1.5，(2) DTW/standardize/pattern single 單執行緒效能打平（±10%），(3) 100 次採樣足夠區分 ±10% 效能差異，(4) GPU cupy 加速在任意批量下均有正向收益。

### 方法

按 NRR 門 2 預登記（hash 454873aa）執行 C++ vs Rust benchmark：20 組合成分組 + 5 組邊緣分組，預熱 5 次/計時 100 次，wrapper-internal 層計時，±10% 閾值。GPU 測試使用 RTX 4060 Laptop + cupy 14.1.1，N = 100/500/1000/5000。

### 預期結果

> 二進位 <1.5×，單執行緒效能打平（0.90 ≤ ratio ≤ 1.10），100 次採樣可區分 10% 差異，GPU 全批量加速比 >1.0。

### 實際結果

(1) 二進位 1.94×，不滿足 <1.5×。(2) DTW ratio 0.29–0.39（Rust 快 2.6–3.5 倍），standardize 0.67，pattern single 0.53——全部遠超出 ±10% 打平區間。(3) cosine median=0 ns（100 ns 量化），所有核心指標 CoV >5% 致結論降級為傾向性。(4) N=100 時 GPU 端到端 0.2×，N=500 時 0.7×，拐點 N≈1000。

### 為什麼會失敗？

預登記的方向預測在跨語言 benchmark 中系統性偏樂觀——同演算法不等於同效能。亞微秒測量需要迴圈放大而非獨立採樣。GPU 加速比為負是教科書級事實，但在實際專案中親眼看到 0.2× 仍具有教育意義。

### 學到了什麼？

1. 預登記不是預測——是暴露盲區：4/12 指標預期被推翻
2. 跨語言 benchmark 中同演算法不等同效能：Rust 和 C++ 在 allocator、exception 語義、numpy 橋接上的差異會累積
3. 基準測試方法需要分層：毫秒級（獨立採樣）、微秒級（迴圈放大）、亞微秒級（Criterion 型統計）
4. GPU 加速有明確資料規模下限：N<1000，kernel launch + PCIe 傳輸主導耗時，加速比可能為負
5. 二進位大小的預登記預期必須在了解調優參數的前提下設定——不應在未做 LTO/strip 時假設 Rust ≈ C++ 大小
