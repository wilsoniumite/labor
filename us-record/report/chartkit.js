// chartkit.js — the reports' chart kit (line, stack, heat, dot and split charts with hover, keyboard and table views),
// inlined into report/page.html and report/misses_page.html by their builders. Depends on nothing; the pages' CSS styles it.
function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
function esc(s) { return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
const ok = (v) => v !== null && v !== undefined && isFinite(v);
function fmt(v, d = 2) { if (!ok(v)) return "–"; const a = Math.abs(v);
  if (a >= 1000) return v.toLocaleString("en-US", { maximumFractionDigits: 0 });
  if (a >= 100) return v.toFixed(Math.min(d, 1)); if (a >= 10) return v.toFixed(Math.min(d, 2));
  if (a === 0) return "0"; if (a < 0.001) return v.toExponential(1); return v.toFixed(d + (a < 0.1 ? 1 : 0)); }
function fmtTick(v) { const a = Math.abs(v); if (a === 0) return "0"; if (a >= 1000) return v.toLocaleString("en-US");
  if (a >= 10) return String(Math.round(v * 100) / 100); if (a >= 1) return String(+v.toFixed(2)); if (a >= 0.01) return String(+v.toFixed(3));
  return v >= 1e-4 ? String(+v.toFixed(5)) : v.toExponential(0); }
const scale100 = (arr, base) => arr.map((v) => (ok(v) ? 100 * v / base : null));
const index1 = (arr, i0 = 0) => arr.map((v) => (ok(v) && ok(arr[i0]) ? v / arr[i0] : null));

// ------------------------------------------------------------------------------------------------- the chart kit
function niceStep(span, n) { const raw = span / Math.max(1, n), mag = Math.pow(10, Math.floor(Math.log10(raw))), r = raw / mag;
  return (r >= 7.5 ? 10 : r >= 3.5 ? 5 : r >= 1.5 ? 2 : 1) * mag; }
function linTicks(lo, hi, n) { const st = niceStep(hi - lo, n), out = [];
  for (let v = Math.ceil(lo / st - 1e-9) * st; v <= hi + st * 1e-9; v += st) out.push(Math.abs(v) < st * 1e-9 ? 0 : +v.toPrecision(12)); return out; }
function logTicks(lo, hi) { if (hi / lo < 3.2) return linTicks(lo, hi, 4).filter((v) => v > 0);
  const e0 = Math.floor(Math.log10(lo)), e1 = Math.ceil(Math.log10(hi)), span = e1 - e0, out = [];
  const ms = span > 5 ? [1] : span > 2 ? [1, 3] : [1, 2, 5];
  for (let e = e0; e <= e1; e++) for (const m of ms) { const v = m * Math.pow(10, e); if (v >= lo && v <= hi) out.push(+v.toPrecision(6)); }
  if (span > 7) return out.filter((v, i) => i % 2 === 0);
  if (out.length < 2) return linTicks(lo, hi, 3).filter((v) => v > 0); return out; }
function segments(n, good) { const out = []; let cur = [];
  for (let i = 0; i < n; i++) { if (good(i)) cur.push(i); else if (cur.length) { out.push(cur); cur = []; } } if (cur.length) out.push(cur); return out; }
function observe(node, fn) { let t = null, w = node.clientWidth;
  new ResizeObserver(() => { if (Math.abs(node.clientWidth - w) < 2) return; w = node.clientWidth; clearTimeout(t); t = setTimeout(fn, 60); }).observe(node); }

function legend(items) { const lg = el("div", "legend");
  for (const it of items) { const s = el("span"); const k = el("span", "key" + (it.kind ? " " + it.kind : ""));
    k.style.background = it.color; s.append(k, document.createTextNode(it.label)); lg.append(s); } return lg; }

function figure(parent, { title, note, wide }) {
  const f = el("figure"); if (wide) f.classList.add("wide");
  const cap = el("figcaption"); cap.append(el("p", "ft", title)); if (note) cap.append(el("p", "fn", note));
  f.append(cap); const body = el("div"); f.append(body); parent.append(f); return body;
}

function numbersTable(host, xs, cols, rows) {
  const d = el("details", "nums"); d.append(el("summary", null, "Numbers"));
  const w = el("div", "tablewrap"), t = el("table"), hr = el("tr");
  hr.append(el("th", null, "")); cols.forEach((c) => hr.append(el("th", null, c.label))); t.append(hr);
  rows.forEach((i) => { const tr = el("tr"); tr.append(el("td", null, String(xs[i])));
    cols.forEach((c) => tr.append(el("td", null, c.fmt ? c.fmt(c.values[i]) : fmt(c.values[i], 3)))); t.append(tr); });
  w.append(t); d.append(w); host.append(d);
}
function defaultRows(xs, cols) { const out = [];
  xs.forEach((x, i) => { if (typeof x === "number" && x % 10 === 0 && cols.some((c) => ok(c.values[i]))) out.push(i); });
  let last = -1; xs.forEach((x, i) => { if (cols.some((c) => ok(c.values[i]))) last = i; });
  if (last >= 0 && !out.includes(last)) out.push(last); return out.length ? out : xs.map((_, i) => i); }

function lineChart(host, spec) {
  host.innerHTML = "";
  const xs = spec.x, ser = spec.series;
  const items = ser.filter((s) => !s.noLegend).map((s) => ({ label: s.label, color: s.color, kind: s.dots ? "dot" : s.width && s.width < 1.5 ? "thin" : "" }));
  ser.forEach((s) => { if (s.band && s.bandLabel) items.push({ label: s.bandLabel, color: "var(--band)", kind: "wash" }); });
  (spec.points || []).forEach((p) => { if (p.legend) items.push({ label: p.legend, color: p.color || "var(--ink)", kind: "dot" }); });
  if (items.length > 1 || spec.forceLegend) host.append(legend(items));
  const plot = el("div", "plot"); host.append(plot);
  const tip = el("div", "tip"); tip.hidden = true; plot.append(tip);
  let cur = null;
  const draw = () => {
    const W = Math.max(260, Math.round(plot.clientWidth || 560)), H = spec.height || 210;
    const ml = spec.ml || 44, mr = 12, mt = 12, mb = 24;
    const x0 = spec.xMin ?? xs[0], x1 = spec.xMax ?? xs[xs.length - 1];
    const inX = (i) => xs[i] >= x0 && xs[i] <= x1;
    const good = (v) => ok(v) && (!spec.log || v > 0);
    const vals = [];
    ser.forEach((s) => { s.values.forEach((v, i) => { if (good(v) && inX(i)) vals.push(v); });
      if (s.band) ["lo", "hi"].forEach((k) => s.band[k].forEach((v, i) => { if (good(v) && inX(i)) vals.push(v); })); });
    (spec.points || []).forEach((p) => vals.push(p.y)); (spec.refs || []).forEach((r) => vals.push(r.y));
    let lo = spec.yMin ?? Math.min(...vals), hi = spec.yMax ?? Math.max(...vals);
    if (spec.log) { if (spec.yMin == null) lo /= 1.08; if (spec.yMax == null) hi *= 1.08; }
    else { const pad = (hi - lo) * 0.07 || Math.abs(hi) * 0.1 || 1; if (spec.yMin == null) lo -= pad; if (spec.yMax == null) hi += pad; }
    const X = (x) => ml + (x - x0) / (x1 - x0) * (W - ml - mr);
    const Y = spec.log ? (y) => mt + (Math.log(hi) - Math.log(y)) / (Math.log(hi) - Math.log(lo)) * (H - mt - mb)
                       : (y) => mt + (hi - y) / (hi - lo) * (H - mt - mb);
    let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" tabindex="0" aria-label="${esc(spec.aria || "")}">`;
    (spec.shade ? [].concat(spec.shade) : []).forEach((sh) => { const a = X(Math.max(x0, sh.from)), b = X(Math.min(x1, sh.to));
      s += `<rect x="${a}" y="${mt}" width="${Math.max(0, b - a)}" height="${H - mt - mb}" class="shade"/>`;
      if (sh.label) s += `<text x="${a + 5}" y="${mt + 12}" class="shade-label">${esc(sh.label)}</text>`; });
    const yt = spec.log ? logTicks(lo, hi) : linTicks(lo, hi, spec.yTicks || 4);
    yt.forEach((v) => { const y = Y(v); s += `<line x1="${ml}" x2="${W - mr}" y1="${y}" y2="${y}" class="grid"/>` +
      `<text x="${ml - 6}" y="${y + 3.5}" class="tick" text-anchor="end">${esc(spec.yFmt ? spec.yFmt(v) : fmtTick(v))}</text>`; });
    const xt = spec.xTicks || linTicks(x0, x1, W < 420 ? 4 : 7).filter((v) => v >= x0 && v <= x1);
    xt.forEach((v) => { const x = X(v); s += `<line x1="${x}" x2="${x}" y1="${H - mb}" y2="${H - mb + 4}" class="axis"/>` +
      `<text x="${x}" y="${H - 7}" class="tick" text-anchor="middle">${esc(spec.xFmt ? spec.xFmt(v) : String(v))}</text>`; });
    s += `<line x1="${ml}" x2="${W - mr}" y1="${H - mb}" y2="${H - mb}" class="axis"/>`;
    (spec.refs || []).forEach((r) => { const y = Y(r.y); s += `<line x1="${ml}" x2="${W - mr}" y1="${y}" y2="${y}" class="ref"/>`;
      if (r.label) s += `<text x="${ml + 6}" y="${y - 5}" class="ref-label">${esc(r.label)}</text>`; });
    (spec.vlines || []).forEach((vl) => { const x = X(vl.x); s += `<line x1="${x}" x2="${x}" y1="${mt}" y2="${H - mb}" class="vline"/>`;
      if (vl.label) s += `<text x="${x + 5}" y="${mt + 12}" class="shade-label">${esc(vl.label)}</text>`; });
    ser.forEach((se) => { if (!se.band) return;
      segments(xs.length, (i) => good(se.band.lo[i]) && good(se.band.hi[i]) && inX(i)).forEach((seg) => {
        const top = seg.map((i) => `${X(xs[i]).toFixed(1)},${Y(se.band.hi[i]).toFixed(1)}`);
        const bot = seg.slice().reverse().map((i) => `${X(xs[i]).toFixed(1)},${Y(se.band.lo[i]).toFixed(1)}`);
        s += `<polygon points="${top.concat(bot).join(" ")}" style="fill:var(--band)"/>`; }); });
    ser.forEach((se) => { if (se.dots) return;
      segments(xs.length, (i) => good(se.values[i]) && inX(i)).forEach((seg) => {
        if (seg.length === 1) { const i = seg[0]; s += `<circle cx="${X(xs[i])}" cy="${Y(se.values[i])}" r="2.5" style="fill:${se.color}"/>`; return; }
        s += `<path d="M${seg.map((i) => `${X(xs[i]).toFixed(1)},${Y(se.values[i]).toFixed(1)}`).join("L")}" class="line" style="stroke:${se.color};stroke-width:${se.width || 2}"/>`; }); });
    ser.forEach((se) => { if (!se.dots) return;
      se.values.forEach((v, i) => { if (!good(v) || !inX(i)) return;
        s += `<circle cx="${X(xs[i]).toFixed(1)}" cy="${Y(v).toFixed(1)}" r="4" class="dot" style="fill:${se.color}"/>`; }); });
    (spec.points || []).forEach((p) => { s += `<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="5" class="anchor" style="fill:${p.color || "var(--ink)"}"/>`;
      if (p.label) s += `<text x="${X(p.x) - 9}" y="${Y(p.y) + 4}" class="pt-label" text-anchor="end">${esc(p.label)}</text>`; });
    s += `<line class="cross" x1="0" x2="0" y1="${mt}" y2="${H - mb}" visibility="hidden"/>`;
    s += `<rect class="hit" x="${ml}" y="${mt}" width="${W - ml - mr}" height="${H - mt - mb}"/></svg>`;
    plot.querySelector("svg")?.remove(); plot.insertAdjacentHTML("afterbegin", s);
    const svg = plot.querySelector("svg"), cross = svg.querySelector(".cross");
    const valid = xs.map((_, i) => inX(i) && ser.some((se) => good(se.values[i])));
    const show = (i) => {
      if (i == null) return; cur = i; const x = X(xs[i]);
      cross.setAttribute("x1", x); cross.setAttribute("x2", x); cross.setAttribute("visibility", "visible");
      tip.replaceChildren(); tip.append(el("div", "th", spec.xFmt ? spec.xFmt(xs[i]) : String(xs[i])));
      ser.forEach((se) => { const v = se.values[i]; if (!ok(v)) return; const r = el("div", "tr"), k = el("span", "key" + (se.dots ? " dot" : ""));
        k.style.background = se.color; r.append(k, el("b", null, se.fmt ? se.fmt(v) : fmt(v, spec.digits ?? 3)), el("i", null, se.label)); tip.append(r); });
      tip.hidden = false; const pw = plot.clientWidth, tw = tip.offsetWidth, px = x / W * pw;
      tip.style.left = (px + 14 + tw > pw ? Math.max(4, px - 14 - tw) : px + 14) + "px";
    };
    const hide = () => { cross.setAttribute("visibility", "hidden"); tip.hidden = true; };
    const nearest = (xv) => { let b = null, bd = Infinity; xs.forEach((x, i) => { if (!valid[i]) return; const d = Math.abs(x - xv); if (d < bd) { bd = d; b = i; } }); return b; };
    svg.addEventListener("pointermove", (ev) => { const r = svg.getBoundingClientRect(); const px = (ev.clientX - r.left) * W / r.width;
      show(nearest(x0 + (px - ml) / (W - ml - mr) * (x1 - x0))); });
    svg.addEventListener("pointerleave", hide); svg.addEventListener("blur", hide);
    svg.addEventListener("focus", () => show(cur ?? valid.lastIndexOf(true)));
    svg.addEventListener("keydown", (ev) => { if (ev.key !== "ArrowLeft" && ev.key !== "ArrowRight") return; ev.preventDefault();
      let i = cur ?? valid.lastIndexOf(true); const step = ev.key === "ArrowLeft" ? -1 : 1;
      do { i += step; } while (i >= 0 && i < xs.length && !valid[i]); if (i >= 0 && i < xs.length) show(i); });
  };
  draw(); observe(plot, draw);
  if (spec.table !== false) { const cols = ser.filter((s) => !s.noTable).map((s) => ({ label: s.label, values: s.values, fmt: s.fmt }));
    numbersTable(host, xs, cols, spec.tableRows || defaultRows(xs, cols)); }
}

function stackChart(host, spec) {
  host.innerHTML = ""; const xs = spec.x, layers = spec.layers;
  host.append(legend(layers.map((l) => ({ label: l.label, color: l.color, kind: "wash" }))));
  const plot = el("div", "plot"); host.append(plot); const tip = el("div", "tip"); tip.hidden = true; plot.append(tip);
  const draw = () => {
    const W = Math.max(260, Math.round(plot.clientWidth || 560)), H = spec.height || 210, ml = 40, mr = 12, mt = 12, mb = 24;
    const x0 = xs[0], x1 = xs[xs.length - 1], X = (x) => ml + (x - x0) / (x1 - x0) * (W - ml - mr), Y = (y) => mt + (1 - y) * (H - mt - mb);
    let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" tabindex="0" aria-label="${esc(spec.aria || "")}">`;
    const base = xs.map(() => 0);
    layers.forEach((l) => { const top = xs.map((_, i) => base[i] + (ok(l.values[i]) ? l.values[i] : 0));
      const pts = xs.map((x, i) => `${X(x).toFixed(1)},${Y(top[i]).toFixed(1)}`).concat(xs.slice().reverse().map((x, j) => { const i = xs.length - 1 - j; return `${X(x).toFixed(1)},${Y(base[i]).toFixed(1)}`; }));
      s += `<polygon points="${pts.join(" ")}" style="fill:${l.color};stroke:var(--surface);stroke-width:1.5"/>`;
      top.forEach((v, i) => { base[i] = v; }); });
    [0, 0.25, 0.5, 0.75, 1].forEach((v) => { s += `<text x="${ml - 6}" y="${Y(v) + 3.5}" class="tick" text-anchor="end">${v}</text>`; });
    linTicks(x0, x1, W < 420 ? 4 : 7).forEach((v) => { if (v < x0 || v > x1) return; s += `<text x="${X(v)}" y="${H - 7}" class="tick" text-anchor="middle">${v}</text>`; });
    s += `<line class="cross" x1="0" x2="0" y1="${mt}" y2="${H - mb}" visibility="hidden"/><rect class="hit" x="${ml}" y="${mt}" width="${W - ml - mr}" height="${H - mt - mb}"/></svg>`;
    plot.querySelector("svg")?.remove(); plot.insertAdjacentHTML("afterbegin", s);
    const svg = plot.querySelector("svg"), cross = svg.querySelector(".cross");
    const show = (i) => { const x = X(xs[i]); cross.setAttribute("x1", x); cross.setAttribute("x2", x); cross.setAttribute("visibility", "visible");
      tip.replaceChildren(); tip.append(el("div", "th", String(xs[i])));
      layers.slice().reverse().forEach((l) => { const r = el("div", "tr"), k = el("span", "key wash"); k.style.background = l.color;
        r.append(k, el("b", null, fmt(l.values[i], 3)), el("i", null, l.label)); tip.append(r); });
      tip.hidden = false; const pw = plot.clientWidth, tw = tip.offsetWidth, px = x / W * pw; tip.style.left = (px + 14 + tw > pw ? Math.max(4, px - 14 - tw) : px + 14) + "px"; };
    let cur = xs.length - 1;
    svg.addEventListener("pointermove", (ev) => { const r = svg.getBoundingClientRect(); const px = (ev.clientX - r.left) * W / r.width;
      cur = Math.max(0, Math.min(xs.length - 1, Math.round(x0 + (px - ml) / (W - ml - mr) * (x1 - x0) - x0))); show(cur); });
    const hide = () => { cross.setAttribute("visibility", "hidden"); tip.hidden = true; };
    svg.addEventListener("pointerleave", hide); svg.addEventListener("blur", hide); svg.addEventListener("focus", () => show(cur));
    svg.addEventListener("keydown", (ev) => { if (ev.key === "ArrowLeft" && cur > 0) { cur--; show(cur); ev.preventDefault(); }
      if (ev.key === "ArrowRight" && cur < xs.length - 1) { cur++; show(cur); ev.preventDefault(); } });
  };
  draw(); observe(plot, draw);
  const cols = layers.map((l) => ({ label: l.label, values: l.values })); numbersTable(host, xs, cols, defaultRows(xs, cols));
}

function heatStrip(host, spec) {
  host.innerHTML = ""; const xs = spec.x, rows = spec.rows, clamp = spec.clamp || 3;
  const lg = el("div", "legend"); [["model below the record", "var(--heat-neg)"], ["on the record", "var(--heat-mid)"], ["model above", "var(--heat-pos)"]]
    .forEach(([t, c]) => { const s = el("span"), k = el("span", "key wash"); k.style.background = c; s.append(k, document.createTextNode(t)); lg.append(s); });
  host.append(lg);
  const plot = el("div", "plot"); host.append(plot); const tip = el("div", "tip"); tip.hidden = true; plot.append(tip);
  const draw = () => {
    const W = Math.max(300, Math.round(plot.clientWidth || 900)), ml = 96, mr = 10, mt = 8, rh = 20, mb = 24, H = mt + rows.length * rh + mb;
    const cw = (W - ml - mr) / xs.length;
    let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${esc(spec.aria || "")}">`;
    rows.forEach((r, j) => { const y = mt + j * rh;
      s += `<text x="${ml - 8}" y="${y + rh / 2 + 4}" class="tick" text-anchor="end" style="fill:var(--ink-2)">${esc(r.short)}</text>`;
      r.values.forEach((v, i) => { if (!ok(v)) return; const t = Math.max(-1, Math.min(1, v / clamp)), pct = Math.round(Math.abs(t) * 100);
        const pole = t < 0 ? "var(--heat-neg)" : "var(--heat-pos)";
        s += `<rect x="${(ml + i * cw).toFixed(2)}" y="${y + 1}" width="${(cw - 0.6).toFixed(2)}" height="${rh - 2}" data-i="${i}" data-j="${j}" style="fill:color-mix(in oklab, ${pole} ${pct}%, var(--heat-mid))"/>`; }); });
    linTicks(xs[0], xs[xs.length - 1], 7).forEach((v) => { const i = xs.indexOf(v); if (i < 0) return;
      s += `<text x="${ml + (i + 0.5) * cw}" y="${H - 7}" class="tick" text-anchor="middle">${v}</text>`; });
    s += `</svg>`; plot.querySelector("svg")?.remove(); plot.insertAdjacentHTML("afterbegin", s);
    const svg = plot.querySelector("svg");
    svg.addEventListener("pointermove", (ev) => { const t = ev.target; if (!t.dataset || t.dataset.i == null) { tip.hidden = true; return; }
      const i = +t.dataset.i, j = +t.dataset.j; tip.replaceChildren(); tip.append(el("div", "th", `${xs[i]} · ${rows[j].label}`));
      const r = el("div", "tr"), k = el("span", "key wash"); k.style.background = "var(--ink-3)"; r.append(k, el("b", null, fmt(rows[j].values[i], 2)), el("i", null, "tolerances, model minus record")); tip.append(r);
      tip.hidden = false; const box = plot.getBoundingClientRect(); const px = ev.clientX - box.left; const tw = tip.offsetWidth;
      tip.style.left = (px + 14 + tw > box.width ? Math.max(4, px - 14 - tw) : px + 14) + "px"; });
    svg.addEventListener("pointerleave", () => { tip.hidden = true; });
  };
  draw(); observe(plot, draw);
  const cols = rows.map((r) => ({ label: r.label, values: r.values, fmt: (v) => fmt(v, 2) })); numbersTable(host, xs, cols, defaultRows(xs, cols));
}

function dotPlot(host, spec) {
  host.innerHTML = ""; host.append(legend([{ label: spec.aLabel, color: spec.aColor, kind: "dot" }, { label: spec.bLabel, color: spec.bColor, kind: "dot" }]));
  const plot = el("div", "plot"); host.append(plot); const tip = el("div", "tip"); tip.hidden = true; plot.append(tip);
  const rows = spec.rows;
  const draw = () => {
    const W = Math.max(300, Math.round(plot.clientWidth || 800)), ml = W < 520 ? 100 : 190, mr = 16, mt = 10, rh = 30, mb = 26, H = mt + rows.length * rh + mb;
    const vals = rows.flatMap((r) => [r.a, r.b]).filter((v) => ok(v) && v > 0), lo = Math.min(...vals) / 1.4, hi = Math.max(...vals) * 1.4;
    const X = (v) => ml + (Math.log(v) - Math.log(lo)) / (Math.log(hi) - Math.log(lo)) * (W - ml - mr);
    let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${esc(spec.aria || "")}">`;
    logTicks(lo, hi).forEach((v) => { const x = X(v); s += `<line x1="${x}" x2="${x}" y1="${mt}" y2="${H - mb}" class="grid"/><text x="${x}" y="${H - 8}" class="tick" text-anchor="middle">${fmtTick(v)}</text>`; });
    rows.forEach((r, j) => { const y = mt + j * rh + rh / 2;
      s += `<text x="${ml - 10}" y="${y + 4}" class="tick" text-anchor="end" style="fill:var(--ink-2)">${esc(W < 520 ? r.short : r.label)}</text>`;
      s += `<line x1="${X(r.a)}" x2="${X(r.b)}" y1="${y}" y2="${y}" class="axis"/>`;
      s += `<circle cx="${X(r.a)}" cy="${y}" r="5" class="dot" style="fill:${spec.aColor}"/><circle cx="${X(r.b)}" cy="${y}" r="5" class="dot" style="fill:${spec.bColor}"/>`;
      s += `<rect x="${ml}" y="${y - rh / 2}" width="${W - ml - mr}" height="${rh}" fill="transparent" data-j="${j}"/>`; });
    s += `</svg>`; plot.querySelector("svg")?.remove(); plot.insertAdjacentHTML("afterbegin", s);
    plot.querySelector("svg").addEventListener("pointermove", (ev) => { const j = ev.target.dataset ? ev.target.dataset.j : null; if (j == null) { tip.hidden = true; return; }
      const r = rows[+j]; tip.replaceChildren(); tip.append(el("div", "th", r.label));
      [[spec.aLabel, r.a, spec.aColor], [spec.bLabel, r.b, spec.bColor]].forEach(([l, v, c]) => { const d = el("div", "tr"), k = el("span", "key dot"); k.style.background = c; d.append(k, el("b", null, fmt(v, 2)), el("i", null, l)); tip.append(d); });
      tip.hidden = false; const box = plot.getBoundingClientRect(), px = ev.clientX - box.left, tw = tip.offsetWidth;
      tip.style.left = (px + 14 + tw > box.width ? Math.max(4, px - 14 - tw) : px + 14) + "px"; tip.style.top = (mt + (+j) * rh + rh) + "px"; });
    plot.querySelector("svg").addEventListener("pointerleave", () => { tip.hidden = true; });
  };
  draw(); observe(plot, draw);
  const d = el("details", "nums"); d.append(el("summary", null, "Numbers")); const w = el("div", "tablewrap"), t = el("table");
  const hr = el("tr"); ["", spec.aLabel, spec.bLabel].forEach((h) => hr.append(el("th", null, h))); t.append(hr);
  rows.forEach((r) => { const tr = el("tr"); tr.append(el("td", null, r.label), el("td", null, fmt(r.a, 2)), el("td", null, fmt(r.b, 2))); t.append(tr); });
  w.append(t); d.append(w); host.append(d);
}

function splitBars(host, rows, legendItems) {
  host.innerHTML = ""; host.append(legend(legendItems.map((l) => ({ label: l.label, color: l.color, kind: "wash" }))));
  rows.forEach((r) => { const row = el("div", "split-row"); row.append(el("span", null, r.label)); const bar = el("div", "split-bar");
    bar.setAttribute("role", "img"); bar.setAttribute("aria-label", r.label + ": " + r.parts.map((p) => `${p.label} ${fmt(p.value, 2)}`).join(", "));
    r.parts.forEach((p) => { const d = el("div"); d.style.flex = `${Math.max(p.value, 0.0001)} 1 0`; d.style.background = p.color;
      if (p.dark) d.classList.add("dark-text"); d.title = `${p.label}: ${fmt(p.value, 3)}`; if (p.value >= 0.09) d.textContent = Math.round(p.value * 100) + "%"; bar.append(d); });
    row.append(bar); host.append(row); });
  const d = el("details", "nums"); d.append(el("summary", null, "Numbers")); const w = el("div", "tablewrap"), t = el("table");
  rows.forEach((r) => r.parts.forEach((p) => { const tr = el("tr"); tr.append(el("td", null, r.label), el("td", null, p.label), el("td", null, fmt(p.value, 3))); t.append(tr); }));
  w.append(t); d.append(w); host.append(d);
}

function htmlTable(t, head, rows) {
  t.replaceChildren(); const hr = el("tr"); head.forEach((h) => hr.append(el("th", null, h))); t.append(hr);
  rows.forEach((r) => { const tr = el("tr"); r.forEach((c) => { const td = el("td"); if (c instanceof Node) td.append(c); else td.textContent = c; tr.append(td); }); t.append(tr); });
}
