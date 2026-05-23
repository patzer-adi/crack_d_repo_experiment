# Section 4 — Step 3: Algorithm in plain English

## Principles (from v2 §8, §18)

### Mandatory numbered description in English
Before any code appears, a numbered list of **4–6 sentences** describes exactly what the code does — in the words a candidate would say out loud in an interview.

This section is not a description of the problem. It is a description of the **procedure**.

Example (3Sum):

```
1. Sort the array. This is what makes the inner search O(n).
2. For each index i from 0 to n−3: if nums[i]==nums[i-1], skip. Set L=i+1, R=n−1.
3. While L < R: compute sum = nums[i]+nums[L]+nums[R].
4. If sum < 0: L++. If sum > 0: R--. If sum == 0: record, skip duplicates, squeeze.
5. Return the collected triplets.
```

### Placement: before the code visualization, not after
The code visualisation is not a substitute for the plain-English description — they serve different purposes. Plain English gives the reader the mental model **first**. The visualisation then animates that mental model executing.

If you describe the algorithm only inside the visualisation's narration, the reader has nothing to scan back to when they lose track. The numbered list is that anchor.

## Markup

- Container: `<div class="algo-steps">` (border, rounded corners).
- One `<div class="algo-step">` per numbered line.
- Each `.algo-step` has `.algo-n` (line number in monospace) + `.algo-t` (sentence). Use `<b>` inside `.algo-t` to emphasise key verbs (sort, set, while, return).

## Length guidance

- Each step is one sentence. If a step needs two sentences, split into two steps.
- No more than 6 steps. If you have 7, fold two consecutive steps together.
- Begin every sentence with an imperative verb (Sort, Set, While, Compute, Return). Do not use "We …" or "The algorithm …".

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 230–243 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 393–410 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 249–266 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 301–314 |
