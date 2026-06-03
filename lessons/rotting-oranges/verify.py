#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for rotting-oranges (LC 994).

Independent of the lesson's layer-by-layer oracle (drGenSteps): this is a
textbook *timestamped* BFS — every cell carries the minute it rots, and the
answer is the max timestamp (or -1 if any fresh orange survives). A different
formulation reaching the same answer, so the verifier's cross-check is not a
tautology.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json
from collections import deque


def oranges_rotting(grid):
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                q.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    g = [row[:] for row in grid]
    minutes = 0
    while q:
        r, c, t = q.popleft()
        minutes = max(minutes, t)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and g[nr][nc] == 1:
                g[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return -1 if fresh > 0 else minutes


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([oranges_rotting(ex["grid"]) for ex in inputs]))


if __name__ == "__main__":
    main()
