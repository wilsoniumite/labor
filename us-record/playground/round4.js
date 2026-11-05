// round4.js — last quick variants: the tilt's start year, A' site shares, the best single changes together, and a
// plausible required return (5%) under the best combination. Run from us-record/: node playground/round4.js
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const out = fs.existsSync("playground/round4.json") ? JSON.parse(fs.readFileSync("playground/round4.json", "utf8")) : {};
const wo = (...n) => FREE.filter((x) => !n.includes(x));
const Ap = (c, w) => { c.S.shelterW = w || 0.4; c.S.shelterBuild = "wage"; };
const tilt = (c, y) => { c.S.tilt = [[1950, 0], [y, 0], [2024, 0]]; };
const EXP = [
  ["tilt from 1990", (c) => { tilt(c, 1990); return FREE.concat(["tilt:2"]); }],
  ["tilt from 2000", (c) => { tilt(c, 2000); return FREE.concat(["tilt:2"]); }],
  ["A' site share 0.6", (c) => { Ap(c, 0.6); }],
  ["A' site share 0.7", (c) => { Ap(c, 0.7); }],
  ["elasticity 1.2 + A' 0.5", (c) => { c.S.sigma = 1.2; Ap(c, 0.5); }],
  ["return 5% + A' 0.5 + tilt 1995", (c) => { c.par.rho = 0.05; Ap(c, 0.5); tilt(c, 1995); return wo("rho").concat(["tilt:2"]); }],
  ["return 5% (kept model otherwise)", (c) => { c.par.rho = 0.05; return wo("rho"); }],
];
for (const [name, mod] of EXP) {
  const c = { S: JSON.parse(JSON.stringify(kept.settings)), par: Object.assign({}, kept.params) };
  const free = mod(c) || FREE;
  // a fixed return far from the kept fit's zero has no equilibrium at the start: walk it there
  let par = Object.assign({}, kept.params), S = c.S;
  if (c.par.rho !== kept.params.rho) {
    for (let s = 1; s <= 6; s++) { par.rho = c.par.rho * s / 6; const f = M.fit(par, S, D, free, { maxIter: 300 }); par = f.par; S = f.S; }
  } else par = c.par;
  const t0 = Date.now();
  const f = M.fit(par, S, D, free, { maxIter: 800 });
  const m = M.path(f.par, f.S, D), mf = m.ok ? M.misfit(m, D) : null;
  const at = (y) => D.years.indexOf(y);
  const site = m.ok ? [1950, 2024].map((y) => (m.site_basket[at(y)] / m.Ps[at(y)]).toFixed(3)).join("->") : "";
  out[name] = { misfit: mf ? mf.total : null, by: mf ? mf.by : null, par: f.par, S: f.S };
  console.log(`${name.padEnd(40)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""} | rho ${f.par.rho.toFixed(3)} clock ${(f.par.g_eta * 100).toFixed(1)}% a ${f.par.a.toFixed(2)} | land share ${site}${f.S.tilt ? " tilt " + Math.exp(f.S.tilt[2][1]).toFixed(2) : ""} | ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  fs.writeFileSync("playground/round4.json", JSON.stringify(out, null, 1));
}
