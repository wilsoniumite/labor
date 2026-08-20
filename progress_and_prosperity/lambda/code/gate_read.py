# gate_read.py — λ unit 6: THE GATE READ.
# Mechanical application of the pre-committed criteria (lambda_spec.md,
# "Read criteria — committed before the pull", amended 2026-08-20 pre-read).
# This script is the record: every number in the memo comes from here.
#
# Operationalization (stated, vetoable):
#   Per grid member m over a window: OLS slope_m of the series on year;
#   Δ_m = slope_m × (span). A leg is:
#     FALLING     iff median(slope) < 0 AND ≥¾ of members have slope < 0
#                 AND max_m Δ_m < 0 (the member-Δ band does not straddle 0)
#     FLAT/RISING iff median(slope) ≥ 0 AND < ½ of members have slope < 0
#     MIXED       otherwise
#   W1b (1982→2023): spliced century series (lam, lami × the 0.9204 link)
#   pooled with the NAICS annual series; within-segment directions reported.
#   World referee: members from wiod13 (1995–2009), wiod16 (2000–2014), and
#   icio25 SOURCED years (1995–2014, ex-frozen) are the PRIMARY members;
#   icio25 full-window (with the frozen-2014 tail) reported as SUPPORTING.
#   Rent robustness: the US pass additionally requires λ̂_purged (S&S,
#   1997–2016) falling. Diagnosis layers (w̄_rel, ρ, foreign share) are
#   reported, not gated.
#
# Verdict logic (spec):
#   PASS  = λ̂ falling AND H_rel falling on the world referee AND on the US
#           referee (W3 and W1b), AND the purge survives.
#   FAIL  = λ̂ AND H_rel flat/rising across the grid on the world referee.
#   AMBIGUOUS otherwise, with the two pre-named mixed cases labeled.

import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")

def leg(series_dict, y0, y1):
    slopes, deltas, detail = {}, {}, {}
    for m, s in series_dict.items():
        s = pd.Series(s).dropna()
        s = s[(s.index >= y0) & (s.index <= y1)]
        if len(s) < 3:
            continue
        x = s.index.values.astype(float)
        b = np.polyfit(x, s.values, 1)[0]
        slopes[m] = b
        deltas[m] = b * (x.max() - x.min())
        detail[m] = (float(s.iloc[0]), float(s.iloc[-1]), len(s))
    if not slopes:
        return None
    sl = np.array(list(slopes.values()))
    med = float(np.median(sl))
    share_neg = float((sl < 0).mean())
    dmin, dmax = float(min(deltas.values())), float(max(deltas.values()))
    if med < 0 and share_neg >= 0.75 and dmax < 0:
        verdict = "FALLING"
    elif med >= 0 and share_neg < 0.5:
        verdict = "FLAT/RISING"
    else:
        verdict = "MIXED"
    return {"verdict": verdict, "median_slope_per_decade": med * 10,
            "share_negative": share_neg, "delta_band": (dmin, dmax),
            "n_members": len(slopes), "members": slopes, "detail": detail}

def show(name, r):
    if r is None:
        print(f"  {name}: NO DATA")
        return
    print(f"  {name}: {r['verdict']}  (median slope {r['median_slope_per_decade']:+.4f}/decade; "
          f"{r['share_negative']:.0%} of {r['n_members']} members negative; "
          f"member-Δ band [{r['delta_band'][0]:+.4f}, {r['delta_band'][1]:+.4f}])")

def main():
    a = pd.read_csv(os.path.join(OUT, "lambda_us_family_a.csv")).set_index("year")
    c = pd.read_csv(os.path.join(OUT, "lambda_us_century.csv")).set_index("year")
    b = pd.read_csv(os.path.join(OUT, "lambda_world_family_b.csv"))
    h = pd.read_csv(os.path.join(OUT, "lambda_us_hours_rent.csv")).set_index("year")

    print("=" * 76)
    print("THE GATE READ — λ assembly, unit 6 (2026-08-20). Criteria as committed.")
    print("=" * 76)

    # ---------- US referee, λ̂ leg: W3 ----------
    us_lam = {f"{s}_{t}": a[f"lam_{s}_{t}"] for s in ("narrow", "medium", "broad")
              for t in ("tot", "dom")}
    r_w3 = leg(us_lam, 1997, 2023)
    print("\n[US λ̂ — W3 1997–2023, 6 members]"); show("W3", r_w3)

    # ---------- US referee, λ̂ leg: W1b (spliced) ----------
    w1b = {}
    for var in ("lam", "lami"):
        sic = c[var].dropna()
        link = a.loc[1997, "lam_narrow_tot"] / c.loc[1992, "lam"]
        spl = pd.concat([sic[sic.index >= 1982] * link, a["lam_narrow_tot"]])
        w1b[f"spliced_{var}"] = spl[~spl.index.duplicated()]
    r_w1b = leg(w1b, 1982, 2023)
    print("\n[US λ̂ — W1b 1982→2023 spliced, 2 members]"); show("W1b", r_w1b)
    sic_dir = c.loc[1992, "lam"] - c.loc[1982, "lam"]
    print(f"  within-segment: SIC 1982→1992 Δ = {sic_dir:+.4f} "
          f"({c.loc[1982,'lam']:.4f} → {c.loc[1992,'lam']:.4f}); "
          f"NAICS 1997→2023 Δ = {a.loc[2023,'lam_narrow_tot']-a.loc[1997,'lam_narrow_tot']:+.4f}")
    print(f"  W1 context 1967→1992 (no sign requirement): "
          f"{c.loc[1967,'lam']:.4f} → {c.loc[1992,'lam']:.4f} "
          f"(path {[round(c.loc[y,'lam'],3) for y in (1967,1972,1977,1982,1987,1992)]})")

    # ---------- US referee, H_rel leg (W3; W1b NAICS segment = same) ----------
    us_h = {f"{s}_{t}": h[f"Hrel_{s}_{t}"] for s in ("narrow", "medium", "broad")
            for t in ("tot", "dom")}
    r_w3h = leg(us_h, 1997, 2023)
    print("\n[US H_rel — W3 1997–2023, 6 members; W1b H leg = NAICS segment (stated)]")
    show("W3 H_rel", r_w3h)

    # ---------- Rent robustness: the purge ----------
    us_p = {f"{s}_{t}": h[f"lampurged_{s}_{t}"] for s in ("narrow", "medium", "broad")
            for t in ("tot", "dom")}
    r_purge = leg(us_p, 1997, 2016)
    print("\n[US λ̂ rent-purged (S&S industry ρ) — 1997–2016, 6 members]")
    show("purge", r_purge)
    r_wrel = leg({f"{s}_{t}": h[f"wrel_{s}_{t}"] for s in ("narrow", "medium", "broad")
                  for t in ("tot", "dom")}, 1997, 2023)
    show("w̄_rel (diagnosis, not gated)", r_wrel)
    rho = h[["rho_machinery_direct", "rho_aggregate"]].dropna()
    print(f"  ρ machinery-direct {rho['rho_machinery_direct'].iloc[0]:.3f} (1997) → "
          f"{rho['rho_machinery_direct'].iloc[-1]:.3f} (2016); "
          f"aggregate {rho['rho_aggregate'].iloc[0]:.3f} → {rho['rho_aggregate'].iloc[-1]:.3f} "
          f"(A&R level anchor for automated jobs: ≈0.35 [0.19–0.445])")

    # ---------- World referee ----------
    def world_members(prefix, srcd_only=True):
        out = {}
        for rel, y0, y1 in (("wiod13", 1995, 2009), ("wiod16", 2000, 2014),
                            ("icio25", 1995, 2014 if srcd_only else 2022)):
            sub = b[b.release == rel].set_index("year")
            if srcd_only and rel == "icio25":
                sub = sub[sub["labor_vintage"] != "frozen2014"]
            sname = "narrow13" if rel == "wiod13" else "narrow"
            for v in ("comp", "lab"):
                for r0 in ("row0", "rowm"):
                    col = f"{prefix}_{sname}_world_{v}_{r0}" if prefix == "lam" \
                        else f"hrel_{sname}_world_h_{r0}"
                    if col in sub.columns and sub[col].notna().sum() >= 3:
                        key = f"{rel}_{v}_{r0}" if prefix == "lam" else f"{rel}_{r0}"
                        out[key] = sub[col]
                if prefix != "lam":
                    break
        return out

    r_w2 = leg(world_members("lam"), 1995, 2014)
    print("\n[World λ̂ — W2 PRIMARY (sourced labor: wiod13 95–09, wiod16 00–14, icio 95–14)]")
    show("W2 λ̂", r_w2)
    full = {}
    sub = b[b.release == "icio25"].set_index("year")
    for v in ("comp", "lab"):
        for r0 in ("row0", "rowm"):
            full[f"icio_full_{v}_{r0}"] = sub[f"lam_narrow_world_{v}_{r0}"]
    r_w2f = leg(full, 1995, 2022)
    show("W2 λ̂ SUPPORTING (icio full 1995–2022 incl. frozen tail)", r_w2f)

    r_w2h = leg(world_members("hrel"), 1995, 2014)
    print("\n[World H_rel — W2 PRIMARY (same windows)]")
    show("W2 H_rel", r_w2h)
    fullh = {f"icio_full_{r0}": sub[f"hrel_narrow_world_h_{r0}"] for r0 in ("row0", "rowm")}
    show("W2 H_rel SUPPORTING (icio full)", leg(fullh, 1995, 2022))

    # offshoring context
    fsh = {}
    for rel in ("wiod13", "wiod16", "icio25"):
        s2 = b[b.release == rel].set_index("year")
        sname = "narrow13" if rel == "wiod13" else "narrow"
        lam_c, lus_c = f"lam_{sname}_uspurch_comp_rowm", f"lamUS_{sname}_comp_rowm"
        if lam_c in s2.columns:
            fsh[rel] = (1 - s2[lus_c] / s2[lam_c]).dropna()
    print("\n[Offshoring context — foreign-labor share of US machinery purchases]")
    for rel, s in fsh.items():
        print(f"  {rel}: {s.iloc[0]:.2f} ({int(s.index[0])}) → {s.iloc[-1]:.2f} ({int(s.index[-1])})")

    # ---------- THE VERDICT ----------
    print("\n" + "=" * 76)
    us_lam_falling = r_w3["verdict"] == "FALLING" and r_w1b["verdict"] == "FALLING"
    us_h_falling = r_w3h["verdict"] == "FALLING"
    purge_ok = r_purge["verdict"] == "FALLING"
    world_lam_falling = r_w2["verdict"] == "FALLING"
    world_h_falling = r_w2h["verdict"] == "FALLING"
    print(f"US λ̂ falling (W3 & W1b): {us_lam_falling}   US H_rel falling: {us_h_falling}   "
          f"purge survives: {purge_ok}")
    print(f"World λ̂ falling: {world_lam_falling}   World H_rel falling: {world_h_falling}")
    if us_lam_falling and us_h_falling and purge_ok and world_lam_falling and world_h_falling:
        verdict = "PASS"
    elif (r_w2["verdict"] == "FLAT/RISING") and (r_w2h["verdict"] == "FLAT/RISING"):
        verdict = "FAIL"
    else:
        verdict = "AMBIGUOUS"
        if world_lam_falling and not world_h_falling:
            verdict += " — pre-named case: λ̂↓ H_rel→ (rent-dissipation candidate; NOT a pass)"
        elif not world_lam_falling and world_h_falling:
            verdict += " — pre-named case: λ̂→ H_rel↓ (rent-masked automation; NOT a clean fail)"
    print(f"\nTHE GATE READ: {verdict}")
    print("=" * 76)

    # ---------- RE-READ (unit 6a): the repaired world quantity leg ----------
    fp = os.path.join(OUT, "world_h_within_index.csv")
    if not os.path.exists(fp):
        print("\n[unit 6a repair not yet computed — re-read pending]")
        return
    idx = pd.read_csv(fp)
    print("\n" + "=" * 76)
    print("RE-READ (unit 6a) — repaired world quantity leg: WITHIN-COUNTRY hours")
    print("index (chained Törnqvist + fixed-base Laspeyres), per the amendment")
    print("committed before this number was computed.")
    members, sup_members = {}, {}
    for rel, y0, y1 in (("wiod13", 1995, 2009), ("wiod16", 2000, 2014), ("icio25", 1995, 2014)):
        sub = idx[idx.release == rel].set_index("year")
        srcd = sub[sub["vintage"] != "frozen2014"] if "vintage" in sub.columns and rel == "icio25" else sub
        for form in ("tornqvist", "laspeyres"):
            members[f"{rel}_{form}"] = srcd[f"H_within_{form}"]
            if rel == "icio25":
                sup_members[f"icio_full_{form}"] = sub[f"H_within_{form}"]
    r_rep = leg(members, 1995, 2014)
    print("\n[World H_within — PRIMARY (sourced windows), 6 members]")
    show("W2 H_within", r_rep)
    show("W2 H_within SUPPORTING (icio full incl. frozen tail)", leg(sup_members, 1995, 2022))
    # relocation component, reported
    for rel in ("wiod13", "wiod16", "icio25"):
        sub = idx[idx.release == rel].set_index("year")
        y0, y1 = sub.index.min(), sub.index.max()
        print(f"  relocation (between) component {rel} {y0}–{y1}: "
              f"raw {sub.loc[y1,'H_raw']:.3f} vs within-Törnqvist "
              f"{sub.loc[y1,'H_within_tornqvist']:.3f} (base {y0} = 1)")

    world_h_falling2 = r_rep is not None and r_rep["verdict"] == "FALLING"
    print(f"\nRepaired leg: World H_within falling: {world_h_falling2}")
    if us_lam_falling and us_h_falling and purge_ok and world_lam_falling and world_h_falling2:
        final = "PASS"
    elif (r_w2["verdict"] == "FLAT/RISING") and r_rep is not None and r_rep["verdict"] == "FLAT/RISING":
        final = "FAIL"
    else:
        final = "AMBIGUOUS (repaired leg did not resolve — back to Stella)"
    print(f"\nTHE GATE READ, FINAL (with the repaired leg): {final}")
    print("=" * 76)

if __name__ == "__main__":
    main()
