# Section 12 — Take home

## Principle (from v2 §27)

The lesson always ends with **2–4 related problems** that use the same skeleton or pattern. These are not just links — each gets one sentence saying exactly what differs:

```
LC 16 — 3Sum Closest — same skeleton; instead of returning triplets that sum to 0, track the closest sum to a target.

LC 18 — 4Sum — same skeleton with one more nested loop; the inner two-pointer pass is identical.

LC 167 — Two Sum II (Sorted) — the inner pass of 3Sum on its own.
```

This shows the reader how the pattern generalises. It is also the section interview prep students reread most.

## Format

- Each entry is one line: problem identifier, em-dash, what differs.
- Order from closest variant to most distant.
- Two to four entries — never more. A long list dilutes which problems are worth knowing.

## Markup

- Container: `<div class="section">` with `.sec-title` "Take home".
- Inside: `<div class="takehome">` (left blue accent border) containing a `<p>` or `<ul>` of related-problem lines.

## What this section is NOT

- Not a list of every problem with the same DS / tag.
- Not a list of harder variants the reader "should also try."
- Not a list of solutions or hints.

It is a map from this pattern to the small cluster of problems that share it.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 431–445 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 629–643 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 463–end |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 514–527 |
