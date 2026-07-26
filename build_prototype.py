#!/usr/bin/env python3
"""MechEd — Year-1-only public prototype build.

Owner directive (2026-07-26): ship ONE shareable link containing Year 1
complete, with Years 2-4 not shown at all. Years 2-4 are not "locked" or
greyed out — they are absent, so a visitor cannot reach an unauthored course
by any route and the site reads as a finished 12-course Year-1 programme.

DESIGN-OWNED CODE IS NOT TOUCHED. This script imports nexus_build and runs its
own main() against a filtered curriculum and a different output directory.
nexus_build.py, nexus.css and nexus.js are read, never modified. If the design
session changes any of them, this script inherits the change automatically.

How the filtering works: nexus_build imports `load_curriculum` and `OUT` into
its own module namespace, and every function inside it resolves those as module
globals. Rebinding them on the module object therefore redirects the whole
build with no edit to the generator itself.

Run:  python3 build_prototype.py
      python3 build_prototype.py --prototype-only   (skip the full-site rebuild)

Emits:
  docs/            the full site (all 4 years) — unchanged behaviour
  docs/prototype/  Year 1 only  ->  https://<pages-host>/prototype/

Order matters: nexus_build.main() does shutil.rmtree(docs) first, which would
delete a prototype living inside it. So the full build runs FIRST and the
prototype is written afterwards. Running this script instead of
`python3 nexus_build.py` keeps the two in sync automatically.
"""
import re
import shutil
import sys
from pathlib import Path

import build as legacy
import nexus_build as nb

PROTOTYPE_YEARS = ("y1s1", "y1s2")          # Year 1 only
FULL_OUT = legacy.OUT                        # docs/
PROTO_OUT = FULL_OUT / "prototype"


#: bound once at import, BEFORE any rebinding — calling nb.load_curriculum from
#: inside the replacement would recurse into itself.
_REAL_LOAD_CURRICULUM = nb.load_curriculum


def filtered_curriculum():
    """The real curriculum, reduced to Year 1. Same objects, fewer semesters."""
    sems = [s for s in _REAL_LOAD_CURRICULUM() if s["id"] in PROTOTYPE_YEARS]
    if len(sems) != len(PROTOTYPE_YEARS):
        raise SystemExit(f"expected {PROTOTYPE_YEARS}, found {[s['id'] for s in sems]}")
    return sems


def build_full():
    print("=" * 64)
    print("FULL SITE  ->", FULL_OUT)
    print("=" * 64)
    nb.main()


# --------------------------------------------------------------- chrome trim --
# Two places name the years from a hardcoded (1,2,3,4) rather than from the
# curriculum: the nav dropdown's year-summary list and the homepage year cards.
# Both live in design-owned chrome, which this script must not edit. So the
# prototype filters the EMITTED HTML at nexus_build's single write funnel
# instead — nexus_build.py stays byte-identical, and because this trims output
# rather than reimplementing the nav, it keeps working if the design changes.
HIDDEN = "234"
_DEAD_YEAR_LINK = re.compile(
    r'<a href="[^"]*curriculum/year-[%s]/summary\.html"[^>]*>.*?</a>' % HIDDEN, re.S)
_HIDDEN_YEAR_CARD = re.compile(
    r'<div class="year-card"><span class="yr">[^<]*\b[%s]\b[^<]*</span>.*?</span></div>'
    % HIDDEN, re.S)


def _trim_hidden_years(html):
    html = _HIDDEN_YEAR_CARD.sub("", html)
    html = _DEAD_YEAR_LINK.sub("", html)
    return html


def build_prototype():
    print()
    print("=" * 64)
    print("YEAR-1 PROTOTYPE  ->", PROTO_OUT)
    print("=" * 64)

    real_loader, real_out, real_emit = nb.load_curriculum, nb.OUT, nb._emit

    def emit_trimmed(path, html):
        return real_emit(path, _trim_hidden_years(html))

    try:
        nb.load_curriculum = filtered_curriculum
        nb.OUT = PROTO_OUT
        legacy.OUT = PROTO_OUT          # anything reached through the legacy layer
        nb._emit = emit_trimmed
        nb.main()
    finally:
        nb.load_curriculum, nb.OUT, nb._emit = real_loader, real_out, real_emit
        legacy.OUT = FULL_OUT


def main():
    proto_only = "--prototype-only" in sys.argv
    if not proto_only:
        build_full()
    elif not FULL_OUT.exists():
        raise SystemExit("docs/ does not exist — run without --prototype-only first")
    else:
        # the prototype lives inside docs/; clear just it, leave the rest alone
        if PROTO_OUT.exists():
            shutil.rmtree(PROTO_OUT)
    build_prototype()

    n_html = len(list(PROTO_OUT.rglob("*.html")))
    print()
    print(f"prototype pages: {n_html}")
    print("verify with:  python3 verify_prototype.py")


if __name__ == "__main__":
    main()
