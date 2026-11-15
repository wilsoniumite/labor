# STATE — walls (resume point)

**Thread:** the upper end of the task schedule: what kind of wall labor faces (the machine chain's soft wall, a hard
wall H, an asymptote), what Appendix B's backward calibration can and cannot say about it, and what lies beyond the
schedule (latent goods: reinstatement). Started 2026-11-15/16 in a session with Stella (her ask, before sleeping:
"explore all these ideas and see which ones you like most; calibrate, check some data, try different ideas, ponder,
repeat"). Nothing here touches `../pinning/`; the paper is her working file.

**Run:** from `walls/`, with numpy, scipy, matplotlib, tqdm (`../venv` on her machine). `checks/check_model.py` gates
`code/model.py` against `../pinning/code/appendix_b.py` (18/18 on 2026-11-16).

## Findings so far (2026-11-16, overnight)

1. **The shares pin a soft wall, whatever the schedule.** Appendix B's two machine-cost targets put the machine chain's
   wall at gamma(x_c)/gamma(x*) = (1 - 0.20)/0.47 = 1.70: every task where people are more than 1.7 times as
   relatively productive as at the margin is closed to machines at any wage (the machines that would do it embody
   more labor than the task takes). In rent units it is an asymptote. Measured counterpart: the lambda thread's US
   full-chain labor share of machinery, 0.53-0.69 over 1967-2023 (1/theta = 1.45-1.9).
2. **The shares cannot see above the margin.** A hard H anywhere above x* leaves the calibrated equilibrium unchanged
   (checked: xH 0.95, 0.90, 0.85 on both roots).
3. **The shares leave one shape parameter free; sigma pins it.** In the scale-free power family gamma = c + x^k, every
   k > 3.88 meets the calibration condition J(x*) = gamma(x*)(1 - x*). Appendix B's two roots (4.355, 15.498) are the
   members with g0 = 0.01. Sigma at the margin (machine services vs labor, final tasks) = 2 gamma/(gamma'(1 - x*)):
   2.29 on the low root, 0.744 on the high root. Literature (verified by search, 2026-11-16): Chirinko 2008 0.40-0.60;
   Oberfield-Raval 2021 0.5-0.7 (US manufacturing aggregate); Gechert-Havranek-Irsova-Kolcunova meta: mean 0.9, 0.3
   after publication-bias correction; Karabarbounis-Neiman 2014 about 1.25 (the high outlier). The low root is outside
   the whole range.
4. **At literature sigma, labor sits just short of the soft wall.** sigma 0.6: gap x_c - x* = 0.026, 84% of labor's
   tasks behind the soft wall; sigma 0.3: 92%; sigma 1.25: 67%; low root (2.29): 35%.
5. **Figure 3's uniform task automation (gamma halved everywhere) raises w/P_s for sigma below 1.63** (+12% at 0.6,
   +22% at 0.3; -3.0% on the low root). Recursive automation lowers it on every member (-11% to -19%).

6. **Where automation lands decides its sign, not sigma** (`code/landing.py`, `results/landing.json`; gamma x 0.5 on
   chosen tasks, schedule re-sorted): machines better at the tasks they already hold: w/P_s +33% to +40% on every
   member; at labor's contestable band (x* to x_c): -9% to -14% on every member; behind the soft wall only: -2% to
   -4%; Figure 3's "everywhere" nets the first two (-3.0% low root, +2.8% sigma 1.25, +12.1% sigma 0.6, +21.9%
   sigma 0.3). The paper's own definition (Section 3.4: "Task automation improves machine capability at tasks near
   the assignment margin") is the contestable-band experiment, negative on every member; Figure 3's experiment
   ("halves gamma at every task") is mostly the productivity effect on machine tasks. Aligning Figure 3 with Section
   3.4 would make Section 5's "both automation channels lower the real wage" hold whatever the root.
7. **Long paths** (eta = 1 ... 0.01): Appendix B's path (lambda 0, gamma x eta) still collapses, but at sigma 0.6 it is
   non-monotone and slow: w/P_s 2.33 -> 2.85 (eta 0.2) -> 1.32 (eta 0.01), participation 0.38 at 0.01 (low root:
   0.35 and 0.14). Machines improving only at the tasks labor held at the start: on the low root labor falls back
   onto the old machine tasks and w/P_s recovers to 2.70; at sigma 0.6 it falls steadily to 1.31.

8. **The soft wall in the data** (`code/soft_wall_data.py`, `figures/soft_wall_data.png`): 1/lambda-hat, the soft
   wall's height over the margin, sits at 1.45-1.92 over 1967-2023 (century arc spliced, family A tot members);
   Appendix B's 1.70 is mid-range.
9. **A second sigma read, from the companion envelope** (`code/flip_check.py`): with R = 1 the share of labor's
   employment flipping per log point of w/p_m is sigma/2, so 2 x flipped mass / log rise of the waterline is a sigma:
   0.08-0.76 across 6 waterline members x 3 flip rules (median 0.24). Same side as the literature; the low root's 2.29
   is out of reach unless occupational flips miss two-thirds of task automation and the waterline is the broad
   equipment one.
10. **Hard wall endgame** (`code/hard_wall.py`): T/h = 5.912 on every member (pinned by the shares); the floor
   (T/h)|H| holds at sigma 0.6 as on the low root; at sigma 0.6 the margin reaches H later (|H| 0.05: at eta 0.001,
   not 0.03).

## Next
- Soft wall from the lambda series (figure). Companion flip rates as a rough cross-check of sigma.
- Latent goods / reinstatement extension. Report.
