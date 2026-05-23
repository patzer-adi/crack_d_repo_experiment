# Project notes for Claude

This is a multi-machine project (synced via git). When making changes that future-you should remember on either machine, write them into the project files (committed to git), not into local Claude memory.

## When working on lessons

- **Batch generation (1–5 problems):** the user invokes `/batch-lesson <slug1> <slug2> ...`. The full workflow lives in [`.claude/commands/batch-lesson.md`](.claude/commands/batch-lesson.md) — read that when the command fires.
- **Single-lesson or ad-hoc work:** read [`lessons/LESSON_DESIGN.md`](lessons/LESSON_DESIGN.md). It is the lean **index** pointing at section-specific files under `lessons/design/`.

**Loading rule (per PLAN-011):** Load `lessons/LESSON_DESIGN.md` by default. Load files under `lessons/design/` *only* when authoring the matching section. Do **not** preload them. The index's section table tells you what to load. For class names, use [`static/CLASSES.md`](static/CLASSES.md), never the full `static/lesson.css`.

**Quality gate (per PLAN-016):** Run [`scripts/lint_lesson.py <slug>`](scripts/lint_lesson.py) before marking `lesson_status=generated`. The batch-lesson skill enforces this. For §1, use the inline canonical pattern in [`lessons/design/sec1_insight.md`](lessons/design/sec1_insight.md) — do not open full golden lessons. To survey state across all lessons, run [`scripts/audit_lessons.py`](scripts/audit_lessons.py).

The legacy monolith lives at [`lessons/archive/LESSON_DESIGN_v2.md`](lessons/archive/LESSON_DESIGN_v2.md). Use the partitioned files under `lessons/design/` instead.

## When working on the broader project

See [AGENT_MD/](AGENT_MD/) for the project's spec, plan/report lifecycle, and authoring rules. The latest implementation plan is [PLAN-016](AGENT_MD/plan/plans/PLAN-016_self_healing_pipeline.md) (self-healing lesson generation pipeline, landed 2026-05-20).
