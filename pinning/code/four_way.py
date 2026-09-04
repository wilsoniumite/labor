# four_way.py — deficit-aware financing split of non-owner-loop consumption.
# Channels: direct wages | transfers from wage taxes | transfers from ownership taxes | transfers from borrowing.
# Borrowed dollars sized by the government current-account gap (GEXPND - GRECPT), attributed to
# transfers under three labeled rules (new grid axis): protected / prorata / marginal.

# %% imports
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from lambda_compute2 import pull_fred, annualize, tax_linkages, GRID as BASE_GRID, R_KEYS, CANDIDATES

EXTRA = {"grecpt": ["GRECPT"], "gexpnd": ["GEXPND"]}
SANE_2023 = {"grecpt": (6200, 8600), "gexpnd": (8200, 10600)}

GRID = dict(BASE_GRID)
GRID["deficit_attribution"] = ["protected", "prorata", "marginal"]

def load_all():
    out = {}
    for concept, sids in {**CANDIDATES, **EXTRA}.items():
        for sid in sids:
            s = pull_fred(sid)
            if s is not None:
                out[concept] = annualize(s); break
    return out

def solve_four(y, rules):
    """returns shares of the non-ownership-financed pool: (direct_wage, wagetax, ownertax, borrowed)."""
    pls, tilt = rules["prop_labor_share"], rules["cap_tax_tilt"]
    W_pre = y["wages"] + y["supplements"] + pls * y["proprietors"]
    K_pre = (1 - pls) * y["proprietors"] + y["rental"] + y["interest"] + y["dividends"]
    wts = W_pre / (W_pre + tilt * K_pre)
    W_net = W_pre - y["contribs"] - y["ptax"] * wts
    K_net = K_pre - y["ptax"] * (1 - wts)
    T, C = y["soc_benefits"], y["pce"]

    deficit = max(y["gexpnd"] - y["grecpt"], 0.0)
    att = rules["deficit_attribution"]
    if att == "prorata":
        T_bor = deficit * T / y["gexpnd"]
    elif att == "marginal":
        T_bor = min(deficit, T)
    else:  # protected: borrowing hits all other outlays before touching transfers
        T_bor = max(deficit - (y["gexpnd"] - T), 0.0)
    T_tax = T - T_bor

    x, lam_T = 0.8, 0.7
    for _ in range(200):
        lamR_all, lam_nonpay, ok = tax_linkages(x, y, rules)
        if rules["transfer_funding"] == "earmarked" and ok:
            ear = min(y["contribs"], T_tax)
            lam_T = (ear + (T_tax - ear) * lam_nonpay) / T_tax if T_tax > 0 else 0.0
        elif ok:
            lam_T = lamR_all
        else:
            lam_T = x
        # sales-tax linkage tracks the wage-financed share of consumption; borrowed- and
        # owner-financed consumption both contribute zero (second-order splits ignored)
        Wl = W_net + lam_T * T_tax
        Ol = K_net + (1 - lam_T) * T_tax + T_bor
        x_new = Wl / (Wl + Ol)
        if abs(x_new - x) < 1e-12: break
        x = x_new
    denom = W_net + T
    return (W_net / denom, lam_T * T_tax / denom, (1 - lam_T) * T_tax / denom, T_bor / denom)

# %% run
if __name__ == "__main__":
    data = load_all()
    need = ["wages","supplements","proprietors","rental","interest","dividends",
            "soc_benefits","contribs","ptax","pce","grecpt","gexpnd"] + R_KEYS
    missing = [c for c in need if c not in data]
    if missing:
        print(f"BLOCKED: {missing} unavailable — stopping."); raise SystemExit(1)
    for c, (lo, hi) in SANE_2023.items():
        v = float(data[c].loc[2023])
        print(f"sanity {c} 2023 = {v:.0f} plausible={lo <= v <= hi}")
        assert lo <= v <= hi, f"{c} implausible — refusing to proceed"

    years = sorted(set.intersection(*[set(data[c].index) for c in need]))
    years = [yy for yy in years if yy >= 1960]
    combos = [dict(zip(GRID, v)) for v in itertools.product(*GRID.values())]

    rows = []
    for yr in years:
        y = {c: float(data[c].loc[yr]) for c in need}
        q = np.array([solve_four(y, r) for r in combos])
        med, mn, mx = np.median(q, 0), q.min(0), q.max(0)
        rows.append({"year": yr,
            "wage_direct_med": med[0], "wagetax_med": med[1], "ownertax_med": med[2], "borrowed_med": med[3],
            "wage_direct_min": mn[0], "wagetax_min": mn[1], "ownertax_min": mn[2], "borrowed_min": mn[3],
            "wage_direct_max": mx[0], "wagetax_max": mx[1], "ownertax_max": mx[2], "borrowed_max": mx[3]})
    res = pd.DataFrame(rows).set_index("year").round(4)
    os.makedirs("data", exist_ok=True); res.to_csv("data/four_way_split.csv")
    m = (res[["wage_direct_med","wagetax_med","ownertax_med","borrowed_med"]] * 100).round(1)
    print(m.loc[[y for y in (1965,1975,1985,1995,1999,2005,2009,2015,2019,2021,res.index.max()) if y in m.index]].to_string())
    last = res.index.max(); r = res.loc[last]
    print(f"\n{last}: borrowed {r.borrowed_med:.3f} [{r.borrowed_min:.3f},{r.borrowed_max:.3f}] | "
          f"ownertax {r.ownertax_med:.3f} [{r.ownertax_min:.3f},{r.ownertax_max:.3f}]")
