// waves.js — her idea of 2026-11-06: technology comes in waves; a discovery is chased hard, then the lower fruit comes
// slower. Each wave lowers the land and hours embodied per unit of task capacity by `size` (logs), fastest at its year,
// with time constant tau; a steady pace runs underneath. Fits from the kept model (cap, basket, pinned start), one start
// each, with the explorer's fitter. Run from us-record/: node playground/waves.js
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const her = JSON.parse(fs.readFileSync("playground/her_spiky.json", "utf8"));
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const out = {};
const W = (years, size = 0.5, tau = 8) => years.map((y) => ({ year: y, size, tau }));
const wn = (n, fields) => Array.from({ length: n }, (_, i) => fields.map((f) => `wave:${i}:${f}`)).flat();
function run(name, S, par, free, maxIter = 600) {
  const t0 = Date.now();
  let f = M.fit(par, S, D, free, { maxIter });
  let m = M.path(f.par, f.S, D);
  if (!m.ok) {                                 // a start without an equilibrium everywhere: search first, then fit
    const r = M.search(par, S, D, free, { maxEval: 3000 });
    f = M.fit(r.par, r.S, D, free, { maxIter }); m = M.path(f.par, f.S, D);
  }
  const mf = m.ok ? M.misfit(m, D) : null;
  out[name] = { misfit: mf ? mf.total : null, by: mf ? mf.by : null, par: f.par, S: f.S };
  const waves = (f.S.waves || []).map((w) => `${w.year.toFixed(0)}: ${w.size.toFixed(2)} over ~${w.tau.toFixed(0)}y`).join("; ");
  console.log(`${name.padEnd(48)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""} | ` +
    `pace ${(100 * f.par.g_eta).toFixed(1)}% ${waves ? "| " + waves : ""} | ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  fs.writeFileSync("playground/waves.json", JSON.stringify(out, null, 1));
  return f;
}
const K = () => JSON.parse(JSON.stringify(kept.settings));
console.log("columns: total | wage durables, wage shelter, labour share, prime-age employment, theta_V");
run("kept, steady clock", K(), kept.params, FREE);
run("one wave at 1970", Object.assign(K(), { waves: W([1970]) }), kept.params, FREE.concat(wn(1, ["size", "tau"])));
run("two waves, 1970 and 1995", Object.assign(K(), { waves: W([1970, 1995]) }), kept.params, FREE.concat(wn(2, ["size", "tau"])));
run("two waves, hours per task steady", Object.assign(K(), { waves: W([1970, 1995]), hoursPerTask: true }), kept.params, FREE.concat(wn(2, ["size", "tau"])));
const freeY = run("two waves, years free (from 1970, 1995)", Object.assign(K(), { waves: W([1970, 1995]) }), kept.params, FREE.concat(wn(2, ["size", "tau", "year"])));
run("two waves, years free (from 1960, 1985)", Object.assign(K(), { waves: W([1960, 1985]) }), kept.params, FREE.concat(wn(2, ["size", "tau", "year"])));
run("two waves, years free (from 1978, 2005)", Object.assign(K(), { waves: W([1978, 2005]) }), kept.params, FREE.concat(wn(2, ["size", "tau", "year"])));
run("three waves, years free (from 1960, 1980, 2000)", Object.assign(K(), { waves: W([1960, 1980, 2000]) }), kept.params, FREE.concat(wn(3, ["size", "tau", "year"])));
// her settings' model (no cap, A' building at the wage), with waves instead of spikes
const HS = () => Object.assign(JSON.parse(JSON.stringify(her.settings)), { clock: null, lamk: null, bk: null });
const hp = Object.assign({}, kept.params);
run("her model (no cap, A'), steady clock", HS(), hp, FREE);
run("her model, two waves, years free", Object.assign(HS(), { waves: W([1970, 1995]) }), hp, FREE.concat(wn(2, ["size", "tau", "year"])));
