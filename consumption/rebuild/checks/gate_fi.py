# gate_fi.py - the Finland gate: every published Finnish number in post_published_numbers.csv that the rebuilt
# static machinery should reproduce (text, Fig 1, Fig 2 labels and ghosts, Fig 3 labels, diamonds and segments),
# beside the rebuilt value, the gap and a status. Finnish rows the static rebuild cannot or should not reproduce
# (inputs, axis ticks, labels, data vintages, the Fig 10 wealth block) are listed with status 'not gated' and the
# reason, so every Finnish row is accounted for.
#
# Status (as in gate_us.py): PASS = within the printed rounding (half a unit of the last printed digit; for read-off
# values the precision stated in the row's note; number words +/-0.5; fraction words +/-5 points, or +/-0.05 for a
# ratio); CLOSE = within 10% of the published value or within EUR 0.05; MISS otherwise. Counts and yes/no claims
# must match exactly; an upper-bound claim ('within EUR 5') passes when the rebuilt value is inside the bound.
# Role: calibration = used to pin a parameter (the VAT-flag grid and the population weights: Fig 1); selection =
# used to choose between discrete alternatives (Fig 2 ghosts: elasticity parents and food system; Fig 2 EUR labels:
# their ratio to the percent labels chose the euro conversion); check = used for nothing. The MPC schedule is the
# US decile schedule averaged to quintiles, so no Finnish number pinned it.
#
# Run from the repo root:  venv/bin/python -I consumption/rebuild/checks/gate_fi.py
# Rebuilds the model from bridge.py's constants (what the LVT step imports), not from run_fi.py's outputs, and checks
# that run_fi.py's fi_demand_shifts.csv agrees with it.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                     # consumption/rebuild/checks
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "code"))

import re

import numpy as np
import pandas as pd

import bridge as B

OUT = B.REBUILD / "out"
Q = B.FI_Q
G = pd.read_csv(B.TIDY / "post_published_numbers.csv")

# %% the rebuilt quantities
m = B.build_fi_model()
acc = B.fi_vat_accounting(m)
NET = acc["net"]
sched = B.fi_mpc_schedules()
MID = sched["mid"].values
sh = B.shifts_from_transfers(m, NET, mpc=MID)
EUR = B.fi_post_eur(m, sh["dUSD_mpc"])                      # the post's EUR units (Cbar from the total column)
PCT = sh["dPct_mpc"]
GHOST = B.fi_post_eur(m, sh["dUSD_mpc1"])
SEG = B.fi_post_eur(m, B.decompose(m, B.budget_shock(NET, MID, m["budget"])))
CH = m["chart"]
charted_budget = float(m["Cbar_post"].loc[CH].sum())
imp = B.impulse(m, NET, MID)
top10 = B.top_movers(pd.DataFrame({"x": EUR}), "x", CH, 10)
m_hh = B.build_fi_model(convention="coherent")             # per-household budget shares (the text's food eta)
gain = NET > 0
recv_mpc = float((m["w"] * NET * MID)[gain].sum() / (m["w"] * NET)[gain].sum())
wealth = pd.read_csv(B.TIDY / "fi_wealth_2023_deciles.csv")
nw = wealth[(wealth["component"] == "net_wealth") & (wealth["measure"] == "mean")].set_index("decile")["value"]
q5_networth_per_cu = (nw["d09"] + nw["d10"]) / 2 / m["units"].loc["q5", "hh_per_cu_ratio"]
_r = lambda x: f"{x.min():.1f}-{x.max():.1f}"
RANGES_NOTE = (f"no rebuilt quantity spans 3-8%: |net|/budget {_r(acc['net_pct_budget'].abs())}, dividend/budget "
               f"{_r(100 * acc['dividend'] / acc['budget'])}, extra VAT/budget {_r(100 * acc['tax'] / acc['budget'])}")

ds_file = pd.read_csv(OUT / "fi_demand_shifts.csv", index_col=0)
assert np.allclose(ds_file.loc[CH, "dEUR_mid"].values, EUR.loc[CH].values, atol=1e-5)   # file keeps 5 decimals

# %% tolerance helpers
WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def num_tokens(s):
    s = str(s).replace("−", "-").replace(",", "")
    return re.findall(r"[-+]?\d+(?:\.\d+)?k?", s)


def printed_tol(row):
    """Half a unit of the last printed digit of the number matching the row's value; None if no digits."""
    v = abs(float(row["value"]))
    for t in num_tokens(row["printed"]):
        k = t.endswith("k")
        x = abs(float(t.rstrip("k"))) * (1000 if k else 1)
        for scale in (1, 100, 0.01):
            if abs(x * scale - v) < 1e-9:
                dec = len(t.rstrip("k").split(".")[1]) if "." in t else 0
                return 0.5 * 10 ** (-dec) * scale * (1000 if k else 1)
    return None


def readoff_tol(row):
    mt = re.search(r"±\s*([0-9.]+)", str(row["note"]))
    return float(mt.group(1)) if mt else None


def tolerance(row):
    if str(row["confidence"]) == "high" and isinstance(row["printed"], str) and row["printed"].strip():
        t = printed_tol(row)
        if t is not None:
            return t, "printed rounding"
        words = [w for w in re.findall(r"[a-z]+", row["printed"].lower()) if w in WORDS]
        if any(WORDS[w] == abs(float(row["value"])) for w in words):
            return (0.0, "number word") if row["unit"] == "count" else (0.5, "number word")
        if row["unit"] == "%":
            return 5.0, "fraction word (+/-5 points)"
        if row["unit"] == "ratio":
            return 0.05, "fraction word (+/-0.05)"
        return 0.0, "count word"
    t = readoff_tol(row)
    if t is not None:
        return t, "read-off precision from note"
    return 5.0 if row["unit"] == "EUR" else 0.01, "read-off (default)"


# %% map every Finnish row to a rebuilt value (or a reason it is not gated)
F1, F2, F3, F10 = ("fig1_net_transfer_fi2022.png", "fig2_demand_shifts_fi2022_mpc.png",
                   "fig3_composition_shift_fi2022_mpc.png", "fig10_wealth_block_paths_fi.png")
QOF = {f"FI Q{i}": f"q{i}" for i in range(1, 6)}


def rebuilt(row):
    """(value, role, scope, note, alt_value, alt_note) or (None, reason)."""
    i, src, q, it, grp = row["id"], row["source"], str(row["quantity"]), str(row["item"]), str(row["group"])
    if "axis tick" in q:
        return None, "axis tick (scale only)"
    if src == F1:
        if i == "P079":
            return float(acc["dividend"].iloc[0]), "calibration", "Fig 1", "dividend = tau x weighted mean VAT-able", None, ""
        if q == "net transfer per adult share per month":
            return float(NET[QOF[grp]]), "calibration", "Fig 1", "", None, ""
        if q == "net transfer as % of budget":
            return float(acc["net_pct_budget"][QOF[grp]]), "calibration", "Fig 1", "", None, ""
        if q.startswith("VAT-able consumption per adult share per month (x-position)"):
            return float(acc["vatable"][QOF[grp]]), "calibration", "Fig 1", "point position", None, ""
        if q.startswith("mean VAT-able consumption"):
            return float(acc["Cbar_v"].iloc[0]), "calibration", "Fig 1", "dashed line", None, ""
        if q.startswith("group definition"):
            u = m["units"]
            return (100 * float(u.loc[QOF[grp], "households"] / u.loc["total", "households"]), "check", "Fig 1",
                    "HBS 14qa households in the quintile / all households (data)", None, "")
        return None, "input or label (rate, survey year, payment weight, table identifiers)"
    if src == F2:
        if q.startswith("change in spending per adult share per month"):
            return (float(EUR[it]), "selection", "Fig 2", "bar label (MPC mid, post EUR); EUR/percent ratio chose the euro "
                    "conversion", None, "")
        if q.startswith("percent change in category spending"):
            return float(PCT[it]), "check", "Fig 2", "percent label (MPC mid)", None, ""
        if q == "MPC=1 benchmark (ghost) value":
            return float(GHOST[it]), "selection", "Fig 2", "outline (MPC=1)", None, ""
        return None, "input (MPC of the benchmark)"
    if src == F3:
        if q.startswith("quintile contribution"):
            return float(SEG.loc[it, QOF[grp]]), "check", "Fig 3 segment", "quintile contribution, MPC mid", None, ""
        if q.startswith("change in spending per adult share per month"):
            return float(EUR[it]), "check", "Fig 3 label", "net label / solid diamond (MPC mid)", None, ""
        if q == "MPC=1 benchmark (ghost) value":
            return float(GHOST[it]), "check", "Fig 3 label", "hollow diamond (MPC=1)", None, ""
        return None, "input or label"
    if src == F10:
        return None, "wealth block (Fig 10): outside this static rebuild"
    if src == "text":
        if i == "P070":
            return float(acc["dividend"].iloc[0]), "calibration", "text", "", None, ""
        if i in ("P072", "P074"):
            return float(NET[QOF[grp]]), "calibration", "text", "", None, ""
        if i in ("P073", "P075"):
            return float(acc["net_pct_budget"][QOF[grp]]), "calibration", "text", "", None, ""
        if i == "P076":
            return float(abs(NET["q3"])), "calibration", "text", "|net| of the middle quintile (upper-bound claim)", None, ""
        if i == "P104":
            return float(acc["vatable_pct_budget"]["q1"]), "calibration", "text", "Q1 VAT-able share of the budget", None, ""
        if i == "P105":
            v = acc["vatable_pct_budget"]
            return (float(v[["q2", "q3", "q4", "q5"]].mean()), "check", "text", "mean VAT-able share, Q2-Q5",
                    float(v[["q4", "q5"]].mean()), "Q4-Q5 only")
        if i in ("P109", "P110"):
            q_ = "q1" if i == "P109" else "q5"
            return (float(m["eta"].loc["01.1 Food (at home)", q_]), "check", "text",
                    "food-at-home eta at per-CU shares (the figures' basis)",
                    float(m_hh["eta"].loc["01.1 Food (at home)", q_]), "at per-household budget shares")
        if i == "P112":
            return 100 * recv_mpc, "check", "text", "net-receipt-weighted MPC of the gaining quintiles (mid)", None, ""
        if i == "P113":
            return (100 * float(EUR.loc[CH].sum()) / charted_budget, "check", "text", "charted bars / charted budget",
                    imp["flow_pct_consumption"], "flow impulse sum_q w_q mpc_q net_q / consumption")
        if i == "P114":
            return float(MID[-1]), "check", "text", "MPC of Q5 (mid): the top's withdrawal relative to MPC=1", None, ""
        if i == "P115":
            return float(EUR.loc[CH].abs().max()), "check", "text", f"largest |bar| ({EUR.loc[CH].abs().idxmax()})", None, ""
        if i == "P116":
            return (m["budget_bar_post"], "check", "text", "budget per share, total column (the post's euro conversion)",
                    m["budget_bar"], "weighted mean of the quintile budgets (equal-CU weights)")
        if i == "P117":
            return (float(abs(acc["net_pct_budget"]["q5"])), "check", "text", "|net| / budget of the top quintile", None,
                    RANGES_NOTE)
        if i == "P118":
            return (float(abs(acc["net_pct_budget"]["q1"])), "check", "text", "|net| / budget of the bottom quintile", None,
                    RANGES_NOTE)
        if i in ("P119", "P234", "P239"):
            return float(EUR["04.1 Actual rents"]), "check", "text", "= Fig 2 '04.1 Actual rents' bar", None, ""
        if i == "P238":
            return float(EUR["07.1 Purchase of vehicles"]), "check", "text", "= Fig 2/3 '07.1 Purchase of vehicles'", None, ""
        if i == "P233":
            return (100 * float(m["Cbar_post"]["10 Education services (off-chart)"]) / m["budget_bar_post"], "check", "text",
                    "education's share of the budget (total column)", None, "")
        if i in ("P235", "P263"):
            pub = set(G[(G["source"] == F3) & G["quantity"].str.startswith("quintile contribution")]["item"])
            return float(len(set(top10) & pub)), "check", "text", "rebuilt ten largest movers that are in the published set", None, ""
        if i == "P236":
            return float((NET < 0).sum()), "check", "text", "quintiles with net < 0", None, ""
        if i == "P237":
            return float((NET > 0).sum()), "check", "text", "quintiles with net > 0", None, ""
        if i == "P963":
            return float(len(NET)), "check", "text", "quintile points", None, ""
        if i == "P886":
            return (float(q5_networth_per_cu), "check", "text", "(D9 + D10)/2 mean net wealth (vtutk 151u) / the Q5 "
                    "per-household/per-CU ratio r_q5: footnote 30's bridge, the conversion bridge.py uses", None, "")
        if i in ("P067", "P103", "P876", "P877", "P906", "P907", "P928"):
            return None, "data vintage"
        if i in ("P069", "P100", "P071", "P101", "P102", "P111", "P232", "P264"):
            return None, "input (rate, payment weights, MPC of the benchmark)"
        if i == "P107":
            return None, "structural description (the 37 charted categories are COICOP 2018 groups, level 2, by construction)"
        return None, "wealth block (Fig 10 text: lambda scenarios, wealth ratios): outside this static rebuild"
    return None, "not a Finnish row of the static rebuild"


def is_fi(row):
    if row["source"] in (F1, F2, F3, F10):
        return True
    return row["source"] == "text" and str(row["group"]).startswith("FI")


rows = []
for _, r in G[G.apply(is_fi, axis=1)].iterrows():
    res = rebuilt(r)
    base = dict(id=r["id"], source=r["source"], locator=r["locator"], item=r["item"], group=r["group"],
                quantity=r["quantity"], published=r["value"], unit=r["unit"], printed=r["printed"],
                confidence=r["confidence"])
    if res[0] is None:
        rows.append(dict(base, status="not gated", reason=res[1]))
        continue
    val, role, scope, note, alt, altnote = res
    tol, tol_kind = tolerance(r)
    gap = val - float(r["value"])
    exact = r["unit"] in ("count",)
    if exact:
        status = "PASS" if abs(gap) < 1e-9 else "MISS"
        tol_kind = "exact"
    elif r["id"] == "P076":                                   # upper bound: 'within EUR 5 of break-even'
        status = "PASS" if val <= float(r["value"]) + 1e-9 else ("CLOSE" if val <= 1.1 * float(r["value"]) else "MISS")
        tol_kind = "upper bound"
    elif abs(gap) <= tol + 1e-9:
        status = "PASS"
    elif abs(gap) <= 0.10 * abs(float(r["value"])) + 1e-12 or (r["unit"] == "EUR" and abs(gap) <= 0.05 + 1e-12):
        status = "CLOSE"
    else:
        status = "MISS"
    alt_status = ""
    if alt is not None:
        ag = alt - float(r["value"])
        alt_status = "PASS" if abs(ag) <= tol + 1e-9 else ("CLOSE" if abs(ag) <= 0.10 * abs(float(r["value"])) else "MISS")
    rows.append(dict(base, rebuilt=val, gap=gap, rel_gap=gap / float(r["value"]) if float(r["value"]) else np.nan,
                     tolerance=tol, tolerance_kind=tol_kind, status=status, role=role, scope=scope, note=note,
                     alt_rebuilt=alt, alt_status=alt_status, alt_note=altnote))
gate = pd.DataFrame(rows)
gate.to_csv(OUT / "gate_fi.csv", index=False, float_format="%.5f")

# %% summary
gated = gate[gate["status"] != "not gated"]
order = ["Fig 1", "Fig 2", "Fig 3 label", "Fig 3 segment", "text"]
tab = gated.pivot_table(index="scope", columns="status", values="id", aggfunc="count", fill_value=0).reindex(order)
tab = tab.reindex(columns=["PASS", "CLOSE", "MISS"], fill_value=0).fillna(0).astype(int)
tab["total"] = tab.sum(axis=1)
tab.loc["all gated"] = tab.sum()
role_tab = gated.pivot_table(index="role", columns="status", values="id", aggfunc="count", fill_value=0)
role_tab = role_tab.reindex(columns=["PASS", "CLOSE", "MISS"], fill_value=0)
print(f"FI gate: {len(gate)} Finnish rows in the gate list; {len(gated)} gated, {int((gate['status'] == 'not gated').sum())} not gated")
print(tab.to_string())
print("\nby role (calibration = used to pin a parameter; selection = used to choose a discrete variant):")
print(role_tab.to_string())
core = gated[gated["scope"].isin(["Fig 1", "Fig 2", "Fig 3 label", "text"])]
cnt = core["status"].value_counts().reindex(["PASS", "CLOSE", "MISS"], fill_value=0)
print(f"\nheadline scope (text, Fig 1, Fig 2, Fig 3 labels and diamonds): {cnt['PASS']} PASS, {cnt['CLOSE']} CLOSE, "
      f"{cnt['MISS']} MISS of {len(core)}")
bad = gated[gated["status"] != "PASS"].copy()
bad["abs_rel"] = bad["rel_gap"].abs()
print("\nnot PASS (sorted by status, then |relative gap|):")
cols = ["id", "scope", "item", "group", "quantity", "published", "rebuilt", "gap", "tolerance", "status", "alt_status"]
bad["quantity"] = bad["quantity"].str.slice(0, 44)
bad["item"] = bad["item"].astype(str).str.slice(0, 30)
print(bad.sort_values(["status", "abs_rel"], ascending=[False, False])[cols].round(4).to_string(index=False))
na = gate[gate["status"] == "not gated"]["reason"].value_counts()
print("\nnot-gated rows by reason:\n" + na.to_string())
