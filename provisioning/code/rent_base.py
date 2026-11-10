# rent_base.py — how large the land loop is: the site-rent base per person against income, a poverty-line bundle and GDP.
#
# The base is the paper's rent-bill measure (Appendix D of the pinning paper, code/feasibility_kappa.py there): land's
# share, 0.30 and 0.50, of BEA's personal consumption of housing services. Those shares are held fixed over time, so the
# series cannot show land's share of housing rising; the paper calls its land measures lower bounds (mineral and
# commercial rents are outside). The bundle is Orshansky's 1963 base updated by the CPI: 782 dollars a person in a
# family of four, 1,540 for a person alone. Every input is already in the repository:
#   ../pinning/cache/DHSGRC1A027NBEA.csv   housing services, $bn          ../pinning/cache/B230RC0A052NBEA.csv  population, thousands
#   ../pinning/cache/CPIAUCSL.csv          CPI, monthly                   ../three-taxes/cache/GDPA.csv         GDP, $bn
#   ../austax/coverage/data/raw/us/A229RC0A052NBEA.csv   disposable personal income per person, $
# Run from provisioning/:  python3 code/rent_base.py      Gated by checks/check_rent_base.py.

import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAND_SHARES = (0.30, 0.50)
BUNDLES_1963 = {"family4": 782.0, "single": 1540.0}


def annual(rel, full=1):
    """A FRED file as an annual series; monthly files keep complete calendar years only (the repository's rule)."""
    d = pd.read_csv(os.path.join(ROOT, rel), parse_dates=["observation_date"])
    d["year"] = d["observation_date"].dt.year
    g = d.groupby("year")[d.columns[1]].agg(["mean", "count"])
    return g[g["count"] >= full]["mean"]


def table():
    hs = annual("pinning/cache/DHSGRC1A027NBEA.csv")
    pop = annual("pinning/cache/B230RC0A052NBEA.csv")
    cpi = annual("pinning/cache/CPIAUCSL.csv", full=12)
    dpi = annual("austax/coverage/data/raw/us/A229RC0A052NBEA.csv")
    gdp = annual("three-taxes/cache/GDPA.csv")
    years = sorted(set(hs.index) & set(pop.index) & set(cpi.index) & set(dpi.index) & set(gdp.index))
    rows = []
    for y in years:
        row = dict(year=y)
        for s in LAND_SHARES:
            k = f"{int(100 * s)}"
            rent = s * hs[y] * 1e9 / (pop[y] * 1e3)                   # dollars a person a year
            row[f"rent_pp_{k}"] = rent
            row[f"rent_pp_{k}_last"] = rent * cpi[years[-1]] / cpi[y]  # in the last year's dollars
            row[f"share_dpi_{k}"] = rent / dpi[y]
            row[f"share_gdp_{k}"] = s * hs[y] / gdp[y]
            for name, base in BUNDLES_1963.items():
                row[f"cover_{name}_{k}"] = rent / (base * cpi[y] / cpi[1963])
        for name, base in BUNDLES_1963.items():                       # a poverty-line bundle for every person, over GDP
            row[f"floor_gdp_{name}"] = base * cpi[y] / cpi[1963] * pop[y] * 1e3 / (gdp[y] * 1e9)
        rows.append(row)
    return pd.DataFrame(rows).set_index("year")


if __name__ == "__main__":
    t = table()
    last = int(t.index[-1])
    show = [y for y in (1955, 1965, 1975, 1985, 1995, 2005, 2015, last) if y in t.index]
    print(f"site rent a person, {last} dollars; share of disposable income; share of a poverty-line bundle (low, high land share)")
    for y in show:
        r = t.loc[y]
        print("  %d  $%5.0f-%5.0f   %.3f-%.3f of income   family of four %.2f-%.2f   alone %.2f-%.2f   the floor %.3f-%.3f of GDP"
              % (y, r["rent_pp_30_last"], r["rent_pp_50_last"], r["share_dpi_30"], r["share_dpi_50"], r["cover_family4_30"],
                 r["cover_family4_50"], r["cover_single_30"], r["cover_single_50"], r["floor_gdp_family4"], r["floor_gdp_single"]))
