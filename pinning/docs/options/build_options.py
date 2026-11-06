"""build_options.py — side-by-side option documents for choosing between versions of the paper.

    python3 -B build_options.py ROWS.json OUT_DIR [--aux-original main.aux] [--aux-rewrite main_rewrite.aux]

A rows file holds one part (structure, the model at three levels, or a part of the text). Each row is one topic;
its options are the versions of that topic, printed side by side in landscape (one to three columns, four for
structure layouts). A row with a single option gets a comment column instead. Options whose text is identical are
merged into one cell, so identical text is never printed twice.

An option's text is either written out ("tex") or extracted verbatim from a version of the paper ("src"):
  {"doc": "original", "lines": [a, b]}                 main.tex lines a..b (one paragraph per line there)
  {"doc": "rewrite", "anchor": "first words", "blocks": n}   n LaTeX paragraphs of main_rewrite.tex from the one
                                                        that starts with the anchor (comments stripped first)
  {"doc": "rewrite", "anchor": "...", "until": "..."}  from the anchor up to, not including, the paragraph that
                                                        starts with "until"
Extracted text keeps its words; only its LaTeX is adapted for narrow columns: cross-references print the version's
own numbers (from its .aux), theorem-like environments print with their numbers, displays shrink to the column,
figures and tables keep their captions.

Rows file:
  {"part": "...", "title": "...", "subtitle": "...", "preface": "LaTeX, full width",
   "columns": "how to read the columns", "rows": [
     {"id": "T.1.1", "title": "Opening", "diff": "one line: how the options differ",
      "reason": "for a single option: can't change | loved | no better idea yet",
      "options": [{"key": "R", "label": "Rewrite", "where": "§1 ¶1", "src": {...}} | {"key": "N1", ..., "tex": "..."}]
     }]}
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = HERE.parents[1]                      # pinning/
PAPER = PIN / "paper"


# ----------------------------------------------------------------------------------------------- sources
def read(p):
    return Path(p).read_text(encoding="utf-8")


def strip_comments(s):
    s = re.sub(r"(?m)^[ \t]*(?<!\\)%.*\n", "", s)
    return re.sub(r"(?<!\\)%.*", "", s)


def norm(s):
    return re.sub(r"\s+", " ", s.replace("~", " ")).strip()


def load_aux(path):
    m = {}
    if path and Path(path).exists():
        for x in re.finditer(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", read(path)):
            m[x.group(1)] = x.group(2)
    return m


class Sources:
    def __init__(self, aux_original, aux_rewrite):
        self.orig_lines = read(PAPER / "main.tex").split("\n")
        rew = strip_comments(read(PAPER / "main_rewrite.tex"))
        body = rew.split("\\begin{document}", 1)[1]
        self.rew_blocks = [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]
        self.aux = {"original": load_aux(aux_original), "rewrite": load_aux(aux_rewrite)}

    def get(self, src):
        doc = src["doc"]
        if doc == "original":
            a, b = src["lines"]
            return "\n".join(self.orig_lines[a - 1:b]), "original"
        if doc == "rewrite":
            anc = norm(src["anchor"])
            idx = [i for i, b in enumerate(self.rew_blocks) if norm(b).startswith(anc)]
            if len(idx) != 1:
                raise SystemExit(f"rewrite anchor matches {len(idx)} paragraphs: {src['anchor'][:70]!r}")
            i = idx[0]
            if "until" in src:
                u = norm(src["until"])
                j = next((k for k in range(i + 1, len(self.rew_blocks)) if norm(self.rew_blocks[k]).startswith(u)), None)
                if j is None:
                    raise SystemExit(f"rewrite 'until' anchor not found after {src['anchor'][:50]!r}: {src['until'][:50]!r}")
                blocks = self.rew_blocks[i:j]
            else:
                blocks = self.rew_blocks[i:i + int(src.get("blocks", 1))]
            return "\n\n".join(blocks), "rewrite"
        raise SystemExit(f"unknown doc {doc!r}")


# ----------------------------------------------------------------------------------------------- conversion
THM = {"proposition": "Proposition", "lemma": "Lemma", "theorem": "Theorem", "corollary": "Corollary",
       "assumption": "Assumption", "definition": "Definition", "remark": "Remark"}
DISPLAY_ENVS = ["equation", "equation*", "align", "align*", "gather", "gather*", "multline", "multline*"]


def balanced(s, i):
    """s[i] == '{'; return the index just after the matching '}'."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return j + 1
    raise ValueError("unbalanced braces")


def convert(tex, aux):
    s = strip_comments(tex)

    def num(label):
        return aux.get(label, "??")

    # sections and subsections: print their number in this version
    def sec(m):
        lab = re.search(r"\\label\{([^}]*)\}", m.group(0))
        n = num(lab.group(1)) if lab else ""
        return f"\\optsec{{{n}}}{{{m.group(2)}}}"
    s = re.sub(r"\\(section|subsection|subsubsection)\*?\{([^{}]*)\}(\\label\{[^}]*\})?", sec, s)

    # figures
    def fig(m):
        body = m.group(1)
        g = re.search(r"\\includegraphics(\[[^\]]*\])?\{([^}]*)\}", body)
        lab = re.search(r"\\label\{([^}]*)\}", body)
        c = body.find("\\caption{")
        cap = body[c + 9:balanced(body, c + 8) - 1] if c >= 0 else ""
        cap = re.sub(r"\\label\{[^}]*\}", "", cap)
        return f"\\optfig{{{g.group(2) if g else ''}}}{{Figure {num(lab.group(1)) if lab else ''}}}{{{cap}}}"
    s = re.sub(r"\\begin\{figure\}(?:\[[^\]]*\])?(.*?)\\end\{figure\}", fig, s, flags=re.S)

    # tables
    def tab(m):
        body = m.group(1)
        lab = re.search(r"\\label\{([^}]*)\}", body)
        c = body.find("\\caption{")
        cap = body[c + 9:balanced(body, c + 8) - 1] if c >= 0 else ""
        if c >= 0:
            body = body[:c] + body[balanced(body, c + 8):]
        body = re.sub(r"\\label\{[^}]*\}|\\centering", "", body)
        return f"\\opttab{{Table {num(lab.group(1)) if lab else ''}}}{{{cap}}}{{{body.strip()}}}"
    s = re.sub(r"\\begin\{table\}(?:\[[^\]]*\])?(.*?)\\end\{table\}", tab, s, flags=re.S)

    # displays
    def disp(m):
        env, body = m.group(1), m.group(2)
        labs = re.findall(r"\\label\{([^}]*)\}", body)
        body = re.sub(r"\\label\{[^}]*\}|\\nonumber|\\notag", "", body).strip()
        if env.startswith("align"):
            body = f"\\begin{{aligned}}{body}\\end{{aligned}}"
        elif env.startswith("gather"):
            body = f"\\begin{{gathered}}{body}\\end{{gathered}}"
        elif env.startswith("multline"):
            body = f"\\begin{{gathered}}{body}\\end{{gathered}}"
        tag = f"({num(labs[0])})" if labs and not env.endswith("*") else ""
        return f"\\optdisp{{{body}}}{{{tag}}}"
    envs = "|".join(re.escape(e) for e in DISPLAY_ENVS)
    s = re.sub(rf"\\begin\{{({envs})\}}(.*?)\\end\{{\1\}}", disp, s, flags=re.S)
    s = re.sub(r"\\\[(.*?)\\\]", lambda m: f"\\optdisp{{{m.group(1).strip()}}}{{}}", s, flags=re.S)

    # theorem-like environments
    def thm(m):
        env, title, rest = m.group(1), (m.group(2) or "")[1:-1] if m.group(2) else "", m.group(3) or ""
        lab = re.search(r"\\label\{([^}]*)\}", rest)
        n = num(lab.group(1)) if lab else ""
        name = THM[env] + (f" {n}" if n and n != "??" else "")
        return f"\\begin{{optthm}}{{{name}}}{{{title}}}"
    s = re.sub(r"\\begin\{(" + "|".join(THM) + r")\}(\[[^\]]*\])?((?:\s*\\label\{[^}]*\})?)", thm, s)
    s = re.sub(r"\\end\{(" + "|".join(THM) + r")\}", r"\\end{optthm}", s)

    # cross-references
    s = re.sub(r"\\eqref\{([^}]*)\}", lambda m: f"({num(m.group(1))})", s)
    s = re.sub(r"\\ref\{([^}]*)\}", lambda m: num(m.group(1)), s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    return s.strip()


# ----------------------------------------------------------------------------------------------- rendering
PREAMBLE = r"""\documentclass[9pt]{extarticle}
\usepackage[a4paper,landscape,left=1.1cm,right=1.1cm,top=1.6cm,bottom=1.3cm,headsep=0.4cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm,bm,graphicx,booktabs,array,adjustbox,paracol,xcolor,fancyhdr,longtable,microtype,enumitem}
\usepackage[hidelinks]{hyperref}
\graphicspath{{@PAPER@/}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.45em}
\setlength{\columnsep}{1.3em}
\setlength{\columnseprule}{0.3pt}
\def\columnseprulecolor{\color{black!30}}
\setlist{nosep,leftmargin=1.4em}
\definecolor{chip}{gray}{0.88}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.3pt}
\fancyhead[L]{\footnotesize\bfseries @HEADTITLE@}
\fancyhead[R]{\footnotesize @HEADRIGHT@}
\fancyfoot[C]{\footnotesize\thepage}
\newcommand{\rowhead}[3]{\par\vspace{0.9em}\noindent\rule{\linewidth}{0.6pt}\par\nopagebreak\vspace{0.15em}%
  \noindent{\large\bfseries #1\quad #2}\par\nopagebreak\noindent{\small\itshape #3}\par\nopagebreak\vspace{0.2em}}
\newcommand{\cell}[3]{\noindent\colorbox{chip}{\footnotesize\bfseries\strut #1}\ {\footnotesize\bfseries #2}%
  \hfill{\footnotesize\color{black!60}#3}\par\nopagebreak\vspace{0.2em}}
\newcommand{\optsec}[2]{\par\smallskip\noindent{\bfseries\ifx&#1&\else#1\enspace\fi#2}\par\nopagebreak}
\newcommand{\optdisp}[2]{\par\smallskip\noindent\makebox[\linewidth]{\hfil
  \adjustbox{max width=\dimexpr\linewidth-3.2em\relax}{$\displaystyle #1$}\hfil\llap{\footnotesize #2}}\par\smallskip}
\newcommand{\optfig}[3]{\par\smallskip\noindent\ifx&#1&\else\includegraphics[width=\linewidth]{#1}\par\fi
  {\footnotesize\textbf{#2.} #3}\par\smallskip}
\newcommand{\opttab}[3]{\par\smallskip\noindent{\footnotesize\textbf{#1.} #2}\par\noindent
  \adjustbox{max width=\linewidth}{\begin{minipage}{1.45\linewidth}#3\end{minipage}}\par\smallskip}
\newenvironment{optthm}[2]{\par\smallskip\noindent\textbf{#1}\ifx&#2&\else\ (#2)\fi.\ \itshape}{\par\smallskip}
\newcommand{\reason}[1]{\par\smallskip{\footnotesize\color{black!60}Same in every version: #1.}}
\newcommand{\commentcol}{\cell{}{Comments}{}}
\newcommand{\pickbox}{$\square$}
\begin{document}
"""


def esc(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")


def render_row(row, sources, parts_cells):
    opts = []
    for o in row["options"]:
        if "same_as" in o:
            continue
        if "src" in o:
            raw, doc = sources.get(o["src"])
            tex = convert(raw, sources.aux[doc])
        else:
            tex = o["tex"]
        opts.append(dict(o, text=tex))
    # an option that keeps another option's text unchanged points to it ("same_as") and joins its cell
    for o in row["options"]:
        if "same_as" in o:
            target = next((m for m in opts if m["key"] == o["same_as"] or m["key"].endswith("=" + o["same_as"])), None)
            if target is None:
                raise SystemExit(f"{row['id']}: option {o['key']} is same_as {o['same_as']}, which is not in the row")
            opts.append(dict(target, key=o["key"], label=o["label"], where=o.get("where", ""), text=target["text"]))
    # merge options with identical text
    merged = []
    for o in opts:
        same = next((m for m in merged if norm(m["text"]) == norm(o["text"])), None)
        if same:
            same["key"] += "=" + o["key"]
            same["label"] += " = " + o["label"]
            same["where"] = "; ".join(x for x in (same.get("where", ""), o.get("where", "")) if x)
        else:
            merged.append(dict(o))
    rid = row["id"]
    out = [f"\\rowhead{{{rid}}}{{{row['title']}}}{{{row.get('diff', '')}}}"]
    n = len(merged)
    if n == 1:
        out += ["\\columnratio{0.64}", "\\begin{paracol}{2}"]
    elif n == 2:
        out += ["\\columnratio{0.5}", "\\begin{paracol}{2}"]
    elif n == 3:
        out += ["\\columnratio{0.333,0.333}", "\\begin{paracol}{3}"]
    else:
        r = round(1 / n, 3)
        out += ["\\columnratio{" + ",".join([str(r)] * (n - 1)) + "}", f"\\begin{{paracol}}{{{n}}}"]
    for k, o in enumerate(merged):
        if k:
            out.append("\\switchcolumn")
        out.append(f"\\cell{{{rid}-{o['key']}}}{{{o['label']}}}{{{o.get('where', '')}}}")
        out.append(o["text"])
        if n == 1 and row.get("reason"):
            out.append(f"\\reason{{{row['reason']}}}")
    if n == 1:
        out += ["\\switchcolumn", "\\commentcol"]
    out.append("\\end{paracol}")
    parts_cells.append((rid, row["title"], [o["key"] for o in merged]))
    return "\n".join(out)


def build(rows_path, out_dir, aux_original=None, aux_rewrite=None):
    spec = json.loads(read(rows_path))
    sources = Sources(aux_original, aux_rewrite)
    pre = PREAMBLE.replace("@PAPER@", str(PAPER)).replace("@HEADTITLE@", spec["title"]).replace(
        "@HEADRIGHT@", spec.get("headright", "Options side by side; each cell's ID is in its corner"))
    body = [pre]
    body.append("{\\LARGE\\bfseries " + spec["title"] + "}\\par\\smallskip")
    if spec.get("subtitle"):
        body.append("{\\large " + spec["subtitle"] + "}\\par\\medskip")
    if spec.get("preface"):
        body.append(spec["preface"] + "\\par")
    cells = []
    for row in spec["rows"]:
        if row.get("section"):
            body.append("\\par\\vspace{1.2em}\\noindent{\\Large\\bfseries " + row["section"] + "}\\par")
            if not row.get("options"):
                continue
        body.append(render_row(row, sources, cells))
    # pick sheet
    body.append("\\clearpage\\section*{Pick sheet}")
    body.append("{\\small Tick the option to keep in each row; write a combination in the notes "
                "(e.g.\\ ``R, with O's last sentence'').}\\par\\medskip")
    body.append("\\begin{longtable}{@{}p{1.6cm}p{8.4cm}p{6.6cm}p{8.2cm}@{}}\\toprule")
    body.append("Row & Topic & Options & Notes\\\\\\midrule\\endhead")
    for rid, title, keys in ([(p["id"], p["title"], p["keys"]) for p in spec["pick_rows"]]
                             if spec.get("pick_rows") else cells):
        boxes = "\\quad ".join(f"\\pickbox\\ {k}" for k in keys)
        body.append(f"{rid} & {title} & {boxes} & \\\\[1.1em]")
    body.append("\\bottomrule\\end{longtable}")
    body.append("\\end{document}")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(rows_path).stem
    tex_path = out_dir / f"{stem}.tex"
    tex_path.write_text("\n\n".join(body), encoding="utf-8")
    r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
                       cwd=out_dir, capture_output=True, text=True)
    log = (out_dir / f"{stem}.log").read_text(encoding="utf-8", errors="replace") if (out_dir / f"{stem}.log").exists() else ""
    errs = re.findall(r"^! .*", log, flags=re.M)
    over = re.findall(r"Overfull \\hbox \((\d+\.\d+)pt", log)
    pages = re.search(r"Output written on .*?\((\d+) pages?", log)
    print(f"{tex_path.with_suffix('.pdf')}: exit {r.returncode}, pages {pages.group(1) if pages else '?'}, "
          f"errors {len(errs)}, overfull boxes {len(over)} (max {max(map(float, over)) if over else 0:.1f}pt)")
    for e in errs[:5]:
        print("  ", e)
    return r.returncode


if __name__ == "__main__":
    args = sys.argv[1:]
    kw = {}
    for flag, key in (("--aux-original", "aux_original"), ("--aux-rewrite", "aux_rewrite")):
        if flag in args:
            i = args.index(flag)
            kw[key] = args[i + 1]
            del args[i:i + 2]
    sys.exit(build(args[0], args[1], **kw))
