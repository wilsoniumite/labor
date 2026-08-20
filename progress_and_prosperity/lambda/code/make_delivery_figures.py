# make_delivery_figures.py — λ delivery unit: the two paper-grade figures
# (accounting tier, banded, caveats in-caption) and the exact headline
# numbers for the prose (printed; nothing in the note is from memory).
#
# Fig L1 — the spine: US λ̂ 1967–2023 (SIC benchmark points, spliced, +
#   annual band) and world λ̂ (three releases, banded), one panel each.
# Fig L2 — the diagnosis: (a) US decomposition λ̂ = H_rel × w̄_rel with the
#   S&S rent purge; (b) the world within-country hours index vs the raw
#   aggregate (the relocation wedge made visible).

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "figures")

a = pd.read_csv(os.path.join(OUT, "lambda_us_family_a.csv")).set_index("year")
c = pd.read_csv(os.path.join(OUT, "lambda_us_century.csv")).set_index("year")
b = pd.read_csv(os.path.join(OUT, "lambda_world_family_b.csv"))
h = pd.read_csv(os.path.join(OUT, "lambda_us_hours_rent.csv")).set_index("year")
w = pd.read_csv(os.path.join(OUT, "world_h_within_index.csv"))

lam_cols = [x for x in a.columns if x.startswith("lam_") and not x.endswith("domp")]
band_lo, band_hi, band_med = a[lam_cols].min(axis=1), a[lam_cols].max(axis=1), a[lam_cols].median(axis=1)

# ---------------- Fig L1 ----------------
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
ax = axes[0]
ax.fill_between(a.index, band_lo, band_hi, alpha=0.25,
                label="annual grid band, 6 members (sets × import treatment)")
ax.plot(a.index, band_med, lw=2, label="median member")
spl = c["lam_spliced"].dropna()
ax.plot(spl.index, spl, "o--", lw=1.3, ms=5,
        label="SIC benchmark points, spliced at 1992→1997 (link 0.920)")
ax.plot(c["lam"].dropna().index, c["lam"].dropna(), "s", ms=4, alpha=0.45,
        label="SIC benchmarks, unspliced")
ax.set_title("United States, 1967–2023")
ax.set_ylabel("labor compensation embodied per $1 of machinery final output")
ax.legend(fontsize=7.5, loc="lower left")
ax = axes[1]
styles = {"wiod13": (":", "WIOD 2013 (1995–2009 sourced)"),
          "wiod16": ("--", "WIOD 2016 (2000–2014)"),
          "icio25": ("-", "OECD ICIO 2025 (1995–2022; 2015–22 shares frozen at 2014)")}
for rel, (st, lab) in styles.items():
    sub = b[b.release == rel].set_index("year")
    cols = [x for x in sub.columns if x.startswith("lam_narrow_world_")
            or x.startswith("lam_narrow13_world_")]
    bandw = sub[cols].dropna(how="all")
    ax.fill_between(bandw.index, bandw.min(axis=1), bandw.max(axis=1), alpha=0.15)
    ax.plot(bandw.index, bandw.median(axis=1), st, lw=2, label=lab)
frozen = b[(b.release == "icio25") & (b.labor_vintage == "frozen2014")]["year"]
ax.axvspan(frozen.min() - 0.5, frozen.max() + 0.5, alpha=0.07, color="gray")
ax.set_title("World (all-country labor, global inverse), 1995–2022")
ax.legend(fontsize=7.5, loc="lower left")
fig.suptitle("λ̂ — the labor-compensation content of machinery final output · tier: accounting · "
             "bands = classification grids; ICIO 2006–10 block pending", fontsize=9.5)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "lambda_delivery_fig1.png"), dpi=170)

# ---------------- Fig L2 ----------------
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
ax = axes[0]
ax.plot(a.index, a["lam_narrow_tot"], lw=2, label="λ̂ (narrow, total requirements)")
ax.plot(h.index, h["Hrel_narrow_tot"], "--", lw=2, label="H_rel — quantity leg (hours at economy-average wage)")
ax.plot(h.index, h["lampurged_narrow_tot"], ":", lw=1.8,
        label="λ̂ rent-purged (Stansbury–Summers industry ρ, to 2016)")
ax.plot(h.index, h["wrel_narrow_tot"] * 0.5, "-.", lw=1.2, alpha=0.8,
        label="w̄_rel × 0.5 — price leg (right scale intuition: flat-to-rising)")
ax.set_title("United States: the decline sits on the quantity leg; rents don't carry it")
ax.set_ylabel("share of $1 machinery final output")
ax.legend(fontsize=7.5, loc="lower left")
ax = axes[1]
for rel, (st, lab) in {"wiod13": (":", "WIOD 2013"), "wiod16": ("--", "WIOD 2016"),
                       "icio25": ("-", "ICIO 2025")}.items():
    sub = w[w.release == rel].set_index("year")
    ax.plot(sub.index, sub["H_within_tornqvist"], st, lw=2, label=f"{lab} — within-country (Törnqvist)")
    ax.plot(sub.index, sub["H_raw"], st, lw=1, alpha=0.45, label=f"{lab} — raw aggregate")
ax.set_title("World hours per $1 machinery: within-country vs raw\n(the gap is the relocation wedge)")
ax.set_ylabel("index, release base year = 1")
ax.legend(fontsize=7, loc="upper right")
fig.suptitle("The diagnosis behind the gate read · tier: accounting · UNREAD flags retired 2026-08-20 (READ: PASS)",
             fontsize=9.5)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "lambda_delivery_fig2.png"), dpi=170)

# ---------------- headline numbers for the prose ----------------
print("=== headline numbers (paste-source for the note and the subsection) ===")
print(f"US annual λ̂ narrow_tot: 1997 {a.loc[1997,'lam_narrow_tot']:.3f} → 2023 {a.loc[2023,'lam_narrow_tot']:.3f}")
print(f"US band 2023 across 6 members: [{band_lo.loc[2023]:.3f}, {band_hi.loc[2023]:.3f}]; median {band_med.loc[2023]:.3f}")
print(f"US band 1997: [{band_lo.loc[1997]:.3f}, {band_hi.loc[1997]:.3f}]; median {band_med.loc[1997]:.3f}")
print(f"spliced 1982 {c.loc[1982,'lam_spliced']:.3f} → 2023 {a.loc[2023,'lam_narrow_tot']:.3f} "
      f"(Δ {a.loc[2023,'lam_narrow_tot']-c.loc[1982,'lam_spliced']:+.3f})")
print(f"benchmarks 1967 {c.loc[1967,'lam']:.3f} (unspliced), spliced {c.loc[1967,'lam_spliced']:.3f}")
w16 = b[b.release == "wiod16"].set_index("year")
ic = b[b.release == "icio25"].set_index("year")
print(f"world wiod16 comp_rowm: 2000 {w16.loc[2000,'lam_narrow_world_comp_rowm']:.3f} → 2014 {w16.loc[2014,'lam_narrow_world_comp_rowm']:.3f}")
print(f"world icio comp_rowm: 1995 {ic.loc[1995,'lam_narrow_world_comp_rowm']:.3f} → 2014 {ic.loc[2014,'lam_narrow_world_comp_rowm']:.3f} → 2022 {ic.loc[2022,'lam_narrow_world_comp_rowm']:.3f} (frozen-share tail)")
print(f"US H_rel: 1997 {h.loc[1997,'Hrel_narrow_tot']:.3f} → 2023 {h.loc[2023,'Hrel_narrow_tot']:.3f}; "
      f"w̄_rel 1997 {h.loc[1997,'wrel_narrow_tot']:.3f} → 2023 {h.loc[2023,'wrel_narrow_tot']:.3f}")
print(f"purge: 1997 {h.loc[1997,'lampurged_narrow_tot']:.3f} → 2016 {h.loc[2016,'lampurged_narrow_tot']:.3f}; "
      f"ρ machinery 1997 {h.loc[1997,'rho_machinery_direct']:.3f} → 2016 {h.loc[2016,'rho_machinery_direct']:.3f}")
for rel in ("wiod13", "wiod16", "icio25"):
    sub = w[w.release == rel].set_index("year")
    y0, y1 = sub.index.min(), sub.index.max()
    print(f"H_within {rel}: {y0}=1 → {y1} {sub.loc[y1,'H_within_tornqvist']:.3f} (raw {sub.loc[y1,'H_raw']:.3f})")
fs = {}
for rel in ("wiod13", "wiod16", "icio25"):
    s2 = b[b.release == rel].set_index("year")
    sn = "narrow13" if rel == "wiod13" else "narrow"
    ser = (1 - s2[f"lamUS_{sn}_comp_rowm"] / s2[f"lam_{sn}_uspurch_comp_rowm"]).dropna()
    print(f"foreign share of US machinery purchases, {rel}: {ser.iloc[0]:.2f} ({int(ser.index[0])}) → {ser.iloc[-1]:.2f} ({int(ser.index[-1])})")
print("\nwrote figures/lambda_delivery_fig1.png and _fig2.png")
