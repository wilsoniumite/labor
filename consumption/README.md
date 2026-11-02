# consumption — the bridge's consumption machinery, an LVT dividend through it, and 2022-2026 moves

Blog-support thread (napkin grade, same no-fudging rules as `austax/` and `three-drivers/`: public official
data only, every raw file vendored with a manifest, every headline number recomputed by a check script).
Started 2026-11-02 from two questions about the 2026-06-14 post
*Labor pressures causing market distortion and a minimally invasive solution*:

1. **Would an LVT-funded dividend move consumption the way the VAT bridge does, and how similarly?** The post's
   machinery (net transfers per adult share, quintile/decile market shares θ, Working-model elasticities η,
   an MPC gradient) is rebuilt from the post, gated on its published numbers (the original code was not in this
   repository), and then run with land holdings in place of consumption as the tax base.
2. **Has the US consumption breakdown moved over 2022-2026?** By sector (is care absorbing spending growth the
   way it absorbs job growth, the watch site's "jobs outside care"?) and by income group (is spending held up by
   higher incomes? read from the official distributions directly, and tested against the category composition of
   national-accounts spending).

**Status:** built, independently verified and audited 2026-11-02. `STATE.md` has the answers, her calls, what is
not done and the run order. Python: the repo-root `venv/` (`venv/bin/python -I consumption/...`).

## Layout

| Path | What |
|---|---|
| `STATE.md` | The answers, her calls, what is not done, the run order. Start here. |
| `code/common.py` | Shared helpers: paths, polite downloads, per-source manifests. BLS hosts get Stella's contact address in the User-Agent (approved for BLS, 2026-11-02); no other host does. |
| `code/acquire_*.py` | Five scripts (bls_ce, bea, fed, fin = StatFin + Eurostat, usda): downloads (skipped when vendored; failures go to `FETCH_FAILURES.csv` and are retried only with `--retry-failed`) and a deterministic tidy build. `raw/post`, `watch`, `other` and `ecb` were fetched once through `common.fetch`. |
| `data/raw/<source>/` | Vendored raw files, never modified, each folder with `MANIFEST.csv` (url, date, sha256, bytes, use). |
| `data/tidy/` | Tidy CSVs built from raw (`README_<source>.md`), plus `post_published_numbers.csv`, the hand-transcribed gate list (`README_post.md`). |
| `rebuild/` | The post's machinery rebuilt (US CE 2024 deciles, Finland HBS 2022 quintiles): `bridge.py`, runners, gates (`checks/gate_*.py`), verifiers, NOTES. |
| `lvt/` | Question 1: the LVT dividend through the same machinery, beside the VAT bridge (US, Finland). |
| `recent/` | Question 2: sector contributions (`sectors.py`), direct reads of the official distributions (`direct.py`), the income-group fingerprint test (`fingerprint.py`). |

Each unit has `code/`, `checks/` (`check_*.py`, or `gate_*.py` in rebuild; plus `verify_independent_*.py`), `out/`,
`figures/` and `NOTES*.md`.
