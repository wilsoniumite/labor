// profiles.js — fixed-number profiles by continuation: walk one number from the kept fit's value to each target in
// small steps, refitting the rest at every step from the step before (a start far from the kept fit often has no
// equilibrium, and the fitter cannot leave such a start). Also combinations of the first batch's better ideas.
// Run from us-record/:  node playground/profiles.js
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const out = fs.existsSync("playground/profiles.json") ? JSON.parse(fs.readFileSync("playground/profiles.json", "utf8")) : {};
const fmtBy = (mf) => (mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : "");

function walk(label, key, targets, setFixed, freeNames, Sbase) {
  let par = Object.assign({}, kept.params), S = Sbase || JSON.parse(JSON.stringify(kept.settings));
  let curVal = key === "rhoData" ? 0 : par[key];
  const rows = [];
  for (const target of targets) {
    const steps = Math.max(1, Math.ceil(Math.abs(target - curVal) / (Math.abs(targets[targets.length - 1] - curVal) / 12 || 1)));
    for (let s = 1; s <= steps; s++) {
      const v = curVal + (target - curVal) * s / steps;
      setFixed(par, S, v);
      const f = M.fit(par, S, D, freeNames, { maxIter: 300 });
      const m = M.path(f.par, f.S, D);
      if (!m.ok) { rows.push({ v, misfit: null }); break; }
      par = f.par; S = f.S;
    }
    curVal = target;
    const m = M.path(par, S, D), mf = m.ok ? M.misfit(m, D) : null;
    rows.push({ v: target, misfit: mf ? mf.total : null, by: mf ? mf.by : null, par: Object.assign({}, par) });
    console.log(`${label.padEnd(30)} ${String(target).padEnd(6)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${fmtBy(mf)} | rho ${par.rho.toFixed(3)} clock ${(par.g_eta * 100).toFixed(1)}% a ${par.a.toFixed(2)} k ${par.k.toFixed(1)} lam ${par.lam0.toPrecision(3)} glam ${(par.g_lam * 100).toFixed(1)}%`);
  }
  out[label] = rows;
  fs.writeFileSync("playground/profiles.json", JSON.stringify(out, null, 1));
}

const only = process.argv[2];
if (!only || only === "clock") {
  walk("clock pace, falling", "g_eta", [0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04], (p, S, v) => { p.g_eta = v; }, FREE.filter((n) => n !== "g_eta"));
  walk("clock pace, rising", "g_eta", [0.12, 0.13, 0.14, 0.16, 0.18], (p, S, v) => { p.g_eta = v; }, FREE.filter((n) => n !== "g_eta"));
}
if (!only || only === "rho") {
  walk("required return", "rho", [0.01, 0.02, 0.03, 0.05, 0.07, 0.10], (p, S, v) => { p.rho = v; }, FREE.filter((n) => n !== "rho"));
}
if (!only || only === "rate") {
  walk("real-rate pass-through", "rhoData", [0.1, 0.25, 0.5, 0.75, 1.0], (p, S, v) => { S.rhoData = v; }, FREE);
}
if (!only || only === "a") {
  walk("machine services a", "a", [7, 5, 3, 2, 1, 0.5], (p, S, v) => { p.a = v; }, FREE.filter((n) => n !== "a"));
}
