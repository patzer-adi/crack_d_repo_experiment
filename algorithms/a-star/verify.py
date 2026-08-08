#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the A* lesson.

Independent of the lesson's oracle (drGenSteps), which is A*: a priority queue
ordered by f = g + h, with a Manhattan heuristic steering the search toward the
goal. This reference is a plain breadth-first search — no priority queue, no
heuristic, no f-value, no notion of a goal until it is reached. If the heuristic
in the lesson were inadmissible (ever over-estimating), A* would return a longer
path than BFS and this check would catch it. That is exactly the failure the
reference exists to detect.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order. -1 means unreachable.
"""
import sys
import json
from collections import deque


def shortest_steps(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    gr, gc = goal
    if grid[sr][sc] == 1 or grid[gr][gc] == 1:
        return -1
    seen = [[False] * cols for _ in range(rows)]
    seen[sr][sc] = True
    q = deque([(sr, sc, 0)])
    while q:
        r, c, d = q.popleft()
        if (r, c) == (gr, gc):
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] == 0:
                seen[nr][nc] = True
                q.append((nr, nc, d + 1))
    return -1


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([shortest_steps(ex["grid"], ex["start"], ex["goal"]) for ex in inputs]))


if __name__ == "__main__":
    main()
