"""
build_submission_em.py — the Economic Modelling submission (double-anonymized review), built from paper/main.tex
and the editable sources in paper/submission/em_src/.

Outputs, in paper/submission/em/:
  manuscript.tex           the anonymized LaTeX source: no authors, affiliations, emails, title footnotes or date;
                           everything else verbatim; figures point at the files beside it
  Figure_1.pdf ... Figure_7.pdf, Figure_D1.pdf
                           the script-built figures, named by their printed numbers (appendix figures by appendix)
  title_page.docx          from em_src/title_page.md: title, authors, affiliations with postal addresses, the
                           corresponding author, the views disclaimer, acknowledgments, competing interests, funding
  highlights.docx          from em_src/highlights.md (3-5 bullets, at most 85 characters each)
  cover_letter.docx        from em_src/cover_letter.md
  manuscript_preview.pdf   the anonymized manuscript compiled here, to look at; not for upload (the journal takes
                           .tex or .docx as source files)

The build stops before writing if: an identifying string (an author's name, an email, an affiliation, the repository
or SSRN address) survives in the anonymized source or in the preview's text and metadata; a figure is missing or
referenced other than once; the abstract exceeds 250 words; there are not 1-7 keywords; the highlights are not 3-5
bullets of at most 85 characters.

Needs pdflatex (latexmk) and pandoc on the path. Run from pinning/:  python3 code/build_submission_em.py
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
SRC = PAPER / "main.tex"
FRONT = PAPER / "submission" / "em_src"
OUT = PAPER / "submission" / "em"

IDENTIFYING = ["Båge", r"B\r{a}ge", "Bage", "Wilson", "Stella", "Johan", "hhs.se", "kth.se", "thmwi", "KTH", "SEB",
               "Skandinaviska", "Stockholm School", "wilsoniumite", "github", "7226858", "ssrn", "SSRN"]


def match_brace(s, i):
    """Index just past the group that opens at s[i] == '{'."""
    depth = 0
    for j in range(i, len(s)):
        depth += {"{": 1, "}": -1}.get(s[j], 0)
        if depth == 0:
            return j + 1
    raise ValueError("unbalanced braces")


def strip_thanks(s):
    """Remove every \\thanks{...} (balanced braces)."""
    while (i := s.find(r"\thanks{")) >= 0:
        s = s[:i] + s[match_brace(s, i + len(r"\thanks")):]
    return s


def anonymize(tex):
    pre, body = tex.split(r"\begin{document}", 1)
    i = pre.index(r"\title{")
    j = match_brace(pre, i + len(r"\title"))
    pre = pre[:i] + strip_thanks(pre[i:j]) + pre[j:]
    i = pre.index(r"\author{")
    j = match_brace(pre, i + len(r"\author"))
    pre = pre[:i] + r"\author{}" + pre[j:]
    pre = re.sub(r"\\date\{[^}]*\}", r"\\date{}", pre)
    # the header comments name the repository files and history: drop the comment lines of the preamble
    pre = "\n".join(line for line in pre.split("\n") if not line.lstrip().startswith("%")) + "\n"
    return pre + r"\begin{document}" + body


def rename_figures(tex):
    """figures/fig_*.pdf -> Figure_<printed number>.pdf: main-text figures 1, 2, ...; appendix figures by appendix letter
    and their number within it (Figure_D1). Returns the new source and {new name: source file}."""
    body_start = tex.index(r"\begin{document}")
    appendix_at = tex.index(r"\appendix")
    files, n_main, out, pos = {}, 0, [], 0
    for m in re.finditer(r"\\includegraphics(\[[^\]]*\])?\{(figures/[^}]+\.pdf)\}", tex):
        if m.start() < body_start:
            continue
        if m.start() < appendix_at:
            n_main += 1
            name = f"Figure_{n_main}.pdf"
        else:
            sections = len(re.findall(r"\\section\{", tex[appendix_at:m.start()]))
            letter = chr(ord("A") + sections - 1)
            k = 1 + sum(1 for f in files if f.startswith(f"Figure_{letter}"))
            name = f"Figure_{letter}{k}.pdf"
        files[name] = PAPER / m.group(2)
        out.append(tex[pos:m.start()] + rf"\includegraphics{m.group(1) or ''}{{{name}}}")
        pos = m.end()
    out.append(tex[pos:])
    return "".join(out), files


def abstract_words(tex):
    a = tex[tex.index(r"\begin{abstract}") + len(r"\begin{abstract}"):tex.index(r"\end{abstract}")]
    a = re.sub(r"\\[A-Za-z]+", " ", a).replace("--", "-")
    return len(a.split())


def keywords(tex):
    m = re.search(r"\\textbf\{Keywords:\}(.*?)\\\\", tex)
    return [k.strip() for k in m.group(1).split(";")] if m else []


def highlights():
    lines = [l[2:].rstrip("\n") for l in (FRONT / "highlights.md").read_text(encoding="utf-8").splitlines()
             if l.startswith("- ")]
    return lines


def identifying_hits(text):
    return sorted({t for t in IDENTIFYING if t in text})


def main():
    tex = SRC.read_text(encoding="utf-8")
    anon, figs = rename_figures(anonymize(tex))
    problems = []
    hits = identifying_hits(anon)
    if hits:
        problems.append(f"identifying strings in manuscript.tex: {hits}")
    for name, src in figs.items():
        if not src.exists():
            problems.append(f"missing figure {src}")
        if anon.count("{" + name + "}") != 1:
            problems.append(f"{name} referenced {anon.count('{' + name + '}')} times")
    if abstract_words(tex) > 250:
        problems.append(f"abstract has {abstract_words(tex)} words (limit 250)")
    if not 1 <= len(keywords(tex)) <= 7:
        problems.append(f"{len(keywords(tex))} keywords (1-7 required)")
    hl = highlights()
    if not 3 <= len(hl) <= 5 or any(len(h) > 85 for h in hl):
        problems.append(f"highlights: {len(hl)} bullets, lengths {[len(h) for h in hl]} (3-5, at most 85)")
    if problems:
        sys.exit("BLOCKED:\n  " + "\n  ".join(problems))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "manuscript.tex").write_text(anon, encoding="utf-8")
        for name, src in figs.items():
            shutil.copy(src, tmp / name)
        r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "manuscript.tex"],
                           cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("BLOCKED: the anonymized manuscript does not compile\n" + r.stdout[-2000:])
        log = (tmp / "manuscript.log").read_text(errors="replace")
        if re.search(r"undefined (references|citations)|Reference .* undefined", log):
            sys.exit("BLOCKED: undefined references in the anonymized manuscript")
        text = subprocess.run(["pdftotext", "manuscript.pdf", "-"], cwd=tmp, capture_output=True, text=True).stdout
        info = subprocess.run(["pdfinfo", "manuscript.pdf"], cwd=tmp, capture_output=True, text=True).stdout
        hits = identifying_hits(text + info)
        if hits:
            sys.exit(f"BLOCKED: identifying strings in the compiled manuscript or its metadata: {hits}")
        pages = re.search(r"Pages:\s+(\d+)", info).group(1)
        if OUT.exists():
            shutil.rmtree(OUT)
        OUT.mkdir(parents=True)
        shutil.copy(tmp / "manuscript.tex", OUT / "manuscript.tex")
        shutil.copy(tmp / "manuscript.pdf", OUT / "manuscript_preview.pdf")
        for name in figs:
            shutil.copy(tmp / name, OUT / name)

    for doc in ("title_page", "highlights", "cover_letter"):
        subprocess.run(["pandoc", str(FRONT / f"{doc}.md"), "-f", "markdown", "-o", str(OUT / f"{doc}.docx")], check=True)
    print(f"wrote {OUT}: manuscript.tex ({pages} pages compiled), {len(figs)} figures ({', '.join(figs)}), "
          f"title_page.docx, highlights.docx, cover_letter.docx")
    print(f"  abstract {abstract_words(tex)} words; {len(keywords(tex))} keywords; highlights {[len(h) for h in hl]} characters")


if __name__ == "__main__":
    main()
