# Sun Devil Factory

A free, textbook-sourced engineering curriculum and career pathway for a
mechanical maintenance engineer moving into manufacturing (reliability,
asset integrity, production, maintenance planning) — built around Kuwait's
industrial anchor companies.

**48 courses · 522 lessons · 8 semesters.** Every lesson has its own page
with five tabs — Lecture, Foundations, Worked Examples, Kuwait Floor,
Library — populated with real content at its current depth tier and honest
"queued" labels where depth is still being written. Every external link
(textbooks via Open Library, MIT OCW lecture-video pages, verified YouTube
courseware, Arabic alternatives) was opened and verified before inclusion.

## Build

Zero dependencies:

```bash
python3 build.py     # reads data/*.json + content/, writes docs/ (~573 pages)
```

- `data/y*.json` — the curriculum (courses, lessons, scopes, sources,
  preview questions, Core-60 tags)
- `data/sources.json` — verified source registry (links, lecture-video
  pages, Arabic alternatives)
- `content/lessons/` — Tier-1 lectures and Tier-2 study guides (HTML
  fragments)
- `content/pages/` — home and career pages
- `CLAUDE.md` — the full project brief and content ledger (continuation
  contract for future working sessions)

## Deploy — GitHub Pages

Target URL: `https://nexuskw.github.io/`

1. Create the GitHub org `nexuskw` and an empty public repo `nexuskw.github.io`.
2. Create a public repo named `asu` and push this repository to it.
3. Repo → Settings → Pages → Deploy from a branch → `main`, folder `/docs`.

All internal links are relative, so the site works at any base path.
See `DEPLOY.md` for exact commands.

## Content rules (non-negotiable)

Derive or source every equation; cite only verifiable texts; never invent
plant data (representative values are labeled); verify every URL before
linking; English is the primary language with Arabic alternatives labeled
as such. Full rules in `CLAUDE.md`.
