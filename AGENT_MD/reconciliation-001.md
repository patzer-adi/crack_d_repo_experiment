# Reconciliation Report — spec.md ↔ current_state_report.md ↔ Actual Implementation

**Report ID:** RECON-001
**Date:** YYYY-MM-DD
**Scope:** Full cross-verification of `spec.md`, `plan/current_state_report.md`, and the live codebase
**Purpose:** Identify all gaps between documentation and reality, then produce a prioritised action plan

---

## Executive Summary

<!-- One paragraph: how well do the docs match reality? What are the biggest surprises? -->

_[Summarise the overall alignment. Call out the most critical discrepancies.]_

### Documents vs Reality — Key Discrepancies Found

| Area | spec.md Says | current_state_report.md Says | Actual Code |
|---|---|---|---|
| _Component A_ | _..._ | _..._ | _..._ |
| _Component B_ | _..._ | _..._ | _..._ |

---

## Priority 1 — 🔴 CRITICAL (Do Immediately)

<!-- Items that block all other work: security issues, data loss risks, broken deployments. -->

### 1.1 [Issue Title]

**Gap:** _[Describe what the docs say vs. what the code actually does.]_

**Actions:**
1. _Step 1_
2. _Step 2_

**Files to modify:**
- _`path/to/file.py`_

**Verification:** _[How to confirm the fix.]_

---

## Priority 2 — 🟠 HIGH (Architectural Alignment)

<!-- Items where architecture has diverged from spec. Decisions needed. -->

### 2.1 Update spec.md to Reflect Reality

**Gap:** _[What's out of date?]_

**Actions:**
1. _Update section X of spec.md_
2. _Update current_state_report.md_

### 2.2 Architectural Decision: [Decision Title]

**Gap:** _[Describe the fork between spec and implementation.]_

**Options:**

**Option A: [Endorse current approach]**
1. _Update docs to match implementation_
2. _Document trade-offs_

**Option B: [Migrate to spec's approach]**
1. _Implementation steps..._

**Decision required from project lead before proceeding.**

---

## Priority 3 — 🟡 MEDIUM (Functional Gaps)

<!-- Missing features, incomplete implementations, wrong defaults. -->

### 3.1 [Gap Title]

**Gap:** _[Description]_
**Actions:** _[Steps]_
**Files:** _[Affected files]_

---

## Priority 4 — 🟢 LOW (Documentation & Cleanup)

<!-- Stale docs, minor inconsistencies, nice-to-haves. -->

### 4.1 [Item Title]

**Gap:** _[Description]_
**Actions:** _[Steps]_

---

## Action Plan Summary

| # | Priority | Action | Est. Effort |
|---|---|---|---|
| 1.1 | 🔴 Critical | _..._ | _..._ |
| 2.1 | 🟠 High | _..._ | _..._ |
| 3.1 | 🟡 Medium | _..._ | _..._ |
| 4.1 | 🟢 Low | _..._ | _..._ |
