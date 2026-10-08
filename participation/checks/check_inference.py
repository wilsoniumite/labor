# check_inference.py — the inference of code/inference.py on synthetic panels (code/simulate_inference.py): size, power,
# randomisation-inference size, CI coverage, agreement with a direct least-squares fit, and the D1-like and D2-like
# designs (an interaction with a country moderator and a dominant country; a within-country square), as the design
# review asks before the P freeze. The results must come from the current code: the SHA-256 of code/inference.py and
# code/simulate_inference.py recorded in the JSON must equal the files' (otherwise rerun the simulation).
#
# Run from participation/:  ../venv/Scripts/python.exe checks/check_inference.py
# Reads results/simulate_inference.json. Exit status 0 only if every check passes.

from __future__ import annotations

import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


S = json.load(open(os.path.join(ROOT, "results", "simulate_inference.json"), encoding="utf-8"))
sp, ri, cv, d = S["size_power"], S["ri"], S["ci"], S["direct"]

rec = S.get("code_sha256", {})
now = {f: hashlib.sha256(open(os.path.join(ROOT, "code", f), "rb").read().replace(b"\r\n", b"\n")).hexdigest()
       for f in ("inference.py", "simulate_inference.py")}
check("0 the results were computed by the current code/inference.py and code/simulate_inference.py (SHA-256)",
      rec == now, "; ".join(f"{f}: recorded {str(rec.get(f))[:12]}, now {h[:12]}" for f, h in now.items()))

for g in ("G15", "G31"):
    r = sp[g]
    check(f"I size, {g}: the one-sided 5% WCR test rejects a true null in 3-7% of {r['panels']} panels "
          f"(T about 25, AR(1) 0.7 errors, unequal cluster variances)",
          r["panels"] >= 1000 and 0.03 <= r["reject_one_sided_5pct"] <= 0.07 and 20 <= r["mean_T"] <= 27,
          f"{r['reject_one_sided_5pct']:.3f} (other side {r['reject_opposite_side_5pct']:.3f}, naive CR1 t "
          f"{r['reject_naive_cr1_t']:.3f}); mean T {r['mean_T']:.1f}, G* {r['mean_G_star']:.1f}")
for g in ("G15", "G31"):
    r, pw = sp[g], sp[g]["power"]
    check(f"II power, {g}: rejection rises with a planted effect of 1, 2, 3 mean CR1 se, starts above size, "
          f"reaches 0.6 or more at 3 se",
          r["reject_one_sided_5pct"] < pw["1"] < pw["2"] < pw["3"] and pw["3"] >= 0.6,
          f"{pw} (mean CR1 se {r['mean_cr1_se']:.3f}, sd of beta-hat {r['sd_beta_hat']:.3f})")
for k, r in ri.items():
    check(f"III randomisation inference under a sharp null, {k}: 5% rejection in 3-7% of {r['draws']} draws",
          r["draws"] >= 1000 and 0.03 <= r["reject_5pct"] <= 0.07, f"{r['reject_5pct']:.3f}, {r['n_perm']} "
          f"assignments, exact={r['exact']}")
check("III the small case is enumerated exactly (3!3!2! = 72 assignments), the 31-country cases are drawn",
      ri["exact_G8_CR1"]["exact"] and ri["exact_G8_CR1"]["n_perm"] == 72
      and not ri["panel_c4_G31_CR1"]["exact"] and not ri["cross_section_c5_G31_HC2"]["exact"])
for g in ("G15", "G31"):
    r = cv[g]
    check(f"IV ci(), {g}: the two-sided 95% interval by test inversion covers the true beta in 93-97% of "
          f"{r['panels']} panels", r["panels"] >= 1000 and 0.93 <= r["coverage"] <= 0.97,
          f"{r['coverage']:.3f}, mean width {r['mean_width']:.2f}")
mo = S.get("moderated", {})
for kind in ("D1", "D2"):
    for g in ("G15", "G31"):
        r = mo.get(f"{kind}_like_{g}")
        check(f"VI {kind}-like design, {g}: the one-sided 5% WCR test (H1 < 0) rejects a true null in 3-7% of "
              f"{r['panels'] if r else 0} panels, the opposite side too; power at 3 se above 0.5",
              bool(r) and r["panels"] >= 1000 and 0.03 <= r["reject_one_sided_5pct"] <= 0.07
              and 0.03 <= r["reject_opposite_side_5pct"] <= 0.07 and r["power_3se"] > 0.5,
              f"{r['reject_one_sided_5pct']:.3f} (other side {r['reject_opposite_side_5pct']:.3f}, naive CR1 t "
              f"{r['reject_naive_cr1_t']:.3f}); power {r['power_3se']:.3f}; G* mean {r['mean_G_star']:.1f}, "
              f"below 8 in {r['share_G_star_below_8']:.0%}" if r else "missing: rerun code/simulate_inference.py")
check("V wcr's beta and CR1 se equal a direct dummy-variable least-squares fit with the CR1 sandwich (to 1e-8)",
      d["abs_diff_beta"] <= 1e-8 and d["abs_diff_se"] <= 1e-8,
      f"beta {d['beta_wcr']:.10f} vs {d['beta_direct']:.10f}; se {d['se_wcr']:.10f} vs {d['se_direct']:.10f}")
check("V a rank-deficient Z (every dummy level, a constant, a duplicated column) gives the same beta, se and p",
      d["rank_deficient_abs_diff_beta"] <= 1e-8 and d["rank_deficient_abs_diff_se"] <= 1e-8 and d["rank_deficient_same_p"],
      f"diffs {d['rank_deficient_abs_diff_beta']:.1e}, {d['rank_deficient_abs_diff_se']:.1e}")
check("V the cluster-score bootstrap equals the literal N x B form of the design review (t*, to 1e-8)",
      d["literal_bootstrap_max_abs_diff_tstar"] <= 1e-8, f"max |diff| {d['literal_bootstrap_max_abs_diff_tstar']:.1e}")
check("V ri's observed statistic equals wcr's (CR1), and its HC2 t a direct HC2 fit (to 1e-8)",
      d["ri_vs_wcr_abs_diff_t"] <= 1e-8 and d["ri_vs_wcr_abs_diff_beta"] <= 1e-8 and d["hc2_abs_diff_t"] <= 1e-8,
      f"{d['ri_vs_wcr_abs_diff_t']:.1e}, {d['ri_vs_wcr_abs_diff_beta']:.1e}, {d['hc2_abs_diff_t']:.1e}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
