# common.py — shared loading and estimation for the housing_floor exploration (explore half only).
#
# Data come only through explore/data.py. Estimation reuses the frozen pipeline's own functions (specs.frame,
# specs.design, inference.wcr) without modifying them, so every variant differs from the frozen D1/D2 only in what is
# named. Every estimated specification is appended to SPECS_LOG (a running count for the forking-paths ledger).

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "explore"))
sys.path.insert(0, os.path.join(ROOT, "code"))
import data  # noqa: E402
import build  # noqa: E402
import specs  # noqa: E402
import inference as inf  # noqa: E402

SPECS_LOG = os.path.join(HERE, "specs_log.jsonl")
FIG = os.path.join(HERE, "fig")
os.makedirs(FIG, exist_ok=True)

BLUE, ORANGE, AQUA, GRAY, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#9a9893", "#0b0b0b", "#52514e"
CEE = ["BG", "EE", "HR", "HU", "LV", "PL"]


def load():
    raw = data.manifest_raw()
    cy = build.country_year("explore", raw=raw)
    cl = build.country_level("explore", raw=raw)
    return raw, cy, cl


def with_lfs_cycle(raw, cy):
    """cy with U, U2554, U1529 replaced by lfsa_urgan (citizen TOTAL) for every country (C7's fallback source,
    used whole for all countries; no splice). Break lists from that series."""
    out = cy.copy()
    grid = out.index
    for name, age in (("U", "Y25-74"), ("U2554", "Y25-54"), ("U1529", "Y15-29")):
        s, b = build.cell(raw["une_lfs"], age=age)
        out[name] = s.reindex(grid).to_numpy(float)
        out[name + "__breaks"] = [list(b.get(g, [])) for g in grid.get_level_values(0)]
    return out


def add_var(cy, name, s: pd.Series, breaks: dict | None = None):
    out = cy.copy()
    out[name] = s.reindex(out.index).to_numpy(float)
    out[name + "__breaks"] = [list((breaks or {}).get(g, [])) for g in out.index.get_level_values(0)]
    return out


def log_spec(label: str, r: dict, extra: dict | None = None):
    rec = dict(label=label, **{k: r.get(k) for k in ("beta", "se", "p", "p_opposite", "n", "G", "G_star", "mde")},
               years=[min(r["years_used"]), max(r["years_used"])] if r.get("years_used") else None,
               geos=r.get("geos_used"), **(extra or {}))
    with open(SPECS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(specs.clean_json(rec)) + "\n")
    return rec


def run(label, cy, cl, base="D1", B=9999, variant=None, geos=None, fstd=None, log=True, **over):
    """specs.estimate on a modified copy of a frozen test (base) with overrides (outcome, x, z, controls, years, side,
    fe). Returns the result dict; logs it."""
    spec = dict(specs.TESTS[base])
    spec.update(over)
    geos = sorted(set(cy.index.get_level_values(0))) if geos is None else sorted(geos)
    fstd = specs.f_constants(cl, geos) if fstd is None else fstd
    ctx = specs.Ctx(cl, fstd)
    r = specs.estimate(cy, cl, spec, ctx, geos, variant=variant, B=B, with_ci=False)
    if log:
        log_spec(label, r, dict(base=base, variant=variant,
                                over={k: (v if not isinstance(v, tuple) else list(v)) for k, v in over.items()}))
    return r


def fmt(r):
    return (f"b={r['beta']:+.3f} se={r['se']:.3f} p={r['p']:.3f} p_opp={r['p_opposite']:.3f} n={r['n']} "
            f"G={r['G']} G*={r['G_star']:.1f} yrs={min(r['years_used'])}-{max(r['years_used'])} "
            f"mde={inf.mde(r['se'], r['G']):.2f}")


def style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": GRAY, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                         "ytick.color": MUTED, "axes.titlesize": 9, "axes.titlecolor": INK,
                         "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.6,
                         "lines.linewidth": 1.6, "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                         "savefig.facecolor": "#fcfcfb", "legend.frameon": False})
    return plt
