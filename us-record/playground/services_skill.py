# services_skill.py — a data look (2026-11-08), before designing a worker for each good and her idea of splitting services
# into low- and high-skill. Services apart (Log 25) found services' prices rising 28% faster than the production wage
# since 1957, which one wage can only follow by machines losing ground at service tasks. Two questions for the record:
#   1. Where does that rise sit? BEA's consumer spending by type of service (NIPA tables 2.4.4 and 2.4.5, the
#      repository's copy of BEA's annual flat file), each type's price over the production wage, 1959-2024.
#   2. Whose pay pulled away from the production wage? BLS's hourly earnings of production and nonsupervisory employees
#      by industry (CES, via FRED, 1964-2024), and BEA's wages and salaries per full-time equivalent employee by industry
#      (NIPA table 6.6D, all employees, 1998-2024).
# Then a rough accounting: if a type of service paid its industry's wage, how much of its price rise would that explain?
# Data only; no model. FRED files are fetched once into cache/ (as code/panel.py does).
# Run from us-record/:  python3 playground/services_skill.py
import csv
import os
import sys
import urllib.request

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
CACHE = os.path.join(ROOT, "cache")
NIPA = os.path.join(REPO, "progress_and_prosperity", "lambda", "data", "cache", "NipaDataA.txt")
REGISTER = os.path.join(os.path.dirname(NIPA), "SeriesRegister.txt")


def fred(sid, path=None):
    """Annual means over complete years of a FRED series, fetched once into cache/."""
    path = path or os.path.join(CACHE, f"{sid}.csv")
    if not os.path.exists(path):
        with urllib.request.urlopen(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", timeout=60) as r:
            data = r.read()
        if not data.startswith(b"observation_date"):
            sys.exit(f"{sid}: unexpected reply from FRED, not cached")
        open(path, "wb").write(data)
    s = pd.read_csv(path)
    s.columns = ["date", "value"]
    s["date"] = pd.to_datetime(s["date"])
    s["value"] = pd.to_numeric(s["value"], errors="coerce")
    s = s.dropna().set_index("date")["value"]
    g = s.groupby(s.index.year)
    return g.mean()[g.count() == 12]


def nipa(codes):
    """BEA NIPA annual series by code, from the flat file; each code's label checked against the register."""
    labels = {r[0]: r[1] for r in csv.reader(open(REGISTER, encoding="utf-8")) if r and not r[0].startswith("%")}
    out = {c: {} for c in codes}
    for r in csv.reader(open(NIPA, encoding="utf-8")):
        if r and r[0] in out and r[1].isdigit():
            out[r[0]][int(r[1])] = float(r[2].replace(",", ""))
    df = pd.DataFrame(out)
    return df, {c: labels.get(c) for c in codes}


def production_wage():
    """The panel's production wage: manufacturing's hourly earnings to 1964, then AHETPI, linked at 1964."""
    raw = os.path.join(REPO, "pinning", "effort", "data", "raw")
    man = fred("AHEMAN", os.path.join(raw, "AHEMAN.csv"))
    ahe = fred("AHETPI", os.path.join(raw, "AHETPI.csv"))
    return pd.concat([man.loc[:1964], ahe.loc[1965:] * (man.loc[1964] / ahe.loc[1964])])


# types of consumer services (BEA's lines; housing left out, as in the model), with a first guess at their skill
# (to be checked against pay below): "high" where the work is mostly done by professionals, "low" where it is mostly
# in-person work at low pay, "other" where the cost is mostly not labour (utilities, communication) or not a service
TYPES = {
    "DUTLRC": ("Household utilities", "other"),
    "DOUTRC": ("Outpatient care (physicians, dentists, paramedical)", "high"),
    "DHPNRC": ("Hospitals and nursing homes", "high"),
    "DMVSRC": ("Motor vehicle services (repair, leasing)", "low"),
    "DPUBRC": ("Public transportation", "low"),
    "DRCARC": ("Recreation services", "low"),
    "DFSERC": ("Food services", "low"),
    "DACCRC": ("Accommodations", "low"),
    "DFNLRC": ("Financial services", "high"),
    "DINSRC": ("Insurance", "high"),
    "DCOMRC": ("Communication", "other"),
    "DTEDRC": ("Education", "high"),
    "DPRSRC": ("Professional and other services", "high"),
    "DPERRC": ("Personal care and clothing services", "low"),
    "DSOCRC": ("Social services and religious activities", "low"),
    "DHHMRC": ("Household maintenance", "low"),
    "DNPIRC": ("Nonprofits' own consumption (NPISHs)", "other"),
}


def services_table(w):
    """Each type's share of consumer services less housing (1959, 2024) and its price over the production wage
    (1959 = 1), from BEA's current-dollar and price-index lines."""
    codes = list(TYPES) + [c[:-1] + "G" for c in TYPES] + ["DSERRC", "DHSGRC", "DSERRG", "DHSGRG"]
    df, labels = nipa(codes)
    for c in TYPES:
        assert labels[c] is not None and labels[c[:-1] + "G"] is not None, c
    total = df["DSERRC"] - df["DHSGRC"]
    rows = []
    for c, (name, skill) in TYPES.items():
        p = df[c[:-1] + "G"].dropna()
        y0 = max(1959, int(p.index.min()))
        rel = (p / w.reindex(p.index)).dropna()
        rows.append(dict(code=c, type=name, skill=skill, first=y0,
                         share_1959=df.loc[1959, c] / total.loc[1959], share_2024=df.loc[2024, c] / total.loc[2024],
                         price_over_wage_2024=rel.loc[2024] / rel.loc[y0],
                         rate=100 * np.log(rel.loc[2024] / rel.loc[y0]) / (2024 - y0)))
    t = pd.DataFrame(rows)
    covered = t["share_2024"].sum()
    return t, covered, df


def group_price(df, w, skill):
    """A Tornqvist index of the types in a skill group, over the production wage, 1959 = 1."""
    cs = [c for c, (_, s) in TYPES.items() if s == skill]
    years = list(range(1959, 2025))
    sh = df.loc[years, cs]
    sh = sh.div(sh.sum(axis=1), axis=0)
    lp = np.log(df.loc[years, [c[:-1] + "G" for c in cs]].values)
    dl = np.diff(lp, axis=0)
    wb = 0.5 * (sh.values[1:] + sh.values[:-1])
    idx = np.exp(np.concatenate([[0.0], np.cumsum((wb * dl).sum(axis=1))]))
    s = pd.Series(idx, index=years)
    return s / w.loc[years] * w.loc[1959]


# BLS: hourly earnings of production and nonsupervisory employees by industry (supersectors), and all employees
CES = {"CES3000000008": ("Manufacturing", "MANEMP"), "CES3100000008": ("  durable goods", None),
       "CES3200000008": ("  nondurable goods", None), "CES4200000008": ("Retail trade", "USTRADE"),
       "CES4300000008": ("Transportation and warehousing", "CES4300000001"), "CES5000000008": ("Information", "USINFO"),
       "CES5500000008": ("Financial activities", "USFIRE"), "CES6000000008": ("Professional and business services", "USPBS"),
       "CES6500000008": ("Education and health services", "USEHS"),
       "CES7000000008": ("Leisure and hospitality", "USLAH"), "CES8000000008": ("Other services", "USSERV")}

# each type's workers, as BLS's industries (production and nonsupervisory employees' hourly earnings): health, education
# and social services in education and health services; professional services in professional and business services;
# finance and insurance in financial activities; meals, rooms and recreation in leisure and hospitality; personal care,
# household maintenance and vehicle repair in other services; public transportation in transportation (from 1972)
PAY = {"DOUTRC": "CES6500000008", "DHPNRC": "CES6500000008", "DTEDRC": "CES6500000008", "DSOCRC": "CES6500000008",
       "DPRSRC": "CES6000000008", "DFNLRC": "CES5500000008", "DINSRC": "CES5500000008", "DFSERC": "CES7000000008",
       "DACCRC": "CES7000000008", "DRCARC": "CES7000000008", "DPERRC": "CES8000000008", "DHHMRC": "CES8000000008",
       "DMVSRC": "CES8000000008", "DPUBRC": "CES4300000008"}


def price_and_pay(df, w, ahe, codes, y0):
    """For a group of types from y0 (= 1): its price over the production wage, its industries' pay over the production
    wage (BLS hourly earnings over AHETPI), and its price over its own pay; Tornqvist over the types on spending shares."""
    years = list(range(y0, 2025))
    sh = df.loc[years, codes]
    sh = sh.div(sh.sum(axis=1), axis=0)
    wb = 0.5 * (sh.values[1:] + sh.values[:-1])
    lp = np.log(df.loc[years, [c[:-1] + "G" for c in codes]].values) - np.log(w.loc[years].values)[:, None]
    lw = np.log(np.column_stack([(fred(PAY[c]) / ahe).loc[years].values for c in codes]))
    price = np.exp(np.concatenate([[0.0], np.cumsum((wb * np.diff(lp, axis=0)).sum(axis=1))]))
    pay = np.exp(np.concatenate([[0.0], np.cumsum((wb * np.diff(lw, axis=0)).sum(axis=1))]))
    return pd.DataFrame(dict(price=price, pay=pay, own=price / pay), index=years)


# BEA table 6.6D: wages and salaries per full-time equivalent employee, by industry (all employees), 1998-
FTE = {"A4403C": "Private industries", "N4413C": "Manufacturing", "N4438C": "Retail trade",
       "N4457C": "Finance and insurance", "N4465C": "Professional, scientific, and technical services",
       "N4473C": "Educational services", "N4475C": "Ambulatory health care services", "N4490C": "Hospitals",
       "N4491C": "Nursing and residential care facilities", "N4492C": "Social assistance",
       "N4493C": "Arts, entertainment, and recreation", "N4497C": "Accommodation",
       "N4498C": "Food services and drinking places", "N4499C": "Other services, except government"}


if __name__ == "__main__":
    w = production_wage()
    t, covered, df = services_table(w)
    pd.set_option("display.width", 200)
    print("1. Consumer services less housing by type (BEA). Price over the production wage, first year = 1.")
    print(f"   the types cover {covered:.1%} of services less housing in 2024 (the rest: net foreign travel)")
    for skill in ("high", "low", "other"):
        s = t[t.skill == skill].sort_values("share_2024", ascending=False)
        print(f"   -- {skill}: {s.share_1959.sum():.0%} of services less housing in 1959, {s.share_2024.sum():.0%} in 2024")
        for _, r in s.iterrows():
            print(f"      {r.type:52s} {r.share_1959:6.1%} -> {r.share_2024:6.1%}   x{r.price_over_wage_2024:5.2f} "
                  f"({r.rate:+.2f}%/yr from {r['first']})")
    groups = {sk: group_price(df, w, sk) for sk in ("high", "low", "other")}
    print("   groups, Tornqvist over their types, price over the production wage (1959 = 1):")
    for sk, s in groups.items():
        marks = " ".join(f"{y} {s.loc[y]:.2f}" for y in (1973, 1990, 2000, 2010, 2024))
        print(f"      {sk:5s} {marks}")

    print("\n2. Price, pay and price over own pay by group (BLS pay by industry from 1964; transportation from 1972)")
    ahe = fred("AHETPI", os.path.join(REPO, "pinning", "effort", "data", "raw", "AHETPI.csv"))
    hi = [c for c, (_, s) in TYPES.items() if s == "high"]
    lo = [c for c, (_, s) in TYPES.items() if s == "low"]
    rows = []
    for name, codes, y0 in (("high", hi, 1964), ("low", lo, 1972), ("low less public transportation", [c for c in lo if c != "DPUBRC"], 1964),
                            ("health care", ["DOUTRC", "DHPNRC"], 1964), ("education", ["DTEDRC"], 1964)):
        g = price_and_pay(df, w, ahe, codes, y0)
        print(f"   {name} ({y0} = 1)")
        for col, lab in (("price", "price over the production wage"), ("pay", "its industries' pay over it"),
                         ("own", "price over its own pay")):
            print(f"      {lab:32s} " + " ".join(f"{y} {g.loc[y, col]:.2f}" for y in (y0, 1973, 1980, 1990, 2000, 2010, 2024) if y >= y0))
        rows.append(g.assign(group=name).reset_index().rename(columns={"index": "year"}))
    pd.concat(rows).to_csv(os.path.join(ROOT, "playground", "services_skill.csv"), index=False)

    print("\n3a. BLS hourly earnings, production and nonsupervisory employees, over the total private (AHETPI)")
    priv = fred("USPRIV")
    for sid, (name, emp) in CES.items():
        e = fred(sid)
        y0 = 1964 if 1964 in e.index else int(e.index.min())
        r0, r1 = e.loc[y0] / ahe.loc[y0], e.loc[2024] / ahe.loc[2024]
        sh = ""
        if emp:
            n = fred(emp)
            sh = f"   share of private jobs {n.loc[y0] / priv.loc[y0]:5.1%} -> {n.loc[2024] / priv.loc[2024]:5.1%}"
        print(f"    {name:38s} {y0} {r0:5.2f} -> 2024 {r1:5.2f}{sh}")

    print("\n3b. BEA wages and salaries per full-time equivalent employee (all employees), over private industries")
    f, labels = nipa(list(FTE))
    for c, name in FTE.items():
        assert labels[c] == name.strip(), (c, labels[c])
    for c, name in FTE.items():
        r = f[c] / f["A4403C"]
        print(f"    {name:52s} 1998 {r.loc[1998]:5.2f} -> 2024 {r.loc[2024]:5.2f}   ({100 * np.log(f.loc[2024, c] / f.loc[1998, c]) / 26:+.2f}%/yr nominal)")
