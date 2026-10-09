# ipums.py — the guarded reader of her IPUMS-International extracts (PROTOCOL L9, L10, L14). The only reader.
#
# She makes the extract(s) after the participation-L-freeze tag and puts them in longrun/data/ipums/ (gitignored): for
# each extract, one rectangular person-level CSV (optionally .gz) and its DDI codebook (.xml) with the same file stem
# (Extract A and, if she makes it, Extract B may be one extract or two). Nothing else reads that folder.
# Refusals, before any row is used:
#   - the half must be open (fetch.allowed_countries: explore after the L tag, confirm after the LE tag);
#   - the file may hold only her variables (COUNTRY YEAR SAMPLE SERIAL PERNUM HHWT PERWT AGE SEX RELATE MOMLOC POPLOC
#     GQ), RELATED (the detailed RELATE IPUMS delivers with it), the technical variables the extract builder preselects
#     and the data-quality flags IPUMS attaches to listed variables (TECHNICAL and FLAGS below; their exact names are
#     confirmed at L2 against the extract builder, PROTOCOL L9). Any labour, education, income, marital-status or tenure
#     variable, or any other column, makes the loader refuse the file;
#   - samples: the frozen list (data/ipums_samples.json as committed in the L tag); an extract whose DDI lists any
#     SAMPLE outside that list is refused whole; a sample the purpose does not use is never read, and a sample of a
#     country outside the open half is never read (row-level guard: rows are filtered on SAMPLE in each chunk, before
#     any other column is converted); a row read with AGE outside 20-34 (the case selection of L9) refuses the extract;
#   - an unguarded copy: while any IPUMS microdata or codebook file lies under longrun/ outside data/ipums/, the
#     loader refuses (stray_microdata()).
# Purposes: 'F_L' (the earliest frozen sample with RELATE per country), 'F_L_1970' (the sample nearest 1970, for the
# robustness run), 'pointer' (the F_L samples organised into households: MOMLOC/POPLOC against RELATE), 'extract_B'
# (LR-C1's censuses 1976+; only if she makes Extract B).
# The measure (L9): the share of persons aged 25-34 (or 20-29) living with a parent = RELATE general code 3 (child of
# the head, every detailed code under it), weighted by PERWT, for men and women separately, F_L = their equal-weight
# mean, in percent. Excluded: persons in group quarters (a GQ code whose DDI label names group quarters or an
# institution); RELATE unknown (a code whose DDI label says unknown), from numerator and denominator. Grouped ages: the
# sample record's age intervals (recorded at L2 from the codebook) select by interval; intervals that do not align with
# the band drop that measure only, and a grouped sample with no recorded intervals is unusable for both bands (that
# sample only, with the reason 'no L2 record of its age intervals'). Reported per sample: n, the unknown share, the share of each combined detailed child
# code, and the flags of the frozen record. An unusable sample (no RELATE, no PERWT, no cases in the band) gives NaN
# with the reason: the mechanical drop of L9.
# Library module; F_L(half) also writes the F_L record to the fetch log (fetch.record), which opens the outcome doors.

from __future__ import annotations

import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch  # noqa: E402

SAMPLES = os.path.join(LROOT, "data", "ipums_samples.json")
HER_VARS = ["COUNTRY", "YEAR", "SAMPLE", "SERIAL", "PERNUM", "HHWT", "PERWT", "AGE", "SEX", "RELATE", "MOMLOC",
            "POPLOC", "GQ"]
DETAILED = ["RELATED"]
TECHNICAL = ["CNTRY"]                                   # provisional: confirmed at L2 against the extract builder
FLAGS = ["QAGE", "QSEX", "QRELATE", "QGQ", "QMOMLOC", "QPOPLOC", "MOMRULE", "POPRULE", "STEPMOM", "STEPPOP",
         "PARRULE"]                                      # attached automatically with listed variables (L2 confirms)
ALLOWED = set(HER_VARS) | set(DETAILED) | set(TECHNICAL) | set(FLAGS)
FORBIDDEN_STEMS = ("EMP", "LAB", "OCC", "IND", "CLASSW", "EDU", "SCHOOL", "LIT", "YRSCH", "INC", "MARST", "OWN",
                   "TENURE", "HRS", "WRK")
PURPOSES = ("F_L", "F_L_1970", "pointer", "extract_B")
CHUNK = 200_000


class ExtractError(Exception):
    """The extract is not what the protocol allows (a refusal, not a data problem)."""


# ---------------------------------------------------------------- the frozen sample list

def frozen_samples() -> dict:
    """data/ipums_samples.json as committed in the L-freeze tag (the working copy must agree)."""
    l_sha = fetch._tag_sha(fetch.L_FREEZE)
    rc, out = fetch._git("show", f"{l_sha}:./data/ipums_samples.json")
    if rc != 0:
        raise fetch.BlindingError("data/ipums_samples.json is not in the L-freeze commit: the sample list is frozen")
    frozen = json.loads(out)
    if os.path.exists(SAMPLES) and json.load(open(SAMPLES, encoding="utf-8")) != frozen:
        raise fetch.BlindingError("data/ipums_samples.json differs from its frozen copy")
    return frozen


def samples_for(purpose: str, smp: dict, countries: set[str]) -> list[dict]:
    """The frozen sample records a purpose reads, for these countries."""
    if purpose not in PURPOSES:
        raise ExtractError(f"purpose {purpose!r} not in {PURPOSES}")
    recs = {r["sample"]: r for r in smp["F_L"] + smp["extract_B"]}
    if purpose in ("F_L", "F_L_1970"):
        ids = [v[purpose] for c, v in smp["roles"].items() if c in countries and purpose in v]
    elif purpose == "pointer":
        ids = [v["F_L"] for c, v in smp["roles"].items() if c in countries and recs[v["F_L"]]["households"]]
    else:
        ids = [r["sample"] for r in smp["extract_B"] if r["country"] in countries and r["relate"]]
    return [recs[i] for i in sorted(ids)]


# ---------------------------------------------------------------- the files

MICRODATA = re.compile(r"(ipums.*\.(csv|dat)(\.gz)?|ipums.*\.xml|.*\.dat(\.gz)?)$", re.I)


def stray_microdata(root: str | None = None) -> list[str]:
    """IPUMS microdata or codebook files under longrun/ outside data/ipums/ (relative paths). Any such file is an
    unguarded copy of regressor and holdout values (PROTOCOL L9, L14)."""
    root = root or fetch.LROOT
    inside = os.path.normcase(os.path.abspath(fetch.IPUMS_DIR))
    out = []
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x not in (".git", "__pycache__")]
        if os.path.normcase(os.path.abspath(d)).startswith(inside):
            continue
        for f in fs:
            if MICRODATA.match(f):
                out.append(os.path.relpath(os.path.join(d, f), root).replace("\\", "/"))
    return sorted(out)


def files() -> list[tuple[str, str]]:
    """[(extract CSV, its DDI)] in data/ipums/: every CSV needs the DDI with its file stem, and every DDI its CSV."""
    stray = stray_microdata()
    if stray:
        raise fetch.BlindingError(f"IPUMS microdata outside longrun/data/ipums/ ({stray}): an unguarded copy; move it "
                                  "out of the repository before any extract is read")
    data = sorted(glob.glob(os.path.join(fetch.IPUMS_DIR, "*.csv")) + glob.glob(os.path.join(fetch.IPUMS_DIR, "*.csv.gz")))
    ddi = sorted(glob.glob(os.path.join(fetch.IPUMS_DIR, "*.xml")))

    def stem(f):
        b = os.path.basename(f)
        for ext in (".csv.gz", ".csv", ".xml"):
            if b.lower().endswith(ext):
                return b[: -len(ext)]
        return b
    by = {stem(x): x for x in ddi}
    pairs = [(f, by.get(stem(f))) for f in data]
    if not data or any(x is None for _, x in pairs) or len(ddi) != len(data):
        raise ExtractError(f"longrun/data/ipums/ must hold extract CSVs, each with the DDI XML of its file stem (found "
                           f"{len(data)} CSV and {len(ddi)} DDI)")
    return pairs


def check_columns(cols) -> None:
    cols = [str(c).strip().upper() for c in cols]
    extra = sorted(set(cols) - ALLOWED)
    if extra:
        raise ExtractError(f"the extract holds variables the protocol does not allow: {extra} (PROTOCOL L9: no labour, "
                           "education, income, marital-status or tenure variable; anything else unlisted is refused)")
    bad = [c for c in cols if c.startswith(FORBIDDEN_STEMS) and c not in ALLOWED]
    if bad:
        raise ExtractError(f"forbidden variables {bad}")
    missing = sorted(set(HER_VARS) - set(cols) - {"MOMLOC", "POPLOC"})
    if missing:
        raise ExtractError(f"the extract lacks {missing}")


def ddi_categories(path: str) -> dict[str, dict[int, str]]:
    """{variable: {code: label}} from the DDI codebook."""
    root = ET.parse(path).getroot()
    out: dict = {}
    for var in root.iter():
        if not var.tag.endswith("var"):
            continue
        name = (var.get("name") or "").upper()
        cats = {}
        for cat in var:
            if not cat.tag.endswith("catgry"):
                continue
            val = lab = None
            for ch in cat:
                if ch.tag.endswith("catValu"):
                    val = (ch.text or "").strip()
                elif ch.tag.endswith("labl"):
                    lab = (ch.text or "").strip()
            if val is not None and re.fullmatch(r"-?\d+", val):
                cats[int(val)] = lab or ""
        if name:
            out[name] = cats
    return out


def sample_codes(cats: dict, recs: list[dict]) -> dict[int, dict]:
    """SAMPLE code -> frozen record, matched on the DDI label (e.g. 'United States 1960') against the record's title."""
    out = {}
    for code, lab in cats.get("SAMPLE", {}).items():
        for r in recs:
            if lab.strip().lower().startswith(r["title"].strip().lower()):
                out[code] = r
    return out


def frozen_titles(smp: dict) -> list[str]:
    return [r["title"].strip().lower() for r in smp["F_L"] + smp["extract_B"] if r.get("title")]


def read_rows(half: str, purpose: str) -> tuple[pd.DataFrame, dict, list[dict]]:
    """The rows of the samples this purpose uses, for the open half's countries only (row-level guard)."""
    allowed = fetch.allowed_countries(half)                 # BlindingError if the half is closed
    smp = frozen_samples()
    recs = samples_for(purpose, smp, allowed)
    titles = frozen_titles(smp)
    parts, cats_all, found = [], {}, set()
    for path, ddi in files():
        cats = ddi_categories(ddi)
        extra = sorted(lab for lab in cats.get("SAMPLE", {}).values()
                       if not any(lab.strip().lower().startswith(t) for t in titles))
        if extra:
            raise ExtractError(f"{os.path.basename(ddi)} lists samples outside the frozen list: {extra[:5]} (L9: exactly "
                               "the frozen sample IDs)")
        codes = sample_codes(cats, recs)
        found |= {r["sample"] for r in codes.values()}
        header = pd.read_csv(path, nrows=0).columns
        check_columns(header)
        for chunk in pd.read_csv(path, chunksize=CHUNK, dtype=str):
            chunk.columns = [c.upper() for c in chunk.columns]
            s_ = pd.to_numeric(chunk["SAMPLE"], errors="coerce")
            keep = s_.isin(list(codes))
            if keep.any():
                part = chunk[keep].copy()
                age = pd.to_numeric(part["AGE"], errors="coerce")
                if (~age.between(20, 34)).any():
                    raise ExtractError(f"{os.path.basename(path)} holds persons outside ages 20-34 (L9's case "
                                       "selection): the extract must be re-made")
                part["sample_id"] = s_[keep].map({k: v["sample"] for k, v in codes.items()})
                part["geo"] = s_[keep].map({k: v["country"] for k, v in codes.items()})
                parts.append(part)
        for v, cs in cats.items():
            cats_all.setdefault(v, {}).update(cs)
    missing = sorted({r["sample"] for r in recs} - found)
    rows = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=HER_VARS + ["sample_id", "geo"])
    for c in rows.columns:
        if c not in ("sample_id", "geo"):
            rows[c] = pd.to_numeric(rows[c], errors="coerce")
    return rows, {"categories": cats_all, "missing_samples": missing}, recs


# ---------------------------------------------------------------- the measure

def _codes_like(cats: dict, var: str, words) -> set[int]:
    return {k for k, v in cats.get(var, {}).items() if any(w in v.lower() for w in words)}


def band_mask(age: pd.Series, rec: dict, lo: int, hi: int) -> pd.Series | None:
    """Persons in [lo, hi]; for a grouped-age sample, by the recorded intervals (None if they do not align)."""
    if not rec.get("grouped_age"):
        return age.between(lo, hi)
    iv = rec.get("age_intervals")
    if not iv:
        return None                                       # no L2 record: unusable, this sample only (see share)
    inside = [(a, b) for a, b in iv if a >= lo and b <= hi]
    if sum(b - a + 1 for a, b in inside) != hi - lo + 1:
        return None
    m = pd.Series(False, index=age.index)
    for a, b in inside:
        m |= age.between(a, b)
    return m


def share(rows: pd.DataFrame, rec: dict, cats: dict, lo: int, hi: int) -> dict:
    """The coresidence share (percent) for one sample and one age band, by sex and their equal-weight mean."""
    d = rows[rows["sample_id"] == rec["sample"]]
    out = {"sample": rec["sample"], "year": rec["year"], "band": f"{lo}-{hi}", "flags": rec.get("flags", [])}
    if not len(d) or d["RELATE"].isna().all():
        return {**out, "value": np.nan, "unusable": "no RELATE"}
    if "PERWT" not in d or d["PERWT"].isna().all():
        return {**out, "value": np.nan, "unusable": "no PERWT"}
    gq_out = _codes_like(cats, "GQ", ("group quarters", "institution"))
    gq_out -= _codes_like(cats, "GQ", ("household",))     # 'households' and split 1-person units stay
    unknown = _codes_like(cats, "RELATE", ("unknown",))
    child = {k for k, v in cats.get("RELATE", {}).items() if "child" in v.lower()}
    if 3 not in child:
        raise ExtractError("RELATE general code 3 is not 'child' in the DDI")
    m = band_mask(d["AGE"], rec, lo, hi)
    if m is None:
        why = ("no L2 record of its age intervals" if rec.get("grouped_age") and not rec.get("age_intervals")
               else f"age intervals do not align with {lo}-{hi}")
        return {**out, "value": np.nan, "unusable": why}
    d = d[m]
    if "GQ" in d and gq_out:
        d = d[~d["GQ"].isin(gq_out)]
    n_all = float(d["PERWT"].sum())
    unk = d["RELATE"].isin(unknown)
    out["share_relate_unknown"] = float(d.loc[unk, "PERWT"].sum() / n_all) if n_all else np.nan
    d = d[~unk]
    if not len(d):
        return {**out, "value": np.nan, "unusable": f"no cases aged {lo}-{hi}"}
    by_sex = {}
    for sx, lab in ((1, "M"), (2, "F")):
        e = d[d["SEX"] == sx]
        w = float(e["PERWT"].sum())
        by_sex[lab] = 100.0 * float(e.loc[e["RELATE"] == 3, "PERWT"].sum()) / w if w > 0 else np.nan
    comb = {}
    if "RELATED" in d:
        labs = cats.get("RELATED", {})
        for code, lab in labs.items():
            if 3000 <= code < 4000 and "/" in lab:
                comb[lab] = float(d.loc[d["RELATED"] == code, "PERWT"].sum() / d["PERWT"].sum())
    return {**out, "value": float(np.nanmean([by_sex["M"], by_sex["F"]])) if all(np.isfinite(list(by_sex.values())))
            else np.nan, "men": by_sex["M"], "women": by_sex["F"], "n": int(len(d)), "combined_child_codes": comb}


def F_L(half: str, purpose: str = "F_L", record: bool = True) -> dict:
    """{country: {'25-34': {...}, '20-29': {...}}} for the open half; writes the F_L record (L14) for purpose F_L."""
    rows, meta, recs = read_rows(half, purpose)
    out = {}
    for rec in recs:
        out[rec["country"]] = {"25-34": share(rows, rec, meta["categories"], 25, 34),
                               "20-29": share(rows, rec, meta["categories"], 20, 29)}
    if meta["missing_samples"]:
        for s in meta["missing_samples"]:
            c = next(r["country"] for r in recs if r["sample"] == s)
            out[c] = {"25-34": {"sample": s, "value": np.nan, "unusable": "sample not in the extract"},
                      "20-29": {"sample": s, "value": np.nan, "unusable": "sample not in the extract"}}
    if record and purpose == "F_L":
        fetch.record("F_L", half, {c: {k: (None if not np.isfinite(v.get("value", np.nan)) else round(v["value"], 6))
                                       for k, v in d.items()} for c, d in out.items()}, by=fetch.F_L_BY)
    return out


def pointer_check(half: str) -> dict:
    """No verdict: the share of 25-34 with a coresident parent by MOMLOC/POPLOC against the RELATE share."""
    rows, meta, recs = read_rows(half, "pointer")
    out = {}
    for rec in recs:
        d = rows[(rows["sample_id"] == rec["sample"]) & rows["AGE"].between(25, 34)]
        if not len(d) or "MOMLOC" not in d:
            continue
        w = d["PERWT"]
        ptr = ((d["MOMLOC"].fillna(0) > 0) | (d["POPLOC"].fillna(0) > 0)).astype(float)
        out[rec["country"]] = {"sample": rec["sample"], "pointer_share": float(100 * (ptr * w).sum() / w.sum()),
                               "relate_share": float(100 * ((d["RELATE"] == 3) * w).sum() / w.sum())}
    return out


def extract_b(half: str) -> pd.DataFrame:
    """LR-C1's outcome R_cy (percent, sexes equal-weighted) at each Extract B census of the open half."""
    rows, meta, recs = read_rows(half, "extract_B")
    out = [dict(geo=r["country"], year=r["year"], sample=r["sample"],
                R=share(rows, r, meta["categories"], 25, 34)["value"]) for r in recs]
    return pd.DataFrame(out, columns=["geo", "year", "sample", "R"])


__all__ = ["F_L", "pointer_check", "extract_b", "check_columns", "ExtractError", "ALLOWED", "samples_for",
           "stray_microdata", "files"]
