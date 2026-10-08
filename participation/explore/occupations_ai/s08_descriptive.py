# s08_descriptive.py - descriptive numbers quoted in findings.md (no tests): the 2011-19 drift of the young's relative
# clerical share, and the pace of the clerical-share decline at 25-64 before 2020 and after 2022.
import sys, json
sys.path.insert(0, "explore")
import data
import numpy as np, pandas as pd
es = data.es
raw = data.manifest_raw(); occ = es.clean(raw["occ"])
w = occ.pivot_table(index=["geo", "year"], columns=["age", "isco08"], values="value")
yg, al = w["Y15-24"], w["Y15-64"]; pr = al - yg
R = np.log((yg["OC4"] / yg["TOTAL"]) / (pr["OC4"] / pr["TOTAL"])).unstack("geo")
dR = R.loc[2017:2019].mean() - R.loc[2011:2013].mean()
s4p = (pr["OC4"] / pr["TOTAL"] * 100).unstack("geo"); s4y = (yg["OC4"] / yg["TOTAL"] * 100).unstack("geo")
pre = (s4p.loc[2019] - s4p.loc[2016]) / 3; post = (s4p.loc[2025] - s4p.loc[2022]) / 3
prey = (s4y.loc[2019] - s4y.loc[2016]) / 3; posty = (s4y.loc[2025] - s4y.loc[2022]) / 3
covid = s4p.loc[2022] - s4p.loc[2019]
out = pd.DataFrame({"dR_OC4_1719_vs_1113": dR, "OC4_2564_pp_per_yr_2016_19": pre, "OC4_2564_pp_per_yr_2022_25": post,
                    "OC4_1524_pp_per_yr_2016_19": prey, "OC4_1524_pp_per_yr_2022_25": posty, "OC4_2564_2019_to_2022": covid})
print(out.round(3).to_string()); print(out.mean().round(3).to_string()); print("n positive dR:", int((dR > 0).sum()), "of", dR.notna().sum())
out.to_csv("explore/occupations_ai/descriptive_clerical_pace.csv")
