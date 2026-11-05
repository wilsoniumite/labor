// land_check.js — how much land the fitted baskets hold: the site's share of a basket's cost and of all land.
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const D = doc.data;
function show(label, par, S) {
  const m = M.path(par, S, D);
  if (!m.ok) { console.log(label, "no path"); return; }
  const at = (y) => D.years.indexOf(y);
  const share = (y) => (m.site_basket[at(y)] / m.Ps[at(y)]).toExponential(2);
  console.log(label.padEnd(26), "site share of a basket's cost: 1950", share(1950), " 1970", share(1970), " 2024", share(2024));
}
const kept = doc.presets.find((p) => p.id === "kept");
show("kept", kept.params, kept.settings);
const R3 = JSON.parse(fs.readFileSync("playground/round3.json", "utf8"));
const t = R3["internet: tastes tilt from land after 1995"];
show("internet tilt", t.par, t.S);
