# Repeated Substring Pattern — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `repeated-substring-pattern`
- **LC #:** 459
- **Difficulty:** Easy
- **Topic:** String
- **Archetype:** `custom` (number-theoretic — divisor enumeration over string length). The four canonical archetypes (two-pointer, sliding-window, prefix-scan, divide-conquer) all assume the optimisation comes from spatial pointer movement; here it comes from the arithmetic constraint that the period must divide `n`. Closest neighbour for visual idiom is the prefix-scan family (per-index periodicity check), but we will write step generators from scratch.

## 1. Clarifying questions (§0)

1. **Q:** Can the repeated substring equal `s` itself, i.e. is one copy allowed?
   **A:** No — the problem requires "multiple copies." The substring length must be strictly less than `n`, and at least two copies must tile `s`.
   **Unlock:** This bounds the candidate period `d` to `1 ≤ d ≤ n/2`. Any `d > n/2` would give fewer than two copies.

2. **Q:** What are the input constraints?
   **A:** `1 ≤ n ≤ 10⁴`, lowercase English letters only.
   **Unlock:** O(n·√n) brute force is fine (≈10⁶ ops at worst); we don't need KMP unless we want to flex.

3. **Q:** Does `n = 1` count?
   **A:** No, returns `false`. A single character cannot be "multiple copies."
   **Unlock:** Loop body never runs when `n//2 == 0`; the default-false fall-through handles it.

4. **Q:** Could the answer ever be `true` for a `d` that does NOT divide `n`?
   **A:** No. If `k` copies of a length-`d` substring produce `s`, then `n = k·d`, so `d | n`.
   **Unlock:** This is the kernel — it lets us prune candidates from `n/2` down to `√n`-many divisors.

## 2. Kernel paragraph (§1)

If `s` of length `n` is `k` copies of some pattern `t` (with `k ≥ 2`), then `n` is a multiple of `|t|` — the candidate pattern lengths are exactly the proper divisors of `n` that are at most `n/2`. For any such candidate length `d`, the string `s` is `n/d` copies of `s[0:d]` **iff** `s[i] == s[i − d]` holds for every `i` in `[d, n)`. So the whole problem reduces to: enumerate divisors `d` of `n` with `d ≤ n/2`; for each, scan `i = d…n−1` and abandon `d` on the first mismatch. The answer is true iff any `d` survives the scan.

## 3. Foundational concept visual (§1)

A row of character cells for `s`, with a coloured **window of length `d`** anchored at index 0 (the candidate pattern). Tick marks at positions `d, 2d, 3d, …` mark where copies must begin. An arrow under each comparison `s[i] vs s[i − d]` flips to green ✓ or red ✗ as the periodicity check advances. When all ticks fall on exactly `n` (i.e. `d | n`) and every arrow is green, the row shades into `n/d` repeated blocks.

## 4. Translations (§3)

**Translation 1 — Build-and-compare → in-place periodicity check.**
Naively, for each candidate `d` we'd build `s[0:d] * (n/d)` and string-compare to `s`. That allocates a fresh string per candidate (≈O(n) memory churn per try). Instead, observe that "`s` equals `s[0:d]` repeated" iff `s[i] == s[i − d]` for every `i ≥ d`. No new string, just `n − d` character comparisons with an early-exit on mismatch.
→ `O(n) memory per candidate → O(1) memory; same time, less allocation`

**Translation 2 — All lengths → divisors only.**
A blind search would try every `d` from `1` to `n/2` — that's `n/2` trials, each costing up to `n` work, so O(n²). But if `k` copies of length `d` tile `s`, then `k·d = n`, so `d` must divide `n`. The number of divisors of `n` is O(√n) on average, and we further cap `d ≤ n/2`. We skip every `d` with `n % d != 0` in O(1).
→ `O(n²) trials → O(n · d(n)) ≈ O(n·√n)` where `d(n)` is the divisor count

## 5. Algorithm in plain English (§4)

1. Let `n = len(s)`. If `n < 2`, return false.
2. For each `d` from `1` to `n // 2`:
3. &nbsp;&nbsp;&nbsp;If `n % d != 0`, skip — non-divisors can't tile `s`.
4. &nbsp;&nbsp;&nbsp;Otherwise scan `i = d, d+1, …, n−1`; if any `s[i] != s[i − d]`, abandon this `d` and continue the outer loop.
5. &nbsp;&nbsp;&nbsp;If the inner scan finished with no mismatch, return true — `s` is `n/d` copies of `s[0:d]`.
6. After the loop, return false.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example:** `s = "abab"` → **true**.
- `d=1`: mismatch at `i=1` (`b ≠ a`).
- `d=2`: matches at `i=2,3` → return true. (≈5 steps total.)

**Slow example:** `s = "abcdabcdabcd"` → **true** via `d=4`.
- `d=1`: fail at `i=1` (`b ≠ a`).
- `d=2`: fail at `i=2` (`c ≠ a`).
- `d=3`: fail at `i=3` (`d ≠ a`).
- `d=4`: 8 successful character matches (`i=4..11`), then return true.
- Total ≥ 12 visualisation steps (4 trials + 8 inner matches + state transitions).

**Mismatch example for dry run:** `s = "abcabcabd"` → **false**.
- `d=1`: fail at `i=1`.
- `d=2`: skipped (9 % 2 = 1).
- `d=3`: matches at `i=3..7` (5 trues), fails at `i=8` (`d ≠ c`).
- `d=4`: skipped (9 % 4 = 1).
- Return false. (Demonstrates both the "skip non-divisor" branch and a late inner mismatch.)

## 7. Corner cases (§8)

1. **`n = 1` (e.g. `"a"`):** `n // 2 == 0`, loop body never runs, returns false. Pattern can't be made from "multiple copies" of anything.
2. **All identical (e.g. `"aaaa"`):** returns true at `d = 1` immediately. Smallest period always wins.
3. **Prime length, no repetition (e.g. `"abc"`):** only divisor of 3 with `d ≤ 1` is `d = 1`, which fails. Returns false. Highlights why most lengths get skipped.
4. **Two distinct chars at the boundary (e.g. `"abcabcabd"`):** the inner scan must keep going past partial matches; can't short-circuit on "first half matches."
5. **Largest valid period (e.g. `"abcabc"`, `d = 3 = n/2`):** boundary of the search range. Confirms we include `d = n/2` (i.e. exactly two copies), not just `d < n/2`.

## 8. Approaches comparison (§10)

**Approach 1 — Divisor enumeration + periodicity check (taught).**
For each divisor `d` of `n` with `d ≤ n/2`, verify `s[i] == s[i−d]` for `i ∈ [d, n)`. Time **O(n · d(n))** which is ≈ O(n · √n) in the worst case; space **O(1)**. Easy to derive from first principles and easy to debug — no string library calls.

**Approach 2 — String doubling trick.**
Build `t = (s + s)[1 : 2n − 1]` and return `s in t`. If `s` has period `p < n` with `p | n`, then `s` appears in `s + s` at offset `p`, and the slice `[1 : 2n − 1]` strips the trivial occurrences at offsets `0` and `n`. With a naive `find`, this is O(n²); with Python's built-in `in` (Boyer–Moore-flavoured) or an explicit KMP it's **O(n)**. Stunning one-liner but the correctness argument requires the periodicity lemma — risky to write in an interview without explaining it.

**Approach 3 — KMP failure function.**
Compute the KMP `lps` (longest proper prefix that is also a suffix) array. Let `L = lps[n − 1]`. Then `s` is periodic iff `L > 0` **and** `(n − L) | n`; in that case the period is `n − L`. **O(n)** time, **O(n)** space. The most "algorithmically clean" answer, but requires KMP machinery that's overkill for an Easy problem.

## 9. Take home (§12)

- **686. Repeated String Match** — given `a` and `b`, fewest copies of `a` so that `b` is a substring. Same "concatenate copies" idea, but the periodicity check is replaced by a substring search.
- **28. Find the Index of the First Occurrence in a String** — the natural place to introduce KMP for real, after meeting the failure function casually here.
- **796. Rotate String** — uses the same `(s + s)` doubling trick: `s` is a rotation of `goal` iff `goal in s + s`.
- **1668. Maximum Repeating Substring** — given a `word`, find max `k` such that `word * k` is a substring of `sequence`. Inverse direction — search for the largest repeat instead of asking whether one exists.

## 10. Python verification (BEFORE writing HTML)

Verifier in `/tmp/verify_rsp.py`. Output:

```
=== Fast example: s = 'abab' (expect True via d=2) ===
Input: s='abab', n=4
Search range: d in [1, 2] (need >=2 copies)
  d=1: candidate period (divides n). Check s[i] == s[i-1] for i in [1, 4)
    i=1: s[1]='b' vs s[0]='a' X
    -> mismatch, abandon d=1
  d=2: candidate period (divides n). Check s[i] == s[i-2] for i in [2, 4)
    i=2: s[2]='a' vs s[0]='a' =
    i=3: s[3]='b' vs s[1]='b' =
  d=2: every position matches -> s is 2 copies of 'ab' -> return True

=== Slow example: s = 'abcdabcdabcd' (expect True via d=4) ===
Input: s='abcdabcdabcd', n=12
Search range: d in [1, 6] (need >=2 copies)
  d=1: candidate period (divides n). Check s[i] == s[i-1] for i in [1, 12)
    i=1: s[1]='b' vs s[0]='a' X
    -> mismatch, abandon d=1
  d=2: candidate period (divides n). Check s[i] == s[i-2] for i in [2, 12)
    i=2: s[2]='c' vs s[0]='a' X
    -> mismatch, abandon d=2
  d=3: candidate period (divides n). Check s[i] == s[i-3] for i in [3, 12)
    i=3: s[3]='d' vs s[0]='a' X
    -> mismatch, abandon d=3
  d=4: candidate period (divides n). Check s[i] == s[i-4] for i in [4, 12)
    i=4: s[4]='a' vs s[0]='a' =
    i=5: s[5]='b' vs s[1]='b' =
    i=6: s[6]='c' vs s[2]='c' =
    i=7: s[7]='d' vs s[3]='d' =
    i=8: s[8]='a' vs s[4]='a' =
    i=9: s[9]='b' vs s[5]='b' =
    i=10: s[10]='c' vs s[6]='c' =
    i=11: s[11]='d' vs s[7]='d' =
  d=4: every position matches -> s is 3 copies of 'abcd' -> return True

=== Corner: s = 'aba' (expect False) ===
Input: s='aba', n=3
Search range: d in [1, 1] (need >=2 copies)
  d=1: candidate period (divides n). Check s[i] == s[i-1] for i in [1, 3)
    i=1: s[1]='b' vs s[0]='a' X
    -> mismatch, abandon d=1
  no divisor worked -> return False

=== Corner: s = 'a' (expect False; n//2 = 0, no candidates) ===
Input: s='a', n=1
Search range: d in [1, 0] (need >=2 copies)
  no divisor worked -> return False

=== Corner: s = 'aa' (expect True via d=1) ===
Input: s='aa', n=2
Search range: d in [1, 1] (need >=2 copies)
  d=1: candidate period (divides n). Check s[i] == s[i-1] for i in [1, 2)
    i=1: s[1]='a' vs s[0]='a' =
  d=1: every position matches -> s is 2 copies of 'a' -> return True

=== Corner: s = 'abcabcabd' (expect False) ===
Input: s='abcabcabd', n=9
Search range: d in [1, 4] (need >=2 copies)
  d=1: candidate period (divides n). Check s[i] == s[i-1] for i in [1, 9)
    i=1: s[1]='b' vs s[0]='a' X
    -> mismatch, abandon d=1
  d=2: skip (n % d = 1 != 0, can't tile)
  d=3: candidate period (divides n). Check s[i] == s[i-3] for i in [3, 9)
    i=3: s[3]='a' vs s[0]='a' =
    i=4: s[4]='b' vs s[1]='b' =
    i=5: s[5]='c' vs s[2]='c' =
    i=6: s[6]='a' vs s[3]='a' =
    i=7: s[7]='b' vs s[4]='b' =
    i=8: s[8]='d' vs s[5]='c' X
    -> mismatch, abandon d=3
  d=4: skip (n % d = 1 != 0, can't tile)
  no divisor worked -> return False
```

All six cases match expectations (4 true asserts, 2 false asserts).
