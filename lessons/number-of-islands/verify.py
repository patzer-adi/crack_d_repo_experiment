#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for number-of-islands (LC 200).

Independent of the lesson's flood-fill oracle (drGenSteps, an iterative stack
DFS that counts how many times the scan starts a new flood). This reference
counts connected components a completely different way — iterative LABEL-MIN
PROPAGATION (a relaxation / "label spreading" method, no queue, no flood):

  1. Give every land cell a unique id (row*n + col + 1); water is 0.
  2. Repeatedly sweep the grid; each land cell copies the smallest id among
     itself and its four orthogonal land neighbours. Stop when a full sweep
     changes nothing.
  3. Every connected island has collapsed to a single id (its minimum cell id),
     so the number of distinct nonzero ids == the number of islands.

A different algorithm reaching the same count, so the verifier's cross-check is
not a tautology.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers (one integer island-count per example) on stdout, in order.
"""
import sys
import json

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def num_islands(grid):
    m = len(grid)
    n = len(grid[0]) if m else 0
    label = [[r * n + c + 1 if grid[r][c] == 1 else 0 for c in range(n)] for r in range(m)]
    changed = True
    while changed:
        changed = False
        for r in range(m):
            for c in range(n):
                if label[r][c] == 0:
                    continue
                best = label[r][c]
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and label[nr][nc] != 0:
                        best = min(best, label[nr][nc])
                if best < label[r][c]:
                    label[r][c] = best
                    changed = True
    return len({label[r][c] for r in range(m) for c in range(n) if label[r][c] != 0})


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([num_islands(ex["grid"]) for ex in inputs]))


if __name__ == "__main__":
    main()
