# Section 5 — Step 4: Code

## Principles (from v2 §13, §25)

### Hide code behind a reveal button
The C++ implementation is collapsed by default. A reader scanning for intuition should never be forced to scroll past code. The reveal button signals "this is available when you're ready" without imposing it.

### Explicit braces in every block
Every `if`, `for`, `while`, and `else` — even single-line bodies — must have `{` and `}`. This is **not a style preference**. It is required for the code visualisation's line highlighting to make structural sense. Without explicit braces, the visualiser highlights a single line and the reader cannot tell where the block ends.

```cpp
// CORRECT
if (sum < 0) {
    L++;
} else if (sum > 0) {
    R--;
}

// WRONG — line highlight will be ambiguous
if (sum < 0) L++;
else if (sum > 0) R--;
```

## Markup

- Container: `<div class="section">` with `.sec-label` "Step 4" and `.sec-title` "Code".
- Reveal button: `<button class="reveal-btn" onclick="toggleEl('code-main')">▶ Reveal Code</button>`.
- Code block: `<div id="code-main" class="code-block"><pre class="cb">…</pre></div>`. Toggling the `.open` class on the block is handled by `toggleEl()` from `static/lesson.js`.
- Inside `<pre class="cb">` use the syntax-highlight spans from `static/lesson.css`: `.kw` (keywords), `.fn` (functions), `.tp` (types), `.nu` (numbers), `.cm` (comments).

## Style

- C++ is the primary language for all lessons. If a problem benefits from a Python-only second pass (e.g. `bisect`), include it as a separate code block — same reveal pattern.
- Variable names follow the conventions in the algorithm-in-English step (§4). If §4 names a variable `diff`, the code names it `diff`.

Also load `design/code_style.md` for the full explicit-braces rule and code-block formatting details.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 244–278 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 411–458 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 267–293 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 315–352 |
