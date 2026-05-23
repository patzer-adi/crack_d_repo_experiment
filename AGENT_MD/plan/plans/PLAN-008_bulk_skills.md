# PLAN-008: Bulk Skills Authoring

**Created:** 2026-05-07
**Status:** In-Progress
**Addresses:** Feature 7 in `AGENT_MD/spec.md` — round out the skill library with 2 DS files and 4 pattern files so future lessons cover the most common L5 interview territory.

---

## 1. Context & motivation

Two skill files exist (`skills/ds/array.md`, `skills/patterns/two_pointers.md`). The dashboard's `TOPIC_SKILL_MAP` already references 6 more that haven't been authored yet — every DP, Sliding Window, Binary Search, BST, Graph, Tree, Linked List, and Backtracking problem generates a prompt that notes these as missing. PLAN-008 fills the gap so generated prompts immediately include the right context.

---

## 2. Goals

- **G1:** `skills/ds/linked_list.md` — nodes split `data | next`, address below, arrows, head/curr/prev pointer conventions.
- **G2:** `skills/ds/binary_tree.md` — circular nodes, left/right children below, null as ∅, BFS level-order and DFS traversal conventions.
- **G3:** `skills/patterns/sliding_window.md` — L/R window highlight, expand/contract frame logic, sum/state formula panel, fixed vs variable size variants.
- **G4:** `skills/patterns/binary_search.md` — lo/mid/hi markers on sorted array, eliminated half greyed out, decision logic.
- **G5:** `skills/patterns/bfs_dfs.md` — frontier/visited highlighting, queue/stack state panel, BFS vs DFS variants.
- **G6:** `skills/patterns/dynamic_programming.md` — DP table fill order, current cell + dependencies highlighted, recurrence in formula panel.
- **G7:** Update `EXISTING_SKILL_FILES` constant in `dashboard/index.html` to include all 6 new files.

---

## 3. Non-goals

- No lesson generation — these are author reference files only.
- No graph DS file (graph problems share the BFS/DFS pattern file visual conventions).
- No heap/stack/trie DS files — low frequency in the 150-problem list; add in a later plan.

---

## 4. Approach

Each file follows the exact same four-section template as `skills/ds/array.md`:
1. **What it is** — 2–4 sentences on when/why.
2. **Visual convention** — precise rendering rules (sizes, colours, layout).
3. **Animation rules** — (pattern files only) controls, formula panel, step panel, frame sequencing. DS files get a shorter "Animation notes" section since they are rendered by patterns.
4. **Common pitfalls** — 4–8 anti-patterns that lesson generators should avoid.

Pattern files additionally include a **C++ algorithmic template** section with a canonical implementation.

---

## 5. Task breakdown

| # | Task | Est. |
|---|------|------|
| 1 | Write PLAN-008 document | 5 min |
| 2 | Write `skills/ds/linked_list.md` | 10 min |
| 3 | Write `skills/ds/binary_tree.md` | 10 min |
| 4 | Write `skills/patterns/sliding_window.md` | 15 min |
| 5 | Write `skills/patterns/binary_search.md` | 12 min |
| 6 | Write `skills/patterns/bfs_dfs.md` | 15 min |
| 7 | Write `skills/patterns/dynamic_programming.md` | 15 min |
| 8 | Update `EXISTING_SKILL_FILES` in dashboard | 5 min |
| 9 | Commit; write REPORT-008; update current_state_report | 10 min |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Skill file style diverges from array.md | Low | Medium | Use array.md as the reference; same section order |
| DP file tries to cover too many sub-types | Medium | Low | Cover the canonical 1-D recurrence visual; note sub-types exist |

---

## 7. Success criteria

- [ ] G1–G7 verified
- [ ] `ls skills/ds/ skills/patterns/` shows all 8 files
- [ ] Dashboard "Generate Plan" for a DP problem generates a prompt that includes `skills/patterns/dynamic_programming.md` with no "not yet authored" note
- [ ] REPORT-008 written; plan status → Completed

## 8. References

- `skills/ds/array.md`, `skills/patterns/two_pointers.md` — style and format reference
- `dashboard/index.html` — `EXISTING_SKILL_FILES` constant to update
- `AGENT_MD/spec.md` Feature 7
