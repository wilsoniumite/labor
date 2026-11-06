// preview.js — a local stand-in for the doc's chart renderer, for looking at a chart before (and after) it is published:
// compiles a widget module (TSX) with a tiny JSX-to-SVG-string runtime, feeds claude.Visualize its sources (inline rows,
// or the doc's CSV blobs mapped to the local files they were uploaded from), and screenshots the SVG with Chromium.
// Usage: NODE_PATH=/opt/node22/lib/node_modules node preview.js <module.tsx> <out.png>
const fs = require("fs");
const path = require("path");
const ts = require("typescript");
const { chromium } = require("playwright");

const BLOBS = {
  "blob/6edd3296-e6db": "/home/user/labor/us-record/results/doc/six.csv",
  "blob/96768651-7204": "/home/user/labor/us-record/results/doc/rest.csv",
};
const ATTR = { strokeWidth: "stroke-width", textAnchor: "text-anchor", fontSize: "font-size", fontWeight: "font-weight",
  fillOpacity: "fill-opacity", strokeOpacity: "stroke-opacity", strokeDasharray: "stroke-dasharray", markerEnd: "marker-end",
  dominantBaseline: "dominant-baseline", strokeLinecap: "stroke-linecap", strokeLinejoin: "stroke-linejoin",
  fontStyle: "font-style", letterSpacing: "letter-spacing" };
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const flat = (a) => a.flat(Infinity).filter((c) => c !== null && c !== undefined && c !== false && c !== true);

function h(tag, props, ...kids) {
  props = props || {};
  if (typeof tag === "function") return tag({ ...props, children: kids });
  const attrs = Object.entries(props).filter(([k, v]) => k !== "key" && k !== "children" && v !== undefined && v !== null && v !== false)
    .map(([k, v]) => ` ${ATTR[k] || k}="${esc(v)}"`).join("");
  const inner = flat(kids).map((c) => (typeof c === "object" && c.__html !== undefined ? c.__html : esc(c))).join("");
  return { __html: `<${tag}${attrs}>${inner}</${tag}>` };
}
const Fragment = ({ children }) => ({ __html: flat(children).map((c) => (c.__html !== undefined ? c.__html : esc(c))).join("") });

function csv(file, adapter) {
  const lines = fs.readFileSync(file, "utf8").trim().split(/\r?\n/);
  const head = lines[0].split(",");
  return lines.slice(1).map((line) => {
    const cells = line.split(",");
    const row = {};
    head.forEach((k, i) => {
      const t = adapter.columns[i].type.type;
      row[k] = t === "number" ? Number(cells[i]) : cells[i];
    });
    return row;
  });
}

const claude = {
  Visualize: ({ sources, children }) => {
    const data = {};
    for (const [k, s] of Object.entries(sources)) data[k] = s.kind === "data" ? s.data : csv(BLOBS[s.ref], s.adapter);
    const fn = flat(children)[0];
    return fn({ ...data, datum: () => ({}) });
  },
};

async function main() {
  const [src, out] = process.argv.slice(2);
  const code = fs.readFileSync(src, "utf8");
  const js = ts.transpileModule(code, { compilerOptions: { jsx: ts.JsxEmit.React, jsxFactory: "h",
    jsxFragmentFactory: "Fragment", module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 } }).outputText;
  const exports = {};
  new Function("h", "Fragment", "claude", "exports", js)(h, Fragment, claude, exports);
  const svg = exports.default().__html;
  const css = `:root{--cds-text-primary:#1d1d1b;--cds-text-secondary:#6b6a66;--cds-chart-grid:#e7e6e2;--cds-chart-axis:#a3a29c;
    --cds-chart-categorical-1:#2a78d6;--cds-chart-categorical-2:#eb6834;--cds-chart-categorical-3:#1baf7a;--cds-chart-muted:#a9a8a3;
    --cds-chart-reference:#8c8b86;--cds-chart-reference-tint:#f3f2ee;--cds-chart-status-good:#2f9e5b;--cds-chart-status-critical:#d64545}
    body{margin:0;background:#fff;font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif} svg{width:760px;display:block}`;
  fs.writeFileSync(out.replace(/\.png$/, ".html"), `<!doctype html><html><head><style>${css}</style></head><body>${svg}</body></html>`);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 760, height: 400 }, deviceScaleFactor: 1 });
  await page.setContent(`<!doctype html><html><head><style>${css}</style></head><body>${svg}</body></html>`);
  const el = await page.$("svg");
  await el.screenshot({ path: out });
  await browser.close();
  console.log(`${out} written (${svg.length} chars of svg)`);
}
main().catch((e) => { console.error(e); process.exit(1); });
