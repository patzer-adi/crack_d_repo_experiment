#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for as-far-from-land-as-possible (LC 1162).

Independent of the lesson's multi-source BFS oracle (drGenSteps): this is the
classic TWO-PASS dynamic-programming distance transform — no queue, no waves.
Treat land as distance 0; sweep top-left -> bottom-right taking min(self, up+1,
left+1), then bottom-right -> top-left taking min(self, down+1, right+1). The
two diagonally-opposite passes together compute every water cell's Manhattan
distance to the nearest land; the answer is the maximum such distance, or -1 if
the grid is all land or all water. A different algorithm reaching the same
number, so the verifier's cross-check is not a tautology.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers (one integer per example) on stdout, in order.
"""
import sys
import json


def max_distance(grid):
    n = len(grid)
    cells = [(r, c) for r in range(n) for c in range(len(grid[r]))]
    land = sum(1 for r, c in cells if grid[r][c] == 1)
    if land == 0 or land == len(cells):
        return -1
    BIG = float("inf")
    d = [[0 if grid[r][c] == 1 else BIG for c in range(len(grid[r]))] for r in range(n)]
    for r in range(n):
        for c in range(len(grid[r])):
            if d[r][c] == 0:
                continue
            if r > 0:
                d[r][c] = min(d[r][c], d[r - 1][c] + 1)
            if c > 0:
                d[r][c] = min(d[r][c], d[r][c - 1] + 1)
    for r in range(n - 1, -1, -1):
        for c in range(len(grid[r]) - 1, -1, -1):
            if d[r][c] == 0:
                continue
            if r + 1 < n:
                d[r][c] = min(d[r][c], d[r + 1][c] + 1)
            if c + 1 < len(grid[r]):
                d[r][c] = min(d[r][c], d[r][c + 1] + 1)
    return max(d[r][c] for r, c in cells)


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([max_distance(ex["grid"]) for ex in inputs]))


if __name__ == "__main__":
    main()
