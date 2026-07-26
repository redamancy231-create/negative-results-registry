# NRR-2026-002: Prompt-TDD A3 — 宣告式路由 vs 自然語言路由無差異

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-002 |
| **標題** | 宣告式 action routing 比自然語言 routing 在 agent 路由決策上無優勢 |
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

> 宣告式 action routing（YAML/JSON 結構定義可選 action → 精確匹配）預期優於自然語言 routing（自然語言描述可選 action → 語義匹配），因為宣告式格式減少了 LLM 對 action 語義的歧義解讀空間。

### 方法

Prompt-TDD 對照實驗設計（Pilot 階段）：
- **實驗組**：宣告式 action routing prompt（YAML 結構定義 actions，嚴格匹配）
- **對照組**：自然語言 routing prompt（自然語言描述 actions，語義匹配）
- **任務**：Claude Code agent 在多步任務中自主選擇 action（檔案操作、搜尋、執行等）
- **樣本量**：Pilot 15 cases（實驗設計階段——Tier 0，未進入 Tier 1 推斷統計）
- **評估**：路由準確率 + 任務完成率

### 預期結果

> 宣告式 routing 應減少 action 選擇錯誤率，預期路由準確率提升 ≥10%。

### 實際結果

Pilot 15 cases 中，兩組路由準確率和任務完成率無顯著差異。效應量不足以支援進入 Tier 1 全規模實驗。

| 指標 | 數值 |
|------|------|
| 效應量 | Pilot 階段差異不顯著（未進入推斷統計） |
| 樣本量 | 15 cases（Pilot） |
| 使用的模型 | GPT-5.5（via Codex CLI） |

---

## 解讀與反思

### 為什麼會失敗？

兩個可能解釋：
1. **LLM 已是足夠好的語義路由器**——自然語言描述 action 時，LLM 的語義理解能力足以消除歧義，宣告式格式帶來的額外精確度是冗餘的
2. **Pilot 樣本太小**——15 cases 可能不足以檢測小效應。但 Pilot 的設計目標就是在低成本階段判斷是否值得投入全規模實驗——答案是"不值得"

### 學到了什麼？

1. **"格式=精確度"的直覺假設不全對**——寫程式碼時宣告式 > 自然語言，但 LLM 作為語義引擎反而可能消化自然語言更自然
2. **Pilot 的價值在於止損**——15 cases 就判斷了不進入 Tier 1，節省了 ~4h 實驗執行 + ~2h 審查時間
3. **陰性 Pilot 也是成功**——A3 在方法論手冊中被標記為"如何閉合無訊號實驗"的**反例**，這個教學價值比正面結果更獨特
4. **和 A2 之間的一致性值得注意但不等於領域級結論**——A2（n=24對照）和 A3（n=15 Pilot）在各自條件下均未檢出差異，形成待檢驗的元假設；需預註冊、多工、充分功效的彙總研究才能做總體判斷

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | prompts, analysis-script |

> 完整 Pilot 設計和 prompts 在 [prompt-tdd-methodology](https://github.com/redamancy231-create/prompt-tdd-methodology) 倉庫。可重跑程式碼，但重現取決於 GPT-5.5 模型版本，API 升級可能導致路由行為變化。

---

## 相關

### 後續是否成功？

無直接後續。A3 被用作"如何閉合無訊號實驗"的教學反例——這個角色比原始實驗目的（證明宣告式路由更好）更有長期價值。

### 相關連結

- [Prompt-TDD 方法論倉庫](https://github.com/redamancy231-create/prompt-tdd-methodology)
- [A3 案例資料](https://github.com/redamancy231-create/prompt-tdd-methodology/tree/master/examples/a3-action-routing)
- [NRR-2026-001](../NRR-2026-001/NRR-2026-001.md) — 同專案的 A2 陰性結果

### 標籤

`prompt-tdd`, `GPT-5.5`, `agent-routing`, `声明式-vs-NL`, `对照实验`, `Pilot`, `零结果`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
