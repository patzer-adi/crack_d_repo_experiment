# Examples

> **This folder can be deleted once you are comfortable with the framework.**
> It contains no framework logic — only illustrative samples.

This folder contains fully populated versions of every AGENT_MD document,
based on a fictional project called **TaskFlow API** (a Python/FastAPI task
management service).

Use these to understand what a real filled-in document looks like before
writing your own.

## What's Here

| Example file | Template it illustrates |
|---|---|
| [`spec_example.md`](spec_example.md) | `AGENT_MD/spec.md` |
| [`current_state_example.md`](current_state_example.md) | `AGENT_MD/plan/current_state_report.md` |
| [`reconciliation_example.md`](reconciliation_example.md) | `AGENT_MD/reconciliation-001.md` |
| [`plans/PLAN-001_example.md`](plans/PLAN-001_example.md) | `AGENT_MD/plan/plans/PLAN-000_template.md` |
| [`reports/REPORT-001_example.md`](reports/REPORT-001_example.md) | `AGENT_MD/plan/reports/REPORT-000_template.md` |

## The Fictional Project

All examples describe **TaskFlow API**:
- Python 3.12 + FastAPI REST service
- PostgreSQL 16 database, Redis cache
- pytest test suite, Docker Compose, GitHub Actions CI
- A realistic mid-development state: basic CRUD working, auth missing, coverage low
