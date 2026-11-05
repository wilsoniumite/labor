# strip_comments.py IN OUT — drop LaTeX comments as TeX does (whole comment lines, and inline comments).
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
s = re.sub(r"(?m)^[ \t]*(?<!\\)%.*\n", "", s)
s = re.sub(r"(?<!\\)%.*", "", s)
open(sys.argv[2], "w", encoding="utf-8").write(s)
