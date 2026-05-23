# Two Sum — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `two-sum`
- **LC #:** 1
- **Difficulty:** Easy
- **Topic:** Arrays
- **Archetype:** `custom` — Two Sum's optimisation insight is "swap a linear
  search for an O(1) hash lookup," which is the hash-map archetype, not one of
  the four currently catalogued (`two_pointer`, `sliding_window`, `prefix_scan`,
  `divide_conquer`). The escape hatch in `design/archetypes.md` applies. The
  closest cousin is `two_pointer` (Two Sum II is listed there), but classic
  LC #1 returns *original indices*, which forbids sorting without bookkeeping
  and makes the hash-map approach the canonical solution being taught.

## 1. Clarifying questions (§0)

1. **"Exactly one solution is guaranteed — can I assume that?"**
   *A:* Yes. The problem statement promises exactly one pair sums to target.
   *Unlocks:* No need to track multiple results; return on first hit and stop.

2. **"Can I use the same element twice (i.e., is `i == j` allowed)?"**
   *A:* No. Each index may appear at most once in the answer.
   *Unlocks:* When checking for a complement at index `i`, look at values
   *previously* seen (indices `< i`) — this naturally excludes `i` itself.

3. **"Can the array contain duplicate values?"**
   *A:* Yes — e.g. `[3,3]` with target `6` is valid.
   *Unlocks:* Storing value→index in a map *overwrites* on duplicates, which is
   fine because by the time we overwrite, the earlier index has already been
   used (or never will be — see corner case §8.1).

4. **"Do indices need to be sorted in the output?"**
   *A:* No. Any order is accepted by the judge.
   *Unlocks:* We can return `[seen[complement], i]` directly without reordering.

## 2. Kernel paragraph (§1)

As you walk left-to-right through the array, at index `i` you are asking one
question: *"is there some index `j < i` where `nums[j] = target − nums[i]`?"*
A linear scan of the prefix answers that in O(n), giving the O(n²) brute force.
But the question only ever asks **"have I seen value `c` already, and at what
index?"** That is exactly what a hash map answers in O(1). So: maintain a
`value → index` map of everything seen so far; at each `i`, first probe for
`target − nums[i]`, then insert `nums[i]`. The check-then-insert order is what
guarantees we never pair an element with itself.

## 3. Foundational concept visual (§1)

A horizontal strip of array cells with a small "seen map" panel beside it.
As a pointer `i` walks right, each visited cell drops a `(value → index)` pill
into the seen-map panel. On step where `target − nums[i]` already sits in the
panel, that pill gets a highlight ring and an arrow connects it back to the
current `i`. This makes visible the asymmetry the algorithm exploits: we only
ever look *backward*, never forward — which is why one pass suffices.

## 4. Translations (§3)

(Folded from three to two on plan-review feedback: the original Translation 3
named only a correctness/cleanliness gain — no distinct complexity step — so
the "one pass, check-before-insert" detail now lives inside Translation 2.)

1. **Pair search → complement search.**
   Instead of asking "is there some pair `(i,j)` with `nums[i]+nums[j]=target`?",
   ask the equivalent: "for the current `nums[i]`, has the value `target−nums[i]`
   appeared earlier?" Same answer, but now we walk the array once and do a
   *lookup* at each step rather than a *pair check*.
   Gain: O(n²) pair scan → O(n) outer scan × O(?) per-step lookup.

2. **Linear lookup → hash lookup, in one pass.**
   The per-step lookup ("has value `c` appeared earlier, and at what index?")
   is exactly what a hash map answers in O(1) average. Maintain `value→index`
   of everything *previously* seen; at index `i`, *probe first*, then *insert*.
   Probe-before-insert keeps the map equal to indices `< i`, so an element can
   never match itself — no explicit `i ≠ j` guard needed.
   Gain: per-step lookup O(n) → O(1); total O(n²) → O(n).

## 5. Algorithm in plain English (§4)

1. **Create** an empty hash map `seen` from value to index.
2. **Walk** `i` from `0` to `n−1`.
3. **Compute** `complement = target − nums[i]`.
4. **Probe** `seen` for `complement`. If found, **return** `[seen[complement], i]`.
5. Otherwise, **store** `seen[nums[i]] = i` and continue.
6. The problem guarantees a solution, so the loop always returns before exiting.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example (3–5 steps) — canonical:**
- Input: `nums = [2,7,11,15], target = 9`
- Expected: `[0,1]`
- Path: i=0 stores 2→0. i=1 probes 9−7=2, hits, returns [0,1]. (2 visible
  iterations, ~5 sub-steps total counting state transitions.)

**Slow example (10–15 steps) — 11-element walk, unique pair:**
- Input: `nums = [1, 5, 9, 3, 8, 11, 4, 7, 2, 6, 10], target = 20`
- Expected: `[2, 5]`
- Path: 6 outer iterations (i=0..5), 5 misses + 1 hit. Two dr sub-steps per
  iteration → 12 visible dry-run steps (within 10–15 range; cv has more
  granularity at 28). Crucially, `target = 20` is reached by **exactly one
  pair** in the input — `nums[2]=9 + nums[5]=11 = 20`. This matters because
  the §10 brute-force and §6 hash-map approaches would otherwise return
  *different valid pairs* (LC's "one solution" guarantee permits either) and
  the reader would see the answer change when switching approaches. With a
  unique pair, brute force at `i=2, j=5` and hash-map at `i=5, complement=9`
  return the same indices `[2, 5]` — coherent narrative across all three
  widgets.

**Edge example (dry run) — duplicate values participate in solution:**
- Input: `nums = [3, 3], target = 6`
- Expected: `[0, 1]`
- Path: i=0 stores 3→0. i=1 probes 6−3=3, hits the *earlier* 3, returns [0,1].
  Demonstrates that duplicates are not a problem because check happens before
  insert overwrites.

## Python verification (full trace below — §10)

All three above plus one extra (`[3,2,4], target=6 → [1,2]`) verified.

## 7. Corner cases (§8)

1. **Duplicate values that form the answer** — `nums=[3,3], target=6` →
   `[0,1]`. The check-before-insert order makes this fall out naturally: at
   `i=1` we probe and find `seen[3]=0` before we'd overwrite it.

2. **Same element can't be reused** — guaranteed by the same ordering. At
   `i=0`, `seen` is empty, so `nums[0]` cannot match itself. After inserting,
   we move on; nothing ever queries the map with its own key at its own index.

3. **Negative numbers / negative target** — `nums=[-3,4,3,90], target=0` →
   `[0,2]`. Hashing is value-agnostic; nothing special is needed.

4. **Solution at the last index** — `nums=[3,2,4], target=6` → `[1,2]`. The
   loop processes earlier indices first, so the second member of the pair is
   always the one that triggers the return. Don't write code that "looks
   ahead."

5. **Large array, answer near the front** — early return is mandatory. Do not
   prefill the entire map; that's an O(n) space waste and risks the
   self-matching bug from translation #3.

## 8. Approaches comparison (§10)

**Approach 1 — Brute force (nested loop).**
For each `i`, scan all `j > i` and check `nums[i]+nums[j] == target`.
Time O(n²), space O(1). Conceptually trivial but quadratic; on the 10⁴-size
inputs LC throws at this problem it's still feasible (~10⁸ ops worst case)
but a clear "did you actually think?" signal in an interview.

**Approach 2 — Sort + two pointers (with index bookkeeping).**
Sort the array, then squeeze with `L=0, R=n−1`. Time O(n log n), space O(n).
**Sorting destroys index information**, which is exactly what this problem
asks us to return — so a naive sort-and-squeeze is *wrong*. To recover, sort
pairs `(value, original_index)` and return the stored original indices on
match. (Equivalent framing: this is "what you'd do if the problem returned
*values* — and the hash map is what you do because it returns *indices*.")
Slower than the hash map and clunkier, but worth knowing as the bridge to
Two Sum II (sorted input, O(1) extra space) and to 3Sum.

**Approach 3 — Hash map, one pass (winning approach).**
Maintain `value → index` of values seen so far; at each `i` probe for the
complement before inserting. Time O(n), space O(n). Optimal time complexity
because we must read every element at least once in the worst case (answer
at the end). The space cost buys us the constant-time complement lookup that
makes the linear time possible.

## 9. Take home (§12)

- **LC #167 Two Sum II — Input Array Is Sorted.** Same question, sorted input,
  indices not required to be original. Hash map still works but is overkill;
  the canonical answer becomes O(1)-space two-pointer squeeze. Teaches that
  "sortedness" is a real algorithmic resource.

- **LC #15 3Sum.** Generalises to triples summing to 0. Brute force is O(n³).
  The optimisation is *not* a hash map — it's sort + two-pointer per fixed
  outer index — because the hash-map approach struggles with duplicate-triple
  deduplication. Shows that the right "translation" depends on the constraints.

- **LC #653 Two Sum IV — Input is a BST.** Same complement question over a
  tree. The hash-map approach ports verbatim (any traversal order works).
  An alternative uses BST in-order traversal + two pointers in O(1) extra
  space (besides the recursion stack). Shows the hash-map technique is
  *data-structure-portable*.

- **LC #1099 Two Sum Less Than K.** Find the maximum sum `< K`. Now we want
  the *largest* qualifying sum, not equality — and the hash-map trick breaks
  because we'd need to query a *range*, not an exact key. Optimal is sort +
  two-pointer. Reinforces *when* hash maps stop being the answer.

## 10. Python verification (BEFORE writing HTML)

Run on 2026-05-14 from `/tmp/two_sum_verify.py` (initial 4) + `/tmp/two_sum_slow2.py`
(slow-example unique-pair check, added after the §6 generators revealed that
target=15 admits two valid pairs and the BF/HM widgets returned different
indices). All examples match expected output. The slow example was changed to
`target=20` (unique pair `(2,5)`) so all three approaches converge on `[2,5]`.

```
=== nums=[2, 7, 11, 15], target=9 ===
  i=0 x=2 complement=7 in_map=False seen={}
     store seen[2] = 0
  i=1 x=7 complement=2 in_map=True seen={2: 0}
  -> match! return [0, 1]
Result: [0, 1]
Expected: [0, 1]

=== nums=[3, 2, 4], target=6 ===
  i=0 x=3 complement=3 in_map=False seen={}
     store seen[3] = 0
  i=1 x=2 complement=4 in_map=False seen={3: 0}
     store seen[2] = 1
  i=2 x=4 complement=2 in_map=True seen={3: 0, 2: 1}
  -> match! return [1, 2]
Result: [1, 2]
Expected: [1, 2]

=== nums=[3, 3], target=6 ===
  i=0 x=3 complement=3 in_map=False seen={}
     store seen[3] = 0
  i=1 x=3 complement=3 in_map=True seen={3: 0}
  -> match! return [0, 1]
Result: [0, 1]
Expected: [0, 1]

=== nums=[-3, 4, 3, 90], target=0 ===
  i=0 x=-3 complement=3 in_map=False seen={}
     store seen[-3] = 0
  i=1 x=4 complement=-4 in_map=False seen={-3: 0}
     store seen[4] = 1
  i=2 x=3 complement=-3 in_map=True seen={-3: 0, 4: 1}
  -> match! return [0, 2]
Result: [0, 2]
Expected: [0, 2]
```

Source script (kept for re-run on algorithm changes):

```python
def verify(nums, target, expected):
    print(f"\n=== nums={nums}, target={target} ===")
    seen = {}  # value -> index
    result = None
    for i, x in enumerate(nums):
        complement = target - x
        in_map = complement in seen
        print(f"  i={i} x={x} complement={complement} in_map={in_map} seen={seen}")
        if in_map:
            result = [seen[complement], i]
            print(f"  -> match! return [{seen[complement]}, {i}]")
            break
        seen[x] = i
        print(f"     store seen[{x}] = {i}")
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    assert result == expected, f"MISMATCH: got {result}, want {expected}"

verify([2,7,11,15], 9, [0,1])
verify([3,2,4],     6, [1,2])
verify([3,3],       6, [0,1])
verify([-3,4,3,90], 0, [0,2])
verify([1,5,9,3,8,11,4,7,2,6,10], 20, [2,5])  # slow-lesson example
```

Slow-example unique-pair check (run separately, output shown below):

```
target=20 unique-pair check: pairs=[(2, 5)]
=== nums=[1, 5, 9, 3, 8, 11, 4, 7, 2, 6, 10], target=20 ===
  i= 0 x=  1 c= 19 hit=False |seen|=0
  i= 1 x=  5 c= 15 hit=False |seen|=1
  i= 2 x=  9 c= 11 hit=False |seen|=2
  i= 3 x=  3 c= 17 hit=False |seen|=3
  i= 4 x=  8 c= 12 hit=False |seen|=4
  i= 5 x= 11 c=  9 hit=True |seen|=5
  -> return [2, 5]
```
