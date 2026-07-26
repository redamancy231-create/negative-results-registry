# QA Test Report: Pages Site Functional Review
Tester: GPT-5.6-Sol (via Codex CLI) · 2026-07-26

## Test Environment and Method

- Reviewed the HTML source embedded in the prompt; it matches `docs/index.html` apart from the generated-file comment.
- Served `docs/` over local HTTP and exercised the page in headless Chrome 150.0.7871.186 through the Chrome DevTools Protocol.
- Inspected the actual data files: `docs/registry.json`, `docs/registry-en.json`, and `docs/registry-zh-Hant.json` (22 entries each, matching IDs and order).
- Simulated delayed and failed fetches to test concurrent language switches and missing translation files.

## Test Results

| # | Test | Result | Details |
|---|------|--------|---------|
| 1 | First Load | PASS | With no query parameters, `state.lang` remains its initialized default, `zh-CN` (`docs/index.html:485-489`); `restoreFromURL()` does not explicitly assign the default when `lang` is absent (`717-727`). `getDataSources()` selects `./registry.json` first (`476-483`). Runtime request: `/registry.json`. The page displayed the Chinese title `AI 协作阴性结果登记册`, Chinese controls and entries, with 22 entries, 10 domains, and 4 categories. |
| 2 | zh-CN → en | FAIL | The code path is correct: `setLanguage("en")` changes `state.lang`, applies English UI text, clears `openIds`, and starts `load()` (`631-637`). The first data URL is `./registry-en.json`; after success, `applyFilters()` calls `updateURL()`, producing `?lang=en`. Titles, hypotheses, methods, expected results, and actual results changed to English. However, many secondary detail fields remained Simplified Chinese, so entry details are not fully English. See Bug 2. |
| 3 | en → zh-Hant | FAIL | The switch fetched `./registry-zh-Hant.json`, updated the UI and dropdown labels to Traditional Chinese, and produced `?lang=zh-Hant`. Primary fields changed to Traditional Chinese, but many secondary fields were copied unchanged from the Simplified Chinese registry, yielding mixed Simplified/Traditional entry details. See Bug 2. |
| 4 | Back to Default | PASS | `getDataSources()` special-cases `DEFAULT_LANG`, so returning to `zh-CN` loads `registry.json`, not a nonexistent `registry-zh-CN.json` (`476-483`). On successful rendering, `updateURL()` omits the default language (`706-715`), removing the `lang` parameter. Existing hash state is preserved, as designed. |
| 5 | URL Restoration | PASS | Startup order is `restoreFromURL()` → `applyLanguage(false)` → `load()` (`917-919`), so `?lang=en&domain=prompt-engineering&sort=date-desc` selects English before the fetch. Runtime confirmed `/registry-en.json`, English UI/data, domain `prompt-engineering`, sort `date-desc`, and 2 matching entries. Note: contrary to the checklist's proposed trace, `initializeRegistry()` does **not** call `restoreFromURL()`; it uses state restored once at startup. |
| 6 | Filter Preservation Across Language Switch | PASS | `setLanguage()` does not clear `search`, `domain`, `category`, `tag`, or `sort`; it only clears `openIds`. Therefore `category=null-result` remains in memory while the translated registry reloads. Runtime confirmed 3 matches before and after the en → zh-Hant switch and URL `?category=null-result&lang=zh-Hant`. Preservation does not depend on a second `restoreFromURL()` call. |
| 7 | Hash Link + Language | PASS | Opening `?lang=en#NRR-2026-001` loaded the English registry and then called `openEntryFromHash(true)` from `initializeRegistry()` (`652-667`, `848-863`). The entry had class `open`, its details were not hidden, and its title was English. |
| 8 | Double-Switch Race Condition | FAIL | A delayed English request followed by a completed Traditional Chinese request reproduced a stale-response overwrite. Before releasing English: `state.lang=zh-Hant` and the entry was Traditional Chinese. After releasing English: `state.lang` and the header stayed Traditional Chinese, but `state.registry`/entries became English. There is no request generation check or abort controller in `load()`/`fetchRegistry()` (`638-650`, `877-883`). See Bug 1. |
| 9 | Missing Translation File | PASS | Failing all three `registry-zh-Hant.json` candidate requests caused `fetchRegistry()` to exhaust its sources and `showLoadError()` to render a localized Traditional Chinese error (`638-650`, `871-883`). The page showed `無法載入登記冊` and a `重新載入` button. After failures were removed, Retry successfully loaded Traditional Chinese data. A separate URL-sync defect occurs while the load remains failed; see Bug 3. |
| 10 | Sort + Language Interaction | PASS | Selecting `repro` wrote `?sort=repro`. The language switch preserved `state.sort`; after English reloaded, the same reproducibility order remained (`NRR-2026-018`, `013`, `005` first, all fully reproducible), and the URL became `?sort=repro&lang=en`. `initializeRegistry()` first establishes the base ID order, then `applyFilters()` applies the retained sort (`652-665`, `728-756`). |

## Edge-Case Results

- **Search across languages:** `state.search` is preserved and rerun against the newly loaded registry. A Simplified Chinese query, `代码审查`, returned 2 Chinese entries and 1 English entry. The remaining English match is caused by untranslated Chinese secondary content in `registry-en.json`, not by cross-language search support. Once translation is complete, a language-specific query may legitimately return zero; consider whether search should be cleared or explicitly retained on language switch.
- **Tag preservation:** Tags are unchanged data values across all three files. `tag=prompt-tdd` remained active across zh-CN → en → zh-Hant, consistently returning 2 entries. The tag cloud re-rendered and retained the active button.
- **Tag-cloud refresh:** `initializeRegistry()` calls `renderTagCloud()` for every successful load (`652-665`). Runtime confirmed a fresh cloud with 15 visible data-tag buttons in each language.
- **Dropdown localization:** Domain and category option labels were regenerated using the current locale. Examples changed from `全部领域` / `方法失败` to `All domains` / `Methodology Failure`, then to `全部領域` / `方法失敗`.
- **Old entry DOM nodes:** Successful loads call `renderEntries()`, which replaces the entry markup, so normal language switches do not leave old entry nodes behind. The stale-request race can nevertheless replace the correct translated entries with data from an earlier request.

## Bugs Found

### 🔴 Bug 1: Concurrent language loads can overwrite the selected language's data
**File:** `docs/index.html:631-650`, `docs/index.html:877-883`

**Problem:** Every language click starts an independent asynchronous `load()`. `fetchRegistry()` captures the source list for the language at call time, but `load()` unconditionally passes whichever response finishes last to `initializeRegistry()`. It does not verify that the response still belongs to `state.lang` or to the newest load operation.

**Reproduction:** Delay `registry-en.json`; click English; immediately click Traditional Chinese; allow Traditional Chinese to finish; then release English. The page ends with a Traditional Chinese header and URL but English entry titles/content. A late failure can similarly replace a newer successful view with an error state.

**Fix:** Add cancellation and/or a monotonically increasing load generation. Capture the requested locale in `load()`, pass it into `getDataSources()`/`fetchRegistry()`, and call `initializeRegistry()` or `showLoadError()` only if both the generation and locale still match the latest request. An `AbortController` should abort the preceding fetch sequence when a new language is selected.

### 🟡 Bug 2: Translation registries contain mixed-language entry details
**File:** `docs/registry-en.json:23-67` and corresponding fields throughout the file; `docs/registry-zh-Hant.json:23-67` and corresponding fields throughout the file

**Problem:** Primary fields (`title`, `hypothesis`, `method`, `expected_result`, `actual_result`) are translated for all 22 entries, but several rendered detail fields are unchanged from `registry.json`:

- English file: all 22 `sample_size`, `interpretation`, `reproducibility.notes`, `related_positive_result`, and link-label sets remain identical to Simplified Chinese; 11/22 `lessons_learned` sets also remain unchanged. Most `effect_size` values are language-bearing Chinese strings as well.
- Traditional Chinese file: the same field groups remain identical to the Simplified Chinese source; 11/22 `lessons_learned` sets are unchanged, producing Simplified Chinese inside a Traditional Chinese page.
- Tags are intentionally stable and are not counted as a defect.

**User impact:** Expanded entries visibly mix languages. In English, for example, NRR-2026-001 shows English hypothesis/method text followed by Chinese sample size, interpretation, reproducibility notes, related result, tags, and link labels. This also contaminates search results: a Chinese query can match the nominally English registry.

**Fix:** Translate every user-visible free-text field, including nested `reproducibility.notes`, array items in `lessons_learned`, and `links[].label`. Add a data-generation validation test that enumerates rendered translatable fields. For English, flag unexpected CJK text with a small allowlist; for Traditional Chinese, validate that copied Simplified text is explicitly reviewed or converted.

### 🟡 Bug 3: The selected language is not written to the URL until data loading succeeds
**File:** `docs/index.html:631-637`, `docs/index.html:706-715`, `docs/index.html:877-883`

**Problem:** `setLanguage()` calls `applyLanguage(false)`, explicitly suppressing URL synchronization. The URL is updated later only through `initializeRegistry()` → `applyFilters()` → `updateURL()`. If all translation fetches fail, that path is never reached.

**Reproduction:** Start on the default URL, fail all three Traditional Chinese data sources, and click `正體中文`. The UI and error message become Traditional Chinese (`state.lang=zh-Hant`), but the URL remains `/index.html` without `?lang=zh-Hant`. Refreshing therefore returns to Simplified Chinese.

**Fix:** Synchronize the URL immediately when accepting a language change, before awaiting data. Preserve the current query/filter/sort/hash parameters. The later successful render can safely normalize the same URL again.

## Race Condition Analysis

There is a confirmed last-response-wins race:

1. `setLanguage("en")` sets the global locale to English and starts load A.
2. Before A finishes, `setLanguage("zh-Hant")` sets the global locale to Traditional Chinese and starts load B.
3. B finishes first and correctly installs Traditional Chinese data.
4. A finishes later and unconditionally calls `initializeRegistry(englishRegistry)`.
5. `initializeRegistry()` renders the English registry while all localization lookups use the current global `state.lang`, which is still `zh-Hant`.

The resulting state is internally inconsistent: Traditional Chinese document language, header, labels, active switcher, and URL; English registry entries. Because both success and error paths are unguarded, an obsolete request may overwrite the newest success with either stale data or a stale error.

Recommended invariant: only the most recently requested language load may mutate `state.registry`, `state.entries`, `state.status`, or the rendered load-error state.

## Overall Verdict

**FAIL — 7 checklist tests passed and 3 failed.**

The default load, URL restoration, enum-filter preservation, hash opening, missing-file error/retry behavior, default-language return, and sort preservation work. However, the language feature is not release-safe yet: rapid switching can produce a mixed UI/data state, and both translated registries contain substantial untranslated entry details. URL synchronization also becomes inconsistent when a language data load fails.