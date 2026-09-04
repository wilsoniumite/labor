# misallocation_firstlook.py — Block E first look: person-years/yr by channel, brackets not
# measurements. Commissioned as exploration ("see what it looks like"); every imported dial
# is named; the envelope is UNATTRIBUTED by construction. 2026-08-09.
import io
import os
import re
import sys

import numpy as np
import pandas as pd
import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fred(sid, must_contain):
    """Pull a FRED series; validate by the series page <title>. Stop-and-report style."""
    tp = requests.get(f"https://fred.stlouisfed.org/series/{sid}", headers=UA, timeout=30)
    m = re.search(r"<title>(.*?)</title>", tp.text, re.S)
    title = (m.group(1).strip() if m else "")
    if must_contain.lower() not in title.lower():
        print(f"  {sid}: title check FAILED ('{title[:70]}...' lacks '{must_contain}')")
        return None, title
    r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", headers=UA, timeout=30)
    df = pd.read_csv(io.StringIO(r.text))
    s = pd.Series(pd.to_numeric(df[sid], errors="coerce").values,
                  index=pd.to_datetime(df["observation_date"])).dropna()
    print(f"  {sid}: OK '{title.split('|')[0].strip()[:70]}' ({s.index.min().year}-{s.index.max().year})")
    return s, title

print("=== pulls (validated by series-page title) ===")
h_us, _ = fred("AVHWPEUSA065NRUG", "Hours Worked")
h_de, _ = fred("AVHWPEDEA065NRUG", "Hours Worked")
emp, _ = fred("CE16OV", "Employment")
esi = None
for sid in ("B1044C1A027NBEA", "B1043C1A027NBEA"):
    esi, t = fred(sid, "group health")
    if esi is not None:
        ESI_LABEL = "employer group-health contributions"
        break
if esi is None:
    print("  group-health line not found under probed IDs — using the validated broader aggregate")
    esi, _ = fred("B040RC1A027NBEA", "pension and insurance")
    ESI_LABEL = "employer pension+insurance supplements (UPPER BOUND for group health; the split is a BEA 6.11 table pull, queued)"
assert h_us is not None and emp is not None, "BLOCKED: core series unavailable"

# ---------------- envelope members (UNATTRIBUTED) ----------------
hu = h_us.groupby(h_us.index.year).mean()
Y0, Y1 = 1950, int(hu.index.max())
rate = np.log(hu.loc[1980] / hu.loc[Y0]) / (1980 - Y0)          # measured 1950-80 slope
h_cf = hu.loc[1980] * np.exp(rate * (Y1 - 1980))                # trend-continuation counterfactual
emp_ann = emp.groupby(emp.index.year).mean()
E_Y1 = emp_ann.loc[Y1] * 1e3                                     # persons employed
WY = hu.loc[Y1]                                                  # one work-year, hours
env_trend = (hu.loc[Y1] - h_cf) * E_Y1 / WY / 1e6                # M work-years/yr
hd = h_de.groupby(h_de.index.year).mean() if h_de is not None else None
env_de = (hu.loc[Y1] - hd.loc[Y1]) * E_Y1 / WY / 1e6 if hd is not None else np.nan
print(f"\nenvelope ({Y1}): US hours {hu.loc[Y1]:.0f}/worker; 1950-80 slope {rate*100:.2f}%/yr")
print(f"  trend-continuation member: gap {hu.loc[Y1]-h_cf:.0f} hrs -> {env_trend:.1f}M work-years/yr")
if hd is not None:
    print(f"  Germany-parity member: gap {hu.loc[Y1]-hd.loc[Y1]:.0f} hrs -> {env_de:.1f}M work-years/yr")
print("  UNATTRIBUTED: rivals (taxes suppressing, preferences, emulation) unresolved; pre-1950")
print("  steeper decline (Huberman-Minns: ~3,100 hrs in 1870) is cited context, not pulled.")

# ---------------- channels ----------------
esi_ann = esi.groupby(esi.index.year).mean()
esi_last = float(esi_ann.iloc[-1]) / 1e3 if esi_ann.iloc[-1] > 1e4 else float(esi_ann.iloc[-1])
print(f"\nchannel 2 ({ESI_LABEL}): ${esi_last:,.0f}B/yr in {int(esi_ann.index[-1])} — the conditioned pipe, ours")
CH2 = (0.5, 1.0)      # M person-yrs/yr, exit-margin employment-lock (GGN 2014 family) — IMPORTED
conf = pd.read_csv(os.path.join(DATA, "ba_degrees_conferred.csv"), index_col=0).iloc[:, 0]
flow = float(conf.iloc[-1]) / 1e6
ny = pd.read_csv(os.path.join(DATA, "nyfed_underemployment.csv"))
recent = pd.to_numeric(ny.iloc[:, 1], errors="coerce").dropna()
under = float(recent.tail(60).mean()) / 100.0
CH4 = (flow * 4 * under * 0.4, flow * 6 * under * 0.6)   # study-yrs x never-escape dial [.4,.6]
print(f"channel 4 (queue/doomed study): conferrals {flow:.2f}M/yr (ours), underemployment {under:.0%} (ours),")
print(f"  years-per-degree [4,6] x never-escape [0.4,0.6] -> {CH4[0]:.1f}-{CH4[1]:.1f}M study-years/cohort-yr")
E_now = emp_ann.iloc[-1] * 1e3 / 1e6
CH3 = (E_now * 0.05 * 0.5, E_now * 0.20 * 1.0)
print(f"channel 3 (slack): employment {E_now:.0f}M x share [.05,.20] x work-fraction [.5,1] -> {CH3[0]:.0f}-{CH3[1]:.0f}M — WIDEST, most contested dial")
print("channel 1 (enclosure-forced participation): NOT YET MEASURED — the P13 panel is the instrument")

rows = [
    ("envelope: trend-continuation", env_trend, env_trend, "unattributed"),
    ("envelope: Germany-parity", env_de, env_de, "unattributed"),
    ("1 enclosure-forced participation", np.nan, np.nan, "open"),
    ("2 insurance-locked (exit margin)", CH2[0], CH2[1], "imported bracket"),
    ("3 slack employment", CH3[0], CH3[1], "contested dial"),
    ("4 doomed study-years", CH4[0], CH4[1], "ours x dial"),
]
out = pd.DataFrame(rows, columns=["item", "lo_Mpy", "hi_Mpy", "status"])
out.to_csv(os.path.join(DATA, "misallocation_firstlook.csv"), index=False)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9.5, 4.6))
ypos = np.arange(len(rows))[::-1]
for y, (name, lo, hi, st) in zip(ypos, rows):
    if np.isnan(lo):
        ax.text(0.55, y, "not yet measured — the channel most native to the paper", va="center",
                fontsize=9, style="italic", color="tab:red")
        ax.plot([0.5], [y], marker="$?$", ms=12, color="tab:red")
        continue
    col = "gray" if "envelope" in name else ("tab:blue" if "insurance" in name else
          ("tab:orange" if "slack" in name else "tab:green"))
    if lo == hi:
        ax.plot([lo], [y], "D", color=col, ms=9)
    else:
        ax.plot([lo, hi], [y, y], lw=7, color=col, alpha=0.65, solid_capstyle="butt")
    ax.text(max(hi, lo) * 1.15, y, st, va="center", fontsize=8.5, color="dimgray")
ax.set_yticks(ypos)
ax.set_yticklabels([r[0] for r in rows], fontsize=10)
ax.set_xscale("log")
ax.set_xlim(0.4, 140)
ax.set_xlabel("million person-years of work per year above the undistorted benchmark (log scale)")
ax.set_title("The misallocation ledger, FIRST LOOK — brackets and dials, not measurements.\n"
             "Envelope rows are unattributed; channel rows carry their status labels.", fontsize=11)
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(DATA, "misallocation_firstlook.png"), dpi=150)
print("\nwrote data/misallocation_firstlook.csv, data/misallocation_firstlook.png")
