"""Like-for-like context for 'Australia vs the paper's US 0.33'.

The two coverage ratios use different baskets: the paper divides by the Orshansky 1963 bundle (CPI-updated),
Australia by the Henderson line, the JobSeeker package and the Age Pension. This script puts both sides on a
common, currency-free footing: (i) each basket as a share of disposable income per head, and (ii) measured land
rent per person as a share of disposable income per head.

US inputs: the paper's own 2025 grid (pinning/data/kappa_results.csv, copied to data/raw/us/ at commit a144337),
CPIAUCSL (calendar-year means) for the Orshansky bundle, BEA disposable personal income per capita
(FRED A229RC0A052NBEA). US rent per person for a grid member = coverage x bundle cost.
AU inputs: out/coverage.csv from build_coverage.py.
Writes out/us_comparison.csv.
"""
import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "out"
ORSHANSKY_1963 = {"single": 1540.0, "pc4": 782.0}   # 1963 dollars, as in pinning/code/feasibility_kappa.py


def fred_annual_mean(path, col):
    by = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if r[col].strip():          # FRED leaves October 2025 CPI blank (not collected during the shutdown)
                by.setdefault(int(r["observation_date"][:4]), []).append(float(r[col]))
    return {y: sum(v) / len(v) for y, v in by.items()}


def main():
    cpi = fred_annual_mean(RAW / "us" / "CPIAUCSL.csv", "CPIAUCSL")
    dpi = fred_annual_mean(RAW / "us" / "A229RC0A052NBEA.csv", "A229RC0A052NBEA")
    with open(RAW / "us" / "kappa_results_paper.csv", newline="") as f:
        us = {int(r["year"]): r for r in csv.DictReader(f)}[2025]
    ps = {b: v * cpi[2025] / cpi[1963] for b, v in ORSHANSKY_1963.items()}
    us_rent_pp = []
    for k, v in us.items():
        if k.startswith("k_") and v and k.endswith("_single"):
            us_rent_pp.append(float(v) * ps["single"])   # one value per numerator construction
    us_flow_pp = [float(us[f"k_flow_{ls}_single"]) * ps["single"] for ls in ("ls30", "ls50")]
    us_land_pp = [float(us[f"k_z1_hh_{c}_single"]) * ps["single"] for c in ("gs10", "gs10p")]
    with open(OUT / "coverage.csv", newline="") as f:
        au = list(csv.DictReader(f))[-1]
    pop, hdi = float(au["population"]), float(au["hdi_per_head_annual"])
    au_flow_pp = [float(au[f"rent_rent_{ls}_bn"]) * 1e9 / pop for ls in ("ls30", "ls50")]
    au_land_pp = [float(au[f"rent_land_res_{c}_bn"]) * 1e9 / pop for c in ("y", "y150")]
    rows = [
        ("US", "2025", "coverage median [min-max] (paper)",
         f"{float(us['kappa_med']):.3f} [{float(us['kappa_min']):.3f}-{float(us['kappa_max']):.3f}]"),
        ("US", "2025", "Orshansky single bundle, $ per year", f"{ps['single']:.0f}"),
        ("US", "2025", "Orshansky per-capita (family of four) bundle, $ per year", f"{ps['pc4']:.0f}"),
        ("US", "2025", "disposable personal income per head, $", f"{dpi[2025]:.0f}"),
        ("US", "2025", "single bundle / income per head", f"{ps['single'] / dpi[2025]:.3f}"),
        ("US", "2025", "per-capita bundle / income per head", f"{ps['pc4'] / dpi[2025]:.3f}"),
        ("US", "2025", "land rent per person, median of the 2025 numerators, $", f"{statistics.median(us_rent_pp):.0f}"),
        ("US", "2025", "land rent per person / income per head", f"{statistics.median(us_rent_pp) / dpi[2025]:.3f}"),
        ("AU", au["financial_year"], "coverage median [min-max]",
         f"{float(au['coverage_median']):.3f} [{float(au['coverage_min']):.3f}-{float(au['coverage_max']):.3f}]"),
        ("AU", au["financial_year"], "household disposable income per head, $ (Melbourne Institute Table 2 x 52)",
         f"{float(au['hdi_per_head_annual']):.0f}"),
        ("AU", au["financial_year"], "Henderson single / income per head", f"{float(au['cost_henderson_over_hdi_per_head']):.3f}"),
        ("AU", au["financial_year"], "JobSeeker package / income per head", f"{float(au['cost_jobseeker_over_hdi_per_head']):.3f}"),
        ("AU", au["financial_year"], "Age Pension / income per head", f"{float(au['cost_age_pension_over_hdi_per_head']):.3f}"),
        ("AU", au["financial_year"], "land rent per person, median of the six numerators, $", f"{float(au['rent_per_person_median']):.0f}"),
        ("AU", au["financial_year"], "land rent per person / income per head", f"{float(au['rent_per_person_over_hdi_per_head']):.3f}"),
        ("US", "2025", "housing-rent constructions (0.30, 0.50 x PCE housing) per person / income per head",
         " to ".join(f"{v / dpi[2025]:.3f}" for v in us_flow_pp)),
        ("AU", au["financial_year"], "housing-rent constructions (0.30, 0.50 x actual + imputed rent) per person / income per head",
         " to ".join(f"{v / hdi:.3f}" for v in au_flow_pp)),
        ("US", "2025", "household land x 10-year yield (+0, +1.5) per person / income per head",
         " to ".join(f"{v / dpi[2025]:.3f}" for v in us_land_pp)),
        ("AU", au["financial_year"], "residential land x 10-year yield (+0, +1.5) per person / income per head",
         " to ".join(f"{v / hdi:.3f}" for v in au_land_pp)),
    ]
    with open(OUT / "us_comparison.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["country", "period", "quantity", "value"])
        w.writerows(rows)
    for r in rows:
        print(" | ".join(r))


if __name__ == "__main__":
    main()
