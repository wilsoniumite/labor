r"""Render the paper HTML to a selectable-text PDF.

Usage:
    venv\Scripts\python.exe tools\render_pdf.py <file-url-of-html> <output.pdf>

e.g.
    venv\Scripts\python.exe tools\render_pdf.py ^
        "file:///C:/Users/s6068C/GitHub/laborformal/dynamics/paper/pinning.html" ^
        "dynamics\paper\pinning.pdf"

Goes through Chromium's Skia printToPDF path, which embeds fonts and a
ToUnicode text map: the output is selectable and searchable. Do NOT print
via the "Microsoft Print to PDF" printer device — the Windows driver path
draws every glyph as vector outlines (no text layer, ~20x the size).
Honors the document's @page rule (A4, 2.3cm/2.5cm margins).
"""
import sys
from playwright.sync_api import sync_playwright

src, out = sys.argv[1], sys.argv[2]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(src)
    page.wait_for_load_state("networkidle")
    page.pdf(path=out, prefer_css_page_size=True, print_background=True)
    browser.close()
print("rendered:", out)
