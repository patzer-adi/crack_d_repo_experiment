#!/usr/bin/env python3
"""
crack_d local server — replaces `python3 -m http.server`.
Serves static files from the project root and adds two write-API endpoints.

Usage:
    python3 scripts/server.py [--port N]   (default: 8000)
"""
import argparse
import json
import re
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_JSON = PROJECT_ROOT / "data" / "problems.json"
STATUS_DATASETS = {
    "problems": PROBLEMS_JSON,
    "basics": PROJECT_ROOT / "data" / "basics.json",
    "warmup": PROJECT_ROOT / "data" / "warmup.json",
    "dpladder": PROJECT_ROOT / "data" / "dp_ladder.json",
}

_lock = threading.Lock()


class CrackDHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    # ── routing ───────────────────────────────────────────────────────────────

    def do_PATCH(self):
        if self.path == "/api/status":
            self._handle_status()
        else:
            self._send_json({"ok": False, "error": "Not found"}, 404)

    def do_POST(self):
        if self.path == "/api/write":
            self._handle_write()
        elif self.path == "/api/add":
            self._handle_add()
        else:
            self._send_json({"ok": False, "error": "Not found"}, 404)

    # ── PATCH /api/status ─────────────────────────────────────────────────────

    def _handle_status(self):
        body = self._read_body()
        if body is None:
            return
        slug          = body.get("slug", "").strip()
        status        = body.get("status", "").strip()
        lesson_status = body.get("lesson_status", "").strip()
        dataset       = body.get("dataset", "problems").strip() or "problems"
        if dataset not in STATUS_DATASETS:
            return self._send_json(
                {"ok": False, "error": f"dataset must be one of {sorted(STATUS_DATASETS)}"}, 400
            )
        if lesson_status and dataset != "problems":
            return self._send_json(
                {"ok": False, "error": "lesson_status only applies to the problems dataset"}, 400
            )
        if not slug:
            return self._send_json({"ok": False, "error": "slug required"}, 400)
        if not status and not lesson_status:
            return self._send_json(
                {"ok": False, "error": "status or lesson_status required"}, 400
            )
        if status and status not in ("done", "new"):
            return self._send_json(
                {"ok": False, "error": "status must be 'done' or 'new'"}, 400
            )
        if lesson_status and lesson_status not in ("none", "generated"):
            return self._send_json(
                {"ok": False, "error": "lesson_status must be 'none' or 'generated'"}, 400
            )

        json_path = STATUS_DATASETS[dataset]
        with _lock:
            try:
                problems = json.loads(json_path.read_text(encoding="utf-8"))
            except Exception as e:
                return self._send_json({"ok": False, "error": f"read error: {e}"}, 500)

            idx = next((i for i, p in enumerate(problems) if p.get("slug") == slug), None)
            if idx is None:
                return self._send_json({"ok": False, "error": f"slug not found: {slug}"}, 404)

            if status:
                problems[idx]["status"] = status
            if lesson_status:
                problems[idx]["lesson_status"] = lesson_status
            try:
                json_path.write_text(
                    json.dumps(problems, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8"
                )
            except Exception as e:
                return self._send_json({"ok": False, "error": f"write error: {e}"}, 500)

        self._send_json({"ok": True})

    # ── POST /api/write ───────────────────────────────────────────────────────

    def _handle_write(self):
        body = self._read_body()
        if body is None:
            return
        rel_path = body.get("path", "").strip()
        content  = body.get("content", "")

        if not rel_path:
            return self._send_json({"ok": False, "error": "path required"}, 400)
        if ".." in rel_path:
            return self._send_json({"ok": False, "error": "path traversal rejected"}, 400)

        resolved = (PROJECT_ROOT / rel_path).resolve()

        # Must stay inside project root
        try:
            resolved.relative_to(PROJECT_ROOT)
        except ValueError:
            return self._send_json({"ok": False, "error": "path outside project root"}, 400)

        # Restrict to lessons/*/plan.md only
        parts = resolved.relative_to(PROJECT_ROOT).parts
        if not (len(parts) == 3 and parts[0] == "lessons" and parts[2] == "plan.md"):
            return self._send_json(
                {"ok": False, "error": "only lessons/<slug>/plan.md writes are allowed"}, 400
            )

        try:
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_text(content, encoding="utf-8")
        except Exception as e:
            return self._send_json({"ok": False, "error": f"write error: {e}"}, 500)

        self._send_json({"ok": True})

    # ── POST /api/add ─────────────────────────────────────────────────────────

    def _handle_add(self):
        body = self._read_body()
        if body is None:
            return
        slug       = body.get("slug", "").strip()
        number     = body.get("number")
        name       = body.get("name", "").strip()
        topic      = body.get("topic", "").strip()
        difficulty = body.get("difficulty", "").strip()

        if not re.fullmatch(r'[a-z0-9-]+', slug):
            return self._send_json({"ok": False, "error": "Invalid slug — use lowercase letters, digits, hyphens only"}, 400)
        if difficulty not in ("Easy", "Medium", "Hard"):
            return self._send_json({"ok": False, "error": "difficulty must be Easy, Medium, or Hard"}, 400)
        if not isinstance(number, int) or number <= 0:
            return self._send_json({"ok": False, "error": "number must be a positive integer"}, 400)
        if not name:
            return self._send_json({"ok": False, "error": "name required"}, 400)
        if not topic:
            return self._send_json({"ok": False, "error": "topic required"}, 400)

        with _lock:
            try:
                problems = json.loads(PROBLEMS_JSON.read_text(encoding="utf-8"))
            except Exception as e:
                return self._send_json({"ok": False, "error": f"read error: {e}"}, 500)

            if any(p.get("slug") == slug for p in problems):
                return self._send_json({"ok": False, "error": f"Duplicate slug: {slug}"}, 409)

            new_order = max((p.get("order", 0) for p in problems), default=0) + 1
            new_problem = {
                "order": new_order,
                "lc_num": number,
                "name": name,
                "url": f"https://leetcode.com/problems/{slug}/",
                "slug": slug,
                "topic": topic,
                "difficulty": difficulty,
                "section": "Ad-hoc",
                "tier": 2,
                "ramp_pos": 999,
                "twist": "",
                "tracks": [],
                "status": "new",
                "lesson_status": "none",
            }
            problems.append(new_problem)
            try:
                PROBLEMS_JSON.write_text(
                    json.dumps(problems, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8"
                )
            except Exception as e:
                return self._send_json({"ok": False, "error": f"write error: {e}"}, 500)

        self._send_json({"ok": True, "problem": new_problem})

    # ── helpers ───────────────────────────────────────────────────────────────

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw)
        except Exception as e:
            self._send_json({"ok": False, "error": f"bad request body: {e}"}, 400)
            return None

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Suppress static-file noise; show API calls only
        if self.path.startswith("/api/"):
            super().log_message(fmt, *args)


def main():
    parser = argparse.ArgumentParser(description="crack_d local server")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    server = HTTPServer(("", args.port), CrackDHandler)
    print(f"crack_d server → http://localhost:{args.port}/dashboard/")
    print(f"Serving from: {PROJECT_ROOT}")
    print("Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
