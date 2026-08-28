# lint_pinning.py — mechanical sweeps over paper/pinning.html
# (the rewrite's version of the old paper's mechanical check battery).

import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(HERE, "..", "paper", "pinning.html")
html = open(PAPER, encoding="utf-8").read()

fails = []
def check(name, cond, detail=""):
    print(("  ok  " if cond else "  FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        fails.append(name)

# 1. tag balance
for tag in ["p", "div", "h2", "h3", "figure", "figcaption", "table", "ol", "ul", "li",
            "i", "b", "sub", "sup"]:
    n_open = len(re.findall(rf"<{tag}[ >]", html))
    n_close = len(re.findall(rf"</{tag}>", html))
    check(f"tag balance <{tag}>: {n_open}/{n_close}", n_open == n_close, f"{n_open} vs {n_close}")

# 2. zero curly quotes / apostrophes
curly = re.findall(r"[‘’“”]", html)
check("zero curly quotes/apostrophes", len(curly) == 0, f"{len(curly)} found")

# 3. figures exist on disk at their relative paths
for m in re.findall(r'src="([^"]+)"', html):
    path = os.path.normpath(os.path.join(HERE, "..", "paper", m))
    check(f"figure exists: {m}", os.path.exists(path))

# 4. every <img> has non-empty alt
imgs = re.findall(r"<img[^>]*>", html)
check("all figures carry alt text", all('alt="' in i and 'alt=""' not in i for i in imgs), f"{len(imgs)} imgs")

# 5. head hygiene
check("html lang=en", '<html lang="en">' in html)
check("<title> present", "<title>" in html)

# 6. banned coined terms in body text (case-insensitive; allowed: 'fork').
#    The paper reads as timeless: no reference to any prior draft, so the
#    ban list also covers 'long draft' and the old title outright.
body = html[html.index("<body>"):]
body_scrubbed = body
for term in ["waterline", "demolition", "the link", "fortified", "fortification",
             "george pair", "corner regime", "corner-above", "corner-below",
             "long draft", "supersede"]:
    hits = re.findall(term, body_scrubbed, flags=re.I)
    check(f"banned term absent: '{term}'", len(hits) == 0, f"{len(hits)} hits")

# 7. citation closure: every (Author Year) in text has a References entry, by surname+year
refs_block = html[html.index('<div class="refs">'):]
ref_entries = re.findall(r"<p>([^<(]+)\((\d{4})\)", refs_block)
ref_keys = set()
for names, year in ref_entries:
    surname = names.strip().split(",")[0].strip()
    ref_keys.add((surname, year))
text_block = body[:body.index('<div class="refs">')]
plain = re.sub(r"<[^>]+>", "", text_block)
cited = set()
for m in re.finditer(r"([A-Z][A-Za-zé&\-]+)[^.()]{0,60}?\((\d{4})\)", plain):
    cited.add((m.group(1), m.group(2)))
# check the reference list is not orphaned: each ref surname+year appears somewhere in text
orphans = []
for surname, year in sorted(ref_keys):
    raw = surname.split()[0]
    candidates = {raw, raw.replace("&eacute;", "e")}
    if not any(re.search(re.escape(p) + r"[^.]{0,120}?" + year, plain) for p in candidates):
        orphans.append(f"{surname} {year}")
check("no orphaned reference entries", len(orphans) == 0, "; ".join(orphans))

# 8. structure counts
n_props = len(re.findall(r"<b>Proposition", html)) + len(re.findall(r"<b>Lemma", html)) + len(re.findall(r"<b>Corollary", html))
n_h2 = len(re.findall(r"<h2", html))
words = len(re.sub(r"<[^>]+>", " ", text_block).split())
print(f"\n  info: {n_h2} h2 sections, {n_props} numbered results, ~{words} words body (main+appendix, pre-refs)")

main_end = body.index("Appendix A.")
main_words = len(re.sub(r"<[^>]+>", " ", body[:main_end]).split())
print(f"  info: main text ~{main_words} words (target ~9,000)")

# assert-forward soft metrics (brief rule of 2026-08-13): em-dash density
# and the presuppose-and-characterize pattern "the X that/which Y treats/takes".
dashes = body.count("&mdash;")
per_k = 1000 * dashes / max(words, 1)
presup = re.findall(r"the [a-z&;#\- ]{1,40}(?:that|which) [a-z ]{1,30}(?:treats?|takes?|leaves?) ", plain)
print(f"  info: em-dashes {dashes} (~{per_k:.1f} per 1,000 words); presuppose-pattern hits: {len(presup)}")

# speak-as-the-author soft metrics: authorial possessives should be rare
# ("this paper" as plain subject is allowed; "the author" only in the
# disclosure/AI-note/draftline).
n_papers_poss = len(re.findall(r"the paper's", plain, flags=re.I))
n_author = len(re.findall(r"the author", plain, flags=re.I))
check("hedge absent: 'to the author's knowledge'", "to the author's knowledge" not in plain.lower())
print(f"  info: \"the paper's\" x{n_papers_poss}; \"the author\" x{n_author} (disclosure/notes expected)")

# register hard-bans, mechanized after the 'keeps the arithmetic honest'
# miss (hand inventories tuned to one surface form let the predicate form
# through three passes). Scope: body up to the Acknowledgements, whose
# text is Stella's verbatim and exempt from register rules.
ack_cut = plain.index("Acknowledgements") if "Acknowledgements" in plain else len(plain)
register_scope = plain[:ack_cut].lower()
for phrase in ["honest", "honesty", "note that", "note now", "reading it as",
               "worth noting", "worth stating", "worth saying", "worth ending",
               # control-vocabulary ban (2026-08-19): planning-layer idiom
               # (blocks/switches/dials/cast) leaked into the environment
               # appendix; the paper describes economies, not its own
               # architecture — model-states are "configuration", "case",
               # "limit", "restriction".
               "extension block", "wedge block", "government block",
               "k block", "preference block", "machine block",
               "blocks on", "blocks off", "full cast", "the dials",
               "turn on appendix", "switch on", "switched on",
               # poetic-register ban (2026-08-19, her 'floor dies' catch):
               # personified life-cycle verbs on model objects and ornate
               # price diction. ' dies' spaced to spare 'subsidies'.
               "dear", " dies", "outlive", "went dormant", "backdrop",
               "comes to rest", "walks the floor", "lifts off",
               "labor-hungry", "plumbed", "reservoir", "eats the budget",
               "last variable standing", "blind in opposite", "summon",
               "on display", "thicken", "society burns"]:
    hits = register_scope.count(phrase)
    check(f"register: '{phrase}' absent from body", hits == 0, f"{hits} hits")

# italic-variable sentinels (2026-08-19): in prose (outside .eq displays,
# the references, and the back matter after Acknowledgements), every Greek
# variable entity must sit inside <i>…</i>. Write new prose bare and run
# code/italicize_math.py; this catches what slipped through.
prose = body[:body.index("<h2>Acknowledgements")] if "<h2>Acknowledgements" in body else body
prose = re.sub(r"<div class=\"eq\">.*?</div>", " ", prose, flags=re.S)
prose = re.sub(r"<div class=\"refs\">.*?</div>", " ", prose, flags=re.S)
bare = []
for ent in ["&rho;", "&lambda;", "&gamma;", "&sigma;", "&eta;", "&kappa;",
            "&micro;", "&tau;", "&delta;", "&epsilon;", "&omega;", "&beta;",
            "&alpha;", "&phi;", "&psi;"]:
    for m in re.finditer(re.escape(ent), prose):
        if prose[max(0, m.start()-3):m.start()] != "<i>":
            bare.append(f"{ent}@{m.start()}")
check("italic variables: no bare Greek entity in prose", len(bare) == 0,
      "; ".join(bare[:6]) + ("..." if len(bare) > 6 else ""))

# claim-status tags (v2 dynamics; structure memo, STATE log 32): every
# in-text citation of a transition result T1–T5 must carry an epistemic
# label in the same paragraph — "numerically verified" (T1–T3 experiment
# results), "conjecture" (T5 until promoted), or "theorem"/"proposition"
# (proof-grade: T1's b_I = 0 closed form, T4's entry-margin algebra).
# Hard-fail otherwise. Vacuous until Phase 3 drafts §8; the fixture
# self-test keeps the family honest meanwhile.
STATUS_LABELS = ("numerically verified", "conjecture", "theorem", "proposition")

def status_tag_violations(text):
    out = []
    for i, para in enumerate(re.split(r"</p>|</li>|</figcaption>", text)):
        plain = re.sub(r"<[^>]+>", " ", para)
        for m in re.finditer(r"\bT([1-5])\b", plain):
            if not any(lbl in plain.lower() for lbl in STATUS_LABELS):
                out.append(f"T{m.group(1)}@para{i}")
    return out

check("claim-status self-test: labeled fixture passes, bare fixture fails",
      status_tag_violations("<p>T1 (numerically verified) decays.</p>") == []
      and status_tag_violations("<p>T5 says the wage dips.</p>") != [])
scope_tags = re.sub(r"<div class=\"refs\">.*?</div>", " ", html, flags=re.S)
viol_tags = status_tag_violations(scope_tags)
check("claim-status tags: every T1–T5 citation carries its epistemic label",
      len(viol_tags) == 0, "; ".join(viol_tags[:6]))

print(f"\n{'ALL GREEN' if not fails else 'FAILURES: ' + str(len(fails))}")
sys.exit(1 if fails else 0)
