# Handoff to Fable 5 — what landed on `main`, 2026-07-26

From the Opus session working content/engineering on `main`. You own the visual
redesign, the MechEd rebrand and the two-tree Arabic system on `design-drafts`.

**Nothing has been pushed.** `main` is 14 commits ahead of `origin/main`,
local only, per the owner's git-safety hold while the rebrand is coordinated on
GitHub.

---

## 1. READ THIS FIRST — I touched two files you own

The file boundary I was given said `nexus_build.py`, `nexus.css` and `nexus.js`
are yours. The owner explicitly confirmed that boundary scopes the **Arabic**
work only, and that Parts 1–2 of the Y1S1 quality plan (which are impossible
without those files) should proceed. So:

| File | Delta | Status |
|---|---|---|
| `assets/nx/nexus.css` | +37 / −2 | **changed — rebase needed** |
| `nexus_build.py` | +73 / −21 | **changed — rebase needed** |
| `assets/nx/nexus.js` | untouched | ✅ clean |

**`nexus.js` is deliberately untouched.** I did not reconnect `applyLang`,
`langBtn` or the localStorage toggle, and I did not touch `NX_PAGE` or
`nx_page()` for any i18n purpose. Your two-tree system remains the only
Arabic architecture.

### What changed in `nexus.css` (all in the summary/print area + one global)

New or re-specialised selectors you'll want to carry into the redesign:

- `.sum-head` — **new.** Summary pages emit with `wrap=False`, so they have no
  `.wrap` ancestor and the header block sat flush-left while the body was
  centred. Gives the header its own `max-width:1060px; margin:0 auto;
  padding-inline:4vw` box matching `.sum-doc`.
- `.part.sum-doc` — **re-specialised from `.sum-doc`.** This was a real latent
  bug: the pages are `<article class="part tight sum-doc">`, and `.part.tight`
  (0,2,0) outranked a bare `.sum-doc` (0,1,0), so the intended `4vw` side
  padding was dead and body text ran into the screen edge on phones. If you
  restructure these classes, keep the specificity in mind.
- `.sum-course` / `.sum-nobreak` — **new print rules.** Per-course page breaks
  in the combined semester/year documents used to ride on Part 1's
  `.sum-part{break-before:page}`. The new recap format has no Part headings, so
  the course heading now carries the break, and `.sum-nobreak` suppresses the
  legacy fallback's Part 1 break so it doesn't emit a near-blank page.
- `.sum-recap` (+ `ul`/`li`/`p`) — **new.** Styles the per-lesson recap bullets;
  serif, 1.8 line-height to match `.measure`.
- `.measure mjx-container[display="true"][width="full"]{min-width:0 !important}`
  — **new, and this one affects lesson pages, not just summaries.** MathJax
  puts an *inline* `min-width` on `\tag{}` display equations; inline beats
  `max-width:100%`, so tagged equations dragged the **whole page** into
  horizontal scroll on a phone instead of scrolling in their own box. Only
  `!important` can override an inline style. **Please keep this rule** — it is
  a genuine mobile fix and easy to lose in a rewrite.
- `figure.lesson-diagram svg{min-width:0}` in the `.sum-doc` and `@media print`
  contexts — the 500px floor is right on a lesson page but clips diagrams in
  print, where nothing scrolls.

### What changed in `nexus_build.py`

Confined to the course-summary functions. No template, routing or chrome changes.

- `course_summary_fragment()` — rewritten. Renders a new per-lesson `recap`
  field instead of dumping every lecture verbatim (owner: the PDFs were just
  copying the lectures).
- `_legacy_compiled_fragment()` — new. Fallback for courses with no recaps yet.
  **Deliberate deviation from the approved plan, flagged to the owner:** the
  plan said fall back to an empty placeholder, which would have instantly
  emptied the PDFs of all 14 already-shipped authored courses. It keeps the
  legacy compiled text with an honest label instead, and courses migrate one at
  a time.
- **"Part 3 — Course reference" removed from summaries for good.** Since the
  Resources restructure that material lives on the course page's own Reference
  tab; printing it twice was duplication. `course_summary_fragment()` therefore
  no longer reads `ref`/`prefix` — I left both in the signature **on purpose**,
  precisely so you don't hit a signature conflict when rebasing.
- `build_course_summary()` / `build_grouped_summary()` — `.sub` copy and meta
  descriptions reworded from "every authored lecture…" to "a condensed revision
  summary".

**Rebase suggestion:** these are additive and localised. If you've rewritten
`nexus.css` wholesale, cherry-pick the `!important` MathJax rule and the four
`.sum-*` rules rather than trying to merge; if you've rewritten
`course_summary_fragment`, take my version's recap-vs-fallback branch since the
`recap` data now exists for 66 lessons.

---

## 2. New data field: `recap` — your AR tree probably wants `recap_ar`

Every Y1S1 lesson (all 66, 6 courses) now has a `recap` key in
`data/content/y1s1-*.json` — a short hand-written bullet summary as an HTML
string, sibling to `lecture`/`foundations`/`kuwait`/`quiz`.

This did not exist when you wrote the Arabic schema, which is why the schema
lists `lecture_ar`/`foundations_ar`/`kuwait_ar` + quiz keys but no `recap_ar`.
I added `recap_ar` by extension on the two lessons I translated, following the
identical sibling convention — **flagging it so you can accept or reject it**.
Without it the AR tree's summary PDFs fall back to English.

Design note: the summary document is now genuinely different in kind from the
lecture pages — scannable bullets, no diagrams, no lecture prose. `.sum-recap`
is the hook. Worth a distinct treatment in the redesign; the year-1 combined
document dropped from 820 KB to 560 KB as a result.

---

## 3. Arabic — stopped, but 2 lessons exist and validate

The owner cancelled the translation ("huge and very hard task that needs super
precise and accurate efforts"). Before that, `y1s1-math-1.json` lessons **1 and
2** were fully translated under your schema:

- `lecture_ar`, `foundations_ar`, `kuwait_ar`, `recap_ar`
- per quiz item: `q_ar`, `choices_ar`, `solution_ar`
- **no `answer_ar` anywhere** — the Arabic item reuses the English `answer`
  index by position, so `choices_ar` must stay in the same order as `choices`

These keys are **inert**: `docs/` builds byte-identical with them present, so
they cost nothing and are there if the translation ever resumes.

### `drafts/verify_ar.py` — please keep and use this

An executable check of the whole contract: markup parity (tag multiset
identical once added `<bdi>` isolators are discounted), inline/display math
span-count parity, glossary row parity, `§N` markers preserved so the build's
`§N→0N` transform still applies, LTR isolation (no bare Latin or digit run in
Arabic prose), quiz shape, and that the English source was never modified.
Run: `python3 drafts/verify_ar.py [course-id]`. Exit non-zero on any failure.

It caught three real defects that reading the Arabic alone could not, because
the Arabic read perfectly well in each case: `\(\sim\)` rendered as the word
"نحو", `\( t \)` rendered as "الزمن", and an English gloss `(Head)` left
un-isolated. **Whoever resumes the translation should run this per lesson.**

### `drafts/ar-terminology.md` — the terminology decisions

Includes the owner's binding rule: *"SI units, prefixes, and all scientific
official terms do not need to be translated into Arabic as they will not make
sense."* Applied as three tiers (established Arabic vocabulary stays Arabic;
units/symbols/standards stay Latin in `<bdi>`; official terms with no settled
Arabic keep the English in `الـ<bdi>term</bdi>`).

Also records source quality, which matters for your `arabize()` work:

- **ARABTERM (arabterm.org)** — best source found. GIZ + Arab League, 156k
  entries, ALECSO-validated "unified Arabic term" marks. Automotive volume has
  Mechanical Engineering / Vibrations / Machine elements / Hydraulics
  categories. Caveat: 2009-era TYPO3, **search box is broken** in a modern
  browser — browse by direct `filterCategory` URL.
- **Reverso Context** — frequency signal only, *not* authority. Four errors
  found in minutes, including "mechanical engineer" → مهندس **مدني** (civil)
  and a flipped inequality. Its headline noun for "gauge pressure" is مقياس
  الضغط, which is the *instrument*, not the quantity.
- **itqan.edu.sa** — genuinely bilingual (EN/AR toggle; the default landing
  page is English, `/ar/` is the Arabic tree). Confirms formal institutional
  MSA and that Latin acronyms stay inline unchanged:
  `شهادات معتمدة من ASNT و ASME و TWI و AWS`.

Owner-corrected terms worth not re-litigating: pump head is **الارتفاع** (not
الرفع); hysteresis is **التخلّف** (owner suggested التباطؤ — undecided, see the
doc); and *gauge* splits three ways — `مقياس الضغط` the instrument,
`قياس الضغط` the act, and `الضغط الـgauge` / `الـabsolute` for the quantity.

---

## 4. Content state

Coverage **224/528 lessons at full depth**. Year 1 is **100% complete** (12/12
courses) — relevant to you because the owner is weighing a **Year-1-only
prototype deploy** as the fastest route to a genuinely complete public site,
and that would be the first thing your redesign is judged on.

Y1S1 also got a notation audit this session: 16 lessons fixed across math-1,
statics, materials-1 and physics-1 where symbols were used without ever being
defined (the curriculum's very first equation, `P = ρgQH`, named none of its
five symbols). Tooling in `drafts/audit_notation.py`, findings in
`drafts/y1s1-notation-audit.md`.

New course in progress: `y2s2-machine-design-1.json`, lessons 1–3 of 11.

**Videos:** the owner has waived the approved-channel list. The integrity floor
that is *not* waived is that every embedded id must be a real video confirmed
live via oEmbed — so no ids were invented, and all video fields remain honest
TODOs pending a proper WebSearch→oEmbed pass.

---

## 5. Short version

1. Rebase `nexus.css` and `nexus_build.py` — additive, localised, described above.
2. **Keep the MathJax `min-width:0 !important` rule**; it fixes mobile on every lesson page.
3. Decide on `recap_ar`; style `.sum-recap` in the redesign.
4. `nexus.js` untouched — your two-tree Arabic system is unchallenged.
5. Nothing pushed; `main` is 14 commits ahead, local only.
