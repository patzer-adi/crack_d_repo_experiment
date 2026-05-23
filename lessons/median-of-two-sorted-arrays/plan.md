# Lesson Plan: Median of Two Sorted Arrays (LC #4)

> **Plan added retroactively** (2026-05-21) as part of the §1 animation backfill.
> Originally authored before the PLAN-011 plan workflow existed; the lesson HTML
> predates this file. See lesson.html §1 for the canonical insight + animation.

## Metadata
- **Slug:** `median-of-two-sorted-arrays`
- **LC #:** 4
- **Difficulty:** Hard
- **Topic:** Arrays / Binary Search
- **Archetype:** binary_search (on partition index of the smaller array)

## 1. Clarifying questions (§0)

1. **Q:** Does either array have to be non-empty?
   **A:** At least one must be non-empty; the other can be empty.
   **Unlocks:** An empty array becomes the trivial split (j = 0 or j = m+n).

2. **Q:** Are values integers or floats?
   **A:** Integers; the median may still be a non-integer when m+n is even.
   **Unlocks:** Decides we return a float (or use floats for the average).

3. **Q:** Does the result need O(log(m+n)) time?
   **A:** Yes — the problem requires it; merging is O(m+n) and disallowed.
   **Unlocks:** Forces the partition-binary-search approach.

## Problem
- **Name:** Median of Two Sorted Arrays
- **Number:** 4
- **Link:** https://leetcode.com/problems/median-of-two-sorted-arrays/
- **Difficulty:** Hard
- **Topic:** Binary Search

## Data structures & patterns
- **DS:** array → load `skills/ds/array.md`
- **Pattern:** binary search → load `skills/patterns/binary_search.md`

## Skill files to load into context
1. `skills/ds/array.md`
2. `skills/patterns/binary_search.md`

## Output file
`lessons/median-of-two-sorted-arrays/lesson.html` — self-contained, offline-capable, no CDN dependencies.

## Lesson sections (produce all of these)

### 1. Intuition
[Explain the key insight that makes this approach work over brute force. Cover: brute-force cost, the invariant or structure that enables the optimal approach, and why the pattern applies here.]

### 2. Animated dry run
[Choose 2–3 representative inputs (one typical, one edge, one tricky). Walk through every step: data structure state, pointer/variable positions, decision made, result update. Use the visual conventions from the DS skill file.]

### 3. Corner cases
| Case | Input | Expected | Why |
|---|---|---|---|
| Empty input | ... | ... | ... |
| Single element | ... | ... | ... |
| All same value | ... | ... | ... |
| [add more relevant cases] | ... | ... | ... |

### 4. Code (C++ — revealed after attempt)
[Canonical C++ solution. Include type declarations, one comment per logical step, complexity analysis at the end. Code hidden behind "Reveal Code" toggle by default.]

### 5. Approaches (two tabs)
**Tab 1 — [Primary approach name]**
Time: O(?). Space: O(?).
[Brief description — why this complexity, what the key insight is.]

**Tab 2 — [Alternative approach name]**
Time: O(?). Space: O(?).
[Brief description. Provide code if it's concise; otherwise a text sketch.]

## Quality bar
Follow the visual conventions in the skill files and match the style of existing lessons:
- Self-contained HTML/CSS/JS, no CDN dependencies
- `.panels-fixed` layout (grid-template-rows: 175px 120px) to prevent control shift
- Formula breakdown panel showing variable values + full substitution per step
- Step panel split: `.step-what` (computed result) + `.step-why` (decision reasoning)
- Keyboard shortcuts: ← → Space R/Esc
- ↺ Reset button, Reveal Code toggle (hidden by default), approach tabs
