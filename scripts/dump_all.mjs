#!/usr/bin/env node
// Dev-only: for every lesson, print its example array + each terminal step's
// short fields, so retrofits can be authored with full info. Writes to stdout.
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

function extractFunction(src, name) {
  const decl = new RegExp(`function\\s+${name}\\s*\\(`).exec(src);
  if (!decl) return null;
  const p0 = src.indexOf("(", decl.index);
  let d = 0, i = p0;
  for (; i < src.length; i++) { if (src[i] === "(") d++; else if (src[i] === ")") { d--; if (!d) break; } }
  const b0 = src.indexOf("{", i);
  let bd = 0;
  for (let j = b0; j < src.length; j++) { if (src[j] === "{") bd++; else if (src[j] === "}") { bd--; if (!bd) return src.slice(decl.index, j + 1); } }
  return null;
}
function paramNames(s) { const m = /function\s+\w+\s*\(([^)]*)\)/.exec(s); return m ? m[1].split(",").map(x => x.trim()).filter(Boolean) : []; }
function arrLit(src, name) {
  const d = new RegExp(`const\\s+${name}\\s*=\\s*\\[`).exec(src);
  if (!d) return null;
  const s = src.indexOf("[", d.index);
  let dep = 0;
  for (let j = s; j < src.length; j++) { if (src[j] === "[") dep++; else if (src[j] === "]") { dep--; if (!dep) return src.slice(s, j + 1); } }
  return null;
}

const slugs = fs.readdirSync(path.join(ROOT, "lessons"))
  .filter(d => fs.existsSync(path.join(ROOT, "lessons", d, "lesson.html")))
  .sort();

for (const slug of slugs) {
  const src = fs.readFileSync(path.join(ROOT, "lessons", slug, "lesson.html"), "utf8");
  const oracleName = extractFunction(src, "drGenSteps") ? "drGenSteps" : extractFunction(src, "drGen") ? "drGen" : null;
  const fnSrc = oracleName && extractFunction(src, oracleName);
  const impure = fnSrc && /\b(document|getElementById|querySelector|window)\b/.test(fnSrc);
  const exName = /const\s+EX\s*=\s*\[/.test(src) ? "EX" : /const\s+EXAMPLES\s*=\s*\[/.test(src) ? "EXAMPLES" : null;
  const exLit = exName && arrLit(src, exName);
  console.log(`\n#### ${slug}  oracle=${oracleName}${fnSrc ? "(" + paramNames(fnSrc).join(", ") + ")" : ""} exVar=${exName} impure=${!!impure}`);
  if (!oracleName) { console.log("   (no oracle)"); continue; }
  if (impure) { console.log("   (oracle impure — needs pure/render split first)"); continue; }
  if (!exLit) { console.log("   (no example array — must author EX from scratch)"); continue; }
  let sandbox = {};
  try {
    vm.createContext(sandbox);
    vm.runInContext(`${fnSrc}\nthis.__EX=${exLit};\nthis.__gen=${oracleName};`, sandbox, { timeout: 5000 });
  } catch (e) { console.log("   sandbox err: " + e.message); continue; }
  const params = paramNames(fnSrc);
  const whole = params.length === 1 && (params[0].startsWith("{") || params[0] === "ex" || params[0] === "e");
  sandbox.__EX.forEach((ex, i) => {
    let args;
    if (whole) args = [ex];
    else {
      const m = params.map(p => ex[p]);
      if (m.every(v => v !== undefined)) args = m;
      else { const k = Object.keys(ex).find(k => k !== "answer" && Array.isArray(ex[k])); args = k ? [ex[k]] : m; }
    }
    let steps;
    try { steps = sandbox.__gen(...args); } catch (e) { console.log(`   [${i}] THREW ${e.message}`); return; }
    const last = steps[steps.length - 1];
    const hasResult = last && "result" in last;
    const hasAnswer = "answer" in ex;
    const short = {};
    for (const [k, v] of Object.entries(last || {})) { const s = JSON.stringify(v); if (s && s.length <= 60) short[k] = v; }
    console.log(`   [${i}] ex=${JSON.stringify(ex).slice(0,90)}  hasAnswer=${hasAnswer} hasResult=${hasResult}`);
    console.log(`        terminal: ${JSON.stringify(short).slice(0,200)}`);
  });
}
