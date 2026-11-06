// explore2.js — four questions while she is away (2026-11-06):
//  A. what would it take to fit labour's share? the kept model refitted with that series weighted up
//  B. waves on defensible numbers: the return at 2% and a from the measured machine-cost split, with dated waves
//  C. her developer story: at each dated wave, a surge in the hours to build machines that peaks and fades
//  D. is the early burst real? one free-dated wave under variations of the setup
// Run from us-record/: node playground/explore2.js [A|B|C|D]
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const R5 = JSON.parse(fs.readFileSync("playground/round5.json", "utf8"));
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const K = () => JSON.parse(JSON.stringify(kept.settings));
const wn = (n, fields) => Array.from({ length: n }, (_, i) => fields.map((f) => `wave:${i}:${f}`)).flat();
const out = fs.existsSync("playground/explore2.json") ? JSON.parse(fs.readFileSync("playground/explore2.json", "utf8")) : {};
const at = (y) => D.years.indexOf(y);
function fitRun(name, S, par, free, maxIter = 700) {
  let f = M.fit(par, S, D, free, { maxIter });
  let m = M.path(f.par, f.S, D);
  if (!m.ok) { const r = M.search(par, S, D, free, { maxEval: 3000 }); f = M.fit(r.par, r.S, D, free, { maxIter }); m = M.path(f.par, f.S, D); }
  const mf = m.ok ? M.misfit(m, D) : null;
  out[name] = { misfit: mf && mf.total, by: mf && mf.by, par: f.par, S: f.S };
  fs.writeFileSync("playground/explore2.json", JSON.stringify(out, null, 1));
  return { f, m, mf };
}
function line(name, r, extra = "") {
  const { f, m, mf } = r;
  if (!mf) { console.log(name.padEnd(52), "no equilibrium"); return; }
  const waves = (f.S.waves || []).map((w) => `${w.year.toFixed(0)}: ${w.size.toFixed(2)}/${w.tau.toFixed(0)}y` + (w.hours ? ` hours ${w.hours >= 0 ? "+" : ""}${w.hours.toFixed(2)} at +${(w.htau || w.tau).toFixed(0)}y` : "")).join("; ");
  console.log(`${name.padEnd(52)} ${mf.total.toFixed(2).padStart(6)} | ${Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ")} | ` +
    `clock ${(100 * f.par.g_eta).toFixed(1)}% gλ ${(100 * f.par.g_lam).toFixed(1)}% a ${f.par.a.toFixed(2)} ρ ${(100 * f.par.rho).toFixed(1)}% k ${f.par.k.toFixed(1)}` +
    (waves ? ` | ${waves}` : "") + extra);
}
const which = process.argv[2] || "ABCD";
console.log("columns: total | wage durables, wage shelter, labour share, prime-age employment, theta_V (unweighted)");
if (which.includes("A")) {
  console.log("-- A: labour's share weighted up");
  for (const w of [1, 3, 10, 30]) {
    const S = Object.assign(K(), { fitWeights: { series: { labour_share_c: w } } });
    const r = fitRun(`A steady clock, labour share x${w}`, S, kept.params, FREE);
    const a = r.m.an;
    line(`steady clock, labour's share weighted x${w}`, r, ` | machines do ${(100 * (1 - a.peopleTasks[0])).toFixed(0)}% of tasks in 1950, ${(100 * (1 - a.peopleTasks[74])).toFixed(0)}% in 2024`);
  }
  for (const w of [1, 10]) {
    const S = Object.assign(K(), { fitWeights: { series: { labour_share_c: w } }, waves: [1948, 1995].map((y) => ({ year: y, size: 0.05, tau: 15 })) });
    line(`dated waves, labour's share weighted x${w}`, fitRun(`A dated waves, labour share x${w}`, S, kept.params, FREE.concat(wn(2, ["size", "tau"]))));
  }
}
if (which.includes("B")) {
  console.log("-- B: the return at 2%, a from the measured split (machine services 0.20 of a machine's cost in 2023)");
  const par = Object.assign({}, R5.set_a_rho);
  const free = ["T", "h", "k", "g_eta", "lam0", "g_lam"];
  line("measured shares, steady clock", fitRun("B measured, steady", K(), par, free));
  line("measured shares, post-war 1948 wave", fitRun("B measured, 1948", Object.assign(K(), { waves: [{ year: 1948, size: 0.05, tau: 15 }] }), par, free.concat(wn(1, ["size", "tau"]))));
  line("measured shares, dated waves 1948 and 1995", fitRun("B measured, 1948 1995", Object.assign(K(), { waves: [1948, 1995].map((y) => ({ year: y, size: 0.05, tau: 15 })) }), par, free.concat(wn(2, ["size", "tau"]))));
}
if (which.includes("C")) {
  console.log("-- C: hours surges at the dated waves (her developer story)");
  const base = Object.assign(K(), { waves: [1948, 1995].map((y) => ({ year: y, size: 0.05, tau: 15 })) });
  const r0 = fitRun("C dated waves", JSON.parse(JSON.stringify(base)), kept.params, FREE.concat(wn(2, ["size", "tau"])));
  line("dated waves, no surge", r0);
  const S1 = JSON.parse(JSON.stringify(r0.f.S)); S1.waves.forEach((w) => { w.hours = 0.05; w.htau = 8; });
  line("dated waves, hours surges free", fitRun("C dated waves + surges", S1, r0.f.par, FREE.concat(wn(2, ["size", "tau", "hours", "htau"]))));
  const S2 = JSON.parse(JSON.stringify(R5.set_a_rho ? base : base));
  S2.waves.forEach((w) => { w.hours = 0.05; w.htau = 8; });
  line("measured shares, dated waves with surges", fitRun("C measured + waves + surges", S2, Object.assign({}, R5.set_a_rho), ["T", "h", "k", "g_eta", "lam0", "g_lam"].concat(wn(2, ["size", "tau", "hours", "htau"]))));
}
if (which.includes("D")) {
  console.log("-- D: one wave, its date free (started at 1960), under variations");
  const W = () => [{ year: 1960, size: 0.3, tau: 12 }];
  const f1 = FREE.concat(wn(1, ["size", "tau", "year"]));
  line("kept setup", fitRun("D kept", Object.assign(K(), { waves: W() }), kept.params, f1));
  line("start not pinned", fitRun("D not pinned", Object.assign(K(), { waves: W(), pin: false }), kept.params, f1.concat(["chi_max"])));
  line("years before 1956 not counted", fitRun("D from 1956", Object.assign(K(), { waves: W(), fitWeights: { from: 1956 } }), kept.params, f1));
  line("labour's share not counted", fitRun("D no labour share", Object.assign(K(), { waves: W(), fitWeights: { series: { labour_share_c: 0 } } }), kept.params, f1));
  line("employment not counted", fitRun("D no employment", Object.assign(K(), { waves: W(), fitWeights: { series: { prime_emp_rate: 0 } } }), kept.params, f1));
  line("started at 1975 instead", fitRun("D start 1975", Object.assign(K(), { waves: [{ year: 1975, size: 0.3, tau: 12 }] }), kept.params, f1));
}
