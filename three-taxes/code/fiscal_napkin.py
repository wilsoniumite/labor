# fiscal_napkin.py — the practical-design arithmetic for the Three Taxes thread
# (design memo 2026-09-02). Four cells: (A) live NIPA/Z.1 aggregates through
# the paper's own FRED machinery (pinning/code) (shared cache, sanity gates); (B) the VAT as a
# residual; (C) the 60/40 use-split schedule over an automation path, under two
# saving closures; (D) the LVT announcement shock: land at risk, mortgage
# collateral, phase-in and grandfathering price paths. Outputs to ../data/.
# Run from three-taxes/:  ../venv/Scripts/python.exe code/fiscal_napkin.py
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # three-taxes/
OUTER = os.path.dirname(ROOT)                     # laborformal/
LINKREPO = os.path.join(OUTER, "pinning")   # the paper folder holds the FRED machinery (was link-repo)
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
os.chdir(ROOT)
sys.path.insert(0, os.path.join(LINKREPO, "code"))
from lambda_compute2 import pull_fred, annualize                                   # noqa: E402
import lambda_compute2 as _lc; _lc.CACHE = os.path.join(ROOT, "cache"); os.makedirs(_lc.CACHE, exist_ok=True)  # this thread's own FRED cache  # noqa: E402
from feasibility_kappa import fetch_all, land_series, GRID_BUNDLE, CPI_BASE_YEAR   # noqa: E402
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------- Cell A: aggregates ----------------
data, ledger = fetch_all()                        # the paper's rT / P_s inputs, gated
land_hh = land_series(data, "z1_hh")

# extra aggregates: (FRED id, loose $B sanity band at 2023 -- a wrong-series guard only)
EXTRA = {
    "gdp":        ("GDPA",            (25000, 32000)),
    "gce":        ("GCEA",            (4000, 6000)),     # govt consumption expenditures + gross investment
    "gpdi":       ("GPDIA",           (4000, 6500)),
    "pce":        ("PCECA",           (16500, 22000)),
    "soc":        ("A063RC1A027NBEA", (3000, 5200)),     # govt social benefits to persons
    "ptax":       ("W055RC1A027NBEA", (2300, 3600)),     # personal current taxes
    "contribs":   ("A061RC1A027NBEA", (1500, 2600)),     # contributions for govt social insurance
    "wages":      ("A576RC1",         (10000, 14000)),
    "suppl":      ("A038RC1A027NBEA", (2000, 4200)),
    "cfc":        ("COFC",            (3800, 5800)),     # consumption of fixed capital, quarterly SAAR
    "corp":       ("A051RC1A027NBEA", (2600, 4400)),     # corporate profits with IVA and CCAdj
    "proptax":    ("B249RC1Q027SBEA", (600, 1100)),      # S&L property taxes, quarterly SAAR
    "fctax":      ("FCTAX",           (300, 700)),       # federal corporate tax receipts
    "mortg":      ("HHMSDODNS",       (11000, 14500)),   # HH home mortgages, liability level ($M -> $B below)
    "fed_debt":   ("GFDEBTN",         (30000, 40000)),   # federal debt, total public, $M -> $B below
    "ss":         ("W823RC1A027NBEA", (1100, 1700)),     # social security benefits
    "medicare":   ("W824RC1A027NBEA", (800, 1400)),
    "medicaid":   ("W729RC1A027NBEA", (600, 1100)),
}
A = {}
for k, (sid, (lo, hi)) in EXTRA.items():
    s = pull_fred(sid)
    if s is None:
        ledger.append((k, sid, "FAIL: no series"))
        continue
    a = annualize(s)
    if k in ("mortg", "fed_debt"):
        a = a / 1e3                               # these two series are published in $M
    last = int(a.index.max())
    chk = min(2023, last)
    v = float(a.loc[chk])
    if not (lo <= v <= hi):
        ledger.append((k, sid, f"FAIL sanity: {chk}={v:,.0f} not in [{lo},{hi}]"))
        continue
    ledger.append((k, sid, f"OK {chk}={v:,.0f} last={last}"))
    A[k] = a
print("=== FRED ledger ===")
for c, sid, msg in ledger:
    print(f"{c:15s} {sid:20s} {msg}")

# Treasury yields: latest daily observations (the bond-yield question), primary source for the US legs
print("\n=== Treasury yields, latest daily observations (FRED) ===")
for sid in ("DGS10", "DGS30"):
    s = pull_fred(sid)
    if s is not None:
        tail = s.dropna().tail(3)
        print(sid, {str(d.date()): float(x) for d, x in tail.items()},
              f"| 2021 mean {float(s[s.index.year == 2021].mean()):.2f}")

YEAR = 2025


def at(k, y=YEAR):
    a = A.get(k)
    if a is None or y not in a.index:
        return float("nan")
    return float(a.loc[y])


N = float(data["pop"].loc[YEAR]) * 1e3
cpi = data["cpi"]
Ps = {name: base * float(cpi.loc[YEAR]) / float(cpi.loc[CPI_BASE_YEAR]) for name, base in GRID_BUNDLE}
g10 = float(data["gs10"].loc[YEAR])
rT = {"z1_hh_gs10": float(land_hh.loc[YEAR]) * g10 / 100,
      "z1_hh_gs10p": float(land_hh.loc[YEAR]) * (g10 + 1.5) / 100,
      "flow_ls30": float(data["pce_housing"].loc[YEAR]) * 0.30,
      "flow_ls50": float(data["pce_housing"].loc[YEAR]) * 0.50}
rT_med = float(np.median(list(rT.values())))
Y = at("gdp")
agg = {k: at(k) for k in EXTRA}
agg.update({"N": N, "P_s_pc4": Ps["pc4"], "P_s_single": Ps["single"], "rT_median": rT_med,
            "land_hh_residual": float(land_hh.loc[YEAR]), "hh_real_estate": float(data["re_hh"].loc[YEAR]),
            "hh_structures": float(data["str_hh_res"].loc[YEAR]), "gs10": g10, "year": YEAR})
pd.Series(agg).to_csv(os.path.join(DATA, "aggregates_2025.csv"), header=["value"])
print(f"\n=== {YEAR} aggregates ($B unless noted) ===")
for k, v in agg.items():
    tail = f"   ({v / Y:.1%} of GDP)" if (k in EXTRA and not np.isnan(v)) else ""
    print(f"{k:18s} {v:>14,.1f}{tail}")
print(f"labor share (wages+supplements)/GDP = {(agg['wages'] + agg['suppl']) / Y:.3f};  "
      f"GPDI/GDP = {agg['gpdi'] / Y:.3f};  CFC/GDP = {agg['cfc'] / Y:.3f}")
fb4, fb1 = N * Ps["pc4"] / 1e9, N * Ps["single"] / 1e9
print(f"floor bill N*P_s: pc4 {fb4:,.0f} ({fb4 / Y:.1%})  single {fb1:,.0f} ({fb1 / Y:.1%})")
kap_grid = [rT[m] / (N * Ps[b] / 1e9) for m in rT for b in Ps]
print("rT members:", {k: f"{v:,.0f} ({v / Y:.1%})" for k, v in rT.items()},
      "| kappa median", round(float(np.median(kap_grid)), 3))

# ---------------- Cell B: the VAT as a residual ----------------
rows = []
for b, ps in Ps.items():
    floor = N * ps / 1e9
    for kap in (rT_med / floor, 0.5, 0.75, 1.0):
        resid = max(0.0, (1 - kap) * floor)
        for eff in (1.0, 0.6):
            base = agg["pce"] * eff
            for carry, need in (("ubi_residual", resid),
                                ("ubi_residual+G_purchases", resid + agg["gce"]),
                                ("ubi_residual+G+half_benefits", resid + agg["gce"] + 0.5 * agg["soc"])):
                t = need / base
                rows.append(dict(floor=b, kappa=round(kap, 3), base_efficiency=eff, carries=carry,
                                 need_B=round(need), vat_excl=round(t, 4), vat_incl=round(t / (1 + t), 4)))
swap = agg["ptax"] + agg["contribs"] - rT_med
for eff in (1.0, 0.6):
    t = swap / (agg["pce"] * eff)
    rows.append(dict(floor="n/a", kappa=round(rT_med / fb4, 3), base_efficiency=eff,
                     carries="swap: replace personal taxes+contributions with LVT+VAT",
                     need_B=round(swap), vat_excl=round(t, 4), vat_incl=round(t / (1 + t), 4)))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "vat_residual.csv"), index=False)
print(f"\n=== VAT residual table written ({len(rows)} rows) ===")

# ---------------- Cell C: the 60/40 use split over a path ----------------
# Shares of Y. Wages and UBI consumed; owners reinvest fraction s of after-tax non-land
# returns and consume the rest; balanced budget; LVT yields kappa x floor share; Gc public
# consumption. Identities checked in checks/check_split.py.
C_TARGET, I_TARGET, GC = 0.6, 0.4, 0.14
PATH = [(0.55, 0.33), (0.45, 0.50), (0.35, 0.75), (0.25, 1.00), (0.15, 1.26)]   # (wage share, kappa)
rows = []
for fname, u in (("pc4", fb4 / Y), ("single", fb1 / Y)):
    for s in (1.0, 0.5):
        for w, k in PATH:
            rL = k * (fb4 / Y)                      # LVT yield as a share of Y (kappa on the pc4 floor)
            pi = 1 - w - rL
            t = 1 - I_TARGET / (s * pi)             # source-tax rate that leaves exactly 0.4Y reinvested
            Gi = 0.0
            if t < 0:                               # owners cannot reach 0.4 even untaxed: the state invests the gap
                t, Gi = 0.0, I_TARGET - s * pi
            own_c = (1 - s) * (1 - t) * pi
            need = GC + Gi + u - rL - t * pi        # VAT revenue required (share of Y)
            spend = w + u + own_c
            tau = need / spend if need > 0 else 0.0
            rows.append(dict(floor=fname, reinvest_s=s, wage_share=w, kappa=k, land_share=round(rL, 4),
                             nonland_share=round(pi, 4), source_tax_rate=round(t, 4),
                             source_yield=round(t * pi, 4), public_invest_Gi=round(Gi, 4),
                             vat_incl=round(tau, 4), vat_excl=round(tau / (1 - tau), 4),
                             surplus=round(max(0.0, -need), 4),
                             consumption_pp=round(C_TARGET * Y * 1e9 / N), ubi_pp=round(u * Y * 1e9 / N)))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA, "split_schedule.csv"), index=False)
print("\n=== 60/40 schedule (pc4 floor) ===")
print(df[df.floor == "pc4"].to_string(index=False))

# ---------------- Cell D: the LVT announcement shock ----------------
land, re_, strc, m = agg["land_hh_residual"], agg["hh_real_estate"], agg["hh_structures"], agg["mortg"]
print(f"\n=== LVT shock sizing ({YEAR}) ===")
print(f"HH real estate {re_:,.0f}; structures (current cost) {strc:,.0f}; land residual {land:,.0f} "
      f"({land / re_:.0%} of real estate, {land / Y:.2f}x GDP); home mortgages {m:,.0f}")
print(f"aggregate LTV: today {m / re_:.1%};  land price -> ~0: {m / strc:.1%}")
tau_bar, gam, dlt = 0.98, 0.02, 0.05
T = 600
tt = np.arange(1, T + 1)
disc = ((1 + gam) / (1 + dlt)) ** tt
P0 = disc.sum()
shock = []
for n in (0, 5, 10, 20, 30):
    tau_t = tau_bar * np.minimum(tt / n, 1.0) if n > 0 else np.full(T, tau_bar)
    ratio = ((1 - tau_t) * disc).sum() / P0
    shock.append(dict(design=f"phase-in {n}y", price_ratio=round(ratio, 3), price_drop=round(1 - ratio, 3)))
# increment-only (grandfathering): tax only rent above the announcement-date level
kept = ((1 - tau_bar * (1 - 1 / (1 + gam) ** tt)) * disc).sum() / P0
shock.append(dict(design="increment-only (grandfather r0)", price_ratio=round(kept, 3), price_drop=round(1 - kept, 3)))
# lagged assessment: effective rate on current rent with a 5-year trailing mean
ma = np.mean([(1 + gam) ** (-j) for j in range(1, 6)])
shock.append(dict(design="5y-lag effective rate, steady 2% growth", price_ratio=round(tau_bar * ma, 3),
                  price_drop=float("nan")))
shock.append(dict(design="5y-lag effective rate, after a -20% rent step", price_ratio=round(tau_bar / 0.8, 3),
                  price_drop=float("nan")))
sd = pd.DataFrame(shock)
sd.to_csv(os.path.join(DATA, "lvt_shock.csv"), index=False)
print(sd.to_string(index=False))
ten = [r for r in shock if r["design"] == "phase-in 10y"][0]["price_ratio"]
print(f"\nland wealth at risk at full capture: {land * tau_bar:,.0f} $B; with a 10y phase-in: {land * (1 - ten):,.0f} $B")
