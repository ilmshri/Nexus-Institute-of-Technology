#!/usr/bin/env python3
"""Motion-treatment draft trees (design session, 2026-07-31).

Copies a REAL content slice from docs/ (home, curriculum index, MTH 101 course
page, lessons 01-03) into design-previews/motion-{a,b,c}/ and overlays one
transition treatment per tree. Content is untouched; each overlay is a single
injected <style> + <script type="speculationrules"> block, so the treatments
are exactly what would ship in nexus.css if chosen.

Also emits motion-{a,b,c}-slow/ with 8x durations — screenshot rigs only,
never for judging feel.

Run from the repo root:  python3 design-previews/build_motion.py
Serve with:              python3 -m http.server -d design-previews 8123
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "design-previews"

SLICE = [
    "index.html",
    "curriculum/index.html",
    "curriculum/y1s1/math-1/index.html",
    "curriculum/y1s1/math-1/01-functions-units-and-engineering-magnitudes.html",
    "curriculum/y1s1/math-1/02-limits-and-continuity.html",
    "curriculum/y1s1/math-1/03-the-derivative-as-a-rate.html",
]

# Same-origin prefetch on hover/pointerdown; external/new-tab links excluded.
SPECRULES = (
    '<script type="speculationrules">'
    '{"prefetch":[{"where":{"and":[{"href_matches":"/*"},'
    '{"not":{"selector_matches":"a[target]"}}]},"eagerness":"moderate"}]}'
    "</script>"
)

# Entry-only fade for the course/lesson tab panels (they currently snap).
TABS = """
@media (prefers-reduced-motion: no-preference){
  html.js .tabpanel.on{transition:opacity .22s ease,translate .22s cubic-bezier(.2,.7,.2,1)}
  @starting-style{ html.js .tabpanel.on{opacity:0;translate:0 {TABDY}px} }
}
"""

TREATMENTS = {
    "a": {
        "tag": "Treatment A — Quiet Crossfade",
        "tabdy": 0,
        "css": """
/* A — Quiet Crossfade+: the shipped root fade, retuned; nothing held, nothing moves. */
::view-transition-old(root){animation-duration:.14s;animation-timing-function:ease-out}
::view-transition-new(root){animation-duration:.22s;animation-timing-function:ease-in-out}
""",
    },
    "b": {
        "tag": "Treatment B — Held Chrome, Threaded Titles",
        "tabdy": 0,
        "css": """
/* B — chrome holds still; the title you clicked travels into the page you land on. */
.appbar{view-transition-name:appbar}
.player .outline{view-transition-name:outline}
::view-transition-old(root){animation-duration:.14s;animation-timing-function:ease-out}
::view-transition-new(root){animation-duration:.22s;animation-timing-function:ease-in-out}
::view-transition-group(*){animation-duration:.3s;animation-timing-function:cubic-bezier(.2,.7,.2,1)}
@media (prefers-reduced-motion: reduce){
  .appbar,.player .outline{view-transition-name:none}
}
""",
    },
    "c": {
        "tag": "Treatment C — Paper Lay-down",
        "tabdy": 6,
        "css": """
/* C — editorial: the old sheet lifts away fast, the new sheet settles onto the desk. */
.appbar{view-transition-name:appbar}
@keyframes mtc-lift{to{opacity:0}}
@keyframes mtc-settle{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
::view-transition-old(root){animation:mtc-lift .12s ease-out both}
::view-transition-new(root){animation:mtc-settle .3s cubic-bezier(.2,.7,.2,1) both}
@media (prefers-reduced-motion: reduce){
  .appbar{view-transition-name:none}
  ::view-transition-old(root),::view-transition-new(root){animation:none}
}
""",
    },
}

TAGCSS = """
.mt-tag{position:fixed;bottom:10px;inset-inline-start:10px;z-index:999;font:600 11px/1 var(--sans);
color:var(--soft);background:var(--surface);border:1px solid var(--line-strong);
border-radius:6px;padding:6px 9px;box-shadow:var(--shadow);pointer-events:none;opacity:.92}
@media print{.mt-tag{display:none}}
"""


def stamp_b(rel: str, html: str) -> str:
    """Treatment B only: per-element view-transition-names on real markup."""
    if rel == "curriculum/index.html":
        html = html.replace(
            'data-key="y1s1/math-1" data-n="11">\n  <span class="code">MTH 101</span>\n  <h4>',
            'data-key="y1s1/math-1" data-n="11">\n  <span class="code">MTH 101</span>\n'
            '  <h4 style="view-transition-name:course-t-math1">',
            1,
        )
    elif rel == "curriculum/y1s1/math-1/index.html":
        html = html.replace(
            "<h1>Engineering Mathematics I</h1>",
            '<h1 style="view-transition-name:course-t-math1">Engineering Mathematics I</h1>',
            1,
        )
        # thread each copied lesson's syllabus link to its page H1
        for n in ("01", "02", "03"):
            html = re.sub(
                r'(<h4>)(<a href="%s-[^"]+\.html">)' % n,
                r'<h4 style="view-transition-name:lesson-t-%s">\2' % n,
                html,
                count=1,
            )
    else:
        m = re.search(r"/(0[123])-[^/]+\.html$", "/" + rel)
        if m:
            html = re.sub(
                r"(<div class=\"lesson-head\">.*?)<h1>",
                r'\1<h1 style="view-transition-name:lesson-t-%s">' % m.group(1),
                html,
                count=1,
                flags=re.S,
            )
    return html


def build(letter: str, spec: dict, slow: int = 1) -> Path:
    name = f"motion-{letter}" + ("-slow" if slow > 1 else "")
    dest = OUT / name
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "assets").mkdir(parents=True)
    shutil.copytree(ROOT / "assets" / "nx", dest / "assets" / "nx")
    # the site build copies the logo into assets/nx at emit time; mirror that
    shutil.copy(ROOT / "nexus" / "logo.svg", dest / "assets" / "nx" / "logo.svg")
    # don't triplicate the 3.6MB hero loop in git — symlink back to the repo copy
    mp4 = dest / "assets" / "nx" / "hero-loop.mp4"
    if mp4.exists():
        mp4.unlink()
        mp4.symlink_to("../../../../assets/nx/hero-loop.mp4")

    css = spec["css"] + TABS.replace("{TABDY}", str(spec["tabdy"])) + TAGCSS
    if slow > 1:
        css = re.sub(r"\.(\d+)s", lambda m: f"{int(m.group(1)) * slow / 100:.2f}s", css)
    tag = spec["tag"] + (" (8x slow capture rig)" if slow > 1 else "")
    inject = f"<style id=\"mt-{letter}\">{css}</style>\n{SPECRULES}\n"

    for rel in SLICE:
        src = DOCS / rel
        html = src.read_text(encoding="utf-8")
        if letter == "b":
            html = stamp_b(rel, html)
        html = html.replace("</head>", inject + "</head>", 1)
        html = html.replace("</body>", f'<div class="mt-tag">{tag}</div></body>', 1)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
    return dest


if __name__ == "__main__":
    for letter, spec in TREATMENTS.items():
        d = build(letter, spec)
        build(letter, spec, slow=8)
        n = len(list(d.rglob("*.html")))
        print(f"{d.name}: {n} pages")
    print("done — serve design-previews/ and open motion-a|b|c/index.html")
