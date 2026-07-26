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
3. Create an `entries/NRR-YYYY-NNN/` directory (use the current highest number +1 for the ID; the ID will be assigned by the maintainer when merging the PR, so use a temporary slug first)
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

- Set `submitted_by` to yourself (the analyst)
- In `reproducibility.notes`, label it as a "third-party analysis entry" and identify the source project
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

1. JSON Schema compliance (passes validation against `entry.schema.json`)
2. Consistency between the entry content and the template
3. Classification accuracy (domain + type)
4. ID uniqueness
5. Both the `.md` and `.json` files are present and their content is consistent

Once approved, the PR will be merged, and `registry.json` will be automatically updated with the entry.

---

## License

- The submitter retains copyright to the entry content; by submitting, you agree to release it under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- By submitting, you confirm that you have the right to authorize the release of the content under CC BY 4.0
- The maintainer reserves the right to reject entries that do not meet the standards

---

*Generation model: DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*Translation model: GPT-5.6-Sol (via Codex CLI) · 2026-07-25*