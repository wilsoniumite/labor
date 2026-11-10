# one_basis.py — what consumption is made of, on the same basis as what finances it (assembly 1 of SKETCH.md).
#
# The paper's two accounts are not on one basis. The financing account (the labour-origin share of personal consumption,
# ../pinning/effort/) is in incomes, which are net of depreciation. The production account it is set beside (BEA
# WP2026-01, digitized) leaves capital services as a primary input, depreciation included, and counts imported content
# apart. On the cost system's own definition a machine's wear is not a claim: it is replaced, and the replacement is made
# by labour, capital and land again. This script traces it.
#
# METHOD. BEA's make-use tables after redefinitions, summary level, 1997-2023, through the lambda thread's engine as
# ../paths/code/chains.py wraps it (build_year, cfc_ratios; the same files, the same gitignored cache). For one dollar of
# a final-use bundle the full chain resolves into compensation, taxes on production less subsidies, gross operating
# surplus and imported content; surplus splits industry by industry into consumption of fixed capital and net surplus
# (Fixed Assets over GDP by industry, capped at the surplus, as chains.py). Then each dollar of capital consumed is
# replaced by a dollar of the investment bundle that rebuilds it, whose own chain is resolved the same way, and so on:
#     housing's capital           <- residential fixed investment (F02R)
#     government's capital        <- government fixed investment (F06, F07, F10: structures, equipment, IPP)
#     every other industry's      <- private nonresidential fixed investment (F02S, F02E, F02N)
# Three linear equations close the recursion. What is left of the consumption dollar is compensation, net surplus, taxes
# and imports, and labour's share of net domestic factor cost is compensation over compensation plus net surplus.
# Proprietors' income sits in net surplus; a share psi of it is labour (0.38 in 2023 is the financing account's central
# judgment), taken at the economy-wide ratio of proprietors' income to net operating surplus (NIPA).
#
# BASES. "domp": domestic content only, imported inputs and imported final products counted as imports (the thread's
# proportional convention). "tot": imports priced as if made at United States cost shares, so nothing is imported.
#
# Run from provisioning/:  python3 code/one_basis.py [--pull]     writes data/one_basis.csv and data/one_basis_vintage.json
# The BEA files are not in the repository (gitignored cache, ../progress_and_prosperity/lambda/data/cache/); --pull
# fetches the ones that are missing from apps.bea.gov, as ../paths/code/chains.py --pull does. Gated by
# checks/check_one_basis.py.

import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(REPO, "paths", "code"))
import chains as ch  # noqa: E402  (the lambda thread's engine and the depreciation ratios)
sys.path.insert(0, HERE)
from one_basis_tables import financing, published  # noqa: E402,F401  (the two accounts this one is set beside)

FILES = ("AllTablesIO.zip", "AllTablesSUP.zip", "ValueAdded.xlsx", "GrossOutput.xlsx", "Section2All_xls.xlsx",
         "Section3All_xls.xlsx", "NipaDataA.txt")
BUNDLES = {"consumption": ["F010"],
           "business": ["F02S", "F02E", "F02N"],
           "housing": ["F02R"],
           "public": ["F06S", "F06E", "F06N", "F07S", "F07E", "F07N", "F10S", "F10E", "F10N"]}
REPLACERS = ("business", "housing", "public")
GOVERNMENT = ("GFGD", "GFGN", "GFE", "GSLG", "GSLE")
CLAIMS = ("comp", "nos", "tax", "imports")
BASES = ("domp", "tot")
PSI = (0.0, 0.38, 0.67)                    # proprietors' income counted as labour: none, the financing account's, two thirds
YEARS = list(range(1997, 2024))
NIPA_CODES = ["A191RC", "A262RC", "W271RC", "A4002C", "A041RC", "B833RC", "B846RC", "B995RC", "B986RC", "W274RC", "A054RC"]
# for code/exposure.py, which reads no gitignored file: corporate income that households do not receive
CORPORATE = {"W274RC": "undistributed_profits", "A054RC": "taxes_on_corporate_income"}


def load():
    """The tables every year reads, opened once."""
    c = ch.CACHE
    frames = (ch.open_xl("AllTablesSUP.zip", "IxC_TR_1997-2023_Summary.xlsx"),
              ch.open_xl("AllTablesIO.zip", "CxI_DR_1997-2023_Summary.xlsx"),
              ch.open_xl("AllTablesIO.zip", "IOMake_After_Redefinitions_PRO_1997-2023_Summary.xlsx"),
              ch.open_xl("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx"))
    return dict(frames=frames,
                fa24=ch.line_table(os.path.join(c, "Section2All_xls.xlsx"), "FAAt204-A"),
                fa34=ch.line_table(os.path.join(c, "Section3All_xls.xlsx"), "FAAt304ESI-A"),
                gdp=ch.tva113(os.path.join(c, "ValueAdded.xlsx")),
                go=ch.line_table(os.path.join(c, "GrossOutput.xlsx"), "TGO105-A"),
                nipa=ch.nipa_flat(os.path.join(c, "NipaDataA.txt"), NIPA_CODES))


def split(Y, f, v_cfc, basis):
    """One dollar of a final-use bundle (weights f over commodities) through the full chain: compensation, taxes, net
    surplus, imported content, and capital consumed by whose capital it is (housing, public, business)."""
    if basis == "domp":
        r = Y.TRdom @ (Y.phi * f)
        imports = float(Y.v_imp @ r + f.sum() - Y.phi @ f)
    else:
        r = Y.TR @ f
        imports = 0.0
    cfc = v_cfc * r
    hs = Y.inds.index("HS")
    gov = [Y.inds.index(i) for i in GOVERNMENT if i in Y.inds]
    worn = dict(housing=float(cfc[hs]), public=float(cfc[gov].sum()))
    worn["business"] = float(cfc.sum()) - worn["housing"] - worn["public"]
    gos = float(Y.v_gos @ r)
    return dict(comp=float(Y.v_w @ r), tax=float(Y.v_tax @ r), nos=gos - float(cfc.sum()), imports=imports, worn=worn)


def resolve(parts, bundle="consumption"):
    """Replace every dollar of capital consumed by a dollar of the bundle that rebuilds it, to the end. parts: each
    bundle's split. Returns a dollar of `bundle` as compensation, net surplus, taxes and imports."""
    A = np.array([[parts[j]["worn"][k] for k in REPLACERS] for j in REPLACERS])        # bundle j wears bundle k's capital
    out = {}
    for c in CLAIMS:
        x = np.linalg.solve(np.eye(len(REPLACERS)) - A, np.array([parts[j][c] for j in REPLACERS]))
        out[c] = parts[bundle][c] + sum(parts[bundle]["worn"][k] * x[i] for i, k in enumerate(REPLACERS))
    return out


def year_rows(tabs, yr):
    Y = ch.build_year(tabs["frames"], yr)
    us = ch.parse(tabs["frames"][3].parse(str(yr), header=None))
    ratio, per_out, _ = ch.cfc_ratios(tabs["fa34"], tabs["fa24"], tabs["gdp"], tabs["go"], tabs["nipa"], Y.inds, yr)
    v_cfc = np.array([min(ratio[i], 1.0) * g if i in ratio else per_out[i] for i, g in zip(Y.inds, Y.v_gos)])
    n = tabs["nipa"]
    v_cfc_ew = float(n["A262RC"][yr] / (n["A262RC"][yr] + n["W271RC"][yr])) * Y.v_gos       # the economy-wide ratio instead
    prop = float(n["A041RC"][yr] / n["W271RC"][yr])                    # proprietors' income over net operating surplus
    weights = {}
    for b, cols in BUNDLES.items():
        fd = us.loc[Y.coms, cols].fillna(0.0).sum(axis=1).clip(lower=0.0)
        weights[b] = (fd / fd.sum()).values
    hs_c = Y.coms.index("HS")                                          # consumption apart: shelter (housing services) and the rest
    shelter_share = float(weights["consumption"][hs_c])
    weights["shelter"] = np.eye(len(Y.coms))[hs_c]
    weights["rest"] = np.where(np.arange(len(Y.coms)) == hs_c, 0.0, weights["consumption"]) / (1.0 - shelter_share)
    rows = []
    for basis in BASES:
        for variant, v in (("central", v_cfc), ("economywide", v_cfc_ew)):
            parts = {b: split(Y, weights[b], v, basis) for b in weights}
            c0, res = parts["consumption"], resolve(parts)
            row = dict(year=yr, basis=basis, depreciation=variant, recon_err=Y.recon_err,
                       gross_comp=c0["comp"], gross_nos=c0["nos"], gross_tax=c0["tax"], gross_imports=c0["imports"],
                       worn_housing=c0["worn"]["housing"], worn_public=c0["worn"]["public"], worn_business=c0["worn"]["business"],
                       gross_sum=c0["comp"] + c0["nos"] + c0["tax"] + c0["imports"] + sum(c0["worn"].values()),
                       comp=res["comp"], nos=res["nos"], tax=res["tax"], imports=res["imports"],
                       net_sum=sum(res[c] for c in CLAIMS), prop_over_nos=prop)
            for b in REPLACERS:                                         # each replacing bundle's own compensation share
                row[f"{b}_comp"] = parts[b]["comp"]
                row[f"{b}_worn"] = sum(parts[b]["worn"].values())
            for psi in PSI:
                tag = f"{int(round(100 * psi)):02d}"
                labour = res["comp"] + psi * prop * res["nos"]
                row[f"labour_dollar_psi{tag}"] = labour                                # of the consumption dollar
                row[f"labour_factor_psi{tag}"] = labour / (res["comp"] + res["nos"])   # of net domestic factor cost
                row[f"labour_gross_psi{tag}"] = c0["comp"] + psi * prop * c0["nos"]    # before replacement is traced
            # shelter and the rest of consumption, each a dollar. Proprietors' labour is put in the rest: housing's surplus
            # is rent, interest and landlords' profit.
            sh, rs = resolve(parts, "shelter"), resolve(parts, "rest")
            row.update(shelter_share=shelter_share, shelter_comp=sh["comp"], shelter_nos=sh["nos"], shelter_tax=sh["tax"],
                       shelter_imports=sh["imports"], rest_comp=rs["comp"], rest_nos=rs["nos"], rest_tax=rs["tax"],
                       rest_imports=rs["imports"], shelter_labour_factor=sh["comp"] / (sh["comp"] + sh["nos"]))
            for psi in PSI:
                tag = f"{int(round(100 * psi)):02d}"
                row[f"rest_labour_factor_psi{tag}"] = ((rs["comp"] + psi * prop * res["nos"] / (1.0 - shelter_share))
                                                       / (rs["comp"] + rs["nos"]))
            rows.append(row)
    return rows


def vintage():
    out = {}
    for name in FILES:
        fp = os.path.join(ch.CACHE, name)
        out[name] = dict(bytes=os.path.getsize(fp), sha256_16=hashlib.sha256(open(fp, "rb").read()).hexdigest()[:16])
    return out


if __name__ == "__main__":
    from tqdm.auto import tqdm
    if "--pull" in sys.argv[1:]:
        for name in FILES:
            ch.pull(name)
    tabs = load()
    rows = []
    for yr in tqdm(YEARS):
        rows += year_rows(tabs, yr)
    out = pd.DataFrame(rows)
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    out.to_csv(os.path.join(ROOT, "data", "one_basis.csv"), index=False)
    json.dump(dict(files=vintage(), years=[YEARS[0], YEARS[-1]], bundles=BUNDLES, psi=PSI),
              open(os.path.join(ROOT, "data", "one_basis_vintage.json"), "w"), indent=1)
    corp = pd.DataFrame({name: {y: tabs["nipa"][code][y] / 1e3 for y in range(2000, 2025) if y in tabs["nipa"][code].index}
                         for code, name in CORPORATE.items()})                     # $ billions, NIPA annual flat file
    corp.index.name = "year"
    corp.to_csv(os.path.join(ROOT, "data", "nipa_corporate.csv"))

    c = out[(out.basis == "domp") & (out.depreciation == "central")].set_index("year")
    fin, pub = financing(), published()
    print("\nthe consumption dollar, domestic content (shares)")
    print("year | as counted: pay  wear  net surplus  taxes  imports | wear traced back: pay  net surplus  taxes  imports | "
          "labour's share of net factor cost (proprietors' labour 0 / 0.38 / 0.67)")
    for y in (1997, 2004, 2010, 2019, 2023):
        r = c.loc[y]
        wear = r["worn_housing"] + r["worn_public"] + r["worn_business"]
        print("%d |  %.3f  %.3f  %.3f  %.3f  %.3f |  %.3f  %.3f  %.3f  %.3f |  %.3f  %.3f  %.3f"
              % (y, r["gross_comp"], wear, r["gross_nos"], r["gross_tax"], r["gross_imports"], r["comp"], r["nos"], r["tax"],
                 r["imports"], r["labour_factor_psi00"], r["labour_factor_psi38"], r["labour_factor_psi67"]))
    print("\nagainst the financing account (2004-2023) and BEA's own grouping")
    print("year | financed by labour [bounds], beyond income | made by labour, of the dollar: as counted, wear traced | "
          "of net factor cost | BEA WP: human effort, capital, foreign")
    for y in (2004, 2010, 2019, 2023):
        r, f, p = c.loc[y], fin.loc[y], pub.loc[y]
        print("%d |  %.3f [%.3f-%.3f]  %.3f |  %.3f  %.3f |  %.3f |  %.3f  %.3f  %.3f"
              % (y, f["fin_labour"], f["fin_lower"], f["fin_upper"], f["fin_beyond_income"], r["labour_gross_psi38"],
                 r["labour_dollar_psi38"], r["labour_factor_psi38"], p["human_effort_share"], p["domestic_capital_total_share"],
                 p["foreign_content_share"]))
