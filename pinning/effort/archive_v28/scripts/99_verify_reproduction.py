#!/usr/bin/env python3
from pathlib import Path
import csv, math, sys
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/"outputs_reproduced"; E=ROOT/"expected"
def rcsv(p):
    with open(p,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def cmp(a,b,key,tol,fields=None):
    A=rcsv(a); B=rcsv(b)
    if len(A)!=len(B): return False,f"row count {len(A)} vs {len(B)}"
    bm={r[key]:r for r in B}; mx=0.0
    for r in A:
        q=bm.get(r[key])
        if q is None:return False,f"missing key {r[key]}"
        ff=fields or [k for k in r if k in q and k!=key]
        for k in ff:
            try:x=float(r[k]);y=float(q[k])
            except Exception:continue
            if math.isfinite(x) and math.isfinite(y):mx=max(mx,abs(x-y))
    return mx<=tol,f"max abs numeric error {mx}"
checks=[
("C28",R/"graph_C28_broad_product_families_1950_2025.csv",E/"graph_C28_broad_product_families_1950_2025.csv","year",1e-9,None),
("DQ",R/"LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv",E/"LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv","year",1e-9,None),
("S1",R/"graph_D2_owner_occupied_land_residual_1945_2025_minimal.csv",E/"graph_D2_owner_occupied_land_residual_1945_2025.csv","year",1e-9,["owner_occupied_real_estate_market_value_b","owner_occupied_residential_structures_current_cost_b","land_site_residual_b","land_site_residual_share_property_value","structure_share_property_value"]),
("DF19",R/"DF19_FINAL_modern_DF_panel_2004_2023.csv",E/"DF19_FINAL_modern_DF_panel_2004_2023.csv","year",1e-8,["pce_b","dpi_b","hard_minimum_intertemporal_share_pce","labor_financing_source_free_lower_share_pce","labor_financing_source_free_upper_share_pce","labor_financing_proportional_tax_lower_share_pce","labor_financing_proportional_tax_upper_share_pce","labor_financing_weak_central_share_pce","net_personal_selfemp_social_contrib_b","personal_current_taxes_b"]),
("DF21",R/"DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv",E/"DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv","year",1e-8,["labor_origin_financing_central","lower","upper"])]
ok=True
for name,a,b,key,tol,fields in checks:
    good,msg=cmp(a,b,key,tol,fields); print(("PASS" if good else "FAIL"),name,msg); ok &= good
sys.exit(0 if ok else 1)
