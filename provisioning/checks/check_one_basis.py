# check_one_basis.py — code/one_basis.py and its stored results (data/one_basis.csv).
#   V  the BEA files are the release the lambda thread and paths/chains.py gated (hashes in ../paths/results/chains.json)
#   G  the engine, run here, is the thread's: its narrow machinery series reproduced to 1e-6, every year
#   B  the split of a bundle is chains.py's: its equipment + IPP + structures bundle for 2023 reproduced
#   A  the accounts add up: every bundle's dollar, before and after replacement is traced, in every year, basis and variant
#   R  the stored file is what the script computes (2023 recomputed)
#   P  the account as counted is BEA WP2026-01's, to within the treatment of proprietors
#   Q  the numbers SKETCH.md and the draft quote
# Needs the BEA files in the gitignored cache: run `python3 code/one_basis.py --pull` once on a fresh clone.
# Run from provisioning/:  python3 checks/check_one_basis.py      Exit 0 only if every check passes.
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import one_basis as ob  # noqa: E402

ch = ob.ch
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def prints(value, printed, decimals):
    return abs(value - printed) <= 0.5 * 10.0 ** (-decimals) * 1.05


def rows(pairs):
    return all(prints(v, q, d) for v, q, d in pairs), "; ".join(f"{v:.4f} for {q}" for v, q, d in pairs)


missing = [n for n in ob.FILES if not os.path.exists(os.path.join(ch.CACHE, n))]
if missing:
    sys.exit(f"BLOCKED: {missing} not in {ch.CACHE}; run `python3 code/one_basis.py --pull` first")

stored = pd.read_csv(os.path.join(ROOT, "data", "one_basis.csv"))
vint = json.load(open(os.path.join(ROOT, "data", "one_basis_vintage.json")))
chains = json.load(open(os.path.join(ob.REPO, "paths", "results", "chains.json")))
rec = chains["meta"]["vintage"]
now = ob.vintage()

# ---- V
same = {n: now[n]["sha256_16"] == rec[n]["sha256_16"] for n in ob.FILES if n in rec}
check("V1 the input-output, fixed-asset and GDP-by-industry files are the ones chains.json recorded (the NIPA flat file may be newer)",
      all(v for n, v in same.items() if n != "NipaDataA.txt"), "; ".join(f"{n} {'same' if v else 'DIFFERENT'}" for n, v in same.items()))
check("V2 the stored results were computed on the files now in the cache",
      all(now[n]["sha256_16"] == vint["files"][n]["sha256_16"] for n in ob.FILES))

# ---- G, B, R
tabs = ob.load()
ref = pd.read_csv(os.path.join(ch.LAMBDA, "data", "lambda_us_family_a.csv")).set_index("year")
gate, recon = [], []
for yr in ob.YEARS:
    Y = ch.build_year(tabs["frames"], yr)
    recon.append(Y.recon_err)
    idx, f = ch.weights(Y, ch.SETS["narrow"], Y.FD_thread)
    gate.append(abs(float(Y.v_w @ Y.TR[:, idx] @ f) - float(ref.loc[yr, "lam_narrow_tot"])))
    gate.append(abs(float(Y.v_w @ Y.TRdom[:, idx] @ (Y.phi[idx] * f)) - float(ref.loc[yr, "lam_narrow_domp"])))
check("G1 the thread's narrow machinery series, total and domestic-content, reproduced every year (1e-6)", max(gate) < 1e-6,
      f"largest gap {max(gate):.1e}")
check("G2 the published total requirements are reconstructed within the thread's tolerance every year", max(recon) < ch.RECON_TOL,
      f"largest {max(recon):.1e} against {ch.RECON_TOL:g}")

Y = ch.build_year(tabs["frames"], 2023)
us = ch.parse(tabs["frames"][3].parse("2023", header=None))
ratio, per_out, _ = ch.cfc_ratios(tabs["fa34"], tabs["fa24"], tabs["gdp"], tabs["go"], tabs["nipa"], Y.inds, 2023)
v_cfc = np.array([min(ratio[i], 1.0) * g if i in ratio else per_out[i] for i, g in zip(Y.inds, Y.v_gos)])
fd = us.loc[Y.coms, ch.BUNDLES[ch.BUNDLE_C]].fillna(0.0).sum(axis=1).clip(lower=0.0)
f = (fd / fd.sum()).values
mine_tot, mine_domp = ob.split(Y, f, v_cfc, "tot"), ob.split(Y, f, v_cfc, "domp")
b = chains["bundles"][ch.BUNDLE_C]["2023"]
gaps = [abs(mine_tot["comp"] - b["theta_tot"]), abs(mine_domp["comp"] - b["theta_domp"]), abs(mine_tot["tax"] - b["tax_tot"]),
        abs(sum(mine_tot["worn"].values()) - b["cfc_tot"]), abs(mine_tot["nos"] - b["nos_tot"]),
        abs(mine_domp["imports"] - b["imports_domp"])]
check("B1 chains.json's investment bundle for 2023 (pay on both bases, taxes, wear, net surplus, imports) reproduced (1e-4: "
      "government enterprises' wear reads the newer NIPA file)", max(gaps) < 1e-4, f"largest gap {max(gaps):.1e}")

again = pd.DataFrame(ob.year_rows(tabs, 2023))
old = stored[stored.year == 2023].reset_index(drop=True)
num = [c for c in old.columns if old[c].dtype.kind == "f"]
gap = float(np.max(np.abs(again[num].values - old[num].values)))
check("R1 the stored 2023 rows are what the script computes (1e-12)", gap < 1e-12, f"{gap:.1e}")

# ---- A
check("A1 every consumption dollar adds to one, before and after replacement is traced (1e-6)",
      max((stored.gross_sum - 1).abs().max(), (stored.net_sum - 1).abs().max()) < 1e-6,
      f"{(stored.gross_sum - 1).abs().max():.1e}, {(stored.net_sum - 1).abs().max():.1e}")
s = stored
whole = max(float((s[k] - (s.shelter_share * s["shelter_" + k] + (1 - s.shelter_share) * s["rest_" + k])).abs().max())
            for k in ("comp", "nos", "tax", "imports"))
check("A2 shelter and the rest of consumption, weighted, are the whole (1e-9)", whole < 1e-9, f"{whole:.1e}")

# ---- P
c = stored[(stored.basis == "domp") & (stored.depreciation == "central")].set_index("year")
pub, fin = ob.published(), ob.financing()
d = (c.labour_gross_psi38 - pub.human_effort_share)
check("P1 labour as counted (wear not traced, proprietors' labour 0.38) is within 0.025 of BEA WP2026-01's human effort every year",
      d.abs().max() < 0.025, f"mean {d.mean():+.3f}, largest {d.abs().max():.3f}")
check("P2 imported content is within 0.02 of BEA WP2026-01's foreign content every year",
      (c.gross_imports - pub.foreign_content_share).abs().max() < 0.02, f"largest {(c.gross_imports - pub.foreign_content_share).abs().max():.3f}")

# ---- Q
r = c.loc[2023]
wear = r.worn_housing + r.worn_public + r.worn_business
check("Q1 the 2023 consumption dollar as counted: pay 0.425, wear 0.142, net surplus 0.270, taxes 0.072, imports 0.091",
      *rows([(r.gross_comp, 0.425, 3), (wear, 0.142, 3), (r.gross_nos, 0.270, 3), (r.gross_tax, 0.072, 3), (r.gross_imports, 0.091, 3)]))
check("Q2 with wear traced back: pay 0.500, net surplus 0.305, taxes 0.078, imports 0.117; with proprietors' labour, labour 0.530 "
      "and capital and land 0.275", *rows([(r.comp, 0.500, 3), (r.nos, 0.305, 3), (r.tax, 0.078, 3), (r.imports, 0.117, 3),
                                           (r.labour_dollar_psi38, 0.530, 3), (r.comp + r.nos - r.labour_dollar_psi38, 0.275, 3)]))
t = stored[(stored.basis == "tot") & (stored.depreciation == "central")].set_index("year")
e = stored[(stored.basis == "domp") & (stored.depreciation == "economywide")].set_index("year")
check("Q3 labour's share of the net domestic factor cost of consumption, 2023: 0.658 (0.621 to 0.687 across proprietors' labour; "
      "0.664 with imports priced as made at home; 0.676 with the economy-wide depreciation ratio)",
      *rows([(r.labour_factor_psi38, 0.658, 3), (r.labour_factor_psi00, 0.621, 3), (r.labour_factor_psi67, 0.687, 3),
             (t.loc[2023, "labour_factor_psi38"], 0.664, 3), (e.loc[2023, "labour_factor_psi38"], 0.676, 3)]))
both = pd.DataFrame({"made": c.labour_factor_psi38, "fin": fin.fin_labour, "beyond": fin.fin_beyond_income,
                     "wp": pub.human_effort_share}).dropna()
gapmf = both.made - both.fin
check("Q4 made less financed, 2004-2023: zero on average (0.000), between -0.025 and +0.020, 0.010 in absolute value on average",
      *rows([(gapmf.mean(), 0.000, 3), (gapmf.min(), -0.025, 3), (gapmf.max(), 0.020, 3), (gapmf.abs().mean(), 0.010, 3)]))
cur = both.fin / (1 - both.beyond) - both.made
check("Q5 of spending paid from current income labour finances more than it makes: 0.072 on average (0.058 to 0.088); 0.736 "
      "against 0.658 in 2023", *rows([(cur.mean(), 0.072, 3), (cur.min(), 0.058, 3), (cur.max(), 0.088, 3),
                                      (both.fin[2023] / (1 - both.beyond[2023]), 0.736, 3)]))
check("Q6 the paper's gap, financed less BEA's human effort: 0.211 on average, 0.186 in 2023; from BEA's 0.472 to 0.658 in "
      "three steps: -0.021 (this engine), +0.079 (wear traced), +0.128 (taxes and imports set aside)",
      *rows([((both.fin - both.wp).mean(), 0.211, 3), (both.fin[2023] - both.wp[2023], 0.186, 3),
             (r.labour_gross_psi38 - pub.human_effort_share[2023], -0.021, 3), (r.labour_dollar_psi38 - r.labour_gross_psi38, 0.079, 3),
             (r.labour_factor_psi38 - r.labour_dollar_psi38, 0.128, 3)]))
check("Q7 since 1997: labour's share of net factor cost 0.683, a peak of 0.713 in 2001, 0.658 in 2023",
      *rows([(c.labour_factor_psi38[1997], 0.683, 3), (c.labour_factor_psi38.max(), 0.713, 3), (float(c.labour_factor_psi38.idxmax()), 2001, 0)]))
check("Q8 shelter is 0.154 of the consumption dollar and labour is 0.232 of its factor cost; the rest of consumption 0.740; "
      "replacing a dollar of wear pays labour 0.53", *rows([(r.shelter_share, 0.154, 3), (r.shelter_labour_factor, 0.232, 3),
                                                            (r.rest_labour_factor_psi38, 0.740, 3), ((r.comp - r.gross_comp) / wear, 0.53, 2)]))

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
