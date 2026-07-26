# Contributing Guide

> We welcome submissions of negative/honest results you have encountered in AI collaboration. A map of "pitfalls others have encountered" needs other people to share their pitfalls.

---

## Submit a Negative Result

### What You Need

- An AI collaboration experiment—what you tried, what you expected, and what actually happened
- An actual negative result (a null result, worse-than-baseline performance, a failed method, an unsuitable tool, and so on—see the taxonomy below)
- A willingness to release it under CC BY 4.0

### What You Do Not Need

- Academic paper formatting
- Statistical significance (honest single-case reports are also welcome)
- A "major failure"—even something as small as "I changed the prompt and it actually got worse" qualifies

### Steps

1. **Fork** this repository
2. Copy `templates/submission-v2.md` → complete it according to the template
3. Create an entry directory with a temporary name (e.g., `temp-method-failure`). The official ID (`NRR-YYYY-NNN`) will be assigned by the maintainer when merging the PR — this prevents ID collisions from concurrent PRs
4. Add a `.md` file (human-readable) + a `.json` file (machine-readable; validate it against `schema/entry.schema.json`)
5. Validate the JSON:
   ```bash
   pip install jsonschema
   python -c "import json, jsonschema; s=json.load(open('schema/entry.schema.json')); e=json.load(open('entries/NRR-2026-XXX/NRR-2026-XXX.json')); jsonschema.Draft202012Validator(s).validate(e); print('OK')"
   ```
6. Run `python scripts/generate_registry.py` to update `registry.json`
7. Open a **Pull Request**

---

## What Can Be Submitted?

| ✅ Welcome | ❌ Not Suitable |
|---------|----------|
| No significant difference in a controlled prompt experiment | "I tried it casually and it didn't work" (no description of the method) |
| Methodology extraction that failed to meet the stability threshold | A purely technical bug unrelated to AI collaboration |
| A particular tool/model failed on a specific task | An impressionistic judgment with no experimental conditions recorded |
| A factor had no predictive power in a strategy backtest | Results from confidential/nonpublic projects |
| A pattern in workflow orchestration produced counterproductive effects | Plagiarized/fabricated/unauthorized content |

---

## Evidence Thresholds

All submissions must meet three hard thresholds. PRs that fail any of them will be returned:

| # | Threshold | Criterion |
|---|-----------|----------|
| 1 | **Falsifiable hypothesis** | `hypothesis` contains a concrete prediction (subject + intervention + direction), not just "I wanted to try X" |
| 2 | **Reproducible method** | `method` includes model/tool versions + sample description + evaluation metrics; third-party analyses additionally include a source snapshot (commit SHA) and access date |
| 3 | **Traceable evidence** | `links` includes at least one item pointing to raw data, code, logs, or a paper — not purely from memory |

---

## Taxonomy Quick Reference

### By Domain (12 Categories)

`prompt-engineering` · `code-review` · `methodology-extraction` · `workflow-orchestration` · `document-generation` · `multi-model-collaboration` · `quantitative-research` · `academic-writing` · `tool-building` · `skill-design` · `benchmarking` · `other`

### By Negative Result Type (9 Categories)

| Type | Description |
|------|------|
| `null-result` | No significant difference between the experimental and control groups |
| `ceiling-effect` | The baseline is already strong, leaving no room for improvement |
| `worse-than-baseline` | The new method performs worse than the baseline |
| `failed-to-replicate` | A previously effective finding cannot be replicated |
| `methodology-failure` | The experimental design or execution itself had problems |
| `abandoned-dead-end` | The direction itself is not viable |
| `hypothesis-falsified` | The original hypothesis was explicitly disproven |
| `tool-unfit-for-purpose` | The selected tool/model is unsuitable for the task |
| `other` | Not covered by the categories above |

---

## Third-Party Analysis

If you are submitting an analysis of a negative result documented in someone else's project rather than your own experiment:

- `source_authors` — the original authors (GitHub username or real name). This is different from `submitted_by` (you)
- `analyst` — yourself (the person who performed the analysis)
- `submitted_by` — yourself
- `source_project` — name of the source project; `source_project_url` — link to the source (recommended)
- Requirement: the target project must have **publicly documented** the negative result itself (it cannot be inferred from silence)

---

## Other Ways to Contribute

- **Improve the Schema**: Add or remove fields or adjust constraints in `schema/entry.schema.json` → discuss in an Issue → submit a PR
- **Improve the Taxonomy**: Domain/type classifications in `methodology.md` → discuss in an Issue
- **Report Factual Errors in an Entry**: Factual errors in an entry, such as numbers or citations → open an Issue
- **Translate**: English/Traditional Chinese translations → see the `en/` and `zh-Hant/` directories

---

## Review Process

After you submit a PR, the maintainer will check:

1. **Evidence thresholds**: falsifiable hypothesis, reproducible method, traceable evidence (see "Evidence Thresholds" above)
2. **Schema compliance**: JSON passes `entry.schema.json` validation (14 required fields)
3. **Classification**: domain + type are accurate
4. **Dual-file consistency**: `.md` and `.json` content matches
5. **ID assignment**: the maintainer assigns the official `NRR-YYYY-NNN` ID before merging

> Review SLA will be determined after the first external PR based on actual workflow. With no external contributions currently, estimated response time ≤ 1 week.

---

## License

- The submitter retains copyright to the entry content; by submitting, you agree to release it under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- By submitting, you confirm that you have the right to authorize the release of the content under CC BY 4.0
- The maintainer reserves the right to reject entries that do not meet the standards

---

*Generation model: DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*Translation model: GPT-5.6-Sol (via Codex CLI) · 2026-07-25*