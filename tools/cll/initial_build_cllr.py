"""One-time build of the relapsed/refractory CLL page (key cllr) from the relapsed FL page, November 12, 2026.
Usage (from the repository root): python3 tools/cll/initial_build_cllr.py <out.html>
After this first build the page itself (source/cllr.html) is the master copy: edit it directly, as for other topics
(tools/UPDATE_GUIDE.md). Then run, from tools/: mechs/install_mechtab.py, review/build_persp.py cllr, review/install_persptint.py."""
import re, json, sys, urllib.parse
out = sys.argv[1]
s = open('source/flr.html', encoding='utf-8').read()
KEY, TITLE = 'cllr', 'Relapsed chronic lymphocytic leukemia'
CHECKED = 'November 12, 2026'

def sub1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

sub1('<title>Relapsed Follicular Lymphoma</title>', '<title>Relapsed chronic lymphocytic leukemia</title>')
sub1('<div class="eyebrow">Relapsed/refractory follicular lymphoma · 2002–2026</div>', '<div class="eyebrow">Relapsed/refractory chronic lymphocytic leukemia · 2002–2026</div>')
sub1('<h1>Landmark trials in relapsed and refractory follicular lymphoma</h1>', '<h1>Landmark trials in relapsed and refractory chronic lymphocytic leukemia</h1>')
s = re.sub(r'(<h1>Landmark trials in relapsed and refractory chronic lymphocytic leukemia</h1>\s*<p>).*?(</p>)',
           lambda m: m.group(1) + 'From chemoimmunotherapy and antibodies to BTK inhibitors and their head-to-head trials, venetoclax-based fixed-duration therapy, the rise and fall of PI3K inhibitors, and treatment after both a BTK and a BCL2 inhibitor: design, verified results, context, open questions and reception.' + m.group(2), s, count=1, flags=re.S)
enc = urllib.parse.quote('Landmark trials (%s): comment' % TITLE, safe='')
old = 'Landmark%20trials%20%28Relapsed%20follicular%20lymphoma%29%3A%20comment'
assert s.count(old) == 2; s = s.replace(old, enc)
s = s.replace('"fl2-sort"', '"cllr-sort"')
# a fifth category colour (neutral outline), as on the relapsed myeloma page
sub1('.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }',
     '.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }\n.tag.risk { color: var(--muted); background: var(--bg); box-shadow: inset 0 0 0 1px var(--rule); }')

# data
ent = open('tools/cll/cllr_entries.js', encoding='utf-8').read()
i, j = s.index('const SETTINGS = {'), s.index('const REG = ')
s = s[:i] + ent.rstrip() + '\n' + s[j:]

REG = {"PCYC-1102 (Byrd)": ["NCT01105247"], "RESONATE (Byrd)": ["NCT01578707"], "HELIOS (Chanan-Khan)": ["NCT01611090"],
 "ACE-CL-001 (Byrd)": ["NCT02029443"], "ASCEND (Ghia)": ["NCT02970318"], "ELEVATE-RR (Byrd)": ["NCT02477696"], "ALPINE (Brown)": ["NCT03734016"],
 "BRUIN CLL-314 (Woyach)": ["NCT05254743"], "M13-982 (Stilgenbauer)": ["NCT01889186"], "M14-032 (Jones)": ["NCT02141282"],
 "MURANO (Seymour)": ["NCT02005471"], "VENICE-1 (Kater)": ["NCT02756611"], "BRUIN CLL-322 (Davids)": ["NCT04965493"],
 "Study 116 (Furman)": ["NCT01539512"], "Study 115 (Zelenetz)": ["NCT01569295"], "Study 119 (Jones)": ["NCT01659021"], "DUO (Flinn)": ["NCT02004522"],
 "BRUIN (Mato)": ["NCT03740529"], "TRANSCEND CLL 004 (Siddiqi)": ["NCT03331198"], "BRUIN CLL-321 (Sharman)": ["NCT04666038"],
 "Hx-CD20-406 (Wierda)": ["NCT00349349"]}
FT = {"PCYC-1102 (Byrd)": ["pmc", "PMC3772525"],
 "RESONATE (Byrd)": ["pmc", "PMC4134521"],
 "HELIOS (Chanan-Khan)": ["doi", "10.1016/S1470-2045(15)00465-9"],
 "ACE-CL-001 (Byrd)": ["pmc", "PMC4862586"],
 "ASCEND (Ghia)": ["doi", "10.1200/JCO.19.03355"],
 "ELEVATE-RR (Byrd)": ["pmc", "PMC8547923"],
 "ALPINE (Brown)": ["doi", "10.1056/NEJMoa2211582", "repo", "https://ruj.uj.edu.pl/xmlui/handle/item/306726"],
 "BRUIN CLL-314 (Woyach)": ["pmc", "PMC12904240"],
 "M13-982 (Stilgenbauer)": ["doi", "10.1016/S1470-2045(16)30019-5", "repo", "https://ruj.uj.edu.pl/xmlui/handle/item/102232"],
 "M14-032 (Jones)": ["pmc", "PMC6027999"],
 "MURANO (Seymour)": ["doi", "10.1056/NEJMoa1713976", "free"],
 "VENICE-1 (Kater)": ["doi", "10.1016/S1470-2045(24)00070-6", "free"],
 "BRUIN CLL-322 (Davids)": ["pmc", "PMC13634592"],
 "Study 116 (Furman)": ["pmc", "PMC4161365"],
 "Study 115 (Zelenetz)": ["pmc", "PMC5589180"],
 "Study 119 (Jones)": ["doi", "10.1016/S2352-3026(17)30019-4"],
 "DUO (Flinn)": ["pmc", "PMC6284216"],
 "BRUIN (Mato)": ["doi", "10.1056/NEJMoa2300696", "repo", "https://ruj.uj.edu.pl/xmlui/handle/item/317128"],
 "TRANSCEND CLL 004 (Siddiqi)": ["pmc", "PMC11753452"],
 "BRUIN CLL-321 (Sharman)": ["pmc", "PMC12288890"],
 "Alemtuzumab after fludarabine (Keating)": ["doi", "10.1182/blood.v99.10.3554"],
 "Hx-CD20-406 (Wierda)": ["pmc", "PMC4979101"],
 "REACH (Robak)": ["doi", "10.1200/JCO.2009.26.4556"]}
TOX = {
 "PCYC-1102 (Byrd)": "Mostly grade 1–2: transient diarrhea, fatigue and upper respiratory tract infection; minimal hematologic toxicity.",
 "RESONATE (Byrd)": "Most frequent with ibrutinib: diarrhea, fatigue, pyrexia and nausea. Final analysis: hypertension 21% (grade ≥3, 9%) and atrial fibrillation 12% (grade ≥3, 6%); 16% stopped ibrutinib for adverse events.",
 "HELIOS (Chanan-Khan)": "Grade 3–4 events 77% vs 74%; neutropenia 54% vs 51%; thrombocytopenia 15% in each group.",
 "ACE-CL-001 (Byrd)": "Headache 43%, diarrhea 39%, weight gain 26%, mostly grade 1–2. Updated report: grade ≥3 neutropenia 14%, pneumonia 11%, hypertension 7%; atrial fibrillation 7% and major bleeding 5% (all grades).",
 "ASCEND (Ghia)": "Serious adverse events 29% (acalabrutinib), 56% (idelalisib-rituximab) and 26% (bendamustine-rituximab). Final results: discontinuation for adverse events 23%, 67% and 17%; atrial fibrillation or flutter 8% vs 3%; grade ≥3 infections 29% in both groups.",
 "ELEVATE-RR (Byrd)": "Atrial fibrillation or flutter 9.4% vs 16.0%; hypertension 9.4% vs 23.2% (full paper); grade ≥3 infections 30.8% vs 30.0%; discontinuation for adverse events 14.7% vs 21.3%.",
 "ALPINE (Brown)": "Fewer cardiac events and fewer discontinuations for adverse events with zanubrutinib. At 42.5 mo: atrial fibrillation or flutter 7.1% vs 17.0%; hypertension 27.2% vs 25.3%; cardiac deaths 0 vs 6.",
 "BRUIN CLL-314 (Woyach)": "Atrial fibrillation or flutter 2.4% vs 13.5% and hypertension 10.6% vs 15.1% (full paper); discontinuation for adverse events 9.7% vs 10.6% (full paper).",
 "M13-982 (Stilgenbauer)": "Grade 3–4 neutropenia 40%, infection 20%, anemia 18%, thrombocytopenia 15%; serious adverse events 55%.",
 "M14-032 (Jones)": "Grade 3–4 neutropenia 51%, thrombocytopenia 29%, anemia 29%; no treatment-related deaths.",
 "MURANO (Seymour)": "Grade 3–4 neutropenia more frequent with venetoclax-rituximab; grade 3–4 febrile neutropenia and infections less frequent than with bendamustine-rituximab; grade 3–4 tumor lysis syndrome 3.1%.",
 "VENICE-1 (Kater)": "Grade ≥3 adverse events 79%; neutropenia 37%; serious adverse events 53%, most often pneumonia (8%); deaths from adverse events 5%, one possibly related to venetoclax.",
 "BRUIN CLL-322 (Davids)": "Grade ≥3 adverse events 79% vs 73%; grade ≥3 infections 34% vs 23% (full paper); grade ≥3 tumor lysis syndrome 1% vs 4%; atrial fibrillation or flutter 3% in each group; treatment-related deaths 1 vs 4.",
 "Study 116 (Furman)": "Serious adverse events 40% vs 35%; grade ≥3 aminotransferase elevations 5% with idelalisib (full paper). Long-term exposure: grade ≥3 diarrhea 16.4%, colitis 8.2%, pneumonitis 6.4%.",
 "Study 115 (Zelenetz)": "Grade ≥3 neutropenia 60% vs 47%; febrile neutropenia 23% with idelalisib; grade ≥3 infections 39% vs 25%; serious adverse events 68% vs 44%; deaths from adverse events 11% vs 7%.",
 "Study 119 (Jones)": "Grade ≥3 neutropenia 34% vs 16%, diarrhea 20% vs 1%, pneumonia 14% vs 8%; Pneumocystis pneumonia 5% vs 1%; treatment-related deaths 22 vs 6 (2:1 randomization).",
 "DUO (Flinn)": "Most common with duvelisib: diarrhea, neutropenia, pyrexia, nausea, anemia and cough; rates not reported in abstract. See the regulatory note on overall survival.",
 "BRUIN (Mato)": "Infections 71.0%, bleeding 42.6%, neutropenia 32.5%; hypertension 14.2%, atrial fibrillation or flutter 3.8%, major hemorrhage 2.2%; 2.8% stopped for a treatment-related adverse event.",
 "TRANSCEND CLL 004 (Siddiqi)": "Grade 3 cytokine release syndrome 9% (no grade 4–5); grade 3 neurological events 18% and grade 4 in 1%; one death related to treatment (macrophage activation syndrome).",
 "BRUIN CLL-321 (Sharman)": "Grade ≥3 adverse events 57.7% vs 73.4%; discontinuation for adverse events 17.2% vs 34.9%.",
 "Alemtuzumab after fludarabine (Keating)": "Infusion-related events, mostly grade 1–2 and in the first week; grade 3–4 infections 26.9%.",
 "Hx-CD20-406 (Wierda)": "Infusion reactions and infections, mainly grade 1–2; anemia and neutropenia.",
 "REACH (Robak)": "Grade 3–4 and serious adverse events slightly more frequent with FCR; rates not reported in abstract."}
master = json.load(open('tools/moa_master.json', encoding='utf-8'))
MOA = {k: master[k] for k in ['btk', 'bcl2L', 'pi3k', 'cd19car', 'cd20', 'cd52']}
B, V, P = ["btk"], ["bcl2L"], ["pi3k"]
MOAMAP = {"PCYC-1102 (Byrd)": B, "RESONATE (Byrd)": B, "HELIOS (Chanan-Khan)": B, "ACE-CL-001 (Byrd)": B, "ASCEND (Ghia)": B, "ELEVATE-RR (Byrd)": B,
 "ALPINE (Brown)": B, "BRUIN CLL-314 (Woyach)": B, "M13-982 (Stilgenbauer)": V, "M14-032 (Jones)": V, "MURANO (Seymour)": V, "VENICE-1 (Kater)": V,
 "BRUIN CLL-322 (Davids)": ["btk", "bcl2L"], "Study 116 (Furman)": P, "Study 115 (Zelenetz)": P, "Study 119 (Jones)": P, "DUO (Flinn)": P,
 "BRUIN (Mato)": B, "TRANSCEND CLL 004 (Siddiqi)": ["cd19car"], "BRUIN CLL-321 (Sharman)": B,
 "Alemtuzumab after fludarabine (Keating)": ["cd52"], "Hx-CD20-406 (Wierda)": ["cd20"], "REACH (Robak)": ["cd20"]}
NEWD = json.load(open('tools/newdrugs/cll.json', encoding='utf-8'))
WATCH = {"note": "Ongoing phase 3 trials selected from ClinicalTrials.gov (checked %s). Status and primary completion dates are as registered; some trials may already have presented results at meetings." % CHECKED,
 "items": [
  {"n": "CaDAnCe-302", "d": "BGB-16673 (BTK degrader) vs investigator's choice of idelalisib-rituximab, bendamustine-rituximab or venetoclax-rituximab retreatment, CLL/SLL previously treated with both a BTK and a BCL2 inhibitor", "ph": "Phase 3", "st": "Recruiting", "pcd": "2028-05-15 (estimated)", "ep": "PFS (independent review)", "nct": "NCT06846671"},
  {"n": "BGB-16673-304", "d": "BGB-16673 (BTK degrader) vs pirtobrutinib, relapsed or refractory CLL/SLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2028-04-17 (estimated)", "ep": "PFS (independent review)", "nct": "NCT06973187"},
  {"n": "NX-5948-306", "d": "NX-5948 (bexobrutideg, BTK degrader) vs pirtobrutinib, relapsed or refractory CLL/SLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2029-10 (estimated)", "ep": "PFS and ORR (independent review)", "nct": "NCT07516093"},
  {"n": "BGB-11417-303", "d": "Sonrotoclax with obinutuzumab or rituximab vs venetoclax-rituximab, relapsed or refractory CLL/SLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2029-09-30 (estimated)", "ep": "PFS (blinded independent review)", "nct": "NCT06943872"},
  {"n": "BELLWAVE-010", "d": "Nemtabrutinib-venetoclax vs venetoclax-rituximab, relapsed or refractory CLL/SLL after at least one prior therapy", "ph": "Phase 3", "st": "Recruiting", "pcd": "2032-06-01 (estimated)", "ep": "PFS (blinded independent review), after a dose-confirmation part", "nct": "NCT05947851"},
  {"n": "LP-168-US-CLL301", "d": "Rocbrutinib (LP-168) vs pirtobrutinib, relapsed or refractory CLL/SLL previously treated with a covalent BTK inhibitor", "ph": "Phase 3", "st": "Recruiting", "pcd": "2029-10-30 (estimated)", "ep": "PFS (independent review)", "nct": "NCT07342478"},
  {"n": "CaDAnCe-303", "d": "BGB-16673 (BTK degrader) vs investigator's choice, relapsed or refractory CLL/SLL previously treated with a covalent BTK inhibitor (sites in China and Taiwan)", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2029-11-30 (estimated)", "ep": "PFS (independent review)", "nct": "NCT06970743"},
  {"n": "DZ2024B0002", "d": "DZD8586 vs investigator's choice, relapsed or refractory CLL/SLL (sites in China)", "ph": "Phase 3", "st": "Recruiting", "pcd": "2029-01 (estimated)", "ep": "PFS (independent review)", "nct": "NCT07139873"}]}

def setconst(name, val):
    global s
    m = re.search(r'\nconst %s = (.*?);\n' % name, s)
    assert m and '\n' not in m.group(1), name
    s = s[:m.start(1)] + json.dumps(val, ensure_ascii=False) + s[m.end(1):]
for n, v in [('REG', REG), ('FT', FT), ('MOA', MOA), ('MOAMAP', MOAMAP), ('NEWD', NEWD), ('TOX', TOX), ('CORE', []), ('WATCH', WATCH)]:
    setconst(n, v)
sub1('const PAGEKEY = "flr";', 'const PAGEKEY = "%s";' % KEY)
sub1('const PAGETITLE = "Relapsed follicular lymphoma";', 'const PAGETITLE = "%s";' % TITLE)

names = re.findall(r'\n\{y:\d+,n:"([^"]+)"', ent)
for d in (REG, FT, TOX, MOAMAP):
    for k in d: assert k in names, k
for n in names: assert n in FT and n in TOX, n

GLOSS = {
 "AE": "Adverse event", "BCL2": "B-cell lymphoma 2 protein (target of venetoclax)", "BR": "Bendamustine, rituximab", "BTK": "Bruton tyrosine kinase",
 "CAR": "Chimeric antigen receptor", "CI": "Confidence interval", "CLL": "Chronic lymphocytic leukemia", "CR": "Complete response",
 "CRi": "Complete response with incomplete marrow recovery", "EU": "European Union", "FC": "Fludarabine, cyclophosphamide",
 "FCR": "Fludarabine, cyclophosphamide, rituximab", "FDA": "US Food and Drug Administration", "HR": "Hazard ratio",
 "ICANS": "Immune effector cell-associated neurotoxicity syndrome", "IGHV": "Immunoglobulin heavy-chain variable region gene (mutated or unmutated)",
 "iwCLL": "International Workshop on Chronic Lymphocytic Leukemia", "MRD": "Measurable (minimal) residual disease", "NCCN": "National Comprehensive Cancer Network",
 "ORR": "Overall response rate", "OS": "Overall survival", "PFS": "Progression-free survival", "PI3K": "Phosphatidylinositol 3-kinase",
 "PLCG2": "Phospholipase C gamma 2 gene, downstream of BTK", "PR": "Partial response", "SLL": "Small lymphocytic lymphoma",
 "TP53": "Tumor protein p53 gene; aberration means del(17p) or TP53 mutation", "del(17p)": "Deletion of the short arm of chromosome 17, the site of TP53",
 "del(11q)": "Deletion of the long arm of chromosome 11"}
gl = '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl></details>' % (
    len(GLOSS), ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in sorted(GLOSS.items(), key=lambda kv: kv[0].lower())))
s, n = re.subn(r'<details class="gloss">.*?</details>', lambda m: gl, s, count=1, flags=re.S); assert n == 1

FOOT = ('Every result was checked against the paper\'s PubMed abstract on %(d)s; values marked "full paper" were checked against the full text in PubMed Central, and "not reported in abstract" means the figure needs the full text. '
 '"Key toxicity" summarizes the main adverse events reported in the abstract; it is not a complete safety profile. '
 '"Drug mechanism" links one recent review per drug or drug class on how it works and how resistance develops, chosen from peer-reviewed journals as the most recent, comprehensive and high-quality review available (no promotional material), with free full text preferred when quality was comparable. '
 '"★ Core" marks trials selected as essential for teaching. '
 'Trials included: phase 3 trials, and phase 2 trials published in the New England Journal of Medicine or Nature Medicine, or in Blood or the Journal of Clinical Oncology when they led to an approval, changed a guideline or defined a regimen still in use, or otherwise practice-changing. '
 'Trials that compared BTK inhibitors with each other are listed here, including BRUIN CLL-314, which also enrolled untreated patients. UNITY-CLL (umbralisib-ublituximab) is not listed because no full report was found in PubMed. Maintenance and transplant trials and Richter transformation are not covered. '
 'Each result is tagged "✓ abstract" or "✓ abstract + full paper" by what it was checked against. '
 '"Free full text" links open the article in PubMed Central; "Free at publisher" links open a publisher page that is free to read; "Publisher" links open the publisher\'s page, where a subscription or institutional access may be needed; "Free copy (repository)" links open a legal free copy in a university repository (sometimes the authors\' manuscript). Free copies were found with Unpaywall (%(d)s). '
 'Registry links (NCT numbers) open the trial\'s registry record and were taken from each paper\'s PubMed record or abstract. '
 'Source links go to the PubMed record (PMIDs checked against journal, volume, pages and first author). '
 '"Builds on", "Changed" and "Open questions" are interpretive summaries, not data from the papers. Commentaries are those PubMed links to each paper ("Comment in"); letters and author replies are not listed. '
 'FDA approval dates given in full were confirmed against FDA announcements or published reports (%(d)s); items marked "verify" could not be confirmed and will be checked at the next update. '
 'Guideline placements marked "NCCN not checked" could not be confirmed, because the NCCN guidelines require a login. No public data report insurance approval rates; US coverage generally follows the FDA label and NCCN compendium listing. '
 'Last checked: %(d)s.') % {'d': CHECKED}
s, n = re.subn(r'(<footer>\s*)Every result was checked.*?(\s*<p class="sitedisc">)', lambda m: m.group(1) + FOOT + m.group(2), s, count=1, flags=re.S); assert n == 1
open(out, 'w', encoding='utf-8').write(s)
print('entries', len(names))
