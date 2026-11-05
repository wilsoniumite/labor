// round3.js — the clock bent at the productivity break years; decade knots; her internet idea as a taste tilt away
// from land after 1995; the 1950 labour share pinned through k. Run from us-record/: node playground/round3.js
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const g0 = kept.params.g_eta, gl0 = kept.params.g_lam;
const out = fs.existsSync("playground/round3.json") ? JSON.parse(fs.readFileSync("playground/round3.json", "utf8")) : {};
const kn = (years, slope) => years.map((y) => [y, slope * (y - 1950)]);
const names = (key, n) => Array.from({ length: n - 1 }, (_, i) => `${key}:${i + 1}`);
const wo = (...n) => FREE.filter((x) => !n.includes(x));
const Ap = (c) => { c.S.shelterW = 0.4; c.S.shelterBuild = "wage"; };
const DEC = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2024];
const BRK = [1950, 1973, 1995, 2024];
const EXP = [
  ["clock bent at 1973 and 1995", (c) => { c.S.clock = kn(BRK, -g0); return wo("g_eta").concat(names("clock", 4)); }],
  ["A' + clock bent at 1973 and 1995", (c) => { Ap(c); c.S.clock = kn(BRK, -g0); return wo("g_eta").concat(names("clock", 4)); }],
  ["A' + clock and machine labour bent at 1973, 1995", (c) => { Ap(c); c.S.clock = kn(BRK, -g0); c.S.lamk = kn(BRK, gl0);
    return wo("g_eta", "g_lam").concat(names("clock", 4), names("lamk", 4)); }],
  ["A' + clock and machine labour by decade", (c) => { Ap(c); c.S.clock = kn(DEC, -g0); c.S.lamk = kn(DEC, gl0);
    return wo("g_eta", "g_lam").concat(names("clock", 8), names("lamk", 8)); }],
  ["internet: tastes tilt from land after 1995", (c) => { c.S.tilt = [[1950, 0], [1995, 0], [2024, 0]]; return FREE.concat(["tilt:2"]); }],
  ["A' + internet tilt", (c) => { Ap(c); c.S.tilt = [[1950, 0], [1995, 0], [2024, 0]]; return FREE.concat(["tilt:2"]); }],
  ["1950 labour share pinned (k solved)", (c) => { c.S.pinLS = true; return wo("k"); }],
  ["A' + 1950 labour share pinned", (c) => { Ap(c); c.S.pinLS = true; return wo("k"); }],
];
const only = process.argv[2];
for (const [name, mod] of EXP) {
  if (only && !name.includes(only)) continue;
  const c = { S: JSON.parse(JSON.stringify(kept.settings)), par: Object.assign({}, kept.params) };
  const free = mod(c) || FREE;
  const t0 = Date.now();
  const f = M.fit(c.par, c.S, D, free, { maxIter: 800 });
  const m = M.path(f.par, f.S, D), mf = m.ok ? M.misfit(m, D) : null;
  out[name] = { misfit: mf ? mf.total : null, by: mf ? mf.by : null, par: f.par, S: f.S, k: m.k,
                ls: m.ok ? m.labour_share_c : null, eta: m.ok ? m.eta : null };
  const rates = (key, sign) => f.S[key] ? " " + key + " %/yr " + f.S[key].slice(1).map((k, i) => (sign * 100 * (k[1] - f.S[key][i][1]) / (k[0] - f.S[key][i][0])).toFixed(1)).join("/") : "";
  console.log(`${name.padEnd(48)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""} | rho ${f.par.rho.toFixed(3)} a ${f.par.a.toFixed(2)} k ${(m.k || f.par.k).toFixed(1)}${rates("clock", -1)}${rates("lamk", 1)}${f.S.tilt ? " tilt " + Math.exp(f.S.tilt[2][1]).toFixed(2) : ""} | ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  fs.writeFileSync("playground/round3.json", JSON.stringify(out, null, 1));
}
