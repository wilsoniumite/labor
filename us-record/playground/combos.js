// combos.js — the first batch's better ideas together, and a few more cheap ones. Run from us-record/: node playground/combos.js
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const g0 = kept.params.g_eta, gl0 = kept.params.g_lam;
const out = fs.existsSync("playground/combos.json") ? JSON.parse(fs.readFileSync("playground/combos.json", "utf8")) : {};
const clockK = () => [1950, 1970, 1990, 2010, 2024].map((y) => [y, -g0 * (y - 1950)]);
const lamK = () => [1950, 1970, 1990, 2010, 2024].map((y) => [y, gl0 * (y - 1950)]);
const KN = (key) => [1, 2, 3, 4].map((i) => `${key}:${i}`);
const wo = (...n) => FREE.filter((x) => !n.includes(x));
const EXP = [
  ["bendable clock + bendable machine labour", (c) => { c.S.clock = clockK(); c.S.lamk = lamK(); return wo("g_eta", "g_lam").concat(KN("clock"), KN("lamk")); }],
  ["A' + bendable machine labour", (c) => { c.S.shelterW = 0.4; c.S.shelterBuild = "wage"; c.S.lamk = lamK(); return wo("g_lam").concat(KN("lamk")); }],
  ["A' + bendable clock", (c) => { c.S.shelterW = 0.4; c.S.shelterBuild = "wage"; c.S.clock = clockK(); return wo("g_eta").concat(KN("clock")); }],
  ["A' + both bendable", (c) => { c.S.shelterW = 0.4; c.S.shelterBuild = "wage"; c.S.clock = clockK(); c.S.lamk = lamK(); return wo("g_eta", "g_lam").concat(KN("clock"), KN("lamk")); }],
  ["labour share read as all labour (traced)", (c) => { c.S.lsBasis = "traced"; }],
  ["traced + bendable machine labour", (c) => { c.S.lsBasis = "traced"; c.S.lamk = lamK(); return wo("g_lam").concat(KN("lamk")); }],
  ["A' site share 0.3", (c) => { c.S.shelterW = 0.3; c.S.shelterBuild = "wage"; }],
  ["A' site share 0.5", (c) => { c.S.shelterW = 0.5; c.S.shelterBuild = "wage"; }],
  ["A' + return fixed at 5%", (c) => { c.S.shelterW = 0.4; c.S.shelterBuild = "wage"; c.par.rho = 0.0; return FREE; }],
];
for (const [name, mod] of EXP) {
  const c = { S: JSON.parse(JSON.stringify(kept.settings)), par: Object.assign({}, kept.params) };
  const free = mod(c) || FREE;
  const t0 = Date.now();
  const f = M.fit(c.par, c.S, D, free, { maxIter: 800 });
  const m = M.path(f.par, f.S, D), mf = m.ok ? M.misfit(m, D) : null;
  out[name] = { misfit: mf ? mf.total : null, by: mf ? mf.by : null, par: f.par, S: f.S };
  const kn = (key) => (f.S[key] ? " " + key + " " + f.S[key].map((k) => k[1].toFixed(2)).join("/") : "");
  console.log(`${name.padEnd(44)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""} | rho ${f.par.rho.toFixed(3)} a ${f.par.a.toFixed(2)}${kn("clock")}${kn("lamk")} | ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  fs.writeFileSync("playground/combos.json", JSON.stringify(out, null, 1));
}
