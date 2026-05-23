# AGENT_MD — AI-Assisted Software Development Framework

> Copy this entire folder into the root of your project.
> Then customise the files for your project.

## What This Is

A structured documentation framework that helps AI coding agents (Claude, Cursor, Gemini, etc.) develop software with you in a disciplined, traceable way. It provides:

- A **master specification** (`spec.md`) — the single source of truth for what the project is and where it's going
- A **plan/report lifecycle** — numbered plans (what to do) and reports (what was done) with matching IDs
- A **current state report** — a living snapshot of the real codebase, updated after major work
- **Reconciliation reports** — gap analysis between spec and reality
- **Authoring rules** — consistent formatting that any AI agent can follow

## Folder Structure

```
AGENT_MD/
├── README.md                         # This file — usage guide
├── spec.md                           # Master project specification (fill in, or generate with spec_init.md)
├── spec_init.md                      # AI-guided interview to generate spec.md from a brain dump
├── reconciliation-001.md             # Gap analysis template: spec vs. reality
├── examples/                         # ⚠️ Delete this folder before shipping your project
│   ├── README.md                     # Index of examples and fictional project description
│   ├── spec_example.md               # Fully filled spec for a sample project (TaskFlow API)
│   ├── current_state_example.md      # Filled-in current state report
│   ├── reconciliation_example.md     # Filled-in reconciliation report
│   ├── plans/
│   │   └── PLAN-001_example.md       # Filled-in plan
│   └── reports/
│       └── REPORT-001_example.md     # Filled-in report
└── plan/
    ├── rules.md                      # Authoring conventions for plans & reports
    ├── current_state_report.md       # Living project state snapshot (fill in for your project)
    ├── plans/                        # Forward-looking: what will be done
    │   └── PLAN-000_template.md      # Template — copy to start a new plan
    └── reports/                      # Backward-looking: what was done
        ├── README.md                 # Report index
        └── REPORT-000_template.md    # Template — copy when closing a plan
```

> **Serial number `000` is reserved for templates.** Real plans and reports start at `001`.
>
> **The `examples/` folder is for learning only.** It contains a fully worked fictional project
> (TaskFlow API) showing what every document looks like when complete. Delete it once you are
> comfortable with the framework — it has no effect on how the framework operates.

## Setup

1. Copy the `AGENT_MD/` folder into your project root.
2. At the start of each AI session, paste:
   ```
   Here is my project spec (see AGENT_MD/spec.md). Today we are implementing
   [FEATURE NAME]. Follow the rules in AGENT_MD/plan/rules.md when writing
   plans or reports. Use TDD: write tests first, get my approval, then implement.
   ```

## How to Use

### 0. Generate your `spec.md` (recommended for new projects)

Instead of filling in the blank template manually, run the AI-guided initialiser:

```
Follow AGENT_MD/spec_init.md. My raw project idea is: [paste your brain dump here]
```

The agent will interview you, fill any gaps, and write a complete `AGENT_MD/spec.md` for you.
If you prefer to fill it in manually, open `AGENT_MD/spec.md` directly.

### 1. Customise `spec.md`

Fill in your project overview, tech stack, architectural principles, codebase inventory, and feature index.

### 2. Populate `current_state_report.md`

Do an initial audit of your codebase and fill in the source code inventory, known issues, and operational status.

### 3. Start a plan/report cycle

When you begin a new feature or fix:

1. Copy `plan/plans/PLAN-000_template.md` to `plan/plans/PLAN-NNN_slug.md`
2. Fill in all sections; set status to `Draft`
3. Change status to `In-Progress` when you start work
4. When done, copy `plan/reports/REPORT-000_template.md` to `plan/reports/REPORT-NNN_slug.md`
5. Mark the plan `Completed`
6. Update `current_state_report.md` with a summary of what changed

### 4. Reconcile periodically

When the spec and reality drift apart, create a new `reconciliation-NNN.md` (copy and increment the serial) to identify gaps and prioritise fixes.

## Key Principles

- **Plans are forward-looking** — what will be done, with task breakdowns and risks
- **Reports are backward-looking** — what was done, with evidence and lessons learned
- **Plan NNN → Report NNN** — every report matches its plan by serial number
- **Test-first workflow** — write tests before implementation
- **Tables over prose** — structured data is easier for AI agents to parse
- **Concrete over vague** — "Add retry loop in `downloader.py:fetch()`" not "improve error handling"


