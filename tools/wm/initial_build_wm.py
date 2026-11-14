"""One-time build of the Waldenström macroglobulinemia page (key wm) from the relapsed FL page, November 14, 2026.
Usage (from the repository root): python3 tools/wm/initial_build_wm.py <out.html>
After this first build the page itself (source/wm.html) is the master copy: edit it directly, as for other topics
(tools/UPDATE_GUIDE.md). Then run, from tools/: mechs/install_mechtab.py, review/build_persp.py wm, review/install_persptint.py."""
import re, json, sys, urllib.parse
out = sys.argv[1]
s = open('source/flr.html', encoding='utf-8').read()
KEY, TITLE = 'wm', 'Waldenström macroglobulinemia'
CHECKED = 'November 14, 2026'

def sub1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

sub1('<title>Relapsed Follicular Lymphoma</title>', '<title>Waldenström macroglobulinemia</title>')
sub1('<div class="eyebrow">Relapsed/refractory follicular lymphoma · 2002–2026</div>', '<div class="eyebrow">Waldenström macroglobulinemia / lymphoplasmacytic lymphoma · 2003–2026</div>')
sub1('<h1>Landmark trials in relapsed and refractory follicular lymphoma</h1>', '<h1>Landmark studies in Waldenström macroglobulinemia and lymphoplasmacytic lymphoma</h1>')
s = re.sub(r'(<h1>Landmark studies in Waldenström macroglobulinemia and lymphoplasmacytic lymphoma</h1>\s*<p>).*?(</p>)',
           lambda m: m.group(1) + 'Untreated and relapsed disease together: the consensus definition, prognostic scores and the MYD88 and CXCR4 genotypes; rituximab and chemoimmunotherapy; proteasome inhibitor regimens; and BTK inhibitors, venetoclax and pirtobrutinib: design, verified results, context, open questions and reception.' + m.group(2), s, count=1, flags=re.S)
enc = urllib.parse.quote('Landmark trials (%s): comment' % TITLE, safe='')
old = 'Landmark%20trials%20%28Relapsed%20follicular%20lymphoma%29%3A%20comment'
assert s.count(old) == 2; s = s.replace(old, enc)
s = s.replace('"fl2-sort"', '"wm-sort"')
sub1('.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }',
     '.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }\n.tag.risk { color: var(--muted); background: var(--bg); box-shadow: inset 0 0 0 1px var(--rule); }')

ent = open('tools/wm/wm_entries.js', encoding='utf-8').read()
i, j = s.index('const SETTINGS = {'), s.index('const REG = ')
s = s[:i] + ent.rstrip() + '\n' + s[j:]

REG = {"Ibrutinib, previously treated (Treon)": ["NCT01614821"], "iNNOVATE arm C (Dimopoulos)": ["NCT02165397"], "iNNOVATE (Dimopoulos)": ["NCT02165397"],
 "Ibrutinib, treatment-naive (Treon)": ["NCT02604511"], "ASPEN (Tam)": ["NCT03053440"], "ASPEN cohort 2, MYD88 wild-type (Dimopoulos)": ["NCT03053440"],
 "ACE-WM-001 (Owen)": ["NCT02180724"], "Venetoclax (Castillo)": ["NCT02677324"], "BRUIN, Waldenström cohort (Palomba)": ["NCT03740529"],
 "WM1 (Leblond)": ["NCT00566332", "NCT00608374"], "StiL NHL 1-2003 (Rummel)": ["NCT00991211"], "EMN BDR (Dimopoulos)": ["NCT00981708"],
 "CaRD (Treon)": ["NCT01470196"], "IDR (Castillo)": ["NCT02400437"], "ECWM-1 (Buske)": ["NCT01788020"]}
FT = {"Ibrutinib, previously treated (Treon)": ["doi", "10.1056/NEJMoa1501548", "free"],
 "iNNOVATE arm C (Dimopoulos)": ["doi", "10.1016/S1470-2045(16)30632-5"],
 "iNNOVATE (Dimopoulos)": ["doi", "10.1056/NEJMoa1802917", "free"],
 "Ibrutinib, treatment-naive (Treon)": ["doi", "10.1200/JCO.2018.78.6426"],
 "ASPEN (Tam)": ["pmc", "PMC7596850"],
 "ASPEN cohort 2, MYD88 wild-type (Dimopoulos)": ["pmc", "PMC7724905"],
 "ACE-WM-001 (Owen)": ["doi", "10.1016/S2352-3026(19)30210-8", "repo", "https://dspace.library.uu.nl/handle/1874/394022"],
 "Venetoclax (Castillo)": ["pmc", "PMC8683218"],
 "BRUIN, Waldenström cohort (Palomba)": ["doi", "10.1016/S2352-3026(26)00037-2"],
 "E3A98 (Gertz)": ["doi", "10.1080/10428190410001714043"],
 "DRC (Dimopoulos)": ["doi", "10.1200/JCO.2007.10.9926", "free"],
 "GLSG R-CHOP vs CHOP (Buske)": ["doi", "10.1038/leu.2008.261"],
 "EBMT autologous transplantation (Kyriakou)": ["doi", "10.1200/JCO.2009.24.4905"],
 "WM1 (Leblond)": ["doi", "10.1200/JCO.2012.44.7920"],
 "StiL NHL 1-2003 (Rummel)": ["doi", "10.1016/S0140-6736(12)61763-2"],
 "WMCTG 05-180, BDR (Treon)": ["pmc", "PMC2727288"],
 "EMN BDR (Dimopoulos)": ["doi", "10.1182/blood-2013-05-503862", "free"],
 "CaRD (Treon)": ["doi", "10.1182/blood-2014-03-566273", "free"],
 "IDR (Castillo)": ["doi", "10.1158/1078-0432.CCR-18-0152"],
 "HOVON124/ECWM-R2 (Kersten)": ["pmc", "PMC8683241"],
 "ECWM-1 (Buske)": ["doi", "10.1200/JCO.22.01805"],
 "Consensus definition, IWWM-2 (Owen)": ["doi", "10.1053/sonc.2003.50082"],
 "IPSSWM (Morel)": ["doi", "10.1182/blood-2008-08-174961", "free"],
 "MYD88 L265P (Treon)": ["doi", "10.1056/NEJMoa1200710", "free"],
 "Response criteria, IWWM-6 (Owen)": ["doi", "10.1111/bjh.12102", "repo", "https://www.openaccessrepository.it/record/151148"],
 "MYD88 and CXCR4 genotype (Treon)": ["doi", "10.1182/blood-2014-01-550905"],
 "BTK Cys481 resistance mutations (Xu)": ["pmc", "PMC7484977"],
 "Revised IPSSWM (Kastritis)": ["doi", "10.1038/s41375-019-0431-y"],
 "Asymptomatic WM risk model (Bustoros)": ["pmc", "PMC6544461"],
 "IWWM-11 treatment consensus (Buske)": ["doi", "10.1053/j.seminhematol.2023.03.005", "repo", "https://pure.amsterdamumc.nl/en/publications/0bfb65a6-81b0-45ba-8d17-19674d299180"]}
NA = "Not applicable (%s)."
TOX = {
 "Ibrutinib, previously treated (Treon)": "Grade ≥2 neutropenia 22% and thrombocytopenia 14%, more common in heavily pretreated patients; atrial fibrillation 5%. Final analysis: grade ≥3 neutropenia 15.9%, thrombocytopenia 11.1%; atrial arrhythmia 12.7%, with 7 of 8 patients continuing treatment.",
 "iNNOVATE arm C (Dimopoulos)": "Grade ≥3 neutropenia 13%, hypertension 10%; serious adverse events 32%, mostly infections; 2 patients stopped for adverse events. Final analysis: no major hemorrhage or atrial fibrillation.",
 "iNNOVATE (Dimopoulos)": "Grade ≥3 atrial fibrillation 12% vs 1% and hypertension 13% vs 4%; fewer grade ≥3 infusion reactions (1% vs 16%) and less IgM flare (8% vs 47%) with ibrutinib-rituximab; major hemorrhage 4% in each group.",
 "Ibrutinib, treatment-naive (Treon)": "Grade 2–3 hypertension 13% and atrial fibrillation 10%; no grade 4 events. Final report: atrial fibrillation 20%.",
 "ASPEN (Tam)": "Final analysis, zanubrutinib vs ibrutinib: atrial fibrillation or flutter 7.9% vs 23.5%, hypertension 14.9% vs 25.5%, diarrhea 22.8% vs 34.7%, pneumonia 5.0% vs 18.4%; neutropenia 34.7% vs 20.4%. Fewer discontinuations for adverse events with zanubrutinib.",
 "ASPEN cohort 2, MYD88 wild-type (Dimopoulos)": "Hypertension in 3 patients, atrial fibrillation in 1 and major hemorrhage in 2; 2 patients stopped for adverse events.",
 "ACE-WM-001 (Owen)": "Grade 3–4 neutropenia 16% and pneumonia 7%; grade 3–4 atrial fibrillation 1% and bleeding 3%; one treatment-related death (intracranial hematoma). At 5 years: cardiac events of clinical interest 20.8%; 17.9% stopped for adverse events.",
 "Venetoclax (Castillo)": "Grade ≥3 neutropenia 45%, including one febrile neutropenia; laboratory tumor lysis in one patient, without clinical consequences; no deaths.",
 "BRUIN, Waldenström cohort (Palomba)": "Grade ≥3 adverse events 71%, most often anemia (24%) and neutropenia (19%); 15% stopped for adverse events; one treatment-related death (necrotising pneumonia).",
 "E3A98 (Gertz)": "Grade 4 toxicity in 11%. IgM flare in the companion series: IgM rose by more than 25% in 8 of 11 patients, with one subdural hemorrhage and worsening hyperviscosity symptoms in two others.",
 "DRC (Dimopoulos)": "Grade 3–4 neutropenia 9%; about 20% had toxicity related to rituximab.",
 "GLSG R-CHOP vs CHOP (Buske)": "No major difference between the arms; rates not reported in abstract.",
 "EBMT autologous transplantation (Kyriakou)": "Non-relapse mortality 3.8% at 1 year; second malignancies in 10 patients (8.4% at 5 years).",
 "WM1 (Leblond)": "Grade 3–4 neutropenia 36% (fludarabine) vs 17.8% (chlorambucil); second malignancies at 6 years 3.7% vs 20.6%.",
 "StiL NHL 1-2003 (Rummel)": "All histologies, bendamustine-rituximab vs R-CHOP: hematologic toxicity 30% vs 68%, infections 37% vs 50%, peripheral neuropathy 7% vs 29%, alopecia 0% vs 100%; erythematous skin reactions 16% vs 9%.",
 "WMCTG 05-180, BDR (Treon)": "Peripheral neuropathy was the most common toxicity (16 patients; resolved to grade ≤1 in 13) and led 61% to stop bortezomib early; herpes zoster in 4 of the first 7 patients, before antiviral prophylaxis.",
 "EMN BDR (Dimopoulos)": "Peripheral neuropathy 46% (grade ≥3, 7%); 8% stopped bortezomib for neuropathy. Final analysis: no secondary myelodysplasia.",
 "CaRD (Treon)": "Grade ≥2: asymptomatic hyperlipasemia 41.9%, neutropenia 12.9%, cardiomyopathy in one patient, peripheral neuropathy in one patient (grade 2); falls in IgA and IgG were common.",
 "IDR (Castillo)": "Grade ≥2 infusion-related reactions 19%, rash 8%, insomnia 8%; no grade 4 events or deaths in long-term follow-up.",
 "HOVON124/ECWM-R2 (Kersten)": "Mostly grade 2–3 cytopenias, grade 1–2 neurotoxicity and grade 2–3 infections; rates not reported in abstract.",
 "ECWM-1 (Buske)": "Grade ≥3 adverse events 49.5% (B-DRC) vs 49.0% (DRC); grade 3 peripheral sensory neuropathy in 2 patients with B-DRC and none with DRC.",
 "Consensus definition, IWWM-2 (Owen)": NA % "consensus statement",
 "IPSSWM (Morel)": NA % "prognostic model",
 "MYD88 L265P (Treon)": NA % "laboratory study",
 "Response criteria, IWWM-6 (Owen)": NA % "consensus statement",
 "MYD88 and CXCR4 genotype (Treon)": NA % "cohort study of genotype",
 "BTK Cys481 resistance mutations (Xu)": NA % "laboratory study",
 "Revised IPSSWM (Kastritis)": NA % "prognostic model",
 "Asymptomatic WM risk model (Bustoros)": NA % "prognostic model",
 "IWWM-11 treatment consensus (Buske)": NA % "consensus statement"}
master = json.load(open('tools/moa_master.json', encoding='utf-8'))
MOA = {k: master[k] for k in ['btk', 'bcl2L', 'cd20', 'benda', 'pi']}
B, P, C = ["btk"], ["pi"], ["cd20"]
MOAMAP = {"Ibrutinib, previously treated (Treon)": B, "iNNOVATE arm C (Dimopoulos)": B, "iNNOVATE (Dimopoulos)": B, "Ibrutinib, treatment-naive (Treon)": B,
 "ASPEN (Tam)": B, "ASPEN cohort 2, MYD88 wild-type (Dimopoulos)": B, "ACE-WM-001 (Owen)": B, "Venetoclax (Castillo)": ["bcl2L"], "BRUIN, Waldenström cohort (Palomba)": B,
 "E3A98 (Gertz)": C, "DRC (Dimopoulos)": C, "GLSG R-CHOP vs CHOP (Buske)": C, "StiL NHL 1-2003 (Rummel)": ["benda"],
 "WMCTG 05-180, BDR (Treon)": P, "EMN BDR (Dimopoulos)": P, "CaRD (Treon)": P, "IDR (Castillo)": P, "HOVON124/ECWM-R2 (Kersten)": P, "ECWM-1 (Buske)": P}
NEWD = json.load(open('tools/newdrugs/wm.json', encoding='utf-8'))
WATCH = {"note": "Only two phase 3 trials are registered for this disease, so the list also holds randomized and single-arm phase 2 trials of regimens that could change practice. Selected from ClinicalTrials.gov (checked %s). Status and primary completion dates are as registered; some trials may already have presented results at meetings." % CHECKED,
 "items": [
  {"n": "RAINBOW", "d": "Rituximab-ibrutinib vs dexamethasone, rituximab and cyclophosphamide (DRC) as first treatment", "ph": "Phase 2/3", "st": "Recruiting", "pcd": "2030-03 (estimated)", "ep": "Response to rituximab-ibrutinib (phase 2); PFS (phase 3)", "nct": "NCT04061512"},
  {"n": "DCL-26-001", "d": "Iopofosine I 131 vs rituximab, cyclophosphamide and dexamethasone in patients previously treated with a BTK inhibitor", "ph": "Phase 3", "st": "Not yet recruiting", "pcd": "2032-01 (estimated)", "ep": "PFS", "nct": "NCT07766421"},
  {"n": "S2005", "d": "Venetoclax-rituximab vs a BTK inhibitor (ibrutinib-rituximab or zanubrutinib) as first treatment of Waldenström macroglobulinemia or lymphoplasmacytic lymphoma", "ph": "Phase 2 (randomized)", "st": "Recruiting", "pcd": "2028-03-31 (estimated)", "ep": "Very good partial response or better", "nct": "NCT04840602"},
  {"n": "VIWA-1", "d": "Venetoclax-rituximab vs dexamethasone, rituximab and cyclophosphamide (DRC)", "ph": "Phase 2 (randomized)", "st": "Recruiting", "pcd": "2028-03 (estimated)", "ep": "Complete or very good partial response", "nct": "NCT05099471"},
  {"n": "CZAR-1", "d": "Carfilzomib with ibrutinib vs ibrutinib alone", "ph": "Phase 2 (randomized)", "st": "Active, not recruiting", "pcd": "2028-05 (estimated)", "ep": "Complete or very good partial response", "nct": "NCT04263480"},
  {"n": "BGB-11417-203", "d": "Sonrotoclax alone in relapsed or refractory disease (three cohorts) and with zanubrutinib, fixed duration, in untreated disease", "ph": "Phase 2 (registrational)", "st": "Active, not recruiting", "pcd": "2026-09-22", "ep": "Major response rate (cohort 1)", "nct": "NCT05952037"},
  {"n": "WAZABI", "d": "Zanubrutinib with sonrotoclax (BGB-11417) in previously treated patients; single arm", "ph": "Phase 2", "st": "Not yet recruiting", "pcd": "2028-12-31 (estimated)", "ep": "Not specified in the registry record", "nct": "NCT06547866"},
  {"n": "ZEBRA", "d": "Zanubrutinib, bendamustine and rituximab as first treatment; single arm", "ph": "Phase 2", "st": "Recruiting", "pcd": "2026-12-01 (estimated)", "ep": "Very good partial response or better", "nct": "NCT06561347"},
  {"n": "BRAWM", "d": "Bendamustine, rituximab and acalabrutinib as first treatment; single arm", "ph": "Phase 2", "st": "Active, not recruiting", "pcd": "2025-12-31", "ep": "Best complete or very good partial response", "nct": "NCT04624906"}]}

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
 "AE": "Adverse event", "AL amyloidosis": "Immunoglobulin light-chain amyloidosis", "B-DRC": "Bortezomib, dexamethasone, rituximab, cyclophosphamide",
 "BCL2": "B-cell lymphoma 2 protein (target of venetoclax)", "BDR": "Bortezomib, dexamethasone, rituximab", "BTK": "Bruton tyrosine kinase",
 "CAR": "Chimeric antigen receptor", "CaRD": "Carfilzomib, rituximab, dexamethasone", "CHOP": "Cyclophosphamide, doxorubicin, vincristine, prednisone",
 "CI": "Confidence interval", "CLL": "Chronic lymphocytic leukemia", "CR": "Complete response", "CXCR4": "C-X-C chemokine receptor 4 gene; WHIM-like mutations are nonsense or frameshift mutations of its C-terminal tail",
 "DRC": "Dexamethasone, rituximab, cyclophosphamide", "EBMT": "European Society for Blood and Marrow Transplantation", "ECWM": "European Consortium for Waldenström's Macroglobulinemia",
 "EMA": "European Medicines Agency", "EMN": "European Myeloma Network", "EU": "European Union", "FDA": "US Food and Drug Administration",
 "GLSG": "German Low-Grade Lymphoma Study Group", "HR": "Hazard ratio", "IDR": "Ixazomib, dexamethasone, rituximab", "IgM": "Immunoglobulin M",
 "IPSSWM": "International Prognostic Scoring System for Waldenström Macroglobulinemia", "IWWM": "International Workshop on Waldenström's Macroglobulinemia",
 "LDH": "Lactate dehydrogenase", "MGUS": "Monoclonal gammopathy of undetermined significance", "MYD88": "Myeloid differentiation primary response 88 gene; L265P is its recurrent activating mutation",
 "NCCN": "National Comprehensive Cancer Network", "ORR": "Overall response rate (minor response or better in this disease)", "OS": "Overall survival", "PCR": "Polymerase chain reaction",
 "PFS": "Progression-free survival", "PLCG2": "Phospholipase C gamma 2 gene, downstream of BTK", "R-CHOP": "Rituximab with CHOP",
 "StiL": "Study group indolent Lymphomas (Germany)", "VGPR": "Very good partial response", "WHIM": "Warts, hypogammaglobulinemia, infections and myelokathexis syndrome (germline CXCR4 mutations)",
 "WM": "Waldenström macroglobulinemia", "WMCTG": "Waldenström's Macroglobulinemia Clinical Trials Group", "Major response": "Partial response or better",
 "Minor response": "A fall in serum IgM of at least 25% but less than 50%"}
gl = '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl></details>' % (
    len(GLOSS), ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in sorted(GLOSS.items(), key=lambda kv: kv[0].lower())))
s, n = re.subn(r'<details class="gloss">.*?</details>', lambda m: gl, s, count=1, flags=re.S); assert n == 1

FOOT = ('Every result was checked against the paper\'s PubMed abstract on %(d)s; "not reported in abstract" means the figure needs the full text. '
 '"Key toxicity" summarizes the main adverse events reported in the abstract; it is not a complete safety profile. '
 '"Drug mechanism" links one recent review per drug or drug class on how it works and how resistance develops, chosen from peer-reviewed journals as the most recent, comprehensive and high-quality review available (no promotional material), with free full text preferred when quality was comparable. '
 '"★ Core" marks studies selected as essential for teaching. '
 'Studies included: untreated and relapsed disease are one topic, because most trials in this disease enrolled both. Only a few randomized trials exist, so the list holds every phase 3 or randomized trial with a full report, the phase 2 trials that were the basis of an approval or that defined a regimen in current use (whatever the journal), and the consensus definition, response criteria, prognostic models and genomic studies on which trials and practice rest. '
 'Ibrutinib-venetoclax, tirabrutinib, orelabrutinib, everolimus, Bing-Neel syndrome and histological transformation are not listed as cards. IgM MGUS and IgM-related disorders (neuropathy, cold agglutinin disease, cryoglobulinemia, amyloidosis) are not covered. '
 'Each result is tagged "✓ abstract" or "✓ abstract + full paper" by what it was checked against. '
 '"Free full text" links open the article in PubMed Central; "Free at publisher" links open a publisher page that is free to read; "Publisher" links open the publisher\'s page, where a subscription or institutional access may be needed; "Free copy (repository)" links open a legal free copy in a university repository (sometimes the authors\' manuscript). Free copies were found with Unpaywall (%(d)s). '
 'Registry links (NCT numbers) open the trial\'s registry record and were taken from each paper\'s PubMed record or abstract. '
 'Source links go to the PubMed record (PMIDs checked against journal, volume, pages and first author). '
 '"Builds on", "Changed" and "Open questions" are interpretive summaries, not data from the papers. Commentaries are those PubMed links to each paper ("Comment in"); letters and author replies are not listed. '
 'FDA approval dates given in full were confirmed against FDA announcements or published reports, and the EU date for zanubrutinib against the EMA record (%(d)s); items marked "verify" could not be confirmed and will be checked at the next update. '
 'Guideline rows cite the International Workshop consensus reports; placements marked "NCCN not checked" could not be confirmed, because the NCCN guidelines require a login. No public data report insurance approval rates; US coverage generally follows the FDA label and NCCN compendium listing. '
 'Last checked: %(d)s.') % {'d': CHECKED}
s, n = re.subn(r'(<footer>\s*)Every result was checked.*?(\s*<p class="sitedisc">)', lambda m: m.group(1) + FOOT + m.group(2), s, count=1, flags=re.S); assert n == 1
open(out, 'w', encoding='utf-8').write(s)
print('entries', len(names))
