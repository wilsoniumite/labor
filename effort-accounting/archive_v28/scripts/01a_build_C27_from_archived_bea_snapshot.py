#!/usr/bin/env python3
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
inp=ROOT/"inputs/c1/BEA_Table2_3_5_leaf_value_snapshot_1950_2025.csv"
out=ROOT/"outputs_reproduced/graph_C27_detailed_major_product_spine_1950_2025.csv"
codes=["DMOTRC","DFDHRC","DREQRC","DODGRC","DFXARC","DCLORC","DGOERC","DONGRC","DHUTRC","DHLCRC","DTRSRC","DRCARC","DFSARC","DIFSRC","DOTSRC","DNPIRC"]
rows=[]
with open(inp,newline="",encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        p=float(r["pce_b"]); o={"year":int(r["year"]),"pce_b":p}; total=0.0
        for c in codes:
            v=float(r[c]); total+=v; o[c]=v; o[c+"_share_pce"]=v/p
        o["detail_sum_b"]=total; o["identity_residual_b"]=p-total; o["source_vintage"]=r["source_vintage"]; rows.append(o)
out.parent.mkdir(parents=True,exist_ok=True)
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
