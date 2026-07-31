#!/usr/bin/env python3
"""Shape text with harfbuzz and emit a single combined SVG path (y-down, baseline at 0)."""
import io
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FDIR = Path(__file__).parent / "fonts"
_cache = {}


def load(path, axes=None):
    key = (str(path), tuple(sorted((axes or {}).items())))
    if key in _cache:
        return _cache[key]
    tt = TTFont(str(path))
    if axes and "fvar" in tt:
        instantiateVariableFont(tt, axes, inplace=True)
    buf = io.BytesIO()
    tt.save(buf)
    data = buf.getvalue()
    face = hb.Face(data)
    font = hb.Font(face)
    upm = face.upem
    _cache[key] = (tt, font, upm)
    return _cache[key]


def shape(path, text, axes=None, direction="ltr", script="Latn", lang="en",
          features=None, tracking=0.0):
    """Returns (svg_path_d, total_advance, upm). tracking in font units added per glyph."""
    tt, font, upm = load(path, axes)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction
    buf.script = script
    buf.language = lang
    hb.shape(font, buf, features or {})
    glyph_set = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    x = 0.0
    parts = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gname = order[info.codepoint]
        spen = SVGPathPen(glyph_set)
        tpen = TransformPen(spen, Transform(1, 0, 0, -1, x + pos.x_offset, -pos.y_offset))
        glyph_set[gname].draw(tpen)
        d = spen.getCommands()
        if d:
            parts.append(d)
        x += pos.x_advance + tracking
    return " ".join(parts), x, upm


if __name__ == "__main__":
    d, adv, upm = shape(FDIR / "SourceSerif4%5Bopsz%2Cwght%5D.ttf", "MechEd",
                        axes={"opsz": 40, "wght": 600})
    print("serif MechEd: advance", round(adv), "upm", upm, "path len", len(d))
    d2, adv2, upm2 = shape(FDIR / "IBMPlexSansArabic-SemiBold.ttf", "هندسةٌ للابتكار",
                           direction="rtl", script="Arab", lang="ar")
    print("arabic descriptor: advance", round(adv2), "upm", upm2, "path len", len(d2))
    d3, adv3, _ = shape(FDIR / "SourceSans3%5Bwght%5D.ttf", "ENGINEERED TO INNOVATE",
                        axes={"wght": 500}, tracking=160)
    print("sans caps descriptor: advance", round(adv3), "path len", len(d3))
