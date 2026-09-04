"""
build_submission_docx.py — the journal's Word files, built from paper/main.tex.

Outputs, in paper/submission/:
  manuscript_blind.docx   the full paper with an anonymized title page: no authors,
                          affiliations, emails, or disclaimer footnote, and the
                          repository address withheld; everything else verbatim.
  title_page.docx         the separate title page carrying the author details.

Route: main.tex -> a pandoc-friendly LaTeX (cross-references resolved to the numbers
LaTeX prints, theorem environments written out with their numbers, headings carrying
their numbers, the few macros pandoc cannot render replaced) -> pandoc's docx writer
(equations become Word equations, figures embed) -> a style patch (Times New Roman
12 pt, one-and-a-half spacing, 2.5 cm margins, no author metadata).

The pandoc binary comes with the pypandoc_binary package in the repo venv.

Run from pinning/:  ../venv/Scripts/python.exe code/build_submission_docx.py
"""

import pathlib
import re
import shutil
import subprocess
import sys
import zipfile

import pypandoc

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
SRC = PAPER / "main.tex"
OUT = PAPER / "submission"
BUILD = OUT / "_build"
PANDOC = pypandoc.get_pandoc_path()

REPO_URL_SENTENCE = "the code and data are public at \\url{https://github.com/wilsoniumite/labor}."
BLIND_SENTENCE = "the code and data are public; the repository address is withheld for review."


# ----------------------------------------------------------------- helpers
def match_brace(s, i):
    """s[i] == '{'; return the index of the matching '}' (ignores escaped braces)."""
    assert s[i] == "{", s[i:i + 20]
    depth = 0
    j = i
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
    """Return (content, end_index_exclusive) of the brace group starting at s[i] == '{'."""
    j = match_brace(s, i)
    return s[i + 1:j], j + 1


def remove_command(s, name, nargs):
    """Delete every occurrence of \\name{..}{..} with nargs brace groups."""
    pat = "\\" + name
    while True:
        k = s.find(pat)
        if k < 0:
            return s
        j = k + len(pat)
        for _ in range(nargs):
            while s[j] in " \n\t":
                j += 1
            _, j = take_group(s, j)
        s = s[:k] + s[j:]


def roman_letter(n):
    return chr(ord("A") + n - 1)


# ------------------------------------------------------ title-block parsing
def parse_title_block(pre):
    """Title, subtitle, the disclaimer footnote text, and the author entries."""
    k = pre.find("\\title{")
    title_raw, _ = take_group(pre, k + len("\\title"))
    # the disclaimer footnote
    t = title_raw.find("\\thanks{")
    thanks, end = take_group(title_raw, t + len("\\thanks"))
    thanks = "\n".join(ln for ln in thanks.splitlines() if not ln.strip().startswith("%"))
    thanks = re.sub(r"\s+", " ", thanks).strip()
    title_raw = title_raw[:t] + title_raw[end:]
    main_title, _, subtitle = title_raw.partition("\\\\")
    main_title = re.sub(r"\\bfseries|\\large|\\mdseries", "", main_title)
    subtitle = re.sub(r"^\[[^\]]*\]", "", subtitle.strip())
    subtitle = re.sub(r"\\bfseries|\\large|\\mdseries", "", subtitle)
    main_title = re.sub(r"\s+", " ", main_title).strip()
    subtitle = re.sub(r"\s+", " ", subtitle).strip()
    # authors
    a = pre.find("\\author{")
    authors_raw, _ = take_group(pre, a + len("\\author"))
    authors = []
    for chunk in authors_raw.split("\\and"):
        chunk = chunk.strip()
        if not chunk:
            continue
        t = chunk.find("\\thanks{")
        note, _ = take_group(chunk, t + len("\\thanks"))
        name = chunk[:t].strip()
        name = name.replace("\\r{a}", "å").replace("\\r{A}", "Å")
        note = re.sub(r"\s+", " ", note).strip()
        m = re.search(r"Email:\s*\\texttt\{([^}]*)\}\.?", note)
        email = m.group(1) if m else ""
        affil = re.sub(r"\s*Email:.*$", "", note).strip().rstrip(".")
        authors.append((name, affil, email))
    return main_title, subtitle, thanks, authors


# --------------------------------------------------------- numbering pass
HEAD_RE = re.compile(r"\\(section|subsection)\*?\{")
THM_RE = re.compile(r"\\begin\{(proposition|lemma|corollary)\}(\[[^\]]*\])?")
FIG_RE = re.compile(r"\\begin\{figure\}")
EQ_RE = re.compile(r"\\begin\{equation\}")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")


def number_document(body):
    """Walk the body in order and assign every numbered object the string LaTeX prints.

    Returns (labels, events) where labels maps label -> printed number and events is
    the list of (position, kind, number, extra) used by the rewrite pass.
    """
    labels = {}
    events = []
    sec = 0
    sub = 0
    appendix = False
    thm = 0          # proposition counter (lemma shares it); reset per appendix section
    fig = 0
    eq = 0
    i = 0
    pos_appendix = body.find("\\appendix")
    tokens = []
    for m in HEAD_RE.finditer(body):
        tokens.append((m.start(), "head", m))
    for m in THM_RE.finditer(body):
        tokens.append((m.start(), "thm", m))
    for m in FIG_RE.finditer(body):
        tokens.append((m.start(), "fig", m))
    for m in EQ_RE.finditer(body):
        tokens.append((m.start(), "eq", m))
    tokens.sort(key=lambda t: t[0])
    for pos, kind, m in tokens:
        if not appendix and pos_appendix >= 0 and pos > pos_appendix:
            appendix = True
            sec = 0
        if kind == "head":
            starred = body[m.end() - 2] == "*"
            title, end = take_group(body, m.end() - 1)
            lab = LABEL_RE.match(body[end:].lstrip())
            label = lab.group(1) if lab else None
            if starred:
                num = None
            elif m.group(1) == "section":
                sec += 1
                sub = 0
                if appendix:
                    thm = 0
                num = roman_letter(sec) if appendix else str(sec)
            else:
                sub += 1
                num = (roman_letter(sec) if appendix else str(sec)) + "." + str(sub)
            if label and num:
                labels[label] = num
            events.append((pos, "head", num, (m.group(1), starred, title, end, label)))
        elif kind == "thm":
            env = m.group(1)
            name = m.group(2)[1:-1] if m.group(2) else None
            lab = LABEL_RE.match(body[m.end():])
            label = lab.group(1) if lab else None
            if env == "corollary":
                num = None
            else:
                thm += 1
                num = (roman_letter(sec) + "." if appendix else "") + str(thm)
            if label and num:
                labels[label] = num
            events.append((pos, "thm", num, (env, name, label)))
        elif kind == "fig":
            fig += 1
            endpos = body.find("\\end{figure}", pos)
            lab = LABEL_RE.search(body[pos:endpos])
            if lab:
                labels[lab.group(1)] = str(fig)
            events.append((pos, "fig", str(fig), None))
        elif kind == "eq":
            eq += 1
            endpos = body.find("\\end{equation}", pos)
            lab = LABEL_RE.search(body[pos:endpos])
            if lab:
                labels[lab.group(1)] = str(eq)
            events.append((pos, "eq", str(eq), None))
    return labels, events


# ----------------------------------------------------------- rewrite pass
DISPLAY_RE = re.compile(r"\\\[.*?\\\]|\\begin\{equation\}.*?\\end\{equation\}", re.S)


def italicize_statement(body):
    """Wrap each text paragraph of a theorem statement in \\emph, leaving display math alone."""
    out = []
    last = 0
    for m in DISPLAY_RE.finditer(body):
        out.append(_emph_paragraphs(body[last:m.start()]))
        out.append("\n" + m.group(0) + "\n")
        last = m.end()
    out.append(_emph_paragraphs(body[last:]))
    return "".join(out)


def _emph_paragraphs(text):
    paras = re.split(r"\n\s*\n", text)
    wrapped = []
    for p in paras:
        p = p.strip()
        if p:
            wrapped.append("\\emph{" + p + "}")
    return "\n\n".join(wrapped) + ("\n\n" if wrapped else "")


def rewrite_theorems(body):
    """Theorem environments -> explicit numbered paragraphs (numbers as LaTeX prints them)."""
    labels, events = number_document(body)
    names = {"proposition": "Proposition", "lemma": "Lemma", "corollary": "Corollary"}
    # walk backwards so positions stay valid
    thm_events = [e for e in events if e[1] == "thm"]
    for pos, _, num, (env, name, label) in reversed(thm_events):
        m = THM_RE.match(body, pos)
        start_body = m.end()
        if label:
            lab = LABEL_RE.match(body[start_body:])
            start_body += lab.end()
        end = body.find("\\end{" + env + "}", start_body)
        stmt = body[start_body:end].strip()
        head = names[env] + (" " + num if num else "") + (" (" + name + ")" if name else "") + "."
        new = "\\noindent\\textbf{" + head + "} " + italicize_statement(stmt).strip()
        body = body[:pos] + new + body[end + len("\\end{" + env + "}"):]
    # proofs
    body = re.sub(r"\\begin\{proof\}\s*", "\\\\noindent\\\\emph{Proof.} ", body)
    body = re.sub(r"\s*\\end\{proof\}", " ∎", body)
    return labels, body


def rewrite_headings(body):
    """Numbered headings -> starred headings carrying the number in the text."""
    _, events = number_document(body)
    head_events = [e for e in events if e[1] == "head"]
    for pos, _, num, (level, starred, title, end, label) in reversed(head_events):
        if starred:
            continue
        seg_end = end
        lab = LABEL_RE.match(body[end:].lstrip())
        if lab:
            seg_end = end + len(body[end:]) - len(body[end:].lstrip()) + lab.end()
        appendix_section = level == "section" and num.isalpha()
        text = ("Appendix " + num + ". " + title) if appendix_section else (num + " " + title)
        body = body[:pos] + "\\" + level + "*{" + text + "}" + body[seg_end:]
    return body


def resolve_refs(body, labels):
    def rep(m):
        key = m.group(2)
        if key not in labels:
            raise KeyError("unresolved reference " + key)
        n = labels[key]
        return "(" + n + ")" if m.group(1) == "eqref" else n
    body = re.sub(r"\\(ref|eqref)\{([^}]*)\}", rep, body)
    body = LABEL_RE.sub("", body)
    return body


def rewrite_figures(body, labels):
    """Prefix every caption with 'Figure N.' (pandoc's Word captions carry no label)."""
    fig = 0
    out = []
    last = 0
    for m in FIG_RE.finditer(body):
        fig += 1
        endpos = body.find("\\end{figure}", m.start())
        block = body[m.start():endpos]
        c = block.find("\\caption{")
        cap, cend = take_group(block, c + len("\\caption"))
        cap = re.sub(r"\s+", " ", cap.strip())
        block = block[:c] + "\\caption{Figure " + str(fig) + ". " + cap + "}" + block[cend:]
        out.append(body[last:m.start()])
        out.append(block)
        last = endpos
    out.append(body[last:])
    return "".join(out)


def rewrite_references(body):
    """\\refentry{...} -> one paragraph per entry."""
    while True:
        k = body.find("\\refentry{")
        if k < 0:
            return body
        entry, end = take_group(body, k + len("\\refentry"))
        body = body[:k] + "\\par\\noindent " + entry.strip() + "\\par\n" + body[end:]


def rewrite_notes(body):
    """The back-matter notes: drop the rules and size commands, keep the bold lead-ins.

    pandoc discards a brace group that directly follows \\noindent, so each note is
    unwrapped into an ordinary paragraph.
    """
    body = body.replace("\\bigskip\\par\\noindent\\rule{0.35\\linewidth}{0.4pt}\\par\\smallskip", "\\bigskip")
    marker = "\\noindent{\\footnotesize\\singlespacing "
    while True:
        k = body.find(marker)
        if k < 0:
            return body
        content, end = take_group(body, k + len("\\noindent"))
        content = content[len("\\footnotesize\\singlespacing "):].strip()
        body = body[:k] + "\\par " + content + "\\par\n" + body[end:]


def replace_math_macros(body):
    body = body.replace("\\bm{", "\\boldsymbol{")
    body = re.sub(r"\\lo(?![A-Za-z])", r"\\mathrm{lo}", body)
    body = re.sub(r"\\hi(?![A-Za-z])", r"\\mathrm{hi}", body)
    return body


def preprocess(blind):
    tex = SRC.read_text(encoding="utf-8")
    pre, _, body = tex.partition("\\begin{document}")
    body = body.replace("\\end{document}", "")
    title, subtitle, thanks, authors = parse_title_block(pre)

    # structural commands pandoc must not see
    body = body.replace("\\maketitle", "")
    body = remove_command(body, "counterwithin", 2)
    body = remove_command(body, "titleformat", 5)

    labels, body = rewrite_theorems(body)
    body = rewrite_headings(body)
    body = rewrite_figures(body, labels)
    body = resolve_refs(body, labels)
    body = body.replace("\\appendix", "")
    body = rewrite_references(body)
    body = rewrite_notes(body)
    body = replace_math_macros(body)

    if blind:
        assert body.count(REPO_URL_SENTENCE) == 1, "repository sentence not found exactly once"
        body = body.replace(REPO_URL_SENTENCE, BLIND_SENTENCE)

    head = ["\\documentclass[12pt]{article}",
            "\\usepackage{amsmath,amssymb,graphicx,booktabs}",
            "\\title{" + title + "}",
            "\\subtitle{" + subtitle + "}"]
    if not blind:
        head.append("\\author{" + " \\and ".join(a[0] for a in authors) + "}")
    head.append("\\begin{document}")
    out = "\n".join(head) + "\n" + body.strip() + "\n\\end{document}\n"
    return out, labels, (title, subtitle, thanks, authors)


# ------------------------------------------------------------ Word output
def reference_docx(path):
    """pandoc's default reference document, restyled: Times New Roman 12 pt, 1.5 spacing, 2.5 cm margins."""
    subprocess.run([PANDOC, "-o", str(path), "--print-default-data-file", "reference.docx"], check=True)
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                s = data.decode("utf-8")
                s = re.sub(r'w:(ascii|hAnsi|eastAsia|cs)="[^"]*"', r'w:\1="Times New Roman"', s)
                s = re.sub(r'w:(asciiTheme|hAnsiTheme|eastAsiaTheme|cstheme)="[^"]*"', "", s)
                # black headings; no letter-spacing on the subtitle
                s = re.sub(r'<w:color w:val="[0-9A-Fa-f]{6}"[^/]*/>', "", s)
                s = re.sub(r'<w:spacing w:val="-?\d+"\s*/>', "", s)
                # body size 12 pt in the document defaults and Normal; keep headings' relative sizes
                s = re.sub(r'(<w:docDefaults>.*?)<w:sz w:val="\d+"\s*/>', r'\1<w:sz w:val="24"/>', s, count=1, flags=re.S)
                s = re.sub(r'(<w:docDefaults>.*?)<w:szCs w:val="\d+"\s*/>', r'\1<w:szCs w:val="24"/>', s, count=1, flags=re.S)
                # one-and-a-half line spacing on the document defaults
                s = re.sub(r'(<w:pPrDefault>\s*<w:pPr>)(.*?)(</w:pPr>)',
                           lambda m: m.group(1) + re.sub(r'<w:spacing[^/]*/>', '', m.group(2)) +
                           '<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>' + m.group(3), s, count=1, flags=re.S)
                data = s.encode("utf-8")
            elif item.filename == "word/document.xml":
                # pandoc copies the reference's section properties; the default carries none
                s = data.decode("utf-8")
                s = re.sub(r"<w:sectPr>.*?</w:sectPr>",
                           '<w:sectPr><w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr>'
                           '<w:pgSz w:w="11906" w:h="16838"/>'
                           '<w:pgMar w:top="1418" w:right="1418" w:bottom="1418" w:left="1418" '
                           'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>', s, count=1, flags=re.S)
                data = s.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)


def scrub_properties(path, keep_creator):
    """No author name in the file properties of the blind manuscript."""
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                s = data.decode("utf-8")
                s = re.sub(r"<dc:creator>.*?</dc:creator>", "<dc:creator>" + keep_creator + "</dc:creator>", s, flags=re.S)
                s = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>", "", s, flags=re.S)
                data = s.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)


def run_pandoc(tex_path, docx_path, ref):
    pypandoc.convert_file(str(tex_path), "docx", format="latex", outputfile=str(docx_path),
                          extra_args=["--resource-path=" + str(PAPER), "--reference-doc=" + str(ref)])


def build_title_page(meta, ref):
    title, subtitle, thanks, authors = meta
    author_block = " \\and ".join(name + "\\\\" + affil + "\\\\" + email for name, affil, email in authors)
    lines = ["\\documentclass[12pt]{article}",
             "\\title{" + title + "}",
             "\\subtitle{" + subtitle + "}",
             "\\author{" + author_block + "}",
             "\\begin{document}", "\\maketitle",
             "\\bigskip", "\\noindent " + thanks, "\\end{document}"]
    tex_path = BUILD / "title_page.tex"
    tex_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    docx_path = OUT / "title_page.docx"
    run_pandoc(tex_path, docx_path, ref)
    scrub_properties(docx_path, authors[0][0] + " and " + authors[1][0] if len(authors) > 1 else authors[0][0])
    return docx_path


def main():
    OUT.mkdir(exist_ok=True)
    BUILD.mkdir(exist_ok=True)
    ref = BUILD / "reference.docx"
    reference_docx(ref)

    tex, labels, meta = preprocess(blind=True)
    tex_path = BUILD / "manuscript_blind.tex"
    tex_path.write_text(tex, encoding="utf-8")
    docx_path = OUT / "manuscript_blind.docx"
    run_pandoc(tex_path, docx_path, ref)
    scrub_properties(docx_path, "")

    tp = build_title_page(meta, ref)

    print("labels resolved:", len(labels))
    for k in ("sec:limit", "app:coverage", "prop:fork", "lem:existence", "lem:superstar", "fig:fourway", "eq:ces-share"):
        print("  ", k, "->", labels[k])
    print("wrote", docx_path.relative_to(ROOT), "and", tp.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
