# build_majors_match.py — "do graduates work in the field they majored in?", two primary sources.
#
# Source A: NSF NCSES, National Survey of College Graduates 2023, Table 1-3
#   "Relationship of highest degree to job among employed college graduates, by level of highest
#    degree, minor field of highest degree, and broad occupation: 2023" (nsf25322-tab001-003.xlsx,
#   vendored in data/raw/). Self-reported: job closely / somewhat / not related to highest degree.
# Source B: NY Fed, The Labor Market for Recent College Graduates — outcomes by major
#   (college-labor-outcomes-by-major-data.csv, vendored). Underemployment = share of employed
#   graduates in jobs not typically requiring a college degree (their O*NET-based definition);
#   NOT the same object as NSCG relatedness — a degree-requiring job can be outside your field.
#
# Outputs: data/majors_match_nscg.csv (by field, all-degree-levels panel + level panel heads),
#          data/majors_match_nyfed.csv (by major, rates as fractions).

import pandas as pd

# ---------------------------------------------------------------- NSCG table 1-3
x = pd.read_excel("data/raw/nscg23_tab1-3.xlsx", header=None)

# Row map established by inspection (see DATA_NOTES): panels start at fixed rows.
PANELS = {"All degrees": (5, 44), "Bachelor's": (45, 84), "Master's": (85, 124),
          "Doctorate": (125, 164), "Professional": (165, 168)}
COLS = {"total": 1, "closely": 2, "somewhat": 3, "not_related": 4}

rows = []
for panel, (r0, r1) in PANELS.items():
    for i in range(r0, r1 + 1):
        label = str(x.iloc[i, 0])
        if label == "nan":
            continue
        rec = {"degree_level": panel, "field": label.strip(),
               "is_panel_total": i == r0}
        for k, c in COLS.items():
            rec[k] = pd.to_numeric(x.iloc[i, c], errors="coerce")  # NCSES 'S' = suppressed -> NaN
        rows.append(rec)
nscg = pd.DataFrame(rows)
for k in ["closely", "somewhat", "not_related"]:
    nscg["share_" + k] = nscg[k] / nscg["total"]
nscg.to_csv("data/majors_match_nscg.csv", index=False)

t = nscg[(nscg.degree_level == "All degrees") & (nscg.field == "All degrees")].iloc[0]
assert abs(t.closely + t.somewhat + t.not_related - t.total) / t.total < 0.005, "components must sum"
print(f"NSCG 2023, all employed college graduates: {t.total/1e6:.1f}M")
print(f"  job closely related to degree : {t.share_closely:.1%}")
print(f"  somewhat related              : {t.share_somewhat:.1%}")
print(f"  not related                   : {t.share_not_related:.1%}")

ba = nscg[(nscg.degree_level == "Bachelor's") & (nscg.field == "Bachelor's")].iloc[0]
print(f"Bachelor's-highest only: closely {ba.share_closely:.1%}, somewhat {ba.share_somewhat:.1%}, "
      f"not related {ba.share_not_related:.1%}")

# ---------------------------------------------------------------- NY Fed outcomes by major
ny = pd.read_csv("data/raw/nyfed_outcomes_by_major.csv")
ny.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in ny.columns]
for c in ["unemployment_rate", "underemployment_rate", "share_with_graduate_degree"]:
    ny[c] = ny[c] / 100.0
ny = ny.sort_values("underemployment_rate", ascending=False).reset_index(drop=True)
ny.to_csv("data/majors_match_nyfed.csv", index=False)

print(f"\nNY Fed outcomes by major: {len(ny)} majors")
print(f"  median underemployment across majors: {ny.underemployment_rate.median():.1%}")
print("  five most underemployed majors:")
print(ny.head(5)[["major", "underemployment_rate"]].to_string(index=False))
print("  five least underemployed majors:")
print(ny.tail(5)[["major", "underemployment_rate"]].to_string(index=False))
print("  agriculture row:")
print(ny[ny.major.str.contains("Agri", case=False)][["major", "underemployment_rate",
      "median_wage_early_career"]].to_string(index=False))
