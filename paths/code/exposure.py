# exposure.py — who is exposed to which wave, region by region. Her call (2026-09-24): robotics is a year or two
# out at least, which should make a difference. So the crash model's displacement comes in two waves: cognitive work
# now (language models, agents), physical work after a robotics lag. Occupations are grouped by ISCO-08 major group:
#   cognitive   1 managers, 2 professionals, 3 technicians and associate professionals, 4 clerical support
#   in-person   5 service and sales workers (care, food, personal services, protective services, shop sales) —
#               exposed to neither wave in this model; it holds shop sales, which are partly exposed to both
#   physical    6 skilled agricultural, 7 craft and trades, 8 plant and machine operators, 9 elementary occupations
# Armed forces (0) are left out.
#
# Measured (ILOSTAT, public, cached under cache/ilo/):
#   shares      employment by occupation, ILO modelled estimates (Nov. 2025) for 2025 — the one source that covers
#               China; its groups 6 and 9 come combined (96), which the grouping above does not need to split;
#   pay         average monthly earnings by occupation (latest year: 2025; Germany 2022), weighted by the labour
#               force survey's employment by occupation in the same year: each group's pay against the average;
#               China has no occupational earnings in ILOSTAT: the mean of the other three regions' premia, stated;
#   cyclicality how each group's employment moved in a recession against employment as a whole — the US 2007-2010
#               (ISCO-08; the labour force survey's annual averages), with Spain 2007-2010 and Sweden 2008-2010
#               (ISCO-88 major groups, the same split at this level) as confirmations. Recessions cut physical work
#               two to three times as fast as the whole; cognitive work half as fast or less.
# The euro area is Germany, France, Italy, Spain and the Netherlands (about 80% of its employment), employment-weighted.
#
# Run from paths/:  ../venv/Scripts/python.exe code/exposure.py
# Out: results/exposure.json

from __future__ import annotations

import json
import os

import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, "cache", "ilo")
ILO = "https://rplumber.ilo.org/data/indicator/?id={ind}&ref_area={area}&timefrom={t0}&format=.csv"
EA = ("DEU", "FRA", "ITA", "ESP", "NLD")
AREAS = {"US": ("USA",), "EA": EA, "SE": ("SWE",), "CN": ("CHN",)}
GROUPS = {"cognitive": ("1", "2", "3", "4"), "in_person": ("5",), "physical": ("6", "7", "8", "9")}


def ilo(ind: str, area: str, tag: str = "", t0: int = 2015, t1: int | None = None, sex: str | None = "SEX_T") -> pd.DataFrame:
    """One ILOSTAT indicator for one country, from the cache or the ILO's public API (rplumber)."""
    fp = os.path.join(CACHE, f"{ind}_{area}{tag}.csv")
    if not os.path.exists(fp):
        url = ILO.format(ind=ind, area=area, t0=t0) + (f"&sex={sex}" if sex else "") + (f"&timeto={t1}" if t1 else "")
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        os.makedirs(CACHE, exist_ok=True)
        open(fp, "wb").write(r.content)
    try:
        return pd.read_csv(fp, encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def by_isco(d: pd.DataFrame, scheme: str = "ISCO08") -> pd.DataFrame:
    d = d[d.classif1.str.startswith(f"OCU_{scheme}_")].dropna(subset=["obs_value"]).copy()
    d["g"] = d.classif1.str.split("_").str[-1]
    return d.pivot_table(index="g", columns="time", values="obs_value")


def group_of(code: str) -> str | None:
    if code == "96":                                     # the modelled estimates' 6 + 9
        return "physical"
    return next((g for g, cs in GROUPS.items() if code in cs), None)


def shares(country: str) -> dict:
    """Employment by group, thousands, 2025 (ILO modelled estimates)."""
    p = by_isco(ilo("EMP_2EMP_SEX_OCU_NB_A", country))
    y = int(p.columns.max())
    out = {g: 0.0 for g in GROUPS}
    for code, v in p[y].items():
        g = group_of(code)
        if g:
            out[g] += float(v)
    return {"year": y, "employment": out}


def premia(country: str) -> dict | None:
    """Each group's average monthly pay against the average of all groups, employment-weighted within the group."""
    e = ilo("EAR_EMTA_SEX_OCU_NB_A", country)
    if e.empty or not e.classif1.str.startswith("OCU_ISCO08_").any():
        return None
    e = by_isco(e)
    n = by_isco(ilo("EMP_TEMP_SEX_OCU_NB_A", country))
    if n.empty:
        return None
    years = [y for y in e.columns if y in n.columns and all(c in e.index and pd.notna(e.loc[c, y]) for c in "123456789")]
    if not years:
        return None
    y = max(years)
    pay = {c: float(e.loc[c, y]) for c in "123456789"}
    emp = {c: float(n.loc[c, y]) for c in "123456789"}
    avg = sum(pay[c] * emp[c] for c in pay) / sum(emp.values())
    return {"year": int(y), **{g: round(sum(pay[c] * emp[c] for c in cs) / sum(emp[c] for c in cs) / avg, 3) for g, cs in GROUPS.items()}}


def cyclicality() -> dict:
    """Each group's employment change in a recession over the change in all employment (the 'beta')."""
    out = {}
    for country, scheme, y0, y1 in (("USA", "ISCO08", 2007, 2010), ("ESP", "ISCO88", 2007, 2010), ("SWE", "ISCO88", 2008, 2010)):
        p = by_isco(ilo("EMP_TEMP_SEX_OCU_NB_A", country, tag="_2006", t0=2006, t1=2012), scheme)
        nine = list("123456789")
        tot = p.loc[nine, y1].sum() / p.loc[nine, y0].sum() - 1
        row = {"window": f"{y0}-{y1}", "scheme": scheme, "all_employment_change_pct": round(100 * float(tot), 2)}
        for g, cs in GROUPS.items():
            ch = p.loc[list(cs), y1].sum() / p.loc[list(cs), y0].sum() - 1
            row[g] = {"share_at_start": round(float(p.loc[list(cs), y0].sum() / p.loc[nine, y0].sum()), 3),
                      "change_pct": round(100 * float(ch), 2), "beta": round(float(ch / tot), 2)}
        out[country] = row
    return out


def regions() -> dict:
    """The four regions: shares of employment by group (2025), pay against the average, and the recession betas
    (the US's, applied everywhere)."""
    cyc = cyclicality()
    beta = {g: cyc["USA"][g]["beta"] for g in GROUPS}
    out = {}
    for r, countries in AREAS.items():
        sh = {g: 0.0 for g in GROUPS}
        for c in countries:
            for g, v in shares(c)["employment"].items():
                sh[g] += v
        tot = sum(sh.values())
        pr, weights = {g: 0.0 for g in GROUPS}, 0.0
        years = []
        for c in countries:
            p = premia(c)
            if p is None:
                continue
            w = sum(shares(c)["employment"].values())
            for g in GROUPS:
                pr[g] += w * p[g]
            weights += w
            years.append(p["year"])
        out[r] = {"countries": list(countries), "employment_thousands": round(tot),
                  "share": {g: round(v / tot, 4) for g, v in sh.items()},
                  "premium": {g: round(v / weights, 3) for g, v in pr.items()} if weights else None,
                  "premium_years": sorted(set(years))}
    measured = [r for r in out if out[r]["premium"]]
    for r in out:
        if out[r]["premium"] is None:                    # China: the mean of the other regions', stated
            out[r]["premium"] = {g: round(sum(out[q]["premium"][g] for q in measured) / len(measured), 3) for g in GROUPS}
            out[r]["premium_note"] = "no occupational earnings in ILOSTAT: the mean of the other regions' premia"
    for r in out:
        s = out[r]["share"]
        z = sum(s[g] * beta[g] for g in GROUPS)
        # the share of a recession's job loss falling on each group, with the US betas and the region's own shares
        out[r]["recession_loss_share"] = {g: round(s[g] * beta[g] / z, 4) for g in GROUPS}
    return {"regions": out, "cyclicality": cyc, "beta_used": beta}


def main():
    res = regions()
    json.dump(res, open(os.path.join(ROOT, "results", "exposure.json"), "w", encoding="utf-8"), indent=1)
    for r, x in res["regions"].items():
        print(f"{r}: shares {x['share']}  pay vs average {x['premium']} ({x['premium_years'] or x.get('premium_note')})  "
              f"recession loss shares {x['recession_loss_share']}")
    for c, x in res["cyclicality"].items():
        print(c, x)


if __name__ == "__main__":
    main()
