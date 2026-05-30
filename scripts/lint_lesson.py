#!/usr/bin/env python3
"""Lint a lesson against the PLAN-016 acceptance criteria.

Usage:
    python3 scripts/lint_lesson.py <slug> [--section N] [--json]

Exit codes:
    0 — pass (no failures, may have warnings)
    1 — fail (one or more MUST checks violated)

Output:
    Human-readable by default. --json emits a structured report.

Checks performed:
    Schema (always):
        - lessons/<slug>/lesson.html exists
        - lessons/<slug>/plan.md exists
        - lesson.html links static/lesson.css and static/lesson.js
        - lesson.html contains exactly 11 <div class="section"> blocks
        - plan.md has '## Metadata' and 'Archetype:' line
        - plan.md has '## 1. Clarifying' (PLAN-011 schema marker)

    Section 1 (when --section 1 or default):
        See lessons/design/sec1_insight.md "Acceptance criteria"
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"

# Legacy carve-out, retained as an empty set so the surrounding code paths
# (severity = "warn" if slug in LEGACY_GOLDENS else "fail") still resolve.
# All previously-listed lessons were brought up to the PLAN-017 §1 animation
# standard on 2026-05-21; any future drift must be remediated, not allowlisted.
LEGACY_GOLDENS: set[str] = set()


@dataclass
class CheckResult:
    rule: str
    passed: bool
    message: str = ""
    severity: str = "fail"  # "fail" or "warn"


@dataclass
class LintReport:
    slug: str
    results: list[CheckResult] = field(default_factory=list)

    def add(self, rule: str, passed: bool, message: str = "", severity: str = "fail"):
        self.results.append(CheckResult(rule, passed, message, severity))

    @property
    def failures(self) -> list[CheckResult]:
        return [r for r in self.results if not r.passed and r.severity == "fail"]

    @property
    def warnings(self) -> list[CheckResult]:
        return [r for r in self.results if not r.passed and r.severity == "warn"]

    @property
    def passed(self) -> bool:
        return len(self.failures) == 0


def lint_schema(report: LintReport, html: str, plan: str) -> None:
    """File-level schema checks. Failures block."""

    if 'href="../../static/lesson.css"' not in html:
        report.add("schema:lesson.css imported", False,
                   "lesson.html must <link> ../../static/lesson.css")
    else:
        report.add("schema:lesson.css imported", True)

    if 'src="../../static/lesson.js"' not in html:
        report.add("schema:lesson.js imported", False,
                   "lesson.html must <script src> ../../static/lesson.js")
    else:
        report.add("schema:lesson.js imported", True)

    sections = re.findall(r'<div class="section"', html)
    if len(sections) != 11:
        report.add("schema:11 section blocks", False,
                   f"expected 11 <div class=\"section\"> blocks, found {len(sections)}")
    else:
        report.add("schema:11 section blocks", True)

    # PLAN-018 contract: every section marker must use the canonical
    # '<!-- ═══ SECTION N: TITLE ═══ -->' format. No bare 'SECTION N',
    # no '§N', no missing decorations. Catches markers like '<!-- SECTION 1: INSIGHT -->'.
    bad_markers = []
    for m in re.finditer(
        r"<!--\s*[═\s]*(?:SECTION\s+|§)(\d+).*?-->",
        html,
    ):
        line = m.group(0)
        if not re.match(r"<!--\s*═══\s+SECTION\s+\d+:\s+[A-Z][A-Z\s]+\s+═══\s+-->", line):
            bad_markers.append(line.strip())
    if bad_markers:
        report.add("schema:section markers canonical", False,
                   f"{len(bad_markers)} non-canonical marker(s) "
                   f"(want '<!-- ═══ SECTION N: TITLE ═══ -->'): "
                   f"{bad_markers[0]}")
    else:
        report.add("schema:section markers canonical", True)

    if not re.search(r"^## Metadata\b", plan, re.MULTILINE):
        report.add("schema:plan has ## Metadata", False,
                   "plan.md should have '## Metadata' section (PLAN-011 schema)",
                   severity="warn")
    else:
        report.add("schema:plan has ## Metadata", True, severity="warn")

    if not re.search(r"^\*\*Archetype:\*\*|^- \*\*Archetype:\*\*|^Archetype:", plan, re.MULTILINE):
        report.add("schema:plan has Archetype line", False,
                   "plan.md Metadata should include 'Archetype:' line",
                   severity="warn")
    else:
        report.add("schema:plan has Archetype line", True, severity="warn")

    if not re.search(r"^## 1\. Clarifying", plan, re.MULTILINE):
        report.add("schema:plan has §1 Clarifying", False,
                   "plan.md should have '## 1. Clarifying questions' (PLAN-011 schema)",
                   severity="warn")
    else:
        report.add("schema:plan has §1 Clarifying", True, severity="warn")


def extract_section(html: str, section_index: int) -> tuple[str, int, int]:
    """Return (text, start_line, end_line) for §N.

    Sections are identified by '<!-- ═══ SECTION N: ' or
    '<!-- SECTION N: ' comments. We look for the Nth and (N+1)th occurrence.
    """
    lines = html.splitlines()
    marker_re = re.compile(rf"<!--\s*[═\s]*(?:SECTION |§){section_index}:")
    next_marker_re = re.compile(rf"<!--\s*[═\s]*(?:SECTION |§){section_index + 1}:")

    start = end = None
    for i, line in enumerate(lines):
        if marker_re.search(line):
            start = i
            break
    if start is None:
        return "", -1, -1

    for i, line in enumerate(lines[start + 1:], start=start + 1):
        if next_marker_re.search(line):
            end = i
            break
    if end is None:
        end = len(lines)

    return "\n".join(lines[start:end]), start, end


def lint_section1(report: LintReport, html: str, slug: str = "") -> None:
    """§1 Insight checks per sec1_insight.md acceptance criteria."""

    text, start, end = extract_section(html, 1)
    if start < 0:
        report.add("§1:exists", False, "section 1 (THE INSIGHT) comment marker not found")
        return
    report.add("§1:exists", True)

    line_count = end - start
    if line_count < 45:
        report.add("§1:line count ≥ 45", False,
                   f"§1 has {line_count} lines, minimum is 45")
    else:
        report.add("§1:line count ≥ 45", True, f"{line_count} lines")

    sec_label_matches = re.findall(r'<p class="sec-label">The Insight</p>', text)
    if len(sec_label_matches) != 1:
        report.add("§1:sec-label present (exactly one)", False,
                   f"expected exactly one sec-label 'The Insight', found {len(sec_label_matches)}")
    else:
        report.add("§1:sec-label present (exactly one)", True)

    sec_title_matches = re.findall(r'<p class="sec-title">([^<]+)</p>', text)
    if len(sec_title_matches) != 1:
        report.add("§1:sec-title present (exactly one)", False,
                   f"expected exactly one sec-title, found {len(sec_title_matches)}")
    else:
        report.add("§1:sec-title present (exactly one)", True)

        title = sec_title_matches[0].strip()
        if re.match(r"^Use\s+\S+\s+as\s+", title, re.IGNORECASE) or \
           re.match(r"^Traverse\s+", title, re.IGNORECASE):
            report.add("§1:sec-title not algorithm description", False,
                       f"sec-title looks like algorithm description: '{title[:60]}'",
                       severity="warn")
        else:
            report.add("§1:sec-title not algorithm description", True, severity="warn")

    body_paras = re.findall(r'<p class="body"[^>]*>(.*?)</p>', text, re.DOTALL)
    kernel_chars = max((len(re.sub(r"<[^>]+>", "", p).strip()) for p in body_paras),
                        default=0)
    if kernel_chars < 180:
        report.add("§1:kernel paragraph ≥ 180 chars", False,
                   f"longest body paragraph is {kernel_chars} chars; minimum is 180")
    else:
        report.add("§1:kernel paragraph ≥ 180 chars", True,
                   f"{kernel_chars} chars")

        first_word_match = next(
            (p for p in body_paras if len(re.sub(r"<[^>]+>", "", p).strip()) == kernel_chars),
            None,
        )
        if first_word_match:
            first_word = re.sub(r"<[^>]+>", "", first_word_match).strip().split()[:1]
            if first_word and first_word[0].lower() in {"iterate", "loop", "first"}:
                report.add("§1:kernel doesn't start with imperative-step word", False,
                           f"kernel paragraph starts with '{first_word[0]}' — restates algorithm steps",
                           severity="warn")
            else:
                report.add("§1:kernel doesn't start with imperative-step word", True,
                           severity="warn")

    infobox_matches = re.findall(r'<div class="infobox success">', text)
    if len(infobox_matches) != 1:
        report.add("§1:kernel infobox (exactly one)", False,
                   f"expected exactly one <div class=\"infobox success\"> in §1, found {len(infobox_matches)}")
    else:
        report.add("§1:kernel infobox (exactly one)", True)

    has_chain_box = '<div class="chain-box">' in text
    chain_rows = re.findall(r'<div class="chain-row">', text)
    chain_examples = re.findall(r'<div class="chain-example">', text)

    infobox_start = text.find('<div class="infobox success">')
    visual_lines_before_kernel = text[:infobox_start].count("\n") if infobox_start >= 0 else 0

    if has_chain_box and len(chain_rows) >= 3 and len(chain_examples) >= 2:
        report.add("§1:foundational structure", True,
                   f"chain-box with {len(chain_rows)} rows, {len(chain_examples)} examples")
    elif visual_lines_before_kernel >= 30 and kernel_chars <= 350:
        report.add("§1:foundational structure", True,
                   f"visual-led style, {visual_lines_before_kernel} lines before kernel infobox, kernel {kernel_chars} chars")
    else:
        details = []
        if has_chain_box:
            details.append(
                f"chain-box present but only {len(chain_rows)} rows, {len(chain_examples)} examples"
            )
        else:
            details.append("no chain-box")
        if visual_lines_before_kernel < 30:
            details.append(
                f"only {visual_lines_before_kernel} lines before kernel infobox (≥ 30 needed for visual-led style)"
            )
        elif kernel_chars > 350:
            details.append(
                f"visual-led requires kernel ≤ 350 chars, found {kernel_chars} — kernel appears to dump the algorithm rather than describe the concept"
            )
        report.add("§1:foundational structure", False, "; ".join(details))

    # PLAN-018 contract: lesson must use the 3-tier canonical CSS variable palette
    # (info = current, success = best/finalized, warn = pivot/restart). Each tier
    # counts if ANY of its bg/text/border variants is present anywhere in the
    # lesson HTML — covers both inline §1 styling AND classes defined in <style>
    # blocks that §1 references (e.g. .rsp-cell.matched). Catches lessons that
    # invent their own colors (hard-coded hex values).
    color_tiers = {
        "info / current": ("var(--bg-info)", "var(--text-info)", "var(--border-info)"),
        "success / best": ("var(--bg-success)", "var(--text-success)", "var(--border-success)"),
        "warn / pivot": ("var(--bg-warn)", "var(--text-warn)", "var(--border-warn)"),
    }
    missing = [tier for tier, variants in color_tiers.items()
               if not any(v in html for v in variants)]
    if missing:
        report.add("§1:color legend uses canonical palette", False,
                   f"missing tier(s): {', '.join(missing)}. "
                   f"Each of info/success/warn must appear as bg-, text-, or border- "
                   f"variant somewhere in the lesson (the 3-layer current/best/pivot convention).",
                   severity="warn")
    else:
        report.add("§1:color legend uses canonical palette", True, severity="warn")

    # PLAN-017: §1 must have animation controls (prev/next/auto/reset)
    # calling siNext/siPrev/siTogglePlay/siReset.
    # LEGACY_GOLDENS allowlist is empty as of 2026-05-21; any drift now fails.
    control_refs = set(re.findall(r"si(?:Next|Prev|TogglePlay|Reset)\(\)", text))
    severity = "warn" if slug in LEGACY_GOLDENS else "fail"
    if len(control_refs) >= 3:
        report.add("§1:animation controls present", True,
                   f"found {', '.join(sorted(control_refs))}")
    else:
        msg = (f"§1 needs prev/next/auto/reset buttons calling siPrev/siNext/"
               f"siTogglePlay/siReset; found {len(control_refs)} of 4 "
               f"({', '.join(sorted(control_refs)) or 'none'})")
        if slug in LEGACY_GOLDENS:
            msg = f"[legacy golden — backfill in future plan] {msg}"
        report.add("§1:animation controls present", False, msg, severity=severity)

    # §1 must define siGenSteps (the step generator); look anywhere in the lesson, not just §1
    if "function siGenSteps" in html or "siGenSteps =" in html or "siGenSteps=" in html:
        report.add("§1:step generator defined", True)
    else:
        sev = "warn" if slug in LEGACY_GOLDENS else "fail"
        msg = "no 'siGenSteps' function found in the lesson"
        if slug in LEGACY_GOLDENS:
            msg = f"[legacy golden — backfill in future plan] {msg}"
        report.add("§1:step generator defined", False, msg, severity=sev)


def lint_section6(report: LintReport, html: str, slug: str = "") -> None:
    """§6 Code Visualization canonical-scaffold checks per sec6_code_viz.md.

    Enforces the chassis (markup ids, function names, buttons, no hex colors)
    so CV sections cannot drift across lessons. Algorithm-specific content
    (which variables to show, what visual lives below cv-split) is free.
    """
    text, start, end = extract_section(html, 6)
    if start < 0:
        report.add("§6:exists", False,
                   "section 6 (CODE VISUALIZATION) comment marker not found")
        return
    report.add("§6:exists", True)

    # Required canonical element ids inside §6
    required_ids = [
        "cv-code-panel", "cv-var-grid", "cv-narration",
        "cv-ex0", "cv-ex1", "cv-ex2",
        "cv-bprev", "cv-bplay", "cv-bnext", "cv-sctr",
    ]
    missing_ids = [i for i in required_ids if f'id="{i}"' not in text]
    if missing_ids:
        report.add("§6:canonical element ids", False,
                   f"missing required ids in §6: {', '.join(missing_ids)}. "
                   f"See sec6_code_viz.md for the canonical chassis.")
    else:
        report.add("§6:canonical element ids", True)

    # Canonical button onclick handlers
    required_handlers = [
        ("cvLoadEx(0)", "Ex 1 button must onclick=\"cvLoadEx(0)\""),
        ("cvLoadEx(1)", "Ex 2 button must onclick=\"cvLoadEx(1)\""),
        ("cvLoadEx(2)", "Ex 3 button must onclick=\"cvLoadEx(2)\""),
        ("cvPrev()",       "Prev button must call cvPrev()"),
        ("cvTogglePlay()", "Auto/Play button must call cvTogglePlay()"),
        ("cvNext()",       "Next button must call cvNext() (NOT cvNextStep)"),
        ("cvReset()",      "Reset button must call cvReset()"),
    ]
    bad_handlers = [m for h, m in required_handlers if h not in text]
    if bad_handlers:
        report.add("§6:canonical button handlers", False,
                   "; ".join(bad_handlers))
    else:
        report.add("§6:canonical button handlers", True)

    # Required top-level cv functions defined SOMEWHERE in the lesson HTML
    required_fns = ["cvNext", "cvPrev", "cvReset", "cvLoadEx", "cvGenSteps", "cvRender"]
    missing_fns = []
    for fn in required_fns:
        if not re.search(rf"function\s+{fn}\b|\b{fn}\s*=\s*function|\b{fn}\s*=\s*\(", html):
            missing_fns.append(fn)
    if missing_fns:
        report.add("§6:canonical cv functions", False,
                   f"missing function definitions: {', '.join(missing_fns)}. "
                   f"static/lesson.js' keyboard + play loop need these exact names.")
    else:
        report.add("§6:canonical cv functions", True)

    # Anti-patterns (drift markers we've actually seen)
    anti_patterns = []
    if "cvNextStep" in html:
        anti_patterns.append("cvNextStep (must be cvNext)")
    if re.search(r"function\s+cvTogglePlay\b", html):
        anti_patterns.append("local cvTogglePlay redefinition (use static/lesson.js's)")
    if re.search(r'■\s*Stop|>\s*Stop\s*<', text):
        anti_patterns.append("'■ Stop' button (no Stop in canonical; Reset replaces it)")
    if 'id="cv-step-num"' in text or 'id="cv-step-max"' in text:
        anti_patterns.append("legacy cv-step-num/cv-step-max ids (use single cv-sctr span)")
    # Hex colors inside §6 markup — drift signal
    hex_inside_cv = re.findall(r"#[0-9a-fA-F]{3,6}\b", text)
    # Filter false positives like fragment ids inside href; for §6 inline styles
    # any hex is suspect — canonical uses var(--*) tokens
    hex_inside_cv = [h for h in hex_inside_cv if not h.startswith("#cv")]  # ignore id refs
    if hex_inside_cv:
        anti_patterns.append(
            f"hard-coded hex color(s) in §6 markup: {', '.join(sorted(set(hex_inside_cv))[:4])}"
            " — use var(--bg-info)/(--bg-success)/(--bg-warn)/(--bg-danger) instead"
        )
    if anti_patterns:
        report.add("§6:no drift anti-patterns", False, "; ".join(anti_patterns))
    else:
        report.add("§6:no drift anti-patterns", True)

    # Variable-card grid: at least 3 cards with the canonical structure
    card_count = len(re.findall(r'<div\s+class="cv-var-card[^"]*"\s+id="cv-v-', text))
    if card_count < 3:
        report.add("§6:variable cards", False,
                   f"§6 has {card_count} cv-var-card elements with id=\"cv-v-*\"; "
                   f"need ≥ 3 (use canonical .cv-var-card markup, not inline-styled divs)")
    else:
        report.add("§6:variable cards", True, f"{card_count} cards")


def lint_section7(report: LintReport, html: str, slug: str = "") -> None:
    """§7 Dry Run canonical-scaffold checks.

    Same chassis as §6 but with the dr- prefix and slightly different counter
    placement. The static/lesson.js drTogglePlay function looks for #dr-bplay,
    so that id is mandatory.
    """
    text, start, end = extract_section(html, 7)
    if start < 0:
        report.add("§7:exists", False, "section 7 (DRY RUN) comment marker not found")
        return
    report.add("§7:exists", True)

    required_ids = ["dr-ex0", "dr-ex1", "dr-ex2", "dr-bplay", "dr-sctr"]
    missing_ids = [i for i in required_ids if f'id="{i}"' not in text]
    if missing_ids:
        report.add("§7:canonical element ids", False,
                   f"missing required ids in §7: {', '.join(missing_ids)}.")
    else:
        report.add("§7:canonical element ids", True)

    required_handlers = [
        ("drLoadEx(0)", "Ex 1 must onclick=\"drLoadEx(0)\""),
        ("drLoadEx(1)", "Ex 2 must onclick=\"drLoadEx(1)\""),
        ("drLoadEx(2)", "Ex 3 must onclick=\"drLoadEx(2)\""),
        ("drPrev()",       "Prev button must call drPrev()"),
        ("drTogglePlay()", "Auto/Play button must call drTogglePlay()"),
        ("drNext()",       "Next button must call drNext() (NOT drNextStep)"),
        ("drReset()",      "Reset button must call drReset()"),
    ]
    bad_handlers = [m for h, m in required_handlers if h not in text]
    if bad_handlers:
        report.add("§7:canonical button handlers", False, "; ".join(bad_handlers))
    else:
        report.add("§7:canonical button handlers", True)

    required_fns = ["drNext", "drPrev", "drReset", "drLoadEx", "drGenSteps", "drRender"]
    missing_fns = [fn for fn in required_fns
                   if not re.search(rf"function\s+{fn}\b|\b{fn}\s*=\s*function|\b{fn}\s*=\s*\(", html)]
    if missing_fns:
        report.add("§7:canonical dr functions", False,
                   f"missing function definitions: {', '.join(missing_fns)}.")
    else:
        report.add("§7:canonical dr functions", True)

    anti_patterns = []
    if "drNextStep" in html:
        anti_patterns.append("drNextStep (must be drNext)")
    if re.search(r"function\s+drTogglePlay\b", html):
        anti_patterns.append("local drTogglePlay redefinition (use static/lesson.js's)")
    if re.search(r'■\s*Stop|>\s*Stop\s*<', text):
        anti_patterns.append("'■ Stop' button (no Stop in canonical; Reset replaces it)")
    if 'id="dr-step-num"' in text or 'id="dr-step-max"' in text:
        anti_patterns.append("legacy dr-step-num/dr-step-max ids (use single dr-sctr span)")
    if 'id="dr-play"' in text and 'id="dr-bplay"' not in text:
        anti_patterns.append("Auto button id is 'dr-play'; static/lesson.js expects 'dr-bplay'")
    if anti_patterns:
        report.add("§7:no drift anti-patterns", False, "; ".join(anti_patterns))
    else:
        report.add("§7:no drift anti-patterns", True)


def lint_section2(report: LintReport, html: str, slug: str = "") -> None:
    """§2 Brute Force canonical-scaffold checks.

    Same chassis but with bf- prefix. static/lesson.js bfTogglePlay looks for
    #bf-play (note: NOT 'bf-bplay' — the bf prefix is the exception).
    """
    text, start, end = extract_section(html, 2)
    if start < 0:
        report.add("§2:exists", False, "section 2 (BRUTE FORCE) comment marker not found")
        return
    report.add("§2:exists", True)

    required_ids = ["bf-ex0", "bf-ex1", "bf-ex2", "bf-play", "bf-sctr"]
    missing_ids = [i for i in required_ids if f'id="{i}"' not in text]
    if missing_ids:
        report.add("§2:canonical element ids", False,
                   f"missing required ids in §2: {', '.join(missing_ids)}.")
    else:
        report.add("§2:canonical element ids", True)

    required_handlers = [
        ("bfLoadEx(0)", "Ex 1 must onclick=\"bfLoadEx(0)\""),
        ("bfLoadEx(1)", "Ex 2 must onclick=\"bfLoadEx(1)\""),
        ("bfLoadEx(2)", "Ex 3 must onclick=\"bfLoadEx(2)\""),
        ("bfPrev()",       "Prev button must call bfPrev()"),
        ("bfTogglePlay()", "Auto/Play button must call bfTogglePlay()"),
        ("bfNext()",       "Next button must call bfNext()"),
        ("bfReset()",      "Reset button must call bfReset()"),
    ]
    bad_handlers = [m for h, m in required_handlers if h not in text]
    if bad_handlers:
        report.add("§2:canonical button handlers", False, "; ".join(bad_handlers))
    else:
        report.add("§2:canonical button handlers", True)

    required_fns = ["bfNext", "bfPrev", "bfReset", "bfLoadEx", "bfGenSteps", "bfRender"]
    missing_fns = [fn for fn in required_fns
                   if not re.search(rf"function\s+{fn}\b|\b{fn}\s*=\s*function|\b{fn}\s*=\s*\(", html)]
    if missing_fns:
        report.add("§2:canonical bf functions", False,
                   f"missing function definitions: {', '.join(missing_fns)}.")
    else:
        report.add("§2:canonical bf functions", True)

    anti_patterns = []
    if re.search(r"function\s+bfTogglePlay\b", html):
        anti_patterns.append("local bfTogglePlay redefinition (use static/lesson.js's)")
    if re.search(r'■\s*Stop|>\s*Stop\s*<', text):
        anti_patterns.append("'■ Stop' button (no Stop in canonical)")
    if anti_patterns:
        report.add("§2:no drift anti-patterns", False, "; ".join(anti_patterns))
    else:
        report.add("§2:no drift anti-patterns", True)


def lint_animation(report: LintReport, slug: str) -> None:
    """Correctness gate: run the animation step-generators headlessly and check
    the computed answer against each example's declared answer.

    Delegates to scripts/verify_animation.mjs (Node). The dry-run generator
    (drGenSteps) is the oracle; see lessons/design/sec7_dry_run.md "Correctness
    contract". A lesson that cannot be verified (no oracle, impure generator,
    missing answers, or a wrong answer) FAILS — it must not reach
    lesson_status=generated.
    """
    node = shutil.which("node")
    if node is None:
        report.add("§animation:correct", False,
                   "node not found on PATH — cannot run verify_animation.mjs; "
                   "install Node to enforce the animation-correctness gate",
                   severity="warn")
        return
    if not VERIFY_SCRIPT.exists():
        report.add("§animation:correct", False,
                   f"{VERIFY_SCRIPT} missing", severity="warn")
        return

    try:
        proc = subprocess.run(
            [node, str(VERIFY_SCRIPT), slug, "--json"],
            capture_output=True, text=True, timeout=30,
        )
        data = json.loads(proc.stdout or "{}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
        report.add("§animation:correct", False,
                   f"verify_animation.mjs failed to run: {e}")
        return

    cases = data.get("cases", [])
    errors = data.get("errors", [])
    matched = [c for c in cases if c.get("ok") is True]
    wrong = [c for c in cases if c.get("ok") is False and "computed" in c]
    unverifiable = [c for c in cases if "computed" not in c and c.get("ok") is False]

    if wrong:
        c = wrong[0]
        report.add("§animation:correct", False,
                   f"{c['gen']} on {c['example']} computed {c.get('computed')!r} "
                   f"≠ expected {c.get('expected')!r}"
                   + (f" (+{len(wrong) - 1} more)" if len(wrong) > 1 else ""))
    elif not matched:
        detail = errors[0] if errors else (
            unverifiable[0].get("reason", "no oracle") if unverifiable else "nothing verifiable")
        report.add("§animation:correct", False,
                   f"no checkable oracle — {detail}. See sec7_dry_run.md "
                   f"'Correctness contract' (needs EX[].answer + terminal result:)")
    else:
        report.add("§animation:correct", True,
                   f"{len(matched)} example(s) verified")


def lint_animation(report: LintReport, slug: str) -> None:
    """Correctness gate: run the animation step-generators headlessly and check
    the computed answer against each example's declared answer.

    Delegates to scripts/verify_animation.mjs (Node). The dry-run generator
    (drGenSteps) is the oracle; see lessons/design/sec7_dry_run.md "Correctness
    contract". A lesson that cannot be verified (no oracle, impure generator,
    missing answers, or a wrong answer) FAILS — it must not reach
    lesson_status=generated.
    """
    node = shutil.which("node")
    if node is None:
        report.add("§animation:correct", False,
                   "node not found on PATH — cannot run verify_animation.mjs; "
                   "install Node to enforce the animation-correctness gate",
                   severity="warn")
        return
    if not VERIFY_SCRIPT.exists():
        report.add("§animation:correct", False,
                   f"{VERIFY_SCRIPT} missing", severity="warn")
        return

    try:
        proc = subprocess.run(
            [node, str(VERIFY_SCRIPT), slug, "--json"],
            capture_output=True, text=True, timeout=30,
        )
        data = json.loads(proc.stdout or "{}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
        report.add("§animation:correct", False,
                   f"verify_animation.mjs failed to run: {e}")
        return

    cases = data.get("cases", [])
    errors = data.get("errors", [])
    matched = [c for c in cases if c.get("ok") is True]
    wrong = [c for c in cases if c.get("ok") is False and "computed" in c]
    unverifiable = [c for c in cases if "computed" not in c and c.get("ok") is False]

    if wrong:
        c = wrong[0]
        report.add("§animation:correct", False,
                   f"{c['gen']} on {c['example']} computed {c.get('computed')!r} "
                   f"≠ expected {c.get('expected')!r}"
                   + (f" (+{len(wrong) - 1} more)" if len(wrong) > 1 else ""))
    elif not matched:
        detail = errors[0] if errors else (
            unverifiable[0].get("reason", "no oracle") if unverifiable else "nothing verifiable")
        report.add("§animation:correct", False,
                   f"no checkable oracle — {detail}. See sec7_dry_run.md "
                   f"'Correctness contract' (needs EX[].answer + terminal result:)")
    else:
        report.add("§animation:correct", True,
                   f"{len(matched)} example(s) verified")


def lint_lesson(slug: str, sections: list[int] | None) -> LintReport:
    report = LintReport(slug=slug)
    lesson_dir = LESSONS / slug
    html_path = lesson_dir / "lesson.html"
    plan_path = lesson_dir / "plan.md"

    if not html_path.exists():
        report.add("file:lesson.html exists", False, f"{html_path} not found")
        return report
    report.add("file:lesson.html exists", True)

    if not plan_path.exists():
        report.add("file:plan.md exists", False, f"{plan_path} not found")
    else:
        report.add("file:plan.md exists", True)

    html = html_path.read_text()
    plan = plan_path.read_text() if plan_path.exists() else ""

    lint_schema(report, html, plan)

    do_sections = sections or [1, 2, 6, 7]
    if 1 in do_sections:
        lint_section1(report, html, slug)
    if 2 in do_sections:
        lint_section2(report, html, slug)
    if 6 in do_sections:
        lint_section6(report, html, slug)
    if 7 in do_sections:
        lint_section7(report, html, slug)

    # Animation-correctness gate runs whenever §7 (the oracle) is in scope, or
    # on a full run. The dry-run generator is verified headlessly against the
    # declared example answers.
    if 7 in do_sections:
        lint_animation(report, slug)

    return report


def render_text(report: LintReport) -> str:
    lines = [f"lint {report.slug}:"]
    for r in report.results:
        if r.passed:
            mark = "  ✓"
        elif r.severity == "warn":
            mark = "  ⚠"
        else:
            mark = "  ✗"
        suffix = f"  — {r.message}" if r.message else ""
        lines.append(f"{mark} {r.rule}{suffix}")
    lines.append("")
    failed = len(report.failures)
    warned = len(report.warnings)
    passed = len([r for r in report.results if r.passed])
    lines.append(f"  totals: {passed} pass, {warned} warn, {failed} fail")
    return "\n".join(lines)


def render_json(report: LintReport) -> str:
    return json.dumps(
        {
            "slug": report.slug,
            "passed": report.passed,
            "results": [
                {
                    "rule": r.rule,
                    "passed": r.passed,
                    "message": r.message,
                    "severity": r.severity,
                }
                for r in report.results
            ],
        },
        indent=2,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint a lesson against PLAN-016 criteria")
    ap.add_argument("slug", help="lesson slug, e.g. 3sum")
    ap.add_argument("--section", type=int, action="append",
                    help="lint only the named section(s); default = §1")
    ap.add_argument("--json", action="store_true", help="emit JSON output")
    args = ap.parse_args()

    report = lint_lesson(args.slug, args.section)
    print(render_json(report) if args.json else render_text(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
