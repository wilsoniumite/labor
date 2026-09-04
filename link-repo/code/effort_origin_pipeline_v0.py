"""
effort_origin_pipeline_v0.py

Scaffold for the effort-origin accounting project.

This file deliberately separates:
  (1) official accounting flows,
  (2) observed proxy series,
  (3) model/specification mappings.

It does NOT yet force all non-wage income into effort/capital/rent buckets.
Unknown components remain unresolved.

Designed to live beside lambda_compute2.py and reuse its FRED pull/annualize
helpers when run in the original project environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Iterable, Mapping

import numpy as np
import pandas as pd

try:
    from lambda_compute2 import pull_fred, annualize
except ImportError:
    pull_fred = None
    annualize = None


# ---------------------------------------------------------------------
# 0. Source registry
# ---------------------------------------------------------------------

# Existing NIPA / fiscal sources already used in lambda_compute2.py.
PRIMARY_INCOME_SERIES = {
    "wages": "A576RC1",
    "supplements": "A038RC1A027NBEA",
    "proprietors": "A041RC1A027NBEA",
    "rental": "A048RC1A027NBEA",
    "interest": "A064RC1A027NBEA",
    "dividends": "B703RC1A027NBEA",
    "social_benefits": "A063RC1A027NBEA",
    "social_contribs": "A061RC1A027NBEA",
    "personal_taxes": "W055RC1A027NBEA",
    "pce": "PCECA",
}

# Bridge between income and consumption.
BRIDGE_SERIES = {
    # BEA Table 2.1
    "personal_saving": "A071RC1A027NBEA",

    # BEA private saving / retained corporate earnings
    "undistributed_corp_profits": "B057RC1A027NBEA",

    # Federal Reserve Financial Accounts, household + nonprofit sector
    "hh_net_lending_financial": "BOGZ1FU155000005A",
    "hh_loan_incurrence": "BOGZ1FA154123005A",

    # Existing government current-account bridge
    "gov_receipts": "GRECPT",
    "gov_expenditures": "GEXPND",
}

# System-effort proxies.
PROXY_FRED_SERIES = {
    # Finance: output per labor hour; inverse is a labor-requirement index.
    "commercial_banking_labor_productivity": "IPUKN522110L000000000",

    # Asset-management / investment-intermediation human hours.
    "investment_activity_hours_millions": "IPUKN5239L200000000",

    # Rental-property system effort.
    "real_estate_lessor_hours_index": "IPULN5311L010000000",
    "real_estate_services_employment_thousands": "IPULN5313W200000000",
}

# Sparse directly observed anchors. Do not silently interpolate these.
ICI_INDEX_SHARE = pd.Series(
    {2010: 0.19, 2015: 0.28, 2020: 0.40, 2024: 0.51},
    name="index_share_long_term_fund_assets",
)
ICI_INDEX_SHARE.attrs["source"] = (
    "Investment Company Institute, 2025 research perspective / Figure 5"
)
ICI_INDEX_SHARE.attrs["definition"] = (
    "Index mutual funds + index ETFs as share of long-term mutual fund and ETF assets"
)

RHFS_WAVES = (2015, 2018, 2021, 2024)


# ---------------------------------------------------------------------
# 1. Utility helpers
# ---------------------------------------------------------------------

def _require_pull_helpers() -> None:
    if pull_fred is None or annualize is None:
        raise RuntimeError(
            "Run this file beside lambda_compute2.py so pull_fred/annualize are available."
        )


def fetch_registry(registry: Mapping[str, str]) -> Dict[str, pd.Series]:
    """
    Pull and annualize a registry of FRED series.

    Returns only successful series and never substitutes alternatives.
    """
    _require_pull_helpers()
    out: Dict[str, pd.Series] = {}
    for name, sid in registry.items():
        s = pull_fred(sid)
        if s is None:
            print(f"MISS {name:40s} {sid}")
            continue
        a = annualize(s)
        out[name] = a
        print(
            f"OK   {name:40s} {sid:24s} "
            f"{int(a.index.min())}-{int(a.index.max())}"
        )
    return out


def common_years(series: Mapping[str, pd.Series], start: int | None = None) -> list[int]:
    years = None
    for s in series.values():
        yy = set(int(y) for y in s.index)
        years = yy if years is None else years & yy
    ans = sorted(years or [])
    if start is not None:
        ans = [y for y in ans if y >= start]
    return ans


def normalize_index(s: pd.Series, base_year: int) -> pd.Series:
    if base_year not in s.index:
        raise KeyError(f"base year {base_year} missing")
    return 100.0 * s / float(s.loc[base_year])


def inverse_productivity_index(prod: pd.Series, base_year: int | None = None) -> pd.Series:
    """
    A simple system-effort proxy: labor requirement per unit output is proportional
    to 1 / output-per-hour.

    If base_year is supplied, normalize labor requirement to 100 in that year.
    """
    req = 1.0 / prod.astype(float)
    if base_year is not None:
        req = normalize_index(req, base_year)
    return req.rename("labor_requirement_index")


def check_exhaustive_shares(df: pd.DataFrame, cols: Iterable[str], tol: float = 1e-8) -> None:
    total = df[list(cols)].sum(axis=1)
    bad = total[(total - 1.0).abs() > tol]
    if len(bad):
        raise AssertionError(
            f"share identity failed in {len(bad)} years; max error "
            f"{float((total - 1.0).abs().max()):.3g}"
        )


# ---------------------------------------------------------------------
# 2. Baseline legal-income assembly
# ---------------------------------------------------------------------

def legal_income_frame(data: Mapping[str, pd.Series], start: int = 1960) -> pd.DataFrame:
    """
    Assemble the legal-form income flows only.

    No economic reclassification is performed here.
    Transfers remain visible rather than being treated as primary income.
    """
    keys = [
        "wages", "supplements", "proprietors",
        "rental", "interest", "dividends", "social_benefits",
    ]
    missing = [k for k in keys if k not in data]
    if missing:
        raise KeyError(f"missing legal-income inputs: {missing}")

    years = common_years({k: data[k] for k in keys}, start=start)
    df = pd.DataFrame(index=years)
    for k in keys:
        df[k] = data[k].loc[years].astype(float)

    df["employee_comp"] = df["wages"] + df["supplements"]
    df["primary_legal_total"] = (
        df["employee_comp"]
        + df["proprietors"]
        + df["rental"]
        + df["interest"]
        + df["dividends"]
    )
    df["resources_before_tax_adjustment"] = (
        df["primary_legal_total"] + df["social_benefits"]
    )
    return df


# ---------------------------------------------------------------------
# 3. Economic-origin mapping (deliberately unresolved-first)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class OriginShares:
    effort: float
    produced_capital: float
    scarcity_rent: float
    unresolved: float

    def validate(self, name: str = "") -> None:
        vals = np.array(
            [self.effort, self.produced_capital, self.scarcity_rent, self.unresolved],
            dtype=float,
        )
        if (vals < -1e-12).any():
            raise ValueError(f"{name}: negative origin share")
        if abs(float(vals.sum()) - 1.0) > 1e-10:
            raise ValueError(f"{name}: origin shares sum to {vals.sum()}, not 1")


def decompose_flow(flow: pd.Series, shares: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """
    Apply time-varying origin shares to one legal income flow.

    Required shares columns:
      effort, produced_capital, scarcity_rent, unresolved

    The caller is responsible for constructing shares from observed proxies.
    """
    cols = ["effort", "produced_capital", "scarcity_rent", "unresolved"]
    if not set(cols).issubset(shares.columns):
        raise KeyError(f"shares must contain {cols}")

    idx = flow.index.intersection(shares.index)
    sh = shares.loc[idx, cols].astype(float)
    err = (sh.sum(axis=1) - 1.0).abs()
    if float(err.max()) > 1e-8:
        raise AssertionError(f"{prefix}: origin-share identity fails; max={err.max()}")

    out = pd.DataFrame(index=idx)
    for c in cols:
        out[f"{prefix}_{c}"] = flow.loc[idx].astype(float) * sh[c]
    return out


# ---------------------------------------------------------------------
# 4. Bridge assembly
# ---------------------------------------------------------------------

def bridge_frame(
    primary: Mapping[str, pd.Series],
    bridge: Mapping[str, pd.Series],
    start: int = 1960,
) -> pd.DataFrame:
    """
    Build observed pieces connecting current income generation to consumption.

    We keep NIPA saving, Flow-of-Funds net lending, and loan incurrence side-by-side.
    They are not interchangeable and should not be algebraically forced to match
    without first reconciling sector definitions and capital-account adjustments.
    """
    required = ["pce", "personal_saving", "undistributed_corp_profits",
                "hh_net_lending_financial", "hh_loan_incurrence"]
    allseries = {
        "pce": primary["pce"],
        **{k: bridge[k] for k in required if k != "pce" and k in bridge},
    }
    missing = [k for k in required if k not in allseries]
    if missing:
        raise KeyError(f"missing bridge inputs: {missing}")

    years = common_years(allseries, start=start)
    df = pd.DataFrame(index=years)
    for k, s in allseries.items():
        df[k] = s.loc[years].astype(float)

    # Ratios are descriptive; do not treat them as accounting identities.
    df["personal_saving_over_pce"] = df["personal_saving"] / df["pce"]
    df["hh_loan_incurrence_over_pce"] = (
        # Flow-of-Funds series is in $ millions; NIPA PCE is generally $ billions.
        (df["hh_loan_incurrence"] / 1000.0) / df["pce"]
    )
    df["hh_net_lending_over_pce"] = (
        (df["hh_net_lending_financial"] / 1000.0) / df["pce"]
    )
    df["undistributed_corp_profits_over_pce"] = (
        df["undistributed_corp_profits"] / df["pce"]
    )
    return df


# ---------------------------------------------------------------------
# 5. Proxy outputs
# ---------------------------------------------------------------------

def equity_proxy_frame(proxy_data: Mapping[str, pd.Series]) -> pd.DataFrame:
    """
    Assemble observed equity-management proxies without inventing an effort mapping.

    `index_share` is recipient/strategy evidence.
    `investment_activity_hours` is system-effort evidence.
    A defensible AUM denominator must be attached before calling hours-per-AUM.
    """
    df = pd.DataFrame(index=sorted(
        set(ICI_INDEX_SHARE.index)
        | set(proxy_data.get("investment_activity_hours_millions", pd.Series(dtype=float)).index)
    ))
    df["index_share"] = ICI_INDEX_SHARE
    if "investment_activity_hours_millions" in proxy_data:
        df["investment_activity_hours_millions"] = proxy_data[
            "investment_activity_hours_millions"
        ]
    return df


def credit_proxy_frame(proxy_data: Mapping[str, pd.Series]) -> pd.DataFrame:
    prod = proxy_data["commercial_banking_labor_productivity"].dropna()
    out = pd.DataFrame(index=prod.index)
    out["bank_labor_productivity"] = prod
    out["bank_labor_requirement_1987_100"] = inverse_productivity_index(
        prod, base_year=int(prod.index.min())
    )
    return out


# ---------------------------------------------------------------------
# 6. Main scaffold
# ---------------------------------------------------------------------

def main() -> None:
    primary = fetch_registry(PRIMARY_INCOME_SERIES)
    bridge = fetch_registry(BRIDGE_SERIES)
    proxies = fetch_registry(PROXY_FRED_SERIES)

    os.makedirs("effort_data", exist_ok=True)

    legal = legal_income_frame(primary)
    legal.to_csv("effort_data/legal_income_baseline.csv")

    bridge_df = bridge_frame(primary, bridge)
    bridge_df.to_csv("effort_data/intermediation_bridge.csv")

    eq = equity_proxy_frame(proxies)
    eq.to_csv("effort_data/equity_proxy_observations.csv")

    credit = credit_proxy_frame(proxies)
    credit.to_csv("effort_data/credit_proxy_observations.csv")

    print("\nWrote v0 accounting/proxy datasets.")
    print("Next module: RHFS rental management 2015/2018/2021/2024.")
    print("No ultimate-origin graph is produced yet: unresolved mappings are intentional.")


if __name__ == "__main__":
    main()
