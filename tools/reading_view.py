"""reading_view.py — a clean reading view of every changed paragraph.

Word-diffs splice red and green into one line; this shows each changed
paragraph of the NEW file as plain readable prose, with the paragraph it
replaced tucked underneath (collapsed), so it can be reread as text.

    python code/reading_view.py OLD.tex NEW.tex OUT.html "title" [PREV.tex]

OLD is the baseline the reader last approved; NEW is the current file; the
optional PREV marks which paragraphs changed since the previous step. Blocks
are blank-line separated; figure environments show their caption. LaTeX is
lightly rendered (\\textbf, \\emph, ---, --, ~, \\ref); math is left as source.
"""

import difflib
import html
import re
import sys

OLD, NEW, OUT, TITLE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
PREV = sys.argv[5] if len(sys.argv) > 5 else None


def blocks(path):
    src = open(path, encoding="utf-8").read()
    body = src.split("\\begin{document}", 1)[-1]
    return [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]


def brace_arg(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1:i]
    return s[start + 1:]


def render(block):
    """Return (kind, html) for a block."""
    b = block
    fig = re.search(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", b)
    if fig and "\\caption" in b:
        lab = re.search(r"\\label\{([^}]*)\}", b)
        cap = brace_arg(b, b.find("{", b.find("\\caption")))
        head = f"Figure caption ({lab.group(1) if lab else fig.group(1)})"
        return "figure", f"<div class='where'>{html.escape(head)}</div>" + prose(cap)
    m = re.match(r"\\(sub)?section\{", b)
    if m:
        title = brace_arg(b, b.find("{"))
        return "heading", f"<div class='where'>Section heading</div><p><b>{prose_inline(title)}</b></p>"
    if b.startswith("\\begin{"):
        return "env", f"<pre>{html.escape(b)}</pre>"
    return "para", prose(b)


def prose_inline(s):
    s = html.escape(s)
    s = re.sub(r"\\textbf\{([^{}]*)\}", r"<b>\1</b>", s)
    s = re.sub(r"\\emph\{([^{}]*)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\(?:eq)?ref\{([^}]*)\}", r"<span class='ref'>[\1]</span>", s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = s.replace("---", "—").replace("--", "–").replace("~", "&nbsp;")
    s = re.sub(r"\$([^$]+)\$", r"<span class='math'>$\1$</span>", s)
    s = s.replace("\\%", "%").replace("\\&", "&amp;")
    return s


def prose(block):
    text = " ".join(line.strip() for line in block.splitlines())
    return f"<p>{prose_inline(text)}</p>"


def section_of(blocks_list):
    """Map each block index to the section/subsection it sits under."""
    where, cur = [], "front matter"
    for b in blocks_list:
        m = re.match(r"\\(sub)?section\{", b)
        if m:
            cur = re.sub(r"\\label\{[^}]*\}", "", brace_arg(b, b.find("{"))).strip()
        where.append(cur)
    return where


old_b, new_b = blocks(OLD), blocks(NEW)
prev_set = set(blocks(PREV)) if PREV else None
old_set = set(old_b)
where = section_of(new_b)

sm = difflib.SequenceMatcher(a=old_b, b=new_b, autojunk=False)
replaced_by = {}          # new index -> list of old blocks it replaced
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ("replace", "insert"):
        olds = old_b[i1:i2]
        for j in range(j1, j2):
            replaced_by[j] = olds

windows = []
for j, b in enumerate(new_b):
    if b in old_set:
        continue
    kind, body = render(b)
    olds = replaced_by.get(j, [])
    # pair each new block with its closest old block, if any
    best = difflib.get_close_matches(b, olds, n=1, cutoff=0.25) if olds else []
    fresh = prev_set is not None and b not in prev_set
    windows.append((j, where[j], kind, body, best, fresh))

n_new_step = sum(1 for w in windows if w[5])
css = """
body{font-family:Georgia,'DejaVu Serif',serif;max-width:780px;margin:2.5rem auto;padding:0 1.2rem;color:#1a1a1a;line-height:1.55}
h1{font-size:1.35rem;margin-bottom:.2rem} .sub{color:#666;font-size:.92rem;margin-bottom:2rem}
.win{border:1px solid #d8d8d8;border-radius:6px;padding:1rem 1.25rem;margin:1.4rem 0;background:#fff}
.win.fresh{border-color:#8b2020}
.loc{font-size:.8rem;color:#8b2020;letter-spacing:.02em;text-transform:uppercase;margin-bottom:.35rem}
.loc .tag{float:right;color:#fff;background:#8b2020;padding:0 .45em;border-radius:3px;font-size:.72rem}
.where{font-size:.85rem;color:#666;margin-bottom:.3rem}
p{margin:.4rem 0 .6rem} .math{font-family:'DejaVu Sans Mono',Consolas,monospace;font-size:.88em;color:#333}
.ref{color:#4878b8;font-size:.9em}
details{margin-top:.6rem;font-size:.92rem;color:#555} summary{cursor:pointer;color:#4878b8}
details p{color:#555} pre{white-space:pre-wrap;font-size:.85em}
"""
out = [f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(TITLE)}</title><style>{css}</style></head><body>",
       f"<h1>{html.escape(TITLE)}</h1>",
       f"<div class='sub'>{len(windows)} changed paragraphs against the baseline"
       + (f"; {n_new_step} changed in this step (red border)" if prev_set is not None else "")
       + ". Each window is the current text, readable as prose; the paragraph it replaced is under the fold.</div>"]
for j, sec, kind, body, best, fresh in windows:
    tag = "<span class='tag'>this step</span>" if fresh else ""
    out.append(f"<div class='win{' fresh' if fresh else ''}'><div class='loc'>{tag}{html.escape(sec)}</div>{body}")
    if best:
        out.append(f"<details><summary>what it replaced in the baseline</summary>{render(best[0])[1]}</details>")
    else:
        out.append("<details><summary>new paragraph — nothing replaced</summary><p><i>inserted</i></p></details>")
    out.append("</div>")
out.append("</body></html>")
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print(f"wrote {OUT}: {len(windows)} windows" + (f", {n_new_step} this step" if prev_set is not None else ""))
