# Section 10 — Step 9: Approaches

## Principle

Two or three named approaches compared in a tabbed view: optimal first, alternatives after. Each tab carries its own code block (still hidden behind a reveal button — see §5), complexity tags, and a short prose paragraph saying when this approach is the right one to mention.

This is where you discuss **trade-offs** that didn't fit in §3 (Translations). Section 3 is the derivation of the optimal solution. Section 10 is "here are the alternatives an interviewer might ask about, and what's different."

## Format

Three tabs is typical for problems with a textbook second approach:

- **Tab 1** — Optimal (the same code as §5).
- **Tab 2** — A common alternative (hashset for 3Sum, brute force for permutation-in-string, DP for trapping-rain-water).
- **Tab 3** — An advanced or theoretical alternative (e.g. Boyer–Moore-like compression, segment tree).

Two tabs is also acceptable when only one alternative is worth mentioning.

## Markup

- Container: `<div class="section">` with `.sec-title` "Approaches".
- Tab bar: `<div class="tab-bar">` with one `<button class="tab-btn">` per tab. The first has `.active`.
- Tab panes: one `<div class="tab-pane">` per tab; the first has `.active`.
- Inside each pane:
  - Complexity tags: `<span class="tag tag-time">O(n²)</span> <span class="tag tag-space">O(1)</span>`.
  - One-paragraph description.
  - `<button class="reveal-btn">` + `<div class="code-block">` for the code.

Switching is wired by `switchTab(barId, paneSelector, idx)` from `static/lesson.js`.

## Pitfall

Do not duplicate the §5 code block verbatim in Tab 1. The optimal code lives in §5 once; Tab 1 of §10 either re-shows it (acceptable) or links to it ("Same code as Step 4"). Do not let the two diverge.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 398–420 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 596–618 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 418–451 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 481–503 |
