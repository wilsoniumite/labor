# check_exposure.py — code/exposure.py and its stored results (data/exposure_deciles.csv, data/exposure_groups.csv).
#   R  the stored files are what the script computes
#   S  the shares held of each claim add to one in every year
#   U  the accounts add up: everyone together is exposed by about nothing, every year (three sources meet: the
#      input-output tables, BEA's distribution of personal income, corporate income from the national accounts)
#   W  the pattern does not turn on the judgments: proprietors' labour at 0, 0.38 and 0.67, the tax-base share at its
#      band's ends, with and without the corporate income households do not receive
#   Q  the numbers SKETCH.md and the draft quote
# Reads only files in the repository. Run from provisioning/:  python3 checks/check_exposure.py
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import exposure as ex  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def prints(value, printed, decimals):
    return abs(value - printed) <= 0.5 * 10.0 ** (-decimals) * 1.05


def rows(pairs):
    return all(prints(v, q, d) for v, q, d in pairs), "; ".join(f"{v:.4f} for {q}" for v, q, d in pairs)


tabs = ex.inputs()
dec, grp = ex.tables(tabs)
sd = pd.read_csv(os.path.join(ROOT, "data", "exposure_deciles.csv"))
sg = pd.read_csv(os.path.join(ROOT, "data", "exposure_groups.csv"))
num = lambda d: [c for c in d.columns if d[c].dtype.kind == "f"]   # noqa: E731
gap = max(float(np.max(np.abs(dec[num(dec)].values - sd[num(sd)].values))), float(np.max(np.abs(grp[num(grp)].values - sg[num(sg)].values))))
check("R1 the stored tables are what the script computes (1e-12)", gap < 1e-12, f"{gap:.1e}")

held = dec.groupby("year")[["share_of_labour_income", "share_of_capital_and_land", "share_of_transfers", "share_of_consumption"]].sum()
check("S1 the shares held of labour income, capital and land, transfers and consumption each add to one, every year (1e-9)",
      float((held - 1).abs().max().max()) < 1e-9, f"{float((held - 1).abs().max().max()):.1e}")

g = grp.set_index(["group", "year"])["exposure"].unstack(0)
e = g["everyone"]
check("U1 everyone together is exposed by less than 0.03 in every year, 2004-2023, and by 0.011 on average",
      e.abs().max() < 0.03 and prints(e.mean(), 0.011, 3), f"mean {e.mean():+.3f}, from {e.min():+.3f} to {e.max():+.3f}")

# ---- W. the judgments
signs, spans = [], {"bottom half": [], "next four tenths": [], "top tenth": []}
for psi in (0.0, 0.38, 0.67):
    for tau_col in ("lamR_min", "lamR_med", "lamR_max"):
        made_col = f"labour_factor_psi{int(round(100 * psi)):02d}"
        t2 = dict(tabs, made=tabs["made"].assign(labour_factor_psi38=tabs["made"][made_col]))   # the same judgment on both sides
        _, gv = ex.tables(t2, psi=psi, tau_col=tau_col)
        x = gv.set_index(["group", "year"])["exposure"].unstack(0)
        signs.append(bool((x["bottom half"] > 0).all() and (x["next four tenths"] > 0).all() and (x["top tenth"] < 0).all()))
        for k in spans:
            spans[k].append(float(x.loc[2023, k]))
check("W1 in all nine combinations of proprietors' labour (0, 0.38, 0.67) and the tax-base share (its band's ends and middle) the "
      "bottom nine tenths are long labour and the top tenth short, every year", all(signs),
      "; ".join(f"{k} in 2023: {min(v):+.3f} to {max(v):+.3f}" for k, v in spans.items()))
a = ex.amounts(tabs, 2023)
m_recv, _ = ex.measures(a.assign(accrued=0.0), float(tabs["tax"].loc[2023, "lamR_med"]), float(tabs["made"].loc[2023, "labour_factor_psi38"]))
check("W2 without the corporate income households do not receive, every decile looks more dependent on labour: the top tenth "
      "0.578 of income where the full account has 0.516",
      *rows([(float(m_recv.loc["90-100%", "labour_of_income"]), 0.578, 3),
             (float(dec[(dec.year == 2023) & (dec.decile == "90-100%")]["labour_of_income"].iloc[0]), 0.516, 3)]))

# ---- Q
q = sg[sg.year == 2023].set_index("group")
check("Q1 2023, labour's share of income: bottom half 0.758, next four tenths 0.773, top tenth 0.516, everyone 0.666; against "
      "0.658 of what consumption buys",
      *rows([(q.loc["bottom half", "labour_of_income"], 0.758, 3), (q.loc["next four tenths", "labour_of_income"], 0.773, 3),
             (q.loc["top tenth", "labour_of_income"], 0.516, 3), (q.loc["everyone", "labour_of_income"], 0.666, 3),
             (q.loc["everyone", "made_by_labour"], 0.658, 3)]))
check("Q2 2023, exposure: bottom half +0.100, next four tenths +0.115, top tenth -0.142",
      *rows([(q.loc["bottom half", "exposure"], 0.100, 3), (q.loc["next four tenths", "exposure"], 0.115, 3),
             (q.loc["top tenth", "exposure"], -0.142, 3)]))
check("Q3 2023, who holds what: the top tenth 0.355 of labour income, 0.672 of capital and land, 0.092 of transfers, 0.202 of "
      "consumption; the bottom half 0.177, 0.083, 0.507, 0.350",
      *rows([(q.loc["top tenth", k], v, 3) for k, v in (("share_of_labour_income", 0.355), ("share_of_capital_and_land", 0.672),
                                                         ("share_of_transfers", 0.092), ("share_of_consumption", 0.202))]
            + [(q.loc["bottom half", k], v, 3) for k, v in (("share_of_labour_income", 0.177), ("share_of_capital_and_land", 0.083),
                                                             ("share_of_transfers", 0.507), ("share_of_consumption", 0.350))]))
q4 = sg[sg.year == 2004].set_index("group")
check("Q4 2004 for comparison: exposure +0.090, +0.093 and -0.125; the top tenth held 0.620 of capital and land",
      *rows([(q4.loc["bottom half", "exposure"], 0.090, 3), (q4.loc["next four tenths", "exposure"], 0.093, 3),
             (q4.loc["top tenth", "exposure"], -0.125, 3), (q4.loc["top tenth", "share_of_capital_and_land"], 0.620, 3)]))
d23 = sd[sd.year == 2023].set_index("decile")
mid = d23.loc[ex.DECILES[1:9]]
lo_m, hi_m = mid.labour_of_market_income.min(), mid.labour_of_market_income.max()
lo_i, hi_i = mid.labour_of_income.min(), mid.labour_of_income.max()
bt = d23.loc["0-10%", "transfers_of_income"]
check("Q5 2023, deciles two to nine: labour is 0.81 to 0.83 of market income and 0.75 to 0.78 of income with transfers and "
      "accrued corporate income; the bottom tenth takes 0.58 of its income in transfers",
      *rows([(lo_m, 0.81, 2), (hi_m, 0.83, 2), (lo_i, 0.75, 2), (hi_i, 0.78, 2), (bt, 0.58, 2)]))
b = {s: ex.basket(tabs, 2023, s) for s in (0.0, 0.30, 0.40)}
avg = ex.basket(tabs, 2023, float(tabs["made"].loc[2023, "shelter_share"]))
check("Q6 2023, the basket: labour is 0.740 of the factor cost of consumption without shelter, 0.658 of the average basket, "
      "0.582 with shelter at 30% of spending and 0.531 at 40%; a household on wages alone is exposed by 0.34, 0.42 and 0.47",
      *rows([(b[0.0], 0.740, 3), (avg, 0.658, 3), (b[0.30], 0.582, 3), (b[0.40], 0.531, 3), (1 - avg, 0.34, 2), (1 - b[0.30], 0.42, 2),
             (1 - b[0.40], 0.47, 2)]))

held, s_now = ex.market_shares(tabs, 2023)
bh, nf, tt = held["bottom half"], held["next four tenths"], held["top tenth"]
check("Q7 2023, shares of market income (labour is paid 0.664 of it): bottom half 0.145, next four tenths 0.393, top tenth 0.462; "
      "with labour paid 0.17 at today's holdings 0.099, 0.283 and 0.618; with labour paid nothing 0.083, 0.245 and 0.672",
      *rows([(s_now, 0.664, 3), (ex.income_share(bh, s_now), 0.145, 3), (ex.income_share(nf, s_now), 0.393, 3),
             (ex.income_share(tt, s_now), 0.462, 3), (ex.income_share(bh, 0.17), 0.099, 3), (ex.income_share(nf, 0.17), 0.283, 3),
             (ex.income_share(tt, 0.17), 0.618, 3), (ex.income_share(bh, 0.0), 0.083, 3), (ex.income_share(nf, 0.0), 0.245, 3),
             (ex.income_share(tt, 0.0), 0.672, 3)]))
check("Q8 a common share of the claims on capital and land that holds the bottom half's share of market income where it is: "
      "0.13 with labour paid 0.17, 0.15 with labour paid nothing; a common fifth takes it to 0.168 and 0.166; the next four "
      "tenths would need 0.86 and 0.96",
      *rows([(ex.holding_share(bh, s_now, 0.17), 0.13, 2), (ex.holding_share(bh, s_now, 0.0), 0.15, 2),
             (ex.income_share(bh, 0.17, 0.2), 0.168, 3), (ex.income_share(bh, 0.0, 0.2), 0.166, 3),
             (ex.holding_share(nf, s_now, 0.17), 0.86, 2), (ex.holding_share(nf, s_now, 0.0), 0.96, 2)]))
check("Q8b with a fifth held in common: the next four tenths 0.309 with labour paid 0.17 and 0.276 with labour paid nothing; the "
      "top tenth 0.523 and 0.558",
      *rows([(ex.income_share(nf, 0.17, 0.2), 0.309, 3), (ex.income_share(nf, 0.0, 0.2), 0.276, 3),
             (ex.income_share(tt, 0.17, 0.2), 0.523, 3), (ex.income_share(tt, 0.0, 0.2), 0.558, 3)]))
tot = sum(ex.income_share(h, 0.3, 0.37) for h in held.values())
check("Q9 the groups' shares of market income add to one at any labour share and any common share (an identity)", abs(tot - 1) < 1e-12)
ss, s0, s1 = ex.shift_share(tabs, 2004, 2023)
exact = max(abs(r["after"] - r["before"] - r["between"] - r["within"]) for r in ss.values())
check("Q10 2004-2023, labour's share of market income 0.709 to 0.664: the top tenth's share of market income rose 4.2 points, 1.4 "
      "from payments moving between claims and 2.8 from holding more of each; the next four tenths lost 4.1 (1.0 and 3.2); the "
      "bottom half 0.1 (0.4 lost, 0.3 gained); the split is exact",
      exact < 1e-12 and rows([(s0, 0.709, 3), (s1, 0.664, 3), (100 * (ss["top tenth"]["after"] - ss["top tenth"]["before"]), 4.2, 1),
                              (100 * ss["top tenth"]["between"], 1.4, 1), (100 * ss["top tenth"]["within"], 2.8, 1),
                              (100 * (ss["next four tenths"]["after"] - ss["next four tenths"]["before"]), -4.1, 1),
                              (100 * ss["next four tenths"]["between"], -1.0, 1), (100 * ss["next four tenths"]["within"], -3.2, 1),
                              (100 * (ss["bottom half"]["after"] - ss["bottom half"]["before"]), -0.1, 1),
                              (100 * ss["bottom half"]["between"], -0.4, 1), (100 * ss["bottom half"]["within"], 0.3, 1)])[0],
      f"exact to {exact:.1e}; top tenth {100 * ss['top tenth']['between']:+.2f} and {100 * ss['top tenth']['within']:+.2f}; next four "
      f"tenths {100 * ss['next four tenths']['between']:+.2f} and {100 * ss['next four tenths']['within']:+.2f}; bottom half "
      f"{100 * ss['bottom half']['between']:+.2f} and {100 * ss['bottom half']['within']:+.2f}")

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
