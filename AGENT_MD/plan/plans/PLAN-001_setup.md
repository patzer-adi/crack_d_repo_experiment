# PLAN-001: Pre-Work Setup

**Created:** 2026-05-07
**Status:** Completed
**Addresses:** Establish a clean, version-controlled project skeleton so that POC work (PLAN-002, Feature 1 in `AGENT_MD/spec.md`) can begin immediately. Currently the project has only `AGENT_MD/` scaffolding plus the curated `problems/finalrepList.HTML` source list — no git repo, no working directories, no verified Python toolchain.

---

## 1. Context & motivation

`AGENT_MD/spec.md` v1.1 defines Feature 0 as the prerequisite for all subsequent work. The spec mandates POC-first ordering: the very next feature (Feature 1) generates an end-to-end lesson on 3Sum with **zero tooling** — only Python's standard library and a terminal HTTP server. For that to start cleanly we need:

- A git repository tracking everything from the first commit (so the curated `problems/finalrepList.HTML` and its history are preserved).
- The full target directory tree (`dashboard/`, `scripts/`, `data/`, `skills/ds/`, `skills/patterns/`, `lessons/`) — even if empty — so later features add files into known locations rather than improvising paths.
- A confirmed Python 3.10+ install, since the spec commits to stdlib-only Python tooling for `scripts/server.py` and `scripts/import_problems.py`.

This plan is intentionally narrow. It does **not** write any Python code, dashboard, parser, or skill files. Those are downstream plans.

---

## 2. Goals

- **G1:** Project root is a clean git repository whose initial commit includes `AGENT_MD/`, `problems/finalrepList.HTML`, a `.gitignore`, and a placeholder under each new directory. Verifiable by `git log --oneline` showing one commit and `git status` showing a clean tree.
- **G2:** All six target directories exist and are git-tracked: `dashboard/`, `scripts/`, `data/`, `skills/ds/`, `skills/patterns/`, `lessons/`. Verifiable by `ls -d dashboard scripts data skills/ds skills/patterns lessons` returning all six without error.
- **G3:** Python 3.10+ is confirmed on the path. Verifiable by `python3 --version` reporting `Python 3.10.*` or higher.
- **G4:** `lesson.html` files are **not** gitignored (per spec §Decision Log: lessons are committed for versioned learning history). Verifiable by `git check-ignore lessons/example/lesson.html` returning non-zero (i.e. not ignored).
- **G5:** `__pycache__/`, `*.pyc`, and `.DS_Store` are gitignored. Verifiable by `git check-ignore __pycache__ foo.pyc .DS_Store` returning all three.

---

## 3. Non-goals

- No Python source code beyond verifying the interpreter version. `scripts/server.py` and `scripts/import_problems.py` belong to later plans.
- No dashboard HTML/JS. That is part of the dashboard plan after the POC milestone.
- No skill files (`skills/ds/array.md` etc.). Those are the deliverables of PLAN-002 (POC Feature 1).
- No parsing of `problems/finalrepList.HTML`. The file is only added to git unchanged.
- No CI, no pre-commit hooks, no virtualenv. Keeps tooling weight at zero per the "stdlib only, no pip" architectural principle.

---

## 4. Approach

The work is essentially shell commands plus one small file (`.gitignore`). It runs in one session and is fully reversible (`rm -rf .git` if anything goes wrong). Sequence:

### 4.1 Repository initialisation

1. `git init` in `/home/mpiuser/MPI_JOBS/crack_d/`.
2. Create `.gitignore` with the patterns from G4/G5.
3. Stage and commit nothing yet — directories first.

### 4.2 Directory skeleton

Create the six target directories and place a `.gitkeep` file in each so git tracks the empty directory. `.gitkeep` is a convention, not a git feature — git only tracks files, so each empty directory needs at least one tracked file to survive in the index.

```
dashboard/.gitkeep
scripts/.gitkeep
data/.gitkeep
skills/ds/.gitkeep
skills/patterns/.gitkeep
lessons/.gitkeep
```

### 4.3 Python version verification

`python3 --version` must report ≥ 3.10. If it reports 3.9 or below, **stop the plan** and surface to the user — the spec commits to features (e.g. structural pattern matching, modern `http.server` defaults) that benefit from 3.10+. Do not attempt to install or upgrade Python silently.

### 4.4 Initial commit

One commit including:
- The new `.gitignore`
- All six `.gitkeep` files
- The pre-existing `AGENT_MD/` tree (already on disk)
- The pre-existing `problems/finalrepList.HTML` (already on disk)

Commit message: `Initial commit: project skeleton (Feature 0 / PLAN-001)`.

### 4.5 Verification

Per rules.md §5.11 (test-first), the substitution for unit tests on a setup-only plan is a verification block: each goal has an explicit shell command whose output confirms the goal is met. Run all of §7 commands; the plan is complete only when all return their expected output.

### Alternatives considered

- **`git init` with an initial empty commit (`--allow-empty`) before adding any files.** Rejected — adds noise to history with no benefit; one clean commit is fine.
- **Skip `.gitkeep` and let directories be created lazily by feature plans.** Rejected — `data/problems.json` and `skills/ds/array.md` need parent dirs to exist; pre-creating costs nothing and removes a class of "directory not found" surprises.
- **Use `pyenv` or a venv.** Rejected — spec architectural principle "stdlib only, no pip" makes a venv unnecessary, and pyenv adds a dependency not present locally.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Run `python3 --version`; abort plan and notify user if < 3.10 | 1 min | — |
| 2 | `git init` in project root | 1 min | 1 |
| 3 | Write `.gitignore` with `__pycache__/`, `*.pyc`, `.DS_Store` | 2 min | 2 |
| 4 | Create six target directories with `.gitkeep` files | 3 min | 2 |
| 5 | `git add .` and review with `git status` (no surprises like editor swap files) | 2 min | 3, 4 |
| 6 | Commit: `Initial commit: project skeleton (Feature 0 / PLAN-001)` | 1 min | 5 |
| 7 | Run all verification commands from §7; confirm each passes | 3 min | 6 |
| 8 | Write REPORT-001 and flip PLAN-001 status to `Completed` | 10 min | 7 |

Total estimate: ~25 minutes.

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Python on the system is 3.9 or older | Low | High | Task 1 runs first and aborts the plan; user is informed and asked to install 3.10+ |
| User has an existing `.git` directory we're unaware of | Low | Medium | `ls -la` for `.git` before `git init`; if present, surface to user instead of overwriting |
| Accidentally committing a sensitive file from the working tree | Low | High | `git status` review (task 5) before commit; only files listed are `.gitignore`, six `.gitkeep` files, the pre-existing `AGENT_MD/` and `problems/` trees |
| `.gitkeep` files become permanent clutter when directories fill up | Low | Low | They are removed organically by the first feature plan that adds real files to each directory; no action needed now |
| User later wants `lesson.html` *not* committed (large diffs, binary-like) | Low | Medium | Documented in spec Decision Log; reversible by adding one line to `.gitignore` and `git rm --cached` |

---

## 7. Success criteria

All of the following must pass before the plan is marked `Completed`:

- [ ] **G1** — `git log --oneline` shows exactly one commit; `git status` reports `nothing to commit, working tree clean`.
- [ ] **G2** — `ls -d dashboard scripts data skills/ds skills/patterns lessons` lists all six directories without error.
- [ ] **G3** — `python3 --version` reports `Python 3.10.x` or higher.
- [ ] **G4** — `git check-ignore lessons/example/lesson.html` exits non-zero (file is *not* ignored).
- [ ] **G5** — `git check-ignore __pycache__ foo.pyc .DS_Store` exits zero for all three.
- [ ] REPORT-001 written under `AGENT_MD/plan/reports/` per rules.md §4.
- [ ] `AGENT_MD/spec.md` Codebase Inventory updated with `.gitignore` row; Feature Index Feature 0 status flipped to ✅.

---

## 8. References

- `AGENT_MD/spec.md` — Feature 0 task list, ⚠️ Critical Pre-Work section, Decision Log entry on committing lessons
- `AGENT_MD/plan/rules.md` — §3 plan template, §5 style rules, §5.11 test-first substitution for setup-only plans
- `problems/finalrepList.HTML` — pre-existing curated problem list to be preserved by the initial commit
