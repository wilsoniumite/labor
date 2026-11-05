# Verify-phase verdicts on the merged design (full text)

Source: the model-section design workflow (wf_3218f051-79c). Each claim was checked analytically and numerically by separate agents.


## C1 (analytic): holds_with_conditions

### Conditions
STATED ECONOMY (Definition 1, synthesis 483-499): (a)-(c) hold in every equilibrium exactly as worded, and (d) is vacuous there because b > 0. They need only what the drafted assumptions already give:
- rho = 1/beta - 1 >= 0 (Ass. 5, synthesis 457);
- delta in (0,1] and (rho+delta)a < 1, implied by Ass. 2's (rho+delta)(a+lambda*gamma(0)) < 1 (383);
- b > 0, which gives tilde-b_m > 0;
- Y = C >= N > 0, which follows from (budget) with nonnegative instruments (446).
The P_s identity uses only the clearing conditions, so it holds under every policy.

"Equality when rho = 0" is sufficient, not necessary. tilde-lambda = L also when lambda = 0 (the automation path), and P_s = wL_s + rB_s also when X = 0 (a corner). So the remark at synthesis 878 ("only when rho = 0") is exact only at margins with X > 0.

NETWORK (Def. B.1 under Ass. B.1, synthesis 1090-1119): (a), (b) and (d) hold. Three conditions apply.
(1) In (c), gamma(x*) must mean w/p_m. It equals gamma_i(x_i*) only if each task-produced good's open tasks, relabeled, form an interval on which gamma_i is continuous. That is the convention of Ass. 1 (synthesis 375-378) and main.tex 158 ("relabeled schedule is continuous").
- Ass. B.1 allows any X_i of positive measure, with gamma_i continuous "on its open tasks". That admits a jump across a gap.
- At such a jump, the sentence at synthesis 1105 ("at every interior margin gamma_i(x_i*) = w/p_m") is false. The margin condition is then only the inequality gamma(x*-) <= w/p_m <= gamma(x*+), as at a boundary assignment.
- Fix: require X_i to be an interval, or require the relabeled schedule to be continuous.
(2) Ass. B.1 allows operating inputs to the machine-hour, but Def. B.1 inherits (ownerseq) (462), which credits the owner with p_m*X. With an operating bill o > 0:
- the budgets overstate income by o*X, so Walras's law fails;
- the owner's return is rho + o/p_K > rho, so Lemma A.1(c) rules out an optimal constant plan with c_o > 0.
- No equilibrium with machines in use exists, so C1 is only vacuously true for such networks. The derivation at main.tex 671 assumes "no separate operating costs".
- Fix: credit the owner with the machine rental (rho+delta)*p_K*X, with p_m = rental + operating cost. (a)-(d) then carry over unchanged, because they use only condition (i).
(3) Ass. B.1 replaces Ass. 2, which is where delta in (0,1] is introduced (383), so Ass. B.1 must restate delta.

### Evidence
Each part was derived analytically and then checked independently by verify_C1.py, which passes 14 of 14 checks. Part (c) was also tested by constructing full network equilibria.

(a) Def. 1(i) (synthesis 486) imposes (unitcost) (401-405) and the user cost, so p = A_rho*p + lambda*w + b*r, with A_rho as in (3) (409-415). For a general M, row 1 holds int_M gamma and |[0,1]\M|.
- A_rho is block triangular with eigenvalues 0, 0 and +-sqrt((rho+delta)a) (check A1).
- So (I - A_rho)^-1 = sum_t A_rho^t >= 0, and its entries are nonnegative ratios over 1 - (rho+delta)a (A2, A3). tildem (424-427) is confirmed.
- In Def. B.1 (1102), productivity of A_rho is imposed, so (a) is immediate there.

(b) rho >= 0, and A_rho - A_0 = rho*e_m*e_K' >= 0, because only machine-hours use machines.
- 0 <= A_0 <= A_rho gives (I - A_0)^-1 <= (I - A_rho)^-1, with equality at rho = 0 for every delta.
- In closed form, the gap is rho*lambda/[(1-(rho+delta)a)(1-delta*a)] for tilde-lambda_m, and the same with b for tilde-b_m (A4).
- From (I - A_0')y = Cz: P_s*Y = ((I - A_0)p)'y = w*N_a + r*ell + rho*V_m*X. Dividing by Y gives the identity (A5). It matches main.tex 717.

(c) Def. 2 (506) gives w > 0 and p_m > 0. With gamma continuous and strictly increasing on [0, x_H] (Ass. 1), Def. 1(i) gives w = p_m*gamma(x*).
- The machine-hour row then gives p_m(1 - gamma*tilde-lambda_m) = r*tilde-b_m > 0, so the feedback term is positive and (5) follows.
- 1 - gamma*tilde-lambda_m = D(x*)/(1-(rho+delta)a), so it is positive exactly when x* < x_c (A6).
- The old hypotheses at main.tex 232 become conclusions in the stated economy.

(d) If tilde-b_m = 0, then p_m = w*tilde-lambda_m, so w/p_m = 1/tilde-lambda_m at every wage. An interior margin then needs gamma*tilde-lambda_m = 1, and (5) reads 0/0.
- D1 builds a funded network equilibrium with b_K = 0, r = 1 and an interior margin.
- There x* = 0.94634 is pinned by technology alone, and w/r = 0.022872 is set by the labor market.

Instance (main.tex 745):
- gamma(x*) evaluated from the schedule is 0.445790, equal to w/p_m.
- (5) on price coefficients gives 0.071654, the solver's v. On physical coefficients it gives 0.011620 (B1).
- P_s = 0.0259890 on both decompositions; tilde-lambda_s 0.26581 >= L_s 0.19967 (B2).

j4 rerun: 365 networks, 314 interior margins, 73 with rho = 0. Price identity error 6.66e-13; closure error 1.90e-13; price coefficients >= physical ones, and equal at rho = 0.
- But j4 and S1b both set g* = w/p_m. With that choice, (5) is algebra implied by (a) (F1). So those checks test (a), not the margin condition in (c).

Why it matters: Prop. 2, Prop. 4 (p <= w by cost minimization, p >= r*tilde-b_g) and Cor. 2 (P_s >= h*r) use only price coefficients, so durable machines need no qualifier there. Only the readings at main.tex 245 and 257 need rho = 0. The b-tilde_m > 0 hypothesis fixes the theorist's flaw: D1 shows that without it the closure is 0/0.

### Counterexample
No counterexample to (a), (b) or (d), or to (c) in the stated economy.

1. Against (c) as worded for networks, and against the sentence defining gamma(x*) at synthesis 1105, under Ass. B.1 as drafted.
- Technology: a task good g has open tasks X_g = [0, 0.5] U [0.8, 1], with gamma = 0.01 + 0.03x on the first piece and gamma = 3 + x on the second. This is continuous and nondecreasing on its open tasks, as Ass. B.1 requires.
- Machines and parameters as in the instance: a = 1.4, lambda = 7.3, b = 0.4, delta = 0.05, rho = 0.09; N = 1, h = 0.0017, T = 0.00557, chi uniform on [0, 2.2].
- A funded equilibrium exists: participation 0.600, c_o = 0.303, Walras residual 4e-16.
- In it, machines do [0, 0.5] and labor does [0.8, 1], which is an interior margin in Def. 2's sense, with x_g* = 0.5 and gamma_g(x_g*) = 0.025.
- But w/p_m = 0.16969 and w/r = 0.015069.
- (5) evaluated at gamma_g(x_g*) gives 0.001798. Evaluated at w/p_m it gives 0.015069, which is correct only as an identity.

2. A case where C1 holds only vacuously.
- At the instance, add operating labor of 0.5 hours per machine-hour, which Ass. B.1 allows.
- Then (ownerseq), as Def. B.1 inherits it, puts budget income at 0.232543 against P_s*Y = 0.208289. The excess is lambda_m*w*X = 0.024255.
- The owner's return is 0.1302, above rho = 0.09.
- So no equilibrium of Def. B.1 with machines in use exists, and j4's networks, nearly all of which have operating inputs, are price systems rather than equilibria.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/_verify_C1/verify_C1.py


## C1 (numerical): holds_with_conditions

### Conditions
STATED ECONOMY (synthesis Definition 1, synthesis.md 483-499, with Assumptions 1-5 at 374-458): parts (a)-(d) hold exactly as stated, with no added condition. b~_m = (rho+delta)b/[1-(rho+delta)a] > 0 follows from b > 0 and delta > 0. Proposition 1's w = p_m gamma(x*) follows from Assumption 1, which makes gamma continuous on the interval [0, x_H] (proof at synthesis.md 652).

NETWORKS (Definition B.1 under Assumption B.1, synthesis.md 1091-1102):
- (a) and (b) hold as stated.
- (c), and the step in (d) that "an interior margin forces gamma(x*) lt_m = 1" (synthesis.md 1236), both need gamma_i(x_i*) = w/p_m at every interior margin. synthesis.md 1105 asserts this without proof.
- It is true only if Assumption B.1 gains one clause: each task-produced good's open tasks, relabeled as in Section 2.1 (synthesis.md 378), form an interval [0, x_H,i] on which gamma_i is continuous and nondecreasing.
- As drafted, B.1 allows "a set X_i in [0,1] of positive measure" and asks only that gamma_i be "continuous and nondecreasing on its open tasks". So the open tasks may have a gap across which gamma_i jumps. Closed tasks in the middle of an interval do the same, if "as in Section 2.1" is not read as placing them last.
- With such a gap, gamma_i(x_i*) < w/p_m at a margin that is interior by Definition 2 (synthesis.md 505-507), applied good by good. Then (5) misses w/r, and when b~_m = 0 it evaluates to 0 rather than 0/0.
- Without the clause, (c) survives only if gamma(x*) is defined as w/p_m. That reduces (5) to the machine-hour price row and removes its pinning content.
- The same gap undermines the remark after Prop. 2 (synthesis.md 678: "holds in any production network") and Prop. B.1(b) (1110).
- main.tex avoided this: 157-158 require the relabeled schedule to be continuous, and 232 takes w = p_m gamma(x*) as a hypothesis.

PORTING NOTE: (b) is correct in the four-good form of synthesis eq:3 (409-415), where lambda and b carry no rho+delta. main.tex's three-row form (713-715) puts rho+delta into lambda and b as well. There, swapping A for A_0 alone gives 1.098925 machine-hour hours on the instance, against 0.392473 physical.

### Evidence
All scripts are in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/:
- c1_stated.py
- c1_networks.py, with its output in c1_networks_out.txt
- c1_relabel.py
- c1_gap_sweep.py
- c1_threerow.py

The checks avoid circularity. Equilibria are found in wage space from the cost equations and the labor market, never from the closure. gamma(x*) is read off the schedule, never set to w/p_m.

1. Symbolic (sympy, four-good eq:3).
- eq:tildem follows from the 4x4 inverse.
- lt - lt_phys = rho*lam*(J, 1, a, 0)/[(1-a*delta)(1-(rho+delta)a)], and bt - bt_phys is the same with b in place of lam. Both are >= 0 and zero exactly when rho = 0, for every delta.
- P_s - [w L_s + r B_s + rho V_m X/Y] = 0 identically, given X/Y = J/(1-a*delta).
- The closure is exact given w = gamma p_m.

2. The instance, through appendix_b.solve (imported read-only, -B, no bytecode written).
- x* = 0.829869; gamma(x*) = 0.445790 = w/p_m.
- lt_m = 1.271144 and bt_m = 0.069652, both matching eq:tildem; price identity error 5.2e-16.
- Basket coefficients on the price basis against physical: lt_s 0.265811 vs L_s 0.199673; bt_s 0.006943 vs B_s 0.003319.
- P_s = 0.0259890 = w L_s + r B_s + rho V_m X/Y (relative error 2.7e-16); w L_s + r B_s alone is 0.0176260. main.tex 717 states the same identity.
- Feedback term 0.433336.
- (5) on price coefficients gives 0.071654 (relative error 1.2e-15 against v, main.tex 745); on physical coefficients it gives 0.011620. Both numbers in the claim reproduce.

3. 600 random stated equilibria from 4,084 draws, each verified against every condition of Definition 1.
- What is checked: cost minimization almost everywhere on a 20,001-point grid; the unit-cost equations; the user cost; clearing of labor, machine-hours and land; Y = C from the budgets; c_o >= 0.
- What varies: a wall x_H <= 1; five gamma families; three F's; rho in {0, (0, 0.3), (0.5, 3)}; delta in {1, 1e-6 to 1e-3, (0.01, 1)}; productivity within 1e-7 of its limit in some draws.
- Mix: 317 interior, 283 boundary, 150 with rho = 0.
- Worst errors: price identity 6.2e-15; basket identity 6.8e-14; closure 1.5e-13; |gamma(x*) - w/p_m| 1.4e-15.
- No price coefficient fell below its physical one, and the two were exactly equal at rho = 0. The feedback term was positive throughout (minimum 1.3e-3).
- 150 zero-rent equilibria also pass (a) and (b) (error 2.8e-16). At the 28 interior ones, gamma(x*) lt_m = 1 to within 6.7e-16.

4. Thirteen boundary cases, in floats and in 50-digit mpmath.
- Cases: the flow benchmark; rho = 0 with delta = 0.05 and 0.5; delta = 1 with rho = 0.09; delta = 1e-6 with rho = 0.09 and with rho = 0; rho + delta = 3; (rho+delta)a = 1 - 1e-9; (rho+delta)(a + lam gamma(0)) = 1 - 1e-6; lam = 0; eta = 0.5; eta = 1e-3.
- In 50 digits every case holds to within 6.3e-48.
- In floats the error reaches 8.8e-8 only where cond(I - A_rho) = 5.3e10. That is rounding, not a failure.

5. Networks under Assumption B.1 with interval task sets.
- Setup: exact piecewise-linear gamma_i with flat stretches; operating inputs; walls; machines built partly from task goods; several methods per good.
- 500 networks at arbitrary (w, r), giving 380 interior margins. Worst errors: Bellman fixed point 1.2e-14; price identity 4.0e-14; closure 1.2e-12.
- 150 networks with exact ties, each under 5 splits of the tied tasks, giving 822 interior margins; closure 7.0e-14.
- 120 full equilibria verified against Definition B.1 (least-cost prices, clearing on A_0, Walras from the budgets, funded support), with 128 interior margins; closure 7.2e-15.
- Price coefficients were never below physical ones, and exactly equal whenever rho = 0.
- Part (d): in 200 networks whose machine chain uses no land, bt_m = 0 exactly and |gamma lt_m - 1| <= 7e-14. w/p_m is the same at w/r = 0.1, 1 and 10, so the closure is 0/0 and does not pin w/r.
- In this continuous case the network checks of (c) are close to identities by construction. The substantive test is the gap case in item 7.

6. The judge's j4_networks.py, rerun.
- Its numbers reproduce: 365 networks, 314 interior margins, closure error 1.90e-13.
- But j4 sets gstar = w/p[1], so that "closure error" is the machine-hour price identity, not the closure. Its 400-cell step schedule could not test gamma(x*) = w/p_m anyway. The claim's "Checked" line therefore does not back (c).

7. Gap counterexamples (item 2 of the counterexample).
- Relabeling the counterexample's open tasks onto an interval exposes a jump of 1.5 in gamma, which the corrected clause excludes.
- A continuous bridge across the jump restores the result: gamma(x*) = w/p_m = 1.041215, and the closure 0.203145892 equals w/r.

8. The repository is unchanged by me.
- I ran only read-only git commands.
- STATE.md changed during the run through commit 34cfc95 (15:17:44), made by another session. git status is clean.

### Counterexample
This is a counterexample under the literal Assumption B.1 (synthesis.md 1091), and only there. Nothing in the stated economy fails.

The economy has four goods: K, m, space, and a final good g.
- Tasks: X_g = [0, .3] U [.6, 1], with closed tasks (.9, 1] and gamma_Lg = 1.
- Schedule: gamma_g = .2 + x on [0, .3] and 2 + (x - .6) on [.6, .9]. It is continuous and nondecreasing on its open tasks.
- Machines: a = .5 machine-hours, lambda = 1 hour and b = 1 land per machine; delta = .1, rho = .05; no operating inputs.
- Households: the basket is one unit of g plus h = .5 of space; N = 1, T = .7, chi uniform on [0, .498210].

The wage scan finds an equilibrium that satisfies every condition of Definition B.1: least-cost prices, clearing on A_0, Walras from the budgets, and funded support (c_o = .187).
- Prices: w/r = .193548 and p_m = .193548, so w/p_m = 1.
- Assignment: machines do [0, .3) and labor does [.6, 1]. The margin is interior by Definition 2.
- Participation is .563; r > 0 and bt_m = .1622 > 0.

The closure fails at this equilibrium.
- x_g* = .3 (the essential supremum of machine tasks), and gamma_g(x_g*) = .5, not w/p_m = 1.
- (5) at that gamma gives w/r = .088235 against .193548, 54% low.
- Reading gamma at the first labor task (2.0) gives .48.
- Only gamma(x*) := w/p_m reproduces w/r, and then (5) is just the machine-hour price row.
- The feedback term stays positive (.919), so only the value of (5) fails.

The same gap breaks part (d).
- Set lambda = 6 and b = 0, so the machine chain uses no land, and chi_max = .5. This is again a funded equilibrium (c_o = .148).
- w/p_m = 1/lt_m = 1.0278, but gamma_g(x_g*) lt_m = .4865, not 1.
- (5) therefore evaluates to 0/.5135 = 0, not 0/0, against w/r = .2394.

The failure is generic. Across 200 random gap economies verified as equilibria, (5) misses w/r by between 1.0% and 99.4% (median 30%).

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/


## C2 (analytic): holds_with_conditions

### Conditions
1. The core holds as stated, under the drafted Definition 1 and Definition B.1. That core is the human-chain bounds, the stated-economy fork, w/r -> 0, w/P_s -> 0 and N_a/N -> 0. It needs the instruments to stay in their drafted ranges: d >= 0, g_e >= 0, tau_w in [0,1), and one support basket in both work and exit. It also needs Assumption 4 (F continuous, F(0) = 0). Two hypotheses can be weakened:
- "F fixed" can become F_k(eps_k) -> 0 whenever eps_k -> 0.
- "g_w <= g_e" is sufficient but not necessary. It can become (g_w - g_e)^+/(P_s + d + g_e) -> 0.
A head tax (d < 0), or support withdrawn in exit, would break the participation limit. The drafted Definition 1 rules out both.

2. The counterexample sentence (synthesis line 1259: "g_w - g_e = theta P_s gives N_a/N >= F(log(1+theta))") is true only when d = g_e = 0, which is the case S5 ran. In general:
- N_a/N >= F(log(1 + theta P_s/(P_s + d + g_e))).
- This equals F(log(1+theta)) only when (d + g_e)/P_s -> 0.
The sentence should say "with d = g_e = 0 and g_w = theta P_s", or give the general formula. Its conclusion still stands: g_w <= g_e cannot simply be dropped, for any theta with F(log(1+theta)) > 0.

3. The upper bound on purchasing power, (w/r)/b~_i, needs b~_i > 0.
- In the stated economy this is automatic. Definition 1 has no corner equilibrium with w > 0, so b~_g = b~_m J(x*) > 0, and the reading holds in every equilibrium with w, r > 0.
- In networks it must be assumed. Proposition B.1(c) rightly keeps it.

4. The human-chain bound needs three things:
- spectral radius of A-bar_S below one (it fails without it; see T5);
- Definition B.1's clause that no feasible method costs less than the price;
- finite chain coefficients.

5. w is the gross wage. With tau_w > 0, the net wage buys (1 - tau_w) w/p >= 1 - tau_w units of the final good.

6. Scope. Suppose the wall is fixed with |H| > 0, T/N is fixed and B_s is bounded. Then labor demand is at least T|H|/B_s, so N_a/N -> 0 is impossible. An interior sequence with gamma b~_m -> 0 must therefore end in a boundary assignment, as the remark after Theorem 1 says (synthesis 747-749), and the participation limit is vacuous there. It has force when H is empty, as on Appendix B's path (main.tex 747).

### Evidence
Lower bound, any good. Definition B.1 (synthesis 1102) requires p = A_rho p + lambda w + b r with spectral radius of A_rho below one. The Neumann series then gives p = w lambda~ + r b~ with lambda~, b~ >= 0, so p_i >= r b~_i for every good (main.tex 209-219, 647-650).

Upper bound. Definition B.1's clause that no feasible method costs less gives p_S <= A-bar_S p_S + lambda-bar_S w + b-bar_S r, entry by entry. A-bar_S >= 0 preserves the inequality under substitution, and A-bar_S^t p_S -> 0 because the spectral radius is below one. So p_S <= (I - A-bar_S)^{-1}(lambda-bar_S w + b-bar_S r). This is main.tex (19) (646-651), with the chain made explicit.

Stated economy.
- Definition 1(i) (synthesis 486) gives p_m gamma <= w on M. So p = w|[0,1]\M| + p_m times the integral of gamma over M, which is at most w. Here lambda-bar_g = 1 because gamma_L = 1 (main.tex 685, 348), and b-bar_g = 0.
- The machine rows (synthesis 401-427) give p_m = w lambda~_m + r b~_m, so p >= r b~_m J(x*) = r b~_g.
- Space rents at r, so w/p_h = w/r.
- There is no corner. With |M| = 0, Definition 1(v) gives X(1 - a delta) = 0, so X = 0 and N_a = Y <= N. But the budget (synthesis 445-447) gives Y = C >= N + (1 - tau_w) w N_a/P_s > N. Contradiction.

Limits.
- The machine row and w = p_m gamma give w(1 - gamma lambda~_m) = r gamma b~_m (main.tex 231-241, 631). With w > 0 (Definition 2) and the xi bound, r > 0 and w/r <= gamma b~_m / xi -> 0 (main.tex 371).
- P_s >= r b~_s >= r B_s, by Lemma 1(iii) (synthesis 634; main.tex 717) and A_rho >= A_0 entrywise.

Participation. The drafted budget gives the work threshold chi* = log[(P_s + (1 - tau_w) w + d + g_w)/(P_s + d + g_e)], the same form as main.tex (27) at 779-786.
- sympy: (1 + w/P_s) - ratio = [P_s(tau_w w + g_e - g_w) + w(d + g_e)] / [P_s(P_s + d + g_e)] >= 0. Hence N_a/N <= F(log(1 + w/P_s)) -> F(0) = 0.
- sympy: with g_w = g_e + theta P_s, ratio = 1 + [theta P_s + (1 - tau_w) w]/(P_s + d + g_e).

Numerical checks.
- j4 rerun gives a largest violation of 3.18e-16. But j4's chains never contain the task good: it rejects any human method that uses goods 0-2.
- My T4 puts the task good, with all tasks to labor, in the chain, along with cycles among human goods and space. Over 1,461 durable networks the largest upper violation is 4.2e-16, the lower bound is never violated, and the bound binds for a non-space good in 387 of them.
- An independent solver reproduces S5: equal payments 0.5160 -> 0.0002 at eta = 1e-5; in-work payment 0.5855 -> 0.0830, against F(log 1.2) = 0.082873.
- Every point was solved as a funded equilibrium of Definition 1: tau_R <= 0.371, c_o >= 0.30, government budget and C = Y within 1e-14. S5 itself did not check funding.
- The stated-economy fork shows no violation at 20,000 random configurations. At the instance, w/p = 2.95 <= (w/r)/b~_g = 13.67.
- Script: verify_C2.py, output in run2.txt; 13 of 13 PASS. Nothing under /home/user/labor was changed (git status is empty).

### Counterexample
This counterexample is to the general form of synthesis line 1259 ("g_w - g_e = theta P_s gives N_a/N >= F(log(1+theta))"), not to the bounds or the limits.

Setting: Appendix B's path (main.tex 747), with lambda = 0, gamma_eta = eta(0.01 + 0.99x^4.4), the instance's other parameters and chi uniform on [0, 2.2]. Each policy below is funded by a rent tax and solved as an equilibrium of Definition 1 at every eta from 1 to 1e-6.

(a) An exit payment as well. g_e = 0.2 P_s, g_w = 0.4 P_s (theta = 0.2), d = 0, tau_R <= 0.371. N_a/N tends to F(log(1.4/1.2)) = 0.0701; it is 0.07008 at eta = 1e-6. That is below F(log 1.2) = 0.0829.

(b) A rent dividend. g_w = 0.2 P_s, g_e = 0, and a tax tau_R = 0.5 whose remainder is paid as a uniform transfer, so d/P_s -> 2.94. N_a/N -> 0.0225.

In both cases participation stays bounded away from zero, so g_w <= g_e still cannot be dropped. But the stated inequality is false unless d = g_e = 0.

No counterexample was found to the human-chain bounds, the stated-economy fork, or the limits under the stated hypotheses. The bound fails only if the spectral-radius condition is dropped (T5): a good that uses 1.25 units of itself gives a "bound" of -1.2 against a price of 0.8.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/_verify_C2/verify_C2.py


## C2 (numerical): holds_with_conditions

### Conditions
1. The necessity formula is false as written. "g_w − g_e = θP_s gives N_a/N ≥ F(log(1 + θ))" holds only when d = g_e = 0 (for any τ_w in [0,1) and either σ). In general the threshold is log R with R − (1+θ) = [(1−τ_w)w − θ(d+g_e)]/(P_s+d+g_e). The correct bound is N_a/N ≥ F(log(1 + θP_s/(P_s + d + g_e))), which is below F(log(1+θ)) as w/P_s → 0 whenever d + g_e > 0. The qualitative point (without g_w ≤ g_e, N_a/N need not go to 0) survives, but only when F has mass below that limit threshold; this holds for χ uniform on [0, 2.2]. The error is confined to synthesis.md line 1259. The drafted Corollary 2 (synthesis.md 839–850), its proof (1057) and Prop. B.1(d) (1112) do not use the formula and are correct. main.tex D.1 (779–787, eq. 27) already shows the exit payment entering the threshold through P_s + m_e, which is why the formula needs g_e = 0.
2. The stated-economy upper bound w/p ≤ (w/r)/b̃_g needs b̃_g = b̃_m J(x*) > 0. This is automatic: the budgets rule out a corner in any equilibrium with w > 0 (C ≥ N ≥ N_a = Y = C forces c = 1 for workers who earn w > 0). The claim should say so.
3. The limit hypotheses are all needed: ξ, F fixed, and B_s bounded below (automatic in the stated economy, B_s ≥ h). So are Definition 1's sign restrictions τ_w ≥ 0 and d, g_e ≥ 0 (synthesis.md 475–479), which the inequality R ≤ 1 + w/P_s uses.
4. Near the productivity limit at x = 0, (ρ+δ)(a + λγ(0)) → 1, the stated economy has no interior equilibrium (x_c → 0 and (25) fails). There the claim holds only vacuously, though the bounds still hold at every Definition 1(i) price configuration.

### Evidence
Scripts are in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/: c2_networks.py, c2_stated.py, c2_limits.py and c2_algebra.py, each with a matching *_out.txt, plus c2_j4_rerun_out.txt. All were run from /home/user/labor/pinning with PYTHONDONTWRITEBYTECODE=1. git status is clean and code/__pycache__ is unchanged.

(1) Network bounds: hold. c2_networks.py is an independent generator. It builds task goods with walls and closed tasks, plain goods with 1–3 methods, machines built partly from task goods, and machine-hours at the user cost ρ+δ plus operating inputs. Prices come from exact policy iteration and are certified: the selection is productive and no method or task reassignment undercuts a price by more than 3.8e-14.
- Coverage: 3,431 networks in 7 regimes, giving 86,530 chain-good tests (34,946 binding, 14,327 cyclic chains, 13,678 chains containing a task good). The regimes are: random; ρ=0, δ=1; δ = 1e-3 and 1e-5; (ρ+δ)a_Km = 1−1e-3 and 1−1e-6; w/r from 1e-8 to 1e8; spectral radius of Ā_S at 1−1e-3 and 1−1e-6; cheap human methods.
- Upper bound: the worst excess is ≤ 6.1e-16 where cond(I−Ā_S) ≤ 2.5, and 3.7e-11 only at cond 4.6e6. A 60-digit re-check of 70 worst cases (top 40 overall plus top 5 per regime) leaves the selection unchanged and gives a worst excess of 2.7e-59, which is rounding.
- Lower bound r b̃_i ≤ p_i: worst excess 2.1e-16. P_s ≥ r b̃_s ≥ r B_s: worst excess 6.9e-16.
- Negative controls: a chain not closed under inputs gives p = 2.6 against a computed "bound" of 0.6. A chain with spectral radius 1.2 gives a negative "bound".
- Rerunning judge/j4 reproduces the claim's 3.2e-16 (3.18e-16 on 365 networks).

(2) Stated economy: holds. 706 solved equilibria were each checked against Definition 1 in four-good matrix form: the printed instance; 200 near it; 105 at ρ=0, δ=1; 200 with small δ; and 200 with (ρ+δ)a = 1−ε and λ=0. The smallest slacks are 6.7e-2 in w/p ≥ 1 and 6.4e-4 in w/p ≤ (w/r)/b̃_g, and w/p_h = w/r exactly. Across 17,579 Definition 1(i) configurations, including walls and 1,470 boundary assignments, the worst value is −2.2e-16 (rounding at w = p).

(3) Limits: hold under the hypotheses. c2_limits.py solves the path (λ = 0, γ_η = ηγ, η from 1 down to 1e-6) as Definition 1 equilibria under 11 policies. Every reported point passes all checks: τ_R in [0,1], c_o ≥ 0, a balanced government budget, C = Y, and every clearing condition.
- With g_w ≤ g_e (no policy; equal payments of 0.2P_s; τ_w = 0.3 funding a dividend; a dividend from τ_R = 0.5; public provision σ = 0), the chain of bounds w/r = γb̃_m/(1−γλ̃_m), w/P_s ≤ (w/r)/B_s and N_a/N ≤ F(log(1+w/P_s)) holds at every point (worst excess 5.6e-17). N_a/N falls monotonically to at most 1.9e-5. Under an exit-only payment, interior equilibria cease to exist from η = 1e-3 on, with N_a = 0.
- Task automation with λ = 7.3: w/r falls from 7.2e-2 to 7.0e-6 and N_a/N from 0.60 to 0.0019.
- The quoted numbers reproduce: equal payments 0.516 → 0.0002; in-work payment 0.0830 against F(log 1.2) = 0.0829.
- ξ is needed: with b → 4e-5 at λ = 7.3, γb̃_m reaches 5.5e-6 but 1−γλ̃_m falls to 2.4e-4, w/r stays near 0.023 and N_a/N near 0.652.
- F fixed is needed: letting χ_max shrink with η holds N_a/N at 0.300 while w/P_s falls to 3.3e-5.

(4) Algebra (sympy): (1+w/P_s) − R = [P_s k + P_s τ_w w + d w + g_e w]/[P_s(P_s+d+g_e)] ≥ 0, with k = g_e − g_w. Also R − (1+θ) = [(1−τ_w)w − θ(d+g_e)]/(P_s+d+g_e).

Line references: main.tex Prop. 4 at 336–349, proof (19) at 646–652, corollary at 355–372, D.1 at 779–787, path at 747. synthesis.md Claim 2 at 1248–1269.

### Counterexample
The claim's necessity formula fails. Take Appendix B's path (main.tex 747): the printed instance with λ = 0 and γ_η = ηγ, η from 1 down to 1e-6. Pay g_w = 0.4P_s in work and g_e = 0.2P_s in exit, so g_w − g_e = θP_s with θ = 0.2. Set d = τ_w = 0, σ = 1, and fund the payments with a rent tax, τ_R = 0.036 at η = 1e-6.

Every point is a Definition 1 equilibrium with an interior margin. The other hypotheses all hold: γb̃_m → 7e-8, ξ = 1, B_s ≥ h, F fixed (uniform on [0, 2.2]). Yet N_a/N → 0.07008, below F(log 1.2) = 0.08287. The exact limit is F(log(7/6)) = 0.07007.

Two more cases with θ = 0.2 also fail:
- d = 2P_s with g_w = 0.2P_s gives N_a/N → 0.02934.
- g_e = P_s with g_w = 1.2P_s gives N_a/N → 0.04333.

These come from c2_limits.py section (4) and match the sympy limits in c2_algebra.py.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/c2_limits.py


## C3 (analytic): holds_with_conditions

### Conditions
(1) The identity I = P_sC = wN_a + rT + rho V_m X holds in every equilibrium of the drafted Definition 1 (synthesis.md 483-499), under every policy that balances the government budget. It depends on two drafted choices:
- Definition 1(i) imposes the user cost p_m = (rho+delta)V_m (486). Without that clause, an equilibrium with c_o = 0 would carry (p_m - delta V_m)X in place of rho V_m X.
- The land tax falls on rental value and is owed whether or not the land is used (475). That makes ell = T whenever r > 0. Under a tax on rent received at tau_R = 1 the owner is indifferent, and the term is r ell.
I is net income, the value of consumption: gross investment delta V_m X is an intermediate input of the machine-hour row.

(2) The bound (15) holds in every equilibrium with r > 0. "Equality iff rho V_m X = 0" is true only when N_a > 0. The exact statement is: equality iff rho V_m X = 0 or N_a = 0.
- With r > 0, every equilibrium has w > 0, X > 0 and V_m > 0, so rho V_m X = 0 iff rho = 0.
- N_a = 0 can occur only when lambda = 0, H is empty, machines do almost every task, and nobody supplies labor at the equilibrium prices. That needs either F = 0 on [0, z*], which Assumption 4's "continuous, F(0) = 0" permits (437), or g_e >= g_w + (1 - tau_w)w.
- N_a = 0 is impossible when lambda > 0 or H is nonempty, and under zero instruments when F(z) > 0 for all z > 0.
- The drafted Proposition 5's one-way "with equality when rho = 0" (867) is correct. The remark's "(15) holds with equality only then" (878) needs "when N_a > 0".

(3) The limit needs T fixed (or bounded away from 0) and N_a <= N.

(4) The path statements hold for every eta in (0,1] with the instance's other parameters: H empty; F uniform on [0, 2.2], so F(z) > 0 for z > 0, which (25) at x_c = 1 needs; zero instruments; sigma = 1; T > Nh. The bound v <= eta pi uses gamma(1) = g0 + g1 = 1. The analytic rent-alone threshold 0.1192 is valid but loose. "Funded throughout" (main.tex 747) also holds analytically on all of (0,1] (see evidence), so it need not rest on the grid.

### Evidence
IDENTITY. From Definition 1(i) and (v):
- pY = w(N_a - lambda delta X) + p_m(1 - a delta)X
- hrY = r(ell - b delta X)
- so P_sY = wN_a + r ell + p_mX - delta X(a p_m + lambda w + b r) = wN_a + r ell + (p_m - delta V_m)X = wN_a + r ell + rho V_mX.
sympy confirms this exactly (A1, A2). Summing the worker, owner and government budgets gives P_sC equal to the same expression for any (tau_R, tau_w, d, g_w, g_e, sigma) (A3).
- This is the identity of main.tex 738 (proof of Lemma B.1) and 717 (P_s = wL_s + rB_s + rho V_mX/Y). It generalizes the flow version I = wN_a + rT (382-385; 749-757).
- At a constant plan, ell = T when r > 0 (Lemma A.1(a)). Aside: at beta = 1, A.1(a)'s "every optimal plan ... in every period" is too strong, because a finite deviation leaves the long-run average unchanged. Constant plans, which are all C3 uses, are unaffected.

BOUND. I >= wN_a + rT > 0. With r > 0:
- If w = 0, then p_m > 0, so labor is cheaper at every task. That gives X = 0, Y = T/h and N_a = T/h <= N, while C >= N + g_wN_a/P_s > N. This contradicts Y = C.
- A corner (X = 0) with w > 0 gives C >= N + (1 - tau_w)wN_a/P_s > N >= N_a = Y, also a contradiction.
- So w, X and V_m are all positive.
Limit: wN_a/I <= (w/r)N/T.

PATH (lambda = 0, H empty).
- (rho+delta)a = 0.196 < 1, so x_c = 1.
- N_D(1) = 0 < N_S(1) = F(log(1 + eta pi/(eta pi J(1) + h))), and T = 0.01 > Nh = 0.0017, so (25) holds.
- p_m = pi r at every margin, with pi = 0.069652. Hence v = eta pi gamma(x*) <= eta pi.
- Because gamma is increasing, p = p_m[gamma_eta(1 - x*) + J_eta(x*)] <= p_m J_eta(1). So P_s <= (eta pi J(1) + h)r <= (eta pi + h)r, with J(1) = 0.19333.
- X = YJ_eta/(1 - a delta) <= eta T/[h(1 - a delta)].
- Rent alone funds the support for eta <= (T - Nh)/(N pi) = 0.119164. The sharp analytic version is (T - Nh)/(N pi J(1)) = 0.616367.
- R/I >= T/(T + eta pi N + rho V_m eta T/[h(1 - a delta)]) -> 1.

FUNDING ON ALL OF (0,1].
- Excess demand falls in x (main.tex 729-734). It also falls in eta: as eta falls, Y rises and v/P_s = eta pi gamma/(eta pi g + h) falls. So x*(eta) decreases in eta.
- At eta = 1 and x = 0.8, n_D = 0.65495 > n_S = 0.54669. So x* > 0.8 for every eta <= 1.
- For eta >= 0.6164: eta J(x*) >= 0.038797, so rho V_mX >= 0.007371 and T + rho V_mX >= 0.017371 > N(pi J(1) + h) = 0.015166 >= NP_s.
- Below 0.6164, rent alone funds the support (previous paragraph).
- The exact rent-alone threshold is 0.78496, and the owner's surplus is at least 0.0083 along the whole path.

NUMBERS. My own solver, which matches appendix_b.solve to 1e-16.
- Instance: x* = 0.82987, v = 0.07165, N_a = 0.60165, and I = 0.078310 = 0.043111 wages + 0.01 rent + 0.025200 interest, equal to P_sY.
- Labor's share is 0.550511 against a bound of 0.811714. The interest share is 0.3218 and the rent share 0.1277. Labor's share of gross income (I + delta V_mX) is 0.467.
- In the matrix form, p^T f = I.
- On 1,201 log-spaced values of eta in [1e-4, 1], every one of these holds: (25), v <= eta pi, both P_s bounds, the X bound, and the identity (error at most 7e-18). Support is funded at every point, by rent alone up to 0.7822 (a contiguous range).
- R/I is 0.999452 at eta = 1e-4 and 0.2698 at eta = 1.
- Participation is 0.01788 at eta = 0.001, 0.56397 at 1 and 0.13398 at 0.01. x*(eta) is strictly decreasing.

Scripts: _verify_C3/verify_C3.py (20 of 20 pass) and certificate_C3.py; outputs in run1.txt and run_certificate.txt. Nothing under /home/user/labor was changed.

### Counterexample
This refutes the "only if" in "equality iff rho V_mX = 0" for every equilibrium.

Take the instance with lambda = 0 (the path's economy at eta = 1), H empty and every instrument zero, but let chi be uniform on [2, 4.2]. That F is continuous with F(0) = 0, as Assumption 4 allows. Machines do every task (M = [0,1]):
- Prices: r = 1, p_m = pi = 0.069652, V_m = 0.497512, and w = pi gamma(1) = 0.069652, so p_m gamma <= w on all of [0,1]. Also p = pi J(1) and P_s = 0.015165, so w/P_s = 4.5926.
- Workers: one works only if chi <= log 5.5926 = 1.7214 < 2, so N_a = 0. That equals labor demand, since lambda = 0 and no task is done by hand.
- Clearing: Y = T/B_s = 1.7072 and X = YJ(1)/(1 - a delta); land, machine-hours and the final good all clear.
- Owner: c_o = 0.7072 >= 0, and the constant plan is optimal by Lemma A.1(b).

Every condition of Definition 1 holds and r > 0, yet labor's share equals the bound (both 0) while rho V_mX = 0.015891 > 0 (check C1).

A second case uses the instance's own F (uniform on [0, 2.2]) with tau_w = 0.99 and g_e = (1 - tau_w)w = 0.000697, funded by tau_R = 0.0697. Again N_a = 0, c_o = 0.6612 and rho V_mX > 0 (check C2).

These are boundary assignments where (25) fails, so they lie outside Theorem 1. They leave the path, the instance and the drafted Proposition 5 ("equality when rho = 0") untouched, but they falsify the claim's "iff" and the remark at synthesis.md 878.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/_verify_C3/verify_C3.py


## C3 (numerical): holds_with_conditions

### Conditions
One clause is false as worded: "with equality iff ρV_mX = 0". The "if" half is true. The "only if" half needs N_a > 0. With r > 0, every equilibrium has w > 0, so N_a > 0 is the same as wN_a > 0.

Why: bound − share = wN_a·ρV_mX / [(wN_a + rT)(wN_a + rT + ρV_mX)]. So equality holds iff ρV_mX = 0 OR wN_a = 0. At an equilibrium with zero employment, both sides are 0 while ρV_mX > 0.

When zero employment can happen:
- It needs H empty, λ = 0 and every task automated.
- Then either F puts no mass near zero, or a policy makes work add nothing to consumption.
- (25) and any interior margin rule it out, so the iff holds on the instance, on the path and under Theorem 1.

A correct statement for the stated economy. With r > 0 there is no corner, so X > 0, and V_m ≥ br > 0. Hence (15) is strict whenever ρ > 0 and N_a > 0, and an equality whenever ρ = 0.

Effect on the draft:
- Proposition 5's "with equality when ρ = 0" (synthesis.md 867) is correct as written.
- The remark "(15) holds with equality only then" (878) and Claim 3's "if and only if" (1273) each need "when N_a > 0".

Everything else in C3 holds as stated. The funding statement holds at every η in (0,1], not only on the grid.

### Evidence
All scripts and outputs are in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/. Every final run passes. Nothing under /home/user/labor changed (git status is clean). code/appendix_b.py was imported read-only with -B.

**Symbolic (c3_symbolic.py).**
- In the four-good system, p'(Cz) − [wλ'y + rb'y + ρV_mX] ≡ 0, using A_ρ − A_0 = ρ e_m e_K'.
- The three budgets sum to P_sC = wN_a + rℓ + ρV_mX for every policy that balances the government budget.
- The gap formula in conditions.
- main.tex proves the identity only in the flow case: Proposition 5 at 380–391 and Appendix C at 753–757. It notes interest as "outside this benchmark" at 393 and 675, and has the durable identity at 738–740.

**Path (c3_path.py).** My own 4×4 solver agrees with appendix_b.solve to 3.2e-13. On the 1,201-point geometric grid over [1e-4, 1]:
- x_c = 1 and (25) hold everywhere: min N_S(x_c) = 1.86e-3, against N_D(x_c) = 0.
- Max v/(ηπ) = 0.99863; max P_s/(ηπ + h) = 0.99671; X ratio ≤ 0.193; identity error ≤ 4.4e-16.
- π = 0.06965 and η̄ = 0.1192, as quoted. Rent alone funds support up to η = 0.7822 on the grid; the exact threshold is 0.78496.
- Rent plus interest funds support everywhere: min c_o = 0.7244, at η = 1.
- R/I = 0.999452 at 1e-4 and 0.2698 at η = 1, and it rises monotonically as η falls.
- Participation is 0.563972, 0.133981 and 0.017877 at η = 1, 0.01 and 0.001.
- Instance: labor's share 0.550511 against the bound 0.811714; interest share 0.321792.

**Path, beyond the grid.**
- Uniqueness: excess labor demand changes sign exactly once over w/r in [1e-14, 1e4] at seven values of η. So the bounds cover every equilibrium on the path.
- Funding at every η in (0,1]:
  - below 0.1192, analytic;
  - on [0.1192, 1], a certificate: x*(η) is decreasing; Y and v/P_s are monotone in (η, x); the lower bound on c_o is at least 0.7241 in all 4,000 cells.
- c3_dense.py: 20,001 values of η in [1e-8, 1]. Every bound holds, with max excess −1.4e-7 and −3.3e-7, and c_o ≥ 0.7244.

**Stated economy (c3_stated.py).** 265 funded equilibria in all:
- random economies with zero instruments;
- six policy families: rental-value tax with a dividend, wage tax, in-work payment, exit payment, public provision σ = 0, and public provision plus a wage tax;
- boundary cases: ρ = 0 with δ = 0.05 or 0.001; δ = 1e-3 and 1e-5; (ρ+δ)a = 1 − 1e-6.

In all of them:
- the identity holds to 1.1e-15 relative, C = Y and the government budget balances;
- each worker's choice checks against utility, and the assignment is cost-minimizing;
- share ≤ bound, strict whenever ρ > 0 (min relative gap 2.3e-3), and an equality whenever ρ = 0.

S-e: with r > 0 there is no equilibrium with w = 0 and no corner.

**Other equilibria (c3_extra.py).**
- r = 0 (abundant land): I = wN_a + ρV_mX = P_sC = 1.61257.
- Boundary equilibria at walls x_H = 0.829, 0.825 and 0.82, where (25) fails: the identity holds and the inequality is strict.

**Networks (c3_networks.py, seeds 78 and 2027).** 2,400 + 10,800 random durable networks:
- 1–3 capital goods, each with its own δ_j; 1–3 non-produced inputs;
- 6,073 with method choice, selected by policy iteration;
- spectral radius of A_ρ up to 0.999999.

Results:
- p'f = wN_a + r'ℓ + ρΣV_jX_j to 7.4e-16 (1.7e-11 near the productivity limit).
- No bound violations in 11,254 networks.
- Strict in 8,048; an equality in 3,133.

Three apparent failures were tolerance artifacts of my own (a free basket with I = 0; stocks of 1e-17; ±1e-16 noise at wN_a = 0). They were fixed and the scripts rerun.

**Side findings.**
- c3_sharper.py: P_s ≤ (ηπJ(1) + h)r, so rent alone provably funds support up to η = 0.6164, not just 0.1192 (synthesis.md 1016 says "about 0.12").
- With λ = 7.3 and γ scaled by η from 1 to 1e-4, labor's share falls from 0.5505 to 1.3e-6, below (w/r)N/T.
- Measured against gross income, labor's share on the instance is 0.467.

### Counterexample
This is a counterexample to the "only if" half of the equality clause only. Nothing contradicts the inequality, the identity, the limit, or any statement about the path.

**(1) Gapped F** (c3_stated.py, S-d).
- Setup: Appendix B's instance with λ = 0 and H empty (x_H = 1), ρ = 0.09, δ = 0.05. The cost of work χ is uniform on [2, 4.2]; F is continuous with F(0) = 0, so Assumption 4 holds.
- Every task goes to machines. Any w/r in [0.06965, 0.09690] clears every market of Definition 1, with r = 1 > 0 and N_a = 0.
  - Labor demand is Y·0 + λδX = 0.
  - Nobody works, because log(1 + w/P_s) ≤ 2.
- Interest ρV_mX = 0.01589, which is 0.614 of I. The owner's consumption c_o = 0.707, so support is funded, and C = Y.
- Labor's share = bound = 0, so the bound holds with equality although ρV_mX > 0.
- (25) fails here, and the economy has no interior equilibrium.

**(2) Policy route** (c3_zero_employment.py).
- Setup: the same economy with the instance's own F (uniform on [0, 2.2]), τ_w = 0.99, an exit payment g_e = (1 − τ_w)w, and a land tax τ_R = 0.0697 to pay for it.
- Work adds nothing to consumption, so N_a = 0. Then c_o = 0.661, and again share = bound = 0 with ρV_mX > 0.
- This is an equilibrium for every τ_w ≥ 1 − T/(Nw) = 0.856.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/


## C4 (analytic): holds_with_conditions

### Conditions
C4 holds for Definition 1 exactly as drafted, under five conditions.

1. The stipulated user cost is load-bearing for uniqueness. Definition 1 is at synthesis.md 483-499; its (i) and eq. `unitcost` (401-405) stipulate p_m = (rho+delta)V_m. main.tex 685 stipulates the same.
   - Owner optimality (iii) yields the user cost only when c_o > 0 (Lemma A.1(c), 1041).
   - At c_o = 0 and any return R > 0, the constant plan is the owner's only feasible plan, so it is optimal.
   - On the printed instance, dropping the clause admits a second stationary equilibrium (see counterexample).
   - So the synthesis's reason for keeping the clause is false for the instance: "Scans of the return find none ... So the clause costs nothing in these economies" (584-587), repeated at 1183, 1334 and 1386. `knife_edge.py` scanned only the interior branch, which ends at R = 0.168, and never reached the zero-rent branch.
   - At delta = 0.2, "no equilibrium" survives without the clause: c_o < 0 on every branch for all R in (0, 0.479).
   - Two honest statements are available. Either keep the clause and add a remark that it selects the return, disclosing the R = 0.192 equilibrium. Or state Theorem 1 for equilibria with c_o > 0: there Lemma A.1(c) derives the user cost, and existence becomes T + rho V_m X > N P_s.
2. rho >= 0 (beta <= 1, Assumption 5, 457) is used. L_s falls on (0, x_c) only because delta(a + lambda gamma) <= (rho+delta)(a + lambda gamma) < 1 (main.tex 729).
3. (25) must be strict, as written. With equality, a continuum can clear: on the instance with lambda = 0, no wall and chi ~ U[2,4], every w/r in [0.06965, 0.09690] gives a funded zero-employment equilibrium.
   - Separately, T > Nh is necessary for any equilibrium at all: Y <= T/h <= N < N + w N_a/P_s forces c_o < 0.
4. Lemma A.1(a) (1039), "every optimal plan rents out l_t = T in every period", is false for beta = 1, because long-run-average ranking ignores any finite set of periods. The proof (1068) needs only that no constant plan with l < T is optimal, which holds for every beta in (0,1]. Reword (a).
5. One supporting statement is wrong at x_H = 0.80. Claim 4's "Where (25) fails (walls at 0.825 and 0.80), it finds boundary equilibria" (1310), and W3's label in `wall_test.py` (94-119), fail there.
   - At 0.80, the zero-rent configuration that clears labor and land leaves c_o = -0.393, so that economy has no equilibrium under Definition 1.
   - At 0.825 the boundary equilibrium is funded (c_o = 0.230).
   - Theorem 1 is unaffected.

### Evidence
**Analytic: every case of Definition 1** (sigma = 1, all instruments zero; Assumptions at synthesis.md 374-458).
- **The assignment.** gamma rises strictly on [0, x_H], and p_m > 0 unless r = 0 and lambda w = 0. So (i) makes M an initial segment up to a null set; w = r = 0 is excluded by P_s > 0.
- **The ceiling.** The identity p_m gamma - w = [(rho+delta) b r gamma - w D]/(1 - (rho+delta)a) puts the margin at or below x_c (sympy, verify_synthesis S7).
- **w = 0.** With r > 0, M is empty and X = 0, so labor demand is Y = C >= N > 0 against a supply of N F(0) = 0. With r = 0, P_s = 0.
- **r = 0.** M = {D > 0} on [0, x_H], and w/P_s = 1/[1 - x_c + lam~_m J(x_c)]. This is at least lim v/P_s: equal at the economic ceiling, larger at the wall, since gamma lam~_m < 1 and h(1 - gamma lam~_m)/b~_m > 0. With Y B_s <= T, supply >= N_S(x_c) > N_D(x_c) >= Y L_s.
- **r > 0, non-interior.** l = T. The corner gives demand T/h > N. A margin at the economic ceiling needs w >= r v(x), which tends to infinity. At a wall boundary w >= v(x_H) r, and w/P_s rises with w, so supply >= N_S(x_H) > N_D(x_H).
- **Interior.** Proposition 1 and the machine row give (21)-(22), with p_m/r = (rho+delta)b/D. Condition (v) gives (23)-(24).
  - N_D falls strictly.
  - d(v/P_s)/dx = (h + b~_m J)v'/P_s^2 > 0, re-derived: the x-derivative of P_s/v reduces to -(b~_m J + h)v'/v^2, since -1 + gamma lam~_m + b~_m/p_m = 0.
  - Hence exactly one crossing, which T > Nh and (25) place in (0, x_c).
- **Funding.** With p_m = (rho+delta)V_m, the stationary owner budget is P_s(c_o + N) = rT + rho V_m X.
  - Necessity: Definition 1 requires c_o >= 0.
  - Sufficiency: Lemma A.1(b), whose present-value bound with Jensen (beta < 1) and averaging (beta = 1) I re-derived. Walras then gives C = Y.
- This matches main.tex 687-741.

**Reran the cited checks.**
- `wall_test.py`: 8/8 PASS.
- `j2_uniqueness.py`: one candidate on each of the 5 solver economies and with the 0.90 wall.
- `verify_synthesis.py`: 12/12. S1 gives C = Y = 3.013205 and c_o = 0.3544. S8 at delta = 0.2 has (25) holding, with income 0.11208 against support 0.40505.

**Independent enumeration** (`verify_C4.py`). It is built from Definition 1's primitives and does not use (21)-(24) to find equilibria. It covers w = 0, r = 0, and r = 1 over w/r from 1e-15 to 1e15.
- **17 named economies**: the 5 solver economies; walls at 0.90, 0.825 and 0.80; delta = 0.2; rho = 0 with delta = 0.2; lambda = 0 with a wall; a = 0; three F families; exponential gamma; a wall exactly at the economic ceiling.
- **10,000 random economies** satisfying Assumptions 1-5. 3,507 satisfy (25); each has exactly one configuration, interior with x* in (0, x_c). Each matches (21)-(24) and passes every Definition 1 check on a 200,001-point task grid. 1,943 are funded and 1,564 are not. There are 0 violations.
- **The "iff" at its knife-edge** (`knife_iff.py`): at delta = 0.0730554 an equilibrium exists exactly when T + rho V_m X - N P_s >= 0.
- **The clause** (`clause_C4.py`, `rival_check.py`): see the counterexample.

### Counterexample
None to C4 as stated.

The counterexample is to the synthesis's claim that the user-cost clause "costs nothing" (synthesis.md 584-587, 1183). Take the printed instance (main.tex 745; `code/appendix_b.py` PRINTED) with machine return R = 0.192269 instead of rho = 0.09.
- **Prices:** r = 0 and w = 1. p_m = 2.676301 = (R+delta)V_m, whereas the clause would require (rho+delta)V_m = 1.546555.
- **Assignment:** machines perform [0, 0.796430), which is the economic ceiling at R.
- **Labor:** N_a = 0.596445, both supplied and demanded.
- **Land:** 0.007921 used, below T = 0.01; the slack makes r = 0 consistent.
- **Final good:** X = 0.17346 and C = Y = 2.618904.
- **Owner:** R V_m X = N P_s = 0.368425, so c_o = 0. Because R > 0, any extra consumption eventually drives wealth negative: none of 20,000 random plans with positive consumption is feasible. So c_o = 0 forever is optimal.

Every condition of Definition 1 holds except the stipulated user cost. The instance therefore has two equilibria without the clause and one with it.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/_verify_C4/verify_C4.py


## C4 (numerical): holds_with_conditions

### Conditions
I could not refute Theorem 1 as stated, for Definition 1 as drafted in synthesis.md 483–499 and N_S(x_c) as defined at main.tex 708. Three things must stay true in the rewrite, and one note in the verification record needs correcting.

(1) Definition 1 must keep imposing the user cost p_m = (ρ+δ)V_m. It does so twice now: in the third equation of (eq:unitcost) at synthesis.md 404 and in the clause at 486.
- Decision 1 (synthesis.md 1181–1183) asks whether to leave the user cost to the owner's first-order condition instead. If it did, uniqueness fails.
- c4_usercost.py: at T = 0.0069 and 0.0072, other parameters as in the instance, a second stationary configuration exists at returns 0.0962 and 0.1182, with c_o = 0. It meets every other condition of Definition 1, because at c_o = 0 the owner's only feasible plan is the constant one.
- It sits beside the funded equilibrium at ρ = 0.09 (x* = 0.785536 and 0.790846).
- So the "proof that none exists anywhere" that 1183 would need cannot be given: rival equilibria exist.

(2) N_S(x_c) in (25) must be defined as the limit of the margin-indexed supply as x rises to x_c. That is main.tex 708; in the draft it survives only as a comment at synthesis.md 733.
- Read instead as "excess supply as w/r → ∞", the theorem is false.
- With λ = 0, H empty and χ ~ U[2.58, 4.58], N_S(x_c) = N_D(x_c) = 0, and there is a continuum of funded zero-employment equilibria (c4_extra X1: 85 grid points, w/r from 0.070 to 0.184).
- 67 random draws where (25) fails show the same kind of multiplicity.

(3) "Up to null sets" must cover the indifferent worker's choice, which is an F-null set of workers. The drafted statement (synthesis.md 742) says only "sets of tasks of measure zero" and gives the quantities as (23)–(24). Consumption and ℓ = T come from the budgets and from Lemma A.1(a).

Record correction (outside the theorem): synthesis.md 1310 says the scan "finds boundary equilibria" at walls 0.825 and 0.80.
- At 0.80 the only configuration has r = 0 and is unfunded (c_o = −0.393), so that economy has no equilibrium.
- j2 reports funded=None there, and wall_test W3 does not check funding.
- At 0.825 a funded boundary equilibrium does exist (c_o = 0.230).

Caveat on reading "interior": (25) can hold while x* lies astronomically close to x_c. With λ = 0, no wall and lognormal F, 1 − x* = 4.2e-47 and 8.7e-101, and employment is about 1e-47 and 1e-100. The theorem is still correct there.

### Evidence
All scripts and outputs are in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/ (files c4_*). Nothing under /home/user/labor was written: git status is clean and the pre-existing __pycache__ is unchanged since 13:35.

1. Cited checks rerun (cited checks reproduced as stated):
- _work_B/wall_test.py: 8/8 PASS.
- verify_synthesis.py: 12/12. S1 gives C = Y = 3.013205 and c_o = 0.3544. S8 at δ = 0.2 gives support 0.40505 against income 0.11208.
- judge/j2_uniqueness.py: exactly one candidate on the five solver economies and with the wall at 0.90 (c4_j2_rerun_out.txt).

2. Independent enumerator, c4_common.py:
- It builds every configuration Definition 1 allows from primitives only: w/r scanned over 1e-14 to 1e14 at r = 1, plus w = 0 and r = 0. It does not use (21)–(24) and does not assume an interior margin.
- It compares the result with (21)–(25) (main.tex 688–724) and checks each condition of Definition 1 as a residual.

3. Printed instance (main.tex 745):
- One configuration, interior: x* = 0.829869204, v = 0.0716535659, Y = 3.013204970, all equal to appendix_b.solve.
- Every Definition 1 residual is at most 9e-16. C from the budgets equals Y = 3.013205; c_o = 0.354402.
- Random owner deviations never gain (largest relative gain −7.9e-6). The numbers at line 745 reproduce.
- Confirmed again at 50 digits (c4_mp_named_out.txt).

4. δ = 0.2:
- (25) holds: N_S(x_c) = 0.55767 > N_D(x_c) = 0.51860.
- Exactly one configuration, x* = 0.734913, unfunded: support 0.405055 against rent plus interest 0.112078, c_o = −0.7233.
- The r = 0 and w = 0 configurations are excluded, so no equilibrium exists. Also at 50 digits.

5. Named economies (c4_stated_out.txt, 19/19 PASS): the five solver economies and walls at 0.95, 0.90, 0.946343 (the ceiling), 0.85 and 0.835 each have exactly one configuration at x*, and it is an equilibrium iff funded.

6. Random economies satisfying Assumptions 1–5 (c4_random.py, seeds 4 and 2027, 3,000 each):
- Five γ families, including near-step logistic and wavy schedules with near-flat points; seven F families, including F with support away from 0 and lognormal F; walls; ρ = 0; δ down to 1e-4; λ = 0.
- (25) holds in 1,141 and 1,104 draws; all confirmed (one configuration, interior at x*, matching (21)–(24), equilibrium iff funded).
- 187 needed more than double precision: either γ is flat at x* (elasticity down to 1e-123, redone at 50–163 digits, gaps at most 1e-40) or x* is within 1e-47 or 1e-101 of x_c (decided in u = 1 − x).
- The excess-demand grid is never non-monotone where (25) holds.

7. Boundary cases, 134 per run: 88/88 inside (25) confirmed in both runs. They cover:
- the flow benchmark ρ = 0, δ = 1, including 60 random draws;
- δ from 1e-3 to 1e-7;
- (ρ+δ)a = 1 − 1e-9;
- T = Nh(1 + 1e-9);
- a (25) margin of 1e-9;
- a wall at the ceiling or ±1e-12 from it;
- scales of 1e±6.
Pushing the productivity condition to its limit through λ drives x_c → 0, where (25) necessarily fails.

8. Probes (c4_extra, 5/5):
- Funding at equality (c_o = 0) gives an equilibrium.
- With a (25) margin of 1e-7, T swept across the funding threshold: one configuration every time, an equilibrium iff funded (12 funded, 8 not).

9. Symbolic checks (c4_symbolic, 8/8): the d(v/P_s)/dx formula (main.tex 732); dL_s/dx < 0; the zero-rent gap [J(1 − γλ̃_m) + h/p_m] ≥ 0; boundary w/P_s rising in w; Lemma 2's identity; the owner's budget identity. Every step of the exclusion proof (synthesis.md 1064–1070) checks.

10. Beyond the theorem's scope: random productive networks for the machine chain (machine-hour row at ρ+δ in prices, δ in quantities). Exactly one configuration whenever the analog of (25) holds: 185/185 without feedback and 168/168 with the final good as an input to the chain.

### Counterexample
None within the theorem's hypotheses, as stated.

Counterexamples exist only to weakened variants:
(a) Without the user cost in Definition 1 (decision 1's alternative): take N=1, h=0.0017, a=1.4, λ=7.3, b=0.4, δ=0.05, ρ=0.09, γ=0.01+0.99x^4.4, χ ~ U[0, 2.2], and T=0.0069.
- The funded equilibrium at ρ has x* = 0.785536.
- A second configuration at return 0.09616 has x = 0.784901 and c_o = 0, and meets every other condition of Definition 1.
(b) With (25) read at w/r → ∞ instead of at x_c: take λ = 0, H empty, χ ~ U[2.582, 4.582], other parameters as in the instance. There is a continuum of funded zero-employment equilibria, w/r from 0.070 to 0.184.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/c4_stated.py


## C5 (analytic): holds_with_conditions

### Conditions
1. Lemma A.1(a), as drafted (synthesis.md 1039: "every optimal plan rents out ℓ_t = T in every period"), is true only for β < 1. Assumption 5 (synthesis 457) allows β = 1 and then ranks paths by the long-run average. Under that criterion, a deviation in finitely many periods leaves the value unchanged, so some optimal plans keep land back. What holds for every β in (0, 1] is weaker: when r > 0, a constant plan with ℓ < T is strictly dominated by the constant plan with ℓ = T, because u is strictly increasing. Definition 1(iii) and the remark at 501 need only this, as do Theorem 1's proof (1068) and Proposition 6(i) (915, 956). Suggested wording: "(a) If r > 0, no optimal constant plan rents out less than T; when β < 1, every optimal plan rents out ℓ_t = T in every period."
2. At β = 1 the constant plan is only weakly optimal. At ρ = 0 the constant plan's consumption, y_o/P_s, does not depend on wealth. So eating part or all of the machine stock in one period and then consuming c* forever gives the same long-run average, with strictly more consumption in that period. The defect "owner indifferent to its stock" (synthesis 89, defect 6) is therefore cured only for β < 1. The ρ = 0 and flow-benchmark equilibria rest on the long-run-average criterion; an overtaking criterion would reject the constant plan whenever X > 0. The printed instance has ρ = 0.09, so it is not affected. Assumption 5 should say liminf or limsup, because the average need not converge.
3. Lemma A.1(c) needs c_o > 0, X > 0 and V_m > 0. At c_o = 0 the user cost is not the owner's first-order condition, and Definition 1(i) imposes it. The note at 582 says the c_o = 0 plan is the only feasible one "whatever the return". That is true only for a positive net return p_m/V_m − δ > 0, or for X = 0. With a zero or negative net return and X > 0, the owner can consume its stock.
4. Part (b) uses the owner's budget at a constant stock and the user cost (464–467). Concluding Y = C also needs the cost equations, labor, machine-hour and land clearing, and P_s > 0.
5. Part (c): Proposition 1 needs w > 0 and p_m > 0 (642, 506), plus Assumption 1's continuity and strict monotonicity (375). In Proposition 3, "prefers work exactly when w ≥ s" (693) is a weak preference at w = s; main.tex 285 says "work is optimal exactly when".
6. The owner check S2 uses log utility, which is outside Assumption 5's requirement that u be continuous on [0, ∞). My check O1 repeats it with three utilities inside that class.

### Evidence
Line numbers: synthesis.md for the drafts, main.tex for the paper.

(a) Owner's problem, Lemma A.1 (synthesis 1037–1046).
- Write W_t = V_m X_t ≥ 0. At the user cost the owner's budget (460–462) becomes W_{t+1} = (1+ρ)W_t + y_{o,t} − P_s c_t, where y_{o,t} = rℓ_t − τ_R rT − σNP_s.
- y_{o,t} is at most its value at ℓ = T, because the rental-value tax τ_R rT does not depend on ℓ. This holds for every τ_R ≥ 0.
- β < 1: sum the budget with weights β^{t+1} and drop β^{t1}W_{t1} ≥ 0. This gives Σβ^t c_t ≤ Σβ^t c*. Jensen's inequality with weights (1−β)β^t then bounds utility by that of the constant plan; the bound is finite because u(0) is finite.
- β < 1, land: renting more land in any single period raises that period's consumption, and u is strictly increasing, so (a) holds.
- β = 1: the average of c_t over t1 periods is at most c* + W_0/(t1 P_s). Concavity and continuity bound the limsup of average utility by u(c*), so (b) holds under either liminf or limsup.
- Converse (c), β < 1: a two-period deviation changes utility by β^t u'(c_o)(ε/P_s)[β(1 + p_m/V_m − δ) − 1]. This is nonzero unless p_m = (ρ+δ)V_m. Saving needs c_o > 0; dissaving needs X > 0 and c_o > 0.
- Converse (c), β = 1: a permanent deviation raises consumption in every later period by |p_m/V_m − δ|ε/P_s.
- At c_o = 0 with net return g > 0, the drawdown follows D_{t+1} ≥ (1+g)D_t, so the constant plan is the only feasible plan.

(b) Walras.
- sympy, exactly: P_sC − (wN_a + rℓ + ρV_mX) equals minus the government budget residual (477), for any (τ_R, τ_w, d, g_w, g_e, σ).
- Cost equations plus labor, machine-hour and land clearing give P_sY = wN_a + rℓ + ρV_mX for any assignment. So Y = C because P_s > 0.
- At zero instruments this reproduces main.tex 736–740 (identity at 738) and corrects 755, which omits ρV_mX.

(c) Propositions 1 and 3.
- Definition 1(i) (486) is pointwise. With γ strictly increasing and θ = w/p_m, M lies between {γ < θ} and {γ ≤ θ}.
- Interior margin: both sets have positive measure, so γ(0) < θ < γ(x_H), and the intermediate value theorem gives a unique x* with w = p_mγ(x*).
- Boundary: M has full measure; continuity at x_H gives w ≥ p_mγ(x_H). Corner: by symmetry, w ≤ p_mγ(0).
- This corrects main.tex 163–166 and 627, which assert indifference at any boundary between human and machine tasks, and extends 186–193.
- Proposition 3: the worker's budget (446) is the same for σ = 0 and σ = 1. With zero payments, u_1 − u_0 = log(1 + w/P_s) − χ. F is continuous with F(0) = 0, so ties have measure zero and N_a = NF(log(1 + w/P_s)). This replaces main.tex 284–292, 304–307 and 639–644.
- Land fully used and supply invariant to the tax are now derived, not assumed as at main.tex 317 and 414. The user cost becomes the owner's first-order condition instead of the stipulation at main.tex 671 and 685.

Numerical checks.
- `verify_synthesis.py`, rerun, 12 of 12 pass:
  - S2: 1,553 feasible perturbations, maximum gain −3.01e−6; returns of ρ ± 0.01 give gains of 8.12e−6 and 8.14e−6.
  - S3: |C − Y| at most 1.3e−15.
- knife_edge.py: c_o stays between 0.24 and 1.02 on returns [−0.045, 0.168]. knife_edge2.py: c_o is negative on [−0.19, 0.10].
- My script verify_C5.py, 7 of 7 pass:
  - W1, W2: the two sympy identities.
  - O1: with sqrt, CARA and log1p utilities, about 2,650 random feasible plans each (varying land, stock and the wealth left at the end) all lose; maximum gains −5.5e−7, −2.7e−10, −4.7e−8.
  - O2: the β = 1 counterexample.
  - O3: the converse at ρ ± 0.001 and ρ ± 0.01, and at β = 1.
  - O4: drawdown exhaustion at g > 0; at g = 0 eating the stock is feasible.
  - P1: the wall at x_H = 0.825 gives a boundary equilibrium satisfying all of Definition 1, with w = 0.093046 ≥ p_mγ(x_H) = 0.081683, c_o = 0.230 and C − Y = −4.4e−16.
- Aside, which belongs to C4: at x_H = 0.80 the only candidate has r = 0 and c_o = −0.39. With every instrument zero it is not an equilibrium, although synthesis 1310 calls it a boundary equilibrium.

Files:
- /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/_verify_C5/verify_C5.py
- /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/_verify_C5/verify_C5_out.txt

### Counterexample
This refutes Lemma A.1(a)'s literal wording at β = 1 only; the rest of the claim stands.

Setup: the printed instance with ρ = 0 (β = 1). It is funded, with κ = 1.694. The owner's constant-plan consumption is c* = 0.6936 baskets, V_mX = 0.13678 and r = 1.

Plan with less land: in period 0 rent ℓ_0 = T − ε with 0 < ε ≤ c*P_s/r, and consume c_0 = c* − rε/P_s ≥ 0. From period 1 on, use the constant plan with ℓ = T. Alternatively set ℓ_0 = 0 and cover the shortfall by running the stock down by rT ≤ V_mX. Either plan has long-run average u(c*), the same as the constant plan, so it is optimal while renting out less than T in period 0. This contradicts "every optimal plan rents out ℓ_t = T in every period" (synthesis 1039).

Plan eating the stock: consume c_0 = c* + V_mX/P_s = 23.86 baskets once, then c* forever with X = 0. It is also optimal under the long-run average, so the constant plan is only weakly optimal at β = 1.

Neither plan is optimal when β < 1.

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/_verify_C5/verify_C5.py


## C5 (numerical): holds_with_conditions

### Conditions
Parts (a), (b) and (c) hold as mathematics, with one correction to Lemma A.1(a). One item in the claim's "Checked" list is false on the full range of returns, and that changes how the user-cost clause must be described.

1. Lemma A.1(a) at synthesis.md 1039 says "every optimal plan rents out l_t = T in every period". This is false at beta = 1. Under long-run average utility, a plan that withholds land for finitely many periods and pays for it by buying fewer machines consumes c* in every period, so it is also optimal.
   - Fix: write "if beta < 1; when beta = 1, every optimal constant plan".
   - The uses in Theorem 1's proof and Proposition 6(i) are unaffected, because Definition 1's plan is constant, and a constant plan with l < T is strictly worse at every beta.

2. The clause "machine-hours rent at the user cost" in Definition 1(i) (synthesis.md 486) selects among equilibria; optimization does not imply it.
   - Optimization implies it only when c_o > 0 (Lemma A.1(c)).
   - The clause bites in the paper's own instance (main.tex 745): a second stationary configuration at another return meets every other condition of Definition 1 (see counterexample).
   - The claim's "scans find no zero-consumption equilibrium at another return" is true only on the scanned range [-0.045, 0.168]. The scan stopped there because appendix_b.solve() raises once the interior crossing fails, so it never looked at the zero-rent regime.
   - Required changes:
     - Delete the bullet at synthesis.md 587: "the clause costs nothing in these economies and makes the theorem hold in general".
     - Qualify the note "The equilibrium concept is standard" (synthesis.md 501): Definition 1 also requires machines to earn rho.
     - Read Theorem 1's uniqueness and its "only if funded" as statements under that selection.
   - An alternative, for the authors to decide: require c_o > 0 in Definition 1. The user cost would then follow from Lemma A.1(c) instead of being imposed.

3. The synthesis.md 582 phrase "its only feasible plan is constant whatever the return" holds only when p_m > delta V_m. When p_m <= delta V_m, the owner can consume part of its stock.

4. Minor points:
   - The corner inequality of Proposition 1(i) is true but vacuous in the stated economy: no corner can be an equilibrium under any policy, because support cannot be funded there.
   - The earlier check S2 used log utility, which Assumption 5 excludes (u(0) = -inf). Admissible utilities give the same result.
   - Proposition 3's formula needs zero instruments: with instruments, N_a departs from it by up to 1.29.

### Evidence
All scripts import code/appendix_b.py read-only, with bytecode writing disabled. git status under /home/user/labor shows no changes.

The earlier checks reproduce: `_work_synthesis/verify_synthesis.py` passes 12 of 12.
- S2: 1,553 random deviations, largest gain -3.0e-6; a return of rho +/- 0.01 gives a gain of 8.1e-6.
- S3: |C - Y| at most 1.3e-15.

**`c5_owner.py`: Lemma A.1, 11 of 11 pass.** Every positive gain in double precision was re-evaluated in 60-digit arithmetic.
- beta < 1, random deviations: 2,787 feasible deviations over 7 utilities, including corners with c* = 0. Exact gains are at most 1.8e-60, which are ties of linear utility.
  - In double precision these gains reached 1.6e-8. That came from plans that are infeasible in exact arithmetic (`c5_owner_diag.py`).
- beta < 1, optimizer: SLSQP over 120 plans of H = 2 to 20 periods with land free. The largest gain is 4.5e-61.
- Bellman's equation holds; the right side exceeds V by at most 2.6e-14.
- beta = 1: over 1,077 plans, average utility never exceeds the bound in the proof.
- Land: renting out T beats any l < T in all 979 cases, for any tau_R in [0, 1] on rental value.
- Converse:
  - beta < 1, |R - rho| from 1e-7 to 0.3: a two-period deviation gains in all 1,933 cases.
  - beta = 1: a permanent change in the stock gains in all 595 cases.
  - At c_o = 0 with R > 0, the constant plan is the only feasible plan (414 cases); with R <= 0 it is not (145 cases).

**`c5_walras.py`: (b), 4 of 4 pass.**
- 300 equilibria of Definition 1 under random policies on 7 economies, 122 of them with public support.
  - |C P_s - (w N_a + r T + rho V_m X)| is at most 3.0e-16 relative.
  - |C - Y|/Y is at most 3.6e-16.
  - The government budget balances to 8.9e-16.
- 2,852 random production networks, with rho = 0 in about half:
  - the identity holds to 1.1e-13;
  - the summed budgets match to 3.1e-13.

**`c5_props.py`: (c), 4 of 4 pass.** Workers choose one by one, and the assignment comes from direct cost comparison, not from the solver's margin.
- Proposition 1(i): 20,000 random price pairs and schedules (8,349 interior, 5,793 boundary, 5,858 corner) with no violation.
- Equilibria of Definition 1, all satisfying every condition and Propositions 1 and 3:
  - 15 interior, including zero-rent equilibria at rho = 0.175, 0.185 and 0.19;
  - 1 boundary, with a wall at x_H = 0.825;
  - 211 random, of which 205 are interior and 6 boundary.

**`c5_zero_consumption.py`: 6 of 6 pass.** It scans the whole admissible range of returns, in every regime. Results are in the counterexample.

### Counterexample
**The instance (main.tex 745; appendix_b.PRINTED).** Definition 1's equilibrium has x* = 0.82987 and c_o = 0.354. A second configuration sits at machine return 0.192269 instead of rho = 0.09.
- It has r = 0, an interior margin at the ceiling x* = x_c = 0.79643, and w/P_s = 2.714.
- N_a = 0.59644, matched by the workers' own choices.
- Y = 2.61890 and X = 0.17346.
- Land used is 0.007921 of T = 0.01; the owner is indifferent at r = 0.
- The owner's budget gives c_o = 0, and C = Y.
- At c_o = 0 with a positive return, the owner has no feasible deviation. Extra consumption of 1e-3, 1e-6 or 1e-9 exhausts the stock after 50, 89 or 129 periods.
- So every agent optimizes and every market clears. Only Definition 1(i)'s user cost at rho excludes the configuration.
- c_o(return) does not involve beta. The same configuration therefore coexists with Definition 1's equilibrium at rho = 0, 0.02, 0.09 and 0.15.

**Where the scan stopped.** knife_edge.py stopped at 0.168. The interior regime ends at 0.1682 and the zero-rent regime starts at 0.1687.

**Other economies with such a configuration:**
- ssrn_flow, at a return of 1.98726;
- the ceiling test economy, at 0.16515;
- Figure 3's task economy, at 0.32814;
- 65 of 265 random economies near the instance. In 14 of these, Definition 1 has no equilibrium because support is unfunded at rho, yet this competitive configuration exists.

**No such configuration** in the delta = 0.2 economy, where c_o stays between -0.99 and -0.67 over all admissible returns, or in the recursive-automation economy.

**Lemma A.1(a) at beta = 1.** Withholding all land for 1 or 5 periods, paid for by buying fewer machines, keeps consumption at c* = 0.192389 in every period. That plan is optimal, contrary to "every optimal plan rents out T in every period".

Script: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/verify/c5_zero_consumption.py
