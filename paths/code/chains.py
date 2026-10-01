# chains.py — the machine chain's labour share by machine type, its cost split, the service-flow conversion, and the
# hours of machine-chain labour per hour a machine replaces, by income. Unit 1 of the fix to the macro block's machine
# chain (her question, 2026-09-30: is the paths model's theta off?). The macro block's calibrations put the labour share
# of a machine's build cost (theta_V = lambda v / Vm) at 0.018 in (a) (flow benchmark: asset = service; 0.026 traced) and
# 0.0023 in (b) (0.0013 as a share of service cost); the lambda thread measures the full-chain compensation share of
# machinery final output at ~0.55. Asset, service and traced bases are different objects, and this unit measures the
# pieces that map one to the other; item 7 sets model against data basis by basis (like for like, the data sit 34x (a)
# and 272x (b) above the model on the asset basis; results model_vs_data, check C21).
#
# STRUCTURE.
#   1. Gate. The lambda thread's engine (progress_and_prosperity/lambda/code/compute_family_a.py: published IxC total
#      requirements, MU after-redefinitions summary, V001/V002/V003 rows, tot/dom/domp import variants, final uses except
#      inventories and imports) is imported and re-run; its narrow/medium/broad series in lambda_us_family_a.csv must be
#      reproduced to <= 1e-6 every year before anything new is computed (the run stops otherwise).
#   2. Theta by machine type, annual 1997-2023: theta_c = v_w' TR e_c for each summary commodity (333, 334, 335, 511, 514,
#      5415, 532RL), tot / dom / domp exactly as the thread. For one commodity the final-use weighting cancels, so the two
#      weightings differ only for aggregates: (i) the thread's (all final uses except F030, F050), (ii) fixed investment in
#      equipment and IPP — F02E, F02N (private nonresidential) and F06E, F06N, F07E, F07N, F10E, F10N (government) — the
#      machines at US task margins. The investment-weighted "machinery + software set" (keyed machinery_software_set;
#      formerly "all machinery", a name that invited misreading) is over the broad set (532RL carries no investment, so it
#      is the medium set in effect): six commodities, 37% of equipment + IPP investment in 2023, leaving out vehicles,
#      aircraft, R&D (5412OP), furniture and the trade margins on equipment (producers' prices) and including government
#      (defense) equipment. Its 2023 theta_tot 0.617 tops a 0.546-0.617 range across scopes (narrow set 0.546, equipment +
#      IPP over all commodities 0.576, calibration (c)'s bundle 0.569). The old 'all_machinery' keys are gone (no reader
#      since calibration_c.py moved to the new ones; meta.renamed_keys maps them). At the 2017 detail benchmark (402
#      industries) the same engine runs on finer types plus a labelled AI-compute composite (a construction, weights below).
#   3. Cost split (tot): full-chain shares of compensation (V001), taxes on production less subsidies (V002) and gross
#      operating surplus (V003); GOS split into consumption of fixed capital and net operating surplus industry by industry:
#      cfc_i = v_gos_i x min(CFC_i / GOS_i, 1), CFC from BEA Fixed Assets Table 3.4ESI (current-cost depreciation of private
#      fixed assets by industry; file created 2026-09-28), GOS from BEA GDP-by-industry TVA113 (published 2026-09-30) —
#      both newer than the I-O release they are applied to (CAVEATS; meta.vintage); housing = FA
#      residential assets (Table 2.4), other real estate = FA real estate less that; general government CFC/GOS = 1 by the
#      NIPA definition (checked); government enterprises from NIPA Table 7.5; where GOS is not positive (the fallback)
#      CFC per $ of gross output (TGO105) directly. The ratio is applied to the I-O's own (after-redefinitions) V003
#      row, so CFC + NOS = GOS within the I-O. The bases do not match cleanly where R&D is large: FA's CFC exceeds GDP by
#      industry's GOS for 334 in most years since 2011 (FA's R&D by industry follows the company-based R&D survey), so the
#      ratio is capped at 1 (central); the uncapped and the economy-wide-ratio (NIPA CFC/(CFC + NOS)) variants sit beside.
#      The full-chain NOS share is the upper bound on the fixed-quantity-rent share sigma (it also holds net interest,
#      profits and proprietors' income, and on the tot basis it prices imported inputs at US cost shares). Every capped and
#      every fallback industry-year is listed with its chain-weighted part (CAVEATS; cfc_cap_and_fallback; check C6, C22).
#   3b. G1, the bundle calibration (c) reads: equipment + IPP (F02E, F02N, F06E, F06N, F07E, F07N, F10E, F10N) plus private
#      nonresidential structures (F02S), all commodities, each commodity clipped at 0 (theta_tot 0.5686 in 2023). Its full
#      chain split on tot, dom and domp — compensation, CFC (three variants), taxes, NOS and imported content (nil on tot;
#      imported intermediates on dom; plus the imported share of the final products on domp), summing to 1 — its chain
#      compensation and hours shares (FTE and bridged) on each basis, and the fixed-rent bound on each basis: sigma_upper
#      = NOS (closed) or NOS + imported content (open), with the closure-multiplier bounds 1 + theta/sigma_upper and the
#      floor 1/(1 - theta) that holds for any sigma (results bundles, targets_for_macro g1_*; check C19). The same split for
#      equipment + IPP alone sits beside. IMPORT CONVENTION (dom, domp): the domestic share of commodity c is phi = q/(q + M),
#      imports' share of total supply — the lambda thread's convention, gated to its series; it assumes exports carry
#      imports in the same proportion as domestic uses. The domestic-use convention of BEA's import matrices (imports in
#      proportion to domestic use, exports excluded: 1 - M/(q + M - X)) is stored beside as a sensitivity for the bundle
#      (import_convention_domestic_use; checks C19, C20): it lowers the 2023 domp theta by about a point (0.470 -> 0.459),
#      the open multiplier bound 2.24 -> 2.17; tot is unchanged. HOURS: the bundle's bridged hours shares borrow the medium
#      (machinery) set's FTE-to-hours-worked bridge (0.904 in 2023), untested for the bundle's mix (R&D and professional
#      services, computer services, construction, trade); its FTE and bridged hours shares are a range, not a point
#      (targets_for_macro g1_*_hours_share_range_2023).
#   4. Service flow: theta_service = theta_asset x delta/(rho + delta), delta = BEA current-cost depreciation over the
#      average current-cost net stock (FA Tables 2.4 and 2.1) of the asset types each commodity becomes, rho in {0.04,
#      0.0575, 0.08}; aggregates by steady-state service cost, sum w theta / sum w (rho + delta)/delta. BEA's published
#      geometric rates (Tablecandtext.pdf, "BEA Rates of Depreciation, Service Lives, Declining-Balance Rates, and
#      Hulten-Wykoff Categories") are parsed for the cross-check. Traced: theta+ = theta/(1 - d), d the full-chain CFC share
#      (one-sector approximation: the capital used up along the chain is replaced by more of the same chain). rho's middle
#      value, keyed rho_central for continuity, is calibration (b)'s required return (macro.CAPITAL_BASE.rho, 0.0575),
#      imported and kept for comparison — not calibration (c)'s: (c)'s rho (0.0755) is an outcome of macro.calibrate_c, which
#      reads this file's targets (calibration_c.py), so converting the data at it here would be circular; the band 0.04-0.08
#      brackets both. Variants: the user cost with the
#      asset's price change relative to the GDP price index (FA 2.1 over FA 2.2, NIPA A191RG; 2015-2023 mean), and BEA's
#      published geometric rates in place of the implied D/K-bar (published_rate_variant_2023).
#   5. Per income: gamma_i lambda~_m = theta_m x w_i / wbar_chain,m — hours of machine-chain labour per hour of group i the
#      machine services replace. wbar_chain = full-chain compensation per full-chain hour. NIPA's hours-by-industry table
#      (6.9D) is no longer in BEA's Section 6 release and BLS files are off limits, so industry hours are NIPA Table 6.5D
#      full-time-equivalent employees x 2,080 (OEWS's own annualisation): wbar_i = NIPA 6.2D compensation / hours, and chain
#      hours per $ = sum_i v_w,i TR_i,m / wbar_i. For narrow/medium/broad the lambda thread's hours-worked construction
#      (lambda_us_hours_rent.csv, WIOD SEA levels + KLEMS-index tails) is used and the FTE basis is checked against it: the
#      FTE basis puts the chain's relative wage 5-19% higher (a uniform full-time year ignores schedule differences across
#      industries), so central per-income values are bridged to the hours-worked basis by the medium set's ratio each year.
#      w_i: OEWS national all-occupations hourly P10/P25/P50/P75/P90 (00-0000 row; 2001-2025 — the 1997-2000 files carry
#      no all-occupations row). Central basis: relative — (P_i / OEWS mean) x (economy compensation per hour / chain
#      compensation per hour), both ratios within one source; direct variant: P_i x NIPA compensation/wages (domestic
#      industries, A4002C/A4102C) / wbar_chain. The unbridged relative_fte values are a co-headline beside the central.
#   6. Targets for the macro block (results key targets_for_macro).
#   7. The model against the data: macro.calibrate's (a) and (b) with each model object on the data's basis — asset
#      theta_V = lambda v / Vm, service theta_V delta/(rho + delta), traced theta_V/(1 - a delta) (a delta: the capital used
#      up per unit of build cost, the model's CFC share) — and the multiples data/model basis by basis, the like-for-like
#      ones flagged, each row with its data scope (the chain share depends on scope: the set, equipment + IPP and (c)'s
#      bundle are all given; results model_vs_data; check C21).
#   8. Vintage: pull() reuses whatever is cached, so each source file's size, sha256 and own stamp lines ('Data published',
#      'File created'), zip-member dates or PDF date go into meta.vintage.
#
# DATA (all primary, publisher's own files; the large ones in the gitignored progress_and_prosperity/lambda/data/cache/,
# fetched where missing by pull() below — the I-O zips too, as that thread's pull_family_a.py fetches them — so a fresh
# clone runs `code/chains.py --pull` once before chains.py or checks/check_chains.py):
#   BEA I-O: AllTablesIO.zip, AllTablesSUP.zip (apps.bea.gov/industry/iTables Static Files); GDP by industry ValueAdded.xlsx;
#   BEA Fixed Assets Section1/2/3 (apps.bea.gov/national/FixedAssets/Release/XLS) and the depreciation-rate table
#   (apps.bea.gov/national/FA2004/Tablecandtext.pdf); NIPA Section 6 (apps.bea.gov/national/Release/XLS/Survey) and the NIPA
#   annual flat file (apps.bea.gov/national/Release/TXT/NipaDataA.txt); FRED A033RC1A027NBEA as a mirror cross-check (FRED's
#   annual wages series A576RC1A027NBEA ends in 2014, so wages come from the NIPA file); OEWS national zips cached in
#   companion/cache/ (oes*nat.zip, oesm*nat.zip).
#
# CAVEATS (the numbers are the run's; results notes, cfc_cap_and_fallback, service_relative_price_variant):
#   - CFC cap and fallback. The cap binds in 125 industry-years and the fallback applies in 18. It is not only R&D in 334
#     (capped 1999, 2001-2002, 2011-2023; up to 0.038 of $1 of the set's final output, 2001): 5415, 22-24% of the set's
#     weight in 1999-2007 (29-36% in 2015-2023), is capped in 1999 and 2001-2007 (up to 0.012, 2001) and on the fallback in
#     2000 (NOS -0.017); 514 is on the fallback in 1999-2001 (NOS down to -0.010); then 3361MV (capped 2008, fallback 2009),
#     523 (capped or fallback in 13 years), 211, 331, 481 (fallback 2002), GSLE (capped 2003-2023), 482, GFE (fallback 2013),
#     and a tail each under 1e-4 of the set's $1 (213, 313TT, 493, 713, 486, 483, 525, 315AL, 452, 55, 623, 622). In the (c)
#     bundle the order shifts toward the chains of what the bundle adds to the set: motor vehicles (3361MV, F02E equipment:
#     its 2009 fallback NOS -0.010 against -0.003 in the set) and structures (213, mining support, capped: 0.003, 2016). In
#     all, the cap removes at most 0.053 of $1 of the set's final output (0.026 in 2015-2023) and 0.020 of the (c) bundle's
#     (0.011): the 1999-2007 cost split is shaped by it, the 2015-2023 targets little.
#   - Releases differ. The I-O tables are the lambda thread's cached release (zip members dated Aug-Sep 2024, data to 2023);
#     the FA CFC and GDP-by-industry GOS are the Sep 2026 releases, so the CFC/GOS ratios are taken across releases and
#     applied to the older I-O's V003 row (2023 total GOS: I-O 11.72 $tn against TVA113 11.81 $tn, 0.75% apart; notes
#     io_release). pull() does not refresh the I-O while the gate is pinned to that release: it fetches a file only when
#     the cache lacks it, and a fresh clone gets BEA's current release (on 2026-10-01 byte-identical to the cached one;
#     meta.vintage records each file's sha256, so a later release shows).
#   - Exercised stock options are NIPA compensation (wages at exercise). In 511, 514 and 5415 part of that is a claim on
#     rents; around 2000 it depresses measured GOS (5415's GDP-by-industry GOS -3.1 $bn in 2000; 514's negative in
#     1999-2001), so theta is overstated there (514 reaches 1.002 in 2000). The bust's losses are not separated from it.
#   - The AI-compute composite's CFC/NOS split is an artefact of the cap: its 334 detail components inherit 334's capped
#     2017 ratio (1.17), so nearly all their GOS is CFC (334111 NOS 0.016, 334413 0.041). Not a sigma bound; the economy-wide-
#     ratio variant (CFC 0.208, NOS 0.307 against 0.395 / 0.120) sits beside.
#   - The service conversion omits the asset's relative price change: ICT and software prices fall about 4% a year against
#     the GDP price index (2015-2023), which raises their user cost and lowers the set's 2023 service share from 0.488 to
#     0.456 (-3.3 points; 334 -6.1, 5415 -5.8). And the service share depends on delta — the set's 0.218 in 2023 against
#     calibration (b)'s 0.08, at which the same theta 0.617 gives 0.359 — so it is not a free-standing target: theta_V and
#     delta go together (macro.calibrate_c targets them jointly). Steady state and one sector: a build-out's investment
#     exceeds replacement.
#   - Per income. The relative basis gives every percentile the economy-wide compensation/wage ratio (1.213 in 2023); benefit
#     loads are lower at low wages, so P10's value is biased up. The OEWS mean is job-weighted, not hours-weighted. The
#     central values carry the bridge (0.864-0.928) to the thread's hours-worked construction, whose 2015-2023 tail rests on
#     index extension from a KLEMS workbook with no recorded source URL; relative_fte is therefore published as a
#     co-headline. OEWS breaks: May panels 2002-03, SOC 2010 (2012), SOC 2018 (2019-21), model-based estimates (May 2021),
#     and the published top code ($70, $80 from 2008, $90 from 2011, $100 from 2016, $115 from May 2022); P10-P90 lie far
#     below every top code, so only the mean can be touched.
#   - The tot basis prices imported inputs at US cost shares; V001 is employee compensation only (proprietors' labour sits
#     in NOS, so theta is understated where contractors matter: 5415, 5412OP).
#   - Thresholds set after seeing the data: C2's detail tolerance, C6, C12, C15 (listed in checks/check_chains.py).
#
# Run from paths/:  ../venv/Scripts/python.exe code/chains.py
# Out: results/chains.json, figures/fig_chains.png
# Fetch only (a fresh clone; BEA's files into the gitignored cache, nothing computed or written):
#   ../venv/Scripts/python.exe code/chains.py --pull

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import zipfile
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
LAMBDA = os.path.join(REPO, "progress_and_prosperity", "lambda")
CACHE = os.path.join(LAMBDA, "data", "cache")                    # gitignored
PCACHE = os.path.join(ROOT, "cache")                             # small FRED csvs, as the other paths modules
OEWS_CACHE = os.path.join(REPO, "companion", "cache")
sys.path.insert(0, os.path.join(LAMBDA, "code"))
from compute_family_a import FD_EXCLUDE, RECON_TOL, SETS, open_xl, parse  # noqa: E402  (the thread's engine)
sys.path.insert(0, HERE)
import macro as m  # noqa: E402  (calibrations (a) and (b) for the model-against-data comparison; (b)'s required return)

YEARS = list(range(1997, 2024))
GATE_TOL = 1e-6
TYPES = {"333": "Machinery", "334": "Computer and electronic products", "335": "Electrical equipment",
         "511": "Publishing incl. software", "514": "Data processing, internet publishing, other info services",
         "5415": "Computer systems design", "532RL": "Rental and leasing"}
# the machinery + software set: six commodities (the broad set; 532RL carries no investment, so the medium set in effect),
# about 37% of equipment + IPP investment. Not "all machinery": it leaves out vehicles, aircraft, R&D (5412OP), furniture
# and the trade margins on equipment, and it includes government (defense) equipment. Formerly keyed "all_machinery".
SET = "machinery_software_set"
SET_LABEL = "machinery + software set (investment-weighted)"
SET_MEMBERS = SETS["broad"]
INV_EQ_IPP = ["F02E", "F02N", "F06E", "F06N", "F07E", "F07N", "F10E", "F10N"]
INV_STRUCT = ["F02S"]                                           # the variant adding private nonresidential structures
BUNDLES = {"equipment_ipp": INV_EQ_IPP, "equipment_ipp_structures": INV_EQ_IPP + INV_STRUCT}
BUNDLE_C = "equipment_ipp_structures"                           # the bundle calibration (c) reads (code/calibration_c.py)
BASES = ("tot", "dom", "domp")
IMPORT_DU_KEYS = [f"{q}_{b}" for b in ("dom", "domp") for q in ("theta", "cfc", "tax", "nos", "imports")] + \
    ["imports_intermediate_domp", "imports_final_domp", "comp_share_of_total_comp_dom", "comp_share_of_total_comp_domp"] + \
    [f"{q}_{b}" for b in ("dom", "domp") for q in ("sigma_upper_closed", "sigma_upper_open", "multiplier_floor_any_sigma",
                                                  "multiplier_lower_bound_closed", "multiplier_lower_bound_open")]
RHO_C = float(m.CAPITAL_BASE.rho)    # (b)'s required return, the middle of RHOS, kept for comparison; not (c)'s (circular: see 4.)
RHOS = (0.04, RHO_C, 0.08)
SVC, SVT = f"service_rho_{RHO_C}", f"service_traced_rho_{RHO_C}"
FTE_HOURS = 2080.0
PCTS = ["P10", "P25", "P50", "P75", "P90"]
REL_PRICE_WINDOW = (2015, 2023)                                 # mean relative price change for the user-cost variant

URLS = {
    # the I-O zips as the lambda thread's pull_family_a.py fetches them (same URLs, same gitignored cache); like every file
    # here, fetched only when missing and never refreshed once cached (meta.vintage records what was read)
    "AllTablesIO.zip": "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesIO.zip",
    "AllTablesSUP.zip": "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesSUP.zip",
    "ValueAdded.xlsx": "https://apps.bea.gov/industry/Release/XLS/GDPxInd/ValueAdded.xlsx",
    "GrossOutput.xlsx": "https://apps.bea.gov/industry/Release/XLS/GDPxInd/GrossOutput.xlsx",
    "Section2All_xls.xlsx": "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section2All_xls.xlsx",
    "Section3All_xls.xlsx": "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section3All_xls.xlsx",
    "Section6All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section6All_xls.xlsx",
    "NipaDataA.txt": "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt",
    "Tablecandtext.pdf": "https://apps.bea.gov/national/FA2004/Tablecandtext.pdf",
}

# ---- industry maps: I-O summary code -> names in each BEA table (occurrence index where a name repeats)
_SAME = {  # names shared by FA 3.4ESI, GDP-by-industry TVA113 and NIPA 6.xD
    "111CA": "Farms", "113FF": "Forestry, fishing, and related activities", "211": "Oil and gas extraction",
    "212": "Mining, except oil and gas", "213": "Support activities for mining", "22": "Utilities", "23": "Construction",
    "321": "Wood products", "327": "Nonmetallic mineral products", "331": "Primary metals",
    "332": "Fabricated metal products", "333": "Machinery", "334": "Computer and electronic products",
    "335": "Electrical equipment, appliances, and components", "3361MV": "Motor vehicles, bodies and trailers, and parts",
    "3364OT": "Other transportation equipment", "337": "Furniture and related products", "339": "Miscellaneous manufacturing",
    "311FT": "Food and beverage and tobacco products", "313TT": "Textile mills and textile product mills",
    "315AL": "Apparel and leather and allied products", "322": "Paper products",
    "323": "Printing and related support activities", "324": "Petroleum and coal products", "325": "Chemical products",
    "326": "Plastics and rubber products", "42": "Wholesale trade", "441": "Motor vehicle and parts dealers",
    "445": "Food and beverage stores", "452": "General merchandise stores", "4A0": "Other retail",
    "481": "Air transportation", "483": "Water transportation", "484": "Truck transportation",
    "485": "Transit and ground passenger transportation", "486": "Pipeline transportation",
    "487OS": "Other transportation and support activities", "493": "Warehousing and storage",
    "512": "Motion picture and sound recording industries", "513": "Broadcasting and telecommunications",
    "523": "Securities, commodity contracts, and investments", "524": "Insurance carriers and related activities",
    "525": "Funds, trusts, and other financial vehicles",
    "532RL": "Rental and leasing services and lessors of intangible assets", "5411": "Legal services",
    "5415": "Computer systems design and related services",
    "5412OP": "Miscellaneous professional, scientific, and technical services",
    "55": "Management of companies and enterprises", "561": "Administrative and support services",
    "562": "Waste management and remediation services", "61": "Educational services",
    "621": "Ambulatory health care services", "622": "Hospitals", "623": "Nursing and residential care facilities",
    "624": "Social assistance", "711AS": "Performing arts, spectator sports, museums, and related activities",
    "713": "Amusements, gambling, and recreation industries", "721": "Accommodation",
    "722": "Food services and drinking places", "81": "Other services, except government",
}
FA_CFC = {k: [(v, 0)] for k, v in _SAME.items()}
FA_CFC.update({"482": [("Railroad transportation", 0)], "511": [("Publishing industries (includes software)", 0)],
               "514": [("Information and data processing services", 0)],
               "521CI": [("Federal Reserve banks", 0), ("Credit intermediation and related activities", 0)]})
GDP_GOS = {k: (v, 0) for k, v in _SAME.items()}
GDP_GOS.update({"482": ("Rail transportation", 0), "511": ("Publishing industries, except internet (includes software)", 0),
                "514": ("Data processing, internet publishing, and other information services", 0),
                "521CI": ("Federal Reserve banks, credit intermediation, and related activities", 0),
                "HS": ("Housing", 0), "ORE": ("Other real estate", 0), "GFGD": ("National defense", 0),
                "GFGN": ("Nondefense", 0), "GFE": ("Government enterprises", 0), "GSLG": ("General government", 1),
                "GSLE": ("Government enterprises", 1)})
NIPA6 = {k: (v, 0) for k, v in _SAME.items()}
NIPA6.update({"482": ("Rail transportation", 0), "511": ("Publishing industries (includes software)", 0),
              "514": ("Information and data processing services", 0),
              "521CI": ("Federal Reserve banks, credit intermediation, and related activities", 0),
              "HS": ("Real estate", 0), "ORE": ("Real estate", 0), "GFGD": ("General government", 0),
              "GFGN": ("General government", 0), "GFE": ("Government enterprises", 0),
              "GSLG": ("General government", 1), "GSLE": ("Government enterprises", 1)})
GENERAL_GOV = ["GFGD", "GFGN", "GSLG"]                          # GOS = CFC by the NIPA definition
GOV_ENT_CFC = {"GFE": "B833RC", "GSLE": "B846RC"}               # NIPA Table 7.5 lines 26, 27

# ---- asset types (FA Tables 2.1 / 2.4 line names) each commodity becomes, for delta
TYPE_ASSETS = {
    "333": ["Engines and turbines", "Metalworking machinery", "Special industry machinery, n.e.c.",
            "General industrial, including materials handling, equipment", "Agricultural machinery",
            "Construction machinery", "Mining and oilfield machinery", "Service industry machinery",
            "Photocopy and related equipment"],
    "334": ["Computers and peripheral equipment", "Communication equipment", "Medical equipment and instruments",
            "Nonmedical instruments"],
    "335": ["Electrical transmission, distribution, and industrial apparatus", "Electrical equipment, n.e.c."],
    "511": ["Prepackaged"], "514": ["Software"], "5415": ["Custom"],
    "532RL": ["Nonresidential equipment"],
}
AGG_ASSETS = {"equipment + IPP (private nonresidential)": ["Nonresidential equipment",
                                                            "Nonresidential intellectual property products"],
              "equipment": ["Nonresidential equipment"], "IPP": ["Nonresidential intellectual property products"],
              "software": ["Software"], "information processing equipment": ["Information processing equipment"]}
PUBLISHED_RATE_KEYS = {"Prepackaged": "Prepackaged", "Custom": "Custom", "Own-account": "Own-account",
                       "Electrical transmission, distribution, and industrial apparatus":
                           "Electrical transmission, distribution, and industrial apparatus",
                       "Nonmedical instruments": "Nonmedical instruments"}

# ---- the 2017 detail benchmark
DETAIL_TYPES = {"334111": "Electronic computers", "334112": "Computer storage devices",
                "334118": "Computer terminals and peripherals", "334210": "Telephone apparatus",
                "334220": "Broadcast and wireless communications equipment", "334413": "Semiconductors",
                "334418": "Printed circuit assemblies", "334510": "Electromedical apparatus",
                "33329A": "Other industrial machinery (incl. NAICS 333249: industrial robots)",
                "333242": "Semiconductor machinery", "333517": "Machine tools", "333318": "Other commercial and service machinery",
                "333920": "Material handling equipment", "333120": "Construction machinery",
                "335312": "Motors and generators", "335314": "Relays and industrial controls",
                "511200": "Software publishers", "518200": "Data processing, hosting", "541511": "Custom computer programming",
                "541512": "Computer systems design", "54151A": "Other computer related services",
                "221100": "Electric power"}
DETAIL_INV = [c + "00" for c in INV_EQ_IPP]
# AI compute: an illustrative year of an AI data centre's cost at a ~5-year hardware life — hardware amortisation about
# three-fifths (accelerators and memory 0.40, the rest of the server 0.20), operation and facility services 0.25 (data
# processing and hosting, which also carries the building and networking staff), electric power 0.15. A construction, not a
# measurement: every component's own value is reported so any other weights can be applied.
AI_COMPUTE = {"334413": 0.40, "334111": 0.20, "518200": 0.25, "221100": 0.15}


# ------------------------------------------------------------------ fetching
FAMILY_A = ("AllTablesIO.zip", "AllTablesSUP.zip", "GrossOutput.xlsx", "ValueAdded.xlsx")   # also pull_family_a.py's


def pull(name: str) -> str:
    """BEA's file `name` in the gitignored lambda cache, fetched from apps.bea.gov first if it is not there (never refreshed
    once cached); stops with a clear message if it cannot be fetched."""
    fp = os.path.join(CACHE, name)
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        return fp
    alt = (" (or fetch it with the lambda thread's progress_and_prosperity/lambda/code/pull_family_a.py, which writes the "
           "same file to the same cache)" if name in FAMILY_A else "")
    try:
        import truststore
        truststore.inject_into_ssl()
        import requests
        r = requests.get(URLS[name], timeout=600)
    except Exception as err:  # noqa: BLE001  (no network, a proxy, a missing package: say which file and how to get it)
        raise SystemExit(f"BLOCKED: {name} not in {CACHE} and not fetched from {URLS[name]}: {type(err).__name__}: {err}{alt}")
    if r.status_code != 200 or len(r.content) < 1000:
        raise SystemExit(f"BLOCKED: {name} not in {CACHE}; {URLS[name]} gave http {r.status_code}{alt}")
    os.makedirs(CACHE, exist_ok=True)
    with open(fp, "wb") as fh:
        fh.write(r.content)
    return fp


def fred(sid: str) -> pd.Series:
    fp = os.path.join(PCACHE, f"{sid}.csv")
    if not os.path.exists(fp):
        import truststore
        truststore.inject_into_ssl()
        import requests
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", timeout=60)
        if r.status_code != 200 or "observation_date" not in r.text[:100]:
            raise SystemExit(f"FRED {sid}: not available")
        with open(fp, "w") as fh:
            fh.write(r.text)
    df = pd.read_csv(fp)
    return pd.Series(pd.to_numeric(df[sid], errors="coerce").values,
                     index=pd.to_datetime(df["observation_date"]).dt.year.values).dropna()


def vintage(fp: str, sheets: tuple = (), members: tuple = ()) -> dict:
    """What was read: pull() reuses a cached file whenever one exists, so every source's identity goes into the results —
    size, sha256 (first 16 hex), the file's own stamp lines ('Data published ...', 'File created ...') from each sheet
    read, the zip-member dates of the members read, or the PDF's creation date."""
    with open(fp, "rb") as fh:
        b = fh.read()
    out = {"file": os.path.relpath(fp, REPO).replace("\\", "/"), "bytes": len(b), "sha256_16": hashlib.sha256(b).hexdigest()[:16]}
    stamps = {}
    for sh in sheets:
        d = pd.read_excel(fp, sheet_name=sh, header=None, nrows=9, usecols=[0])
        stamps[sh] = [str(v).strip() for v in d[0] if isinstance(v, str)
                      and re.match(r"(Data published|File created|Release)", str(v).strip())]
    if stamps:
        out["stamps"] = stamps
    if members:
        zf = zipfile.ZipFile(io.BytesIO(b))
        out["member_dates"] = {mb: "%04d-%02d-%02d %02d:%02d" % zf.getinfo(mb).date_time[:5] for mb in members}
    if fp.endswith(".pdf"):
        mm = re.search(rb"/CreationDate\s*\(D:(\d{8,14})", b)
        out["pdf_creation"] = mm.group(1).decode() if mm else None
    if fp.endswith(".txt"):
        yrs = set(re.findall(rb"\n[A-Z0-9]+,(\d{4}),", b))
        out["last_period"] = max(int(x) for x in yrs) if yrs else None
    return out


def oews_top_codes() -> dict:
    """OEWS's published top code by year (the field descriptions: '# = indicates a wage equal to or greater than $X per
    hour'): $70 (2001-07), $80, $90, $100 and, from May 2022, $115. All-occupation P10-P90 lie far below every top code."""
    out = {}
    pat = re.compile(r"#\s*=\s*indicates a wage[^$]*\$\s?([\d.,]+)\s*per hour", re.I)
    for year in range(2001, 2026):
        name = f"oes{year % 100:02d}nat.zip" if year <= 2002 else f"oesm{year % 100:02d}nat.zip"
        zf = zipfile.ZipFile(os.path.join(OEWS_CACHE, name))
        for mb in [n for n in zf.namelist() if n.lower().endswith((".xls", ".xlsx"))]:
            x = pd.ExcelFile(io.BytesIO(zf.read(mb)))
            for sh in [s for s in x.sheet_names if "field" in s.lower() or "field" in mb.lower()]:
                for v in x.parse(sh, header=None).values.ravel():
                    mm = pat.search(v) if isinstance(v, str) else None
                    if mm and year not in out:
                        out[year] = float(mm.group(1).replace(",", ""))
    return out


# ------------------------------------------------------------------ BEA readers
def clean(s) -> str:
    s = re.sub(r"\\\d+\\", "", str(s))
    return s.strip().rstrip(",").strip()


def line_table(path: str, sheet: str) -> pd.DataFrame:
    """A BEA NIPA/FA/GDPxInd 'Line' sheet -> rows (in order) with a 'name' column and one column per year."""
    d = pd.read_excel(path, sheet_name=sheet, header=None)
    h = next(i for i in range(20) if str(d.iloc[i, 0]).strip() == "Line")
    years = {j: int(float(d.iloc[h, j])) for j in range(2, d.shape[1])
             if pd.notna(d.iloc[h, j]) and re.fullmatch(r"\d{4}(\.0)?", str(d.iloc[h, j]).strip())}
    rows = d.iloc[h + 1:]
    rows = rows[pd.to_numeric(rows[0], errors="coerce").notna()]
    out = pd.DataFrame({y: pd.to_numeric(rows[j], errors="coerce").values for j, y in years.items()})
    out.insert(0, "name", [clean(n) for n in rows[1]])
    return out.reset_index(drop=True)


def row(t: pd.DataFrame, name: str, occ: int = 0) -> pd.Series:
    hits = t.index[t["name"] == name].tolist()
    if len(hits) <= occ:
        raise SystemExit(f"BEA table: '{name}' occurrence {occ} not found")
    return t.loc[hits[occ]].drop("name").astype(float)


def tva113(path: str) -> dict:
    """GDP by industry, components of value added: (industry name, occurrence) -> DataFrame(comp, tax, gos) by year."""
    t = line_table(path, "TVA113-A")
    comps = {"Compensation of employees": "comp", "Taxes on production and imports less subsidies": "tax",
             "Gross operating surplus": "gos"}
    out, seen, i = {}, {}, 0
    while i < len(t):
        nm = t.loc[i, "name"]
        if nm in comps or nm == "Addenda:":
            i += 1
            continue
        block = {}
        j = i + 1
        while j < len(t) and t.loc[j, "name"] in comps:
            block[comps[t.loc[j, "name"]]] = t.loc[j].drop("name").astype(float).fillna(0.0)
            j += 1
        if block:
            k = seen.get(nm, 0)
            seen[nm] = k + 1
            out[(nm, k)] = pd.DataFrame(block)
        i = j if block else i + 1
    return out


def nipa_flat(path: str, codes: list[str]) -> dict:
    d = pd.read_csv(path, dtype=str)
    d.columns = ["code", "period", "value"]
    d = d[d["code"].isin(codes)]
    out = {}
    for c, g in d.groupby("code"):
        out[c] = pd.Series(pd.to_numeric(g["value"].str.replace(",", ""), errors="coerce").values,
                           index=g["period"].astype(int).values)
    return out


def published_rates(path: str) -> dict:
    """BEA's published geometric depreciation rates (Tablecandtext.pdf), text layer read from its Flate streams."""
    with open(path, "rb") as fh:
        b = fh.read()
    txt = []
    for s in re.findall(rb"stream\r?\n(.*?)\r?\nendstream", b, re.S):
        try:
            t = __import__("zlib").decompress(s)
        except Exception:
            continue
        for a, bb in re.findall(rb"\((.*?)\)\s*Tj|\[(.*?)\]\s*TJ", t, re.S):
            txt.append(a.decode("latin-1") if a else "".join(x.decode("latin-1") for x in re.findall(rb"\((.*?)\)", bb)))
    out = {}
    for line in txt:
        for key in PUBLISHED_RATE_KEYS:
            m = re.match(r"\s*" + re.escape(key) + r"\s*(/\d+/)?\s*(0\.\d{4})", line)
            if m and key not in out:
                out[key] = float(m.group(2))
    return out


def oews_all_occupations() -> pd.DataFrame:
    """OEWS national, all occupations (00-0000): hourly mean and P10..P90, 2001-2025."""
    rows = []
    for year in range(1997, 2026):
        name = f"oes{year % 100:02d}nat.zip" if year <= 2002 else f"oesm{year % 100:02d}nat.zip"
        zf = zipfile.ZipFile(os.path.join(OEWS_CACHE, name))
        mem = [n for n in zf.namelist() if "national" in os.path.basename(n).lower() and not n.endswith("/")]
        xls = pd.ExcelFile(io.BytesIO(zf.read(mem[0])))
        found = None
        for sh in xls.sheet_names:
            cand = pd.read_excel(xls, sheet_name=sh, header=None)
            for i in range(min(40, len(cand))):
                if (cand.iloc[i].astype(str).str.strip().str.lower() == "occ_code").any():
                    found = (cand, i)
                    break
            if found:
                break
        raw, h = found
        df = raw.iloc[h + 1:].copy()
        df.columns = raw.iloc[h].astype(str).str.strip().str.lower()
        if "i_group" in df.columns:
            df = df[df["i_group"].astype(str).str.strip() == "cross-industry"]
        if "own_code" in df.columns:
            df = df[df["own_code"].astype(str).str.strip() == "1235"]
        r = df[df["occ_code"].astype(str).str.strip() == "00-0000"]
        if not len(r):
            continue                                            # 1997-2000: no all-occupations row
        r = r.iloc[0]
        g = lambda *ks: float(str(next(r[k] for k in ks if k in r.index)).replace(",", "").strip())
        rows.append({"year": year, "mean": g("h_mean"), "P10": g("h_pct10", "h_wpct10"), "P25": g("h_pct25", "h_wpct25"),
                     "P50": g("h_median", "h_wpct50"), "P75": g("h_pct75", "h_wpct75"), "P90": g("h_pct90", "h_wpct90")})
    return pd.DataFrame(rows).set_index("year")


# ------------------------------------------------------------------ the engine, per year
@dataclass
class Year:
    yr: int
    inds: list
    coms: list
    TR: np.ndarray        # published IxC TR (import-comparable)
    TRdom: np.ndarray     # proportional domestic purge (the thread's)
    phi: np.ndarray
    v_w: np.ndarray
    v_tax: np.ndarray
    v_gos: np.ndarray
    v_imp: np.ndarray     # imported intermediates per $ industry output (dom leakage)
    g: np.ndarray         # industry output
    FD_thread: pd.Series
    FD_inv: pd.Series
    FD_invS: pd.Series
    recon_err: float
    phi_du: np.ndarray | None = None        # the domestic-use convention's domestic share, 1 - M/(q + M - X) (sensitivity)
    TRdom_du: np.ndarray | None = None
    v_imp_du: np.ndarray | None = None


def build_year(frames, yr: int) -> Year:
    tr, dr, mk, us = (parse(x.parse(str(yr), header=None)) for x in frames)
    inds = [i for i in tr.index if i in mk.index]
    coms = [c for c in tr.columns if c in mk.columns]
    V = mk.loc[inds, coms].fillna(0.0)
    q = V.sum(axis=0)
    W = np.nan_to_num(V.values / np.where(q.values[None, :] == 0, np.nan, q.values[None, :]))
    Bc = dr.loc[coms, inds].fillna(0.0).values
    TR = tr.loc[inds, coms].fillna(0.0).values
    Ic = np.eye(len(coms))
    recon = float(np.max(np.abs(W @ np.linalg.inv(Ic - Bc @ W) - TR)))
    M_c = (-us.loc[coms, "F050"].fillna(0.0)).clip(lower=0.0)
    phi = (q / (q + M_c)).clip(0.0, 1.0).fillna(0.0).values       # the thread's convention: imports' share of supply
    TRdom = W @ np.linalg.inv(Ic - (phi[:, None] * Bc) @ W)
    fd_cols = [c for c in us.columns if c.startswith("F") and c not in FD_EXCLUDE]
    missing = [c for c in INV_EQ_IPP + INV_STRUCT + ["F040"] if c not in us.columns]
    if missing:
        raise SystemExit(f"{yr}: final-use columns missing {missing}")
    fd = lambda cols: us.loc[coms, cols].fillna(0.0).sum(axis=1)
    # sensitivity: the domestic-use convention (imports in proportion to domestic use, exports excluded, as BEA's import
    # matrices assume): the imported share M/(q + M - X); where q + M - X is not positive, the thread's share
    den = (q + M_c - us.loc[coms, "F040"].fillna(0.0)).values
    phi_du = np.where(den > 0, 1.0 - np.clip(M_c.values / np.where(den > 0, den, 1.0), 0.0, 1.0), phi)
    TRdom_du = W @ np.linalg.inv(Ic - (phi_du[:, None] * Bc) @ W)
    return Year(yr, inds, coms, TR, TRdom, phi,
                dr.loc["V001", inds].fillna(0.0).values, dr.loc["V002", inds].fillna(0.0).values,
                dr.loc["V003", inds].fillna(0.0).values, ((1.0 - phi)[:, None] * Bc).sum(axis=0),
                V.sum(axis=1).values, fd(fd_cols), fd(INV_EQ_IPP), fd(INV_EQ_IPP + INV_STRUCT), recon,
                phi_du=phi_du, TRdom_du=TRdom_du, v_imp_du=((1.0 - phi_du)[:, None] * Bc).sum(axis=0))


def weights(Y: Year, members: list, fd: pd.Series) -> tuple[list, np.ndarray]:
    mem = [m for m in members if m in Y.coms]
    f = fd.loc[mem].clip(lower=0.0)
    return [Y.coms.index(m) for m in mem], (f / f.sum()).values


def shares(Y: Year, idx: list, f: np.ndarray, cfc: dict, h: np.ndarray | None) -> dict:
    """Full-chain shares of $1 of final output of the weighted bundle. cfc: industry CFC coefficients by variant —
    'central' (FA/GDP-by-industry ratio capped at GOS), 'uncapped', 'economywide'."""
    r, rd = Y.TR[:, idx] @ f, Y.TRdom[:, idx] @ f
    rp = Y.TRdom[:, idx] @ (Y.phi[idx] * f)
    out = {"theta_tot": float(Y.v_w @ r), "theta_dom": float(Y.v_w @ rd), "theta_domp": float(Y.v_w @ rp),
           "tax_tot": float(Y.v_tax @ r), "gos_tot": float(Y.v_gos @ r),
           "tax_dom": float(Y.v_tax @ rd), "gos_dom": float(Y.v_gos @ rd), "imports_dom": float(Y.v_imp @ rd),
           "cfc_dom": float(cfc["central"] @ rd)}
    for var, v in cfc.items():
        sfx = "" if var == "central" else f"_{var}"
        out[f"cfc_tot{sfx}"] = float(v @ r)
        out[f"nos_tot{sfx}"] = out["gos_tot"] - out[f"cfc_tot{sfx}"]
    out["nos_dom"] = out["gos_dom"] - out["cfc_dom"]
    if h is not None:
        for tag, rr in (("tot", r), ("dom", rd), ("domp", rp)):
            H = float(h @ rr)
            out[f"hours_per_dollar_{tag}"] = H
            out[f"wbar_chain_{tag}"] = out[f"theta_{tag}"] / H
    # the full split on every basis, every CFC variant: imported content is nil on tot by construction (imports priced at
    # US cost shares), the imported intermediates on dom, and on domp those plus the imported share of the final
    # products themselves — so compensation + CFC + taxes + NOS + imported content = 1 on each basis (checks C4, C19)
    out["imports_tot"] = 0.0
    out["tax_domp"], out["gos_domp"] = float(Y.v_tax @ rp), float(Y.v_gos @ rp)
    out["imports_intermediate_domp"] = float(Y.v_imp @ rp)
    out["imports_final_domp"] = float(f.sum() - Y.phi[idx] @ f)
    out["imports_domp"] = out["imports_intermediate_domp"] + out["imports_final_domp"]
    for var, v in cfc.items():
        sfx = "" if var == "central" else f"_{var}"
        if var != "central":
            out[f"cfc_dom{sfx}"] = float(v @ rd)
        out[f"cfc_domp{sfx}"] = float(v @ rp)
        for tag in ("dom", "domp"):
            out[f"nos_{tag}{sfx}"] = out[f"gos_{tag}"] - out[f"cfc_{tag}{sfx}"]
    return out


def bounds(s: dict) -> dict:
    """The fixed-quantity-rent bound on each basis and what it implies for the closure multiplier 1 + theta/sigma
    (macro.py: d ln v / d ln gamma at a fixed return). sigma <= NOS (closed: imported content is produced capital and
    labour abroad) or <= NOS + imported content (open: imports as a fixed-quantity claim); and sigma <= 1 - theta always,
    so the multiplier is at least 1/(1 - theta) whatever sigma is. Taxes have no counterpart in the model."""
    out = {}
    for b in BASES:
        th = s[f"theta_{b}"]
        out[f"sigma_upper_closed_{b}"] = s[f"nos_{b}"]
        out[f"sigma_upper_open_{b}"] = s[f"nos_{b}"] + s[f"imports_{b}"]
        out[f"multiplier_floor_any_sigma_{b}"] = 1.0 / (1.0 - th)
        out[f"multiplier_lower_bound_closed_{b}"] = 1.0 + th / out[f"sigma_upper_closed_{b}"]
        out[f"multiplier_lower_bound_open_{b}"] = 1.0 + th / out[f"sigma_upper_open_{b}"]
    return out


def chain_weighted_cfc(Y: Year, ratio: dict, per_out: dict, fvec: np.ndarray) -> dict:
    """Every capped and every fallback industry's part in $1 of a bundle's final output (tot): its GOS along the chain,
    the CFC the cap removes ((ratio - 1) x GOS), or, for a fallback industry, the CFC per $ of gross output it gets
    and the NOS that leaves. The removals sum to the bundle's uncapped less central CFC share (check C22)."""
    r = Y.TR @ fvec
    cap, fb = {}, {}
    for j, i in enumerate(Y.inds):
        gos = float(Y.v_gos[j] * r[j])
        if i in ratio and ratio[i] > 1.0:
            cap[i] = {"ratio": ratio[i], "gos_in_chain": gos, "cfc_removed_by_cap": (ratio[i] - 1.0) * gos}
        elif i in per_out:
            cfc = float(per_out[i] * r[j])
            fb[i] = {"gos_in_chain": gos, "cfc_in_chain": cfc, "nos_in_chain": gos - cfc}
    return {"capped": cap, "fallback": fb, "cap_removed_total": float(sum(v["cfc_removed_by_cap"] for v in cap.values()))}


# ------------------------------------------------------------------ side data: CFC ratios, wages by industry, delta
def cfc_ratios(fa34: pd.DataFrame, fa24: pd.DataFrame, gdp: dict, go: pd.DataFrame, nipa: dict, inds: list,
               yr: int) -> tuple[dict, dict, dict]:
    """CFC/GOS by I-O industry for one year (applied to the I-O's V003 coefficient); where GDP-by-industry GOS is not
    positive (514 in 1999-2001, 5415 in 2000, 481, 523, 525, 3361MV, GFE in single years: the list is in the results'
    cfc_ledger) the ratio is undefined and CFC per $ of gross output (TGO105) is used directly, so that industry's NOS is
    negative, as it was. Returns (ratio, per_output, ledger)."""
    gos = {k: float(gdp[GDP_GOS[k]].loc[yr, "gos"]) for k in GDP_GOS}
    cfc = {k: sum(float(row(fa34, n, o)[yr]) for n, o in v) for k, v in FA_CFC.items()}
    resid = float(row(fa24, "Residential equipment")[yr] + row(fa24, "Residential structures")[yr])
    cfc["HS"] = resid
    cfc["ORE"] = float(row(fa34, "Real estate")[yr]) - resid
    for k, s in GOV_ENT_CFC.items():
        cfc[k] = float(nipa[s][yr])
    ratio, per_output = {}, {}
    for i in inds:
        if i in GENERAL_GOV:
            ratio[i] = 1.0
        elif i in cfc and gos.get(i, 0.0) > 0:
            ratio[i] = cfc[i] / gos[i]
        elif i in cfc:
            per_output[i] = cfc[i] / float(row(go, *GDP_GOS[i])[yr])
        else:
            raise SystemExit(f"{yr}: no CFC/GOS match for industry {i}")
    ledger = {"fa_private_total": float(row(fa34, "Private fixed assets")[yr]),
              "fa_mapped_private": float(sum(v for k, v in cfc.items() if k not in GOV_ENT_CFC)),
              "general_gov_gos_gdpxind": float(sum(gos[k] for k in GENERAL_GOV)),
              "general_gov_cfc_nipa": float(nipa["B995RC"][yr] + nipa["B986RC"][yr]),
              "per_output_fallback": sorted(per_output)}
    return ratio, per_output, ledger


def wages_by_industry(t62: pd.DataFrame, t65: pd.DataFrame, t63: pd.DataFrame, inds: list, yr: int) -> tuple[np.ndarray, np.ndarray]:
    """Compensation per FTE hour (FTE x 2,080) and compensation/wages, by I-O industry."""
    w, cw = [], []
    for i in inds:
        n, o = NIPA6[i]
        comp, fte, wag = float(row(t62, n, o)[yr]), float(row(t65, n, o)[yr]), float(row(t63, n, o)[yr])
        w.append(comp * 1e6 / (fte * 1e3 * FTE_HOURS))
        cw.append(comp / wag)
    return np.array(w), np.array(cw)


def implied_delta(fa21: pd.DataFrame, fa24: pd.DataFrame, names: list, yr: int) -> float:
    D = sum(float(row(fa24, n)[yr]) for n in names)
    K = sum(0.5 * (float(row(fa21, n)[yr - 1]) + float(row(fa21, n)[yr])) for n in names)
    return D / K


def rel_price_change(fa21: pd.DataFrame, fa22: pd.DataFrame, names: list, defl: pd.Series, yr: int) -> float:
    """The asset group's price change relative to the GDP price index (NIPA A191RG), year yr: each line's stock price is
    current-cost net stock (FA 2.1) over its chain-type quantity index (FA 2.2); lines are weighted by last year's
    current-cost stock. Negative for ICT and software (their prices fall against the general price level)."""
    num = den = 0.0
    for n in names:
        c0, c1 = float(row(fa21, n)[yr - 1]), float(row(fa21, n)[yr])
        q0, q1 = float(row(fa22, n)[yr - 1]), float(row(fa22, n)[yr])
        num += c0 * ((c1 / q1) / (c0 / q0) - 1.0)
        den += c0
    return (1.0 + num / den) / (float(defl[yr]) / float(defl[yr - 1])) - 1.0


# ------------------------------------------------------------------ the 2017 detail benchmark
def detail_parse(df: pd.DataFrame) -> pd.DataFrame:
    r = next(i for i in range(12) if str(df.iloc[i, 0]).strip() == "Code")
    body = df.iloc[r + 1:, 2:].apply(pd.to_numeric, errors="coerce")
    body.index = [str(c).strip() for c in df.iloc[r + 1:, 0]]
    body.columns = [str(c).strip() for c in df.iloc[r, 2:]]
    return body


def detail_to_summary() -> dict:
    d = open_xl("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_2017_Detail.xlsx").parse("NAICS Codes", header=None)
    out, cur = {}, None
    for i in range(5, len(d)):
        s, det = d.iloc[i, 1], d.iloc[i, 3]
        if pd.notna(s) and str(s).strip():
            cur = str(s).strip()
        if pd.notna(det) and str(det).strip() and cur:
            out[str(det).strip()] = cur
    return out


def detail_benchmark(ratio17: dict, cfc_ew: float) -> dict:
    tr = detail_parse(open_xl("AllTablesSUP.zip", "IxC_TR_2017_PRO_DET.xlsx").parse("2017", header=None))
    dr = detail_parse(open_xl("AllTablesIO.zip", "CxI_DR_2017_Detail.xlsx").parse("2017", header=None))
    mk = detail_parse(open_xl("AllTablesIO.zip", "IOMake_After_Redefinitions_2017_Detail .xlsx").parse("2017", header=None))
    us = detail_parse(open_xl("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_2017_Detail.xlsx").parse("2017", header=None))
    inds = [i for i in tr.index if i in mk.index]
    coms = [c for c in tr.columns if c in mk.columns]
    V = mk.loc[inds, coms].fillna(0.0)
    q = V.sum(axis=0)
    W = np.nan_to_num(V.values / np.where(q.values[None, :] == 0, np.nan, q.values[None, :]))
    Bc = dr.loc[coms, inds].fillna(0.0).values
    TR = tr.loc[inds, coms].fillna(0.0).values
    Ic = np.eye(len(coms))
    recon = float(np.max(np.abs(W @ np.linalg.inv(Ic - Bc @ W) - TR)))
    M_c = (-us.loc[coms, "F05000"].fillna(0.0)).clip(lower=0.0)
    phi = (q / (q + M_c)).clip(0.0, 1.0).fillna(0.0).values
    TRdom = W @ np.linalg.inv(Ic - (phi[:, None] * Bc) @ W)
    v_w, v_tax, v_gos = (dr.loc[k, inds].fillna(0.0).values for k in ("V00100", "V00200", "V00300"))
    parent = detail_to_summary()
    unmapped = [i for i in inds if parent.get(i) not in ratio17]
    v_cfc = np.array([min(ratio17.get(parent.get(i), cfc_ew), 1.0) * gv for i, gv in zip(inds, v_gos)])
    v_cfc_ew = cfc_ew * v_gos                                     # the economy-wide-ratio variant: no inherited cap
    # at detail, noncomparable imports and used goods (S00300, S00402) have no domestic output, so their use as inputs
    # does not resolve to value added through the import-comparable TR: the identity is VA + that leakage = 1
    produced = q.values > 0
    leak0 = Bc[~produced, :].sum(axis=0)
    va_all = float(np.max(np.abs(((v_w + v_tax + v_gos + leak0) @ TR - 1.0)[produced])))
    out = {"recon_err": recon, "recon_tol": 1e-3, "industries": len(inds), "commodities": len(coms),
           "unmapped_to_summary_cfc": unmapped, "zero_output_commodities": [c for c, pr in zip(coms, produced) if not pr],
           "va_resolution_max_dev": va_all, "types": {}}
    for c, nm in DETAIL_TYPES.items():
        if c not in coms:
            out["types"][c] = {"name": nm, "exists": False}
            continue
        j = coms.index(c)
        e = {"name": nm, "exists": True, "summary_parent": parent.get(c),
             "theta_tot": float(v_w @ TR[:, j]), "theta_dom": float(v_w @ TRdom[:, j]),
             "theta_domp": float(phi[j] * (v_w @ TRdom[:, j])), "tax_tot": float(v_tax @ TR[:, j]),
             "gos_tot": float(v_gos @ TR[:, j]), "cfc_tot": float(v_cfc @ TR[:, j]), "import_share": float(1 - phi[j]),
             "unresolved_noncomparable_tot": float(leak0 @ TR[:, j]),
             "investment_$m": float(us.loc[c, [k for k in DETAIL_INV if k in us.columns]].fillna(0.0).sum())}
        e["nos_tot"] = e["gos_tot"] - e["cfc_tot"]
        e["cfc_tot_economywide"] = float(v_cfc_ew @ TR[:, j])
        e["nos_tot_economywide"] = e["gos_tot"] - e["cfc_tot_economywide"]
        e["summary_parent_ratio_capped"] = bool(ratio17.get(parent.get(c), 0.0) > 1.0)
        out["types"][c] = e
    ai = {}
    for tag in ("theta_tot", "theta_dom", "theta_domp", "tax_tot", "gos_tot", "cfc_tot", "nos_tot",
                "cfc_tot_economywide", "nos_tot_economywide"):
        ai[tag] = float(sum(w * out["types"][c][tag] for c, w in AI_COMPUTE.items()))
    out["ai_compute_composite"] = {"weights": AI_COMPUTE, **ai,
                                   "component_range_theta_tot": [min(out["types"][c]["theta_tot"] for c in AI_COMPUTE),
                                                                 max(out["types"][c]["theta_tot"] for c in AI_COMPUTE)],
                                   "cfc_nos_split_note": (
        "The central CFC/NOS split is an artefact of the cap: every 334 detail industry inherits 334's 2017 FA/GDP-by-"
        f"industry ratio ({ratio17['334']:.3f}, capped at 1), so nearly all of its GOS becomes CFC (334111 NOS "
        f"{out['types']['334111']['nos_tot']:.3f}, 334413 {out['types']['334413']['nos_tot']:.3f}). The composite's NOS "
        "therefore understates rents in the chain where IP and institutional rents are largest (semiconductors, AI) and "
        "is not a bound on sigma; the economy-wide-ratio variant (cfc_tot_economywide, nos_tot_economywide) sits beside. "
        "The composite also weights asset-basis thetas by annual-cost shares, which leaves out the return on the hardware.")}
    # the investment-weighted machinery + software set at detail, for the aggregation check against the summary 2017 value
    mem = [c for c in coms if parent.get(c) in SET_MEMBERS]
    finv = us.loc[mem, [k for k in DETAIL_INV if k in us.columns]].fillna(0.0).sum(axis=1).clip(lower=0.0)
    f = (finv / finv.sum()).values
    idx = [coms.index(c) for c in mem]
    out[f"{SET}_investment_weighted"] = {"theta_tot": float(v_w @ TR[:, idx] @ f),
                                                "theta_dom": float(v_w @ TRdom[:, idx] @ f),
                                                "theta_domp": float(v_w @ TRdom[:, idx] @ (phi[idx] * f)),
                                                "n_commodities": len(mem)}
    return out


# ------------------------------------------------------------------ main
def main():
    for n in URLS:
        pull(n)
    ref = pd.read_csv(os.path.join(LAMBDA, "data", "lambda_us_family_a.csv")).set_index("year")
    hrs_ref = pd.read_csv(os.path.join(LAMBDA, "data", "lambda_us_hours_rent.csv")).set_index("year")
    frames = (open_xl("AllTablesSUP.zip", "IxC_TR_1997-2023_Summary.xlsx"),
              open_xl("AllTablesIO.zip", "CxI_DR_1997-2023_Summary.xlsx"),
              open_xl("AllTablesIO.zip", "IOMake_After_Redefinitions_PRO_1997-2023_Summary.xlsx"),
              open_xl("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx"))
    fa21 = line_table(os.path.join(CACHE, "Section2All_xls.xlsx"), "FAAt201-A")
    fa22 = line_table(os.path.join(CACHE, "Section2All_xls.xlsx"), "FAAt202-A")
    fa24 = line_table(os.path.join(CACHE, "Section2All_xls.xlsx"), "FAAt204-A")
    fa34 = line_table(os.path.join(CACHE, "Section3All_xls.xlsx"), "FAAt304ESI-A")
    gdp = tva113(os.path.join(CACHE, "ValueAdded.xlsx"))
    go = line_table(os.path.join(CACHE, "GrossOutput.xlsx"), "TGO105-A")
    t62, t63, t65 = (line_table(os.path.join(CACHE, "Section6All_xls.xlsx"), s) for s in ("T60200D-A", "T60300D-A", "T60500D-A"))
    nipa = nipa_flat(os.path.join(CACHE, "NipaDataA.txt"),
                     ["A191RC", "A262RC", "W271RC", "A4002C", "A4102C", "A033RC", "B833RC", "B846RC", "B995RC", "B986RC",
                      "A191RG"])
    pub = published_rates(os.path.join(CACHE, "Tablecandtext.pdf"))
    oews = oews_all_occupations()
    top_codes = oews_top_codes()
    fred_comp = fred("A033RC1A027NBEA")
    # what was read (G7): every source's identity and its own vintage stamp
    oews_zips = {y: (f"oes{y % 100:02d}nat.zip" if y <= 2002 else f"oesm{y % 100:02d}nat.zip") for y in range(2001, 2026)}
    vint = {
        "AllTablesIO.zip": vintage(os.path.join(CACHE, "AllTablesIO.zip"), members=(
            "CxI_DR_1997-2023_Summary.xlsx", "IOMake_After_Redefinitions_PRO_1997-2023_Summary.xlsx",
            "IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx", "CxI_DR_2017_Detail.xlsx",
            "IOMake_After_Redefinitions_2017_Detail .xlsx", "IOUse_After_Redefinitions_PRO_2017_Detail.xlsx")),
        "AllTablesSUP.zip": vintage(os.path.join(CACHE, "AllTablesSUP.zip"),
                                    members=("IxC_TR_1997-2023_Summary.xlsx", "IxC_TR_2017_PRO_DET.xlsx")),
        "Section2All_xls.xlsx": vintage(os.path.join(CACHE, "Section2All_xls.xlsx"), sheets=("FAAt201-A", "FAAt202-A", "FAAt204-A")),
        "Section3All_xls.xlsx": vintage(os.path.join(CACHE, "Section3All_xls.xlsx"), sheets=("FAAt304ESI-A",)),
        "ValueAdded.xlsx": vintage(os.path.join(CACHE, "ValueAdded.xlsx"), sheets=("TVA113-A",)),
        "GrossOutput.xlsx": vintage(os.path.join(CACHE, "GrossOutput.xlsx"), sheets=("TGO105-A",)),
        "Section6All_xls.xlsx": vintage(os.path.join(CACHE, "Section6All_xls.xlsx"), sheets=("T60200D-A", "T60300D-A", "T60500D-A")),
        "NipaDataA.txt": vintage(os.path.join(CACHE, "NipaDataA.txt")),
        "Tablecandtext.pdf": vintage(os.path.join(CACHE, "Tablecandtext.pdf")),
        "A033RC1A027NBEA.csv (FRED mirror)": vintage(os.path.join(PCACHE, "A033RC1A027NBEA.csv")),
        "lambda_us_family_a.csv (the gate)": vintage(os.path.join(LAMBDA, "data", "lambda_us_family_a.csv")),
        "lambda_us_hours_rent.csv (the thread's hours)": vintage(os.path.join(LAMBDA, "data", "lambda_us_hours_rent.csv")),
        "OEWS national zips": {str(y): vintage(os.path.join(OEWS_CACHE, z)) for y, z in oews_zips.items()},
    }

    gate, per_year, recon = [], {}, {}
    types = {c: {} for c in TYPES}
    aggs, bundles = {}, {b: {} for b in BUNDLES}
    ledger_cfc, econ, imp_du, io_gos = {}, {}, {}, {}
    for yr in YEARS:
        Y = build_year(frames, yr)
        io_gos[yr] = float((Y.v_gos * Y.g).sum())
        recon[yr] = Y.recon_err
        if Y.recon_err > RECON_TOL:
            raise SystemExit(f"BLOCKED: {yr} reconstruction {Y.recon_err:.2e} > {RECON_TOL}")
        # 1. the gate — the thread's series, reproduced before anything new
        for s, mem in SETS.items():
            idx, f = weights(Y, mem, Y.FD_thread)
            for tag, v in (("tot", Y.v_w @ Y.TR[:, idx] @ f), ("dom", Y.v_w @ Y.TRdom[:, idx] @ f),
                           ("domp", Y.v_w @ Y.TRdom[:, idx] @ (Y.phi[idx] * f))):
                gate.append(abs(float(v) - float(ref.loc[yr, f"lam_{s}_{tag}"])))
        if max(gate) > GATE_TOL:
            raise SystemExit(f"GATE FAILED at {yr}: max |dev| {max(gate):.2e} vs lambda_us_family_a.csv")

        # 3. CFC coefficients
        ratio, per_out, led = cfc_ratios(fa34, fa24, gdp, go, nipa, Y.inds, yr)
        ledger_cfc[yr] = {**led, "ratio_machine_industries": {i: ratio.get(i) for i in TYPES}}
        v_cfc = np.array([min(ratio[i], 1.0) * gv if i in ratio else per_out[i] for i, gv in zip(Y.inds, Y.v_gos)])
        v_cfc_unc = np.array([ratio[i] * gv if i in ratio else per_out[i] for i, gv in zip(Y.inds, Y.v_gos)])
        ledger_cfc[yr]["cap_binds"] = sorted(i for i in ratio if ratio[i] > 1.0)
        ledger_cfc[yr]["cap_excess_share_of_io_gos"] = float(
            sum((ratio[i] - 1.0) * gv * g for i, gv, g in zip(Y.inds, Y.v_gos, Y.g) if i in ratio and ratio[i] > 1.0)
            / float((Y.v_gos * Y.g).sum()))
        kappa = float(nipa["A262RC"][yr] / (nipa["A262RC"][yr] + nipa["W271RC"][yr]))
        CFC = {"central": v_cfc, "uncapped": v_cfc_unc, "economywide": kappa * Y.v_gos}
        # 5. hours (1998+: NIPA 6.xD)
        h, wbar_i, cw_i = None, None, None
        if yr >= 1998:
            wbar_i, cw_i = wages_by_industry(t62, t65, t63, Y.inds, yr)
            h = Y.v_w / wbar_i
        comp_levels = Y.v_w * Y.g
        E = {"total_comp_io": float(comp_levels.sum()), "kappa_cfc_over_gos": kappa}
        if h is not None:
            E["total_hours_io_fte"] = float((h * Y.g).sum())
            E["wbar_us_fte"] = E["total_comp_io"] / E["total_hours_io_fte"]
            E["nipa_fte_hours_domestic"] = float(row(t65, "Domestic industries")[yr]) * 1e3 * FTE_HOURS / 1e6  # $m-units: millions of hours
            E["comp_over_wages_by_industry_mean"] = float(np.average(cw_i, weights=comp_levels))
        # labour embodied in fixed investment (6b): levels over all commodities, clipped at 0 (used equipment's negative
        # net sales are left out, as the thread's clip rule does)
        for tag_inv, fd in (("equipment_ipp", Y.FD_inv), ("equipment_ipp_structures", Y.FD_invS)):
            fl = fd.clip(lower=0.0).values
            E[f"inv_{tag_inv}_$m"] = float(fl.sum())
            for tag, Mx, ff in (("tot", Y.TR, fl), ("dom", Y.TRdom, fl), ("domp", Y.TRdom, Y.phi * fl)):
                E[f"inv_{tag_inv}_comp_{tag}_share_of_total_comp"] = float(Y.v_w @ Mx @ ff) / E["total_comp_io"]
                E[f"inv_{tag_inv}_theta_{tag}"] = float(Y.v_w @ Mx @ ff) / float(fl.sum())
                if h is not None:
                    E[f"inv_{tag_inv}_hours_{tag}_share_of_total_hours"] = float(h @ Mx @ ff) / E["total_hours_io_fte"]
            # G1: the bundle's full-chain cost split on every basis (the same linear map as the types and aggregates)
            B = shares(Y, list(range(len(Y.coms))), fl / fl.sum(), CFC, h)
            B.update(bounds(B))
            B["investment_$m"] = float(fl.sum())
            for tag in BASES:
                B[f"comp_share_of_total_comp_{tag}"] = E[f"inv_{tag_inv}_comp_{tag}_share_of_total_comp"]
                if h is not None:
                    B[f"hours_share_of_total_hours_fte_{tag}"] = E[f"inv_{tag_inv}_hours_{tag}_share_of_total_hours"]
            bundles[tag_inv][yr] = B
            ledger_cfc[yr].setdefault("chain_weighted", {})[tag_inv] = chain_weighted_cfc(Y, ratio, per_out, fl / fl.sum())
            if tag_inv == BUNDLE_C:          # the import-convention sensitivity: the same map with the domestic-use shares
                Yd = replace(Y, TRdom=Y.TRdom_du, phi=Y.phi_du, v_imp=Y.v_imp_du)
                Bd = shares(Yd, list(range(len(Y.coms))), fl / fl.sum(), CFC, None)
                Bd.update(bounds(Bd))
                for tag, ff in (("dom", fl), ("domp", Y.phi_du * fl)):
                    Bd[f"comp_share_of_total_comp_{tag}"] = float(Y.v_w @ Y.TRdom_du @ ff) / E["total_comp_io"]
                imp_du[yr] = {k: Bd[k] for k in IMPORT_DU_KEYS}
        E[f"{SET}_investment_$m"] = float(Y.FD_inv.loc[[c for c in SET_MEMBERS if c in Y.coms]].clip(lower=0.0).sum())
        E[f"{SET}_share_of_equipment_ipp_investment"] = E[f"{SET}_investment_$m"] / E["inv_equipment_ipp_$m"]
        econ[yr] = E

        # 2. theta by type (a single commodity: the weighting cancels)
        for c in TYPES:
            idx, f = weights(Y, [c], Y.FD_thread)
            s = shares(Y, idx, f, CFC, h)
            s["import_share"] = float(1.0 - Y.phi[idx[0]])
            s["investment_$m"] = float(Y.FD_inv.loc[c])
            s["final_uses_$m"] = float(Y.FD_thread.loc[c])
            types[c][yr] = s
        # aggregates: the thread's sets under both weightings, and the machinery + software set, investment-weighted
        for s_name, mem in SETS.items():
            for wname, fd in (("thread", Y.FD_thread), ("investment", Y.FD_inv)):
                idx, f = weights(Y, mem, fd)
                a = shares(Y, idx, f, CFC, h)
                a["weights"] = {Y.coms[i]: float(w) for i, w in zip(idx, f)}
                aggs.setdefault(f"{s_name}|{wname}", {})[yr] = a
        idx, f = weights(Y, SET_MEMBERS, Y.FD_inv)
        a = shares(Y, idx, f, CFC, h)
        a["weights"] = {Y.coms[i]: float(w) for i, w in zip(idx, f)}
        a.update(bounds(a))
        aggs.setdefault(f"{SET}|investment", {})[yr] = a
        fvec = np.zeros(len(Y.coms))
        fvec[idx] = f
        ledger_cfc[yr]["chain_weighted"][SET] = chain_weighted_cfc(Y, ratio, per_out, fvec)
        ledger_cfc[yr]["chain_weighted"][SET]["weights_of_capped_or_fallback_members"] = {
            Y.coms[i]: float(w) for i, w in zip(idx, f)
            if Y.coms[i] in ledger_cfc[yr]["cap_binds"] or Y.coms[i] in ledger_cfc[yr]["per_output_fallback"]}
        per_year[yr] = Y
        print(f"  {yr}: recon {Y.recon_err:.1e}, gate max {max(gate):.1e}", flush=True)

    # 4. delta, service flow, traced
    delta = {c: {yr: implied_delta(fa21, fa24, TYPE_ASSETS[c], yr) for yr in YEARS} for c in TYPES}
    delta_agg = {k: {yr: implied_delta(fa21, fa24, v, yr) for yr in range(1997, 2026)} for k, v in AGG_ASSETS.items()}
    delta_pub_types = {k: {yr: implied_delta(fa21, fa24, [k if k != "Own-account" else "Own account"], yr)
                           for yr in YEARS} for k in ("Prepackaged", "Custom", "Own-account")}

    def service_block(series: dict, wts: dict | None, c: str | None) -> dict:
        out = {"service": {str(r): {} for r in RHOS}, "traced": {}, "traced_service_central": {}, "delta": {}}
        for yr in YEARS:
            s = series[yr]
            if c is not None:
                dl = delta[c][yr]
                facs = {r: dl / (r + dl) for r in RHOS}
                out["delta"][yr] = dl
            else:   # aggregate: steady-state service cost of the weighted stock
                facs = {r: 1.0 / sum(w * (r + delta[k][yr]) / delta[k][yr] for k, w in wts[yr].items() if w > 0)
                        for r in RHOS}
                out["delta"][yr] = 1.0 / sum(w / delta[k][yr] for k, w in wts[yr].items() if w > 0)
            for r in RHOS:
                out["service"][str(r)][yr] = s["theta_tot"] * facs[r] if c is not None else \
                    sum(w * types[k][yr]["theta_tot"] for k, w in wts[yr].items()) * facs[r]
            d = s["cfc_tot"]
            out["traced"][yr] = s["theta_tot"] / (1.0 - d)
            out["traced_service_central"][yr] = out["service"][str(RHO_C)][yr] / (1.0 - d)
        return out

    svc = {c: service_block(types[c], None, c) for c in TYPES}
    inv_w = {yr: aggs[f"{SET}|investment"][yr]["weights"] for yr in YEARS}
    svc_agg = service_block(aggs[f"{SET}|investment"], inv_w, None)
    # the aggregate's own theta_tot and the weighted sum of types must agree (the same linear map)
    agg_consistency = max(abs(aggs[f"{SET}|investment"][yr]["theta_tot"]
                              - sum(w * types[k][yr]["theta_tot"] for k, w in inv_w[yr].items())) for yr in YEARS)
    # G5 variant: the user cost with the asset's relative price change, (rho + delta - pi_rel) V, pi_rel the group's price
    # change against the GDP price index, averaged over REL_PRICE_WINDOW (one year's change is noisy). Falling ICT and
    # software prices raise the user cost and lower the service share; the central conversion leaves this out.
    defl = nipa["A191RG"]
    w0, w1 = REL_PRICE_WINDOW
    pi_rel = {c: {yr: rel_price_change(fa21, fa22, TYPE_ASSETS[c], defl, yr) for yr in range(w0, w1 + 1)} for c in TYPES}
    pi_bar = {c: float(np.mean(list(v.values()))) for c, v in pi_rel.items()}
    relp = {"window": list(REL_PRICE_WINDOW), "price_index": "NIPA A191RG (GDP chain-type price index)",
            "pi_rel_mean": pi_bar, "pi_rel_annual": {c: {str(y): x for y, x in v.items()} for c, v in pi_rel.items()},
            "types_2023": {}}
    for c in TYPES:
        dl, th = delta[c][2023], types[c][2023]["theta_tot"]
        relp["types_2023"][c] = {"service_central": svc[c]["service"][str(RHO_C)][2023],
                                 "service_with_relative_price": th * dl / (RHO_C + dl - pi_bar[c])}
    w23 = inv_w[2023]
    relp["set_2023"] = {
        "service_central": svc_agg["service"][str(RHO_C)][2023],
        "service_with_relative_price": sum(w * types[k][2023]["theta_tot"] for k, w in w23.items())
        / sum(w * (RHO_C + delta[k][2023] - pi_bar[k]) / delta[k][2023] for k, w in w23.items() if w > 0)}
    relp["set_2023"]["difference_points"] = 100 * (relp["set_2023"]["service_with_relative_price"]
                                                   - relp["set_2023"]["service_central"])
    # BEA's published geometric rates against the implied D/K-bar for the single-line types (the service/asset factor at
    # the central rho under each): how much the choice of rate moves the service share
    pub_var = {}
    for k, dp in pub.items():
        line = "Own account" if k == "Own-account" else k
        di = implied_delta(fa21, fa24, [line], 2023)
        pub_var[k] = {"published_geometric": dp, "implied_D_over_Kbar_2023": di,
                      "implied_over_steady_state_published": di / (dp / (1.0 - dp / 2.0)),
                      "service_over_asset_implied": di / (RHO_C + di), "service_over_asset_published": dp / (RHO_C + dp)}

    # 5. per income
    comp_wage = {yr: float(nipa["A4002C"][yr] / nipa["A4102C"][yr]) for yr in range(1998, 2026)}
    thread_wrel = {s: {yr: float(hrs_ref.loc[yr, f"wrel_{s}_tot"]) for yr in YEARS} for s in SETS}
    # the FTE-basis relative chain wage against the thread's hours-worked basis (validation of the hours source), and the
    # bridge: FTE x 2,080 ignores that full-time schedules differ across industries, which compresses measured hourly
    # pay in short-hour industries and so raises the chain's relative wage; the medium set (the aggregate's commodities,
    # thread weights) carries the thread's hours-worked correction over to the investment aggregate and the types
    wrel_cmp = {s: {yr: {"fte_basis": aggs[f"{s}|thread"][yr]["wbar_chain_tot"] / econ[yr]["wbar_us_fte"],
                         "thread_hours_basis": thread_wrel[s][yr]} for yr in YEARS if yr >= 1998} for s in SETS}
    bridge = {yr: wrel_cmp["medium"][yr]["thread_hours_basis"] / wrel_cmp["medium"][yr]["fte_basis"]
              for yr in YEARS if yr >= 1998}
    for yr in bridge:
        for tag_inv in ("equipment_ipp", "equipment_ipp_structures"):
            for tag in BASES:
                k = f"inv_{tag_inv}_hours_{tag}_share_of_total_hours"
                econ[yr][k + "_bridged_hours_worked"] = econ[yr][k] / bridge[yr]
                bundles[tag_inv][yr][f"hours_share_of_total_hours_bridged_{tag}"] = econ[yr][k + "_bridged_hours_worked"]
    per_income = {}
    for yr in [y for y in YEARS if y in oews.index and y >= 1998]:
        o = oews.loc[yr]
        wus = econ[yr]["wbar_us_fte"]
        P = {"yr": yr, "oews": {k: float(o[k]) for k in ["mean"] + PCTS}, "comp_over_wages_nipa": comp_wage[yr],
             "wbar_us_fte_comp_per_hour": wus, "hours_bridge_medium": bridge[yr], "rows": {}}

        def rowset(label, theta_basis: dict, wbar_chain: float, wrel_hw: float):
            wrel_fte = wbar_chain / wus
            P["rows"][label] = {
                basis: {
                    "central_relative_hours_worked": {k: th * (float(o[k]) / float(o["mean"])) / wrel_hw for k in PCTS},
                    "relative_fte": {k: th * (float(o[k]) / float(o["mean"])) / wrel_fte for k in PCTS},
                    "direct_fte": {k: th * float(o[k]) * comp_wage[yr] / wbar_chain for k in PCTS}}
                for basis, th in theta_basis.items()}
            P["rows"][label].update({"wbar_chain_fte": wbar_chain, "wrel_fte": wrel_fte, "wrel_hours_worked": wrel_hw})
        A = aggs[f"{SET}|investment"][yr]
        for tag in ("tot", "dom", "domp"):
            wb = A[f"wbar_chain_{tag}"]
            th = {"asset": A[f"theta_{tag}"]}
            if tag == "tot":
                th[SVC] = svc_agg["service"][str(RHO_C)][yr]
                th[SVT] = svc_agg["traced_service_central"][yr]
            rowset(f"{SET}|investment|{tag}", th, wb, wb / wus * bridge[yr])
        for c in TYPES:
            S = types[c][yr]
            wb = S["wbar_chain_tot"]
            rowset(f"type {c}|tot", {"asset": S["theta_tot"], SVC: svc[c]["service"][str(RHO_C)][yr],
                                     SVT: svc[c]["traced_service_central"][yr]},
                   wb, wb / wus * bridge[yr])
        for s in SETS:   # the thread's hours-worked construction for its own sets (thread weights)
            A2 = aggs[f"{s}|thread"][yr]
            rowset(f"{s}|thread|tot", {"asset": A2["theta_tot"]}, A2["wbar_chain_tot"], thread_wrel[s][yr])
        per_income[str(yr)] = P

    # 6. economy ratios (NIPA flat file: the publisher's own; FRED mirror checked for compensation)
    nipa_ratios = {yr: {"cfc_over_gdp": float(nipa["A262RC"][yr] / nipa["A191RC"][yr]),
                        "nos_over_gdp": float(nipa["W271RC"][yr] / nipa["A191RC"][yr]),
                        "comp_over_gdp": float(nipa["A4002C"][yr] / nipa["A191RC"][yr])} for yr in range(1997, 2026)}
    # FRED ships $ billions, the NIPA file $ millions
    fred_check = {yr: {"fred_A033RC1A027NBEA": float(fred_comp.loc[yr]) * 1e3, "nipa_A033RC": float(nipa["A033RC"][yr])}
                  for yr in (2015, 2020, 2023, 2025) if yr in fred_comp.index}

    # the detail benchmark
    kappa17 = econ[2017]["kappa_cfc_over_gos"]
    ratio17, per17, _ = cfc_ratios(fa34, fa24, gdp, go, nipa, per_year[2017].inds, 2017)
    if per17:
        raise SystemExit(f"2017: per-output CFC fallback not wired into the detail run: {per17}")
    det = detail_benchmark(ratio17, kappa17)

    # 7. the model against the data (G7): calibrations (a) and (b) from macro.py, each model object put on the data's
    # basis. Model: build cost Vm = a p_m + lambda v + b, service cost (rho + delta) Vm; its untraced share theta_V =
    # lambda v / Vm is the data's theta (the Leontief chain has no capital inputs); service share theta_V delta/(rho +
    # delta); the capital used up building a machine is a delta per unit of build cost (the data's CFC share d), so traced
    # = theta_V / (1 - a delta) as the data's theta / (1 - d). (a) is the flow benchmark (rho 0, delta 1): its service
    # share is its asset share, and so is the data's at rho 0 — so (a)'s like-for-like comparison is the asset basis.
    model = {}
    for cal, base in (("a", m.CALIBRATION_BASE), ("b", m.CAPITAL_BASE)):
        e, q, _, err = m.calibrate(base=base)
        u, d = e.delta / (e.rho + e.delta), e.a * e.delta
        model[cal] = {"rho": e.rho, "delta": e.delta, "a": e.a, "calibration_max_residual": err,
                      "theta_V_asset": q["theta_V"], "theta_V_service": q["theta_V"] * u, "cfc_share_of_build_cost": d,
                      "theta_V_traced_asset": q["theta_V"] / (1.0 - d), "theta_V_traced_service": q["theta_V"] * u / (1.0 - d),
                      "kappa_V": q["kappa_V"], "sigma_V": q["sigma_V"], "multiplier": q["multiplier"],
                      "chain_share": q["chain_share"], "capital_output": q["capital_output"]}
    A = aggs[f"{SET}|investment"]
    Bc = bundles[BUNDLE_C]
    kc = f"inv_{BUNDLE_C}"
    data23 = {
        "set_asset": (A[2023]["theta_tot"], f"aggregates['{SET}|investment']['2023']['theta_tot']"),
        "set_service": (svc_agg["service"][str(RHO_C)][2023], f"{SET}_service['service']['{RHO_C}']['2023'] (data delta)"),
        "set_traced_asset": (svc_agg["traced"][2023], f"{SET}_service['traced']['2023']"),
        "set_traced_service": (svc_agg["traced_service_central"][2023], f"{SET}_service['traced_service_central']['2023']"),
        "bundle_asset": (Bc[2023]["theta_tot"], f"bundles['{BUNDLE_C}']['2023']['theta_tot']"),
        "bundle_comp_share": (econ[2023][f"{kc}_comp_tot_share_of_total_comp"],
                              f"economy['2023']['{kc}_comp_tot_share_of_total_comp']"),
        "bundle_hours_share": (econ[2023][f"{kc}_hours_tot_share_of_total_hours_bridged_hours_worked"],
                               f"economy['2023']['{kc}_hours_tot_share_of_total_hours_bridged_hours_worked']"),
        "bundle_hours_share_fte": (econ[2023][f"{kc}_hours_tot_share_of_total_hours"],
                                   f"economy['2023']['{kc}_hours_tot_share_of_total_hours']"),
        "eqipp_comp_share": (econ[2023]["inv_equipment_ipp_comp_tot_share_of_total_comp"],
                             "economy['2023']['inv_equipment_ipp_comp_tot_share_of_total_comp']"),
        "set_comp_share": (A[2023]["theta_tot"] * econ[2023][f"{SET}_investment_$m"] / econ[2023]["total_comp_io"],
                           f"aggregates['{SET}|investment']['2023']['theta_tot'] x economy['2023']['{SET}_investment_$m'] / "
                           "economy['2023']['total_comp_io']")}
    scope_of = {"set": SET_LABEL, "bundle": "calibration (c)'s bundle: equipment + IPP + private nonresidential structures, "
                "all commodities", "eqipp": "equipment + IPP (private and government), all commodities"}
    for cal in ("a", "b"):   # the data's asset share put on the model's (rho, delta): theta x delta_m / (rho_m + delta_m)
        u = model[cal]["delta"] / (model[cal]["rho"] + model[cal]["delta"])
        data23[f"set_service_at_model_{cal}_rho_delta"] = (A[2023]["theta_tot"] * u, f"set_asset x {u:.6f}")
    cmp = {}
    for key, cal, mk, dk, like, basis in (
            ("a|asset", "a", "theta_V_asset", "set_asset", True,
             "asset (build cost); at (a)'s rho 0 the service share equals the asset share on both sides"),
            ("a|traced_asset", "a", "theta_V_traced_asset", "set_traced_asset", True, "traced asset"),
            ("a|service_at_model_rho_delta", "a", "theta_V_service", "set_service_at_model_a_rho_delta", True,
             "service at (a)'s (rho, delta): the same as the asset basis"),
            ("a|service_data_rho_central", "a", "theta_V_service", "set_service", False,
             f"mixed: the data converted at rho {RHO_C}, the model's flow share at its rho 0"),
            ("a|traced_service_data_rho_central", "a", "theta_V_traced_service", "set_traced_service", False,
             f"mixed: traced, the data at rho {RHO_C}, the model at rho 0"),
            ("a|bundle_asset", "a", "theta_V_asset", "bundle_asset", True, "asset, calibration (c)'s bundle"),
            ("a|chain_share_comp", "a", "chain_share", "bundle_comp_share", True,
             "chain share of compensation (one wage in the model: its hours share is its compensation share)"),
            ("a|chain_share_hours", "a", "chain_share", "bundle_hours_share", True,
             "chain share of hours (hours worked, via the medium set's bridge, borrowed)"),
            ("a|chain_share_hours_fte", "a", "chain_share", "bundle_hours_share_fte", True, "chain share of hours (FTE, no bridge)"),
            ("a|chain_share_comp_eqipp", "a", "chain_share", "eqipp_comp_share", True, "chain share of compensation"),
            ("a|chain_share_comp_set", "a", "chain_share", "set_comp_share", True, "chain share of compensation"),
            ("b|asset", "b", "theta_V_asset", "set_asset", True, "asset (build cost)"),
            ("b|service_own_delta", "b", "theta_V_service", "set_service", True,
             f"service, each at rho {RHO_C} and its own delta (data 2023 set delta against the model's 0.08)"),
            ("b|service_at_model_rho_delta", "b", "theta_V_service", "set_service_at_model_b_rho_delta", True,
             "service, both at the model's (rho, delta): the same multiple as the asset basis"),
            ("b|traced_asset", "b", "theta_V_traced_asset", "set_traced_asset", True, "traced asset"),
            ("b|traced_service_own_delta", "b", "theta_V_traced_service", "set_traced_service", True,
             "traced service, each at its own delta"),
            ("b|bundle_asset", "b", "theta_V_asset", "bundle_asset", True, "asset, calibration (c)'s bundle"),
            ("b|chain_share_comp", "b", "chain_share", "bundle_comp_share", True, "chain share of compensation"),
            ("b|chain_share_hours", "b", "chain_share", "bundle_hours_share", True,
             "chain share of hours (hours worked, via the medium set's bridge, borrowed)"),
            ("b|chain_share_hours_fte", "b", "chain_share", "bundle_hours_share_fte", True, "chain share of hours (FTE, no bridge)"),
            ("b|chain_share_comp_eqipp", "b", "chain_share", "eqipp_comp_share", True, "chain share of compensation"),
            ("b|chain_share_comp_set", "b", "chain_share", "set_comp_share", True, "chain share of compensation")):
        dv, src = data23[dk]
        cmp[key] = {"calibration": cal, "basis": basis, "scope": scope_of[dk.split("_")[0]], "like_for_like": like,
                    "model_key": mk, "model": model[cal][mk], "data_key": dk, "data": dv, "data_source": src,
                    "multiple": dv / model[cal][mk]}
    model_vs_data = {"model": model, "data_2023": {k: v[0] for k, v in data23.items()}, "comparisons": cmp,
                     "note": "multiple = data / model on the stated basis; like_for_like False marks a mixed-basis figure "
                             "kept only because earlier prose quoted it. like_for_like is about the basis, not the scope: "
                             "each row names its data scope",
                     "scope_note": (
                         "The chain share depends heavily on scope (2023, tot: the set "
                         f"{data23['set_comp_share'][0]:.4f}, equipment + IPP {data23['eqipp_comp_share'][0]:.4f}, (c)'s bundle "
                         f"{data23['bundle_comp_share'][0]:.4f}). The (a)/(b) model's machine chain stands for all produced "
                         f"capital ((b)'s capital stock is {model['b']['capital_output']:.2f}x income, set against all fixed "
                         "capital, housing structures inside it), so of the three the widest, (c)'s bundle, is the nearest "
                         "match, and it still leaves out residential investment; the set and equipment + IPP rows show how much "
                         "of the multiple is scope.")}

    # G3: every capped and every fallback industry-year, with its chain-weighted part in $1 of the set's and the bundle's
    # final output (the per-year detail sits in cfc_ledger[year]['chain_weighted'])
    capfb = {}
    for key in (SET, BUNDLE_C):
        inds_ = {}
        for yr in YEARS:
            cw = ledger_cfc[yr]["chain_weighted"][key]
            for i, v in cw["capped"].items():
                e_ = inds_.setdefault(i, {"capped_years": [], "fallback_years": [], "cfc_removed_by_cap": {}, "fallback": {}})
                e_["capped_years"].append(yr)
                e_["cfc_removed_by_cap"][str(yr)] = v["cfc_removed_by_cap"]
            for i, v in cw["fallback"].items():
                e_ = inds_.setdefault(i, {"capped_years": [], "fallback_years": [], "cfc_removed_by_cap": {}, "fallback": {}})
                e_["fallback_years"].append(yr)
                e_["fallback"][str(yr)] = v
        for i, e_ in inds_.items():
            e_["max_cfc_removed_by_cap"] = max(e_["cfc_removed_by_cap"].values(), default=0.0)
        tot_rm = {str(yr): ledger_cfc[yr]["chain_weighted"][key]["cap_removed_total"] for yr in YEARS}
        capfb[key] = {"industries": inds_, "cap_removed_total_by_year": tot_rm,
                      "cap_removed_total_max": max(tot_rm.values()),
                      "cap_removed_total_max_2015_2023": max(tot_rm[str(y)] for y in range(2015, 2024))}
    capfb["set_weight_5415"] = {str(yr): inv_w[yr].get("5415", 0.0) for yr in YEARS}
    gos_by = lambda i, yrs: {str(y): float(gdp[GDP_GOS[i]].loc[y, "gos"]) for y in yrs}  # noqa: E731
    capfb["gdpxind_gos_$m"] = {"5415": gos_by("5415", range(1998, 2003)), "514": gos_by("514", range(1998, 2003))}

    # ---- assemble
    ys = lambda d: {str(k): v for k, v in d.items()}  # noqa: E731
    mean_ = lambda d, a=2015, b=2023: float(np.mean([d[y] for y in range(a, b + 1)]))  # noqa: E731
    W15 = range(2015, 2024)
    res = {"meta": {
        "unit": "paths Unit 1 — machine-chain labour share by type, cost split, service flow, per-income hours",
        "years": [YEARS[0], YEARS[-1]], "investment_columns_equipment_ipp": INV_EQ_IPP,
        "investment_columns_structures_variant": INV_STRUCT, "rhos": list(RHOS), "rho_central": RHO_C,
        "rho_central_source": "macro.CAPITAL_BASE.rho (calibration (b)'s required return), imported",
        "rho_central_label": ("the middle of the rho band, calibration (b)'s required return, kept for comparison; not the central "
                              "calibration (c)'s rho (0.0755), which is an outcome of macro.calibrate_c reading this file's targets, so "
                              "converting the data at it here would be circular; the 0.04-0.08 band brackets both"),
        "fte_hours": FTE_HOURS, "ai_compute_weights": AI_COMPUTE, "type_assets_for_delta": TYPE_ASSETS,
        "hours_source": "NIPA Table 6.5D FTE employees x 2,080 (Table 6.9D hours no longer published in BEA's Section 6); "
                        "narrow/medium/broad also on the lambda thread's hours-worked construction",
        "cfc_source": "FA Table 3.4ESI / GDP-by-industry TVA113 GOS by industry, applied to the I-O V003 row; general "
                      "government = 1; government enterprises NIPA 7.5; housing = FA residential",
        "set_label": SET_LABEL, "set_members": SET_MEMBERS,
        "bundles": {k: {"investment_columns": v, "commodities": "all, each commodity's sum clipped at 0"}
                    for k, v in BUNDLES.items()},
        "renamed_keys": {"aggregates['all_machinery|investment']": f"aggregates['{SET}|investment']",
                         "per_income[year]['rows']['all_machinery|investment|<basis>']":
                             f"per_income[year]['rows']['{SET}|investment|<basis>']",
                         "targets_for_macro['a_theta_V_all_machinery_investment_weighted']":
                             f"targets_for_macro['a_theta_V_{SET}_investment_weighted']",
                         "targets_for_macro['d_cost_split_all_machinery_investment_weighted_tot']":
                             f"targets_for_macro['d_cost_split_{SET}_investment_weighted_tot']",
                         "note": "the old 'all_machinery' names and where the values now are; the identical copies under the "
                                 "old names were dropped (no reader: code/calibration_c.py reads the new keys)"},
        "import_convention": ("dom/domp: phi = q/(q + M), imports' share of total supply (the lambda thread's convention, "
                              "gated to its series; it assumes exports carry imports in the same proportion as domestic "
                              "uses). Sensitivity for the (c) bundle: the domestic-use convention of BEA's import matrices, "
                              "1 - M/(q + M - X) (import_convention_domestic_use)."),
        "io_release_vs_gdpxind_gos_2023": {"io_total_gos_$m": io_gos[2023],
                                           "tva113_total_gos_$m": float(gdp[("Gross domestic product", 0)].loc[2023, "gos"]),
                                           "gap_share": float(gdp[("Gross domestic product", 0)].loc[2023, "gos"]) / io_gos[2023] - 1.0},
        "oews_top_code_hourly": ys(top_codes),
        "vintage": vint},
        "gate": {"max_abs_dev": max(gate), "n_values": len(gate), "tol": GATE_TOL, "recon_err_max": max(recon.values())},
        "types": {c: {"name": TYPES[c], "annual": ys(types[c]), "delta": ys(svc[c]["delta"]),
                      "service": {r: ys(v) for r, v in svc[c]["service"].items()}, "traced": ys(svc[c]["traced"]),
                      "traced_service_central": ys(svc[c]["traced_service_central"])} for c in TYPES},
        "aggregates": {k: ys(v) for k, v in aggs.items()},
        f"{SET}_service": {"delta": ys(svc_agg["delta"]), "service": {r: ys(v) for r, v in svc_agg["service"].items()},
                           "traced": ys(svc_agg["traced"]), "traced_service_central": ys(svc_agg["traced_service_central"]),
                           "consistency_max_dev": agg_consistency},
        "bundles": {k: ys(v) for k, v in bundles.items()},
        "delta_aggregates": {k: ys(v) for k, v in delta_agg.items()},
        "delta_software_implied": {k: ys(v) for k, v in delta_pub_types.items()},
        "published_rates_pdf": pub, "published_rate_variant_2023": pub_var,
        "service_relative_price_variant": relp,
        "cfc_ledger": ys(ledger_cfc), "cfc_cap_and_fallback": capfb,
        "economy": ys(econ),
        "nipa_ratios": ys(nipa_ratios), "fred_mirror_check": ys(fred_check),
        "oews_all_occupations": {str(k): v for k, v in oews.to_dict(orient="index").items()},
        "per_income": per_income,
        "wrel_validation": {s: ys(v) for s, v in wrel_cmp.items()}, "hours_bridge_medium": ys(bridge),
        "detail_2017": det,
        "model_vs_data": model_vs_data,
        "import_convention_domestic_use": {BUNDLE_C: ys(imp_du)},
    }
    # 6. targets for the macro block
    E = econ
    rng = {"narrow set (333, 334, 335), investment-weighted": aggs["narrow|investment"][2023]["theta_tot"],
           "equipment + IPP, all commodities": bundles["equipment_ipp"][2023]["theta_tot"],
           "equipment + IPP + private nonresidential structures, all commodities (calibration (c))": Bc[2023]["theta_tot"],
           SET_LABEL: A[2023]["theta_tot"]}
    g1_keys = [f"{q}_{b}" for b in BASES for q in ("theta", "cfc", "tax", "nos", "imports")] + \
              [f"{q}_{b}_{v}" for b in BASES for v in ("uncapped", "economywide") for q in ("cfc", "nos")] + \
              ["imports_intermediate_domp", "imports_final_domp"] + \
              [f"{q}_{b}" for b in BASES for q in ("comp_share_of_total_comp", "hours_share_of_total_hours_fte",
                                                    "hours_share_of_total_hours_bridged", "sigma_upper_closed",
                                                    "sigma_upper_open", "multiplier_floor_any_sigma",
                                                    "multiplier_lower_bound_closed", "multiplier_lower_bound_open")] + \
              ["investment_$m"]
    tg = {
        f"a_theta_V_{SET}_investment_weighted": {
            "tot_2023": A[2023]["theta_tot"], "dom_2023": A[2023]["theta_dom"], "domp_2023": A[2023]["theta_domp"],
            "tot_mean_2015_2023": mean_({y: A[y]["theta_tot"] for y in YEARS}),
            "dom_mean_2015_2023": mean_({y: A[y]["theta_dom"] for y in YEARS}),
            "domp_mean_2015_2023": mean_({y: A[y]["theta_domp"] for y in YEARS}),
            "label": SET_LABEL,
            "set_share_of_equipment_ipp_investment_2023": E[2023][f"{SET}_share_of_equipment_ipp_investment"],
            "range_2023_tot_across_scopes": rng, "range_2023_tot": [min(rng.values()), max(rng.values())]},
        "b_labour_embodied_in_fixed_investment": {
            k: {"2023": E[2023][k], "mean_2015_2023": mean_({y: E[y][k] for y in range(2015, 2024)})}
            for k in ["inv_equipment_ipp_comp_domp_share_of_total_comp", "inv_equipment_ipp_comp_tot_share_of_total_comp",
                      "inv_equipment_ipp_hours_domp_share_of_total_hours", "inv_equipment_ipp_hours_tot_share_of_total_hours",
                      "inv_equipment_ipp_structures_comp_domp_share_of_total_comp",
                      "inv_equipment_ipp_structures_hours_domp_share_of_total_hours",
                      "inv_equipment_ipp_hours_domp_share_of_total_hours_bridged_hours_worked",
                      "inv_equipment_ipp_theta_tot", "inv_equipment_ipp_theta_domp"]},
        "c_nipa": {k: {"2023": nipa_ratios[2023][k], "mean_2015_2023": mean_({y: nipa_ratios[y][k] for y in YEARS})}
                   for k in ["cfc_over_gdp", "nos_over_gdp"]},
        f"d_cost_split_{SET}_investment_weighted_tot": {
            k: {"2023": A[2023][f"{k}_tot"], "mean_2015_2023": mean_({y: A[y][f"{k}_tot"] for y in YEARS})}
            for k in ["theta", "cfc", "tax", "nos"]},
        "d_cost_split_dom": {k: {"2023": A[2023][k], "mean_2015_2023": mean_({y: A[y][k] for y in YEARS})}
                             for k in ["theta_dom", "cfc_dom", "tax_dom", "nos_dom", "imports_dom"]},
        f"d_cost_split_{SET}_domp": {k: {"2023": A[2023][k], "mean_2015_2023": mean_({y: A[y][k] for y in YEARS})}
                                     for k in ["theta_domp", "cfc_domp", "tax_domp", "nos_domp", "imports_domp"]},
        f"d_bounds_{SET}": {k: {"2023": A[2023][k], "mean_2015_2023": mean_({y: A[y][k] for y in YEARS})}
                            for k in bounds(A[2023])},
        "e_delta_equipment_ipp_private": {"2023": delta_agg["equipment + IPP (private nonresidential)"][2023],
                                          "mean_2015_2023": mean_(delta_agg["equipment + IPP (private nonresidential)"]),
                                          f"{SET}_investment_weighted_2023": svc_agg["delta"][2023]},
        f"service_flow_{SET}_2023": {r: svc_agg["service"][r][2023] for r in svc_agg["service"]},
        f"traced_{SET}_2023": svc_agg["traced"][2023],
        f"traced_service_central_{SET}_2023": svc_agg["traced_service_central"][2023],
        f"g1_{BUNDLE_C}_full_chain": {k: {"2023": Bc[2023][k], "mean_2015_2023": mean_({y: Bc[y][k] for y in W15})}
                                      for k in g1_keys},
        f"g1_{BUNDLE_C}_scope": (
            "Exactly the bundle calibration (c) reads (economy[year]['inv_equipment_ipp_structures_theta_tot']): fixed "
            "investment in equipment and IPP, private (F02E, F02N) and government (F06E, F06N, F07E, F07N, F10E, F10N), plus "
            "private nonresidential structures (F02S), all commodities, each commodity's sum clipped at 0. On each basis "
            "theta (compensation) + cfc + tax + nos + imports (imported content) = 1: tot prices imports at US cost shares "
            "(imports 0); dom counts imported intermediates; domp adds the imported share of the final products. "
            "sigma_upper_closed = NOS, sigma_upper_open = NOS + imported content; the multiplier bounds are 1 + theta/sigma "
            "at those bounds and 1/(1 - theta) for any sigma. Means are of the annual values. Import convention (dom, domp): "
            "the domestic share phi = q/(q + M), imports' share of total supply (the lambda thread's, gated to its series); "
            "the domestic-use convention of BEA's import matrices, 1 - M/(q + M - X), gives in 2023 theta_domp "
            f"{imp_du[2023]['theta_domp']:.4f} (against {Bc[2023]['theta_domp']:.4f}), chain compensation share domp "
            f"{imp_du[2023]['comp_share_of_total_comp_domp']:.4f} ({Bc[2023]['comp_share_of_total_comp_domp']:.4f}), NOS domp "
            f"{imp_du[2023]['nos_domp']:.4f} ({Bc[2023]['nos_domp']:.4f}), imported content domp {imp_du[2023]['imports_domp']:.4f} "
            f"({Bc[2023]['imports_domp']:.4f}), open multiplier bound {imp_du[2023]['multiplier_lower_bound_open_domp']:.2f} "
            f"({Bc[2023]['multiplier_lower_bound_open_domp']:.2f}), floor {imp_du[2023]['multiplier_floor_any_sigma_domp']:.2f} "
            f"({Bc[2023]['multiplier_floor_any_sigma_domp']:.2f}); tot is unchanged (g1_*_import_convention_domestic_use). "
            "Hours: hours_share_of_total_hours_bridged_* borrows the medium (machinery) set's FTE-to-hours-worked bridge "
            f"({bridge[2023]:.3f} in 2023), untested for the bundle's mix (R&D and professional services, computer services, "
            "construction, trade), so the FTE and bridged shares are a range, not a point (g1_*_hours_share_range_2023)."),
        f"g1_{BUNDLE_C}_hours_share_range_2023": {
            b: sorted([Bc[2023][f"hours_share_of_total_hours_fte_{b}"], Bc[2023][f"hours_share_of_total_hours_bridged_{b}"]])
            for b in BASES},
        f"g1_{BUNDLE_C}_import_convention_domestic_use": {
            k: {"2023": imp_du[2023][k], "mean_2015_2023": mean_({y: imp_du[y][k] for y in W15})} for k in IMPORT_DU_KEYS},
    }
    res["targets_for_macro"] = tg
    pi23 = per_income["2023"]["rows"][f"{SET}|investment|tot"]
    res["headline"] = {
        "gate_max_abs_dev": max(gate),
        "theta_2023_by_type_tot": {c: types[c][2023]["theta_tot"] for c in TYPES},
        "theta_V_2023_tot": A[2023]["theta_tot"], "theta_V_2023_dom": A[2023]["theta_dom"],
        "theta_service_2023_central": svc_agg["service"][str(RHO_C)][2023],
        "per_income_2023_service_central": pi23[SVC]["central_relative_hours_worked"],
        "per_income_2023_service_relative_fte": pi23[SVC]["relative_fte"],
        "hours_bridge_2023": bridge[2023],
        "per_income_2023_asset": pi23["asset"]["central_relative_hours_worked"],
        "per_income_2023_service_traced": pi23[SVT]["central_relative_hours_worked"],
        "ai_compute_theta_tot_2017": det["ai_compute_composite"]["theta_tot"],
        "g1_bundle_2023": {b: {q: Bc[2023][f"{q}_{b}"] for q in ("theta", "cfc", "tax", "nos", "imports")} for b in BASES},
        "g1_bundle_mean_2015_2023": {b: {q: mean_({y: Bc[y][f"{q}_{b}"] for y in YEARS})
                                         for q in ("theta", "cfc", "tax", "nos", "imports")} for b in BASES},
        "model_vs_data_multiples": {k: v["multiple"] for k, v in cmp.items()},
    }
    res["notes"] = notes(res)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "chains.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps({"gate": res["gate"], "headline": res["headline"],
                      "g1": tg[f"g1_{BUNDLE_C}_full_chain"]}, indent=1))
    figure(res)

# ------------------------------------------------------------------ notes (the caveats, with their numbers from the run)
def spans(years: list) -> str:
    """[1999, 2001, 2002, 2003] -> '1999, 2001-2003'."""
    out, ys_ = [], sorted(int(y) for y in years)
    i = 0
    while i < len(ys_):
        j = i
        while j + 1 < len(ys_) and ys_[j + 1] == ys_[j] + 1:
            j += 1
        out.append(str(ys_[i]) if i == j else f"{ys_[i]}-{ys_[j]}")
        i = j + 1
    return ", ".join(out)


def fx(x: float) -> str:
    return f"{x:.4f}" if abs(x) >= 5e-5 else f"{x:.1e}"


def cap_lines(capfb_key: dict) -> list:
    """One line per industry: capped years and the largest CFC the cap removes, fallback years and the CFC/NOS they get."""
    out = []
    inds = capfb_key["industries"]
    for i in sorted(inds, key=lambda k: -max([inds[k]["max_cfc_removed_by_cap"]]
                                             + [abs(v["nos_in_chain"]) for v in inds[k]["fallback"].values()])):
        e = inds[i]
        s = i
        if e["capped_years"]:
            ymax = max(e["cfc_removed_by_cap"], key=e["cfc_removed_by_cap"].get)
            s += f" capped {spans(e['capped_years'])} (removes up to {fx(e['max_cfc_removed_by_cap'])}, {ymax})"
        if e["fallback_years"]:
            fb = "; ".join(f"{y} CFC {fx(v['cfc_in_chain'])} NOS {fx(v['nos_in_chain'])}" for y, v in e["fallback"].items())
            s += (";" if e["capped_years"] else "") + f" fallback {spans(e['fallback_years'])} ({fb})"
        out.append(s)
    return out


def notes(res: dict) -> dict:
    A23 = res["aggregates"][f"{SET}|investment"]["2023"]
    tg = res["targets_for_macro"][f"a_theta_V_{SET}_investment_weighted"]
    svc, rp = res[f"{SET}_service"], res["service_relative_price_variant"]
    cf = res["cfc_cap_and_fallback"]
    w5415 = cf["set_weight_5415"]
    w_cap = [w5415[str(y)] for y in cf[SET]["industries"]["5415"]["capped_years"]
             + cf[SET]["industries"]["5415"]["fallback_years"]]
    w_rec = [w5415[str(y)] for y in range(2015, 2024)]
    d_b = m.CAPITAL_BASE.delta
    th, sv, dl = A23["theta_tot"], svc["service"][str(RHO_C)]["2023"], svc["delta"]["2023"]
    P23 = res["per_income"]["2023"]
    tc = res["meta"]["oews_top_code_hourly"]
    changes = [f"${tc[y]:.0f} from {y}" for k, y in enumerate(sorted(tc)) if k == 0 or tc[y] != tc[sorted(tc)[k - 1]]]
    br = list(res["hours_bridge_medium"].values())
    g_ = cf["gdpxind_gos_$m"]
    t514 = res["types"]["514"]["annual"]
    ai = res["detail_2017"]["ai_compute_composite"]
    return {
        "set_label": (
            f"The '{SET_LABEL}' (keyed '{SET}'; formerly 'all machinery') is six commodities ({', '.join(SET_MEMBERS[:-1])}; "
            f"532RL carries no investment), {tg['set_share_of_equipment_ipp_investment_2023']:.0%} of equipment + IPP "
            "investment in 2023. It leaves out vehicles, aircraft, R&D (5412OP's F02N), furniture and the trade margins on "
            "equipment (weights at producers' prices), and it includes government equipment, defense among it. Its 2023 "
            f"theta_tot {th:.3f} is the top of a {tg['range_2023_tot'][0]:.3f}-{tg['range_2023_tot'][1]:.3f} range across "
            "scopes (range_2023_tot_across_scopes)."),
        "cfc_cap_and_fallback": {
            "summary": (
                "Where FA's CFC exceeds GDP-by-industry GOS the ratio is capped at 1 (central); where GOS is not positive, "
                "CFC per $ of gross output is used (fallback). It is not only R&D in 334: 5415 carries "
                f"{min(w_cap):.0%}-{max(w_cap):.0%} of the set's weight in those years ({min(w_rec):.0%}-{max(w_rec):.0%} "
                f"in 2015-2023) and is capped in {spans(cf[SET]['industries']['5415']['capped_years'])} and on the "
                "fallback in "
                f"{spans(cf[SET]['industries']['5415']['fallback_years'])}, so the set's 1999-2007 cost split is shaped by "
                f"it. The cap removes at most {cf[SET]['cap_removed_total_max']:.4f} of $1 of the set's final output in any "
                f"year ({cf[SET]['cap_removed_total_max_2015_2023']:.4f} in 2015-2023) and at most "
                f"{cf[BUNDLE_C]['cap_removed_total_max']:.4f} of the (c) bundle's "
                f"({cf[BUNDLE_C]['cap_removed_total_max_2015_2023']:.4f} in 2015-2023); each removal is (ratio - 1) x the "
                "industry's GOS along the chain, per $1 of final output (tot). Exercised stock options in NIPA compensation "
                "also depress tech GOS around 2000 (stock_options)."),
            f"per_industry_{SET}": cap_lines(cf[SET]), f"per_industry_{BUNDLE_C}": cap_lines(cf[BUNDLE_C])},
        "stock_options": (
            "NIPA compensation includes exercised employee stock options (recorded in wages and salaries at exercise). In "
            "the tech industries (511, 514, 5415) part of that is a claim on rents, and around 2000 it depresses measured "
            f"GOS: GDP-by-industry GOS of 5415 was {g_['5415']['2000']:,.0f} $m in 2000 and of 514 "
            f"{g_['514']['1999']:,.0f} / {g_['514']['2000']:,.0f} / {g_['514']['2001']:,.0f} $m in 1999-2001, which puts "
            f"them on the per-output CFC fallback, and 514's theta_tot reaches {t514['2000']['theta_tot']:.3f} in 2000. "
            "The dot-com bust's losses and the option exercises are not separated here."),
        "ai_composite": ai["cfc_nos_split_note"] + (
            f" Economy-wide-ratio variant: CFC {ai['cfc_tot_economywide']:.3f}, NOS {ai['nos_tot_economywide']:.3f} "
            f"(central CFC {ai['cfc_tot']:.3f}, NOS {ai['nos_tot']:.3f})."),
        "service_conversion": (
            "(i) The user cost is (rho + delta) V, with no term for the asset's relative price change. ICT and software "
            f"prices fall against the GDP price index (mean {rp['window'][0]}-{rp['window'][1]}: 334 "
            f"{rp['pi_rel_mean']['334']:+.3f}, 511 {rp['pi_rel_mean']['511']:+.3f}, 514 {rp['pi_rel_mean']['514']:+.3f}, "
            f"5415 {rp['pi_rel_mean']['5415']:+.3f}, 333 {rp['pi_rel_mean']['333']:+.3f} a year), which raises their user "
            f"cost and lowers the service share: with it the set's 2023 service share is "
            f"{rp['set_2023']['service_with_relative_price']:.3f} against {sv:.3f} central "
            f"({rp['set_2023']['difference_points']:+.1f} points; service_relative_price_variant). (ii) The service share "
            f"depends on delta: the set's 2023 delta is {dl:.3f}, calibration (b)'s {d_b}; at (b)'s delta the same theta "
            f"{th:.3f} gives {th * d_b / (RHO_C + d_b):.3f}, not {sv:.3f}. The service share is therefore not a free-standing "
            "target: theta_V and delta are targeted jointly (macro.calibrate_c does). (iii) The conversion is steady-state "
            "and one-sector: during a build-out, investment exceeds replacement."),
        "per_income": (
            "(i) The relative basis gives every percentile the economy-wide compensation/wage ratio "
            f"({P23['comp_over_wages_nipa']:.3f} in 2023). Benefit loads are lower at low wages, so P10's compensation per "
            "hour, and with it P10's chain hours per hour replaced, is overstated (an upward bias at P10, smaller or "
            "reversed toward the top). The OEWS mean in the ratio is job-weighted, not hours-weighted. (ii) The central "
            f"values carry the bridge to the lambda thread's hours-worked construction ({P23['hours_bridge_medium']:.3f} in "
            f"2023; {min(br):.3f}-{max(br):.3f} over 1998-2023), which rests on WIOD SEA levels to 2014 and KLEMS-index tails "
            "for 2015-23 from a KLEMS workbook (klems_ilpa_1997_2024.xlsx) with no recorded source URL; so the unbridged "
            "relative_fte values are published beside it as a co-headline (headline per_income_2023_service_relative_fte). "
            "(iii) OEWS method breaks: the 2002-03 move to May panels, SOC 2010 in 2012, SOC 2018 phased in over 2019-21, "
            "model-based estimation from May 2021, and the published top code (a wage at or above it is shown as '#'): "
            f"{', '.join(changes)} (the May 2022 change: $100 -> $115). All-occupation P10-P90 lie far below every top "
            f"code (2023 P90 ${P23['oews']['P90']:.2f}), so only the mean, the relative basis's denominator, can be "
            "touched, if its top band moved with the code (not verified)."),
        "rho_central": f"rho_central {RHO_C} is imported from macro.CAPITAL_BASE.rho, not hard-coded: calibration (b)'s return, kept for "
                       "comparison (the key's name predates calibration (c), whose own rho, 0.0755, is an outcome of calibrate_c reading "
                       "this file's targets — circular here).",
        "io_release": (
            "The I-O tables are the lambda thread's cached release (zip members dated "
            f"{min(d_ for d_ in res['meta']['vintage']['AllTablesIO.zip']['member_dates'].values())} to "
            f"{max(d_ for d_ in res['meta']['vintage']['AllTablesIO.zip']['member_dates'].values())}; data to 2023); the FA CFC and "
            "GDP-by-industry GOS behind the CFC/GOS ratios are the Sep 2026 releases, so the ratios are taken across releases "
            "and applied to the older I-O's V003 row. 2023 total GOS: I-O "
            f"{res['meta']['io_release_vs_gdpxind_gos_2023']['io_total_gos_$m'] / 1e6:.3f} $tn, TVA113 "
            f"{res['meta']['io_release_vs_gdpxind_gos_2023']['tva113_total_gos_$m'] / 1e6:.3f} $tn "
            f"({res['meta']['io_release_vs_gdpxind_gos_2023']['gap_share']:.2%} apart). pull() does not refresh the I-O while "
            "the gate is pinned to that release."),
    }


# ------------------------------------------------------------------ figure
def figure(res: dict):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3df"
    cat = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
                         "ytick.color": muted, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.9), gridspec_kw={"width_ratios": [1.35, 1, 1]})
    yrs = [int(y) for y in res["types"]["333"]["annual"]]
    S = res[f"{SET}_service"]
    # (1) theta by type, asset basis, tot, with the set's service-flow band
    ax = axes[0]
    ends = {}
    for k, c in enumerate(TYPES):
        v = [res["types"][c]["annual"][str(y)]["theta_tot"] for y in yrs]
        ax.plot(yrs, v, lw=1.6, color=cat[k])
        ends[c] = (v[-1], cat[k], c)
    agg = [res["aggregates"][f"{SET}|investment"][str(y)]["theta_tot"] for y in yrs]
    ax.plot(yrs, agg, lw=2.6, color=ink, label=f"{SET_LABEL}, asset basis")
    ends["set"] = (agg[-1], ink, "set")
    svc_end = S["service"][str(RHO_C)][str(yrs[-1])]
    ends["svc"] = (svc_end, ink, f"set, service (rho {RHO_C})")
    placed = []                                                   # direct labels, nudged apart, each with a leader line
    for key, (v, col, lab) in sorted(ends.items(), key=lambda kv: kv[1][0]):
        y = v if not placed or v - placed[-1] >= 0.032 else placed[-1] + 0.032
        placed.append(y)
        ax.annotate(lab, (yrs[-1], v), xytext=(yrs[-1] + 1.3, y), textcoords="data", fontsize=7.5, color=col, va="center",
                    fontweight="bold" if key in ("set", "svc") else "normal",
                    arrowprops={"arrowstyle": "-", "color": col, "lw": 0.6, "shrinkA": 0, "shrinkB": 1})
    lo = [S["service"]["0.08"][str(y)] for y in yrs]
    hi = [S["service"]["0.04"][str(y)] for y in yrs]
    ax.fill_between(yrs, lo, hi, color=muted, alpha=0.22, lw=0, label="its service-flow share, rho 0.04-0.08")
    ax.plot(yrs, [S["service"][str(RHO_C)][str(y)] for y in yrs], lw=1.2, ls="--", color=ink,
            label=f"its service-flow share at rho {RHO_C}")
    ax.set_ylim(0, 1.08)
    ax.set_xlim(yrs[0], yrs[-1] + 5.5)
    ax.annotate("514 ≈ 1 in 2000: GOS < 0 in 1999-2001 (bust losses; exercised\nstock options booked as compensation)",
                (2000, res["types"]["514"]["annual"]["2000"]["theta_tot"]), xytext=(2002.2, 1.0), fontsize=6.8, color=muted,
                va="center", arrowprops={"arrowstyle": "-", "color": muted, "lw": 0.6})
    ax.grid(axis="y", color=grid, lw=0.8)
    ax.set_ylabel("full-chain compensation share of $1 of final output")
    ax.set_title("Labour's share of the machine chain, by type (tot)", loc="left", fontsize=10, color=ink)
    handles = [plt.Line2D([], [], color=cat[k], lw=1.6, label=f"{c} {TYPES[c]}") for k, c in enumerate(TYPES)]
    h0, l0 = ax.get_legend_handles_labels()
    ax.legend(handles + h0, [h.get_label() for h in handles] + l0, fontsize=6.6, loc="lower left", frameon=False, ncol=2,
              columnspacing=1.0)
    # (2) cost split of the set
    ax = axes[1]
    A = res["aggregates"][f"{SET}|investment"]
    parts = [("theta_tot", "compensation", cat[0]), ("cfc_tot", "consumption of fixed capital", cat[1]),
             ("tax_tot", "taxes on production less subsidies", cat[3]), ("nos_tot", "net operating surplus", cat[6])]
    bottom = np.zeros(len(yrs))
    for key, lab, col in parts:
        v = np.array([A[str(y)][key] for y in yrs])
        ax.bar(yrs, v, bottom=bottom, color=col, width=0.8, label=lab, edgecolor="white", linewidth=0.6)
        bottom += v
    ax.set_ylim(0, 1.13)
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.set_ylabel("share of $1 of the set's final output")
    ax.set_title(f"Cost split of the {SET_LABEL} (tot)", loc="left", fontsize=9.2, color=ink)
    ci = res["cfc_cap_and_fallback"][SET]["industries"]
    y5415 = ci["5415"]["capped_years"] + ci["5415"]["fallback_years"]
    ax.plot([min(y5415) - 0.4, max(y5415) + 0.4], [1.02, 1.02], color=muted, lw=0.8)
    ax.annotate(f"CFC/GOS capped at 1:\n5415 {spans(ci['5415']['capped_years'])}\n(fallback {spans(ci['5415']['fallback_years'])})",
                (min(y5415) - 0.4, 1.035), fontsize=6.8, color=muted, ha="left", va="bottom")
    y334 = [y for y in ci["334"]["capped_years"] if y > max(y5415)]          # 334's later run; its early years sit under 5415's
    ax.plot([min(y334) - 0.4, max(y334) + 0.4], [1.02, 1.02], color=muted, lw=0.8)
    ax.annotate(f"334 {spans(y334)}\n(also {spans([y for y in ci['334']['capped_years'] if y <= max(y5415)])})",
                (max(y334) + 0.4, 1.035), fontsize=6.8, color=muted, ha="right", va="bottom")
    ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=2, frameon=False)
    ax.grid(axis="y", color=grid, lw=0.8)
    # (3) per-income bars, 2023: every bar labelled directly above itself
    ax = axes[2]
    P = res["per_income"]["2023"]["rows"][f"{SET}|investment|tot"]
    x = np.arange(len(PCTS))
    bw = 0.26
    top = 0.0
    for k, (basis, lab, col) in enumerate([("asset", "asset basis", cat[0]),
                                           (SVC, f"service flow, rho {RHO_C} ((b)'s)", cat[2]),
                                           (SVT, "service flow, traced", cat[6])]):
        v = [P[basis]["central_relative_hours_worked"][p] for p in PCTS]
        ax.bar(x + (k - 1) * bw, v, width=bw - 0.03, color=col, label=lab)
        for xi, vi in zip(x, v):
            ax.annotate(f"{vi:.2f}", (xi + (k - 1) * bw, vi), xytext=(0, 2), textcoords="offset points", ha="center",
                        va="bottom", rotation=90, fontsize=6.6, color=ink, fontweight="bold" if k == 1 else "normal")
        top = max(top, max(v))
    ax.set_ylim(0, top * 1.22)
    ax.set_xticks(x, PCTS)
    ax.set_ylabel("chain hours per hour replaced")
    ax.set_title(f"Chain hours per hour replaced, 2023\n({SET_LABEL.split(' (')[0]})", loc="left", fontsize=10, color=ink)
    ax.set_xlabel("OEWS all-occupations percentile\n(relative basis, bridged to hours worked)", fontsize=7.5, color=muted)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.grid(axis="y", color=grid, lw=0.8)
    fig.suptitle("The machine chain in the data: BEA I-O 1997-2023, investment weights (equipment + IPP), "
                 "Fixed Assets depreciation, OEWS all-occupation percentiles", fontsize=10, color=muted, x=0.01, ha="left")
    fig.tight_layout()
    p = os.path.join(ROOT, "figures", "fig_chains.png")
    fig.savefig(p, dpi=150, facecolor="white")
    print(p)


if __name__ == "__main__":
    if "--pull" in sys.argv[1:]:
        for n_ in URLS:
            print(pull(n_))
    else:
        main()
