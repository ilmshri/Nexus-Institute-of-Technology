# Nexus Institute of Technology

**Learn Mechanical Engineering from Scratch to Industry 4.0.**
Live site: **https://nexuskw.github.io/**

A textbook-sourced online mechanical-engineering curriculum for anyone,
starting from zero background: the classic ME core (mathematics, mechanics,
materials, thermal-fluids, design) extended into Industry 4.0 — PLC, SCADA,
condition monitoring, smart manufacturing.

**48 courses · 528 lessons · 8 semesters.** Every fully-authored lesson is a
four-tab Educational Unit — **Lecture** (textbook-style, 500–1000 words),
**Foundations** (prerequisites + glossary table), **Examples and Quiz**
(3 worked problems + 5 graded multiple-choice, every number machine-verified
before publication), **Library** (verified video from an approved channel
list + references). Lessons not yet at full depth say so honestly — no filler,
ever. Bilingual EN/AR chrome with RTL support; installable as a PWA.

## Build

Zero dependencies:

```bash
python3 nexus_build.py   # reads data/ + content/, writes the full site to docs/
```

(`build.py` is the retained data/helper library that `nexus_build.py` imports —
never deploy from it directly.)

- `data/y*.json` — the curriculum catalog (8 semesters × 6 courses × 11 lessons)
- `data/content/*.json` — full lesson content per authored course
- `data/sources.json` — verified source registry
- `content/pages/` — mission and career pages (EN + AR)
- `PROJECT_MAP.md` / `OWNER_MANUAL.md` — repository guide + owner's editing manual
- `CLAUDE.md` — full project brief and decision ledger (continuation contract)

## Deploy

GitHub Pages serves `main:/docs` at https://nexuskw.github.io/. After any
content change:

```bash
python3 nexus_build.py && git add -A && git commit -m "…" && git push
```

## Content rules (non-negotiable)

Derive or source every equation; cite only verifiable texts; machine-verify
all worked arithmetic before publication; no company names inside academic
content; verify every URL and video before linking; no fabricated data, ever.
Full rules in `CLAUDE.md`.
