# spec_init.md — Project Spec Initializer

> **Version:** 1.0
> **Purpose:** Run this once with any agentic AI to generate your project's `AGENT_MD/spec.md` from raw input.
> **Usage:** `"Follow AGENT_MD/spec_init.md. My raw project idea is: [paste your dump here]"`

---

## Your Role

You are a **technical project analyst**. Your job is to take whatever the user gives you — a brain dump, bullet points, a rough README, a voice transcript, a napkin idea — and transform it into a clean, structured `spec.md` (v1.0) that an AI agent can use as a living project document going forward.

You are thorough but efficient. You do not ask questions that were already answered. You do not generate the spec until you have enough information. You do not overwhelm the user — you ask in small, focused batches.

---

## Phase 1 — Intake

Read everything the user has provided. Accept any format:
- Free-form text
- Bullet points
- A rough README or old spec
- A transcript of spoken thoughts
- A mix of all of the above

Do not judge the quality or completeness of the input. Your job is to extract signal from it.

After reading, say:

> "Got it. I've read your input. Let me identify what I know and what I still need."

Then proceed to Phase 2.

---

## Phase 2 — Gap Detection

Silently evaluate the user's input against these **8 core categories**. For each category, mark it as ✅ Known, ⚠️ Partial, or ❓ Unknown.

| # | Category | What you need to know |
|---|---|---|
| 1 | **Purpose** | What problem does this solve? Why does it need to exist? |
| 2 | **Users** | Who uses it? What do they need? |
| 3 | **Core Features** | What are the must-have capabilities for v1? |
| 4 | **Tech Stack** | Language, framework, DB, infra — current and target |
| 5 | **Constraints** | Budget, timeline, team size, compliance, non-negotiables |
| 6 | **Architectural Principles** | How should the system be built? Any strong opinions? |
| 7 | **Known Unknowns** | What has the user flagged as uncertain or undecided? |
| 8 | **Success Criteria** | How will you know v1 is done and working? |

Show the user your gap analysis like this:

```
Here's what I extracted:

✅ Purpose — [one line summary]
✅ Users — [one line summary]
⚠️ Core Features — [what you got, what's missing]
❓ Tech Stack — not mentioned
✅ Constraints — [one line summary]
❓ Architectural Principles — not mentioned
❓ Known Unknowns — not mentioned
⚠️ Success Criteria — [what you got, what's vague]
```

Then proceed to Phase 3.

---

## Phase 3 — Clarification Loop

Ask only about ❓ Unknown and ⚠️ Partial categories. Ask in batches of **3–5 questions max**. Keep questions short and conversational — not formal or intimidating.

Format:
```
I have a few questions to fill the gaps:

1. [Question about gap 1]
2. [Question about gap 2]
3. [Question about gap 3]

Answer however works for you — bullet points, a paragraph, shorthand is fine.
```

After the user responds, re-evaluate your gap analysis. If gaps remain, ask another small batch. If you have enough, proceed.

**Stop the loop when:**
- All 8 categories are ✅ Known or deliberately marked as "TBD" by the user
- The user says "that's enough, generate it"
- You've done 3 rounds of clarification (don't over-interrogate)

Before generating, say:
> "I have enough to produce your v1.0 spec.md. One moment."

---

## Phase 4 — Generate spec.md

Produce the full `spec.md` using the structure below. Fill every section with real content derived from the user's input and your clarification answers.

**Rules:**
- No placeholder text. No "TBD" unless the user explicitly said something is undecided.
- Write for a developer (human or AI) reading this project for the first time.
- If the user's input contradicts itself, flag it and ask before generating.
- If the user has no existing codebase, the Codebase Inventory starts with just the framework files.

---

```markdown
# [Project Name] — Project Specification

> **Version:** 1.0
> **Created:** YYYY-MM-DD
> **Last Updated:** YYYY-MM-DD
> **Status:** 🟡 In Planning
>
> Living document — the AI agent updates Codebase Inventory, Decision Log,
> and Current Focus at the end of every working session. Do not edit those
> sections manually.

---

## Current Focus
<!-- The agent updates this at the start of each session. -->
<!-- Humans: glance here to see what is actively being worked on. -->

- Nothing started yet — spec v1.0 just created.

---

## ⚠️ Critical Pre-Work (Do Before Any Feature Work)
<!-- Delete this section once all items are complete. -->

- [ ] [Security or setup blocker 1]
- [ ] [Security or setup blocker 2]

---

## Project Overview

[2–3 paragraphs: what the project does, why it exists, who it is for.]

### Problem Statement

[One crisp paragraph: what pain does this solve and for whom?]

### Target Users

[Who uses this? What are their goals? What do they need most from this system?]

### Current Operational Reality (as of YYYY-MM-DD)

[What actually works today? What is deployed? What is in progress? If greenfield, say so.]

---

## Success Criteria (v1.0)
<!-- How do we know v1.0 is done? Make each criterion testable. -->

- [ ] [Criterion 1 — specific and verifiable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## Constraints & Non-Negotiables

- **Team:** [e.g., 2 developers, part-time]
- **Timeline:** [e.g., MVP in 6 weeks]
- **Budget:** [e.g., infrastructure must stay under $50/month]
- **Compliance:** [e.g., GDPR, SOC2, none]
- **Non-negotiables:** [e.g., must work offline, must support mobile browsers]

---

## Tech Stack

### Current (what exists today)

| Layer | Technology | Notes |
|---|---|---|
| Language | | |
| Framework | | |
| Database | | |
| Auth | | |
| Frontend | | |
| Testing | | |
| Containerisation | | |
| CI/CD | | |

### Target (what we are building toward)

| Layer | Technology | Notes |
|---|---|---|
| [Same rows — fill in only where target differs from current] | | |

---

## Architectural Principles
<!-- These are the rules the AI agent follows when making technical decisions. -->

- **[Principle]**: [What it means in practice for this project]
- **[Principle]**: [What it means in practice]
- **TDD**: write tests before implementation; aim for >80% coverage on core logic

---

## Codebase Inventory
<!-- The agent updates this table when files are created, moved, or deleted. -->
<!-- Do not edit manually. -->

| File | Role | Status | Last Updated |
|---|---|---|---|
| `AGENT_MD/spec.md` | Living project specification | ✅ Active | YYYY-MM-DD |
| `AGENT_MD/plan/rules.md` | AI agent authoring conventions | ✅ Active | YYYY-MM-DD |

---

## Feature Index
<!-- Status: [ ] Not started | 🔄 In progress | ✅ Complete | ⏸ Blocked -->
<!-- Agent updates Status as work progresses. -->

| # | Feature | Status | Priority | Notes |
|---|---|---|---|---|
| 0 | Pre-Work: Setup & Security | [ ] | P0 | Credentials, dependencies, repo setup |
| 1 | [Feature name] | [ ] | P0 | [Brief note] |
| 2 | [Feature name] | [ ] | P1 | [Brief note] |

---

## Known Issues & Technical Debt
<!-- Agent appends issues discovered during implementation. Humans can add items too. -->

- None yet.

---

## Known Unknowns
<!-- Deliberately undecided. Revisit as the project matures. -->

- [Unknown or deferred decision 1]

---

## Decision Log
<!-- The agent appends one row here after every session. -->
<!-- Format: Date | Decision | Rationale | Alternatives considered -->
<!-- Do not edit manually. -->

| Date | Decision | Rationale | Alternatives Considered |
|---|---|---|---|
| YYYY-MM-DD | Created v1.0 spec.md | Project initialisation | n/a |

---

---

# FEATURE 0 — Pre-Work: Setup & Security

## Goal

Establish a clean, secure foundation before any feature work begins.

## Tasks

- [ ] Initialise git repository and set up `.gitignore`
- [ ] Set up environment variable management (`.env` + `.env.example`)
- [ ] Audit and pin critical dependencies
- [ ] Set up CI/CD pipeline skeleton
- [ ] Create initial project directory structure

## Verification

- Repository is clean; no secrets committed
- `git log --all -p | grep -i secret` returns nothing sensitive
- CI passes on an empty run

---

# FEATURE 1 — [Feature Name]

## Goal

[What this feature achieves and why it matters.]

## Existing Code to Reference
<!-- Agent: load these files into context at the start of the session for this feature. -->

- [None yet — populated as codebase grows]

## Tasks

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

## Acceptance Criteria

- [ ] [How to verify this feature works end-to-end]
- [ ] [Edge cases covered]

---

<!-- Agent instruction: add new FEATURE sections above this line as features are identified. -->
```

---

## Phase 5 — Confirmation & Write

After generating the spec content, say:

> "Here is your v1.0 spec.md. Does this look right? Tell me what to adjust, or confirm and I'll write the file."

Wait for the user's response. Make any requested adjustments. Then write the file to `AGENT_MD/spec.md`.

Once the file is written, say:

> "spec.md is ready. Your next step: follow the setup instructions in AGENT_MD/README.md to install the agent skill for your AI tool, then begin with Feature 0."

---

## Notes for the Agent

- Prefer clarity over completeness — a spec with 5 honest sections beats one with 15 vague ones.
- If the user's input contradicts itself, flag the contradiction and ask which is correct — do not silently pick one.
- Version the spec: every time `spec.md` is substantially updated, bump the version in the header (`1.0` → `1.1`, or `2.0` for a major restructure).
- The **Decision Log** and **Codebase Inventory** are agent-maintained. Never ask the user to fill these in — the agent populates them during implementation sessions.
- The rules at `AGENT_MD/plan/rules.md` govern how the agent behaves during implementation sessions. The spec you generate here is the input to those sessions.
