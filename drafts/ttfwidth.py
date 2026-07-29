"""Minimal TrueType advance-width reader — no third-party deps.

Gives real glyph advances for the macOS system sans (SF NS), which is what
`font-family="ui-sans-serif,system-ui,sans-serif"` actually resolves to in the
browser the diagrams are checked in. Used to size SVG <text> labels honestly
instead of guessing an average character width.
"""
import struct
from pathlib import Path

FONT = Path("/System/Library/Fonts/SFNS.ttf")

# SFNS.ttf is a variable font; hmtx carries its *default* instance, but at the
# 10-12px sizes these diagrams use the browser selects a wider optical size.
# Measured against getComputedTextLength() over 8 real labels in a built lesson
# page: ratio 1.135-1.175, mean 1.149. Use the top of that range — a false
# "too wide" costs a minute, a missed one ships a clipped label.
CALIBRATION = 1.18


def _tables(buf):
    tag = buf[:4]
    off = 0
    if tag == b"ttcf":
        off = struct.unpack(">I", buf[12:16])[0]
    num = struct.unpack(">H", buf[off + 4:off + 6])[0]
    out = {}
    for i in range(num):
        p = off + 12 + i * 16
        name = buf[p:p + 4].decode("latin-1")
        start, length = struct.unpack(">II", buf[p + 8:p + 16])
        out[name] = (start, length)
    return out


def _cmap(buf, start):
    n = struct.unpack(">H", buf[start + 2:start + 4])[0]
    best = None
    for i in range(n):
        pid, eid, off = struct.unpack(">HHI", buf[start + 4 + i * 8:start + 12 + i * 8])
        fmt = struct.unpack(">H", buf[start + off:start + off + 2])[0]
        if fmt == 4 and (pid, eid) in ((3, 1), (0, 3), (0, 4)):
            best = start + off
        elif fmt == 12 and (pid, eid) in ((3, 10), (0, 4), (0, 6)):
            return ("12", start + off)
    if best is None:
        raise RuntimeError("no usable cmap subtable")
    return ("4", best)


def _lookup4(buf, t, ch):
    segx2 = struct.unpack(">H", buf[t + 6:t + 8])[0]
    seg = segx2 // 2
    ends = t + 14
    starts = ends + segx2 + 2
    deltas = starts + segx2
    ranges = deltas + segx2
    for i in range(seg):
        end = struct.unpack(">H", buf[ends + i * 2:ends + i * 2 + 2])[0]
        if ch > end:
            continue
        st = struct.unpack(">H", buf[starts + i * 2:starts + i * 2 + 2])[0]
        if ch < st:
            return 0
        delta = struct.unpack(">h", buf[deltas + i * 2:deltas + i * 2 + 2])[0]
        ro = struct.unpack(">H", buf[ranges + i * 2:ranges + i * 2 + 2])[0]
        if ro == 0:
            return (ch + delta) & 0xFFFF
        p = ranges + i * 2 + ro + (ch - st) * 2
        g = struct.unpack(">H", buf[p:p + 2])[0]
        return 0 if g == 0 else (g + delta) & 0xFFFF
    return 0


def _lookup12(buf, t, ch):
    n = struct.unpack(">I", buf[t + 12:t + 16])[0]
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        p = t + 16 + mid * 12
        s, e, g = struct.unpack(">III", buf[p:p + 12])
        if ch < s:
            hi = mid - 1
        elif ch > e:
            lo = mid + 1
        else:
            return g + (ch - s)
    return 0


class Metrics:
    def __init__(self, path=FONT):
        buf = path.read_bytes()
        self.buf = buf
        t = _tables(buf)
        head = t["head"][0]
        self.upem = struct.unpack(">H", buf[head + 18:head + 20])[0]
        hhea = t["hhea"][0]
        self.num_h = struct.unpack(">H", buf[hhea + 34:hhea + 36])[0]
        self.hmtx = t["hmtx"][0]
        self.cfmt, self.ctab = _cmap(buf, t["cmap"][0])
        self._cache = {}

    def advance(self, ch):
        """Advance width of one character, in em units (1.0 == font-size)."""
        if ch in self._cache:
            return self._cache[ch]
        cp = ord(ch)
        g = (_lookup12(self.buf, self.ctab, cp) if self.cfmt == "12"
             else _lookup4(self.buf, self.ctab, cp))
        if g == 0:                      # missing glyph — assume a wide fallback
            w = 0.6
        else:
            i = min(g, self.num_h - 1)
            aw = struct.unpack(">H", self.buf[self.hmtx + i * 4:self.hmtx + i * 4 + 2])[0]
            w = aw / self.upem
        self._cache[ch] = w
        return w

    def width(self, text, size, weight=400):
        """Rendered width of `text` at `size` px. Bold gets a modest uplift —
        SFNS.ttf's default instance is Regular, and the browser synthesises or
        selects a heavier cut for font-weight:700."""
        w = sum(self.advance(c) for c in text) * size * CALIBRATION
        return w * (1.06 if int(weight) >= 600 else 1.0)


_M = None


def metrics():
    global _M
    if _M is None:
        _M = Metrics()
    return _M


if __name__ == "__main__":
    m = metrics()
    for s in ("Marin factors", "Se = 174", "life N (log cycles)",
              "Kt is geometry only — what a material actually \"feels\" in "
              "fatigue depends on notch sensitivity too"):
        print(f"{m.width(s, 11):7.1f}px  ({len(s)} chars, "
              f"{m.width(s,11)/len(s)/11:.3f} em/char)  {s[:50]}")
