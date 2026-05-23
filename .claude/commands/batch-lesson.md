---
description: Generate lessons for 1–5 problem slugs, one at a time with review checkpoints
argument-hint: <slug1> [slug2] [slug3] [slug4] [slug5]
---

Generate lessons for these slugs, one at a time in order:

$ARGUMENTS

Read `lessons/LESSON_DESIGN.md` once at the start. Then for **each slug**, do these six steps before moving to the next slug:

1. Run `python3 scripts/new_lesson.py <slug>` via Bash. Stop and ask the user if it errors.
2. Classify the archetype per `lessons/design/archetypes.md` (load it if not already loaded). Re-derive per problem.
3. Overwrite `lessons/<slug>/plan.md` with: kernel paragraph, archetype, translations, fast + slow examples (slow ≥ 10 visualisation steps), corner cases, approaches.
4. Run a Python algorithm trace on every planned example per `lessons/design/python_verify.md`. Paste the trace into `plan.md`. If any example fails, fix and re-trace.
5. **PAUSE.** Tell the user `Plan for <slug> ready. Approve to write HTML.` Wait for their reply before continuing.
6. On approval, author `lessons/<slug>/lesson.html` section-by-section per the index in `LESSON_DESIGN.md`. For each section, load only the design file it names. Use `static/CLASSES.md` for class names.

   **For §1 specifically (PLAN-017):**
   - Use the **inline canonical pattern** matching the chosen archetype inside `lessons/design/sec1_insight.md` — do NOT open the full golden lesson.html.
   - §1 visual MUST be **animated with reader controls** (prev/auto/next/reset). Use the matching per-archetype step-generator template in the "Animation step-generator templates" section of `sec1_insight.md`. Function names: `siGenSteps`, `siRender`, `siNext`, `siPrev`, `siReset`, `siTogglePlay`. Auto-mode speed: 1200 ms. Target 4–9 steps (one per decision point, not per loop iteration).
   - §7 (Dry Run) MUST have **≥ 3 example buttons** wired to `drLoadEx(idx)` — §7 is multi-example practice distinct from §6's single-example code walkthrough.

   **After §1 is written:**
     a. Run `python3 scripts/lint_lesson.py <slug>`. Read the output. If lint fails, the message names the specific rule (e.g. "no chain-box", "kernel paragraph 587 chars exceeds 350", "§1 needs prev/next/auto/reset buttons"). Fix exactly what failed and re-lint until exit 0.
     b. Self-review (one pass only — do NOT loop): re-read the new §1 against the matching archetype's canonical pattern in `sec1_insight.md`. Verify (i) it builds a foundational concept before stating the algorithm, (ii) animation controls are wired (`siNext` etc.), (iii) `siGenSteps` runs the canonical example through the algorithm, (iv) the sec-title doesn't open with "Use X as Y" or "Traverse N <thing>". Rewrite once if any of these fail. Skip if all pass.

   **After all sections written:**
     c. Run `python3 scripts/lint_lesson.py <slug>` one final time. Hard stop if any check fails — do NOT PATCH `lesson_status=generated` until lint exits 0.

   **Then PATCH:**
   ```bash
   curl -s -X PATCH http://localhost:8000/api/status \
     -H 'Content-Type: application/json' \
     -d '{"slug":"<slug>","lesson_status":"generated"}'
   ```
   If the server is not running, edit `data/problems.json` directly (set `lesson_status` to `"generated"`).

Anti-drift: re-derive archetype, translation count, and example pacing per problem. Do not default to the previous lesson's choices.

If more than 5 slugs were given, generate the first 5 and report the rest as deferred.
