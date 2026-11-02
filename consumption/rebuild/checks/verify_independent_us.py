"""Independent verification of the US rebuild (consumption/rebuild/NOTES_us.md taken as the specification).

Nothing here is imported or copied from consumption/rebuild/code/. The method is re-implemented from the post
(consumption/data/raw/post/post.txt) and from the judgment calls documented in NOTES_us.md, reading the RAW files:

  - BLS CE Table 1110 (deciles, 2024) and Table 2500 (all-CU detail, 2024): xlsx read with zipfile + xml.etree;
  - USDA ERS TB-1929 Tables 3 and 4 (Working/Florida-PI betas): read from the bulletin's PDF with pdfplumber.

The builder's outputs (out/us_*.csv, out/gate_us.csv) and the gate list (data/tidy/post_published_numbers.csv)
are read only to compare against. Every claim prints one line

    OK  | claim | builder | mine | published | note        (or BAD | ...)

OK means: my independent value agrees with the builder's value (within the stated numerical tolerance) AND the
builder's statement about it (its gate status, or the sentence in NOTES_us.md) is borne out by my value. BAD means
one of the two fails, or that a judgment call does not hold up on review (the note says why). A final count follows.
A CSV copy goes to out/verify_independent_us.csv; the headline sensitivity to alternative defensible choices (flags,
group mapping, food split, MPC shape, weights, nets), each with a Fig 5 MPC refit, to
out/verify_independent_us_sensitivity.csv.

Run from the repo root:  venv/bin/python -I consumption/rebuild/checks/verify_independent_us.py   (about 20 s)

Plain functions and top-level code, so the cells can be pasted into a notebook.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # house convention; nothing is imported from ../code

import re
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import pdfplumber
from scipy.optimize import brentq
from tqdm.auto import tqdm

CONS = HERE.parents[1]                      # consumption/
RAW_DEC = CONS / "data/raw/bls_ce/tables/deciles/cu-income-deciles-before-taxes-2024.xlsx"
RAW_DET = CONS / "data/raw/bls_ce/tables/detail/cu-all-detail-2024.xlsx"
RAW_PDF = CONS / "data/raw/usda/report/tb-1929.pdf"
GATE_LIST = CONS / "data/tidy/post_published_numbers.csv"
BOUT = CONS / "rebuild/out"                 # the builder's outputs (read only)
OUT_CSV = BOUT / "verify_independent_us.csv"

TAU = 0.15
CHILD_SHARE = 0.3
DEC = [f"d{i:02d}" for i in range(1, 11)]

# ----------------------------------------------------------------------------------------------------------
# 1. xlsx reader: zipfile + xml.etree only (shared strings, cell styles for the label indent and number format)
# ----------------------------------------------------------------------------------------------------------
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col_index(ref):
    n = 0
    for ch in re.match(r"([A-Z]+)", ref).group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx_cells(path):
    """Rows of the first sheet as (row number, {col: (value, indent, number format)})."""
    z = zipfile.ZipFile(path)
    sst = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            sst.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    st = ET.fromstring(z.read("xl/styles.xml"))
    fmts = {int(n.get("numFmtId")): n.get("formatCode") for n in st.findall("m:numFmts/m:numFmt", NS)}
    xfs = []
    for xf in st.findall("m:cellXfs/m:xf", NS):
        al = xf.find("m:alignment", NS)
        xfs.append((int(al.get("indent", 0)) if al is not None else 0, fmts.get(int(xf.get("numFmtId", 0)), "")))
    rows = []
    for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).findall("m:sheetData/m:row", NS):
        cells = {}
        for c in r.findall("m:c", NS):
            t, v = c.get("t"), c.find("m:v", NS)
            if t == "s":
                val = sst[int(v.text)] if v is not None else ""
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif t == "str":
                val = v.text if v is not None else ""
            else:
                val = float(v.text) if v is not None and v.text is not None else None
            indent, fmt = xfs[int(c.get("s", 0))]
            cells[col_index(c.get("r"))] = (val, indent, fmt)
        rows.append((int(r.get("r")), cells))
    return rows


def clean_label(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+\[[ID]\]$", "", s)          # Table 2500 survey-source tags
    s = re.sub(r"\s+[a-d]/$", "", s)            # footnote markers
    return s.strip()


def parse_ce_table(path, ncol):
    """{path: {'mean': [...], 'value': [...], 'flag': [...]}} with the hierarchy read from the label indents."""
    out, stack, cur = {}, [], None
    for _, cells in read_xlsx_cells(path):
        lab = cells.get(0, ("", 0, ""))
        if not isinstance(lab[0], str) or not lab[0].strip():
            continue
        text = clean_label(lab[0])
        vals = [cells.get(k, (None, 0, ""))[0] for k in range(1, ncol + 1)]
        flags = []
        for k in range(1, ncol + 1):
            v, _, fmt = cells.get(k, (None, 0, ""))
            if isinstance(v, str):
                flags.append(v.strip())
            elif "\\b\\/" in fmt:
                flags.append("b/")
            elif "\\c\\/" in fmt:
                flags.append("c/")
            else:
                flags.append("")
        if text in ("Mean", "Share", "SE", "RSE", "CV(%)") or text.lower().startswith("percent reporting"):
            if cur is not None and text == "Mean":
                out[cur]["mean"] = [v if isinstance(v, float) else (0.0 if f in ("c/", "d/") else np.nan)
                                    for v, f in zip(vals, flags)]
                out[cur]["flag"] = flags
            continue
        while stack and stack[-1][0] >= lab[1]:
            stack.pop()
        stack.append((lab[1], text))
        cur = " > ".join(t for _, t in stack)
        out[cur] = {"value": [v if isinstance(v, float) else np.nan for v in vals], "mean": None, "flag": flags}
    return out


T1110 = parse_ce_table(RAW_DEC, 11)           # column 0 = all CUs, 1..10 = deciles
T2500 = parse_ce_table(RAW_DET, 1)


def dec_mean(p):
    return np.array(T1110[p]["mean"][1:], dtype=float)


def dec_value(p):
    return np.array(T1110[p]["value"][1:], dtype=float)


def det(p):
    m = T2500[p]["mean"]
    return float(m[0]) if m is not None and np.isfinite(m[0]) else 0.0


AAE = "Average annual expenditures"
P = {  # the 40 budget categories: Fig 5's 36 bars + 4 off-chart rows (NOTES_us.md, "The method as rebuilt")
    "Food at home": f"{AAE} > Food > Food at home",
    "Food away from home": f"{AAE} > Food > Food away from home",
    "Alcoholic beverages": f"{AAE} > Alcoholic beverages",
    "Mortgage interest and charges": f"{AAE} > Housing > Shelter > Owned dwellings > Mortgage interest and charges",
    "Property taxes": f"{AAE} > Housing > Shelter > Owned dwellings > Property taxes",
    "Home maintenance, repairs & insurance":
        f"{AAE} > Housing > Shelter > Owned dwellings > Maintenance, repairs, insurance, and other expenses",
    "Rented dwellings": f"{AAE} > Housing > Shelter > Rented dwellings",
    "Other lodging": f"{AAE} > Housing > Shelter > Other lodging",
    "Natural gas": f"{AAE} > Housing > Utilities, fuels, and public services > Natural gas",
    "Electricity": f"{AAE} > Housing > Utilities, fuels, and public services > Electricity",
    "Fuel oil and other fuels": f"{AAE} > Housing > Utilities, fuels, and public services > Fuel oil and other fuels",
    "Telephone services": f"{AAE} > Housing > Utilities, fuels, and public services > Telephone services",
    "Water and other public services":
        f"{AAE} > Housing > Utilities, fuels, and public services > Water and other public services",
    "Personal services (incl. childcare)": f"{AAE} > Housing > Household operations > Personal services",
    "Other household expenses": f"{AAE} > Housing > Household operations > Other household expenses",
    "Housekeeping supplies": f"{AAE} > Housing > Housekeeping supplies",
    "Household furnishings & equipment": f"{AAE} > Housing > Household furnishings and equipment",
    "Apparel and services": f"{AAE} > Apparel and services",
    "Cars and trucks, new": f"{AAE} > Transportation > Vehicle purchases (net outlay) > Cars and trucks, new",
    "Cars and trucks, used": f"{AAE} > Transportation > Vehicle purchases (net outlay) > Cars and trucks, used",
    "Other vehicles (residual)": None,  # parent minus new minus used (BLS dropped 'Other vehicles' in 2024)
    "Gasoline and other fuels": f"{AAE} > Transportation > Gasoline and other fuels",
    "Vehicle finance charges": f"{AAE} > Transportation > Other vehicle expenses > Vehicle finance charges",
    "Vehicle maintenance and repairs": f"{AAE} > Transportation > Other vehicle expenses > Maintenance and repairs",
    "Vehicle rental, leases, licenses":
        f"{AAE} > Transportation > Other vehicle expenses > Vehicle rental, leases, licenses, and other charges",
    "Vehicle insurance": f"{AAE} > Transportation > Other vehicle expenses > Vehicle insurance",
    "Public and other transportation": f"{AAE} > Transportation > Public and other transportation",
    "Health insurance": f"{AAE} > Healthcare > Health insurance",
    "Medical services": f"{AAE} > Healthcare > Medical services",
    "Drugs": f"{AAE} > Healthcare > Drugs",
    "Medical supplies": f"{AAE} > Healthcare > Medical supplies",
    "Fees and admissions": f"{AAE} > Entertainment > Fees and admissions",
    "Audio & visual equipment and services": f"{AAE} > Entertainment > Audio and visual equipment and services",
    "Pets, toys, hobbies": f"{AAE} > Entertainment > Pets, toys, hobbies, and playground equipment",
    "Other entertainment equipment": f"{AAE} > Entertainment > Other entertainment supplies, equipment, and services",
    "Personal care products and services": f"{AAE} > Personal care products and services",
    "Reading": f"{AAE} > Reading",
    "Education": f"{AAE} > Education",
    "Tobacco products": f"{AAE} > Tobacco products and smoking supplies",
    "Miscellaneous": f"{AAE} > Miscellaneous",
}
CATS = list(P)
OFFCHART = ["Mortgage interest and charges", "Property taxes", "Education", "Other vehicles (residual)"]
CHART = [c for c in CATS if c not in OFFCHART]
VP = f"{AAE} > Transportation > Vehicle purchases (net outlay)"

annual = {}
for c in CATS:
    if P[c] is None:
        annual[c] = dec_mean(VP) - dec_mean(P["Cars and trucks, new"]) - dec_mean(P["Cars and trucks, used"])
    else:
        annual[c] = dec_mean(P[c])
A = np.vstack([annual[c] for c in CATS])                 # 40 x 10, dollars per CU per year
TOTAL = dec_mean(AAE)
CASH = dec_mean(f"{AAE} > Cash contributions")
PIP = dec_mean(f"{AAE} > Personal insurance and pensions")
NCU = dec_value("Number of consumer units (in thousands)")
PEOPLE = dec_value("Consumer unit characteristics: > Average number in consumer unit: > People")
KIDS = dec_value("Consumer unit characteristics: > Average number in consumer unit: > Children under 18")
RENTER = dec_value("Percent distribution: > Housing tenure: > Renter")
HIGH_RSE = {c: [d for d, f in zip(DEC, T1110[P[c]]["flag"][1:]) if f == "b/"] if P[c] else [] for c in CATS}

# ----------------------------------------------------------------------------------------------------------
# 2. Payment units, weights, per-share monthly spending (NOTES_us.md: footnote 26 payment units)
# ----------------------------------------------------------------------------------------------------------
ADULTS = PEOPLE - KIDS
SHARES = ADULTS + CHILD_SHARE * KIDS
W = NCU * SHARES / (NCU * SHARES).sum()                  # population weight of a payment share in decile d


def per_share_month(x, shares=None):
    return np.asarray(x, dtype=float) / 12.0 / (SHARES if shares is None else shares)


C = per_share_month(A)                                   # 40 x 10, $ per share per month
BUDGET = C.sum(0)                                        # C_d
CBAR = C @ W                                             # Cbar_g
IX = {c: i for i, c in enumerate(CATS)}

# ----------------------------------------------------------------------------------------------------------
# 3. VAT flags. Mixed lines from the 2024 Table 2500 composition, recomputed here from the raw children;
#    the child lists encode the Directive reading stated in NOTES_us.md / out/us_flags.csv.
# ----------------------------------------------------------------------------------------------------------
OD = f"{AAE} > Housing > Shelter > Owned dwellings > Maintenance, repairs, insurance, and other expenses"
RD = f"{AAE} > Housing > Shelter > Rented dwellings"
OL = f"{AAE} > Housing > Shelter > Other lodging"
OVH = f"{OL} > Owned vacation homes > Maintenance, insurance, and other expenses"
WA = f"{AAE} > Housing > Utilities, fuels, and public services > Water and other public services"
HK = f"{AAE} > Housing > Housekeeping supplies"
VR = f"{AAE} > Transportation > Other vehicle expenses > Vehicle rental, leases, licenses, and other charges"
MI = f"{AAE} > Miscellaneous"
ED = f"{AAE} > Education"
OH = f"{AAE} > Housing > Household operations > Other household expenses"
FA = f"{AAE} > Entertainment > Fees and admissions"
DR = f"{AAE} > Healthcare > Drugs"
PT = f"{AAE} > Transportation > Public and other transportation"


def share_of(parent, taxable_children):
    return sum(det(f"{parent} > {k}") for k in taxable_children) / det(parent)


MIXED = {
    "Home maintenance, repairs & insurance": share_of(OD, [
        "Maintenance and repair services", "Maintenance and repair commodities",
        "Property management and security", "Parking"]),            # out: homeowners insurance, ground rent
    "Rented dwellings": share_of(RD, [
        "Maintenance, insurance, and other expenses > Maintenance and repair services",
        "Maintenance, insurance, and other expenses > Maintenance and repair commodities"]),
    "Other lodging": (det(f"{OL} > Lodging on out of town trips") + sum(det(f"{OVH} > {k}") for k in [
        "Maintenance and repair services", "Maintenance and repair commodities",
        "Property management and security", "Parking"])) / det(OL),
    "Water and other public services": share_of(WA, ["Water and sewerage maintenance", "Septic tank cleaning"]),
    "Housekeeping supplies": 1 - det(f"{HK} > Postage and stationery > Postage") / det(HK),
    "Vehicle rental, leases, licenses": share_of(VR, [
        "Leased and rented vehicles", "Parking fees", "Tolls or electronic toll passes",
        "Tolls on out of town trips", "Towing charges", "Automobile service clubs and GPS services"]),
    "Miscellaneous": share_of(MI, [
        "Miscellaneous fees", "Legal fees", "Funeral expenses", "Safe deposit box rental", "Accounting fees",
        "Miscellaneous personal services", "Dating services", "Shopping club membership fees", "Vacation clubs"]),
    "Education": share_of(ED, ["Educational books, supplies, and other expenditures",
                               "School supplies, etc., unspecified"]),
}
EXEMPT = ["Mortgage interest and charges", "Property taxes", "Vehicle finance charges", "Vehicle insurance",
          "Health insurance", "Medical services", "Personal services (incl. childcare)"]
SPEC_FLAGS = {c: (MIXED[c] if c in MIXED else 0.0 if c in EXEMPT else 1.0) for c in CATS}
SPEC_FLAGS["Cars and trucks, used"] = 0.5          # calibrated (NOTES_us.md: pinned by Fig 4)


def flag_vector(flags):
    return np.array([flags[c] for c in CATS])


# ----------------------------------------------------------------------------------------------------------
# 4. Accounting tier: net_d = tau (Cbar_v - C_v,d), balanced over payment shares
# ----------------------------------------------------------------------------------------------------------
def accounting(flags, C=C, W=W, tau=TAU):
    f = flag_vector(flags) if isinstance(flags, dict) else np.asarray(flags)
    cv = f @ C
    budget = C.sum(0)
    cbar_v = cv @ W
    net = tau * (cbar_v - cv)
    return {"cv": cv, "budget": budget, "cbar_v": cbar_v, "dividend": tau * cbar_v, "net": net,
            "net_pct": 100 * net / budget, "vat_share": 100 * cv / budget,
            "agg_vat_share": 100 * cbar_v / (budget @ W), "balance": net @ W}


ACC = accounting(SPEC_FLAGS)

# ----------------------------------------------------------------------------------------------------------
# 5. TB-1929 parameters from the bulletin's PDF (Table 3: printed p. 12 = PDF p. 18; Table 4: p. 16 = PDF p. 22)
# ----------------------------------------------------------------------------------------------------------
def tb1929_tables(path):
    with pdfplumber.open(path) as pdf:
        t3 = pdf.pages[17].extract_text()
        t4 = pdf.pages[21].extract_text()
    num = r"(-?\d*\.\d+)"

    def block(text, start, stop, names):
        seg = text[text.index(start):text.index(stop, text.index(start))]
        vals = {}
        for nm in names:
            m = re.search(re.escape(nm) + r"\s+" + num + r"\s+" + num, seg)
            vals[nm] = float(m.group(1))
        return vals

    g9 = ["Food, beverage, and tobacco", "Clothing and footwear", "Housing and utilities",
          "Furnishing, household equipment, and maintenance", "Medical and health",
          "Transportation and communication", "Recreation and culture", "Education", "Other"]
    s8 = ["Cereals", "Meat", "Fish", "Dairy and eggs", "Oils and fat", "Fruit and vegetables", "Food other",
          "Beverages and tobacco"]
    assert "Table 3" in t3 and "Table 4" in t4
    return {"beta": block(t3, "Beta", "Alpha", g9), "alpha": block(t3, "Alpha", "Heteroskedasticity", g9),
            "beta_star": block(t4, "Beta", "Alpha", s8), "alpha_star": block(t4, "Alpha", "Slutsky", s8),
            "phi": float(re.search(r"Income flexibility φ\s+" + num, t3).group(1))}


TB = tb1929_tables(RAW_PDF)
GROUP_OF = {  # stage-one mapping (NOTES_us.md: CE major categories, telephone in transport & communication)
    "food": ["Food at home", "Food away from home", "Alcoholic beverages", "Tobacco products"],
    "clothing": ["Apparel and services"],
    "housing": ["Mortgage interest and charges", "Property taxes", "Home maintenance, repairs & insurance",
                "Rented dwellings", "Other lodging", "Natural gas", "Electricity", "Fuel oil and other fuels",
                "Water and other public services"],
    "furnishings": ["Personal services (incl. childcare)", "Other household expenses", "Housekeeping supplies",
                    "Household furnishings & equipment"],
    "medical": ["Health insurance", "Medical services", "Drugs", "Medical supplies"],
    "transport": ["Telephone services", "Cars and trucks, new", "Cars and trucks, used", "Other vehicles (residual)",
                  "Gasoline and other fuels", "Vehicle finance charges", "Vehicle maintenance and repairs",
                  "Vehicle rental, leases, licenses", "Vehicle insurance", "Public and other transportation"],
    "recreation": ["Fees and admissions", "Audio & visual equipment and services", "Pets, toys, hobbies",
                   "Other entertainment equipment", "Reading"],
    "education": ["Education"],
    "other": ["Personal care products and services", "Miscellaneous"],
}
TBNAME = {"food": "Food, beverage, and tobacco", "clothing": "Clothing and footwear",
          "housing": "Housing and utilities", "furnishings": "Furnishing, household equipment, and maintenance",
          "medical": "Medical and health", "transport": "Transportation and communication",
          "recreation": "Recreation and culture", "education": "Education", "other": "Other"}
SIX = ["Cereals", "Meat", "Fish", "Dairy and eggs", "Oils and fat", "Fruit and vegetables"]
FOOD_CLASS = {  # food split A (NOTES_us.md)
    "at_home": (["Food at home"], sum(TB["beta_star"][s] for s in SIX)),
    "away": (["Food away from home"], TB["beta_star"]["Food other"]),
    "bev_tob": (["Alcoholic beverages", "Tobacco products"], TB["beta_star"]["Beverages and tobacco"]),
}

# ----------------------------------------------------------------------------------------------------------
# 6. Elasticities: TB-1929 eq. 5 at observed decile shares; food through eq. 11 (split A)
# ----------------------------------------------------------------------------------------------------------
def elasticities(C=C, group_of=GROUP_OF, food_class=FOOD_CLASS, beta=None):
    beta = TB["beta"] if beta is None else beta
    budget = C.sum(0)
    eta = np.full(C.shape, np.nan)
    wk = {}
    for k, cats in group_of.items():
        wk[k] = C[[IX[c] for c in cats]].sum(0) / budget
        if k != "food":
            for c in cats:
                eta[IX[c]] = 1 + beta[TBNAME[k]] / wk[k]
    food_cats = group_of["food"]
    food_spend = C[[IX[c] for c in food_cats]].sum(0)
    eta_f = 1 + beta[TBNAME["food"]] / wk["food"]
    for cls, (cats, bstar) in food_class.items():
        wstar = C[[IX[c] for c in cats]].sum(0) / food_spend
        for c in cats:
            eta[IX[c]] = eta_f * (1 + bstar / wstar)
    assert np.isfinite(eta).all()
    return eta, wk, eta_f


ETA, WK, ETA_F = elasticities()

# ----------------------------------------------------------------------------------------------------------
# 7. Demand tier: shock_d = mpc_d net_d / C_d; dPct_g = sum_d theta_dg eta_gd shock_d; dUSD_g = dPct_g Cbar_g
# ----------------------------------------------------------------------------------------------------------
def shifts(net, mpc, C=C, W=W, eta=None):
    eta = ETA if eta is None else eta
    budget = C.sum(0)
    shock = np.asarray(mpc) * np.asarray(net) / budget
    contrib = (W * C) * eta * shock                       # c_dg = w_d C_gd eta_gd shock_d  (Fig 6 segments)
    usd = contrib.sum(1)
    cbar = C @ W
    theta = (W * C) / cbar[:, None]
    pct = 100 * (theta * eta * shock).sum(1)              # identical to 100 usd / cbar
    return {"usd": usd, "pct": pct, "contrib": contrib, "flow": (W * np.asarray(mpc) * np.asarray(net)).sum(),
            "consumption": budget @ W}


def mpc_knee(knee, top):
    d = np.arange(1, 11, dtype=float)
    return np.where(d <= knee, 1.0, 1.0 - (1.0 - top) * (d - knee) / (10.0 - knee))


MPC_SPEC = {"low": mpc_knee(1.93, 0.40), "mid": mpc_knee(2.55, 0.53), "high": mpc_knee(3.29, 0.65)}

# ----------------------------------------------------------------------------------------------------------
# 8. The published numbers (gate list) and the builder's outputs
# ----------------------------------------------------------------------------------------------------------
GL = pd.read_csv(GATE_LIST)
GATE = pd.read_csv(BOUT / "gate_us.csv")
B_ACC = pd.read_csv(BOUT / "us_accounting_by_decile.csv").set_index("decile")
B_SH = pd.read_csv(BOUT / "us_demand_shifts.csv").set_index("category")
B_DEC = pd.read_csv(BOUT / "us_decomposition_top10.csv")
B_ETA = pd.read_csv(BOUT / "us_eta.csv")
B_FLAGS = pd.read_csv(BOUT / "us_flags.csv").set_index("category")
B_IMP = pd.read_csv(BOUT / "us_impulse.csv")
B_MPCP = pd.read_csv(BOUT / "us_mpc_params.csv")
B_MPCS = pd.read_csv(BOUT / "us_mpc_schedules.csv").set_index("decile")
B_BUD = pd.read_csv(BOUT / "us_budget_tests.csv")
B_SENS = pd.read_csv(BOUT / "us_sensitivity.csv").set_index("variant")
B_MAP = pd.read_csv(BOUT / "us_mapping_tests.csv")
B_FS = pd.read_csv(BOUT / "us_flags_search.csv")


def pub(pid):
    return float(GL.loc[GL.id == pid, "value"].iloc[0])


F5 = GL[GL.source == "fig5_demand_shifts_us2024_mpc.png"]
F5_USD = F5[F5.quantity.str.startswith("change in spending")].set_index("item")["value"]
F5_PCT = F5[F5.quantity.str.startswith("percent change")].set_index("item")["value"]
F5_GHOST = F5[F5.quantity.str.startswith("MPC=1 benchmark")].set_index("item")["value"]
assert len(F5_USD) == len(F5_PCT) == len(F5_GHOST) == 36 and set(F5_USD.index) == set(CHART)
F6 = GL[GL.source == "fig6_composition_us2024_mpc-1.png"]
F6_SEG = F6[F6.quantity.str.startswith("decile contribution")].copy()
F6_SEG["d"] = F6_SEG.group.str.replace("US D", "", regex=False).astype(int)
F6_NET = F6[F6.quantity.str.startswith("change in spending")].set_index("item")["value"]
F6_GHOST = F6[F6.quantity.str.startswith("MPC=1 benchmark")].set_index("item")["value"]
F4 = GL[GL.source == "fig4_net_transfer_us2024-1.png"]
F4_LABEL = F4[F4.quantity == "net transfer per adult share per month"].copy()
F4_LABEL["d"] = F4_LABEL.group.str.replace("US D", "", regex=False).astype(int)
F4_LABEL = F4_LABEL.set_index("d")["value"].sort_index()
F4_X = F4[F4.quantity.str.startswith("VAT-able consumption per adult share")].copy()
F4_X["d"] = F4_X.group.str.replace("US D", "", regex=False).astype(int)
F4_X = F4_X.set_index("d")["value"].sort_index()
CHART_IDX = [IX[c] for c in CHART]
PUB_USD = np.array([F5_USD[c] for c in CHART])

# ----------------------------------------------------------------------------------------------------------
# 9. MPC calibration, redone: least squares of the 36 Fig 5 dollar bars over the knee family
# ----------------------------------------------------------------------------------------------------------
NET = ACC["net"]
M36 = ((W * C) * ETA * (NET / BUDGET))[CHART_IDX]          # bars = M36 @ mpc (linear in the schedule)
KNEES = np.round(np.arange(1.0, 6.0001, 0.01), 2)
TOPS = np.round(np.arange(0.30, 0.80001, 0.0025), 4)
rmse_grid = np.empty((len(KNEES), len(TOPS)))
for i, kn in enumerate(tqdm(KNEES, desc="MPC knee grid", leave=False)):
    mp = np.array([mpc_knee(kn, tp) for tp in TOPS])       # len(TOPS) x 10
    rmse_grid[i] = np.sqrt((((mp @ M36.T) - PUB_USD) ** 2).mean(1))
i0, j0 = np.unravel_index(np.argmin(rmse_grid), rmse_grid.shape)
FIT_KNEE, FIT_TOP, FIT_RMSE = KNEES[i0], TOPS[j0], rmse_grid[i0, j0]
INT_KNEE_BEST = {k: (TOPS[np.argmin(rmse_grid[KNEES == k][0])], rmse_grid[KNEES == k][0].min()) for k in (1, 2, 3, 4, 5)}


def refit_mpc(net, eta=None, Cm=None, Wm=None):
    """Least-squares (knee, top) on the 36 Fig 5 dollar bars for a given net vector: (rmse, knee, top)."""
    Cm, Wm, eta = (C if Cm is None else Cm), (W if Wm is None else Wm), (ETA if eta is None else eta)
    Mv = ((Wm * Cm) * eta * (np.asarray(net) / Cm.sum(0)))[CHART_IDX]
    best_ = (np.inf, None, None)
    for kn in KNEES:
        mp = np.array([mpc_knee(kn, tp) for tp in TOPS])
        e = np.sqrt((((mp @ Mv.T) - PUB_USD) ** 2).mean(1))
        j = int(np.argmin(e))
        if e[j] < best_[0]:
            best_ = (float(e[j]), float(kn), float(TOPS[j]))
    return best_


def flow_pct(mpc, net=NET):
    return 100 * (W * mpc * net).sum() / (BUDGET @ W)


KNEE_LOW = brentq(lambda k: flow_pct(mpc_knee(k, 0.40)) - pub("P538"), 1.0, 6.0)
KNEE_HIGH = brentq(lambda k: flow_pct(mpc_knee(k, 0.65)) - pub("P539"), 1.0, 6.0)

# ----------------------------------------------------------------------------------------------------------
# 10. A whole-model wrapper so every alternative is one call (generic in the net vector, as the LVT step needs)
# ----------------------------------------------------------------------------------------------------------
def model(flags=SPEC_FLAGS, people=PEOPLE, kids=KIDS, ncu=NCU, group_of=GROUP_OF, food_class=FOOD_CLASS,
          equal_cu=False, net=None, mpc=None, eta_fn=None):
    shares = (people - kids) + CHILD_SHARE * kids
    w = (np.ones(10) if equal_cu else ncu) * shares
    w = w / w.sum()
    Cm = A / 12.0 / shares
    acc = accounting(flags, C=Cm, W=w)
    eta = (eta_fn or elasticities)(C=Cm, group_of=group_of, food_class=food_class)[0]
    n = acc["net"] if net is None else np.asarray(net, dtype=float)
    m = MPC_SPEC["mid"] if mpc is None else mpc
    s = shifts(n, m, C=Cm, W=w, eta=eta)
    s1 = shifts(n, np.ones(10), C=Cm, W=w, eta=eta)
    return {"acc": acc, "eta": eta, "s": s, "s1": s1, "C": Cm, "W": w, "net": n, "mpc": m}


def headlines(r):
    a, s, s1 = r["acc"], r["s"], r["s1"]
    u, u1 = s["usd"], s1["usd"]
    gain = int((r["net"] > 0).sum())
    chart_sum = u[CHART_IDX].sum()
    charted_budget = r["C"][CHART_IDX].sum(0) @ r["W"]
    return {"dividend": a["dividend"], "D1 net": a["net"][0], "D1 %": a["net_pct"][0], "D10 net": a["net"][9],
            "D10 %": a["net_pct"][9], "gaining deciles": gain, "VAT-able min %": a["vat_share"].min(),
            "VAT-able max %": a["vat_share"].max(), "rent": u[IX["Rented dwellings"]],
            "health ins": u[IX["Health insurance"]], "vehicle ins": u[IX["Vehicle insurance"]],
            "new cars": u[IX["Cars and trucks, new"]], "new cars ghost": u1[IX["Cars and trucks, new"]],
            "used cars": u[IX["Cars and trucks, used"]], "used cars ghost": u1[IX["Cars and trucks, used"]],
            "fees": u[IX["Fees and admissions"]], "lodging": u[IX["Other lodging"]],
            "impulse % cons": 100 * s["flow"] / s["consumption"], "bars/charted %": 100 * chart_sum / charted_budget,
            "largest mover": CHART[int(np.argmax(np.abs(u[CHART_IDX])))]}


HEAD_PUB = {"dividend": (249, 0.5), "D1 net": (88, 0.5), "D1 %": (4.8, 0.05), "D10 net": (-173, 0.5),
            "D10 %": (-3.9, 0.05), "gaining deciles": (7, 0), "VAT-able min %": (59, 0.5), "VAT-able max %": (64, 0.5),
            "rent": (3.36, 0.005), "health ins": (1.08, 0.005), "vehicle ins": (0.53, 0.005), "new cars": (-0.39, 0.005),
            "new cars ghost": (-1.23, 0.005), "used cars": (0.38, 0.005), "used cars ghost": (-0.05, 0.01),
            "fees": (-0.20, 0.005), "lodging": (-0.13, 0.005)}


def broken_headlines(h):
    return [k for k, (v, t) in HEAD_PUB.items() if abs(h[k] - v) > t + 1e-9]


def qualitative_ok(h):
    """The post's qualitative US statements: 7 deciles gain, rent the largest mover, new cars down and used cars up
    (ghost of used cars negative), both insurances up, fees and lodging down, impulse positive."""
    return (h["gaining deciles"] == 7 and h["largest mover"] == "Rented dwellings" and h["new cars"] < 0
            < h["used cars"] and h["used cars ghost"] < 0 and h["health ins"] > 0 and h["vehicle ins"] > 0
            and h["fees"] < 0 and h["lodging"] < 0 and h["impulse % cons"] > 0)


BASE = model()
HBASE = headlines(BASE)

# ----------------------------------------------------------------------------------------------------------
# 11. The claims engine
# ----------------------------------------------------------------------------------------------------------
CLAIMS = []


def fv(x):
    if x is None:
        return ""
    if isinstance(x, (bool, np.bool_)):
        return "yes" if x else "no"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        if not np.isfinite(x):
            return "nan"
        return f"{x:.4f}".rstrip("0").rstrip(".") if abs(x) < 1000 else f"{x:.1f}"
    return str(x)


def claim(ok, text, builder=None, mine=None, published=None, note="", area=""):
    CLAIMS.append({"status": "OK" if ok else "BAD", "area": area, "claim": text, "builder": fv(builder),
                   "mine": fv(mine), "published": fv(published), "note": note})


def close(a, b, tol):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol + 1e-12


def num_tokens(s):
    return re.findall(r"[-+]?\d+(?:\.\d+)?", str(s).replace("−", "-").replace(",", ""))


def my_tol(row):
    """Half a unit of the last printed digit (printed numbers); the note's +/- precision (read-offs)."""
    if str(row["confidence"]) == "high" and isinstance(row["printed"], str) and row["printed"].strip():
        v = abs(float(row["value"]))
        for t in num_tokens(row["printed"]):
            if abs(abs(float(t)) - v) < 1e-9:
                return 0.5 * 10 ** (-(len(t.split(".")[1]) if "." in t else 0))
        return 5.0 if row["unit"] == "%" else 0.0           # fraction or count words
    mt = re.search(r"±\s*([0-9.]+)", str(row["note"]))
    if mt:
        return float(mt.group(1))
    return 5.0 if row["unit"] == "USD" else 0.01


def my_status(value, row):
    pubv, tol = float(row["value"]), my_tol(row)
    gap = value - pubv
    if tol == 0:
        return "PASS" if abs(gap) < 1e-9 else "MISS"
    if abs(gap) <= tol + 1e-9:
        return "PASS"
    if abs(gap) <= 0.10 * abs(pubv) or (row["unit"] == "USD" and abs(gap) <= 0.05):
        return "CLOSE"
    return "MISS"

# ----------------------------------------------------------------------------------------------------------
# 12. Claims: inputs read from the raw files
# ----------------------------------------------------------------------------------------------------------
AR = "inputs"
b = B_ACC.loc[DEC]
claim(np.allclose(SHARES, b.payment_shares.values, atol=1e-9) and np.allclose(ADULTS, b.adults.values),
      "payment shares = (People - Children) + 0.3 Children, Table 1110 printed rows (fn 26)",
      f"{b.payment_shares.min():.2f}..{b.payment_shares.max():.2f}", f"{SHARES.min():.2f}..{SHARES.max():.2f}", None,
      "identical in all 10 deciles", AR)
claim(np.allclose(W, b.w_share_weight.values, atol=6e-5), "population weight w_d = N_d shares_d / sum",
      b.w_share_weight.values[0], W[0], None, f"max |diff| {np.abs(W - b.w_share_weight.values).max():.1e} (file keeps 4 dp)", AR)
claim(np.allclose(BUDGET, b.budget_usd_month.values, atol=6e-4), "budget C_d = sum of the 40 categories, $/share-month",
      b.budget_usd_month.values[9], BUDGET[9], None,
      f"max |diff| {np.abs(BUDGET - b.budget_usd_month.values).max():.1e}; 40 lines = total - personal insurance and "
      f"pensions - cash contributions within ${np.abs(A.sum(0) - (TOTAL - CASH - PIP)).max():.0f}/CU-yr (rounding)", AR)
bc = B_FLAGS.loc[CATS, "Cbar_usd_month"].values
claim(np.allclose(CBAR, bc, atol=6e-5), "category means Cbar_g (40 lines)", bc.sum(), CBAR.sum(), None,
      f"max |diff| {np.abs(CBAR - bc).max():.1e}", AR)
resid_all = T1110[VP]["mean"][0] - T1110[P['Cars and trucks, new']]["mean"][0] - T1110[P['Cars and trucks, used']]["mean"][0]
claim(abs(resid_all - 50) < 0.5, "vehicle-purchase residual (no 'Other vehicles' row in 2024) is $50 a CU a year", 50, resid_all,
      None, "all-CU column; off-chart, flagged taxable", AR)
n_rse_chart = sum(len(HIGH_RSE[c]) for c in CHART)
n_rse_edu = len(HIGH_RSE["Education"])
claim(n_rse_chart == 27 and n_rse_edu == 2, "high-RSE (b/) cells used as printed: 27 charted (29 with education's 2)",
      "27 / 29", f"{n_rse_chart} / {n_rse_chart + n_rse_edu}", None,
      "decoded from the cells' number formats in the raw xlsx", AR)
be = B_ETA.drop_duplicates("category").set_index("category")
ok_beta = all(abs(be.loc[c, "beta_stage1"] - TB["beta"][TBNAME[k]]) < 1e-9 for k, cs in GROUP_OF.items() for c in cs)
# us_eta.csv apportions the B&T beta* between alcohol and tobacco by within-class spending (same single eta), so the
# class sums are compared per decile
bstar_cls = B_ETA.assign(cls=B_ETA.category.map({c: cl for cl in FOOD_CLASS for c in FOOD_CLASS[cl][0]})).dropna(
    subset=["cls"]).groupby(["cls", "decile"]).beta_star.sum()
ok_bstar = all(abs(v - FOOD_CLASS[cl][1]) < 2e-5 for (cl, _), v in bstar_cls.items())
claim(ok_beta and ok_bstar and abs(sum(TB["beta"].values())) < 1e-9 and abs(sum(TB["beta_star"].values()) - 0.001) < 1e-9,
      "TB-1929 betas (Table 3) and beta* (Table 4) as used, read from the PDF with pdfplumber",
      "food -0.108 ... other +0.030; at-home -0.138, Food other +0.088, B&T +0.051",
      f"food {TB['beta']['Food, beverage, and tobacco']:+.3f} ... other {TB['beta']['Other']:+.3f}; at-home "
      f"{FOOD_CLASS['at_home'][1]:+.3f}, Food other {FOOD_CLASS['away'][1]:+.3f}, B&T {FOOD_CLASS['bev_tob'][1]:+.3f}",
      None, "stage-one betas sum to 0.000, stage-two to +0.001, as printed", AR)
beta_piv = B_ETA.pivot(index="category", columns="decile", values="eta").loc[CATS, DEC].values
claim(np.allclose(beta_piv, ETA, atol=2e-5), "elasticities eta_gd = 1 + beta_k/w_kd (eq. 5), food eta_F (1 + beta*_s/w*_s) "
      "(eq. 11), 40 lines x 10 deciles", f"{np.nanmin(beta_piv):.3f}..{np.nanmax(beta_piv):.3f}",
      f"{ETA.min():.3f}..{ETA.max():.3f}", None, f"max |diff| {np.abs(beta_piv - ETA).max():.1e} (file keeps 5 dp)", AR)
for c in MIXED:
    claim(abs(MIXED[c] - B_FLAGS.loc[c, "vat_flag"]) < 6e-5, f"VAT flag of mixed line '{c}' from Table 2500 2024",
          B_FLAGS.loc[c, "vat_flag"], MIXED[c], None, "builder rounds the share to 4 dp (moves the dividend by $0.0004)", AR)
other_flags_ok = all(abs(SPEC_FLAGS[c] - B_FLAGS.loc[c, "vat_flag"]) < 1e-9 for c in CATS if c not in MIXED)
claim(other_flags_ok, "VAT flags of the 32 other lines (0, 1, or used cars 1/2)", "as us_flags.csv", "same", None, "", AR)

# ----------------------------------------------------------------------------------------------------------
# 13. Claims: every gated row of out/gate_us.csv, recomputed (value and PASS/CLOSE/MISS)
# ----------------------------------------------------------------------------------------------------------
MID, LOW, HIGH = MPC_SPEC["mid"], MPC_SPEC["low"], MPC_SPEC["high"]
S_MID, S_ONE = BASE["s"], BASE["s1"]
U_MID, U_ONE, PCT_MID = S_MID["usd"], S_ONE["usd"], S_MID["pct"]
CONTRIB = S_MID["contrib"]
CONS_TOT = S_MID["consumption"]
CHARTED_BUDGET = C[CHART_IDX].sum(0) @ W
CHART_SUM = U_MID[CHART_IDX].sum()
FLOW = {k: (W * MPC_SPEC[k] * NET).sum() for k in MPC_SPEC}
FLOWPCT = {k: 100 * FLOW[k] / CONS_TOT for k in MPC_SPEC}
VSHARE = ACC["cbar_v"] / CONS_TOT
PRICE = {p: 100 * TAU * VSHARE * p for p in (0.8, 0.9, 1.0)}


def weighted_mpc(mpc, mask):
    a = (W * np.abs(NET))[mask]
    return float((mpc[mask] * a).sum() / a.sum())


RENT_ADD = np.clip(CONTRIB[IX["Rented dwellings"]], 0, None)
RENT_BULK_K = int(np.argmax(np.cumsum(RENT_ADD) > 0.5 * RENT_ADD.sum()) + 1)
TEXT_CAT = {"P279": "Rented dwellings", "P280": "Cars and trucks, new", "P281": "Cars and trucks, new",
            "P282": "Cars and trucks, used", "P283": "Cars and trucks, used", "P284": "Health insurance",
            "P285": "Vehicle insurance", "P286": "Fees and admissions", "P287": "Other lodging"}
FIXED = {
    "P273": ACC["dividend"], "P274": int((NET > 0).sum()), "P275": int(np.where(NET > 0)[0].max() + 1),
    "P276": int(np.where(NET < 0)[0].min() + 1), "P277": NET[9], "P278": ACC["net_pct"][9],
    "P324": ACC["vat_share"].min(), "P325": ACC["vat_share"].max(), "P438": 100 * CHART_SUM / CHARTED_BUDGET,
    "P439": RENTER[0], "P440": RENTER[9], "P441": RENT_BULK_K, "P496": 100 * VSHARE,
    "P497": PRICE[0.8], "P498": PRICE[1.0], "P500": PRICE[0.8] / 3, "P501": PRICE[1.0] / 3, "P506": PRICE[1.0],
    "P562": PRICE[0.8], "P563": PRICE[1.0], "P564": PRICE[0.8] / 3, "P565": PRICE[1.0] / 3,
    "P566": FLOWPCT["high"], "P567": FLOWPCT["low"], "P662": FLOWPCT["mid"],
    "P916": MID[0], "P917": LOW[9], "P918": HIGH[9],
    "P513": PRICE[0.8] / 3, "P514": PRICE[1.0] / 3, "P516": PRICE[0.9], "P517": PRICE[1.0], "P518": PRICE[0.8],
    "P534": 100 * weighted_mpc(MID, NET > 0), "P535": 100 * weighted_mpc(LOW, NET < 0),
    "P536": 100 * weighted_mpc(HIGH, NET < 0), "P537": FLOWPCT["mid"], "P538": FLOWPCT["low"],
    "P539": FLOWPCT["high"], "P290": ACC["dividend"], "P315": ACC["cbar_v"], "P436": 100 * CHART_SUM / CONS_TOT,
}


def mine_for(row):
    i, q, it, grp = row["id"], str(row["quantity"]), str(row["item"]), str(row["group"])
    if i in FIXED:
        return FIXED[i]
    if i in TEXT_CAT:
        return (U_ONE if q.startswith("MPC=1") else U_MID)[IX[TEXT_CAT[i]]]
    k = int(grp.replace("US D", "")) - 1 if grp.startswith("US D") and grp[4:].isdigit() else None
    if row["source"] == "fig4_net_transfer_us2024-1.png":
        if q == "net transfer per adult share per month":
            return NET[k]
        if q == "net transfer as % of budget":
            return ACC["net_pct"][k]
        if q.startswith("VAT-able consumption per adult share"):
            return ACC["cv"][k]
    if row["source"] in ("fig5_demand_shifts_us2024_mpc.png", "fig6_composition_us2024_mpc-1.png") and it in IX:
        if q.startswith("change in spending"):
            return U_MID[IX[it]]
        if q.startswith("percent change"):
            return PCT_MID[IX[it]]
        if q.startswith("MPC=1 benchmark"):
            return U_ONE[IX[it]]
        if q.startswith("decile contribution"):
            return CONTRIB[IX[it], k]
    raise KeyError(f"no mapping for gated row {i}: {q} / {it} / {grp}")


GROWS = GATE[GATE.status.isin(["PASS", "CLOSE", "MISS"])].copy()
gl_by_id = GL.set_index("id")
GROWS["mine"] = [mine_for(gl_by_id.loc[i].to_dict() | {"id": i}) for i in GROWS.id]
GROWS["mine_status"] = [my_status(v, gl_by_id.loc[i].to_dict()) for v, i in zip(GROWS.mine, GROWS.id)]
GROWS["my_tol"] = [my_tol(gl_by_id.loc[i].to_dict()) for i in GROWS.id]
for _, r in GROWS.iterrows():
    agree = abs(r.mine - r.rebuilt) <= max(0.0025, 2e-5 * abs(r.rebuilt))
    same_status = r.mine_status == r.status
    note = f"{r.scope}; status builder {r.status} / mine {r.mine_status}; tol {r.my_tol:g}"
    if not agree:
        note += f"; VALUE DIFFERS by {r.mine - r.rebuilt:+.4f}"
    if isinstance(r.alt_status, str):
        note += f"; alt reading {fv(r.alt_rebuilt)} -> {r.alt_status}"
    claim(agree and same_status, f"{r.id} {str(r['item'])[:38]} {str(r['group'])[:12]}: {str(r.quantity)[:48]}",
          r.rebuilt, r.mine, r.published, note, "gate row")

AR = "builder files"
acc_cols = {"net_usd_month": NET, "net_pct_budget": ACC["net_pct"], "vatable_usd_month": ACC["cv"],
            "vatable_pct_budget": ACC["vat_share"], "tax_usd_month": TAU * ACC["cv"]}
dmax_acc = {k: float(np.abs(B_ACC.loc[DEC, k].values - v).max()) for k, v in acc_cols.items()}
claim(dmax_acc["net_usd_month"] < 0.002 and dmax_acc["vatable_usd_month"] < 0.01 and dmax_acc["net_pct_budget"] < 1e-4
      and dmax_acc["vatable_pct_budget"] < 1e-3,
      "us_accounting_by_decile.csv: net, net % of budget, VAT-able $ and %, tax, all 10 deciles", "file", "recomputed", None,
      "max |diff| " + ", ".join(f"{k} {v:.1e}" for k, v in dmax_acc.items()) + " (the 4-dp flag rounding)", AR)
SCHED = {"mid": MID, "low": LOW, "high": HIGH, "mpc1": np.ones(10)}
dmax_sh = {}
for k, mp in SCHED.items():
    s_ = shifts(NET, mp)
    dmax_sh[k] = max(float(np.abs(B_SH.loc[CATS, f"dUSD_{k}"].values - s_["usd"]).max()),
                     float(np.abs(B_SH.loc[CATS, f"dPct_{k}"].values - s_["pct"]).max()))
claim(max(dmax_sh.values()) < 1e-4, "us_demand_shifts.csv: all 40 lines, $ and %, under mid, low, high and MPC=1", "file",
      "recomputed", None, "max |diff| " + ", ".join(f"{k} {v:.1e}" for k, v in dmax_sh.items()), AR)
bi_ = B_IMP.set_index(["schedule", "variant"])
imp_ok = all(abs(bi_.loc[(k, "chosen"), "flow_usd"] - FLOW[k]) < 0.002 and abs(bi_.loc[(k, "chosen"), "flow_pct_consumption"] - FLOWPCT[k]) < 1e-4
             for k in ("low", "mid", "high"))
ck = {("low", "common knee"): mpc_knee(2.55, 0.40), ("high", "common knee"): mpc_knee(2.55, 0.65)}
imp_ok = imp_ok and all(abs(bi_.loc[key, "flow_pct_consumption"] - flow_pct(mp)) < 1e-4 for key, mp in ck.items())
claim(imp_ok, "us_impulse.csv: flow impulse $ and % of consumption under low, mid, high and the common-knee variants",
      " / ".join(f"{bi_.loc[(k, 'chosen'), 'flow_pct_consumption']:.3f}" for k in ("low", "mid", "high")),
      " / ".join(f"{FLOWPCT[k]:.3f}" for k in ("low", "mid", "high")), "0.474 / 0.390 / 0.305 (Fig 7)", "", AR)

# ----------------------------------------------------------------------------------------------------------
# 14. Claims: the result paragraph and method of NOTES_us.md
# ----------------------------------------------------------------------------------------------------------
AR = "notes: result/method"
gap36 = U_MID[CHART_IDX] - PUB_USD
rmse36 = float(np.sqrt((gap36 ** 2).mean()))
claim(int((np.abs(gap36) <= 0.005 + 1e-9).sum()) == 36 and abs(rmse36 - 0.0027) < 0.00006,
      "all 36 Fig 5 bars within the printed rounding (+/-$0.005); RMSE $0.0027", "36/36, 0.0027",
      f"{int((np.abs(gap36) <= 0.005 + 1e-9).sum())}/36, {rmse36:.5f}", None,
      f"largest |gap| {np.abs(gap36).max():.4f} ({CHART[int(np.argmax(np.abs(gap36)))]}); calibration rows (2 MPC parameters fitted to these 36)", AR)
order = [CHART[i] for i in np.argsort(-np.abs(U_MID[CHART_IDX]))]
top10 = order[:10]
fig6_items = list(F6_NET.index)
top10_signed = sorted(top10, key=lambda c: -U_MID[IX[c]])
gap_10_11 = abs(U_MID[IX[order[9]]]) - abs(U_MID[IX[order[10]]])
claim(top10_signed == fig6_items, "the ten largest movers come back in the published (Fig 6) order", "yes",
      top10_signed == fig6_items, None,
      f"10th '{order[9]}' {U_MID[IX[order[9]]]:+.4f} vs 11th '{order[10]}' {U_MID[IX[order[10]]]:+.4f}: margin "
      f"${gap_10_11:.4f} (knife-edge; both print 0.38)", AR)
claim(close(ACC["dividend"], 249, 0.5) and round(ACC["vat_share"].min()) == 59 and round(ACC["vat_share"].max()) == 64
      and round(ACC["net_pct"][0], 1) == 4.8 and round(ACC["net_pct"][9], 1) == -3.9,
      "accounting reproduces $249, 59-64%, D1 +4.8%, D10 -3.9%",
      f"{B_ACC.dividend_usd_month.iloc[0]:.2f}; {B_ACC.vatable_pct_budget.min():.1f}-{B_ACC.vatable_pct_budget.max():.1f}; "
      f"{B_ACC.net_pct_budget.iloc[0]:+.2f}; {B_ACC.net_pct_budget.iloc[9]:+.2f}",
      f"{ACC['dividend']:.2f}; {ACC['vat_share'].min():.1f}-{ACC['vat_share'].max():.1f}; {ACC['net_pct'][0]:+.2f}; "
      f"{ACC['net_pct'][9]:+.2f}", "249; 59-64; +4.8; -3.9", "", AR)
lab_gap = NET - F4_LABEL.values
off = np.where(np.abs(lab_gap) > 0.5)[0]
claim(len(off) == 4 and 0.5 < np.abs(lab_gap[off]).min() and np.abs(lab_gap[off]).max() < 1.25,
      "four of ten Fig 4 net labels are off by $0.5 to $1.2 (D2, D4, D8, D10)", "4: D2, D4, D8, D10",
      f"{len(off)}: " + ", ".join(f"D{i + 1} {NET[i]:+.2f} vs {F4_LABEL.values[i]:+.0f}" for i in off), None,
      f"{int((np.round(NET) == F4_LABEL.values).sum())} of 10 labels exact", AR)
cnt = GROWS.mine_status.value_counts()
claim((cnt.get("PASS", 0), cnt.get("CLOSE", 0), cnt.get("MISS", 0)) == (256, 43, 2) and len(GROWS) == 301,
      "of 301 gated US numbers: 256 PASS, 43 CLOSE, 2 MISS", "256 / 43 / 2",
      f"{cnt.get('PASS', 0)} / {cnt.get('CLOSE', 0)} / {cnt.get('MISS', 0)}", None,
      "statuses recomputed with my values and my reading of the printed precision; identical row by row", AR)
by_scope = GROWS.groupby(["scope", "mine_status"]).size().unstack(fill_value=0).reindex(columns=["PASS", "CLOSE", "MISS"], fill_value=0)
NOTES_SCOPE = {"Fig 4": (17, 7, 0), "Fig 5": (102, 6, 1), "Fig 6 diamond": (17, 3, 0), "text": (34, 2, 1),
               "Fig 6 segment": (80, 20, 0), "Fig 7": (6, 5, 0)}
mine_scope = {sc: tuple(int(x) for x in by_scope.loc[sc]) for sc in by_scope.index}
claim(mine_scope == NOTES_SCOPE, "scope table: Fig 4 17/7/0, Fig 5 102/6/1, Fig 6 diamonds 17/3/0, text 34/2/1, "
      "segments 80/20/0, Fig 7 6/5/0", "as NOTES", "; ".join(f"{k} {'/'.join(map(str, v))}" for k, v in mine_scope.items()),
      None, "", AR)
by_role = GROWS.groupby(["role", "mine_status"]).size().unstack(fill_value=0).reindex(columns=["PASS", "CLOSE", "MISS"], fill_value=0)
NOTES_ROLE = {"calibration": (73, 8, 0), "selection": (36, 2, 0), "check": (147, 33, 2)}
mine_role = {ro: tuple(int(x) for x in by_role.loc[ro]) for ro in by_role.index}
claim(mine_role == NOTES_ROLE, "by role: calibration 73/8/0, selection 36/2/0, checks 147/33/2", "as NOTES",
      "; ".join(f"{k} {'/'.join(map(str, v))}" for k, v in mine_role.items()), None,
      "149 of the 301 published numbers were not used in any choice (checks)", AR)
us_ids = set(GL.loc[GL.group.fillna("").str.startswith("US"), "id"])
claim(len(GATE) == 669 and set(GATE.id) == us_ids | {"P916", "P917", "P918"} and (GATE.status == "not gated").sum() == 368,
      "669 US rows, 368 not gated (170 Fig 8/9, 87 axis ticks, the rest inputs, labels, cited statistics)", "669 / 368",
      f"{len(us_ids)} rows with a US group + 3 footnote-27 MPC rows = {len(GATE)}; not gated {(GATE.status == 'not gated').sum()}",
      None, "", AR)
pct_gap = PCT_MID[CHART_IDX] - np.array([F5_PCT[c] for c in CHART])
n_pct_pass = int((np.abs(pct_gap) <= 0.005 + 1e-9).sum())
worst_rel = max(abs(PCT_MID[IX[c]] - F5_PCT[c]) / abs(F5_PCT[c]) for c in CHART if abs(PCT_MID[IX[c]] - F5_PCT[c]) > 0.005)
claim(n_pct_pass == 32 and worst_rel < 0.023, "Fig 5 percent labels: 32 of 36 PASS, the other four within 2.3%",
      "32 (others <2.3%)", f"{n_pct_pass} (worst other {100 * worst_rel:.2f}%)", None,
      "a genuine check of the categories and per-share conversion (percent labels were not fitted)", AR)
claim(abs(ACC["balance"]) < 1e-9, "sum_d w_d net_d = 0 (balanced budget per payment share)", 0, ACC["balance"], None, "", AR)
bars_all = U_MID.sum()
claim(abs(bars_all - FLOW["mid"]) < 0.002, "impulse sum_d w_d mpc_d net_d equals the sum of all 40 bars to $0.002",
      f"{B_IMP.loc[(B_IMP.schedule == 'mid') & (B_IMP.variant == 'chosen'), 'flow_usd'].iloc[0]:.5f} / "
      f"{B_IMP.loc[(B_IMP.schedule == 'mid') & (B_IMP.variant == 'chosen'), 'bars_all_usd'].iloc[0]:.5f}",
      f"{FLOW['mid']:.5f} / {bars_all:.5f}", None,
      "betas sum to 0; the three food classes' beta* to +0.001 (the only leak)", AR)

# impulse readings (P436 footer: % of consumption; P438 caption: % of charted budget)
sum_labels = float(PUB_USD.sum())
offc = {c: U_MID[IX[c]] for c in OFFCHART}
claim(abs(CHART_SUM - 10.950) < 0.0015 and abs(sum_labels - 10.95) < 0.006,
      "charted bars sum to $10.950, the same as the 36 printed labels", 10.95, CHART_SUM, sum_labels,
      "published column = sum of the printed labels", AR)
claim(abs(100 * CHART_SUM / CONS_TOT - 0.406) < 0.0006 and abs(100 * CHART_SUM / CHARTED_BUDGET - 0.462) < 0.0006
      and abs(FLOWPCT["mid"] - 0.389) < 0.0006,
      "charted bars = 0.406% of consumption and 0.462% of charted budget; flow $10.48 = 0.389% of consumption",
      "0.406 / 0.462 / 0.389", f"{100 * CHART_SUM / CONS_TOT:.3f} / {100 * CHART_SUM / CHARTED_BUDGET:.3f} / {FLOWPCT['mid']:.3f}",
      "caption +0.4 (charted budget); footer +0.5 (consumption); Fig 7 0.390", "", AR)
claim(abs(offc["Mortgage interest and charges"] + 0.377) < 0.001 and abs(offc["Education"] + 0.188) < 0.001
      and abs(offc["Property taxes"] - 0.098) < 0.001 and abs(sum(offc.values()) + 0.474) < 0.002,
      "off-chart rows absorb $0.47: mortgage interest -0.38, education -0.19, property taxes +0.10",
      "-0.38 / -0.19 / +0.10", " / ".join(f"{offc[c]:+.3f}" for c in ["Mortgage interest and charges", "Education", "Property taxes"]),
      None, f"vehicle residual {offc['Other vehicles (residual)']:+.4f}; sum {sum(offc.values()):+.4f}", AR)
dn, dl = np.sign(np.diff(NET)), np.sign(np.diff(F4_LABEL.values))
claim((dn == dl).all(), "Fig 4 dots not in income order through the middle (D2 < D3, D5 < D6): same pattern as the labels",
      None, " ".join(f"{x:+.0f}" for x in NET), " ".join(f"{x:+.0f}" for x in F4_LABEL.values),
      "the payment follows adults, not equivalence (composition, not error)", AR)
flow_over_charted = 100 * FLOW["mid"] / CHARTED_BUDGET
claim(False, "P438 '+0.4% of charted budget' is a MISS under every reading", "MISS (0.462); swap -> PASS",
      f"flow/charted = {flow_over_charted:.3f}", 0.4,
      "the caption's literal denominator also PASSes if the numerator is the whole-budget impulse (all 40 bars, "
      "$10.48) rather than the 36 charted bars; MISS overstates. Only the footer (P436, 'of consumption' 0.5) has "
      "no same-denominator reading: it needs bars/charted (0.462)", AR)

# ----------------------------------------------------------------------------------------------------------
# 15. Claims: Fig 6 (decile decomposition) diagnostics
# ----------------------------------------------------------------------------------------------------------
AR = "notes: Fig 6"
seg = F6_SEG.copy()
seg["mine"] = [CONTRIB[IX[it], d - 1] for it, d in zip(seg["item"], seg["d"])]
seg["gap"] = seg["mine"] - seg["value"]
bd = B_DEC[B_DEC.decile.str.match(r"d\d\d$")].copy()
bd["d"] = bd.decile.str[1:].astype(int)
bmerge = seg.merge(bd, left_on=["item", "d"], right_on=["category", "d"])
claim(np.allclose(bmerge["mine"], bmerge["contrib_mid"], atol=6e-5), "Fig 6 decile segments c_dg = w_d C_gd eta_gd shock_d",
      "us_decomposition_top10.csv", f"max |diff| {np.abs(bmerge['mine'] - bmerge['contrib_mid']).max():.1e}", None,
      f"segment RMSE vs read-offs {np.sqrt((seg.gap ** 2).mean()):.4f} (builder 0.0073)", AR)
g8 = seg.loc[seg.d == 8, "gap"].mean()
g6 = seg.loc[seg.d == 6, "gap"].mean()
claim(abs(g8 - 0.012) < 0.003 and abs(g6 + 0.008) < 0.003 and (seg.loc[seg.d == 8, "gap"] > 0).all(),
      "every D8 withdrawal ~$0.012 smaller than published, D6 addition ~$0.008 smaller", "+0.012 / -0.008",
      f"{g8:+.4f} / {g6:+.4f}", None, f"D8 gaps all positive: {(seg.loc[seg.d == 8, 'gap'] > 0).all()}", AR)
U10 = ((W * C) * ETA * (NET / BUDGET))
implied = []
for d in range(1, 11):
    s_ = seg[seg.d == d]
    u = np.array([U10[IX[it], d - 1] for it in s_["item"]])
    implied.append(float((u * s_["value"].values).sum() / (u * u).sum()))
implied = np.array(implied)
bi = B_MPCS.loc[DEC, "fig6_implied_mpc_diagnostic"].values
claim(np.allclose(implied, bi, atol=0.002), "per-decile MPCs implied by the Fig 6 segments (diagnostic)",
      " ".join(f"{x:.2f}" for x in bi), " ".join(f"{x:.2f}" for x in implied), None,
      "least squares per decile over the 10 categories; D6 and D8 sit above the knee line (0.78, 0.66)", AR)
mono = B_MPCS.loc[DEC, "mpc_mid_monotone_fig5_fig6_diagnostic"].values
mono_bars = shifts(NET, mono)["usd"][CHART_IDX]
mono_seg = np.array([shifts(NET, mono)["contrib"][IX[it], d - 1] for it, d in zip(seg["item"], seg["d"])])
r_mb, r_ms = np.sqrt(((mono_bars - PUB_USD) ** 2).mean()), np.sqrt(((mono_seg - seg["value"].values) ** 2).mean())
r_ks = np.sqrt((seg.gap ** 2).mean())
claim(abs(r_mb - 0.0028) < 0.0002 and abs(r_ms - 0.0049) < 0.0002 and abs(r_ks - 0.0073) < 0.0002,
      "monotone per-decile diagnostic: bars RMSE $0.0028, segment RMSE $0.0073 -> $0.0049", "0.0028; 0.0073 -> 0.0049",
      f"{r_mb:.4f}; {r_ks:.4f} -> {r_ms:.4f}", None, "evaluated with the builder's schedule values", AR)
add = RENT_ADD
share_d13 = add[:3].sum() / add.sum()
claim(abs(100 * share_d13 - 63.5) < 0.15 and RENT_BULK_K == 3,
      "bottom three deciles supply 63.5% of the gross rent additions ('the bulk')", 63.5, 100 * share_d13, 3,
      f"deciles needed for >50%: {RENT_BULK_K}", AR)
hi = CONTRIB[IX["Health insurance"]]
hi_in, hi_out = hi[hi > 0].sum(), -hi[hi < 0].sum()
hp = seg.loc[seg["item"] == "Health insurance", "value"].values
hp_in, hp_out = hp[hp > 0].sum(), -hp[hp < 0].sum()
gross = {c: np.abs(CONTRIB[IX[c]]).sum() for c in CHART}
gross_rank = sorted(gross, key=gross.get, reverse=True)
churn = {c: (CONTRIB[IX[c]][CONTRIB[IX[c]] > 0].sum() - CONTRIB[IX[c]][CONTRIB[IX[c]] < 0].sum()) / max(abs(U_MID[IX[c]]), 1e-9)
         for c in CHART}
biggest = max(churn, key=churn.get)
claim(hi_in / hi_out > 2 and (hi_in + hi_out) / abs(U_MID[IX["Health insurance"]]) > 2,
      "health insurance: gross inflow 'several times' the top-side trim; gross flows 'several times the net'", None,
      f"inflow/trim {hi_in / hi_out:.2f}; gross/net {(hi_in + hi_out) / abs(U_MID[IX['Health insurance']]):.2f}", None,
      f"the post's own Fig 6 segments give inflow/trim {hp_in / hp_out:.2f}, so 'several times' is the post's loose "
      f"wording, not a rebuild gap. 'Biggest churner': by gross dollars it is #{gross_rank.index('Health insurance') + 1} "
      f"({gross['Health insurance']:.2f}) after '{gross_rank[0]}' ({gross[gross_rank[0]]:.2f}); by gross/net the largest is "
      f"'{biggest}' ({churn[biggest]:.0f}x)", AR)
neg_top10 = [c for c in top10 if U_MID[IX[c]] < 0]
claim(neg_top10 == ["Cars and trucks, new"], "the impact-period top 10 is green almost throughout (only new cars red)",
      None, ", ".join(neg_top10), None, "", AR)

# ----------------------------------------------------------------------------------------------------------
# 16. Claims: the MPC schedules (footnote 27 shape, knee family) and Fig 7
# ----------------------------------------------------------------------------------------------------------
AR = "notes: MPC"
bmid = B_MPCS.loc[DEC, "mpc_mid"].values
claim(np.allclose(MID, bmid, atol=6e-5) and np.allclose(LOW, B_MPCS.loc[DEC, "mpc_low"].values, atol=6e-5)
      and np.allclose(HIGH, B_MPCS.loc[DEC, "mpc_high"].values, atol=6e-5),
      "schedules: flat 1.0 to the knee, linear to the top at D10 (mid knee 2.55 top 0.53; low 1.93/0.40; high 3.29/0.65)",
      " ".join(f"{x:.2f}" for x in bmid), " ".join(f"{x:.2f}" for x in MID), None, "low and high also identical", AR)
claim(FIT_TOP == 0.53 and abs(FIT_KNEE - 2.55) <= 0.011 and abs(FIT_RMSE - 0.0027) < 0.00005,
      "MPC mid pinned by least squares on the 36 Fig 5 dollar bars", "knee 2.55, top 0.53, RMSE 0.0027",
      f"knee {FIT_KNEE:.2f}, top {FIT_TOP:.4f}, RMSE {FIT_RMSE:.5f}", None,
      f"my grid is 0.01 x 0.0025 (builder 0.05 x 0.0025); RMSE at (2.55, 0.53) "
      f"{np.sqrt((((mpc_knee(2.55, 0.53) @ M36.T) - PUB_USD) ** 2).mean()):.5f}", AR)
sig2 = 0.005 ** 2 / 3
in68 = 36 * (rmse_grid ** 2 - FIT_RMSE ** 2) / sig2 <= 2.30
kn68, tp68 = KNEES[in68.any(1)], TOPS[in68.any(0)]
coarse = (np.round(KNEES * 100).astype(int) % 5 == 0)[:, None] & np.ones_like(in68)
n68_coarse = int((in68 & coarse & (TOPS[None, :] >= 0.4) & (TOPS[None, :] <= 0.65)).sum())
claim(n68_coarse == 1, "the 68% region (rounding noise only) is a single grid point", "1 point",
      f"{n68_coarse} on the 0.05 grid; on 0.01: knee {kn68.min():.2f}-{kn68.max():.2f}, top {tp68.min():.4f}-{tp68.max():.4f}",
      None, "true at the builder's resolution; the honest statement is the range", AR)
claim(abs(INT_KNEE_BEST[2][0] - 0.5125) < 1e-9 and abs(INT_KNEE_BEST[3][0] - 0.545) < 1e-9
      and abs(INT_KNEE_BEST[2][1] - 0.011) < 0.0005 and abs(INT_KNEE_BEST[3][1] - 0.010) < 0.0005,
      "integer knees: knee 2 top 0.5125 (RMSE $0.011); knee 3 top 0.545 ($0.010)", "0.5125/0.011; 0.545/0.010",
      f"{INT_KNEE_BEST[2][0]:.4f}/{INT_KNEE_BEST[2][1]:.4f}; {INT_KNEE_BEST[3][0]:.4f}/{INT_KNEE_BEST[3][1]:.4f}", None,
      "a 2.5-decile knee fits 4x better than either integer knee", AR)
claim(abs(KNEE_LOW - 1.93) < 0.006 and abs(KNEE_HIGH - 3.29) < 0.006,
      "low / high knees pinned by the Fig 7 band edges 0.474 / 0.305 (tops 0.40 / 0.65 from fn 27)", "1.93 / 3.29",
      f"{KNEE_LOW:.3f} / {KNEE_HIGH:.3f}", "0.474 / 0.305", "two numbers, two knees: reproduced, not tested", AR)
ck_lo, ck_hi = flow_pct(mpc_knee(2.55, 0.65)), flow_pct(mpc_knee(2.55, 0.40))
claim(abs(ck_lo - 0.290) < 0.001 and abs(ck_hi - 0.497) < 0.001, "with a common knee 2.55 the band would be 0.290-0.497",
      "0.290-0.497", f"{ck_lo:.3f}-{ck_hi:.3f}", "0.305-0.474", "5-6% too wide, which is why the knees differ", AR)
avg_dev = np.abs(MID - (LOW + HIGH) / 2).max()
claim(avg_dev <= 0.0115, "the mid schedule is within 0.011 of the average of low and high at every decile", 0.011, avg_dev,
      None, "an unforced consistency check", AR)
claim(abs(FLOWPCT["mid"] - 0.390) <= 0.0015, "mid-schedule impulse 0.389% of consumption vs Fig 7 central plateau 0.390",
      0.3889, FLOWPCT["mid"], 0.390, "not used in any calibration", AR)
r_mpc = 100 * weighted_mpc(MID, NET > 0)
p_lo, p_hi = 100 * weighted_mpc(LOW, NET < 0), 100 * weighted_mpc(HIGH, NET < 0)
pmin, pmax = 100 * min(LOW[NET < 0].min(), HIGH[NET < 0].min()), 100 * max(LOW[NET < 0].max(), HIGH[NET < 0].max())
claim(abs(r_mpc - 91.4) < 0.1 and abs(p_lo - 42.1) < 0.1 and abs(p_hi - 66.5) < 0.1 and abs(pmin - 40) < 0.1
      and abs(pmax - 75.4) < 0.1, "Fig 7 wording: recipients' MPC 91%; payers 42% (low) / 66% (high); extremes 40% / 75%",
      "91 / 42 / 66; 40 / 75", f"{r_mpc:.1f} / {p_lo:.1f} / {p_hi:.1f}; {pmin:.1f} / {pmax:.1f}", "~100 / 40-70",
      "CLOSE as the builder says: the annotation is stylised", AR)
claim(MID[0] == 1.0 and MID[1] == 1.0 and 0.40 <= MID[9] <= 0.65 and (np.diff(MID) <= 1e-12).all()
      and (np.diff(LOW) <= 1e-12).all() and (np.diff(HIGH) <= 1e-12).all() and (LOW <= MID + 1e-12).all()
      and (MID <= HIGH + 1e-12).all(),
      "schedules inside fn 27's stated range (1.0 at the bottom deciles, 0.40-0.65 at the top), monotone and nested",
      None, f"mid D1-D2 1.0, D10 {MID[9]:.2f}; low <= mid <= high everywhere", "1.0 -> 0.40-0.65",
      "knee 2.55 deciles puts ~25% of units at MPC 1, close to Kaplan-Violante-Weidner's ~1/3 hand-to-mouth (fn 27)", AR)

# ----------------------------------------------------------------------------------------------------------
# 17. Claims: the judgment-call table of NOTES_us.md, re-tested
# ----------------------------------------------------------------------------------------------------------
AR = "notes: judgment calls"
# 17a. budget rows
NET_PCT_DEN = {"chosen": C.sum(0), "cash in": C.sum(0) + per_share_month(CASH),
               "everything in": per_share_month(TOTAL),
               "off-chart out": C.sum(0) - C[[IX[c] for c in ["Education", "Mortgage interest and charges", "Property taxes"]]].sum(0)}
bt_rows = {"chosen": 0, "cash in": 1, "everything in": 2, "off-chart out": 3}
for nm, den in NET_PCT_DEN.items():
    p1, p10 = 100 * NET[0] / den[0], 100 * NET[9] / den[9]
    vs = 100 * ACC["cv"] / den
    br = B_BUD.iloc[bt_rows[nm]]
    passes = round(p1, 1) == 4.8 and round(p10, 1) == -3.9 and round(vs.min()) == 59 and round(vs.max()) == 64
    agree = abs(p1 - br.D1_net_pct) < 0.002 and abs(p10 - br.D10_net_pct) < 0.002 and abs(vs.min() - br.vatable_share_min) < 0.003 \
        and abs(vs.max() - br.vatable_share_max) < 0.003
    claim(agree and passes == (nm == "chosen"), f"budget rows '{nm}': only the chosen definition passes Fig 4's +4.8 / -3.9 / 59-64",
          f"{br.D1_net_pct:+.2f} / {br.D10_net_pct:+.2f} / {br.vatable_share_min:.1f}-{br.vatable_share_max:.1f}",
          f"{p1:+.2f} / {p10:+.2f} / {vs.min():.1f}-{vs.max():.1f}", "+4.8 / -3.9 / 59-64",
          "passes" if passes else "fails", AR)
claim(False, "us_budget_tests.csv 'chosen' row uses the same budget as the model", f"max VAT-able {B_BUD.iloc[0].vatable_share_max:.4f}",
      f"{ACC['vat_share'].max():.4f} (sum of 40 lines); {100 * ACC['cv'][9] / per_share_month(TOTAL - CASH - PIP)[9]:.4f} (printed totals)",
      None, "cosmetic: the budget test divides by printed total - pensions - cash ($2/CU-yr below the 40-line sum the "
      "model uses); no verdict changes", AR)

# 17b. payment units and weights
exact = int((np.round(NET) == F4_LABEL.values).sum())
rng = np.random.default_rng(20261102)
draws = []
for _ in tqdm(range(1000), desc="payment-unit rounding draws", leave=False):
    pe = PEOPLE + rng.uniform(-0.05, 0.05, 10)
    ki = np.clip(KIDS + rng.uniform(-0.05, 0.05, 10), 0, None)
    r = model(people=pe, kids=ki)
    draws.append((int((np.round(r["acc"]["net"]) == F4_LABEL.values).sum()), r["acc"]["dividend"], r["acc"]["net"][7],
                  r["acc"]["net"][9], r["s"]["usd"][IX["Rented dwellings"]]))
draws = np.array(draws)
q5, q50, q95 = np.percentile(draws, [5, 50, 95], axis=0)
bs = B_SENS
claim(exact == 6 and q50[0] <= 1.5, "printed People/Children rows reproduce 6 of 10 labels; +/-0.05 redraws a median of 1",
      "6; median 1", f"{exact}; median {q50[0]:.0f}", None,
      "evidence that the post used the same printed one-decimal rows", AR)
lo_b = bs.loc["payment-unit rounding draws, 5th percentile"]
hi_b = bs.loc["payment-unit rounding draws, 95th percentile"]
ok_draw = (abs(q5[1] - lo_b.dividend) < 0.4 and abs(q95[1] - hi_b.dividend) < 0.4 and abs(q5[2] - lo_b.D8_net) < 1.5
           and abs(q95[2] - hi_b.D8_net) < 1.5 and abs(q5[3] - lo_b.D10_net) < 1.5 and abs(q95[3] - hi_b.D10_net) < 1.5
           and abs(q5[4] - lo_b.rent) < 0.03 and abs(q95[4] - hi_b.rent) < 0.03)
claim(ok_draw, "rounding spread (5th-95th pct): dividend 247.5-251.3, D8 -20..-8, D10 -181..-163, rent bar 3.24-3.48",
      f"{lo_b.dividend:.1f}-{hi_b.dividend:.1f}; {lo_b.D8_net:.0f}..{hi_b.D8_net:.0f}; {lo_b.D10_net:.0f}..{hi_b.D10_net:.0f}; "
      f"{lo_b.rent:.2f}-{hi_b.rent:.2f}",
      f"{q5[1]:.1f}-{q95[1]:.1f}; {q5[2]:.0f}..{q95[2]:.0f}; {q5[3]:.0f}..{q95[3]:.0f}; {q5[4]:.2f}-{q95[4]:.2f}", None,
      "my own 1,000 draws (seed 20261102); a property of the data shared with the post", AR)
eq = model(equal_cu=True)
claim(np.abs(eq["acc"]["net"] - NET).max() < 0.15 and abs(eq["acc"]["dividend"] - ACC["dividend"]) < 0.15,
      "equal CU weights instead of CU counts: the same to +/-$0.1", "+/-0.1",
      f"max |d net| {np.abs(eq['acc']['net'] - NET).max():.3f}, d dividend {eq['acc']['dividend'] - ACC['dividend']:+.3f}",
      None, "", AR)

# 17c. VAT-flag search, replicated with the builder's stated objective (run_us.py step 2 comment)
ALT = {"water_refuse_out": MIXED["Water and other public services"],
       "lodging_trips_only": det(f"{OL} > Lodging on out of town trips") / det(OL),
       "vehicle_tolls_public": share_of(VR, ["Leased and rented vehicles", "Parking fees", "Towing charges",
                                             "Automobile service clubs and GPS services"]),
       "drugs_rx_relief": share_of(DR, ["Nonprescription drugs", "Vitamins and supplements"]),
       "transit_exempt": 1 - share_of(PT, ["Intracity mass transit fares", "School bus"]),
       "fees_clubs_exempt": 1 - share_of(FA, ["Social, recreation, and health club memberships"]),
       "inspections_taxable": share_of(VR, ["Leased and rented vehicles", "Parking fees", "Tolls or electronic toll passes",
                                            "Tolls on out of town trips", "Towing charges",
                                            "Automobile service clubs and GPS services", "Vehicle inspections"]),
       "household_staff_out": 1 - share_of(OH, ["Housekeeping services"]),
       "hoa_exempt": share_of(OD, ["Maintenance and repair services", "Maintenance and repair commodities", "Parking"]),
       "air_zero_rated": 1 - share_of(PT, ["Airline fares"])}
r4 = lambda x: round(x, 4)
GRID = {"Cars and trucks, used": [0.0, 0.25, 0.5, 0.75, 1.0],
        "Water and other public services": [r4(ALT["water_refuse_out"]), 1.0],
        "Other lodging": [r4(ALT["lodging_trips_only"]), r4(MIXED["Other lodging"])],
        "Vehicle rental, leases, licenses": [r4(ALT["vehicle_tolls_public"]), r4(MIXED["Vehicle rental, leases, licenses"])],
        "Drugs": [r4(ALT["drugs_rx_relief"]), 1.0],
        "Public and other transportation": [r4(ALT["transit_exempt"]), 1.0],
        "Fees and admissions": [r4(ALT["fees_clubs_exempt"]), 1.0],
        "Rented dwellings": [0.0, r4(MIXED["Rented dwellings"])],
        "Education": [0.0, r4(MIXED["Education"])]}
gkeys = list(GRID)
combos = np.array(np.meshgrid(*[GRID[k] for k in gkeys], indexing="ij")).reshape(len(gkeys), -1).T
base4 = {c: (r4(v) if c in MIXED else v) for c, v in SPEC_FLAGS.items()}
fixed = [c for c in CATS if c not in GRID]
v0 = sum(base4[c] * C[IX[c]] for c in fixed)
cvs = v0[None, :] + combos @ C[[IX[k] for k in gkeys]]
cbar_v = cvs @ W
nets = TAU * (cbar_v[:, None] - cvs)
divs = TAU * cbar_v
pcts = 100 * nets / BUDGET[None, :]
shs = 100 * cvs / BUDGET[None, :]
s_lab, s_x, s_pct = 0.5 / np.sqrt(3), 5 / np.sqrt(3), 0.05 / np.sqrt(3)
xw = np.array([1, 0, 1, 1, 1, 1, 1, 1, 1, 1.0])               # D2 hidden behind D4 (low confidence)
lab_term = (((nets - F4_LABEL.values) / s_lab) ** 2).sum(1) + ((divs - 249) / s_lab) ** 2 \
    + ((pcts[:, 0] - 4.8) / s_pct) ** 2 + ((pcts[:, 9] + 3.9) / s_pct) ** 2 \
    + 100.0 * ((np.round(shs.min(1)) != 59) | (np.round(shs.max(1)) != 64))
x_term = ((((cvs - F4_X.values) / s_x) ** 2) * xw).sum(1)
obj = lab_term + x_term
ordr = np.argsort(obj)
best = dict(zip(gkeys, combos[ordr[0]]))
n_exact = (np.round(nets) == F4_LABEL.values).sum(1)
claim(len(combos) == 1280 and all(abs(best[k] - base4[k]) < 1e-9 for k in gkeys) and abs(obj[ordr[0]] - B_FS.objective.iloc[0]) < 0.05,
      "Directive grid (1,280 sets): the builder's objective picks the adopted flags", f"objective {B_FS.objective.iloc[0]:.2f}",
      f"{len(combos)} sets; best objective {obj[ordr[0]]:.2f} = adopted flags", None, "", AR)
top20_used = combos[ordr[:20], 0]
by_used = {u: obj[combos[:, 0] == u].min() for u in GRID["Cars and trucks, used"]}
claim((top20_used == 0.5).all() and all(by_used[u] > by_used[0.5] for u in by_used if u != 0.5),
      "used cars: all 20 best sets have 1/2; 0, 1/4, 3/4, 1 all worse", "20/20 at 1/2",
      f"{int((top20_used == 0.5).sum())}/20; best objective by flag " + ", ".join(f"{u:g}: {by_used[u]:.0f}" for u in by_used),
      None, "sharply pinned by Fig 4 (the D7 dip and the D9-D10 fall of the used-car line)", AR)
ok249 = np.round(divs) == 249
claim(not ((n_exact == 10) & ok249).any(), "no Directive-consistent set reproduces all ten labels and the dividend",
      "none", f"max labels exact with $249: {int(n_exact[ok249].max())}", None, "", AR)
wat = dict(SPEC_FLAGS, **{"Water and other public services": 1.0})
claim(abs(accounting(wat)["dividend"] - 250.9) < 0.06, "water at the Nordic reading (1.0) gives a $250.9 dividend", 250.9,
      accounting(wat)["dividend"], 249, "so 0.688 (refuse collection outside scope) is pinned by the dividend level", AR)
alt_expect = {"lodging_trips_only": 0.673, "vehicle_tolls_public": 0.626, "drugs_rx_relief": 0.42, "transit_exempt": 0.90,
              "fees_clubs_exempt": 0.71}
claim(all(abs(ALT[k] - v) < 0.0051 for k, v in alt_expect.items()),
      "alternative mixed-line shares tested in the grid: trips-only lodging 0.673, tolls public 0.626, Rx relief 0.42, "
      "transit exempt 0.90, clubs exempt 0.71", "as listed", ", ".join(f"{ALT[k]:.3f}" for k in alt_expect), None,
      "from the raw Table 2500 children", AR)
# rent flag: NOTES lists 0.017 as 'not pinned (Directive reading)'; it was in the grid with 0
printed_only = lab_term
i_rent0 = int(np.argmin(np.where(combos[:, gkeys.index("Rented dwellings")] == 0, printed_only, np.inf)))
i_adopt = int(ordr[0])
r_rent0 = model(flags=dict(SPEC_FLAGS, **{"Rented dwellings": 0.0}))
rf0 = refit_mpc(r_rent0["acc"]["net"])
PUB_GH = np.array([F5_GHOST[c] for c in CHART])
gh_rmse0 = float(np.sqrt(((r_rent0["s1"]["usd"][CHART_IDX] - PUB_GH) ** 2).mean()))
gh_rmse_a = float(np.sqrt(((U_ONE[CHART_IDX] - PUB_GH) ** 2).mean()))
claim(False, "rent flag 0.017 'not pinned (Directive reading)'", "0.0167, not pinned",
      f"chosen over 0 by the grid; printed numbers alone prefer 0: labels exact {n_exact[i_rent0]} vs {n_exact[i_adopt]}, "
      f"label SSE {((nets[i_rent0] - F4_LABEL.values) ** 2).sum():.2f} vs {((nets[i_adopt] - F4_LABEL.values) ** 2).sum():.2f}, "
      f"dividend {divs[i_rent0]:.2f} vs {divs[i_adopt]:.2f}",
      "labels, $249, +4.8/-3.9, 59-64",
      f"only the pixel read-offs of the point positions (+/-5) tip it to 0.0167 (x term {x_term[i_rent0]:.1f} vs "
      f"{x_term[i_adopt]:.1f}); the Fig 5 ghosts also prefer 0 (RMSE {gh_rmse0:.4f} vs {gh_rmse_a:.4f}; rent ghost "
      f"{r_rent0['s1']['usd'][IX['Rented dwellings']]:.3f} vs {U_ONE[IX['Rented dwellings']]:.3f}, read off 3.26) and the bars "
      f"refit as well (knee {rf0[1]:.2f}, top {rf0[2]:.4f}, RMSE {rf0[0]:.4f}). Rent = 0 is the post's own 'rent exempt' "
      "wording. Downstream effect small", AR)
loose = B_FS[B_FS.grid.str.startswith("loose")]
lres = []
for _, r in loose.iterrows():
    fl = dict(base4)
    for k in gkeys + ["Home maintenance, repairs & insurance", "Miscellaneous", "Housekeeping supplies"]:
        if k in r and pd.notna(r[k]):
            fl[k] = float(r[k])
    a = accounting(fl)
    lres.append((int((np.round(a["net"]) == F4_LABEL.values).sum()), a["dividend"]))
claim(all(e == int(r.labels_exact) and abs(d - r.dividend) < 0.01 for (e, d), (_, r) in zip(lres, loose.iterrows()))
      and max(e for e, _ in lres) == 9,
      "loose grid (licences, registration, vehicle property tax or vacation-home interest in; drugs/transit partly out): "
      "9 of 10 labels with the dividend", "9/10", f"{max(e for e, _ in lres)}/10 (all {len(lres)} rows reproduced)", None,
      "rightly not adopted: those lines are taxes or exempt credit under the Directive", AR)
dir20 = B_FS[B_FS.grid == "Directive-consistent"].head(20)
bars20 = []
for _, r in dir20.iterrows():
    fl = dict(base4, **{k: float(r[k]) for k in gkeys})
    s_ = model(flags=fl)["s"]["usd"]
    bars20.append((s_[IX["Rented dwellings"]], s_[IX["Health insurance"]], s_[IX["Cars and trucks, new"]]))
bars20 = np.array(bars20)
claim(bars20[:, 0].min() >= 3.335 and bars20[:, 0].max() < 3.385 and bars20[:, 1].min() >= 1.065 and bars20[:, 1].max() < 1.095
      and np.all(np.round(bars20[:, 2], 2) == -0.39),
      "across the 20 best Directive sets: rent 3.34-3.38, health insurance 1.07-1.09, new cars -0.39", "as listed",
      f"rent {bars20[:, 0].min():.3f}-{bars20[:, 0].max():.3f}, health {bars20[:, 1].min():.3f}-{bars20[:, 1].max():.3f}, "
      f"new {bars20[:, 2].min():.3f}..{bars20[:, 2].max():.3f}", None, "MPC held at mid", AR)
labnet = model(net=F4_LABEL.values.astype(float))
dmax = np.abs(labnet["s"]["usd"] - U_MID)[CHART_IDX]
lb = bs.loc["published Fig 4 labels as nets"]
claim(dmax.max() <= 0.0115 and CHART[int(np.argmax(dmax))] == "Rented dwellings"
      and abs(labnet["s"]["usd"][IX["Rented dwellings"]] - lb.rent) < 1e-3 and abs(labnet["s"]["usd"][IX["Health insurance"]] - lb.health_ins) < 1e-3
      and abs(labnet["s1"]["usd"][IX["Cars and trucks, new"]] - lb.new_cars_ghost) < 1e-3,
      "published labels as the net vector move no bar by more than $0.011 (rent)", f"rent {lb.rent:.4f}",
      f"rent {labnet['s']['usd'][IX['Rented dwellings']]:.4f}; max |d bar| {dmax.max():.4f}", None,
      "also a genericity check: the machinery takes any net vector (what the LVT step needs)", AR)

# 17d. stage-one mapping and food split (ghost RMSE vs the 36 read-off outlines)
PUB_GHOST = np.array([F5_GHOST[c] for c in CHART])


def regroup(moves):
    G = {k: [c for c in v if c not in moves] for k, v in GROUP_OF.items()}
    for c, k in moves.items():
        G[k].append(c)
    return G


def elasticities_A2(C=C, group_of=GROUP_OF, food_class=FOOD_CLASS):
    """Food split A2: nonalcoholic beverages (inside CE 'Food at home') counted in Beverages and tobacco."""
    eta, wk, eta_f = elasticities(C=C, group_of=group_of, food_class=food_class)
    shares = A.sum(0) / 12.0 / C.sum(0)       # per-share divisor recovered from C
    nab = dec_mean(f"{AAE} > Food > Food at home > Other food at home > Nonalcoholic beverages") / 12.0 / shares
    food = C[[IX[c] for c in group_of["food"]]].sum(0)
    fah = C[IX["Food at home"]]
    bt = C[IX["Alcoholic beverages"]] + C[IX["Tobacco products"]] + nab
    e_home = eta_f * (1 + FOOD_CLASS["at_home"][1] / ((fah - nab) / food))
    e_bt = eta_f * (1 + FOOD_CLASS["bev_tob"][1] / (bt / food))
    eta = eta.copy()
    eta[IX["Food at home"]] = ((fah - nab) * e_home + nab * e_bt) / fah
    eta[IX["Alcoholic beverages"]] = e_bt
    eta[IX["Tobacco products"]] = e_bt
    return eta, wk, eta_f


def elasticities_F(C=C, group_of=GROUP_OF, food_class=FOOD_CLASS):
    eta, wk, eta_f = elasticities(C=C, group_of=group_of, food_class=food_class)
    eta = eta.copy()
    for c in group_of["food"]:
        eta[IX[c]] = eta_f
    return eta, wk, eta_f


def mapping_fit(group_of=GROUP_OF, eta_fn=None):
    r = model(group_of=group_of, eta_fn=eta_fn)
    gh = r["s1"]["usd"][CHART_IDX]
    Mv = ((W * C) * r["eta"] * (NET / BUDGET))[CHART_IDX]
    best_ = np.inf
    for kn in np.arange(1.0, 6.0001, 0.05):
        mp = np.array([mpc_knee(kn, tp) for tp in TOPS])
        best_ = min(best_, np.sqrt((((mp @ Mv.T) - PUB_USD) ** 2).mean(1)).min())
    return float(np.sqrt(((gh - PUB_GHOST) ** 2).mean())), best_, r


MAPS = {"chosen: CE majors, telephone in transport & communication": GROUP_OF,
        "telephone in housing (CE utilities)": regroup({"Telephone services": "housing"}),
        "personal services in other (social protection)": regroup({"Personal services (incl. childcare)": "other"}),
        "health insurance in other (COICOP 12)": regroup({"Health insurance": "other"}),
        "vehicle insurance in other (COICOP 12)": regroup({"Vehicle insurance": "other"}),
        "other lodging in other (COICOP 11.2)": regroup({"Other lodging": "other"}),
        "other lodging in recreation": regroup({"Other lodging": "recreation"}),
        "vehicle finance charges in other": regroup({"Vehicle finance charges": "other"}),
        "home maintenance in furnishings": regroup({"Home maintenance, repairs & insurance": "furnishings"}),
        "reading in other": regroup({"Reading": "other"})}
bm = B_MAP.set_index("variant")
map_res = {}
for nm, G in tqdm(MAPS.items(), desc="mapping variants", leave=False):
    map_res[nm] = mapping_fit(G)
for nm, (grm, brm, _) in map_res.items():
    claim(abs(grm - bm.loc[nm, "ghost_rmse"]) < 6e-5, f"mapping test '{nm}': ghost RMSE", bm.loc[nm, "ghost_rmse"], grm, None,
          f"bar RMSE at best knee/top: mine {brm:.4f} (0.05 x 0.0025 grid), builder {bm.loc[nm, 'bars_rmse_best_knee']:.4f}", AR)
tel = map_res["telephone in housing (CE utilities)"][2]["s1"]["usd"][IX["Telephone services"]]
g0, b0 = map_res["chosen: CE majors, telephone in transport & communication"][:2]
both10 = [nm for nm, (gr, br, _) in map_res.items() if gr < 0.9 * g0 and br < 0.9 * b0]
best_ghost = min(map_res, key=lambda k: map_res[k][0])
claim(abs(tel - 0.264) < 0.001 and not both10,
      "telephone in housing: ghost 0.264 vs 0.30 read off; no alternative mapping improves both fits by more than 10%",
      "0.264; none", f"{tel:.4f}; {', '.join(both10) or 'none'}", 0.30,
      f"lowest ghost RMSE is '{best_ghost}' ({map_res[best_ghost][0]:.4f} vs {g0:.4f}, -{100 * (1 - map_res[best_ghost][0] / g0):.0f}%) "
      "but its bars fit worse", AR)
claim(False, "bar RMSE at the best knee for the chosen mapping is quoted as $0.0032 (NOTES table) and $0.0027 (us_flags.csv)",
      "0.0032 / 0.0027", f"{map_res['chosen: CE majors, telephone in transport & communication'][1]:.4f} (0.05 grid), {FIT_RMSE:.4f} (0.01 grid)",
      None, "cosmetic: the mapping tests used a coarser knee grid; quote one number", AR)
FOODS = {"chosen A: Food other = restaurants, B&T = alcohol + tobacco, at home = six named": None,
         "A2: nonalcoholic beverages in Beverages and tobacco": elasticities_A2,
         "F: no split, stage-one food eta for all four": elasticities_F}
for nm, fn in FOODS.items():
    grm, brm, r = mapping_fit(eta_fn=fn)
    gh4 = [r["s1"]["usd"][IX[c]] for c in ["Food at home", "Food away from home", "Alcoholic beverages", "Tobacco products"]]
    b4 = [bm.loc[nm, f"ghost_{c}"] for c in ["Food at home", "Food away from home", "Alcoholic beverages", "Tobacco products"]]
    claim(abs(grm - bm.loc[nm, "ghost_rmse"]) < 6e-5 and np.allclose(gh4, b4, atol=6e-5), f"food split '{nm[:40]}': four food ghosts",
          " / ".join(f"{x:.3f}" for x in b4), " / ".join(f"{x:.3f}" for x in gh4), "0.44 / 0.08 / -0.03 / 0.12",
          f"ghost RMSE {grm:.4f}; bar RMSE at best knee {brm:.4f}", AR)

# ----------------------------------------------------------------------------------------------------------
# 18. Adversarial review 1: each VAT flag against the EU VAT Directive (2006/112/EC), the post's 'EU-style base'
# ----------------------------------------------------------------------------------------------------------
AR = "review: VAT flags vs Directive"
DIRECTIVE = [  # (category, consistent?, reading)
    ("Cars and trucks, used", False,
     "second-hand goods sold by taxable dealers are taxed on the dealer's margin (Arts. 311-325), private sales are "
     "outside the scope: a Directive reading is ~0.1, not 1/2. 1/2 = dealer sales taxed on the full price (a sales-tax "
     "rule). It is the post's own flag (sharply pinned by Fig 4) and NOTES/us_flags.csv say so, but the judgment-call "
     "table still heads all flags 'EU Directive reading'"),
    ("Water and other public services", True,
     "water supply by public bodies is taxable (Art. 13 + Annex I(2)); sewerage and refuse collection by public "
     "authorities are outside the scope unless competition is distorted. CE merges water with sewerage, so 0.688 taxes "
     "sewerage (Nordic practice) and exempts refuse; a strict reading would be lower, the Nordic one 1.0. Choice between "
     "0.688 and 1.0 pinned by the $249 dividend: documented"),
    ("Rented dwellings", True,
     "letting of immovable property exempt (Art. 135(1)(l)), tenant insurance exempt (135(1)(a)), tenant-paid repairs "
     "taxable: 0.017 is a correct reading, but 0 (the post's 'rent exempt') is equally Directive-consistent and fits the "
     "printed Fig 4 numbers better"),
    ("Home maintenance, repairs & insurance", True,
     "repair services and materials taxable (Annex III(10a) allows reduced rates), homeowners insurance exempt "
     "(135(1)(a)), ground rent = letting of land (135(1)(l)). Condo/HOA management fees (4.9% of the line) are exempt "
     "or outside in some member states"),
    ("Other lodging", True,
     "hotel accommodation is carved out of the letting exemption (Art. 135(2)(a)) so taxable; vacation-home interest, "
     "taxes and insurance are not taxable supplies; school housing exempt (letting, or 132(1)(i))"),
    ("Vehicle rental, leases, licenses", True,
     "registration, vehicle property tax and licences are taxes or public-authority fees (Art. 13); vehicle inspections "
     "(1.7% of the line) are also treated as public fees, though private test centres charge VAT in most states"),
    ("Miscellaneous", True,
     "legal, accounting, funeral (Annex III(16)) taxable; lotteries (135(1)(i)), bank charges (135(1)(d)), credit "
     "interest (135(1)(b)), union and professional dues (132(1)(l)) exempt; taxes outside"),
    ("Housekeeping supplies", True, "postage by the universal service provider exempt (Art. 132(1)(a))"),
    ("Education", True, "tuition exempt (Art. 132(1)(i),(j)); books and supplies taxable"),
    ("Fees and admissions", True,
     "simplification: Art. 132(1)(m) (sport by non-profits) and (n) (cultural services of public or recognised bodies) "
     "exempt part of this line; taxing all of it is the post's uniform-base reading (club memberships exempt, 0.71, "
     "fits Fig 4 worse)"),
    ("Public and other transportation", True,
     "passenger transport taxable (Annex III(5)); some states keep exemptions under Art. 371/Annex X and international "
     "air is effectively zero-rated (airline fares are 60% of this line)"),
    ("Other household expenses", True,
     "taxable services (internet, gardening, pest control, moving); housekeeping paid to household employees (13.6% "
     "of the line) is a wage, not a supply"),
    ("Vehicle maintenance and repairs", True,
     "repairs and parts taxable; the 'auto repair service policy' (5.2%) is exempt insurance when a third-party "
     "insurer sells it (CJEU C-349/96)"),
    ("Drugs", True, "medicines are goods: taxable, reduced rates allowed (Annex III(3)); some states zero-rate Rx"),
    ("Personal services (incl. childcare)", True, "child and elderly care by recognised bodies exempt (Art. 132(1)(g),(h))"),
]
CLEAR = {"exempt or outside": ["Mortgage interest and charges (135(1)(b))", "Property taxes (not a supply)",
                               "Vehicle finance charges (135(1)(b))", "Vehicle insurance, Health insurance (135(1)(a))",
                               "Medical services (132(1)(b),(c),(e))"],
         "taxable": ["food, alcohol, tobacco, restaurants", "energy", "telephone", "furnishings", "apparel", "new cars",
                     "other vehicles", "fuel", "medical supplies", "recreation lines", "personal care", "reading"]}
for c, ok, why in DIRECTIVE:
    claim(ok, f"flag of '{c}' is consistent with the Directive", B_FLAGS.loc[c, "vat_flag"], SPEC_FLAGS[c], None, why, AR)
wreason = str(B_FLAGS.loc["Water and other public services", "vat_reason"])
claim("sewerage taxable (Annex I)" not in wreason, "us_flags.csv reason for the water line cites the Directive correctly",
      wreason[:60] + "...", "Annex I(2) is the supply of water only", None,
      "documentation: sewerage is not an Annex I activity; taxing it is member-state practice (Nordic), so the 0.688 "
      "share is 'water + sewerage taxed as in the Nordics, refuse outside under Art. 13', not an Annex I reading", AR)
claim(all(SPEC_FLAGS[c] in (0.0, 1.0) for c in CATS if c not in MIXED and c != "Cars and trucks, used"),
      "the remaining 23 clear-cut flags are consistent with the Directive", "0 / 1", "0 / 1", None,
      "exempt or outside: " + "; ".join(CLEAR["exempt or outside"]) + ". Taxable: " + ", ".join(CLEAR["taxable"]), AR)

# ----------------------------------------------------------------------------------------------------------
# 19. Adversarial review 2: would another defensible choice change a headline?
# ----------------------------------------------------------------------------------------------------------
AR = "review: headline sensitivity"
coicop = regroup({"Health insurance": "other", "Vehicle insurance": "other", "Personal services (incl. childcare)": "other",
                  "Other lodging": "other", "Vehicle finance charges": "other"})
k2, k3 = INT_KNEE_BEST[2][0], INT_KNEE_BEST[3][0]
ALTS = {
    "rent flag 0 (the post's 'rent exempt'; best on printed numbers)": dict(flags=dict(SPEC_FLAGS, **{"Rented dwellings": 0.0})),
    "used cars 0.1 (Directive margin scheme)": dict(flags=dict(SPEC_FLAGS, **{"Cars and trucks, used": 0.1})),
    "used cars 1.0 (all taxable)": dict(flags=dict(SPEC_FLAGS, **{"Cars and trucks, used": 1.0})),
    "water 1.0 (Nordic)": dict(flags=dict(SPEC_FLAGS, **{"Water and other public services": 1.0})),
    "drugs: Rx zero-rated (0.42)": dict(flags=dict(SPEC_FLAGS, **{"Drugs": ALT["drugs_rx_relief"]})),
    "fees: Art. 132(1)(m) clubs exempt (0.71)": dict(flags=dict(SPEC_FLAGS, **{"Fees and admissions": ALT["fees_clubs_exempt"]})),
    "transport: air zero-rated (0.40)": dict(flags=dict(SPEC_FLAGS, **{"Public and other transportation": ALT["air_zero_rated"]})),
    "household staff wages outside VAT (0.86)": dict(flags=dict(SPEC_FLAGS, **{"Other household expenses": ALT["household_staff_out"]})),
    "vehicle inspections taxable (0.72)": dict(flags=dict(SPEC_FLAGS, **{"Vehicle rental, leases, licenses": ALT["inspections_taxable"]})),
    "HOA/condo fees exempt (0.67)": dict(flags=dict(SPEC_FLAGS, **{"Home maintenance, repairs & insurance": ALT["hoa_exempt"]})),
    "bulletin-faithful COICOP groups (insurances, childcare, lodging, vehicle finance -> Other)": dict(group_of=coicop),
    "food split F (no stage-two split)": dict(eta_fn=elasticities_F),
    f"MPC integer knee 2 (top {k2:.4f})": dict(mpc=mpc_knee(2, k2)),
    f"MPC integer knee 3 (top {k3:.4f})": dict(mpc=mpc_knee(3, k3)),
    "MPC monotone per-decile diagnostic": dict(mpc=mono),
    "MPC low schedule (Fig 7 upper band)": dict(mpc=LOW),
    "MPC high schedule (Fig 7 lower band)": dict(mpc=HIGH),
    "equal CU weights": dict(equal_cu=True),
    "published Fig 4 labels as nets": dict(net=F4_LABEL.values.astype(float)),
}
SENS = []
for nm, kw in tqdm(ALTS.items(), desc="alternatives", leave=False):
    r = model(**kw)
    h = headlines(r)
    brk = broken_headlines(h)
    rf = (np.nan, np.nan, np.nan) if "mpc" in kw else refit_mpc(r["net"], eta=r["eta"], Cm=r["C"], Wm=r["W"])
    SENS.append(dict(variant=nm, **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in h.items()},
                     broken=";".join(brk), qualitative=qualitative_ok(h), fig5_refit_rmse=rf[0], refit_knee=rf[1],
                     refit_top=rf[2]))
    moved = ", ".join(f"{k} {h[k]:+.2f} ({HEAD_PUB[k][0]:+g})" for k in brk) or "none"
    refit_note = "" if "mpc" in kw else f"; Fig 5 after an MPC refit: RMSE {rf[0]:.4f} (knee {rf[1]:.2f}, top {rf[2]:.4f})"
    claim(qualitative_ok(h), f"qualitative US story survives: {nm}", None,
          f"rent {h['rent']:+.2f}, health {h['health ins']:+.2f}, new {h['new cars']:+.2f}, used {h['used cars']:+.2f}, "
          f"impulse {h['impulse % cons']:.3f}%", None,
          f"at the mid MPC, printed headlines that no longer round to the post: {moved}{refit_note}", AR)
SENS = pd.DataFrame(SENS)
base_brk = broken_headlines(HBASE)
claim(base_brk == ["D10 net"], "baseline: every printed headline except D10's -$173 (CLOSE, -172.05) rounds to the post",
      "D10 -172.05 CLOSE", ", ".join(base_brk), None, "", AR)

# ----------------------------------------------------------------------------------------------------------
# 20. Adversarial review 3: MPC, betas, tuning (summary verdicts)
# ----------------------------------------------------------------------------------------------------------
AR = "review: summary"
claim(True, "MPC schedule inside the post's stated range and plausibly shaped", "knee family, mid 2.55/0.53",
      f"refit {FIT_KNEE:.2f}/{FIT_TOP:.2f}", "fn 27: 1.0 -> 0.40-0.65",
      "flat 1.0 for the bottom ~25% (hand-to-mouth), then linear; mid ~ average of low and high; fits 36 bars at the "
      "printing floor with 2 parameters. Caveat: Fig 6 says D6 and D8 sat higher in the post's own schedule", AR)
claim(True, "beta mapping faithful to the bulletin (values, equations) and documented where it is not (grouping)",
      "Table 3/4 printed values; eq. 5, eq. 11", "identical, read from the PDF", None,
      "eta is evaluated at observed decile shares (the post's fn 23), not the bulletin's fitted shares at geometric mean "
      "prices. Grouping follows CE major categories, not the bulletin's COICOP groups, for health and vehicle insurance "
      "(COICOP 12), childcare (12/social), other lodging (11.2) and vehicle finance (outside consumption): pinned by the "
      "Fig 5 ghosts and bars (COICOP grouping: bar RMSE 10x worse). Moving them would put health insurance at +1.12 and "
      "vehicle insurance at +0.57", AR)
claim(True, "nothing tuned outside a defensible range to force a match", "documented calibrations",
      "used cars 1/2, water 0.688, MPC knee/top, low/high knees", None,
      "each calibrated value sits inside its defensible interval and is sharply identified; the one non-Directive value "
      "(used cars) is the post's own and is labelled; misses are reported, not forced (Fig 4 D8/D10, impulse wording)", AR)

# ----------------------------------------------------------------------------------------------------------
# 21. Output
# ----------------------------------------------------------------------------------------------------------
out = pd.DataFrame(CLAIMS)
out.insert(0, "n", range(1, len(out) + 1))
out.to_csv(OUT_CSV, index=False)
SENS.to_csv(BOUT / "verify_independent_us_sensitivity.csv", index=False)
cur = None
for _, r in out.iterrows():
    if r["area"] != cur:
        cur = r["area"]
        print(f"\n# {cur}")
    print(" | ".join([r["status"].ljust(3), r["claim"], r["builder"], r["mine"], r["published"], r["note"]]))
n_ok, n_bad = int((out.status == "OK").sum()), int((out.status == "BAD").sum())
print(f"\nclaims: {len(out)}  OK: {n_ok}  BAD: {n_bad}")
print("BAD:")
for _, r in out[out.status == "BAD"].iterrows():
    print(f"  [{r['area']}] {r['claim']}")
print(f"written: {OUT_CSV.relative_to(CONS.parent)}, {(BOUT / 'verify_independent_us_sensitivity.csv').relative_to(CONS.parent)}")
