#!/usr/bin/env python3
"""MechEd visual variants (owner order 2026-07-26: pure visual/design work).

Copies three REAL built pages per variant out of docs/ and layers a small
override stylesheet on top of the committed MechEd system. Pure preview
tooling — the site generator, its emission logic, and the i18n layer are
untouched. Serve the worktree root and open
  design-previews/meched-variants/index.html
"""
import re, posixpath, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
HERE = pathlib.Path(__file__).resolve().parent

PAGES = [
    ("home.html",   "index.html", ""),
    ("course.html", "curriculum/y2s1/electronics-sensors/index.html",
     "curriculum/y2s1/electronics-sensors/"),
    ("lesson.html", "curriculum/y2s1/electronics-sensors/08-vibration-and-speed-sensors.html",
     "curriculum/y2s1/electronics-sensors/"),
]
VARIANTS = ["charter", "gallery", "majlis"]
ATTR = re.compile(r'(href|src|poster)="([^"]+)"')

def rooted(html, origdir):
    def fix(m):
        a, u = m.groups()
        if u.startswith(("http", "#", "/", "data:", "mailto")):
            return m.group(0)
        return f'{a}="{posixpath.normpath("/docs/" + origdir + u)}"'
    html = ATTR.sub(fix, html)
    # keep nexus.js path lookups (search index, sw) pointed at the real tree
    return re.sub(r'data-root="[^"]*"', 'data-root="/docs/"', html)

def main():
    for v in VARIANTS:
        out = HERE / v
        out.mkdir(exist_ok=True)
        for name, src, origdir in PAGES:
            html = (DOCS / src).read_text(encoding="utf-8")
            html = rooted(html, origdir)
            html = html.replace(
                "</head>", f'<link rel="stylesheet" href="../{v}.css">\n</head>')
            html = html.replace("<title>", f"<title>[{v.upper()}] ", 1)
            (out / name).write_text(html, encoding="utf-8")
        print(f"{v}: {len(PAGES)} pages")

if __name__ == "__main__":
    main()
