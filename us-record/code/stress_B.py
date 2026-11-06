# stress_B.py — model B (results/fit_B.json, STATE.md decision 23) under stress: does the fit hold, and do its readings,
# when what was set or chosen moves? Every variant is refitted from B's best. A set value that moves far is stepped there
# (refitting at each step, so the fit follows the same optimum); a variant whose fit fails from B is retried from the
# calibrated 1950 starts (fit_base.starts). Groups:
#   split    fitted on 1950-1995 (or 1950-1985) only, then read on the later years, out of sample, with the inputs as
#            measured (adults, depreciation, the utility's knots); once more with the utility held after 1990, so that
#            nothing after 1990 enters but adults and depreciation
#   drop     one targeted series left out of the misfit: how well do the other four predict it?
#   set      a set value moved: the basket's elasticity (and the one consistent with B's own goods price), the utility's
#            knot years, the year women's entry ends, the return, the schedule's floor g0
#   simpler  one free number fewer, or a path set more simply
#   ablate   one of B's pieces taken out (the official twin of playground/newmodel.js)
#   profile  the clock's pace held on a grid, everything else refitted: how sharply does the record pin the clock?
# Run from us-record/:  python3 code/stress_B.py      (writes results/stress_B.json; a few minutes on four cores)

import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np
from tqdm.auto import tqdm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402

B = json.load(open(os.path.join(ROOT, "results", "fit_B.json")))
META, PAR = B["meta"], B["best"]["par"]
NAMES = META["names"]


def v(group, name, steps, record_steps=False, note=""):
    """A variant: its meta changes in steps (the last is the variant itself); record_steps keeps every step's fit."""
    return dict(group=group, name=name, steps=steps if isinstance(steps, list) else [steps], record_steps=record_steps,
                note=note)


def stepped(key, values, **extra):
    return [dict(extra, **{key: x}) for x in values]


VARIANTS = [
    v("split", "fitted 1950-1995, read 1996-2024", dict(fit_years=[1950, 1995])),
    v("split", "fitted 1950-1985, read 1986-2024", dict(fit_years=[1950, 1985])),
    v("split", "fitted 1950-1995, utility held after 1990", dict(fit_years=[1950, 1995], utility=dict(knots=[1950, 1970, 1990])),
      note="nothing after 1990 enters but adults and depreciation"),
] + [v("drop", f"without {s}", dict(drop=[s])) for s in F.SERIES] + [
    v("set", "basket elasticity 0.75", stepped("sigma", [0.825, 0.775, 0.75])),
    v("set", "basket elasticity 1.0 (Cobb-Douglas)", stepped("sigma", [0.925, 0.975, 1.0])),
    v("set", "basket elasticity 0.636 (set from all-but-shelter prices)", stepped("sigma", [0.825, 0.775, 0.725, 0.675, 0.636]),
      note="the share regression read with B's own goods price"),
    v("set", "utility knots 1950, 1965, 1985, 2024", dict(utility=dict(knots=[1950, 1965, 1985, 2024]))),
    v("set", "utility knots 1950, 1975, 1995, 2024", dict(utility=dict(knots=[1950, 1975, 1995, 2024]))),
    v("set", "women's entry ends 1980", dict(women=1980)),
    v("set", "women's entry ends 2000", dict(women=2000)),
    v("set", "return 1%", stepped("rho_fixed", [0.0175, 0.015, 0.0125, 0.01])),
    v("set", "return 3%", stepped("rho_fixed", [0.0225, 0.025, 0.0275, 0.03])),
    v("set", "schedule floor g0 0.005", [dict(set=dict(META["set"], g0=g, g1=1.0 - g)) for g in (0.0075, 0.005)]),
    v("set", "schedule floor g0 0.02", [dict(set=dict(META["set"], g0=g, g1=1.0 - g)) for g in (0.0125, 0.015, 0.0175, 0.02)]),
    v("simpler", "hours per unit of task capacity steady", dict(hours_per_task=0.0, names=[n for n in NAMES if n != "g_lam"])),
    v("simpler", "utility through the real wage every year", dict(utility=dict(knots=list(range(1950, 2025))))),
    v("ablate", "without women's entry", dict(women=None, names=[n for n in NAMES if n != "chi_w"])),
    v("ablate", "utility rising to 1970, then held", dict(utility=dict(knots=[1950, 1970]))),
    v("ablate", "utility flat", dict(utility=dict(knots=[1950]))),
    v("ablate", "with the cap", dict(cap=F.CAP_SET)),
    v("ablate", "start not pinned", dict(pin_start=False, names=NAMES + ["chi_max"])),
    v("ablate", "without the basket (fixed basket)", stepped("sigma", [0.5, 0.25, 0.1, None], utility=META["utility"])),
    v("ablate", "return free", dict(rho_fixed=None, names=NAMES + ["rho"])),
    v("profile", "clock slower", [dict(fixed=dict(g_eta=g), names=[n for n in NAMES if n != "g_eta"])
                                  for g in (0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04)], record_steps=True),
    v("profile", "clock faster", [dict(fixed=dict(g_eta=g), names=[n for n in NAMES if n != "g_eta"])
                                  for g in (0.13, 0.135, 0.14, 0.145, 0.15, 0.155, 0.16, 0.17, 0.18)], record_steps=True),
]


def readout(par):
    """What a fit says, beyond its misfit: the paths of the targeted series and some insides, and the 2024 readings."""
    m = F.model_path(par)
    dev = F.deviations(m)
    years = np.array(F.YEARS)
    keep = {s: F.counted(s) for s in F.SERIES}
    measured = {s: F.target(s).notna().values for s in F.SERIES}
    out_years = {s: measured[s] & ~keep[s] if F.FIT_YEARS is not None else np.zeros(len(years), bool) for s in F.SERIES}
    sq = lambda s, mask: float(np.mean(dev[s][mask] ** 2)) if mask.any() else None   # noqa: E731
    return dict(
        by_series=F.misfit_by_series(m),
        by_series_in={s: sq(s, keep[s]) for s in F.SERIES},
        by_series_out={s: sq(s, out_years[s]) for s in F.SERIES},
        path={c: [float(x) for x in m[c].values] for c in F.SERIES + ["x", "site_share"] if c in m},
        readings=dict(g_eta=par["g_eta"], hours_per_task=par["g_lam"] - par["g_eta"], x_1950=float(m["x"].iloc[0]),
                      x_2024=float(m["x"].iloc[-1]), labour_share_2024=float(m["labour_share_c"].iloc[-1]),
                      site_share_1950=float(m["site_share"].iloc[0]) if "site_share" in m else None,
                      site_share_2024=float(m["site_share"].iloc[-1]) if "site_share" in m else None,
                      work_cost_by_women=float(np.exp(par["chi_w"])) if "chi_w" in par and F.WOMEN else None))


def fit_variant(var):
    """Steps a variant from B's best; each step refitted from the last (from the calibrated starts if that fails)."""
    t0 = time.time()
    par, meta, records = dict(PAR), dict(META), []
    for step in var["steps"]:
        meta = dict(meta, **step)
        F.configure(meta)
        start = F.complete(par)
        if not F.PIN_START and "chi_max" not in start:
            start["chi_max"] = PAR["chi_max"]
        r = F.run_start(start)
        if r["misfit"] >= 10.0:                       # no equilibrium path from here: the calibrated starts instead
            rs = [F.run_start(F.complete(s)) for s in F.starts()]
            r = min(rs, key=lambda x: x["misfit"])
        par = r["par"]
        if F.PIN_START:
            par["chi_max"] = F.pinned_chi(par)
        if var["record_steps"] or step is var["steps"][-1]:
            records.append(dict(group=var["group"], name=var["name"], note=var["note"], step=step,
                                settings=F.settings_meta(), par=par, misfit=r["misfit"], status=r["status"],
                                **readout(par)))
    for rec in records:
        rec["seconds"] = round(time.time() - t0, 1)
    return records


if __name__ == "__main__":
    # --only NAME: refit only the variants of that name and put them in place of the stored ones (the rest kept)
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    t0 = time.time()
    todo = [x for x in VARIANTS if only is None or x["name"] == only]
    with Pool(min(4, os.cpu_count() or 1)) as pool:
        out = [rec for recs in tqdm(pool.imap(fit_variant, todo), total=len(todo), desc="variants") for rec in recs]
    if only is not None:
        old = json.load(open(os.path.join(ROOT, "results", "stress_B.json")))["variants"]
        names = [x["name"] for x in VARIANTS]
        out = sorted([r for r in old if r["name"] != only] + out, key=lambda r: names.index(r["name"]))
    F.configure(META)
    base = dict(group="B", name="model B", note="", step={}, settings=F.settings_meta(), par=PAR, misfit=B["best"]["misfit"],
                status=None, **readout(PAR))
    with open(os.path.join(ROOT, "results", "stress_B.json"), "w") as f:
        json.dump(dict(meta=dict(source="results/fit_B.json", seconds=round(time.time() - t0, 1)), base=base, variants=out),
                  f, indent=1)
    print(f"results/stress_B.json written ({len(out)} fits, {time.time() - t0:.0f} s)")
    for r in [base] + out:
        o = r["by_series_out"]
        oo = [x for x in o.values() if x is not None]
        print(f"{r['group']:8s} {r['name'][:52]:52s} {r['misfit']:7.3f}  all-years {np.mean(list(r['by_series'].values())):7.3f}"
              + (f"  out {np.mean(oo):7.2f}" if oo else "") + f"  clock {100 * r['par']['g_eta']:5.1f}%"
              f"  hours/task {100 * r['readings']['hours_per_task']:5.1f}%  x2024 {r['readings']['x_2024']:.3f}")
