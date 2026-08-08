#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the Dijkstra lesson.

Independent of the lesson's oracle (drGenSteps), which is Dijkstra: a priority
queue, a settled set, and the greedy claim that the smallest tentative distance
is final. This reference is Bellman-Ford: no queue, no settled set, no greedy
choice — just sweep the whole edge list n-1 times, relaxing whatever improves.
It reaches the same distances by an entirely different argument (induction on
path length, not on the order of settling), so agreement is real evidence.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json

INF = float("inf")


def shortest_distances(n, edges, src):
    dist = [INF] * n
    dist[src] = 0
    for _ in range(max(n - 1, 1)):
        changed = False
        for u, v, w in edges:               # undirected: relax in both directions
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
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
