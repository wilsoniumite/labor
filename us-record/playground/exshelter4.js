// exshelter4.js — all but shelter + women's entry, with the defensible machine numbers: the return at 2% and a set so
// machine services are 0.20 of a machine's cost in 2023 (calibration (c)'s measured split), with and without the dated waves.
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const alt = JSON.parse(fs.readFileSync("playground/wage_exshelter.json", "utf8")).wage_exshelter;
const D = Object.assign({}, doc.data, { wage_goods: alt });
const kept = doc.presets.find((p) => p.id === "kept");
const R5 = JSON.parse(fs.readFileSync("playground/round5.json", "utf8"));
const out = {};
const wn = (n, fields) => Array.from({ length: n }, (_, i) => fields.map((f) => `wave:${i}:${f}`)).flat();
function run(name, S, par, free) {
  let f = M.fit(par, S, D, free, { maxIter: 1200 });
  let m = M.path(f.par, f.S, D);
  if (!m.ok) { const r = M.search(par, S, D, free, { maxEval: 4000 }); f = M.fit(r.par, r.S, D, free, { maxIter: 1200 }); m = M.path(f.par, f.S, D); }
  const mf = m.ok ? M.misfit(m, D) : null, a = m.ok ? m.an : null, L = 74;
  out[name] = { misfit: mf && mf.total, by: mf && mf.by, par: f.par, S: f.S };
  console.log(`${name.padEnd(46)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""}` +
    (mf ? ` | clock ${(100 * f.par.g_eta).toFixed(1)}%, hours/task ${(100 * (f.par.g_lam - f.par.g_eta)).toFixed(1)}%, work cost by 1990 x${Math.exp(f.S.chi[1][1]).toFixed(2)}, ` +
      `machine cost 2024: services ${(100 * a.kappaV[L]).toFixed(0)}% labour ${(100 * m.theta_V[L]).toFixed(0)}% land ${(100 * a.sigmaV[L]).toFixed(0)}%, machine-making hours ${(100 * a.hoursMachine[L]).toFixed(0)}%` : ""));
  fs.writeFileSync("playground/exshelter4.json", JSON.stringify(out, null, 1));
  return f;
}
const S = Object.assign(JSON.parse(JSON.stringify(kept.settings)), { chi: [[1950, 0], [1990, 0]], coords: { land: "Th", machine: "a", labour: "task" } });
const par = Object.assign({}, R5.set_a_rho);
const free = ["T", "h", "k", "g_eta", "lam0", "g_lamTask", "chi:1"];
const f1 = run("measured shares, women's entry to 1990", S, par, free);
run("... and the dated waves 1948, 1995", Object.assign(JSON.parse(JSON.stringify(f1.S)), { waves: [1948, 1995].map((y) => ({ year: y, size: 0.05, tau: 15 })) }), f1.par, free.concat(wn(2, ["size", "tau"])));
