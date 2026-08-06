# NRR-2026-024: CUDA 因子截面加速端到端 3.04×，未達預註冊 ≥5× 目標

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-024 |
| **標題** | CUDA 因子截面加速端到端 3.04×，未達預註冊 ≥5× 目標（≥2× 最低可接受已達成） |
| **領域** | benchmarking |
| **類型** | hypothesis-falsified |
| **提交者** | redamancy231-create |
| **來源專案** | factor-cuda |
| **來源作者** | redamancy231-create |
| **分析師** | redamancy231-create |
| **日期** | 2026-08-06 |

---

## 實驗概述

### 原始假設

預註冊（CLAUDE.md「PoC 決策表」：NRR 門檻 ≥5×、最低可接受 ≥2×；PLAN.md §9）：在 RTX 4060 Laptop GPU（sm_89）上，fc 加速器（pybind11 + CUDA 綁定，binding 級含傳輸）於固定 corpus_synth_v1（T=1218×N=5000×F=12）最小參數掃描流水（parameter_scan → 逐因子 rolling_ic → factor_corr + IC 合併，verdict_scope 排除 stock_corr）相對最佳免費替代（qgplearn 未安裝 → min(numpy,cupy)，同資料同 mask 同語意，含 H2D 傳輸與合併）端到端加速比 ≥5×。

### 方法

預註冊錨點：CLAUDE.md PoC 決策表（≥5× NRR 門檻 / ≥2× 最低）與 PLAN.md §9。端到端（主判據）：benchmarks/poc4_e2e_v1.py + benchmarks/phase4_bench_v1.py——最小參數掃描流水，GPU 臂 pybind11 綁定（factor_cuda_pybind/factor_corr_pybind），numpy/cupy 臂 benchmarks/backends.py，對稱 reps + Phase 4 fresh 輪（**臂序輪轉 + 熱採樣 + bootstrap CI**），best_free=min(numpy,cupy) 執行時記錄，verdict_scope 排除 stock_corr；**判據統計量=min-of-run-medians（最壞情況，跨 fresh 輪）**。單算子（產品層補充）：phase4_bench_v1.py binding 級（含 H2D/D2H）vs numpy/cupy，median + bootstrap 95% CI + CV，warm 3 + 20 採樣（原樣持久化）；介接層開銷單獨測量（fc 介接層 vs 裸綁定）。可複現性：雙 corpus 經 corpus_loader_v1 驗證 data_sha256（fail-closed）；流水兩 run 輸出雜湊逐位相等；G6 證據 self-hash 實門（源檔缺失/髒即 FAIL）；git HEAD 釘紮；corpus_real_v1（N=93）僅正確性/確定性錨點。證據：benchmarks/results/phase4_bench_v1.{json,md} + poc4_e2e_v1.json + acceptance_v1.json。

### 預期結果

假設成立：F=12 端到端加速比 ≥5×（相對 best-free，含傳輸與合併）；單算子 ≥2×。預註冊失敗判據：<2× → STOP；≥2× 且 <5× → 記負結果 NRR-2026-024。

### 實際結果

E2E F=12 端到端加速比 3.035–3.046×（committed poc4_e2e_v1.json 3.0353×；Phase 4 fresh 輪 3.046×，臂序輪轉後消除固定臂序熱偏置；跨 run delta 0.34% 穩定）。≥2× 最低可接受達成（PASS-partial），≥5× 預註冊目標未達成（假設被證偽）。單算子（binding 級含傳輸，corpus_synth_v1 全量，vs best-free）：除 factor_corr 外全部 <5×；factor_corr 約 12–15×（≥5×，binding 級）；cs_rank/parameter_scan/rolling_ic/stock_corr general 觀察區間 1.6–3.8×。⚠️ 跨會話變異披露：本機（RTX 4060 Laptop）單算子中位數跨會話波動可達 ~2×（如 cs_rank 1.6×→3.1×、cupy 基線 69ms→218ms），單算子邊界斷言（如 cs_rank <2×）不跨會話穩定、僅作指示性；E2E 判據（預註冊決策）穩定。元件級負結果：e2e 分操作 ic_stack（IC 合併）約 0.72× 劣於基線，顯式暴露不埋入聚合 PASS。關鍵層差異：早期驗收 below_5x（cs_rank 3.01×/parameter_scan 3.02×/rolling_ic 3.14×）為 kernel-resident（GPU 純計算無傳輸）口徑，產品實際支付（binding 含傳輸）更低；介接層 factor_corr f32→f64 Python upcast 額外開銷 +178%~+266%（**產品層 factor_corr 約 3.98× <5×，binding 級 12–15×**）。corpus_real_v1（N=93）僅正確性+確定性錨點。

### 為什麼失敗

預註冊 ≥5× 端到端目標未達成（3.04×），≥2× 最低可接受達成。歸因分機制、均標為候選而非已證實：①FP64 硬體天花板（候選機制，未做 FP32 聚合路徑確認實驗）——RTX 4060 Laptop FP64≈FP32/64 可能限制 float64 聚合操作（rolling_ic/factor_corr 一般歸約/stock_corr general）的加速上限，但同證據集 factor_corr（float64）達 12–15×，削弱天花板為主因的強度；②launch/傳輸/佔用開銷（候選機制）——解釋 float32 操作（cs_rank/parameter_scan）與產品層傳輸成本；③陽性對照（binding 級）證明內核可達 ≥5×——factor_corr 12–15×（同 corpus_synth_v1 非退化面板），below_5x 是負載/層相關而非普遍內核低效；④kernel-resident 口徑高估使用者側——早期驗收為 GPU 純計算口徑，產品實際支付（含傳輸）更低；⑤介接層 Python 開銷——fc 介接層契約強制 f32→f64 Python upcast（factor_corr +178%~+266%），產品層 factor_corr 約 3.98× <5×，為產品最佳化機會非綁定缺陷。跨會話變異：單算子中位數本機跨會話波動 ~2×，單算子邊界斷言不作決策依據，決策僅依 E2E（穩定）。未驗證的替代解釋（更高 FP64 吞吐 GPU、FP32 聚合路徑、kernel 調優）標為未驗證假設。結論限定於 RTX 4060 Laptop + 固定 corpus + 排除 stock_corr 的 E2E 口徑。

### 我們學到了什麼

- 預註冊雙門檻（≥2× 最低 / ≥5× 目標）使 3.04× 成為無歧義裁決：下限達成、目標未達 → 如實記負，不得把已記錄缺口包裝為成功。
- 消費級 GPU（RTX 40 系）效能變異大——單算子加速比跨會話可波動 ~2×（cs_rank 1.6×→3.1×），預註冊決策須基於穩健的端到端判據而非波動大的單算子邊界。
- 效能聲明必須標註層與傳輸口徑：kernel-resident（GPU 純計算）、binding 含傳輸（使用者支付）、介接層（產品）三層可差 2–3×。
- 『≥5× 可達』須分機制錨定：binding 級 factor_corr 12–15× 證明內核可超 5×，但產品介接層 f32→f64 Python upcast 開銷把產品層降至約 3.98×——產品層與內核層分別報告。
- E2E 判定口徑執行前聲明並沿用（verdict_scope 排除 stock_corr）；元件級負結果（ic_stack 0.72×）顯式暴露；benchmark 須臂序輪轉 + 熱採樣防固定臂序偏置。

## 關鍵教訓

1. **預註冊雙門檻使 3.04× 成為無歧義裁決**——下限達成、目標未達 → 如實記負，不得成功化包裝。
2. **消費級 RTX 40 系效能變異大**——單算子加速比跨會話波動 ~2×；決策依穩健的 E2E。
3. **效能聲明必須標註層/傳輸口徑**——kernel-resident vs binding 含傳輸 vs 介接層差 2–3×。
4. **『≥5× 可達』分機制錨定**——binding factor_corr 12–15×；產品介接層 ~3.98×（Python upcast 開銷）。
5. **執行前聲明 E2E 口徑；顯式暴露元件負結果；臂序輪轉 + 熱採樣。**

## 可複現性

- **Level**: partially-reproducible（同機同 commit 同 corpus → 輸出位級確定性；計時跨會話/異機不可搬移）
- **Artifacts available**: code, data, logs, analysis-script, raw-output
- **Notes**: corpus manifest 已提交（real data_sha256=FB23D9E1CC81401EBB7C439BFDB514F5FC9A0C2C57BA1AA363852B398388504F；synth 由 loader 執行時確認）；流水輸出兩 run 雜湊逐位相等；G6 證據 self-hash 實門（11 源檔，0 mismatch）；git HEAD 釘紮。qgplearn 基線臂未安裝，best-free=min(numpy,cupy) 為替代，故 level 為 partially-reproducible（非 fully）。單算子跨會話變異 ~2× 已披露。

## 相關陽性結果

同證據集陽性對照（binding 級）：corpus_synth_v1 全量（非退化面板、同 corpus）上 factor_corr 12–15×（≥5× PASS）證明同一批內核可達 ≥5×，把 below_5x 隔離為負載/層相關而非普遍低效；但產品介接層 factor_corr 約 3.98×（Python upcast 開銷），**陽性對照須限定 binding 級**。stock_corr fast 路徑（全有效退化-mask 合成面板特例）5–12× 須與 general 口徑並排，不單獨用作內核能力證據。

## 標籤

factor-cuda, CUDA, GPU, benchmark, preregistered, FP64-ceiling, RTX-4060, speedup, negative-result, hypothesis-falsified

## 連結

- [factor-cuda 儲存庫](https://github.com/redamancy231-create/factor-cuda)（**VERIFY-AT-PUBLISH**：尚無 origin remote，URL 為投影）
- [Phase 4 benchmark 證據 phase4_bench_v1.json](https://github.com/redamancy231-create/factor-cuda/blob/main/benchmarks/results/phase4_bench_v1.json)（**VERIFY-AT-PUBLISH**）
- [端到端證據 poc4_e2e_v1.json](https://github.com/redamancy231-create/factor-cuda/blob/main/benchmarks/results/poc4_e2e_v1.json)（**VERIFY-AT-PUBLISH**）
- [negative-results-registry 儲存庫](https://github.com/redamancy231-create/negative-results-registry)
