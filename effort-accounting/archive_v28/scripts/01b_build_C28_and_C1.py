#!/usr/bin/env python3
from pathlib import Path
import csv, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/"outputs_reproduced"
inp=O/"graph_C27_detailed_major_product_spine_1950_2025.csv"; out=O/"graph_C28_broad_product_families_1950_2025.csv"
rows=[]
with open(inp,newline="",encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        y=int(r["year"]); p=float(r["pce_b"])
        vals={
          "durable_goods_b":sum(float(r[c]) for c in ["DMOTRC","DFDHRC","DREQRC","DODGRC"]),
          "food_beverages_off_premises_b":float(r["DFXARC"]),
          "clothing_footwear_b":float(r["DCLORC"]),
          "gasoline_other_energy_goods_b":float(r["DGOERC"]),
          "other_nondurable_goods_b":float(r["DONGRC"]),
          "housing_utilities_b":float(r["DHUTRC"]),
          "health_care_b":float(r["DHLCRC"]),
          "financial_services_insurance_b":float(r["DIFSRC"]),
          "other_household_services_b":sum(float(r[c]) for c in ["DTRSRC","DRCARC","DFSARC","DOTSRC"]),
          "npish_final_consumption_b":float(r["DNPIRC"])}
        o={"year":y,"pce_b":p}
        for k,v in vals.items():
            o[k]=v; o[k[:-2]+"_share_pce"]=v/p
        o["sum_b"]=sum(vals.values()); o["identity_residual_b"]=p-o["sum_b"]; rows.append(o)
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
years=np.array([r["year"] for r in rows])
goods=np.array([100*(r["durable_goods_share_pce"]+r["food_beverages_off_premises_share_pce"]+r["clothing_footwear_share_pce"]+r["gasoline_other_energy_goods_share_pce"]+r["other_nondurable_goods_share_pce"]) for r in rows])
stack=[goods,
 np.array([100*r["housing_utilities_share_pce"] for r in rows]),
 np.array([100*r["health_care_share_pce"] for r in rows]),
 np.array([100*r["financial_services_insurance_share_pce"] for r in rows]),
 np.array([100*r["other_household_services_share_pce"] for r in rows]),
 np.array([100*r["npish_final_consumption_share_pce"] for r in rows])]
fig,ax=plt.subplots(figsize=(12.2,6.7)); ax.stackplot(years,*stack,labels=["Goods","Housing & utilities","Health care","Financial services & insurance","Other household services","NPISH"])
ax.set_xlim(1950,2025); ax.set_ylim(0,100); ax.set_xlabel("Year"); ax.set_ylabel("Percent of PCE")
ax.set_title("What households consume: the PCE mix has shifted from goods toward housing, health, and services")
ax.grid(axis="y",alpha=.25); ax.legend(loc="lower left",ncol=2,frameon=False,fontsize=8.5)
fig.tight_layout(); fig.savefig(O/"FIG_C1_PCE_product_composition_1950_2025.png",dpi=240,bbox_inches="tight"); plt.close(fig)
