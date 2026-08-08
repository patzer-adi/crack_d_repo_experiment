# Algorithm Lesson Design

**Status:** Active contract (PLAN-027, 2026-08-05). Supersedes the PLAN-014 placeholder,
which was never written.

An algorithm lesson teaches a canonical CS algorithm. It lives at
`algorithms/<id>/lesson.html`, where `<id>` is the `id` field in
[`data/algorithms.json`](../../data/algorithms.json).

---

## 1. It is the LC chassis, not a new one

An algorithm lesson is the **same 13-section document** as an LC lesson: same section
order, same markers, same four animation generators, same canonical ids and handlers.
Read [`lessons/LESSON_DESIGN.md`](../../lessons/LESSON_DESIGN.md) and its
`design/sec<N>_*.md` files under the same load-on-demand rule — they are the spec for
every section. This file only records what is **different**.

Reusing the chassis is what makes the three quality gates apply unchanged, which is
the only reason an algorithm lesson can be verified at all.

`algorithms/<id>/` sits at the same depth as `lessons/<slug>/`, so `../../static/…`
asset paths work verbatim.

## 2. The four differences

### 2.1 Two extra shared assets

```html
<link rel="stylesheet" href="../../static/lesson.css">
<link rel="stylesheet" href="../../static/algo.css">
...
<script src="../../static/lesson.js"></script>
<script src="../../static/algo.js"></script>
```

[`static/algo.js`](../../static/algo.js) provides `gvPaint` (node-link graph),
`dpPaint` (DP table) and `stripPaint` (chip row for a per-node array); the matching
classes are in [`static/algo.css`](../../static/algo.css) and indexed in
[`static/CLASSES.md`](../../static/CLASSES.md). **Do not hand-roll SVG in a lesson**
and do not restyle `.gv-*` / `.dp-*` locally — that is exactly the drift the shared
file exists to prevent. A lesson-specific `<style>` block is for genuinely one-off
markup only.

Each lesson still owns a small `gDraw(conId, exIdx, st)` adapter that maps *its* step
objects onto `gvPaint`'s `nodeCls` / `edgeCls` / `labels` arrays. That mapping is
algorithm-specific and belongs in the lesson.

### 2.2 Header

No LC number, no difficulty. Show where the algorithm sits and what it costs:

```html
<div class="header">
  <p class="header-eyebrow">Algorithm Lesson</p>
  <h1>Breadth-First Search (BFS)</h1>
  <div class="header-meta">
    <span class="badge badge-arr">Graph Algorithms</span>
    <span class="badge badge-med">Tier 1 · primer</span>
    <span class="badge badge-arr">O(V + E) time · O(V) space</span>
  </div>
</div>
```

Category, tier and complexity are copied from `data/algorithms.json` — never invented.
Tier 1 = primer, 2 = core, 3 = advanced.

### 2.3 §5 carries two languages

C++ under `id="code-main"` (the version §6 animates, and the one to write in an
interview), then a second reveal button with the Python version under `id="code-py"`.
Python is there so the reader can see the shape without the type noise. Both must be
the *same* algorithm — if they diverge, the lesson is wrong.

### 2.4 §12 points back into the practice set

"Related problems" becomes **LeetCode problems that are this algorithm**, taken from
the entry's `related_lc` field where possible. Reference material should hand the
reader back to something they can actually solve.

## 3. Section map, adapted

| § | LC framing | Algorithm framing |
|---|---|---|
| 0 | Clarifying questions | **Preconditions.** What must be true for this algorithm to apply — negative weights, directedness, connectivity, acyclicity. Getting one wrong is how people pick the wrong algorithm. |
| 1 | The insight | The one idea that makes it work, carried by an animated visual. |
| 2 | Brute force | The naive method this algorithm beats, with a live cost counter. |
| 3 | Translations | The named steps from naive to this algorithm. |
| 4 | Plain English | 4–6 steps, verbs bolded. |
| 5 | Code | C++ then Python (§2.3). |
| 6 | Code visualization | Line-by-line over the C++. |
| 7 | Dry run | **The oracle.** See §4. |
| 8 | Corner cases | Where it silently breaks, and the classic implementation bugs. |
| 9 | Production readiness | Overflow, data-structure choice, iterative-vs-recursive, API contract. |
| 10 | Approaches | Sibling algorithms and when to reach for each. |
| 11 | Complexity | Derived, not asserted — say *why* the bound is what it is. |
| 12 | Take home | LC problems that are this algorithm (§2.4). |

## 4. Correctness — the non-negotiable part

Identical to the LC contract in
[`lessons/design/sec7_dry_run.md`](../../lessons/design/sec7_dry_run.md), plus one
extra rule.

- `const EX = [{ <inputs>, answer }, …]` with **hand-derived** answers.
- `drGenSteps` is the oracle; its terminal step carries `result` deep-equal to `answer`.
- All generators pure — no DOM. Helpers must be inlined inside the generator.

**The extra rule: `verify.py` must use a different algorithm, not the same one
retyped.** The point of the independent reference is to catch a wrong *idea*, and two
copies of one idea agree even when the idea is wrong. Worked examples:

| Lesson | Oracle (`drGenSteps`) | Independent reference (`verify.py`) |
|---|---|---|
| BFS | queue, ring by ring | Bellman-Ford relaxation to a fixpoint |
| Dijkstra | priority-queue relaxation | Bellman-Ford |
| Kruskal | sort edges + union-find | Prim's, growing from one node |
| LIS | patience/binary-search | O(n²) DP scan |

Record the choice in `plan.md` under `## 8. Independence`.

## 5. Gates

Every lesson must pass all three before `lesson_status` is flipped. The target takes
an **`algo:` prefix** — mandatory, because `edit-distance` and `binary-search` are both
a `problems.json` slug *and* an `algorithms.json` id, so a bare name would gate the
wrong file:

```bash
node   scripts/verify_animation.mjs algo:<id>   # ≥1 verified, 0 WRONG, 0 unverifiable
python3 scripts/lint_lesson.py      algo:<id>   # 0 fail
node   scripts/render_check.mjs     algo:<id>   # no JS error, every §6 step lights a line,
                                                # no overflow at 1000px or 390px
```

Then, and only then:

```jsonc
// data/algorithms.json
"lesson_status": "generated",
"lesson_path": "algorithms/<id>/lesson.html"
```

`scripts/audit_lessons.py` sweeps both corpora. No algorithm lesson may be added to
`scripts/audit_baseline.json` — that list grandfathers pre-PLAN-019 drift and only
ever shrinks. This corpus is new, so it is clean from birth or it does not ship.

## 6. Three rules that bite

Learned the hard way, recorded so they are not rediscovered 30 times:

- **§1 kernel length.** With the visual-led §1 (no chain-box), the longest
  `<p class="body">` in §1 must be **180–350 characters**. Over 350 the linter reads
  it as dumping the algorithm instead of describing the idea.
- **§1 needs ≥ 30 lines of visual before the `infobox success`**, and ≥ 45 lines total.
- **No module-level helper may be called from a generator.** The verifier extracts
  each `*GenSteps` function *alone* and runs it in a bare sandbox, so a shared
  `const DIRS = [...]` or a helper function defined outside it throws
  `X is not defined` and the lesson reports **unverifiable**. Inline every constant
  and helper inside each generator, even at the cost of repeating it four times.
  (Caught on `algo:a-star`; the same trap is noted in the LC contract.)

## 7. Scaffolding

```bash
python3 scripts/new_algorithm.py <id>     # writes algorithms/<id>/plan.md
```

Then author `plan.md` (metadata, an `Archetype:` line, `## 1. Clarifying`, the
hand-derived example table, and `## 8. Independence`), `verify.py`, and `lesson.html`.

## 8. Reference golden

[`algorithms/bfs/`](../bfs/) — first lesson built to this contract, all three gates
clean. Use it for the chassis; re-derive the pedagogy per algorithm rather than
copying its prose.
