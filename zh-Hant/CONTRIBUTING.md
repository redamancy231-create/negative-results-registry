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
2. 複製 `templates/submission.md` → 依照範本填寫
3. 建立 `entries/NRR-YYYY-NNN/` 目錄（ID 使用目前最大編號 +1，例如現有最大編號為 NRR-2026-018，則使用 NRR-2026-019）
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

- `submitted_by` 填寫你自己（分析者）
- 在 `reproducibility.notes` 中標註「第三方分析條目」和來源專案
- 條件：目標專案本身**公開記錄**了該陰性結果（不能從沉默中推斷）

---

## 其他貢獻方式

- **改進 Schema**：增刪 `schema/entry.schema.json` 的欄位或調整限制 → Issue 討論 → PR
- **改進分類體系**：`methodology.md` 中的領域／類型分類 → Issue 討論
- **回報條目事實錯誤**：條目中的數字、引用等事實性錯誤 → Issue
- **翻譯**：英文／正體中文翻譯 → 請見 `en/` 和 `zh-Hant/` 目錄

---

## 審查流程

提交 PR 後，維護者會檢查：

1. 符合 JSON Schema 規範（通過 `entry.schema.json` 驗證）
2. 條目內容與範本的一致性
3. 分類正確性（領域 + 類型）
4. ID 唯一性
5. `.md` 和 `.json` 兩者齊全且內容一致

通過後合併，`registry.json` 會隨條目自動更新。

---

## 授權

- 條目內容著作權歸提交者所有，提交即表示同意以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 發布
- 提交即確認你有權授權該內容以 CC BY 4.0 發布
- 維護者保留拒絕不符合標準之條目的權利

---

*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-25*
