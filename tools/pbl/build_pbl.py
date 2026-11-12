#!/usr/bin/env python3
"""Build the Primary bone lymphoma page (key "pbl") from the standard topic template.
Usage (from the repository root): python3 tools/pbl/build_pbl.py <out.html>
This topic is an evidence map of a rare entity (mostly retrospective series), not a list of trials, so the
card layout differs from the trial-based topics: design badge, definition used, prognostic factors, limitations
and cohort overlap; an evidence grid (histology x study design) that filters the list; a "What is not known" box.
Data: tools/pbl/pbl_data.py and tools/pbl/ft.json (full-text links). Then run, in order:
  python3 tools/review/build_persp.py pbl <out.html>   (from tools/)
  python3 tools/review/install_persptint.py <out.html>
Tabs for Trials to watch / New drugs to watch / Drug mechanisms are kept in the page but stay hidden while
their lists are empty (Andres, Nov 11, 2026: leave them off unless something comes up, e.g. after ASH)."""
import re, sys, json, os, io
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(os.path.dirname(here))
sys.path.insert(0, here)
import pbl_data as D

CHECKED = "November 11, 2026"
out = sys.argv[1]
s = io.open(os.path.join(root, "source", "flr.html"), encoding="utf-8").read()
J = lambda v: json.dumps(v, ensure_ascii=False)

def sub1(pat, rep, flags=re.S):
    global s
    s, n = re.subn(pat, lambda m: rep, s, count=1, flags=flags)
    assert n == 1, pat
def rep1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

# ---- head, header
sub1(r"<title>.*?</title>", "<title>Primary Bone Lymphoma</title>")
sub1(r"<header>.*?</header>", """<header>
    <div class="eyebrow">Primary bone lymphoma · adults · 2003–2026</div>
    <h1>Key studies in primary bone lymphoma</h1>
    <p>A rare lymphoma with one small prospective trial and no randomized evidence. This page gathers what has been published: treatment series, registries, prognosis, single versus multiple lesions, biology, circulating tumor DNA, non-DLBCL histologies and imaging.</p>
  </header>""")
# The template's Perspective block is replaced by tools/review/build_persp.py (run after this script).

# ---- evidence-map banner, grid, what is not known (before the tab bar)
unk = "".join("<li>%s</li>" % u for u in D.UNKNOWN)
EV = """  <section class="evmap" aria-label="How to read this page">
    <p class="ev-banner"><b>An evidence map, not a list of practice-changing trials.</b> Almost everything here is retrospective. Each card shows its study design, the definition of primary bone lymphoma it used (gray row), and its limitations. Series define the disease differently and some share patients, so results should not be pooled or compared directly.</p>
    <div class="ev-cols">
      <div class="ev-gridbox"><h2 class="ev-h">What has been published</h2><p class="ev-sub">Number of studies by histology and design. Select a number to filter the list; empty cells are gaps.</p><div class="ev-grid"></div></div>
      <div class="ev-unk"><h2 class="ev-h">What is not known</h2><ul>""" + unk + """</ul></div>
    </div>
  </section>

"""
rep1('  <div class="tabs" role="tablist"', EV + '  <div class="tabs" role="tablist"')
rep1('data-tab="trials">Landmark trials</button>', 'data-tab="trials">Key studies</button>')
sub1(r'<a class="tabmail" href="[^"]*">', '<a class="tabmail" href="mailto:andresferber@hotmail.com?subject=Landmark%20trials%20%28Primary%20bone%20lymphoma%29%3A%20comment">')
rep1('placeholder="Search trial, drug, regimen…" aria-label="Search trials"', 'placeholder="Search study, center, design, factor…" aria-label="Search studies"')
rep1('title="Print or save as PDF (prints the trials currently shown)"', 'title="Print or save as PDF (prints the studies currently shown)"')

# ---- data
def js_entry(t):
    keys = ["y","n","s","ph","hist","d","per","df","ep","r","N","fu","pf","tox","i","q","ov","c","p","cm","rel"]
    parts = []
    for k in keys:
        if k in ("cm",): v = t.get(k, [])
        elif k not in t: continue
        else: v = t[k]
        parts.append(k + ":" + J(v))
    return "{" + ",".join(parts) + "}"
T_JS = "const T = [\n" + ",\n".join(js_entry(t) for t in D.T) + "\n];"
ft_raw = json.load(open(os.path.join(here, "ft.json")))
FT = {t["n"]: ft_raw[str(t["p"])] for t in D.T if ft_raw.get(str(t["p"]))}

def set_const(name, js):
    global s
    i = s.index("\nconst " + name + " =") + 1
    ends = [x for x in (s.find("\nconst ", i + 5), s.find("\nfunction ", i + 5), s.find("\nlet ", i + 5), s.find("\n//", i + 5), s.find("\nT.forEach", i + 5)) if x > 0]
    s = s[:i] + "const " + name + " = " + js + ";" + s[min(ends):]
set_const("SETTINGS", J({k: v for k, v, c in D.SETTINGS}))
set_const("CLS", J({k: c for k, v, c in D.SETTINGS}))
set_const("order", J([k for k, v, c in D.SETTINGS]))
i = s.index("\nconst T = [") + 1; j = s.index("\n];", i) + 3
s = s[:i] + T_JS + s[j:]
set_const("REG", J(D.REG)); set_const("FT", J(FT))
set_const("MOA", "{}"); set_const("MOAMAP", "{}"); set_const("MECH", "{}")
set_const("NEWD", J({"note": "", "checked": CHECKED, "items": [], "grad": [], "disc": []}))
set_const("TOX", "{}"); set_const("CORE", J(D.CORE))
set_const("WATCH", J({"note": "No ongoing trial dedicated to primary bone lymphoma was found on ClinicalTrials.gov (checked %s)." % CHECKED, "items": []}))
set_const("PAGEKEY", '"pbl"'); set_const("PAGETITLE", '"Primary bone lymphoma"')
s = s.replace("const DESIGNS_PLACEHOLDER", "")
rep1('T.forEach(t => { t.tx = TOX[t.n] || "Not reported in abstract"; t.core = CORE.includes(t.n); t.slug = SLUG(t.n);',
     'const DESIGNS = %s, HISTS = %s, HISTLABEL = {"DLBCL": "DLBCL only", "Mixed": "Mixed histologies, mostly DLBCL", "Non-DLBCL": "Non-DLBCL"};\nlet gridF = null;\nT.forEach(t => { t.tx = t.tox || ""; t.core = CORE.includes(t.n); t.slug = SLUG(t.n);' % (J(D.DESIGNS), J(D.HISTS)))
rep1('t.full = [t.r, t.N, t.hr, t.fu, t.tx].some(', 't.full = [t.r, t.N, t.fu, t.d, t.per, t.df, t.pf, t.tx].some(')
s = s.replace('"fl2-sort"', '"pbl-sort"')
rep1('["core","★ Core trials"]', '["core","★ Core studies"]')

# ---- reception: commentary and related papers only
i = s.index("  return `<div class=\"rk\">Commentary</div>"); j = s.index("\n}", i)
s = s[:i] + "  return `<div class=\"rk\">Commentary</div><ul>${cm}</ul>${rel}`;" + s[j:]
rep1("const r = t.rc; if (!r) return \"\";", "const r = t.rc; if (!r) return \"\";")

# ---- filter, count, card
rep1('(active === "all" || (active === "core" ? t.core : t.s === active)) &&',
     '(active === "all" || (active === "core" ? t.core : t.s === active)) && (!gridF || (t.hist === gridF.h && t.ph === gridF.d)) &&')
rep1('[t.n,t.d,t.r,t.tx,t.i,t.b,t.q,t.c,t.ph,String(t.y),t.reg,t.gl,t.acc,', '[t.n,t.d,t.r,t.tx,t.i,t.q,t.c,t.ph,String(t.y),t.df,t.pf,t.ep,t.per,t.ov||"",HISTLABEL[t.hist],')
i = s.index('  list.innerHTML = rows.map((t, i) => GRPHDR(t, i, rows) + `'); j = s.index('</li>`).join("");', i) + len('</li>`).join("");')
CARD = r'''  list.innerHTML = rows.map((t, i) => GRPHDR(t, i, rows) + `
    <li class="trial" data-trial="${t.slug}">
      <div class="yr">${t.y}</div>
      <div class="body">
        <div class="top"><h2 class="name">${esc(t.n)}</h2><span class="tag ${CLS[t.s]}">${esc(SETTINGS[t.s])}</span><span class="phase dz dz-${DESIGNS.indexOf(t.ph)}">${esc(t.ph)}</span><span class="phase">${esc(HISTLABEL[t.hist])}</span>${t.core ? '<span class="core" title="Core study for teaching">★ Core</span>' : ''}<button type="button" class="share" data-slug="${t.slug}" title="Copy a link to this study" aria-label="Copy a link to ${esc(t.n)}"><svg viewBox="0 0 20 20" width="14" height="14" aria-hidden="true"><path d="M8.5 11.5a3 3 0 0 0 4.2 0l2.6-2.6a3 3 0 0 0-4.2-4.2l-1 1M11.5 8.5a3 3 0 0 0-4.2 0l-2.6 2.6a3 3 0 0 0 4.2 4.2l1-1" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span class="lbl">Link copied</span></button></div>
        <p class="design">${esc(t.d)}</p>
        <div class="stats">
          <span><b>N</b>${esc(t.N)}</span>
          <span><b>Period</b>${esc(t.per)}</span>
          <span><b>Median F/U</b>${esc(t.fu)}</span>
        </div>
        <dl>
          <dt class="f-ep">Definition used</dt><dd class="f-ep">${esc(t.df)}</dd>
          <dt>Outcomes</dt><dd>${esc(t.ep)}</dd>
          <dt class="f-res">Result</dt><dd class="result f-res">${esc(t.r)} ${eviHTML(t)}</dd>
          <dt class="f-tox">Prognostic factors</dt><dd class="tox f-tox">${esc(t.pf)}</dd>
          ${t.tx ? `<dt>Complications</dt><dd>${esc(t.tx)}</dd>` : ""}
          <dt>What it adds</dt><dd>${esc(t.i)}</dd>
          <dt>Limitations</dt><dd class="qs">${esc(t.q)}</dd>
          ${t.ov ? `<dt>Overlap</dt><dd class="ovl">${esc(t.ov)}</dd>` : ""}
          <dt>Reception</dt><dd class="rec">${recHTML(t)}</dd>
          <dt>Source</dt><dd class="cite"><a href="${esc(t.url)}" target="_blank" rel="noopener">${esc(t.c)} ↗</a>${t.ft ? ` · <a class="ft" href="${esc(FTURL(t.ft))}" target="_blank" rel="noopener" title="${FTTITLE(t.ft)}">${FTLABEL(t.ft)} ↗</a>` : ''}${t.ft && t.ft[2] === 'repo' ? ` · <a class="ft" href="${esc(t.ft[3])}" target="_blank" rel="noopener" title="Free legal copy in a university repository, found through Unpaywall; it may be the authors' manuscript rather than the final journal version">Free copy (repository) ↗</a>` : ''}${t.trn.map(id => ` · <a class="trn" href="${esc(REGURL(id))}" target="_blank" rel="noopener" title="Trial registry record">${esc(id)} ↗</a>`).join('')} · <a class="report" href="${esc(REPORT(t))}" title="Email a correction for this study">Report an error</a></dd>
        </dl>
      </div>
    </li>`).join("");'''
s = s[:i] + CARD + s[j:]
rep1("No studies match that search. Clear the search or pick another category.", "No studies match. Clear the search, pick another category, or clear the evidence-grid filter.")

# ---- grid script + hide empty tabs (after the first render() call)
GRID = r'''
(function evidenceGrid(){
  // Evidence grid: histology x study design. Counts filter the list; empty cells show the gaps.
  const listEl = document.getElementById("list");
  const box = listEl.parentNode && listEl.parentNode.querySelector(".ev-grid");
  if (!box) return;
  function draw(){
    const n = (h, d) => T.filter(t => t.hist === h && t.ph === d).length;
    box.innerHTML = '<table><thead><tr><th scope="col"><span class="ev-vh">Histology</span></th>' + DESIGNS.map(d => '<th scope="col">' + esc(d) + '</th>').join("") + '</tr></thead><tbody>' +
      HISTS.map(h => '<tr><th scope="row">' + esc(HISTLABEL[h]) + '</th>' + DESIGNS.map(d => { const c = n(h, d);
        const on = gridF && gridF.h === h && gridF.d === d;
        return '<td>' + (c ? '<button type="button" class="ev-cell" data-h="' + esc(h) + '" data-d="' + esc(d) + '" aria-pressed="' + (on ? "true" : "false") + '" title="' + c + (c === 1 ? ' study' : ' studies') + ': ' + esc(HISTLABEL[h]) + ', ' + esc(d) + '">' + c + '</button>' : '<span class="ev-none" title="Nothing published">–</span>') + '</td>'; }).join("") + '</tr>').join("") +
      '</tbody></table>' + (gridF ? '<p class="ev-clear"><button type="button" class="ev-reset">✕ Clear grid filter</button> Showing ' + esc(HISTLABEL[gridF.h]) + ', ' + esc(gridF.d) + '.</p>' : '');
  }
  box.addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    if (b.classList.contains("ev-reset")) gridF = null;
    else { const h = b.getAttribute("data-h"), d = b.getAttribute("data-d"); gridF = (gridF && gridF.h === h && gridF.d === d) ? null : { h: h, d: d }; }
    const first = chipsEl.querySelector(".chip");
    if (gridF && first && first.getAttribute("aria-pressed") !== "true") first.click();
    draw(); render();
    if (gridF && listEl.scrollIntoView) listEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
  draw();
})();
(function hideEmptyTabs(){
  // Trials to watch, New drugs to watch and Drug mechanisms appear only when they have entries.
  const listEl = document.getElementById("list");
  const tabs = listEl.parentNode && listEl.parentNode.querySelector(".tabs");
  if (!tabs) return;
  const n = { watch: (WATCH.items || []).length, newdrugs: (NEWD.items || []).length, mech: Object.keys(MOAMAP).length };
  Object.keys(n).forEach(k => { const b = tabs.querySelector('[data-tab="' + k + '"]'); if (b) b.style.display = n[k] ? "" : "none"; });
})();
'''
rep1("render();\n\n(function renderWatch(){", "render();\n" + GRID + "\n(function renderWatch(){")

# ---- CSS: own accent (slate-teal) and the new components
s = s.replace("--accent: #2c4a8a;", "--accent: #2f6468;").replace("--accent: #8fb0f2;", "--accent: #8fcdd1;").replace("--accent: #1a3a7a;", "--accent: #23494c;")
CSS = '''
/* Primary bone lymphoma (Nov 11, 2026): evidence-map page. Own accent; banner, grid, design badges. */
.evmap { margin-top: 18px; }
.ev-banner { margin: 0 0 12px; padding: 12px 14px; border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 10px; background: var(--surface); font-size: 14px; line-height: 1.5; }
.ev-cols { display: grid; grid-template-columns: minmax(0, 1fr); gap: 12px; }
@media (min-width: 761px) { .ev-unk ul { columns: 2; column-gap: 28px; } .ev-unk li { break-inside: avoid; } }
.ev-gridbox, .ev-unk { border: 1px solid var(--rule); border-radius: 10px; background: var(--surface); padding: 12px 14px; min-width: 0; }
.ev-h { font: 500 11px/1.4 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); margin: 0 0 4px; }
.ev-sub { margin: 0 0 8px; font-size: 12.5px; color: var(--muted); }
.ev-grid { overflow-x: auto; }
.ev-grid table { border-collapse: collapse; width: 100%; font-size: 12.5px; }
.ev-grid th, .ev-grid td { border: 1px solid var(--rule); padding: 5px 6px; text-align: center; vertical-align: middle; }
.ev-grid thead th { font: 500 11px/1.25 var(--font-body); color: var(--muted); min-width: 62px; }
.ev-grid tbody th { text-align: left; font-weight: 600; font-size: 12.5px; min-width: 96px; }
.ev-cell { all: unset; cursor: pointer; display: inline-block; min-width: 30px; padding: 4px 6px; border-radius: 6px; font: 600 13px/1 var(--font-mono); color: var(--accent); background: color-mix(in srgb, var(--accent) 12%, var(--surface)); text-align: center; }
.ev-cell:hover, .ev-cell[aria-pressed="true"] { background: var(--accent); color: var(--surface); }
.ev-cell:focus-visible, .ev-reset:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.ev-none { color: var(--muted); }
.ev-vh { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.ev-clear { margin: 8px 0 0; font-size: 12.5px; color: var(--muted); }
.ev-reset { all: unset; cursor: pointer; font: 500 12.5px/1 var(--font-body); padding: 5px 10px; border-radius: 999px; border: 1px solid var(--rule); color: var(--fg); margin-right: 6px; }
.ev-unk ul { margin: 4px 0 0; padding-left: 18px; font-size: 13.5px; line-height: 1.45; }
.ev-unk li { margin: 0 0 7px; }
.phase.dz { border-color: var(--accent); color: var(--accent); font-weight: 600; }
.phase.dz-0 { background: color-mix(in srgb, var(--accent) 14%, var(--surface)); }
.phase.dz-5 { border-style: dashed; }
dd.ovl { color: var(--muted); font-style: italic; }
@media print { .evmap .ev-cols { display: none; } }
'''
i = s.index("--font-display"); j = s.index("</style>", i); s = s[:j] + CSS + s[j:]

# ---- glossary and footer
G = [("aa-IPI","Age-adjusted International Prognostic Index"),("ALLG","Australasian Leukaemia and Lymphoma Group"),("CAR-T","Chimeric antigen receptor T-cell therapy"),("CHOP","Cyclophosphamide, doxorubicin, vincristine, prednisone"),("CLL/SLL","Chronic lymphocytic leukemia / small lymphocytic lymphoma"),("CNS","Central nervous system"),("ctDNA","Circulating tumor DNA"),("DLBCL","Diffuse large B-cell lymphoma"),("DSHNHL","German High-Grade Non-Hodgkin Lymphoma Study Group"),("ECOG","Eastern Cooperative Oncology Group (performance status)"),("EZB","Genetic subtype of DLBCL defined by EZH2 mutations and BCL2 translocations"),("FDG","Fluorodeoxyglucose"),("FISH","Fluorescence in situ hybridization"),("HR","Hazard ratio"),("IELSG","International Extranodal Lymphoma Study Group"),("IPI","International Prognostic Index"),("LDH","Lactate dehydrogenase"),("LYSA","Lymphoma Study Association"),("MInT","MabThera International Trial"),("MRI","Magnetic resonance imaging"),("MSTS","Musculoskeletal Tumor Society (functional score)"),("NCCN","National Comprehensive Cancer Network"),("PET/CT","Positron emission tomography with computed tomography"),("R-CHOP","Rituximab, cyclophosphamide, doxorubicin, vincristine, prednisone"),("RICOVER-60","Rituximab with CHOP over 60 years (trial)"),("SEER","Surveillance, Epidemiology, and End Results program (US cancer registry)"),("SUVmax","Maximum standardized uptake value"),("TROG","Trans-Tasman Radiation Oncology Group"),("WHO","World Health Organization")]
gl = '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl></details>' % (len(G), "".join("<dt>%s</dt><dd>%s</dd>" % g for g in G))
sub1(r'<details class="gloss">.*?</details>', gl)
FOOT = """<footer>
    How this page was built. PubMed was searched on """ + CHECKED + """ for primary bone lymphoma in title or abstract ("primary bone lymphoma", "primary lymphoma of bone", "lymphoma of bone", "osteolymphoma", "primary bone diffuse large B-cell lymphoma" and variants; 593 records), with added searches for circulating tumor DNA, genomics, unifocal versus multifocal disease, non-DLBCL histologies, CNS relapse and imaging. Included: studies in adults published since 2000 with about 20 or more patients with primary bone lymphoma, and smaller series or a case report only where nothing larger exists (circulating tumor DNA, non-DLBCL histologies, PET). Not included: pediatric series, single case reports otherwise, reviews, and papers on primary bone marrow lymphoma. Two studies of lymphoma with any skeletal involvement (DSHNHL, Held 2013; Ghione 2024) are included as context and are labelled as such on their cards. ClinicalTrials.gov was searched on the same date: no ongoing trial dedicated to primary bone lymphoma was found, so there are no "Trials to watch" or "New drugs to watch" lists for this topic; they will appear if that changes. Every result was checked against the paper's PubMed abstract; "not reported in abstract" means the figure needs the full text, and values marked "full paper" were checked against the full publication in PubMed Central. Each result is tagged "✓ abstract" or "✓ abstract + full paper" by what it was checked against. "Design" labels (prospective trial, multicenter retrospective, single-center series, registry or population-based, laboratory series, case report) describe the study type and are not a formal grade of evidence. "Definition used" gives each study's own definition of primary bone lymphoma as far as the abstract or full paper states it. "Overlap" notes cohorts that share patients. "What it adds" and "Limitations" are interpretive summaries, not data from the papers. "★ Core" marks studies selected as essential for teaching. "Free full text" links open the article in PubMed Central; "Free at publisher" links open a publisher page that is free to read; "Publisher" links open the publisher's page, where a subscription or institutional access may be needed; "Free copy (repository)" links open a legal free copy in a university repository (sometimes the authors' manuscript). Free copies were found with Unpaywall (""" + CHECKED + """). Source links go to the PubMed record (PMIDs checked against journal, volume, pages and first author). Commentaries are editorials or letters linked to the paper. Last checked: """ + CHECKED + """.
    <p class="sitedisc"><b>For education only.</b> This site summarizes published research and the author's views. It is not medical advice, a clinical practice guideline or a substitute for professional judgment; treatment decisions should rely on the primary literature, current guidelines, approved prescribing information and the individual patient. This is an independent project, not affiliated with any institution or company.</p>
    <p class="reportall">Comments and suggestions are welcome: <a href="mailto:andresferber@hotmail.com?subject=Landmark%20trials%20%28Primary%20bone%20lymphoma%29%3A%20comment">send a comment</a>. Spotted an error or a missing study? Use "Report an error" on any study. Both go to andresferber@hotmail.com.</p>
  </footer>"""
i = s.index("<footer>"); j = s.index("</footer>", i) + len("</footer>")
old_foot = s[i:j]
s = s[:i] + FOOT + s[j:]
io.open(out, "w", encoding="utf-8").write(s)
print("wrote", out, len(s), "| old footer tail:", old_foot[-900:])
