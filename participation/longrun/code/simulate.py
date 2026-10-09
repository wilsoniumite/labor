# simulate.py — the whole long-run pipeline end to end on SYNTHETIC data, before any value is downloaded: the guarded
# doors (fetch.py) are kept, but the network is replaced by a synthetic world that answers in the real schemas (SDMX-CSV
# long frames for the OECD flows, the JST columns, ILOSTAT rows, WPP rows, a synthetic IPUMS extract CSV with its DDI
# codebook), and the freeze tags are simulated by a fake git (fetch._git). Coverage follows data/coverage.json (the
# probes), so the synthetic panel has the real holes, seams and memberships.
#
# Each world: log q by the L6 ladder (JST rows for the JST countries' documented years, RPI/CPI elsewhere and as
# extensions), one OBS_STATUS B flag inside one rung-2 country's q years, one interpolated JST year; U AR(1); F_L from
# the synthetic census shares (25-34 children of the head) of the frozen F_L samples (grouped-age samples get recorded
# intervals, as L2 will record them); activity cells whose 25-34 mean carries the planted effects through the basis the
# pipeline itself computes from q (stage 1, q first), so the world plants exactly what the test measures:
#   null      no effect of q;
#   planted   DiD = -40 points per log unit of q (high floor: the top-tercile slope falls by 40 relative to the bottom
#             one, to below zero), the model's case with the drop condition; LR-Y0's bottom slope +20; school on U +2.0
#             (effects well above the skeleton's MDEs, so the run checks plumbing, not power);
#   opposite  DiD = +40.
# The worlds have no country trends (the skeleton simulation is where size under trends is measured). A synthetic
# Kholodilin coding covers a few countries (strict control in their early years), so the strict-control robustness
# rows, the control-era qualifier and the list of uncovered countries run as they will at the look. The fake git
# answers as a ready freeze would (production skeleton, filled forecast sheets, a European run, segments, the scouts'
# move recorded), so the guard's readiness and pinning checks run too; q downloads are logged as the real doors log
# them, so L14's order guard runs on the same evidence.
# The run: the explore opening (opening.open_half('explore')), then confirm.look() (all tags simulated), at B = 999 and
# RI exact; the result files go to a temporary folder. Recorded for the checks: the verdicts, the model-level and joint
# readings, the order of the fetch-log records against the outcome fetches, every door call, the knots kept for the
# explore countries, and that nothing reached the network.
#
# Run from longrun/:  ../../venv/Scripts/python.exe code/simulate.py
# Out: results/simulate.json

from __future__ import annotations

import gzip
import hashlib
import io
import json
import math
import os
import shutil
import socket
import sys
import tempfile
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402
import confirm  # noqa: E402
import coverage as cv  # noqa: E402
import fetch  # noqa: E402
import ipums  # noqa: E402
import opening  # noqa: E402
import specs  # noqa: E402

OUT = os.path.join(LROOT, "results", "simulate.json")
SEED = 20261009
WORLDS = {"null": dict(DiD=0.0, g1=0.0, school=0.0),
          "planted": dict(DiD=-40.0, g1=20.0, school=2.0),
          "opposite": dict(DiD=40.0, g1=20.0, school=2.0)}
IPUMS_ISO_NUM = {"AT": 40, "CA": 124, "CH": 756, "CL": 152, "CO": 170, "CR": 188, "DE": 276, "FR": 250, "EL": 300,
                 "HU": 348, "IE": 372, "IL": 376, "MX": 484, "NL": 528, "UK": 826, "US": 840, "ES": 724, "PT": 620,
                 "TR": 792}


# ---------------------------------------------------------------- the synthetic world

class World:
    def __init__(self, seed: int, plant: dict, cube: dict, samples: dict, split: dict):
        self.r = np.random.default_rng(seed)
        self.plant, self.cube, self.samples, self.split = plant, cube, samples, split
        self.countries = split["countries"]
        self.calls: list = []
        r = self.r
        self.q, self.F = {}, {}
        for c in self.countries:
            v = cube["countries"][c]
            qy = sorted(int(y) for y in v["q_ladder"])
            years = list(range(1945, 2026))
            walk = np.cumsum(r.normal(0.02, 0.05, len(years)))
            self.q[c] = dict(zip(years, walk))
        k2 = cube["families"]["members"].get("K2", [])
        z = {c: float(r.normal()) for c in k2}
        self.F = {c: float(round(np.clip(25 + 12 * z[c], 3, 80))) for c in k2}   # whole percents: exact in the extract
        self.U = {c: dict(zip(range(1945, 2026), 6 + np.cumsum(r.normal(0, 0.6, 81)) * 0.3)) for c in self.countries}

    # --- q sources (stage 1)
    def frame_oecd(self, source, key, geos):
        rows = []
        for c in geos:
            v = self.cube["countries"][c]["series"]
            if source == "oecd_rpi":
                for meas in key["MEASURE"] if isinstance(key["MEASURE"], list) else [key["MEASURE"]]:
                    for y in v["rpi"]:
                        cpi = math.exp(0.03 * (y - 1950))
                        val = math.exp(self.q[c][y]) * cpi * 100 if meas == "RPI" else math.exp(self.q[c][y] + 0.3)
                        flag = "B" if (meas == "RPI" and c == self._b_country() and y == self._b_year(c)) else ""
                        rows.append(dict(geo=c, year=y, value=val, flag=flag, MEASURE=meas, UNIT_MEASURE="IX"))
            elif source in ("oecd_cpi", "oecd_cpi2018"):
                ys = v["cpi"] if source == "oecd_cpi" else v["cpi2018"]
                for y in ys:
                    rows.append(dict(geo=c, year=y, value=math.exp(0.03 * (y - 1950)), flag="", METHODOLOGY="N",
                                     MEASURE="CPI", UNIT_MEASURE="IX", EXPENDITURE="_T", ADJUSTMENT="N",
                                     TRANSFORMATION="_Z"))
            elif source == "oecd_lfs":
                rows += self._lfs(c, key)
        cols = ["geo", "year", "value", "flag"] + [d for d in fetch.SOURCES[source]["dims"]
                                                   if d not in ("REF_AREA", "FREQ")]
        df = pd.DataFrame(rows, columns=cols)
        if len(df):
            cap = {c: (fetch.last_obs_year(c) - (1 if fetch.SOURCES[source]["role"] == "regressor" else 0))
                   for c in geos}
            df = df[df["year"] <= df["geo"].map(cap)]
        return df.reset_index(drop=True)

    def _b_country(self):
        cs = [c for c in self.countries if c not in cv.JST_DOC and self.cube["countries"][c]["series"]["rpi"]]
        return cs[0] if cs else None

    def _b_year(self, c):
        ys = sorted(int(y) for y, s in self.cube["countries"][c]["q_ladder"].items() if s != "jst")
        return ys[len(ys) // 3] if ys else None

    def frame_jst(self, geos):
        rows = []
        for c in geos:
            if c not in cv.JST_DOC:
                continue
            for y in self.cube["countries"][c]["series"]["jst"]:
                cpi = math.exp(0.03 * (y - 1950))
                hp = math.exp(0.04 * (y - 1950) + 0.1 * math.sin(y))
                hp_prev = math.exp(0.04 * (y - 1951) + 0.1 * math.sin(y - 1))
                rent = math.exp(self.q[c][y]) * cpi
                capg = hp / hp_prev - 1
                rows.append(dict(geo=c, year=y, hpnom=np.nan if c in build.CAPGAIN_Q else hp,
                                 housing_rent_yd=rent / hp, housing_capgain=capg,
                                 housing_capgain_ipol=1 if (c == "ES" and y == 1980) else 0,
                                 rent_ipolated=0, cpi=cpi))
        return pd.DataFrame(rows, columns=["geo"] + fetch.SOURCES["jst"]["columns"][1:]) if rows else pd.DataFrame(
            columns=["geo"] + fetch.SOURCES["jst"]["columns"][1:])

    # --- outcomes (stage 2: need the knots the pipeline computed from q)
    def set_basis(self, knots: dict, H: dict, qpanel: pd.DataFrame):
        self.knots, self.H, self.qpanel = knots, H, qpanel

    def _effect(self, c, y):
        k = self.knots.get(c)
        if not k or k.get("k1") is None or y not in set(k["years"]):
            return 0.0
        x = self.qpanel.loc[(c, y), "logq_l1"]
        P = specs.basis([x], k["k1"], k["k2"])[0]
        h = self.H.get(c, 0)
        return self.plant["DiD"] * h * P[2] + self.plant["g1"] * P[0]

    def _lfs(self, c, key):
        v = self.cube["countries"][c]["series"]
        rows = []
        r = np.random.default_rng(int(hashlib.sha1(f"{c}|{key['MEASURE']}".encode()).hexdigest()[:8], 16))
        if key["MEASURE"] == "UNE_RATE":
            for y in v["une_T_Y25T54"]:
                rows.append(dict(geo=c, year=y, value=self.U[c][y], flag="", MEASURE="UNE_RATE",
                                 UNIT_MEASURE="PT_LF_SUB", SEX="_T", AGE="Y25T54", LABOUR_FORCE_STATUS="UNE"))
            return rows
        years = sorted(set.intersection(*[set(v[k]) for k in cv.A2534_CELLS]))
        for y in years:
            base = 75 - 0.3 * self.U[c][y] + r.normal(0, 0.5)
            eff = self._effect(c, y)
            for sex in ("F", "M"):
                for age in build.AGES_PRIME + build.AGES_OLD:
                    val = (base + (eff if age in ("Y25T29", "Y30T34") else 0.0) + (5 if sex == "M" else -5)
                           + r.normal(0, 0.5))
                    rows.append(dict(geo=c, year=y, value=val, flag="", MEASURE="LF_RATE", UNIT_MEASURE="PT_POP_SUB",
                                     SEX=sex, AGE=age, LABOUR_FORCE_STATUS="LF"))
        return rows

    def frame_ilostat(self, geos):
        rows = []
        for c in geos:
            for y in self.cube["countries"][c]["series"]["school"]:
                if y > fetch.last_obs_year(c):
                    continue
                share = 40 + self.plant["school"] * self.U[c][y] + self.r.normal(0, 1)
                src = "BA:1" if y < 1990 else "BA:2"
                for cls, val in (("STU_EDU_YES", share), ("STU_EDU_NO", 100 - share)):
                    rows.append(dict(geo=c, ref_area=fetch.ISO3[c], source=src, indicator="POP_3WAP_SEX_AGE_STU_NB",
                                     sex="SEX_T", classif1="AGE_YTHBANDS_Y20-24", classif2=cls, time=str(y),
                                     obs_value=str(val), obs_status=""))
        return pd.DataFrame(rows)

    def frame_wpp(self, geos):
        rows = []
        for c in geos:
            for y in range(1950, 2026):
                for a in range(25, 65, 5):
                    rows.append(dict(geo=c, Time=y, AgeGrp=f"{a}-{a + 4}", AgeGrpStart=a,
                                     PopTotal=1000 + 10 * math.sin(y + a), Variant="Medium"))
        return pd.DataFrame(rows)

    KH_COVERED = ("US", "DE", "FR", "CA", "NL", "CL")

    def frame_kh(self, geos):
        """A synthetic Kholodilin coding (geo, year, strict): first-generation control up to 1965 in the covered
        countries (to 1975 in FR), none after; the other countries are not covered."""
        rows = [dict(geo=c, year=y, strict=int(y <= (1975 if c == "FR" else 1965)))
                for c in geos if c in self.KH_COVERED for y in range(1950, 2026)]
        return pd.DataFrame(rows, columns=["geo", "year", "strict"])

    def frame_gn(self, geos):
        return pd.DataFrame({"geo": geos, "v8": [float(self.r.uniform(0, 1)) for _ in geos]})

    # --- the IPUMS extract (person records 20-34 of the F_L samples) and its DDI
    def write_ipums(self, folder: str, samples: dict):
        recs = {r["sample"]: r for r in samples["F_L"] + samples["extract_B"]}
        rows, labels = [], {}
        code = 0
        todo = [(c, sid) for c, roles in samples["roles"].items() for sid in sorted(set(roles.values()))]
        todo += [(r["country"], r["sample"]) for r in samples["extract_B"] if r["relate"]
                 and r["country"] in self.countries]
        for c, sid in todo:
            if True:
                rec = recs[sid]
                code += 1
                scode = 100000000 + code
                labels[scode] = rec["title"]
                share = self.F.get(c, 20.0) / 100.0
                n = 3000                                       # 100 cycles of the 15 ages x 2 sexes
                ages = np.arange(20, 35)
                for i in range(n):
                    age = int(ages[i % len(ages)])
                    if rec.get("grouped_age"):
                        age = {20: 22, 25: 27, 30: 32}[(age // 5) * 5]
                    rel = 3 if (i // 30) < round(share * 100) else 1  # exactly the share in every age and sex
                    rows.append(dict(COUNTRY=IPUMS_ISO_NUM.get(c, 0), YEAR=rec["year"], SAMPLE=scode, SERIAL=i + 1,
                                     PERNUM=1, HHWT=10, PERWT=10, AGE=age, SEX=1 + (i % 2), RELATE=rel,
                                     RELATED=rel * 1000, MOMLOC=1 if rel == 3 else 0, POPLOC=0, GQ=10))
        df = pd.DataFrame(rows)
        df.to_csv(os.path.join(folder, "ipumsi_00001.csv"), index=False)
        cats = {"SAMPLE": labels, "RELATE": {1: "Head", 2: "Spouse/partner", 3: "Child", 4: "Other relative",
                                             5: "Non-relative", 9: "Unknown"},
                "RELATED": {1000: "Head", 3000: "Child", 3400: "Child/child-in-law"},
                "GQ": {10: "Households", 20: "Group quarters", 21: "Institutions", 99: "Unknown"}}
        xml = ['<?xml version="1.0"?><codeBook><dataDscr>']
        for v, cs in cats.items():
            xml.append(f'<var name="{v}">')
            for k, lab in cs.items():
                xml.append(f"<catgry><catValu>{k}</catValu><labl>{lab}</labl></catgry>")
            xml.append("</var>")
        xml.append("</dataDscr></codeBook>")
        open(os.path.join(folder, "ipumsi_00001.xml"), "w", encoding="utf-8").write("".join(xml))


# ---------------------------------------------------------------- the fake git and doors

FILLED_FORECASTS = "\n".join(
    ["# synthetic forecast sheets (simulate.py)", ""]
    + sum([[f"## {who}", "", "| Test | Model's sign | Expected sign | P(model's sign) | P(supported) | P(contradicted) | "
            "Note |", "|---|---|---|---|---|---|---|"]
           + [f"| {t}: synthetic | > 0 | + | 0.5 | {sup} | 0.1 | |"
              for t, sup in (("LR-K2", 0.6), ("LR-Y0", 0.3), ("C-6L", 0.6), ("LR-C1", 0.2))] + [""]
           for who in ("Stella", "Claude")], [])
    + ["## E-L (synthetic)", "", "| Participant | E-L | Predicted sign | Expected sign | P(predicted sign) | "
       "P(supported) | P(contradicted) | Note |", "|---|---|---|---|---|---|---|---|", ""])


class FakeGit:
    """Answers the git calls of fetch.py and confirm.py as if both freeze tags existed on a clean tree, and the L tag
    held a ready freeze (production skeleton, filled forecast sheets, a European run, segments, the scouts' move)."""

    def __init__(self, split: dict, samples: dict, tags=("L", "LE", "E")):
        self.split, self.samples = split, samples
        self.tags = {"participation-L-freeze": "a" * 40, "participation-LE-freeze": "b" * 40,
                     "participation-E-freeze": "c" * 40}
        self.tags = {k: v for k, v in self.tags.items() if any(k.endswith(f"-{t}-freeze") for t in tags)}
        self.committed_log = ""

    def __call__(self, *args):
        a = list(args)
        if a[:2] == ["rev-parse", "-q"]:
            tag = a[3].replace("refs/tags/", "").replace("^{commit}", "")
            return (0, self.tags[tag] + "\n") if tag in self.tags else (1, "")
        if a[:1] == ["merge-base"]:
            return 0, ""
        if a[:1] == ["show"]:
            if a[1].endswith("data/split.json"):
                return 0, json.dumps(self.split)
            if a[1].endswith("data/ipums_samples.json"):
                return 0, json.dumps(self.samples)
            if a[1].endswith("data/fetch_log.jsonl"):
                return 0, self.committed_log
            if a[1].endswith("data/skeleton.json"):
                return 0, json.dumps({"quick": False})
            if a[1].endswith("FORECASTS.md"):
                return 0, FILLED_FORECASTS
            if a[1].endswith("data/seen.json"):
                return 0, json.dumps({"scouts_folders": {"moved_to": "synthetic"}})
            if a[1].endswith("data/segments.csv"):
                return 0, "geo,series,tau,reason,citation\n"
            return 1, ""
        if a[:1] == ["ls-tree"]:
            return 0, "results/europe_run_abc1234.json\n"
        if a[:1] == ["status"]:
            return 0, ""
        if a[:1] == ["diff"]:
            return 0, ""
        if a[:1] == ["ls-files"]:
            return (0, "data/skeleton.json\n") if "skeleton" in a[-1] else (0, "")
        if a[:2] == ["rev-parse", "--short"]:
            return 0, "abc1234\n"
        if a[:1] == ["rev-parse"]:
            return 0, "d" * 40 + "\n"
        return 1, ""


def install(world: World, tmp: str, split: dict, samples: dict, calls: list):
    """Point fetch at the world: fake git, temporary log and cache, doors answering from the world."""
    saved = {k: getattr(fetch, k) for k in ("_git", "LOG", "RAW", "IPUMS_DIR", "SPLIT", "oecd", "jst", "ilostat",
                                             "wpp_age", "giuliano_nunn", "kholodilin", "FORECASTS_PATH")}
    saved_samples = ipums.SAMPLES
    saved_stray = ipums.stray_microdata
    ipums.stray_microdata = lambda root=None: saved_stray(tmp)   # the synthetic extract's own folder tree only
    fetch._READY.clear()
    fetch._git = FakeGit(split, samples)
    fetch.FORECASTS_PATH = os.path.join(tmp, "FORECASTS.md")
    open(fetch.FORECASTS_PATH, "w", encoding="utf-8").write(FILLED_FORECASTS)
    fetch.LOG = os.path.join(tmp, "fetch_log.jsonl")
    fetch.RAW = os.path.join(tmp, "raw")
    fetch.IPUMS_DIR = os.path.join(tmp, "ipums")
    fetch.SPLIT = os.path.join(tmp, "split.json")
    json.dump(split, open(fetch.SPLIT, "w"))
    ipums.SAMPLES = os.path.join(tmp, "ipums_samples.json")
    json.dump(samples, open(ipums.SAMPLES, "w"))
    os.makedirs(fetch.IPUMS_DIR, exist_ok=True)
    fetch._APPENDED.clear()

    def door(name, fn):
        def f(*args, **kw):
            half = kw.get("half", args[-1])
            geos = args[2] if name == "oecd" else args[0]
            src = args[0] if name == "oecd" else {"jst": "jst", "ilostat": "ilostat", "wpp_age": "wpp_age",
                                                   "giuliano_nunn": "giuliano_nunn", "kholodilin": "kholodilin"}[name]
            fetch.guard(half, list(geos), src)              # the real guard, with the fake tags
            calls.append(dict(door=name, source=src, half=half, geos=sorted(geos),
                              records=[e.get("record") for e in fetch._entries() if e.get("record")
                                       and e.get("half") == half]))
            out = fn(*args, **kw)
            fetch._log({"source": src, "url": f"synthetic://{src}", "utc": fetch._now(), "half": half,
                        "geos": sorted(geos), "sha256": "synthetic", "bytes": 0, "head_commit": None})
            return out
        return f
    fetch.oecd = door("oecd", lambda source, key, geos, half: world.frame_oecd(source, key, geos))
    fetch.jst = door("jst", lambda geos, half: world.frame_jst(geos))
    fetch.ilostat = door("ilostat", lambda geos, half: world.frame_ilostat(geos))
    fetch.wpp_age = door("wpp_age", lambda geos, half: world.frame_wpp(geos))
    fetch.giuliano_nunn = door("giuliano_nunn", lambda geos, half, column="v8": world.frame_gn(geos))

    fetch.kholodilin = door("kholodilin", lambda geos, half: world.frame_kh(geos))
    world.write_ipums(fetch.IPUMS_DIR, samples)
    return saved, saved_samples, saved_stray


def uninstall(saved, saved_samples, saved_stray):
    for k, v in saved.items():
        setattr(fetch, k, v)
    ipums.SAMPLES = saved_samples
    ipums.stray_microdata = saved_stray
    fetch._APPENDED.clear()
    fetch._READY.clear()


def with_intervals(samples: dict) -> dict:
    """The L2 record of grouped-age intervals, simulated (five-year groups aligned with 20-29 and 25-34)."""
    s = json.loads(json.dumps(samples))
    for r in s["F_L"] + s["extract_B"]:
        if r.get("grouped_age"):
            r["age_intervals"] = [[20, 24], [25, 29], [30, 34]]
    return s


# ---------------------------------------------------------------- one end-to-end run

def run_world(name: str, plant: dict, B: int = 999) -> dict:
    cube = json.load(open(opening.CUBE, encoding="utf-8"))
    split = json.load(open(os.path.join(LROOT, "data", "split.json"), encoding="utf-8"))
    samples = with_intervals(json.load(open(os.path.join(LROOT, "data", "ipums_samples.json"), encoding="utf-8")))
    world = World(SEED + sum(map(ord, name)), plant, cube, samples, split)
    tmp = tempfile.mkdtemp(prefix=f"lr_sim_{name}_")
    calls: list = []
    saved = install(world, tmp, split, samples, calls)
    try:
        # stage 1: q only, the pipeline's own knots and H, so the world can plant through the basis it will measure
        seg = opening.sg.load()
        raw_q = {"house": world.frame_oecd("oecd_rpi", {"MEASURE": ["RPI", "HPI"]}, split["countries"]),
                 "cpi": world.frame_oecd("oecd_cpi", {}, split["countries"]),
                 "cpi2018": world.frame_oecd("oecd_cpi2018", {}, split["countries"]),
                 "jst": world.frame_jst(split["countries"])}
        qp = build.panel(raw_q, split["countries"], seg, build.ladders_of(cube))
        chosen = opening.chosen_segments(cube)
        kn = specs.knots(qp[["logq_l1", "qseg_l1"]], chosen)
        F = {c: world.F[c] for c in cube["families"]["members"].get("K2", []) if kn.get(c, {}).get("k1") is not None}
        H = specs.compute_H(F, list(F))
        world.set_basis(kn, H, qp)
        # the explore opening (records knots and F_L for the explore half)
        t0 = time.time()
        opening.open_half("explore", split["explore"])
        log_after_explore = [e for e in fetch._entries() if e.get("record")]
        # the look
        confirm.B = B
        old_run = specs.run

        def run_b(data, **kw):
            kw.setdefault("B", B)
            return old_run(data, **kw)
        specs.run = run_b
        confirm.RESULTS = os.path.join(tmp, "results")
        if not os.path.exists(confirm.SKELETON):              # before the skeleton exists: an empty table
            stub = os.path.join(tmp, "skeleton.json")
            json.dump({"calibration": None, "mde": {}, "benchmark": {}}, open(stub, "w"))
            confirm.SKELETON = stub
        try:
            out = confirm.look(extract_b=True)
        finally:
            specs.run = old_run
        records = [dict(record=e.get("record"), half=e.get("half")) for e in fetch._entries() if e.get("record")]
        p = out["primary"]
        res = dict(world=name, plant=plant, seconds=time.time() - t0, verdicts=p["verdicts"], verdict_p=p["verdict_p"],
                   model_verdict=p["model_verdict"], model_sentence=p["model_sentence"],
                   joint_reading=p["joint_reading"], qualifiers=p["qualifiers"], readings=p["readings"],
                   H_world=H, H_look=out["H"], knots_explore=log_after_explore[0]["payload"]["q"] if
                   log_after_explore else None,
                   k2=specs.clean_json({k: v for k, v in p["tests"]["LR-K2"].items()
                                        if k not in ("country_fits", "qualifier_runs")}),
                   k2_qualifiers=specs.clean_json({k: dict(fires=v["fires"], text=v.get("text"))
                                                   for k, v in p["tests"]["LR-K2"].get("qualifier_runs", {}).items()}),
                   robustness_ids=sorted(p.get("robustness", {})), no_verdict_ids=sorted(p.get("no_verdict", {})),
                   replication_labels=out["P_confirm_half_replication"]["labels_for_information"],
                   replication_k2=specs.clean_json({k: v for k, v in out["P_confirm_half_replication"]["tests"]
                                                    ["LR-K2"].items() if k in ("beta", "p_stat", "testable", "error",
                                                                                "information_only", "H")}),
                   robustness=specs.clean_json({k: ({kk: vv for kk, vv in v.items() if kk in ("beta", "error", "n")}
                                                    if isinstance(v, dict) else v)
                                                for k, v in p.get("robustness", {}).items()}),
                   control_era=specs.clean_json(p["tests"]["LR-K2"].get("qualifier_runs", {})
                                                .get("rests on control-era years")),
                   d2_placebo=specs.clean_json(p["no_verdict"]["D2-L"].get("placebo")),
                   pooled_d1=specs.clean_json(p["no_verdict"].get("pooled_D1_two_studies")),
                   kholodilin_uncovered=p.get("kholodilin_uncovered"),
                   calls=calls, records=records, vintage=out["vintage_knots_vs_explore"])
        return specs.clean_json(res)
    finally:
        uninstall(*saved)
        shutil.rmtree(tmp, ignore_errors=True)


NET: list = []


def block_network():
    import requests

    def blocked(*a, **k):
        NET.append(1)
        raise RuntimeError("network call attempted")
    requests.adapters.HTTPAdapter.send = blocked
    socket.create_connection = blocked
    socket.socket.connect = blocked


def code_sha() -> dict:
    files = ["simulate.py", "specs.py", "confirm.py", "opening.py", "build.py", "fetch.py", "ipums.py", "coverage.py",
             "segments.py", "inference_l.py"]
    import hashlib
    return {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read().replace(bytes([13, 10]), bytes([10])))
            .hexdigest() for f in files}


def main() -> None:
    block_network()
    out = {"seed": SEED, "worlds": {}, "code_sha256": code_sha()}
    for name, plant in WORLDS.items():
        print(f"world {name} ...", flush=True)
        out["worlds"][name] = run_world(name, plant)
        w = out["worlds"][name]
        print(f"  verdicts {w['verdicts']}; model: {w['model_verdict']}; {w['seconds']:.0f}s", flush=True)
    out["network_calls"] = len(NET)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
