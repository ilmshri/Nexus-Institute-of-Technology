# FIGURES — pictorial figure spec (design side)

Owner directive 2026-08-02 (figure split, recorded in CLAUDE.md shared
contract): COMPUTED technical diagrams (plots, data-driven FBDs, cycles) are
CONTENT-side, authored via drafts/lessonlib.py. PICTORIAL/ILLUSTRATIVE figures
are DESIGN-side, drawn original after studying correct conventions from real
textbooks and official lecture notes. This file is the binding spec for the
design-side half. The library is design-previews/tools/figlib.py; the exemplar
pair lives beside this file.

## Studied sources (2026-08-03, live)

Conventions below were extracted by studying — never copying or tracing —
these public sources in the browser:

1. **NASA GRC, Beginner's Guide to Aeronautics — "Newton's Laws of Motion"**
   (secondlaw figure). Pictorial object shown at two instants with state
   labels attached (t₀X₀/V₀m₀ → t₁X₁/V₁m₁); one bold, filled, labeled force
   arrow on the line of action; the word-equation stated before the symbolic
   forms; every symbol used in the figure defined in an in-figure legend;
   vector caveat carried on the figure itself.
2. **NASA GRC, Beginner's Guide — "Four Forces on an Airplane"** (forces
   figure). Force arrows anchored at their physical points of application
   (lift at centre of pressure, weight at CG, thrust on the engine line, drag
   opposite motion); plain-word labels sit immediately beside each arrowhead;
   one consistent arrow style throughout.
3. **MIT OCW 8.01SC Classical Mechanics (Fall 2016), Week 2, PS 2.1 figure**
   (week2ps1.svg). Restrained grayscale line-art: pale fills, thin ink
   outlines, zero decoration. Physical situation drawn pictorially (incline
   triangle, block labeled *m*, spring zigzag, hatched anchor); speed-lines
   as the motion cue; gravity arrow *g* at the panel edge; free unit-vector
   arrow (î with hat) giving the coordinate direction; angle θ marked with an
   arc at the base; two side-by-side panels comparing two states, each with a
   short serif title.

Textbook norms assumed alongside (Hibbeler/Shigley register): the FBD isolates
the body — supports removed and replaced by their reactions; forces drawn from
the point of application; axes shown; angles marked with arcs, never bare
numbers floating.

## The pairing rule (owner-ratified)

A pictorial figure is a PAIR: the physical sketch and its abstraction
(free-body diagram, cycle, mechanism skeleton) presented together, sketch
inline-start, abstraction inline-end. **Neither session ships half a pair.**
One combined SVG carrying both panels is the required form — it keeps the
halves inseparable in every layout and in print.

## Anatomy

Sketch panel (left):
- The physical situation drawn pictorially: machine surfaces as pale filled
  shapes (`--sunken` fill, `--ink` outline), ground/anchors hatched.
- The body of interest carries its symbol (*m*, *W*…) ON the body.
- Motion cue: 2-3 short speed-lines trailing the body, or a curved arrow for
  rotation. Gravity arrow at the panel edge when weight matters.
- The governing angle marked with an arc and symbol at the real geometry.

Abstraction panel (right):
- The body isolated (simple outline at the same tilt), every contact replaced
  by its force arrow drawn FROM the point of application.
- Arrows: single consistent style, `--accent` fill for applied/reaction
  forces, `--bad` reserved for resultants when contrast is required.
- Axes: short unit-vector arrows (with hats) in a free corner, tilted with
  the problem's natural frame.
- The same angle symbol re-marked where it enters the decomposition.
- Every symbol that appears must be readable in the run-line, caption, or an
  in-figure legend — no orphan symbols.

Caption (HTML, outside the SVG): one sentence naming the situation and the
abstraction, e.g. "A crate held on a rough incline — and the same crate as a
free-body diagram." Symbols italicised with <i>.

## Size and fit (gate-enforced)

- A figure block may never exceed HALF an A4 content page; the fit gate
  enforces ~45% of the 252mm print zone (428px of 952px at CSS 96dpi).
- Canonical viewBox: **1280×620** for the pair (two ~600-wide panels + gap).
  Rendered at content width (673px print) that is ≈ 326px tall ≈ 34% of the
  zone — comfortable margin under the 45% ceiling with caption included.
- Markup convention (renderer contract): the pair is emitted as
  `<figure class="rev-fig"><svg …>…</svg><figcaption>…</figcaption></figure>`
  inside `.rev-body`. qa_revision_fit.py measures every `figure.rev-fig`
  per block and fails any figure taller than 45% of the zone.

## Style rules

- Flat vectors only. Existing palette tokens only: ink `#20325A`, soft
  `#44506B`, muted `#6E7688`, line `#DBD7CF`, pale fill `#F6F4F1`, accent
  `#2D5397`, gold `#CBA85F` (highlights/angle arcs), bad `#B3382C`
  (resultants only). Backgrounds stay paper — never dark.
- Strokes: 2px bodies, 1.5px construction, arrows 2.5px shafts with filled
  triangular heads (single marker style per figure).
- Type inside SVG: serif italic for symbols (matches MathJax's register),
  11-13px; sans 10px small-caps for panel titles. No mid-word hyphen wraps.
- Labels collision-free — figlib's `check()` asserts pairwise label
  clearance and viewBox containment at authoring time; run it before every
  commit (same discipline as lessonlib on the content side).
- NOTHING copied or traced from any source, ever. Conventions yes, artwork no.

## Workflow

1. Author the pair as a small Python script using figlib (geometry computed,
   not eyeballed — trig for every arrow and arc).
2. `python3 design-previews/tools/figlib.py --selftest`, then run the
   authoring script: it asserts collisions/containment and writes the SVG.
3. Preview in the browser at 673px width (print) and 320px (mobile).
4. Course integration waits for the renderer's figure slot (content shape
   still in flux — folio verification HELD; see CLAUDE.md).
