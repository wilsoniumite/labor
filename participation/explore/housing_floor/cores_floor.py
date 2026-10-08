# cores_floor.py — the other side of the kink: does coresidence (25-34) absorb q more where the floor is available?
# C-1's equation (SILC window 2005-2025, U control) with log q x F_c added, with and without country trends; and the
# young's overburden (understanding only, not in the manifest) as an outcome.
# Out: cores_floor.json; estimates logged.

import json
import os

import numpy as np

import common as C

raw, cy, cl = C.load()
cyl = C.with_lfs_cycle(raw, cy)
out = {}


def go(label, frame, base, **over):
    r = C.run(label, frame, cl, base=base, **over)
    out[label] = {k: r.get(k) for k in ("beta", "se", "p", "p_opposite", "n", "G", "G_star")}
    print(f"{label:52s} {C.fmt(r)}")
    return r


for lab, fr in (("frozen U", cy), ("lfsa_urgan U", cyl)):
    go(f"cores on q x F, {lab}", fr, "C1", x="Q*F", z=["Q"], side=1)
    go(f"cores on q x F, {lab}, trends", fr, "C1", x="Q*F", z=["Q"], side=1, variant="country_trends")
go("C1 (cores on q), lfsa_urgan U, trends", cyl, "C1", variant="country_trends")

json.dump(C.specs.clean_json(out), open(os.path.join(C.HERE, "cores_floor.json"), "w"), indent=1)
