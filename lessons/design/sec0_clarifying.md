# Section 0 — Before you code (Clarifying questions)

## Principle (from v2 §4)

This section is not "facts about the problem." It is "the questions you would ask in an interview, and what each answer unlocks." Treat it as an interview script, not a FAQ.

## Format

Each question card has three parts:

```
Q: Can s1 have duplicate characters?
A: Yes — e.g. s1="aab" requires exactly 2 a's and 1 b in the window.
→ unlocks: need counts, not just presence
```

The `→ unlocks:` line is **mandatory**. It shows the reader why the question matters — what design decision the answer enables.

## Count

Four questions per problem is the right number. Fewer feels thin; more dilutes.

## Markup

- `<div class="asgrid">` wraps four `<div class="acard">`.
- Each `.acard` contains `.acard-q` (question), `.acard-a` (answer), `.acard-u` (unlock line, monospace green).
- After the grid: optional `<div class="infobox">` titled "Assumptions we carry forward" summarising what was decided. One short paragraph.

## Pitfalls

- The unlock line cannot be a restatement of the answer. It must name a design consequence.
- Do not ask questions whose answer is "given in the problem statement." Ask questions whose answer changes the algorithm.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 21–52 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 127–159 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 81–113 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 69–101 |

Open only the matching archetype's range.
