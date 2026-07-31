#!/usr/bin/env python3
"""Assemble the MechEd design-review gallery artifact (single self-contained HTML)."""
import base64
import json
import re
from pathlib import Path

SP = Path(__file__).parent
LOGOS = Path("/Users/ilmshri/Social Media/nexus-design-drafts/design-previews/logo-candidates")
IMG = json.load(open(SP / "b64_images.json"))
WEIGHTS = json.load(open(SP / "photos/weights.json"))
META = json.load(open(SP / "photos/meta.json"))

F = {k: (SP / f"b64_{k}.txt").read_text() for k in ("serif600", "serif400", "sans400", "sans600")}


def svg(name):
    s = (LOGOS / name).read_text()
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    return s.strip()


CAND = [
    ("c1", "Incumbent — slab M", svg("c1-incumbent.svg"),
     "The mark shipped with the 07-26 rebrand: cream tile, navy slab M, gold keyline and pearl. The control every challenger must beat."),
    ("c2", "Serif M tile", svg("c2-serif-m.svg"),
     "The wordmark's own capital, cut from Source Serif 4 — the site's display face becomes the mark. Pairs natively with candidate 3."),
    ("c3", "Wordmark lockup", svg("c3-wordmark-lockup.svg"),
     "Type-led: MechEd set in Source Serif 4, gold rule, dual descriptors — ENGINEERED TO INNOVATE and هندسةٌ للابتكار sharing one line (the itqan.edu.sa pattern). Uses the serif M tile (candidate 2) wherever a square icon is required."),
    ("c4", "Gear coin", svg("c4-gear-coin.svg"),
     "The one pictorial device: a machined coin edge around the serif M. Most literal 'mechanical' register; the busiest at small sizes."),
    ("c5", "Gauge sweep", svg("c5-moment-arc.svg"),
     "The incumbent's slab M with a gold instrument-arc — mines the old moment-arm study as a measuring sweep. Quietest way to add motion to the mark."),
    ("c6", "Shield", svg("c6-shield.svg"),
     "A re-cut of the retired Academic Shield in the current language: single navy outline, gold inner keyline, serif M. The most 'official institution' register on the board."),
]
WORDMARK_ONLY = svg("c3-wordmark-only.svg")


def photo(k):
    return "data:image/jpeg;base64," + IMG[k]


LIC_ROWS = []
CAPTIONS = {
    "machining": "Representative example: morse-taper lathe tooling in a workshop tray",
    "thermal": "Representative example: technician blading a steam-turbine rotor",
    "divider": "Representative example: steam-turbine assembly hall",
    "mechanisms": "Representative example: gear train of a tower-clock movement",
    "metrology": "Representative example: micrometer measurement of a machined part",
    "band": "Archival: machine floor with power shear and riveting machines (c. 1875 plant, HABS survey)",
}
for slot, m in META.items():
    LIC_ROWS.append(
        f'<tr><td>{slot}</td><td><a href="{m["page"]}" target="_blank" rel="noopener">{m["title"].replace("File:", "")[:44]}…</a></td>'
        f'<td>{m["licence"]}</td><td>{(m["artist"] or "US government work (public domain)")[:38]}</td><td class="cap">{CAPTIONS[slot]}</td></tr>')

WROWS = []
for r in WEIGHTS:
    WROWS.append(
        f'<tr><td>{r["slot"]}</td><td>{r["use"]}</td><td>{r["size"]}</td>'
        f'<td>{r["desktopWebpKB"]} <span class="dim">/ {r["desktopJpgKB"]}</span></td>'
        f'<td>{r["mobileWebpKB"]} <span class="dim">/ {r["mobileJpgKB"]}</span></td>'
        f'<td>{r["duoWebpKB"]} <span class="dim">/ {r["duoJpgKB"]}</span></td></tr>')

avg_desk = sum(r["desktopWebpKB"] for r in WEIGHTS[:4]) // 4
avg_mob = sum(r["mobileWebpKB"] for r in WEIGHTS[:4]) // 4


def insitu_row(cid, title, tile_svg, header_inner):
    return f'''
<div class="insitu" id="row-{cid}">
  <div class="insitu-head"><span class="cid">{cid.upper()}</span> {title}</div>
  <div class="ctx-grid">
    <div class="ctx ctx-wide"><div class="ctx-label">Site header (real chrome)</div>
      <div class="mock-appbar">{header_inner}
        <nav><span>Home</span><span>About</span><span class="on">Curriculum</span><span>Resources</span><span>Career Paths</span></nav>
      </div></div>
    <div class="ctx"><div class="ctx-label">Favicon · 16&nbsp;px</div>
      <div class="mock-tab"><span class="f16">{tile_svg}</span><span class="tabtxt">MechEd — Curriculum</span></div></div>
    <div class="ctx"><div class="ctx-label">Phone app icon</div>
      <div class="ios-wrap"><span class="ios">{tile_svg}</span><span class="ioslbl">MechEd</span></div></div>
    <div class="ctx"><div class="ctx-label">Maskable (Android crop)</div>
      <div class="mask-wrap"><span class="maskable">{tile_svg}</span></div></div>
    <div class="ctx"><div class="ctx-label">Printed summary header</div>
      <div class="mock-print"><span class="pr-logo">{tile_svg}</span>
        <span class="pr-title">Engineering Mathematics I — Course summary</span><span class="pr-rule"></span></div></div>
  </div>
</div>'''


INSITU = []
for cid, title, s, _ in CAND:
    if cid == "c3":
        header = f'<span class="brand-wm">{WORDMARK_ONLY}</span><span class="tagline">ENGINEERED TO INNOVATE</span>'
        INSITU.append(insitu_row(cid, title + " (tile contexts use its companion C2)", svg("c2-serif-m.svg"), header))
    else:
        header = (f'<span class="brand-logo">{s}</span><span class="brand-txt">MechEd'
                  f'<span class="tagline">ENGINEERED TO INNOVATE</span></span>')
        INSITU.append(insitu_row(cid, title, s, header))

CARDS = []
for cid, title, s, why in CAND:
    big = "big-wide" if cid == "c3" else "big"
    CARDS.append(f'''<div class="cand"><div class="{big}">{s}</div>
      <div class="cand-name"><span class="cid">{cid.upper()}</span> {title}</div><p>{why}</p></div>''')

html = """<title>MechEd — Design Review: Motion · Logo · Photography</title>
<style>
@font-face{font-family:'SS4';src:url(data:font/woff2;base64,__SERIF600__) format('woff2');font-weight:600}
@font-face{font-family:'SS4';src:url(data:font/woff2;base64,__SERIF400__) format('woff2');font-weight:400}
@font-face{font-family:'SSans';src:url(data:font/woff2;base64,__SANS400__) format('woff2');font-weight:400}
@font-face{font-family:'SSans';src:url(data:font/woff2;base64,__SANS600__) format('woff2');font-weight:600}
:root{--paper:#FDFCFB;--surface:#FFFFFF;--sunken:#F6F4F1;--ink:#20325A;--soft:#44506B;--muted:#6E7688;
--line:#ECE9E3;--line2:#DBD7CF;--royal:#2D5397;--navy:#14294B;--gold:#CBA85F;--gold-tint:#F9F3E4;
--serif:'SS4',Georgia,serif;--sans:'SSans',-apple-system,'Helvetica Neue',Arial,sans-serif;color-scheme:only light}
html{background:var(--paper)}
body{margin:0;font:16px/1.65 var(--sans);color:var(--ink);background:var(--paper);-webkit-text-size-adjust:100%}
.wrap{max-width:1060px;margin-inline:auto;padding:0 20px 90px}
header.masthead{padding:34px 0 18px;border-bottom:2px solid var(--navy);margin-bottom:0}
.masthead .kicker{font:600 11.5px/1 var(--sans);letter-spacing:.18em;color:var(--gold);text-transform:uppercase}
.masthead h1{font:600 clamp(26px,5vw,38px)/1.15 var(--serif);margin:10px 0 6px;text-wrap:balance}
.masthead p{margin:0;color:var(--soft);max-width:64ch}
.tabs{position:sticky;top:0;background:var(--paper);z-index:50;display:flex;gap:4px;padding:10px 0;border-bottom:1px solid var(--line2)}
.tabs button{font:600 13.5px var(--sans);letter-spacing:.04em;border:1px solid var(--line2);background:var(--surface);
color:var(--soft);padding:9px 16px;border-radius:8px;cursor:pointer;min-height:40px}
.tabs button.on{background:var(--navy);border-color:var(--navy);color:#fff}
.tabs button:focus-visible{outline:2px solid var(--royal);outline-offset:2px}
section.pane{display:none;padding-top:26px}section.pane.on{display:block}
h2{font:600 26px/1.2 var(--serif);margin:8px 0 4px}
h3{font:600 19px/1.3 var(--serif);margin:26px 0 6px}
.lede{color:var(--soft);max-width:70ch;margin:0 0 14px}
.note{background:var(--gold-tint);border:1px solid var(--gold);border-radius:8px;padding:12px 16px;margin:16px 0;font-size:14.5px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:14px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px}
.twrap{overflow-x:auto;margin:10px 0}
th{font:600 11px var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:8px 10px;border-bottom:2px solid var(--navy);white-space:nowrap}
td{padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
td.cap{font-style:italic;color:var(--soft);min-width:200px}
.dim{color:var(--muted)}
tbody tr:nth-child(even){background:var(--sunken)}
a{color:var(--royal)}
.rate{border-inline-start:3px solid var(--gold);background:var(--surface);border-radius:0 8px 8px 0;padding:12px 16px;margin:22px 0;font-size:14.5px}
.rate b{font-family:var(--serif)}
/* ---------------- simulator ---------------- */
.simbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:12px 0}
.simbar label{font:600 13px var(--sans);display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line2);
background:var(--surface);border-radius:8px;padding:8px 12px;cursor:pointer;min-height:40px;box-sizing:border-box}
.simbar label.on{border-color:var(--navy);background:var(--navy);color:#fff}
.simbar input{accent-color:var(--royal)}
#simcap{font-size:13.5px;color:var(--soft);margin:4px 0 10px;min-height:2.6em}
#simframe{border:1px solid var(--line2);border-radius:12px;overflow:hidden;background:var(--paper);box-shadow:0 1px 2px rgba(32,50,90,.05)}
.sim-appbar{display:flex;align-items:center;gap:10px;background:var(--surface);border-bottom:1px solid var(--line);padding:10px 16px}
.sim-appbar .sl{width:24px;height:24px;flex:none}
.sim-appbar .sb{font:600 16px var(--serif)}
.sim-appbar .sn{margin-inline-start:auto;display:flex;gap:12px;font:600 11.5px var(--sans);color:var(--soft)}
#simpage{padding:18px 20px 26px;min-height:340px}
.sim-kick{font:600 10.5px var(--sans);letter-spacing:.16em;color:var(--gold);text-transform:uppercase}
.sim-h1{font:600 24px/1.2 var(--serif);margin:6px 0 8px}
.sim-sub{color:var(--soft);font-size:14px;margin:0 0 14px;max-width:56ch}
.sim-card{border:1px solid var(--line);background:var(--surface);border-radius:9px;padding:12px 14px;margin:10px 0;cursor:pointer}
.sim-card:hover{border-color:var(--royal)}
.sim-card .cc{font:600 10.5px ui-monospace,monospace;color:var(--muted);letter-spacing:.08em}
.sim-card .ct{font:600 16px var(--serif);margin:2px 0}
.sim-card p{margin:0;font-size:13px;color:var(--soft)}
.sim-row{display:flex;gap:10px;align-items:baseline;border-bottom:1px solid var(--line);padding:10px 4px;cursor:pointer}
.sim-row:hover .rt{color:var(--royal)}
.sim-row .no{font:600 12px ui-monospace,monospace;color:var(--muted)}
.sim-row .rt{font:600 15px var(--serif)}
.sim-tabs{display:flex;gap:14px;border-bottom:1px solid var(--line2);margin:14px 0 4px;font:600 11.5px var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.sim-tabs span{padding:6px 2px;border-bottom:3px solid transparent}
.sim-tabs .on{color:var(--ink);border-color:var(--gold)}
.sim-nav{display:flex;justify-content:space-between;gap:10px;margin-top:22px;font:600 13px var(--sans)}
.sim-nav a{cursor:pointer;text-decoration:none;padding:8px 0;display:inline-block}
.sim-crumb{font:12px var(--sans);color:var(--muted);margin-bottom:10px}
.sim-crumb a{cursor:pointer}
.sim-video{background:var(--navy);color:#cfd8ea;border-radius:9px;padding:26px 14px;text-align:center;font:600 12px var(--sans);letter-spacing:.06em;margin:12px 0}
::view-transition-old(sim-page){animation-duration:var(--vt-old,.14s);animation-timing-function:ease-out}
::view-transition-new(sim-page){animation-duration:var(--vt-new,.22s);animation-timing-function:ease-in-out}
::view-transition-group(*){animation-duration:.3s;animation-timing-function:cubic-bezier(.2,.7,.2,1)}
html.lift ::view-transition-old(sim-page){animation:simlift .12s ease-out both}
html.lift ::view-transition-new(sim-page){animation:simsettle .3s cubic-bezier(.2,.7,.2,1) both}
@keyframes simlift{to{opacity:0}}
@keyframes simsettle{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){::view-transition-group(*),::view-transition-old(*),::view-transition-new(*){animation:none !important}}
.stills{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:12px 0}
.stills figure{margin:0}
.stills img{width:100%;border:1px solid var(--line2);border-radius:8px;display:block}
.stills figcaption{font-size:12px;color:var(--muted);padding-top:4px}
/* ---------------- logo section ---------------- */
.cands{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:14px 0}
.cand{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px}
.cand .big svg{width:104px;height:104px;display:block;margin:6px auto 10px}
.cand .big-wide svg{width:100%;max-width:330px;height:auto;display:block;margin:14px auto}
.cand-name{font:600 15px var(--sans);margin:2px 0 4px}
.cand p{font-size:13.5px;color:var(--soft);margin:0}
.cid{display:inline-block;font:600 10.5px ui-monospace,monospace;background:var(--navy);color:#fff;border-radius:4px;padding:2px 6px;margin-inline-end:4px;letter-spacing:.06em}
.insitu{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:12px 0}
.insitu-head{font:600 14.5px var(--sans);margin-bottom:10px}
.ctx-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.ctx-wide{grid-column:1/-1}
.ctx-label{font:600 10px var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.mock-appbar{display:flex;align-items:center;gap:10px;background:var(--surface);border:1px solid var(--line2);border-radius:8px;padding:10px 14px;overflow:hidden}
.mock-appbar .brand-logo svg{width:30px;height:30px;display:block}
.mock-appbar .brand-txt{font:600 17px var(--serif);line-height:1.1;display:flex;flex-direction:column}
.mock-appbar .brand-wm svg{height:24px;width:auto;display:block}
.tagline{font:600 7.5px var(--sans);letter-spacing:.22em;color:var(--gold)}
.mock-appbar nav{margin-inline-start:auto;display:flex;gap:12px;font:600 11px var(--sans);color:var(--soft);white-space:nowrap}
.mock-appbar nav .on{border-bottom:2px solid var(--gold)}
.mock-tab{display:flex;align-items:center;gap:7px;background:var(--sunken);border:1px solid var(--line2);border-bottom:none;border-radius:9px 9px 0 0;padding:7px 12px;width:max-content}
.f16 svg{width:16px;height:16px;display:block}
.tabtxt{font:12px var(--sans);color:var(--soft)}
.ios-wrap{display:flex;flex-direction:column;align-items:center;gap:5px;width:max-content}
.ios svg{width:58px;height:58px;border-radius:13px;display:block;box-shadow:0 2px 6px rgba(32,50,90,.25)}
.ioslbl{font:11px var(--sans);color:var(--soft)}
.mask-wrap{width:58px;height:58px;border-radius:50%;overflow:hidden;border:1px dashed var(--line2);display:grid;place-items:center;background:#fff}
.maskable svg{width:74px;height:74px;display:block}
.mock-print{background:#fff;border:1px solid var(--line2);border-radius:6px;padding:14px;display:flex;flex-direction:column;gap:6px;align-items:center;text-align:center}
.pr-logo svg{width:34px;height:34px}
.pr-title{font:600 12.5px var(--serif)}
.pr-rule{width:70%;height:1px;background:var(--gold)}
/* ---------------- photo section ---------------- */
.duo-toggle{display:flex;gap:8px;margin:10px 0}
.duo-toggle button{font:600 12.5px var(--sans);border:1px solid var(--line2);background:var(--surface);border-radius:7px;padding:8px 14px;cursor:pointer;min-height:40px}
.duo-toggle button.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.mock-course{border:1px solid var(--line2);border-radius:12px;overflow:hidden;background:var(--surface);margin:12px 0}
.mock-course .imgband{position:relative;aspect-ratio:1600/560;overflow:hidden}
.mock-course .imgband img{width:100%;height:100%;object-fit:cover;display:block}
.mock-course .imgband::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(253,252,251,0) 40%,rgba(253,252,251,.94) 96%)}
.mock-course .head{padding:6px 22px 18px;margin-top:-52px;position:relative;z-index:2}
.mock-course .k{font:600 10.5px var(--sans);letter-spacing:.16em;color:var(--gold);text-transform:uppercase}
.mock-course h4{font:600 24px var(--serif);margin:4px 0 2px}
.mock-course .cap,.figcap{font-size:11.5px;color:var(--muted);font-style:italic;padding:6px 22px 12px;margin:0}
.mock-band{position:relative;border-radius:12px;overflow:hidden;margin:12px 0}
.mock-band img{width:100%;aspect-ratio:1920/480;object-fit:cover;display:block}
.mock-band .ov{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 34px;background:linear-gradient(90deg,rgba(20,41,75,.78) 0%,rgba(20,41,75,.25) 55%,rgba(20,41,75,0) 80%)}
.mock-band .ov .k{font:600 10.5px var(--sans);letter-spacing:.2em;color:var(--gold)}
.mock-band .ov h4{font:600 26px var(--serif);color:#fff;margin:4px 0}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
footer{margin-top:44px;border-top:1px solid var(--line2);padding-top:16px;font-size:13px;color:var(--muted)}
.reply{background:var(--sunken);border:1px solid var(--line2);border-radius:8px;padding:14px 16px;font:13px ui-monospace,monospace;white-space:pre-wrap}
</style>
<div class="wrap">
<header class="masthead">
  <div class="kicker">MechEd · design session · 2026-07-31 · private review</div>
  <h1>Three decisions, side by side: motion, the mark, and photography</h1>
  <p>Everything below is built from the real site — real chrome, real MTH 101 content, the fixed Gallery palette.
  Nothing ships until you choose. Real screen-recordings of the cross-page transitions are attached in the chat;
  the simulator here reproduces their exact timing and easing.</p>
</header>
<div class="tabs" role="tablist">
  <button class="on" data-pane="motion">1 · Motion</button>
  <button data-pane="logo">2 · Logo</button>
  <button data-pane="photo">3 · Photography</button>
</div>

<section class="pane on" id="pane-motion">
  <h2>Motion &amp; transitions</h2>
  <p class="lede">All three treatments are CSS-only progressive enhancement on the View Transitions layer the site
  already ships. Zero JavaScript added by any of them. Firefox (no cross-document support yet) keeps today's instant
  navigation; under “reduce motion” every one of them switches off entirely.</p>
  <div class="twrap"><table>
    <thead><tr><th></th><th>A · Quiet Crossfade</th><th>B · Held Chrome, Threaded Titles</th><th>C · Paper Lay-down</th></tr></thead>
    <tbody>
      <tr><td><b>Page → page</b></td><td>Whole page cross-fades, 0.14s out / 0.22s in. Nothing is held.</td>
        <td>App bar and lesson sidebar hold perfectly still; content cross-fades beneath them.</td>
        <td>Old page lifts away in 0.12s; the new page settles down 14&nbsp;px like a fresh sheet laid on the desk, 0.3s.</td></tr>
      <tr><td><b>Course → lesson</b></td><td>Same quiet fade everywhere.</td>
        <td><b>The title you clicked travels</b> — the syllabus row floats into the lesson’s own heading; course cards thread into the course page the same way.</td>
        <td>Same lay-down gesture everywhere; direction never varies.</td></tr>
      <tr><td><b>Reduced motion</b></td><td colspan="3">Identical for all three: the site’s existing switch turns navigation transitions off completely; tab fades become instant. No layout is left broken.</td></tr>
      <tr><td><b>JS cost</b></td><td colspan="3">0&nbsp;KB — pure CSS (plus one declarative prefetch rule that makes the next page load before it is clicked). B adds ~40 bytes of build-stamped markup per syllabus row.</td></tr>
      <tr><td><b>Phone feel</b></td><td>Softens the page-load blink; otherwise invisible.</td>
        <td>Strongest on the phone — the held header removes the “everything vanished” jolt; the travelling title tells you where you landed.</td>
        <td>Reads as a gentle page-turn; the most “printed notes” of the three.</td></tr>
      <tr><td><b>In-course tabs</b></td><td colspan="3">All three add the same quiet entry fade to Syllabus / Reference / Tools panels (they currently snap). C adds a 6&nbsp;px rise.</td></tr>
    </tbody>
  </table></div>

  <h3>Try them — live simulator</h3>
  <div class="simbar" id="tsel">
    <label class="on"><input type="radio" name="t" value="a" checked> A · Quiet Crossfade</label>
    <label><input type="radio" name="t" value="b"> B · Held Chrome, Threaded Titles</label>
    <label><input type="radio" name="t" value="c"> C · Paper Lay-down</label>
  </div>
  <p id="simcap"></p>
  <div id="simframe">
    <div class="sim-appbar" id="simbarrow"><span class="sl">__C1SVG__</span><span class="sb">MechEd</span>
      <span class="sn"><span>Curriculum</span><span>Resources</span></span></div>
    <div id="simpage"></div>
  </div>
  <p class="note" id="vtnote" hidden>This browser doesn’t support the View Transitions API — the simulator is
  navigating instantly, exactly what unsupported browsers get on the real site.</p>

  <h3>The real thing, recorded</h3>
  <p class="lede">Five recordings are attached in the chat: each treatment’s full journey
  (curriculum → course → tabs → lesson 02 → lesson 03) slowed 8× so the mechanics are visible, plus treatment B at
  real speed and on a phone-width viewport. The trees themselves are browsable on the Mac under
  <code>design-previews/motion-a|b|c/</code>.</p>
  <div class="stills">
    <figure><img src="__DESKCURR__" alt="Curriculum page, real build"><figcaption>Real build — curriculum (treatment trees use the live Gallery chrome)</figcaption></figure>
    <figure><img src="__DESKCOURSE__" alt="Course page, real build"><figcaption>Real build — MTH 101 course page</figcaption></figure>
    <figure><img src="__DESKL02__" alt="Lesson page, real build"><figcaption>Real build — Lesson 02 with video hero</figcaption></figure>
  </div>
  <div class="rate"><b>To rate:</b> reply with the letter — e.g. “Motion: B” — plus anything to tune
  (speed, how far the title travels, whether tabs should move at all).</div>
</section>

<section class="pane" id="pane-logo">
  <h2>The mark</h2>
  <p class="lede">Six candidates, all flat vector, all drawn only from colours already in the system, no text
  elements (every letter is an outlined path — nothing depends on a font being installed). C1 is the mark you have
  today, kept in the running as the control.</p>
  <div class="cands">__CARDS__</div>

  <h3>Every candidate, everywhere it has to survive</h3>
  __INSITU__

  <h3>Recommendation</h3>
  <div class="card"><p><b>First choice: C3 — the wordmark lockup, with C2 as its icon.</b> Every serious institution
  on the reference board — MIT, Imperial, Cambridge, IMechE, the university presses — leads with a wordmark; devices
  are held in reserve. C3 is the only candidate that carries the Arabic descriptor <em>inside</em> the identity
  (the itqan pattern you named), it is cut from the site’s own Source Serif so the brand and the page are one voice,
  and its licence position is clean: OFL-outlined artwork is fully yours, no obligations. C2 gives it a
  pixel-perfect square form for favicons and app icons that C1’s hand-drawn M never quite was.</p>
  <p><b>Second choice: C1 — keep the incumbent.</b> It is already good: legible at 16&nbsp;px, honest, in production.
  If nothing here clearly beats it for you, keeping it is a respectable decision, and the money conversation goes away.</p>
  <p><b>A decision either way:</b> the incumbent’s gold is <code>#C9A45C</code> while the site token is
  <code>#CBA85F</code> — two golds one step apart. Whichever mark wins, pick one gold and let the other die.</p></div>

  <h3>Reference board (all fetched and verified live, 2026-07-31)</h3>
  <div class="grid2">
    <div class="card"><b>Reads “official institution”</b><br>
    <a href="https://www.imeche.org" target="_blank" rel="noopener">IMechE</a> — the name is the mark; nothing to degrade.<br>
    <a href="https://ethz.ch/en.html" target="_blank" rel="noopener">ETH Zurich</a> — acronym wordmark, rigour from typesetting alone.<br>
    <a href="https://www.mit.edu" target="_blank" rel="noopener">MIT</a> — lettermark of plain bars; survives one-colour, tiny, engraved.<br>
    <a href="https://www.imperial.ac.uk" target="_blank" rel="noopener">Imperial College</a> — no crest; type-only reads more elite, not less.<br>
    <a href="https://www.asme.org" target="_blank" rel="noopener">ASME</a> — acronym + spelled-out name, the engineering dual register.<br>
    <a href="https://www.cam.ac.uk" target="_blank" rel="noopener">Cambridge</a> — even they lead digital with a shield-free wordmark.<br>
    <a href="https://www.kfupm.edu.sa" target="_blank" rel="noopener">KFUPM</a> — Gulf technical university, per-language logo variants.<br>
    <a href="https://www.theiet.org" target="_blank" rel="noopener">IET</a> — compact mark, chartered gravitas in the lockup.</div>
    <div class="card"><b>Reads “quietly elegant”</b><br>
    <a href="https://royalsociety.org" target="_blank" rel="noopener">The Royal Society</a> — 360 years carried by typography; crest in reserve.<br>
    <a href="https://press.princeton.edu" target="_blank" rel="noopener">Princeton University Press</a> — no device at all; confidence by absence.<br>
    <a href="https://yalebooks.yale.edu" target="_blank" rel="noopener">Yale University Press</a> — the institution’s own typeface is the brand.<br>
    <a href="https://www.rigb.org" target="_blank" rel="noopener">Royal Institution</a> — two letters, two centuries.<br>
    <a href="https://www.qnl.qa/en" target="_blank" rel="noopener">Qatar National Library</a> — the regional model: one thin device + Arabic-over-English stack, single colour.<br>
    <a href="https://www.bodleian.ox.ac.uk" target="_blank" rel="noopener">Bodleian Libraries</a> — wordmark first, heritage second.</div>
  </div>

  <h3>Where to get it — honestly</h3>
  <div class="card" style="font-size:14.5px">
  <p><b>Set it in the faces you already use (what C2/C3 are)</b> — Source Serif 4 and Source Sans 3 are SIL OFL 1.1
  (verified from the licence texts in Adobe’s repositories): commercial use and modified letterforms expressly
  permitted, and outlined logo artwork carries <em>no licence obligation at all</em>. Free, immediate, fully owned,
  consistent with the site by construction. For a minimal educational mark this is a first-class route, not a fallback.</p>
  <p><b>Author it as SVG</b> (what C4–C6 are) — this repo already computes SVG programmatically; costs only time.</p>
  <p><b>Commission a designer</b> — marketplace one-offs roughly $50–500 (quality lottery, check exclusivity in
  writing); an independent identity designer roughly $1–5k for a small system; a studio $10k+. What you are buying
  is <em>exclusive rights and a system</em>, and the rights clause is the part most often got wrong — insist on full
  assignment, not a licence.</p>
  <p><b>Stock/template marks</b> — non-exclusive: someone else can run the same mark. Unacceptable for an institution.</p>
  <p><b>AI-generated marks</b> — sketching aid only; anything shipped must be redrawn as controlled vector, and
  ownership of raw generated output is not settled enough to build an institution on.</p>
  <p><b>Whichever route:</b> Kuwait MOCI trademark clearance has never been done. Do it before the mark is
  everywhere — a forced rebrand after launch is the expensive version.</p></div>
  <div class="rate"><b>To rate:</b> reply like “Logo: C3, second C1” — or name a direction to push further
  (heavier M, no gold dot, tighter lockup…). Switching the deployed mark is a one-file swap plus regenerating the
  PNG icon set; I’ll handle the full cascade (manifest, service worker, favicons, print) when you choose.</div>
</section>

<section class="pane" id="pane-photo">
  <h2>Photography — a proposal, not a fait accompli</h2>
  <p class="lede">You asked whether photos belong. My honest answer: <b>yes in three bounded places, no everywhere
  else.</b> Course headers (one image, behind the title), semester dividers on the curriculum page, and at most one
  homepage band. Not inside lessons — the computed diagrams are the product there and photography would dilute them.</p>
  <p class="note"><b>The tension you should rule on:</b> “no new colours” and “add photography” pull against each
  other — every photograph imports its own palette. Below, each placement is shown twice: <b>full colour</b>
  (honest, livelier, but each image brings foreign colour onto the page) and <b>navy duotone</b> (every image
  remapped into the site’s own navy-to-paper ramp — zero new colour, printed-notes register, and 20–45% lighter
  files). I recommend duotone for headers and dividers; if colour is used anywhere, only in the bounded homepage band.</p>
  <div class="duo-toggle" id="duosel"><button class="on" data-m="duo">Navy duotone</button><button data-m="full">Full colour</button></div>

  <h3>Course header</h3>
  <div class="grid2">
    <div class="mock-course"><div class="imgband"><img class="ph" data-slot="machining" src="__MACH_DUO__" alt=""></div>
      <div class="head"><div class="k">MFG 154 · Year 2 · Semester 1</div><h4>Manufacturing Processes II</h4></div>
      <p class="cap">__CAP_MACH__ · photo: D.&nbsp;Rabich, CC&nbsp;BY-SA&nbsp;4.0</p></div>
    <div class="mock-course"><div class="imgband"><img class="ph" data-slot="mechanisms" src="__MECH_DUO__" alt=""></div>
      <div class="head"><div class="k">KIN 252 · Year 2 · Semester 2</div><h4>Kinematics &amp; Dynamics of Machinery</h4></div>
      <p class="cap">__CAP_MECH__ · photo: D.&nbsp;Rabich, CC&nbsp;BY-SA&nbsp;4.0</p></div>
    <div class="mock-course"><div class="imgband"><img class="ph" data-slot="thermal" src="__THER_DUO__" alt=""></div>
      <div class="head"><div class="k">THM 202 · Year 2 · Semester 2</div><h4>Thermodynamics II — Cycles &amp; Utilities</h4></div>
      <p class="cap">__CAP_THER__ · photo: Siemens Pressebild, CC&nbsp;BY-SA&nbsp;3.0</p></div>
    <div class="mock-course"><div class="imgband"><img class="ph" data-slot="metrology" src="__METR_DUO__" alt=""></div>
      <div class="head"><div class="k">MET 204 · Year 2 · Semester 2</div><h4>Metrology &amp; Quality Control</h4></div>
      <p class="cap">__CAP_METR__ · photo: U.S. Air Force / E.&nbsp;Dunkleberger, public domain</p></div>
  </div>

  <h3>Semester divider (curriculum page)</h3>
  <div class="mock-band"><img class="ph" data-slot="divider" src="__DIV_DUO__" alt="">
    <div class="ov"><div class="k">Year 2 · Semester 2</div><h4>Six courses. The machines get real.</h4></div></div>
  <p class="figcap">__CAP_DIV__ · photo: Siemens Pressebild, CC&nbsp;BY-SA&nbsp;3.0. Dark pixels stay inside the bounded band — the page around it never dims.</p>

  <h3>Homepage band</h3>
  <div class="mock-band"><img class="ph" data-slot="band" src="__BAND_DUO__" alt="">
    <div class="ov"><div class="k">The archive register</div><h4>Engineering, taught like it’s printed.</h4></div></div>
  <p class="figcap">__CAP_BAND__ · Historic American Buildings Survey, public domain.</p>

  <h3>What it costs the page</h3>
  <p class="lede">Measured from the real files above (WebP quality 68 / JPEG quality 72, sizes as delivered with
  <code>srcset</code>; every image gets an explicit <code>aspect-ratio</code> so nothing shifts on load, and
  <code>loading="lazy"</code> below the fold).</p>
  <div class="twrap"><table>
    <thead><tr><th>Image</th><th>Use</th><th>Pixels</th><th>Desktop KB webp <span class="dim">/ jpg</span></th><th>Mobile (800w) KB</th><th>Duotone KB</th></tr></thead>
    <tbody>__WROWS__</tbody>
  </table></div>
  <div class="card" style="font-size:14.5px">
  <b>Budget maths.</b> A course page today is ~60–90&nbsp;KB before video posters. One duotone header adds
  ~__AVGD__&nbsp;KB on desktop, ~30&nbsp;KB on phones — roughly a 2× page-weight step, still under a quarter of a
  single YouTube poster frame. Sitewide: 48 course headers ≈ 3.5–4.5&nbsp;MB of new static assets. For the installed
  app, that must <b>not</b> go in the service-worker precache (which currently holds 5 files); headers should cache
  on visit like pages do. Dividers ≈ 8 images sitewide; the homepage band is one. Lessons: zero — 1,262 lesson/other
  pages stay imageless, which is why the sitewide bill stays in single-digit megabytes.</div>

  <h3>Sources &amp; honest captions</h3>
  <div class="twrap"><table>
    <thead><tr><th>Slot</th><th>Commons file (licence page)</th><th>Licence</th><th>Credit</th><th>Caption as it would ship</th></tr></thead>
    <tbody>__LICROWS__</tbody>
  </table></div>
  <p class="note">CC&nbsp;BY-SA images require visible credit (shown in the mock captions) and the duotone remap is
  an adaptation, which BY-SA permits with share-alike on the adapted image — fine for a public site, stated here so
  it’s chosen, not stumbled into. The two public-domain items carry no obligation; credits shown anyway. If you’d
  rather commission real Kuwait-facility photography later, these slots are exactly where it would go — with real
  captions replacing “representative example”.</p>
  <div class="rate"><b>To rate:</b> e.g. “Photos: yes — duotone, headers + dividers only, no homepage band” or
  “Photos: no — keep the site vector-only”. Both are good answers; the site works without photography.</div>
</section>

<footer>
  <p><b>How to reply, all in one line if you like:</b></p>
  <div class="reply">Motion: A / B / C (+ tuning notes)
Logo: first + second choice (+ direction notes)
Photos: yes-duotone / yes-colour / no (+ which placements)</div>
  <p>Standing rules honoured throughout: colours untouched, backgrounds bright, no remote git operations, nothing
  applied site-wide. Built by the design session, 2026-07-31.</p>
</footer>
</div>
<script>
(function(){
  var tabs=document.querySelectorAll('.tabs button');
  tabs.forEach(function(b){b.addEventListener('click',function(){
    tabs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');
    document.querySelectorAll('.pane').forEach(function(p){p.classList.remove('on')});
    document.getElementById('pane-'+b.dataset.pane).classList.add('on');
    try{history.replaceState(null,'','#'+b.dataset.pane)}catch(e){}
  })});
  var h=location.hash.replace('#','');
  if(h){var b=document.querySelector('.tabs button[data-pane="'+h+'"]');if(b)b.click();}

  /* ---- simulator ---- */
  var T={
    a:{old:'.14s',neu:'.22s',hold:false,morph:false,lift:false,
       cap:'A — the whole frame cross-fades quietly. Nothing is held, nothing travels. The safest possible upgrade to what already ships.'},
    b:{old:'.14s',neu:'.22s',hold:true,morph:true,lift:false,
       cap:'B — watch the app bar: it never flinches. Click a course or a lesson and its title physically travels into the next page\\u2019s heading.'},
    c:{old:'.12s',neu:'.3s',hold:true,morph:false,lift:true,
       cap:'C — the old sheet lifts away and the new one settles onto the desk. One gesture, every navigation, like turning printed notes.'}
  };
  var cur='a',page='curriculum';
  var sp=document.getElementById('simpage'),bar=document.getElementById('simbarrow'),cap=document.getElementById('simcap');
  var COURSES=[['MTH 101','Engineering Mathematics I','Single-variable calculus rebuilt as a working tool: limits, derivatives, integrals.'],
               ['PHY 107','Engineering Physics I — Mechanics','Newton\\u2019s laws to rigid bodies, taught for machines rather than exams.'],
               ['DRW 102','Engineering Drawing & CAD','The language of drawings: projection, sections, tolerances, CAD practice.']];
  var LESSONS=[['01','Functions, units, and engineering magnitudes'],
               ['02','Limits and continuity'],['03','The derivative as a rate']];
  var L2={ '02':['Limits and continuity','The limit as the formal version of \\u201cwhat happens as we approach\\u201d. Continuity, and why physical quantities are usually — but not always — continuous.'],
           '03':['The derivative as a rate','Definition from first principles, then the derivative as velocity, heat-up rate, and wear rate.']};
  function vt(n){return T[cur].morph? ' style="view-transition-name:'+n+'"':''}
  function render(){
    bar.style.viewTransitionName = T[cur].hold ? 'sim-appbar' : '';
    document.documentElement.classList.toggle('lift', T[cur].lift);
    document.documentElement.style.setProperty('--vt-old',T[cur].old);
    document.documentElement.style.setProperty('--vt-new',T[cur].neu);
    var h='';
    if(page==='curriculum'){
      h='<div class="sim-kick">Curriculum \\u00b7 Year 1 \\u00b7 Semester 1</div>'+
        '<div class="sim-h1"'+vt('t-course')+ (0?'':'')+'>48 courses. 528 lessons.</div>'+
        '<p class="sim-sub">Tap a course \\u2014 this is the journey a learner takes a hundred times.</p>'+
        COURSES.map(function(c,i){return '<div class="sim-card" data-go="course"><span class="cc">'+c[0]+'</span>'+
          '<div class="ct"'+(i===0?vt('t-c0'):'')+'>'+c[1]+'</div><p>'+c[2]+'</p></div>'}).join('');
    } else if(page==='course'){
      h='<div class="sim-crumb"><a data-go="curriculum">Curriculum</a> / MTH 101</div>'+
        '<div class="sim-kick">MTH 101 \\u00b7 Year 1 \\u00b7 Semester 1</div>'+
        '<div class="sim-h1"'+vt('t-c0')+'>Engineering Mathematics I</div>'+
        '<p class="sim-sub">Single-variable calculus rebuilt as a working tool \\u2014 11 lessons, all at full depth.</p>'+
        '<div class="sim-tabs"><span class="on">Syllabus</span><span>Reference</span><span>Tools & Software</span></div>'+
        LESSONS.map(function(l){return '<div class="sim-row" data-go="l'+l[0]+'"><span class="no">'+l[0]+'</span>'+
          '<span class="rt"'+(l[0]!=='01'?vt('t-l'+l[0]):'')+'>'+l[1]+'</span></div>'}).join('');
    } else {
      var n=page.slice(1),d=L2[n]||L2['02'];
      h='<div class="sim-crumb"><a data-go="curriculum">Curriculum</a> / <a data-go="course">MTH 101</a> / Lesson '+n+'</div>'+
        '<div class="sim-kick">MTH 101 \\u00b7 Lesson '+n+' of 11</div>'+
        '<div class="sim-h1"'+vt('t-l'+n)+'>'+d[0]+'</div>'+
        '<p class="sim-sub">'+d[1]+'</p>'+
        '<div class="sim-video">Lecture video \\u00b7 MIT OCW 18.01</div>'+
        '<div class="sim-nav">'+(n==='03'?'<a data-go="l02">\\u2190 02 \\u00b7 Limits and continuity</a>':'<a data-go="course">\\u2190 All lessons</a>')+
        (n==='02'?'<a data-go="l03">03 \\u00b7 The derivative as a rate \\u2192</a>':'<a data-go="course">All lessons \\u00b7 MTH 101</a>')+'</div>';
    }
    sp.innerHTML='<div style="view-transition-name:sim-page">'+h+'</div>';
    cap.textContent=T[cur].cap.replace('\\\\u2019','\\u2019');
  }
  sp.addEventListener('click',function(e){
    var t=e.target.closest('[data-go]');if(!t)return;
    var go=t.getAttribute('data-go');
    var reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(document.startViewTransition&&!reduced){page=go;document.startViewTransition(render);}
    else{page=go;render();document.getElementById('vtnote').hidden=!!document.startViewTransition;}
  });
  document.getElementById('tsel').addEventListener('change',function(e){
    cur=e.target.value;
    document.querySelectorAll('#tsel label').forEach(function(l){l.classList.toggle('on',l.querySelector('input').value===cur)});
    render();
  });
  if(!document.startViewTransition)document.getElementById('vtnote').hidden=false;
  render();
  cap.textContent=T[cur].cap;

  /* ---- photo duotone toggle ---- */
  var SRC=__PHOTOSRC__;
  document.getElementById('duosel').addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;
    document.querySelectorAll('#duosel button').forEach(function(x){x.classList.toggle('on',x===b)});
    var m=b.dataset.m;
    document.querySelectorAll('img.ph').forEach(function(im){im.src=SRC[im.dataset.slot][m]});
  });
})();
</script>
"""

PH = {
    "machining": {"duo": photo("machining-prevduo"), "full": photo("machining-prev")},
    "mechanisms": {"duo": photo("mechanisms-prevduo"), "full": photo("mechanisms-prev")},
    "thermal": {"duo": photo("thermal-prevduo"), "full": photo("thermal-prev")},
    "metrology": {"duo": photo("metrology-prevduo"), "full": photo("metrology-prev")},
    "divider": {"duo": photo("divider-prevduo"), "full": photo("divider-prev")},
    "band": {"duo": photo("band-prevduo"), "full": photo("band-prev")},
}

subs = {
    "__SERIF600__": F["serif600"], "__SERIF400__": F["serif400"],
    "__SANS400__": F["sans400"], "__SANS600__": F["sans600"],
    "__C1SVG__": svg("c1-incumbent.svg"),
    "__CARDS__": "\n".join(CARDS), "__INSITU__": "\n".join(INSITU),
    "__WROWS__": "\n".join(WROWS), "__LICROWS__": "\n".join(LIC_ROWS),
    "__AVGD__": str(sum(r["duoWebpKB"] for r in WEIGHTS[:4]) // 4),
    "__DESKCURR__": "data:image/jpeg;base64," + IMG["desk-curriculum"],
    "__DESKCOURSE__": "data:image/jpeg;base64," + IMG["desk-course"],
    "__DESKL02__": "data:image/jpeg;base64," + IMG["desk-lesson02"],
    "__MACH_DUO__": PH["machining"]["duo"], "__MECH_DUO__": PH["mechanisms"]["duo"],
    "__THER_DUO__": PH["thermal"]["duo"], "__METR_DUO__": PH["metrology"]["duo"],
    "__DIV_DUO__": PH["divider"]["duo"], "__BAND_DUO__": PH["band"]["duo"],
    "__CAP_MACH__": CAPTIONS["machining"], "__CAP_MECH__": CAPTIONS["mechanisms"],
    "__CAP_THER__": CAPTIONS["thermal"], "__CAP_METR__": CAPTIONS["metrology"],
    "__CAP_DIV__": CAPTIONS["divider"], "__CAP_BAND__": CAPTIONS["band"],
    "__PHOTOSRC__": json.dumps(PH),
}
for k, v in subs.items():
    html = html.replace(k, v)

out = SP / "gallery.html"
out.write_text(html)
print("gallery.html", out.stat().st_size // 1024, "KB")
