"""Install the three-tab bar (Landmark trials | Trials to watch | New drugs to watch) plus a
"Send a comment" link on all six pages, with shared New-drugs lists per disease. Rerunnable."""
import json, re, urllib.parse

PM = lambda p: 'https://pubmed.ncbi.nlm.nih.gov/%s/' % p
CT = lambda n: 'https://clinicaltrials.gov/study/' + n
CHECKED = "October 24, 2026"
NOTE = ("Agents with a new mechanism, target or modality that are not yet approved for this disease, selected from peer-reviewed "
        "early-phase trials and major meetings. Early response rates often fall with more patients and longer follow-up; meeting data are not peer-reviewed.")

MYELOMA = json.load(open('newdrugs/myeloma.json'))
MYELOMA["note"] = NOTE
MYELOMA["scope"] = "This list is shared by the three myeloma topics: most new myeloma drugs are tested first in relapsed disease."

FL = {"checked": CHECKED, "note": NOTE,
 "scope": "This list is shared by the two follicular lymphoma topics.",
 "items": [
  {"n": "Golcadomide", "mod": "Oral small molecule (cereblon modulator)", "tgt": "Cereblon E3 ligase modulator (Ikaros/Aiolos degrader)",
   "ev": "Phase 1/2, meeting data (not yet peer-reviewed)", "pub": "EHA 2026",
   "why": "A next-generation cereblon modulator, more potent than lenalidomide, that also stimulates T cells; oral and chemotherapy-free, and active after lenalidomide and T-cell-redirecting therapy.",
   "data": "With rituximab, in patients with a median of three prior lines: ORR 97% and complete response 78% at 0.4 mg (36 evaluable); ORR 77% and complete response 41% at 0.2 mg (22 evaluable). Median follow-up 14 months.",
   "safety": "Grade 3–4 neutropenia 68% at 0.4 mg and 59% at 0.2 mg, the most common severe adverse event.",
   "next": "Phase 3 GOLSEEK-4: golcadomide-rituximab vs investigator's choice after at least one prior line (recruiting).",
   "src": [["EHA 2026 report (Blood Cancers Today)", "https://www.bloodcancerstoday.com/post/golcadomide-combo-produces-durable-responses-with-manageable-safety-in-relapsed-or-refractory-follicular-lymphoma"], ["NCT06911502", CT("NCT06911502")]]},
  {"n": "Surovatamig", "mod": "Bispecific antibody (new target in FL)", "tgt": "CD19 × CD3",
   "ev": "Phase 1, meeting data (not yet peer-reviewed)", "pub": "ASH 2025",
   "why": "A T-cell engager directed at CD19 rather than CD20, so it may remain active after anti-CD20 therapy and when CD20 is lost.",
   "data": "61 patients after ≥2 prior lines: complete response 86–100% across dose levels; estimated 12-month PFS 87.9%.",
   "safety": "Cytokine release syndrome 57%, all grade 1–2.",
   "next": "Phase 3 with rituximab vs chemoimmunotherapy in untreated FL (recruiting).",
   "src": [["ASH 2025 report (Lymphoma Hub)", "https://lymphomahub.com/medical-information/surovatamig-for-patients-with-rr-fl-3-year-follow-up-results"], ["NCT06549595", CT("NCT06549595")]]},
  {"n": "Loncastuximab tesirine with rituximab", "mod": "Antibody-drug conjugate", "tgt": "CD19 (pyrrolobenzodiazepine payload)",
   "ev": "Peer-reviewed phase 2 (single centre)", "pub": "Lancet Haematol 2025",
   "why": "A CD19-directed antibody-drug conjugate, approved for large B-cell lymphoma, tested as a time-limited outpatient option in FL, including POD24 disease.",
   "data": "39 patients after ≥1 line (51% with POD24): complete response at week 12 in 67%; median follow-up 18.2 months.",
   "safety": "Grade ≥3 lymphopenia 21% and neutropenia 13%; edema mostly grade 1–2; no treatment-related deaths.",
   "next": "Investigator-initiated phase 2 continuing; no phase 3 in FL identified.",
   "src": [["Alderuccio JP, Lancet Haematol 2025", PM("39662486")], ["NCT04998669", CT("NCT04998669")]]}
 ], "grad": [], "disc": []}

MCL = {"checked": CHECKED, "note": NOTE, "scope": "",
 "items": [
  {"n": "BTK degraders (BGB-16673, bexobrutideg)", "mod": "Oral protein degrader", "tgt": "BTK (degraded rather than inhibited)",
   "ev": "Phase 1, meeting data across B-cell malignancies (not yet peer-reviewed)", "pub": "ASH 2023 onward",
   "why": "Degrading BTK, rather than blocking it, can overcome resistance mutations that defeat covalent and noncovalent BTK inhibitors, a common route of relapse in MCL.",
   "data": "BGB-16673 first report (51 patients with B-cell malignancies, 80% after a covalent BTK inhibitor): ORR 57% overall and 56% in the combined Waldenström, mantle cell and marginal zone group; MCL-specific results are still small.",
   "safety": "Bleeding 42% (grade ≥3 in 4%), infections 40% (grade ≥3 in 16%); no atrial fibrillation or hypertension reported.",
   "next": "Phase 1/2 expansion; phase 3 trials so far are in CLL rather than MCL.",
   "src": [["ASH 2023 report (OncLive)", "https://www.onclive.com/view/bgb-16673-delivers-reponses-with-a-tolerable-safety-profile-across-r-r-b-cell-malignancies"], ["Montoya S, Science 2024 (resistance biology)", PM("38301010")]]},
  {"n": "Dual-target CD20/CD19 CAR-T (LV20.19)", "mod": "Autologous CAR-T, point-of-care manufacturing", "tgt": "CD20 and CD19",
   "ev": "Peer-reviewed phase 1/2", "pub": "J Clin Oncol 2025",
   "why": "Targeting two antigens to prevent CD19-negative escape, made on site in 8 to 12 days with a product enriched for naive and stem-cell-like T cells.",
   "data": "17 patients after ≥2 lines or relapse after transplant: ORR 100%, complete response 88%; median PFS and overall survival not reached at 15.8 months.",
   "safety": "Cytokine release syndrome 94%, all grade 1–2; ICANS 18% (grade 3 in 2, reversible).",
   "next": "Phase 1/2 only.",
   "src": [["Shah NN, J Clin Oncol 2025", PM("40163793")], ["NCT04186520", CT("NCT04186520")]]},
  {"n": "Zilovertamab vedotin", "mod": "Antibody-drug conjugate", "tgt": "ROR1 (new target)",
   "ev": "Peer-reviewed phase 1", "pub": "NEJM Evid 2022",
   "why": "ROR1 is an oncofetal protein present on MCL cells but largely absent from normal adult tissue, and it is upregulated in some relapses after CD19 CAR-T.",
   "data": "15 patients with heavily pretreated MCL: responses in 7 (47%), including 3 complete responses.",
   "safety": "Neutropenia and cumulative neuropathy, as expected with a monomethyl auristatin E payload; no unexpected ROR1-related toxicity.",
   "next": "Further development has focused on large B-cell lymphoma; no MCL-specific phase 3 identified.",
   "src": [["Wang ML, NEJM Evid 2022", PM("38319241")]]}
 ], "grad": [], "disc": []}

PAGES = {
 "mcl-trials": ("Mantle cell lymphoma", MCL),
 "smm-studies": ("Smoldering myeloma", MYELOMA),
 "ndmm-trials": ("Newly diagnosed myeloma", MYELOMA),
 "rrmm-trials": ("Relapsed/refractory myeloma", MYELOMA),
 "fl-untreated": ("Untreated follicular lymphoma", FL),
 "fl-relapsed": ("Relapsed follicular lymphoma", FL),
}

CSS = '''
/* Added Oct 24, 2026: section tabs, Trials to watch tab, New drugs to watch, comment link */
.tabs { display: flex; flex-wrap: wrap; align-items: center; gap: 4px; margin-top: 18px; padding: 6px 8px 0; background: #e6ecf6; background: color-mix(in srgb, var(--accent) 11%, var(--surface)); border: 1px solid var(--rule); border-radius: 10px 10px 0 0; }
.tabs button { all: unset; cursor: pointer; font: 600 14px/1 var(--font-body); padding: 12px 14px; color: var(--muted); border-bottom: 3px solid transparent; margin-bottom: -1px; }
.tabs button:hover { color: var(--fg); }
.tabs button { border-radius: 8px 8px 0 0; }
.tabs button:hover { background: var(--surface); }
.tabs button[aria-selected="true"] { color: var(--fg); background: var(--surface); border-bottom-color: var(--accent); }
.tabs button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.tabs .tcount { font: 500 11px var(--font-mono); color: var(--muted); margin-left: 6px; }
.tabs .tabmail { margin-left: auto; font: 500 13px/1 var(--font-body); color: var(--accent); text-decoration: none; padding: 8px 4px; }
.tabs .tabmail:hover { text-decoration: underline; }
.newdrugs[hidden] { display: none; }
.newdrugs { padding-top: 12px; }
.newdrugs .nd-note { font-size: 13.5px; color: var(--muted); margin: 4px 0 14px; max-width: 72ch; }
.newdrugs .nd-mods { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px; }
.newdrugs .nd-item { border-top: 1px solid var(--rule); padding: 16px 0; display: flex; flex-direction: column; gap: 6px; }
.newdrugs .nd-top { display: flex; flex-wrap: wrap; gap: 8px; align-items: baseline; }
.newdrugs .nd-name { font-family: var(--font-display); font-weight: 650; font-size: 1.12rem; margin: 0; }
.newdrugs .nd-mod { font: 500 11px/1 var(--font-mono); letter-spacing: .04em; text-transform: uppercase; padding: 4px 7px; border-radius: 4px; color: var(--s-p2); background: var(--s-p2-bg); }
.newdrugs .nd-ev { font: 500 11.5px var(--font-mono); color: var(--muted); }
.newdrugs .nd-ev.pr { color: var(--s-young); }
.newdrugs dl { margin: 2px 0 0; }
.newdrugs a { color: var(--accent); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px; }
.newdrugs h3 { font-family: var(--font-display); font-weight: 650; font-size: 1.1rem; margin: 22px 0 6px; }
.newdrugs .nd-log { padding-left: 20px; }
.newdrugs .nd-log li { margin: 6px 0; font-size: 14px; }
.newdrugs .nd-rules { font-size: 12.5px; color: var(--muted); margin-top: 16px; max-width: 72ch; }
@media print { .tabs { display: none; } }
'''

JS = '''
(function setupTabs(){
  const listEl = document.getElementById("list");
  const root = listEl.parentNode;
  const tabs = root.querySelector(".tabs"), panel = root.querySelector(".newdrugs"), watch = root.querySelector(".watch"), controls = root.querySelector(".controls");
  if (!tabs) return;
  const L = (s) => '<a href="' + esc(s[1]) + '" target="_blank" rel="noopener">' + esc(s[0]) + ' ↗</a>';
  const nW = (typeof WATCH !== "undefined" && WATCH.items) ? WATCH.items.length : 0;
  const nD = (typeof NEWD !== "undefined") ? NEWD.items.length : 0;
  const cw = tabs.querySelector('[data-tab="watch"] .tcount'), cd = tabs.querySelector('[data-tab="newdrugs"] .tcount');
  if (cw) cw.textContent = nW; if (cd) cd.textContent = nD;
  let mod = "all";
  function draw(){
    if (!panel || !nD) return;
    const mods = [...new Set(NEWD.items.map(d => d.mod))];
    const items = NEWD.items.filter(d => mod === "all" || d.mod === mod);
    const log = (arr, none) => '<ul class="nd-log">' + (arr.length ? arr.map(g => '<li><b>' + esc(g.n) + ':</b> ' + esc(g.txt) + ' ' + g.src.map(L).join(" · ") + '</li>').join("") : '<li>' + none + '</li>') + '</ul>';
    panel.innerHTML = '<p class="nd-note">' + esc(NEWD.note) + (NEWD.scope ? ' ' + esc(NEWD.scope) : '') + ' Status checked ' + esc(NEWD.checked) + '.</p>' +
      (mods.length > 1 ? '<div class="nd-mods">' + [["all","All"]].concat(mods.map(m => [m, m])).map(([k, l]) => '<button type="button" class="chip" data-mod="' + esc(k) + '" aria-pressed="' + (k === mod) + '">' + esc(l) + '</button>').join("") + '</div>' : '') +
      items.map(d => '<div class="nd-item"><div class="nd-top"><h2 class="nd-name">' + esc(d.n) + '</h2><span class="nd-mod">' + esc(d.mod) + '</span><span class="nd-ev' + (/^Peer-reviewed/.test(d.ev) ? ' pr' : '') + '">' + esc(d.ev) + ' · ' + esc(d.pub) + '</span></div>' +
        '<dl><dt>Target</dt><dd>' + esc(d.tgt) + '</dd><dt>Why it matters</dt><dd>' + esc(d.why) + '</dd><dt>Key data</dt><dd>' + esc(d.data) + '</dd><dt>Safety</dt><dd>' + esc(d.safety) + '</dd><dt>Next step</dt><dd>' + esc(d.next) + '</dd><dt>Sources</dt><dd class="nd-src">' + d.src.map(L).join(" · ") + '</dd></dl></div>').join("") +
      '<h3>Moved on to phase 3 results</h3>' + log(NEWD.grad, "None so far.") +
      '<h3>Discontinued</h3>' + log(NEWD.disc, "None so far.") +
      '<p class="nd-rules">How this list is kept: agents with a new mechanism, target or modality (including phase 1 when the approach is new, and repurposed drugs with credible clinical data; no biosimilars and no preclinical-only agents). An agent moves to "Moved on" when phase 3 results are published, and to "Discontinued", with the reason and date, when development stops or a pivotal trial fails; discontinued entries are removed after 2 years. Checked at each scheduled update and after major meetings (ASH, ASCO, EHA, AACR, ESMO, IMS).</p>';
    panel.querySelectorAll(".nd-mods .chip").forEach(b => b.addEventListener("click", () => { mod = b.getAttribute("data-mod"); draw(); }));
  }
  draw();
  function show(which){
    tabs.querySelectorAll("button[data-tab]").forEach(x => x.setAttribute("aria-selected", x.getAttribute("data-tab") === which));
    if (controls) controls.style.display = which === "trials" ? "" : "none";
    listEl.style.display = which === "trials" ? "" : "none";
    if (watch) watch.style.display = (which === "newdrugs" || !nW) ? "none" : "";
    if (panel) panel.hidden = which !== "newdrugs";
  }
  tabs.addEventListener("click", e => {
    const b = e.target.closest("button[data-tab]"); if (!b) return;
    show(b.getAttribute("data-tab"));
  });
  show("trials");
})();
'''

def tab_html(title):
    subj = urllib.parse.quote('Landmark trials (' + title + '): comment')
    return ('  <div class="tabs" role="tablist" aria-label="Page sections">\n'
            '    <button type="button" role="tab" aria-selected="true" data-tab="trials">Landmark trials</button>\n'
            '    <button type="button" role="tab" aria-selected="false" data-tab="watch">Trials to watch<span class="tcount"></span></button>\n'
            '    <button type="button" role="tab" aria-selected="false" data-tab="newdrugs">New drugs to watch<span class="tcount"></span></button>\n'
            '    <a class="tabmail" href="mailto:andresferber@hotmail.com?subject=' + subj + '">✉ Send a comment</a>\n'
            '  </div>\n  <section class="newdrugs" hidden aria-label="New drugs to watch"></section>\n')

for f, (title, data) in PAGES.items():
    p = f + '.html'; h = open(p, encoding='utf-8').read()
    # remove previous pilot block, old CSS and old JS
    h = re.sub(r'<!--pilot-start-->.*?<!--pilot-end-->\n?', '', h, flags=re.S)
    h = re.sub(r'  <div class="tabs".*?</section>\n', '', h, count=1, flags=re.S)
    h = re.sub(r'\n/\* Added Oct 24, 2026: tabs and New drugs to watch \(pilot\) \*/.*?@media print \{ \.tabs \{ display: none; \} [^\n]*\n', '\n', h, flags=re.S)
    h = re.sub(r'\n/\* Added Oct 24, 2026: section tabs.*?@media print \{ \.tabs \{ display: none; \} \}\n', '\n', h, flags=re.S)
    h = re.sub(r'\n\(function setupNewDrugs\(\)\{.*?\n\}\)\(\);\n', '\n', h, flags=re.S)
    h = re.sub(r'\n\(function setupTabs\(\)\{.*?\n\}\)\(\);\n', '\n', h, flags=re.S)
    assert 'setupNewDrugs' not in h and '.tabs button' not in h, p
    # data
    line = 'const NEWD = ' + json.dumps(data, ensure_ascii=False) + ';\n'
    if 'const NEWD = ' in h:
        h = re.sub(r'const NEWD = .*?;\n', lambda m: line, h, count=1)
    else:
        a = 'const TOX = '; assert h.count(a) == 1
        h = h.replace(a, '// NEWD: new drugs to watch (shared per disease).\n' + line + a, 1)
    a = '  <div class="controls">'; assert h.count(a) == 1
    h = h.replace(a, tab_html(title) + '\n' + a, 1)
    i = h.index('--font-display'); j = h.index('</style>', i); h = h[:j] + CSS + h[j:]
    a = '(function setupShare(){'; assert h.count(a) == 1
    h = h.replace(a, JS + a, 1)
    open(p, 'w', encoding='utf-8').write(h)
    print(f, 'ok', len(data['items']))
