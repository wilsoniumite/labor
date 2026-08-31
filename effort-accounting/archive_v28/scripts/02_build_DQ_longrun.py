#!/usr/bin/env python3
from pathlib import Path
import csv, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/"outputs_reproduced"
def rcsv(p):
    with open(p,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
c28={int(r["year"]):r for r in rcsv(O/"graph_C28_broad_product_families_1950_2025.csv")}
full={int(r["year"]):r for r in rcsv(ROOT/"inputs/dq/D_Q11_bea_wp2026_fullchain_consumption_grouped_1997_2023_digitized.csv")}
def feat(y):
    r=c28[y]; d={"housing":float(r["housing_utilities_share_pce"]),"health":float(r["health_care_share_pce"]),"finance":float(r["financial_services_insurance_share_pce"]),"otherserv":float(r["other_household_services_share_pce"]),"npish":float(r["npish_final_consumption_share_pce"]),"durable":float(r["durable_goods_share_pce"]),"food":float(r["food_beverages_off_premises_share_pce"]),"clothing":float(r["clothing_footwear_share_pce"]),"energygoods":float(r["gasoline_other_energy_goods_share_pce"]),"othernd":float(r["other_nondurable_goods_share_pce"])}
    d["goods"]=d["durable"]+d["food"]+d["clothing"]+d["energygoods"]+d["othernd"]; return d
specs=[("H-H-F-G",["housing","health","finance","goods"]),("H-H-G",["housing","health","goods"]),("H-F-G",["health","finance","goods"]),("H-H-F-S",["housing","health","finance","otherserv"]),("H-H-G-N",["housing","health","goods","npish"])]
ys=sorted(full); yl=np.array([float(full[y]["human_effort_share"]) for y in ys]); yf=np.array([float(full[y]["foreign_content_share"]) for y in ys]); models=[]
for name,spec in specs:
    X=np.array([[1.0]+[feat(y)[k] for k in spec] for y in ys]); bl=np.linalg.lstsq(X,yl,rcond=None)[0]; bf=np.linalg.lstsq(X,yf,rcond=None)[0]
    models.append((name,spec,bl,bf,float(np.sqrt(np.mean((X@bl-yl)**2))),float(np.sqrt(np.mean((X@bf-yf)**2)))))
rows=[]
for y in range(1950,2026):
    lp=[]; fp=[]
    for _,spec,bl,bf,_,_ in models:
        x=np.array([1.0]+[feat(y)[k] for k in spec]); lp.append(float(x@bl)); fp.append(float(x@bf))
    arl=float(np.mean([m[4] for m in models])); arf=float(np.mean([m[5] for m in models])); lc=float(np.mean(lp)); fc=float(np.mean(fp))
    llo=max(0,min(lp)-arl); lhi=min(1,max(lp)+arl); flo=max(0,min(fp)-arf); fhi=min(1,max(fp)+arf); strong=y in full
    if strong: lab=float(full[y]["human_effort_share"]); foreign=float(full[y]["foreign_content_share"]); capital=float(full[y]["domestic_capital_total_share"])
    else: lab=lc; foreign=fc; capital=1-lab-foreign
    rows.append({"year":y,"evidence_tier":"STRONG" if strong else "WEAK","human_effort_share_headline":lab,"human_effort_weak_central":lc,"human_effort_weak_lower":llo,"human_effort_weak_upper":lhi,"foreign_content_share_headline":foreign,"foreign_content_weak_central":fc,"foreign_content_weak_lower":flo,"foreign_content_weak_upper":fhi,"domestic_capital_share_headline":capital,"domestic_capital_weak_lower":max(0,1-lhi-fhi),"domestic_capital_weak_upper":min(1,1-llo-flo),"strong_source_note":"BEA WP2026-01 Figure 9 grouped annual benchmark, digitized and validated to published means." if strong else "","weak_method_note":"Ensemble of five OLS product-composition specifications estimated only on 1997–2023; current NIPA product shares are observed for all years." if not strong else ""})
with open(O/"LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
yrs=np.array([r["year"] for r in rows]); lo=np.array([100*r["human_effort_weak_lower"] for r in rows]); hi=np.array([100*r["human_effort_weak_upper"] for r in rows])
fig,ax=plt.subplots(figsize=(12.2,6.4)); ax.fill_between(yrs,lo,hi,alpha=.18,label="Weak extension band")
pre=[r for r in rows if r["year"]<=1997]; st=[r for r in rows if 1997<=r["year"]<=2023]; post=[r for r in rows if r["year"]>=2023]
ax.plot([r["year"] for r in pre],[100*r["human_effort_weak_central"] for r in pre],linestyle="--",linewidth=2,label="Weak compositional extension")
ax.plot([r["year"] for r in st],[100*r["human_effort_share_headline"] for r in st],linewidth=2.6,label="BEA full-chain benchmark")
ax.plot([r["year"] for r in post],[100*r["human_effort_weak_central"] for r in post],linestyle="--",linewidth=2)
ax.set_xlim(1950,2025); ax.set_xlabel("Year"); ax.set_ylabel("Human-effort content of PCE (%)")
ax.set_title("Production labor content of consumption: strong benchmark in the middle, weak long-run extension outside"); ax.grid(True,alpha=.25); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(O/"FIG_DQ_human_effort_content_1950_2025.png",dpi=240,bbox_inches="tight"); plt.close(fig)
