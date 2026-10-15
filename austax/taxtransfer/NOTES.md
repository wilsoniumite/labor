# Australia's tax and transfer facts (austax/taxtransfer)

Napkin-grade support for the Austaxpolicy article, built 2026-10-15. It is the Australian mirror of the paper's
Appendix D table (US: 0.68 of tax revenue from labour-income bases; at least 0.84 of benefits conditioned on work
or means). These are new estimates for a blog post, not paper results.

Run: `venv\Scripts\python.exe -I code\build_facts.py`, then `code\fig_income_shares.py`, then
`checks\check_facts.py` (67 checks; last run: 67/67 PASS).

## Sources
- ABS, Taxation Revenue, Australia, 2024-25 (released 21 April 2026; formerly cat. 5506.0). Key tables
  55060DO002 (Table 2 sub-categories, Table 3 published distribution, Table 5 totals) and detail tables 55060DO001
  (Table 1 Commonwealth, Table 10 all states, state and local). All levels of government, financial years ending
  30 June, general government plus taxes received from public corporations, net of intergovernmental taxes.
- History: ABS 5506.0 2009-10 data cube (released 12 April 2011; Tables 1 and 18, 2000-01 to 2009-10), and the
  all-levels totals from the archived 5506.0 2005-06 main features (2000-01) and 2009-10 main features page 7
  (2009-10).
- ABS 5206.0 National Accounts, June quarter 2026 (released 2 September 2026), Table 7 Income from GDP, original
  current-price series: compensation of employees A2302401K, total factor income A2302411R, gross operating surplus
  of dwellings owned by persons A2302408A, gross mixed income A2302410L. Checked against the ABS Data API dataflow
  ANA_INC (all 67 financial years agree).
- OECD (2018), The Future of Social Protection, chapter 2 "Australia: Providing social protection to non-standard
  workers with tax financing" (Peter Whiteford and Alexandra Heron), published 7 November 2018,
  https://doi.org/10.1787/9789264306943-en.
- DSS Social Security Guide 4.2.1.10, 4.2.2 and 4.2.3 (guides.dss.gov.au). Services Australia and dss.gov.au timed
  out from this machine, so the DSS guide (the department's own decision-maker guide) is the source for the
  income and assets test statements.
- US comparison: BEA NIPA via FRED W055RC1A027NBEA, A061RC1A027NBEA, W054RC1A027NBEA (calendar 2025).

## Definitions and choices
- (i) Taxes on income of individuals = personal income tax + Medicare levy (ABS line "Government health insurance
  levy"), excluding fringe benefits tax. The ABS category "Income taxes levied on individuals" includes FBT.
- (ii) Payroll taxes = state payroll tax. (ii') adds other taxes on employers' payroll and labour force (mainly the
  Commonwealth superannuation guarantee charge).
- (iii) Fringe benefits tax (Commonwealth).
- Taxes mainly on labour = (i) + (ii') + (iii) = ABS "Income taxes levied on individuals" + "Total taxes on
  employers payroll and labour force".
- (iv) Company income tax excludes income tax paid by superannuation funds (shown separately).
- Recurrent taxes on land = land taxes + municipal rates. (vii) Stamp duties on conveyances, from the state and
  local table (no intergovernmental netting applies to this line at the all-levels level).
- Labour's share = compensation of employees / total factor income; four original quarters summed to the
  financial year ending June. Total factor income = compensation of employees + gross operating surplus + gross
  mixed income (identity holds to within $3m in the API data).

## Headline numbers
Tax, all levels of government, 2024-25 (total $838,974m, 30.2% of GDP per ABS):

| Item | Share of total tax |
|---|---|
| (i) Income tax on individuals incl. Medicare levy, excl. FBT | 40.8% |
| (ii) Payroll tax / (ii') all taxes on employers' payroll and labour force | 4.8% / 5.0% |
| (iii) Fringe benefits tax | 0.6% |
| **Taxes mainly on labour (i)+(ii')+(iii)** | **46.4%** |
| (iv) Company income tax | 17.1% |
| (v) GST | 11.3% |
| (vi) Land taxes / municipal rates / **recurrent taxes on land** | 2.4% / 3.0% / **5.4%** |
| (vii) Stamp duties on conveyances | 4.1% |
| Income tax paid by superannuation funds (not counted as labour) | 3.1% |

History (share of total tax): taxes on individuals' income excl. FBT 36.1% in 2000-01, 36.5% in 2009-10, 40.5% in
2015-16, 40.8% in 2024-25. Recurrent taxes on land 4.0%, 5.2%, 5.2%, 5.4%. Taxes mainly on labour 42.2%, 42.6%,
46.3%, 46.4%. Year to year the individuals' share (ABS category) moved between 38.9% (2021-22) and 42.5% (2023-24).

US on the same simple definition, (personal current taxes + social insurance contributions) / (tax receipts +
contributions), calendar 2025: 0.647.

Labour's share of total factor income: 54.1% in 2025-26; 62.0% in 1974-75 (the series peak); 55.2% in 2000-01;
50.3% in 2021-22 (the series low); 50.4% in 1959-60. Gross operating surplus of dwellings owned by persons: 9.1% of
total factor income in 2025-26, 7.7% in 2000-01, 4.4% in 1974-75, 2.4% in 1959-60.

Transfers: OECD (2018): "the Australian social security system is highly income-tested, with spending being more
targeted to the poor than any other OECD country"; "nearly 80% of total benefit spending in 2012" went to
income-tested payments; the main non-income-tested spending is state workers' compensation and pensions for retired
public servants (note 3), both tied to past work. DSS: the benefits income test and the benefits assets test apply
to JobSeeker Payment; the pensions income test and the pensions assets test apply to all pensions, including the
Age Pension (rate calculator A).

## Caveats
- Not like-for-like with the paper's US 0.68, which is model-based: it counts the wage part of personal income tax,
  all social contributions and labour-linked slices of company and sales taxes. On one simple definition the US is
  0.65 and Australia 0.46. Australia has no social security contributions: pensions and unemployment payments are
  paid from general revenue, and compulsory employer superannuation is private saving, not tax.
- (i) also taxes individuals' capital income (interest, dividends, rent, capital gains), which pushes the labour
  share up. Not counted, which pushes it down: the tax on superannuation contributions (inside the 3.1% paid by funds),
  any labour-origin slice of GST, and any part of company tax that falls on wages.
- Municipal rates are levied on land value in some council areas and on land plus buildings in others, and state
  land taxes mostly exempt the owner-occupied home; "recurrent taxes on land" is a description of the tax lines, not
  a measure of land rent.
- History joins three ABS vintages (2007, 2011 and 2026 releases). Seams tested: the 2000-01 individuals' share
  matches the ABS-published 37.9%; the 2005-06 all-levels total was revised by -0.06% between releases; land taxes
  and rates in 2000-01 come from a state and local table before intergovernmental netting (at most 0.1 point).
- 2025-26 national accounts are first estimates and will be revised. Compensation of employees excludes the labour
  income of the self-employed (in mixed income); treating mixed income as split like the rest gives 58.4% in 2025-26
  and 71.8% in 1974-75. Dwellings' operating surplus is before interest and depreciation and includes the return on
  buildings, so it is not land rent.
- The OECD targeting figures are for 2012 and were published in 2018; they are quoted, not recomputed here.
