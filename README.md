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
│   └── index.html              # problem tracker — filter, status toggle, open lessons
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
│   └── problems.json           # source of truth for all problems + metadata
├── skills/
│   ├── ds/                     # data structure reference sheets
│   └── patterns/               # algorithm pattern reference sheets
├── scripts/
│   ├── server.py               # local file server + API
│   ├── import_problems.py      # one-time HTML → JSON problem importer
│   ├── new_lesson.py           # scaffolds lessons/<slug>/ from _template.html + problems.json
│   ├── verify_animation.mjs    # animation-correctness gate (Node) — runs drGenSteps + optional verify.py
│   ├── render_check.mjs        # headless render gate (Chromium/CDP) — JS errors, active code line, overflow
│   ├── lint_lesson.py          # structural + scaffold linter; delegates to the gate for §7
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
#    no horizontal overflow. Catches layout/runtime drift the other two cannot see.
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

The latest plan: [PLAN-019](AGENT_MD/plan/plans/PLAN-019_antidrift_visual_gate_and_doc_reconciliation.md) — anti-drift hardening (headless render gate, corpus re-verification, independent `verify.py` references, and a `doctor.py` for planning-doc/lesson reconciliation), landed 2026-06-03. It builds on [PLAN-016](AGENT_MD/plan/plans/PLAN-016_self_healing_pipeline.md), the self-healing pipeline that first made the animation-correctness gate a hard gate.

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
