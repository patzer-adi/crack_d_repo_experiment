# Cross-cutting — Code style

## Principle (from v2 §25)

**Always use explicit braces in every code example.**

Every `if`, `for`, `while`, and `else` block — even single-line bodies — must have `{` and `}`. This is required for the code visualisation's line highlighting to make structural sense. Without explicit braces, the visualiser highlights a single line and the reader cannot tell where the block ends.

## Correct

```cpp
for (int i = 0; i < n - 2; i++) {
    if (i > 0 && nums[i] == nums[i-1]) {
        continue;
    }
    int L = i + 1, R = n - 1;
    while (L < R) {
        int sum = nums[i] + nums[L] + nums[R];
        if (sum < 0) {
            L++;
        } else if (sum > 0) {
            R--;
        } else {
            result.push_back({nums[i], nums[L], nums[R]});
            L++;
            R--;
        }
    }
}
```

## Wrong (do not use)

```cpp
for (int i = 0; i < n - 2; i++)
    if (i > 0 && nums[i] == nums[i-1]) continue;
    // ^ line highlight will look like part of the for body
```

## Other style rules

- C++ is the primary language. `<vector>` / `<algorithm>` / `<unordered_map>` are assumed available; do not include `#include` lines in the displayed code block.
- Use `int n = nums.size();` — never `auto n = nums.size();`. Type-explicit code is easier for a beginner to read.
- Variable names in code must match the names used in §4 (algorithm in plain English) and the names shown in the code-visualization variable cards.
- Do not use Python-flavoured constructs (`for v in vec`) when teaching C++. Use range-based for or index loops, but be consistent within one lesson.

## CV_LINES tagging

Each line in the `CV_LINES` array carries a number `n:` that matches its displayed line number. When you edit code lines, you also edit any `cvGen` step object that references those numbers. Mismatches produce silently wrong highlighting.
