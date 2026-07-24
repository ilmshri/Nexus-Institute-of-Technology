# Nexus Design Drafts — How These Previews Work

Three complete, isolated design directions for nexuskw.github.io, built 2026-07-24 on the
`design-drafts` branch. Nothing here touches the live site, the build system, or any content.

## View them

```
python3 -m http.server -d "/Users/ilmshri/Social Media/nexus-design-drafts" 8010
```

Then open **http://localhost:8010/design-previews/** — the hub links every page of every draft.
(Opening the HTML files directly from disk also works.)

Each draft covers the same four real surfaces, so it can be judged as an experience:

| Surface | File | What to judge |
|---|---|---|
| Homepage | `index.html` | identity, hero, how the product is presented |
| Curriculum index | `curriculum.html` | how 48 courses / 8 semesters read; search + filter live |
| Course + career | `course.html` | course anatomy + the Career outlook block treatment |
| Lesson (all 4 tabs) | `lesson.html` | reading experience, tabs, working quiz engine, library |

## The three directions

- **`draft-a-foundry/` — Foundry.** Industrial / workshop-HMI register. Dark graphite chrome,
  hazard-amber accents, condensed stencil display type (Saira Condensed), IBM Plex Sans/Mono.
  Lessons read on white "engineering drawing sheets" with title blocks; the depth ledger is
  presented as plant telemetry; curriculum is a dense spec-sheet grouped into semester "bays."
- **`draft-b-press/` — Press.** Academic / technical-editorial register. Warm paper, near-black
  ink, one crimson; Fraunces display + Source Serif 4 text + Plex Mono folios. No cards — rules,
  hanging numerals, chapters, dot-leader contents. Curriculum is a university-press catalogue;
  lessons are journal articles with a margin table of contents.
- **`draft-c-atlas/` — Atlas.** Learning-console register. App shell, persistent course rail with
  progress ticks, segmented tabs, ⌘K search, status chips, one emerald accent on zinc neutrals;
  Geist + Geist Mono. Includes a genuinely adapted dark theme via `prefers-color-scheme`.
  Career outlook is elevated to its own rail card beside the syllabus.

## Integrity guarantees

- `build_drafts.py` assembles every page from the REAL generated pages in `docs/` — the four
  lesson tab panels, quiz items, syllabus rows, and career-outlook copy are **byte-identical**
  to the live content (verified programmatically). No file under `docs/`, `data/`, or `content/`
  was modified.
- The shared behavior layer (`shared/drafts.js`) re-implements the live site's DOM contracts
  (tabs, select-then-submit quiz, reveal solutions, semester chips) so the previews are
  interactive without touching `assets/nx/nexus.js`.
- MathJax loads on lesson AND course pages — this is why the `\( F_s>2f_{max} \)` career-block
  math renders here while it leaks raw on the live course page (see AUDIT.md #15).

## Chrome copy changes (the only copy this build rewrites — deliberate, documented)

Per the owner's binding cost rule (CLAUDE.md, 2026-07-18: the site never mentions its own
cost/"free"), which the current live homepage violates:
- CTA band "Start with Lesson 01. **Free, forever.**" → "Start with Lesson 01."
- Footer "**Free,** open engineering education." → "Open engineering education."
- NOTE 03 "**No paywalls,** no accounts." → "No accounts needed."

Other chrome notes: the "7 of 11 complete — preview state" progress shown in course/lesson rails
is demo state (labeled as such on-page); Draft B's masthead "Est. MMXXVI" is a removable flourish;
fonts load from the Google Fonts CDN (same pattern as the existing MathJax CDN dependency —
self-hosting is an option at rollout).

## Companion documents

- `RESEARCH.md` — verified market study (education platforms + industrial/docs register, 2026).
- `AUDIT.md` — honest audit of the current site: 25 findings, incl. 3 content-side bugs reported
  (not fixed — content is out of scope for design work).

## What happens after a direction is chosen (not before)

Owner picks one draft (or a mix — e.g. "Atlas structure with Foundry's lesson sheet"). Then, per
the agreed workflow: the chosen system is applied site-wide by porting its `draft.css` into
`assets/nx/nexus.css` and updating the chrome templates inside `nexus_build.py` — the content
pipeline, quiz engine contracts, and all data files stay untouched — then rebuilt, verified
page-by-page, and only then merged back. **No merge happens until the owner's explicit go-ahead.**
