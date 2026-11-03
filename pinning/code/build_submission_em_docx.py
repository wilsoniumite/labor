"""
build_submission_em_docx.py — the Word version of the anonymized Economic Modelling manuscript.

Input:  paper/submission/em/manuscript.tex and the Figure_*.pdf files beside it, as build_submission_em.py writes
        them (that script calls this one at the end of its build).
Output: paper/submission/em/manuscript.docx

Route: the anonymized LaTeX -> a pandoc-friendly LaTeX in which every number is the one LaTeX prints -> pandoc's Word
writer -> a style patch.
  - Numbers: sections and subsections, appendix sections, propositions and the lemma, equations, figures and tables
    are numbered as LaTeX numbers them (in the appendices within each appendix, as \\counterwithin does: Lemma B.1,
    (B.5), Figure D.1, Table A.1); the numbers are written into the text and every \\ref and \\eqref is replaced by
    its number. The build compiles the LaTeX and stops unless every label gets the number in LaTeX's own .aux file.
  - Equations become Word equations; a numbered equation carries its number at its end.
  - Figures embed as 300-dpi PNGs rendered from the PDFs.
  - Times New Roman 12 pt, 1.5 line spacing, A4 with 2.5 cm margins, page numbers in the footer, upright captions;
    no author in the file properties.
The build also stops if pandoc cannot convert an equation or find a figure, if a figure or table is missing from the
Word file, or if an identifying string appears in the document's text or properties.

Needs pandoc, pdftoppm and latexmk on the path. Run from pinning/:  python3 code/build_submission_em_docx.py
"""

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from build_submission_em import OUT as EM, identifying_hits, pandoc_env

SRC = EM / "manuscript.tex"
DOCX = EM / "manuscript.docx"


# ----------------------------------------------------------------- helpers
def match_brace(s, i):
    """s[i] == '{'; the index of the matching '}' (escaped characters skipped)."""
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    raise ValueError("unbalanced braces at " + s[i:i + 40])


def take_group(s, i):
    """(content, index just past it) of the brace group opening at s[i], after any whitespace."""
    while s[i] in " \t\n":
        i += 1
    j = match_brace(s, i)
    return s[i + 1:j], j + 1


def remove_command(s, name, nargs):
    """Delete every \\name{..}..{..} with nargs brace groups."""
    while (k := s.find("\\" + name)) >= 0:
        j = k + len(name) + 1
        for _ in range(nargs):
            _, j = take_group(s, j)
        s = s[:k] + s[j:]
    return s


def unwrap(s, opener):
    """Replace each group that starts with opener (e.g. '{\\small') by its content."""
    while (k := s.find(opener)) >= 0:
        j = match_brace(s, k)
        s = s[:k] + s[k + len(opener):j] + s[j + 1:]
    return s


def letter(n):
    return chr(ord("A") + n - 1)


# --------------------------------------------------------- numbering pass
HEAD_RE = re.compile(r"\\(section|subsection)(\*?)\{")
THM_RE = re.compile(r"\\begin\{(proposition|lemma|corollary)\}(\[[^\]]*\])?")
ENV_RE = re.compile(r"\\begin\{(equation|figure|table)\}")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")


def number_objects(body):
    """Walk the body in order. Returns ({label: printed number}, {kind: [printed number of each occurrence]}).

    Kinds: 'head' (None for a starred heading), 'thm' (None for the unnumbered corollary), 'equation', 'figure',
    'table'. Main text: sections 1, 2, ...; propositions and the lemma share one counter; equations, figures and
    tables run through the main text. Appendices: sections A, B, ...; propositions, equations, figures and tables
    restart in each appendix and print with its letter.
    """
    appendix_at = body.index("\\appendix")
    tokens = sorted([(m.start(), "head", m) for m in HEAD_RE.finditer(body)] +
                    [(m.start(), "thm", m) for m in THM_RE.finditer(body)] +
                    [(m.start(), m.group(1), m) for m in ENV_RE.finditer(body)], key=lambda t: t[0])
    labels = {}
    numbers = {"head": [], "thm": [], "equation": [], "figure": [], "table": []}
    count = dict.fromkeys(["thm", "equation", "figure", "table"], 0)
    sec = sub = 0
    in_appendix = False
    for pos, kind, m in tokens:
        if not in_appendix and pos > appendix_at:
            in_appendix, sec = True, 0
        if kind == "head":
            _, end = take_group(body, m.end() - 1)
            lab = LABEL_RE.match(body[end:].lstrip())
            if m.group(2) == "*":
                num = None
            elif m.group(1) == "section":
                sec, sub = sec + 1, 0
                if in_appendix:
                    count = dict.fromkeys(count, 0)
                num = letter(sec) if in_appendix else str(sec)
            else:
                sub += 1
                num = (letter(sec) if in_appendix else str(sec)) + "." + str(sub)
        else:
            prefix = letter(sec) + "." if in_appendix else ""
            if kind == "thm":
                lab = LABEL_RE.match(body, m.end())
                if m.group(1) == "corollary":
                    num = None
                else:
                    count["thm"] += 1
                    num = prefix + str(count["thm"])
            else:
                count[kind] += 1
                num = prefix + str(count[kind])
                lab = LABEL_RE.search(body, pos, body.index("\\end{" + kind + "}", pos))
        numbers[kind].append(num)
        if lab and num:
            labels[lab.group(1)] = num
    return labels, numbers


def latex_labels(tmp):
    """{label: number} as LaTeX itself prints them: compile the manuscript and read its .aux."""
    r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "manuscript.tex"],
                       cwd=tmp, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("BLOCKED: manuscript.tex does not compile\n" + r.stdout[-2000:])
    aux = (tmp / "manuscript.aux").read_text(errors="replace")
    return {m.group(1): m.group(2) for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", aux)}


# ----------------------------------------------------------- rewrite passes
DISPLAY_RE = re.compile(r"\\\[.*?\\\]|\\begin\{(equation|align\*|gather\*)\}.*?\\end\{\1\}", re.S)


def emph_paragraphs(text):
    """Each paragraph of text in \\emph; paragraph breaks kept, including one at either end."""
    return "\n\n".join("\\emph{" + p + "}" if p else "" for p in (q.strip() for q in re.split(r"\n\s*\n", text)))


def italic_statement(stmt):
    """A theorem statement as LaTeX sets it: the text in italics, display math as it is."""
    out, last = [], 0
    for m in DISPLAY_RE.finditer(stmt):
        out.append(emph_paragraphs(stmt[last:m.start()]))
        out.append("\n" + m.group(0) + "\n")
        last = m.end()
    out.append(emph_paragraphs(stmt[last:]))
    return "".join(out).strip()


def rewrite_theorems(body, nums):
    """Theorem environments -> paragraphs that open with 'Proposition 4 (name).' in LaTeX's style. Proofs open with
    'Proof.' or their own title ('Proof of Proposition 1.') in italics and end in □."""
    names = {"proposition": "Proposition", "lemma": "Lemma", "corollary": "Corollary"}
    matches = list(THM_RE.finditer(body))
    assert len(matches) == len(nums)
    for m, num in reversed(list(zip(matches, nums))):
        env = m.group(1)
        start = m.end()
        lab = LABEL_RE.match(body, start)
        if lab:
            start = lab.end()
        end = body.index("\\end{" + env + "}", start)
        note = " (" + m.group(2)[1:-1] + ")" if m.group(2) else ""
        head = "\\textbf{" + names[env] + (" " + num if num else "") + "}" + note + "\\textbf{.}"
        new = "\n\n\\noindent " + head + " " + italic_statement(body[start:end].strip()) + "\n\n"
        body = body[:m.start()] + new + body[end + len("\\end{" + env + "}"):]
    body = re.sub(r"\\begin\{proof\}(?:\[([^\]]*)\])?\s*",
                  lambda m: "\\noindent\\emph{" + (m.group(1) or "Proof") + ".} ", body)
    body = re.sub(r"\s*\\end\{proof\}", lambda _: " □", body)
    return body


def number_equations(body, nums):
    """Each numbered equation carries its number at its end: x = y   (B.5). The number is upright math inside
    math brackets: a text run holding brackets is shown with backslashes by some renderers."""
    matches = list(re.finditer(r"\\begin\{equation\}(.*?)\\end\{equation\}", body, re.S))
    assert len(matches) == len(nums)
    for m, num in reversed(list(zip(matches, nums))):
        new = "\\begin{equation}" + m.group(1).rstrip() + "\\qquad(\\mathrm{" + num + "})\n\\end{equation}"
        body = body[:m.start()] + new + body[m.end():]
    return body


TEXT_WIDTH_CM = 16.0    # A4 with 2.5 cm margins, the manuscript's geometry (asserted in pandoc_latex)
LABEL_COLUMN_CM = 3.0   # an l, c or r column, which holds short labels ('Sections 3-5', 'Appendix B')


def relative_columns(spec):
    """A tabular column spec with every width as a fraction of the line: pandoc carries those into Word and
    splits the table evenly when widths are absolute or missing."""
    out, i = [], 0
    while i < len(spec):
        c = spec[i]
        if c in "lcr":
            out.append("p{%.4f\\linewidth}" % (LABEL_COLUMN_CM / TEXT_WIDTH_CM))
            i += 1
        elif c == "p":
            width, i = take_group(spec, i + 1)
            cm = re.fullmatch(r"([\d.]+)cm", width.strip())
            out.append("p{%.4f\\linewidth}" % (float(cm.group(1)) / TEXT_WIDTH_CM) if cm else "p{" + width + "}")
        else:
            out.append(c)
            i += 1
    return "".join(out)


def rewrite_floats(body, kind, nums):
    """'Figure 3.' or 'Table A.1.' in bold before each caption, as LaTeX prints it. Figures point at the PNGs;
    tables get relative column widths and lose the size group and the ragged-right commands pandoc does not read."""
    word = {"figure": "Figure", "table": "Table"}[kind]
    pattern = re.compile(r"\\begin\{" + kind + r"\}(\[[^\]]*\])?(.*?)\\end\{" + kind + r"\}", re.S)
    out, last, k = [], 0, 0
    for m in pattern.finditer(body):
        block = m.group(2)
        c = block.index("\\caption")
        cap, cend = take_group(block, c + len("\\caption"))
        cap = re.sub(r"\s+", " ", cap.strip())
        block = block[:c] + "\\caption{\\textbf{" + word + " " + nums[k] + ".} " + cap + "}" + block[cend:]
        if kind == "figure":
            block = re.sub(r"\{(Figure_[A-Z]?\d+)\.pdf\}", r"{\1.png}", block)
        else:
            block = unwrap(block, "{\\small")
            block = block.replace("\\raggedright", "").replace("\\tabularnewline", "\\\\")
            t = block.index("\\begin{tabular}") + len("\\begin{tabular}")
            spec, send = take_group(block, t)
            block = block[:t] + "{" + relative_columns(spec) + "}" + block[send:]
        out.append(body[last:m.start()] + "\\begin{" + kind + "}" + block + "\\end{" + kind + "}")
        last = m.end()
        k += 1
    assert k == len(nums)
    out.append(body[last:])
    return "".join(out)


def rewrite_headings(body, nums):
    """Numbered headings -> unnumbered headings that carry LaTeX's number in their text."""
    matches = list(HEAD_RE.finditer(body))
    assert len(matches) == len(nums)
    for m, num in reversed(list(zip(matches, nums))):
        if num is None:
            continue
        title, end = take_group(body, m.end() - 1)
        appendix_section = m.group(1) == "section" and num.isalpha()
        text = ("Appendix " + num + ". " + title) if appendix_section else (num + " " + title)
        body = body[:m.start()] + "\\" + m.group(1) + "*{" + text + "}" + body[end:]
    return body


def resolve_refs(body, labels):
    def number(m):
        if m.group(2) not in labels:
            raise KeyError("unresolved reference " + m.group(2))
        n = labels[m.group(2)]
        return "(" + n + ")" if m.group(1) == "eqref" else n
    body = re.sub(r"\\(ref|eqref)\{([^}]*)\}", number, body)
    return LABEL_RE.sub("", body)


def rewrite_back_matter(body):
    """References: one paragraph per entry. The data note: a plain paragraph (pandoc drops a brace group that
    follows \\noindent, and draws no rule)."""
    body = unwrap(body, "{\\small\\singlespacing")
    while (k := body.find("\\refentry{")) >= 0:
        entry, end = take_group(body, k + len("\\refentry"))
        body = body[:k] + "\n\n" + entry.strip() + "\n\n" + body[end:]
    body = body.replace("\\bigskip\\par\\noindent\\rule{0.35\\linewidth}{0.4pt}\\par\\smallskip", "\n\n")
    marker = "\\noindent{\\footnotesize\\singlespacing"
    while (k := body.find(marker)) >= 0:
        content, end = take_group(body, k + len("\\noindent"))
        body = body[:k] + "\n\n" + content[len("\\footnotesize\\singlespacing"):].strip() + "\n\n" + body[end:]
    return body


def title_parts(pre):
    k = pre.index("\\title{")
    raw, _ = take_group(pre, k + len("\\title"))
    main, _, sub = raw.partition("\\\\")
    sub = re.sub(r"^\[[^\]]*\]", "", sub.strip())

    def clean(s):
        return re.sub(r"\s+", " ", re.sub(r"\\(bfseries|large|mdseries)", "", s)).strip()
    return clean(main), clean(sub)


def pandoc_latex(tex):
    """The anonymized manuscript as LaTeX that pandoc reads correctly, and the label numbers it uses."""
    pre, body = tex.split("\\begin{document}", 1)
    assert "\\usepackage[a4paper, margin=2.5cm]{geometry}" in pre, "page geometry changed: update TEXT_WIDTH_CM"
    body = body.replace("\\end{document}", "").replace("\\maketitle", "").replace("\\qedhere", "")
    body = remove_command(body, "counterwithin", 2)
    body = remove_command(body, "titleformat", 5)
    labels, nums = number_objects(body)
    body = rewrite_theorems(body, nums["thm"])
    body = number_equations(body, nums["equation"])
    body = rewrite_floats(body, "figure", nums["figure"])
    body = rewrite_floats(body, "table", nums["table"])
    body = rewrite_headings(body, nums["head"])
    body = resolve_refs(body, labels)
    body = body.replace("\\appendix", "")
    body = rewrite_back_matter(body)
    body = body.replace("\\bm{", "\\boldsymbol{")
    # x^* with the glyph LaTeX prints, U+2217: pandoc writes \ast as an ASCII '*', which some renderers read as an
    # operator missing its operands
    body = re.sub(r"\^(\{\*\}|\*)", lambda _: "^{∗}", body)
    title, subtitle = title_parts(pre)
    head = ["\\documentclass[12pt]{article}", "\\usepackage{amsmath,amssymb,graphicx,booktabs}",
            "\\title{" + title + "}", "\\subtitle{" + subtitle + "}", "\\begin{document}"]
    return "\n".join(head) + "\n" + body.strip() + "\n\\end{document}\n", labels, nums


# ------------------------------------------------------------ Word output
FOOTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
          '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
          '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
          '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
SECTION = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdPageFooter"/>'
           '<w:pgSz w:w="11906" w:h="16838"/>'
           '<w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1418" w:header="709" w:footer="709" '
           'w:gutter="0"/></w:sectPr>')


def patch_styles(s):
    """Times New Roman 12 pt, black headings, 1.5 line spacing, upright captions, an 11 pt abstract."""
    s = re.sub(r'w:(ascii|hAnsi|eastAsia|cs)="[^"]*"', r'w:\1="Times New Roman"', s)
    s = re.sub(r'\s*w:(asciiTheme|hAnsiTheme|eastAsiaTheme|cstheme)="[^"]*"', "", s)
    s = re.sub(r'<w:color w:val="[0-9A-Fa-f]{6}"[^/]*/>', "", s)
    s = re.sub(r'<w:spacing w:val="-?\d+"\s*/>', "", s)
    s = re.sub(r'(<w:docDefaults>.*?)<w:sz w:val="\d+"\s*/>', r'\1<w:sz w:val="24"/>', s, count=1, flags=re.S)
    s = re.sub(r'(<w:docDefaults>.*?)<w:szCs w:val="\d+"\s*/>', r'\1<w:szCs w:val="24"/>', s, count=1, flags=re.S)
    s = re.sub(r'(<w:pPrDefault>\s*<w:pPr>)(.*?)(</w:pPr>)',
               lambda m: m.group(1) + re.sub(r'<w:spacing[^/]*/>', '', m.group(2)) +
               '<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>' + m.group(3), s, count=1, flags=re.S)
    s = re.sub(r'(<w:style [^>]*w:styleId="Caption">.*?)<w:i\s*/>(.*?</w:style>)', r'\1\2', s, count=1, flags=re.S)
    s = re.sub(r'(<w:style [^>]*w:styleId="Abstract">.*?)<w:sz w:val="20"\s*/>\s*<w:szCs w:val="20"\s*/>',
               r'\1<w:sz w:val="22"/><w:szCs w:val="22"/>', s, count=1, flags=re.S)
    return s


def reference_docx(path):
    """pandoc's default reference document with the journal layout: styles, A4 page, margins, footer page number."""
    subprocess.run(["pandoc", "-o", str(path), "--print-default-data-file", "reference.docx"], check=True, env=pandoc_env())
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                data = patch_styles(data.decode("utf-8")).encode("utf-8")
            elif item.filename == "word/document.xml":
                s = data.decode("utf-8")
                assert s.count("<w:sectPr />") == 1, "the default reference document changed"
                data = s.replace("<w:sectPr />", SECTION).encode("utf-8")
            elif item.filename == "word/_rels/document.xml.rels":
                rel = ('<Relationship Id="rIdPageFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                       'relationships/footer" Target="footer1.xml"/>')
                data = data.decode("utf-8").replace("</Relationships>", rel + "</Relationships>").encode("utf-8")
            elif item.filename == "[Content_Types].xml":
                ct = ('<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-'
                      'officedocument.wordprocessingml.footer+xml"/>')
                data = data.decode("utf-8").replace("</Types>", ct + "</Types>").encode("utf-8")
            zout.writestr(item, data)
        # pandoc copies the footer part with its zip timestamp: give it the template's, not the build time
        footer = zipfile.ZipInfo("word/footer1.xml", date_time=item.date_time)
        footer.compress_type = zipfile.ZIP_DEFLATED
        zout.writestr(footer, FOOTER)
    shutil.move(tmp, path)


def scrub_properties(path):
    """No author in the file properties."""
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                s = data.decode("utf-8")
                s = re.sub(r"<dc:creator>.*?</dc:creator>|<dc:creator\s*/>", "<dc:creator></dc:creator>", s, flags=re.S)
                s = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>", "", s, flags=re.S)
                data = s.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)


def docx_text(path):
    """The text of every XML part (document, properties, footer), tags removed."""
    with zipfile.ZipFile(path) as z:
        return " ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "replace"))
                        for n in z.namelist() if n.endswith(".xml"))


def main():
    tex = SRC.read_text(encoding="utf-8")
    word_tex, labels, nums = pandoc_latex(tex)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copy(SRC, tmp / "manuscript.tex")
        figures = sorted(EM.glob("Figure_*.pdf"))
        for pdf in figures:
            shutil.copy(pdf, tmp / pdf.name)
        printed = latex_labels(tmp)
        wrong = {k: (labels.get(k), printed.get(k)) for k in set(printed) | set(labels) if labels.get(k) != printed.get(k)}
        if wrong:
            sys.exit(f"BLOCKED: numbers differ from LaTeX's (ours, LaTeX's): {wrong}")
        for pdf in figures:
            subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", pdf.name, pdf.stem], cwd=tmp, check=True)
        (tmp / "word.tex").write_text(word_tex, encoding="utf-8")
        ref = tmp / "reference.docx"
        reference_docx(ref)
        out = tmp / "manuscript.docx"
        r = subprocess.run(["pandoc", "word.tex", "-f", "latex", "-t", "docx", "--reference-doc=reference.docx",
                            "-o", out.name], cwd=tmp, capture_output=True, text=True, env=pandoc_env())
        if r.returncode != 0 or re.search(r"Could not (convert TeX math|fetch|find)", r.stderr):
            sys.exit("BLOCKED: pandoc\n" + r.stderr)
        scrub_properties(out)
        with zipfile.ZipFile(out) as z:
            doc = z.read("word/document.xml").decode("utf-8")
            images = [n for n in z.namelist() if n.startswith("word/media/")]
        problems = []
        if len(images) != len(figures) or len(figures) != len(nums["figure"]):
            problems.append(f"{len(images)} images in the Word file, {len(figures)} figure files, "
                            f"{len(nums['figure'])} figures in the text")
        if doc.count("<w:tbl>") != len(nums["table"]):
            problems.append(f"{doc.count('<w:tbl>')} tables in the Word file, {len(nums['table'])} in the text")
        hits = identifying_hits(docx_text(out))
        if hits:
            problems.append(f"identifying strings in the Word file: {hits}")
        if problems:
            sys.exit("BLOCKED:\n  " + "\n  ".join(problems))
        shutil.copy(out, DOCX)
    if r.stderr.strip():
        print("pandoc notes:\n" + r.stderr.strip())
    print(f"wrote {DOCX.relative_to(EM.parents[2])}: {len(labels)} labels as LaTeX prints them; "
          f"{len(nums['equation'])} numbered equations, {len(nums['figure'])} figures, {len(nums['table'])} tables")


if __name__ == "__main__":
    main()
