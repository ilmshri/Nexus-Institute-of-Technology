# Arabic content authoring spec — MechEd two-tree system

Owner decision 2026-07-26: the `/ar/` mirror-tree architecture (design-drafts
branch) is the permanent Arabic system. This card tells the content-translation
session exactly how to author Arabic so it merges with zero rework. It is a
reference, not a rebuild guide.

## How the system works (30 seconds)

Every page is emitted twice by `nx_page()`: English at `<path>`, Arabic at
`ar/<path>` with `<html lang="ar" dir="rtl">`. Chrome (nav, footer, labels) is
translated by the build. Bodies come from one of THREE channels, in order of
preference for content work:

1. **`ar_body`** — a full Arabic HTML body for the page (career/mission pattern).
2. **`data-ar` leaf swap** — short labels only, swapped at build time.
3. **Fallback** — English body shipped under Arabic chrome, bidi-isolated in
   `<div lang="en" dir="ltr" class="en-body">`, with an honest `ar-note` banner.

The quiz ENGINE (verdicts, reveal buttons, score lines) is already bilingual at
runtime via `qtxt(ar, en)` in nexus.js — it keys off `document.documentElement.lang`,
which the AR tree bakes in. Do not re-translate engine strings.

## Channel 1 — lesson content (what the translation session authors)

Author Arabic as **sibling `_ar` keys** in the existing per-course content files
`data/content/<sem>-<course>.json`, per lesson dict:

```json
"7": {
  "lecture":        "<existing English HTML>",
  "lecture_ar":     "<full Arabic HTML, same structure>",
  "foundations":    "…",
  "foundations_ar": "…",
  "kuwait":         "…",
  "kuwait_ar":      "…"
}
```

Rules for the `_ar` HTML:
- **Same markup contracts as English**: identical classes and structure
  (`.keybox`, `figure.lesson-diagram`, `table.glossary` with the same columns,
  `h3` section heads). Translate text, never restructure.
- **Binding bilingual rule (owner, 2026-07-17)**: translate everything EXCEPT
  numbers, equations, math symbols, proper nouns, and core technical terms —
  those stay English/original.
- **Bidi isolation**: wrap every inline LTR run (numbers with units, MathJax
  `\( … \)`, English technical terms, code) in `<span dir="ltr">…</span>` or
  `<bdi>` so mixed lines never flip punctuation. Display math: keep the block
  on its own line; MathJax delimiters work unchanged.
- Formal Arabic (فصحى), professor's voice. Never machine-mangled output.
- Quiz items: reserved keys `q_ar`, `choices_ar`, `solution_ar` per item —
  same shape as the English keys. Fine to author now; they wire later.
- Brand word stays Latin **MechEd/MECHED** in Arabic text (owner constraint
  2026-07-25). SVG diagram text labels stay English for now (they are computed
  vectors; a labeled-AR variant is a later, separate pass).

NOTE: the builder wiring that CONSUMES `_ar` keys does not exist yet (frozen by
owner order). Authoring to this schema is exactly what makes the later wiring a
no-rework merge: the lesson builder will pass the assembled Arabic tabs as
`ar_body` and drop the honest note automatically when all `_ar` parts exist.

## Channel 2 — `data-ar` leaf swap (labels only)

`arabize()` in nexus_build.py swaps element text with its `data-ar` attribute at
build time using this contract (regex-enforced):

```
<tag … data-ar="النص العربي" …>plain English text</tag>
```

Hard constraints:
- The element's inner content must be **plain text only — no child tags, no
  comments**. An element containing children is silently left English (safe
  degradation). Put `data-ar` on the deepest text-bearing element.
- Opening and closing tag must be the same element (no self-closing/void
  elements — they have no inner text; use ar_body content instead).
- The attribute value is normal HTML-escaped attribute text (`&amp;` etc. fine).
- One attribute translates one element. No nesting tricks.
- The EN tree strips all `data-ar` at emit; the AR tree consumes then strips.
- Use it for SHORT labels (buttons, headings of fixed sections, chips). Never
  for paragraphs — long text belongs in `_ar` keys / `ar_body`.

## Channel 3 — page-level overrides (already wired)

`nx_page(..., ar_body=…, title_ar=…, ar_note=…)`:
- `ar_body`: full replacement body for the AR twin (Arabic HTML). No `.en-body`
  wrapper is applied; the page is a native RTL document. Precedents:
  `content/pages/career-ar.html` (whole-page fragment) and mission's embedded
  `<div class="lang-ar">` block.
- `title_ar`: the AR `<title>`. Convention: `"العنوان — MechEd"`.
- `ar_note`: `True` = lesson-specific honest note, `"page"` = generic page note.
  Don't combine with `ar_body` (a translated page needs no note).
- Asset paths inside any body: write them `{prefix}assets/…` as usual — the
  emitter rewrites `src=`/`href=`/`poster=` asset references one level up for
  the mirror automatically. Page-to-page links stay `{prefix}`-relative and
  resolve inside `ar/` on their own. Never hand-write `../ar/` or `ar/` links.

## Merge safety

Content translation work should touch ONLY `data/content/*.json` (the `_ar`
keys) and, if translating static pages, new `*-ar.html` fragments under
`content/pages/`. No changes to nexus_build.py, nexus.css, or nexus.js are
needed for authoring — that keeps the eventual merge with the design branch
conflict-free.
