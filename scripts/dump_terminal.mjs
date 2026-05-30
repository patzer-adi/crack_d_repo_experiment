#!/usr/bin/env node
// Introspection helper for the step-(b) retrofit (NOT a gate).
// For each example, run the dry-run oracle and print the example inputs plus
// the terminal step object, so we can see which field already carries the
// answer and what to expose as `result:`. Usage: node dump_terminal.mjs <slug>
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const GENS = ["drGenSteps", "drGen"];

function extractFunction(src, name) {
  const decl = new RegExp(`function\\s+${name}\\s*\\(`).exec(src);
  if (!decl) return null;
  const parenStart = src.indexOf("(", decl.index);
  let depth = 0, i = parenStart;
  for (; i < src.length; i++) {
    if (src[i] === "(") depth++;
    else if (src[i] === ")") { depth--; if (depth === 0) break; }
  }
  const braceStart = src.indexOf("{", i);
  let bdepth = 0;
  for (let j = braceStart; j < src.length; j++) {
    if (src[j] === "{") bdepth++;
    else if (src[j] === "}") { bdepth--; if (bdepth === 0) return src.slice(decl.index, j + 1); }
  }
  return null;
}
function paramNames(fnSource) {
  const m = /function\s+\w+\s*\(([^)]*)\)/.exec(fnSource);
  return m ? m[1].split(",").map(s => s.trim()).filter(Boolean) : [];
}
function extractArrayLiteral(src, name) {
  const decl = new RegExp(`const\\s+${name}\\s*=\\s*\\[`).exec(src);
  if (!decl) return null;
  const start = src.indexOf("[", decl.index);
  let depth = 0;
  for (let j = start; j < src.length; j++) {
    if (src[j] === "[") depth++;
    else if (src[j] === "]") { depth--; if (depth === 0) return src.slice(start, j + 1); }
  }
  return null;
}

const slug = process.argv[2];
const src = fs.readFileSync(path.join(ROOT, "lessons", slug, "lesson.html"), "utf8");
const oracleName = GENS.find(n => extractFunction(src, n));
const fnSrc = extractFunction(src, oracleName);
const exName = /const\s+EX\s*=\s*\[/.test(src) ? "EX" : "EXAMPLES";
const exLit = extractArrayLiteral(src, exName);

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(`${fnSrc}\nthis.__EX=${exLit};\nthis.__gen=${oracleName};`, sandbox, { timeout: 5000 });

const params = paramNames(fnSrc);
const endsInGen = /(?<!Steps)Gen$/.test(oracleName);
const destructures = params.length === 1 && params[0].startsWith("{");

console.log(`slug=${slug} oracle=${oracleName}(${params.join(", ")}) exVar=${exName} n=${sandbox.__EX.length}`);
sandbox.__EX.forEach((ex, i) => {
  let args;
  if (endsInGen || destructures) args = [ex];
  else {
    const matched = params.map(p => ex[p]);
    if (matched.every(v => v !== undefined)) args = matched;
    else { const k = Object.keys(ex).find(k => Array.isArray(ex[k])); args = k ? [ex[k]] : matched; }
  }
  let steps;
  try { steps = sandbox.__gen(...args); }
  catch (e) { console.log(`  [${i}] THREW ${e.message}`); return; }
  const last = steps[steps.length - 1];
  console.log(`  [${i}] input=${JSON.stringify(ex)}`);
  console.log(`       hasAnswer=${"answer" in ex} answer=${JSON.stringify(ex.answer)}`);
  console.log(`       terminal keys: ${Object.keys(last).join(", ")}`);
  // print scalar/short fields of the terminal step to spot the answer-bearing one
  const shortFields = {};
  for (const [k, v] of Object.entries(last)) {
    const s = JSON.stringify(v);
    if (s && s.length <= 80) shortFields[k] = v;
  }
  console.log(`       terminal short fields: ${JSON.stringify(shortFields)}`);
});
