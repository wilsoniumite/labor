# s09_results.py — writes results/explore_women_men.json from the committed-to-be outputs (re-estimates the two
# candidates once more with B = 9999; these reruns are not new specifications).
from __future__ import annotations
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402
df = cm.panel(); cl = cm.data.panel()[1]
O = cl["owner_outright_5564"]; O = (O - O.mean()) / O.std(ddof=0)
df["QxO"] = df["logq_l1"].to_numpy() * df.index.get_level_values(0).map(O).to_numpy(float)
a = cm.inf.wcr  # noqa
ra = cm.reg(df, "AW2554", ["QxO", "logq_l1"], ["U_lfs"], side=-1, trends=True, label="WM-1 final rerun")
rb = cm.reg(df, [(1, "AW2554"), (-1, "AM2554")], "U2554_lfs", side=+1, label="WM-2 final rerun")
with open(cm.COUNTER, "a") as f:
    f.write("-2\treruns of the two candidates for the results file (not new specifications)\n")
def keep(r):
    return {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in r.items()
            if k in ("beta", "se", "t", "p", "p_opposite", "n", "G", "G_star", "mde", "years")}
res = {"theme": "women_men", "half": "explore", "geos": cm.GEOS,
       "specifications_estimated": 61, "loo_reruns": 32,
       "candidates": {
           "WM-1": dict(keep(ra), mde_15=cm.inf.mde(ra["se"] * math.sqrt(16 / 15), 15), side=-1,
                        outcome="AW2554", regressor="logq_l1 x z(OWN_NL 55-64, 2015-2017 mean)",
                        controls="logq_l1, U 25-74 (lfsa_urgan), country+year FE, country linear trends, C3 breaks",
                        varies_P="C-3 (leg 2)", variants_tried=21),
           "WM-2": dict(keep(rb), mde_15=cm.inf.mde(rb["se"] * math.sqrt(16 / 15), 15), side=1,
                        outcome="AW2554 - AM2554", regressor="U 25-54 (lfsa_urgan, sex T)",
                        controls="country+year FE, C3 breaks", varies_P="none", variants_tried=11)}}
os.makedirs(os.path.join(cm.ROOT, "results"), exist_ok=True)
json.dump(res, open(os.path.join(cm.ROOT, "results", "explore_women_men.json"), "w"), indent=1)
print(json.dumps(res["candidates"], indent=1))
