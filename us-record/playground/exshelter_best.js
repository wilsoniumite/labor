// exshelter_best.js — the all-but-shelter + women's entry fit (per-task hours growth), saved for the explorer's preset.
const fs = require("fs");
const M = require("../explorer/model.js");
const doc = JSON.parse(fs.readFileSync("explorer/data.json", "utf8"));
const alt = JSON.parse(fs.readFileSync("playground/wage_exshelter.json", "utf8")).wage_exshelter;
const D = Object.assign({}, doc.data, { wage_goods: alt });
const best = JSON.parse(fs.readFileSync("playground/exshelter2.json", "utf8"))["women's entry until 1990"];
const S = Object.assign(JSON.parse(JSON.stringify(best.S)), { coords: { land: "Th", machine: "a", labour: "task" }, goods: "exshelter" });
const f = M.fit(best.par, S, D, ["T", "h", "a", "k", "rho", "g_eta", "lam0", "g_lamTask", "chi:1"], { maxIter: 1200 });
const mf = M.misfit(M.path(f.par, f.S, D), D);
fs.writeFileSync("playground/exshelter_best.json", JSON.stringify({ "all but shelter, women's entry to 1990": { misfit: mf.total, by: mf.by, par: f.par, S: f.S } }, null, 1));
console.log("saved:", mf.total.toFixed(3));
