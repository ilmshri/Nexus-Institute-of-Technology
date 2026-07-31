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

## 5. Owner-referenced bilingual model: itqan.edu.sa (added 2026-07-25)

Owner directive 2026-07-25: use ITQAN Institute's site as a design reference, especially its
English/Arabic handling. Reference = pattern study only; no assets or copy are copied. (Unrelated
to the naming track: the ITQAN name-collision finding there stands.)

Verified firsthand by browser inspection, 2026-07-25:
- **Stack**: WordPress 7.0.2 + Elementor (irrelevant to us — we stay static).
- **Type**: Gill Sans (EN) + **GE SS** (AR) — one humanist sans paired with the classic Gulf
  corporate Arabic face; identical hierarchy and weights in both languages.
- **Color**: one deep institutional green `#005B2E` on white; flat, no gradients.
- **Bilingual architecture**: SEPARATE URL TREES `/en/` + `/ar/` (WPML pattern), document-level
  `lang` + `dir=rtl`; **full 1:1 content parity** (every homepage section translated, same order);
  complete RTL mirror (logo docks right, nav reverses, CTA pill flips side); language toggle
  labeled in the DESTINATION language ("العربية" on EN pages; "English" + flag on AR pages).
- **Logo lockup is bilingual by construction**: Arabic إتقان + Latin ITQAN stacked in one mark,
  dual descriptor lines beneath (AR full institutional name + EN full name). One logo serves both
  trees unchanged — no logo swapping.
- **Homepage register**: hero video, mission headlines, program cards, career pitch, news,
  stakeholders/accreditations bands, count-up counters.

ADOPT when the Arabic layer returns (all gated with that owner decision):
1. **Emit-two-trees** bilingual architecture from `nexus_build.py` (`/` + `/ar/`) — replaces the
   retired in-page data-ar/localStorage toggle; real per-language URLs, shareable, honest.
2. Toggle labeled in the destination language — the owner's "non-confusing" bilingual instinct.
3. **Bilingual logo lockup** (Latin brand word + designed Arabic script line + dual descriptors) —
   the owner's stated wordmark treatment, validated in the wild here.
4. A deliberate AR type partner for the winning draft's EN face (IBM Plex Sans Arabic earmarked;
   final pairing chosen per-draft at apply time).
5. 1:1 parity discipline (the standing BILINGUAL RULE already requires it).

NOT adopted: their green (palette comes from the round-2 winner), photography-led content
(vector-only rule), the WordPress stack.

## 6. Transition craft — verified reference study (added 2026-07-31, design session)

Method: every URL below was fetched live this session (HTTP status recorded); where a technique
is claimed, the marker (`@view-transition`, `view-transition-name`, `animation-timeline`,
`@starting-style`, `prefers-reduced-motion`) was found in the fetched CSS/HTML itself.
Existing sections above are untouched.

### Browser ground truth (mid-2026; fetched from MDN + MDN browser-compat-data + caniuse raw JSON)

- **Cross-document View Transitions** (`@view-transition` — the technique that matters for our
  static MPA): Chrome/Edge 126+, Safari & iOS Safari 18.2+. **Firefox stable through 155: NOT
  supported** (partial = same-document only; open bug bugzil.la/1860854). Not Baseline.
- **Same-document** `document.startViewTransition`: Chrome 111+, Safari 18+, Firefox 144+ —
  Baseline across all three engines.
- **Scroll-driven animations** (`animation-timeline`): Chrome 115+, Safari 26+; Firefox stable
  not shipped (Nightly flag only).
- Implication: cross-document view transitions are a pure progressive enhancement here —
  Firefox users keep instant plain navigation, zero breakage, zero JS. Scroll-driven animation
  stays decorative-only. (Sources fetched: developer.mozilla.org View_Transition_API and
  @view-transition pages; raw.githubusercontent.com mdn/browser-compat-data
  css/at-rules/view-transition.json, api/Document.json, css/properties/animation-timeline.json;
  Fyrd/caniuse features-json cross-document-view-transitions.json + view-transitions.json;
  web-platform-dx/web-features cross-document-view-transitions.yml + scroll-driven-animations.yml.)

### Reference sites (all fetched live 2026-07-31)

| Site | Register | What it does well for us | Technique (verified in fetched source) | Reduced motion |
|---|---|---|---|---|
| worksinprogress.co | editorial | Best brand match: classical print-soul magazine; gentle whole-page cross-fade between pages + Speculation-Rules prefetch so a static MPA feels instant | `@view-transition{navigation:auto}` in Layout CSS + `<script type="speculationrules">` in HTML; Astro static | Yes (3 rules) |
| daverupert.com | editorial | Canonical persistent-element morph: masthead logo carries `view-transition-name`, glides between sizes on every navigation — our curriculum→course→lesson continuity pattern | Cross-doc VT + named morph + spring easing on `::view-transition-group` + `@starting-style` | Yes — morph downgraded to plain fade |
| thesession.org | archive | Tens of thousands of server-rendered pages (closest scale analogy to our 1,262); cross-doc VT as pure progressive enhancement, calm register | `@view-transition` + tuned `::view-transition-old/new`; plain MPA, no framework | Yes (3 rules) |
| dladukedev.com | editorial | Cleanest minimal build: post title/date in the index morphs into the article header — exactly our course-syllabus-row → lesson-H1 journey | Cross-doc VT + 12 `view-transition-name`s; 11ty static | Not determinable from fetch |
| utilitybend.com | editorial | Working catalogue of all four techniques composed in one restrained file, incl. tab-switch analogs via `@starting-style` instead of JS | `@view-transition`, old/new/group pseudo-elements, `@starting-style`, `animation-timeline` all in one Layout CSS | Yes (7 rules) |
| una.im | editorial | **The gating pattern to copy verbatim**: `@media not (prefers-reduced-motion: reduce){@view-transition{navigation:auto}}` — motion-sensitive readers never opt in at all | Cross-doc VT inside a `not (prefers-reduced-motion)` media query; sparse `animation-timeline` | Structurally yes |
| nerdy.dev | editorial | Technique ceiling, not register model: 636 auto-generated `view-transition-name`s prove per-lesson names can be stamped mechanically at build time | VT API (CSS + `startViewTransition`), `@starting-style`, scroll-driven | Yes (3 rules) |
| events-3bg.pages.dev/jotter | documentation | The community's canonical VT pattern cookbook, itself a static docs MPA: sidebar/header hold still, content pane cross-fades — our lesson→next-lesson shape | Cross-doc VT on Astro/Starlight docs shell | Yes (3 rules) |
| ocw.mit.edu | education | The honest baseline: zero page transitions, sub-second navigation, 19 reduced-motion guards — speed and stillness as the default to layer quiet enhancement onto | Plain CSS; restraint by omission (Yale/Princeton/Harvard homepages also fetched — no motion craft at all) | Yes (19 rules) |
| rijksmuseum.nl/en | museum | Collection→artwork journey (mirrors curriculum→lesson) done with short plain-CSS fades; most motion-accessibility-disciplined production site found | Plain CSS only; craft is duration/easing restraint | Yes (43 rules) |
| joshwcomeau.com | education | Teaching widgets animate, page chrome stays still — the right in-page register for our tabs; "motion as meaning, never decoration" | `@starting-style` (5), `animation-timeline` (2), one `view-transition-name`; Next.js so page-nav model translates less directly | JS-handled; not confirmable from fetch |
| 11ty.dev/docs | documentation | Control reference: effortless feel is 80% payload discipline + stable layout + instant static navigation; VT is the last 20%, not the foundation | Plain CSS + reduced-motion guards | Yes |

### Read against what MechEd already ships (nexus.css:835-845)

We already have `@view-transition{navigation:auto}` with .18s/.26s root fades, disabled under
reduced motion. The craft gap the references expose, in order of payoff: (1) named-element
continuity (breadcrumb/title morphs — daverupert/dladukedev pattern); (2) Speculation-Rules
prefetch (worksinprogress pattern) so lesson→next-lesson is already loaded; (3) una.im's
opt-in-only-without-reduced-motion gating (stronger than our current disable-after-the-fact);
(4) in-page tab switches via `@starting-style` (utilitybend pattern) — currently our tabs snap.

## 7. Institutional logo reference board (added 2026-07-31, design session)

All URLs fetched live this session, HTTP 200 confirmed. Two buckets per the owner's two
possible registers.

### Bucket A — reads "official educational institution"

| Mark | URL | Why it holds up |
|---|---|---|
| IMechE | imeche.org | Pure wordmark — the institution's name IS the mark; nothing to degrade at small sizes; closest domain-mate to MechEd |
| ETH Zurich | ethz.ch/en.html | Acronym-led grotesque wordmark backed by the spelled-out name; typesetting discipline alone signals rigor |
| MIT | mit.edu | Lettermark built from plain geometric bars; reduces to rectangles, survives one-color/tiny/engraved |
| Imperial College London | imperial.ac.uk | Single-color all-type wordmark, no crest — dropping heraldry reads as more elite, not less |
| ASME | asme.org | Acronym mark + spelled-out name in support — the standard dual-register pattern for engineering authority |
| University of Cambridge | cam.ac.uk | Even the most heraldic institution leads its digital header with a clean shield-free wordmark |
| KFUPM | kfupm.edu.sa | Gulf technical university with explicit per-language logo variants (`kfupm_logo_en`) — a managed bilingual identity system |
| IET | theiet.org | Acronym + full name in the lockup's second register: compact mark, chartered gravitas |

### Bucket B — reads "quietly elegant / exclusive"

| Mark | URL | Why it holds up |
|---|---|---|
| The Royal Society | royalsociety.org | Definite-article wordmark, classical setting; crest held in reserve rather than forced small |
| Princeton University Press | press.princeton.edu | No device at all — restrained typography and hierarchy as the confidence signal |
| Yale University Press | yalebooks.yale.edu | Wordmark set in the institution's own typeface — the type system itself is the brand (directly relevant to our Source Serif system) |
| The Royal Institution | rigb.org | 200 years compressed to a two-letter "Ri" monogram — the template for a quiet short-form mark |
| Qatar National Library | qnl.qa/en | Strongest regional model: one thin-line device + Arabic-over-English stacked wordmark, single color (logo PNG downloaded and inspected) |
| Bodleian Libraries | bodleian.ox.ac.uk | Wordmark first, university crest demoted to the footer — the hierarchy that keeps serious marks usable small |

### itqan.edu.sa lockup, dissected from the actual SVG (fetched + rendered)

Downloaded https://itqan.edu.sa/wp-content/uploads/2021/06/logo.svg (48 KB) and rendered it.
One two-color SVG serves BOTH language trees unchanged: (1) Arabic brand 'إتــقــان' in warm
gray, letterspaced with kashida elongation; (2) Latin 'ITQAN' beneath in wide letterspaced
light caps, optically width-matched to the Arabic; (3) a shared-baseline third tier
'INSTITUTE' + 'معهد' joined by a thin rule — dual-script descriptor on one line; (4) a single
flat green faceted-shield device to one side; (5) two full-width formal-name descriptor lines
(AR kashida-justified above EN) beneath. Pattern confirmed: Latin brand + Arabic script line as
equals in one neutral color, dual descriptors, one restrained device — never per-language logos.

### Type licences, verified from the licence texts themselves

Source Serif 4 and Source Sans 3 are both **SIL OFL 1.1** (fetched:
raw.githubusercontent.com/adobe-fonts/source-serif/main/LICENSE.md and
…/source-sans/main/LICENSE.md; corroborated by fonts.google.com metadata endpoints reporting
license "ofl"). The fetched OFL text permits commercial use and modification of letterforms,
and states the share-alike requirement "does not apply to any document created using the
fonts" — outlined logo artwork is such a document, so a MechEd wordmark cut from these faces
carries **no licence obligation at all**. Only constraints: a modified *font file* may not be
named "Source", must stay OFL, and font files can't be sold standalone. A wordmark drawn from
the licensed faces and hand-corrected in vector is free, immediate, fully owned, and
consistent with the site by construction.
