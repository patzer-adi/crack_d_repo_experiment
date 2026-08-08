#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the Borůvka lesson.

Independent of the lesson's oracle (drGenSteps), which is Borůvka: every
component picks its own cheapest outgoing edge simultaneously, then all the
chosen edges are merged in one go, halving the component count each round.

This reference is Prim's algorithm: one blob, grown one node at a time by its
cheapest exit, with no rounds and no simultaneous choices. Borůvka's whole risk
is the tie-break (two components choosing the same edge from opposite ends, or a
cycle forming when equal weights let several picks close a loop). Prim cannot
make that mistake, so it is the right thing to check against.

Answer: the total weight of a minimum spanning tree, or null when the graph is
disconnected.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json
import heapq


def prim(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    in_tree = [False] * n
    pq = [(0, 0)]
    total = 0
    used = 0
    while pq:
        w, u = heapq.heappop(pq)
        if in_tree[u]:
            continue
        in_tree[u] = True
        total += w
        used += 1
        for wt, v in adj[u]:
            if not in_tree[v]:
                heapq.heappush(pq, (wt, v))
    return total if used == n else None


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([prim(ex["n"], ex["edges"]) for ex in inputs]))


if __name__ == "__main__":
    main()
