# pull.py — fetch the eras thread's two external sources into cache/ (gitignored) and write the series it uses to data/.
#   1. Warde, P. (2007). Energy Consumption in England & Wales, 1560-2000. Consiglio Nazionale delle Ricerche.
#      Appendix I, table 1: energy inputs by carrier, PJ per year (food for the population, feed for draught animals, the
#      water through mill wheels, the wind on sails and windmills, coal, ...). Harvard's energy-history mirror.
#   2. Thomas, R. and N. Dimsdale (2017). A Millennium of Macroeconomic Data for the UK, v3.1. Bank of England.
#      Sheet "A1. Headline series": real GDP, employment, weekly hours, GDP per hour, the labour share excluding rents.
# Both URLs answered HTTP 200 on 2026-11-17. If either fails, stop: no substitute source is used.
# Run from eras/:  ../venv/Scripts/python.exe code/pull.py
from pathlib import Path
import re
import subprocess

import openpyxl
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE, DATA = ROOT / "cache", ROOT / "data"
WARDE_URL = "https://histecon.fas.harvard.edu:443/energyhistory/data/Warde_Energy%20Consumption%20England.pdf"
BOE_URL = ("https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/"
           "a-millennium-of-macroeconomic-data-for-the-uk.xlsx")


def fetch(url, path, magic):
    if not path.exists():
        r = requests.get(url, timeout=300)
        r.raise_for_status()
        path.write_bytes(r.content)
    head = path.read_bytes()[:4]
    assert head.startswith(magic), f"{path.name}: unexpected content {head!r}"
    return path


# %% Warde, appendix table 1, 1560-1870. To 1850 every row prints six carriers (draught, population, firewood, wind,
# water, coal) and the total. From 1851 firewood is blank (zero) and oil appears from 1857, so a row is draught,
# population, wind, water, coal, [oil,] total; later columns (gas, primary electricity) start after 1870.
pdf = fetch(WARDE_URL, CACHE / "warde_2007.pdf", b"%PDF")
txt = subprocess.run(["pdftotext", "-layout", "-f", "113", "-l", "125", str(pdf), "-"], capture_output=True, text=True,
                     check=True).stdout
rows = []
for line in txt.splitlines():
    m = re.match(r"^\s*(1[5-8]\d\d)\s+(.*)$", line)
    if not m or int(m.group(1)) > 1870:
        continue
    y, nums = int(m.group(1)), [float(v) for v in m.group(2).split()]
    if y <= 1850:
        assert len(nums) == 7, (y, nums)                 # draught, population, firewood, wind, water, coal, total
        rows.append([y, *nums[:6], 0.0, nums[6]])
    else:
        assert len(nums) in (6, 7), (y, nums)            # draught, population, wind, water, coal, [oil,] total
        oil = nums[5] if len(nums) == 7 else 0.0
        rows.append([y, nums[0], nums[1], 0.0, nums[2], nums[3], nums[4], oil, nums[-1]])
w = pd.DataFrame(rows, columns=["year", "draught_feed", "human_food", "firewood", "wind", "water", "coal", "oil", "total"])
w = w.drop_duplicates("year").sort_values("year").reset_index(drop=True)
assert list(w.year) == list(range(1560, 1871)), "Warde: a year is missing or doubled"
gap = (w[["draught_feed", "human_food", "firewood", "wind", "water", "coal", "oil"]].sum(axis=1) - w.total).abs()
assert gap.max() <= 0.25, f"Warde: carriers do not add to the printed total (max gap {gap.max():.2f} PJ)"
assert (w.coal.loc[w.year > 1850] > 10 * w.wind.loc[w.year > 1850]).all()      # columns read in the right places
w.to_csv(DATA / "warde_energy_1560_1870.csv", index=False)
print(f"Warde: {len(w)} years, carriers add to the total within {gap.max():.2f} PJ")

# %% Bank of England millennium dataset, sheet A1 (descriptions in row 4, units in row 6, data from row 9)
xl = fetch(BOE_URL, CACHE / "boe_millennium_v3.1.xlsx", b"PK")
ws = openpyxl.load_workbook(xl, read_only=True, data_only=True)["A1. Headline series"]
a1 = list(ws.iter_rows(min_row=1, max_row=1000, values_only=True))
desc, units = a1[3], a1[5]
COLS = {"gdp_real": 1, "pop_gbni": 24, "pop_england": 25, "employment": 26, "weekly_hours": 28,
        "gdp_per_hour": 32, "labour_share_ex_rents": 33}
assert desc[1].startswith("Real UK GDP at market prices") and desc[26] == "Employment"
assert desc[28] == "Average weekly hours worked" and units[32] == "Real GDP per hour, 2013 prices"
assert desc[33] == "Labour share, whole economy excluding rents"
b = pd.DataFrame([[r[0], *[r[i] for i in COLS.values()]] for r in a1[8:] if isinstance(r[0], (int, float))],
                 columns=["year", *COLS])
b = b[(b.year >= 1700) & (b.year <= 2016)].astype(float).astype({"year": int})
b.to_csv(DATA / "boe_uk_1700_2016.csv", index=False)

# %% sheet A47: composite average weekly earnings (England/GB, £) and the implied consumption and investment deflators
# (UK, 2013 = 100, from 1830); wage over the investment deflator is a coarse waterline (it prices structures with
# machines)
ws = openpyxl.load_workbook(xl, read_only=True, data_only=True)["A47. Wages and prices"]
a47 = list(ws.iter_rows(min_row=1, max_row=900, values_only=True))
assert a47[2][1] == "Composite Average Weekly Earnings series" and a47[2][9] == "Implied consumption deflator"
assert a47[2][10] == "Implied investment deflator"
wp = pd.DataFrame([[r[0], r[1], r[9], r[10]] for r in a47 if isinstance(r[0], (int, float))],
                  columns=["year", "weekly_earnings", "consumption_deflator", "investment_deflator"])
wp = wp[(wp.year >= 1700) & (wp.year <= 2016)].astype(float).astype({"year": int})
wp.to_csv(DATA / "boe_uk_wages_prices.csv", index=False)
print(f"BoE A47: earnings from {int(wp.dropna(subset=['weekly_earnings']).year.min())}, investment deflator from "
      f"{int(wp.dropna(subset=['investment_deflator']).year.min())}")
print(f"BoE: {len(b)} years; GDP per hour from {int(b.dropna(subset=['gdp_per_hour']).year.min())}, "
      f"employment from {int(b.dropna(subset=['employment']).year.min())}, "
      f"labour share from {int(b.dropna(subset=['labour_share_ex_rents']).year.min())}")
