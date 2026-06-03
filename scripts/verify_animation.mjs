#!/usr/bin/env node
// Verify a lesson's animation step-generators compute the CORRECT answer.
//
// Usage:
//   node scripts/verify_animation.mjs <slug> [--json]
//
// Exit codes:
//   0 — every example with an oracle was verified and matched
//   1 — a mismatch (animation computes the wrong answer) OR a lesson that
//       claims to be verifiable has no usable oracle (see --strict default)
//
// Why this exists
// ---------------
// lint_lesson.py checks that the animation has the right SHAPE (controls,
// ids, a siGenSteps function). It cannot tell whether the animation computes
// the right NUMBER. This script runs each pure *GenSteps generator headlessly
// over the lesson's own declared examples and asserts that the terminal step's
// `.result` equals the example's declared `.answer`. It is the correctness gate
// that makes dropping the manual approval step safe.
//
// Contract a lesson must satisfy to be auto-verifiable
// ----------------------------------------------------
//   1. An example array `const EX = [ { <input fields>, answer: <expected> }, ... ];`
//   2. Each *GenSteps(...) returns an array whose LAST element has a `result`
//      field equal to the algorithm's answer for that input.
//   3. *GenSteps must be PURE — no document / getElementById / window refs.
//      (Rendering belongs in *Render, not in the generator.)
//
// A lesson that does not meet the contract is reported UNVERIFIABLE, which the
// gate treats as a failure for newly-generated lessons. Existing lessons that
// predate the contract will show up as UNVERIFIABLE until retrofitted with the
// two fields (a ~2-line change each).

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

// Two authoring conventions coexist in the corpus:
//   A (newer): function drGenSteps(arg, ...) driven by `const EX = [...]`
//   B (older): function drGen(ex)            driven by `const EXAMPLES = [...]`
// We extract the generators of both so the oracle can be found either way.
const GEN_NAMES = [
  "siGenSteps", "drGenSteps", "cvGenSteps", "bfGenSteps",
  "siGen", "drGen", "cvGen", "bfGen",
];

// ── source extraction ──────────────────────────────────────────────────────

// Return the source of `function <name>(...) { ... }` by brace-matching from
// the declaration. Returns null if not found.
function extractFunction(src, name) {
  const decl = new RegExp(`function\\s+${name}\\s*\\(`).exec(src);
  if (!decl) return null;
  const parenStart = src.indexOf("(", decl.index);
  // find the opening brace of the body (first { after the param list)
  let depth = 0,
    i = parenStart;
  for (; i < src.length; i++) {
    if (src[i] === "(") depth++;
    else if (src[i] === ")") {
      depth--;
      if (depth === 0) break;
    }
  }
  const braceStart = src.indexOf("{", i);
  if (braceStart < 0) return null;
  let bdepth = 0;
  for (let j = braceStart; j < src.length; j++) {
    const c = src[j];
    if (c === "{") bdepth++;
    else if (c === "}") {
      bdepth--;
      if (bdepth === 0) return src.slice(decl.index, j + 1);
    }
  }
  return null;
}

// Blank out string-literal contents, template literals, and comments so a
// textual code scan (e.g. the DOM-purity check) never matches a keyword that
// only appears in prose. Real code like `window.foo` survives; the word
// "window" inside a narration string does not. This keeps the purity heuristic
// honest without ever letting a wrong *answer* through (answers are checked
// separately by deep-equality on the terminal step's result).
function stripStringsAndComments(code) {
  return code
    .replace(/`(?:\\[\s\S]|\$\{[^}]*\}|[^\\`])*`/g, "``")
    .replace(/'(?:\\.|[^'\\])*'/g, "''")
    .replace(/"(?:\\.|[^"\\])*"/g, '""')
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/\/\/[^\n]*/g, "");
}

// Parse the parameter names of `function name(a, b)` from its source.
// Split only at brace-depth 0 so a destructured param like `{s1, s2}` stays a
// SINGLE param (a naive comma split would shatter it into `{s1` / `s2}` and
// defeat whole-object detection below).
function paramNames(fnSource) {
  const m = /function\s+\w+\s*\(([^)]*)\)/.exec(fnSource);
  if (!m) return [];
  const out = [];
  let depth = 0,
    cur = "";
  for (const c of m[1]) {
    if (c === "{" || c === "[") depth++;
    else if (c === "}" || c === "]") depth--;
    if (c === "," && depth === 0) {
      out.push(cur.trim());
      cur = "";
    } else cur += c;
  }
  out.push(cur.trim());
  return out.filter(Boolean);
}

// Extract `const EX = [ ... ];` (array literal) source by brace-matching.
function extractArrayLiteral(src, name) {
  const decl = new RegExp(`const\\s+${name}\\s*=\\s*\\[`).exec(src);
  if (!decl) return null;
  const start = src.indexOf("[", decl.index);
  let depth = 0;
  for (let j = start; j < src.length; j++) {
    const c = src[j];
    if (c === "[") depth++;
    else if (c === "]") {
      depth--;
      if (depth === 0) return src.slice(start, j + 1);
    }
  }
  return null;
}

// ── evaluation ─────────────────────────────────────────────────────────────

function deepEqual(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}

// Run one generator over one example. Returns {ok, computed, expected, reason}.
function runCase(ctx, genName, fnSource, ex) {
  const params = paramNames(fnSource);
  // Convention B generators (drGen, siGen, …) take the WHOLE example object,
  // e.g. drGen(ex) reads ex.nums / ex.target itself. Convention A generators
  // (drGenSteps, …) take unpacked arguments mapped from the example's keys.
  // Decide how to call the generator from its PARAMETER shape, not its name —
  // both drGen and drGenSteps appear with either unpacked args or a single
  // whole-object arg in the corpus:
  //   • single param named `ex`/`e`, or a destructured `{a,b}` → pass the whole
  //     example object   (drGen(ex), drGenSteps({nums}), drGen({n,reqs}))
  //   • params that match example keys                        → unpack them
  //     (drGen(nums), drGen(h), drGenSteps(coins, amount))
  //   • single unmatched param + one array field              → pass that array
  const wholeObject =
    params.length === 1 &&
    (params[0].startsWith("{") || params[0] === "ex" || params[0] === "e");
  let args;
  if (wholeObject) {
    args = [ex];
  } else {
    const matched = params.map((p) => (p in ex ? ex[p] : undefined));
    if (matched.every((v) => v !== undefined) && params.length > 0) {
      args = matched;
    } else {
      const inputKeys = Object.keys(ex).filter((k) => k !== "answer" && k !== "label");
      const firstArrayKey = inputKeys.find((k) => Array.isArray(ex[k]));
      if (params.length === 1 && firstArrayKey) args = [ex[firstArrayKey]];
      // Positional fallback: param names don't match keys (e.g. drGen(Aorig,
      // Borig) over {A, B}); if the count of input fields equals the param
      // count, map them in declaration order.
      else if (inputKeys.length === params.length) args = inputKeys.map((k) => ex[k]);
      else if (matched.some((v) => v !== undefined)) args = matched.map((v) => v ?? null);
      else return { ok: false, reason: `cannot map args ${JSON.stringify(params)} to example keys ${JSON.stringify(Object.keys(ex))}` };
    }
  }

  let steps;
  try {
    steps = ctx[genName](...args);
  } catch (e) {
    return { ok: false, reason: `${genName} threw: ${e.message}` };
  }
  if (!Array.isArray(steps) || steps.length === 0)
    return { ok: false, reason: `${genName} returned no steps` };

  const last = steps[steps.length - 1];
  if (last == null || !("result" in last))
    return { ok: false, reason: `final step of ${genName} has no .result field` };

  if (!("answer" in ex))
    return { ok: false, reason: `example has no .answer field` };

  const ok = deepEqual(last.result, ex.answer);
  return { ok, computed: last.result, expected: ex.answer };
}

function verify(slug) {
  const htmlPath = path.join(ROOT, "lessons", slug, "lesson.html");
  const report = { slug, cases: [], errors: [], skipped: [] };
  if (!fs.existsSync(htmlPath)) {
    report.errors.push(`lesson.html not found at ${htmlPath}`);
    return report;
  }
  const src = fs.readFileSync(htmlPath, "utf8");

  // examples: prefer EX (convention A); fall back to EXAMPLES (convention B).
  const exName = new RegExp("const\\s+EX\\s*=\\s*\\[").test(src) ? "EX" : "EXAMPLES";
  const exLit = extractArrayLiteral(src, exName);
  if (!exLit) {
    report.errors.push("no `const EX = [...]` or `const EXAMPLES = [...]` example array found");
    return report;
  }

  const gens = {};
  for (const name of GEN_NAMES) {
    const fnSrc = extractFunction(src, name);
    if (fnSrc) {
      // scan code only — strings/comments are prose and must not trip the check
      if (/\b(document|getElementById|querySelector|window)\b/.test(stripStringsAndComments(fnSrc)))
        report.errors.push(`${name} is impure (touches the DOM) — cannot verify headlessly`);
      else gens[name] = fnSrc;
    }
  }
  if (Object.keys(gens).length === 0) {
    report.errors.push("no pure *GenSteps generator found");
    return report;
  }

  // Build a sandbox: define the generators + EX, expose them.
  const sandbox = {};
  vm.createContext(sandbox);
  const bootstrap =
    Object.values(gens).join("\n\n") +
    `\nthis.__EX = ${exLit};\n` +
    GEN_NAMES.filter((n) => gens[n])
      .map((n) => `this.${n} = ${n};`)
      .join("\n");
  try {
    vm.runInContext(bootstrap, sandbox, { timeout: 5000 });
  } catch (e) {
    report.errors.push(`sandbox eval failed: ${e.message}`);
    return report;
  }

  const examples = sandbox.__EX;

  // drGenSteps is the designated oracle (see sec7_dry_run.md): it is the only
  // generator wired to EX (the answer-bearing examples). si/cv/bf animate
  // pedagogical inputs (SI_NUMS, BF_EX) that carry no answer AND are not built
  // to run on EX shapes — running them here risks infinite loops, so we never
  // do. The contract requires drGenSteps to exist and expose a terminal result.
  const oracle = gens["drGenSteps"] ? "drGenSteps" : gens["drGen"] ? "drGen" : null;
  if (!oracle) {
    report.errors.push(
      "no pure drGenSteps / drGen generator found — one is the required correctness oracle"
    );
    for (const n of Object.keys(gens)) report.skipped.push({ gen: n, reason: "not the oracle" });
    return report;
  }
  for (const n of Object.keys(gens)) {
    if (n !== oracle) report.skipped.push({ gen: n, reason: "not the oracle (pedagogical input)" });
  }

  for (let i = 0; i < examples.length; i++) {
    const r = runCase(sandbox, oracle, gens[oracle], examples[i]);
    report.cases.push({
      gen: oracle,
      example: examples[i].label ?? `EX[${i}]`,
      ...r,
    });
  }
  report.independence = runIndependence(slug, examples);
  return report;
}

// PLAN-019 G4: cross-check the answers against an INDEPENDENT brute force
// committed at lessons/<slug>/verify.py. The oracle check above only proves the
// animation agrees with the EX answers; if those answers were copied from the
// generator that is a tautology. verify.py recomputes them a different way — we
// feed it the EX inputs (JSON on stdin) and compare its JSON output to the
// declared answers. Enforced ON PRESENCE: a lesson without verify.py is reported
// (backfill pending) but not failed, so the pre-G4 corpus keeps passing.
function runIndependence(slug, examples) {
  const py = path.join(ROOT, "lessons", slug, "verify.py");
  if (!fs.existsSync(py)) return { status: "absent" };
  const inputs = examples.map(({ answer, label, ...rest }) => rest);
  const res = spawnSync("python3", [py], { input: JSON.stringify(inputs), encoding: "utf8", timeout: 20000 });
  if (res.status !== 0)
    return { status: "error", reason: (res.stderr || res.error?.message || "non-zero exit").trim().split("\n").slice(-1)[0] };
  let computed;
  try { computed = JSON.parse(res.stdout); }
  catch { return { status: "error", reason: "verify.py stdout is not JSON" }; }
  if (!Array.isArray(computed) || computed.length !== examples.length)
    return { status: "error", reason: `verify.py returned ${Array.isArray(computed) ? computed.length : "non-array"} answers for ${examples.length} examples` };
  const cases = examples.map((e, i) => ({
    label: e.label ?? `EX[${i}]`,
    ok: JSON.stringify(computed[i]) === JSON.stringify(e.answer),
    computed: computed[i], expected: e.answer,
  }));
  return { status: "checked", cases };
}

// ── output ─────────────────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const json = args.includes("--json");
  const slug = args.find((a) => !a.startsWith("--"));
  if (!slug) {
    console.error("usage: node scripts/verify_animation.mjs <slug> [--json]");
    process.exit(2);
  }

  const report = verify(slug);
  const verifiable = report.cases.filter((c) => "computed" in c || c.ok === false && c.expected !== undefined);
  const matched = report.cases.filter((c) => c.ok === true);
  const mismatched = report.cases.filter((c) => c.ok === false && "computed" in c);
  const unusable = report.cases.filter((c) => !("computed" in c) && c.ok === false);

  if (json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(`verify-animation ${report.slug}:`);
    for (const e of report.errors) console.log(`  ✗ ${e}`);
    for (const s of report.skipped) console.log(`  · skip ${s.gen} (not an oracle: ${s.reason})`);
    for (const c of report.cases) {
      if (c.ok === true)
        console.log(`  ✓ ${c.gen}  ${c.example}  → ${JSON.stringify(c.computed)}`);
      else if ("computed" in c)
        console.log(
          `  ✗ ${c.gen}  ${c.example}  computed ${JSON.stringify(c.computed)} ≠ expected ${JSON.stringify(c.expected)}`
        );
      else console.log(`  ⚠ ${c.gen}  ${c.example}  UNVERIFIABLE — ${c.reason}`);
    }
    const ind = report.independence || { status: "absent" };
    if (ind.status === "absent")
      console.log("  · independent reference: none — add lessons/" + report.slug + "/verify.py (PLAN-019 G4)");
    else if (ind.status === "error")
      console.log(`  ✗ independent reference (verify.py): ${ind.reason}`);
    else
      for (const c of ind.cases)
        console.log(`  ${c.ok ? "✓" : "✗"} verify.py  ${c.label}  → ${JSON.stringify(c.computed)}` +
          (c.ok ? "" : ` ≠ declared ${JSON.stringify(c.expected)}`));
    console.log("");
    console.log(
      `  totals: ${matched.length} verified, ${mismatched.length} WRONG, ${unusable.length} unverifiable`
    );
  }

  // Gate semantics: fail on any wrong answer. Unverifiable / no-oracle is a
  // failure too (a lesson with no checkable oracle cannot be auto-approved),
  // EXCEPT when there were structural errors that already make it clear the
  // lesson predates the contract — those still exit 1 so the pipeline stops.
  const ind = report.independence || { status: "absent" };
  const indFail = ind.status === "error" || (ind.status === "checked" && ind.cases.some((c) => !c.ok));
  if (mismatched.length > 0) process.exit(1);
  if (matched.length === 0) process.exit(1); // nothing could be verified
  if (indFail) process.exit(1); // independent reference present but disagrees / errored
  process.exit(0);
}

main();
