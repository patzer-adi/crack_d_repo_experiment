# Two Pointers — Skill File

## What it is
Two index variables (`left`/`right`, or `i`/`j`) scanning the same array, typically from opposite ends inward. Used when a brute-force O(n²) pair comparison can be collapsed to O(n) by exploiting sort order: on a sorted array, every move of L rightward increases the sum, every move of R leftward decreases it — so each frame eliminates a whole direction. Canonical problems: Two Sum II, 3Sum, Container With Most Water, Trapping Rain Water.

For 3Sum specifically, the pattern runs inside an outer loop that fixes one element `i`, reducing the 3-pointer O(n³) problem to O(n²): fix `i`, sweep `L`/`R` inward in O(n).

## Visual convention
Render the array using `skills/ds/array.md` conventions (boxes, index labels above, pointer labels below).

- `i` — anchor: blue cell (`--bg-info`), label `i` in blue below cell. Omit when the problem has no outer-loop anchor (e.g. Container With Most Water).
- `L` — left pointer: green cell (`--bg-success`), label `L` in green below cell.
- `R` — right pointer: amber/orange cell (`--bg-warn`), label `R` in amber below cell.
- When the current pair produces a match / new max: colour both L and R cells green (`.af`).
- When a duplicate outer-loop index is skipped: grey out that cell (`opacity: 0.35`), no pointer label.
- When L/R are skipped for duplicate avoidance: show a separate frame with new positions.
- Decision label: shown in a coloured step panel below the formula panel:
  - sum < 0 / area improvable via L: blue panel
  - sum > 0 / area improvable via R: amber panel
  - found / new max: green panel
  - done: green panel

## Animation rules

### Controls — required on every lesson
Every animated dry run must include **four controls**:
- **← Prev** — step backward one frame.
- **▶ Auto / ⏸ Pause** — toggle auto-play at ~1.1 s per step.
- **Next →** — step forward one frame.
- **↺ Reset** — return to frame 0 of the currently loaded example without reloading the page.

Below the control row show a keyboard hint line styled with `<kbd>` tags:
```
← → step   Space auto/pause   R reset
```

Keyboard listener (add once at page bottom, after `loadEx(0)`):
```js
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'ArrowLeft')  { e.preventDefault(); prevS(); }
  if (e.key === 'ArrowRight') { e.preventDefault(); nextS(); }
  if (e.key === ' ')          { e.preventDefault(); togglePlay(); }
  if (e.key === 'r' || e.key === 'R' || e.key === 'Escape') { resetAnim(); }
});
```

### Stable panel layout — controls must not shift
Wrap the formula-panel and step-panel in a `.panels-fixed` grid container with explicit row heights.  
This locks the controls' vertical position regardless of content changes:
```css
.panels-fixed {
  display: grid;
  grid-template-rows: 175px 120px; /* adjust per-lesson if fitem-val size differs */
  gap: .875rem;
  margin-bottom: .875rem;
}
.panels-fixed .formula-panel,
.panels-fixed .step-panel { margin-bottom: 0; overflow: hidden; }
```
Also set `min-height: 54px` on `.formula-eq` to reserve two line-heights even in single-line states (init / done frames), preventing the formula-panel from shrinking between frames.

### Formula breakdown panel — required on every lesson
Between the array and the step panel, render a **formula breakdown panel** that shows every variable used in the current frame's computation, labeled by name and index. Each entry shows: variable name (coloured to match its pointer), current index in brackets, and the value at that index.

For sum-based problems (e.g. 3Sum):
```
nums[i=1] = -1    nums[L=2] = -1    nums[R=5] = 2
sum  =  -1  +  -1  +  2  =  0
```

For area-based problems (e.g. Container With Most Water):
```
h[L=1] = 8       h[R=8] = 7       width = R−L = 8−1 = 7
cap = min(8, 7) = 7     area = cap × width = 7 × 7 = 49
```

Every number in the formula must trace back to a labeled source. Never display `area = min(7,8) × 7` without showing that the trailing `7` is `R − L = 8 − 1 = 7`.

### Step panel — structured reasoning
The step panel must contain **two logical parts**, not one long sentence:
1. **What:** the computed value and outcome (`sum = 0 → match`, `area = 49 → new max`).
2. **Why:** the greedy reason the pointer moves (`h[L] < h[R] → right side is the bottleneck; moving R left is the only move that can raise the cap`).

### Frame sequencing
- **Frame 0:** initial state — sorted array (or raw array if no sort needed), both pointers at starting positions, no computation shown yet. Caption explains what we are looking for.
- **Frame 0 without sort:** if the problem does not require sorting (e.g. CWMW), show the raw array as frame 0 and omit the sort step. The skill file's default "show sorted array" applies only to sort-prerequisite patterns.
- **Each inner frame:** show current positions → populate formula panel → show step panel with what+why → positions in the *next* frame reflect the move.
- **Never move both L and R in the same frame.** One pointer move per frame.
- **Duplicate skip:** one separate frame per skip event.
- **Final frame:** "Done!" caption with the result.

## Algorithmic template (include in lesson code tab)

C++ — Sort + Two Pointers (3Sum):
```cpp
vector<vector<int>> threeSum(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> ans;
    int n = nums.size();
    for (int i = 0; i < n - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue;  // skip outer dup
        int L = i + 1, R = n - 1;
        while (L < R) {
            int sum = nums[i] + nums[L] + nums[R];
            if (sum == 0) {
                ans.push_back({nums[i], nums[L], nums[R]});
                while (L < R && nums[L] == nums[L+1]) L++;  // skip L dup
                while (L < R && nums[R] == nums[R-1]) R--;  // skip R dup
                L++; R--;
            } else if (sum < 0) { L++; }
            else                { R--; }
        }
    }
    return ans;
}
```

C++ — Two Pointers (Container With Most Water):
```cpp
int maxArea(vector<int>& height) {
    int L = 0, R = (int)height.size() - 1, best = 0;
    while (L < R) {
        best = max(best, min(height[L], height[R]) * (R - L));
        if (height[L] < height[R]) L++;
        else                       R--;
    }
    return best;
}
```

## Common pitfalls
- Forgetting to include a **Reset** button and **keyboard shortcuts** (← → Space R/Esc) — users need both mouse and keyboard navigation.
- Not wrapping formula-panel + step-panel in a `.panels-fixed` grid — without fixed row heights the controls jump up and down as panel content changes size.
- Not showing the formula breakdown panel — never display a bare arithmetic result; always label every operand.
- Omitting the sort-step frame for problems that require sorting (3Sum); or incorrectly adding a sort frame for problems that do not (CWMW).
- Omitting the `i` anchor pointer when the problem has one (3Sum); or incorrectly showing `i` when the problem has no outer anchor (CWMW).
- Moving both L and R in the same frame — always one move per frame.
- Labelling the pointer with the index value instead of the variable name — breaks comprehension when the pointer jumps non-consecutively.
- Step panel showing only WHAT happened without WHY — the greedy reason must be stated in the same frame.
- For area problems: showing `area = cap × 7` without showing `7 = R − L = 8 − 1` — the width must trace back to the index arithmetic explicitly.
