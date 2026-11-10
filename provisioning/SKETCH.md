# P2 — What pays for consumption — paper sketch (v0)

**Working title candidates** (hers to pick; none is settled):
"What Pays for Consumption" · "Claims on a Living: Financing Consumption from Labor, Capital, and Land" ·
"Matching Claims to Consumption".

**Status:** v0 sketch, 2026-11-10. Model numbers gated: `checks/check_paper_path.py` ALL GREEN (25),
`checks/check_rent_base.py` ALL GREEN (5). Section 4's accounting is computed and not gated on this branch (its inputs
are the backward model's, on another branch). No paper prose, no citation verified: every reference below is from
memory until the verify pass (section 10).

**Provenance:** the session of 2026-11-10. Her question on the rewrite and the backward model ("is it as significant
as it feels?"), then: the Great Stagnation reading put against the record (every leg of the wage fell together;
shelter's price is 8% of the shortfall); her iron deposits (two owners with spare capacity compete the rent to zero);
her loop ("fund it, at least in part, through a loop that goes via the fixed factors and resources we actually live
off of"); her statement of the paper ("A proper, sensible, prosperous economy would fund consumption through land,
capital, and labor"); and her four calls: three-taxes absorbed, capital tackled, the distortion conjecture in only if
the participation test supports it, P2 renamed.

---

## 1. The claim

A household's real income moves with factor payments by the gap between what its income is made of and what its
purchases are made of. United States consumption is about two-thirds labour-financed (65.8% in 2023), the production
it buys is under half labour-made (47.2%), and the fiscal system leans the same way: 68% of tax revenue is raised from
labour-income bases and at least 84% of benefits are conditioned on work or means. So most households, and the safety
net under them, hold one claim. The paper measures that mismatch by household, shows what it has cost, and sizes the
three ways to close it: land and the commons, which can be taxed without moving a margin and are small; capital, which
is large and can be shared only by owning it; and labour, which carries the rest. The companion paper (P1) says which
way factor payments move as machines improve. This paper says who is exposed to the move and what a matched claim
would cost, now and later.

The conclusion is old: Paine, George and Meade all say spread the claims. What is new is the measured mismatch, the
reading of the fiscal base as an exposure, and what the companion economy says about capital.

## 2. Objects

Inherited from P1, unchanged: the cost system (every price resolves into hours and land through every round of
production, interest carried inside the total requirements); the task margin and the closure; the threshold (replacing
the hardest hour embodies less than an hour); the automation path.

New, and reused throughout:

- **The factor content of a basket**, c_k: the share of a household's spending that resolves into payments to claim k
  (wages, rent, interest) through the full chain. P1's total requirements, weighted by the basket.
- **The factor make-up of an income**, i_k: the share of the household's income paid by claim k. A transfer counts as
  a claim on the base that funds it.
- **Exposure**, e_k = i_k − c_k. They sum to zero across claims.
- **The common share**, θ: the share of the claims on rent and interest held equally by everyone.

From three-taxes: the resolution shares φ_w and φ_r (T1) are c_k in the two-claim flow case; κ, the coverage ratio;
the grandfathering dial γ/δ (T4); the index D = φ_C (1 − κ)² (P1's Appendix D).

## 3. The blocks

**B1 — Two accounts.** *Built (P1, Appendix F and Table D.1).* The financing account: labour-origin resources finance
69.6% [59.8–83.1] of consumption in 2004 and 65.8% [52.7–80.1] in 2023. The production account: human effort is 50.1%
of consumed production in 1997 and 47.2% in 2023. Taxes: 0.68 from labour-income bases in 2025. Benefits: at least 0.84
conditioned on work or means. The four-way split of financing in 2025, leaving out what owners consume from their own
returns (medians, which need not add to one): wages directly 0.73, taxes on wages 0.16, taxes on owners 0.06,
borrowing 0.05.
*To add first:* the two accounts are not on one basis. The production account leaves capital services as a primary
input, depreciation included; the financing account is in incomes net of depreciation. On the cost system's own
definition, replacement is traced back into the wages, rent and interest that rebuild the machines, labour's content
is higher, and the 19-point gap shrinks. A rough size, not a computation: replacement is about 16 points of output and
the labour content of machinery is 0.55 (the λ series), so labour's content rises by about 9 points and the gap falls
to about 10. This is the paper's central number and it has to be rebuilt on one basis before anything rests on it.

**B2 — The exposure identity.** *New; one page.* To first order, for any constant-returns technology and any
preferences,

    change in real income = g + Σ_k (i_k − c_k) × change in the payment to claim k

where g is the rate at which the full-chain cost of the household's basket falls at fixed factor payments. The price
side is Shephard's lemma on the basket and on each good's unit cost with P1's total requirements; substitution is
second-order. Four consequences:

1. A household whose claims match its basket (i = c) gets g whatever happens to wages, rents and interest. That is
   the condition Keynes's forecast needed.
2. A wage-only household carries −c_k on every other claim: 0.53 in all on the production account as built (about
   0.44 on the rough single basis of B1).
3. A transfer carries the exposure of the base that funds it. With 68% of revenue on labour bases, the safety net is
   written on the same risk as the wage: pooling works for one worker's bad year and fails when labour's share falls.
4. In a closed economy the exposures add up, income-weighted, to the factor content of what investment and the state
   buy. One household's long position is another's short.

What it does not do: it hedges shifts between claims, not falls in output. The formula is the dual of growth
accounting joined to sources-and-uses incidence. Applying it full-chain, by household, to automation and land is new
as far as known.

**B3 — Who is exposed.** *To build.* Exposure by income decile and by tenure. Expected, not yet computed: the middle of
the distribution is far more labour-financed than the aggregate; renters are short land (their basket holds it, their
income does not), owner-occupiers are matched on shelter; funded pensions are capital claims and pay-as-you-go
pensions are labour claims. The financing account is computed decile by decile and published only in aggregate
(`../pinning/effort/`); land and financial assets by income decile are on the `consumption` branch (the top income
decile holds 39% of United States residential land and 66% of financial assets).

**B4 — What it cost.** *Computed 2026-11-10; not gated here (`code/wage_shortfall.py`).* From 1973 to 1995 every leg of
the production wage dropped together, and the fork between durables and shelter kept its pace:

| Production wage, % a year | 1950–73 | 1973–95 | 1995–2024 |
|---|---|---|---|
| over durables | 3.4 | 0.3 | 3.4 |
| over everything but shelter | 2.2 | −0.6 | 1.1 |
| over shelter | 1.5 | −1.7 | 0.2 |
| durables less shelter | 1.8 | 2.0 | 3.2 |

By 2024 the wage over everything but shelter is short of its 1950–73 pace by a factor of 2.6. In logs: slower output
per hour 42%, average pay pulling away from production pay 30%, the nonfarm labour share 16%, left over 13%; counting
shelter's price adds 8%. So about a quarter is payments moving between claims, the part a matched household would not
have felt. The 42% no claim hedges. The 30% is inside labour, and a flat dividend only dilutes it. The paper claims
that quarter and no more.

**B5 — Land and the commons.** *Built; absorbs three-taxes T3, T4, T5, T8, T11 and the `consumption` branch's LVT
units.*
- *Size* (`code/rent_base.py`): site rent is 4.3–7.1% of disposable income in 2024 (3.5–5.8% in 1975), 2,776–4,627
  dollars a person a year; full capture covers 0.30 [0.15–0.59] of a poverty-line bundle (κ, 2025). The measure holds
  land's share of housing fixed and leaves out mineral and commercial rents.
- *Why it is small* (her iron deposits): rent is paid for having no second source. Most of what we live off has one.
  So "resources to spare" and "fund it from land" pull against each other: abundance is why the base is small.
- *The ceiling* (T3): 100% of market rent, by definition; above it the tax falls on what the occupant adds.
- *The cost of getting there* (T4, T11; the LVT units): the stock and the flow are one object at two dates. At the
  rate that funds the post's 249-dollar monthly dividend, land prices fall 85% at announcement and 16.8 million
  mortgaged owners cross 80% loan-to-value; 99% of payers own their home and owners over 65 make 45% of net payments;
  demand at impact is about neutral. Increment-only grandfathering caps the stock loss at γ/δ, 40%.
- *The loop* (T5): real and second-order. The dividend's own rent demand returns about 1.1% of it as land rent.
- *The commons* (T8): congestion, spectrum, water, slots, the carbon sink. The same instrument; not core-budget scale.

**B6 — Capital.** *New, with three-taxes T10 and the old P2's pension material.*
- *Size.* Interest is 31% of income in the companion's calibration, 53% at t = 1 and 65% in the limit, against rent's
  9%, 30% and 35%. That figure includes pure profits, which the economy does not separate from interest.
- *Three ways to move a share to the public, and who pays* (`code/paper_path.py`, E3–E5, F1). Owners require the
  return ρ after tax (P1's Assumption A4), so in the long run:

  | Route | The public gets | Paid by | The economy |
  |---|---|---|---|
  | Tax the return at 20% | 6.3% of income | Wages today (−6.1 points of income; the real wage 10% lower). Land later (−5.9 at t = 1, wages untouched) | Capital 19% lower, real income 6.5% lower |
  | Tax the cash flow at 20%, investment expensed | 6.2% of income | Today's owners, once: a fifth of the existing stock | Unchanged |
  | Buy a fifth of the stock | 6.2% of income | Whoever saves for it: 1.0 year of the whole wage bill today | Unchanged |

  Given every cent of the first route's revenue, a wage earner is 0.3% ahead. So the claim on capital can be shared
  only by owning it. A cash-flow tax is ownership by another name: the state pays its share of every machine and takes
  its share of every rental (F1), and at introduction it takes its share of the machines already standing. This
  sharpens three-taxes' "interest is not a base": there the supply response was outside the model; in the rewrite's
  economy it is inside, and wages pay.
- *The window* (E2). The claims on interest and rent together cost 6.7 years of the whole wage bill today, 9.1 at
  t = 0.5, 19 at the threshold and 48 at t = 1. A buy-in financed from wages works only while labour's share is high.
- *What a common share does* (E6). A common share θ of both claims pays everyone θ times the non-labour share of mean
  income: with θ = 0.2, 8% today, 17% at t = 1, 20% in the limit. A poverty-line bundle for every person costs 9–18%
  of GDP in 2024, down from 18–35% in 1975 and 27–52% in 1955 (`code/rent_base.py`; GDP is gross, and against net
  income the floor is about a fifth larger).
- *Instruments, by who pays.* Mandated saving out of wages (funded pensions) turns a labour claim into a capital claim
  over a working life; pay-as-you-go promises stay labour claims (the old P2's pension fork: keep the promises,
  migrate the base, the double payment). The cash-flow tax (T10) reaches pure profit and the standing stock and
  exempts the normal return on new investment. A share levy (Meidner) is the same levy paid in shares. A fund can
  also be bought with saved rent or with borrowing.
- *Open, and the paper should say so.* The model has no risk, so it cannot price what a fund's holders bear. The
  saving response is assumed (A4), not derived; with a less elastic supply owners bear part of a tax on the return.
  How much of "interest" is pure profit decides how much can be taxed like rent. An open economy shifts more.

**B7 — The path.** *Built (`code/paper_path.py`, gated on the numbers the rewrite prints).* The matching mix
(labour / interest / rent) goes from 60 / 31 / 9 to 17 / 53 / 30 at t = 1 and 0 / 65 / 35 at t = 2. The threshold
(t = 0.77 on the calibrated schedule) says when it starts to matter; nothing here needs the bound to hold today.

**B8 — The distortion conjecture.** *Conditional (her call: in only if the participation test supports it).* When
consumption depends on earning a wage, a lower wage need not reduce the labour offered, so the wage stops signalling
that less labour is wanted (P1's closing conjecture). The test is the participation thread's. If it does not support
the conjecture, the section is cut and the paper loses nothing it rests on.

## 4. What the paper must not claim

- That land explains the stagnation, or that the backward fit shows history. B4 rests on the record.
- That a rent loop can carry the floor: κ is 0.30.
- That the loop creates resources (T5).
- That taxing capital's return shares it (B6).
- That the conclusion is new.
- More than a quarter of the wage's shortfall.

## 5. New against already claimed

Already in P1 (`../pinning/paper/main.tex`): the two accounts and the gap (Section 9, Appendix F); the conjecture
(Section 11); the rent tax and uniform transfer (Proposition 6); conditionality, coverage, the index D and Table D.1
(Appendix D). The rewrite she sent drops the accounts and the conjecture.
Already in three-taxes: T1–T12 with their checks. Already in the old P2: the provisioning identity, the pension fork,
the fund against the Meidner levy, the one-time-levy reading.
Known in the literature (from memory, to verify): sources-and-uses incidence; dual growth accounting; the cash-flow
tax as a silent partnership; long-run incidence of a capital tax under elastic supply and its qualifications; housing
as a hedge against rent risk; labour and capital income moving together in levels, so a capital claim hedges the
share and not the level; the factor content of consumption baskets by income in trade; automation and wealth
concentration; the social dividend.
New here: the exposure accounting carried full-chain to households for automation and land (B2, B3); the fiscal base
read as an exposure; the three routes' incidence, the window and the common share in the companion economy (B6); the
floor's cost series (B5, B6); the accounting of the shortfall (B4).

## 6. Absorption ledger

**three-taxes** (her call, 2026-11-10; the folder stays as the record, nothing in it is edited but its header):
- *Taken:* T1 the resolution ledger (as c_k); T3 the ceiling, stated not re-derived; T4 and T11 the stock, the dial
  and the announcement shock; T5 the loop; T7 convergence, as B7's limit; T8 the commons; T10 the source tier, as the
  second capital route.
- *Left as record:* T2 the three-tier frame; T6 the gate tax's design and rate; T9; T10b and T10c (the wage-share
  clock and the use-split rule); T12 the valuation mechanism; the removal order and allocation rule; everything in its
  dropped list. They come back only if the paper turns to design.
- It was sequenced after "the dynamics paper", which the `us-record` branch parks (its move of `dynamics/` to an
  archive, 2026-11-05). If that stands, what three-taxes deferred there (the announcement-date theorem, the price
  paths, the shock experiments) has no home until she assigns one.

**The old P2** ("the transition"): the provisioning identity is B2 and B3; pensions and the fund against the share levy
are B6; conditionality, the enclosure race and trigger design stay in P1's appendix and the plan until wanted.
**P1:** Appendices D and F and the conjecture are this paper's opening. They are not moved out of `main.tex` here: the
Economic Modelling package is built and waits on Johan's sign-off.
**`consumption` branch** (`claude/nice-johnson-v2zp7f`): the LVT-dividend units feed B5; its decile machinery feeds B3.
**`landtax` branch** (`claude/friendly-ritchie-2ewxw8`): the land-tax timeline, for B5's history; not read for this sketch.
**`us-record` branch** (`claude/focused-bardeen-aciw2z`): its panel feeds B4. The fit itself is not used.

## 7. Paper plan

1. Introduction: the question, the two numbers, the answer in a paragraph.
2. Two accounts, on one basis (B1).
3. Exposure (B2).
4. Who is exposed (B3).
5. What it cost, 1973–2024 (B4).
6. Land and the commons (B5).
7. Capital (B6).
8. The path (B7).
9. What would count against the account; what the paper leaves out. (B8 before this if it survives.)

## 8. Assemblies, in order

1. **One basis for the two accounts** (B1): the production account with replacement traced into the claims that
   rebuild the machines. Inputs: the λ thread's input–output machinery and BEA's fixed-asset depreciation by industry.
2. **Exposure by decile and tenure** (B3): incomes from the financing account's decile profiles; baskets from the
   consumer expenditure survey; content by product from the input–output chain; land's share of shelter as a band.
3. **The shortfall, gated** (B4): when the backward model's panel is on the same branch, `wage_shortfall.py` gets its
   check; until then its numbers carry the label "not gated".
4. **Capital in the record** (B6): net capital income split into the normal return and the rest; who holds it by
   decile, funded pensions counted as claims; pension systems as cases (her list: Sweden and Norway; Australia's
   contribution system belongs beside them).
5. **Land, a second country** (B5): Finland is built on the `consumption` branch.

## 9. Objections to meet

(i) "Households can buy shares." Most hold none, and wages are the only thing most could buy them with: the window.
(ii) "A capital claim does not hedge a recession." Agreed: B2 says shifts, not levels.
(iii) "Your owners never bear the tax because you assumed they would not." A4 is the long run; the short run and a
less elastic supply go the other way, and B6 says so.
(iv) "The gap is depreciation." Assembly 1.
(v) "A dividend lowers work." That is the Keynes margin and P1's participation block; it is an outcome, not a cost
the paper hides.
(vi) "The land tax's shock is the whole problem." B5 sizes it; the dial is the answer on offer.

## 10. Verify ledger (nothing enters a draft from memory)

Musgrave on sources and uses; the dual approach to growth accounting; Brown 1948 and Meade 1978 on the cash-flow tax;
Auerbach and Kotlikoff 1987 on the levy; Chamley 1986 and Judd 1985, with Straub and Werning's qualification; Sinai
and Souleles on owning as a hedge against rent; Baxter and Jermann on labour and capital income; Borusyak and Jaravel
on the factor content of baskets; Moll, Rachel and Restrepo on automation and wealth; Freeman on who owns the robots;
Meade's social dividend; Paine 1797; Barkai 2020 (verified in P1); Rognlie 2015 (verified in P1); Diamond and
Geanakoplos on public funds holding equity; the Meidner plan's history; Australia's contribution rate and fund size;
plus three-taxes' own ledger for what is taken from it.

## 11. Decisions for her

1. Title.
2. Whether the paper recommends a capital route or only prices the three. The sketch prices them and rules out one.
3. Scope: the United States alone, or with Finland (land is built) and a pension-system comparison.
4. The yardstick in B4: 1950–73 is a choice, and the shares move with it.
5. When Appendices D and F leave P1, and whether Johan is on this paper.
6. Whether three-taxes moves under this folder or stays where it is.
7. The folder's name (`provisioning`, after the old P2's identity) is Claude's placeholder.

---

All prose here is draft register, hers to re-voice. Checks: `checks/check_paper_path.py` (25) and
`checks/check_rent_base.py` (5), numpy and pandas only.
