# Section 3 — Step 2: Translations

## Principles (from v2 §5, §6)

### Identify ALL independent translations upfront in a named skeleton
If the algorithm requires multiple stacked optimisations, list every one of them in a numbered `.wt-item` skeleton **before any code appears**. Each item needs:

- A **distinct name**: "Translation 3 — Full array comparison → diff counter"
- A **one-paragraph description** with a concrete inline example
- A **complexity gain line** in monospace green: "→ O(26) comparison per step → O(1) per step"

The reader must see the complete mental model before any code. The skeleton is the map; the code is the territory. Never show the territory first.

### Name every optimisation distinctly
Not "the fix" or "the optimisation." Use "Translation 1 / 2 / 3" or "Step 1 / 2 / 3" with a specific verb:

- "Translation 2 — Frequency map → int[26]"
- "Translation 4 — Per-step full compare → diff counter"

The reader should never wonder "wait, was that one trick or two?"

## When to use one translation vs many

- One clean insight (3Sum: sort + two pointers) → one or two translations is enough.
- Stacked optimisations (Permutation in String: sliding window + frequency map + int[26] + diff counter) → list **all four**, in order, each on its own `.wt-item`.

If you find yourself merging two ideas into one bullet "for brevity," you are setting up the reader to fail later when they cannot tell the ideas apart.

## Markup

- Container: `<div class="skeleton">` containing one `<div class="wt-item">` per translation.
- Each `.wt-item` has `.wt-num` (circle with the translation number) and `.wt-body` containing `.wt-name`, `.wt-desc`, `.wt-gain`.
- The `.wt-gain` line is monospace green — small but always present, even if the gain is "→ same complexity, simpler code."

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer (2 translations) | `lessons/3sum/lesson.html` | 194–229 |
| Sliding-window (4 translations) | `lessons/permutation-in-string/lesson.html` | 298–392 |
| Prefix-scan (3 translations) | `lessons/trapping-rain-water/lesson.html` | 206–248 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 268–300 |
