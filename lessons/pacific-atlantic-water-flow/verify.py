#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for pacific-atlantic-water-flow (LC 417).

Independent of the lesson's reverse-flood oracle (drGenSteps floods *uphill*
from each shore once): this is the FORWARD brute force — from every cell, flood
*downhill* and record which oceans the flood touches; keep the cells that touch
both. O((m·n)^2) and structurally opposite to the oracle, so agreement is
meaningful rather than circular.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers (each a sorted list of [r, c]) on stdout, in order.
"""
import sys
import json


def pacific_atlantic(h):
    m, n = len(h), len(h[0])

    def reaches_both(sr, sc):
        seen = {(sr, sc)}
        stack = [(sr, sc)]
        pac = atl = False
        while stack:
            r, c = stack.pop()
            if r == 0 or c == 0:
                pac = True
            if r == m - 1 or c == n - 1:
                atl = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen and h[nr][nc] <= h[r][c]:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return pac and atl

    res = [[r, c] for r in range(m) for c in range(n) if reaches_both(r, c)]
    res.sort()
    return res


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([pacific_atlantic(ex["heights"]) for ex in inputs]))


if __name__ == "__main__":
    main()
