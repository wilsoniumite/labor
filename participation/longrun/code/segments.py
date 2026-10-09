# segments.py — 'a splice is a fixed effect' (PROTOCOL L7): the segment table and the segment dummies.
#
# data/segments.csv (geo, series, tau, reason, citation) = the rows transcribed from documentation, by hand, in
# data/segments_documented.csv, plus the source switches of q that the L6 ladder makes (rung 1 to rung 2, DF_PRICES_ALL
# to DF_PRICES_C2018_ALL), computed from the availability probes by coverage.q_ladder. It is frozen at the L-freeze.
# Each row says: from observation year tau on (for q: from q year tau, so from observation year tau + 1 for the lagged
# regressor, C3's rule), country geo's series is a new segment. Series:
#   lfs        every DF_LFS_INDIC series of the country (the activity cells, A2534, A5564, AW/AM 25-54, U 25-54)
#   lfs_A5564  the 55-64 cells only
#   q          the rent-over-CPI regressor (JST rung 1 or RPI/CPI rung 2)
#   q_hpi      the house-price robustness regressor
#   school     ILOSTAT school attendance 20-24 (C-6L)
#   coresid    census coresidence 25-34 (LR-C1, Extract B; the RELATE-scheme rows come with the L2 sample records)
#   us_cps, us_q, us_coresid, us_enrol   the US deep study's series (section 6)
# Transcription rules (the agent that compiled the documented rows had seen no long-run value):
#   - OECD LFSNOTES_SOURCES.pdf Table 6 rows that concern the survey itself (new or continuous survey, questionnaire,
#     survey period), the population covered (age limits, armed forces, territory) or the classification of labour
#     force status (employment, unemployment, family workers), and Table 1's dated changes of survey period or
#     coverage. Rows confined to another named series (hours, duration, part-time, discouraged or marginally attached
#     workers, temporary workers, job tenure) are not segments of participation or unemployment rates. A row 'a/b'
#     starts the new segment in year b. Rows that concern 2020 alone (a dropped year) are not transcribed. Rows of a
#     European member after 1996 are not transcribed (no observation year can carry them, L1).
#   - The US (L7 'the BLS and Census notes'): BLS's changes in concepts and methods, territorial changes, and each new
#     decennial-census population base at the first year whose published data rest on it (revisions back counted);
#     the intercensal annual population-control adjustments are not segments. OECD Table 6's US rows are added.
#   - JST/RORE: every change of rent-index source after 1949 in the RORE per-country source tables, every stretch the
#     documentation says was rescaled or extrapolated (its first year, and the year after it ends), and R6's 2016-2020
#     extension. No territorial change for Germany is named in the JST R6 documentation (searched: 'West Germany',
#     'reunif', 'unification', 'territor', 'border'), so none is transcribed (L7's conditional).
# Rules applied when values arrive (build.py), not rows of this table: OECD OBS_STATUS B (a segment from that year,
# C3/L7); a change of ILOSTAT 'source' code within a country (a source switch, L7). A documented break found after the
# freeze goes to data/segments_postfreeze.csv and enters only the no-verdict run 'with post-freeze segments' (section 8).
#
# Run from longrun/:  ../../venv/Scripts/python.exe code/segments.py   (writes data/segments.csv; needs the probes)

from __future__ import annotations

import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch  # noqa: E402

DOCUMENTED = os.path.join(LROOT, "data", "segments_documented.csv")
TABLE = os.path.join(LROOT, "data", "segments.csv")
POST = os.path.join(LROOT, "data", "segments_postfreeze.csv")
SERIES = {"lfs", "lfs_A5564", "q", "q_hpi", "school", "coresid", "us_cps", "us_q", "us_coresid", "us_enrol"}
COLUMNS = ["geo", "series", "tau", "reason", "citation"]
# Which segment series each panel variable carries (outcome, regressor, controls).
VARIABLE_SERIES = {"A2534": ["lfs"], "A2534_M": ["lfs"], "A2534_F": ["lfs"], "A5564": ["lfs", "lfs_A5564"],
                   "AW2554": ["lfs"], "AM2554": ["lfs"], "U": ["lfs"], "logq_l1": ["q"], "logq_hpi_l1": ["q_hpi"],
                   "school2024": ["school"], "R": ["coresid"]}
LAGGED = {"logq_l1", "logq_hpi_l1"}


def validate(df: pd.DataFrame) -> list[str]:
    """Problems with a segment table (empty list if none)."""
    bad = []
    if list(df.columns) != COLUMNS:
        bad.append(f"columns {list(df.columns)} != {COLUMNS}")
        return bad
    for i, r in df.iterrows():
        if r["geo"] not in fetch.ISO3:
            bad.append(f"row {i}: geo {r['geo']!r} is not a member")
        if r["series"] not in SERIES:
            bad.append(f"row {i}: series {r['series']!r}")
        try:
            t = int(r["tau"])
            if not 1940 <= t <= 2030:
                bad.append(f"row {i}: tau {t}")
        except (TypeError, ValueError):
            bad.append(f"row {i}: tau {r['tau']!r}")
        if not str(r["reason"]).strip() or not str(r["citation"]).strip() or str(r["citation"]) == "nan":
            bad.append(f"row {i}: a reason and a citation are required")
    if df.duplicated(["geo", "series", "tau"]).any():
        bad.append("duplicate (geo, series, tau) rows")
    return bad


def load(path: str = TABLE, post_freeze: bool = False) -> pd.DataFrame:
    """The frozen segment table (plus the post-freeze rows when asked: the no-verdict run only)."""
    df = pd.read_csv(path, dtype={"tau": int}, keep_default_na=False)
    bad = validate(df)
    if bad:
        raise ValueError("segments table: " + "; ".join(bad[:5]))
    if post_freeze and os.path.exists(POST):
        extra = pd.read_csv(POST, dtype={"tau": int}, keep_default_na=False)
        if validate(extra):
            raise ValueError("post-freeze segments table: " + "; ".join(validate(extra)[:5]))
        df = pd.concat([df, extra], ignore_index=True).drop_duplicates(["geo", "series", "tau"])
    return df


def has_post_freeze() -> bool:
    return os.path.exists(POST) and len(pd.read_csv(POST)) > 0


def ladder_switches() -> pd.DataFrame:
    """The q source switches of the L6 ladder, from the availability probes (coverage.q_ladder)."""
    import coverage as cv
    raw = json.load(open(os.path.join(LROOT, "data", "coverage_probes.json"), encoding="utf-8"))["available"]
    rows = []
    for c in fetch.COUNTRIES:
        lad = cv.q_ladder(c, cv.cube_for(c, raw))
        ys = sorted(lad)
        for a, b in zip(ys[:-1], ys[1:]):
            if lad[a] != lad[b]:
                rows.append(dict(geo=c, series="q", tau=b, reason=f"source switch: {lad[a]} to {lad[b]} (L6 ladder)",
                                 citation="PROTOCOL L6 and L7 (every source switch); OECD availability probes, "
                                          "data/coverage_probes.json"))
    return pd.DataFrame(rows, columns=COLUMNS)


def build() -> pd.DataFrame:
    doc = pd.read_csv(DOCUMENTED, dtype={"tau": int}, keep_default_na=False)
    bad = validate(doc)
    if bad:
        raise ValueError("documented segments: " + "; ".join(bad[:5]))
    sw = ladder_switches()
    sw = sw[~sw.set_index(["geo", "series", "tau"]).index.isin(doc.set_index(["geo", "series", "tau"]).index)]
    out = pd.concat([doc, sw], ignore_index=True).sort_values(["geo", "series", "tau"]).reset_index(drop=True)
    bad = validate(out)
    if bad:
        raise ValueError("; ".join(bad[:5]))
    return out


def breaks(seg: pd.DataFrame, geos, variables) -> list[tuple[str, int]]:
    """(geo, tau) for every segment start of every series the regression's variables carry; a lagged regressor's
    segment starting in q year tau acts from observation year tau + 1 (C3)."""
    out = set()
    geos = set(geos)
    for v in variables:
        shift = 1 if v in LAGGED else 0
        for s in VARIABLE_SERIES.get(v, []):
            d = seg[(seg["series"] == s) & seg["geo"].isin(geos)]
            out.update((g, int(t) + shift) for g, t in zip(d["geo"], d["tau"]))
    return sorted(out)


def main() -> None:
    out = build()
    out.to_csv(TABLE, index=False, lineterminator="\n")
    print(f"{len(out)} segment rows ({(out['citation'].str.startswith('PROTOCOL L6')).sum()} ladder switches); "
          f"wrote {TABLE}")


if __name__ == "__main__":
    main()
