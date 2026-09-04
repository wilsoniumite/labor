# Every word in every figure — latex/v5.tex (2026-09-03)

Captions are verbatim from the tex (LaTeX markup kept). In-figure text is taken from the script that draws each figure and checked against the rendered PNG; a slash marks a line break inside one label. Figures are numbered in the order they appear.

## Figure 1 — `fig_schedule.png` (`fig:schedule`)

Drawn by: `the-link-revision/code/fig_model_schematics.py`

**Caption (tex):**

The task-assignment schedule. Tasks are ordered so $\gamma(x)$ increases. On the machine-contestable set, the ratio $w/c$ divides tasks: machines hold tasks with $\gamma(x)<w/c$, labor holds tasks with $\gamma(x)>w/c$, and an interior margin $x^*$ satisfies equality. Tasks in $H$ are closed to machines and appear as a wall at the right edge. If labor holds no machine-contestable task, the wall marks a boundary case rather than an additional price schedule. A cheaper machine or a lower $\gamma$ near an interior margin shifts tasks toward machines.

**Text inside the figure:**

- x-axis label: Tasks x, ordered by increasing γ; closed tasks last
- y-axis label: Relative human productivity γ(x)
- annotation: w/c
- annotation: x*
- annotation: Machines: γ(x) < w/c
- annotation: Labor: γ(x) > w/c
- annotation: H: tasks closed to machines

## Figure 2 — `fig_eras_workers.png` (`fig:eras`)

Drawn by: `the-link-revision/code/fig_eras_workers.py`

**Caption (tex):**

Four schematic configurations of the task schedule, shown for an untrained entrant (top) and a worker with accumulated training or experience (bottom). Closed tasks appear as a wall at the right edge. A dot on the machine-contestable schedule marks an interior task margin; a dot on the wall marks the boundary case in which no machine comparison pins the wage. In the pre-industrial configuration, most tasks are closed for both worker types. Industrialization opens many physical tasks and creates a steep contestable margin, initially affecting less-trained workers most directly. Computing flattens the routine region while many trained tasks remain closed. In the candidate AI configuration, the closed set retreats for both worker types and the contestable schedules flatten.

**Text inside the figure:**

- panel title (top): Untrained entrant
- panel title (bottom): Worker with training or experience
- x-axis label: Tasks x, ordered by this worker's γ; closed tasks last
- y-axis label: Relative human productivity γ(x)
- legend: pre-industrial (to about 1780)
- legend: industrial (1780–1950)
- legend: computing (1970–2020)
- legend: Candidate AI
- annotation, top panel: Wall boundary: participation floor binds
- annotation, top panel: Steep task margin: machine substitution prices the wage
- annotation, top panel: Flat task margin: wage locally pinned
- annotation, top panel: Contestable schedule nearly flat
- annotation, bottom panel: Wall boundary: floor and skill scarcity
- annotation, bottom panel: Wall boundary: skilled tasks remain closed to engines
- annotation, bottom panel: Wall boundary: skilled tasks remain closed to computers
- annotation, bottom panel: Retreating wall: training premium may narrow

## Figure 3 — `fig_deflator_fork.png` (`fig:fork`)

Drawn by: `effort-accounting/code/build_fig3_realwage_fan.py (its output FIG3_realwage_fan_1950.png, renamed to the old fork name for Overleaf — her note, 2026-09-02)`

**Caption (tex):**

U.S. average hourly earnings for production and nonsupervisory workers deflated by the consumer-price indexes for durables, food, energy, and shelter, 1950 = 100, through the last complete calendar year, 2024. Values before 1964 use the spliced wage series. The energy index begins in 1957; its 1950--1956 values are a linear backcast estimated over 1957--1966. Over 1964--2024 the ratio of the durables-deflated to the shelter-deflated wage reaches $4.8\times$, a ratio that does not depend on the index base.

**Text inside the figure:**

- title: The deflator fork: the same U.S. paycheck against four consumption categories
- legend: durables CPI (machine-made goods)
- legend: food CPI
- legend: energy CPI (1950–56 backcast)
- legend: shelter CPI (land-priced)
- note inside the plot: dashed pre-1964: spliced-wage era (members and seams as in the 1950 fork variant); food is CPI food NSA from 1950; the energy aggregate begins 1957 — dotted 1950–56 is a linear deflator backcast (fit 1957–66). Complete calendar years through 2024.
- end-of-line labels: durables / food / energy / shelter
- x-axis label: Year
- y-axis label: Real average hourly earnings, 1950 = 100

## Figure 4 — `fig_kappa_measurement.png` (`fig:kappa`)

Drawn by: `the-link-revision/code/fig_kappa_measurement.py`

**Caption (tex):**

The coverage ratio $\kappa=rT/(N\cdot P_s)$ is aggregate site-rent flow divided by the cost of providing the specified subsistence bundle to every person; U.S., 1953--2025. The line is the median and the band is the min--max range across specifications combining land sources, capitalization rates, and subsistence bundles. The dashed specifications subtract residential structures at replacement cost (Z.1, BOGZ1LM155012665Q) from household real estate at market value (Z.1, FRED HNOREMV) and convert the residual to an annual flow using the 10-year Treasury yield (GS10), with a +150 basis-point variant and household and economy-wide scopes. The red specifications apply land shares of 0.30 and 0.50 to PCE housing services (BEA, DHSGRC1A027NBEA). Every specification uses population times the Orshansky 1963 subsistence bundle as the denominator.

**Text inside the figure:**

- title: Rent-funded-floor coverage: two measures of U.S. site rents
- legend: Min–max range across specifications
- legend: Median across specifications
- legend: Real-estate residual × Treasury yield (median)
- legend: Share of BEA housing services (median)
- legend: κ = 1 (full coverage)
- y-axis label: Coverage ratio κ = rT/(N·P_s)

## Figure 5 — `fig_consumption_financing_and_human_effort.png` (`fig:labor-linkages`)

Drawn by: `effort-accounting/code/build_fullband_df_figures.py (the D-F vs D-Q full-band figure; the PNG is your Overleaf upload — confirm it is this render)`

**Caption (tex):**

Two labor linkages in U.S. consumption, 1950--2025. The upper series is the share of consumption financed from labor-origin resources; the lower is the share of consumed production that resolves into human effort through the full production chain. Markers identify the benchmark-data windows: annual BEA income-source profiles for financing in 2004--2023 and the BEA full-chain production benchmark in 1997--2023. Values outside those windows are model-based extensions. In the common benchmark-data window, consumption is substantially more labor-financed than production is labor-intensive.

**Text inside the figure:**

- title: Financing origin and production content are different labor linkages
- legend: D-F weak-extension interval
- legend: D-F partial-identification interval
- legend: D-Q weak-extension band
- legend: D-F financing — weak extension
- legend: D-F financing — annual source profiles
- legend: D-Q production labor — weak extension
- legend: D-Q production labor — BEA full-chain benchmark
- x-axis label: Year
- y-axis label: Percent of PCE

## Figure 6 — `fig_fourway.png` (`fig:fourway`)

Drawn by: `link-repo/code/make_figs.py (Fig 5)`

**Caption (tex):**

Composition of U.S. consumption financing excluding consumption financed directly from household capital income, in which owners consume their own returns, 1962--2025. Lines are medians across the classification-rule grid; the shaded band spans the deficit-attribution rules. The direct-wage share fell by about twenty percentage points over sixty years. Transfers grew while approximately one quarter of their financing continued to come from taxes on ownership income. Borrowing financed 19\% of transfers in 2025 and was zero only in 1998--2000. The allocation is pro-rata accounting, not an estimate of tax incidence.

**Text inside the figure:**

- legend: direct wages
- legend: transfers from wage taxes
- legend: transfers from ownership taxes
- legend: transfers from borrowing
- annotation: 1998–2000: the only fully tax-financed years
- annotation: crisis borrowing
- x-axis label: year
- y-axis label: % of non-owner-loop consumption financing
