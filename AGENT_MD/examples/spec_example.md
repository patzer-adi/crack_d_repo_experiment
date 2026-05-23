# TaskFlow API — Project Specification

> **Version:** 1.0
> **Created:** 2026-03-15
> **Last Updated:** 2026-04-01
> **Status:** 🟡 In Planning
>
> Living document — the AI agent updates **Codebase Inventory**, **Decision Log**, and **Current Focus**
> at the end of every working session. Do not edit those sections manually.

---

## Current Focus
<!-- Updated by the agent at the start of each session. -->

- Feature 0 (Pre-Work): rotate SECRET_KEY and upgrade cryptography — **in progress**
- Feature 3 (JWT Authentication): ready to start once Pre-Work is done

---

## ⚠️ Critical Pre-Work (Do Before Any Feature Work)

- [ ] Rotate the `SECRET_KEY` value committed in `src/config.py` on 2026-03-10 — remove from git history with `git filter-repo`
- [ ] Upgrade `cryptography` from 41.0.3 → 42.0.5 (CVE-2023-49083)

---

## Project Overview

TaskFlow API is a REST API for personal and small-team task management. Users create projects, add tasks to them, set due dates and priorities, and track completion. The API is consumed by a React frontend (separate repository) and a CLI client.

The project exists because the team needed a self-hosted alternative to Todoist with full data ownership and a programmable API.

### Problem Statement

Off-the-shelf task managers (Todoist, Linear, Asana) require storing sensitive project data on third-party servers, offer no programmatic customisation, and charge per-seat at scale. Small technical teams need a self-hosted, API-first alternative they can adapt without vendor lock-in.

### Target Users

Primary: individual developers and small technical teams (2–10 people) who are comfortable self-hosting a Docker application. They need full control of their data, a clean REST API for automation, and a simple web UI for daily use. Secondary: power users who want to script task management from the CLI.

### Current Operational Reality (as of 2026-04-01)

Core CRUD for projects and tasks is working and deployed to a single DigitalOcean droplet. There is no authentication — all endpoints are publicly accessible, which is acceptable only because the server IP is not public. JWT auth is the next priority. Redis is installed but not yet used by the application code. Test coverage is 48%, below the 80% target.

---

## Success Criteria (v1.0)

- [ ] A user can register, log in, and receive a JWT — unauthenticated requests return 401
- [ ] Full CRUD for projects and tasks — all endpoints covered by tests
- [ ] Test suite passes with ≥80% overall coverage and 0 failures
- [ ] Application runs end-to-end via `docker-compose up` with no manual steps
- [ ] No secrets or credentials committed to git history
- [ ] Production deployment accessible via HTTPS with a valid TLS certificate

---

## Constraints & Non-Negotiables

- **Team:** 1 developer, part-time (~10 hours/week)
- **Timeline:** MVP (Features 0–3) in 6 weeks from 2026-04-01
- **Budget:** Infrastructure must stay under $20/month (single DigitalOcean droplet)
- **Compliance:** No regulated data — GDPR not in scope for v1
- **Non-negotiables:** Must be fully self-hosted; no third-party auth providers; API must be versioned (`/api/v1/`)

---

## Tech Stack

### Current (what exists today)

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI 0.110 |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 (async) |
| Cache | Redis 7 (installed, not yet wired in) |
| Testing | pytest 8, pytest-asyncio, httpx |
| Containerisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Migrations | Alembic |

### Target (what we are building toward)

| Layer | Technology |
|---|---|
| Auth | JWT (python-jose) with refresh tokens |
| Cache | Redis for rate limiting and response caching |
| Deployment | Docker Compose on DigitalOcean, with Caddy reverse proxy + TLS |

---

## Architectural Principles

- **API-first**: every capability exposed as a versioned REST endpoint under `/api/v1/`
- **Async throughout**: no synchronous I/O in request handlers — all DB calls use `AsyncSession`
- **DB-primary**: PostgreSQL is the authoritative store; no business logic in Redis
- **TDD**: write pytest tests before implementation; target >80% coverage on core logic
- **No global state**: configuration via environment variables only — no hardcoded values
- **Fail loudly**: unhandled errors return 500 with a structured JSON body and a correlation ID, never silent failures

---

## Codebase Inventory

### Core (`src/`)

| File | LOC | Status | Role |
|---|---:|---|---|
| `src/main.py` | 42 | ✅ Active | FastAPI app factory, router registration |
| `src/config.py` | 38 | ✅ Active | `Settings` class via pydantic-settings |
| `src/dependencies.py` | 55 | ✅ Active | FastAPI dependency injectors (DB session, current user) |

### Database layer (`src/db/`)

| File | LOC | Status | Role |
|---|---:|---|---|
| `src/db/session.py` | 28 | ✅ Active | AsyncSession factory, engine setup |
| `src/db/models.py` | 110 | ✅ Active | SQLAlchemy ORM models: `User`, `Project`, `Task` |
| `src/db/migrations/` | — | ✅ Active | Alembic migration scripts |

### API layer (`src/api/`)

| File | LOC | Status | Role |
|---|---:|---|---|
| `src/api/projects.py` | 98 | ✅ Active | CRUD router for `/api/v1/projects` |
| `src/api/tasks.py` | 134 | ✅ Active | CRUD router for `/api/v1/tasks` |
| `src/api/auth.py` | 0 | ❌ Missing | JWT login/refresh endpoints — not yet implemented |

### Services (`src/services/`)

| File | LOC | Status | Role |
|---|---:|---|---|
| `src/services/task_service.py` | 88 | ✅ Active | Business logic: task creation, status transitions |
| `src/services/auth_service.py` | 0 | ❌ Missing | Token creation, validation — not yet implemented |

### Tests (`tests/`)

| File | LOC | Status | Role |
|---|---:|---|---|
| `tests/test_projects.py` | 120 | ✅ Active | 14 tests for project CRUD |
| `tests/test_tasks.py` | 145 | ✅ Active | 18 tests for task CRUD |
| `tests/conftest.py` | 62 | ✅ Active | Fixtures: test DB, async client |

### Known Configuration Values

```
DATABASE_URL = postgresql+asyncpg://user:pass@localhost/taskflow  (required)
REDIS_URL    = redis://localhost:6379/0                           (required, unused in code)
SECRET_KEY   = changeme                                          (⚠ must be rotated before auth ships)
ACCESS_TOKEN_EXPIRE_MINUTES = 30                                 (default)
REFRESH_TOKEN_EXPIRE_DAYS   = 7                                  (default)
```

---

## Feature Index

| # | Feature Name | Status | Notes |
|---|---|---|---|
| 0 | Pre-Work: Security + Stability | ⚠️ Partial | `SECRET_KEY` rotation + `cryptography` upgrade pending |
| 1 | Project CRUD | ✅ Complete | `GET /projects`, `POST`, `PATCH`, `DELETE` — all tested |
| 2 | Task CRUD | ✅ Complete | Full CRUD + status transitions — all tested |
| 3 | JWT Authentication | [ ] | See PLAN-001 |
| 4 | Redis Rate Limiting | [ ] | Blocked by Feature 3 (auth required first) |
| 5 | Response Caching (Redis) | [ ] | Blocked by Feature 4 |
| 6 | Caddy TLS + Production Deploy | [ ] | Blocked by Feature 3 |

---

## Known Issues & Technical Debt

- `SECRET_KEY` was committed in plaintext on 2026-03-10 — must be rotated and scrubbed from git history before auth ships (Pre-Work §0)
- No rate limiting on any endpoint — risk of abuse; blocked by auth (Feature 4)
- `src/api/tasks.py:filter_tasks()` at line 87 does a full table scan on the `tasks` table — needs an index on `(project_id, status)` before scale testing
- 3 flaky tests in `tests/test_tasks.py` related to async teardown timing (lines 201–215, non-blocking but noisy)

---

## Known Unknowns

- Refresh token revocation strategy not decided — simple expiry or Redis blocklist?
- Whether to add user registration via API or seed users manually for v1
- Rate limiting approach: in-process (slowapi) vs. Caddy middleware

---

## Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|---|---|---|---|
| 2026-03-15 | Use FastAPI over Flask | Native async support, automatic OpenAPI docs, strong type safety via Pydantic | Flask (sync by default, more manual), Django (too heavy for API-only) |
| 2026-03-15 | SQLAlchemy 2.0 async ORM | Avoids blocking DB calls in async handlers; integrates cleanly with FastAPI DI | Raw asyncpg (more boilerplate), Tortoise ORM (smaller community) |
| 2026-03-20 | Keep Redis in Docker Compose but unused for v1 | Avoids service churn when rate limiting is added in Feature 4 | Remove Redis until needed (cleaner now, more work later) |
| 2026-04-01 | Created v1.0 spec.md | Project initialisation | n/a |

---

# FEATURE 0 — Pre-Work: Security & Stability

## Goal

Ensure no credentials are exposed and critical dependencies are patched before auth is implemented.

## Tasks

- [ ] Rotate `SECRET_KEY`: generate with `openssl rand -hex 32`, set in `.env`, remove old value from git history using `git filter-repo --path src/config.py --invert-paths` then force-push
- [ ] Upgrade `cryptography`: `pip install cryptography==42.0.5`, run full test suite, update `requirements.txt`
- [ ] Add `SECRET_KEY` to `.env.example` with a placeholder value

## Verification

- `git log --all -p -- src/config.py | grep SECRET_KEY` returns nothing
- `pip show cryptography | grep Version` returns `42.0.5`
- `pytest tests/ -q` exits 0

---

# FEATURE 3 — JWT Authentication

## Goal

Add token-based auth so all project and task endpoints require a valid JWT. Unauthenticated requests receive 401.

## Existing Code to Reference

- `src/dependencies.py` — add `get_current_user` dependency here
- `src/db/models.py` — `User` model already exists with `hashed_password` field
- `src/main.py` — mount auth router here

## Tasks

- [ ] Write tests for `POST /api/v1/auth/login` and `POST /api/v1/auth/refresh`
- [ ] Write tests for protected endpoint returning 401 without token
- [ ] Implement `src/services/auth_service.py`: `create_access_token()`, `verify_token()`, `hash_password()`, `verify_password()`
- [ ] Implement `src/api/auth.py`: login and refresh endpoints
- [ ] Add `get_current_user` dependency to all project and task routers
- [ ] Update `current_state_report.md`

## Acceptance Criteria

- [ ] `pytest tests/ -q` exits 0 with no failures
- [ ] `curl -X GET http://localhost:8000/api/v1/projects` returns 401
- [ ] `curl -X POST http://localhost:8000/api/v1/auth/login -d '{"email":...}'` returns a valid access token
- [ ] Auth service coverage ≥ 90%
