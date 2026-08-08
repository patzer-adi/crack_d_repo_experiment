#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the Bellman-Ford lesson.

Independent of the lesson's oracle (drGenSteps), which is Bellman-Ford itself:
n-1 single-source relaxation rounds over the edge list, plus one extra round to
detect a negative cycle.

This reference is Floyd-Warshall: an all-pairs dynamic program over an
intermediate-vertex index k, with no notion of a "round" and no source at all
until the very end, when the source's row is read off. Negative cycles are found
from the diagonal (dist[k][k] < 0) rather than from a late improvement. Different
recurrence, different detection rule, same answer.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order. An answer is
{"dist": [...], "neg": bool}; an unreachable node is null.
"""
import sys
import json

INF = float("inf")


def floyd_warshall(n, edges, src):
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:                       # directed; keep the cheapest parallel edge
        if w < d[u][v]:
            d[u][v] = w

    for k in range(n):
        for i in range(n):
            if d[i][k] == INF:
                continue
            for j in range(n):
                if d[k][j] == INF:
                    continue
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]

    # A negative cycle matters only if the source can reach it.
    neg = any(d[k][k] < 0 and d[src][k] < INF for k in range(n))
    if neg:
        return {"dist": None, "neg": True}
    return {"dist": [None if x == INF else x for x in d[src]], "neg": False}


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([floyd_warshall(ex["n"], ex["edges"], ex["src"]) for ex in inputs]))


if __name__ == "__main__":
    main()
