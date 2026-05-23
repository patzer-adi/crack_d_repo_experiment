# Binary Tree — Skill File

## What it is
A hierarchical structure where each node has at most two children (left, right). Used for BST search/insert/delete, tree traversals (inorder, preorder, postorder, level-order), and recursive divide-and-conquer problems. The key mental model: a tree problem is almost always solved recursively — define what a single node must return to its parent, and trust the recursion to handle the subtree. Height of a balanced tree is O(log n); height of a skewed tree is O(n).

## Visual convention
- **Node shape:** a circle, diameter ~44 px, centred value in bold monospace.
- **Default state:** white/light fill, 1.5 px dark border.
- **Edges:** straight lines from the centre-bottom of the parent to the centre-top of the child. Left child is drawn down-left; right child is down-right.
- **Null child:** shown as a small hollow circle or `∅` label at the expected child position — never omit null children; their presence is often the edge case.
- **Level layout:** nodes at the same depth are on the same horizontal row. Use consistent horizontal spacing to prevent edge crossings.
- **Highlighted states:**
  - `current` / `root of recursion`: blue fill, blue border.
  - `left subtree being processed`: green fill on the subtree root.
  - `right subtree being processed`: amber fill on the subtree root.
  - `visited / returned from`: `opacity: 0.45`, grey fill.
  - `found / matched`: green fill, green border.
  - `path from root to current`: blue edge highlight on the edges along the path.
- **Value labels:** inside the node. If the node stores extra metadata (e.g. BST key + subtree size), show key inside and metadata below in a muted smaller font.
- **Pointer labels:** variable names shown to the side of the node (`root`, `curr`, `node`). Use the same colour as the node's highlight state.

## Animation notes
- **Frame 0:** show the full tree, no highlighting. Caption describes the goal.
- **DFS traversal:** one node processed per frame. Show the call stack depth as a muted number next to the current node, or as a separate call-stack panel listing pending frames. Grey out nodes after their subtree returns.
- **BFS traversal:** show the queue state as a row of node values below the tree. Each frame: dequeue the front, highlight it, enqueue its children (show them being added to the queue row).
- For problems with a return value bubbling up (e.g. height, path sum): annotate each node with the return value in a small badge above or beside the node, shown in the frame when that node's call returns.
- Never try to animate the full recursion tree for deep inputs — pick an example with depth ≤ 4.

## Common pitfalls
- Omitting null children — `∅` nodes are often the base case; not drawing them hides the termination condition.
- Drawing edges that cross — increase horizontal spacing at each level; use 2× the spacing of the level below as a starting point.
- Not greying out returned-from nodes during DFS — the reader loses track of which part of the tree is still "live".
- Showing a recursion with depth > 4 — use a small, concrete example tree; complexity is in the pattern, not the example size.
- Forgetting that inorder traversal of a BST gives a sorted sequence — this property should be captioned when relevant.
- Mixing up left/right assignment — always verify the tree visually matches the input array (level-order) or the problem's stated structure.
