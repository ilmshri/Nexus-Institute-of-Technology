# SUN DEVIL FACTORY — MASTER BRIEF (final authority)

This file is the continuation contract for any model or person working on this
repository. Where any other instruction differs from this brief, this brief wins.

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
