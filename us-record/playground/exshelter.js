// exshelter.js — the model's one final good read as everything but shelter (the real wage over the CPI less shelter)
// instead of durables, the fastest-cheapening goods; is labour's share then still at odds with the goods wage?
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D0 = doc.data;
const alt = JSON.parse(fs.readFileSync("playground/wage_exshelter.json", "utf8")).wage_exshelter;
const D1 = Object.assign({}, D0, { wage_goods: alt });
const kept = doc.presets.find((p) => p.id === "kept");
const R5 = JSON.parse(fs.readFileSync("playground/round5.json", "utf8"));
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const K = () => JSON.parse(JSON.stringify(kept.settings));
const wn = (n, fields) => Array.from({ length: n }, (_, i) => fields.map((f) => `wave:${i}:${f}`)).flat();
const out = {};
function run(name, D, S, par, free) {
  let f = M.fit(par, S, D, free, { maxIter: 800 });
  let m = M.path(f.par, f.S, D);
  if (!m.ok) { const r = M.search(par, S, D, free, { maxEval: 3000 }); f = M.fit(r.par, r.S, D, free, { maxIter: 800 }); m = M.path(f.par, f.S, D); }
  const mf = m.ok ? M.misfit(m, D) : null;
  out[name] = { misfit: mf && mf.total, by: mf && mf.by, par: f.par, S: f.S };
  const waves = (f.S.waves || []).map((w) => `${w.year}: ${w.size.toFixed(2)}/${w.tau.toFixed(0)}y`).join("; ");
  console.log(`${name.padEnd(50)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""} | ` +
    `clock ${(100 * f.par.g_eta).toFixed(1)}% gλ ${(100 * f.par.g_lam).toFixed(1)}% a ${f.par.a.toFixed(2)} ρ ${(100 * f.par.rho).toFixed(1)}%${waves ? " | " + waves : ""}`);
  fs.writeFileSync("playground/exshelter.json", JSON.stringify(out, null, 1));
  return f;
}
console.log("columns: total | goods wage, shelter wage, labour share, prime-age employment, theta_V");
run("durables (as kept)", D0, K(), kept.params, FREE);
const g1 = run("all but shelter, steady clock", D1, K(), kept.params, FREE);
run("all but shelter, dated waves 1948 and 1995", D1, Object.assign(K(), { waves: [1948, 1995].map((y) => ({ year: y, size: 0.05, tau: 15 })) }), g1.par, FREE.concat(wn(2, ["size", "tau"])));
run("all but shelter, measured shares (2%, a 2.77)", D1, K(), Object.assign({}, R5.set_a_rho), ["T", "h", "k", "g_eta", "lam0", "g_lam"]);
run("all but shelter, labour's share weighted x10", D1, Object.assign(K(), { fitWeights: { series: { labour_share_c: 10 } } }), g1.par, FREE);
