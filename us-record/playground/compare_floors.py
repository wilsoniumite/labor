# compare_floors.py — the rent-floor trade-off, one good against two (durables apart): at each floor under fixed rents'
# share of a machine's cost (1997-2023), the best fit's misfit on the original five targets (and, for two goods, the
# durables wage). Reads playground/rent_floor.json and rent_floor_Bd.json; prints a table.
# Run from us-record/:  python3 playground/compare_floors.py
import json

import numpy as np

FIVE = ["wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"]


def best_by_floor(path):
    rows = [r for r in json.load(open(path)) if r.get("misfit5") is not None]
    out = {}
    for r in rows:
        ok = r["sigma_min_1997_2023"] >= r["floor"] - 0.005           # the floor held
        key = r["floor"]
        if ok and (key not in out or r["misfit5"] < out[key]["misfit5"]):
            out[key] = r
    return out


one, two = best_by_floor("playground/rent_floor.json"), best_by_floor("playground/rent_floor_Bd.json")
main1 = json.load(open("results/fit_Bw.json"))["best"]["by_series"]
main2 = json.load(open("results/fit_Bd.json"))["best"]["by_series"]
print(f"{'floor':>6} | {'one good: five':>15} | {'two goods: five':>16} {'durables wage':>14} {'all six':>8}")
print(f"{'none':>6} | {np.mean([main1[s] for s in FIVE]):15.2f} | {np.mean([main2[s] for s in FIVE]):16.2f} "
      f"{main2['wage_durables']:14.2f} {np.mean(list(main2.values())):8.2f}")
for f in sorted(set(one) | set(two)):
    a = np.mean([one[f]["by"][s] for s in FIVE]) if f in one else np.nan
    b = two.get(f)
    print(f"{100 * f:5.1f}% | {a:15.2f} | " + (f"{np.mean([b['by'][s] for s in FIVE]):16.2f} {b['by']['wage_durables']:14.2f} "
                                              f"{b['misfit5']:8.2f}" if b else "    (no fit held the floor)"))
