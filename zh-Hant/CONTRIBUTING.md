# 貢獻指南

> 歡迎提交你在 AI 協作中遇到的陰性／誠實結果。一本「別人踩過的坑」地圖，需要別人的坑。

---

## 提交一條陰性結果

### 你需要的

- 一個 AI 協作實驗——嘗試了什麼、預期什麼、實際發生了什麼
- 實際結果是陰性的（零結果、劣於基線、方法失敗、工具不適用……請見下方分類）
- 願意以 CC BY 4.0 發布

### 你不需要的

- 學術論文格式
- 統計顯著性（也歡迎單一案例的誠實報告）
- 「大失敗」——小到「換了一個 prompt 反而更差」也可以

### 步驟

1. **Fork** 本倉庫
2. 複製 `templates/submission-v2.md` → 依照範本填寫
3. 建立條目目錄，使用臨時標識命名（如 `temp-method-failure`）。正式 ID（`NRR-YYYY-NNN`）由維護者在合併 PR 時分配——防止併發 PR 產生 ID 衝突
4. 放入 `.md`（供人閱讀）+ `.json`（供機器讀取，依 `schema/entry.schema.json` 驗證）
5. JSON 驗證：
   ```bash
   pip install jsonschema
   python -c "import json, jsonschema; s=json.load(open('schema/entry.schema.json')); e=json.load(open('entries/NRR-2026-XXX/NRR-2026-XXX.json')); jsonschema.Draft202012Validator(s).validate(e); print('OK')"
   ```
6. 執行 `python scripts/generate_registry.py` 更新 `registry.json`
7. 提出 **Pull Request**

---

## 什麼可以提交？

| ✅ 歡迎 | ❌ 不適合 |
|---------|----------|
| Prompt 對照實驗中無顯著差異 | 「我隨便試了一下但不行」（缺少方法描述） |
| 方法論文獻提取未達穩定門檻 | 與 AI 協作無關的純技術 bug |
| 某個工具／模型在特定任務上失敗 | 未記錄實驗條件的印象式判斷 |
| 策略回測中某個因子無預測力 | 機密／未公開專案的結果 |
| 工作流程編排中某種模式產生反效果 | 抄襲／造假／未經授權的內容 |

---

## 證據門檻

所有提交必須滿足三條硬門檻，不滿足的 PR 將被退回：

| # | 門檻 | 判定標準 |
|---|------|---------|
| 1 | **假設可證偽** | `hypothesis` 包含具體預測（對象 + 干預 + 方向），不能用「我想試試 X」替代 |
| 2 | **方法可複核** | `method` 包含模型/工具版本 + 樣本描述 + 評價指標；第三方分析額外包含來源快照（commit SHA）和訪問日期 |
| 3 | **證據可追溯** | `links` 至少一項指向原始資料/程式碼/日誌/論文，不能純靠記憶 |

---

## 分類速查

### 按領域（12 類）

`prompt-engineering` · `code-review` · `methodology-extraction` · `workflow-orchestration` · `document-generation` · `multi-model-collaboration` · `quantitative-research` · `academic-writing` · `tool-building` · `skill-design` · `benchmarking` · `other`

### 按陰性結果類型（9 類）

| 類型 | 說明 |
|------|------|
| `null-result` | 實驗組與對照組無顯著差異 |
| `ceiling-effect` | 基線已經很好，改進空間為零 |
| `worse-than-baseline` | 新方法比基線更差 |
| `failed-to-replicate` | 無法重現先前有效的發現 |
| `methodology-failure` | 實驗設計／執行本身出現問題 |
| `abandoned-dead-end` | 方向本身不可行 |
| `hypothesis-falsified` | 明確推翻了原有假設 |
| `tool-unfit-for-purpose` | 所選的工具／模型不適合該任務 |
| `other` | 不在以上分類中 |

---

## 第三方分析

如果你提交的不是自己的實驗，而是分析他人專案中記錄的陰性結果：

- `source_authors` 填寫原作者（GitHub 使用者名稱或真實姓名）——與 `submitted_by`（你）區分
- `analyst` 填寫你自己（分析者）
- `submitted_by` 填寫你自己
- `source_project` 填寫源專案名稱，`source_project_url` 填寫源專案連結（推薦）
- 條件：目標專案本身**公開記錄**了該陰性結果（不能從沉默中推斷）

---

## 其他貢獻方式

- **改進 Schema**：增刪 `schema/entry.schema.json` 的欄位或調整限制 → Issue 討論 → PR
- **改進分類體系**：`methodology.md` 中的領域／類型分類 → Issue 討論
- **回報條目事實錯誤**：條目中的數字、引用等事實性錯誤 → Issue
- **翻譯**：英文／正體中文翻譯校訂 → 請見 `en/` 和 `zh-Hant/` 目錄

---

## 審查流程

提交 PR 後，維護者會逐項檢查：

1. **證據門檻**：假設可證偽、方法可複核、證據可追溯（見上方「證據門檻」）
2. **Schema 合規**：JSON 通過 `entry.schema.json` 校驗（14 個必填欄位）
3. **分類正確**：領域 + 類型選擇準確
4. **雙件一致**：`.md` 和 `.json` 內容匹配
5. **ID 分配**：維護者分配正式 `NRR-YYYY-NNN` ID 後合併

> 審核 SLA 將在首次外部 PR 後根據實際工作流確定。目前無外部貢獻，預估回應時間 ≤ 1 週。

---

## 授權

- 條目內容著作權歸提交者所有，提交即表示同意以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 發布
- 提交即確認你有權授權該內容以 CC BY 4.0 發布
- 維護者保留拒絕不符合標準之條目的權利

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-25*
