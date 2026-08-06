# NRR-2026-024: CUDA 因子截面加速端到端約 2.9–3.0×，未達預註冊 ≥5× 目標

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-024 |
| **標題** | CUDA 因子截面加速端到端約 2.9–3.0×，未達預註冊 ≥5× 目標（≥2× 最低可接受已達成） |
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

預註冊錨點：CLAUDE.md PoC 決策表（≥5× NRR 門檻 / ≥2× 最低）與 PLAN.md §9。端到端（主判據）：benchmarks/poc4_e2e_v1.py + benchmarks/phase4_bench_v1.py——最小參數掃描流水，GPU 臂 pybind11 綁定（factor_cuda_pybind/factor_corr_pybind），numpy/cupy 臂 benchmarks/backends.py，對稱 reps + Phase 4 fresh 輪（**臂序輪轉 + untimed warmup + 熱採樣 + bootstrap CI**），best_free=min(numpy,cupy) 執行時記錄，verdict_scope 排除 stock_corr；**統一估計量=ratio-of-medians（min(med(numpy),med(cupy))/med(gpu)，與 committed poc4 一致）**；**決策統計量=worst-case min-of-run-medians**。單算子（產品層補充）：phase4_bench_v1.py binding 級 vs numpy/cupy，median + bootstrap CI，warm 3 + 20 採樣（原樣持久化）；介接層開銷單獨測量。可複現性：雙 corpus 經 corpus_loader_v1 驗證 data_sha256（fail-closed）；流水兩 run 輸出雜湊逐位相等；G6 證據 self-hash 實門（**fail-closed 非零退出**）；git HEAD 釘紮 + **gate provenance envelope（綁 producer commit）**；corpus_real_v1（N=93）僅正確性/確定性錨點。**經 GPT-5.6-Sol 獨立審查（13 發現）修復後 fresh 重出證。**證據：benchmarks/results/phase4_bench_v1.{json,md} + poc4_e2e_v1.json + acceptance_v1.json。

### 預期結果

假設成立：F=12 端到端加速比 ≥5×（相對 best-free，含傳輸與合併）；單算子 ≥2×。預註冊失敗判據：<2× → STOP；≥2× 且 <5× → 記負結果 NRR-2026-024。

### 實際結果

E2E F=12 端到端加速比 2.895–3.035×（fresh 輪統一估計量 **2.895×**；committed poc4_e2e_v1.json 3.035×；跨 run delta 4.6% 穩定，ratio-of-medians 估計量）。≥2× 最低可接受達成（PASS-partial），≥5× 預註冊目標未達成（假設被證偽）。單算子（binding 級含傳輸，corpus_synth_v1 全量，vs best-free）：factor_corr **13.15×**（≥5×，binding 級）；其餘本輪 cs_rank 1.59× / parameter_scan 2.28× / rolling_ic 1.99× / stock_corr general 2.31–2.65×。⚠️ 跨會話變異：單算子中位數跨會話波動顯著（如 rolling_ic 觀測 1.99×→6.94×、cs_rank 1.59×→3.11×），**不聲稱「除 factor_corr 外全部 <5×」**（rolling_ic 跨會話可超 5×）；單算子邊界斷言僅指示性，預註冊決策僅依穩健的 E2E。元件級負結果：e2e 分操作 ic_stack（IC 合併）約 0.72× 劣於基線，顯式暴露。介接層開銷：factor_corr 介接層相對裸綁定 **+238%**（1112.7ms vs 329.2ms，契約強制 f32→f64 Python upcast）；**不聲稱具體產品層 speedup**（介接層與 best-free 來自不同測量塊，機械組合無結構化依據）。corpus_real_v1（N=93）僅正確性+確定性錨點。

### 為什麼失敗

預註冊 ≥5× 端到端目標未達成（2.9–3.0×），≥2× 最低可接受達成。歸因分機制、均標為候選而非已證實：①FP64 硬體天花板（候選機制，未做 FP32 聚合路徑確認實驗）——RTX 4060 Laptop FP64≈FP32/64 可能限制 float64 聚合操作（rolling_ic/factor_corr 一般歸約/stock_corr general）的加速上限，但同證據集 factor_corr（float64）達 13.15×，削弱天花板為主因的強度；②launch/傳輸/佔用開銷（候選機制）——解釋 float32 操作與產品層傳輸成本；③陽性對照（binding 級）證明內核可達 ≥5×——factor_corr 13.15×（同 corpus_synth_v1 非退化面板），below_5x 是負載/層相關而非普遍內核低效；④層差異披露（非因果）——acceptance kernel-resident 與當前 binding 含傳輸來自不同會話/基線，僅披露層差異，不作「kernel 高估使用者側」的因果聲明（跨會話方向不穩）；⑤介接層 Python 開銷——fc 介接層契約強制 f32→f64 Python upcast（factor_corr +238%），為產品最佳化機會非綁定缺陷，不機械組合產品層 speedup。跨會話變異：單算子中位數波動大（rolling_ic 1.99→6.94×），單算子邊界斷言不作決策依據，決策僅依 E2E（穩定）。未驗證的替代解釋（更高 FP64 吞吐 GPU、FP32 聚合路徑、kernel 調優）標為未驗證假設。結論限定於 RTX 4060 Laptop + 固定 corpus + 排除 stock_corr 的 E2E 口徑。

### 我們學到了什麼

- 預註冊雙門檻（≥2× 最低 / ≥5× 目標）使 2.9–3.0× 成為無歧義裁決：下限達成、目標未達 → 如實記負，不得把已記錄缺口包裝為成功。
- 消費級 GPU（RTX 40 系）效能變異大——單算子加速比跨會話可波動數倍（rolling_ic 1.99→6.94×），預註冊決策須基於穩健的端到端判據而非波動大的單算子邊界。
- 效能聲明必須標註層與傳輸口徑 + 統一估計量：kernel-resident/binding 含傳輸/介接層三層口徑不同；ratio-of-medians vs median-of-ratios 估計量給出不同數字（3.076 vs 2.895），須預註冊唯一估計量。
- 『≥5× 可達』須分機制錨定 + 陽性對照限定層：binding 級 factor_corr 13.15× 證明內核可超 5×，但介接層 Python upcast 有真實開銷（+238%），不機械組合產品層 speedup。
- E2E 判定口徑執行前聲明並沿用（verdict_scope 排除 stock_corr）；元件級負結果（ic_stack 0.72×）顯式暴露；benchmark 須臂序輪轉 + untimed warmup + 熱採樣防偏置；門須 fail-closed 非零退出。

## 關鍵教訓

1. **預註冊雙門檻使 2.9–3.0× 成為無歧義裁決**——下限達成、目標未達 → 如實記負，不得成功化包裝。
2. **消費級 RTX 40 系效能變異大**——單算子加速比跨會話波動數倍（rolling_ic 1.99→6.94×）；決策依穩健的 E2E。
3. **效能聲明必須標註層/傳輸口徑 + 單一預註冊估計量**——ratio-of-medians vs median-of-ratios 不同（3.076 vs 2.895）。
4. **『≥5× 可達』分機制錨定、陽性對照限定層**——binding factor_corr 13.15×；介接層 Python upcast +238% 是真實開銷，不機械組合產品層 speedup。
5. **執行前聲明 E2E 口徑；顯式暴露元件負結果；臂序輪轉 + untimed warmup + 熱採樣；門 fail-closed。**

## 可複現性

- **Level**: partially-reproducible（同機同 commit 同 corpus → 輸出位級確定性；計時跨會話/異機不可搬移）
- **Artifacts available**: code, data, logs, analysis-script, raw-output
- **Notes**: corpus manifest 已提交（real data_sha256=FB23D9E1CC81401EBB7C439BFDB514F5FC9A0C2C57BA1AA363852B398388504F；synth 由 loader 執行時確認）；流水輸出兩 run 雜湊逐位相等；G6 證據 self-hash 實門（11 源檔，fail-closed 非零退出）；gate provenance envelope（綁 producer commit）。qgplearn 基線臂未安裝，best-free=min(numpy,cupy) 為替代，故 level 為 partially-reproducible（非 fully）。單算子跨會話變異已披露（1.59–6.94× 觀測區間）。

## 相關陽性結果

同證據集陽性對照（binding 級）：corpus_synth_v1 全量（非退化面板、同 corpus）上 factor_corr 13.15×（≥5× PASS）證明同一批內核可達 ≥5×，把 below_5x 隔離為負載/層相關而非普遍低效；**陽性對照限定 binding 級**（介接層有 Python upcast 開銷）。stock_corr fast 路徑（全有效退化-mask 合成面板特例）5–12× 須與 general 口徑並排，不單獨用作內核能力證據。

## 標籤

factor-cuda, CUDA, GPU, benchmark, preregistered, FP64-ceiling, RTX-4060, speedup, negative-result, hypothesis-falsified

## 連結

- [factor-cuda 儲存庫](https://github.com/redamancy231-create/factor-cuda)（**VERIFY-AT-PUBLISH**：尚無 origin remote，URL 為投影）
- [Phase 4 benchmark 證據 phase4_bench_v1.json](https://github.com/redamancy231-create/factor-cuda/blob/main/benchmarks/results/phase4_bench_v1.json)（**VERIFY-AT-PUBLISH**）
- [端到端證據 poc4_e2e_v1.json](https://github.com/redamancy231-create/factor-cuda/blob/main/benchmarks/results/poc4_e2e_v1.json)（**VERIFY-AT-PUBLISH**）
- [negative-results-registry 儲存庫](https://github.com/redamancy231-create/negative-results-registry)
