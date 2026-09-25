# paths — the dynamic model, built for risk

Paths over time for the paper's mechanism: how wages, rents, prices, policy rates and the yield
curve move as automation proceeds, at speeds set by three clocks — **technology** (how fast
automation moves wages, jobs and rents), **recognition** (how fast markets price it) and
**institutions** (how fast central banks, taxes and transfers respond). The aim is scenarios
coherent enough to stress a bank's balance sheet: rate paths, not single shocks.

Built from scratch (not on `../dynamics/`, whose engine is real-side only, at a fixed world rate,
on the configurations before the interior revision). **Public data only**: FRED, Statistics Sweden,
the Riksbank, the ECB. Any application to a particular bank's book happens elsewhere, and nothing
from it is reproduced here.

**Start with `STATE.md`.**

## Layout

| Path | What it is |
|---|---|
| `code/curve.py` | The curve layer: policy rate, cycle target, destination, speed, term premium, basis; closed-form zero and forward curves; the modes; the policy rule; the supervisory (SOT) shapes for comparison. |
| `code/regimes.py` | Expectations as a mixture of regimes: static and arrival weights; recognition (the market's probability of a new world rising) and resolution (the jump when uncertainty ends). |
| `code/regimes_demo.py` | Stylised illustration: what waking up to a higher- or lower-rate world looks like on the curve. |
| `code/sovereign.py` | The anchor-failure state: a government curve as the common curve plus a sovereign spread (average expected loss plus convenience); fiscal regimes via `regimes.py`. |
| `code/sovereign_monitor.py` | Public sovereign spreads over Germany, 2019–2026 (euro area as the pure sovereign part), and Sweden 1994 at 5Y and 10Y. |
| `code/se_1990s.py` | Sweden 1990–95 from the Riksbank's public API: the 1992 defence, the float, the 1994 fiscal crash, speed against today. |
| `code/macro.py` | The macro block: the paper's Appendix B (SSRN version) along a technology clock, calibrated to public targets, with bridges to the curve layer (nominal, fiscal, neutral rate, policy, premia); produced capital at Appendix A.4's user cost, so rates feed back into automation. |
| `code/macro_scenarios.py` | Deep automation at three speeds, run through to curves; with capital split out (b), who is paid, what a sustained rate shock does, and the loop between rates and automation. |
| `code/recognition.py` | The recognition clock as a mixture: two worlds, Bayesian learning from noisy labour-share data (plus narrative shocks), the market curve as the probability-weighted mix, a common policy rate; and the market's speed — capacity growing with trust in AI, a shared model error, digestion. |
| `code/recognition_scenarios.py` | When the market wakes up, what the curve does, the jump still waiting, and a false dawn. |
| `code/speed_scenarios.py` | Markets at machine speed: capacity (recognition earlier), digestion (news gaps; the front waits for policy meetings), and a shared error that fools an unaware market. |
| `code/digestion_history.py` | Has digestion speed changed before? Variance ratios of US Treasury yield changes 1962–2026 by era, and the partial-digestion fit behind the speed ladder. |
| `code/regime_digestion.py` | How slowly are regime judgements digested? Coibion–Gorodnichenko tests on survey (SPF) and market (Gürkaynak–Sack–Wright, net of Kim–Wright) forecasts, the long-run anchors, and the model's catch-up when AI is adopted. |
| `code/bank.py` | A stylised bank on the paths (illustrative balance sheet, not any bank's): deposits that migrate and catch up, mortgage margins that lag, reserves, a securities ladder, house prices as capitalised site rent, wage-earning borrowers, commercial property. |
| `code/bank_scenarios.py` | The bank on four paths — status quo, a pure tightening, and the paper's world with real rates rising or falling: where NII comes from, houses against wages, borrowers, commercial property, NII less credit losses. |
| `code/floor_margins.py` | What Swedish banks did at the floor and on the way up: mortgage margins below zero, deposit rates floored at zero, deposit pass-through up against down, the 2022-23 margin squeeze (Statistics Sweden, Riksbank). |
| `code/deposits_wages.py` | Do Swedish household deposits follow wages? Deposit growth against wage and income growth, deposits against saving, the wage share and the cost of holding them; the share of non-wage income households receive (Statistics Sweden, Riksbank). |
| `code/demand.py` | A demand gap for the macro block: output, unemployment and inflation when the central bank learns the neutral rate with a lag or meets the floor; Okun and Phillips slopes measured on Swedish data (Statistics Sweden). |
| `code/households.py` | Who carries the people who leave work — the state (today's Swedish support) or family and friends (a lean state, networks with finite capacity), their savings — and borrowers' debt service on fixed money debts, fed into the demand layer; emergency checks; rigid money wages. Swedish household debt, fixation and margins from Statistics Sweden. |
| `code/global_crash.py` | Could an AI bust become a Great Depression, worldwide? Four regions (US, euro area, Sweden, China) with recessions triggering adoption, bank capital and spreads, trade, and rules that change under pressure; validated on US 1929-33 and 2008-10 with one parameter set (FRED, BIS). Optionally two waves: cognitive work exposed now, physical work once robotics arrives (`exposure.py`), and care as the absorber within its pace, who moves into it, and what pays for it (taxes on labour, borrowing at the measured price of debt, or a levy on AI income); a participation margin (the displaced leaving the labour force, measured for the US) and the US build-out measured (`decoupling.py`). |
| `code/exposure.py` | Who is exposed to which wave: employment by occupation group (cognitive ISCO 1-4, in-person 5, physical 6-9) in the four regions, each group's pay against the average, and how each moved in the 2008-10 recession; for care as the absorber, its share, pace, the ceiling (the largest share any rich economy employs) and who moves into it (ILOSTAT). |
| `code/baumol.py` | Where the jobs are going: net job growth by sector and sex (US payrolls monthly, labour force surveys for the US, Sweden and five euro-area countries, China), care in recessions, Baumol's premise in US prices and spending, what care pays and who pays for it (BLS, BEA via FRED; ILOSTAT). |
| `code/financing.py` | Is the most care a society employs set by need or by financing? Care's share of jobs across OECD economies against public long-term care and health spending, income and age; Norway's fund transfers against its public health and care bill; long-term borrowing rates against net public debt; taxes on labour income by region (OECD health accounts, Economic Outlook and Revenue Statistics, ILOSTAT, World Bank, Statistics Norway). |
| `code/decoupling.py` | Output rising while work does not: US output against hours, labour's share against its history since 1947, GDPNow and its track record, manufacturing output by industry against jobs, the AI build-out net of computer imports, and where the displaced go (unemployment or out of the labour force) (FRED: BLS, BEA, Federal Reserve, Atlanta Fed). |
| `code/export_paths.py` | The paths as a plain table for anyone to put their own book on: per scenario and quarter, the policy rate, zero rates 3M-10Y, the real wage bill, for a credit book the real wage, employment, the real site rent and site price, and the price level, and for a deposit book real income and the labour share (`results/paths_for_banks.csv`); apply the changes to your own curve. |
| `code/reverse.py` | Reverse stress testing, part 1: the model's dials (technology path, bridges, capital premium, learning) over broad stated ranges; the run; rank correlations; the most plausible draw reaching a threshold. |
| `code/reverse_envelope.py` | 4,000 Latin-hypercube draws: the envelope of curve and macro outcomes, what drives them, the most plausible routes to a ±100 bp 10Y move. |
| `code/cycle.py` | A rate cycle driven through the three clocks: a lagged, stepwise central bank and a market that learns. |
| `code/us_modes.py` | The public test: phases of the Fed's 2021–23 cycle and the last twelve months on FRED Treasury yields. |
| `checks/check_curve.py`, `checks/check_regimes.py`, `checks/check_sovereign.py`, `checks/check_macro.py`, `checks/check_recognition.py`, `checks/check_reverse.py`, `checks/check_speed.py`, `checks/check_regime_digestion.py`, `checks/check_bank.py`, `checks/check_floor_margins.py`, `checks/check_deposits_wages.py`, `checks/check_demand.py`, `checks/check_households.py`, `checks/check_global_crash.py`, `checks/check_exposure.py`, `checks/check_financing.py`, `checks/check_decoupling.py` | The batteries: sympy identities, the code against the algebra, the stylised cycle, the regime mixtures, the sovereign spread, the macro block (gated on the paper's published Appendix B figures), recognition, the reverse stress machinery, speed, the digestion estimators and the forward-rate test, the stylised bank. They gate everything. |
| `results/`, `figures/` | Outputs of `code/`. |
| `cache/` | The data vintages behind every number: FRED (pulled by `pinning/code/lambda_compute2.pull_fred`); under `cache/riksbank/`, the Riksbank's SWEA API; under `cache/fed/`, a trimmed vintage of the Fed Board's Gürkaynak–Sack–Wright curve; under `cache/spf/`, the Philadelphia Fed's survey files; under `cache/scb/`, Statistics Sweden's interest-rate tables; under `cache/ilo/`, ILOSTAT's employment and earnings by occupation and industry; under `cache/oecd/`, the OECD's health accounts and Economic Outlook; under `cache/worldbank/`, World Bank indicators; under `cache/ssb_no/`, Statistics Norway's tables. |

## Running

From this folder, with the repository's venv:

```
../venv/Scripts/python.exe checks/check_curve.py
../venv/Scripts/python.exe checks/check_regimes.py
../venv/Scripts/python.exe checks/check_sovereign.py
../venv/Scripts/python.exe checks/check_macro.py
../venv/Scripts/python.exe checks/check_recognition.py
../venv/Scripts/python.exe checks/check_reverse.py
../venv/Scripts/python.exe checks/check_speed.py
../venv/Scripts/python.exe checks/check_regime_digestion.py
../venv/Scripts/python.exe checks/check_bank.py
../venv/Scripts/python.exe checks/check_floor_margins.py
../venv/Scripts/python.exe checks/check_deposits_wages.py
../venv/Scripts/python.exe checks/check_demand.py
../venv/Scripts/python.exe checks/check_households.py
../venv/Scripts/python.exe checks/check_global_crash.py
../venv/Scripts/python.exe checks/check_exposure.py
../venv/Scripts/python.exe checks/check_financing.py
../venv/Scripts/python.exe checks/check_decoupling.py
../venv/Scripts/python.exe code/us_modes.py
```
