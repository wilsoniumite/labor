# run_fi.py - the post's Finnish exercise rebuilt (HBS 2022 income quintiles, Figures 1-3): every judgment call
# re-derived against the published numbers, the constants in bridge.py asserted, and the Finnish outputs written.
#
# Run from the repo root:  venv/bin/python -I consumption/rebuild/code/run_fi.py
# Outputs (consumption/rebuild/out/): fi_accounting_by_quintile.csv, fi_demand_shifts.csv, fi_decomposition_top10.csv,
#   fi_flags.csv, fi_mpc_schedules.csv, fi_eta.csv (the deliverables), plus the evidence for each call:
#   fi_units_tests.csv, fi_budget_tests.csv, fi_base_tests.csv, fi_flags_search.csv, fi_mapping_tests.csv,
#   fi_mpc_tests.csv, fi_mpc_fit_surface.csv, fi_impulse.csv, fi_convention_compare.csv.
# Figure (consumption/rebuild/figures/): fig2_rebuilt.png.
# Gate: consumption/rebuild/checks/gate_fi.py. Write-up: consumption/rebuild/NOTES_fi.md.
# Plain functions plus top-level code; each %% block pastes into a notebook cell.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import itertools

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

import bridge as B

OUT = B.REBUILD / "out"
FIG = B.REBUILD / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
Q = B.FI_Q
GATE = pd.read_csv(B.TIDY / "post_published_numbers.csv")
pd.set_option("display.width", 220)


def gate_value(pid):
    return float(GATE.loc[GATE["id"] == pid, "value"].iloc[0])


# %% published targets (ids from post_published_numbers.csv)
F1 = "fig1_net_transfer_fi2022.png"
F2 = "fig2_demand_shifts_fi2022_mpc.png"
F3 = "fig3_composition_shift_fi2022_mpc.png"
PUB_NET = pd.Series([gate_value(p) for p in ["P080", "P083", "P085", "P087", "P089"]], index=Q)
PUB_PCT = pd.Series([gate_value(p) for p in ["P081", "P084", "P086", "P088", "P090"]], index=Q)
PUB_X = pd.Series([gate_value(f"P{i:03d}") for i in range(92, 97)], index=Q)          # point positions, +/-3
PUB_DIV, PUB_BREAK = gate_value("P079"), gate_value("P097")
PUB_Q1_SHARE, PUB_AVG_BUDGET = gate_value("P104"), gate_value("P116")
_f2 = GATE[GATE["source"] == F2]
PUB2 = pd.DataFrame({
    "pub_eur": _f2[_f2["quantity"].str.startswith("change in spending per adult share")].set_index("item")["value"],
    "pub_pct": _f2[_f2["quantity"].str.startswith("percent change in category spending")].set_index("item")["value"],
    "pub_ghost": _f2[_f2["quantity"] == "MPC=1 benchmark (ghost) value"].set_index("item")["value"]})
PUB2 = PUB2.loc[_f2[_f2["quantity"].str.startswith("change in spending")]["item"]]      # figure order, top to bottom
_f3 = GATE[GATE["source"] == F3]
_seg = _f3[_f3["quantity"].str.startswith("quintile contribution")].copy()
_seg["q"] = _seg["group"].str.replace("FI ", "").str.lower()
PUB3 = _seg.pivot(index="item", columns="q", values="value")[Q]
PUB3_NET = _f3[_f3["quantity"].str.startswith("change in spending")].set_index("item")["value"]
PUB3_GHOST = _f3[_f3["quantity"] == "MPC=1 benchmark (ghost) value"].set_index("item")["value"]
PUB3_ORDER = list(PUB3_NET.index)

m = B.build_fi_model()                      # post convention, 12ew pair-averaged composition, food system F3
assert set(PUB2.index) == set(m["chart"]), set(PUB2.index) ^ set(m["chart"])
CH = list(PUB2.index)
MID = B.fi_mpc_mid()
print(f"HBS 2022 quintiles: {len(m['C'])} budget categories ({len(CH)} charted); post-convention budget "
      f"EUR {m['budget_bar']:.2f} (weighted) / {m['budget_bar_post']:.2f} (total column) per share-month")


# %% scoring helpers shared by the steps
S_LAB, S_X, S_PCT, S_SH = 0.5 / np.sqrt(3), 3 / np.sqrt(3), 0.05 / np.sqrt(3), 0.5 / np.sqrt(3)


def fig1_objective(x, net, div, pct, share1):
    """Chi-square-like distance to Fig 1 (rounding noise as uniform errors): net labels, dividend, point positions,
    percent-of-budget labels, and the Q1 VAT-able share (59%). Arrays may be 2-D (combinations x quintiles)."""
    x, net, pct = np.atleast_2d(x), np.atleast_2d(net), np.atleast_2d(pct)
    return ((((net - PUB_NET.values) / S_LAB) ** 2).sum(1) + ((np.asarray(div) - PUB_DIV) / S_LAB) ** 2
            + (((x - PUB_X.values) / S_X) ** 2).sum(1) + (((pct - PUB_PCT.values) / S_PCT) ** 2).sum(1)
            + ((np.asarray(share1) - PUB_Q1_SHARE) / S_SH) ** 2)


FLAG_GRID = {
    "maintenance charges of housing companies": [0.0, 1.0],
    "used cars": [0.0, 0.5, 1.0],
    "driving lessons, tests, licences": [0.0, 1.0],
    "international air transport": [0.0, 1.0],
    "sea and inland-waterway transport": [0.0, 1.0],
    "letter post": [0.0, 1.0],
    "games of chance": [0.0, 1.0],
    "package holidays": [0.0, 1.0],
    "religious services": [0.0, 1.0],
    "other services n.e.c.": [0.0, 0.5, 1.0],
    "13.3 Social protection (off-chart)": [0.0, 1.0],
    "77 Consumption abroad (off-chart)": [0.0, 1.0],
    "domestic services by paid staff": [0.0, 1.0],
}


def flag_search(mm, grid=FLAG_GRID, base_flags=None, inclusive=True, chunk=50000, desc="VAT flags"):
    """Score every combination of grid values (other lines at base_flags) against Fig 1 under model mm's weights
    and budgets; returns all combinations sorted by the objective."""
    base_flags = B.fi_vat_flags() if base_flags is None else base_flags
    L = mm["lines"]
    if not inclusive:
        L = L.div(1.0 + mm["line_meta"]["rate"].reindex(L.index), axis=0)
    keys = list(grid)
    fixed = [k for k in L.index if k not in grid]
    v0 = L.loc[fixed].mul(pd.Series(base_flags).reindex(fixed), axis=0).sum().values
    M = L.loc[keys].values
    w, bud = mm["w"].values, mm["budget"].values
    combos = np.array(list(itertools.product(*[grid[k] for k in keys])), dtype=float)
    res = []
    for a in tqdm(range(0, len(combos), chunk), desc=desc, leave=False):
        cb = combos[a:a + chunk]
        x = v0[None, :] + cb @ M
        cbar = x @ w
        net = B.TAU * (cbar[:, None] - x)
        div = B.TAU * cbar
        pct = 100 * net / bud[None, :]
        if inclusive:
            sh = 100 * x / bud[None, :]
        else:                                         # report the tax-inclusive VAT-able share for the same flags
            Li = mm["lines"]
            xi = Li.loc[fixed].mul(pd.Series(base_flags).reindex(fixed), axis=0).sum().values[None, :] + cb @ Li.loc[keys].values
            sh = 100 * xi / bud[None, :]
        r = pd.DataFrame(cb, columns=keys)
        r["objective"] = fig1_objective(x, net, div, pct, sh[:, 0])
        r["dividend"] = div
        for i, q in enumerate(Q):
            r[f"net_{q}"], r[f"x_{q}"], r[f"pct_{q}"] = net[:, i], x[:, i], pct[:, i]
        r["vatable_share_q1"], r["vatable_share_q5"] = sh[:, 0], sh[:, 4]
        r["labels_exact"] = (np.round(net) == PUB_NET.values).sum(1)
        r["pct_exact"] = (np.round(pct, 1) == PUB_PCT.values).sum(1)
        res.append(r)
    return pd.DataFrame(pd.concat(res, ignore_index=True)).sort_values("objective").reset_index(drop=True)


def demand_post(mm, net, mpc):
    """Fig 2/3 quantities in the post's units: dPct (system), dEUR on the post's EUR conversion (total column),
    ghost (MPC=1) in post EUR, and the quintile segments in post EUR."""
    sh = B.shifts_from_transfers(mm, net, mpc=mpc)
    eur = B.fi_post_eur(mm, sh["dUSD_mpc"])
    ghost = B.fi_post_eur(mm, sh["dUSD_mpc1"])
    seg = B.fi_post_eur(mm, B.decompose(mm, B.budget_shock(net, mpc, mm["budget"])))
    seg1 = B.fi_post_eur(mm, B.decompose(mm, B.budget_shock(net, np.ones(5), mm["budget"])))
    return dict(eur=eur, pct=sh["dPct_mpc"], ghost=ghost, ghost_pct=sh["dPct_mpc1"], seg=seg, seg1=seg1, shifts=sh)


def rmse(a):
    a = np.asarray(a, dtype=float)
    return float(np.sqrt(np.nanmean(a ** 2)))


def implied_cbar():
    """Category means implied by the Fig 2 labels: EUR / percent, with rounding bounds; well identified when both
    labels are at least 0.05 EUR and 0.25%."""
    e, p = PUB2["pub_eur"], PUB2["pub_pct"]
    lo = (e.abs() - 0.005) / ((p.abs() + 0.005) / 100)
    hi = (e.abs() + 0.005) / ((p.abs() - 0.005) / 100)
    ok = (e.abs() >= 0.05) & (p.abs() >= 0.25)
    return pd.DataFrame({"impl": e / (p / 100), "lo": lo, "hi": hi, "ok": ok})


CB = implied_cbar()


def units_scores(mm, label):
    """Flag-independent tests of a units variant, plus its best Fig 1 fit over the flag grid."""
    bud = mm["budget"]
    lo = 100 * (PUB_NET.abs() - 0.5) / (PUB_PCT.abs() + 0.05)          # budgets the printed net and percent allow
    hi = 100 * (PUB_NET.abs() + 0.5) / (PUB_PCT.abs() - 0.05)
    in_rng = int(((bud >= lo) & (bud <= hi)).sum())
    cb = mm["Cbar_post"].reindex(CB.index)
    ok = CB["ok"]
    z = ((cb - CB["impl"]) / ((CB["hi"] - CB["lo"]) / (2 * np.sqrt(3))))[ok]
    in_cb = int(((cb >= CB["lo"]) & (cb <= CB["hi"]))[ok].sum())
    d = demand_post(mm, PUB_NET, MID)
    fs = flag_search(mm, desc=f"flags ({label})")
    b = fs.iloc[0]
    return dict(variant=label, budget_q1=bud["q1"], budget_q2=bud["q2"], budget_q5=bud["q5"],
                budgets_in_fig1_range=in_rng, avg_budget_eur_conversion=mm["budget_bar_post"],
                avg_budget_weighted=mm["budget_bar"], cbar_chi2=float((z ** 2).sum()),
                cbar_in_rounding=f"{in_cb}/{int(ok.sum())}",
                ghost_rmse_pub_nets=rmse(d["ghost"].loc[CH] - PUB2["pub_ghost"]),
                pct_rmse_pub_nets=rmse(d["pct"].loc[CH] - PUB2["pub_pct"]),
                seg_rmse_pub_nets=rmse((d["seg"].loc[PUB3.index] - PUB3).values),
                best_flag_objective=float(b["objective"]), best_dividend=float(b["dividend"]),
                best_labels_exact=int(b["labels_exact"]), best_pct_exact=int(b["pct_exact"]))


# %% step 1: units - composition route (payment shares), per-CU -> per-share conversion and population weights.
# Flag-independent tests: the five budgets the Fig 1 percent labels imply, the 'EUR 2,051' average, the category
# means implied by the Fig 2 EUR/percent label pairs, and the ghosts/segments with the published nets as the net
# vector; then each variant's best Fig 1 fit over the whole flag grid.
UNIT_VARIANTS = [
    ("post: 12ew pair means, r_q, equal-CU weights (adopted)", dict()),
    ("post: 12ew pairs pooled", dict(composition="12ew_pooled")),
    ("post: 12ew pair means, 'other households' two adults", dict(composition="12ew_two_adults")),
    ("post conventions on the 14qa composition (consistent route)", dict(composition="14qa")),
    ("post, equal-HOUSEHOLD weights", dict(weights="equal_households")),
    ("post, CU per household from 14qa means", dict(cu_per_household="14qa_mean")),
    ("post, CU per household implied by 12ew adults/children", dict(cu_per_household="route")),
    ("post, EUR conversion from the weighted mean (no total column)", dict(_eur="weighted")),
    ("coherent: per-household table, equal-household weights, 12ew", dict(convention="coherent")),
    ("coherent: per-household table, equal-household weights, 14qa", dict(convention="coherent", composition="14qa")),
]
rows = []
for name, kw in tqdm(UNIT_VARIANTS, desc="units variants", leave=False):
    mm = B.build_fi_model(**{k: v for k, v in kw.items() if not k.startswith("_")})
    if kw.get("_eur") == "weighted":           # the system's own weighted mean instead of the total column
        mm = dict(mm, Cbar_post=mm["Cbar"], eur_scale=mm["Cbar"] / mm["Cbar"], budget_bar_post=mm["budget_bar"])
    rows.append(units_scores(mm, name))
units_tests = pd.DataFrame(rows)
units_tests.to_csv(OUT / "fi_units_tests.csv", index=False, float_format="%.4f")
print("\nstep 1, units (budgets in Fig 1 range of 5; EUR 2,051; category means; best Fig 1 objective over the flag grid):")
print(units_tests[["variant", "budgets_in_fig1_range", "avg_budget_eur_conversion", "cbar_chi2", "cbar_in_rounding",
                   "ghost_rmse_pub_nets", "best_flag_objective", "best_dividend", "best_labels_exact",
                   "best_pct_exact"]].round(3).to_string(index=False))
ut = units_tests.set_index("variant")
ADOPTED_UNITS = UNIT_VARIANTS[0][0]
assert ut["best_flag_objective"].idxmin() == ADOPTED_UNITS, ut["best_flag_objective"].idxmin()
assert ut.loc[ADOPTED_UNITS, "cbar_chi2"] <= ut["cbar_chi2"].min() + 1e-9
assert ut.loc[ADOPTED_UNITS, "budgets_in_fig1_range"] >= 4


# %% step 2: budget rows (which categories make up the per-share budget B_q). Nets do not depend on them; the
# percent labels, the VAT-able shares, the 2,051 average and the elasticities (through w) do.
code_of = {c["cat"]: c["code"] for c in B.FI_CATEGORIES}
BUDGET_ALTS = {"all consumption, incl. imputed rent, interest, education, abroad (adopted)": [],
               "minus consumption abroad (77)": ["77"],
               "minus imputed rent and interest (nothing transacted)": ["042", "046"],
               "minus imputed rent, interest, education, abroad": ["042", "046", "10", "77"],
               "minus education": ["10"]}
flags_adopted = B.fi_vat_flags()
rows = []
for name, drop in BUDGET_ALTS.items():
    cats = [c for c in B.FI_CATEGORIES if c["code"] not in drop]
    mm = B.build_fi_model(cats=cats)
    fl = {k: v for k, v in flags_adopted.items() if k in mm["lines"].index}
    acc = B.fi_vat_accounting(mm, fl)
    d = demand_post(mm, acc["net"], MID)
    rows.append(dict(budget=name, **{f"pct_{q}": acc["net_pct_budget"][q] for q in Q},
                     pct_exact=int((np.round(acc["net_pct_budget"], 1) == PUB_PCT).sum()),
                     vatable_share_q1=acc["vatable_pct_budget"]["q1"], vatable_share_q5=acc["vatable_pct_budget"]["q5"],
                     avg_budget_eur_conversion=mm["budget_bar_post"], dividend=float(acc["dividend"].iloc[0]),
                     ghost_rmse=rmse(d["ghost"].loc[CH] - PUB2["pub_ghost"]), bars_rmse=rmse(d["eur"].loc[CH] - PUB2["pub_eur"]),
                     eta_food_q1=mm["eta"].loc["01.1 Food (at home)", "q1"], eta_food_q5=mm["eta"].loc["01.1 Food (at home)", "q5"]))
budget_tests = pd.DataFrame(rows)
budget_tests.to_csv(OUT / "fi_budget_tests.csv", index=False, float_format="%.4f")
print("\nstep 2, budget rows (published % 5.9 2.4 0.2 -0.7 -3.1; Q1 VAT-able 59%; average EUR 2,051):")
print(budget_tests[["budget", "pct_q1", "pct_q2", "pct_q5", "pct_exact", "vatable_share_q1", "avg_budget_eur_conversion",
                    "ghost_rmse", "bars_rmse"]].round(3).to_string(index=False))
bt = budget_tests.set_index("budget")
assert bt["pct_exact"].idxmax() == list(BUDGET_ALTS)[0] and bt["ghost_rmse"].idxmin() == list(BUDGET_ALTS)[0]


# %% step 3: tax-inclusive or tax-exclusive base. Fig 1's line has slope -0.15 against VAT-able consumption, and
# the text has each adult pay tau x C_i. Read instead as 15 points on the net-of-VAT price, the tax is 0.15 x C /
# (1 + existing rate): run the whole flag grid both ways.
fs_incl = flag_search(m, desc="flags, tax-inclusive")
fs_excl = flag_search(m, inclusive=False, desc="flags, tax-exclusive")
base_tests = pd.DataFrame([
    dict(base="tax-inclusive spending (adopted)", best_objective=fs_incl.iloc[0]["objective"],
         dividend=fs_incl.iloc[0]["dividend"], labels_exact=fs_incl.iloc[0]["labels_exact"],
         max_dividend_over_grid=fs_incl["dividend"].max(), min_dividend_over_grid=fs_incl["dividend"].min()),
    dict(base="tax-exclusive (net-of-VAT price)", best_objective=fs_excl.iloc[0]["objective"],
         dividend=fs_excl.iloc[0]["dividend"], labels_exact=fs_excl.iloc[0]["labels_exact"],
         max_dividend_over_grid=fs_excl["dividend"].max(), min_dividend_over_grid=fs_excl["dividend"].min())])
base_tests.to_csv(OUT / "fi_base_tests.csv", index=False, float_format="%.4f")
print("\nstep 3, base:"); print(base_tests.round(2).to_string(index=False))
assert fs_excl["dividend"].max() < PUB_DIV - 20


# %% step 4: VAT flags. The Finnish-law reading line by line (flag_law) against the grid; Fig 1 picks.
fs = fs_incl
best = fs.iloc[0]
for k in FLAG_GRID:
    assert abs(best[k] - flags_adopted[k]) < 1e-9, (k, best[k], flags_adopted[k])
law = B.fi_vat_flags("law")
whole = dict(flags_adopted)                    # level-2 whole-category reading: every split line of a category alike
for l in B.FI_VAT_LINES:
    whole[l["line"]] = 1.0
for k in ["13.3 Social protection (off-chart)", "77 Consumption abroad (off-chart)"]:
    whole[k] = 0.0


def score_flags(fl, label):
    acc = B.fi_vat_accounting(m, fl)
    o = fig1_objective(acc["vatable"].values, acc["net"].values, float(acc["dividend"].iloc[0]),
                       acc["net_pct_budget"].values, acc["vatable_pct_budget"]["q1"])[0]
    return dict(reading=label, objective=float(o), dividend=float(acc["dividend"].iloc[0]),
                **{f"net_{q}": acc["net"][q] for q in Q}, **{f"pct_{q}": acc["net_pct_budget"][q] for q in Q},
                labels_exact=int((np.round(acc["net"]) == PUB_NET).sum()),
                pct_exact=int((np.round(acc["net_pct_budget"], 1) == PUB_PCT).sum()),
                vatable_share_q1=acc["vatable_pct_budget"]["q1"])


readings = pd.DataFrame([score_flags(flags_adopted, "adopted (grid best)"), score_flags(law, "Finnish law, line by line"),
                         score_flags(whole, "whole COICOP groups (13.9 and 09.8 taxable)")])
top20 = fs.head(20).copy()
top20["grid"] = "top 20 of the grid"
stability = {k: top20[k].value_counts().to_dict() for k in FLAG_GRID}
fs_out = pd.concat([top20, readings.assign(grid="named readings")], ignore_index=True)
fs_out.to_csv(OUT / "fi_flags_search.csv", index=False, float_format="%.4f")
print(f"\nstep 4, VAT flags: {len(fs)} combinations; best objective {best['objective']:.1f} (dividend "
      f"EUR {best['dividend']:.2f}, {int(best['labels_exact'])}/5 net labels, {int(best['pct_exact'])}/5 percent labels)")
print(readings.round(2).to_string(index=False))
print("   value counts across the 20 best combinations:")
for k, v in stability.items():
    print(f"     {k:42s} {v}")


# %% step 5: the accounting tier
acc = B.fi_vat_accounting(m)
NET = acc["net"]
u = m["units"]
acc_out = pd.DataFrame({
    "quintile": Q, "households": u.loc[Q, "households"], "adults_per_household_12ew": u.loc[Q, "adults"],
    "children_per_household_12ew": u.loc[Q, "children"], "payment_shares_per_household": u.loc[Q, "shares"],
    "hh_per_cu_ratio": u.loc[Q, "hh_per_cu_ratio"], "w_equal_cu_weight": m["w"], "budget_eur_month": m["budget"],
    "vatable_eur_month": acc["vatable"], "vatable_pct_budget": acc["vatable_pct_budget"], "tax_eur_month": acc["tax"],
    "dividend_eur_month": acc["dividend"], "net_eur_month": acc["net"], "net_pct_budget": acc["net_pct_budget"],
    "pub_net_label": PUB_NET, "pub_pct_label": PUB_PCT, "pub_x_position": PUB_X})
acc_out["net_gap"] = acc_out["net_eur_month"] - acc_out["pub_net_label"]
acc_out["net_rounds_to_label"] = np.round(acc_out["net_eur_month"]) == acc_out["pub_net_label"]
acc_out["pct_rounds_to_label"] = np.round(acc_out["net_pct_budget"], 1) == acc_out["pub_pct_label"]
# the same flags under equal-household weights and the coherent convention (for the record)
m_eqhh = B.build_fi_model(weights="equal_households")
acc_eqhh = B.fi_vat_accounting(m_eqhh)
acc_out["net_eur_month_if_equal_household_weights"] = acc_eqhh["net"]
acc_out.loc["total"] = {"quintile": "total (12ew total column)", "households": u.loc["total", "households"],
                        "adults_per_household_12ew": u.loc["total", "adults"],
                        "children_per_household_12ew": u.loc["total", "children"],
                        "payment_shares_per_household": u.loc["total", "shares"],
                        "hh_per_cu_ratio": u.loc["total", "hh_per_cu_ratio"], "w_equal_cu_weight": 1.0,
                        "budget_eur_month": m["budget_bar_post"], "dividend_eur_month": float(acc["dividend"].iloc[0])}
acc_out.to_csv(OUT / "fi_accounting_by_quintile.csv", index=False, float_format="%.4f")
DIV = float(acc["dividend"].iloc[0])
print(f"\nstep 5, accounting: dividend EUR {DIV:.2f} (published {PUB_DIV:.0f}); mean VAT-able EUR {acc['Cbar_v'].iloc[0]:.1f} "
      f"(break-even line {PUB_BREAK:.0f}); equal-household weights would give EUR {float(acc_eqhh['dividend'].iloc[0]):.2f}")
print(acc_out.loc[Q, ["quintile", "net_eur_month", "pub_net_label", "net_pct_budget", "pub_pct_label", "vatable_eur_month",
                      "pub_x_position", "vatable_pct_budget"]].round(2).T.to_string(header=False))


# %% step 6: elasticities - parent group, food system and evaluation basis, tested on the MPC-free ghosts; bars at
# the adopted MPC schedule and the Fig 3 segments reported alongside. Adoption rule as in the US: a variant replaces
# the adopted one only if it lowers BOTH the ghost RMSE and the bar RMSE by more than 10%.
def mapping_score(mm, net=None, eta=None, label=""):
    mm2 = dict(mm) if eta is None else dict(mm, eta=eta)
    net = NET if net is None else net
    d = demand_post(mm2, net, MID)
    gg = d["ghost"].loc[CH] - PUB2["pub_ghost"]
    return dict(variant=label, ghost_rmse=rmse(gg), ghost_max_abs=float(gg.abs().max()), worst_ghost=gg.abs().idxmax(),
                bars_rmse=rmse(d["eur"].loc[CH] - PUB2["pub_eur"]), pct_rmse=rmse(d["pct"].loc[CH] - PUB2["pub_pct"]),
                seg_rmse=rmse((d["seg"].loc[PUB3.index] - PUB3).values),
                seg_q1_rmse=rmse(d["seg"].loc[PUB3.index, "q1"] - PUB3["q1"]),
                eta_food_q1=mm2["eta"].loc["01.1 Food (at home)", "q1"], eta_food_q5=mm2["eta"].loc["01.1 Food (at home)", "q5"])


m_hh = B.build_fi_model(convention="coherent")             # per-household budget shares, for the eta-basis test
rows = [mapping_score(m, label="adopted: division parents, food system F3 (01+02+11; 01.2 in B&T), own (per-CU) shares")]
MAP_VARIANTS = [("parents pooled into TB-1929 groups (07+08, 12+13)", dict(eta_parent="usda")),
                ("food F2: 01.2 with the six at-home subgroups", dict(food_map="F2")),
                ("food F4: 01.2 in 'Food other'", dict(food_map="F4")),
                ("food F1: food = 01+02+11.1, accommodation its own 'Other' parent", dict(food_map="F1")),
                ("food F0: no stage-two split", dict(food_map="F0")),
                ("TB-1929 betas back-solved (unrounded)", dict(params=B.usda_params(True)))]
for name, kw in tqdm(MAP_VARIANTS, desc="mapping variants", leave=False):
    rows.append(mapping_score(B.build_fi_model(**kw), label=name))
rows.append(mapping_score(m, eta=m_hh["eta"].loc[m["C"].index], label="eta at per-household budget shares (the text's 0.44)"))
rows.append(mapping_score(m, net=PUB_NET, label="published Fig 1 labels as the net vector"))
map_tests = pd.DataFrame(rows)
map_tests.to_csv(OUT / "fi_mapping_tests.csv", index=False, float_format="%.5f")
print("\nstep 6, elasticity mapping (ghost RMSE drives the choice; bars at the adopted MPC):")
print(map_tests[["variant", "ghost_rmse", "worst_ghost", "bars_rmse", "pct_rmse", "seg_rmse", "eta_food_q1",
                 "eta_food_q5"]].round(4).to_string(index=False))
a0 = map_tests.iloc[0]
better = map_tests.iloc[1:-1][(map_tests.iloc[1:-1]["ghost_rmse"] < 0.9 * a0["ghost_rmse"])
                              & (map_tests.iloc[1:-1]["bars_rmse"] < 0.9 * a0["bars_rmse"])]
assert better.empty, better
assert map_tests.iloc[1:-1]["ghost_rmse"].min() > a0["ghost_rmse"], "a variant fits the ghosts better"

# elasticities table
det = m["eta_detail"]
rows = []
for c in m["C"].index:
    for q in Q:
        r = dict(category=c, code=m["code"][c], quintile=q, role=m["prov"].loc[c, "role"],
                 division=m["prov"].loc[c, "division"], parent=det.loc[c, "parent"], beta=det.loc[c, "beta"],
                 w_parent_share=det.loc[c, f"w_{q}"], eta=m["eta"].loc[c, q], eta_per_household_shares=m_hh["eta"].loc[c, q])
        if det.loc[c, "parent"] == "food system":
            r.update(food_subgroup=det.loc[c, "subgroup"], eta_food_group=det.loc[c, f"etaF_{q}"],
                     w_star_within_food=det.loc[c, f"wstar_{q}"], beta_star=det.loc[c, f"betastar_{q}"])
        rows.append(r)
eta_out = pd.DataFrame(rows)
eta_out.to_csv(OUT / "fi_eta.csv", index=False, float_format="%.5f")


# %% step 7: the MPC schedule. Adopted: the post's decile 'literature schedule' (the US low/mid/high, pinned by Fig 5
# and Fig 7) aggregated to quintiles by decile-pair means, so no Finnish number is used to pin it. Diagnostics: a free
# per-quintile fit to the 37 bars, the per-quintile MPC the Fig 3 segments imply, the decile knee family pair-
# averaged and fitted to the Finnish bars, the quintile knee family, and the US monotone diagnostic pair-averaged.
sched = B.fi_mpc_schedules()
Dq = B.fi_post_eur(m, B.decompose(m, (NET / m["budget"]).values))       # EUR per unit MPC, by category x quintile
Dch = Dq.loc[CH].values
y = PUB2["pub_eur"].values
mpc_free = np.linalg.lstsq(Dch, y, rcond=None)[0]
Dseg = Dq.loc[PUB3.index]
mpc_seg = np.array([float((PUB3[q] * Dseg[q]).sum() / (Dseg[q] ** 2).sum()) for q in Q])
KN = np.round(np.arange(1.0, 9.0001, 0.05), 3)
TP = np.round(np.arange(0.40, 0.65001, 0.0025), 4)
S = np.empty((len(KN), len(TP)))
for i, k in enumerate(tqdm(KN, desc="MPC fit surface (decile knee x top, pair means)", leave=False)):
    P = np.stack([B.mpc_knee(k, t, 10).reshape(5, 2).mean(1) for t in TP], axis=1)
    S[i] = ((Dch @ P - y[:, None]) ** 2).sum(0)
i, j = np.unravel_index(S.argmin(), S.shape)
k_fit, t_fit = float(KN[i]), float(TP[j])
surf = pd.DataFrame([(k, t, S[a, b], np.sqrt(S[a, b] / len(CH))) for a, k in enumerate(KN) for b, t in enumerate(TP)],
                    columns=["decile_knee", "top", "sse", "rmse_eur"])
surf.to_csv(OUT / "fi_mpc_fit_surface.csv", index=False, float_format="%.6f")
KQ = np.round(np.arange(1.0, 5.0001, 0.05), 3)
SQ = np.empty((len(KQ), len(TP)))
for a, k in enumerate(KQ):
    P = np.stack([B.mpc_knee(k, t, 5) for t in TP], axis=1)
    SQ[a] = ((Dch @ P - y[:, None]) ** 2).sum(0)
a_, b_ = np.unravel_index(SQ.argmin(), SQ.shape)
kq_fit, tq_fit = float(KQ[a_]), float(TP[b_])
us_sched = pd.read_csv(OUT / "us_mpc_schedules.csv")
us_mono = us_sched["mpc_mid_monotone_fig5_fig6_diagnostic"].values.reshape(5, 2).mean(1)
bar_rmse = lambda mp: rmse(Dch @ np.asarray(mp) - y)
seg_rmse = lambda mp: rmse((Dseg.values * np.asarray(mp)[None, :] - PUB3.values))
cand = {"adopted: US mid schedule, decile-pair means": sched["mid"].values,
        f"decile knee family fitted to the Finnish bars (knee {k_fit:g}, top {t_fit:g}), pair means":
            B.mpc_knee(k_fit, t_fit, 10).reshape(5, 2).mean(1),
        f"quintile knee family fitted to the bars (knee {kq_fit:g}, top {tq_fit:g})": B.mpc_knee(kq_fit, tq_fit, 5),
        "free per-quintile fit to the 37 bars (diagnostic)": mpc_free,
        "implied by the 50 Fig 3 segments (diagnostic)": mpc_seg,
        "US monotone per-decile diagnostic, pair means": us_mono}
mpc_tests = pd.DataFrame([dict(schedule=k, **{f"mpc_{q}": v[i] for i, q in enumerate(Q)}, bars_rmse=bar_rmse(v),
                               seg_rmse=seg_rmse(v), impulse_pct_charted=np.nan) for k, v in cand.items()])
for r_, (k, v) in enumerate(cand.items()):
    d = demand_post(m, NET, v)
    mpc_tests.loc[r_, "impulse_pct_charted"] = 100 * d["eur"].loc[CH].sum() / m["Cbar_post"].loc[CH].sum()
mpc_tests.to_csv(OUT / "fi_mpc_tests.csv", index=False, float_format="%.5f")
sched_out = pd.DataFrame({"quintile": Q, "mpc_low": sched["low"].values, "mpc_mid": sched["mid"].values,
                          "mpc_high": sched["high"].values,
                          "source": "US decile schedules (bridge.US_MPC_KNEE/TOP), decile-pair means",
                          "mpc_mid_decile_knee_fit_fi_bars_diagnostic": cand[list(cand)[1]],
                          "mpc_free_fit_fi_bars_diagnostic": mpc_free, "mpc_implied_fig3_segments_diagnostic": mpc_seg,
                          "mpc_us_monotone_pair_means_diagnostic": us_mono})
sched_out.to_csv(OUT / "fi_mpc_schedules.csv", index=False, float_format="%.4f")
print("\nstep 7, MPC (bars and segments in post EUR; printing floor of the bars $0.0029):")
print(mpc_tests.round(4).to_string(index=False))
assert bar_rmse(sched["mid"].values) < 2 * bar_rmse(mpc_free)


# %% step 8: demand shifts (mid, low, high, MPC=1) in the post's units, beside the published bars; the coherent
# machinery alongside (its own nets: same flags, equal-household weights, per-household table).
D = {k: demand_post(m, NET, sched[k].values) for k in ["mid", "low", "high"]}
ds = pd.DataFrame({"code": pd.Series(m["code"]), "role": m["prov"]["role"], "division": m["prov"]["division"],
                   "usda": m["prov"]["usda"], "Cbar_post_eur": m["Cbar_post"], "Cbar_weighted_eur": m["Cbar"],
                   "dEUR_mid": D["mid"]["eur"], "dPct_mid": D["mid"]["pct"], "dEUR_low": D["low"]["eur"],
                   "dEUR_high": D["high"]["eur"], "dEUR_mpc1": D["mid"]["ghost"], "dPct_mpc1": D["mid"]["ghost_pct"],
                   "dEUR_mid_weighted_units": D["mid"]["shifts"]["dUSD_mpc"]})
ds = ds.join(PUB2)
ds["gap_eur"] = ds["dEUR_mid"] - ds["pub_eur"]
ds["gap_pct"] = ds["dPct_mid"] - ds["pub_pct"]
ds["gap_ghost"] = ds["dEUR_mpc1"] - ds["pub_ghost"]
m_coh = B.build_fi_model(convention="coherent")
acc_coh = B.fi_vat_accounting(m_coh)
sh_coh = B.shifts_from_transfers(m_coh, acc_coh["net"], mpc=MID)
ds["coherent_Cbar_eur"], ds["coherent_dEUR_mid"] = m_coh["Cbar"], sh_coh["dUSD_mpc"]
ds["coherent_dPct_mid"], ds["coherent_dEUR_mpc1"] = sh_coh["dPct_mpc"], sh_coh["dUSD_mpc1"]
order = CH + [c for c in ds.index if c not in CH]
ds = ds.loc[order]
ds.index.name = "category"
ds.to_csv(OUT / "fi_demand_shifts.csv", float_format="%.5f")
print(f"\nstep 8, Fig 2: bars RMSE EUR {rmse(ds.loc[CH, 'gap_eur']):.4f} (max {ds.loc[CH, 'gap_eur'].abs().max():.4f}, "
      f"{ds.loc[CH, 'gap_eur'].abs().idxmax()}); percent RMSE {rmse(ds.loc[CH, 'gap_pct']):.4f} pp; ghost RMSE "
      f"{rmse(ds.loc[CH, 'gap_ghost']):.4f}; bars within +/-0.005: {(ds.loc[CH, 'gap_eur'].abs() <= 0.005 + 1e-9).sum()}/37")


# %% step 9: quintile decomposition of the ten largest movers (Fig 3)
top10 = B.top_movers(ds.rename(columns={"dEUR_mid": "x"}), "x", CH, 10)
assert set(top10) == set(PUB3_ORDER), (top10, PUB3_ORDER)
top10 = sorted(top10, key=lambda c: -ds.loc[c, "dEUR_mid"])            # the figure lists them by signed value
rows = []
for r_, c in enumerate(top10, 1):
    for q in Q:
        rows.append(dict(rank=r_, category=c, quintile=q, contrib_mid=D["mid"]["seg"].loc[c, q],
                         contrib_mpc1=D["mid"]["seg1"].loc[c, q], pub_segment=PUB3.loc[c, q],
                         gap=D["mid"]["seg"].loc[c, q] - PUB3.loc[c, q]))
    rows.append(dict(rank=r_, category=c, quintile="net", contrib_mid=D["mid"]["seg"].loc[c].sum(),
                     contrib_mpc1=D["mid"]["seg1"].loc[c].sum(), pub_segment=PUB3_NET[c],
                     gap=D["mid"]["seg"].loc[c].sum() - PUB3_NET[c]))
dec_out = pd.DataFrame(rows)
dec_out.to_csv(OUT / "fi_decomposition_top10.csv", index=False, float_format="%.5f")
seg = dec_out[dec_out["quintile"] != "net"]
print(f"step 9, Fig 3: top 10 = the published set (order {'identical' if top10 == PUB3_ORDER else 'differs: ' + str(top10)}); "
      f"segments RMSE EUR {rmse(seg['gap']):.4f}, max |gap| {seg['gap'].abs().max():.3f} "
      f"({seg.loc[seg['gap'].abs().idxmax(), 'category']} {seg.loc[seg['gap'].abs().idxmax(), 'quintile']})")


# %% step 10: the aggregate demand impulse, every way it can be quoted
rows = []
for k in ["low", "mid", "high"]:
    ii = B.impulse(m, NET, sched[k].values)
    eur_all = float(D[k]["eur"].sum())
    eur_ch = float(D[k]["eur"].loc[CH].sum())
    rows.append(dict(schedule=k, convention="post", flow_eur_weighted=ii["flow_usd"], bars_all_eur_post=eur_all,
                     bars_chart_eur_post=eur_ch, budget_eur_post=m["budget_bar_post"],
                     charted_budget_eur_post=float(m["Cbar_post"].loc[CH].sum()),
                     pct_charted_budget=100 * eur_ch / float(m["Cbar_post"].loc[CH].sum()),
                     pct_consumption=100 * eur_all / m["budget_bar_post"],
                     flow_pct_consumption_weighted=ii["flow_pct_consumption"]))
    ic = B.impulse(m_coh, acc_coh["net"], sched[k].values)
    rows.append(dict(schedule=k, convention="coherent", flow_eur_weighted=ic["flow_usd"], bars_all_eur_post=ic["bars_all_usd"],
                     bars_chart_eur_post=ic["bars_chart_usd"], budget_eur_post=ic["budget_usd"],
                     charted_budget_eur_post=ic["charted_budget_usd"], pct_charted_budget=ic["bars_chart_pct_charted"],
                     pct_consumption=100 * ic["bars_all_usd"] / ic["budget_usd"],
                     flow_pct_consumption_weighted=ic["flow_pct_consumption"]))
imp_out = pd.DataFrame(rows)
imp_out.to_csv(OUT / "fi_impulse.csv", index=False, float_format="%.5f")
im = imp_out[(imp_out["schedule"] == "mid") & (imp_out["convention"] == "post")].iloc[0]
print(f"step 10, impulse (mid, post units): charted bars EUR {im['bars_chart_eur_post']:.3f} = {im['pct_charted_budget']:.3f}% "
      f"of the charted budget (text '+0.4% of charted budget'); all bars {im['pct_consumption']:.3f}% of consumption")


# %% step 11: flags table (line, category, law reading, adopted flag, what pinned it)
PINNED = {k: "Fig 1 (net labels, dividend, positions, percent labels, Q1 59%): grid best; "
             f"value counts across the 20 best: {stability[k]}" for k in FLAG_GRID}
lm = m["line_meta"]
rows = []
for ln in m["lines"].index:
    rows.append(dict(line=ln, category=lm.loc[ln, "cat"], coicop=lm.loc[ln, "code"], hbs_codes=lm.loc[ln, "codes"],
                     flag_law=lm.loc[ln, "flag_law"], vat_flag=flags_adopted[ln],
                     adopted_vs_law=("same" if flags_adopted[ln] == lm.loc[ln, "flag_law"] else
                                     "the post's whole-group reading, pinned by Fig 1 (law: "
                                     f"{lm.loc[ln, 'flag_law']:g})"), existing_rate=lm.loc[ln, "rate"],
                     reason=lm.loc[ln, "reason"],
                     pinned_by=PINNED.get(ln, "not a judgment line (law and the post's grouping agree)"),
                     eur_month_total_column=m["lines_total"][ln], vatable_eur_month_total_column=flags_adopted[ln] * m["lines_total"][ln],
                     **{f"eur_month_{q}": m["lines"].loc[ln, q] for q in Q}))
flags_out = pd.DataFrame(rows)
flags_out.to_csv(OUT / "fi_flags.csv", index=False, float_format="%.4f")


# %% step 12: the post's conventions against the coherent machinery (what the LVT step should know)
def headline(mm, label, eur_post=True):
    a = B.fi_vat_accounting(mm)
    sh_ = B.shifts_from_transfers(mm, a["net"], mpc=MID)
    ii = B.impulse(mm, a["net"], MID)
    eur = B.fi_post_eur(mm, sh_["dUSD_mpc"]) if eur_post else sh_["dUSD_mpc"]
    cb = mm["Cbar_post"] if eur_post else mm["Cbar"]
    t10 = B.top_movers(pd.DataFrame({"x": eur}), "x", mm["chart"], 10)
    return dict(variant=label, dividend=float(a["dividend"].iloc[0]), **{f"net_{q}": a["net"][q] for q in Q},
                **{f"pct_{q}": a["net_pct_budget"][q] for q in Q}, avg_budget=float(cb.sum()),
                rent=eur["04.1 Actual rents"], food=eur["01.1 Food (at home)"], vehicles=eur["07.1 Purchase of vehicles"],
                vehicle_operation=eur["07.2 Operation of personal transport equipment"],
                impulse_pct_charted=100 * float(eur.loc[mm["chart"]].sum()) / float(cb.loc[mm["chart"]].sum()),
                flow_pct_consumption=ii["flow_pct_consumption"],
                all_bars_over_flow=ii["bars_all_usd"] / ii["flow_usd"],          # 1 when Engel adding-up holds
                top10_overlap_with_published=len(set(t10) & set(PUB3_ORDER)))


conv_cmp = pd.DataFrame([headline(m, "post conventions (reproduces the figures)"),
                         headline(m, "post conventions, EUR from the weighted mean (no total-column rescale)", eur_post=False),
                         headline(B.build_fi_model(weights="equal_households"), "post data and units, equal-household weights"),
                         headline(m_coh, "coherent machinery, 12ew composition", eur_post=False),
                         headline(B.build_fi_model(convention="coherent", composition="14qa"),
                                  "coherent machinery, 14qa composition", eur_post=False),
                         headline(B.build_fi_model(convention="coherent", eta_parent="usda"),
                                  "coherent machinery, 12ew, TB-1929 group parents (adding-up holds)", eur_post=False)])
conv_cmp.to_csv(OUT / "fi_convention_compare.csv", index=False, float_format="%.4f")
print("\nstep 12, conventions:")
print(conv_cmp[["variant", "dividend", "net_q1", "net_q5", "avg_budget", "rent", "food", "vehicles", "impulse_pct_charted",
                "flow_pct_consumption", "all_bars_over_flow", "top10_overlap_with_published"]].round(3).to_string(index=False))


# %% step 13: Fig 2 rebuilt (light mode, PNG at 200 dpi). Palette and mark specs from the dataviz skill's reference
# instance, as in fig5_rebuilt.png: one series hue (slot-1 blue), ink for published values, hairline recessive grid.
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch, Rectangle

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, BAND = "#2a78d6", "#f0efec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "savefig.facecolor": SURF})


def style_axes(ax, grid_axis="x"):
    for s_ in ["top", "right", "left"]:
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8, linestyle="-")
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def hbar_rounded(ax, yc, v, h, color, r_px=8):
    """Horizontal bar from 0 to v centred on yc: rounded data-end, square at the baseline (r_px at 200 dpi)."""
    if v == 0:
        return
    p0, p1 = ax.transData.transform((0, 0)), ax.transData.transform((1, 1))
    ppx, ppy = abs(p1[0] - p0[0]), abs(p1[1] - p0[1])
    rx = r_px / ppx
    x0, x1 = min(0, v), max(0, v)
    if (x1 - x0) <= 2.2 * rx:
        ax.add_patch(Rectangle((x0, yc - h / 2), x1 - x0, h, facecolor=color, edgecolor="none", zorder=3))
        return
    ax.add_patch(FancyBboxPatch((x0, yc - h / 2), x1 - x0, h, boxstyle=f"round,pad=0,rounding_size={rx}",
                                mutation_aspect=ppx / ppy, facecolor=color, edgecolor="none", zorder=3))
    sq = (0, v / 2) if v > 0 else (v / 2, 0)
    ax.add_patch(Rectangle((min(sq), yc - h / 2), abs(sq[1] - sq[0]), h, facecolor=color, edgecolor="none", zorder=3))


n = len(CH)
yy = np.arange(n)[::-1].astype(float)
fig = plt.figure(figsize=(13.0, 13.4), dpi=200)
axL = fig.add_axes([0.30, 0.085, 0.46, 0.745])
axR = fig.add_axes([0.80, 0.085, 0.17, 0.745], sharey=axL)
axL.set_xlim(-1.8, 8.6)
axL.set_ylim(-0.8, n - 0.2)
style_axes(axL)
axL.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
fig.canvas.draw()
for c, yc in zip(CH, yy):
    g = ds.loc[c, "dEUR_mpc1"]
    axL.add_patch(Rectangle((min(0, g), yc - 0.33), abs(g), 0.66, facecolor="none", edgecolor=MUTED, linewidth=0.9, zorder=2))
    hbar_rounded(axL, yc, ds.loc[c, "dEUR_mid"], 0.40, BLUE)
    axL.plot([PUB2.loc[c, "pub_eur"]] * 2, [yc - 0.27, yc + 0.27], color=INK, linewidth=1.6, zorder=5, solid_capstyle="butt")
    axL.plot(PUB2.loc[c, "pub_ghost"], yc, marker="D", markersize=4.2, markerfacecolor=SURF, markeredgecolor=INK,
             markeredgewidth=1.0, zorder=6, linestyle="none")
axL.set_yticks(yy)
axL.set_yticklabels(CH, fontsize=8.4)
axL.set_xlabel("Change in spending, EUR per adult share per month", fontsize=9, color=INK2)
for c in ["04.1 Actual rents", "01.1 Food (at home)", "07.2 Operation of personal transport equipment", "07.1 Purchase of vehicles"]:
    yc = yy[CH.index(c)]
    v = ds.loc[c, "dEUR_mid"]
    xt = max(v, ds.loc[c, "dEUR_mpc1"], 0) + 0.10
    axL.text(xt, yc, f"{v:+.2f} rebuilt / {PUB2.loc[c, 'pub_eur']:+.2f} published\nMPC=1: {ds.loc[c, 'dEUR_mpc1']:+.2f} / "
             f"{PUB2.loc[c, 'pub_ghost']:+.2f}", va="center", fontsize=7.3, color=INK2, linespacing=1.15)
style_axes(axR)
axR.axvspan(-0.005, 0.005, color=BAND, zorder=0, linewidth=0)
for xv in (-0.02, 0.02):
    axR.axvline(xv, color=GRID, linewidth=0.8, zorder=1)
axR.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
axR.plot(ds.loc[CH, "gap_ghost"].values, yy, marker="D", markersize=4.2, markerfacecolor=SURF, markeredgecolor=MUTED,
         markeredgewidth=1.0, linestyle="none", zorder=3)
axR.plot(ds.loc[CH, "gap_eur"].values, yy, marker="o", markersize=4.6, markerfacecolor=BLUE, markeredgecolor=SURF,
         markeredgewidth=1.0, linestyle="none", zorder=4)
lim = max(0.04, float(np.ceil(100 * max(ds.loc[CH, "gap_ghost"].abs().max(), ds.loc[CH, "gap_eur"].abs().max())) / 100) + 0.005)
axR.set_xlim(-lim, lim)
axR.set_xticks([-0.02, 0, 0.02])
axR.set_xticklabels(["−0.02", "0", "+0.02"])
axR.tick_params(axis="y", labelleft=False)
axR.set_xlabel("Rebuilt minus published, EUR", fontsize=9, color=INK2)
axR.text(0, n - 0.05, "shaded: ±0.005, the bar labels' rounding", ha="center", va="bottom", fontsize=7.3, color=INK2)
n_in = int((ds.loc[CH, "gap_eur"].abs() <= 0.005 + 1e-9).sum())
fig.text(0.30, 0.962, "Fig 2 rebuilt: Finland impact-period demand shifts under the 15-point VAT bridge", fontsize=13.5,
         color=INK, ha="left", weight="bold")
fig.text(0.30, 0.946, "HBS 2022 quintiles (ktutk 14pg, per consumption unit), payment shares from tulonjako 12ew, Working-model "
         "elasticities (TB-1929)\nat the COICOP-division level, MPC = the US decile schedule averaged to quintiles "
         f"({', '.join(f'{v:.2f}' for v in MID)}), not fitted to these bars.\n"
         f"{n_in} of 37 bars land within ±EUR 0.005 of the printed labels (RMSE EUR {rmse(ds.loc[CH, 'gap_eur']):.4f}); "
         f"MPC=1 ghosts: RMSE EUR {rmse(ds.loc[CH, 'gap_ghost']):.4f} against ±0.01 read-offs.",
         fontsize=9.0, color=INK2, ha="left", va="top", linespacing=1.35)
handles = [Patch(facecolor=BLUE, edgecolor="none", label="rebuilt, MPC mid schedule"),
           Patch(facecolor="none", edgecolor=MUTED, label="rebuilt, MPC = 1 (ghost)"),
           Line2D([0], [0], color=INK, linewidth=1.6, label="published bar label"),
           Line2D([0], [0], marker="D", markersize=4.6, markerfacecolor=SURF, markeredgecolor=INK, linestyle="none",
                  label="published ghost (read off Fig 2, ±0.01)"),
           Line2D([0], [0], marker="o", markersize=5, markerfacecolor=BLUE, markeredgecolor=SURF, linestyle="none",
                  label="gap, MPC mid bar"),
           Line2D([0], [0], marker="D", markersize=4.6, markerfacecolor=SURF, markeredgecolor=MUTED, linestyle="none",
                  label="gap, ghost")]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.30, 0.888), ncol=3, frameon=False, fontsize=8.2,
           handlelength=1.6, columnspacing=1.6, labelcolor=INK2)
fig.text(0.30, 0.022, "Rebuilt in consumption/rebuild (bridge.py, run_fi.py) from Statistics Finland HBS 2022 (ktutk 14pg, 14qa), "
         "tulonjako 12ew and USDA ERS TB-1929 Tables 3-4.\nPublished values: bar labels and outlines of Fig 2 in the 2026-06-14 "
         "post (post_published_numbers.csv). Same category order as the published figure.", fontsize=7.3, color=MUTED,
         ha="left", linespacing=1.3)
fig.savefig(FIG / "fig2_rebuilt.png", dpi=200)
plt.close(fig)
print("figure: fig2_rebuilt.png")
