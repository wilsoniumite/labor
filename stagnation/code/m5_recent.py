# m5_recent.py — M5 of docs/spec.md: 2019 onward, from the dated FRED pull (code/fred.py).
# Output per hour (OPHNFB), hours per person 16 and over (HOANBS over CNP16OV), and a compression index: average
# hourly earnings of production and nonsupervisory employees over those of all employees (AHETPI / CES0500000003, the
# latter from 2006). Annual averages (code/m1_eras.py; 2025 over the 11 months the household survey published).
# As frozen: counts against the account if output per hour grew faster with rising hours per person and no compression.
# The plan stated no prediction for these years (the pickup in output per hour was known when it was written);
# `opposite_combination` records whether the opposite of the counting-against combination occurred, the pattern
# Proposition 1 gives when hours leave work.
# Writes data/m5_recent.json.
# Run from stagnation/:  ../venv/bin/python code/m5_recent.py
import json
from pathlib import Path

import numpy as np
import pandas as pd

import m1_eras

ROOT = Path(__file__).resolve().parents[1]


def rate(s, y0, y1):
    return 100 * (np.log(s[y1]) - np.log(s[y0])) / (y1 - y0)


def run():
    a = pd.DataFrame({s: m1_eras.annual(s) for s in ("OPHNFB", "HOANBS", "CNP16OV", "AHETPI", "CES0500000003")})
    hpp = a.HOANBS / a.CNP16OV
    comp = a.AHETPI / a.CES0500000003
    q = m1_eras.fred.fetch("OPHNFB")
    q19, qlast = q[q.index == "2019-10-01"].iloc[0], q.iloc[-1]
    years_q = (q.index[-1] - pd.Timestamp("2019-10-01")).days / 365.25
    out = dict(
        productivity_2004_2019=rate(a.OPHNFB, 2004, 2019), productivity_2019_2025=rate(a.OPHNFB, 2019, 2025),
        productivity_q4_2019_to_last=100 * np.log(qlast / q19) / years_q, last_quarter=str(q.index[-1].date()),
        hours_pp_2004_2019=rate(hpp, 2004, 2019), hours_pp_2019_2025=rate(hpp, 2019, 2025),
        compression_2007_2019=rate(comp, 2007, 2019), compression_2019_2025=rate(comp, 2019, 2025),
        compression_level_2019=comp[2019], compression_level_2025=comp[2025],
        compression_pct_2019_2025=100 * (comp[2025] / comp[2019] - 1))
    faster = out["productivity_2019_2025"] > out["productivity_2004_2019"]
    rising_hours = out["hours_pp_2019_2025"] > 0
    compressed = out["compression_2019_2025"] > 0
    out.update(faster=bool(faster), rising_hours=bool(rising_hours), compressed=bool(compressed),
               counts_against=bool(faster and rising_hours and not compressed),
               opposite_combination=bool(faster and not rising_hours and compressed))
    return out


if __name__ == "__main__":
    out = run()
    (ROOT / "data" / "m5_recent.json").write_text(json.dumps(out, indent=2, default=float))
    for k, v in out.items():
        print(f"  {k:32s} {v:.3f}" if isinstance(v, float) else f"  {k:32s} {v}")
