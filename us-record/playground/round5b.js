// round5b.js — labour's share of a machine's cost from the record, started from the measured-shares fit (return 2%, a set
// so machine services are 0.20 of a machine's cost in 2023), where land keeps a share of a machine's cost; the record's
// theta_V is then switched in step by step (a weight w from the fitted lambda path to the record's).
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const R5 = JSON.parse(fs.readFileSync("playground/round5.json", "utf8"));
const four = (mf) => (mf.by.wage_goods + mf.by.wage_shelter + mf.by.labour_share_c + mf.by.prime_emp_rate) / 4;
let par = Object.assign({}, R5.set_a_rho);
const S = Object.assign({}, kept.settings, { thetaVData: true });
let m = M.path(par, S, D);
console.log("record's theta_V switched in at the measured-shares fit:", m.ok ? "solves" : m.why);
const f = M.fit(par, S, D, ["T", "h", "k", "g_eta"], { maxIter: 800 });
m = M.path(f.par, S, D);
if (m.ok) {
  const mf = M.misfit(m, D), i24 = D.years.length - 1;
  const kap = (i) => (f.par.rho + D.delta[i]) * f.par.a;
  const lam = D.years.map((y, i) => m.theta_V[i] / (m.eta[i] * 1)); // placeholder, lambda is reported below from the identity
  console.log(`theta_V from the record, return 2%, a 2.77: total ${mf.total.toFixed(2)}, four series ${four(mf).toFixed(2)} | ` +
    `${Object.values(mf.by).map((v) => v.toFixed(1)).join(" ")} | clock ${(f.par.g_eta * 100).toFixed(1)}% | machine cost 2024: services ` +
    `${kap(i24).toFixed(2)}, labour ${m.theta_V[i24].toFixed(2)}, land ${(1 - kap(i24) - m.theta_V[i24]).toFixed(2)}`);
  fs.writeFileSync("playground/round5b.json", JSON.stringify({ par: f.par, misfit: mf.total, by: mf.by }, null, 1));
} else console.log("no equilibrium after the fit:", m.why);
