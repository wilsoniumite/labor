# dynamics — the dynamic extension (a later paper)

The v2 dynamic rewrite of *Pinning the Wage to Scarcity and Technology*: capital as
time (waiting and build lags), one dynamic environment declared once, the main text as
its steady state, and one transition act hinged on a machine-checked steady-state
equivalence lemma. Adopted 2026-08-27 (brief: `docs/rewrite_brief_pinning_v2.md`),
engine built and verified 2026-08-28, draft executed the same day, voice-normalized
2026-08-30. The paper being submitted took the static route (`../pinning/`); this
thread is what its Future Work section's first paragraph points to.

**Start with `STATE.md`.** Logs 31–37 are this thread's own; the other logs are the
pinning paper's history under this folder's old name, the-link-revision.

- `paper/pinning.html` — the v2 dynamic draft, canonical for this lineage;
  `paper/snapshots/` holds its pre-surgery states (house rule: snapshot before any
  structural edit).
- `code/dynamics/` — the transition engine: `model.py` (environment, both steady states,
  the hard gate), `solve.py` (the validation ladder and the T1–T3 and T5 experiments),
  `figures.py` (the four transition figures), `results_dynamics.json` (verdict record).
- `checks/` — `check_dynamics.py` (54 checks: the user cost of capital, the equivalence
  lemma, the ledger, T1's closed form, T4's algebra; writes `dynamics_ss_targets.json`),
  `lint_pinning.py` (mechanical sweeps and the claim-status-tag family over the HTML),
  `census_symbols.py` (the symbols-earn-their-ink census).
- `code/html_to_latex.py` generates `latex/main.tex` from the HTML with word-fidelity
  verification; `code/italicize_math.py` is the idempotent variable italicizer (new
  prose is written bare); `code/fig_model_schematics.py` and `code/fig_eras.py` draw the
  HTML's schematics.
- `docs/` — the two frozen rewrite briefs, `notation_map.md` (the v1 to v2 symbol map),
  `reading_guide.md` (the literature behind the paper, ordered by load).
- `figures/` and `latex/` — the draft's figures and the generated LaTeX
  (`latex/README.md`).

Prose-maintenance loop: write bare, run `italicize_math.py`, run lint. Never hand-wrap.
