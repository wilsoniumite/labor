# check_rent_base.py — code/rent_base.py against the paper's own coverage file and the numbers SKETCH.md quotes.
#   R1  the four rent-bill coverage members equal ../pinning/data/kappa_results.csv's (k_flow_*), every common year
#   R2  the series ends at the last complete calendar year of the CPI
#   R3-R5  the quoted readings: site rent a person, its share of disposable income, the floor's cost over GDP
# Run from provisioning/:  python3 checks/check_rent_base.py      Exit 0 only if every check passes.
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import rent_base as rb  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def prints(value, printed, decimals):
    return abs(value - printed) <= 0.5 * 10.0 ** (-decimals) * 1.05


t = rb.table()
k = pd.read_csv(os.path.join(rb.ROOT, "pinning", "data", "kappa_results.csv")).set_index("year")
common = [y for y in t.index if y in k.index]
gap = max(abs(t.loc[y, f"cover_{b}_{s}"] - k.loc[y, f"k_flow_ls{s}_{c}"])
          for y in common for b, c in (("family4", "pc4"), ("single", "single")) for s in ("30", "50"))
check("R1 the rent-bill coverage members are the paper's, every common year (1e-12)", gap < 1e-12,
      f"{len(common)} years, largest gap {gap:.1e}")
check("R2 the series ends in 2024, the CPI's last complete calendar year", int(t.index[-1]) == 2024)

a, b = t.loc[1975], t.loc[2024]
check("R3 site rent a person, 2024 dollars: 1,153-1,922 in 1975 and 2,776-4,627 in 2024",
      all(prints(v, q, 0) for v, q in ((a["rent_pp_30_last"], 1153), (a["rent_pp_50_last"], 1922),
                                       (b["rent_pp_30_last"], 2776), (b["rent_pp_50_last"], 4627))),
      f"{a['rent_pp_30_last']:.0f}, {a['rent_pp_50_last']:.0f}; {b['rent_pp_30_last']:.0f}, {b['rent_pp_50_last']:.0f}")
check("R4 its share of disposable income: 3.5-5.8% in 1975, 4.3-7.1% in 2024",
      all(prints(100 * v, q, 1) for v, q in ((a["share_dpi_30"], 3.5), (a["share_dpi_50"], 5.8),
                                             (b["share_dpi_30"], 4.3), (b["share_dpi_50"], 7.1))),
      f"{100 * a['share_dpi_30']:.2f}, {100 * a['share_dpi_50']:.2f}; {100 * b['share_dpi_30']:.2f}, {100 * b['share_dpi_50']:.2f}")
c = t.loc[1955]
check("R5 a poverty-line bundle for every person, over GDP: 27-52% in 1955, 18-35% in 1975, 9-18% in 2024",
      all(prints(100 * v, q, 0) for v, q in ((c["floor_gdp_family4"], 27), (c["floor_gdp_single"], 52),
                                             (a["floor_gdp_family4"], 18), (a["floor_gdp_single"], 35),
                                             (b["floor_gdp_family4"], 9), (b["floor_gdp_single"], 18))),
      "; ".join(f"{100 * r['floor_gdp_family4']:.1f}-{100 * r['floor_gdp_single']:.1f}" for r in (c, a, b)))

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
