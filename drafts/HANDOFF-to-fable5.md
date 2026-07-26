# Handoff to Fable 5 — what landed on `main`, 2026-07-26

From the Opus session working content/engineering on `main`. You own the visual
redesign, the MechEd rebrand and the two-tree Arabic system on `design-drafts`.

**Nothing has been pushed.** `main` is 15 commits ahead of `origin/main`,
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

## 2. New data field: `recap`

Every Y1S1 lesson (all 66, 6 courses) now has a `recap` key in
`data/content/y1s1-*.json` — a short hand-written bullet summary as an HTML
string, sibling to `lecture`/`foundations`/`kuwait`/`quiz`.

Design note: the summary document is now genuinely different in kind from the
lecture pages — scannable bullets, no diagrams, no lecture prose. `.sum-recap`
is the hook. Worth a distinct treatment in the redesign; the year-1 combined
document dropped from 820 KB to 560 KB as a result.

---

## 3. Arabic — cancelled

The owner cancelled the Arabic translation. Nothing further is being authored,
and it is not waiting on you for anything.

One factual note so it doesn't surprise you in a diff: `y1s1-math-1.json`
lessons 1 and 2 still carry `_ar` sibling keys from before the cancellation.
They are **inert** — `docs/` builds byte-identical with them present — so they
were left in place rather than deleted. Strip them or ignore them as you
prefer.

Leftover working notes live in `drafts/ar-terminology.md` and
`drafts/verify_ar.py` if the translation is ever revived. Not needed otherwise.

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
3. Style `.sum-recap` — the summary document is now bullets, not lecture prose.
4. `nexus.js` untouched. Arabic is cancelled; two lessons of inert `_ar` keys remain in the data.
5. Nothing pushed; `main` is 15 commits ahead, local only.
