#!/usr/bin/env python3
"""THE one-A4-page gate for revision blocks — real print layout, really measured.

This is the authority drafts/qa_revision.py defers to. It renders every
revision block through the REAL renderer (nexus_build.revision_lesson_pages),
with the site's real stylesheet, the real webfonts, and MathJax fully typeset,
inside the exact A4 content box the print CSS produces, and measures each
block's rendered height in that layout. Word counts play no part in the
verdict; they are reported only to calibrate the authors' provisional
320-420 words/page budget against reality.

A4 geometry (must match @page in assets/nx/nexus.css):
    sheet 210x297mm, margins 18mm top/bottom + 16mm left/right
    -> content box 178mm x 261mm = 672.8px x 986.5px at CSS 96dpi.

Usage, from the repo root:
    python3 design-previews/tools/qa_revision_fit.py            # all content files
    python3 design-previews/tools/qa_revision_fit.py data/content/y1s1-math-1.json
Exit 1 if any block overflows its page.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import nexus_build as nb  # noqa: E402  (import-safe: build runs under __main__)

from playwright.sync_api import sync_playwright  # noqa: E402

MM = 96 / 25.4
CONTENT_W = round((210 - 2 * 16) * MM)          # 673 px
# The print CSS fixes each sheet at 260mm with an 8mm folio zone at the foot
# (see .rev-page in @media print) — content must fit the remaining 252mm.
CONTENT_H = (260 - 8) * MM                      # 952.5 px

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
         '?family=Source+Serif+4:opsz,wght@8..60,400..700'
         '&family=Source+Sans+3:wght@400..700'
         '&family=Source+Code+Pro:wght@400;600&display=swap">')


def words(html):
    s = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", " ", html, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return len(s.split())


def blocks_for(path):
    """(block_id, html, words) for every lesson carrying a renderable revision."""
    data = json.loads(path.read_text(encoding="utf-8"))
    sem, _, course_id = path.stem.partition("-")
    sd = json.loads((ROOT / f"data/{sem}.json").read_text(encoding="utf-8"))
    course = next((c for c in sd.get("courses", []) if c["id"] == course_id), None)
    if course is None:
        return []
    out = []
    for les in course["lessons"]:
        tab = data.get(str(les["n"]))
        if not nb._revision_ok(tab):
            continue
        rev = tab["revision"]
        pages = nb.revision_lesson_pages(nb.esc(course["code"]), les, rev)
        labels = (["opener", "terms"]
                  + [f"sheet {i+1}" for i in range(len(rev["sheets"]))]
                  + [f"example {i+1}" for i in range(len(rev.get("examples") or []))])
        for label, html in zip(labels, pages):
            out.append((f'{path.stem} L{les["n"]} {label}', html, words(html)))
    return out


def measure(blocks):
    css = (ROOT / "assets/nx/nexus.css").read_text(encoding="utf-8")
    body = "".join(
        f'<div class="qa-block" data-id="{i}">{html}</div>'
        for i, (_bid, html, _w) in enumerate(blocks))
    page_html = f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}
<style>{css}</style>
<style>body{{margin:0;background:#fff}}
.qa-wrap{{width:{CONTENT_W}px}}
.qa-block{{outline:1px dotted #ccc;margin-bottom:4px}}
/* measure CONTENT height, not the fixed printed sheet box: the print CSS
   pins .rev-page at 260mm, which would make every block "measure" exactly
   the box. Neutralise the box here; the verdict compares natural content
   height against the 252mm content zone of that box. */
.qa-block .rev-page{{height:auto !important;min-height:0 !important;
  padding:0 !important;overflow:visible !important}}</style>
{nb.MATHJAX}</head>
<body><article class="part tight sum-doc qa-wrap">{body}</article></body></html>"""
    tmp = ROOT / "design-previews" / "tools" / "_qa_fit_tmp.html"
    tmp.write_text(page_html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            pg = b.new_page(viewport={"width": CONTENT_W + 60, "height": 1200})
            pg.emulate_media(media="print")
            pg.goto(tmp.as_uri())
            pg.wait_for_load_state("networkidle")
            pg.wait_for_function(
                "window.MathJax && MathJax.startup && MathJax.startup.promise")
            # evaluate() awaits returned promises: block until maths and fonts
            # are genuinely typeset before measuring anything.
            pg.evaluate("() => MathJax.startup.promise")
            pg.evaluate("() => document.fonts.ready")
            pg.wait_for_timeout(200)
            heights = pg.evaluate(
                "[...document.querySelectorAll('.qa-block')]"
                ".map(e=>e.getBoundingClientRect().height)")
            b.close()
    finally:
        tmp.unlink(missing_ok=True)
    return heights


def main(argv):
    files = [Path(a) for a in argv[1:]] or sorted(
        (ROOT / "data/content").glob("*.json"))
    blocks = []
    for f in files:
        blocks.extend(blocks_for(f))
    if not blocks:
        print("no renderable revision blocks found")
        return 0
    heights = measure(blocks)
    fails, capacities = 0, []
    print(f"A4 sheet content box: {CONTENT_W} x {CONTENT_H:.0f} px "
          f"(210x297mm, margins 18/16mm, 260mm fixed sheet, 8mm folio zone)\n")
    print(f'{"block":<44}{"words":>6}{"height":>9}{"page%":>7}  verdict')
    for (bid, _html, w), h in zip(blocks, heights):
        pct = h / CONTENT_H * 100
        ok = h <= CONTENT_H
        fails += (not ok)
        if w > 40:                       # prose-bearing blocks calibrate capacity
            capacities.append(w * CONTENT_H / h)
        print(f'{bid:<44}{w:>6}{h:>8.0f}px{pct:>6.0f}%  '
              f'{"PASS" if ok else "OVERFLOW"}')
    if capacities:
        capacities.sort()
        med = capacities[len(capacities) // 2]
        print(f"\nMeasured page capacity (extrapolated from these blocks): "
              f"min {capacities[0]:.0f}, median {med:.0f} words/page "
              f"at current density — authors' provisional budget is 320-420.")
    print(f"\n{len(blocks)} block(s), {fails} overflow(s).")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
