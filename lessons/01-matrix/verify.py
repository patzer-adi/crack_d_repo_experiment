#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for 01-matrix (LC 542).

Independent of the lesson's multi-source BFS oracle (drGenSteps): this is the
classic TWO-PASS dynamic-programming formulation — no queue, no waves. Sweep
top-left -> bottom-right taking min(self, up+1, left+1), then bottom-right ->
top-left taking min(self, down+1, right+1). The two diagonally-opposite passes
together cover every shortest path to a 0. A different algorithm reaching the
same distance matrix, so the verifier's cross-check is not a tautology.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers (one distance matrix per example) on stdout, in order.
"""
import sys
import json


def update_matrix(mat):
    m, n = len(mat), len(mat[0])
    BIG = float("inf")
    d = [[0 if mat[r][c] == 0 else BIG for c in range(n)] for r in range(m)]
    for r in range(m):
        for c in range(n):
            if d[r][c] == 0:
                continue
            if r > 0:
                d[r][c] = min(d[r][c], d[r - 1][c] + 1)
            if c > 0:
                d[r][c] = min(d[r][c], d[r][c - 1] + 1)
    for r in range(m - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            if d[r][c] == 0:
                continue
            if r + 1 < m:
                d[r][c] = min(d[r][c], d[r + 1][c] + 1)
            if c + 1 < n:
                d[r][c] = min(d[r][c], d[r][c + 1] + 1)
    return d


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([update_matrix(ex["mat"]) for ex in inputs]))


if __name__ == "__main__":
    main()
