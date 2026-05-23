# Cross-cutting — Known bugs to avoid

These are recurring bugs found during lesson reviews. Read this file when authoring §1 (kernel introducing a counter), §6 (code visualization), or §7 (dry run).

## Diff counter inversion

The direction of diff adjustment is counterintuitive and easy to get backwards.

`freq[x]--` with `old==1` means the slot is going `1 → 0` — a mismatch just resolved, so `diff--`. With `old==0`, the slot goes `0 → -1` — a new mismatch, so `diff++`.

Code that **looks** correct is wrong:

```cpp
freq[c]--;
if (freq[c] == 1) diff++;   // WRONG — old==1 means we just RESOLVED
if (freq[c] == 0) diff--;   // missing the old==0 → diff++ branch
```

The correct logic reads the value **before** the mutation:

```cpp
if (freq[c] == 1) { diff--; }    // freq was 1, now 0 — resolved
else if (freq[c] == 0) { diff++; } // freq was 0, now -1 — new mismatch
freq[c]--;
```

Always verify with a Python trace (`design/python_verify.md`).

## CV scrollbar

Never set `max-height` + `overflow-y: auto` on the code panel. Use `overflow: hidden` only. The scrollbar makes the lesson feel cramped and breaks the visual rhythm. If the code is too long, use a smaller font or tighten the line height — never clip with a scrollbar.

## Variables visible before their line executes

In the code visualization, variable cards initialised at the top of the function (`k`, `n`, `diff`, `maxL`, `maxR`) must not appear populated until the line that assigns them executes. Start all cards dimmed (`opacity: 0.32`), then promote to highlighted as their initialising line fires.

## Collapsed priming steps

In dry-run step generators, never collapse multi-character initialisation into one step. Trace each character. A single "after priming, diff=4" step teaches nothing — the reader needs to see `diff` adjusting character-by-character.

## Wrong expected values in the algorithm test

Always **print what the algorithm actually returns**, then decide if that's the right example to use. Do not write a test with an expected value from memory. The Python verifier is the source of truth.

## Partial state reset on example switch

When the reader switches examples in §7 (dry run), every piece of state must reset: frequency arrays, diff counters, loop indices, result arrays, animation timers, variable card highlights. A partial reset that leaves stale state from the previous example is the most common source of subtle bugs in step generators. **Reset everything, always.**

## When in doubt — heuristics

- Less prose, more pictures.
- Foundational concept visual before kernel paragraph.
- One narrative kernel, then named translations.
- Brute force animation before the optimisation.
- Algorithm in plain English before code.
- Code visualisation before dry run.
- Checklist for production readiness, not prose.
- If a paragraph just describes what a visual already shows, delete the paragraph.
- If a counter or derived value feels magical, build a scanner widget that computes it slot-by-slot.
- Verify the algorithm with Python before writing JS.
