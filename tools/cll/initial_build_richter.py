"""One-time build of the Richter transformation page (key richter) from the relapsed FL page, November 12, 2026.
Usage (from the repository root): python3 tools/cll/initial_build_richter.py <out.html>
After this first build the page itself (source/richter.html) is the master copy: edit it directly, as for other topics
(tools/UPDATE_GUIDE.md). Then run, from tools/: mechs/install_mechtab.py, review/build_persp.py richter, review/install_persptint.py."""
import re, json, sys, urllib.parse
out = sys.argv[1]
s = open('source/flr.html', encoding='utf-8').read()
KEY, TITLE = 'richter', 'Richter transformation'
CHECKED = 'November 12, 2026'

def sub1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

sub1('<title>Relapsed Follicular Lymphoma</title>', '<title>Richter transformation</title>')
sub1('<div class="eyebrow">Relapsed/refractory follicular lymphoma · 2002–2026</div>', '<div class="eyebrow">Richter transformation of CLL · first-line and relapsed · 2003–2026</div>')
sub1('<h1>Landmark trials in relapsed and refractory follicular lymphoma</h1>', '<h1>Landmark studies in Richter transformation</h1>')
s = re.sub(r'(<h1>Landmark studies in Richter transformation</h1>\s*<p>).*?(</p>)',
           lambda m: m.group(1) + 'Initial treatment and relapse in one topic, because no treatment is established at either point: risk, biology and diagnosis, chemoimmunotherapy and transplantation, BTK, BCL2 and checkpoint inhibitors, bispecific antibodies and CAR T cells, and the Hodgkin variant. There are no randomized trials yet; most entries are phase 2 trials and retrospective series, each with its design, verified results, context, open questions and reception.' + m.group(2), s, count=1, flags=re.S)
enc = urllib.parse.quote('Landmark trials (%s): comment' % TITLE, safe='')
old = 'Landmark%20trials%20%28Relapsed%20follicular%20lymphoma%29%3A%20comment'
assert s.count(old) == 2; s = s.replace(old, enc)
s = s.replace('"fl2-sort"', '"richter-sort"')
sub1('.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }',
     '.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }\n.tag.risk { color: var(--muted); background: var(--bg); box-shadow: inset 0 0 0 1px var(--rule); }')

ent = open('tools/cll/richter_entries.js', encoding='utf-8').read()
i, j = s.index('const SETTINGS = {'), s.index('const REG = ')
s = s[:i] + ent.rstrip() + '\n' + s[j:]

REG = {"PET after BCR pathway inhibitors (Mato)": ["NCT02141282"], "R-CHOP, GCLLSG phase 2 (Langerbeins)": ["NCT00309881"], "VR-EPOCH (Davids)": ["NCT03054896"],
 "Pembrolizumab, Mayo Clinic phase 2 (Ding)": ["NCT02332980"], "Ibrutinib-nivolumab, phase 1/2a (Younes)": ["NCT02329847"], "KEYNOTE-170, Richter cohort (Armand)": ["NCT02576990"],
 "ACE-CL-001, Richter cohort (Eyre)": ["NCT02029443"], "Nivolumab-ibrutinib, MD Anderson phase 2 (Jain)": ["NCT02420912"], "Zanubrutinib, alone or with tislelizumab (Tam)": ["NCT02343120", "NCT02795182"],
 "RT1 (Al-Sawaf)": ["NCT04271956"], "MOLTO (Tedeschi)": ["NCT04082897"], "BRUIN, Richter cohort (Wierda)": ["NCT03740529"], "High-dose blinatumomab (Thompson)": ["NCT03121534"],
 "BLINART (Guièze)": ["NCT03931642"], "EPCORE CLL-1, Richter cohort (Kater)": ["NCT04623541"], "Mosunetuzumab, phase 1/2 cohort (Lewis)": ["NCT02500407"], "Glofitamab, NP30179 Richter cohort (Carlo-Stella)": ["NCT03075696"]}
ftj = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else None
FT = {"Richter score, MD Anderson (Tsimberidou)": ["doi", "10.1200/JCO.2005.05.0187"],
 "Genetics and clonal relationship (Rossi)": ["doi", "10.1182/blood-2010-09-302174", "repo", "http://hdl.handle.net/11380/649123"],
 "Mayo Clinic newly diagnosed cohort (Parikh)": ["pmc", "PMC4098845"],
 "Genetic lesions of transformation (Fabbri)": ["pmc", "PMC3804949"],
 "Two genetic pathways (Chigrinova)": ["doi", "10.1182/blood-2013-03-489518", "repo", "http://hdl.handle.net/11380/1064004"],
 "FDG-PET and histology (Falchi)": ["pmc", "PMC4123418"],
 "PET after BCR pathway inhibitors (Mato)": ["pmc", "PMC6821597"],
 "Mayo Clinic series of 204 patients (Wang)": ["pmc", "PMC7049354"],
 "GELLC real-world series (Abrisqueta)": ["doi", "10.1111/bjh.16748"],
 "GCLLSG pooled analysis (Al-Sawaf)": ["doi", "10.1038/s41375-020-0797-x"],
 "Early seeding of transformation (Nadeu)": ["pmc", "PMC9388377"],
 "Evolutionary history of transformation (Parry)": ["pmc", "PMC10155825"],
 "ERIC consensus recommendations (Kittai)": ["doi", "10.1182/blood.2024028064"],
 "Transformation without prior chemoimmunotherapy (Kittai)": ["pmc", "PMC11842760"],
 "EHA guidelines 2026 (Eichhorst)": ["pmc", "PMC13254007"],
 "Hyper-CVXD with rituximab (Tsimberidou)": ["doi", "10.1002/cncr.11238", "free"],
 "OFAR (Tsimberidou)": ["doi", "10.1200/JCO.2007.11.8513"],
 "EBMT transplant registry (Cwynarski)": ["doi", "10.1200/JCO.2011.37.4108"],
 "R-CHOP, GCLLSG phase 2 (Langerbeins)": ["doi", "10.1002/ajh.23841", "free"],
 "CHOP-O, NCRI phase 2 (Eyre)": ["doi", "10.1111/bjh.14177", "repo", "https://ora.ox.ac.uk/objects/uuid:34244807-a3dc-4aaf-8b76-8eec509388e7/files/m9f241a878f80c5a69ece37c9190eec84"],
 "R-EPOCH, Ohio State (Rogers)": ["doi", "10.1111/bjh.15035"],
 "CIBMTR transplant registry (Herrera)": ["pmc", "PMC8945575"],
 "VR-EPOCH (Davids)": ["pmc", "PMC8814674"],
 "EBMT allogeneic transplant series (Guièze)": ["doi", "10.1038/s41409-024-02256-9", "repo", "https://cris.maastrichtuniversity.nl/en/publications/3a4190c7-d32a-4a91-83e2-9cca8ce68d70"],
 "Pembrolizumab, Mayo Clinic phase 2 (Ding)": ["pmc", "PMC5492091"],
 "Ibrutinib-nivolumab, phase 1/2a (Younes)": ["doi", "10.1016/S2352-3026(18)30217-5", "repo", "https://ruj.uj.edu.pl/xmlui/handle/item/108096"],
 "KEYNOTE-170, Richter cohort (Armand)": ["pmc", "PMC7496875"],
 "ACE-CL-001, Richter cohort (Eyre)": ["pmc", "PMC11729767"],
 "Nivolumab-ibrutinib, MD Anderson phase 2 (Jain)": ["pmc", "PMC10189379"],
 "Zanubrutinib, alone or with tislelizumab (Tam)": ["pmc", "PMC10043571"],
 "RT1 (Al-Sawaf)": ["pmc", "PMC10803258"],
 "MOLTO (Tedeschi)": ["doi", "10.1016/S1470-2045(24)00396-6", "repo", "https://hdl.handle.net/20.500.11768/172816"],
 "Venetoclax-based treatment, multicenter series (Hampel)": ["pmc", "PMC11127193"],
 "BRUIN, Richter cohort (Wierda)": ["doi", "10.1016/S2352-3026(24)00172-8"],
 "High-dose blinatumomab (Thompson)": ["pmc", "PMC9467861"],
 "BLINART (Guièze)": ["pmc", "PMC11316063"],
 "CAR T cells, international series (Kittai)": ["doi", "10.1200/JCO.24.00033"],
 "EPCORE CLL-1, Richter cohort (Kater)": ["doi", "10.1016/S2352-3026(25)00327-8", "repo", "https://biblio.ugent.be/publication/01KWYAFHPG895SAGKVHXZC9F4X"],
 "Mosunetuzumab, phase 1/2 cohort (Lewis)": ["pmc", "PMC13141522"],
 "Glofitamab, NP30179 Richter cohort (Carlo-Stella)": ["pmc", "PMC13285835"],
 "Hodgkin transformation, Mayo Clinic (Parikh)": ["pmc", "PMC4438308"],
 "Hodgkin transformation, multicenter series (Stephens)": ["pmc", "PMC8561295"],
 "Hodgkin variant, British Columbia (Zhu)": ["doi", "10.1111/bjh.18241", "free"]}
NA = "Not applicable (%s)."
TOX = {
 "Richter score, MD Anderson (Tsimberidou)": "Not reported in abstract.",
 "Genetics and clonal relationship (Rossi)": NA % "molecular study",
 "Mayo Clinic newly diagnosed cohort (Parikh)": NA % "cohort study of incidence and risk",
 "Genetic lesions of transformation (Fabbri)": NA % "genomic study",
 "Two genetic pathways (Chigrinova)": NA % "genomic study",
 "FDG-PET and histology (Falchi)": NA % "imaging study",
 "PET after BCR pathway inhibitors (Mato)": NA % "imaging study",
 "Mayo Clinic series of 204 patients (Wang)": "Not reported in abstract.",
 "GELLC real-world series (Abrisqueta)": "Not reported in abstract.",
 "GCLLSG pooled analysis (Al-Sawaf)": "Not reported in abstract.",
 "Early seeding of transformation (Nadeu)": NA % "genomic study",
 "Evolutionary history of transformation (Parry)": NA % "genomic study",
 "ERIC consensus recommendations (Kittai)": NA % "consensus statement",
 "Transformation without prior chemoimmunotherapy (Kittai)": "Not reported.",
 "EHA guidelines 2026 (Eichhorst)": NA % "guideline",
 "Hyper-CVXD with rituximab (Tsimberidou)": "18% of patients died during the first cycle and 4% during the second.",
 "OFAR (Tsimberidou)": "Mainly hematologic; no dose-limiting toxicity and no prolonged myelosuppression.",
 "EBMT transplant registry (Cwynarski)": "3-year nonrelapse mortality 26% after allogeneic and 12% after autologous transplantation.",
 "R-CHOP, GCLLSG phase 2 (Langerbeins)": "All 60 patients: hematologic toxicity in 92%, severe infections in 28%; treatment stopped early in 45%, mainly for toxicity.",
 "CHOP-O, NCRI phase 2 (Eyre)": "15 episodes of neutropenic fever and 46 non-neutropenic infections; no treatment-related deaths.",
 "R-EPOCH, Ohio State (Rogers)": "Toxicity was high: 30% of patients died without progression or response.",
 "CIBMTR transplant registry (Herrera)": "Not reported in abstract.",
 "VR-EPOCH (Davids)": "Grade ≥3 neutropenia 65% and thrombocytopenia 50%; febrile neutropenia 38%. No tumor lysis syndrome with the daily venetoclax ramp-up.",
 "EBMT allogeneic transplant series (Guièze)": "Nonrelapse mortality 38% at 3 years; grade II–IV acute graft-versus-host disease 41% at day 100; chronic graft-versus-host disease 53% at 3 years.",
 "Pembrolizumab, Mayo Clinic phase 2 (Ding)": "Treatment-related grade ≥3 adverse events in 60% of all 25 patients, described as manageable.",
 "Ibrutinib-nivolumab, phase 1/2a (Younes)": "All 141 patients: grade 3–4 neutropenia 28% and anemia 23% (anemia in 7 of 20 with Richter transformation); grade 3–4 immune-related rash 8%. No deaths reported as drug-related.",
 "KEYNOTE-170, Richter cohort (Armand)": "Treatment-related adverse events in 57%; immune-mediated events in 22%; 13% stopped for treatment-related events (autoimmune hemolytic anemia, pneumonitis, rash); no treatment-related deaths (full paper).",
 "ACE-CL-001, Richter cohort (Eyre)": "Diarrhea 48%, headache 44%, anemia 32% (all grades); grade 3–4 neutropenia 28% and anemia 20%. No treatment-related deaths.",
 "Nivolumab-ibrutinib, MD Anderson phase 2 (Jain)": "Immune-related toxicity from checkpoint inhibition in 4 of 24 patients (17%).",
 "Zanubrutinib, alone or with tislelizumab (Tam)": "Zanubrutinib alone: grade 3 adverse events in 69.2%, infections in 69.2% (none opportunistic), no atrial fibrillation; two deaths from adverse events (myocardial infarction, bacteremia) (full paper).",
 "RT1 (Al-Sawaf)": "Most common adverse events: infections (18.0%), gastrointestinal disorders (13.0%) and hematological toxicities (11.4%). No atrial fibrillation was reported (full paper).",
 "MOLTO (Tedeschi)": "Grade ≥3 adverse events 61%, most often neutropenia (39%); serious infections 18%; immune-related adverse events 21.4%, none leading to discontinuation; no tumor lysis syndrome; 2 deaths from infection, not considered directly treatment-related.",
 "Venetoclax-based treatment, multicenter series (Hampel)": "Grade 3–4 neutropenia and thrombocytopenia were most frequent with intensive chemoimmunotherapy plus venetoclax; grade 3–4 infection rates were similar across groups.",
 "BRUIN, Richter cohort (Wierda)": "Most common grade ≥3 adverse event: neutropenia (19 of 82 patients). No treatment-related deaths.",
 "High-dose blinatumomab (Thompson)": "No cytokine release syndrome above grade 3; one case of reversible grade 3 neurotoxicity.",
 "BLINART (Guièze)": "With blinatumomab: fever 36%, anemia 24%, lymphopenia 24%; cytokine release syndrome 16% (grade 1–2); neurotoxicity 20%.",
 "CAR T cells, international series (Kittai)": "Grade ≥3 cytokine release syndrome 16%; grade ≥3 neurotoxicity (ICANS) 37%.",
 "EPCORE CLL-1, Richter cohort (Kater)": "Cytokine release syndrome 86% (grade 3 in 7%); ICANS 12% (all grade 1–2); grade 3–4 neutropenia 45%, anemia 38%, thrombocytopenia 38%, infection 21%; clinical tumor lysis syndrome 5%; no treatment-related deaths.",
 "Mosunetuzumab, phase 1/2 cohort (Lewis)": "Cytokine release syndrome 65%, almost all grade 1 (20%) or grade 2 (40%), in the first cycle; no adverse event led to discontinuation.",
 "Glofitamab, NP30179 Richter cohort (Carlo-Stella)": "Cytokine release syndrome 72.7% (grade 3 in 9.1% and grade 4 in 9.1%); grade 3–4 neutropenia 27.3%; no adverse event led to discontinuation and none was fatal (full paper).",
 "Hodgkin transformation, Mayo Clinic (Parikh)": NA % "cohort study of incidence and survival",
 "Hodgkin transformation, multicenter series (Stephens)": "Not reported in abstract.",
 "Hodgkin variant, British Columbia (Zhu)": "Not reported in abstract."}
master = json.load(open('tools/moa_master.json', encoding='utf-8'))
MOA = {k: master[k] for k in ['btk', 'bcl2L', 'pd1', 'cd20', 'cd19tce', 'cd20tce', 'cd19car']}
MOAMAP = {"CHOP-O, NCRI phase 2 (Eyre)": ["cd20"], "VR-EPOCH (Davids)": ["bcl2L"],
 "Pembrolizumab, Mayo Clinic phase 2 (Ding)": ["pd1"], "KEYNOTE-170, Richter cohort (Armand)": ["pd1"],
 "Ibrutinib-nivolumab, phase 1/2a (Younes)": ["btk", "pd1"], "Nivolumab-ibrutinib, MD Anderson phase 2 (Jain)": ["btk", "pd1"],
 "ACE-CL-001, Richter cohort (Eyre)": ["btk"], "Zanubrutinib, alone or with tislelizumab (Tam)": ["btk", "pd1"], "RT1 (Al-Sawaf)": ["btk", "pd1"],
 "MOLTO (Tedeschi)": ["pd1", "bcl2L"], "Venetoclax-based treatment, multicenter series (Hampel)": ["bcl2L"], "BRUIN, Richter cohort (Wierda)": ["btk"],
 "High-dose blinatumomab (Thompson)": ["cd19tce"], "BLINART (Guièze)": ["cd19tce"], "CAR T cells, international series (Kittai)": ["cd19car"],
 "EPCORE CLL-1, Richter cohort (Kater)": ["cd20tce"], "Mosunetuzumab, phase 1/2 cohort (Lewis)": ["cd20tce"], "Glofitamab, NP30179 Richter cohort (Carlo-Stella)": ["cd20tce"]}
NEWD = json.load(open('tools/newdrugs/richter.json', encoding='utf-8'))
WATCH = {"note": "Ongoing trials selected from ClinicalTrials.gov (checked %s). Only one phase 3 trial is registered for Richter transformation, so this list also includes randomized and single-arm phase 2 trials of regimens that could change practice. Status and primary completion dates are as registered; some trials may already have presented results at meetings." % CHECKED,
 "items": [
  {"n": "PIRAMID (S2504)", "d": "Pirtobrutinib plus R-CHOP vs R-CHOP, previously untreated Richter transformation", "ph": "Phase 3", "st": "Recruiting", "pcd": "2035-10-01 (estimated)", "ep": "PFS", "nct": "NCT07220187"},
  {"n": "CLLRT2", "d": "Pirtobrutinib plus epcoritamab vs R-CHOP or R-mini-CHOP, Richter transformation of diffuse large B-cell type (randomized; registered as phase 2, described as phase 3 in its title)", "ph": "Phase 2 (randomized)", "st": "Recruiting", "pcd": "2030-05-15 (estimated)", "ep": "PFS", "nct": "NCT07917780"},
  {"n": "STELLAR", "d": "CHOP-R with or without acalabrutinib, newly diagnosed Richter syndrome (randomized), with platform cohorts of acalabrutinib alone or with CHOP-R", "ph": "Phase 2 (randomized)", "st": "Active, not recruiting", "pcd": "2028-06-30 (estimated)", "ep": "PFS (randomized part)", "nct": "NCT03899337"},
  {"n": "CLL-RT1", "d": "Zanubrutinib plus tislelizumab, with or without sonrotoclax, Richter transformation (the cohort without sonrotoclax is on the landmark list as RT1)", "ph": "Phase 2", "st": "Recruiting", "pcd": "2027-08 (estimated)", "ep": "ORR after induction", "nct": "NCT04271956"},
  {"n": "GLORIFY", "d": "Glofitamab with rituximab or obinutuzumab plus CHOP, first-line Richter syndrome", "ph": "Phase 2", "st": "Recruiting", "pcd": "2028-03-01 (estimated)", "ep": "Objective response", "nct": "NCT06186648"},
  {"n": "GELLC9RICHTER", "d": "Mosunetuzumab plus CHOP for 6 cycles, then mosunetuzumab alone, first-line Richter syndrome", "ph": "Phase 2", "st": "Recruiting", "pcd": "2028-05-15 (estimated)", "ep": "Efficacy at the end of induction", "nct": "NCT06926205"},
  {"n": "16-596 (venetoclax with R-CHOP)", "d": "Venetoclax plus dose-adjusted R-EPOCH (cohort 1, on the landmark list as VR-EPOCH) or plus R-CHOP (cohort 2), Richter syndrome", "ph": "Phase 2", "st": "Active, not recruiting", "pcd": "2025-12-24", "ep": "Complete response rate", "nct": "NCT03054896"},
  {"n": "MC198B", "d": "Acalabrutinib, venetoclax and durvalumab, Richter transformation", "ph": "Phase 2", "st": "Active, not recruiting", "pcd": "2026-09-23", "ep": "PFS", "nct": "NCT05388006"},
  {"n": "I-3586924", "d": "Nemtabrutinib plus pembrolizumab, Richter transformation of diffuse large B-cell type", "ph": "Phase 2", "st": "Recruiting", "pcd": "2029-06-01 (estimated)", "ep": "ORR", "nct": "NCT06863402"}]}

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
 "ABVD": "Doxorubicin, bleomycin, vinblastine, dacarbazine", "BCL2": "B-cell lymphoma 2 protein (target of venetoclax)", "BCR": "B-cell receptor",
 "BTK": "Bruton tyrosine kinase", "CAR": "Chimeric antigen receptor", "CHOP": "Cyclophosphamide, doxorubicin, vincristine, prednisone",
 "CHOP-O": "CHOP with ofatumumab", "CI": "Confidence interval", "CIBMTR": "Center for International Blood and Marrow Transplant Research",
 "CLL": "Chronic lymphocytic leukemia", "CR": "Complete response", "DLBCL": "Diffuse large B-cell lymphoma",
 "EBMT": "European Society for Blood and Marrow Transplantation", "ECOG": "Eastern Cooperative Oncology Group", "EHA": "European Hematology Association",
 "ERIC": "European Research Initiative on CLL", "FDG": "Fluorodeoxyglucose", "FISH": "Fluorescence in situ hybridization",
 "GCLLSG": "German CLL Study Group", "GELLC": "Spanish CLL Study Group", "GM-CSF": "Granulocyte-macrophage colony-stimulating factor",
 "HR": "Hazard ratio", "hyper-CVXD": "Fractionated cyclophosphamide, vincristine, liposomal daunorubicin, dexamethasone",
 "ICANS": "Immune effector cell-associated neurotoxicity syndrome", "IGHV": "Immunoglobulin heavy-chain variable region gene (mutated or unmutated)",
 "LDH": "Lactate dehydrogenase", "MRD": "Measurable (minimal) residual disease", "NCCN": "National Comprehensive Cancer Network", "NCRI": "National Cancer Research Institute (UK)",
 "OFAR": "Oxaliplatin, fludarabine, cytarabine, rituximab", "ORR": "Overall response rate", "OS": "Overall survival", "PD-1": "Programmed cell death protein 1",
 "PD-L1": "Programmed death-ligand 1", "PET-CT": "Positron emission tomography with computed tomography", "PFS": "Progression-free survival",
 "PR": "Partial response", "R-CHOP": "Rituximab with CHOP", "R-EPOCH": "Rituximab, etoposide, prednisone, vincristine, cyclophosphamide, doxorubicin (infusional)",
 "SLL": "Small lymphocytic lymphoma", "SUVmax": "Maximum standardized uptake value on PET", "TP53": "Tumor protein p53 gene; disruption means del(17p) or TP53 mutation",
 "VR-EPOCH": "Venetoclax with dose-adjusted R-EPOCH", "del(17p)": "Deletion of the short arm of chromosome 17, the site of TP53"}
gl = '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl></details>' % (
    len(GLOSS), ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in sorted(GLOSS.items(), key=lambda kv: kv[0].lower())))
s, n = re.subn(r'<details class="gloss">.*?</details>', lambda m: gl, s, count=1, flags=re.S); assert n == 1

FOOT = ('Every result was checked against the paper\'s PubMed abstract on %(d)s; values marked "full paper" were checked against the full text in PubMed Central, and "not reported in abstract" means the figure needs the full text. '
 '"Key toxicity" summarizes the main adverse events reported in the abstract; it is not a complete safety profile. '
 '"Drug mechanism" links one recent review per drug or drug class on how it works and how resistance develops, chosen from peer-reviewed journals as the most recent, comprehensive and high-quality review available (no promotional material), with free full text preferred when quality was comparable. '
 '"★ Core" marks studies selected as essential for teaching. '
 'Studies included: Richter transformation is rare and has no randomized trials, so the usual rule for this site (phase 3 trials and selected phase 2 trials) would leave almost nothing. This topic therefore lists the prospective trials published in Richter transformation, whatever the journal, the larger retrospective, registry and genomic studies that shape prognosis and practice, and the consensus and guideline documents. First-line and relapsed disease are covered together. '
 'Small case series, single-agent reports with fewer than 9 patients and reports published only as meeting abstracts are not listed. '
 'Each result is tagged "✓ abstract" or "✓ abstract + full paper" by what it was checked against. '
 '"Free full text" links open the article in PubMed Central; "Free at publisher" links open a publisher page that is free to read; "Publisher" links open the publisher\'s page, where a subscription or institutional access may be needed; "Free copy (repository)" links open a legal free copy in a university repository (sometimes the authors\' manuscript). Free copies were found with Unpaywall (%(d)s). '
 'Registry links (NCT numbers) open the trial\'s registry record and were taken from each paper\'s PubMed record, abstract or full text. '
 'Source links go to the PubMed record (PMIDs checked against journal, volume, pages and first author). '
 '"Builds on", "Changed" and "Open questions" are interpretive summaries, not data from the papers. Commentaries are those PubMed links to each paper ("Comment in"); letters and author replies are not listed. '
 'No drug has an approval specific to Richter transformation; regulatory notes say so for each agent, and one item marked "verify" will be checked at the next update. '
 'Guideline statements from the EHA 2026 guidelines were checked against their full text; placements marked "NCCN not checked" could not be confirmed, because the NCCN guidelines require a login. No public data report insurance approval rates. '
 'Last checked: %(d)s.') % {'d': CHECKED}
s, n = re.subn(r'(<footer>\s*)Every result was checked.*?(\s*<p class="sitedisc">)', lambda m: m.group(1) + FOOT + m.group(2), s, count=1, flags=re.S); assert n == 1
open(out, 'w', encoding='utf-8').write(s)
print('entries', len(names))
