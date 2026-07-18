#!/usr/bin/env python3
"""NEXUS INSTITUTE OF TECHNOLOGY — static site generator (Stages 2–4).

Zero dependencies. Reuses the data layer and verified-link machinery from
build.py (the retained previous-generation library) and emits the full Nexus
platform into docs/: centered brand chrome with Mission | Curriculum |
Career Paths, four-tab lesson pages (Foundations / Lecture / Worked
Examples / Library), interactive quiz engine, side drop-down section menu,
original vector illustrations (zero photography), EN/AR bilingual chrome
with RTL, installable PWA, and an honest completion tracker.

Integrity floor: no filler, no fabricated links, no unverified arithmetic,
zero "§" characters in output. Run:  python3 nexus_build.py
"""
import hashlib
import json
import re
import shutil

import build as legacy
from build import (DATA, OUT, ROOT, esc, fragment, lesson_page_name,
                   load_curriculum, load_sources, load_tab_content, slugify,
                   yt_embed_url)

ASSETS_NX = ROOT / "assets" / "nx"
MATHJAX = legacy.MATHJAX

# ---------------------------------------------------------------- i18n ----
AR = {
    "Mission": "الرسالة", "Curriculum": "المنهج", "Career Paths": "المسارات المهنية",
    "Sections": "الأقسام", "Foundations": "الأسس", "Lecture": "المحاضرة",
    "Worked Examples": "أمثلة محلولة", "Examples and Quiz": "الأمثلة والاختبار",
    "Library": "المكتبة", "Search": "ابحث", "All lessons": "كل الدروس",
}

# Owner-approved embed channels — STRICT list of exactly 15 (owner correction,
# 2026-07-17, supersedes ALL earlier embed policies). NPTEL and LearnChemE are
# explicitly BANNED from embedding, even where the registry carries them; their
# verified text links may remain in the references section only. A video embeds
# ONLY if its verified source matches one of these channels; otherwise the
# Library shows the honest "TODO: Find approved video" placeholder.
APPROVED_CHANNELS = ("mit opencourseware", "mit ocw",   # one org, two spellings
                     "engineer4free", "efficient engineer", "jeff hanson",
                     "engineering explained", "practical engineering",
                     "engineering mindset", "realpars", "solisplc",
                     "automationdirect", "plcprofessor", "galcotv",
                     "hegamastery", "siemens knowledge hub",
                     "schneider electric hub",
                     # owner expansion (Phase-3 / Global Directive, 2026-07-17/18):
                     "engineering deciphered", "randall manteufel",
                     "3blue1brown", "less boring lectures",
                     "husam's mech vision", "khan academy")

def channel_approved(name):
    low = (name or "").lower()
    return any(c in low for c in APPROVED_CHANNELS)
BRAND_AR = "معهد نيكسس للتكنولوجيا"
AR_LESSON_NOTE = ("محتوى هذا الدرس متاح حاليًا باللغة الإنجليزية. الترجمة "
                  "العربية للدروس تصل تباعًا مع اكتمال المحتوى — وواجهة "
                  "المنصة وصفحتا الرسالة والمسارات المهنية متاحة بالعربية "
                  "كاملة اليوم.")

# ------------------------------------------------- vector illustrations ----
def _svg(inner):
    return ('<svg viewBox="0 0 120 120" aria-hidden="true" fill="none" '
            'stroke-width="5" stroke-linecap="round" '
            'xmlns="http://www.w3.org/2000/svg">' + inner + "</svg>")

ILLOS = {
    "gear": _svg('<circle cx="60" cy="60" r="30"/><g><line x1="60" y1="14" x2="60" y2="30"/>'
        '<line x1="60" y1="90" x2="60" y2="106"/><line x1="14" y1="60" x2="30" y2="60"/>'
        '<line x1="90" y1="60" x2="106" y2="60"/><line x1="28" y1="28" x2="39" y2="39"/>'
        '<line x1="81" y1="81" x2="92" y2="92"/><line x1="92" y1="28" x2="81" y2="39"/>'
        '<line x1="39" y1="81" x2="28" y2="92"/></g><circle cx="60" cy="60" r="10" class="amb"/>'),
    "ladder": _svg('<line x1="24" y1="14" x2="24" y2="106"/><line x1="96" y1="14" x2="96" y2="106"/>'
        '<line x1="24" y1="38" x2="50" y2="38"/><line x1="70" y1="38" x2="96" y2="38"/>'
        '<line x1="50" y1="30" x2="50" y2="46"/><line x1="70" y1="30" x2="70" y2="46"/>'
        '<line x1="24" y1="74" x2="52" y2="74"/><line x1="68" y1="74" x2="96" y2="74"/>'
        '<circle cx="60" cy="74" r="9" class="amb"/>'),
    "gauge": _svg('<circle cx="60" cy="64" r="34"/><line x1="60" y1="64" x2="78" y2="46"/>'
        '<line x1="34" y1="88" x2="26" y2="96"/><line x1="86" y1="88" x2="94" y2="96"/>'
        '<circle cx="60" cy="64" r="6" class="amb"/><line x1="40" y1="40" x2="44" y2="46"/>'
        '<line x1="60" y1="30" x2="60" y2="37"/><line x1="80" y1="40" x2="76" y2="46"/>'),
    "lattice": _svg('<circle cx="30" cy="30" r="7"/><circle cx="90" cy="30" r="7"/>'
        '<circle cx="30" cy="90" r="7"/><circle cx="90" cy="90" r="7"/>'
        '<circle cx="60" cy="60" r="8" class="amb"/>'
        '<line x1="37" y1="30" x2="83" y2="30"/><line x1="37" y1="90" x2="83" y2="90"/>'
        '<line x1="30" y1="37" x2="30" y2="83"/><line x1="90" y1="37" x2="90" y2="83"/>'
        '<line x1="36" y1="36" x2="52" y2="52"/><line x1="84" y1="36" x2="68" y2="52"/>'
        '<line x1="36" y1="84" x2="52" y2="68"/><line x1="84" y1="84" x2="68" y2="68"/>'),
    "ladle": _svg('<path d="M30 26 L54 26 L50 54 L34 54 Z"/><line x1="54" y1="30" x2="66" y2="30"/>'
        '<path d="M42 54 L42 66" class="amb" stroke="none" fill="none"/>'
        '<line x1="42" y1="58" x2="42" y2="72"/><rect x="26" y="76" width="34" height="24" rx="3"/>'
        '<line x1="70" y1="88" x2="98" y2="88"/><line x1="78" y1="76" x2="98" y2="76"/>'
        '<circle cx="88" cy="100" r="5" class="amb"/>'),
    "lathe": _svg('<rect x="18" y="52" width="56" height="20" rx="9"/>'
        '<line x1="18" y1="62" x2="8" y2="62"/><line x1="84" y1="46" x2="84" y2="78"/>'
        '<path d="M84 62 L98 54"/><circle cx="98" cy="52" r="5" class="amb"/>'
        '<line x1="30" y1="84" x2="90" y2="84"/><line x1="30" y1="96" x2="90" y2="96"/>'),
    "press": _svg('<rect x="24" y="16" width="72" height="16" rx="4"/>'
        '<line x1="42" y1="32" x2="42" y2="56"/><line x1="78" y1="32" x2="78" y2="56"/>'
        '<rect x="34" y="56" width="52" height="12" rx="3" class="amb" stroke="none"/>'
        '<path d="M20 92 L52 92 L60 84 L68 92 L100 92"/><line x1="24" y1="104" x2="96" y2="104"/>'),
    "arc": _svg('<line x1="70" y1="16" x2="52" y2="52"/><rect x="66" y="8" width="18" height="12" rx="4"/>'
        '<path d="M52 56 L46 66 L56 64 L50 76" class="amb" stroke="none" fill="none"/>'
        '<path d="M50 56 L44 66 L54 64 L48 76"/><line x1="16" y1="88" x2="104" y2="88"/>'
        '<line x1="24" y1="100" x2="96" y2="100"/><circle cx="50" cy="84" r="4" class="amb"/>'),
    "curve": _svg('<line x1="20" y1="12" x2="20" y2="100"/><line x1="20" y1="100" x2="108" y2="100"/>'
        '<path d="M26 88 C 46 88, 52 34, 72 34 S 100 66, 104 60"/>'
        '<circle cx="72" cy="34" r="6" class="amb"/>'),
    "drafting": _svg('<path d="M24 96 L60 24 L96 96 Z"/><path d="M50 74 L70 74 L60 54 Z"/>'
        '<circle cx="94" cy="30" r="12"/><line x1="94" y1="24" x2="94" y2="36"/>'
        '<circle cx="60" cy="88" r="4" class="amb"/>'),
    "wave": _svg('<line x1="14" y1="60" x2="106" y2="60" stroke-dasharray="3 7"/>'
        '<path d="M14 60 C 22 26, 34 26, 42 60 S 60 96, 70 60 S 86 30, 94 52"/>'
        '<rect x="98" y="44" width="6" height="16" class="amb" stroke="none"/>'
        '<rect x="88" y="88" width="6" height="14" class="amb" stroke="none"/>'
        '<rect x="76" y="94" width="6" height="8" class="amb" stroke="none"/>'
        '<line x1="70" y1="102" x2="106" y2="102"/>'),
    "pump": _svg('<circle cx="56" cy="64" r="30"/><path d="M56 64 C 66 54, 74 52, 82 56"/>'
        '<path d="M56 64 C 52 50, 46 46, 38 46"/><path d="M56 64 C 50 76, 52 84, 60 90"/>'
        '<circle cx="56" cy="64" r="7" class="amb"/><line x1="86" y1="40" x2="104" y2="40"/>'
        '<line x1="86" y1="34" x2="86" y2="46"/>'),
    "flow": _svg('<path d="M14 40 L66 40 C 84 40, 84 64, 100 64"/>'
        '<path d="M14 56 L60 56 C 74 56, 76 78, 100 78"/>'
        '<path d="M14 72 L52 72 C 62 72, 64 92, 100 92"/>'
        '<circle cx="100" cy="40" r="5" class="amb"/>'),
    "circuit": _svg('<line x1="12" y1="60" x2="32" y2="60"/>'
        '<path d="M32 60 L38 48 L46 72 L54 48 L62 72 L68 60"/>'
        '<line x1="68" y1="60" x2="84" y2="60"/><line x1="84" y1="48" x2="84" y2="72"/>'
        '<line x1="92" y1="52" x2="92" y2="68"/><line x1="92" y1="60" x2="108" y2="60"/>'
        '<circle cx="20" cy="60" r="4" class="amb"/>'),
    "network": _svg('<circle cx="60" cy="28" r="9"/><circle cx="26" cy="82" r="9"/>'
        '<circle cx="94" cy="82" r="9"/><circle cx="60" cy="64" r="7" class="amb"/>'
        '<line x1="60" y1="37" x2="60" y2="56"/><line x1="54" y1="68" x2="33" y2="76"/>'
        '<line x1="66" y1="68" x2="87" y2="76"/>'),
    "robot": _svg('<rect x="18" y="92" width="40" height="12" rx="4"/>'
        '<line x1="38" y1="92" x2="38" y2="66"/><line x1="38" y1="66" x2="66" y2="42"/>'
        '<line x1="66" y1="42" x2="92" y2="52"/><circle cx="38" cy="66" r="6" class="amb"/>'
        '<circle cx="66" cy="42" r="6" class="amb"/><path d="M92 44 L102 40 M92 60 L102 64"/>'),
    "plan": _svg('<rect x="24" y="16" width="72" height="88" rx="8"/>'
        '<line x1="36" y1="38" x2="66" y2="38"/><rect x="36" y="50" width="48" height="8" class="amb" stroke="none"/>'
        '<rect x="36" y="66" width="32" height="8" class="amb" stroke="none"/>'
        '<rect x="36" y="82" width="40" height="8" class="amb" stroke="none"/>'),
    "shield": _svg('<path d="M60 12 L98 26 L98 58 C 98 84, 82 98, 60 108 C 38 98, 22 84, 22 58 L22 26 Z"/>'
        '<path d="M44 60 L56 72 L80 44"/><circle cx="60" cy="60" r="0" class="amb"/>'),
    "vessel": _svg('<path d="M40 30 C 40 18, 80 18, 80 30 L80 90 C 80 102, 40 102, 40 90 Z"/>'
        '<line x1="40" y1="44" x2="80" y2="44"/><line x1="40" y1="78" x2="80" y2="78"/>'
        '<line x1="80" y1="58" x2="100" y2="58"/><circle cx="104" cy="58" r="4" class="amb"/>'),
    "bathtub": _svg('<line x1="16" y1="14" x2="16" y2="100"/><line x1="16" y1="100" x2="108" y2="100"/>'
        '<path d="M20 30 C 32 66, 40 70, 58 70 C 80 70, 88 64, 100 30"/>'
        '<circle cx="58" cy="70" r="5" class="amb"/>'),
    "flag": _svg('<line x1="40" y1="12" x2="40" y2="106"/>'
        '<path d="M40 18 L92 26 L40 46"/><line x1="24" y1="106" x2="72" y2="106"/>'
        '<circle cx="40" cy="12" r="4" class="amb"/>'),
    "terminal": _svg('<rect x="14" y="24" width="92" height="70" rx="8"/>'
        '<path d="M28 44 L42 56 L28 68"/><line x1="50" y1="68" x2="72" y2="68"/>'
        '<circle cx="94" cy="36" r="4" class="amb"/>'),
    "caliper": _svg('<line x1="20" y1="24" x2="100" y2="24"/><line x1="34" y1="24" x2="34" y2="72"/>'
        '<line x1="78" y1="24" x2="78" y2="72"/><path d="M28 72 L40 72 L34 88 Z"/>'
        '<path d="M72 72 L84 72 L78 88 Z"/><line x1="34" y1="52" x2="78" y2="52" stroke-dasharray="3 6"/>'
        '<circle cx="56" cy="52" r="4" class="amb"/>'),
    "histogram": _svg('<line x1="18" y1="14" x2="18" y2="100"/><line x1="18" y1="100" x2="106" y2="100"/>'
        '<rect x="28" y="70" width="12" height="30" class="amb" stroke="none"/>'
        '<rect x="46" y="46" width="12" height="54" class="amb" stroke="none"/>'
        '<rect x="64" y="34" width="12" height="66" class="amb" stroke="none"/>'
        '<rect x="82" y="58" width="12" height="42" class="amb" stroke="none"/>'
        '<path d="M26 76 C 46 30, 74 22, 100 62"/>'),
}

COURSE_ILLO = {
    "math-1": "curve", "math-2": "curve", "statistics": "histogram",
    "computing": "terminal", "drawing-cad": "drafting",
    "statics": "gear", "dynamics": "gear", "strength": "gear",
    "machine-design-1": "gear", "machine-design-2": "gear",
    "kinematics-machinery": "gear", "vibrations": "wave",
    "materials-1": "lattice", "materials-2": "lattice", "corrosion": "lattice",
    "mfg-processes-1": "ladle", "mfg-processes-2": "lathe",
    "mfg-processes-3": "press", "welding-ndt": "arc", "metrology": "caliper",
    "thermo-1": "gauge", "thermo-2": "gauge", "heat-transfer": "gauge",
    "fluids": "flow", "hydraulics-pneumatics": "flow",
    "electrical": "circuit", "electronics-sensors": "circuit",
    "plc-1": "ladder", "plc-2": "ladder", "controls-1": "ladder",
    "instrumentation": "gauge", "robotics": "robot",
    "scada-iiot": "network", "smart-manufacturing": "network",
    "rotating-equipment": "pump", "condition-monitoring": "wave",
    "reliability-1": "bathtub", "reliability-2": "bathtub",
    "maintenance-fundamentals": "plan", "maintenance-planning": "plan",
    "production-planning": "plan", "lean-six-sigma": "histogram",
    "engineering-economics": "histogram", "asset-integrity": "shield",
    "pressure-equipment": "vessel", "safety": "shield", "hse": "shield",
    "capstone": "flag",
}

def illo(course_id):
    return ILLOS[COURSE_ILLO.get(course_id, "gear")]

# ------------------------------------------------------- transforms -------
SECTION_SIGN = "§"

def nx_text(html):
    """Nexus content transform: retire the section sign everywhere."""
    html = html.replace(f"{SECTION_SIGN}Worked Examples", "the Worked Examples tab")
    html = re.sub(rf"<h3>{SECTION_SIGN}(\d) · ", lambda m: f"<h3>0{m.group(1)} · ", html)
    html = re.sub(rf"{SECTION_SIGN}\s?(\d+)", r"\1", html)
    html = html.replace(SECTION_SIGN, "")
    return html

def nx_fragment(frag):
    """Photo-free fragment: drop hero/pagehead, convert photo figures to
    field notes (keeping only the original teaching caption), drop imgs."""
    frag = re.sub(r'<div class="hero[^"]*".*?<div class="hero-credit">.*?</div>\s*</div>',
                  "", frag, count=1, flags=re.S)
    frag = re.sub(r'\s*<div class="pagehead">.*?</div>\s*', "", frag, count=1, flags=re.S)

    def fig_to_note(m):
        block = m.group(0)
        note = re.search(r'<span class="notice"><b>NOTICE</b>(.*?)</span>', block, re.S)
        if note:
            return (f'<div class="fieldnote"><b>Field note</b> —{note.group(1)}</div>')
        return ""
    frag = re.sub(r'<figure class="bleed[^"]*">.*?</figure>', fig_to_note, frag, flags=re.S)
    frag = re.sub(r"<img[^>]*>", "", frag)
    return frag

# ------------------------------------------------------------ chrome ------
NX_PAGE = """<!doctype html>
<html lang="en" dir="ltr" data-root="{prefix}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0E1626">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="manifest" href="{prefix}manifest.webmanifest">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/nx/logo.svg">
<link rel="apple-touch-icon" href="{prefix}assets/nx/icons/icon-192.png">
<link rel="stylesheet" href="{prefix}assets/nx/nexus.css?v={v}">
{extra_head}</head>
<body{body_attrs}>
<header class="appbar">
  <div class="in">
    <a class="brand" href="{prefix}index.html" aria-label="{brand_ar} — Nexus Institute of Technology">
      <img src="{prefix}assets/nx/logo.svg" alt="">
      <span class="txt"><span class="teal">Nexus</span> Institute of Technology
        <small data-ar="تعليم هندسي عبر الإنترنت">Online Engineering Education</small></span>
    </a>
    <nav aria-label="Site">
      <a href="{prefix}index.html"{on_home} data-ar="{ar_mission}">Mission</a>
      <a href="{prefix}curriculum/index.html"{on_curr} data-ar="{ar_curr}">Curriculum</a>
      <a href="{prefix}career/index.html"{on_career} data-ar="{ar_career}">Career Paths</a>
    </nav>
    <span class="spacer"></span>
    <button id="langBtn" class="lang-btn" type="button">العربية</button>
  </div>
</header>
{sidemenu}
<main{main_class}>
{body}
</main>
<footer class="nx-foot">
  <div class="mark"><span class="teal">NEXUS</span> INSTITUTE OF TECHNOLOGY</div>
  <nav>
    <a href="{prefix}index.html" data-ar="{ar_mission}">Mission</a> ·
    <a href="{prefix}curriculum/index.html" data-ar="{ar_curr}">Curriculum</a> ·
    <a href="{prefix}career/index.html" data-ar="{ar_career}">Career Paths</a>
  </nav>
  <p class="lang-en">Bilingual engineering education. Worked-example values are
  pedagogical; representative industrial figures are labeled as such and are not
  published operating data of any named company. Every visual is an original vector
  illustration. Lessons not yet at full depth say so honestly.</p>
  <p class="lang-ar">تعليم هندسي ثنائي اللغة. قيم الأمثلة المحلولة تعليمية؛
  والأرقام الصناعية التمثيلية موسومة بذلك وليست بيانات تشغيل منشورة لأي شركة مسماة.
  كل عنصر بصري رسم متجهي أصلي. والدروس التي لم تبلغ عمقها الكامل تصرّح بذلك بصدق.</p>
</footer>
<script src="{prefix}assets/nx/nexus.js?v={v}"></script>
</body>
</html>
"""

NX_V = None

def sidemenu_html(items):
    """items: list of (href, label, ar_label_or_None, is_sub, data_tab)."""
    if not items:
        return ""
    rows = []
    for href, label, ar, sub, tab in items:
        cls = ' class="sub"' if sub else ""
        ar_attr = f' data-ar="{esc(ar)}"' if ar else ""
        tab_attr = f' data-tab="{tab}"' if tab else ""
        rows.append(f'<a href="{href}"{cls}{ar_attr}{tab_attr}>{label}</a>')
    return (f'<div class="sidemenu" id="sideMenu">'
            f'<button type="button" data-ar="{AR["Sections"]}">Sections</button>'
            f'<div class="panel"><p data-ar="{AR["Sections"]}">Sections</p>'
            f'{"".join(rows)}</div></div>')

def nx_page(path, title, desc, body, prefix, active="", extra_head="", menu=None,
            wrap=True, body_attrs=""):
    body = nx_text(body)
    html = NX_PAGE.format(
        title=esc(title), desc=esc(desc), prefix=prefix, body=body,
        extra_head=extra_head, v=NX_V, brand_ar=BRAND_AR,
        ar_mission=AR["Mission"], ar_curr=AR["Curriculum"], ar_career=AR["Career Paths"],
        sidemenu=sidemenu_html(menu or []),
        main_class=' class="wrap"' if wrap else "",
        body_attrs=body_attrs,
        on_home=' class="on"' if active == "home" else "",
        on_curr=' class="on"' if active == "curriculum" else "",
        on_career=' class="on"' if active == "career" else "",
    )
    assert SECTION_SIGN not in html, f"section sign leaked into {path}"
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

# ------------------------------------------------------------ library -----
# Canonical university-texts registry (owner directive 2026-07-18): the texts
# used at top-tier engineering schools, per course. Links were verified via
# the Open Library search API when the registry was built; texts without a
# verified url render as plain text. See data/textbooks.json.
TEXTBOOKS = json.loads((DATA / "textbooks.json").read_text(encoding="utf-8"))

def canonical_texts_html(course):
    keys = TEXTBOOKS["courses"].get(course["id"], [])
    if not keys:
        return ""
    items = []
    for k in keys:
        t = TEXTBOOKS["texts"][k]
        label = f'{esc(t["title"])}' + (f' — {esc(t["author"])}' if t["author"] else "")
        if t.get("url"):
            items.append(f'<li><a href="{esc(t["url"])}" target="_blank" '
                         f'rel="noopener">{label}</a></li>')
        else:
            items.append(f"<li>{label}</li>")
    return ('<p class="src"><b>The standard university texts</b> — the same '
            'references assigned at leading engineering schools:</p>'
            f'<ul class="plain small">{"".join(items)}</ul>')

def embed_card(url, caption, sub=""):
    """YouTube-only embeds, approved channels only (owner list, 2026-07-17)."""
    if not channel_approved(caption) and not channel_approved(sub):
        return ""
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
    """Course-level courseware: link cards only — the lesson Library carries
    at most ONE embedded video (owner architecture, 2026-07-17)."""
    cards = []
    for v in course.get("videos", []):
        cards.append(f"""
<a class="vid" href="{esc(v['url'])}" target="_blank" rel="noopener">
  <span class="vtag">{esc(v.get('tag', 'COURSE VIDEO — VERIFIED'))}</span>
  <h4>{esc(v['title'])}</h4>
  <p>{esc(v.get('note', ''))}</p>
  <span class="src">{esc(v['src'])}</span>
</a>""")
    return cards

def library_tab(les, course):
    """Owner lesson architecture (2026-07-17, revised 2026-07-18): exactly ONE
    embedded video from the approved-channel list (honest TODO placeholder
    otherwise), then the canonical university texts (data/textbooks.json,
    verified links only). Certifications are centralized on the Career Paths
    page (owner directive 2026-07-18) — no per-lesson certs block."""
    src_raw = les.get("src", "")
    src_html = legacy.linkify(esc(src_raw))
    taught = "".join(f"<li>{legacy.linkify(esc(t))}</li>"
                     for t in course.get("taught_from", []))

    video = ""
    # Per-lesson curated video (owner Library Patch, 2026-07-17): every id is
    # oEmbed-verified against the approved channel before entry to data.
    lv = les.get("video")
    if lv == "none":
        video = ('<div class="lib-video-todo">No relevant video found in the '
                 'approved channel list</div>'
                 '<p class="small">The approved channels were searched for this '
                 'lesson\'s topic; nothing suitable was verified. Only videos '
                 'from the approved list are ever embedded.</p>')
    elif isinstance(lv, dict):
        video = embed_card(f"https://www.youtube.com/watch?v={lv['id']}",
                           lv["title"], lv.get("channel", ""))
        assert video, f"lesson video failed approval gate: {lv}"
    for s in ([] if video else legacy.matched_sources(src_raw)):
        for key, cap in (("watch", s["name"] + " — lecture videos"), ("url", s["name"])):
            u = s.get(key)
            if u:
                video = embed_card(u, cap)
                if video:
                    break
        if video:
            break
    if not video:
        for v in course.get("videos", []):
            video = embed_card(v["url"], v["title"], v.get("src", ""))
            if video:
                break
    if not video:
        video = ('<div class="lib-video-todo">TODO: Find approved video</div>'
                 '<p class="small">Only videos from the approved-channel list embed '
                 'here; nothing is linked until it has been opened and verified.</p>')

    cards = video_cards(course)
    cards_html = (f'<h3>Course-level courseware — verified links</h3>'
                  f'<div class="vids">{"".join(cards)}</div>') if cards else ""

    # E2 — Supplemental/Arabic Resources (owner hierarchy rule, 2026-07-18):
    # link cards ONLY, never the primary frame; renders only when approved
    # resources exist in the lesson's "arabic" list.
    arabic_html = ""
    ar_items = les.get("arabic") or []
    if ar_items:
        rows = "".join(
            f'<li><a href="{esc(a["url"])}" target="_blank" rel="noopener" dir="ltr">'
            f'{esc(a["title"])}</a> <span class="src">{esc(a.get("channel", ""))}</span>'
            f'{("<p class=" + chr(34) + "small" + chr(34) + ">" + esc(a["note"]) + "</p>") if a.get("note") else ""}</li>'
            for a in ar_items)
        arabic_html = (f'<div class="lib-block lib-arabic">'
                       f'<h3 data-ar="مصادر تكميلية بالعربية">Supplemental/Arabic Resources</h3>'
                       f'<p class="small">Deep-understanding supplements in Arabic — the primary '
                       f'lesson video above remains the technical reference.</p>'
                       f'<ul class="plain">{rows}</ul></div>')

    return f"""
<div class="lib-block lib-video">
  <h3 data-ar="فيديو الدرس">Lesson video</h3>
  {video}
</div>
{arabic_html}
<div class="lib-block lib-books">
  <h3 data-ar="الكتب والمراجع">Textbooks &amp; references</h3>
  {canonical_texts_html(course)}
  <p class="src"><b>Taught from</b> — {src_html}</p>
  <ul class="plain small">{taught}</ul>
</div>
<div class="wide">{cards_html}</div>"""

# ------------------------------------------------------------ quiz --------
def quiz_html(items):
    n = len(items)
    has_mc = any(it["type"] == "mc" for it in items)
    parts = ['<div class="measure quiz">',
             '<p class="quiz-intro">Work every problem on paper first. '
             'Solved examples reveal their full solution; for the multiple-choice '
             'questions, select your answers and press <b>Submit</b> to see '
             'what was right, what was not, and why.</p>']
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
                             f'<span class="key">{key}</span><span>{ch}</span></button>')
            parts.append('</div><p class="quiz-verdict" hidden></p>')
        else:
            parts.append('<button type="button" class="quiz-reveal" '
                         'aria-expanded="false">Show the full solution</button>')
        parts.append(f'<div class="quiz-sol">{it["solution"]}</div></div>')
    if has_mc:
        parts.append(
            '<div class="quiz-actions">'
            '<button type="button" class="quiz-submit btn btn-primary" '
            'data-ar="إرسال الإجابات">Submit answers</button>'
            '<p class="quiz-score" hidden></p></div>')
    parts.append("</div>")
    return "".join(parts)

def preview_block(les):
    if not les.get("preview"):
        return ""
    qs = "".join(f"<li>{esc(q)}</li>" for q in les["preview"])
    return (f'<div class="preview"><b>After this lesson you can answer:</b>'
            f'<ul>{qs}</ul></div>')

def applied_block(html):
    return (f'<div class="applied"><span class="tag">Applied case — factory '
            f'floor (Kuwait)</span>{html}</div>')

# --------------------------------------------------------- lesson page ----
def hero(course, eyebrow, title, sub, meta):
    meta_html = "".join(f"<div>{m[0]}<b>{esc(m[1])}</b></div>" for m in meta)
    return f"""
<div class="nx-hero">
  <div class="bg">{illo(course["id"])}</div>
  <div class="txt">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{esc(title)}</h1>
    <p class="sub">{esc(sub)}</p>
  </div>
  <div class="meta">{meta_html}</div>
</div>"""

def build_lesson_page(sem, course, les, prefix, tabs_all):
    tabs = tabs_all.get(str(les["n"]), {})
    n_total = len(course["lessons"])
    tier = les.get("tier", 3)
    core = les.get("core60")
    frag_id = les.get("content")
    frag = None
    if frag_id:
        frag = fragment(f"lessons/{frag_id}.html")
        if frag is None:
            raise SystemExit(f"missing content fragment: {frag_id}")
        frag = nx_fragment(frag.replace("{{prefix}}", prefix))

    kw = les.get("kuwait")

    # ---- Lecture
    if tabs.get("lecture"):
        lecture = preview_block(les) + f'<div class="measure">{tabs["lecture"]}</div>'
        fmt = "Full lesson"
    elif frag:
        lecture = preview_block(les) + frag
        fmt = "Full lecture · ~90 min" if tier == 1 else "Study guide · Core 60"
    else:
        depth = ("This is a Core 60 lesson — its full study guide is in "
                 "production and will replace this page's skeleton." if core else
                 "In production: the scope above defines the lesson; full "
                 "teaching depth arrives with its course's authoring slot.")
        lecture = (f'<div class="measure">{preview_block(les)}'
                   f'<p class="queued-note">{depth}</p></div>')
        fmt = "Scope + sources (in production)"

    # ---- Foundations
    if tabs.get("foundations"):
        foundations = f'<div class="measure">{tabs["foundations"]}</div>'
    else:
        taught = "".join(f"<li>{legacy.linkify(esc(t))}</li>"
                         for t in course.get("taught_from", []))
        frag_note = ("<p>This lesson's foundations layer — prerequisite "
                     "refreshers and dependency map — is embedded in the "
                     "lecture itself: open the <b>Lecture</b> tab.</p>"
                     if frag and tier == 1 else "")
        foundations = f"""
<div class="measure">
  {frag_note}
  <p>This lesson belongs to <b>{esc(course['code'])} · {esc(course['title'])}</b>
  ({esc(sem['title'])}). It stands on the course's primary texts:</p>
  <ul class="plain">{taught}</ul>
  <p class="small">Course context: {esc(course['summary'])}</p>
</div>"""

    # ---- Worked Examples (quiz engine + applied cases merged here)
    if tabs.get("quiz"):
        examples = quiz_html(tabs["quiz"])
    elif tabs.get("examples"):
        examples = f'<div class="measure">{tabs["examples"]}</div>'
    elif frag and tier == 1:
        examples = ('<div class="measure"><p>The worked examples for this '
                    'lesson are written into the lecture as whiteboard boards — '
                    'open the <b>Lecture</b> tab and scroll to the dark board '
                    'sections. Each carries given data, numbered steps with '
                    'units, and an engineering read-out.</p></div>')
    elif frag:
        examples = ('<div class="measure"><p>This study guide carries one '
                    'condensed worked example inside the <b>Lecture</b> tab '
                    '(the boxed calculation). Full five-problem quiz depth '
                    'arrives when this lesson is promoted.</p></div>')
    elif les.get("preview"):
        qs = "".join(f"<li>{esc(q)}</li>" for q in les["preview"])
        examples = f"""
<div class="measure">
  <p>The five-problem interactive quiz for this lesson is in production. Until
  it lands, use the lesson's checkpoint questions as practice prompts —
  attempt them from the cited source before reading on:</p>
  <div class="preview"><b>Practice prompts — solutions not yet published:</b>
  <ul>{qs}</ul></div>
</div>"""
    else:
        examples = ('<div class="measure"><p class="queued-note">Worked '
                    'examples in production for this lesson.</p></div>')

    if tabs.get("kuwait"):
        examples += applied_block(tabs["kuwait"])
    elif frag:
        examples += ('<div class="applied"><span class="tag">Applied case</span>'
                     '<p>This lesson\'s factory-floor application is written '
                     'into the <b>Lecture</b> tab' +
                     (f' — anchor company: <b>{esc(kw)}</b>.' if kw else '.') +
                     '</p></div>')
    elif kw:
        examples += (f'<div class="applied"><span class="tag">Applied case</span>'
                     f'<p>Industry anchor for this lesson: <b>{esc(kw)}</b>. '
                     f'The full applied case is written when this lesson '
                     f'reaches full depth; the <a href="{prefix}career/index.html">'
                     f'Career Paths page</a> maps what {esc(kw)} runs and which '
                     f'roles touch this topic.</p></div>')

    library = library_tab(les, course)

    # ---- shell
    name = lesson_page_name(course, les)
    idx = next(i for i, l in enumerate(course["lessons"]) if l["n"] == les["n"])
    prev_l = course["lessons"][idx - 1] if idx > 0 else None
    next_l = course["lessons"][idx + 1] if idx + 1 < n_total else None
    nav = '<nav class="prevnext">'
    if prev_l:
        nav += (f'<a href="{lesson_page_name(course, prev_l)}">← '
                f'{prev_l["n"]:02d} · {esc(prev_l["t"])}</a>')
    nav += f'<a href="index.html" data-ar="{AR["All lessons"]} · {esc(course["code"])}">All lessons · {esc(course["code"])}</a>'
    if next_l:
        nav += (f'<a href="{lesson_page_name(course, next_l)}">'
                f'{next_l["n"]:02d} · {esc(next_l["t"])} →</a>')
    nav += "</nav>"

    core_chip = (f'<span class="badge amber">CORE 60 · {esc(core)}</span>'
                 if core else "")
    n_q = len(les.get("preview", []))
    assess = (f"{len(tabs['quiz'])}-problem interactive quiz" if tabs.get("quiz") else
              "2 worked boards + hidden-answer check" if frag and tier == 1 else
              "worked examples + checkpoint questions" if tabs.get("examples") else
              f"{n_q} checkpoint questions" if n_q else "in production")
    first_text = re.split(r"[—(;]", course.get("taught_from", [""])[0])[0].strip()[:44]

    lesson_key = f"{sem['id']}/{course['id']}/{les['n']}"
    outline_rows = []
    for l in course["lessons"]:
        cur = " cur" if l["n"] == les["n"] else ""
        outline_rows.append(
            f'<a href="{lesson_page_name(course, l)}" class="ol{cur}" '
            f'data-key="{sem["id"]}/{course["id"]}/{l["n"]}">'
            f'<span class="tick"></span><span>{l["n"]:02d} · {esc(l["t"])}</span></a>')
    outline = f"""
<aside class="outline" id="outline" aria-label="Course outline">
  <div class="oh">
    <a href="index.html">{esc(course['code'])} · {esc(course['title'])}</a>
    <div class="bar"><i></i></div><span class="ptext"></span>
  </div>
  {''.join(outline_rows)}
</aside>"""

    body = f"""
<div class="player">
{outline}
<div class="lesson-main">
<nav class="crumbs"><a href="{prefix}curriculum/index.html" data-ar="{AR['Curriculum']}">Curriculum</a> /
<a href="index.html">{esc(course['code'])}</a> /
<span>Lesson {les['n']:02d} of {n_total}</span></nav>
{hero(course, f"{esc(course['code'])} · LESSON {les['n']:02d} OF {n_total} · {esc(sem['title'].upper())}",
      les["t"], les.get("scope", ""),
      [("Format", fmt), ("Primary text", first_text), ("Assessment", assess)])}
<div class="lesson-tools">
  <button id="completeBtn" class="complete-btn" type="button" data-key="{lesson_key}">Mark as complete</button>
  {core_chip}
</div>
<div class="lang-ar"><div class="ar-note">{AR_LESSON_NOTE}</div></div>
<div class="tabs" role="tablist">
  <button class="on" data-tab="t-lecture" data-ar="{AR['Lecture']}">Lecture</button>
  <button data-tab="t-foundations" data-ar="{AR['Foundations']}">Foundations</button>
  <button data-tab="t-examples" data-ar="{AR['Examples and Quiz']}">Examples and Quiz</button>
  <button data-tab="t-library" data-ar="{AR['Library']}">Library</button>
</div>
<section class="tabpanel on" id="t-lecture"><h2 class="tabcap" data-ar="{AR['Lecture']}">Lecture</h2>{lecture}</section>
<section class="tabpanel" id="t-foundations"><h2 class="tabcap" data-ar="{AR['Foundations']}">Foundations</h2>{foundations}</section>
<section class="tabpanel" id="t-examples"><h2 class="tabcap" data-ar="{AR['Examples and Quiz']}">Examples and Quiz</h2>{examples}</section>
<section class="tabpanel" id="t-library"><h2 class="tabcap" data-ar="{AR['Library']}">Library</h2>{library}</section>
{nav}
</div>
</div>"""

    nx_page(f"curriculum/{sem['id']}/{course['id']}/{name}",
            f"{les['t']} — {course['title']} — Nexus Institute of Technology",
            les.get("scope", "")[:150], body, prefix, "curriculum",
            extra_head=MATHJAX, wrap=False,
            body_attrs=f' data-key="{lesson_key}"')

# --------------------------------------------------------- course page ----
def lesson_depth(les, tabs_all):
    return bool(tabs_all.get(str(les["n"]), {}).get("lecture")) or bool(les.get("content"))

def tier_badge(les, tabs_all):
    t = les.get("tier", 3)
    tabs = tabs_all.get(str(les["n"]), {})
    if tabs.get("lecture"):
        return '<span class="badge t1">Full lesson</span>'
    if t == 1 and les.get("content"):
        return '<span class="badge t1">Full lecture</span>'
    if t == 2 and les.get("content"):
        return '<span class="badge t2">Study guide</span>'
    if t in (1, 2):
        return '<span class="badge queued">Core 60 · in production</span>'
    return ""

def build_course_page(sem, course, prefix, tabs_all):
    rows = []
    for les in course["lessons"]:
        href = lesson_page_name(course, les)
        core = les.get("core60")
        core_note = f' <b>CORE 60 · {esc(core)}</b> ·' if core else ""
        checkpoints = ""
        if les.get("preview"):
            qs = "".join(f"<li>{esc(q)}</li>" for q in les["preview"])
            checkpoints = (f'<details><summary data-ar="أسئلة التحقق">Checkpoint '
                           f'questions</summary><ul>{qs}</ul></details>')
        rows.append(f"""
<div class="syl" data-key="{sem['id']}/{course['id']}/{les['n']}" data-href="{href}">
  <span class="tick"></span>
  <div class="no">{les['n']:02d}</div>
  <div class="body">
    <h4><a href="{href}">{esc(les["t"])}</a>{tier_badge(les, tabs_all)}</h4>
    <p class="scope">{esc(les.get("scope", ""))}</p>
    <p class="src"><b>Taught from</b> —{core_note} {legacy.linkify(esc(les.get("src", "")))}</p>
    {checkpoints}
  </div>
</div>""")

    # "What you'll learn" — verbatim first sentences of existing scope text
    learn = []
    for les in course["lessons"][:6]:
        first = les.get("scope", "").split(".")[0].strip()
        if first:
            learn.append(f'<div><span class="ck">✓</span><span>{esc(first)}.</span></div>')
    learn_html = (f'<div class="learn"><h3 data-ar="ما الذي ستتعلمه">What you\'ll learn</h3>'
                  f'<div class="learn-grid">{"".join(learn)}</div></div>') if learn else ""

    taught = "".join(f"<li>{legacy.linkify(esc(t))}</li>"
                     for t in course.get("taught_from", []))
    cards = video_cards(course)
    vids = (f'<h3>Open courseware for this course</h3><div class="vids">'
            f'{"".join(cards)}</div>') if cards else ""
    # Career module — the ONLY place company names are permitted (owner rule
    # 2026-07-17: academic tabs strictly company-free; career/employment
    # content may and should name real local, regional, and global employers).
    career = (f'<div class="career-block"><span class="tag">Career outlook — '
              f'where this course pays</span>{course["career"]}'
              f'<p class="small"><a href="{prefix}career/index.html">'
              f'Explore career paths →</a></p></div>') if course.get("career") else ""
    n_core = sum(1 for l in course["lessons"] if l.get("core60"))
    n_depth = sum(1 for l in course["lessons"] if lesson_depth(l, tabs_all))
    n_quiz = sum(1 for l in course["lessons"]
                 if tabs_all.get(str(l["n"]), {}).get("quiz"))
    chips = [f"{len(course['lessons'])} lessons",
             f"{n_depth} of {len(course['lessons'])} at full depth"]
    if n_quiz:
        chips.append(f"{n_quiz} interactive quizzes")
    if n_core:
        chips.append(f"{n_core} Core-60 lessons")
    chips_html = "".join(f'<span class="mchip">{esc(c)}</span>' for c in chips)

    hero_html = f"""
<div class="nx-hero">
  <div class="bg">{illo(course["id"])}</div>
  <div class="txt">
    <p class="eyebrow">{esc(course['code'])} · {esc(sem['title'].upper())}</p>
    <h1>{esc(course['title'])}</h1>
    <p class="sub">{esc(course['summary'])}</p>
  </div>
  <div class="metachips">{chips_html}</div>
</div>"""

    body = f"""
<nav class="crumbs"><a href="{prefix}curriculum/index.html" data-ar="{AR['Curriculum']}">Curriculum</a> /
<span>{esc(course['code'])}</span></nav>
{hero_html}
<div class="cta-row">
  <a id="resumeBtn" class="btn btn-primary" href="{lesson_page_name(course, course['lessons'][0])}">Start lesson 01</a>
  <a class="btn btn-ghost" href="{prefix}curriculum/index.html" data-ar="{AR['Curriculum']}">Full curriculum</a>
</div>
{learn_html}
<section class="part tight">
  <div class="wide">
    <h3 data-ar="المنهج الدراسي">Syllabus</h3>
    <div class="lessons">{''.join(rows)}</div>
    <ul class="plain small">{taught}</ul>
    {vids}
    {career}
  </div>
</section>"""
    nx_page(f"curriculum/{sem['id']}/{course['id']}/index.html",
            f"{course['title']} — Nexus Institute of Technology",
            course["summary"][:150], body, prefix, "curriculum")

# ----------------------------------------------------- curriculum index ---
def build_curriculum_index(sems, tabs_by_course, prefix):
    total = sum(len(c["lessons"]) for s in sems for c in s["courses"])
    depth = sum(1 for s in sems for c in s["courses"] for l in c["lessons"]
                if lesson_depth(l, tabs_by_course[(s["id"], c["id"])]))
    pct = round(100 * depth / total)
    cards = []
    chips = ['<button type="button" class="chip on" data-sem="all" data-ar="الكل">All</button>']
    for sem in sems:
        chips.append(f'<button type="button" class="chip" data-sem="{sem["id"]}">'
                     f'{esc(sem["title"])}</button>')
        for c in sem["courses"]:
            tabs_all = tabs_by_course[(sem["id"], c["id"])]
            n_depth = sum(1 for l in c["lessons"] if lesson_depth(l, tabs_all))
            depth_txt = ('<b>complete</b> · ' if n_depth == len(c["lessons"])
                         else f'<b>{n_depth} built</b> · ' if n_depth else "")
            cards.append(f"""
<a class="course-card" href="{sem['id']}/{c['id']}/index.html" data-sem="{sem['id']}"
   data-key="{sem['id']}/{c['id']}" data-n="{len(c['lessons'])}">
  <span class="cap">{illo(c['id'])}</span>
  <span class="code">{esc(c['code'])} · {esc(sem['title'])}</span>
  <h4>{esc(c['title'])}</h4>
  <p>{esc(c['summary'][:110])}…</p>
  <span class="meta">{depth_txt}{len(c['lessons'])} lessons</span>
  <span class="pbar"><i></i></span>
  <span class="pnote"></span>
</a>""")
    parts = [f'<div class="chips" id="semChips">{"".join(chips)}</div>',
             f'<div class="course-grid">{"".join(cards)}</div>']
    body = f"""
<div class="pagehead">
  <p class="kicker"><span class="n">CURRICULUM</span>4 years · 8 semesters</p>
  <h1>48 courses. {total} lessons. One pathway.</h1>
  <p class="sub">The complete B.S.-shaped map — from foundational mathematics and physics
  to Industry 4.0 — covering every core mechanical-engineering discipline and role. Every
  lesson already has its own page — scope, sources, and checkpoint questions — and full
  teaching depth is rolling out course by course, tracked honestly below. The catalog
  is a strict grid — 6 classes per semester, 11 lessons per class, 528 lessons — built
  as authored content, never as padding.</p>
  <div class="tracker">
    <p class="small"><b>{depth} of {total}</b> lessons at full teaching depth · {pct}% —
    updated with every build. The rest are in production, in queue order.</p>
    <div class="bar"><i style="width:{pct}%"></i></div>
    <p class="small">Full depth = complete lecture + foundations + five-problem interactive
    quiz (or a Tier-1 lecture / Core-60 study guide).</p>
  </div>
  <div class="searchbox">
    <input type="search" id="lessonSearch" placeholder="Search all {total} lessons — title, course, keywords…"
      data-ar-placeholder="ابحث في كل الدروس — العنوان أو المقرر أو الكلمات المفتاحية…"
      aria-label="Search lessons" data-index="search-index.json">
    <div id="searchResults" class="search-results" hidden></div>
  </div>
</div>
<div class="catch"><b>Depth you can audit.</b> Every claim on this page is recomputed from the content at build time.</div>
<section class="part tight"><div class="wide">{''.join(parts)}</div></section>"""
    nx_page("curriculum/index.html", "Curriculum — Nexus Institute of Technology",
            f"48 courses, {total} lessons: the complete mechanical-engineering map "
            f"from first principles to Industry 4.0; {depth} at full depth.",
            body, prefix, "curriculum")
    return total, depth

# ------------------------------------------------------------- statics ----
def build_static_pages():
    mission = fragment("pages/mission.html")
    nx_page("index.html",
            "Nexus Institute of Technology — Learn Mechanical Engineering from Scratch to Industry 4.0",
            "A complete, bilingual B.S.-shaped mechanical engineering "
            "curriculum for anyone — from zero background to Industry 4.0.",
            mission, "", "home",
            menu=[("#premise", "The premise", "الفكرة", False, None),
                  ("#method", "How content is built", "طريقة البناء", False, None),
                  ("#start", "Where to start", "من أين تبدأ", False, None),
                  ("#integrity", "The integrity floor", "أرضية النزاهة", False, None)])

    career_en = fragment("pages/career.html")
    career_ar = fragment("pages/career-ar.html")
    career = (f'<div class="lang-en">{career_en}</div>'
              f'<div class="lang-ar" dir="rtl">{career_ar}</div>')
    nx_page("career/index.html",
            "Career Paths — Nexus Institute of Technology",
            "Careers in advanced industrial systems: the full role landscape, "
            "the certification architecture, interview mastery, and a "
            "twelve-month development plan.",
            career, "../", "career",
            menu=[("#top", "The landscape", "الخريطة", False, None)])

def build_search_index(sems):
    idx = []
    for sem in sems:
        for c in sem["courses"]:
            for les in c["lessons"]:
                idx.append({"t": les["t"], "c": f"{c['code']} · {c['title']}",
                            "u": f"{sem['id']}/{c['id']}/{lesson_page_name(c, les)}",
                            "k": les.get("scope", "")[:140]})
    (OUT / "curriculum" / "search-index.json").write_text(
        json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    return len(idx)

# --------------------------------------------------------------- main -----
def main():
    global NX_V
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / ".nojekyll").write_text("")
    shutil.copytree(ASSETS_NX, OUT / "assets" / "nx")
    shutil.copy(ROOT / "nexus" / "logo.svg", OUT / "assets" / "nx" / "logo.svg")

    h = hashlib.sha256()
    for rel in ("nexus.css", "nexus.js"):
        h.update((ASSETS_NX / rel).read_bytes())
    h.update((ROOT / "nexus" / "logo.svg").read_bytes())
    NX_V = h.hexdigest()[:10]

    manifest = (ASSETS_NX / "manifest.webmanifest").read_text(encoding="utf-8")
    (OUT / "manifest.webmanifest").write_text(manifest, encoding="utf-8")
    sw = (ASSETS_NX / "sw.js").read_text(encoding="utf-8").replace("__NX_V__", NX_V)
    (OUT / "sw.js").write_text(sw, encoding="utf-8")
    (OUT / "assets" / "nx" / "sw.js").unlink()
    (OUT / "assets" / "nx" / "manifest.webmanifest").unlink()

    legacy.SOURCES = load_sources()
    sems = load_curriculum()

    tabs_by_course = {}
    for sem in sems:
        for c in sem["courses"]:
            tabs_by_course[(sem["id"], c["id"])] = load_tab_content(sem, c)

    n_pages = 1  # curriculum index
    total, depth = build_curriculum_index(sems, tabs_by_course, "../")
    for sem in sems:
        for c in sem["courses"]:
            tabs_all = tabs_by_course[(sem["id"], c["id"])]
            build_course_page(sem, c, "../../../", tabs_all)
            n_pages += 1
            for les in c["lessons"]:
                build_lesson_page(sem, c, les, "../../../", tabs_all)
                n_pages += 1
    build_static_pages()
    n_pages += 2
    n_idx = build_search_index(sems)

    # ---------------- integrity audit over emitted output ----------------
    bad_sign, bad_img = [], []
    n_embeds = 0
    for p in OUT.rglob("*.html"):
        txt = p.read_text(encoding="utf-8")
        if SECTION_SIGN in txt:
            bad_sign.append(p)
        imgs = re.findall(r"<img[^>]*>", txt)
        for i in imgs:
            if "assets/nx/logo.svg" not in i:
                bad_img.append((p, i[:80]))
        n_embeds += txt.count("youtube.com/embed")
        if "nptel" in txt.lower():
            assert "youtube.com/embed" not in txt.lower().split("nptel")[0][-200:], p
    assert not bad_sign, f"section sign leaked: {bad_sign[:3]}"
    assert not bad_img, f"non-logo <img> leaked: {bad_img[:3]}"

    print(f"NEXUS build {NX_V}")
    print(f"pages: {n_pages} | search index: {n_idx} | embeds: {n_embeds}")
    print(f"coverage: {depth}/{total} lessons at full depth "
          f"({round(100*depth/total)}%)")
    print(f"wrote -> {OUT}")


if __name__ == "__main__":
    main()
