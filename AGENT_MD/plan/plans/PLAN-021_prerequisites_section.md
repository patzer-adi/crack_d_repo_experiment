# PLAN-021: Prerequisites section — foundational knowledge layer for the problem set

**Created:** 2026-06-05
**Status:** Completed
**Completed:** 2026-06-05 — see [REPORT-021](../reports/REPORT-021_prerequisites_section.md).
**Addresses:** There is no place that names and explains the foundational knowledge
(data structures, core algorithms, base concepts) a learner should hold *before*
attempting the 211 problems. The Patterns tab covers problem-solving *techniques*;
the `skills/ds/*.md` files exist but are rendered nowhere. Learners cannot see
"to be ready for this problem, first understand X, Y, Z."

---

## 1. Context & motivation

The dashboard (`dashboard/index.html`) has three tabs — Problems, Algorithms,
Patterns. The **Patterns** tab (`data/patterns.json`, 20 entries) already explains
*how to attack* a problem (two-pointers, sliding window, dynamic programming…) as
rich expandable cards with a core idea, code snippets, pitfalls, and a
"→ N problems" cascade chip. See [REPORT-005](../reports/REPORT-005_dashboard.md)
for the tab architecture and the recent "Patterns section added" work.

What is **missing** is the layer *beneath* technique: the **prerequisites** — the
data structures and base concepts a learner must already understand for a
technique or problem to make sense. Three signals that this is a real gap:

1. `skills/ds/array.md`, `skills/ds/linked_list.md`, `skills/ds/binary_tree.md`
   exist as authored explainers but are **not surfaced in any UI**.
2. `TOPIC_SKILL_MAP` in `dashboard/index.html` references DS skill files for
   `graph`, `heap`, `stack`, `trie` that **do not exist on disk** — the model
   wants a DS knowledge layer that was never built.
3. Each of the 211 problems carries a `topic` (21 distinct values), but nothing
   tells the learner what foundational knowledge that topic presumes.

This plan adds a **Prerequisites** tab: a browseable, grouped set of foundational
knowledge cards (data structures · core algorithms · base concepts), each with a
lucid explanation, an analogy, short code, and an automatically-derived list of
the problems it unlocks. A small number of hero animations make the most
fundamental ideas intuitive.

**Product decisions (confirmed with the user before drafting):**
- **Structure:** a *new* Prerequisites tab modeled on the Patterns tab, backed by
  a new `data/prerequisites.json` that absorbs/extends the existing
  `skills/ds/*.md` content. The Patterns tab stays technique-focused.
- **Cascade (point 4 of the brief):** the "→ N problems" link is **derived from
  each problem's `topic`** — zero edits to the 211 problem records. A
  data-structure-level prerequisite automatically affects every problem in the
  topics it maps to.
- **Depth (point 7):** lean expandable cards for *all* prerequisites, **plus 1–3
  hero inline animations** for the most foundational ideas. This honours the
  project's "nothing fancy" default while still making key ideas intuitive.

**Interpretation of "can have multiple pages" (point 5):** satisfied by the same
idiom the Patterns tab uses — the tab is split into independently collapsible
grouped sections (Data Structures / Core Algorithms / Foundational Concepts) with
search + level filters. No literal multi-URL pagination is introduced; that would
duplicate the lessons subsystem for no benefit. Flagged here per
`AGENT_MD/plan/rules.md` §6.1 (surface interpretation, don't pick silently).

---

## 2. Goals

- **G1** A new **Prerequisites** tab exists in `dashboard/index.html` alongside
  Problems / Algorithms / Patterns, reachable via the `#prerequisites` hash, with
  no JS console error on load.
- **G2** `data/prerequisites.json` ships with **≥ 15 prerequisite entries**
  spanning three levels — data structures, core algorithms, foundational concepts
  — and **collectively maps to topics covering ≥ 90 % of the 211 problems** (every
  problem can see at least one prerequisite via its topic).
- **G3** Each card renders a **tagline, analogy, lucid explanation, ≥ 1 short code
  snippet**, and a **"→ N problems" cascade chip** whose count is computed live
  from `problems.json` by topic and that jumps to the filtered Problems tab.
- **G4** The three authored `skills/ds/*.md` explainers (array, linked list,
  binary tree) are **reused** — their content is migrated into the matching
  `prerequisites.json` entries (no orphaned, unsurfaced explainer files).
- **G5** **1–3 hero inline animations** (target: Hash Map, Binary Search,
  Recursion/Call-Stack) play step-by-step inside their cards with Prev/Next
  controls and no horizontal overflow.
- **G6** A data validator `scripts/check_prerequisites.py` passes: unique `id`s,
  required fields present, every `topics[]` value exists in `problems.json`'s
  topic set (cascade can never silently resolve to zero), and every animation id
  referenced by a card is registered.
- **G7** The new tab has **zero horizontal page overflow at 360 px and 390 px**
  across the section (honours [PLAN-020](PLAN-020_mobile_friendly_responsive.md)),
  verified headless.
- **G8** Existing tabs (Problems / Algorithms / Patterns) are **visually and
  behaviourally unchanged**; `scripts/audit_lessons.py` and `scripts/doctor.py`
  stay green.

## 3. Non-goals

- **Not** turning each prerequisite into a full standalone lesson page under the
  `lessons/` gate pipeline (`lint_lesson.py` / `verify_animation.mjs` /
  `render_check.mjs`). Prerequisites are dashboard cards, not gated lessons.
- **Not** editing the 211 records in `data/problems.json`. No per-problem
  `prerequisites:[]` field — the cascade is topic-derived (confirmed decision).
- **Not** reworking the Patterns tab or `data/patterns.json`.
- **Not** exhaustive coverage of every conceivable concept on day one; ≥ 15
  high-leverage entries, expandable later.
- **Not** fixing the pre-existing `body` max-width doc/CSS discrepancy (1270 vs
  1100 px) carried over from REPORT-020 §5 — unrelated.

## 4. Approach

### 4.1 Data model — `data/prerequisites.json` (new)

A JSON array mirroring the *shape* of `patterns.json` so the render code can be
near-identical, with three additions geared to "foundational knowledge":
`level`, `analogy`, and an optional `animation` id.

```jsonc
{
  "id": "hash-map",                    // kebab slug, unique
  "name": "Hash Map / Hash Set",
  "level": "data-structure",           // data-structure | algorithm | concept
  "group": "Data Structures",          // collapsible-section bucket
  "group_order": 1, "order": 2,
  "icon": "#",
  "tagline": "O(1) average lookup by key.",
  "analogy": "A coat-check: hand over a ticket (key), get your coat (value) back instantly — no scanning every hook.",
  "explanation": "A hash map stores key→value pairs... (markdown, lucid).",
  "snippets": [
    { "label": "Membership / dedup",
      "code": ["unordered_set<int> seen;", "if (seen.count(x)) ...", "seen.insert(x);"] }
  ],
  "pitfalls": ["Average O(1), worst-case O(n) on pathological hashing."],
  "complexity": "Lookup/insert O(1) avg, O(n) memory.",
  "topics": ["Arrays & Hashing"],      // drives the cascade (point 4)
  "animation": "anim-hash-map"          // optional; only the 1–3 hero entries
}
```

- **`topics[]` is the cascade key.** It lists `problems.json` `topic` values; the
  card's "→ N problems" count is `ALL.filter(p => topics.has(p.topic)).length`.
  Many-to-many: a prerequisite may map to several topics (e.g. *Recursion* →
  `Backtracking`, `Trees`, `Graphs — BFS / DFS`), and a topic may be unlocked by
  several prerequisites.
- **Seed set (~15–18):** *Data structures* — Array, Hash Map/Set, Linked List,
  Stack, Queue, Binary Tree, BST, Heap/Priority Queue, Graph (adjacency
  list/matrix), Trie. *Core algorithms* — Binary Search mechanics, BFS/DFS
  traversal, Sorting (and when to sort), Recursion & the call stack. *Foundational
  concepts* — Big-O / complexity, Prefix sums, Bit manipulation basics. Array,
  Linked List, Binary Tree reuse the prose already in `skills/ds/*.md` (G4).

### 4.2 Optional schema — `data/prerequisites.schema.json` (new)

Mirror the existing `data/algorithms.schema.json` convention so the dataset has a
declared contract the validator can lean on. Lightweight; lists required fields
and the `level` enum.

### 4.3 Dashboard — new Prerequisites tab (mirrors Patterns)

In `dashboard/index.html`, the tab is a near-clone of the Patterns plumbing:

- **Topbar:** add a 4th `.tab-btn` (`id="tab-btn-prerequisites"`,
  `onclick="switchTab('prerequisites')"`, label `Prerequisites` + count span).
  Extend `const TABS = ['problems','algorithms','patterns','prerequisites']` — the
  generic `switchTab` + hash routing then work unchanged.
- **Panel:** add `<div class="tab-panel" id="tab-panel-prerequisites">` with a
  stats bar (total · groups · levels · problems-mapped), a filter bar (search +
  level/group `<select>`), and `<div class="content" id="pre-content">`.
- **JS:** `let PREREQS = []`; `loadPrerequisites()` (fetch
  `../data/prerequisites.json`, sort by `group_order`/`order`, set count, populate
  filters, render) added to the existing `Promise.all([...])` in init;
  `applyPrereqFilters()`, `renderPrereqs(visible)` (grouped collapsible sections
  via the existing `toggleSection`/`section-hdr` pattern), `buildPrereqCard(p)`
  (analogy block + explanation + snippets + pitfalls + cascade chip + optional
  animation mount), and `prereqProblemCount(p)`:

```js
function prereqProblemCount(pr) {
  const topics = new Set(pr.topics || []);
  return ALL.filter(p => topics.has(p.topic)).length;   // cascade by topic
}
```

  The cascade chip reuses the existing `goToTopic(primaryTopic)` to jump to the
  filtered Problems tab — no new navigation code.
- **CSS:** add `.pre-*` classes by analogy to `.pat-*` (or reuse `.pat-*`
  directly where identical) plus a `.pre-analogy` callout and a `.badge-level`
  chip. All new rules scoped so other tabs are untouched (G8).

### 4.4 Hero animations (1–3, gate-exempt)

Reuse the lessons' vanilla-JS, step-driven frame idiom (Prev/Next over a small
frame array; see [PLAN-017](PLAN-017_animation_conventions.md)) but **lighter and
inline** — these are dashboard widgets, not gated lessons, so they are explicitly
out of the lesson render/verify gates (§3). To keep `dashboard/index.html` from
ballooning (already ~1740 lines), animation code lives in a new
`dashboard/prereq-anims.js`: a registry `{ "anim-hash-map": mountFn, ... }` keyed
by the card's `animation` id. `buildPrereqCard` mounts the matching widget into a
`<div class="pre-anim" data-anim="...">` placeholder.

- **Scope:** at most three — Hash Map (insert→lookup), Binary Search (interval
  halving), Recursion (call-stack push/pop). Each ≤ ~6 frames, CSS-only visuals,
  wrapped in `overflow-x:auto` so they never overflow the page (G7).
- **Alternative considered:** inline the animation JS directly in
  `index.html`. Rejected — it would add ~150+ lines to an already-large single
  file; a separate, lazily-relevant script is cleaner and easier to revert.

### 4.5 Mobile (honour PLAN-020)

Four tabs + logo must still fit a 360 px topbar. The existing
`@media(max-width:480px)` rule `.tab-btn span{display:none}` already hides all
count badges (covers the new tab). If four labels still crowd 360 px, allow the
tab strip to scroll horizontally (`overflow-x:auto` on the tab container) rather
than shrink fonts further — verified headless at 360/390 px. Cards inherit the
patterns-card responsive behaviour; animations are `overflow-x:auto`.

### 4.6 Validation — test-first (rules.md §5.11)

`scripts/check_prerequisites.py` is written **before** the dataset and run as the
authoring gate: (a) `id` unique & kebab-case; (b) required fields present per the
schema; (c) every `topics[]` value ∈ the set of `problems.json` topics (fail loud
if a cascade maps to nothing); (d) every `animation` id referenced is registered
in `dashboard/prereq-anims.js`; (e) report total problems covered (for G2's 90 %
threshold). The dashboard render is validated by the PLAN-020 headless
overflow harness extended to switch to the `#prerequisites` tab at 360/390 px,
plus a smoke assertion that *N* cards rendered with no JS error.

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Write `scripts/check_prerequisites.py` (validator) + `data/prerequisites.schema.json` against the schema in §4.1, with a tiny fixture so it runs red first | 1.5 hr | — |
| 2 | Author `data/prerequisites.json` seed (~15–18 entries; migrate `skills/ds/*.md` prose for array/linked-list/binary-tree) until the validator passes & ≥ 90 % coverage | 3 hr | 1 |
| 3 | Dashboard: add 4th tab button, panel markup, `TABS` entry, `loadPrerequisites` into init `Promise.all`, stats/filter wiring | 1.5 hr | 2 |
| 4 | Dashboard: `renderPrereqs` + `buildPrereqCard` + `prereqProblemCount` + cascade chip (reuse `goToTopic`); `.pre-*` CSS | 2.5 hr | 3 |
| 5 | `dashboard/prereq-anims.js`: 1–3 hero animations + mount registry; wire into `buildPrereqCard` | 3 hr | 4 |
| 6 | Mobile pass: 360/390 px tab-fit + card/animation no-overflow; extend the PLAN-020 headless check to the new tab | 1.5 hr | 4, 5 |
| 7 | Docs: README (Prerequisites subsection + `data/` inventory line), `current_state_report.md` (new top entry), bump "latest plan" → PLAN-021 in `CLAUDE.md` + README; write `REPORT-021` | 1.5 hr | 6 |
| 8 | Final gate sweep: `check_prerequisites.py` ✓, headless dashboard delta=0 @360/390, `audit_lessons.py` no new drift, `doctor.py` 0 violations | 0.5 hr | 7 |

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Topic→prerequisite mapping too coarse (one topic needs several prereqs, or a prereq spans topics) | Med | Med | `topics` is an array → many-to-many; validator reports coverage so gaps are visible |
| Hero-animation scope creep beyond "nothing fancy" | Med | Med | Hard cap of 3, gate-exempt, ≤6 frames each, isolated in `prereq-anims.js` so they are trivially droppable/revertible |
| Four tabs crowd the 360 px topbar | Med | Low | Count badges already hidden on phone; fall back to horizontal tab-strip scroll; verified headless (G7) |
| `dashboard/index.html` grows unwieldy | Med | Low | Animation code in a separate `prereq-anims.js`; render code reuses patterns helpers (`toggleSection`, `mdInline`, `goToTopic`) |
| Cascade silently maps to zero problems (typo in a topic string) | Low | Med | Validator rule (c) fails the build if any `topics[]` value isn't a real `problems.json` topic |
| Regressing existing tabs / gates | Low | High | All new CSS/JS additive & namespaced; `audit_lessons.py` + `doctor.py` in the final sweep (G8) |

## 7. Success criteria

The plan is complete when, with `data/`, `dashboard/`, `scripts/`, and docs
changed and nothing committed until the user asks:

1. **G1/G3** — Loading `dashboard/index.html#prerequisites` shows the new tab with
   grouped cards, each rendering tagline + analogy + explanation + code + a live
   "→ N problems" chip that navigates to the filtered Problems tab; no console
   error.
2. **G2/G4** — `data/prerequisites.json` has ≥ 15 entries across all three levels,
   covers ≥ 90 % of the 211 problems by topic, and the three `skills/ds/*.md`
   explainers are reused (no unsurfaced explainer files remain).
3. **G5** — The hero animations step forward/back inside their cards with no
   overflow.
4. **G6** — `python3 scripts/check_prerequisites.py` exits 0.
5. **G7** — Headless dashboard at 360 px and 390 px on the Prerequisites tab:
   `delta = 0`.
6. **G8** — `scripts/audit_lessons.py` → no new drift; `scripts/doctor.py` → 0
   violations; Problems/Algorithms/Patterns tabs unchanged.

All six map back to §2 goals G1–G8.

## 8. References

- `AGENT_MD/plan/rules.md` — authoring conventions (this plan follows the §3 template).
- `AGENT_MD/plan/current_state_report.md` — latest project state.
- [PLAN-020](PLAN-020_mobile_friendly_responsive.md) / [REPORT-020](../reports/REPORT-020_mobile_friendly_responsive.md) — mobile gate this plan must honour.
- [PLAN-017](PLAN-017_animation_conventions.md) — animation conventions reused (lightly) for hero widgets.
- [REPORT-005](../reports/REPORT-005_dashboard.md) — dashboard tab architecture the new tab mirrors.
- `data/patterns.json` + `dashboard/index.html` `renderPatterns`/`buildPatternCard` — structural template for the Prerequisites tab.
- `skills/ds/array.md`, `skills/ds/linked_list.md`, `skills/ds/binary_tree.md` — explainer prose reused in the seed dataset.
- `data/problems.json` — 211 problems, 21 `topic` values; the cascade source.
