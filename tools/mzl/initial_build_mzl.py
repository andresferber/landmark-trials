"""One-time build of the marginal zone lymphoma page (key mzl) from the relapsed FL page, November 14, 2026.
Usage (repository root): python3 tools/mzl/fetch_meta.py (network), then python3 tools/mzl/initial_build_mzl.py <out.html>
After this first build the page itself (source/mzl.html) is the master copy: edit it directly, as for other topics
(tools/UPDATE_GUIDE.md). Then run mechs/install_mechtab.py, review/build_persp.py mzl, review/install_persptint.py.
Differences from other topics: each entry has `sub` (subtypes enrolled, shown as the "Subtypes" row) and optional `also`
(subtype categories the trial also enrolled); a subtype chip shows its own category plus every entry whose `also` lists it."""
import re, json, sys, urllib.parse
sys.path.insert(0, 'tools/mzl')
import mzl_data as M
out = sys.argv[1]
s = open('source/flr.html', encoding='utf-8').read()
KEY, TITLE = 'mzl', 'Marginal zone lymphomas'
CHECKED = 'November 14, 2026'
def sub1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)
H1 = 'Landmark studies in marginal zone lymphomas'
sub1('<title>Relapsed Follicular Lymphoma</title>', '<title>Marginal zone lymphomas</title>')
sub1('<div class="eyebrow">Relapsed/refractory follicular lymphoma · 2002–2026</div>', '<div class="eyebrow">Marginal zone lymphomas · gastric MALT · non-gastric MALT · nodal · splenic · 2002–2026</div>')
sub1('<h1>Landmark trials in relapsed and refractory follicular lymphoma</h1>', '<h1>%s</h1>' % H1)
s = re.sub(r'(<h1>%s</h1>\s*<p>).*?(</p>)' % re.escape(H1),
    lambda m: m.group(1) + 'Gastric MALT lymphoma, non-gastric MALT lymphoma, nodal and splenic marginal zone lymphoma, with the trials that enrolled more than one subtype kept in groups of their own: antibiotics and antivirals, radiotherapy, rituximab and chemoimmunotherapy, BTK inhibitors, lenalidomide, PI3K inhibitors and CAR T cells, with the prognostic scores and genomic studies of each subtype. Each card states which subtypes were enrolled.' + m.group(2), s, count=1, flags=re.S)
enc = urllib.parse.quote('Landmark trials (%s): comment' % TITLE, safe='')
old = 'Landmark%20trials%20%28Relapsed%20follicular%20lymphoma%29%3A%20comment'
assert s.count(old) == 2; s = s.replace(old, enc)
s = s.replace('"fl2-sort"', '"mzl-sort"')
sub1('.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }',
     '.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }\n.tag.risk { color: var(--muted); background: var(--bg); box-shadow: inset 0 0 0 1px var(--rule); }\n'
     '.tag.mixed { color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--surface)); }\n'
     '.subnote { margin: 8px 0 0; font-size: 12.5px; color: var(--muted); }\ndd.subs { font-weight: 550; }')
sub1('<div class="chips" role="group" aria-label="Filter by category" id="chips"></div>',
     '<div class="chips" role="group" aria-label="Filter by category" id="chips"></div>\n    <p class="subnote">A subtype filter shows the studies of that subtype and, under separate headings, the studies that enrolled it together with other subtypes.</p>')

# ----- data -----
meta = json.load(open('tools/mzl/meta.json', encoding='utf-8'))
REG, FT, CM = meta['REG'], meta['FT'], meta['CM']
REG["MAGNOLIA (Opat)"] = ["NCT03846427"]; REG["CHRONOS-1 (Dreyling)"] = ["NCT01660451"]
FT["Pooled analysis of eradication (Zullo)"] = FT["Pooled analysis of eradication (Zullo)"][:2]   # the Unpaywall copy is on the publisher's own site
J = lambda v: json.dumps(v, ensure_ascii=False)
lines = ['const SETTINGS = {\n' + ',\n'.join('  %s: %s' % (k, J(l)) for k, l, c in M.SETTINGS) + '\n};',
         'const CLS = { ' + ', '.join('%s: "%s"' % (k, c) for k, l, c in M.SETTINGS) + ' };',
         'const order = ' + J([k for k, l, c in M.SETTINGS]) + ';',
         'const PM = id => "https://pubmed.ncbi.nlm.nih.gov/" + id + "/";', '', 'const T = [']
TOX, MOAMAP, names = {}, {}, []
for x in M.E:
    x = dict(x); n = x['n']; names.append(n)
    TOX[n] = x.pop('tox')
    if 'moa' in x: MOAMAP[n] = x.pop('moa')
    x['cm'] = CM[n]
    keys = ['y', 'n', 's', 'also', 'sub', 'ph', 'd', 'ep', 'r', 'N', 'hr', 'fu', 'c', 'p', 'extra', 'rel', 'b', 'i', 'q', 'cm', 'reg', 'gl', 'acc']
    assert set(x) <= set(keys), set(x) - set(keys)
    lines.append('{' + ','.join('%s:%s' % (k, J(x[k])) for k in keys if k in x) + '},')
lines.append('];')
i, j = s.index('const SETTINGS = {'), s.index('const REG = ')
s = s[:i] + '\n'.join(lines) + '\n' + s[j:]
master = json.load(open('tools/moa_master.json', encoding='utf-8'))
MOA = {k: master[k] for k in ['cd20', 'benda', 'btk', 'imidL', 'pi3k', 'cd19car']}
NEWD = json.load(open('tools/newdrugs/mzl.json', encoding='utf-8'))
WATCH = {"note": "Ongoing phase 3 trials selected from ClinicalTrials.gov (checked %s), with two randomized or large phase 2 trials that could change practice. Status and primary completion dates are as registered; some trials may already have presented results at meetings." % CHECKED,
 "items": [
  {"n": "MAHOGANY", "d": "Zanubrutinib with rituximab vs lenalidomide with rituximab in relapsed or refractory marginal zone lymphoma (and zanubrutinib-obinutuzumab vs lenalidomide-rituximab in follicular lymphoma); the confirmatory trial for zanubrutinib", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2028-07 (estimated)", "ep": "PFS (blinded independent review)", "nct": "NCT05100862"},
  {"n": "MARSUN", "d": "Mosunetuzumab-lenalidomide vs investigator's choice (rituximab-lenalidomide, rituximab-bendamustine or R-CHOP) in relapsed or refractory marginal zone lymphoma", "ph": "Phase 3", "st": "Recruiting", "pcd": "2027-09 (estimated)", "ep": "PFS (investigator)", "nct": "NCT06006117"},
  {"n": "RITZ", "d": "Rituximab with zanubrutinib vs rituximab alone in untreated, symptomatic splenic marginal zone lymphoma (IELSG48)", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2029-05 (estimated)", "ep": "PFS rate at 3 years", "nct": "NCT05735834"},
  {"n": "OLYMPIA-5", "d": "Odronextamab with lenalidomide vs rituximab with lenalidomide in relapsed or refractory follicular and marginal zone lymphoma", "ph": "Phase 3", "st": "Recruiting", "pcd": "2031-04-30 (estimated)", "ep": "Dose-limiting toxicities and adverse events (safety run-in); efficacy endpoints as registered", "nct": "NCT06149286"},
  {"n": "InMIND", "d": "Tafasitamab vs placebo, each with lenalidomide and rituximab, in relapsed or refractory follicular or marginal zone lymphoma; the follicular lymphoma results are published (Lancet 2026), those of the marginal zone cohort are not", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2024-02-23", "ep": "PFS in the follicular lymphoma population", "nct": "NCT04680052"},
  {"n": "ICP-CL-00123", "d": "Orelabrutinib with rituximab vs lenalidomide with rituximab in relapsed or refractory marginal zone lymphoma", "ph": "Phase 3", "st": "Recruiting", "pcd": "2028-08-31 (estimated)", "ep": "PFS (independent review)", "nct": "NCT06082102"},
  {"n": "ICP-CL-00136", "d": "Orelabrutinib with ICP-248 vs orelabrutinib alone in relapsed or refractory marginal zone lymphoma", "ph": "Phase 3", "st": "Not yet recruiting", "pcd": "2028-10 (estimated)", "ep": "Complete response rate and PFS (independent review)", "nct": "NCT07896590"},
  {"n": "25-089", "d": "Standard radiotherapy (24 Gy) vs a PET response-guided very low dose (4 Gy) staged strategy for potentially curable follicular and marginal zone lymphoma", "ph": "Phase 3", "st": "Recruiting", "pcd": "2028-06 (estimated)", "ep": "PFS", "nct": "NCT07029217"},
  {"n": "MALIBU", "d": "Ibrutinib with rituximab in untreated marginal zone lymphomas (extranodal, nodal and splenic); single arm, 175 patients (IELSG47)", "ph": "Phase 2", "st": "Active, not recruiting", "pcd": "2027-06-15 (estimated)", "ep": "Complete response rate at 12 months; PFS at 5 years", "nct": "NCT03697512"},
  {"n": "S2506", "d": "Mosunetuzumab alone vs with zanubrutinib vs with polatuzumab vedotin in relapsed or refractory marginal zone lymphoma (MOZART MZL)", "ph": "Phase 2 (randomized)", "st": "Not yet recruiting", "pcd": "2034-04-03 (estimated)", "ep": "Complete response rate", "nct": "NCT07638722"}]}
def setconst(name, val):
    global s
    m = re.search(r'\nconst %s = (.*?);\n' % name, s)
    assert m and '\n' not in m.group(1), name
    s = s[:m.start(1)] + J(val) + s[m.end(1):]
for n, v in [('REG', REG), ('FT', FT), ('MOA', MOA), ('MOAMAP', MOAMAP), ('NEWD', NEWD), ('TOX', TOX), ('CORE', []), ('WATCH', WATCH)]:
    setconst(n, v)
sub1('const PAGEKEY = "flr";', 'const PAGEKEY = "%s";' % KEY)
sub1('const PAGETITLE = "Relapsed follicular lymphoma";', 'const PAGETITLE = "%s";' % TITLE)
for d in (REG, FT, TOX, MOAMAP):
    for k in d: assert k in names, k
for n in names: assert n in FT and n in TOX, n

# ----- subtype row and subtype-aware filter -----
sub1('(active === "core" ? t.core : t.s === active)', '(active === "core" ? t.core : (t.s === active || (t.also || []).includes(active)))')
sub1('!q || [t.n,t.d,t.r,', '!q || [t.n,t.sub || "",t.d,t.r,')
sub1('<dt class="f-ep">Endpoint</dt>', '${t.sub ? `<dt>Subtypes</dt><dd class="subs">${esc(t.sub)}</dd>` : ""}\n          <dt class="f-ep">Endpoint</dt>')

GLOSS = {
 "AE": "Adverse event", "ALLG": "Australasian Leukaemia and Lymphoma Group", "API2-MALT1": "Fusion gene produced by t(11;18)(q21;q21)", "BTK": "Bruton tyrosine kinase",
 "CAR": "Chimeric antigen receptor", "CHOP": "Cyclophosphamide, doxorubicin, vincristine, prednisone", "CI": "Confidence interval", "CLL": "Chronic lymphocytic leukemia",
 "CR": "Complete response", "CT": "Computed tomography", "CVP": "Cyclophosphamide, vincristine, prednisone", "DMT": "Genetic cluster of splenic marginal zone lymphoma with DNA-damage response, MAPK and TLR lesions",
 "EFS": "Event-free survival", "EGILS": "European Gastro-Intestinal Lymphoma Study group", "EMA": "European Medicines Agency", "ESMO": "European Society for Medical Oncology", "EU": "European Union",
 "FDA": "US Food and Drug Administration", "FISH": "Fluorescence in situ hybridization", "FLIPI": "Follicular Lymphoma International Prognostic Index", "GELA": "Groupe d'Etude des Lymphomes de l'Adulte",
 "Gy": "Gray (unit of radiation dose)", "HCV": "Hepatitis C virus", "HPLL": "Prognostic score for splenic marginal zone lymphoma: hemoglobin, platelets, LDH, extrahilar lymphadenopathy",
 "HR": "Hazard ratio", "ICRU": "International Commission on Radiation Units and Measurements", "IELSG": "International Extranodal Lymphoma Study Group", "IIL": "Intergruppo Italiano Linfomi",
 "ILROG": "International Lymphoma Radiation Oncology Group", "IPI": "International Prognostic Index", "KLF2": "Krüppel-like factor 2 gene", "LDH": "Lactate dehydrogenase",
 "MALT": "Mucosa-associated lymphoid tissue; MALT lymphoma is extranodal marginal zone lymphoma", "MALT-IPI": "MALT lymphoma International Prognostic Index (age, stage, LDH)",
 "MZL-IPI": "Marginal Zone Lymphoma International Prognostic Index", "NCCN": "National Comprehensive Cancer Network", "NNK": "Genetic cluster of splenic marginal zone lymphoma with NF-κB, NOTCH and KLF2 lesions",
 "NOTCH2": "Notch receptor 2 gene, needed for marginal zone B-cell development", "OR": "Odds ratio", "ORR": "Overall (objective) response rate", "OS": "Overall survival",
 "PCR": "Polymerase chain reaction", "PEST": "Proline, glutamate, serine and threonine-rich domain that marks a protein for degradation", "PFS": "Progression-free survival",
 "PI3K": "Phosphatidylinositol 3-kinase", "pMRD": "Probable minimal residual disease (GELA grading)", "POD24": "Progression of disease within 24 months",
 "PTPRD": "Protein tyrosine phosphatase receptor type D gene", "R-CHOP": "Rituximab with CHOP", "R-CVP": "Rituximab with CVP", "RT-PCR": "Reverse-transcription polymerase chain reaction",
 "StiL": "Study group indolent Lymphomas (Germany)", "t(11;18)": "Translocation t(11;18)(q21;q21), producing API2-MALT1", "TROG": "Trans-Tasman Radiation Oncology Group",
 "Stage IE, II1E": "Lugano staging of gastrointestinal lymphoma: confined to the organ (IE); with local nodal involvement (II1E)"}
gl = '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl></details>' % (
    len(GLOSS), ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in sorted(GLOSS.items(), key=lambda kv: kv[0].lower())))
s, n = re.subn(r'<details class="gloss">.*?</details>', lambda m: gl, s, count=1, flags=re.S); assert n == 1

FOOT = ('Every result was checked against the paper\'s PubMed abstract on %(d)s; "not reported in abstract" means the figure needs the full text. '
 '"Subtypes" states which marginal zone lymphoma subtypes each study enrolled, with numbers where the abstract or full paper gives them. Studies that enrolled more than one subtype are grouped as "MALT lymphoma, gastric and non-gastric together" or "Trials across subtypes"; choosing a subtype filter shows them as well, under their own headings. '
 '"Key toxicity" summarizes the main adverse events reported in the abstract; it is not a complete safety profile. '
 '"Drug mechanism" links one recent review per drug or drug class on how it works and how resistance develops, chosen from peer-reviewed journals as the most recent, comprehensive and high-quality review available (no promotional material), with free full text preferred when quality was comparable. '
 '"★ Core" marks studies selected as essential for teaching. '
 'Studies included: few randomized trials exist and most evidence for the individual subtypes is observational, so the list holds every phase 3 or randomized trial with a full report that enrolled marginal zone lymphoma; the phase 2 trials that were the basis of an approval or that defined a regimen or drug class in current use, whatever the journal; the cohort studies of antibiotic, antiviral and radiation treatment on which practice rests; and the consensus statements, prognostic scores and genomic studies of each subtype. '
 'Primary cutaneous marginal zone lymphoma and pediatric nodal marginal zone lymphoma are not covered. Not listed as cards: idelalisib, duvelisib, parsaclisib, orelabrutinib, lenalidomide-rituximab in MALT lymphoma (a letter without an abstract), fludarabine-rituximab and autologous transplantation. '
 'Each result is tagged "✓ abstract" or "✓ abstract + full paper" by what it was checked against. '
 '"Free full text" links open the article in PubMed Central; "Free at publisher" links open a publisher page that is free to read; "Publisher" links open the publisher\'s page, where a subscription or institutional access may be needed; "Free copy (repository)" links open a legal free copy in a university repository (sometimes the authors\' manuscript). Free copies were found with Unpaywall (%(d)s). '
 'Registry links (NCT numbers) open the trial\'s registry record and were taken from each paper\'s PubMed record or abstract. '
 'Source links go to the PubMed record (PMIDs checked against journal, volume, pages and first author). '
 '"Builds on", "Changed" and "Open questions" are interpretive summaries, not data from the papers. Commentaries are those PubMed links to each paper ("Comment in"); letters and author replies are not listed. '
 'FDA dates given in full were confirmed against FDA announcements or the Federal Register (%(d)s); items marked "verify" could not be confirmed and will be checked at the next update. '
 'Guideline rows refer to the ESMO 2020 guideline, whose full text could not be read for this page, and are marked "not checked"; the NCCN guidelines require a login and were not checked. No public data report insurance approval rates; US coverage generally follows the FDA label and NCCN compendium listing. '
 'Last checked: %(d)s.') % {'d': CHECKED}
s, n = re.subn(r'(<footer>\s*)Every result was checked.*?(\s*<p class="sitedisc">)', lambda m: m.group(1) + FOOT + m.group(2), s, count=1, flags=re.S); assert n == 1
open(out, 'w', encoding='utf-8').write(s)
print('entries', len(names), 'moa', len(MOAMAP), 'reg', len(REG))
