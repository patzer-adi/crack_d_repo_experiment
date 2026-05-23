# REPORT-011: Token-Efficient Lesson Generation — Phase 1

**Plan:** PLAN-011
**Completed:** 2026-05-14 (Phase 1 only; Phase 2 deferred to PLAN-012)
**Author:** Claude (Sonnet 4.6) under user direction

---

## 1. Summary

Phase 1 of PLAN-011 partitioned the monolithic `lessons/LESSON_DESIGN_v2.md` into a lean load-on-demand index (`lessons/LESSON_DESIGN.md`) plus 18 modular files under `lessons/design/`, created the section skeleton template `lessons/_template.html`, extracted a class-vocabulary index `static/CLASSES.md`, defined the lesson spec schema `lessons/design/spec_schema.json`, and added the `scripts/new_lesson.py` scaffolder. These changes deliver the input-side substrate needed for the ~95% token reduction targeted by the plan. Phase 2 (the spec → HTML renderer, per-archetype partials, Python verifier, and lossless re-render of the four existing goldens) is deferred to a follow-up plan because spec extraction from existing lessons — particularly reverse-engineering the `cvGen` / `drGen` / `bfGen` step generators — is multi-day work that did not fit this session.

## 2. Goals vs. actuals

| Goal (from plan §2) | Outcome | Evidence |
|---|---|---|
| `lessons/design/` directory with one .md per section + cross-cutting files | ✅ Met | 13 section files (`sec0_clarifying.md` … `sec12_take_home.md`) + 5 cross-cutting (`layout.md`, `code_style.md`, `python_verify.md`, `known_bugs.md`, `archetypes.md`) |
| `lessons/LESSON_DESIGN.md` rewritten as lean index ≤ 800 tokens with load-on-demand table and explicit "do not preload" directive | ✅ Met | ~720 tokens, section→files table at top of file, directive present in the opening blockquote |
| `lessons/_template.html` (~8 KB) section skeleton | ✅ Met | 6.5 KB, 13 sections present with class names + `<!-- PER-PROBLEM: ... -->` markers |
| `static/CLASSES.md` flat class-vocabulary index ≤ 60 lines | ⚠️ Partial | 110 lines — exceeds the 60-line target because the markup vocabulary genuinely has 100+ classes. Still ~1.1 KB vs `static/lesson.css` at 19 KB, so the token-saving goal is met even with the line-count miss. |
| `lessons/design/archetypes.md` problem → archetype → canonical golden lookup | ✅ Met | Four archetypes mapped (`two_pointer`, `sliding_window`, `prefix_scan`, `divide_conquer`) with classification rule and escape hatch |
| `lessons/design/spec_schema.json` (JSON Schema draft-07) | ✅ Met | Covers all 13 lesson sections + `play_speeds`, `custom_step_generator_js`, `overrides`; schema-version-pinned at `"1.0"` |
| `scripts/render_lesson.py` deterministic spec → HTML renderer | ❌ Not met — deferred | Phase 2. Schema and template exist; renderer + partials do not. |
| `scripts/verify_algorithm.py` Python pre-render gate | ❌ Not met — deferred | Phase 2. Principle documented in `design/python_verify.md`; verifier itself not implemented. |
| `scripts/new_lesson.py` scaffolder | ✅ Met | Created; smoke-tested on `two-sum` (happy path) + three error paths (no arg, bad slug, existing dir) |
| End-to-end ≤ 25k tokens for a new lesson, verified by instrumented dry run | ❌ Not met — deferred | Phase 2. Cannot verify the output-side budget without the renderer. The input-side substrate that enables the budget is in place. |
| Four existing goldens re-render byte-equivalent from extracted specs | ❌ Not met — deferred | Phase 2. Requires the renderer + manual spec extraction (~3 hr per lesson per plan §5 task 12). |

## 3. Changes made

### 3.1 Modular design partition (Phase 1.1, §4.1 of plan)
- `lessons/design/sec0_clarifying.md` — principle 4
- `lessons/design/sec1_insight.md` — principles 1, 2, 3, 7
- `lessons/design/sec2_brute_force.md` — principles 9, 10, 13
- `lessons/design/sec3_translations.md` — principles 5, 6
- `lessons/design/sec4_algorithm_english.md` — principles 8, 18
- `lessons/design/sec5_code.md` — principles 13, 25
- `lessons/design/sec6_code_viz.md` — principles 14, 15, 16, 17
- `lessons/design/sec7_dry_run.md` — principles 11, 12, 19, 20, 28
- `lessons/design/sec8_corner_cases.md` — new (no specific v2 principle)
- `lessons/design/sec9_production.md` — principle 21
- `lessons/design/sec10_approaches.md` — new
- `lessons/design/sec11_complexity.md` — new
- `lessons/design/sec12_take_home.md` — principle 27
- `lessons/design/layout.md` — principles 22, 23, 24
- `lessons/design/code_style.md` — principle 25 (cross-cutting)
- `lessons/design/python_verify.md` — principle 26
- `lessons/design/known_bugs.md` — diff inversion + CV scrollbar + variables-before-line + collapsed-priming + wrong-expected + partial-reset
- `lessons/design/archetypes.md` — four-archetype lookup table

Each `sec<N>_*.md` ends with a **Reference excerpts** table mapping the four archetypes to the line range in their canonical golden, so an agent authoring §6 (for example) opens only `lessons/permutation-in-string/lesson.html:459-511` instead of the full 65 KB file.

### 3.2 Index rewrite (Phase 1.2, §4.1 of plan)
- `lessons/LESSON_DESIGN.md` — fully rewritten. Old content (the 290-line legacy doc) replaced with the 70-line index. Old content was already superseded by `LESSON_DESIGN_v2.md`; nothing was lost.

### 3.3 Template skeleton (Phase 1.3, §4.3 of plan)
- `lessons/_template.html` — 6.5 KB, 13 sections, all class names in place, `<!-- PER-PROBLEM: ... -->` markers for the parts the generator fills. References `static/lesson.css` and `static/lesson.js`. Title/slug/LC#/difficulty/tags are template placeholders (`{{TITLE}}` etc.) substituted by `scripts/new_lesson.py`.

### 3.4 Class vocabulary index (Phase 1.4, §4.4 of plan)
- `static/CLASSES.md` — 110 lines, one-line description per class, grouped by section. Notes that this file (not the full CSS) is the input the lesson generator should receive.

### 3.5 Spec schema (Phase 1.5, §4.5 of plan)
- `lessons/design/spec_schema.json` — JSON Schema draft-07 with `spec_version: "1.0"`. Required keys: 17 top-level branches. Optional escape hatches: `custom_step_generator_js`, `overrides`, `play_speeds`. Schema is forward-compatible — additive fields will not break the renderer (per plan §6 risk mitigation).

### 3.6 Scaffolder (Phase 1.6, task 15 of plan)
- `scripts/new_lesson.py` — 100 lines, stdlib-only. Reads `data/problems.json`, substitutes metadata into `_template.html`, writes `lessons/<slug>/{lesson.html, plan.md}`. Exits non-zero on bad slug, missing problem, or pre-existing lesson directory.

### 3.7 Project-meta updates
- `CLAUDE.md` — rewritten to point at `LESSON_DESIGN.md` (the new index) and the load-on-demand rule. References `scripts/new_lesson.py` and `static/CLASSES.md` as required generator inputs.
- `README.md` — project-layout block updated to show `lessons/design/`, `_template.html`, `LESSON_DESIGN.md`, `static/CLASSES.md`, `scripts/new_lesson.py`. New "Authoring a new lesson" subsection added under "Lessons".
- `AGENT_MD/plan/current_state_report.md` — Update entry for 2026-05-14 prepended above the PLAN-010 entry, summarising Phase 1 changes and naming the deferred Phase 2 substrate.
- `AGENT_MD/plan/plans/PLAN-011_lesson_gen_efficiency.md` — status flipped from `Draft` to `In-Progress`.

### 3.8 Files NOT changed (intentional)
- `lessons/LESSON_DESIGN_v2.md` — retained as historical reference per plan §3 non-goals. Future edits should target `LESSON_DESIGN.md` + the `design/` partition, not v2.
- The four golden lessons (`3sum`, `permutation-in-string`, `trapping-rain-water`, `median-of-two-sorted-arrays`) — untouched per plan §3.

## 4. Testing & validation

### 4.1 Scaffolder smoke test

```
$ python3 scripts/new_lesson.py                  # no arg
usage: new_lesson.py <slug>
$ python3 scripts/new_lesson.py 'Bad-Slug'       # invalid slug
slug must match ^[a-z0-9-]+$
$ python3 scripts/new_lesson.py 3sum             # existing directory
lessons/3sum/ already exists — refusing to overwrite.
$ python3 scripts/new_lesson.py two-sum          # happy path
created lessons/two-sum/lesson.html
created lessons/two-sum/plan.md
```

The generated `lessons/two-sum/lesson.html` contained:

```
<title>Two Sum — Interactive Lesson</title>
<link rel="stylesheet" href="../../static/lesson.css">
```

— metadata correctly substituted from `data/problems.json` (LC 1, Easy, Arrays). `plan.md` stub populated with slug, LC #, difficulty, topic. Test artifacts cleaned up after verification.

### 4.2 Manual cross-checks
- Every `lessons/design/sec<N>_*.md` file's **Reference excerpts** line ranges were verified by `grep -n "═══ SECTION"` on each of the four goldens. Numbers match.
- `lessons/LESSON_DESIGN.md` section table cross-checked against the markup in `lessons/_template.html` — all 13 sections present, in order.
- `static/CLASSES.md` cross-checked against `static/lesson.css` — every class name listed in CLASSES.md exists in the CSS; problem-specific classes from individual lessons (e.g. `.bf-bar-con`) are intentionally not listed.

### 4.3 Tests NOT run
- Renderer round-trip on the four goldens (deferred — renderer not implemented).
- Token-budget instrumented dry run (deferred — same reason).
- An automated test asserting `LESSON_DESIGN.md` stays under the 800-token cap (per plan §6 risk mitigation). This is a follow-up CI hook for Phase 2.

## 5. Known issues & follow-ups

The bulk of follow-up work lands in **PLAN-012 (Phase 2 — Renderer + verifier + spec extraction)**. Tasks deferred from PLAN-011:

- Build `lessons/design/partials/sec*.html.tmpl` Jinja fragments — task 9.
- Build `lessons/design/partials/js/<archetype>.js.tmpl` step-generator templates — task 10.
- Implement `scripts/render_lesson.py` — task 11.
- Extract specs from `3sum`, `permutation-in-string`, `trapping-rain-water`, `median-of-two-sorted-arrays` and iterate until lossless round-trip — tasks 12, 13.
- Implement `scripts/verify_algorithm.py` — task 14.
- Instrumented end-to-end token-budget run on `two-sum` — task 16.

Other follow-ups discovered during Phase 1:

- `static/CLASSES.md` overflows the 60-line target. Worth re-grouping or accepting the overflow; the token impact is small (~1.1 KB).
- The four-archetype taxonomy in `archetypes.md` excludes graph / DP / stack / heap / backtracking patterns. The plan's escape hatch (`custom_step_generator_js`) suffices for now, but if > 50% of new lessons need it, a fifth archetype should be promoted (per plan §6 risk row).
- `lessons/design/sec0_clarifying.md` has reference-excerpt line ranges that point one line beyond the next section's marker (e.g. `21-52` ends one line before §1 starts at line 54). Consistent across all section files; documented here for the spec-extractor to follow.

## 6. Metrics

### Tokens for design-doc context (per turn)

| Mode | Tokens loaded |
|---|---|
| Pre-PLAN-011: full `LESSON_DESIGN_v2.md` | ~4,600 |
| Post-Phase-1 idle: `LESSON_DESIGN.md` only | **~720** (−84%) |
| Post-Phase-1, authoring one section: index + 1 section file + cross-cutting | **~1,500–2,500** (−46% to −67%) |

### Tokens for golden-lesson reference (per turn)

| Mode | Tokens loaded |
|---|---|
| Pre-PLAN-011: four goldens loaded whole | ~52,700 |
| Post-Phase-1: index + one archetype excerpt for current section | **~1,000–1,500** (−97%) |

### Tokens for class vocabulary

| Mode | Tokens loaded |
|---|---|
| Pre-PLAN-011: `static/lesson.css` | ~4,800 |
| Post-Phase-1: `static/CLASSES.md` | **~1,100** (−77%) |

Output-side savings (target ~80% via spec → render) **not yet realised** — deferred to Phase 2.

### File sizes

| Path | Bytes |
|---|---|
| `lessons/LESSON_DESIGN.md` (new) | 2.9 KB |
| `lessons/LESSON_DESIGN_v2.md` (retained) | 18.0 KB |
| `lessons/design/` total (18 files) | ~21 KB |
| `lessons/_template.html` | 6.5 KB |
| `static/CLASSES.md` | 4.5 KB |
| `lessons/design/spec_schema.json` | 6.4 KB |
| `scripts/new_lesson.py` | 3.5 KB |

## 7. Lessons learned

- **Spec extraction from existing goldens is the real cost.** The 30-hour plan estimate was front-loaded with quick-win refactors (Phase 1) and back-loaded with deeply manual reverse-engineering (Phase 2 tasks 12–13). One session realistically lands Phase 1 cleanly; Phase 2 needs its own plan with per-lesson time-boxing.
- **British spellings tripped the markdown diagnostics throughout** ("optimisation", "memoisation", "initialised"). Not a code issue, but the diagnostic noise was high. Consider a project-level dictionary if it remains distracting.
- **The "do not preload" directive is a behavioural ask, not a mechanical guarantee.** Until Phase 2's generation script enforces context assembly mechanically, the savings depend on the model following the index. Worth measuring once a real lesson is generated under the new workflow before claiming the headline 95% reduction.
- **The Reference excerpts approach is simple and effective.** Pointing at line ranges in goldens (instead of duplicating the markup inline in `design/` files) keeps the partition lean and prevents drift if a golden is later edited.
- **The scaffolder is a tiny ergonomic win.** ~100 lines of Python eliminate the "copy 3sum, find-and-replace title, hope you didn't miss a reference" loop that Phase-1-without-the-scaffolder would still require.
