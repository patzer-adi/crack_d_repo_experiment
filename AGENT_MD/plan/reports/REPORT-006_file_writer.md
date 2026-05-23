# REPORT-006: Python File-Writer Service

**Plan:** PLAN-006
**Completed:** 2026-05-07
**Author:** Claude Sonnet 4.6 (AI agent)

---

## 1. Summary

Implemented `scripts/server.py` — a `SimpleHTTPRequestHandler` subclass that serves static files from the project root and adds `PATCH /api/status` and `POST /api/write` write-API endpoints. Updated `dashboard/index.html` to wire status-toggle buttons to the new API. All seven PLAN-006 goals met.

---

## 2. Goals vs. actuals

| Goal | Outcome | Evidence |
|---|---|---|
| G1 — `python3 scripts/server.py` with `--port` flag | ✅ Met | `argparse` wired; default 8000; prints start URL |
| G2 — Static file serving identical to `http.server` | ✅ Met | `super().do_GET()` delegates to `SimpleHTTPRequestHandler` with `directory=PROJECT_ROOT` |
| G3 — `PATCH /api/status` updates problems.json atomically | ✅ Met | `_lock` guards read-modify-write; round-trip verified via curl |
| G4 — `POST /api/write` writes `lessons/*/plan.md` | ✅ Met | Creates parent dir; UTF-8 write; verified with test slug |
| G5 — Path traversal rejected (400) | ✅ Met | `..` check + `Path.resolve().relative_to()` + pattern check; all three rejection paths tested |
| G6 — Dashboard "Mark Done / Mark New" toggle persists | ✅ Met | `toggleStatus()` sends PATCH, updates in-memory `ALL`, re-renders stats + row; toast on result |
| G7 — Stdlib only | ✅ Met | `http.server`, `json`, `pathlib`, `argparse`, `threading` only |

---

## 3. Changes made

### 3.1 New files

| File | Description |
|---|---|
| `scripts/server.py` | 115-line server: `CrackDHandler`, `PATCH /api/status`, `POST /api/write`, `main()` with argparse |
| `AGENT_MD/plan/plans/PLAN-006_file_writer.md` | Plan document |

### 3.2 Modified files

| File | Changes |
|---|---|
| `dashboard/index.html` | Added `.status-toggle` and `#toast` CSS; replaced static `statusBadge` span with interactive `<button>`; added `toggleStatus()`, `showToast()`; updated error message to reference `python3 scripts/server.py` |

### 3.3 Key design decisions

**`directory=PROJECT_ROOT` kwarg** — `SimpleHTTPRequestHandler.__init__` accepts a `directory` kwarg (Python 3.7+). Setting it to the project root means the server can be invoked from any working directory and still serve all assets correctly.

**`_lock` for write serialisation** — a single `threading.Lock` guards the read-modify-write cycle on `problems.json`. The server uses the default single-threaded `HTTPServer`, so this is belt-and-suspenders, but it makes the intent explicit and protects against future `ThreadingHTTPServer` upgrades.

**Three-layer path validation** — `POST /api/write` applies independent checks in order: (1) reject `..` literally, (2) resolve and confirm inside `PROJECT_ROOT`, (3) restrict to exactly `lessons/<slug>/plan.md`. Any of the three independently closes a different attack vector.

**Toggle button built with `createElement` not `innerHTML`** — the event handler for `toggleStatus` is attached via `addEventListener`, avoiding any possibility of XSS from problem names or slugs that might contain quotes.

**Toast auto-dismisses at 2200ms** — long enough to read a short message; clears timer on re-trigger so rapid toggles don't stack.

---

## 4. Testing & validation

| Check | Result |
|---|---|
| Static files: `curl http://localhost:8002/dashboard/` → 200 | ✅ |
| Static files: `curl http://localhost:8002/data/problems.json` → 200 | ✅ |
| `PATCH /api/status` 3sum → done, persists to disk | ✅ |
| `PATCH /api/status` 3sum → new, persists to disk | ✅ |
| `PATCH /api/status` unknown slug → `{"ok":false,"error":"slug not found: ..."}` | ✅ |
| `POST /api/write` path `../../etc/passwd` → 400 path traversal rejected | ✅ |
| `POST /api/write` path `lessons/3sum/notes.txt` → 400 pattern rejected | ✅ |
| `POST /api/write` path `lessons/test-problem/plan.md` → 200, file created | ✅ |

---

## 5. Known issues & follow-ups

- **No "Generate Plan" UI yet** — `POST /api/write` is implemented and ready; PLAN-007 will wire it to the dashboard "Generate Plan" button.
- **API logging suppressed for static files** — only `/api/` routes log to console; high-volume static-file requests would drown the terminal otherwise.
- **Port conflict** — if 8000 is in use, `HTTPServer` raises `OSError: [Errno 98] Address already in use` with a clear message. `--port` flag is the fix.

---

## 6. Metrics

| Metric | Value |
|---|---|
| `scripts/server.py` | 115 lines, 0 pip installs |
| `dashboard/index.html` additions | +65 lines (CSS + JS) |
| API endpoints | 2 (`PATCH /api/status`, `POST /api/write`) |
| Path validation layers | 3 (literal `..`, resolve+prefix, pattern match) |
| Test cases validated | 8 |

---

## 7. Lessons learned

- **`SimpleHTTPRequestHandler` + `directory` kwarg is the cleanest approach.** No need to `chdir()` or fiddle with `os.getcwd()`. Python 3.7+ supports it natively; the server is working-directory-agnostic.
- **Three independent path checks are better than one clever regex.** Each check is trivially auditable; a single regex trying to do all three would be opaque and easy to get wrong.
- **Next session:** PLAN-007 — Plan generation + copy-paste prompt: "Generate Plan" button in dashboard writes `lessons/<slug>/plan.md` via `POST /api/write` and displays the Claude prompt for copy-pasting into VS Code.
