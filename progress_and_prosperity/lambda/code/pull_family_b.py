# pull_family_b.py — λ unit 4: Family B members (WIOD 2016 + long-run WIOD).
# Sources: GGDC DataverseNL API (public GET; HEAD is refused — 403 — so the
# prober uses streamed GET). URL↔content mapping harvested from the release
# pages via the in-app browser 2026-08-20. ICIO (webfs-sti route, unit 1) is
# the extension member, attempted separately after WIOD is secured.

import os, sys
import truststore
truststore.inject_into_ssl()
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
os.makedirs(CACHE, exist_ok=True)
API = "https://dataverse.nl/api/access/datafile/"

MEMBERS = {
    # name on disk                    (datafile id, expected MB — sanity band)
    "wiod16_sea.xlsx":                ("199095", (4, 9)),
    "lr_wiod_sea_final.xlsx":         ("268662", (6, 12)),
    # lr_wiod_wiot_delim (268663) DROPPED from the pull 2026-08-20: the LR SEA
    # carries no labor variables (GO/II/VA/EXP only), so LR WIOTs cannot feed
    # λ̂ — the 1965– world leg is a recorded downgrade, not a member.
    "WIOTS_in_STATA.zip":             ("199103", (500, 800)),
    # WIOD 2013 release (labor layer exists for 1995–2011; LR SEA has none)
    "wiod13_sea_jul14.xlsx":          ("199111", (2, 30)),
    "wiod13_exr.xlsx":                ("199108", (0.01, 5)),
    "WIOT13_in_STATA.zip":            ("199124", (50, 700)),
}

def pull(name, fid, band):
    fp = os.path.join(CACHE, name)
    if os.path.exists(fp) and os.path.getsize(fp) > band[0] * 1e6:
        return "cached", os.path.getsize(fp)
    with requests.get(API + fid, timeout=1800, stream=True) as r:
        if r.status_code != 200:
            return f"FAIL http={r.status_code}", 0
        with open(fp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    size = os.path.getsize(fp)
    if not (band[0] * 1e6 <= size <= band[1] * 1e6):
        return f"FAIL size {size/1e6:.1f}MB outside [{band[0]},{band[1]}]MB", size
    return "pulled", size

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    blocked = []
    for name, (fid, band) in MEMBERS.items():
        if only and only not in name:
            continue
        status, size = pull(name, fid, band)
        print(f"{name:28s} {status:10s} {size/1e6:8.1f} MB", flush=True)
        if status.startswith("FAIL"):
            blocked.append(name)
    if blocked:
        print(f"BLOCKED: {blocked} — stopping, no substitution.")
        sys.exit(1)
    print("pull complete")
