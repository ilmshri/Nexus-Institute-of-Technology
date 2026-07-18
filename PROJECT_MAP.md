# PROJECT MAP — Nexus Institute of Technology

Live site: **https://nexuskw.github.io/** · Repo: `github.com/nexuskw/nexuskw.github.io`
Companion guide: **[OWNER_MANUAL.md](OWNER_MANUAL.md)** — step-by-step editing instructions.

This map lists every file and folder in the repository, split into two categories:

- 🟢 **EDITABLE CONTENT** — safe for you to modify. Worst case, a mistake here shows
  wrong text on one page; it will not take the site down.
- 🔴 **SYSTEM INFRASTRUCTURE — DO NOT TOUCH** — the machinery. Editing, renaming, or
  moving anything here can break the build or the live site.

> **The one rule that outranks everything: never rename or move ANY file, in either
> category.** File names here are not decorative — the build system finds content by
> exact name (`y1s1-computing.json` = Year 1, Semester 1, course "computing"). The names
> are already systematic; what they mean is decoded below. Edit file *contents* (green
> ones), never file *names*.

---

## 🟢 EDITABLE CONTENT (safe to modify)

### `data/content/` — the lessons themselves (your main workspace)

One JSON file per fully-authored course. Each contains, per lesson: the **lecture**, the
**foundations** glossary table, and the 8-item **quiz**.

| File | What it is |
|---|---|
| `data/content/y1s1-math-1.json` | Calculus I — all 11 lessons |
| `data/content/y1s1-drawing-cad.json` | Engineering Drawing & CAD — 11 lessons |
| `data/content/y1s1-statics.json` | Statics — 11 lessons |
| `data/content/y1s1-materials-1.json` | Materials Science I — 11 lessons |
| `data/content/y1s1-physics-1.json` | Physics I — 11 lessons |
| `data/content/y1s1-computing.json` | Engineering Computing — 11 lessons |

Naming code: `y1s1` = Year 1 Semester 1 · then the course id. New courses will follow
the same pattern (`y1s2-math-2.json`, …).

### `data/y*.json` — the course catalog (edit carefully)

Eight files, one per semester (`y1s1.json` … `y4s2.json`). Each lists that semester's
courses: titles, summaries, lesson titles/scopes, video selections, and the per-course
**career** paragraph. Text fields here are safe to edit (course summary, career block,
lesson scope). The structural fields (`id`, `n`, `tier`, `content`) are wiring — leave
them (see manual, section "Catalog files").

### `content/pages/` — the site's standalone pages

| File | What it is |
|---|---|
| `content/pages/mission.html` | Mission page (English + Arabic in one file) |
| `content/pages/career.html` | Career Paths page (English) |
| `content/pages/career-ar.html` | Career Paths page (Arabic) |
| `content/pages/home.html` | Legacy home fragment (mostly superseded) |

### `content/lessons/` — long-form lecture fragments (legacy format)

Eight hand-written casting/manufacturing lectures from the first build era
(`y1s1-mp1-01.html` … `y2s2-mp3-02.html`). Naming: semester + course + 2-digit lesson
number. Their text is editable; the build converts old photo figures automatically.

### `assets/img/` — retired photo pool (inert)

Eight `.jpg` photos + `CREDITS.md`. **Not used by the live site** (Nexus is
vector-only). Kept as archive; harmless either way.

### Documentation (plain reading/writing, no build impact)

| File | What it is |
|---|---|
| `README.md` | Public repo description |
| `DEPLOY.md` | Original deployment notes |
| `PROJECT_MAP.md` | This file |
| `OWNER_MANUAL.md` | Your editing manual |
| `CLAUDE.md` | ⚠️ Special: the project's master brief + decision ledger. Editable *by agreement* — it is the continuation contract every future working session obeys. Add decisions; don't casually delete history. |

---

## 🔴 SYSTEM INFRASTRUCTURE — DO NOT TOUCH

### The generators

| File | Why it's critical |
|---|---|
| `nexus_build.py` | **The build system.** Reads everything above, emits the whole site into `docs/`. All quality gates (no company names in lessons, verified videos only, etc.) are enforced here. |
| `build.py` | **Library the build system imports.** It looks legacy; it is not — `nexus_build.py` imports its data-loading core. Deleting or renaming it kills every build. |

### The live site's engine room

| Path | Why it's critical |
|---|---|
| `docs/` (8.6 MB, ~579 pages) | **Generated output — the actual live site.** Never edit by hand: the next build overwrites everything in it. All changes go through the green files + a rebuild. |
| `assets/nx/` | The live design system: `nexus.css` (all styling), `nexus.js` (tabs, quiz engine, language toggle, progress), `manifest.webmanifest` + `sw.js` + `icons/` (the installable-app machinery). A typo in `nexus.js` breaks every quiz on the site. |
| `nexus/logo.svg` | The approved v5 Academic Shield logo, copied into the site at build. |
| `nexus/logo-v4-gear-coin-unapproved.svg` | Archived unapproved logo — keep as record. |
| `nexus/design-system.html` | Stage-1 design reference artifact. |

### Retired chrome (inert but keep)

| Path | Why it stays |
|---|---|
| `assets/css/site.css`, `assets/js/site.js` | The retired Sun Devil Factory design. Not shipped by the Nexus build, but kept for history/rollback. |

### Working directories

| Path | What it is |
|---|---|
| `drafts/phase2-quiz-mc-drafts/` | Unverified quiz drafts (drawing-cad) + authoring journal. The build deliberately ignores this folder. Do not promote drafts to live content — their arithmetic has not been machine-verified yet. |
| `data/sources.json` | Verified source/URL registry. Every link was checked live before entry — don't add links without verifying. |
| `.claude/launch.json` | Local preview-server config for working sessions. |
| `.git/` | Version history — your safety net. Never edit internals. |

---

## The flow, in one picture

```
🟢 data/*.json  +  🟢 data/content/*.json  +  🟢 content/pages|lessons/*
        │
        ▼
🔴 python3 nexus_build.py      (imports 🔴 build.py; copies 🔴 assets/nx + 🔴 nexus/logo.svg)
        │
        ▼
🔴 docs/  ──git push──▶  https://nexuskw.github.io/  (GitHub Pages serves /docs)
```

Edit green → run the build → the build's own gates check your work → push → live.
Exact commands and templates: **[OWNER_MANUAL.md](OWNER_MANUAL.md)**.
