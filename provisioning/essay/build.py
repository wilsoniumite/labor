# build.py — the essay's reading copies: essay.md -> essay.html (pandoc) -> essay.pdf (Chromium, through Node's playwright).
# It uses the paper's builder (paper/build.py) with a few rules changed for an essay: no figure or table numbers, since the
# text never refers to one, and the text set ragged on the right.
#
# Run from provisioning/:  python3 essay/build.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "paper"))
import build  # noqa: E402

build.CSS += """
html { font-size: 11.6pt; line-height: 1.55; }
p { text-align: left; hyphens: manual; }
figcaption::before, caption::before { content: none; }
figcaption { color: #555; }
h2 { font-size: 1.42em; margin-top: 2.1em; }
h3 { font-size: 1.12em; margin-top: 1.6em; }
ol { padding-left: 1.4em; }
li, li p { hyphens: manual; }
hr { border: 0; border-top: 0.7px solid #999; margin: 2.4em 0 1.4em 0; }
td, th { text-align: left; }
table { font-size: 0.86em; }
"""

if __name__ == "__main__":
    md, page, paper = (os.path.join(HERE, "essay." + ext) for ext in ("md", "html", "pdf"))
    build.html(md, page)
    print("wrote", page)
    build.pdf(page, paper)
    print("wrote", paper)
