# italicize_math.py — wrap math variables in <i>…</i> throughout the prose of
# paper/pinning.html (her rule, 2026-08-19: all variables italic in prose).
# Convention mirrors TeX: Latin variables and lowercase Greek italic;
# uppercase Greek (Δ, Λ, Σ), operator names (max, min), digits, and bold
# vectors upright. .eq displays are already italic via CSS and are skipped,
# as are the references and the Acknowledgements (verbatim text).
#
# IDEMPOTENT: text already inside <i>…</i> is never rewrapped. Maintenance
# workflow: write new prose bare, re-run this script, re-run lint.
# Run: ../venv/Scripts/python.exe code/italicize_math.py   (from the-link-revision/)

import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(HERE, "..", "paper", "pinning.html")
html = open(PAPER, encoding="utf-8").read()

START = html.index('<div class="abstract">')
END = html.index('<h2>Acknowledgements</h2>')
head, region, tail = html[:START], html[START:END], html[END:]

GREEK = ("alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|micro|nu|"
         "xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega")
COMBINING = r"(?:&#77[012];)*"   # macron / tilde / circumflex riders

# blanket single Latin letters that are never English words in this body
BLANKET = list("cfjknqrtuvwxKNPRTXY")

A_PATTERNS = [  # 'a' is the article; only these are the coefficient
    ("a units of machine services", "<i>a</i> units of machine services"),
    ("(a &lt; 1", "(<i>a</i> &lt; 1"),
    ("(a, &lambda;", "(<i>a</i>, &lambda;"),
    ("(a = ", "(<i>a</i> = "),
    ("a + &lambda;", "<i>a</i> + &lambda;"),
    ("content a, plus", "content <i>a</i>, plus"),
    ("as a varies", "as <i>a</i> varies"),
    ("a(1+&delta;)", "<i>a</i>(1+&delta;)"),
    ("a(&delta;+d)", "<i>a</i>(&delta;+d)"),
    ("1 &minus; a", "1 &minus; <i>a</i>"),
    ("(1&minus;a)", "(1&minus;<i>a</i>)"),
]
D_PATTERNS = [  # 'd' appears as the (a)-(d) list labels; only these are the wear rate
    ("wear at rate d,", "wear at rate <i>d</i>,"),
    ("(&delta;+d)", "(&delta;+<i>d</i>)"),
    ("durability (&delta;, d)", "durability (&delta;, <i>d</i>)"),
    ("wear d)", "wear <i>d</i>)"),
]
COMPOUNDS = r"\b(dx|dz|ac|rT|qT|aX)\b"
SUB_BASES = set("ghmpsqrwkxTPK")  # trailing letter before <sub> (p_g, h_e, m_w, ...)

def transform_text(text, next_token):
    # 0. curated 'a'/'d' first, on pristine text
    for old, new in A_PATTERNS + D_PATTERNS:
        text = text.replace(old, new)
    text = re.sub(r"\bPerson i\b", "Person <i>i</i>", text)
    text = text.replace("(I&minus;", "(<i>I</i>&minus;")
    # 1. lowercase Greek entities (with combining riders) -> italic
    text = re.sub(rf"(&(?:{GREEK});{COMBINING})", r"<i>\1</i>", text)
    # 2. L-bar and letter compounds
    text = text.replace("L&#772;", "<i>L&#772;</i>")
    text = re.sub(COMPOUNDS, r"<i>\1</i>", text)
    # 3. mask: list labels, entities, and everything already wrapped
    stash = []
    def mask(m):
        stash.append(m.group(0))
        return f"\x00{len(stash)-1}\x00"
    text = re.sub(r"(?<=\s)\([abcd]\)(?=\s)", mask, text)           # list labels
    text = re.sub(r"<i>.*?</i>", mask, text)                        # wrapped already
    text = re.sub(r"&[a-zA-Z][a-zA-Z0-9]*;|&#\d+;", mask, text)     # entities
    # 4. blanket letters
    for L in BLANKET:
        text = re.sub(rf"\b{L}\b", f"<i>{L}</i>", text)
    text = re.sub(r"(?<!')\bs\b", "<i>s</i>", text)                 # skip possessives
    # 5. trailing subscript base (p_g, h_e, g_s, m_w ... on node boundary)
    if next_token.startswith("<sub"):
        m = re.search(r"([A-Za-z])$", text)
        if m and m.group(1) in SUB_BASES:
            text = text[:m.start()] + f"<i>{m.group(1)}</i>"
    # 6. restore masks
    text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text

tokens = re.split(r"(<[^>]+>)", region)
out = []
eq_depth = refs_depth = 0
b_depth = i_depth = sub_depth = 0
for idx, tok in enumerate(tokens):
    if tok.startswith("<"):
        t = tok.lower()
        if t.startswith("<div"):
            if 'class="eq"' in t: eq_depth = 1
            elif eq_depth: eq_depth += 1
            if 'class="refs"' in t: refs_depth = 1
            elif refs_depth: refs_depth += 1
        elif t == "</div>":
            if eq_depth: eq_depth -= 1
            if refs_depth: refs_depth -= 1
        elif t.startswith("<b>") or t.startswith("<b "): b_depth += 1
        elif t == "</b>": b_depth -= 1
        elif t.startswith("<i>") or t.startswith("<i "): i_depth += 1
        elif t == "</i>": i_depth -= 1
        elif t.startswith("<sub"): sub_depth += 1
        elif t == "</sub>": sub_depth -= 1
        out.append(tok)
        continue
    if eq_depth or refs_depth or b_depth or i_depth or not tok.strip():
        out.append(tok)
        continue
    if sub_depth:
        out.append(re.sub(r"^([A-Za-z]{1,2})$", r"<i>\1</i>", tok))
        continue
    nxt = tokens[idx + 1] if idx + 1 < len(tokens) else ""
    out.append(transform_text(tok, nxt))

new_region = "".join(out)
result = head + new_region + tail
n_i_open = len(re.findall(r"<i[ >]", result))
n_i_close = result.count("</i>")
assert n_i_open == n_i_close, f"<i> imbalance: {n_i_open} vs {n_i_close}"

wrapped_before = len(re.findall(r"<i[ >]", html))
print(f"<i> spans: {wrapped_before} -> {n_i_open} (+{n_i_open - wrapped_before})")
open(PAPER, "w", encoding="utf-8").write(result)

# review sweep: bare single letters still adjacent to math operators, for eyeball
scan = re.sub(r"<div class=\"eq\">.*?</div>", " ", new_region, flags=re.S)
scan = re.sub(r"<div class=\"refs\">.*?</div>", " ", scan, flags=re.S)
scan = re.sub(r"<i>.*?</i>", " ", scan)
scan = re.sub(r"<[^>]+>", " ", scan)
hits = set()
for m in re.finditer(r"(?:^|[\s(])([a-zA-Z])(?=\s?(?:=|&lt;|&ge;|&le;|&gt;|&minus;|&middot;|&rarr;|/|\*|\+))", scan):
    hits.add(m.group(0).strip())
for m in re.finditer(r"(?:=|&lt;|&ge;|&le;|&gt;|&minus;|&middot;|&rarr;|/|\+)\s?([a-zA-Z])(?=[\s.,;:)])", scan):
    hits.add(m.group(1))
print("review — bare letters still near operators (should be empty or benign):",
      sorted(hits) if hits else "none")
