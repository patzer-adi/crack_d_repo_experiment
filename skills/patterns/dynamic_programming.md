# Dynamic Programming — Skill File

## What it is
Breaking a problem into overlapping subproblems, solving each once, and storing the result to avoid recomputation (memoisation or tabulation). Applies when: (1) the problem has **optimal substructure** (optimal solution is built from optimal subsolutions) and (2) **overlapping subproblems** (same subproblem recurs). Time complexity moves from exponential (naive recursion) to polynomial (DP).

Two implementation styles:
- **Top-down (memoisation):** recursive function + cache. Natural to write; call-stack overhead.
- **Bottom-up (tabulation):** fill a DP table iteratively from base cases. Usually preferred in interviews for clarity and space-optimisability.

Sub-types covered by a single recurrence-table visual: 1-D DP (array), 2-D DP (matrix), interval DP, subsequence DP. Stock / unbounded knapsack / palindrome problems use the same table convention with a different recurrence.

Canonical problems: Climbing Stairs, Coin Change, Longest Common Subsequence, Edit Distance, House Robber, Unique Paths.

## Visual convention

### 1-D DP table
- A single horizontal row of cells, one per index `i` (like an array).
- Cell label: `dp[i]` above (index), value inside (computed result).
- **Base case cell(s):** blue fill (`--bg-info`), blue border.
- **Current cell being filled:** green fill (`--bg-success`), green border.
- **Dependency cells** (the prior cells used in the recurrence): amber fill (`--bg-warn`), amber border. Draw arrows from dependency cells to the current cell.
- **Filled (done) cells:** white/light fill, full opacity.
- **Not-yet-filled cells:** `opacity: 0.35`, no fill.

### 2-D DP table
- A `m × n` grid. Row index `i` on the left, column index `j` on top.
- Same colour scheme as 1-D: blue for base cases (row 0 and/or column 0), green for current cell, amber for dependencies.
- Dependency arrows: show explicitly which cells the current cell reads (e.g. `dp[i-1][j]`, `dp[i][j-1]`, `dp[i-1][j-1]`).
- Shade the entire filled region (cells with `i' < i` or `j' < j`) lightly to show fill progress.

### Recurrence panel
Below the DP table, show the recurrence relation for the current fill frame:
```
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
      = max(dp[3], dp[2] + nums[4])
      = max(4, 2 + 3)
      = max(4, 5)
      = 5
```
Full substitution on every line — never show `dp[i] = 5` without tracing through the recurrence.

## Animation rules

### Controls — required on every lesson
Every animated dry run must include four controls: ← Prev, ▶ Auto / ⏸ Pause, Next →, ↺ Reset.
Keyboard shortcuts: ← → for prev/next, Space for auto/pause, R or Esc for reset.
See `skills/patterns/two_pointers.md` for the keyboard listener snippet.

### Stable panel layout
Wrap the recurrence panel and step panel in `.panels-fixed` (see `skills/patterns/two_pointers.md`). The recurrence panel is multi-line; set its `min-height` to the tallest recurrence that will appear (typically 4–5 lines for a 2-step recurrence).

### Step panel — structured reasoning
1. **What:** the value computed (`dp[4] = 5`).
2. **Why:** the subproblem meaning and the choice made (`take nums[4]=3, skip nums[3]; total = dp[2] + 3 = 5`).

### Frame sequencing
- **Frame 0:** show the input array and the empty DP table (all cells at `opacity: 0.35`). Caption states the meaning of `dp[i]` and the recurrence.
- **Base case frame(s):** fill `dp[0]` (and `dp[1]` if needed) in blue. Caption explains the base case.
- **Each fill frame:** highlight dependency cells in amber with arrows → compute recurrence (show in formula panel) → fill current cell in green. Then advance: the newly filled cell becomes white, and the next current cell turns green.
- **Final frame:** the answer is `dp[n-1]` (or `dp[m-1][n-1]` for 2-D). Highlight the answer cell green. Caption: "Answer = dp[n-1] = X".
- Fill one cell per frame. For 2-D DP, fill row by row (left to right, top to bottom).

## Algorithmic template (C++)

1-D DP — House Robber:
```cpp
int rob(vector<int>& nums) {
    int n = nums.size();
    if (n == 1) return nums[0];
    vector<int> dp(n);
    dp[0] = nums[0];
    dp[1] = max(nums[0], nums[1]);            // base cases
    for (int i = 2; i < n; i++)
        dp[i] = max(dp[i-1], dp[i-2] + nums[i]);  // recurrence
    return dp[n-1];
}
// Space-optimised: keep only prev2 and prev1 (O(1) space)
```

1-D DP — Coin Change (unbounded knapsack variant):
```cpp
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;                               // base case: 0 coins for amount 0
    for (int a = 1; a <= amount; a++)
        for (int c : coins)
            if (c <= a && dp[a - c] != INT_MAX)
                dp[a] = min(dp[a], dp[a - c] + 1);
    return dp[amount] == INT_MAX ? -1 : dp[amount];
}
```

2-D DP — Longest Common Subsequence:
```cpp
int longestCommonSubsequence(string s, string t) {
    int m = s.size(), n = t.size();
    vector<vector<int>> dp(m+1, vector<int>(n+1, 0));  // base: row 0, col 0 = 0
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            if (s[i-1] == t[j-1]) dp[i][j] = dp[i-1][j-1] + 1;   // match
            else                   dp[i][j] = max(dp[i-1][j], dp[i][j-1]); // skip
    return dp[m][n];
}
```

## Common pitfalls
- Not defining `dp[i]` meaning before showing the table — every lesson must state "dp[i] = the [optimal value / count / boolean] for the subproblem of size i" before filling the first cell.
- Showing only the final filled table without animating the fill order — the fill order IS the algorithm; animate it cell by cell.
- Omitting the arrows from dependency cells to the current cell — dependencies are non-obvious (especially for 2-D DP); always draw them explicitly.
- Not showing the full recurrence substitution — `dp[4] = 5` with no derivation hides the algorithm. Show every substitution step.
- Confusing 0-indexed and 1-indexed tables — be explicit in the formula panel which convention is used; many LCS implementations use a (m+1) × (n+1) table with 1-based string indexing.
- For space-optimised DP: do not animate the space-optimised version as the primary — animate the full table first so the pattern is clear, then mention the optimisation in the code tab.
- Showing too large an example (n > 6 for 1-D, m×n > 4×4 for 2-D) — keep examples small enough that every cell is visible without scrolling.
