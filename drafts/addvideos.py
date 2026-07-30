"""Verify candidate YouTube ids live, then write them into a course's lessons.

Usage:  python3 addvideos.py <sem> <course-id> L01=ID L02=ID ...
        python3 addvideos.py --check L01=ID ...      (verify only, write nothing)

Integrity rules this enforces, per CLAUDE.md:
  * an id is only written after oEmbed returns HTTP 200 for it
  * title and channel are copied from the oEmbed response, never typed
  * a candidate that fails verification is reported and SKIPPED, never guessed
Verification goes through curl: this machine's Python trust store fails every
youtube.com request with CERTIFICATE_VERIFY_FAILED, which is a local problem and
says nothing about the video.
"""
import json
import pathlib
import subprocess
import sys
import time
import urllib.parse

PACE = 2.0   # seconds between requests, to stay well clear of rate limiting


def oembed(vid):
    url = ("https://www.youtube.com/oembed?url="
           + urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}", safe="")
           + "&format=json")
    r = subprocess.run(["curl", "-sS", "--max-time", "25",
                        "-w", "\n%{http_code}", url],
                       capture_output=True, text=True)
    parts = r.stdout.rsplit("\n", 1)
    if len(parts) != 2 or parts[1].strip() != "200":
        return None, (parts[1].strip() if len(parts) == 2 else "no-response")
    try:
        return json.loads(parts[0]), "200"
    except json.JSONDecodeError:
        return None, "bad-json"


def main(argv):
    check_only = argv[1] == "--check"
    pairs_at = 2 if check_only else 3
    if not check_only:
        sem, cid = argv[1], argv[2]
    pairs = []
    for a in argv[pairs_at:]:
        k, v = a.split("=", 1)
        pairs.append((int(k.lstrip("Ll")), v))

    ok, bad = {}, []
    for i, (n, vid) in enumerate(pairs):
        d, code = oembed(vid)
        if d:
            ok[n] = {"id": vid, "title": d["title"],
                     "channel": d["author_name"], "verified": True}
            print(f"  L{n:02d}  {vid}  OK   [{d['author_name']}] {d['title'][:62]}")
        else:
            bad.append((n, vid, code))
            print(f"  L{n:02d}  {vid}  FAIL ({code}) — skipped, not written")
        if i < len(pairs) - 1:
            time.sleep(PACE)

    if check_only:
        print(f"\n{len(ok)} verified, {len(bad)} failed")
        return 1 if bad else 0

    p = pathlib.Path(f"data/{sem}.json")
    raw = p.read_text(encoding="utf-8")
    data = json.loads(raw)
    fmt = next(((i, t) for i in (1, 2, 4) for t in ("", "\n")
                if json.dumps(data, indent=i, ensure_ascii=False) + t == raw), None)
    assert fmt, f"{p}: unrecognised JSON formatting, refusing to rewrite"
    indent, tail = fmt

    course = next(c for c in data["courses"] if c["id"] == cid)
    written = 0
    for les in course["lessons"]:
        if les["n"] in ok:
            les["video"] = ok[les["n"]]
            written += 1
    p.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + tail,
                 encoding="utf-8")
    have = sum(1 for l in course["lessons"] if isinstance(l.get("video"), dict))
    print(f"\n{cid}: wrote {written}, now {have}/{len(course['lessons'])} "
          f"lessons have a verified video")
    if bad:
        print(f"STILL MISSING: {', '.join('L%02d' % n for n, _, _ in bad)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
