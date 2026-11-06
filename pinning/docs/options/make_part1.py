"""make_part1.py — Part 1 (whole-paper layouts) as a rows file for build_options.py.

    python3 -B make_part1.py STRUCTURES.json rows/part1_structure.json

STRUCTURES.json: {"blocks": [{"id", "name", "contains", "in_S1", "in_S2", "new"}],
                  "structures": [{"key", "name", "idea", "pages", "new_content", "appendix",
                                  "outline": [{"number", "title", "blocks", "description", "pages"}]}]}
The document opens with a map (content blocks down, layouts across, each cell the section that holds the block),
then prints the layouts' outlines four to a row, then a pick sheet with one line for the layout.
"""
import json
import sys

src, out = sys.argv[1], sys.argv[2]
S = json.load(open(src, encoding="utf-8"))
blocks, structs = S["blocks"], S["structures"]


def tex_escape(s):
    return (s or "").replace("&", "\\&").replace("%", "\\%").replace("#", "\\#").replace("_", "\\_")


def where(st, bid):
    secs = [sec["number"] for sec in st["outline"] if bid in sec.get("blocks", [])]
    return ", ".join("\\S" + n for n in secs) if secs else "--"


n = len(structs)
colw = 20.6 / n
head = " & ".join("\\textbf{" + st["key"] + "}" for st in structs)
lines = ["\\noindent\\textbf{The map.} Each row is a block of content; each column a layout; each cell the section "
         "that holds the block in that layout. Blocks in italics are new content that only some layouts add.",
         "\\par\\smallskip{\\small",
         "\\begin{longtable}{@{}p{5.4cm}" + ("p{%.2fcm}" % colw) * n + "@{}}\\toprule",
         "Content block & " + head + "\\\\\\midrule\\endhead"]
for b in blocks:
    name = tex_escape(b["name"])
    name = "\\emph{" + name + "}" if b.get("new") else name
    lines.append(name + " & " + " & ".join(where(st, b["id"]) for st in structs) + "\\\\")
lines.append("\\midrule")
lines.append("Main-text pages (est.) & " + " & ".join(str(st.get("pages", "")) for st in structs) + "\\\\")
lines += ["\\bottomrule\\end{longtable}}", "\\par\\smallskip",
          "{\\small " + "\\par ".join("\\textbf{" + st["key"] + "} " + tex_escape(st["name"]) + ". " +
                                     tex_escape(st["idea"]) for st in structs) + "}\\par"]
preface = "\n".join(lines)


def outline_tex(st):
    t = ["\\emph{" + tex_escape(st["idea"]) + "}\\par\\smallskip"]
    for sec in st["outline"]:
        pages = sec.get("pages")
        pg = f" ({pages:g} pp.)" if isinstance(pages, (int, float)) else ""
        t.append("\\textbf{" + tex_escape(str(sec["number"])) + "\\enspace " + tex_escape(sec["title"]) + "}" + pg +
                 "\\par\\nopagebreak{\\small " + tex_escape(sec.get("description", "")) + "}\\par")
    t.append("\\smallskip{\\small\\textbf{Appendices.} " + tex_escape(st.get("appendix", "")) + "}\\par")
    if st.get("new_content"):
        t.append("{\\small\\textbf{New content.} " + tex_escape(st["new_content"]) + "}\\par")
    t.append("{\\small\\textbf{Main text.} about " + str(st.get("pages", "?")) + " pages.}")
    return "\n".join(t)


rows = []
for i in range(0, n, 4):
    group = structs[i:i + 4]
    rows.append({"id": f"S.{i // 4 + 1}", "title": "Layouts " + ", ".join(st["key"] for st in group),
                 "diff": "; ".join(f"{st['key']}: {tex_escape(st['name'])}" for st in group),
                 "options": [{"key": st["key"], "label": tex_escape(st["name"]), "where": "",
                              "tex": outline_tex(st)} for st in group]})
spec = {"part": "1", "title": "Part 1 — Layouts of the whole paper",
        "subtitle": "S1 is the rewrite, S2 the original without Section 2; S3 onward are new. Every layout keeps all "
                    "of the main text's content.",
        "preface": preface, "rows": rows,
        "pick_rows": [{"id": "S", "title": "Layout", "keys": [st["key"] for st in structs]}]}
json.dump(spec, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out, len(rows), "rows,", n, "layouts,", len(blocks), "blocks")
