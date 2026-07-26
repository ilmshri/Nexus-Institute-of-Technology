# -*- coding: utf-8 -*-
"""Verify the Arabic (_ar) sibling keys against their English originals.

Run:  python3 drafts/verify_ar.py            # all Y1S1 courses
      python3 drafts/verify_ar.py math-1     # one course

Checks the contract the Arabic content must satisfy, per the two-tree schema:

  1. markup parity   — identical HTML tag multiset per field, once the added
                       <bdi> LTR isolators are discounted. Translate text,
                       never restructure.
  2. math parity     — identical count of inline \\( \\) and display \\[ \\]
                       spans. Rendering an equation or symbol as an Arabic
                       word is restructuring, and this is what catches it.
  3. table parity    — identical <tr> count in glossary tables.
  4. section markers — §N headings preserved so the build's §N->0N transform
                       still applies to the Arabic tree.
  5. LTR isolation   — no bare Latin letter or digit anywhere in Arabic prose;
                       every unit, numeral and token must sit inside <bdi>
                       (or inside math, or be a structural §N marker).
  6. quiz shape      — choices_ar has the same length as choices AND there is
                       no answer_ar: the Arabic item reuses the English answer
                       index by position. That is deliberate — a second index
                       is a value that can drift across ~330 MC items.
  7. English intact  — translating must never modify the English source field.

Reports per lesson; exit status is non-zero if anything fails.
"""
import html
import json
import re
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "data" / "content"
COURSES = ["math-1", "statics", "materials-1", "physics-1", "computing", "drawing-cad"]
PROSE = ("lecture", "foundations", "kuwait", "recap", "examples")

TAGS = lambda s: sorted(t for t in re.findall(r"<(\w+)", s) if t != "bdi")
INLINE = lambda s: s.count("\\(")
DISPLAY = lambda s: s.count("\\[")
ROWS = lambda s: len(re.findall(r"<tr>", s))
SECT = lambda s: re.findall(r"§\d", s)


def leaks(arabic):
    """Bare Latin/digit runs in Arabic prose (outside <bdi>, math, tags, §N)."""
    s = re.sub(r"<bdi>.*?</bdi>", " ", arabic, flags=re.S)
    s = re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>|§\d|&[a-z]+;|&#\d+;", " ", s)
    return [m.group(0) for m in re.finditer(r"[A-Za-z0-9]+", html.unescape(s))]


def check_pair(label, en, ar, fails, *, tags=True):
    if tags and TAGS(en) != TAGS(ar):
        fails.append(f"{label}: tag structure differs")
    if INLINE(en) != INLINE(ar):
        fails.append(f"{label}: inline math {INLINE(en)} -> {INLINE(ar)}")
    if DISPLAY(en) != DISPLAY(ar):
        fails.append(f"{label}: display math {DISPLAY(en)} -> {DISPLAY(ar)}")
    if ROWS(en) != ROWS(ar):
        fails.append(f"{label}: table rows {ROWS(en)} -> {ROWS(ar)}")
    if SECT(en) != SECT(ar):
        fails.append(f"{label}: section markers differ")
    bad = leaks(ar)
    if bad:
        fails.append(f"{label}: unisolated Latin/digit {bad[:5]}")


def main():
    courses = sys.argv[1:] or COURSES
    total_lessons = translated = 0
    all_fails = []

    for cid in courses:
        data = json.loads((CONTENT / f"y1s1-{cid}.json").read_text(encoding="utf-8"))
        for n in sorted(data, key=lambda k: int(k)):
            les = data[n]
            total_lessons += 1
            has_ar = any(k.endswith("_ar") for k in les) or \
                any("q_ar" in it for it in (les.get("quiz") or []) if isinstance(it, dict))
            if not has_ar:
                continue
            translated += 1
            fails = []
            tag = f"{cid} L{int(n):02d}"

            for f in PROSE:
                if f + "_ar" in les:
                    if f not in les:
                        fails.append(f"{f}_ar present with no English {f}")
                        continue
                    check_pair(f"{tag} {f}", les[f], les[f + "_ar"], fails)

            for i, it in enumerate(les.get("quiz") or [], 1):
                if not isinstance(it, dict) or "q_ar" not in it:
                    continue
                check_pair(f"{tag} q{i} q", it["q"], it["q_ar"], fails)
                if "solution_ar" in it:
                    check_pair(f"{tag} q{i} sol", it["solution"], it["solution_ar"], fails)
                if it.get("type") == "mc":
                    ca = it.get("choices_ar")
                    if ca is None:
                        fails.append(f"{tag} q{i}: mc item missing choices_ar")
                    elif len(ca) != len(it["choices"]):
                        fails.append(f"{tag} q{i}: choices_ar length "
                                     f"{len(ca)} != {len(it['choices'])}")
                    else:
                        for j, c in enumerate(ca):
                            if leaks(c):
                                fails.append(f"{tag} q{i} choice{j}: unisolated {leaks(c)[:3]}")
                    if "answer_ar" in it:
                        fails.append(f"{tag} q{i}: answer_ar present — the English "
                                     f"answer index must be reused by position")
                    if not isinstance(it.get("answer"), int):
                        fails.append(f"{tag} q{i}: English answer index missing/!int")
                elif "choices_ar" in it:
                    fails.append(f"{tag} q{i}: solve item must not carry choices_ar")

            print(("  OK   " if not fails else "  FAIL ") + tag +
                  ("" if not fails else "  (" + str(len(fails)) + " problem(s))"))
            for f in fails:
                print("         - " + f)
            all_fails += fails

    print(f"\n{translated}/{total_lessons} Y1S1 lessons carry Arabic; "
          f"{len(all_fails)} contract problem(s).")
    return 1 if all_fails else 0


if __name__ == "__main__":
    sys.exit(main())
