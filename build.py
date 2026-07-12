#!/usr/bin/env python3
"""Sun Devil Factory — static site generator.

Zero dependencies. Reads data/*.json + content fragments, emits docs/.
GitHub Pages serves docs/ on main. Run:  python3 build.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
DATA = ROOT / "data"
CONTENT = ROOT / "content"
SEMESTERS = ["y1s1", "y1s2", "y2s1", "y2s2", "y3s1", "y3s2", "y4s1", "y4s2"]

CORE60_BLOCKS = {
    "A": "Processes", "B": "Fundamentals", "C": "Reliability",
    "D": "Condition Monitoring", "E": "Rotating Equipment",
    "F": "Planning", "G": "Automation",
}

FORK = (
    '<svg class="fork" viewBox="1.8 0 18.4 30" aria-hidden="true" focusable="false">'
    '<path d="M11,0 L13.1,3.2 L13.1,13 L8.9,13 L8.9,3.2 Z"/>'
    '<path d="M3,1.4 C1.8,4.6 2.1,8.6 3.9,11.5 C4.6,12.5 5.5,13 6.5,13 L8.6,13 '
    'C6.8,11.4 5.7,8.9 5.4,5.9 C5.3,4.3 5.1,2.7 3,1.4 Z"/>'
    '<path d="M19,1.4 C20.2,4.6 19.9,8.6 18.1,11.5 C17.4,12.5 16.5,13 15.5,13 L13.4,13 '
    'C15.2,11.4 16.3,8.9 16.6,5.9 C16.7,4.3 16.9,2.7 19,1.4 Z"/>'
    '<rect x="3.2" y="13" width="15.6" height="2.6"/>'
    '<rect x="8.5" y="15.6" width="5" height="1.9"/>'
    '<rect x="9.6" y="15.6" width="2.8" height="14.4"/>'
    '</svg>'
)

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{prefix}assets/css/site.css">
</head>
<body>
<header class="hd">
  <a class="wordmark" href="{prefix}index.html">Sun {fork} Devil <span>Factory</span></a>
  <nav aria-label="Site">
    <a href="{prefix}index.html"{on_home}>Start Here</a>
    <a href="{prefix}curriculum/index.html"{on_curr}>Curriculum</a>
    <a href="{prefix}career/index.html"{on_career}>Career</a>
  </nav>
</header>
<main>
{body}
</main>
<footer>
  <div class="inner">
    {footer_next}
    <div class="cols">
      <div>
        <h5>The pathway</h5>
        A maintenance engineer's route into manufacturing:<br>
        Reliability · Asset Integrity · Production/Operations · Maintenance Planning
      </div>
      <div>
        <h5>Site</h5>
        <a href="{prefix}index.html">Start here</a><br>
        <a href="{prefix}curriculum/index.html">Curriculum — 48 courses</a><br>
        <a href="{prefix}career/index.html">Career strategy</a>
      </div>
      <div>
        <h5>Kuwait industry context</h5>
        Kuwait Steel · Gulf Cable · Kirby Building Systems · EQUATE · KDD / Petra · HEISCO
      </div>
    </div>
    <div class="mark"><span class="mn">Sun</span> {fork} <span class="mn">Devil</span> Factory</div>
    <p class="fine">Educational material. Worked-example values are pedagogical; representative
    industrial figures are labeled as such and are not published operating data of any named
    company. Photography is openly licensed; credits on each image and in the repository.</p>
  </div>
</footer>
<script src="{prefix}assets/js/site.js"></script>
</body>
</html>
"""


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def load_sources():
    """Registry of verified source URLs; returns [(escaped_match, entry)]
    sorted longest-match-first so specific names win over generic ones."""
    reg = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    entries = []
    for s in reg["sources"]:
        for m in s["match"]:
            entries.append((esc(m), s))
    entries.sort(key=lambda e: -len(e[0]))
    return entries


SOURCES = None  # set in main()


def linkify(escaped_text):
    """Replace known source names (already-escaped text) with links to the
    verified registry URL, plus optional Watch-lectures / label / Arabic
    companions. Placeholder pass prevents nested anchors."""
    subs = []
    for m, s in SOURCES:
        if m in escaped_text:
            token = f"\x00{len(subs)}\x00"
            escaped_text = escaped_text.replace(m, token, 1)
            html = (f'<a href="{s["url"]}" title="{esc(s["name"])}" '
                    f'target="_blank" rel="noopener">{m}</a>')
            if s.get("watch"):
                html += (f' <a class="watch" href="{s["watch"]}" '
                         f'target="_blank" rel="noopener">Watch lectures ▶</a>')
            if s.get("arabic"):
                ar = s["arabic"]
                ar_url = ar["url"] if isinstance(ar, dict) else ar
                html += (f' <a class="watch ar" href="{ar_url}" '
                         f'target="_blank" rel="noopener">In Arabic — alternative</a>')
                if isinstance(ar, dict) and ar.get("note"):
                    html += f' <span class="srcnote">{esc(ar["note"])}</span>'
            if s.get("label"):
                html += f' <span class="srcnote">{esc(s["label"])}</span>'
            subs.append((token, html))
    for token, anchor in subs:
        escaped_text = escaped_text.replace(token, anchor)
    return escaped_text


def page(path, title, desc, body, prefix, active="", footer_next=""):
    html = PAGE.format(
        title=esc(title), desc=esc(desc), prefix=prefix, body=body,
        footer_next=footer_next, fork=FORK,
        on_home=' class="on"' if active == "home" else "",
        on_curr=' class="on"' if active == "curriculum" else "",
        on_career=' class="on"' if active == "career" else "",
    )
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def fragment(name):
    f = CONTENT / name
    return f.read_text(encoding="utf-8") if f.exists() else None


def load_curriculum():
    sems = []
    for sid in SEMESTERS:
        sems.append(json.loads((DATA / f"{sid}.json").read_text(encoding="utf-8")))
    return sems


def tier_badge(lesson):
    t = lesson.get("tier", 3)
    has = bool(lesson.get("content"))
    if t == 1 and has:
        return '<span class="badge t1">Full lecture</span>'
    if t == 2 and has:
        return '<span class="badge t2">Study guide</span>'
    if t in (1, 2):
        return '<span class="badge queued">Core 60 · guide queued</span>'
    return ""


def lesson_page_name(course, lesson):
    return f"{lesson['n']:02d}-{slugify(lesson['t'])[:60]}.html"


def build_course_page(sem, course, prefix):
    rows = []
    for les in course["lessons"]:
        title = esc(les["t"])
        badge = tier_badge(les)
        if les.get("content"):
            href = lesson_page_name(course, les)
            title_html = f'<a href="{href}">{title}</a>'
        else:
            title_html = title
        core = les.get("core60")
        core_note = f' <b>CORE 60 · {esc(core)}</b> ·' if core else ""
        src = linkify(esc(les.get("src", "")))
        scope = esc(les.get("scope", ""))
        preview = ""
        if les.get("preview"):
            qs = "".join(f"<li>{esc(q)}</li>" for q in les["preview"])
            preview = (f'<div class="preview"><b>After this lesson you can '
                       f'answer:</b><ul>{qs}</ul></div>')
        rows.append(f"""
<div class="lesson-row rv">
  <div class="no">{les['n']:02d}</div>
  <div>
    <h4>{title_html}{badge}</h4>
    <p class="scope">{scope}</p>
    {preview}
    <p class="src"><b>Taught from</b> —{core_note} {src}</p>
  </div>
</div>""")

    taught = "".join(f"<li>{linkify(esc(t))}</li>"
                     for t in course.get("taught_from", []))
    vids = ""
    if course.get("videos"):
        cards = "".join(f"""
<a class="vid" href="{esc(v['url'])}" target="_blank" rel="noopener">
  <span class="vtag">{esc(v.get('tag', 'COURSE VIDEO — VERIFIED'))}</span>
  <h4>{esc(v['title'])}</h4>
  <p>{esc(v.get('note', ''))}</p>
  <span class="src">{esc(v['src'])}</span>
</a>""" for v in course["videos"])
        vids = f"""
<h3>Open courseware for this course</h3>
<div class="vids">{cards}</div>"""

    n_core = sum(1 for l in course["lessons"] if l.get("core60"))
    body = f"""
<div class="pagehead">
  <p class="kicker"><span class="n">{esc(course['code'])}</span>{esc(sem['title'])}</p>
  <h1>{esc(course['title'])}</h1>
  <p class="sub">{esc(course['summary'])}</p>
</div>
<section class="part tight">
  <div class="wide">
    <p class="small">{len(course['lessons'])} lessons · {n_core} in the Core&nbsp;60 ·
    Primary texts: </p>
    <ul class="plain small">{taught}</ul>
    <div class="lessons">{''.join(rows)}</div>
    {vids}
  </div>
</section>"""
    page(
        f"curriculum/{sem['id']}/{course['id']}/index.html",
        f"{course['title']} — Sun Devil Factory",
        course["summary"][:150], body, prefix, "curriculum",
    )


def build_lesson_pages(sem, course, prefix):
    for les in course["lessons"]:
        frag_id = les.get("content")
        if not frag_id:
            continue
        frag = fragment(f"lessons/{frag_id}.html")
        if frag is None:
            raise SystemExit(f"missing content fragment: {frag_id}")
        frag = frag.replace("{{prefix}}", prefix)
        name = lesson_page_name(course, les)
        nxt = ""
        page(
            f"curriculum/{sem['id']}/{course['id']}/{name}",
            f"{les['t']} — {course['title']} — Sun Devil Factory",
            les.get("scope", "")[:150], frag, prefix, "curriculum", nxt,
        )


def build_curriculum_index(sems, prefix):
    parts = []
    total_lessons = 0
    total_core = 0
    for i, sem in enumerate(sems, 1):
        cards = []
        for c in sem["courses"]:
            n_core = sum(1 for l in c["lessons"] if l.get("core60"))
            total_core += n_core
            total_lessons += len(c["lessons"])
            core_txt = f"<b>{n_core} core</b> · " if n_core else ""
            cards.append(f"""
<a class="course-card" href="{sem['id']}/{c['id']}/index.html">
  <span class="code">{esc(c['code'])}</span>
  <h4>{esc(c['title'])}</h4>
  <p>{esc(c['summary'][:130])}…</p>
  <span class="meta">{core_txt}{len(c['lessons'])} lessons</span>
</a>""")
        parts.append(f"""
<div class="sem rv">
  <div class="sem-head"><span class="n">{i:02d}</span><h3>{esc(sem['title'])}</h3></div>
  <div class="course-grid">{''.join(cards)}</div>
</div>""")

    body = f"""
<div class="pagehead">
  <p class="kicker"><span class="n">CURRICULUM</span>4 years · 8 semesters</p>
  <h1>48 courses. {total_lessons} lessons. One pathway.</h1>
  <p class="sub">The full degree-shaped map, rebuilt for a maintenance engineer entering
  manufacturing. {total_core} lessons form the Core 60+ spine — the ones interviews and
  plant floors actually test — and are built to study-guide or full-lecture depth.
  Everything else carries a scope note and its textbook source, so you always know
  what a topic is and where it is taught from.</p>
</div>
<section class="part tight"><div class="wide">{''.join(parts)}</div></section>"""
    page("curriculum/index.html", "Curriculum — Sun Devil Factory",
         "48 courses and 522 lessons mapped for a maintenance-to-manufacturing transition.",
         body, prefix, "curriculum")


def build_static_pages(sems, prefix_root):
    home = fragment("pages/home.html")
    career = fragment("pages/career.html")
    if home:
        page("index.html", "Sun Devil Factory — a maintenance engineer's route into manufacturing",
             "Free, textbook-sourced curriculum and career strategy for mechanical maintenance "
             "engineers moving into manufacturing roles in Kuwait.",
             home.replace("{{prefix}}", ""), "", "home")
    if career:
        page("career/index.html", "Career strategy — Sun Devil Factory",
             "Tactical maintenance-to-manufacturing career plan: CV translation, Kuwait "
             "employers, certifications, interview prep, 12-month plan.",
             career.replace("{{prefix}}", "../"), "../", "career")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / ".nojekyll").write_text("")
    shutil.copytree(ROOT / "assets", OUT / "assets")

    global SOURCES
    SOURCES = load_sources()
    sems = load_curriculum()
    n_prev = sum(1 for s in sems for c in s["courses"] for l in c["lessons"]
                 if l.get("preview"))
    print(f"preview questions: {n_prev}/522 lessons")

    # sanity: counts
    n_courses = sum(len(s["courses"]) for s in sems)
    n_lessons = sum(len(c["lessons"]) for s in sems for c in s["courses"])
    n_core = sum(1 for s in sems for c in s["courses"] for l in c["lessons"]
                 if l.get("core60"))
    print(f"courses={n_courses} lessons={n_lessons} core60={n_core}")

    build_curriculum_index(sems, "../")
    for sem in sems:
        for course in sem["courses"]:
            build_course_page(sem, course, "../../../")
            build_lesson_pages(sem, course, "../../../")
    build_static_pages(sems, "")
    n_pages = len(list(OUT.rglob("*.html")))
    print(f"wrote {n_pages} pages -> {OUT}")


if __name__ == "__main__":
    main()
