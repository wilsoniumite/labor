# build_envelope.py — unit 2: the w/c grid and the family A revealed-adoption
# envelope (spec: companion_schedule_spec.md). Lemma 1 inverted: a task flips
# when rho-tilde crosses w/c, so a flip date plus the w/c path pins
# rho-tilde = (w/c)(flip year) on the flipped set and censors the unflipped
# set above today's waterline. Units: w/c normalized to 1999 = 1 (the panel
# base) — the schedule is identified up to scale, and the envelope delivers
# it in waterline units; no capability numeraire is claimed.
#
# The w/c grid — 2 wage x 3 machine-cost members, every FRED ID title-verified
# live 2026-08-06 (session log):
#   w: AHETPI  "Average Hourly Earnings of Production and Nonsupervisory
#              Employees, Total Private" (1964-);
#      oews    employment-weighted mean h_mean from the unit-1 panel (1999-).
#   c: B935RG3Q086SBEA "Private fixed investment, chained price index:
#              Nonresidential: Equipment: Information processing equipment:
#              Computers and peripheral equipment" (1959-) — the hedonic
#              collapsing series (aggressive member);
#      PCU334111334111 "PPI by Industry: Electronic Computer Manufacturing"
#              (1990-12-) — middle member;
#      Y033RG3Q086SBEA "Gross Private Domestic Investment: Fixed Investment:
#              Nonresidential: Equipment (chain-type price index)" (1947-)
#              — broad-equipment conservative member.
#
# Flip detection — occupation-level proxy for the task bundle's marginal task
# crossing the waterline; a labeled judgment layer, run as a RULE GRID:
#   rule (ceil, cross): occupation j flips iff its employment share falls to
#   <= ceil of its within-panel peak by 2025, with the peak at or before
#   2022 (>= 3 post-peak years); the flip year is the first post-peak year
#   the share crosses <= cross of peak. d30 = (0.70, 0.85), d40 = (0.60,
#   0.80), d50 = (0.50, 0.75). MIN_EMP screens noise occupations.
# Pre-registered honesty (spec): share declines conflate demand shifts with
# automation — this unit delivers the envelope under labeled rules and
# states the confound; the exposure-instrument refinement is family C /
# cross-validation work. Occupations are task bundles; the flip date proxies
# the bundle's marginal task, not every task in it.
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))
CACHE = os.path.normpath(os.path.join(HERE, "..", "cache"))
os.makedirs(DATA, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

# house FRED machinery, cache redirected to companion/cache
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "pinning", "code")))
import lambda_compute2 as lc  # noqa: E402
lc.CACHE = CACHE

W_IDS = {"ahetpi": "AHETPI"}
C_IDS = {"pc_hedonic": "B935RG3Q086SBEA",
         "ppi_computer": "PCU334111334111",
         "equip_broad": "Y033RG3Q086SBEA"}
# wrong-series catchers: (level-ratio 2025/1999 lo, hi) after annualizing.
# pc_hedonic band top 0.40, not 0.25: the hedonic decline slowed sharply
# after 2010 (realized ratio 0.286 = -4.7%/yr avg over the span); a
# wrong-series pull would sit >= 0.8, so the catcher still catches.
C_SANITY = {"pc_hedonic": (0.0, 0.40), "ppi_computer": (0.0, 0.80),
            "equip_broad": (0.70, 2.00)}
BASE = 1999
RULES = {"d30": (0.70, 0.85), "d40": (0.60, 0.80), "d50": (0.50, 0.75)}
MIN_EMP = 10_000          # mean panel employment screen (noise floor)
LAST = 2025
PEAK_MAX = LAST - 3       # peak must leave >= 3 post-peak years
ERAS = [2005, 2015, 2025]

ledger = []


def note(msg):
    ledger.append(msg)
    print(msg)


def pull_annual(sid):
    s = lc.pull_fred(sid)
    if s is None:
        note(f"BLOCKED: FRED {sid} unavailable — stopping rather than approximating.")
        raise SystemExit(1)
    return lc.annualize(s)


def build_wc(panel):
    wages = {"ahetpi": pull_annual(W_IDS["ahetpi"])}
    oews = (panel.dropna(subset=["h_mean"]).groupby("year")
            .apply(lambda g: np.average(g["h_mean"], weights=g["emp"]),
                   include_groups=False))
    wages["oews"] = oews
    costs = {}
    for name, sid in C_IDS.items():
        a = pull_annual(sid)
        ratio = float(a.loc[LAST]) / float(a.loc[BASE])
        lo, hi = C_SANITY[name]
        if not (lo <= ratio <= hi):
            note(f"BLOCKED: {name} ({sid}) {LAST}/{BASE} level ratio {ratio:.3f} "
                 f"outside [{lo},{hi}] — wrong series?")
            raise SystemExit(1)
        note(f"c member {name} ({sid}): {BASE}->{LAST} level ratio {ratio:.3f}")
        costs[name] = a
    years = list(range(BASE, LAST + 1))
    grid = pd.DataFrame(index=pd.Index(years, name="year"))
    for wn, ws in wages.items():
        for cn, cs in costs.items():
            ok_years = [y for y in years if y in ws.index and y in cs.index]
            if ok_years != years:
                note(f"BLOCKED: member {wn}_x_{cn} misses years "
                     f"{sorted(set(years) - set(ok_years))}.")
                raise SystemExit(1)
            m = pd.Series({y: float(ws.loc[y]) / float(cs.loc[y]) for y in years})
            grid[f"{wn}_x_{cn}"] = m / m.loc[BASE]
    grid["wc_median"] = grid.median(axis=1)
    note(f"w/c grid: {grid.shape[1] - 1} members, waterline median "
         f"{BASE}=1.000 -> {LAST}={grid.loc[LAST, 'wc_median']:.2f} "
         f"(spread {grid.loc[LAST].drop('wc_median').min():.2f}"
         f"-{grid.loc[LAST].drop('wc_median').max():.2f})")
    return grid


def detect_flips(panel):
    """Per rule: occupation flip status and flip year from employment shares."""
    emp = panel.pivot(index="year", columns="occ1990dd", values="emp")
    share = emp.div(emp.sum(axis=1), axis=0)
    labels = (panel[panel["year"] == panel["year"].max()]
              .set_index("occ1990dd")["top_source_title"])
    universe = emp.columns[emp.mean() >= MIN_EMP]
    note(f"universe: {len(universe)} occupations with mean emp >= {MIN_EMP:,} "
         f"({emp[universe].loc[BASE].sum() / emp.loc[BASE].sum():.3f} of {BASE} employment); "
         f"{emp.shape[1] - len(universe)} screened out")
    base_w = emp.loc[BASE]
    out = {}
    for rule, (ceil_, cross) in RULES.items():
        rows = []
        for j in universe:
            s = share[j].dropna()
            if BASE not in s.index or len(s) < 10:
                continue
            peak_year = int(s.idxmax())
            ratio_end = float(s.loc[LAST] / s.loc[peak_year]) if LAST in s.index else np.nan
            flipped = (peak_year <= PEAK_MAX) and (ratio_end <= ceil_)
            flip_year = None
            if flipped:
                post = s.loc[peak_year:]
                below = post[post / s.loc[peak_year] <= cross]
                flip_year = int(below.index[0]) if len(below) else None
                flipped = flip_year is not None
            rows.append({"occ1990dd": j, "label": labels.get(j, ""),
                         "emp_base": float(base_w.get(j, np.nan)),
                         "peak_year": peak_year, "end_over_peak": ratio_end,
                         "flipped": flipped, "flip_year": flip_year})
        df = pd.DataFrame(rows)
        mass = df[df["flipped"]]["emp_base"].sum() / df["emp_base"].sum()
        note(f"rule {rule}: {int(df['flipped'].sum())}/{len(df)} occupations "
             f"flipped, {mass:.3f} of {BASE} universe employment")
        if df["flipped"].sum() < 5 or not (0.01 <= mass <= 0.60):
            note(f"BLOCKED: rule {rule} degenerate — stopping.")
            raise SystemExit(1)
        out[rule] = df
    return out


def build_envelope(flips, grid):
    members = [c for c in grid.columns if c != "wc_median"] + ["wc_median"]
    rows = []
    for rule, df in flips.items():
        for r in df[df["flipped"]].itertuples(index=False):
            for m in members:
                rows.append({"rule": rule, "wc_member": m,
                             "occ1990dd": r.occ1990dd, "label": r.label,
                             "flip_year": int(r.flip_year),
                             "rho_wc": float(grid.loc[int(r.flip_year), m]),
                             "emp_base": r.emp_base})
    env = pd.DataFrame(rows)

    stats = []
    for rule, df in flips.items():
        tot = df["emp_base"].sum()
        f = df[df["flipped"]]
        for era in ERAS:
            by = f[f["flip_year"] <= era]
            rho = env[(env["rule"] == rule) & (env["wc_member"] == "wc_median")
                      & (env["flip_year"] <= era)]
            q = (rho.assign(w=rho["emp_base"])
                 .sort_values("rho_wc")) if len(rho) else None
            if q is not None and len(q):
                cum = q["w"].cumsum() / q["w"].sum()
                def wq(p):
                    return float(q["rho_wc"][cum >= p].iloc[0])
                p25, p50, p75 = wq(0.25), wq(0.50), wq(0.75)
            else:
                p25 = p50 = p75 = np.nan
            stats.append({"rule": rule, "era": era,
                          "mass_flipped": by["emp_base"].sum() / tot,
                          "n_flipped": len(by),
                          "rho_p25": p25, "rho_p50": p50, "rho_p75": p75,
                          "rho_iqr_log": (np.log(p75) - np.log(p25))
                          if np.isfinite(p25) and p25 > 0 else np.nan})
    stats = pd.DataFrame(stats)

    dens = []
    logwc = np.log(grid["wc_median"])
    for rule, df in flips.items():
        tot = df["emp_base"].sum()
        f = df[df["flipped"]]
        for y in range(BASE + 1, LAST + 1):
            dmass = f[f["flip_year"] == y]["emp_base"].sum() / tot
            dlog = float(logwc.loc[y] - logwc.loc[y - 1])
            dens.append({"rule": rule, "year": y, "dmass": dmass,
                         "dlog_wc": dlog,
                         "density": dmass / dlog if dlog > 0 else np.nan})
    dens = pd.DataFrame(dens)
    return env, stats, dens


def draw(grid, flips, env):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    members = [c for c in grid.columns if c != "wc_median"]
    ax1.fill_between(grid.index, grid[members].min(axis=1),
                     grid[members].max(axis=1), alpha=0.25,
                     label="w/c band across 6 members")
    ax1.plot(grid.index, grid["wc_median"], lw=2, label="w/c median")
    ax1.set_yscale("log")
    ax1.set_ylabel(f"waterline w/c ({BASE} = 1, log scale)")
    ax1.set_title("The waterline: wage over machine cost")
    ax1.legend(loc="upper left", fontsize=8)

    colors = {"d30": "tab:blue", "d40": "tab:orange", "d50": "tab:green"}
    for rule, df in flips.items():
        tot = df["emp_base"].sum()
        e = (env[(env["rule"] == rule) & (env["wc_member"] == "wc_median")]
             .sort_values("rho_wc"))
        if not len(e):
            continue
        x = e["rho_wc"].values
        y = e["emp_base"].cumsum().values / tot
        ax2.step(x, y, where="post", color=colors[rule], lw=1.6,
                 label=f"rule {rule} ({y[-1]:.0%} flipped by {LAST})")
    top = grid.loc[LAST, "wc_median"]
    ax2.axvline(top, color="k", lw=1, ls=":")
    ax2.annotate(f"waterline {LAST}\n(censoring bound:\nmass to the right\n"
                 "is unflipped, only\nbounded below)",
                 xy=(top, 0.55), xytext=(top * 0.28, 0.62), fontsize=7.5,
                 arrowprops=dict(arrowstyle="->", lw=0.8))
    for era in ERAS[:-1]:
        ax2.axvline(grid.loc[era, "wc_median"], color="gray", lw=0.8, ls="--")
        ax2.text(grid.loc[era, "wc_median"] * 1.04, 0.35,
                 f"waterline {era}", fontsize=7, ha="left", va="bottom",
                 color="gray", rotation=90)
    ax2.set_xscale("log")
    ax2.set_xlim(0.9, top * 1.6)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel(f"rho-tilde in waterline units (w/c at flip, {BASE} = 1, log)")
    ax2.set_ylabel(f"cumulative {BASE}-employment share flipped")
    ax2.set_title("The schedule's measured lower envelope")
    ax2.legend(loc="upper left", fontsize=8)

    fig.tight_layout()
    fp = os.path.join(FIGS, "schedule_envelope.png")
    fig.savefig(fp, dpi=150)
    note(f"wrote {os.path.relpath(fp, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    note("=== envelope build (unit 2): w/c grid + revealed-adoption envelope ===")
    panel = pd.read_csv(os.path.join(DATA, "oews_occ1990dd_panel.csv"))
    grid = build_wc(panel)
    flips = detect_flips(panel)
    env, stats, dens = build_envelope(flips, grid)

    tel = {rule: df[df["occ1990dd"] == 348] for rule, df in flips.items()}
    for rule, t in tel.items():
        if len(t) and bool(t["flipped"].iloc[0]):
            note(f"telephone operators under {rule}: flip year "
                 f"{int(t['flip_year'].iloc[0])}")

    grid.to_csv(os.path.join(DATA, "wc_grid.csv"))
    env.to_csv(os.path.join(DATA, "envelope.csv"), index=False)
    stats.to_csv(os.path.join(DATA, "envelope_stats.csv"), index=False)
    dens.to_csv(os.path.join(DATA, "waterline_density.csv"), index=False)
    for rule, df in flips.items():
        df.to_csv(os.path.join(DATA, f"flips_{rule}.csv"), index=False)
    draw(grid, flips, env)
    with open(os.path.join(DATA, "envelope_ledger.txt"), "w", encoding="utf8") as fh:
        fh.write("\n".join(ledger) + "\n")
    print("\n=== era-slice stats (wc_median member) ===")
    print(stats.round(3).to_string(index=False))
    note("wrote data/wc_grid.csv, envelope.csv, envelope_stats.csv, "
         "waterline_density.csv, flips_*.csv, envelope_ledger.txt")
