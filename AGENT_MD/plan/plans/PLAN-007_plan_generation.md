# PLAN-007: Plan Generation + Copy-Paste Prompt

**Created:** 2026-05-07
**Status:** In-Progress
**Addresses:** Feature 6 in `AGENT_MD/spec.md` — dashboard "Generate Plan" flow that creates `lessons/<slug>/plan.md` and shows the user a ready-to-paste Claude prompt.

---

## 1. Context & motivation

PLAN-006 added `POST /api/write` — the write primitive is ready. The user now needs a dashboard UI to:
1. Select one or more problems.
2. Click "Generate Plan" → auto-builds a `plan.md` template per problem and POSTs it.
3. See a modal with the exact Claude prompt to paste in VS Code to generate `lesson.html`.

This removes the friction of manually writing `plan.md` for each new problem.

---

## 2. Goals

- **G1:** Each problem row in the dashboard has a checkbox. A "select all visible" checkbox is in the table header.
- **G2:** A sticky action bar appears at the bottom when ≥1 problem is selected; it shows the count and a "Generate Plan" button.
- **G3:** Clicking "Generate Plan" calls `POST /api/write` for each selected problem, creating `lessons/<slug>/plan.md` with a structured template inferred from the problem's topic, difficulty, LC number, and URL.
- **G4:** The generated `plan.md` follows the structure of `lessons/3sum/plan.md`: problem metadata, inferred DS + patterns, skill-file list, output file path, five lesson section outlines, and quality bar.
- **G5:** A modal appears after generation showing, per problem: a ready-to-paste Claude prompt that lists `lessons/<slug>/plan.md` and all skill files to load (with existence status noted). Each prompt has a "Copy" button.
- **G6:** Already-generated plans (where `lessons/<slug>/plan.md` already exists) trigger a 409-style warning in the modal rather than silently overwriting (the write still succeeds — this is just a UI notice).
- **G7:** Checkbox state persists across filter changes (selection is slug-keyed, not DOM-keyed).

---

## 3. Non-goals

- No new server endpoints — uses the existing `POST /api/write`.
- No auto-run of Claude — user always pastes the prompt manually.
- No per-problem status update (`lesson_status` remains `none` until the user runs `import_problems.py` after generating the lesson).
- No bulk "Generate All" action — deliberate per-problem control.

---

## 4. Approach

### 4.1 Selection model

`SELECTED = new Set()` of slugs. Checkbox changes toggle entries. `updateActionBar()` shows/hides the sticky bar and updates the count. `buildRow()` checks `SELECTED.has(p.slug)` when re-rendering filtered rows so checkboxes survive filter changes.

### 4.2 Topic → skill file mapping

A `TOPIC_SKILL_MAP` table maps each of the 25 known topics to DS and pattern skill files. `EXISTING_SKILL_FILES` is a hardcoded Set of skill files that currently exist on disk (updated when PLAN-008 adds more). The prompt only labels existing files; missing files are noted as `(not yet authored — PLAN-008)`.

### 4.3 plan.md template

```
# Lesson Plan: {name} (LC #{lc_num})

## Problem
- **Name:** {name}
- **Number:** {lc_num}
- **Link:** {url}
- **Difficulty:** {difficulty}
- **Topic:** {topic}

## Data structures & patterns
[inferred from TOPIC_SKILL_MAP]

## Skill files to load into context
[numbered list of skill file paths]

## Output file
`lessons/{slug}/lesson.html`

## Lesson sections (produce all of these)
### 1. Intuition
### 2. Animated dry run
### 3. Corner cases
### 4. Code (C++ — revealed after attempt)
### 5. Approaches (two tabs)

## Quality bar
[standard quality requirements copied from 3sum plan]
```

### 4.4 Claude prompt template

```
Read the following files into your context, then generate the lesson HTML:

  lessons/{slug}/plan.md
  {existing_skill_files — one per line}

Generate: lessons/{slug}/lesson.html

Follow the plan exactly. The lesson must be:
- Self-contained HTML/CSS/JS (no CDN, everything inline)
- Visual style: warm grey background (#efede8), dark near-black text
- .panels-fixed layout (prevents control shift on content resize)
- Formula breakdown panel with full substitution per step
- Step panel split: .step-what + .step-why
- Keyboard shortcuts: ← → Space R/Esc
- ↺ Reset button, Reveal Code toggle (hidden by default), approach tabs
```

### 4.5 Modal UX

- **Header:** "Plans created for N problem(s)"
- **Per-problem section:** problem name, slug, write status (✓ created / ⚠ already existed / ✗ failed), full prompt text, "Copy" button
- **Dismiss:** × button or click outside

---

## 5. Task breakdown

| # | Task | Est. |
|---|------|------|
| 1 | Write PLAN-007 document | 10 min |
| 2 | Add checkbox column CSS + HTML to dashboard | 15 min |
| 3 | Add SELECTED state + `buildRow` checkbox + header select-all | 15 min |
| 4 | Add action bar (sticky footer, count, Generate Plan button) | 10 min |
| 5 | Implement `TOPIC_SKILL_MAP`, `buildPlanMd()`, `buildPrompt()` | 20 min |
| 6 | Implement `generatePlans()` (async POST loop) + `showModal()` | 20 min |
| 7 | Smoke test: select 2 problems, generate plans, inspect files, copy prompt | 10 min |
| 8 | Commit; write REPORT-007; update current_state_report | 10 min |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Skill file list goes stale after PLAN-008 | Medium | Low | `EXISTING_SKILL_FILES` constant in dashboard JS — update it when PLAN-008 runs |
| Modal prompt too long for multi-problem | Low | Low | Each problem is its own collapsible block; modal scrolls |
| `POST /api/write` race on concurrent generates | Very low | Low | Sequential awaits in the generate loop |

---

## 7. Success criteria

- [ ] G1–G7 above verified
- [ ] Select 2 problems → generate → both `lessons/<slug>/plan.md` files created with correct metadata
- [ ] Modal copy button pastes a valid prompt referencing existing skill files
- [ ] Filter → problems stay selected (slugs in SELECTED survive re-render)
- [ ] REPORT-007 written; plan status → Completed

## 8. References

- `scripts/server.py` — `POST /api/write` endpoint (PLAN-006)
- `dashboard/index.html` — file being modified
- `lessons/3sum/plan.md` — plan.md format reference
- `AGENT_MD/spec.md` Feature 6
