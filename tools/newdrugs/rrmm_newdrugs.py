"""Add the "New drugs to watch" tab (pilot) to rrmm-trials.html. Rerunnable: replaces the data line."""
import json, re, sys

PAGE = 'rrmm-trials.html'
PM = lambda p: 'https://pubmed.ncbi.nlm.nih.gov/%s/' % p
CT = lambda n: 'https://clinicaltrials.gov/study/' + n

ND = {
 "checked": "October 24, 2026",
 "note": "Agents with a new mechanism, target or modality that are not yet approved for myeloma, selected from peer-reviewed early-phase trials and major meetings. Early response rates often fall with more patients and longer follow-up; meeting data are not peer-reviewed.",
 "items": [
  {"n": "Cevostamab", "mod": "Bispecific antibody", "tgt": "FcRH5 × CD3 (new target)",
   "ev": "Peer-reviewed phase 1", "pub": "Nat Med 2026",
   "why": "A third T-cell-engager target after BCMA and GPRC5D, given as fixed-duration therapy (about 12 months).",
   "data": "324 patients, median 6 prior lines, 47.5% after BCMA therapy. ORR 42.1% overall; at the recommended 160 mg dose 44.3%, and 60.6% in BCMA-naive patients. Median duration of response 11.2 months.",
   "safety": "Grade 3–4 adverse events 59.6%; treatment-related deaths 0.9% (hemophagocytic lymphohistiocytosis in 2, sepsis with DIC in 1).",
   "next": "Phase 3 CEVOLUTION: cevostamab-pomalidomide-dexamethasone vs standard of care (recruiting).",
   "src": [["Cohen AD, Nat Med 2026", PM("42487061")], ["NCT07555938", CT("NCT07555938")]]},
  {"n": "Ramantamig", "mod": "Trispecific antibody", "tgt": "BCMA × GPRC5D × CD3",
   "ev": "Phase 1, meeting data (not yet peer-reviewed)", "pub": "ASCO 2025; preclinical paper Blood 2026",
   "why": "Engages two myeloma antigens at once, designed to counter antigen loss, a main cause of relapse after single-target T-cell redirection.",
   "data": "147 patients enrolled. At the recommended 100 mg dose every 4 weeks, ORR 100% in 27 patients naive to BCMA and GPRC5D therapy; 55% in previously exposed patients across doses.",
   "safety": "At the recommended dose, infections 80.6% (grade 3–4 in 33.3%); two deaths from infection with hypogammaglobulinemia across the trial. Cytokine release syndrome mostly grade 1.",
   "next": "Phase 3 TRIlogy-4 (vs a BCMA bispecific) and TRIlogy-5 (vs teclistamab), recruiting.",
   "src": [["Phase 1 report (OncLive, ASCO 2025)", "https://www.onclive.com/view/trispecific-antibody-jnj-79635322-is-safe-and-demonstrates-early-efficacy-signals-in-r-r-myeloma"], ["Pillarisetti K, Blood 2026 (preclinical)", PM("41100731")], ["NCT07258511", CT("NCT07258511")], ["NCT07518186", CT("NCT07518186")]]},
  {"n": "In vivo BCMA CAR-T (ESO-T01)", "mod": "In vivo CAR-T", "tgt": "BCMA",
   "ev": "Peer-reviewed phase 1 (5 patients)", "pub": "Nat Med 2026; Lancet 2025",
   "why": "A single infusion of a lentiviral vector creates CAR-T cells inside the body, with no leukapheresis, manufacturing wait or lymphodepleting chemotherapy.",
   "data": "5 patients, median 3 prior lines: 4 responses, including 3 stringent complete responses; MRD-negative in all 4 evaluable responders by day 60. Median follow-up 6.0 months.",
   "safety": "Cytokine release syndrome in 4 (grade 3 in 3); all patients had grade ≥3 adverse events, mostly cytopenias and transient liver enzyme rises.",
   "next": "The trial stopped enrolling early in 2025 and the registry lists it as suspended; other in vivo CAR-T programs are in phase 1.",
   "src": [["An N, Nat Med 2026", PM("41882404")], ["Xu J, Lancet 2025", PM("40617243")], ["NCT06691685", CT("NCT06691685")]]},
  {"n": "Allogeneic (off-the-shelf) BCMA CAR-T", "mod": "Allogeneic, gene-edited CAR-T", "tgt": "BCMA",
   "ev": "Peer-reviewed phase 1", "pub": "Nat Med 2023; Blood 2026",
   "why": "Donor-derived, gene-edited CAR-T cells available immediately, avoiding manufacturing delays and bridging therapy.",
   "data": "ALLO-715 (43 patients): ORR 55.8%; 70.8% at the selected dose and lymphodepletion, with median duration of response 8.3 months. CT0590, edited to resist host NK cells (5 patients): 3 responses, 2 stringent complete responses lasting about 20 months or more.",
   "safety": "ALLO-715: grade ≥3 infections 23.3%; cytokine release syndrome 55.8%, grade ≥3 in 2.3%. CT0590: no dose-limiting toxicity or graft-versus-host disease.",
   "next": "Phase 1 only; durability remains the main question.",
   "src": [["Mailankody S, Nat Med 2023", PM("36690811")], ["Jin S, Blood 2026", PM("42275247")]]},
  {"n": "Anitocabtagene autoleucel (anito-cel)", "mod": "Autologous CAR-T (new binder)", "tgt": "BCMA (synthetic D-domain binder)",
   "ev": "Peer-reviewed phase 1", "pub": "N Engl J Med 2026",
   "why": "A synthetic binder with a faster off-rate, designed to keep efficacy while lowering cytokine release and neurotoxicity.",
   "data": "38 patients after ≥3 lines: ORR 100%, complete response 79%. Median PFS 30.2 months; 36-month overall survival 65% (median follow-up 38.1 months).",
   "safety": "At the recommended dose, cytokine release syndrome 94%, all grade 1–2; ICANS 16% grade 1–2 and 1 grade 3; no delayed neurotoxicity.",
   "next": "Phase 3 iMMagine-3 vs standard regimens (active, not recruiting).",
   "src": [["Frigault MJ, N Engl J Med 2026", PM("42777241")], ["NCT06413498", CT("NCT06413498")]]},
  {"n": "Arlocabtagene autoleucel (arlo-cel)", "mod": "Autologous CAR-T", "tgt": "GPRC5D",
   "ev": "Peer-reviewed phase 1", "pub": "Blood 2026",
   "why": "A CAR-T against a non-BCMA target, active after prior BCMA therapy.",
   "data": "84 patients, median 5 prior regimens, 49% after BCMA therapy: ORR 87%, complete response 53%, median PFS 18.3 months, 1-year overall survival 90%.",
   "safety": "Cytokine release syndrome 82%, mostly grade 1–2; ICANS 10%; one death from cytokine release syndrome at the highest dose. Skin (30%), nail (19%) and oral (32%) effects, grade 1–2.",
   "next": "Phase 3 QUINTESSENTIAL-2 vs standard regimens in lenalidomide-exposed patients (recruiting).",
   "src": [["Bal S, Blood 2026", PM("42233419")], ["NCT06615479", CT("NCT06615479")]]},
  {"n": "Inobrodib", "mod": "Oral small molecule (epigenetic)", "tgt": "EP300/CBP bromodomain",
   "ev": "Phase 2 meeting data (not yet peer-reviewed); peer-reviewed preclinical and early clinical paper", "pub": "EMN 2026; Cancer Cell 2023",
   "why": "A new epigenetic mechanism that evicts EP300/CBP from oncogenic enhancer networks in myeloma; oral, and active after T-cell redirection.",
   "data": "Randomized dose optimization with pomalidomide-dexamethasone (61 patients, median 5 prior lines, 66% after BCMA or T-cell engager therapy): ORR 69% at 20 mg, 54% at 30 mg and 33% at 40 mg in 44 evaluable patients.",
   "safety": "Grade 3–4 adverse events 71%, mostly thrombocytopenia (36%), neutropenia (34%) and anemia (20%).",
   "next": "Phase 3 DOMMINO-2: inobrodib-pomalidomide-dexamethasone vs standard therapy (recruiting).",
   "src": [["Phase 2 abstract, EMN 2026 (Haematologica suppl.)", "https://haematologica.org/article/view/haematol.2026.s2.14069"], ["Nicosia L, Cancer Cell 2023", PM("37995682")], ["NCT07772024", CT("NCT07772024")]]}
 ],
 "grad": [
  {"n": "Mezigdomide (cereblon E3 ligase modulator)", "txt": "Phase 3 SUCCESSOR-2 (Lancet 2026): mezigdomide-carfilzomib-dexamethasone vs carfilzomib-dexamethasone, median PFS 18.0 vs 8.3 months (HR 0.48); grade 3–4 neutropenia 61% vs 9%. Candidate for the landmark list.", "src": [["Dimopoulos MA, Lancet 2026", PM("42289183")]]},
  {"n": "Iberdomide (cereblon E3 ligase modulator)", "txt": "Phase 3 EXCALIBER-RRMM (Lancet Oncol 2026): iberdomide-daratumumab-dexamethasone vs daratumumab-bortezomib-dexamethasone, MRD-negative complete response 41% vs 21%; PFS not yet reported. Candidate for the landmark list.", "src": [["Lonial S, Lancet Oncol 2026", PM("42790445")]]}
 ],
 "disc": []
}

CSS = '''
/* Added Oct 24, 2026: tabs and New drugs to watch (pilot) */
.tabs { display: flex; gap: 4px; margin-top: 18px; border-bottom: 1px solid var(--rule); }
.tabs button { all: unset; cursor: pointer; font: 600 14px/1 var(--font-body); padding: 12px 14px; color: var(--muted); border-bottom: 3px solid transparent; margin-bottom: -1px; }
.tabs button[aria-selected="true"] { color: var(--fg); border-bottom-color: var(--accent); }
.tabs button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.tabs .tcount { font: 500 11px var(--font-mono); color: var(--muted); margin-left: 6px; }
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
.newdrugs .nd-src a { color: var(--accent); }
.newdrugs h3 { font-family: var(--font-display); font-weight: 650; font-size: 1.1rem; margin: 22px 0 6px; }
.newdrugs .nd-log li { margin: 6px 0; font-size: 14px; }
.newdrugs .nd-rules { font-size: 12.5px; color: var(--muted); margin-top: 16px; max-width: 72ch; }
@media print { .tabs { display: none; } .newdrugs[hidden] { display: none !important; } }
'''

HTML = '''<!--pilot-start-->
  <div class="tabs" role="tablist" aria-label="Page sections">
    <button type="button" role="tab" aria-selected="true" data-tab="trials">Landmark trials</button>
    <button type="button" role="tab" aria-selected="false" data-tab="newdrugs">New drugs to watch<span class="tcount"></span></button>
  </div>
  <section class="newdrugs" hidden aria-label="New drugs to watch"></section>
<!--pilot-end-->
'''

JS = '''
(function setupNewDrugs(){
  const listEl = document.getElementById("list");
  const root = listEl.parentNode;
  const panel = root.querySelector(".newdrugs"), tabs = root.querySelector(".tabs");
  if (!panel || !tabs || typeof NEWD === "undefined") return;
  const L = (s) => '<a href="' + esc(s[1]) + '" target="_blank" rel="noopener">' + esc(s[0]) + ' ↗</a>';
  const mods = [...new Set(NEWD.items.map(d => d.mod))];
  let mod = "all";
  function draw(){
    const items = NEWD.items.filter(d => mod === "all" || d.mod === mod);
    panel.innerHTML = '<p class="nd-note">' + esc(NEWD.note) + ' Status checked ' + esc(NEWD.checked) + '.</p>' +
      '<div class="nd-mods">' + [["all","All"]].concat(mods.map(m => [m, m])).map(([k, l]) => '<button type="button" class="chip" data-mod="' + esc(k) + '" aria-pressed="' + (k === mod) + '">' + esc(l) + '</button>').join("") + '</div>' +
      items.map(d => '<div class="nd-item"><div class="nd-top"><h2 class="nd-name">' + esc(d.n) + '</h2><span class="nd-mod">' + esc(d.mod) + '</span><span class="nd-ev' + (/^Peer-reviewed/.test(d.ev) ? ' pr' : '') + '">' + esc(d.ev) + ' · ' + esc(d.pub) + '</span></div>' +
        '<dl><dt>Target</dt><dd>' + esc(d.tgt) + '</dd><dt>Why it matters</dt><dd>' + esc(d.why) + '</dd><dt>Key data</dt><dd>' + esc(d.data) + '</dd><dt>Safety</dt><dd>' + esc(d.safety) + '</dd><dt>Next step</dt><dd>' + esc(d.next) + '</dd><dt>Sources</dt><dd class="nd-src">' + d.src.map(L).join(" · ") + '</dd></dl></div>').join("") +
      (NEWD.grad.length ? '<h3>Moved on to phase 3 results</h3><ul class="nd-log">' + NEWD.grad.map(g => '<li><b>' + esc(g.n) + ':</b> ' + esc(g.txt) + ' ' + g.src.map(L).join(" · ") + '</li>').join("") + '</ul>' : '') +
      '<h3>Discontinued</h3><ul class="nd-log">' + (NEWD.disc.length ? NEWD.disc.map(g => '<li><b>' + esc(g.n) + ':</b> ' + esc(g.txt) + ' ' + g.src.map(L).join(" · ") + '</li>').join("") : '<li>None so far.</li>') + '</ul>' +
      '<p class="nd-rules">How this list is kept: agents with a new mechanism, target or modality (including phase 1 when the approach is new, and repurposed drugs with credible clinical data; no biosimilars and no preclinical-only agents). An agent moves to "Moved on" when phase 3 results are published, and to "Discontinued", with the reason and date, when development stops or a pivotal trial fails; discontinued entries are removed after 2 years. Checked at each scheduled update and after major meetings (ASH, ASCO, EHA, AACR, ESMO, IMS).</p>';
    panel.querySelectorAll(".nd-mods .chip").forEach(b => b.addEventListener("click", () => { mod = b.getAttribute("data-mod"); draw(); }));
  }
  draw();
  tabs.querySelector(".tcount").textContent = NEWD.items.length;
  const hideEls = [root.querySelector(".controls"), listEl, root.querySelector(".watch")];
  tabs.addEventListener("click", e => {
    const b = e.target.closest("button[data-tab]"); if (!b) return;
    tabs.querySelectorAll("button").forEach(x => x.setAttribute("aria-selected", x === b));
    const nd = b.getAttribute("data-tab") === "newdrugs";
    panel.hidden = !nd;
    hideEls.forEach(el => { if (el) el.style.display = nd ? "none" : ""; });
    if (!nd) renderWatchVisibility();
  });
  function renderWatchVisibility(){ const w = root.querySelector(".watch"); if (w && WATCH.items && WATCH.items.length) w.hidden = false; }
})();
'''

h = open(PAGE, encoding='utf-8').read()
line = 'const NEWD = ' + json.dumps(ND, ensure_ascii=False) + ';\n'
if 'const NEWD = ' in h:
    h = re.sub(r'const NEWD = .*?;\n', lambda m: line, h, count=1)
else:
    a = 'const TOX = '
    assert h.count(a) == 1
    h = h.replace(a, '// Added Oct 24, 2026 (pilot). NEWD: new drugs to watch.\n' + line + a, 1)
    a = '  <div class="controls">'
    assert h.count(a) == 1
    h = h.replace(a, HTML + '\n' + a, 1)
    i = h.index('--font-display'); j = h.index('</style>', i); h = h[:j] + CSS + h[j:]
    a = '(function setupShare(){'
    assert h.count(a) == 1
    h = h.replace(a, JS + a, 1)
open(PAGE, 'w', encoding='utf-8').write(h)
print('ok', len(ND['items']))
