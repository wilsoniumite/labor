# calibration_c.py — calibration (c) of the macro block: the machine chain at its measured labour content, side by side
# with calibrations (a) and (b) under deep automation, with the rate feedback and the sensitivity to the machine chain's
# fixed-rent share sigma — the one object that sets both the closure multiplier and the rate headroom.
#
# WHY. Calibrations (a) and (b) put almost no labour in machine services: labour's full-chain share of machine cost is 0.026
# in (a) (0.018 direct, before tracing through the machines that build machines) and ~0.002 in (b), and 2.3% / 0.1% of hours
# work in the machine chain. BEA's input-output accounts (code/chains.py) put 0.57 of a machine's build cost in full-chain
# compensation with imports priced at US cost shares (0.47 counting US labour only), and 15-18% of all compensation in the
# chain that builds fixed investment. (c) recalibrates the same Appendix B / A.4 economy to those measurements
# (macro.ChainTargets, macro.calibrate_c: closed form, every root) and reruns the paths. Her decision (2026-09-30): the
# downstream modules switch from (b) to this module's central economy, which they take from macro.central() (it re-solves
# the central targets stored in results/calibration_c.json; checks/check_calibration_c.py E1 gates it equal to the economy
# built here) with macro.deep_tech / capital_premium / feedback_bridges in place of (b)'s hard-coded 0.01 and 5.0.
#
# THE CENTRAL READING (revised after the review of 2026-09-30; the parent's decision, open to her veto). All four chain
# targets on one import basis: US labour throughout, imported content outside the labour share as a fixed-quantity cost
# ('open'; chains.py's domp). In the model that content is part of the chain's land b — paid as domestic rent and drawn
# from the endowment T that housing shares, not an elastic import at a world price (an open item, with its size measured:
# readouts.import_as_land).
#   labour 0.47 — BEA WP2026-01's human-effort share of PCE, which leaves foreign content (0.094 in 2023) in its own bucket;
#   theta_V 0.470, chain share 0.151 — the equipment + IPP + private-structures bundle on the domp basis;
#   sigma_V — the same bundle's imported content (0.185) plus its domestic fixed rent, NOS less a normal return on the
#     chain's own capital: sigma = imports + NOS - CFC x rho(sigma) / delta_chain (a fixed point; a construction), every
#     piece from the bundle's own cost split (chains.py G1: targets_for_macro['g1_equipment_ipp_structures_full_chain']).
# Why: it is one of two basis-consistent readings (open and tot-consistent: each puts all four chain targets on one import
# basis); it is preferred because the tot-consistent reading has no root at g0 0.01 (it needs g0 <= 0.0080) and its return,
# 0.0504, lies below the NIPA band [(NOS - site)/K, (NOS + taxes - site)/K], while the open reading's 0.0755 lies inside it
# (check M8); its rate headroom (7.2 / 7.9 pp) is consistent with economies that survive large rises in real rates. Named
# variants, each with both roots in k:
#   tot-consistent — labour grossed up for PCE's foreign content, 0.47/(1 - 0.094) = 0.519 (imports at the domestic PCE
#     chain's labour share), theta_V 0.569 and chain share 0.183 on tot, sigma = NOS - CFC rho/delta_chain from the tot
#     split. It has no root at g0 0.01 (it needs g0 <= 0.0080) and runs at g0 0.005;
#   mixed basis — severe bound (of the three basis readings) — labour 0.47 (US labour only) against the tot theta_V and chain
#     share: the pre-review central, with sigma now from the bundle's own tot split;
#   pre-review central (superseded) — the mixed basis with sigma from the machinery + software set's split (a different
#     scope: theta 0.617, not the bundle's 0.569); kept only to trace the change;
#   the open sigma bracket — imported content only (the chain's domestic NOS all a normal return) / NOS + imports;
#   (ii) the site at its measured flow; her four read literally (traced basis, g0 0.02); equipment + IPP without structures
#     (its own split); two deltas (these hold the central sigma);
#   a sweep over sigma_V at the central targets, over its whole admissible range (0, 1 - theta_V), and the sigma at which the
#     rate headroom is 5 pp on each basis reading.
# Comparators: (a) and (b) as stored (macro.calibrate: the low root) and their other root (macro.calibrate_roots, closed form;
# calibrate() unchanged), (b) at g0 0.01 (both roots) — the like-for-like comparator for (c)'s g0 — and (b) calibrated at the
# measured site (the site as 4.2% of GDP, macro.calibrate_roots(site_basis='gdp'); g0 0.02 and 0.01, both roots) — the
# like-for-like comparator for variant (ii), whose site is measured.
# Probes of the open reading (readouts): imported content as land (its share of sigma, the chain's share of T along the
# path, the rent paid on it) and the consumption chain's own foreign content (0.094 of PCE) moved out of capital services
# into a site-like fixed rent in the basket (the central's sigma held).
#
# STRUCTURE.
#   1. Data, BEA's own files (the gitignored lambda cache; pulled if missing): Fixed Assets Section 1 — Tables 1.1
#      (current-cost net stock), 1.3 (depreciation), 1.5 (investment), lines matched by number and name text;
#      delta(scope, year) = depreciation / mean of the two yearend net stocks. NIPA annual flat file, codes verified against
#      SeriesRegister.txt: GDP A191RC, GDI A261RC, CFC A262RC, compensation A4002C, taxes on production and imports less
#      subsidies W254RC, net operating surplus W271RC, PCE housing DHSGRC. Site-rent flow = land share (0.30 / 0.50) x PCE
#      housing / GDP, the flow-side lower bound of pinning/code/feasibility_kappa.py (non-housing site rent omitted).
#      WP2026-01's 2023 PCE decomposition (human effort 0.4723, foreign content 0.0936) from the repository's digitisation of
#      its Figure 9 (pinning/effort/archive_v28/inputs/dq/D_Q11_...csv; approximate, not BEA microdata).
#   2. Targets, read from results/chains.json (Unit 1; never recomputed here; each number's source key is recorded):
#      economy['2023'] theta and compensation share of the bundle on tot and domp; the bundle's full cost split, hours shares
#      and CFC variants from targets_for_macro['g1_equipment_ipp_structures_full_chain']; equipment + IPP from
#      bundles['equipment_ipp']; the machinery + software set's tot split (the pre-review sigma only); delta_chain = BEA's
#      private equipment + IPP depreciation rate (Unit 1). Scope check: chain share = theta_V x NIPA CFC / compensation.
#   3. Economies: (a), (b) and their second roots; (b) at g0 0.01; (b) at the measured site (g0 0.02, 0.01); (c) at each
#      variant, both roots in k.
#   4. Runs (quasi-static, as macro_scenarios): capability eta 1 -> 0.04, lambda to a fifth of its start (0.05 -> 0.01 in
#      (a)/(b); macro.deep_tech), at macro_scenarios' three speeds; the decomposition (capability only, lambda only); static +-100 / +200 bp on
#      the required return, the rate headroom, sustained +100 / +200 bp with the return following r*, and the loop (return
#      following r* against a fixed return); the sigma sweep and the 5 pp headroom bound.
# LABELS. Labour's share on the paper's Figure 7 basis is v(1 - x)/Ps under A.4's capital (labour_share_bea) and v n / income
# in (a)'s flow benchmark (rho 0, delta 1: the machine chain is a within-period intermediate), so (a) is shown on labor_share.
# chain_share is the chain's share of compensation (effective labour: the model has one wage); the measured hours share is
# quoted beside it. BRIDGES. The (c) tags run on the bridges refit on (c) (macro.Bridges(); Log 46: r* keyed to replacement
# investment / income, owners' saving and deficits on one evidence-based scale, the fiscal start at the measured primary
# deficit); (a), (b) and (b)'s variants on the bridges as tuned on (b) (macro.BRIDGES_B: the pace key), so they stay the
# pre-switch runs (bridges_for).
#
# Run from paths/:  ../venv/Scripts/python.exe code/calibration_c.py   (clean under -W error: every file is closed)
# Out: results/calibration_c.json, figures/fig_calibration_c.png

from __future__ import annotations

import csv
import json
import os
import sys
from dataclasses import asdict, replace

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
sys.path.insert(0, HERE)
import macro as m  # noqa: E402

CACHE = os.path.join(REPO, "progress_and_prosperity", "lambda", "data", "cache")
URLS = {"Section1All_xls.xlsx": "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section1All_xls.xlsx",
        "NipaDataA.txt": "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt",
        "SeriesRegister.txt": "https://apps.bea.gov/national/Release/TXT/SeriesRegister.txt"}
WP_DQ11 = ("pinning", "effort", "archive_v28", "inputs", "dq", "D_Q11_bea_wp2026_fullchain_consumption_grouped_1997_2023_digitized.csv")
YEAR = 2023
FA_SHEETS = {"stock": ("FAAt101-A", "Table 1.1. Current-Cost Net Stock of Fixed Assets"),
             "dep": ("FAAt103-A", "Table 1.3. Current-Cost Depreciation of Fixed Assets"),
             "inv": ("FAAt105-A", "Table 1.5. Investment in Fixed Assets")}
FA_LINES = {"all": (2, "Fixed assets"), "private": (3, "Private"), "private_nonres": (4, "Nonresidential"),
            "equipment": (5, "Equipment"), "structures": (6, "Structures"), "ipp": (7, "Intellectual property products"),
            "residential": (8, "Residential"), "government": (9, "Government")}
NIPA = {"gdp": ("A191RC", "Gross domestic product"), "gdi": ("A261RC", "Gross domestic income"),
        "cfc": ("A262RC", "Consumption of fixed capital"), "comp": ("A4002C", "Compensation of employees, paid"),
        "tax": ("W254RC", "Taxes on production and imports less subsidies"), "nos": ("W271RC", "Net operating surplus"),
        "housing": ("DHSGRC", "Housing")}
LAND_SHARES = (0.30, 0.50)
LABOUR = 0.47                   # her labour share (WP2026-01's human effort, 2023, rounded)
G0_CENTRAL = 0.01               # her 0.02 has no root on the BEA basis at measured values
G0_TOT = 0.005                  # the tot-consistent reading needs g0 <= 0.0080; half the central's keeps its two roots apart
SPEEDS = m.TECH_SPEEDS          # slow / medium / fast: macro_scenarios.SPEEDS's clocks
ETA_END = 0.04
DATES = (0.0, 3.0, 6.0, 10.0, 15.0)
SIGMA_SWEEP = (0.03, 0.05, 0.07, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50)
HEADROOM_TEST_PP = 5.0          # a sustained rise in the required return the economy is taken to survive (Volcker-sized)
BASIS_READINGS = ("c_central", "c_tot", "c_mixed")


# ------------------------------------------------------------------ data (BEA's own files)
def pull(name: str) -> str:
    fp = os.path.join(CACHE, name)
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        return fp
    import truststore
    truststore.inject_into_ssl()
    import requests
    r = requests.get(URLS[name], timeout=600)
    if r.status_code != 200 or len(r.content) < 1000:
        raise SystemExit(f"BLOCKED: {name} http {r.status_code}")
    os.makedirs(CACHE, exist_ok=True)
    with open(fp, "wb") as f:
        f.write(r.content)
    return fp


def fixed_assets():
    """{kind: {scope: {year: $ billions}}} from FA Section 1; every line matched on its number and its name text."""
    import openpyxl
    wb = openpyxl.load_workbook(pull("Section1All_xls.xlsx"), read_only=True)
    out = {}
    for kind, (sheet, title) in FA_SHEETS.items():
        rows = list(wb[sheet].iter_rows(values_only=True))
        if not str(rows[0][0]).startswith(title):
            raise SystemExit(f"FA sheet {sheet}: title {rows[0][0]!r} is not {title!r}")
        head = next(r for r in rows if r and r[0] == "Line")
        col = {int(v): i for i, v in enumerate(head) if isinstance(v, str) and v.isdigit()}
        out[kind] = {}
        for scope, (line, name) in FA_LINES.items():
            r = next(r for r in rows if r and r[0] == str(line))
            if str(r[1]).strip() != name:
                raise SystemExit(f"FA {sheet} line {line}: {r[1]!r} is not {name!r}")
            out[kind][scope] = {y: float(r[i]) / 1e3 for y, i in col.items() if isinstance(r[i], (int, float))}
    return out


def fa_delta(fa, scopes, y=YEAR):
    """Current-cost depreciation over the mean of the two yearend current-cost net stocks, summed over `scopes`."""
    dep = sum(fa["dep"][s][y] for s in scopes)
    stock = sum(0.5 * (fa["stock"][s][y - 1] + fa["stock"][s][y]) for s in scopes)
    return dep / stock


def nipa():
    """{role: {year: $ billions}} from the NIPA annual flat file; each code's label checked against the register."""
    reg = {}
    with open(pull("SeriesRegister.txt"), encoding="utf-8") as f:
        for row in csv.reader(f):
            if row and not row[0].startswith("%"):
                reg[row[0]] = row[1]
    for role, (code, label) in NIPA.items():
        if reg.get(code) != label:
            raise SystemExit(f"NIPA {role}: {code} is {reg.get(code)!r} in SeriesRegister.txt, not {label!r}")
    want = {code: role for role, (code, _) in NIPA.items()}
    out = {role: {} for role in NIPA}
    with open(pull("NipaDataA.txt"), encoding="utf-8") as f:
        for row in csv.reader(f):
            if row and row[0] in want and row[1].isdigit():
                out[want[row[0]]][int(row[1])] = float(row[2].replace(",", "")) / 1e3
    return out


def wp2026(y=YEAR):
    """WP2026-01's PCE decomposition for year y from the repository's digitisation of its Figure 9 (approximate)."""
    fp = os.path.join(REPO, *WP_DQ11)
    with open(fp, encoding="utf-8") as f:
        row = next(r for r in csv.DictReader(f) if r["year"] == str(y))
    he, dk, fc = (float(row[k]) for k in ("human_effort_share", "domestic_capital_total_share", "foreign_content_share"))
    return dict(human_effort=he, domestic_capital=dk, foreign_content=fc, labour_tot=LABOUR / (1.0 - fc),
                labour_tot_digitised=he / (1.0 - fc), source="/".join(WP_DQ11) + f" (year {y}; digitised from BEA WP2026-01 "
                "Figure 9, approximate)", tot_construction="labour / (1 - foreign content): imports at the domestic PCE "
                "chain's labour share, the PCE analogue of chains.py's tot basis (imports priced at US cost shares)")


def inputs():
    """Every number (c) is built on, with where it came from."""
    fa, ni = fixed_assets(), nipa()
    with open(os.path.join(ROOT, "results", "chains.json"), encoding="utf-8") as f:
        CJ = json.load(f)
    src = {}

    def take(name, *path):
        v = CJ
        for p in path:
            v = v[p]
        src[name] = {"value": float(v), "source": "results/chains.json " + "".join(f"[{p!r}]" for p in path)}
        return float(v)

    E = ("economy", "2023")
    G = ("targets_for_macro", "g1_equipment_ipp_structures_full_chain")
    Q = ("bundles", "equipment_ipp", "2023")
    S = ("targets_for_macro", "d_cost_split_machinery_software_set_investment_weighted_tot")
    t = {}
    for b in ("tot", "domp"):
        t[f"theta_{b}"] = take(f"theta_V_{b}", *E, f"inv_equipment_ipp_structures_theta_{b}")
        t[f"share_{b}"] = take(f"chain_share_{b}", *E, f"inv_equipment_ipp_structures_comp_{b}_share_of_total_comp")
        for q in ("theta", "cfc", "tax", "nos", "imports"):
            t[f"g1_{q}_{b}"] = take(f"bundle_{q}_{b}", *G, f"{q}_{b}", "2023")
        for q in ("uncapped", "economywide"):
            t[f"g1_cfc_{b}_{q}"] = take(f"bundle_cfc_{b}_{q}", *G, f"cfc_{b}_{q}", "2023")
        t[f"g1_comp_share_{b}"] = take(f"bundle_comp_share_{b}", *G, f"comp_share_of_total_comp_{b}", "2023")
        t[f"hours_fte_{b}"] = take(f"bundle_hours_share_fte_{b}", *G, f"hours_share_of_total_hours_fte_{b}", "2023")
        t[f"hours_bridged_{b}"] = take(f"bundle_hours_share_bridged_{b}", *G, f"hours_share_of_total_hours_bridged_{b}", "2023")
        t[f"floor_{b}"] = take(f"bundle_multiplier_floor_{b}", *G, f"multiplier_floor_any_sigma_{b}", "2023")
    t["eqipp_theta_domp"] = take("eqipp_theta_V_domp", *E, "inv_equipment_ipp_theta_domp")
    t["eqipp_share_domp"] = take("eqipp_chain_share_domp", *E, "inv_equipment_ipp_comp_domp_share_of_total_comp")
    for q in ("theta", "cfc", "nos", "imports"):
        t[f"eqipp_{q}_domp"] = take(f"eqipp_{q}_domp", *Q, f"{q}_domp")
    for q in ("theta", "cfc", "tax", "nos"):
        t[f"set_{q}_tot"] = take(f"set_{q}_tot", *S, q, "2023")
    t["set_theta_domp"] = take("set_theta_domp", "targets_for_macro", "a_theta_V_machinery_software_set_investment_weighted",
                               "domp_2023")
    t["delta_chain"] = take("delta_chain_equipment_ipp_private", "targets_for_macro", "e_delta_equipment_ipp_private", "2023")
    t["delta_chain_unit1"] = take("delta_equipment_ipp_unit1", "delta_aggregates", "equipment + IPP (private nonresidential)", "2023")
    t["cfc_gdp"] = take("nipa_cfc_over_gdp", "nipa_ratios", "2023", "cfc_over_gdp")
    t["comp_gdp"] = take("nipa_comp_over_gdp", "nipa_ratios", "2023", "comp_over_gdp")
    for p in ("P25", "P50", "P75"):
        t[f"hpr_{p}"] = take(f"hours_per_hour_replaced_{p}", "per_income", "2023", "rows", "machinery_software_set|investment|tot",
                             "service_rho_0.0575", "central_relative_hours_worked", p)
    y = YEAR
    delta = {s: fa_delta(fa, [s]) for s in FA_LINES}
    delta["equipment_ipp"] = fa_delta(fa, ["equipment", "ipp"])
    site = {ls: ls * ni["housing"][y] / ni["gdp"][y] for ls in LAND_SHARES}
    site_mid = 0.5 * (site[0.30] + site[0.50])
    K_all = 0.5 * (fa["stock"]["all"][y - 1] + fa["stock"]["all"][y])
    site_mid_usd = site_mid * ni["gdp"][y]
    nat = dict(gdp=ni["gdp"][y], comp_gdp=ni["comp"][y] / ni["gdp"][y], cfc_gdp=ni["cfc"][y] / ni["gdp"][y],
               nos_gdp=ni["nos"][y] / ni["gdp"][y], tax_gdp=ni["tax"][y] / ni["gdp"][y], cfc_comp=ni["cfc"][y] / ni["comp"][y],
               K_gdp=K_all / ni["gdp"][y], fa_dep_over_nipa_cfc=fa["dep"]["all"][y] / ni["cfc"][y],
               rho_band=[(ni["nos"][y] - site_mid_usd) / K_all, (ni["nos"][y] + ni["tax"][y] - site_mid_usd) / K_all],
               site_gdp={str(k): v for k, v in site.items()}, site_gdp_mid=site_mid)
    return dict(fa=fa, nipa=ni, chains=t, sources=src, delta=delta, nat=nat, wp=wp2026())


# ------------------------------------------------------------------ the economies
def sigma_fixed_point(tg, split, delta_chain):
    """sigma = imports + NOS - CFC x rho(sigma) / delta_chain on one cost split (imports 0 on tot): the fixed-quantity share
    of build cost, the chain's own NOS less a normal return on its own capital, plus (open) its imported content. rho from
    calibrate_c (the adding-up pins it; both roots in k share it); iterated to |change| < 1e-12."""
    for _ in range(200):
        e, _info = m.calibrate_c(tg)[0]
        s_new = split["imports"] + split["nos"] - split["cfc"] * e.rho / delta_chain
        if abs(s_new - tg.sigma_V) < 1e-12:
            return tg
        tg = replace(tg, sigma_V=s_new)
    raise RuntimeError("sigma fixed point did not converge")


def variants(I):
    """name -> dict(tg, label, bases (the import basis of labour, theta_V, chain_share, sigma_V), mixed, superseded,
    sigma (its construction), imports and cfc (the scope's cost split on the basis of theta_V))."""
    t, d_all, dc = I["chains"], I["delta"]["all"], I["chains"]["delta_chain"]
    split = {b: dict(nos=t[f"g1_nos_{b}"], cfc=t[f"g1_cfc_{b}"], imports=t[f"g1_imports_{b}"]) for b in ("tot", "domp")}
    open_ = sigma_fixed_point(m.ChainTargets(theta_V=t["theta_domp"], chain_share=t["share_domp"], sigma_V=0.3, delta=d_all,
                                             labour=LABOUR, g0=G0_CENTRAL), split["domp"], dc)
    tot0 = m.ChainTargets(theta_V=t["theta_tot"], chain_share=t["share_tot"], sigma_V=0.15, delta=d_all, labour=LABOUR, g0=G0_CENTRAL)
    mixed = sigma_fixed_point(tot0, split["tot"], dc)
    tot = sigma_fixed_point(replace(tot0, labour=I["wp"]["labour_tot"], g0=G0_TOT), split["tot"], dc)
    pre = sigma_fixed_point(replace(tot0, sigma_V=0.09), dict(nos=t["set_nos_tot"], cfc=t["set_cfc_tot"], imports=0.0), dc)
    eq = sigma_fixed_point(replace(open_, theta_V=t["eqipp_theta_domp"], chain_share=t["eqipp_share_domp"]),
                           dict(nos=t["eqipp_nos_domp"], cfc=t["eqipp_cfc_domp"], imports=t["eqipp_imports_domp"]), dc)
    O = dict(labour="domp", theta_V="domp", chain_share="domp", sigma_V="domp")
    T = dict(labour="tot", theta_V="tot", chain_share="tot", sigma_V="tot")
    M = dict(labour="domp", theta_V="tot", chain_share="tot", sigma_V="tot")
    fp_o = "imports + NOS - CFC x rho(sigma) / delta_chain, the bundle's domp split (fixed point)"
    fp_t = "NOS - CFC x rho(sigma) / delta_chain, the bundle's tot split (fixed point)"
    held = "held at the central's value (isolates the one change)"
    oc = dict(imports=t["g1_imports_domp"], cfc=t["g1_cfc_domp"])
    tc = dict(imports=0.0, cfc=t["g1_cfc_tot"])
    V = {"c_central": dict(tg=open_, label="central: the open reading — US labour throughout, imported content outside the labour "
                                            "share as a fixed-quantity cost (domp; in the model, part of the chain's land)", bases=O,
                           sigma=fp_o, **oc),
         "c_tot": dict(tg=tot, label=f"tot-consistent: labour {I['wp']['labour_tot']:.3f} (0.47 grossed up for PCE's foreign "
                                     f"content), theta_V and chain share on tot, g0 {G0_TOT}", bases=T, sigma=fp_t, **tc),
         "c_mixed": dict(tg=mixed, label="mixed basis — severe bound (of the three basis readings): labour 0.47 (US labour only) "
                                         "against the tot theta_V and chain share", bases=M, mixed=True, sigma=fp_t, **tc),
         "c_prereview": dict(tg=pre, label="pre-review central (superseded): the mixed basis with sigma from the machinery + "
                                           "software set's tot split (scope-mismatched: theta 0.617, not the bundle's 0.569)",
                             bases=M, mixed=True, superseded=True, sigma="NOS - CFC x rho(sigma) / delta_chain, the machinery + "
                             "software set's tot split (fixed point)", **tc),
         "c_sig_imports": dict(tg=replace(open_, sigma_V=t["g1_imports_domp"]), label="open sigma bracket, low end: imported "
                               "content only (the chain's domestic NOS all a normal return)", bases=O, sigma="imports (domp)", **oc),
         "c_sig_nosimports": dict(tg=replace(open_, sigma_V=t["g1_nos_domp"] + t["g1_imports_domp"]), label="open sigma bracket, "
                                  "high end: NOS + imported content (no normal return)", bases=O, sigma="NOS + imports (domp)", **oc),
         "c_site": dict(tg=replace(open_, site=I["nat"]["site_gdp_mid"], site_basis="gdp"), label="(ii) the site at its measured "
                        "flow (4.2% of GDP)", bases=O, sigma=held, **oc),
         "c_traced_g02": dict(tg=replace(open_, basis="traced", g0=0.02), label="her four read literally: labour 0.47 on the "
                              "traced basis (v n / income), g0 0.02", bases=O, sigma=held, **oc),
         "c_eqipp": dict(tg=eq, label="scope: equipment + IPP without structures (its own theta, chain share and split, domp)",
                         bases=O, sigma="imports + NOS - CFC x rho(sigma) / delta_chain, equipment + IPP's own domp split (fixed point)",
                         imports=t["eqipp_imports_domp"], cfc=t["eqipp_cfc_domp"]),
         "c_dnonres": dict(tg=replace(open_, delta=I["delta"]["private_nonres"]), label="delta: private nonresidential",
                           bases=O, sigma=held, **oc),
         "c_deqipp": dict(tg=replace(open_, delta=I["delta"]["equipment_ipp"]), label="delta: private equipment + IPP",
                          bases=O, sigma=held, **oc)}
    for v in V.values():
        v.setdefault("mixed", False)
        v.setdefault("superseded", False)
    return V


def economies(I, V):
    """tag -> dict(e, tg, info, variant, root). (a), (b) from macro.calibrate (the low root) and their high roots from
    macro.calibrate_roots; (b) at g0 0.01, both roots; (b) at the measured site (the site as its measured flow, 4.2% of GDP,
    as variant (ii) reads it: macro.calibrate_roots(site_basis='gdp')) at g0 0.02 (b_site) and 0.01 (b_site_g001), both
    roots; (c) tags end _lo / _hi (low / high root in k)."""
    ea, _, _, _ = m.calibrate()
    eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    out = {"a": dict(e=ea, tg=None, info=None, variant=None, root="lo"), "b": dict(e=eb, tg=None, info=None, variant=None, root="lo")}
    for name, base in (("a", m.CALIBRATION_BASE), ("b", m.CAPITAL_BASE), ("b_g001", replace(m.CAPITAL_BASE, g0=0.01, g1=0.99))):
        sols = m.calibrate_roots(base=base)
        if len(sols) != 2:
            raise RuntimeError(f"{name}: {len(sols)} roots in k, not 2")
        for j, (e, info) in enumerate(sols):
            if name in ("a", "b") and j == 0:
                out[name]["info"] = info                  # the stored economy stays macro.calibrate()'s own
                continue
            out[f"{name}_{'lo' if j == 0 else 'hi'}" if name == "b_g001" else f"{name}_hi"] = dict(e=e, tg=None, info=info,
                                                                                                    variant=None, root="lo" if j == 0 else "hi")
    site = {"site_share": I["nat"]["site_gdp_mid"]}
    for name, base in (("b_site", m.CAPITAL_BASE), ("b_site_g001", replace(m.CAPITAL_BASE, g0=0.01, g1=0.99))):
        sols = m.calibrate_roots(targets=site, base=base, site_basis="gdp")
        if len(sols) != 2:
            raise RuntimeError(f"{name}: {len(sols)} roots in k, not 2")
        for j, (e, info) in enumerate(sols):
            r = "lo" if j == 0 else "hi"
            out[f"{name}_{r}"] = dict(e=e, tg=None, info=info, variant=None, root=r)
    for name, v in V.items():
        for j, (e, info) in enumerate(m.calibrate_c(v["tg"])):
            out[f"{name}_{'lo' if j == 0 else 'hi'}"] = dict(e=e, tg=v["tg"], info=info, variant=name, root="lo" if j == 0 else "hi")
    return out


HEADLINE_C = tuple(f"{n}_{r}" for n in ("c_central", "c_tot", "c_mixed", "c_sig_imports", "c_sig_nosimports", "c_site") for r in ("lo", "hi"))
RATE_TAGS = ("b", "b_hi") + tuple(f"{n}_{r}" for n in ("c_central", "c_tot", "c_mixed", "c_sig_imports", "c_sig_nosimports")
                                  for r in ("lo", "hi"))
TABLE = ("b", "b_hi", "b_g001_lo", "b_g001_hi", "c_central_lo", "c_central_hi", "c_tot_lo", "c_tot_hi", "c_mixed_lo", "c_mixed_hi",
         "c_site_lo", "c_site_hi", "b_site_g001_lo", "b_site_g001_hi", "b_site_lo", "b_site_hi", "c_prereview_lo", "c_prereview_hi")
B_LABELS = {"b": "(b) as stored (low root)", "b_hi": "(b), its other root", "b_g001_lo": "(b) at g0 0.01, low root",
            "b_g001_hi": "(b) at g0 0.01, high root", "b_site_lo": "(b) at the measured site (4.2% of GDP), low root",
            "b_site_hi": "(b) at the measured site, high root", "b_site_g001_lo": "(b) at the measured site and g0 0.01, low root",
            "b_site_g001_hi": "(b) at the measured site and g0 0.01, high root"}


def tech(tag, e, speed, eta_end=ETA_END, lam_end=None):
    """The deep-automation clock, macro.deep_tech: lambda ends at a fifth of its start (0.05 -> 0.01 exactly in (a)/(b),
    macro_scenarios' 0.01); lam_end overrides it (the decomposition). tag is kept for the callers' readability."""
    if lam_end is None:
        return m.deep_tech(e, eta_end=eta_end, **SPEEDS[speed])
    return m.TechPath(eta_end=eta_end, lam_end=lam_end, **SPEEDS[speed])


def flow_benchmark(e):
    return e.rho == 0.0 and e.delta == 1.0


def bridges_for(tag):
    """The bridges a tag runs on: (a), (b) and (b)'s variants on the bridges as tuned on (b) (macro.BRIDGES_B), so they stay the
    pre-switch runs; every (c) tag on the refit (macro.Bridges(); Log 46)."""
    return m.BRIDGES_B if tag.split("_")[0] in ("a", "b") else m.Bridges()


def describe(e, theta_data=None, imports=0.0, cfc_data=None):
    """The calibrated start in national-accounts terms (GDP_m = income + replacement investment; GDP net of the chain's
    imported content, which NIPA's GDP excludes, for the open reading)."""
    q = m.solve(e)
    Vk = q["Vm"] * q["K"]
    inv = e.delta * Vk
    gdp = q["income"] + inv
    gdp_net = gdp - imports * inv
    u = e.delta / (e.rho + e.delta)
    fig7 = q["labor_share"] if flow_benchmark(e) else q["labour_share_bea"]
    d = dict(params={k: float(v) for k, v in asdict(e).items()}, x=q["x"], x_ceiling=q["x_ceiling"],
             theta_V=q["theta_V"], kappa_V=q["kappa_V"], sigma_V=q["sigma_V"], multiplier=q["multiplier"],
             multiplier_floor_any_sigma=1.0 / (1.0 - q["theta_V"]), rate_elasticity_of_w_over_r=1.0 / q["sigma_V"],
             labor_share=q["labor_share"], labour_share_bea=q["labour_share_bea"], labour_share_fig7=fig7,
             fig7_basis="labor_share (flow benchmark)" if flow_benchmark(e) else "labour_share_bea", chain_share=q["chain_share"],
             participation=q["participation"], real_wage=q["real_wage"], site_basket=e.h / q["Ps"],
             site_income=e.h * q["Y"] / q["income"], site_gdp=e.h * q["Y"] / gdp, interest_share=q["capital_share"],
             K_gdp=Vk / gdp, cfc_gdp=inv / gdp, comp_gdp=q["v"] * q["n"] / gdp, gdp_net_over_gdp=gdp_net / gdp,
             K_gdp_net=Vk / gdp_net, cfc_gdp_net=inv / gdp_net, comp_gdp_net=q["v"] * q["n"] / gdp_net, inv_income=q["inv_income"],
             a_delta=e.a * e.delta, a_rho_plus_sigma=e.a * e.rho + q["sigma_V"], rho_over_delta=e.rho / e.delta,
             hours_per_hour_replaced=q["theta_V"] * u / (1.0 - e.a * e.delta), headroom_pp=m.rate_headroom(e),
             appendix_b_assumption_at_1=1.0 - (e.rho + e.delta) * (e.a + e.lam * e.gamma(1.0)))
    if theta_data is not None and cfc_data is not None:
        d["hours_per_hour_replaced_matched_data"] = theta_data * u / (1.0 - cfc_data)
    return d


# ------------------------------------------------------------------ runs
def summarise(e, mp):
    t = mp["t"]
    at = {d: int(np.argmin(np.abs(t - d))) for d in DATES}
    site = e.h * mp["Y"] / mp["income"]
    rw, lsb = mp["real_wage"], mp["labour_share_bea"]
    f7 = mp["labor_share"] if flow_benchmark(e) else lsb
    ip = int(np.argmax(rw))
    below = np.nonzero(lsb <= 0.5 * lsb[0])[0]
    below7 = np.nonzero(f7 <= 0.5 * f7[0])[0]
    inv = e.delta * mp["Vm"] * mp["K"] / mp["income"]
    series = dict(participation=mp["participation"], real_wage=rw, real_wage_index=rw / rw[0], labor_share=mp["labor_share"],
                  labour_share_bea=lsb, labour_share_fig7=f7, chain_share=mp["chain_share"], interest_share=mp["capital_share"],
                  site_share=site, multiplier=mp["multiplier"], inv_income=inv, r_star=mp["r_star"], debt=mp["debt"], x=mp["x"])
    out = {k: {str(d): float(v[i]) for d, i in at.items()} for k, v in series.items()}
    out.update(real_wage_peak=float(rw[ip]), real_wage_peak_year=float(t[ip]), real_wage_peak_over_start=float(rw[ip] / rw[0]),
               labour_share_bea_halves_year=float(t[below[0]]) if len(below) else None,
               labour_share_fig7_halves_year=float(t[below7[0]]) if len(below7) else None,
               fig7_basis="labor_share (flow benchmark)" if flow_benchmark(e) else "labour_share_bea",
               w_over_r_end_over_start=float(mp["v"][-1] / mp["v"][0]), r_star_max=float(mp["r_star"].max()),
               r_star_max_year=float(t[int(np.argmax(mp["r_star"]))]))
    return out


def path_prefix(e, tp, br=m.Bridges(), years=15.0, dt=0.25):
    """macro_path, or its longest prefix that solves when a date has no land-scarce equilibrium (each date's
    equilibrium depends only on the past, so a shorter run is a prefix of the longer one)."""
    try:
        return m.macro_path(e, tp, br, years, dt), years, None
    except m.NoEquilibrium as ex:
        err = str(ex)
    for yrs in np.arange(years - dt, dt - 1e-9, -dt):
        try:
            return m.macro_path(e, tp, br, float(yrs), dt), float(yrs), err
        except m.NoEquilibrium:
            continue
    return None, None, err


def static_shock(e, bp):
    q0 = m.solve(e)
    try:
        q1 = m.solve(replace(e, rho=e.rho + bp / 1e4))
    except m.NoEquilibrium as ex:
        return dict(solved=False, error=str(ex))
    return dict(solved=True, dx_pp=(q1["x"] - q0["x"]) * 100, d_labour_share_pp=(q1["labor_share"] - q0["labor_share"]) * 100,
                d_labour_share_bea_pp=(q1["labour_share_bea"] - q0["labour_share_bea"]) * 100,
                d_ln_w_over_r=float(np.log(q1["v"] / q0["v"])), d_participation_pp=(q1["participation"] - q0["participation"]) * 100)


def premium(e, br=m.Bridges()):
    """The capital premium that makes the feedback path start at the economy's own required return (macro.capital_premium)."""
    return m.capital_premium(e, br)


def rate_tests(tag, e):
    tp = tech(tag, e, "medium")
    br = bridges_for(tag)
    prem = premium(e, br)
    out = {"static": {f"{bp:+d}bp": static_shock(e, bp) for bp in (-100, 100, 200)}, "headroom_pp": m.rate_headroom(e),
           "capital_premium_pp": prem}
    fixed = m.macro_path(e, tp, br)
    follow, yrs_f, err_f = path_prefix(e, tp, replace(br, capital_premium=prem))
    out["follow_solved_years"], out["follow_error"] = yrs_f, err_f
    for bp in (100, 200):
        sh, yrs, err = path_prefix(e, tp, replace(br, capital_premium=prem, rho_shift=bp / 100))
        rec = dict(solved_years=yrs, error=err)
        if sh is not None and follow is not None:
            n = min(len(sh["t"]), len(follow["t"]))
            dx = (sh["x"][:n] - follow["x"][:n])[1:]
            dl = (sh["labor_share"][:n] - follow["labor_share"][:n])
            rec.update(dx_pp_min=float(dx.min() * 100) if len(dx) else None, dx_pp_max=float(dx.max() * 100) if len(dx) else None,
                       slows_every_date=bool(np.all(dx < 0)) if len(dx) else None,
                       d_labour_share_pp_max=float(dl.max() * 100), d_labour_share_pp_start=float(dl[0] * 100))
        out[f"sustained_{bp:+d}bp"] = rec
    if follow is not None and yrs_f == 15.0:
        gap = follow["x"] - fixed["x"]
        r_dev = follow["rho"] - fixed["rho"]
        mask = np.abs(r_dev) > 0.05
        out["loop"] = dict(corr=float(np.corrcoef(r_dev[mask], gap[mask])[0, 1]) if mask.sum() > 2 else None,
                           tasks_ahead_year15_pp=float(gap[-1] * 100), rho_dev_min_pp=float(r_dev.min()),
                           rho_dev_max_pp=float(r_dev.max()), n_dates=int(mask.sum()))
    return out


def sweep_row(tg, s, j, e):
    mp = m.macro_path(e, tech("c", e, "medium"))
    S = summarise(e, mp)
    up = static_shock(e, 100)
    return dict(sigma_V=s, root="lo" if j == 0 else "hi", k=e.k, rho=e.rho, multiplier=1 + tg.theta_V / s,
                multiplier_numeric=m.solve(e)["multiplier"], participation_y6=S["participation"]["6.0"],
                participation_y15=S["participation"]["15.0"], real_wage_index_y15=S["real_wage_index"]["15.0"],
                real_wage_peak_year=S["real_wage_peak_year"], real_wage_peak_over_start=S["real_wage_peak_over_start"],
                w_over_r_end_over_start=S["w_over_r_end_over_start"],
                labour_share_fig7_halves_year=S["labour_share_fig7_halves_year"],
                d_labour_share_100bp_pp=up.get("d_labour_share_pp"), headroom_pp=m.rate_headroom(e))


def sigma_sweep(V):
    """sigma_V over its admissible range (0, 1 - theta_V) at the central targets, plus the central value and the open bracket."""
    c = V["c_central"]["tg"]
    special = {round(c.sigma_V, 6), round(V["c_sig_imports"]["tg"].sigma_V, 6), round(V["c_sig_nosimports"]["tg"].sigma_V, 6)}
    rows = []
    for s in sorted(set(SIGMA_SWEEP) | special):
        tg = replace(c, sigma_V=s)
        try:
            sols = m.calibrate_c(tg)
        except ValueError as ex:
            rows.append(dict(sigma_V=s, error=str(ex)))
            continue
        rows += [sweep_row(tg, s, j, e) for j, (e, _info) in enumerate(sols)]
    return rows


def sigma_at_headroom(tg, j, pp=HEADROOM_TEST_PP):
    """The sigma_V at which root j's rate headroom equals pp (the targets otherwise held): bracketed on the sweep's grid,
    then brentq. Headroom rises with sigma (checked), so every sigma above it survives a sustained +pp."""
    def h(s):
        return m.rate_headroom(m.calibrate_c(replace(tg, sigma_V=s))[j][0])
    grid = [s for s in SIGMA_SWEEP if s < 1.0 - tg.theta_V]
    hs = [h(s) for s in grid]
    for s0, s1, h0, h1 in zip(grid, grid[1:], hs, hs[1:]):
        if h0 < pp <= h1:
            return brentq(lambda s: h(s) - pp, s0, s1, xtol=1e-10), dict(zip(map(str, grid), hs))
    return None, dict(zip(map(str, grid), hs))


def sigma_bounds(V):
    """For each basis reading and root: the sigma at which the rate headroom is 5 pp, the multiplier there, and (central)
    the medium path there."""
    out = {}
    for name in BASIS_READINGS:
        tg = V[name]["tg"]
        for j, r in enumerate(("lo", "hi")):
            s5, grid = sigma_at_headroom(tg, j)
            rec = dict(sigma_5pp=s5, multiplier_at_bound=1 + tg.theta_V / s5 if s5 else None, sigma_V=tg.sigma_V,
                       multiplier=1 + tg.theta_V / tg.sigma_V, multiplier_floor_any_sigma=1 / (1 - tg.theta_V),
                       headroom_on_grid=grid)
            if s5 and name == "c_central":
                e = m.calibrate_c(replace(tg, sigma_V=s5))[j][0]
                rec["at_bound"] = sweep_row(replace(tg, sigma_V=s5), s5, j, e)
            out[f"{name}_{r}"] = rec
    return out


def g0_bound(tg):
    """The largest g0 at which calibrate_c finds a root (bisection, 60 steps on [1e-4, 0.05])."""
    def has(g0):
        try:
            m.calibrate_c(replace(tg, g0=g0))
            return True
        except ValueError:
            return False
    lo, hi = 1e-4, 0.05
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if has(mid) else (lo, mid)
    return lo


def build():
    I = inputs()
    V = variants(I)
    EC = economies(I, V)
    cal = {}
    for tag, d in EC.items():
        v = V.get(d["variant"]) if d["variant"] else None
        cal[tag] = describe(d["e"], theta_data=v["tg"].theta_V if v else None, imports=v["imports"] if v else 0.0,
                            cfc_data=v["cfc"] if v else None)
        cal[tag]["root"] = d["root"]
        if d["tg"] is not None:
            cal[tag]["variant"] = d["variant"]
            cal[tag]["targets"] = {k: v_ for k, v_ in asdict(d["tg"]).items()}
            cal[tag]["closed_form"] = {k: float(v_) for k, v_ in d["info"].items()}
            cal[tag]["max_abs_residual"] = max(abs(v_) for v_ in m.target_residuals(d["e"], d["tg"]).values())
        elif d["info"] is not None:
            cal[tag]["closed_form"] = dict(d["info"])
    scen, runs = {}, {}
    for tag, d in EC.items():
        speeds = SPEEDS if tag in ("a", "b", "c_central_lo", "c_central_hi") else ("medium",)
        scen[tag] = {}
        for sp in speeds:
            mp = m.macro_path(d["e"], tech(tag, d["e"], sp), bridges_for(tag))
            runs[(tag, sp)] = mp
            scen[tag][sp] = summarise(d["e"], mp)
    dec = {}
    for tag in ("b", "c_central_lo", "c_central_hi"):
        e = EC[tag]["e"]
        lam_end = e.lam / m.LAM_END_DIVISOR                  # 0.01 exactly for (b)
        cap = m.macro_path(e, tech(tag, e, "medium", lam_end=e.lam), bridges_for(tag))
        lam = m.macro_path(e, tech(tag, e, "medium", eta_end=1.0, lam_end=lam_end), bridges_for(tag))
        dec[tag] = {"capability_only": summarise(e, cap), "lambda_only": summarise(e, lam)}
        runs[(tag, "lambda_only")] = lam
    rate = {tag: rate_tests(tag, EC[tag]["e"]) for tag in RATE_TAGS}
    for tag in EC:
        if tag not in rate:
            rate[tag] = {"headroom_pp": cal[tag]["headroom_pp"], "static": {"+100bp": static_shock(EC[tag]["e"], 100)}}
    for tag in ("c_central_lo", "c_central_hi", "c_dnonres_lo", "c_deqipp_lo"):
        rate[tag]["headroom_pp_cap60"] = m.rate_headroom(EC[tag]["e"], hi_pp=60.0)      # uncapped by 20 pp (the delta variants)
    sweep = sigma_sweep(V)
    bounds = sigma_bounds(V)
    g0b = {"c_tot": g0_bound(V["c_tot"]["tg"]), "c_central": g0_bound(V["c_central"]["tg"]),
           "tot_digitised_labour": g0_bound(replace(V["c_tot"]["tg"], labour=I["wp"]["labour_tot_digitised"])),
           "tot_imports_at_theta_V": g0_bound(replace(V["c_tot"]["tg"], labour=LABOUR + I["wp"]["foreign_content"] * I["chains"]["theta_tot"]))}
    return I, V, EC, cal, scen, dec, rate, sweep, bounds, g0b, runs


def comparator(tag, other=False):
    """(b) at the same root, like for like: at (c)'s g0 (0.01: b_g001; 0.02: b as stored; 0.005: the nearest, b_g001) and, for
    the measured-site variant (ii), at its site ((b) calibrated at the measured site: b_site_g001 at g0 0.01) — or, with
    other, the same (b) at the other g0 (b_site for (ii))."""
    r = tag.rsplit("_", 1)[1]
    if tag.startswith("c_site"):
        stored, g001 = f"b_site_{r}", f"b_site_g001_{r}"
    else:
        stored, g001 = ("b" if r == "lo" else "b_hi"), f"b_g001_{r}"
    like = stored if tag.startswith("c_traced_g02") else g001
    return (g001 if like == stored else stored) if other else like


def exceptions(runs, scen):
    """Every (c) medium run whose real wage rises above its start, or whose participation is at or above (b)'s at the same root on
    some date after the start (like for like in g0, and against the other (b)), or whose labour's share (Figure 7 basis) halves
    no earlier than that (b)'s."""
    out = {"real_wage_rises": {}, "participation_not_below_like_for_like": {}, "participation_not_below_other_b": {},
           "halves_no_earlier_like_for_like": {}, "halves_no_earlier_other_b": {},
           "site_mismatched_readout": {}}
    for tag in scen:
        if not tag.startswith("c_"):
            continue
        s = scen[tag]["medium"]
        if s["real_wage_peak_year"] > 0:
            out["real_wage_rises"][tag] = dict(peak_year=s["real_wage_peak_year"], peak_over_start=s["real_wage_peak_over_start"])
        p = runs[(tag, "medium")]["participation"]
        for key, other in (("like_for_like", False), ("other_b", True)):
            b = comparator(tag, other)
            q = runs[(b, "medium")]["participation"]
            t = runs[(tag, "medium")]["t"]
            bad = np.nonzero(p[1:] >= q[1:])[0]
            if len(bad):
                out[f"participation_not_below_{key}"][tag] = dict(against=b, first_year=float(t[1:][bad[0]]),
                                                                 y15=[float(p[-1]), float(q[-1])])
            h, hb = s["labour_share_fig7_halves_year"], scen[b]["medium"]["labour_share_fig7_halves_year"]
            if h is None or (hb is not None and h >= hb):
                out[f"halves_no_earlier_{key}"][tag] = dict(against=b, years=[h, hb])
    for tag in ("c_site_lo", "c_site_hi"):          # (ii) against (b) at the calibrated site (13% of the basket): not like for like
        r = tag[-2:]
        p, t = runs[(tag, "medium")]["participation"], runs[(tag, "medium")]["t"]
        for b in (("b" if r == "lo" else "b_hi"), f"b_g001_{r}"):
            q = runs[(b, "medium")]["participation"]
            bad = np.nonzero(p[1:] >= q[1:])[0]
            out["site_mismatched_readout"][f"{tag}|{b}"] = dict(
                participation_not_below_from=float(t[1:][bad[0]]) if len(bad) else None, y15=[float(p[-1]), float(q[-1])],
                halves=[scen[tag]["medium"]["labour_share_fig7_halves_year"], scen[b]["medium"]["labour_share_fig7_halves_year"]])
    return out


def site_note(ex, scen):
    """The measured-site variant (ii) in words, from the exceptions and the runs (every number from them)."""
    groups = ("like_for_like", "other_b")
    part = sorted({t for g in groups for t in ex[f"participation_not_below_{g}"] if t.startswith("c_site")})
    s = ("like for like in the site — against (b) calibrated at the measured site (4.2% of GDP), at g0 0.01 and 0.02, root for "
         "root — the measured-site variant (ii)'s participation is " + ("below (b)'s at every date after the start" if not part
                                                                         else f"not below (b)'s at some date in {part}"))
    for t, v in ex["real_wage_rises"].items():
        r = t[-2:]
        bs = [scen[f"b_site_g001_{r}"]["medium"], scen[f"b_site_{r}"]["medium"]]
        s += (f"; what remains: {t}'s real wage rises before falling (x{v['peak_over_start']:.3f} at year {v['peak_year']:.2f}), "
              f"less than (b) at the measured site does at the same root (x{bs[0]['real_wage_peak_over_start']:.3f} at g0 0.01, "
              f"x{bs[1]['real_wage_peak_over_start']:.3f} at g0 0.02)")
    for t in ("c_site_lo", "c_site_hi"):
        pairs = [f"{ex[f'halves_no_earlier_{g}'][t]['years'][0]} vs {ex[f'halves_no_earlier_{g}'][t]['years'][1]} "
                 f"({ex[f'halves_no_earlier_{g}'][t]['against']})" for g in groups if t in ex[f"halves_no_earlier_{g}"]]
        if pairs:
            s += f"; {t}'s labour share (Figure 7 basis) halves no earlier than (b)'s at the measured site: {', '.join(pairs)}"
    ahead = {k: v for k, v in ex["site_mismatched_readout"].items() if v["participation_not_below_from"] is not None}
    if ahead:
        s += (". Against (b) at its calibrated site (13% of the basket; not like for like in the site, kept as a readout): "
              + "; ".join(f"{k.split('|')[0]} not below {k.split('|')[1]} from year {v['participation_not_below_from']:g} "
                          f"({v['y15'][0]:.3f} vs {v['y15'][1]:.3f} at year 15)" for k, v in ahead.items()))
    return s


def headline(I, V, cal, scen, dec, rate, sweep, bounds, g0b, runs):
    """The headline, in the order it is to be read: (1) the direction and the sigma sweep; (2) the rate-plausibility link;
    (3) the medium-path table, root for root; (4) how much of the gap is the g0 change; (5) the bridge readouts."""
    t = I["chains"]
    b_mult = cal["b"]["multiplier"]
    ok = [r for r in sweep if "error" not in r]
    by = {r: [x for x in ok if x["root"] == r] for r in ("lo", "hi")}
    b_ref = {"lo": scen["b"]["medium"], "hi": scen["b_hi"]["medium"]}
    rises = sorted(x["sigma_V"] for x in ok if x["real_wage_peak_year"] > 0)
    c = V["c_central"]["tg"]
    ex_ = exceptions(runs, scen)
    direction = dict(
        statement="For any fixed-rent share sigma the closure multiplier 1 + theta_V/sigma_V is at least 1/(1 - theta_V) "
                  "(sigma_V <= 1 - theta_V), against (b)'s ~1.00: cheaper labour makes machines cheaper, so the wage must fall "
                  "further to hold the task margin. Across the whole admissible sigma range, root for root, participation is "
                  "below (b)'s at years 6 and 15. sigma sets the size, not the sign.",
        multiplier_floor_any_sigma={"domp (central)": 1 / (1 - c.theta_V), "tot": 1 / (1 - t["theta_tot"])},
        multiplier_b=b_mult, multiplier_b_hi=cal["b_hi"]["multiplier"],
        sweep_sigma_range=[min(x["sigma_V"] for x in ok), max(x["sigma_V"] for x in ok)],
        sweep_multiplier_range=[min(x["multiplier"] for x in ok), max(x["multiplier"] for x in ok)],
        sweep_participation_y15={r: [min(x["participation_y15"] for x in by[r]), max(x["participation_y15"] for x in by[r])] for r in by},
        sweep_participation_y6={r: [min(x["participation_y6"] for x in by[r]), max(x["participation_y6"] for x in by[r])] for r in by},
        b_participation={r: dict(y6=b_ref[r]["participation"]["6.0"], y15=b_ref[r]["participation"]["15.0"]) for r in b_ref},
        sweep_below_b_root_for_root=all(x["participation_y15"] < b_ref[x["root"]]["participation"]["15.0"]
                                        and x["participation_y6"] < b_ref[x["root"]]["participation"]["6.0"] for x in ok),
        sweep_real_wage_rises_from_sigma=rises[0] if rises else None,
        exceptions=ex_,
        exceptions_note=site_note(ex_, scen),
        open_bracket=[V["c_sig_imports"]["tg"].sigma_V, V["c_sig_nosimports"]["tg"].sigma_V], central_sigma=c.sigma_V)
    cb = bounds["c_central_lo"], bounds["c_central_hi"]
    rate_link = dict(
        statement="Headroom and the multiplier are the same 1/sigma object: at a fixed task margin d ln(w/r)/d ln(rho + delta) "
                  "= 1/sigma_V and d ln(w/r)/d ln gamma = 1 + theta_V/sigma_V. An economy that survives a sustained +5 pp rise "
                  "in the required return (headroom >= 5 pp at the all-assets delta) has sigma_V at or above the bound below, "
                  "which puts it at the mild end of the sweep.",
        headroom_test_pp=HEADROOM_TEST_PP, delta=c.delta,
        sigma_5pp={k: v["sigma_5pp"] for k, v in bounds.items()},
        multiplier_at_bound={k: v["multiplier_at_bound"] for k, v in bounds.items()},
        central_at_bound={r: {k: b["at_bound"][k] for k in ("participation_y6", "participation_y15", "real_wage_index_y15",
                                                           "multiplier", "headroom_pp")} for r, b in zip(("lo", "hi"), cb)},
        central_headroom_pp={"lo": rate["c_central_lo"]["headroom_pp"], "hi": rate["c_central_hi"]["headroom_pp"]},
        headroom_pp_uncapped={k: rate[k]["headroom_pp_cap60"] for k in ("c_central_lo", "c_central_hi", "c_dnonres_lo", "c_deqipp_lo")},
        caveat="headroom in pp scales with delta (headroom / delta is invariant): at the equipment + IPP delta the same economy has "
               f"{rate['c_deqipp_lo']['headroom_pp_cap60']:.2f} pp, so the bound depends on which delta the +5 pp is read against")
    table = {}
    for tg in TABLE:
        s = scen[tg]["medium"]
        v = V.get(tg.rsplit("_", 1)[0], {}) if tg.startswith("c_") else {}
        table[tg] = dict(label=v.get("label", B_LABELS.get(tg)),
                         participation_y6=s["participation"]["6.0"], participation_y15=s["participation"]["15.0"],
                         real_wage_index_y15=s["real_wage_index"]["15.0"], real_wage_peak_year=s["real_wage_peak_year"],
                         real_wage_peak_over_start=s["real_wage_peak_over_start"], w_over_r_end_over_start=s["w_over_r_end_over_start"],
                         labour_share_fig7_halves_year=s["labour_share_fig7_halves_year"], fig7_basis=s["fig7_basis"],
                         multiplier=cal[tg]["multiplier"], headroom_pp=rate[tg]["headroom_pp"], sigma_V=cal[tg]["sigma_V"],
                         theta_V=cal[tg]["theta_V"], k=cal[tg]["params"]["k"], g0=cal[tg]["params"]["g0"], rho=cal[tg]["params"]["rho"])
    attribution = {}
    for r, (b, b1, cc_) in (("lo", ("b", "b_g001_lo", "c_central_lo")), ("hi", ("b_hi", "b_g001_hi", "c_central_hi"))):
        rec = {}
        for y in ("6.0", "15.0"):
            pb, pb1, pc = (scen[x]["medium"]["participation"][y] for x in (b, b1, cc_))
            rec[f"y{y[:-2]}"] = dict(b=pb, b_g001=pb1, c_central=pc, gap=pb - pc, g0_part=pb - pb1, chain_part=pb1 - pc,
                                      g0_share_of_gap=(pb - pb1) / (pb - pc))
        attribution[r] = rec
    bridge = dict(
        note="(c)'s r*, policy rate and debt on the bridges refit on (c) (Log 46: the capex channel keyed to replacement investment / "
             "income, which falls along the path); (b)'s on the bridges as tuned on (b) (the pace key).",
        inv_income={tg: scen[tg]["medium"]["inv_income"] for tg in ("b", "b_hi", "c_central_lo", "c_central_hi", "c_mixed_lo", "c_tot_lo")},
        r_star_max={tg: scen[tg]["medium"]["r_star_max"] for tg in ("b", "c_central_lo", "c_central_hi")},
        r_star_max_year={tg: scen[tg]["medium"]["r_star_max_year"] for tg in ("b", "c_central_lo", "c_central_hi")},
        debt_y15={tg: scen[tg]["medium"]["debt"]["15.0"] for tg in ("b", "c_central_lo", "c_central_hi")})
    return dict(order=["direction (the sigma sweep)", "rate_link", "table_medium", "g0_attribution", "bridge_readouts"],
                direction=direction, rate_link=rate_link, table_medium=table, g0_attribution=attribution,
                g0_bounds=dict(g0b, note="the largest g0 with a root in k: the tot-consistent labour (0.47 grossed up) runs at "
                               f"g0 {G0_TOT}; with the digitised 0.4723 grossed up, or imports at theta_V, the bound is lower"),
                lambda_only_labour_share_fall_y15={tg: dec[tg]["lambda_only"]["labor_share"]["0.0"] - dec[tg]["lambda_only"]["labor_share"]["15.0"]
                                                   for tg in dec},
                plus100bp_labour_share_pp={tg: rate[tg]["static"]["+100bp"].get("d_labour_share_pp") for tg in RATE_TAGS},
                bridge_readouts=bridge,
                chain_share_labels=dict(model="chain_share: the chain's share of compensation (effective labour; one wage)",
                                        measured_2023={b: dict(compensation=t[f"share_{b}"], hours_fte=t[f"hours_fte_{b}"],
                                                               hours_worked_bridged=t[f"hours_bridged_{b}"]) for b in ("domp", "tot")}))


def import_as_land(I, V, EC, runs):
    """Readout for the open item: under the open reading the chain's imported content is part of its land b — paid as domestic
    rent (so it counts in model income) and drawn from the endowment T that housing shares. Its share of sigma_V (so of b),
    the machine chain's share of T (b delta K / T) along the medium path, and the rent paid on the imported part at the start."""
    c, imp = V["c_central"]["tg"], I["chains"]["g1_imports_domp"]
    share = imp / c.sigma_V
    out = {"imports_share_of_sigma": share, "imports": imp, "sigma_V": c.sigma_V,
           "note": "imported content is modelled as the chain's fixed-quantity land (domestic rent, drawn from T), not as an "
                   "elastic import at a world price; as investment falls along the path the chain's land is freed for housing"}
    for tag in ("c_central_lo", "c_central_hi", "b", "b_hi"):
        e, mp = EC[tag]["e"], runs[(tag, "medium")]
        at = {d: int(np.argmin(np.abs(mp["t"] - d))) for d in DATES}
        land = e.b * e.delta * mp["K"] / e.T
        out[tag] = {"chain_land_share_of_T": {str(d): float(land[i]) for d, i in at.items()}}
        if tag.startswith("c_"):
            out[tag]["import_rent_share_of_income_y0"] = float(share * e.b * e.delta * mp["K"][0] / mp["income"][0])
    return out


def pce_import_probe(I, V):
    """Readout for the open item: the consumption chain's own foreign content (WP2026-01, 0.094 of PCE in 2023) moved out of
    capital services (cs = 1 - labour - site) into a fixed-rent part of the basket — site-like, drawing on T: the site target
    0.13 + that content, the central's sigma held (isolates the one change). Its largest g0 with a root; at G0_TOT (0.005)
    both roots on the medium path against the central and (b) at the same g0 (macro.calibrate_roots). A probe, not a variant."""
    c, fc = V["c_central"]["tg"], I["wp"]["foreign_content"]
    probe = replace(c, site=c.site + fc)
    out = {"construction": "site target 0.13 + PCE foreign content (basket basis), sigma_V held at the central's, a probe",
           "site_target": probe.site, "foreign_content": fc, "sigma_V_held": c.sigma_V, "g0_bound": g0_bound(probe),
           "g0_bound_central": g0_bound(c)}
    try:
        m.calibrate_c(replace(probe, g0=G0_CENTRAL))
        out["root_at_g0_central"], out["no_root_message"] = True, None
    except ValueError as ex:
        out["root_at_g0_central"], out["no_root_message"] = False, str(ex)
    g0 = G0_TOT
    econ = {"probe": m.calibrate_c(replace(probe, g0=g0)), "central": m.calibrate_c(replace(c, g0=g0)),
            "b": m.calibrate_roots(base=replace(m.CAPITAL_BASE, g0=g0, g1=1.0 - g0))}
    out["g0"], out["roots"] = g0, {}
    for j, r in enumerate(("lo", "hi")):
        rec, part = {}, {}
        for name, sols in econ.items():
            e = sols[j][0]
            mp = m.macro_path(e, tech(name, e, "medium"), bridges_for(name))
            S = summarise(e, mp)
            part[name] = mp["participation"]
            rec[name] = dict(k=e.k, rho=e.rho, participation_y6=S["participation"]["6.0"], participation_y15=S["participation"]["15.0"],
                             real_wage_index_y15=S["real_wage_index"]["15.0"], real_wage_peak_year=S["real_wage_peak_year"],
                             labour_share_fig7_halves_year=S["labour_share_fig7_halves_year"])
        rec["probe_below_central_every_date"] = bool(np.all(part["probe"][1:] < part["central"][1:]))
        rec["probe_below_b_every_date"] = bool(np.all(part["probe"][1:] < part["b"][1:]))
        out["roots"][r] = rec
    return out


def open_items(I, R):
    """The open items, with the numbers the readouts measured (R: the readouts block)."""
    L, P = R["import_as_land"], R["pce_import_probe"]
    cl = L["c_central_lo"]
    pr = P["roots"]
    return [
        "WP2026-01's labour definition is unverified: its 'human effort' is split into college and non-college labour, which suggests "
        "the BEA-BLS integrated accounts, and those impute self-employed labour. theta_V (I-O compensation of employees) leaves "
        "proprietors' labour in NOS, which matters in construction, part of the bundle. If the labour target includes imputed "
        "self-employed labour, theta_V is understated against it, which would push toward a more severe result. The WP2026-01 PDF is "
        "not in the repository (pinning/effort README 'Known gaps').",
        f"Under the open reading the investment chain's imported content ({L['imports']:.4f} of build cost, {L['imports_share_of_sigma']:.0%} "
        f"of sigma_V {L['sigma_V']:.4f}) is modelled as the chain's fixed-quantity land b — paid as domestic rent, so it counts in "
        f"model income ({cl['import_rent_share_of_income_y0']:.1%} of it at the start; hence M8's GDP net of imports), and drawn "
        "from the endowment T that housing shares — not as an elastic import at a world price. As investment falls the chain's "
        f"land is freed for housing: its share of T {cl['chain_land_share_of_T']['0.0']:.3f} -> {cl['chain_land_share_of_T']['6.0']:.3f} "
        f"-> {cl['chain_land_share_of_T']['10.0']:.3f} -> {cl['chain_land_share_of_T']['15.0']:.3f} (years 0/6/10/15, central low "
        f"root; (b) {L['b']['chain_land_share_of_T']['0.0']:.3f} -> {L['b']['chain_land_share_of_T']['15.0']:.3f}). The sigma sweep "
        "brackets sigma's size, not this land-market channel; its direction on the paths is not quantified "
        "(readouts.import_as_land).",
        f"Under the open reading the consumption chain's own foreign content ({P['foreign_content']:.3f} of PCE) is left in the model's "
        "capital services (cs = 1 - labour - site), so the model makes it with machines; only the investment chain's imported "
        "content is a fixed-quantity cost. The model has no fixed-price import in the consumption basket. A probe that moves it "
        f"into a site-like fixed rent (site target {P['site_target']:.3f}, sigma held) points toward a more severe result: it has "
        f"{'a' if P['root_at_g0_central'] else 'no'} root at g0 {G0_CENTRAL} (its largest g0 is {P['g0_bound']:.5f}), and at g0 "
        f"{P['g0']} participation at year 15 is {pr['lo']['probe']['participation_y15']:.3f} / {pr['hi']['probe']['participation_y15']:.3f} "
        f"(low / high root) against the central's {pr['lo']['central']['participation_y15']:.3f} / "
        f"{pr['hi']['central']['participation_y15']:.3f} at the same g0 — so the open reading's choice here is the mild one "
        "(readouts.pce_import_probe).",
        "delta_chain (the normal return in sigma's construction) is BEA's private equipment + IPP rate, not the depreciation rate of "
        "the chain's own capital (FA 3.1ESI / 3.4ESI by industry would give it).",
        f"The tot-consistent labour prices PCE's foreign content at the domestic PCE chain's labour share (0.47/(1 - "
        f"{I['wp']['foreign_content']:.3f})); pricing it at theta_V instead gives {LABOUR + I['wp']['foreign_content'] * I['chains']['theta_tot']:.4f} "
        "and a lower g0 bound. The WP2026-01 numbers are a digitisation of its Figure 9.",
    ]


def results():
    """The results document (JSON-ready) and what the figure needs; deterministic, so the checks rebuild it and compare."""
    I, V, EC, cal, scen, dec, rate, sweep, bounds, g0b, runs = build()
    c = V["c_central"]["tg"]
    readouts = {"import_as_land": import_as_land(I, V, EC, runs), "pce_import_probe": pce_import_probe(I, V)}
    out = {"sources": {"fixed_assets": "BEA Fixed Assets Section1All_xls.xlsx (Tables 1.1, 1.3, 1.5), " + URLS["Section1All_xls.xlsx"],
                       "nipa": "BEA NIPA annual flat file NipaDataA.txt, codes checked against SeriesRegister.txt, "
                               + URLS["NipaDataA.txt"],
                       "nipa_codes": {r: c_ for r, (c_, _) in NIPA.items()}, "chains": "results/chains.json (code/chains.py)",
                       "wp2026": I["wp"]["source"], "year": YEAR},
           "targets": {"from_chains_json": I["sources"], "wp2026_2023": I["wp"],
                       "central": {"reading": "open (domp): US labour throughout, imported content outside the labour share as a "
                                              "fixed-quantity cost (in the model, part of the chain's land)",
                                   "labour": LABOUR, "theta_V": c.theta_V, "chain_share": c.chain_share, "sigma_V": c.sigma_V,
                                   "sigma_construction": V["c_central"]["sigma"],
                                   "sigma_pieces": dict(imports=I["chains"]["g1_imports_domp"], nos=I["chains"]["g1_nos_domp"],
                                                        cfc=I["chains"]["g1_cfc_domp"], delta_chain=I["chains"]["delta_chain"]),
                                   "sigma_bracket_open": [I["chains"]["g1_imports_domp"], I["chains"]["g1_nos_domp"] + I["chains"]["g1_imports_domp"]],
                                   "g0": c.g0},
                       "machinery_software_set_theta_domp_vs_bundle": [I["chains"]["set_theta_domp"], I["chains"]["theta_domp"]],
                       "delta_fa": I["delta"], "nipa_2023": I["nat"],
                       "scope_check": {b: {"theta_x_cfc_over_comp": I["chains"][f"theta_{b}"] * I["chains"]["cfc_gdp"] / I["chains"]["comp_gdp"],
                                           "chain_share": I["chains"][f"share_{b}"]} for b in ("tot", "domp")},
                       "her_four": {"labour_bea": LABOUR, "participation": 0.60, "baskets_per_person": 3.0, "site_basket": 0.13}},
           "variants": {n: {k: v[k] for k in ("label", "bases", "mixed", "superseded", "sigma", "imports", "cfc")} | {"sigma_V": v["tg"].sigma_V}
                        for n, v in V.items()},
           "headline": headline(I, V, cal, scen, dec, rate, sweep, bounds, g0b, runs),
           "calibrations": cal, "scenarios": scen, "decomposition": dec, "rate": rate, "sigma_sweep": sweep, "sigma_bounds": bounds,
           "readouts": readouts, "open_items": open_items(I, readouts)}
    return jsonable(out), I, V, EC, runs


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out, I, V, EC, runs = results()
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "calibration_c.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    report(out)
    figure(EC, V, runs, out, I)


def report(out):
    H, cal = out["headline"], out["calibrations"]
    d = H["direction"]
    print("1. DIRECTION AND THE SIGMA SWEEP")
    print(f"   multiplier >= 1/(1 - theta): {', '.join(f'{k} {v:.3f}' for k, v in d['multiplier_floor_any_sigma'].items())}; "
          f"(b) {d['multiplier_b']:.4f} / {d['multiplier_b_hi']:.4f}")
    print(f"   sweep sigma {d['sweep_sigma_range'][0]:.3f}-{d['sweep_sigma_range'][1]:.3f}: multiplier {d['sweep_multiplier_range'][1]:.2f}-"
          f"{d['sweep_multiplier_range'][0]:.2f}; participation y15 lo {d['sweep_participation_y15']['lo'][0]:.3f}-"
          f"{d['sweep_participation_y15']['lo'][1]:.3f}, hi {d['sweep_participation_y15']['hi'][0]:.3f}-{d['sweep_participation_y15']['hi'][1]:.3f} "
          f"vs (b) {d['b_participation']['lo']['y15']:.3f} / {d['b_participation']['hi']['y15']:.3f}; below (b) root for root: "
          f"{d['sweep_below_b_root_for_root']}; real wage rises from sigma {d['sweep_real_wage_rises_from_sigma']}")
    r = H["rate_link"]
    print("2. THE RATE LINK (headroom and multiplier: the same 1/sigma)")
    for k, v in r["sigma_5pp"].items():
        print(f"   {k:15s} sigma at 5 pp headroom {v:.4f}, multiplier there {r['multiplier_at_bound'][k]:.3f}")
    for k, v in r["central_at_bound"].items():
        print(f"   central {k} at the bound: participation y6 {v['participation_y6']:.3f} y15 {v['participation_y15']:.3f}, real wage y15 "
              f"{v['real_wage_index_y15']:.3f}; central headroom {r['central_headroom_pp'][k]:.2f} pp")
    print("3. MEDIUM PATH")
    for tg, v in H["table_medium"].items():
        print(f"   {tg:16s} part y6 {v['participation_y6']:.3f} y15 {v['participation_y15']:.3f} | real wage y15 {v['real_wage_index_y15']:.3f} "
              f"peak @ {v['real_wage_peak_year']:.2f} | w/r {v['w_over_r_end_over_start']:.4f} | labour halves @ {v['labour_share_fig7_halves_year']} "
              f"| mult {v['multiplier']:.3f} headroom {v['headroom_pp']:.2f} | sigma {v['sigma_V']:.4f} k {v['k']:.3f} g0 {v['g0']}")
    print("4. g0 ATTRIBUTION (participation)")
    for rr, rec in H["g0_attribution"].items():
        for y, a in rec.items():
            print(f"   {rr} {y}: gap {a['gap']:.3f} = g0 {a['g0_part']:+.3f} + chain {a['chain_part']:+.3f} (g0 share {a['g0_share_of_gap']:+.2f})")
    print("   g0 bounds:", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in H["g0_bounds"].items()})
    print("   exceptions:", {k: v for k, v in d["exceptions"].items() if v})
    print("5. BRIDGE READOUTS (omit the investment fall):", {k: {y: round(x, 3) for y, x in v.items()} for k, v in H["bridge_readouts"]["inv_income"].items()})
    print("   the measured site:", d["exceptions_note"])
    L, P = out["readouts"]["import_as_land"], out["readouts"]["pce_import_probe"]
    print(f"6. PROBES OF THE OPEN READING: imports {L['imports_share_of_sigma']:.3f} of sigma; chain land / T (central lo) "
          f"{', '.join(f'{v:.3f}' for v in L['c_central_lo']['chain_land_share_of_T'].values())}; PCE-import probe: root at g0 "
          f"{G0_CENTRAL} {P['root_at_g0_central']}, g0 bound {P['g0_bound']:.5f}; at g0 {P['g0']} y15 "
          + ", ".join(f"{r} probe {v['probe']['participation_y15']:.3f} / central {v['central']['participation_y15']:.3f} / (b) "
                      f"{v['b']['participation_y15']:.3f}" for r, v in P["roots"].items()))
    for tag, dd in cal.items():
        print(f"{tag:22s} k {dd['params']['k']:7.3f} rho {dd['params']['rho']:.4f} x* {dd['x']:.4f} ceil {dd['x_ceiling']:.4f} theta {dd['theta_V']:.3f} "
              f"sigma {dd['sigma_V']:.3f} mult {dd['multiplier']:6.2f} chain {dd['chain_share']:.3f} K/GDP {dd['K_gdp_net']:.2f} "
              f"CFC/GDP {dd['cfc_gdp_net']:.3f} comp/GDP {dd['comp_gdp_net']:.3f} headroom {dd['headroom_pp']:.2f}")


def figure(EC, V, runs, out, I):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    CB, CB2, CC, CT, CM, CS, CA = "#52514e", "#a3a29d", "#2a78d6", "#1baf7a", "#eb6834", "#9b59b6", "#b7b6b1"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                         "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 10.5, "axes.titleweight": "bold",
                         "axes.titlecolor": INK, "axes.titlelocation": "left"})
    fig, ax = plt.subplots(3, 3, figsize=(15.5, 13.2), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    H, sweep, rate = out["headline"], out["sigma_sweep"], out["rate"]
    c = V["c_central"]["tg"]
    brk = H["direction"]["open_bracket"]
    s5 = H["rate_link"]["sigma_5pp"]
    lo = [r for r in sweep if r.get("root") == "lo"]
    hi = [r for r in sweep if r.get("root") == "hi"]
    pb = {r: H["direction"]["b_participation"][r]["y15"] for r in ("lo", "hi")}
    # 1. the sweep: participation at year 15
    a = ax[0, 0]
    a.axvspan(brk[0], brk[1], color=CC, alpha=0.07, lw=0)
    for rows, ls, lab in ((lo, "-", "low root"), (hi, "--", "high root")):
        s = [r["sigma_V"] for r in rows]
        a.plot(s, [r["participation_y15"] for r in rows], color=CC, ls=ls, lw=1.9, marker="o", ms=3, label=f"(c), {lab}")
    for r, ls in (("lo", "-"), ("hi", "--")):
        a.axhline(pb[r], color=CB, lw=1.1, ls=ls)
        a.text(0.51, pb[r] + 0.006, f"(b) {r} root {pb[r]:.2f}", ha="right", fontsize=7.5, color=INK2)
    a.axvline(c.sigma_V, color=CC, lw=0.9, ls=":")
    a.text(c.sigma_V + 0.004, 0.13, "central", fontsize=7.5, color=CC)
    for r, ls in (("lo", "-"), ("hi", "--")):
        a.axvline(s5[f"c_central_{r}"], color=CM, lw=1.0, ls=ls)
    a.text(s5["c_central_hi"] - 0.004, 0.03, "headroom 5 pp", ha="right", fontsize=7.5, color=CM)
    a.text(0.5 * (s5["c_central_lo"] + brk[1]) + 0.01, 0.445, "measured\nbracket", ha="center", va="center", fontsize=7.5, color=CC)
    a.set_ylim(0, 0.52); a.set_xlim(0, 0.52)
    a.set_title("1. σ sets the size, not the sign\nparticipation at year 15, medium path, central targets")
    a.set_xlabel("σ_V, the chain's fixed-rent share of build cost"); a.set_ylabel("share of potential workers")
    a.legend(frameon=False, fontsize=7.5, labelcolor=INK, loc="lower right")
    # 2. the same 1/sigma object: multiplier and headroom
    a = ax[0, 1]
    for rows, ls in ((lo, "-"), (hi, "--")):
        s = [r["sigma_V"] for r in rows]
        a.plot(s, [r["multiplier"] for r in rows], color=CC, ls="-", lw=1.9)
    fl = 1 / (1 - c.theta_V)
    a.axhline(fl, color=CC, lw=0.9, ls=":")
    a.text(0.51, 0.5 * (1.0 + fl), f"floor for any σ: 1/(1 − θ) = {fl:.2f}", ha="right", va="center", fontsize=7.5, color=CC)
    a.axhline(H["direction"]["multiplier_b"], color=CB, lw=1.1)
    a.text(0.51, 0.45, f"(b) {H['direction']['multiplier_b']:.2f}", ha="right", va="center", fontsize=7.5, color=INK2)
    a.set_ylim(0, 17); a.set_xlim(0, 0.52)
    a.set_ylabel("closure multiplier 1 + θ/σ", color=CC); a.set_xlabel("σ_V")
    a2 = a.twinx()
    for rows, ls, lab in ((lo, "-", "headroom, low root"), (hi, "--", "headroom, high root")):
        a2.plot([r["sigma_V"] for r in rows], [r["headroom_pp"] for r in rows], color=CM, ls=ls, lw=1.7, label=lab)
    a2.axhline(5.0, color=CM, lw=0.8, ls=":"); a2.text(0.02, 5.3, "+5 pp", fontsize=7.5, color=CM)
    a2.set_ylim(0, 21); a2.set_ylabel("rate headroom, pp (capped at 20)", color=CM)
    for s_ in ("top",):
        a2.spines[s_].set_visible(False)
    a2.spines["right"].set_edgecolor(GRID); a2.tick_params(colors=INK2)
    a2.legend(frameon=False, fontsize=7.5, labelcolor=INK, loc="center right")
    a.set_title("2. The multiplier and the rate headroom: one 1/σ object\nsurviving +5 pp needs σ above the orange crossing")
    lines = (("b", CB, "-", 2.0, "(b) as stored, low root"), ("b_hi", CB, "--", 1.6, "(b), high root"),
             ("b_g001_lo", CB2, "-", 1.4, "(b) at g0 0.01, low root"),
             ("c_central_lo", CC, "-", 2.3, "(c) central (open), low root"), ("c_central_hi", CC, "--", 2.0, "(c) central, high root"),
             ("c_tot_lo", CT, "-", 1.5, "(c) tot-consistent, low root"), ("c_mixed_lo", CM, "-", 1.5, "(c) mixed basis (severe), low root"),
             ("c_site_lo", CS, ":", 1.6, "(c) site at the measured flow, low root"),
             ("b_site_g001_lo", CS, "-", 0.9, "(b) at the measured site, g0 0.01, low root (its comparator)"))
    t = I["chains"]
    panels = ((ax[0, 2], "participation", 1, "3. Participation, medium path", "share of potential workers"),
              (ax[1, 0], "real_wage", "index", "4. What an hour's wage buys\nindex, start = 1", "index"),
              (ax[1, 1], "fig7", 100, "5. Labour's share, the paper's Figure 7 basis\nconsumption chain's labour, capital services in surplus", "% of income"),
              (ax[1, 2], "chain_share", 100, "6. The machine chain's share of compensation\n(effective labour: the model has one wage)", "%"))
    for a, key, scale, title, unit in panels:
        for tag, col, ls, lw, lab in lines:
            mp = runs[(tag, "medium")]
            y = mp[key] / mp[key][0] if scale == "index" else (mp["labour_share_bea"] if key == "fig7" else mp[key]) * scale
            a.plot(mp["t"], y, color=col, ls=ls, lw=lw, label=lab)
        a.set_title(title); a.set_ylabel(unit); a.set_xlabel("years")
    ax[0, 2].legend(frameon=False, fontsize=7.3, labelcolor=INK, loc="lower left")
    ax[1, 2].text(0.98, 0.97, f"measured 2023, the bundle\ndomp: compensation {t['share_domp'] * 100:.1f}%,\nhours {t['hours_fte_domp'] * 100:.1f}% (FTE) / "
                  f"{t['hours_bridged_domp'] * 100:.1f}% (worked)\ntot: compensation {t['share_tot'] * 100:.1f}%,\nhours {t['hours_fte_tot'] * 100:.1f}% / "
                  f"{t['hours_bridged_tot'] * 100:.1f}%", transform=ax[1, 2].transAxes, ha="right", va="top", fontsize=7.3, color=INK2)
    a = ax[2, 0]
    for tag, col, lab in (("a", CA, "(a) (labor_share: flow benchmark)"), ("b", CB, "(b)"), ("c_central_lo", CC, "(c) central, low root")):
        for sp, ls in (("slow", ":"), ("medium", "-"), ("fast", "--")):
            mp = runs[(tag, sp)]
            y = mp["labor_share"] if tag == "a" else mp["labour_share_bea"]
            a.plot(mp["t"], y * 100, color=col, ls=ls, lw=1.6, label=lab if sp == "medium" else None)
    a.set_title("7. Labour's share (Figure 7 basis) at three speeds\ndotted slow, solid medium, dashed fast"); a.set_ylabel("% of income")
    a.set_ylim(0, 63)
    a.set_xlabel("years"); a.legend(frameon=False, fontsize=7.5, labelcolor=INK, loc="upper right")
    a = ax[2, 1]
    tags = ("b", "c_central_lo", "c_central_hi", "c_tot_lo", "c_mixed_lo", "c_sig_imports_lo", "c_sig_nosimports_lo")
    vals = [rate[x]["static"]["+100bp"].get("d_labour_share_pp") or 0.0 for x in tags]
    hr = [rate[x]["headroom_pp"] for x in tags]
    a.bar(range(len(tags)), vals, color=[CB, CC, CC, CT, CM, CB2, CB2])
    for i, (v, h) in enumerate(zip(vals, hr)):
        a.text(i, v + 0.08, f"{v:+.2f}\n{'≥' if h >= 20 else ''}{h:.1f} pp", ha="center", fontsize=7.3, color=INK)
    a.set_xticks(range(len(tags)))
    a.set_xticklabels(["(b)", "central\nlo", "central\nhi", "tot\nlo", "mixed\nlo", "σ =\nimports", "σ = NOS\n+ imports"], fontsize=7.5)
    a.set_ylim(0, max(vals) * 1.45)
    a.set_title("8. +100 bp on the required return: labour's share\n(bar, pp) and the rate headroom (label)"); a.set_ylabel("pp")
    a = ax[2, 2]
    for tag, col, ls, lw, lab in lines:
        mp, e = runs[(tag, "medium")], EC[tag]["e"]
        a.plot(mp["t"], e.delta * mp["Vm"] * mp["K"] / mp["income"] * 100, color=col, ls=ls, lw=lw)
    a.set_title("9. Replacement investment / income\nthe series (c)'s r* is keyed to (medium)"); a.set_ylabel("% of income")
    a.set_xlabel("years")
    fig.text(0.01, 0.004, "Medium automation (capability 1 → 0.04, labour per machine-service hour to a fifth) unless stated. (c) central: the chain that builds "
             f"equipment, IPP and private structures on the domp basis (US labour only), θ_V {c.theta_V:.3f}, {c.chain_share * 100:.1f}% of compensation; "
             f"σ {c.sigma_V:.3f} = imported content {t['g1_imports_domp']:.3f}\n+ NOS {t['g1_nos_domp']:.3f} − CFC {t['g1_cfc_domp']:.3f} × ρ/δ_chain (a construction); "
             f"labour 0.47 (BEA WP2026-01, foreign content outside); δ {c.delta:.4f} (BEA Fixed Assets); g0 {c.g0}. Bridges at their illustrative "
             "defaults; r* and debt are bridge readouts (in results/calibration_c.json).", fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_calibration_c.png"); fig.savefig(p, dpi=150, facecolor=SURF); print(p)


if __name__ == "__main__":
    main()
