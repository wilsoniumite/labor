#!/usr/bin/env python3
from pathlib import Path
import csv, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; I=ROOT/"inputs/df"; O=ROOT/"outputs_reproduced"
def rcsv(p):
    with open(p,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def wcsv(p,rows):
    fields=[]
    for r in rows:
        for k in r:
            if k not in fields: fields.append(k)
    with open(p,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
bea=rcsv(I/"BEA_distribution_summary-file.csv"); legal={int(r["year"]):r for r in rcsv(I/"legal_income_audit_1960_2025.csv")}; b0={int(r["year"]):r for r in rcsv(I/"graph_B0_disposable_income_disposition_1960_2025.csv")}; df9={int(r["year"]):r for r in rcsv(I/"DF9_current_resource_origin_strong_weak_1950_2025.csv")}; df10={int(r["year"]):r for r in rcsv(I/"DF10_full_pce_financing_ledger_strong_weak_1950_2025.csv")}; joint_all=rcsv(I/"bea_sharp_intertemporal_bound_decile_2000_2023.csv"); controls={int(r["year"]):r for r in rcsv(I/"annual_national_deduction_controls_2004_2025.csv")}
RANK="Equivalized Disposable Personal Income"; deciles=[f"{i*10}-{(i+1)*10}%" for i in range(10)]
concepts={"comp":"Compensation of employees","prop":"Proprietors' income with inventory valuation","rent":"Rental income of households with capital consumption adjustment","interest":"Household interest income","dividends":"Household dividend income","transfers":"Government social benefits","contrib":"Contributions for government social insurance, domestic","taxes":"Taxes"}
def profile(y,c):
    d={r["Quantile or Summary Metric"]:float(r["Value"]) for r in bea if r["Year"]==str(y) and r["Ranking"]==RANK and r["Income Concept"]==c and r["Quantile or Summary Metric"] in deciles}
    a=np.array([d[q] for q in deciles]); return a/a.sum()
annual=[]
for y in range(2004,2024):
    lr=legal[y]; orow=df9[y]; dpi=float(b0[y]["dpi"]); pce=float(b0[y]["pce"]); prop_eff=float(orow["proprietor_effort_share_mid"]); transfer_wage=float(orow["transfer_wage_exposure_mid"])
    joint=[r for r in joint_all if int(r["Year"])==y]; joint.sort(key=lambda r:deciles.index(r["decile"]))
    dsh=np.array([float(r["dpi_share"]) for r in joint]); dsh/=dsh.sum(); psh=np.array([float(r["pce_share"]) for r in joint]); psh/=psh.sum(); D=dpi*dsh; P=pce*psh; C=np.minimum(D,P)
    emp=float(lr["employee_comp"])*profile(y,concepts["comp"]); prop=float(lr["proprietors"])*profile(y,concepts["prop"]); rent=float(lr["rental"])*profile(y,concepts["rent"]); intr=float(lr["interest"])*profile(y,concepts["interest"]); div=float(lr["dividends"])*profile(y,concepts["dividends"]); trans=float(lr["transfers"])*profile(y,concepts["transfers"])
    cc=controls[y]; a061=float(cc["A061_total_domestic_gov_social_contrib_b"]); b039=float(cc["B039_employer_gov_social_contrib_b"]); taxes=float(cc["W055_personal_current_taxes_b"])
    social=a061*profile(y,concepts["contrib"])-b039*profile(y,concepts["comp"]); tax=taxes*profile(y,concepts["taxes"])
    labor_gross=emp+prop*prop_eff+trans*transfer_wage; nonlabor_gross=prop*(1-prop_eff)+rent+intr+div+trans*(1-transfer_wage); labor_after=np.maximum(0,labor_gross-social)
    labor_net_min=np.maximum(0,labor_after-tax); labor_net_max=labor_after-np.maximum(0,tax-nonlabor_gross); net=np.maximum(1e-12,labor_after+nonlabor_gross-tax)
    llo=np.minimum(np.clip(labor_net_min/net,0,1),np.clip(labor_net_max/net,0,1)); lhi=np.maximum(np.clip(labor_net_min/net,0,1),np.clip(labor_net_max/net,0,1)); pre=np.maximum(1e-12,labor_after+nonlabor_gross); lprop=labor_after/pre
    spend_lo=np.maximum(0,C-D*(1-llo)); spend_hi=np.minimum(C,D*lhi)
    annual.append({"year":y,"panel_tier":"STRONG_ANNUAL_DPI_RANKED_SOURCE_PROFILES__PARTIAL_IDENTIFICATION","pce_b":pce,"dpi_b":dpi,"hard_minimum_intertemporal_share_pce":float(np.sum(np.maximum(0,P-D))/pce),"labor_financing_source_free_lower_share_pce":float(spend_lo.sum()/pce),"labor_financing_source_free_upper_share_pce":float(spend_hi.sum()/pce),"labor_financing_proportional_tax_lower_share_pce":float(np.maximum(0,C-D*(1-lprop)).sum()/pce),"labor_financing_proportional_tax_upper_share_pce":float(np.minimum(C,D*lprop).sum()/pce),"labor_financing_weak_central_share_pce":float(np.sum(C*lprop)/pce),"net_personal_selfemp_social_contrib_b":float(social.sum()),"personal_current_taxes_b":taxes,"source_profile_status":"ACTUAL ANNUAL BEA DPI-RANKED PROFILE","remaining_weakness":"Proprietor labor split, transfer funding look-through, personal-tax source incidence, and within-decile spending-source fungibility."})
wcsv(O/"DF19_FINAL_modern_DF_panel_2004_2023.csv",annual)
modern={r["year"]:r for r in annual}; long=[]
for y in range(1950,2026):
    if y in modern:
        r=modern[y]; c=r["labor_financing_weak_central_share_pce"]; lo=r["labor_financing_source_free_lower_share_pce"]; hi=r["labor_financing_source_free_upper_share_pce"]; tier="STRONG_ANNUAL_SOURCE_PROFILES__PARTIAL_ID"
    else:
        r=df10[y]; c=float(r["current_labor_origin_share_pce_central"]); lo=float(r["labor_financing_capacity_lower_share_pce"]); hi=float(r["labor_financing_capacity_upper_share_pce"]); tier="WEAK_LONGRUN_EXTENSION"
    long.append({"year":y,"labor_origin_financing_central":c,"lower":lo,"upper":hi,"tier":tier,"note":"2004–2023 uses actual annual BEA DPI-ranked source profiles. Outer years use the earlier aggregate strong/weak extension."})
wcsv(O/"DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv",long)
yrs=np.array([r["year"] for r in long]); cen=np.array([100*r["labor_origin_financing_central"] for r in long]); my=np.arange(2004,2024); lo=np.array([100*modern[y]["labor_financing_source_free_lower_share_pce"] for y in my]); hi=np.array([100*modern[y]["labor_financing_source_free_upper_share_pce"] for y in my])
fig,ax=plt.subplots(figsize=(12.2,6.5)); ax.fill_between(my,lo,hi,alpha=.16,label="Modern partial-identification interval"); pre=yrs<=2004; mid=(yrs>=2004)&(yrs<=2023); post=yrs>=2023
ax.plot(yrs[pre],cen[pre],linestyle="--",linewidth=2,label="Weak long-run extension"); ax.plot(yrs[mid],cen[mid],linewidth=2.7,label="Annual BEA DPI-ranked source-profile central"); ax.plot(yrs[post],cen[post],linestyle="--",linewidth=2)
ax.set_xlim(1950,2025); ax.set_ylim(40,100); ax.set_xlabel("Year"); ax.set_ylabel("Labor-origin financing share of PCE (%)"); ax.set_title("Labor-origin financing of consumption"); ax.grid(True,alpha=.25); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(O/"FIG_DF_FINAL_labor_origin_financing_1950_2025.png",dpi=250,bbox_inches="tight"); plt.close(fig)
