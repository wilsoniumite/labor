# build.py — the draft's reading copies: draft.md -> draft.html (pandoc) -> draft.pdf (Chromium, through Node's playwright).
# No TeX and no math font are needed: the draft's few formulas are simple enough for pandoc to set in the text's own
# font. For LaTeX: pandoc paper/draft.md -o draft.tex
#
# Run from provisioning/:  python3 paper/build.py

import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
@page { size: A4; margin: 24mm 25mm 24mm 25mm; }
html { font-family: Caladea, "Liberation Serif", "DejaVu Serif", serif; font-size: 11.2pt; line-height: 1.5; color: #111; }
body { max-width: 42em; margin: 2.5em auto; padding: 0 1.2em; hyphens: auto; }
@media print { body { max-width: none; margin: 0; padding: 0; } }
header#title-block-header { margin: 1.5em 0 2em 0; }
h1.title { font-size: 2.0em; line-height: 1.2; margin: 0 0 0.25em 0; font-weight: 700; }
p.subtitle { font-size: 1.25em; margin: 0 0 0.9em 0; color: #333; }
p.author { font-size: 0.95em; color: #444; margin: 0; }
h2 { font-size: 1.3em; margin: 1.9em 0 0.5em 0; line-height: 1.25; break-after: avoid; }
h3 { font-size: 1.07em; margin: 1.4em 0 0.35em 0; break-after: avoid; }
p { margin: 0 0 0.75em 0; text-align: justify; orphans: 3; widows: 3; }
blockquote { margin: 1.4em 0; padding: 0.7em 1em 0.1em 1em; border-left: 3px solid #b5b3ab; background: #f6f5f1; font-size: 0.93em; }
blockquote p { text-align: left; }
figure { margin: 1.5em 0 1.6em 0; break-inside: avoid; counter-increment: figure; }
figure img { display: block; max-width: 100%; margin: 0 auto; }
figcaption { font-size: 0.88em; line-height: 1.4; color: #333; margin-top: 0.6em; text-align: left; }
figcaption::before { content: "Figure " counter(figure) ". "; font-weight: 700; }
table { border-collapse: collapse; margin: 1.3em auto 1.5em auto; font-size: 0.9em; line-height: 1.35; break-inside: avoid;
        counter-increment: table; font-variant-numeric: tabular-nums; width: 100%; hyphens: manual; }
caption { caption-side: bottom; text-align: left; font-size: 0.97em; color: #333; padding-top: 0.6em; line-height: 1.4; }
caption::before { content: "Table " counter(table) ". "; font-weight: 700; }
th, td { padding: 0.3em 0.6em; vertical-align: top; }
thead th { border-top: 1.2px solid #111; border-bottom: 0.7px solid #111; font-weight: 700; vertical-align: bottom; }
tbody tr:last-child td { border-bottom: 1.2px solid #111; }
span.math { white-space: nowrap; }
span.math.display { display: block; text-align: center; margin: 1.0em 0 1.1em 0; font-size: 1.1em; }
sub, sup { line-height: 0; font-size: 0.72em; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 0.84em; }
a { color: inherit; }
section.footnotes, section#footnotes { font-size: 0.88em; margin-top: 2.5em; }
section.footnotes hr, section#footnotes hr { border: 0; border-top: 0.7px solid #999; width: 30%; margin: 0 0 0.8em 0; }
ul { padding-left: 1.3em; }
li { margin-bottom: 0.4em; }
li p { text-align: left; }
h2#references ~ p { text-align: left; hyphens: manual; }
"""

PRINT = """
const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(1);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + src, { waitUntil: 'load' });
  await page.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font-size:8pt;font-family:serif;color:#555;"><span class="pageNumber"></span></div>',
    margin: { top: '24mm', bottom: '24mm', left: '25mm', right: '25mm' } });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
"""


def html(src, out):
    """Markdown to one standalone HTML page, the stylesheet above in its head."""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write("<style>" + CSS + "</style>")
        head = f.name
    subprocess.run(["pandoc", src, "-o", out, "--standalone", "--columns", "10000", "--from", "markdown+smart", "--to", "html5",
                    "-M", "document-css=false", "-M", "lang=en-GB", "-H", head], check=True, cwd=HERE)
    os.unlink(head)


def pdf(src, out):
    """The HTML page printed by Chromium."""
    subprocess.run(["node", "-e", PRINT, src, out], check=True, cwd=HERE)


if __name__ == "__main__":
    md, page, paper = (os.path.join(HERE, "draft." + ext) for ext in ("md", "html", "pdf"))
    html(md, page)
    print("wrote", page)
    pdf(page, paper)
    print("wrote", paper)
