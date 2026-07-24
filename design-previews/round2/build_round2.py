#!/usr/bin/env python3
"""
Round 2 — five FULL bright design drafts (owner order 2026-07-24: never dark,
3-5 directions, effects/video allowed). Reuses round 1's verified content
extraction (build_drafts.py import runs extraction only, never its main()).
Emits 5 drafts x 4 surfaces from the same REAL site content, plus nothing
else — content stays byte-identical, chrome carries the personality.
"""
import sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
PREV = HERE.parent
sys.path.insert(0, str(PREV))
import build_drafts as R1  # noqa: E402  (extraction happens at import)

lesson, course, course_syls = R1.lesson, R1.course, R1.course_syls
cards, home, tracks = R1.cards, R1.home, R1.tracks
tr_n, tr_total, tr_pct = R1.tr_n, R1.tr_total, R1.tr_pct
SEM_NAMES, ROMAN = R1.SEM_NAMES, R1.ROMAN
rewire, relink, MATHJAX, FOOT_TEXT = R1.rewire, R1.relink, R1.MATHJAX, R1.FOOT_TEXT
GLYPHS = {c["code"].split(" ·")[0]: c["svg"] for c in cards}

F = {
 "aurora":   "https://fonts.googleapis.com/css2?family=Geist:wght@400..750&family=Geist+Mono:wght@400..600&display=swap",
 "meridian": "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&family=IBM+Plex+Mono:wght@400;500&display=swap",
 "beacon":   "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Inter:wght@400..800&family=JetBrains+Mono:wght@400..600&display=swap",
 "blueprint":"https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,400..800;1,62..125,400..800&family=IBM+Plex+Mono:wght@400;500;600&display=swap",
 "skyline":  "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=Inter:wght@400..800&family=Space+Mono&display=swap",
}
THEMES = [
 dict(key="aurora",    folder="a-aurora",    name="Aurora",    tag="The bright learning console"),
 dict(key="meridian",  folder="b-meridian",  name="Meridian",  tag="The bright press — editorial daylight"),
 dict(key="beacon",    folder="c-beacon",    name="Beacon",    tag="Encouragement as a design system"),
 dict(key="blueprint", folder="d-blueprint", name="Blueprint Day", tag="The drawing office at noon"),
 dict(key="skyline",   folder="e-skyline",   name="Skyline",   tag="The open-sky, video-led showcase"),
]
NAV = [("index.html","Home"),("curriculum.html","Curriculum"),("course.html","ELX 205"),("lesson.html","Lesson 08")]

def head(t, title, extra=""):
    return f"""<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Draft {t['name']}</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="../../shared/logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{F[t['key']]}">
<link rel="stylesheet" href="draft.css">
{extra}
</head>
<body>"""

def appbar(t, current):
    links = "".join(f'<a href="{h}"{" class=\"on\"" if h==current else ""}>{l}</a>' for h, l in NAV)
    dead = "".join(f'<a href="#" title="Outside this preview">{x}</a>' for x in ("Reference","Career Paths","Feedback"))
    return f"""
<header class="appbar"><div class="in">
  <a class="brand" href="index.html"><img src="../../shared/logo.svg" alt="">
    <span class="txt"><em>Nexus</em> Institute of Technology</span></a>
  <nav>{links}{dead}</nav>
</div></header>"""

def foot(t):
    return f"""
<footer class="foot"><div class="in">
  <div class="mark"><em>Nexus</em> Institute of Technology</div>
  <nav><a href="index.html">Home</a><a href="curriculum.html">Curriculum</a>
  <a href="course.html">ELX 205</a><a href="lesson.html">Lesson 08</a></nav>
  <p>Preliminary open release — a prototype published so learners can try it and reflect;
  feedback shapes the final, tailored releases. {FOOT_TEXT.split('releases. ',1)[-1]}</p>
</div></footer>
<a class="hubchip" href="../index.html#rate-{t['key']}">&larr; Rate this draft</a>
<script src="../../shared/drafts.js"></script>
<script src="../fx.js"></script>
</body>
</html>"""

# ---------------------------------------------------------------- heroes ---
def hero_aurora(t):
    rows = ""
    for code, label, pct in [("ELX 205","Electronics & Sensors — L08 · Vibration and speed sensors",64),
                             ("MTH 207","Engineering Mathematics III — complete",100),
                             ("FLD 203","Fluid Mechanics — complete",100)]:
        rows += f"""<div class="citem"><span class="glyph">{GLYPHS.get(code,'')}</span>
<span class="cmeta"><b>{label}</b><span>{code}</span></span>
<span class="cbar"><span class="bar"><i style="width:{pct}%"></i></span><span>{pct}%</span></span></div>"""
    return f"""<section class="hero"><div class="wrap"><div class="grid">
<div><p class="eyebrow">{home['eyebrow']}</p>
<h1>Learn Mechanical Engineering from scratch to <span class="hl">Industry&nbsp;4.0</span>.</h1>
<p class="sub">{home['sub']}</p>
<div class="cta-row"><a class="btn" href="curriculum.html">Explore the curriculum &rarr;</a>
<a class="btn btn-ghost" href="course.html">Sample a course</a></div>
<div class="statline"><span><b>4</b> years</span><span><b>48</b> courses</span><span><b>528</b> lessons</span><span><b>{tr_n}</b> at full depth · {tr_pct}%</span></div></div>
<div class="card console" data-reveal="reveal-right"><div class="rowhead"><b>Your program</b><span>Learner console</span></div>
{rows}<div class="cfoot"><span><b style="color:var(--accent-ink)">{tr_n} of {tr_total}</b> at full depth · recomputed every build</span><a href="curriculum.html">Open &rarr;</a></div></div>
</div></div></section>"""

MERIDIAN_PLATE = """<figure class="hero-plate draw-on"><svg viewBox="0 0 560 240" xmlns="http://www.w3.org/2000/svg" fill="none" stroke-width="1.5">
<circle cx="150" cy="120" r="76"/><circle cx="150" cy="120" r="58" stroke-dasharray="4 6"/><circle cx="150" cy="120" r="15"/>
<circle cx="284" cy="120" r="50"/><circle cx="284" cy="120" r="36" stroke-dasharray="4 6"/><circle cx="284" cy="120" r="11"/>
<circle cx="382" cy="120" r="38"/><circle cx="382" cy="120" r="26" stroke-dasharray="4 6"/><circle cx="382" cy="120" r="8" class="amb"/>
<line x1="58" y1="120" x2="470" y2="120" stroke-dasharray="9 7" stroke-width="1"/>
<line x1="150" y1="34" x2="150" y2="206" stroke-dasharray="9 7" stroke-width="1"/>
<polyline points="440,60 500,60 492,55 500,60 492,65" stroke-width="1"/>
</svg><figcaption><b>Plate I.</b> Power transmission by meshing gear train — every visual on the
platform is an original vector illustration, and this one draws itself as you arrive.</figcaption></figure>"""

def hero_meridian(t):
    return f"""<section class="hero"><div class="wrap"><div class="grid">
<div><p class="eyebrow">Vol. II — The Bright Edition</p>
<h1>Learn Mechanical Engineering <span class="it">from scratch</span> to Industry&nbsp;4.0.</h1>
<p class="sub">{home['sub']}</p>
<div class="statline"><span><b>{home['chips']}</b></span><span>·</span><span><b>{tr_n} of {tr_total}</b> at full depth ({tr_pct}%)</span><span>·</span><span>every number machine-verified</span></div>
<div class="cta-row"><a class="btn" href="curriculum.html">Open the catalogue</a>
<a class="btn btn-ghost" href="course.html">Sample a course</a></div></div>
<div>{MERIDIAN_PLATE}</div>
</div></div></section>"""

def hero_beacon(t):
    cheers = "".join(f'<span class="cheer"><span class="ic">{ic}</span>{txt}</span>' for ic, txt in [
        ("✓","Start from absolute zero"), ("✓","Every number machine-verified"), ("✓","Honest depth labels"), ("✓","No accounts needed")])
    bots = '<div class="bot bot-wrench"></div><div class="bot bot-gear"></div><div class="bot bot-caliper"></div><div class="bot bot-oil"></div>'
    return f"""<section class="hero">{bots}<div class="wrap"><div class="in">
<p class="eyebrow">{home['eyebrow']}</p>
<h1>Learning this is <span class="hl">bright work</span> — from scratch to Industry&nbsp;4.0.</h1>
<p class="sub">{home['sub']}</p>
<div class="cta-row"><a class="btn" href="curriculum.html">Start learning &rarr;</a>
<a class="btn btn-ghost" href="course.html">Peek at a course</a></div>
<div class="statline"><span><b>4</b> years</span><span><b>48</b> courses</span><span><b>528</b> lessons</span><span><b>{tr_n}</b> at full depth</span></div>
<div class="cheer-row">{cheers}</div>
</div></div></section>"""

BLUEPRINT_FIG = """<div class="hero-fig"><svg class="draw-on" viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#1D63B8" stroke-width="1.6">
<circle cx="180" cy="150" r="92"/><circle cx="180" cy="150" r="70" stroke-dasharray="5 7"/><circle cx="180" cy="150" r="20"/>
<circle cx="340" cy="150" r="58"/><circle cx="340" cy="150" r="42" stroke-dasharray="5 7"/><circle cx="340" cy="150" r="13" stroke="#C77F0A"/>
<line x1="60" y1="150" x2="460" y2="150" stroke-dasharray="10 8" stroke-width="1"/>
<line x1="180" y1="40" x2="180" y2="260" stroke-dasharray="10 8" stroke-width="1"/>
<polyline points="180,262 180,282 340,282 340,262" stroke-width="1"/>
<polyline points="186,276 180,282 186,288" stroke-width="1"/><polyline points="334,276 340,282 334,288" stroke-width="1"/>
<line x1="186" y1="282" x2="334" y2="282" stroke-width="1"/>
</svg><div class="figcap"><span>FIG 01 — GEAR TRAIN, SINGLE REDUCTION</span><span>SCALE 1:1</span></div></div>"""

def hero_blueprint(t):
    return f"""<section class="hero"><div class="wrap"><div class="sheet">
<div class="sheet-head"><span><b>NEXUS</b> · SHEET NX-0528</span><span>PRELIMINARY RELEASE · OPEN REVIEW</span><span>SCALE 1:1 · REV D</span></div>
<div class="sheet-body">
<div><p class="eyebrow">{home['eyebrow']}</p>
<h1>Learn Mechanical Engineering <span class="hl">from scratch to Industry&nbsp;4.0.</span></h1>
<p class="sub">{home['sub']}</p>
<div class="statline"><span><b>4</b> YEARS</span><span><b>48</b> COURSES</span><span><b>528</b> LESSONS</span><span><b>{tr_n}/{tr_total}</b> FULL DEPTH · {tr_pct}%</span></div>
<div class="cta-row"><a class="btn" href="curriculum.html">Open the curriculum &rarr;</a>
<a class="btn btn-ghost" href="course.html">Inspect a course</a></div></div>
{BLUEPRINT_FIG}
</div></div></div></section>"""

def hero_skyline(t):
    return f"""<section class="hero"><div class="wrap">
<p class="eyebrow">{home['eyebrow']}</p>
<h1>Learn Mechanical Engineering <span class="hl">from scratch to Industry&nbsp;4.0</span>.</h1>
<p class="sub">{home['sub']}</p>
<div class="cta-row"><a class="btn" href="curriculum.html">Explore the curriculum &rarr;</a>
<a class="btn btn-ghost" href="course.html">Sample a course</a></div>
<div class="statline"><span><b>4</b> years</span><span><b>48</b> courses</span><span><b>528</b> lessons</span><span><b>{tr_n} of {tr_total}</b> at full depth</span></div>
<div class="hero-media" data-drift="0.04">
  <video autoplay muted loop playsinline poster="../assets/hero-bright.png" src="../assets/hero-bright.mp4" aria-hidden="true"></video>
  <div class="hm-bar">Prototype · Open build</div>
  <div class="float-chip" style="top:8%;left:4%"><span class="ic">&#8984;K</span> Search 528 lessons</div>
  <div class="float-chip" style="top:16%;right:5%"><span class="ic">✓</span> Machine-verified quizzes</div>
  <div class="float-chip" style="bottom:12%;left:7%"><span class="ic">{tr_pct}%</span> at full depth — honest</div>
</div>
</div></section>"""

HEROES = dict(aurora=hero_aurora, meridian=hero_meridian, beacon=hero_beacon,
              blueprint=hero_blueprint, skyline=hero_skyline)

# ------------------------------------------------------------- shared body -
def home_sections(t):
    feats = "".join(f"""<a class="ccard" href="{rewire(h)}"><div class="top"><span class="glyph">{GLYPHS.get(c.split(' ·')[0],'')}</span>
<span class="code">{c.split(' ·')[0]}</span><span style="margin-inline-start:auto" class="chip-status done">Complete</span></div>
<h3>{ti}</h3><p>{p}</p>
<div class="foot"><span class="bar"><i style="width:100%"></i></span><span class="n">11 lessons</span></div></a>"""
        for h, c, ti, p, m in home["feats"])
    tl = ""
    for tr in tracks:
        rows = "".join(f'<a class="trow" href="{rewire(h)}"><span class="tcode">{c}</span><span>{n}</span><span class="arr">&rarr;</span></a>'
                       for h, c, n in tr["rows"])
        tl += f"""<div class="card tracklist"><div class="cap"><p class="eyebrow">{tr['cap']}</p><h3>{tr['title']}</h3><p>{tr['small']}</p></div>{rows}</div>"""
    notes = "".join(f'<div class="card note"><p class="eyebrow">{cap}</p><h3>{h3}</h3><p>{p}</p></div>'
                    for cap, h3, p in home["notes"])
    stats = "".join(f'<div class="stat"><b data-count="{v}">{v}</b><span>{l}</span></div>'
                    if v.isdigit() else f'<div class="stat"><b>{v}</b><span>{l}</span></div>'
                    for v, l in home["stats"])
    return f"""
<main class="wrap">
<section class="sect"><div class="statgrid">{stats}</div></section>
<section class="sect"><div class="sect-head"><h2>A cross-section of the program</h2>
<span class="aux"><a href="curriculum.html">All 48 courses &rarr;</a></span></div>
<div class="cardgrid">{feats}</div></section>
<section class="sect"><div class="sect-head"><h2>Two tracks, one pathway</h2></div>
<div class="twocol">{tl}</div></section>
<section class="sect"><div class="sect-head"><h2>Built like a program, not a playlist</h2></div>
<div class="notegrid">{notes}</div></section>
<section class="sect"><div class="cta-band"><div><h2>Start with Lesson 01.</h2>
<p>Then rate this draft — round 2 is shaped by your reactions.</p></div>
<div class="cta-row" style="margin:0"><a class="btn" href="curriculum.html">Explore the curriculum &rarr;</a>
<a class="btn btn-ghost" href="../index.html#rate-{t['key']}">Rate this draft</a></div></div></section>
</main>"""

def page_home(t):
    return head(t, "Nexus Institute of Technology") + appbar(t, "index.html") + HEROES[t["key"]](t) + home_sections(t) + foot(t)

def page_curriculum(t):
    groups = ""
    for sem, name in SEM_NAMES.items():
        semcards = [c for c in cards if c["sem"] == sem]
        done = sum(1 for c in semcards if c["status"] == "done")
        cc = ""
        for c in semcards:
            pct = {"done":100,"amber":9,"queued":0}[c["status"]]
            chip = {"done":'<span class="chip-status done">Complete</span>',
                    "amber":'<span class="chip-status prog">In build</span>',
                    "queued":'<span class="chip-status dim">Queued</span>'}[c["status"]]
            cc += f"""<a class="ccard" href="{rewire(c['href'])}" data-course data-sem="{c['sem']}" data-search="{(c['code']+' '+c['title']+' '+c['desc']).lower()}">
<div class="top"><span class="glyph">{c['svg']}</span><span class="code">{c['code'].split(' ·')[0]}</span><span style="margin-inline-start:auto">{chip}</span></div>
<h4>{c['title']}</h4><p>{c['desc']}</p>
<div class="foot"><span class="bar"><i style="width:{pct}%"></i></span><span class="n">{c['n']} lessons</span></div></a>"""
        groups += f"""<section class="semgroup" data-semgroup><div class="semgroup-head"><h3>{name}</h3>
<div class="rule"></div><span class="count">{done}/{len(semcards)} complete</span></div>
<div class="course-grid">{cc}</div></section>"""
    chips = '<button type="button" class="chip on" data-sem="all">All</button>' + "".join(
        f'<button type="button" class="chip" data-sem="{s}">Y{s[1]}·S{s[3]}</button>' for s in SEM_NAMES)
    body = f"""
<main class="wrap">
<div class="pagehead"><p class="eyebrow">Curriculum · 4 years · 8 semesters</p>
<h1>48 courses. 528 lessons. One pathway.</h1>
<p class="sub">The complete B.S.-shaped map — from foundational mathematics and physics to Industry 4.0.
Prerequisites in order, six classes a semester, eleven lessons a class — built as authored content,
never as padding.</p>
<div class="tracker-strip"><span><b>{tr_n} / {tr_total}</b> at full depth</span>
<span class="bar"><i style="width:{tr_pct}%"></i></span><span>{tr_pct}% · recomputed every build</span></div></div>
<div class="toolbar"><div class="searchbox"><input type="search" id="lessonSearch"
  placeholder="Search all 528 lessons — title, course, keywords&hellip;" aria-label="Search lessons"><span class="kbd">&#8984;K</span></div>
<div class="chips" id="semChips">{chips}</div></div>
{groups}
</main>"""
    return head(t, "Curriculum") + appbar(t, "curriculum.html") + body + foot(t)

def page_course(t):
    glyph = next((c["svg"] for c in cards if "electronics-sensors" in c["href"]), "")
    learn = R1.re.sub(r"<h3>.*?</h3>", "", course["learn"], flags=R1.re.S)
    syls = ""
    for s in course_syls:
        done = " done" if int(s["no"]) <= 7 else ""
        det = f'<details>{s["det"]}</details>' if s["det"] else ""
        syls += f"""<div class="syl{done}"><span class="tick">&#10003;</span><span class="no">{s['no']}</span>
<div class="body"><h4><a href="{rewire(s['href'])}">{s['title']}</a><span class="badge">Full lesson</span></h4>
<p class="scope">{s['scope']}</p><p class="src">{s['src']}</p>{det}</div></div>"""
    chips = "".join(f'<span class="chip-status done">{c}</span>' for c in course["chips"])
    facts = ('<div class="frow"><span>Course code</span><b>ELX 205</b></div>'
             '<div class="frow"><span>Placement</span><b>Year 2 · Semester 1</b></div>'
             '<div class="frow"><span>Lessons</span><b>11 · all full depth</b></div>'
             '<div class="frow"><span>Assessment</span><b>11 interactive quizzes</b></div>'
             '<div class="frow"><span>Core-60 lessons</span><b>1</b></div>')
    body = f"""
<div class="course-shell"><main>
<nav class="crumbs"><a href="curriculum.html">Curriculum</a> / Year 2 · Semester 1 / ELX 205</nav>
<div class="course-head" style="padding-top:22px"><div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
<span class="glyph" style="width:44px;height:44px;border-radius:var(--r-sm);background:var(--tint);border:1px solid var(--tint-line);display:flex;align-items:center;justify-content:center">{glyph}</span>
<span class="eyebrow" style="margin:0">{course['eyebrow']}</span></div>
<h1>{course['title']}</h1><p class="sub" style="margin-top:14px">{course['sub']}</p>
<div class="chiprow">{chips}</div>
<div class="cta-row"><a class="btn" href="lesson.html">Start lesson 01 &rarr;</a>
<a class="btn btn-ghost" href="#" title="Outside this preview">Course summary (PDF)</a></div></div>
<div class="card learn"><h3>What you'll learn</h3><div class="body">{learn}</div></div>
<div class="card syllabus"><div class="cap"><b>Syllabus — 11 lessons</b><span class="chip-status done">7 of 11 done · preview state</span></div>{syls}</div>
</main>
<aside class="rail">
<div class="card facts"><h3>Course facts</h3>{facts}</div>
{relink(course['career'])}
<div class="card nextcourse"><span class="lbl">Next course</span><a href="#">{course['next']} &rarr;</a></div>
</aside></div>"""
    return head(t, "Electronics & Sensors", MATHJAX) + appbar(t, "course.html") + body + foot(t)

def page_lesson(t):
    outline = "".join(
        f'<a href="{rewire(h)}" class="ol{cur}"{" data-demo-done" if int(label.split(" ·")[0])<=7 else ""}><span class="tick">&#10003;</span><span>{label}</span></a>'
        for h, cur, label in lesson["outline"])
    meta = "".join(f'<span class="mchip">{k.strip()} <b>{v}</b></span>' for k, v in lesson["meta"])
    video = ('<span class="video-status"><span class="dot"></span>Lecture video — in production</span>'
             if lesson["video_todo"] else "")
    panels = "".join(f'<section class="tabpanel{" on" if pid=="t-lecture" else ""}" id="{pid}">{inner}</section>'
                     for pid, inner in lesson["panels"].items())
    body = f"""
<div class="player">
<aside class="outline card" aria-label="Course outline"><div class="oh"><a href="course.html">ELX 205 · Electronics &amp; Sensors</a>
<div class="bar"><i style="width:64%"></i></div><span class="ptext">7 of 11 complete — preview state</span></div>{outline}</aside>
<main class="lesson-main">
<nav class="crumbs" style="padding:0 0 16px"><a href="curriculum.html">Curriculum</a> / <a href="course.html">ELX 205</a> / Lesson 08 of 11</nav>
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
</main></div>"""
    return head(t, lesson["title"], MATHJAX) + appbar(t, "lesson.html") + body + foot(t)

def main():
    for t in THEMES:
        outdir = HERE / t["folder"]
        outdir.mkdir(parents=True, exist_ok=True)
        for fname, builder in (("index.html", page_home), ("curriculum.html", page_curriculum),
                               ("course.html", page_course), ("lesson.html", page_lesson)):
            html = builder(t)
            (outdir / fname).write_text(html, encoding="utf-8")
            print(f"wrote round2/{t['folder']}/{fname:16s} {len(html):>8,} bytes")

if __name__ == "__main__":
    main()
