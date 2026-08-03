#!/usr/bin/env python3
"""MechEd — Years 1-2 public prototype build.

Owner directive (2026-08-03, "scope = C"): ship ONE shareable link containing
Years 1 AND 2 complete, with Years 3-4 not shown at all. They are not "locked"
or greyed out — they are absent, so a visitor cannot reach an unauthored course
by any route and the site reads as a finished 24-course programme.

SUPERSEDES the 2026-07-26 Year-1-only scope this file was originally written
for (and which was deleted in c9c94942 when the prototype was cancelled). The
mechanism is unchanged; the scope and the chrome trim are not.

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

PROTOTYPE_YEARS = ("y1s1", "y1s2", "y2s1", "y2s2")     # Years 1 and 2
FULL_OUT = legacy.OUT                        # docs/
PROTO_OUT = FULL_OUT / "prototype"


#: bound once at import, BEFORE any rebinding — calling nb.load_curriculum from
#: inside the replacement would recurse into itself.
_REAL_LOAD_CURRICULUM = nb.load_curriculum


def filtered_curriculum():
    """The real curriculum, reduced to Years 1-2. Same objects, fewer semesters."""
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
# The homepage names the years from a hardcoded (1,2,3,4) rather than from the
# curriculum, so the filtered build still emits cards for years that no longer
# exist. That markup lives in design-owned chrome, which this script must not
# edit, so the prototype filters the EMITTED HTML at nexus_build's single write
# funnel instead — nexus_build.py stays byte-identical.
#
# RE-DERIVED 2026-08-03 against the current build, NOT inherited on trust. Two
# things had moved since this file was written in July:
#   * The year-N/summary.html links the old _DEAD_YEAR_LINK pattern targeted no
#     longer exist ANYWHERE (0 files) — the per-year compiled summaries were
#     retired by the 2026-07-30 "summaries per course, not per year" directive.
#     That pattern is deleted rather than kept: a regex that silently matches
#     nothing reads like coverage it does not provide.
#   * The homepage now emits the year cards TWICE (8 cards, not 4), so the
#     substitution must be global — it is, but the old count-based reasoning
#     about it was wrong.
# The residual year-N references are in-page anchors (curriculum/index.html#year-3),
# which the curriculum filter removes at source along with the section itself.
HIDDEN = "34"
_HIDDEN_YEAR_CARD = re.compile(
    r'<div class="year-card"><span class="yr">[^<]*\b[%s]\b[^<]*</span>.*?</span></div>'
    % HIDDEN, re.S)

# THE ONE UNTRUE CLAIM ON THE PAGE, fixed here rather than shipped again.
# content/pages/home-nexus.html hardcodes "4 years / 48 courses / 528 lessons"
# in the stat band and the hero meta line. Those numbers are TRUE of the full
# site, so the fragment must not be edited — the full build would start lying
# instead. The prototype rewrites them on the way out, the same way it drops
# the year cards.
#
# This exact defect shipped in the 2026-07-26 Year-1 prototype and was recorded
# as known-issue #1 ("the one untrue claim on the page"). It was never fixed,
# and the recovered script did not carry a fix, so it would have shipped a
# second time.
SCOPE_STATS = (
    ('<div class="stat"><b>4</b><span>years</span></div>',
     '<div class="stat"><b>2</b><span>years</span></div>'),
    ('<div class="stat"><b>48</b><span>courses</span></div>',
     '<div class="stat"><b>24</b><span>courses</span></div>'),
    ('<div class="stat"><b>528</b><span>lessons</span></div>',
     '<div class="stat"><b>264</b><span>lessons</span></div>'),
    ('4 YEARS &middot; 8 SEMESTERS &middot; 48 COURSES',
     '2 YEARS &middot; 4 SEMESTERS &middot; 24 COURSES'),
    ('4 YEARS · 8 SEMESTERS · 48 COURSES',
     '2 YEARS · 4 SEMESTERS · 24 COURSES'),
)


# The Curriculum nav dropdown also lists the years from a hardcoded 1-4. These
# are in-page anchors rather than page links, so they never reach an unauthored
# course — which is exactly why the semester-id scan in verify_prototype.py
# passed them. They are still wrong to ship: they advertise two years that are
# not in this build, and they scroll nowhere because the curriculum page no
# longer emits those sections. FOUND BY LOOKING AT THE PAGE, not by the gate;
# the gate now checks for them too.
_HIDDEN_NAV_YEAR = re.compile(
    r'<a href="[^"]*curriculum/index\.html#year-[%s]"[^>]*>[^<]*</a>' % HIDDEN)


def _trim_to_scope(html):
    html = _HIDDEN_YEAR_CARD.sub("", html)
    html = _HIDDEN_NAV_YEAR.sub("", html)
    for before, after in SCOPE_STATS:
        html = html.replace(before, after)
    return html


def build_prototype():
    print()
    print("=" * 64)
    print("YEARS 1-2 PROTOTYPE  ->", PROTO_OUT)
    print("=" * 64)

    real_loader, real_out, real_emit = nb.load_curriculum, nb.OUT, nb._emit

    def emit_trimmed(path, html):
        return real_emit(path, _trim_to_scope(html))

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
