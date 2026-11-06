// waves3.js — waves dated from the productivity record, started small so the fitter can grow them (waves2's start, with
// sizes 0.8 on top of the kept pace, had no way down). Run from us-record/: node playground/waves3.js
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const K = () => JSON.parse(JSON.stringify(kept.settings));
const wn = (n, fields) => Array.from({ length: n }, (_, i) => fields.map((f) => `wave:${i}:${f}`)).flat();
const at = (y) => D.years.indexOf(y);
const eras = [[1950, 1960], [1960, 1973], [1973, 1995], [1995, 2005], [2005, 2024]];
const out = {};
for (const [label, yrs] of [["dated: post-war 1948 + IT 1995", [1948, 1995]], ["dated: post-war 1948 + IT 1995 + 2015", [1948, 1995, 2015]],
                            ["dated: IT 1995 alone", [1995]]]) {
  let best = null;
  for (const tau0 of [5, 15, 30]) {
    const S = Object.assign(K(), { waves: yrs.map((y) => ({ year: y, size: 0.05, tau: tau0 })) });
    const f = M.fit(kept.params, S, D, FREE.concat(wn(yrs.length, ["size", "tau"])), { maxIter: 800 });
    if (!best || f.misfit < best.misfit) best = f;
  }
  const m = M.path(best.par, best.S, D), mf = M.misfit(m, D), eta = M.etaPath(best.par, best.S, D);
  out[label] = { misfit: mf.total, by: mf.by, par: best.par, S: best.S };
  console.log(`${label.padEnd(40)} ${mf.total.toFixed(2)} | ${Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ")} | pace ${(100 * best.par.g_eta).toFixed(1)}% | ` +
    best.S.waves.map((w) => `${w.year}: ${w.size.toFixed(2)} over ~${w.tau.toFixed(0)}y`).join("; "));
  console.log("   by era:", eras.map(([a, b]) => `${a}-${b} ${(-100 * Math.log(eta[at(b)] / eta[at(a)]) / (b - a)).toFixed(1)}%`).join("  "));
}
fs.writeFileSync("playground/waves3.json", JSON.stringify(out, null, 1));
