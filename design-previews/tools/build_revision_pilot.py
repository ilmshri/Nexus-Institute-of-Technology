#!/usr/bin/env python3
"""MTH 101 L1 revision-notes PILOT page (owner review, 2026-08-01).

Renders the ONE migrated lesson through the REAL renderer
(nexus_build.revision_lesson_pages) into a standalone page under
design-previews/revision-pilot/. The live site is untouched: MTH 101 is not
fully migrated, so its course summary correctly stays on the recap spread
(all-or-legacy contract) until all 11 lessons carry revision blocks.

Run from the repo root:  python3 design-previews/tools/build_revision_pilot.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import nexus_build as nb  # noqa: E402

OUT = ROOT / "design-previews" / "revision-pilot"
OUT.mkdir(exist_ok=True)

data = json.loads((ROOT / "data/content/y1s1-math-1.json").read_text("utf-8"))
sd = json.loads((ROOT / "data/y1s1.json").read_text("utf-8"))
course = next(c for c in sd["courses"] if c["id"] == "math-1")
les = next(l for l in course["lessons"] if l["n"] == 1)
rev = data["1"]["revision"]
assert nb._revision_ok(data["1"]), "L1 revision block failed the renderer guard"

pages = nb.revision_lesson_pages(nb.esc(course["code"]), les, rev)

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PILOT — Revision notes — MTH 101 Lesson 01 — MechEd</title>
<link rel="icon" type="image/svg+xml" href="../../assets/nx/logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400..700&family=Source+Sans+3:wght@400..700&family=Source+Code+Pro:wght@400;600&display=swap">
<link rel="stylesheet" href="../../assets/nx/nexus.css">
{nb.MATHJAX}</head>
<body>
<main class="wrap">
<div class="pagehead sum-head">
  <p class="kicker"><span class="n">PILOT · DESIGN REVIEW</span>MTH 101 · Year 1 · Semester 1</p>
  <h1>{nb.esc(course['code'])} — {nb.esc(course['title'])}</h1>
  <p class="sub">Revision notes, new format — Lesson 01 only (the schema pilot).
  Terms and signs first, then one sheet per page, then the worked examples.
  Every block below is measured to fit a single A4 page. Use
  <b>Print / Save as PDF</b> to judge the printed set.</p>
  <div class="cta-row no-print">
    <button class="btn btn-primary" type="button" onclick="window.print()">Print / Save as PDF</button>
  </div>
</div>
<article class="part tight sum-doc">
{''.join(pages)}
</article>
</main>
</body></html>
"""
(OUT / "index.html").write_text(html, encoding="utf-8")
print(f"wrote {OUT/'index.html'} — {len(pages)} one-page blocks")
