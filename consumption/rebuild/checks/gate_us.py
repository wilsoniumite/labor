# gate_us.py - the US gate: every published US number in post_published_numbers.csv that the rebuilt static
# machinery should reproduce (text, Fig 4, Fig 5, Fig 6 labels/diamonds/segments, the static parts of Fig 7),
# beside the rebuilt value, the gap and a status. Rows the static rebuild cannot or should not reproduce (inputs,
# axis ticks, labels, cited statistics, the Fig 8/9 wealth block, Fig 0 boxes with no country) are listed with
# status 'n/a' and the reason, so every US row is accounted for.
#
# Status: PASS = within the printed rounding (half a unit of the last printed digit; for read-off values the
# precision stated in the row's note; fraction words +/-5 points); CLOSE = within 10% of the published value or
# within $0.05 for dollar values; MISS otherwise. Counts and yes/no claims must match exactly.
# Role: calibration = used to pin a continuous parameter (VAT flags: Fig 4; MPC knee/top: Fig 5 dollar bars;
# low/high knees: Fig 7 band edges); selection = used to choose between discrete alternatives (group mapping and
# food split: the MPC=1 ghosts); check = not used in any choice.
#
# Run from the repo root:  venv/bin/python -I consumption/rebuild/checks/gate_us.py
# Rebuilds the model from bridge.py's calibrated constants (what the LVT step imports), not from run_us.py's
# outputs, and checks that run_us.py's us_demand_shifts.csv agrees with it.

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
DEC = [f"d{i:02d}" for i in range(1, 11)]
G = pd.read_csv(B.TIDY / "post_published_numbers.csv")

# %% the rebuilt quantities
m = B.build_model(2024)
acc = B.vat_accounting(m)
NET = acc["net"]
sched = B.mpc_schedules()
mid, low, high = sched["mid"].values, sched["low"].values, sched["high"].values
sh = B.shifts_from_transfers(m, NET, mpc=mid)
dec_mid = B.decompose(m, B.budget_shock(NET, mid, m["budget"]))
dec_one = B.decompose(m, B.budget_shock(NET, np.ones(10), m["budget"]))
imp = {k: B.impulse(m, NET, sched[k].values) for k in sched}
vshare = B.vatable_share_aggregate(m)
price = {p: 100 * B.TAU * vshare * p for p in (0.8, 0.9, 1.0)}
pay = NET < 0
w = m["w"]


def weighted_mpc(mpc, mask):
    """Share of the net transfer that becomes spending, weighted by |net| x population, over a set of deciles."""
    a = (w * np.abs(NET))[mask]
    return float((pd.Series(mpc, index=DEC)[mask] * a).sum() / a.sum())


rent_adds = dec_mid.loc["Rented dwellings"].clip(lower=0)
rent_k = int(np.argmax(np.cumsum(rent_adds.values) > 0.5 * rent_adds.sum()) + 1)   # deciles needed for the bulk
renter = m["vals"].loc["Consumer unit characteristics: > Percent distribution: > Housing tenure: > Renter", DEC] \
    if "Consumer unit characteristics: > Percent distribution: > Housing tenure: > Renter" in m["vals"].index else None
if renter is None:
    rp = [p for p in m["vals"].index if p.endswith("> Renter")]
    renter = m["vals"].loc[rp[0], DEC]

# consistency with run_us.py's written output
ds_file = pd.read_csv(OUT / "us_demand_shifts.csv", index_col=0)
assert np.allclose(ds_file.loc[m["chart"], "dUSD_mid"].values, sh.loc[m["chart"], "dUSD_mpc"].values, atol=1e-5)   # file keeps 5 decimals


# %% tolerance helpers
def num_tokens(s):
    s = str(s).replace("−", "-").replace(",", "")
    return re.findall(r"[-+]?\d+(?:\.\d+)?", s)


def printed_tol(row):
    """Half a unit of the last printed digit of the number matching the row's value; None if no digits."""
    v = abs(float(row["value"]))
    best = None
    for t in num_tokens(row["printed"]):
        x = abs(float(t))
        for scale in (1, 100, 0.01):              # percent shares sometimes printed as fractions or the reverse
            if abs(x * scale - v) < 1e-9:
                dec = len(t.split(".")[1]) if "." in t else 0
                best = 0.5 * 10 ** (-dec) * scale
                break
        if best is not None:
            break
    return best


def readoff_tol(row):
    mt = re.search(r"±\s*([0-9.]+)", str(row["note"]))
    return float(mt.group(1)) if mt else None


def tolerance(row):
    if str(row["confidence"]) == "high" and isinstance(row["printed"], str) and row["printed"].strip():
        t = printed_tol(row)
        if t is not None:
            return t, "printed rounding"
        return 5.0 if row["unit"] == "%" else 0.0, "fraction or count word"
    t = readoff_tol(row)
    if t is not None:
        return t, "read-off precision from note"
    return 5.0 if row["unit"] == "USD" else 0.01, "read-off (default)"


# %% map every US row to a rebuilt value (or a reason it is not gated)
F4, F5, F6, F7 = ("fig4_net_transfer_us2024-1.png", "fig5_demand_shifts_us2024_mpc.png",
                  "fig6_composition_us2024_mpc-1.png", "fig7_ramp_inflation_us.png")
DEC_OF = {f"US D{i}": f"d{i:02d}" for i in range(1, 11)}
TEXT_CAT = {"P279": "Rented dwellings", "P280": "Cars and trucks, new", "P281": "Cars and trucks, new",
            "P282": "Cars and trucks, used", "P283": "Cars and trucks, used", "P284": "Health insurance",
            "P285": "Vehicle insurance", "P286": "Fees and admissions", "P287": "Other lodging"}


def rebuilt(row):
    """(value, role, scope, note, alt_value, alt_note) or (None, reason)."""
    i, src, q, it, grp = row["id"], row["source"], str(row["quantity"]), str(row["item"]), str(row["group"])
    if "axis tick" in q:
        return None, "axis tick (scale only)"
    if src == F4:
        if i == "P290":
            return float(acc["dividend"].iloc[0]), "calibration", "Fig 4", "dividend = tau x mean VAT-able consumption", None, ""
        if q == "net transfer per adult share per month":
            return float(NET[DEC_OF[grp]]), "calibration", "Fig 4", "", None, ""
        if q == "net transfer as % of budget":
            return float(acc["net_pct_budget"][DEC_OF[grp]]), "calibration", "Fig 4", "", None, ""
        if q.startswith("VAT-able consumption per adult share per month (x-position)"):
            return float(acc["vatable"][DEC_OF[grp]]), "calibration", "Fig 4", "point position", None, ""
        if q.startswith("mean VAT-able consumption"):
            return float(acc["Cbar_v"].iloc[0]), "calibration", "Fig 4", "dashed line", None, ""
        return None, "input or label (survey year, payment weights, group definition)"
    if src == F5:
        if i == "P436":
            return (imp["mid"]["bars_chart_pct_consumption"], "check", "Fig 5", "charted bars / total consumption",
                    imp["mid"]["bars_chart_pct_charted"], "charted bars / charted budget (the caption's denominator)")
        if q.startswith("change in spending per adult share per month"):
            return float(sh.loc[it, "dUSD_mpc"]), "calibration", "Fig 5", "bar label (MPC mid)", None, ""
        if q.startswith("percent change in category spending"):
            return float(sh.loc[it, "dPct_mpc"]), "check", "Fig 5", "percent label: tests Cbar_g (category definitions, payment units)", None, ""
        if q == "MPC=1 benchmark (ghost) value":
            return float(sh.loc[it, "dUSD_mpc1"]), "selection", "Fig 5", "outline (MPC=1)", None, ""
        return None, "input (MPC of the benchmark)"
    if src == F6:
        if q.startswith("decile contribution"):
            return float(dec_mid.loc[it, DEC_OF[grp]]), "check", "Fig 6 segment", "decile contribution, MPC mid", None, ""
        if q.startswith("change in spending per adult share per month"):
            return float(sh.loc[it, "dUSD_mpc"]), "check", "Fig 6 diamond", "solid diamond / net label (MPC mid)", None, ""
        if q == "MPC=1 benchmark (ghost) value":
            return float(sh.loc[it, "dUSD_mpc1"]), "check", "Fig 6 diamond", "hollow diamond (MPC=1)", None, ""
        return None, "input or label"
    if src == F7:
        if i in ("P516", "P517", "P518"):
            p = {"P516": 0.9, "P517": 1.0, "P518": 0.8}[i]
            return price[p], "check", "Fig 7", f"tau x {p:.0%} pass-through x aggregate VAT-able share", None, ""
        if i in ("P513", "P514"):
            p = {"P513": 0.8, "P514": 1.0}[i]
            return price[p] / 3, "check", "Fig 7", f"level shift at {p:.0%} pass-through / 3 ramp years", None, ""
        if i == "P537":
            return imp["mid"]["flow_pct_consumption"], "check", "Fig 7", "flow impulse, mid schedule", None, ""
        if i == "P538":
            return imp["low"]["flow_pct_consumption"], "calibration", "Fig 7", "flow impulse, low schedule (knee pinned here)", None, ""
        if i == "P539":
            return imp["high"]["flow_pct_consumption"], "calibration", "Fig 7", "flow impulse, high schedule (knee pinned here)", None, ""
        if i == "P534":
            return (100 * weighted_mpc(mid, ~pay), "check", "Fig 7", "net-receipt-weighted MPC of the gaining deciles (mid)",
                    None, "")
        if i in ("P535", "P536"):
            s = low if i == "P535" else high
            alt = 100 * (low[pay.values].min() if i == "P535" else high[pay.values].max())
            return (100 * weighted_mpc(s, pay), "check", "Fig 7",
                    f"payment-weighted MPC of the paying deciles, {'low' if i == 'P535' else 'high'} schedule", alt,
                    "alternative reading: lowest / highest payer MPC across the low and high schedules")
        return None, "input (ramp length, rate, pass-through range) or structural zero"
    if src == "text":
        if i in TEXT_CAT:
            c = TEXT_CAT[i]
            if "ghost" in q:
                return float(sh.loc[c, "dUSD_mpc1"]), "selection", "text", f"= Fig 5 '{c}' ghost", None, ""
            return float(sh.loc[c, "dUSD_mpc"]), "calibration", "text", f"= Fig 5 '{c}' bar", None, ""
        if i in ("P273",):
            return float(acc["dividend"].iloc[0]), "calibration", "text", "", None, ""
        if i == "P274":
            return float((NET > 0).sum()), "calibration", "text", "count of deciles with net > 0", None, ""
        if i == "P275":
            return float(np.where(NET.values > 0)[0].max() + 1), "calibration", "text", "last gaining decile", None, ""
        if i == "P276":
            return float(np.where(NET.values < 0)[0].min() + 1), "calibration", "text", "first paying decile", None, ""
        if i == "P277":
            return float(NET["d10"]), "calibration", "text", "", None, ""
        if i == "P278":
            return float(acc["net_pct_budget"]["d10"]), "calibration", "text", "", None, ""
        if i == "P324":
            return float(acc["vatable_pct_budget"].min()), "calibration", "text", "lowest decile VAT-able share", None, ""
        if i == "P325":
            return float(acc["vatable_pct_budget"].max()), "calibration", "text", "highest decile VAT-able share", None, ""
        if i == "P438":
            return (imp["mid"]["bars_chart_pct_charted"], "check", "text", "charted bars / charted budget",
                    imp["mid"]["bars_chart_pct_consumption"], "charted bars / total consumption (the footer's denominator)")
        if i in ("P439", "P440"):
            return float(renter[{"P439": "d01", "P440": "d10"}[i]]), "check", "text", "CE Table 1110 renter share (data)", None, ""
        if i == "P441":
            return float(rent_k), "check", "text", "deciles D1..Dk needed for > half of gross rent additions (MPC mid)", None, ""
        if i == "P496":
            return 100 * vshare, "check", "text", "aggregate VAT-able share of the budget", None, ""
        if i in ("P497", "P562"):
            return price[0.8], "check", "text", "level shift at 80% pass-through", None, ""
        if i in ("P498", "P563", "P506"):
            return price[1.0], "check", "text", "level shift at 100% pass-through", None, ""
        if i in ("P500", "P564"):
            return price[0.8] / 3, "check", "text", "per ramp year, 80% pass-through", None, ""
        if i in ("P501", "P565"):
            return price[1.0] / 3, "check", "text", "per ramp year, 100% pass-through", None, ""
        if i == "P566":
            return imp["high"]["flow_pct_consumption"], "calibration", "text", "flow impulse, high schedule", None, ""
        if i == "P567":
            return imp["low"]["flow_pct_consumption"], "calibration", "text", "flow impulse, low schedule", None, ""
        if i == "P662":
            return (imp["mid"]["flow_pct_consumption"], "check", "text",
                    "static flow impulse, mid; the text's figure is Fig 8's flow-only path at year 3 (wealth block)", None, "")
        if i == "P916":
            return float(mid[0]), "check", "text", "mid schedule, D1", None, ""
        if i == "P917":
            return float(low[-1]), "calibration", "text", "low schedule top (input to the knee family)", None, ""
        if i == "P918":
            return float(high[-1]), "calibration", "text", "high schedule top (input to the knee family)", None, ""
        return None, "not a static-rebuild quantity (input, cited statistic, time reference, Fig 8/9 wealth block)"
    if src in ("fig8_wealth_block_paths_us.png", "fig9_demand_shifts_us_year2.png"):
        return None, "wealth block / year-two dynamics (Figs 8-9): outside this static rebuild"
    return None, "not a US row of the static rebuild"


def is_us(row):
    g = str(row["group"])
    if row["source"] in (F4, F5, F6, F7, "fig8_wealth_block_paths_us.png", "fig9_demand_shifts_us_year2.png"):
        return True
    if row["source"] == "text" and (g.startswith("US") or row["id"] in ("P916", "P917", "P918")):
        return True
    return False


rows = []
for _, r in G[G.apply(is_us, axis=1)].iterrows():
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
    exact = r["unit"] in ("count", "decile")
    if exact:
        status = "PASS" if abs(gap) < 1e-9 else "MISS"
    elif abs(gap) <= tol + 1e-9:
        status = "PASS"
    elif abs(gap) <= 0.10 * abs(float(r["value"])) + 1e-12 or (r["unit"] == "USD" and abs(gap) <= 0.05 + 1e-12):
        status = "CLOSE"
    else:
        status = "MISS"
    alt_status = ""
    if alt is not None:
        ag = alt - float(r["value"])
        alt_status = "PASS" if abs(ag) <= tol + 1e-9 else ("CLOSE" if abs(ag) <= 0.10 * abs(float(r["value"])) else "MISS")
    rows.append(dict(base, rebuilt=val, gap=gap, rel_gap=gap / float(r["value"]) if float(r["value"]) else np.nan,
                     tolerance=tol, tolerance_kind="exact" if exact else tol_kind, status=status, role=role, scope=scope,
                     note=note, alt_rebuilt=alt, alt_status=alt_status, alt_note=altnote))
gate = pd.DataFrame(rows)
gate.to_csv(OUT / "gate_us.csv", index=False, float_format="%.5f")

# %% summary
gated = gate[gate["status"] != "not gated"]
order = ["Fig 4", "Fig 5", "Fig 6 diamond", "Fig 6 segment", "Fig 7", "text"]
tab = gated.pivot_table(index="scope", columns="status", values="id", aggfunc="count", fill_value=0).reindex(order)
tab = tab.reindex(columns=["PASS", "CLOSE", "MISS"], fill_value=0)
tab["total"] = tab.sum(axis=1)
tab.loc["all gated"] = tab.sum()
role_tab = gated.pivot_table(index="role", columns="status", values="id", aggfunc="count", fill_value=0)
role_tab = role_tab.reindex(columns=["PASS", "CLOSE", "MISS"], fill_value=0)
print(f"US gate: {len(gate)} US rows in the gate list; {len(gated)} gated, {int((gate["status"] == "not gated").sum())} not gated")
print(tab.to_string())
print("\nby role (calibration = used to pin a parameter; selection = used to choose a discrete variant):")
print(role_tab.to_string())
core = gated[gated["scope"].isin(["Fig 4", "Fig 5", "Fig 6 diamond", "text"])]
cnt = core["status"].value_counts().reindex(["PASS", "CLOSE", "MISS"], fill_value=0)
print(f"\nheadline scope (text, Fig 4, Fig 5, Fig 6 diamonds): {cnt['PASS']} PASS, {cnt['CLOSE']} CLOSE, {cnt['MISS']} MISS "
      f"of {len(core)}")
bad = gated[gated["status"] != "PASS"].copy()
bad["abs_rel"] = bad["rel_gap"].abs()
print("\nnot PASS (sorted by status, then |relative gap|):")
cols = ["id", "scope", "item", "group", "quantity", "published", "rebuilt", "gap", "tolerance", "status", "alt_status"]
bad["quantity"] = bad["quantity"].str.slice(0, 48)
bad["item"] = bad["item"].astype(str).str.slice(0, 30)
print(bad.sort_values(["status", "abs_rel"], ascending=[False, False])[cols].round(4).to_string(index=False))
na = gate[gate["status"] == "not gated"]["reason"].value_counts()
print("\nnot-gated rows by reason:\n" + na.to_string())
