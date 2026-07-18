# OWNER'S MANUAL — editing Nexus content yourself

Companion to **[PROJECT_MAP.md](PROJECT_MAP.md)** (which files are safe). This manual
covers *how* to edit the safe ones without breaking the Nexus site.

---

## 0 · The five golden rules

1. **Never rename or move a file.** Names are wiring. Edit contents only.
2. **Never edit anything inside `docs/`.** It is generated; the next build erases your
   change. All edits go in `data/` or `content/`, then you rebuild.
3. **Nothing goes live until you push.** You can experiment freely — the live site only
   changes at step "push" (section 2). If a build fails, the site is untouched.
4. **The build is your bodyguard.** `python3 nexus_build.py` re-checks every page. If it
   prints an error instead of the summary, it *refused to build* — read the message, fix,
   rerun. Never push after a failed build.
5. **Integrity gates are content law.** No company names inside lessons (career blocks
   are the one exception). No invented numbers — every quiz answer was machine-verified;
   keep it that way. No YouTube video that isn't from the approved channel list and
   personally verified to exist. When unsure, leave a TODO instead of guessing.

---

## 1 · What you need (one-time)

A Mac Terminal at the project folder:

```bash
cd "/Users/ilmshri/Social Media/nexus-institute"
```

Python 3 and git are already installed and configured (the push credential is in your
keychain). There is nothing to install.

---

## 2 · The edit cycle (always the same five steps)

```bash
# 1. edit a green file (see templates below)

# 2. rebuild the site
python3 nexus_build.py
#    success looks like:   NEXUS build <hash>
#                          pages: 579 | search index: 528 | embeds: 102
#                          coverage: 74/528 lessons at full depth (14%)
#    an error (long "AssertionError: ...") means: nothing was deployed,
#    fix the file and rerun.

# 3. preview on your own machine (optional but recommended)
python3 -m http.server -d docs 8000
#    then open http://localhost:8000 in your browser. Ctrl+C stops it.

# 4. save a checkpoint
git add -A
git commit -m "describe what you changed"

# 5. publish
git push origin main
#    this one command pushes to BOTH Nexus repos: the code home
#    (ilmshri/Nexus-Institute-of-Technology) and the live-site repo
#    (nexuskw/nexuskw.github.io). The live site updates ~1 minute later.
```

---

## 3 · Editing lessons — `data/content/y1s1-<course>.json`

Each course file is one JSON object: lesson numbers (`"1"`…`"11"`) → three parts.

```json
"9": {
  "lecture":     "<h3>§1 · Title</h3><p>…</p> … <h3>§4 · …</h3><p>…</p>",
  "foundations": "<h4>What this lesson assumes</h4>…<table class=\"glossary\">…",
  "quiz":        [ eight items: 3 "solve" + 5 "mc", templates below ]
}
```

**JSON survival kit** (the three mistakes that cause 95% of failures):
- Every `"` inside text must be written `\"`.
- Items in a list are separated by commas — but there is **no comma after the last one**.
- Check yourself before building: `python3 -m json.tool data/content/y1s1-computing.json`
  — prints the file if valid, or points at the exact broken line.

**House style constraints** (the build and the ledger enforce these):
- Lecture: 500–1000 words, four sections headed `<h3>§1 · …</h3>` … `<h3>§4 · …</h3>`
  (the build converts `§1` to `01` automatically — type it with `§` in the source).
- Foundations: the glossary must be a `<table class="glossary">` with columns
  *Term | Equation | When to use*.
- Math notation: `\\( … \\)` around LaTeX, e.g. `\\( F = ma \\)`.
- **No company names anywhere in these files.** Use "a steel mill", "a dairy filling
  hall", "a fabrication yard".

### Quiz item templates (copy, fill, keep the order 3 solves then 5 MCs)

**Solve** (student works it, then reveals your worked solution):
```json
{
  "type": "solve",
  "q": "<p class=\"qname\"><b>Short problem name</b></p><p><b>Problem.</b> …</p>",
  "solution": "<p><b>Solution.</b> (1) … (2) …</p><p><b>Answer:</b> … <b>Sanity check:</b> …</p>"
}
```

**Multiple choice** (`"answer"` counts from 0: first choice = 0, second = 1, …):
```json
{
  "type": "mc",
  "q": "<p>The question?</p>",
  "choices": ["Right answer", "Classic mistake", "Classic mistake", "Classic mistake"],
  "answer": 0,
  "solution": "<p>Why the right one is right and what mistake each wrong one represents.</p>"
}
```

**Arithmetic rule:** any number appearing in a solution must be checked by an actual
calculation first (calculator or a 3-line Python check), never typed from memory. The
platform's credibility is these numbers.

---

## 4 · Editing the catalog — `data/y1s1.json` … `data/y4s2.json`

Safe to edit (plain text, shown on pages):
- course `"title"`, `"summary"`, `"taught_from"`
- per-course `"career"` — the *only* place company names are allowed
- lesson `"t"` (title), `"scope"`, `"preview"` questions

**Leave alone** even though they sit in the same file:
- `"id"` (folder name of the course — wiring), `"code"`, lesson `"n"`, `"tier"`,
  `"core60"`, `"content"` (points to a fragment file by name), `"kuwait"`
- `"video"` — every entry was individually verified against YouTube and the approved
  channel list. **Never type in a YouTube ID by hand**; a broken or wrong video is worse
  than the honest "no video yet" marker (`"video": "none"`).

## 5 · Editing pages — `content/pages/`

`mission.html`, `career.html`, `career-ar.html` are ordinary HTML text — edit wording
freely, keep the existing tags around it. The career pages may name companies. The
Arabic file must keep formulas/numbers inside `<span dir="ltr">…</span>` wrappers so
mixed lines don't flip.

---

## 6 · When something goes wrong

| Symptom | Meaning | Fix |
|---|---|---|
| `json.decoder.JSONDecodeError: … line 213` | Broken JSON (comma/quote) | Open the file at that line; run the `json.tool` check above |
| `AssertionError: section sign leaked …` | A `§` ended up somewhere the transform doesn't cover | Remove the stray `§` from the file named in the message |
| `AssertionError: lesson video failed approval gate` | A video entry names an unapproved channel | Restore the previous `"video"` value |
| Build succeeds but a page looks wrong | Content mistake, not structure | Fix the text, rebuild, refresh |

**Undo — your safety net (nothing is ever lost):**
```bash
git checkout -- path/to/file.json   # discard your uncommitted edits to that file
git log --oneline -10               # see recent checkpoints
git revert <commit>                 # undo a bad checkpoint that was already pushed
```
If you're ever unsure, stop before `git push` — the live site cannot be hurt by
anything you do locally.

---

## 7 · What to hand back to a working session instead of doing yourself

- Adding **new courses/lessons** (needs the verified-arithmetic pipeline)
- Anything in `nexus_build.py`, `build.py`, `assets/nx/`
- **Video additions** (need oEmbed verification against the approved list)
- Design/layout changes (pending your visual-style decision)
- Promoting anything from `drafts/` (unverified numbers)
