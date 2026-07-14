#!/usr/bin/env python3
"""Validator for data/roadmap.json (PLAN-024 G3).

The roadmap is the topic dependency DAG rendered behind the Problems tab's
Roadmap view. It stores *edges and layout only* — never problem counts. Counts
are derived from data/problems.json at render time, which is the whole point:
the picture this replaces (a hand-drawn PNG) carried transcribed counts that
did not match the dataset and went stale the moment a problem was added.

Checks, in order:

  1. The file parses and is a non-empty JSON array.
  2. Every node has the required fields, all non-empty.
  3. **No count field exists anywhere.** A `count`/`total`/`n` key would be a
     transcribed number, i.e. the exact bug this rewrite exists to kill.
  4. Every `topic` is a real topic in problems.json, and no topic is repeated.
  5. **Coverage is total**: every topic in problems.json has a node. A topic
     with no node would be unreachable on the map while its problems still sit
     in the table below it.
  6. Every `prereqs` entry names a declared node (no dangling edges).
  7. The graph is acyclic, and `layer` is monotone: a prereq's layer is
     strictly less than its dependent's. This is what makes the render a clean
     top-down DAG with no back-edges, and it subsumes the cycle check — but
     both are asserted, because a future hand-edit could break either.
  8. Layers are contiguous from 0 (no empty rank in the middle).
  9. Exactly one root (a node with no prereqs). A second root would be a topic
     you can start from cold, which is a curriculum claim, not a layout detail.
 10. Report: the layer plan, with derived problem counts alongside.

Exit code 0 on pass, 1 on any violation. Stdlib only.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROADMAP = ROOT / "data" / "roadmap.json"
PROBLEMS = ROOT / "data" / "problems.json"

REQUIRED = ("topic", "layer", "prereqs", "why")
FORBIDDEN = ("count", "total", "n", "num_problems", "problems", "done")
MIN_WHY = 40


def main() -> int:
    fatals: list[str] = []

    if not ROADMAP.exists():
        _summary(["roadmap.json missing"])
        return 1
    try:
        nodes = json.loads(ROADMAP.read_text())
    except json.JSONDecodeError as e:
        _summary([f"roadmap.json is not valid JSON: {e}"])
        return 1
    if not isinstance(nodes, list) or not nodes:
        _summary(["roadmap.json must be a non-empty array"])
        return 1

    problems = json.loads(PROBLEMS.read_text())
    real_topics = {p["topic"] for p in problems}
    counts = Counter(p["topic"] for p in problems)
    done = Counter(p["topic"] for p in problems if p.get("status") == "done")

    declared: set[str] = set()
    layer_of: dict[str, int] = {}

    for i, n in enumerate(nodes):
        tag = f"node[{i}] ({n.get('topic', '?')})"

        for field in REQUIRED:
            if field not in n or n[field] in ("", None) or (field != "prereqs" and n[field] == []):
                fatals.append(f"{tag}: missing/empty required field '{field}'")

        for bad in FORBIDDEN:
            if bad in n:
                fatals.append(
                    f"{tag}: has a '{bad}' field — counts must be DERIVED from "
                    f"problems.json at render time, never stored here")

        topic = n.get("topic")
        if topic in declared:
            fatals.append(f"{tag}: duplicate topic '{topic}'")
        elif topic is not None:
            declared.add(topic)
        if topic is not None and topic not in real_topics:
            fatals.append(f"{tag}: topic '{topic}' is not a topic in data/problems.json")

        layer = n.get("layer")
        if not isinstance(layer, int) or layer < 0:
            fatals.append(f"{tag}: layer must be a non-negative integer")
        elif topic is not None:
            layer_of[topic] = layer

        why = n.get("why")
        if isinstance(why, str) and len(why.strip()) < MIN_WHY:
            fatals.append(f"{tag}: why too short ({len(why.strip())} < {MIN_WHY} chars)")

        if not isinstance(n.get("prereqs"), list):
            fatals.append(f"{tag}: prereqs must be an array")

    # 5. total coverage — an orphaned topic is invisible on the map
    for t in sorted(real_topics - declared):
        fatals.append(f"topic '{t}' has {counts[t]} problems but no roadmap node")

    # 6/7. edges resolve, and layers strictly increase along every edge
    for n in nodes:
        topic = n.get("topic")
        for pre in n.get("prereqs") or []:
            if pre not in declared:
                fatals.append(f"node ({topic}): prereq '{pre}' is not a declared node")
            elif topic in layer_of and pre in layer_of and layer_of[pre] >= layer_of[topic]:
                fatals.append(
                    f"node ({topic}): prereq '{pre}' is at layer {layer_of[pre]}, "
                    f"not strictly above layer {layer_of[topic]} — back-edge")

    # 7. explicit cycle check (Kahn), independent of the layer check
    indeg = {n["topic"]: 0 for n in nodes if "topic" in n}
    adj = defaultdict(list)
    for n in nodes:
        for pre in n.get("prereqs") or []:
            if pre in indeg and n.get("topic") in indeg:
                adj[pre].append(n["topic"])
                indeg[n["topic"]] += 1
    queue = [t for t, d in indeg.items() if d == 0]
    seen = 0
    while queue:
        t = queue.pop()
        seen += 1
        for nxt in adj[t]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    if seen != len(indeg):
        stuck = sorted(t for t, d in indeg.items() if d > 0)
        fatals.append(f"graph has a cycle — unresolvable: {stuck}")

    # 8. contiguous layers
    layers = sorted({n["layer"] for n in nodes if isinstance(n.get("layer"), int)})
    if layers and layers != list(range(len(layers))):
        fatals.append(f"layers must be contiguous from 0, got {layers}")

    # 9. exactly one root
    roots = [n["topic"] for n in nodes if not (n.get("prereqs") or [])]
    if len(roots) != 1:
        fatals.append(f"expected exactly 1 root (no prereqs), found {len(roots)}: {roots}")

    by_layer: dict[int, list[str]] = defaultdict(list)
    for n in nodes:
        if isinstance(n.get("layer"), int):
            by_layer[n["layer"]].append(n["topic"])

    print("check_roadmap — PLAN-024 G3")
    print("─" * 72)
    print(f"  {len(nodes)} nodes · {sum(len(n.get('prereqs') or []) for n in nodes)} edges · "
          f"{len(by_layer)} layers · root: {roots[0] if len(roots) == 1 else '??'}")
    print(f"  covers {len(declared & real_topics)}/{len(real_topics)} topics, "
          f"{sum(counts[t] for t in declared & real_topics)}/{len(problems)} problems")
    print("─" * 72)
    for L in sorted(by_layer):
        for t in sorted(by_layer[L], key=lambda x: -counts[x]):
            print(f"  L{L}  {done[t]:>2}/{counts[t]:<3} {t}")
    print("─" * 72)
    _summary(fatals)
    return 1 if fatals else 0


def _summary(fatals: list[str]) -> None:
    for f in fatals:
        print(f"  ✗ {f}")
    if fatals:
        print(f"  => FAIL ({len(fatals)} violation(s))")
    else:
        print("  => OK")


if __name__ == "__main__":
    sys.exit(main())
