# word_diff_report.py — word-level HTML diff for prose-heavy HTML files
# whose source lines are whole paragraphs (line diffs are unreadable there).
# Usage: python code/word_diff_report.py OLD NEW OUT.html "Title"
# Output: changed words highlighted (del = red strikethrough, ins = green),
# unchanged runs collapsed to a context window with a skip marker.

import difflib
import html
import sys

OLD, NEW, OUT, TITLE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
CONTEXT = 10  # unchanged words shown on each side of a change

a = open(OLD, encoding="utf-8").read().split()
b = open(NEW, encoding="utf-8").read().split()

sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
ops = sm.get_opcodes()

def esc(tok_list):
    return html.escape(" ".join(tok_list), quote=False)

parts = []
n_changes = 0
for k, (tag, i1, i2, j1, j2) in enumerate(ops):
    if tag == "equal":
        run = a[i1:i2]
        first = k == 0
        last = k == len(ops) - 1
        if len(run) <= 2 * CONTEXT + 6:
            parts.append(esc(run))
        else:
            if not first:
                parts.append(esc(run[:CONTEXT]))
            skipped = len(run) - (0 if first else CONTEXT) - (0 if last else CONTEXT)
            parts.append(f'<span class="skip">&#8943; {skipped} unchanged words &#8943;</span>')
            if not last:
                parts.append(esc(run[-CONTEXT:]))
    else:
        n_changes += 1
        if i1 < i2:
            parts.append(f'<del>{esc(a[i1:i2])}</del>')
        if j1 < j2:
            parts.append(f'<ins>{esc(b[j1:j2])}</ins>')

body = " ".join(parts)

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{html.escape(TITLE)}</title>
<style>
body {{ font-family: Georgia, serif; font-size: 12.5px; line-height: 1.75;
       color: #222; max-width: 900px; margin: 30px auto; padding: 0 20px; }}
h1 {{ font-size: 17px; }}
.meta {{ color: #666; font-size: 11px; margin-bottom: 18px; }}
del {{ background: #ffe3e3; color: #8b2020; text-decoration: line-through; padding: 1px 2px; }}
ins {{ background: #e2f4e2; color: #17501a; text-decoration: none; padding: 1px 2px; }}
.skip {{ display: block; color: #999; font-size: 11px; text-align: center;
         margin: 10px 0; font-style: italic; }}
</style></head><body>
<h1>{html.escape(TITLE)}</h1>
<div class="meta">{n_changes} changed regions &middot; old text struck through in red, new text in green &middot; unchanged stretches collapsed</div>
<div>{body}</div>
</body></html>"""

open(OUT, "w", encoding="utf-8").write(page)
print(f"wrote {OUT}: {n_changes} changed regions")
