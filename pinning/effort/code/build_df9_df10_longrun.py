"""
build_df9_df10_longrun.py — pinning/effort

Consolidated rebuild of the long-run D-F ledgers DF9 (current-resource
origin, 1950-2025) and DF10 (full-PCE financing ledger with capacity bounds,
1950-2025), whose source-to-model construction was previously spread across
the legacy chat archives (the v28 audit's named gap). One script, from
archive_v28 inputs plus the vendored legacy intermediates, with every
generated column verified against the archived files by the companion check.

Reconstructed rules (each verified to machine precision in the 2026-08-31
consolidation session):

- DF9 composition shares 1960+ = legal_income_audit component shares;
  1950-59 = archived weak composition backcast (vendored table).
- Proprietor effort share low/mid/high: linear interpolation between the
  five proxy anchors 2005-2025; OLS logit-linear trend fitted on the five
  anchors, extrapolated 1950-2004 (the archive's WEAK_LOGIT_BACKCAST).
- Transfer wage-exposure mid 1960+ = program-value-weighted mean of the
  DF_3 program exposures (SS, Medicare, Medicaid, UI, other); low/high =
  archived DF_1 scenario bounds (vendored; per-program scenario
  recomputation is the remaining frontier); 1950-59 holds the 1960 values
  (the archive's rule).
- DF9 origin shares: labor = comp + prop x prop_eff + transfers x exposure;
  ownership = prop x (1-prop_eff) + rental + interest + dividends;
  fiscal = transfers x (1-exposure); each tier with matched parameters.
- DF10: PCE/DPI from graph_B0 (1960+) and the archived 1950s backcast;
  T = DF8 headline minimum-intertemporal share; centrals = (1-T) x DF9 mid
  shares; capacity lower = max(0, (1-T_weak_upper) x PCE - (1-labor_low) x
  DPI)/PCE; capacity upper = min(labor_high x DPI, PCE)/PCE.

KNOWN DISCREPANCY (surfaced 2026-08-31, pending Stella): the archived DF10
capacity upper for 1958-1979 (22 values) sits up to 3.28pp BELOW what the
archive's own DF9 labor_high implies under the formula that reproduces
every other year exactly - consistent with DF10 having been built from a
preliminary DF9 vintage whose pre-1970 high-scenario program-funding
handling was later revised (the low-scenario lower bound, untouched by that
revision, reproduces exactly in those same years). The rebuild emits the
coherent (wider, more conservative) values and writes the archived-vs-
rebuilt comparison to data/rebuilt/DF10_upper_1958_1979_discrepancy.csv.

Run from the repo root:
    ./venv/Scripts/python.exe pinning/effort/code/build_df9_df10_longrun.py
"""

import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
V28DF = ROOT / "archive_v28" / "inputs" / "df"
LEGIN = ROOT / "data" / "legacy_inputs"
OUT = ROOT / "data" / "rebuilt"

COMPS = ["employee_comp", "proprietors", "rental", "interest", "dividends", "transfers"]
YEARS = range(1950, 2026)


def load(p, key="year"):
    return {int(r[key]): r for r in csv.DictReader(open(p, encoding="utf-8-sig"))}


def f(r, k):
    return float(r[k])


def logit(p):
    return np.log(p / (1 - p))


def build():
    legal = load(V28DF / "legal_income_audit_1960_2025.csv")
    b0 = load(V28DF / "graph_B0_disposable_income_disposition_1960_2025.csv")
    df8 = load(LEGIN / "DF8_minimum_intertemporal_strong_weak_1950_2025.csv")
    df3 = load(LEGIN / "DF_3_program_funding_lookthrough_detail_1960_2025.csv")
    prox = load(LEGIN / "proprietor_effort_proxy_v1.csv")
    comp50 = load(LEGIN / "DF9_1950s_composition_backcast.csv")
    pd50 = load(LEGIN / "DF10_1950s_pce_dpi_backcast.csv")
    tbnd = load(LEGIN / "transfer_wage_exposure_bounds_1960_2025.csv")

    # Proprietor effort parameters: anchor interpolation + logit-linear backcast.
    anchors = sorted(prox)
    xs = np.array(anchors, float)
    prop = {}
    for tier, col in [("low", "effort_share_min"), ("mid", "effort_share_mid"),
                      ("high", "effort_share_max")]:
        ys = np.array([f(prox[a], col) for a in anchors])
        slope, icept = np.polyfit(xs, logit(ys), 1)
        prop[tier] = {y: (float(np.interp(y, xs, ys)) if y >= anchors[0]
                          else float(1 / (1 + np.exp(-(icept + slope * y)))))
                      for y in YEARS}

    # Transfer wage exposure: mid generated from DF_3 programs (1960+);
    # low/high vendored scenario bounds; 1950s hold the 1960 values.
    trans = {"low": {}, "mid": {}, "high": {}}
    for y in range(1960, 2026):
        r = df3[y]
        pairs = [("social_security_b", "social_security_central_wage_exposure"),
                 ("medicare_b", "medicare_central_wage_exposure"),
                 ("medicaid_b", "medicaid_central_wage_exposure"),
                 ("ui_b", "ui_wage_exposure"),
                 ("other_transfers_b", "other_central_wage_exposure")]
        num = sum(f(r, b) * f(r, e) for b, e in pairs)
        den = sum(f(r, b) for b, _ in pairs)
        trans["mid"][y] = num / den
        trans["low"][y] = f(tbnd[y], "transfer_wage_exposure_low")
        trans["high"][y] = f(tbnd[y], "transfer_wage_exposure_high")
    for tier in trans:
        for y in range(1950, 1960):
            trans[tier][y] = trans[tier][1960]

    # DF9: composition + origin shares.
    df9_rows = []
    for y in YEARS:
        if y >= 1960:
            sh = {c: f(legal[y], c + "_share") for c in COMPS}
            legal_tier = "STRONG_LEGAL_FORM"
        else:
            sh = {c: f(comp50[y], c + "_share_resources") for c in COMPS}
            legal_tier = "WEAK_COMPOSITION_BACKCAST"
        row = {"year": y, "legal_form_tier": legal_tier,
               "proprietor_effort_tier": ("PROXY_ANCHOR_INTERPOLATION" if y >= anchors[0]
                                          else "WEAK_LOGIT_BACKCAST")}
        for c in COMPS:
            row[c + "_share_resources"] = sh[c]
        for tier in ("low", "mid", "high"):
            row[f"proprietor_effort_share_{tier}"] = prop[tier][y]
            row[f"transfer_wage_exposure_{tier}"] = trans[tier][y]
            row[f"labor_origin_current_resource_share_{tier}"] = (
                sh["employee_comp"] + sh["proprietors"] * prop[tier][y]
                + sh["transfers"] * trans[tier][y])
        row["ownership_origin_current_resource_share_mid"] = (
            sh["proprietors"] * (1 - prop["mid"][y]) + sh["rental"]
            + sh["interest"] + sh["dividends"])
        row["fiscal_nonlabor_or_unresolved_current_resource_share_mid"] = (
            sh["transfers"] * (1 - trans["mid"][y]))
        df9_rows.append(row)
    df9 = {r["year"]: r for r in df9_rows}

    # DF10: timing slice + centrals + capacity bounds.
    df10_rows = []
    for y in YEARS:
        pce = f(b0[y], "pce") if y >= 1960 else f(pd50[y], "pce_b")
        dpi = f(b0[y], "dpi") if y >= 1960 else f(pd50[y], "dpi_b")
        T = f(df8[y], "minimum_intertemporal_share_pce_headline")
        T_hi = f(df8[y], "weak_upper")
        r9 = df9[y]
        ll = r9["labor_origin_current_resource_share_low"]
        lh = r9["labor_origin_current_resource_share_high"]
        df10_rows.append({
            "year": y,
            "pce_b": pce, "dpi_b": dpi,
            "minimum_intertemporal_share_pce": T,
            "current_labor_origin_share_pce_central": (1 - T) * r9["labor_origin_current_resource_share_mid"],
            "current_ownership_property_origin_share_pce_central": (1 - T) * r9["ownership_origin_current_resource_share_mid"],
            "current_fiscal_nonlabor_unresolved_share_pce_central": (1 - T) * r9["fiscal_nonlabor_or_unresolved_current_resource_share_mid"],
            "labor_financing_capacity_lower_share_pce": max(0.0, (1 - T_hi) * pce - (1 - ll) * dpi) / pce,
            "labor_financing_capacity_upper_share_pce": min(lh * dpi, pce) / pce,
            "tier": "STRONG_TIMING" if df8[y]["tier"].startswith("STRONG") else "WEAK",
        })
    return df9_rows, df10_rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df9_rows, df10_rows = build()
    for name, rows in [("DF9_rebuilt_1950_2025.csv", df9_rows),
                       ("DF10_rebuilt_1950_2025.csv", df10_rows)]:
        with open(OUT / name, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    # The known-discrepancy report: archived vs rebuilt upper, 1958-1979.
    arch10 = load(V28DF / "DF10_full_pce_financing_ledger_strong_weak_1950_2025.csv")
    with open(OUT / "DF10_upper_1958_1979_discrepancy.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "archived_upper", "rebuilt_upper", "rebuilt_minus_archived_pp"])
        for r in df10_rows:
            y = r["year"]
            if 1958 <= y <= 1979:
                a = f(arch10[y], "labor_financing_capacity_upper_share_pce")
                b = r["labor_financing_capacity_upper_share_pce"]
                w.writerow([y, a, b, 100 * (b - a)])
    print("wrote DF9_rebuilt, DF10_rebuilt, and the 1958-1979 upper discrepancy report to", OUT)


if __name__ == "__main__":
    main()
