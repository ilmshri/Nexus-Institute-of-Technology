"""Y1S1 notation audit v2 (Part 3) — find symbols that are NEVER DEFINED.

v1 flagged "symbol appears in a display equation before appearing inline".
Reading the hits showed that is mostly noise: "equation, then \\( A \\) the
atomic weight, \\( V_C \\) the cell volume" is standard, clear technical
writing, and the plan's actual concern is *undefined* constants -- symbols the
prose never explains at all.

So v2 asks the question that matters: for each quantity symbol used in a
lesson's lecture, does the prose anywhere define it?

A symbol counts as DEFINED at an occurrence if, immediately around that
occurrence, the text reads like a definition:
  - "\\( A \\) the atomic weight"      -> article/noun right after
  - "\\( \\rho \\) is the density"     -> copula right after
  - "the density \\( \\rho \\)"        -> noun phrase right before
  - "where \\( x \\) ..."              -> explicit where-clause
Subscripts are stripped (V_C and N_A are V and N -- one symbol, not three),
because the definition line names the subscripted form and the base is what
carries the meaning.

Output is a reading list, not a verdict: every hit still gets read in context.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/ilmshri/Social Media/nexus-institute")
CONTENT = ROOT / "data" / "content"

NOT_SYMBOLS = {
    "frac", "dfrac", "tfrac", "sqrt", "left", "right", "big", "Big", "bigg", "Bigg",
    "begin", "end", "tag", "label", "text", "mathrm", "mathbf", "mathit", "mathcal",
    "operatorname", "displaystyle", "limits", "nolimits", "quad", "qquad",
    "hspace", "vspace", "newline", "cases", "aligned", "align", "array", "matrix",
    "pmatrix", "bmatrix", "vmatrix", "substack", "overline", "underline", "hat", "bar",
    "vec", "dot", "ddot", "tilde", "widehat", "widetilde", "boxed", "phantom",
    "cdot", "times", "div", "pm", "mp", "approx", "sim", "simeq", "cong", "equiv",
    "propto", "neq", "leq", "geq", "ll", "gg", "to", "rightarrow", "leftarrow",
    "Rightarrow", "Leftarrow", "leftrightarrow", "mapsto", "infty", "partial",
    "nabla", "sum", "prod", "int", "iint", "iiint", "oint", "lim", "max", "min",
    "log", "ln", "exp", "sin", "cos", "tan", "sec", "csc", "cot", "sinh", "cosh",
    "tanh", "arcsin", "arccos", "arctan", "det", "dim", "deg", "gcd", "bmod", "pmod",
    "in", "notin", "subset", "supset", "cup", "cap", "emptyset", "forall", "exists",
    "cdots", "ldots", "dots", "vdots", "ddots", "prime", "circ", "ast", "star",
    "colon", "mid", "parallel", "perp", "angle", "triangle", "square",
    "textrm", "textbf", "textit", "mbox", "hfill", "space", "thinspace",
    "Sigma", "le", "ge", "lt", "gt", "ne", "xrightarrow", "xleftarrow",
    "texttt", "pi", "circ", "degree", "infty",
    "longrightarrow", "implies", "iff", "because", "therefore", "cdotp",
}

MATH_RE = re.compile(r"\\\((.+?)\\\)|\\\[(.+?)\\\]", re.S)
TAG_RE = re.compile(r"\\tag\{[^}]*\}")
WORD_RE = re.compile(r"\\(?:mathrm|text|textrm|texttt|mbox|operatorname)\s*\{[^{}]*\}")
SUB_RE = re.compile(r"_\{[^{}]*\}|_[A-Za-z0-9]")
CMD_RE = re.compile(r"\\([A-Za-z]+)")
LETTER_RE = re.compile(r"(?<![A-Za-z\\])([A-Za-z])(?![A-Za-z])")

# definition cues in the text immediately FOLLOWING a symbol
AFTER_RE = re.compile(
    r"^[\s,)]*(?:is|are|was|denotes?|means?|gives?|measures?|represents?|"
    r"the|a|an|its|their)\b", re.I)
# a noun phrase immediately PRECEDING a symbol ("the cell volume \( V_C \)")
BEFORE_RE = re.compile(r"(?:the|a|an|each|every|its)\s+[a-z][a-z\-']*"
                       r"(?:\s+[a-z][a-z\-']*){0,3}[\s,]*$", re.I)
WHERE_RE = re.compile(r"\bwhere\b[^.]{0,40}$", re.I)


def base_symbols(expr):
    e = TAG_RE.sub(" ", expr)
    e = WORD_RE.sub(" ", e)
    e = SUB_RE.sub("", e)                     # V_C -> V, N_A -> N
    out = set()
    for cmd in CMD_RE.findall(e):
        if cmd not in NOT_SYMBOLS and len(cmd) > 1:
            out.add("\\" + cmd)
    for ch in LETTER_RE.findall(CMD_RE.sub(" ", e)):
        out.add(ch)
    return out


def analyse(lec):
    """-> {symbol: {'defined': bool, 'n': int, 'first_ctx': str}}"""
    plain = html.unescape(re.sub(r"<[^>]+>", "", lec))
    info = {}
    for m in MATH_RE.finditer(plain):
        expr = m.group(1) if m.group(1) is not None else m.group(2)
        before = plain[max(0, m.start() - 90):m.start()]
        after = plain[m.end():m.end() + 90]
        looks_defined = bool(AFTER_RE.match(after) or BEFORE_RE.search(before)
                             or WHERE_RE.search(before))
        for s in base_symbols(expr):
            rec = info.setdefault(s, {"defined": False, "n": 0, "first_ctx": ""})
            rec["n"] += 1
            if not rec["first_ctx"]:
                rec["first_ctx"] = (before[-45:] + "⟦" + expr.strip()[:28] + "⟧"
                                    + after[:45]).replace("\n", " ")
            if looks_defined:
                rec["defined"] = True
    return info


def main():
    courses = sys.argv[1:] or ["math-1", "statics", "materials-1",
                               "physics-1", "computing", "drawing-cad"]
    grand = 0
    for cid in courses:
        data = json.loads((CONTENT / f"y1s1-{cid}.json").read_text(encoding="utf-8"))
        hits_here = 0
        print("=" * 78)
        print(f"COURSE {cid}")
        print("=" * 78)
        for n in sorted(data, key=lambda k: int(k)):
            lec = data[n].get("lecture")
            if not isinstance(lec, str) or not lec.strip():
                continue
            info = analyse(lec)
            undef = {s: r for s, r in info.items() if not r["defined"]}
            if not undef:
                continue
            print(f"  L{int(n):02d}  ({len(info)} symbols, {len(undef)} never defined)")
            for s, r in sorted(undef.items(), key=lambda kv: -kv[1]["n"]):
                print(f"      {s:<10} x{r['n']:<3} …{r['first_ctx']}…")
                hits_here += 1
        print(f"  --> {cid}: {hits_here} never-defined symbols\n")
        grand += hits_here
    print(f"TOTAL never-defined symbols across audited courses: {grand}")


if __name__ == "__main__":
    main()
