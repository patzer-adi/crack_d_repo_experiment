# crack_d

A personal LeetCode study platform. Each problem gets an interactive HTML lesson — visual explanations, step-through animations, and C++ code — all browsable from a local dashboard.

The lesson-authoring side is AI-driven: a single `/batch-lesson` slash command in Claude Code generates lessons end-to-end against the design system in `lessons/design/`. Every lesson is held to a machine-checkable bar: a structural **linter**, a headless **animation-correctness gate** (runs each lesson's step generators and asserts the computed answer matches an independently hand-derived one), and a headless **render check** (loads the lesson in Chromium and asserts no JS error, every code-viz step lights a code line, and nothing overflows). Run `python3 scripts/audit_lessons.py` for live corpus status (it is baseline-aware — see [Quality gate](#quality-gate)). See [Quality gate](#quality-gate) below.

---

## Quick start

```bash
cd crack_d
python3 scripts/server.py
# open http://localhost:8000/dashboard/
```

No dependencies beyond Python stdlib. The server serves all static files and exposes three API endpoints the dashboard uses:

- `PATCH /api/status` — flips `status` (done/new) and/or `lesson_status` (none/generated)
- `POST /api/write` — writes `lessons/<slug>/plan.md`
- `POST /api/add` — adds a new problem from a LeetCode URL

---

## What you actually do day-to-day

There are two normal workflows.

### A. Track and study problems (no AI needed)

1. Open the dashboard at `http://localhost:8000/dashboard/`.
2. Filter by topic, difficulty, status — find what to work on.
3. Click **Open ↗** on any problem with `lesson_status: generated` to read its lesson.
4. Toggle a problem's status (new → done) once you've solved it. The change persists to `data/problems.json`.

### B. Generate lessons for new problems

This is the AI-assisted path. You run it in a Claude Code session.

1. **(Optional)** If the problem isn't in `data/problems.json`, add it via the dashboard's **+ Add problem** button — paste the LeetCode URL and confirm.
2. In a Claude Code session in this repo, type:
   ```
   /batch-lesson <slug1> <slug2> <slug3>
   ```
   Up to 5 slugs per invocation. Slugs match the `slug` field in `data/problems.json` (URL-style: `two-sum`, `3sum-closest`, `find-all-anagrams-in-a-string` — **not** `Two Sum`).
3. The agent runs the workflow for each slug, one at a time:
   - Scaffolds `lessons/<slug>/` from the template.
   - Fills `plan.md` (kernel, archetype, translations, examples with hand-derived answers).
   - Writes `lesson.html`.
   - Runs the [quality gate](#quality-gate) (lint + animation-correctness + render) with bounded auto-retry, and only marks the lesson `generated` once all checks pass, then PATCHes the dashboard so the lesson shows up immediately.
4. Repeats for the next slug.

There is **no manual approval checkpoint** — the gates stand in for human review, so they are non-negotiable and may never be weakened to force a pass (`.claude/commands/batch-lesson.md`).

The full workflow specification lives in [`.claude/commands/batch-lesson.md`](.claude/commands/batch-lesson.md). It loads only when the command fires, so it costs nothing on other sessions.

---

## Project layout

```
crack_d/
├── dashboard/
│   ├── index.html              # 6 tabs in 2 groups — Practice: Basics, Warm-Up, Problems │ Learn: Foundations, Patterns, Algorithms
│   └── prereq-anims.js         # hero step-animations for the Foundations tab (PLAN-021)
├── static/
│   ├── lesson.css              # shared styles for all lessons (extracted once)
│   ├── lesson.js               # shared JS functions for all lessons
│   └── CLASSES.md              # class vocabulary index — feed to generators, not the full CSS
├── lessons/
│   ├── LESSON_DESIGN.md        # lean index (loaded by default); points at design/ on demand
│   ├── LESSON_DESIGN_v2.md     # historical — superseded by design/ partition (PLAN-011)
│   ├── _template.html          # section skeleton used by scripts/new_lesson.py
│   ├── design/                 # load-on-demand section files (sec0…sec12 + cross-cutting)
│   └── <problem-slug>/
│       ├── lesson.html         # interactive lesson — imports static/ assets, problem-specific only
│       └── plan.md             # lesson outline + Python verification trace
├── data/
│   ├── problems.json           # source of truth for all problems + metadata
│   ├── algorithms.json         # algorithm/data-structure catalog (Algorithms tab)
│   ├── patterns.json           # problem-solving patterns by topic (Patterns tab)
│   ├── prerequisites.json      # foundational knowledge units (Prerequisites tab, PLAN-021)
│   ├── prerequisites.schema.json # contract for prerequisites.json
│   ├── basics.json             # language-agnostic programming drills (Basics tab, PLAN-022)
│   ├── warmup.json             # 30 easy LeetCode problems, the on-ramp (Warm-Up tab, PLAN-023)
│   └── roadmap.json            # topic dependency DAG — edges + layout only, no counts (PLAN-024)
├── skills/
│   ├── ds/                     # data structure reference sheets
│   └── patterns/               # algorithm pattern reference sheets
├── scripts/
│   ├── server.py               # local file server + API
│   ├── import_problems.py      # one-time HTML → JSON problem importer
│   ├── new_lesson.py           # scaffolds lessons/<slug>/ from _template.html + problems.json
│   ├── verify_animation.mjs    # animation-correctness gate (Node) — runs drGenSteps + optional verify.py
│   ├── render_check.mjs        # headless render gate (Chromium/CDP) — JS errors, active code line, overflow @ desktop + phone
│   ├── lint_lesson.py          # structural + scaffold linter; delegates to the gate for §7
│   ├── check_prerequisites.py  # data gate for prerequisites.json (ids, fields, topic cascade, coverage)
│   ├── check_basics.py         # data gate for basics.json (slugs, ordering, difficulty ramp, sections)
│   ├── check_warmup.py         # data gate for warmup.json (Easy-only, disjoint from the 211, URL/slug match)
│   ├── check_roadmap.py        # data gate for roadmap.json (acyclic, full topic coverage, stores no counts)
│   ├── audit_lessons.py        # corpus-wide sweep: full lint + render, baseline-aware regression gate
│   ├── audit_baseline.json     # known pre-existing lint/render drift (grandfathered; list only shrinks)
│   └── doctor.py               # planning-doc / lesson-status reconciliation invariants
├── .claude/
│   └── commands/
│       └── batch-lesson.md     # /batch-lesson slash command (Claude Code)
├── CLAUDE.md                   # entry-point conventions for AI sessions (load-on-demand rule)
└── AGENT_MD/                   # planning docs and completion reports (PLAN-NNN / REPORT-NNN)
```

---

## Architecture overview

### Data flow

```
problems.json  ──▶  dashboard/index.html  ──▶  user
       ▲                  │
       │                  ├─ PATCH /api/status  (toggle done, mark generated)
       │                  ├─ POST  /api/write   (write plan.md)
       │                  └─ POST  /api/add     (new problem from LC URL)
       │
       └── PATCH from /batch-lesson agent after each lesson HTML is written
```

### Lesson design system (PLAN-011)

The design guidance is split into a lean index + load-on-demand section files to keep AI generation cheap:

- [`lessons/LESSON_DESIGN.md`](lessons/LESSON_DESIGN.md) is loaded by default (~720 tokens). It contains the section order, the loading rule, and a table mapping each lesson section to the design files that should be loaded when authoring that section.
- [`lessons/design/sec0_clarifying.md`](lessons/design/sec0_clarifying.md) … [`sec12_take_home.md`](lessons/design/sec12_take_home.md) — one file per section, loaded only on demand.
- Cross-cutting: [`design/layout.md`](lessons/design/layout.md), [`design/code_style.md`](lessons/design/code_style.md), [`design/python_verify.md`](lessons/design/python_verify.md), [`design/known_bugs.md`](lessons/design/known_bugs.md), [`design/archetypes.md`](lessons/design/archetypes.md).
- Each section file ends with a **Reference excerpts** table pointing at specific line ranges in canonical golden lessons — so the agent loads ~60 lines of one golden instead of all four whole files.

### Lesson structure

Every generated lesson HTML follows the same 13-section layout (§0–§12), enforced by [`lessons/_template.html`](lessons/_template.html):

| § | Section |
|---|---|
| 0 | Before you code — clarifying questions |
| 1 | The insight — kernel paragraph + foundational visual |
| 2 | Brute force — animation with cost counter |
| 3 | Translations — every named optimisation |
| 4 | The algorithm in plain English |
| 5 | Code (hidden behind reveal button) |
| 6 | Code visualization — line-by-line execution |
| 7 | Dry run — interactive, multiple examples |
| 8 | Corner cases |
| 9 | Production readiness checklist |
| 10 | Approaches — tabs with complexity tags |
| 11 | Complexity |
| 12 | Take home — related problems |

### Tab architecture (PLAN-023)

The dashboard has **six tabs in two labelled groups**, split by what you *do* with them:

```
  PRACTICE                        │  LEARN
  Basics · Warm-Up · Problems     │  Foundations · Patterns · Algorithms
   (70)     (30)      (211)       │
```

**Practice** holds the things you solve — they have a difficulty, a persistent done/new toggle, and a natural order, so they run left-to-right as the ramp you actually walk. **Learn** holds the things you read — reference material with no completion state. Tabs used to render in the order they were *built*, which put the easiest material (Basics) last and the hardest (Problems) first.

`TABS` in [`dashboard/index.html`](dashboard/index.html) is declared in topbar order and is the single source of truth for both routing and rendering. PLAN-023 renamed **Prerequisites → Foundations**; `TAB_ALIASES` redirects `#prerequisites` to `#foundations`, so links that already exist keep working.

**The ⓘ hover card.** Basics and Warm-Up rows carry a small ⓘ next to the name holding fuller guidance (`details`) and a worked `example`. It is one `.info-card` element at `<body>` level, re-anchored per trigger — deliberately *not* nested in the row, because the table wrappers carry `overflow-x: auto` and would clip a positioned descendant. It opens on mouse hover, on tap, **and** on keyboard focus; mouse-vs-touch is branched on `event.pointerType` rather than a `(hover: hover)` media query, so a hybrid laptop gets both right. On phones (≤560px) it docks as a bottom sheet.

### Topic roadmap (PLAN-024)

The Problems tab has two views, switched with `[ Table | Roadmap ]` in the stats bar. Roadmap renders [`data/roadmap.json`](data/roadmap.json) — a 20-node dependency DAG over the problem topics (Arrays & Hashing → Two Pointers → Binary Search / Linked Lists → **Trees** → Backtracking → DP / Graphs → Graphs Advanced). An arrow means *learn this first*. It answers the question the table can't: **what order do I learn topics in, and what does finishing this one unlock?**

It is a *view* of the 211 problems, not a 7th tab — six tabs is already the practical limit of a nav row (PLAN-023).

**`roadmap.json` stores edges and layout only — never a count.** Every `done/total` on the map is computed from `problems.json` at render time, nodes are coloured by progress (complete / in progress / not started), and clicking a node opens that topic in the table. [`scripts/check_roadmap.py`](scripts/check_roadmap.py) enforces this: it **fails if any node has a `count`/`total`/`n` field**, if any topic in `problems.json` lacks a node (a topic would silently vanish from the map), if an edge dangles, or if the graph has a cycle or a back-edge (checked twice — Kahn's algorithm *and* strict layer monotonicity).

That constraint is the whole point. The diagram this replaces was a PNG whose transcribed counts did not match the dataset and could not track it; a derived count cannot drift.

### Responsive / mobile (PLAN-020)

The lessons and the dashboard are usable on a phone — no horizontal page scroll down to 360px. It is plain CSS media queries, no framework:

- **Lessons** ([`static/lesson.css`](static/lesson.css)) collapse two-column grids at `≤680px` and, at `≤480px`, trim padding, scale type down, wrap long code, and let the fixed-height dry-run panels grow. The render gate ([`scripts/render_check.mjs`](scripts/render_check.mjs)) enforces no overflow at 390px going forward.
- **Dashboard** ([`dashboard/index.html`](dashboard/index.html)) hides low-value table columns at `≤700px`/`≤480px`, and every wide table scrolls inside its own wrapper so the page itself never scrolls sideways. The tab strip scrolls horizontally inside the topbar (group labels drop at `≤900px`) so six tabs never widen the page. PLAN-023 widened the check to seven viewports (1440 → 360px), which caught a real bug: the table-wrapper `overflow-x` had been scoped to `≤480px`, so a 768px tablet in portrait scrolled the whole page sideways. It is now unconditional.

### Foundations tab (PLAN-021; renamed from Prerequisites by PLAN-023)

The dashboard's fourth tab answers "what should I understand *before* attempting these problems?". [`data/prerequisites.json`](data/prerequisites.json) holds foundational knowledge units at three levels — **data structures**, **core algorithms**, and **foundational concepts** — each rendered as a card with a plain-language analogy, a lucid explanation, short code snippets, common pitfalls, and a complexity line. Three cards (Hash Map, Binary Search, Recursion) carry a lightweight inline step-animation from [`dashboard/prereq-anims.js`](dashboard/prereq-anims.js).

The "→ N problems" cascade is **derived from each problem's `topic`**, never stored per-problem: a prerequisite lists the topics it unlocks, and the count + clickable topic pills are computed live from `problems.json`. The seed set maps to 20 of the 21 topics, covering 208/211 problems. [`scripts/check_prerequisites.py`](scripts/check_prerequisites.py) is the data gate — it fails if any `topics[]` value is not a real problem topic (so the cascade can never silently resolve to zero), if a referenced animation is unregistered, or if coverage drops below 90 %.

### Basics tab (PLAN-022)

The dashboard's fifth tab is the rung *below* Prerequisites: **language-agnostic learn-to-program drills** — I/O, arithmetic, conditionals, loops, and nested-loop patterns — curated from a user-supplied practice sheet, de-duplicated, difficulty-ramped, and stripped of any one language's syntax. [`data/basics.json`](data/basics.json) holds 70 entries across 7 collapsible sections (Output/Input & Variables → Arithmetic & Expressions → Conditionals → Loop Fundamentals → Digits, Divisors & Primes → Interactive Programs & Loop Control → Nested Loops & Patterns), each with a `statement` (the drill, in prose) and a `source` trace back to the original sheet (or `"new"` for the 12 gap-filling additions). The tab mirrors the Problems tab's idiom — collapsible tables, difficulty badges, a persistent done/new status toggle, search + filters — minus the columns that only make sense for a LeetCode problem (LC number, URL, algorithm cross-links, lesson link).

The status toggle reuses `PATCH /api/status` with an added `dataset` field (`"problems"` default | `"basics"` | `"warmup"`) so [`scripts/server.py`](scripts/server.py) writes the right JSON file. [`scripts/check_basics.py`](scripts/check_basics.py) is the data gate — it fails on slug collisions with `data/problems.json`, non-kebab or duplicate slugs, out-of-order `order` values, a difficulty that drops within a section (the "build up gradually" guarantee), or an unrecognized section/source-ref format. Since PLAN-023 it also requires a `details` blurb and a well-formed `example` on every entry — those feed the ⓘ hover card, and a missing one ships an empty popover.

### Warm-Up tab (PLAN-023)

There is a cliff between Basics and Problems. Basics ends at nested loops and prime factorisation — no hash maps, no trees, no recursion beyond a factorial — while Problems opens on a 211-problem DSA set that is 73 % Medium/Hard and assumes all of it. **Warm-Up** is the ladder between them: [`data/warmup.json`](data/warmup.json) holds 30 **easy** LeetCode problems across 9 sections (Arrays & Hashing → Strings → Two Pointers & Sliding Window → Binary Search → Stack → Linked Lists → Trees → Math & Bits → Dynamic Programming), each picked because it introduces exactly one transferable idea.

That idea is stored in a `skill` field ("prefix sums — a running accumulator", "the recursive tree template", "binary search on a predicate boundary") and rendered as a pill under the statement, so the tab reads as a curriculum rather than a list. All 30 are **disjoint from the 211** — Warm-Up is additive, so the catalogue is 70 + 30 + 211 = **311 problems with no double-entry**.

[`scripts/check_warmup.py`](scripts/check_warmup.py) is the data gate. Beyond the usual field/slug/order checks it enforces the three invariants that make Warm-Up *Warm-Up*: exactly 30 entries and **all Easy** (a Medium belongs in Problems); slug **and** `lc_num` disjoint from `problems.json` and `basics.json` (an overlap would silently double-count a problem across two tabs); and the `url` slug matching `slug` (a row that links somewhere other than what it describes is worse than a row with no link).

---

## Quality gate

Generated lessons are not trusted on faith. Three checks (PLAN-016, extended by PLAN-019) gate a lesson before it may be marked `generated`; `/batch-lesson` enforces all of them, and you can run them by hand:

```bash
# 1. Animation-correctness gate (Node). The dry-run generator (drGenSteps) is the oracle:
#    it is run headlessly over answer-bearing examples and its terminal `result` is
#    deep-compared to each example's independently hand-derived `answer`. If a
#    lessons/<slug>/verify.py exists, it is run too and cross-checked (PLAN-019 G4).
node scripts/verify_animation.mjs <slug>

# 2. Structural + scaffold linter (Python). Section order/markers, the §1/§2/§6/§7
#    canonical chassis (ids, handlers, function names), the §1 insight rules, and
#    the §6 code-line-resolves check. It delegates to the gate above for §7.
python3 scripts/lint_lesson.py <slug>

# 3. Render check (Node + headless Chromium). Loads the lesson, drives every
#    animation, asserts no JS error, every §6 step lights an active code line, and
#    no horizontal overflow at BOTH desktop (1000px) and phone (390px) widths
#    (PLAN-020). Catches layout/runtime drift the other two cannot see.
node scripts/render_check.mjs <slug>

# Corpus-wide sweep — full lint + render over every lesson, baseline-aware (it
# grandfathers pre-PLAN-019 known failures and fails only on NEW regressions).
python3 scripts/audit_lessons.py

# Planning-doc / lesson-status reconciliation invariants (PLAN-019 G5).
python3 scripts/doctor.py
```

**The contract a lesson must satisfy to pass the gate:**

- A pure `drGenSteps` generator (no DOM access) is the correctness oracle. `si`/`cv`/`bf` generators animate pedagogical inputs and are skipped as non-oracles, but must still be pure.
- Examples are declared as `const EX = [{ <inputs>, answer }, …]` (preferred over the bare `EXAMPLES` array). Every `answer` must be **independently hand-derived** — never copied from generator output.
- The generator's **terminal step carries a `result` field** that deep-equals the example's `answer`. Any module-level helper a generator calls must be inlined inside it, because the gate extracts and runs only the generator's own source.

A lesson passes only if ≥1 example verifies, 0 are wrong, and 0 are unverifiable. The full design lives in [`lessons/design/sec7_dry_run.md`](lessons/design/sec7_dry_run.md) ("Correctness contract").

---

## API reference

### `PATCH /api/status`

Update `status` and/or `lesson_status` for one problem.

```bash
# mark problem as solved
curl -X PATCH http://localhost:8000/api/status \
  -H 'Content-Type: application/json' \
  -d '{"slug":"two-sum","status":"done"}'

# mark lesson as generated (the /batch-lesson command does this automatically)
curl -X PATCH http://localhost:8000/api/status \
  -H 'Content-Type: application/json' \
  -d '{"slug":"two-sum","lesson_status":"generated"}'

# both at once
curl -X PATCH http://localhost:8000/api/status \
  -H 'Content-Type: application/json' \
  -d '{"slug":"two-sum","status":"done","lesson_status":"generated"}'
```

Accepted values: `status` ∈ `{done, new}`, `lesson_status` ∈ `{none, generated}`. At least one of the two must be supplied.

### `POST /api/write`

Write a `lessons/<slug>/plan.md` file. Path is validated — only `lessons/<slug>/plan.md` writes are allowed.

```bash
curl -X POST http://localhost:8000/api/write \
  -H 'Content-Type: application/json' \
  -d '{"path":"lessons/two-sum/plan.md","content":"# plan body…"}'
```

### `POST /api/add`

Add a new problem from a LeetCode URL.

```bash
curl -X POST http://localhost:8000/api/add \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://leetcode.com/problems/coin-change/",
    "name": "Coin Change",
    "difficulty": "Medium",
    "topic": "Dynamic Programming"
  }'
```

---

## Adding a new problem manually

If you want to skip the dashboard's **+ Add problem** flow and edit by hand:

```bash
python3 -c "
import json
p = {
    'order': 999, 'lc_num': 322, 'name': 'Coin Change',
    'url': 'https://leetcode.com/problems/coin-change/',
    'slug': 'coin-change', 'topic': 'Dynamic Programming',
    'difficulty': 'Medium', 'status': 'new',
    'section': 'Ad-hoc', 'lesson_status': 'none',
}
data = json.load(open('data/problems.json'))
if not any(x['slug'] == p['slug'] for x in data):
    data.append(p)
    json.dump(data, open('data/problems.json', 'w'), indent=2, ensure_ascii=False)
print('done')
"
```

Then refresh the dashboard.

---

## Authoring a lesson by hand (without `/batch-lesson`)

For single-lesson work or when you don't want to invoke the slash command:

1. **Scaffold:**
   ```bash
   python3 scripts/new_lesson.py <slug>
   ```
2. **Read the index** [`lessons/LESSON_DESIGN.md`](lessons/LESSON_DESIGN.md) — it names which `design/sec<N>_*.md` to load per section. Do not preload all design files.
3. **Fill `plan.md`**, then run a Python trace per [`lessons/design/python_verify.md`](lessons/design/python_verify.md) against every example.
4. **Author each section** of `lesson.html` in order. For class names, use [`static/CLASSES.md`](static/CLASSES.md), never the full CSS.
5. **Pass the [quality gate](#quality-gate)** — both must be clean before the lesson counts as done:
   ```bash
   node scripts/verify_animation.mjs <slug>   # animation-correctness (exit 0)
   python3 scripts/lint_lesson.py <slug>      # structural + scaffold lint
   ```
6. **Mark generated** when done:
   ```bash
   curl -X PATCH http://localhost:8000/api/status \
     -H 'Content-Type: application/json' \
     -d '{"slug":"<slug>","lesson_status":"generated"}'
   ```

---

## Skills

`skills/` contains pattern and data-structure reference sheets useful when authoring lessons:

| File | Contents |
|------|----------|
| `ds/array.md` | Array conventions and pointer notation |
| `ds/linked_list.md` | Linked list patterns and C++ templates |
| `ds/binary_tree.md` | Tree traversal and common operations |
| `patterns/two_pointers.md` | L/R squeeze, complement-sum framing |
| `patterns/sliding_window.md` | Fixed and variable window patterns |
| `patterns/binary_search.md` | Search on answer, rotated arrays |
| `patterns/bfs_dfs.md` | Graph traversal, topological sort |
| `patterns/dynamic_programming.md` | 1D/2D DP, memoisation templates |

---

## Data model

`data/problems.json` is a list of problem objects. Each one:

```json
{
  "order": 27,
  "lc_num": 567,
  "name": "Permutation in String",
  "url": "https://leetcode.com/problems/permutation-in-string/",
  "slug": "permutation-in-string",
  "topic": "Sliding Window",
  "difficulty": "Medium",
  "status": "new",
  "section": "Two Pointers / Sliding Window",
  "lesson_status": "generated"
}
```

- `status` — your personal solve state. `new` or `done`. Toggled from the dashboard.
- `lesson_status` — whether an interactive lesson exists for this problem. `none` or `generated`. Set automatically by `/batch-lesson`, or manually via `PATCH /api/status`.

---

## Planning documents

Implementation work is tracked under `AGENT_MD/plan/`:

- `plans/PLAN-NNN_*.md` — forward-looking design docs (what will be built).
- `reports/REPORT-NNN_*.md` — backward-looking outcome docs (what was actually built).
- `current_state_report.md` — living snapshot of project state.
- `rules.md` — authoring conventions for plan and report documents.

The latest plan: [PLAN-025](AGENT_MD/plan/plans/PLAN-025_nav_declutter_and_roadmap_polish.md) — a presentation-only polish pass: the roadmap now scales to fill the content column (no horizontal scroll on large screens) with a legend-only header, and the nav dropped its `Practice`/`Learn` group labels and per-tab counts, the counts recast on each Practice page as **X of Y completed**, landed 2026-07-15 ([REPORT-025](AGENT_MD/plan/reports/REPORT-025_nav_declutter_and_roadmap_polish.md)).

It builds on [PLAN-024](AGENT_MD/plan/plans/PLAN-024_topic_roadmap_and_branding.md) — the **topic roadmap** (a live, clickable 20-node dependency DAG behind a `Table | Roadmap` switch on the Problems tab, with every count derived from the problem set rather than stored) and the **crack_IT** identity (pinned logo + favicon, replacing a topbar that picked a random logo on every page load), landed 2026-07-14 ([REPORT-024](AGENT_MD/plan/reports/REPORT-024_topic_roadmap_and_branding.md)).

It builds on [PLAN-023](AGENT_MD/plan/plans/PLAN-023_tab_architecture_and_warmup.md) — regrouped the dashboard into six tabs across two groups (**Practice** ‖ **Learn**), renamed Prerequisites → **Foundations**, gave every Basics problem a fuller `details` blurb and a worked example behind an ⓘ hover card, and added the **Warm-Up** tab (30 easy LeetCode problems bridging Basics and the 211), landed 2026-07-14 ([REPORT-023](AGENT_MD/plan/reports/REPORT-023_tab_architecture_and_warmup.md)).

It builds on [PLAN-022](AGENT_MD/plan/plans/PLAN-022_basics_problems_tab.md) — a new **Basics** dashboard tab (70 curated, language-agnostic learn-to-program drills across 7 sections, difficulty-ramped, sourced from a user-supplied practice sheet), landed 2026-07-14 ([REPORT-022](AGENT_MD/plan/reports/REPORT-022_basics_problems_tab.md)).

It builds on [PLAN-021](AGENT_MD/plan/plans/PLAN-021_prerequisites_section.md) — a new **Prerequisites** dashboard tab (foundational data-structure / algorithm / concept knowledge, topic-derived problem cascade, a few hero animations), landed 2026-06-05 ([REPORT-021](AGENT_MD/plan/reports/REPORT-021_prerequisites_section.md)).

It builds on [PLAN-020](AGENT_MD/plan/plans/PLAN-020_mobile_friendly_responsive.md) — mobile-friendly responsive layout for the lessons and dashboard (CSS-only breakpoints; the render gate now also asserts no overflow at 390px), landed 2026-06-04. It builds on [PLAN-019](AGENT_MD/plan/plans/PLAN-019_antidrift_visual_gate_and_doc_reconciliation.md) — anti-drift hardening (headless render gate, corpus re-verification, independent `verify.py` references, and a `doctor.py` for planning-doc/lesson reconciliation), landed 2026-06-03.

> `AGENT_MD/spec.md` is a historical 2026-05-07 snapshot (it predates the gates and most lessons). For current state, read this README + `CLAUDE.md`, or run `python3 scripts/audit_lessons.py` and `python3 scripts/doctor.py`.

---

## Troubleshooting

**Dashboard doesn't show my new lesson.**
The `lesson_status` field in `data/problems.json` is what the dashboard reads. The `/batch-lesson` command sets it automatically. If you authored a lesson by hand, run the curl in [Authoring a lesson by hand](#authoring-a-lesson-by-hand-without-batch-lesson) step 5.

**`new_lesson.py` says "slug not found in data/problems.json".**
Add the problem first — either via the dashboard's **+ Add problem** button or the manual snippet under [Adding a new problem manually](#adding-a-new-problem-manually).

**Slash command does nothing in Claude Code.**
Confirm `.claude/commands/batch-lesson.md` exists in the project root. Slash commands are loaded per-project; the file must be in the working directory when the session starts.

**The agent is loading way too many design files.**
The load-on-demand rule lives in `lessons/LESSON_DESIGN.md`. If an agent ignores it, the cheapest mitigation is to remind it in the prompt; a more durable fix (a mechanical context-assembly script) is anticipated by PLAN-011's deferred Phase 2 but not yet planned.
