# PLAN-011: Token-Efficient Lesson Generation (Tier 1 + Tier 2)

**Created:** 2026-05-14
**Status:** In-Progress
**Addresses:** Lesson generation currently loads ~62k input tokens (monolithic `LESSON_DESIGN_v2.md` + four golden lessons + CSS + JS) and emits ~14k output tokens per turn, with 2–3 revision rounds totalling ~200k–225k tokens per lesson. This plan reduces per-lesson cost by ≥90% via two mechanisms: (1) a modular, load-on-demand `LESSON_DESIGN` directory, and (2) a structured-spec → deterministic-render pipeline.

---

## 1. Context & motivation

The prior cost audit (this session, 2026-05-14) measured the per-turn input as:

| Artifact | Bytes | ~Tokens |
|---|---|---|
| `lessons/LESSON_DESIGN_v2.md` | 18 KB | 4,600 |
| `lessons/3sum/lesson.html` | 45 KB | 11,300 |
| `lessons/permutation-in-string/lesson.html` | 65 KB | 16,400 |
| `lessons/trapping-rain-water/lesson.html` | 46 KB | 11,400 |
| `lessons/median-of-two-sorted-arrays/lesson.html` | 54 KB | 13,600 |
| `static/lesson.css` | 19 KB | 4,800 |
| `static/lesson.js` | 2.5 KB | 620 |
| **Total** | **250 KB** | **≈62,000** |

Two structural problems drive the cost:

1. **Monolithic design doc.** `LESSON_DESIGN_v2.md` mixes section-specific principles (e.g. dry-run priming, code-visualization dimming) with global rules (layout, shared assets). All 28 principles load whether or not the current work touches them.
2. **Whole-file goldens as reference.** A model writing the Step 7 "Dry run" section does not need the 800 lines of brute-force, code-visualization, and corner-case markup from `3sum/lesson.html` — but the file is loaded whole because there is no per-section excerpt.

The companion design change in [LESSON_DESIGN_v2.md](../../../lessons/LESSON_DESIGN_v2.md) ("Shared assets") already exists, established by PLAN-010, but the document itself is still monolithic and full lesson HTMLs are still fed as references.

This plan addresses **Tier 1 (reduce input load)** and **Tier 2 (restructure output)** from the in-session efficiency analysis. Tier 3 (mixed-model strategy) and Tier 4 (hygiene) are deferred to a future plan.

## 2. Goals

- A new `lessons/design/` directory exists, containing one Markdown file per lesson section plus three cross-cutting files (`layout.md`, `python_verify.md`, `known_bugs.md`).
- `lessons/LESSON_DESIGN.md` is rewritten as a lean **index** (≤ 800 tokens) containing only: shared-assets rule, mandatory section order, reader assumption, and a **load-on-demand table** mapping each lesson section to the design files that must be loaded when authoring it.
- The index explicitly instructs: *"Do not load any file under `lessons/design/` by default. Load only the rows of the table that match the section currently being authored."*
- `lessons/_template.html` exists: an ~8 KB skeleton with all 12 sections present, each containing class names and `<!-- PER-PROBLEM: ... -->` placeholders, derived from `lessons/3sum/lesson.html`.
- `static/CLASSES.md` exists: a flat class-vocabulary index (≤ 60 lines) replacing the need to feed `static/lesson.css` into generation prompts.
- `lessons/design/archetypes.md` maps problem archetypes (two-pointer, sliding-window, prefix-scan, divide-conquer) to a single canonical golden, so the generator loads **one** golden per problem instead of four.
- `lessons/design/spec_schema.json` defines a JSON schema for a **lesson spec** containing every per-problem variable (kernel, foundational concept, brute force, translations, algorithm steps, code, examples, dry-run traces, edge cases, approaches, take-home).
- `scripts/render_lesson.py` reads a spec + `_template.html` + per-section partial templates under `lessons/design/partials/` and emits a complete `lesson.html`. No LLM call inside the renderer.
- `scripts/verify_algorithm.py` reads a spec's `code` and `examples` fields, runs a Python equivalent, asserts expected output, and refuses to render if the trace fails. Mandatory pre-render gate.
- `scripts/new_lesson.py` scaffolds a `lessons/<slug>/` directory with `plan.md` stub, copied template, and pre-wired imports.
- After implementation, generating one complete lesson end-to-end consumes ≤ 25k tokens (input + output combined) under prompt caching, verified by an instrumented dry run on a fresh problem.
- The existing four golden lessons re-render byte-equivalent (or accepted-diff-equivalent) from extracted specs, proving the renderer is lossless.

## 3. Non-goals

- Mixed-model orchestration (Haiku for mechanical sections, Sonnet for creative). Deferred.
- Parallel subagent generation infrastructure. The spec/render substrate built here enables it, but wiring agents is a separate plan.
- Modifying any of the four golden lessons' final HTML output beyond what is needed to extract a spec.
- Replacing `lessons/LESSON_DESIGN_v2.md`. v2 stays as historical reference and is what `LESSON_DESIGN.md` is rewritten *from*. No content is lost — content is partitioned.
- A web UI for spec editing. Specs are JSON edited in any editor.
- Caching infrastructure for the Claude API itself. This plan produces cache-friendly inputs; the actual `cache_control` wiring lives in whatever generation script the user runs.

## 4. Approach

### 4.1 Modular `LESSON_DESIGN` split

`lessons/LESSON_DESIGN_v2.md` currently bundles 28 principles. They partition cleanly by lesson section:

| Section in lesson | Principles in v2 | New file |
|---|---|---|
| 0. Clarifying questions | 4 | `lessons/design/sec0_clarifying.md` |
| 1. The Insight (kernel + foundational visual + equivalence chain) | 1, 2, 3, 7 | `lessons/design/sec1_insight.md` |
| 2. Brute force | 9, 10, 13 | `lessons/design/sec2_brute_force.md` |
| 3. Translations | 5, 6 | `lessons/design/sec3_translations.md` |
| 4. Algorithm in plain English | 8, 18 | `lessons/design/sec4_algorithm_english.md` |
| 5. Code reveal | 13, 25 | `lessons/design/sec5_code.md` |
| 6. Code visualization | 14, 15, 16, 17 | `lessons/design/sec6_code_viz.md` |
| 7. Dry run | 11, 12, 19, 20, 28 | `lessons/design/sec7_dry_run.md` |
| 8. Production readiness | 21 | `lessons/design/sec8_production.md` |
| 9. Approaches tab | — | `lessons/design/sec9_approaches.md` |
| 10. Complexity | — | `lessons/design/sec10_complexity.md` |
| 11. Take home | 27 | `lessons/design/sec11_take_home.md` |
| (cross-cutting) Layout & keyboard | 22, 23, 24 | `lessons/design/layout.md` |
| (cross-cutting) Code style | 25 | `lessons/design/code_style.md` |
| (cross-cutting) Algorithm verification | 26 | `lessons/design/python_verify.md` |
| (cross-cutting) Known bugs | diff inversion, CV scrollbar, etc. | `lessons/design/known_bugs.md` |

`lessons/LESSON_DESIGN.md` is rewritten as the only file loaded by default. Its body is:

```markdown
# Lesson Design Index

> Load this file by default. Load anything else under `lessons/design/`
> ONLY when the row in the table below applies to the section you are
> currently authoring. Do not preload.

## Always true
- Shared CSS/JS: `static/lesson.css`, `static/lesson.js`. Do not regenerate.
- Mandatory section order: 0..11 (see table).
- Reader assumption: they have failed at this problem and want the insight, not array basics.

## Section index — load on demand

| Section | Title | Load these when authoring |
|---------|-------|---------------------------|
| 0 | Before you code | `design/sec0_clarifying.md` |
| 1 | The Insight | `design/sec1_insight.md` + `design/known_bugs.md` |
| 2 | Brute force | `design/sec2_brute_force.md` |
| ... | ... | ... |

## Before any HTML is written
Always load `design/python_verify.md` and run the verifier.

## Layout / keyboard / code style
Load `design/layout.md` and `design/code_style.md` once per lesson, after the spec is approved and before rendering.
```

The directive language ("Load ... ONLY when ...") is interpreted by both human authors and AI agents. AI agents following this index pull only the matching rows into context.

### 4.2 Per-section golden excerpts

Each `lessons/design/sec<N>_*.md` file ends with a **Reference excerpts** block linking to the line range of the canonical golden's matching section:

```markdown
## Reference excerpts
- Two-pointer archetype: `lessons/3sum/lesson.html:120-185` (Step 2 brute force markup + JS)
- Sliding-window archetype: `lessons/permutation-in-string/lesson.html:240-320`
```

A model loading `sec2_brute_force.md` follows the link for the matching archetype only, fetching ~60 lines (~600 tokens) instead of the full 800-line golden.

`lessons/design/archetypes.md` is the lookup: problem → archetype → canonical golden filename.

### 4.3 Template skeleton

`lessons/_template.html` is created by copying `lessons/3sum/lesson.html` and replacing every per-problem block with a comment marker:

```html
<!-- ═══ SECTION 0: CLARIFYING QUESTIONS ═══ -->
<div class="section" style="padding-top:.5rem">
  <p class="sec-label">Before you code</p>
  <p class="sec-title">{{TITLE_SEC0}}</p>
  <!-- PER-PROBLEM: 4 .acard blocks (Q / A / unlock line) -->
  <!-- PER-PROBLEM: optional .infobox "Assumptions we carry forward" -->
</div>
```

The skeleton preserves every class name, container, and section delimiter — i.e., everything the model would otherwise reinvent. Output by the LLM is reduced to the per-problem inserts only.

### 4.4 Class vocabulary index

`static/CLASSES.md` is a flat list:

```markdown
# CSS class vocabulary

## Section frames
- `.section` — outer container, 1.25rem padding
- `.sec-label` — eyebrow text above section title
- `.sec-title` — h2-equivalent
- `.body` — paragraph

## Clarifying cards
- `.asgrid` — grid container for `.acard`
- `.acard` — single Q/A/unlock card
- `.acard-q`, `.acard-a`, `.acard-u`

## Visualizations
- `.number-line`, `.nl-wrap`, `.nl-num`, `.nl-label` — sorted-array pointer visual
- `.bf-num`, `.bi`, `.bj`, `.bk`, `.bmatch` — brute-force cells
- ...
```

Generation prompts feed this (~1k tokens) instead of `static/lesson.css` (~4.8k tokens).

### 4.5 Lesson spec schema

`lessons/design/spec_schema.json` defines (informally — JSON Schema draft-07):

```json
{
  "slug": "3sum",
  "title": "3Sum",
  "lc_id": 15,
  "difficulty": "Medium",
  "tags": ["Arrays", "Two Pointers"],
  "archetype": "two_pointer",
  "clarifying": [{"q": "...", "a": "...", "unlocks": "..."}, ...],
  "insight": {
    "kernel": "Sort. Fix one. Two pointers inward.",
    "kernel_paragraph": "...",
    "foundational_visual": { "type": "number_line", "data": {...} },
    "equivalence_chain": [{"text": "...", "pills": [...]}]
  },
  "brute_force": {
    "code": "...",
    "complexity": "O(n^3)",
    "examples": [[-1,0,1,2,-1,-4], [0,0,0,0]],
    "counter_label": "Checks"
  },
  "translations": [{"name": "...", "description": "...", "gain": "..."}],
  "algorithm_english": ["1. Sort.", "2. For each i...", ...],
  "code": {
    "language": "cpp",
    "lines": [{"n": 1, "c": "..."}, ...],
    "variables": [{"name": "n", "appears_on_line": 4}, ...]
  },
  "examples": [{"name": "fast", "input": [...], "trace_steps": [...]}, ...],
  "edge_cases": [{"label": "...", "explanation": "..."}],
  "approaches": [{"name": "...", "code": "...", "complexity": "..."}],
  "complexity": {"time": "O(n^2)", "space": "O(1)"},
  "take_home": [{"problem": "LC 16 — 3Sum Closest", "differs_by": "..."}]
}
```

The LLM's job becomes filling this spec. Output is ~2k–3k tokens vs ~14k tokens of HTML.

### 4.6 Renderer

`scripts/render_lesson.py`:

```python
def render(spec_path: Path, out_path: Path) -> None:
    spec = json.loads(spec_path.read_text())
    template = (LESSONS / "_template.html").read_text()
    partials = load_partials(LESSONS / "design" / "partials")
    html = render_template(template, partials, spec)
    out_path.write_text(html)
```

Partials live in `lessons/design/partials/sec0_clarifying.html.tmpl`, etc. They are Jinja2-style fragments that consume the matching spec branch. The renderer is deterministic, fast (< 100 ms), and re-runnable.

The renderer also generates the per-problem inline `<script>` block — the `EXAMPLES`, `BF_EXAMPLES`, `CV_LINES`, and the `cvGen`/`drGen`/`bfGen` step generators — from the spec's `examples` and `code` fields. Step generators are produced from a small per-archetype JS template under `lessons/design/partials/js/<archetype>.js.tmpl`. (For algorithms outside the four archetypes, the spec may include a `custom_step_generator_js` field that the renderer interpolates verbatim — this is the escape hatch.)

### 4.7 Python algorithm verifier

`scripts/verify_algorithm.py` reads `code.language` + `code.lines` from the spec. For each `examples[i]`, it runs a Python equivalent of the algorithm (translated by the spec author or via a separate Python field `code.python`) against the input, then compares to expected output. If any example fails, `render_lesson.py` refuses to write output. This implements principle #26 (`design/python_verify.md`) as a hard gate.

### 4.8 End-to-end workflow

For a new problem:

```
1. scripts/new_lesson.py <slug>     # creates lessons/<slug>/{plan.md, spec.json stub}
2. (LLM, with cached prefix)         # fills plan.md
3. (human review of plan.md)         # cheap text review
4. (LLM, with cached prefix)         # fills spec.json from approved plan.md
5. scripts/verify_algorithm.py spec.json   # gate
6. scripts/render_lesson.py spec.json lessons/<slug>/lesson.html
```

Step 2 and 4 are the only LLM-calling steps. Both load only `LESSON_DESIGN.md` (index) plus whichever `design/sec*.md` files match the current section — typically 2–4 files totalling ~2k tokens, plus the per-archetype golden excerpt (~1k tokens). With prompt caching the per-lesson marginal input cost is ~3k tokens read at 0.1× rate.

### 4.9 Migration of existing lessons (proof of losslessness)

Extract a spec from each of the four golden lessons. Run the renderer. Diff the output against the original. Resolve diffs by either tweaking the template/partials or — where the original has a legitimate one-off — adding an `overrides` field to the spec for surgical insertion. Goal: the renderer can recreate every existing golden.

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Write tests: `tests/test_render_lesson.py` asserting that rendering an extracted 3sum spec produces HTML byte-equivalent to (or accepted-diff against) `lessons/3sum/lesson.html`. | 1.5 hr | — |
| 2 | Create `lessons/design/` dir; split `LESSON_DESIGN_v2.md` into `sec0..sec11`, `layout.md`, `code_style.md`, `python_verify.md`, `known_bugs.md` per §4.1 table. Verbatim content move; no rewrites. | 2 hr | — |
| 3 | Rewrite `lessons/LESSON_DESIGN.md` as the lean load-on-demand index per §4.1. Include the section→files table and the explicit "do not preload" directive. | 1 hr | 2 |
| 4 | Add **Reference excerpts** blocks to each `design/sec<N>_*.md` linking to specific line ranges in the matching golden. | 1.5 hr | 2 |
| 5 | Create `lessons/design/archetypes.md` (problem → archetype → canonical golden filename + which sections to excerpt). | 30 min | 4 |
| 6 | Create `lessons/_template.html` by stripping per-problem content from `lessons/3sum/lesson.html`. | 1 hr | — |
| 7 | Create `static/CLASSES.md` by extracting class names from `static/lesson.css` with one-line descriptions. | 1 hr | — |
| 8 | Define `lessons/design/spec_schema.json` (JSON Schema draft-07) per §4.5. | 1.5 hr | — |
| 9 | Write per-section partials under `lessons/design/partials/sec*.html.tmpl` using Jinja2 syntax. | 3 hr | 6, 8 |
| 10 | Write per-archetype JS step-generator templates under `lessons/design/partials/js/<archetype>.js.tmpl`. | 2 hr | 8 |
| 11 | Implement `scripts/render_lesson.py` consuming spec + template + partials. | 2 hr | 9, 10 |
| 12 | Extract spec from `lessons/3sum/lesson.html` into `lessons/3sum/spec.json`. Run test from task 1. Iterate template/partials until diff acceptable. | 3 hr | 11 |
| 13 | Repeat task 12 for `permutation-in-string`, `trapping-rain-water`, `median-of-two-sorted-arrays`. | 4 hr | 12 |
| 14 | Implement `scripts/verify_algorithm.py` per §4.7. Add `code.python` field to all four existing specs. Wire as a pre-render gate in `render_lesson.py`. | 2 hr | 11, 12 |
| 15 | Implement `scripts/new_lesson.py` per §4.8. | 1 hr | 6, 8 |
| 16 | Instrument an end-to-end dry run on one new problem (e.g. `two-sum`) and record actual token consumption. Verify ≤ 25k tokens total. | 1.5 hr | 11, 14, 15 |
| 17 | Update `CLAUDE.md` to point at `LESSON_DESIGN.md` (already does) and add a one-liner: "Generation workflow lives in `AGENT_MD/plan/plans/PLAN-011...`." Update [current_state_report.md](../current_state_report.md). | 30 min | 16 |
| 18 | Write `AGENT_MD/plan/reports/REPORT-011_lesson_gen_efficiency.md`. | 1 hr | 16 |

Total: ~30 hr.

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Renderer cannot reproduce a golden lesson byte-equivalent due to one-off styling. | High | Med | Accept a small diff list documented in `REPORT-011`; add `overrides` spec field for legitimate one-offs. Task 12 surfaces this early on the simplest lesson. |
| Per-archetype step-generator JS templates do not cover algorithms outside the four archetypes (e.g. graph BFS). | Med | High | Spec field `custom_step_generator_js` is an escape hatch (§4.6). When > 50% of new lessons use the escape hatch, fold the new archetype into `partials/js/`. |
| LLM ignores "load on demand" directive and pulls every `design/*.md` anyway. | Med | Med | The index file states the rule first-thing. The generation script can also do mechanical context assembly — load only files matching the section spec branch — bypassing model judgment. |
| Spec schema drift: a new lesson needs a field not in the schema. | Med | Low | Schema is versioned (`"spec_version": "1.0"`). Additive fields are non-breaking. Renderer logs warnings on unknown fields rather than failing. |
| Diff-based revisions of an existing lesson still go through the full pipeline. | Low | Low | Spec edits are tiny; `render_lesson.py` is idempotent and re-rendering is < 1s. Diff cost stays low. |
| Test in task 1 is fragile (e.g., whitespace differences) and blocks progress. | Med | Med | Normalize whitespace before diff; allow a tolerated-diffs file listed in the test. |
| The `lessons/design/` directory itself grows large and re-introduces monolithic loading. | Low | Med | Index file caps to 800 tokens; per-section files cap to 800 tokens. Add a CI check in task 16 that fails if any single design file exceeds 800 tokens. |

## 7. Success criteria

- **Goal §2.1–§2.7 met:** all listed files exist with the specified contents.
- **Renderer is lossless:** `python scripts/render_lesson.py <each golden spec>` produces output that diffs cleanly (or with documented accepted diffs) against the original golden lesson HTML.
- **Verifier gates render:** intentionally corrupting a spec's `code.python` causes `render_lesson.py` to refuse and exit non-zero.
- **Token budget met:** end-to-end generation of a new lesson (`two-sum`) using only `LESSON_DESIGN.md` + load-on-demand files + one archetype excerpt consumes ≤ 25k total tokens (input + output, pre-cache). Recorded in REPORT-011.
- **Modular index is sufficient:** an AI agent given only `LESSON_DESIGN.md` can correctly identify which `design/*.md` files to load for any section, verified by spot check on three sections.

## 8. References

- [lessons/LESSON_DESIGN_v2.md](../../../lessons/LESSON_DESIGN_v2.md) — source of all 28 principles to be partitioned.
- [PLAN-010_static_asset_migration.md](PLAN-010_static_asset_migration.md) — the prior cut that moved CSS/JS to `static/`; this plan continues that direction.
- [AGENT_MD/plan/rules.md](../rules.md) — authoring rules followed by this plan.
- [lessons/3sum/lesson.html](../../../lessons/3sum/lesson.html) — primary template source.
- [lessons/3sum/plan.md](../../../lessons/3sum/plan.md) — example of the `plan.md` checkpoint format referenced in §4.8.
- In-session efficiency analysis (this conversation, 2026-05-14) — Tier 1 + Tier 2 origins.
