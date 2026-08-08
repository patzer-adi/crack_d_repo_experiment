#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the Kruskal lesson.

Independent of the lesson's oracle (drGenSteps), which is Kruskal: sort every
edge by weight and accept one whenever its endpoints are in different union-find
components.

This reference is Prim's algorithm: start from node 0 and repeatedly absorb the
cheapest edge leaving the tree built so far. It never sorts the edge list, has no
union-find, and grows one connected blob instead of merging many — a genuinely
different strategy that the cut property says must reach the same total weight.

Answer: the total weight of a minimum spanning tree, or null when the graph is
disconnected and no spanning tree exists. Deliberately NOT the accepted-edge
count — Kruskal ends a disconnected run holding a spanning forest while Prim
holds only node 0's component, so that number is implementation-defined.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json


def prim(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    in_tree = [False] * n
    in_tree[0] = True
    total = 0
    for _ in range(n - 1):
        best = None                       # cheapest edge leaving the tree
        for u in range(n):
            if not in_tree[u]:
                continue
            for v, w in adj[u]:
                if in_tree[v]:
                    continue
                if best is None or w < best[0]:
                    best = (w, v)
        if best is None:                  # tree cannot grow => disconnected
            return None
        total += best[0]
        in_tree[best[1]] = True
    return total


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([prim(ex["n"], ex["edges"]) for ex in inputs]))


if __name__ == "__main__":
    main()
