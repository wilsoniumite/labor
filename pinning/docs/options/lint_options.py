"""lint_options.py — style and real-difference checks for the written options of a rows file.

    python3 -B lint_options.py ROWS.json [--aux-original A] [--aux-rewrite B]

For every option written for the option documents (a "tex" option, not text extracted from a version of the
paper), report:
- style: em dashes, "load-bearing", stock words Johan dislikes, "not X but Y" contrasts, "turns";
- real difference: its word-level similarity to every other option of the row; above 0.75 the two are close to a
  rewording, so the new one should be dropped or replaced by a pointer to the other (same_as).
Exit 1 if anything is flagged.
"""
import difflib
import json
import re
import sys

from build_options import Sources, convert, norm, strip_comments

STOCK = ["crucial", "crucially", "pivotal", "profound", "striking", "remarkable", "remarkably", "notably",
         "importantly", "delve", "underscore", "underscores", "landscape", "navigate", "leverage", "nuanced",
         "multifaceted", "seamless", "intricate", "realm", "testament", "foster", "unpack", "shed light", "tapestry",
         "load-bearing", "load bearing", "vibrant", "showcase", "paradigm"]


def words(tex):
    t = strip_comments(tex)
    t = re.sub(r"\$[^$]*\$", " M ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    return re.findall(r"[A-Za-z']+|\d+(?:\.\d+)?", t.lower())


def style(tex):
    flags = []
    t = strip_comments(tex)
    n_em = t.count("---") + t.count("\u2014")
    if n_em:
        flags.append(f"{n_em} em dash(es)")
    low = re.sub(r"\$[^$]*\$", " ", t.lower())
    for w in STOCK:
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            flags.append(f"stock word '{w}'")
    for m in re.finditer(r"\bnot\b[^.;:]{0,80}?\bbut\b", low):
        flags.append("not-X-but-Y: '" + m.group(0)[:70] + "'")
    for m in re.finditer(r"\bturns?\b(?! out)", low):
        flags.append("'turns'")
    return flags


def main():
    args = sys.argv[1:]
    kw = {}
    for flag, key in (("--aux-original", "aux_original"), ("--aux-rewrite", "aux_rewrite")):
        if flag in args:
            i = args.index(flag)
            kw[key] = args[i + 1]
            del args[i:i + 2]
    spec = json.load(open(args[0], encoding="utf-8"))
    src = Sources(kw.get("aux_original"), kw.get("aux_rewrite"))
    bad = 0
    for row in spec["rows"]:
        texts = {}
        for o in row.get("options", []):
            if "same_as" in o:
                continue
            if "src" in o:
                raw, doc = src.get(o["src"])
                texts[o["key"]] = (convert(raw, src.aux[doc]), False)
            else:
                texts[o["key"]] = (o["tex"], True)
        for k, (t, written) in texts.items():
            if not written:
                continue
            msgs = style(t)
            for k2, (t2, _) in texts.items():
                if k2 == k:
                    continue
                a, b = words(t), words(t2)
                if len(a) > 12 and len(b) > 12:
                    r = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
                    if r > 0.75:
                        msgs.append(f"{r:.2f} similar to {k2} (a rewording?)")
            if msgs:
                bad += 1
                print(f"{row['id']}-{k}: " + "; ".join(msgs))
    print(f"{bad} option(s) flagged")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
