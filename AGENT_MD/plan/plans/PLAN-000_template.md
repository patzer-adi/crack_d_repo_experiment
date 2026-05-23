# PLAN-001: [Title — Example: Initial Setup & Security Hardening]

**Created:** YYYY-MM-DD
**Status:** Draft
**Addresses:** _[One-line description of the gap or need this plan targets.]_

---

## 1. Context & motivation

_[Why this plan exists. Link to the current state report or prior reports that surfaced the need.]_

Example: The Current State Report (`plan/current_state_report.md`) identified that the project has no authentication system and API keys are stored in plaintext config files.

---

## 2. Goals

- **G1:** _[Measurable outcome — e.g., "No plaintext credentials in the repository or git history."]_
- **G2:** _[Measurable outcome — e.g., "All API endpoints require authentication."]_
- **G3:** _[Measurable outcome — e.g., "Test suite covers auth flows with >90% branch coverage."]_

---

## 3. Non-goals

- _[What's explicitly out of scope — e.g., "Building a user registration UI — that is PLAN-002."]_
- _[Prevents scope creep and sets expectations for AI agents.]_

---

## 4. Approach

_[Detailed description of the technical approach. Include architecture decisions, trade-offs, and alternatives considered.]_

### 4.1 _[Subsection — e.g., "Credential management"]_

1. _Step 1_
2. _Step 2_

### 4.2 _[Subsection — e.g., "JWT authentication"]_

1. _Step 1_
2. _Step 2_

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | _Create `.env.example` with all required env vars_ | 15 min | — |
| 2 | _Add `python-dotenv` and load `.env` in `config.py`_ | 30 min | 1 |
| 3 | _Write auth middleware tests_ | 1 hr | — |
| 4 | _Implement JWT auth middleware_ | 2 hr | 3 |
| 5 | _Write integration tests for protected endpoints_ | 1 hr | 4 |
| 6 | _Update `current_state_report.md`_ | 15 min | 5 |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| _Breaking existing API consumers_ | Medium | High | _Version the API (`/api/v1/`); keep old endpoints working during transition_ |
| _Token expiry edge cases_ | Low | Medium | _Include refresh token flow from the start_ |

---

## 7. Success criteria

- [ ] All goals from §2 verified
- [ ] All tests green
- [ ] `current_state_report.md` updated
- [ ] No regressions in existing test suite

---

## 8. References

- `AGENT_MD/spec.md` — Feature 0 (Pre-Work)
- `AGENT_MD/plan/current_state_report.md` — §6 Known Issues
