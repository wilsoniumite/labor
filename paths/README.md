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
| `code/recognition.py` | The recognition clock as a mixture: two worlds, Bayesian learning from noisy labour-share data (plus narrative shocks), the market curve as the probability-weighted mix, a common policy rate. |
| `code/recognition_scenarios.py` | When the market wakes up, what the curve does, the jump still waiting, and a false dawn. |
| `code/reverse.py` | Reverse stress testing, part 1: the model's dials (technology path, bridges, capital premium, learning) over broad stated ranges; the run; rank correlations; the most plausible draw reaching a threshold. |
| `code/reverse_envelope.py` | 4,000 Latin-hypercube draws: the envelope of curve and macro outcomes, what drives them, the most plausible routes to a ±100 bp 10Y move. |
| `code/cycle.py` | A rate cycle driven through the three clocks: a lagged, stepwise central bank and a market that learns. |
| `code/us_modes.py` | The public test: phases of the Fed's 2021–23 cycle and the last twelve months on FRED Treasury yields. |
| `checks/check_curve.py`, `checks/check_regimes.py`, `checks/check_sovereign.py`, `checks/check_macro.py`, `checks/check_recognition.py`, `checks/check_reverse.py` | The batteries: sympy identities, the code against the algebra, the stylised cycle, the regime mixtures, the sovereign spread, the macro block (gated on the paper's published Appendix B figures), recognition, the reverse stress machinery. They gate everything. |
| `results/`, `figures/` | Outputs of `code/`. |
| `cache/` | The data vintages behind every number: FRED (pulled by `pinning/code/lambda_compute2.pull_fred`) and, under `cache/riksbank/`, the Riksbank's SWEA API. |

## Running

From this folder, with the repository's venv:

```
../venv/Scripts/python.exe checks/check_curve.py
../venv/Scripts/python.exe checks/check_regimes.py
../venv/Scripts/python.exe checks/check_sovereign.py
../venv/Scripts/python.exe checks/check_macro.py
../venv/Scripts/python.exe checks/check_recognition.py
../venv/Scripts/python.exe checks/check_reverse.py
../venv/Scripts/python.exe code/us_modes.py
```
