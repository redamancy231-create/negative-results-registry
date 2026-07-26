# 陰性結果提交範本（v2）
> **v2 變更**：對齊 `schema/entry.schema.json` 的所有欄位；補充提交來源、hypothesis、domain/category 與可重現性選擇指南；明確說明指標表與 `effect_size` / `sample_size` / `models_used` 的對應關係；新增第三方分析要求、欄位限制和提交前檢查清單。
> 複製後填寫，並刪除所有說明、範例和未使用的預留內容。

---

## 提交步驟

1. **Fork** 本倉庫
2. 複製本範本，依下方各節填寫
3. 建立條目目錄，使用臨時標識命名（如 `temp-method-failure`）。正式 ID（`NRR-YYYY-NNN`）由維護者在合併 PR 時分配——防止併發 PR 產生 ID 衝突
4. 儲存為與臨時目錄名稱一致的 `.md` 和 `.json` 檔案（如 `temp-method-failure.md` + `temp-method-failure.json`，依 `schema/entry.schema.json` 驗證）。合併 PR 時，維護者會重新命名為正式 ID
5. 執行 `python scripts/generate_registry.py` 更新 `registry.json`
6. 提出 **Pull Request**

---

## 提交類型（填寫說明，不新增 JSON 欄位）
- **第一方報告**：你參與了實驗或執行過程。應報告實際設定、基線、樣本、停止規則、原始產物及已知偏差。
- **第三方分析**：你分析他人的論文、倉庫、日誌或公開記錄。`submitted_by` 填寫本條目的提交者，不填原作者；`hypothesis` 寫下你所檢驗的主張；`date` 填寫本次分析完成日期。
- **第三方提交必須做到**：在 `method` 寫明來源版本／提交號、訪問日期、納入範圍與核查步驟；在 `actual_result` 區分「來源明確報告」與「你的觀察」；在 `interpretation` 標註推斷和局限；在 `links` 至少提供一個一手來源。沒有公開證據時只能寫「未發現公開記錄」，不能寫「從未發生」。
- 第三方條目的 `reproducibility` 評估的是**本次分析能否依公開來源複核**，不是代替原研究判斷整體可重現性。
---
## 基本資訊
| 欄位（JSON） | 內容 |
|---|---|
| **條目 ID `id`** | `NRR-YYYY-NNN`（由維護者分配，須與目錄及檔案名稱一致） |
| **標題 `title`** | _≤120 字元；以一句話包含「測試對象／基線 + 陰性結果」，避免只寫「實驗失敗」。例：`结构化 prompt 相比单段 prompt 未提高代码审查召回率`_ |
| **領域 `domain`** | _從下列列舉中選擇 1 個最能代表主要研究對象的代碼_ |
| **分類 `category`** | _從下列列舉中選擇 1 個最能代表主要陰性結論的代碼_ |
| **提交者 `submitted_by`** | _GitHub 使用者名稱或姓名；向本登記冊提交此條目的人_ |
| **來源專案 `source_project`** | _陰性結果來自哪個專案／論文？第一方填寫自己的專案名稱，第三方填寫來源專案／論文名稱（≤200 字元）_ |
| **來源作者 `source_authors`** | _來源專案的原作者。第一方填寫自己（與 submitted_by 相同），第三方填寫原作者（如 `Kuai et al.`、`baopinshui`；≤300 字元）_ |
| **分析者 `analyst`** | _誰分析了這個陰性結果？第一方=自己，第三方分析=你（與 submitted_by 相同，與 source_authors 不同）_ |
| **來源專案 URL `source_project_url`** | _（可選）來源專案的連結，如 GitHub 倉庫或論文 URL_ |
| **日期 `date`** | `YYYY-MM-DD`；第一方填寫實驗結束日期，第三方填寫本次分析完成日期 |

> **`domain` 如何選擇**：依主要研究對象選擇，而不是依偶然使用的工具選擇。`prompt-engineering`（prompt 內容／結構）、`code-review`（程式碼審查）、`methodology-extraction`（方法論提取）、`workflow-orchestration`（工作流程編排）、`document-generation`（檔案生成）、`multi-model-collaboration`（多模型協作）、`quantitative-research`（量化研究）、`academic-writing`（學術寫作）、`tool-building`（工具開發）、`skill-design`（Agent/Skill 設計）、`benchmarking`（基準測試）、`other`（皆不適用，須在方法中說明）。若橫跨多個領域，只選擇主要領域，其餘放入 `tags`。

> **`category` 如何選擇**：依證據直接支持的主要結果選擇。`null-result`（未發現具實際意義的差異）、`ceiling-effect`（瓶頸限制了可達增益）、`worse-than-baseline`（劣於明確基線）、`failed-to-replicate`（未能重現既有陽性結果）、`methodology-failure`（方法／流程無法產出可信結論）、`abandoned-dead-end`（因成本、資料或可行性而停止，不宣稱無效）、`hypothesis-falsified`（證據與明確預測相反）、`tool-unfit-for-purpose`（工具無法滿足目標約束）、`other`（皆不適用，須加以解釋）。證據不足或樣本過少時，不要將「不確定」寫成 `null-result`。
---
## 實驗概述
### 原始假設 `hypothesis`（必填，≤500 字元）
> 寫成可證偽的預測：對象／場景 + 干預 + 基線 + 指標 + 預期方向；不要以結果出來後的解釋取代原始假設。  
> 範例：在同一批多檔案審查任務中，三段式 prompt 相較於單段 prompt，會將高嚴重度缺陷召回率提高至少 10%。

_（填寫）_
### 方法 `method`（必填，≤1000 字元）
> 說明實驗設計、對照／基線、樣本與抽樣方式、模型／工具及版本、關鍵參數、評價指標和停止規則。第三方分析還須說明來源快照、納入範圍、訪問日期和核查步驟。  
> 範例：對 24 個任務進行配對比較；兩組僅 prompt 結構不同；由不同後端盲評；主要指標為缺陷召回率，預先以 Δ≥10% 為具實際意義的改善。

_（填寫）_
### 預期結果 `expected_result`（必填，≤500 字元）
> 寫明假設成立時應觀察到的量化或可判定結果，盡量提供閾值；不要只寫「效果更好」。

_（填寫）_
### 實際結果 `actual_result`（必填，≤1000 字元）
> 先寫觀察事實和資料，再寫是否達到預期；原因分析留到 `interpretation`。同時報告不利結果、異常和不確定性。第三方分析須區分來源原文／資料與自己的複核結果。

_（填寫）_

| 指標（JSON） | 數值 |
|---|---|
| **效應量 `effect_size`** | _≤100 字元；如 `d=0.03`、`ΔRankIC=-0.01`；不適用則寫 `N/A（原因）`_ |
| **樣本量 `sample_size`** | _≤200 字元；寫明分析單位、數量、組別／條件，如 `n=24 prompts × 2 conditions`_ |
| **模型／工具 `models_used`** | _逐項寫出準確名稱及可取得的版本；JSON 中為字串陣列，如 `["GPT-5.5", "python-docx 1.2.0"]`_ |
---
## 解讀與反思
### 解讀 `interpretation`（必填，≤1000 字元）
> 分開寫：①證據支持的解釋；②仍可能存在的替代解釋／混雜因素；③結論邊界。避免將相關性寫成因果，或將「未檢出差異」寫成「證明完全無效」。

_（填寫）_
### 學到了什麼 `lessons_learned`（1–5 條；每條 ≤200 字元）
> 每條寫一項可移轉、可付諸行動的教訓，不重複結果摘要。JSON 中為字串陣列。

1. _（填寫）_
2. _（可選）_
3. _（可選）_
---
## 可重現性 `reproducibility`
| `level` 值 | 選擇指南 |
|---|---|
| `fully-reproducible` | 關鍵資料、程式碼／prompt、環境或版本、步驟和輸出均可取得，第三方可依說明完整複核 |
| `partially-reproducible` | 核心步驟可重新執行，但缺少模型快照、部分資料、環境或其他關鍵材料 |
| `not-reproducible` | 關鍵材料已遺失、屬私有內容或無法存取，依現有資訊無法重新執行 |
| `not-assessed` | 尚未嘗試評估；常用於僅做文獻摘要且未複核原始材料的第三方條目 |

| 欄位（JSON） | 內容 |
|---|---|
| **級別 `reproducibility.level`** | _填寫上表中的一個代碼_ |
| **可用產物 `reproducibility.artifacts_available`** | `prompts` / `data` / `code` / `logs` / `analysis-script` / `raw-output` / `none`；可複選，選擇 `none` 時不得再選其他項目 |
| **備註 `reproducibility.notes`** | _≤500 字元；說明材料位置、缺漏項目、執行環境和版本漂移風險_ |
---
## 相關資訊
### 後續陽性結果 `related_positive_result`（可選，≤500 字元）
> 後來是否透過其他方法成功？寫下簡短說明及連結／條目 ID；若無，則在 .md 中寫「無」，並在 .json 中省略該欄位。

_（填寫或「無」）_
### 相關連結 `links`（可選）
> 每項使用 `[標籤](絕對 URL)`；在 JSON 中轉換為 `{"label": "...", "url": "https://..."}`。優先放置原始資料、程式碼、論文、報告或相關 NRR 條目。沒有連結時，JSON 寫 `[]` 或省略。

- _[標籤](https://example.com)_
### 標籤 `tags`（可選，最多 10 個；每個 ≤50 字元）
> 使用便於檢索的簡短標籤，補充次要領域、模型、方法和失敗機制；JSON 中為字串陣列。

_例如：`prompt-tdd`, `GPT-5.5`, `code-review`, `第三方分析`_
---
## 提交前檢查清單
- [ ] `.md` 與 `.json` 以相同名稱成對存在，目錄名稱、檔案名稱和 `id` 完全一致。
- [ ] 14 個必填欄位均已填寫：`id`, `title`, `domain`, `category`, `submitted_by`, `source_project`, `source_authors`, `analyst`, `date`, `hypothesis`, `method`, `expected_result`, `actual_result`, `interpretation`。
- [ ] `domain`、`category`、可重現性級別和產物均使用 schema 中的英文代碼；日期格式為 `YYYY-MM-DD`。
- [ ] 標題及各長文字均未超過限制；`lessons_learned` 為 1–5 條且每條 ≤200 字元；`tags` 最多 10 個且每個 ≤50 字元。
- [ ] 指標表與 JSON 的 `effect_size`、`sample_size`、`models_used` 完全一致；Markdown 與 JSON 的其他鏡像欄位也一致。
- [ ] 方法包含基線、樣本、模型／工具版本和評價指標；實際結果包含證據與不確定性，沒有將「未檢出」誇大為「證明無效」。
- [ ] 第三方分析已提供一手來源、版本／訪問日期、納入範圍和核查步驟，並明確區分來源事實、個人觀察與推斷。
- [ ] 可重現性級別與實際可用產物相符；`none` 未與其他產物並列。
- [ ] 已刪除所有範例、說明和 `_（填寫）_` 預留內容，並使用 `schema/entry.schema.json` 驗證 JSON。
---
*如使用 AI 協助生成或編輯，請在 `.md` 頁尾註明生成模型（如 `*生成模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-25*`）；此說明不寫入 `.json`。*
*翻譯模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*
