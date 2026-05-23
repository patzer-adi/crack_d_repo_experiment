# PLAN-006: Python File-Writer Service

**Created:** 2026-05-07
**Status:** In-Progress
**Addresses:** Feature 5 in `AGENT_MD/spec.md` — a single local server (`scripts/server.py`) that replaces `python3 -m http.server`, adds write-API endpoints, and enables the dashboard "Mark Done" action.

---

## 1. Context & motivation

The dashboard (PLAN-005) is read-only — the browser cannot write files. Two write operations are needed:
1. **Mark Done / Mark New** — update `data/problems.json` in place.
2. **Write plan.md** — create `lessons/<slug>/plan.md` when the user triggers "Generate Plan" (PLAN-007).

The server replaces `python3 -m http.server` entirely: it serves static files identically (subclasses `SimpleHTTPRequestHandler`) and adds two API routes. The dashboard fetch URLs are unchanged (`../data/problems.json` still resolves correctly). No CORS complexity — everything on one port.

---

## 2. Goals

- **G1:** `scripts/server.py` runs with `python3 scripts/server.py` (default port 8000; `--port N` override).
- **G2:** Static file serving is identical to `python3 -m http.server` — all dashboard and lesson assets load unchanged.
- **G3:** `PATCH /api/status` accepts `{"slug": "...", "status": "done"|"new"}`, updates `data/problems.json` atomically, returns `{"ok": true}`.
- **G4:** `POST /api/write` accepts `{"path": "lessons/<slug>/plan.md", "content": "..."}`, writes the file after path-traversal validation, returns `{"ok": true}`. Restricted to `lessons/*/plan.md` pattern only.
- **G5:** Path traversal rejected — any `path` containing `..` or resolving outside the project root returns `{"ok": false, "error": "..."}` with HTTP 400.
- **G6:** Dashboard "Mark Done / Mark New" toggle button wired to `PATCH /api/status` — status persists to disk and survives browser refresh.
- **G7:** Stdlib only (`http.server`, `json`, `pathlib`, `argparse`, `threading`). Zero pip installs.

---

## 3. Non-goals

- No "Generate Plan" UI (PLAN-007).
- No auth or rate limiting — local single-user tool.
- No HTTPS.
- No general-purpose file write (only `lessons/*/plan.md`).

---

## 4. Approach

### 4.1 Server architecture

```python
class CrackDHandler(SimpleHTTPRequestHandler):
    # directory = PROJECT_ROOT (parent of scripts/)
    # GETs → super().do_GET() (static file serving)
    # PATCH /api/status → update problems.json
    # POST  /api/write  → write lessons/*/plan.md
```

`SimpleHTTPRequestHandler` takes a `directory` kwarg (Python 3.7+); we set it to the project root so `python3 scripts/server.py` works from any working directory.

### 4.2 PATCH /api/status

```
Request:  PATCH /api/status
Body:     {"slug": "3sum", "status": "done"}
Response: {"ok": true}  or  {"ok": false, "error": "..."}
```

Reads `data/problems.json`, finds the matching slug, updates `status`, writes back with `indent=2`. If slug not found → 404.

### 4.3 POST /api/write

```
Request:  POST /api/write
Body:     {"path": "lessons/3sum/plan.md", "content": "# ..."}
Response: {"ok": true}  or  {"ok": false, "error": "..."}
```

Path validation:
1. Reject if `path` contains `..`.
2. Resolve `PROJECT_ROOT / path` and confirm it starts with `PROJECT_ROOT`.
3. Reject if the resolved path does not match `lessons/*/plan.md` (exactly two path segments after `lessons/`).
4. `mkdir -p` the parent dir; write content as UTF-8.

### 4.4 Dashboard changes

- Update error message to reference `python3 scripts/server.py`.
- Replace static status badge with a `<button class="status-toggle">` that calls `toggleStatus(slug, currentStatus)`.
- `toggleStatus` sends `PATCH /api/status`, updates the in-memory `ALL` array, re-renders stats and the single row.
- Brief toast on success/error.

---

## 5. Task breakdown

| # | Task | Est. |
|---|------|------|
| 1 | Write `scripts/server.py` | 25 min |
| 2 | Update `dashboard/index.html`: status toggle button + toast | 20 min |
| 3 | Smoke test: start server, open dashboard, toggle a problem, refresh, confirm persisted | 5 min |
| 4 | Test path-traversal rejection | 3 min |
| 5 | Commit; write REPORT-006; update current_state_report | 10 min |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Port 8000 already in use | Low | Low | `--port` flag; clear error message on bind failure |
| problems.json write race (two browser tabs) | Very low | Low | Single-threaded by default; acceptable for solo tool |
| Path traversal bypass via symlinks | Very low | Low | `Path.resolve()` follows symlinks before prefix check |

---

## 7. Success criteria

- [ ] G1–G7 above verified
- [ ] Toggle "done" → "new" → "done" on a problem; each persists after browser refresh
- [ ] `curl -X POST /api/write` with `path=../../etc/passwd` returns HTTP 400
- [ ] REPORT-006 written; plan status → Completed

## 8. References

- `scripts/import_problems.py` — style reference for stdlib-only Python scripts
- `dashboard/index.html` — consumer of the new API endpoints
- `AGENT_MD/spec.md` Feature 5
