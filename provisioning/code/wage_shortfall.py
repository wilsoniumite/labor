# wage_shortfall.py — where the production worker's wage fell short of its 1950-73 pace: an accounting, in logs.
#
# The wage is production and nonsupervisory hourly earnings over the CPI less shelter (shelter is counted apart, so the
# old CPI's treatment of owners' housing before 1983 stays out of the main line). Had it kept its 1950-73 pace it would
# be higher by the shortfall; the shortfall is split into pieces the repository can size:
#   output     output per hour (nonfarm business, OPHNFB) growing more slowly than in 1950-73
#   dispersion average pay pulling away from production pay (the backward model's pay_gap; only its change is read)
#   share      the nonfarm business labour share falling (PRS85006173)
#   left over  consumer against output prices, benefits, and what the three measures do not line up on
# and, read on the all-items wage, the part shelter's relative price adds. Pro-rata accounting, not incidence.
#
# NOT GATED on this branch: the wage legs and the pay gap come from the backward model's panel
# (us-record/data/panel.csv, branch claude/focused-bardeen-aciw2z, at 457e38b), which is not on this branch.
# Run:  python3 code/wage_shortfall.py PATH/TO/us-record/data/panel.csv

import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def annual(rel):
    d = pd.read_csv(os.path.join(ROOT, rel), parse_dates=["observation_date"])
    d["year"] = d["observation_date"].dt.year
    g = d.groupby("year")[d.columns[1]].agg(["mean", "count"])
    return g[g["count"] == g["count"].max()]["mean"]                  # complete years only


def rate(s, a, b):
    return np.log(s[b] / s[a]) / (b - a)


def shortfall(panel, a, b, base=(1950, 1973)):
    oph, ls = annual("paths/cache/OPHNFB.csv"), annual("paths/cache/PRS85006173.csv")
    n = b - a
    short = rate(panel["wage_exshelter"], *base) * n - np.log(panel.loc[b, "wage_exshelter"] / panel.loc[a, "wage_exshelter"])
    pieces = dict(output=(rate(oph, *base) - rate(oph, a, b)) * n,
                  dispersion=np.log(panel.loc[b, "pay_gap"] / panel.loc[a, "pay_gap"]),
                  share=-np.log(ls[b] / ls[a]))
    pieces["left_over"] = short - sum(pieces.values())
    all_items = rate(panel["real_wage_cpi"], *base) * n - np.log(panel.loc[b, "real_wage_cpi"] / panel.loc[a, "real_wage_cpi"])
    return dict(span=f"{a}-{b}", shortfall=short, **pieces, shelter=all_items - short, all_items=all_items)


if __name__ == "__main__":
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        sys.exit("give the path to us-record/data/panel.csv (see the header)")
    panel = pd.read_csv(sys.argv[1]).set_index("year")
    legs = {"durables": "wage_goods", "all but shelter": "wage_exshelter", "shelter": "wage_shelter"}
    print("the production wage over each price, % a year")
    for a, b in ((1950, 1973), (1973, 1995), (1995, 2024)):
        print(f"  {a}-{b}  " + "  ".join(f"{k} {100 * rate(panel[c], a, b):+.2f}" for k, c in legs.items())
              + f"  durables less shelter {100 * (rate(panel['wage_goods'], a, b) - rate(panel['wage_shelter'], a, b)):+.2f}")
    for a, b in ((1973, 1995), (1973, 2024)):
        r = shortfall(panel, a, b)
        s = r["shortfall"]
        print(f"\n{r['span']}: the wage over all but shelter is short of its 1950-73 pace by {s:.3f} in logs (a factor of {np.exp(s):.2f})")
        print("  " + "  ".join(f"{k} {100 * r[k] / s:.0f}%" for k in ("output", "dispersion", "share", "left_over")))
        print(f"  on the all-items wage the shortfall is {r['all_items']:.3f}; shelter's relative price is {100 * r['shelter'] / r['all_items']:.0f}% of it")
