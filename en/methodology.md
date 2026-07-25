# Why Record Negative Results?

> The scientific community has a "file drawer problem": positive results get published, while negative results get tucked away in a drawer. The result is publication bias—we always see "what works" in the literature and rarely see "what does not work."
>
> The same is true in the field of AI collaboration. GitHub is filled with showcases of "I used AI to do X," but almost no one documents "I tried X, and it failed."

## Why Negative Results Are Valuable

### 1. Prevent Others from Repeating the Same Mistakes

Knowing that you went down a dead end means I will not go down it again. This is especially important in AI collaboration—many experiments that "were tried but had no effect" took hours or even days.

### 2. Negative Results May Be "Conditional Negatives"

Something that fails with a particular model version, prompt phrasing, or task type may succeed under different conditions. Recording the precise conditions of failure is more informative than recording success.

### 3. Honesty Builds Trust

Someone who says "all my experiments succeeded" has either never conducted an experiment or is lying. Making negative results public demonstrates your commitment to the facts.

### 4. Methodological Evolution Requires Failure Data

If your methodological framework is distilled only from successful cases, it will have systematic bias. Knowing what does **not** work is just as important as knowing what does work.

## What This Registry Is Not

- ❌ It is not an academic journal—full paper formatting is not required
- ❌ It is not a "losers' club"—negative results are a normal research output
- ❌ It does not require statistical significance—honest reports of individual cases are also welcome
- ❌ It is not limited to "major failures"—something as small as "I changed the prompt and it actually got worse" can also be registered

## What This Registry Is

- ✅ A structured, searchable database of experience
- ✅ A map of "pitfalls others have encountered"
- ✅ A community practice that encourages honesty

---

## Classification System

### By Domain

| Code | Domain | Description |
|------|------|------|
| prompt-engineering | Prompt Engineering | Prompt design, comparative experiments, and structural optimization |
| code-review | Code Review | Multi-model review, bug detection, and quality assessment |
| methodology-extraction | Methodology Extraction | Extracting reusable patterns from projects |
| workflow-orchestration | Workflow Orchestration | Multi-agent orchestration and parallel/pipeline strategies |
| document-generation | Document Generation | MD→DOCX/PDF and multilingual translation |
| multi-model-collaboration | Multi-Model Collaboration | Model role assignment and cross-validation |
| quantitative-research | Quantitative Research | Factors, strategies, backtesting, and ML models |
| academic-writing | Academic Writing | Paper pipelines and literature reviews |
| tool-building | Tool Development | CLI tools and skill development |
| skill-design | Skill Design | Claude Code skills/plugins |
| benchmarking | Benchmarking | Model/tool performance comparisons |
| other | Other | Not covered by the categories above |

### By Negative Result Type (Category)

| Code | Type | Description |
|------|------|------|
| null-result | Null Result | No significant difference between the experimental and control groups |
| ceiling-effect | Ceiling Effect | The baseline is already strong, leaving no room for improvement |
| worse-than-baseline | Worse Than Baseline | The new method performs worse than the baseline |
| failed-to-replicate | Failed to Replicate | A previously effective finding cannot be replicated |
| methodology-failure | Methodology Failure | The experimental design or execution itself was flawed |
| abandoned-dead-end | Abandoned Dead End | The direction itself is infeasible and was abandoned |
| hypothesis-falsified | Hypothesis Falsified | The original hypothesis was clearly disproven |
| tool-unfit-for-purpose | Tool Unfit for Purpose | The selected tool/model is not suitable for the task |
| other | Other | Not covered by the categories above |

---

## Relationship to the Academic Literature

In 2026, several papers have already provided external support for the academic value of negative results:

- **Kohli (2026-05)**: A panel of 9 LLM reviewers produces only ~2 effectively independent votes—adding more models may not help, a negative result supported by quantitative evidence
- **Kuai et al. (2026-04)**: 18 LLMs exhibit widespread "behavioral entanglement"—models are not as independent as you might think
- **Nájera et al. (2026-05)**: Reframes multi-model disagreement as a diagnostic signal—"models disagreeing" is not a bug

These papers themselves publish findings that run counter to intuition. This registry aims to do the same at a more lightweight level.

---

*Generation model: DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-25*
*Translation model: GPT-5.6-Sol (via Codex CLI) · 2026-07-25*