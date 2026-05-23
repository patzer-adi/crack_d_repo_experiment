# Linked List — Skill File

## What it is
A sequence of nodes where each node stores a value and a pointer to the next node. Unlike arrays, nodes are not contiguous in memory — traversal is always O(n), random access is O(n), prepend is O(1). Appears in problems involving pointer manipulation, cycle detection, reversal, and merging. The key mental model: at any moment you hold a pointer to exactly one node; you can look at its value and follow its `next`, nothing else.

## Visual convention
- **Node shape:** a rounded rectangle split vertically into two cells: `[ data | next→ ]`.
  - Left cell: the stored value, centred, bold monospace font.
  - Right cell: the arrow `→` (or `∅` if null), centred, muted text.
  - Width: data cell ~52 px, next cell ~28 px; height ~40 px.
- **Arrow:** a horizontal arrow connecting the right cell of one node to the left cell of the next. Use `→` inline or an SVG line; never leave the gap implicit.
- **Null terminator:** the last node's right cell shows `∅`, and no arrow is drawn after it.
- **Memory address (optional):** shown in a smaller muted label below each node (e.g. `0x04`). Include when the problem requires understanding pointer identity (cycle detection, node deletion).
- **Pointer labels:** variable names shown above or below the node they point to, coloured to match role:
  - `head` — blue, shown above the first node.
  - `curr` / `cur` — blue, shown above the current traversal node.
  - `prev` — green, shown above the previous node.
  - `slow` — green; `fast` — amber (Floyd's cycle detection).
  - `p1`, `p2` (two-list merge) — green and amber respectively.
- **Highlighted node:** border and background match the pointer colour (blue/green/amber); default state is white/light.
- **Deleted / unlinked node:** `opacity: 0.35`, dashed border, no pointer label.
- **Reversed arrow:** when illustrating an in-place reversal, draw the arrow pointing leftward from the node being reversed; the `next` cell shows `←`.
- Layout: left-to-right, single horizontal row. For circular lists, show a curved return arrow from tail to head.

## Animation notes
Linked list nodes are rendered by the pattern skill file (e.g. two-pointer sweeps, cycle detection). When drawing an animation frame:
- Show the full list every frame; do not truncate.
- Move only one pointer per frame.
- When a pointer is reassigned (`prev = curr; curr = curr.next`), show the intermediate state (prev on old curr, curr on new node) as a separate frame if it reduces confusion.
- For in-place reversal: animate the `next` pointer flip one node at a time; do not show the final reversed list until all flips are done.
- For cycle detection: show both `slow` and `fast` every frame; label the meeting point when they coincide.

## Common pitfalls
- Drawing the `next` cell with a numeric address instead of a visual arrow — use arrows, not pointer values.
- Omitting the `∅` terminator — always show it; many bugs come from failing to null-check the tail.
- Moving `curr` before saving `curr.next` during reversal — show the save step explicitly as a frame.
- Showing only the current node and hiding the rest of the list — always show the whole list so the reader can see traversal progress.
- Labelling the node with the variable name AND the memory address in the same label — keep pointer label (above) and address (below) separate.
- For two-pointer problems on a linked list: do not use L/R labels — use the problem's own variable names (`slow`/`fast`, `p1`/`p2`) to avoid confusion with the array two-pointer convention.
