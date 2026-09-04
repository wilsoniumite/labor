"""
build_fig3_realwage_fan.py — pinning/effort (Figure 3 of the paper)

ADOPTED 2026-09-04 as the paper's Figure 3, written to paper/figures/
fig_deflator_fork.png with no in-figure title (the caption carries it).
The deflator FAN (built first as an exploratory variant, her asks 2026-09-01: "I also would
like to see food and energy deflator lines", then "start the series at
1950... extrapolate a bit back for energy, you can use linear"): the
Figure-3 fork's two legs plus food and energy as real-wage legs, drawn
1950–2024 and indexed 1950 = 100. The adopted figure, the 1950 fork
variant, and their inputs are untouched.

Construction. The wage/durables/shelter members are rebuilt with exactly
the 1950 variant's splice rules (AHETPI+AHEMAN seam 1964; CUSR0000SAD +
quarterly CUUR0000SAD seam 1956; CUSR0000SAH1 + CUUR0000SEHA seam 1953)
and GATED: both legs, rebased to 1950 = 100, must equal the shipped
data/fig3_realwage_fork_1950.csv to 1e-9 in every overlapping year — the
fan inherits every adopted-figure anchor transitively through that file,
and the adopted 2024 anchors are re-checked directly on the internal
1964 base. The two new members:

  food    CPIUFDNS   CPI food NSA, monthly from 1913 — complete
                     1950–2024 coverage, no splice.
  energy  CPIENGNS   CPI energy NSA, monthly from 1957 — the energy
                     aggregate did not exist earlier. 1950–56 is a LINEAR
                     BACK-EXTRAPOLATION of the deflator (her call: "you
                     can use linear"): least squares on the first ten
                     complete years, 1957–66, extended back seven years.
                     Drawn dotted and flagged in the CSV; the leg's
                     1950 = 100 anchor therefore stands on the fit.

Both are pulled live from FRED, vendored to data/raw/ with manifest rows,
and held by frozen sanity bands (guards id drift, set from the 2026-09-01
pull). NOTE: the FRED ids are the mnemonic forms — the BLS-style
CUUR0000SAF1 / CUUR0000SA0E return 404 on fredgraph. Legs are annual
means over complete calendar years (the family rule; 2025 is incomplete
because the October-2025 CPI was never published). Pre-1964 stretches
are dashed: the wage member is spliced there.

Gates: the transitive 1e-9 equality above; the adopted 2024 anchors on
the internal 1964 base; new-member sanity bands; the backcast held to a
band at 1950 and to a ≤5% fit-vs-actual gap at 1957; rebase checks.
Any gate failure stops the build rather than approximating.

Run from the repo root:
    ./venv/Scripts/python.exe pinning/effort/code/build_fig3_realwage_fan.py [--refresh]
"""

import csv
import sys
import urllib.request
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
VARIANT_1950_CSV = ROOT / "data" / "fig3_realwage_fork_1950.csv"
OUT_CSV = ROOT / "data" / "fig3_realwage_fan.csv"
OUT_PNG = ROOT.parent / "paper" / "figures" / "fig_deflator_fork.png"  # the paper's Figure 3

ESTABLISHED = {  # adopted-figure inputs — present from prior builds, never pulled here
    "wage": "AHETPI",
    "durables": "CUSR0000SAD",
    "shelter": "CUSR0000SAH1",
}
LONG = {  # 1950-variant long members — present from its build, never pulled here
    "wage_long": "AHEMAN",
    "durables_long": "CUUR0000SAD",
    "shelter_long": "CUUR0000SEHA",
}
NEW = {  # the fan's additions — pulled here, vendored, manifest rows appended
    "food": "CPIUFDNS",
    "energy": "CPIENGNS",
}
START_YEAR = 1950
BASE_YEAR = 1964                       # internal gate base (the adopted figure's)
OUT_BASE = 1950                        # output index base (her call, 2026-09-01)
WAGE_SEAM, DUR_SEAM, SHEL_SEAM = 1964, 1956, 1953
QUARTER_MONTHS = frozenset(("03", "06", "09", "12"))
E_FIT = (1957, 1966)                   # backcast fit window (first ten complete years)

# Frozen sanity bands for the new members (2026-09-01 pull; guards id drift).
SANITY_NEW = {
    "food": [(1950, 20, 32), (2024, 300, 370)],
    "energy": [(1957, 18, 26), (2024, 240, 330)],
}
# Backcast gates: the fitted 1950 level and the fit's anchoring at 1957.
E_1950_BAND = (17.0, 25.0)
E_FIT_GAP_TOL = 0.05
# The two established legs' adopted anchors, re-checked on the internal base.
FORK_ANCHORS = [
    ("durables leg 2024", 2024, "durables", 376.8, 3.0),
    ("shelter leg 2024", 2024, "shelter", 78.6, 1.5),
]

COLORS = {  # family colors for the established legs; Okabe–Ito for the additions
    "durables": "tab:blue",
    "food": "#E69F00",
    "energy": "#009E73",
    "shelter": "tab:red",
}
LABELS = {
    "durables": "durables CPI (machine-made goods)",
    "food": "food CPI",
    "energy": "energy CPI (1950–56 backcast)",
    "shelter": "shelter CPI (land-priced)",
}


def pull(sid: str) -> None:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
    with urllib.request.urlopen(url, timeout=60) as r:
        (RAW / f"{sid}.csv").write_text(r.read().decode("utf-8"), encoding="utf-8")


def load_monthly(sid: str) -> dict[int, dict[str, float]]:
    out: dict[int, dict[str, float]] = {}
    with open(RAW / f"{sid}.csv", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            val = row[sid]
            if val in ("", "."):
                continue
            out.setdefault(int(row["observation_date"][:4]), {})[row["observation_date"][5:7]] = float(val)
    return out


def annual12(m: dict[int, dict[str, float]]) -> dict[int, float]:
    """Annual means over complete years only (12 monthly observations)."""
    return {y: sum(d.values()) / len(d) for y, d in m.items() if len(d) >= 12}


def annual_quarters(m: dict[int, dict[str, float]]) -> dict[int, float]:
    """Annual means for the quarterly-era years — exactly the four
    quarter-end months present, nothing else masquerading as a year."""
    return {y: sum(d.values()) / 4 for y, d in m.items() if set(d) == QUARTER_MONTHS}


def linear_fit(xs: list[int], ys: list[float]) -> tuple[float, float]:
    """Least-squares slope and intercept (plain formulas, no deps)."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return slope, my - slope * mx


def main() -> int:
    refresh = "--refresh" in sys.argv
    for label, table in (("established", ESTABLISHED), ("1950-variant long", LONG)):
        for concept, sid in table.items():
            if not (RAW / f"{sid}.csv").exists():
                print(f"BLOCKED: {label} raw {sid}.csv missing — run the owning "
                      "build script first (its inputs are not pulled here).")
                return 1

    manifest = []
    for concept, sid in NEW.items():
        if refresh or not (RAW / f"{sid}.csv").exists():
            pull(sid)
            manifest.append({"series": sid, "concept": concept,
                             "url": f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}",
                             "pulled": date.today().isoformat()})
    if manifest:
        mf = RAW / "fig3_pull_manifest.csv"
        rows = list(csv.DictReader(open(mf, encoding="utf-8"))) if mf.exists() else []
        rows.extend(manifest)
        with open(mf, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["series", "concept", "url", "pulled"])
            w.writeheader()
            w.writerows(rows)

    est = {c: annual12(load_monthly(sid)) for c, sid in ESTABLISHED.items()}
    mfg = annual12(load_monthly(LONG["wage_long"]))
    dur_nsa_m = load_monthly(LONG["durables_long"])
    dur_nsa12 = annual12(dur_nsa_m)
    dur_nsa_q = annual_quarters(dur_nsa_m)
    rent = annual12(load_monthly(LONG["shelter_long"]))
    food = annual12(load_monthly(NEW["food"]))
    energy_obs = annual12(load_monthly(NEW["energy"]))

    failures = []
    for concept, anchors in SANITY_NEW.items():
        series = food if concept == "food" else energy_obs
        for y, lo, hi in anchors:
            v = series.get(y)
            if v is None or not (lo <= v <= hi):
                failures.append(f"sanity {concept} {y}={v} not in [{lo},{hi}]")

    # Energy backcast: linear fit on the first ten complete years,
    # extended 1950–56 (her call: linear). Flagged, gated, drawn dotted.
    e_start = min(energy_obs)
    fit_years = [y for y in range(E_FIT[0], E_FIT[1] + 1) if y in energy_obs]
    if e_start > E_FIT[0] or len(fit_years) != E_FIT[1] - E_FIT[0] + 1:
        failures.append(f"energy fit window {E_FIT} incomplete (starts {e_start})")
        energy_x, slope, fit_gap = dict(energy_obs), float("nan"), float("nan")
    else:
        slope, icept = linear_fit(fit_years, [energy_obs[y] for y in fit_years])
        energy_x = {y: slope * y + icept for y in range(START_YEAR, e_start)}
        energy_x.update(energy_obs)
        fit_gap = abs((slope * e_start + icept) - energy_obs[e_start]) / energy_obs[e_start]
        if not (E_1950_BAND[0] <= energy_x[START_YEAR] <= E_1950_BAND[1]):
            failures.append(f"energy backcast 1950={energy_x[START_YEAR]:.2f} "
                            f"not in {E_1950_BAND}")
        if fit_gap > E_FIT_GAP_TOL:
            failures.append(f"energy fit-vs-actual gap at {e_start} {fit_gap:.1%} > "
                            f"{E_FIT_GAP_TOL:.0%}")

    # Extended members: the 1950 variant's splice rules, verbatim.
    wage_x, dur_x, shel_x = dict(est["wage"]), dict(est["durables"]), dict(est["shelter"])
    missing = []
    for y in range(START_YEAR, WAGE_SEAM):
        if y in mfg:
            wage_x[y] = est["wage"][WAGE_SEAM] * mfg[y] / mfg[WAGE_SEAM]
        else:
            missing.append(f"wage_long {y}")
    for y in range(START_YEAR, DUR_SEAM):
        if y in dur_nsa_q:
            dur_x[y] = est["durables"][DUR_SEAM] * dur_nsa_q[y] / dur_nsa12[DUR_SEAM]
        else:
            missing.append(f"durables_long {y}")
    for y in range(START_YEAR, SHEL_SEAM):
        if y in rent:
            shel_x[y] = est["shelter"][SHEL_SEAM] * rent[y] / rent[SHEL_SEAM]
        else:
            missing.append(f"shelter_long {y}")
    for y in range(START_YEAR, 2025):
        if y not in food:
            missing.append(f"food {y}")
        if y not in energy_x:
            missing.append(f"energy {y}")
    if missing:
        failures.append("member years missing: " + ", ".join(missing))

    deflators = {"durables": dur_x, "food": food, "energy": energy_x, "shelter": shel_x}
    years = sorted(y for y in wage_x
                   if START_YEAR <= y and all(y in d for d in deflators.values()))
    legs = {}       # internal 1964 base — everything is gated here
    legs_out = {}   # output 1950 base — a pure rebase of the gated series
    for name, defl in deflators.items():
        real = {y: wage_x[y] / defl[y] for y in years}
        legs[name] = {y: 100 * real[y] / real[BASE_YEAR] for y in years}
        legs_out[name] = {y: 100 * legs[name][y] / legs[name][OUT_BASE] for y in years}
        if abs(legs_out[name][OUT_BASE] - 100) > 1e-9:
            failures.append(f"rebase check: {name} leg at {OUT_BASE} != 100")

    # The adopted anchors on the fan's own build (internal base).
    for name, y, leg, target, tol in FORK_ANCHORS:
        v = legs[leg].get(y)
        if v is None or abs(v - target) > tol:
            failures.append(f"anchor {name}: {v} vs {target}±{tol}")

    # The transitive gate: durables/shelter legs on the output base must
    # equal the shipped 1950-variant CSV to 1e-9 in every overlapping year.
    if not VARIANT_1950_CSV.exists():
        failures.append(f"{VARIANT_1950_CSV.name} missing — the fan is defined relative to it")
    else:
        shipped = {}
        with open(VARIANT_1950_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                shipped[int(row["year"])] = (float(row["real_wage_durables_1950_100"]),
                                             float(row["real_wage_shelter_1950_100"]))
        dev = 0.0
        for y, (d, s) in shipped.items():
            if y not in legs_out["durables"]:
                failures.append(f"variant year {y} missing from the fan build")
                break
            dev = max(dev, abs(legs_out["durables"][y] - d), abs(legs_out["shelter"][y] - s))
        if dev > 1e-9:
            failures.append(f"durables/shelter deviate from the 1950 variant by {dev:.2e} > 1e-9")

    last = years[-1]
    print("=== validation ledger ===")
    print(f"years {years[0]}–{last} | output base {OUT_BASE} = 100 (gates on {BASE_YEAR}) | "
          f"energy observed from {e_start}, backcast {START_YEAR}–{e_start - 1} "
          f"(fit {E_FIT[0]}–{E_FIT[1]}, slope {slope:+.3f}/yr, 1950 level "
          f"{energy_x.get(START_YEAR, float('nan')):.2f}, fit-vs-actual gap at {e_start} {fit_gap:.2%})")
    print(f"internal {BASE_YEAR} base (gates): 2024 legs " +
          " | ".join(f"{n} {legs[n][last]:.1f}" for n in deflators))
    print(f"output {OUT_BASE} base: 2024 legs " +
          " | ".join(f"{n} {legs_out[n][last]:.1f}" for n in deflators))
    print("fork ratios 2024 (1964-window; the window moves with the base): " + " | ".join(
        f"durables/{n} {legs['durables'][last] / legs[n][last]:.2f}x"
        for n in ("food", "energy", "shelter")) +
        f" | food/shelter {legs['food'][last] / legs['shelter'][last]:.2f}x")
    e = legs_out["energy"]
    post = [y for y in e if y >= BASE_YEAR]
    pk, tr = max(post, key=e.get), min(post, key=e.get)
    print(f"energy diagnostics (post-{BASE_YEAR}): peak {e[pk]:.1f} ({pk}), trough "
          f"{e[tr]:.1f} ({tr}), peak/trough {e[pk] / e[tr]:.2f}x | "
          f"1972→1981 {e[1981] / e[1972] - 1:+.0%} | 1981→1998 {e[1998] / e[1981] - 1:+.0%} | "
          f"2020→2022 {e[2022] / e[2020] - 1:+.0%}")
    if failures:
        for msg in failures:
            print("FAIL", msg)
        print("BLOCKED: validation failed — stopping rather than approximating.")
        return 1
    print("all gates PASS")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year"] + [f"real_wage_{n}_1950_100" for n in deflators] + ["energy_member"])
        for y in years:
            w.writerow([y] + [legs_out[n][y] for n in deflators] +
                       ["linear-backcast" if y < e_start else NEW["energy"]])

    fig, ax = plt.subplots(figsize=(12.2, 6.5))
    for name in deflators:
        yrs = sorted(legs_out[name])
        if name == "energy":
            back = [y for y in yrs if y <= e_start]           # dotted: backcast years
            mid = [y for y in yrs if e_start <= y <= BASE_YEAR]
            ax.plot(back, [legs_out[name][y] for y in back], linewidth=2.0,
                    color=COLORS[name], linestyle=":")
            ax.plot(mid, [legs_out[name][y] for y in mid], linewidth=2.0,
                    color=COLORS[name], linestyle="--")
        else:
            pre = [y for y in yrs if y <= BASE_YEAR]
            ax.plot(pre, [legs_out[name][y] for y in pre], linewidth=2.0,
                    color=COLORS[name], linestyle="--")
        post = [y for y in yrs if y >= BASE_YEAR]
        ax.plot(post, [legs_out[name][y] for y in post], linewidth=2.5,
                color=COLORS[name], label=LABELS[name])
        ax.annotate(name, (yrs[-1], legs_out[name][yrs[-1]]), xytext=(6, 0),
                    textcoords="offset points", va="center", fontsize=9,
                    color=COLORS[name])
    ax.axhline(100, color="k", linewidth=0.8, linestyle=":")
    ax.set_xlim(START_YEAR, last + 6)
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Real average hourly earnings, {OUT_BASE} = 100")
    ax.grid(True, alpha=0.25)
    ax.text(0.012, 0.83, "dashed pre-1964: spliced-wage era (members and seams as in the\n"
                         "1950 fork variant); food is CPI food NSA from 1950; the energy\n"
                         "aggregate begins 1957 — dotted 1950–56 is a linear deflator\n"
                         "backcast (fit 1957–66). Complete calendar years through 2024.",
            transform=ax.transAxes, fontsize=8.5, va="top", color="0.35")
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT_CSV.name, "and", OUT_PNG.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
