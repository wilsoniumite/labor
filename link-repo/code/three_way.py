# three_way.py — of consumption NOT directly financed by ownership income:
# shares from (a) direct wages, (b) transfers funded by taxes on wages, (c) transfers funded by taxes on ownership.
# Reuses the cached FRED pulls and rule grid from lambda_compute2.

# %% imports
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from lambda_compute2 import pull_fred, annualize, tax_linkages, GRID, R_KEYS, CANDIDATES

def load_all():
    out = {}
    for concept, sids in CANDIDATES.items():
        s = None
        for sid in sids:
            s = pull_fred(sid)
            if s is not None:
                out[concept] = annualize(s); break
    return out

def solve_shares(y, rules):
    """returns (direct_wage, transfer_wagetax, transfer_ownertax) shares of non-ownership-financed consumption."""
    pls, tilt = rules["prop_labor_share"], rules["cap_tax_tilt"]
    W_pre = y["wages"] + y["supplements"] + pls * y["proprietors"]
    K_pre = (1 - pls) * y["proprietors"] + y["rental"] + y["interest"] + y["dividends"]
    wts = W_pre / (W_pre + tilt * K_pre)
    W_net = W_pre - y["contribs"] - y["ptax"] * wts
    K_net = K_pre - y["ptax"] * (1 - wts)
    T, C = y["soc_benefits"], y["pce"]

    x, lam_T = 0.8, 0.7
    for _ in range(200):
        lamR_all, lam_nonpay, ok = tax_linkages(x, y, rules)
        if rules["transfer_funding"] == "earmarked" and ok:
            ear = min(y["contribs"], T)
            lam_T = (ear + (T - ear) * lam_nonpay) / T
        elif ok:
            lam_T = lamR_all
        else:
            lam_T = x
        Wl, Ol = W_net + lam_T * T, K_net + (1 - lam_T) * T
        order = rules["financing_order"]
        if order == "proportional":
            x_new = Wl / (Wl + Ol)
        elif order == "wages_first":
            x_new = (min(Wl, C) + max(C - Wl - Ol, 0.0)) / C
        else:
            x_new = min(Wl, max(C - Ol, 0.0)) / C
        if abs(x_new - x) < 1e-12: break
        x = x_new
    denom = W_net + T          # the non-ownership-financed pool splits pro rata within itself
    return W_net / denom, lam_T * T / denom, (1 - lam_T) * T / denom

# %% run
if __name__ == "__main__":
    data = load_all()
    core = ["wages","supplements","proprietors","rental","interest","dividends",
            "soc_benefits","contribs","ptax","pce"] + R_KEYS
    missing = [c for c in core if c not in data]
    if missing:
        print(f"BLOCKED: {missing} unavailable — stopping."); raise SystemExit(1)
    years = sorted(set.intersection(*[set(data[c].index) for c in core]))
    years = [yy for yy in years if yy >= 1960]
    combos = [dict(zip(GRID, v)) for v in itertools.product(*GRID.values())]

    rows = []
    for yr in years:
        y = {c: float(data[c].loc[yr]) for c in core}
        tri = np.array([solve_shares(y, r) for r in combos])
        rows.append({"year": yr,
            "wage_direct_med": np.median(tri[:,0]), "wage_direct_min": tri[:,0].min(), "wage_direct_max": tri[:,0].max(),
            "wagetax_med":     np.median(tri[:,1]), "wagetax_min":     tri[:,1].min(), "wagetax_max":     tri[:,1].max(),
            "ownertax_med":    np.median(tri[:,2]), "ownertax_min":    tri[:,2].min(), "ownertax_max":    tri[:,2].max()})
    res = pd.DataFrame(rows).set_index("year").round(4)
    os.makedirs("data", exist_ok=True); res.to_csv("data/three_way_split.csv")
    snap = res[[c for c in res.columns if c.endswith("_med")]]
    print(snap.loc[[y for y in (1965,1985,2005,2015,res.index.max()) if y in snap.index]].to_string())
    last = res.index.max()
    r = res.loc[last]
    print(f"\n{last}: direct wages {r.wage_direct_med:.3f} [{r.wage_direct_min:.3f},{r.wage_direct_max:.3f}] | "
          f"wage-tax transfers {r.wagetax_med:.3f} [{r.wagetax_min:.3f},{r.wagetax_max:.3f}] | "
          f"owner-tax transfers {r.ownertax_med:.3f} [{r.ownertax_min:.3f},{r.ownertax_max:.3f}]")
