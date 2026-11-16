# hx_test.py — H-X, the cross-country test of absorption, run exactly as frozen in docs/spec.md Section 7 (commit
# c8750c0, pushed 2026-11-16 before any of its data were pulled).
#   Claim tested: where hours per working-age person grew faster, output per hour grew more slowly.
#   Data: OECD Productivity database (GDP per hour worked, USD at constant PPPs, chain-linked volume; total hours
#   worked) and OECD population aged 15-64 (cache/oecd/, MANIFEST.md). Sample: the 38 OECD members with complete
#   annual data 1995-2019, excluding Ireland and Luxembourg.
#   Primary: OLS g_pi = a + b g_h + c log pi_1995, HC1 standard errors.
#   Secondary: five-year panel (1995-2000, ..., 2015-19), country and period fixed effects, wild cluster bootstrap by
#   country (Webb weights, 9,999 draws), restricted (null imposed).
#   Robustness: leave one country out; division bias, with Penn World Table 11.0 hours as an instrument for the OECD
#   measure. Decision: consistent if b < 0 with two-sided p < 0.05 in the primary and the same sign in the secondary;
#   counts against if b > 0 with p < 0.05 in the primary; otherwise uninformative.
# Plain functions, numpy and scipy. Run from stagnation/:  ../venv/bin/python code/hx_test.py
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from tqdm.auto import tqdm

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache"
OUT_JSON = ROOT / "data" / "hx_results.json"
OUT_CSV = ROOT / "data" / "hx_sample.csv"

# the 38 OECD members (November 2026; Bulgaria, Croatia, Peru and Romania are candidates, not members)
MEMBERS = ("AUS", "AUT", "BEL", "CAN", "CHE", "CHL", "COL", "CRI", "CZE", "DEU", "DNK", "ESP", "EST", "FIN", "FRA",
           "GBR", "GRC", "HUN", "IRL", "ISL", "ISR", "ITA", "JPN", "KOR", "LTU", "LUX", "LVA", "MEX", "NLD", "NOR",
           "NZL", "POL", "PRT", "SVK", "SVN", "SWE", "TUR", "USA")
EXCLUDE = ("IRL", "LUX")
Y0, Y1 = 1995, 2019
PERIODS = ((1995, 2000), (2000, 2005), (2005, 2010), (2010, 2015), (2015, 2019))
DRAWS, SEED = 9999, 20261116


# ------------------------------------------------------------------------------------------------------------ data
def load():
    """(GDP per hour at constant PPPs, total hours in millions, population 15-64 in persons, PWT hours in millions):
    each a country x year frame."""
    pdb = pd.read_csv(CACHE / "oecd" / "pdb_raw.csv")
    gdph = pdb[(pdb.MEASURE == "GDPHRS") & (pdb.ACTIVITY == "_T") & (pdb.UNIT_MEASURE == "USD_PPP_H")
               & (pdb.PRICE_BASE == "LR") & (pdb.CONVERSION_TYPE == "PPP") & (pdb.TRANSFORMATION == "N")]
    hrs = pdb[(pdb.MEASURE == "HRSTO") & (pdb.ACTIVITY == "_T") & (pdb.UNIT_MEASURE == "H")
              & (pdb.TRANSFORMATION == "N")]
    assert (hrs.UNIT_MULT == 6).all(), "total hours expected in millions"
    pop = pd.read_csv(CACHE / "oecd" / "pop_raw.csv")
    pop = pop[(pop.MEASURE == "POP") & (pop.UNIT_MEASURE == "PS") & (pop.SEX == "_T") & (pop.AGE == "Y15T64")
              & (pop.TIME_HORIZ == "H")]
    assert (pop.UNIT_MULT == 0).all()
    wide = lambda d: d.pivot_table(index="REF_AREA", columns="TIME_PERIOD", values="OBS_VALUE", aggfunc="first")  # noqa
    for d in (gdph, hrs, pop):
        assert not d.duplicated(["REF_AREA", "TIME_PERIOD"]).any(), "one value per country and year"
    pwt = pd.read_excel(CACHE / "pwt" / "pwt110.xlsx", sheet_name="Data")
    pwt_h = (pwt.assign(h=pwt.avh * pwt.emp).pivot_table(index="countrycode", columns="year", values="h"))  # millions
    return wide(gdph), wide(hrs), wide(pop), pwt_h


def sample(gdph, hrs, pop, y0=Y0, y1=Y1):
    years = list(range(y0, y1 + 1))
    keep = []
    for c in MEMBERS:
        if c in EXCLUDE:
            continue
        ok = all(c in d.index and all(y in d.columns and np.isfinite(d.loc[c, y]) for y in years)
                 for d in (gdph, hrs, pop))
        if ok:
            keep.append(c)
    return keep


def growth(d, c, y0, y1):
    return (np.log(d.loc[c, y1]) - np.log(d.loc[c, y0])) / (y1 - y0)


def build(gdph, hrs, pop, countries, y0=Y0, y1=Y1):
    hpp = hrs / pop * 1e6                    # hours per person aged 15-64
    rows = [dict(country=c, g_pi=growth(gdph, c, y0, y1), g_h=growth(hpp, c, y0, y1),
                 log_pi0=np.log(gdph.loc[c, y0]), pi0=gdph.loc[c, y0], hpp0=hpp.loc[c, y0], hpp1=hpp.loc[c, y1])
            for c in countries]
    return pd.DataFrame(rows).set_index("country")


# ------------------------------------------------------------------------------------------------ the estimators
def ols_hc1(y, X):
    """OLS with HC1 standard errors: (beta, se, t, two-sided p with n - k df)."""
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    meat = (X * e[:, None] ** 2).T @ X
    V = n / (n - k) * XtXi @ meat @ XtXi
    se = np.sqrt(np.diag(V))
    t = b / se
    return b, se, t, 2 * stats.t.sf(np.abs(t), n - k)


def primary(df):
    X = np.column_stack([np.ones(len(df)), df.g_h.values, df.log_pi0.values])
    b, se, t, p = ols_hc1(df.g_pi.values, X)
    return dict(beta=b[1], se=se[1], t=t[1], p=p[1], gamma=b[2], n=len(df))


def panel_frame(gdph, hrs, pop, countries):
    hpp = hrs / pop * 1e6
    rows = [dict(country=c, period=f"{a}-{z}", g_pi=growth(gdph, c, a, z), g_h=growth(hpp, c, a, z))
            for c in countries for a, z in PERIODS]
    return pd.DataFrame(rows)


def webb(rng, size):
    w = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
    return w[rng.integers(0, 6, size=size)]


def panel(pf, draws=DRAWS, seed=SEED):
    """g_pi = b g_h + country FE + period FE; CR1 by country; restricted wild cluster bootstrap with Webb weights."""
    country = pf.country.to_numpy(dtype=object)
    period = pf.period.to_numpy(dtype=object)
    cs, ps = sorted(set(country)), sorted(set(period))
    D_c = (country[:, None] == np.array(cs, dtype=object)[None, :]).astype(float)
    D_p = (period[:, None] == np.array(ps, dtype=object)[None, 1:]).astype(float)    # one period dropped
    X = np.column_stack([pf.g_h.to_numpy(float), D_c, D_p])
    y = pf.g_pi.to_numpy(float)
    n, k = X.shape
    g_idx = np.searchsorted(np.array(cs, dtype=object), country)
    G = len(cs)
    A = np.linalg.inv(X.T @ X) @ X.T                                                 # beta = A y
    c1 = G / (G - 1) * (n - 1) / (n - k)

    def t_stat(yv):
        b = A @ yv
        u = yv - X @ b
        s = np.bincount(g_idx, weights=A[0] * u, minlength=G)                          # per-cluster score, coef 0
        return b[0], b[0] / np.sqrt(c1 * np.sum(s ** 2))

    b0, t0 = t_stat(y)
    Xr = X[:, 1:]                                                                     # the null b = 0 imposed
    br = np.linalg.lstsq(Xr, y, rcond=None)[0]
    yhat_r, u_r = Xr @ br, y - Xr @ br
    rng = np.random.default_rng(seed)
    tb = np.empty(draws)
    for i in tqdm(range(draws), desc="wild cluster bootstrap", leave=False):
        v = webb(rng, G)[g_idx]
        tb[i] = t_stat(yhat_r + u_r * v)[1]
    p = np.mean(np.abs(tb) >= abs(t0))
    return dict(beta=b0, t=t0, p_boot=p, n=n, clusters=G, draws=draws)


def leave_one_out(df):
    out = {}
    for c in df.index:
        r = primary(df.drop(index=c))
        out[c] = dict(beta=r["beta"], p=r["p"])
    return out


def iv_pwt(df, pwt_h, pop, y0=Y0, y1=Y1):
    """2SLS: the OECD hours measure instrumented by PWT hours (avh x emp) over the same population; HC1-type robust
    standard errors on the second stage with the structural residuals."""
    have = [c for c in df.index if c in pwt_h.index and np.isfinite(pwt_h.loc[c, y0]) and np.isfinite(pwt_h.loc[c, y1])]
    d = df.loc[have].copy()
    d["g_h_pwt"] = [(np.log(pwt_h.loc[c, y1] * 1e6 / pop.loc[c, y1]) - np.log(pwt_h.loc[c, y0] * 1e6 / pop.loc[c, y0]))
                    / (y1 - y0) for c in have]
    n = len(d)
    Z = np.column_stack([np.ones(n), d.g_h_pwt.values, d.log_pi0.values])
    X = np.column_stack([np.ones(n), d.g_h.values, d.log_pi0.values])
    y = d.g_pi.values
    # first stage
    fs_b, fs_se, fs_t, fs_p = ols_hc1(d.g_h.values, Z)
    Xhat = Z @ np.linalg.lstsq(Z, X, rcond=None)[0]
    b = np.linalg.lstsq(Xhat, y, rcond=None)[0]
    e = y - X @ b
    XhXi = np.linalg.inv(Xhat.T @ Xhat)
    V = n / (n - 3) * XhXi @ ((Xhat * e[:, None] ** 2).T @ Xhat) @ XhXi
    se = np.sqrt(np.diag(V))
    return dict(beta=b[1], se=se[1], p=2 * stats.t.sf(abs(b[1] / se[1]), n - 3), n=n,
                first_stage_coef=fs_b[1], first_stage_t=fs_t[1], corr=np.corrcoef(d.g_h, d.g_h_pwt)[0, 1])


def decide(pr, pa):
    if pr["beta"] < 0 and pr["p"] < 0.05 and pa["beta"] < 0:
        return "consistent"
    if pr["beta"] > 0 and pr["p"] < 0.05:
        return "counts against"
    return "uninformative"


def run():
    gdph, hrs, pop, pwt_h = load()
    countries = sample(gdph, hrs, pop)
    df = build(gdph, hrs, pop, countries)
    pr = primary(df)
    pa = panel(panel_frame(gdph, hrs, pop, countries))
    loo = leave_one_out(df)
    iv = iv_pwt(df, pwt_h, pop)
    dropped = [c for c in MEMBERS if c not in countries and c not in EXCLUDE]
    res = dict(sample=countries, n=len(countries), dropped_incomplete=dropped, excluded=list(EXCLUDE),
               primary=pr, panel=pa, iv_pwt=iv, decision=decide(pr, pa),
               loo_sign_flips=[c for c, r in loo.items() if np.sign(r["beta"]) != np.sign(pr["beta"])],
               loo_p_above_005=[c for c, r in loo.items() if r["p"] >= 0.05],
               loo_beta_range=[min(r["beta"] for r in loo.values()), max(r["beta"] for r in loo.values())],
               loo_p_max=max(r["p"] for r in loo.values()),
               mean_g_pi=df.g_pi.mean(), mean_g_h=df.g_h.mean())
    return df, res


if __name__ == "__main__":
    df, res = run()
    OUT_JSON.parent.mkdir(exist_ok=True)
    df.to_csv(OUT_CSV)
    OUT_JSON.write_text(json.dumps(res, indent=2, default=float))
    print(f"sample: {res['n']} countries; dropped for incomplete data: {res['dropped_incomplete']}; "
          f"excluded: {res['excluded']}")
    p, a, v = res["primary"], res["panel"], res["iv_pwt"]
    print(f"primary   beta {p['beta']:+.4f}  se {p['se']:.4f}  p {p['p']:.4f}  (gamma on log pi_1995 {p['gamma']:+.4f})")
    print(f"panel     beta {a['beta']:+.4f}  t {a['t']:+.3f}  bootstrap p {a['p_boot']:.4f}  ({a['n']} obs, "
          f"{a['clusters']} clusters, {a['draws']} draws)")
    print(f"IV (PWT)  beta {v['beta']:+.4f}  se {v['se']:.4f}  p {v['p']:.4f}  first stage {v['first_stage_coef']:.3f} "
          f"(t {v['first_stage_t']:.1f}, corr {v['corr']:.3f}, n {v['n']})")
    print(f"leave one out: beta in [{res['loo_beta_range'][0]:+.4f}, {res['loo_beta_range'][1]:+.4f}], "
          f"max p {res['loo_p_max']:.4f}, sign flips {res['loo_sign_flips']}, p >= 0.05 without {res['loo_p_above_005']}")
    print(f"DECISION (as frozen): {res['decision']}")
