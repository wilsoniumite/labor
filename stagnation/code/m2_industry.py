# m2_industry.py — M2 of docs/spec.md: where the slowdown lives. U.S. sectors, 1947-2024, from the BEA-BLS integrated
# industry-level production account (cache/bea/; source amended before any outcome was computed, docs/spec.md):
#   1947-1997: the 1947-2016 research tables' underlying data (Eldridge et al. 2020): nominal gross output (go) and
#              intermediate input (ii), their quantity indexes (goqi, iiqi), total hours of all workers (hrs);
#              44 industries to 1963, 63 after; aggregated here to 20 NAICS sectors.
#   1997-2024: the 1997-2024 release: nominal value added, value-added quantity index, labor-hours quantity index;
#              hours levels carried forward from 1997 by the hours index, industry by industry.
# Real value added by sector: Tornqvist double deflation (1947-97) or Tornqvist over the value-added indexes (1997-).
# Decomposition, as frozen: g_{Y/H} = sum s(g_Y - g_H) + sum (s - h) g_H (s, h: average value-added and hours shares of
# the sectors in scope); eras 1948-73, 1973-95, 1995-2004, 2004-19, 2019-24; each era's change against 1948-73 split
# exactly (midpoint weights) into within-sector slowdown, weight shift (Baumol) and hours reallocation, summed by class
# (M machine-contestable, S site- and resource-bound, H human-required) on the grid G1-G6. Prediction: the weight-shift
# and reallocation terms are negative in 1973-95 and 2004-19 and together at least a quarter of the slowdown against
# 1948-73 in the median member; a tenth or less, or a positive sign, counts against; between, partial.
# Writes data/m2_sectors.csv (the annual sector panel), data/m2_decomp.json, draws Figure 4 (fig_industry.pdf, .png).
# Run from stagnation/:  ../venv/bin/python code/m2_industry.py
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

ROOT = Path(__file__).resolve().parents[1]
BEA = ROOT / "cache" / "bea"
RESEARCH = BEA / "KLEMS-Research-Tables-Underlying-Data_0.xlsx"
RELEASE = BEA / "BEA-BLS-industry-level-production-account-1997-2024.xlsx"
SPLICE = 1997
ERAS = ((1948, 1973), (1973, 1995), (1995, 2004), (2004, 2019), (2019, 2024))
BASE = (1948, 1973)

# industry number (1963-2016 numbering; the 1947-63 sheet's merged codes listed too) -> sector
SECTOR = {1: "agr", 2: "agr", 3: "min", 4: "min", 5: "min", 6: "utl", 7: "con", **{i: "mfg" for i in range(8, 27)},
          27: "whl", 28: "ret", **{i: "trn" for i in range(29, 37)}, **{i: "inf" for i in range(37, 41)},
          **{i: "fin" for i in range(41, 45)}, 45: "rea", 46: "rea", **{i: "pro" for i in range(47, 50)}, 50: "mgt",
          51: "adm", 52: "adm", 53: "edu", 54: "hea", 55: "hea", 56: "hea", 57: "art", 58: "art", 59: "acc",
          60: "acc", 61: "oth", 62: "gov", 63: "gov",
          2936: "trn", 3740: "inf", 4144: "fin", 4749: "pro", 5152: "adm", 5456: "hea", 5758: "art"}
NAMES = {"agr": "Agriculture, forestry, fishing", "min": "Mining", "utl": "Utilities", "con": "Construction",
         "mfg": "Manufacturing", "whl": "Wholesale trade", "ret": "Retail trade", "trn": "Transportation, warehousing",
         "inf": "Information", "fin": "Finance and insurance", "rea": "Real estate, rental and leasing",
         "pro": "Professional and technical services", "mgt": "Management of companies",
         "adm": "Administrative and waste services", "edu": "Educational services",
         "hea": "Health care and social assistance", "art": "Arts and recreation", "acc": "Accommodation and food",
         "oth": "Other services", "gov": "Government"}

# the classification grid of docs/spec.md (scope = sectors in the decomposition; class = M, S or H)
G1 = {"mfg": "M", "whl": "M", "trn": "M", "inf": "M", "fin": "M", "pro": "M", "mgt": "M", "ret": "M", "adm": "M",
      "agr": "S", "min": "S", "utl": "S", "con": "S",
      "edu": "H", "hea": "H", "art": "H", "acc": "H", "oth": "H"}
GRID = {"G1": G1, "G2": {**G1, "ret": "H", "adm": "H"}, "G3": {**G1, "utl": "M"}, "G4": {**G1, "gov": "H"},
        "G5": {**G1, "rea": "S"}, "G6": {**G1, "acc": "S"}}
# Exploratory, added after the frozen grid was run and NOT part of the verdict: G1 without agriculture, whose
# 1948-73 exodus of hours (22 to 7 percent of the total) is a one-time reallocation bonus no account of the later
# slowdown needs.
EXPLORE = {"X1": {k: v for k, v in G1.items() if k != "agr"}}


# -------------------------------------------------------------------------------------------- the sector panel
def research():
    out = []
    for sheet in ("1947-1963", "1963-2016"):
        d = pd.read_excel(RESEARCH, sheet, header=1)
        d = d[["yr", "indnum", "Description", "go.", "ii.", "goqi.", "iiqi.", "hrs"]].dropna(subset=["yr"])
        d["sector"] = d.indnum.astype(int).map(SECTOR)
        assert d.sector.notna().all(), d[d.sector.isna()].Description.unique()
        d["sheet"] = sheet
        out.append(d)
    return out


def tornqvist(w0, w1, g):
    w = 0.5 * (w0 / w0.sum() + w1 / w1.sum())
    return float((w * g).sum())


def sectors_research(d):
    """Per sector and year (within one sheet): nominal VA, hours, and growth of real VA (double deflation) and hours."""
    rows = []
    years = sorted(d.yr.unique())
    for s, g in d.groupby("sector"):
        g = g.set_index(["yr", "indnum"]).sort_index()
        for y in years:
            cur = g.loc[y]
            row = dict(sector=s, year=int(y), va=float(cur["go."].sum() - cur["ii."].sum()),
                       hours=float(cur.hrs.sum()))
            if y - 1 in years:
                prv = g.loc[y - 1]
                idx = cur.index.intersection(prv.index)
                gGO = tornqvist(prv.loc[idx, "go."], cur.loc[idx, "go."],
                                np.log(cur.loc[idx, "goqi."] / prv.loc[idx, "goqi."]))
                gII = tornqvist(prv.loc[idx, "ii."], cur.loc[idx, "ii."],
                                np.log(cur.loc[idx, "iiqi."] / prv.loc[idx, "iiqi."]))
                GO0, GO1 = prv.loc[idx, "go."].sum(), cur.loc[idx, "go."].sum()
                II0, II1 = prv.loc[idx, "ii."].sum(), cur.loc[idx, "ii."].sum()
                VA0, VA1 = GO0 - II0, GO1 - II1
                wGO, wII = 0.5 * (GO0 / VA0 + GO1 / VA1), 0.5 * (II0 / VA0 + II1 / VA1)
                row["g_va"] = wGO * gGO - wII * gII
                row["g_hours"] = float(np.log(cur.loc[idx, "hrs"].sum() / prv.loc[idx, "hrs"].sum()))
            rows.append(row)
    return pd.DataFrame(rows)


def release(hours_1997):
    """1997-2024 by sector: nominal VA, real VA growth (Tornqvist over industries' VA indexes), hours (1997 levels
    from the research data carried forward by each industry's hours index)."""
    read = lambda sh: (pd.read_excel(RELEASE, sh, header=1).rename(columns={"Industry Description": "ind"})  # noqa
                       .dropna(subset=["ind"]).set_index("ind"))
    va, vq, hq = read("Value Added"), read("VA_Quantity"), read("Labor Hours_Quantity")
    va.columns = vq.columns = hq.columns = [int(c) for c in va.columns]
    # the two vintages list the same 63 industries in the same order (one name differs in wording: hospitals and
    # nursing facilities); match by position, guarded by the first two words of each name
    assert len(va) == len(hours_1997) == 63 and list(va.index) == list(vq.index) == list(hq.index)
    norm = lambda s: " ".join(s.lower().replace(",", "").split()[:2])  # noqa: E731
    assert all(norm(a) == norm(b) for a, b in zip(va.index, hours_1997.index))
    sec = pd.Series(hours_1997.sector.values, index=va.index)
    hrs = hq.div(hq[SPLICE], axis=0).mul(pd.Series(hours_1997.hrs.values, index=va.index), axis=0)
    rows = []
    years = list(va.columns)
    for s in sorted(sec.unique()):
        inds = sec.index[sec == s]
        for y in years:
            row = dict(sector=s, year=y, va=float(va.loc[inds, y].sum()), hours=float(hrs.loc[inds, y].sum()))
            if y - 1 in years:
                row["g_va"] = tornqvist(va.loc[inds, y - 1], va.loc[inds, y], np.log(vq.loc[inds, y] / vq.loc[inds, y - 1]))
                row["g_hours"] = float(np.log(hrs.loc[inds, y].sum() / hrs.loc[inds, y - 1].sum()))
            rows.append(row)
    return pd.DataFrame(rows)


def panel():
    a, b = research()
    pa, pb = sectors_research(a), sectors_research(b)
    # 1947-63 sheet through 1963 (its 1963 growth), the 1963-2016 sheet from 1964 to the splice
    early = pa[pa.year <= 1963]
    mid = pb[(pb.year > 1963) & (pb.year <= SPLICE)]
    h97 = b[b.yr == SPLICE].set_index("Description")[["hrs", "sector"]]
    late = release(h97)
    late = late[late.year > SPLICE]
    p = pd.concat([early, mid, late], ignore_index=True).sort_values(["sector", "year"])
    return p


# ----------------------------------------------------------------------------------------------- decomposition
def annual_terms(p, scope):
    """Per year: s, h (average shares over t-1, t among the sectors in scope), and the two terms per sector."""
    q = p[p.sector.isin(scope)].copy()
    q["s_share"] = q.va / q.groupby("year").va.transform("sum")
    q["h_share"] = q.hours / q.groupby("year").hours.transform("sum")
    q = q.sort_values(["sector", "year"])
    q["s_bar"] = 0.5 * (q.s_share + q.groupby("sector").s_share.shift(1))
    q["h_bar"] = 0.5 * (q.h_share + q.groupby("sector").h_share.shift(1))
    q = q.dropna(subset=["s_bar", "g_va", "g_hours"])
    q["pi"] = q.g_va - q.g_hours                                         # sector labor-productivity growth
    q["within"] = q.s_bar * q.pi
    q["realloc"] = (q.s_bar - q.h_bar) * q.g_hours
    # by-sector attribution of reallocation against aggregate hours growth (the total is unchanged, since the share
    # gaps s - h sum to zero each year): hours growing faster than the total where the value-added share is below
    # the hours share (a low productivity level) count against growth
    q["g_hours_agg"] = q.groupby("year").apply(lambda d: (d.h_bar * d.g_hours).sum(), include_groups=False)\
        .reindex(q.year).values
    q["realloc_dev"] = (q.s_bar - q.h_bar) * (q.g_hours - q.g_hours_agg)
    return q


def era_stats(q, y0, y1):
    """Per sector over the era (growth years y0+1..y1): mean share s_e, share-weighted mean growth pi_e (so that the
    era's within term is sum s_e pi_e exactly), and the mean reallocation term."""
    e = q[(q.year > y0) & (q.year <= y1)]
    n = e.year.nunique()
    g = e.groupby("sector")
    s_e = g.s_bar.sum() / n
    pi_e = g.within.sum() / g.s_bar.sum()
    r_e = g.realloc.sum() / n
    r_dev = g.realloc_dev.sum() / n
    return s_e, pi_e, r_e, r_dev


def decompose(p, member):
    cls = GRID[member]
    q = annual_terms(p, list(cls))
    s0, pi0, r0, rd0 = era_stats(q, *BASE)
    out = {}
    for y0, y1 in ERAS:
        s1, pi1, r1, rd1 = era_stats(q, y0, y1)
        W0, W1 = (s0 * pi0).sum(), (s1 * pi1).sum()
        within_slow = 0.5 * (s1 + s0) * (pi1 - pi0)
        weight = 0.5 * (pi1 + pi0) * (s1 - s0)
        realloc = r1 - r0
        # class attribution against the average: growth relative to the mean of the two eras' aggregate within
        # growth, hours growth relative to total hours growth (both leave the totals unchanged)
        cbar = 0.5 * (W0 + W1)
        weight_dev = (0.5 * (pi1 + pi0) - cbar) * (s1 - s0)
        realloc_dev = rd1 - rd0
        tot1, tot0 = W1 + r1.sum(), W0 + r0.sum()
        by = lambda v: {c: 100 * float(v[[k for k, kc in cls.items() if kc == c]].sum()) for c in "MSH"}  # noqa
        assert abs(weight_dev.sum() - weight.sum()) < 1e-12 and abs(realloc_dev.sum() - realloc.sum()) < 1e-10
        out[f"{y0}-{y1}"] = dict(
            growth=100 * tot1, growth_within=100 * W1, growth_realloc=100 * r1.sum(),
            change=100 * (tot1 - tot0), within_slowdown=100 * within_slow.sum(), weight_shift=100 * weight.sum(),
            realloc_change=100 * realloc.sum(), by_class=dict(within_slowdown=by(within_slow), weight_shift=by(weight_dev),
                                                             realloc_change=by(realloc_dev)),
            realloc_level_by_class=by(rd1),
            exact=abs((tot1 - tot0) - (within_slow.sum() + weight.sum() + realloc.sum())) < 1e-12)
        if (y0, y1) != BASE:
            r = out[f"{y0}-{y1}"]
            r["composition"] = r["weight_shift"] + r["realloc_change"]
            r["composition_share"] = r["composition"] / r["change"] if r["change"] < 0 else float("nan")
    return out


def verdict(results):
    """The frozen reading, on the median member, for the two slow eras."""
    out = {}
    for era in ("1973-1995", "2004-2019"):
        comps = sorted(results[m][era]["composition"] for m in GRID)
        shares = sorted(results[m][era]["composition_share"] for m in GRID)
        med_c, med_s = float(np.median(comps)), float(np.median(shares))
        v = ("supports" if med_c < 0 and med_s >= 0.25 else
             "counts against" if med_c >= 0 or med_s <= 0.10 else "partial")
        out[era] = dict(median_composition=med_c, median_share=med_s, min_share=shares[0], max_share=shares[-1],
                        verdict=v)
    eras = [out[e]["verdict"] for e in out]
    out["overall"] = ("supports" if all(v == "supports" for v in eras) else
                      "counts against" if all(v == "counts against" for v in eras) else "partial")
    return out


# ------------------------------------------------------------------------------------------------------ figure
rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"], "mathtext.fontset": "dejavuserif",
                 "pdf.fonttype": 42, "font.size": 8.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
                 "axes.linewidth": 0.53, "xtick.major.width": 0.45, "ytick.major.width": 0.45,
                 "xtick.major.size": 2.3, "ytick.major.size": 2.3})
PRINT_W = 0.88 * 16 / 2.54
COLORS = {"within_slowdown": "#2a78d6", "weight_shift": "#eb6834", "realloc_change": "#1baf7a"}
LABELS = {"within_slowdown": "Growth within sectors", "weight_shift": "Shift of value added among sectors",
          "realloc_change": "Reallocation of hours"}
INK, MUTED, GRID_C = "#0b0b0b", "#52514e", "#e4e3df"


def draw(res):
    r = res["G1"]
    eras = [f"{y0}-{y1}" for y0, y1 in ERAS[1:]]
    fig, ax = plt.subplots(figsize=(PRINT_W, PRINT_W / 2.3), layout="constrained")
    x = np.arange(len(eras))
    width = 0.22
    for i, k in enumerate(("within_slowdown", "weight_shift", "realloc_change")):
        vals = [r[e][k] for e in eras]
        ax.bar(x + (i - 1) * width, vals, width=width * 0.92, color=COLORS[k], label=LABELS[k], zorder=3)
    ax.scatter(x, [r[e]["change"] for e in eras], marker="D", s=22, color=INK, zorder=4,
               label="Change in output-per-hour growth (sum)")
    ax.axhline(0, color=MUTED, lw=0.6, zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels([e.replace("-", "–") for e in eras])
    ax.set_ylabel("Percentage points a year,\nagainst 1948–73", fontsize=7.5)
    ax.grid(True, axis="y", color=GRID_C, lw=0.5, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.set_ylim(-2.15, 1.3)
    fig.legend(*ax.get_legend_handles_labels(), frameon=False, fontsize=6.8, loc="outside upper center", ncol=2,
               handlelength=1.2, columnspacing=1.2)
    out = ROOT / "paper" / "figures" / "fig_industry.png"
    fig.savefig(out, dpi=300)
    fig.savefig(out.with_suffix(".pdf"), metadata={"CreationDate": None})
    return out


if __name__ == "__main__":
    p = panel()
    p.to_csv(ROOT / "data" / "m2_sectors.csv", index=False)
    res = {m: decompose(p, m) for m in GRID}
    res["verdict"] = verdict(res)
    GRID_ALL = {**GRID, **EXPLORE}
    for m, cls in EXPLORE.items():
        GRID[m] = cls                       # decompose() reads the class map from GRID
        res[m] = decompose(p, m)
        del GRID[m]
    (ROOT / "data" / "m2_decomp.json").write_text(json.dumps(res, indent=2, default=float))
    for m in list(GRID) + list(EXPLORE):
        print(f"--- {m}")
        for e, r in res[m].items():
            extra = (f"  composition {r['composition']:+.3f} ({100 * r['composition_share']:.0f}% of the slowdown)"
                     if "composition" in r and np.isfinite(r.get("composition_share", np.nan)) else "")
            print(f"  {e}: growth {r['growth']:.2f} | change {r['change']:+.2f} = within {r['within_slowdown']:+.2f}"
                  f" + weight {r['weight_shift']:+.2f} + realloc {r['realloc_change']:+.2f}{extra}  exact {r['exact']}")
    print("VERDICT:", json.dumps(res["verdict"], indent=1, default=lambda v: round(float(v), 3)))
    print("wrote", draw(res))
