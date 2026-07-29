"""Add translated NRR-2026-023 entries to language-specific registry JSONs."""
import json, shutil

EN_ENTRY = {
    "id": "NRR-2026-023",
    "title": "Four negative findings from C++ vs Rust benchmark: binary size exceeded, direction prediction overturned, sub-microsecond measurement failed, GPU small-batch speedup negative",
    "domain": "benchmarking",
    "category": "hypothesis-falsified",
    "submitted_by": "Acerolaorion",
    "date": "2026-07-29",
    "hypothesis": "Four frozen pre-registration expectations: (1) Rust binary < C++ ×1.5, (2) single-thread DTW/standardize/pattern single performance within ±10%, (3) 100 samples sufficient to distinguish ±10% performance difference, (4) GPU cupy acceleration yields positive speedup at any batch size.",
    "method": "C++ vs Rust benchmark executed per NRR Gate 2 pre-registration (hash 454873aa): 20 synthetic corpus groups + 5 edge corpus groups, 5 warmup + 100 timed iterations, wrapper-internal layer timing, ±10% threshold. GPU testing on RTX 4060 Laptop + cupy 14.1.1, N = 100/500/1000/5000.",
    "expected_result": "Binary <1.5×, single-thread performance within ±10% (0.90 ≤ ratio ≤ 1.10), 100 samples sufficient for 10% discrimination, GPU speedup >1.0 at all batch sizes.",
    "actual_result": "(1) Binary ratio 1.94×, does not satisfy <1.5×. (2) DTW ratio 0.29–0.39 (Rust 2.6–3.5× faster), standardize 0.67, pattern single 0.53—all far beyond ±10% tie range. (3) cosine median=0 ns (100 ns quantization), all core indicators CoV >5% → conclusions downgraded to indicative. (4) GPU N=100 end-to-end 0.2×, N=500 0.7×, break-even N≈1000.",
    "effect_size": "Binary deviation +29%; DTW actual ratio 61–71% below pre-registration; cosine 100% undecidable; GPU N=100 speedup −80%",
    "sample_size": "20 standard + 5 edge corpus groups, 3 independent experiments, 100 timed iterations/group",
    "models_used": ["rustc 1.97.1", "MSVC 19.51", "pyo3 0.23.5", "cupy 14.1.1", "RTX 4060 Laptop GPU"],
    "interpretation": "Pre-registration direction predictions were systematically over-optimistic in cross-language benchmarks—same algorithm ≠ same performance. Sub-microsecond measurement requires loop amplification, not independent sampling. GPU speedup being negative is a textbook fact, but seeing 0.2× firsthand remains educational.",
    "reproducibility": {
        "level": "partially-reproducible",
        "artifacts_available": ["data", "data", "code", "raw-output"],
        "notes": "Pre-registration: docs/nrr_gate2_preregistration.md (hash 454873aa). Full NRR report at etf-pattern-match-pyo3. Raw results available via GitHub Release asset."
    },
    "related_positive_result": "Rust was faster on DTW/standardize/pattern single, 16-thread batch 5.33× self-speedup. Positive findings omitted from this entry.",
    "lessons_learned": [
        "Pre-registration is not prediction—it exposes blind spots: 4/12 expectations were overturned",
        "In cross-language benchmarks, same algorithm ≠ same performance",
        "Benchmark methodology needs tiering: ms-level, µs-level, sub-µs-level",
        "GPU acceleration has a clear minimum data threshold: N<1000, speedup can be negative",
        "Binary size expectations need tuning parameters specified upfront"
    ],
    "tags": ["Rust", "C++", "benchmark", "pre-registration", "GPU", "binary-size", "sub-microsecond", "cross-language", "direction-failure"],
    "links": [
        {"label": "Full NRR-2026-023 report", "url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3/blob/main/docs/NRR-2026-023_cpp_vs_rust_comparison.md"},
        {"label": "NRR Gate 2 pre-registration", "url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3/blob/main/docs/nrr_gate2_preregistration.md"},
        {"label": "etf-pattern-match-pyo3 repository", "url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3"}
    ],
    "source_project": "etf-pattern-match-pyo3",
    "source_authors": "redamancy231-create",
    "analyst": "Acerolaorion",
    "source_project_url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3"
}

ZH_HANT_ENTRY = {
    "id": "NRR-2026-023",
    "title": "C++ vs Rust benchmark 中的四項陰性發現：二進位大小超標、預期方向被推翻、亞微秒測量失效、GPU 小批量加速比為負",
    "domain": "benchmarking",
    "category": "hypothesis-falsified",
    "submitted_by": "Acerolaorion",
    "date": "2026-07-29",
    "hypothesis": "四項凍結預登記預期——(1) Rust 二進位 < C++ ×1.5，(2) DTW/standardize/pattern single 單執行緒效能打平（±10%），(3) 100 次採樣足夠區分 ±10% 效能差異，(4) GPU cupy 加速在任意批量下均有正向收益。",
    "method": "按 NRR 門 2 預登記（hash 454873aa）執行 C++ vs Rust benchmark：20 組合成分組 + 5 組邊緣分組，預熱 5 次/計時 100 次，wrapper-internal 層計時，±10% 閾值。GPU 測試使用 RTX 4060 Laptop + cupy 14.1.1，N = 100/500/1000/5000。",
    "expected_result": "二進位 <1.5×，單執行緒效能打平（0.90 ≤ ratio ≤ 1.10），100 次採樣可區分 10% 差異，GPU 全批量加速比 >1.0。",
    "actual_result": "(1) 二進位 1.94×，不滿足 <1.5×。(2) DTW ratio 0.29–0.39（Rust 快 2.6–3.5 倍），standardize 0.67，pattern single 0.53——全部遠超出 ±10% 打平區間。(3) cosine median=0 ns（100 ns 量化），所有核心指標 CoV >5% 致結論降級為傾向性。(4) N=100 時 GPU 端到端 0.2×，N=500 時 0.7×，拐點 N≈1000。",
    "effect_size": "二進位偏差 +29%；DTW 實際 ratio 比預登記預期低 61–71%；cosine 100% 不可判定；GPU N=100 加速比 −80%",
    "sample_size": "20 組標準 + 5 組邊緣分組，3 次獨立實驗，100 次計時/組",
    "models_used": ["rustc 1.97.1", "MSVC 19.51", "pyo3 0.23.5", "cupy 14.1.1", "RTX 4060 Laptop GPU"],
    "interpretation": "預登記的方向預測在跨語言 benchmark 中系統性偏樂觀——同演算法不等於同效能。亞微秒測量需要迴圈放大而非獨立採樣。GPU 加速比為負是教科書級事實，但在實際專案中親眼看到 0.2× 仍具有教育意義。",
    "reproducibility": {
        "level": "partially-reproducible",
        "artifacts_available": ["data", "data", "code", "raw-output"],
        "notes": "預登記文件 docs/nrr_gate2_preregistration.md（hash 454873aa）。完整 NRR 報告見 etf-pattern-match-pyo3。原始結果可透過 GitHub Release asset 獲取。"
    },
    "related_positive_result": "Rust 在 DTW/standardize/pattern single 上更快，16 執行緒 batch 5.33× 自身加速。陽性發現不納入本條目。",
    "lessons_learned": [
        "預登記不是預測——是暴露盲區：4/12 指標預期被推翻",
        "跨語言 benchmark 中同演算法不等同效能",
        "基準測試方法需要分層：毫秒級、微秒級、亞微秒級",
        "GPU 加速有明確資料規模下限：N<1000，加速比可能為負",
        "二進位大小的預登記預期必須在了解調優參數的前提下設定"
    ],
    "tags": ["Rust", "C++", "benchmark", "預登記", "GPU", "二進位大小", "亞微秒測量", "跨語言對比", "方向預測失敗"],
    "links": [
        {"label": "NRR-2026-023 完整報告", "url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3/blob/main/docs/NRR-2026-023_cpp_vs_rust_comparison.md"},
        {"label": "NRR 門 2 預登記", "url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3/blob/main/docs/nrr_gate2_preregistration.md"},
        {"label": "etf-pattern-match-pyo3 倉庫", "url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3"}
    ],
    "source_project": "etf-pattern-match-pyo3",
    "source_authors": "redamancy231-create",
    "analyst": "Acerolaorion",
    "source_project_url": "https://github.com/redamancy231-create/etf-pattern-match-pyo3"
}

for fname, entry in [("registry-en.json", EN_ENTRY), ("registry-zh-Hant.json", ZH_HANT_ENTRY)]:
    with open(fname, encoding="utf-8") as fh:
        d = json.load(fh)
    d["entries"].append(entry)
    d["metadata"]["total_entries"] = 23
    d["metadata"]["last_updated"] = "2026-07-29"
    s = d["stats"]["by_domain"]
    s["benchmarking"] = s.get("benchmarking", 0) + 1
    with open(fname, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
    print(f"{fname}: {len(d['entries'])} entries, benchmarking: {s['benchmarking']}")

# Copy to docs/
for f in ["registry-en.json", "registry-zh-Hant.json"]:
    shutil.copy(f, f"docs/{f}")
    print(f"docs/{f}: copied")
