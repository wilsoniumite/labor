# Hours: the intensive margin in the model (2026-10-09, theory and coverage only, no data values)

Her question: if exit is a consumption problem, so is leisure; would hours sharpen the model? A theorist derived
the extension with sympy, an adversarial critic re-derived and judged it, and a scout checked data coverage.

## The extension (theorist)

MINIMAL HOURS EXTENSION (no data were looked at; the IPUMS files you put in /data were not opened, since this task was theory only).

Units: goods are the numeraire. omega = w/p is the goods wage, v = w/r is the wage in rent units, q = r/p, and omega = v q. At an active contestable margin, w = c(r) gamma(x*) with c = b r/(1-a-lambda gamma), so v = b gamma(x*)/(1-a-lambda gamma) is pinned by technology. Write epsilon = dlog w/dlog r for the pass-through (epsilon = 1 at fixed x*).

Household (one person, time 1, hours n in [0,1], leisure l = 1-n). Each type has land a (ownership income q a, as in App. B where A = a - h in rent units), base housing h, goods-fixed nonlabor income A0 (0 in App. B), leisure taste theta, and a participation cost chi.

Leisure is a household commodity, L = CES(l, k, x; elasticity rho). The Leontief case (rho -> 0) uses kappa units of non-produced services and phi goods (price pi) per leisure hour.

Work also needs f units of non-produced services per worker that do not scale with hours (workspace, a dwelling near the job). If the employer bears this cost at the margin, the competitive hourly wage is w(n) = c(r) gamma(x*) - f r/n, which is the same as a work-side housing requirement h_w = h + f.

Budget (n > 0):
  g + q(h + f) + (q kappa + pi phi)(1 - n) = omega n + q a + A0
Full income M = omega + q(a - h - f) + A0. Full price of a leisure hour P_L = omega + q kappa + pi phi (in rent units v + kappa + p pi phi; relative to the wage, 1 + kappa/v + ...).

Preferences: u = g^(1-s)/(1-s) + theta log L - chi 1[n > 0]. The case s = 1 is App. B's log. s > 1 means income effects dominate.

Interior (Leontief, s = 1): l* = theta/(1+theta) * M/P_L.
General s: FOC theta/l = P_L g^(-s).
CES inputs (outer log): l = theta/(1+theta) M alpha^rho omega^(-rho) P_L^(rho-1).

Exit (n = 0, l = 1): g_e = max(q(a - h - kappa) + A0 - pi phi + s0x, s_u). This is the paper's A + s(q), with exit-specific services h_e = kappa (a whole day of leisure) and the dependency floor s_u.

Participation: work iff V_w = (1+theta) log M - theta log P_L + log(1/(1+theta)) + theta log(theta/(1+theta)) - chi >= log g_e (log case).

Equivalence used throughout: the Leontief leisure-space requirement is a standard labor-leisure model with effective wage (v + kappa) q and a lump-sum charge -kappa q. That is, a Stone-Geary-type subsistence cost of leisure indexed to RENT, not to goods; its weight relative to the wage is kappa/v.

### (i) Rent at a fixed goods wage: d log l/d log q|omega = q(a-h)/M - q kappa/P_L (log, Leontief). In general CRRA: sign(dl...

(i) Rent at a fixed goods wage: d log l/d log q|omega = q(a-h)/M - q kappa/P_L (log, Leontief). In general CRRA: sign(dl/dq) = sign[-kappa g + s P_L((a-h) - kappa l)]. Hours rise with q for every household whose net position including leisure space is short (a - h <= kappa l), for any s > 0. This covers renters and owner-occupiers (a = h). Net-long owners may cut hours (the income effect). With substitutable inputs, d log l/d log q = q(a-h)/M + (rho-1) s_k, where s_k is the space cost share of leisure.

*Derivation.* h1_core_logcd.py: closed-form l* from the Lagrangian; the numerator of dl/dq is theta[(a-h)(omega+pi phi) - kappa(omega+A0)], checked with sympy. h2_crra.py: implicit differentiation of the FOC, with F_l = -theta/l^2 - s P_L^2 g^(-s-1) < 0; the sign object is checked symbolically. h3_ces_inputs.py: Shephard's lemma and cost shares, checked by exact-rational evaluation at random points. The Leontief limit rho -> 0 reproduces h1.

*Conditions.* The sketch's sign (rent raises hours at zero net position) needs kappa > 0 at the MARGINAL leisure hour and rho < 1 (time and space are complements in leisure). If the space is a per-household stock (dwelling size independent of hours at home), it acts like h: only the income channel survives, and outright owner-occupiers' hours do not respond. With rho = 1 (Cobb-Douglas) the substitution term is 0. With rho > 1 the sign reverses: rent raises leisure time by lowering its space intensity. kappa is therefore mostly energy, travel and site-based recreation, and only marginally floor space.

### (ii) Automation that lowers v = w/r. At fixed q (log case): sign(dl/dv) = sign[q kappa + pi phi - q(a-h) - A0], the non-...

(ii) Automation that lowers v = w/r. At fixed q (log case): sign(dl/dv) = sign[q kappa + pi phi - q(a-h) - A0], the non-wage cost of a leisure hour minus nonlabor income. So a fall in w/r RAISES hours for anyone whose nonlabor income is below the non-wage cost of leisure, and lowers hours (toward exit) for net owners, as in App. B. CRRA: leisure rises with v iff s P_L n > g, a set that grows with s. Special case A0 = 0, phi = 0: l* = theta/(1+theta) (v + a - h)/(v + kappa), so hours depend ONLY on the wage deflated by rent, not on the goods wage. Pass-through: d log l/d log q = [q(a-h) + epsilon omega]/M - [epsilon omega + q kappa]/P_L. Its derivative in epsilon is omega/M - omega/P_L, and at epsilon = 1, A0 = 0, phi = 0 it is exactly 0. A rent shock fully passed into the wage leaves hours unchanged; only a change in technology (v) moves them.

*Derivation.* h1_core_logcd.py: substitute omega = v q; the dl/dv numerator is -q theta(A0 + q(a-h) - q kappa - pi phi), checked. dl/dq|v has sign pi phi(v+a-h) - A0(v+kappa). The pass-through elasticity is checked at levels. h2_crra.py: the sign object of dF/dv is q[-g + s P_L n], checked.

*Conditions.* Requires the replacement closure (w = c(r) gamma(x*), so v is technological) and the Leontief leisure inputs. Goods wage growth at fixed v (rising q) moves leisure under s = 1 only through the goods part of leisure cost and through A0. If A0 > 0 (price-indexed pensions), rising q at fixed v raises hours, which links to LR-O2. If epsilon < 1, rent shocks also move v.

### (iii) Cheaper goods used in leisure. Leontief: d log l/d log pi = -pi phi/P_L (log); the CRRA sign object is -phi(g + s ...

(iii) Cheaper goods used in leisure. Leontief: d log l/d log pi = -pi phi/P_L (log); the CRRA sign object is -phi(g + s P_L l) < 0. Cheaper leisure goods raise leisure and lower hours for every s, with a bounded effect: l(pi -> 0) = theta/(1+theta) M/(omega + q kappa). Substitutable inputs: d log l/d log pi = (rho-1) s_x. For rho < 1 cheaper leisure goods raise leisure time; for rho > 1 they lower it, because goods replace time in leisure.

*Derivation.* h1 (closed form and limit), h2 (implicit sign object -phi(g + s P_L l), checked), h3 (CES elasticity (rho-1)s_x).

*Conditions.* The sign depends on rho (time vs goods within leisure) and not on income vs substitution. Under the pinned economy, cheaper goods lose weight in P_L as goods prices approach their rent content, so this channel fades when q nears its bound 1/b.

### (iv) Interaction with participation; who exits and who cuts hours. (a) The model microfounds the paper's reduced-form sl...

(iv) Interaction with participation; who exits and who cuts hours. (a) The model microfounds the paper's reduced-form slope h_e - h_w: in goods, d(work - exit)/dq = kappa n - f. Exit is more space-intensive than work because the leisure hours it adds use space (kappa n). Work is more space-intensive if the job carries a fixed space bill f. Full-timers (kappa n > f) are pushed toward work by rent; short-hours workers (kappa n < f) are pushed away. (b) dD/dq|omega = (1+theta)(a-h-f)/M_w - theta kappa/P_L - (a-h-kappa)/g_e. At a goods-fixed dependency floor this is negative for renters and owner-occupiers: floor-available types move to exit as rent rises, which is the participation study's floor kink, now with hours. (c) When v falls 10% at fixed q (illustrative): for renters and owner-occupiers the marginal participants exit (theta_m 1.27 -> 1.06 for renters) while inframarginal workers LENGTHEN hours (0.840 -> 0.855). For net-long owners both margins fall: exit (theta_m 0.99 -> 0.90) and shorter hours (0.520 -> 0.507). Hours per worker and the employment rate therefore move in opposite directions among the short. Owners mostly exit rather than shorten.

*Derivation.* h4_participation_parttime.py: sympy check of the linear reduced-form slope kappa n - f, the indirect utility V_w, and dD/dq. Numeric marginal participant: root of D(theta) = 0 on theta < theta_c (the interior range), with h = 0.3, kappa = 0.2, f = 0.1, phi = 0.05, s_u = 0.05.

*Conditions.* Log utility, Leontief leisure; theta is the heterogeneity; at least one fixed cost (f > 0 or chi > 0), without which the in/out margin is just the hours corner and there is no jump. The floor regime matters, as in LR-K1: a rent-indexed in-kind floor (parental room) flattens the q-response of exit. The exit-vs-hours split rests on tenure/net position, which in microdata is observed only with error (mortgagors are partly hedged).

### (v) Part-time and partial retirement: the fixed-cost squeeze. With per-worker space f, the hourly wage in rent units is ...

(v) Part-time and partial retirement: the fixed-cost squeeze. With per-worker space f, the hourly wage in rent units is v(n) = v - f/n. The proportional part-time penalty f/(n v) rises as w/r falls, and zero-earnings hours n0 = f/v rise. More generally, any fixed cost of participating (f, or a utility cost chi) makes the shortest hours anyone works, n_R (the marginal participant's interior hours), rise as v falls. Illustrative, f = 0.1: n_R rises from 0.33 to 0.98 (renters), 0.21 to 0.73 (owner-occupiers) and 0.13 to 0.40 (net-long owners) as v goes from 3 to 0.5. dn_R/dv < 0 at every grid point, and for chi = 0.1 with f = 0 too. Partial retirement (high a, high theta) is squeezed into full retirement: older owners leave rather than shorten hours. Remote work, which moves f into the worker's own kappa, relaxes the squeeze.

*Derivation.* h4_participation_parttime.py: symbolic v(n) penalty and its v-derivative; tables of n_R by wealth and v; finite-difference dn_R/dv for (a, f, chi) in {0, 0.3, 1.2} x {(0.1, 0), (0, 0.1)}.

*Conditions.* The f channel is model-specific only if workspace is rent-priced at the margin, so the squeeze tracks w/r_commercial (the wage deflated by office/site rent) and not w/p. With only chi, the squeeze tracks the goods wage, as in any fixed-cost model (Cogan 1981). The numbers are illustrative calibration, not estimates. Hours regulation, part-time mandates and women's entry dominate actual part-time shares.

### (vi) Long-run path and Keynes. The sketch's claim that rent-priced leisure by itself stops hours falling as goods produc...

(vi) Long-run path and Keynes. The sketch's claim that rent-priced leisure by itself stops hours falling as goods productivity rises is FALSE for s > 1. The space requirement is a wage-like scale factor: with A0 = 0, phi = 0, F = theta/l - q^(1-s)(v + kappa) G(l)^(-s), so dl/dq|v has the sign of (s-1) and l -> 1 as q -> infinity. What stops the decline is (a) a bound on q: goods need b units of the non-produced input, so p >= b r and q <= 1/b (the paper's purchasing-power bound), together with (b) a fall in v, which raises kappa/v, the rent-indexed subsistence weight. Under s = 1, hours never trend with goods-wage growth (the KPR benchmark gives l = theta/(1+theta)), so the 1950-80 decline itself needs s > 1, a goods-indexed subsistence term, A0, or falling pi. Simulated paths (theta lognormal, a = h): when q grows 2.5%/yr unbounded at fixed v, s = 2 hours keep falling ~0.27-0.30%/yr through 2020 with or without kappa. When q saturates and v falls 1.2%/yr after 1980 (goods wage falling), hours per worker turn up for renters and owner-occupiers, while net-long owners exit: participation 0.83 -> 0.57 at s = 1. When the goods wage keeps rising 0.5%/yr after 1980 (q +1.5%, v -1%): s = 2 hours change -0.47%/yr then +0.03%/yr with kappa = 0.2 and f = 0.1, against -0.64%/yr then -0.15%/yr in the clean kappa = f = 0 benchmark. The rent channel adds about +0.2 pp/yr; most of the stall comes from slower goods-wage growth, which the standard model also predicts.

*Derivation.* h2_crra.py: scale argument (dF/dq = (kappa+v)(s-1)/(q^s G^s), sympy) and the effective-wage equivalence. h1: limits (q -> infinity gives l -> theta(a-h+v)/((1+theta)(kappa+v)); v -> 0 gives l -> theta q(a-h)/((1+theta)(q kappa + pi phi))). h5_longrun_path.py: heterogeneous-theta simulation with fixed costs, three paths, and a clean benchmark.

*Conditions.* s > 1 is needed for any secular decline. The stall or reversal requires q to approach its rent-content bound and v = w/r to fall. Net-short households lengthen hours; net-long owners exit, so hours per worker rise partly by composition. Magnitudes are illustrative, and kappa is not separately identified from the level of v except through rent variation at a fixed goods wage.

## Testable predictions proposed

- **H1** The deflator split: holding the wage deflated by goods prices, a lower wage deflated by rents goes with longer hours per worker. In the clean standard model (owned housing, no rent-priced leisure or workspace) the rent deflator has no role. Measure: Country-year panel 1950+ (annual hours per worker, e.g. Conference Board TED / PWT / OECD). Regress log hours per worker on log(w/p_goods ex-shelter) and log(w/r) (rent CPI or market rent index), with country and year FE. Run 1950-1980 and 1980+ separately. Simulated grid coefficients on log(w/r): -0.13 (s=1) / -0.12 (s=2) with kappa > 0, against about -0.07 with kappa = 0 (that remainder comes from f and the floor). Sign: coef on log(w/r) < 0; coef on log(w/p) <= 0 (≈0 if s=1, <0 if s>1)
- **H2** The tenure test, the distinctive core: outright owner-occupiers (zero net rent position) also work longer when w/r falls at a given goods wage. Without per-hour rent-priced leisure their hours do not respond, and only renters respond, through the income effect. Measure: LFS / IPUMS-type microdata where tenure is recorded (usual hours of employed 25-54 by sex). log hours on log(w/r) x tenure (outright owner, mortgagor, renter) with country-year controls for log(w/p). Sign: outright owners: < 0 (standard model: 0); renters: more negative than owners
- **H3** Opposite margins when w/r falls: hours per worker rise while participation falls among floor-available and net-long groups. Owners and older people exit rather than shorten hours. Measure: LFS employment rate and usual hours per employed by age and sex (25-34, 55-64, 65-69). Changes against Δlog(w/r) at given Δlog(w/p); the covariance of Δhours-per-worker with Δemployment-rate across country-periods of falling w/r. Sign: Δhours/worker on Δlog(w/r): -; Δemployment rate (55-69, floor-available young) on Δlog(w/r): +; their covariance across falling-w/r episodes: < 0
- **H4** The part-time squeeze: the part-time share and partial retirement shrink when the wage falls relative to workspace rent. The shortest hours worked rise. Measure: OECD part-time share (<30h) overall and for 55-64 / 65-69 by sex, and the 10th percentile of usual hours among the employed. Regress on log(w / commercial or office rent) and log(w/p), with FE. Event: the post-2020 remote-work shift lowers f, which should raise part-time and partial retirement. Sign: coef on log(w/r_commercial) > 0 (higher wage-to-workspace-rent ratio, more part-time); post-remote-work part-time share among 55-69: +
- **H5** Leisure-goods prices: falls in the relative price of goods used in leisure lower hours if time and goods are complements in leisure (rho < 1). Not distinctive to the paper. Measure: Country-year hours per worker on log(CPI recreation & AV equipment / CPI all goods), with FE. Sign: coef > 0 if rho<1 (cheaper leisure goods → fewer hours); < 0 if rho>1
- **H6** The Keynes stall: the secular decline of hours per worker slows or reverses once goods prices approach their rent content and w/r falls. The slowdown is larger than slower goods-wage growth alone implies. Measure: Within-country trend breaks in log hours per worker, 1950-2020. Δlog hours on Δlog(w/p) and Δlog(w/r), interacted with the shelter + energy share of the CPI basket (a proxy for q near its bound 1/b). Compare residual post-break trends with and without the w/r term. Sign: the w/r term absorbs part of the post-break slowdown (coef on Δlog(w/r) < 0); hours decline is slower where the shelter+energy share is higher
- **H7** Sign of the participation response by usual hours (h_e - h_w = kappa n - f): rent at a given goods wage pushes full-time groups toward work and short-hours groups (high fixed job cost relative to hours) away. Measure: LFS activity rates by group on log q_{t-1} (rent CPI / goods CPI), interacted with the group's pre-period mean usual hours (e.g. prime-age men vs women 1960s-80s, by country), with country and year FE. Sign: interaction (q-slope x group mean hours) > 0
- **H8** Price-indexed nonlabor income: at a given w/r, goods-wage growth raises the hours of older workers whose pensions are fixed in goods (A0), relative to those with wage-indexed pensions (extends LR-O2 to the intensive margin). Measure: Usual hours of employed 60-69 on log(w/p) x price-indexation indicator (legal dates coded before outcomes), controlling for log(w/r), with country and year FE. Sign: interaction > 0

## The critic's verdicts

### (i) rent at a fixed goods wage — holds: with_conditions

*Against other accounts.* The algebra is right. Becker (1965) already contains it: a leisure commodity with a rent-priced input has full price w + r k. For RENTERS the sign is the same as the standard model with a rent-priced housing need h (q(a-h)/M < 0 with kappa = 0), so it is not distinctive for them. It is distinctive only for owner-occupiers (a = h). There, standard models with fixed or separable housing (Boppart-Krusell, Prescott, Blanchard) predict 0. Housing-wealth studies (house-price gains lower owners' labor supply, e.g. Disney-Gathergood; mortgage commitment raises hours, e.g. Fortin 1995, Del Boca-Lusardi 2003) predict 0 or the OPPOSITE sign. Home-production models with home capital (Benhabib-Rogerson-Wright 1991, Greenwood-Hercowitz 1991, McGrattan-Rogerson-Wright 1997, Fisher 2007; also Ngai-Pissarides through marketization) predict the SAME sign whenever home time and home capital are complements, governed by the same elasticity rho. So the owner sign is new only against fixed-housing and wealth-effect accounts.

*Best test.* Owner-occupiers' usual hours (prime-age men, employed) on log q_{t-1} at given log(w/p), with country and census-round FE. Prediction: hours rise with q. This is the only moment that separates kappa from a rent-priced housing need: in the log closed form the renter-minus-owner gap is -q h/M under both models, so a within-country-year tenure DiD is uninformative.

*Problems.* I re-derived the log closed form, the CRRA sign object -kappa g + s P_L[(a-h) - kappa l] and the CES elasticity q(a-h)/M + (rho-1)s_k (c1_symbolic.py); all are correct. The size is the product of two small things, s_k and |rho-1|, and time-goods elasticities in home production are close to 1 and imprecise. Floor space is a stock, so its per-hour use is near zero except through dwelling choice in the long run. kappa is then mostly energy, travel and site recreation, which a shelter-rent q does not measure: the proposed regressor mismatches the mechanism.

### (ii) automation lowering v = w/r — holds: with_conditions

*Against other accounts.* Algebra confirmed: sign of dl/dv, the special case l = theta/(1+theta)(v+a-h)/(v+kappa), the pass-through elasticity and its zero at epsilon = 1 with A0 = phi = 0. But the 'hours depend only on w/r' structure is not unique to kappa. A standard renter with kappa = 0 and a rent-priced housing need gets l = theta(v-h)/((1+theta)v), which also depends only on v (c1). Boppart-Krusell and Blanchard make hours depend on w/p only. Prescott makes them depend on the tax wedge. At the paper's bound q = 1/b, d log(w/p) = d log v, so the kappa model and any s > 1 income-effect model agree in sign there.

*Best test.* None at the aggregate. The owner-occupier slope (see (i)) is the only clean separation. The pass-through result implies that rent shocks absorbed into wages leave hours unchanged, which cannot be falsified without an independent measure of epsilon.

*Problems.* Year FE absorb the common technological v, which is the paper's own pinned object. What remains of w/r variation across country-years is housing-supply, rent-control and interest-rate variation, so no panel hours test touches the pinning; it tests only the household auxiliary kappa. There is also a cross-section tension (c2 item 4). Within a country-year, kappa > 0 makes owners' hours fall with the individual wage. That is the 1890 gradient (Costa 2000), opposite to the modern positive gradient for men (Kuhn-Lozano 2008).

### (iii) cheaper leisure goods — holds: yes

*Against other accounts.* Not distinctive. This is Becker's goods-time composition result. Aguiar-Bils-Charles-Hurst (leisure luxuries, video games and young men's hours) is the same sign under rho < 1. Ngai-Pissarides and the home-production literature carry the same elasticity logic.

*Best test.* None for this protocol; at most a descriptive check.

*Problems.* The CRRA sign object -phi(g + s P_L l) and the CES (rho-1)s_x are confirmed. The sign rests entirely on rho, which is unknown. The claim that 'this channel fades near q = 1/b' rests on the bound, which the rising rent/goods ratio shows is not binding in sample.

### (iv) participation and hours interaction — holds: with_conditions

*Against other accounts.* (b), the floor case, is the participation study's existing floor kink and adds nothing new about hours. (c), hours per worker moving opposite to the employment rate, follows from the selection and composition present in any model with fixed costs and heterogeneity (Cogan 1981; any selection model), so it is not distinctive. (a)'s hours-dependent sign would be distinctive, but it does not hold (see problems).

*Best test.* None as a verdict. (b) is already covered by LR-K2.

*Problems.* V_w and dD/dq are confirmed (c1). But (a), d(work-exit)/dq = kappa n - f, is goods accounting, not the participation sign. The exact derivative is u_w(kappa n - f) + (u_e - u_w)(h + kappa - a). Because exit consumption is lower (u_e > u_w), net-short types are pushed toward work whatever their hours. In 3071 random interior log-case draws off the floor, sign(dD/dq) differs from sign(kappa n - f) in 33% (c2 item 1), including cases with kappa n < f where rent pushes toward work. The (c) numbers come from a calibration with inframarginal hours of 0.84 of the time endowment, so their magnitudes mean nothing.

### (v) part-time squeeze — holds: with_conditions

*Against other accounts.* This is a Cogan (1981) fixed-cost result. It is distinctive only if f is rent-priced and only through variation in workspace rent at a given goods wage. kappa plays no role. My rerun (c2 item 5) gets the squeeze with kappa = 0 and f = 0.1, and it also rises with q at a fixed goods wage. Standard accounts (regulation, part-time mandates, female entry) dominate the actual part-time shares.

*Best test.* None in the long-run protocol. Commercial-rent series are not in the manifest, and the post-2020 remote-work event is already history and confounded by the cycle and retirement.

*Problems.* The assumption that the employer bears per-worker space at the margin conflicts with desk sharing: much workspace scales with FTE, not headcount. n_R = 0.98 is the marginal participant working 98% of the time endowment, which means the calibration is degenerate near subsistence. Known history runs the other way: part-time shares rose in Europe from 1980 to 2010 while rents rose relative to wages.

### (vi) long run and Keynes — holds: with_conditions

*Against other accounts.* The colleague's correction holds: the sketch is false under s > 1 with unbounded q (dF/dq|v = (s-1)q^-s(v+kappa)G^-s, confirmed), and with s = 1 there is no trend at all. What is left is that hours stop falling when goods-wage growth stops. Boppart-Krusell (2020) predicts exactly that, with hours falling in proportion to wage growth. The paper's own goods-wage ceiling w/p <= v/b = gamma/(1-a-lambda gamma) is what stops goods-wage growth, and it does so without kappa (this ceiling does not depend on b). In my rerun of path 3 (c2 item 3), the rent channel adds about +0.18 pp/yr, and f alone (kappa = 0) gives about the same as kappa alone. So the stall is not kappa-specific. Blanchard reads the US-Europe gap as preferences, and Prescott reads it as taxes.

*Best test.* None with a verdict. US hours per worker flattened after about 1980, European hours kept falling to about 2000 and then flattened, and the paper itself already shows the US w/shelter vs w/durables divergence for 1964-2024. Any test of the stall is therefore a postdiction.

*Problems.* The path in which the goods wage falls after 1980 is counterfactual. The prediction that participation of net-long owners falls (0.83 to 0.57) contradicts the known rise in 55-64 employment since the late 1990s, which pension reform confounds. The 'answer to Keynes' belongs to the paper's existing purchasing-power ceiling, not to the hours extension.

### H1 deflator split (aggregate) — holds: with_conditions

*Against other accounts.* Not distinctive in sign or in size. In c2 item 2, a kappa = 0 economy with a 35% renter share and f = 0.1 gives a coefficient on log(w/r) of -0.114 (s=1) and -0.128 (s=2). The kappa = 0.2 owners-only economy gives -0.125 and -0.120. A rent-priced Stone-Geary housing need predicts the same sign. Davis-Ortalo-Magné (constant housing share) predicts about 0. Prescott (VAT raises p but not rents) and energy-price cycles load mechanically on q. Boppart-Krusell predicts a coefficient of 0 on w/r and < 0 on w/p.

*Best test.* Report with no verdict, with the tax wedge and the cycle controlled.

*Problems.* Postdiction: US hours flat while q rose since 1980 is known. A shelter-rent q also misses kappa's likely content (energy, sites).

### H2 tenure test (owner-occupiers) — holds: with_conditions

*Against other accounts.* This is the only prediction whose sign separates the kappa model from fixed or separable-housing models (owners' slope 0) and from the housing-wealth literature (owners' hours fall when house values rise). It does NOT separate it from home-production models with home capital complementary to home time (Benhabib-Rogerson-Wright, Greenwood-Hercowitz, McGrattan-Rogerson-Wright, Fisher), which predict the same sign. Mortgagors also have a = h. The outright/mortgage split matters only for leverage and wealth, so OWNERSHP (owned vs rented) is enough.

*Best test.* Usual hours of employed owner-occupier men aged 25-54 (cells by country × census round) on log q_{t-1}, controlling for log(w/p), with country and round FE and the cycle control. Predicted: hours rise with q. Not a renter-minus-owner DiD, which cancels kappa exactly.

*Problems.* Identified only from between-country-year variation, so it is exposed to taxes, cycles and rent control. A null or negative result is weak evidence, because wealth effects for older or net-long owners offset it. The test is asymmetric: support is informative, contradiction is not decisive. Tenure is selected by age and wealth and responds to q. Census-year cells give few observations per country, so power is likely low. Shelter rent is a poor proxy for the marginal leisure input. Feasibility (hours and ownership in the frozen IPUMS samples, and a goods-deflated wage in the manifest) must be settled from codebooks only. I did not open the IPUMS files in /data.

### H3 opposite margins — holds: no

*Against other accounts.* Negative covariance between hours per worker and the employment rate follows from selection or composition in any fixed-cost model. Pension-reform accounts explain older workers' participation.

*Best test.* None.

*Problems.* Known history works against it: employment of 55-64s rose across the OECD from the late 1990s while w/r fell. It overlaps the participation tests and is confounded by reforms.

### H4 part-time squeeze — holds: no

*Against other accounts.* Cogan fixed costs, regulation and female entry account for part-time shares. kappa is not involved (c2 item 5).

*Best test.* None.

*Problems.* Commercial-rent series are not in the manifest. The European part-time rise from 1980 to 2010 is known history against it. The remote-work event after 2020 is already published and confounded by COVID retirements and the tight labor market.

### H5 leisure-goods prices — holds: with_conditions

*Against other accounts.* Not distinctive, as the colleague says: it is Becker or Aguiar-Bils-Charles-Hurst, with the sign set by rho.

*Best test.* None.

*Problems.* The sign is unknown ex ante, so there is no prediction to test.

### H6 Keynes stall — holds: no

*Against other accounts.* Boppart-Krusell predicts a stall from slower goods-wage growth. Prescott (taxes) and Blanchard (preferences) explain the US-Europe pattern. The rent term adds about 0.2 pp/yr, comparable to the f-only and Stone-Geary-renter versions.

*Best test.* None with a verdict. Report descriptively.

*Problems.* Pure postdiction: the trend breaks are known, and so is the paper's own w/r history. Interacting with the shelter + energy CPI share is ad hoc, and the q bound is not binding in sample.

### H7 participation by usual hours — holds: no

*Against other accounts.* The standard income-effect account, and the 'two-income trap' (high housing costs push secondary earners into work), predict the OPPOSITE sign: the largest positive q-response among low-hours groups.

*Best test.* None.

*Problems.* The sign derives from (iv-a), which fails as a utility sign in 33% of draws. Women's participation rising while q rose is known history against it, and it overlaps the no-verdict C-3L.

### H8 price-indexed pensions — holds: with_conditions

*Against other accounts.* The standard life-cycle income effect predicts the same sign. It is not specific to rent.

*Best test.* None.

*Problems.* It needs hand-coded indexation dates, the reason the protocol dropped LR-O2, so it is infeasible under the protocol's own rules.

## The critic's recommendation

Do not add an hours verdict family to the participation long-run protocol. Its model-level verdict rests on LR-K2, and every hours test checks a new household-side auxiliary assumption, kappa > 0 at the marginal leisure hour with rho < 1. None of them tests the paper's pinning, because year fixed effects absorb the common technological w/r. Most hours predictions are either shared with standard accounts or already known history (US hours flat after about 1980, European hours falling then flattening, the paper's own US w/r series).

If the researcher wants hours in the protocol at all, use at most ONE verdict test, in a separate family H-L that never enters or alters the LR-K2 or joint reading. That test is the owner-occupier slope (a restated H2):
- Outcome: usual hours of employed owner-occupier men aged 25-54, by country and census round from the frozen IPUMS samples.
- Regressor: log q_{t-1}, controlling for log(w/p), with country and round FE and the cycle control.
- Prediction: hours rise with q.
- Foils: fixed or separable-housing models (0) and housing-wealth effects (negative). State that home-production models with complementary home capital predict the same sign.
- Readings: support counts; contradiction reads "dominated by wealth effects, not decisive".
- Drop the strict rent-control years, as in LR-RC.

Report with no verdict:
- the renter slope, and the renter-minus-owner gap against the rent share of income, as consistency checks;
- the aggregate deflator split (H1) and the Keynes-stall description (H6), labelled postdictions.

Drop H3, H4, H5, H7 and H8.

Preconditions, settled before the L-freeze from codebooks and metadata only, without opening the IPUMS extract now in /data (I did not open it):
- an hours variable and OWNERSHP present in enough frozen samples (for example at least 8 countries with at least 3 rounds);
- a goods-deflated wage series in the manifest;
- a skeleton MDE no larger than the participation benchmark's.

If any precondition fails, run the H-L test as a no-verdict exploratory. Leave the second verdict slot empty: no other hours prediction is both distinctive and not already known history.

Checks: C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\hours_crit\c1_symbolic.py and c2_numeric.py.

## Data coverage (scout)

Long-run cross-country panel. Use PWT 11.0 avh (annual hours per person engaged, 1950-2023) with the JST R6 wage, cpi and rent ingredients (to 2020). The 16 JST countries that have rent yields (AUS BEL CHE DEU DNK ESP FIN FRA GBR ITA JPN NLD NOR PRT SWE USA) all have avh from 1950, so the core panel is 16 countries x 1950-2020 (71 years). This compares hours per worker with w/p_rent against w/p_goods. Caveats: hpnom starts late for ESP, ITA and PRT, so their rent index uses cumulated capital gains, and CAN and IRL have no rent data. Cross-check avh against OECD DSD_HW@DF_AVG_ANN_HRS_WKD (FRA, SWE and USA from 1950; most countries from 1970) and AMECO NLHA (1960/1970+), which use different national sources. A pre-war extension is possible only with the Huberman-Minns benchmarks: 14 countries, 13 benchmark years 1870-2000 for annual hours, production workers only. Their 1870-1938 points are machine-readable through OWID; the rest is PDF only.

Sex x age (intensive margin by demographic cell). OECD DF_AVG_USL_WK_WKD and Eurostat lfsa_ewhuis/lfsa_ewhais give usual and actual weekly hours by sex x age x FT/PT from 1983 for 9 EU countries (BE DE DK FR GR IE IT LU NL; UK to 2019) and from 1995-2002 for the rest. The US series is employees only, from 1979. Part-time shares by sex x age: OECD national-definition flow (USA 1976, AUS 1966, NOR 1972, CAN FIN SWE 1976) and the harmonised flow (CAN 1976, JPN 1980, EU 1983); Eurostat lfsa_eppga from 1983. The US has the only century-long sex x age series: Ramey-Francis 1900-2005, per capita (to 2012 for 25-54), with IPUMS-USA censuses (HRSWORK2 1940-1990, UHRSWORK 1980-2024) and IPUMS-CPS ASEC (AHRSWORKT 1962+, UHRSWORKLY and WKSWORK1 1976+) as microdata backbone. The BLS LN aggregates by age start only in 2022-10, and the DBnomics mirror stops in 2025-01.

IPUMS-I is thin for hours before 2001. The extract you put in participation/longrun/data has no hours variable. Of its 52 samples from 1960-2000, only 16 (in 7 of 18 countries: CAN GRC CHE USA with HRSWORK1; DEU ISR PRT with HRSWORK2 bands only) have hours on IPUMS-I. A new extract adding HRSWORK1 and HRSWORK2 would be needed.

Usable wage pairs are JST (1870-2020) and AMECO compensation per employee (1960+). OECD AV_AN_WAGE starts in 1990. Avoid TED as a primary source: its licence bars publication and derivative works without permission. PWT 11.0 must be downloaded by hand in a browser (dataverse.nl runs an Anubis bot check, which was not bypassed).

Blinding. Value-bearing files from this scout are in the scratchpad (hours_scout/: OECD, Eurostat, ILO, DBnomics, OWID, JST R6, Ramey-Francis, the Huberman-Minns PDF). Treat them as unblinded and keep them out of any blind phase. Nothing was written in the repository.

- **https://www.rug.nl/ggdc/productivity/pwt/ ; DOI 10.34894/FABVLR ; Excel https://dataverse.nl/api/access/datafile/554105 (the file OWID cites; the second button, 554030, is presumably Stata). PWT 10.0 avh is also on DBnomics as GGDC/penn10 avh.{ISO3}** (Penn World Table 11.0 (Feenstra, Inklaar, Timmer; GGDC), variable avh) — avh = average annual hours worked by persons engaged. PWT 11.0 was published 7 Oct 2025 and covers 185 countries, 1950-2023. Licence CC BY 4.0.; Country x year only. No sex or age.; Counted from OWID's copy of the full 11.0 avh: 130 countries with at least one observation from 1950. 24 start in 1950 (AUS AUT BEL BRA CAN CHE COL DEU DNK ESP FIN FRA GBR IRL ITA JPN MEX NLD NOR PER PRT SWE USA VEN). 45 start by 1970, and 61 start only in 2005. All 38 OECD members are covered. On DBnomics, PWT 10.0 has avh for 69 countries.; 1950-2023 (129 countries end in 2023, one ends in 2014). OECD start years: CHL and GRC 1951, KOR 1953, ISL 1964, LUX NZL TUR 1970, HUN 1980, ISR 1981, CRI 1987, SVK 1990, CZE 1993, the Baltic states, POL and SVN 1995. Within-series gaps in NLD, TWN, ZAF and a few others.
- **OECD.ELS.SAE,DSD_HW@DF_AVG_ANN_HRS_WKD,1.0 ; https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_HW@DF_AVG_ANN_HRS_WKD,1.0/all** (OECD Data Explorer (OECD.ELS.SAE): average annual hours actually worked per worker) — Annual hours actually worked per person employed (UNIT H_Y_PS, HOURS_TYPE ACTUAL, MEAN).; WORKER_STATUS: _T (all) and ICSE93_1 (employees). No sex, no age, no FT/PT split.; 46 areas including the OECD aggregate: AUS AUT BEL BGR CAN CHE CHL COL CRI CYP CZE DEU DNK ESP EST FIN FRA GBR GRC HRV HUN IRL ISL ISR ITA JPN KOR LTU LUX LVA MEX MLT NLD NOR NZL PER POL PRT ROU RUS SVK SVN SWE TUR USA.; 1950-2025 overall. All-worker series: FRA, SWE and USA 1950-2025. FIN 1960, CAN 1961, NOR 1962. BEL COL DEU DNK ESP GBR IRL ISL ITA JPN LUX NLD NZL PRT TUR and OECD from 1970 (TUR ends 2021, COL 2024). AUS 1979, HUN 1980, ISR 1981, GRC 1983, CHL 1986, CRI 1987, CHE and MEX 1991, RUS 1992-2020, CZE and POL 1993, most other EU members 1995, EST 2000, PER 2004, KOR 2008. The employee series start later for most countries (DNK 1966, ESP 1977).
- **OECD.ELS.SAE,DSD_HW@DF_AVG_USL_WK_WKD,1.0** (OECD Data Explorer: average usual weekly hours worked on the main job) — Mean usual weekly hours in the main job, employed persons (H_WK_PS).; SEX F/M/_T x AGE 15-24, 25-54, 55-64, 65+, 15-64 and total x WORKER_STATUS (_T, employees, self-employed and others) x WORK_TIME_ARNGMNT (_T, FT, PT). Sex x age cells have the same year coverage as the totals.; 55 areas (OECD and EU members plus ARG BRA IDN MKD RUS ZAF and aggregates).; 1979-2025 overall. From 1983: BEL DEU DNK FRA GBR GRC IRL LUX NLD (gaps in 1984 and 1986). USA 1979-2025, employees only (no all-worker series for the US). PRT and NZL 1986, ESP 1987, CHE and KOR 1991, SVK 1994, AUT HUN ISR ITA MEX 1995, CHL and NOR 1996, POL 1997, LTU 1998, most new EU members 2000, AUS and FIN 2001, SWE CZE HRV 2002, TUR 2006, CAN JPN and OECD 2009.
- **OECD.ELS.SAE,DSD_FTPT@DF_FTPT_COMMON_INC,1.0 (key ......._T.PT.. ; MEASURE EMP_PT or EMP; UNIT PT_POP_SUB). Related flows: DF_FTPT_COMMON (levels), DF_FTPT_INC_GEN (women's share of part-time).** (OECD Data Explorer: incidence of part-time employment, OECD-harmonised definition (under 30 usual hours)) — Part-time share of employment.; SEX F/M/_T x 22 age bands (5-year bands 15-19 up to 70-74, plus 15-24, 25-54, 55-64, 65+ and others) x WORKER_STATUS x FT/PT.; 54 areas (OECD and EU members, ARG BRA IDN MKD RUS ZAF). No USA.; 1976-2025 overall. CAN 1976, JPN 1980, BEL DEU DNK FRA GBR GRC IRL ITA LUX NLD from 1983, PRT and NZL 1986, ESP and SWE 1987, TUR 1988, FIN KOR NOR 1989, CHE and ISL 1991, RUS 1992-2020, CZE 1993, AUT HUN ISR MEX 1995, AUS 2001.
- **OECD.ELS.SAE,DSD_FTPT@DF_FTPT_NATIONAL_INC,1.0 (key ......._T.PT..)** (OECD Data Explorer: incidence of part-time employment, national definitions) — Part-time share of employment, national definitions.; SEX F/M/_T x AGE 15-24, 25-54, 55-64, 65+, 15-64, total x WORKER_STATUS (_T, employees) x FT/PT.; 53 areas, including USA, AUS and DEU_F.; 1966-2025 overall. AUS 1966, NOR 1972, FRA 1975, USA CAN FIN SWE 1976, EU core 1983, JPN 2000. Sex x age detail: USA 1976-2025, NOR 1972-2025, CAN FIN SWE 1976-2025 (SWE 65+ from 2007), JPN 2000-2025.
- **lfsa_ewhuis (usual) and lfsa_ewhais (actual), 1983-2025; lfsa_ewhuna (usual, NACE Rev.1.1, 1992-2008); lfsa_ewhun2 (usual, NACE Rev.2, 2008-2025); lfsa_ewhana / lfsa_ewhan2 (actual, same splits). API: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{code}** (Eurostat EU-LFS: average usual and actual weekly hours, main job) — Mean weekly hours in the main job.; sex T/M/F x age (Y15-24, Y15-34, Y15-64, Y_GE15, Y20-64, Y25-54, Y25-64, Y35-49, Y_GE50, Y55-64) x wstatus (EMP, SAL, SELF, ...) x worktime (TOTAL, FT, PT) x ISCO-08 or NACE.; 38 geos: EU27 members, EA21, EU27_2020, IS NO CH UK BA ME MK RS TR.; Sex x 25-54, all employed, usual hours: BE DE DK EL FR IE IT LU 1983-2025, NL 1983-2025 with gaps, UK 1983-2019, PT 1986, ES 1987, AT FI IS NO SE 1995, CH HU SI 1996, CZ EE RO 1997, LT LV SK 1998, CY 1999, BG MT 2000, PL 2001, HR and EU aggregates 2002, MK TR 2006, RS 2010, ME 2011-2020, BA 2021. Actual hours: same, except ES from 1986 and PL from 1997. lfsa_ewhuna: 1992-2008 (BE DE DK EL ES FR IE from 1992).
- **lfsa_eppga (also lfsa_epgaed for levels by sex x age x FT/PT x ISCED)** (Eurostat EU-LFS: part-time employment as a share of total employment, by sex and age) — Part-time share of employment (self-declared).; sex T/M/F x 24 age bands (Y15-19 to Y_GE75, including Y25-49 and Y50-64).; Same 38 geos as the hours tables.; 1983-2025. Women 25-49: BE DE DK EL FR IT LU 1983-2025, IE 1983-2025 (one gap), NL with gaps, UK 1983-2019, PT 1986, ES 1987, AT FI IS NO SE 1995, and later entrants as in the hours tables.
- **HOW_TEMP_SEX_AGE_NB_A (also _ECO, _JBT; HOW_TEMP_SEX_ECO_NB_A starts 1948) ; https://rplumber.ilo.org/data/indicator/?id=HOW_TEMP_SEX_AGE_NB_A** (ILOSTAT: average weekly hours actually worked per employed person, by sex and age) — Mean weekly hours actually worked.; sex x age (aggregate bands such as AGE_AGGREGATE_Y25-54, plus 10-year and youth/adult bands) x source.; 248 ref areas in the catalogue. Women 25-54: 161 areas, 15 starting by 1990.; Catalogue 1976-2027. Women 25-54: CAN 1976-2025; BEL DEU DNK FRA GBR IRL ITA LUX NLD from 1983; ESP PRT 1986; GRC 1987; CHE 1991; USA 1994-2025; most others 1995-2000. No JPN, AUS or NZL in the 25-54 band.
- **Average hours at work (tdat 04, wkst 01), not seasonally adjusted, monthly. All 16+: LNU02005054; men LNU02005118; women LNU02005150. By age: both sexes LNU02005058 (16-19) ... LNU02005084 (65+), LNU0201B958 (25-54); men LNU02005132 (25-34) ... LNU02005148, LNU0201B95D (25-54); women LNU02005164 ... LNU02005180, LNU0201B962 (25-54). Usually part-time (lfst 26, thousands): LNU02600000/01/02 (both/men/women 16+), LNU02600060/61/62 (25-54), LNU02600012 (16-19), LNU02624230-32 (55+). Hours bands 35+: LNU02024369 (both), LNU02022606/07 (men/women).** (BLS CPS (Labor Force Statistics, LN) via DBnomics BLS/ln) — Mean weekly hours at work, counts of usual part-time workers, and hours bands, from the CPS.; sex x age (16-19, 20-24, 25-34, 35-44, 45-54, 55-64, 65+, 25-54, 55+). Part-time by sex x age 16-19, 20+, 20-24, 25+, 25-54, 55+.; USA; Average hours by sex (all ages): 1976-06 to 2025-01. Average hours by age, and by sex x age: only 2022-10 to 2025-01 (28 months). Part-time by sex, 16+ and 16-19: 1968-01 to 2025-01. Part-time by sex x other ages: 1986-01 to 2025-01. 35+ hour band: 1976-06 (by sex from 1983-01).
- **https://cps.ipums.org : AHRSWORKT (hours worked last week), UHRSWORKLY (usual hours last year), WKSWORK1 (weeks worked last year), UHRSWORK1 (usual hours, main job)** (IPUMS-CPS (ASEC and basic monthly microdata)) — Person-level hours and weeks worked. Annual hours = usual hours x weeks.; Any sex x age x education cell (microdata).; USA; AHRSWORKT: ASEC 1962-1988, then every month 1989-2026. UHRSWORKLY and WKSWORK1: ASEC 1976-2026. UHRSWORK1: monthly 1982-2026.
- **https://usa.ipums.org : HRSWORK1, HRSWORK2, UHRSWORK** (IPUMS-USA (decennial census and ACS microdata)) — Hours worked last week (continuous or intervalled) and usual hours per week last year.; Any sex x age cell.; USA (and Puerto Rico); HRSWORK1: 1940, 1950, 1980, 1990. HRSWORK2 (intervals): 1940, 1950, 1960, 1970, 1980, 1990. UHRSWORK: 1980, 1990, 2000-2024 (ACS).
- **https://international.ipums.org/international-action/variables/HRSWORK1 and .../HRSWORK2 . User's extract: C:\Users\s6068C\GitHub\laborformal\participation\longrun\data\ipumsi_00001.csv.gz** (IPUMS-International: HRSWORK1 (hours per week, continuous) and HRSWORK2 (intervalled)) — Usual or last-week hours worked, harmonised across censuses and surveys.; Any sex x age cell (microdata).; HRSWORK1: 30 countries. HRSWORK2: 34 countries. 1960-2000, either variable: 26 countries, 55 country-years. OECD and European samples in 1960-2000: CAN 1981, 1991; DEU 1970 (HRSWORK2 only); GRC 1971, 1981, 1991; ISR 1972, 1983, 1995 (HRSWORK2 only); MEX 1990, 1995, 2000; PRT 1991 (HRSWORK2 only); CHE 2000; USA 1960, 1970 (HRSWORK2 only), 1980, 1990, 2000. Others in 1960-2000: BRA, DOM, ECU, SLV, GHA, HND, IDN, JAM, MYS, MUS, NIC, PAK 1973, PAN 1970, PHL LFS 1997-2000, PRI, LCA, TTO, VEN.; HRSWORK1: 296 samples in total (1970s 4, 1980s 11, 1990s 28, 2000s 103, 2010s 140, 2020s 10); 54 of them in 1960-2000. HRSWORK2: 313 samples (one in the 1960s: USA 1960); 67 in 1960-2000. After 2000: ESP 2001 plus LFS 2005-2020; ITA LFS 2011Q1-2020Q1 (not the 2011 census); HUN 2001; PRT 2001 and 2011 (HRSWORK2); CHE 2011; CAN 2001 and 2011; GRC 2001 and 2011; USA 2005-2020.
- **PDF: https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp95.pdf ; RePEc https://ideas.repec.org/p/iis/dispap/iiisdp95.html ; machine-readable 1870-1938 portion: https://ourworldindata.org/grapher/annual-working-hours-per-worker.csv** (Huberman and Minns (2007), 'The times they are not changin'', Explorations in Economic History 44(4):538-567; working paper IIIS DP 95 (2005), 'Hours of Work in Old and New Worlds: The Long View, 1870-2000') — Table 1: weekly hours of full-time production workers. Table 2: vacation plus holiday days. Table 3: annual hours of work.; Country x benchmark year. Table 1 splits 2000 into men and women; otherwise no sex or age split. Old World / New World averages.; 14: BEL DNK FRA DEU IRL ITA NLD ESP SWE CHE GBR AUS CAN USA.; Table 3 (annual hours): 1870, 1880, 1890, 1900, 1913, 1929, 1938, 1950, 1960, 1973, 1980, 1990, 2000. Table 1 (weekly): 1870, 1880, 1890, 1900, 1913, 1929, 1938, 1950, 1960, 1970, 1980, 1990, 2000 (M and F). Table 2 (days): 1870, 1900, 1938, 1950, 1980, 1990, 2000. OWID's CSV carries the 1870-1938 benchmarks only (7 benchmark years x 14 countries) and splices PWT 11.0 avh from 1950.
- **https://www.conference-board.org/topics/total-economy-database (downloads through TCB Data Central after creating a free account)** (The Conference Board Total Economy Database (TED), Output, Labor and Labor Productivity (May 2025) and Growth Accounting (Sept 2025)) — Employment and total hours worked (hours per worker can be derived), GDP, labour quality, and the labour share.; Country x year. No sex or age.; 131 countries (stated on the page). Per-country hours coverage was not checked.; Release vintages May and Sept 2025. 2024 values are estimates and 2025 values are forecasts. The start year of the hours series was not verified (the page does not state it).
- **https://econweb.ucsd.edu/~vramey/research/Century_Public_Data.xls ; update https://econweb.ucsd.edu/~vramey/research/Century_Update.xlsx** (Ramey and Francis (2009), 'A Century of Work and Leisure', AEJ: Macroeconomics 1(2)) — Average weekly hours per person (per capita, not per worker) of market work, school, home production and leisure, plus lifetime leisure by birth cohort.; Work: Males, Females and All x ages 10-13, 14-17, 18-24, 25-54, 55-64, 65+, 14+. Home production and leisure: sex x 14-17, 18-24, 25-54, 55-64, 65+. Update: market work and home production by sex for ages 25-54 and 18-64.; USA; Annual 1900-2005 (106 years). Update 1900-2012 (113 years). Lifetime leisure for cohorts born 1890-2000 (12 rows).
- **https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx (variables wage, cpi, housing_rent_yd, hpnom; rent index = housing_rent_yd x hpnom, as in participation/longrun)** (Jorda-Schularick-Taylor Macrohistory Database R6) — Nominal wage index, CPI, and the ingredients of an implied rent index (rental yield x house prices). This pairs w/p_rent with w/p_goods.; Country x year. No sex, age or sector.; 18: AUS BEL CAN CHE DEU DNK ESP FIN FRA GBR IRL ITA JPN NLD NOR PRT SWE USA. The rent yield covers 16 (no CAN, no IRL).; wage: 1870-2020 for 16 countries, ITA 1871-2020, IRL 1943-2020. Gaps: BEL 146 years, ESP 144, DEU 150. cpi: 1870-2020 (IRL from 1922). housing_rent_yd starts: DEU FRA NLD 1870, NOR 1871, DNK 1875, SWE 1883, BEL USA 1890, GBR 1895, ESP 1900, AUS CHE 1901, FIN 1920, ITA 1927, JPN 1931, PRT 1948; all end 2020. hpnom starts late for ESP (1971), ITA (1970) and PRT (1988); the project uses cumulated housing_capgain for those.
- **OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0** (OECD Data Explorer: average annual wages) — Average annual wages per full-time-equivalent dependent employee (national-accounts wage bill / FTE).; PRICE_BASE V (current prices) and Q (constant prices); national currency, USD and USD PPP. SEX _Z (no sex or age).; 42 areas: OECD members (no NLD gap; includes USA, JPN, KOR) plus BGR HRV ROU and OECD.; 1990-2025 for most (AUS AUT BEL CAN CHE DEU DNK ESP FIN FRA GBR IRL ITA JPN KOR LUX MEX NLD NOR NZL SWE USA). CZE EST GRC HUN LTU LVA POL PRT SVN 1995. CHL 1995/1996-2023, COL 2005-2024, TUR 1990 (constant prices) and 1998 (current prices) to 2024.
- **DBnomics AMECO/NLHA (average annual hours worked per person employed, total economy) and AMECO/HWCDW (nominal compensation per employee); e.g. USA.1.0.0.0.NLHA** (European Commission AMECO via DBnomics) — Annual hours per worker and compensation per employee, national accounts.; Country x year. No sex or age.; NLHA: 41 series (EU members, EU and EA aggregates, CAN CHE ISL JPN NOR USA, West Germany). HWCDW: 120 series, including AUS, CAN, USA, JPN.; NLHA: FRA 1960, DNK 1966, NLD 1969, BEL CAN CHE ESP FIN GBR IRL ISL ITA JPN LUX NOR PRT SWE USA 1970, West Germany 1970-1991, DEU 1991, GRC 1983, others 1990-1995. Ends 2027 (2024 for CAN), and the last years are Commission forecasts. HWCDW: from 1960 for many (AUS AUT BEL CAN DNK ESP FIN FRA GBR GRC IRL ...).