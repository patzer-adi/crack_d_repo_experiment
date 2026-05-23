# Section 1 — The Insight

## Principles (from v2 §1, §2, §3, §7)

### Single-paragraph kernel
One infobox paragraph dense enough that the algorithm is derivable from it. Place it **before** brute force when the problem has a clean single insight (3Sum: "fix one number, squeeze two pointers"). Place it **after** brute force when the cost of the naive approach needs to be felt first (Permutation in String: the diff counter only makes sense once you've seen why per-step comparison is wasteful).

### Foundational concept first — not the algorithm
Before any algorithm is mentioned, establish what the problem is really asking in computational terms. A separate visual section that comes **before** the kernel.

- **Permutation in String**: "ba" is a permutation of "ab" because same counts, different order — three-column visual (s1 / permutation / non-permutation) with frequency badges, before sliding windows.
- **Trapping Rain Water**: single annotated histogram with maxL wall, maxR wall, water level between them, before two pointers.
- **3Sum**: sorted array with a fixed element and two inward-moving pointers on a concrete example, before describing the algorithm.

Test: could a reader who doesn't know the algorithm understand what the section is showing? If yes, it's the right foundational concept. If it requires knowing the algorithm first, it's not a concept visual — it's a code explanation.

### Lead with a picture, then formalize
Mental model first, formula second. The water formula `water[i] = min(maxL, maxR) - h[i]` is introduced with an annotated bar chart showing exactly those values, then the formula appears in a green infobox underneath. If the picture comes after the formula, the formula feels like a definition to memorise rather than something that falls out of what you can see.

### Equivalence chain — every ≡ line gets a concrete pill example
When reducing the problem through equivalent formulations, each step shows a concrete example of what that equivalence looks like — not just symbols:

```
≡  freq_s1[c] == freq_win[c]  for every character c
   [pill: freq_s1: a=1 b=1 rest=0] [vs] [pill: freq_win("ba"): a=1 b=1 rest=0] [→] [pill green: all 26 slots match ✓]
   [pill: freq_win("cd"): c=1 d=1 rest=0] [→] [pill red: a-slot: 0≠1, b-slot: 0≠1 ✗]
```

Symbols alone do not teach. The pill examples are what turn a symbol chain into an insight.

## Markup

- Section title: `<p class="sec-label">The Insight</p>` + `<p class="sec-title">…</p>`
- Foundational visual: any combination of `.number-line` (sorted arrays), bar charts, frequency badges — sized to fit without horizontal scroll.
- Kernel: `<div class="infobox success">` with `.infobox-t` ("The kernel") + `.infobox-d`.
- Equivalence chain: `<div class="chain-box">` with `.chain-row` rows; each row has `.chain-sym` + `.chain-content` containing `.chain-text` and `.chain-example` (pills via `.pill`, `.pill.ok`, `.pill.bad`).

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 54–143 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 160–250 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 114–162 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 102–214 |

Also load `design/known_bugs.md` (the diff-inversion warning applies when the kernel introduces a diff counter).

## Acceptance criteria (machine-checkable)

These rules are enforced by `scripts/lint_lesson.py` (PLAN-016). A §1 that fails any MUST is blocked from `lesson_status=generated`. SHOULD/MUST NOT items emit warnings.

§1 **MUST** contain (hard checks):

| Rule | What lint looks for |
|---|---|
| Sec-label present | exactly one `<p class="sec-label">The Insight</p>` |
| Sec-title present | exactly one `<p class="sec-title">…</p>` |
| Kernel paragraph | at least one `<p class="body">` whose text length ≥ 180 chars |
| Kernel infobox | exactly one `<div class="infobox success">` block |
| Foundational structure | EITHER a `<div class="chain-box">` with ≥ 3 `<div class="chain-row">` children, with ≥ 2 of those rows containing a `<div class="chain-example">` — OR a foundational visual block ≥ 30 lines positioned **before** the `infobox success` AND a kernel paragraph ≤ 350 chars (so the conceptual heavy-lifting is in the visual, not the kernel) |
| Line-count floor | §1 total line count ≥ 45 (trapping-rain-water sits at 49; floor accommodates visual-led prefix-scan style) |

§1 **MUST NOT** (soft warnings — do not block):

| Rule | Why |
|---|---|
| sec-title starts with "Use X as Y" or "Traverse N <thing>" | These are algorithm descriptions, not foundational concepts. The principle "Foundational concept first — not the algorithm" is violated. |
| Kernel paragraph reads as restating the algorithm steps | Lint detects via heuristic: kernel paragraph that contains "Iterate", "Loop", "First pass / Second pass" as its first word triggers a warning. |

### Why these thresholds

- **180 char kernel paragraph:** The four goldens' kernel paragraphs measure 186–283 chars; permutation-in-string sits at 188 and median-of-two-sorted-arrays at 186. The 180 floor accommodates all four goldens while still catching the severely-drifted lessons (whose §1 paragraphs are 80–150 chars).
- **chain-box OR ≥30-line visual:** trapping-rain-water uses a visual-led §1 (no chain-box). Both teaching modes are valid; lint accepts either.
- **Line count ≥ 45:** trapping-rain-water §1 is 49 lines (the smallest golden §1). Setting the floor at 45 leaves 4 lines of slack while still rejecting the drifted lessons (the highest drift case is 45 lines exactly — find-the-duplicate-number — so a floor of 45 may need adjustment to 50 if that lesson should fail).

---

## §1 animation conventions (PLAN-017)

Every §1 foundational visual must be **animated with reader controls**, not a static multi-frame diagram. The reader steps through the algorithm at their own pace via prev/auto/next/reset buttons. Convention mirrors §6/§7 but with a slower default speed and a shorter step count (§1 builds intuition; brevity matters).

### Required markup

| Element | Convention |
|---|---|
| Control row | `<div class="ctrl-row">` containing `← Prev`, `▶ Auto`, `Next →`, `↺ Reset` buttons calling `siPrev()` / `siTogglePlay()` / `siNext()` / `siReset()` |
| Play button id | `id="si-bplay"` so `siTogglePlay` can toggle the label between `▶ Auto` and `⏸ Pause` |
| Step counter | `<span class="step-ctr" id="si-sctr"></span>` shows `step N / M` next to the controls |
| State display | Per-archetype DOM elements (rows of cells, frequency badges, partition diagram, histogram) that `siRender(st)` updates in place |

### Required JS

| Element | Convention |
|---|---|
| Step generator | `function siGenSteps(input) → array of step objects` — pure function, no DOM access |
| Renderer | `function siRender(st)` — reads `st`, writes DOM. No state changes. |
| Navigation | `siNext()`, `siPrev()`, `siReset()` — standard pattern (see archetype templates below) |
| Auto-mode | `siTogglePlay()` running at **1400 ms** per step (uniform with bf/cv/dr) |
| Initial render | `siRender(siSteps[0])` called once at end of `<script>` |

### Step count target

§1: **4–9 steps**. Fewer than 4 doesn't reveal the dynamic; more than 9 turns intuition into a lecture. Use one step per "decision point" the algorithm makes; not every loop iteration needs a frame.

Per archetype defaults:
- two_pointer: one step per pointer move (typically 6–8)
- sliding_window: one step per window slide (typically 5–7)
- prefix_scan: one step per index of the canonical example (5–9 depending on example length)
- divide_conquer: one step per partition adjustment (typically 4–6)

### Why 1400 ms (uniform)

User-validated speed (set 2026-05-21). 1400 ms gives readers enough time to absorb each step's state change without the rapid-fire feel of the original 300 ms brute-force speed. Same value across bf/cv/dr/si so readers don't have to recalibrate between sections.

---

## Acceptance criteria addendum (animation, PLAN-017)

In addition to the structural criteria above, §1 MUST contain (hard checks):

| Rule | What lint looks for |
|---|---|
| Animation controls present | At least 3 of `siNext()`, `siPrev()`, `siTogglePlay()`, `siReset()` referenced from button onclick handlers in §1 |
| Step generator defined | `function siGenSteps` defined somewhere in the lesson (typically just below §1 markup) |

Legacy goldens (`3sum`, `permutation-in-string`, `trapping-rain-water`, `median-of-two-sorted-arrays`) predate this convention and lint emits a **warning** (not failure) for them; they backfill in a future plan.

---

## Canonical pattern — two-pointer archetype

Source: lifted from `lessons/3sum/lesson.html` lines 54–143 (snapshot 2026-05-19).

This is the full markup pattern. When authoring §1 of a two-pointer lesson, copy this skeleton and replace problem-specific tokens. Keep the structure: kernel paragraph → foundational visual (number-line, 2-step) → kernel infobox → chain-box with 4 rows (problem → 2-var reduction → sort+squeeze → dedup).

```html
<!-- ═══ SECTION 1: THE INSIGHT ═══ -->
<div class="section">
  <p class="sec-label">The Insight</p>
  <p class="sec-title">[INSIGHT NOT ALGORITHM — e.g. "Fix one number. Find a pair that sums to its negation."]</p>

  <p class="body">[KERNEL PARAGRAPH — re-state the problem, then the reduction. Include the algebraic transformation if any (e.g. <code>a+b+c=0 → b+c=−a</code>). 280–540 chars target.]</p>

  <!-- Insight visual: two-step number-line showing the squeeze -->
  <div style="margin:1.25rem 0">
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:11px;color:var(--text3);margin-bottom:.5rem">[SETUP CAPTION: input · fixed element · target]</div>
    <div class="number-line">
      <!-- step 1 cells with .nl-num .fixed/.ptr-l/.ptr-r markers -->
    </div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text2);margin:.5rem 0">
      [STEP 1 ACTION: sum=… → pointer move] <span style="color:var(--text3)">// [WHY]</span>
    </div>
    <div class="number-line">
      <!-- step 2 cells, one pointer moved -->
    </div>
    <div style="font-family:var(--mono);font-size:12px;color:var(--text-success);margin:.5rem 0">
      [STEP 2 RESULT: match found / continued squeeze]
    </div>
  </div>

  <div class="infobox success">
    <p class="infobox-t">The kernel</p>
    <p class="infobox-d">[ONE-PARAGRAPH ALGORITHM SUMMARY — dense enough that the algorithm is derivable from it.]</p>
  </div>

  <!-- Equivalence chain -->
  <p class="body" style="margin-top:1rem">Why [CORE TECHNIQUE — e.g. "sorting"] is the key that unlocks everything:</p>
  <div class="chain-box">
    <div class="chain-row">
      <span class="chain-sym"></span>
      <div class="chain-content">
        <div class="chain-text">[THE PROBLEM, in its raw form]</div>
        <div class="chain-note">the problem</div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text">[FIRST REDUCTION — e.g. 3-var → 2-var]</div>
        <div class="chain-note">[WHY THIS REDUCTION IS VALID]</div>
        <div class="chain-example">
          <span class="pill n">[CONCRETE INPUT]</span><span class="arrow">→</span>
          <span class="pill n">[CONCRETE OUTPUT of the reduction]</span>
        </div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text">[SECOND REDUCTION — e.g. "sort first → two-pointer squeeze"]</div>
        <div class="chain-note">[COMPLEXITY GAIN / WHY THIS WORKS]</div>
        <div class="chain-example">
          <span class="pill n">[CONDITION A]</span><span class="arrow">→</span><span class="pill n">[ACTION A]</span>
          <span style="margin:0 4px;color:var(--text3)">·</span>
          <span class="pill n">[CONDITION B]</span><span class="arrow">→</span><span class="pill n">[ACTION B]</span>
          <span style="margin:0 4px;color:var(--text3)">·</span>
          <span class="pill ok">[SUCCESS CONDITION]</span>
        </div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text"><span class="chain-hl">[THE CORRECTNESS-CRITICAL DETAIL]</span> [e.g. "skip duplicates at both loops"]</div>
        <div class="chain-note">[WHY IT'S BAKED IN, NOT POST-PROCESSING]</div>
        <div class="chain-example">
          <span class="pill n">[PRECONDITION]</span><span class="arrow">→</span><span class="pill bad">[SKIP/REJECT]</span>
          <span style="margin:0 4px;color:var(--text3)">·</span>
          <span class="pill n">[POSTCONDITION]</span><span class="arrow">→</span><span class="pill ok">[GUARANTEED OUTCOME]</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

**Field count to imitate:** kernel paragraph ≥ 200 chars, 2-step visual ≥ 20 lines, chain-box with 4 rows, ≥ 2 chain-examples. Final §1 line count target: 85–95 (3sum is 90).

---

## Canonical pattern — sliding_window archetype

Source: lifted from `lessons/permutation-in-string/lesson.html` lines 160–250 (snapshot 2026-05-19).

This archetype teaches via a **frequency-badge visual** (showing same-counts-different-order) before introducing the window mechanic. The chain-box reduces from "is permutation?" through "frequency counts match" to "diff counter tracks delta in O(1) per step".

```html
<!-- ═══ SECTION 1: THE INSIGHT ═══ -->
<div class="section">
  <p class="sec-label">The Insight</p>
  <p class="sec-title">[INSIGHT NOT ALGORITHM — e.g. "Same character counts, any order. Maintain a window; track only the delta."]</p>

  <p class="body">[KERNEL PARAGRAPH — define what "permutation" / "window-property" means in counts. Mention that comparing counts at every step is O(26) and the diff counter eliminates that.]</p>

  <!-- Foundational visual: three-column frequency badges -->
  <div style="margin:1.25rem 0">
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem">
      <!-- column 1: s1 -->
      <div>
        <div class="freq-label">[LABEL — e.g. s1 = "ab"]</div>
        <div class="freq-row">
          <span class="freq-badge">a:1</span><span class="freq-badge">b:1</span>
        </div>
      </div>
      <!-- column 2: a permutation (✓) -->
      <div>
        <div class="freq-label">[PERMUTATION example: "ba"]</div>
        <div class="freq-row">
          <span class="freq-badge ok">a:1</span><span class="freq-badge ok">b:1</span>
        </div>
        <div class="freq-verdict ok">[verdict: same counts → permutation ✓]</div>
      </div>
      <!-- column 3: not a permutation (✗) -->
      <div>
        <div class="freq-label">[NON-PERMUTATION example: "cd"]</div>
        <div class="freq-row">
          <span class="freq-badge bad">c:1</span><span class="freq-badge bad">d:1</span>
        </div>
        <div class="freq-verdict bad">[verdict: a/b counts mismatch ✗]</div>
      </div>
    </div>
  </div>

  <div class="infobox success">
    <p class="infobox-t">The kernel</p>
    <p class="infobox-d">[ONE-PARAGRAPH ALGORITHM SUMMARY — slide a window of size |s1| across s2; maintain a frequency map of window contents; track a diff counter that increments/decrements when a character moves toward or away from its target count. Answer is yes whenever diff == 0.]</p>
  </div>

  <!-- Equivalence chain -->
  <p class="body" style="margin-top:1rem">Why a diff counter beats per-step comparison:</p>
  <div class="chain-box">
    <div class="chain-row">
      <span class="chain-sym"></span>
      <div class="chain-content">
        <div class="chain-text">[THE PROBLEM — "is any window a permutation of s1?"]</div>
        <div class="chain-note">the problem</div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text">freq_s1[c] == freq_win[c] for every character c</div>
        <div class="chain-note">[restate "permutation" in count terms]</div>
        <div class="chain-example">
          <span class="pill n">[freq_s1: a=1 b=1 rest=0]</span>
          <span class="pill ok">[freq_win("ba"): a=1 b=1 → all match ✓]</span>
          <span class="pill bad">[freq_win("cd"): a-slot 0≠1 ✗]</span>
        </div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text">[REDUCE COMPARISON COST — maintain a diff counter that already encodes "how many slots are mismatched"]</div>
        <div class="chain-note">comparing 26 slots every step is wasteful; diff goes from O(26) to O(1) per step</div>
        <div class="chain-example">
          <span class="pill n">char enters window</span><span class="arrow">→</span><span class="pill n">freq_win[c]++</span><span class="arrow">→</span><span class="pill ok">diff adjusts ±1</span>
        </div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text"><span class="chain-hl">diff == 0 ⟺ window is a permutation of s1</span></div>
        <div class="chain-note">[the invariant that makes it O(n) total]</div>
        <div class="chain-example">
          <span class="pill n">[walk through one slide showing diff transition]</span>
          <span class="pill ok">diff becomes 0 → record answer</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

**Field count to imitate:** 3-column foundational visual ≥ 25 lines, chain-box with 4 rows, ≥ 3 chain-examples. Final §1 line count target: 85–100 (permutation-in-string is 91).

Also load `design/known_bugs.md` — the diff-inversion warning is critical when authoring this kernel.

---

## Canonical pattern — prefix_scan archetype

Source: lifted from `lessons/trapping-rain-water/lesson.html` lines 114–162 (snapshot 2026-05-19).

This archetype teaches via a **single densely-annotated visual** (no chain-box). The visual carries the entire insight — formula falls out of it. Use this style when the insight is local (per-index, depending on neighbours' min/max/sum) and a single labelled diagram can show all moving parts.

```html
<!-- ═══ SECTION 1: THE INSIGHT ═══ -->
<div class="section">
  <p class="sec-label">The Insight</p>
  <p class="sec-title">[INSIGHT — e.g. "Water level at any bar is set by its shortest surrounding wall"]</p>

  <p class="body">[KERNEL PARAGRAPH — describe the per-index relationship to neighbours. State the dependency clearly: this index's answer depends on max/min/sum of its left side and right side. 200+ chars.]</p>

  <!-- Densely-annotated foundational visual: bar chart / matrix / number-line -->
  <!-- This is the most important block; it does the teaching. -->
  <div style="display:flex;align-items:flex-end;gap:5px;margin:1.25rem 0 .5rem;flex-wrap:wrap">
    <!-- For each cell/bar/element: -->
    <!--   - container div (flex column, align center) -->
    <!--   - the bar itself (styled to show height/value) -->
    <!--   - annotation overlay (showing trapped quantity, dependency, etc.) -->
    <!--   - bottom label (index, value, or role: maxL/maxR/h) -->
    <!-- Use color coding: info color for "wall" bars, warn color for second wall, success for trapped quantity -->
    <!-- ≥ 30 lines total in this block — substantial enough to show ALL dependencies -->
    [REPLACE WITH PROBLEM-SPECIFIC CHART]
  </div>

  <div class="infobox success">
    <p class="infobox-t">[THE FORMULA / THE INVARIANT — e.g. "The water formula"]</p>
    <p class="infobox-d" style="font-family:var(--mono);font-size:13px;line-height:2">
      [FORMULA — e.g. water[i] = min(maxLeft[i], maxRight[i]) − height[i]]<br>
      <span style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:12px;color:var(--text3)">[WHERE-CLAUSE defining each term]</span>
    </p>
  </div>
</div>
```

**Field count to imitate:** kernel paragraph + densely-annotated visual ≥ 30 lines + formula infobox. **No chain-box required** — the visual carries the reduction. Final §1 line count target: 45–60 (trapping-rain-water is 49).

The lint rule explicitly accepts this style: "OR a foundational visual block ≥ 30 lines positioned before the infobox success".

---

## Canonical pattern — divide_conquer archetype

Source: lifted from `lessons/median-of-two-sorted-arrays/lesson.html` lines 102–214 (snapshot 2026-05-19).

This archetype teaches via a **partition diagram** plus a chain-box that proves correctness of the partition condition. The insight is that the answer is characterized by a single invariant (e.g. "k elements on the left half across both arrays") and binary search finds it.

```html
<!-- ═══ SECTION 1: THE INSIGHT ═══ -->
<div class="section">
  <p class="sec-label">The Insight</p>
  <p class="sec-title">[INSIGHT — e.g. "Partition both arrays so the left half has exactly k elements; the median lives at the boundary."]</p>

  <p class="body">[KERNEL PARAGRAPH — define the partition / split / pivot. State the invariant the algorithm maintains. Mention that binary search on the smaller array converges in O(log min(m,n)).]</p>

  <!-- Foundational visual: partition diagram showing the cut across both arrays -->
  <div style="margin:1.25rem 0">
    <!-- Two horizontal arrays side by side, each split by a vertical bar (partition line) -->
    <!-- Highlight the four boundary elements: A[i-1], A[i], B[j-1], B[j] -->
    <!-- Annotate: left half size = i + j; total left = k where k = (m+n+1)/2 -->
    <!-- Use color: success-bg for elements in the left half, danger-bg for right half, warn-border for boundary elements -->
    [REPLACE WITH PROBLEM-SPECIFIC PARTITION DIAGRAM — ≥ 25 lines]
  </div>

  <div class="infobox success">
    <p class="infobox-t">The kernel</p>
    <p class="infobox-d">[ONE-PARAGRAPH ALGORITHM SUMMARY — binary search on partition position i in the smaller array. Compute j = k - i. Valid partition: A[i-1] ≤ B[j] AND B[j-1] ≤ A[i]. Answer at the partition boundary.]</p>
  </div>

  <!-- Equivalence chain: proves the partition condition is correct -->
  <p class="body" style="margin-top:1rem">Why the partition condition characterizes the median:</p>
  <div class="chain-box">
    <div class="chain-row">
      <span class="chain-sym"></span>
      <div class="chain-content">
        <div class="chain-text">[THE PROBLEM — find median of A ∪ B in sorted order]</div>
        <div class="chain-note">the problem</div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text">find a split such that left half has k elements, right has m+n-k</div>
        <div class="chain-note">[median is at the boundary by definition]</div>
        <div class="chain-example">
          <span class="pill n">[concrete A, B]</span><span class="arrow">→</span>
          <span class="pill n">[show k = (m+n+1)/2]</span>
        </div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text">pick i in A, set j = k - i; condition: max(left) ≤ min(right) across both arrays</div>
        <div class="chain-note">[two arrays already sorted internally — only cross-array order matters]</div>
        <div class="chain-example">
          <span class="pill n">[show i, j on the diagram]</span>
          <span class="pill ok">[A[i-1] ≤ B[j] AND B[j-1] ≤ A[i]]</span>
        </div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text"><span class="chain-hl">binary search on i in the smaller array</span></div>
        <div class="chain-note">[O(log min(m,n)) — the bigger array is never iterated]</div>
        <div class="chain-example">
          <span class="pill n">A[i-1] &gt; B[j]</span><span class="arrow">→</span><span class="pill n">i too big, search left</span>
          <span style="margin:0 4px;color:var(--text3)">·</span>
          <span class="pill n">B[j-1] &gt; A[i]</span><span class="arrow">→</span><span class="pill n">i too small, search right</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

**Field count to imitate:** partition diagram ≥ 25 lines + kernel infobox + chain-box with 4 rows. Final §1 line count target: 100–115 (median-of-two-sorted-arrays is 113).

---

## Custom archetype (no canonical match)

If the problem doesn't fit any of the four canonical patterns (e.g. spiral-matrix, first-missing-positive, find-the-duplicate-number — array-as-hash, cycle detection on implicit list, boundary shrinking), pick the canonical pattern closest in *teaching structure* and adapt:

- **In-place marking / array-as-hash** → adapt two-pointer pattern (chain reduces from "find missing X" to "encode presence in indices" to "swap to home position" to "scan for first wrong slot").
- **Cycle detection on implicit list** → adapt divide_conquer pattern (chain reduces from "find duplicate" to "treat array as linked list" to "Floyd's two-phase cycle detection").
- **Geometric / boundary shrinking** → adapt prefix_scan pattern (densely-annotated visual showing all four boundaries; no chain-box needed if the visual makes the algorithm obvious).

Lint enforces structural minimums (chain-box OR ≥ 30-line visual), not exact match to one of the four. Adapt freely as long as the lint passes.

---

## Animation step-generator templates (PLAN-017)

Each archetype has a different state shape, so each gets a JS skeleton showing what `siGenSteps(input)` should return and what `siRender(st)` should update. The control wiring (`siNext`, `siPrev`, `siReset`, `siTogglePlay`, `siStopPlay`) is identical across all four; only the generator and renderer differ.

### Shared control wiring (copy verbatim)

Append once per lesson, in the `<script>` block below §1 markup:

```html
<script>
  let siSteps = [];      // populated by siGenSteps at init
  let siCur = 0;
  let siTimer = null;

  // ── shared control wiring (identical across all four archetypes) ──
  function siNext()   { if (siCur < siSteps.length - 1) { siCur++; siRender(siSteps[siCur]); } else siStopPlay(); }
  function siPrev()   { if (siCur > 0)                    { siCur--; siRender(siSteps[siCur]); } }
  function siReset()  { siStopPlay(); siCur = 0; siRender(siSteps[0]); }
  function siStopPlay(){ clearInterval(siTimer); siTimer = null;
                         document.getElementById('si-bplay').textContent = '▶ Auto'; }
  function siTogglePlay(){
    if (siTimer) { siStopPlay(); }
    else {
      document.getElementById('si-bplay').textContent = '⏸ Pause';
      siTimer = setInterval(() => {
        if (siCur < siSteps.length - 1) siNext(); else siStopPlay();
      }, 1400);
    }
  }
  function siUpdateCtr(){
    const c = document.getElementById('si-sctr');
    if (c) c.textContent = `step ${siCur + 1} / ${siSteps.length}`;
  }
</script>
```

The control row in the §1 markup ties to these:

```html
<div class="ctrl-row" style="margin-top:.625rem">
  <button class="ctrl-btn" onclick="siPrev()">← Prev</button>
  <button class="ctrl-btn pri" id="si-bplay" onclick="siTogglePlay()">▶ Auto</button>
  <button class="ctrl-btn" onclick="siNext()">Next →</button>
  <button class="ctrl-btn" onclick="siReset()">↺ Reset</button>
  <span class="step-ctr" id="si-sctr"></span>
</div>
```

### Per-archetype step shape

#### two_pointer (e.g. 3sum, container-with-most-water)

```js
function siGenSteps(input) {
  const nums = [...input].sort((a, b) => a - b);  // archetype expects sorted
  const steps = [];
  let i = 0;
  steps.push({ i, L: i + 1, R: nums.length - 1, action: 'init',
               note: `fix nums[${i}]; squeeze L and R inward` });
  // Push one step per pointer move. Each step object names:
  //   i, L, R    — pointer positions
  //   action     — 'L++' | 'R--' | 'match' | 'restart-i'
  //   sum        — current nums[i] + nums[L] + nums[R]
  //   note       — short caption shown beneath the visual
  // Aim for 6–8 steps total. End on a 'match' or 'no-match' final state.
  return steps;
}

function siRender(st) {
  // for each cell in the number-line, toggle .nl-num.fixed / .ptr-l / .ptr-r
  // based on st.i, st.L, st.R. Update sum label and note caption.
  siUpdateCtr();
}
```

#### sliding_window (e.g. permutation-in-string, longest-substring)

```js
function siGenSteps([s1, s2]) {
  const steps = [];
  const k = s1.length;
  const freqS1 = freqMap(s1);
  let freqWin = freqMap(s2.slice(0, k));
  steps.push({ winStart: 0, winEnd: k - 1, freqWin: {...freqWin},
               diff: countDiff(freqS1, freqWin),
               note: `initial window: "${s2.slice(0, k)}"` });
  for (let i = k; i < s2.length; i++) {
    // remove s2[i-k], add s2[i], update diff
    steps.push({ winStart: i - k + 1, winEnd: i, freqWin: {...freqWin},
                 diff: ..., note: `slide window to "${s2.slice(i - k + 1, i + 1)}"` });
  }
  return steps;  // typically 5–7 steps
}

function siRender(st) {
  // highlight cells s2[st.winStart..st.winEnd] as window
  // render frequency badges per character (color match = freqWin[c] === freqS1[c])
  // show diff counter
  siUpdateCtr();
}
```

#### prefix_scan (e.g. trapping-rain-water, maximum-subarray, product-of-array-except-self)

```js
function siGenSteps(nums) {
  const steps = [];
  let cur = nums[0], best = nums[0];
  steps.push({ i: 0, nums: [...nums], cur, best, action: 'init',
               note: `start: cur = best = nums[0] = ${nums[0]}` });
  for (let i = 1; i < nums.length; i++) {
    const extend = cur + nums[i];
    const restart = nums[i];
    const action = restart > extend ? 'restart' : 'extend';
    cur = Math.max(restart, extend);
    const newBest = cur > best;
    best = Math.max(best, cur);
    steps.push({ i, nums: [...nums], cur, best, action, newBest,
                 note: `i=${i}: ${action} → cur=${cur}` });
  }
  return steps;  // one per index of the example
}

function siRender(st) {
  // for each cell in row 1 (nums): mark dim except the cell at st.i
  // row 2 (cur after): show st.cur, color-coded by st.action (extend/restart)
  // row 3 (best): show st.best, add ★ if st.newBest
  siUpdateCtr();
}
```

#### divide_conquer (e.g. median-of-two-sorted-arrays, search-in-rotated-sorted-array)

```js
function siGenSteps([A, B]) {
  const m = A.length, n = B.length;
  const total = m + n;
  const k = Math.floor((total + 1) / 2);
  const steps = [];
  let lo = 0, hi = m;
  while (lo <= hi) {
    const i = Math.floor((lo + hi) / 2);
    const j = k - i;
    const Aleft  = i === 0 ? -Infinity : A[i - 1];
    const Aright = i === m ? +Infinity : A[i];
    const Bleft  = j === 0 ? -Infinity : B[j - 1];
    const Bright = j === n ? +Infinity : B[j];
    let action;
    if (Aleft <= Bright && Bleft <= Aright) { action = 'valid-partition'; }
    else if (Aleft > Bright) { action = 'i-too-big'; hi = i - 1; }
    else { action = 'i-too-small'; lo = i + 1; }
    steps.push({ A, B, i, j, Aleft, Aright, Bleft, Bright, action,
                 note: `i=${i}, j=${j}: ${action}` });
    if (action === 'valid-partition') break;
  }
  return steps;  // typically 4–6 steps (log m iterations)
}

function siRender(st) {
  // render two horizontal arrays A, B with vertical bars at positions i, j
  // colour-code the four boundary cells (Aleft, Aright, Bleft, Bright)
  // show "i too big" or "valid partition" verdict next to the diagram
  siUpdateCtr();
}
```

### Reuse across §1 and §6

`siGenSteps` and `cvGenSteps` often have similar shape (both walk the same algorithm). The differences:

- §1 generator walks the **canonical insight example**; §6 generator walks one of several **execution examples** (and the reader can switch via `cvLoadEx(idx)`).
- §1 has 4–9 steps focused on *decisions*; §6 has 10–15 steps covering *every* loop iteration.
- §1 renders the *foundational visual* (the §1 layout); §6 renders the side-by-side code panel + state panel.

You can copy the algorithm logic from `siGenSteps` into `cvGenSteps` and add finer granularity. Not the other way around — `cvGenSteps` is usually too granular to be useful in §1.
