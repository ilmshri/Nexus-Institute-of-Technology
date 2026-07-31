#!/usr/bin/env python3
"""Round 2 — the two directions the owner picked, built into a proper family.

r2-wordmark      MechEd + gold rule + EN descriptor (no Arabic, per owner)
r2-shield-dot    shield + serif M + gold pivot dot
r2-shield-nodot  shield + serif M, dot removed (for the owner's dot question)
r2-lockup-h      shield beside wordmark — the university-crest lockup
r2-stack         ceremonial stack for print covers
System colours only; all letters outlined paths.
"""
from pathlib import Path

from outline import shape, FDIR

NAVY, INK, GOLD, CREAM = "#14294B", "#20325A", "#CBA85F", "#FAF8F4"
OUT = Path("/Users/ilmshri/Social Media/nexus-design-drafts/design-previews/logo-candidates")
SERIF = FDIR / "SourceSerif4%5Bopsz%2Cwght%5D.ttf"
SANS = FDIR / "SourceSans3%5Bwght%5D.ttf"

dW, advW, _ = shape(SERIF, "MechEd", axes={"opsz": 40, "wght": 620})
dEN, advEN, _ = shape(SANS, "ENGINEERED TO INNOVATE", axes={"wght": 540}, tracking=210)
dM, advM, _ = shape(SERIF, "M", axes={"opsz": 40, "wght": 640})

SHIELD = "M32 5 L54 12 V32 C54 46 45 55 32 60 C19 55 10 46 10 32 V12 Z"
KEYLINE = "M32 9.5 L50 15.3 V32 C50 43.6 42.6 51.6 32 55.9 C21.4 51.6 14 43.6 14 32 V15.3 Z"


def g(d, adv, scale, cx, by, fill):
    tx = cx - adv * scale / 2
    return (f'<g transform="translate({tx:.2f} {by:.2f}) scale({scale:.5f})">'
            f'<path d="{d}" fill="{fill}"/></g>')


def shield_group(dot=True, tx=0.0, ty=0.0, s=1.0):
    dotel = f'<circle cx="32" cy="47.5" r="2.0" fill="{GOLD}"/>' if dot else ""
    inner = (f'<path d="{SHIELD}" fill="{CREAM}" stroke="{NAVY}" stroke-width="3"/>'
             f'<path d="{KEYLINE}" fill="none" stroke="{GOLD}" stroke-width="1.3"/>'
             + g(dM, advM, 36 / 1000, 32, 41.5, NAVY) + dotel)
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{inner}</g>'


def write(name, viewbox, body, label):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" '
           f'aria-label="{label}">\n<!-- MechEd round-2 candidate — system colours, outlined type -->\n'
           f'{body}\n</svg>\n')
    (OUT / name).write_text(svg)
    print(name)


# shields
write("r2-shield-dot.svg", "0 0 64 64", shield_group(True), "MechEd shield")
write("r2-shield-nodot.svg", "0 0 64 64", shield_group(False), "MechEd shield")

# wordmark (no Arabic): MechEd / gold rule / EN caps centred
W, H = 640, 190
sW, sEN = 100 / 1000, 15 / 1000
wm_w = advW * sW
cx = W / 2
body = "\n".join([
    g(dW, advW, sW, cx, 100, NAVY),
    f'<line x1="{cx - wm_w/2:.1f}" y1="126" x2="{cx + wm_w/2:.1f}" y2="126" '
    f'stroke="{GOLD}" stroke-width="1.6"/>',
    g(dEN, advEN, sEN, cx, 156, INK),
])
write("r2-wordmark.svg", f"0 0 {W} {H}", body, "MechEd — Engineered to Innovate")

# horizontal crest lockup: shield left, wordmark + descriptor right
W2, H2 = 620, 160
s2 = 1.7
sh_h = 64 * s2
sW2, sEN2 = 82 / 1000, 12.6 / 1000
wm_w2 = advW * sW2
x_text = 196
body = "\n".join([
    shield_group(True, tx=26, ty=(H2 - sh_h) / 2 + 2, s=s2),
    f'<line x1="168" y1="36" x2="168" y2="124" stroke="{GOLD}" stroke-width="1.4"/>',
    f'<g transform="translate({x_text} 92) scale({sW2:.5f})"><path d="{dW}" fill="{NAVY}"/></g>',
    f'<g transform="translate({x_text + 2} 122) scale({sEN2:.5f})"><path d="{dEN}" fill="{INK}"/></g>',
])
write("r2-lockup-h.svg", f"0 0 {W2} {H2}", body, "MechEd crest lockup")

# ceremonial stack
W3, H3 = 380, 300
s3 = 1.6
body = "\n".join([
    shield_group(True, tx=(W3 - 64 * s3) / 2, ty=14, s=s3),
    g(dW, advW, 86 / 1000, W3 / 2, 202, NAVY),
    f'<line x1="{W3/2 - advW*86/2000:.1f}" y1="224" x2="{W3/2 + advW*86/2000:.1f}" y2="224" '
    f'stroke="{GOLD}" stroke-width="1.5"/>',
    g(dEN, advEN, 12.2 / 1000, W3 / 2, 250, INK),
])
write("r2-stack.svg", f"0 0 {W3} {H3}", body, "MechEd ceremonial lockup")
