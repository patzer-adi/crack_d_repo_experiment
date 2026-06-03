# Lesson Plan: {{NAME}} (LC #{{LC_NUM}})

## Metadata
- **Slug:** `{{SLUG}}`
- **LC #:** {{LC_NUM}}
- **Difficulty:** {{DIFFICULTY}}               <!-- Easy | Medium | Hard -->
- **Topic:** {{TOPIC}}                          <!-- from problems.json "section" field -->
- **Tier:** {{TIER}}                            <!-- 1 = primer | 2 = standard | 3 = hard -->
- **Twist:** {{TWIST}}                          <!-- verbatim from problems.json "twist" field -->
- **Archetype:** {{ARCHETYPE}}                  <!-- see design/archetypes.md -->

---

## §1 — The Concept

### Plain-English explanation
<!-- One paragraph. No code syntax. Explain what the algorithm does the way you
     would explain it to a smart friend who isn't a programmer.                  -->
[FILL]

### Key insight (one sentence)
<!-- The single sentence from which the algorithm is derivable.
     E.g. "Binary search works because a sorted array lets you eliminate half
     the candidates with a single comparison."                                    -->
[FILL]

### Concept visual description
<!-- Describe the static or lightly-animated visual that will illustrate the
     insight. Be specific about what is shown and labelled.
     E.g. "A sorted array [1,3,5,7,9] with lo=0, hi=4, mid=2 markers;
     target=7 is highlighted; left half is greyed out to show elimination."       -->
[FILL]

### Kernel (infobox text)
<!-- Dense paragraph for the .infobox.success "The kernel" box.
     Must be algorithm-derivable from this text alone.                            -->
[FILL]

---

## §2 — Data Structure Visual

### Primary DS
<!-- Name the data structure: sorted array, deque, hash map, prefix array, etc.  -->
[FILL]

### Invariants to show
<!-- What invariants does this DS maintain? What guarantees does it provide?
     E.g. For a monotonic deque: "elements are always in decreasing order;
     back element is always the newest candidate; front element is always
     the current window maximum."                                                  -->
[FILL]

### Visual layout
<!-- Describe the static diagram. What cells/nodes are shown? What labels?
     What colour coding?                                                           -->
[FILL]

---

## §3 — Algorithm in Plain English

<!-- 4–6 numbered steps. Bold verb at the start of each.
     These are the exact words the reader should say in an interview.              -->

1. **[Verb]** [step]
2. **[Verb]** [step]
3. **[Verb]** [step]
4. **[Verb]** [step]
5. **[Verb]** [step] (optional)
6. **Return** [what]

---

## §4 — Interactive Animation

### Preset examples
<!-- Choose 3 examples that together cover: typical, edge, tricky.
     For each: state the input, the expected output, and what the example teaches. -->

| # | Input | Expected | Teaches |
|---|-------|----------|---------|
| 1 | [FILL] | [FILL] | typical case |
| 2 | [FILL] | [FILL] | edge / no-match / empty |
| 3 | [FILL] | [FILL] | tricky: duplicates / wrap / overflow |

### Custom input spec
<!-- What field(s) does the user type? Comma-separated array? Also a target k?
     What validation is needed?                                                    -->
[FILL]

### Visual conventions for this problem
<!-- Map the four standard colours to this problem's concepts.
     E.g. for Binary Search:
       blue  = current search range (lo..hi)
       green = found element / match
       amber = mid pointer
       red   = eliminated half (flash before grey)                                 -->

| Colour | Used for |
|--------|----------|
| Blue (info)    | [FILL] |
| Green (success)| [FILL] |
| Amber (warn)   | [FILL] |
| Red (danger)   | [FILL] |

### Step narration examples
<!-- Write 3 representative step narrations to test that the prose is informative.
     Format: "Step N: [what happened]. [Why the pointer/window moved]."            -->

- Step [N]: [FILL]
- Step [N]: [FILL]
- Step [N]: [FILL]

### Formula row fields
<!-- List every field that appears in the formula row and its label.
     E.g. lo, hi, mid, target, nums[mid], decision                                -->
[FILL]

---

## §5 — Code (C++ only)

### Algorithm to implement
<!-- Which variant / approach? E.g. "iterative binary search with closed interval
     [lo, hi] — lo <= hi loop condition, mid = lo + (hi-lo)/2 to avoid overflow"  -->
[FILL]

### Brute force (for comparison infobox)
<!-- What naive approach is this optimising over?
     State the time complexity of the brute force.                                 -->
[FILL]

### Complexity
- **Time:** O([FILL]) — [one sentence]
- **Space:** O([FILL]) — [one sentence]

---

## §6 — Code Walkthrough

### Variable cards
<!-- List every variable that will have a card, and the line number at which
     it first becomes visible (i.e. is first assigned).                           -->

| Variable | First visible at line | Card label |
|----------|-----------------------|------------|
| [FILL]   | [FILL]                | [FILL]     |

### Array strip colour scheme
<!-- How does the array strip differ from the animation in §4?
     The walkthrough strip shows the *code's* view of state, not the high-level
     algorithm view. Map colours to the specific code variables.                   -->
[FILL]

### Red-flash elements
<!-- Which elements flash red and when?
     E.g. "When lo > hi, the eliminated side cells flash red for one step."        -->
[FILL]

---

## §7 — Complexity

| | Big-O | Justification |
|-|-------|---------------|
| **Time** | O([FILL]) | [FILL] |
| **Space** | O([FILL]) | [FILL] |

---

## Corner cases
<!-- 4–5 cases. These are used internally to verify the algorithm and can be
     referenced in the lesson if a "gotcha" section is added later.                -->

| Case | Input | Expected | Why tricky |
|------|-------|----------|------------|
| Empty | [] | [FILL] | [FILL] |
| Single element | [[FILL]] | [FILL] | [FILL] |
| All same | [FILL] | [FILL] | [FILL] |
| Not found / no match | [FILL] | [FILL] | [FILL] |
| [Problem-specific] | [FILL] | [FILL] | [FILL] |

---

## Python verification trace
<!-- Run this before writing any HTML. Print every variable at every step.
     Verify output matches expected for all 3 preset examples and corner cases.    -->

```python
# [FILL — paste trace output here after running]
```

---

## Related problems (for future "Take home" section)
<!-- 2–4 problems from problems.json that use the same pattern.
     For each, note what differs.                                                  -->

- LC [FILL] ([FILL]) — same skeleton, [what differs]
- LC [FILL] ([FILL]) — [what differs]

---

## Output file
`lessons/{{SLUG}}/lesson.html` — self-contained, offline-capable, no CDN dependencies.

## Quality checklist
- [ ] Python trace run and verified for all 3 examples + corner cases
- [ ] §4 animation has 3 presets + custom input field
- [ ] Keyboard shortcuts work (← → Space R)
- [ ] §6 all variable cards start dimmed
- [ ] Hard-reset fires on example switch in both §4 and §6
- [ ] Code uses explicit braces on every block
- [ ] No CDN links, no external fonts, no external scripts
- [ ] Complexity matches trace output
