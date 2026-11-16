# eras.py — output per hour by era, U.S. nonfarm business sector (FRED OPHNFB, index), the introduction's numbers.
# Annual averages of the quarterly index (complete years only), then annualized log growth between era endpoints.
# Reads cache/fred/OPHNFB.csv, the dated pull of 2026-11-16 (cache/fred/MANIFEST.csv), which replaced the vintage
# copied from ../paths/cache (identical through 2019; 2019-25 revised from 2.16 to 2.25 percent a year).
# Run from stagnation/:  ../venv/bin/python code/eras.py
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ERAS = ((1948, 1973), (1973, 1995), (1995, 2004), (2004, 2019), (2019, 2025))


def annual(path=ROOT / "cache" / "fred" / "OPHNFB.csv"):
    s = pd.read_csv(path, parse_dates=["observation_date"]).set_index("observation_date")["OPHNFB"]
    g = s.groupby(s.index.year)
    return g.mean()[g.count() == 4]


def eras(a=None):
    a = annual() if a is None else a
    return {(y0, y1): 100 * (np.log(a[y1]) - np.log(a[y0])) / (y1 - y0) for y0, y1 in ERAS}


if __name__ == "__main__":
    for (y0, y1), g in eras().items():
        print(f"{y0}-{y1}: {g:.2f} percent a year")
