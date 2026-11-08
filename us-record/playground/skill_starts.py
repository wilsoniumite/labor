# skill_starts.py — starts for the skill split's two fits (her go, 2026-11-08: "go ahead with step 1, BLS is fine for
# now"). The split's settings are the main case's (results/fit_Br0.json) with --skill, and with --pay for each good's pay.
# Candidates: the main case and services apart (results/fit_Bs.json) with the services groups on their clocks and some
# with high-skill services slower; each is fitted once here (fit_base.run_start), and the fitted points are written as
# "fits" for fit_base --start-fits (its three best become starts beside the calibrated ones and the --ref start).
# Writes playground/skill_starts_one.json (one wage), skill_starts_pay.json (each good's pay moving as its industries'
# did, the average left free) and skill_starts_lvl.json (each good's pay at its industries' level, the average held at the
# production wage).
# Run from us-record/:  python3 playground/skill_starts.py
import json
import sys
from multiprocessing import Pool

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

B0 = json.load(open("results/fit_Br0.json"))
BS = json.load(open("results/fit_Bs.json"))["best"]["par"]
P0 = B0["best"]["par"]
META = dict(B0["meta"], services="skill", pay=None, names=B0["meta"]["names"] + ["g_low", "g_high"],
            extra=["wage_durables", "wage_ndg", "wage_low", "wage_high"])
g, gs = P0["g_eta"], BS["g_srv"]
CANDIDATES = [(dict(P0, g_low=g, g_high=g), "main case, services on nondurables' clock"),
              (dict(P0, g_low=g, g_high=g - 0.015), "main case, high-skill 1.5 points slower"),
              (dict(P0, g_low=g, g_high=g - 0.03), "main case, high-skill 3 points slower"),
              (dict(P0, g_low=g + 0.005, g_high=g - 0.02), "main case, low faster, high slower"),
              (dict({k: v for k, v in BS.items() if k != "g_srv"}, g_low=gs, g_high=gs), "services apart's fit"),
              (dict({k: v for k, v in BS.items() if k != "g_srv"}, g_low=BS["g_eta"], g_high=gs - 0.01),
               "services apart's fit, low on nondurables' clock, high slower")]


def fit(job):
    pay, start, label = job
    F.configure(dict(META, pay=pay))
    r = F.run_start(F.complete(dict(start)))
    return dict(pay=pay, label=label, misfit=r["misfit"], par=r["par"], nfev=r["nfev"])


if __name__ == "__main__":
    jobs = [(pay, st, lab) for pay in (None, "record", "levels") for st, lab in CANDIDATES]
    with Pool(4) as pool:
        out = pool.map(fit, jobs)
    for pay, name in ((None, "one"), ("record", "pay"), ("levels", "lvl")):
        fits = sorted([r for r in out if r["pay"] == pay], key=lambda r: r["misfit"])
        json.dump(dict(meta=dict(META, pay=pay), fits=fits), open(f"playground/skill_starts_{name}.json", "w"), indent=1)
        print(name, [(round(r["misfit"], 3), r["label"]) for r in fits])
