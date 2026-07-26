#!/usr/bin/env python3
"""Prove the Year-1 prototype contains no route to Years 2-4.

"Hidden" is only safe to publish if a visitor cannot reach an unauthored
course by ANY route — not the curriculum listing, not search, not Resources,
not a next-course link, not the Arabic mirror. This asserts that, and fails
loudly rather than reporting a pass it did not earn.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTO = ROOT / "docs" / "prototype"
HIDDEN_SEMS = ("y2s1", "y2s2", "y3s1", "y3s2", "y4s1", "y4s2")

fails, notes = [], []


def check(name, ok, detail=""):
    (notes if ok else fails).append(f"{name}{'' if ok else '  -> ' + detail}")


# 0. built at all
check("prototype directory exists", PROTO.is_dir(), str(PROTO))
if not PROTO.is_dir():
    print("FAIL: prototype not built"); sys.exit(1)

html_files = sorted(PROTO.rglob("*.html"))
check("prototype emitted pages", len(html_files) > 0, "no html")

# 1. no hidden-semester directories on disk
stray = [str(p.relative_to(PROTO)) for s in HIDDEN_SEMS for p in PROTO.rglob(s) if p.is_dir()]
check("no Y2-Y4 directories on disk", not stray, str(stray[:5]))

# 2. no hidden-semester reference in any emitted HTML (EN or AR)
hits = {}
for f in html_files:
    txt = f.read_text(encoding="utf-8", errors="ignore")
    for s in HIDDEN_SEMS:
        if s in txt:
            hits.setdefault(s, []).append(str(f.relative_to(PROTO)))
check("no Y2-Y4 reference in any HTML",
      not hits, "; ".join(f"{k} in {v[:2]}" for k, v in hits.items()))

# 3. search index contains Year 1 only
idx_path = PROTO / "curriculum" / "search-index.json"
if idx_path.exists():
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    bad = [e for e in idx if any(s in json.dumps(e, ensure_ascii=False) for s in HIDDEN_SEMS)]
    check(f"search index Year-1 only ({len(idx)} entries)", not bad, f"{len(bad)} leaked")
    check("search index has the full 132 Y1 lessons", len(idx) == 132, f"got {len(idx)}")
else:
    check("search index exists", False, "missing")

# 4. every internal link resolves to a file that exists
broken = []
for f in html_files:
    txt = f.read_text(encoding="utf-8", errors="ignore")
    for href in re.findall(r'href="([^"#?]+)"', txt):
        if href.startswith(("http://", "https://", "mailto:", "data:", "#")):
            continue
        target = (f.parent / href).resolve()
        if not target.exists():
            broken.append(f"{f.relative_to(PROTO)} -> {href}")
check("no broken internal links", not broken, f"{len(broken)}: {broken[:3]}")

# 5. all 12 Year-1 courses are present and reachable
curr = PROTO / "curriculum"
courses = sorted(p.name for s in ("y1s1", "y1s2") for p in (curr / s).iterdir()
                 if (curr / s).is_dir() and p.is_dir())
check(f"12 Year-1 courses present ({len(courses)})", len(courses) == 12, str(courses))

# 6. every Y1 lesson page is full-depth (has a quiz) — nothing half-built ships
thin = []
for s in ("y1s1", "y1s2"):
    for cdir in sorted((curr / s).iterdir()):
        if not cdir.is_dir():
            continue
        for page in sorted(cdir.glob("*.html")):
            if page.name in ("index.html", "summary.html"):
                continue
            if "quiz-item" not in page.read_text(encoding="utf-8", errors="ignore"):
                thin.append(f"{s}/{cdir.name}/{page.name}")
check(f"all Year-1 lesson pages carry a quiz ({132 - len(thin)}/132)", not thin,
      f"{len(thin)} thin: {thin[:3]}")

# 7. the Arabic mirror exists and is likewise filtered
ar = PROTO / "ar"
check("Arabic mirror present", ar.is_dir(), "missing")
if ar.is_dir():
    ar_hits = [str(p.relative_to(PROTO)) for p in ar.rglob("*.html")
               if any(s in p.read_text(encoding="utf-8", errors="ignore") for s in HIDDEN_SEMS)]
    check("Arabic mirror Year-1 only", not ar_hits, str(ar_hits[:3]))

# 8. no absolute-root links (would break under a /prototype/ subpath)
abs_links = []
for f in html_files:
    abs_links += re.findall(r'(?:href|src)="(/[^"]*)"', f.read_text(encoding="utf-8", errors="ignore"))
check("no absolute-root links (subpath-safe)", not abs_links, str(sorted(set(abs_links))[:3]))

# 9. brand check — prototype must carry MechEd, not the old name
idx_html = (PROTO / "index.html").read_text(encoding="utf-8", errors="ignore")
check("homepage carries MechEd", "MechEd" in idx_html, "wordmark missing")
old = sum("Nexus Institute" in f.read_text(encoding="utf-8", errors="ignore") for f in html_files)
check("no old-brand residue", old == 0, f"{old} pages")

print("PASS")
for n in notes:
    print("  ok   " + n)
if fails:
    print("\nFAIL")
    for f in fails:
        print("  X    " + f)
    sys.exit(1)
print(f"\nAll checks passed — {len(html_files)} pages, Year 1 only.")
