"""Minimal stdlib HTML table extractor: returns list of tables, each a list of rows (list of cell text)."""
from html.parser import HTMLParser
import html as _html, re

class _P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables=[]; self.stack=[]; self.cell=None; self.row=None
    def handle_starttag(self, tag, attrs):
        if tag=='table': self.stack.append([])
        elif tag=='tr' and self.stack: self.row=[]
        elif tag in ('td','th') and self.row is not None: self.cell=[]
        elif tag=='br' and self.cell is not None: self.cell.append(' ')
    def handle_endtag(self, tag):
        if tag in ('td','th') and self.cell is not None and self.row is not None:
            self.row.append(re.sub(r'\s+',' ',''.join(self.cell)).strip()); self.cell=None
        elif tag=='tr' and self.row is not None and self.stack:
            self.stack[-1].append(self.row); self.row=None
        elif tag=='table' and self.stack:
            self.tables.append(self.stack.pop())
    def handle_data(self, d):
        if self.cell is not None: self.cell.append(d)

def tables(path):
    p=_P(); p.feed(open(path,encoding='utf8').read()); return p.tables
