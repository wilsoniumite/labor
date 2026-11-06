// exshelter2.js — with the goods wage read over everything but shelter, participation's rise to 1985 needs a driver
// other than the wage: women's entry as a falling cost of working until a year (her cap's story), then held.
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const alt = JSON.parse(fs.readFileSync("playground/wage_exshelter.json", "utf8")).wage_exshelter;
const D = Object.assign({}, doc.data, { wage_goods: alt });
const kept = doc.presets.find((p) => p.id === "kept");
const EX = JSON.parse(fs.readFileSync("playground/exshelter.json", "utf8"));
const FREE = ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lam"];
const K = () => JSON.parse(JSON.stringify(kept.settings));
const wn = (n, fields) => Array.from({ length: n }, (_, i) => fields.map((f) => `wave:${i}:${f}`)).flat();
const out = {};
function run(name, S, par, free) {
  let f = M.fit(par, S, D, free, { maxIter: 900 });
  let m = M.path(f.par, f.S, D);
  if (!m.ok) { const r = M.search(par, S, D, free, { maxEval: 3000 }); f = M.fit(r.par, r.S, D, free, { maxIter: 900 }); m = M.path(f.par, f.S, D); }
  const mf = m.ok ? M.misfit(m, D) : null;
  out[name] = { misfit: mf && mf.total, by: mf && mf.by, par: f.par, S: f.S };
  const chi = f.S.chi ? ` | cost of working by ${f.S.chi[1][0]}: x${Math.exp(f.S.chi[1][1]).toFixed(2)}` : "";
  const waves = (f.S.waves || []).map((w) => `${w.year}: ${w.size.toFixed(2)}/${w.tau.toFixed(0)}y`).join("; ");
  console.log(`${name.padEnd(54)} ${mf ? mf.total.toFixed(2).padStart(6) : "  none"} | ${mf ? Object.values(mf.by).map((v) => v.toFixed(1).padStart(5)).join(" ") : ""} | ` +
    `clock ${(100 * f.par.g_eta).toFixed(1)}% gλ ${(100 * f.par.g_lam).toFixed(1)}% ρ ${(100 * f.par.rho).toFixed(1)}%${chi}${waves ? " | " + waves : ""}`);
  fs.writeFileSync("playground/exshelter2.json", JSON.stringify(out, null, 1));
  return f;
}
const base = EX["all but shelter, steady clock"];
console.log("columns: total | goods wage (all but shelter), shelter wage, labour share, prime-age employment, theta_V");
for (const until of [1980, 1990]) {
  run(`women's entry until ${until}`, Object.assign(K(), { chi: [[1950, 0], [until, 0]] }), base.par, FREE.concat(["chi:1"]));
}
const wv = EX["all but shelter, dated waves 1948 and 1995"];
run("women's entry until 1985 + dated waves", Object.assign(JSON.parse(JSON.stringify(wv.S)), { chi: [[1950, 0], [1985, 0]] }), wv.par, FREE.concat(["chi:1"], wn(2, ["size", "tau"])));
run("women's entry until 1985, no cap", Object.assign(K(), { chi: [[1950, 0], [1985, 0]], cap: null }), base.par, FREE.concat(["chi:1"]));
