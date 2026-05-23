# PLAN-001: JWT Authentication

**Created:** 2026-04-02
**Status:** Completed
**Addresses:** All API endpoints are unauthenticated. TaskFlow cannot be exposed publicly until JWT auth is implemented (identified in RECON-001 Priority 1 and `spec.md` Feature 3).

---

## 1. Context & motivation

The current state report (`plan/current_state_report.md`, §6) and reconciliation report (`reconciliation_example.md`, §1.1) both flag the absence of authentication as the top blocker for production deployment. Every endpoint under `/api/v1/` returns data to any caller with network access to the server.

The `User` model and `hashed_password` field already exist in `src/db/models.py`, so we are not designing a user schema from scratch — we are adding the auth layer on top of existing user records.

Pre-Work task 1.1 (rotate `SECRET_KEY`) must be completed before this plan ships, because the JWT signing key must not be the compromised `changeme` value.

---

## 2. Goals

- **G1:** `POST /api/v1/auth/login` accepts `{email, password}` and returns `{access_token, refresh_token, token_type}`.
- **G2:** `POST /api/v1/auth/refresh` accepts a valid refresh token and returns a new access token.
- **G3:** All `GET`, `POST`, `PATCH`, `DELETE` endpoints under `/api/v1/projects` and `/api/v1/tasks` return HTTP 401 when called without a valid `Authorization: Bearer <token>` header.
- **G4:** Test coverage for `src/services/auth_service.py` and `src/api/auth.py` is ≥ 90%.
- **G5:** `SECRET_KEY` is loaded from environment — not hardcoded in any source file.

---

## 3. Non-goals

- User registration UI — there is no frontend in this repository.
- User management endpoints (`PATCH /users/me`, `DELETE /users/me`) — deferred to PLAN-003.
- Role-based access control (RBAC) — all authenticated users have equal access for now.
- OAuth2 / social login — not in scope.

---

## 4. Approach

### 4.1 Token implementation

We use `python-jose[cryptography]` for JWT encoding/decoding. Tokens are signed with HS256 using the `SECRET_KEY` env var. Access tokens expire in 30 minutes; refresh tokens in 7 days (both configurable via `src/config.py`).

We do not store tokens in the database. Refresh tokens are opaque JWTs — revocation is handled by expiry only. This is acceptable for the current scale; a token blocklist can be added later if needed.

### 4.2 Password hashing

Use `passlib[bcrypt]` with bcrypt rounds = 12. The `User.hashed_password` DB column already exists. We add `hash_password()` and `verify_password()` to `src/services/auth_service.py`.

### 4.3 FastAPI integration

We add a `get_current_user` dependency to `src/dependencies.py`. This dependency reads the `Authorization` header, validates the JWT, and returns the `User` ORM object. All existing project and task routers add this as a parameter — one line change per router function signature.

We mount a new `src/api/auth.py` router at `/api/v1/auth` in `src/main.py`.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Pre-work: confirm `SECRET_KEY` is rotated and not in git history | 15 min | — |
| 2 | Write tests for `auth_service.py`: hash, verify, create_token, verify_token | 45 min | — |
| 3 | Implement `src/services/auth_service.py` | 45 min | 2 |
| 4 | Write tests for `POST /api/v1/auth/login` and `POST /api/v1/auth/refresh` | 30 min | 2 |
| 5 | Implement `src/api/auth.py` with login and refresh endpoints | 45 min | 3, 4 |
| 6 | Write tests: existing endpoints return 401 without token | 20 min | — |
| 7 | Add `get_current_user` dependency to `src/dependencies.py` | 20 min | 3 |
| 8 | Apply `get_current_user` dependency to all routes in `src/api/projects.py` and `src/api/tasks.py` | 20 min | 7 |
| 9 | Mount auth router in `src/main.py` | 10 min | 5 |
| 10 | Run full test suite; fix any failing tests | 30 min | 6, 8, 9 |
| 11 | Update `current_state_report.md` | 15 min | 10 |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Existing tests break when 401 is added to all routes | High | Medium | Tasks 6 and 8 are sequenced to add auth to tests before applying to routes; run suite after each change |
| `SECRET_KEY` not yet rotated when plan starts | Low | Critical | Task 1 is a gate: if key is not rotated, stop and complete Pre-Work first |
| Refresh token reuse after expiry gives misleading 422 instead of 401 | Low | Low | Add explicit expiry check in `verify_token()`; covered by tests in Task 2 |
| `python-jose` has known issues with certain JWK formats | Low | Low | We use HS256 only (symmetric key) — affected code paths don't apply |

---

## 7. Success criteria

- [ ] **G1 verified:** `curl -X POST .../auth/login -d '{"email":"test@test.com","password":"hunter2"}'` returns `{access_token, refresh_token, token_type: "bearer"}`
- [ ] **G2 verified:** `curl -X POST .../auth/refresh -H "Authorization: Bearer <refresh_token>"` returns a new `access_token`
- [ ] **G3 verified:** `curl -X GET .../projects` returns `{"detail":"Not authenticated"}` with status 401
- [ ] **G4 verified:** `pytest --cov=src/services/auth_service --cov=src/api/auth --cov-report=term` shows ≥ 90% coverage
- [ ] **G5 verified:** `grep -r "SECRET_KEY" src/` shows only `os.getenv("SECRET_KEY")` or `settings.SECRET_KEY` — no string literal value
- [ ] `pytest tests/ -q` exits 0 with 0 failures, 0 skipped
- [ ] `current_state_report.md` updated with Feature 3 completion summary

---

## 8. References

- `AGENT_MD/spec.md` — Feature 3 (JWT Authentication), Feature 0 (Pre-Work task 1.1)
- `AGENT_MD/plan/current_state_report.md` — §6 Known Issues (auth gap, SECRET_KEY)
- `AGENT_MD/examples/reconciliation_example.md` — Priority 1.1 (SECRET_KEY), Priority 1.2 (cryptography)
- `src/db/models.py` — existing `User` model with `hashed_password` field
- `src/dependencies.py` — where `get_current_user` will be added
- python-jose docs: https://python-jose.readthedocs.io/
- passlib docs: https://passlib.readthedocs.io/
