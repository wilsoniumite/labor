// waves_look.js — her spiky settings of 2026-11-06 (playground/her_spiky.json), solved as pasted.
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
const her = JSON.parse(fs.readFileSync("playground/her_spiky.json", "utf8"));
const m = M.path(her.params, her.settings, D);
const mf = M.misfit(m, D);
console.log("her settings:", m.ok ? "every year solves" : m.why, "| misfit", mf.total.toFixed(2), "|",
  Object.entries(mf.by).map(([k, v]) => `${k} ${v.toFixed(1)}`).join(", "));
const at = (y) => D.years.indexOf(y);
const yrs = [1950, 1960, 1965, 1968, 1970, 1975, 1985, 1995, 1997, 1999, 2005, 2015, 2024];
console.log("year  clock(eta)  hours/machine  hours/task  land/machine  tasks by machine  wage(land units)  land share of machine cost  machine-making hours");
for (const y of yrs) {
  const i = at(y), a = m.an;
  console.log(String(y).padEnd(6), m.eta[i].toExponential(2).padStart(10), (a.lam[i] / a.lam[0]).toExponential(2).padStart(13),
    (a.lam[i] * m.eta[i] / a.lam[0]).toExponential(2).padStart(11), (a.b[i] / a.b[0]).toExponential(2).padStart(13),
    (1 - a.peopleTasks[i]).toFixed(3).padStart(17), m.v[i].toExponential(2).padStart(17), a.sigmaV[i].toFixed(3).padStart(27), a.hoursMachine[i].toFixed(3).padStart(21));
}
