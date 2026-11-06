// waves2.js — waves dated from outside the fit (the US productivity record's textbook breaks: the post-war boom from
// about 1948, the IT boom from about 1995), so only their sizes and speeds are fitted; and how the record reads the
// waves found with free dates, in the two real clocks (land and hours per unit of task capacity).
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const K = () => JSON.parse(JSON.stringify(kept.settings));
const wn = (n, fields) => Array.from({ length: n }, (_, i) => fields.map((f) => `wave:${i}:${f}`)).flat();
const report = (name, f) => {
  const m = M.path(f.par, f.S, D), mf = M.misfit(m, D);
  const waves = (f.S.waves || []).map((w) => `${w.year.toFixed(0)}: ${w.size.toFixed(2)} over ~${w.tau.toFixed(0)}y`).join("; ");
  console.log(`${name.padEnd(46)} ${mf.total.toFixed(2).padStart(6)} | ${Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ")} | pace ${(100 * f.par.g_eta).toFixed(1)}% | ${waves}`);
  return m;
};
for (const [label, yrs] of [["post-war 1948 + IT 1995 (dated)", [1948, 1995]], ["post-war 1948 alone (dated)", [1948]], ["post-war 1948 + IT 1995 + AI 2015 (dated)", [1948, 1995, 2015]]]) {
  const S = Object.assign(K(), { waves: yrs.map((y) => ({ year: y, size: 0.8, tau: 12 })) });
  let f = M.fit(kept.params, S, D, FREE.concat(wn(yrs.length, ["size", "tau"])), { maxIter: 800 });
  report(label, f);
}
// the real clocks in the free-date fits: land per unit of task capacity (b eta) and hours per unit (lambda eta), yearly pace by era
const R = JSON.parse(fs.readFileSync("playground/waves.json", "utf8"));
console.log("\\nyearly fall in land per unit of task capacity, by era (the hours per unit of task capacity fall with it here):");
for (const name of ["kept, steady clock", "two waves, years free (from 1970, 1995)", "two waves, years free (from 1960, 1985)", "three waves, years free (from 1960, 1980, 2000)"]) {
  const f = R[name], eta = M.etaPath(f.par, f.S, D), at = (y) => D.years.indexOf(y);
  const eras = [[1950, 1960], [1960, 1973], [1973, 1995], [1995, 2005], [2005, 2024]];
  console.log(name.padEnd(48), eras.map(([a, b]) => `${a}-${b} ${(-100 * Math.log(eta[at(b)] / eta[at(a)]) / (b - a)).toFixed(1)}%`).join("  "));
}
