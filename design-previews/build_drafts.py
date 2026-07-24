#!/usr/bin/env python3
"""
Nexus design-draft preview assembler.

Reads REAL generated pages from docs/ (never modified), extracts their content
blocks byte-for-byte, and re-wraps them in three alternative design shells:

  draft-a-foundry/  — industrial / workshop-HMI register
  draft-b-press/    — academic / technical-editorial register
  draft-c-atlas/    — learning-console / product register

Curriculum text, lesson bodies, quiz items, career copy: UNTOUCHED (verbatim
inner HTML). The only copy this script rewrites is site CHROME (nav labels,
hero/CTA/footer sentences) — and it applies the owner's binding cost rule
(no "free"/paywall wording) to that chrome, which the current live homepage
violates. See design-previews/README.md.
"""
import re, shutil, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT  = ROOT / "design-previews"

LESSON_SRC = DOCS / "curriculum/y2s1/electronics-sensors/08-vibration-and-speed-sensors.html"
COURSE_SRC = DOCS / "curriculum/y2s1/electronics-sensors/index.html"
CURR_SRC   = DOCS / "curriculum/index.html"
HOME_SRC   = DOCS / "index.html"

SEM_NAMES = {"y1s1":"Year 1 · Semester 1","y1s2":"Year 1 · Semester 2",
             "y2s1":"Year 2 · Semester 1","y2s2":"Year 2 · Semester 2",
             "y3s1":"Year 3 · Semester 1","y3s2":"Year 3 · Semester 2",
             "y4s1":"Year 4 · Semester 1","y4s2":"Year 4 · Semester 2"}
ROMAN = {"y1s1":"I","y1s2":"II","y2s1":"III","y2s2":"IV","y3s1":"V","y3s2":"VI","y4s1":"VII","y4s2":"VIII"}

FOOT_TEXT = ("Open engineering education — preliminary prototype release; learner feedback "
             "shapes the final, tailored releases. Worked-example values are pedagogical; "
             "representative industrial figures are labeled as such and are not published "
             "operating data of any named company. Every visual is an original vector "
             "illustration. Lessons not yet at full depth say so honestly.")

MATHJAX = ("<script>MathJax={tex:{inlineMath:[['\\\\(','\\\\)']]},svg:{fontCache:'global'}};</script>\n"
           "<script defer src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js\"></script>")

FONTS = {
 "a": "https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@500;600;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap",
 "b": "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&family=IBM+Plex+Mono:wght@400;500&display=swap",
 "c": "https://fonts.googleapis.com/css2?family=Geist:wght@400..700&family=Geist+Mono:wght@400..600&display=swap",
}

# ---------------------------------------------------------------- extraction
def read(p): return p.read_text(encoding="utf-8")

def block(src, marker, start=0):
    """Return (outer, inner, end_index) of the balanced <div> starting at marker."""
    i = src.index(marker, start)
    j = src.index(">", i) + 1
    depth, k = 1, j
    while depth:
        m = re.search(r"<div\b|</div>", src[k:])
        if not m: raise ValueError("unbalanced div for " + marker)
        k += m.end()
        depth += 1 if m.group(0) == "<div" else -1
    return src[i:k], src[j:k-6], k

def blocks_all(src, marker):
    out, pos = [], 0
    while True:
        i = src.find(marker, pos)
        if i < 0: return out
        outer, inner, pos = block(src, marker, i)
        out.append((outer, inner))

def first(pattern, src, flags=re.S):
    m = re.search(pattern, src, flags)
    return m.group(1) if m else ""

# ---- lesson ----------------------------------------------------------------
L = read(LESSON_SRC)
lesson = {
    "eyebrow": first(r'<p class="eyebrow">(.*?)</p>', L),
    "title":   first(r'<h1>(.*?)</h1>', L),
    "sub":     first(r'<p class="sub">(.*?)</p>', L),
    "meta":    re.findall(r'<div>([^<]+)<b>(.*?)</b></div>', block(L, '<div class="meta">')[1]),
    "source":  first(r'<div class="src-strip">.*?<b>(.*?)</b>', L),
    "panels":  {m.group(1): m.group(2) for m in
                re.finditer(r'<section class="tabpanel(?: on)?" id="(t-\w+)">(.*?)</section>', L, re.S)},
    "outline": re.findall(r'<a href="([^"]+)" class="ol( cur)?"[^>]*><span class="tick"></span><span>(.*?)</span></a>', L),
    "prev":    first(r'<nav class="prevnext"><a href="[^"]*">(.*?)</a>', L),
    "next":    re.findall(r'<a href="[^"]*">([^<]*?)</a></nav>', L),
}
lesson["video_todo"] = "lib-video-todo" in first(r'(<div class="video-hero">.*?)<div class="tabs"', L)

# ---- course ----------------------------------------------------------------
C = read(COURSE_SRC)
course = {
    "eyebrow": first(r'<p class="eyebrow">(.*?)</p>', C),
    "title":   first(r'<h1>(.*?)</h1>', C),
    "sub":     first(r'<p class="sub">(.*?)</p>', C),
    "chips":   re.findall(r'<span class="mchip">(.*?)</span>', C),
    "learn":   block(C, '<div class="learn-grid">')[1],
    "career":  block(C, '<div class="career-block">')[0],
    "next":    re.sub(r'\s*(?:→|&rarr;|&#8594;)\s*$', '',
                      first(r'<nav class="coursenav">.*?<a class="cn-link" href="[^"]*">(.*?)</a>', C)),
}
course_syls = []
for outer, inner in blocks_all(C, '<div class="syl" '):
    course_syls.append({
        "href":  first(r'data-href="([^"]+)"', outer),
        "no":    first(r'<div class="no">(\d+)</div>', outer),
        "title": first(r'<h4><a href="[^"]*">(.*?)</a>', outer),
        "badge": first(r'<span class="badge[^"]*">(.*?)</span>', outer),
        "scope": first(r'<p class="scope">(.*?)</p>', outer),
        "src":   first(r'<p class="src">(.*?)</p>', outer),
        "det":   first(r'<details>(.*?)</details>', outer),
    })

# ---- curriculum ------------------------------------------------------------
K = read(CURR_SRC)
tracker = re.search(r'<b>(\d+) of (\d+)</b> lessons at full teaching depth · (\d+)%', K)
tr_n, tr_total, tr_pct = tracker.group(1), tracker.group(2), tracker.group(3)
tr_def = first(r'<p class="small">(Full depth = .*?)</p>', K)
cards = []
for m in re.finditer(r'<a class="course-card" href="([^"]+)" data-sem="(\w+)"\s+data-key="([^"]+)" data-n="(\d+)">\s*'
                     r'<span class="cap">(<svg.*?</svg>)</span>\s*<span class="code">(.*?)</span>\s*'
                     r'<h4>(.*?)</h4>\s*<p>(.*?)</p>\s*<span class="meta">(.*?)</span>', K, re.S):
    href, sem, key, n, svg, code, title, desc, meta = m.groups()
    meta_txt = re.sub(r"<.*?>", "", meta)
    status = "done" if "complete" in meta_txt else ("amber" if "built" in meta_txt else "queued")
    cards.append(dict(href=href, sem=sem, key=key, n=n, svg=svg, code=code,
                      title=title, desc=desc.replace("…","&hellip;"), meta=meta_txt, status=status))

# ---- homepage --------------------------------------------------------------
H = read(HOME_SRC)
home = {
    "eyebrow": first(r'<p class="eyebrow">(.*?)</p>', H),
    "h1":      first(r'<h1>(.*?)</h1>', H),
    "sub":     first(r'<p class="sub">(.*?)</p>', H, re.S),
    "chips":   first(r'<div>Curriculum<b>(.*?)</b></div>', H),
    "stats":   re.findall(r'<div class="stat"><b>(.*?)</b><span>(.*?)</span></div>', H),
    "feats":   re.findall(r'<a class="feat-card" href="([^"]+)">\s*<span class="code">(.*?)</span>'
                          r'<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*<span class="meta">(.*?)</span></a>', H, re.S),
    "notes":   re.findall(r'<div class="note"><p class="ncap">(.*?)</p><h3>(.*?)</h3>\s*<p>(.*?)</p></div>', H, re.S),
}
tracks = []
for outer, inner in blocks_all(H, '<div class="track">'):
    tracks.append({
        "cap":   first(r'<p class="tcap">(.*?)</p>', outer),
        "title": first(r'<h3>(.*?)</h3>', outer),
        "small": first(r'<p class="small">(.*?)</p>', outer),
        "rows":  re.findall(r'<a class="trow" href="([^"]+)"><span class="tcode">(.*?)</span><span>(.*?)</span>', outer),
    })
# chrome-copy compliance (owner cost rule) — chrome only, never lesson content
home["notes"] = [(cap, h3, p.replace("No paywalls, no accounts.", "No accounts needed.")) for cap, h3, p in home["notes"]]
# prototype-phase positioning (owner directive 2026-07-24): the site is a
# preliminary open release for trial and reflection, not the final product
if len(home["notes"]) >= 3:
    cap3, _h3, p3 = home["notes"][2]
    home["notes"][2] = (cap3, "Open prototype",
        "A preliminary release, public so real learners can try it and reflect — that feedback "
        "tunes the final, tailored releases. No accounts needed; every equation derived or "
        "sourced, every number machine-verified, every depth label honest.")

# ---------------------------------------------------------------- link rewiring
COURSE_HTML = "y2s1/electronics-sensors/index.html"
LESSON_HTML = "08-vibration-and-speed-sensors.html"

def rewire(href):
    h = href.split("#")[0]
    if h.endswith(LESSON_HTML): return "lesson.html"
    if h.endswith(COURSE_HTML) or h == "index.html" and "electronics" in href: return "course.html"
    if h.endswith("curriculum/index.html"): return "curriculum.html"
    return "#"

def relink(html_block, mapping=None):
    def sub(m):
        href = m.group(1)
        if mapping and href in mapping: return f'href="{mapping[href]}"'
        return f'href="{rewire(href)}"'
    return re.sub(r'href="([^"#][^"]*)"', sub, html_block)

# ---------------------------------------------------------------- shared shell bits
def head(draft, title, desc, extra=""):
    return f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="../shared/logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS[draft]}">
<link rel="stylesheet" href="draft.css">
{extra}
</head>
<body>"""

def tail():
    return '\n<a class="hubchip" href="../index.html">&larr; Draft hub</a>\n<script src="../shared/drafts.js"></script>\n</body>\n</html>\n'

NAV_PAGES = [("index.html","Home"), ("curriculum.html","Curriculum"), ("course.html","ELX 205"), ("lesson.html","Lesson 08")]
def navlinks(current):
    out = []
    for href, label in NAV_PAGES:
        on = ' class="on"' if href == current else ""
        out.append(f'<a href="{href}"{on}>{label}</a>')
    dead = "".join(f'<a href="#" title="Outside this preview">{x}</a>' for x in ("Reference","Career Paths"))
    return "".join(out) + dead

# ════════════════════════════════════════════════ DRAFT A — FOUNDRY ═════════
def a_appbar(current):
    return f"""
<div class="hazard-strip"></div>
<header class="appbar"><div class="in">
  <a class="brand" href="index.html"><img src="../shared/logo.svg" alt="">
    <span><span class="txt"><em>Nexus</em> Institute of Technology</span>
    <small>Online Engineering Education</small></span></a>
  <nav>{navlinks(current)}</nav>
</div></header>"""

def a_foot():
    return f"""
<footer class="foot"><div class="hazard-strip"></div><div class="in">
  <div><div class="mark"><em>NEXUS</em> INSTITUTE OF TECHNOLOGY</div>
  <p>{FOOT_TEXT}</p></div>
  <nav><a href="index.html">Home</a><a href="curriculum.html">Curriculum</a>
  <a href="course.html">ELX 205</a><a href="lesson.html">Lesson 08</a></nav>
</div></footer>"""

A_SCHEMATIC = """<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#3D4756" stroke-width="1.6" aria-hidden="true">
<circle cx="330" cy="180" r="118"/><circle cx="330" cy="180" r="86" stroke-dasharray="5 7"/>
<circle cx="330" cy="180" r="30" stroke="#F5A623"/><circle cx="330" cy="180" r="9" fill="#F5A623" stroke="none"/>
<g stroke="#4A5568">""" + "".join(
    f'<line x1="{330+118*__import__("math").cos(a/12*6.28318):.1f}" y1="{180+118*__import__("math").sin(a/12*6.28318):.1f}" x2="{330+140*__import__("math").cos(a/12*6.28318):.1f}" y2="{180+140*__import__("math").sin(a/12*6.28318):.1f}"/>'
    for a in range(12)) + """</g>
<line x1="330" y1="20" x2="330" y2="340" stroke-dasharray="10 8" stroke-width="1"/>
<line x1="170" y1="180" x2="490" y2="180" stroke-dasharray="10 8" stroke-width="1"/>
<circle cx="120" cy="300" r="58"/><circle cx="120" cy="300" r="20" stroke="#14CFA0"/>
<line x1="120" y1="230" x2="120" y2="370" stroke-dasharray="8 7" stroke-width="1"/>
<line x1="178" y1="300" x2="272" y2="180" stroke="#F5A623" stroke-dasharray="4 6"/>
<rect x="60" y="60" width="130" height="64" stroke-width="1.4"/>
<line x1="60" y1="82" x2="190" y2="82" stroke-width="1"/><line x1="126" y1="82" x2="126" y2="124" stroke-width="1"/>
<text x="70" y="76" fill="#5F6975" font-family="monospace" font-size="11" stroke="none">NX-0528</text>
<text x="70" y="104" fill="#5F6975" font-family="monospace" font-size="9" stroke="none">SCALE 1:1</text>
<text x="134" y="104" fill="#5F6975" font-family="monospace" font-size="9" stroke="none">REV C</text>
</svg>"""

def a_rows(rows_cards):
    out = []
    for c in rows_cards:
        badge = {"done": '<span class="badge done">Complete</span>',
                 "amber": '<span class="badge amber">In build</span>',
                 "queued": '<span class="badge queued">Queued</span>'}[c["status"]]
        out.append(f"""<a class="row" href="{rewire(c['href'])}" data-course data-sem="{c['sem']}" data-search="{(c['code']+' '+c['title']+' '+c['desc']).lower()}">
<span class="code">{c['code'].split(' ·')[0]}</span><span class="title">{c['title']}</span>
<span class="desc">{c['desc']}</span><span class="stat">{badge}</span></a>""")
    return "".join(out)

def build_a_home():
    stats_cells = "".join(
        f'<div class="cell"><b>{v}</b><span>{lbl}</span>' +
        (f'<div class="bar"><i style="width:{tr_pct}%"></i></div>' if "%" in lbl else "") + "</div>"
        for v, lbl in home["stats"])
    feats = a_rows([dict(href=h, sem="", code=c.split(" ·")[0], title=t, desc=p, status="done", meta=m)
                    for h, c, t, p, m in home["feats"]])
    track_sheets = ""
    for t in tracks:
        rows = "".join(f'<a class="row" href="{rewire(h)}"><span class="code">{c}</span><span class="title">{n}</span><span class="stat">&rarr;</span></a>'
                       for h, c, n in t["rows"])
        track_sheets += f"""<div class="specsheet compact panel"><div class="panel-cap"><b>{t['cap']}</b><span>{t['title']}</span></div>{rows}</div>"""
    notes = "".join(f"""<div class="panel brackets" style="padding:20px 22px"><div class="d-eyebrow">{cap}</div>
<h2 style="font-size:20px">{h3}</h2><p style="color:var(--muted);font-size:14px;margin:10px 0 0">{p}</p></div>"""
                    for cap, h3, p in home["notes"])
    page = head("a", "Nexus Institute of Technology — Draft A · Foundry",
                "Design draft A — industrial register preview.") + a_appbar("index.html") + f"""
<section class="hero"><div class="hero-schematic">{A_SCHEMATIC}</div><div class="in">
  <p class="d-eyebrow">{home['eyebrow']}</p>
  <h1>Learn Mechanical Engineering <span class="amber">from Scratch to Industry&nbsp;4.0.</span></h1>
  <p class="d-sub">{home['sub']}</p>
  <div class="spec-chips"><div>Phase<b>Prototype · Open build</b></div><div>Curriculum<b>{home['chips']}</b></div><div>Assessment<b>Machine-verified quizzes</b></div><div>Depth ledger<b>{tr_n} / {tr_total} lessons · {tr_pct}%</b></div></div>
  <div class="cta-row"><a class="btn" href="curriculum.html">Explore the curriculum &rarr;</a>
  <a class="btn btn-ghost" href="#" title="Outside this preview">About the institute</a></div>
</div></section>
<main class="wrap">
<section class="sect"><div class="telemetry brackets">{stats_cells}</div></section>
<section class="sect"><div class="sect-head"><span class="no">NO. 01</span><h2>A cross-section of the program</h2>
<span class="aux">Complete educational units live today</span></div>
<div class="specsheet">{feats}</div></section>
<section class="sect"><div class="sect-head"><span class="no">NO. 02</span><h2>Two tracks, one pathway</h2></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px" class="tracks-grid">{track_sheets}</div>
<style>@media(max-width:880px){{.tracks-grid{{grid-template-columns:1fr!important}}}}</style></section>
<section class="sect"><div class="sect-head"><span class="no">NO. 03</span><h2>Built like a program, not a playlist</h2></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px" class="notes-grid">{notes}</div>
<style>@media(max-width:880px){{.notes-grid{{grid-template-columns:1fr!important}}}}</style></section>
<section class="sect"><div class="panel brackets" style="display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;padding:26px 28px">
<div><p class="d-eyebrow">Ready when you are</p><h2>Start with Lesson 01.</h2></div>
<a class="btn" href="curriculum.html">Explore the curriculum &rarr;</a></div></section>
</main>""" + a_foot() + tail()
    return page

def build_a_curriculum():
    bays = ""
    for sem, name in SEM_NAMES.items():
        semcards = [c for c in cards if c["sem"] == sem]
        done = sum(1 for c in semcards if c["status"] == "done")
        bays += f"""<section class="bay" data-semgroup><div class="bay-head"><span class="tag">Bay {ROMAN[sem]}</span>
<h3>{name}</h3><div class="rule"></div><span class="count">{done} of {len(semcards)} complete</span></div>
<div class="specsheet">{a_rows(semcards)}</div></section>"""
    chips = '<button type="button" class="chip on" data-sem="all">All</button>' + "".join(
        f'<button type="button" class="chip" data-sem="{s}">{SEM_NAMES[s]}</button>' for s in SEM_NAMES)
    page = head("a", "Curriculum — Draft A · Foundry", "Design draft A curriculum preview.") + a_appbar("curriculum.html") + f"""
<main class="wrap">
<div class="pagehead"><p class="d-eyebrow">Curriculum · 4 years · 8 semesters</p>
<h1>48 courses. 528 lessons. One pathway.</h1>
<p class="d-sub">The complete B.S.-shaped map — from foundational mathematics and physics to Industry 4.0 —
covering every core mechanical-engineering discipline and role. The catalog is a strict grid — 6 classes
per semester, 11 lessons per class — built as authored content, never as padding.</p>
<div class="tracker-strip brackets"><div class="lbl"><span>DEPTH LEDGER — RECOMPUTED EVERY BUILD</span><span><b>{tr_n} / {tr_total}</b> LESSONS AT FULL DEPTH · {tr_pct}%</span></div>
<div class="bar"><i style="width:{tr_pct}%"></i></div><p class="foot">{tr_def}</p></div>
<div class="searchbox"><input type="search" id="lessonSearch" placeholder="SEARCH ALL 528 LESSONS — TITLE, COURSE, KEYWORDS" aria-label="Search lessons"><span class="kbd">&#8984;K</span></div>
<div class="chips" id="semChips">{chips}</div></div>
{bays}
</main>""" + a_foot() + tail()
    return page

def a_sheethead(tabname):
    code = course["eyebrow"].split(" ·")[0]
    return (f'<div class="sheet-head"><span><b>NEXUS</b> · {code} · LESSON 08 OF 11</span>'
            f'<span>{tabname}</span><span>SHEET 08 · REV A</span></div>')

def build_a_lesson():
    outline = "".join(
        f'<a href="{rewire(h)}" class="ol{cur}"{" aria-current=&quot;page&quot;" if cur else ""}><span class="tick"></span><span>{label}</span></a>'
        for h, cur, label in lesson["outline"])
    meta = "".join(f'<div><span>{k.strip()}</span><b>{v}</b></div>' for k, v in lesson["meta"])
    tabnames = {"t-lecture":"LECTURE","t-foundations":"FOUNDATIONS","t-examples":"EXAMPLES AND QUIZ","t-library":"LIBRARY"}
    panels = ""
    for pid, label in tabnames.items():
        on = " on" if pid == "t-lecture" else ""
        panels += (f'<section class="tabpanel{on}" id="{pid}"><div class="sheet">{a_sheethead(label)}'
                   f'<div class="sheet-body">{lesson["panels"][pid]}</div></div></section>')
    tabs = "".join(f'<button{" class=&quot;on&quot;" if i==0 else ""} data-tab="{pid}">{label.title() if pid!="t-examples" else "Examples and Quiz"}</button>'
                   for i,(pid,label) in enumerate(tabnames.items()))
    tabs = tabs.replace('&quot;', '"')
    video = ('<div class="video-status"><span class="dot"></span>Lecture video — in production. Only verified, approved-channel embeds ship.</div>'
             if lesson["video_todo"] else "")
    page = head("a", f"{lesson['title']} — Draft A · Foundry", "Design draft A lesson preview.", MATHJAX) + a_appbar("lesson.html") + f"""
<main><div class="player">
<aside class="outline" aria-label="Course outline"><div class="oh"><a href="course.html">ELX 205 · Electronics &amp; Sensors</a>
<div class="bar"><i style="width:64%"></i></div><span class="ptext">7 OF 11 COMPLETE — PREVIEW STATE</span></div>{outline}</aside>
<div class="lesson-main">
<nav class="crumbs"><a href="curriculum.html">Curriculum</a> / <a href="course.html">ELX 205</a> / <span>Lesson 08 of 11</span></nav>
<div class="lesson-head panel brackets"><p class="d-eyebrow">{lesson['eyebrow']}</p>
<h1>{lesson['title']}</h1><p class="d-sub">{lesson['sub']}</p>
<div class="lesson-meta">{meta}</div></div>
<div class="lesson-tools"><button class="complete-btn" type="button">Mark as complete</button>
<span class="src-strip"><span class="t">Sourced from</span>{lesson['source']}</span></div>
{video}
<div class="tabs" role="tablist">{tabs}</div>
{panels}
<nav class="prevnext"><a href="#">&larr; 07 · Pressure and level measurement in depth</a><a href="course.html">All lessons · ELX 205</a><a href="#">09 · Analog-to-digital and sampling &rarr;</a></nav>
<nav class="coursenav"><span class="cn-label">Next course</span><a class="cn-link" href="#">{course['next']} &rarr;</a></nav>
</div></div></main>""" + a_foot() + tail()
    return page

def build_a_course():
    chips = course["chips"]
    tb = (f'<div class="tb-grid"><div><span>Part no.</span><b>{course["eyebrow"].split(" ·")[0]}</b></div>'
          f'<div><span>Placement</span><b>Year 2 · Semester 1</b></div>'
          f'<div><span>Lessons</span><b>{chips[0]}</b></div>'
          f'<div><span>Status</span><b>{chips[1].upper()}</b></div></div>')
    syls = ""
    for s in course_syls:
        badge = '<span class="badge done">Full lesson</span>'
        det = f'<details>{s["det"]}</details>' if s["det"] else ""
        syls += f"""<div class="syl"><span class="tick">{s['no']}</span><div><h4><a href="{rewire(s['href'])}">{s['title']}</a>{badge}</h4>
<p class="scope">{s['scope']}</p><p class="src">{s['src']}</p>{det}</div><span class="tickno">SHEET {s['no']} / 11</span></div>"""
    learn = f'<div class="learn panel-x"><div class="panel-cap"><b>WHAT YOU\'LL LEARN</b><span>SIX WORKING OUTCOMES</span></div><div class="body">{re.sub(r"<h3>.*?</h3>", "", course["learn"], flags=re.S)}</div></div>'
    page = head("a", "Electronics & Sensors — Draft A · Foundry", "Design draft A course preview.", MATHJAX) + a_appbar("course.html") + f"""
<main class="wrap">
<nav class="crumbs" style="margin:22px 0 0"><a href="curriculum.html">Curriculum</a> / <span>ELX 205</span></nav>
<div class="titleblock brackets"><div class="tb-main"><p class="d-eyebrow">{course['eyebrow']}</p>
<h1>{course['title']}</h1><p class="d-sub">{course['sub']}</p></div>{tb}</div>
<div class="cta-row"><a class="btn" href="lesson.html">Start lesson 01 &rarr;</a>
<a class="btn btn-ghost" href="#" title="Outside this preview">Course summary (PDF)</a>
<a class="btn btn-dim" href="curriculum.html">Full curriculum</a></div>
{learn}
<div class="syllabus"><div class="sect-head" style="margin-top:44px"><span class="no">SYLLABUS</span><h2>Eleven lessons, in working order</h2></div>{syls}</div>
{relink(course['career'])}
<div class="nextcourse"><span class="lbl">Next course</span><a href="#">{course['next']} &rarr;</a></div>
</main>""" + a_foot() + tail()
    return page

# ════════════════════════════════════════════════ DRAFT B — PRESS ═══════════
def b_masthead(current):
    return f"""
<header class="masthead"><div class="in">
  <a class="brand" href="index.html"><img src="../shared/logo.svg" alt="">
    <span><span class="txt">Nexus Institute of Technology</span>
    <small>Online Engineering Education · Est. MMXXVI</small></span></a>
  <nav>{navlinks(current)}</nav>
</div></header>"""

def b_foot():
    return f"""
<footer class="foot"><div class="in">
  <div class="mark">Nexus Institute of Technology</div>
  <span class="sc">Online Engineering Education</span>
  <nav><a href="index.html">Home</a><a href="curriculum.html">Curriculum</a>
  <a href="course.html">ELX 205</a><a href="lesson.html">Lesson 08</a></nav>
  <p>{FOOT_TEXT}</p>
</div></footer>"""

B_PLATE = """<figure class="plate"><svg viewBox="0 0 560 250" xmlns="http://www.w3.org/2000/svg" fill="none" stroke-width="1.5" aria-hidden="true">
<circle cx="150" cy="125" r="78"/><circle cx="150" cy="125" r="60" stroke-dasharray="4 6"/><circle cx="150" cy="125" r="16"/>
<circle cx="286" cy="125" r="52"/><circle cx="286" cy="125" r="38" stroke-dasharray="4 6"/><circle cx="286" cy="125" r="12"/>
<circle cx="386" cy="125" r="40"/><circle cx="386" cy="125" r="28" stroke-dasharray="4 6"/><circle cx="386" cy="125" r="9" class="amb"/>
<line x1="60" y1="125" x2="480" y2="125" stroke-dasharray="9 7" stroke-width="1"/>
<line x1="150" y1="35" x2="150" y2="215" stroke-dasharray="9 7" stroke-width="1"/>
<path d="M470 60 h60 M470 60 l8 -5 v10 z" stroke-width="1"/>
<text x="60" y="228" font-size="11" font-family="monospace" stroke="none" fill="#6E675C">RATIO 24 : 16 : 12 — MESHING TRAIN, SINGLE REDUCTION</text>
</svg><figcaption><b>Plate I.</b> Power transmission by meshing gear train — the opening figure of the
program's machine-design spine. Every visual on the platform is an original vector illustration.</figcaption></figure>"""

def build_b_home():
    idx_entries = "".join(
        f'<a class="entry" href="curriculum.html"><span class="t">{SEM_NAMES[s]}</span><span class="dots"></span><span class="folio">{ROMAN[s]}</span></a>'
        for s in SEM_NAMES)
    stats_line = " ".join(f"<b>{v}</b>&nbsp;{lbl.replace(' · 36%','')} ·" for v, lbl in home["stats"]).rstrip("·")
    feats = "".join(f"""<div class="entry-course"><span class="folio">{c.split(" ·")[0]} — {m.title().replace("·","·")}</span>
<h4><a href="{rewire(h)}">{t}</a></h4><p>{p}</p></div>""" for h, c, t, p, m in home["feats"])
    track_cols = ""
    for t in tracks:
        rows = "".join(f'<a class="entry" href="{rewire(h)}"><span class="folio">{c}</span><span class="t" style="font-size:15.5px">{n}</span><span class="dots"></span></a>'
                       for h, c, n in t["rows"])
        track_cols += f"""<div><h3 style="font-family:var(--disp);font-weight:520;font-size:22px;margin:0 0 4px">{t['title']}</h3>
<p style="font-size:13.5px;color:var(--muted);font-style:italic;margin:0 0 14px">{t['small']}</p>
<div class="contents" style="border:0;padding:0">{rows}</div></div>"""
    notes = "".join(f"""<div><span class="sc" style="color:var(--crimson)">{h3}</span>
<p style="font-size:15px;line-height:1.75;color:var(--soft);margin:10px 0 0">{p}</p></div>""" for _, h3, p in home["notes"])
    page = head("b", "Nexus Institute of Technology — Draft B · Press", "Design draft B — editorial register preview.") + b_masthead("index.html") + f"""
<main class="wrap">
<section class="front"><div class="grid">
<div><div class="kick"><span class="folio">Vol. I — The Complete Curriculum</span></div>
<h1>Learn Mechanical Engineering <span class="it">from scratch</span> to Industry&nbsp;4.0.</h1>
<p class="standfirst">{home['sub']}</p>
<div class="colophon-line"><span><b>Preliminary edition</b> — issued openly for review</span><span>·</span><span><b>{home['chips']}</b></span><span>·</span><span><b>{tr_n} of {tr_total}</b> lessons at full depth ({tr_pct}%)</span><span>·</span><span>every number machine-verified</span></div>
<div class="cta-row"><a class="btn" href="curriculum.html">Open the catalogue</a><a class="btn btn-ghost" href="course.html">Sample a course</a></div></div>
<div class="contents"><h3>In this catalogue</h3>{idx_entries}
<div style="margin-top:34px">{B_PLATE}</div></div>
</div></section>
<section class="sect"><div class="sect-head"><span class="folio">No. 01</span><h2>A cross-section of the program</h2>
<p class="note">Complete educational units — lecture, foundations, verified quiz, and library — live today.</p></div>
<hr class="rule-double"><div class="catalogue two">{feats}</div></section>
<section class="sect"><div class="sect-head"><span class="folio">No. 02</span><h2>Two tracks, one pathway</h2></div>
<hr class="rule-double"><div style="display:grid;grid-template-columns:1fr 1fr;gap:54px" class="btracks">{track_cols}</div>
<style>@media(max-width:880px){{.btracks{{grid-template-columns:1fr!important}}}}</style></section>
<section class="sect"><div class="sect-head"><span class="folio">No. 03</span><h2>Built like a program, not a playlist</h2></div>
<hr class="rule-double"><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:44px" class="bnotes">{notes}</div>
<style>@media(max-width:880px){{.bnotes{{grid-template-columns:1fr!important}}}}</style></section>
<section class="sect" style="padding-bottom:20px"><hr class="rule-double">
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;padding-top:22px">
<h2 style="font-size:26px">Start with Lesson 01.</h2>
<a class="btn" href="curriculum.html">Open the catalogue</a></div></section>
</main>""" + b_foot() + tail()
    return page

def build_b_curriculum():
    chapters = ""
    for sem, name in SEM_NAMES.items():
        semcards = [c for c in cards if c["sem"] == sem]
        done = sum(1 for c in semcards if c["status"] == "done")
        entries = ""
        for c in semcards:
            stat = {"done": '<b>complete</b>', "amber": '<b class="due">in build</b>', "queued": "queued"}[c["status"]]
            entries += f"""<div class="entry-course" data-course data-sem="{c['sem']}" data-search="{(c['code']+' '+c['title']+' '+c['desc']).lower()}">
<span class="folio">{c['code']}</span><h4><a href="{rewire(c['href'])}">{c['title']}</a></h4>
<p>{c['desc']}</p><span class="stat">{c['n']} lessons — {stat}</span></div>"""
        chapters += f"""<section class="chapter" data-semgroup><div class="chapter-head"><span class="folio">Chapter {ROMAN[sem]}</span>
<h3>{name}</h3><div class="rule"></div><span class="count">{done} of {len(semcards)} complete</span></div>
<div class="catalogue two">{entries}</div></section>"""
    chips = '<button type="button" class="chip on" data-sem="all">All chapters</button>' + "".join(
        f'<button type="button" class="chip" data-sem="{s}">{ROMAN[s]} — {SEM_NAMES[s].replace("Year ","Y").replace(" · Semester ","S")}</button>' for s in SEM_NAMES)
    page = head("b", "The Catalogue — Draft B · Press", "Design draft B curriculum preview.") + b_masthead("curriculum.html") + f"""
<main class="wrap">
<div class="pagehead"><div class="kick"><span class="folio">The Catalogue</span></div>
<h1>48 courses. 528 lessons. <span style="font-style:italic;font-weight:480;color:var(--crimson)">One pathway.</span></h1>
<p class="standfirst">The complete B.S.-shaped map — from foundational mathematics and physics to Industry 4.0 —
covering every core mechanical-engineering discipline and role, sequenced the way engineering schools actually teach.
A strict grid: 6 classes per semester, 11 lessons per class, built as authored content, never as padding.</p>
<div class="tracker-line"><div class="lbl"><span>Depth you can audit — recomputed from the content at every build</span>
<span><b>{tr_n} of {tr_total}</b> lessons at full depth · {tr_pct}%</span></div>
<div class="bar"><i style="width:{tr_pct}%"></i></div><p class="foot">{tr_def}</p></div>
<div class="searchbox"><input type="search" id="lessonSearch" placeholder="Search the catalogue — title, course, keywords&hellip;" aria-label="Search lessons"><span class="kbd">&#8984;K</span></div>
<div class="chips" id="semChips">{chips}</div></div>
{chapters}
</main>""" + b_foot() + tail()
    return page

def build_b_course():
    learn_cols = re.sub(r"<h3>.*?</h3>", "", course["learn"], flags=re.S)
    syls = ""
    for s in course_syls:
        det = f'<details>{s["det"]}</details>' if s["det"] else ""
        syls += f"""<div class="syl"><div class="no">{s['no']}</div><div><h4><a href="{rewire(s['href'])}">{s['title']}</a>
<span class="badge">Full lesson</span></h4><p class="scope">{s['scope']}</p><p class="src">{s['src']}</p>{det}</div></div>"""
    chips_line = " · ".join(course["chips"])
    page = head("b", "Electronics & Sensors — Draft B · Press", "Design draft B course preview.", MATHJAX) + b_masthead("course.html") + f"""
<main class="wrap">
<nav class="crumbs"><a href="curriculum.html">The Catalogue</a> / Chapter III / <span>ELX 205</span></nav>
<article><header class="article-head"><div class="kick"><span class="folio">{course['eyebrow']}</span></div>
<h1>{course['title']}</h1><p class="standfirst">{course['sub']}</p>
<div class="byline"><span><b>{chips_line}</b></span></div></header>
<div class="cta-row"><a class="btn" href="lesson.html">Begin — Lesson 01</a>
<a class="btn btn-ghost" href="#" title="Outside this preview">Course summary (PDF)</a></div>
<div class="learn"><h3>Contents &amp; aims</h3><div class="body">{learn_cols}</div></div>
<div class="syllabus"><h3>The eleven lessons</h3>{syls}</div>
{relink(course['career'])}
<div class="nextcourse"><span class="lbl">Next in the catalogue</span><a href="#">{course['next']} &rarr;</a></div>
</article></main>""" + b_foot() + tail()
    return page

def build_b_lesson():
    rail = "".join(
        f'<a href="{rewire(h)}"{" class=&quot;cur&quot;" if cur else ""}><span class="folio">{label.split(" · ")[0]}</span><span>{label.split(" · ",1)[1]}</span></a>'
        for h, cur, label in lesson["outline"]).replace("&quot;", '"')
    meta_line = " · ".join(f"<b>{v}</b>" for _, v in lesson["meta"])
    video = ('<p class="video-status"><span class="dot"></span>The lecture film for this lesson is in production — '
             'only verified, approved-channel recordings are ever embedded.</p>'
             if lesson["video_todo"] else "")
    panels = "".join(f'<section class="tabpanel{" on" if pid=="t-lecture" else ""}" id="{pid}">{inner}</section>'
                     for pid, inner in lesson["panels"].items())
    page = head("b", f"{lesson['title']} — Draft B · Press", "Design draft B lesson preview.", MATHJAX) + b_masthead("lesson.html") + f"""
<div class="lesson-shell"><main class="lesson-main">
<nav class="crumbs"><a href="curriculum.html">Catalogue</a> / <a href="course.html">ELX 205</a> / Lesson 08 of 11</nav>
<header class="lesson-head"><div class="kick"><span class="folio">{lesson['eyebrow']}</span></div>
<h1>{lesson['title']}</h1><p class="standfirst">{lesson['sub']}</p>
<div class="byline">{meta_line}</div>
<div class="lesson-tools"><button class="complete-btn" type="button">Mark as complete</button>
<span class="src-strip"><span class="t">Sourced from</span><i>{lesson['source']}</i></span></div>
{video}</header>
<nav class="tabs" role="tablist"><button class="on" data-tab="t-lecture">Lecture</button>
<button data-tab="t-foundations">Foundations</button><button data-tab="t-examples">Examples &amp; Quiz</button>
<button data-tab="t-library">Library</button></nav>
{panels}
<nav class="prevnext"><a href="#">&larr; 07 · Pressure and level measurement</a><a href="course.html">All lessons</a><a href="#">09 · Analog-to-digital &rarr;</a></nav>
<nav class="coursenav"><span class="cn-label">Next course</span><a class="cn-link" href="#">{course['next']} &rarr;</a></nav>
</main>
<aside class="margin-rail"><h5>In this course</h5>{rail}</aside>
</div>""" + b_foot() + tail()
    return page

# ════════════════════════════════════════════════ DRAFT C — ATLAS ═══════════
def c_appbar(current):
    return f"""
<header class="appbar"><div class="in">
  <a class="brand" href="index.html"><img src="../shared/logo.svg" alt="">
    <span class="txt"><em>Nexus</em> Institute of Technology</span></a>
  <nav>{navlinks(current)}</nav>
  <span class="spacer"></span>
  <button class="kbtn" type="button" onclick="var s=document.getElementById('lessonSearch');if(s){{s.focus()}}else{{location.href='curriculum.html'}}">
  Search 528 lessons <span class="kbd">&#8984;K</span></button>
</div></header>"""

def c_foot():
    return f"""
<footer class="foot"><div class="in">
  <div class="mark"><em>Nexus</em> Institute of Technology</div>
  <nav><a href="index.html">Home</a><a href="curriculum.html">Curriculum</a>
  <a href="course.html">ELX 205</a><a href="lesson.html">Lesson 08</a></nav>
  <p>{FOOT_TEXT}</p>
</div></footer>"""

def c_ccard(c):
    pct = {"done": 100, "amber": 9, "queued": 0}[c["status"]]
    chip = {"done": '<span class="chip-status done">Complete</span>',
            "amber": '<span class="chip-status prog">In build</span>',
            "queued": '<span class="chip-status dim">Queued</span>'}[c["status"]]
    return f"""<a class="ccard" href="{rewire(c['href'])}" data-course data-sem="{c['sem']}" data-search="{(c['code']+' '+c['title']+' '+c['desc']).lower()}">
<div class="top"><span class="glyph">{c['svg']}</span><span class="code">{c['code'].split(' ·')[0]}</span><span style="margin-inline-start:auto">{chip}</span></div>
<h3>{c['title']}</h3><p>{c['desc']}</p>
<div class="foot"><span class="bar"><i style="width:{pct}%"></i></span><span class="n">{c['n']} lessons</span></div></a>"""

def build_c_home():
    console_rows = ""
    demo = [("ELX 205","Electronics & Sensors — L08 · Vibration and speed sensors",64),
            ("MTH 207","Engineering Mathematics III — complete",100),
            ("FLD 203","Fluid Mechanics — complete",100)]
    glyphs = {c["code"].split(" ·")[0]: c["svg"] for c in cards}
    for code, label, pct in demo:
        console_rows += f"""<div class="citem"><span class="glyph">{glyphs.get(code,"")}</span>
<span class="cmeta"><b>{label}</b><span>{code}</span></span>
<span class="cbar"><span class="bar"><i style="width:{pct}%"></i></span><span>{pct}%</span></span></div>"""
    feats = "".join(c_ccard(dict(href=h, sem="", svg=glyphs.get(c.split(" ·")[0],""), code=c, title=t, desc=p,
                                 n="11", status="done")) for h, c, t, p, m in home["feats"])
    tracklists = ""
    for t in tracks:
        rows = "".join(f'<a class="trow" href="{rewire(h)}"><span class="tcode">{c}</span><span>{n}</span><span class="arr">&rarr;</span></a>'
                       for h, c, n in t["rows"])
        tracklists += f"""<div class="card tracklist"><div class="cap"><p class="eyebrow">{t['cap']}</p><h3>{t['title']}</h3><p>{t['small']}</p></div>{rows}</div>"""
    notes = "".join(f'<div class="card note"><p class="eyebrow">{cap}</p><h3>{h3}</h3><p>{p}</p></div>'
                    for cap, h3, p in home["notes"])
    stats = " <span class=\"sep\">|</span> ".join(f"<b>{v}</b> {lbl}" for v, lbl in home["stats"])
    page = head("c", "Nexus Institute of Technology — Draft C · Atlas", "Design draft C — learning-console preview.") + c_appbar("index.html") + f"""
<main class="wrap">
<section class="hero"><div class="grid">
<div><p class="eyebrow">{home['eyebrow']}</p>
<h1>Learn Mechanical Engineering from scratch to Industry&nbsp;4.0.</h1>
<p class="sub">{home['sub']}</p>
<div class="cta-row"><a class="btn" href="curriculum.html">Explore the curriculum &rarr;</a>
<a class="btn btn-ghost" href="course.html">Sample a course</a></div>
<div class="statline">{stats}</div>
<div class="statline"><span class="chip-status prog" style="text-transform:none;letter-spacing:0;font-family:var(--sans);font-size:11.5px">Open prototype — your feedback shapes the final releases</span></div></div>
<div class="card console"><div class="rowhead"><b>Your program</b><span>Learner console</span></div>
{console_rows}
<div class="cfoot"><span><b style="color:var(--accent-ink)">{tr_n} of {tr_total}</b> lessons at full depth · recomputed every build</span><a href="curriculum.html">Open &rarr;</a></div></div>
</div></section>
<section class="sect"><div class="sect-head"><h2>A cross-section of the program</h2>
<span class="aux"><a href="curriculum.html">All 48 courses &rarr;</a></span></div>
<div class="cardgrid">{feats}</div></section>
<section class="sect"><div class="sect-head"><h2>Two tracks, one pathway</h2></div>
<div class="twocol">{tracklists}</div></section>
<section class="sect"><div class="sect-head"><h2>Built like a program, not a playlist</h2></div>
<div class="notegrid">{notes}</div></section>
<section class="sect"><div class="cta-band"><div><h2>Start with Lesson 01.</h2>
<p>No sign-up gate between you and the first derivation.</p></div>
<a class="btn" href="curriculum.html">Explore the curriculum &rarr;</a></div></section>
</main>""" + c_foot() + tail()
    return page

def build_c_curriculum():
    groups = ""
    for sem, name in SEM_NAMES.items():
        semcards = [c for c in cards if c["sem"] == sem]
        done = sum(1 for c in semcards if c["status"] == "done")
        groups += f"""<section class="semgroup" data-semgroup><div class="semgroup-head"><h3>{name}</h3>
<div class="rule"></div><span class="count">{done}/{len(semcards)} complete</span></div>
<div class="cardgrid">{''.join(c_ccard(c) for c in semcards)}</div></section>"""
    chips = '<button type="button" class="chip on" data-sem="all">All</button>' + "".join(
        f'<button type="button" class="chip" data-sem="{s}">Y{s[1]}·S{s[3]}</button>' for s in SEM_NAMES)
    page = head("c", "Curriculum — Draft C · Atlas", "Design draft C curriculum preview.") + c_appbar("curriculum.html") + f"""
<main class="wrap">
<div class="pagehead"><p class="eyebrow">Curriculum · 4 years · 8 semesters</p>
<h1>48 courses. 528 lessons. One pathway.</h1>
<p class="sub">The complete B.S.-shaped map — from foundational mathematics and physics to Industry 4.0.
Prerequisites in order, six classes a semester, eleven lessons a class — sequenced the way engineering
schools actually teach, built as authored content, never as padding.</p>
<div class="card tracker-strip"><span><b>{tr_n} / {tr_total}</b> at full depth</span>
<span class="bar"><i style="width:{tr_pct}%"></i></span><span>{tr_pct}% · recomputed every build</span></div></div>
<div class="toolbar"><div class="searchbox"><svg viewBox="0 0 20 20" fill="none" stroke-width="1.8"><circle cx="9" cy="9" r="6"/><path d="m14 14 4 4"/></svg>
<input type="search" id="lessonSearch" placeholder="Search all 528 lessons — title, course, keywords&hellip;" aria-label="Search lessons"><span class="kbd">&#8984;K</span></div>
<div class="chips" id="semChips">{chips}</div></div>
{groups}
</main>""" + c_foot() + tail()
    return page

def build_c_course():
    glyph = next((c["svg"] for c in cards if "electronics-sensors" in c["href"]), "")
    learn = f'<div class="card learn"><h3>What you\'ll learn</h3><div class="body">{re.sub(r"<h3>.*?</h3>", "", course["learn"], flags=re.S)}</div></div>'
    syls = ""
    for s in course_syls:
        done = ' done' if int(s["no"]) <= 7 else ""
        det = f'<details>{s["det"]}</details>' if s["det"] else ""
        syls += f"""<div class="syl{done}"><span class="tick">&#10003;</span><span class="no">{s['no']}</span>
<div class="body"><h4><a href="{rewire(s['href'])}">{s['title']}</a><span class="badge">Full lesson</span></h4>
<p class="scope">{s['scope']}</p><p class="src">{s['src']}</p>{det}</div></div>"""
    chips = "".join(f'<span class="chip-status done">{c}</span>' for c in course["chips"])
    facts = (f'<div class="frow"><span>Course code</span><b>ELX 205</b></div>'
             f'<div class="frow"><span>Placement</span><b>Year 2 · Semester 1</b></div>'
             f'<div class="frow"><span>Lessons</span><b>11 · all full depth</b></div>'
             f'<div class="frow"><span>Assessment</span><b>11 interactive quizzes</b></div>'
             f'<div class="frow"><span>Core-60 lessons</span><b>1</b></div>')
    page = head("c", "Electronics & Sensors — Draft C · Atlas", "Design draft C course preview.", MATHJAX) + c_appbar("course.html") + f"""
<div class="course-shell"><main>
<nav class="crumbs"><a href="curriculum.html">Curriculum</a> / <a href="curriculum.html">Year 2 · Semester 1</a> / ELX 205</nav>
<div class="course-head"><div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
<span class="glyph" style="width:44px;height:44px;border-radius:11px;background:var(--tint);border:1px solid var(--tint-line);display:flex;align-items:center;justify-content:center">{glyph}</span>
<span class="eyebrow" style="margin:0">{course['eyebrow']}</span></div>
<h1>{course['title']}</h1><p class="sub">{course['sub']}</p>
<div class="chiprow">{chips}</div>
<div class="cta-row"><a class="btn" href="lesson.html">Start lesson 01 &rarr;</a>
<a class="btn btn-ghost" href="#" title="Outside this preview">Course summary (PDF)</a></div></div>
{learn}
<div class="card syllabus"><div class="card-cap"><b>Syllabus — 11 lessons</b><span class="chip-status done">7 of 11 done · preview state</span></div>{syls}</div>
</main>
<aside class="rail">
<div class="card facts"><h3>Course facts</h3>{facts}</div>
{relink(course['career'])}
<div class="card nextcourse"><span class="lbl">Next course</span><a href="#">{course['next']} &rarr;</a></div>
</aside></div>""" + c_foot() + tail()
    return page

def build_c_lesson():
    outline = "".join(
        f'<a href="{rewire(h)}" class="ol{cur}"{"" if not cur else ""}{" data-demo-done" if int(label.split(" ·")[0])<=7 else ""}><span class="tick">&#10003;</span><span>{label}</span></a>'
        for h, cur, label in lesson["outline"])
    meta = "".join(f'<span class="mchip">{k.strip()} <b>{v}</b></span>' for k, v in lesson["meta"])
    video = ('<span class="video-status"><span class="dot"></span>Lecture video — in production</span>'
             if lesson["video_todo"] else "")
    panels = "".join(f'<section class="tabpanel{" on" if pid=="t-lecture" else ""}" id="{pid}">{inner}</section>'
                     for pid, inner in lesson["panels"].items())
    page = head("c", f"{lesson['title']} — Draft C · Atlas", "Design draft C lesson preview.", MATHJAX) + c_appbar("lesson.html") + f"""
<div class="player">
<aside class="outline card" aria-label="Course outline"><div class="oh"><a href="course.html">ELX 205 · Electronics &amp; Sensors</a>
<div class="bar"><i style="width:64%"></i></div><span class="ptext">7 of 11 complete — preview state</span></div>{outline}</aside>
<main class="lesson-main">
<nav class="crumbs"><a href="curriculum.html">Curriculum</a> / <a href="course.html">ELX 205</a> / Lesson 08 of 11</nav>
<div class="lesson-head"><p class="eyebrow">{lesson['eyebrow']}</p>
<h1>{lesson['title']}</h1><p class="sub">{lesson['sub']}</p>
<div class="metachips">{meta}</div>
<div class="lesson-tools"><button class="complete-btn" type="button">&#10003;&nbsp; Mark as complete</button>{video}</div>
<p class="src-strip"><span class="t">Sourced from</span>{lesson['source']}</p></div>
<div class="tabs" role="tablist"><button class="on" data-tab="t-lecture">Lecture</button>
<button data-tab="t-foundations">Foundations</button><button data-tab="t-examples">Examples &amp; Quiz</button>
<button data-tab="t-library">Library</button></div>
{panels}
<nav class="prevnext"><a href="#">&larr; 07 · Pressure and level measurement</a><a href="course.html">All lessons · ELX 205</a><a href="#">09 · Analog-to-digital &rarr;</a></nav>
<nav class="coursenav"><span class="cn-label">Next course</span><a class="cn-link" href="#">{course['next']} &rarr;</a></nav>
</main></div>""" + c_foot() + tail()
    return page

# ---------------------------------------------------------------- emit
def main():
    shutil.copyfile(ROOT / "nexus" / "logo.svg", OUT / "shared" / "logo.svg")
    outputs = {
        "draft-a-foundry/index.html":      build_a_home(),
        "draft-a-foundry/curriculum.html": build_a_curriculum(),
        "draft-a-foundry/course.html":     build_a_course(),
        "draft-a-foundry/lesson.html":     build_a_lesson(),
        "draft-b-press/index.html":        build_b_home(),
        "draft-b-press/curriculum.html":   build_b_curriculum(),
        "draft-b-press/course.html":       build_b_course(),
        "draft-b-press/lesson.html":       build_b_lesson(),
        "draft-c-atlas/index.html":        build_c_home(),
        "draft-c-atlas/curriculum.html":   build_c_curriculum(),
        "draft-c-atlas/course.html":       build_c_course(),
        "draft-c-atlas/lesson.html":       build_c_lesson(),
    }
    for rel, content in outputs.items():
        p = OUT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"wrote {rel:38s} {len(content):>8,} bytes")
    print(f"\nextracted: {len(cards)} course cards · {len(course_syls)} syllabus rows · "
          f"{len(lesson['panels'])} lesson tab panels · tracker {tr_n}/{tr_total} ({tr_pct}%)")

if __name__ == "__main__":
    main()
