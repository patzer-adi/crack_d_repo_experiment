# Reconciliation Report — spec.md ↔ current_state_report.md ↔ Actual Implementation

**Report ID:** RECON-001
**Date:** 2026-04-01
**Scope:** Full cross-verification of `spec.md`, `plan/current_state_report.md`, and the live codebase (`src/`, `tests/`)
**Purpose:** Identify all gaps between documentation and reality before the auth sprint begins

---

## Executive Summary

The spec and current state report are broadly consistent with reality for completed features (Project CRUD, Task CRUD). The critical gap is security: a plaintext `SECRET_KEY` was committed to git history and has not been rotated, and no authentication exists on any endpoint. A secondary gap is that `spec.md` describes Redis caching as "installed," which is technically true but misleading — no application code uses Redis. Test coverage is reported as "target >80%" in the spec but the actual figure is 48%. Overall: feature documentation is accurate; security and infrastructure claims overstate reality.

### Documents vs Reality — Key Discrepancies Found

| Area | spec.md Says | current_state_report.md Says | Actual Code |
|---|---|---|---|
| Auth | "JWT auth is next priority" | "No authentication" | No `src/api/auth.py` or `src/services/auth_service.py` exist |
| Redis | "Redis 7 (installed)" | "Installed, not yet wired in" | Zero imports of Redis in any `src/` file |
| `SECRET_KEY` | "must be rotated before auth ships" | "Was committed 2026-03-10, must rotate" | `changeme` visible in `git log` history |
| Test coverage | ">80% target" | "48% actual" | `pytest --cov` output confirms 48% |
| TLS / Caddy | Listed in Target stack | "Not configured" | No `Caddyfile` in repo |

---

## Priority 1 — 🔴 CRITICAL (Do Immediately)

### 1.1 Rotate Exposed `SECRET_KEY`

**Gap:** `changeme` was committed to `src/config.py` on 2026-03-10. It is visible in `git log --all -p`. Anyone with repo access can forge JWT tokens once auth ships.

**Actions:**
1. Generate a new key: `openssl rand -hex 32`
2. Add it to `.env` (not tracked by git)
3. Remove old value from git history: `git filter-repo --path src/config.py --invert-paths` or use a targeted `git filter-repo` rewrite
4. Force-push to remote and notify all collaborators to re-clone

**Files to modify:**
- `src/config.py` — remove hardcoded default; require env var
- `.env.example` — add `SECRET_KEY=<generate with: openssl rand -hex 32>`
- `.gitignore` — confirm `.env` is listed

**Verification:** `git log --all -p -- src/config.py | grep SECRET_KEY` returns nothing.

---

### 1.2 Upgrade `cryptography` Package

**Gap:** `cryptography==41.0.3` is installed. CVE-2023-49083 allows a NULL pointer dereference when parsing certain PKCS12 certificates. Affects any code that processes external certificates.

**Actions:**
1. `pip install "cryptography>=42.0.5"`
2. Run full test suite: `pytest tests/ -q`
3. Update `requirements.txt` or `pyproject.toml`

**Files to modify:**
- `requirements.txt` — bump `cryptography` version pin

**Verification:** `pip show cryptography | grep Version` returns `42.0.5` or higher; test suite exits 0.

---

## Priority 2 — 🟠 HIGH (Architectural Alignment)

### 2.1 Redis Claim in spec.md Is Misleading

**Gap:** `spec.md` Tech Stack table lists "Redis 7" under Current stack, implying it is in use. It is only running as a Docker container. Not a single line of application code imports or calls Redis.

**Options:**

**Option A: Update spec.md to clarify (recommended)**
1. Change Redis row label to "Redis 7 (container running; not yet integrated)"
2. Note in Feature Index that Feature 4 (rate limiting) is the first Redis integration point

**Option B: Remove Redis from Current stack, move to Target only**
1. Move Redis row to the Target table
2. Note that the Docker Compose file includes it for readiness

**Decision:** Option A — the container being present is real and useful to document; clarifying the label is sufficient.

**Actions:**
1. Update `spec.md` Tech Stack table — Current row for Redis
2. Update `current_state_report.md` §5 Infrastructure note for Redis

---

### 2.2 Test Coverage Gap: 48% vs >80% Target

**Gap:** `spec.md` states ">80% coverage on core logic" as an architectural principle. Actual coverage is 48%. Auth service and API are untested (they don't exist yet), but even the existing code is under-covered.

**Actions:**
1. After auth is implemented (Feature 3), run `pytest --cov=src --cov-report=term-missing`
2. Identify uncovered branches in `src/services/task_service.py` (currently 61% covered)
3. Add missing tests as part of each feature plan going forward — do not ship a feature with coverage below 80% for that module

**This is not a blocker but must be tracked.** Add as a standing item in every plan's success criteria.

---

## Priority 3 — 🟡 MEDIUM (Functional Gaps)

### 3.1 `filter_tasks()` Full Table Scan

**Gap:** `src/api/tasks.py` line 87 runs `SELECT * FROM tasks WHERE project_id = ? AND status = ?` with no index. On the current dataset (< 500 rows) this is imperceptible. It will become a problem at > 10,000 rows.

**Actions:**
1. Create Alembic migration: `CREATE INDEX ix_tasks_project_status ON tasks (project_id, status)`
2. Add to PLAN-002 (or the next available plan)

**Files:** `src/db/migrations/` (new migration file), `tests/test_tasks.py` (add a query-plan assertion)

---

### 3.2 No Production Deployment Automation

**Gap:** `spec.md` lists GitHub Actions CI/CD but the CD half is manual SSH. The "CI/CD" label overstates reality.

**Actions:**
1. Update `spec.md` CI/CD row to "GitHub Actions (CI only; CD is manual SSH)"
2. Add Feature 7 to spec.md Feature Index: "Automated CD via GitHub Actions + DigitalOcean API"

---

## Priority 4 — 🟢 LOW (Documentation & Cleanup)

### 4.1 Three Flaky Tests

**Gap:** `tests/test_tasks.py` lines 201–215 have async teardown timing issues causing intermittent skips. They appear in the CI log and reduce confidence in the suite.

**Actions:**
1. Add `@pytest.mark.asyncio(loop_scope="session")` and a shared teardown fixture to eliminate race condition
2. Target: 0 skipped tests in CI

### 4.2 `REDIS_URL` in `.env.example` Has No Explanation

**Gap:** A new contributor sees `REDIS_URL=redis://localhost:6379/0` in `.env.example` but nothing explains that it is unused. Could cause confusion.

**Actions:**
1. Add a comment above the line: `# Required by Docker Compose; not yet used in application code (see Feature 4)`

---

## Action Plan Summary

| # | Priority | Action | Est. Effort |
|---|---|---|---|
| 1.1 | 🔴 Critical | Rotate SECRET_KEY and scrub git history | 1 hr |
| 1.2 | 🔴 Critical | Upgrade cryptography to 42.0.5 | 15 min |
| 2.1 | 🟠 High | Clarify Redis label in spec.md | 10 min |
| 2.2 | 🟠 High | Track coverage gap in every future plan's success criteria | 10 min |
| 3.1 | 🟡 Medium | Add DB index on tasks(project_id, status) in PLAN-002 | 30 min |
| 3.2 | 🟡 Medium | Update spec.md CI/CD label; add Feature 7 | 15 min |
| 4.1 | 🟢 Low | Fix flaky test teardown | 30 min |
| 4.2 | 🟢 Low | Add comment to REDIS_URL in .env.example | 5 min |
