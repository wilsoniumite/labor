#!/usr/bin/env python3
from pathlib import Path
import csv, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/"outputs_reproduced"
def rcsv(p):
    with open(p,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
df={int(r["year"]):r for r in rcsv(O/"DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv")}; modern={int(r["year"]):r for r in rcsv(O/"DF19_FINAL_modern_DF_panel_2004_2023.csv")}; dq={int(r["year"]):r for r in rcsv(O/"LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv")}
yrs=np.arange(1950,2026); dc=np.array([100*float(df[y]["labor_origin_financing_central"]) for y in yrs]); my=np.arange(2004,2024); dlo=np.array([100*float(modern[y]["labor_financing_source_free_lower_share_pce"]) for y in my]); dhi=np.array([100*float(modern[y]["labor_financing_source_free_upper_share_pce"]) for y in my]); qc=np.array([100*float(dq[y]["human_effort_share_headline"]) for y in yrs]); qlo=np.array([100*float(dq[y]["human_effort_weak_lower"]) for y in yrs]); qhi=np.array([100*float(dq[y]["human_effort_weak_upper"]) for y in yrs])
fig,ax=plt.subplots(figsize=(12.2,6.6)); ax.fill_between(my,dlo,dhi,alpha=.11,label="D-F partial-identification interval"); ax.fill_between(yrs,qlo,qhi,alpha=.09,label="D-Q weak-extension band")
pre=yrs<=2004; mid=(yrs>=2004)&(yrs<=2023); post=yrs>=2023; qpre=yrs<=1997; qs=(yrs>=1997)&(yrs<=2023); qpost=yrs>=2023
ax.plot(yrs[pre],dc[pre],linestyle="--",linewidth=2,label="D-F financing — weak extension"); ax.plot(yrs[mid],dc[mid],linewidth=2.5,label="D-F financing — annual source profiles"); ax.plot(yrs[post],dc[post],linestyle="--",linewidth=2)
ax.plot(yrs[qpre],qc[qpre],linestyle="--",linewidth=2,label="D-Q production labor — weak extension"); ax.plot(yrs[qs],qc[qs],linewidth=2.7,label="D-Q production labor — BEA full-chain benchmark"); ax.plot(yrs[qpost],qc[qpost],linestyle="--",linewidth=2)
ax.set_xlim(1950,2025); ax.set_ylim(35,100); ax.set_xlabel("Year"); ax.set_ylabel("Percent of PCE"); ax.set_title("Financing origin and production content are different labor linkages"); ax.grid(True,alpha=.25); ax.legend(frameon=False,fontsize=8.2,loc="upper right")
fig.tight_layout(); fig.savefig(O/"FIG_DFQ_FINAL_financing_vs_production_1950_2025.png",dpi=250,bbox_inches="tight"); plt.close(fig)
