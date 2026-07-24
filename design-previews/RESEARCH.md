# Market Study — Education & Technical-Industrial Design Language, mid-2026

Compiled 2026-07-24 from live fetches + firsthand browsing this session. Every specific claim below was
verified from a fetched page, an official design-system repo, or a first-party announcement; where a
value could not be verified it is labeled as a general pattern. (Full source-tagged reports preserved
in this file's two appendices' underlying agent runs; key sources linked inline.)

## 1. What the serious education platforms actually do (verified)

**MIT OpenCourseWare** (browsed firsthand + theme repo `mitodl/ocw-hugo-themes`):
- Identity: MIT crimson (`#a31f34`, dark `#750014`) + steel blue (`#126f9a`) on white/near-white grays.
- Typography: **Cardo (serif) + Helvetica** pairing; headings weight 600; type scale 12–32px.
- Course pages read as **document archives**: flat steel-blue title band (`2.003SC | Fall 2011 |
  Undergraduate` eyebrow + huge white title), left sidebar of materials, underlined links, outlined
  resource pills, "Download Course" — zero ratings, zero conversion furniture. Register: institutional,
  print-like, dense, credible.
- Current platform is the 2022 "NextGen OCW"; actively maintained into 2026.

**Coursera** (official brand guide): palette is deliberately tiny — **blue `#0056D2` + black + white**;
**Source Sans Pro everywhere** (chosen for 582-language support). Course pages are conversion pages:
ratings, enrolled counts, accordion syllabus with hour estimates, LinkedIn-shareable certificate badges.

**edX / Open edX**: rebranded to **navy `#092B4D`/`#0A3055` + magenta `#9d0054`** (Open edX brand
transition completed April 2026; Paragon design-system tokens match). Homepage now opens on a discount
banner — the most commercial register of the group. Old rainbow-gradient logos retired.

**Khan Academy** (Wonder Blocks tokens, firsthand chrome check): functional color — action blue
`#1865f2`, **offBlack `#21242c` / offWhite `#f7f8fa`** (no pure black anywhere), brand darkBlue
`#0b2149`; **Lato**; 2025–26 rebuild adds a 4-level *semantic* token hierarchy
(Domain→Layer→Context→Intensity) and a learner dashboard with mastery queue, streaks, and the AI tutor
pinned at top. Principles: Empowering, **Credible**, Flexible, Joyful.

**Engineering-education specifically**: Brilliant repositioned as "a world-class tutor" with boutique
type (CoFo Robert/Sans, 2024 Koto refresh) — the consumer-premium end. The Efficient Engineer = the
credible single-author register (video-first lesson + long sectioned article + LaTeX equations +
summary-sheet callouts). NPTEL = what "dated institutional" looks like: stats carousel homepage, mega-
menus, Google-Docs announcements, slate grays. Ansys is relaunching its learning space as "AI-powered."

**2026 register table** (verified across the above):
- *Institutional/academic* (OCW, MITx): university color + course numbers + faculty names; document-
  archive course pages; donation not pricing; serif accent + grotesque.
- *Commercial MOOC* (Coursera, edX): corporate blue/navy + partner-logo walls; conversion furniture.
- *Consumer/K-12* (Khan, Brilliant): functional bright palette + mascot/AI persona; dashboard-first.

**Now-dated patterns** (all verified retired or observed as the outlier): multi-color/gradient logos and
icon-glyph marks (norm is a confident wordmark), auto-rotating promo carousels, stats-carousel
homepages, mega-menu navigation, catalog-as-plain-list.

## 2. What the serious technical/industrial register does (verified)

**Docs leaders** (Stripe, Vercel, Tailwind, Linear, PyAnsys, MATLAB, Fusion):
- The respected register = **complete, hierarchical, searchable, terse**: ⌘K search affordance
  (Tailwind shows the shortcut in the nav), deep sidebars (Tailwind ~200 links; MATLAB 60+ categories),
  numbered install steps, task-oriented grouping, uniform card/link rhythm (Linear caps card copy at
  ~125 chars), Light/Dark/System toggles (PyAnsys).
- **Vercel Geist**: Geist Sans + **Geist Mono**, "high contrast, accessible color system," and "Grid —
  a core part of the Vercel aesthetic." The sans + semantic-mono pairing is the 2026 signature.
- New in 2025–26: AI/agent surfaces inside docs (markdown endpoints, MCP sections, Copilot entries).

**Industrial SaaS** (Ignition, Tulip, Samsara, Cognite, Siemens Insights Hub/iX):
- Seriousness is signaled by **numbers-with-units owned by named customers** ("↓66% defects — DMG
  MORI", "7500 data points every 15 s"), **protocol vocabulary as in-group handshake** (OPC UA, MQTT,
  OEE, GxP), product screenshots / field photography **with data overlays** (a dark map reading "Van
  #735 … at 43 MPH"), compliance/analyst badges, and clipped imperative copy — Samsara's
  "**Operator grade. Proven in the field.**" is the purest example. Siemens ships an open design system
  explicitly "for industrial software products" (Siemens iX).

## 3. 2026 trend ground truth (dated sources; agency/practitioner blogs — directional)

- **Typography**: monospace revival is mainstream and semantic (data, codes, labels), beyond dev tools;
  variable fonts standard; big display type continues; the *pure Inter-alike neo-grotesk default* is
  what now reads generic (Font Trends 2026, May 2026; Geist verified firsthand).
- **Color**: dark-mode-first is a workflow, not a feature (design dark, adapt light) — but for
  education/reading surfaces, high-contrast restrained light remains the credibility register (Vercel:
  "high contrast, accessible"; Khan: offBlack on offWhite).
- **Layout**: bento grids are simultaneously "the default" and decayed into decorative card walls; the
  full 2023-24 "**Linear Look**" package (dark bg + purple glows + glass + thin borders + bento) is
  now catalogued startup-generic. Counter-current: brutalist/industrial edge — visible grid, mono
  labels, high-contrast blocks.
- **Texture**: glassmorphism demoted to accent-only (contrast + FPS costs); current kit = hairline
  rules, subtle grain/noise, gradient borders used sparingly.
- **Motion**: micro-interactions and CSS View Transitions ship; kinetic-type heroes and heavy WebGL
  demo well and ship badly. (Also binding here: owner's no-animation stance outside approved cases,
  and `prefers-reduced-motion` support everywhere.)

## 4. Implications chosen for the three Nexus drafts

1. Pair one workhorse sans with a **real monospace used semantically** (codes, units, stats, labels) —
   Nexus already speaks in course codes (ELX 205) and machine-verified numbers; lean in.
2. Seriousness through **numbers-with-units and honest telemetry** (the 199/528 tracker is an asset —
   design it up, Samsara-style, instead of hiding it in a gray bar).
3. The computed SVG diagrams are Nexus's "product screenshots" — give them the hero treatment
   industrial sites give real telemetry.
4. One saturated hue on a disciplined neutral base per draft; no multi-accent salads, no glow package.
5. Course pages: the **document-archive register** (OCW) for the editorial draft; the **learning-
   console register** (Khan dashboard/Linear docs curation) for the app draft; the **operator/HMI
   register** (Ignition/Samsara/iX) for the industrial draft.
6. Search deserves ⌘K-class prominence on a 528-lesson catalog.
7. Honest depth labels stay in ALL drafts (integrity floor) — styled as status chips/telemetry, not
   apologies. No cost/"free" mentions anywhere (binding owner rule).
