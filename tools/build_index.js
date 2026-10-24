#!/usr/bin/env node
/* Build index.json (search across all topics) from source/<key>.html.
   Usage: node tools/build_index.js   (run from the repository root)
   Each entry: k topic key, n name, y year, s trial slug, d design, c core flag,
   h lowercase text the website search matches against. */
const fs = require("fs"), vm = require("vm"), path = require("path");
const root = path.join(__dirname, "..");
const topics = JSON.parse(fs.readFileSync(path.join(root, "topics.json"), "utf8")).topics;
const el = () => ({ setAttribute() {}, addEventListener() {}, appendChild() {}, querySelectorAll() { return []; },
  querySelector() { return null; }, closest() { return null; }, classList: { add() {}, remove() {}, toggle() {} },
  style: {}, value: "", innerHTML: "", textContent: "", parentNode: { querySelector() { return null; } } });
const out = [];
for (const t of topics) {
  const file = path.join(root, "source", t.key + ".html");
  if (!fs.existsSync(file)) { console.error("missing " + file); process.exitCode = 1; continue; }
  const h = fs.readFileSync(file, "utf8");
  const s = [...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(x => x.includes("const T") && x.includes("function render"));
  const els = {};
  const ctx = { document: { getElementById: id => els[id] || (els[id] = el()), createElement: () => el(), querySelectorAll: () => [], addEventListener() {} },
    localStorage: { getItem() { return null; }, setItem() {} }, window: { addEventListener() {}, print() {} }, location: { hash: "", search: "" }, console, setTimeout() {} };
  vm.createContext(ctx);
  vm.runInContext(s + "\n;globalThis.__x = { T, SETTINGS };", ctx);
  const { T, SETTINGS } = ctx.__x;
  for (const x of T) {
    const hay = [x.n, x.d, x.r, x.ep, x.ph, String(x.y), SETTINGS[x.s] || "", t.title].join(" ").toLowerCase();
    out.push({ k: t.key, n: x.n, y: x.y, s: x.slug, d: x.d, c: x.core ? 1 : 0, h: hay });
  }
}
out.sort((a, b) => topics.findIndex(t => t.key === a.k) - topics.findIndex(t => t.key === b.k) || a.y - b.y);
fs.writeFileSync(path.join(root, "index.json"), JSON.stringify(out));
console.log("index.json: " + out.length + " trials");
