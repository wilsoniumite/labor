# STATE — provisioning (P2; resume point for the next session)

**Project:** P2, renamed and re-centred on 2026-11-10: *What pays for consumption* (working title). How consumption is
financed against what it is made of; who is exposed to payments moving between labour, capital and land; and what a
matched claim would cost. The governing document is `SKETCH.md`; read it first. The companion is P1 (`../pinning/`),
which says which way factor payments move.
**Collaboration:** same contract as the sibling threads: working format, sequencing and drafting delegated to Claude;
checks gate absolutely; direct critique over validation; her voice pass re-voices any prose that enters a paper. Code
in plain functions, notebook-cell style.
**The wall:** this repository is public. Public data only.
**State as of:** 2026-11-10 (founding session). Sketch v0 written; three scripts and two batteries; nothing drafted.

## Her calls, 2026-11-10

1. **P2 is this paper** ("P2 renamed, I think"). `../progress_and_prosperity/PLAN.md` carries the new entry.
2. **three-taxes is absorbed** ("Three taxes probably won't get revived by me so you can absorb it if you want").
   `SKETCH.md` section 6 lists what is taken and what stays behind as record.
3. **Capital is in** ("Yes, I realise now we need to tackle capital"). It is block B6 and the paper's largest new part.
4. **The distortion conjecture is conditional** ("Sure on distortion"): a section only if the participation test
   supports it.

## Claude's calls, in her veto window

- **The folder is `provisioning/`**, after the old P2's provisioning identity. A placeholder; rename freely.
- **three-taxes stays where it is.** Only its `STATE.md` header changed. Moving the folder would break its checks'
  paths for no gain today.
- **The spine is positive, with one benchmark** (a household matched to its basket). Instruments appear only where
  they size a loop or say who pays. She did not rule on this; three-taxes' design blocks are held back on that reading.
- **P1 is not touched.** Its Appendices D and F and its closing conjecture are this paper's opening, but
  `../pinning/paper/main.tex` is at the journal-package stage and waits on Johan's sign-off.
- **The companion economy is the rewrite's** (*What Machines Cannot Make*, October 2026, the PDF she uploaded; its
  source is not in this repository). `code/paper_path.py` re-derives it from the printed equations and parameters.

## What exists

| File | What it is | Gate |
|---|---|---|
| `SKETCH.md` | The paper sketch, v0: claim, objects, blocks B1–B8, what not to claim, absorption ledger, plan, assemblies, decisions | — |
| `code/paper_path.py` | The rewrite's calibrated economy, re-derived; who is paid along the path, what the claims cost, who bears a tax on interest | `checks/check_paper_path.py`, 25 green: the rewrite's Appendix C baseline, Table 2, Sections 8.3, 8.5 and 8.7, the accounts, and every number B6 and B7 quote |
| `code/rent_base.py` | The site-rent base a person against income, a poverty-line bundle and GDP, 1947–2024 | `checks/check_rent_base.py`, 5 green: equal to the paper's four rent-bill coverage members in all 72 common years (1e-16), and the quoted readings |
| `code/wage_shortfall.py` | Where the production wage fell short of its 1950–73 pace | **Not gated here.** It reads the backward model's panel, which is on `claude/focused-bardeen-aciw2z` (at 457e38b). Run against that file it prints B4's numbers |

Run from this folder: `python3 checks/check_paper_path.py`, `python3 checks/check_rent_base.py` (numpy and pandas).

## What the founding session found

1. **The companion economy reproduces.** Every number tried from the rewrite's Section 8 comes out of an independent
   re-derivation, cheaper finance (8.7) included, which is the lever the capital block uses.
2. **A tax on the return to capital is paid by wages** (B6). At 20%, long run, today's technology: revenue 6.3% of
   income, wages −6.1, owners' interest −5.9, rents −0.8, real income −6.5%. At t = 1 the same tax falls on land.
   A cash-flow tax or a purchase moves the same share with nothing else changed.
3. **The window** (B6): the claims on interest and rent cost 6.7 years of the wage bill today and 48 at t = 1.
4. **The floor is cheaper than it was** (B5, B6): 9–18% of GDP in 2024, 18–35% in 1975, 27–52% in 1955.
5. **The two accounts are not on one basis** (B1). On a rough count the 19-point gap halves once replacement is traced
   back into the claims that rebuild machines. Assembly 1 settles it, and it comes first.
6. **The stagnation is mostly not a land story** (B4): shelter's price is 8% of the shortfall and labour's share 16%;
   slower output per hour is 42% and dispersion inside labour 30%.

Also from the session, belonging to other threads and not landed here: a no-change benchmark for the backward model's
out-of-sample splits (the main case 5.2 against 4.6 from 1995, 12.7 with the utility held after 1990; 6.7 against 13.6
from 1985); in the stored main case land's share of a machine's cost is 0.33 in 1950 and 4e-8 in 2024, and labour's
lost share of income since 1970 goes to interest (5.1 of 6.4 points), not land (0.3). Those are `us-record`'s to keep
or drop.

## Next

0. **Her read of `SKETCH.md`** and its section 11 (title; whether the paper recommends a capital route; scope; B4's
   yardstick; when P1 gives up its appendices and whether Johan is on this paper; three-taxes' folder; this folder's
   name).
1. **Assembly 1: the two accounts on one basis.** Nothing else rests on a firm number until this is done.
2. **Assembly 2: exposure by decile and tenure.** The paper's first new exhibit.
3. **The verify pass** on section 10's ledger before any prose.
4. When `us-record` and `consumption` are on the same branch as this folder: gate `wage_shortfall.py`, and read the
   LVT units and the decile machinery directly.

## Cross-thread map

- **P1** (`../pinning/`): the cost system, the direction of the risk, the threshold. Untouched.
- **three-taxes** (`../three-taxes/`): absorbed; the block ledger T1–T12, the design memo and their checks stay there.
- **PLAN** (`../progress_and_prosperity/PLAN.md`): P2's entry rewritten; P5 keeps the political economy and reads
  B3's table.
- **Branches not merged into this one:** `us-record` (`claude/focused-bardeen-aciw2z`), `consumption`
  (`claude/nice-johnson-v2zp7f`), `landtax` (`claude/friendly-ritchie-2ewxw8`), the Lucas-style rewrite of P1
  (`claude/elegant-bardeen-7q0oxs`). This folder was written on a branch from `main` and names them where it leans on
  them; the root `README.md` is edited on each, so expect one small conflict there.
- **participation** (`../participation/`): B8's test.

## Log

1. **2026-11-10 — founded.** From her question on the rewrite and the backward model. The session read the rewrite in
   full, the `us-record` thread through its Log 27, three-taxes, the plan, and the `consumption` thread's state; put
   the Great Stagnation reading against the record; and ended on her statement of the paper and her four calls.
   Written: `SKETCH.md`, the three scripts, the two batteries; `PLAN.md`'s P2 entry; the root README's rows;
   three-taxes' header. Not done, deliberately: no paper prose, no citation verified, nothing in `../pinning/` or in
   three-taxes' contents changed, no data fetched.
