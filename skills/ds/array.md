# Array — Skill File

## What it is
A contiguous, zero-indexed sequence of elements stored in a single row. Appears in the majority of interview problems. Visually the simplest data structure; the foundation on which pointer, sliding-window, and prefix-sum patterns are drawn. Sorting the array first is a prerequisite for several O(n²) patterns that would otherwise be O(n³).

## Visual convention
- Each element: a fixed-width square box, minimum 46 px wide, border-radius 8 px, 0.5 px border.
- **Index label:** shown **above** each box in a smaller muted font (grey, e.g. `#9ca3af`), centred. Never omit the index row.
- **Value:** centred inside the box, bold monospace font.
- **Default state:** white/light background, grey border.
- **Active / anchor element (i):** blue background (`--color-background-info`), blue border, blue text.
- **Left-pointer element (L):** green background (`--color-background-success`), green border, green text.
- **Right-pointer element (R):** amber/orange background (`--color-background-warning`), amber border, amber text.
- **Found / matched element:** green background on both L and R cells (same as L colour), to signal the triplet is recorded.
- **Processed / duplicate-skipped element:** `opacity: 0.35` on the cell, no colour change, to show the outer-loop duplicate skip.
- **Pointer label:** a small text label (`i`, `L`, `R`) rendered **below** the box, 10 px font, coloured to match the pointer (blue / green / amber). Label is the variable name, not the index value.
- Layout: always left-to-right, single horizontal row. Use a 2-D grid skill file for matrix problems.

## Animation rules
- Each animation step is a discrete frame; navigation is button-driven (Prev / Next) with an optional auto-play.
- Frame 0: show the sorted array with no pointers highlighted; caption explains the sort step.
- Each subsequent frame: show the current state of `i`, `L`, `R` → display the decision label in the step panel → pointer moves in the **next** frame (i.e. caption describes what is about to happen, positions reflect the state *after* the decision).
- When a triplet is found: briefly colour both L and R green (`.af` class) in the same frame as the "✓ Found!" caption.
- When duplicate values are skipped at L/R: show a separate frame captioned "Skip duplicate L/R values" with the new positions, before continuing.
- When the outer-loop index `i` hits a duplicate, fade that cell out (`opacity: 0.35`) and caption "skip dup i".
- Show `nums[i] + nums[L] + nums[R] = value` in a monospace line above the step panel, updated each frame.
- Show all found triplets as green badges below the controls, accumulated across frames.

## Common pitfalls
- Index labels start at 0, not 1. Never omit the index row above the cells.
- Pointer label must show the variable name (`L`, `R`) not the index number — showing the index value only confuses problems where the pointer jumps non-consecutively.
- Do not move both L and R in the same animation frame. One pointer move per frame.
- Do not skip the duplicate-avoidance frame — animate `while nums[L] == nums[L+1]: L++` explicitly as a separate "skip dup" step.
- Do not skip the sort-step frame for problems that require sorting; show the sorted array as frame 0 before any pointer is placed. Omit it for problems that do not sort (e.g. Container With Most Water).
- When any formula uses index arithmetic (e.g. `R − L` as a width), show the full substitution: `R − L = 8 − 1 = 7`. Never display a bare number without tracing it to its source indices.
