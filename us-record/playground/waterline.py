# waterline.py — does the untargeted waterline (the wage against machine cost at the margin, 1999 = 1, wc_median) tell
# the clock paces on the ridge apart? The model's counterpart is gamma(x*), the machine service needed at the margin.
import json, sys
import numpy as np
sys.path.insert(0, "code")
import fit_base as F
R = json.load(open("results/fit_capbasket_pin.json"))
F.CAP, F.SIGMA, F.PIN_START, F.UTILITY_KNOTS = R["meta"]["cap"], R["meta"]["sigma"], True, [1950, 1970]
wc = F.PANEL["wc_median"]
data = np.log(wc.loc[2023] / wc.loc[1999])
print(f"record: the waterline 1999 -> 2023, log change {data:+.3f} ({np.exp(data):.2f}x)")
runs = [("kept (clock 11.3%)", R["best"]["par"])]
prof = json.load(open("playground/profiles.json"))
for row in prof["clock pace, falling"] + prof["clock pace, rising"]:
    if row.get("misfit") is not None and row["v"] in (0.08, 0.10, 0.12, 0.14):
        runs.append((f"clock fixed at {row['v'] * 100:.0f}% (misfit {row['misfit']:.2f})", row["par"]))
for label, par in runs:
    m = F.model_path(par)
    g = m["gamma"]
    eta = np.exp(-par["g_eta"] * (np.array(F.YEARS) - 1950.0))
    w = g / eta                                           # the margin in capability units: g0 + g1 x*^k
    print(f"{label:34s} gamma(x*) {np.log(g.loc[2023] / g.loc[1999]):+.3f};  gamma(x*)/eta {np.log(w.loc[2023] / w.loc[1999]):+.3f}")
