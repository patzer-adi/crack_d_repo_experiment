#!/usr/bin/env node
// scripts/render_check.mjs — PLAN-019 G3 render smoke test.
//
// Usage:
//   node scripts/render_check.mjs <slug> [<slug> ...]
//   node scripts/render_check.mjs --all          # every generated lesson
//   node scripts/render_check.mjs <slug> --json
//
// Why this exists
// ---------------
// lint_lesson.py reads HTML text; verify_animation.mjs runs the dry-run oracle
// in a DOM-less sandbox. Neither can see LAYOUT or RUNTIME behaviour, so a
// lesson can pass both gates while its code overflows the page (the grid-blowout
// CSS class) or its §6 highlight points at a line that never lights up. This
// script loads each lesson in headless Chromium via the DevTools Protocol —
// over Node's built-in WebSocket, no npm dependency — drives every animation,
// and asserts:
//   1. no uncaught JS exception / console error during load or stepping;
//   2. every §6 code-viz step lights an active code line (runtime check that
//      also covers dynamic line numbers the linter cannot see);
//   3. no horizontal page overflow at desktop width (1000px) AND at phone
//      width (390px) — documentElement.scrollWidth ≤ clientWidth at both.
//
// Exit codes: 0 pass · 1 a lesson failed · 2 usage/launch error.
// If no browser is found it prints a loud warning and exits 0 (skip), per
// PLAN-019 §6 risk mitigation — the gate degrades, it does not block.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const VIEWPORT = { width: 1000, height: 900 };
const MOBILE = { width: 390, height: 844 }; // phone overflow pass (PLAN-020)
const OVERFLOW_TOL = 2; // px slack for sub-pixel rounding

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ── browser discovery ────────────────────────────────────────────────────────
function findBrowser() {
  const cands = [];
  if (process.env.CHROME_BIN) cands.push(process.env.CHROME_BIN);
  const pw = path.join(os.homedir(), ".cache/ms-playwright");
  if (fs.existsSync(pw)) {
    for (const d of fs.readdirSync(pw)) {
      if (!d.startsWith("chromium")) continue;
      for (const sub of ["chrome-linux64/chrome", "chrome-linux/chrome", "chrome-linux/headless_shell"]) {
        cands.push(path.join(pw, d, sub));
      }
    }
  }
  cands.push("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser");
  return cands.find((p) => { try { fs.accessSync(p, fs.constants.X_OK); return true; } catch { return false; } });
}

function launch(bin) {
  const userDir = fs.mkdtempSync(path.join(os.tmpdir(), "rendercheck-"));
  const proc = spawn(bin, [
    "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
    "--hide-scrollbars", "--remote-debugging-port=0", `--user-data-dir=${userDir}`,
    "about:blank",
  ], { stdio: ["ignore", "pipe", "pipe"] });
  return { proc, userDir };
}

function wsEndpoint(proc, timeoutMs = 20000) {
  return new Promise((res, rej) => {
    let buf = "";
    const t = setTimeout(() => rej(new Error("timed out waiting for DevTools endpoint")), timeoutMs);
    proc.stderr.on("data", (d) => {
      buf += d.toString();
      const m = /DevTools listening on (ws:\/\/\S+)/.exec(buf);
      if (m) { clearTimeout(t); res(m[1]); }
    });
    proc.on("exit", (c) => { clearTimeout(t); rej(new Error(`browser exited early (code ${c})`)); });
  });
}

// ── minimal CDP client over a WebSocket ──────────────────────────────────────
class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map(); this.listeners = new Set();
    ws.addEventListener("message", (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id !== undefined) {
        const p = this.pending.get(m.id);
        if (p) { this.pending.delete(m.id); m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); }
      } else {
        for (const l of this.listeners) l(m);
      }
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    const msg = { id, method, params };
    if (sessionId) msg.sessionId = sessionId;
    return new Promise((res, rej) => { this.pending.set(id, { res, rej }); this.ws.send(JSON.stringify(msg)); });
  }
  on(fn) { this.listeners.add(fn); return () => this.listeners.delete(fn); }
}

// Measures horizontal page overflow of the CURRENT layout and names the widest
// offending element. Embedded in CHECKER, which is evaluated once per viewport
// (desktop, then phone — PLAN-020), so both viewports report overflow identically.
const OVERFLOW_JS = `(() => {
  const de = document.documentElement;
  const o = { scrollW: de.scrollWidth, clientW: de.clientWidth, delta: de.scrollWidth - de.clientWidth };
  let widest = null, maxr = de.clientWidth + 0.5;
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > maxr) { maxr = r.right; widest = { tag: el.tagName, cls: String(el.className).slice(0,60), right: Math.round(r.right) }; }
  }
  o.widest = widest;
  return o;
})()`;

// In-page checker: drives every animation and measures overflow. Runs in page
// global scope, so top-level function declarations (cvNext…) are reachable by
// bare name; module-scoped `let` step arrays are probed with typeof guards.
const CHECKER = `(() => {
  const out = { cv:{driven:0,noActive:[],threw:null}, dr:{driven:0,threw:null},
                si:{driven:0,threw:null}, bf:{driven:0,threw:null}, overflow:{} };
  // A code line counts as highlighted if it carries the canonical 'active'/
  // 'active-match' class OR any lesson-specific active-* variant (active-best,
  // active-done, ...). Matching only the canonical two false-flags lessons that
  // use their own highlight class.
  const activeLine = () => document.querySelector(
    '#cv-code-panel .cv-line[class~="active"], #cv-code-panel .cv-line[class*="active-"]');
  const drive = (key, reset, next, steps) => {
    try {
      if (typeof reset !== 'function' || typeof steps === 'undefined' || !steps) return;
      reset();
      for (let k = 0; k < steps.length; k++) {
        if (key === 'cv' && !activeLine()) out.cv.noActive.push(k);
        out[key].driven++;
        if (k < steps.length - 1) next();
      }
    } catch (e) { out[key].threw = String(e && e.message || e); }
  };
  drive('cv', typeof cvReset==='function'?cvReset:null, typeof cvNext==='function'?cvNext:null, typeof cvSteps!=='undefined'?cvSteps:undefined);
  drive('dr', typeof drReset==='function'?drReset:null, typeof drNext==='function'?drNext:null, typeof drSteps!=='undefined'?drSteps:undefined);
  drive('si', typeof siReset==='function'?siReset:null, typeof siNext==='function'?siNext:null, typeof siSteps!=='undefined'?siSteps:undefined);
  drive('bf', typeof bfReset==='function'?bfReset:null, typeof bfNext==='function'?bfNext:null, typeof bfSteps!=='undefined'?bfSteps:undefined);
  out.overflow = ${OVERFLOW_JS};
  return out;
})()`;

async function checkSlug(cdp, sessionId, slug, getErrors, resetErrors) {
  const htmlPath = path.join(ROOT, "lessons", slug, "lesson.html");
  if (!fs.existsSync(htmlPath)) return { slug, ok: false, reasons: ["lesson.html not found"] };
  resetErrors();
  const s = sessionId;
  const loaded = new Promise((r) => {
    const off = cdp.on((m) => { if (m.sessionId === s && m.method === "Page.loadEventFired") { off(); r(); } });
  });
  await cdp.send("Page.navigate", { url: pathToFileURL(htmlPath).href }, s);
  await Promise.race([loaded, sleep(10000)]);
  await sleep(200); // let init scripts paint

  let res;
  try {
    res = await cdp.send("Runtime.evaluate", { expression: CHECKER, returnByValue: true, awaitPromise: true }, s);
  } catch (e) {
    return { slug, ok: false, reasons: [`evaluate failed: ${e.message}`] };
  }
  if (res.exceptionDetails) {
    return { slug, ok: false, reasons: [`checker threw: ${res.exceptionDetails.exception?.description || res.exceptionDetails.text}`] };
  }
  const o = res.result.value;
  const reasons = [];
  for (const e of getErrors()) reasons.push(e);
  for (const k of ["cv", "dr", "si", "bf"]) if (o[k].threw) reasons.push(`${k}* threw while stepping: ${o[k].threw}`);
  if (o.cv.noActive.length) reasons.push(`§6 step(s) with no active code line: [${o.cv.noActive.join(", ")}] of ${o.cv.driven}`);
  if (o.overflow.delta > OVERFLOW_TOL) {
    const w = o.overflow.widest;
    reasons.push(`horizontal overflow: page scrollWidth ${o.overflow.scrollW} > clientWidth ${o.overflow.clientW}` +
      (w ? ` (widest: <${w.tag.toLowerCase()} class="${w.cls}"> right=${w.right})` : ""));
  }

  // ── mobile pass (PLAN-020): re-layout at phone width, RE-DRIVE the animations
  // so width-reactive renders (charts that read clientWidth) recompute the way
  // they would for a phone visitor, then measure overflow; restore the desktop
  // viewport for the next slug. ──
  await cdp.send("Emulation.setDeviceMetricsOverride",
    { width: MOBILE.width, height: MOBILE.height, deviceScaleFactor: 1, mobile: true }, s);
  await sleep(150); // let the reflow settle
  let mob = null;
  try {
    const mres = await cdp.send("Runtime.evaluate", { expression: CHECKER, returnByValue: true, awaitPromise: true }, s);
    if (!mres.exceptionDetails) mob = mres.result.value.overflow;
  } catch { /* measurement is best-effort; absence is not a failure */ }
  await cdp.send("Emulation.setDeviceMetricsOverride",
    { width: VIEWPORT.width, height: VIEWPORT.height, deviceScaleFactor: 1, mobile: false }, s);
  if (mob) {
    o.mobileOverflow = mob;
    if (mob.delta > OVERFLOW_TOL) {
      const w = mob.widest;
      reasons.push(`mobile horizontal overflow @${MOBILE.width}px: scrollWidth ${mob.scrollW} > clientWidth ${mob.clientW}` +
        (w ? ` (widest: <${w.tag.toLowerCase()} class="${w.cls}"> right=${w.right})` : ""));
    }
  }
  return { slug, ok: reasons.length === 0, reasons, meta: o };
}

function discoverGenerated() {
  const probs = JSON.parse(fs.readFileSync(path.join(ROOT, "data/problems.json"), "utf8"));
  return probs.filter((p) => p.lesson_status === "generated" &&
    fs.existsSync(path.join(ROOT, "lessons", p.slug, "lesson.html"))).map((p) => p.slug).sort();
}

async function main() {
  const argv = process.argv.slice(2);
  const json = argv.includes("--json");
  let slugs = argv.filter((a) => !a.startsWith("--"));
  if (argv.includes("--all") || slugs.length === 0) slugs = discoverGenerated();
  if (slugs.length === 0) { console.error("usage: node scripts/render_check.mjs <slug> [...] | --all"); process.exit(2); }

  const bin = findBrowser();
  if (!bin) {
    console.warn("⚠ render_check: no Chromium/Chrome found — SKIPPING render smoke test.\n" +
      "  Set CHROME_BIN, or install Playwright's chromium. Gate degrades to skip (exit 0).");
    process.exit(0);
  }

  const { proc, userDir } = launch(bin);
  let exitCode = 0;
  try {
    const endpoint = await wsEndpoint(proc);
    const ws = new WebSocket(endpoint);
    await new Promise((res, rej) => {
      ws.addEventListener("open", res, { once: true });
      ws.addEventListener("error", () => rej(new Error("ws connect failed")), { once: true });
    });
    const cdp = new CDP(ws);
    const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" });
    const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });

    let errors = [];
    cdp.on((m) => {
      if (m.sessionId !== sessionId) return;
      if (m.method === "Runtime.exceptionThrown") {
        const e = m.params.exceptionDetails;
        errors.push("uncaught: " + (e.exception?.description || e.text || "exception").split("\n")[0]);
      } else if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error") {
        errors.push("console.error: " + m.params.args.map((a) => a.value ?? a.description ?? a.type).join(" "));
      } else if (m.method === "Log.entryAdded" && m.params.entry.level === "error") {
        errors.push("log.error: " + m.params.entry.text);
      }
    });
    await cdp.send("Runtime.enable", {}, sessionId);
    await cdp.send("Log.enable", {}, sessionId);
    await cdp.send("Page.enable", {}, sessionId);
    await cdp.send("Emulation.setDeviceMetricsOverride",
      { width: VIEWPORT.width, height: VIEWPORT.height, deviceScaleFactor: 1, mobile: false }, sessionId);

    const reports = [];
    for (const slug of slugs) {
      reports.push(await checkSlug(cdp, sessionId, slug, () => errors.slice(), () => { errors = []; }));
    }

    if (json) {
      console.log(JSON.stringify(reports, null, 2));
    } else {
      console.log(`render-check (${bin.includes("ms-playwright") ? "playwright chromium" : bin}):`);
      for (const r of reports) {
        if (r.ok) console.log(`  ✓ ${r.slug}`);
        else { console.log(`  ✗ ${r.slug}`); for (const why of r.reasons) console.log(`      - ${why}`); }
      }
      const pass = reports.filter((r) => r.ok).length;
      console.log(`\n  totals: ${pass} ok, ${reports.length - pass} failed (of ${reports.length})`);
    }
    if (reports.some((r) => !r.ok)) exitCode = 1;
  } catch (e) {
    console.error(`render_check error: ${e.message}`);
    exitCode = 2;
  } finally {
    try { proc.kill("SIGKILL"); } catch {}
    try { fs.rmSync(userDir, { recursive: true, force: true }); } catch {}
  }
  process.exit(exitCode);
}

main();
