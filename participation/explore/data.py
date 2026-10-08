# data.py — the explore half's data, for exploration only (PROTOCOL section 1, tier E).
#
# get(code, filters) wraps eurostat.get for the explore half: the 16 explore countries of the frozen split, with an
# exclusive lock file around each call so parallel explorers never append to data/fetch_log.jsonl at the same time.
# A cached query is served from data/raw/explore/ without a new log line. EXTRA is the broad set of series prefetched
# for exploration (run this file once); anything in it, or any further query, is for understanding only: an
# E-hypothesis may use only what the frozen manifest fetches (manifest_raw()).
#
# Run from participation/:  ../venv/Scripts/python.exe explore/data.py     (prefetches EXTRA and the manifest)

from __future__ import annotations

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import build  # noqa: E402
import eurostat as es  # noqa: E402

LOCK = os.path.join(ROOT, "data", "raw", ".explore.lock")
GEOS = sorted(es.frozen_split()["explore"])

AGES5 = [f"Y{a}-{a + 4}" for a in range(15, 75, 5)]
EXTRA = {
    "argan": ("lfsa_argan", {"unit": "PC", "sex": ["M", "F", "T"], "age": AGES5 + ["Y15-24", "Y25-54", "Y55-64"],
                             "citizen": ["NAT", "TOTAL"]}),
    "ergan": ("lfsa_ergan", {"unit": "PC", "sex": ["M", "F", "T"], "age": AGES5 + ["Y15-24", "Y25-54", "Y55-64"],
                             "citizen": ["NAT", "TOTAL"]}),
    "urgan": ("lfsa_urgan", {"unit": "PC", "sex": ["M", "F", "T"], "citizen": "TOTAL",
                             "age": ["Y15-24", "Y20-24", "Y25-29", "Y15-29", "Y25-54", "Y25-74", "Y55-64"]}),
    "igar": ("lfsa_igar", {"unit": "PC_POP", "sex": ["M", "F", "T"],
                           "age": ["Y15-24", "Y15-29", "Y25-54", "Y55-64", "Y15-64"]}),
    "neet": ("edat_lfse_20", {"unit": "PC", "sex": ["M", "F", "T"], "training": "NO_FE_NO_NFE",
                              "age": ["Y20-24", "Y25-29", "Y15-29", "Y20-34"]}),
    "educ": ("edat_lfse_19", {"unit": "PC", "sex": ["M", "F", "T"], "wstatus": "POP", "training": "FE",
                              "age": ["Y15-19", "Y20-24", "Y25-29"]}),
    "cores": ("ilc_lvps08", {"unit": "PC", "sex": ["M", "F", "T"]}),
    "cores_status": ("ilc_lvps09", {"unit": "PC"}),
    "tenure": ("ilc_lvps05", {"unit": "PC", "sex": "T"}),
    "overburden": ("ilc_lvho07a", {"unit": "PC", "sex": "T", "rskpovth": "TOTAL"}),
    "hicp": ("prc_hicp_aind", {"unit": "INX_A_AVG",
                               "coicop": ["CP00", "CP041", "IGD_NNRG", "GD", "SERV", "NRG", "CP053"]}),
    "hpi": ("prc_hpi_a", {"purchase": "TOTAL", "unit": ["I15_A_AVG", "I25_A_AVG"]}),
    "comp": ("nama_10_lp_ulc", {"na_item": ["D1_SAL_PER", "RLPR_PER"], "unit": ["NAC", "I15"]}),
    "occ": ("lfsa_egais", {"unit": "THS_PER", "sex": ["M", "F", "T"], "wstatus": "EMP",
                           "age": ["Y15-24", "Y25-54", "Y55-64", "Y15-64"]}),
    "leave_age": ("yth_demo_030", {"unit": "AVG", "sex": ["M", "F", "T"]}),
    "pop": ("demo_pjan", {"unit": "NR", "sex": ["M", "F", "T"],
                          "age": [f"Y{a}" for a in range(1, 100)] + ["Y_LT1", "Y_OPEN"]}),
}


class _Lock:
    def __enter__(self):
        os.makedirs(os.path.dirname(LOCK), exist_ok=True)
        t0 = time.time()
        while True:
            try:
                self.fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.time() - t0 > 600:
                    raise TimeoutError(f"{LOCK} held for 10 minutes; remove it if no fetch is running")
                time.sleep(0.5)

    def __exit__(self, *a):
        os.close(self.fd)
        os.remove(LOCK)


def get(code: str, filters: dict, geos: list[str] | None = None, since: int | None = None):
    """eurostat.get on the explore half (all 16 countries unless a subset is given), under the lock."""
    with _Lock():
        return es.get(code, filters, sorted(geos or GEOS), half="explore", since=since)


def extra(key: str):
    """One EXTRA series, long format, u/c cells blanked (C4)."""
    code, filters = EXTRA[key]
    return es.clean(get(code, filters))


def manifest_raw() -> dict:
    """The frozen manifest's raw frames for the explore half — the only data an E-hypothesis may use."""
    with _Lock():
        return build.fetch("explore")


def panel():
    """The frozen pipeline's variables for the explore half: (country_year, country_level)."""
    raw = manifest_raw()
    return build.country_year("explore", raw=raw), build.country_level("explore", raw=raw)


if __name__ == "__main__":
    for k in EXTRA:
        try:
            d = extra(k)
            print(f"  {k:12s} {EXTRA[k][0]:14s} {len(d):7d} rows, years {d['year'].min()}-{d['year'].max()}")
        except Exception as e:                                # a wrong code is reported, not fatal
            print(f"  {k:12s} {EXTRA[k][0]:14s} FAILED: {type(e).__name__}: {str(e)[:200]}")
    cy, cl = panel()
    print(f"manifest panel: {cy.shape}, country level {cl.shape}")
