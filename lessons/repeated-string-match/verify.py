#!/usr/bin/env python3
"""PLAN-019 G4 independent reference for repeated-string-match (LC 686).

Independent of the lesson's oracle (drGenSteps), which builds a.repeat(k) and
calls indexOf(b) — string concatenation plus substring search. This reference
builds NO string and runs NO substring search. Instead it uses the periodic
structure directly:

  b is a substring of some repetition of a  iff  b can be read off the infinite
  tiling a a a ... starting at some offset 0 <= start < len(a). For a given
  start, b matches when b[j] == a[(start + j) % m] for every j; that match needs
  ceil((start + n) / m) copies of a. The answer is the minimum copies over all
  matching offsets, or -1 if no offset matches.

A completely different mechanism (modular character indexing + a copy-count
formula) reaching the same integer, so the verifier's cross-check is not a
tautology.

Protocol: read the EX inputs as a JSON array on stdin, print a JSON array of
answers (one integer per example) on stdout, in order.
"""
import sys
import json


def repeated_string_match(a, b):
    m, n = len(a), len(b)
    best = -1
    for start in range(m):
        if all(b[j] == a[(start + j) % m] for j in range(n)):
            copies = -(-(start + n) // m)   # ceil((start + n) / m)
            if best == -1 or copies < best:
                best = copies
    return best


def main():
    inputs = json.load(sys.stdin)
    print(json.dumps([repeated_string_match(ex["a"], ex["b"]) for ex in inputs]))


if __name__ == "__main__":
    main()
