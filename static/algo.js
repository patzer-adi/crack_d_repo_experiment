/* algo.js — shared painters for ALGORITHM lessons (algorithms/<id>/lesson.html).
   Loaded IN ADDITION TO lesson.js. Pure DOM rendering: a lesson's *GenSteps
   generators must never call anything in here (the correctness gate runs them
   without a DOM). Styles live in static/algo.css.

   gvPaint(conId, cfg, st) — node-link graph
     cfg = { vb, pos, edges, directed?, weights? }
       vb        viewBox string, e.g. '0 0 515 210'
       pos       [[x, y], ...] one per node, in viewBox coordinates
       edges     [[u, v], ...]
       directed  true → draw arrowheads
       weights   [w, ...] parallel to edges; omitted → no weight labels
     st = { nodeCls?, edgeCls?, labels? }
       nodeCls   ['', 'cur' | 'queue' | 'seen' | 'bad', ...] parallel to pos
       edgeCls   ['', 'hot' | 'tree' | 'bad' | 'dim', ...]   parallel to edges
       labels    [string | null, ...] small caption under each node

   dpPaint(conId, cfg, st) — dynamic-programming table
     cfg = { colHead?, rowHead?, corner? }
     st  = { cells: [[{ v, cls } | value, ...], ...] }
       cls in '', 'set', 'cur', 'src', 'best', 'bad', 'dim'

   stripPaint(conId, items) — chip row for a per-node array
     items = [{ text, cls } | string, ...]                                    */

const ALGO_SVG_NS = 'http://www.w3.org/2000/svg';

function gvPaint(conId, cfg, st) {
  const con = document.getElementById(conId);
  if (!con) { return; }
  const pos = cfg.pos, edges = cfg.edges || [];
  const nodeCls = st.nodeCls || [], edgeCls = st.edgeCls || [], labels = st.labels || [];
  con.innerHTML = '';

  const svg = document.createElementNS(ALGO_SVG_NS, 'svg');
  svg.setAttribute('viewBox', cfg.vb);
  svg.setAttribute('class', 'gv-svg');

  if (cfg.directed) {
    const defs = document.createElementNS(ALGO_SVG_NS, 'defs');
    for (const [id, colour] of [['gvArrow', 'var(--border2)'],
                                ['gvArrowHot', 'var(--text-info)'],
                                ['gvArrowTree', 'var(--text-success)']]) {
      const mk = document.createElementNS(ALGO_SVG_NS, 'marker');
      mk.setAttribute('id', id);
      mk.setAttribute('viewBox', '0 0 10 10');
      mk.setAttribute('refX', '9'); mk.setAttribute('refY', '5');
      mk.setAttribute('markerWidth', '5'); mk.setAttribute('markerHeight', '5');
      mk.setAttribute('orient', 'auto-start-reverse');
      const p = document.createElementNS(ALGO_SVG_NS, 'path');
      p.setAttribute('d', 'M 0 1 L 10 5 L 0 9 z');
      p.setAttribute('fill', colour);
      mk.appendChild(p);
      defs.appendChild(mk);
    }
    svg.appendChild(defs);
  }

  const R = 22;
  edges.forEach((e, i) => {
    const a = pos[e[0]], b = pos[e[1]];
    const dx = b[0] - a[0], dy = b[1] - a[1];
    const len = Math.hypot(dx, dy) || 1;
    // stop the line at the node border so an arrowhead is not hidden under the circle
    const pad = cfg.directed ? R + 4 : 0;
    const x1 = a[0] + (dx / len) * (cfg.directed ? R : 0);
    const y1 = a[1] + (dy / len) * (cfg.directed ? R : 0);
    const x2 = b[0] - (dx / len) * pad;
    const y2 = b[1] - (dy / len) * pad;
    const ln = document.createElementNS(ALGO_SVG_NS, 'line');
    ln.setAttribute('x1', x1); ln.setAttribute('y1', y1);
    ln.setAttribute('x2', x2); ln.setAttribute('y2', y2);
    const cls = edgeCls[i] || '';
    ln.setAttribute('class', 'gv-edge' + (cls ? ' ' + cls : ''));
    if (cfg.directed) {
      ln.setAttribute('marker-end',
        cls === 'hot' ? 'url(#gvArrowHot)' : cls === 'tree' ? 'url(#gvArrowTree)' : 'url(#gvArrow)');
    }
    svg.appendChild(ln);

    if (cfg.weights && cfg.weights[i] !== undefined && cfg.weights[i] !== null) {
      const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
      const nx = -dy / len, ny = dx / len;      // unit normal, to nudge off the line
      const t = document.createElementNS(ALGO_SVG_NS, 'text');
      t.setAttribute('x', mx + nx * 11);
      t.setAttribute('y', my + ny * 11 + 4);
      t.setAttribute('class', 'gv-w' + (cls === 'hot' || cls === 'tree' ? ' hot' : ''));
      t.textContent = cfg.weights[i];
      svg.appendChild(t);
    }
  });

  pos.forEach((p, i) => {
    const c = document.createElementNS(ALGO_SVG_NS, 'circle');
    c.setAttribute('cx', p[0]); c.setAttribute('cy', p[1]); c.setAttribute('r', R);
    c.setAttribute('class', 'gv-node' + (nodeCls[i] ? ' ' + nodeCls[i] : ''));
    svg.appendChild(c);

    const t = document.createElementNS(ALGO_SVG_NS, 'text');
    t.setAttribute('x', p[0]); t.setAttribute('y', p[1] + 5);
    t.setAttribute('class', 'gv-id');
    t.textContent = cfg.names ? cfg.names[i] : i;
    svg.appendChild(t);

    if (labels[i] !== undefined && labels[i] !== null && labels[i] !== '') {
      const l = document.createElementNS(ALGO_SVG_NS, 'text');
      l.setAttribute('x', p[0]); l.setAttribute('y', p[1] + 40);
      l.setAttribute('class', 'gv-lbl' + (st.labelOn && st.labelOn[i] ? ' on' : ''));
      l.textContent = labels[i];
      svg.appendChild(l);
    }
  });

  con.appendChild(svg);
}

function dpPaint(conId, cfg, st) {
  const con = document.getElementById(conId);
  if (!con) { return; }
  con.innerHTML = '';
  const wrap = document.createElement('div');
  wrap.className = 'dp-wrap';
  const tbl = document.createElement('table');
  tbl.className = 'dp-table';

  if (cfg.colHead) {
    const thead = document.createElement('thead');
    const tr = document.createElement('tr');
    if (cfg.rowHead) {
      const th = document.createElement('th');
      th.textContent = cfg.corner || '';
      tr.appendChild(th);
    }
    cfg.colHead.forEach(h => {
      const th = document.createElement('th');
      th.textContent = h;
      tr.appendChild(th);
    });
    thead.appendChild(tr);
    tbl.appendChild(thead);
  }

  const tbody = document.createElement('tbody');
  st.cells.forEach((row, r) => {
    const tr = document.createElement('tr');
    if (cfg.rowHead) {
      const th = document.createElement('th');
      th.textContent = cfg.rowHead[r];
      tr.appendChild(th);
    }
    row.forEach(cell => {
      const td = document.createElement('td');
      const isObj = cell !== null && typeof cell === 'object';
      const v = isObj ? cell.v : cell;
      td.textContent = (v === null || v === undefined) ? '·' : v;
      const cls = isObj ? (cell.cls || '') : '';
      if (cls) { td.className = cls; }
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  tbl.appendChild(tbody);
  wrap.appendChild(tbl);
  con.appendChild(wrap);
}

function stripPaint(conId, items) {
  const con = document.getElementById(conId);
  if (!con) { return; }
  con.innerHTML = '';
  (items || []).forEach(it => {
    const s = document.createElement('span');
    const isObj = it !== null && typeof it === 'object';
    s.textContent = isObj ? it.text : it;
    if (isObj && it.cls) { s.className = it.cls; }
    con.appendChild(s);
  });
}
