#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for subsets (LC 78).

Independent of the lesson's recursive backtracking oracle (drGenSteps): this is
the ITERATIVE BITMASK enumeration — no recursion, no call stack. Count an n-bit
integer `mask` from 0 to 2**n - 1; each value is one include/skip pattern.

To match the depth-first order the backtracking oracle emits, note how that
oracle orders things: it decides element 0 first and tries the SKIP branch
before the INCLUDE branch, so element 0 is the *most significant* choice — the
empty set (skip everything) comes out first and the full set last. We reproduce
that by reading element i from bit (n-1-i): the leftmost bit is element 0. A
completely different mechanism (plain integer counting + bit math) reaching the
same list in the same order, so the verifier's cross-check is not a tautology.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers (one power set per example) on stdout, in order.
"""
import sys
import json


def subsets(nums):
    n = len(nums)
    out = []
    for mask in range(1 << n):
        sub = [nums[i] for i in range(n) if mask & (1 << (n - 1 - i))]
        out.append(sub)
    return out


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([subsets(ex["nums"]) for ex in inputs]))


if __name__ == "__main__":
    main()
