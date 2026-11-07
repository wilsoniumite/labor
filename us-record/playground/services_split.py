# services_split.py — a data look (2026-11-07): the fit's "other goods" (all consumption but shelter and durables) has
# one slow clock: hours of machine-making per unit of task capacity fall 0.44% a year (results/fit_Br0.json), against 3%
# in durables. Is the slow part services (Baumol) rather than nondurable goods? The wage over each, from BLS CPI indexes
# via FRED (fetched once into cache/, as code/panel.py does): nondurables (CUUR0000SAN) and services less rent of shelter
# (CUUR0000SASLE), beside the panel's wage over all but shelter (wage_exshelter) and over durables. Annual means over
# complete years only; the wage over X = the wage over all-but-shelter times (all-but-shelter CPI / X).
# Run from us-record/:  python3 playground/services_split.py
import os
import sys
import urllib.request

import numpy as np
import pandas as pd

CACHE = "cache"
SERIES = {"CUUR0000SAN": "nondurables", "CUUR0000SASLE": "services less rent of shelter", "CUUR0000SA0L2": "all but shelter"}


def fred(sid):
    path = os.path.join(CACHE, f"{sid}.csv")
    if not os.path.exists(path):
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
        if not data.startswith(b"observation_date") and not data.startswith(b"DATE"):
            sys.exit(f"{sid}: unexpected reply from FRED, not cached")
        open(path, "wb").write(data)
    s = pd.read_csv(path)
    s.columns = ["date", "value"]
    s["date"] = pd.to_datetime(s["date"])
    s["value"] = pd.to_numeric(s["value"], errors="coerce")
    s = s.dropna().set_index("date")["value"]
    g = s.groupby(s.index.year)
    return g.mean()[g.count() == 12]


if __name__ == "__main__":
    cpi = {sid: fred(sid) for sid in SERIES}
    P = pd.read_csv("data/panel.csv").set_index("year")
    w_xs = P["wage_exshelter"].dropna()
    years = [y for y in w_xs.index if all(y in c.index for c in cpi.values())]
    y0 = years[0]
    out = pd.DataFrame(index=years)
    out["wage_over_all_but_shelter"] = w_xs.loc[years] / w_xs.loc[y0]
    for sid in ("CUUR0000SAN", "CUUR0000SASLE"):
        rel = (cpi["CUUR0000SA0L2"].loc[years] / cpi[sid].loc[years])
        out[f"wage_over_{SERIES[sid].split()[0]}"] = out["wage_over_all_but_shelter"] * rel / rel.loc[y0]
    out["wage_over_durables"] = P.loc[years, "wage_goods"] / P.loc[y0, "wage_goods"]
    print(f"index {y0} = 1; years {years[0]}-{years[-1]}")
    for col in out.columns:
        s = out[col]
        rates = []
        for a, b in ((y0, 1973), (1973, 1995), (1995, 2024)):
            if a in s.index and b in s.index:
                rates.append(f"{a}-{b} {100 * np.log(s.loc[b] / s.loc[a]) / (b - a):+.2f}%")
        print(f"{col:32s} x{s.iloc[-1]:.2f} by {years[-1]} | " + " | ".join(rates))
    out.to_csv("playground/services_split.csv")
