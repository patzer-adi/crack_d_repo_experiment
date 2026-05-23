"""
import_problems.py — parse problems/finalrepList.HTML → data/problems.json

Run from project root:
    python3 scripts/import_problems.py

Exits 1 if the parsed count is not 150.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from html import unescape

HTML_PATH = "problems/finalrepList.HTML"
JSON_PATH = "data/problems.json"
LESSONS_DIR = "lessons"
EXPECTED_COUNT = 150


class ProblemParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.problems = []

        # Table-level state
        self._in_problem_table = False  # inside a plain <table> (not class="dtable")
        self._in_problem_tbody = False  # inside <tbody> of a problem table

        # Row-level state
        self._in_sec = False       # inside <tr class="sec"> section banner
        self._in_row = False       # inside a problem <tr>
        self._row_is_done = False  # True if <tr class="done-row">
        self._col = -1             # 0-based column counter within current row
        self._collect = False      # True when we want to capture text
        self._buf = ""             # text accumulation buffer
        self._cur = {}             # fields being built for current problem
        self._cur_href = ""        # href from <a> in col 2
        self._section = ""         # most-recently-seen section banner text

    # ── tag open ──────────────────────────────────────────────────────────────

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = attrs.get("class", "")

        if tag == "table":
            # Problem tables have no class; schedule tables use class="dtable"
            self._in_problem_table = (cls == "")
            return

        if tag == "tbody":
            if self._in_problem_table:
                self._in_problem_tbody = True
            return

        if not self._in_problem_tbody:
            return

        if tag == "tr":
            if cls == "sec":
                self._in_sec = True
                self._collect = True
                self._buf = ""
            elif cls in ("done-row", ""):
                self._in_row = True
                self._row_is_done = (cls == "done-row")
                self._col = -1
                self._cur = {}
                self._cur_href = ""

        elif tag == "td" and self._in_row:
            self._col += 1
            self._collect = True
            self._buf = ""

        elif tag == "a" and self._in_row and self._col == 2:
            self._cur_href = attrs.get("href", "")

        elif tag == "span" and self._in_row and self._col in (4, 5):
            self._collect = True
            self._buf = ""

    # ── tag close ─────────────────────────────────────────────────────────────

    def handle_endtag(self, tag):
        if tag == "table":
            self._in_problem_table = False
            return

        if tag == "tbody":
            self._in_problem_tbody = False
            return

        if not self._in_problem_tbody:
            return

        if tag == "tr":
            if self._in_sec:
                self._section = unescape(self._buf.strip())
                self._in_sec = False
                self._collect = False
            elif self._in_row:
                self._in_row = False
                self._collect = False
                if self._cur.get("order") is not None:
                    self.problems.append(self._cur)

        elif tag == "td" and self._in_row:
            text = unescape(self._buf.strip())
            col = self._col

            if col == 0:
                if text.isdigit():
                    self._cur["order"] = int(text)
                else:
                    self._in_row = False  # skip non-problem rows (e.g. thead)
            elif col == 1:
                if text.isdigit():
                    self._cur["lc_num"] = int(text)
            elif col == 2:
                self._cur["name"] = text
                self._cur["url"] = self._cur_href
                m = re.search(r"/problems/([^/]+)/", self._cur_href)
                self._cur["slug"] = m.group(1) if m else ""
            elif col == 3:
                self._cur["topic"] = text
            # cols 4 and 5 captured in </span> handler
            self._collect = False

        elif tag == "span" and self._in_row:
            text = unescape(self._buf.strip())
            if self._col == 4:
                self._cur["difficulty"] = text
            elif self._col == 5:
                self._cur["status"] = "done" if self._row_is_done else "new"
                self._cur["section"] = self._section
            self._collect = False

    # ── text ──────────────────────────────────────────────────────────────────

    def handle_data(self, data):
        if self._collect:
            self._buf += data


def annotate_lesson_status(problems):
    """Set lesson_status='generated' for slugs with an existing lessons/ dir."""
    existing = set()
    if os.path.isdir(LESSONS_DIR):
        for name in os.listdir(LESSONS_DIR):
            if os.path.isdir(os.path.join(LESSONS_DIR, name)):
                existing.add(name)
    for p in problems:
        p["lesson_status"] = "generated" if p.get("slug") in existing else "none"


def main():
    with open(HTML_PATH, encoding="utf-8") as f:
        html = f.read()

    parser = ProblemParser()
    parser.feed(html)
    problems = parser.problems

    annotate_lesson_status(problems)

    total = len(problems)
    done_count = sum(1 for p in problems if p["status"] == "done")
    new_count  = sum(1 for p in problems if p["status"] == "new")
    gen_count  = sum(1 for p in problems if p["lesson_status"] == "generated")
    gen_slugs  = [p["slug"] for p in problems if p["lesson_status"] == "generated"]

    print(f"Parsed {total} problems.")
    print(f"  done:      {done_count}")
    print(f"  new:       {new_count}")
    print(f"  generated: {gen_count}  ({', '.join(gen_slugs)})")
    print(f"Output: {JSON_PATH}")

    if total != EXPECTED_COUNT:
        print(f"ERROR: expected {EXPECTED_COUNT} problems, got {total}.", file=sys.stderr)
        sys.exit(1)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
