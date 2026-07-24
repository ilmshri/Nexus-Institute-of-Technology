# NEXUS INSTITUTE OF TECHNOLOGY — MASTER BRIEF (final authority)

This file is the continuation contract for any model or person working on this
repository. Where any other instruction differs from this brief, this brief wins.

PROJECT IDENTITY (owner directive, 2026-07-18, permanent): this project is
**Nexus Institute of Technology** — live at https://nexuskw.github.io/, repo
github.com/nexuskw/nexuskw.github.io, generator `nexus_build.py`. All
owner-facing output, documents, and instructions use the name "Nexus" ONLY.
The ledger below is the historical decision record: entries predating the
rebrand keep their original wording verbatim (deleting or rewording history
is prohibited — it is the audit trail). Where old entries conflict with
newer ones, the newer entry wins, as always.

## FINAL DECISIONS (from the project owner)

1. Real hosted domain — build as a static site for GitHub Pages/Cloudflare Pages
   deployment, haruchika design language, real video embeds now allowed.
2. Full lecture depth for the agreed Core 60 lessons, structured-notes depth for
   the rest of the 48-course catalog.
3. Audience is a mechanical maintenance engineer transitioning into manufacturing
   with no manufacturing background — reframe as a transition pathway and write
   the career section tactically for that profile.

## MASTER BRIEF (verbatim)

PROJECT: Public educational website for a mechanical maintenance engineer
transitioning into manufacturing (no manufacturing background). Target roles:
Reliability, Asset Integrity, Production/Operations, Maintenance Planning.

ARCHITECTURE: Static site generator — ONE haruchika-style template +
build.py + curriculum.json (all courses/lessons as data; script emits every
page). Deploy to GitHub Pages free URL immediately; custom domain later.
FIRST COMMIT = CLAUDE.md containing this entire brief (model-agnostic
continuation insurance).

DESIGN: haruchika.co.jp language — paper-white base, near-black ink, steel-
gray secondary; serif editorial headlines, spaced small-caps "SUN DEVIL
FACTORY" wordmark (only branding); numbered sections (01,02…), hairline
rules, generous whitespace; full-bleed licensed photos, scroll reveals
(IntersectionObserver), hover captions; English only; no edtech look.

CONTENT TIERS:
- Tier 1 (today: casting lecture only, gold standard): objectives; full
  derivations; 2 worked examples with units; misconceptions; check-your-
  understanding with hidden answer; refresher blocks; Kuwait tie-in.
- Tier 2 (Core 60, ~400-word study guides, batches of 8-10): objectives,
  key equations w/ named textbook source, 1 condensed worked example,
  misconceptions, Kuwait line, course-level video link.
- Tier 3 (all remaining lessons): title + 3-sentence scope + "taught from:
  [textbook, chapter]" — generated from curriculum.json.

CORE 60 (Tier 2), by block:
A-Processes(16): plant taxonomy; casting solidification/gating/risers(=Tier1);
casting practice+defects; continuous casting(Kuwait Steel); rolling; forging;
extrusion+wire drawing(Gulf Cable); sheet metal+springback(Kirby); machining
theory; turning/milling/drilling; grinding; welding processes; weld
metallurgy/HAZ; weld defects+WPS/PQR; NDT PT/MT/UT/RT; plastics/packaging(KDD).
B-Fundamentals(8): stress-strain; Fe-C+heat treatment; fatigue/fracture/creep;
corrosion in Gulf; transient conduction; heat exchangers; Bernoulli/pipe flow/
pump curves; utilities thermo (steam/air/refrigeration).
C-Reliability(8): failure patterns+P-F; Weibull; system reliability;
FMEA/FMECA; RCM principles; RCM implementation+RCA; bad actors+KPIs;
building a plant reliability program.
D-Condition Monitoring(8): PdM strategy+P-F economics; vibration fundamentals;
measurement+FFT; spectra I (unbalance/misalignment/looseness); spectra II
(bearings/gears); thermography; oil analysis; ultrasound+MCA+routes.
E-Rotating Equipment(8): pump theory+curves; system curves/NPSH/cavitation;
PD pumps; compressors; mechanical seals; bearings+lubrication; couplings/
alignment/balancing; gearboxes+failure modes.
F-Planning(8): work management flow; job plans; scheduling; backlog+KPIs;
spares+BOMs; CMMS/SAP PM; turnarounds; budgeting.
G-Automation(4): PLC/ladder essentials; sensors on a line; P&ID reading;
OEE/SCADA/production data.

FULL CATALOG (Tier 3 fill, 48 courses, ~522 lessons, generate lesson titles):
Y1S1: Math I, Drawing&CAD, Statics, Materials Sci I, Manuf Processes I
(casting/bulk forming), Engineering Computing.
Y1S2: Math II, Dynamics, Materials Sci II, Manuf Processes II (machining/
joining), Thermodynamics I, Electrical Fundamentals.
Y2S1: Strength of Materials, Thermo II, Fluid Mechanics, Metrology&QC,
Electronics&Sensors, Engineering Statistics.
Y2S2: Machine Design I, Kinematics&Dynamics of Machinery, Heat Transfer,
Manuf Processes III (sheet/plastics/additive), PLC Fundamentals I,
Industrial Safety.
Y3S1: Machine Design II, Control Systems I, PLC II & Industrial Networks,
Hydraulics&Pneumatics, Welding Engineering&NDT, Maintenance Engineering
Fundamentals.
Y3S2: Vibrations, Instrumentation&Process Control, Industrial Robotics,
Reliability Engineering I, Corrosion&Degradation, Production Planning&Control.
Y4S1: Rotating Equipment, Asset Integrity Mgmt, Condition Monitoring&PdM,
SCADA/DCS/IIoT, Lean&Six Sigma, Engineering Economics&PM.
Y4S2: Smart Manufacturing&Digital Twin, Maintenance Planning/Turnarounds/
CMMS, Pressure Equipment&Piping, HSE (NEBOSH-aligned), Reliability II,
Capstone.

SOURCES (only these; cite title+author; verify edition or omit it; never
fabricate; no Wikipedia/blogs): Groover Fundamentals of Modern Manufacturing;
Kalpakjian&Schmid Manufacturing Engineering&Technology; Black&Kohser
DeGarmo's; Flemings Solidification Processing; Campbell Complete Casting
Handbook; ASM Handbook Vol 15 Casting; Çengel&Ghajar Heat and Mass Transfer;
Çengel&Cimbala Fluid Mechanics; Callister&Rethwisch Materials Science;
Making Shaping and Treating of Steel (AISE); MIT OCW; NPTEL.

KUWAIT TIE-INS (only these companies; name process/equipment; never invent
plant data — label numbers "representative"): Kuwait Steel (EAF, billet
caster, rolling mill), Gulf Cable (wire drawing/stranding/extrusion), Kirby
(steel fabrication/welding), EQUATE (rotating equipment/asset integrity),
KDD/Petra (filling/packaging/utilities), HEISCO (fabrication/NDT/services).

MEDIA: ONE pool of ~8 openly-licensed photos (Wikimedia Commons; verify
license; honest captions — "representative example: X" when facility
unknown) reused site-wide. Videos today = course-level MIT OCW/NPTEL links
only, verified live. No fabricated URLs ever.

CAREER SECTION (full, today, tactical): maintenance→manufacturing CV
translation table; entry via maintenance/reliability roles at the six
companies first, production later; certs: CMRP flagship + ISO 18436 Cat I
vibration, API 510/570/653 flagged as experience-gated; KSE registration
note; interview topics mapped to Core 60; 12-month action plan.

EXECUTION: Hour 1 = repo, CLAUDE.md(this brief), template+script,
curriculum.json, career section, DEPLOY (public). Hour 2 = casting Tier-1
lecture, Core 60 study guides in batches, photo pool, video links, push
incrementally. Never trade correctness for speed — cut breadth instead.

## REPO ORIENTATION (how to continue)

- `build.py` — zero-dependency Python 3 generator. Run `python3 build.py`;
  output goes to `docs/` (GitHub Pages serves from /docs on main).
- `data/y{1..4}s{1,2}.json` — the curriculum: 48 courses, 522 lessons.
  Lesson fields: `n`, `t` (title), `tier` (1/2/3), `scope`, `src`,
  optional `core60` (block tag like "A4"), optional `content` (fragment id
  in content/lessons/), optional `kuwait`.
- `content/lessons/<id>.html` — body fragments for Tier 1/2 lesson pages.
  Fragment id convention: `<semester>-<course-id>-<lesson number two digits>`.
- `content/pages/` — home and career page fragments.
- `assets/` — site.css, site.js, img/ (photo pool with credits in
  `assets/img/CREDITS.md`).
- Preview locally: `python3 -m http.server -d docs 8000`.

### Content status ledger (update when you add content)

- COMPANY-NAMES RULE v2 (owner, 2026-07-17 PM — supersedes the blanket ban):
  (a) ACADEMIC content (lessons, lectures, examples, quizzes, foundations):
  STRICTLY NO specific company names — industrial examples stay universal,
  objective, representative. (b) CAREER PATHS & EMPLOYMENT section: real,
  specific company names are ALLOWED AND ENCOURAGED (Kuwait companies such
  as EQUATE, Kuwait Steel, KDD, and global industrial firms) for job
  placements, career trajectories, CV building, interview preparation.
  Consequence: the Career page rewrite question is resolved (keep/expand
  real companies there); the 44 older lessons + 8 lecture fragments with
  company-named applied cases still need the ACADEMIC scrub in Phase 2.
- CURRICULUM MAP APPROVED & EXECUTED (owner, 2026-07-17 PM; commit
  a3d12da): university-grade 48-class structure researched from
  MIT/ASU/Caltech/TAMU BSME catalogs. NEW: physics-1 (PHY 107, Y1S1,
  8.01SC-modeled) and math-3 (MTH 207, Y2S1, DiffEq+LinAlg, 18.03-modeled),
  full 11-lesson syllabi authored, preview arithmetic machine-verified.
  MERGED: production-planning+lean-six-sigma → production-lean (PPL 405,
  Y4S1); asset-integrity+pressure-equipment → pressure-integrity (PAI 453,
  Y4S2) — 22→11 lesson selections, overlapping stubs fused, scopes kept.
  MOVED (12): mfg-1→y1s2, mfg-2→y2s1, thermo-2→y2s2, metrology→y2s2,
  plc-1→y3s1, safety→y3s1, vibrations→y3s1 (now BEFORE controls, TAMU
  MEEN 363→364 pattern), controls-1→y3s2 (retitled "System Dynamics &
  Control I"), plc-2→y3s2, maintenance-fundamentals→y3s2, robotics→y4s1.
  Grid invariant intact: 48×11=528. Casting content moved intact with
  mfg-1 (fragment ids are semester-agnostic; coverage stayed 52/528).
- CAREER MODULE MECHANISM (owner Phase-2 rule, 2026-07-17 PM): per-course
  "Career outlook" block on the COURSE page (course dict "career" HTML
  field; renderer + .career-block CSS live). This is the ONLY place company
  names may appear — academic tabs stay company-free (verified by scan in
  the content pipeline). BROAD-SPECTRUM ROTATION (binding): rotate sectors
  per course from {Construction/Real Estate, FMCG/Food, Infrastructure/
  Utilities, Automotive/Heavy Equipment, Specialized Mfg, Global OEM},
  always mixing local Kuwaiti / regional / global employers, tailored to
  the course. USED SO FAR: math-1 = Construction (Mabanee) + FMCG (KDD) +
  Global OEM (Siemens). Next courses must rotate to unused sectors.
- CHECKPOINT Y1S1C1 (MTH 101 math-1) EN CORE DONE (2026-07-17 PM): all 11
  lessons migrated to the strict architecture — lectures expanded to
  500-1000 words with "working method" sections; foundations converted to
  glossary TABLES (Term|Equation|When to use); Examples and Quiz = 3 solve
  + 5 submit-graded MC per lesson (88 items: 22 legacy solves converted,
  11 new solves, 33 drafts re-verified from journal, 22 new MCs — ALL
  numeric answers machine-verified pre-write; drafts for drawing-cad remain
  unverified in drafts/). Company-free scan of academic content PASS.
  STILL OWED for full Y1S1C1: Arabic lesson bodies (honest AR notice still
  shows), Library texts/certs curation.
  Sector rotation and quiz pipeline are the template for Y1S1C2 onward.
- Y1S1 LIBRARY PATCH (owner directive, 2026-07-17 PM; in progress):
  per-lesson "video" field now supported in the lesson data — dict
  {id,title,channel} embeds (channel must pass APPROVED_CHANNELS; build
  asserts), the string "none" renders the honest "No relevant video found
  in the approved channel list" marker. EVERY id is oEmbed-verified
  (author_name + title checked via youtube.com/oembed) BEFORE entry — no
  invented ids, ever. DONE: math-1 — 10 embeds from MIT OpenCourseWare
  (18.01 Fall 2007 Lec 1,2,4,6,11,16,18,23,30,38, ids sourced from the
  official OCW video gallery and individually oEmbed-verified) + L1 marked
  "none" (no units/dimensional-analysis lecture exists in the approved
  channels). DONE (session 2, commit aa44b4f): statics — 11 embeds, Jeff
  Hanson statics series (playlist bulk-extracted via browser pass; ids
  oEmbed-verified; best-fit mapping per owner rule: Hanson lessons
  4/21/18/16/29/48/53/57/62/37/67 → our L1–L11). computing — 11 embeds,
  MIT OCW 6.0001 (Lec 1,3,2,4,7,5,10) + 6.0002 (Lec 5,9,6,15), all
  oEmbed-verified; L7/L8/L11 are declared best-fits, titled honestly.
  Site embeds 32.
- HUMAN-IN-THE-LOOP VIDEO PROTOCOL (owner, Phase-3 + Global Directive,
  2026-07-17/18 — supersedes autonomous embedding): ALL video candidates
  are PROPOSED in table format (Lesson | Primary | Arabic Supplemental |
  Justification), oEmbed-verified BEFORE proposal, and embedded only after
  the owner's explicit APPROVE per row. CHANNEL LIST v2 (primary/English
  technical, enforced in APPROVED_CHANNELS): original 15 + Engineering
  Deciphered, Randall Manteufel, 3Blue1Brown, Less Boring Lectures,
  Husam's Mech Vision, Khan Academy. ARABIC RULE: Arabic channels
  (قناة د.محمد شايع — thermo/heat-transfer, 550+ lectures; Ala Hijazi —
  GJU, mechanical drawing/statics, channel URL still unverified) are
  SUPPLEMENTAL ONLY — never the primary frame; a dedicated
  "Supplemental/Arabic Resources" renderer block is still to be built
  before the first Arabic approval can ship.
- CHECKPOINT: STATICS EDUCATIONAL UNIT COMPLETE (2026-07-18): first course
  shipped under the approved Unit template. All 11 lessons: lectures
  500-1000w (working-method sections added), foundations converted to
  glossary TABLES, quizzes upgraded [s,m,m,s,m] → [s,s,s,m,m,m,m,m] (+11
  authored solves, +22 authored MCs — every number Python-verified
  pre-write; the 55 legacy items kept verbatim), applied-case vignettes
  scrubbed company-free (11 replacements: steel mill / cable plant /
  fabricated steel / petrochemical plant / dairy filling hall /
  fabrication yard), Library = 11 approved Hanson embeds. E2
  "Supplemental/Arabic Resources" renderer BUILT (lesson "arabic" list →
  link cards under dedicated header; renders only when approved resources
  exist — none approved yet). Career module attached (rotation: 
  Construction/Contracting–Asico, Automotive & Heavy Equipment,
  Specialized Mfg–Gulf Glass; distinct from math-1's sectors). NEXT per
  approved order: materials-1 → physics-1 → computing → drawing-cad →
  Y1S2 stream.
- MASS PRODUCTION MODE (owner Master Directive, 2026-07-18 — supersedes
  the per-row video approval loop): the Chief Architect authors curriculum
  autonomously. BINDING GATES UNCHANGED: 4-tab Educational Unit per lesson
  (500-1000w §1-§4 lecture w/ working method; prerequisites + glossary
  TABLE; 3 solves + 5 MCQs Python-verified pre-write; Library = E1 primary
  English embed oEmbed-verified from the approved channel list, E2 Arabic
  link-cards (supplemental only), E3/E4 placeholders); company-free scrub;
  career-sector rotation per course. WORKFLOW: remaining gaps in current
  courses → Y1S1 → Y1S2 → Y2S1 onward; report per course; no lesson is
  Done below full Unit; video-only lessons get retrofitted. No more
  per-step permission requests — integrity gates are the authority.
- CHECKPOINT: PHYSICS-1 EDUCATIONAL UNIT COMPLETE (2026-07-18): FIRST
  FRESH-AUTHORED course under Mass Production Mode — no legacy content
  existed; all 11 lessons written from scratch to the Unit template:
  §1-§4 lectures 500-1000w (units/vectors, 1D+2D kinematics, Newton's
  laws + applications, work-energy, conservation, momentum, rotation I/II,
  oscillations — each with a working-method section), glossary TABLES,
  quizzes 3 solves + 5 MCs per lesson (88 items, ~60 numeric checks
  Python-verified pre-write), Library = 11 approved embeds already in
  place (ED/Khan/MIT). Company-free by construction. Career module
  (rotation: FMCG-KDD, Automotive & Heavy Equipment, Global OEM-Siemens
  drives — trio distinct from all previous courses). Coverage 52→63/528
  (12%). Commits: 9e9006c (L1-4), 96e825c (L5-8), this one (L9-11).
  Y1S1 Unit scoreboard: math-1 ✓ statics ✓ materials-1 ✓ physics-1 ✓;
  NEXT per approved order: computing → drawing-cad (incl. re-verifying its
  drafts) → Y1S2 stream.
- MAINTENANCE PHASE (owner, 2026-07-18 — content pipeline PAUSED after the
  computing checkpoint; drawing-cad stays next in queue, untouched): pivot
  to site maintenance & structure organization. SHIPPED THIS PHASE:
  PROJECT_MAP.md (full repo audit; every file classified Editable Content
  vs System Infrastructure/do-not-touch; no files renamed — names are
  load-bearing wiring, documented instead) + OWNER_MANUAL.md (owner-facing
  edit cycle, JSON lesson/quiz templates, catalog do's/don'ts, failure
  table, git recovery). PENDING (gated on owner): design refinement —
  owner will finalize visual style, then layout suggestions; NO animations
  per explicit owner order.
- NEXUS-ONLY IDENTITY PURGE (owner CRITICAL directive, 2026-07-18,
  permanent — see PROJECT IDENTITY at the top of this file): all owner-
  facing output/docs use "Nexus" exclusively. EXECUTED: table.sdf CSS class
  → table.nx-table (nexus.css 6 rules + career.html/career-ar.html 3 tables
  each; styling verified by computed-style check on the rendered page);
  launch configs sdf-docs → nexus-docs (project + session level, path
  updated); build.py docstring + nexus_build.py comment retitled neutral
  ("previous-generation library"); README.md + DEPLOY.md rewritten
  Nexus-current (old build/deploy steps were stale); PROJECT_MAP.md +
  OWNER_MANUAL.md re-issued Nexus-exclusive; local folder renamed
  sun-devil-factory → nexus-institute (git/remote unaffected; verified).
  Emitted docs/ scanned: ZERO old-brand residue. NOT purged, by rule:
  ledger history below (audit trail, verbatim), dead-path strings inside
  build.py (inert library internals), archived first-generation assets.
- HOMEPAGE WELCOME ANIMATION v2 (owner orders 2026-07-18 — partially lifts
  the earlier "no animations" hold, for this feature only; broader design
  refinement remains gated on the owner's visual-style decision): FINAL
  STATE per owner iteration: gear motif DISCARDED (.nx-hero .bg
  display:none — markup kept, CSS-off, reversible; nx-turn/nx-breathe
  removed), hero text stack CENTERED (EN + AR; text-align:center +
  meta justify-content:center, direction-neutral), banner SHINE sweep
  (.nx-hero::after skewed amber-white gradient band, nx-shine 5.5s
  ease-in-out infinite), staggered nx-rise entrance KEPT (eyebrow .1s →
  h1 .28s → sub .46s → meta .64s, translateY only, RTL-safe). All
  animations disabled under prefers-reduced-motion (shine ::after
  display:none). Scope: .nx-hero, homepage only. Verified in-browser:
  centering both languages, gear off, shine band position sampled
  moving (~33px/1.2s). Earlier v1 (rotating gear at 60s/rev) superseded
  same-day by owner order "cancel this. discard the gear."
- YEAR 2-4 AUTHORING STARTED (owner order 2026-07-18: full Educational
  Units for all Y2S1-Y4S2 lessons + videos in empty lessons; 396 lessons
  total, multi-session). BATCH 1 = math-3 (MTH 207) L1-L4: fresh-authored
  units — 500-600w §1-§5 lectures (first-order separable/linear +
  integrating-factor DERIVATION; first-order modelling w/ time constants;
  second-order homogeneous + discriminant/ωn/ζ; nonhomogeneous +
  undetermined coefficients), glossary TABLES, 3 solves + 5 MCs each (24
  items, every number Python-verified pre-write: e^2, y=2+3e^-2,
  Newton-cooling 62.5°C, half-life 13.9min, RC τ=0.1s, tank τ=40min,
  roots -2/-3 & -1±2i, ωn=10, c_c=20, ζ=0.4, xp=5, ramp a=1/b=-1.5,
  amp 0.447). Library already 11/11 approved MIT OCW embeds. Career
  attached (rotation: Automotive-Toyota, Aerospace-Airbus, Industrial
  controls-Rockwell — distinct trio). Company-free scan PASS. Render
  verified in-browser: L3 quiz 5/5, glossary, MathJax 105, embed, zero §.
  Coverage 74→78/528 (15%).
- BREADTH MODE (owner directive 2026-07-18: "prioritize breadth" — one
  starter batch per course across more of Year 2, plus "add whatever
  parts you finish to each lesson at the same time" = incremental merge).
  BATCH 2 = strength (SOM 201) L1-L4 fresh units: 500-540w §1-§5 lectures
  (axial stress/strain + Hooke + FoS; series/indeterminate + thermal
  stress; torsion + power-torque; bending + section modulus + shear),
  glossary TABLES, 24 Python-verified quiz items (σ=204MPa, δ=2.55mm,
  FoS=1.56, εT=600µε, σth=120MPa, T=95.5N·m, τ=7.6MPa, J∝d⁴ ×16,
  I=4.17e6mm⁴, S=83333mm³, σ=120MPa). Library already 11/11 approved
  Hanson MoM embeds (Wave D). Career attached (Construction-Bechtel,
  Process-Shell, Automotive-Caterpillar — distinct trio). Company-free
  scan PASS; render-gate spot check PASS (§ none, glossary, 8 quiz,
  embed, no company names in academic tabs). Coverage 78→82/528 (16%).
  Y2S1 status: math-3 4/11, strength 4/11 authored; both have full
  approved videos. NEXT (empty-video courses): fluids/statistics/etc.
  need the real per-video verification pass under video-policy v3.
- STATISTICS (STS 206) COURSE COMPLETE (2026-07-19): second fully-complete
  Year-2 course. All 11 lessons full Educational Units — 500-1000w lectures,
  glossary tables, 3 solve + 5 MC (every number Python-verified: descriptive
  stats, probability rules, binomial/Poisson, normal/z/empirical-rule,
  SE/CLT, confidence intervals, z-test/p-value, least-squares regression/R²,
  2^k factorial DOE, reliability R(t)/MTBF/series-parallel, malpractice/
  multiple-comparisons/base-rate) + approved videos + alternatives + texts.
  Company-free PASS. Coverage 93→104/528 (20% milestone). Commits 3aa00b3,
  e4751a9, 0b47408. STILL OWED for the directive: math-3 L5-L11 + L2/L3/L4
  word-count top-up (last video-bearing course needing content).
- FLUIDS (FLD 203) COURSE COMPLETE (owner directive "every video lesson
  gets the full unit", 2026-07-19): all 11 lessons now full Educational
  Units — lecture (500-1000w §1-§4), glossary-table foundations, 3 solve +
  5 MC quiz (every number Python-verified pre-write), plus the already-
  approved video embed + alternatives + canonical textbooks. Batches:
  L1-4 (properties/statics/Reynolds/Bernoulli), L5-8 (momentum/dim-analysis/
  friction-Moody/networks-valves), L9-11 (flow-measurement/turbomachinery-
  NPSH/compressible). Company-free PASS. First fully-complete Year-2 course.
  Coverage 74→93/528 (18%). Commits 66cad73, f960430, a0d6947. STILL OWED
  for the directive: statistics content (11 lessons, videos already in),
  math-3 L5-L11 + L2/L3/L4 word-count top-up.
- YEAR-2 VIDEO + CONTENT PUSH (owner, 2026-07-18/19): dual track. VIDEOS
  (owner: embed-then-report, batches of 3, primary embed + verified
  alternatives, finish all Year-2 empty-video courses): FLUIDS 11/11
  (4 approved + 7 v3) + 32 alt links; STATISTICS 11/11 (StatQuest-tier,
  all v3) + 19 alt links. New Library renderer "Alternative videos"
  (primary embed + link list; each id oEmbed-verified real). Remaining
  Y2 empty-video courses: electronics-sensors, mfg-processes-2, all six
  Y2S2. CONTENT: math-3 (MTH 207) L1-L4 authored (first-order ODEs,
  modelling, 2nd-order homogeneous, forced response) — glossary tables,
  3 solve + 5 MC each, ALL arithmetic Python-verified pre-write;
  company-free PASS; renders + counts (coverage 78→82). NOTE (polish
  owed): math-3 L2/L3/L4 lectures 484/398/450 words, slightly under the
  500-word floor — top-up owed; L1 547 OK. Video approval list was
  presented to owner and approved (fluids L1-L3 approve-all + alternates).
  OWNER APPROVED (2026-07-19): the full fluids (11/11) + statistics (11/11)
  video sets with all alternatives, AND math-3 L1-L4 content — confirmed,
  no longer provisional. math-3 L2/L3/L4 lecture word-count top-up still owed.
- VIDEO-POLICY v3 GATE + FLUIDS VIDEOS (owner directive "keep spreading
  videos", 2026-07-18): build gate relaxed — embed_card() now takes
  allow=; a lesson video dict with "verified":true embeds from ANY channel
  (channel name always shown for transparency); approved channels still
  auto-pass. FLUIDS (FLD 203) — 11/11 videos, each id oEmbed-verified REAL
  before entry (title+author confirmed live, no fabricated ids): L1
  Efficient Engineer viscosity, L2 Less Boring Lectures hydrostatic, L3
  Fluid Matters Reynolds, L4 Efficient Engineer Bernoulli, L5 Fluid
  Matters momentum, L6 Prof. Van Buren Buckingham-Pi, L7 Efficient
  Engineer laminar/turbulent, L8 saVRee valves, L9 Fluid Matters venturi,
  L10 HardHat Engineer pump curves, L11 CPPMechEngTutorials compressible.
  4 approved-channel + 7 policy-v3 (each an established educational channel
  reliably >3k views; exact count not machine-readable via oEmbed, so
  recorded as a verification note, not a fabricated number). Embeds
  102→113. Fluids content still to author (videos-first per owner breadth
  order). Method proven: WebSearch → candidate ids → paced oEmbed verify
  (2.5s spacing to avoid YT rate-limit) → embed verified only.
- VIDEO POLICY v3 (owner directive 2026-07-18 — RELAXES the strict
  APPROVED_CHANNELS allowlist): videos may now come from ANY channel, not
  just the 21-item list, PROVIDED (a) the video is the best on-topic fit
  for the lecture and (b) it has >3,000 views. Approved-list channels
  remain preferred; text textbook links stay as alternatives. HARD
  CONSTRAINTS UNCHANGED (integrity floor, NOT waived): every embedded id
  is a REAL video looked up and confirmed live — no fabricated ids, no
  invented view counts, ever; view-count and topic-fit verified before
  entry; a lesson with no verifiable qualifying video keeps the honest
  "none"/TODO marker rather than a guessed embed. Implementation: relax
  the build's channel-gate assertion to accept a verified-non-approved
  video carrying a recorded view count + source note; embed ONE best
  video per lecture. Executed course-by-course as authoring reaches each
  empty-video course (real per-video web verification) — NOT a blind bulk
  pass. math-3 unaffected (already approved-list embeds).
- HOMEPAGE ROBOT CREW (owner order 2026-07-18): four small flat-vector
  robot characters playing with mechanical tools, generated via Higgsfield
  (nano_banana jobs 9bf28329 wrench-on-bolt / 8ecc4264 gear-hoop /
  247e699f caliper+blueprint / d4f0f791 oil-can, backgrounds removed via
  remove_background, true-PNG cutouts resized to 320px) →
  assets/nx/bots/*.png. Placed as decorative .nx-bot divs (CSS
  background-image, NOT <img> — keeps the non-logo <img> build gate
  meaningful) beside homepage sections 01–04 in BOTH language blocks
  (inset-inline-end positioning mirrors in RTL); gentle nx-bob 5.5s
  animation, staggered delays; hidden ≤1120px (would overlap text);
  animation off under prefers-reduced-motion. Verified at 1280px: all 4
  visible per language, zero text overlap (elementFromPoint check),
  images load. Homepage only — academic pages untouched.
- BANNER v3 + COST PURGE (owner orders 2026-07-18): (a) hero meta chips:
  Languages and Cost REMOVED from the banner (Curriculum chip only);
  the appbar language toggle (.lang-btn) STAYS — banner-only removal.
  (b) COST RULE (binding): the site never mentions its own cost/"free"
  anywhere — purged from hero chips (EN+AR), footer line (EN+AR), homepage
  meta description, PWA manifest, README. Engineering-economics "cost"
  content is unaffected (technical term). (c) HERO BACKGROUND ANIMATION
  via Higgsfield MCP: style-key frame nano_banana 21:9 (brand navy→teal
  gradient, thin teal line-art gear train / robot arm+conveyor /
  centrifugal pump / vibration waveform / amber IoT telemetry, calm
  center for headline; job 5733bbfa) → seedance_2_0 10s 720p loop with
  the SAME frame as start_image+end_image for a seamless loop (job
  6166ebd0 — owner-requested regeneration take; first take 58db4191
  discarded), silent, non-photoreal. Shipped as assets/nx/hero-loop.mp4
  (3.6 MB), <video autoplay muted loop playsinline> first child of both
  heroes, radial scrim ::before for text readability, shine ::after
  z-index above, reduced-motion hides the video. The "zero photography"
  rule is intact (the loop is a stylized vector-look animation, owner-
  ordered). Verified: playback advancing/looping, scrim, chips, toggle.
  v3.1 (owner iteration, same day): loop REPLACED with the centered-arm
  cycle — new key frame job 240ff3f8 (robotic arm dead-center, gripper
  holding amber-hub gear above the open slot of a gear train, dashed
  motion arc, conveyor left / waveform+telemetry right, top half clean)
  → seedance_2_0 job 3b23faf3: one 10s cause-and-effect cycle (arm
  lowers gear → train meshes and spins up → waveform/telemetry react →
  arm lifts back to exact start pose; seamless). Owner also ordered the
  video visible across the WHOLE banner behind the text: scrim lightened
  .55/.18 → .26/.08 and readability moved to .txt text-shadow. Verified:
  video box == banner box exactly, playing, full-banner scene visible
  behind the headline.
  tone pivot from transition-playbook to professional-institute voice.
  MISSION: eyebrow now "Mission · Advanced Industrial Systems & Engineering
  Mastery" (Free & bilingual removed from eyebrow only; meta chips keep
  Free/bilingual); owner's verbatim H1 KEPT; sub + premise elevated
  optimistic/accessible in EN and AR. TONE RULE (owner): marketing surfaces
  (mission/career) may use optimistic, encouraging language; ACADEMIC
  content keeps the professor voice — unchanged. CAREER PAGES (EN+AR)
  rebuilt: approved H1 "Careers in Advanced Industrial Systems — from
  specialization to leadership"; sections = 01 all-roles landscape (10
  specializations→curriculum spines), 02 CV translation (kept), 03 arena,
  04 CERTIFICATION ARCHITECTURE (centralized; CSWA/CSWP, AutoCAD, CMRP,
  ISO 18436, API 510/570/653, CWI, CQE, PMP, ISA, NEBOSH, ASME — every
  link opened and verified live 2026-07-18; experience gates stated
  honestly; NO literal "guaranteed employment" claims — integrity floor),
  05 interview map (kept), 06 twelve-month plan (reframed as development
  plan). LESSON LIBRARY: "Related certifications & licenses" block REMOVED
  from all 528 lesson pages (was placeholder-only; now centralized on
  Career Paths); "Textbooks & references" upgraded — new
  data/textbooks.json registry (52 canonical university texts, 48 with
  Open-Library-API-verified links, all 48 courses mapped; unverified
  texts render as plain text). TEXTBOOK CANON EXPANDED (owner): the
  Library references block may cite the standard university canon
  (Hibbeler, Shigley, Incropera, Rao, Ogata, Montgomery, ...); the
  SOURCES list still governs in-lesson citations. Course-page link label
  "Full career playbook →" → "Explore career paths →".
- CORPORATE NEUTRALITY POLICY v3 (owner addendum, 2026-07-18 — supersedes
  the v2 career-page exception): (a) ACADEMIC tabs: company-free,
  unchanged. (b) Course-page "Career outlook" blocks: PEDAGOGICAL —
  specific company names (local + global) allowed and encouraged;
  retained exactly as written. (c) CAREER STRATEGY / interview-prep /
  job-seeking pages (career.html + career-ar.html): NO company names —
  describe industry sector, business model, and engineering function
  instead (six named anchors → six sector profiles; both languages;
  scan verified zero names). Certification issuing bodies (SMRP, ASME,
  API, ...) are not employer references and remain named + linked.
- DUAL-REMOTE CONFIG (owner directive 2026-07-18, supersedes all earlier
  "origin = nexuskw" notes): origin FETCH =
  github.com/ilmshri/Nexus-Institute-of-Technology (the Nexus code home;
  full 51-commit history imported 2026-07-18, replacing its stub README);
  origin carries TWO PUSH URLs — the code home AND
  github.com/nexuskw/nexuskw.github.io (the GitHub Pages repo that SERVES
  https://nexuskw.github.io/; the URL is bound to that repo name). One
  `git push origin main` updates both. NEVER drop the nexuskw push URL —
  doing so silently stops live-site deploys. (Session evidence note: the
  premise "pushes were going to ilmshri/asu" was checked and false — asu
  is the dead 2026-07-13 first-deploy stub; all session pushes had gone
  to nexuskw/nexuskw.github.io.)
- CHECKPOINT: COMPUTING EDUCATIONAL UNIT COMPLETE (2026-07-18): fifth Y1S1
  course under the Unit template; second fresh-authored (no legacy content).
  Batches 1-2 (commits 785b322, debd9da) shipped L1-8; Batch 3 this commit:
  L9 curve fitting/interpolation (642w), L10 small simulations/Euler (584w),
  L11 maintenance-data project (584w) — each §1-§4 with working-method
  closing, glossary TABLES, 3 solves + 5 MCs (24 new items; every number
  Python-verified pre-write: pump-curve interpolation 40.4 m, transmitter
  LS fit 1.545x+4.12, U-residuals [+0.30,-0.15,-0.30,-0.15,+0.30] at
  R²=0.9954, Euler cooling 84.0/78.6 vs exact 79.12, tank march
  1.4/1.72→h*=3.0, instability 90→-60→165 past dt=2/k, MTBF 168/MTTR 12/
  avail 93.3%, unit-error mean 84.0→5.33 h with median 5.5 fixed, Pareto
  73.5%). Company-free scan PASS (scan upgraded to word-boundary matching —
  "adequate" no longer false-positives EQUATE). Library was already 11/11
  approved MIT OCW embeds. Career module attached (rotation:
  Infrastructure/Utilities-KNPC, Specialized Mfg-Kirby, Construction&EPC-
  Bechtel — trio distinct from all four previous courses). RENDER GATES
  VERIFIED in-browser on localhost: quiz engine graded 5/5 on L9/L10/L11
  (answer keys independently confirmed), MathJax typeset (35/44/3
  containers), glossary tables render, embeds live, zero "§", career block
  renders with all three companies, all 11 lessons badged Full lesson.
  Coverage 71→74/528 (14%). Y1S1 Unit scoreboard: math-1 ✓ statics ✓
  materials-1 ✓ physics-1 ✓ computing ✓; NEXT per approved order:
  drawing-cad (incl. re-verifying its drafts/ quiz items) → Y1S2 stream
  (math-2 first).
- CHECKPOINT: MATERIALS-1 EDUCATIONAL UNIT COMPLETE (2026-07-18): second
  course under the Unit template. All 11 lessons: lectures 500-1000w
  (working-method sections: failure-reading, bond-reading, unit-cell
  bookkeeping, indexing, defect inventory, diffusion estimating, tension-
  test reading, hardness honesty, strengthening decisions, annealing
  decisions, cast-structure reading), glossary TABLES, quizzes
  [s,m,m,s,m] → [s,s,s,m,m,m,m,m] (+11 solves +22 MCs, all Python-verified
  pre-write: corroded-bolt stress, bond-energy conversion, Cu density from
  FCC cell, linear density, vacancy exponential, carburizing time, modulus
  from elastic leg, HB→UTS triage, Hall-Petch, grain growth, Chvorinov);
  applied vignettes scrubbed company-free (11 replacements); Library = 7
  approved 3.091/EE embeds + owner-approved "none"/continue-hunt markers.
  Career module attached (rotation: Infrastructure/Utilities-Gulf Cable,
  Automotive & Heavy Equipment, Global OEM-Schneider Electric — distinct
  from math-1 and statics sectors). NEXT per approved order: physics-1
  (fresh authoring) → computing → drawing-cad → Y1S2 stream.
- BATCH A+B APPROVED & EXECUTED (owner, 2026-07-18): embeds now 73.
  VERIFIED+EMBEDDED: materials-1 L7/L8 (Efficient Engineer stress-strain,
  strength/ductility/toughness); physics-1 L1–L9 (Engineering Deciphered
  units + dynamics series); drawing-cad L7 (Efficient Engineer GD&T);
  math-1 L1 (Khan Academy units/dimensional analysis — replaced the
  "none" marker); math-2 L1–L6,L8–L11 (MIT OCW 18.02/18.03); math-3 全11
  (MIT OCW 18.03/18.02). "NONE" MARKERS (owner-approved): materials-1
  L10 (recrystallization) + L11 (solidification) — approved list has no
  match; our casting lectures carry L11's depth in-house. DUP-RULING
  (owner): 18.03 Lec 14 Resonance + Lec 19 Laplace intentionally
  cross-listed in math-2 L9/L10 AND math-3 L5/L6 as reinforcement/bridge
  lectures. SYLLABUS-REFINEMENT NOTE (owner-acknowledged): math-2 L7–L10
  duplicates math-3 topics (legacy overlap from the Curriculum Map's
  math-3 addition) — refine math-2 toward pure multivariable/vector
  calculus in a future map revision. math-2 L7 (3Blue1Brown
  eigenvectors, PFDu9oVAE-g) APPROVED & embedded 2026-07-18 — math-2 now
  11/11; embeds 74. WAVE C APPROVED & EXECUTED (owner,
  2026-07-18): dynamics L1-L9 (Hanson dynamics course L1/16/23/26/13/28/31
  + ED relative-acceleration + Khan rotational KE), dynamics L11 + physics-1
  L11 cross-listed MIT 8.03 Lec 1 SHM (reinforcement precedent), physics-1
  L10 Khan rigid-system rotational energy. Dynamics L10 (rotor balancing)
  stays continue-hunt per owner. physics-1 now 11/11; dynamics 10/11;
  embeds 86. Discarded at gate: John Wolbeck SHM (unapproved channel).
  WAVE D APPROVED & EXECUTED (owner, 2026-07-18): strength 11/11 (Hanson
  MoM lessons 9/21/23/31/62/44/50/41/55/66/22), materials-2 L1/L2 (EE
  Understanding Metals + Steels/Heat Treatment), L7 (Hanson S-N fatigue),
  L8/L9 (3.091 Polymers I + Glassy Solids best-fit); L3/4/5/6/10/11
  continue-hunt per owner. Embeds 102.
- EDUCATIONAL-UNIT PROTOCOL (owner, 2026-07-18, immediate + retroactive):
  every lesson is a complete unit — A Theoretical Summary, B Key Concepts
  & Formulas, C 2-3 Worked Examples, D Quick Quiz (3-5 questions),
  E Supplemental Resources (primary technical embed + Arabic supplemental
  block). This maps 1:1 onto the existing 4-tab architecture (Lecture =
  A, Foundations glossary table = B, Examples and Quiz = C+D, Library =
  E); the ONE new element is the "Supplemental/Arabic Resources" block in
  Library (renderer + data field to build). math-1 is the live reference
  implementation of A-D+primary-video. NO lesson counts as "Done" without
  the full structure. RETROACTIVE ROLLOUT (gated): Full Lesson Template
  presented to owner for approval; on approval, content-filling proceeds
  course-by-course (Wave D courses + previous semesters first) with
  checkpoint commits, Python-verified arithmetic, company-free scans, and
  career-sector rotation — the established math-1 pipeline. QUEUED FOR NEXT PASS (owner-approved as
  queued): physics-1 L10 (rigid-body kinetics — Hanson Dynamics
  playlist), L11 (SHM — Less Boring Lectures); drawing-cad L1–L6,L8–L11
  (Husam's Mech Vision scoping + Ala Hijazi Arabic supplemental).
  WAVE PLAN C–J recorded in session log; Wave C = dynamics + physics-1
  remainder via Hanson/ED dynamics playlists. Then Y1S2 with each
  course build. BATCH SCALING ORDER (owner): after Y1S1 patch → full
  math-1-pipeline builds for Y1S2, Y2S1, Y2S2, with per-lesson video
  mapping from the approved channels and career-sector rotation per course.

- 528 NORMALIZATION EXECUTED (2026-07-17, owner-approved): the catalog is now a
  strict 6×11 grid — 48 courses × 11 lessons = 528, verified at build
  (coverage 52/528 = 10%). Actions: (a) MOVES — reliability-1 "Reliability
  testing and growth" → reliability-2 (now L6, after design-for-
  maintainability); condition-monitoring "Online monitoring and protection
  systems" → scada-iiot (now L7, after IIoT sensors; kuwait tag moved with
  it). (b) MERGES of adjacent thin Tier-3 pairs (scopes combined verbatim-
  faithful, nothing dropped): mfg-processes-1 6+11 (forming fundamentals +
  workability), mfg-processes-2 9+10 (welding II + thermal cutting/joint
  prep), strength 4+5 (bending + transverse shear), fluids 3+4 (flow
  description/Re + continuity), heat-transfer 9+10 (radiation pair),
  welding-ndt 8+9 (UT + RT in depth), rotating-equipment 9+10 (fans/blowers
  + turbines), maintenance-planning 10+11 (shutdown execution + contractor
  mgmt, HEISCO kuwait tag kept). (c) NEW AUTHORED STUBS (Tier 3, real scope
  + src + 2 preview questions each, never padding): computing L5 testing/
  debugging code; electrical L9 synchronous machines & standby generation;
  thermo-2 L7 cooling towers; metrology L5 limit gauging & Taylor's
  principle; electronics-sensors L8 vibration & speed sensors;
  kinematics-machinery L8 clutches & brakes; safety L9 PPE & its limits;
  plc-2 L8 HMI design; robotics L8 machine tending & assembly cells;
  corrosion L8 materials selection; engineering-economics L7 uncertainty/
  sensitivity/risk; smart-manufacturing L3 MES & ISA-95 stack; hse L10
  monitoring/audit/review; capstone L5 spares & materials strategy.
  mfg-processes-1 fragment ids (…-01…-09) still align with lesson numbers
  (only L11 was removed). Curriculum-page copy updated to "strict grid"
  wording in nexus_build.py. Lesson renumbering shifts localStorage
  progress keys for in-flight learners in the 24 touched courses — accepted.
- APPROVALS RECEIVED (owner, 2026-07-17 PM): (1) v5 Academic Shield logo
  APPROVED; (2) shell/UI/colors APPROVED; (3) 522→528 strict 6×11
  normalization APPROVED (execute in the NEXT session — 9 courses have 12
  lessons, 15 have 10; net +6); (4) Phase-2 order APPROVED (Year 1 content
  first). MISSION COPY REWRITTEN & DEPLOYED (owner's verbatim copy): hero
  "Learn Mechanical Engineering from Scratch to Industry 4.0."; audience =
  ANYONE, zero background; Two Doors = Complete Academic Curriculum +
  Modern Applications & Industry 4.0; integrity floor unchanged. SCOPE
  RULES (binding for ALL future content): the platform covers ALL
  mechanical-engineering roles (design, operations, maintenance, planning,
  thermal systems, fluid dynamics) — never manufacturing-only; Industry
  4.0/PLC/SCADA/automation integrated as modern extensions; NO company
  names in examples or text (existing named applied-cases and the Career
  page await a Phase-2 rewrite decision). BILINGUAL RULE (binding): AR
  version translates EVERYTHING (UI, cards, lesson content, worked
  solutions, quiz explanations) into formal Arabic EXCEPT numbers,
  equations, math symbols, proper nouns, and core technical terms, which
  stay English/original — with flawless bidi via <span dir="ltr"> (or
  <bdi>) isolation so mixed lines never break or flip punctuation.
  Handoff document issued to the owner for the next session; its pending
  tasks: execute 528 normalization, then Phase 2 Year-1 content.
- PHASE GATES REINSTATED (owner, 2026-07-17 PM — supersedes the zero-approval
  rollout where they conflict): NO content generation until the owner approves
  the Phase-1 design + logo. Phase 1 (SHIPPED, awaiting approval) = branding,
  UI/UX shell, architecture. Phase 2 (GATED) = content: Year 1-2 full tabs,
  math-1/drawing-cad quiz retrofits (unverified drafts preserved in
  drafts/phase2-quiz-mc-drafts/ — generator ignores that dir), computing
  course, mission-copy rewrite, per-lesson video curation, cert maps,
  foundations glossary-table migration, 522→528 normalization decision.
- MISSION REFRAME (owner): from-scratch online B.S. Mechanical Engineering
  institute for ANYONE with zero background; classic ME core with Industry
  4.0 / PLC / SCADA integrated in later stages. Mission-page copy still says
  "one specific person" — rewrite is Phase-2 text work, gated.
- LOGO v5 "Academic Shield" (nexus/logo.svg, PENDING owner approval): flat
  navy shield, amber keyline, teal 8-tooth gear with amber hub, cream open
  book; no gradients/filters. The v4 metallic gear-coin was NOT approved —
  archived untouched at nexus/logo-v4-gear-coin-unapproved.svg. Palette
  unchanged (v5 is built from the existing navy/teal/amber/cream tokens, so
  the platform already harmonizes with it). App bar uses a serif lockup
  ("Nexus Institute of Technology" + small-caps "Online Engineering
  Education").
- LESSON ARCHITECTURE (owner, STRICT, supersedes the earlier 4-tab spec):
  tab order is Lecture | Foundations | Examples and Quiz | Library.
  Lecture: 500-1000 words, textbook-style, NO solved examples. Foundations:
  glossary TABLE Term | Equation | When to use (style ready:
  table.glossary/.glossary-wrap; existing list-style foundations migrate in
  Phase 2). Examples and Quiz: 3 solved examples + 5-question MCQ graded by
  a Submit button (engine v2 LIVE: select-then-submit, per-question
  verdicts + explanations + score; solve items keep reveal buttons).
  Library: exactly ONE embedded video from the strict channel list below,
  else the "TODO: Find approved video" placeholder; then Textbooks &
  references (3 US-published texts per lesson in Phase 2; verified links
  only); then Related certifications & licenses (2-3 per lesson, Phase 2,
  verified links only — placeholders stay empty until verified).
- STRICT EMBED CHANNELS (owner correction, 2026-07-17 PM — supersedes ALL
  earlier embed policy; exactly these 15, enforced by APPROVED_CHANNELS in
  nexus_build.py): MIT OpenCourseWare, Engineer4Free, The Efficient
  Engineer, Jeff Hanson, Engineering Explained, Practical Engineering, The
  Engineering Mindset, RealPars, SolisPLC, AutomationDirect, Plcprofessor,
  GalcoTV, Hegamastery, Siemens Knowledge Hub, Schneider Electric Hub.
  NPTEL and LearnChemE are BANNED from embedding (verified text links in
  references only). Every URL still gets opened and verified before entry;
  channels not yet in the registry (e.g. Hegamastery) must be verified to
  exist before first use.

- NEXUS IS THE PLATFORM (owner EXECUTION OVERRIDE, 2026-07-17 — supersedes
  the stage gates and the "separate platform" plan): the live site at
  https://nexuskw.github.io/ IS Nexus Institute of Technology, replacing the
  Sun Devil Factory chrome. DEPLOY GENERATOR: `python3 nexus_build.py`
  (build.py is retained ONLY as the data/helper layer nexus_build.py imports
  — never deploy from build.py; it emits the retired SDF chrome).
  Platform rules (binding): centered brand + Mission | Curriculum | Career
  Paths pipe nav; FOUR tabs per lesson (Foundations | Lecture | Worked
  Examples | Library) — Kuwait floor content lives inside Worked Examples as
  "Applied case" blocks; zero "§" anywhere (nx_text() transform + build
  assertion); zero photography — original vector illustrations only (ILLOS
  in nexus_build.py, one motif per course; photo figures in Tier-1 fragments
  auto-convert to .fieldnote blocks keeping only the original NOTICE text);
  EN/AR bilingual chrome with RTL toggle (localStorage nx-lang), Mission +
  Career fully Arabic (content/pages/mission.html embeds both languages;
  career-ar.html is the Arabic career page); installable PWA (manifest +
  sw.js + icons, generated from nexus/logo.svg); honest completion tracker
  on the curriculum page, recomputed every build; library embeds are
  native-English YouTube only — NPTEL never embeds (text links only).
  CONTINUOUS ROLLOUT (owner order, zero approvals): every session author the
  next courses to full 4-tab depth (EN + AR lesson content) in queue order
  until 528/528; report coverage after every course. 522→528 normalization
  happens by AUTHORING the missing lessons (6 courses are short), never by
  padding. Coverage at handoff: 52/522 (10%) at full depth. RETROFIT still
  owed: math-1 + drawing-cad to 5-problem quiz format; then computing, then
  y1s2 onward. Arabic lesson content ships with each newly authored course.

- NEXUS INSTITUTE OF TECHNOLOGY (2026-07-13): a SEPARATE platform (owner
  decision — does NOT replace the live ASU site). Staged rebuild lives in
  nexus/ (Stage 1 design system approved-pending: metallic planetary-gear
  logo per owner's reference image, teal #14CFA0/#07785C + amber #F5A623
  on whitish bg, 4-tab lesson model Foundations/Lecture/Worked Examples/
  Library, bilingual EN/AR RTL, PWA planned, no photography — original
  vectors only, no "§" anywhere). Stage gates: 2 = nav/IA, 3 = sample
  lesson, 4 = full rollout — each requires owner approval. Stage-1 artifact:
  https://claude.ai/code/artifact/23ea55c4-300a-41aa-a9d6-c3bf25ce1930

- STANDING ORDER (owner, 2026-07-13): fill ALL 522 lessons' five tabs with
  real content, course by course, WITHOUT per-batch approval. Content merges
  via data/content/<sem>-<course>.json ({lesson_n: {lecture, foundations,
  examples, kuwait}} — HTML, MathJax LaTeX allowed). Arithmetic in worked
  examples must be verified before writing. DONE: y1s1/math-1 (MTH 101),
  y1s1/drawing-cad (DRW 102), y1s1/statics (STA 103, 2026-07-17),
  y1s1/materials-1 (MAT 104, 2026-07-17) — 44 lessons full, all worked-example
  arithmetic machine-verified before writing. NEXT QUEUE: computing,
  then y1s2 onward. Every session: author as many complete courses as fit,
  EXAMPLES FORMAT (owner order 2026-07-17, supersedes the 2-example blob):
  every lesson's Worked Examples tab is a FIVE-problem interactive quiz —
  content JSON key "quiz": list of 5 items, order [solve, mc, mc, solve, mc].
  solve = {"type":"solve","q":html,"solution":html} (student attempts, then
  reveals the full solution); mc = {"type":"mc","q":html,"choices":[4 html],
  "answer":idx,"solution":html} (click → correct/wrong verdict + the correct
  choice highlighted + explanation auto-opens; one attempt, buttons disable).
  Rendered by quiz_html() in build.py; behavior in assets/js/site.js; styles
  .quiz-* in site.css. Asset URLs carry ?v=<content-hash> (cache busting —
  keep it). statics + materials-1 already converted (110 quiz problems, all
  numeric answers machine-verified; distractors are classic errors, named in
  the explanation). RETROFIT QUEUE: math-1 and drawing-cad still carry the
  old 2-example "examples" blob (renderer still supports it) — convert both
  to 5-problem quizzes before starting computing.
  rebuild, push (origin = sundevilfactory/asu, credential in keychain),
  verify live.

- ARCHITECTURE (2026-07-13, owner-approved): every lesson has its own page
  with FIVE TABS — Lecture / Foundations / Worked Examples / Kuwait Floor /
  Library (~573 pages total). Tabs are populated from real content at the
  lesson's tier; unbuilt depth carries queued labels, never filler.
  DESIGN (owner REVERSED their earlier choice on 2026-07-13, second
  instruction wins): ASU-style palette is now PRIMARY — --ember token IS
  maroon #8C1D40 (universal accent), --gold #FFC627 for lines/chips/fork
  and dark-board accents (never body text on white — contrast). Trademark
  exposure was flagged twice; owner accepted it. Layout: left sidebar
  (semesters → courses → current course's lessons) on all course/lesson
  pages, stacking below 1000px. MathJax 3 loads from CDN on all lesson
  pages (tex-chtml, \( \) inline) — existing equations remain hand-built
  HTML/CSS; write NEW lecture math in either, prefer LaTeX going forward.
  Depth continues in batches, Core-60 first; the "522 fully written
  lessons in one pass" demand remains infeasible and is delivered
  incrementally instead. Per-lesson video embeds are verified-only
  (fabricating YouTube IDs is prohibited regardless of instructions).
  Library-tab embeds are generated ONLY from registry/card URLs that are
  embeddable YouTube watch/playlist links — all verified. Client search:
  docs/curriculum/search-index.json + JS on the curriculum index.
  Deploy target (changed 2026-07-17: owner deleted the sundevilfactory org
  by accident while renaming; full repo + history live locally):
  github.com/nexuskw/nexuskw.github.io →
  https://nexuskw.github.io/ (root URL, no /asu path). Owner creates
  the org + empty public repo; push from this Mac; Pages = main:/docs.
  The old sundevilfactory.github.io/asu URL is dead.

- Preview questions ("preview" field, rendered above Taught-from): 522/522 —
  COMPLETE (Core 60 numeric micro-problems + all Tier-3 conceptual pairs,
  all 8 semesters). Rules that governed them: original wording, match the
  lesson scope + cited source, no invented plant data. New lessons added
  later must ship with a preview field.
- Source registry: data/sources.json — every URL verified live before entry
  (OCW course pages, NPTEL course pages, Open Library work pages,
  smrp.org, nebosh.org.uk). Sources without verifiable official URLs stay
  plain text. build.py linkify() renders them.
- Video-source policy (applied 2026-07-13): registry entries may carry
  "watch" (verified lecture-videos page → rendered "Watch lectures ▶"),
  "label" (visible note, e.g. NPTEL's "alternative (enable captions)"),
  and "arabic" (verified Arabic source → rendered "In Arabic — alternative";
  bar RELAXED by owner decision 2026-07-13: independent Arabic educators and
  unofficial recordings of real university lectures are acceptable if
  on-topic, technically sound, and watchable — each URL oEmbed/title
  verified before entry; ripped paid courses and content farms remain
  excluded; English always stays the primary link; where the source is an
  unofficial recording, add {"url":…, "note":"unofficial recording"}).
  Registry uses topic-suffixed match tokens (e.g. "LearnChemE (CU Boulder)
  — fluids") so an Arabic source never renders on a lesson whose topic it
  doesn't cover. Priority: OCW video pages > university channels
  (Jeff Hanson/TTU via channel id UCXKW_dKcpFh358S1rV5qBDw — NOT the
  @JeffHanson handle, which is a different channel; LearnChemE/CU Boulder)
  > professional bodies (SME channel UCiEiOeFUl4Ytrv63Udugckg, Mobius
  Institute) > independent channels labeled "supplementary" (The Efficient
  Engineer, RealPars). NPTEL links are kept as labeled alternatives, never
  removed without a verified replacement.

- Tier 1 done: y1s1-mp1-02 (casting solidification), y1s1-mp1-03 (casting
  practice, quality & defects).
- Tier 2 done (batch 1, A-block): see ledger comments in data/y1s1.json and
  content/lessons/. Next batches in order: remainder of A (machining/welding/
  NDT/sheet/plastics), then B, C, D, E, F, G.
- Tier 2 lessons without a written guide yet are tagged `core60` but have no
  `content` field — the course page automatically shows them as
  "study guide queued".
- Every new Tier 1/2 page: follow the gold standard structure of
  y1s1-mp1-02/03. Verify every citation and URL before adding. Label all
  industrial numbers "representative" unless from a cited source.
- MATH-3 (MTH 207) COURSE COMPLETE (2026-07-19, owner directive "every
  video lesson gets the full unit"): all 11 lessons now full Educational
  Units. AUTHORED THIS SESSION: L5-L11 fresh (free/forced oscillations +
  resonance/beats; Laplace transforms I — definition/table/derivative &
  shift rules; Laplace II — transform-solve-invert IVPs + partial
  fractions; systems as Ax=b + determinant/inverse; Gaussian elimination/
  pivots/rank; eigenvalues/eigenvectors + x'=Ax stability; numerical ODEs
  Euler/Heun/RK4 + step-size convergence). Each: §1-§5 lecture 550-612w
  (all >=500 floor), glossary-TABLE foundations, 3 solve + 5 MC quiz.
  L2/L3/L4 lecture top-up DONE (484/398/450 -> 700/678/704w via a §5
  each; all verified numbers preserved). Every quiz number machine-checked
  pre-write in pure-Python (56 assertions: L5-L7 21 incl. Laplace
  transforms confirmed by numerical integration of ∫₀^∞ e^{-st}f dt; L8-L11
  35 incl. 2×2/3×3 solve, determinant, inverse·A=I, eigenvalues via
  trace/det, Euler global-error halving ratio 1.92≈2). Company-free scan
  PASS (academic rule). Videos already 11/11 approved MIT OCW 18.03 embeds
  — untouched. Build clean (nexus_build.py): pages 579, embeds 124,
  coverage 104→111/528 (21%). Render-gate: zero raw § leak (build
  normalises §N→0N), all 11 pages placeholder-free, glossary + 8-item quiz
  + embed present, MTH 207 L10 spot-checked in-browser ("Full lesson" /
  "8-problem interactive quiz" headers confirmed). Content-review doc at
  drafts/mth207-content-review.html. NOT YET PUSHED to live — awaiting
  owner go-ahead. STILL OWED for the wider directive: Year-2 empty-video
  courses electronics-sensors, mfg-processes-2 (no videos/content yet).
- MATH-2 (MTH 151, Y1S2) COURSE COMPLETE (2026-07-19, owner "keep going"): first
  Year-1-Semester-2 course authored end-to-end to the UPGRADED spec. All 11 lessons
  fresh full Educational Units: vectors/dot-cross; partial derivatives/gradient;
  chain rule/total differential/error-propagation; multiple integrals/centroid/
  moment-of-inertia; vector fields/flux/circulation/div/curl/Green; matrices &
  Gaussian elimination; eigenvalues/eigenvectors; second-order ODEs (damping
  regimes); forced oscillations/resonance; Laplace transforms; Fourier series.
  Each: topic-sized lecture with .keybox callouts + a coordinate-accurate inline
  SVG diagram (generated + verified in Python); foundations toolkit table; 3 solve
  + 8 MC quiz (121 items total; ~110 numbers Python-verified pre-write incl. Laplace
  by numerical integration); company-free applied-case (kuwait field). Videos
  inherited from y1s2.json base data (MIT OCW 18.02/18.03 + 3Blue1Brown, pre-verified)
  — none fabricated. Coverage 104->122/528 (23%). Commits: 7e7378b, cefc370, c407627,
  a3611cf + this. NEW RENDERING STANDARDS (owner directives this session, now
  permanent — see memory feedback_math_rendering / feedback_lecture_length):
  (a) lecture length matches the topic — short topics may be <1000w, never pad;
  (b) reading line-height 1.8; big blocks (.keybox 34px, figure.lesson-diagram 36px,
  glossary 30px) spaced to breathe; (c) multi-row matrices ALWAYS display math, never
  inline; multi-equation systems as stacked \begin{cases}; one matrix per display line;
  column vectors as inline transposes; (d) display eqns + quiz stems/solutions +
  glossary get overflow-x:auto — verified NO horizontal page scroll at 320px across
  the course. CSS commits also fix the already-live math-3 pages' spacing/overflow.
  STILL OWED for Year 1: Y1S2 dynamics, materials-2, thermo-1, electrical,
  mfg-processes-1 (55 lessons) — then Year 1 closes.
- DYNAMICS (DYN 152, Y1S2) COURSE COMPLETE (2026-07-19, owner "proceed"): second
  Y1S2 course, all 11 lessons full Educational Units to the upgraded spec. Particle
  block: L1 kinematics (normal-tangential), L2 Newton's 2nd law (incline FBD), L3
  work-energy (energy bars), L4 impulse-momentum-impact (collision). Rigid-body block:
  L5 systems/centre-of-mass/jet force, L6 rigid-body kinematics (rolling/instant
  centre), L7 relative accel & Coriolis, L8 Newton-Euler kinetics (ΣM=Iα, parallel
  axis), L9 rotational energy/momentum (flywheel/ang-momentum conservation), L10
  balancing of rotors (mrω²), L11 intro to vibration (ωn, ζ, log decrement). Each:
  topic-sized lecture + keybox callout + coordinate-accurate SVG diagram (all
  Python-generated & verified); foundations toolkit; 3 solve + 8 MC (121 items,
  ~75 numbers Python-verified); company-free applied case. Videos inherited from
  y1s2.json (Jeff Hanson dynamics series + MIT/Khan/Eng.Deciphered). L10 has NO
  base-data video -> renders the honest "video TODO" marker, ZERO fabricated embeds
  (integrity floor held). Rendering rules from the math-2 session applied throughout.
  Coverage 122->133/528 (25%). Commits a019b8b + this. Y1S2 status: math-2 ✓,
  dynamics ✓; STILL OWED for Year 1: materials-2, thermo-1, electrical,
  mfg-processes-1 (44 lessons) -> then Year 1 closes.
- FRONTEND REDESIGN v3 (owner directive 2026-07-20/21, executed): structure mirrors
  the owner's reference (meched.lovable.app) in the Nexus LIGHT identity — background
  stays light, fonts unchanged (Helvetica Neue / Georgia / mono). NAV is now 5 tabs:
  Home / About / Mission / Curriculum / Career Paths. NEW homepage (index.html,
  content/pages/home-nexus.html generated by scratchpad gen_home.py): banner preserved
  VERBATIM (nx-hero + hero-loop.mp4 + shine), then stats band (live build-computed
  depth), FIG 01 interactive workshop (computed meshing gear train 24:16:12 + crank-
  piston + tool chips; cursor parallax + velocity-driven gear spin in vanilla JS at
  end of nexus.js — "Higgsfield automation" request implemented natively; Higgsfield
  is media-gen only), FIG 02 system-overview (6 clickable discipline nodes -> flagship
  courses), featured courses (3 complete), Track A/B course lists, notes, CTA band.
  ROBOTS REMOVED from homepage (.nx-bot mascots stay only on Mission, which is "as
  is"). NEW About page (content/pages/about.html, passionate copy). Mission moved to
  mission/index.html with its body untouched (hero moved to Home). ARABIC ON HOLD
  (owner: re-add later with a translation toolkit): langBtn removed, data-ar stripped
  at emit (nx_page regex), ar-note/footer-AR/career-AR dropped, JS lang restore
  guarded; source fragments keep their AR text for later re-enable. LESSON PAGES
  (owner loves the reference lesson layout): new SOURCED-FROM strip + VIDEO HERO —
  the one approved embed now plays front-and-center under the lesson header in a
  framed panel with a minimal bar (title + channel ONLY — owner removed "EMBEDDED
  LECTURE" label and "WATCH ON YOUTUBE" link); Library tab keeps alternatives +
  canonical texts; honest in-production panel when no approved video. Verified:
  0 Arabic chars in docs/, 0 nx-bot on homepage, 375px no overflow, gears animate
  (JS transform sampled). Reduced-motion disables all homepage motion.
- GTRANSLATE — ADDED THEN REMOVED (owner, 2026-07-21): the owner-supplied GTranslate
  float widget (EN/FR/IT/ES/AR) was integrated site-wide, then the owner said "cancel
  and remove this current translating tool" — FULLY REVERTED same session (widget,
  GTRANSLATE_WIDGET constant + {gtranslate} field, CSS switcher override all removed;
  0 residue in docs/). Translation remains ON HOLD — the site is EN-only, no language
  switcher. Do NOT re-add a translation tool without a fresh owner directive. (Note:
  in-sandbox the switcher rendered and loaded 5 languages, but the actual Google
  cross-origin translation could not be exercised in the localhost/in-app browser;
  the removal was an owner product decision, not a verified failure.)

### Writing rules (non-negotiable)

- Derive or source every equation. Never state a result bare.
- Only the SOURCES list above may be cited. Verify editions or omit them.
- Kuwait examples only from the six companies; name process/equipment;
  never invent plant data.
- All photo captions honest: "representative example: X" when the facility
  is not identifiable. Never caption a stock photo as a named Kuwait plant.
- No fabricated URLs. Verify every external link live before committing.
- English only. Professor's voice: direct, precise, no filler, no
  motivational language.

## STANDING DIRECTIVE — ME / Industry 4.0 platform build (owner, 2026-07-22)

Applies to this repo permanently, retroactively to all courses/lessons and
proactively to all future content, regardless of any future rebrand.

1. MEDIA CENTERING & RESPONSIVENESS — Library-tab lecture videos centered in
   their container (`display:flex; justify-content:center; align-items:center;
   margin:0 auto`). 100% fluid across mobile/tablet/laptop/desktop. Kill the
   right-side whitespace asymmetry on MacBook: auto-center main containers,
   grids, and video wrappers (`margin-left:auto; margin-right:auto; width:100%;
   max-width:960px`).
2. UNIT POLICY — SI is the default baseline for all theory, derivations, and
   core content. Worked examples and quiz questions MUST also test alternative
   systems (US Customary/Imperial, CGS) for real-world versatility.
3. GLOBAL REFERENCE TAB — dedicated site-wide Reference section indexing unit
   conversions, variable definitions, equations, and terminology. Every
   variable/factor/equation/term introduced inline in lessons BEFORE it appears
   in a quiz or example.
4. DYNAMIC QUIZ ENGINE — on an incorrect MCQ answer, swap the question for an
   alternative variant that tests the same underlying concept.
5. COURSE-SUMMARY PDF — prominent download at the end of each completed course.
   Structure: Part 1 = all lecture lessons compiled sequentially; Part 2 = all
   corresponding foundations pages/toolkits following the lectures.
6. FOOTER NAVIGATION — bottom of every lesson and course-completion state gives
   BOTH "Next Lesson" and "Next Course" (direct progression to the next course).

Build order this pass (owner, 2026-07-22): #1 → #6 → #3 → #4 → #2 → #5.

## CONTENT-COMPLETION MODE + YEAR 1 COMPLETE (owner, 2026-07-24)

STANDING DIRECTIVE (owner, 2026-07-24, supersedes the per-lesson video-approval
protocol for the duration of this pass): author full Educational Units for
every remaining lesson site-wide — Lecture/Foundations/Examples-and-Quiz/
Kuwait-applied-case — and leave the video field untouched (honest "TODO"
marker) on every lesson that does not already have one. The owner will
research and supply `{id,title,channel}` candidates in a later pass for a
batched embed; no video-sourcing (WebSearch/oEmbed) work is to be done
meanwhile. Content must be original — no reproducing textbook passages or
real exam problems verbatim (copyright; also lower-integrity than an
independently Python-verified original problem, which is the binding
standard regardless). Pace note (owner asked directly): a full 528-lesson
site in one sitting is not realistic at this quality bar without cutting
verification corners, which the owner does not want — work continues
course-by-course, curriculum order, with honest progress reporting, not a
promised completion time.

CHECKPOINT — YEAR 1 COMPLETE (2026-07-24): every Y1S1 + Y1S2 course is now
a full Educational Unit (computed SVG diagram, topic-sized §1-§4 lecture +
keybox, foundations glossary table, 3 solve + 8 MC Python-verified quiz,
company-free applied case, career block). This session: materials-2
(finished L3-11 + career), thermo-1 (fresh, all 11 + career), electrical
(fresh, all 11 + career), mfg-processes-1 (all 11 + career — L1-4/7-9
upgraded the project's original "gold standard" first-era fragments in
content/lessons/y1s1-mp1-*.html from the legacy template to the current
one, preserving their derivations — Chvorinov's rule, Bernoulli sprue
design, Sievert's law, the rolling/forging/drawing equations — L5/L6/L10/L11
authored fresh). 42 lessons total this pass, ~290 quiz items, every
number Python-verified pre-write. One gap remains from Y1: drawing-cad
(DRW 102) has full lecture+foundations content but its Examples tab is
still the pre-quiz-engine "examples" text blob — a format retrofit, not
new authoring — tracked separately, not blocking Year 1 closure.
Coverage 133→170/528 lessons at full depth (25%→32%) across this session.

CHECKPOINT — Y2S1 THREE OF FOUR DONE (2026-07-24, same session continued):
strength (SOM 201) finished L5-11 (7 lessons — L1-4 pre-existed in an
older 8-item-quiz/no-kuwait format and were left as-is, not retrofitted).
electronics-sensors (ELX 205) authored fresh, all 11 lessons + career
block (Texas Instruments / Analog Devices / Omron — none reused from an
earlier course's rotation). Coverage 170→188/528 (32%→36%). Diagram QA
note for future authoring: several SVG `<text>` labels initially
overflowed the 560-unit viewBox and were visually clipped in the browser
(caught by screenshot spot-check, not by the pre-build Python validation,
which does not measure rendered text width) — fixed by shortening or
repositioning. Worth a quick visual scan of any new free-floating diagram
label whose x-position plus estimated width sits past ~500-520.

CHECKPOINT — Y2S1 COMPLETE (2026-07-24, same session continued):
mfg-processes-2 (MFG 154) authored fresh, all 11 lessons + career block
(Sandvik Coromant / Lincoln Electric / Stratasys — fresh rotation).
Orthogonal cutting/Merchant's circle, tool wear modes, turning-milling-
drilling arithmetic, CNC/G-code and machine-health quantities, grinding
specific energy, Ra/Rz and residual stress, EDM/ECM/laser/waterjet,
arc welding heat input, resistance/brazing/thermal cutting, bolt preload
and torque-tension, and an AM capstone tying the whole course together —
all Python-verified (self-consistent Merchant's-circle force example,
verified Ra=h/4 for an idealized triangular profile, verified heat-input
and torque-tension arithmetic including a real "unexpectedly lubricated
bolt" 33%-overtightening example). Adopted this pass's diagram-label
lesson proactively: labels kept short and generously margined from the
start, plus a pre-build Python overflow scanner (x-position + estimated
text width vs. the 560-unit viewBox) added to the verification pipeline
before every build — caught one real overflow (L9) before it ever
reached the browser. Coverage 188→199/528 (36%→38%). Y2S1 (strength,
electronics-sensors, mfg-processes-2, plus previously-complete
electrical/thermo-1/materials-2/mfg-processes-1 from Y1) is now fully
authored — every Year 1 and Year 2 Semester 1 course is a complete
Educational Unit.
NEXT (approved order, unstarted): Y2S2 — thermo-2, heat-transfer,
machine-design-1, kinematics-machinery, metrology, mfg-processes-3 —
then Y3S1, Y3S2, Y4S1, Y4S2. 32 courses remain empty across Years 3-4
plus the six Y2S2 courses just named.
