# 阴性结果提交模板（v2）
> **v2 变更**：对齐 `schema/entry.schema.json` 的全部字段；补充提交来源、hypothesis、domain/category 与可复现性选择指南；明确指标表到 `effect_size` / `sample_size` / `models_used` 的映射；新增第三方分析要求、字段限制和提交前检查清单。
> 复制后填写，并删除所有说明、示例和未使用的占位内容。

---

## 提交步骤

1. **Fork** 本仓库
2. 复制本模板，按下方各节填写
3. 创建 `entries/NRR-YYYY-NNN/` 目录（ID 用当前最大编号 +1，分配后告知维护者）
4. 保存为 `NRR-YYYY-NNN.md`，并创建对应的 `NRR-YYYY-NNN.json`（按 `schema/entry.schema.json` 校验）
5. 运行 `python scripts/generate_registry.py` 更新 `registry.json`
6. 提 **Pull Request**

---

## 提交类型（填写说明，不新增 JSON 字段）
- **第一方报告**：你参与了实验或执行过程。应报告实际配置、基线、样本、停止规则、原始产物及已知偏差。
- **第三方分析**：你分析他人的论文、仓库、日志或公开记录。`submitted_by` 填本条目提交者，不填原作者；`hypothesis` 写你所检验的主张；`date` 填本次分析完成日期。
- **第三方提交必须做到**：在 `method` 写明来源版本/提交号、访问日期、纳入范围与核查步骤；在 `actual_result` 区分“来源明确报告”与“你的观察”；在 `interpretation` 标注推断和局限；在 `links` 至少提供一个一手来源。没有公开证据只能写“未发现公开记录”，不能写“从未发生”。
- 第三方条目的 `reproducibility` 评估的是**本次分析能否从公开来源复核**，不是替原研究判断整体可复现性。
---
## 基本信息
| 字段（JSON） | 内容 |
|---|---|
| **条目 ID `id`** | `NRR-YYYY-NNN`（由维护者分配，须与目录及文件名一致） |
| **标题 `title`** | _≤120 字符；一句话包含“测试对象/基线 + 阴性结果”，避免只写“实验失败”。例：`结构化 prompt 相比单段 prompt 未提高代码审查召回率`_ |
| **领域 `domain`** | _从下列枚举中选 1 个最能代表主要研究对象的代码_ |
| **分类 `category`** | _从下列枚举中选 1 个最能代表主要阴性结论的代码_ |
| **提交者 `submitted_by`** | _GitHub 用户名或姓名；谁向本登记册提交了这条目_ |
| **来源项目 `source_project`** | _阴性结果来自哪个项目/论文？第一方填自己的项目名，第三方填源项目/论文名（≤200 字符）_ |
| **来源作者 `source_authors`** | _源项目的原始作者。第一方填自己（与 submitted_by 同），第三方填原作者（如 `Kuai et al.`、`baopinshui`；≤300 字符）_ |
| **分析者 `analyst`** | _谁分析了这个阴性结果？第一方=自己，第三方分析=你（与 submitted_by 同，与 source_authors 不同）_ |
| **来源项目 URL `source_project_url`** | _（可选）源项目的链接，如 GitHub 仓库或论文 URL_ |
| **日期 `date`** | `YYYY-MM-DD`；第一方填实验结束日，第三方填本次分析完成日 |

> **`domain` 怎么选**：按主要研究对象选择，而不是按偶然使用的工具选择。`prompt-engineering`（prompt 内容/结构）、`code-review`（代码审查）、`methodology-extraction`（方法论提取）、`workflow-orchestration`（流程编排）、`document-generation`（文档生成）、`multi-model-collaboration`（多模型协作）、`quantitative-research`（量化研究）、`academic-writing`（学术写作）、`tool-building`（工具开发）、`skill-design`（Agent/Skill 设计）、`benchmarking`（基准评测）、`other`（均不适用，须在方法中说明）。若跨领域，只选主领域，其余放入 `tags`。

> **`category` 怎么选**：按证据直接支持的主要结果选择。`null-result`（未发现有实际意义的差异）、`ceiling-effect`（瓶颈限制了可达增益）、`worse-than-baseline`（劣于明确基线）、`failed-to-replicate`（未复现既有正结果）、`methodology-failure`（方法/流程无法产出可信结论）、`abandoned-dead-end`（因成本、数据或可行性停止，不宣称无效）、`hypothesis-falsified`（证据与明确预测相反）、`tool-unfit-for-purpose`（工具无法满足目标约束）、`other`（均不适用，须解释）。证据不足或样本过小时，不要把“不确定”写成 `null-result`。
---
## 实验概述
### 原始假设 `hypothesis`（必填，≤500 字符）
> 写成可证伪的预测：对象/场景 + 干预 + 基线 + 指标 + 预期方向；不要用结果出来后的解释替代原始假设。  
> 示例：在同一批多文件审查任务上，三段式 prompt 相比单段 prompt 将高严重度缺陷召回率提高至少 10%。

_（填写）_
### 方法 `method`（必填，≤1000 字符）
> 说明实验设计、对照/基线、样本与抽样方式、模型/工具及版本、关键参数、评价指标和停止规则。第三方分析还须说明来源快照、纳入范围、访问日期和核查步骤。  
> 示例：对 24 个任务做配对比较；两组仅 prompt 结构不同；由异后端盲评；主指标为缺陷召回率，预先以 Δ≥10% 为有意义改善。

_（填写）_
### 预期结果 `expected_result`（必填，≤500 字符）
> 写明假设成立时应观察到的量化或可判定结果，尽量给阈值；不要只写“效果更好”。

_（填写）_
### 实际结果 `actual_result`（必填，≤1000 字符）
> 先写观察事实和数据，再写是否达到预期；原因分析留到 `interpretation`。同时报告不利结果、异常和不确定性。第三方分析须区分来源原话/数据与自己的复核结果。

_（填写）_

| 指标（JSON） | 数值 |
|---|---|
| **效应量 `effect_size`** | _≤100 字符；如 `d=0.03`、`ΔRankIC=-0.01`；不适用则写 `N/A（原因）`_ |
| **样本量 `sample_size`** | _≤200 字符；写分析单位、数量、组别/条件，如 `n=24 prompts × 2 conditions`_ |
| **模型/工具 `models_used`** | _逐项写准确名称及可得版本；JSON 中为字符串数组，如 `["GPT-5.5", "python-docx 1.2.0"]`_ |
---
## 解读与反思
### 解读 `interpretation`（必填，≤1000 字符）
> 分开写：①证据支持的解释；②仍可能的替代解释/混杂因素；③结论边界。避免把相关性写成因果，或把“未检出差异”写成“证明完全无效”。

_（填写）_
### 学到了什么 `lessons_learned`（1–5 条；每条 ≤200 字符）
> 每条写一个可迁移、可行动的教训，不重复结果摘要。JSON 中为字符串数组。

1. _（填写）_
2. _（可选）_
3. _（可选）_
---
## 可复现性 `reproducibility`
| `level` 取值 | 选择指南 |
|---|---|
| `fully-reproducible` | 关键数据、代码/prompt、环境或版本、步骤和输出均可获得，第三方可按说明完整复核 |
| `partially-reproducible` | 核心步骤可重跑，但缺少模型快照、部分数据、环境或其他关键材料 |
| `not-reproducible` | 关键材料已丢失、私有或不可访问，按现有信息无法重跑 |
| `not-assessed` | 尚未尝试评估；常用于只做文献摘要且未复核原始材料的第三方条目 |

| 字段（JSON） | 内容 |
|---|---|
| **级别 `reproducibility.level`** | _填写上表中的一个代码_ |
| **可用产物 `reproducibility.artifacts_available`** | `prompts` / `data` / `code` / `logs` / `analysis-script` / `raw-output` / `none`；可多选，选 `none` 时不得再选其他项 |
| **备注 `reproducibility.notes`** | _≤500 字符；说明材料位置、缺失项、运行环境和版本漂移风险_ |
---
## 相关信息
### 后续正结果 `related_positive_result`（可选，≤500 字符）
> 后来是否用其他方法成功？写简短说明及链接/条目 ID；没有则在 .md 中写”无”，.json 中省略该字段。

_（填写或”无”）_
### 相关链接 `links`（可选）
> 每项使用 `[标签](绝对 URL)`；JSON 中转换为 `{"label": "...", "url": "https://..."}`。优先放原始数据、代码、论文、报告或相关 NRR 条目。无链接时 JSON 写 `[]` 或省略。

- _[标签](https://example.com)_
### 标签 `tags`（可选，最多 10 个；每个 ≤50 字符）
> 使用便于检索的简短标签，补充次要领域、模型、方法和失败机制；JSON 中为字符串数组。

_例如：`prompt-tdd`, `GPT-5.5`, `code-review`, `第三方分析`_
---
## 提交前检查清单
- [ ] `.md` 与 `.json` 同名成对存在，目录名、文件名和 `id` 完全一致。
- [ ] 14 个必填字段均已填写：`id`, `title`, `domain`, `category`, `submitted_by`, `source_project`, `source_authors`, `analyst`, `date`, `hypothesis`, `method`, `expected_result`, `actual_result`, `interpretation`。
- [ ] `domain`、`category`、可复现性级别和产物均使用 schema 中的英文代码；日期为 `YYYY-MM-DD`。
- [ ] 标题及各长文本未超限；`lessons_learned` 为 1–5 条且每条 ≤200 字符；`tags` 最多 10 个且每个 ≤50 字符。
- [ ] 指标表与 JSON 的 `effect_size`、`sample_size`、`models_used` 完全一致；Markdown 与 JSON 的其他镜像字段也一致。
- [ ] 方法包含基线、样本、模型/工具版本和评价指标；实际结果包含证据与不确定性，没有把“未检出”夸大为“证明无效”。
- [ ] 第三方分析已给出一手来源、版本/访问日期、纳入范围和核查步骤，并明确区分来源事实、个人观察与推断。
- [ ] 可复现性级别与实际可用产物相符；`none` 未与其他产物并列。
- [ ] 已删除全部示例、说明和 `_（填写）_` 占位符，并使用 `schema/entry.schema.json` 校验 JSON。
---
*如使用 AI 协助生成或编辑，请在 `.md` footer 注明生成模型（如 `*生成模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-25*`）；该说明不写入 `.json`。*

