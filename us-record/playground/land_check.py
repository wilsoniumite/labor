# land_check.py — land in baskets against land in the machines in the kept fit (the Python model, stored parameters).
import json, sys
sys.path.insert(0, "code")
import fit_base as F
R = json.load(open("results/fit_capbasket_pin.json"))
F.CAP, F.SIGMA, F.PIN_START, F.UTILITY_KNOTS = R["meta"]["cap"], R["meta"]["sigma"], True, [1950, 1970]
par = dict(R["best"]["par"])
p_ref = F.pm.solve(F.economies(par)[0])["p"]
es = F.economies(par, p_ref=p_ref)
for i, y in ((0, 1950), (20, 1970), (50, 2000), (74, 2024)):
    e = es[i]
    q = F.pm.solve(e)
    lb = q["site_basket"] * q["baskets"]
    print(y, f"land in baskets {lb / e.T:.4f} of all land, in machines {e.b * e.delta * q['K'] / e.T:.4f}; "
             f"site rent's share of income {lb / q['income']:.2e}; machines' land rent share {e.b * e.delta * q['K'] / q['income']:.3f}")
