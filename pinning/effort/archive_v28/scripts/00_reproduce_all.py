#!/usr/bin/env python3
from pathlib import Path
import runpy, shutil
ROOT=Path(__file__).resolve().parents[1]; out=ROOT/"outputs_reproduced"
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True)
for s in ["01a_build_C27_from_archived_bea_snapshot.py","01b_build_C28_and_C1.py","02_build_DQ_longrun.py","03_build_S1_from_owner_stock_snapshot.py","04_build_DF_final.py","05_build_DFQ_synthesis.py"]:
    print("RUN",s); runpy.run_path(str(ROOT/"scripts"/s),run_name="__main__")
print("DONE")
