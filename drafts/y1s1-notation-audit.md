# Y1S1 notation audit (Part 3) — method, findings, status

Owner rule being enforced: **every variable/symbol is introduced in prose
before it appears in a formula** (standing directive #3; restated in the Y1S1
quality-pass plan as "err toward more explanation, not less").

Tooling: `drafts/audit_notation.py` (run `python3 drafts/audit_notation.py`,
optionally with course ids). Raw output: `drafts/y1s1-notation-audit.txt`.

## What the tool actually measures

It extracts every math span from a lesson's `lecture`, reduces each to base
quantity symbols (subscripts stripped — `V_C` and `N_A` are `V` and `N`, one
symbol each, not three), and asks whether the surrounding prose ever reads
like a definition of that symbol: an article/copula right after it
(`\( A \) the atomic weight`, `\( \rho \) is the density`), a noun phrase
right before it (`the cell volume \( V_C \)`), or a `where` clause.

**It produces a reading list, not a verdict.** Every hit is judged by hand.
Known limits, all of which produce FALSE POSITIVES, never false negatives:

- A definition with no article is missed — `period \( T \)`, `functions
  \( u, v \)`, `constants \( c \)` all read as undefined to the regex but are
  perfectly well defined in the prose.
- Conventional symbols that need no definition are still flagged: `e` in
  `e^x`, integration dummies `a`/`b`/`x`, the generic exponent `n`.
- A symbol defined in an earlier lesson of the same course is flagged again in
  every later lesson (the tool is per-lesson).

## Correction to the plan's premise

The plan stated that 4 of 6 Y1S1 courses were already clean and only
`materials-1` and `math-1` had real gaps. **That is not what the evidence
shows**, in both directions:

- An earlier version of this check (display-equation-before-inline-mention)
  reported `physics-1`, `computing` and `drawing-cad` as clean with zero hits.
  That was an artefact: **`physics-1` and `computing` contain zero display
  equations** — all their math is inline — so that check structurally could
  not flag them. A clean result there meant "not measured", not "good".
- `statics` was described as clean but carries real hits.
- `materials-1` L3 — a specifically named example — was read in full and is
  **fine**: it states `\[ \rho = nA/(V_C N_A) \]` and immediately names every
  symbol (`\( n \) atoms per cell, \( A \) the atomic weight, ...`). That is
  standard, clear technical writing, not a defect.

The genuine defect pattern is narrower than "symbol used before introduced"
(which mostly catches the normal equation-then-where-clause order). It is
**symbols that are never named anywhere in the lesson**.

## Fixed so far

- **`math-1` L1** — the first equation of the entire curriculum,
  \( P = \rho g Q H \), named none of its five symbols, in a lesson whose
  subject is unit discipline. Now names power, density, gravitational
  acceleration, volumetric flow and head before the units are substituted.
  (4 undefined symbols → 1, and that one is `e` in `e^x`.)
- **`math-1` L7** — `V`, `T` and `Q` first appeared inside the accumulation
  integral \( V = \int_0^T Q(t)\,dt \). Now named in the lead-in sentence.

## Still to do

Hand-review the remaining reading list, course by course, and fix the genuine
never-named cases:

| Course | Raw hits | Notes |
|---|---|---|
| math-1 | ~32 left | L4's `u, v` are false positives (prose says "functions u, v"); check `N` in `P = kN^3` |
| statics | 14 | plan wrongly called this clean |
| materials-1 | 29 | L3 verified fine; rest unread |
| physics-1 | 23 | never actually measured before this pass |
| computing | 18 | many hits are code identifiers inside `\texttt{}`, likely mostly noise |
| drawing-cad | 0 | almost no math; genuinely low risk |

Do this **before** authoring the per-lesson `recap` fields and before the
Arabic translation, so neither is written twice.
