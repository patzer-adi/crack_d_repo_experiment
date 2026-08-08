#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the Prim lesson.

Independent of the lesson's oracle (drGenSteps), which is Prim: grow one blob
from node 0, repeatedly absorbing the cheapest edge that leaves it, using a heap
keyed on edge weight.

This reference is Kruskal: sort the whole edge list once and accept any edge
whose endpoints are in different union-find components. It never grows a
connected blob, has no heap, and merges many components at once instead of one.
The cut property says both must reach the same total, so agreement tests the
greedy claim rather than restating it.

Answer: the total weight of a minimum spanning tree, or null when the graph is
disconnected.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json


def kruskal(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    used = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        parent[ru] = rv
        total += w
        used += 1
        if used == n - 1:
            break
    return total if used == n - 1 else None


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([kruskal(ex["n"], ex["edges"]) for ex in inputs]))


if __name__ == "__main__":
    main()
