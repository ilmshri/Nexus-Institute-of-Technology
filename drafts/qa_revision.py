#!/usr/bin/env python3
"""Author-side gates for the per-lesson "revision" blocks.

⚠️ THIS IS NOT THE PAGE-FIT GATE. design-previews/tools/qa_revision_fit.py is,
and it now EXISTS: it renders every block through the real renderer with the
real stylesheet, webfonts and typeset MathJax inside the exact A4 content box
and measures rendered height. Word counts play no part in its verdict. Run it
before every build; this file is the fast pre-check you run while writing.

What this one does that the fit gate cannot:

  1. Schema shape — fields exist and are the right types.
  2. Budget — a prose estimate, RECALIBRATED 2026-08-01 against the fit gate's
     real measurements. It replaced a provisional 320-420 words/page guess.
  3. TERMS FIRST — the owner's rule 1, exact: no symbol may appear in a sheet
     or example unless intro.terms declared it. A renderer cannot check this,
     and neither can a height measurement.

Run from the repo root:  python3 drafts/qa_revision.py [content-json ...]
"""
import json
import re
import sys
from html import unescape
from pathlib import Path

# Vertical cost, in "word equivalents", of things that are not prose. Tuned to
# the house print CSS (reading line-height 1.8, display maths generously
# spaced). Conservative on purpose: over-estimating pushes an author to split a
# block, which is the safe direction.
COST_DISPLAY_EQ = 30
COST_TABLE_ROW = 10
COST_LIST_ITEM = 4
COST_HEADING = 12

# MEASURED CAPACITY — recalibrated 2026-08-02 by drafts/calibrate_revision.py
# after the design session's folio work (02999f1c) shrank the content box from
# 261mm to 252mm (a fixed 260mm sheet less an 8mm folio zone): 986px -> 952px.
#
# TWO THINGS CHANGED, and the second matters more than the box did.
#
# (1) Capacity is now PER BLOCK KIND. The old single PAGE_MEDIAN 330 / PAGE_MIN
#     253 pair could not be right for all four kinds, because this file spends
#     three different cost models and each omits different fixed furniture. An
#     opener costed at 78 word-equivalents really renders 631px, since its model
#     prices neither the lesson-title rule nor the key-point line-height; a
#     sheet costed at 288 renders 751px. Pooling them put the "floor" near 110
#     and would flag every sheet in the document.
# (2) The old numbers were in the WRONG UNIT. They were lifted from
#     qa_revision_fit.py's capacity line, which extrapolates in RAW WORDS, and
#     then used to judge WORD-EQUIVALENTS. On prose the two agree; on an
#     equation-heavy block they do not, so the error was invisible.
#     calibrate_revision.py now extrapolates in word-equivalents — the same
#     unit this file spends.
#
# Measured over MTH 101's 44 blocks (min / median capacity, word-equivalents):
PAGE_CAP = {
    "opener":  (107, 120),
    "terms":   (221, 263),
    "sheet":   (361, 392),
    "example": (262, 291),
}
# Fail above a kind's median — at typical density that cost exactly fills the
# sheet. Warn between its min and median: at the worst density observed it
# would fill the sheet, so only qa_revision_fit.py can rule.

# A FIGURE'S VERTICAL COST, measured directly (2026-08-02) by rendering the
# same sheet with and without a figure at six viewBox heights: the cost is
# linear in viewBox height, 93px of fixed furniture (frame, padding, caption,
# margins) plus 1.05px per viewBox unit. Converted to word-equivalents at the
# sheet's measured 2.43px per word-equivalent:
#
#   COST_FIGURE(H) = (93 + 1.05*H) / 2.43  ~=  38 + 0.43*H
#
# so the house 560x300 diagram costs ~168 word-equivalents and a 560x200 one
# ~124. Worth knowing while authoring: 560x300 renders 409px = 43% of a page.
# That is under the owner's half-page ceiling but leaves a sheet no room for
# prose, which is why a figure earns its own page rather than riding on one.
FIG_FURNITURE_PX = 93.0
FIG_PX_PER_UNIT = 1.05
PX_PER_WORD_EQ = 2.43
HALF_PAGE_PX = 476.0            # 952px content box / 2 — the owner's ceiling

# The renderer emits TWO opening sheets — an opener (what + keypoints) and a
# separate "Terms & signs" sheet — because the original combined intro page
# measured 175% of A4. Each is a page and each is budgeted as one.
MAX_TERMS_PER_SHEET = 11

# The terms sheet is consistently the TIGHTEST block in the document, and a
# row count alone does not predict it — measured at 11 rows it ran 91% of A4
# in MTH 101 L1 and 96% in L4, the difference being how long the meanings and
# symbols are. So cost it from its real text plus a per-row overhead, fitted
# to those four measured sheets (79%, 80%, 91%, 96%).
COST_TERM_ROW = 6

# LaTeX control words that are structure or operators, never a quantity the
# student must have been introduced to.
STRUCTURAL = {
    "frac", "dfrac", "tfrac", "sqrt", "left", "right", "begin", "end", "text",
    "mathrm", "cdot", "cdots", "ldots", "dots", "times", "div", "quad",
    "qquad", "displaystyle", "sum", "prod", "int", "iint", "lim", "to",
    "infty", "approx", "sim", "simeq", "equiv", "propto", "neq", "ne", "le",
    "leq", "ge", "geq", "ll", "gg", "pm", "mp", "cases", "array", "align",
    "aligned", "partial", "d", "dx", "dt", "log", "ln", "exp", "sin", "cos",
    "tan", "sec", "csc", "cot", "arctan", "sinh", "cosh", "matrix", "pmatrix",
    "bmatrix", "vmatrix", "hline", "\\", "over", "big", "Big", "bigg", "Bigg",
    "label", "tag", "operatorname", "mathbf", "mathit", "boldsymbol", "colon",
    "circ", "deg", "prime", "langle", "rangle", "lvert", "rvert", "lVert",
    "rVert", "vert", "mid", "space", ";", ",", "!", "hat", "bar", "tilde",
    "vec", "overline", "underline", "limits", "nolimits", "substack",
    "Rightarrow", "Leftarrow", "rightarrow", "leftarrow", "implies",
    "therefore", "because", "big|", "bigg|",
}


def _text(html):
    """Visible prose only: strip tags, drop maths, decode entities."""
    s = re.sub(r"\\\[.*?\\\]", " ", html, flags=re.S)      # display maths
    s = re.sub(r"\\\(.*?\\\)", " ", s, flags=re.S)          # inline maths
    s = re.sub(r"<[^>]+>", " ", s)
    return unescape(s)


def _words(html):
    return len(_text(html).split())


def figure_heights(html):
    """viewBox heights of every <svg> in the block, in viewBox units."""
    return [float(m) for m in
            re.findall(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+([\d.]+)',
                       html)]


def figure_px(vb_height):
    """Rendered height of one figure, in px, from the measured linear fit."""
    return FIG_FURNITURE_PX + FIG_PX_PER_UNIT * vb_height


def cost(html):
    """Word-equivalent vertical cost of one block."""
    w = _words(html)
    w += COST_DISPLAY_EQ * len(re.findall(r"\\\[", html))
    w += COST_TABLE_ROW * len(re.findall(r"<tr\b", html))
    w += COST_LIST_ITEM * len(re.findall(r"<li\b", html))
    w += COST_HEADING * len(re.findall(r"<h[3-5]\b", html))
    for vb in figure_heights(html):
        w += round(figure_px(vb) / PX_PER_WORD_EQ)
    return w


def symbols_in(html):
    """Symbol-ish tokens used inside maths: control words and bare letters."""
    out = set()
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", html, flags=re.S):
        math = m.group(1) or m.group(2) or ""
        # Unit symbols live inside \mathrm{} / \text{} and are NOT quantities
        # the student must have been introduced to — "kg", "m/s^2" and "W" are
        # units, not variables. Drop those spans before hunting for letters,
        # or every worked example reports its own units as undeclared.
        math = re.sub(r"\\(?:mathrm|text|operatorname)\s*\{[^{}]*\}", " ", math)
        for cw in re.findall(r"\\([A-Za-z]+)", math):
            if cw not in STRUCTURAL:
                out.add("\\" + cw)
        # bare single letters that are not part of a control word
        stripped = re.sub(r"\\[A-Za-z]+", " ", math)
        for ltr in re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", stripped):
            out.add(ltr)
    return out


def check_lesson(name, lid, lesson, issues, lesson_title=None,
                 warnings=None):
    warnings = [] if warnings is None else warnings
    rev = lesson.get("revision")
    if rev is None:
        return False
    tag = f"{name} L{lid}"

    intro = rev.get("intro")
    if not isinstance(intro, dict):
        issues.append(f"{tag}: revision.intro missing or not an object")
        return True
    what = intro.get("what", "")
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", _text(what).strip()) if s]
    if not 2 <= len(sentences) <= 4:
        issues.append(f"{tag}: intro.what has {len(sentences)} sentences, "
                      f"brief says 2-4")
    kp = intro.get("keypoints", [])
    if not 5 <= len(kp) <= 8:
        issues.append(f"{tag}: intro.keypoints has {len(kp)}, brief says 5-8")
    terms = intro.get("terms", [])
    if not terms:
        issues.append(f"{tag}: intro.terms is empty — every term and symbol "
                      f"the lesson uses must be declared")
    for i, t in enumerate(terms):
        for f in ("term", "symbol", "read", "meaning"):
            if not t.get(f):
                issues.append(f"{tag}: terms[{i}] missing {f!r}")

    sheets = rev.get("sheets", [])
    examples = rev.get("examples", [])
    if not sheets:
        issues.append(f"{tag}: revision.sheets is empty")

    # Sheets and examples are {title, body} (design session, 2026-08-01): the
    # RENDERER emits the heading, so a body carrying its own <h3> would print
    # the heading twice.
    for kind, blocks in (("sheet", sheets), ("example", examples)):
        for i, blk in enumerate(blocks):
            if not isinstance(blk, dict):
                issues.append(f"{tag}: {kind}[{i}] is not a "
                              f"{{title, body}} object")
                continue
            if not blk.get("title"):
                issues.append(f"{tag}: {kind}[{i}] has no title")
            if not blk.get("body"):
                issues.append(f"{tag}: {kind}[{i}] has no body")
            if re.search(r"<h[1-5]\b", blk.get("body", "")):
                issues.append(f"{tag}: {kind}[{i}] body contains a heading — "
                              f"the renderer emits it; bodies are heading-free")
            # rule 4: never duplicate the lesson title, which the contents page
            # already takes from data/y*.json
            lt = (lesson_title or "").strip().lower()
            if lt and blk.get("title", "").strip().lower() == lt:
                issues.append(f"{tag}: {kind}[{i}] title duplicates the lesson "
                              f"title {lesson_title!r} — contents page owns it")

    # ---- budget (estimate; qa_revision_fit.py is the authority)
    def _report(label, c, kind):
        lo, med = PAGE_CAP[kind]
        if c > med:
            issues.append(f"{tag}: {label} ~{c} word-equivalents > the median "
                          f"{kind} capacity {med} — split it or move a figure "
                          f"to its own page; never shrink type")
        elif c > lo:
            warnings.append(f"{tag}: {label} ~{c} is between the tightest "
                            f"{kind} page ({lo}) and the median ({med}) — "
                            f"qa_revision_fit.py decides")

    # ---- the owner's figure rules (2026-08-02)
    def _check_figures(label, html):
        for vb in figure_heights(html):
            px = figure_px(vb)
            if px > HALF_PAGE_PX:
                issues.append(
                    f"{tag}: {label} has a figure {px:.0f}px tall — more than "
                    f"half the {HALF_PAGE_PX*2:.0f}px page. Owner rule: no "
                    f"figure may take half a page. Use a shorter viewBox "
                    f"(max ~{(HALF_PAGE_PX - FIG_FURNITURE_PX)/FIG_PX_PER_UNIT:.0f} units).")

    # opening sheet 1: opener
    _report("intro opener", _words(what) + COST_LIST_ITEM * len(kp), "opener")
    # opening sheet 2: terms & signs
    if len(terms) > MAX_TERMS_PER_SHEET:
        issues.append(f"{tag}: {len(terms)} terms — more than "
                      f"{MAX_TERMS_PER_SHEET} will not fit one terms sheet")
    terms_words = sum(_words(t.get("term", "") + " " + t.get("read", "")
                             + " " + t.get("meaning", "")) for t in terms)
    _report("terms sheet", terms_words + COST_TERM_ROW * len(terms), "terms")
    for kind, blocks in (("sheet", sheets), ("example", examples)):
        for i, blk in enumerate(blocks):
            body = blk.get("body", "") if isinstance(blk, dict) else blk
            _report(f"{kind}[{i}]", cost(body) + COST_HEADING, kind)
            _check_figures(f"{kind}[{i}]", body)

    # ---- TERMS FIRST (exact, and the reason this file exists)
    declared = " ".join(t.get("symbol", "") + " " + t.get("term", "")
                        for t in terms)
    declared_syms = symbols_in("\\(" + declared + "\\)") | set(
        re.findall(r"\\([A-Za-z]+)", declared))
    declared_syms |= {"\\" + s for s in
                      re.findall(r"\\([A-Za-z]+)", declared)}
    for kind, blocks in (("sheet", sheets), ("example", examples)):
        for i, blk in enumerate(blocks):
            blk_html = blk.get("body", "") if isinstance(blk, dict) else blk
            for sym in sorted(symbols_in(blk_html)):
                if sym in declared_syms:
                    continue
                if sym.lstrip("\\") in {t.get("term", "") for t in terms}:
                    continue
                issues.append(
                    f"{tag}: {kind}[{i}] uses symbol {sym!r} that intro.terms "
                    f"never introduces (owner rule 1: terms and signs first)")
    return True


def _titles_for(stem):
    """Lesson titles from data/y*.json — the contents page's source of truth."""
    sem, _, course = stem.partition("-")
    try:
        sd = json.loads(Path(f"data/{sem}.json").read_text(encoding="utf-8"))
    except OSError:
        return {}
    for c in sd.get("courses", []):
        if c["id"] == course:
            return {str(l["n"]): l.get("t", "") for l in c["lessons"]}
    return {}


def main(argv):
    files = [Path(p) for p in argv[1:]] or sorted(
        Path("data/content").glob("*.json"))
    issues, warns, seen, withrev = [], [], 0, 0
    for p in files:
        data = json.loads(p.read_text(encoding="utf-8"))
        titles = _titles_for(p.stem)
        for lid in sorted((k for k in data if k.isdigit()), key=int):
            seen += 1
            if check_lesson(p.stem, lid, data[lid], issues, titles.get(lid),
                            warns):
                withrev += 1
    for w in warns:
        print("WARN:", w)
    for s in issues:
        print("FAIL:", s)
    print(f"\n{len(files)} file(s), {seen} lesson(s), {withrev} carrying "
          f"revision blocks — {len(issues)} issue(s), {len(warns)} warning(s).")
    caps = "  ".join(f"{k} {lo}-{med}" for k, (lo, med) in PAGE_CAP.items())
    print(f"Per-kind capacity, word-equivalents (min-median): {caps}")
    print(f"Max {MAX_TERMS_PER_SHEET} terms/sheet. A figure costs "
          f"~{FIG_FURNITURE_PX:.0f}px + {FIG_PX_PER_UNIT}px per viewBox unit; "
          f"none may exceed half a page.")
    print("The AUTHORITY is design-previews/tools/qa_revision_fit.py — run it "
          "before every build; this is the fast pre-check.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
