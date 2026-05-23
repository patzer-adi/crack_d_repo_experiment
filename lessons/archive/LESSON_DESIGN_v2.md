# Lesson Design Principles

## Shared assets

**Do NOT regenerate `lesson.css` or the shared JS functions.** They live in `static/lesson.css` and `static/lesson.js` and are extracted once from the golden lessons.

Every lesson HTML must import them with:
```html
<link rel="stylesheet" href="../../static/lesson.css">
<!-- problem-specific inline <style> only, if any unique styles are needed -->
<script src="../../static/lesson.js"></script>
<script>
  /* PROBLEM-SPECIFIC ONLY */
  /* Override any shared function that differs (e.g. bfTogglePlay with a custom speed) */
</script>
```

**What you write per lesson (the only unique parts):**

| Item | Where |
|------|-------|
| Problem-specific CSS (bar charts, freq arrays, state variants, panel-height overrides) | Inline `<style>` |
| `EXAMPLES` and `BF_EXAMPLES` data | Inline `<script>` |
| `CV_LINES` code line array | Inline `<script>` |
| `cvGen()`, `drGen()`, `bfGen()` step generators | Inline `<script>` |
| `cvRender()`, `drRender()`, `bfRender()` (differ per problem) | Inline `<script>` |
| `cvLoadEx()`, `drLoadEx()`, `bfLoadEx()` + init calls | Inline `<script>` |
| Any play-speed override (e.g. `bfTogglePlay` at a non-default speed) | Inline `<script>` before problem-specific script |

**What `static/lesson.js` already provides (do not rewrite):**
`toggleEl`, `switchTab` (null-safe, handles 2- or 3-tab layouts), `cvBuildCode(lines)`, `cvStopPlay`, `cvTogglePlay` (900ms), `drStopPlay`, `drTogglePlay` (1100ms), `bfStopPlay`, `bfTogglePlay` (300ms default), `visPx`, and the `keydown` router.

---

The bar for lessons in this directory is set by three golden reference lessons: [3sum](3sum/lesson.html), [permutation-in-string](permutation-in-string/lesson.html), and [trapping-rain-water](trapping-rain-water/lesson.html). Each is a fully self-contained HTML file — no build step, no CDN dependencies — that a reader can open directly in a browser.

The failure mode these principles are designed to prevent: silently stacking independent ideas and presenting them as one fuzzy slope with vague section labels. A reader can understand each piece individually and still never see why they fit together — the high-level algorithm never crystallizes. Every principle below is a specific fix for a specific way that failure happens.

---

## Mandatory section order

Every lesson must contain these sections in this order. Do not skip, reorder, or merge them.

```
0.  Before you code        — clarifying questions
1.  The Insight            — foundational concept visual + kernel paragraph
2.  Step 1: Brute force    — animation + cost infobox + hidden code
3.  Step 2: Translations   — named skeleton with complexity gains
4.  Step 3: Algorithm      — plain English numbered steps
5.  Step 4: Code           — hidden behind reveal button
6.  Step 5: Code visualization — side-by-side execution
7.  Step 6: Dry run        — interactive, 3 examples
8.  Step 7: Corner cases
9.  Step 8: Production readiness checklist
10. Step 9: Approaches     — tab comparison with code
11. Step 10: Complexity
12. Take home              — related problems
```

The reader assumption: they have already tried to solve the problem, failed, and are now here. They are not a beginner. The lesson does not need to explain what an array is. It needs to explain why the insight works.

---

## The principles

### 1. Surface a single-paragraph kernel early.
One infobox paragraph dense enough that the algorithm is derivable from it. Place it before brute force when the problem has a clean single insight (3Sum: "fix one number, squeeze two pointers"). Place it after brute force when the cost of the naive approach needs to be felt first (Permutation in String: the diff counter only makes sense once you've seen why per-step comparison is wasteful).

### 2. Start with the foundational concept — not the algorithm.
Before any algorithm is mentioned, establish what the problem is really asking in computational terms. This is a separate visual section that comes before the kernel.

- **Permutation in String**: "ba" is a permutation of "ab" because same counts, different order — show the three-column visual (s1 / permutation / non-permutation) with frequency badges before touching sliding windows.
- **Trapping Rain Water**: show a single annotated histogram with maxL wall, maxR wall, and the water level between them before touching two pointers.
- **3Sum**: show the sorted array with a fixed element and two inward-moving pointers on a concrete example before describing the algorithm.

The test: could a reader who doesn't know the algorithm understand what the section is showing? If yes, it's the right foundational concept. If it requires knowing the algorithm first, it's not a concept visual — it's a code explanation.

### 3. The equivalence chain: every ≡ line gets a concrete pill example.
When reducing the problem through a chain of equivalent formulations, each step must show a concrete example of what that equivalence looks like — not just symbols. Format:

```
≡  freq_s1[c] == freq_win[c]  for every character c
   [pill: freq_s1: a=1 b=1 rest=0] [vs] [pill: freq_win("ba"): a=1 b=1 rest=0] [→] [pill green: all 26 slots match ✓]
   [pill: freq_win("cd"): c=1 d=1 rest=0] [→] [pill red: a-slot: 0≠1, b-slot: 0≠1 ✗]
```

Symbols alone do not teach. The pill examples are what turn a symbol chain into an insight.

### 4. Clarifying questions are an interview script, not a FAQ.
Section 0 is not "here are some facts about the problem." It is "here are the questions you would ask in an interview, and here is what each answer unlocks." Format each card as:

```
Q: Can s1 have duplicate characters?
A: Yes — e.g. s1="aab" requires exactly 2 a's and 1 b in the window.
→ unlocks: need counts, not just presence
```

The unlock line (monospace, green) is mandatory. It shows the reader why the question matters — what design decision it enables. Four questions per problem is the right number.

### 5. Identify ALL independent translations upfront in a named skeleton.
If the algorithm requires multiple stacked optimizations, list every one of them in a numbered `.wt-item` skeleton section before any code appears. Each item needs:
- A distinct name ("Translation 3 — Full array comparison → diff counter")
- A one-paragraph description with a concrete inline example
- A complexity gain line in monospace green ("→ O(26) comparison per step → O(1) per step")

The reader must see the complete mental model before any code. The skeleton is the map; the code is the territory. Never show the territory first.

### 6. Name every optimization distinctly.
Not "the fix" or "the optimization." Use "Translation 1 / 2 / 3" or "Step 1 / 2 / 3" with a specific verb: "Translation 2 — Frequency map → int[26]." The reader should never wonder "wait, was that one trick or two?"

### 7. Lead with a picture, then formalize.
Mental model first, formula second. The water formula for Trapping Rain Water (`water[i] = min(maxL, maxR) - h[i]`) is introduced with an annotated bar chart showing exactly those values, then the formula is given as a green infobox underneath. If the picture comes after the formula, the formula feels like a definition to memorize rather than something that falls out of what you can see.

### 8. The algorithm in plain English is a mandatory section.
Before any code appears, there must be a numbered list of 4–6 sentences that describe exactly what the code does — in the words a candidate would say out loud in an interview. This section has a `.algo-steps` style and lives between the translations and the code reveal. It is not a description of the problem. It is a description of the procedure.

Example (3Sum):
```
1. Sort the array. This is what makes the inner search O(n).
2. For each index i from 0 to n−3: if nums[i]==nums[i-1], skip. Set L=i+1, R=n−1.
3. While L < R: compute sum = nums[i]+nums[L]+nums[R].
4. If sum < 0: L++. If sum > 0: R--. If sum == 0: record, skip duplicates, squeeze.
5. Return the collected triplets.
```

### 9. Get the first animation in front of the reader fast.
The brute force animation is the first thing that moves. A reader who scrolls through three sections of prose before seeing anything interactive will lose focus. The brute force widget should be small, auto-playable, and immediately show why the naive approach is slow — the comparison counter ticking up is more visceral than a complexity label.

### 10. Brute force animation: show the cost, not just the answer.
The animation must make O(n²) or O(n³) visible. For 3Sum that means showing the three nested loop indices stepping through all combinations with a live "checks" counter. For Trapping Rain Water that means showing the left scan and right scan for each bar. The counter is the point — the reader needs to *feel* why this is slow before the optimization feels worthwhile.

### 11. Show every diff/boundary-crossing case explicitly.
For any update logic with multiple input combinations (e.g. the diff counter in Permutation in String: freq[x]-- with old==1 → diff--, old==0 → diff++), enumerate all cases and prove each one. The rules must not feel magical. This is especially critical for any counter that tracks "how many X are satisfied" because the boundary crossing direction is always counterintuitive.

**Known invariant:** `freq[x]--` (s2 character entering window):
- old==1 → slot goes 1→0: mismatch **resolved** → `diff--`
- old==0 → slot goes 0→-1: **new** mismatch → `diff++`

`freq[x]++` (s2 character leaving window):
- old==-1 → slot goes -1→0: mismatch **resolved** → `diff--`
- old==0 → slot goes 0→+1: **new** mismatch → `diff++`

Always verify this logic with a Python trace before shipping any frequency-counting lesson. The inversion is easy to get backwards and produces subtly wrong results.

### 12. Two diff-scanner examples: one match, one mismatch.
Whenever showing a diff counter being computed slot-by-slot, always show two side-by-side panels — one where the result is diff=0 (permutation found) and one where diff>0 (no match). A single example with diff=0 makes the counter seem trivial. The mismatch case is what makes the counter's purpose clear.

### 13. Hide code behind a reveal button.
Every code block — including brute force code — is collapsed by default with a "▶ Reveal Code" button. A reader scanning for intuition should never be forced to scroll past C++. The reveal button signals "this is available when you're ready" without imposing it.

### 14. Code visualization: variables dim until their line executes.
The right panel of the code visualization starts with all variable cards dimmed (`opacity: 0.32`). A card becomes visible and highlighted only when the line that assigns it executes. This teaches execution order, not just variable values. Specifically:
- `k` and `n` appear only when line 2 executes
- `diff` appears only when line 6 executes
- Loop index `i` appears only inside the loop
- `c` (character variable) appears only when the character assignment line executes

### 15. Code visualization: freq[] shown as a labeled 26-slot array.
When the algorithm uses an int[26] frequency array, render it as 26 individual cells labeled a–z with color coding:
- Positive values: blue (slot still has unmet demand from s1)
- Negative values: red (window has excess of this character)
- Zero: green (slot satisfied — agreement between s1 and window)
- Active slot (currently being updated): outlined in amber

The active slot is highlighted as each character is processed. This makes the array's state readable at a glance and the diff counter's meaning obvious.

### 16. Code visualization: never set max-height + overflow-y:auto on the code panel.
This creates a scrollbar inside the code panel, which makes the lesson feel cramped and breaks the visual rhythm. The code panel must use `overflow: hidden` only. If the code is too long, use a smaller font or tighten line height — never clip it with a scrollbar.

### 17. Make small indexing details explicit with a visual.
Any time the code uses ASCII arithmetic (`c - 'a'`) or fixed-size buffers, show the mapping explicitly on first introduction:
```
'a' = 97 → index 0
'b' = 98 → index 1
'z' = 122 → index 25
```
Pair this with a small a–z grid showing the example's frequency values filled in. These details are where readers quietly get lost, and a five-second visual eliminates the confusion permanently.

### 18. Algorithm in plain English before the code visualization, not after.
The production readiness checklist lives after the dry run. The algorithm in plain English lives before the code. The reader needs to understand what the code does before watching it execute. The code visualization is not a substitute for the plain-English description — they serve different purposes.

### 19. Dry run: every example should have a "slow" example and a "fast" one.
Pick examples where one finishes in 3–5 steps (lets the reader see the full loop quickly) and one takes 10–15 steps (shows the sliding behavior, the dedup logic, or the edge case). Wire both into an example switcher. The pacing difference alone teaches algorithm behavior that a single example cannot.

### 20. Dry run: prime/setup steps must be traced individually.
Never collapse initialization into a single step. If the algorithm has a priming phase (e.g. building the initial window in Permutation in String), trace each character of that phase individually. The reader needs to see diff adjusting character by character during priming — a single "after priming, diff=4" step teaches nothing.

### 21. Production readiness is a checklist, not prose.
Section 8 is a visual checklist with green checkmark icons. One line per item. Each item has a bold label and a one-sentence explanation. Cover: empty input, all-same input, no-match case, integer overflow, off-by-one in loop bounds, and any problem-specific edge case. The format trains the interview habit of running through edge cases before calling code done.

### 22. Formula panel: fixed height, no layout shift.
The `.panels-fixed` grid uses `grid-template-rows: 175px 110px` — fixed heights for the formula panel and step panel respectively. This prevents the controls from jumping as content changes, which is disorienting during step-through. The formula panel and step panel must never change height between steps.

### 23. Use full page width.
`body { max-width: 1100px }`. The code visualization and dry run both require two side-by-side panels. At 780px these feel cramped and produce horizontal scrollbars inside panels. 1100px is the minimum at which the layout breathes.

### 24. Route keyboard shortcuts to the visible section.
One global `keydown` handler, routing `←`/`→`/`Space`/`R` to whichever interactive section (cv-section or dr-section) has more pixels visible in the viewport. Use `getBoundingClientRect()` to compare. The reader should never have to think about which widget has focus — the keys follow their eyes.

### 25. Always use explicit braces in all code examples.
Every `if`, `for`, `while`, and `else` block — even single-line bodies — must have `{` and `}`. This is not a style preference. It is required for the code visualization's line highlighting to make structural sense. Without explicit braces, the visualizer highlights a single line and the reader cannot tell where the block ends.

### 26. Verify algorithm correctness with a Python trace before writing any HTML.
For every problem, run a Python simulation of the algorithm against all planned examples before writing the step generator. Print every variable at every step. Verify the output matches expected. This catches logic bugs — especially diff counter inversions — before they are embedded in hundreds of lines of JS. A bug in the step generator produces subtly wrong narration that is very hard to find later.

### 27. The "take home" section names related problems.
The last section always ends with 2–4 related problems that use the same skeleton or pattern. These are not just links — each gets one sentence saying exactly what differs: "LC 438 (Find All Anagrams — same algorithm, collect all match positions instead of returning on first match)." This shows the reader how the pattern generalizes.

### 28. Example switcher: hard-reset all state on switch.
When the reader switches examples, every piece of state must reset: frequency arrays, diff counters, loop indices, result arrays, animation timers, variable card highlights. A partial reset that leaves stale state from the previous example is the most common source of subtle bugs in the step generators. Reset everything, always.

---

## Known bugs to avoid

**Diff counter inversion.** The direction of diff adjustment is counterintuitive and is easy to get backwards. `freq[x]--` with old==1 means the slot is going 1→0 — a mismatch just resolved, so `diff--`. With old==0, the slot goes 0→-1 — a new mismatch, so `diff++`. The code that appears correct (`if freq[c]==1: diff++`) is wrong. Always verify with a Python trace.

**CV scrollbar.** Never set `max-height` + `overflow-y: auto` on the code panel. Use `overflow: hidden` only.

**Variables visible before their line.** In the code visualization, variable cards initialized at the top of the function (k, n, diff, maxL, maxR) must not appear populated until the line that assigns them executes. Start all cards dimmed.

**Collapsed priming steps.** In dry run step generators, never collapse multi-character initialization into one step. Trace each character.

**Wrong expected values in algorithm test.** Always print what the algorithm actually returns, then decide if that's the right example to use — don't write a test with an expected value from memory.

---

## When in doubt

- Less prose, more pictures.
- Foundational concept visual before kernel paragraph.
- One narrative kernel, then named translations.
- Brute force animation before the optimization.
- Algorithm in plain English before code.
- Code visualization before dry run.
- Checklist for production readiness, not prose.
- If a paragraph just describes what a visual already shows, delete the paragraph.
- If a counter or derived value feels magical, build a scanner widget that computes it slot-by-slot.
- Verify the algorithm with Python before writing JS.