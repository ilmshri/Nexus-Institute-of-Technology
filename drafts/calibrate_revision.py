#!/usr/bin/env python3
"""Recalibrate qa_revision.py's page-capacity constants against real measurement.

WHY THIS EXISTS. qa_revision.py budgets a block in WORD-EQUIVALENTS — prose
words plus a fitted vertical cost for display equations, table rows, list items
and headings. qa_revision_fit.py measures real rendered height and extrapolates
capacity in RAW WORDS. Those are different units, and the 2026-08-01 pass set
PAGE_MEDIAN/PAGE_MIN straight from the raw-word figure. On a prose-only block
the two agree; on an equation-heavy one a word-equivalent is worth far less
vertical space than a word, so the constants were wrong in a direction nobody
could see. This tool closes that by extrapolating capacity in the SAME units
qa_revision.py spends: for every block,

    capacity_we = (that block's word-equivalent cost) x CONTENT_H / (its height)

i.e. "how many word-equivalents of THIS block's density would fill one A4
sheet". Median and minimum over every measured block are the constants.

Re-run it whenever page density changes materially — adding figures to the
notes changes it a lot, which is exactly why this is a committed tool and not
a scratchpad one-off.

    python3 drafts/calibrate_revision.py [content-json ...]
"""
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "design-previews" / "tools"))

import qa_revision as qr                      # noqa: E402
import qa_revision_fit as fit                 # noqa: E402


def kind_of(block_id):
    """'... L7 sheet 1' -> 'sheet'. The trailing index is not part of a kind."""
    tail = block_id.rsplit(" L", 1)[-1].split(" ", 1)[-1]
    return tail.split(" ")[0]


def word_equivalents(block_id, rev, label):
    """The exact number qa_revision.py's _report() would judge this block by.

    Kept deliberately in lockstep with check_lesson(): if the cost model there
    changes, this must change with it or the constants drift out of meaning.
    """
    intro = rev["intro"]
    if label == "opener":
        return (qr._words(intro["what"])
                + qr.COST_LIST_ITEM * len(intro["keypoints"]))
    if label == "terms":
        terms = intro["terms"]
        body = sum(qr._words(t.get("term", "") + " " + t.get("read", "")
                             + " " + t.get("meaning", "")) for t in terms)
        return body + qr.COST_TERM_ROW * len(terms)
    kind, _, idx = label.partition(" ")
    blk = rev["sheets" if kind == "sheet" else "examples"][int(idx) - 1]
    return qr.cost(blk["body"]) + qr.COST_HEADING


def main(argv):
    files = [Path(a) for a in argv[1:]] or sorted(
        (ROOT / "data/content").glob("*.json"))
    blocks, meta = [], []
    for f in files:
        for bid, html, words in fit.blocks_for(f):
            blocks.append((bid, html, words))
            meta.append(bid)
    if not blocks:
        print("no renderable revision blocks found")
        return 0

    heights = fit.measure(blocks)

    # re-derive the word-equivalent cost per block from the source data
    import json
    costs = {}
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        sem, _, course_id = f.stem.partition("-")
        sd = json.loads((ROOT / f"data/{sem}.json").read_text(encoding="utf-8"))
        course = next((c for c in sd.get("courses", [])
                       if c["id"] == course_id), None)
        if course is None:
            continue
        for les in course["lessons"]:
            tab = data.get(str(les["n"]))
            if not tab or "revision" not in tab:
                continue
            rev = tab["revision"]
            labels = (["opener", "terms"]
                      + [f"sheet {i+1}" for i in range(len(rev["sheets"]))]
                      + [f"example {i+1}"
                         for i in range(len(rev.get("examples") or []))])
            for label in labels:
                costs[f'{f.stem} L{les["n"]} {label}'] = word_equivalents(
                    f.stem, rev, label)

    print(f'{"block":<44}{"word-eq":>8}{"height":>9}{"page%":>7}'
          f'{"capacity":>10}')
    caps = []                       # (kind, capacity) per measured block
    for (bid, _html, _w), h in zip(blocks, heights):
        we = costs.get(bid)
        if we is None:
            continue
        cap = we * fit.CONTENT_H / h
        caps.append((kind_of(bid), cap))
        print(f'{bid:<44}{we:>8}{h:>8.0f}px{h/fit.CONTENT_H*100:>6.0f}%'
              f'{cap:>10.0f}')

    print(f"\n{len(caps)} block(s) measured against a {fit.CONTENT_H:.0f}px "
          f"content box.")

    # Capacity is PER KIND, not global. qa_revision.py spends three different
    # cost models — the opener's (what + keypoints), the terms sheet's (row
    # text + per-row overhead) and cost() for sheets/examples — and each omits
    # different fixed furniture. An opener costed at 78 word-equivalents really
    # renders 631px because its model does not price the lesson-title rule or
    # the key-point line-height; pooling that with a sheet's model would put
    # the global floor near 110 and flag every sheet in the document. So each
    # kind is calibrated against its own measurements.
    print("\nWORD-EQUIVALENT capacity, per block kind "
          "(each kind has its own cost model, so each has its own capacity):")
    by_kind, order = {}, ["opener", "terms", "sheet", "example"]
    for kind, cap in caps:
        by_kind.setdefault(kind, []).append(cap)
    for kind in order:
        vals = sorted(by_kind.get(kind, []))
        if not vals:
            continue
        print(f"  {kind:<9} n={len(vals):<3} min {vals[0]:>5.0f}   "
              f"median {statistics.median(vals):>5.0f}   max {vals[-1]:>5.0f}")
    cur = "  ".join(f"{k} {lo}-{med}" for k, (lo, med) in qr.PAGE_CAP.items())
    print(f"\nqa_revision.py currently carries: {cur}")
    print("Fail a block above its kind's median; warn between its kind's min "
          "and median — that band is where only qa_revision_fit.py can rule.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
