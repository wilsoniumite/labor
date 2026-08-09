# feasibility_kappa.py — coverage ratio kappa(t) = rT / (N·P_s) for Proposition 8.
# Method and all classification choices per feasibility_empirics_spec.md (repo root);
# fetch/cache/validation machinery reused from lambda_compute2.py (same folder).
# All FRED IDs verified by page title on 2026-08-05.
#
# Numerator rT — aggregate site-rent flow, two families x variants:
#   z1_hh:   (HH+NPO real estate at market value) - (HH residential structures,
#            current cost) = household land residual, x cap-rate variants.
#   z1_econ: adds NFC + NNB real estate minus their residential + nonresidential
#            structures — economy-wide residual; NFC structures end 2020, so this
#            member stops there. Z.1 land residuals carry the known post-1995
#            reliability caveat; both are LOWER bounds (financial/government/farm
#            land omitted).
#   flow_housing: PCE housing services x land-share-of-housing variants — a flow-
#            side lower bound (non-housing site rent omitted entirely).
# Denominator N·P_s — NIPA population x subsistence-bundle cost:
#   P_s = Orshansky 1963 base x CPI(t)/CPI(1963) — the Census thresholds ARE
#   CPI-updated fixed baskets, so the base constants are methodological
#   parameters (like GRID shares in lambda_compute2), not pulled data. Both
#   variants validated against published 2023 thresholds before use.

# %% imports
import os
import sys
import itertools

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lambda_compute2 import pull_fred, annualize  # cache/, retries, courtesy delays

# concept -> (ordered candidate IDs, unit divisor to $B [pop stays thousands])
CANDIDATES = {
    "re_hh":          (["HNOREMV"], 1e3),               # HH+NPO real estate, $M, Q
    "re_nfc":         (["BOGZ1LM105035005A"], 1e3),     # NFC real estate, $M, A
    "re_nnb":         (["BOGZ1LM115035005A"], 1e3),     # NNB real estate, $M, A
    "str_hh_res":     (["BOGZ1LM155012665Q"], 1e3),     # HH residential structures, $M
    "str_nfc_res":    (["BOGZ1LM105012665Q"], 1e3),     # ends 2020
    "str_nfc_nonres": (["BOGZ1LM105013665A"], 1e3),     # ends 2020
    "str_nnb_res":    (["BOGZ1LM115012665Q"], 1e3),
    "str_nnb_nonres": (["BOGZ1LM115013665A"], 1e3),
    "pce_housing":    (["DHSGRC1A027NBEA"], 1.0),       # PCE services: housing, $B
    "gs10":           (["GS10"], 1.0),                  # %, monthly
    "pop":            (["B230RC0A052NBEA", "POPTHM"], 1.0),  # thousands
    "cpi":            (["CPIAUCSL"], 1.0),
}

# loose anchors AFTER unit normalization ($B; % ; thousands; index), anchor 2023;
# stale series checked at their last year with the widened band (as in lambda_compute2)
SANITY = {
    "re_hh": (40000, 60000), "re_nfc": (10000, 22000), "re_nnb": (10000, 22000),
    "str_hh_res": (22000, 34000), "str_nfc_res": (120, 550),
    "str_nfc_nonres": (6000, 14000), "str_nnb_res": (3500, 7500),
    "str_nnb_nonres": (2000, 4800), "pce_housing": (2400, 3300),
    "gs10": (3.0, 5.0), "pop": (328000, 342000), "cpi": (295, 315),
}
ANCHOR = 2023

# %% grid — labeled classification choices (see spec)
GRID_RENT = [
    ("z1_hh_gs10",    "z1_hh",   "gs10"),
    ("z1_hh_gs10p",   "z1_hh",   "gs10p150"),
    ("z1_econ_gs10",  "z1_econ", "gs10"),
    ("z1_econ_gs10p", "z1_econ", "gs10p150"),
    ("flow_ls30",     "flow",    0.30),
    ("flow_ls50",     "flow",    0.50),
]
# Orshansky 1963 bases (1963 dollars): family-of-four 3128 (per capita 782),
# single person 1540. CPI-updated; validated against 2023 published thresholds.
GRID_BUNDLE = [("pc4", 782.0), ("single", 1540.0)]
PS_ANCHOR_2023 = {"pc4": (6800, 8600), "single": (13500, 17000)}
CPI_BASE_YEAR = 1963


def fetch_all():
    data, ledger = {}, []
    for concept, (sids, div) in CANDIDATES.items():
        got = None
        for sid in sids:
            s = pull_fred(sid)
            if s is None:
                ledger.append((concept, sid, "FAIL: no series")); continue
            a = annualize(s) / div
            last = int(a.index.max())
            chk = min(ANCHOR, last)
            lo, hi = SANITY[concept]
            if chk < ANCHOR:
                lo, hi = lo * 0.6, hi * 1.1
            v = float(a.loc[chk])
            if not (lo <= v <= hi):
                ledger.append((concept, sid,
                               f"FAIL sanity: {chk}={v:,.0f} not in [{lo:,.0f},{hi:,.0f}]")); continue
            ledger.append((concept, sid, f"OK {chk}={v:,.1f} last={last}"
                           + ("  [STALE]" if last < ANCHOR else "")))
            got = a
            break
        data[concept] = got
    return data, ledger


def land_series(data, scope):
    """Z.1 land residual by scope; returns annual $B series on the years where
    every needed input exists. Never extrapolates."""
    if scope == "z1_hh":
        need = ["re_hh", "str_hh_res"]
        pos = lambda y: y["re_hh"] - y["str_hh_res"]
    else:  # z1_econ
        need = ["re_hh", "re_nfc", "re_nnb", "str_hh_res", "str_nfc_res",
                "str_nfc_nonres", "str_nnb_res", "str_nnb_nonres"]
        pos = lambda y: (y["re_hh"] + y["re_nfc"] + y["re_nnb"]
                         - y["str_hh_res"] - y["str_nfc_res"] - y["str_nfc_nonres"]
                         - y["str_nnb_res"] - y["str_nnb_nonres"])
    if any(data[c] is None for c in need):
        return None
    years = None
    for c in need:
        yy = set(data[c].index)
        years = yy if years is None else years & yy
    out = {}
    for yr in sorted(years):
        v = pos({c: float(data[c].loc[yr]) for c in need})
        if v > 0:                                  # identity check: residual must be positive
            out[yr] = v
    return pd.Series(out)


# %% run
if __name__ == "__main__":
    data, ledger = fetch_all()
    print("\n=== validation ledger ===")
    for c, sid, msg in ledger:
        print(f"{c:15s} {sid:20s} {msg}")

    core = ["re_hh", "str_hh_res", "pce_housing", "gs10", "pop", "cpi"]
    missing = [c for c in core if data.get(c) is None]
    if missing:
        print(f"\nBLOCKED: {missing} unavailable — stopping rather than approximating.")
        raise SystemExit(1)

    land = {"z1_hh": land_series(data, "z1_hh"), "z1_econ": land_series(data, "z1_econ")}
    for scope, s in land.items():
        if s is not None:
            v23 = s.loc[min(2023, int(s.index.max()))]
            print(f"{scope}: land residual positive on {int(s.index.min())}–{int(s.index.max())}, "
                  f"latest-anchor value {v23:,.0f} $B")
    lo, hi = (12000, 32000)
    if land["z1_hh"] is not None and not lo <= float(land["z1_hh"].loc[2023]) <= hi:
        print("BLOCKED: household land residual fails its anchor — stopping.")
        raise SystemExit(1)

    cpi, pop = data["cpi"], data["pop"]
    cpi0 = float(cpi.loc[CPI_BASE_YEAR]) if CPI_BASE_YEAR in cpi.index else None
    if cpi0 is None:
        print("BLOCKED: CPI base year missing."); raise SystemExit(1)

    # validate bundle variants against published 2023 thresholds; drop failures
    bundles = []
    for name, base in GRID_BUNDLE:
        ps23 = base * float(cpi.loc[2023]) / cpi0
        lo, hi = PS_ANCHOR_2023[name]
        if lo <= ps23 <= hi:
            bundles.append((name, base))
            print(f"bundle {name}: P_s(2023) = ${ps23:,.0f}  [anchor OK]")
        else:
            print(f"bundle {name}: P_s(2023) = ${ps23:,.0f} outside [{lo},{hi}] — DROPPED")
    if not bundles:
        print("BLOCKED: no bundle variant validates."); raise SystemExit(1)

    rows = []
    years = sorted(set(int(y) for y in data["gs10"].index)
                   & set(int(y) for y in pop.index) & set(int(y) for y in cpi.index))
    for yr in years:
        members = {}
        g10 = float(data["gs10"].loc[yr])
        for label, source, rate in GRID_RENT:
            if source in ("z1_hh", "z1_econ"):
                s = land[source]
                if s is None or yr not in s.index:
                    continue
                cap = g10 + (1.5 if rate == "gs10p150" else 0.0)
                rT = float(s.loc[yr]) * cap / 100.0
            else:
                if yr not in data["pce_housing"].index:
                    continue
                rT = float(data["pce_housing"].loc[yr]) * rate
            for bname, base in bundles:
                ps = base * float(cpi.loc[yr]) / cpi0
                nps = float(pop.loc[yr]) * ps / 1e6          # $B
                members[f"k_{label}_{bname}"] = rT / nps
        if len(members) >= 4:
            vals = list(members.values())
            rows.append({"year": yr, "kappa_min": min(vals),
                         "kappa_med": float(np.median(vals)),
                         "kappa_max": max(vals), **members})

    res = pd.DataFrame(rows).set_index("year")
    os.makedirs("data", exist_ok=True)
    res.to_csv("data/kappa_results.csv")
    snap_years = [y for y in (1955, 1965, 1975, 1985, 1995, 2005, 2015, res.index.max())
                  if y in res.index]
    print("\n=== kappa snapshots (min / med / max across the grid) ===")
    print(res.loc[snap_years, ["kappa_min", "kappa_med", "kappa_max"]].round(3).to_string())
    last = int(res.index.max())
    print(f"\n§7 row candidate — coverage ratio of the rent-funded floor, κ ({last}): "
          f"{res.loc[last, 'kappa_med']:.2f} [{res.loc[last, 'kappa_min']:.2f}–"
          f"{res.loc[last, 'kappa_max']:.2f}]")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.fill_between(res.index, res["kappa_min"], res["kappa_max"], alpha=0.25,
                    label="κ band across source/cap-rate/bundle grid")
    ax.plot(res.index, res["kappa_med"], lw=2, label="κ median rule set")
    ax.axhline(1.0, color="k", lw=1, ls=":", label="κ = 1 (floor fully funded)")
    ax.set_ylabel("coverage ratio κ = rT / (N·P_s)")
    ax.set_title("Feasibility of the rent-funded floor: coverage ratio κ, U.S., "
                 "band across classification rules")
    ax.legend(loc="upper left", fontsize=8, framealpha=1.0)
    fig.tight_layout()
    os.makedirs("figures", exist_ok=True)
    fig.savefig("figures/kappa_coverage.png", dpi=150)
    print("\nwrote data/kappa_results.csv and figures/kappa_coverage.png")
