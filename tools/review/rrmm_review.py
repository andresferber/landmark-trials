"""Build the RRMM narrative review and insert it into rrmm-trials.html (pilot).
Every number below comes from a trial entry on the page; [[Trial name]] becomes a numbered
reference that jumps to that trial's card. Rerun safely: it replaces the previous review block."""
import re, html, sys

PAGE = 'rrmm-trials.html'
TITLE = 'The evolution of management of relapsed and refractory multiple myeloma, 2003–2026'
UPDATED = 'October 24, 2026'

TAKE = [
    'Relapse therapy has moved through four eras: proteasome inhibitor and immunomodulatory backbones, anti-CD38 triplets, new mechanisms with mixed fortunes, and T-cell redirection.',
    'Because lenalidomide and anti-CD38 antibodies now move to frontline and maintenance, the key questions at first relapse are lenalidomide refractoriness and prior anti-CD38 exposure, not the line number alone.',
    'Ciltacabtagene autoleucel (CARTITUDE-4) was the first cellular therapy to improve overall survival in myeloma, and it is approved from first relapse in lenalidomide-refractory disease.',
    'Teclistamab with daratumumab (MajesTEC-3) produced the largest progression-free survival effect yet seen in early relapse, but infection-related deaths remain a central concern with T-cell redirection.',
    'Accelerated approvals based on response rates have been withdrawn when confirmatory trials failed or showed a survival signal (panobinostat, melflufen, single-agent belantamab), a recurring lesson for trainees.',
    'The open problems are sequencing of BCMA-directed therapies, antigen escape, infection prevention and immune recovery, fixed-duration treatment, and access.',
]

TIMELINE = [
    ('2003', 'Bortezomib accelerated approval', 'bb'),
    ('2005', 'APEX: bortezomib full approval', 'bb'),
    ('2006', 'Lenalidomide-dexamethasone approved (MM-009/010)', 'bb'),
    ('2013', 'Pomalidomide approved (MM-003)', 'bb'),
    ('2015', 'Carfilzomib (ASPIRE), ixazomib and elotuzumab triplets; panobinostat accelerated approval', 'bb'),
    ('2016', 'Daratumumab triplets approved (CASTOR, POLLUX); carfilzomib-dexamethasone (ENDEAVOR)', 'cd38'),
    ('2019', 'Selinexor accelerated approval (STORM); venetoclax myeloma trials on partial clinical hold (BELLINI)', 'oth'),
    ('2020', 'Isatuximab (ICARIA-MM), DKd (CANDOR), SVd (BOSTON); belantamab accelerated approval', 'cd38'),
    ('2021', 'First CAR-T in myeloma (idecabtagene vicleucel); DPd and Isa-Kd; melflufen approved, then withdrawal announced; panobinostat withdrawn', 'imm'),
    ('2022', 'Ciltacabtagene autoleucel; teclistamab, the first BCMA bispecific; single-agent belantamab withdrawn (DREAMM-3)', 'imm'),
    ('2023', 'Talquetamab (first GPRC5D agent) and elranatamab', 'imm'),
    ('2024', 'CAR-T moves to earlier relapse (KarMMa-3, CARTITUDE-4)', 'imm'),
    ('2025', 'Linvoseltamab; belantamab returns in combination (BVd, DREAMM-7)', 'oth'),
    ('2026', 'Teclistamab-daratumumab at early relapse (MajesTEC-3); first phase 3 results for cereblon E3 ligase modulators (SUCCESSOR-2, EXCALIBER-RRMM); CANOVA misses its endpoint', 'imm'),
]

BODY = """
<h3>Why relapse management keeps changing</h3>
<p>Almost every patient with multiple myeloma relapses, and for two decades the relapsed setting has been where new drugs prove themselves before moving to frontline therapy. That pattern has a consequence that shapes every era described here: each successful relapse drug is soon used earlier, so the population that relapses next has already been exposed to it. Trials designed in one era therefore enrolled patients who look different from those seen in clinic a few years later.</p>

<h3>Era 1: proteasome inhibitor and immunomodulatory backbones (2003–2015)</h3>
<p>Bortezomib was the first new drug class in myeloma in decades. APEX randomized 669 patients after one to three prior therapies and showed higher response rates (38% vs 18%), longer time to progression (6.22 vs 3.49 months; HR 0.55) and better 1-year survival (80% vs 66%) than high-dose dexamethasone, converting the 2003 accelerated approval to full approval in 2005 [[APEX (Richardson)]]. Two parallel trials then established lenalidomide-dexamethasone, roughly doubling time to progression compared with dexamethasone alone (about 11 vs 4.7 months) [[MM-009 / MM-010 (Weber, Dimopoulos)]]. Pomalidomide followed for disease refractory to both lenalidomide and bortezomib, with modest absolute gains (median PFS 4.0 vs 1.9 months) but a backbone that later trials would build on [[MM-003 (San Miguel)]].</p>
<p>The next step was the triplet. Carfilzomib added to lenalidomide-dexamethasone prolonged median PFS from 17.6 to 26.3 months and more than tripled complete responses (31.8% vs 9.3%) [[ASPIRE (Stewart)]], and carfilzomib-dexamethasone doubled PFS compared with bortezomib-dexamethasone in a head-to-head trial [[ENDEAVOR (Dimopoulos)]]. The oral proteasome inhibitor ixazomib [[TOURMALINE-MM1 (Moreau)]] and the first monoclonal antibody, elotuzumab [[ELOQUENT-2 (Lonial)]], each improved PFS on the lenalidomide backbone, more modestly. Panobinostat showed that a PFS gain is not enough on its own: it was approved with substantial gastrointestinal toxicity and later withdrawn in the US when the confirmatory trial was not completed [[PANORAMA-1 (San-Miguel)]]. As lenalidomide moved into frontline and maintenance therapy, OPTIMISMM became the first phase 3 trial in an entirely lenalidomide-exposed population, establishing pomalidomide-bortezomib-dexamethasone for lenalidomide-refractory relapse [[OPTIMISMM (Richardson)]].</p>

<h3>Era 2: anti-CD38 triplets (2016–2021)</h3>
<p>Daratumumab changed the scale of benefit. Added to bortezomib-dexamethasone it raised 12-month PFS from 26.9% to 60.7% (HR 0.39) [[CASTOR (Palumbo)]], and added to lenalidomide-dexamethasone from 60.1% to 83.2% (HR 0.37) [[POLLUX (Dimopoulos)]]. Isatuximab confirmed the class effect with pomalidomide [[ICARIA-MM (Attal)]], and for lenalidomide-refractory patients anti-CD38 antibodies were paired with carfilzomib [[CANDOR (Dimopoulos)]] [[IKEMA (Moreau)]] and pomalidomide [[APOLLO (Dimopoulos)]], with PFS hazard ratios of 0.53 to 0.63. These regimens remain standard for patients whose disease is not yet refractory to anti-CD38 therapy. Their own success created the next problem: once daratumumab moved into frontline therapy, a growing share of patients reached first relapse already exposed to, or refractory to, both lenalidomide and an anti-CD38 antibody.</p>

<h3>Era 3: new mechanisms, and lessons from accelerated approval (2019–2026)</h3>
<p>Several new mechanisms were tested for triple-class-refractory disease. Selinexor, an XPO1 inhibitor, produced responses in 26% of heavily pretreated patients [[STORM (Chari)]] and, given weekly with bortezomib-dexamethasone, prolonged PFS at earlier relapse [[BOSTON (Grosicki)]], though its toxicity limits use. Venetoclax illustrates the value of biomarker selection: in an unselected population it prolonged PFS but caused more deaths, mainly from infection, prompting a partial clinical hold in 2019 [[BELLINI (Kumar)]]. The benefit appeared concentrated in t(11;14) disease, yet the randomized trial in that subgroup did not meet its PFS endpoint despite higher response rates [[CANOVA (Popat)]], so venetoclax remains off-label in myeloma.</p>
<p>Two accelerated approvals were withdrawn. Melflufen improved PFS but showed an overall survival signal against it (HR 1.10) [[OCEAN (Schjesvold)]]. Belantamab mafodotin, the first BCMA-directed drug, was approved on response rates with frequent corneal toxicity [[DREAMM-2 (Lonial)]] and withdrawn as monotherapy when its confirmatory trial failed (PFS HR 1.03) [[DREAMM-3 (Dimopoulos)]]. Its return in combination is instructive: with bortezomib-dexamethasone it nearly tripled median PFS compared with daratumumab-bortezomib-dexamethasone (36.6 vs 13.4 months; HR 0.41) [[DREAMM-7 (Hungria)]], and with pomalidomide-dexamethasone it improved PFS over pomalidomide-bortezomib-dexamethasone [[DREAMM-8 (Dimopoulos)]]. The US approval in October 2025 covered only the bortezomib combination, whereas the EU approved both. Ocular toxicity, requiring eye examinations and dose holds, remains the price of an off-the-shelf BCMA therapy that does not depend on T-cell fitness.</p>

<h3>Era 4: T-cell redirection (2021–2026)</h3>
<p>BCMA CAR-T therapy produced responses not previously seen in late-line disease: 73% with idecabtagene vicleucel [[KarMMa (Munshi)]] and 97%, with 67% stringent complete responses, with ciltacabtagene autoleucel [[CARTITUDE-1 (Berdeja)]]. Off-the-shelf bispecific antibodies followed, targeting BCMA [[MajesTEC-1 (Moreau)]] [[MagnetisMM-3 (Lesokhin)]] [[LINKER-MM1 (Bumma)]] and, for the first time, a non-BCMA target, GPRC5D, with talquetamab and its distinctive skin, nail and taste toxicity [[MonumenTAL-1 (Chari)]]. Response rates of roughly 60–70% after triple-class exposure came with cytokine release syndrome and a high burden of infection.</p>
<p>Randomized trials then moved these therapies earlier. Idecabtagene vicleucel tripled median PFS against standard regimens after two to four lines (13.3 vs 4.4 months), although early deaths before infusion in the CAR-T arm drew attention to bridging and manufacturing time [[KarMMa-3 (Rodriguez-Otero)]]. Ciltacabtagene autoleucel, in lenalidomide-refractory patients after one to three lines, reduced the risk of progression by about three-quarters and, with longer follow-up, improved overall survival (HR 0.55), the first cellular therapy to do so in myeloma [[CARTITUDE-4 (San-Miguel)]]. In 2026, teclistamab with daratumumab after one to three lines achieved 36-month PFS of 83.4% vs 29.7% (HR 0.17), with a complete response rate above 80%, but also a higher rate of deaths from adverse events (7.1% vs 5.9%) [[MajesTEC-3 (Costa)]].</p>

<h3>Where we are now</h3>
<p>Current practice, as summarized in the 2026 ASCO-Ontario living guideline and NCCN (version 5.2026, high-level positions only; regimen-specific NCCN placement was not checked for this review), favors a triplet at early relapse using drugs from classes the patient is not refractory to, with T-cell redirecting therapy chosen by principle rather than a fixed sequence. In practical terms, the first questions at relapse are whether the disease is refractory to lenalidomide and whether the patient has received an anti-CD38 antibody.</p>
<ul>
<li><b>Lenalidomide-sensitive, anti-CD38-naive:</b> anti-CD38 triplets remain effective options [[POLLUX (Dimopoulos)]] [[CASTOR (Palumbo)]].</li>
<li><b>Lenalidomide-refractory at first relapse:</b> options now include ciltacabtagene autoleucel for eligible patients [[CARTITUDE-4 (San-Miguel)]], teclistamab-daratumumab [[MajesTEC-3 (Costa)]], anti-CD38 combinations with carfilzomib or pomalidomide when the patient is anti-CD38-naive [[CANDOR (Dimopoulos)]] [[APOLLO (Dimopoulos)]], and belantamab combinations [[DREAMM-7 (Hungria)]] [[DREAMM-8 (Dimopoulos)]].</li>
<li><b>Triple-class-exposed disease:</b> BCMA CAR-T if not yet used, BCMA or GPRC5D bispecific antibodies, and, selectively, selinexor-based regimens or venetoclax for t(11;14) off-label.</li>
</ul>
<p>Choice among these depends on fitness, access to a certified cellular therapy center, manufacturing time, infection risk, prior BCMA exposure and patient preference. None of the available comparisons is head-to-head between CAR-T and bispecific antibodies.</p>

<h3>Open questions</h3>
<ul>
<li><b>Sequencing BCMA-directed therapy:</b> CAR-T, bispecifics and belantamab share a target; antigen loss and T-cell exhaustion may limit the second BCMA agent.</li>
<li><b>Infections and immune recovery:</b> hypogammaglobulinemia and infection deaths are now a leading toxicity of effective therapy; prophylaxis and immunoglobulin replacement are still being defined.</li>
<li><b>Fixed duration:</b> whether deep, MRD-negative responses to bispecifics allow treatment to stop.</li>
<li><b>Comparators:</b> several trials used control arms that clinicians questioned as outdated for exposed populations; trial results must be read against the patient's actual prior therapy.</li>
<li><b>Endpoints:</b> the withdrawals of panobinostat, melflufen and single-agent belantamab show why overall survival and confirmatory trials matter.</li>
<li><b>Access:</b> cellular therapy capacity, cost and travel limit who benefits.</li>
</ul>

<h3>What is coming</h3>
<p>The next class is already reporting. Cereblon E3 ligase modulators (CELMoDs) degrade the same targets as lenalidomide and pomalidomide more potently and retain activity in refractory disease. Mezigdomide with carfilzomib-dexamethasone more than doubled median PFS (18.0 vs 8.3 months; HR 0.48) in a population that was largely refractory to both lenalidomide and an anti-CD38 antibody, at the cost of more neutropenia and infection [[SUCCESSOR-2 (Dimopoulos)]], and its US application is under review. Iberdomide with daratumumab-dexamethasone doubled the MRD-negative complete response rate compared with daratumumab-bortezomib-dexamethasone, with PFS still to come [[EXCALIBER-RRMM (Lonial)]]. CELMoDs could offer an oral, off-the-shelf alternative or partner to T-cell redirection.</p>
<p>Ongoing phase 3 trials (listed under Trials to watch at the end of this page) test talquetamab combinations, elranatamab and linvoseltamab against standard regimens, and new CAR-T products, including anitocabtagene autoleucel and the GPRC5D-directed arlocabtagene autoleucel. Their results will decide whether immunotherapy becomes the default at first relapse.</p>
"""


def build(h):
    names = re.findall(r'n:"([^"]+)"', h)
    cites = dict(re.findall(r'n:"([^"]+)".*?c:"([^"]+)"', h, flags=re.S))
    pmids = dict(re.findall(r'n:"([^"]+)".*?p:(\d+)', h, flags=re.S))
    slug = lambda s: re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', s.lower()))
    order = []

    def ref(m):
        n = m.group(1)
        if n not in names:
            sys.exit('unknown trial ' + n)
        if n not in order:
            order.append(n)
        i = order.index(n) + 1
        return f'<sup><a class="rref" href="#t-rrmm-{slug(n)}" data-slug="{slug(n)}" title="{html.escape(n)}">{i}</a></sup>'
    body = re.sub(r'\s*\[\[([^\]]+)\]\]', ref, BODY.strip())
    refs = ''.join(
        f'<li><a class="rref" href="#t-rrmm-{slug(n)}" data-slug="{slug(n)}">{html.escape(n)}</a>. {html.escape(cites[n])}. '
        f'<a href="https://pubmed.ncbi.nlm.nih.gov/{pmids[n]}/" target="_blank" rel="noopener">PubMed ↗</a></li>' for n in order)
    take = ''.join(f'<li>{html.escape(t)}</li>' for t in TAKE)
    tl = ''.join(f'<li class="tl-{c}"><span class="tl-y">{y}</span><span class="tl-e">{html.escape(e)}</span></li>' for y, e, c in TIMELINE)
    words = len(re.sub(r'<[^>]+>', ' ', body).split())
    block = f'''  <details class="review" id="review">
    <summary><span class="rv-kicker">Perspective</span><span class="rv-title">{TITLE}</span><span class="rv-open">Read the perspective</span></summary>
    <div class="rv-body">
      <p class="rv-meta">Andres Ferber, MD, with the assistance of Claude (Anthropic) · Last updated {UPDATED} · About {round(words, -2):,} words. Numbers are taken from the verified trial entries on this page; numbered references jump to each trial.</p>
      <p class="rv-disc"><b>Personal perspective, for education only.</b> This text reflects the author's own reading and opinion of the published evidence. It is not a clinical practice guideline, medical advice or a substitute for clinical judgment. Patient care should follow the primary literature, current guidelines (such as NCCN, ESMO, IMWG and ASCO), approved prescribing information and the individual patient's circumstances.</p>
      <div class="rv-take"><h3>Key points</h3><ul>{take}</ul></div>
      <figure class="rv-tl"><figcaption>Timeline of key trials and US regulatory milestones</figcaption><ol>{tl}</ol></figure>
      {body}
      <h3>References</h3>
      <ol class="rv-refs">{refs}</ol>
      <div class="rv-endbar"><button type="button" class="rv-close">Close the perspective ▴</button></div>
    </div>
  </details>
'''
    return block, len(order), words


CSS = '''
/* Added Oct 24, 2026: narrative review (collapsible reader view) */
.review { margin-top: 18px; border: 1px solid var(--rule); border-radius: 12px; background: var(--surface); }
.review > summary { list-style: none; cursor: pointer; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; padding: 14px 18px; }
.review > summary::-webkit-details-marker { display: none; }
.review .rv-kicker { font: 500 11px/1 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
.review .rv-title { font-family: var(--font-display); font-weight: 650; font-size: 1.05rem; flex: 1 1 260px; }
.review .rv-open { font: 500 13px/1 var(--font-body); padding: 8px 14px; border-radius: 999px; border: 1px solid var(--rule); background: var(--bg); color: var(--fg); }
.review[open] .rv-open::before { content: "Close "; }
.review[open] .rv-open { font-size: 0; }
.review[open] .rv-open::before { font-size: 13px; }
.review .rv-body { padding: 0 18px 18px; max-width: 72ch; font-size: 15.5px; line-height: 1.65; }
.review .rv-body h3 { font-family: var(--font-display); font-weight: 650; font-size: 1.12rem; margin: 22px 0 6px; }
.review .rv-body p { margin: 0 0 12px; }
.review .rv-body ul { margin: 0 0 12px; padding-left: 20px; }
.review .rv-body li { margin: 4px 0; }
.review .rv-meta { font-size: 12.5px; color: var(--muted); }
.review .rv-disc { font-size: 13px; line-height: 1.5; color: var(--fg); background: var(--s-old-bg); border: 1px solid var(--rule); border-radius: 8px; padding: 10px 12px; margin: 8px 0 14px; }
.review .rv-take { border-left: 3px solid var(--accent); background: var(--bg); padding: 4px 14px 6px; margin: 12px 0 16px; border-radius: 0 8px 8px 0; }
.review .rv-take h3 { margin-top: 10px; }
.review sup a { font: 600 11px var(--font-mono); text-decoration: none; color: var(--accent); padding: 0 1px; }
.review a { color: var(--accent); }
.review .rv-refs { font-size: 13.5px; padding-left: 22px; }
.review .rv-endbar { display: flex; justify-content: center; margin: 18px 0 2px; }
.review .rv-close { all: unset; cursor: pointer; font: 500 13px/1 var(--font-body); padding: 9px 16px; border-radius: 999px; border: 1px solid var(--rule); background: var(--bg); color: var(--fg); }
.review .rv-close:hover { border-color: var(--accent); color: var(--accent); }
.review .rv-close:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
@media print { .review .rv-endbar { display: none; } }
.rv-tl { margin: 8px 0 18px; }
.rv-tl figcaption { font: 500 11px/1.6 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
.rv-tl ol { list-style: none; margin: 0; padding: 0 0 0 4px; border-left: 2px solid var(--rule); }
.rv-tl li { position: relative; display: grid; grid-template-columns: 48px minmax(0, 1fr); gap: 10px; padding: 5px 0 5px 14px; font-size: 14px; line-height: 1.45; }
.rv-tl li::before { content: ""; position: absolute; left: -7px; top: 10px; width: 10px; height: 10px; border-radius: 50%; background: var(--surface); border: 2px solid var(--muted); }
.rv-tl li.tl-bb::before { border-color: var(--s-old); background: var(--s-old-bg); }
.rv-tl li.tl-cd38::before { border-color: var(--s-young); background: var(--s-young-bg); }
.rv-tl li.tl-oth::before { border-color: var(--s-p2); background: var(--s-p2-bg); }
.rv-tl li.tl-imm::before { border-color: var(--s-rr); background: var(--s-rr-bg); }
.rv-tl .tl-y { font: 500 13px var(--font-mono); color: var(--muted); }
@media print { .review { break-inside: auto; } .review .rv-open { display: none; } }
'''

JUMP = '''
(function setupReviewRefs(){
  const listEl = document.getElementById("list");
  const box = listEl.parentNode.querySelector(".review");
  if (!box) return;
  box.addEventListener("click", e => {
    if (e.target.closest(".rv-close")) {
      box.open = false;
      box.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    const a = e.target.closest("a.rref");
    if (!a) return;
    e.preventDefault();
    const first = chipsEl.querySelector(".chip");
    if (first && first.getAttribute("aria-pressed") !== "true") first.click();
    if (qEl.value) { qEl.value = ""; render(); }
    const li = listEl.querySelector('li[data-trial="' + a.getAttribute("data-slug") + '"]');
    if (!li) return;
    li.scrollIntoView({ behavior: "smooth", block: "start" });
    li.classList.remove("flash"); void li.offsetWidth; li.classList.add("flash");
  });
})();
'''

h = open(PAGE, encoding='utf-8').read()
block, nrefs, words = build(h)
if '<details class="review"' in h:
    h = re.sub(r'  <details class="review".*?</details>\n', lambda m: block, h, count=1, flags=re.S)
else:
    a = '  </header>\n'
    assert h.count(a) == 1
    h = h.replace(a, a + '\n' + block, 1)
    i = h.index('--font-display'); j = h.index('</style>', i); h = h[:j] + CSS + h[j:]
    a = '(function setupShare(){'
    assert h.count(a) == 1
    h = h.replace(a, JUMP + a, 1)
open(PAGE, 'w', encoding='utf-8').write(h)
print('refs', nrefs, 'words', words)
