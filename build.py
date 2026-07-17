#!/usr/bin/env python3
"""Sun Devil Factory — static site generator.

Zero dependencies. Reads data/*.json + content fragments, emits docs/.
Every lesson gets its own page with five tabs (Lecture / Foundations /
Worked Examples / Kuwait Floor / Library), populated with real content at
its current tier depth — unbuilt depth is labeled queued, never faked.
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
ASSETS = ROOT / "assets"
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
<link rel="stylesheet" href="{prefix}assets/css/site.css?v={asset_v}">
{extra_head}</head>
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
<script src="{prefix}assets/js/site.js?v={asset_v}"></script>
</body>
</html>
"""

PHOTOS = {
    "sand-pour": ("sand-pour.jpg",
        "Molten cast iron poured into a green-sand mold in a foundry",
        "Photo: Sm faysal — CC BY-SA 4.0, Wikimedia Commons"),
    "eaf-tapping": ("eaf-tapping.jpg",
        "White-hot steel tapped from a 35-ton electric furnace",
        "Photo: Alfred T. Palmer, U.S. OWI — public domain (Library of Congress)"),
    "caster-interior": ("caster-interior.jpg",
        "Ladle and tundish inside a continuous casting facility",
        "Photo: Jet Lowe, HAER — public domain (Library of Congress)"),
    "billet-cutting": ("billet-cutting.jpg",
        "Gas torch cutting a red-hot steel billet",
        "Photo: GenFM31 — CC BY-SA 4.0, Wikimedia Commons"),
    "welding": ("welding.jpg",
        "Welder striking an arc on structural steel",
        "Photo: Spc. Erica Isaacson, U.S. Army (DVIDS) — public domain, via Wikimedia Commons"),
    "machining": ("machining.jpg",
        "Turning a workpiece on an engine lathe",
        "Photo: Mostafa Meraji — CC0, via Wikimedia Commons"),
    "control-room": ("control-room.jpg",
        "Control hall of the Kelenföld power plant, Budapest",
        "Kelenföld Power Plant. Photo: AndreasS — CC BY 2.0, via Wikimedia Commons"),
    "turbine-hall": ("turbine-hall.jpg",
        "The historic turbine hall building, Johannesburg",
        "Turbine hall building, Johannesburg. Photo: Ossewa — CC BY 4.0, via Wikimedia Commons"),
}

COURSE_PHOTO = {
    "mfg-processes-1": "sand-pour", "mfg-processes-2": "machining",
    "mfg-processes-3": "machining",
    "materials-1": "billet-cutting", "materials-2": "billet-cutting",
    "corrosion": "billet-cutting",
    "welding-ndt": "welding", "safety": "welding", "hse": "welding",
    "electrical": "control-room", "electronics-sensors": "control-room",
    "plc-1": "control-room", "plc-2": "control-room",
    "controls-1": "control-room", "instrumentation": "control-room",
    "scada-iiot": "control-room", "robotics": "control-room",
    "smart-manufacturing": "control-room", "computing": "control-room",
    "statistics": "control-room", "math-1": "control-room",
    "math-2": "control-room",
    "drawing-cad": "machining", "statics": "machining",
    "strength": "machining", "machine-design-1": "machining",
    "machine-design-2": "machining", "kinematics-machinery": "machining",
    "metrology": "machining",
    "thermo-1": "eaf-tapping", "thermo-2": "eaf-tapping",
    "fluids": "eaf-tapping", "heat-transfer": "eaf-tapping",
    "hydraulics-pneumatics": "eaf-tapping", "rotating-equipment": "eaf-tapping",
    "vibrations": "eaf-tapping", "dynamics": "eaf-tapping",
    "condition-monitoring": "eaf-tapping", "reliability-1": "eaf-tapping",
    "reliability-2": "turbine-hall", "maintenance-planning": "turbine-hall",
    "asset-integrity": "caster-interior", "pressure-equipment": "caster-interior",
    "capstone": "caster-interior",
    "maintenance-fundamentals": "turbine-hall", "production-planning": "turbine-hall",
    "lean-six-sigma": "turbine-hall", "engineering-economics": "turbine-hall",
}


def hero_block(course, prefix, eyebrow, title, sub, meta):
    key = COURSE_PHOTO.get(course["id"], "eaf-tapping")
    f, alt, credit = PHOTOS[key]
    meta_html = "".join(f"<div>{m[0]}<b>{esc(m[1])}</b></div>" for m in meta)
    return f"""
<div class="hero lesson">
  <img src="{prefix}assets/img/{f}" alt="{esc(alt)}">
  <div class="hero-inner">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{esc(title)}</h1>
    <p class="sub">{esc(sub)}</p>
    <div class="hero-meta">{meta_html}</div>
  </div>
  <div class="hero-credit">{esc(credit)}</div>
</div>"""


MATHJAX = (
    "<script>MathJax={tex:{inlineMath:[['\\\\(','\\\\)']]},svg:{fontCache:'global'}};</script>\n"
    '<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>\n'
)

YT_WATCH = re.compile(r"youtube\.com/watch\?v=([\w-]{6,})")
YT_LIST = re.compile(r"youtube\.com/playlist\?list=([\w-]+)")


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def yt_embed_url(url):
    """Return an embeddable YouTube URL, or None. Only watch/playlist URLs
    embed; channels and non-YouTube pages stay links."""
    m = YT_WATCH.search(url or "")
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    m = YT_LIST.search(url or "")
    if m:
        return f"https://www.youtube.com/embed/videoseries?list={m.group(1)}"
    return None


def load_sources():
    reg = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    entries = []
    for s in reg["sources"]:
        for m in s["match"]:
            entries.append((esc(m), s))
    entries.sort(key=lambda e: -len(e[0]))
    return entries


SOURCES = None  # set in main()


def linkify(escaped_text):
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


def matched_sources(raw_text):
    """Registry entries whose match string appears in the raw text."""
    esc_t = esc(raw_text or "")
    out = []
    for m, s in SOURCES:
        if m in esc_t and s not in out:
            out.append(s)
    return out


def asset_version():
    """Short content hash of css+js so every change busts browser caches."""
    import hashlib
    h = hashlib.sha256()
    for rel in ("css/site.css", "js/site.js"):
        h.update((ASSETS / rel).read_bytes())
    return h.hexdigest()[:10]


ASSET_V = None  # set in main() after assets exist


def page(path, title, desc, body, prefix, active="", footer_next="", extra_head=""):
    html = PAGE.format(
        title=esc(title), desc=esc(desc), prefix=prefix, body=body,
        footer_next=footer_next, fork=FORK, extra_head=extra_head,
        asset_v=ASSET_V,
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


def preview_block(les):
    if not les.get("preview"):
        return ""
    qs = "".join(f"<li>{esc(q)}</li>" for q in les["preview"])
    return (f'<div class="preview"><b>After this lesson you can '
            f'answer:</b><ul>{qs}</ul></div>')


def strip_pagehead(frag):
    """Remove a fragment's own pagehead (the lesson shell provides one)."""
    return re.sub(r'\s*<div class="pagehead">.*?</div>\s*', "", frag,
                  count=1, flags=re.S)


def embed_card(url, caption, sub=""):
    e = yt_embed_url(url)
    if not e:
        return ""
    sub_html = f'<span class="src">{esc(sub)}</span>' if sub else ""
    return (f'<figure class="embed"><iframe loading="lazy" '
            f'src="{e}" title="{esc(caption)}" frameborder="0" '
            f'allow="accelerometer; encrypted-media; picture-in-picture" '
            f'allowfullscreen></iframe>'
            f'<figcaption>{esc(caption)} {sub_html}</figcaption></figure>')


def video_cards(course):
    """Course-level courseware cards: embeds where the URL is embeddable,
    link cards otherwise."""
    cards = []
    for v in course.get("videos", []):
        e = embed_card(v["url"], v["title"], v.get("src", ""))
        if e:
            cards.append(e)
        else:
            cards.append(f"""
<a class="vid" href="{esc(v['url'])}" target="_blank" rel="noopener">
  <span class="vtag">{esc(v.get('tag', 'COURSE VIDEO — VERIFIED'))}</span>
  <h4>{esc(v['title'])}</h4>
  <p>{esc(v.get('note', ''))}</p>
  <span class="src">{esc(v['src'])}</span>
</a>""")
    return cards


def sidebar_html(sems, cur_sem, cur_course, prefix):
    """8 semesters -> courses -> (current course's) lessons."""
    parts = ['<aside class="sidenav"><p class="sn-title">Curriculum</p>']
    for sem in sems:
        is_cur_sem = sem["id"] == cur_sem["id"]
        parts.append(f'<details{" open" if is_cur_sem else ""}>'
                     f'<summary>{esc(sem["title"])}</summary><ul>')
        for c in sem["courses"]:
            href = f'{prefix}curriculum/{sem["id"]}/{c["id"]}/index.html'
            if is_cur_sem and c["id"] == cur_course["id"]:
                lessons = "".join(
                    f'<li class="sn-les"><a href="{prefix}curriculum/{sem["id"]}/{c["id"]}/'
                    f'{lesson_page_name(c, l)}">{l["n"]:02d} · {esc(l["t"])}</a></li>'
                    for l in c["lessons"])
                parts.append(f'<li class="sn-cur"><a href="{href}">{esc(c["code"])} · '
                             f'{esc(c["title"])}</a><ul>{lessons}</ul></li>')
            else:
                parts.append(f'<li><a href="{href}">{esc(c["code"])} · {esc(c["title"])}</a></li>')
        parts.append("</ul></details>")
    parts.append("</aside>")
    return "".join(parts)


def load_tab_content(sem, course):
    """Optional full per-tab content: data/content/<sem>-<course>.json
    maps lesson n (as str) -> {lecture, foundations, examples, kuwait} HTML."""
    f = DATA / "content" / f"{sem['id']}-{course['id']}.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text(encoding="utf-8"))


def quiz_html(items):
    """Interactive worked-example quiz. Item kinds:
    {"type":"solve","q":html,"solution":html}            — attempt, then reveal
    {"type":"mc","q":html,"choices":[html,...],
     "answer":int,"solution":html}                        — pick, get verdict
    """
    n = len(items)
    parts = ['<div class="measure quiz">',
             '<p class="quiz-intro">Attempt each problem before checking — '
             'pick an answer or reveal the solution only after you have '
             'worked it on paper.</p>']
    for i, it in enumerate(items, 1):
        kind = it["type"]
        label = "multiple choice" if kind == "mc" else "solve, then check"
        parts.append(f'<div class="quiz-item" data-kind="{kind}">')
        parts.append(f'<div class="q"><span class="tag">Problem {i} of {n} · '
                     f'{label}</span>{it["q"]}</div>')
        if kind == "mc":
            parts.append('<div class="choices">')
            for j, ch in enumerate(it["choices"]):
                ok = ' data-ok="1"' if j == it["answer"] else ""
                key = chr(ord("A") + j)
                parts.append(f'<button type="button" class="quiz-choice"{ok}>'
                             f'<span class="key">{key}</span><span>{ch}</span>'
                             f'</button>')
            parts.append('</div><p class="quiz-verdict" hidden></p>')
        else:
            parts.append('<button type="button" class="quiz-reveal" '
                         'aria-expanded="false">Show the full solution</button>')
        parts.append(f'<div class="quiz-sol">{it["solution"]}</div></div>')
    parts.append("</div>")
    return "".join(parts)


def build_lesson_page(sems, sem, course, les, prefix, tabs=None):
    """One page per lesson, five tabs, populated from what actually exists."""
    tabs = (tabs or {}).get(str(les["n"]), {})
    n_total = len(course["lessons"])
    tier = les.get("tier", 3)
    core = les.get("core60")
    frag_id = les.get("content")
    frag = None
    if frag_id:
        frag = fragment(f"lessons/{frag_id}.html")
        if frag is None:
            raise SystemExit(f"missing content fragment: {frag_id}")
        frag = strip_pagehead(frag.replace("{{prefix}}", prefix))

    src_raw = les.get("src", "")
    src_html = linkify(esc(src_raw))
    taught = "".join(f"<li>{linkify(esc(t))}</li>"
                     for t in course.get("taught_from", []))

    # ---------- Lecture ----------
    if tabs.get("lecture"):
        lecture = preview_block(les) + f'<div class="measure">{tabs["lecture"]}</div>'
        fmt = "Full lesson"
    elif frag:
        kind = "full lecture" if tier == 1 else "study guide"
        lecture = preview_block(les) + frag
        fmt = "Full lecture · ~90 min" if tier == 1 else "Study guide · Core 60"
    else:
        depth = ("This is a Core 60 lesson — its study guide is queued and will "
                 "replace this skeleton." if core else
                 "Structured-notes tier: the scope below defines the lesson; "
                 "full teaching depth is queued behind the Core 60.")
        lecture = f"""
<div class="measure">
  {preview_block(les)}
  <p class="queued-note">{depth}</p>
</div>"""
        fmt = "Scope + sources (depth queued)"

    # ---------- Foundations ----------
    if tabs.get("foundations"):
        foundations = f'<div class="measure">{tabs["foundations"]}</div>'
    frag_note = ("<p>This lesson's foundations layer — prerequisite refreshers "
                 "and dependency map — is embedded in the lecture itself: open "
                 "the <b>Lecture</b> tab.</p>" if frag and tier == 1 else "")
    if not tabs.get("foundations"):
        foundations = f"""
<div class="measure">
  {frag_note}
  <p>This lesson belongs to <b>{esc(course['code'])} · {esc(course['title'])}</b>
  ({esc(sem['title'])}). It stands on the course's primary texts:</p>
  <ul class="plain">{taught}</ul>
  <p class="small">Course context: {esc(course['summary'])}</p>
</div>"""

    # ---------- Worked examples ----------
    if tabs.get("quiz"):
        examples = quiz_html(tabs["quiz"])
    elif tabs.get("examples"):
        examples = f'<div class="measure">{tabs["examples"]}</div>'
    elif frag and tier == 1:
        examples = ("<div class=\"measure\"><p>The worked examples for this "
                    "lesson are written into the lecture as whiteboard boards — "
                    "open the <b>Lecture</b> tab and scroll to the dark board "
                    "sections. Each carries given data, numbered steps with "
                    "units, and an engineering read-out.</p></div>")
    elif frag:
        examples = ("<div class=\"measure\"><p>This study guide carries one "
                    "condensed worked example inside the <b>Lecture</b> tab "
                    "(the boxed calculation). Full multi-example depth arrives "
                    "when this lesson is promoted to lecture tier.</p></div>")
    elif les.get("preview"):
        qs = "".join(f"<li>{esc(q)}</li>" for q in les["preview"])
        examples = f"""
<div class="measure">
  <p>Worked solutions for this lesson are queued. Until they land, use the
  lesson's own checkpoint questions as practice prompts — attempt them from
  the cited source before reading on:</p>
  <div class="preview"><b>Practice prompts — solutions not yet published:</b>
  <ul>{qs}</ul></div>
</div>"""
    else:
        examples = ("<div class=\"measure\"><p class=\"queued-note\">Worked "
                    "examples queued for this lesson.</p></div>")

    # ---------- Kuwait floor ----------
    kw = les.get("kuwait")
    if tabs.get("kuwait"):
        kuwait = f'<div class="measure">{tabs["kuwait"]}</div>'
    elif frag:
        kuwait = ("<div class=\"measure\"><p>This lesson's Kuwait-floor "
                  "application is written into the <b>Lecture</b> tab — see its "
                  "Kuwait floor section." +
                  (f" Anchor company: <b>{esc(kw)}</b>." if kw else "") +
                  "</p></div>")
    elif kw:
        kuwait = f"""
<div class="measure">
  <p>Kuwait anchor for this lesson: <b>{esc(kw)}</b>. The full floor vignette
  is written when this lesson's guide is built; until then, the
  <a href="{prefix}career/index.html">career page</a> maps what {esc(kw)}
  runs and which roles touch this topic.</p>
</div>"""
    else:
        kuwait = ("<div class=\"measure\"><p class=\"queued-note\">No Kuwait "
                  "anchor assigned to this lesson yet. The six anchor companies "
                  "and their processes are mapped on the career page.</p></div>")

    # ---------- Library ----------
    embeds = []
    seen = set()
    for s in matched_sources(src_raw):
        for key, cap in (("url", s["name"]),
                         ("watch", s["name"] + " — lecture videos"),):
            u = s.get(key)
            if u and u not in seen:
                e = embed_card(u, cap)
                if e:
                    embeds.append(e)
                    seen.add(u)
        ar = s.get("arabic")
        ar_url = ar["url"] if isinstance(ar, dict) else ar
        if ar_url and ar_url not in seen:
            e = embed_card(ar_url, "In Arabic — alternative",
                           "verified independent educator")
            if e:
                embeds.append(e)
                seen.add(ar_url)
    course_cards = video_cards(course)
    embeds_html = "".join(embeds)
    cards_html = (f'<h3>Course-level courseware</h3><div class="vids">'
                  f'{"".join(course_cards)}</div>') if course_cards else ""
    library = f"""
<div class="measure">
  <p class="src"><b>Taught from</b> — {src_html}</p>
  {embeds_html if embeds_html else
   '<p class="small">No verified embeddable video is mapped to this specific lesson yet — verified links above and course-level courseware below are the study path.</p>'}
</div>
<div class="wide">{cards_html}</div>"""

    # ---------- shell ----------
    core_chip = f'<span class="badge t2">CORE 60 · {esc(core)}</span>' if core else ""
    name = lesson_page_name(course, les)
    idx = next(i for i, l in enumerate(course["lessons"]) if l["n"] == les["n"])
    prev_l = course["lessons"][idx - 1] if idx > 0 else None
    next_l = course["lessons"][idx + 1] if idx + 1 < n_total else None
    nav = "<nav class=\"prevnext\">"
    if prev_l:
        nav += (f'<a href="{lesson_page_name(course, prev_l)}">← '
                f'{prev_l["n"]:02d} · {esc(prev_l["t"])}</a>')
    nav += f'<a href="index.html">All lessons · {esc(course["code"])}</a>'
    if next_l:
        nav += (f'<a href="{lesson_page_name(course, next_l)}">'
                f'{next_l["n"]:02d} · {esc(next_l["t"])} →</a>')
    nav += "</nav>"

    first_text = re.split(r"[—(;]", course.get("taught_from", [""])[0])[0].strip()[:44]
    n_q = len(les.get("preview", []))
    assess = (f"{len(tabs['quiz'])}-problem interactive quiz" if tabs.get("quiz") else
              "2 worked boards + hidden-answer check" if frag and tier == 1 else
              "worked examples + checkpoint questions" if tabs.get("examples") else
              f"{n_q} checkpoint questions" if n_q else "queued")
    hero = hero_block(
        course, prefix,
        f"{esc(course['code'])} · LESSON {les['n']:02d} OF {n_total} · {esc(sem['title'].upper())}",
        les["t"], les.get("scope", ""),
        [("Format", fmt), ("Primary text", first_text), ("Assessment", assess)])
    body = f"""
<nav class="crumbs"><a href="{prefix}curriculum/index.html">Curriculum</a> /
<a href="index.html">{esc(course['code'])} · {esc(course['title'])}</a> /
<span>Lesson {les['n']:02d}</span></nav>
{hero}
<div class="corechip">{core_chip}</div>
<div class="tabs" role="tablist">
  <button class="on" data-tab="t-lecture">Lecture</button>
  <button data-tab="t-foundations">Foundations</button>
  <button data-tab="t-examples">Worked Examples</button>
  <button data-tab="t-kuwait">Kuwait Floor</button>
  <button data-tab="t-library">Library</button>
</div>
<section class="tabpanel on" id="t-lecture"><h2 class="tabcap">Lecture</h2>{lecture}</section>
<section class="tabpanel" id="t-foundations"><h2 class="tabcap">Foundations</h2>{foundations}</section>
<section class="tabpanel" id="t-examples"><h2 class="tabcap">Worked Examples</h2>{examples}</section>
<section class="tabpanel" id="t-kuwait"><h2 class="tabcap">Kuwait Floor</h2>{kuwait}</section>
<section class="tabpanel" id="t-library"><h2 class="tabcap">Library</h2>{library}</section>
{nav}"""
    body = (f'<div class="withside">{sidebar_html(sems, sem, course, prefix)}'
            f'<div class="main-col">{body}</div></div>')
    page(
        f"curriculum/{sem['id']}/{course['id']}/{name}",
        f"{les['t']} — {course['title']} — Sun Devil Factory",
        les.get("scope", "")[:150], body, prefix, "curriculum",
        extra_head=MATHJAX,
    )


def build_course_page(sems, sem, course, prefix):
    rows = []
    for les in course["lessons"]:
        href = lesson_page_name(course, les)
        title_html = f'<a href="{href}">{esc(les["t"])}</a>'
        badge = tier_badge(les)
        core = les.get("core60")
        core_note = f' <b>CORE 60 · {esc(core)}</b> ·' if core else ""
        src = linkify(esc(les.get("src", "")))
        scope = esc(les.get("scope", ""))
        rows.append(f"""
<div class="lesson-row rv">
  <div class="no">{les['n']:02d}</div>
  <div>
    <h4>{title_html}{badge}</h4>
    <p class="scope">{scope}</p>
    {preview_block(les)}
    <p class="src"><b>Taught from</b> —{core_note} {src}</p>
  </div>
</div>""")

    taught = "".join(f"<li>{linkify(esc(t))}</li>"
                     for t in course.get("taught_from", []))
    cards = video_cards(course)
    vids = (f'<h3>Open courseware for this course</h3><div class="vids">'
            f'{"".join(cards)}</div>') if cards else ""

    n_core = sum(1 for l in course["lessons"] if l.get("core60"))
    hero = hero_block(
        course, prefix, f"{esc(course['code'])} · {esc(sem['title'].upper())}",
        course["title"], course["summary"],
        [("Lessons", str(len(course["lessons"]))),
         ("Core 60", str(n_core) if n_core else "—"),
         ("Track", "Maintenance → Manufacturing")])
    body = f"""
{hero}
<section class="part tight">
  <div class="wide">
    <p class="small">{len(course['lessons'])} lessons · {n_core} in the Core&nbsp;60 ·
    Primary texts: </p>
    <ul class="plain small">{taught}</ul>
    <div class="lessons">{''.join(rows)}</div>
    {vids}
  </div>
</section>"""
    body = (f'<div class="withside">{sidebar_html(sems, sem, course, prefix)}'
            f'<div class="main-col">{body}</div></div>')
    page(
        f"curriculum/{sem['id']}/{course['id']}/index.html",
        f"{course['title']} — Sun Devil Factory",
        course["summary"][:150], body, prefix, "curriculum",
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
  <div class="searchbox">
    <input type="search" id="lessonSearch" placeholder="Search all {total_lessons} lessons — title, course, keywords…"
      aria-label="Search lessons" data-index="search-index.json">
    <div id="searchResults" class="search-results" hidden></div>
  </div>
</div>
<section class="part tight"><div class="wide">{''.join(parts)}</div></section>"""
    page("curriculum/index.html", "Curriculum — Sun Devil Factory",
         "48 courses and 522 lessons mapped for a maintenance-to-manufacturing transition.",
         body, prefix, "curriculum")


def build_search_index(sems):
    idx = []
    for sem in sems:
        for c in sem["courses"]:
            for les in c["lessons"]:
                idx.append({
                    "t": les["t"],
                    "c": f"{c['code']} · {c['title']}",
                    "u": f"{sem['id']}/{c['id']}/{lesson_page_name(c, les)}",
                    "k": les.get("scope", "")[:140],
                })
    (OUT / "curriculum" / "search-index.json").write_text(
        json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    return len(idx)


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

    global ASSET_V
    ASSET_V = asset_version()

    global SOURCES
    SOURCES = load_sources()
    sems = load_curriculum()
    n_prev = sum(1 for s in sems for c in s["courses"] for l in c["lessons"]
                 if l.get("preview"))
    print(f"preview questions: {n_prev}/522 lessons")

    n_courses = sum(len(s["courses"]) for s in sems)
    n_lessons = sum(len(c["lessons"]) for s in sems for c in s["courses"])
    n_core = sum(1 for s in sems for c in s["courses"] for l in c["lessons"]
                 if l.get("core60"))
    print(f"courses={n_courses} lessons={n_lessons} core60={n_core}")

    build_curriculum_index(sems, "../")
    for sem in sems:
        for course in sem["courses"]:
            build_course_page(sems, sem, course, "../../../")
            tabs = load_tab_content(sem, course)
            for les in course["lessons"]:
                build_lesson_page(sems, sem, course, les, "../../../", tabs)
    build_static_pages(sems, "")
    n_idx = build_search_index(sems)
    n_pages = len(list(OUT.rglob("*.html")))
    n_embeds = sum(p.read_text(encoding="utf-8").count("youtube.com/embed")
                   for p in OUT.rglob("*.html"))
    print(f"search index: {n_idx} entries | embedded players: {n_embeds}")
    print(f"wrote {n_pages} pages -> {OUT}")


if __name__ == "__main__":
    main()
