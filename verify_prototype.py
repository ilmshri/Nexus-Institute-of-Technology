#!/usr/bin/env python3
"""Prove the Years 1-2 prototype contains no route to Years 3-4.

"Hidden" is only safe to publish if a visitor cannot reach an unauthored
course by ANY route — not the curriculum listing, not search, not Resources,
not a next-course link, not the Arabic mirror. This asserts that, and fails
loudly rather than reporting a pass it did not earn.

Scope widened from Year 1 to Years 1-2 on 2026-08-03 (owner, "scope = C").
Both the hidden set and every expected count moved with it: 24 courses and
264 lessons instead of 12 and 132.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTO = ROOT / "docs" / "prototype"
HIDDEN_SEMS = ("y3s1", "y3s2", "y4s1", "y4s2")
SHOWN_SEMS = ("y1s1", "y1s2", "y2s1", "y2s2")
N_COURSES, N_LESSONS = 24, 264

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
check("no Y3-Y4 directories on disk", not stray, str(stray[:5]))

# 2. no hidden-semester reference in any emitted HTML (EN or AR)
hits = {}
for f in html_files:
    txt = f.read_text(encoding="utf-8", errors="ignore")
    for s in HIDDEN_SEMS:
        if s in txt:
            hits.setdefault(s, []).append(str(f.relative_to(PROTO)))
check("no Y3-Y4 reference in any HTML",
      not hits, "; ".join(f"{k} in {v[:2]}" for k, v in hits.items()))

# 3. search index contains Year 1 only
idx_path = PROTO / "curriculum" / "search-index.json"
if idx_path.exists():
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    bad = [e for e in idx if any(s in json.dumps(e, ensure_ascii=False) for s in HIDDEN_SEMS)]
    check(f"search index Years 1-2 only ({len(idx)} entries)", not bad, f"{len(bad)} leaked")
    check(f"search index has all {N_LESSONS} Y1+Y2 lessons", len(idx) == N_LESSONS, f"got {len(idx)}")
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
courses = sorted(p.name for s in SHOWN_SEMS for p in (curr / s).iterdir()
                 if (curr / s).is_dir() and p.is_dir())
check(f"{N_COURSES} Y1+Y2 courses present ({len(courses)})",
      len(courses) == N_COURSES, str(courses))

# 6. every Y1 lesson page is full-depth (has a quiz) — nothing half-built ships
thin = []
for s in SHOWN_SEMS:
    for cdir in sorted((curr / s).iterdir()):
        if not cdir.is_dir():
            continue
        for page in sorted(cdir.glob("*.html")):
            if page.name in ("index.html", "summary.html"):
                continue
            if "quiz-item" not in page.read_text(encoding="utf-8", errors="ignore"):
                thin.append(f"{s}/{cdir.name}/{page.name}")
check(f"all lesson pages carry a quiz ({N_LESSONS - len(thin)}/{N_LESSONS})", not thin,
      f"{len(thin)} thin: {thin[:3]}")

# 7. the Arabic mirror exists and is likewise filtered
ar = PROTO / "ar"
check("Arabic mirror present", ar.is_dir(), "missing")
if ar.is_dir():
    ar_hits = [str(p.relative_to(PROTO)) for p in ar.rglob("*.html")
               if any(s in p.read_text(encoding="utf-8", errors="ignore") for s in HIDDEN_SEMS)]
    check("Arabic mirror Years 1-2 only", not ar_hits, str(ar_hits[:3]))

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

# 10. the page must not claim a scope it does not contain. The 2026-07-26
#     prototype shipped "4 YEARS / 48 COURSES / 528 LESSONS" on a 12-course
#     build; that was its one untrue claim and it is now an assertion.
idx_txt = (PROTO / "index.html").read_text(encoding="utf-8", errors="ignore")
overclaims = [c for c in ("<b>48</b>", "<b>528</b>", "<b>4</b><span>years",
                          "4 YEARS", "8 SEMESTERS", "48 COURSES")
              if c in idx_txt]
check("homepage does not overclaim scope", not overclaims, str(overclaims))
truthful = [c for c in ("<b>24</b>", "<b>264</b>", "<b>2</b><span>years")
            if c in idx_txt]
check(f"homepage states the real scope ({len(truthful)}/3 markers)",
      len(truthful) == 3, f"found {truthful}")

# 11. no NAVIGABLE hidden-year reference. The semester-id scan above passes
#     "#year-3" and the words "Year 3" — neither contains "y3s1" — and a live
#     page check found exactly that leak in the Curriculum nav dropdown.
#
#     Scoped deliberately to ANCHORS AND LINKS, not prose. Lesson bodies say
#     things like "the bridge lesson into the Year 3 Vibrations course" and
#     "Year 4's asset-integrity coursework"; those are a curriculum telling a
#     student what comes later, not a route to an unauthored page. An earlier
#     draft of this check flagged all 12 of them and would have pushed someone
#     into deleting good editorial copy. Do not widen it back to bare text.
nav_leaks = {}
for f in html_files:
    txt = f.read_text(encoding="utf-8", errors="ignore")
    for token in ('#year-3"', '#year-4"', ">Year 3</a>", ">Year 4</a>"):
        if token in txt:
            nav_leaks.setdefault(token, []).append(str(f.relative_to(PROTO)))
check("no hidden-year anchors or nav links",
      not nav_leaks,
      "; ".join(f"{k} in {len(v)} file(s) e.g. {v[0]}"
                for k, v in nav_leaks.items()))

print("PASS")
for n in notes:
    print("  ok   " + n)
if fails:
    print("\nFAIL")
    for f in fails:
        print("  X    " + f)
    sys.exit(1)
print(f"\nAll checks passed — {len(html_files)} pages, Years 1-2 only.")
