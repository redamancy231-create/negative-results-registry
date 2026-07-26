# NRR-2026-001: Prompt-TDD A2 — prep/exec/post 三段式分段對審查品質無顯著影響

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-001 |
| **標題** | Prompt 三段式分段（prep/exec/post）對程式碼審查品質無顯著影響 |
| **領域** | prompt-engineering |
| **分類** | null-result |
| **提交者** | Acerolaorion |
| **來源專案** | prompt-tdd-methodology |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-06-22 |

---

## 實驗概述

### 原始假設

> 將程式碼審查 prompt 按 prep（規範載入）/ exec（逐檔案審查）/ post（交叉驗證）三段結構化分段，預期能提升 GPT-5.5 在多檔案程式碼審查中的發現品質——相比單段"全部規範+全部檔案一起審"的基線 prompt。

### 方法

Prompt-TDD 對照實驗設計：
- **實驗組**：prep/exec/post 三段式 prompt（A2 變體）
- **對照組**：單段綜合 prompt（A2 基線）
- **任務**：對同一程式碼庫進行多檔案審查，記錄發現數量、嚴重程度、誤報率
- **樣本量**：n=24/臂
- **跨模型重現**：GPT-5.5 主實驗 + Qwen3.7-Max 獨立重現
- **評估**：雙 LLM 異後端盲評（審查者不知哪組是實驗組）

### 預期結果

> 三段式 prompt 應產生更多高品質發現、更少誤報。預期效應量 d ≥ 0.3（小到中）。

### 實際結果

兩組在發現數量、嚴重程度分佈、誤報率上均無顯著差異。

| 指標 | 數值 |
|------|------|
| 效應量 | d ≈ 0.03（trivial） |
| 樣本量 | n=24/臂 × 2 個模型重現 |
| 使用的模型 | GPT-5.5, Qwen3.7-Max |
| 重現一致性 | Qwen 重現 Δ = −0.014，方向一致（均為零） |

---

## 解讀與反思

### 為什麼會失敗？

最可能的解釋是**任務型別決定了 prompt 變異的效應量上限**。程式碼審查是一個結構化判別任務——審查者按明確的規範逐條檢查。在這種任務中，prompt 的"包裝"（分段還是單段）對輸出品質的影響遠小於任務本身的約束力。換言之：當規範足夠明確時，prompt 怎麼寫沒那麼重要。

### 學到了什麼？

1. **結構化判別任務上 prompt 變異效應近零**——與開放式生成任務（翻譯、寫作）形成對比，後者 prompt 變異效應更大
2. **規範本身比 prompt 結構更重要**——把精力放在寫好審查規範，而非 prompt 的段落組織
3. **陰性結果需要跨模型重現**——GPT-5.5 的零效應可能是單模型噪聲，Qwen 重現確認了效應的確為零
4. **實驗設計的"工程門/科學門"拆分有價值**——即使實驗結果是陰性，實驗結構本身是可複用的
5. **效應量預估應在實驗前做 ceiling probe**——如果早知道結構化判別的天花板效應，可能不會對這個方向抱太大期望

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | prompts, data, code, analysis-script |

> 完整實驗管線在 [prompt-tdd-methodology](https://github.com/redamancy231-create/prompt-tdd-methodology) 倉庫。可重跑程式碼（repeatable），但重現取決於 GPT-5.5/Qwen3.7-Max 模型版本——API 模型別名指向的後端可能已升級，結果可能不同。

---

## 相關

### 後續是否成功？

無直接後續。A2 的陰性結果 + A3 的陰性結果共同導致了"Prompt-TDD 方法論作為案例手冊而非工具庫發布"的決策——陰性結果的價值在於幫我們決定**不做什麼**。

### 相關連結

- [Prompt-TDD 方法論倉庫](https://github.com/redamancy231-create/prompt-tdd-methodology)
- [A2 案例資料](https://github.com/redamancy231-create/prompt-tdd-methodology/tree/master/examples/a2-prep-exec-post)
- [NRR-2026-002](../NRR-2026-002/NRR-2026-002.md) — 同專案的 A3 陰性結果

### 標籤

`prompt-tdd`, `GPT-5.5`, `Qwen3.7-Max`, `code-review`, `对照实验`, `零结果`, `prep-exec-post`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
