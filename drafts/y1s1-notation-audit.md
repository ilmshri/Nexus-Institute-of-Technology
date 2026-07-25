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

## Fixed (all read in full context before editing)

**`math-1`** — L1: the first equation of the entire curriculum,
\( P = \rho g Q H \), named none of its five symbols, in the lesson whose
subject is unit discipline; now names power, density, gravitational
acceleration, volumetric flow and head. L4: the fan law \( P = kN^3 \) now
names shaft power, rotational speed and the machine constant. L7: `V`, `T`,
`Q` named before the accumulation integral. L9: `\rho`, `g`, `A` named in the
layer-weight expression. L10: `V/Q` given as tank volume over volumetric flow.

**`statics`** — L8: `w(x)`, the distributed load intensity, appeared cold in
the shear/moment differential relations while `N`, `V` and `M` right above it
were all properly named. Now names `w` (a force per unit length, N/m — the
distinction that actually trips students) and `x`.

**`materials-1`** — the course with the densest real gaps, matching the plan's
description. L1: `\sigma = F/A` in the course opener named nothing. L2:
Pauling's relation used `X_A`, `X_B` with no mention of electronegativity.
L5: the vacancy relation's `N_v`, `N`, `Q_v`, `k`, `T`. L6: Fick's laws —
`C`, `x`, `t` unnamed (`J` and `D` were fine). L7: `F`, `A_0`, `\Delta L`,
`L_0` behind the named stress and strain. L9: Hall–Petch named none of its
four symbols. L10: `T_R`, `T_m`. L11: the critical-radius symbols and
Chvorinov's mould constant `B`.

**`physics-1`** — L6: `\theta` and `d` in \( W = Fd\cos\theta \). L11: `L` is
the pendulum length here, having been angular momentum in L10 — the collision
is now called out explicitly in the text.

## Judged and deliberately NOT changed

- **`materials-1` L3** and **`physics-1` L4** read as violations to the tool
  but are good writing: both state the equation and name every symbol in the
  very next clause ("the net force … produces acceleration … scaled inversely
  by the mass"). Editing them would make the prose worse.
- **`computing`** (18 raw hits) is essentially all noise. Its "symbols" are
  code identifiers inside `\texttt{}` (`abs(a - b)`, `flow_m3h`) and the
  generic table coordinates of L9's interpolation lesson, which the prose
  introduces as "two table rows \( (x_1,y_1) \) and \( (x_2,y_2) \)".
- Conventional symbols left alone throughout: `e` in `e^x`, integration
  dummies and limits (`a`, `b`, `x`), the generic exponent `n`.

## Status

Raw hits 118 → 89, but **the raw number is a poor progress metric** and should
not be read as "89 defects left": the counter cannot see a definition written
without an article, so several of the fixes above still show up as hits (e.g.
"shaft power \( P \) rising with…"). What matters is that every hit in every
Y1S1 course has now been read in context and either fixed or judged sound.

Remaining genuinely-unread surface: none in Y1S1. The lower-value tail
(cross-lesson symbols defined in an earlier lesson of the same course, e.g.
`d` for grain diameter reused in materials-1 L10 from L9) was judged
acceptable — the courses are taken in order.

Done **before** the per-lesson `recap` fields and before the Arabic
translation, so neither is written against text that was about to change.
