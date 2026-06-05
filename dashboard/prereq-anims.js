/* ──────────────────────────────────────────────────────────────
   PLAN-021 — hero animations for the Prerequisites tab.

   Lightweight, vanilla, step-driven widgets (Prev / Next over a small
   array of pre-rendered frames). These are dashboard widgets, NOT gated
   lessons, so they are intentionally out of the lesson render/verify gate.

   To add one: write a mount(host) that calls buildStepper(host, title,
   frames), then register it in PREREQ_ANIMS by the id a prerequisite's
   `animation` field references. The .pa-* styles live in dashboard/index.html.
   ────────────────────────────────────────────────────────────── */

// Generic stepper. `frames` is an array of { stage: htmlString, cap: htmlString }.
function buildStepper(host, title, frames) {
  host.innerHTML = `
    <div class="pa-wrap">
      <div class="pa-title">${title}</div>
      <div class="pa-stage"></div>
      <div class="pa-caption"></div>
      <div class="pa-controls">
        <button class="pa-btn" data-act="prev">‹ Prev</button>
        <span class="pa-counter"></span>
        <button class="pa-btn" data-act="next">Next ›</button>
      </div>
    </div>`;
  const stage   = host.querySelector('.pa-stage');
  const caption = host.querySelector('.pa-caption');
  const counter = host.querySelector('.pa-counter');
  const prevBtn = host.querySelector('[data-act="prev"]');
  const nextBtn = host.querySelector('[data-act="next"]');

  let i = 0;
  function draw() {
    stage.innerHTML   = frames[i].stage;
    caption.innerHTML = frames[i].cap;
    counter.textContent = `Step ${i + 1} / ${frames.length}`;
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i === frames.length - 1;
  }
  prevBtn.addEventListener('click', () => { if (i > 0) { i--; draw(); } });
  nextBtn.addEventListener('click', () => { if (i < frames.length - 1) { i++; draw(); } });
  draw();
}

// ── Hash Map: hashing, a collision, then an O(1) lookup ──────────
function mountHashMap(host) {
  const N = 5;
  // bucket contents after each insert; [] = empty, arrays chain on collision
  const buckets = (hl, slots) => {
    let cells = '';
    for (let b = 0; b < N; b++) {
      const items = (slots[b] || []).map(v =>
        `<span class="pa-slot${hl.slot === v ? ' hl' : ''}">${v}</span>`).join('<span class="pa-link">→</span>');
      cells += `<div class="pa-bucket${hl.bucket === b ? ' hl' : ''}">
                  <div class="pa-bidx">${b}</div>
                  <div class="pa-chain">${items || '<span class="pa-empty">·</span>'}</div>
                </div>`;
    }
    return `<div class="pa-buckets">${cells}</div>`;
  };
  const s0 = {}, s1 = { 3: [13] }, s2 = { 3: [13], 2: [7] },
        s3 = { 3: [13], 2: [7], 4: [4] }, s4 = { 3: [13], 2: [7, 12], 4: [4] };
  const frames = [
    { stage: buckets({}, s0),
      cap: 'A hash map has a fixed row of buckets. To place a key we hash it: <code>bucket = key % 5</code>.' },
    { stage: buckets({ bucket: 3, slot: 13 }, s1),
      cap: '<code>put(13)</code>: 13 % 5 = <b>3</b> → drop 13 into bucket 3.' },
    { stage: buckets({ bucket: 2, slot: 7 }, s2),
      cap: '<code>put(7)</code>: 7 % 5 = <b>2</b> → bucket 2.' },
    { stage: buckets({ bucket: 4, slot: 4 }, s3),
      cap: '<code>put(4)</code>: 4 % 5 = <b>4</b> → bucket 4.' },
    { stage: buckets({ bucket: 2, slot: 12 }, s4),
      cap: '<code>put(12)</code>: 12 % 5 = <b>2</b>, but bucket 2 already holds 7 — a <b>collision</b>, so we chain 12 after it.' },
    { stage: buckets({ bucket: 2, slot: 7 }, s4),
      cap: '<code>get(7)</code>: jump straight to bucket 2 in O(1) and scan its tiny chain — no walk over the whole map.' },
  ];
  buildStepper(host, 'Hash map — hashing, collision, O(1) lookup', frames);
}

// ── Binary Search: halving a sorted range to find 13 ─────────────
function mountBinarySearch(host) {
  const a = [1, 3, 5, 7, 9, 11, 13, 15];
  const row = (lo, hi, mid, found) => {
    let cells = a.map((v, k) => {
      let cls = 'pa-cell';
      if (k < lo || k > hi) cls += ' dim';
      if (k === found) cls += ' found';
      else if (k === mid) cls += ' mid';
      return `<div class="${cls}"><div class="pa-cidx">${k}</div><div class="pa-cval">${v}</div></div>`;
    }).join('');
    return `<div class="pa-cells">${cells}</div>`;
  };
  const frames = [
    { stage: row(0, 7, -1, -1),
      cap: 'Find <b>13</b> in a sorted array. Range <code>lo=0, hi=7</code>.' },
    { stage: row(0, 7, 3, -1),
      cap: '<code>mid=3</code> → a[3]=7 &lt; 13, so the answer is to the right. Discard the left half, <code>lo=4</code>.' },
    { stage: row(4, 7, 5, -1),
      cap: '<code>mid=5</code> → a[5]=11 &lt; 13, discard again, <code>lo=6</code>.' },
    { stage: row(6, 7, 6, 6),
      cap: '<code>mid=6</code> → a[6]=13 = target. <b>Found</b> in 3 steps (log₂8 = 3 max).' },
  ];
  buildStepper(host, 'Binary search — halving a sorted range', frames);
}

// ── Recursion: the call stack of fact(3) growing then unwinding ──
function mountRecursion(host) {
  // each frame lists the live stack top→bottom; `ret` annotates a returning frame
  const stack = (rows) => {
    if (!rows.length) return `<div class="pa-stack"><div class="pa-empty-stack">empty stack</div></div>`;
    const items = rows.map(r =>
      `<div class="pa-frame${r.base ? ' base' : ''}${r.ret ? ' ret' : ''}">
         <span>${r.label}</span>${r.note ? `<span class="pa-fnote">${r.note}</span>` : ''}
       </div>`).join('');
    return `<div class="pa-stack">${items}</div>`;
  };
  const F = (label, note, opt) => ({ label, note, ...(opt || {}) });
  const frames = [
    { stage: stack([]),
      cap: 'Compute <code>fact(3)</code>, where <code>fact(n) = n · fact(n−1)</code> and <code>fact(0) = 1</code>.' },
    { stage: stack([F('fact(3)', 'waits for fact(2)')]),
      cap: '<code>fact(3)</code> is called and pushed — it pauses, needing <code>fact(2)</code>.' },
    { stage: stack([F('fact(2)', 'waits for fact(1)'), F('fact(3)', '…')]),
      cap: '<code>fact(2)</code> pushed on top. The stack grows as each call waits for a smaller one.' },
    { stage: stack([F('fact(1)', 'waits for fact(0)'), F('fact(2)', '…'), F('fact(3)', '…')]),
      cap: '<code>fact(1)</code> pushed.' },
    { stage: stack([F('fact(0)', 'returns 1', { base: true }), F('fact(1)', '…'), F('fact(2)', '…'), F('fact(3)', '…')]),
      cap: '<code>fact(0)</code> hits the <b>base case</b> → returns 1. Now the stack unwinds.' },
    { stage: stack([F('fact(1)', 'returns 1·1 = 1', { ret: true }), F('fact(2)', '…'), F('fact(3)', '…')]),
      cap: '<code>fact(1)</code> resumes: 1 · 1 = 1, returns, and pops off.' },
    { stage: stack([F('fact(2)', 'returns 2·1 = 2', { ret: true }), F('fact(3)', '…')]),
      cap: '<code>fact(2)</code> resumes: 2 · 1 = 2, pops off.' },
    { stage: stack([F('fact(3)', 'returns 3·2 = 6', { ret: true })]),
      cap: '<code>fact(3)</code> resumes: 3 · 2 = <b>6</b>, pops off — the stack is empty again.' },
  ];
  buildStepper(host, 'Recursion — the call stack of fact(3)', frames);
}

const PREREQ_ANIMS = {
  'anim-hash-map':      mountHashMap,
  'anim-binary-search': mountBinarySearch,
  'anim-recursion':     mountRecursion,
};

// Called by buildPrereqCard once the card is in the DOM.
function mountPrereqAnim(id, host) {
  const fn = PREREQ_ANIMS[id];
  if (fn) fn(host);
}
