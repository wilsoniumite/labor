# swedish_fork.py — the Swedish companion to the deflator fork (Figure 3):
# manual-worker hourly pay deflated by (a) machine-made-goods CPI members and
# (b) housing CPI members. Primary source: SCB PXWeb API (Statistikdatabasen),
# every table verified by its metadata TITLE at pull time (the FRED page-title
# rule, transplanted). House rules: live pull with cache; sanity anchors only
# to catch wrong-series pulls; complete calendar years only; stop rather than
# approximate; every contestable choice a labeled member; nothing spliced
# across a break without an overlap gate.
#
# Wage members (the between-legs fork RATIO is wage-invariant — the wage
# cancels; wage members set only the legs' levels):
#   w_manuf: manual workers, mining+manufacturing (B+C), pay for time worked —
#            SLP11a (1952–2013) continued by SLP9a07/AM0103K8 (2008–2025);
#            treated as ONE series only if the 2008–2013 overlap agrees
#            within 1 percent, else the long member is refused.
#   w_klp:   manual workers, all private industry (B–S excl O), hourly
#            earnings incl. overtime (KLP), monthly 2008– (AHETPI's cousin).
# Machine-goods members: VV — "Durable goods", SCB's special aggregate, the
#   direct US durables-CPI analog; 05 furnishings/household equipment; 08.1
#   ICT equipment (window reported; dropped from the chart if short).
# Housing members: 04 housing incl. energy (Swedish KPI carries owner
#   interest costs → rate-sensitive, labeled); 04.1 actual rents (Swedish
#   rents are negotiated under the use-value system — scarcity partly shows
#   as queues, so this member is a lower bound on the scarcity signal);
#   KPIF-04 (fixed interest rate, 1987–, removes the policy-rate wobble).

# %% imports
import io
import json
import os
import time
import hashlib

import pandas as pd
import requests

BASE = "https://api.scb.se/OV0104/v1/doris/en/ssd"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, "cache")
os.makedirs(CACHE, exist_ok=True)

S = requests.Session()
S.headers["User-Agent"] = "laborformal-research/0.1"


def api(path, query=None):
    """GET metadata (query=None) or POST a data query; disk-cached; retries."""
    key = path if query is None else path + "|" + json.dumps(query, sort_keys=True)
    fp = os.path.join(CACHE, "scb_" + hashlib.md5(key.encode()).hexdigest() + ".json")
    if os.path.exists(fp):
        return json.load(open(fp, encoding="utf-8"))
    out = None
    for wait in (0, 8, 25):
        if wait:
            time.sleep(wait)
        try:
            if query is None:
                r = S.get(BASE + path, timeout=40)
            else:
                r = S.post(BASE + path, json={"query": query,
                                              "response": {"format": "json"}}, timeout=60)
        except requests.RequestException:
            continue
        if r.status_code == 200:
            out = json.loads(r.content.decode("utf-8-sig"))
            break
    time.sleep(1.2)  # SCB courtesy: ~10 calls/10 s
    if out is None:
        return None
    json.dump(out, open(fp, "w", encoding="utf-8"))
    return out


def item(code, values):
    return {"code": code, "selection": {"filter": "item", "values": values}}


def to_series(resp, keypos_time=-1, keep=None, keypos_group=0):
    """PXWeb json -> {groupcode: Series}; '..'/'.' dropped; monthly or annual index."""
    out = {}
    for row in resp["data"]:
        g = row["key"][keypos_group] if keep else "_"
        if keep and g not in keep:
            continue
        t = row["key"][keypos_time]
        v = row["values"][0]
        if v in ("..", ".", ""):
            continue
        out.setdefault(g, {})[t] = float(v)
    res = {}
    for g, d in out.items():
        s = pd.Series(d)
        if "M" in next(iter(d)):
            s.index = pd.to_datetime(s.index, format="%YM%m")
        else:
            s.index = s.index.astype(int)
        res[g] = s.sort_index()
    return res


def annualize_complete(s, need=12):
    """Annual means over COMPLETE years only (the deflator_fork.py rule)."""
    g = s.groupby(s.index.year)
    a, n = g.mean(), g.size()
    return a[n >= need]


# %% table registry — path, title fragment asserted at pull time
TABLES = {
    "kpi_coicop": ("/PR/PR0101/PR0101A/KPI2020COICOPM",
                   "Consumer Price Index 2020=100 by Product group"),
    "kpi_sa":     ("/PR/PR0101/PR0101DE/KPI2020SA1MA",
                   "CPI special aggregates for goods and services"),
    "kpif_coicop": ("/PR/PR0101/PR0101G/KPIF2020COICOPM",
                    "fixed interest rate 2020=100 by Product group"),
    "klp":        ("/AM/AM0101/AM0101A/LonArb07Privat",
                   "Average hourly earnings of manual workers in the private sector"),
    "slp_ind":    ("/AM/AM0103/AM0103A/SLP9a07",
                   "manual workers private sector (SLP) by industrial classification"),
    "slp_long":   ("/AM/AM0103/AM0103D/SLP11a",
                   "real pay development (mining and manufacturing)"),
}

# loose value anchors, ONLY to catch wrong-series pulls (never substitute data)
SANITY_2023 = {
    "kpi_total": (112, 126), "vv": (95, 130), "c05": (105, 140),
    "c04": (112, 148), "c041": (101, 118), "kpif04": (103, 132),
    "w_klp": (150, 235), "w_slp_bc": (150, 245),
}
SANITY_2013 = {"w_long13": (120, 185)}   # SLP11a checked at its last year

if __name__ == "__main__":
    ledger = []

    # -- title verification (the page-title rule) --
    for name, (path, frag) in TABLES.items():
        m = api(path)
        if m is None:
            print(f"BLOCKED: metadata unavailable for {name} ({path}) — stopping.")
            raise SystemExit(1)
        title = m.get("title", "")
        ok = frag.lower() in title.lower()
        ledger.append((name, "TITLE " + ("OK" if ok else "FAIL"), title[:80]))
        if not ok:
            print(f"TITLE MISMATCH for {name}: {title!r} lacks {frag!r} — stopping.")
            raise SystemExit(1)

    # -- CPI pulls (monthly, annualized over complete years) --
    coicop_codes = ["00", "04", "04.1", "05", "08.1"]
    r = api(TABLES["kpi_coicop"][0], [item("VaruTjanstegrupp", coicop_codes),
                                      item("ContentsCode", ["0000080H"])])
    kpi = to_series(r, keep=set(coicop_codes))
    r = api(TABLES["kpi_sa"][0], [item("VaruTjanstegrupp", ["VV"]),
                                  item("ContentsCode", ["0000084A"])])
    sa = to_series(r, keep={"VV"})
    r = api(TABLES["kpif_coicop"][0], [item("VaruTjanstegrupp", ["04"]),
                                       item("ContentsCode", ["00000813"])])
    kpif = to_series(r, keep={"04"})

    cpi = {}
    for label, s in [("kpi_total", kpi.get("00")), ("c04", kpi.get("04")),
                     ("c041", kpi.get("04.1")), ("c05", kpi.get("05")),
                     ("c081", kpi.get("08.1")), ("vv", sa.get("VV")),
                     ("kpif04", kpif.get("04"))]:
        if s is None or len(s) == 0:
            ledger.append((label, "MISSING", "no observations returned"))
            cpi[label] = None
            continue
        a = annualize_complete(s)
        ledger.append((label, "OK", f"{int(a.index.min())}–{int(a.index.max())}"))
        cpi[label] = a

    # -- wage pulls --
    r = api(TABLES["klp"][0], [item("SNI2007", ["B-S exkl.O"]),
                               item("Overtidstillagg", ["20"]),
                               item("ContentsCode", ["AM0101D4"])])
    w_klp_m = to_series(r, keep={"B-S exkl.O"}, keypos_group=0)["B-S exkl.O"]
    w_klp = annualize_complete(w_klp_m)
    ledger.append(("w_klp", "OK", f"{int(w_klp.index.min())}–{int(w_klp.index.max())} (monthly, complete years)"))

    r = api(TABLES["slp_ind"][0], [item("SNI2007", ["B+C"]),
                                   item("Arbetstidsart", ["0"]),
                                   item("Kon", ["1+2"]),
                                   item("ContentsCode", ["AM0103K8"])])
    w_slp_bc = to_series(r, keep={"B+C"}, keypos_group=0)["B+C"]
    ledger.append(("w_slp_bc", "OK", f"{int(w_slp_bc.index.min())}–{int(w_slp_bc.index.max())} (annual)"))

    r = api(TABLES["slp_long"][0], [item("Kon", ["1+2"]),
                                    item("ContentsCode", ["AM0103H9"])])
    w_long_hist = to_series(r, keep={"1+2"}, keypos_group=0)["1+2"]
    ledger.append(("w_long_hist", "OK", f"{int(w_long_hist.index.min())}–{int(w_long_hist.index.max())} (annual)"))

    # -- sanity anchors --
    checks = {"kpi_total": cpi["kpi_total"], "vv": cpi["vv"], "c05": cpi["c05"],
              "c04": cpi["c04"], "c041": cpi["c041"], "kpif04": cpi["kpif04"],
              "w_klp": w_klp, "w_slp_bc": w_slp_bc}
    failed = False
    for label, s in checks.items():
        lo, hi = SANITY_2023[label]
        v = float(s.loc[2023])
        ok = lo <= v <= hi
        ledger.append((label, "SANITY " + ("OK" if ok else "FAIL"), f"2023={v:.1f} band=[{lo},{hi}]"))
        failed |= not ok
    v = float(w_long_hist.loc[2013])
    lo, hi = SANITY_2013["w_long13"]
    ok = lo <= v <= hi
    ledger.append(("w_long_hist", "SANITY " + ("OK" if ok else "FAIL"), f"2013={v:.1f} band=[{lo},{hi}]"))
    failed |= not ok
    # hard check against a published number: KPI annual-average inflation 2022 ≈ 8.4%
    infl22 = float(cpi["kpi_total"].loc[2022] / cpi["kpi_total"].loc[2021] - 1)
    ok = 0.077 <= infl22 <= 0.091
    ledger.append(("kpi_total", "PUBLISHED-VALUE " + ("OK" if ok else "FAIL"),
                   f"2022 annual inflation = {infl22:.3f} (published ≈ 0.084)"))
    failed |= not ok

    print("=== validation ledger ===")
    for row in ledger:
        print(f"{row[0]:12s} {row[1]:22s} {row[2]}")
    if failed:
        print("\nBLOCKED: a sanity check failed — stopping rather than approximating.")
        raise SystemExit(1)

    # -- the long wage series: overlap gate, not a splice --
    overlap = sorted(set(w_long_hist.index) & set(w_slp_bc.index))
    ratios = (w_slp_bc.loc[overlap] / w_long_hist.loc[overlap])
    print(f"\noverlap gate (SLP9a07 B+C vs SLP11a), {overlap[0]}–{overlap[-1]}: "
          + ", ".join(f"{y}:{r_:.4f}" for y, r_ in ratios.items()))
    if (ratios - 1).abs().max() <= 0.01:
        w_manuf = pd.concat([w_long_hist[w_long_hist.index < overlap[0]], w_slp_bc]).sort_index()
        print("gate PASSED (≤1%): one series across the publication seam; modern table used from "
              f"{overlap[0]}.")
    else:
        w_manuf = None
        print("gate FAILED (>1%): long member REFUSED; wage-based fork restricted to 2008–.")

    # -- assemble annual panel --
    cols = {"w_klp": w_klp}
    if w_manuf is not None:
        cols["w_manuf"] = w_manuf
    for k, v_ in cpi.items():
        if v_ is not None:
            cols[k] = v_
    df = pd.DataFrame(cols)

    wage_key = "w_manuf" if w_manuf is not None else "w_klp"
    MACHINE = [k for k in ("vv", "c05", "c081") if k in df]
    HOUSING = [k for k in ("c04", "c041", "kpif04") if k in df]
    base = int(df.dropna(subset=[wage_key, "vv", "c04", "c041"]).index.min())
    last = int(df.dropna(subset=[wage_key, "vv", "c04", "c041"]).index.max())
    print(f"\nwage member: {wage_key}; base year {base}; last complete year {last}")

    legs = pd.DataFrame(index=df.index)
    for m in MACHINE + HOUSING:
        real = df[wage_key] / df[m]
        if pd.isna(real.get(base)):
            first = int(real.dropna().index.min())
            print(f"  member {m}: starts {first} (> base {base}) — kept in CSV, off the base-year chart")
            legs[f"leg_{m}"] = 100 * real / real.loc[first]
            continue
        legs[f"leg_{m}"] = 100 * real / real.loc[base]

    out = pd.concat([df, legs], axis=1)
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    out.to_csv(os.path.join(ROOT, "data", "swedish_fork.csv"))

    # -- snapshot + the plain-language decomposition --
    snap_years = [y for y in (base, 1990, 1995, 2000, 2008, 2015, 2020, last) if y in legs.index]
    print(f"\n=== the Swedish fork, {base} = 100 (wage: {wage_key}) ===")
    print(legs.loc[snap_years].round(1).to_string())
    for h in ("c04", "c041"):
        ratio = float(legs.loc[last, "leg_vv"] / legs.loc[last, f"leg_{h}"])
        print(f"fork ratio at {last}, durables (VV) vs {h}: {ratio:.2f}x")
    g = float(df.loc[last, wage_key] / df.loc[base, wage_key])
    print(f"\nplain numbers {base}->{last}:  paycheck x{g:.1f}   "
          f"durables prices x{float(df.loc[last,'vv']/df.loc[base,'vv']):.1f}   "
          f"rents x{float(df.loc[last,'c041']/df.loc[base,'c041']):.1f}   "
          f"housing-incl-energy x{float(df.loc[last,'c04']/df.loc[base,'c04']):.1f}")
    if 1995 in legs.index:
        print("since 1995 (US comparison window): "
              f"durables leg x{float(legs.loc[last,'leg_vv']/legs.loc[1995,'leg_vv']):.2f}, "
              f"rent leg x{float(legs.loc[last,'leg_c041']/legs.loc[1995,'leg_c041']):.2f}, "
              f"housing leg x{float(legs.loc[last,'leg_c04']/legs.loc[1995,'leg_c04']):.2f}")

    # -- figure --
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5))
    yrs = legs.index
    ax.plot(yrs, legs["leg_vv"], lw=2.2, color="tab:blue",
            label="pay deflated by durable goods CPI (machine-made)")
    ax.plot(yrs, legs["leg_c041"], lw=2.2, color="tab:red",
            label="pay deflated by actual-rents CPI (land-priced)")
    ax.plot(yrs, legs["leg_c04"], lw=1.4, color="tab:red", ls="--",
            label="… by housing incl. energy and owner costs")
    # c081 (ICT equipment) is off-scale (~x276 by 2025) — in the CSV, not the chart
    if "leg_c05" in legs and legs["leg_c05"].notna().sum() > 10:
        ax.plot(yrs, legs["leg_c05"], lw=0.9, alpha=0.6, color="tab:cyan",
                label="… by furnishings/household equipment CPI")
    ax.axhline(100, color="k", lw=0.8, ls=":")
    ax.set_ylabel(f"real hourly pay, manual workers, {base} = 100")
    ax.set_title("The Swedish fork: the same paycheck against machine-made goods and against housing")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig.savefig(os.path.join(ROOT, "figures", "fig_swedish_fork.png"), dpi=150)
    print("\nwrote data/swedish_fork.csv and figures/fig_swedish_fork.png")
