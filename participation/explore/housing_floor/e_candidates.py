# e_candidates.py — the candidate E-hypotheses of this theme on the explore half, as they would be coded for the
# confirm half (manifest series only), with their explore estimates, one-sided WCR p (B = 9999, 15 clusters with F),
# test-inversion intervals, MDE on 15 clusters, and leave-one-out; plus the robustness that motivated them.
#   E-HF1 (varies D1): A(25-34) on log q_{t-1}, log q_{t-1} x F_c, U = lfsa_urgan Y25-74 TOTAL for every country,
#          country FE, year FE, country linear trends, C3 breaks; 1997-2025 minus 2020-21. H1: b2 < 0.
#   E-HF2 (varies C-1): coresidence 25-34 on the same right-hand side (SILC window 2005-2025). H1: b(q x F) > 0.
# Out: e_candidates.json, fig/e_candidates_loo.png; estimates logged.

import json
import os

import numpy as np

import common as C

raw, cy, cl = C.load()
cyl = C.with_lfs_cycle(raw, cy)
plt = C.style()
geos = sorted(set(cy.index.get_level_values(0)))
fstd = C.specs.f_constants(cl, geos)
ctx = C.specs.Ctx(cl, fstd)
B = 9999
CANDS = {
    "E-HF1": dict(base="D1", over=dict(), side=-1),
    "E-HF2": dict(base="C1", over=dict(x="Q*F", z=["Q"], side=1), side=1),
}
out = {}
for k, c in CANDS.items():
    spec = dict(C.specs.TESTS[c["base"]]); spec.update(c["over"])
    r = C.specs.estimate(cyl, cl, spec, ctx, geos, variant="country_trends", B=B, with_ci=True)
    C.log_spec(f"{k} final", r)
    loo = {}
    for g in r["geos_used"]:
        rr = C.run(f"{k} LOO -{g}", cyl, cl, base=c["base"], B=B, variant="country_trends",
                   geos=[x for x in geos if x != g], fstd=fstd, **c["over"])
        loo[g] = dict(beta=rr["beta"], se=rr["se"], p=rr["p"])
    worst = max(loo.items(), key=lambda kv: kv[1]["p"])
    out[k] = dict(beta=r["beta"], se=r["se"], p=r["p"], p_opposite=r["p_opposite"], ci=r["ci"],
                  ci_one_sided=r["ci_one_sided"], n=r["n"], G=r["G"], G_star=r["G_star"],
                  years=[min(r["years_used"]), max(r["years_used"])], geos=r["geos_used"],
                  mde_15=C.inf.mde(r["se"], 15), loo=loo, loo_max_p=worst[1]["p"], loo_max_p_country=worst[0])
    print(f"{k}: {C.fmt(r)} ci1={r['ci_one_sided']} ci={r['ci']} mde15={C.inf.mde(r['se'], 15):.2f} "
          f"LOO max p={worst[1]['p']:.3f} (-{worst[0]})")

# E-HF2 robustness (the D1 side was done in checks.py)
def swap_q(frame, col):
    f = frame.copy(); f["logq_l1"] = f[col]; f["logq_l1__breaks"] = f[col + "__breaks"]; return f


rob = {}
for lab, fr, kw in (("q_cp00", swap_q(cyl, "logq_cp00_l1"), {}), ("q_comp", swap_q(cyl, "logq_comp_l1"), {}),
                    ("q_hpi", swap_q(cyl, "logq_hpi_l1"), {}), ("no cycle control", cyl, dict(controls=[])),
                    ("2009+", cyl, dict(years=(2009, 2025))), ("2005-2019", cyl, dict(years=(2005, 2019)))):
    r = C.run(f"E-HF2 trends {lab}", fr, cl, base="C1", B=B, variant="country_trends",
              **{**CANDS["E-HF2"]["over"], **kw})
    rob[lab] = dict(beta=r["beta"], se=r["se"], p=r["p"], n=r["n"], G=r["G"])
    print(f"   E-HF2 {lab:18s} {C.fmt(r)}")
out["E-HF2 robustness"] = rob

# implied slopes of A on q at F = 25th and 75th percentile (E-HF1 terms; descriptive, CR1 via the swap trick)
F = ctx.F.reindex(out["E-HF1"]["geos"]).to_numpy(float)
for pct in (25, 75):
    f0 = float(np.percentile(F, pct))
    cl2 = cl.copy(); cl2["F_raw"] = cl["F_raw"] - f0 * fstd[1]   # shift so the main effect is the slope at f0
    r = C.run(f"E-HF1 implied slope at F p{pct}", cyl, cl2, base="D1", B=B, variant="country_trends", x="Q",
              z=["Q*F"], side=0, fstd=fstd)
    out[f"E-HF1 slope at F p{pct}"] = dict(F_std=f0, beta=r["beta"], se=r["se"], p_two_sided=r["p"])
    print(f"   slope of A on log q at F p{pct} (std {f0:+.2f}): {r['beta']:+.2f} (se {r['se']:.2f}, two-sided p {r['p']:.3f})")

json.dump(C.specs.clean_json(out), open(os.path.join(C.HERE, "e_candidates.json"), "w"), indent=1)

fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
for ax, k, lab in ((axs[0], "E-HF1", "activity 25-34: b on log q x F"),
                   (axs[1], "E-HF2", "coresidence 25-34: b on log q x F")):
    loo = out[k]["loo"]
    gs = list(loo)
    b = [loo[g]["beta"] for g in gs]
    se = [loo[g]["se"] for g in gs]
    ax.errorbar(range(len(gs)), b, yerr=1.645 * np.array(se), fmt="o", color=C.BLUE, ms=4, lw=1)
    ax.axhline(out[k]["beta"], color=C.ORANGE, lw=1.2, label=f"all countries: {out[k]['beta']:+.1f}")
    ax.axhline(0, color=C.GRAY, lw=0.8)
    ax.set_xticks(range(len(gs)), ["-" + g for g in gs], fontsize=7)
    ax.set_title(f"{k}, leave one country out ({lab})", loc="left")
    ax.legend(loc="best")
fig.supxlabel("country left out; bars = estimate +/- 1.645 CR1 se; country trends, lfsa_urgan U", color=C.MUTED,
              fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(C.FIG, "e_candidates_loo.png"), dpi=130)
