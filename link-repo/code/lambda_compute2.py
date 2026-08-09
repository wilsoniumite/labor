# lambda_compute2.py — wage-linkage of US consumption financing (lambda_C) and tax revenue (lambda_R)
# v2: verified-current FRED series only; total TOPI derived by NIPA identity W054 - ptax - corp.
# All classification choices live in GRID; the reported object is the band across all combos.

# %% imports
import io
import itertools
import requests
import pandas as pd
import numpy as np
from tqdm.auto import tqdm

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

# concept -> ordered candidates (verified by FRED page titles on 2026-08-03)
CANDIDATES = {
    "wages":        ["A576RC1"],            # wage & salary disbursements, monthly, current
    "supplements":  ["A038RC1A027NBEA"],    # supplements to wages & salaries, annual
    "proprietors":  ["A041RC1A027NBEA"],
    "rental":       ["A048RC1A027NBEA"],    # rental income of persons (incl. imputed owner net rent)
    "interest":     ["A064RC1A027NBEA"],
    "dividends":    ["B703RC1A027NBEA", "B703RC1Q027SBEA"],
    "soc_benefits": ["A063RC1A027NBEA"],
    "contribs":     ["A061RC1A027NBEA"],
    "ptax":         ["W055RC1A027NBEA"],
    "pce":          ["PCECA", "PCEC"],
    "tax_receipts": ["W054RC1A027NBEA"],    # TOTAL govt current TAX receipts (excl. social contribs)
    "corp_tax_fed": ["FCTAX"],
    "corp_tax_sl":  ["ASLCTAX"],
    "prop_tax":     ["B249RC1Q027SBEA"],    # S&L property taxes, quarterly, current
    "imputed_rent": ["A2013C1A027NBEA"],    # gross imputed rental, owner-occupied; lags (~2022)
}

# loose value anchors ($B) at the anchor year, ONLY to catch wrong-series pulls; never substitutes data
SANITY = {
    "wages": (9000, 14000), "supplements": (2000, 4200), "proprietors": (1200, 2600),
    "rental": (500, 1400), "interest": (1100, 2600), "dividends": (1000, 2700),
    "soc_benefits": (3000, 5200), "contribs": (1300, 2600), "ptax": (1900, 3600),
    "pce": (16500, 21000), "tax_receipts": (4200, 7000), "corp_tax_fed": (250, 750),
    "corp_tax_sl": (40, 300), "prop_tax": (500, 1100), "imputed_rent": (1400, 2600),
}
ANCHOR = 2023  # sanity anchor year; series ending earlier are checked at their last year with a widened band

import os, time
CACHE = "cache"
os.makedirs(CACHE, exist_ok=True)

def pull_fred(sid):
    fp = f"{CACHE}/{sid}.csv"
    if os.path.exists(fp):
        txt = open(fp).read()
    else:
        txt = None
        for wait in (0, 8, 25):          # patient retries; FRED throttles bursts
            if wait: time.sleep(wait)
            try:
                r = requests.get(FRED_CSV.format(sid=sid), timeout=30)
            except requests.RequestException:
                continue
            if r.status_code == 200 and "observation_date" in r.text[:100]:
                txt = r.text
                open(fp, "w").write(txt)
                break
        time.sleep(2.0)                   # courtesy delay between series
        if txt is None:
            return None
    df = pd.read_csv(io.StringIO(txt))
    if sid not in df.columns:
        return None
    idx = pd.to_datetime(df["observation_date"], errors="coerce")
    s = pd.Series(pd.to_numeric(df[sid], errors="coerce").values, index=idx).dropna()
    return s if len(s) > 10 else None

def annualize(s):
    return s.groupby(s.index.year).mean()

def fetch_all():
    data, ledger = {}, []
    for concept, sids in tqdm(CANDIDATES.items(), desc="pulling FRED"):
        got = None
        for sid in sids:
            s = pull_fred(sid)
            if s is None:
                ledger.append((concept, sid, "FAIL: no series")); continue
            a = annualize(s)
            last = int(a.index.max())
            chk_year = min(ANCHOR, last)
            lo, hi = SANITY[concept]
            if chk_year < ANCHOR:            # widen band for off-anchor check
                lo, hi = lo * 0.6, hi * 1.1
            v = float(a.loc[chk_year])
            if not (lo <= v <= hi):
                ledger.append((concept, sid, f"FAIL sanity: {chk_year}={v:.0f} not in [{lo:.0f},{hi:.0f}]")); continue
            stale = last < ANCHOR
            ledger.append((concept, sid, f"OK {chk_year}={v:.0f} last={last}" + ("  [STALE]" if stale else "")))
            got = (sid, a, stale)
            break
        data[concept] = got
    return data, ledger

# %% rule grid — each axis is a labeled classification choice
GRID = {
    "prop_labor_share": [0.50, 0.65, 0.80],
    "cap_tax_tilt":     [1.0, 1.5],          # relative personal-tax rate on capital income
    "corp_lambda":      [0.25, 0.50],        # current-labor-linked share of corporate tax
    "transfer_funding": ["pooled", "earmarked"],
    "financing_order":  ["capital_first", "proportional", "wages_first"],
}
R_KEYS = ["tax_receipts", "ptax", "corp_tax_fed", "corp_tax_sl", "prop_tax", "contribs"]

def tax_linkages(x, y, rules):
    """returns (lamR_all, lam_nonpayroll, ok). x = lambda_C guess feeding sales-tax linkage."""
    if any(k not in y for k in R_KEYS):
        return np.nan, np.nan, False
    pls, tilt = rules["prop_labor_share"], rules["cap_tax_tilt"]
    W_pre = y["wages"] + y["supplements"] + pls * y["proprietors"]
    K_pre = (1 - pls) * y["proprietors"] + y["rental"] + y["interest"] + y["dividends"]
    w_tax_share = W_pre / (W_pre + tilt * K_pre)
    corp_total = y["corp_tax_fed"] + y["corp_tax_sl"]
    topi = y["tax_receipts"] - y["ptax"] - corp_total          # NIPA identity
    sales_part = max(topi - y["prop_tax"], 0.0)                 # residual TOPI: consumption-linked, lambda = x
    pit_linked = y["ptax"] * w_tax_share
    corp_linked = corp_total * rules["corp_lambda"]
    nonpay_linked = pit_linked + corp_linked + sales_part * x   # property part: current-wage lambda = 0
    lam_nonpayroll = nonpay_linked / y["tax_receipts"]
    lamR_all = (y["contribs"] * 1.0 + nonpay_linked) / (y["tax_receipts"] + y["contribs"])
    return lamR_all, lam_nonpayroll, True

def lambda_C_year(y, rules):
    pls, tilt, order = rules["prop_labor_share"], rules["cap_tax_tilt"], rules["financing_order"]
    W_pre = y["wages"] + y["supplements"] + pls * y["proprietors"]
    K_pre = (1 - pls) * y["proprietors"] + y["rental"] + y["interest"] + y["dividends"]
    w_tax_share = W_pre / (W_pre + tilt * K_pre)
    W_net = W_pre - y["contribs"] - y["ptax"] * w_tax_share
    K_net = K_pre - y["ptax"] * (1 - w_tax_share)
    T, C = y["soc_benefits"], y["pce"]

    x = 0.8
    for _ in range(200):
        lamR_all, lam_nonpay, ok = tax_linkages(x, y, rules)
        if rules["transfer_funding"] == "earmarked" and ok:
            ear = min(y["contribs"], T)
            lam_T = (ear + (T - ear) * lam_nonpay) / T
        elif ok:
            lam_T = lamR_all
        else:
            lam_T = x  # self-consistent proxy when revenue split unavailable
        Wl = W_net + lam_T * T
        Ol = K_net + (1 - lam_T) * T
        if order == "proportional":
            x_new = Wl / (Wl + Ol)
        elif order == "wages_first":     # upper bound: saving comes out of ownership income first
            x_new = (min(Wl, C) + max(C - Wl - Ol, 0.0)) / C
        else:                            # capital_first, lower bound
            x_new = min(Wl, max(C - Ol, 0.0)) / C
        if abs(x_new - x) < 1e-12:
            return x_new
        x = x_new
    return x

# %% run
if __name__ == "__main__":
    data, ledger = fetch_all()
    print("\n=== validation ledger ===")
    for c, sid, msg in ledger:
        print(f"{c:14s} {sid:18s} {msg}")

    core = ["wages","supplements","proprietors","rental","interest","dividends",
            "soc_benefits","contribs","ptax","pce"]
    missing = [c for c in core if data.get(c) is None]
    if missing:
        print(f"\nBLOCKED: {missing} unavailable — stopping rather than approximating."); raise SystemExit(1)
    have_R = all(data.get(k) is not None for k in R_KEYS)
    have_ir = data.get("imputed_rent") is not None
    ir_last = int(data["imputed_rent"][1].index.max()) if have_ir else None
    print(f"\nrevenue split available: {have_R};  imputed rent available through: {ir_last}")

    need = core + (R_KEYS if have_R else [])
    years = None
    for c in set(need):
        yy = set(data[c][1].index)
        years = yy if years is None else years & yy
    years = sorted(v for v in years if v >= 1960)

    combos = [dict(zip(GRID, v)) for v in itertools.product(*GRID.values())]
    rows = []
    for yr in tqdm(years, desc="years"):
        y = {c: float(t[1].loc[yr]) for c, t in data.items() if t is not None and yr in t[1].index}
        vals  = [lambda_C_year(y, r) for r in combos]
        row = {"year": yr, "lamC_min": min(vals), "lamC_med": float(np.median(vals)), "lamC_max": max(vals)}
        if have_ir and yr <= ir_last:
            IR = y["imputed_rent"]
            y2 = dict(y); y2["pce"] = y["pce"] - IR
            y2["rental"] = y["rental"] - min(y["rental"], IR)   # remove owner net rent from ownership income
            vir = [lambda_C_year(y2, r) * (y["pce"] - IR) / y["pce"] for r in combos]  # IR part: 0 wage-linked
            row |= {"lamC_IR_min": min(vir), "lamC_IR_med": float(np.median(vir)), "lamC_IR_max": max(vir)}
        if have_R:
            vR = []
            for r in combos:
                xc = lambda_C_year(y, r)
                lamR, _, ok = tax_linkages(xc, y, r)
                if ok: vR.append(lamR)
            row |= {"lamR_min": min(vR), "lamR_med": float(np.median(vR)), "lamR_max": max(vR)}
        rows.append(row)

    res = pd.DataFrame(rows).set_index("year")
    os.makedirs("data", exist_ok=True); res.to_csv("data/lambda_results.csv")
    snap = res.loc[[y for y in (1965, 1975, 1985, 1995, 2005, 2015, res.index.max()) if y in res.index]]
    print("\n=== snapshots ===\n" + snap.round(3).to_string())

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.fill_between(res.index, res["lamC_min"], res["lamC_max"], alpha=0.25, label="λ_C band across rule grid")
    ax.plot(res.index, res["lamC_med"], lw=2, label="λ_C median rule set")
    if "lamC_IR_med" in res:
        ir = res.dropna(subset=["lamC_IR_med"])
        ax.plot(ir.index, ir["lamC_IR_med"], lw=1.5, ls="--", label="λ_C, imputed rent reclassified (median)")
    if "lamR_med" in res:
        ax.plot(res.index, res["lamR_med"], lw=1.5, color="tab:green", label="λ_R median (tax revenue exposure)")
    ax.axhline(0.89, color="k", lw=1, ls=":", label="essay napkin (0.89)")
    ax.set_ylim(0.4, 1.0); ax.set_ylabel("wage-linked share")
    ax.set_title("Wage linkage of US consumption financing and tax revenue, band across classification rules")
    ax.legend(loc="lower left", fontsize=8)
    fig.tight_layout(); os.makedirs("figures", exist_ok=True); fig.savefig("figures/lambda_band.png", dpi=150)
    print("\nwrote data/lambda_results.csv and figures/lambda_band.png")
