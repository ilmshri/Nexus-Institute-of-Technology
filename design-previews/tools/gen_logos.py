#!/usr/bin/env python3
"""MechEd logo candidates — clean flat SVGs, system colours only, no <text> elements.

Colours used (all already in the shipped system):
  navy #14294B (--navy / logo navy)   ink #20325A (--ink)
  gold #CBA85F (--gold token)         cream #FAF8F4 (logo field / theme-color)
Candidate 1 is the incumbent monogram byte-for-byte (its gold is #C9A45C —
the one place the mark and the CSS token differ; flagged to the owner).
"""
import math
import shutil
from pathlib import Path

from outline import shape, FDIR

NAVY, INK, GOLD, CREAM = "#14294B", "#20325A", "#CBA85F", "#FAF8F4"
OUT = Path("/Users/ilmshri/Social Media/nexus-design-drafts/design-previews/logo-candidates")
OUT.mkdir(exist_ok=True)

SERIF = FDIR / "SourceSerif4%5Bopsz%2Cwght%5D.ttf"
SANS = FDIR / "SourceSans3%5Bwght%5D.ttf"
ARAB = FDIR / "IBMPlexSansArabic-SemiBold.ttf"


def glyph_group(d, adv, scale, cx, baseline_y, fill):
    """Centre a shaped run horizontally at cx, baseline at baseline_y."""
    tx = cx - adv * scale / 2
    return (f'<g transform="translate({tx:.2f} {baseline_y:.2f}) scale({scale:.5f})">'
            f'<path d="{d}" fill="{fill}"/></g>')


def tile(inner, name, rx=13):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" '
           f'aria-label="MechEd monogram">\n'
           f'<!-- MechEd logo candidate — flat vectors, system colours, no text elements -->\n'
           f'<rect x="1.5" y="1.5" width="61" height="61" rx="{rx}" fill="{CREAM}" '
           f'stroke="{NAVY}" stroke-width="3"/>\n{inner}\n</svg>\n')
    (OUT / name).write_text(svg)
    print(name)


# serif M (display optical size, semibold-plus)
dM, advM, _ = shape(SERIF, "M", axes={"opsz": 40, "wght": 640})

# ---- C1: incumbent (copy verbatim) ----
shutil.copy("/Users/ilmshri/Social Media/nexus-design-drafts/nexus/logo.svg", OUT / "c1-incumbent.svg")
print("c1-incumbent.svg (copied)")

# ---- C2: serif-M tile (wordmark's own letter as the mark) ----
s = 44 / 1000  # cap height ~29px in a 64 tile
inner = (f'<rect x="8" y="8" width="48" height="48" rx="8" fill="none" '
         f'stroke="{GOLD}" stroke-width="1.4"/>\n'
         + glyph_group(dM, advM, s, 32, 45.0, NAVY)
         + f'\n<circle cx="32" cy="51.5" r="2.2" fill="{GOLD}"/>')
tile(inner, "c2-serif-m.svg")

# ---- C4: gear-coin ----
def gear_ring(cx, cy, r_root, r_tip, teeth, tooth_frac=0.42):
    pts = []
    for i in range(teeth):
        a0 = 2 * math.pi * i / teeth
        a1 = a0 + 2 * math.pi * tooth_frac / teeth / 2
        a2 = a0 + 2 * math.pi / teeth / 2
        a3 = a0 + 2 * math.pi / teeth / 2 + 2 * math.pi * tooth_frac / teeth / 2
        a4 = a0 + 2 * math.pi / teeth
        for r, a in ((r_tip, a0), (r_tip, a1), (r_root, a2), (r_root, a3), (r_tip, a4)):
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"

sc = 36 / 1000
ring = gear_ring(32, 32, 27.0, 30.4, 12, 0.46)
inner_cut = 'M32 8.4 A23.6 23.6 0 1 0 32.01 8.4 Z'
coin = (f'<path d="{ring} {inner_cut}" fill="{NAVY}" fill-rule="evenodd"/>\n'
        f'<circle cx="32" cy="32" r="23.6" fill="{CREAM}"/>\n'
        f'<circle cx="32" cy="32" r="20.8" fill="none" stroke="{GOLD}" stroke-width="1.2"/>\n'
        + glyph_group(dM, advM, sc, 32, 43.0, NAVY)
        + f'\n<circle cx="32" cy="48.6" r="1.9" fill="{GOLD}"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" '
       f'aria-label="MechEd monogram">\n<!-- gear-coin candidate -->\n{coin}\n</svg>\n')
(OUT / "c4-gear-coin.svg").write_text(svg)
print("c4-gear-coin.svg")

# ---- C5: moment arc over slab M (mines the incumbent's M) ----
slab_m = (f'<path d="M19 45 V22 L32 36 L45 22 V45" fill="none" stroke="{NAVY}" '
          f'stroke-width="5.2" stroke-linecap="square" stroke-linejoin="miter"/>')
arc = (f'<path d="M36.2 8.6 A 24 24 0 0 1 55.4 27.8" fill="none" stroke="{GOLD}" '
       f'stroke-width="2" stroke-linecap="round"/>\n'
       f'<circle cx="55.4" cy="27.8" r="2.3" fill="{GOLD}"/>')
tile(f'{arc}\n{slab_m}', "c5-moment-arc.svg")

# ---- C6: shield ----
shield_path = "M32 5 L54 12 V32 C54 46 45 55 32 60 C19 55 10 46 10 32 V12 Z"
inner_shield = "M32 9.5 L50 15.3 V32 C50 43.6 42.6 51.6 32 55.9 C21.4 51.6 14 43.6 14 32 V15.3 Z"
sc6 = 36 / 1000
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" '
       f'aria-label="MechEd shield">\n<!-- shield candidate -->\n'
       f'<path d="{shield_path}" fill="{CREAM}" stroke="{NAVY}" stroke-width="3"/>\n'
       f'<path d="{inner_shield}" fill="none" stroke="{GOLD}" stroke-width="1.3"/>\n'
       + glyph_group(dM, advM, sc6, 32, 41.5, NAVY)
       + f'\n<circle cx="32" cy="47.5" r="2.0" fill="{GOLD}"/>\n</svg>\n')
(OUT / "c6-shield.svg").write_text(svg)
print("c6-shield.svg")

# ---- C3: the full wordmark lockup (wide) ----
dW, advW, _ = shape(SERIF, "MechEd", axes={"opsz": 40, "wght": 620})
dEN, advEN, _ = shape(SANS, "ENGINEERED TO INNOVATE", axes={"wght": 540}, tracking=210)
dAR, advAR, _ = shape(ARAB, "هندسةٌ للابتكار", direction="rtl", script="Arab", lang="ar")

W, H = 640, 200
sW = 96 / 1000            # wordmark scale: cap ~64px
sEN = 15.5 / 1000         # caps line
sAR = 26 / 1000
wm_w = advW * sW
cx = W / 2
base_wm = 96
rule_y = 122
desc_y = 152
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
       f'aria-label="MechEd — Engineered to Innovate">',
       '<!-- wordmark lockup candidate: Source Serif 4 (OFL) outlined, hand-kept as paths -->',
       glyph_group(dW, advW, sW, cx, base_wm, NAVY),
       f'<line x1="{cx - wm_w/2:.1f}" y1="{rule_y}" x2="{cx + wm_w/2:.1f}" y2="{rule_y}" '
       f'stroke="{GOLD}" stroke-width="1.6"/>',
       # EN caps left-aligned to rule start, AR right-aligned to rule end (itqan pattern)
       f'<g transform="translate({cx - wm_w/2:.1f} {desc_y}) scale({sEN:.5f})">'
       f'<path d="{dEN}" fill="{INK}"/></g>',
       f'<g transform="translate({cx + wm_w/2 - advAR*sAR:.1f} {desc_y + 2}) scale({sAR:.5f})">'
       f'<path d="{dAR}" fill="{INK}"/></g>',
       '</svg>', '']
(OUT / "c3-wordmark-lockup.svg").write_text("\n".join(svg))
print("c3-wordmark-lockup.svg")

# compact header lockup for c3 (wordmark alone, for the 30px appbar slot)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {advW*sW + 8:.0f} 110" role="img" aria-label="MechEd">',
       glyph_group(dW, advW, sW, (advW * sW + 8) / 2, 88, NAVY), '</svg>', '']
(OUT / "c3-wordmark-only.svg").write_text("\n".join(svg))
print("c3-wordmark-only.svg")
