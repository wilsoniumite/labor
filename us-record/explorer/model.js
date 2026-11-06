// model.js — the backward model in JavaScript, for the explorer page (explorer/index.html): the pinning model
// (../../pinning/code/pinning_model.py) with the cap and the basket, run over the US record the way code/fit_base.py runs
// it, the misfit as fit_base.py scores it, and a small least-squares fitter for the page's "fit" button.
// checks/check_explorer.py holds this file to the Python model, to a relative 1e-9, on every stored fit.
// Plain functions; works in a browser (window.USRecordModel), a Web Worker (self.USRecordModel) and Node (require).

(function (root) {
  "use strict";

  const SET = { b: 0.4, g0: 0.01, g1: 0.99 };
  const SERIES = ["wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"];
  const TOL = { wage_goods: 0.05, wage_shelter: 0.05, labour_share_c: 0.01, prime_emp_rate: 0.015, theta_V: 0.02 };
  const BOUNDS = { T: [1e-5, 10], h: [1e-6, 1], a: [0.01, 10], k: [0.05, 60], chi_max: [0.3, 20], rho: [0, 0.3],
                   g_eta: [-0.05, 0.25], lam0: [0.01, 1000], g_lam: [-0.1, 0.1] };
  const LOGP = { T: 1, h: 1, a: 1, k: 1, chi_max: 1, lam0: 1 };   // searched in logs
  const NAMES = ["T", "h", "a", "k", "chi_max", "rho", "g_eta", "lam0", "g_lam"];
  const EPS4 = 4 * 2.220446049250313e-16;                           // scipy's brentq rtol

  // ---------------------------------------------------------------- scipy's brentq, line for line
  function brentq(f, xa, xb, xtol, rtol, maxiter) {
    rtol = rtol === undefined ? EPS4 : rtol;
    maxiter = maxiter === undefined ? 100 : maxiter;
    let xpre = xa, xcur = xb, xblk = 0, fblk = 0, spre = 0, scur = 0;
    let fpre = f(xpre), fcur = f(xcur);
    if (!(isFinite(fpre) && isFinite(fcur))) throw new Error("brentq: not finite at the bracket");
    if (fpre === 0) return xpre;
    if (fcur === 0) return xcur;
    if ((fpre < 0) === (fcur < 0)) throw new Error("brentq: no sign change");
    for (let i = 0; i < maxiter; i++) {
      if (fpre !== 0 && fcur !== 0 && ((fpre < 0) !== (fcur < 0))) {
        xblk = xpre; fblk = fpre; spre = scur = xcur - xpre;
      }
      if (Math.abs(fblk) < Math.abs(fcur)) {
        xpre = xcur; xcur = xblk; xblk = xpre;
        fpre = fcur; fcur = fblk; fblk = fpre;
      }
      const delta = (xtol + rtol * Math.abs(xcur)) / 2;
      const sbis = (xblk - xcur) / 2;
      if (fcur === 0 || Math.abs(sbis) < delta) return xcur;
      if (Math.abs(spre) > delta && Math.abs(fcur) < Math.abs(fpre)) {
        let stry;
        if (xpre === xblk) {
          stry = -fcur * (xcur - xpre) / (fcur - fpre);
        } else {
          const dpre = (fpre - fcur) / (xpre - xcur);
          const dblk = (fblk - fcur) / (xblk - xcur);
          stry = -fcur * (fblk * dblk - fpre * dpre) / (dblk * dpre * (fblk - fpre));
        }
        if (2 * Math.abs(stry) < Math.min(Math.abs(spre), 3 * Math.abs(sbis) - delta)) {
          spre = scur; scur = stry;
        } else {
          spre = sbis; scur = sbis;
        }
      } else {
        spre = sbis; scur = sbis;
      }
      xpre = xcur; fpre = fcur;
      xcur += Math.abs(scur) > delta ? scur : (sbis > 0 ? delta : -delta);
      fcur = f(xcur);
      if (!isFinite(fcur)) throw new Error("brentq: not finite");
    }
    return xcur;
  }

  // ---------------------------------------------------------------- the economy (pinning_model.py)
  // e: {N, T, h, a, b, lam, g0, g1, k, eta, chi_max, rho, delta, cap, sigma (null: the fixed basket), p_ref, utility}
  function gamma(e, x) { return e.eta * (e.g0 + e.g1 * Math.pow(x, e.k)); }
  function Jint(e, x) { return e.eta * (e.g0 * x + e.g1 * Math.pow(x, e.k + 1) / (e.k + 1)); }

  function basket(e, p) {
    if (e.sigma === null || e.sigma === undefined) return [1, e.h];
    let th = e.p_ref / (e.p_ref + e.h), ts = e.h / (e.p_ref + e.h);
    if (e.tilt !== undefined && e.tilt !== 1) { ts = ts * e.tilt; th = 1 - ts; }
    const r = p / e.p_ref;
    let Ps, thp, tsp;
    if (e.sigma === 1) {
      Ps = (e.p_ref + e.h) * Math.pow(r, th); thp = th; tsp = ts;
    } else {
      const m = th * Math.pow(r, 1 - e.sigma) + ts;
      Ps = (e.p_ref + e.h) * Math.pow(m, 1 / (1 - e.sigma));
      thp = th * Math.pow(r, 1 - e.sigma) / m; tsp = ts / m;
    }
    return [e.utility * thp * Ps / p, e.utility * tsp * Ps];
  }

  function parts(e, x) {
    const g = gamma(e, x), J = Jint(e, x);
    const cpt = e.rho + e.delta;
    if (e.thetaV !== undefined) e = Object.assign({}, e, { lam: e.thetaV / (g * cpt) });   // lambda from the record's theta_V
    const den = 1 - cpt * (e.a + e.lam * g);
    const Vm = e.b / den, pm = cpt * Vm, v = g * pm;
    const p = v * (1 - x) + pm * J;
    const gs = basket(e, p), gb = gs[0], sb = gs[1];
    const Ps = p * gb + sb;
    const B = e.T / (sb + gb * e.b * e.delta * J / (1 - e.a * e.delta));
    const Y = gb * B;
    const K = Y * J / (1 - e.a * e.delta);
    const final = Y * (1 - x), mh = e.lam * e.delta * K;
    const z = Math.log1p(v / Ps);
    const nS = e.N * Math.min(Math.max(z / e.chi_max, 0), e.cap);
    return { x, gamma: g, J, v, pm, Vm, p, Ps, B, Y, K, final, mh, nD: final + mh, nS, gb, sb };
  }

  function xCeiling(e) {
    const cpt = e.rho + e.delta;
    if (e.thetaV !== undefined) {                 // with theta_V given, a machine's cost is finite at every task or none
      if (1 - cpt * e.a - e.thetaV > 0) return 1;
      throw new Error("no equilibrium: machine services and labour take the whole of a machine's cost");
    }
    const g = (x) => 1 - cpt * (e.a + e.lam * gamma(e, x));
    const g1 = g(1);
    if (g1 > 0) return 1;
    const g0 = g(0);
    if (g0 <= 0) throw new Error("no equilibrium: machine-service cost undefined at x = 0");
    if (g1 === 0) return brentq((x) => g(x) - 1e-9 * g0, 0, 1, 1e-15);
    return brentq(g, 0, 1, 1e-15);
  }

  function solve(e) {
    const xb = xCeiling(e);
    const f = (x) => { const q = parts(e, x); return q.nD - q.nS; };
    const lo = 1e-12;
    let hi = xb >= 1 ? 1 : xb * (1 - 1e-13);
    if (hi < 1) {
      const den = (x) => 1 - (e.rho + e.delta) * (e.a + e.lam * gamma(e, x));
      let j = 0;
      while (den(hi) <= 0) {
        j += 1;
        if (j > 40) throw new Error("no equilibrium: cost not finite below the ceiling");
        hi = xb * (1 - 1e-13 * Math.pow(2, j));
      }
    }
    const flo = f(lo), fhi = f(hi);
    if (!(flo > 0) || !(fhi < 0)) throw new Error("no interior equilibrium");
    const x = brentq(f, lo, hi, 1e-15);
    const q = parts(e, x);
    q.n = q.nD;
    q.participation = q.n / e.N;
    q.income = q.v * q.n + e.T + e.rho * q.Vm * q.K;
    q.theta_V = (e.thetaV !== undefined ? e.thetaV / (q.gamma * (e.rho + e.delta)) : e.lam) * q.v / q.Vm;
    q.labour_share_bea = q.v * q.final / q.income;
    q.labour_share_traced = q.v * q.n / q.income;            // all labour, the machine chain's included
    return q;
  }

  // ---------------------------------------------------------------- the record (fit_base.py)
  // D: {years, N (adults, 1950 = 1), delta, data series..., ls_tol, real_wage_cpi}
  // S: {cap: null|share, sigma: null|elasticity, utility: [[year, level], ...] (1950 at 1), pin: bool,
  //     shelterW: null|site share (A), clock: null (steady, par.g_eta) or [[year, log eta], ...] (1950 at 0)}
  function interp(x, xs, ys) {                  // numpy.interp: flat beyond the ends
    if (x <= xs[0]) return ys[0];
    const n = xs.length;
    if (x >= xs[n - 1]) return ys[n - 1];
    let j = 1;
    while (xs[j] < x) j++;
    return ys[j - 1] + (x - xs[j - 1]) * (ys[j] - ys[j - 1]) / (xs[j] - xs[j - 1]);
  }

  function etaPath(par, S, D) {
    if (S.clock && S.clock.length) {
      const xs = S.clock.map((k) => k[0]), ys = S.clock.map((k) => k[1]);
      return D.years.map((y) => Math.exp(interp(y, xs, ys)));
    }
    return D.years.map((y) => Math.exp(-par.g_eta * (y - 1950)));
  }

  function utilityPath(S, D) {
    const xs = S.utility.map((k) => k[0]), ys = S.utility.map((k) => Math.log(k[1]));
    return D.years.map((y) => Math.exp(interp(y, xs, ys)));
  }

  function thetaVPath(D) {                      // the record's theta_V, straight between measured years, flat beyond
    const xs = [], ys = [];
    D.years.forEach((y, i) => { if (D.theta_V[i] !== null && isFinite(D.theta_V[i])) { xs.push(y); ys.push(D.theta_V[i]); } });
    return D.years.map((y) => interp(y, xs, ys));
  }

  function knotMul(knots, D) {                  // optional paths in logs through [year, log multiplier] knots, 1 if none
    if (!knots || !knots.length) return null;
    const xs = knots.map((k) => k[0]), ys = knots.map((k) => k[1]);
    return D.years.map((y) => Math.exp(interp(y, xs, ys)));
  }

  function economies(par, S, D, pRef) {
    const eta = etaPath(par, S, D);
    const util = S.sigma !== null && S.sigma !== undefined && pRef !== undefined && pRef !== null ? utilityPath(S, D) : null;
    // Optional paths, off unless set (the page does not set them; the playground does): land, the cost of working and the
    // machine chain's labour through knots, and the required return following the measured real rate.
    const land = knotMul(S.land, D), chi = knotMul(S.chi, D), lamk = knotMul(S.lamk, D), tilt = knotMul(S.tilt, D);
    const bk = knotMul(S.bk, D);                // land in a machine through knots (1950 = the unit b)
    const out = [];
    for (let i = 0; i < D.years.length; i++) {
      const t = D.years[i] - 1950;
      const lam = lamk ? par.lam0 * lamk[i] : par.lam0 * Math.exp(par.g_lam * t);
      const rho = S.rhoData ? par.rho + S.rhoData * D.real_rate[i] : par.rho;
      const e = { N: D.N[i], T: par.T * (land ? land[i] : 1), h: par.h, a: par.a, b: SET.b * (bk ? bk[i] : 1), lam,
                  g0: SET.g0, g1: SET.g1, k: par.k, eta: eta[i], chi_max: par.chi_max * (chi ? chi[i] : 1), rho,
                  delta: D.delta[i], cap: S.cap === null || S.cap === undefined ? 1 : S.cap, sigma: null };
      if (util) { e.sigma = S.sigma; e.p_ref = pRef; e.utility = util[i]; if (tilt) e.tilt = tilt[i]; }
      if (S.thetaVData) e.thetaV = thetaVPath(D)[i];
      out.push(e);
    }
    return out;
  }

  function linspace(a, b, n) {
    const out = [], step = (b - a) / (n - 1);
    for (let i = 0; i < n; i++) out.push(a + i * step);
    out[n - 1] = b;
    return out;
  }

  function pinnedChi(par, S, D) {
    const e0 = economies(Object.assign({}, par, { chi_max: 1 }), S, D)[0];
    const target = D.prime_emp_rate[0];
    const gap = (lc) => {
      try { return solve(Object.assign({}, e0, { chi_max: Math.exp(lc) })).participation - target; }
      catch (err) { return NaN; }
    };
    const grid = linspace(Math.log(BOUNDS.chi_max[0]), Math.log(BOUNDS.chi_max[1]), 25);
    const vals = grid.map(gap);
    for (let j = 0; j < grid.length - 1; j++) {
      if (isFinite(vals[j]) && isFinite(vals[j + 1]) && vals[j] * vals[j + 1] < 0) {
        return Math.exp(brentq(gap, grid[j], grid[j + 1], 1e-14));
      }
    }
    return null;
  }

  // Each year's equilibrium read as the targets; null if any year has no equilibrium (with the year).
  function pinnedK(par, S, D) {                  // k at which 1950's labour share is the record's (the start pinned)
    const target = D.labour_share_c[0];
    const gap = (lk) => {
      try {
        let p = Object.assign({}, par, { k: Math.exp(lk) });
        if (S.pin) { const chi = pinnedChi(p, S, D); if (chi === null) return NaN; p.chi_max = chi; }
        const e0 = economies(p, S, D)[0];
        const q = solve(e0);
        return (S.lsBasis === "traced" ? q.v * q.n / q.income : q.labour_share_bea) - target;
      } catch (err) { return NaN; }
    };
    const grid = linspace(Math.log(BOUNDS.k[0]), Math.log(BOUNDS.k[1]), 25), vals = grid.map(gap);
    for (let j = 0; j < grid.length - 1; j++) {
      if (isFinite(vals[j]) && isFinite(vals[j + 1]) && vals[j] * vals[j + 1] < 0) return Math.exp(brentq(gap, grid[j], grid[j + 1], 1e-12));
    }
    return null;
  }

  function path(par0, S, D) {
    let par = par0;
    if (S.pinLS) {
      const k = pinnedK(par, S, D);
      if (k === null) return { ok: false, why: "no steepness gives 1950's labour share" };
      par = Object.assign({}, par, { k });
    }
    if (S.pin) {
      const chi = pinnedChi(par, S, D);
      if (chi === null) return { ok: false, why: "no work-cost scale gives 1950's employment" };
      par = Object.assign({}, par, { chi_max: chi });
    }
    let pRef = null;
    if (S.sigma !== null && S.sigma !== undefined) {
      try { pRef = solve(economies(par, S, D)[0]).p; }
      catch (err) { return { ok: false, why: "no equilibrium in 1950" }; }
    }
    const es = economies(par, S, D, pRef);
    const cols = { x: [], v: [], p: [], Ps: [], wg: [], ws: [], labour_share_c: [], prime_emp_rate: [], theta_V: [],
                   goods_basket: [], site_basket: [], eta: [], utility: [] };
    const an = { pm: [], kappaV: [], sigmaV: [], landHomes: [], landMachines: [], hoursFinal: [], hoursMachine: [],
                 goodsShare: [], siteShare: [], wageGoodsLevel: [], peopleTasks: [], lam: [], b: [], xCeil: [] };
    for (let i = 0; i < es.length; i++) {
      let q;
      try { q = solve(es[i]); } catch (err) { return { ok: false, why: "no equilibrium in " + D.years[i], year: D.years[i] }; }
      if (!isFinite(q.v) || !isFinite(q.p)) return { ok: false, why: "no equilibrium in " + D.years[i], year: D.years[i] };
      cols.x.push(q.x); cols.v.push(q.v); cols.p.push(q.p); cols.Ps.push(q.Ps);
      cols.wg.push(q.v / q.p); cols.ws.push(q.v);
      cols.labour_share_c.push(S.lsBasis === "traced" ? q.labour_share_traced : q.labour_share_bea);
      cols.prime_emp_rate.push(q.participation);
      cols.theta_V.push(q.theta_V); cols.goods_basket.push(q.gb); cols.site_basket.push(q.sb);
      cols.eta.push(es[i].eta); cols.utility.push(es[i].utility === undefined ? 1 : es[i].utility);
      const e = es[i];
      an.pm.push(q.pm); an.kappaV.push(e.a * q.pm / q.Vm); an.sigmaV.push(e.b / q.Vm);
      an.lam.push(e.thetaV !== undefined ? e.thetaV / (q.gamma * (e.rho + e.delta)) : e.lam); an.b.push(e.b);
      an.landHomes.push(q.sb * q.B / e.T); an.landMachines.push(e.b * e.delta * q.K / e.T);
      an.hoursFinal.push(q.final / q.n); an.hoursMachine.push(q.mh / q.n);
      an.goodsShare.push(q.p * q.gb / q.Ps); an.siteShare.push(q.sb / q.Ps);
      an.wageGoodsLevel.push(q.v / q.p); an.peopleTasks.push(1 - q.x);
      let xc = null; try { xc = xCeiling(e); } catch (err) { xc = null; }
      an.xCeil.push(xc);
    }
    cols.an = an;
    if (S.shelterW !== null && S.shelterW !== undefined) {      // addition A: shelter is building and site
      const w = S.shelterW, pl = cols.p[cols.p.length - 1], vl = cols.v[cols.v.length - 1];
      cols.ws = S.shelterBuild === "wage"                         // the building priced like construction: at the wage
        ? cols.v.map((v) => v / (w + (1 - w) * v / vl))
        : cols.v.map((v, i) => v / (w + (1 - w) * cols.p[i] / pl));
    }
    cols.wage_goods = cols.wg.map((x) => 100 * x / cols.wg[0]);
    cols.wage_shelter = cols.ws.map((x) => 100 * x / cols.ws[0]);
    cols.ok = true;
    cols.chi_max = par.chi_max;
    cols.k = par.k;
    return cols;
  }

  // ---------------------------------------------------------------- the misfit (fit_base.py)
  function deviations(m, D) {
    const out = {};
    for (const s of SERIES) {
      out[s] = D[s].map((y, i) => {
        if (y === null || y === undefined || !isFinite(y)) return NaN;
        const f = m[s][i];
        if (s === "wage_goods" || s === "wage_shelter") return (Math.log(f) - Math.log(y)) / TOL[s];
        if (s === "labour_share_c") return (f - y) / D.ls_tol[i];
        return (f - y) / TOL[s];
      });
    }
    return out;
  }

  function misfit(m, D) {
    const dev = deviations(m, D), by = {};
    let tot = 0;
    for (const s of SERIES) {
      let sum = 0, n = 0;
      for (const d of dev[s]) if (isFinite(d)) { sum += d * d; n += 1; }
      by[s] = sum / n; tot += by[s];
    }
    return { total: tot / SERIES.length, by };
  }

  function nObs(D) {
    const out = {};
    for (const s of SERIES) out[s] = D[s].filter((y) => y !== null && y !== undefined && isFinite(y)).length;
    return out;
  }

  function residuals(par, S, D, N_OBS) {
    const m = path(par, S, D);
    const out = [];
    if (!m.ok) {
      for (const s of SERIES) for (let j = 0; j < N_OBS[s]; j++) out.push(10);
      return out;
    }
    const dev = deviations(m, D);
    for (const s of SERIES) {
      const w = 1 / Math.sqrt(N_OBS[s] * SERIES.length);
      for (const d of dev[s]) if (isFinite(d)) out.push(d * w);
    }
    return out;
  }

  // ---------------------------------------------------------------- coordinates (her ask, 2026-11-06)
  // Some numbers come in linked groups, and each group can be set in more than one way: land as (T, h) or as T and a
  // basket's land over land per adult (hT = h / T); machine services as a or as their share of a machine's cost in 1950
  // (kappa50 = (rho + delta_1950) a, so a follows the return); the hours to build a machine growing per machine (g_lam) or per
  // fixed task (g_lamTask = g_lam - g_eta). The dials and the fitter work in the chosen ones; the others follow.
  // COORD: [low, high, searched in logs]
  const COORD = { T: [1e-5, 10, true], h: [1e-6, 1, true], hT: [1e-4, 100, true], a: [0.01, 10, true],
                  kappa50: [0.001, 0.99, false], rho: [0, 0.3, false], k: [0.05, 60, true], chi_max: [0.3, 20, true],
                  g_eta: [-0.05, 0.25, false], lam0: [0.01, 1000, true], g_lam: [-0.1, 0.1, false],
                  g_lamTask: [-0.35, 0.2, false] };
  const DEFAULT_SYS = { land: "Th", machine: "a", labour: "lam" };
  function toCoords(par, D) {
    return { T: par.T, h: par.h, hT: par.h / par.T, a: par.a, kappa50: (par.rho + D.delta[0]) * par.a, rho: par.rho,
             k: par.k, chi_max: par.chi_max, g_eta: par.g_eta, lam0: par.lam0, g_lam: par.g_lam,
             g_lamTask: par.g_lam - par.g_eta };
  }
  function fromCoords(c, sys, D) {
    sys = Object.assign({}, DEFAULT_SYS, sys || {});
    return { T: c.T, h: sys.land === "TS" ? c.hT * c.T : c.h,
             a: sys.machine === "kappa" ? c.kappa50 / (c.rho + D.delta[0]) : c.a, rho: c.rho, k: c.k, chi_max: c.chi_max,
             g_eta: c.g_eta, lam0: c.lam0, g_lam: sys.labour === "task" ? c.g_lamTask + c.g_eta : c.g_lam };
  }
  const KNOT_KEYS = ["clock", "land", "chi", "lamk", "tilt", "bk", "utility"];

  // ---------------------------------------------------------------- a small fitter (Levenberg-Marquardt, in bounds)
  // free: names from NAMES (not chi_max when pinned), plus "clock:<i>" for the knots of a bent clock (log eta at knot i).
  // free: coordinate names (COORD), and knots of a path in S: "key:i" its level, "key:i:y" its year (utility levels are
  // levels, searched in logs; every other path's levels are logs already).
  function fit(par0, S0, D, free, opts) {
    opts = opts || {};
    const N_OBS = nObs(D);
    const maxIter = opts.maxIter || 300;
    const onStep = opts.onStep || (() => {});
    const sys = Object.assign({}, DEFAULT_SYS, S0.coords || {});
    const c0 = toCoords(par0, D);
    const isKnot = (n) => n.indexOf(":") > 0;
    const parse = (n) => { const q = n.split(":"); return { key: q[0], i: +q[1], year: q[2] === "y" }; };
    const getK = (S, n) => { const k = parse(n), kn = S[k.key][k.i]; return k.year ? kn[0] : (k.key === "utility" ? Math.log(kn[1]) : kn[1]); };
    const putK = (S, n, v) => { const k = parse(n), kn = S[k.key][k.i]; if (k.year) kn[0] = v; else kn[1] = k.key === "utility" ? Math.exp(v) : v; };
    const bounds = free.map((n) => {
      if (!isKnot(n)) { const b = COORD[n]; return b[2] ? [Math.log(b[0]), Math.log(b[1])] : [b[0], b[1]]; }
      const k = parse(n);
      if (!k.year) return k.key === "clock" ? [-25, 5] : (k.key === "utility" ? [Math.log(0.2), Math.log(5)] : [-6, 6]);
      const arr = S0[k.key], here = arr[k.i][0], prev = arr[k.i - 1][0], last = k.i === arr.length - 1;
      const lo = free.includes(`${k.key}:${k.i - 1}:y`) ? (prev + here) / 2 : prev + 0.5;
      const hi = last ? 2024 : (free.includes(`${k.key}:${k.i + 1}:y`) ? (arr[k.i + 1][0] + here) / 2 : arr[k.i + 1][0] - 0.5);
      return [lo, hi];
    });
    const lo = bounds.map((b) => b[0]), hi = bounds.map((b) => b[1]);
    const toU = (n, v) => (!isKnot(n) && COORD[n][2] ? Math.log(v) : v);
    const fromU = (n, u) => (!isKnot(n) && COORD[n][2] ? Math.exp(u) : u);
    const clamp = (u) => u.map((x, j) => Math.min(Math.max(x, lo[j]), hi[j]));
    const copyS = (S) => {
      const out = Object.assign({}, S);
      for (const key of KNOT_KEYS) if (S[key]) out[key] = S[key].map((k) => k.slice());
      return out;
    };
    const unpack = (u) => {
      const c = Object.assign({}, c0), S = copyS(S0);
      free.forEach((n, j) => { if (isKnot(n)) putK(S, n, u[j]); else c[n] = fromU(n, u[j]); });
      return { par: Object.assign({}, par0, fromCoords(c, sys, D)), S };
    };
    const cost = (r) => r.reduce((a, x) => a + x * x, 0);
    let u = clamp(free.map((n) => (isKnot(n) ? getK(S0, n) : toU(n, c0[n]))));
    let cur = unpack(u), r = residuals(cur.par, cur.S, D, N_OBS), c = cost(r);
    let mu = 1e-3, quiet = 0, it = 0;
    for (it = 0; it < maxIter; it++) {
      const nF = u.length, nR = r.length;
      const Jm = [];
      for (let j = 0; j < nF; j++) {
        let step = 1e-6 * Math.max(1, Math.abs(u[j]));
        if (u[j] + step > hi[j]) step = -step;
        const u2 = u.slice(); u2[j] += step;
        const t = unpack(u2), r2 = residuals(t.par, t.S, D, N_OBS);
        Jm.push(r2.map((x, i) => (x - r[i]) / step));
      }
      const A = [], g = [];
      for (let a = 0; a < nF; a++) {
        A.push([]);
        let ga = 0;
        for (let i = 0; i < nR; i++) ga += Jm[a][i] * r[i];
        g.push(ga);
        for (let b = 0; b < nF; b++) {
          let sum = 0;
          for (let i = 0; i < nR; i++) sum += Jm[a][i] * Jm[b][i];
          A[a].push(sum);
        }
      }
      let accepted = false;
      for (let tries = 0; tries < 12 && !accepted; tries++) {
        const M = A.map((row, a) => row.map((x, b) => (a === b ? x * (1 + mu) + 1e-12 : x)));
        const step = solveLinear(M, g.map((x) => -x));
        if (!step) { mu *= 10; continue; }
        const u2 = clamp(u.map((x, j) => x + step[j]));
        const t = unpack(u2), r2 = residuals(t.par, t.S, D, N_OBS), c2 = cost(r2);
        if (c2 < c) {
          const rel = (c - c2) / c;
          u = u2; r = r2; cur = t; mu = Math.max(mu / 3, 1e-9); accepted = true;
          quiet = rel < 1e-10 ? quiet + 1 : 0;
          c = c2;
        } else {
          mu *= 4;
        }
      }
      onStep({ iter: it + 1, misfit: c, par: cur.par, S: cur.S });
      if (!accepted || quiet >= 3) break;
    }
    return { par: cur.par, S: cur.S, misfit: c, iters: it + 1 };
  }

  function solveLinear(A, b) {                  // Gaussian elimination with partial pivoting
    const n = b.length, M = A.map((row, i) => row.slice().concat([b[i]]));
    for (let c = 0; c < n; c++) {
      let piv = c;
      for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[piv][c])) piv = r;
      if (!(Math.abs(M[piv][c]) > 1e-300)) return null;
      [M[c], M[piv]] = [M[piv], M[c]];
      for (let r = c + 1; r < n; r++) {
        const f = M[r][c] / M[c][c];
        for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
      }
    }
    const x = new Array(n).fill(0);
    for (let r = n - 1; r >= 0; r--) {
      let s = M[r][n];
      for (let k = r + 1; k < n; k++) s -= M[r][k] * x[k];
      x[r] = s / M[r][r];
    }
    return x.every(isFinite) ? x : null;
  }

  const api = { SET, SERIES, TOL, BOUNDS, LOGP, NAMES, COORD, DEFAULT_SYS, KNOT_KEYS, brentq, gamma, parts, basket, solve,
                xCeiling, economies, pinnedChi, path, deviations, misfit, residuals, nObs, fit, interp, utilityPath, etaPath,
                toCoords, fromCoords, knotMul };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.USRecordModel = api;
})(typeof self !== "undefined" ? self : this);
