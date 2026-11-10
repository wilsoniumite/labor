# one_basis_tables.py — the stored tables code/one_basis.py writes and the two it is set beside, read without the BEA
# files: for the figures, the decile account and anything else that only needs the results.

import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
EFFORT = os.path.join(REPO, "pinning", "effort", "archive_v28")


def made(basis="domp", depreciation="central"):
    """What consumption is made of, by year (data/one_basis.csv)."""
    d = pd.read_csv(os.path.join(ROOT, "data", "one_basis.csv"))
    return d[(d.basis == basis) & (d.depreciation == depreciation)].set_index("year")


def financing():
    """The financing account's modern panel (2004-2023): labour-origin share of consumption, its bounds, and the share
    spent beyond current income."""
    d = pd.read_csv(os.path.join(EFFORT, "expected", "DF19_FINAL_modern_DF_panel_2004_2023.csv"))
    return d.set_index("year").rename(columns={"labor_financing_weak_central_share_pce": "fin_labour",
                                               "labor_financing_source_free_lower_share_pce": "fin_lower",
                                               "labor_financing_source_free_upper_share_pce": "fin_upper",
                                               "hard_minimum_intertemporal_share_pce": "fin_beyond_income"})[
        ["fin_labour", "fin_lower", "fin_upper", "fin_beyond_income"]]


def published():
    """BEA WP2026-01's own grouping of the consumption dollar, as digitized for the production account."""
    d = pd.read_csv(os.path.join(EFFORT, "inputs", "dq",
                                 "D_Q11_bea_wp2026_fullchain_consumption_grouped_1997_2023_digitized.csv")).set_index("year")
    return d[["human_effort_share", "domestic_capital_total_share", "foreign_content_share"]]
