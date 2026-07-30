#!/usr/bin/env python3
"""Curriculum-sequencing gates for MechEd (owner directive, 2026-07-31).

Imported by qa_content.py, which runs these as part of every sweep. Kept in
its own module because these four checks are COURSE-level and cross-file,
where every gate in qa_content.py is per-lesson.

The rule they enforce: a lesson may never assume anything not already taught
in an earlier lesson. The four checks are

  (a) declared forward reference    — a foundations "What this lesson assumes"
      entry citing a LATER lesson of the same course
  (b) undeclared forward reference  — a lesson using a term that its own course
      does not introduce until a later lesson
  (c) cross-course prerequisite direction — a foundations entry citing a course
      that does not precede this one in curriculum order, or a lesson number
      that course does not have
  (d) series instalment             — an embedded video that is a numbered
      instalment of a semester course, which carries the previous lecture's
      context, notation and running examples our student never saw

Run standalone for the sequencing report only:  python3 drafts/qa_sequence.py
"""
import json
import re
import sys
from html import unescape
from pathlib import Path

LESSONS_PER_COURSE = 11

# Informal names used in foundations blocks that are not the course title.
# Everything else is resolved from the course titles themselves.
ALIASES = {
    "math i": "math-1", "maths i": "math-1", "mathematics i": "math-1",
    "math ii": "math-2", "mathematics ii": "math-2",
    "math iii": "math-3", "mathematics iii": "math-3",
    "physics i": "physics-1", "physics": "physics-1",
    "materials i": "materials-1", "materials science i": "materials-1",
    "materials ii": "materials-2", "materials science ii": "materials-2",
    "statics": "statics", "engineering statics": "statics",
    "dynamics": "dynamics", "engineering dynamics": "dynamics",
    "thermodynamics i": "thermo-1", "thermo i": "thermo-1",
    "thermodynamics ii": "thermo-2", "thermo ii": "thermo-2",
    "strength of materials": "strength", "som": "strength",
    "fluid mechanics": "fluids", "fluids": "fluids",
    "engineering statistics": "statistics", "statistics": "statistics",
    "electronics & sensors": "electronics-sensors",
    "electronics and sensors": "electronics-sensors",
    "electrical fundamentals": "electrical", "electrical": "electrical",
    "engineering computing": "computing", "computing": "computing",
    "engineering drawing & cad": "drawing-cad", "drawing & cad": "drawing-cad",
    "heat transfer": "heat-transfer",
    "machine design i": "machine-design-1",
    "machine design ii": "machine-design-2",
    "manufacturing processes i": "mfg-processes-1",
    "manufacturing processes ii": "mfg-processes-2",
    "manufacturing processes iii": "mfg-processes-3",
    "metrology": "metrology", "metrology & quality control": "metrology",
    "kinematics & dynamics of machinery": "kinematics-machinery",
    "mechanical vibrations": "vibrations", "vibrations": "vibrations",
}

# Channels that publish numbered instalments of a taught semester course.
COURSE_CHANNELS = {
    "mit opencourseware", "nptelhrd", "nptel-noc iitm", "nptel",
    "yale courses", "stanford online", "iit kharagpur july 2018",
}

INSTALMENT_RE = re.compile(
    r"\b(?:lec(?:ture)?\.?\s*[-#]?\s*(\d+)"
    r"|part\s*[-#]?\s*(\d+)"
    r"|episode\s*(\d+)|ep\.?\s*(\d+)"
    r"|#\s?(\d+))\b", re.I)

# "MIT 18.01", "MIT 6.0002", "18.03SC" — the series a lecture belongs to.
SERIES_RE = re.compile(r"\b((?:MIT|NPTEL)\s*[\dA-Z]+(?:\.\d+)?(?:SC)?)\b", re.I)


def curriculum(root=Path(".")):
    """Ordered course records: index rises with curriculum position."""
    out = []
    for f in sorted(root.glob("data/y[0-9]s[0-9].json")):
        sem = f.stem
        data = json.loads(f.read_text(encoding="utf-8"))
        for c in data.get("courses", []):
            out.append({
                "index": len(out), "sem": sem, "id": c["id"],
                "code": c.get("code", ""), "title": c.get("title", ""),
                "lessons": c.get("lessons", []),
            })
    return out


def alias_map(courses):
    m = dict(ALIASES)
    for c in courses:
        head = re.split(r"\s+[—–-]\s+", c["title"])[0].strip().lower()
        m.setdefault(head, c["id"])
        m.setdefault(c["title"].strip().lower(), c["id"])
        if c["code"]:
            m.setdefault(c["code"].strip().lower(), c["id"])
    return m


def strip_html(s):
    return unescape(re.sub(r"<[^>]+>", " ", s or ""))


def assumes_block(foundations):
    """The 'What this lesson assumes' <ul>, as a list of plain-text entries."""
    m = re.search(r"What this lesson assumes.*?<ul[^>]*>(.*?)</ul>",
                  foundations or "", re.S | re.I)
    if not m:
        return []
    return [re.sub(r"\s+", " ", strip_html(li)).strip()
            for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.S)]


# ---------------------------------------------------------------- (a)
SAME_COURSE_RE = re.compile(
    r"\(\s*Lessons?\s+([0-9,\s–—-]+(?:and\s*\d+)?)\s*\)", re.I)


def _lesson_numbers(chunk):
    chunk = chunk.replace("and", ",").replace("&", ",")
    nums = []
    for part in re.split(r"[,\s]+", chunk):
        part = part.strip()
        if not part:
            continue
        rng = re.match(r"^(\d+)\s*[–—-]\s*(\d+)$", part)
        if rng:
            nums.extend(range(int(rng.group(1)), int(rng.group(2)) + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums


def check_declared_forward(course_id, lessons, issues):
    for lid, les in lessons.items():
        try:
            here = int(lid)
        except ValueError:
            continue
        raw = les.get("foundations") or ""
        block = re.search(r"What this lesson assumes.*?</ul>", raw, re.S | re.I)
        text = unescape(block.group(0)) if block else ""
        for m in SAME_COURSE_RE.finditer(text):
            for n in _lesson_numbers(m.group(1)):
                if n >= here:
                    issues.append(
                        ("a", course_id, here,
                         f"foundations cites Lesson {n} of its own course "
                         f"(this is Lesson {here})"))


# ---------------------------------------------------------------- (b)
STOP = {
    "the", "and", "for", "with", "this", "that", "key", "relation", "relations",
    "problem", "solution", "answer", "sanity", "check", "note", "find", "given",
    "what", "when", "why", "how", "from", "into", "over", "under", "each",
    "both", "same", "than", "then", "they", "them", "its", "one", "two",
}


def term_index(lessons):
    """First lesson at which each term is INTRODUCED, per course.

    A term counts as introduced by a glossary row, a keybox tag, or a bold
    run inside the lecture — the three places this project defines things.
    """
    first = {}
    for lid in sorted(lessons, key=lambda k: int(k) if k.isdigit() else 999):
        if not lid.isdigit():
            continue
        n = int(lid)
        les = lessons[lid]
        found = set()
        fo = les.get("foundations") or ""
        for row in re.findall(r"<tr>\s*<td>(.*?)</td>", fo, re.S):
            found.add(strip_html(row))
        lec = les.get("lecture") or ""
        for tag in re.findall(r'<span class="tag">(.*?)</span>', lec, re.S):
            txt = strip_html(tag)
            txt = re.split(r"[—–-]", txt, 1)[-1]
            found.add(txt)
        for b in re.findall(r"<b>(.*?)</b>", lec, re.S):
            found.add(strip_html(b))
        for term in found:
            t = normalise_term(term)
            if t and t not in first:
                first[t] = n
    return first


def normalise_term(term):
    t = re.sub(r"\\\(.*?\\\)", " ", term)          # drop inline maths
    t = re.sub(r"[^A-Za-z \-']", " ", t)
    t = re.sub(r"\s+", " ", t).strip().lower()
    if len(t) < 6 or len(t.split()) > 4:
        return None
    if all(w in STOP for w in t.split()):
        return None
    if t.split()[0] in {"problem", "solution", "answer", "sanity"}:
        return None
    return t


def check_undeclared_forward(course_id, lessons, issues):
    first = term_index(lessons)
    for lid in sorted(lessons, key=lambda k: int(k) if k.isdigit() else 999):
        if not lid.isdigit():
            continue
        here = int(lid)
        les = lessons[lid]
        body = strip_html(les.get("lecture") or "")
        for q in les.get("quiz") or []:
            body += " " + strip_html(q.get("q") or "")
            body += " " + strip_html(q.get("solution") or "")
        low = re.sub(r"\s+", " ", body).lower()
        for term, intro in first.items():
            if intro <= here:
                continue
            if re.search(r"\b" + re.escape(term) + r"\b", low):
                issues.append(
                    ("b", course_id, here,
                     f"uses {term!r}, which this course does not introduce "
                     f"until Lesson {intro}"))


# ---------------------------------------------------------------- (c)
CROSS_RE = re.compile(r"\(([^()]{2,60}?)\)")


def check_cross_course(course_id, lessons, courses, amap, issues):
    by_id = {c["id"]: c for c in courses}
    here_idx = by_id[course_id]["index"] if course_id in by_id else None
    if here_idx is None:
        return
    for lid, les in lessons.items():
        if not lid.isdigit():
            continue
        for entry in assumes_block(les.get("foundations")):
            for m in CROSS_RE.finditer(entry):
                raw = m.group(1).strip()
                if re.match(r"^Lessons?\b", raw, re.I):
                    continue                       # handled by check (a)
                mm = re.match(r"^(.*?)(?:,?\s*L(?:esson)?\s*(\d+)"
                              r"(?:\s*[–—-]\s*L?(\d+))?)?$", raw, re.I)
                nameraw = (mm.group(1) or "").strip(" ,")
                key = nameraw.lower().strip()
                cid = amap.get(key)
                if not cid:
                    continue                       # not a course citation
                cited = by_id.get(cid)
                if cited is None:
                    continue
                if cited["index"] >= here_idx:
                    rel = ("itself" if cid == course_id
                           else f"{cited['sem']} vs this course's "
                                f"{by_id[course_id]['sem']}")
                    issues.append(
                        ("c", course_id, int(lid),
                         f"cites {nameraw!r} ({cid}) which does NOT precede "
                         f"this course ({rel})"))
                nums = [int(g) for g in (mm.group(2), mm.group(3)) if g]
                for n in nums:
                    have = len(cited["lessons"]) or LESSONS_PER_COURSE
                    if n > have:
                        issues.append(
                            ("c", course_id, int(lid),
                             f"cites {nameraw} L{n}, but {cid} has only "
                             f"{have} lessons"))


# ---------------------------------------------------------------- (d)
def instalment_number(title):
    m = INSTALMENT_RE.search(title or "")
    if not m:
        return None
    for g in m.groups():
        if g:
            return int(g)
    return None


def series_key(title, channel):
    m = SERIES_RE.search(title or "")
    if m:
        return re.sub(r"\s+", " ", m.group(1)).upper()
    return (channel or "").strip()


def check_videos(courses, issues):
    stats = {"embeds": 0, "instalments": 0}
    for c in courses:
        seen = {}
        for i, L in enumerate(c["lessons"], 1):
            v = L.get("video") or {}
            if not v.get("id"):
                continue
            stats["embeds"] += 1
            title, channel = v.get("title", ""), v.get("channel", "")
            num = instalment_number(title)
            is_course_channel = channel.strip().lower() in COURSE_CHANNELS
            if num is not None or is_course_channel:
                stats["instalments"] += 1
                why = []
                if num is not None:
                    why.append(f"numbered instalment {num}")
                if is_course_channel:
                    why.append(f"course channel {channel!r}")
                issues.append(("d", c["id"], i,
                               f"{'; '.join(why)} — {title[:64]!r}"))
            if num is not None:
                seen.setdefault(series_key(title, channel), []).append((i, num))
        for key, pairs in seen.items():
            if len(pairs) < 2:
                continue
            nums = [n for _, n in pairs]
            if nums != sorted(nums):
                inversions = [(pairs[a], pairs[b])
                              for a in range(len(pairs))
                              for b in range(a + 1, len(pairs))
                              if pairs[a][1] > pairs[b][1]]
                issues.append(
                    ("d-order", c["id"], 0,
                     f"series {key}: {len(pairs)} instalments, numbering does "
                     f"NOT rise with our lesson order "
                     f"({', '.join(f'L{l}=#{n}' for l, n in pairs)}) — "
                     f"{len(inversions)} inverted pair(s)"))
    return stats


# ---------------------------------------------------------------- driver
def run(root=Path("."), content_files=None):
    courses = curriculum(root)
    amap = alias_map(courses)
    issues = []
    files = content_files or sorted((root / "data/content").glob("*.json"))
    for f in files:
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        cid = re.sub(r"^y\ds\d-", "", Path(f).stem)
        check_declared_forward(cid, data, issues)
        check_undeclared_forward(cid, data, issues)
        check_cross_course(cid, data, courses, amap, issues)
    stats = check_videos(courses, issues)
    return issues, stats


def main():
    issues, stats = run()
    by_kind = {}
    for kind, cid, lid, msg in issues:
        by_kind.setdefault(kind, []).append((cid, lid, msg))
    labels = {"a": "(a) declared forward reference",
              "b": "(b) undeclared forward reference",
              "c": "(c) cross-course prerequisite direction",
              "d": "(d) video is a series instalment",
              "d-order": "(d) series numbering out of order"}
    for kind in ("a", "b", "c", "d", "d-order"):
        rows = by_kind.get(kind, [])
        print(f"\n=== {labels[kind]}: {len(rows)} finding(s)")
        for cid, lid, msg in rows:
            print(f"  {cid} L{lid}: {msg}")
    print(f"\nembeds scanned: {stats['embeds']}, "
          f"series instalments: {stats['instalments']}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
