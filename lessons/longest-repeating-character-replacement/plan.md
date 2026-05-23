# Longest Repeating Character Replacement — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `longest-repeating-character-replacement`
- **LC #:** 424
- **Difficulty:** Medium
- **Topic:** Sliding Window / Frequency Map
- **Archetype:** `sliding_window` — canonical golden is `permutation-in-string`.
  The shape is the same (variable window + freq counts over A–Z) but the
  validity check is `windowLen − maxCount ≤ k` instead of a target-vs-window
  diff counter.

## 1. Clarifying questions (§0)

1. **Q: What's the alphabet?**
   A: Uppercase English letters only (A–Z) per the constraints.
   **Unlocks:** A 26-slot int array suffices for the freq map — no hash map.

2. **Q: What does "longest" mean if k ≥ |s|?**
   A: If we have at least |s| replacements available we can paint the whole
   string a single letter — answer is just |s|.
   **Unlocks:** The window can grow to span the entire string; no upper bound
   on window length other than n.

3. **Q: Do we have to *use* all k replacements?**
   A: "At most" k — fewer is fine. We're counting the resulting same-letter
   run length, not the replacement count.
   **Unlocks:** Validity check is `windowLen − maxCount ≤ k`, an inequality
   — not an equation.

4. **Q: When the window shrinks from the left, does maxCount need to be
   recomputed?**
   A: No — and this is the subtle part. The answer only ever increases when
   we find a *larger* valid window. A larger valid window requires
   `maxCount ≥ previousMax`, which can only happen by the right pointer
   adding more of some letter. So letting `maxCount` linger as a high-water
   mark never causes us to miss a larger answer.
   **Unlocks:** O(1) work per step on shrink — no inner scan of the 26 slots.

## 2. Kernel paragraph (§1)

A window is valid if we can turn all of it into one letter using at most k
replacements. Inside a window of length L, the cheapest replacement plan is
to *keep the most frequent letter* and *replace everything else*. So the
"replacements needed" is exactly `L − maxCount`, where `maxCount = max(freq[c])`
across the window. The window is valid iff `L − maxCount ≤ k`. Slide R
rightward and grow L by 1 each step; whenever validity breaks, advance L by
one (the window stays the same size or grows — it never shrinks net). Track
the largest L the constraint held for.

## 3. Foundational concept visual (§1)

A window strip showing the canonical example `s = "AABABBA"` with `k = 1`.
At each step:
- The current window `[L..R]` is highlighted.
- A small badge row below shows freq counts for letters currently in the
  window.
- The dominant letter (max-count) is coloured green and labelled
  "maxCount = X".
- A formula readout: `len − maxCount = (R−L+1) − max = replaced`.
- The verdict: "valid (≤ k)" or "invalid → shrink L by 1".

The reader sees that growing the window can only ever drive `maxCount` up or
flat; shrinking only changes L; and the answer only grows on `valid` steps.
This is what makes the "don't recompute maxCount on shrink" trick visible
rather than mysterious.

Animation: ~9 steps over the canonical example (one per R move + the shrink
moments).

## 4. Translations (§3)

| Plain-English phrase | Code construct |
|---|---|
| "window of size L" | indices `[L..R]` with `L ≤ R` |
| "letter counts in the window" | `int freq[26]` indexed by `ch - 'A'` |
| "most frequent letter's count" | `maxCount`, updated only by R-side adds |
| "valid window" | `(R − L + 1) − maxCount ≤ k` |
| "shrink because invalid" | `freq[s[L] − 'A']--; L++` once |
| "best answer" | `ans = max(ans, R − L + 1)` |

## 5. Algorithm in plain English (§4)

1. Initialise an int[26] `freq`, `L = 0`, `maxCount = 0`, `ans = 0`.
2. For each `R` from 0 to n−1: bump `freq[s[R]]`, refresh
   `maxCount = max(maxCount, freq[s[R]])`.
3. If the window is invalid (`R − L + 1 − maxCount > k`), decrement
   `freq[s[L]]` and increment `L` once. (One shrink per outer step is enough.)
4. Update `ans = max(ans, R − L + 1)`.
5. Return `ans`.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example (§6 walkthrough):** `s = "ABAB", k = 2`
- Expected: 4
- 4 outer steps, no shrinks needed. Validity equation evaluates to 0,1,1,2
  (all ≤ k).

**Slow example (§7 default):** `s = "AABABBA", k = 1`
- Expected: 4
- 7 outer steps, with 3 shrink moments at R=4, 5, 6. Best window
  `[0..3] = "AABA"` found at R=3; subsequent windows slide right at the same
  size.

**§7 dry-run example buttons (≥ 3):**
1. `"AABABBA", k=1` → 4 (canonical LC).
2. `"ABAB", k=2`    → 4 (no shrinks ever; the easy case).
3. `"ABCDE", k=1`   → 2 (window can never exceed `k+1=2`; shrink fires every
   step after R=2).
4. `"AAAA", k=2`    → 4 (already one letter; k unused).

## 7. Corner cases (§8)

| Case | Input | Expected | Why interesting |
|---|---|---|---|
| Single letter | `"A", k=0` | 1 | Loop runs once; immediate answer. |
| Already one letter | `"AAAA", k=2` | 4 | maxCount climbs every step; no shrink. |
| k=0 | `"AABCDE", k=0` | 2 | Reduces to "longest run of the same letter". |
| All distinct | `"ABCDE", k=1` | 2 | Window can hold maxCount + k = 1 + 1 = 2 letters. |
| k ≥ |s| | `"ABCD", k=10` | 4 | Whole string is one window; never invalid. |
| Surprise stagnation | `"AABABBA", k=1` | 4 | Best window found at R=3; later R's shrink without improving ans. |

## 8. Approaches comparison (§10)

| Approach | Time | Space | Trade-off |
|---|---|---|---|
| **Brute force (every substring)** | O(n²·26) | O(26) | For each (L, R) pair, count letter frequencies and check validity. Simple but TLE at n=10⁵. |
| **Window with maxCount recompute on shrink** | O(n·26) | O(26) | Sliding window, but rescan the 26-slot freq array after each shrink to refresh maxCount. Correct and easy to argue. The extra 26 factor is a constant. |
| **Window with sticky maxCount** | O(n) | O(26) | Never decrement maxCount on shrink. Stale `maxCount` only matters if a *larger* valid window exists, which a later R would discover anyway. The canonical answer. |

## 9. Take home (§12)

- **LC 567 Permutation in String:** Same sliding-window shape, different
  validity check (target frequency match via diff counter).
- **LC 76 Minimum Window Substring:** Variable window, but here we *shrink*
  to find the smallest valid window rather than grow to find the largest.
- **LC 1004 Max Consecutive Ones III:** Same equation in disguise — replace
  0s with 1s using at most k flips, find longest stretch of 1s.
- **LC 340 Longest Substring with At Most K Distinct Characters:** Variable
  window over a freq map again; validity = "at most K non-zero slots".

## 10. Python verification (BEFORE writing HTML)

All 7 cases match expected outputs. Full trace for the canonical slow example:

```
=== verify s='AABABBA' k=1 ===
  R=0 ch=A: freq[A]=1 maxc=1 win=A     len=1 replaced=0  ans=1
  R=1 ch=A: freq[A]=2 maxc=2 win=AA    len=2 replaced=0  ans=2
  R=2 ch=B: freq[B]=1 maxc=2 win=AAB   len=3 replaced=1  ans=3
  R=3 ch=A: freq[A]=3 maxc=3 win=AABA  len=4 replaced=1  ans=4  ★
  R=4 ch=B: freq[B]=2 maxc=3 win=AABAB len=5 replaced=2  INVALID → shrink L (drop s[0]=A); ans=4
  R=5 ch=B: freq[B]=3 maxc=3 win=ABABB len=5 replaced=2  INVALID → shrink L (drop s[1]=A); ans=4
  R=6 ch=A: freq[A]=2 maxc=3 win=BABBA len=5 replaced=2  INVALID → shrink L (drop s[2]=B); ans=4
Got: 4, Expected: 4   OK

Other verified examples:
  s="ABAB",   k=2 → 4    (no shrinks)
  s="ABCDE",  k=1 → 2    (shrink every step after R=2)
  s="AAAA",   k=2 → 4    (maxCount climbs to n)
  s="AABCDE", k=0 → 2    (k=0 boundary)
  s="AAAB",   k=1 → 4    (single trailing different)
  s="BAAAB",  k=2 → 5    (replace both Bs)
```

All matches expected. This is the source of truth for `cvGen`, `drGen`, and
`siGen` step generators.
