# STEP 5 — Site-wide application of the chosen direction (worklog)

Owner's resolved choice (2026-07-24, via structured answers):
- **Base system: Atlas (Draft C) across all surfaces** — lessons explicitly; curriculum/course
  delegated ("whatever fits all devices, satisfying") → Atlas for coherence + mobile fit.
- **Identity:** "modern, reflects the site's purpose, installable on phones/tablets (PWA
  add-to-home-screen)" → Atlas tokens (Geist, zinc + emerald, adaptive dark) + keep/refresh
  existing PWA machinery (manifest, sw.js, icons, theme-color).
- **Homepage:** owner loves "sliding illustration … moving smoothly and sliding into another
  section" → scroll-driven storytelling: illustrations animate with scroll, sections slide in.
  Interpretation stated to owner in chat (Apple-style scrollytelling; carousel correction
  invited). Implement with CSS scroll-driven animations + IntersectionObserver fallback classes;
  everything off under prefers-reduced-motion.
- **Feedback path:** GitHub Issues chosen, BUT both repos verified live 2026-07-24 with
  "Issue creation is restricted" (nexuskw/nexuskw.github.io AND ilmshri/Nexus-Institute-of-
  Technology). Ship notice linking to https://github.com/nexuskw/nexuskw.github.io (verified
  live, public) labeled "Source & feedback on GitHub"; owner must enable public issue creation
  (org/repo interaction settings), then the link can point at /issues.
- Prototype-phase positioning (no "free" ever): footer line + NOTE 03 wording from the draft
  pass carries into the real chrome. Fixes live cost-rule violations (AUDIT #8).
- Scope: this branch (design-drafts) only. Rebuild docs/ via nexus_build.py. NO merge to main,
  NO push, NO live deploy — gated on owner reviewing the applied result.

## STATUS: COMPLETE (2026-07-24) — all checklist items executed and verified
Build b68cf87567 · 628 pages · gates pass · coverage 188/528 + 124 embeds unchanged ·
zero cost-wording across 631 emitted files · prototype line + GitHub link on every page ·
verified in-browser: home (scroll story, banner preserved), curriculum (semester groups,
toolbar, chips+search), lesson TODO & embed variants (segmented tabs, quiz 8/8, status
chip / video hero), course two-pane (facts + career rail, MathJax leak FIXED), feedback
composer (prefilled-issue URL captured & inspected), career (5 tables), reference (48),
summary (3 parts/22 blocks), mission+about (dark theme pass), mobile 375 (scrollable nav
fix b68cf87567). Committed on design-drafts; merge/deploy remains owner-gated.

## Task checklist

1. [ ] Map build templates: NX_PAGE shell (l.227), nx_page(), hero() (l.559),
       build_lesson_page (l.588), build_course_page (l.792), build_curriculum_index (l.884),
       build_static_pages (l.945: home/about/mission/career), build_reference_page (1241),
       build_course_summary (1340), main() (1400, copies nexus.css/js).
2. [ ] New assets/nx/nexus.css = Atlas system (from design-previews/draft-c-atlas/draft.css)
       EXTENDED to every legacy class the site emits (verify against old nexus.css selector
       inventory): .work boards, .eqrow/.eq/.fr/.rt, .fieldnote, .catch, .plan, .dep-grid,
       .refresher, .check, .map, table.nx-table, .tablewrap, .ref-* (reference page), .sum-*
       + @media print (summary PDF), .searchbox/.search-results, .badge.*, .preview,
       .queued-note, .applied, .keybox, .glossary, .quiz-* (v1+v2), .lib-*, .embed, .vids/.vid,
       .metachips/.mchip, .learn/.learn-grid, .syl, .course-card/.pbar, .tracker, .lesson-row,
       .sem-head, .chips/.chip, .crumbs, .pagehead, .catchphrase, .coursenav, .prevnext,
       .src-strip, .video-hero, .lang-ar/.ar-note (dormant), .sidemenu, .nx-bot (mission only),
       .nx-hero (mission keeps its hero+video), .nx-stats, .fig-panel/.scene/.overview,
       .feat-*, .track/.trow, .note*, .cta-band, .home-cta, .toolchip, .gear-spin/.crank/.piston.
       Keep hero-loop video + FIG scenes working on the new homepage (owner-approved assets).
3. [ ] nexus_build.py template edits (markup only, content pipeline untouched):
       appbar → Atlas app bar (+ ⌘K search affordance linking to curriculum search);
       footer → Atlas slim footer + prototype line + GitHub link; theme-color #0F1115/#FAFAFB;
       lesson page → Atlas player (outline card, segmented tabs, video-status chip when TODO,
       meta chips); course page → two-pane with facts + career rail; curriculum → toolbar +
       semester groups + ccards; home → NEW scroll-story built from existing sections
       (hero w/ approved video loop + console card, sliding FIG scenes, featured, tracks,
       notes, CTA; all real data); mission/about/career/reference/summary → Atlas pagehead
       + restyled existing structures.
4. [ ] nexus.js: append scroll-reveal module (IO adds .in-view; CSS scroll-driven where
       supported; reduced-motion + no-JS safe). Do not touch quiz/tabs/progress logic.
5. [ ] manifest.webmanifest / theme-color emission: match Atlas (check where generated).
6. [ ] python3 nexus_build.py — all gates pass; page count ~579; zero "free"/paywall in
       emitted chrome (scan); prototype line present; Issues→repo link present.
7. [ ] Browser verify: home (scroll story, reduced-motion), curriculum (search/filter),
       course (career rail, MathJax), lesson (4 tabs + quiz + video-status; one WITH real
       embed e.g. fluids L4 + one TODO), career page (nx-table), reference page, summary
       print CSS, mission (hero video + bots intact), about; mobile 375 pass on home/lesson/
       curriculum; dark-mode pass.
8. [ ] Commit on design-drafts. Update this worklog + README. Report to owner with
       merge/deploy gate reminder + GitHub issue-setting instruction.

## ADDENDUM — Review section (owner order mid-Step-5, 2026-07-24)

Owner: "build me a review section where users using the website can comment their reactions
and what they think of the website/application for any future releases and modifications."
Static-site reality: no backend → reviews must land in an owner-readable channel.
Implementation (this pass): new emitted page `feedback/index.html` (nav item "Feedback"):
structured review composer — overall reaction 1–5, what was tried, what worked, what should
change, optional name — with two honest actions: (a) "Post on GitHub" → prefilled new-issue
URL on nexuskw/nexuskw.github.io (goes live when the owner lifts the issue-creation
restriction — flip BEFORE deploying); (b) "Copy review text" (clipboard). Clear note that
posting needs a GitHub account. Homepage CTA band + footer prototype line link to it.
NO fake comment display, NO invented reviews, NO email published (owner has not approved
publishing an address — offered as a follow-up option). JS composer lives in nexus.js.

## Key invariants (binding)

- No content/data edits; docs/ changes come ONLY from rebuilding with new templates.
- No renames/moves of any file. nexus.css/nexus.js keep their names (cache-busted by ?v=hash).
- Quiz/tabs/progress DOM contracts unchanged (nexus.js logic untouched).
- Company-name, §, video-channel build gates stay enforced (don't touch gate code).
- prefers-reduced-motion: all new motion off; keyboard/focus states preserved.
- English-only chrome; Arabic machinery stays dormant but unbroken.
