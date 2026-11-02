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
    another table) into monthly dollars per payment share, the unit every function here works in."""
    x = pd.Series(x_cu_annual, dtype=float).reindex(m["units"].index)
    return x / (m["units"]["shares"] * 12.0)


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
        mpc = mpc_mid(n) if mpc is None else np.asarray(mpc, dtype=float)
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
