# STATE — austax (blog-support thread)

**Project:** Australian data for the Austaxpolicy article summarising *Pinning the Wage to Scarcity and
Technology* (Johan Båge and Stella Wilson). Austaxpolicy is the Tax and Transfer Policy Blog of the Tax and
Transfer Policy Institute (ANU and Monash). It asked for 800 to 1,200 words. Stella asked on 2026-10-15 to
"reconfigure it around aus data". Napkin-grade, like `three-drivers/`, with the same no-fudging rules: public
official data only, every raw file vendored with a manifest, and each number recomputed by a check script.
**State as of:** 2026-10-15. Thread created, committed and pushed this session.

## Where things stand

Three measures. Each was built by one agent and re-derived independently by another
(`checks/verify_independent.py` in each folder). Every check passes.

| Folder | Mirrors in the paper | Headline (2024-25 or 1998-2025) |
|---|---|---|
| `paycheck/` | Figure 5, US pay deflated by price category | What an hour's pay buys (Wage Price Index), 1998-2025: durable goods +242% (3.4 times), food +4%, rents +1.5%, energy -30% (after the 2023-25 electricity rebates). Established houses (ABS index, includes land): -45% over 2002-2021. Average full-time weekly earnings, 1995-2025: rents +26%. |
| `coverage/` | Figure 6, the coverage ratio | Collecting all land rent covers about one-seventh (land as 30 to 50% of housing rents, 0.14) to a little over half (land values at the bond yield, 0.57) of a basic living standard per resident. Range 0.10 to 0.85 across 18 estimates. Not comparable with the US 0.33. |
| `taxtransfer/` | Appendix D table | Income tax on individuals plus FBT plus payroll taxes = 46.4% of $839.0bn (2024-25). Land taxes plus council rates = 5.4%. Compensation of employees fell from 62.0% of total factor income (1974-75) to 54.1% (2025-26, first estimate). Dwellings' gross operating surplus rose from 2.4% (1959-60) to 9.1%. OECD (Whiteford and Heron 2018): the most targeted transfers in the OECD. |

Each folder's NOTES.md lists its sources, definitions, caveats and how to run it. The verifiers' do-not-publish
items are recorded in the session's working files and summarised here:
- No Australia-versus-US ranking, either of the durables gap or of coverage. The baskets and land measures differ.
- No unqualified energy number. The CPI electricity series is held down by the 2023-25 rebates.
- No tax-share trend from a 2000-01 base. 2000-01 is a low year, so use decade averages.
- "Gross" stays on the dwellings measure. Council rates are not labelled "taxes on land".

The article itself is a Claude Doc:
https://claude.ai/code/artifact/0cfce69c-cce6-466a-9e44-7e374a15920c

## Open — her calls

1. Done 2026-10-15 at her go: `austax/` committed and pushed to main. The article's code link now points at
   `github.com/wilsoniumite/labor/tree/main/austax`.
2. The lead wage series is the Wage Price Index, which tracks pay for the same jobs. The verifier chose it over Average
   Weekly Earnings: AWE starts only three years earlier, and the ABS says AWE is not designed to measure movement.
   The AWE figure is built (`paycheck/out/figure_au_paycheck_awe.png`) if she prefers it.
3. A second figure is available (`coverage/out/figure_au_coverage.png`, 1990-91 to 2024-25). It is not used, for length.
