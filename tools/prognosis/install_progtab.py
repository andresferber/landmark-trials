"""Add a "Prognosis" tab: Established entries (every T entry with a PROG record, shown as compact rows that
jump to the full card) and Markers to watch (shared per disease, from a JSON file). Also adds Kind, Validation
and Used in rows to prognostic cards, and a Markers used row (chips) to trials listed in PROGMAP.
Run after tools/mechs/install_mechtab.py. Rerunnable: it replaces its own blocks and refreshes NEWM.
Usage: python3 install_progtab.py markers.json page.html [page.html ...]"""
import sys, json, re

markers = json.load(open(sys.argv[1], encoding="utf-8"))
J = lambda o: json.dumps(o, ensure_ascii=False)

CSS = """/* PROGTAB-CSS (Oct 31, 2026): Prognosis tab */
.prog { margin-top: 14px; }
.prog a { color: var(--accent); }
.prog .pg-note { font-size: 14px; color: var(--muted); margin: 0 0 10px; max-width: 72ch; }
.prog h2.pg-h { font-family: var(--font-display); font-weight: 650; font-size: 1.3rem; margin: 22px 0 4px; }
.prog .pg-chips { display: flex; flex-wrap: wrap; gap: 6px; padding-bottom: 10px; border-bottom: 1px solid var(--rule); }
.prog h3.pg-grp { font: 600 12px/1 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--fg); margin: 20px 0 0; padding-bottom: 8px; border-bottom: 2px solid var(--fg); }
.prog h3.pg-grp .gn { font-weight: 500; color: var(--muted); margin-left: 8px; }
.prog .pg-row { display: grid; grid-template-columns: 56px minmax(0,1fr); gap: 14px; padding: 14px 0; border-bottom: 1px solid var(--rule); }
.prog .pg-y { font: 500 14px var(--font-mono); color: var(--muted); padding-top: 2px; }
.prog .pg-b { min-width: 0; display: flex; flex-direction: column; gap: 5px; }
.prog .pg-top { display: flex; flex-wrap: wrap; gap: 8px; align-items: baseline; }
.prog .pg-name { font-family: var(--font-display); font-weight: 650; font-size: 1.08rem; margin: 0; }
.prog .pg-res, .prog .pg-val { margin: 0; font-size: 14px; }
.prog .pg-val { color: var(--muted); }
.prog .pg-k { font: 500 11px/1.9 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-right: 8px; }
.prog .pg-links { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-size: 13px; }
.pkind { font: 500 11px/1 var(--font-mono); letter-spacing: .05em; text-transform: uppercase; padding: 4px 7px; border-radius: 4px; color: var(--s-young); background: var(--s-young-bg); }
.pkind.cons { color: var(--s-p2); background: var(--s-p2-bg); }
.pkind.sur { color: var(--s-old); background: var(--s-old-bg); }
.pkind.pred { color: var(--s-rr); background: var(--s-rr-bg); }
.ptype { font: 400 12px var(--font-mono); color: var(--muted); }
a.pchip { display: inline-block; text-decoration: none; color: var(--fg); border: 1px solid var(--rule); background: var(--surface); border-radius: 999px; padding: 3px 10px; font-size: 13px; }
a.pchip:hover { border-color: var(--accent); color: var(--accent); }
.pchip-y { font: 500 11px var(--font-mono); color: var(--muted); margin-left: 4px; }
.puse { font-size: 13px; color: var(--muted); }
dd.pchips { display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: center; }
.prog .mw-item { border: 1px solid var(--rule); border-radius: 10px; background: var(--surface); padding: 14px 16px; margin: 12px 0; display: flex; flex-direction: column; gap: 6px; }
.prog .mw-ev { align-self: flex-start; font: 500 12px var(--font-mono); padding: 4px 8px; border-radius: 4px; color: var(--muted); background: var(--bg); }
.prog .mw-ev.lv0 { color: var(--s-young); background: var(--s-young-bg); }
.prog .mw-ev.lv1 { color: var(--accent); background: color-mix(in srgb, var(--accent) 12%, var(--surface)); }
.prog .mw-ev.lv2 { color: var(--s-old); background: var(--s-old-bg); }
.prog .mw-item dl { margin: 0; }
.prog .mw-hist { font-size: 13.5px; color: var(--muted); margin: 0; }
.prog .mw-foot { font-size: 13px; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 8px; }
.prog .mw-cite { font: 400 12px var(--font-mono); color: var(--muted); }
.prog details.mw-log { border: 1px solid var(--rule); border-radius: 10px; background: var(--surface); padding: 0 16px; margin-top: 10px; }
.prog details.mw-log summary { cursor: pointer; padding: 12px 0; font-weight: 600; font-size: 14px; }
.prog .pg-rules { font-size: 12.5px; color: var(--muted); margin-top: 16px; max-width: 72ch; }
@media (max-width: 480px) { .prog .pg-row { grid-template-columns: 1fr; gap: 2px; } }
@media print { .prog { display: none; } }
/* /PROGTAB-CSS */
"""

BTN = '<button type="button" role="tab" aria-selected="false" data-tab="prog" title="Click again to return to the trial list">Prognosis<span class="tcount"></span></button>\n    '
SEC_ANCHOR = '<section class="mechs" hidden aria-label="Drug mechanisms"></section>'
SEC = '\n  <section class="prog" hidden aria-label="Prognosis"></section>'

# Global helpers (before render(), which calls PROGROWS for each card).
JS_HELPERS = r"""// PROGTAB-HELPERS (Oct 31, 2026): rows on cards for prognostic entries and for trials that used them.
const PKIND = k => /consensus/i.test(k) ? "cons" : /surrogate/i.test(k) && !/candidate/i.test(k) ? "sur" : /predictive/i.test(k) ? "pred" : "";
const PTYPE = { model: "Models and staging", bio: "Biomarkers", resp: "Response and MRD" };
const PUSEDIN = n => (typeof PROGMAP === "undefined") ? [] : Object.keys(PROGMAP).filter(k => PROGMAP[k].some(x => x[0] === n));
function PCHIP(name, label, year) {
  return '<a class="pchip" href="#t-' + PAGEKEY + '-' + SLUG(name) + '" data-slug="' + SLUG(name) + '">' + esc(label) + (year ? '<span class="pchip-y">' + year + '</span>' : '') + '</a>';
}
function PROGROWS(t) {
  if (typeof PROG === "undefined") return "";
  const P = PROG[t.n];
  if (P) {
    const used = PUSEDIN(t.n).map(n => T.find(x => x.n === n)).filter(Boolean).sort((a, b) => a.y - b.y);
    return '<dt>Kind</dt><dd><span class="pkind ' + PKIND(P.pk) + '">' + esc(P.pk) + '</span> <span class="ptype">' + esc(PTYPE[P.pt] || "") + '</span></dd>' +
      '<dt>Validation</dt><dd>' + esc(P.val) + '</dd>' +
      (used.length ? '<dt>Used in</dt><dd class="pchips">' + used.map(x => PCHIP(x.n, x.n, x.y)).join("") + '</dd>' : '');
  }
  const M = (typeof PROGMAP !== "undefined") && PROGMAP[t.n];
  if (!M) return "";
  return '<dt>Markers used</dt><dd class="pchips">' + M.map(x => PCHIP(x[0], (PROG[x[0]] && PROG[x[0]].sh) || x[0]) + ' <span class="puse">' + esc(x[1]) + '</span>').join("") + '</dd>';
}
// /PROGTAB-HELPERS
"""

JS_TAB = r"""  // PROGTAB-TAB (Oct 31, 2026): Prognosis tab: Established entries and Markers to watch.
  const ppanel = root.querySelector(".prog");
  const pEst = (typeof PROG !== "undefined") ? T.filter(t => PROG[t.n]) : [];
  const pMk = (typeof NEWM !== "undefined" && NEWM.items) ? NEWM.items : [];
  const cpg = tabs.querySelector('[data-tab="prog"] .tcount'); if (cpg) cpg.textContent = pEst.length + pMk.length;
  let ptype = "all";
  const EVL = ["Validated, not yet practical", "Independent validation", "Discovery only"];
  function drawProg(){
    if (!ppanel) return;
    const est = pEst.filter(t => ptype === "all" || PROG[t.n].pt === ptype)
      .sort((a, b) => (["model", "bio", "resp"].indexOf(PROG[a.n].pt) - ["model", "bio", "resp"].indexOf(PROG[b.n].pt)) || a.y - b.y || a.n.localeCompare(b.n));
    const mk = pMk.slice().sort((a, b) => (EVL.indexOf(a.ev) - EVL.indexOf(b.ev)) || String(b.last).localeCompare(String(a.last)));
    const L = s => '<a href="' + esc(s[1]) + '" target="_blank" rel="noopener">' + esc(s[0]) + ' ↗</a>';
    const row = (k, v, cls) => v ? '<dt' + (cls ? ' class="' + cls + '"' : '') + '>' + k + '</dt><dd' + (cls ? ' class="' + cls + '"' : '') + '>' + esc(v) + '</dd>' : '';
    ppanel.innerHTML =
      '<p class="pg-note">Risk models, biomarkers and response measures. Each entry states whether it is prognostic (outcome regardless of treatment), predictive (who benefits from a given treatment), a surrogate endpoint or a consensus definition. Within each group, oldest first, so each tool appears after the one it built on. Select an entry to open its full card.</p>' +
      '<h2 class="pg-h">Established</h2><p class="pg-note">Externally validated, or adopted in an IMWG or IMS consensus, a guideline or a regulatory decision.</p>' +
      '<div class="pg-chips">' + [["all", "All"], ["model", PTYPE.model], ["bio", PTYPE.bio], ["resp", PTYPE.resp]].map(([k, l]) =>
        '<button type="button" class="chip" data-pt="' + k + '" aria-pressed="' + (k === ptype) + '">' + esc(l) + ' <span class="gn">' + (k === "all" ? pEst.length : pEst.filter(t => PROG[t.n].pt === k).length) + '</span></button>').join("") + '</div>' +
      est.map((t, i) => { const P = PROG[t.n];
        const grp = (ptype === "all" && (i === 0 || PROG[est[i - 1].n].pt !== P.pt))
          ? '<h3 class="pg-grp">' + esc(PTYPE[P.pt]) + '<span class="gn">' + est.filter(x => PROG[x.n].pt === P.pt).length + '</span></h3>' : '';
        const used = PUSEDIN(t.n).map(n => T.find(x => x.n === n)).filter(Boolean).sort((a, b) => a.y - b.y);
        return grp + '<div class="pg-row"><div class="pg-y">' + t.y + '</div><div class="pg-b"><div class="pg-top"><h3 class="pg-name"><a href="#t-' + PAGEKEY + '-' + t.slug + '" class="pjump" data-slug="' + t.slug + '">' + esc(t.n) + '</a></h3>' +
          '<span class="pkind ' + PKIND(P.pk) + '">' + esc(P.pk) + '</span><span class="ptype">' + esc(PTYPE[P.pt]) + '</span>' + (t.core ? '<span class="core" title="Core trial for teaching">★ Core</span>' : '') + '</div>' +
          '<p class="pg-res">' + esc(t.r) + '</p><p class="pg-val"><span class="pg-k">Validation</span>' + esc(P.val) + '</p>' +
          '<div class="pg-links"><a href="#t-' + PAGEKEY + '-' + t.slug + '" class="pjump" data-slug="' + t.slug + '">Full card ↗</a>' +
          (used.length ? '<span class="pg-k" style="margin-left:8px">Used in</span>' + used.map(x => PCHIP(x.n, x.n, x.y)).join("") : '') + '</div></div></div>'; }).join("") +
      '<h2 class="pg-h">Markers to watch</h2><p class="pg-note">' + esc(NEWM.note) + (NEWM.scope ? ' ' + esc(NEWM.scope) : '') + ' Checked ' + esc(NEWM.checked) + '.</p>' +
      (mk.length ? mk.map(d => '<div class="mw-item"><div class="pg-top"><h3 class="pg-name">' + esc(d.n) + '</h3><span class="pkind ' + PKIND(d.kind) + '">' + esc(d.kind) + '</span><span class="ptype">' + esc(d.type) + '</span></div>' +
        '<span class="mw-ev lv' + Math.max(0, EVL.indexOf(d.ev)) + '">Evidence: ' + esc(d.ev) + ' · ' + esc(d.pub) + '</span>' +
        '<dl>' + row("Why it matters", d.why) + row("Cohort", d.cohort) + row("Key data", d.data, "f-res") + row("Adjusted for", d.adj) + row("Still missing", d.missing) + row("Status", d.status) + row("Next step", d.next) +
        '<dt>Sources</dt><dd>' + d.src.map(L).join(" · ") + '</dd></dl>' +
        (d.hist ? '<p class="mw-hist"><b>History.</b> ' + esc(d.hist) + '</p>' : '') +
        (d.cites ? '<p class="mw-cite">Cited by ' + d.cites.total + ' papers in PubMed Central, ' + d.cites.recent + ' in the last 24 months (checked ' + esc(NEWM.checked) + ').</p>' : '') +
        '<p class="mw-foot">Not validated for clinical decisions.</p></div>').join("") : '<p class="pg-note">None at present.</p>') +
      '<details class="mw-log"><summary>Did not validate (' + (NEWM.failed || []).length + ')</summary>' +
        ((NEWM.failed || []).length ? '<ul>' + NEWM.failed.map(g => '<li><b>' + esc(g.n) + ':</b> ' + esc(g.txt) + ' ' + (g.src || []).map(L).join(" · ") + '</li>').join("") + '</ul>'
          : '<p class="pg-note">None so far. Markers that fail independent validation are listed here with the reason and date, and removed after 2 years.</p>') + '</details>' +
      '<p class="pg-rules">How Markers to watch is kept: peer-reviewed papers only (meeting data can update an entry, labelled as such). Ordered by evidence (validated but not yet practical, then independent validation, then discovery only), newest evidence first. A marker moves to Established when it is validated and recognized in a consensus or guideline, or can be measured with standard tests; to "Did not validate" when an independent study fails to confirm it; and is proposed for removal when no new validation study has appeared for 24 months. Checked at each scheduled update and after major meetings.</p>';
    ppanel.querySelectorAll(".pg-chips .chip").forEach(b => b.addEventListener("click", () => { ptype = b.getAttribute("data-pt"); drawProg(); }));
  }
  drawProg();
  if (ppanel) ppanel.addEventListener("click", e => {
    const a = e.target.closest("a.pjump, a.pchip"); if (!a) return;
    e.preventDefault();
    show("trials");
    tabs.dispatchEvent(new Event("tabschange"));
    jumpTo(a.getAttribute("data-slug"));
  });
  // /PROGTAB-TAB
"""

# Chips on cards in the trial list jump to the linked card.
JS_LISTCLICK = r"""// PROGTAB-LIST (Oct 31, 2026): chips on cards jump to the linked card.
function jumpTo(slug){
  const listEl = document.getElementById("list");
  const first = chipsEl.querySelector(".chip");
  if (first && first.getAttribute("aria-pressed") !== "true") first.click();
  if (qEl.value) { qEl.value = ""; render(); }
  const li = listEl.querySelector('li[data-trial="' + slug + '"]');
  if (!li) return;
  li.scrollIntoView({ behavior: "smooth", block: "start" });
  li.classList.remove("flash"); void li.offsetWidth; li.classList.add("flash");
}
document.getElementById("list").addEventListener("click", e => {
  const a = e.target.closest("a.pchip"); if (!a) return;
  e.preventDefault(); jumpTo(a.getAttribute("data-slug"));
});
// /PROGTAB-LIST
"""

SHOW_OLD = '    if (watch && which === "mech") watch.style.display = "none";\n'
SHOW_NEW = SHOW_OLD + '    if (ppanel) ppanel.hidden = which !== "prog";\n    if (watch && which === "prog") watch.style.display = "none";\n'
ROW_ANCHOR = '          ${MOAMAP[t.n] ? `<dt>Drug mechanism</dt><dd class="moas">${MOAHTML(t)}</dd>` : ""}\n'
ROW_NEW = ROW_ANCHOR + '          ${PROGROWS(t)}\n'
TAB_ANCHOR = '  tabs.addEventListener("click", e => {\n    const b = e.target.closest("button[data-tab]"); if (!b) return;'
FOOT_ANCHOR = '    <p class="sitedisc">'
FOOT = '    <p class="pgfoot">Prognosis tab (added October 31, 2026): models, biomarkers and response measures are included when externally validated or adopted in an IMWG or IMS consensus, a guideline or a regulatory decision; links between trial cards and prognostic entries are shown only when the trial used the measure in its design (endpoint, eligibility, stratification or treatment assignment). Numbers checked against the PubMed abstract on October 31, 2026.</p>\n'

def strip(h, a, b):
    return re.sub(re.escape(a) + r'.*?' + re.escape(b) + r'\n?', '', h, flags=re.S)

for page in sys.argv[2:]:
    h = open(page, encoding="utf-8").read()
    assert "const PROG = " in h, page + ": run the topic's entries script first (PROG missing)"
    for a, b in [("/* PROGTAB-CSS", "/* /PROGTAB-CSS */"), ("// PROGTAB-HELPERS", "// /PROGTAB-HELPERS"), ("// PROGTAB-LIST", "// /PROGTAB-LIST"), ("  // PROGTAB-TAB", "  // /PROGTAB-TAB")]:
        h = strip(h, a, b)
    # CSS: before the first </style>.
    i = h.index("</style>"); h = h[:i] + CSS + h[i:]
    # Tab button and section.
    if 'data-tab="prog"' not in h:
        h = h.replace('<a class="tabmail"', BTN + '<a class="tabmail"', 1)
    if '<section class="prog"' not in h:
        assert SEC_ANCHOR in h, page + ": Drug mechanisms tab missing (run install_mechtab.py first)"
        h = h.replace(SEC_ANCHOR, SEC_ANCHOR + SEC, 1)
    # NEWM data next to PROG.
    line = "const NEWM = " + J(markers) + ";\n"
    if "const NEWM = " in h:
        h = re.sub(r'const NEWM = .*?;\n', lambda _: line, h, count=1)
    else:
        h = h.replace("const PROG = ", line + "const PROG = ", 1)
    # Helpers before the first render() call; card rows; list click handler after render().
    i = h.index("function render(){"); h = h[:i] + JS_HELPERS + h[i:]
    if ROW_NEW not in h:
        assert ROW_ANCHOR in h, page + ": card template anchor not found"
        h = h.replace(ROW_ANCHOR, ROW_NEW, 1)
    i = h.index("\nrender();\n") + len("\nrender();\n"); h = h[:i] + JS_LISTCLICK + h[i:]
    if SHOW_NEW not in h:
        assert SHOW_OLD in h, page + ": show() anchor not found"
        h = h.replace(SHOW_OLD, SHOW_NEW, 1)
    assert TAB_ANCHOR in h, page + ": tab click anchor not found"
    h = h.replace(TAB_ANCHOR, JS_TAB + TAB_ANCHOR, 1)
    if 'class="pgfoot"' not in h:
        h = h.replace(FOOT_ANCHOR, FOOT + FOOT_ANCHOR, 1)
    open(page, "w", encoding="utf-8").write(h)
    print("ok", page)
