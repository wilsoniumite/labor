# case.py — her case: what we think is happening, as runs of the crash model. Her call (2026-09-25): pin down a
# "this is what we think is happening" case across the model, the watcher and the website. Her leanings: deficit worries,
# perhaps sovereign default worries; recession and consumption-demand worries; a stock bust bigger and faster than the
# dot-com one; care capping out as an absorber; reckless tariffs from the US and something more sensible but still austere
# from Europe; the process under way for two to four years, accelerating as AI companies behave differently. Where she left
# it open, the settings are Claude's best guesses, each stated, and each a decision in STATE.md's veto window (23-27).
#
# The case, in the model's terms (today's measured regions; one dating, gc.quarter_label: index 0 is the state measured
# on data to September 2026, 2026Q3, and index 1, the first simulated quarter, 2026Q4; six years, to 2032Q3 at index 24):
#   the bust        bigger and faster than the dot-com one: ai_shock at 1.5x (US stocks -60%, AI investment -90%, 1.5x the
#                   losses on AI lending) over two quarters (dot-com: the S&P 500 -49% over some 30 months);
#   the pace        displacement starts at the upper bound seen so far (pace.py: 0.15 of the paper's pace) and rises on a
#                   logistic to the paper's pace, half the rise by 2028Q2 (index 7; AI companies consolidating and
#                   deploying: faster than the macro block's clock, whose fits put its midpoint near 2031);
#   adoption        a range: firms automate the usual share of the jobs they cut in the downturn (the low end) or twice
#                   it (the high end, the case as quoted); the model's largest single lever, so the case is a band;
#   robotics        two years out (her call, 2026-09-24);
#   care            caps out: every region's own ceiling one year of trend above today's share (a financing limit reached
#                   well before Norway's);
#   the US          tariffs of 25 points from the second simulated quarter (2027Q1), read as the model's symmetric tariff
#                   (US exports face retaliation of that size); today's fiscal response, rescues and benefits; deficit
#                   worry as a premium on borrowing, rising a point over the first year and held (another move the size
#                   of the ten-year term premium's rise since 2019) and passed to private borrowers. For the US the worry
#                   is fiscal dominance (inflation, a central bank leaning on), not default; the model has no default,
#                   and a looser US anchor is run as a sensitivity;
#   Europe, Sweden  no tariffs of their own; the US's reach them through their exports to it (25 points times that share);
#                   spending cuts as unemployment rises; rescues and benefits intact; the euro area carries half a point
#                   of sovereign premium (France). The euro area is one region: Germany spending while the periphery cuts
#                   cannot be split, and is run as a sensitivity (the euro area neither stimulating nor cutting);
#   China           the US tariff through its exports to the US; today's response (stimulus).
# What the model cannot do: it has no revenue side, so deficits are priced (the premium), not computed, and it has no
# default. Watched, not modelled (the watcher's wider rules): energy (an oil surge ties central banks' hands), housing and
# mortgage costs, private credit beyond the bust's lending losses, Japan (repatriation, the carry trade), Korea and Taiwan
# (where the hardware collapse lands first). The attribution runs take one piece of the case back to the model's central
# setting at a time; the sensitivities change one setting the case does not carry.
#
# Run from paths/:  ../venv/Scripts/python.exe code/case.py
# Out: results/case.json, figures/fig_case.png

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import global_crash as gc  # noqa: E402

N = 25                # 2026Q3 (index 0, the start) .. 2032Q3 (index 24): six years of simulated quarters
START = gc.START
END_2028 = 9          # the quarter index of 2028Q4 (gc.quarter_label(9))
Q2032Q2 = N - 2       # 2032Q2, quoted where a run is at the model's cap by 2032Q3
CAP = 50.0            # the model's ceiling on non-employment (u + out), %
US_TARIFF = 25.0
PIECES = ("bust", "pace", "adoption", "premium", "tariffs", "austerity", "care")


def stored():
    j = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
    return gc.Common(**j["common"]), {r: gc.Region(**j["regions"][r]) for r in gc.R}


def logistic_pace(paper: float, seen: float, mid_q: float, width_q: float, n: int = N) -> np.ndarray:
    """From `seen` x the paper's pace now to the paper's pace, half the rise by quarter mid_q."""
    k = np.arange(n)
    w = 1 / (1 + np.exp(-(k - mid_q) / (width_q / 4)))
    w0 = 1 / (1 + np.exp(mid_q / (width_q / 4)))
    return paper * (seen + (1 - seen) * (w - w0) / (1 - w0))


def ramp_to(total: float, quarters: int, n: int = N) -> np.ndarray:
    return np.array([total * min(k / quarters, 1.0) for k in range(n)])


def settings(regs, pace_seen: float) -> dict:
    """The case's settings, piece by piece, so that each can be taken back to the model's central setting."""
    care_cap = {r: round(regs[r].care_share + regs[r].care_trend, 2) for r in gc.R}
    tariff_hit = {"US": US_TARIFF, **{r: round(US_TARIFF * regs[r].trade.get("US", 0.0), 2) for r in ("EA", "SE", "CN")}}
    return {
        "bust": {"scale": 1.5, "speed": 2.0},
        "pace": {"seen": pace_seen, "mid_quarter": 7, "width_quarters": 8},
        "adoption_multiple": {"low": 1.0, "high": 2.0},
        "robot_lag_years": 2.0,
        "care_cap": care_cap,
        "tariff": tariff_hit, "tariff_quarter": 2,
        "fiscal": {"US": "stimulus", "EA": "austerity", "SE": "austerity", "CN": "stimulus"},
        "premium": {"US": 1.0, "EA": 0.5, "SE": 0.0, "CN": 0.0}, "premium_quarters": 4,
    }


# the sensitivities: one setting the case does not carry, on the case at its high end
SENSITIVITIES = {
    "fiscal dominance: the US anchor loosens to the eroding rules' 0.6": {"rules": {"US": {"anchor": 0.6}}},
    "fiscal dominance: the US anchor loosens to 0.6 and the Fed tolerates 3% inflation":
        {"rules": {"US": {"anchor": 0.6, "pi_star": 3.0}}},
    "Germany's spending offsets the periphery's cuts: the euro area neither stimulates nor cuts": {"rules": {"EA": {"fiscal": "none"}}},
    "the euro area stimulates": {"rules": {"EA": {"fiscal": "stimulus"}}},
    "the US exit share at decision 21's proposal (0.36)": {"regions": {"US": {"exit_share": 0.36}}},
    "fiscal triggers watch non-employment": {"rules": {r: {"trigger_on": "non-employment"} for r in gc.R}},
}


def build(cm, regs, st: dict, drop: str | None = None, adoption: str = "high", sens: dict | None = None, n: int = N):
    """The case, or the case with one piece (`drop`) taken back to the model's central setting, or with one sensitivity
    (n quarters: the case's N; check K12 runs it at 24 too)."""
    central = {"bust": {"scale": 1.0, "speed": 1.0}, "adoption_multiple": 1.0}
    b = central["bust"] if drop == "bust" else st["bust"]
    shock = gc.ai_shock(n, b["scale"], b["speed"])
    pace = st["pace"]
    if drop != "pace":
        shock.drift = {r: logistic_pace(regs[r].drift, pace["seen"], pace["mid_quarter"], pace["width_quarters"], n) for r in gc.R}
    if drop != "premium":
        shock.spread = {r: ramp_to(v, st["premium_quarters"], n) for r, v in st["premium"].items() if v}
    adopt = central["adoption_multiple"] if drop == "adoption" else st["adoption_multiple"][adoption]
    sens = sens or {}
    rg = {r: replace(g, eta=g.eta * adopt, **sens.get("regions", {}).get(r, {})) for r, g in regs.items()}
    rules = {}
    for r in gc.R:
        rl = gc.MODERN
        if drop != "tariffs":
            rl = replace(rl, tariff=st["tariff"][r], tariff_q=st["tariff_quarter"])
        if drop != "austerity":
            rl = replace(rl, fiscal=st["fiscal"][r])
        if drop != "care":
            rl = replace(rl, care_cap=st["care_cap"][r])
        rules[r] = replace(rl, **sens.get("rules", {}).get(r, {}))
    waves = gc.Waves(split=True, robot_lag=st["robot_lag_years"], absorb=True)
    return rg, gc.simulate(rg, rules, shock, cm, n, waves=waves)


def reference(cm, regs, n: int = N):
    """The model's central run: today's policies, a dot-com-sized bust, the paper's pace, robotics in two years."""
    return regs, gc.simulate(regs, {r: gc.MODERN for r in gc.R}, gc.ai_shock(n), cm, n,
                             waves=gc.Waves(split=True, robot_lag=2.0, absorb=True))


def four(rg, o) -> np.ndarray:
    size = {r: rg[r].size for r in gc.R}
    return np.array([sum(size[r] * o[r]["y"][k] for r in gc.R) / sum(size.values()) for k in range(len(o["US"]["y"]))])


def read(rg, o) -> dict:
    f = four(rg, o)
    us = o["US"]
    oow = us["u"] + us["out"]
    k = int(np.argmax(oow))
    res = {"four_output_worst": round(float(f.min()), 1), "four_output_worst_year": round(float(f.argmin()) / 4, 2),
           "four_output_end_2028": round(float(f[END_2028]), 1),
           "us_out_of_work_peak": round(float(oow.max()), 1), "us_out_of_work_peak_year": round(k / 4, 2),
           "us_unemployment_at_peak": round(float(us["u"][k]), 1), "us_left_at_peak": round(float(us["out"][k]), 1),
           "us_out_of_work_end_2028": round(float(oow[END_2028]), 1),
           "us_output_end_2028": round(float(us["y"][END_2028]), 1),
           "us_out_of_work_2032Q2": round(float(oow[Q2032Q2]), 1),
           "us_at_the_models_cap_from": next((gc.quarter_label(j) for j in range(len(oow)) if oow[j] >= CAP - 1e-9), None),
           "still_rising_at_end": bool(oow[-1] > oow[-2]),
           "regions": {}}
    for r in gc.R:
        x = o[r]
        res["regions"][r] = {"output_worst": round(float(x["y"].min()), 1),
                             "out_of_work_peak": round(float((x["u"] + x["out"]).max()), 1),
                             "out_of_work_end_2028": round(float((x["u"] + x["out"])[END_2028]), 1),
                             "unemployment_peak": round(float(x["u"].max()), 1),
                             "bank_capital_lost_max_pct": round(float(x["stress"].max()) * 100),
                             "inflation_min": round(float(x["pi"].min()), 1), "inflation_max": round(float(x["pi"].max()), 1),
                             "policy_rate_min": round(float(x["i"].min()), 2),
                             "credit_spread_max": round(float(x["s"].max()), 2),
                             "care_end": round(float(x["care"][-1]), 1)}
    return res


def paths(rg, o) -> dict:
    out = {"four_output": [round(float(v), 2) for v in four(rg, o)]}
    for r in gc.R:
        x = o[r]
        out[r] = {k: [round(float(v), 2) for v in arr] for k, arr in
                  (("out_of_work", x["u"] + x["out"]), ("unemployment", x["u"]), ("left_workforce", x["out"]),
                   ("output", x["y"]), ("inflation", x["pi"]), ("rate", x["i"]), ("spread", x["s"]),
                   ("capital_lost", x["stress"] * 100), ("care", x["care"]))}
    return out


def verdict(r: dict) -> str:
    if r["four_output_worst"] <= -20:
        return "a depression"
    if r["us_out_of_work_peak"] >= 15:
        return "a labour depression, output held" if r["four_output_worst"] > -10 else "a labour depression"
    if r["four_output_worst"] <= -4:
        return "a 2008-scale recession"
    return "a recession" if r["four_output_worst"] <= -2 else "a slowdown"


def short(x: dict) -> dict:
    return {"us_out_of_work_end_2028": x["us_out_of_work_end_2028"], "us_out_of_work_peak": x["us_out_of_work_peak"],
            "us_out_of_work_2032Q2": x["us_out_of_work_2032Q2"], "us_at_the_models_cap_from": x["us_at_the_models_cap_from"],
            "four_output_worst": x["four_output_worst"], "ea_out_of_work_peak": x["regions"]["EA"]["out_of_work_peak"],
            "se_out_of_work_peak": x["regions"]["SE"]["out_of_work_peak"],
            "us_inflation_min": x["regions"]["US"]["inflation_min"], "us_inflation_max": x["regions"]["US"]["inflation_max"]}


def run_all(cm, regs, st) -> dict:
    ends = {}
    for end in ("low", "high"):
        x = read(*build(cm, regs, st, adoption=end))
        x["verdict"] = verdict(x)
        ends[end] = x
    hi = ends["high"]
    ref = read(*reference(cm, regs))
    ref["verdict"] = verdict(ref)
    drops = {}
    for d in PIECES:
        x = short(read(*build(cm, regs, st, d)))
        x.update({"adds_to_us_out_of_work": round(hi["us_out_of_work_peak"] - x["us_out_of_work_peak"], 1),
                  "adds_to_us_out_of_work_end_2028": round(hi["us_out_of_work_end_2028"] - x["us_out_of_work_end_2028"], 1),
                  "adds_to_us_out_of_work_2032Q2": round(hi["us_out_of_work_2032Q2"] - x["us_out_of_work_2032Q2"], 1),
                  "adds_to_four_output": round(hi["four_output_worst"] - x["four_output_worst"], 1),
                  "adds_to_ea_out_of_work": round(hi["regions"]["EA"]["out_of_work_peak"] - x["ea_out_of_work_peak"], 1),
                  "adds_to_se_out_of_work": round(hi["regions"]["SE"]["out_of_work_peak"] - x["se_out_of_work_peak"], 1)})
        drops[d] = x
    sens = {}
    for name, s in SENSITIVITIES.items():
        x = short(read(*build(cm, regs, st, sens=s)))
        x["change_in_us_out_of_work"] = round(x["us_out_of_work_peak"] - hi["us_out_of_work_peak"], 1)
        x["change_in_us_out_of_work_2032Q2"] = round(x["us_out_of_work_2032Q2"] - hi["us_out_of_work_2032Q2"], 1)
        x["change_in_four_output"] = round(x["four_output_worst"] - hi["four_output_worst"], 1)
        x["change_in_ea_out_of_work"] = round(x["ea_out_of_work_peak"] - hi["regions"]["EA"]["out_of_work_peak"], 1)
        sens[name] = x
    return {"case": ends, "reference_central_run": ref,
            "piece_by_piece": {"note": "each row takes one piece of the case (at its high end) back to the model's central "
                                       "setting; 'adds' is the case minus that run (what the piece adds): at 2028Q4, at "
                                       "2032Q2, and at the peak (2032Q3 while still rising; where the run is at the model's "
                                       "50% cap there, its peak is a floor and 2032Q2 is the reading)", **drops},
            "sensitivities": {"note": "each changes one setting the case does not carry, on the case at its high end; at the "
                                      "peak and at 2032Q2 (the reading where the run is at the model's 50% cap by 2032Q3)", **sens}}


def main():
    cm, regs = stored()
    pace = json.load(open(os.path.join(ROOT, "results", "pace.json"), encoding="utf-8"))
    seen = pace["paces"]["multiples_of_the_papers"]["trend + 2 s.e."]
    st = settings(regs, seen)
    res = {"start": START, "quarters": N,
           "dating": f"index 0 = {gc.quarter_label(0)}, the state measured on data to September 2026; index 1 = "
                     f"{gc.quarter_label(1)}, the first simulated quarter; index {END_2028} = {gc.quarter_label(END_2028)}; "
                     f"index {N - 1} = {gc.quarter_label(N - 1)} (decision 43)",
           "settings": st, **run_all(cm, regs, st),
           "paths": {end: paths(*build(cm, regs, st, adoption=end)) for end in ("low", "high")}}
    res["paths"]["reference"] = paths(*reference(cm, regs))
    json.dump(res, open(os.path.join(ROOT, "results", "case.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "paths"}, indent=1))
    figure(res)


def figure(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    t = gc.quarter_mid(np.arange(N))             # each quarter at its middle
    lo, hi, ref = res["paths"]["low"], res["paths"]["high"], res["paths"]["reference"]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.06, 1, 0.94))
    cols = {"US": "C0", "EA": "C1", "SE": "C2", "CN": "C3"}
    for a, key, title in ((ax[0], "out_of_work", "1. Out of work (unemployed + left the workforce), %"),
                          (ax[1], "output", "2. Output against capacity, %")):
        for r in gc.R:
            a.fill_between(t, lo[r][key], hi[r][key], color=cols[r], alpha=0.25, lw=0)
            a.plot(t, hi[r][key], color=cols[r], label=r)
            a.plot(t, lo[r][key], color=cols[r], lw=0.8)
        a.plot(t, ref["US"][key], color="C0", ls=":", label="US, the model's central run")
        a.axvline(t[END_2028], color="grey", lw=0.6, ls="--")
        a.set_title(title); a.legend(fontsize=8)
    ax[1].axhline(0, color="grey", lw=0.8)
    a = ax[2]
    for r in gc.R:
        a.plot(t, hi[r]["spread"], color=cols[r], label=r)
    a.set_title("3. Credit spread over the safe rate, points (high end)"); a.legend(fontsize=8)
    fig.text(0.01, 0.01, "Her case: a bust 1.5x the dot-com size over two quarters; displacement rising from the pace seen so far to "
             "the paper's by 2029; care capping out; US tariffs 25 points; spending cuts in Europe and Sweden; a premium on "
             "borrowing (US +1 point, euro area +0.5).\nBands: firms automate the usual share of the jobs they cut in the "
             "downturn (lower line) or twice it (upper line). Index 0 = 2026Q3, the start measured to September 2026; the "
             "first simulated quarter is 2026Q4; dashed line: 2028Q4.", fontsize=8)
    p = os.path.join(ROOT, "figures", "fig_case.png"); fig.savefig(p, dpi=150); print(p)


if __name__ == "__main__":
    main()
