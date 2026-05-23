# Lesson archetypes — canonical golden lookup

When authoring a new lesson, classify the problem against this table and load **only the matching golden** for reference excerpts. Do not load all four.

## Archetype table

| Archetype | Pattern | Canonical golden | Use when the problem … |
|---|---|---|---|
| `two_pointer` | Sort + squeeze | `lessons/3sum/lesson.html` | Asks for a tuple satisfying a sum / comparison condition, with O(n²) or O(n³) brute force and an O(n)/O(n²) sorted two-pointer optimisation. Examples: 3Sum, 4Sum, Two Sum II, Container With Most Water. |
| `sliding_window` | Variable / fixed window + frequency map | `lessons/permutation-in-string/lesson.html` | Asks about a contiguous substring / subarray satisfying a count or sum condition. Often introduces a diff counter to avoid per-step comparison. Examples: Permutation in String, Find All Anagrams, Minimum Window Substring, Longest Repeating Character Replacement. |
| `prefix_scan` | Spatial / monotonic pre-computation | `lessons/trapping-rain-water/lesson.html` | Asks for a value per index that depends on neighbours' min/max/sum, derivable by a two-pass scan or two converging pointers. Examples: Trapping Rain Water, Largest Rectangle in Histogram, Product of Array Except Self. |
| `divide_conquer` | Recursive search / partition | `lessons/median-of-two-sorted-arrays/lesson.html` | Asks for a value across multiple sorted structures, or has an O(log n) target via partitioning. Examples: Median of Two Sorted Arrays, Search in Rotated Sorted Array, Kth Smallest in Sorted Matrix. |

## Classification rule

If the problem fits multiple archetypes (e.g. a sliding-window problem whose optimal solution is a two-pointer squeeze), pick the archetype whose **optimisation insight** is the one being taught. Translations may borrow markup from a second archetype on a case-by-case basis.

## Escape hatch

If no archetype fits (graph BFS, DP table, stack-based parsing, etc.), proceed without an archetype excerpt. Use the section files in `lessons/design/sec<N>_*.md` for principles, and write the problem-specific step generators from scratch. Phase 2 of PLAN-011 will add per-archetype JS step-generator templates; lessons outside the four archetypes will use a `custom_step_generator_js` spec field.

## What to load from the chosen golden

Each `design/sec<N>_*.md` file's **Reference excerpts** section names a line range in each archetype. Open only the matching range. Do not open the full file.

## Provenance

Archetypes were chosen to span the four golden lessons that already exist (`3sum`, `permutation-in-string`, `trapping-rain-water`, `median-of-two-sorted-arrays`). As more lessons are written and new patterns recur, this table will grow — append rows, do not rename existing keys.
