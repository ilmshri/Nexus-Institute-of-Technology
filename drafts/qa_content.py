#!/usr/bin/env python3
"""Pre-build content gates for MechEd lesson JSONs.

Run from the repo root:  python3 qa_content.py [content-json ...]
With no args it scans every data/content/*.json.

Gates (each has caught a real defect in this project):
  1. SVG <text> overflow past the 560-unit viewBox
  2. Same-row <text> collisions inside a <figure>
  3. Mid-word hyphen line-wraps ([a-z]-\\n) in hand-written HTML
  4. LaTeX delimiter balance  \\( \\)  and  \\[ \\]
  5. Company names in academic content (career blocks are exempt — they
     live in data/y*.json, not here, so any hit in data/content is a defect)
  6. Structural contract: 3 solve + 8 mc, 4 choices, integer answer in range
"""
import json
import re
import sys
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))  # drafts/ttfwidth.py
from ttfwidth import metrics          # real SF NS advance widths, not a guess
from svggeom import shapes_in, text_hits_shape, text_box
import qa_sequence                   # curriculum-sequencing gates (a)-(d)

VIEWBOX_W = 560

COMPANIES = [
    "KNPC", "KOC", "KIPIC", "EQUATE", "KDD", "Petra", "HEISCO", "Kirby",
    "Kuwait Steel", "Gulf Cable", "Gulf Glass", "Mabanee", "Bechtel",
    "Siemens", "ABB", "Schneider", "Caterpillar", "Cummins",
    "Toyota", "Boeing", "Airbus", "Alfa Laval", "Danfoss",
    "Vertiv", "Mitsubishi", "Atlas Copco", "Sandvik",
    "Lincoln Electric", "Stratasys", "Omron", "Texas Instruments",
    "Analog Devices", "SKF", "Nord-Lock", "Lesjofors",
    "Timken", "Bosch", "Parker Hannifin", "Emerson", "Honeywell",
]
# Deliberately NOT checked here: Shell, Rockwell, Thomson, GE. Each is ordinary
# engineering vocabulary ("shell-and-tube", "shell growth" in casting, Thomson
# for Kelvin) and every occurrence found in data/content was the technical
# sense, never the company. Company names legitimately live only in the career
# blocks in data/y*.json, which this scanner does not cover — check those by
# hand when writing one.
# "Carrier" is ordinary machinery vocabulary — the planet carrier of an
# epicyclic train (KDM 252 L6 uses it in almost every sentence), the carrier
# gas of a process, the charge carriers of a semiconductor. Matching the bare
# word produced a false positive per lesson, so it is checked only in a form
# that can only be the company.
AMBIGUOUS = {
    "Carrier": r"\bCarrier\s+(Corporation|Corp\.?|Global|Air Conditioning)\b",
}


def texts_in_figures(html):
    """Yield (figure_index, viewbox_w, x, y, anchor, size, weight, content)."""
    for fi, fig in enumerate(re.findall(r"<figure.*?</figure>", html, re.S)):
        vb = re.search(r'viewBox="([^"]+)"', fig)
        vbw = float(vb.group(1).split()[2]) if vb else float(VIEWBOX_W)
        for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", fig, re.S):
            attrs, body = m.group(1), m.group(2)

            def a(name, default=None):
                mm = re.search(rf'{name}="([^"]*)"', attrs)
                return mm.group(1) if mm else default

            # Rotated labels sit on the axis, not the row grid — skip them.
            if a("transform"):
                continue
            try:
                x = float(a("x", "0"))
                y = float(a("y", "0"))
            except ValueError:
                continue
            size = float(a("font-size", "12"))
            anchor = a("text-anchor", "start")
            weight = a("font-weight", "400")
            tfill = a("fill")
            # Entities must be decoded before measuring: "&#956; = 46.4&#176;"
            # is nine rendered glyphs, not eighteen. Measuring the raw source
            # made every entity-bearing label read ~2.3x too wide.
            content = unescape(re.sub(r"<[^>]+>", "", body))
            yield fi, vbw, x, y, anchor, size, weight, content, tfill


def span(x, anchor, size, weight, content):
    w = metrics().width(content, size, weight)
    if anchor == "middle":
        return x - w / 2, x + w / 2
    if anchor == "end":
        return x - w, x
    return x, x + w


def gate_svg(name, lid, field, html, issues):
    rows = list(texts_in_figures(html))
    for fi, vbw, x, y, anchor, size, weight, content, _tf in rows:
        x0, x1 = span(x, anchor, size, weight, content)
        if x1 > vbw or x0 < 0:
            issues.append(
                f"{name} L{lid} {field}: SVG overflow fig{fi} "
                f"[{x0:.0f},{x1:.0f}] outside 0..{vbw:.0f} — {content!r}")
    # labels colliding with the DRAWING (owner 2026-07-30: "components overlap").
    # Text-vs-text alone missed this class entirely.
    for fi, fig in enumerate(re.findall(r"<figure.*?</figure>", html, re.S)):
        shapes = list(shapes_in(fig))
        for r in rows:
            if r[0] != fi:
                continue
            _, _, x, y, anchor, size, weight, content, tfill = r
            if not content.strip():
                continue
            tbox = text_box(x, y, anchor, size, weight, content)
            for sh in shapes:
                if text_hits_shape(tbox, sh, tfill):
                    issues.append(
                        f"{name} L{lid} {field}: label over {sh['kind']} "
                        f"<{sh['name']}> fig{fi} — {content!r}")
                    break

    # collisions: same figure, y within 6 units, x-ranges overlap
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            fi, _, xi, yi, ai, si, wi, ci, _a = rows[i]
            fj, _, xj, yj, aj, sj, wj, cj, _b = rows[j]
            if fi != fj:
                continue
            bi = text_box(xi, yi, ai, si, wi, ci)
            bj = text_box(xj, yj, aj, sj, wj, cj)
            if not (bi[0] < bj[2] and bj[0] < bi[2]
                    and bi[1] < bj[3] and bj[1] < bi[3]):
                continue
            i0, i1, j0, j1 = bi[0], bi[2], bj[0], bj[2]
            if True:
                issues.append(
                    f"{name} L{lid} {field}: SVG collision fig{fi} y≈{yi:.0f} "
                    f"— {ci!r} [{i0:.0f},{i1:.0f}] vs {cj!r} [{j0:.0f},{j1:.0f}]")


def gate_text(name, lid, field, html, issues):
    for m in re.finditer(r"[a-z]-\n[a-z]", html):
        issues.append(f"{name} L{lid} {field}: mid-word hyphen wrap "
                      f"{html[max(0,m.start()-25):m.end()+15]!r}")
    if html.count(r"\(") != html.count(r"\)"):
        issues.append(f"{name} L{lid} {field}: unbalanced \\( \\) "
                      f"({html.count(chr(92)+'(')} vs {html.count(chr(92)+')')})")
    if html.count(r"\[") != html.count(r"\]"):
        issues.append(f"{name} L{lid} {field}: unbalanced \\[ \\]")
    # A doubled backslash reaches the browser as a literal "\\(" and MathJax
    # leaves the whole expression as raw text. Caused by an r"..." literal in
    # an authoring script that also escaped the delimiter.
    for tok in (r"\\(", r"\\)", r"\\[", r"\\]"):
        if tok in html:
            i = html.index(tok)
            issues.append(f"{name} L{lid} {field}: double-escaped math "
                          f"delimiter {tok!r} — {html[max(0,i-40):i+25]!r}")
            break
    for c in COMPANIES:
        if re.search(rf"\b{re.escape(c)}\b", html):
            issues.append(f"{name} L{lid} {field}: company name {c!r} "
                          f"in academic content")
    for c, pat in AMBIGUOUS.items():
        if re.search(pat, html):
            issues.append(f"{name} L{lid} {field}: company name {c!r} "
                          f"in academic content")


def gate_quiz(name, lid, quiz, issues):
    solve = [q for q in quiz if q.get("type") == "solve"]
    mc = [q for q in quiz if q.get("type") == "mc"]
    if len(solve) != 3 or len(mc) != 8:
        issues.append(f"{name} L{lid} quiz: {len(solve)} solve + {len(mc)} mc "
                      f"(want 3 + 8)")
    for k, q in enumerate(mc):
        ch = q.get("choices", [])
        if len(ch) != 4:
            issues.append(f"{name} L{lid} mc[{k}]: {len(ch)} choices, want 4")
        ans = q.get("answer")
        if not isinstance(ans, int) or isinstance(ans, bool):
            issues.append(f"{name} L{lid} mc[{k}]: answer {ans!r} not an int")
        elif not 0 <= ans < len(ch):
            issues.append(f"{name} L{lid} mc[{k}]: answer {ans} out of range")


def main(argv):
    # Naming files explicitly means "I authored these" — the 3+8 quiz contract
    # is enforced. A bare sweep only reports it, because several early courses
    # legitimately predate that contract and are not being retrofitted here.
    explicit = [Path(p) for p in argv[1:]]
    files = explicit or sorted(Path("data/content").glob("*.json"))
    strict_quiz = bool(explicit)
    shapes = {}
    issues = []
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        name = f.stem
        for lid, les in data.items():
            if not isinstance(les, dict):
                continue
            for field in ("lecture", "foundations", "kuwait", "recap"):
                html = les.get(field)
                if not isinstance(html, str):
                    continue
                gate_text(name, lid, field, html, issues)
                if field == "lecture":
                    gate_svg(name, lid, field, html, issues)
            quiz = les.get("quiz")
            # Quiz strings were outside every text gate until 2026-07-31, which
            # is exactly where a double-escaped delimiter survived a clean scan.
            if isinstance(quiz, list):
                for qi, q in enumerate(quiz):
                    if not isinstance(q, dict):
                        continue
                    for key in ("q", "solution"):
                        if isinstance(q.get(key), str):
                            gate_text(name, lid, f"quiz[{qi}].{key}",
                                      q[key], issues)
                    for ci, ch in enumerate(q.get("choices", []) or []):
                        if isinstance(ch, str):
                            gate_text(name, lid, f"quiz[{qi}].choices[{ci}]",
                                      ch, issues)
            if isinstance(quiz, list):
                if strict_quiz:
                    gate_quiz(name, lid, quiz, issues)
                else:
                    shape = (sum(1 for q in quiz if q.get("type") == "solve"),
                             sum(1 for q in quiz if q.get("type") == "mc"))
                    shapes.setdefault(name, {}).setdefault(shape, []).append(lid)
                    # choice/answer integrity is enforced everywhere
                    bad = []
                    gate_quiz(name, lid,
                              [q for q in quiz if q.get("type") == "mc"] + [
                                  {"type": "solve"}] * 3, bad)
                    issues.extend(b for b in bad if "want 3 + 8" not in b)
                for k, q in enumerate(quiz):
                    for field in ("q", "solution"):
                        if isinstance(q.get(field), str):
                            gate_text(name, lid, f"quiz[{k}].{field}",
                                      q[field], issues)
                    for c in q.get("choices", []):
                        gate_text(name, lid, f"quiz[{k}].choice", c, issues)
    for i in issues:
        print("FAIL:", i)
    if shapes:
        off = {n: s for n, s in shapes.items()
               if list(s) != [(3, 8)]}
        if off:
            print("\nINFO — quiz shapes that are not 3 solve + 8 mc "
                  "(legacy format, not retrofitted here):")
            for n, s in sorted(off.items()):
                print(f"  {n}: " + ", ".join(
                    f"{a}+{b} x{len(v)}" for (a, b), v in sorted(s.items())))
    # Curriculum-sequencing gates (owner directive, 2026-07-31). Course-level
    # and cross-file, so they live in qa_sequence.py and are summarised here.
    seq, vstats = qa_sequence.run(Path("."), files)
    counts = {}
    for kind, cid, lid, msg in seq:
        counts[kind] = counts.get(kind, 0) + 1
    if seq:
        print("\nSEQUENCING — run `python3 drafts/qa_sequence.py` for detail:")
        for kind, label in (("a", "declared forward reference"),
                            ("b", "undeclared forward reference"),
                            ("c", "cross-course prerequisite direction"),
                            ("d", "video is a numbered series instalment"),
                            ("d-order", "series numbering vs our lesson order")):
            if counts.get(kind):
                print(f"  ({kind}) {label}: {counts[kind]}")
        print(f"  {vstats['instalments']} of {vstats['embeds']} embeds are "
              f"series instalments")

    print(f"\n{len(files)} file(s) scanned — {len(issues)} issue(s)"
          f"{' (quiz contract enforced)' if strict_quiz else ''}.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
