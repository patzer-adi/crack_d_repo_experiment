# Lesson plan — Repeated String Match (LC 686)

## Metadata

- **Slug:** repeated-string-match
- **LC #:** 686
- **Difficulty:** Medium
- **Topic:** String Matching
- **Archetype:** custom (escape-hatch). None of the four canonical archetypes
  (two-pointer / sliding-window / prefix-scan / divide-conquer) fits a "how many
  times must I tile string a so b is a substring" question, so the step generators
  are written from scratch. The teaching object is the **bound itself**: why only
  ⌈n/m⌉ and ⌈n/m⌉+1 copies ever need checking.
- **Twist (from problems.json):** "bounded brute: only need to repeat a up to
  ⌈len(b)/len(a)⌉ + 1 times" — the naive "keep appending a and search" loop has no
  stopping rule; the insight supplies one.

## 1. Clarifying questions

1. **What exactly is returned — a boolean or a count?** The *minimum number of
   copies* of `a` whose concatenation contains `b`, or `-1` if no number works. →
   the answer is an integer, so the oracle compares with `===` on a plain int (no
   ordering subtleties).
2. **Can the answer be 0 or 1?** Never 0 (zero copies is the empty string, which
   contains `b` only if `b` is empty — out of LC's constraints); it can be 1 when
   `b` already sits inside a single `a`. → the floor is `⌈n/m⌉ ≥ 1`.
3. **When is it impossible (−1)?** When `b` uses a character not in `a`, or a
   substring that the periodic tiling of `a` never produces. → after the bounded
   check fails, return −1; do not loop forever.
4. **How large can the strings get?** `a`, `b` up to ~10⁴. → building `b` plus two
   extra copies of `a` and one substring search is O(m + n); fine. The naive
   unbounded loop is the trap, not the search itself.

## 2. The insight (foundational concept)

`b` is a substring of `a` repeated `k` times **iff** `b` can be read off the
periodic tiling `a a a …` starting at some offset. Two facts bound `k`:

- **Length floor.** To even *fit* an `n`-char `b`, the tiling must be at least
  length `n`, i.e. at least `k = ⌈n/m⌉` copies (`m = |a|`, `n = |b|`).
- **Offset ceiling (+1).** `b` need not begin at a copy boundary — it can start as
  far as offset `m−1` into the first copy, pushing its tail into one extra copy. So
  `⌈n/m⌉ + 1` copies cover **every** possible starting offset within the first copy.

Therefore the answer is `⌈n/m⌉`, or `⌈n/m⌉ + 1`, or — if `b` is in neither — `−1`,
because the tiling is periodic with period `m`: any window of length `n` that does
not appear within `⌈n/m⌉+1` copies has already been seen, so longer tilings add
nothing new. Two `find`s decide the whole problem.

## 3. Translations

1. "Keep appending a and search after each copy" → **bounded loop**: only `k =
   ⌈n/m⌉` and `k+1` can be answers, so check exactly those two and stop. Kills the
   infinite loop on impossible inputs.
2. "Re-search the whole growing string each time" → **build once, search twice**:
   build `a` repeated `⌈n/m⌉` times, `find(b)`; if absent append one more `a` and
   `find(b)` again.
3. "Is `b` reachable at all?" → **periodicity argument**: if `b` is absent from
   `⌈n/m⌉+1` copies it is absent from every repetition → `−1`.

## 4. Algorithm (bounded brute force)

1. `m = |a|`, `n = |b|`. Compute `k = ⌈n/m⌉ = (n + m − 1) / m` (integer division).
2. Build `s = a` repeated `k` times. If `b` is a substring of `s`, return `k`.
3. Otherwise append one more `a` (`s += a`, now `k+1` copies). If `b` is a
   substring, return `k + 1`.
4. Otherwise return `−1`.

## 5. Examples (hand-derived two ways: bounded-brute and the modular reference)

The oracle (`drGenSteps`) builds `a.repeat(k)` and calls `indexOf(b)`. The
independent reference (`verify.py`) never builds a string: for each start offset
`0 ≤ start < m` it tests `b[j] == a[(start+j) % m]` for all `j`, and if every
character matches it needs `⌈(start+n)/m⌉` copies; the answer is the minimum over
matching offsets, else `−1`. Different mechanism, same number — so the cross-check
is not a tautology.

| # | a | b | k=⌈n/m⌉ | answer | why |
|---|------|------------|--------|--------|-----|
| EX0 (LC ex1) | `abcd` | `cdabcdab` | 2 | **3** | absent in 2 copies (starts at offset 2, spills); present in 3 |
| EX1          | `abcd` | `abcdabcd` | 2 | **2** | exact: `a`×2 == `b`, no +1 needed |
| EX2          | `abc`  | `abac`     | 2 | **−1** | content mismatch — never appears in the period-3 tiling |
| EX3 (LC ex2) | `a`    | `aa`       | 2 | **2** | `a`×2 == `aa` |

Both methods verified by hand for all four rows. EX0 is the canonical "+1" case,
EX1 the exact case, EX2 the impossible case, EX3 the minimal LC example.

## 6/7. Animation

- §1 insight (`siGenSteps`): on `a="abcd", b="cdabcdab"`. Grow the tiling copy by
  copy. 1 copy is too short; `⌈8/4⌉=2` copies reach length 8 but `b` starts at
  offset 2 and **spills** past the end (dashed phantom cells); a 3rd copy covers
  the offset and `b` matches → 3. Final frame states the ⌈n/m⌉ / +1 / −1 bound.
- §2 brute force (`bfGenSteps`): the **naive unbounded** loop — append one `a`,
  search, repeat. Capped at `⌈n/m⌉+1` for display, with narration that the naive
  version has *no* stopping rule and would append forever on an impossible `b`
  (TLE). Motivates the bound.
- §6 code-viz (`cvGenSteps`): the bounded C++ walked line by line — compute
  `k=⌈n/m⌉`, build `k` copies, `find`, append one more, `find`, else `−1` — with
  variable cards (m / n / k / |s| / found) and the tiled strip below.
- §7 dry run (`drGenSteps`): the oracle. Try `k` copies (search), then `k+1`,
  emitting the matched window when found; the terminal step carries `result` = the
  integer answer (deep-compared to EX answer). All four examples, incl. the −1 case.

## Complexity

- Time: O(m + n) — building `⌈n/m⌉+1 ≈ n/m + 1` copies is O(n + m) characters, and
  one substring search is O(m + n) with a linear matcher. Independent of how large
  a hypothetical unbounded loop could grow.
- Space: O(m + n) — the repeated string `s` (length ≤ n + 2m) plus `b`.
