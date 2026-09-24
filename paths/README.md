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
| `code/cycle.py` | A rate cycle driven through the three clocks: a lagged, stepwise central bank and a market that learns. |
| `code/us_modes.py` | The public test: phases of the Fed's 2021–23 cycle and the last twelve months on FRED Treasury yields. |
| `checks/check_curve.py` | The battery: sympy identities, the code against the algebra, the stylised cycle. Gates everything. |
| `results/`, `figures/` | Outputs of `code/`. |
| `cache/` | The FRED vintage behind every number (pulled by `pinning/code/lambda_compute2.pull_fred`). |

## Running

From this folder, with the repository's venv:

```
../venv/Scripts/python.exe checks/check_curve.py
../venv/Scripts/python.exe code/us_modes.py
```
