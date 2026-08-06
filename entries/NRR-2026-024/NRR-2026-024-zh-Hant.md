# NRR-2026-024: CUDA 因子截面加速端到端約 3.0×，未達預註冊 ≥5× 目標

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-024 |
| **標題** | CUDA 因子截面加速端到端約 3.0×，未達預註冊 ≥5× 目標（FP64 硬體天花板 + 傳輸開銷主導；≥2× 最低可接受已達成） |
| **領域** | benchmarking |
| **類型** | ceiling-effect |
| **提交者** | redamancy231-create |
| **來源專案** | factor-cuda |
| **來源作者** | redamancy231-create |
| **分析師** | redamancy231-create |
| **日期** | 2026-08-06 |

---

## 實驗概述

### 原始假設

預註冊（CLAUDE.md「PoC 決策表」：NRR 門檻 ≥5×、最低可接受 ≥2×；PLAN.md §9）：在 RTX 4060 Laptop GPU（sm_89）上，fc 介接層（pybind11 + CUDA）於固定 corpus_synth_v1（T=1218×N=5000×F=12）最小參數掃描流水（parameter_scan → 逐因子 rolling_ic → factor_corr + IC 合併，verdict_scope 排除 stock_corr）相對最佳免費替代（qgplearn 未安裝 → min(numpy,cupy)，同資料同 mask 同語意，含 H2D 傳輸與合併）端到端加速比 ≥5×。

### 方法

預註冊錨點：CLAUDE.md PoC 決策表（≥5× NRR 門檻 / ≥2× 最低）與 PLAN.md §9。端到端：benchmarks/poc4_e2e_v1.py（F∈{4,8,12} 最小參數掃描流水，GPU 臂用 pybind11 綁定，numpy/cupy 臂用 benchmarks/backends.py，對稱 reps，verdict_scope 明確排除 stock_corr，best_free=min(numpy,cupy) 執行時記錄）；Phase 4 新增 fresh 輪 + 跨 run 穩定性門。單算子（產品層）：benchmarks/phase4_bench_v1.py——binding 級（含 H2D 傳輸 + D2H，與 e2e 同層）vs numpy/cupy 最佳免費替代，median + bootstrap 95% CI(1000, seed=0) + CV，warm 3+20 採樣，逐塊 nvidia-smi 熱採樣，corpus_synth_v1 全量。可複現性：雙 corpus（synth+real）經 corpus_loader_v1 驗證 data_sha256（fail-closed）；流水兩 run 輸出雜湊逐位相等；git HEAD 釘紮 + 證據 self-hash；corpus_real_v1（N=93）僅正確性/確定性錨點，不產 perf 數字。證據：benchmarks/results/phase4_bench_v1.{json,md} + poc4_e2e_v1.json + acceptance_v1.json。

### 預期結果

假設成立：F=12 端到端加速比 ≥5×（相對 best-free，含傳輸與合併）；單算子 ≥2×；float64 聚合類（rolling_ic/factor_corr）預期貢獻主要加速。預註冊失敗判據：<2× → STOP；≥2× 且 <5× → 記負結果 NRR-2026-024。

### 實際結果

E2E F=12 端到端加速比約 3.03–3.20×（committed poc4_e2e_v1.json 記錄 3.0353×；Phase 4 fresh 輪 3.198× / 3.141×，跨 run |Δmedian| ≈ 2–5% 穩定）。≥2× 最低可接受達成（PASS），≥5× 預註冊目標未達成。單算子（binding 級含傳輸，corpus_synth_v1 全量，vs best-free=min(numpy,cupy)）：cs_rank 約 1.6×（低於產品層 2× 下限）、parameter_scan(G=4) 約 2.2×、rolling_ic 約 2.1×、factor_corr 約 15×（≥5× PASS）、stock_corr general N=500 約 2.1× / N=2000 約 2.6×。元件級負結果：e2e 分操作 ic_stack（IC 合併）約 0.72× 劣於基線，顯式暴露不埋入聚合 PASS。關鍵層差異：早期驗收 below_5x（cs_rank 3.01×/parameter_scan 3.02×/rolling_ic 3.14×）為 kernel-resident（GPU 純計算無傳輸）口徑，產品實際支付（binding 含傳輸）更低，cs_rank 甚至 <2×。corpus_real_v1（N=93）僅正確性+確定性錨點（流水兩 run 輸出雜湊逐位相等），不產 perf。

### 為什麼失敗

預註冊 ≥5× 端到端目標未達成（約 3.0×），≥2× 最低可接受達成。歸因分機制不作單一概括：①FP64 硬體天花板（主因，僅解釋 float64 聚合操作）——RTX 4060 Laptop FP64≈FP32/64（官方架構特性物理上限），rolling_ic 約 2.1×、stock_corr general 約 2.1–2.6× 與 factor_corr 一般歸約受限；②launch/傳輸/佔用開銷（解釋 float32 操作 + 產品層缺口）——cs_rank 約 1.6×、parameter_scan 約 2.2× 的缺口機制為 per-call H2D/D2H 傳輸 + kernel launch + 小面板佔用，不可歸因 FP64；③陽性對照證明非普遍低效——同證據集、同 corpus_synth_v1 非退化面板上 factor_corr 約 13–15×（≥5× PASS），同一批內核可達 ≥5×，below_5x 是負載相關而非普遍內核低效；④kernel-resident 口徑高估使用者側——早期驗收 below_5x 為 GPU 純計算口徑，產品實際支付（binding 含傳輸）更低，效能聲明必須標註傳輸口徑；⑤介接層 Python 開銷——fc 介接層對 factor_corr 的契約強制 f32→f64 Python upcast（約 1 秒/呼叫，相對綁定內部 forcecast upcast 慢約 178%），產品 Python 層有可最佳化空間，非綁定缺陷。未驗證的替代解釋（更高 FP64 吞吐 GPU、FP32 聚合路徑、kernel 調優）標為未驗證假設而非可行性聲明。結論限定於 RTX 4060 Laptop + 固定 corpus（synth_v1 規模；real_v1 僅正確性）+ 排除 stock_corr 的 E2E 口徑，不推廣至其他 GPU 或 FP64 不佔主導的工作負載。

### 我們學到了什麼

- 預註冊雙門檻（≥2× 最低 / ≥5× 目標）使約 3.0× 成為無歧義裁決：下限達成、目標未達 → 如實記負，不得把已記錄缺口包裝為成功。
- 消費級 GPU（RTX 40 系）FP64≈FP32/64 是 float64 聚合工作負載的硬天花板——設 ≥5× 目標前先查設備 FP64 規格，或為聚合內核設計 FP32 路徑。
- 效能聲明必須標註傳輸口徑：kernel-resident（GPU 純計算）與 binding-含傳輸（使用者實際支付）可差 2–3×（cs_rank 3.01× vs 1.6×）——未標註口徑即誤導。
- 硬體天花板歸因須分機制 + 同證據集陽性對照錨定：FP64 天花板只解釋 float64 操作；float32 的 <2× 歸因 launch/傳輸/佔用；factor_corr 約 13–15× 證明內核可超 5×。
- 執行前聲明並沿用 E2E 判定口徑（verdict_scope 排除 stock_corr）；元件級負結果（ic_stack 0.72×）顯式暴露，不埋入聚合 PASS。

## 關鍵教訓

1. **預註冊雙門檻使約 3.0× 成為無歧義裁決**——下限達成、目標未達 → 如實記負，不得成功化包裝。
2. **消費級 RTX 40 系 FP64≈FP32/64 是 float64 聚合的硬天花板**——設 ≥5× 前先查設備 FP64 規格，或設計 FP32 路徑。
3. **效能聲明必須標註傳輸口徑**——kernel-resident 與 binding-含傳輸差 2–3×（cs_rank 3.01× vs 1.6×）。
4. **硬體歸因分機制 + 同證據陽性對照**——FP64 天花板只解釋 float64 操作；factor_corr 約 13–15× 證明內核可超 5×。
5. **執行前聲明 E2E 口徑；顯式暴露元件負結果**（ic_stack 0.72×），不埋沒。

## 可複現性

- **Level**: partially-reproducible（同機同 commit 同 corpus → 輸出位級確定性 + 計時 CI-overlap；異機計時不可搬移）
- **Artifacts available**: code, data, logs, analysis-script, raw-output
- **Notes**: corpus manifest 已提交（real data_sha256=FB23D9E1CC81401EBB7C439BFDB514F5FC9A0C2C57BA1AA363852B398388504F；synth 由 loader 執行時確認）；流水輸出兩 run 雜湊逐位相等；證據 self-hash + git HEAD 釘紮。qgplearn 基線臂未安裝，best-free=min(numpy,cupy) 為替代，故 level 為 partially-reproducible（非 fully）。作用域：同機輸出位級 + 計時 CI-overlap；異機計時不可搬移。環境 Python 3.12.7 / numpy 2.4.4 / cupy 14.1.1 / CUDA 13.3 / RTX 4060 Laptop。

## 相關陽性結果

同證據集陽性對照（不掩蓋缺口）：corpus_synth_v1 全量（非退化面板、同 corpus）上 factor_corr 約 13–15×（≥5× PASS）證明同一批內核可達 ≥5×，把 below_5x 隔離為負載/硬體相關而非普遍低效。stock_corr fast 路徑（全有效退化-mask 合成面板特例）5–12× 須與 general 約 2.1–2.6× 並排引用，不單獨用作內核能力證據。

## 標籤

factor-cuda, CUDA, GPU, benchmark, preregistered, FP64-ceiling, RTX-4060, speedup, negative-result, ceiling-effect, product-layer-overhead

## 連結

- [factor-cuda 儲存庫](https://github.com/redamancy231-create/factor-cuda)（發布時驗證 URL 可解析）
- [Phase 4 benchmark 證據 phase4_bench_v1.json](https://github.com/redamancy231-create/factor-cuda/blob/main/benchmarks/results/phase4_bench_v1.json)（發布時驗證 blob URL）
- [端到端證據 poc4_e2e_v1.json](https://github.com/redamancy231-create/factor-cuda/blob/main/benchmarks/results/poc4_e2e_v1.json)（發布時驗證 blob URL）
- [negative-results-registry 儲存庫](https://github.com/redamancy231-create/negative-results-registry)
