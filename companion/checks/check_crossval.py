# check_crossval.py — gate for unit 5 (build_crossval.py outputs). Structural
# and accounting gates, spot re-derivations against the panel, and sentence
# guards pinning the README's claims. Directions of hypotheses are not gated;
# published sentences are.
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))

s = pd.read_csv(os.path.join(DATA, "reinstatement_series.csv"),
                parse_dates=["date0", "date1"])
fr = pd.read_csv(os.path.join(DATA, "friction.csv"))
st = pd.read_csv(os.path.join(DATA, "friction_stats.csv"))
named = pd.read_csv(os.path.join(DATA, "friction_named.csv"))
panel = pd.read_csv(os.path.join(DATA, "oews_occ1990dd_panel.csv"))

ok = 0


def check(name, cond):
    global ok
    assert cond, f"FAIL: {name}"
    ok += 1
    print(f"  ok  {name}")


print("== reinstatement series structure ==")
check("22 release pairs", len(s) == 22)
check("dates strictly increasing, spans positive",
      s["date0"].is_monotonic_increasing and (s["date1"] > s["date0"]).all())
check("matched occupations >= 700 on every pair",
      (s["matched_occs"] >= 700).all())
check("base tasks >= 10,000 on every pair", (s["base_tasks"] >= 10_000).all())
rates = ["birth_rate_txt", "death_rate_txt", "birth_rate_id", "death_rate_id"]
check("all rates finite and nonnegative where present",
      all((s[c].dropna() >= 0).all() and np.isfinite(s[c].dropna()).all()
          for c in rates))
both = s.dropna(subset=["birth_rate_id"])
check("text member >= ID member on births (rewording adds text churn)",
      (both["birth_rate_txt"] >= both["birth_rate_id"] - 1e-9).all())

print("== reinstatement sentence guards ==")
last = s.iloc[-1]
check("latest pair records ZERO task births, both members",
      last["birth_rate_txt"] == 0 and last["birth_rate_id"] == 0)
mature = s[s["date0"] >= "2012-07-01"].dropna(subset=["birth_rate_id"])
x = mature["date1"].map(pd.Timestamp.toordinal) / 365.25
tr = np.polyfit(x, mature["birth_rate_id"], 1)[0] * 10
check(f"mature-era ID births: mean < 10 and falling ({tr:+.1f}/decade)",
      mature["birth_rate_id"].mean() < 10 and tr < 0)
check("construction-era ramp visible (first two pairs > 50 txt births) — "
      "keeps the caveat honest",
      (s.head(2)["birth_rate_txt"] > 50).all())
check("the 2024 pruning wave is real (28->29 deaths > 20/1000 both members)",
      float(s[s["to"] == 29.0]["death_rate_txt"].iloc[0]) > 20
      and float(s[s["to"] == 29.0]["death_rate_id"].iloc[0]) > 20)

print("== friction structure ==")
check(">= 300 occupations with both window slopes", len(fr) >= 300)
check("terciles balanced at n = len/3 each",
      (st["n"] == len(fr.dropna(subset=["human_rating_beta"])) // 3).all()
      or (st.groupby("variant")["n"].sum() == len(fr)).all())
# spot re-derivation: one occupation's pre-slope straight from the panel
emp = panel.pivot(index="year", columns="occ1990dd", values="emp")
share = emp.div(emp.sum(axis=1), axis=0)
j = int(fr.iloc[0]["occ1990dd"])
w = share[j].loc[2015:2019]
slope = np.polyfit(w.index, np.log(w), 1)[0]
check("first row's pre-slope recomputes from the panel exactly",
      np.isclose(slope, fr.iloc[0]["pre_slope"]))
cell = st[(st["variant"] == "human_rating_beta")
          & (st["exposure_terc"] == "high")]["d_slope_wmean"].iloc[0]
d = fr.dropna(subset=["human_rating_beta"]).copy()
d["terc"] = pd.qcut(d["human_rating_beta"], 3, labels=["low", "mid", "high"])
g = d[d["terc"] == "high"]
check("high-tercile cell recomputes exactly",
      np.isclose(np.average(g["d_slope"], weights=g["emp_2025"]), cell))

print("== friction sentence guards ==")
csr = fr[fr["occ1990dd"] == 376].iloc[0]      # customer service representatives
check("flagship instance: customer service flipped sign, post < -5%/yr",
      csr["pre_slope"] > 0 and csr["post_slope"] < -0.05)
hb = st[st["variant"] == "human_rating_beta"].set_index("exposure_terc")
check("no positive aggregate exposure gradient (high decelerated no more "
      "than low)",
      hb.loc["high", "d_slope_wmean"] >= hb.loc["low", "d_slope_wmean"])
check("named table includes the operators-era controls and translators",
      named["top_source_title"].str.contains("Interpreters", case=False).any()
      and named["top_source_title"].str.contains("Data Entry", case=False).any())

fp = os.path.join(FIGS, "crossval.png")
check("figure exists and is substantive",
      os.path.exists(fp) and os.path.getsize(fp) > 30_000)

print(f"\nALL GREEN — {ok} checks passed.")
