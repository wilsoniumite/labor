# run_us.py - the post's US exercise rebuilt (CE 2024 deciles): every judgment call re-derived against the
# published numbers, the calibrated constants in bridge.py asserted, and the US outputs written.
#
# Run from the repo root:  venv/bin/python -I consumption/rebuild/code/run_us.py
# Outputs (consumption/rebuild/out/): us_accounting_by_decile.csv, us_demand_shifts.csv, us_decomposition_top10.csv,
#   us_flags.csv, us_mpc_schedules.csv, us_eta.csv, plus the calibration evidence us_budget_tests.csv,
#   us_flags_search.csv, us_mapping_tests.csv, us_mpc_fit_surface.csv, us_mpc_params.csv, us_impulse.csv,
#   us_sensitivity.csv, us_flag_variants.csv (every bar under the rent-0 and used-cars-0.1 flag variants).
#   Figures (consumption/rebuild/figures/): fig5_rebuilt.png, us_mpc_fit.png.
# Gate: consumption/rebuild/checks/gate_us.py. Write-up: consumption/rebuild/NOTES_us.md.
# Plain functions plus top-level code; each %% block pastes into a notebook cell.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import itertools

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from tqdm.auto import tqdm

import bridge as B

OUT = B.REBUILD / "out"
FIG = B.REBUILD / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
DEC = [f"d{i:02d}" for i in range(1, 11)]
GATE = pd.read_csv(B.TIDY / "post_published_numbers.csv")
pd.set_option("display.width", 220)


def gate_value(pid):
    return float(GATE.loc[GATE["id"] == pid, "value"].iloc[0])


# %% published targets used in the calibration (ids from post_published_numbers.csv)
F4 = "fig4_net_transfer_us2024-1.png"
F5 = "fig5_demand_shifts_us2024_mpc.png"
F6 = "fig6_composition_us2024_mpc-1.png"
PUB_NET = pd.Series([gate_value(f"P{i}") for i in [291, 294, 295, 296, 297, 298, 299, 300, 301, 302]], index=DEC)
PUB_X = pd.Series([gate_value(f"P{i}") for i in range(305, 315)], index=DEC)       # point positions, +/-5
PUB_DIV, PUB_D1_PCT, PUB_D10_PCT = gate_value("P290"), gate_value("P292"), gate_value("P303")
_f5 = GATE[GATE["source"] == F5]
PUB5 = pd.DataFrame({
    "pub_usd": _f5[_f5["quantity"].str.startswith("change in spending per adult share")].set_index("item")["value"],
    "pub_pct": _f5[_f5["quantity"].str.startswith("percent change in category spending")].set_index("item")["value"],
    "pub_ghost": _f5[_f5["quantity"] == "MPC=1 benchmark (ghost) value"].set_index("item")["value"]})
PUB5 = PUB5.loc[_f5[_f5["quantity"].str.startswith("change in spending")]["item"]]       # figure order, top to bottom
_seg = GATE[(GATE["source"] == F6) & GATE["quantity"].str.startswith("decile contribution to change in spending")].copy()
_seg["decile"] = _seg["group"].str.replace("US D", "").astype(int).map(lambda d: f"d{d:02d}")
PUB6 = _seg.pivot(index="item", columns="decile", values="value")[DEC]
FIG7 = {"low": gate_value("P538"), "mid": gate_value("P537"), "high": gate_value("P539")}   # % of consumption

m = B.build_model(2024)
assert set(PUB5.index) == set(m["chart"]), set(PUB5.index) ^ set(m["chart"])
CH = list(PUB5.index)
print(f"CE 2024 deciles: {len(m['C'])} budget categories ({len(CH)} charted), budget ${m['budget_bar']:.2f}/share/month")

# %% step 1: budget rows (which CE rows make up the consumption budget C_d)
# The VAT base and the nets do not depend on this (the candidate rows carry flag 0); the budget enters through
# Fig 4's percent-of-budget labels (D1 +4.8%, D10 -3.9%), the 59-64% VAT-able range and every demand shock.
vals = m["vals"]
pip_ = vals.loc[B.EXP + " > Personal insurance and pensions", DEC]
cc = vals.loc[B.EXP + " > Cash contributions", DEC]
off = m["spend"].loc[["Education", "Mortgage interest and charges", "Property taxes"]].sum()
acc0 = B.vat_accounting(m)
# Every alternative starts from the model's own budget, the sum of the 40 lines (annual per CU). It equals the printed
# total minus personal insurance and pensions minus cash contributions within $4 a CU-year (CE prints whole dollars).
lines40 = m["spend"].sum()
assert np.allclose(lines40 / 12.0 / m["units"]["shares"], m["budget"], rtol=0, atol=1e-9)
budget_alts = {"sum of the 40 lines = total - pensions/insurance - cash contributions (chosen)": lines40,
               "40 lines + cash contributions": lines40 + cc,
               "40 lines + cash contributions + pensions/insurance (total expenditures)": lines40 + cc + pip_,
               "chosen minus education, mortgage interest, property taxes": lines40 - off}
rows = []
for name, b in budget_alts.items():
    bm = b / 12.0 / m["units"]["shares"]
    pct = 100 * acc0["net"] / bm
    sh = 100 * acc0["vatable"] / bm
    rows.append(dict(budget=name, D1_net_pct=pct["d01"], D10_net_pct=pct["d10"], vatable_share_min=sh.min(),
                     vatable_share_max=sh.max(), D1_pass=round(pct["d01"], 1) == PUB_D1_PCT,
                     D10_pass=round(pct["d10"], 1) == PUB_D10_PCT,
                     range_pass=(round(sh.min()) == 59) and (round(sh.max()) == 64)))
budget_tests = pd.DataFrame(rows)
budget_tests.to_csv(OUT / "us_budget_tests.csv", index=False, float_format="%.4f")
print("\nstep 1, budget rows (published D1 +4.8%, D10 -3.9%, VAT-able 59-64%):")
print(budget_tests.round(3).to_string(index=False))
assert budget_tests.iloc[0][["D1_pass", "D10_pass", "range_pass"]].all()
assert not budget_tests.iloc[1][["D1_pass", "D10_pass"]].all()
chk = B.budget_check(vals, m["spend"], m["prov"])
assert chk["diff"].abs().max() <= 5, chk                     # $1 rounding per CE line, up to ~40 lines

# %% step 2: VAT flags. A grid of Directive-consistent values for the lines whose treatment is a judgment, each
# value with a stated reason (US_VAT_REASONS / the grid notes below); the published accounting numbers pick one.
# Objective: Fig 4 net labels and the dividend (printed integers: sd 0.5/sqrt 3), D1 and D10 percent-of-budget
# (sd 0.05/sqrt 3), point positions (+/-5: sd 5/sqrt 3; D2 skipped, hidden behind D4), and the 59-64% range.
T25 = {"water_public_refuse_out": round((559.48 + 8.69) / 826.03, 4),   # Table 2500 2024 lines, see bridge reasons
       "lodging_trips_only": round(905.72 / 1346.64, 4),
       "vehicle_charges_tolls_public": round((423.57 + 57.99 + 6.0 + 19.44) / 810.56, 4),
       "drugs_rx_relief": round((142.69 + 134.37) / 657.81, 4),
       "transport_local_transit_exempt": round((1130.58 - 108.85 - 2.51) / 1130.58, 4),
       "fees_nonprofit_clubs_exempt": round((934.9 - 271.87) / 934.9, 4)}
FLAG_GRID = {
    "Cars and trucks, used": [0.0, 0.25, 0.5, 0.75, 1.0],                       # dealer vs private: CE cannot split
    "Water and other public services": [T25["water_public_refuse_out"], 1.0],   # public-body refuse (Art. 13) | Nordic
    "Other lodging": [T25["lodging_trips_only"], B.US_VAT_START["Other lodging"]],
    "Vehicle rental, leases, licenses": [T25["vehicle_charges_tolls_public"], B.US_VAT_START["Vehicle rental, leases, licenses"]],
    "Drugs": [T25["drugs_rx_relief"], 1.0],                                      # Rx zero-rated (SE, IE, MT) | Annex III
    "Public and other transportation": [T25["transport_local_transit_exempt"], 1.0],
    "Fees and admissions": [T25["fees_nonprofit_clubs_exempt"], 1.0],
    "Rented dwellings": [0.0, B.US_VAT_START["Rented dwellings"]],
    "Education": [0.0, B.US_VAT_START["Education"]],
}


def flag_search(m, grid, base_flags, chunk=200000, desc="flag grid"):
    """Score every combination of grid values (other lines at base_flags) against the published accounting
    numbers; returns a DataFrame sorted by the objective."""
    C, w, bud = m["C"], m["w"].values, m["budget"].values
    keys = list(grid)
    fixed = [k for k in C.index if k not in grid]
    v0 = C.loc[fixed].mul(pd.Series(base_flags).reindex(fixed).fillna(0.0), axis=0).sum().values
    M = C.loc[keys].values
    combos = np.array(list(itertools.product(*[grid[k] for k in keys])), dtype=float)
    lab, xp = PUB_NET.values, PUB_X.values
    xw = np.array([1, 0, 1, 1, 1, 1, 1, 1, 1, 1.0])
    s_lab, s_x, s_pct = 0.5 / np.sqrt(3), 5 / np.sqrt(3), 0.05 / np.sqrt(3)
    res = []
    for a in tqdm(range(0, len(combos), chunk), desc=desc, leave=False):
        cb = combos[a:a + chunk]
        cv = v0[None, :] + cb @ M
        cbar = cv @ w
        net = B.TAU * (cbar[:, None] - cv)
        div = B.TAU * cbar
        pct = 100 * net / bud[None, :]
        sh = 100 * cv / bud[None, :]
        obj = (((net - lab) / s_lab) ** 2).sum(1) + ((div - PUB_DIV) / s_lab) ** 2 \
            + ((((cv - xp) / s_x) ** 2) * xw).sum(1) + ((pct[:, 0] - PUB_D1_PCT) / s_pct) ** 2 \
            + ((pct[:, 9] - PUB_D10_PCT) / s_pct) ** 2 \
            + 100.0 * ((np.round(sh.min(1)) != 59) | (np.round(sh.max(1)) != 64))
        r = pd.DataFrame(cb, columns=keys)
        r["objective"], r["dividend"] = obj, div
        r["labels_exact"] = (np.round(net) == lab).sum(1)
        r["max_abs_net_gap"] = np.abs(net - lab).max(1)
        res.append(r)
    return pd.concat(res, ignore_index=True).sort_values("objective").reset_index(drop=True)


fs = flag_search(m, FLAG_GRID, B.US_VAT_START, desc="VAT flags (Directive grid)")
best = fs.iloc[0]
for k in FLAG_GRID:
    assert abs(best[k] - B.US_VAT_FLAGS[k]) < 1e-4, (k, best[k], B.US_VAT_FLAGS[k])
fs["grid"] = "Directive-consistent"
# Diagnostic: a looser grid that also allows whole-line 0/0.5/1 flags on the mixed lines, including values the
# Directive reading rules out (licences and vehicle property tax, vacation-home interest and property tax in the
# base). Reported, not adopted.
LOOSE = dict(FLAG_GRID, **{"Home maintenance, repairs & insurance": [0.0, 0.5, B.US_VAT_START["Home maintenance, repairs & insurance"], 1.0],
                           "Other lodging": [0.0, 0.5, T25["lodging_trips_only"], B.US_VAT_START["Other lodging"], 1.0],
                           "Vehicle rental, leases, licenses": [0.0, 0.5, B.US_VAT_START["Vehicle rental, leases, licenses"], 1.0],
                           "Miscellaneous": [0.0, 0.5, B.US_VAT_START["Miscellaneous"], 1.0],
                           "Drugs": [0.0, T25["drugs_rx_relief"], 0.5, 1.0],
                           "Public and other transportation": [0.5, T25["transport_local_transit_exempt"], 1.0],
                           "Housekeeping supplies": [B.US_VAT_START["Housekeeping supplies"], 1.0]})
fl_loose = flag_search(m, LOOSE, B.US_VAT_START, desc="VAT flags (loose grid, diagnostic)")
fl_loose["grid"] = "loose (diagnostic, not adopted)"
search_out = pd.concat([fs.head(20), fl_loose.head(20)], ignore_index=True)
search_out.to_csv(OUT / "us_flags_search.csv", index=False, float_format="%.4f")
used_share = fs.head(20)["Cars and trucks, used"].value_counts().to_dict()
print(f"\nstep 2, VAT flags: Directive grid {len(fs)} combinations, best objective {best['objective']:.1f} "
      f"(dividend ${best['dividend']:.2f}, {int(best['labels_exact'])}/10 labels exact, max gap ${best['max_abs_net_gap']:.2f}); "
      f"loose grid best {fl_loose.iloc[0]['objective']:.1f} ({int(fl_loose.iloc[0]['labels_exact'])}/10). "
      f"Used-car flag across the top 20: {used_share}")

# %% step 3: the accounting tier
acc = B.vat_accounting(m)
u = m["units"]
acc_out = pd.DataFrame({
    "decile": DEC, "cu_thousand": u["N_thousand"], "people": u["people"], "children": u["children"],
    "adults": u["adults"], "payment_shares": u["shares"], "w_share_weight": u["w"],
    "budget_usd_month": m["budget"], "vatable_usd_month": acc["vatable"], "vatable_pct_budget": acc["vatable_pct_budget"],
    "tax_usd_month": acc["tax"], "dividend_usd_month": acc["dividend"], "net_usd_month": acc["net"],
    "net_pct_budget": acc["net_pct_budget"], "pub_net_label": PUB_NET, "pub_x_position": PUB_X})
acc_out["net_gap"] = acc_out["net_usd_month"] - acc_out["pub_net_label"]
acc_out["net_rounds_to_label"] = np.round(acc_out["net_usd_month"]) == acc_out["pub_net_label"]
acc_out.to_csv(OUT / "us_accounting_by_decile.csv", index=False, float_format="%.4f")
NET = acc["net"]
vs = B.vatable_share_aggregate(m)
print(f"\nstep 3, accounting: dividend ${acc['dividend'].iloc[0]:.2f} (published {PUB_DIV:.0f}), mean VAT-able "
      f"${acc['Cbar_v'].iloc[0]:.1f}, aggregate VAT-able share {100 * vs:.2f}%")
print(acc_out[["decile", "net_usd_month", "pub_net_label", "net_pct_budget", "vatable_pct_budget"]].round(2).T.to_string(header=False))

# %% step 4: elasticities - the stage-one mapping and the food split, tested on the Fig 5 ghosts (MPC=1: no MPC
# enters) and on the bars at each variant's best knee/top. Every bar RMSE in this file is on one knee x top grid,
# the step-5 calibration grid (knee 1-9 by 0.05, top 0.40-0.65 by 0.0025), except the flag-variant refits of step 5b,
# which also use knee steps of 0.01 and say so.
KNEES = np.round(np.arange(1.0, 9.0001, 0.05), 3)
TOPS = np.round(np.arange(0.40, 0.65001, 0.0025), 4)


def knee_fit(D, y, knees, tops):
    """SSE over a knee x top grid for contributions-per-unit-MPC D (categories x groups) against bars y."""
    S = np.empty((len(knees), len(tops)))
    for i, k in enumerate(knees):
        P = np.stack([B.mpc_knee(k, t, D.shape[1]) for t in tops], axis=1)   # groups x tops
        S[i] = ((D @ P - y[:, None]) ** 2).sum(0)
    return S


def mapping_score(mm, net, knees=KNEES, tops=TOPS):
    sh = B.shifts_from_transfers(mm, net, mpc=np.ones(10))
    gg = sh.loc[CH, "dUSD_mpc1"] - PUB5["pub_ghost"]
    D = B.decompose(mm, (net / mm["budget"]).values).loc[CH].values
    S = knee_fit(D, PUB5["pub_usd"].values, knees, tops)
    i, j = np.unravel_index(S.argmin(), S.shape)
    return dict(ghost_rmse=float(np.sqrt((gg ** 2).mean())), ghost_max_abs=float(gg.abs().max()),
                worst_ghost=gg.abs().idxmax(), bars_rmse_best_knee=float(np.sqrt(S[i, j] / len(CH))),
                best_knee=float(knees[i]), best_top=float(tops[j]))


usda0 = {c["cat"]: c["usda"] for c in B.US_CATEGORIES}
MAP_ALTS = {"chosen: CE majors, telephone in transport & communication": {},
            "telephone in housing (CE utilities)": {"Telephone services": "housing"},
            "personal services in other (social protection)": {"Personal services (incl. childcare)": "other"},
            "health insurance in other (COICOP 12)": {"Health insurance": "other"},
            "vehicle insurance in other (COICOP 12)": {"Vehicle insurance": "other"},
            "other lodging in other (COICOP 11.2)": {"Other lodging": "other"},
            "other lodging in recreation": {"Other lodging": "recreation"},
            "vehicle finance charges in other": {"Vehicle finance charges": "other"},
            "home maintenance in furnishings": {"Home maintenance, repairs & insurance": "furnishings"},
            "reading in other": {"Reading": "other"}}
rows = []
for name, alt in tqdm(MAP_ALTS.items(), desc="mapping variants", leave=False):
    mm = B.build_model(2024, usda=dict(usda0, **alt))
    rows.append(dict(test="stage-one mapping", variant=name, **mapping_score(mm, NET)))
for fmap, desc in [("A", "chosen A: Food other = restaurants, B&T = alcohol + tobacco, at home = six named"),
                   ("A2", "A2: nonalcoholic beverages in Beverages and tobacco"),
                   ("B", "B: CE food-at-home lines mapped; at-home 'other foods' share Food other with restaurants"),
                   ("B2", "B2: as B, nonalcoholic beverages in Beverages and tobacco"),
                   ("F", "F: no split, stage-one food eta for all four")]:
    mm = B.build_model(2024, food_map=fmap)
    sc = mapping_score(mm, NET)
    fo = B.shifts_from_transfers(mm, NET, mpc=B.mpc_mid())
    food = ["Food at home", "Food away from home", "Alcoholic beverages", "Tobacco products"]
    sc.update({f"ghost_{c}": fo.loc[c, "dUSD_mpc1"] for c in food})
    sc.update({f"bar_{c}": fo.loc[c, "dUSD_mpc"] for c in food})
    rows.append(dict(test="food split", variant=desc, **sc))
for desc, mm in [("TB-1929 betas back-solved (unrounded) instead of printed", B.build_model(2024, params=B.usda_params(True)))]:
    rows.append(dict(test="parameters", variant=desc, **mapping_score(mm, NET)))
rows.append(dict(test="nets", variant="published Fig 4 labels as the net vector", **mapping_score(m, PUB_NET)))
map_tests = pd.DataFrame(rows)
map_tests.to_csv(OUT / "us_mapping_tests.csv", index=False, float_format="%.5f")
print("\nstep 4, mapping and food split (ghost RMSE; bar RMSE at each variant's best knee/top):")
print(map_tests[["test", "variant", "ghost_rmse", "worst_ghost", "bars_rmse_best_knee", "best_knee", "best_top"]].round(4).to_string(index=False))
# Adoption rule: a variant replaces the chosen one only if it lowers BOTH the ghost RMSE and the best-knee bar RMSE
# by more than 10% (smaller differences are inside the +/-0.01 read-off noise of the ghosts). Telephone moved to
# transport & communication passed it against the CE-utilities reading (ghosts -34%, bars -64%); nothing passes it
# against the chosen mapping or food split.
ch0 = map_tests.iloc[0]
better = map_tests[(map_tests["ghost_rmse"] < 0.9 * ch0["ghost_rmse"]) & (map_tests["bars_rmse_best_knee"] < 0.9 * ch0["bars_rmse_best_knee"])]
assert better.empty, better
tel = map_tests[map_tests["variant"].str.startswith("telephone in housing")].iloc[0]
assert ch0["ghost_rmse"] < 0.9 * tel["ghost_rmse"] and ch0["bars_rmse_best_knee"] < 0.9 * tel["bars_rmse_best_knee"]

# %% step 5: the MPC schedules. mid: knee and top by least squares on the 36 Fig 5 dollar bars (fit surface below);
# low/high: tops 0.40 and 0.65 (footnote 27), knees pinned by Fig 7's band edges.
D1 = B.decompose(m, (NET / m["budget"]).values)
Dch = D1.loc[CH].values
y = PUB5["pub_usd"].values
S = np.empty((len(KNEES), len(TOPS)))
for i, k in enumerate(tqdm(KNEES, desc="MPC fit surface (knee x top)", leave=False)):
    P = np.stack([B.mpc_knee(k, t) for t in TOPS], axis=1)
    S[i] = ((Dch @ P - y[:, None]) ** 2).sum(0)
i, j = np.unravel_index(S.argmin(), S.shape)
k_mid, t_mid = float(KNEES[i]), float(TOPS[j])
assert abs(k_mid - B.US_MPC_KNEE["mid"]) < 1e-9 and abs(t_mid - B.US_MPC_TOP["mid"]) < 1e-9, (k_mid, t_mid)
surf = pd.DataFrame([(k, t, S[a, b], np.sqrt(S[a, b] / len(CH))) for a, k in enumerate(KNEES) for b, t in enumerate(TOPS)],
                    columns=["knee", "top", "sse", "rmse_usd"])
surf.to_csv(OUT / "us_mpc_fit_surface.csv", index=False, float_format="%.6f")
rm_min = np.sqrt(S.min() / len(CH))
sd_round = 0.005 / np.sqrt(3)
near = surf[surf["sse"] <= S.min() + 2.30 * sd_round ** 2]          # 68% region for 2 parameters, rounding noise only
int_knees = {k: (float(TOPS[S[np.where(KNEES == k)[0][0]].argmin()]),
                 float(np.sqrt(S[np.where(KNEES == k)[0][0]].min() / len(CH)))) for k in [1.0, 2.0, 3.0, 4.0, 5.0]}


def impulse_pct(mpc):
    return B.impulse(m, NET, mpc)["flow_pct_consumption"]


f_imp = lambda k, top, target: impulse_pct(B.mpc_knee(k, top)) - target
k_low_exact = brentq(f_imp, 1.0, 8.0, args=(B.US_MPC_TOP["low"], FIG7["low"]))
k_high_exact = brentq(f_imp, 1.0, 8.0, args=(B.US_MPC_TOP["high"], FIG7["high"]))
assert abs(round(k_low_exact, 2) - B.US_MPC_KNEE["low"]) < 1e-9 and abs(round(k_high_exact, 2) - B.US_MPC_KNEE["high"]) < 1e-9
sched = B.mpc_schedules()
common = B.mpc_schedules(knees=k_mid)
# Fig 6 diagnostic (not used in the fit): per-decile MPC implied by the 100 read-off segments, least squares across
# the ten categories at each decile, given the rebuilt nets and elasticities
fig6_mpc = pd.Series({d: float((PUB6[d] * D1.loc[PUB6.index, d]).sum() / (D1.loc[PUB6.index, d] ** 2).sum()) for d in DEC})
fig6_mpc_labelnets = pd.Series({d: fig6_mpc[d] * NET[d] / PUB_NET[d] for d in DEC})


def monotone_mpc_fit(Dbars, ybars, Dseg, yseg, s_bar=0.005 / np.sqrt(3), s_seg=0.01 / np.sqrt(3), lo=0.40):
    """Per-decile MPCs, non-increasing in income, bottom <= 1, top >= lo, fitted by weighted least squares to the
    Fig 5 bars (printing noise) and the Fig 6 segments (read-off noise). mpc_d = 1 - sum_{j<=d} delta_j, delta >= 0."""
    from scipy.optimize import lsq_linear
    n = Dbars.shape[1]
    L = np.tril(np.ones((n, n)))                                   # mpc = 1 - L @ delta
    A = np.vstack([-(Dbars @ L) / s_bar, -(Dseg @ L) / s_seg])
    b = np.concatenate([(ybars - Dbars.sum(1)) / s_bar, (yseg - Dseg.sum(1)) / s_seg])
    # top >= lo  <=>  sum(delta) <= 1 - lo: enforced by bounds on a cumulative reparameterisation is awkward, so
    # check afterwards (it does not bind for these data)
    r = lsq_linear(A, b, bounds=(0, np.inf))
    mpc = 1 - L @ r.x
    assert mpc[-1] >= lo - 1e-9
    return mpc


segs = [(c, d) for c in PUB6.index for d in DEC]
Dseg = np.zeros((len(segs), 10))
for a, (c, d) in enumerate(segs):
    Dseg[a, DEC.index(d)] = D1.loc[c, d]
yseg = np.array([PUB6.loc[c, d] for c, d in segs])
mpc_mono = monotone_mpc_fit(Dch, y, Dseg, yseg)
seg_rmse = lambda mpc: float(np.sqrt(((Dseg @ mpc - yseg) ** 2).mean()))
bar_rmse = lambda mpc: float(np.sqrt(((Dch @ mpc - y) ** 2).mean()))
sched_out = pd.DataFrame({"decile": DEC, "mpc_low": sched["low"].values, "mpc_mid": sched["mid"].values,
                          "mpc_high": sched["high"].values, "mpc_low_common_knee": common["low"].values,
                          "mpc_high_common_knee": common["high"].values,
                          "mpc_mid_monotone_fig5_fig6_diagnostic": mpc_mono,
                          "fig6_implied_mpc_diagnostic": fig6_mpc.values,
                          "fig6_implied_mpc_at_label_nets": fig6_mpc_labelnets.values})
sched_out.to_csv(OUT / "us_mpc_schedules.csv", index=False, float_format="%.4f")
imp = {k: B.impulse(m, NET, sched[k].values) for k in sched}
imp_c = {k: B.impulse(m, NET, common[k].values) for k in common}
params = pd.DataFrame([
    dict(schedule="mid", knee=k_mid, top=t_mid, pinned_by="least squares on the 36 Fig 5 dollar bars",
         fit_rmse_usd=rm_min, impulse_pct_consumption=imp["mid"]["flow_pct_consumption"], fig7_published=FIG7["mid"]),
    dict(schedule="low", knee=B.US_MPC_KNEE["low"], top=B.US_MPC_TOP["low"],
         pinned_by="top: footnote 27 (0.40); knee: Fig 7 upper band edge 0.474", fit_rmse_usd=np.nan,
         impulse_pct_consumption=imp["low"]["flow_pct_consumption"], fig7_published=FIG7["low"]),
    dict(schedule="high", knee=B.US_MPC_KNEE["high"], top=B.US_MPC_TOP["high"],
         pinned_by="top: footnote 27 (0.65); knee: Fig 7 lower band edge 0.305", fit_rmse_usd=np.nan,
         impulse_pct_consumption=imp["high"]["flow_pct_consumption"], fig7_published=FIG7["high"]),
    dict(schedule="low, common knee (alternative)", knee=k_mid, top=B.US_MPC_TOP["low"], pinned_by="mid knee",
         fit_rmse_usd=np.nan, impulse_pct_consumption=imp_c["low"]["flow_pct_consumption"], fig7_published=FIG7["low"]),
    dict(schedule="high, common knee (alternative)", knee=k_mid, top=B.US_MPC_TOP["high"], pinned_by="mid knee",
         fit_rmse_usd=np.nan, impulse_pct_consumption=imp_c["high"]["flow_pct_consumption"], fig7_published=FIG7["high"]),
    dict(schedule="mid, monotone per-decile (diagnostic)", knee=np.nan, top=float(mpc_mono[-1]),
         pinned_by="weighted LS on the 36 Fig 5 bars and the 100 Fig 6 segments, non-increasing",
         fit_rmse_usd=bar_rmse(mpc_mono), impulse_pct_consumption=impulse_pct(mpc_mono), fig7_published=FIG7["mid"],
         fig6_segment_rmse_usd=seg_rmse(mpc_mono))]
    + [dict(schedule=f"best top at integer knee {k:.0f}", knee=k, top=v[0], pinned_by="fit surface", fit_rmse_usd=v[1],
            impulse_pct_consumption=impulse_pct(B.mpc_knee(k, v[0])), fig7_published=FIG7["mid"]) for k, v in int_knees.items()])
params.loc[params["schedule"] == "mid", "fig6_segment_rmse_usd"] = seg_rmse(sched["mid"].values)
params.to_csv(OUT / "us_mpc_params.csv", index=False, float_format="%.5f")
avg_gap = float(np.abs(sched["mid"] - (sched["low"] + sched["high"]) / 2).max())
print(f"\nstep 5, MPC: mid knee {k_mid}, top {t_mid}, bar RMSE ${rm_min:.4f} (printing floor ${sd_round:.4f}); "
      f"68% region knee {near['knee'].min()}-{near['knee'].max()}, top {near['top'].min()}-{near['top'].max()}")
print(f"   low knee {k_low_exact:.3f} -> {B.US_MPC_KNEE['low']}, high knee {k_high_exact:.3f} -> {B.US_MPC_KNEE['high']}; "
      f"max |mid - (low+high)/2| = {avg_gap:.4f}")
print(params[["schedule", "knee", "top", "fit_rmse_usd", "impulse_pct_consumption", "fig7_published"]].round(4).to_string(index=False))
print("   schedules:\n" + sched_out.round(3).T.to_string(header=False))

# %% step 5b: two flag variants the independent review asked to carry beside the adopted flags. The outputs keep the
# adopted flags (rent 0.0167, used cars 1/2) and the mid schedule; the variants go to us_sensitivity.csv and
# us_flag_variants.csv.
#   rent 0: the post's own 'rent exempt', as Directive-consistent as 0.0167 (renter-paid repairs). The step-2 grid takes
#           0.0167 only through the read-off point positions (+/-5); the printed numbers prefer 0, and the Fig 5 bars
#           refit as well. An equally good alternative, carried with its own MPC refit.
#   used cars 0.1: the Directive's margin scheme (Arts. 311-325) instead of the post-calibrated 1/2; a sensitivity at
#           the mid schedule (its refit is a diagnostic: Fig 5 cannot be matched at the printing floor).
# Refits use knee steps of 0.01 (top steps 0.0025, as in step 5) so that nearby optima can be told apart.
KNEES_FINE = np.round(np.arange(1.0, 9.0001, 0.01), 2)


def knee_refit(net, knees=KNEES_FINE, tops=TOPS):
    """Least-squares (knee, top) on the 36 Fig 5 dollar bars for one net vector: (rmse, knee, top)."""
    S_ = knee_fit(B.decompose(m, (net / m["budget"]).values).loc[CH].values, y, knees, tops)
    a_, b_ = np.unravel_index(S_.argmin(), S_.shape)
    return float(np.sqrt(S_[a_, b_] / len(CH))), float(knees[a_]), float(tops[b_])


def fig4_terms(fl):
    """Step 2's objective for one flag set, split into the printed numbers (net labels, dividend, D1/D10 percent of
    budget, the 59-64 range) and the read-off point positions (+/-5)."""
    a_ = B.vat_accounting(m, fl)
    net, cv, div = a_["net"].values, a_["vatable"].values, float(a_["dividend"].iloc[0])
    pct, sh_ = 100 * net / m["budget"].values, 100 * cv / m["budget"].values
    s_lab, s_x, s_pct = 0.5 / np.sqrt(3), 5 / np.sqrt(3), 0.05 / np.sqrt(3)
    xw = np.array([1, 0, 1, 1, 1, 1, 1, 1, 1, 1.0])
    printed = ((((net - PUB_NET.values) / s_lab) ** 2).sum() + ((div - PUB_DIV) / s_lab) ** 2
               + ((pct[0] - PUB_D1_PCT) / s_pct) ** 2 + ((pct[9] - PUB_D10_PCT) / s_pct) ** 2
               + 100.0 * ((np.round(sh_.min()) != 59) | (np.round(sh_.max()) != 64)))
    return float(printed), float(((((cv - PUB_X.values) / s_x) ** 2) * xw).sum())


FLAG_VARIANTS = {"adopted": B.US_VAT_FLAGS,
                 "rent 0": dict(B.US_VAT_FLAGS, **{"Rented dwellings": 0.0}),
                 "used cars 0.1": dict(B.US_VAT_FLAGS, **{"Cars and trucks, used": 0.1})}
VAR = {}
for name, fl in FLAG_VARIANTS.items():
    a_ = B.vat_accounting(m, fl)
    pt, xt = fig4_terms(fl)
    VAR[name] = dict(acc=a_, dividend=float(a_["dividend"].iloc[0]), refit=knee_refit(a_["net"]), printed_term=pt,
                     x_term=xt, labels_exact=int((np.round(a_["net"]) == PUB_NET).sum()),
                     label_sse=float(((a_["net"] - PUB_NET) ** 2).sum()))
assert abs(VAR["adopted"]["printed_term"] + VAR["adopted"]["x_term"] - best["objective"]) < 1e-6   # same objective as step 2
_r0 = fs[(fs["Rented dwellings"] == 0.0) & np.all([np.isclose(fs[k], B.US_VAT_FLAGS[k], rtol=0, atol=1e-9)
                                                    for k in FLAG_GRID if k != "Rented dwellings"], axis=0)]
assert len(_r0) == 1 and abs(VAR["rent 0"]["printed_term"] + VAR["rent 0"]["x_term"] - _r0["objective"].iloc[0]) < 1e-6
va, vr, vu = VAR["adopted"], VAR["rent 0"], VAR["used cars 0.1"]
assert vr["printed_term"] < va["printed_term"] and vr["x_term"] > va["x_term"]        # only the read-offs prefer 0.0167
assert vr["labels_exact"] > va["labels_exact"] and round(vr["dividend"]) == PUB_DIV
assert vr["refit"][0] <= va["refit"][0] + 1e-4                                         # the bars refit as well
print(f"\nstep 5b, flag variants (Fig 4 objective = printed numbers + read-off positions; refit on knee 0.01 x top 0.0025):")
for name, v in VAR.items():
    print(f"   {name:14s} dividend ${v['dividend']:.2f}; labels exact {v['labels_exact']}/10, label SSE {v['label_sse']:.2f}; "
          f"objective {v['printed_term']:.1f} + {v['x_term']:.1f}; Fig 5 refit knee {v['refit'][1]:.2f}, top {v['refit'][2]:.4f}, "
          f"RMSE ${v['refit'][0]:.4f}")

# %% step 6: elasticities table
det = m["eta_detail"]
rows = []
for c in m["C"].index:
    for d in DEC:
        r = dict(category=c, decile=d, role=m["prov"].loc[c, "role"], usda_group=B.USDA_GROUPS[m["usda"][c]],
                 eta=m["eta"].loc[c, d], beta_stage1=det.loc[c, "beta"], w_group_share=det.loc[c, f"w_{d}"])
        if m["usda"][c] == "food":
            r.update(eta_food_group=det.loc[c, f"etaF_{d}"], w_star_within_food=det.loc[c, f"wstar_{d}"],
                     beta_star=det.loc[c, f"betastar_{d}"],
                     food_subgroup={"Food at home": "six named at-home subgroups (sum of beta*)",
                                    "Food away from home": "Food other",
                                    "Alcoholic beverages": "Beverages and tobacco",
                                    "Tobacco products": "Beverages and tobacco"}[c])
        rows.append(r)
eta_out = pd.DataFrame(rows)
eta_out.to_csv(OUT / "us_eta.csv", index=False, float_format="%.5f")

# %% step 7: demand shifts (mid, low, high, MPC=1) beside the published bars
sh = {k: B.shifts_from_transfers(m, NET, mpc=sched[k].values, mpc_label=k) for k in sched}
ds = sh["mid"][["role", "usda", "Cbar", "dUSD_mid", "dPct_mid"]].copy()
for k in ["low", "high"]:
    ds[f"dUSD_{k}"], ds[f"dPct_{k}"] = sh[k][f"dUSD_{k}"], sh[k][f"dPct_{k}"]
ds["dUSD_mpc1"], ds["dPct_mpc1"] = sh["mid"]["dUSD_mpc1"], sh["mid"]["dPct_mpc1"]
ds = ds.join(PUB5)
ds["gap_usd"] = ds["dUSD_mid"] - ds["pub_usd"]
ds["gap_pct"] = ds["dPct_mid"] - ds["pub_pct"]
ds["gap_ghost"] = ds["dUSD_mpc1"] - ds["pub_ghost"]
ds = ds.join(m["prov"][["ce_source", "n_high_rse", "high_rse_groups"]])
order = list(PUB5.index) + [c for c in ds.index if c not in PUB5.index]
ds = ds.loc[order]
ds.index.name = "category"
ds.to_csv(OUT / "us_demand_shifts.csv", float_format="%.5f")
print(f"\nstep 7, Fig 5: bars RMSE ${np.sqrt((ds.loc[CH, 'gap_usd'] ** 2).mean()):.4f}, "
      f"max |gap| ${ds.loc[CH, 'gap_usd'].abs().max():.4f} ({ds.loc[CH, 'gap_usd'].abs().idxmax()}); "
      f"ghost RMSE ${np.sqrt((ds.loc[CH, 'gap_ghost'] ** 2).mean()):.4f}; "
      f"% RMSE {np.sqrt((ds.loc[CH, 'gap_pct'] ** 2).mean()):.4f} pp")

# %% step 8: decile decomposition of the ten largest movers (Fig 6)
top10 = B.top_movers(ds, "dUSD_mid", CH, 10)
assert top10 == list(PUB6.reindex(top10).index) and set(top10) == set(PUB6.index), (top10, list(PUB6.index))
cm = B.decompose(m, B.budget_shock(NET, sched["mid"].values, m["budget"]))
c1 = B.decompose(m, B.budget_shock(NET, np.ones(10), m["budget"]))
rows = []
for r, c in enumerate(top10, 1):
    for d in DEC:
        rows.append(dict(rank=r, category=c, decile=d, contrib_mid=cm.loc[c, d], contrib_mpc1=c1.loc[c, d],
                         pub_segment=PUB6.loc[c, d], gap=cm.loc[c, d] - PUB6.loc[c, d]))
    rows.append(dict(rank=r, category=c, decile="net", contrib_mid=cm.loc[c].sum(), contrib_mpc1=c1.loc[c].sum(),
                     pub_segment=PUB5.loc[c, "pub_usd"], gap=cm.loc[c].sum() - PUB5.loc[c, "pub_usd"]))
dec_out = pd.DataFrame(rows)
dec_out.to_csv(OUT / "us_decomposition_top10.csv", index=False, float_format="%.5f")
seg = dec_out[dec_out["decile"] != "net"]
print(f"step 8, Fig 6: top 10 identical to the published set and order; segments RMSE ${np.sqrt((seg['gap'] ** 2).mean()):.4f}, "
      f"max |gap| ${seg['gap'].abs().max():.3f} ({seg.loc[seg['gap'].abs().idxmax(), 'category']} "
      f"{seg.loc[seg['gap'].abs().idxmax(), 'decile']})")

# %% step 9: the aggregate demand impulse, every way it is quoted
rows = []
for k in sched:
    for sname, s in [("chosen", sched), ("common knee", common)]:
        if sname == "common knee" and k == "mid":
            continue
        ii = B.impulse(m, NET, s[k].values)
        rows.append(dict(schedule=k, variant=sname, **ii))
imp_out = pd.DataFrame(rows)
imp_out.to_csv(OUT / "us_impulse.csv", index=False, float_format="%.5f")
im = imp["mid"]
print(f"step 9, impulse (mid): flow ${im['flow_usd']:.3f} = {im['flow_pct_consumption']:.3f}% of consumption (Fig 7 0.390); "
      f"charted bars ${im['bars_chart_usd']:.3f} = {im['bars_chart_pct_consumption']:.3f}% of consumption, "
      f"{im['bars_chart_pct_charted']:.3f}% of the charted budget (caption '+0.4% of charted budget', footer '~+0.5% of consumption'); "
      f"flow / charted budget {im['flow_pct_charted']:.3f}% (the caption's own denominator)")

# %% step 10: flags table (category, VAT-able share, USDA group, rationale, what pinned it)
GROUP_REASON = {
    "food": "TB-1929 'Food, beverage, and tobacco' (restaurants included since the 2005 ICP)",
    "clothing": "TB-1929 'Clothing and footwear' (CE major category)",
    "housing": "TB-1929 'Housing and utilities' (CE shelter and utilities; owner cash costs stand in for imputed rent)",
    "furnishings": "TB-1929 'Furnishing, household equipment, and maintenance' (CE household operations, supplies, furnishings)",
    "medical": "TB-1929 'Medical and health' (CE healthcare, out-of-pocket)",
    "transport": "TB-1929 'Transportation and communication' (CE transportation)",
    "recreation": "TB-1929 'Recreation and culture' (CE entertainment, reading)",
    "education": "TB-1929 'Education'", "other": "TB-1929 'Other' (CE personal care, miscellaneous)"}
SPECIAL_GROUP = {"Telephone services": "TB-1929 'Transportation and communication' (COICOP 08), not CE utilities: pinned by "
                 f"Fig 5 (telephone ghost 0.264 vs 0.30 read off with housing; bar RMSE at the best knee "
                 f"${tel['bars_rmse_best_knee']:.4f} -> ${ch0['bars_rmse_best_knee']:.4f} on the calibration grid)"}
for c in ["Personal services (incl. childcare)", "Health insurance", "Vehicle insurance", "Other lodging",
          "Vehicle finance charges", "Home maintenance, repairs & insurance", "Reading"]:
    SPECIAL_GROUP[c] = "CE major category; the COICOP-style reassignment was tested and fits Fig 5 worse (us_mapping_tests.csv)"
PINNED = {"Cars and trucks, used": "post-calibrated 1/2, pinned by Fig 4: decile profile of the point positions and net labels "
                                   "(every good grid combination has 1/2). Not a Directive reading: the margin scheme "
                                   f"(Arts. 311-325) gives about 0.1, which funds ${vu['dividend']:.1f} with {vu['labels_exact']} "
                                   "labels exact (a sensitivity: us_sensitivity.csv, us_flag_variants.csv)",
          "Water and other public services": "Fig 4: the $249 dividend level, given the other flags (Nordic reading 1.0 gives $250.9)",
          "Rented dwellings": "not pinned by a printed number: the grid takes 0.0167 over 0 only through the read-off point "
                              f"positions (+/-5). Rent 0 (the post's 'rent exempt') gets {vr['labels_exact']} labels exact "
                              f"against {va['labels_exact']} and refits the Fig 5 bars as well (knee {vr['refit'][1]:.2f}, "
                              f"top {vr['refit'][2]:.4f}, RMSE ${vr['refit'][0]:.4f}): an equally good alternative, carried in "
                              "us_sensitivity.csv and us_flag_variants.csv. The outputs use 0.0167"}
fl_rows = []
for c in m["C"].index:
    fl_rows.append(dict(category=c, role=m["prov"].loc[c, "role"], ce_source=m["prov"].loc[c, "ce_source"],
                        vat_flag=B.US_VAT_FLAGS[c], vat_flag_start=B.US_VAT_START[c], vat_reason=B.US_VAT_REASONS[c],
                        vat_pinned_by=PINNED.get(c, "Directive reading and Table 2500 shares (not pinned by a published number)"),
                        usda_group=B.USDA_GROUPS[m["usda"][c]], usda_reason=SPECIAL_GROUP.get(c, GROUP_REASON[m["usda"][c]]),
                        food_subgroup={"Food at home": "six named at-home subgroups", "Food away from home": "Food other",
                                       "Alcoholic beverages": "Beverages and tobacco",
                                       "Tobacco products": "Beverages and tobacco"}.get(c, ""),
                        Cbar_usd_month=m["Cbar"][c], vatable_usd_month=B.US_VAT_FLAGS[c] * m["Cbar"][c],
                        n_high_rse_cells=m["prov"].loc[c, "n_high_rse"], high_rse_deciles=m["prov"].loc[c, "high_rse_groups"]))
for k in B.NOT_BUDGET:
    v = vals.loc[f"{B.EXP} > {B.NOT_BUDGET[k][0]}", DEC] / 12 / u["shares"]
    fl_rows.append(dict(category=k, role="outside budget", ce_source=B.NOT_BUDGET[k][0], vat_flag=np.nan, vat_flag_start=np.nan,
                        vat_reason="not consumption", vat_pinned_by="Fig 4: D1 +4.8% and D10 -3.9% of budget (us_budget_tests.csv)",
                        usda_group="", usda_reason="outside consumption", food_subgroup="",
                        Cbar_usd_month=float(v @ m["w"]), vatable_usd_month=0.0, n_high_rse_cells=np.nan, high_rse_deciles=""))
flags_out = pd.DataFrame(fl_rows)
flags_out["n_high_rse_cells"] = flags_out["n_high_rse_cells"].astype("Int64")
flags_out.to_csv(OUT / "us_flags.csv", index=False, float_format="%.4f")

# %% step 11: sensitivity of the headline numbers to the inputs the table cannot pin
def headline(mm, net, mpc=None, label=""):
    mpc = B.mpc_mid() if mpc is None else mpc
    s = B.shifts_from_transfers(mm, net, mpc=mpc)
    ii = B.impulse(mm, net, mpc)
    gap = (s.loc[CH, "dUSD_mpc"] - PUB5["pub_usd"])
    return dict(variant=label, dividend=np.nan,
                D1_net=float(net.iloc[0]), D8_net=float(net.iloc[7]), D10_net=float(net.iloc[-1]),
                rent=s.loc["Rented dwellings", "dUSD_mpc"], health_ins=s.loc["Health insurance", "dUSD_mpc"],
                new_cars=s.loc["Cars and trucks, new", "dUSD_mpc"], used_cars=s.loc["Cars and trucks, used", "dUSD_mpc"],
                new_cars_ghost=s.loc["Cars and trucks, new", "dUSD_mpc1"], used_cars_ghost=s.loc["Cars and trucks, used", "dUSD_mpc1"],
                impulse_pct=ii["flow_pct_consumption"], bars_rmse=float(np.sqrt((gap ** 2).mean())))


def variant_cols(v):
    """The step-5b columns: labels exact, label SSE, the two objective terms, and the Fig 5 refit (knee step 0.01)."""
    return dict(labels_exact=v["labels_exact"], label_sse=v["label_sse"], fig4_printed_term=v["printed_term"],
                fig4_readoff_term=v["x_term"], refit_knee=v["refit"][1], refit_top=v["refit"][2], refit_rmse=v["refit"][0])


rows = [headline(m, NET, label="rebuild as calibrated")]
rows[-1]["dividend"] = float(acc["dividend"].iloc[0])
rows[-1].update(variant_cols(va))
a_s = B.vat_accounting(m, B.US_VAT_START)
rows.append(headline(m, a_s["net"], label="START flags (Directive + Table 2500, used cars and water at 1)"))
rows[-1]["dividend"] = float(a_s["dividend"].iloc[0])
MPC_R0 = B.mpc_knee(vr["refit"][1], vr["refit"][2])
rows.append(headline(m, vr["acc"]["net"], mpc=MPC_R0, label=f"rent flag 0 (the post's 'rent exempt'), MPC refit (knee "
                     f"{vr['refit'][1]:.2f}, top {vr['refit'][2]:.4f}): an equally good alternative"))
rows[-1].update(dividend=vr["dividend"], **variant_cols(vr))
rows.append(headline(m, vu["acc"]["net"], label="used cars 0.1 (Directive margin scheme, Arts. 311-325), MPC mid: sensitivity"))
rows[-1].update(dividend=vu["dividend"], **variant_cols(vu))
# every bar of the two variants beside the adopted ones (rent 0 at its own refit, used cars 0.1 at the mid schedule)
fv = pd.DataFrame({"role": m["prov"]["role"], "pub_usd": PUB5["pub_usd"], "pub_ghost": PUB5["pub_ghost"]})
for tag, v, mp in [("adopted", va, sched["mid"].values), ("rent_0_refit", vr, MPC_R0), ("used_cars_0.1", vu, sched["mid"].values)]:
    s_ = B.shifts_from_transfers(m, v["acc"]["net"], mpc=mp)
    fv[f"dUSD_{tag}"], fv[f"dPct_{tag}"], fv[f"ghost_{tag}"] = s_["dUSD_mpc"], s_["dPct_mpc"], s_["dUSD_mpc1"]
fv = fv.loc[list(PUB5.index) + [c for c in m["C"].index if c not in PUB5.index]]
fv.index.name = "category"
assert np.allclose(fv["dUSD_adopted"], ds.loc[fv.index, "dUSD_mid"], rtol=0, atol=1e-12)
fv.to_csv(OUT / "us_flag_variants.csv", float_format="%.5f")
_g = lambda c: float(np.sqrt(((fv.loc[CH, c] - fv.loc[CH, "pub_usd" if c.startswith("dUSD") else "pub_ghost"]) ** 2).mean()))
print(f"\nflag variants, Fig 5 (us_flag_variants.csv): bars RMSE adopted ${_g('dUSD_adopted'):.4f}, rent 0 at its refit "
      f"${_g('dUSD_rent_0_refit'):.4f}, used cars 0.1 at mid ${_g('dUSD_used_cars_0.1'):.4f}; ghosts RMSE "
      f"${_g('ghost_adopted'):.4f} / ${_g('ghost_rent_0_refit'):.4f} / ${_g('ghost_used_cars_0.1'):.4f}; largest |bar change| "
      f"rent 0 ${(fv['dUSD_rent_0_refit'] - fv['dUSD_adopted']).abs().max():.3f}, used cars 0.1 "
      f"${(fv['dUSD_used_cars_0.1'] - fv['dUSD_adopted']).abs().max():.3f} "
      f"({(fv['dUSD_used_cars_0.1'] - fv['dUSD_adopted']).abs().idxmax()})")
rows.append(headline(m, PUB_NET, label="published Fig 4 labels as nets"))
rows[-1]["dividend"] = PUB_DIV
for fmap in ["A2", "B", "F"]:
    rows.append(headline(B.build_model(2024, food_map=fmap), NET, label=f"food split {fmap}"))
rows.append(headline(B.build_model(2024, params=B.usda_params(True)), NET, label="back-solved TB-1929 betas"))
rows.append(headline(m, NET, mpc=B.mpc_knee(2.0, int_knees[2.0][0]), label=f"MPC knee 2, top {int_knees[2.0][0]}"))
rows.append(headline(m, NET, mpc=B.mpc_knee(3.0, int_knees[3.0][0]), label=f"MPC knee 3, top {int_knees[3.0][0]}"))
# payment-unit rounding: People and Children under 18 print to one decimal; draw each uniformly within +/-0.05
rng = np.random.default_rng(20261102)
mc = []
base_vals = m["vals"]
for draw in tqdm(range(300), desc="payment-unit rounding draws", leave=False):
    vv = base_vals.copy()
    vv.loc[B.PEOPLE, DEC] = base_vals.loc[B.PEOPLE, DEC] + rng.uniform(-0.05, 0.05, 10)
    vv.loc[B.CHILDREN, DEC] = base_vals.loc[B.CHILDREN, DEC] + rng.uniform(-0.05, 0.05, 10)
    uu = B.payment_units(vv)
    C2 = m["spend"].div(uu["shares"] * 12.0, axis=1)
    mm = dict(m, units=uu, w=uu["w"], C=C2, budget=C2.sum(), Cbar=C2 @ uu["w"], budget_bar=float(C2.sum() @ uu["w"]))
    mm["theta"] = B.theta_table(C2, uu["w"])
    mm["eta"], mm["eta_detail"] = B.eta_table(mm)
    a2 = B.vat_accounting(mm)
    h = headline(mm, a2["net"])
    h["dividend"] = float(a2["dividend"].iloc[0])
    h["labels_exact"] = int((np.round(a2["net"]) == PUB_NET).sum())
    mc.append(h)
mc = pd.DataFrame(mc)
for q, lab in [(0.05, "payment-unit rounding draws, 5th percentile"), (0.5, "payment-unit rounding draws, median"),
               (0.95, "payment-unit rounding draws, 95th percentile")]:
    r = mc.drop(columns=["variant"]).quantile(q).to_dict()
    r["variant"] = lab
    rows.append(r)
sens = pd.DataFrame(rows)
sens.to_csv(OUT / "us_sensitivity.csv", index=False, float_format="%.4f")
print("\nstep 11, sensitivity:")
print(sens[["variant", "dividend", "D8_net", "D10_net", "rent", "new_cars", "used_cars", "impulse_pct", "bars_rmse"]].round(3).to_string(index=False))
print(f"   payment-unit draws: labels exact median {mc['labels_exact'].median():.0f}/10, "
      f"share of draws with all 10 exact {(mc['labels_exact'] == 10).mean():.2f}")
print(f"   monotone per-decile mid (diagnostic, Fig 5 + Fig 6): {np.round(mpc_mono, 3).tolist()}; bars RMSE "
      f"${bar_rmse(mpc_mono):.4f}, segments RMSE ${seg_rmse(mpc_mono):.4f} (knee fit: ${bar_rmse(sched['mid'].values):.4f}, "
      f"${seg_rmse(sched['mid'].values):.4f}); impulse {impulse_pct(mpc_mono):.3f}%")

# %% step 12: figures (light mode, PNG at 200 dpi). Palette and mark specs from the dataviz skill's reference
# instance: one series hue (slot-1 blue), ink for published values, hairline recessive grid, 2px gaps.
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch, Rectangle

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, BLUE_L, BLUE_D, BAND = "#2a78d6", "#9ec5f4", "#104281", "#f0efec"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "savefig.facecolor": SURF})


def style_axes(ax, grid_axis="x"):
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
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
    if (x1 - x0) <= 2.2 * rx:                       # too short to round: a plain block
        ax.add_patch(Rectangle((x0, yc - h / 2), x1 - x0, h, facecolor=color, edgecolor="none", zorder=3))
        return
    ax.add_patch(FancyBboxPatch((x0, yc - h / 2), x1 - x0, h, boxstyle=f"round,pad=0,rounding_size={rx}",
                                mutation_aspect=ppx / ppy, facecolor=color, edgecolor="none", zorder=3))
    sq = (0, v / 2) if v > 0 else (v / 2, 0)        # square off the baseline half
    ax.add_patch(Rectangle((min(sq), yc - h / 2), abs(sq[1] - sq[0]), h, facecolor=color, edgecolor="none", zorder=3))


# --- Fig 5 rebuilt
cats = list(PUB5.index)
n = len(cats)
yy = np.arange(n)[::-1].astype(float)
fig = plt.figure(figsize=(13.0, 13.2), dpi=200)
axL = fig.add_axes([0.255, 0.085, 0.50, 0.76])
axR = fig.add_axes([0.79, 0.085, 0.18, 0.76], sharey=axL)
axL.set_xlim(-1.5, 5.6)
axL.set_ylim(-0.8, n - 0.2)
style_axes(axL)
axL.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
fig.canvas.draw()
for c, yc in zip(cats, yy):
    g = ds.loc[c, "dUSD_mpc1"]
    axL.add_patch(Rectangle((min(0, g), yc - 0.33), abs(g), 0.66, facecolor="none", edgecolor=MUTED, linewidth=0.9, zorder=2))
    hbar_rounded(axL, yc, ds.loc[c, "dUSD_mid"], 0.40, BLUE)
    axL.plot([PUB5.loc[c, "pub_usd"]] * 2, [yc - 0.27, yc + 0.27], color=INK, linewidth=1.6, zorder=5, solid_capstyle="butt")
    axL.plot(PUB5.loc[c, "pub_ghost"], yc, marker="D", markersize=4.2, markerfacecolor=SURF, markeredgecolor=INK,
             markeredgewidth=1.0, zorder=6, linestyle="none")
axL.set_yticks(yy)
axL.set_yticklabels(cats, fontsize=8.6)
axL.set_xlabel("Change in spending, \\$ per adult share per month", fontsize=9, color=INK2)
for c in ["Rented dwellings", "Cars and trucks, new", "Cars and trucks, used"]:
    yc = yy[cats.index(c)]
    v = ds.loc[c, "dUSD_mid"]
    xt = max(v, ds.loc[c, "dUSD_mpc1"], 0) + 0.08
    axL.text(xt, yc, f"{v:+.2f} rebuilt / {PUB5.loc[c, 'pub_usd']:+.2f} published\nMPC=1: {ds.loc[c, 'dUSD_mpc1']:+.2f} / "
             f"{PUB5.loc[c, 'pub_ghost']:+.2f}", va="center", fontsize=7.4, color=INK2, linespacing=1.15)
style_axes(axR)
axR.axvspan(-0.005, 0.005, color=BAND, zorder=0, linewidth=0)
for xv in (-0.01, 0.01):
    axR.axvline(xv, color=GRID, linewidth=0.8, zorder=1)
axR.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
axR.plot(ds.loc[cats, "gap_ghost"].values, yy, marker="D", markersize=4.2, markerfacecolor=SURF, markeredgecolor=MUTED,
         markeredgewidth=1.0, linestyle="none", zorder=3)
axR.plot(ds.loc[cats, "gap_usd"].values, yy, marker="o", markersize=4.6, markerfacecolor=BLUE, markeredgecolor=SURF,
         markeredgewidth=1.0, linestyle="none", zorder=4)
axR.set_xlim(-0.03, 0.03)
axR.set_xticks([-0.02, 0, 0.02])
axR.set_xticklabels(["−0.02", "0", "+0.02"])
axR.tick_params(axis="y", labelleft=False)
axR.set_xlabel("Rebuilt minus published, \\$", fontsize=9, color=INK2)
axR.text(0, n - 0.05, "shaded: ±0.005, the bar labels' rounding", ha="center", va="bottom", fontsize=7.4, color=INK2)
fig.text(0.255, 0.962, "Fig 5 rebuilt: US impact-period demand shifts under the 15-point VAT bridge", fontsize=13.5,
         color=INK, ha="left", weight="bold")
fig.text(0.255, 0.946, f"CE 2024 deciles, Working-model elasticities (TB-1929), MPC mid schedule (1.0 through decile {k_mid:g}, "
         f"linear to {t_mid:g} at D10).\nAll 36 bars land within ±\\$0.005 of the printed labels (RMSE \\${rm_min:.4f}).\n"
         f"MPC=1 ghosts: RMSE \\${np.sqrt((ds.loc[CH, 'gap_ghost'] ** 2).mean()):.3f} against ±0.01 read-offs, largest gap "
         f"{ds.loc[CH, 'gap_ghost'].abs().idxmax().lower()} {ds.loc[ds.loc[CH, 'gap_ghost'].abs().idxmax(), 'gap_ghost']:+.3f}.",
         fontsize=9.2, color=INK2, ha="left", va="top", linespacing=1.35)
handles = [Patch(facecolor=BLUE, edgecolor="none", label="rebuilt, MPC mid schedule"),
           Patch(facecolor="none", edgecolor=MUTED, label="rebuilt, MPC = 1 (ghost)"),
           Line2D([0], [0], color=INK, linewidth=1.6, label="published bar label"),
           Line2D([0], [0], marker="D", markersize=4.6, markerfacecolor=SURF, markeredgecolor=INK, linestyle="none",
                  label="published ghost (read off Fig 5, ±0.01)"),
           Line2D([0], [0], marker="o", markersize=5, markerfacecolor=BLUE, markeredgecolor=SURF, linestyle="none",
                  label="gap, MPC mid bar"),
           Line2D([0], [0], marker="D", markersize=4.6, markerfacecolor=SURF, markeredgecolor=MUTED, linestyle="none",
                  label="gap, ghost")]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.255, 0.898), ncol=3, frameon=False, fontsize=8.2,
           handlelength=1.6, columnspacing=1.6, labelcolor=INK2)
fig.text(0.255, 0.022, "Rebuilt in consumption/rebuild (bridge.py, run_us.py) from BLS CE 2024 Table 1110 and USDA ERS TB-1929 "
         "Tables 3-4.\nPublished values: bar labels and outlines of Fig 5 in the 2026-06-14 post (post_published_numbers.csv). "
         "Same category order as the published figure.", fontsize=7.4, color=MUTED, ha="left", linespacing=1.3)
fig.savefig(FIG / "fig5_rebuilt.png", dpi=200)
plt.close(fig)

# --- MPC fit surface and schedules
fig = plt.figure(figsize=(13.0, 5.6), dpi=200)
ax1 = fig.add_axes([0.06, 0.13, 0.40, 0.70])
ax2 = fig.add_axes([0.56, 0.13, 0.41, 0.70])
R = np.sqrt(S / len(CH))
levels = [0.003, 0.005, 0.01, 0.02, 0.04, 0.08]
ramp = ["#104281", "#1c5cab", "#2a78d6", "#5598e7", "#86b6ef", "#b7d3f6"]
cs = ax1.contour(TOPS, KNEES, R, levels=levels, colors=ramp, linewidths=1.4)
ax1.clabel(cs, levels=[0.01, 0.02, 0.04, 0.08], fmt=lambda v: f"\\${v:g}", fontsize=7.2, inline_spacing=3)
ax1.plot(t_mid, k_mid, marker="o", markersize=7, markerfacecolor=INK, markeredgecolor=SURF, markeredgewidth=1.5, zorder=5)
ax1.annotate(f"best: knee {k_mid:g}, top {t_mid:g}\nRMSE \\${rm_min:.4f}", (t_mid, k_mid), xytext=(0.445, 6.6),
             fontsize=8, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8))
for k, (tb, rr) in int_knees.items():
    ax1.plot(tb, k, marker="o", markersize=5, markerfacecolor=SURF, markeredgecolor=INK2, markeredgewidth=1.0, zorder=4)
for nm, mk in [("low", "<"), ("high", ">")]:
    ax1.plot(B.US_MPC_TOP[nm], B.US_MPC_KNEE[nm], marker=mk, markersize=7, markerfacecolor=BLUE_L, markeredgecolor=BLUE_D,
             markeredgewidth=1.0, zorder=5, clip_on=False)
    ax1.text(B.US_MPC_TOP[nm] + (0.006 if nm == "low" else -0.006), B.US_MPC_KNEE[nm] + 0.35,
             f"{nm}: Fig 7 edge", fontsize=7.4, color=INK2, ha="left" if nm == "low" else "right")
style_axes(ax1, grid_axis="both")
ax1.set_xlabel("MPC of the top decile (top)", fontsize=9)
ax1.set_ylabel("knee: last decile at MPC 1.0", fontsize=9)
ax1.set_xlim(0.40, 0.65)
ax1.set_ylim(1, 9)
ax1.set_title("Fit surface: RMSE of the 36 Fig 5 dollar bars (contours \\$0.003 to \\$0.08)", fontsize=10.5, color=INK, loc="left")
ax1.legend(handles=[Line2D([0], [0], marker="o", markersize=7, markerfacecolor=INK, markeredgecolor=SURF, linestyle="none",
                           label="best fit (mid schedule)"),
                    Line2D([0], [0], marker="o", markersize=5, markerfacecolor=SURF, markeredgecolor=INK2, linestyle="none",
                           label="best top at knee 1, 2, 3, 4, 5"),
                    Line2D([0], [0], marker=">", markersize=7, markerfacecolor=BLUE_L, markeredgecolor=BLUE_D, linestyle="none",
                           label="low / high schedules (knees from Fig 7)")],
           loc="upper right", frameon=False, fontsize=7.6, labelcolor=INK2)
dd = np.arange(1, 11)
ax2.plot(dd, sched["low"].values, color=BLUE_L, linewidth=1.6, zorder=3)
ax2.plot(dd, sched["high"].values, color=BLUE_L, linewidth=1.6, zorder=3)
ax2.plot(dd, sched["mid"].values, color=BLUE, linewidth=2.2, zorder=4, marker="o", markersize=5,
         markerfacecolor=BLUE, markeredgecolor=SURF, markeredgewidth=1.2)
ax2.plot(dd, mpc_mono, color=INK2, linewidth=0, marker="s", markersize=4.4, markerfacecolor=SURF,
         markeredgecolor=INK2, markeredgewidth=1.0, zorder=5)
ax2.plot(dd, fig6_mpc.values, linewidth=0, marker="D", markersize=4.4, markerfacecolor=SURF, markeredgecolor=INK,
         markeredgewidth=1.0, zorder=6)
ax2.text(10.15, sched["low"].values[-1], "low (top 0.40)", va="center", fontsize=7.8, color=INK2)
ax2.text(10.15, sched["mid"].values[-1], f"mid (top {t_mid:g})", va="center", fontsize=7.8, color=INK2)
ax2.text(10.15, sched["high"].values[-1], "high (top 0.65)", va="center", fontsize=7.8, color=INK2)
style_axes(ax2, grid_axis="both")
ax2.set_xlim(0.6, 11.4)
ax2.set_ylim(0.35, 1.05)
ax2.set_xticks(dd)
ax2.set_xticklabels([f"D{i}" for i in dd])
ax2.set_ylabel("MPC out of the net transfer", fontsize=9)
ax2.set_title("The schedules, and what Fig 6's segments imply", fontsize=10.5, color=INK, loc="left")
ax2.legend(handles=[Line2D([0], [0], color=BLUE, linewidth=2.2, marker="o", markersize=5, markeredgecolor=SURF,
                           label="mid: knee fit to Fig 5"),
                    Line2D([0], [0], color=BLUE_L, linewidth=1.6, label="low / high: knees pinned by Fig 7"),
                    Line2D([0], [0], marker="s", markersize=4.4, markerfacecolor=SURF, markeredgecolor=INK2,
                           linestyle="none", label="monotone per-decile fit, Fig 5 + Fig 6 (diagnostic)"),
                    Line2D([0], [0], marker="D", markersize=4.4, markerfacecolor=SURF, markeredgecolor=INK,
                           linestyle="none", label="Fig 6 segments alone, decile by decile")],
           loc="lower left", frameon=False, fontsize=7.8, labelcolor=INK2)
fig.text(0.06, 0.93, "MPC schedule: flat at 1.0 to a knee decile, then linear to the top value", fontsize=12.5,
         color=INK, weight="bold")
fig.text(0.06, 0.035, "Rebuilt nets and elasticities (consumption/rebuild/code/run_us.py); grid: knee 1-9 by 0.05, top 0.40-0.65 by "
         "0.0025. Fig 6 points are diagnostics, not used in the knee fit.", fontsize=7.4, color=MUTED)
fig.savefig(FIG / "us_mpc_fit.png", dpi=200)
plt.close(fig)
print("figures: fig5_rebuilt.png, us_mpc_fit.png")
