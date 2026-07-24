# Nexus Institute — Honest Design Audit (2026-07-24)

Audited against the current build in `docs/` (viewed at localhost, desktop 1280px + mobile 375px):
homepage, curriculum index, course page (ELX 205 incl. career outlook), lesson page (ELX 205 L08, all 4 tabs).

## The one-line verdict

The site is **coherent, honest, and completely anonymous**: system Helvetica + Georgia, teal-on-cream,
rounded 14px cards for *everything* — it reads as "nicely configured template," not as an institution
with a visual point of view. Nothing in the visual language says *engineering* except the (excellent)
diagram content itself.

## Identity & typography

1. **Zero typographic identity.** Helvetica Neue (headings) + Georgia (body) + system mono. No display
   face, no chosen text face — the exact stack of a 2012 default. The wordmark is styled body text.
2. **Half-committed serif/sans mix.** Georgia appears in body copy, subheads, and figcaptions; Helvetica
   in headings and UI; mono in labels. Three voices with no rule for who speaks when.
3. **The teal (#14CFA0→#07785C) + amber (#F5A623) palette is pleasant but unowned** — it's the default
   "SaaS green" family. Navy #0E1626 exists only as card caps and table headers. There is no dark mode.

## The card monoculture

4. **Everything is the same 14px-radius outlined white card** — stats, figure panels, featured courses,
   tracks, notes, syllabus rows, quiz items, keyboxes, career blocks, library blocks. Identical corner
   radius, identical 1px #E2E5E4 border, identical weight. No hierarchy between decoration and product.
5. **Card-inset heroes.** Homepage, course, and lesson all open with the same rounded dark-gradient
   panel floating in margins. Three contexts, one gesture — and it caps presence (no full-bleed moment
   anywhere on the site).

## Homepage

6. **The product is buried.** Two large decorative panels (FIG 01 gears, FIG 02 system map) sit between
   the hero and the first actual course link. FIG 02 particularly is ~500px of six plain circles +
   dashed lines — clip-art information density.
7. **Headline set in bold white Helvetica over a busy illustration** — the video loop is nice, but the
   serif subhead over mid-tone teal machinery strains readability (text-shadow is doing heavy lifting).
8. **COST-RULE VIOLATION (owner's own binding rule, 2026-07-18):** "Start with Lesson 01. **Free,
   forever.**" (CTA band), "**Free**, open engineering education" (footer, every page), "**No paywalls,
   no accounts**" (NOTE 03), meta description "Free, forever." — all reintroduced by the v3 homepage.
9. Stats band is honest (good) but visually four more identical cards.

## Curriculum index

10. **Default "All" view is a wall of 48 near-identical cards** — the semester/pathway structure (the
    site's core claim: "strict grid, prerequisites in order") is invisible until you use filter chips.
    A degree map presented as a shop catalog.
11. **Navy card caps waste space**: 96px dark slabs with a small centered icon; several icons repeat
    (sun/gear variants), so cards don't actually identify their course visually.
12. Card descriptions truncate mid-word ("…the sec…", "…differential equ…"). Mono status lines +
    empty progress bars on 47 cards add noise before any learning starts.
13. Search box is visually minor for a 528-lesson catalog; no ⌘K affordance, results dropdown only.

## Course page

14. **Career outlook — the platform's differentiator — is visually an afterthought**: a cream box with
    an amber border at the very bottom, dense bullet prose, no structure (roles/employers/skills all
    inline). It reads as a disclaimer, not a selling point.
15. **Raw LaTeX leaks in career blocks**: `\( F_s>2f_{max} \)` renders as literal text on the ELX 205
    course page (course pages don't load MathJax; career data contains math markup).
16. Syllabus = 11 stacked full-width cards, each with a repeating "FULL LESSON" badge — 11 identical
    badges is noise, and checkpoint questions hide behind small expanders.

## Lesson page (the product's core surface)

17. **The first thing a learner sees on most lessons is an empty placeholder**: the "TODO: Find approved
    video" dashed panel sits above the tabs on every lesson without an approved embed (the majority).
    Honesty is right; giving the gap the hero position is a design choice that punishes it.
18. **Tabs look like filter chips, not the lesson's primary navigation**: small uppercase letter-spaced
    text buttons with a 3px underline, visually weaker than the "Mark as complete" button above them.
19. **Repeated identity chrome eats the viewport**: dark hero card (~200px) + tools row + source strip +
    video panel — real content starts ~700px down even on desktop.
20. Quiz UI: three consecutive full-width ALL-CAPS green "SHOW THE FULL SOLUTION" bars band the page;
    A/B/C/D key chips are tiny; "Check again / Reveal answer" buttons appear before any selection
    (probably unintended). No per-item progress indication until the bottom Submit.
21. Library tab renders an **empty "Lesson video" card** when there's no video, and the NPTEL source
    line appears **three times** on one page (source strip, "Taught from," references list).
22. Sidebar outline is functional but cramped (12.5px), and "0 of 11 complete" mono text is the only
    progress voice on the page.

## Mobile (375px)

23. No mobile nav pattern — six links wrap to two crowded lines; brand text hidden entirely.
24. Hero + meta stack + video TODO push first content ~2 screens down.
25. Diagrams scroll horizontally by design, but with zero scroll affordance (labels visibly clipped).

## Content-side bugs noticed in passing (NOT design; not touched — reported only)

- Stripped section references read as bare numbers: "applying 3's ranking", "per 3 and 4"
  (ELX 205 L08 applied case) — the §-purge transform appears to eat "§3" → "3".
- "industrial Safety" lowercase title on the curriculum card (SAF 256).
- Homepage/footer/meta "free" wording violates the owner's binding cost rule (see #8).

## What's genuinely good (keep in all drafts)

- The computed SVG diagrams are excellent and unique — they should be *more* prominent, not less.
- Honest depth labeling ("199 of 528 · 38%", "in production") is a trust asset worth designing UP.
- The 4-tab Educational Unit structure is sound; content typography (75ch, 1.8 line-height) reads well.
- The Academic Shield logo + navy/teal/amber tokens are approved equity — reusable as accents even in
  new palettes.
