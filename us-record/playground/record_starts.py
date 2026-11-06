# record_starts.py — a flight lead (2026-11-06): record_case.py found that none of the calibrated 1950 starts reach an
# equilibrium path under D2's settings (the rent 0.20, the return 8%, land growing with adults): they are calibrated with
# fixed rents all land (0.30) and their own return. Here each is moved first, as record_case.moved does: a and lam0
# scaled by the ratio of (rho + delta) in 1950, a lowered by the rent / (rho + delta), so that 1950's distance to the
# chain's ceiling is about kept. Then fitted with the wave and without it. Does anything fit better than D2's 1.536?
# Writes playground/record_starts.json.   Run from us-record/:  python3 playground/record_starts.py
import json
import sys
from multiprocessing import Pool

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import record_case as RC  # noqa: E402  (BASE, NOWAVE, fit; sets land in use growing with adults)


def moved(s, rho, phi):
    p = dict(s)
    old, new = p["rho"] + F.DELTA[0], rho + F.DELTA[0]
    p["a"] = max(0.011, (p["a"] * old - phi) / new)
    p["lam0"] = p["lam0"] * old / new
    p["rho"] = rho
    return p


if __name__ == "__main__":
    F.configure(RC.BASE)
    cal = F.starts()
    phi, rho = RC.S["phi"], RC.S["rho"]
    jobs = [("starts", RC.BASE, moved(s, rho, phi), f"calibrated 1950 start {i + 1}, moved") for i, s in enumerate(cal)]
    jobs += [("wave", RC.NOWAVE, moved(s, rho, phi), f"calibrated 1950 start {i + 1}, moved, no wave") for i, s in enumerate(cal)]
    with Pool(4) as pool:
        out = pool.map(RC.fit, jobs)
    json.dump(dict(fits=out), open("playground/record_starts.json", "w"), indent=1)
    for group in ("starts", "wave"):
        rows = sorted([r for r in out if r["group"] == group], key=lambda r: r["misfit"])
        ok = [r for r in rows if r["misfit"] < 10]
        print(f"{group}: {len(ok)} of {len(rows)} reach an equilibrium path: " + ", ".join(f"{r['misfit']:.3f}" for r in ok))
        for r in ok[:2]:
            p = r["par"]
            print(f"   {r['label']}: return {p['rho']:.2f} clock {100 * p['g_eta']:.1f}% hours/task {100 * (p['g_lam'] - p['g_eta']):.2f}%"
                  f" durables {100 * p['g_dur']:.1f}% wave {p.get('w0_size', 0):.2f} a {p['a']:.2f} k {p['k']:.2f}")
