# Sliding Window — Skill File

## What it is
Two indices `L` and `R` defining a contiguous subarray (the "window"). `R` advances one step per iteration (expanding the window); when a constraint is violated, `L` advances to shrink the window until the constraint is restored. This collapses an O(n²) nested-loop scan to O(n): each element enters and exits the window exactly once. Two variants:
- **Fixed-size window:** `R - L + 1 == k` always; `L` and `R` advance in lockstep.
- **Variable-size window:** window grows until a constraint is violated, then shrinks until it is satisfied again. The answer is updated at every valid state.

Canonical problems: Longest Substring Without Repeating Characters, Minimum Window Substring, Subarray Sum Equals K, Maximum Sliding Window.

## Visual convention
Render the array using `skills/ds/array.md` conventions (boxes, index labels above, pointer labels below).

- `L` — left window boundary: green cell (`--bg-success`), label `L` in green below cell.
- `R` — right window boundary: amber cell (`--bg-warn`), label `R` in amber below cell.
- **Window interior** (cells between L and R, exclusive): light blue tint (`--bg-info` at 30% opacity), no border change. This visually groups the current window contents.
- **Outside window** (cells left of L or right of R): default white/light, no highlight.
- **Best/answer window:** when a new best is recorded, flash the window interior green for one frame before returning to the default tint.
- **State panel** (below the array, above the step panel): shows the current window contents as a small list or hash map — e.g. `{a:1, b:2, c:1}` for character-frequency problems, or a running sum for sum problems. Updated every frame.

## Animation rules

### Controls — required on every lesson
Every animated dry run must include four controls: ← Prev, ▶ Auto / ⏸ Pause, Next →, ↺ Reset.
Keyboard shortcuts: ← → for prev/next, Space for auto/pause, R or Esc for reset.
See `skills/patterns/two_pointers.md` for the keyboard listener snippet.

### Stable panel layout
Wrap the state-panel and step-panel in a `.panels-fixed` grid (see `skills/patterns/two_pointers.md`). Set `min-height` on the state panel to its tallest expected content to prevent the controls from shifting.

### Formula / state panel — required
Between the array and the step panel, show the current window state every frame:
- **Sum problems:** `window sum = X`, `window size = R − L + 1 = R_val − L_val + 1`.
- **Frequency problems:** a compact key→count table for the current window.
- **Longest/shortest tracking:** `current length = R − L + 1`, `best = Y`.

Always show full substitution: `R − L + 1 = 5 − 2 + 1 = 4`. Never show a bare number.

### Step panel — structured reasoning
1. **What:** result of the current operation (`add nums[R]=3 → sum=11`, `window size=4 → new best`).
2. **Why:** which constraint governs the move (`sum > target → shrink from L`, `char already in window → advance L to remove it`).

### Frame sequencing
- **Frame 0:** full array, `L = R = 0`, window contains just the first element. Caption describes the goal and constraint.
- **Expand frame:** `R` advances right by one. New element added to state. Caption: "Expand: add `arr[R]`".
- **Constraint check frame:** if the constraint is violated after expanding, show a red tint on the step panel. Caption: "Constraint violated — shrink".
- **Shrink frame(s):** `L` advances right by one per frame until constraint is restored. Caption: "Shrink: remove `arr[L]`".
- **Record frame:** when a new best is found (variable window) or a complete fixed window is valid, flash the window green. Caption: "New best: length/sum = X".
- **Final frame:** "Done! Answer = X."
- One pointer move per frame. Never advance both L and R in the same frame.

## Algorithmic template (C++)

Fixed-size window (max sum of k consecutive elements):
```cpp
int maxSumFixed(vector<int>& nums, int k) {
    int sum = 0, best = 0;
    for (int i = 0; i < k; i++) sum += nums[i];     // seed first window
    best = sum;
    for (int R = k; R < (int)nums.size(); R++) {
        sum += nums[R] - nums[R - k];                // slide: add right, drop left
        best = max(best, sum);
    }
    return best;
}
```

Variable-size window (longest subarray with sum ≤ target):
```cpp
int longestSubarray(vector<int>& nums, int target) {
    int L = 0, sum = 0, best = 0;
    for (int R = 0; R < (int)nums.size(); R++) {
        sum += nums[R];                              // expand
        while (sum > target) sum -= nums[L++];       // shrink until valid
        best = max(best, R - L + 1);                 // record
    }
    return best;
}
```

## Common pitfalls
- Advancing both L and R in the same frame — always one pointer move per frame so the viewer can follow the constraint check.
- Not showing the window interior tint — without highlighting the window cells the viewer cannot distinguish inside from outside.
- Forgetting the state panel — `sum` or `frequency map` must be visible every frame; it is the central data structure, not a side note.
- Not showing the full substitution in the formula — `window size = 4` with no trace to `R − L + 1 = 5 − 2 + 1` is ambiguous.
- Using the same L/R green/amber colours without the window interior tint — the interior tint is what makes "window" legible as a group, not just two independent pointers.
- For variable windows: forgetting that `L` can advance multiple times before `R` moves again — animate each `L` advance as a separate frame, not one combined shrink step.
- For fixed windows: not seeding the first window in frame 0 before the slide loop — the first k elements must be visible as the initial window.
