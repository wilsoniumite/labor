# STATE — walls (resume point)

**Thread:** the upper end of the task schedule: what kind of wall labor faces (the machine chain's soft wall, a hard
wall H, an asymptote), what Appendix B's backward calibration can and cannot say about it, and what lies beyond the
schedule (latent goods: reinstatement). Started 2026-11-15/16 in a session with Stella. Her ask, before sleeping:
"explore all these ideas and see which ones you like most; calibrate, check some data, try different ideas, ponder,
repeat". Nothing here touches `../pinning/`; the paper is her working file, and every change it suggests is hers to
make.

**Read first:** `REPORT.md`, which has the findings ranked, figures, tables, the suggestions for the paper with my
lean, caveats and sources.

**Run:** from `walls/`, with numpy, scipy, matplotlib and tqdm (`../venv` on her machine; the session used a scratch
venv). `checks/check_model.py` gates `code/model.py` against `../pinning/code/appendix_b.py` (18/18 on 2026-11-16).
Each script in `code/` writes its `results/*.json` and, where it draws, `figures/*.png`. `code/sigma_figure.py` reuses
its JSON unless given `--recompute`.

## State as of 2026-11-16

Done: the closed-form backward calibration and its free shape parameter; sigma at the margin against the literature
(verified by search) and the companion envelope; the soft wall from the lambda series; the first-order formula
(contestable share = s_M sigma ln(1/theta)) on two schedule families; where automation lands; long paths; the
hard-wall endgame; latent goods in partial equilibrium; a complete-schedule figure; the evening's mock-ups ported
(`code/toys_wall_shapes.py`, `code/toy_law_only.py`, `code/calib_options_first_pass.py`).

The headline numbers (details and sources in REPORT.md):
- The soft wall sits at gamma(x_c)/gamma(x*) = 1.70 from the shares; 1/lambda-hat was 1.45-1.92 over 1967-2023.
- Sigma at the margin is 2.28 on the printed instance. The literature gives 0.3-0.7 and the companion envelope
  0.08-0.76. At literature sigma, 77-94% of labor's tasks sit behind the soft wall.
- Gamma halved on labor's contestable band (Section 3.4's definition) moves w/P_s by -7% to -14% on every member.
  Gamma halved everywhere (Figure 3) flips sign near sigma 1.6 (+12% at 0.6).
- The hard-wall floor along the automation path is (T/h)|H| = 5.9|H| on every member.
- Latent goods: general-purpose automation switches them on already automated; reinstatement with people starts only
  once the real wage turns down.

## Open (not started)

- Latent goods in general equilibrium: reinstated labor feeding back on the wage, with buyers' budgets (owners vs
  workers).
- Machine-specific theta: the soft wall per machine type (computers' lambda-hat vs equipment's), and for AI services.
- If she takes REPORT.md section 7's item 1 or 2: a port into `pinning/` (Figure 3's experiment, Appendix B's sigma
  sentence or eighth target), following the paper's contract (word diffs, her one-word decisions).
