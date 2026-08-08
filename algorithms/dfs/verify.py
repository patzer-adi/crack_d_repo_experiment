#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the DFS lesson.

Independent of the lesson's oracle (drGenSteps), which is an explicit-stack DFS
that dives deep and restarts. This is union-find (disjoint-set with path
compression): it never traverses the graph at all — it just merges the two
endpoints of every edge and reads off the resulting classes. A completely
different mechanism that must produce the same components.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json


def components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv

    groups = {}
    for x in range(n):
        groups.setdefault(find(x), []).append(x)
    return sorted((sorted(g) for g in groups.values()), key=lambda g: g[0])


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([components(ex["n"], ex["edges"]) for ex in inputs]))


if __name__ == "__main__":
    main()
