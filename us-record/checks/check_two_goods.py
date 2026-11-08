# check_two_goods.py — the two-good economy (code/two_goods.py, durables apart) against the one-good pinning model:
#   N  nesting: with durables on the other goods' clock the two goods are one. Every year of the main case
#      (results/fit_Bw.json) re-solved as two goods, at any composite elasticity and durables share, gives the one-good
#      solution (relative 1e-9): the wage, the price, the task line, participation, labour's share, theta_V, the chain.
#      fit_base's two-good path at g_dur = g_eta gives the main case's five series and misfit (1e-9).
#   I  identities, with durables on a faster clock: labour demand equals supply; income equals the baskets' cost
#      (consumption is income); land adds up (sites in baskets and the machines' land are T); the composite's unit cost
#      is its goods' cost; at the reference point the composite's demands are the reference shares.
#   M  monotone: a faster durables clock makes durables cheaper against the other goods.
#   S  services apart (2026-11-08): nesting, identities, the nest, a slower services clock.
#   K  the skill split and a worker for each good (2026-11-08): with both services groups on nondurables' clock and one
#      wage the split is the main case; with the groups on one services clock it is services apart, year by year; pay at
#      one is one wage bit for bit; with each good's pay from the record the accounts add up; dearer high-skill workers
#      make high-skill services dearer and machines take more of their tasks; with pay at its industries' level the
#      model's average pay is the production wage.
# Run from us-record/:  python3 checks/check_two_goods.py      Exit 0 only if every check passes.

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402
import two_goods as tg  # noqa: E402

pm = F.pm
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


R = json.load(open(os.path.join(ROOT, "results", "fit_Bw.json")))
F.configure(R["meta"])
par = F.fill(R["best"]["par"])
par = dict(par, chi_max=F.pinned_chi(par))
p_ref = pm.solve(F.economies(par)[0])["p"]
es = F.economies(par, p_ref=p_ref)

# ---- N: nesting
worst, keys = 0.0, ("v", "x", "participation", "labour_share_bea", "theta_V", "chain_share")
for sig, w in ((0.72, 0.19), (1.0, 0.5), (1.6, 0.05)):
    cmp = dict(omega_d=w, sigma_dg=sig, pref_d=p_ref, pref_g=p_ref)
    for e in es:
        q1, q2 = pm.solve(e), tg.solve(e, e.eta, cmp)
        q2 = dict(q2, x=q2["xg"])
        worst = max(worst, max(abs(q2[k] - q1[k]) / abs(q1[k]) for k in keys), abs(q2["pg"] - q1["p"]) / q1["p"],
                    abs(q2["pd"] - q1["p"]) / q1["p"], abs(q2["c"] - q1["p"]) / q1["p"])
check("N1 durables on the other goods' clock: every year of the main case, as two goods, is the one-good solution "
      "(three composites; relative 1e-9)", worst < 1e-9, f"{worst:.1e}")
q1 = pm.solve(F.economies(par)[0])
q2 = tg.solve(F.economies(par)[0], F.economies(par)[0].eta, dict(mode="ref", omega_d=0.19))
gap = max(abs(q2["v"] - q1["v"]) / q1["v"], abs(q2["participation"] - q1["participation"]))
check("N2 the reference point (1950) with one clock is the one-good solution (1e-9)", gap < 1e-9, f"{gap:.1e}")
m1 = F.model_path(R["best"]["par"])
F.configure(dict(R["meta"], durables=dict(sigma_dg=F.SIGMA_DG_SET, omega_d=F.OMEGA_D_SET), extra=["wage_durables"],
                 names=R["meta"]["names"] + ["g_dur"]))
par2 = dict(R["best"]["par"], g_dur=R["best"]["par"]["g_eta"])
m2 = F.model_path(par2)
gap = max(float(np.max(np.abs(m2[s].values - m1[s].values) / np.abs(m1[s].values))) for s in F.SERIES)
gap_w = float(np.max(np.abs(m2["wage_durables"].values - m1["wage_goods"].values) / m1["wage_goods"].values))
check("N3 fit_base's two-good path at g_dur = g_eta gives the main case's five series, and the durables wage is the "
      "goods wage (1e-9)", gap < 1e-9 and gap_w < 1e-9, f"{gap:.1e}, {gap_w:.1e}")

# ---- I: identities, durables on a faster clock
par3 = dict(R["best"]["par"], g_dur=R["best"]["par"]["g_eta"] + 0.04)
got = F.durables_years(par3)
check("I0 with durables 4 points a year faster the two-good economy has an equilibrium every year", got is not None)
if got is not None:
    qs, es3 = got
    w_lab = max(abs(q["nD"] - q["nS"]) / q["nD"] for q in qs)
    w_inc = max(abs(q["income"] - q["Ps"] * q["B"]) / q["income"] for q in qs)
    w_land = max(abs(q["B"] * q["sb"] + e.b * e.delta * q["K"] - e.T) / e.T for q, e in zip(qs, es3))
    w_cost = max(abs(q["dd"] * q["pd"] + q["dg"] * q["pg"] - q["c"]) / q["c"] for q in qs)
    check("I1 labour demand equals supply every year (1e-9)", w_lab < 1e-9, f"{w_lab:.1e}")
    check("I2 income is the baskets' cost every year: wages, land rent and interest buy every basket (1e-9)",
          w_inc < 1e-9, f"{w_inc:.1e}")
    check("I3 land adds up every year: sites in baskets and the machines' land are T (1e-9)", w_land < 1e-9, f"{w_land:.1e}")
    check("I4 the composite's unit cost is its goods' cost every year (1e-12)", w_cost < 1e-12, f"{w_cost:.1e}")
    q0 = qs[0]
    check("I5 at the reference point (1950) durables' share of the composite's cost is the set share (1e-12)",
          abs(q0["dur_share"] - F.OMEGA_D_SET) < 1e-12, f"{q0['dur_share']:.6f} vs {F.OMEGA_D_SET:.6f}")
    rel = [q["pd"] / q["pg"] for q in qs]
    m_fast = F.model_path(dict(par3, g_dur=par3["g_eta"] + 0.06))
    ok_m = m_fast is not None and float(m_fast["pd"].iloc[-1] / m_fast["p"].iloc[-1]) < rel[-1]
    check("M1 a faster durables clock makes durables cheaper against the other goods by 2024",
          ok_m and rel[-1] < rel[0], f"durables over other goods, 1950 {rel[0]:.3f}, 2024 {rel[-1]:.3f}")

# ---- services apart (her go, 2026-11-08): on nondurables' clock, services are nondurables, and the three-good economy is
# the two-good one; then services on a slower clock, the accounts adding up and the nest's cost its goods' cost
R0 = json.load(open(os.path.join(ROOT, "results", "fit_Br0.json")))
F.configure(R0["meta"])
m2 = F.model_path(R0["best"]["par"])
F.configure(dict(R0["meta"], services="record", names=R0["meta"]["names"] + ["g_srv"], extra=["wage_durables", "wage_services"]))
par_s = dict(R0["best"]["par"], g_srv=R0["best"]["par"]["g_eta"])
m3 = F.model_path(par_s)
cols = ["wage_goods", "wage_durables", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V", "chain_share"]
worst = max(float(np.max(np.abs(m3[c].values / m2[c].values - 1.0))) for c in cols) if m3 is not None else np.inf
check("S1 services on nondurables' clock: the three-good economy is the main case (fit_Br0) to 1e-12", worst < 1e-12,
      f"worst relative gap {worst:.1e}")
got = F.durables_years(dict(par_s, g_srv=par_s["g_eta"] - 0.01))
check("S2 with services a point a year slower the three-good economy has an equilibrium every year", got is not None)
if got is not None:
    qs, es_ = got
    w_lab = max(abs(q["nD"] - q["nS"]) / q["nD"] for q in qs)
    w_inc = max(abs(q["income"] - q["Ps"] * q["B"]) / q["income"] for q in qs)
    w_nest = max(abs(q["dn"] * q["pg"] + q["ds"] * q["ps"] - q["prest"]) / q["prest"] for q in qs)
    w_share = max(abs(q["ds"] * q["ps"] / q["prest"] - w) for q, w in zip(qs, F.OMEGA_S))
    # labour to 1e-8: near the ceiling a machine's price moves about a million times as fast as the margin, so the root's
    # last digit in the margin (1e-15) shows as ~1e-9 in labour demand
    check("S3 labour clears (1e-8: the knife edge's amplification of the root's last digit) and income buys every "
          "basket (1e-9), services apart", w_lab < 1e-8 and w_inc < 1e-9, f"labour {w_lab:.1e}, income {w_inc:.1e}")
    check("S4 the nest's unit cost is its goods' cost, and services' share of it is the record's, every year (1e-12)",
          max(w_nest, w_share) < 1e-12, f"cost {w_nest:.1e}, share {w_share:.1e}")
    check("S5 a slower services clock leaves services' task line below nondurables' by 2024",
          qs[-1]["xs"] < qs[-1]["xg"] and abs(qs[0]["xs"] - qs[0]["xg"]) < 1e-12,
          f"1950 {qs[0]['xs']:.3f} / {qs[0]['xg']:.3f}, 2024 {qs[-1]['xs']:.3f} / {qs[-1]['xg']:.3f}")

# ---- the skill split and a worker for each good (her idea and go, 2026-11-08)
F.configure(R0["meta"])
m2 = F.model_path(R0["best"]["par"])
SKILL = dict(R0["meta"], services="skill", pay=None, names=R0["meta"]["names"] + ["g_low", "g_high"],
             extra=["wage_durables", "wage_ndg", "wage_low", "wage_high"])
F.configure(SKILL)
par_k = dict(R0["best"]["par"], g_low=R0["best"]["par"]["g_eta"], g_high=R0["best"]["par"]["g_eta"])
mk = F.model_path(par_k)
worst = max(float(np.max(np.abs(mk[c].values / m2[c].values - 1.0))) for c in cols) if mk is not None else np.inf
check("K1 both services groups on nondurables' clock, one wage: the skill split is the main case (fit_Br0) to 1e-12",
      worst < 1e-12, f"worst relative gap {worst:.1e}")
RS = json.load(open(os.path.join(ROOT, "results", "fit_Bs.json")))
F.configure(RS["meta"])
got = F.durables_years(RS["best"]["par"])
worst = np.inf
if got is not None:
    qs, es_ = got
    eta_s = F.eta_s_path(F.fill(dict(RS["best"]["par"], chi_max=F.pinned_chi(RS["best"]["par"]))))
    q0 = qs[0]
    base = dict(omega_d=F.OMEGA_D_SET, sigma_dg=F.SIGMA_DG_SET, pref_d=q0["pd"], pref_g=q0["pg"], phi=F.VALUE_RENT,
                pref_n=q0["pg"])
    worst = 0.0
    for i, (q, e) in enumerate(zip(qs, es_)):
        w = float(F.OMEGA_S[i])
        if i == 0:
            cmp_k = dict(mode="ref", omega_d=F.OMEGA_D_SET, phi=F.VALUE_RENT, omega_l=0.4 * w, omega_h=0.6 * w)
        else:
            cmp_k = dict(base, pref_l=q0["ps"], pref_h=q0["ps"], omega_l=0.4 * w, omega_h=0.6 * w)
        qk = tg.solve(e, F.eta_d_path(F.fill(dict(RS["best"]["par"], chi_max=F.pinned_chi(RS["best"]["par"]))))[i],
                      cmp_k, (eta_s[i], eta_s[i]))
        worst = max(worst, max(abs(qk[k] / q[k] - 1.0) for k in ("v", "pg", "pd", "c", "participation",
                                                                  "labour_share_bea", "theta_V", "chain_share")),
                    abs(qk["pl"] / q["ps"] - 1.0), abs(qk["ph"] / q["ps"] - 1.0))
check("K2 low- and high-skill services on one services clock, one wage, their shares summing to services': every year of "
      "services apart (fit_Bs) is the skill split's solution (relative 1e-12)", worst < 1e-12, f"{worst:.1e}")
F.configure(dict(SKILL, pay="record"))
saved = {k: v.copy() for k, v in F.PAY_PATHS.items()}
for k in F.PAY_PATHS:
    F.PAY_PATHS[k] = np.ones_like(saved[k])
m_one = F.model_path(par_k)
for k in F.PAY_PATHS:
    F.PAY_PATHS[k] = saved[k]
same = m_one is not None and all(np.array_equal(m_one[c].values, mk[c].values) for c in mk.columns)
check("K3 each good's pay at one is the one-wage split, bit for bit (every column of the path)", same)
got = F.durables_years(par_k)
check("K4a with each good's pay from the record (BLS) the split has an equilibrium every year at the main case's numbers",
      got is not None)
if got is not None:
    qs, es_ = got
    w_lab = max(abs(q["nD"] - q["nS"]) / q["nD"] for q in qs)
    w_inc = max(abs(q["income"] - q["Ps"] * q["B"]) / q["income"] for q in qs)
    w_land = max(abs(q["B"] * q["sb"] + e.b * e.delta * q["K"] - e.T) / e.T for q, e in zip(qs, es_))
    w_nest = max(abs(q["dn"] * q["pg"] + q["dl"] * q["pl"] + q["dh"] * q["ph"] - q["prest"]) / q["prest"] for q in qs)
    w_sh = max(max(abs(q["dl"] * q["pl"] / q["prest"] - F.OMEGA_L[i]), abs(q["dh"] * q["ph"] / q["prest"] - F.OMEGA_H[i]))
               for i, q in enumerate(qs))
    w_pay = 0.0
    for i, q in enumerate(qs):
        hd, hn = q["B"] * q["gb"] * q["dd"] * (1 - q["xd"]), q["B"] * q["gb"] * q["dg"] * q["dn"] * (1 - q["xg"])
        hl, hh = q["B"] * q["gb"] * q["dg"] * q["dl"] * (1 - q["xl"]), q["B"] * q["gb"] * q["dg"] * q["dh"] * (1 - q["xh"])
        pay = q["v"] * (F.PAY_PATHS["r_d"][i] * hd + F.PAY_PATHS["r_n"][i] * hn + F.PAY_PATHS["r_l"][i] * hl
                        + F.PAY_PATHS["r_h"][i] * hh + q["mh"])
        w_pay = max(w_pay, abs(pay / (q["v"] * (q["final_w"] + q["mh"])) - 1.0), abs(hd + hn + hl + hh - q["final"]) / q["final"])
    check("K4b with each good's pay: labour clears (1e-8), income buys every basket (1e-9), land adds up (1e-9), and labour "
          "income is each good's hours at its own pay plus the machine chain's at the production wage (1e-12)",
          w_lab < 1e-8 and w_inc < 1e-9 and w_land < 1e-9 and w_pay < 1e-12,
          f"labour {w_lab:.1e}, income {w_inc:.1e}, land {w_land:.1e}, pay {w_pay:.1e}")
    check("K4c the nest's unit cost is its goods' cost, and the services groups' shares of it are the record's (1e-12)",
          max(w_nest, w_sh) < 1e-12, f"cost {w_nest:.1e}, shares {w_sh:.1e}")
    e24, q24 = es_[-1], qs[-1]
    ed24 = F.eta_d_path(F.fill(dict(par_k, chi_max=F.pinned_chi(par_k))))[-1]
    lo24, hi24 = F.eta_skill_path(F.fill(par_k))
    cmp24 = dict(omega_d=F.OMEGA_D_SET, sigma_dg=F.SIGMA_DG_SET, pref_d=qs[0]["pd"], pref_g=qs[0]["pg"], phi=F.VALUE_RENT,
                 pref_n=qs[0]["pg"], pref_l=qs[0]["pl"], pref_h=qs[0]["ph"], **F.year_cmp(len(qs) - 1))
    qa = tg.solve(e24, ed24, cmp24, (lo24[-1], hi24[-1]))
    qb = tg.solve(e24, ed24, dict(cmp24, r_h=1.2 * cmp24["r_h"]), (lo24[-1], hi24[-1]))
    check("K5 2024 with high-skill pay 20% higher: high-skill services dearer against the production wage, and machines "
          "take more of their tasks", qb["ph"] / qb["v"] > qa["ph"] / qa["v"] and qb["xh"] > qa["xh"],
          f"price over the wage {qa['ph'] / qa['v']:.3f} -> {qb['ph'] / qb['v']:.3f}, task line {qa['xh']:.3f} -> {qb['xh']:.3f}")

# pay at its industries' level with the average held at the production wage (fit_Bkl's setting)
F.configure(dict(SKILL, pay="levels"))
saved = {k: v.copy() for k, v in F.LVL_PATHS.items()}
for k in F.LVL_PATHS:
    F.LVL_PATHS[k] = np.ones_like(saved[k])
m_one = F.model_path(par_k)
for k in F.LVL_PATHS:
    F.LVL_PATHS[k] = saved[k]
same = m_one is not None and all(np.array_equal(m_one[c].values, mk[c].values) for c in mk.columns if c not in ("avg_pay", "kappa"))
RL = json.load(open(os.path.join(ROOT, "results", "fit_Bkl.json")))
F.configure(RL["meta"])
ml = F.model_path(RL["best"]["par"])
dev = float(np.max(np.abs(ml["avg_pay"].values - 1.0))) if ml is not None else np.inf
gap = float(np.max(np.abs(ml["r_h"].values / ml["kappa"].values - F.LVL_PATHS["r_h"]))) if ml is not None else np.inf
check("K6 pay levels at one are the one-wage split bit for bit; at the record's levels (fit_Bkl) the hours-weighted "
      "average pay is the production wage every year (1e-12) and each good's pay is the common factor times its level",
      same and dev < 1e-12 and gap < 1e-12, f"average {dev:.1e}, levels {gap:.1e}; factor 1950 {ml['kappa'].iloc[0]:.3f}, "
      f"2024 {ml['kappa'].iloc[-1]:.3f}")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
