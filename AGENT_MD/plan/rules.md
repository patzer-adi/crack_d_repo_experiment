# Plan & Report Authoring Rules

> **Purpose:** This file defines the conventions for all plan and report documents
> stored under `plan/`. It is designed to be referenced in LLM/agent prompts so
> that any AI assistant producing plans or reports follows a consistent format.
>
> **Usage in prompts:** Include the directive
> `Follow the rules in AGENT_MD/plan/rules.md when writing plans or reports.`

---

## 1. Directory layout

```
plan/
├── rules.md                          # THIS FILE — authoring conventions
├── current_state_report.md           # Latest project state snapshot
├── plans/                            # One file per plan
│   └── PLAN-NNN_<slug>.md
└── reports/                          # One file per implementation report
    └── REPORT-NNN_<slug>.md
```

- **plans/** stores *forward-looking* documents (what will be done).
- **reports/** stores *backward-looking* documents (what was done, results, learnings).
- A report's NNN **must match** the plan it implements (e.g., `PLAN-001` → `REPORT-001`).
- `current_state_report.md` is a living document updated whenever a major audit is performed.

---

## 2. Naming conventions

| Item | Pattern | Example |
|------|---------|---------|
| Plan file | `PLAN-NNN_<short-slug>.md` | `PLAN-001_auth_system.md` |
| Report file | `REPORT-NNN_<short-slug>.md` | `REPORT-001_auth_system.md` |
| Slug | lowercase, underscores, ≤ 5 words | `user_auth_jwt` |
| NNN | Zero-padded 3-digit serial | `001`, `002`, … |

---

## 3. Plan document template

Every plan **must** contain these sections in order:

```markdown
# PLAN-NNN: <Title>

**Created:** YYYY-MM-DD
**Status:** Draft | Approved | In-Progress | Completed | Abandoned
**Addresses:** <one-line description of the gap/need this plan targets>

---

## 1. Context & motivation
Why this plan exists. Link to the current state report or prior reports
that surfaced the need.

## 2. Goals
Bulleted list of measurable outcomes.
Each goal should be verifiable (pass/fail, metric threshold, etc.).

## 3. Non-goals
What is explicitly out of scope.

## 4. Approach
Detailed description of the technical approach.
Include architecture decisions, trade-offs, and alternatives considered.

## 5. Task breakdown
Numbered, actionable tasks. Each task should be small enough to complete
in a single working session (< 4 hours). Use this format:

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | … | 30 min | — |
| 2 | … | 2 hr | 1 |

## 6. Risks & mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| … | Low/Med/High | Low/Med/High | … |

## 7. Success criteria
How we know the plan is fully implemented.
Reference specific goals from §2.

## 8. References
Links to docs, files, external resources.
```

---

## 4. Report document template

Every report **must** contain these sections in order:

```markdown
# REPORT-NNN: <Title>

**Plan:** PLAN-NNN
**Completed:** YYYY-MM-DD
**Author:** <human or AI agent identifier>

---

## 1. Summary
One paragraph: what was implemented, key outcomes.

## 2. Goals vs. actuals
Table mapping each goal from the plan to its actual outcome.

| Goal (from plan) | Outcome | Evidence |
|-------------------|---------|----------|
| … | ✅ Met / ⚠️ Partial / ❌ Not met | link or description |

## 3. Changes made
List every file created, modified, or deleted.
Group by logical unit (e.g., "Auth system", "Database migration").

### 3.1 <Logical unit>
- `path/to/file.py` — description of change
- …

## 4. Testing & validation
How correctness was verified. Include command outputs, test results,
or manual verification steps.

## 5. Known issues & follow-ups
Anything left unresolved. Link to follow-up plan if one exists.

## 6. Metrics (if applicable)
Before/after performance numbers, error rates, etc.

## 7. Lessons learned
What went well, what was harder than expected, what to do differently.
```

---

## 5. Writing style rules

These apply to **both** plans and reports:

1. **Be concrete, not vague.** Write "Add a 3-retry loop with exponential backoff in `downloader.py:fetch()`" — not "Improve error handling."
2. **Reference files by relative path** from project root (e.g., `src/auth.py`).
3. **Use present tense** in plans ("We add…"), **past tense** in reports ("We added…").
4. **Include code snippets** when they clarify intent, but keep them short (< 20 lines). Use fenced blocks with language tags.
5. **No orphan acronyms.** First use must expand: "Server-Sent Events (SSE)".
6. **Dates** use ISO 8601: `YYYY-MM-DD`.
7. **Status field** must be kept current. When work begins on a plan, change status to `In-Progress`. When the report is written, change the plan status to `Completed`.
8. **Cross-reference** between plan and report using the NNN identifier.
9. **Keep each section self-contained.** A reader should be able to jump to §5 of a report without reading §1–4.
10. **Tables over prose** for structured data (task lists, file inventories, metrics).
11. **Test-first workflow.** Every implementation task follows this sequence:
    1. **Write test(s)** — define the expected behaviour before writing production code.
    2. **Implement** — write the minimum code to make the tests pass.
    3. **Run & verify** — execute the test suite; the task is not done until tests are green.

    AI agents must follow this order. A task's PR/commit should contain test files *before* or *alongside* the implementation, never after.

---

## 6. Advanced rules for AI agents

These rules govern **how AI agents behave during implementation**, complementing
the writing style rules in §5.

### 6.1 Think before coding

1. **State assumptions explicitly.** If uncertain about intent, ask before implementing.
2. **Surface ambiguity.** If multiple interpretations exist, present them — don't pick silently.
3. **Propose simpler alternatives.** If a simpler approach exists, say so. Push back when warranted.
4. **Stop on confusion.** If something is unclear, name what's confusing and ask. Don't guess.

### 6.2 Minimum viable changes

1. **No speculative features.** Don't add capabilities, configurability, or abstractions beyond what was requested.
2. **No single-use abstractions.** Don't create helpers, wrappers, or utilities for code that's used once.
3. **No impossible-case handling.** Don't add error handling, fallbacks, or validation for scenarios that cannot occur. Validate only at system boundaries (user input, external APIs).
4. **Question your own output.** If 200 lines could be 50, rewrite before submitting.

### 6.3 Surgical edits

When modifying existing code:

1. **Touch only what you must.** Every changed line should trace directly to the request.
2. **Don't "improve" adjacent code.** No reformatting, comment tidying, or refactoring of code that isn't broken.
3. **Match existing style.** Follow the conventions already in the file, even if you'd do it differently.
4. **Clean up only your own orphans.** Remove imports, variables, or functions that *your* changes made unused. Don't remove pre-existing dead code unless asked — mention it instead.

### 6.4 Goal-driven execution

1. **Define success criteria before starting.** Transform vague tasks into verifiable goals:
   - "Add validation" → "Write tests for invalid inputs, then make them pass"
   - "Fix the bug" → "Write a test that reproduces it, then make it pass"
   - "Refactor X" → "Ensure tests pass before and after"
2. **State a brief plan for multi-step work:**
   ```
   1. [Step] → verify: [check]
   2. [Step] → verify: [check]
   3. [Step] → verify: [check]
   ```
3. **Loop until verified.** Don't mark a task done until its success criteria are confirmed.

---

## 7. Lifecycle

```
Draft plan  →  Approved  →  In-Progress  →  Completed (report written)
                                ↘ Abandoned (with reason noted)
```

1. Create `PLAN-NNN_slug.md` with status `Draft`.
2. Review and change status to `Approved`.
3. Begin work → status `In-Progress`.
4. Finish work → write `REPORT-NNN_slug.md`, change plan status to `Completed`.
5. If abandoned, change plan status to `Abandoned` and note the reason in §1 of the plan.

---

## 8. Prompt integration

When instructing an AI agent to create a plan or report, include:

```
Follow the rules defined in AGENT_MD/plan/rules.md for document structure,
naming, and style. The plan directory is at AGENT_MD/plan/ relative to
project root. Use the next available NNN serial number.
```

This ensures consistent output regardless of which agent or session produces the document.
