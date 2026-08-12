# Block E — the misallocation ledger (working sketch, FIRST LOOK)

**Status.** Drafted 2026-08-09 on Stella's commission: *"pursue the idea, not wanting to
prove it, but to see what it looks like."* Everything here is exploratory. Per the
standing data-purpose rule, NO number in this block may be quoted as measured weight
until its channel's chain (counterfactual + attribution + magnitude) holds; the first
look computes the pieces that are pure accounting and brackets the rest with named,
imported dials. Origin: the blog post "Millions of Lifetimes" (wilsoniumite.com,
2026-08-04) — lifetimes that "would most likely have been put into leisure. Do not
forget, leisure means taking care of parents, of kids, of meeting friends in third
spaces."

## E.0 The object

Misallocated labor, in person-years per year:

    L(t) = Σ_i [ h_i(t) − h*_i(t) ]₊

where h* is the hours person i would choose in the undistorted configuration the
model can state exactly: exit unpriced at the natural floor (no enclosure debt,
Prop 9), income support unconditional (Δ = 0, Prop 6), no slack employment
(species 4 = 0), and acquisition undertaken only at true marginal premia (no
composition illusion, C3). h* is not observable; the ledger is built channel by
channel, each with its own counterfactual and attribution instrument. **Sign
caution, structural:** some distortions run the other way — a payroll-tax wedge
*suppresses* hours (Prescott's channel) — so the aggregate gap is a NET shadow;
channels can individually exceed it.

## E.1 The four channels (each already in the machinery)

| # | Channel | Model anchor | Counterfactual | Attribution instrument | Status |
|---|---|---|---|---|---|
| 1 | Enclosure-manufactured participation (rent forces the second earner; exit priced away) | Prop 9 remark (a): "enclosure manufactures labor supply" | participation at s = s₀ | Prediction 13 machinery: household formation, coresidence, second-earner participation against LOCAL rent-to-wage, not unemployment | OPEN — the P13 cross-metro panel is the next data build |
| 2 | Conditionality-summoned work; the giant U.S. instance is employment-tied health insurance | Prop 6(ii); the λ table's blind spot — ESI is a work-conditioned in-kind transfer with λ = 1, outside the public-benefits table | coverage decoupled from the job | quasi-experiments already in the literature: employment-lock estimates (Madrian 1994; Garthwaite–Gross–Notowidigdo 2014 QJE); ACA-era labor-supply releases | FLOW measured by us (first look, below); the summoned-hours response is an IMPORTED bracket, labeled |
| 3 | Slack employment (species 4: labor sustained by rent dissipation) | Block D species 4 | competitive product markets + measurement | procyclical purges concentrated in high-market-power firms (P-D5) | CONTESTED survey base (Graeber vs Soffia–Wood–Burchell); enters only as a wide labeled dial |
| 4 | Queue years and doomed acquisition (study time for premia the marginal entrant never receives) | C3 (composition needs no friction), C4 (doomed vintage) | entry at true marginal premia | our own measurements: the 35-year ~38–48% recent-graduate underemployment series; IPEDS completions × persistence-of-underemployment | PARTLY MEASURED (queue); C4 pass queued |

Interactions are real (a rent-forced second earner may also be insurance-locked);
the ledger must not double-count — the first look keeps channels separate and
reports them unsummed.

## E.2 The aggregate shadow (the Keynes gap) — envelope, NOT attribution

U.S. annual hours per worker fell steeply for a century, then stopped: roughly
3,000 (1870s) → ~1,900 (1950) → ~1,800 (1980) → ~1,750–1,800 (today), while
productivity more than doubled after 1980. Continuing the 1900–1980 rate of
decline would put hours near 1,300–1,400 today — where Germany actually is. The
gap, ~400 hours per worker-year across ~160M workers, is on the order of
**30 million work-year-equivalents per year** — decades of which is the
"millions of lifetimes" arithmetic. **This is an unattributed envelope.** Rival
attributions are live and partially opposite-signed (Prescott: taxes suppress
European hours — i.e., the U.S. level is the *undistorted* one; preferences;
emulation/status races; measurement of home production). The envelope's job in
the ledger is only to bound the channels and to pose the question sharply — the
stopping of the decline coincides with the scissors era (λ_R locking, labor
share turning) and with the enclosure era (the deflator fork opening), which is
suggestive and no more.

## E.3 First-look magnitudes (what is computable today, and the dials)

- **(2) ESI flow, ours:** employer group-health contributions from NIPA (pulled
  and validated in `code/misallocation_firstlook.py`) — the size of the pipe
  that conditions coverage on employment. Summoned hours: imported bracket only —
  employment-lock literature puts the *exit-margin* stock (people who would leave
  employment entirely if coverage decoupled) around **0.5–1M workers**
  (GGN 2014's counterfactual family), i.e. ~0.5–1M person-years/yr, with wider
  job-lock (mobility, not exit) several times larger but NOT summed here since
  mobility-lock is misallocation *between* jobs, not extra hours.
- **(4) Queue/doomed acquisition, ours + one dial:** ~2M bachelor's conferrals/yr
  × 4–6 years of study each ≈ 8–12M study-years committed per cohort-year; the
  chronically-underemployed share of recent graduates is measured at ~40%, and
  the share of those who never escape is the dial (published follow-ups put
  roughly half still underemployed a decade on — imported, labeled). Doomed
  study-years per cohort-year under that dial: **~1.5–2.5M** — before the C4
  copy-window channel adds to it.
- **(3) Slack, dial only:** employment share dial [0.05, 0.20] (Soffia et al.'s
  ~5% self-reported "useless" floor to Graeber's high estimates), × an
  hours-that-are-actually-work factor left explicitly at [0.5, 1]. Enters the
  figure as the widest, palest bracket.
- **(1) Enclosure, open:** no number until the P13 panel runs. The channel most
  native to the paper and least measured — deliberately listed with an empty
  magnitude cell so the gap is visible.

## E.4 Welfare accounting, stated once

The counterfactual hours are not idleness: the blog's point, and Prop 9's — exit
and leisure are care, parenting, third places — home production with real product
outside GDP. So the ledger's welfare reading is conservative when it prices
foregone leisure at s: the true loss includes unpriced care displaced. Conversely,
hours a person would choose anyway (work as meaning) must never be counted — the
[·]₊ and the channel-level counterfactuals are what keep this honest. The species-3
lesson applies here too: not every wedge is welfare-free to demolish, and not every
hour above h* is pure loss to its holder.

## E.5 Integration and predictions

- Home: **paper three's welfare spine** — the hours-of-life dimension of the fork.
  The corner ending gains its sharpest sentence: the unconditional side is the
  first configuration that stops charging lifetimes for income.
- The fiscal half of the main paper gains one row at merge (surgical list,
  pending): ESI as a work-conditioned transfer the conditionality table missed.
- **P-E1.** Where coverage decouples from employment (ACA marketplaces, public
  options), exit-margin labor supply falls measurably among the previously locked
  (partly already documented — the channel's live test).
- **P-E2.** Second-earner participation tracks local rent-to-wage conditional on
  wages, and weakens where housing is cheap (P13 restated at the household margin).
- **P-E3.** Slack purges (P-D5) reduce measured hours with no output loss —
  distinguishable in firm data from ordinary layoffs, which reduce both.
- **P-E4.** Under any unconditional-income pilot at scale, hours fall most among
  exactly the populations channels 1–2 mark as summoned — and little elsewhere
  (the income effect near zero for the unsummoned is the paper's own Prop 6
  evidence read forward).

## Decisions needed (Stella's)

1. The benchmark stance for h*: preference-at-current-prices (as drafted) or a
   normative floor (h* = hours at a guaranteed subsistence). The drafted choice is
   the conservative one.
2. Whether channel 3 (slack) belongs in the ledger at all, given its survey base —
   or waits for P-D5-style firm evidence.
3. Whether the Keynes-gap envelope appears in any figure that leaves this folder,
   given how loudly it must be labeled unattributed.
