# Negative Results Submission Template (v2)
> **What changed in v2**: Aligned with all fields in `schema/entry.schema.json`; added guidance for submission sources, hypothesis, domain/category, and reproducibility selection; clarified how the metrics table maps to `effect_size` / `sample_size` / `models_used`; added requirements for third-party analyses, field limits, and a pre-submission checklist.
> Make a copy, fill it out, and delete all instructions, examples, and unused placeholders.

---

## Submission Steps

1. **Fork** this repository
2. Copy this template and complete each section below
3. Create an entry directory using a temporary identifier as its name (for example, `temp-method-failure`). Maintainers will assign the official ID (`NRR-YYYY-NNN`) when merging the PR—this prevents ID conflicts between concurrent PRs
4. Save the entry as `.md` and `.json` files matching your temporary directory name (for example, `temp-method-failure.md` + `temp-method-failure.json`, validated against `schema/entry.schema.json`). The maintainer will rename them to the official ID when merging the PR
5. Run `python scripts/generate_registry.py` to update `registry.json`
6. Submit a **Pull Request**

---

## Submission Type (completion guidance only; do not add a JSON field)
- **First-party report**: You participated in the experiment or execution process. Report the actual configuration, baseline, sample, stopping rule, raw artifacts, and known biases.
- **Third-party analysis**: You are analyzing someone else's paper, repository, logs, or public records. Set `submitted_by` to the person submitting this entry, not the original author; use `hypothesis` for the claim you tested; set `date` to the date this analysis was completed.
- **Third-party submissions must**: In `method`, specify the source version/commit, access date, inclusion scope, and verification steps; in `actual_result`, distinguish between “what the source explicitly reports” and “your observations”; in `interpretation`, label inferences and limitations; and in `links`, provide at least one primary source. If no public evidence is available, write only “no public record was found,” not “this never happened.”
- For third-party entries, `reproducibility` assesses **whether this analysis can be independently verified from public sources**, not the overall reproducibility of the original research.
---
## Basic Information
| Field (JSON) | Content |
|---|---|
| **Entry ID `id`** | `NRR-YYYY-NNN` (assigned by maintainers; must match the directory and filenames) |
| **Title `title`** | _≤120 characters; in one sentence, include “test subject/baseline + negative result”; avoid simply writing “the experiment failed.” Example: `Structured prep/exec/post prompt did not improve code review recall over a single-stage baseline`_ |
| **Domain `domain`** | _Select the one code from the enum below that best represents the primary research subject_ |
| **Category `category`** | _Select the one code from the enum below that best represents the primary negative conclusion_ |
| **Submitter `submitted_by`** | _GitHub username or name of the person submitting this entry to the registry_ |
| **Source project `source_project`** | _Which project or paper produced the negative result? For first-party reports, enter your project name; for third-party analyses, enter the source project or paper title (≤200 characters)_ |
| **Source authors `source_authors`** | _Original authors of the source project. For first-party reports, enter yourself (same as submitted_by); for third-party analyses, enter the original authors (for example, `Kuai et al.` or `baopinshui`; ≤300 characters)_ |
| **Analyst `analyst`** | _Who analyzed this negative result? For first-party reports, enter yourself; for third-party analyses, enter yourself (same as submitted_by and different from source_authors)_ |
| **Source project URL `source_project_url`** | _(optional) Link to the source project, such as a GitHub repository or paper URL_ |
| **Date `date`** | `YYYY-MM-DD`; for first-party reports, use the experiment end date; for third-party analyses, use the date this analysis was completed |

> **How to choose `domain`**: Choose based on the primary research subject, not a tool used incidentally. `prompt-engineering` (prompt content/structure), `code-review` (code review), `methodology-extraction` (methodology extraction), `workflow-orchestration` (workflow orchestration), `document-generation` (document generation), `multi-model-collaboration` (multi-model collaboration), `quantitative-research` (quantitative research), `academic-writing` (academic writing), `tool-building` (tool development), `skill-design` (Agent/Skill design), `benchmarking` (benchmark evaluation), `other` (none apply; explain in `method`). If the entry spans multiple domains, select only the primary domain and put the others in `tags`.

> **How to choose `category`**: Choose based on the primary result directly supported by the evidence. `null-result` (no practically meaningful difference was detected), `ceiling-effect` (a bottleneck limited the attainable improvement), `worse-than-baseline` (performed worse than an explicit baseline), `failed-to-replicate` (did not reproduce an existing positive result), `methodology-failure` (the method/process could not produce a credible conclusion), `abandoned-dead-end` (stopped because of cost, data, or feasibility without claiming ineffectiveness), `hypothesis-falsified` (the evidence contradicted an explicit prediction), `tool-unfit-for-purpose` (the tool could not satisfy the target constraints), `other` (none apply; explain). If the evidence is insufficient or the sample is too small, do not label “uncertain” as `null-result`.
---
## Experiment Overview
### Original Hypothesis `hypothesis` (required, ≤500 characters)
> Write a falsifiable prediction: subject/scenario + intervention + baseline + metric + expected direction. Do not replace the original hypothesis with a post hoc explanation.  
> Example: On the same set of multi-file review tasks, a three-stage prompt will improve recall of high-severity defects by at least 10% compared with a single-stage prompt.

_(fill in)_
### Method `method` (required, ≤1000 characters)
> Describe the experimental design, control/baseline, sample and sampling method, models/tools and versions, key parameters, evaluation metrics, and stopping rule. Third-party analyses must also specify the source snapshot, inclusion scope, access date, and verification steps.  
> Example: Paired comparison across 24 tasks; the two conditions differed only in prompt structure; evaluation was blinded and performed by a separate backend; the primary metric was defect recall, with Δ≥10% predefined as a meaningful improvement.

_(fill in)_
### Expected Result `expected_result` (required, ≤500 characters)
> State the quantitative or clearly assessable result that should be observed if the hypothesis is supported, and provide a threshold whenever possible; do not just write “better performance.”

_(fill in)_
### Actual Result `actual_result` (required, ≤1000 characters)
> Present the observed facts and data first, then state whether they met the expectation; leave causal analysis for `interpretation`. Also report unfavorable outcomes, anomalies, and uncertainty. Third-party analyses must distinguish the source's statements/data from your own verification results.

_(fill in)_

| Metric (JSON) | Value |
|---|---|
| **Effect size `effect_size`** | _≤100 characters; for example, `d=0.03` or `ΔRankIC=-0.01`; if not applicable, write `N/A (reason)`_ |
| **Sample size `sample_size`** | _≤200 characters; state the unit of analysis, count, and groups/conditions, for example, `n=24 prompts × 2 conditions`_ |
| **Models/tools `models_used`** | _List each exact name and available version; in JSON, use a string array such as `["GPT-5.5", "python-docx 1.2.0"]`_ |
---
## Interpretation and Reflection
### Interpretation `interpretation` (required, ≤1000 characters)
> Address separately: ① interpretations supported by the evidence; ② remaining alternative explanations/confounding factors; and ③ the boundaries of the conclusion. Avoid presenting correlation as causation or treating “no detected difference” as “proof of no effect.”

_(fill in)_
### Lessons Learned `lessons_learned` (1–5 items; each ≤200 characters)
> Each item should state one transferable, actionable lesson without repeating the result summary. In JSON, use a string array.

1. _(fill in)_
2. _(optional)_
3. _(optional)_
---
## Reproducibility `reproducibility`
| `level` Value | Selection Guide |
|---|---|
| `fully-reproducible` | Key data, code/prompts, environment or versions, steps, and outputs are all available, allowing a third party to fully verify the result by following the instructions |
| `partially-reproducible` | The core steps can be rerun, but model snapshots, some data, the environment, or other key materials are missing |
| `not-reproducible` | Key materials have been lost, are private, or are inaccessible, so the work cannot be rerun with the available information |
| `not-assessed` | No assessment has been attempted; often used for third-party entries that only summarize the literature without checking the original materials |

| Field (JSON) | Content |
|---|---|
| **Level `reproducibility.level`** | _Enter one of the codes from the table above_ |
| **Available artifacts `reproducibility.artifacts_available`** | `prompts` / `data` / `code` / `logs` / `analysis-script` / `raw-output` / `none`; select all that apply, but do not select any other item with `none` |
| **Notes `reproducibility.notes`** | _≤500 characters; describe where the materials are located, what is missing, the runtime environment, and risks from version drift_ |
---
## Related Information
### Subsequent Positive Result `related_positive_result` (optional, ≤500 characters)
> Did another method succeed later? Provide a brief description and a link/entry ID; if none, write “None” in the .md file and omit this field from the .json file.

_(fill in or “None”)_
### Related Links `links` (optional)
> Use `[label](absolute URL)` for each item; convert it in JSON to `{"label": "...", "url": "https://..."}`. Prioritize raw data, code, papers, reports, or related NRR entries. If there are no links, use `[]` in JSON or omit the field.

- _[label](https://example.com)_
### Tags `tags` (optional, up to 10; each ≤50 characters)
> Use short, searchable tags to capture secondary domains, models, methods, and failure mechanisms; in JSON, use a string array.

_For example: `prompt-tdd`, `GPT-5.5`, `code-review`, `third-party-analysis`_
---
## Pre-Submission Checklist
- [ ] The `.md` and `.json` files both exist with matching names, and the directory name, filenames, and `id` are identical.
- [ ] All 14 required fields are complete: `id`, `title`, `domain`, `category`, `submitted_by`, `source_project`, `source_authors`, `analyst`, `date`, `hypothesis`, `method`, `expected_result`, `actual_result`, `interpretation`.
- [ ] `domain`, `category`, reproducibility level, and artifacts use the English codes defined in the schema; the date uses `YYYY-MM-DD`.
- [ ] The title and all long-text fields are within their limits; `lessons_learned` contains 1–5 items of ≤200 characters each; `tags` contains no more than 10 items of ≤50 characters each.
- [ ] The metrics table exactly matches `effect_size`, `sample_size`, and `models_used` in the JSON; all other mirrored fields also match between Markdown and JSON.
- [ ] The method includes the baseline, sample, model/tool versions, and evaluation metrics; the actual result includes evidence and uncertainty without overstating “not detected” as “proven ineffective.”
- [ ] The third-party analysis provides a primary source, version/access date, inclusion scope, and verification steps, and clearly distinguishes source facts, personal observations, and inferences.
- [ ] The reproducibility level matches the artifacts actually available; `none` is not listed alongside any other artifact.
- [ ] All examples, instructions, and `_(fill in)_` placeholders have been removed, and the JSON has been validated against `schema/entry.schema.json`.
---
*If AI assistance was used to generate or edit the entry, identify the generation model in the `.md` footer (for example, `*生成模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-25*`); do not include this note in the `.json` file.*
*生成模型：DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*翻译模型：GPT-5.6-Sol (via Codex CLI) · 2026-07-26*