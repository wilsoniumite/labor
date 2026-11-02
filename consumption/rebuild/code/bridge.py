# bridge.py - the 2026-06-14 post's VAT-bridge consumption machinery, rebuilt from its text and published numbers
# (consumption/rebuild; the post's own code was never committed anywhere we can reach).
#
# The post's method, as it states it (Figures 1-6, footnotes 23, 26, 27):
#   accounting   net_d = tau * (Cbar_v - C_v,d)                    per payment share (adult 1, child 0.3)
#   demand       dPct_g = sum_d theta_dg * eta_gd * shock_d,        shock_d = mpc_d * net_d / C_d
#                dUSD_g = dPct_g * Cbar_g
#   theta_dg     decile d's share of all spending on category g
#   eta_gd       Working model, eta = 1 + beta_k / w_kd (TB-1929 eq. 5) at OBSERVED decile budget shares w_kd
#                of the USDA group k holding g; food categories via the stage-two conditional betas (eq. 11):
#                eta = eta_F * (1 + beta*_s / w*_s), w*_s = observed within-food share
#   mpc_d        "literature schedule": 1.0 in the bottom deciles falling to 0.40-0.65 at the top
#
# Generic on purpose: shifts_from_transfers() takes ANY per-share net-transfer vector by income group (and an
# MPC vector, or a precomputed budget shock dC_d/C_d) and returns category shifts, so an LVT-funded dividend
# (consumption/lvt) runs through exactly the machinery the gate checks. Works for any CE year 2014-2025 and for
# the quintile table (Table 1101) as well as deciles (Table 1110): the group columns are read from the table.
# Finland (HBS 2022 quintiles, Figures 1-3): the FINLAND section at the end (build_fi_model, fi_vat_accounting,
# fi_mpc_schedules); its model dicts plug into the same generic tier-2 functions. Calibration: run_fi.py, NOTES_fi.md.
#
# Plain functions plus constants, no classes, so pieces paste into a notebook cell. A "model" is a plain dict.
# Units throughout: dollars per payment share per month unless a name says otherwise.
# Judgment inputs (VAT flags, group mapping, food split, MPC shape) live in the constants below; how each was
# chosen, and which published numbers pinned it, is derived again in run_us.py and written up in NOTES_us.md.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # consumption/rebuild/code
sys.path.insert(0, str(HERE))

import numpy as np
import pandas as pd

REBUILD = HERE.parent                                     # consumption/rebuild
THREAD = REBUILD.parent                                   # consumption
TIDY = THREAD / "data" / "tidy"
RAW = THREAD / "data" / "raw"

TAU = 0.15                     # surcharge on the VAT-able base (post: "fifteen points")
ADULT_W, CHILD_W = 1.0, 0.3    # payment shares (post: "each adult one share, each child 0.3")
EXP = "Average annual expenditures"
CHAR = "Consumer unit characteristics:"
NCU = "Number of consumer units (in thousands)"
PEOPLE = CHAR + " > Average number in consumer unit: > People"
CHILDREN = CHAR + " > Average number in consumer unit: > Children under 18"

# %% the category list: the 36 bars of Fig 5, the three off-chart budget rows, and one residual
# cat: Fig 5 label exactly as printed. ce: alternative paths below 'Average annual expenditures' (first hit wins;
# labels change across years). residual: (parent, [children]) used when no ce path exists (Other vehicles was
# dropped from Table 1110 in 2024, so it is parent minus new minus used). role: chart = a Fig 5 bar, offchart =
# in the budget totals but not drawn (post: "Education, mortgage interest, and property taxes are in the budget
# totals but off the chart"). usda: TB-1929 stage-one group key (USDA_GROUPS). The usda keys below are the
# CE-major-category reading of TB-1929 sec. 8, with telephone moved to "Transportation and communication" as the
# bulletin's own grouping has it; run_us.py tests the alternatives (telephone, personal services, insurance lines,
# other lodging, vehicle finance, home maintenance, reading) against the Fig 5 ghosts and bars.
US_CATEGORIES = [
    dict(cat="Food at home", ce=["Food > Food at home"], role="chart", usda="food"),
    dict(cat="Food away from home", ce=["Food > Food away from home"], role="chart", usda="food"),
    dict(cat="Alcoholic beverages", ce=["Alcoholic beverages"], role="chart", usda="food"),
    dict(cat="Mortgage interest and charges", ce=["Housing > Shelter > Owned dwellings > Mortgage interest and charges"],
         role="offchart", usda="housing"),
    dict(cat="Property taxes", ce=["Housing > Shelter > Owned dwellings > Property taxes"], role="offchart", usda="housing"),
    dict(cat="Home maintenance, repairs & insurance",
         ce=["Housing > Shelter > Owned dwellings > Maintenance, repairs, insurance, and other expenses",
             "Housing > Shelter > Owned dwellings > Maintenance, repairs, insurance, other expenses"],
         role="chart", usda="housing"),
    dict(cat="Rented dwellings", ce=["Housing > Shelter > Rented dwellings"], role="chart", usda="housing"),
    dict(cat="Other lodging", ce=["Housing > Shelter > Other lodging"], role="chart", usda="housing"),
    dict(cat="Natural gas", ce=["Housing > Utilities, fuels, and public services > Natural gas"], role="chart", usda="housing"),
    dict(cat="Electricity", ce=["Housing > Utilities, fuels, and public services > Electricity"], role="chart", usda="housing"),
    dict(cat="Fuel oil and other fuels", ce=["Housing > Utilities, fuels, and public services > Fuel oil and other fuels"],
         role="chart", usda="housing"),
    dict(cat="Telephone services", ce=["Housing > Utilities, fuels, and public services > Telephone services"],
         role="chart", usda="transport"),     # TB-1929 "Transportation and communication" (COICOP 08), pinned by Fig 5
    dict(cat="Water and other public services",
         ce=["Housing > Utilities, fuels, and public services > Water and other public services"], role="chart", usda="housing"),
    dict(cat="Personal services (incl. childcare)", ce=["Housing > Household operations > Personal services"],
         role="chart", usda="furnishings"),
    dict(cat="Other household expenses", ce=["Housing > Household operations > Other household expenses"],
         role="chart", usda="furnishings"),
    dict(cat="Housekeeping supplies", ce=["Housing > Housekeeping supplies"], role="chart", usda="furnishings"),
    dict(cat="Household furnishings & equipment", ce=["Housing > Household furnishings and equipment"],
         role="chart", usda="furnishings"),
    dict(cat="Apparel and services", ce=["Apparel and services"], role="chart", usda="clothing"),
    dict(cat="Cars and trucks, new", ce=["Transportation > Vehicle purchases (net outlay) > Cars and trucks, new"],
         role="chart", usda="transport"),
    dict(cat="Cars and trucks, used", ce=["Transportation > Vehicle purchases (net outlay) > Cars and trucks, used"],
         role="chart", usda="transport"),
    dict(cat="Other vehicles (residual)", ce=["Transportation > Vehicle purchases (net outlay) > Other vehicles"],
         residual=("Transportation > Vehicle purchases (net outlay)",
                   ["Transportation > Vehicle purchases (net outlay) > Cars and trucks, new",
                    "Transportation > Vehicle purchases (net outlay) > Cars and trucks, used"]),
         role="offchart", usda="transport"),
    dict(cat="Gasoline and other fuels", ce=["Transportation > Gasoline and other fuels",
                                             "Transportation > Gasoline, other fuels, and motor oil",
                                             "Transportation > Gasoline and motor oil"], role="chart", usda="transport"),
    dict(cat="Vehicle finance charges", ce=["Transportation > Other vehicle expenses > Vehicle finance charges"],
         role="chart", usda="transport"),
    dict(cat="Vehicle maintenance and repairs", ce=["Transportation > Other vehicle expenses > Maintenance and repairs"],
         role="chart", usda="transport"),
    dict(cat="Vehicle rental, leases, licenses",
         ce=["Transportation > Other vehicle expenses > Vehicle rental, leases, licenses, and other charges"],
         role="chart", usda="transport"),
    dict(cat="Vehicle insurance", ce=["Transportation > Other vehicle expenses > Vehicle insurance"], role="chart", usda="transport"),
    dict(cat="Public and other transportation", ce=["Transportation > Public and other transportation"],
         role="chart", usda="transport"),
    dict(cat="Health insurance", ce=["Healthcare > Health insurance"], role="chart", usda="medical"),
    dict(cat="Medical services", ce=["Healthcare > Medical services"], role="chart", usda="medical"),
    dict(cat="Drugs", ce=["Healthcare > Drugs"], role="chart", usda="medical"),
    dict(cat="Medical supplies", ce=["Healthcare > Medical supplies"], role="chart", usda="medical"),
    dict(cat="Fees and admissions", ce=["Entertainment > Fees and admissions"], role="chart", usda="recreation"),
    dict(cat="Audio & visual equipment and services", ce=["Entertainment > Audio and visual equipment and services"],
         role="chart", usda="recreation"),
    dict(cat="Pets, toys, hobbies", ce=["Entertainment > Pets, toys, hobbies, and playground equipment"],
         role="chart", usda="recreation"),
    dict(cat="Other entertainment equipment", ce=["Entertainment > Other entertainment supplies, equipment, and services"],
         role="chart", usda="recreation"),
    dict(cat="Personal care products and services", ce=["Personal care products and services"], role="chart", usda="other"),
    dict(cat="Reading", ce=["Reading"], role="chart", usda="recreation"),
    dict(cat="Education", ce=["Education"], role="offchart", usda="education"),
    dict(cat="Tobacco products", ce=["Tobacco products and smoking supplies"], role="chart", usda="food"),
    dict(cat="Miscellaneous", ce=["Miscellaneous"], role="chart", usda="other"),
]
# Outside the consumption budget (pinned in run_us.py by Fig 4's D1 +4.8% and D10 -3.9% of budget):
NOT_BUDGET = {"Cash contributions": ["Cash contributions"],
              "Personal insurance and pensions": ["Personal insurance and pensions"]}

USDA_GROUPS = {"food": "Food, beverage, and tobacco", "clothing": "Clothing and footwear",
               "housing": "Housing and utilities", "furnishings": "Furnishing, household equipment, and maintenance",
               "medical": "Medical and health", "transport": "Transportation and communication",
               "recreation": "Recreation and culture", "education": "Education", "other": "Other"}
FOOD_SUBGROUPS = ["Cereals", "Meat", "Fish", "Dairy and eggs", "Oils and fat", "Fruit and vegetables",
                  "Food other", "Beverages and tobacco"]
SIX_AT_HOME = FOOD_SUBGROUPS[:6]

# %% food split (TB-1929 stage two). Each food category is cut into components, each component assigned to a
# stage-two subgroup; a subgroup's beta* is spread over its components in proportion to their observed spending,
# so a category wholly inside one subgroup inherits that subgroup's eta (alcohol and tobacco share one), and a
# category spanning subgroups gets the share-weighted combination. '*' = the whole category, 'rest' = what is left
# of the category after the listed components. 'six' = the union of the six named at-home subgroups (fitted
# shares are linear in q, so its beta* is the sum: -0.138).
_FAH = "Food > Food at home"
_MPFE = _FAH + " > Meats, poultry, fish, and eggs"
_OFAH = _FAH + " > Other food at home"
FOOD_MAPS = {
    # A: 'Food other' = restaurants (food away from home), 'Beverages and tobacco' = alcohol + tobacco, food at
    #    home = the six named subgroups. The bulletin's own words make 'Food other' the restaurant subgroup.
    "A": {"Food at home": [("*", "six")], "Food away from home": [("*", "Food other")],
          "Alcoholic beverages": [("*", "Beverages and tobacco")], "Tobacco products": [("*", "Beverages and tobacco")]},
    # B: CE components mapped line by line; the at-home 'other foods' (sweets, miscellaneous foods, food on trips,
    #    nonalcoholic beverages) share 'Food other' with restaurants, by observed spending.
    "B": {"Food at home": [(_FAH + " > Cereals and bakery products", "Cereals"),
                           (_MPFE + " > Beef", "Meat"), (_MPFE + " > Pork", "Meat"), (_MPFE + " > Other meats", "Meat"),
                           (_MPFE + " > Poultry", "Meat"), (_MPFE + " > Fish and seafood", "Fish"),
                           (_MPFE + " > Eggs", "Dairy and eggs"), (_FAH + " > Dairy products", "Dairy and eggs"),
                           (_OFAH + " > Fats and oils", "Oils and fat"), (_FAH + " > Fruits and vegetables", "Fruit and vegetables"),
                           ("rest", "Food other")],
          "Food away from home": [("*", "Food other")],
          "Alcoholic beverages": [("*", "Beverages and tobacco")], "Tobacco products": [("*", "Beverages and tobacco")]},
    # B2: as B, but nonalcoholic beverages sit in 'Beverages and tobacco' (the bulletin never says which).
    "B2": {"Food at home": [(_FAH + " > Cereals and bakery products", "Cereals"),
                            (_MPFE + " > Beef", "Meat"), (_MPFE + " > Pork", "Meat"), (_MPFE + " > Other meats", "Meat"),
                            (_MPFE + " > Poultry", "Meat"), (_MPFE + " > Fish and seafood", "Fish"),
                            (_MPFE + " > Eggs", "Dairy and eggs"), (_FAH + " > Dairy products", "Dairy and eggs"),
                            (_OFAH + " > Fats and oils", "Oils and fat"), (_FAH + " > Fruits and vegetables", "Fruit and vegetables"),
                            (_OFAH + " > Nonalcoholic beverages", "Beverages and tobacco"), ("rest", "Food other")],
           "Food away from home": [("*", "Food other")],
           "Alcoholic beverages": [("*", "Beverages and tobacco")], "Tobacco products": [("*", "Beverages and tobacco")]},
    # A2: as A, but nonalcoholic beverages (inside CE food at home) sit in 'Beverages and tobacco'.
    "A2": {"Food at home": [(_OFAH + " > Nonalcoholic beverages", "Beverages and tobacco"), ("rest", "six")],
           "Food away from home": [("*", "Food other")],
           "Alcoholic beverages": [("*", "Beverages and tobacco")], "Tobacco products": [("*", "Beverages and tobacco")]},
    # F: no split; every food category gets the food group's eta (the stage-one value alone).
    "F": {"Food at home": [("*", "food_group")], "Food away from home": [("*", "food_group")],
          "Alcoholic beverages": [("*", "food_group")], "Tobacco products": [("*", "food_group")]},
}

# %% VAT flags (VAT-able fraction of each line under an EU-style base introduced in the US). The judgment input of
# the accounting tier. START = EU VAT Directive (2006/112/EC) reading with the mixed lines at their 2024 Table 2500
# composition; CALIBRATED = what Fig 4 pins (run_us.py re-derives it and asserts it). Reasons in US_VAT_REASONS.
US_VAT_START = {
    "Food at home": 1.0, "Food away from home": 1.0, "Alcoholic beverages": 1.0, "Tobacco products": 1.0,
    "Mortgage interest and charges": 0.0, "Property taxes": 0.0,
    "Home maintenance, repairs & insurance": 0.7223, "Rented dwellings": 0.0167, "Other lodging": 0.7272,
    "Natural gas": 1.0, "Electricity": 1.0, "Fuel oil and other fuels": 1.0, "Telephone services": 1.0,
    "Water and other public services": 1.0, "Personal services (incl. childcare)": 0.0,
    "Other household expenses": 1.0, "Housekeeping supplies": 0.9507, "Household furnishings & equipment": 1.0,
    "Apparel and services": 1.0, "Cars and trucks, new": 1.0, "Cars and trucks, used": 1.0,
    "Other vehicles (residual)": 1.0, "Gasoline and other fuels": 1.0, "Vehicle finance charges": 0.0,
    "Vehicle maintenance and repairs": 1.0, "Vehicle rental, leases, licenses": 0.7064, "Vehicle insurance": 0.0,
    "Public and other transportation": 1.0, "Health insurance": 0.0, "Medical services": 0.0, "Drugs": 1.0,
    "Medical supplies": 1.0, "Fees and admissions": 1.0, "Audio & visual equipment and services": 1.0,
    "Pets, toys, hobbies": 1.0, "Other entertainment equipment": 1.0, "Personal care products and services": 1.0,
    "Reading": 1.0, "Education": 0.0628, "Miscellaneous": 0.4834,
}
US_VAT_FLAGS = dict(US_VAT_START, **{
    # Pinned by Fig 4 and the $249 dividend (run_us.py step 2 searches a grid of Directive-consistent values, each
    # with a stated reason, and asserts this is the best). Used cars: the only line whose decile profile (dip at D7,
    # D10 below D9) matches the gap between START and the published points; every good combination has it at 1/2.
    # Water: with refuse collection in (Nordic reading) the dividend comes out $250.9; with municipal refuse
    # collection outside the scope (Art. 13, public bodies acting as public authorities) it is $249.4.
    "Cars and trucks, used": 0.5, "Water and other public services": 0.6878,
})
US_VAT_REASONS = {
    "Food at home": "goods; taxable (reduced rates allowed, Annex III)",
    "Food away from home": "restaurant and catering services; taxable",
    "Alcoholic beverages": "goods; taxable", "Tobacco products": "goods; taxable",
    "Mortgage interest and charges": "credit: exempt financial service, Art. 135(1)(b)",
    "Property taxes": "a tax, not a supply",
    "Home maintenance, repairs & insurance": "mixed: repair services and materials, management and parking taxable; "
        "homeowners insurance (Art. 135(1)(a)) and ground rent (Art. 135(1)(l)) exempt; Table 2500 2024 taxable share 72.2%",
    "Rented dwellings": "letting of immovable property: exempt, Art. 135(1)(l); renter-paid repair services and materials "
        "taxable: Table 2500 2024 share 1.7%",
    "Other lodging": "mixed: hotels and trip lodging taxable (Art. 135(2)(a)); vacation-home interest, taxes and "
        "school housing not; Table 2500 2024 taxable share 72.7%",
    "Natural gas": "goods; taxable", "Electricity": "goods; taxable", "Fuel oil and other fuels": "goods; taxable",
    "Telephone services": "electronic communications; taxable",
    "Water and other public services": "water and sewerage taxable (Annex I), septic cleaning taxable; refuse collection "
        "by municipalities outside the scope (Art. 13): Table 2500 2024 share 68.8% (Nordic reading, all taxable: 1.0)",
    "Personal services (incl. childcare)": "child care, elderly and adult day care: exempt social services, Art. 132(1)(g),(h)",
    "Other household expenses": "housekeeping, gardening, pest control, moving, repairs, internet: taxable services",
    "Housekeeping supplies": "goods taxable; postage exempt (Art. 132(1)(a)), 4.9% of the line in 2024",
    "Household furnishings & equipment": "goods; taxable", "Apparel and services": "goods and services; taxable",
    "Cars and trucks, new": "goods; taxable",
    "Cars and trucks, used": "second-hand goods: dealer sales taxable, private sales outside VAT; CE cannot split them, "
        "so the share is pinned by Fig 4 at 1/2 (taxing dealer sales in full and private sales not, at about equal "
        "spending; the EU margin scheme, Arts. 311-325, would put it nearer 0.1)",
    "Other vehicles (residual)": "motorcycles etc.; taxable (off-chart, $50 a CU a year)",
    "Gasoline and other fuels": "goods; taxable", "Vehicle finance charges": "credit: exempt, Art. 135(1)(b)",
    "Vehicle maintenance and repairs": "services and parts; taxable",
    "Vehicle rental, leases, licenses": "mixed: leases, rentals, parking, tolls, towing taxable; registration, vehicle "
        "property tax, licences are taxes; Table 2500 2024 taxable share 70.6%",
    "Vehicle insurance": "insurance: exempt, Art. 135(1)(a)",
    "Public and other transportation": "passenger transport; taxable (reduced rates allowed)",
    "Health insurance": "insurance: exempt, Art. 135(1)(a)", "Medical services": "medical care: exempt, Art. 132(1)(b),(c)",
    "Drugs": "medicines are goods: taxable (reduced rates allowed, Annex III)",
    "Medical supplies": "goods (glasses, hearing aids, equipment): taxable",
    "Fees and admissions": "admissions, clubs, lessons: taxable (non-profit exemptions ignored)",
    "Audio & visual equipment and services": "goods and services; taxable", "Pets, toys, hobbies": "goods and vet services; taxable",
    "Other entertainment equipment": "goods; taxable", "Personal care products and services": "goods and services; taxable",
    "Reading": "goods; taxable", "Education": "tuition exempt, Art. 132(1)(i),(j); books and school supplies taxable: "
        "Table 2500 2024 share 6.3% (off-chart)",
    "Miscellaneous": "mixed: legal, accounting, funeral, memberships taxable; credit-card and loan interest, bank charges, "
        "lotteries, union dues, taxes exempt; Table 2500 2024 taxable share 48.3%",
}

# %% MPC schedules. Family: 1.0 through the knee (an income-group index, may be fractional), then linear to `top`
# at the top group. mid: knee and top are the least-squares fit to the 36 Fig 5 dollar bars (run_us.py step 5;
# RMSE $0.0027, the printing floor). low/high: tops are the ends of footnote 27's range (0.40, 0.65); their knees are
# pinned by Fig 7's band edges (0.474 and 0.305% of consumption). Out of sample, the mid schedule's impulse is
# 0.389% (Fig 7 central 0.390) and the mid schedule is within 0.011 of the low/high average at every decile.
US_MPC_KNEE = {"low": 1.93, "mid": 2.55, "high": 3.29}
US_MPC_TOP = {"low": 0.40, "mid": 0.53, "high": 0.65}


def mpc_knee(knee, top, n=10, bottom=1.0):
    """MPC by income group (1-based): `bottom` through group `knee`, then linear to `top` at group n.
    knee may be fractional (a continuous family for the fit surface); knee=1 means only the bottom group at 1.0."""
    d = np.arange(1, n + 1, dtype=float)
    if knee >= n:
        return np.full(n, bottom)
    return np.where(d <= knee, bottom, bottom + (top - bottom) * (d - knee) / (n - knee))


def mpc_schedules(knees=None, tops=None, n=10):
    """The low/mid/high schedules as a DataFrame (rows = income groups 1..n). knees and tops: dicts by schedule
    name, or a single knee for all schedules."""
    knees = US_MPC_KNEE if knees is None else knees
    tops = US_MPC_TOP if tops is None else tops
    if not isinstance(knees, dict):
        knees = {k: knees for k in tops}
    return pd.DataFrame({k: mpc_knee(knees[k], t, n) for k, t in tops.items()}, index=np.arange(1, n + 1))


def mpc_mid(n=10):
    return mpc_knee(US_MPC_KNEE["mid"], US_MPC_TOP["mid"], n)


# %% CE loading (any year, deciles or quintiles)
def load_ce_long(table="deciles"):
    f = {"deciles": "ce_income_deciles_long.csv", "quintiles": "ce_income_quintiles_long.csv"}[table]
    return pd.read_csv(TIDY / f, low_memory=False)


def ce_wide(year, table="deciles", long=None):
    """One CE table-year as (values, flags): index = full path, columns = 'all' then the income groups in order.
    values holds the mean (expenditure, income rows) or the single printed value (counts, characteristics);
    flags holds flag_kind ('high_rse25', 'suppressed_rse25', 'too_small', 'no_data', ...) or NaN."""
    df = load_ce_long(table) if long is None else long
    d = df[(df["year"] == year) & (df["stat"].isin(["mean", "value"]))]
    if d.empty:
        raise ValueError(f"no CE {table} table for {year}")
    if d.duplicated(["path", "group"]).any():
        raise ValueError("path x group not unique")
    vals = d.set_index(["path", "group"])["value"].astype(float).unstack("group")
    flags = d.set_index(["path", "group"])["flag_kind"].astype(object).unstack("group")
    groups = sorted([g for g in vals.columns if g != "all"])
    cols = ["all"] + groups
    return vals[cols], flags[cols]


def income_groups(vals):
    return [g for g in vals.columns if g != "all"]


def ce_path(vals, alternatives, root=EXP):
    """First alternative path (relative to root) present in the table, else None."""
    for rel in alternatives:
        full = f"{root} > {rel}" if root else rel
        if full in vals.index:
            return full
    return None


def payment_units(vals, adult_w=ADULT_W, child_w=CHILD_W):
    """Payment shares per CU from the table's own composition rows (post fn. 26): adults = people - children
    under 18; shares = adult_w*adults + child_w*children. w = each group's fraction of all payment shares
    (N_g * shares_g / sum), the weight that turns per-share group means into per-share population means.
    The rows print to one decimal, so shares carry up to +/-0.085 of rounding (run_us.py shows the effect)."""
    g = income_groups(vals)
    u = pd.DataFrame({"N_thousand": vals.loc[NCU, g], "people": vals.loc[PEOPLE, g], "children": vals.loc[CHILDREN, g]})
    u["adults"] = u["people"] - u["children"]
    u["shares"] = adult_w * u["adults"] + child_w * u["children"]
    u["w"] = u["N_thousand"] * u["shares"] / (u["N_thousand"] * u["shares"]).sum()
    u["cu_frac"] = u["N_thousand"] / u["N_thousand"].sum()
    return u


# Parents BLS prints only in part (README_bls_ce.md): their children do not add up to them, so a missing child
# cannot be recovered as parent minus siblings.
PARTIAL_PARENTS = {EXP + " > Transportation > Gasoline and other fuels": range(2023, 2100),
                   EXP + " > Transportation > Vehicle purchases (net outlay)": range(2024, 2100)}


def fill_from_parents(vals, flags, year=None):
    """Fill coded expenditure cells that the table itself identifies: 'too small to display' -> 0, and a single
    missing (suppressed or no-data) child of a parent whose children add up to it -> parent minus its other
    children. Repeats until nothing changes. Cells that are not identifiable (two or more children of one
    parent missing in the same group) stay NaN. Returns (filled values, log of every filled cell)."""
    v = vals.copy()
    g = income_groups(v)
    log = []
    exp_rows = [r for r in v.index if r == EXP or r.startswith(EXP + " > ")]
    for r in exp_rows:
        for c in g:
            if pd.isna(v.loc[r, c]) and flags.loc[r, c] == "too_small":
                v.loc[r, c] = 0.0
                log.append(dict(path=r, group=c, value=0.0, rule="too small to display -> 0"))
    kids = {}
    for r in exp_rows:
        if " > " in r:
            kids.setdefault(r.rsplit(" > ", 1)[0], []).append(r)
    changed = True
    while changed:
        changed = False
        for par, ch in kids.items():
            if par not in v.index or (year is not None and year in PARTIAL_PARENTS.get(par, ())):
                continue
            for c in g:
                miss = [k for k in ch if pd.isna(v.loc[k, c])]
                if len(miss) == 1 and pd.notna(v.loc[par, c]):
                    val = v.loc[par, c] - sum(v.loc[k, c] for k in ch if k != miss[0])
                    v.loc[miss[0], c] = val
                    log.append(dict(path=miss[0], group=c, value=val, rule=f"parent minus siblings ({par.split(' > ')[-1]})"))
                    changed = True
    return v, pd.DataFrame(log, columns=["path", "group", "value", "rule"])


def category_spending(vals, flags, cats=None):
    """Annual dollars per CU, rows = categories, columns = income groups, plus a provenance table (which path or
    residual, and how many cells carry a CE flag). Cells still missing (2022-2023 suppressions that the table
    cannot identify) come back NaN; a category with a residual rule takes the residual where its own row is NaN."""
    cats = US_CATEGORIES if cats is None else cats
    g = income_groups(vals)
    rows, prov = {}, []
    for c in cats:
        p = ce_path(vals, c["ce"])
        if p is not None:
            v = vals.loc[p, g]
            fl = flags.loc[p, g]
            src = p.replace(EXP + " > ", "")
            if v.isna().any() and c.get("residual"):
                par, kids = c["residual"]
                res = vals.loc[f"{EXP} > {par}", g] - sum(vals.loc[f"{EXP} > {k}", g] for k in kids)
                v = v.fillna(res)
                src += " (missing cells: residual of the parent)"
        elif c.get("residual"):
            par, kids = c["residual"]
            v = vals.loc[f"{EXP} > {par}", g] - sum(vals.loc[f"{EXP} > {k}", g] for k in kids)
            fl = pd.Series(np.nan, index=g, dtype=object)
            src = f"residual: {par} minus " + " minus ".join(k.split(" > ")[-1] for k in kids)
        else:
            raise KeyError(f"no CE row for {c['cat']}: {c['ce']}")
        rows[c["cat"]] = v.astype(float)
        nflag = {k: int((fl == k).sum()) for k in ["high_rse25", "suppressed_rse25", "too_small", "no_data"]}
        prov.append(dict(cat=c["cat"], role=c["role"], usda=c["usda"], ce_source=src,
                         n_high_rse=nflag["high_rse25"], n_suppressed=nflag["suppressed_rse25"],
                         n_too_small=nflag["too_small"], n_no_data=nflag["no_data"],
                         high_rse_groups=",".join(fl.index[fl == "high_rse25"]), n_nan=int(v.isna().sum())))
    return pd.DataFrame(rows).T[g], pd.DataFrame(prov).set_index("cat")


def budget_check(vals, spend, prov):
    """Budget = sum of the chart and off-chart categories; it should equal total expenditures minus personal
    insurance and pensions minus cash contributions (to the table's $1 rounding per line)."""
    g = income_groups(vals)
    tot = vals.loc[f"{EXP}", g]
    out = {k: vals.loc[f"{EXP} > {v[0]}", g] for k, v in NOT_BUDGET.items()}
    rule = tot - sum(out.values())
    inb = prov.index[prov["role"].isin(["chart", "offchart"])]
    return pd.DataFrame({"total_expenditure": tot, **out, "budget_rule": rule,
                         "budget_categories": spend.loc[inb].sum(), "diff": spend.loc[inb].sum() - rule})


# %% stage-one and stage-two parameters
def usda_params(backsolved=False):
    """TB-1929 Table 3 betas (stage one, 9 groups) and Table 4 beta* (stage two, 8 food subgroups), as printed
    (3 decimals), or the unrounded values back-solved from ERS's country tables (sensitivity only)."""
    p = pd.read_csv(TIDY / "usda_tb1929_params.csv", dtype=str)
    p["v"] = p["value"].astype(float)
    b1 = p[(p.stage == "1") & (p.parameter == "beta")].set_index("category")["v"]
    b2 = p[(p.stage == "2") & (p.parameter == "beta_star")].set_index("category")["v"]
    if backsolved:
        b = pd.read_csv(TIDY / "usda_tb1929_backsolved.csv")
        b1 = b[(b.stage == 1) & (b.parameter == "beta")].set_index("category")["value_backsolved"].reindex(b1.index)
        b2 = b[(b.stage == 2) & (b.parameter == "beta_star")].set_index("category")["value_backsolved"].reindex(b2.index)
    beta = {k: float(b1[v]) for k, v in USDA_GROUPS.items()}
    beta_star = {k: float(b2[k]) for k in FOOD_SUBGROUPS}
    beta_star["six"] = sum(beta_star[k] for k in SIX_AT_HOME)
    return dict(beta=beta, beta_star=beta_star)


def working_eta(beta, w):
    """TB-1929 eq. 5: eta = 1 + beta / w (Working's model), at whatever share w is passed."""
    return 1.0 + beta / w


# %% elasticities at observed shares
def group_shares(C, usda, budget):
    """w_kd: each income group's budget share of every USDA stage-one group (rows = group keys)."""
    k = pd.Series(usda).reindex(C.index)
    return C.groupby(k).sum().div(budget, axis=1)


def food_component_spend(vals, cat, comps, cat_spend):
    """Split one food category's annual $/CU into (subgroup, Series) parts following a FOOD_MAPS entry."""
    g = income_groups(vals)
    parts, used = [], 0.0
    for path, sub in comps:
        if path in ("*", "rest"):
            continue
        v = vals.loc[f"{EXP} > {path}", g].astype(float)
        parts.append((sub, v))
        used = used + v
    for path, sub in comps:
        if path == "*":
            parts.append((sub, cat_spend.loc[cat]))
        elif path == "rest":
            parts.append((sub, cat_spend.loc[cat] - used))
    return parts


def eta_table(model_or_parts, food_map="A", params=None, usda=None):
    """eta_gd for every category and income group. Non-food: 1 + beta_k / w_kd. Food (TB-1929 eq. 11):
    eta_F,d * (1 + beta*_g,d / w*_g,d), with w*_g,d the category's observed share of the food group and beta*_g,d
    its subgroups' beta* spread by observed spending (see FOOD_MAPS). Returns (eta, detail) where detail holds the
    shares and betas each value was evaluated at."""
    m = model_or_parts
    C, budget, vals = m["C"], m["budget"], m["vals"]
    params = usda_params() if params is None else params
    usda = m["usda"] if usda is None else usda
    fmap = FOOD_MAPS[food_map] if isinstance(food_map, str) else food_map
    wk = group_shares(C, usda, budget)
    eta = pd.DataFrame(index=C.index, columns=C.columns, dtype=float)
    det = []
    for cat in C.index:
        k = usda[cat]
        if k == "food":
            continue
        e = working_eta(params["beta"][k], wk.loc[k])
        eta.loc[cat] = e
        det.append(dict(cat=cat, usda=k, beta=params["beta"][k], **{f"w_{d}": wk.loc[k, d] for d in C.columns}))
    # food system
    food_cats = [c for c in C.index if usda[c] == "food"]
    wF = wk.loc["food"]
    etaF = working_eta(params["beta"]["food"], wF)
    food_total = C.loc[food_cats].sum()
    shares_den = m["units"]["shares"] * 12.0                       # annual $/CU -> $/share/month
    parts = {c: [(s, v / shares_den) for s, v in food_component_spend(vals, c, fmap[c], m["spend"])] for c in food_cats}
    sub_tot = {}
    for c in food_cats:
        for s, v in parts[c]:
            sub_tot[s] = sub_tot.get(s, 0.0) + v
    for c in food_cats:
        bstar = sum(params["beta_star"].get(s, 0.0) * v / sub_tot[s] for s, v in parts[c] if s != "food_group")
        wstar = C.loc[c] / food_total
        if all(s == "food_group" for s, _ in parts[c]):
            e = etaF
        else:
            e = etaF * working_eta(bstar, wstar)
        eta.loc[c] = e
        det.append(dict(cat=c, usda="food", beta=params["beta"]["food"],
                        **{f"w_{d}": wF[d] for d in C.columns},
                        **{f"wstar_{d}": wstar[d] for d in C.columns},
                        **{f"betastar_{d}": (bstar[d] if hasattr(bstar, "index") else bstar) for d in C.columns},
                        **{f"etaF_{d}": etaF[d] for d in C.columns}))
    return eta.astype(float), pd.DataFrame(det).set_index("cat")


# %% the model dict
def build_model(year=2024, table="deciles", cats=None, adult_w=ADULT_W, child_w=CHILD_W, usda=None,
                food_map="A", params=None, long=None, fill=True):
    """Everything the two tiers need for one CE table-year, as a plain dict:
    vals/flags (the table), units (payment shares, weights w), spend (annual $/CU by category), C ($/share/month),
    budget (C_d, $/share/month), Cbar (population mean per share), theta, eta (+ eta_detail), prov (sources),
    fills (cells filled by fill_from_parents; empty for 2024). Note the MPC knees are in decile units: for the
    quintile table pass an explicit 5-element MPC vector."""
    cats = US_CATEGORIES if cats is None else cats
    vals, flags = ce_wide(year, table, long)
    fills = pd.DataFrame(columns=["path", "group", "value", "rule"])
    if fill:
        vals, fills = fill_from_parents(vals, flags, year)
    units = payment_units(vals, adult_w, child_w)
    spend, prov = category_spending(vals, flags, cats)
    if spend.isna().any().any():
        bad = {c: list(spend.columns[spend.loc[c].isna()]) for c in spend.index[spend.isna().any(axis=1)]}
        raise ValueError(f"CE {year} {table}: cells the table cannot identify (suppressed, RSE >= 25%) in {bad}; "
                         "the unsuppressed values are in the BLS LABSTAT cx database, not vendored here")
    C = spend.div(units["shares"] * 12.0, axis=1)
    inb = prov.index[prov["role"].isin(["chart", "offchart"])]
    C = C.loc[inb]
    budget = C.sum()
    w = units["w"]
    m = dict(year=year, table=table, vals=vals, flags=flags, fills=fills, units=units, spend=spend.loc[inb], C=C, budget=budget,
             w=w, Cbar=C @ w, budget_bar=float(budget @ w), prov=prov.loc[inb],
             chart=[c for c in inb if prov.loc[c, "role"] == "chart"],
             usda={c["cat"]: c["usda"] for c in cats} if usda is None else dict(usda), food_map=food_map)
    m["theta"] = theta_table(C, w)
    m["eta"], m["eta_detail"] = eta_table(m, food_map, params)
    return m


def theta_table(C, w):
    """theta_dg: income group d's share of all spending on g (rows = categories, columns sum to 1 across groups)."""
    X = C.mul(w, axis=1)
    return X.div(X.sum(axis=1), axis=0)


# %% tier 1: accounting
def per_share_monthly(m, x_cu_annual):
    """Convert an annual amount per consumer unit by income group (e.g. a land-value or land-rent base taken from
    another table) into monthly dollars per payment share, the unit every function here works in.
    Finland: pass an annual amount PER HOUSEHOLD (either convention); an HBS per-consumption-unit amount must first
    be multiplied by units['hh_per_cu_ratio'] (the post convention's r_q)."""
    g = m["C"].columns
    x = pd.Series(x_cu_annual, dtype=float).reindex(g)
    return x / (m["units"]["shares"].reindex(g) * 12.0)


def net_from_base(base, w, tau=TAU, budget=None):
    """Balanced-budget flat dividend paid per share, financed by a proportional tax tau on any per-share base
    (by income group): tax_d = tau*base_d, dividend = sum_d w_d tax_d, net_d = dividend - tax_d, so
    sum_d w_d net_d = 0. For the VAT bridge base = VAT-able consumption; for an LVT, land value or land rent."""
    base = pd.Series(base, dtype=float)
    tax = tau * base
    div = float((w * tax).sum())
    out = pd.DataFrame({"base": base, "tax": tax, "dividend": div, "net": div - tax})
    if budget is not None:
        out["budget"] = budget
        out["net_pct_budget"] = 100.0 * out["net"] / budget
        out["base_pct_budget"] = 100.0 * base / budget
    return out


def vat_base(C, flags):
    """VAT-able consumption per share by income group: sum_g f_g * C_gd (flags missing from the dict count 0)."""
    f = pd.Series(flags, dtype=float).reindex(C.index).fillna(0.0)
    return C.mul(f, axis=0).sum()


def vat_accounting(m, flags=None, tau=TAU):
    """The post's accounting tier: net_d = tau * (Cbar_v - C_v,d) per share."""
    flags = US_VAT_FLAGS if flags is None else flags
    acc = net_from_base(vat_base(m["C"], flags), m["w"], tau, m["budget"])
    acc = acc.rename(columns={"base": "vatable", "base_pct_budget": "vatable_pct_budget"})
    acc["Cbar_v"] = float((m["w"] * acc["vatable"]).sum())
    return acc


def vatable_share_aggregate(m, flags=None):
    """Aggregate VAT-able share of the consumption budget (Fig 7's price-level effect is tau x pass-through x this)."""
    flags = US_VAT_FLAGS if flags is None else flags
    return float((m["w"] * vat_base(m["C"], flags)).sum() / m["budget_bar"])


# %% tier 2: demand
def budget_shock(net, mpc, budget):
    """shock_d = mpc_d * net_d / C_d (Fig 5 footer), the proportional change in group d's budget."""
    return pd.Series(np.asarray(mpc, dtype=float) * np.asarray(net, dtype=float) / np.asarray(budget, dtype=float),
                     index=budget.index)


def decompose(m, shock, eta=None):
    """c_dg = theta_dg * eta_gd * shock_d * Cbar_g = w_d * C_gd * eta_gd * shock_d: income group d's contribution
    to category g's shift ($/share/month; rows = categories, columns = groups). Fig 3/6 segments."""
    eta = m["eta"] if eta is None else eta
    shock = pd.Series(np.asarray(shock, dtype=float), index=m["C"].columns)
    return m["C"].mul(m["w"], axis=1).mul(eta).mul(shock, axis=1)


def demand_shifts(m, shock, eta=None):
    """dPct_g (in percent) and dUSD_g for one budget-shock vector."""
    c = decompose(m, shock, eta)
    usd = c.sum(axis=1)
    return pd.DataFrame({"Cbar": m["Cbar"], "dUSD": usd, "dPct": 100.0 * usd / m["Cbar"]})


def shifts_from_transfers(m, net, mpc=None, shock=None, eta=None, mpc_label="mpc"):
    """THE generic entry point. Category shifts for ANY per-share monthly net-transfer vector `net` (by income
    group; e.g. an LVT dividend minus each group's land tax), with an MPC vector `mpc` (default: the mid
    schedule) and the MPC=1 ghost alongside; or with a precomputed budget shock dC_d/C_d in `shock` (then
    `net` may be None and the ghost is skipped; if both are given, `shock` wins). Returns one row per budget
    category: role, usda, Cbar, dUSD_<mpc_label>, dPct_<mpc_label> (percent), and for the ghost dUSD_mpc1,
    dPct_mpc1. Example, any balanced-budget dividend financed by a tax on a per-share base:
        acc = net_from_base(per_share_monthly(m, base_per_cu_annual), m["w"], tau, m["budget"])
        out = shifts_from_transfers(m, acc["net"], mpc=mpc_mid())"""
    n = len(m["C"].columns)
    out = pd.DataFrame({"role": m["prov"]["role"], "usda": pd.Series(m["usda"]).reindex(m["C"].index)})
    if shock is None:
        if mpc is None:   # a model dict may carry its own default (Finland: quintile-aggregated schedule); else the decile mid
            mpc = np.asarray(m["mpc_default"], dtype=float) if "mpc_default" in m else mpc_mid(n)
        mpc = np.asarray(mpc, dtype=float)
        shock = budget_shock(net, mpc, m["budget"])
        ghost = demand_shifts(m, budget_shock(net, np.ones(n), m["budget"]), eta)
        out["dUSD_mpc1"], out["dPct_mpc1"] = ghost["dUSD"], ghost["dPct"]
    s = demand_shifts(m, shock, eta)
    out["Cbar"], out[f"dUSD_{mpc_label}"], out[f"dPct_{mpc_label}"] = s["Cbar"], s["dUSD"], s["dPct"]
    return out


def impulse(m, net=None, mpc=None, shock=None):
    """The aggregate demand impulse three ways: exact flow (sum_d w_d mpc_d net_d, $/share/month; equals the sum of
    ALL budget bars up to Engel-aggregation rounding), and the sum of the charted bars; each as % of total
    consumption (the budget) and of the charted budget. With a precomputed budget shock dC_d/C_d instead of
    (net, mpc), flow = sum_d w_d shock_d C_d."""
    if shock is None:
        if mpc is None and "mpc_default" in m:
            mpc = m["mpc_default"]
        shock = budget_shock(net, mpc, m["budget"])
    shock = pd.Series(np.asarray(shock, dtype=float), index=m["budget"].index)
    flow = float((m["w"] * shock * m["budget"]).sum())
    usd = demand_shifts(m, shock)["dUSD"]
    chart = m["chart"]
    charted_budget = float(m["Cbar"].loc[chart].sum())
    return dict(flow_usd=flow, bars_all_usd=float(usd.sum()), bars_chart_usd=float(usd.loc[chart].sum()),
                budget_usd=m["budget_bar"], charted_budget_usd=charted_budget,
                flow_pct_consumption=100 * flow / m["budget_bar"],
                bars_chart_pct_consumption=100 * float(usd.loc[chart].sum()) / m["budget_bar"],
                bars_chart_pct_charted=100 * float(usd.loc[chart].sum()) / charted_budget,
                flow_pct_charted=100 * flow / charted_budget)


def top_movers(shifts, col, chart, k=10):
    """The k charted categories with the largest |shift| (Fig 3/6 selection)."""
    s = shifts.loc[chart, col]
    return s.abs().sort_values(ascending=False).index[:k].tolist()


# %% =============================================================================================================
# FINLAND: Household Budget Survey 2022 by household income quintile (ktutk 14pg), Figures 1-3 of the post.
# The same two tiers as the US, on the HBS table the post cites (footnote 22). Everything is in euros per payment
# share per month (adult 1, child 0.3); groups are q1..q5 (each 20% of households, README_fin.md).
#
# What the post did, as reconstructed from its published numbers (run_fi.py derives every item again):
#   data          the per-CONSUMPTION-UNIT table (OECD-modified units) for every category; per household only for the
#                 all-items total, through the quintile's per-household/per-CU ratio  r_q = hh_total_q / cu_total_q
#   payment units tulonjako 12ew (person deciles by life-cycle stage): adults = everyone in one-person, couple and
#                 'other' households, 2 per couple-with-children household, 1 per single parent; children = the rest;
#                 decile pairs averaged into 'quintiles' (D1, D2 -> q1 ...); shares s_q = adults + 0.3 children per hh
#   per share     C_gq = cu_gq * r_q / (12 s_q), so the budget B_q = hh_total_q / (12 s_q)
#   weights       w_q proportional to s_q / r_q: payment shares per consumption unit, i.e. the quintiles treated as
#                 holding EQUAL NUMBERS OF CONSUMPTION UNITS (they hold equal numbers of households). This weighting is
#                 what makes the dividend EUR 193 and the nets balance; it also makes theta the per-CU market share
#                 theta_qg = cu_gq / sum_q cu_gq, which is what the Fig 3 segments and Fig 2 ghosts require.
#   EUR labels    dEUR_g = dPct_g * Cbar_g with Cbar_g from the TOTAL column: cu_total_g * r_total / (12 s_total),
#                 s_total from 12ew's own total column (1.6168 shares per household). This is 4.1% above the
#                 weighted mean sum_q w_q C_gq that the dividend uses ('budgets averaging EUR 2,051' is this column).
#                 Division parents also break Engel adding-up: a TB-1929 group split over two divisions counts its
#                 beta twice (07/08, 12/13), so sum beta = +0.052 and the bars over-allocate the flow by 5.2%.
#   elasticities  'parent-group fidelity' = the COICOP DIVISION: eta_gq = 1 + beta_k / w_dq with w_dq the division's
#                 budget share and beta_k the TB-1929 beta of the division's group; the food system is divisions
#                 01 + 02 + 11 (restaurants AND accommodation), split by the stage-two betas (eq. 11): 01.1 the six
#                 named subgroups, 01.2 + 02 'Beverages and tobacco', 11 'Food other'.
#   VAT flags     whole COICOP-2018 groups (the Fig 2 categories), not Finnish law line by line (see FI_VAT_LINES).
#   MPC           the post's decile 'literature schedule' aggregated to quintiles: pair means of the US schedules.
# convention="post" rebuilds exactly that. convention="coherent" is the same machinery with the bases made
# consistent (per-household table, equal-HOUSEHOLD weights, theta and Cbar from the same weighted data): the
# version to use for new comparisons (NOTES_fi.md says by how much the two differ).

FI_Q = ["q1", "q2", "q3", "q4", "q5"]
FI_HBS_FILE, FI_COMP_FILE = "fi_hbs2022_long.csv", "fi_hh_composition.csv"

# The 47 budget categories: the 37 bars of Fig 2 (labels exactly as printed), then the 10 off-chart lines that are in
# the budget totals: imputed rentals and owner-occupied housing (nothing transacted), education (0.3% budget share:
# beta/w degenerate), consumption abroad (not domestic), and six small groups the figure does not draw. COICOP 01.3
# and 02.2 are not asked in the HBS ('.....') and are left out. 'div' = COICOP division (the elasticity parent);
# 'usda' = TB-1929 stage-one group of the division (README_usda sec. 8).
FI_CATEGORIES = [
    dict(cat="04.1 Actual rents", code="041", role="chart"),
    dict(cat="01.1 Food (at home)", code="011", role="chart"),
    dict(cat="08.3 Information and communication services", code="083", role="chart"),
    dict(cat="06.1 Medicines and health products", code="061", role="chart"),
    dict(cat="13.1 Personal care", code="131", role="chart"),
    dict(cat="03.1 Clothing", code="031", role="chart"),
    dict(cat="07.2 Operation of personal transport equipment", code="072", role="chart"),
    dict(cat="11.1 Food and beverage serving services", code="111", role="chart"),
    dict(cat="04.4 Water & misc. dwelling services", code="044", role="chart"),
    dict(cat="12.1 Insurance", code="121", role="chart"),
    dict(cat="06.2 Outpatient care services", code="062", role="chart"),
    dict(cat="08.1 Information and communication equipment", code="081", role="chart"),
    dict(cat="04.5 Electricity, gas and other fuels", code="045", role="chart"),
    dict(cat="12.2 Financial services", code="122", role="chart"),
    dict(cat="07.3 Passenger transport services", code="073", role="chart"),
    dict(cat="09.3 Garden products and pets", code="093", role="chart"),
    dict(cat="09.4 Recreational services", code="094", role="chart"),
    dict(cat="02.3 Tobacco", code="023", role="chart"),
    dict(cat="01.2 Non-alcoholic beverages", code="012", role="chart"),
    dict(cat="02.1 Alcoholic beverages", code="021", role="chart"),
    dict(cat="09.7 Newspapers, books and stationery", code="097", role="chart"),
    dict(cat="13.2 Other personal effects", code="132", role="chart"),
    dict(cat="05.6 Goods and services for routine household maintenance", code="056", role="chart"),
    dict(cat="03.2 Footwear", code="032", role="chart"),
    dict(cat="09.2 Other recreational goods", code="092", role="chart"),
    dict(cat="05.2 Household textiles", code="052", role="chart"),
    dict(cat="09.6 Cultural services", code="096", role="chart"),
    dict(cat="05.3 Household appliances", code="053", role="chart"),
    dict(cat="05.4 Glassware, tableware and household utensils", code="054", role="chart"),
    dict(cat="11.2 Accommodation services", code="112", role="chart"),
    dict(cat="05.1 Furniture, furnishings and loose carpets (D)", code="051", role="chart"),
    dict(cat="04.3 Maintenance, repair and security of the dwelling", code="043", role="chart"),
    dict(cat="05.5 Tools and equipment for house and garden", code="055", role="chart"),
    dict(cat="09.8 Package holidays", code="098", role="chart"),
    dict(cat="09.1 Recreational durables", code="091", role="chart"),
    dict(cat="13.9 Other services", code="139", role="chart"),
    dict(cat="07.1 Purchase of vehicles", code="071", role="chart"),
    dict(cat="04.2 Imputed rentals (off-chart)", code="042", role="offchart"),
    dict(cat="04.6 Interest on housing loans (off-chart)", code="046", role="offchart"),
    dict(cat="06.3 Inpatient care services (off-chart)", code="063", role="offchart"),
    dict(cat="06.4 Other health services (off-chart)", code="064", role="offchart"),
    dict(cat="07.4 Transport services of goods (off-chart)", code="074", role="offchart"),
    dict(cat="08.2 Software, excluding games (off-chart)", code="082", role="offchart"),
    dict(cat="09.5 Cultural goods (off-chart)", code="095", role="offchart"),
    dict(cat="10 Education services (off-chart)", code="10", role="offchart"),
    dict(cat="13.3 Social protection (off-chart)", code="133", role="offchart"),
    dict(cat="77 Consumption abroad (off-chart)", code="77", role="offchart"),
]
FI_DIV_USDA = {"01": "food", "02": "food", "03": "clothing", "04": "housing", "05": "furnishings", "06": "medical",
               "07": "transport", "08": "transport", "09": "recreation", "10": "education", "11": "food", "12": "other",
               "13": "other", "77": None}

# Food system (TB-1929 stage two). members: categories in the food group (its budget share gives eta_F); map:
# category -> stage-two subgroup ('six' = the six named at-home subgroups, beta* summed); a subgroup's beta* is spread
# over its member categories by observed spending, so every category in one subgroup gets that subgroup's eta.
FI_FOOD_MAPS = {
    # F3 (adopted, pinned by the Fig 2 ghosts): the food group is divisions 01, 02 and 11 whole; non-alcoholic
    # beverages sit in 'Beverages and tobacco' (the bulletin leaves it open, README_usda sec. 8).
    "F3": dict(members=["011", "012", "021", "023", "111", "112"],
               map={"011": "six", "012": "Beverages and tobacco", "021": "Beverages and tobacco",
                    "023": "Beverages and tobacco", "111": "Food other", "112": "Food other"}),
    "F2": dict(members=["011", "012", "021", "023", "111", "112"],
               map={"011": "six", "012": "six", "021": "Beverages and tobacco", "023": "Beverages and tobacco",
                    "111": "Food other", "112": "Food other"}),
    "F4": dict(members=["011", "012", "021", "023", "111", "112"],
               map={"011": "six", "012": "Food other", "021": "Beverages and tobacco", "023": "Beverages and tobacco",
                    "111": "Food other", "112": "Food other"}),
    # F1: the README_usda reading (food = 01, 02, 11.1); accommodation 11.2 is its own parent with the 'Other' beta.
    "F1": dict(members=["011", "012", "021", "023", "111"],
               map={"011": "six", "012": "Beverages and tobacco", "021": "Beverages and tobacco",
                    "023": "Beverages and tobacco", "111": "Food other"}),
    # F0: no stage-two split; every food category gets eta_F.
    "F0": dict(members=["011", "012", "021", "023", "111", "112"],
               map={"011": None, "012": None, "021": None, "023": None, "111": None, "112": None}),
}

# VAT lines: each budget category is one line, or is split where Finnish law treats its parts differently (2022 law:
# standard 24%; 14% food and restaurant/catering; 10% books, newspapers, medicines, passenger transport,
# accommodation, cultural and entertainment events, sports services; exempt: letting of dwellings, health and
# medical care, social services, education, insurance and financial services, lotteries; outside: public fees and
# taxes). codes: HBS codes summed for the line; None = the rest of the category. flag_law = the law reading;
# flag = the adopted value: the best of run_fi.py's step-4 grid against Fig 1, which re-derives and asserts it.
# Fig 1 pins the post's whole-group reading on the big mixed lines (housing-company charges, used cars, licences
# and vehicle fees in, package holidays and consumption abroad out; games of chance and international flights in,
# less firmly); on the lines it cannot see (sea transport, letter post, church fees, social services) the best
# combination is the law reading. rate = the existing rate, used only for the tax-exclusive test.
FI_VAT_LINES = [
    dict(line="maintenance charges of housing companies", cat="044", codes=["04441"], flag_law=0.0, flag=1.0, rate=0.24,
         reason="housing-company maintenance charges to shareholder-residents are not a VAT-able supply (real-estate "
                "exemption; the company cannot deduct input VAT, so VAT is embedded, not charged)"),
    dict(line="water, refuse, sewerage, other dwelling services", cat="044", codes=None, flag_law=1.0, flag=1.0, rate=0.24,
         reason="water supply, sewerage and waste collection by utilities are taxable at 24%; chimney sweeping etc. taxable"),
    dict(line="used cars", cat="071", codes=["07112"], flag_law=0.5, flag=1.0, rate=0.24,
         reason="dealer sales taxed on the margin only (margin scheme), private sales outside VAT; the HBS cannot split them"),
    dict(line="new cars, motorcycles, bicycles", cat="071", codes=None, flag_law=1.0, flag=1.0, rate=0.24, reason="goods; 24%"),
    dict(line="driving lessons, tests, licences", cat="072", codes=["07243"], flag_law=0.0, flag=1.0, rate=0.24,
         reason="mostly licences and vehicle charges (public fees, outside VAT); inspections and lessons taxable"),
    dict(line="fuels, parts, repairs, parking, hire", cat="072", codes=None, flag_law=1.0, flag=1.0, rate=0.24,
         reason="goods and services; 24%"),
    dict(line="international air transport", cat="073", codes=["07332"], flag_law=0.0, flag=1.0, rate=0.10,
         reason="international passenger transport is exempt with the right of deduction (zero-rated)"),
    dict(line="sea and inland-waterway transport", cat="073", codes=["0734"], flag_law=0.0, flag=0.0, rate=0.10,
         reason="mostly international ferry crossings (zero-rated); domestic road ferries are free"),
    dict(line="domestic passenger transport", cat="073", codes=None, flag_law=1.0, flag=1.0, rate=0.10,
         reason="passenger transport; 10%"),
    dict(line="letter post", cat="074", codes=["07411"], flag_law=0.0, flag=0.0, rate=0.24,
         reason="universal postal service exempt (Directive Art. 132(1)(a))"),
    dict(line="parcels, removals, delivery", cat="074", codes=None, flag_law=1.0, flag=1.0, rate=0.24, reason="services; 24%"),
    dict(line="games of chance", cat="094", codes=["0947"], flag_law=0.0, flag=1.0, rate=0.24,
         reason="lotteries and gambling exempt (lottery tax instead)"),
    dict(line="sports and recreational services", cat="094", codes=["0946"], flag_law=1.0, flag=1.0, rate=0.10,
         reason="sports services and admissions; 10%"),
    dict(line="other recreational services", cat="094", codes=None, flag_law=1.0, flag=1.0, rate=0.24,
         reason="repairs and hire of recreational goods, veterinary services; 24%"),
    dict(line="package holidays", cat="098", codes=None, flag_law=0.0, flag=0.0, rate=0.24,
         reason="travel-agent margin scheme; the margin on trips outside the EU is zero-rated"),
    dict(line="religious services", cat="139", codes=["13902"], flag_law=0.0, flag=0.0, rate=0.24,
         reason="church membership fees and church tax: not a supply"),
    dict(line="other services n.e.c.", cat="139", codes=["13909"], flag_law=0.5, flag=1.0, rate=0.24,
         reason="mixed: legal services, funerals, agencies taxable; union dues and administrative fees outside VAT"),
    dict(line="rest of other services", cat="139", codes=None, flag_law=0.0, flag=0.0, rate=0.24,
         reason="13.9.0.1 (published only as '...'): not VAT-registered"),
    dict(line="domestic services by paid staff", cat="056", codes=["05621"], flag_law=1.0, flag=1.0, rate=0.24,
         reason="cleaning and household services bought from firms; 24%"),
    dict(line="household goods and other services", cat="056", codes=None, flag_law=1.0, flag=1.0, rate=0.24, reason="24%"),
    dict(line="medicines", cat="061", codes=["0611"], flag_law=1.0, flag=1.0, rate=0.10, reason="medicines; 10%"),
    dict(line="medical products and appliances", cat="061", codes=None, flag_law=1.0, flag=1.0, rate=0.24,
         reason="medical goods, glasses, aids; 24%"),
    dict(line="books, newspapers and periodicals", cat="097", codes=["0971", "0972"], flag_law=1.0, flag=1.0, rate=0.10,
         reason="books, newspapers, periodicals; 10%"),
    dict(line="printed matter and stationery", cat="097", codes=None, flag_law=1.0, flag=1.0, rate=0.24, reason="24%"),
    dict(line="cinemas, theatres, concerts, museums", cat="096", codes=["0961", "0962"], flag_law=1.0, flag=1.0, rate=0.10,
         reason="cultural and entertainment events; 10%"),
    dict(line="other cultural services", cat="096", codes=None, flag_law=1.0, flag=1.0, rate=0.24, reason="24%"),
]
# Whole categories (one line each): exempt or outside, with reasons; every other category is one taxable line at the
# rate in FI_RATES (default 24%).
FI_EXEMPT = {
    "041": "letting of dwellings: exempt", "042": "imputed rent of owner-occupiers: nothing transacted",
    "046": "interest on housing loans: exempt financial service", "062": "outpatient health care: exempt",
    "063": "inpatient care: exempt", "064": "diagnostic, laboratory and ambulance services: exempt",
    "10": "education: exempt", "121": "insurance: exempt", "122": "financial services: exempt",
    "133": "social services (child care, home care): exempt", "77": "consumption abroad: not in the Finnish base"}
FI_RATES = {"011": 0.14, "012": 0.14, "111": 0.14, "112": 0.10}   # 11.1 at the food rate (its alcohol part is 24%)


def fi_hbs_wide(measure="per_cu_year", long=None):
    """One HBS 2022 measure as (values, status): index = StatFin COICOP2018 code ('0' total, '01'..'13' divisions,
    '011' groups, ...), columns 'total', q1..q5. Euro measures are annual per consumption unit or per household."""
    df = pd.read_csv(TIDY / FI_HBS_FILE, dtype={"coicop_code": str, "parent_code": str}) if long is None else long
    d = df[df["measure"] == measure]
    vals = d.set_index(["coicop_code", "group"])["value"].astype(float).unstack("group")[["total"] + FI_Q]
    stat = d.set_index(["coicop_code", "group"])["status"].astype(object).unstack("group")[["total"] + FI_Q]
    return vals, stat


def fi_composition(route="12ew", year=2022, comp=None):
    """Payment units per household by HBS quintile (rows 'total', q1..q5): adults, children, persons, shares
    (= adults + 0.3 children), households, the route's own OECD-modified units, and the HBS 14qa means.
    Routes:
      '12ew'             the post's (footnote 22), adopted: tulonjako 12ew 2022, person deciles by life-cycle stage.
                         Adults: every person in one-person, childless-couple and 'other' households, 2 per couple
                         with children, 1 per single parent; children: the rest. Decile pairs averaged (the mean of
                         D1's and D2's per-household values -> q1, ...); 'total' from the table's own total column.
                         12ew deciles are PERSON deciles on another income concept, so the pairs are not the HBS
                         quintiles (README_fin.md).
      '12ew_pooled'      the same, the pair pooled (sum of persons / sum of households) instead of averaged.
      '12ew_two_adults'  pair means, with 'other households' holding two adults each and the rest children.
      '14qa'             the HBS's own quintiles (ktutk 14qa): persons aged 14+ and 0-13 from the mean household size
                         and mean OECD-modified units (adults = 14+; the age split is 14, not 18)."""
    c = pd.read_csv(TIDY / FI_COMP_FILE) if comp is None else comp
    q14 = c[(c["source_table"] == "ktutk 14qa") & (c["year"] == year) & (c["subgroup"] == "all")]
    g14 = lambda meas: q14[q14["measure"] == meas].set_index("group")["value"].astype(float).reindex(["total"] + FI_Q)
    out = pd.DataFrame(index=["total"] + FI_Q)
    out["households"] = g14("households")
    out["hbs_mean_size"], out["hbs_mean_cu"] = g14("avg_household_size"), g14("avg_consumption_units")
    if route.startswith("12ew"):
        e = c[(c["source_table"] == "tjt 12ew") & (c["year"] == year)]
        hh = e[e["measure"] == "households"].pivot_table(index="subgroup", columns="group", values="value", aggfunc="first")
        pp = e[e["measure"] == "persons"].pivot_table(index="subgroup", columns="group", values="value", aggfunc="first")
        ad = pp.loc["stage_1"] + pp.loc["stage_2"] + 2.0 * hh.loc["stage_31"] + 1.0 * hh.loc["stage_32"]
        ch = (pp.loc["stage_31"] - 2.0 * hh.loc["stage_31"]) + (pp.loc["stage_32"] - 1.0 * hh.loc["stage_32"])
        if route == "12ew_two_adults":
            ad = ad + 2.0 * hh.loc["stage_4"]
            ch = ch + pp.loc["stage_4"] - 2.0 * hh.loc["stage_4"]
        else:
            ad = ad + pp.loc["stage_4"]
        nh = hh.loc["all"]
        dec = [f"d{i:02d}" for i in range(1, 11)]
        a, k = {"total": ad["total"] / nh["total"]}, {"total": ch["total"] / nh["total"]}
        for i, q in enumerate(FI_Q):
            d1, d2 = dec[2 * i], dec[2 * i + 1]
            if route in ("12ew", "12ew_two_adults"):
                a[q] = (ad[d1] / nh[d1] + ad[d2] / nh[d2]) / 2.0
                k[q] = (ch[d1] / nh[d1] + ch[d2] / nh[d2]) / 2.0
            else:
                a[q] = (ad[d1] + ad[d2]) / (nh[d1] + nh[d2])
                k[q] = (ch[d1] + ch[d2]) / (nh[d1] + nh[d2])
        out["adults"], out["children"] = pd.Series(a), pd.Series(k)
        out["source_households_12ew"] = pd.Series({"total": nh["total"], **{q: nh[dec[2 * i]] + nh[dec[2 * i + 1]]
                                                                           for i, q in enumerate(FI_Q)}})
    elif route == "14qa":
        out["adults"], out["children"] = g14("avg_persons_14plus"), g14("avg_children_under14")
    else:
        raise ValueError(f"unknown composition route {route}")
    out["persons"] = out["adults"] + out["children"]
    out["shares"] = ADULT_W * out["adults"] + CHILD_W * out["children"]
    out["route_oecd_cu"] = 1.0 + 0.5 * (out["adults"] - 1.0) + 0.3 * out["children"]
    out["route"] = route
    return out


def fi_category_spending(vals, cats=None):
    """Annual euros by category (rows) and group (columns 'total', q1..q5) on the table's basis."""
    cats = FI_CATEGORIES if cats is None else cats
    return pd.DataFrame({c["cat"]: vals.loc[c["code"], ["total"] + FI_Q] for c in cats}).T.astype(float)


def fi_line_spending(vals, cats=None, lines=None):
    """Annual euros by VAT line (rows) and group: the split lines of FI_VAT_LINES (a line with codes=None is the rest
    of its category), plus one whole-category line for every other category. Returns (spending, line table)."""
    cats = FI_CATEGORIES if cats is None else cats
    lines = FI_VAT_LINES if lines is None else lines
    code2cat = {c["code"]: c["cat"] for c in cats}
    split = {l["cat"] for l in lines}
    rows, meta = {}, []
    for c in cats:
        cc = c["code"]
        tot = vals.loc[cc, ["total"] + FI_Q].astype(float)
        if cc not in split:
            ex = cc in FI_EXEMPT
            rows[c["cat"]] = tot
            meta.append(dict(line=c["cat"], cat=c["cat"], code=cc, codes=cc, flag_law=0.0 if ex else 1.0,
                             flag=0.0 if ex else 1.0, rate=0.0 if ex else FI_RATES.get(cc, 0.24),
                             reason=FI_EXEMPT.get(cc, "goods and services; taxable")))
            continue
        used = 0.0 * tot
        for l in [l for l in lines if l["cat"] == cc and l["codes"] is not None]:
            v = vals.loc[l["codes"], ["total"] + FI_Q].astype(float)
            if v.isna().any().any():
                raise ValueError(f"suppressed cells in VAT line {l['line']}: {l['codes']}")
            rows[l["line"]] = v.sum()
            used = used + v.sum()
        for l in [l for l in lines if l["cat"] == cc and l["codes"] is None]:
            rows[l["line"]] = tot - used
        for l in [l for l in lines if l["cat"] == cc]:
            meta.append(dict(line=l["line"], cat=code2cat[cc], code=cc, codes=",".join(l["codes"]) if l["codes"] else
                             f"rest of {cc}", flag_law=l["flag_law"], flag=l["flag"], rate=l["rate"], reason=l["reason"]))
    return pd.DataFrame(rows).T, pd.DataFrame(meta).set_index("line")


def fi_eta_table(m, food_map="F3", params=None, parent="division"):
    """eta_gq for every category and quintile, at the model's own budget shares (C / budget).
    parent='division' (the post's 'parent-group fidelity'): eta = 1 + beta_k / w_d, w_d the COICOP division's share,
    beta_k the TB-1929 beta of the division's group. parent='usda': divisions pooled into the TB-1929 groups (07+08
    'Transportation and communication', 12+13 'Other') before taking the share (the US reading; a mapping test).
    Food (TB-1929 eq. 11): eta_F * (1 + beta*_g / w*_g), eta_F from the food group's share (FI_FOOD_MAPS[food_map]),
    beta*_g the category's subgroup beta* spread by spending, w*_g its share of the food group. Consumption abroad
    (no TB-1929 group) gets eta = 1. Returns (eta, detail)."""
    params = usda_params() if params is None else params
    fm = FI_FOOD_MAPS[food_map] if isinstance(food_map, str) else food_map
    C, bud, code = m["C"], m["budget"], m["code"]
    cat_of = {v: k for k, v in code.items()}
    food = [cat_of[c] for c in fm["members"]]
    div = {g: (code[g][:2] if code[g] != "10" else "10") for g in C.index}
    if parent == "usda":
        par = {g: FI_DIV_USDA.get(div[g]) for g in C.index}
    else:
        par = dict(div)
    if code.get(cat_of.get("112")) and cat_of["112"] not in food:     # F1: accommodation is its own 'Other' parent
        par[cat_of["112"]] = "112"
    beta_of = lambda p: params["beta"][FI_DIV_USDA[p] if p in FI_DIV_USDA else ("other" if p == "112" else p)]
    eta = pd.DataFrame(index=C.index, columns=C.columns, dtype=float)
    det = []
    for g in C.index:
        if g in food:
            continue
        if div[g] == "77":
            eta.loc[g] = 1.0
            det.append(dict(cat=g, parent="none", beta=0.0, **{f"w_{q}": np.nan for q in C.columns}))
            continue
        members = [h for h in C.index if par.get(h) == par[g] and h not in food]
        w = C.loc[members].sum() / bud
        b = beta_of(par[g])
        eta.loc[g] = working_eta(b, w)
        det.append(dict(cat=g, parent=par[g], beta=b, **{f"w_{q}": w[q] for q in C.columns}))
    F = C.loc[food].sum()
    wF = F / bud
    etaF = working_eta(params["beta"]["food"], wF)
    subs = {}
    for g in food:
        s = fm["map"][code[g]]
        subs.setdefault(s, []).append(g)
    for g in food:
        s = fm["map"][code[g]]
        if s is None:
            e, bstar, wstar = etaF, 0.0 * wF, C.loc[g] / F
        else:
            bs = params["beta_star"][s]
            bstar = bs * C.loc[g] / C.loc[subs[s]].sum()
            wstar = C.loc[g] / F
            e = etaF * working_eta(bstar, wstar)
        eta.loc[g] = e
        det.append(dict(cat=g, parent="food system", beta=params["beta"]["food"], subgroup=s,
                        **{f"w_{q}": wF[q] for q in C.columns}, **{f"wstar_{q}": wstar[q] for q in C.columns},
                        **{f"betastar_{q}": bstar[q] for q in C.columns}, **{f"etaF_{q}": etaF[q] for q in C.columns}))
    return eta.astype(float), pd.DataFrame(det).set_index("cat")


def fi_mpc_schedules(knees=None, tops=None):
    """The decile schedules (mpc_schedules(): low / mid / high) aggregated to quintiles by decile-pair means: the
    post's 'literature MPC schedule (quintile-aggregated)'. Rows q1..q5."""
    dec = mpc_schedules(knees, tops, n=10)
    out = dec.groupby((np.arange(10) // 2)).mean()
    out.index = FI_Q
    return out


def fi_mpc_mid():
    return fi_mpc_schedules()["mid"].values


def build_fi_model(composition="12ew", convention="post", food_map="F3", params=None, eta_parent="division",
                   cats=None, lines=None, long=None, comp=None, weights=None, cu_per_household="hbs_ratio"):
    """Everything the two tiers need for the Finnish HBS 2022 quintiles, as a plain dict with the same keys as
    build_model(), so net_from_base(), shifts_from_transfers(), decompose() and impulse() work unchanged.
    convention='post'     per-CU table, C_gq = cu_gq * r_q / (12 s_q), weights proportional to s_q / r_q (equal
                          consumption units per quintile), theta = per-CU market shares; Cbar_post (the post's EUR
                          conversion, from the total column) and eur_scale = Cbar_post / Cbar ride along.
    convention='coherent' per-household table, C_gq = hh_gq / (12 s_q), weights proportional to N_q s_q (equal
                          households), theta, Cbar and eta all from the same data; Cbar_post = Cbar, eur_scale = 1.
    Options used only to test what pins each element (run_fi.py): weights='equal_cu' | 'equal_households'
    (overrides the convention's weighting); cu_per_household (post only) = 'hbs_ratio' (r_q, the table's own
    per-household / per-CU ratio) | '14qa_mean' (14qa mean OECD units) | 'route' (units implied by the
    composition route's adults and children).
    Extra keys: code (category -> COICOP code), lines / line_meta (VAT lines in EUR per share per month),
    conv (annual table units -> monthly per share), mpc_default (fi_mpc_mid())."""
    cats = FI_CATEGORIES if cats is None else cats
    long = pd.read_csv(TIDY / FI_HBS_FILE, dtype={"coicop_code": str, "parent_code": str}) if long is None else long
    vcu, scu = fi_hbs_wide("per_cu_year", long)
    vhh, shh = fi_hbs_wide("per_household_year", long)
    units = fi_composition(composition, comp=comp)
    s = units["shares"]
    units["hh_per_cu_ratio"] = vhh.loc["0"] / vcu.loc["0"]   # per-household / per-CU, all items (1.404 in total)
    if convention == "post":
        vals, stat = vcu, scu
        ratio = {"hbs_ratio": units["hh_per_cu_ratio"], "14qa_mean": units["hbs_mean_cu"],
                 "route": units["route_oecd_cu"]}[cu_per_household]
        conv = ratio / (12.0 * s)
        weights = "equal_cu" if weights is None else weights
    elif convention == "coherent":
        vals, stat = vhh, shh
        ratio = pd.Series(1.0, index=s.index)
        conv = 1.0 / (12.0 * s)
        weights = "equal_households" if weights is None else weights
    else:
        raise ValueError(convention)
    if weights == "equal_cu":
        w = (s / ratio).loc[FI_Q]
    elif weights == "equal_households":
        w = (units["households"] * s).loc[FI_Q]
    else:
        raise ValueError(weights)
    w = w / w.sum()
    units["cu_per_household_used"] = ratio
    units["conv"] = conv
    units["w"] = w
    spend_all = fi_category_spending(vals, cats)
    if spend_all[FI_Q].isna().any().any():
        raise ValueError("suppressed cells in budget categories")
    spend = spend_all[FI_Q]
    C = spend.mul(conv[FI_Q], axis=1)
    budget = C.sum()
    Cbar = C @ w
    if convention == "post":
        Cbar_post = spend_all["total"] * conv["total"]   # the total column converted on its own (r_total, 12ew total)
    else:
        Cbar_post = Cbar.copy()
    lsp, lmeta = fi_line_spending(vals, cats, lines)
    prov = pd.DataFrame({"role": {c["cat"]: c["role"] for c in cats}, "code": {c["cat"]: c["code"] for c in cats}})
    prov["division"] = [c if c in ("10", "77") else c[:2] for c in prov["code"]]
    prov["usda"] = prov["division"].map(FI_DIV_USDA)
    sup = [{k: int((stat.loc[c["code"], FI_Q].astype(str).isin([".", "..", "...", "....."])).sum())
            for k in ["n_suppressed"]} for c in cats]
    prov["n_suppressed_cells"] = [d["n_suppressed"] for d in sup]
    prov["source"] = f"HBS 2022 ktutk 14pg, {'per consumption unit' if convention == 'post' else 'per household'}"
    m = dict(year=2022, table=f"fi_hbs_quintiles ({convention}, {composition})", convention=convention,
             composition=composition, weights=weights, cu_per_household=cu_per_household if convention == "post" else None,
             vals=vals, status=stat, vals_cu=vcu, vals_hh=vhh, units=units, spend=spend,
             spend_total=spend_all["total"], C=C, budget=budget, w=w, Cbar=Cbar, budget_bar=float(budget @ w),
             Cbar_post=Cbar_post, budget_bar_post=float(Cbar_post.sum()), eur_scale=Cbar_post / Cbar, prov=prov,
             chart=[c["cat"] for c in cats if c["role"] == "chart"], usda=prov["usda"].to_dict(),
             code=prov["code"].to_dict(), food_map=food_map, lines=lsp[FI_Q].mul(conv[FI_Q], axis=1),
             lines_total=lsp["total"] * conv["total"], line_meta=lmeta, conv=conv, mpc_default=fi_mpc_mid())
    m["theta"] = theta_table(C, w)
    m["eta"], m["eta_detail"] = fi_eta_table(m, food_map, params, eta_parent)
    return m


def fi_vat_flags(which="adopted", lines=None):
    """Line flags as a dict: 'adopted' (FI_VAT_LINES flag, whole categories per FI_EXEMPT) or 'law'."""
    lines = FI_VAT_LINES if lines is None else lines
    key = "flag" if which == "adopted" else "flag_law"
    out = {l["line"]: l[key] for l in lines}
    for c in FI_CATEGORIES:
        if c["code"] not in {l["cat"] for l in lines}:
            out[c["cat"]] = 0.0 if c["code"] in FI_EXEMPT else 1.0
    return out


def fi_vat_base(m, flags=None, inclusive=True):
    """VAT-able consumption per share by quintile: sum over VAT lines of flag x spending (EUR per share per month).
    inclusive=False: the tax-exclusive base, each line divided by 1 + its existing rate (the surcharge read as 15
    points on the net-of-VAT price)."""
    flags = fi_vat_flags() if flags is None else flags
    f = pd.Series(flags, dtype=float).reindex(m["lines"].index)
    if f.isna().any():
        raise KeyError(f"no flag for lines {list(f.index[f.isna()])}")
    L = m["lines"]
    if not inclusive:
        L = L.div(1.0 + m["line_meta"]["rate"].reindex(L.index), axis=0)
    return L.mul(f, axis=0).sum()


def fi_vat_accounting(m, flags=None, tau=TAU, inclusive=True):
    """The accounting tier on the Finnish model: tax_q = tau x VAT-able_q, dividend = sum_q w_q tax_q,
    net_q = dividend - tax_q (balanced under the model's weights)."""
    acc = net_from_base(fi_vat_base(m, flags, inclusive), m["w"], tau, m["budget"])
    acc = acc.rename(columns={"base": "vatable", "base_pct_budget": "vatable_pct_budget"})
    acc["Cbar_v"] = float((m["w"] * acc["vatable"]).sum())
    return acc


def fi_post_eur(m, x):
    """Rescale category euro amounts (a Series or DataFrame indexed by category) to the post's EUR conversion
    (Cbar from the total column). Identity for the coherent convention."""
    return x.mul(m["eur_scale"].reindex(x.index), axis=0)
