#!/usr/bin/env python3
"""ASU maroon+gold palette SAMPLE (owner request, 2026-07-31) — a browsable
draft tree at design-previews/palette-asu/, built from the real docs/ slice.

Faithful to ASU brand colours already recorded in this repo's history
(maroon #8C1D40, gold #FFC627), with derived shades where the current system
needs depth steps. ASU's own contrast rule is kept: #FFC627 is never text on
white — text-gold uses a darkened tone. NOTHING here ships unless the owner
chooses; the live palette is untouched.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DEST = ROOT / "design-previews" / "palette-asu"
LOGOS = ROOT / "design-previews" / "logo-candidates"

SLICE = [
    "index.html",
    "curriculum/index.html",
    "curriculum/y1s1/math-1/index.html",
    "curriculum/y1s1/math-1/01-functions-units-and-engineering-magnitudes.html",
    "curriculum/y1s1/math-1/02-limits-and-continuity.html",
    "curriculum/y1s1/math-1/03-the-derivative-as-a-rate.html",
]

TOKENS = """
/* ASU palette sample — token overrides only; layout/type untouched. */
:root{
  --ink:#2B2A28;--soft:#4C4A46;--muted:#716E68;--faint:#9E9A93;
  --accent:#8C1D40;--accent-deep:#66142E;--accent-ink:#7A1938;
  --tint:#F9EEF1;--tint-line:#EACBD6;
  --gold:#DFA800;--gold-soft:#FFC627;--gold-tint:#FFF5D9;
  --amber:#B98C00;--amber-tint:var(--gold-tint);
  --navy:#55102A;
  --shadow:0 1px 2px rgba(60,20,35,.06);
  --nx-panel:#55102A;--nx-panel-soft:#6E1632;
  --nx-teal:#8C1D40;--nx-teal-d:#8C1D40;--nx-teal-dd:#66142E;--nx-teal-h:#66142E;
  --nx-amber:#FFC627;--nx-amber-d:#B98C00;
  --nx-grad:linear-gradient(135deg,#8C1D40 0%,#66142E 100%);
  --nx-grad-hero:linear-gradient(135deg,#55102A 0%,#6E1632 55%,#8C1D40 100%);
}
.pal-tag{position:fixed;bottom:10px;inset-inline-start:10px;z-index:999;font:600 11px/1 var(--sans);
color:var(--soft);background:var(--surface);border:1px solid var(--line-strong);
border-radius:6px;padding:6px 9px;box-shadow:var(--shadow);pointer-events:none;opacity:.92}
@media print{.pal-tag{display:none}}
"""

RECOLOR = {"#14294B": "#8C1D40", "#C9A45C": "#FFC627", "#CBA85F": "#FFC627", "#20325A": "#2B2A28"}


def recolour_svg(src: Path, dest: Path):
    s = src.read_text()
    for old, new in RECOLOR.items():
        s = s.replace(old, new).replace(old.lower(), new)
    dest.write_text(s)


def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    (DEST / "assets").mkdir(parents=True)
    shutil.copytree(ROOT / "assets" / "nx", DEST / "assets" / "nx")
    # ASU-recoloured incumbent logo so the header matches the sample palette
    recolour_svg(ROOT / "nexus" / "logo.svg", DEST / "assets" / "nx" / "logo.svg")
    # ASU-recoloured round-2 family, kept alongside for the gallery
    for name in ("r2-wordmark.svg", "r2-shield-dot.svg", "r2-lockup-h.svg"):
        recolour_svg(LOGOS / name, LOGOS / name.replace(".svg", "-asu.svg"))

    inject = f"<style id=\"pal-asu\">{TOKENS}</style>\n"
    for rel in SLICE:
        html = (DOCS / rel).read_text(encoding="utf-8")
        html = html.replace("</head>", inject + "</head>", 1)
        html = html.replace(
            "</body>", '<div class="pal-tag">Palette sample — ASU maroon &amp; gold</div></body>', 1)
        target = DEST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
    print(f"palette-asu: {len(SLICE)} pages + recoloured logo family")


if __name__ == "__main__":
    main()
