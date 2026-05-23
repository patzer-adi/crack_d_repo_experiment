# Lesson Plan: Trapping Rain Water (LC #42)

> **Plan added retroactively** (2026-05-21) as part of the §1 animation backfill.
> Originally authored before the PLAN-011 plan workflow existed; the lesson HTML
> predates this file. See lesson.html §1 for the canonical insight + animation.

## Metadata
- **Slug:** `trapping-rain-water`
- **LC #:** 42
- **Difficulty:** Hard
- **Topic:** Arrays / Two Pointers
- **Archetype:** two_pointer (outside-in, commit water at the side with smaller running max)

## 1. Clarifying questions (§0)

1. **Q:** Can heights be zero?
   **A:** Yes — a zero bar still traps water if walls surround it.
   **Unlocks:** Drives the water[i] = min(maxL, maxR) − h[i] formula even when h[i] = 0.

2. **Q:** Are bars unit width?
   **A:** Yes — area is just sum of trapped heights.
   **Unlocks:** Lets us count integers, not areas.

3. **Q:** Can n be very small?
   **A:** n can be 0 or 1; both trap 0 water.
   **Unlocks:** Early exit at the start of the function.

## Problem
- **Name:** Trapping Rain Water
- **Number:** 42
- **Link:** https://leetcode.com/problems/trapping-rain-water/
- **Difficulty:** Hard
- **Topic:** Arrays

## Data structures & patterns
- **DS:** array → load `skills/ds/array.md`
- **Pattern:** two pointers → load `skills/patterns/two_pointers.md`

## Skill files to load into context
1. `skills/ds/array.md`
2. `skills/patterns/two_pointers.md`

## Output file
`lessons/trapping-rain-water/lesson.html` — self-contained, offline-capable, no CDN dependencies.

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
