# STATE — provisioning (P2; resume point for the next session)

**Project:** P2, renamed and re-centred on 2026-11-10: *What pays for consumption* (working title). What consumption is
made of against what pays for it; who holds which claim; what a shift of payments between labour, capital and land does
to each household; and what it would take to change the holdings. The governing document is `SKETCH.md` (v1); read it
first. The companion is P1 (`../pinning/`), which says which way factor payments move.
**Authors:** Stella Wilson; Johan Båge probably; Luna possibly (her words, 2026-11-10).
**Collaboration:** same contract as the sibling threads: working format, sequencing and drafting delegated to Claude;
checks gate absolutely; direct critique over validation; her voice pass re-voices any prose that enters a paper. Code
in plain functions, notebook-cell style.
**Register for prose** (her instruction, 2026-11-10): "please don't be too poetic or terse, nor patronising. A paper
that most smart people would read." Full sentences, terms defined once, no aphorisms, no clipped notes.
**And after reading the first draft** (2026-11-10): "making it more standalone, timeless. People haven't read our
previous 19 point error, or our other paper. They might have heard of the other papers, so referencing them is good
for authority, but you can't rely on someone having read them. And the paper needs to be a fraction more weighty given
the subject matter. Still not poetic or patronising, but a kind of quiet confidence, and the worry of someone who is
usually calm and collected." So the paper describes its own model and data, cites the other paper as a source and
never as a prerequisite, and does not mention the earlier reading of the nineteen points.
**The wall:** this repository is public. Public data only.
**State as of:** 2026-11-10, sixth unit. Assemblies 1 and 2 (first cut) built and gated; sketch v1; the draft in
`paper/` revised to stand alone and given a program for the United States (Section 9), every number in it tied to the
tables by `checks/check_draft.py`.

## For her, first

**P1's Section 9 needs restating before the Economic Modelling package goes.** `../pinning/paper/main.tex` says
"consumption remains substantially more labor-financed than production is labor-intensive ... a gap of about nineteen
percentage points" (Section 9, Figure 7, Appendix F). The gap is a difference of definitions. BEA's production account
counts machines' wear as capital's and sets taxes on production and imports beside the factors; the financing account
is in incomes, which are net of wear. With wear traced back into the labour, capital and land that rebuild the machines,
and taxes and imports set aside, labour makes 0.658 of what consumption buys in 2023 and finances 0.658 of it, and over
2004–2023 the two differ by 0.000 on average (between −0.025 and +0.020). `checks/check_one_basis.py` Q4 and Q6 hold
the numbers. Nothing in `../pinning/` was changed. What the two accounts do show is worth saying there: built from
different data, they agree. The October rewrite (*What Machines Cannot Make*) does not carry the claim; `main.tex`,
the version in the Economic Modelling package, does.

**The draft no longer mentions the earlier reading, or the words "nineteen points"** (her call after the first draft:
the paper stands alone; and her question on the revision, which had kept one sentence of it in the introduction).
Section 3.3 reconciles the Bureau's 0.472 with 0.658 step by step and says no more than that; Figure 1's note reads
"wear, taxes and imports". The correction to `main.tex` is still hers to make there.

**Read the agreement for what it is.** Income and product are two sides of one ledger, so the two accounts should
agree once they are on one basis, up to what is saved, taxed or traded. The finding is that the earlier comparison was
not on one basis, and that the financing account's central case sits where the production side says it should. The
draft says so in Section 3.3. It is a correction and a cross-check more than a discovery.

## Her calls, 2026-11-10

1. **P2 is this paper** ("P2 renamed, I think"). `../progress_and_prosperity/PLAN.md` carries the new entry.
2. **three-taxes is absorbed** ("Three taxes probably won't get revived by me so you can absorb it if you want").
3. **Capital is in** ("Yes, I realise now we need to tackle capital").
4. **The distortion conjecture is conditional** ("Sure on distortion"): a section only if the participation test
   supports it.
5. **Authors and register** ("Johan will probably be on it. Luna might be too. Keep going, I want to see where you
   take this"), with the register above.
6. **The paper recommends a mix, for the United States** ("yeah, lets put the mix into the paper, puts some action
   behind it"; "USA"). This replaces the earlier stance that instruments appear only where they size a base.
7. **Weave it in; more pictures; what the United States does now** ("Yeah, weaving it in is good, and having more
   tables and figures is good. Right now, section nine reads like a blob of numbers in prose. I want more pictures,
   and i want to know what the US does now and how those should be changed").
8. **Her storyline for the moral claim** ("Current wealth holders justify that wealth because standard thinking
   attributes that wealth to work, intelligence, and giving back to society. The idea that money represents value,
   and therefore what you contribute to society. I think that framing is fine, so long as it is true, and [this] is
   what we have to do to make it most true"), with her questions: is it fair, does it fall apart if machines do nine
   tenths of the work, is half and half the better rule, and can an arbitrary number be escaped. Section 10 is the
   draft answer; she has not yet accepted it.

## Claude's calls, in her veto window

- **The folder is `provisioning/`**, after the old P2's provisioning identity. A placeholder; rename freely.
- **three-taxes stays where it is.** Only its `STATE.md` header changed.
- **The spine is positive, with one benchmark** (a household matched to its basket), up to Section 8. Section 9 then
  recommends, on her call 6.
- **What the program contains** (Section 9; every size from `code/program.py`). A holding in common of about a fifth,
  paid as an equal dividend: the corporate income tax put on a cash-flow base at its present 21 percent, a tax on the
  growth of land rent, charges on the commons, and purchases for the remainder. Funded saving out of wages for the
  four tenths above the median, whom no holding in common can match. Contributions on wages replaced step by step by a
  tax on consumption. No further tax on the return to capital, and no universal income beyond the dividend.
- **"Matched" in Section 9 is the share identity's sense**: a group's share of the claims on capital and land equals
  its share of labor income. Transfers and baskets are left out of that arithmetic, and the section says the sizes
  are for the average basket.
- **Section 10 is a draft of the authors' position on fairness**, written to her storyline and hers and Johan's to
  change. Judgments made on their behalf there: that the standard of contribution is "a reasonable standard"; that a
  tax on the growth of rent is "a fair division" between people who bought land in good faith and the public; that
  inherited capital is left aside; that a second premise is needed (no one left without means) and that the dividend
  is how the program meets it. What it adds to her storyline: pay measures what would be lost if the person stopped,
  so a worker's contribution falls when a machine learns the job; and the share held in common is an outcome of the
  standard, about half in the model's limit, with two numbers still chosen (the public's stake, and what is enough).
- **How Section 9 was made less of a blob.** Table 4 sets what the United States does now beside what the program
  would change; four figures carry the sizes (where each group stands, what a holding in common would pay, the years
  of saving, what is taxed now); the prose keeps the argument and few numbers. The statute citations moved to
  Appendix B.
- **What in Section 9 is argued and not computed.** That a tax on all spending at one rate is neutral in the model
  economy and paid in proportion to income (it follows from hours being fixed and the required return unchanged; the
  shares themselves are held). That a stake taken through a cash-flow tax pays out less while capital grows.
- **The paper no longer opens on a gap.** After assembly 1 it opens on the three accounts agreeing, and its subject is
  who holds the claims (`SKETCH.md`, "What changed from v0").
- **Corporate income that is not paid out is counted as the households'**, in proportion to dividends. Without it every
  decile looks more dependent on labour than it is (check W2 shows both).
- **P1 is not touched.**
- **The companion economy is the rewrite's** (*What Machines Cannot Make*, October 2026, the PDF she uploaded; its
  source is not in this repository). `code/paper_path.py` re-derives it from the printed equations and parameters.
- **The draft is Markdown** (`paper/draft.md`), with a script that renders it to HTML and PDF for reading. No TeX is
  installed in the cloud session; pandoc turns the same file into LaTeX when she wants it in Overleaf. Its two
  displayed formulas are written so that pandoc can set them in the text's font (no math font is installed either).
- **The draft has no footnotes.** What is provisional is said in the text where it is used, and in a status note at
  the top.
- **The draft's names for the groups** are the poorer half, the next four tenths and the richest tenth. The code and
  the stored tables keep "bottom half" and "top tenth".
- **Coverage is quoted from the rewrite** (0.33, range 0.18 to 0.59, its Section 10.1), not from the September version
  (0.30, 0.15 to 0.59), because the rewrite is the companion the draft cites.
- **Two citations were added to the sketch's list** once Crossref confirmed them: Sinai and Souleles 2005 (owning as a
  hedge against rent) and Freeman 2015.
- **The paper is in American spelling** (labor, center, gray), as *What Machines Cannot Make* is. The figures follow.
  The code, the stored tables and these notes keep their spelling.
- **How the paper stands alone.** The model economy is described in Section 6.1 and stated in Appendix A, with its
  parameters, targets and path; Båge and Wilson (2026) is cited for the derivations. The data and methods are in
  Appendix B. The second account is described where it is used (Section 3.3) and is no longer called "the financing
  account". The reference list follows the October paper's style, without DOIs or notes; what is unconfirmed is in the
  drafting note at the top of the draft and in `SKETCH.md` section 10.
- **Where the weight is.** The introduction says why the position is worth examining before anyone knows whether it
  will matter; Section 8.3 calls the rising price of ownership in years of wages "the most troubling result in the
  paper"; the conclusion ends on settling ownership "while it is still cheap to settle". Nothing else was raised in
  pitch. If it reads as too much or too little, those three places are the dial.

## What exists

| File | What it is | Gate |
|---|---|---|
| `SKETCH.md` | The paper sketch, v1 | — |
| `code/one_basis.py` → `data/one_basis.csv`, `data/one_basis_vintage.json`, `data/nipa_corporate.csv` | What consumption is made of, 1997–2023, with machines' wear traced back into the claims that rebuild them; shelter and the rest apart | `checks/check_one_basis.py`, 18 green. Needs the BEA files in the gitignored cache (`python3 code/one_basis.py --pull`). The engine reproduces the λ thread's series to 1e-16 and `chains.json`'s investment bundle to 1e-16 |
| `code/exposure.py` → `data/exposure_deciles.csv`, `data/exposure_groups.csv` | Each income decile's income against what consumption is made of, 2004–2023; who holds which claim; shares of income at other labour shares and common shares; the 2004–2023 shift-share | `checks/check_exposure.py`, 16 green. Reads only files in the repository |
| `code/paper_path.py` | The rewrite's calibrated economy, re-derived; who is paid along the path, what the claims cost, who bears a tax on interest | `checks/check_paper_path.py`, 25 green |
| `code/rent_base.py` | The site-rent base a person against income, a poverty-line bundle and GDP, 1947–2024 | `checks/check_rent_base.py`, 5 green |
| `code/wage_shortfall.py` | Where the production wage fell short of its 1950–73 pace | **Not gated here.** It reads the backward model's panel, on `claude/focused-bardeen-aciw2z` (at 457e38b) |
| `code/one_basis_tables.py` | The stored tables read without the BEA files (what is made; the financing panel; the Bureau's published grouping) | used by the figures, the decile account and the draft's check |
| `code/nipa_fiscal.py` → `data/nipa_fiscal.csv`, `data/nipa_fiscal_vintage.json` | What the United States taxes and pays out, by kind, 2000–2024 (BEA Tables 3.1, 3.5 and 3.12) | needs NipaDataA.txt in the cache to rebuild; the stored table is what everything reads, and `check_program.py` Q9c ties its vintage to the one-basis account's |
| `code/program.py` | The sizes behind Sections 9 and 10: how far each group is from a matched position, with and without a fifth in common; what a common fifth pays; the years of saving that close the gap; taxes on corporate income and the growth of site rent as claims the public could hold; taxes and benefits by kind; who is paid for what along the model's path under the program | `checks/check_program.py`, 18 green. Reads only files in the repository |
| `code/figures.py` → `paper/figures/` | The draft's eleven figures | drawn from the stored tables; colours validated with the dataviz skill's script |
| `paper/draft.md`, `paper/build.py` → `paper/draft.html`, `paper/draft.pdf` | The draft (about 15,000 words, 33 pages, five tables, eleven figures, two appendices) and its reading copies. Needs pandoc and Node's playwright | `checks/check_draft.py`, 173 green: each sentence or table row that prints a number is rebuilt from the tables and must be in the draft, and numbers given in words sit inside stated bands. It also holds Appendix A's parameters, targets and path against `code/paper_path.py`. With the backward model's panel as an argument it holds Section 5's wage accounting too (177 green) |

Run from this folder: `python3 checks/check_one_basis.py`, `python3 checks/check_exposure.py`,
`python3 checks/check_paper_path.py`, `python3 checks/check_rent_base.py`, `python3 checks/check_program.py`,
`python3 checks/check_draft.py` (numpy, pandas; the first also scipy and openpyxl through `../paths/code/chains.py`).
All six were green on 2026-11-10: 18, 16, 25, 5, 18 and 173. To rebuild the reading copies: `python3 code/figures.py`, then `python3 paper/build.py`.

**Not held on this branch**, and said so in the draft: Section 5's wage accounting (`code/wage_shortfall.py`, the
backward model's panel) and Section 7.4's land-tax figures (`consumption/lvt/NOTES_us.md` on the `consumption`
branch). Both were read against their sources on 2026-11-10 and match.

**Data fetched this session** (all from apps.bea.gov, into the gitignored cache
`../progress_and_prosperity/lambda/data/cache/`): the two input-output zips, ValueAdded.xlsx, GrossOutput.xlsx, Fixed
Assets sections 2 and 3, NipaDataA.txt and SeriesRegister.txt. Six of the seven files `chains.json` records are
byte-identical to its vintage; NipaDataA.txt is newer (4 November 2026). Nothing was substituted.

## What the six units found

1. **Three accounts agree** (B1). Labour makes 0.658 of what consumption buys, finances 0.658 of it, and is 0.666 of
   households' income once corporate income that is not paid out is counted. The first two differ by a point on average
   over twenty years. P1's nineteen points are wear (+0.079), taxes and imports (+0.128) and the engine (−0.021).
2. **Who holds the claims** (B3). The bottom nine tenths are long labour by about a tenth of income; the top tenth is
   short by 0.14 and holds 0.67 of the claims on capital and land (0.62 in 2004). Everyone together is exposed by
   +0.008.
3. **The shift so far is small, and most of it is not between claims** (B3, B4). 2004–2023: the top tenth gained 4.2
   points of market income, 1.4 from payments moving between claims and 2.8 from holding more of each. The next four
   tenths lost 4.1. The bottom half's share barely moved.
4. **Shelter is where a wage earner is most exposed** (B2). Labour is 0.23 of the factor cost of shelter and 0.74 of
   the rest; a household on wages alone that spends 30–40% on shelter is exposed by 0.42–0.47.
5. **A common share of about a seventh holds the bottom half** (B6) at any labour share; nothing short of 0.86 holds
   the next four tenths.
6. **A tax on the return to capital is paid by wages** (B6): at 20%, revenue 6.3% of income, wages −6.1, real income
   −6.5%. A cash-flow tax or a purchase moves the same share with nothing else changed.
7. **The window** (B6): the claims on interest and rent cost 6.7 years of the wage bill today and 48 at t = 1.
8. **The floor is cheaper than it was** (B5, B6): 9–18% of GDP in 2024, 18–35% in 1975, 27–52% in 1955.
9. **The stagnation is mostly not a land story** (B4): shelter's price is 8% of the wage's shortfall and labour's share
   16%; slower output per hour is 42% and dispersion inside labour 30%.
10. **Corrections the draft's own check and reading pass forced.** Labour pays for 8 points more of spending from
    current income than it makes (7 on average), not 7. Taxing only the growth of rent does not avoid a fall in the
    price of land: the price falls by the share of value that growth accounts for (40% at 2 and 5 percent), against
    85%. Net surplus is not "several times" the cost of a floor: the floor is 14 to 27 cents of the consumer's dollar
    and net surplus 30.5. The financing account's bounds are 12 points below its centre and 14 above on average.

Also from the session, belonging to other threads and not landed here: a no-change benchmark for the backward model's
out-of-sample splits (the main case 5.2 against 4.6 from 1995, 12.7 with the utility held after 1990; 6.7 against 13.6
from 1985); in the stored main case land's share of a machine's cost is 0.33 in 1950 and 4e-8 in 2024, and labour's
lost share of income since 1970 goes to interest (5.1 of 6.4 points), not land (0.3). Those are `us-record`'s to keep
or drop.

11. **What making the paper stand alone turned up.** The second account has three parts, and the paper now gives them:
    labor income pays for 65.8% of consumption in 2023, other current income for 23.6%, savings or borrowing for 10.6%.
    The four tenths above the median lose the most points under a larger shift (11.0 against 4.6), but in proportion to
    its own share the poorer half loses slightly more (32% against 28%); the draft says both. Baxter and Jermann's
    finding is about the returns to human and physical capital, not labor and capital income, and the draft now says
    what their abstract says. On the model's path income is 32 times as large at t = 1 and the real wage 9 times, so
    the path is about the division of a gain, and the draft says so.

12. **The size of the task, and how the program divides it** (Section 9). For every dollar of labor income the poorer
    half has 24 cents from capital and land, the next four tenths 27, the richest tenth 96; a matched group would have
    51. The poorer nine tenths hold about half the claims that would match them, and 31.7% of all the claims would
    have to pass to them: 9.4 points to the poorer half, 22.3 to the next four tenths. A fifth in common leaves the
    poorer half 1.0 point short and the next four tenths 19.2. The corporate income tax (8% of the income of capital
    and land) and the growth of site rent (5 to 8% after 25 years at 2%) come to 13 to 16%, about a seventh, which is
    what keeps the poorer half's share whole. A common fifth pays $4,493 a person a year, 29 to 58% of a poverty-line
    bundle. Saving 5% of wages closes the upper middle's gap in 34 years at a 5% return (17 at 10%); with labor paid
    what it is paid at t = 1, in 76.

13. **What the United States does now, and where the standard of contribution leads** (Sections 9 and 10). Of all taxes
    and contributions in 2023 ($7,147bn): personal taxes 40%, contributions on wages 25%, sales and other taxes 17%,
    property taxes 10% ($697bn), taxes on corporate income 9% ($608bn). Social benefits $4,144bn, none paid to
    everyone; a common fifth ($1,515bn) would pay out more than Social Security ($1,357bn). In the model economy under
    the program, what is held in common (the public's fifth of the return to capital, and the rent of land above what
    it paid at the start) is 6% of income at the start, 40% at t = 1 and 48% at t = 2, while work goes from 60% to 17%
    to under 1%. So "half and half" is where the program arrives, not a number put in. And the exposures cancel
    (+0.10, +0.115, −0.14; everyone +0.008), so before a shift matching is an exchange; after it, a transfer.

## Next

0. **Her read of the draft and of `SKETCH.md` section 11**, P1's Section 9 first.
1. **Baskets by decile and tenure** (assembly 2's second half): the consumer expenditure machinery is on the
   `consumption` branch. Until then B3 gives every decile the average basket, and the paper says so.
2. **The rest of the verify pass** on section 10's ledger. Done on 2026-11-10: every reference's details against
   Crossref, RePEc or Open Library, except the title of Brown's chapter; Keynes's two forecasts against the essay's
   text; and what the draft attributes to nine papers against their abstracts (`SKETCH.md` section 10 has the list).
   Not done: what it attributes to Brown, Meade (twice), Auerbach and Kotlikoff, Musgrave, Paine and George, which
   needs the books. For Section 9, the rates of the corporate income tax (21%) and of the tax for old-age, survivors
   and disability insurance (6.2% on each side) were read in the US Code at law.cornell.edu. Two statements were not
   confirmed, because ssa.gov, taxpolicycenter.org, congress.gov, oecd.org, cbo.gov, gao.gov and jct.gov all refused
   the session's requests (HTTP 403): that there is no broad federal tax on consumption, and that Social Security
   pays current pensions out of current contributions. Three more in Table 4 are from general knowledge: that
   property taxes fall on land and buildings together, that interest, dividends and gains are taxed as personal
   income, and that no social benefit is paid to everyone. The draft's drafting note lists all five.
3. **Capital in the record** (assembly 4): net surplus split into the normal return and the rest; funded pensions as
   claims; pension systems as cases.
4. **The long run of B1** (assembly 6): the production account before 1997 on one basis.
5. When `us-record` and `consumption` are on the same branch as this folder: gate `wage_shortfall.py`.

## Cross-thread map

- **P1** (`../pinning/`): the cost system, the direction of the risk, the threshold. Untouched; see "For her, first".
- **three-taxes** (`../three-taxes/`): absorbed; the block ledger T1–T12, the design memo and their checks stay there.
- **PLAN** (`../progress_and_prosperity/PLAN.md`): P2's entry rewritten on 2026-11-10 (before assembly 1; its sentence
  about the nineteen points says they shrink, which they did, to nothing).
- **λ thread and paths** (`../progress_and_prosperity/lambda/`, `../paths/code/chains.py`): the input-output engine and
  the depreciation ratios B1 runs on.
- **Branches not merged into this one:** `us-record` (`claude/focused-bardeen-aciw2z`), `consumption`
  (`claude/nice-johnson-v2zp7f`), `landtax` (`claude/friendly-ritchie-2ewxw8`), the Lucas-style rewrite of P1
  (`claude/elegant-bardeen-7q0oxs`). The root `README.md` is edited on each, so expect one small conflict there.
- **participation** (`../participation/`): B8's test.

## Log

1. **2026-11-10 — founded.** From her question on the rewrite and the backward model. The session read the rewrite in
   full, the `us-record` thread through its Log 27, three-taxes, the plan, and the `consumption` thread's state; put
   the Great Stagnation reading against the record; and ended on her statement of the paper and her four calls.
   Written: `SKETCH.md` v0, three scripts, two batteries; `PLAN.md`'s P2 entry; the root README's rows; three-taxes'
   header.
2. **2026-11-10 — assemblies 1 and 2, sketch v1, a first draft** (her "keep going"). BEA's files fetched (see above).
   `code/one_basis.py` runs the λ thread's engine on the consumption bundle and three investment bundles and closes the
   replacement of wear with three linear equations; the first run showed the two accounts meeting, and the sketch was
   rewritten around that. `code/exposure.py` reads BEA's distribution of personal income by decile, already in the
   repository as the financing account's input. Both gated. Then the draft (`paper/`), in the register she asked for.
   Not done, deliberately: nothing in `../pinning/` or in three-taxes' contents changed; no citation verified; no
   baskets by decile or tenure.
3. **2026-11-10 — the draft made checkable, read through and corrected** (the same "keep going"). `paper/build.py`
   renders the Markdown to HTML and PDF. `checks/check_draft.py` rebuilds every sentence and table row that prints a
   number from the tables; writing it and reading the render turned up the four corrections in finding 10. The wage
   accounting was re-run on a copy of the backward model's panel and the land-tax figures read against the
   `consumption` branch's notes; both match and both stay marked as not held here. Crossref was reachable, so the
   journal articles' details were checked and two citations added. The figures were relabelled in the draft's words.
   Footnotes were folded into the text. Coverage is quoted from the rewrite. Not done: baskets by tenure; the claims
   attributed to sources; anything in `../pinning/`.
4. **2026-11-10 — the draft revised to stand alone, and a little graver** (her two notes on the first draft, quoted
   under the register above). Rewritten: the abstract, the introduction, Sections 3.3 and 3.4, Section 6 (now with the
   model economy described), 8.3, 9 and the conclusion; Appendices A and B are new; the earlier reading of the nineteen
   points and every reliance on the other paper are gone. American spelling throughout, figures relabelled.
   `checks/check_draft.py` rewritten to match (127 green, 131 with the panel) and extended to Appendix A. The reference
   details were completed from RePEc and Open Library, and nine attributions read against abstracts. Not done: baskets
   by tenure; the attributions that need the books; anything in `../pinning/`.
5. **2026-11-10 — a program for the United States** (her call 6). `code/program.py` and `checks/check_program.py`
   (15 green) size it from tables already held; the draft gains Section 9 with a table and a figure, and the abstract,
   the introduction, Section 8.5, the conclusion and Appendix B follow; the old Sections 9 and 10 are now 10 and 11.
   `checks/check_draft.py` holds the new sentences (158 green, 162 with the panel). Before that, the same day: the
   words "nineteen points" taken out of the introduction, Section 3.3 and Figure 1, after her question. Not done:
   baskets by tenure; a tax on consumption computed in the model; anything in `../pinning/`.
6. **2026-11-10 — Section 9 in tables and pictures, what the United States does now, and a section on fairness** (her
   calls 7 and 8). `code/nipa_fiscal.py` takes taxes and benefits by kind from the BEA file into `data/nipa_fiscal.csv`.
   Section 9 now opens on Table 4 (now, and under the program) and carries four figures; six sentences of consequence
   were woven into Sections 4.2, 5, 6.3, 7.4, 8.2 and 8.3. Section 10, new, separates efficiency from fairness
   (Table 5), sets out the standard of contribution, and shows where it leads when work becomes scarce (Figure 11).
   The old Sections 10 and 11 are now 11 and 12. Checks: program 18, draft 173 (177 with the panel). Not done:
   baskets by tenure; a tax on consumption computed in the model; her acceptance of Section 10.
