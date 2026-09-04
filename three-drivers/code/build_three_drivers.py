# build_three_drivers.py — back-of-the-napkin: where each of the three drivers points, by sector.
#
#   driver 1  MARKET PULL   = share of the 2024 US wage bill (QCEW, all ownerships).
#                             Wages are the market's signal of where it wants people NOW.
#   driver 2  CRISIS VALUE  = how often the sector appears in the seven standing risk /
#                             essential-service lists (data/risk_lists.csv; sector_map is our
#                             judgment; cross_cutting items excluded).
#   driver 3  PEOPLE PULL   = share of bachelor's degrees conferred by field (NCES 322.10,
#                             2021-22), mapped to sectors with fractional weights (judgment;
#                             unmapped share reported, not hidden).
#
# All classification judgments live in this file, in the open. Napkin quality: the point is
# the pattern (which corners of the grid are crowded/empty), not any single number.
#
# Known undercounts, stated: QCEW excludes active-duty military (~1.3M) and most self-employed
# farmers (UI coverage) — defense_public_safety and food_agriculture market pull are lower
# bounds; the direction strengthens the napkin's contrast rather than creating it.

import pandas as pd

# ---------------------------------------------------------------- QCEW wage bills (2024, US000)
q = pd.read_csv("data/raw/qcew_2024_us000.csv",
                dtype={"industry_code": str, "own_code": str, "agglvl_code": str})
q = q[q.own_code.isin(["1", "2", "3", "5"])]  # federal, state, local, private; sums to total covered

def wages_emp(code):
    sub = q[q.industry_code == code]
    return sub.total_annual_wages.sum(), sub.annual_avg_emplvl.sum()

# sector := [(industry_code, +1/-1), ...] — a signed composition over NAICS pieces
QCEW_MAP = {
    "food_agriculture":      [("11", 1), ("311", 1)],                      # farms + food manufacturing
    "energy":                [("21", 1), ("22", 1), ("2213", -1)],         # mining/oil/gas + utilities − water
    "water":                 [("2213", 1)],                                # water, sewage, related systems
    "health_social_care":    [("62", 1)],
    "transport_logistics":   [("48-49", 1)],
    "communications_it":     [("513", 1), ("5131", -1), ("517", 1), ("518", 1), ("519", 1), ("5415", 1)],
    "finance_insurance":     [("52", 1)],
    "construction_housing":  [("23", 1), ("53", 1)],                       # construction + real estate
    "manufacturing":         [("31-33", 1), ("311", -1)],
    "defense_public_safety": [("922", 1), ("928", 1)],                     # justice/public order + natsec
    "education_research":    [("61", 1), ("5417", 1)],                     # education + scientific R&D
    "media_arts_culture":    [("512", 1), ("516", 1), ("5131", 1), ("71", 1)],
    "government_admin":      [("92", 1), ("922", -1), ("928", -1)],
    "professional_business": [("54", 1), ("5415", -1), ("5417", -1), ("55", 1), ("56", 1)],
    "retail_leisure":        [("42", 1), ("44-45", 1), ("72", 1), ("81", 1)],
}

market = {}
for sector, parts in QCEW_MAP.items():
    w = e = 0.0
    for code, sign in parts:
        wi, ei = wages_emp(code)
        w += sign * wi
        e += sign * ei
    market[sector] = dict(wagebill_usd=w, employment=e)
m = pd.DataFrame(market).T

total_w = q[q.agglvl_code == "11"].total_annual_wages.sum()
total_e = q[q.agglvl_code == "11"].annual_avg_emplvl.sum()
cover_w = m.wagebill_usd.sum() / total_w
print(f"QCEW 2024: total covered wages ${total_w/1e12:.2f}T, employment {total_e/1e6:.1f}M; "
      f"sector map covers {cover_w:.1%} of wages (gap = undisclosed cells / unclassified)")
m["wagebill_share"] = m.wagebill_usd / total_w
m["emp_share"] = m.employment / total_e

# ---------------------------------------------------------------- crisis-list tally
r = pd.read_csv("data/risk_lists.csv")
r = r[r.sector_map != "cross_cutting"]
long = r.assign(sector=r.sector_map.str.split(";")).explode("sector")
long = long[long.sector != "cross_cutting"]
crisis = long.groupby("sector").agg(crisis_items=("item", "count"),
                                    crisis_sources=("source", "nunique"))

# ---------------------------------------------------------------- NCES 322.10 degrees by field
x = pd.read_excel("data/raw/nces_322_10.xlsx", header=None)
year_row = 1
last_col = x.shape[1] - 1
year_label = str(x.iloc[year_row, last_col]).strip()
import re
fields = {}
for i in range(3, len(x)):
    lab = str(x.iloc[i, 0]).strip()
    v = pd.to_numeric(x.iloc[i, last_col], errors="coerce")
    if lab != "nan" and pd.notna(v):
        lab = re.sub(r"\\\d+\\", "", lab)          # strip footnote markers like \1\
        lab = re.sub(r"\s+", " ", lab).strip(" .")  # collapse embedded newlines/indents
        fields[lab] = float(v)
total_deg = fields.pop("Total")

def find(prefix):
    exact = [k for k in fields if k.lower() == prefix.lower()]
    if exact:
        return exact[0]
    hits = [k for k in fields if k.lower().startswith(prefix.lower())]
    assert len(hits) == 1, f"field lookup '{prefix}' -> {hits}"
    return hits[0]

# field-prefix -> {sector: weight}; weights sum to 1; "unmapped" is an explicit bucket
DEGREE_MAP = {
    "Agriculture and natural resources": {"food_agriculture": 1.0},
    "Architecture": {"construction_housing": 1.0},
    "Area, ethnic": {"unmapped": 1.0},
    "Biological and biomedical": {"health_social_care": 0.5, "education_research": 0.5},
    "Business": {"professional_business": 0.6, "finance_insurance": 0.4},
    "Communication, journalism": {"media_arts_culture": 1.0},
    "Communications technologies": {"communications_it": 1.0},
    "Computer and information sciences": {"communications_it": 1.0},
    "Education": {"education_research": 1.0},
    # per table footnote 3: includes construction trades and mechanic/repair technologies
    "Engineering technologies": {"manufacturing": 0.6, "construction_housing": 0.2, "transport_logistics": 0.2},
    "Engineering": {"manufacturing": 0.4, "energy": 0.2, "construction_housing": 0.2, "communications_it": 0.2},
    "English language": {"unmapped": 1.0},
    "Family and consumer sciences": {"unmapped": 1.0},
    "Foreign languages": {"unmapped": 1.0},
    "Health professions": {"health_social_care": 1.0},
    "Homeland security": {"defense_public_safety": 1.0},
    "Legal professions": {"professional_business": 0.5, "government_admin": 0.5},
    "Liberal arts": {"unmapped": 1.0},
    "Library science": {"education_research": 1.0},
    "Mathematics and statistics": {"education_research": 0.5, "finance_insurance": 0.25, "communications_it": 0.25},
    "Military technologies": {"defense_public_safety": 1.0},
    "Multi/interdisciplinary": {"unmapped": 1.0},
    "Parks, recreation": {"retail_leisure": 1.0},
    "Philosophy and religious": {"unmapped": 1.0},
    "Physical sciences": {"education_research": 0.6, "energy": 0.4},
    "Precision production": {"manufacturing": 1.0},
    "Psychology": {"health_social_care": 1.0},
    "Public administration": {"government_admin": 0.5, "health_social_care": 0.5},
    "Social sciences and history": {"unmapped": 1.0},
    "Theology": {"unmapped": 1.0},
    "Transportation and materials moving": {"transport_logistics": 1.0},
    "Visual and performing arts": {"media_arts_culture": 1.0},
    "Other and not classified": {"unmapped": 1.0},
}

deg = {s: 0.0 for s in list(QCEW_MAP) + ["unmapped"]}
assigned = 0.0
for prefix, wmap in DEGREE_MAP.items():
    n = fields[find(prefix)]
    assigned += n
    for sector, wgt in wmap.items():
        deg[sector] += n * wgt
assert abs(assigned - total_deg) / total_deg < 0.01, \
    f"degree fields sum {assigned:,.0f} vs total {total_deg:,.0f}"
degrees = pd.Series(deg, name="degrees")
unmapped_share = degrees["unmapped"] / total_deg
print(f"NCES 322.10 ({year_label}): {total_deg:,.0f} bachelor's degrees; "
      f"{unmapped_share:.1%} in fields we do not force onto a sector")

# ---------------------------------------------------------------- assemble
out = m.join(crisis).fillna({"crisis_items": 0, "crisis_sources": 0})
out["degrees"] = degrees
out["degrees_share"] = out.degrees / total_deg
out = out[["wagebill_usd", "wagebill_share", "employment", "emp_share",
           "crisis_sources", "crisis_items", "degrees", "degrees_share"]]
out.index.name = "sector"
out = out.sort_values("crisis_sources", ascending=False)
out.to_csv("data/three_drivers.csv")
print(f"\nwrote data/three_drivers.csv ({year_label} degrees; 2024 wages; 2024-26 lists)\n")
disp = out.copy()
disp["wagebill_share"] = (disp.wagebill_share * 100).round(1)
disp["emp_share"] = (disp.emp_share * 100).round(1)
disp["degrees_share"] = (disp.degrees_share * 100).round(1)
disp["employment"] = (disp.employment / 1e6).round(2)
print(disp[["wagebill_share", "emp_share", "degrees_share",
            "crisis_sources", "crisis_items"]].to_string())
