# Interior revision, 21 September 2026

This revision starts from the supplied `v5 (3).tex`. The separately supplied revised PDF informs the general bounds and the worked equilibrium; it is not substituted for the original paper. The original paper's structure, historical discussion, empirical series, and closing reflections are retained around the revised argument.

## Main change

The interior task margin and machine recursion remain the starting point:

\[
\frac{w}{r}=\frac{b\gamma(x^*)}{1-a-\lambda\gamma(x^*)}.
\]

The category-price formula is now exact for nonflat schedules. Define the task list's wage-equivalent cost by

\[
L_j^*=\int_{\mathcal X_j}\frac{1}{\gamma_{Lj}(x)}
\min\left\{1,\frac{\gamma_j(x)}{\gamma(x^*)}\right\}dx.
\]

Then

\[
p_j=wL_j^*+rb_j,
\qquad
\frac{w}{p_j}=\frac{1}{L_j^*+b_j(r/w)}.
\]

`L_j^*` includes the cost of machine work expressed in wage units. It is not actual human employment or a fixed technological hours coefficient. Its response can offset a change in the direct rent bill. This is why the exact formula does not establish an unconditional ordering of actual category price changes by non-produced input intensity.

The feasible human method gives `L_j^* <= bar L_j` and the general price bounds. A vanishing wage–rent ratio remains a corollary under the stated replacement and viability conditions, with persistent direct requirements for the non-produced input needed for the consumption-category conclusion. Uniform capability is unnecessary.

## Changes that follow from using an interior economy

- Section 6 replaces the flat-capability proposition with the exact interior formula, general bounds, and income accounting while labor remains employed. One short remark recovers flat cost parity.
- Section 7 retains wage income in household and aggregate receipts. A fixed rent-tax base and no withdrawal upon employment are distinguished from full allocation neutrality; income effects can change participation.
- The old land-only closure is replaced by a solved equilibrium with a strictly increasing task schedule, explicit household participation, and both final-task and machine-sector labor. A separate appendix proves the general income identity and states the conditional CES expenditure result.
- The abstract, introduction, AI discussion, scope statements, and references now point to the interior results. The original assumption of a reduced-form outside option remains identified as a separate benchmark from the explicit household example.
- The exact zero-direct-land equality becomes a general lower bound. Exact equality with the solo-hours benchmark is retained only in the flat-case remark.
- The earlier broad existence assertion is replaced by the scope of the explicit interior example. Payroll incidence is no longer presented as identifying schedule slope on its own.

## Figure changes

The two panels and four eras remain. AI curves retain slope and an illustrative positive training premium. Wall annotations refer to land access and labor scarcity, rather than asserting that participation binds. Dots are labelled as illustrative `w/c` ratios, and interior markers are calculated at their actual curve intersections. The caption specifies different worker-specific task mixes, fixed across eras within each panel.

The figure script includes the caption as `FIGURE_CAPTION`, creates missing output directories, and accepts `--output`. Existing default output behavior is retained.

The follow-up figure revision removes the logistic function entirely from both computing and AI schedules. Smooth convex power curves now keep rising towards each wall, with no sigmoid shoulder or horizontal plateau. Their curvature is explicitly illustrative. Nesting is satisfied by the curves themselves and checked numerically; later curves are no longer clipped against earlier ones. The blue annotation and the paper's caption and historical discussion have been updated accordingly. Wage-ratio levels and wall positions are retained, while interior markers move to their new intersections.

## Standalone presentation and abstract

The manuscript presents the interior model directly throughout the abstract, introduction, results, caption, conclusion, and appendices. References to relaxing an earlier assumption, replacing earlier results, or the verification status of an earlier version have been removed from the paper. The flat schedule appears only in one short special-case remark. Editorial history remains in this handoff note and the source diffs.

The abstract follows the supplied Europe version and contains 138 words by whitespace count, or 147 when compounds and the year range are split. It retains the two empirical figures and describes the interior price result and rent-tax policy at the scope established in the paper. `europe-abstract.txt` provides the plain-text abstract for submission.

The final computation note describes the checks supplied with this paper. This copyedit does not alter the equations or empirical series.

## Non-produced inputs and consolidated discussion

The general theory uses a non-produced input with a fixed service endowment. The definitions of `r`, `b`, `b_j`, and `T`, category-price interpretation, income accounting, and fiscal coverage calculation use that interpretation consistently. Produced energy, structures, and extraction costs remain inside the production recursion. Land is retained as a concrete example for access, enclosure, and the household equilibrium, and as the measured input in the U.S. site-rent application. The empirical rent base has not been broadened to include unmeasured inputs.

The three paragraphs on heterogeneity, closed tasks, and skill premia are merged into one paragraph before Section 6. All displayed equations and empirical figures are unchanged. The abstract remains below 150 words even when compounds and the year range are split.

## Verification

- The replacement derivatives agree with numerical differences to about `3.1e-10` relative error.
- 100 heterogeneous-task examples verify the exact interior price formula.
- 80 sets of heterogeneous assignments, including human-required tasks, verify the category-price bounds and factor-income cancellation.
- The complete example gives `x* = 0.96791136`, `w/r = 0.59840547`, and output `18.47540180`.
- An independent linear production program with 2,048 task cells reproduces output with relative error `3.23e-8` and corroborates the wage–rent ratio through dual prices.
- The paper compiles without unresolved references or overfull boxes. The figure and PDF have been visually reviewed.

The empirical series were not re-estimated. The unchanged figure assets were extracted from the original `laborgeneral (3).pdf`; the eras figure was regenerated from its edited Python source. The new interior results are not claimed to be verified by the earlier Lean files.

## Files and reproduction

`changes.patch` compares this manuscript to the supplied original. `figure-changes.patch` records the Python changes. `check-results.json` contains the numerical output.

From this directory:

```bash
python fig_eras_workers.py --output figures/fig_eras_workers.png
python check_interior.py > check-results.json
pdflatex -interaction=nonstopmode -halt-on-error v5_interior.tex
pdflatex -interaction=nonstopmode -halt-on-error v5_interior.tex
```

The Python dependencies are NumPy, Matplotlib, and SciPy. The LaTeX source uses standard packages including Latin Modern, AMS math, graphicx, booktabs, caption, and microtype. This bundle contains the edited manuscript, figures, and checks; it does not include the upstream empirical data pipeline.
