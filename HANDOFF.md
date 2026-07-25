# HANDOFF — Nexus design-refinement work (design-drafts branch)

Written 2026-07-24 at owner's request before a chat switch. A fresh session must be able
to continue from THIS FILE ALONE. Read CLAUDE.md (master brief + ledger) alongside it —
the ledger's newest entries (BRIGHTNESS VALUE, ATLAS REDESIGN APPLIED) were written this
session and are binding.

## 0. Where you are

- This worktree: `/Users/ilmshri/Social Media/nexus-design-drafts`, branch **design-drafts**.
  Main checkout: `/Users/ilmshri/Social Media/nexus-institute` on `main` (untouched; has its
  own uncommitted docs rebuild from a prior session — leave it alone).
- Branch commits this effort (oldest→newest): `2abe4d3f` round-1 drafts + research + audit ·
  `9b04610b` prototype positioning · `352d6026` **Atlas applied site-wide + review section** ·
  `85607559` ledger · `bf9fb635` **dark mode removed (brightness value)** · `4282e553`
  **round-2 five bright drafts** · `f04bad4a` bright hero loop wired · (this file's commit).
- **NOT merged to main, NOT pushed, NOT deployed. Live site (nexuskw.github.io) unchanged.**
  Merge/deploy is explicitly owner-gated.
- Preview server: launch config **nexus-drafts** (project `.claude/launch.json`) serves this
  worktree at **http://localhost:8010** (`python3 -m http.server -d <worktree> 8010` works
  too). Port 8000 may be occupied by another chat's `nexus-docs` server.

## 1. What exists, and where

### A. The APPLIED site (docs/ — the real build, restyled)
Owner's round-1 choice ("Atlas base + scroll homepage + PWA") is fully applied through the
real generator on this branch:
- `assets/nx/nexus.css` — rewritten as the Atlas system; **always-light** (all
  `prefers-color-scheme: dark` blocks removed in bf9fb635 per the brightness value).
- `nexus_build.py` — chrome templates changed: app bar (+ **Feedback** nav item, ⌘K search
  link), compliant footer (prototype line + GitHub repo link, NO cost wording), Atlas lesson
  headers (+ metachips), compact "Lecture video — in production" chip replacing the old giant
  empty panel, course pages two-pane (facts card + career-block in right rail, **MathJax now
  loads on course pages** — fixes the raw `\( \)` leak), curriculum grouped by semester with
  sticky search/filter toolbar, NEW `feedback/index.html` builder (review composer).
- `assets/nx/nexus.js` — appended: homepage scroll reveals, scroll-spun FIG-01 gears,
  semester-group filter sync, ⌘K, review composer (prefilled GitHub issue + clipboard).
  Core quiz/tabs/progress logic untouched.
- `content/pages/home-nexus.html` — cost-rule violations fixed ("Free, forever", "No
  paywalls" removed), NOTE 03 → "Open prototype", review CTA added. (Green-listed file.)
- `assets/nx/manifest.webmanifest` — light colors (#FAFAFB / theme #0B8A68), compliant copy.
- Build state: `python3 nexus_build.py` → 628 pages, ALL integrity gates pass (§-scan,
  non-logo-img, NPTEL-embed guard, unit-policy 17/17), coverage **188/528 (36%)** and
  **124 embeds** byte-identical to before the redesign (content untouched). Verified in
  browser across every page type + mobile 375px. Mobile nav is scrollable (fix in b68cf875…
  generation, commit 4282e553's parent chain).

### B. Round 1 drafts (design-previews/) — historical reference
`draft-a-foundry` (dark industrial — **RETIRED**, violates brightness value),
`draft-b-press` (light editorial), `draft-c-atlas` (light console; basis of the applied
site). Hub `design-previews/index.html` (carries a banner marking round 2 + Foundry's
retirement). Assembler `design-previews/build_drafts.py` extracts REAL content from docs/
— it now has fallbacks for BOTH markup generations (old pre-Atlas and applied-Atlas), so it
still runs against current docs/. `shared/drafts.js` re-implements site DOM contracts
(tabs/quiz/chips) for previews. Docs: `RESEARCH.md` (market study), `AUDIT.md` (25-finding
site audit), `README.md`, `STEP5_WORKLOG.md` (the applied-redesign log, marked COMPLETE).

### C. Round 2 drafts (design-previews/round2/) — **CURRENT, awaiting owner ratings**
Owner order: never dark; 3–5 full bright designs to experience and rate; effects/video
allowed. Five complete drafts, each = 4 surfaces (home, curriculum, ELX 205 course+career,
Lesson 08 with 4 live tabs + working quiz), same byte-identical real content:
- `a-aurora` — bright learning console (Geist, emerald, aurora hero wash, learner console).
- `b-meridian` — bright editorial press (Fraunces + Source Serif, paper+one crimson,
  self-drawing gear plate, small-caps underline tabs).
- `c-beacon` — encouragement-as-design (Bricolage Grotesque, sunshine amber + teal + coral,
  robot crew from assets/nx/bots/, cheer chips). Academic voice unchanged.
- `d-blueprint` — bright technical (Archivo + Plex Mono, cyan grid paper, drafting blue +
  amber, title-block sheet hero, draw-on figures, squared corners).
- `e-skyline` — video-led showcase (Space Grotesk, sky gradient, light-glass chips,
  gradient headline, generated bright hero loop front and center).
Infrastructure: `base.css` (variable-driven shared layer styling ALL content contracts —
each draft.css only sets tokens + chrome + personality overrides), `fx.js` (reveals,
SVG draw-on, count-up stats, scroll-spun gears, parallax; ALL off under
prefers-reduced-motion), `build_round2.py` (imports ../build_drafts.py for extraction),
**rating hub `round2/index.html`** — per-draft 1–5 score + notes + "Copy my ratings"
button that composes a paste-back summary.
Generated media (Higgsfield, owner-invited): `assets/hero-bright.png` (key frame, job
c379b1c2-6205-4aec-b50f-9f07c3f56fa4, nano_banana_pro 21:9) and `assets/hero-bright.mp4`
(10 s seamless loop, H.264, silent, seedance_2_0 job cbfee7b3-8bb5-427e-a23d-a062dc423e35;
first attempt was a filter false-positive, retried with neutral wording). 92 credits spent
this session; **765 remain**. The loop follows the owner's approved v3.1 recipe (arm places
gear → train spins → telemetry pulses → arm returns) but BRIGHT cream, per the new value.
Verification: all 20 pages built; lesson tab panels byte-identical to docs/ source
(programmatic check); zero "free"/paywall wording; quiz engine live-tested (8/8) on
round-2 pages; all five homepages screenshot-verified.

## 2. Owner decisions — made, standing, ruled out

MADE / BINDING:
1. **Brightness value (2026-07-24, permanent):** backgrounds never dark or dim; no dark
   mode; dark pixels only inside bounded approved media. (Ledgered; also in auto-memory.)
2. **Prototype positioning (2026-07-24):** the platform is a preliminary open release for
   trial and reflection; NEVER described as "free"; feedback shapes final tailored releases.
   Footer line + NOTE 03 carry this site-wide.
3. Round-1 selection: **Atlas base everywhere** (lessons explicitly; curriculum/course
   delegated to fit-all-devices), modern identity, installable PWA kept, **scroll-driven
   "sliding illustrations"** homepage (interpretation confirmed in chat: scroll-triggered
   section slides + scroll-linked illustration motion; carousel correction was invited and
   not raised).
4. **Review section** (owner order): built as the Feedback page — composer → prefilled
   public GitHub issue on nexuskw/nexuskw.github.io or clipboard copy. NO fake/displayed
   reviews, NO email published (owner never approved an address).
5. Feedback channel: **GitHub Issues** — BUT both repos verified live with "issue creation
   restricted" (nexuskw/nexuskw.github.io and ilmshri/Nexus-Institute-of-Technology).
   **Owner must flip that setting before deploy**, else the Post button gets rejected.
6. Motion allowed (supersedes old no-animation hold) but ALWAYS disabled under
   prefers-reduced-motion; no cost to brightness.
7. Standing integrity rules obeyed everywhere: content byte-identical (no lesson/quiz/
   career text edits by design work), no file renames, no fabricated URLs/reviews, build
   gates never touched.

RULED OUT / RETIRED: dark mode & dark-first design (Foundry retired as historical);
"free"/paywall wording; fake comment walls; email feedback link (unapproved); GTranslate
(older owner removal, stays out).

OPEN — CONSIDERING (no decision yet):
- **Platform rename.** Assessment given: name lives in ~40 chrome strings + 2 fragments +
  docs + manifest; **zero occurrences in lesson content** (grep-verified) — name-only
  rename is ~1 hour + residue scan (precedent: the SDF→Nexus purge). The consequential
  part is the URL (GitHub account binding; renaming orgs is the risk zone — the old
  sundevilfactory org was once accidentally deleted; custom domain is the clean end state;
  dual-remote push URLs must never drop nexuskw). Shortlist offered (availability NOT
  verified — must check GitHub handle, domain, GCC trademark distance before committing):
  **Itqan** (mastery — top conviction), **Masar** (pathway), **Qantara** (arch/bridge),
  **Sanad** (support + verified chain), **Manara** (beacon — collision flag: manara.tech),
  **Rakiza** (structural pillar), or Latin fallback **Meridian**.
- **Kuwaiti heritage layer.** Recommendation delivered: yes, as core identity (not
  AR-only skin), under three rules — structural not decorative (Sadu-inspired geometric
  bands in functional slots: dividers, active-tab underline, progress texture, certificate
  headers, PWA icon frame), **pearl-strand progress metaphor** (completed lesson = pearl,
  course = strand), always bright with deep Sadu red only as a thread accent. Original
  vector interpretations only (Al Sadu is UNESCO-listed heritage — never copy real
  weavings; also keeps the vector-only rule). Arabic layer itself remains ON HOLD (owner
  2026-07-21); heritage can ship subtly site-wide now and deepen when AR returns (that
  future pass should add a real Arabic webfont, e.g. IBM Plex Sans Arabic). A ~1-hour
  heritage demo on the winning draft was OFFERED, not yet ordered.

## 3. Exact next step (what I was about to do)

**Waiting on the owner**: they experience the five round-2 drafts at
`http://localhost:8010/design-previews/round2/` (start the `nexus-drafts` server first),
score each 1–5 with notes, press **"Copy my ratings"**, and paste the block into chat.

When that paste arrives, the plan in order:
1. Parse ratings → winner or blend (blend = per-surface mix like round 1; get specifics if
   free-text is ambiguous).
2. If the rename is decided by then: run availability checks (GitHub handle — expect the
   `<name>kw` pattern, domain, trademark distance), then fold the name in.
3. Build the offered **heritage demo** (Sadu band + pearl-strand progress) on the winning
   draft for approval BEFORE applying.
4. Apply winner (+ name + heritage if approved) site-wide through `nexus_build.py` /
   `assets/nx/nexus.css` exactly like the Atlas pass (STEP5_WORKLOG.md documents that
   pipeline; build_round2 themes port the same way — base.css tokens → nexus.css).
   Rebuild, run gates, verify page types + mobile, commit on design-drafts.
5. Still owner-gated after that: GitHub issue-creation flip, merge to main, push/deploy.

## 4. Market research — keep, don't re-research

Full source-tagged reports: `design-previews/RESEARCH.md` (market study; every claim
verified or labeled) and `design-previews/AUDIT.md` (25 findings on the pre-redesign site).
Headlines a new session should know:
- Verified tokens: MIT OCW = Cardo serif + Helvetica, crimson #a31f34/#750014, blue
  #126f9a, "document archive" course pages (no ratings). Coursera = #0056D2 + black +
  white only, Source Sans Pro. Khan = action blue #1865f2 on offBlack #21242c / offWhite
  #f7f8fa, Lato; 2025-26 rebuild = learner dashboard, mastery queue, semantic token
  hierarchy. Open edX = navy #092B4D + magenta #9d0054 (April 2026 rebrand).
- Registers: institutional (OCW) vs commercial MOOC (Coursera/edX) vs consumer (Khan/
  Brilliant). Docs register engineers respect: ⌘K search, deep sidebars, terse task
  grouping, Geist Sans + Geist Mono pairing (Vercel), Light/Dark/System toggles (dark now
  irrelevant here by owner value).
- Industrial-SaaS seriousness = numbers-with-units owned by named customers, protocol
  vocabulary (OPC UA, OEE), product screenshots/telemetry, clipped copy ("Operator grade.
  Proven in the field." — Samsara). Nexus's honest depth ledger maps onto this.
- 2026 trends: semantic monospace mainstream; the dark+glow+bento "Linear look" is now
  startup-generic; glass = accent only on light; scroll micro-motion ships, heavy WebGL
  doesn't; pure Inter-alike defaults read generic. Dated: multi-color logos, promo
  carousels, mega-menus, catalog-as-plain-list.
- AUDIT keepers: the computed SVG diagrams are the platform's "product screenshots" —
  feature them; honest depth labels are a trust asset — style up, never hide.
- CONTENT bugs found but NOT fixed (content work is out of design scope — report to owner
  in a content session): §-references stripped to bare numbers ("per 3 and 4") in ELX 205
  L08 applied case; "industrial Safety" lowercase title (SAF 256 data). FIXED in this
  branch (were chrome/template bugs): live homepage cost-rule violations; raw LaTeX in
  course-page career blocks.

## 5. Environment quirks (so the next session doesn't chase ghosts)

- The embedded browser pane sometimes blanks on scrolled screenshots, pauses background
  <video> (the bright loop IS valid H.264 — verify playback on a real browser), and
  captures reveal animations mid-flight (below-fold elements look half-faded in
  screenshots; they complete for real users). Use tall viewports + JS scrollTo.
- `build_drafts.py` is import-safe (extraction at module level, emit under __main__ guard);
  `build_round2.py` depends on that import.
- Higgsfield jobs: image ~30 s, video ~5-8 min; poll with job_display; one video attempt
  was rejected "nsfw" (false positive on a gear illustration) — rephrase neutrally and
  retry with declined_preset_id if a preset nag appears.
- Owner interaction pattern: fast decisive replies, sometimes mid-turn ("pause"/"resume");
  values honesty, brightness, Kuwait identity, integrity floor above speed.
