# outlook.py — the case: what we think is happening and where it leads, as one run of the crash engine and the runs
# around it. Written 2026-11-13 from a clean slate (STATE.md): the engine is paths/code/global_crash.py as fitted on nine
# past downturns by month, unchanged; everything the case adds is an input to it, each measured or stated:
#   the start      the five economies as measured on the dated vintage (paths/cache/start, to September 2026: index 0);
#   inflation      where core inflation is above target at the start it stays there for a time: the excess over what
#                  the engine's expectations give fades at the pace each region's own excess fell from its peak to its
#                  low after it (Shock.push). Where it is below target the engine's expectations bring it back at once,
#                  as before: the engine reads any shortfall of prices from their targeted path as a heavier real debt,
#                  which a short undershoot is not;
#   the pace       AI's net displacement of jobs starts at the most the US jobs data allow (paths/results/pace.json:
#                  the trend in prime-age non-employment since the 2024 employment peak plus two standard errors, all
#                  of it attributed to AI) and doubles every two years, up to a point of the workforce a year (stated);
#                  the other economies at the engine's ratios to the US (stated);
#   who leaves     the US share of the displaced that leaves the workforce: the middle of the three bases it has been
#                  measured from (pace.json), in place of the highest;
#   the bust       half the dot-com bust (stated), on that bust's measured path, dated from the day of this year's high
#                  in share prices (6 October 2026);
#   robots         not within the run (stated: they can do most physical tasks and are cost-competitive on very few);
#   policy         today's rules, each economy's discretionary lever starting the month after its own unemployment has
#                  risen by the rules' trigger in that run (global_crash.trigger_dates): governments respond to what
#                  happens in the run, not on dates fixed in another.
# The runs around the case change one setting at a time; the page's settings (the watcher's web/model_export.py) are
# the same ones.
#
# Run from outlook/:  python code/outlook.py
# Out: results/outlook.json

from __future__ import annotations

import datetime as dt
import json
import math
import os
import statistics
import sys
from dataclasses import replace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PATHS = os.path.join(os.path.dirname(ROOT), "paths")
sys.path.insert(0, os.path.join(PATHS, "code"))
import global_crash as gc  # noqa: E402
import vintage  # noqa: E402

SET = "2026-11-13"                     # the day the case was set
DT = gc.DT                             # the engine's step: a month
N = gc.months(24)                      # 70 steps: index 0 the start (the end of September 2026) .. 69 (the end of June 2032)
LATEST = 13                            # the last quarter a bust may peak in (2029Q4), as an index
PEAK, PEAK_2000 = "2026-10-06", "2000-03-10"     # this year's high in the Nasdaq and the S&P 500; the Nasdaq's in 2000
DAYS_Q = 365.25 / 4
TARGET = 2.0                           # the inflation target the excess is measured against, % (every region's pi_star)
CEILING = 1.0                          # the most the pace reaches, points of the US workforce a year (stated)
# the pace's options: (key, years in which it doubles; None: it does not grow)
PACES = (("none", None), ("seen", None), ("central", 2.0), ("fast", 1.0))
# core inflation by region on the vintage (the engine's pi is core): the series its excess's fading is measured on
CORE = {"US": "PCEPILFE", "EA": "00XEFDEZ19M086NEST", "FR": "FR_HICP_CORE", "SE": "00XEFDSEM086NEST"}
POLICIES = {"today": "modern rules", "guarantee": "rules expand under pressure", "care": "rules expand into care",
            "care-tax": "care financed by labour taxes", "care-levy": "care financed by a levy on AI income",
            "erode": "rules erode under pressure", "1930s": "the 1930s' rules"}
ADOPTIONS = {"1": 1.0, "2": 2.0, "3": 3.0}
ROBOTS = {"0": 0.0, "1": 1.0, "2": 2.0, "3": 3.0, "never": 99.0}
CENTRAL = {"policy": "today", "size": 0.5, "speed": 1.0, "shape": "2000", "start": PEAK, "pace": "central",
           "adoption": "1", "robots": "never"}
# the runs around the case, one change each (the last two change two): (key, what changes)
AROUND = (
    ("funding holds", {"size": 0.0}),
    ("a dot-com-sized bust", {"size": 1.0}),
    ("a severe bust", {"size": 1.5}),
    ("no AI job losses", {"pace": "none"}),
    ("the pace stays as seen", {"pace": "seen"}),
    ("the pace doubles every year", {"pace": "fast"}),
    ("firms automate twice the jobs they cut", {"adoption": "2"}),
    ("robots from late 2029", {"robots": "3"}),
    ("an income guarantee", {"policy": "guarantee"}),
    ("more care jobs", {"policy": "care"}),
    ("spending cuts and tariffs", {"policy": "erode"}),
    ("the better case", {"size": 0.0, "pace": "seen"}),
    ("the worse case", {"size": 1.0, "policy": "erode"}),
)


def load(name: str) -> dict:
    return json.load(open(os.path.join(PATHS, "results", name), encoding="utf-8"))


# ------------------------------------------------------------------ the inputs, measured
def stored() -> tuple:
    """The engine as fitted and its start as measured (paths/results/global_crash.json): the common, the regions."""
    j = load("global_crash.json")
    return gc.Common(**j["common"]), {r: gc.Region(**j["regions"][r]) for r in gc.R}


def seen() -> dict:
    """What the US jobs data allow (paths/results/pace.json, measured from the employment peak of September 2024): the
    pace on the trend, its upper bound (two standard errors above) and the endpoints' reading, in points of the
    workforce a year, all of the change attributed to AI; and the share of the displaced that left the workforce, on
    each of the three bases it is measured from."""
    p = load("pace.json")
    m, unit = p["paces"]["multiples_of_the_papers"], p["paces"]["us_drift_papers_pts_a_year"]
    bases = {k: v["exit_share"] for k, v in p["observed"]["endpoints_from"].items()}
    return {"window": p["observed"]["window"], "trend": m["trend"] * unit, "bound": m["trend + 2 s.e."] * unit,
            "endpoints": m["endpoint"] * unit, "exit_share_by_base": bases,
            "exit_share": statistics.median(bases.values())}


def regions() -> dict:
    """The regions the case runs on: as stored, the US share of the displaced that leaves the workforce at the middle
    of its three measured bases."""
    _, regs = stored()
    return {**regs, "US": replace(regs["US"], exit_share=seen()["exit_share"])}


def us_pace(option: str, n: int) -> np.ndarray:
    """The US pace by step, points of the workforce a year: none; as seen (flat at the bound); or from the bound,
    doubling every so many years, up to the ceiling."""
    years = dict(PACES)[option]
    if option == "none":
        return np.zeros(n)
    start = seen()["bound"]
    if years is None:
        return np.full(n, start)
    return np.minimum(CEILING, start * 2.0 ** (np.arange(n) * DT / years))


def pace_paths(option: str, n: int, regs: dict | None = None) -> dict:
    """Every region's pace by step: the US path at the engine's ratio of the region's stored pace to the US's."""
    regs = regs or regions()
    us = us_pace(option, n)
    return {r: regs[r].drift / regs["US"].drift * us for r in gc.R}


def fading(sid: str) -> dict:
    """How fast a region's core inflation above target has faded: from the highest twelve-month rate the vintage holds
    to the lowest after it, the half-life of the excess over the target (least squares on its logarithm, the months
    the excess is above 0.2)."""
    s = vintage.read(sid).dropna()
    y = ((s / s.shift(12) - 1) * 100).dropna()
    peak = y.idxmax()
    after = y[peak:]
    low = after.idxmin()
    ex = (after[:low] - TARGET)
    ex = ex[ex > 0.2]
    t = np.array([(d - peak).days / 365.25 for d in ex.index])
    slope = float(np.polyfit(t, np.log(ex.values), 1)[0])
    return {"series": sid, "peak": [f"{peak:%Y-%m}", round(float(y[peak]), 2)], "low": [f"{low:%Y-%m}", round(float(y[low]), 2)],
            "half_life_years": math.log(2) / -slope}


def push_paths(regs: dict, n: int, cm=None) -> tuple[dict, dict]:
    """The inflation in the pipeline at the start, by region and step (Shock.push), and how each was measured: core
    inflation at the start above what the engine's expectations give in the first step (the anchor's weight on the
    target, the rest on the past year's inflation), fading at the region's measured half-life; none where core inflation
    is at or below that."""
    cm = cm or stored()[0]
    paths, info = {}, {}
    anchor = gc.MODERN.anchor
    for r, g in regs.items():
        expected = anchor * TARGET + (1 - anchor) * g.pi0
        excess = g.pi0 - expected
        if r not in CORE or excess <= 0:
            info[r] = {"core_inflation_at_the_start": round(g.pi0, 2), "excess": 0.0}
            continue
        f = fading(CORE[r])
        paths[r] = excess * 0.5 ** (np.arange(n) * DT / f["half_life_years"])
        info[r] = {"core_inflation_at_the_start": round(g.pi0, 2), "excess": round(excess, 3),
                   "half_life_years": round(f["half_life_years"], 2), "measured": f}
    return paths, info


# ------------------------------------------------------------------ the bust's dating, by the day
def _day(s: str) -> dt.date:
    return dt.date.fromisoformat(str(s))


def quarter_end(d: dt.date) -> dt.date:
    m = 3 * ((d.month - 1) // 3 + 1)
    return (dt.date(d.year + 1, 1, 1) if m == 12 else dt.date(d.year, m + 1, 1)) - dt.timedelta(days=1)


def to_end(d: dt.date) -> int:
    return (quarter_end(d) - d).days


def quarter_index(d: dt.date) -> int:
    """The engine's index of the quarter `d` falls in: 0 for the start's quarter (2026Q3), 1 for 2026Q4."""
    return d.year * 4 + (d.month - 1) // 3 - (int(gc.START[:4]) * 4 + int(gc.START[-1]) - 1)


def delay_of(day: str, shape: str = "2000") -> float:
    """gc.ai_shock's delay for a bust whose share prices peak on `day`. On the measured path the first quarter ends 21
    days after the peak (10 March 2000 to the end of 2000Q1), so the delay is the peak's quarter (index 1 + delay) less
    how much later in its quarter the peak comes than 10 March 2000 did in its own. The straight-line fall starts with
    the peak's quarter."""
    d = _day(day)
    q = quarter_index(d)
    if shape == "ramp":
        return q - 1
    return q - 1 - (to_end(d) - to_end(_day(PEAK_2000))) / DAYS_Q


def length(delay: float) -> int:
    """A run's steps: N, and as many more as the bust peaks later than the first simulated quarter."""
    return N + max(0, math.ceil(delay * gc.quarter_steps(DT)))


# ------------------------------------------------------------------ a run
def settings_of(pick: dict | None = None) -> dict:
    """A run's settings: the case's, with `pick`'s changes. Without a bust its speed, shape and day do not apply."""
    s = {**CENTRAL, **(pick or {})}
    bad = [k for k in s if k not in CENTRAL]
    if bad or s["policy"] not in POLICIES or s["pace"] not in dict(PACES) or s["adoption"] not in ADOPTIONS \
            or s["robots"] not in ROBOTS or s["shape"] not in ("2000", "ramp"):
        raise ValueError(f"no such run: {pick}")
    if s["size"] == 0:
        s.update(speed=1.0, shape="2000", start=PEAK)
    return s


def run(pick: dict | None = None, regs: dict | None = None, cm=None, push: bool = True) -> dict:
    """One run of the engine by its settings: {settings, regions, rules (with their levers' dates), dates, shock, out,
    n}. The levers start the month after the region's own unemployment has risen by the rules' trigger in this run."""
    s = settings_of(pick)
    cm = cm or stored()[0]
    regs = regs or regions()
    rg = {r: replace(g, eta=g.eta * ADOPTIONS[s["adoption"]]) for r, g in regs.items()}
    delay = delay_of(s["start"], s["shape"])
    n = length(delay)
    shock = gc.ai_shock(n, s["size"], s["speed"], delay=delay, shape=s["shape"], dt=DT) if s["size"] > 0 else gc.Shock()
    shock.drift = pace_paths(s["pace"], n, rg)
    if push:
        shock.push = push_paths(rg, n, cm)[0]
    waves = gc.Waves(split=True, robot_lag=ROBOTS[s["robots"]], absorb=True)
    rl = gc.PRESETS[POLICIES[s["policy"]]]
    dates = gc.trigger_dates(rg, rl, shock, cm, n, DT, waves=waves)
    rules = gc.dated(rl, dates)
    out = gc.simulate(rg, rules, shock, cm, n, waves=waves, dt=DT)
    return {"settings": s, "regions": rg, "rules": rules, "dates": dates, "shock": shock, "out": out, "n": n, "waves": waves}


# ------------------------------------------------------------------ reading a run
def q_of(label: str) -> int:
    """The quarterly index of a quarter named '2028Q4'."""
    return int(label[:4]) * 4 + int(label[-1]) - 1 - (int(gc.START[:4]) * 4 + int(gc.START[-1]) - 1)


def quarters(x) -> np.ndarray:
    return gc.to_quarters(np.asarray(x, float), DT)


def four(rg: dict, out: dict) -> np.ndarray:
    """The four economies' output against capacity together, size-weighted, by step."""
    tot = sum(rg[r].size for r in gc.R)
    return sum(rg[r].size * np.asarray(out[r]["y"]) for r in gc.R) / tot


def verdict(out_min: float, us_peak: float, us_u0: float) -> str:
    """The run's outcome in a word (the page's reading, web/model_export.verdict): on the four economies' output at its
    worst and the US share out of work at its highest."""
    if out_min <= -20:
        return "depression"
    if us_peak >= 15:
        return "labour-held" if out_min > -10 else "labour"
    if out_min <= -4:
        return "deep"
    if out_min <= -2 or us_peak >= us_u0 + 2:
        return "recession"
    return "slowdown"


def sahm_month(u_run: np.ndarray) -> str | None:
    """The first month the US unemployment rate's three-month average is half a point or more above its lowest in the
    twelve months before (the Sahm rule), on the measured rate to the start and the run's after it."""
    hist = vintage.read("UNRATE").dropna()
    hist = hist[:f"{gc.month_label(0)}-28"]
    u = np.concatenate([hist.values[-15:], np.asarray(u_run, float)[1:]])
    avg = np.convolve(u, np.ones(3) / 3, mode="valid")           # avg[j] ends at u[j + 2]
    for j in range(12, len(avg)):
        k = j + 2 - 14                                           # the run's step this average ends at
        if k >= 1 and avg[j] - avg[j - 12:j].min() >= 0.5:
            return gc.month_label(k)
    return None


def readings(r: dict) -> dict:
    """The numbers the case is stated in, each a quarter's average of the run's months unless a month is named."""
    rg, out = r["regions"], r["out"]
    us = out["US"]
    u, left, i, pi, y = (quarters(us[k]) for k in ("u", "out", "i", "pi", "y"))
    oow, f = u + left, quarters(four(rg, out))
    at = lambda x, q: round(float(x[q_of(q)]), 2)  # noqa: E731
    # the first rise in unemployment: its high before the first quarter it has fallen half a point below a high
    hi = 0
    for k in range(1, len(u)):
        if u[k] > u[hi]:
            hi = k
        elif u[hi] - u[k] >= 0.5:
            break
    lo = hi + int(np.argmin(u[hi:]))
    k_rate = int(np.argmax(i))
    lever = {reg: None if d is None else gc.month_label(int(round(d / DT)) + 1) for reg, d in r["dates"].items()}
    res = {
        "us_unemployment": {q: at(u, q) for q in ("2026Q4", "2027Q2", "2027Q4", "2028Q4", "2029Q4", "2030Q4", "2032Q2")},
        "us_out_of_work": {q: at(oow, q) for q in ("2026Q4", "2027Q4", "2028Q4", "2029Q4", "2030Q4", "2032Q2")},
        "us_left_the_workforce_2032Q2": at(left, "2032Q2"),
        "us_unemployment_first_high": [gc.quarter_label(hi), round(float(u[hi]), 2)],
        "us_unemployment_low_after": [gc.quarter_label(lo), round(float(u[lo]), 2)],
        "us_out_of_work_highest": [gc.quarter_label(int(np.argmax(oow))), round(float(oow.max()), 2)],
        "still_rising_at_the_end": bool(oow[-1] > oow[-2]),
        "us_sahm_rule_month": sahm_month(us["u"]),
        "us_policy_rate": {q: at(i, q) for q in ("2026Q4", "2027Q2", "2027Q4", "2028Q4", "2030Q4", "2032Q2")},
        "us_policy_rate_high": [gc.quarter_label(k_rate), round(float(i[k_rate]), 2)],
        "us_policy_rate_low": [gc.quarter_label(int(np.argmin(i))), round(float(i.min()), 2)],
        "us_inflation": {q: at(pi, q) for q in ("2027Q4", "2028Q4", "2032Q2")},
        "us_output_worst": [gc.quarter_label(int(np.argmin(y))), round(float(y.min()), 2)],
        "four_output_worst": [gc.quarter_label(int(np.argmin(f))), round(float(f.min()), 2)],
        "us_output": {q: at(y, q) for q in ("2027Q4", "2028Q4", "2029Q4", "2030Q4", "2032Q2")},
        "four_output": {q: at(f, q) for q in ("2027Q4", "2028Q4", "2029Q4", "2030Q4", "2032Q2")},
        # the downturn's own low in output: the four economies' worst quarter up to the first high in US unemployment
        "four_output_worst_in_the_downturn": [gc.quarter_label(int(np.argmin(f[:hi + 1]))), round(float(f[:hi + 1].min()), 2)],
        "us_household_equity_fall_most_pct": round(float(np.max(r["shock"].equity["US"])) * 100, 1) if r["shock"].equity else 0.0,
        "us_pace_summed_to_the_end": round(float(np.sum(r["shock"].drift["US"][1:]) * DT), 2),
        "policy_lever_from": lever,
        "regions": {},
    }
    for reg in gc.R:
        o = out[reg]
        ru, ro = quarters(o["u"]), quarters(o["u"]) + quarters(o["out"])
        res["regions"][reg] = {"out_of_work": {q: at(ro, q) for q in ("2027Q4", "2028Q4", "2030Q4", "2032Q2")},
                               "unemployment_highest": round(float(ru.max()), 2),
                               "output_worst": round(float(quarters(o["y"]).min()), 2),
                               "policy_rate": {q: at(quarters(o["i"]), q) for q in ("2027Q2", "2027Q4", "2028Q4")},
                               "bank_capital_lost_most_pct": round(float(np.max(o["stress"])) * 100)}
    res["verdict"] = verdict(float(f.min()), float(oow.max()), float(u[0]))
    return res


def paths(r: dict) -> dict:
    """The run's paths by quarter, for charts: every region's unemployment, share out of work, output, inflation and
    policy rate; the four economies' output."""
    out = r["out"]
    rd = lambda x: [round(float(v), 2) for v in quarters(x)]  # noqa: E731
    reg = {g: {"unemployment": rd(out[g]["u"]), "out_of_work": rd(np.asarray(out[g]["u"]) + np.asarray(out[g]["out"])),
               "output": rd(out[g]["y"]), "inflation": rd(out[g]["pi"]), "rate": rd(out[g]["i"])} for g in gc.R}
    n_q = len(reg["US"]["output"])
    return {"quarters": [gc.quarter_label(k) for k in range(n_q)], "regions": reg, "four_output": rd(four(r["regions"], out))}


def short(x: dict) -> dict:
    """A run's readings for a table of the runs around the case."""
    return {"us_unemployment_2028Q4": x["us_unemployment"]["2028Q4"], "us_out_of_work_2028Q4": x["us_out_of_work"]["2028Q4"],
            "us_out_of_work_2032Q2": x["us_out_of_work"]["2032Q2"], "us_out_of_work_highest": x["us_out_of_work_highest"],
            "still_rising_at_the_end": x["still_rising_at_the_end"], "us_policy_rate_low": x["us_policy_rate_low"],
            "four_output_worst": x["four_output_worst"], "us_sahm_rule_month": x["us_sahm_rule_month"],
            "us_lever_from": x["policy_lever_from"]["US"], "verdict": x["verdict"],
            "out_of_work_2032Q2": {g: v["out_of_work"]["2032Q2"] for g, v in x["regions"].items()}}


# ------------------------------------------------------------------ the case
def inputs() -> dict:
    """Every input the case adds to the engine, as measured or stated."""
    cm, regs = stored()[0], regions()
    sn = seen()
    _, push = push_paths(regs, N, cm)
    b = gc.bust_2000()["measured"]
    years = [0, 1, 2, 3, 4, 5]
    pace = {}
    for key, doubling in PACES:
        p = us_pace(key, N + 3 * (LATEST - 1))
        pace[key] = {"doubles_every_years": doubling,
                     "us_points_a_year": {gc.month_label(12 * y): round(float(p[12 * y]), 3) for y in years},
                     "reaches_the_ceiling": next((gc.month_label(k) for k, v in enumerate(p) if v >= CEILING), None)}
    return {
        "set": SET, "start": gc.START, "steps": N, "ends": gc.month_label(N - 1),
        "pace": {"seen": sn, "ceiling_points_a_year": CEILING, "options": pace,
                 "ratio_to_the_us": {r: round(regs[r].drift / regs["US"].drift, 2) for r in gc.R}},
        "inflation_in_the_pipeline": push,
        "bust": {"peak": PEAK, "peak_2000": PEAK_2000, "size": CENTRAL["size"],
                 "us_household_equity_fall_at_the_trough_dot_com": round(float(b["equity_fall"].max()), 3),
                 "delay_quarters": delay_of(PEAK)},
        "robots": CENTRAL["robots"], "policy": POLICIES[CENTRAL["policy"]],
        "trigger_points": {k: gc.PRESETS[v].trigger for k, v in POLICIES.items()},
        "vintage": vintage.manifest().get("written") if hasattr(vintage, "manifest") else None,
    }


def build() -> dict:
    cm, regs = stored()[0], regions()
    c = run(None, regs, cm)
    res = {"inputs": inputs(), "settings": c["settings"], "case": readings(c), "paths": paths(c), "around": {}}
    for key, pick in AROUND:
        x = run(pick, regs, cm)
        res["around"][key] = {"changes": pick, **short(readings(x))}
    # the range the pace alone gives, and the bust's size alone (none to dot-com), on the case's other settings: the
    # share of the US workforce out of work in 2032Q2 (a reading on one date soon after a lever starts would mislead:
    # the sharper the downturn, the earlier the response)
    a = res["around"]
    mid = res["case"]["us_out_of_work"]["2032Q2"]
    res["ranges"] = {
        "us_out_of_work_2032Q2_by_pace": [a["the pace stays as seen"]["us_out_of_work_2032Q2"], mid,
                                          a["the pace doubles every year"]["us_out_of_work_2032Q2"]],
        "us_out_of_work_2032Q2_by_bust": [a["funding holds"]["us_out_of_work_2032Q2"], mid,
                                          a["a dot-com-sized bust"]["us_out_of_work_2032Q2"]],
    }
    # the engine as stored, with none of the case's inflation input, on the case's other settings: what the input does
    bare = readings(run(None, regs, cm, push=False))
    res["without_the_inflation_input"] = {"us_policy_rate": bare["us_policy_rate"], "us_inflation": bare["us_inflation"],
                                          "us_unemployment": bare["us_unemployment"]}
    return res


def main():
    res = build()
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "outlook.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
        f.write("\n")
    c = res["case"]
    print("the case:", res["settings"])
    print("  US unemployment", c["us_unemployment"], "| first high", c["us_unemployment_first_high"], "| Sahm", c["us_sahm_rule_month"])
    print("  US out of work", c["us_out_of_work"], "| highest", c["us_out_of_work_highest"], "rising" if c["still_rising_at_the_end"] else "")
    print("  US policy rate", c["us_policy_rate"], "| high", c["us_policy_rate_high"], "| low", c["us_policy_rate_low"])
    print("  US inflation", c["us_inflation"], "| output worst: US", c["us_output_worst"], "four", c["four_output_worst"], "|", c["verdict"])
    print("  levers from", c["policy_lever_from"])
    for k, v in res["around"].items():
        print(f"  {k:40} u 2028Q4 {v['us_unemployment_2028Q4']:5.2f}  out of work 2028Q4 {v['us_out_of_work_2028Q4']:5.2f}  "
              f"2032Q2 {v['us_out_of_work_2032Q2']:5.2f}  four {v['four_output_worst'][1]:6.2f}  {v['verdict']}")


if __name__ == "__main__":
    main()


