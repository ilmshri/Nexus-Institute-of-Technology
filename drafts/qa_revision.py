#!/usr/bin/env python3
"""Author-side gates for the per-lesson "revision" blocks.

⚠️ THIS IS NOT THE PAGE-FIT GATE. The owner's brief assigns
design-previews/tools/qa_revision_fit.py to the DESIGN session; it measures
real rendered height in the print layout and is the authority on whether a
block fits one A4 page. That file does not exist yet, so this checker stands
in for the part an author can verify WITHOUT a renderer:

  1. Schema shape — the fields exist and are the right types.
  2. Budget    — a prose-length estimate against the owner's stated
                 320-420 words/sheet, with equations and table rows costed as
                 vertical space. An ESTIMATE, deliberately conservative; it
                 cannot see the real layout and must not be reported as if it
                 could.
  3. TERMS FIRST — the owner's rule 1, and the one gate here that is exact:
                 no symbol may appear in a sheet or example unless it was
                 declared in intro.terms. This catches the defect the rule
                 exists to prevent, and a renderer would never catch it.

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

BUDGET_SHEET = 420          # owner's stated upper bound
BUDGET_WARN = 380
BUDGET_EXAMPLE = 460        # examples run a little denser (steps, not prose)
BUDGET_INTRO = 430

# LaTeX control words that are structure or operators, never a quantity the
# student must have been introduced to.
STRUCTURAL = {
    "frac", "sqrt", "left", "right", "begin", "end", "text", "mathrm", "cdot",
    "times", "quad", "qquad", "displaystyle", "sum", "int", "lim", "to",
    "infty", "approx", "le", "ge", "ne", "pm", "mp", "cases", "array",
    "partial", "d", "dx", "dt", "log", "ln", "exp", "sin", "cos", "tan",
    "matrix", "pmatrix", "bmatrix", "hline", "\\", "over", "big", "Big",
    "label", "tag", "operatorname", "mathbf", "boldsymbol", "colon",
}


def _text(html):
    """Visible prose only: strip tags, drop maths, decode entities."""
    s = re.sub(r"\\\[.*?\\\]", " ", html, flags=re.S)      # display maths
    s = re.sub(r"\\\(.*?\\\)", " ", s, flags=re.S)          # inline maths
    s = re.sub(r"<[^>]+>", " ", s)
    return unescape(s)


def _words(html):
    return len(_text(html).split())


def cost(html):
    """Word-equivalent vertical cost of one block."""
    w = _words(html)
    w += COST_DISPLAY_EQ * len(re.findall(r"\\\[", html))
    w += COST_TABLE_ROW * len(re.findall(r"<tr\b", html))
    w += COST_LIST_ITEM * len(re.findall(r"<li\b", html))
    w += COST_HEADING * len(re.findall(r"<h[3-5]\b", html))
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


def check_lesson(name, lid, lesson, issues, lesson_title=None):
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

    # ---- budget (ESTIMATE — see module docstring)
    intro_cost = (_words(what) + COST_LIST_ITEM * len(kp)
                  + COST_TABLE_ROW * len(terms))
    if intro_cost > BUDGET_INTRO:
        issues.append(f"{tag}: intro ~{intro_cost} word-equivalents > "
                      f"{BUDGET_INTRO} — split the terms table or trim keypoints")
    for i, s in enumerate(sheets):
        c = cost(s.get("body", "")) + COST_HEADING if isinstance(s, dict) else cost(s)
        if c > BUDGET_SHEET:
            issues.append(f"{tag}: sheet[{i}] ~{c} word-equivalents > "
                          f"{BUDGET_SHEET} — split it, do not shrink type")
    for i, e in enumerate(examples):
        c = cost(e.get("body", "")) + COST_HEADING if isinstance(e, dict) else cost(e)
        if c > BUDGET_EXAMPLE:
            issues.append(f"{tag}: example[{i}] ~{c} word-equivalents > "
                          f"{BUDGET_EXAMPLE} — move one example to its own page")

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
    issues, seen, withrev = [], 0, 0
    for p in files:
        data = json.loads(p.read_text(encoding="utf-8"))
        titles = _titles_for(p.stem)
        for lid in sorted((k for k in data if k.isdigit()), key=int):
            seen += 1
            if check_lesson(p.stem, lid, data[lid], issues, titles.get(lid)):
                withrev += 1
    for s in issues:
        print("FAIL:", s)
    print(f"\n{len(files)} file(s), {seen} lesson(s), {withrev} carrying "
          f"revision blocks — {len(issues)} issue(s).")
    print("NOTE: budget numbers are an ESTIMATE. The authoritative page-fit "
          "gate is design-previews/tools/qa_revision_fit.py, owned by the "
          "design session and NOT YET PRESENT.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
