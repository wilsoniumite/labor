# consumption — the bridge's consumption machinery, an LVT dividend through it, and 2022-2026 moves

Blog-support thread (napkin grade, same no-fudging rules as `austax/` and `three-drivers/`: public official
data only, every raw file vendored with a manifest, every headline number recomputed by a check script).
Started 2026-11-02 from two questions about the 2026-06-14 post
*Labor pressures causing market distortion and a minimally invasive solution*:

1. **Would an LVT-funded dividend move consumption the way the VAT bridge does, and how similarly?** The post's
   machinery (net transfers per adult share, quintile/decile market shares θ, Working-model elasticities η,
   an MPC gradient, and a two-channel macro block) is rebuilt from the post, gated on its published numbers
   (the original code was not in this repository), and then run with land holdings in place of consumption
   as the tax base.
2. **Has the US consumption breakdown moved over 2022-2026?** By sector (is care absorbing spending growth the
   way it absorbs job growth, the watch site's "jobs outside care"?) and by income group (is spending held up
   by higher incomes? tested against the category composition of national-accounts spending).

## Layout

| Path | What |
|---|---|
| `code/common.py` | Shared helpers: paths, polite downloads, per-source manifests. BLS hosts get Stella's contact address in the User-Agent (approved for BLS, 2026-11-02); no other host does. |
| `code/acquire_*.py` | One script per source family: downloads (skipped when vendored) and builds `data/tidy/` deterministically. |
| `data/raw/<source>/` | Vendored raw files, never modified, each folder with `MANIFEST.csv` (url, date, sha256, bytes, use). |
| `data/tidy/` | Tidy CSVs built from raw, documented in `README_<source>.md`. |
| `rebuild/` | The post's machinery rebuilt (US CE 2024 deciles, Finland HBS 2022 quintiles) and its gates. |
| `lvt/` | Question 1: the LVT dividend through the same machinery, beside the VAT bridge. |
| `recent/` | Question 2: sector contributions, the income-group fingerprint test, direct reads. |

Status: in progress (see `STATE.md` once written). Python: the repo-root `venv/` (`venv/bin/python -I ...`).
