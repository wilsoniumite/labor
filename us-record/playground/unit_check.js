// unit_check.js — is the machine's size a free unit? Scale, year by year, the machine service a task needs (eta) by c_t and
// both the hours and the land in a machine by 1/c_t: if only hours and land per unit of task capacity matter, nothing
// real moves. c_t is spiky on purpose.
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const kept = doc.presets.find((p) => p.id === "kept");
const g = kept.params.g_eta, gl = kept.params.g_lam;
const yrs = [1950, 1960, 1966, 1971, 1983, 1995, 1999, 2008, 2016, 2024];
const spike = [0, 1.7, -2.3, 3.1, -0.8, 2.4, -3.0, 1.2, -1.9, 0.6];      // log c at each year, any values
const S = Object.assign({}, kept.settings, {
  clock: yrs.map((y, i) => [y, -g * (y - 1950) + spike[i]]),
  lamk: yrs.map((y, i) => [y, gl * (y - 1950) - spike[i]]),
  bk: yrs.map((y, i) => [y, -spike[i]]) });
const base = M.misfit(M.path(kept.params, kept.settings, D), D);
const m = M.path(kept.params, S, D), mf = M.misfit(m, D);
console.log("kept model:", base.total.toFixed(6), "| machine unit rescaled with wild spikes:", m.ok ? mf.total.toFixed(6) : m.why);
const only = Object.assign({}, kept.settings, { clock: S.clock });
const m2 = M.path(kept.params, only, D);
console.log("the same spikes in the clock alone:", m2.ok ? M.misfit(m2, D).total.toFixed(2) : m2.why);
