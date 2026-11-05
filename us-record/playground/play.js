// play.js — cheap experiments on the backward model (her request, 2026-11-05: "play around with the model, try lots
// and lots of stuff cheaply"). Each experiment changes one thing from the kept model (cap, basket, pinned start) and
// refits the free numbers from the kept fit with the explorer's fitter (explorer/model.js), one start, no validation
// beyond the fit itself. Results: playground/results.json; a reading in docs/playground.md.
// Run from us-record/:  node playground/play.js [filter]
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const rw = (y) => D.real_wage_cpi[D.years.indexOf(y)];
const g0 = kept.params.g_eta, gl0 = kept.params.g_lam;
const without = (...names) => FREE.filter((n) => !names.includes(n));

const EXP = [
  ["kept, refit from itself", () => {}],
  ...[0.04, 0.06, 0.08, 0.10, 0.13, 0.16].map((g) => [`clock pace fixed at ${(g * 100).toFixed(0)}%`, (c) => { c.par.g_eta = g; return without("g_eta"); }]),
  ...[0.03, 0.06, 0.10].map((r) => [`required return fixed at ${(r * 100).toFixed(0)}%`, (c) => { c.par.rho = r; return without("rho"); }]),
  ["machine services in a machine fixed at 1", (c) => { c.par.a = 1; return without("a"); }],
  ["bendable clock (points 1970, 1990, 2010, 2024)", (c) => {
    c.S.clock = [1950, 1970, 1990, 2010, 2024].map((y) => [y, -g0 * (y - 1950)]);
    return without("g_eta").concat(["clock:1", "clock:2", "clock:3", "clock:4"]); }],
  ...[0.5, 1.0, 1.2].map((sg) => [`basket elasticity ${sg}`, (c) => { c.S.sigma = sg; }]),
  ["utility flat from 1950", (c) => { c.S.utility = [[1950, 1]]; }],
  ["utility rising all along at its 1950-70 pace", (c) => { c.S.utility = [[1950, 1], [2024, Math.pow(rw(1970), 74 / 20)]]; }],
  ["utility kinked at 1973 (the real wage's peak)", (c) => { c.S.utility = [[1950, 1], [1973, rw(1973)]]; }],
  ["utility is the real wage, every year", (c) => { c.S.utility = D.years.map((y) => [y, rw(y)]); }],
  ...[0.80, 0.815].map((cp) => [`cap at ${cp}`, (c) => { c.S.cap = cp; }]),
  ["no cap", (c) => { c.S.cap = null; }],
  ["no basket", (c) => { c.S.sigma = null; }],
  ["start not pinned", (c) => { c.S.pin = false; c.par.chi_max = 1.027; return FREE.concat(["chi_max"]); }],
  ["women's entry: the cost of working falls to 1985, held after", (c) => {
    c.S.chi = [[1950, 0], [1985, 0]]; return FREE.concat(["chi:1"]); }],
  ["land expanding to 1970, held after (suburbs)", (c) => { c.S.land = [[1950, 0], [1970, 0]]; return FREE.concat(["land:1"]); }],
  ["land path bent at 1970 and 2024", (c) => { c.S.land = [[1950, 0], [1970, 0], [2024, 0]]; return FREE.concat(["land:1", "land:2"]); }],
  ["machine-making labour bendable (1970, 1990, 2010, 2024)", (c) => {
    c.S.lamk = [1950, 1970, 1990, 2010, 2024].map((y) => [y, gl0 * (y - 1950)]);
    return without("g_lam").concat(["lamk:1", "lamk:2", "lamk:3", "lamk:4"]); }],
  ["A' (shelter's building priced at the wage, site 0.4)", (c) => { c.S.shelterW = 0.4; c.S.shelterBuild = "wage"; }],
  ["A (shelter's building priced like durables, site 0.4)", (c) => { c.S.shelterW = 0.4; }],
  ["return follows the real rate (premium fitted)", (c) => { c.S.rhoData = 1; c.par.rho = 0.02; }],
  ["return follows half the real rate", (c) => { c.S.rhoData = 0.5; c.par.rho = 0.02; }],
];

const filter = process.argv[2];
const out = fs.existsSync("playground/results.json") ? JSON.parse(fs.readFileSync("playground/results.json", "utf8")) : {};
for (const [name, mod] of EXP) {
  if (filter && !name.includes(filter)) continue;
  const c = { S: JSON.parse(JSON.stringify(kept.settings)), par: Object.assign({}, kept.params) };
  const free = mod(c) || FREE;
  const t0 = Date.now();
  const start = M.path(c.par, c.S, D);
  const f = M.fit(c.par, c.S, D, free, { maxIter: 600 });
  const m = M.path(f.par, f.S, D);
  const mf = m.ok ? M.misfit(m, D) : null;
  const row = { misfit: mf ? mf.total : null, by: mf ? mf.by : null, par: f.par, S: f.S, iters: f.iters,
                seconds: (Date.now() - t0) / 1000, start_ok: start.ok };
  out[name] = row;
  const by = mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : "";
  console.log(`${name.padEnd(62)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${by} | rho ${f.par.rho.toFixed(3)} clock ${(f.par.g_eta * 100).toFixed(1)}% a ${f.par.a.toFixed(2)} k ${f.par.k.toFixed(1)} | ${row.seconds.toFixed(0)}s`);
  fs.writeFileSync("playground/results.json", JSON.stringify(out, null, 1));
}
