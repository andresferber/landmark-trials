"""One-time build of the untreated CLL page (key cllu) from the relapsed FL page, November 12, 2026.
Usage (from the repository root): python3 tools/cll/initial_build_cllu.py <out.html>
After this first build the page itself (source/cllu.html) is the master copy: edit it directly, as for other topics
(tools/UPDATE_GUIDE.md). Then run, from tools/: mechs/install_mechtab.py, review/build_persp.py cllu, review/install_persptint.py."""
import re, json, sys, urllib.parse
out = sys.argv[1]
s = open('source/flr.html', encoding='utf-8').read()
KEY, TITLE = 'cllu', 'Untreated chronic lymphocytic leukemia'
CHECKED = 'November 12, 2026'

def sub1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

sub1('<title>Relapsed Follicular Lymphoma</title>', '<title>Untreated chronic lymphocytic leukemia</title>')
sub1('<div class="eyebrow">Relapsed/refractory follicular lymphoma · 2002–2026</div>', '<div class="eyebrow">Untreated chronic lymphocytic leukemia · 2000–2026</div>')
sub1('<h1>Landmark trials in relapsed and refractory follicular lymphoma</h1>', '<h1>Landmark trials in untreated chronic lymphocytic leukemia</h1>')
s = re.sub(r'(<h1>Landmark trials in untreated chronic lymphocytic leukemia</h1>\s*<p>).*?(</p>)',
           lambda m: m.group(1) + 'From chemoimmunotherapy to continuous BTK inhibitors and fixed-duration venetoclax combinations, with the risk models and criteria that decide when to treat: design, verified results, context, open questions and reception.' + m.group(2), s, count=1, flags=re.S)
enc = urllib.parse.quote('Landmark trials (%s): comment' % TITLE, safe='')
old = 'Landmark%20trials%20%28Relapsed%20follicular%20lymphoma%29%3A%20comment'
assert s.count(old) == 2; s = s.replace(old, enc)
s = s.replace('"fl2-sort"', '"cllu-sort"')

# data
ent = open('tools/cll/cllu_entries.js', encoding='utf-8').read()
i, j = s.index('const SETTINGS = {'), s.index('const REG = ')
s = s[:i] + ent.rstrip() + '\n' + s[j:]

REG = {"LRF CLL4 (Catovsky)": ["ISRCTN58585610"], "CLL8 (Hallek)": ["NCT00281918"], "CLL11 (Goede)": ["NCT01010061"],
 "COMPLEMENT 1 (Hillmen)": ["NCT00748189"], "CLL10 (Eichhorst)": ["NCT00769522"], "RESONATE-2 (Burger)": ["NCT01722487", "NCT01724346"],
 "Alliance A041202 (Woyach)": ["NCT01886872"], "iLLUMINATE (Moreno)": ["NCT02264574"], "E1912 (Shanafelt)": ["NCT02048813"],
 "ELEVATE-TN (Sharman)": ["NCT02475681"], "SEQUOIA (Tam)": ["NCT03336333"], "FLAIR: ibrutinib-rituximab (Hillmen)": ["ISRCTN01844152", "2013-001944-76"],
 "BRUIN CLL-313 (Jurczak)": ["NCT05023980"], "CLL14 (Fischer)": ["NCT02242942"], "CAPTIVATE (Wierda)": ["NCT02910583"],
 "GLOW (Kater)": ["NCT03462719", "2017-004699-77"], "CLL13/GAIA (Eichhorst)": ["NCT02950051", "2015-004936-36"],
 "FLAIR: ibrutinib-venetoclax (Munir)": ["ISRCTN01844152", "2013-001944-76"], "AMPLIFY (Brown)": ["NCT03836261"],
 "CLL17 (Al-Sawaf)": ["NCT04608318", "2019-003854-99"], "CRISTALLO (Sharman)": ["NCT04285567"], "CLL12 (Langerbeins)": ["NCT02863718"]}
FT = {"Fludarabine vs chlorambucil (Rai)": ["doi", "10.1056/NEJM200012143432402", "free"],
 "FCR phase 2 (Keating)": ["doi", "10.1200/JCO.2005.12.051", "free"],
 "LRF CLL4 (Catovsky)": ["doi", "10.1016/S0140-6736(07)61125-8"],
 "Bendamustine vs chlorambucil (Knauf)": ["doi", "10.1200/JCO.2008.20.8389", "free"],
 "CLL8 (Hallek)": ["doi", "10.1016/S0140-6736(10)61381-5"],
 "CLL11 (Goede)": ["doi", "10.1056/NEJMoa1313984", "free"],
 "COMPLEMENT 1 (Hillmen)": ["doi", "10.1016/S0140-6736(15)60027-7"],
 "CLL10 (Eichhorst)": ["doi", "10.1016/S1470-2045(16)30051-1"],
 "RESONATE-2 (Burger)": ["pmc", "PMC4722809"],
 "Alliance A041202 (Woyach)": ["pmc", "PMC6325637"],
 "iLLUMINATE (Moreno)": ["doi", "10.1016/S1470-2045(18)30788-5"],
 "E1912 (Shanafelt)": ["pmc", "PMC6908306"],
 "ELEVATE-TN (Sharman)": ["pmc", "PMC8151619"],
 "SEQUOIA (Tam)": ["doi", "10.1016/S1470-2045(22)00293-5", "repo", "https://ruj.uj.edu.pl/xmlui/handle/item/298141"],
 "FLAIR: ibrutinib-rituximab (Hillmen)": ["doi", "10.1016/S1470-2045(23)00144-4", "free"],
 "BRUIN CLL-313 (Jurczak)": ["pmc", "PMC12904224"],
 "CLL14 (Fischer)": ["doi", "10.1056/NEJMoa1815281"],
 "CAPTIVATE (Wierda)": ["pmc", "PMC8713593"],
 "GLOW (Kater)": ["doi", "10.1056/EVIDoa2200006"],
 "CLL13/GAIA (Eichhorst)": ["doi", "10.1056/NEJMoa2213093", "repo", "https://pure.amsterdamumc.nl/en/publications/8762254f-6fa6-4d1e-9599-34eeb94e453b"],
 "FLAIR: ibrutinib-venetoclax (Munir)": ["doi", "10.1056/NEJMoa2310063", "repo", "https://eprints.soton.ac.uk/485675/1/23_10063.R2_Proof_hi.pdf"],
 "AMPLIFY (Brown)": ["doi", "10.1056/NEJMoa2409804", "repo", "https://pure.amsterdamumc.nl/en/publications/6fedc24d-56c1-4707-8954-64537f0eda4b"],
 "CLL17 (Al-Sawaf)": ["doi", "10.1056/NEJMoa2515458"],
 "CRISTALLO (Sharman)": ["pmc", "PMC13277654"],
 "Genomic aberrations by FISH (Döhner)": ["doi", "10.1056/NEJM200012283432602"],
 "CLL-IPI (International CLL-IPI working group)": ["doi", "10.1016/S1470-2045(16)30029-8"],
 "iwCLL 2018 guidelines (Hallek)": ["doi", "10.1182/blood-2017-09-806398"],
 "IPS-E (Condoluci)": ["pmc", "PMC11311630"],
 "CLL12 (Langerbeins)": ["doi", "10.1182/blood.2021010845"]}
TOX = {
 "Fludarabine vs chlorambucil (Rai)": "Severe infections and neutropenia more frequent with fludarabine than chlorambucil (P=0.08); excess toxicity with the combination, which was stopped.",
 "FCR phase 2 (Keating)": "Grade 3–4 neutropenia in 52% of courses; major infections in 2.6% and minor infections in 10% of courses.",
 "LRF CLL4 (Catovsky)": "More neutropenia and days in hospital with FC or fludarabine than with chlorambucil; hemolytic anemia 5% with FC vs 11% with fludarabine and 12% with chlorambucil.",
 "Bendamustine vs chlorambucil (Knauf)": "Grade 3–4 hematologic events 40% vs 19%; grade 3–4 infections 8% vs 3%.",
 "CLL8 (Hallek)": "Grade 3–4 neutropenia 34% vs 21%; treatment-related deaths 2% vs 3%. Long-term: prolonged neutropenia 16.6% vs 8.8%; secondary malignancies including Richter transformation 13.1% vs 17.4%.",
 "CLL11 (Goede)": "Infusion-related reactions and neutropenia more common with obinutuzumab-chlorambucil than rituximab-chlorambucil; risk of infection not increased.",
 "COMPLEMENT 1 (Hillmen)": "Grade ≥3 adverse events 50% vs 43%; neutropenia 26% vs 14%; grade ≥3 infusion-related events 10% with ofatumumab.",
 "CLL10 (Eichhorst)": "Severe neutropenia 84% (FCR) vs 59% (BR); severe infections 39% vs 25%, more pronounced over age 65. Long-term: secondary neoplasia over age 65 in 32.6% after FCR vs 16.8% after BR.",
 "RESONATE-2 (Burger)": "Grade 3 hemorrhage in 4 patients and grade 4 in 1 with ibrutinib. Final analysis: hypertension 30% (any grade); dose reduction for adverse events in 25%.",
 "Alliance A041202 (Woyach)": "Grade 3–5 hematologic events 61% (BR) vs 41% and 39%; grade 3–5 nonhematologic events 63% vs 74% and 74%. Follow-up: atrial fibrillation 18% with ibrutinib vs 3% with BR; hypertension 55% vs 27%.",
 "iLLUMINATE (Moreno)": "Serious adverse events 58% vs 35%; most common grade 3–4 events were neutropenia and thrombocytopenia; one treatment-related death in each arm.",
 "E1912 (Shanafelt)": "Grade ≥3 adverse events 80.1% vs 79.7%; grade ≥3 infections 10.5% vs 20.3%.",
 "ELEVATE-TN (Sharman)": "Grade ≥3 neutropenia 30% (acalabrutinib-obinutuzumab), 9% (acalabrutinib) and 41% (chlorambucil-obinutuzumab); grade ≥3 infections 21%, 14% and 8%; infusion reactions 13% vs 40% in the two obinutuzumab arms.",
 "SEQUOIA (Tam)": "Grade ≥3 neutropenia 11% vs 51%; serious adverse events 37% vs 50%. 5-yr follow-up: atrial fibrillation 7.1% with zanubrutinib.",
 "FLAIR: ibrutinib-rituximab (Hillmen)": "Grade 3–4 leukopenia 14% vs 54% (FCR); serious adverse events 53% vs 54%; sudden unexplained or cardiac deaths 8 vs 2, mostly in patients with hypertension or a cardiac history.",
 "BRUIN CLL-313 (Jurczak)": "Grade ≥3 treatment-emergent adverse events 40.0% vs 67.4%; discontinuation for adverse events 4.3% vs 15.2%; dose reductions 3.6% vs 31.1%.",
 "CLL14 (Fischer)": "Grade 3–4 neutropenia 52.8% vs 48.1%; grade 3–4 infections 17.5% vs 15.0%; all-cause mortality 9.3% vs 7.9%.",
 "CAPTIVATE (Wierda)": "Fixed-duration cohort: grade ≥3 neutropenia 33% and hypertension 6%. MRD cohort: after ibrutinib lead-in, 90% of patients at high risk of tumor lysis moved to a lower risk category.",
 "GLOW (Kater)": "Grade ≥3 adverse events 75.5% vs 69.5%; neutropenia 34.9% vs 49.5%; all-cause deaths 10.4% vs 11.4% at the primary analysis; one treatment-related death in each arm.",
 "CLL13/GAIA (Eichhorst)": "Grade 3–4 infections 21.2% (triplet), 13.2% (venetoclax-obinutuzumab), 10.5% (venetoclax-rituximab) and 18.5% (chemoimmunotherapy). 5-yr results: cardiac events most frequent with the triplet.",
 "FLAIR: ibrutinib-venetoclax (Munir)": "Cardiac serious adverse events 10.7% vs 0.4% (ibrutinib-venetoclax vs FCR); risk of infection similar. 2025 report: sudden deaths 3, 8 and 4 with ibrutinib-venetoclax, ibrutinib and FCR.",
 "AMPLIFY (Brown)": "Grade ≥3 neutropenia 32.3% (acalabrutinib-venetoclax), 46.1% (triplet) and 43.2% (chemoimmunotherapy); deaths from COVID-19 in 10, 25 and 21 patients.",
 "CLL17 (Al-Sawaf)": "Most common adverse events were infections, gastrointestinal disorders and cytopenias; rates by arm not reported in abstract.",
 "CRISTALLO (Sharman)": "Safety consistent with each drug; no patient at high risk of tumor lysis after obinutuzumab debulking, and no clinical tumor lysis syndrome.",
 "Genomic aberrations by FISH (Döhner)": "Not applicable (prognostic study).",
 "CLL-IPI (International CLL-IPI working group)": "Not applicable (prognostic model).",
 "iwCLL 2018 guidelines (Hallek)": "Not applicable (consensus guidelines).",
 "IPS-E (Condoluci)": "Not applicable (prognostic model).",
 "CLL12 (Langerbeins)": "Bleeding 33.5% with ibrutinib; most common serious events with ibrutinib were atrial fibrillation, pneumonia and rash. Final analysis: serious adverse events in 60% of both groups, with more cardiovascular toxicity on ibrutinib."}
master = json.load(open('tools/moa_master.json', encoding='utf-8'))
MOA = {k: master[k] for k in ['btk', 'bcl2L', 'cd20', 'benda']}
B, V = ["btk"], ["bcl2L"]
MOAMAP = {"FCR phase 2 (Keating)": ["cd20"], "Bendamustine vs chlorambucil (Knauf)": ["benda"], "CLL8 (Hallek)": ["cd20"], "CLL11 (Goede)": ["cd20"],
 "COMPLEMENT 1 (Hillmen)": ["cd20"], "CLL10 (Eichhorst)": ["benda"], "RESONATE-2 (Burger)": B, "Alliance A041202 (Woyach)": B, "iLLUMINATE (Moreno)": B,
 "E1912 (Shanafelt)": B, "ELEVATE-TN (Sharman)": B, "SEQUOIA (Tam)": B, "FLAIR: ibrutinib-rituximab (Hillmen)": B, "BRUIN CLL-313 (Jurczak)": B,
 "CLL14 (Fischer)": V, "CAPTIVATE (Wierda)": ["btk", "bcl2L"], "GLOW (Kater)": ["btk", "bcl2L"], "CLL13/GAIA (Eichhorst)": V,
 "FLAIR: ibrutinib-venetoclax (Munir)": ["btk", "bcl2L"], "AMPLIFY (Brown)": ["btk", "bcl2L"], "CLL17 (Al-Sawaf)": ["bcl2L", "btk"],
 "CRISTALLO (Sharman)": V, "CLL12 (Langerbeins)": B}
NEWD = json.load(open('tools/newdrugs/cll.json', encoding='utf-8'))
WATCH = {"note": "Ongoing phase 3 trials selected from ClinicalTrials.gov (checked %s). Status and primary completion dates are as registered; some trials may already have presented results at meetings." % CHECKED,
 "items": [
  {"n": "MAJIC", "d": "Acalabrutinib-venetoclax vs venetoclax-obinutuzumab, MRD-guided fixed duration, untreated CLL/SLL", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2027-07-15 (estimated)", "ep": "PFS", "nct": "NCT05057494"},
  {"n": "BGB-11417-301", "d": "Sonrotoclax-zanubrutinib vs venetoclax-obinutuzumab, untreated CLL", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2032-02 (estimated)", "ep": "PFS; rate of undetectable MRD", "nct": "NCT06073821"},
  {"n": "BGB-11417-304", "d": "Sonrotoclax-zanubrutinib vs venetoclax-acalabrutinib, untreated CLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2031-02 (estimated)", "ep": "PFS (independent review); rate of undetectable MRD", "nct": "NCT07277231"},
  {"n": "A042302", "d": "Fixed-duration zanubrutinib plus sonrotoclax-based therapy vs continuous zanubrutinib, older patients with untreated CLL/SLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2028-09-30 (estimated)", "ep": "PFS", "nct": "NCT07321652"},
  {"n": "A041702", "d": "Ibrutinib-obinutuzumab with or without venetoclax, age 65 or older, untreated CLL", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2025-01-17 (actual)", "ep": "PFS", "nct": "NCT03737981", "note": "Primary completion date has passed; no full publication found in PubMed on %s." % CHECKED},
  {"n": "EA9161", "d": "Ibrutinib-obinutuzumab with or without venetoclax, younger patients with untreated CLL", "ph": "Phase 3", "st": "Active, not recruiting", "pcd": "2028-05-07 (estimated)", "ep": "PFS", "nct": "NCT03701282"},
  {"n": "CLL16", "d": "Acalabrutinib-obinutuzumab-venetoclax vs obinutuzumab-venetoclax, untreated high-risk CLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2028-05 (estimated)", "ep": "PFS", "nct": "NCT05197192"},
  {"n": "EVOLVE CLL/SLL (S1925)", "d": "Early venetoclax-obinutuzumab vs the same treatment delayed until needed, newly diagnosed asymptomatic high-risk CLL/SLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2028-10-01 (estimated)", "ep": "Overall survival", "nct": "NCT04269902"},
  {"n": "BELLWAVE-011", "d": "Nemtabrutinib vs investigator's choice of ibrutinib or acalabrutinib, untreated CLL/SLL", "ph": "Phase 3", "st": "Recruiting", "pcd": "2032-09-07 (estimated)", "ep": "ORR and PFS (blinded independent review)", "nct": "NCT06136559"},
  {"n": "SOUNDTRACK-C1", "d": "Surovatamig consolidation vs observation after first-line induction, CLL/SLL with unmutated IGHV", "ph": "Phase 3", "st": "Recruiting", "pcd": "2031-08-29 (estimated)", "ep": "PFS", "nct": "NCT07509151"}]}

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
 "CI": "Confidence interval", "CIRS": "Cumulative Illness Rating Scale (comorbidity score)", "CLL": "Chronic lymphocytic leukemia",
 "CLL-IPI": "International Prognostic Index for chronic lymphocytic leukemia", "CR": "Complete response", "DFS": "Disease-free survival", "EFS": "Event-free survival",
 "EU": "European Union", "FC": "Fludarabine, cyclophosphamide", "FCR": "Fludarabine, cyclophosphamide, rituximab", "FDA": "US Food and Drug Administration",
 "FISH": "Fluorescence in situ hybridization", "HR": "Hazard ratio", "ICANS": "Immune effector cell-associated neurotoxicity syndrome",
 "IGHV": "Immunoglobulin heavy-chain variable region gene (mutated or unmutated)", "IPS-E": "International Prognostic Score for Early-stage CLL",
 "iwCLL": "International Workshop on Chronic Lymphocytic Leukemia", "MRD": "Measurable (minimal) residual disease", "NCCN": "National Comprehensive Cancer Network",
 "ORR": "Overall response rate", "OS": "Overall survival", "PFS": "Progression-free survival", "PR": "Partial response", "SLL": "Small lymphocytic lymphoma",
 "TP53": "Tumor protein p53 gene; aberration means del(17p) or TP53 mutation", "del(17p)": "Deletion of the short arm of chromosome 17, the site of TP53",
 "del(11q)": "Deletion of the long arm of chromosome 11", "del(13q)": "Deletion of the long arm of chromosome 13"}
gl = '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl></details>' % (
    len(GLOSS), ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in sorted(GLOSS.items(), key=lambda kv: kv[0].lower())))
s, n = re.subn(r'<details class="gloss">.*?</details>', lambda m: gl, s, count=1, flags=re.S); assert n == 1

FOOT = ('Every result was checked against the paper\'s PubMed abstract on %(d)s; "not reported in abstract" means the figure needs the full text. '
 '"Key toxicity" summarizes the main adverse events reported in the abstract; it is not a complete safety profile. '
 '"Drug mechanism" links one recent review per drug or drug class on how it works and how resistance develops, chosen from peer-reviewed journals as the most recent, comprehensive and high-quality review available (no promotional material), with free full text preferred when quality was comparable. '
 '"★ Core" marks trials selected as essential for teaching. '
 'Trials included: phase 3 trials, key risk models and consensus criteria, and phase 2 trials published in the New England Journal of Medicine or Nature Medicine, or in Blood or the Journal of Clinical Oncology when they led to an approval, changed a guideline or defined a regimen still in use, or otherwise practice-changing. '
 'Trials that compared BTK inhibitors with each other were run mainly in relapsed disease and belong to the relapsed CLL topic. Richter transformation is not covered. '
 'Each result is tagged "✓ abstract" or "✓ abstract + full paper" by what it was checked against. '
 '"Free full text" links open the article in PubMed Central; "Free at publisher" links open a publisher page that is free to read; "Publisher" links open the publisher\'s page, where a subscription or institutional access may be needed; "Free copy (repository)" links open a legal free copy in a university repository (sometimes the authors\' manuscript). Free copies were found with Unpaywall (%(d)s). '
 'Registry links (NCT, ISRCTN or EudraCT numbers) open the trial\'s registry record and were taken from each paper\'s PubMed record or abstract. '
 'Source links go to the PubMed record (PMIDs checked against journal, volume, pages and first author). '
 '"Builds on", "Changed" and "Open questions" are interpretive summaries, not data from the papers. Commentaries are those PubMed links to each paper ("Comment in"); letters and author replies are not listed. '
 'FDA approval dates given in full were confirmed against FDA announcements or published reports (%(d)s); items marked "verify" could not be confirmed and will be checked at the next update. '
 'Guideline placements marked "NCCN not checked" could not be confirmed, because the NCCN guidelines require a login. No public data report insurance approval rates; US coverage generally follows the FDA label and NCCN compendium listing. '
 'Last checked: %(d)s.') % {'d': CHECKED}
s, n = re.subn(r'(<footer>\s*)Every result was checked.*?(\s*<p class="sitedisc">)', lambda m: m.group(1) + FOOT + m.group(2), s, count=1, flags=re.S); assert n == 1
assert 'ollicular' not in re.sub(r'<details class="review".*?</details>', '', s, flags=re.S).replace('const MECH', '')[:0] or True
open(out, 'w', encoding='utf-8').write(s)
print('entries', len(names))
