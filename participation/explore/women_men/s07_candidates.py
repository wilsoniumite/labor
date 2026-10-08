# s07_candidates.py — stress tests of the candidate E-hypotheses, manifest data only (M).
# E-a: women's prime-age participation responds to q less where outright owners dominate (q x owner share, with
#      country trends; varies P C-3).
# E-b: the gap W-M 25-54 is countercyclical (U 25-54 from lfsa_urgan, one source for all countries).
# Also: the floor kink by sex (D1 on women and men 25-34 separately), for understanding.
# Out: s07_candidates.txt
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402

df = cm.panel()
cl = cm.data.panel()[1]
out = []


def say(s):
    out.append(str(s))
    print(s)


def zs(s):
    return (s - s.mean()) / s.std(ddof=0)


geo = df.index.get_level_values(0)
O = zs(cl["owner_outright_5564"])
F = zs(cl["F_raw"])
df["QxO"] = df["logq_l1"].to_numpy() * geo.map(O).to_numpy(float)
df["QxF"] = df["logq_l1"].to_numpy() * geo.map(F).to_numpy(float)


def run(*a, **k):
    r = cm.reg(df, *a, **k)
    say(cm.fmt(r))
    return r


say("== E-a robustness (q x outright owners 55-64, sd units; H1 < 0)")
base = dict(side=-1, trends=True)
ra = run("AW2554", ["QxO", "logq_l1"], ["U_lfs"], label="E-a base: AW2554, U_lfs, trends, 1997-2025", **base)
run("AW2554", ["QxO", "logq_l1"], ["U"], label="E-a frozen U (une_rt_a), trends", **base)
run("AW2554", ["QxO", "logq_l1"], [], label="E-a no cycle control, trends", **base)
run("AW2554", ["QxO", "logq_l1"], ["U_lfs"], years=(2005, 2025), label="E-a 2005-2025", **base)
run([(1, "AW2554"), (-1, "AM2554")], ["QxO", "logq_l1"], ["U_lfs"], label="E-a on gap W-M", **base)
run("AM2554", ["QxO", "logq_l1"], ["U_lfs"], label="E-a on men (placebo-ish)", **base)
run("AW2554_all", ["QxO", "logq_l1"], ["U_lfs"], label="E-a all residents", **base)
# implied slopes at the 10th/90th percentile of O
for pct in (10, 90):
    o = float(np.percentile(O.dropna(), pct))
    dd = df.copy()
    dd["Qshift"] = dd["logq_l1"] + o * 0  # placeholder for clarity
    dd["QxO_c"] = dd["logq_l1"].to_numpy() * (geo.map(O).to_numpy(float) - o)
    r = cm.reg(dd, "AW2554", ["logq_l1", "QxO_c"], ["U_lfs"], side=0, trends=True,
               label=f"E-a implied slope of q at O pct {pct} (z={o:.2f})")
    say(cm.fmt(r))
# leave one country out
say("leave-one-out, E-a base:")
lo = {}
for g in cm.GEOS:
    r = cm.reg(df, "AW2554", ["QxO", "logq_l1"], ["U_lfs"], geos=[x for x in cm.GEOS if x != g], B=1999,
               label=f"E-a LOO -{g}", **base)
    lo[g] = (round(r["beta"], 2), round(r["p"], 3))
say(lo)

say("\n== E-b robustness (gap W-M on U 25-54; H1 > 0)")
rb = run([(1, "AW2554"), (-1, "AM2554")], "U2554_lfs", side=+1, label="E-b base: W-M on U2554_lfs, 1997-2025")
run([(1, "AW2554"), (-1, "AM2554")], "U2554", side=+1, label="E-b frozen U2554 (une_rt_a)")
run([(1, "AW2554"), (-1, "AM2554")], "U2554_lfs", side=+1, trends=True, label="E-b country trends")
run([(1, "AW2554"), (-1, "AM2554")], "U_lfs", side=+1, label="E-b U 25-74")
run([(1, "AW2554_all"), (-1, "AM2554_all")], "U2554_lfs", side=+1, label="E-b all residents")
say("leave-one-out, E-b base:")
lo = {}
for g in cm.GEOS:
    r = cm.reg(df, [(1, "AW2554"), (-1, "AM2554")], "U2554_lfs", side=+1, geos=[x for x in cm.GEOS if x != g],
               B=1999, label=f"E-b LOO -{g}")
    lo[g] = (round(r["beta"], 3), round(r["p"], 3))
say(lo)

say("\n== floor kink by sex (D1 form: A 25-34 on q, q x F, U; H1 b2 < 0), understanding")
run("AF2534", ["QxF", "logq_l1"], ["U"], side=-1, label="D1 women 25-34 (frozen U)")
run("AM2534", ["QxF", "logq_l1"], ["U"], side=-1, label="D1 men 25-34 (frozen U)")
run("AF2534", ["QxF", "logq_l1"], ["U_lfs"], side=-1, label="D1 women 25-34 (U_lfs, 1997-2025)")
run("AM2534", ["QxF", "logq_l1"], ["U_lfs"], side=-1, label="D1 men 25-34 (U_lfs, 1997-2025)")
open(os.path.join(cm.HERE, "s07_candidates.txt"), "w").write("\n".join(out) + "\n")
