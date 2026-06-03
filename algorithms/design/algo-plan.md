# Algorithm Lesson Plan

This document defines the target structure for canonical algorithm lessons under
`algorithms/<id>/`. These lessons teach the algorithm itself, not one LeetCode
problem. The page should feel like a simple, readable GeeksforGeeks-style
explanation paired with a lightweight Visualgo-style interactive animation.

Algorithm lessons are generated only from the curated dashboard inventory:
`data/algorithms.json`, currently 121 entries. Do not invent new algorithm
lesson slugs outside that list. If an algorithm is not in the inventory, add it
through the seed/build flow first, then generate the lesson from the resulting
entry.

This plan intentionally borrows the strongest rules from
`lessons/archive/LESSON_DESIGN_v2.md` and the pasted lesson-design notes:
concept first, one sharp kernel paragraph, named transformations, code hidden
until the reader asks for it, trace-first animations, hard resets between
examples, and variable cards that stay dim until their initializing line runs.

## Goal

Each lesson should help the reader answer four questions:

1. What problem does this algorithm solve?
2. What data structure or state does it maintain?
3. How does the algorithm move from one state to the next?
4. Why does the code match the visual process?

The lesson should be usable without heavy UI libraries. Prefer plain HTML,
CSS, and JavaScript. Animations should be simple, legible, and controllable.

## Inventory Source Of Truth

Every algorithm lesson must begin from one entry in `data/algorithms.json`.
That entry supplies:

- `id`: folder name, such as `binary-search`.
- `name`: display title, such as `Binary Search`.
- `category`: dashboard grouping.
- `tier`: primer/core/advanced teaching depth.
- `interview_relevance`: dashboard priority.
- `complexity`: default time and space claims.
- `prereqs`: prerequisite algorithm IDs.
- `short_note`: first-pass intuition.
- `related_lc`: optional practice links back to LC-style lessons.

The generated folder must match the inventory ID:

```text
algorithms/<id>/
  plan.md
  lesson.html
```

Example:

```text
data/algorithms.json entry: id = "binary-search"
lesson folder: algorithms/binary-search/
plan file: algorithms/binary-search/plan.md
lesson file: algorithms/binary-search/lesson.html
```

The dashboard is the public list. `lesson_status` and `lesson_path` in the
inventory should reflect whether the lesson exists.

## Page Requirements

- Use one `lesson.html` file per algorithm unless the implementation becomes
  genuinely too large.
- Use shared project assets where available.
- Import shared assets from each algorithm lesson with:
  ```html
  <link rel="stylesheet" href="../../static/lesson.css">
  <script src="../../static/lesson.js"></script>
  ```
- Keep the layout calm and readable: explanation first, then interaction.
- Use C++ as the required code language.
- Do not rely on external animation libraries.
- Use buttons and keyboard controls for every visualization.
- Include three built-in examples and one custom input mode.
- Make the custom input validate and normalize user data before animation.
- Ensure the lesson still makes sense if the user never runs the animation.
- Keep problem-specific CSS and JavaScript inline inside `lesson.html` unless a
  shared algorithm asset is deliberately introduced later.
- Do not create inner scrollbars in code panels. If code is too tall, reduce
  font size or line height.
- Use explicit braces in all C++ examples, including single-line `if`, `for`,
  `while`, and `else` bodies.

## Required Sections

Every algorithm lesson should use these sections in this order.

### Section 1: Explain The Algorithm In Plain English

Purpose: make the algorithm feel understandable before symbols, code, or
formal steps appear.

Content should include:

- A foundational concept visual before the algorithm is named formally.
- The real problem the algorithm solves.
- The intuition in everyday language.
- When the algorithm is useful.
- What kind of input it expects.
- What result it produces.
- The key idea in one or two sentences.
- A single kernel paragraph dense enough that the algorithm can be derived from
  it.

Style:

- Use short paragraphs.
- Use concrete language.
- Avoid proof-heavy wording here.
- Do not start with code.
- Lead with a picture, then formalize with text or formulas.
- If there are important preconditions, present them as interview-style
  clarifying questions with an `unlocks` line.

Example shape for `binary-search`:

```text
Binary Search asks: if the input is already sorted, can we find a target
without checking every element?

Linear search works, but it wastes the sorted order. Binary Search keeps a
range of possible answers and throws away half of that range after each
comparison.
```

Clarifying-question shape:

```text
Q: Is the array sorted?
A: Yes. The values are in nondecreasing order.
unlocks: compare against the middle and discard half the range
```

### Section 2: Visualize The Data Structure

Purpose: introduce the moving parts before the full algorithm runs.

This section should visually explain the algorithm's core state. Examples:

- Search range for Binary Search.
- Sorted array for comparison-based search.
- Heap for Dijkstra or Heap Sort.
- Queue for BFS.
- Stack for monotonic stack algorithms.
- Parent array for Union-Find.
- DP table for dynamic programming algorithms.
- Prefix table for KMP.

Content should include:

- What each visual element represents.
- What enters the structure.
- What leaves the structure.
- What invariant the structure maintains.
- Why the structure helps avoid repeated work.

Visual requirements:

- Show the raw input and the live data structure side by side or stacked.
- Use stable dimensions so animation does not shift the page.
- Highlight active elements clearly.
- Use at most a few strong colors with fixed meaning.
- Include a small legend when color meaning is not obvious.
- Show small indexing details visually when they matter, such as `c - 'a'`,
  heap indices, parent pointers, or graph edge weights.
- If a formula appears, place it under the picture that makes the formula feel
  obvious.

For the Binary Search example:

- The current search range is blue.
- The middle cell being inspected is cyan.
- The target, when found, is green.
- The half being discarded briefly flashes red.
- Cells outside the live range stay muted.

### Section 3: Algorithm In Plain English

Purpose: convert the intuition into exact steps before code.

This section should be precise enough that the reader could implement it.

Content should include:

- Inputs.
- Output.
- State variables.
- Initialization.
- Loop steps.
- Update rules.
- Stop condition.
- What gets recorded as the answer.
- Named transformations if the final algorithm is built from multiple ideas.
- The complexity gain from each transformation.

Recommended format:

```text
1. Start with `left = 0` and `right = n - 1`.
2. While `left <= right`, inspect the middle index.
3. If the middle value equals the target, return that index.
4. If the middle value is smaller than the target, move `left` to `mid + 1`.
5. If the middle value is larger than the target, move `right` to `mid - 1`.
6. If the range becomes empty, return `-1`.
```

The section should also state the invariant:

```text
If the target exists, it is always inside the current `[left, right]` range.
```

If the algorithm needs stacked optimizations, show them as a named skeleton
before the final steps:

```text
Translation 1: Check every element -> use sorted order
gain: stop treating the array like an unordered list

Translation 2: Search all remaining values -> inspect the middle
gain: one comparison decides which half cannot contain the target

Translation 3: Shrink by one -> shrink by half
gain: O(n) checks become O(log n) checks
```

### Section 4: Interactive Visualization

Purpose: let the user control the algorithm state, similar in spirit to
Visualgo, but implemented with simple HTML, CSS, and JavaScript.

Required controls:

- Play / pause.
- Step forward.
- Step backward.
- Reset.
- Speed control.
- Example selector with three examples.
- Custom input editor.
- Run custom input.

Keyboard controls:

- Space: play / pause.
- Right Arrow: step forward.
- Left Arrow: step backward.
- R: reset.
- 1, 2, 3: load built-in examples.
- Route keyboard shortcuts to the visible interactive section when a page has
  both the concept visualization and the code walkthrough on screen.

Built-in examples:

Each lesson must include three examples:

1. A small easy example that shows the normal flow.
2. An example that forces the key data-structure behavior.
3. An edge-heavy example with duplicates, boundaries, or unusual shape.

For Binary Search, the examples could be:

```text
Example 1:
nums = [1, 3, 5, 7, 9], target = 7

Example 2:
nums = [2, 4, 6, 8, 10, 12], target = 5

Example 3:
nums = [-10, -3, 0, 4, 4, 9, 12], target = 4
```

Custom input requirements:

- Let the user edit the sorted array.
- Let the user edit the target or algorithm parameter.
- Validate input before running.
- Show clear validation feedback.
- Keep input limits modest so the animation remains readable.
- For algorithms with preconditions, validate the precondition. For Binary
  Search, reject or warn on unsorted input before animation.

Animation requirements:

- The visualization must be state-driven.
- Store each animation frame as a snapshot or derive it from deterministic
  trace data.
- Step backward must work reliably.
- The same trace should drive both the animation and the code walkthrough.
- Avoid animation that depends only on timers; the user must control progress.
- When the user switches examples, hard-reset every timer, frame index, array,
  highlighted cell, output row, variable card, and transient effect.
- If a naive baseline exists, include a compact cost panel or counter so the
  reader feels why the optimized algorithm matters.

For data-structure lessons, the visualization should show:

- The original input.
- The current pointer/index.
- The live data structure.
- Any answer/output built so far.
- A short current-action label.

### Section 5: C++ Code

Purpose: provide the final reference implementation.

Rules:

- Code must be C++.
- Code should be behind a reveal control by default, while the section remains
  visible.
- Use readable modern C++.
- Keep variable names tied to the visualization.
- Avoid clever one-liners.
- Include only comments that clarify non-obvious algorithm decisions.
- The code should be complete enough to copy into a solution function.
- Use explicit braces for every block.
- Keep line breaks friendly to line-by-line highlighting.

For Binary Search-style lessons, prefer:

```cpp
int binarySearch(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (nums[mid] == target) {
            return mid;
        }

        if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}
```

### Section 6: Line-By-Line Code Walkthrough With Visualization

Purpose: connect each statement of C++ code to the visual state change.

This section is separate from the main visualization. The user should be able
to walk through the implementation one statement at a time.

Required behavior:

- Show the C++ code in a code panel.
- Highlight the active line.
- Provide step forward, step backward, reset, and play / pause.
- Use the same examples as Section 4.
- Synchronize code lines with visual state.
- Show variable cards for important variables.
- Variable cards stay dim until their initializing line fires.
- The active variable card lights cyan.
- Values update as the highlighted line executes.
- The code panel must not use `max-height` with an internal scrollbar.
- Every initializing statement should have a visible effect in the variable
  card area.

For the Binary Search walkthrough:

- The array appears below the code or beside it.
- Cells inside the current `[left, right]` range light blue.
- The `mid` cell lights cyan while it is inspected.
- The found target cell lights green.
- The half about to be discarded briefly flashes red.
- Variable cards show `left`, `right`, `mid`, `nums[mid]`, and `target`.
- When the range becomes empty, show the `-1` result clearly.

Trace design:

- Each trace frame should include:
  - `line`
  - `action`
  - `i` or active pointer
  - current data structure state
  - current answer state
  - variables that should be highlighted
  - optional transient effects, such as `flashRed`

Example trace frame shape:

```js
{
  line: 7,
  action: "Compare nums[mid] with the target.",
  left: 0,
  right: 6,
  mid: 3,
  target: 4,
  value: 4,
  result: null,
  activeVars: ["mid", "value"],
  flashRed: []
}
```

The walkthrough should make the code feel inevitable: every line should visibly
do one thing the reader already saw in Sections 2-4.

When the algorithm uses a specialized structure, render that structure in its
most teachable form:

- Frequency arrays: labeled cells, such as `a` through `z`.
- Heap: tree view plus backing-array view.
- Graph algorithms: graph view plus queue/heap/stack frontier.
- Union-Find: parent array plus compressed tree view.
- DP: table view with the active recurrence cell highlighted.

### Section 7: Time And Space Complexity

Purpose: explain the cost in a way that matches the algorithm's mechanics.

Content should include:

- Time complexity.
- Space complexity.
- Why the time bound is true.
- What operations dominate.
- Best, average, and worst case only when they differ meaningfully.
- Common misconception about complexity, if relevant.

For Binary Search:

```text
Time: O(log n)

Each comparison removes about half of the remaining search range. After k
steps, the range has size about n / 2^k. The search stops when that becomes 0
or 1, so k is O(log n).

Space: O(1)

The iterative version stores only `left`, `right`, and `mid`.
```

## Interaction Contract

The page should have two independent but visually consistent interactive areas:

1. Concept visualization.
2. Code walkthrough visualization.

Both should share:

- Example data.
- Color semantics.
- Keyboard controls.
- State labels.
- Reset behavior.
- Example switcher state.
- Validation messages for custom input.

The implementation should prefer a trace-first model:

```text
algorithm input -> trace builder -> list of frames -> renderer
```

Do not make the animation logic mutate the algorithm directly in the DOM. Build
the trace first, then render frame `n`. This keeps pause, rewind, replay, and
keyboard navigation simple.

Before writing HTML, verify the trace logic with a small script or hand-check
table for every built-in example. The expected output, intermediate state, and
edge-case behavior should be known before the animation renderer is written.

## Visual Style

Use a simple educational style:

- White or near-white background.
- Dark readable text.
- Small amount of color for meaning.
- Rounded cards are allowed, but keep them modest.
- Avoid heavy gradients.
- Avoid decorative animation unrelated to the algorithm.
- Prefer clarity over spectacle.

Suggested color meanings:

- Blue: current range/window/active region.
- Green: selected answer or best candidate.
- Cyan: active variable or active code state.
- Red: removal, conflict, failed condition, or pop.
- Gray: inactive, future, or already processed.

## Authoring Checklist

Before marking an algorithm lesson complete:

- Section 1 explains the idea without code.
- Section 1 has a concept visual and a kernel paragraph.
- Section 2 explains the data structure visually.
- Section 3 gives exact plain-English algorithm steps.
- Section 3 names independent transformations when the algorithm has more than
  one core move.
- Section 4 has interactive controls and three examples.
- Section 4 supports custom input.
- Space, arrow keys, and reset shortcuts work.
- Keyboard shortcuts route to the visible interactive section.
- Section 5 shows C++ code.
- Section 5 code uses explicit braces.
- Section 6 syncs code lines with visualization.
- Variable cards initialize and highlight correctly.
- Code panels do not have internal scrollbars.
- Step backward works in both interactive sections.
- Section 7 explains time and space complexity.
- The page works on desktop and mobile widths.
- The animation is readable with the largest built-in example.
- Custom input validation prevents broken states.
- Switching examples hard-resets all state.
- The trace has been verified against every built-in example before shipping.

## Recommended File Shape

For each algorithm:

```text
algorithms/<id>/
  plan.md
  lesson.html
```

The `plan.md` should be written before `lesson.html` and should include:

- Algorithm name.
- Category.
- Prerequisites.
- Core insight.
- Data structure state.
- Invariant.
- Kernel paragraph.
- Named transformations.
- Three built-in examples.
- Custom input format.
- C++ implementation.
- Trace frame schema.
- Complexity explanation.
- Known edge cases.

## Plan Template

Use this when creating `algorithms/<id>/plan.md`.

````md
# <Algorithm Name> Plan

## Metadata

- id:
- category:
- prerequisites:
- audience:
- difficulty:

## Section 1: Explain The Algorithm

- Foundational visual:
- Problem solved:
- Plain-English intuition:
- Kernel paragraph:
- Clarifying questions:
- When to use:
- Input:
- Output:
- Key idea:

## Section 2: Visualize The Data Structure

- Data structure:
- What it stores:
- Invariant:
- Add rule:
- Remove rule:
- Highlight rules:

## Section 3: Algorithm In Plain English

Named transformations:
-

1.
2.
3.

Invariant:

## Section 4: Interactive Visualization

Controls:
- Play / pause:
- Step forward:
- Step backward:
- Reset:
- Speed:
- Keyboard:
- Visible-section routing:

Built-in examples:
1.
2.
3.

Custom input:
- Format:
- Limits:
- Validation:

Trace frames:
- Fields:
- Transient effects:
- Reset behavior:

## Section 5: C++ Code

```cpp
// final implementation
```

## Section 6: Code Walkthrough

- Code lines to highlight:
- Variable cards:
- Visual state per line:
- Pop/removal effects:
- Answer-recording effects:

## Section 7: Complexity

- Time:
- Why:
- Space:
- Why:
- Misconception to address:

## Edge Cases

-

## Completion Checklist

-
````
