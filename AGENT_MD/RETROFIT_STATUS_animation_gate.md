# Retrofit status — animation correctness gate (step b)

_Last updated: 2026-05-30_

This file tracks the in-progress work to make every lesson pass the animation
**correctness** gate (`scripts/verify_animation.mjs`, surfaced in
`scripts/lint_lesson.py` as `§animation:correct`). It is the "b" of the agreed
**a → b → c** plan:

- **a (done):** build the correctness gate + codify the contract + wire it into
  the linter.
- **b (in progress — this file):** retrofit every existing generated lesson so
  it passes the gate.
- **c (not started):** rewrite `.claude/commands/batch-lesson.md` for autonomy
  (drop the manual PAUSE, wire lint+verify as hard gates, bounded auto-retry).

## What the gate actually checks

For a lesson, it runs the **pure dry-run step-generator** (the oracle)
headlessly in a Node `vm` over the lesson's declared examples, and asserts the
terminal step's answer **equals an independently-declared ground-truth answer**.

> The ground truth must be *independent* of the generator's own output. If the
> "expected" answer is just whatever the generator computes, the gate is a
> tautology and cannot catch a numerically-wrong animation — which is the single
> worst failure mode (polished, uniform, WRONG). When authoring answers, compute
> them by hand / brute force, not by copying the generator's result.

## Two authoring conventions exist in the corpus

The verifier (as of the `gate: support both dry-run conventions` commit) handles
**both**:

- **Convention A** — `function drGenSteps(args)` driven by `const EX` (or, in
  most A lessons, `const EXAMPLES`). Newer style. Some A generators destructure
  their single arg (`drGenSteps({nums})`); the verifier passes the whole example
  object for those.
- **Convention B** — `function drGen(ex)` driven by `const EXAMPLES`. Older
  style; `drGen` takes the whole example object. The terminal "done" step
  usually already computes the answer in a named field (e.g. two-sum `ans`,
  trapping-rain-water `water`) but does not expose it as `result`.

Oracle selection: `drGenSteps` if present, else `drGen`.

## The retrofit recipe (per lesson)

1. Run `node scripts/dump_terminal.mjs <slug>` — prints each example's inputs and
   the terminal step's fields. Identify which field holds the answer.
2. Make the terminal step expose `result: <answerVar>`:
   - Convention B: add `result: <answerVar>` to the object the `snap(...)`
     closure pushes (one additive line; every step gets it, only the last is
     checked). e.g. two-sum → `result: ans`; trapping-rain-water → `result: water`.
   - Convention A: ensure the terminal `phase:'done'` step carries
     `result: <finalValue>` (house-robber added `result: prev1`).
3. Add an independent ground-truth `answer:` to each example object
   (in `EX`/`EXAMPLES`).
4. **Verify before claiming done:** `node scripts/verify_animation.mjs <slug>`
   must print `N verified, 0 WRONG, 0 unverifiable` and exit 0. Never commit a
   lesson as green without this.
5. Commit in small verified batches.

## Per-lesson status

Source: `scripts/dump_terminal.mjs` + the analyzer sweep on 2026-05-30. Impurity
only blocks the gate when it is the **oracle** generator that is impure (si/cv/bf
impurity is tolerated — the verifier only runs the oracle).

| slug | conv | oracle sig | terminal answer field | oracle pure? | status |
|------|------|-----------|----------------------|--------------|--------|
| house-robber | A | drGenSteps(nums) | result (prev1) | yes | **PASS** ✅ |
| two-sum | B | drGen(ex) | ans | yes | TODO |
| trapping-rain-water | B | drGen(ex) | water | yes | TODO |
| 3sum | B | drGen(ex) | _dump_ | yes | TODO |
| best-time-to-buy-and-sell-stock-with-cooldown | B | drGen(ex) | _dump_ | yes | TODO |
| container-with-most-water | B | drGen(ex) | _dump_ | yes | TODO |
| count-permutations-with-inversion-requirement | B | drGen(ex) | _dump_ | yes (si impure, ok) | TODO |
| maximum-subarray | B | drGen(ex) | _dump_ | yes (si impure, ok) | TODO |
| median-of-two-sorted-arrays | B | drGen(ex) | _dump_ | yes | TODO |
| merge-intervals | B | drGen(ex) | _dump_ | yes | TODO |
| move-zeroes | B | drGen(ex) | _dump_ | yes | TODO |
| product-of-array-except-self | B | drGen(ex) | _dump_ | yes | TODO |
| two-sum-ii-input-array-is-sorted | B | drGen(ex) | _dump_ | yes | TODO |
| house-robber-ii | A | drGenSteps(nums) | needs result | yes | TODO (has EX, add result) |
| coin-change | A | drGenSteps(coins, amount) | _dump_ | yes | TODO |
| find-the-duplicate-number | A | drGenSteps(nums) | _dump_ | yes | TODO |
| first-missing-positive | A | drGenSteps(nums) | _dump_ | yes | TODO |
| majority-element | A | drGenSteps({nums}) | _dump_ | yes | TODO |
| majority-element-ii | A | drGenSteps({nums}) | _dump_ | yes | TODO |
| maximum-product-subarray | A | drGenSteps(nums) | _dump_ | yes (bfGenSteps impure, ok) | TODO |
| repeated-substring-pattern | A | drGenSteps({s}) | _dump_ | yes | TODO |
| spiral-matrix | A | drGenSteps(matrix) | has result | yes | TODO (add EX[].answer) |
| valid-palindrome | A | drGenSteps(input) | _dump_ | yes | TODO |
| longest-repeating-character-replacement | A | drGenSteps(s, k) | _dump_ | **NO — drGenSteps impure** | TODO (refactor oracle to pure first) |
| permutation-in-string | A | drGenSteps({s1,s2}) | _dump_ | **NO — drGenSteps impure** | TODO (refactor oracle to pure first) |
| sliding-window-maximum | A | drGenSteps(nums, k) | _dump_ | **NO — drGenSteps impure** | TODO (refactor oracle to pure first) |

`_dump_` = run `dump_terminal.mjs <slug>` to read the exact answer field before editing.

### The 3 hard cases (impure oracle)

`longest-repeating-character-replacement`, `permutation-in-string`, and
`sliding-window-maximum` have an **impure dry-run generator** (it touches the
DOM). These cannot be verified headlessly until the generator is split into a
pure step-generator (`*GenSteps` returns plain state objects) + a separate
renderer (`*Render` does the DOM). Do this refactor first, confirm the animation
still renders identically in a browser, then apply the recipe.

## Environment note (2026-05-30)

This session ran under a severely degraded tool-output pipeline (reads/greps
frequently returned empty or lag-duplicated output). Per-file HTML surgery under
those conditions is unsafe — it is the exact condition that previously produced a
commit whose message claimed edits that had silently failed. The infrastructure
(verifier two-convention support, lint regression fix, `dump_terminal.mjs`) was
completed and committed; the per-lesson retrofits were deferred to a reliable
session rather than risk blind edits. **Discipline: re-run the verifier and
confirm `0 WRONG, 0 unverifiable` before marking any lesson PASS or committing.**
