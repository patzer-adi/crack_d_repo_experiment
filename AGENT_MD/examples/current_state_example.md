# TaskFlow API — Current State Report

**Date:** 2026-04-01
**Prepared for:** Sprint planning — Feature 3 (JWT Authentication) kickoff
**Scope:** Full source scan of `src/`, `tests/`, `docker-compose.yml`, `.env.example`

---

## Update — 2026-04-01 [Baseline audit before auth sprint]

- Completed full source scan
- Discovered `SECRET_KEY` was committed in plaintext on 2026-03-10 — added to Pre-Work
- Confirmed Redis is installed but zero application code references it
- Test suite: 32 passed, 0 failed, 3 skipped (async teardown flakes)

---

## 1. Executive summary

The codebase is in a working but pre-production state. Project and task CRUD endpoints are complete, tested, and deployed to a staging droplet. The single biggest risk is that authentication does not exist — all endpoints are open to anyone who can reach the server. The server IP is currently unexposed, but auth must ship before any DNS record is created. Redis is installed and configured in Docker Compose but is not referenced anywhere in application code. Test coverage is 48% (32 of ~66 branches covered), below the 80% target.

---

## 2. Source code inventory

### Core files by size

| File | LOC | Role |
|---|---:|---|
| `src/api/tasks.py` | 134 | Task CRUD router |
| `src/api/projects.py` | 98 | Project CRUD router |
| `src/db/models.py` | 110 | ORM models: User, Project, Task |
| `src/services/task_service.py` | 88 | Task business logic |
| `src/dependencies.py` | 55 | FastAPI dependency injectors |
| `src/config.py` | 38 | pydantic-settings config |
| `src/main.py` | 42 | App factory, router registration |
| `src/db/session.py` | 28 | AsyncSession factory |

### API layer

| Component | Count | Key files |
|---|---:|---|
| Routers | 2 | `src/api/projects.py`, `src/api/tasks.py` |
| Services | 1 | `src/services/task_service.py` |
| Tests | 32 | `tests/test_projects.py` (14), `tests/test_tasks.py` (18) |

### Missing / not yet implemented

| File | Reason missing |
|---|---|
| `src/api/auth.py` | JWT auth not yet built (Feature 3) |
| `src/services/auth_service.py` | JWT auth not yet built (Feature 3) |

---

## 3. Configuration audit

| Setting | Default | Source | Notes |
|---|---|---|---|
| `DATABASE_URL` | none | `.env` (required) | Points to local PostgreSQL in dev |
| `REDIS_URL` | `redis://localhost:6379/0` | `.env` | Present but unused in application code |
| `SECRET_KEY` | `changeme` | `.env` | ⚠️ Was committed in plaintext on 2026-03-10 — must rotate |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | `src/config.py` | Reasonable default |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | `src/config.py` | Reasonable default |

---

## 4. Test suite status

| Suite | Passed | Failed | Skipped | Notes |
|---|---:|---:|---:|---|
| Unit tests | 14 | 0 | 0 | `tests/test_projects.py` |
| Integration | 18 | 0 | 3 | `tests/test_tasks.py` — 3 async teardown flakes |
| **Total** | **32** | **0** | **3** | Coverage: 48% |

To reproduce: `pytest tests/ -v --cov=src --cov-report=term-missing`

---

## 5. Infrastructure & deployment

| Component | Status | Notes |
|---|---|---|
| Docker Compose | ✅ Working | `docker-compose up` starts API + PostgreSQL + Redis |
| GitHub Actions CI | ✅ Working | Runs `pytest` on every push to `main` |
| Production deploy | ⚠️ Manual | SSH + `docker-compose pull && docker-compose up -d` on droplet |
| TLS / HTTPS | ❌ Not configured | Caddy reverse proxy planned but not configured (blocked by auth) |
| DNS | ❌ Not set | No public domain yet — server IP is private |

---

## 6. Known issues & technical debt

- **[CRITICAL]** `SECRET_KEY` committed in plaintext on 2026-03-10. Must rotate and scrub git history before auth ships. See Pre-Work in `spec.md`.
- **[HIGH]** No authentication on any endpoint. Server is safe only because IP is unexposed.
- **[HIGH]** `cryptography` package at 41.0.3 — CVE-2023-49083 applies. Upgrade to 42.0.5.
- **[MEDIUM]** Full table scan in `src/api/tasks.py:filter_tasks()` line 87. Needs index on `tasks(project_id, status)` before load testing.
- **[LOW]** 3 flaky tests in `tests/test_tasks.py` (lines 201–215) — async session teardown race condition. Non-blocking but noisy.
- **[LOW]** Redis installed and in Docker Compose but zero application code uses it — wasted container resource in dev.
