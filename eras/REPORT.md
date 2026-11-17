# Eras: rough shapes and sizes of the task schedule through history

A first look, 2026-11-17, at her ask: "Do you think there's any way we could actually visualise shapes and sizes for
historic task curves and the regions within? Even if they're rough?" ("Its just to take a look, might be a paper down
the line.") Nothing here touches `../pinning/`.

The regions are the paper's: machines below the margin x*; the contestable band between the margin and the ceiling;
tasks behind the ceiling (machines could do them, but never more cheaply); H (machines cannot). The task measure is the
model's own: with gamma_L = 1, a task's size is the hours it takes by hand, so x* is the share of hand-equivalent work
that non-human inputs perform.

## Findings, roughest last

1. **The ceiling has sat 1.3–1.9 times above the margin for 150 years** (`figures/skeleton.png`, panel a). US
   machinery's full-chain labor share (the lambda thread, BEA input–output, 1967–2023) puts it at 1.35–1.9, about 1.8
   now; Appendix B's 1.71 is mid-range. Before 1967 there are no input–output tables here; the UK whole-economy labour
   share excluding rents (Bank of England, 1855–2016) stands in, at 1.3–1.7. Where the US has both, machinery's share
   runs 0.02–0.14 above the economy's, so the proxy is rough and likely puts the ceiling too low.

2. **The contestable band is a modest slice of the tasks people perform, in every era measured**: about 8–16 percent
   central, 3–30 percent across the assumptions (`figures/skeleton.png`, panel b). The elasticity of substitution
   dominates the uncertainty, not theta.

3. **1999–2025: the margin and the ceiling climbed the schedule together** (`figures/modern_schedule.png`, panel a).
   The companion thread's revealed adoption puts each occupation that switched to machines at the waterline (wage over
   quality-adjusted machine prices) of its switch year. The waterline rose 8.0 times. 86–99 percent of the switched
   employment sat above the 1999 ceiling: those tasks were opened as the ceiling rose, which is recursive automation
   in quality-adjusted machine units. The envelope is steeper than sigma 0.6 implies: s_M sigma comes out 0.05–0.16
   (sigma about 0.1–0.35 at s_M 0.45), which would narrow today's contestable band to 3–9 percent.

4. **2025 split of the tasks people perform** (`figures/modern_schedule.png`, panel b): contestable 3–16 percent;
   behind the ceiling but LLM-capable 0–48 percent; H for LLMs 49–85 percent. The middle reading (exposure's beta
   aggregation, sigma 0.6) is 16 / 17 / 67. LLM exposure understates what machines can do (robots and other software
   add to it), so H here is an upper bound.

5. **The machines' region was never small** (`figures/machines_region.png`). In England and Wales around 1700,
   non-human power already did about 65 percent (48–78 percent) of the hand-equivalent work, mostly draught animals;
   mills and sails alone did about 25 percent (14–41 percent). The share held flat until about 1840 and rose with steam
   to about 74 percent by 1870. After 1870 the model's own accounting (output per final-task hour is 1/(1 - x*))
   reads x* from output per hour: about 95 percent by 1970 and 98 percent by 2016, so people do 1–3 percent of the
   hand-equivalent work. The Hand and Machine Labor study's US manufactures (machine-method time 0.14 of hand time,
   about 1895) sit near the UK path (0.19 then).
   - In the model's terms a draught animal is non-human capital: bred, fed from land, tended by labor. Its b-tilde is
     large, which ties the pre-industrial replacement price to land rent.
   - **The overlap test fails, informatively.** Between 1760 and 1870 output per hour doubled, but people's share of
     hand-equivalent work, counted from power, fell by only about a quarter. Early-industrial productivity came from
     more than power: division of labour, organisation, more hours. The reading after 1870 therefore overstates x*.

6. **The margin's path traces a schedule that curves up like 1/(1 - x)** (`figures/eras.png`, panel a). The task
   condition makes the margin's relative productivity equal the wage over the machine rental. If the schedule held
   still in machine-service units, each year's margin is a point on it. With x* from finding 5 and the UK wage over
   the investment deflator (1830–2016), the points lie on gamma proportional to (1 - x)^-0.78. In hand-equivalent
   units the schedule rises toward the end of the task axis. Part of this is built in, since both axes scale with
   output per hour under balanced growth, and the investment deflator prices buildings with machines. The slope is
   the statement; the curvature is not evidence.

`figures/eras.png`, panel b, puts the sizes side by side for c. 1700, c. 1870, c. 1970 and 2016–2025. The H versus
behind-the-ceiling split exists only for 2025.

## Sources and what was not reached

- Warde, P. (2007), *Energy Consumption in England & Wales, 1560–2000*, CNR: appendix table 1 (energy inputs by
  carrier) and table 8 (fixed motive power). PDF at Harvard's energy-history site; parsed 1560–1870, carriers add to
  the printed totals within 0.2 PJ.
- Thomas, R. and N. Dimsdale (2017), *A Millennium of Macroeconomic Data for the UK*, v3.1, Bank of England: sheets A1
  (GDP, employment, hours, GDP per hour, labour share) and A47 (earnings, deflators).
- Atack, J., R. A. Margo and P. W. Rhode (2019), "'Automation' of Manufacturing in the Late Nineteenth Century: The
  Hand and Machine Labor Study," *Journal of Economic Perspectives* 33(2): 51–70, the published mean only. **The
  operation-level microdata (openICPSR project 166741) returned HTTP 403 from this container.** Nothing was substituted
  for it. With an openICPSR login on her machine it would give the 1890s distribution of hand/machine time across
  ~7,000 tasks, a real shape for the industrial era.
- In the repo: the lambda thread's machinery shares (`../progress_and_prosperity/lambda/data/`), and the companion
  thread's switches, waterline and LLM exposure (`../companion/data/`).

## Assumptions (bands, not data)

Human sustained power 50–100 W; draught animals 7–13 percent feed to work (Warde: about 10); water wheels 15–40
percent rising to 30–75 percent by 1870 (Warde: 15 early, up to 85 late); sails and windmills 25–50 percent; steam
engines run 1,500–3,500 hours a year; sigma 0.3–0.9; s_M 0.35–0.55. Before 1760 employment follows the 1760 ratio to
population. The history is England/UK, the modern detail US.

## What would sharpen it

- Leontief's 1919 and 1929 US tables for theta before 1967.
- The Hand and Machine Labor microdata, for the industrial era's shape.
- A hedonic machinery price index for the long waterline, in place of the investment deflator.
- Census occupations crossed with task content (DOT) for an H split before 2025.

## Files

`code/pull.py` (sources to `data/`), `code/machines_region.py`, `code/skeleton.py`, `code/modern_schedule.py`,
`code/eras.py`; run in that order from `eras/`. Each writes its CSV to `data/` and its figure to `figures/`.
