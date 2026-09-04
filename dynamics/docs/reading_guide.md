# Reading guide to the literature behind `pinning.html`

Built 2026-08-17. Ordered by how much of the paper falls over if the citation is
wrong. For each entry: **why we lean on it**, **exactly what to read**, and
**what to watch for**.

Provenance rule for this document: entries marked **[read in full this session]**
were read end-to-end from the PDF and the section/page pointers are verified.
Entries marked **[pointer]** carry a located section but were not read line by
line — verify as you read, and flag anything that does not match.

---

> **Notation (2026-08-27):** the paper now uses its v2 symbols — γ(x) for the
> schedule, b for the land coefficient, ρ for the interest rate; the full map
> is `docs/notation_map.md`. Other papers' symbols below remain their own.

## Tier 1 — the paper does not stand without these

### 1. Caselli & Manning (2019), "Robot Arithmetic: New Technology and Wages," *AER: Insights* 1(1): 1–12 **[read in full this session]**

**Why:** §7 Proposition 4(i) is built as a concession to this paper. It is the
single strongest standing objection to any technological-immiseration story, and
our whole fork construction exists to route around it.

**Read (ungated LSE author version, ~13 pp. of text):**
- pp. 3–5, "Benchmark Model": Assumptions CRS, RK, PC, HOM. **Read these
  assumptions carefully — they are where the action is.**
- p. 5, **Result 1** (technology must raise the real wage of at least one type
  of worker; corollary: with one type of labor, real wages rise).
- pp. 6–9, **Result 2** and its proof in the main text (average real wage rises
  if the investment-goods price index does not rise relative to consumption
  goods). The intuition paragraph on p. 9 is the one to hold onto.
- **p. 11, "Decreasing Returns to Scale" — the most important half-page in the
  whole reading list.** Read it twice.
- p. 13, "Non-Steady States" — their singularity paragraph (robots identical to
  people ⇒ labor no longer a fixed factor ⇒ wages to zero).

**Watch for — this is a finding, not a nuance.** Our §7 says C&M "prove that new
technology cannot lower the real wage in terms of the goods machines make."
That is not their theorem, in two ways:

1. Their Results 1 and 2 are stated against the **consumer price index** `e(p)`
   over the whole bundle, not against a machine-made-goods deflator. Result 1 is
   also weaker than we imply per worker — "at least one type of worker" gains,
   not all; Result 3 (all gain) needs perfectly elastic labor supply across
   occupations.
2. **Their benchmark assumes labor is the only fixed factor.** On p. 11 they name
   our exact escape hatch themselves: a decreasing-returns result "could be
   interpreted to say that while new technology increases the returns to fixed
   factors as a whole, it is just that labor is not the only fixed factor…it is
   possible that the benefits from new technology go to the owners of that scarce
   factor and not to labor. But this is a different argument from most accounts."

So Proposition 4(i) is not a concession inside their theorem's domain — our model
sits **outside** it, in the case they flagged and declined to build. That is a
stronger and more honest position than the one §7 currently takes, and it comes
with a named-in-print invitation. Worth a rewrite of that paragraph.

---

### 2. Acemoglu & Restrepo (2018), "The Race between Man and Machine," *AER* 108(6): 1488–1542 **[read in full: §I and §II.A]**

**Why:** Proposition 1 *is* their factor-price condition at the task margin. §1
says so. If this citation is wrong the paper has no starting point.

**Read:**
- **pp. 1494–1496, §I.A "Environment"**: eq. (1) task aggregator, eq. (2)–(3)
  task production, **Assumption 1** (γ(i) strictly increasing — our relabeling
  assumption, same object).
- **p. 1496, eq. (5) and eq. (6). This is the one.** eq. (5) is the unit cost
  `min{R, W/γ(i)}`; **eq. (6) is `W/R = γ(Ĩ)`** — literally our `w = c·γ(x*)`,
  with their γ(i) playing our γ(x) (capital productivity normalized to 1; the v2 rename makes the correspondence nominal). Then
  `I* = min{I, Ĩ}` on pp. 1496–1497: the distinction between the
  technologically-feasible and the cost-minimizing threshold.
- pp. 1500–1501, **Proposition 2** (comparative statics: automation ↓ W/R, new
  tasks ↑ W/R). Our Proposition 1(ii) — the slope governs the wage's
  sensitivity — is the same object read through Λ_I and ε_γ.
- pp. 1501–1503, **Proposition 3**: productivity effect vs displacement effect,
  and the result that automation *can* lower the wage when `K < K̃`.
- **p. 1506** (§II.A, balanced growth): the BGP condition **`R = ρ + δ + θg`**.

**Watch for:** p. 1506 is the sharpest single line for our contribution claim. In
A&R the machine rental `R` is pinned by the **Euler equation** — by preferences,
the discount rate and depreciation. It never resolves into what a machine is
made of. That is precisely the parameter §4 closes from the production side.
§2.3 currently says "the machine rental and the outside option enter as
parameters"; it can say something much more specific and harder to argue with:
*the rental is pinned by time preference, not by the machine's recipe.*

Minor: "reinstatement effect" as a coinage is A&R (2019, *JEP*), not the 2018
paper — 2018 says "creation of new tasks" (an increase in N). The mechanism we
cite is genuinely in 2018, so this is vocabulary, not a citation error.

---

### 3. Ljungqvist & Sargent (2017), "The Fundamental Surplus," *AER* 107(9): 2630–2665 **[read: §1 and §3]**

**Why:** §2.2 is the paper's central positioning claim — that modern macro-labor's
core calibration debate is a debate about the level of an object the framework
treats as a parameter. If this reading of the literature is wrong, §2.2 collapses
and with it the "we supply both endpoints" claim.

**Read:**
- **p. 2630, the abstract**, for the verbatim definition we quote: the
  fundamental surplus fraction, "an upper bound on the fraction of a job's output
  that the invisible hand can allocate to vacancy creation." (Already verified
  against the AEA page.)
- **pp. 2631–2632, §1 Introduction**, through eq. (1): `η_θ,y = Υ_j · y/(y − x_j)`
  — the elasticity of market tightness factors into a bounded piece and the
  inverse fundamental-surplus fraction, and only the second has no agreed bound.
- **Table 1 (p. 2632). Read the table itself, not the prose around it.** Every row
  is a proposed resolution of the Shimer puzzle, and every row is the same
  formula with a different deduction `x`: value of leisure `z` (Hagedorn–
  Manovskii), sticky wage `ŵ` (Hall), `ŵ + k` (Wasmer–Weil), `z + β(1−s)γ`
  (Hall–Milgrom), `z + β(r+s)H` (Pissarides 2009), `z + b` (UI), `z + βsτ`
  (layoff tax). This table *is* our §2.2 argument, in their notation.
- §3, "Fundamental surplus as essential object," esp. §3.2 on its relation to
  match surplus and outside values — the passage establishing that a small
  fundamental surplus fraction is the *only* reliable indicator.

**Watch for:** they are explicit that the deductions differ in economic
interpretation across models. Our claim is that in several of them the deduction
is a **price** rather than a taste parameter. Read Table 1 asking, row by row,
which `x` we can actually reprice with the two closures. Honestly, `z` is the
clean case; the sticky-wage and layoff-tax rows are not ours. §2.2 currently
implies a broader sweep than the table supports.

---

### 4. Acemoglu & Restrepo (2026), "Automation and Rent Dissipation," *QJE* 141(2): 1521–1579 **[read in full: §1, §2.2–2.3, §3.3, §4.3]**

**Why:** Appendix B is entirely theirs, restated in our notation, and Predictions
1–3 in Appendix I are transplanted from their estimates. Use the NBER WP w32536
version; page numbers below are the WP's.

**Read (WP pagination):**
- pp. 1–2, Introduction, the three numbered implications (average group wages,
  within-group dispersion, productivity/welfare).
- **p. 11, Proposition 3 (Targeting of high-rent tasks)** — our Proposition B.2.
  Note their Assumption 2 (neutrality of automation opportunities) is what does
  the work; our proviso about wedges whose institution can block adoption is the
  same caveat.
- **pp. 11–12, Proposition 4 (within-group wage compression) and Figure 1** —
  our Figure 6. The U-shape is a theorem here, not just an empirical pattern.
- **p. 2 and §3.3, p. 29** for the 70th–95th percentile claim.
- §4.3, **pp. 43–46** for the quantification: cost savings raised TFP 3%;
  rent dissipation offset 60–90%; net TFP contribution 0.3–1.3%; automation
  accounts for 52% of the rise in between-group inequality, a fifth of that from
  rent dissipation.

**Watch for — a number to fix.** Appendix B(b) says automated jobs pay "rents on
the order of 40–50% above base." Their estimate is **35% central, range
19–44.5%** (§3.3, WP p. 31; abstract and intro repeat 35%). The 50% figure is an
assumed value in a robustness column of Table 1, not an estimate. Change to
"about 35% (19–44.5%)". The 60–90% offset figure we quote is correct and is their
headline.

---

### 5. Korinek & Suh (2024), "Scenarios for the Transition to AGI," NBER WP 32255 **[read in full: §4.1]**

**Why:** §2.6 calls this "the closest formal predecessor." It is closer than that
sentence admits, and this is the referee risk to prepare for.

**Read:**
- §2.3–2.4, pp. 10–15: the two regions and the factor price frontier.
- **§4.1, "Fixed Factors and the Return of Scarcity," pp. 25–28. Read all of it.**
  Lemma 8 (production with a fixed factor M — "land, space, minerals, or solar
  radiation"), Lemma 9 (hump-shaped wage path, peak arrives earlier with M),
  **Proposition 10** (with a fixed factor, the economy enters region 2 in finite
  time and wages fall to `w = R = ρ + δ` — automation always outpaces capital
  accumulation), and Figure 9 (wages peak ~10 years, region 2 at 25 years).

**Watch for:** the differentiator is real but §2.6 states it imprecisely. Their
fixed factor enters the **final-good** production function as a Cobb–Douglas
term with a constant exogenous share `(1−α)`, so the rent share cannot migrate —
it is a parameter, set to 0.10 in their simulation. And their wage floor is
`ρ + δ`, a preference parameter, exactly as §2.6 says ("accumulated capital").
Our claim is different in kind: the fixed factor sits inside the **machine's own
cost recursion**, so `r/p` is endogenous and **divergent** (Prop 4(ii)), and the
wage resolves into rent rather than into the discount rate. That is a sharper
line than "differing in where the collapse ends," and it deserves more than a
clause — probably its own short paragraph in §2.6.

---

### 6. Sraffa (1960), *Production of Commodities by Means of Commodities*; Leontief (1936), *REStat* 18(3): 105–125 **[pointer]**

**Why:** `c = ac + λw + br` is theirs. §4 says so. Without this the closure has no
lineage and looks invented.

**Read (Sraffa, short book, read the chapters not the whole thing):**
- **Ch. I, "Production for Subsistence" (§§1–3, ~5 pp.)** — the bare price system
  where the surplus is zero. This is the structure of our recursion.
- **Ch. II, "Production with a Surplus" (§§4–9)** — where wages enter and the
  system gains a degree of freedom. §§8–9 introduce the wage as a share of the
  surplus; note that Sraffa lets `w` range from 0 to 1 rather than pinning it.
  **Our contribution is exactly that pinning: the task margin closes Sraffa's open
  degree of freedom.** This is the sentence §4 could make and currently does not.
- Ch. III on the standard commodity is not needed for us.
- **Ch. XI, "Land"** (§§85–87) — non-produced inputs entering the price system
  and rent as the residual on the intensive/extensive margin. This is the
  terminal-input position, in Sraffa's own hands.

Leontief (1936): §§1–2 for the input–output cost identity; that is the citation
for the empirical counterpart, §10's assembly (2).

---

### 7. George (1879), *Progress and Poverty* **[pointer]**

**Why:** §8's lineage sentence and the whole fiscal completion.

**Read (do not read the book; read two books of it):**
- **Book IV, ch. 2–3** — material progress raising rent, which is the qualitative
  version of Prop 4(ii).
- **Book VIII, ch. 3–4** — "the proposition tested," the efficiency argument for
  taxing land values: the tax cannot be shifted, does not reduce supply, does not
  discourage production. Prop 5(i) is this argument made inside a model.
- Book V, ch. 2 is worth ten minutes for the rhetorical register of the
  "progress and poverty" claim, which is our §12 in nineteenth-century clothes.

---

## Tier 2 — load-bearing for one section each

### 8. Lewis (1954), *The Manchester School* 22(2): 139–191 **[pointer]**
§2.5 calls this "the closest antecedent to Section 5." Read **pp. 139–149**: the
unlimited-supply setup and the determination of the modern-sector wage by what
the subsistence sector affords (including the customary ~30% premium over
subsistence earnings). Watch the difference we claim: his traditional sector is
exhausted by **absorption** as the modern sector grows; ours is **priced away by
rent** with no absorption at all. Check that this contrast survives his own text —
he discusses the terms of trade between sectors later in the paper, and that
discussion is the nearest thing to our mechanism.

### 9. Shimer (2005), *AER* 95(1): 25–49 **[pointer]**
The 20× volatility fact in §2.2. Read **§I, Table 1 and the surrounding pages
(pp. 27–30)** for the v/u ratio's volatility against labor productivity, and §IV
for why the calibrated model fails. Only the fact is load-bearing for us; it is
already verified against the source.

### 10. Hagedorn & Manovskii (2008), *AER* 98(4): 1692–1706 **[pointer]**
Cited twice — §2.2 (resolution via a high value of non-market activity) and §5
(the calibration sets the outside option high "for exactly this reason"). Read
**§II, the calibration section**, for how `z` is set relative to productivity
(their headline z ≈ 0.955 of productivity). **Watch for:** §5 says the high
calibration reflects the *inputs of unwaged life*. It does not — they back `z`
out to match observed volatility and wage cyclicality; the interpretation is
ours, not theirs. §5's sentence should attribute the number to them and the
interpretation to us, or a referee will call it out.

### 11. Rognlie (2015), *BPEA* Spring 2015 **[pointer, structure verified]**
The corollary's "the wealth data lean this way" and Prediction 6. Read
**§2, "Composition of the net capital share: the role of housing" and Figure 3**
(around p. 11 of the Brookings PDF): the entire postwar rise in the net capital
share is housing; outside housing there is a U-shape with no net rise. Then
**§4's nested framework**, where he separates housing from non-housing and
equipment from structures and land — that is the decomposition our claim needs.

### 12. Aghion, Jones & Jones (2019), in *The Economics of Artificial Intelligence* (NBER WP 23928) **[read: §2.2]**
Appendix G's stabilizer. Read **§2.2, "Automation and Baumol's Cost Disease,"
pp. 7–12 of the WP**: GDP as a CES aggregate with ρ < 0 (gross complements), the
"weak link" reading, eq. (11)–(14), and the result that the labor share is pinned
by the non-automated tasks however far automation runs. Our Proposition G.1 is
their mechanism restated over a task set K. Also worth reading **§4,
"Singularities"** — it is the case Caselli & Manning point at.

### 13. Baumol (1967), *AER* 57(3): 415–426 **[pointer]**
Short. Read it whole if you read Aghion–Jones–Jones; it is where the unbalanced-
growth asymmetry is set up, and Prop G.1 is named after it.

### 14. Zeira (1998), *QJE* 113(4) **[pointer]**
Cited in §1 and §2.3 as the threshold-logic ancestor. Read **§II**, the
technology-adoption threshold — a task is machine-produced iff the wage exceeds
the machine cost at that task. It is A&R's eq. (6) a generation earlier and in a
growth setting. Twenty minutes.

### 15. Diamond & Mirrlees (1971), *AER* 61(1) **[pointer]**
Prop 5(i) cites this as the production-efficiency analogue. Read the statement
and proof of the **production efficiency theorem in §III** only. **Watch for:**
their theorem requires 100% taxation of pure profits and a full set of commodity
taxes. Ours is the fixed-factor case, which is easier but is *not* their theorem —
§8 says "the fixed-factor analogue of," which is the right hedge; make sure it
stays hedged.

### 16. Arnott & Stiglitz (1979), *QJE* 93(4): 471–500 **[pointer]**
§8's "real but distinct" paragraph. Read **§II** for the Henry George theorem
statement: at optimal city size, aggregate land rents exactly finance the public
good. Confirm for yourself that the distinction we draw holds — theirs is a
local-public-goods financing result at an optimum, ours is a redistribution base
at a technological limit.

### 17. Jones & Marinescu (2022), *AEJ: Policy* 14(2): 315–340 **[pointer]**
Prop 5(ii)'s evidence. Read the **abstract, §I, and the main results table** for
the two numbers we use: no significant effect on aggregate employment, part-time
work up 1.8 pp. Already page-verified. Note the paper's own hedge — we call it
"consistent with the identity, though the identity itself is algebra" — which is
the correct relationship and worth keeping.

---

## Tier 3 — read only if you touch that specific claim

| Paper | Where we use it | What to read |
|---|---|---|
| Karabarbounis & Neiman (2014) | Prediction 5, §2.7 | Intro + Fig. 1 (global labor-share decline) |
| Knoll, Schularick & Steger (2017) | Prediction 6 | Intro + the house-price/land decomposition |
| Piketty & Zucman (2014) | §2.7 | Wealth–income ratios; the housing component |
| Gruber (1997) | §10 assembly (1) | Chile payroll-tax results table — full shifting |
| Kugler & Kugler (2009) | §10 assembly (1) | The 1.4–2.3%-per-10% estimate |
| Saez, Schoefer & Seim (2019) | §10 assembly (1) | Limited short-run shifting + firm-side responses |
| Allen (2001); Clark (2005) | §2.7, §9, assembly (3) | The welfare-ratio construction — that is the object we price as the floor |
| Bouscasse, Nakamura & Steinsson (2025) | §9 pre-industrial | The Malthusian-regime results; growth beginning before wages escape |
| Crafts (2022) | §9 industrial | Slow early real-wage growth |
| Autor, Levy & Murnane (2003); Autor & Dorn (2013) | §9 post-industrial | The routine-task hypothesis and polarization — cross-sectional dating only |
| Mas & Pallais (2019) | §5 | The willingness-to-pay estimates for non-work time |
| Hoynes & Rothstein (2019) | Prop 5(ii), F.1 | The income-effect evidence on UBI-type transfers |
| Rosen (1981) | App G superstars | The concentration mechanism |
| Romer (1990) | §4 ideas boundary | The non-rivalry + fixed-cost argument |
| Uzawa (1961) | §2.1 | The BGP labor-augmenting requirement |
| Moll, Rachel & Restrepo (2022); Hémous & Olsen (2022); Susskind (2017); Sachs & Kotlikoff (2012); Korinek & Stiglitz (2019) | §2.6 survey | Abstracts and intros; we only need to place them |
| Shapiro & Stiglitz (1984); Manning (2003); Card et al. (2018) | §2.4 wedges | Abstracts; the wedge layer is App B's, not the core's |
| MP (1994); Diamond (1982); Pissarides (2000); Hall (2005) | §2.2 | Only if Ljungqvist–Sargent's Table 1 leaves a row unclear |
| Samuelson (1966); Arrow (1951); Ricardo; Malthus; Polanyi | one-clause citations | Skip unless challenged |

---

## Suggested order for the sessions ahead

1. **Caselli & Manning** (one sitting, ~40 min) — because it changes a paragraph.
2. **A&R 2018 §I** (one sitting) — because it is our first equation.
3. **Ljungqvist & Sargent Table 1 + §1** (30 min) — because it is our positioning.
4. **Korinek & Suh §4.1** (30 min) — because it is the referee risk.
5. **Sraffa Ch. I–II + Ch. XI** (one sitting) — because it names the contribution.
6. **A&R 2026 Props 3–4 + §4.3** (one sitting) — because Appendix B is theirs.
7. Then Tier 2, in the order the sections come up in revision.

## Open items this reading produced

- [ ] §7: rewrite the Caselli–Manning paragraph. Their theorem's domain excludes
      us by their own statement (p. 11); we should say so rather than concede
      inside it.
- [ ] App B(b): 40–50% → about 35% (19–44.5%), A&R 2026 §3.3.
- [ ] §2.3 / §4: name the A&R closure precisely — the rental is pinned by the
      Euler equation, `R = ρ + δ + θg` (A&R 2018, p. 1506).
- [ ] §2.6: expand the Korinek–Suh differentiator to a paragraph; their §4.1 is
      close enough that a clause reads as evasion.
- [ ] §5: separate Hagedorn–Manovskii's number from our interpretation of it.
- [ ] §2.2: check Table 1 row by row — not every deduction `x` is a price we can
      reprice, and the section currently implies all of them are.
- [ ] §4: consider stating the Sraffa relationship as "the task margin closes the
      degree of freedom Sraffa leaves open."
