# s08_older.py — the net-long logic at 55-64 by sex: participation on q x outright owners 55-64 (country trends).
# Out: s08_older.txt
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402
df = cm.panel(); cl = cm.data.panel()[1]
O = cl["owner_outright_5564"]; O = (O - O.mean()) / O.std(ddof=0)
df["QxO"] = df["logq_l1"].to_numpy() * df.index.get_level_values(0).map(O).to_numpy(float)
out = []
for y in ("AF5564", "AM5564"):
    r = cm.reg(df, y, ["QxO", "logq_l1"], ["U_lfs"], side=-1, trends=True, label=f"{y} on q x O55-64, trends, U_lfs")
    out.append(cm.fmt(r)); print(out[-1])
open(os.path.join(cm.HERE, "s08_older.txt"), "w").write("\n".join(out) + "\n")
