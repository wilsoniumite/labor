// round5.js — her questions of 2026-11-06: (1) labour's share of a machine's cost taken from the record, so the machine
// chain's labour lambda follows and needs no clock of its own; (2) the return set at 2% and a set so that machine services
// are a fifth of a machine's cost in 2023 (calibration (c)'s measured shares: labour 0.47, fixed rents 0.33).
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const prof = JSON.parse(fs.readFileSync("playground/profiles.json", "utf8"));
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const four = (mf) => (mf.by.wage_goods + mf.by.wage_shelter + mf.by.labour_share_c + mf.by.prime_emp_rate) / 4;
function report(name, f, S) {
  const m = M.path(f.par, S, D);
  if (!m.ok) { console.log(name.padEnd(56), "no equilibrium:", m.why); return; }
  const mf = M.misfit(m, D), i50 = 0, i24 = D.years.length - 1;
  const kap = (i) => (f.par.rho + D.delta[i]) * f.par.a;
  console.log(`${name.padEnd(56)} total ${mf.total.toFixed(2)}, four series ${four(mf).toFixed(2)} | ${Object.values(mf.by).map((v) => v.toFixed(1)).join(" ")} | ` +
    `clock ${(f.par.g_eta * 100).toFixed(1)}% a ${f.par.a.toFixed(2)} rho ${(f.par.rho * 100).toFixed(1)}% | machine cost: services ${kap(i50).toFixed(2)}->${kap(i24).toFixed(2)}, ` +
    `labour ${m.theta_V[i50].toFixed(2)}->${m.theta_V[i24].toFixed(2)}, land ${(1 - kap(i50) - m.theta_V[i50]).toFixed(3)}->${(1 - kap(i24) - m.theta_V[i24]).toFixed(3)}`);
}
report("kept (for comparison)", { par: kept.params }, kept.settings);
// (1) theta_V from the record, lambda's two numbers gone
let S1 = Object.assign({}, kept.settings, { thetaVData: true });
let f1 = M.fit(kept.params, S1, D, ["T", "h", "a", "k", "rho", "g_eta"], { maxIter: 800 });
report("labour's share of machine cost from the record", f1, S1);
// (2) return 2%, then a walked to the measured machine-services share (0.20 in 2023)
const r2 = prof["required return"].find((r) => r.v === 0.02);
const aTarget = 0.20 / (0.02 + D.delta[D.years.indexOf(2023)]);
let par = Object.assign({}, r2.par), S2 = kept.settings;
const free2 = ["T", "h", "k", "g_eta", "lam0", "g_lam"];
for (let s = 1; s <= 8; s++) { par.a = r2.par.a + (aTarget - r2.par.a) * s / 8; par = M.fit(par, S2, D, free2, { maxIter: 300 }).par; }
report(`return 2%, a ${aTarget.toFixed(2)} (machine services 0.20 in 2023)`, { par }, S2);
// (3) both: theta_V from the record, return 2%, a from the measured share
let par3 = Object.assign({}, f1.par);
for (let s = 1; s <= 8; s++) {
  par3.rho = f1.par.rho + (0.02 - f1.par.rho) * s / 8; par3.a = f1.par.a + (aTarget - f1.par.a) * s / 8;
  par3 = M.fit(par3, S1, D, ["T", "h", "k", "g_eta"], { maxIter: 300 }).par;
}
report("both: theta_V from the record, return 2%, a set", { par: par3 }, S1);
fs.writeFileSync("playground/round5.json", JSON.stringify({ thetaV: f1, set_a_rho: par, both: par3 }, null, 1));
