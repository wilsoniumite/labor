# split.py — the one long-run split into an EXPLORE and a CONFIRM half (longrun/PROTOCOL.md section 4).
#
# Who is split: the members that enter at least one verdict test by the testability rules of section 3, read from
# data/coverage.json (coverage.py; LR-C1's members count only if LR-C1 is in the C-L family, which needs her Extract B).
# Strata, in the protocol's order: Nordic, Continental, Anglo, South, Asia, Latin America, Other (IL, TR and any other
# member that enters, appended in code order). Within each stratum the countries are ranked by population on 1 July
# 1960 (UN WPP2024, the design covariate, through fetch.population_1960: half 'design'), largest first, and adjacent
# countries are paired: (1,2), (3,4), ...; the smallest of an odd stratum is its leftover.
# Forced placement: the US goes to EXPLORE and its pair partner to CONFIRM, with no draw for that pair (if the US were
# a leftover it would go to EXPLORE and the leftover draw would run over the others).
# Draws: numpy.random.default_rng(seed), seed = int(sha256(b'participation-longrun-split-v1|' +
# ','.join(sorted(codes)).encode()).hexdigest()[:16], 16); one integer draw per unforced pair, in stratum order and
# rank order (0: the larger goes to explore), then one draw uniform over the leftover assignments that leave the halves
# differing in size by at most one.
#
# Run from longrun/:  ../../venv/Scripts/python.exe code/split.py
# Out: data/split.json {seed, countries, strata, population_1960, pairs, forced, explore, confirm, membership_source}

from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch  # noqa: E402

OUT = os.path.join(LROOT, "data", "split.json")
CUBE = os.path.join(LROOT, "data", "coverage.json")


def seed_of(codes: list[str]) -> int:
    return int(hashlib.sha256(b"participation-longrun-split-v1|" + ",".join(sorted(codes)).encode()).hexdigest()[:16],
               16)


def entering(cube: dict | None = None, with_c1: bool = False) -> list[str]:
    """The members that enter at least one verdict test (section 3), from data/coverage.json."""
    cube = json.load(open(CUBE, encoding="utf-8")) if cube is None else cube
    fam = cube["families"]
    tests = (["K2"] if fam["testable"]["K2"] else []) + [k for k, t in (("Y0", "LR-Y0"), ("C6L", "C-6L"))
                                                         if t in fam["C-L"]]
    if with_c1 and "LR-C1" in fam["C-L"]:
        tests.append("C1")
    return sorted(set().union(*[set(fam["members"][k]) for k in tests])) if tests else []


def strata_for(countries: list[str]) -> dict[str, list[str]]:
    out = {s: [c for c in cs if c in countries] for s, cs in fetch.STRATA.items()}
    known = {c for cs in fetch.STRATA.values() for c in cs}
    out["Other"] += sorted(c for c in countries if c not in known)
    return {s: cs for s, cs in out.items() if cs}


def assign(population: dict[str, float], countries: list[str], forced: str = fetch.FORCED_EXPLORE) -> dict:
    countries = sorted(countries)
    strata = strata_for(countries)
    seed = seed_of(countries)
    rng = np.random.default_rng(seed)
    pairs, explore, confirm, leftovers = [], [], [], []
    for members in strata.values():
        ranked = sorted(members, key=lambda c: (-population[c], c))
        for a, b in zip(ranked[0::2], ranked[1::2]):
            pairs.append([a, b])
            if forced in (a, b):
                explore.append(forced)
                confirm.append(b if a == forced else a)
                continue
            first = int(rng.integers(2))                      # 0: the larger goes to explore
            explore.append((a, b)[first])
            confirm.append((a, b)[1 - first])
        if len(ranked) % 2:
            if ranked[-1] == forced:
                explore.append(forced)
            else:
                leftovers.append(ranked[-1])
    n = len(countries)
    valid = [z for z in itertools.product((0, 1), repeat=len(leftovers))
             if abs((len(explore) + sum(z)) - (len(confirm) + len(z) - sum(z))) <= 1]
    pick = valid[int(rng.integers(len(valid)))] if leftovers else ()
    for c, z in zip(leftovers, pick):
        (explore if z else confirm).append(c)
    assert sorted(explore + confirm) == countries and abs(len(explore) - len(confirm)) <= 1 and n
    return {"seed": seed, "countries": countries, "strata": strata,
            "population_1960": {c: float(population[c]) for c in countries}, "pairs": pairs, "forced": forced,
            "explore": sorted(explore), "confirm": sorted(confirm)}


def build(with_c1: bool = False) -> dict:
    cs = entering(with_c1=with_c1)
    out = assign(fetch.population_1960(cs), cs)
    out["membership_source"] = ("data/coverage.json families: members of LR-K2, LR-Y0, C-6L"
                                + (", LR-C1" if with_c1 else " (LR-C1 left out until her Extract B decision)"))
    return out


def write(out: dict) -> None:
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("{\n" + ",\n".join(f" {json.dumps(k)}: {json.dumps(v)}" for k, v in out.items()) + "\n}\n")


def main() -> None:
    out = build(with_c1="--with-c1" in sys.argv)
    write(out)
    print(f"seed {out['seed']}; {len(out['countries'])} countries, {len(out['pairs'])} pairs")
    print("explore:", " ".join(out["explore"]))
    print("confirm:", " ".join(out["confirm"]))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
