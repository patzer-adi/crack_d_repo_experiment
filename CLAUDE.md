# Project notes for Claude

This is a multi-machine project (synced via git). When making changes that future-you should remember on either machine, write them into the project files (committed to git), not into local Claude memory.

## When working on lessons

- **Batch generation (1–5 problems):** the user invokes `/batch-lesson <slug1> <slug2> ...`. The full workflow lives in [`.claude/commands/batch-lesson.md`](.claude/commands/batch-lesson.md) — read that when the command fires.
- **Single-lesson or ad-hoc work:** read [`lessons/LESSON_DESIGN.md`](lessons/LESSON_DESIGN.md). It is the lean **index** pointing at section-specific files under `lessons/design/`.

**Loading rule (per PLAN-011):** Load `lessons/LESSON_DESIGN.md` by default. Load files under `lessons/design/` *only* when authoring the matching section. Do **not** preload them. The index's section table tells you what to load. For class names, use [`static/CLASSES.md`](static/CLASSES.md), never the full `static/lesson.css`.

**Quality gate (per PLAN-016, hardened by PLAN-019):** Before marking `lesson_status=generated`, a lesson must pass three checks: [`scripts/lint_lesson.py <slug>`](scripts/lint_lesson.py) (structure + the §6 code-line-resolves check), [`scripts/verify_animation.mjs <slug>`](scripts/verify_animation.mjs) (answer-correctness; also runs `lessons/<slug>/verify.py` if present), and [`scripts/render_check.mjs <slug>`](scripts/render_check.mjs) (headless: no JS error, every §6 step lights a code line, no horizontal overflow). The batch-lesson skill enforces these. For §1, use the inline canonical pattern in [`lessons/design/sec1_insight.md`](lessons/design/sec1_insight.md) — do not open full golden lessons. To survey the whole corpus run [`scripts/audit_lessons.py`](scripts/audit_lessons.py) (full lint + render, baseline-aware); to check planning-doc/lesson reconciliation run [`scripts/doctor.py`](scripts/doctor.py).

The legacy monolith lives at [`lessons/archive/LESSON_DESIGN_v2.md`](lessons/archive/LESSON_DESIGN_v2.md). Use the partitioned files under `lessons/design/` instead.

## When working on the broader project

See [AGENT_MD/](AGENT_MD/) for the project's spec, plan/report lifecycle, and authoring rules. The latest implementation plan is [PLAN-021](AGENT_MD/plan/plans/PLAN-021_prerequisites_section.md) (Prerequisites tab — a 4th dashboard tab of foundational data-structure / algorithm / concept knowledge with a topic-derived problem cascade and a few hero animations; data gated by `scripts/check_prerequisites.py`, landed 2026-06-05), building on [PLAN-020](AGENT_MD/plan/plans/PLAN-020_mobile_friendly_responsive.md) (mobile-friendly responsive layout; render gate now also checks 390px) and [PLAN-019](AGENT_MD/plan/plans/PLAN-019_antidrift_visual_gate_and_doc_reconciliation.md) (anti-drift gate). Note `AGENT_MD/spec.md` is a historical 2026-05-07 snapshot — this file plus `README.md` are the current source of truth.
