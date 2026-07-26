# NRR-2026-007: AI 自審查漏掉死亡判據順序 bug

## 基本資訊

| 欄位 | 內容 |
|------|------|
| **條目 ID** | NRR-2026-007 |
| **標題** | AI 自審查漏掉死亡判據順序 bug——Claude 的對抗式自檢未能檢測到 Codex 一眼看到的硬傷 |
| **領域** | skill-design |
| **分類** | methodology-failure |
| **提交者** | Acerolaorion |
| **來源專案** | claude-skills |
| **來源作者** | Acerolaorion |
| **分析者** | Acerolaorion |
| **日期** | 2026-07-06 |

---

## 實驗概述

### 原始假設

> Claude（DeepSeek-V4-Pro，即 kill-test-first Skill 的設計者）對自己的 Skill 進行對抗式自檢後，預期能找出所有結構性缺陷——尤其是直接違反 Skill 自身核心原則（預登記：死亡判據必須在看到結果前制定）的錯誤。

### 方法

kill-test-first Skill 的設計者完成了 Skill 初版後，進行了對抗式自檢。隨後將 Skill 提交給 Codex CLI（GPT-5.5，不同後端，零涉入）進行獨立審查。對比自檢發現 vs 獨立審查發現。Qwen3.7-Max 執行第二輪獨立審查。

### 預期結果

> 自檢應找出所有 MAJOR 及以上結構性缺陷；獨立審查的增量發現應為 MINOR/MODERATE 層級。

### 實際結果

**Codex 第一輪發現 5 個硬傷**，最關鍵的是死亡判據順序 bug——Skill 門 1 協議將"制定死亡判據"放在"看到實驗結果"之後，直接違背預登記核心原則。Claude 的自檢完全漏掉了這個 bug。Qwen 第二輪又新發現 REDESIGN 可逃避 STOP + 三態裁決未覆蓋所有象限。

| 指標 | 數值 |
|------|------|
| 效應量 | 自檢 0 個 MAJOR → Codex 5 個硬傷（含 1 個直接違背核心原則的順序 bug）→ Qwen 第二輪 +2 個新問題 |
| 樣本量 | 1 個 Skill × 3 輪審查（1 自檢 + 2 獨立） |
| 使用的模型 | DeepSeek-V4-Pro, GPT-5.5, Qwen3.7-Max |

---

## 解讀與反思

### 為什麼會失敗？

**同一後端自我審查存在結構性盲區。** 不是 Claude 能力不足——死亡判據順序 bug 之所以被漏掉，正是因為設計者自己的思維已經固化在"當然要先看結果再判死刑"的直覺中——而這恰恰是預登記要對抗的認知偏差。不同後端（GPT-5.5）沒有這個思維慣性，一眼就看到矛盾。

### 學到了什麼？

1. **同一後端自我審查存在結構性盲區**——設計者的思維慣性會遮蔽違背自身設計直覺的錯誤
2. **死亡判據順序 bug 是最危險的 bug 型別**——不是邏輯錯誤，是設計者認知偏差的直接投射
3. **兩輪異後端審查的價值超過同後端多輪**——Codex（結構性問題）+ Qwen（邊界條件）的互補性遠超兩輪同後端
4. **Skill 自身的死亡判據原則在本案例中被驗證有效**——"用它自己的藥——出現即棄用/重構"

---

## 可重現性

| 維度 | 評估 |
|------|------|
| **整體可重現性** | partially-reproducible |
| **可用產物** | prompts, logs, raw-output |

> 完整審查記錄在 [claude-skills](https://github.com/redamancy231-create/claude-skills) 的 `kill-test-first/EXAMPLES.md` 案例 2。三版迭代的 prompts 和審查報告均保留。

---

## 相關

### 後續是否成功？

全部修復。Codex 第二輪審查確認全部閉合。核心教訓：異後端獨立審查的必要性被直接證實。

### 相關連結

- [Claude Skills 倉庫](https://github.com/redamancy231-create/claude-skills)
- [Kill-Test-First EXAMPLES（案例 2）](https://github.com/redamancy231-create/claude-skills/blob/main/kill-test-first/EXAMPLES.md)

### 標籤

`自审盲区`, `kill-test-first`, `Codex审查`, `死亡判据`, `预登记`, `顺序bug`, `独立审查`, `Skill设计`

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
