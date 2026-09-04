"""
build_fig3_realwage_fork_1950.py — effort-accounting thread

The deflator fork extended back to 1950 (VARIANT artwork, pending her call;
the adopted FIG3_realwage_fork.png and its inputs are untouched). The
established 1964–2024 segment is reproduced from the same vendored raws and
gated to equal data/fig3_realwage_fork.csv to 1e-9; three documented long
members extend the legs left, each growth-spliced at its seam:

  wage      1950–63  AHEMAN (avg hourly earnings, production & nonsupervisory,
                     MANUFACTURING; = CES3000000008; monthly from 1939) —
                     spliced at 1964, the same long-member move as the Swedish
                     fork's manufacturing manual workers. The between-legs
                     ratio is wage-invariant, so this seam cannot touch any
                     fork-ratio claim; it moves both legs identically.
  durables  1950–55  CUUR0000SAD (CPI durables NSA; QUARTERLY Mar/Jun/Sep/Dec
                     in those years) — annual mean over exactly the four
                     quarter-end months, spliced at 1956. Overlap validation:
                     SA-vs-NSA annual means ≤0.09% apart 1956–2024, and the
                     quarterly-subsample rule ≤0.24% off the 12-month mean in
                     1956–65 (both measured at the 2026-09-01 freeze).
  shelter   1950–52  CUUR0000SEHA (CPI rent of primary residence NSA, monthly
                     from 1941) — spliced at 1953. Rent is the CPI housing
                     concept that existed before shelter did (homeownership
                     entered the index in 1953) and is the flow concept the
                     fork's framing already defends; over the first post-seam
                     decade rent grew ×1.183 vs shelter's ×1.186 (1953–63).

Output is indexed 1950 = 100 (her call, 2026-09-01). The gates run on the
internal 1964-base series, so every adopted-figure anchor is still checked
verbatim; the legs are rebased only for the CSV and the figure. In the 1950
base the 2024 endpoints read 619.0 (durables) / 104.5 (shelter), a 5.9×
fork over 1950–2024 — base-window numbers, not replacements for the
briefing's 1964-base 376.8 / 78.6 / 4.8×.

A second output overlays the project's D-F − D-Q gap (labor-origin
financing minus human-effort content of PCE, her ask 2026-09-01), read from
the frozen archive ledgers the adopted full-band figures already draw
(DF21_FINAL / LR_Q1), rebased to 0 at 1950 on a right axis whose zero is
aligned with the legs' 100 line. Raw 1950 gap +5.85pp; rebased it rises to
+14.9pp (2004) and ends +12.3pp (2024). Solid only in the both-strong
window 2004–23; dashed where either series is a weak extension.

Data rule (house): live public data only, no substitution. The three long
members vendor to data/raw/ with manifest rows appended; --refresh re-pulls
the LONG MEMBERS ONLY — the established three raws are the adopted figure's
inputs and refresh via the adopted script.

Validation gates: the adopted script's own anchors must still pass on the
extended series (2023 sanity, 2024 legs, 1983 seam ratio); the 1964+ segment
must equal the shipped CSV; long-member level sanity (frozen 2026-09-01);
the three seam-overlap validations; the extension's endpoint anchors (1950
legs 60.9 / 75.2). Any gate failure stops the build rather than approximating.

Run from the repo root:
    ./venv/Scripts/python.exe effort-accounting/code/build_fig3_realwage_fork_1950.py [--refresh]
"""

import csv
import sys
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
ADOPTED_CSV = ROOT / "data" / "fig3_realwage_fork.csv"
OUT_CSV = ROOT / "data" / "fig3_realwage_fork_1950.csv"
OUT_PNG = ROOT / "figures" / "FIG3_realwage_fork_1950.png"

ESTABLISHED = {  # the adopted figure's inputs — never pulled here
    "wage": "AHETPI",
    "durables": "CUSR0000SAD",
    "shelter": "CUSR0000SAH1",
}
LONG = {  # the extension's long members
    "wage_long": "AHEMAN",
    "durables_long": "CUUR0000SAD",
    "shelter_long": "CUUR0000SEHA",
}
START_YEAR = 1950
BASE_YEAR = 1964                      # internal gate base (the adopted figure's)
OUT_BASE = 1950                       # output index base (her call, 2026-09-01)
WAGE_SEAM, DUR_SEAM, SHEL_SEAM = 1964, 1956, 1953
QUARTER_MONTHS = frozenset(("03", "06", "09", "12"))

# Adopted-figure gates, carried over verbatim (build_fig3_realwage_fork.py).
SANITY_2023 = {"wage": (26, 32), "durables": (105, 140), "shelter": (350, 420)}
FORK_ANCHORS = [
    ("durables leg 2024", 2024, "durables", 376.8, 3.0),
    ("shelter leg 2024", 2024, "shelter", 78.6, 1.5),
]
SEAM_RATIO_1983 = (1.46, 0.05)
# Long-member level sanity, frozen from the 2026-09-01 pulls (guards id drift).
SANITY_LONG = {
    "wage_long": [(1950, 1.1, 1.5), (2024, 25, 31)],
    "durables_long": [(1950, 32, 38)],
    "shelter_long": [(1950, 27, 33), (2024, 395, 445)],
}
# Extension endpoint anchors (series built 2026-09-01).
EXT_ANCHORS = [
    ("durables leg 1950", 1950, "durables", 60.9, 1.0),
    ("shelter leg 1950", 1950, "shelter", 75.2, 1.0),
]

# D-F − D-Q gap overlay (her ask, 2026-09-01): frozen archive inputs — the
# same two files the adopted full-band figures read. Read-only.
ARCHIVE_EXPECTED = ROOT / "archive_v28" / "expected"
DF21_FILE = "DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv"
DQ_FILE = "LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv"
GAP_ANCHORS = [  # frozen values (STATE.md quotes them to 1dp); ±0.01
    ("D-F 2004 central", 2004, "df", 69.64),
    ("D-F 2023 central", 2023, "df", 65.81),
    ("D-Q 1950 headline", 1950, "dq", 66.38),
    ("D-Q 2023 headline", 2023, "dq", 47.23),
]
OUT_PNG_OVERLAY = ROOT / "figures" / "FIG3_realwage_fork_1950_dfq_overlay.png"
OUT_GAP_CSV = ROOT / "data" / "fig3_dfq_gap_overlay.csv"


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


def main() -> int:
    refresh = "--refresh" in sys.argv
    for concept, sid in ESTABLISHED.items():
        if not (RAW / f"{sid}.csv").exists():
            print(f"BLOCKED: established raw {sid}.csv missing — run "
                  "build_fig3_realwage_fork.py first (its inputs are not pulled here).")
            return 1

    manifest = []
    for concept, sid in LONG.items():
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
    long_annual = {"wage_long": mfg, "durables_long": dur_nsa_q, "shelter_long": rent}

    failures = []
    for concept, (lo, hi) in SANITY_2023.items():
        v = est[concept].get(2023)
        if v is None or not (lo <= v <= hi):
            failures.append(f"sanity {concept} 2023={v} not in [{lo},{hi}]")
    for concept, anchors in SANITY_LONG.items():
        for y, lo, hi in anchors:
            v = long_annual[concept].get(y)
            if v is None or not (lo <= v <= hi):
                failures.append(f"sanity {concept} {y}={v} not in [{lo},{hi}]")

    # Seam-overlap validations.
    overlap = sorted(set(est["durables"]) & set(dur_nsa12))
    sa_nsa_gap = max(abs(dur_nsa12[y] - est["durables"][y]) / est["durables"][y] for y in overlap)
    if sa_nsa_gap > 0.005:
        failures.append(f"durables SA-vs-NSA annual-mean gap {sa_nsa_gap:.2%} > 0.5%")
    q_gap = max(abs(sum(dur_nsa_m[y][m] for m in QUARTER_MONTHS) / 4 - dur_nsa12[y]) / dur_nsa12[y]
                for y in range(1956, 1966))
    if q_gap > 0.01:
        failures.append(f"quarterly-subsample rule gap {q_gap:.2%} > 1% in 1956-65")
    rent_growth = rent[1963] / rent[SHEL_SEAM]
    shel_growth = est["shelter"][1963] / est["shelter"][SHEL_SEAM]
    if abs(rent_growth / shel_growth - 1) > 0.03:
        failures.append(f"rent-vs-shelter 1953-63 growth {rent_growth:.3f} vs {shel_growth:.3f}")
    wage_factor = est["wage"][BASE_YEAR] / mfg[BASE_YEAR]
    if not (0.95 <= wage_factor <= 1.15):
        failures.append(f"wage splice factor {wage_factor:.4f} not in [0.95,1.15]")

    # Extended annual series: growth-splice each long member at its seam.
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
    if missing:
        failures.append("long-member years missing: " + ", ".join(missing))

    years = sorted(y for y in set(wage_x) & set(dur_x) & set(shel_x) if y >= START_YEAR)
    legs = {}       # internal 1964 base — everything is gated here
    legs_out = {}   # output 1950 base — a pure rebase of the gated series
    for name, defl in (("durables", dur_x), ("shelter", shel_x)):
        real = {y: wage_x[y] / defl[y] for y in years}
        legs[name] = {y: 100 * real[y] / real[BASE_YEAR] for y in years}
        legs_out[name] = {y: 100 * legs[name][y] / legs[name][OUT_BASE] for y in years}
        if abs(legs_out[name][OUT_BASE] - 100) > 1e-9:
            failures.append(f"rebase check: {name} leg at {OUT_BASE} != 100")

    # Adopted anchors must still pass on the extended series.
    for name, y, leg, target, tol in FORK_ANCHORS + EXT_ANCHORS:
        v = legs[leg].get(y)
        if v is None or abs(v - target) > tol:
            failures.append(f"anchor {name}: {v} vs {target}±{tol}")
    seam = legs["durables"][1983] / legs["shelter"][1983]
    if abs(seam - SEAM_RATIO_1983[0]) > SEAM_RATIO_1983[1]:
        failures.append(f"1983 seam ratio {seam:.3f} vs {SEAM_RATIO_1983[0]}±{SEAM_RATIO_1983[1]}")

    # The 1964+ segment must be the adopted figure, exactly.
    if not ADOPTED_CSV.exists():
        failures.append(f"{ADOPTED_CSV.name} missing — the extension is defined relative to it")
    else:
        shipped = {}
        with open(ADOPTED_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                shipped[int(row["year"])] = (float(row["real_wage_durables_1964_100"]),
                                             float(row["real_wage_shelter_1964_100"]))
        ext_post = [y for y in years if y >= BASE_YEAR]
        if ext_post != sorted(shipped):
            failures.append(f"1964+ year set differs from shipped: {ext_post[0]}–{ext_post[-1]} "
                            f"vs {min(shipped)}–{max(shipped)}")
        else:
            dev = max(max(abs(legs["durables"][y] - d), abs(legs["shelter"][y] - s))
                      for y, (d, s) in shipped.items())
            if dev > 1e-9:
                failures.append(f"1964+ segment deviates from shipped CSV by {dev:.2e} > 1e-9")

    # Gap overlay inputs and gates.
    def rcsv_by_year(p: Path) -> dict[int, dict[str, str]]:
        with open(p, newline="", encoding="utf-8-sig") as f:
            return {int(r["year"]): r for r in csv.DictReader(f)}

    df21 = rcsv_by_year(ARCHIVE_EXPECTED / DF21_FILE)
    dq = rcsv_by_year(ARCHIVE_EXPECTED / DQ_FILE)
    df_c = {y: 100 * float(r["labor_origin_financing_central"]) for y, r in df21.items()}
    dq_c = {y: 100 * float(r["human_effort_share_headline"]) for y, r in dq.items()}
    for name, y, which, target in GAP_ANCHORS:
        v = (df_c if which == "df" else dq_c).get(y)
        if v is None or abs(v - target) > 0.01:
            failures.append(f"gap anchor {name}: {v} vs {target}±0.01")
    gap_years = [y for y in years if y in df_c and y in dq_c]
    gap_raw0 = df_c[START_YEAR] - dq_c[START_YEAR]
    gap = {y: (df_c[y] - dq_c[y]) - gap_raw0 for y in gap_years}
    gap_strong = [y for y in gap_years if df21[y]["tier"].startswith("STRONG")
                  and dq[y]["evidence_tier"].startswith("STRONG")]
    if gap_strong != list(range(2004, 2024)):
        failures.append(f"gap both-strong window {gap_strong} != 2004–2023")

    print("=== validation ledger ===")
    print(f"years {years[0]}–{years[-1]} | seams: wage {WAGE_SEAM} (factor {wage_factor:.4f}), "
          f"durables {DUR_SEAM} (SA-NSA gap {sa_nsa_gap:.2%}, q-rule gap {q_gap:.2%}), "
          f"shelter {SHEL_SEAM} (rent x{rent_growth:.3f} vs shelter x{shel_growth:.3f} to 1963)")
    print(f"internal 1964 base (gates): 1950 legs {legs['durables'][1950]:.1f} / "
          f"{legs['shelter'][1950]:.1f} | 1983 seam ratio {seam:.2f} | "
          f"2024 legs {legs['durables'].get(2024, float('nan')):.1f} / "
          f"{legs['shelter'].get(2024, float('nan')):.1f}")
    last = years[-1]
    print(f"output {OUT_BASE} base: {last} legs {legs_out['durables'][last]:.1f} / "
          f"{legs_out['shelter'][last]:.1f} | fork ratio {OUT_BASE}–{last} "
          f"{legs_out['durables'][last] / legs_out['shelter'][last]:.2f}x")
    print(f"gap overlay: raw 1950 gap {gap_raw0:+.2f}pp (rebase zero) | both-strong "
          f"{gap_strong[0]}–{gap_strong[-1]} | rebased 2004 {gap[2004]:+.1f} / "
          f"2023 {gap[2023]:+.1f} / {gap_years[-1]} {gap[gap_years[-1]]:+.1f}pp")
    if failures:
        for msg in failures:
            print("FAIL", msg)
        print("BLOCKED: validation failed — stopping rather than approximating.")
        return 1
    print("all gates PASS")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "real_wage_durables_1950_100", "real_wage_shelter_1950_100",
                    "wage_member", "durables_member", "shelter_member"])
        for y in years:
            w.writerow([y, legs_out["durables"][y], legs_out["shelter"][y],
                        ESTABLISHED["wage"] if y >= WAGE_SEAM else LONG["wage_long"],
                        ESTABLISHED["durables"] if y >= DUR_SEAM else LONG["durables_long"],
                        ESTABLISHED["shelter"] if y >= SHEL_SEAM else LONG["shelter_long"]])

    with open(OUT_GAP_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "df_financing_central_pct", "dq_content_headline_pct",
                    "gap_pp", "gap_rebased_1950_pp", "df_tier", "dq_tier"])
        for y in sorted(set(df_c) & set(dq_c)):
            g = df_c[y] - dq_c[y]
            w.writerow([y, df_c[y], dq_c[y], g, g - gap_raw0,
                        df21[y]["tier"], dq[y]["evidence_tier"]])

    pre = [y for y in years if y <= BASE_YEAR]      # spliced-wage era, drawn dashed
    post = [y for y in years if y >= BASE_YEAR]

    def draw_fork(ax):
        for leg, color, label in (("durables", "tab:blue", "wage deflated by durables CPI (machine-made goods)"),
                                  ("shelter", "tab:red", "wage deflated by shelter CPI (land-priced)")):
            ax.plot(post, [legs_out[leg][y] for y in post], linewidth=2.5, color=color, label=label)
            ax.plot(pre, [legs_out[leg][y] for y in pre], linewidth=2.0, color=color, linestyle="--")
        ax.axhline(100, color="k", linewidth=0.8, linestyle=":")
        ax.set_xlim(START_YEAR, max(years))
        ax.set_xlabel("Year")
        ax.set_ylabel(f"Real average hourly earnings, {OUT_BASE} = 100")
        ax.set_title("The deflator fork: the same U.S. paycheck against machine-made goods and against land-priced shelter")
        ax.grid(True, alpha=0.25)
        ax.text(0.012, 0.76, "dashed 1950–63: long members, growth-spliced —\n"
                             "manufacturing wage (seam 1964); quarterly NSA\n"
                             "durables CPI (1956); rent of primary residence (1953)",
                transform=ax.transAxes, fontsize=8.5, va="top", color="0.35")

    fig, ax = plt.subplots(figsize=(12.2, 6.5))
    draw_fork(ax)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=250, bbox_inches="tight")
    plt.close(fig)

    # Overlay variant: the D-F − D-Q gap on a right axis whose zero is
    # aligned with the legs' 100 line (one dotted line serves both).
    fig, ax = plt.subplots(figsize=(12.2, 6.5))
    draw_fork(ax)
    lo_ax, hi_ax = ax.get_ylim()
    ax.set_ylim(lo_ax, hi_ax)
    frac = (100 - lo_ax) / (hi_ax - lo_ax)
    span = 30.0
    ax2 = ax.twinx()
    ax2.set_ylim(-frac * span, (1 - frac) * span)
    g_pre = [y for y in gap_years if y <= gap_strong[0]]
    g_mid = [y for y in gap_years if gap_strong[0] <= y <= gap_strong[-1]]
    g_post = [y for y in gap_years if y >= gap_strong[-1]]
    ax2.plot(g_mid, [gap[y] for y in g_mid], linewidth=2.0, color="tab:green",
             label="financing − content gap: D-F minus D-Q, 0 at 1950 (right axis)")
    ax2.plot(g_pre, [gap[y] for y in g_pre], linewidth=1.8, color="tab:green", linestyle="--")
    ax2.plot(g_post, [gap[y] for y in g_post], linewidth=1.8, color="tab:green", linestyle="--")
    ax2.set_ylabel("D-F − D-Q gap since 1950, percentage points", color="tab:green")
    ax2.tick_params(axis="y", labelcolor="tab:green")
    ax2.text(0.012, 0.60, "gap line: solid 2004–23 (both series strong), dashed =\n"
                          "weak-extension years; dotted line is legs 100 / gap 0",
             transform=ax.transAxes, fontsize=8.5, va="top", color="0.35")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT_PNG_OVERLAY, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT_CSV.name + ",", OUT_GAP_CSV.name + ",",
          OUT_PNG.name, "and", OUT_PNG_OVERLAY.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
