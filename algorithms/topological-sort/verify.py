#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for the Topological Sort lesson.

Independent of the lesson's oracle (drGenSteps), which is Kahn's algorithm:
maintain an in-degree count per node, repeatedly take the smallest node whose
count has fallen to zero, and decrement its successors.

This reference does not compute an in-degree at all. It enumerates permutations
of the nodes in lexicographic order and returns the first one that satisfies
every edge (u must appear before v). If none does, the graph has a cycle and the
answer is []. Brute force over orderings is a completely different mechanism from
incremental in-degree bookkeeping, so agreement is real evidence. It is only
tractable because the examples are tiny, which is exactly what a reference is for.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers on stdout (one per example), in order.
"""
import sys
import json
from itertools import permutations


def lex_smallest_topo_order(n, edges):
    for perm in permutations(range(n)):          # itertools yields these in lex order
        place = {node: i for i, node in enumerate(perm)}
        if all(place[u] < place[v] for u, v in edges):
            return list(perm)
    return []                                    # no valid ordering => a cycle


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([lex_smallest_topo_order(ex["n"], ex["edges"]) for ex in inputs]))


if __name__ == "__main__":
    main()
