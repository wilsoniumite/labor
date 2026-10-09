# opening.py — opening a half in the order of PROTOCOL L14: q first; the knots from q alone, recorded with their hash
# in the fetch log; F_L read (recorded); at the look, H computed once and recorded; only then the outcomes.
#
# open_half(half, countries) -> dict(raw, cy, cl, knots, H, census, ...). The explore opening (after the L-freeze tag)
# runs it with half='explore' on the explore countries; the look (confirm.py, after the LE-freeze tag) with
# half='confirm' on every country of the split, in one vintage. At the look the explore countries keep the knots their
# FIRST explore opening recorded, for q and for q_hpi alike (L14: knots are never recomputed after outcomes are seen);
# the new vintage's knots and each country's q path (its hash) are computed only to report any difference.
# A half's knots are recorded once: a second opening of a half with record=True is refused (a later explore session
# opens with record=False and keeps the first record).
# q comes from the frozen L2 ladder (data/coverage.json 'q_ladder'; build.ladders_of): a missing or flagged value is NaN
# inside its run and never moves a run or a membership. q_hpi's knots lie inside its longest piece by the same rule as
# q's chosen segment (the most q years whose observation year is in the window; ties: the later), from q_hpi alone.
# The frozen inputs are read from the working copy, which every guard requires to equal the L-freeze commit
# (fetch.pinned_unchanged): data/coverage.json (memberships, chosen q segments, ladders), data/segments.csv,
# data/ipums_samples.json.
#
# Library module (no run line); used by confirm.py and, for the explore half, by hand after the L-freeze.

from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402
import fetch  # noqa: E402
import ipums  # noqa: E402
import segments as sg  # noqa: E402
import specs  # noqa: E402

CUBE = os.path.join(LROOT, "data", "coverage.json")


def frozen_cube() -> dict:
    return json.load(open(CUBE, encoding="utf-8"))


def chosen_segments(cube: dict) -> dict:
    return {c: tuple(v["chosen_q_segment"]) for c, v in cube["countries"].items() if v["chosen_q_segment"]}


def knots_payload(kn: dict) -> dict:
    return {c: {k: v for k, v in d.items() if k in ("n", "k1", "k2", "years", "piece")} for c, d in kn.items()}


def q_hashes(qp: pd.DataFrame, col: str = "logq_l1") -> dict:
    """{country: SHA-256 of its q path} (observation year, value rounded to 10 decimals; NaN as null)."""
    out = {}
    d = qp.reset_index()
    for c, e in d.groupby("geo"):
        path = [[int(t), (None if not np.isfinite(v) else round(float(v), 10))]
                for t, v in zip(e["year"], pd.to_numeric(e[col], errors="coerce"))]
        out[str(c)] = hashlib.sha256(json.dumps(path, separators=(",", ":")).encode()).hexdigest()
    return out


def logged_knots(half: str) -> dict:
    """The FIRST knots record of a half (L14: the opening's knots; a later record never replaces them)."""
    rec = fetch.recorded("knots", half)
    return rec[0]["payload"] if rec else {}


def compute_H(cube: dict, cl: pd.DataFrame, kn: dict) -> dict:
    """L9: H over LR-K2's frozen members left after the mechanical drops (an unusable F_L sample; fewer than 6 ranked
    q years), once."""
    k2 = cube["families"]["members"].get("K2", [])
    F = {c: float(cl.loc[c, "F_L"]) for c in k2 if c in cl.index and np.isfinite(cl.loc[c, "F_L"])
         and kn.get(c, {}).get("k1") is not None}
    return specs.compute_H(F, list(F))


def hpi_spans(qp: pd.DataFrame) -> dict:
    """q_hpi's span per country (its first and last q year); knots() then takes the longest piece inside it."""
    d = qp.reset_index()
    d = d[np.isfinite(pd.to_numeric(d["logq_hpi_l1"], errors="coerce"))]
    return {c: (int(e["year"].min()) - 1, int(e["year"].max()) - 1) for c, e in d.groupby("geo")}


def open_half(half: str, countries: list[str], extract_b: bool = False, record: bool = True) -> dict:
    """The opening of a half (see the header). Every door it calls is guarded."""
    fetch.allowed_countries(half)                             # refuses before anything if the half is closed
    if record and fetch.recorded("knots", half):
        raise fetch.BlindingError(f"the {half} half's knots are already recorded (L14: recorded once); open it again "
                                  "with record=False")
    cube = frozen_cube()
    ladders = build.ladders_of(cube)
    seg = sg.load()
    chosen = chosen_segments(cube)
    raw = build.fetch_regressors(half, countries)            # 1. q first
    qp = build.panel(raw, countries, seg, ladders)
    kn_new = specs.knots(qp[["logq_l1", "qseg_l1"]], {c: chosen[c] for c in countries if c in chosen})
    qh = qp[["logq_hpi_l1", "qseg_hpi_l1"]].rename(columns={"logq_hpi_l1": "logq_l1", "qseg_hpi_l1": "qseg_l1"})
    spans = hpi_spans(qp)
    kn_hpi = specs.knots(qh, {c: spans[c] for c in countries if c in spans})
    hashes = {"q": q_hashes(qp), "q_hpi": q_hashes(qp, "logq_hpi_l1")}
    vintage = {}
    if half == "confirm":                                     # explore countries keep their explore-opening knots
        first = logged_knots("explore")
        for key, kn in (("q", kn_new), ("q_hpi", kn_hpi)):
            kept = first.get(key, {})
            for c, k in kept.items():
                old_hash = (first.get("q_hash", {}).get(key) or {}).get(c)
                v = {"explore_k1": k.get("k1"), "explore_k2": k.get("k2"),
                     "new_k1": kn.get(c, {}).get("k1"), "new_k2": kn.get(c, {}).get("k2"),
                     "q_path_changed": (old_hash != hashes[key].get(c)) if old_hash else None}
                v["differ"] = (k.get("k1"), k.get("k2")) != (v["new_k1"], v["new_k2"])
                vintage.setdefault(key, {})[c] = v
                kn[c] = {**kn.get(c, {}), "k1": k.get("k1"), "k2": k.get("k2"), "years": k.get("years"),
                         "n": k.get("n"), "piece": k.get("piece")}
    knots = {"q": kn_new, "q_hpi": kn_hpi}
    if record:                                                # 2. knots recorded before any outcome
        fetch.record("knots", half, {"q": knots_payload(kn_new), "q_hpi": knots_payload(kn_hpi),
                                     "q_hash": hashes, "geos": sorted(countries)}, by=fetch.KNOTS_BY)
    fl = ipums.F_L(half, "F_L", record=record)                # 3. F_L (recorded)
    try:
        fl70 = ipums.F_L(half, "F_L_1970", record=False)
    except ipums.ExtractError:
        fl70 = {}
    smp = json.load(open(ipums.SAMPLES, encoding="utf-8"))
    cl = build.country_level(fl, fl70, None, smp, countries)
    H = compute_H(cube, cl, kn_new) if half == "confirm" else {}
    if half == "confirm" and record:
        fetch.record("H", half, H)                            # 4. H, once
    raw.update(build.fetch_outcomes(half, countries))         # 5. outcomes
    controls = build.fetch_controls(half, countries)
    raw.update(controls)
    cl = build.country_level(fl, fl70, controls.get("gn"), smp, countries)
    cy = build.panel(raw, countries, seg, ladders)
    census = pd.DataFrame()
    if extract_b:
        R = ipums.extract_b(half)
        census = build.census(R, cy, seg)
    return dict(raw=raw, cy=cy, cl=cl, knots=knots, H=H, census=census, vintage_knots=vintage, cube=cube,
                kholodilin_uncovered=build.kholodilin_uncovered(raw, countries))
