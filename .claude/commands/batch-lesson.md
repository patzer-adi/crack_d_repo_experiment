---
description: Generate lessons for 1–5 problem slugs, one at a time with autonomous correctness gates
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Batch lesson generation (autonomous)

You are generating DSA Intuition Lab lessons for the slugs the user passed: **$ARGUMENTS**

Process them **one at a time**, fully finishing each (both gates green + committed)
before starting the next. There is **no manual approval checkpoint** — the lint gate
and the animation-correctness gate together stand in for the human review, so they are
non-negotiable and may never be weakened to force a pass.

## Per-lesson workflow

For each slug:

### 1. Setup

- Read `lessons/LESSON_DESIGN.md` **once** at the very start (it's the index; load
  section files only as you author the matching section, per the loading rule in
  `CLAUDE.md`). For class names use `static/CLASSES.md`, never the full `lesson.css`.
- Create `lessons/<slug>/` if it doesn't exist.

### 2. Author the lesson

Follow the design system. Build the full `lesson.html` with all sections, animations,
and the **dry-run oracle**. The primary focus of every lesson is a graphical, animated
intuition for solving the problem.

The oracle must satisfy the verifier's contract (see the header of
`scripts/verify_animation.mjs`):

1. A pure `drGenSteps(...)` (or `drGen(...)`) generator — **no `document` /
   `getElementById` / `window`**; rendering lives in `*Render`, never in the generator.
2. An answer-bearing example array: `const EX = [ { <input fields>, answer: <expected> }, … ]`.
   - If the lesson drives its panels from a bare-array `const EXAMPLES`, add a
     **parallel** `const EX` of `{…, answer}` objects instead of mutating `EXAMPLES`
     (the gate prefers `EX`; this leaves the bf/cv/render wiring untouched).
3. The generator's **terminal step carries a `result`** field equal to the algorithm's
   answer for that input. If steps are built via a `snap()`/helper with a fixed field
   whitelist, forward it (`result: vars.result` / `...extra`), or the field is silently dropped.

**Independence rule:** every `answer:` must be **hand-derived** (brute force / by hand),
never copied from the generator's own output — otherwise the gate is a tautology and
proves nothing.

### 3. Gates (both mandatory)

Run, in order:

```
python3 scripts/lint_lesson.py <slug>
node   scripts/verify_animation.mjs <slug>
```

A lesson is **done only when both** exit 0 and the verifier prints
`N verified, 0 WRONG, 0 unverifiable` (N ≥ 1). Read that line back before believing it.

An informational `✗ drGen is impure` line is acceptable **only** when it refers to an
interactive DOM handler that is not the oracle and a pure `drGenSteps` still verifies;
the gate will still exit 0. Anything that makes the gate exit non-zero is a real failure.

### 4. Bounded auto-retry

If either gate fails:

- Diagnose from its output and fix the **lesson** (the generator, the `result`, or a
  genuinely wrong hand-derived `answer`).
- Re-run both gates. Allow **up to 3 fix attempts** per lesson.
- **Never** "fix" a failure by editing a gate/script, deleting an example, copying
  generator output into `answer:`, or otherwise weakening the check.
- If a lesson still fails after 3 attempts, **stop**: leave it uncommitted, report the
  exact failing gate output for that slug, and do not silently move on. Continue with
  the remaining slugs only if they are independent.

### 5. Commit

Once both gates are green, commit just that lesson, quoting the verified line in the
message:

```
git add lessons/<slug>/
git commit -m "feat(lessons): add <slug> (lint clean; animation N verified, 0 WRONG)"
```

Then move to the next slug.

## Rules

- One lesson at a time. Never batch-generate the HTML for several at once.
- Both gates are mandatory; a lesson is not done until lint **and** verify pass.
- Never weaken, bypass, or fake a gate. A failing lesson stays uncommitted and reported.
- If the user says "stop" or "pause", finish the current step and wait.
- Do not touch unrelated working-tree files; commit only the lesson(s) you generated.
