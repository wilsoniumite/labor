# diag_reconstruction.py — find the exact construction behind BEA's published
# IxC Total Requirements (Summary), so the domestic variant can inherit it.
# Candidates follow BEA Concepts & Methods ch.12: market-shares W from the Make
# table, direct requirements B (published CxI_DR), scrap ('Used') removed from
# market shares with the non-scrap ratio h, noncomparable imports ('Other')
# excluded from the recursion.

import io, os, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
YR = "2023"

def parse(df):
    col_codes = [str(c) for c in df.iloc[5, 2:]]
    row_codes = [str(c) for c in df.iloc[7:, 0]]
    body = df.iloc[7:, 2:]
    body = pd.DataFrame(pd.to_numeric(body.stack(), errors="coerce").unstack().values,
                        index=row_codes, columns=col_codes)
    ok = lambda c: c != "nan" and " " not in c and len(c) <= 8
    return body.loc[[c for c in body.index if ok(c)],
                    [c for c in body.columns if ok(c)]]

def load(zname, fname, sheet=YR):
    z = zipfile.ZipFile(os.path.join(CACHE, zname))
    return parse(pd.ExcelFile(io.BytesIO(z.read(fname))).parse(sheet, header=None))

tr = load("AllTablesSUP.zip", "IxC_TR_1997-2023_Summary.xlsx")
dr = load("AllTablesIO.zip", "CxI_DR_1997-2023_Summary.xlsx")
mk = load("AllTablesIO.zip", "IOMake_After_Redefinitions_PRO_1997-2023_Summary.xlsx")
us = load("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx")

inds = [i for i in tr.index if i in mk.index]              # 71 industries
coms_pub = list(tr.columns)                                 # incl Used/Other
print("published TR:", tr.shape, "| DR:", dr.shape, "| Make:", mk.shape)
print("DR rows head/tail:", list(dr.index[:3]), list(dr.index[-3:]))
print("Make cols tail:", list(mk.columns[-4:]))

q_row = "T007" if "T007" in mk.columns else None
print("make col T007 present:", q_row is not None)

def err(TRc, coms):
    common = [c for c in coms if c in coms_pub]
    A = pd.DataFrame(TRc, index=inds, columns=coms).loc[inds, common]
    Bm = tr.loc[inds, common]
    return float((A - Bm).abs().max().max())

# commodity output q from Make row sums (industries' production), scrap col name 'Used'
V = mk.loc[inds, [c for c in mk.columns if c in coms_pub]].fillna(0.0)
coms = list(V.columns)
q = V.sum(axis=0)
g = mk.loc[inds, "T008"] if "T008" in mk.columns else V.sum(axis=1)
Bfull = dr.loc[[c for c in dr.index if c in coms], inds].fillna(0.0).reindex(index=coms).fillna(0.0)

def build(drop=(), scrap_h=False, row_scale=True):
    keep = [c for c in coms if c not in drop]
    Vk = V[keep]
    qk = q[keep]
    if scrap_h:
        scrap_cols = [c for c in ("Used",) if c in coms]
        h = (g - V[scrap_cols].sum(axis=1)) / g
    else:
        h = pd.Series(1.0, index=inds)
    W = (Vk.values / np.where(qk.values[None, :] == 0, np.nan, qk.values[None, :]))
    W = np.nan_to_num(W)                                   # i×c over keep
    Bk = Bfull.loc[keep, inds].values                       # c×i
    Ic = np.eye(len(keep))
    TRc = W @ np.linalg.inv(Ic - Bk @ W)
    if scrap_h and row_scale:
        TRc = TRc / h.values[:, None]
    return TRc, keep

for name, kw in [
    ("naive (all coms)",               dict(drop=())),
    ("drop Used+Other",                dict(drop=("Used", "Other"))),
    ("scrap-h, keep Other",            dict(drop=("Used",), scrap_h=True)),
    ("scrap-h + drop Other",           dict(drop=("Used", "Other"), scrap_h=True)),
    ("scrap-h no rowscale, drop U+O",  dict(drop=("Used", "Other"), scrap_h=True, row_scale=False)),
]:
    try:
        TRc, keep = build(**kw)
        print(f"{name:32s} max|err| = {err(TRc, keep):.3e}")
    except Exception as e:
        print(f"{name:32s} FAILED {type(e).__name__}: {e}")
