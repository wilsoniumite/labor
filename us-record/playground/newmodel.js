// newmodel.js — her setup of 2026-11-06: goods read over everything but shelter, women's entry, no cap, the return at 2%,
// a dip in the basket's utility; then pieces taken out one at a time (does each earn its place?).
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = Object.assign({}, doc.data, { wage_goods: doc.data.wage_exshelter });
const best = JSON.parse(fs.readFileSync("playground/exshelter_best.json", "utf8"))["all but shelter, women's entry to 1990"];
const rw = (y) => D.real_wage_cpi[D.years.indexOf(y)];
const out = {};
function fitFrom(name, S, par, free, quiet) {
  let f = M.fit(par, S, D, free, { maxIter: 1200 });
  let m = M.path(f.par, f.S, D);
  if (!m.ok) { const r = M.search(par, S, D, free, { maxEval: 4000 }); f = M.fit(r.par, r.S, D, free, { maxIter: 1200 }); m = M.path(f.par, f.S, D); }
  const mf = m.ok ? M.misfit(m, D) : null;
  out[name] = { misfit: mf && mf.total, by: mf && mf.by, par: f.par, S: f.S };
  if (!quiet) console.log(`${name.padEnd(56)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""}` +
    (mf ? ` | clock ${(100 * f.par.g_eta).toFixed(1)}%, hours/task ${(100 * (f.par.g_lam - f.par.g_eta)).toFixed(1)}%, a ${f.par.a.toFixed(2)}, k ${f.par.k.toFixed(1)}` +
      (f.S.chi ? `, work cost by ${f.S.chi[1][0]} x${Math.exp(f.S.chi[1][1]).toFixed(2)}` : "") : ""));
  fs.writeFileSync("playground/newmodel.json", JSON.stringify(out, null, 1));
  return f;
}
// walk the return from where the fit has it (0) to 2%, refitting the rest at each step
function walkRho(S, par, free, to) {
  let p = Object.assign({}, par), s = JSON.parse(JSON.stringify(S));
  for (let i = 1; i <= 8; i++) { p.rho = par.rho + (to - par.rho) * i / 8; const f = M.fit(p, s, D, free, { maxIter: 300 }); p = f.par; s = f.S; }
  return { par: p, S: s };
}
const FREE = ["T", "h", "a", "k", "g_eta", "lam0", "g_lamTask", "chi:1"];
const dip = [[1950, 1], [1970, rw(1970)], [1990, rw(1990)], [2024, rw(2024)]];
const S0 = Object.assign(JSON.parse(JSON.stringify(best.S)), { cap: null, utility: dip, knotLocks: undefined });
console.log("columns: total | goods (all but shelter), shelter, labour share, prime-age employment, theta_V");
const w = walkRho(S0, best.par, FREE, 0.02);
const her = fitFrom("her setup: no cap, return 2%, utility dip, women's entry", w.S, w.par, FREE);
// one piece out at a time, from her setup
const S = () => JSON.parse(JSON.stringify(her.S)), P = () => Object.assign({}, her.par);
fitFrom("  without women's entry", Object.assign(S(), { chi: null }), P(), FREE.filter((n) => n !== "chi:1"));
fitFrom("  without the utility dip (rise to 1970, held)", Object.assign(S(), { utility: [[1950, 1], [1970, rw(1970)]] }), P(), FREE);
fitFrom("  without the utility's rise (flat from 1950)", Object.assign(S(), { utility: [[1950, 1]] }), P(), FREE);
fitFrom("  with the cap back", Object.assign(S(), { cap: doc.set_values.cap }), P(), FREE);
fitFrom("  with the start not pinned", Object.assign(S(), { pin: false }), P(), FREE.concat(["chi_max"]));
fitFrom("  without the basket (fixed basket)", Object.assign(S(), { sigma: null }), P(), FREE);
fitFrom("  with the return free", S(), P(), FREE.concat(["rho"]));
fitFrom("  with the post-war wave", Object.assign(S(), { waves: [{ year: 1948, size: 0.05, tau: 15 }] }), P(), FREE.concat(["wave:0:size", "wave:0:tau"]));
fitFrom("  women's entry until 1980", Object.assign(S(), { chi: [[1950, 0], [1980, her.S.chi[1][1]]] }), P(), FREE);
fitFrom("  women's entry until 2000", Object.assign(S(), { chi: [[1950, 0], [2000, her.S.chi[1][1]]] }), P(), FREE);
