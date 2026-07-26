Model: GPT-5.6-Sol (Codex)

# UX Review: Negative Results Registry
Reviewer: GPT-5.6-Sol (via Codex CLI) · 2026-07-26

## Page 1: GitHub Repository
### Above the Fold

**Five-second answer: mostly yes, but with a damaging contradiction.** The repository name and About description quickly communicate the core idea: this is a structured, searchable registry of failed or negative AI-collaboration experiments. The topics reinforce “negative results,” “open science,” “reproducibility,” and “AI collaboration.” A stranger does not have to reverse-engineer the purpose from the file tree.

However, the live GitHub About description still says **18 entries × 8 domains × 7 types**, while the README and Pages site say **22 entries × 10 domains × 4 represented types**. That discrepancy is visible before the visitor has formed an opinion. For a project whose product is careful evidence and structured metadata, stale metadata is not a cosmetic mistake; it weakens the central promise.

The rest of the first screen is recognizably a GitHub repository: repository controls, topics, a file list, and—depending on viewport height—the beginning of the README. The README opening is strong: a clear title, one-sentence definition, license/CI/entry badges, language links, and an “在线浏览” link. But the language badge row is immediately repeated as a text language row, and the browse link is buried inside a slogan rather than presented as the primary action.

For a Chinese-speaking technical visitor, the project is understandable quickly. For an English-speaking stranger, the repository advertises bilingual support but still makes them locate and select English before they can understand the substance.

### Credibility Signals

**Signals that build trust:**

- The project is unusually candid that it is currently a **single-maintainer prototype**, not yet a community registry. That disclosure is more credible than pretending that 22 entries constitute a movement.
- CI, a clear CC BY 4.0 license, a JSON Schema, machine-readable `registry.json`, contribution templates, methodology documentation, and paired Markdown/JSON records all suggest that the maintainer has thought beyond a one-off README.
- Entries expose hypothesis, method, expected versus actual result, sample size, effect size, reproducibility, lessons, and source links. That is materially better than a vague collection of “things that did not work.”
- The README includes known limitations and distinguishes third-party source analysis from independent registry contributors. This is good epistemic hygiene.

**Signals that erode trust:**

- As of July 26, 2026, the public repository is approximately one day old and shows **0 stars, 0 forks, and 0 watchers**, with no releases. This is not a defect, but it means there is no social proof to offset the single-maintainer limitation.
- All 22 entries have the same submitter. The project therefore demonstrates a schema and a personal evidence log, not yet a registry with independent adoption.
- The stale About counts conflict with the current dataset. Again, this is especially serious for a registry.
- The README says the submission contract is not finalized, including ID assignment, evidence thresholds, and review SLA. Inviting contributions before the acceptance contract is settled creates uncertainty for the first real contributor.
- The “Entries” badge and the Chinese language badge use empty links. They look clickable but do not lead anywhere. That is a small but visible quality-control miss.
- Claims about the scale of GitHub’s AI ecosystem and the project’s experience density are persuasive copy, but they read as self-asserted unless citations and provenance are close at hand.
- The repository admits that link checking skips GitHub and arXiv under rate limits. A registry whose value depends on traceability needs a more visible indication of which evidence links were actually verified and when.

My trust level would be: **promising prototype, not yet trusted community infrastructure**. The honesty helps substantially; the inconsistent metadata and lack of independent contributions hold it back.

### Navigation & Findability

**(a) What is this? — Easy.** The About description, README title, definition, and “这是什么” section answer this well.

**(b) How do I submit? — Findable, but not fast enough.** `CONTRIBUTING.md` is visible in the file list, and the README eventually explains the process. A motivated GitHub user can find it. A first-time visitor should not need to scan the file list, scroll through taxonomy, or search the page for “提交.” Put a prominent **Submit a negative result** link beside **Browse the registry** near the top. Also resolve the submission-contract ambiguity before treating submission as a primary CTA.

**(c) What is already in it? — Technically easy, visually underemphasized.** The online browser link appears near the top, `registry.json` is visible, and a 22-row overview table exists later in the README. But the most useful destination—the interactive browser—looks like a secondary inline link. It should be a button-style primary action, with a short preview such as “Browse 22 reports across 10 domains.”

The README’s long taxonomy and project rationale are useful reference material, but they delay task-oriented navigation. A stranger needs a compact route map near the top: **Browse · Submit · Methodology · Data/API**.

### Visual Polish

The presentation is more professional than the average new open-source data repository, but not fully polished.

- **Badges:** Standard and legible, but there are too many language indicators because badges and text links repeat one another. Empty badge links make the row feel unfinished. Keep one language control, make every badge purposeful, and make the entry badge link to the browser or entry table.
- **Mermaid diagram:** It communicates the lifecycle and gives the repository a systems-oriented feel. However, emoji, bold HTML, multiline labels, and several actors make it visually busy. It is useful documentation, not a strong hero graphic. A simpler three- or four-step flow would scan faster.
- **Tables:** The taxonomy tables look disciplined, but the large entry overview becomes dense and spreadsheet-like. It proves that content exists, yet it is a poor browsing experience compared with the Pages site. Show a compact sample or summary in the README and let the browser own the full catalog.
- **Tone and typography:** The mixed Chinese/English phrase “知道什么不 work…” is memorable and human, but slightly informal beside the project’s methodological framing. That is acceptable if treated as a deliberate tagline, not repeated as technical terminology.

The biggest visual problem is not styling; it is **information hierarchy**. The README treats rationale, taxonomy, contribution, inventory, and governance as nearly equal. A newcomer needs the value proposition and two actions first, with everything else progressively disclosed.

## Page 2: GitHub Pages
### First-Load Experience

The first load is not a blank screen: the hero title, subtitle, three statistic placeholders, filters, and page structure render immediately. That is good. The loading panel is also honest and has a retry path on failure.

However, **“正在读取 registry.json” is implementation language, not visitor language**. A stranger does not care which file is being fetched. “正在加载 22 条阴性结果…” would be clearer and would preserve context. A lightweight skeleton of two or three entry cards would feel more intentional than a large dashed loading box.

There is also a concrete deployment weakness: the page tries three data URLs sequentially. On the deployed Pages site, `./registry.json` and `../registry.json` return 404, so the application depends on the third fallback—the raw GitHub URL. This creates two avoidable failed requests before the real download and makes the site dependent on another GitHub endpoint. If raw content is blocked, rate-limited, or slow, the registry appears broken even though the HTML loaded correctly. Copy or generate `registry.json` into the deployed `docs/` output and make the same-origin URL the successful first request.

The failure message tells users to open the page through a local HTTP server, which is appropriate for a developer opening `index.html` from disk but confusing on the public website. Public-site errors should say that the data could not be loaded, provide Retry, and link to the GitHub data file or issue tracker.

Finally, the first-load UI is Chinese-only despite the repository advertising English and Traditional Chinese versions. That makes the Pages site feel narrower than the repository it represents.

### Information Architecture

The core browsing model is understandable:

- keyword search;
- domain and category filters;
- live result count and reset;
- clickable tags;
- collapsed entry summaries that expand into structured evidence.

The cards contain the right information. Their summary line—ID, title, domain/date/submitter, and category—supports scanning, while expansion avoids placing every method and result on the page at once. Direct links to individual entries through URL hashes are also valuable.

The weak point is the **tag cloud**. The current dataset contains **142 unique tags for only 22 entries**, and most tags occur once. Rendering all of them before the entry list creates a wall of pills, makes frequency-based font sizing mostly decorative, and pushes the actual evidence far down the page. On mobile it can become several screens of low-signal navigation. Show perhaps the 8–12 most-used tags, add “Show all tags,” or replace the cloud with an autocomplete/tag filter.

Other IA gaps:

- There is no sort control for newest, domain, evidence strength, sample size, or reproducibility.
- Filter state is not encoded in the URL, so a visitor cannot share a useful view such as “all multi-model null results.”
- The site says “4 types,” while the taxonomy supports more types. Label this **“4 represented types”** to avoid implying that the registry’s ontology has only four categories.
- There is no “start here” or featured-entry path. A new visitor sees 22 equal cards and must choose randomly.
- There is no compact evidence/provenance indicator on collapsed cards. A card sourced from a controlled experiment and a card based on a smaller observational review can look equally authoritative until opened.

The browser is functional, but it behaves like a dataset explorer built for someone who already understands the registry. A newcomer layer is still missing.

### Visual Design Quality

**Professionalism: 7/10. Readability: 8/10. Consistency: 7/10.**

The site is surprisingly polished for a single-file, dependency-free page. The off-white grid background, dark green accent, restrained shadows, consistent radii, serif headings, and sans-serif body create a coherent visual system. The filter panel and cards have clear boundaries without looking like a generic admin dashboard. Focus-visible outlines, semantic labels, `aria-live`, reduced-motion support, and a print stylesheet show care beyond surface styling.

What keeps it from looking fully professional:

- The 142-tag cloud overwhelms the otherwise calm design.
- The hero is attractive but has no navigation or CTA, so it reads like a poster above a database rather than the front door of a project.
- Category colors are useful, but eight palettes are defined while only four categories currently appear. The system is more complex than the visible data requires.
- Mixed Georgia and platform-dependent Chinese serif fallbacks may render unevenly across Windows, macOS, Android, and iOS. A tested CJK font stack or bundled variable font would improve consistency, though bundling a font would trade away the page’s dependency-free simplicity.
- The footer credit **“页面生成：GPT-5.6-Sol”** is likely to raise the wrong question: “Was the evidence generated by AI too?” Even if it refers only to the HTML, the distinction is not obvious. Put implementation credit in the repository or an About page; use the public footer for data version, last update, license, provenance policy, and contribution links.
- There is no visible brand mark, favicon, or shared navigation connecting About, Browse, Submit, and Methodology. The page looks designed, but not yet like a complete product surface.
- Hardcoded light mode is not a serious defect, but a system dark theme would be a reasonable later refinement.

The design should not become more decorative. It needs less visual noise, clearer hierarchy, and stronger trust information.

### Mobile & Responsive

The responsive foundation is sensible. At 760px, filters and detail blocks become one column; entry headers simplify; category badges move below the title; detail padding tightens. Inputs have a 44px minimum height, which is appropriate for touch. At 480px, outer margins and card padding shrink without collapsing the layout.

Likely mobile issues remain:

- The three statistic cards stay in one row even below 480px. Bilingual labels can wrap awkwardly, producing cramped or uneven cards. A 2+1 layout or horizontal scroll is not desirable; a stacked compact summary or three smaller inline metrics would be cleaner.
- The full tag cloud is the dominant mobile problem. It can force users through multiple screens before the first entry.
- Long Chinese/English titles, IDs, metadata, and badges will make some collapsed cards very tall. The design can handle this, but scanning 22 items becomes tiring.
- Expanded entries become extremely long single-column documents. There is no sticky collapse action, “back to results,” or persistent filter summary.
- The filter panel stacks correctly, but after selecting a tag or filter there is no shortcut that moves the user to results.
- The footer’s wrapped links and generation credit may become a dense final block.

I would expect the site to remain usable on mobile, but not efficient. The CSS prevents obvious breakage; it does not yet optimize the browsing journey for a small screen.

## Cross-Page Consistency

Conceptually, the pages belong together: the same Chinese project name, same central slogan, same dataset, same terminology, same license, and direct links between repository and browser. The Pages site’s restrained green/open-evidence visual language fits the registry’s serious tone.

Operationally, they feel partially disconnected:

- GitHub’s About description reports 18/8/7 while the browser reports 22/10/4.
- The repository offers three language paths; the browser offers only Chinese.
- The repository explains submission and methodology; the browser hides GitHub until the footer and offers no submission route.
- The browser foregrounds an AI generation credit that the repository does not contextualize.
- The repo-to-site link is inline text, while the site-to-repo link is a footer link. Neither page has a shared top-level navigation model.

The Pages site currently feels like a well-styled viewer attached to the repository, not yet a unified second surface of the same product. A shared header vocabulary—**About · Browse · Submit · Methodology · GitHub · Language**—would close much of that gap.

## Call to Action Clarity

The project does not make one action unmistakably primary.

On GitHub, I can infer several possibilities: browse the online registry, inspect `registry.json`, submit an entry, read the methodology, or fork the project. On the Pages site, the implied action is “browse,” but there is no explicit invitation, guided first step, featured entry, or submission link. After expanding a card, the next action is usually to collapse it or leave.

The project should define a simple visitor funnel:

1. **Primary:** Browse the evidence.
2. **Secondary:** Submit a documented negative result.
3. **Trust path:** Read the methodology and provenance policy.
4. **Technical path:** Access the JSON/schema or fork the project.

Place those actions near the top of both pages. Do not make “Fork” a primary CTA for ordinary visitors; that is a maintainer/developer action, not the natural next step for someone discovering the idea.

## Top 3 Improvements

1. **Fix the trust-breaking inconsistencies and deployment path — why:** Update or remove volatile counts in the GitHub About description; ensure all displayed metrics come from one generated source; deploy `registry.json` with the Pages site so the first request succeeds; show a clear data version and last-verified date. This immediately improves credibility and first-load reliability. **Estimated effort: 2–4 hours**, plus a small CI update.
2. **Create one newcomer funnel across both pages — why:** Put three prominent links at the top of the README and site: **Browse 22 results**, **Submit a result**, and **How evidence is reviewed**. Add shared navigation and a language selector to Pages, and finalize the minimum submission contract before strongly soliciting contributions. This turns an interesting artifact into a comprehensible project. **Estimated effort: 1–2 days.**
3. **Replace the full tag cloud with progressive disclosure and shareable browsing — why:** Show only top tags by default, provide an expandable/all-tags control or autocomplete, add sorting and URL-synchronized filters, and expose a compact provenance/evidence indicator on each collapsed card. This reduces noise, improves mobile use, and makes filtered discoveries shareable. **Estimated effort: 1–3 days.**

## Overall Verdict

A stranger interested in AI evaluation or open science might bookmark this because the core idea is memorable: **a searchable ledger of AI-collaboration approaches that did not work, with enough structure to learn from them**. The Pages design is better than the project’s current maturity level, and the README’s candor is its strongest credibility asset. Most general visitors, however, will still treat it as a thoughtful personal prototype rather than a trusted registry because the public metadata disagrees, all entries come from one maintainer, the submission contract is unfinished, and neither page clearly tells them what to do next. The one thing they will remember is the premise; the next iteration must make the evidence pipeline and participation path equally memorable.