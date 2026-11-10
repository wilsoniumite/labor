# P2 — What pays for consumption — paper sketch (v1)

**Working title candidates** (hers to pick; none is settled):
"What Pays for Consumption" · "Claims on a Living: Financing Consumption from Labor, Capital, and Land" ·
"Matching Claims to Consumption".
**Authors:** Stella Wilson; Johan Båge probably; Luna possibly (her words, 2026-11-10).

**Status:** v1, 2026-11-10, after the first two assemblies. Gated: `checks/check_one_basis.py` (18),
`checks/check_exposure.py` (15), `checks/check_paper_path.py` (25), `checks/check_rent_base.py` (5), all green. Block
B4's accounting is computed and not gated on this branch. A first draft is in `paper/`. No citation is verified: every
reference is from memory until the verify pass (section 10).

**What changed from v0.** v0 opened on the paper's two numbers: consumption two-thirds labour-financed, the production
it buys under half labour-made. The first assembly put the two accounts on one basis and the gap is gone: labour makes
0.658 of what consumption buys and finances 0.658 of it (2023), and the two differ by a point on average over
2004–2023. The nineteen points were machines' wear, taxes on production and imports. So the paper no longer opens on a
gap in the aggregate. It opens on the agreement, and its subject is who holds which claim.

**Provenance:** the session of 2026-11-10. Her question on the rewrite and the backward model ("is it as significant
as it feels?"), then: the Great Stagnation reading put against the record; her iron deposits (two owners with spare
capacity compete the rent to zero); her loop ("fund it, at least in part, through a loop that goes via the fixed
factors and resources we actually live off of"); her statement of the paper ("A proper, sensible, prosperous economy
would fund consumption through land, capital, and labor"); her four calls (three-taxes absorbed, capital tackled, the
distortion conjecture in only if the participation test supports it, P2 renamed); and "keep going".

---

## 1. The claim

Taken together, American households are paid by labour, capital and land in the proportions in which what they buy is
made by them: labour makes about two-thirds of what consumption buys and pays for about two-thirds of it, and three
accounts built from different data agree on that to within a point or two. No household is the average one. Nine in
ten hold more of their income in labour than their purchases contain, by about a tenth of income; the lower half's
other income is mostly transfers, which are funded two-thirds from taxes on labour; those who rent are short the land
in their shelter; and the top tenth holds two-thirds of the claims on capital and land. A household's share of income
is its share of each claim weighted by what the claim is paid, so when payments move from labour to the other claims
its position is what it gains or loses. The move so far has been small and so has the cost. The companion paper (P1)
says the move could become large. This paper measures the positions, sizes what it would take to change them, and
shows that the two bases differ in kind: land and the commons can be taxed without moving a margin and are small;
capital is large and, in the companion's economy, a tax on its return is paid by wages, so its claim can be shared
only by owning it.

The conclusion is old: Paine, George and Meade all say spread the claims. What is new is the measurement and what the
companion economy says about capital.

## 2. Objects

Inherited from P1, unchanged: the cost system (every price resolves into hours and land through every round of
production, interest carried inside the total requirements); the task margin and the closure; the threshold; the path.

New, and reused throughout:

- **A claim**: a title to a kind of payment. Three kinds: labour (hours), capital (the stock, at cost), land and the
  commons (what production cannot make and has no second source of).
- **What a basket is made of**, c_k: the share of a household's spending that resolves into payments to claim k through
  the full chain, wear replaced. Taxes on production and imports are set aside.
- **What an income is made of**, i_k: the share of the household's income paid by claim k. Corporate income that is
  not paid out is counted where the dividends go. A transfer is a claim on the base that funds it.
- **A holding**, h_k: the household's share of all the income claim k pays.
- **Exposure**, i_k − c_k. It sums to zero across claims, and across households it sums to about zero for each claim.
- **The common share**, θ: the share of the claims on capital and land held equally by everyone.

From three-taxes: the resolution shares (T1) are c_k in the two-claim flow case; κ, the coverage ratio; the
grandfathering dial γ/δ (T4).

## 3. The blocks

**B1 — Three accounts, one basis.** *Built and gated (`code/one_basis.py`).* BEA's make-use tables through the λ
thread's engine, 1997–2023. The 2023 consumption dollar as BEA's production account counts it: pay 0.425, machines'
wear 0.142, net surplus 0.270, taxes on production 0.072, imports 0.091. A dollar of wear is replaced by a dollar of
the investment that rebuilds it, and that dollar pays labour 0.53 by the end of the recursion. With wear traced back:
pay 0.500, net surplus 0.305, taxes 0.078, imports 0.117; with the financing account's share of proprietors' income
counted as labour (0.38), labour 0.530 and capital and land 0.275. Of net domestic factor cost labour is 0.658 (0.621
to 0.687 across proprietors' labour at 0 to two-thirds; 0.664 with imports priced as if made at home).
- *Against the financing account.* 0.658 against 0.658 in 2023. Over 2004–2023 the difference is zero on average,
  between −0.025 and +0.020, and 0.010 in absolute value. The financing account's own bounds are [0.53, 0.80]; the
  production side pins its middle.
- *Against household incomes* (B3). With corporate income that is not paid out counted, labour is 0.666 of all
  households' income in 2023, and the difference from 0.658 is +0.011 on average over 2004–2023.
- *The nineteen points.* From BEA's 0.472 to 0.658: −0.021 this engine against the digitized figure, +0.079 wear traced
  back, +0.128 taxes and imports set aside.
- *What is left.* Of spending paid from current income, labour finances 0.736 (2023), seven points more than it makes
  on average. That is what is saved out of capital's income or never paid out.
- *The trend.* Labour's share of the net factor cost of consumption: 0.683 in 1997, 0.713 at its peak in 2001, 0.658 in
  2023.

**B2 — The identity.** *New; one page.* Exact, in shares: a household's share of income is its holding of each claim
weighted by what the claim is paid, so its share moves with labour's share of income by (its holding of labour less its
holding of the other claims). To first order, in real terms, for any constant-returns technology and any preferences:

    change in real income = g + Σ_k (i_k − c_k) × change in the payment to claim k

where g is the rate at which the full-chain cost of the household's basket falls at fixed payments. Consequences:

1. A household whose claims match its basket gets g whatever happens to wages, rents and interest. That is the
   condition Keynes's forecast needed.
2. A household living on wages alone is exposed by 0.34 at the average basket and by 0.42 to 0.47 if it rents and
   spends 30 to 40% on shelter, because labour is 0.23 of the factor cost of shelter and 0.74 of the rest.
3. A transfer carries the exposure of the base that funds it.
4. The exposures add up across households to the factor content of what net investment and the state buy, which is
   small. One household's long position is another's short.

It hedges shifts between claims, not falls in output. The formula is the dual of growth accounting joined to
sources-and-uses incidence; carrying it full-chain to households for automation and land is new as far as known.

**B3 — Who holds the claims.** *Built and gated, first cut (`code/exposure.py`).* BEA's distribution of personal
income by decile of equivalized disposable income, 2004–2023, with undistributed corporate profits and corporate income
taxes given to deciles in proportion to dividends, and transfers counted as claims on the tax base (0.68 labour in
2023).

| 2023 | Labour's share of income | Exposure | Holds of labour income | of capital and land | of transfers | Does of consumption |
|---|---|---|---|---|---|---|
| Bottom half | 0.758 | +0.100 | 0.177 | 0.083 | 0.507 | 0.350 |
| Next four tenths | 0.773 | +0.115 | 0.468 | 0.245 | 0.401 | 0.448 |
| Top tenth | 0.516 | −0.142 | 0.355 | 0.672 | 0.092 | 0.202 |
| Everyone | 0.666 | +0.008 | 1 | 1 | 1 | 1 |

- The signs hold in every year and in all nine combinations of proprietors' labour and the tax-base share (2023 ranges:
  +0.06 to +0.15, +0.09 to +0.15, −0.16 to −0.13).
- Deciles two to nine are alike: labour is 0.81 to 0.83 of market income, 0.75 to 0.78 with transfers and accrued
  corporate income. The bottom tenth takes 0.58 of its income in transfers.
- 2004–2023, exact shift-share: the top tenth's share of market income rose 4.2 points, 1.4 from payments moving
  between claims and 2.8 from holding more of each claim. The next four tenths lost 4.1 (1.0 and 3.2). The bottom
  half's share barely moved.
- *Not yet:* every decile is given the average basket, and renters and owners are not told apart. The survey machinery
  for both is on the `consumption` branch.

**B4 — What it has cost.** *The household side is B3's shift-share, gated. The wage side is computed and not gated here
(`code/wage_shortfall.py`).* From 1973 to 1995 every leg of the production wage dropped together and the fork between
durables and shelter kept its pace:

| Production wage, % a year | 1950–73 | 1973–95 | 1995–2024 |
|---|---|---|---|
| over durables | 3.4 | 0.3 | 3.4 |
| over everything but shelter | 2.2 | −0.6 | 1.1 |
| over shelter | 1.5 | −1.7 | 0.2 |
| durables less shelter | 1.8 | 2.0 | 3.2 |

By 2024 the wage over everything but shelter is short of its 1950–73 pace by a factor of 2.6. In logs: slower output
per hour 42%, average pay pulling away from production pay 30%, the nonfarm labour share 16%, left over 13%; counting
shelter's price adds 8%. About a quarter is payments moving between claims. On both sides the larger part is inside
labour, or is output not growing, and no claim on capital or land would have hedged either.

**B5 — Land and the commons.** *Built; absorbs three-taxes T3, T4, T5, T8, T11 and the `consumption` branch's LVT
units.*
- *Size* (`code/rent_base.py`): site rent is 4.3–7.1% of disposable income in 2024 (3.5–5.8% in 1975), 2,776–4,627
  dollars a person a year; full capture covers 0.30 [0.15–0.59] of a poverty-line bundle (κ, 2025). The measure holds
  land's share of housing fixed and leaves out mineral and commercial rents.
- *Why it is small* (her iron deposits): rent is paid for having no second source. Most of what we live off has one.
  Abundance is why the base is small, so "resources to spare" and "fund it from land" pull against each other.
- *What it hedges:* shelter. A dividend from land rent rises when rent does, and for a household that occupies the
  average site the two cancel.
- *The ceiling* (T3): 100% of market rent, by definition; above it the tax falls on what the occupant adds.
- *The cost of getting there* (T4, T11; the LVT units): the stock and the flow are one object at two dates. At the rate
  that funds the post's 249-dollar monthly dividend, land prices fall 85% at announcement and 16.8 million mortgaged
  owners cross 80% loan-to-value; 99% of payers own their home and owners over 65 make 45% of net payments; demand at
  impact is about neutral. Increment-only grandfathering caps the stock loss at γ/δ, 40%.
- *The loop* (T5): real and second-order. The dividend's own rent demand returns about 1.1% of it as land rent.
- *The commons* (T8): congestion, spectrum, water, slots, the carbon sink. The same instrument; not core-budget scale.

**B6 — Capital.** *New, with three-taxes T10 and the old P2's pension material; gated in `code/paper_path.py` and
`code/exposure.py`.*
- *Size.* Net surplus is 0.305 of the consumption dollar against land's few points. In the companion's calibration
  interest is 31% of income, 53% at t = 1 and 65% in the limit, against rent's 9%, 30% and 35%.
- *Three ways to move a share to the public, and who pays.* Owners require the return ρ after tax (P1's Assumption
  A4), so in the long run:

  | Route | The public gets | Paid by | The economy |
  |---|---|---|---|
  | Tax the return at 20% | 6.3% of income | Wages today (−6.1 points of income; the real wage 10% lower). Land later (−5.9 at t = 1, wages untouched) | Capital 19% lower, real income 6.5% lower |
  | Tax the cash flow at 20%, investment expensed | 6.2% of income | Today's owners, once: a fifth of the existing stock | Unchanged |
  | Buy a fifth of the stock | 6.2% of income | Whoever saves for it: 1.0 year of the whole wage bill today | Unchanged |

  Given every cent of the first route's revenue, a wage earner is 0.3% ahead. So the claim on capital can be shared
  only by owning it. A cash-flow tax is ownership by another name: the state pays its share of every machine and takes
  its share of every rental, and at introduction it takes its share of the machines already standing. This sharpens
  three-taxes' "interest is not a base": there the supply response was outside the model; here it is inside, and
  wages pay.
- *The window.* The claims on interest and rent together cost 6.7 years of the whole wage bill today, 9.1 at t = 0.5,
  19 at the threshold and 48 at t = 1. A buy-in financed from wages works only while labour's share is high.
- *What a common share does.* At today's holdings, if labour were paid 0.17 of market income (the companion's t = 1)
  the top tenth's share would go from 0.462 to 0.618, the next four tenths' from 0.393 to 0.283 and the bottom half's
  from 0.145 to 0.099. A common share of 0.13 of the claims on capital and land holds the bottom half where it is; 0.15
  holds it with labour paid nothing; a common fifth raises it to 0.17. Nothing short of 0.86 holds the next four
  tenths: they hold 0.47 of labour income, and it is they who lose most.
- *The floor.* A poverty-line bundle for every person costs 9–18% of GDP in 2024, down from 18–35% in 1975 and 27–52%
  in 1955 (GDP is gross; against net income the floor is about a fifth larger).
- *Instruments, by who pays.* Mandated saving out of wages (funded pensions) turns a labour claim into a capital claim
  over a working life; pay-as-you-go promises stay labour claims (the old P2's pension fork). The cash-flow tax (T10)
  reaches pure profit and the standing stock and exempts the normal return on new investment. A share levy (Meidner)
  is the same levy paid in shares. A fund can also be bought with saved rent or with borrowing.
- *Open, and the paper should say so.* The model has no risk. The saving response is assumed (A4), not derived; with a
  less elastic supply owners bear part of a tax on the return. How much of "interest" is pure profit decides how much
  can be taxed like rent. An open economy shifts more.

**B7 — The path.** *Built (`code/paper_path.py`, gated on the numbers the rewrite prints).* What is paid to labour,
interest and rent goes from 60 / 31 / 9 to 17 / 53 / 30 at t = 1 and 0 / 65 / 35 at t = 2. The threshold (t = 0.77 on
the calibrated schedule) says when it starts to matter; nothing here needs the bound to hold today.

**B8 — The distortion conjecture.** *Conditional (her call: in only if the participation test supports it).* When
consumption depends on earning a wage, a lower wage need not reduce the labour offered, so the wage stops signalling
that less labour is wanted (P1's closing conjecture). The test is the participation thread's. Not in the draft.

## 4. What the paper must not claim

- **That consumption is more labour-financed than production is labour-made.** On one basis it is not. This is also a
  correction to P1 (section 11, item 1).
- That most households hold one claim. They are long labour by about a tenth of income.
- That land explains the stagnation, or that the backward fit shows history. B4 rests on the record.
- That a rent loop can carry the floor: κ is 0.30.
- That the loop creates resources (T5).
- That taxing capital's return shares it (B6).
- That the shift between claims has cost households much so far.
- That the conclusion is new.

## 5. New against already claimed

Already in P1 (`../pinning/paper/main.tex`): the two accounts (Section 9, Appendix F); the conjecture (Section 11); the
rent tax and uniform transfer (Proposition 6); conditionality, coverage, the index D and Table D.1 (Appendix D). P1's
reading of the two accounts as a gap is withdrawn here.
Already in three-taxes: T1–T12 with their checks. Already in the old P2: the provisioning identity, the pension fork,
the fund against the Meidner levy, the one-time-levy reading.
Known in the literature (from memory, to verify): sources-and-uses incidence; dual growth accounting; the cash-flow
tax as a silent partnership; long-run incidence of a capital tax under elastic supply and its qualifications; housing
as a hedge against rent risk; labour and capital income moving together in levels, so a capital claim hedges the
share and not the level; the factor content of consumption baskets by income in trade; distributional national
accounts; automation and wealth concentration; the social dividend.
New here: the production account with wear traced back, and its agreement with the financing account and with
household incomes (B1); exposure by decile against what consumption is made of, with transfers read through to their
base (B3); the three routes' incidence, the window and the common share (B6); the floor's cost series; the accounting of
the shortfall (B4).

## 6. Absorption ledger

**three-taxes** (her call, 2026-11-10; the folder stays as the record, nothing in it is edited but its header):
- *Taken:* T1 the resolution ledger (as c_k); T3 the ceiling, stated not re-derived; T4 and T11 the stock, the dial
  and the announcement shock; T5 the loop; T7 convergence, as B7's limit; T8 the commons; T10 the source tier, as the
  second capital route.
- *Left as record:* T2 the three-tier frame; T6 the gate tax's design and rate; T9; T10b and T10c; T12 the valuation
  mechanism; the removal order and allocation rule; everything in its dropped list. Its sentence that the
  financing-versus-production gap is evidence for the reinvestment closure does not survive B1.
- It was sequenced after "the dynamics paper", which the `us-record` branch parks. If that stands, what three-taxes
  deferred there has no home until she assigns one.

**The old P2** ("the transition"): the provisioning identity is B2 and B3; pensions and the fund against the share levy
are B6; conditionality, the enclosure race and trigger design stay in P1's appendix and the plan until wanted.
**P1:** Appendices D and F and the conjecture are this paper's opening. They are not moved out of `main.tex` here.
**`consumption` branch** (`claude/nice-johnson-v2zp7f`): the LVT-dividend units feed B5; its decile and tenure
machinery is what B3 needs next.
**`landtax` branch** (`claude/friendly-ritchie-2ewxw8`): the land-tax timeline, for B5's history; not read yet.
**`us-record` branch** (`claude/focused-bardeen-aciw2z`): its panel feeds B4. The fit itself is not used.

## 7. Paper plan

1. Introduction. 2. Claims, baskets and the identity (B2). 3. Three accounts, one basis (B1). 4. Who holds the claims
(B3). 5. What the shift has cost so far (B4). 6. If the shift continues (B7 with B3's holdings). 7. Land and the
commons (B5). 8. Capital (B6). 9. What the paper leaves out and what would count against it.

## 8. Assemblies, in order

1. ~~One basis for the two accounts~~ Done (B1).
2. ~~Exposure by decile~~ First cut done (B3). **Next: baskets by decile and tenure**, from the consumer expenditure
   survey on the `consumption` branch, so renters and owners are told apart.
3. **The shortfall, gated** (B4): when the backward model's panel is on the same branch.
4. **Capital in the record** (B6): net surplus split into the normal return and the rest; funded pensions counted as
   claims; pension systems as cases (her list: Sweden and Norway; Australia's contribution system belongs beside them).
5. **Land, a second country** (B5): Finland is built on the `consumption` branch.
6. **The long run of B1**: the production account before 1997 on one basis, to see whether 2001 is a peak or a point
   on a longer fall.

## 9. Objections to meet

(i) "Households can buy shares." Most hold few, and wages are what they would buy them with: the window.
(ii) "A capital claim does not hedge a recession." Agreed: B2 says shifts, not levels.
(iii) "Your owners never bear the tax because you assumed they would not." A4 is the long run; the short run and a
less elastic supply go the other way, and B6 says so.
(iv) "Corporate income is not the households'." It is their claim; leaving it out makes every decile look more
dependent on labour, and the check shows both.
(v) "A dividend lowers work." That is the Keynes margin and P1's participation block; an outcome, not a hidden cost.
(vi) "The land tax's shock is the whole problem." B5 sizes it; the dial is the answer on offer.
(vii) "A tenth of income is not much." It is the position today. Section 6 is what it becomes on the companion's path.

## 10. Verify ledger (nothing enters the paper from memory)

Musgrave on sources and uses; the dual approach to growth accounting; Brown 1948 and Meade 1978 on the cash-flow tax;
Auerbach and Kotlikoff 1987 on the levy; Chamley 1986 and Judd 1985, with Straub and Werning's qualification; Sinai
and Souleles on owning as a hedge against rent; Baxter and Jermann on labour and capital income; Borusyak and Jaravel
on the factor content of baskets; Piketty, Saez and Zucman on distributional national accounts; Moll, Rachel and
Restrepo on automation and wealth; Freeman on who owns the robots; Meade's social dividend; Paine 1797; Keynes 1930;
Samuels and Senel 2026 (verified in P1); Barkai 2020 (verified in P1); Rognlie 2015 (verified in P1); Diamond and
Geanakoplos on public funds holding equity; the Meidner plan's history; Australia's contribution rate and fund size;
plus three-taxes' own ledger for what is taken from it.

**Status, 2026-11-10.** Bibliographic details confirmed for every reference in the draft, against Crossref, RePEc or
Open Library, or taken from the reference list of *What Machines Cannot Make*; the one exception is the title of
Brown's chapter in the Hansen volume. Keynes's two forecasts (four to eight times; a fifteen-hour week) were read
against the essay's text. What the draft attributes to these was read against their abstracts: Caselli and Manning
2019, Korinek and Suh 2024, Sachs and Kotlikoff 2012, Freeman 2015, Moll, Rachel and Restrepo 2022, Piketty, Saez and
Zucman 2018, Sinai and Souleles 2005, Straub and Werning 2020 (which also states the Chamley-Judd result), and Baxter
and Jermann 1997. What it attributes to these follows *What Machines Cannot Make*: Zeira 1998, Acemoglu and Restrepo
2018, Korinek and Stiglitz 2019, Cummins and Violante 2002, Rognlie 2015, Barkai 2020, Hall and Jorgenson 1967,
Orshansky 1963. Still from memory: Brown 1948, Meade 1964 and 1978, Auerbach and Kotlikoff 1987, Musgrave 1959, Paine
1797, George 1879. Listed above and not used in the draft: the dual approach to growth accounting, Borusyak and
Jaravel, Diamond and Geanakoplos, the Meidner plan, Australia's funds.

## 11. Decisions for her

1. **P1's Section 9.** It reads the two accounts as a nineteen-point gap between financing and production. On one basis
   there is none. The paragraph, Figure 7's caption and Appendix F's last sentence need restating before the Economic
   Modelling package goes, and Johan should see why.
2. Title.
3. ~~Whether the paper recommends a capital route or only prices the three.~~ **Decided 2026-11-10: it recommends.** Her
   words: "lets put the mix into the paper, puts some action behind it". The draft's Section 9 is a program: a holding
   in common of about a fifth (the corporate income tax on a cash-flow base, a tax on the growth of land rent, charges
   on the commons), paid as an equal dividend; funded saving out of wages for the households above the median; taxes
   moved from wages to consumption; no further tax on the return to capital and no full universal income.
   `code/program.py` sizes it and `checks/check_program.py` holds the sizes.
4. ~~Scope.~~ **Decided 2026-11-10: the United States** (her "USA").
5. The yardstick in B4: 1950–73 is a choice, and the shares move with it.
6. When Appendices D and F leave P1.
7. Whether three-taxes moves under this folder or stays where it is; and this folder's name.

---

All prose here is draft register, hers to re-voice. Checks: `checks/check_one_basis.py` (18; needs the BEA files, see
its header), `checks/check_exposure.py` (16), `checks/check_paper_path.py` (25), `checks/check_rent_base.py` (5),
`checks/check_program.py` (15), `checks/check_draft.py` (158).
