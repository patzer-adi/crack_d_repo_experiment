# BFS / DFS — Skill File

## What it is
Graph and tree traversal strategies for visiting all reachable nodes. Both achieve O(V + E) time.

**BFS (Breadth-First Search):** explores level by level using a queue. Guarantees the shortest path (in terms of edge count) to any node when all edge weights are equal. Best for: shortest path, level-order traversal, minimum steps problems.

**DFS (Depth-First Search):** explores as deep as possible along one branch before backtracking, using a stack (explicit or the call stack). Best for: connected component detection, cycle detection, topological sort, path enumeration, tree recursion.

Canonical problems: Number of Islands, Word Ladder, Clone Graph, Course Schedule, Binary Tree Level Order Traversal, Pacific Atlantic Water Flow.

## Visual convention

### Graph / grid layout
- **Node (graph):** circle ~40 px diameter, node ID inside, bold monospace.
- **Cell (grid/matrix):** square ~38 px, value inside. Grid problems are matrices — show as a 2-D grid, not as a node graph.
- **Edge (graph):** straight line between node centres. Directed edges have an arrowhead; undirected edges do not.
- **States:**
  - `unvisited`: white fill, grey border.
  - `in frontier / queue / stack`: amber fill (`--bg-warn`), amber border. "About to be processed."
  - `visited / processed`: blue fill (`--bg-info`), blue border. "Already dequeued and explored."
  - `current` (node being processed this frame): green fill (`--bg-success`), green border.
  - `source`: blue-filled with a bold `S` label; `target`: amber with bold `T` label (when applicable).
  - `blocked / wall` (grid): dark grey fill (e.g. `#6b7280`).
- **BFS distance label:** for shortest-path BFS, show the discovered distance as a small badge above each node, revealed when that node is first enqueued.

### Queue / Stack panel
Below or beside the graph, show the current state of the auxiliary data structure every frame:
- **BFS queue:** a horizontal row of node IDs, front on the left. Label: `Queue: [ A, B, C ]`.
- **DFS stack:** a vertical column of node IDs, top on the top. Label: `Stack: [ A, B, C ]` (or "Call stack" for recursive DFS).
- When an element is enqueued/pushed: show it being added to the right (queue) or top (stack).
- When dequeued/popped: remove from the left (queue) or top (stack) in the same frame.

## Animation rules

### Controls — required on every lesson
Every animated dry run must include four controls: ← Prev, ▶ Auto / ⏸ Pause, Next →, ↺ Reset.
Keyboard shortcuts: ← → for prev/next, Space for auto/pause, R or Esc for reset.
See `skills/patterns/two_pointers.md` for the keyboard listener snippet.

### Stable panel layout
Use `.panels-fixed` or equivalent fixed-height containers for the queue/stack panel and step panel so controls do not shift as panel content changes.

### Step panel — structured reasoning
1. **What:** the operation performed (`dequeue A → process neighbours B, C, D`).
2. **Why:** the invariant it maintains (`BFS processes all distance-k nodes before distance-(k+1)`).

### Frame sequencing — BFS
- **Frame 0:** graph/grid shown, source node amber (in queue), queue = `[source]`. All other nodes unvisited (white).
- **Each iteration:**
  1. Dequeue front → colour it green (current).
  2. For each unvisited neighbour: colour amber (enqueue), add to queue panel, record distance = parent distance + 1.
  3. Colour dequeued node blue (visited) at end of its frame.
- **Final frame:** target node reached (green), or queue empty (no path). Caption: "Shortest path = D steps."
- Process one node per frame. Enqueuing all neighbours of one node counts as one frame.

### Frame sequencing — DFS (iterative)
- **Frame 0:** graph/grid, source node amber (pushed), stack = `[source]`.
- **Each iteration:**
  1. Pop top → colour it green (current). Check visited; skip if already visited.
  2. Mark visited (blue). Push unvisited neighbours onto stack (amber), in desired order.
- **Final frame:** target found or stack empty.

### Frame sequencing — DFS (recursive / tree)
Follow the binary_tree.md animation notes: one node processed per frame, grey out after subtree returns, show call-stack depth beside current node.

## Algorithmic template (C++)

BFS (shortest path in unweighted graph):
```cpp
int bfs(vector<vector<int>>& adj, int src, int dst, int n) {
    vector<int> dist(n, -1);
    queue<int> q;
    dist[src] = 0;
    q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        if (u == dst) return dist[u];
        for (int v : adj[u]) {
            if (dist[v] == -1) {        // unvisited
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return -1;                          // unreachable
}
```

DFS (connected components / visited marking):
```cpp
void dfs(vector<vector<int>>& adj, vector<bool>& vis, int u) {
    vis[u] = true;
    for (int v : adj[u])
        if (!vis[v]) dfs(adj, vis, v);
}

int countComponents(int n, vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); adj[e[1]].push_back(e[0]); }
    vector<bool> vis(n, false);
    int count = 0;
    for (int i = 0; i < n; i++)
        if (!vis[i]) { dfs(adj, vis, i); count++; }
    return count;
}
```

BFS on grid (Number of Islands):
```cpp
int numIslands(vector<vector<char>>& grid) {
    int m = grid.size(), n = grid[0].size(), islands = 0;
    auto bfs = [&](int r, int c) {
        queue<pair<int,int>> q;
        grid[r][c] = '0';               // mark visited in-place
        q.push({r, c});
        while (!q.empty()) {
            auto [x, y] = q.front(); q.pop();
            for (auto [dx, dy] : vector<pair<int,int>>{{0,1},{0,-1},{1,0},{-1,0}}) {
                int nx = x+dx, ny = y+dy;
                if (nx>=0 && nx<m && ny>=0 && ny<n && grid[nx][ny]=='1') {
                    grid[nx][ny] = '0';
                    q.push({nx, ny});
                }
            }
        }
    };
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++)
            if (grid[r][c] == '1') { bfs(r, c); islands++; }
    return islands;
}
```

## Common pitfalls
- Not showing the queue/stack state panel — the auxiliary data structure is the heart of the algorithm; hiding it makes the traversal order opaque.
- Colouring a node "visited" when it is first pushed/enqueued (it should be amber — "about to be processed") rather than when it is popped/dequeued and processed (it should be blue). BFS visits a node when it is dequeued, not when it is enqueued.
- Processing multiple nodes per frame — one dequeue/pop per frame; enqueuing all the neighbours of that one node is acceptable in the same frame.
- For grid problems: not showing the 4-directional neighbours explicitly — list the `(dx, dy)` deltas in the formula panel so the neighbour-generation logic is visible.
- Forgetting to mark nodes visited before enqueuing (BFS) — if you mark only when dequeued, the same node can be enqueued multiple times; show the mark-on-enqueue rule in the formula panel.
- Mixing up BFS and DFS in the same animation — pick one for the primary animation; mention the other in a separate tab with code only.
- For cycle detection with DFS: not distinguishing `visited` (fully processed) from `in-stack` (currently on the recursion path) — use two separate colours (blue vs amber) for these two states.
