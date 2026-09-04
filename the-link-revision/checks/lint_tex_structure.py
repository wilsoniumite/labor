"""lint_tex_structure.py — structural lint for a LaTeX paper file that has
no local compile (Overleaf is the first compile). Checks, per the-link-
revision house rule: brace balance, $ parity, \\begin/\\end nesting, every
\\ref target has a \\label, labels unique, every \\includegraphics file exists
next to the tex under figures/. Usage:

    python checks/lint_tex_structure.py latex/FILE.tex

Exit 0 and ALL GREEN, or a list of findings and exit 1."""

import os
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
findings = []

# strip comments (unescaped % to end of line) for the counts below
body = re.sub(r"(?<!\\)%.*", "", src)

# braces (ignore escaped \{ \})
stripped = body.replace(r"\{", "").replace(r"\}", "")
depth, line_no = 0, 1
for ch in stripped:
    if ch == "\n":
        line_no += 1
    elif ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth < 0:
            findings.append(f"brace closes below zero near line {line_no}")
            depth = 0
if depth != 0:
    findings.append(f"unbalanced braces: net depth {depth} at end of file")

# $ parity per paragraph (blank-line separated), $$ counted as pairs, \$ ignored
for i, para in enumerate(re.split(r"\n\s*\n", body)):
    dollars = re.sub(r"\\\$", "", para).count("$")
    if dollars % 2:
        head = para.strip().splitlines()[0][:70] if para.strip() else ""
        findings.append(f"odd number of $ in paragraph {i}: {head!r}")

# environments
stack = []
for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", body):
    kind, env = m.group(1), m.group(2)
    ln = body.count("\n", 0, m.start()) + 1
    if kind == "begin":
        stack.append((env, ln))
    else:
        if not stack:
            findings.append(f"\\end{{{env}}} with empty stack at line {ln}")
        else:
            top, tl = stack.pop()
            if top != env:
                findings.append(f"\\end{{{env}}} at line {ln} closes \\begin{{{top}}} from line {tl}")
for env, ln in stack:
    findings.append(f"\\begin{{{env}}} at line {ln} never closed")

# labels / refs
labels = re.findall(r"\\label\{([^}]*)\}", body)
dupes = {l for l in labels if labels.count(l) > 1}
for d in sorted(dupes):
    findings.append(f"duplicate label {d}")
label_set = set(labels)
for m in re.finditer(r"\\(?:eq)?ref\{([^}]*)\}", body):
    if m.group(1) not in label_set:
        findings.append(f"\\ref to missing label {m.group(1)}")

# figure files
tex_dir = os.path.dirname(os.path.abspath(path))
for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", body):
    f = os.path.join(tex_dir, m.group(1))
    if not os.path.exists(f):
        findings.append(f"includegraphics file missing: {m.group(1)}")

n_ref = len(re.findall(r"\\(?:eq)?ref\{", body))
print(f"{os.path.basename(path)}: {len(labels)} labels, {n_ref} refs, "
      f"{len(re.findall(r'\\begin\{', body))} environments, "
      f"{len(re.findall(r'\\includegraphics', body))} figures")
if findings:
    for f in findings:
        print("  FINDING ", f)
    sys.exit(1)
print("  ALL GREEN")
