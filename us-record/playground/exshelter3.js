// exshelter3.js — is the all-but-shelter + women's entry fit a stable optimum? (1) the machine-making hours' growth
// expressed per unit of task capacity (no bound in the way); (2) twelve random restarts: the start search from scattered
// points, then the fit. Run from us-record/: node playground/exshelter3.js
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const alt = JSON.parse(fs.readFileSync("playground/wage_exshelter.json", "utf8")).wage_exshelter;
const D = Object.assign({}, doc.data, { wage_goods: alt });
const kept = doc.presets.find((p) => p.id === "kept");
const EX2 = JSON.parse(fs.readFileSync("playground/exshelter2.json", "utf8"));
const best = EX2["women's entry until 1990"];
const S = Object.assign(JSON.parse(JSON.stringify(best.S)), { coords: { land: "Th", machine: "a", labour: "task" } });
const freeT = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lamTask", "chi:1"];
const show = (name, f) => {
  const m = M.path(f.par, f.S, D), mf = m.ok ? M.misfit(m, D) : null;
  console.log(`${name.padEnd(30)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""} | ` +
    `clock ${(100 * f.par.g_eta).toFixed(1)}%, hours per task ${(100 * (f.par.g_lam - f.par.g_eta)).toFixed(1)}%, ρ ${(100 * f.par.rho).toFixed(1)}%, a ${f.par.a.toFixed(2)}, k ${f.par.k.toFixed(1)}, ` +
    `cost of working by 1990 x${Math.exp(f.S.chi[1][1]).toFixed(2)}`);
  return mf ? mf.total : Infinity;
};
const f0 = M.fit(best.par, S, D, freeT, { maxIter: 1200 });
show("per-task growth, from the fit", f0);
let seed = 7;
const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
const results = [];
for (let r = 0; r < 12; r++) {
  const par = Object.assign({}, f0.par, {
    T: f0.par.T * Math.exp(2 * (rnd() - 0.5)), h: f0.par.h * Math.exp(2 * (rnd() - 0.5)), a: Math.min(9.5, f0.par.a * Math.exp(1.5 * (rnd() - 0.5))),
    k: f0.par.k * Math.exp(1.0 * (rnd() - 0.5)), rho: 0.10 * rnd(), g_eta: 0.04 + 0.10 * rnd(), lam0: f0.par.lam0 * Math.exp(2 * (rnd() - 0.5)) });
  par.g_lam = par.g_eta + (f0.par.g_lam - f0.par.g_eta) + 0.04 * (rnd() - 0.5);
  const S2 = JSON.parse(JSON.stringify(f0.S)); S2.chi[1][1] = Math.log(0.6 + 0.5 * rnd());
  let st = { par, S: S2 };
  if (!M.path(par, S2, D).ok) { const s = M.search(par, S2, D, freeT, { maxEval: 3000, seed: 99 + r }); st = { par: s.par, S: s.S }; if (!s.ok) { console.log(`restart ${r + 1}: no start found`); continue; } }
  const f = M.fit(st.par, st.S, D, freeT, { maxIter: 1200 });
  results.push(show(`restart ${r + 1}`, f));
}
console.log("restart misfits, sorted:", results.sort((a, b) => a - b).map((v) => v.toFixed(2)).join(", "));
