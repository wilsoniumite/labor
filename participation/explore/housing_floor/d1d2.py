# d1d2.py — D1 and D2 on the explore half: the frozen specification reproduced, then the window / cycle-control /
# q-measure variants, to see what (if anything) about the specification drives the estimates.
# Out: d1d2.json, printed table. Every estimate is logged to specs_log.jsonl.

import json
import os

import common as C

raw, cy, cl = C.load()
cyl = C.with_lfs_cycle(raw, cy)
out = {}


def go(label, frame, base, **over):
    r = C.run(label, frame, cl, base=base, **over)
    out[label] = {k: r.get(k) for k in ("beta", "se", "p", "p_opposite", "n", "G", "G_star", "years_used",
                                         "geos_used", "q")}
    print(f"{label:42s} {C.fmt(r)}")
    return r


for T in ("D1", "D2"):
    go(f"{T} frozen (une_rt_a, 2003/09+)", cy, T)
    go(f"{T} long: lfsa_urgan U, 1997+", cyl, T)
    go(f"{T} lfsa_urgan U, 2009+", cyl, T, years=(2009, 2025))
    go(f"{T} no cycle control, 1997+", cy, T, controls=[])
    go(f"{T} no cycle control, 2009+", cy, T, controls=[], years=(2009, 2025))
    go(f"{T} long, lfsa_urgan U, 1997-2019", cyl, T, years=(1997, 2019))
    for v in ("q_cp00", "q_comp", "q_hpi"):
        go(f"{T} long, lfsa_urgan U, {v}", cyl, T, variant=v)
    go(f"{T} long, lfsa_urgan U, country trends", cyl, T, variant="country_trends")
    go(f"{T} long, lfsa_urgan U, all residents", cyl, T, variant="all_residents")

json.dump(C.specs.clean_json(out), open(os.path.join(C.HERE, "d1d2.json"), "w"), indent=1)
