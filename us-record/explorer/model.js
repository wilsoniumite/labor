// model.js — the backward model in JavaScript, for the explorer page (explorer/index.html): the pinning model
// (../../pinning/code/pinning_model.py) with the cap and the basket, and (v5, 2026-11-08) the goods model of
// code/two_goods.py (durables apart, services apart, the value-share rent, land growing with adults; v6, the skill split
// and a worker for each good), run over the US record
// the way code/fit_base.py runs it, the misfit as fit_base.py scores it, and a small least-squares fitter for the page.
// checks/check_explorer.py holds this file to the Python model, to a relative 1e-9, on every stored fit.
// Plain functions; works in a browser (window.USRecordModel), a Web Worker (self.USRecordModel) and Node (require).

(function (root) {
  "use strict";

  const SET = { b: 0.4, g0: 0.01, g1: 0.99 };
  const SERIES = ["wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"];
  const TOL = { wage_goods: 0.05, wage_shelter: 0.05, labour_share_c: 0.01, prime_emp_rate: 0.015, theta_V: 0.02 };
  // the goods model's further targets (durables apart, services apart), scored as the other wages: fit_base.EXTRA_TOL_LOG
  const EXTRA_TOL = { wage_durables: 0.05, wage_services: 0.05, wage_nondurables: 0.05, wage_ndg: 0.05, wage_low: 0.05,
                      wage_high: 0.05 };
  const seriesOf = (extra) => SERIES.concat(extra || []);
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

  // How far an economy is from having an interior equilibrium, in [0, 1): the relative excess of labour demand over
  // supply at the end of the task range where they fail to cross (0 if they cross). Guides the start search only.
  function gapMeasure(e) {
    let xb;
    try { xb = xCeiling(e); } catch (err) { return 0.99; }
    const hi = xb >= 1 ? 1 : xb * (1 - 1e-9);
    try {
      const a = parts(e, 1e-12), b = parts(e, hi);
      const fl = (a.nD - a.nS) / Math.max(a.nS, 1e-12), fh = (b.nD - b.nS) / Math.max(b.nS, 1e-12);
      let g = 0;
      if (!(fl > 0)) g = isFinite(fl) ? -fl : 1;
      else if (!(fh < 0)) g = isFinite(fh) ? fh : 1;
      return g / (1 + g);
    } catch (err) { return 0.99; }
  }


  // ---------------------------------------------------------------- the goods economy (code/two_goods.py)
  // Durables apart, and services apart: two or three final goods made by one kind of machine, one wage and one land
  // market, one equation in the common margin m = v / p_m. Each function is its Python twin's, line for line.
  // e as above; etaD, etaS: durables' and services' clocks; cmp: {omega_d, sigma_dg, pref_d, pref_g, phi, omega_s, pref_n,
  // pref_s} or {mode: "ref", omega_d, phi, omega_s} in 1950.
  function xOf(m, eta, e) {
    const r = (m / eta - e.g0) / e.g1;
    if (r <= 0) return 0;
    if (r >= 1) return 1;
    return Math.pow(r, 1 / e.k);
  }
  function JOf(x, eta, e) { return eta * (e.g0 * x + e.g1 * Math.pow(x, e.k + 1) / (e.k + 1)); }

  function composite(pd, pg, cmp) {                // the goods' CES composite, its unit cost the other goods' at 1950's prices
    const w = cmp.omega_d;
    if (cmp.mode === "ref") { const c = pg; return [c, w * c / pd, (1 - w) * c / pg]; }
    const s = cmp.sigma_dg, rd = cmp.pref_d, rg = cmp.pref_g;
    if (Math.abs(s - 1) < 1e-12) {
      const c = rg * Math.pow(pd / rd, w) * Math.pow(pg / rg, 1 - w);
      return [c, w * c / pd, (1 - w) * c / pg];
    }
    const ad = w * Math.pow(rg / rd, 1 - s), ag = 1 - w;
    const c = Math.pow(ad * Math.pow(pd, 1 - s) + ag * Math.pow(pg, 1 - s), 1 / (1 - s));
    return [c, ad * Math.pow(pd / c, -s), ag * Math.pow(pg / c, -s)];
  }

  function restNest(pn, ps, cmp) {                 // services apart: nondurables and services, services' share the record's
    const w = cmp.omega_s;
    let c;
    if (cmp.mode === "ref") c = pn;
    else { const rn = cmp.pref_n, rs = cmp.pref_s; c = rn * Math.pow(pn / rn, 1 - w) * Math.pow(ps / rs, w); }
    return [c, (1 - w) * c / pn, w * c / ps];
  }

  function restSkill(pn, pl, ph, cmp) {           // the skill split: nondurables, low- and high-skill services, shares the record's
    const wl = cmp.omega_l, wh = cmp.omega_h, wn = 1 - wl - wh;
    let c;
    if (cmp.mode === "ref") c = pn;
    else { const rn = cmp.pref_n, rl = cmp.pref_l, rh = cmp.pref_h;
      c = rn * Math.pow(pn / rn, wn) * Math.pow(pl / rl, wl) * Math.pow(ph / rh, wh); }
    return [c, wn * c / pn, wl * c / pl, wh * c / ph];
  }

  const r1 = (x) => (x === undefined || x === null ? 1 : x);   // a good's pay over the production wage (1: one wage)
  function partsG(e, m, etaD, cmp, etaS) {
    const cpt = e.rho + e.delta, phi = cmp.phi || 0;
    const den = 1 - phi - cpt * (e.a + e.lam * m);
    const Vm = e.b / den, pm = cpt * Vm, v = m * pm;
    const rd = r1(cmp.r_d), rg = r1(cmp.r_n);
    const xg = xOf(rg * m, e.eta, e), xd = xOf(rd * m, etaD, e);
    const Jg = JOf(xg, e.eta, e), Jd = JOf(xd, etaD, e);
    const pg = rg * v * (1 - xg) + pm * Jg, pd = rd * v * (1 - xd) + pm * Jd;
    let prest, Jrest, Lrest, Wrest, extra = {};
    if (etaS === null || etaS === undefined) { prest = pg; Jrest = Jg; Lrest = 1 - xg; Wrest = rg * (1 - xg); }
    else if (!Array.isArray(etaS)) {
      const rs = r1(cmp.r_s);
      const xs = xOf(rs * m, etaS, e), Js = JOf(xs, etaS, e), ps = rs * v * (1 - xs) + pm * Js;
      const r = restNest(pg, ps, cmp), dn = r[1], ds = r[2];
      prest = r[0]; Jrest = dn * Jg + ds * Js; Lrest = dn * (1 - xg) + ds * (1 - xs);
      Wrest = dn * rg * (1 - xg) + ds * rs * (1 - xs);
      extra = { xs, Js, ps, dn, ds, prest };
    } else {
      const etaL = etaS[0], etaH = etaS[1], rl = r1(cmp.r_l), rh = r1(cmp.r_h);
      const xl = xOf(rl * m, etaL, e), xh = xOf(rh * m, etaH, e);
      const Jl = JOf(xl, etaL, e), Jh = JOf(xh, etaH, e);
      const pl = rl * v * (1 - xl) + pm * Jl, ph = rh * v * (1 - xh) + pm * Jh;
      const r = restSkill(pg, pl, ph, cmp), dn = r[1], dl = r[2], dh = r[3];
      prest = r[0];
      Jrest = dn * Jg + dl * Jl + dh * Jh;
      Lrest = dn * (1 - xg) + dl * (1 - xl) + dh * (1 - xh);
      Wrest = dn * rg * (1 - xg) + dl * rl * (1 - xl) + dh * rh * (1 - xh);
      extra = { xl, xh, Jl, Jh, pl, ph, dn, dl, dh, prest };
    }
    const cc = composite(pd, prest, cmp), c = cc[0], dd = cc[1], dg = cc[2];
    const gs = basket(e, c), gb = gs[0], sb = gs[1];
    const Ps = c * gb + sb;
    const Jmix = dd * Jd + dg * Jrest;
    const B = e.T / (sb + gb * e.b * e.delta * Jmix / (1 - e.a * e.delta));
    const K = B * gb * Jmix / (1 - e.a * e.delta);
    const final = B * gb * (dd * (1 - xd) + dg * Lrest);
    const final_w = B * gb * (dd * rd * (1 - xd) + dg * Wrest);   // final labour's pay, in production wages
    const mh = e.lam * e.delta * K;
    const z = Math.log1p(v / Ps);
    const nS = e.N * Math.min(Math.max(z / e.chi_max, 0), e.cap);
    return Object.assign({ m, xg, xd, Jg, Jd, v, pm, Vm, pg, pd, c, dd, dg, gb, sb, Ps, B, K, final, final_w, mh, nD: final + mh, nS,
                           rd, rg }, extra);
  }

  function mCeiling(e, phi) {
    const cpt = e.rho + e.delta;
    if (phi + cpt * e.a >= 1) throw new Error("no equilibrium: machine-service cost undefined even with no labour in the chain");
    return e.lam <= 0 ? Infinity : ((1 - phi) / cpt - e.a) / e.lam;
  }

  function solveG(e, etaD, cmp, etaS) {
    const phi = cmp.phi || 0, hasS = etaS !== null && etaS !== undefined, skill = hasS && Array.isArray(etaS);
    const mbar = mCeiling(e, phi);
    const rd = r1(cmp.r_d), rg = r1(cmp.r_n);
    let top = Math.max(e.eta / rg, etaD / rd) * (e.g0 + e.g1);
    if (hasS && !skill) top = Math.max(top, etaS / r1(cmp.r_s) * (e.g0 + e.g1));
    else if (skill) top = Math.max(top, etaS[0] / r1(cmp.r_l) * (e.g0 + e.g1), etaS[1] / r1(cmp.r_h) * (e.g0 + e.g1));
    const hi = isFinite(mbar) ? Math.min(mbar * (1 - 1e-13), top) : top;
    const lo = 1e-12 * hi;
    const f = (m) => { const q = partsG(e, m, etaD, cmp, etaS); return q.nD - q.nS; };
    const flo = f(lo), fhi = f(hi);
    if (!(flo > 0 && fhi < 0)) throw new Error("no interior equilibrium");
    const m = brentq(f, lo, hi, 1e-15 * hi, 1e-15);
    const q = partsG(e, m, etaD, cmp, etaS);
    const n = q.nD, interest = e.rho * q.Vm * q.K, rent = phi * q.Vm * e.delta * q.K;
    const income = q.v * (q.final_w + q.mh) + e.T + interest + rent;   // each good's workers at their own pay
    Object.assign(q, { n, participation: n / e.N, income, labour_share_bea: q.v * q.final_w / income, theta_V: e.lam * q.v / q.Vm,
      kappa_V: e.a * q.pm / q.Vm, sigma_V: e.b / q.Vm, phi, fixed_rents: phi + e.b / q.Vm, rent_income: rent / income,
      chain_share: q.mh / n, inv_income: e.delta * q.Vm * q.K / income, m_ceiling: mbar,
      xg_ceiling: isFinite(mbar) ? xOf(rg * mbar, e.eta, e) : 1, xd_ceiling: isFinite(mbar) ? xOf(rd * mbar, etaD, e) : 1,
      dur_share: q.pd * q.dd / q.c, interest_income: interest / income, land_income: e.T / income });
    if (hasS && !skill) Object.assign(q, { xs_ceiling: isFinite(mbar) ? xOf(r1(cmp.r_s) * mbar, etaS, e) : 1,
                                           srv_share: q.ps * q.ds * q.dg / q.c, nd_share: q.pg * q.dn * q.dg / q.c });
    else if (skill) {
      const rl = r1(cmp.r_l), rh = r1(cmp.r_h);
      Object.assign(q, { xl_ceiling: isFinite(mbar) ? xOf(rl * mbar, etaS[0], e) : 1, xh_ceiling: isFinite(mbar) ? xOf(rh * mbar, etaS[1], e) : 1,
                         low_share: q.pl * q.dl * q.dg / q.c, high_share: q.ph * q.dh * q.dg / q.c, nd_share: q.pg * q.dn * q.dg / q.c, rl, rh });
    }
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

  // Technology waves (her idea, 2026-11-06: a discovery is chased hard, then the lower fruit comes slower): on top of the
  // steady pace g_eta, each wave lowers the land and hours embodied per unit of task capacity by size (in logs) as
  // size (1 - exp(-(t - year) / tau)) after its year: fastest at the discovery, slowing after.
  function waveLog(S, y) {
    let out = 0;
    for (const w of S.waves || []) if (y > w.year) out -= w.size * (1 - Math.exp(-(y - w.year) / w.tau));
    return out;
  }

  function hoursSurge(S, y) {
    let out = 0;
    for (const w of S.waves || []) if (w.hours && y > w.year) { const x = (y - w.year) / (w.htau || w.tau); out += w.hours * x * Math.exp(1 - x); }
    return out;
  }

  function etaPath(par, S, D) {
    if (S.waves && S.waves.length) return D.years.map((y) => Math.exp(-par.g_eta * (y - 1950) + waveLog(S, y)));
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
      const lam = lamk ? par.lam0 * lamk[i]
        : S.hoursPerTask ? par.lam0 * Math.exp((par.g_lam - par.g_eta) * t) * eta[0] / eta[i]   // hours per task: steady
        : par.lam0 * Math.exp(par.g_lam * t);
      const lamW = S.waves ? lam * Math.exp(hoursSurge(S, D.years[i])) : lam;
      const rho = S.rhoData ? par.rho + S.rhoData * D.real_rate[i] : par.rho;
      const e = { N: D.N[i], T: par.T * (land ? land[i] : 1) * (S.landAdults ? D.N[i] : 1), h: par.h, a: par.a, b: SET.b * (bk ? bk[i] : 1), lam: lamW,
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
    if (S.durables) return pathGoods(par0, S, D);
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
    const failed = [];
    let gapSum = 0;
    for (let i = 0; i < es.length; i++) {
      let q = null;
      try { q = solve(es[i]); } catch (err) { q = null; }
      if (!q || !isFinite(q.v) || !isFinite(q.p)) {        // no equilibrium this year: nulls, and on to the next
        failed.push(D.years[i]); gapSum += gapMeasure(es[i]);
        for (const key of ["x", "v", "p", "Ps", "wg", "ws", "labour_share_c", "prime_emp_rate", "theta_V", "goods_basket", "site_basket"]) cols[key].push(null);
        cols.eta.push(es[i].eta); cols.utility.push(es[i].utility === undefined ? 1 : es[i].utility);
        for (const key of Object.keys(an)) an[key].push(null);
        an.b[i] = es[i].b; an.lam[i] = es[i].thetaV !== undefined ? null : es[i].lam;
        continue;
      }
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
    const nn = (f) => (v, i) => (v === null || v === undefined ? null : f(v, i));
    if (S.shelterW !== null && S.shelterW !== undefined) {      // addition A: shelter is building and site
      const w = S.shelterW, pl = cols.p[cols.p.length - 1], vl = cols.v[cols.v.length - 1];
      cols.ws = pl === null ? cols.v.map(() => null) : S.shelterBuild === "wage"   // the building priced like construction: at the wage
        ? cols.v.map(nn((v) => v / (w + (1 - w) * v / vl)))
        : cols.v.map(nn((v, i) => v / (w + (1 - w) * cols.p[i] / pl)));
    }
    cols.wage_goods = cols.wg.map(nn((x) => (cols.wg[0] === null ? null : 100 * x / cols.wg[0])));
    cols.wage_shelter = cols.ws.map(nn((x) => (cols.ws[0] === null ? null : 100 * x / cols.ws[0])));
    cols.failed = failed;
    cols.gapSum = gapSum;
    cols.ok = failed.length === 0;
    cols.partial = !cols.ok && failed.length < es.length;
    if (!cols.ok) {
      const runs = [];
      for (const y of failed) { const r = runs[runs.length - 1]; if (r && y === r[1] + 1) r[1] = y; else runs.push([y, y]); }
      cols.why = `no equilibrium in ${failed.length} year${failed.length > 1 ? "s" : ""}: ` +
        runs.map((r) => (r[0] === r[1] ? `${r[0]}` : `${r[0]}–${r[1]}`)).join(", ");
    }
    cols.chi_max = par.chi_max;
    cols.k = par.k;
    return cols;
  }


  // ---------------------------------------------------------------- the goods model's path (fit_base.durables_years)
  const isSkill = (S) => S.services === "skill";
  function etaGoods(par, S, D) {                  // the other goods' clock, durables' and services': equal in 1950
    const eta = etaPath(par, S, D), t = (i) => D.years[i] - 1950;
    const etaD = eta.map((v, i) => v * Math.exp(-(par.g_dur - par.g_eta) * t(i)));
    if (isSkill(S)) {                              // the skill split: low- and high-skill services, each at its own pace
      const etaL = eta.map((v, i) => v * Math.exp(-(par.g_low - par.g_eta) * t(i)));
      const etaH = eta.map((v, i) => v * Math.exp(-(par.g_high - par.g_eta) * t(i)));
      return { eta, etaD, etaS: null, etaL, etaH, etaPair: etaL.map((v, i) => [v, etaH[i]]) };
    }
    const etaS = S.services ? eta.map((v, i) => v * Math.exp((par.s0_srv || 0) - (par.g_srv - par.g_eta) * t(i))) : null;
    return { eta, etaD, etaS, etaPair: etaS };
  }

  function yearCmp(S, D, i) {                     // fit_base.year_cmp: the nest's shares and each good's pay in year i
    const out = {};
    if (isSkill(S)) { out.omega_l = D.low_share[i]; out.omega_h = D.high_share[i]; }
    else if (S.services) out.omega_s = D.srv_in_rest[i];
    if (S.pay === "record") Object.assign(out, { r_d: D.pay_dur[i], r_n: D.pay_nd[i], r_l: D.pay_low[i], r_h: D.pay_high[i] });
    else if (S.pay === "levels") Object.assign(out, { r_d: D.lvl_dur[i], r_n: D.lvl_nd[i], r_l: D.lvl_low[i], r_h: D.lvl_high[i] });
    return out;
  }

  // fit_base.solve_year: with pay "levels", each good's pay is kappa times its level, kappa holding the model's average pay
  // at the production wage (fixed-point iteration on the equilibrium)
  function solveYear(e, etaD, cmp, etaS, S) {
    if (S.pay !== "levels") return solveG(e, etaD, cmp, etaS);
    const lv = { r_d: cmp.r_d, r_n: cmp.r_n, r_l: cmp.r_l, r_h: cmp.r_h };
    let kappa = 1;
    for (let it = 0; it < 100; it++) {
      const q = solveG(e, etaD, Object.assign({}, cmp, { r_d: kappa * lv.r_d, r_n: kappa * lv.r_n, r_l: kappa * lv.r_l, r_h: kappa * lv.r_h }), etaS);
      const hours = q.dd * (1 - q.xd) + q.dg * (q.dn * (1 - q.xg) + q.dl * (1 - q.xl) + q.dh * (1 - q.xh));
      const paid = q.dd * lv.r_d * (1 - q.xd) + q.dg * (q.dn * lv.r_n * (1 - q.xg) + q.dl * lv.r_l * (1 - q.xl) + q.dh * lv.r_h * (1 - q.xh));
      const nw = hours / paid;
      if (Math.abs(nw - kappa) <= 1e-13 * kappa) { q.kappa = kappa; return q; }
      kappa = nw;
    }
    throw new Error("the pay scale did not settle");
  }

  function refCmp(S, D) {
    return Object.assign({ mode: "ref", omega_d: S.durables.omega_d, phi: S.phi || 0 }, yearCmp(S, D, 0));
  }

  function pinnedChiG(par, S, D) {                // fit_base.pinned_chi: 1950's employment, the goods at their reference point
    const e0 = economies(Object.assign({}, par, { chi_max: 1 }), S, D)[0];
    const g = etaGoods(par, S, D), ref = refCmp(S, D), es0 = S.services ? g.etaPair[0] : null;
    const target = D.prime_emp_rate[0];
    const gap = (lc) => {
      try { return solveYear(Object.assign({}, e0, { chi_max: Math.exp(lc) }), g.etaD[0], ref, es0, S).participation - target; }
      catch (err) { return NaN; }
    };
    const grid = linspace(Math.log(BOUNDS.chi_max[0]), Math.log(BOUNDS.chi_max[1]), 25), vals = grid.map(gap);
    for (let j = 0; j < grid.length - 1; j++) {
      if (isFinite(vals[j]) && isFinite(vals[j + 1]) && vals[j] * vals[j + 1] < 0) return Math.exp(brentq(gap, grid[j], grid[j + 1], 1e-14));
    }
    return null;
  }

  function pathGoods(par0, S, D) {
    let par = par0;
    if (S.pin) {
      const chi = pinnedChiG(par, S, D);
      if (chi === null) return { ok: false, why: "no work-cost scale gives 1950's employment" };
      par = Object.assign({}, par, { chi_max: chi });
    }
    const g = etaGoods(par, S, D), ref = refCmp(S, D), phi = S.phi || 0;
    let q0;
    try { q0 = solveYear(economies(par, S, D)[0], g.etaD[0], ref, S.services ? g.etaPair[0] : null, S); }
    catch (err) { return { ok: false, why: "no equilibrium in 1950" }; }
    const cmp = { omega_d: S.durables.omega_d, sigma_dg: S.durables.sigma_dg, pref_d: q0.pd, pref_g: q0.pg, phi };
    if (isSkill(S)) { cmp.pref_n = q0.pg; cmp.pref_l = q0.pl; cmp.pref_h = q0.ph; }
    else if (S.services) { cmp.pref_n = q0.pg; cmp.pref_s = q0.ps; }
    const es = economies(par, S, D, S.sigma !== null && S.sigma !== undefined ? q0.c : null);
    const keys = ["x", "xd", "xs", "v", "p", "pd", "ps", "c", "Ps", "wg", "ws", "wd", "wsv", "wnd", "labour_share_c", "prime_emp_rate",
                  "theta_V", "goods_basket", "site_basket", "chain_share", "dur_share", "srv_share", "xl", "xh", "wndg", "wlow", "whigh",
                  "low_share", "high_share", "r_d", "r_n", "r_l", "r_h", "kappa", "avg_pay"];
    const cols = {}; for (const k of keys) cols[k] = [];
    cols.eta = g.eta; cols.etaD = g.etaD; cols.etaS = g.etaS; cols.etaL = g.etaL || null; cols.etaH = g.etaH || null; cols.utility = [];
    const sk = isSkill(S);
    const an = { pm: [], kappaV: [], sigmaV: [], phi: [], landHomes: [], landMachines: [], hoursFinal: [], hoursMachine: [],
                 goodsShare: [], siteShare: [], wageGoodsLevel: [], peopleTasks: [], lam: [], b: [], xCeil: [], xdCeil: [],
                 xsCeil: [], rentIncome: [], interestIncome: [], landIncome: [], payIncome: [], replacement: [] };
    const failed = [];
    for (let i = 0; i < es.length; i++) {
      const e = es[i];
      cols.utility.push(e.utility === undefined ? 1 : e.utility);
      let q = null;
      try { q = solveYear(e, g.etaD[i], Object.assign({}, cmp, yearCmp(S, D, i)), S.services ? g.etaPair[i] : null, S); }
      catch (err) { q = null; }
      if (!q || !isFinite(q.v)) {
        failed.push(D.years[i]);
        for (const k of keys) cols[k].push(null);
        for (const k of Object.keys(an)) an[k].push(null);
        continue;
      }
      cols.x.push(q.xg); cols.xd.push(q.xd); cols.xs.push(S.services && !sk ? q.xs : null); cols.v.push(q.v); cols.p.push(q.pg);
      cols.pd.push(q.pd); cols.ps.push(S.services && !sk ? q.ps : null); cols.c.push(q.c); cols.Ps.push(q.Ps);
      cols.wg.push(q.v / q.c); cols.ws.push(q.v); cols.wd.push(q.v / q.pd);
      cols.wsv.push(S.services && !sk ? q.v / q.ps : null); cols.wnd.push(S.services && !sk ? q.v / q.pg : null);
      cols.labour_share_c.push(q.labour_share_bea); cols.prime_emp_rate.push(q.participation); cols.theta_V.push(q.theta_V);
      cols.goods_basket.push(q.gb); cols.site_basket.push(q.sb); cols.chain_share.push(q.chain_share);
      cols.dur_share.push(q.dur_share); cols.srv_share.push(S.services && !sk ? q.srv_share : null);
      cols.xl.push(sk ? q.xl : null); cols.xh.push(sk ? q.xh : null);
      cols.wndg.push(sk ? q.v / q.pg : null); cols.wlow.push(sk ? q.v / q.pl : null); cols.whigh.push(sk ? q.v / q.ph : null);
      cols.low_share.push(sk ? q.low_share : null); cols.high_share.push(sk ? q.high_share : null);
      cols.r_d.push(q.rd); cols.r_n.push(q.rg); cols.r_l.push(sk ? q.rl : null); cols.r_h.push(sk ? q.rh : null);
      cols.kappa.push(q.kappa === undefined ? 1 : q.kappa); cols.avg_pay.push((q.final_w + q.mh) / (q.final + q.mh));
      an.pm.push(q.pm); an.kappaV.push(q.kappa_V); an.sigmaV.push(q.sigma_V); an.phi.push(phi);
      an.landHomes.push(q.sb * q.B / e.T); an.landMachines.push(e.b * e.delta * q.K / e.T);
      an.hoursFinal.push(q.final / q.n); an.hoursMachine.push(q.mh / q.n);
      an.goodsShare.push(q.c * q.gb / q.Ps); an.siteShare.push(q.sb / q.Ps); an.wageGoodsLevel.push(q.v / q.c);
      an.peopleTasks.push(1 - q.xg); an.lam.push(e.lam); an.b.push(e.b);
      an.xCeil.push(q.xg_ceiling); an.xdCeil.push(q.xd_ceiling); an.xsCeil.push(S.services && !sk ? q.xs_ceiling : null);
      an.rentIncome.push(q.rent_income); an.interestIncome.push(q.interest_income); an.landIncome.push(q.land_income);
      an.payIncome.push(q.v * (q.final_w + q.mh) / q.income); an.replacement.push(q.inv_income / (1 + q.inv_income));
    }
    cols.an = an;
    const i57 = D.years.indexOf(1957);
    const idx = (arr, at) => arr.map((v) => (v === null || arr[at] === null ? null : 100 * v / arr[at]));
    cols.wage_goods = idx(cols.wg, 0); cols.wage_shelter = idx(cols.ws, 0); cols.wage_durables = idx(cols.wd, 0);
    if (S.services && !sk) { cols.wage_services = idx(cols.wsv, i57); cols.wage_nondurables = idx(cols.wnd, i57); }
    if (sk) { cols.wage_ndg = idx(cols.wndg, 0); cols.wage_low = idx(cols.wlow, 0); cols.wage_high = idx(cols.whigh, 0); }
    cols.extra = S.extra || [];
    cols.failed = failed; cols.gapSum = failed.length; cols.ok = failed.length === 0;
    cols.partial = !cols.ok && failed.length < es.length;
    if (!cols.ok) cols.why = `no equilibrium in ${failed.length} year${failed.length > 1 ? "s" : ""}`;
    cols.chi_max = par.chi_max; cols.k = par.k; cols.goods = true;
    return cols;
  }

  // ---------------------------------------------------------------- the misfit (fit_base.py)
  function deviations(m, D) {
    const out = {};
    for (const s of seriesOf(m.extra)) {
      out[s] = D[s].map((y, i) => {
        if (y === null || y === undefined || !isFinite(y)) return NaN;
        const f = m[s] ? m[s][i] : null;
        if (f === null || f === undefined || !isFinite(f)) return NaN;
        if (s === "wage_goods" || s === "wage_shelter") return (Math.log(f) - Math.log(y)) / TOL[s];
        if (EXTRA_TOL[s] !== undefined) return (Math.log(f) - Math.log(y)) / EXTRA_TOL[s];
        if (s === "labour_share_c") return (f - y) / D.ls_tol[i];
        return (f - y) / TOL[s];
      });
    }
    return out;
  }

  // The misfit; over the solved years only when some years have no equilibrium (partial), and then over the series that
  // have any solved year with data.
  function misfit(m, D) {
    const dev = deviations(m, D), by = {};
    let tot = 0, k = 0;
    for (const s of seriesOf(m.extra)) {
      let sum = 0, n = 0;
      for (const d of dev[s]) if (isFinite(d)) { sum += d * d; n += 1; }
      by[s] = n ? sum / n : null;
      if (n) { tot += by[s]; k += 1; }
    }
    return { total: k ? tot / k : null, by, partial: !m.ok };
  }

  function nObs(D, extra) {
    const out = {};
    for (const s of seriesOf(extra)) out[s] = D[s].filter((y) => y !== null && y !== undefined && isFinite(y)).length;
    return out;
  }

  function residuals(par, S, D, N_OBS) {
    const m = path(par, S, D), ser = seriesOf(S.extra);
    const out = [];
    if (!m.ok) {
      for (const s of ser) for (let j = 0; j < N_OBS[s]; j++) out.push(10);
      return out;
    }
    const dev = deviations(m, D);
    const FW = S.fitWeights || null;               // exploration only: {series: {name: weight}, from: first year counted}
    for (const s of ser) {
      const w = 1 / Math.sqrt(N_OBS[s] * ser.length) * (FW && FW.series && FW.series[s] !== undefined ? Math.sqrt(FW.series[s]) : 1);
      dev[s].forEach((d, i) => {
        if (D[s][i] === null || D[s][i] === undefined || !isFinite(D[s][i])) return;
        out.push(FW && FW.from && D.years[i] < FW.from ? 0 : (isFinite(d) ? d * w : 0));
      });
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
                  g_eta: [-0.05, 0.8, false], lam0: [0.01, 1000, true], g_lam: [-0.1, 0.8, false],
                  g_lamTask: [-0.35, 0.2, false], g_dur: [-0.05, 0.9, false], g_srv: [-0.05, 0.9, false],
                  g_durTask: [-0.35, 0.2, false], g_srvTask: [-0.35, 0.2, false], g_low: [-0.05, 0.9, false],
                  g_high: [-0.05, 0.9, false], g_lowTask: [-0.35, 0.2, false], g_highTask: [-0.35, 0.2, false] };
  const DEFAULT_SYS = { land: "Th", machine: "a", labour: "lam" };
  function toCoords(par, D) {
    const c = { T: par.T, h: par.h, hT: par.h / par.T, a: par.a, kappa50: (par.rho + D.delta[0]) * par.a, rho: par.rho,
                k: par.k, chi_max: par.chi_max, g_eta: par.g_eta, lam0: par.lam0, g_lam: par.g_lam,
                g_lamTask: par.g_lam - par.g_eta };
    if (par.g_dur !== undefined) { c.g_dur = par.g_dur; c.g_durTask = par.g_lam - par.g_dur; }    // the goods model: each good's
    if (par.g_srv !== undefined) { c.g_srv = par.g_srv; c.g_srvTask = par.g_lam - par.g_srv; }    // hours per task capacity
    if (par.g_low !== undefined) { c.g_low = par.g_low; c.g_lowTask = par.g_lam - par.g_low; }    // the skill split's groups
    if (par.g_high !== undefined) { c.g_high = par.g_high; c.g_highTask = par.g_lam - par.g_high; }
    return c;
  }
  function fromCoords(c, sys, D) {
    sys = Object.assign({}, DEFAULT_SYS, sys || {});
    const out = { T: c.T, h: sys.land === "TS" ? c.hT * c.T : c.h,
                  a: sys.machine === "kappa" ? c.kappa50 / (c.rho + D.delta[0]) : c.a, rho: c.rho, k: c.k, chi_max: c.chi_max,
                  g_eta: c.g_eta, lam0: c.lam0, g_lam: sys.labour === "task" ? c.g_lamTask + c.g_eta : c.g_lam };
    if (c.g_dur !== undefined) out.g_dur = sys.labour === "task" ? out.g_lam - c.g_durTask : c.g_dur;
    if (c.g_srv !== undefined) out.g_srv = sys.labour === "task" ? out.g_lam - c.g_srvTask : c.g_srv;
    if (c.g_low !== undefined) out.g_low = sys.labour === "task" ? out.g_lam - c.g_lowTask : c.g_low;
    if (c.g_high !== undefined) out.g_high = sys.labour === "task" ? out.g_lam - c.g_highTask : c.g_high;
    return out;
  }
  const KNOT_KEYS = ["clock", "land", "chi", "lamk", "tilt", "bk", "utility"];

  // ---------------------------------------------------------------- a small fitter (Levenberg-Marquardt, in bounds)
  // free: names from NAMES (not chi_max when pinned), plus "clock:<i>" for the knots of a bent clock (log eta at knot i).
  // The space the fitter and the start search move in. free: coordinate names (COORD), and knots of a path in S:
  // "key:i" its level, "key:i:y" its year (utility levels are levels, searched in logs; every other path's levels are
  // logs already). Returns the start, the bounds and the map back to (par, S), and a natural step per direction.
  function space(par0, S0, D, free) {
    const sys = Object.assign({}, DEFAULT_SYS, S0.coords || {});
    const c0 = toCoords(par0, D);
    const isKnot = (n) => n.indexOf(":") > 0;
    const parse = (n) => { const q = n.split(":"); return { key: q[0], i: +q[1], year: q[2] === "y", field: q[2] }; };
    const getK = (S, n) => {
      const k = parse(n);
      if (k.key === "wave") return k.field === "tau" || k.field === "htau" ? Math.log(S.waves[k.i][k.field] || S.waves[k.i].tau) : (S.waves[k.i][k.field] || 0);
      const kn = S[k.key][k.i]; return k.year ? kn[0] : (k.key === "utility" ? Math.log(kn[1]) : kn[1]);
    };
    const putK = (S, n, v) => {
      const k = parse(n);
      if (k.key === "wave") { S.waves[k.i][k.field] = k.field === "tau" || k.field === "htau" ? Math.exp(v) : v; return; }
      const kn = S[k.key][k.i]; if (k.year) kn[0] = v; else kn[1] = k.key === "utility" ? Math.exp(v) : v;
    };
    const bounds = free.map((n) => {
      if (!isKnot(n)) { const b = COORD[n]; return b[2] ? [Math.log(b[0]), Math.log(b[1])] : [b[0], b[1]]; }
      const k = parse(n);
      if (k.key === "wave") return k.field === "size" ? [0, 10] : k.field === "hours" ? [-5, 5]
        : k.field === "tau" || k.field === "htau" ? [Math.log(0.5), Math.log(60)] : [1950, 2022];
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
      if (S.waves) out.waves = S.waves.map((w) => Object.assign({}, w));
      return out;
    };
    const unpack = (u) => {
      const c = Object.assign({}, c0), S = copyS(S0);
      free.forEach((n, j) => { if (isKnot(n)) putK(S, n, u[j]); else c[n] = fromU(n, u[j]); });
      return { par: Object.assign({}, par0, fromCoords(c, sys, D)), S };
    };
    const u0 = clamp(free.map((n) => (isKnot(n) ? getK(S0, n) : toU(n, c0[n]))));
    const scale = free.map((n, j) => (isKnot(n) ? (parse(n).key === "wave" ? (parse(n).field === "year" ? 4 : 0.5) : parse(n).year ? 3 : 0.4)
      : Math.min(1, 0.15 * (hi[j] - lo[j]))));
    return { u0, lo, hi, clamp, unpack, scale };
  }

  function fit(par0, S0, D, free, opts) {
    opts = opts || {};
    const N_OBS = nObs(D, S0.extra);
    const maxIter = opts.maxIter || 300;
    const onStep = opts.onStep || (() => {});
    const sp = space(par0, S0, D, free), lo = sp.lo, hi = sp.hi, clamp = sp.clamp, unpack = sp.unpack;
    const cost = (r) => r.reduce((a, x) => a + x * x, 0);
    let u = sp.u0;
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

  // The start search (her ask, 2026-11-06): moves the free numbers and points at random around where they are, keeping a
  // move when fewer years lack an equilibrium (or the same number, nearer to having one), until every year solves. A start
  // for the fitter, not a fit: it stops as soon as every year solves.
  function search(par0, S0, D, free, opts) {
    opts = opts || {};
    const maxEval = opts.maxEval || 3000, onStep = opts.onStep || (() => {});
    let seed = opts.seed || 12345;
    const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
    const gauss = () => { const a = Math.max(rnd(), 1e-12), b = rnd(); return Math.sqrt(-2 * Math.log(a)) * Math.cos(2 * Math.PI * b); };
    const sp = space(par0, S0, D, free);
    const score = (m) => (m.failed ? m.failed.length + Math.min(0.999, m.gapSum / (1 + m.gapSum)) : D.years.length + 1);
    let u = sp.u0, best = sp.unpack(u), mBest = path(best.par, best.S, D), sBest = score(mBest);
    let sigma = 0.5, evals = 1;
    while (evals < maxEval && !(mBest.ok)) {
      let improved = false;
      for (let c = 0; c < 8; c++) {
        const u2 = sp.clamp(u.map((x, j) => x + sigma * sp.scale[j] * gauss()));
        const t = sp.unpack(u2), m = path(t.par, t.S, D), sc = score(m);
        evals += 1;
        if (sc < sBest) { u = u2; best = t; mBest = m; sBest = sc; improved = true; if (m.ok) break; }
      }
      sigma = improved ? Math.min(sigma * 1.5, 3) : Math.max(sigma * 0.85, 0.02);
      onStep({ evals, unsolved: mBest.failed ? mBest.failed.length : D.years.length, par: best.par, S: best.S });
    }
    return { par: best.par, S: best.S, ok: !!mBest.ok, evals, unsolved: mBest.failed ? mBest.failed.length : D.years.length };
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

  const api = { SET, SERIES, TOL, EXTRA_TOL, seriesOf, BOUNDS, LOGP, NAMES, COORD, DEFAULT_SYS, KNOT_KEYS, brentq, gamma, parts,
                basket, solve, xCeiling, economies, pinnedChi, path, deviations, misfit, residuals, nObs, fit, interp, utilityPath,
                etaPath, toCoords, fromCoords, knotMul, search, gapMeasure, xOf, JOf, composite, restNest, partsG, mCeiling, solveG,
                etaGoods, pinnedChiG, pathGoods };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.USRecordModel = api;
})(typeof self !== "undefined" ? self : this);
