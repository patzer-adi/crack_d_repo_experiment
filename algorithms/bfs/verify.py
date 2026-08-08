#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the BFS lesson.

Independent of the lesson's oracle (drGenSteps), which is a queue BFS that
expands the graph in rings. This is Bellman-Ford relaxation to a fixpoint:
sweep the whole edge list over and over, lowering dist[v] to dist[u] + 1
whenever that helps, until a full sweep changes nothing. No queue, no frontier,
no rings — a different algorithm that must land on the same distance array, so
the cross-check is evidence rather than a restatement.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json

INF = float("inf")


def shortest_distances(n, edges, src):
    dist = [INF] * n
    dist[src] = 0
    # n - 1 sweeps suffice for a shortest path of at most n - 1 edges; the
    # early exit just stops sooner once nothing moves.
    for _ in range(max(n - 1, 1)):
        changed = False
        for u, v in edges:                 # undirected: relax both ways
            if dist[u] + 1 < dist[v]:
                dist[v] = dist[u] + 1
                changed = True
            if dist[v] + 1 < dist[u]:
                dist[u] = dist[v] + 1
                changed = True
        if not changed:
            break
    return [-1 if d == INF else d for d in dist]


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([shortest_distances(ex["n"], ex["edges"], ex["src"])
                      for ex in inputs]))


if __name__ == "__main__":
    main()
