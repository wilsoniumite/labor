# split.py — the one split of the 31 countries into an EXPLORE and a CONFIRM half (PROTOCOL section 4).
#
# Within each stratum the countries are ranked by population on 1 January 2010 (demo_pjan TOTAL, sex T, unit NR; a
# design covariate fetched through the guarded loader with half='design'), largest first, and adjacent countries are
# paired: (1,2), (3,4), ... The smallest country of an odd stratum is its leftover. One member of each pair goes to
# each half by a coin flip; the leftovers are then assigned by one draw, uniform over the assignments that leave the
# halves at 15 and 16. The generator is numpy.random.default_rng(seed), seed = int(sha256(b'participation-split-v1|'
# + ','.join(sorted(codes))).hexdigest()[:16], 16); the draws run over the strata in the protocol's order (Nordic,
# Continental, Anglo, South, CEE), pairs in rank order, then the leftover draw. Given the country list and the
# populations the split is deterministic.
#
# Run from participation/:  ../venv/Scripts/python.exe code/split.py
# Out: data/split.json {seed, countries, strata, population_2010, pairs, explore, confirm}
#      (pairs: [larger, smaller] by 2010 population, in draw order)

from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import eurostat as es  # noqa: E402

OUT = os.path.join(ROOT, "data", "split.json")


def seed_of(codes: list[str]) -> int:
    return int(hashlib.sha256(b"participation-split-v1|" + ",".join(sorted(codes)).encode()).hexdigest()[:16], 16)


def population_2010(countries: list[str] = es.COUNTRIES) -> dict[str, int]:
    df = es.get("demo_pjan", {"age": "TOTAL", "sex": "T", "unit": "NR"}, countries, half="design")
    s = df[df["year"] == 2010].set_index("geo")["value"]
    missing = [c for c in countries if c not in s.index or not np.isfinite(s[c])]
    if missing:
        raise RuntimeError(f"no 2010 population for {missing}")
    return {c: int(s[c]) for c in countries}


def assign(population: dict[str, int], strata: dict[str, list[str]] = es.STRATA,
           countries: list[str] = es.COUNTRIES) -> dict:
    countries = sorted(countries)
    assert sorted(c for s in strata.values() for c in s) == countries
    seed = seed_of(countries)
    rng = np.random.default_rng(seed)
    pairs, explore, confirm, leftovers = [], [], [], []
    for members in strata.values():
        ranked = sorted(members, key=lambda c: (-population[c], c))
        for a, b in zip(ranked[0::2], ranked[1::2]):
            pairs.append([a, b])
            first = int(rng.integers(2))                       # 0: the larger goes to explore
            explore.append((a, b)[first])
            confirm.append((a, b)[1 - first])
        if len(ranked) % 2:
            leftovers.append(ranked[-1])
    sizes = {len(countries) // 2, (len(countries) + 1) // 2}
    valid = [z for z in itertools.product((0, 1), repeat=len(leftovers))   # 1: to explore
             if len(explore) + sum(z) in sizes]
    pick = valid[int(rng.integers(len(valid)))]
    for c, z in zip(leftovers, pick):
        (explore if z else confirm).append(c)
    return {"seed": seed, "countries": countries, "strata": strata,
            "population_2010": {c: int(population[c]) for c in countries},
            "pairs": pairs, "explore": sorted(explore), "confirm": sorted(confirm)}


def build() -> dict:
    return assign(population_2010())


def main() -> None:
    out = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:                 # one key a line, values compact
        f.write("{\n" + ",\n".join(f" {json.dumps(k)}: {json.dumps(v)}" for k, v in out.items()) + "\n}\n")
    print(f"seed {out['seed']}")
    print(f"pairs: {len(out['pairs'])}; explore {len(out['explore'])}, confirm {len(out['confirm'])}")
    print("explore:", " ".join(out["explore"]))
    print("confirm:", " ".join(out["confirm"]))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
