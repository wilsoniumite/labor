# deflator_fork.py — Prediction 8 drawn: the same paycheck under two deflators.
# Real wage = AHETPI (production & nonsupervisory average hourly earnings)
# deflated by (a) CPI durables and (b) CPI shelter, both indexed 1964 = 100.
# Fetch/cache/validation machinery reused from lambda_compute2.py (same folder).
# FRED IDs verified by page title on 2026-08-05.

# %% imports
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lambda_compute2 import pull_fred


def annualize_complete(s, need=12):
    """Annual means over COMPLETE years only — a partial year (e.g. a
    June-vintage pull) must not masquerade as an annual observation."""
    g = s.groupby(s.index.year)
    a, counts = g.mean(), g.size()
    return a[counts >= need]

CANDIDATES = {
    "wage":     "AHETPI",         # avg hourly earnings, prod. & nonsup., $/hr, monthly
    "durables": "CUSR0000SAD",    # CPI durables, monthly
    "shelter":  "CUSR0000SAH1",   # CPI shelter, monthly
}
SANITY = {  # loose anchors at 2023 (annual means)
    "wage": (26, 32), "durables": (105, 140), "shelter": (350, 420),
}
ANCHOR = 2023
BASE_YEAR = 1964                  # first full AHETPI year

if __name__ == "__main__":
    data, ledger = {}, []
    for concept, sid in CANDIDATES.items():
        s = pull_fred(sid)
        if s is None:
            ledger.append((concept, sid, "FAIL: no series")); data[concept] = None; continue
        a = annualize_complete(s)
        v = float(a.loc[ANCHOR])
        lo, hi = SANITY[concept]
        if not (lo <= v <= hi):
            ledger.append((concept, sid, f"FAIL sanity: {ANCHOR}={v:.1f} not in [{lo},{hi}]"))
            data[concept] = None; continue
        ledger.append((concept, sid, f"OK {ANCHOR}={v:.1f} last={int(a.index.max())}"))
        data[concept] = a

    print("=== validation ledger ===")
    for c, sid, msg in ledger:
        print(f"{c:9s} {sid:14s} {msg}")
    if any(v is None for v in data.values()):
        print("\nBLOCKED: series unavailable — stopping rather than approximating.")
        raise SystemExit(1)

    years = sorted(set(data["wage"].index) & set(data["durables"].index)
                   & set(data["shelter"].index))
    years = [y for y in years if y >= BASE_YEAR]
    df = pd.DataFrame(index=years)
    for deflator in ("durables", "shelter"):
        real = data["wage"].loc[years] / data[deflator].loc[years]
        df[f"real_wage_{deflator}"] = 100 * real / real.loc[BASE_YEAR]
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/deflator_fork.csv")

    last = df.index.max()
    print(f"\n=== the fork, {BASE_YEAR} = 100 ===")
    snap = df.loc[[y for y in (1964, 1975, 1985, 1995, 2005, 2015, last) if y in df.index]]
    print(snap.round(1).to_string())
    ratio = df.loc[last, "real_wage_durables"] / df.loc[last, "real_wage_shelter"]
    print(f"\nfork ratio at {last}: {ratio:.2f}x — the same paycheck, two deflators")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df.index, df["real_wage_durables"], lw=2,
            label="wage deflated by durables CPI (machine-made goods)")
    ax.plot(df.index, df["real_wage_shelter"], lw=2, color="tab:red",
            label="wage deflated by shelter CPI (land-priced)")
    ax.axhline(100, color="k", lw=0.8, ls=":")
    ax.set_ylabel(f"real average hourly earnings, {BASE_YEAR} = 100")
    ax.set_title("The deflator fork: the same U.S. paycheck against gadgets and against ground")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    os.makedirs("figures", exist_ok=True)
    fig.savefig("figures/fig7_deflator_fork.png", dpi=150)
    print("\nwrote data/deflator_fork.csv and figures/fig7_deflator_fork.png")
