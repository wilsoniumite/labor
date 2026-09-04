#!/usr/bin/env python3
from pathlib import Path
import csv, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/"outputs_reproduced"
rows=[]
with open(ROOT/"inputs/scarcity/owner_housing_stock_source_snapshot_1945_2025.csv",newline="",encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        mv=float(r["owner_occupied_real_estate_market_value_b"]); st=float(r["owner_occupied_residential_structures_current_cost_b"]); land=mv-st
        rows.append({"year":int(r["year"]),"owner_occupied_real_estate_market_value_b":mv,"owner_occupied_residential_structures_current_cost_b":st,"land_site_residual_b":land,"land_site_residual_share_property_value":land/mv if mv else "","structure_share_property_value":st/mv if mv else ""})
with open(O/"graph_D2_owner_occupied_land_residual_1945_2025_minimal.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
rr=[r for r in rows if 1950<=r["year"]<=2025]
fig,ax=plt.subplots(figsize=(12,6.2)); ax.plot([r["year"] for r in rr],[100*r["land_site_residual_share_property_value"] for r in rr],linewidth=2.5)
ax.set_xlim(1950,2025); ax.set_xlabel("Year"); ax.set_ylabel("Land/site residual share of owner property value (%)")
ax.set_title("Owner housing scarcity evidence: land/site is a much larger share of property value than in the early postwar period"); ax.grid(True,alpha=.25)
fig.tight_layout(); fig.savefig(O/"FIG_S1_owner_land_stock_share_1950_2025.png",dpi=240,bbox_inches="tight"); plt.close(fig)
