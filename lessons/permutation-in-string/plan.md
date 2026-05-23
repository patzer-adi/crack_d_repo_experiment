# Lesson Plan: Permutation in String (LC #567)

> **Plan added retroactively** (2026-05-21) as part of the §1 animation backfill.
> Originally authored before the PLAN-011 plan workflow existed; the lesson HTML
> predates this file. See lesson.html §1 for the canonical insight + animation.

## Metadata
- **Slug:** `permutation-in-string`
- **LC #:** 567
- **Difficulty:** Medium
- **Topic:** Strings / Sliding Window
- **Archetype:** sliding_window (fixed size |s1|, character-frequency comparison)

## 1. Clarifying questions (§0)

1. **Q:** Are s1 and s2 lowercase ASCII?
   **A:** Yes — alphabet size = 26.
   **Unlocks:** Allows a 26-slot freq array instead of a hash map.

2. **Q:** Does the permutation have to be contiguous in s2?
   **A:** Yes — we look for a contiguous substring that is a permutation.
   **Unlocks:** Confirms sliding window applies (not subsequence search).

3. **Q:** Is the answer just a boolean?
   **A:** Yes — true/false, not the index.
   **Unlocks:** Lets us stop at the first match.

## Problem
- **Name:** Permutation in String
- **Number:** 567
- **Link:** https://leetcode.com/problems/permutation-in-string/
- **Difficulty:** Medium
- **Topic:** Sliding Window

## Data structures & patterns
- **DS:** array → load `skills/ds/array.md`
- **Pattern:** sliding window → load `skills/patterns/sliding_window.md`

## Skill files to load into context
1. `skills/ds/array.md`
2. `skills/patterns/sliding_window.md`

## Output file
`lessons/permutation-in-string/lesson.html` — self-contained, offline-capable, no CDN dependencies.

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
