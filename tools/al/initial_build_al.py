"""One-time build of the AL amyloidosis page (key al) from the relapsed FL page, November 15, 2026.
Usage (from the repository root): python3 tools/al/initial_build_al.py <out.html>
After this first build the page itself (source/al.html) is the master copy: edit it directly, as for other topics
(tools/UPDATE_GUIDE.md). Then run, from tools/: mechs/install_mechtab.py, review/build_persp.py al, review/install_persptint.py."""
import re, json, sys, urllib.parse
out = sys.argv[1]
s = open('source/flr.html', encoding='utf-8').read()
KEY, TITLE = 'al', 'AL amyloidosis'
CHECKED = 'November 15, 2026'

def sub1(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

sub1('<title>Relapsed Follicular Lymphoma</title>', '<title>AL Amyloidosis Landmark Studies</title>')
sub1('<div class="eyebrow">Relapsed/refractory follicular lymphoma · 2002–2026</div>', '<div class="eyebrow">Immunoglobulin light chain (AL) amyloidosis · 2002–2026</div>')
sub1('<h1>Landmark trials in relapsed and refractory follicular lymphoma</h1>', '<h1>Landmark studies in AL amyloidosis</h1>')
s = re.sub(r'(<h1>Landmark studies in AL amyloidosis</h1>\s*<p>).*?(</p>)',
           lambda m: m.group(1) + 'How to prove the amyloid is AL and not ATTR, AA or a hereditary type (tissue typing, the monoclonal protein screen, bone scintigraphy and cardiac MRI); cardiac staging, prognostic markers and response criteria; first-line therapy and transplantation; relapsed disease; and fibril-directed antibodies: design, verified results, context, open questions and reception.' + m.group(2), s, count=1, flags=re.S)
enc = urllib.parse.quote('Landmark trials (%s): comment' % TITLE, safe='')
old = 'Landmark%20trials%20%28Relapsed%20follicular%20lymphoma%29%3A%20comment'
assert s.count(old) == 2; s = s.replace(old, enc)
s = s.replace('"fl2-sort"', '"al-sort"')
sub1('.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }',
     '.tag.rr { color: var(--s-rr); background: var(--s-rr-bg); }\n.tag.risk { color: var(--muted); background: var(--bg); box-shadow: inset 0 0 0 1px var(--rule); }')

ent = open('tools/al/al_entries.js', encoding='utf-8').read()
i, j = s.index('const SETTINGS = {'), s.index('const REG = ')
s = s[:i] + ent.rstrip() + '\n' + s[j:]

REG = {"Boston University BNP staging (Lilleness)": ["NCT00898235"], "High-dose melphalan vs MDex (Jaccard)": ["NCT00344526"],
 "Bortezomib-dexamethasone induction before transplantation (Huang)": ["NCT01998503"], "BMDex vs MDex (Kastritis)": ["NCT01277016"],
 "ANDROMEDA (Kastritis)": ["NCT03201965"], "EMN22, daratumumab in stage IIIb (Kastritis)": ["NCT04131309"],
 "Bortezomib, once vs twice weekly (Reece)": ["NCT00298766"], "Pomalidomide-dexamethasone (Dispenzieri)": ["NCT00558896"],
 "Daratumumab monotherapy, relapsed (Roussel)": ["NCT02816476"], "Daratumumab monotherapy, relapsed (Sanchorawala)": ["NCT02841033"],
 "Bendamustine-dexamethasone (Lentzsch)": ["NCT01222260"], "TOURMALINE-AL1 (Dispenzieri)": ["NCT01659658"],
 "SWOG S1702, isatuximab (Parker)": ["NCT03499808"], "NEOD001 (birtamimab) phase 1/2 (Gertz)": ["NCT01707264"],
 "Doxycycline with CyBorD (Shen)": ["NCT03401372"], "VITAL, birtamimab (Gertz)": ["NCT02312206"],
 "CARES, anselamimab (Wechalekar)": ["NCT04512235", "NCT04504825"]}
FTP = json.load(open('tools/al/ft.json', encoding='utf-8'))  # PMID -> full-text link (Unpaywall checked Nov 15, 2026)
names = re.findall(r'\n\{y:\d+,n:"([^"]+)"', ent)
pm = dict(re.findall(r'\n\{y:\d+,n:"([^"]+)".*?\bp:(\d+)', ent, flags=re.S))
FT = {n: FTP[pm[n]] for n in names}
NA = "Not applicable (%s)."
TOX = {
 "Hereditary amyloidosis misdiagnosed as AL (Lachmann)": NA % "genetic screening study",
 "Cardiac MRI in cardiac amyloidosis (Maceira)": NA % "diagnostic study",
 "Abdominal fat aspiration (van Gameren)": NA % "diagnostic study",
 "Free light chains with immunofixation (Palladini)": NA % "diagnostic study",
 "AL vs ATTR cardiac profiles (Rapezzi)": NA % "cohort study",
 "Mass spectrometry typing (Vrana)": NA % "diagnostic study",
 "Immunohistochemistry typing (Schönland)": NA % "diagnostic study",
 "Renal amyloidosis typing, 474 cases (Said)": NA % "pathology series",
 "DPD scintigraphy in AL and ATTR (Hutt)": NA % "diagnostic study",
 "Nonbiopsy diagnosis of cardiac ATTR (Gillmore)": NA % "diagnostic study",
 "MGUS in ATTR amyloidosis (Phull)": NA % "cohort study",
 "Mass spectrometry typing, 16,175 samples (Dasari)": NA % "laboratory series",
 "ESC position statement on cardiac amyloidosis (Garcia-Pavia)": NA % "position statement",
 "Mayo 2004 cardiac staging (Dispenzieri)": NA % "prognostic model",
 "Consensus organ involvement and response criteria (Gertz)": NA % "consensus statement",
 "Revised Mayo 2012 staging (Kumar)": NA % "prognostic model",
 "Hematologic and cardiac response criteria (Palladini)": NA % "response criteria",
 "European stage IIIb, NT-proBNP >8500 ng/L (Wechalekar)": "Not reported in abstract (cohort study of treatment outcomes); 42% died before the first response assessment.",
 "Marrow plasma cells >10% (Kourelis)": NA % "cohort study",
 "Renal staging and response (Palladini)": NA % "prognostic model",
 "t(11;14) and bortezomib (Bochtler)": NA % "cohort study of cytogenetics",
 "Boston University BNP staging (Lilleness)": NA % "prognostic model",
 "MRD by next-generation flow (Palladini)": NA % "cohort study",
 "Graded cardiac response criteria (Muchtar)": NA % "response criteria",
 "Extracellular volume by cardiac MRI (Porcari)": NA % "imaging cohort",
 "AL-ISS with stage IIIC (Khwaja)": NA % "prognostic model",
 "High-dose melphalan and transplantation, 8-year series (Skinner)": "Mortality within 100 days of transplantation 13%, highest with cardiomyopathy.",
 "Melphalan-dexamethasone (Palladini)": "Severe adverse events in 11% (3 of 5 hospitalised); no treatment-related deaths.",
 "High-dose melphalan vs MDex (Jaccard)": "Not reported in abstract; early mortality of 24% with transplantation in this trial, as cited by the CIBMTR analysis (D'Souza 2015).",
 "Bortezomib-dexamethasone induction before transplantation (Huang)": "Treatment-related mortality 3.6% (2 deaths within 100 days of transplantation).",
 "CyBorD, European study (Palladini)": "Not reported in abstract.",
 "CIBMTR transplantation trends (D'Souza)": "Mortality at 30 and 100 days 3% and 5% in 2007–2012 (11% and 20% in 1995–2000).",
 "BMDex vs MDex (Kastritis)": "Grade 3–4 adverse events in 20% vs 10% of cycles, mostly cytopenias, peripheral neuropathy and heart failure.",
 "ANDROMEDA (Kastritis)": "Grade 3–4 lymphopenia 13.0% vs 10.1%, pneumonia 7.8% vs 4.3%, cardiac failure 6.2% vs 4.8%, diarrhea 5.7% vs 3.7%; systemic administration reactions 7.3%; deaths 27 vs 29, mostly from cardiomyopathy.",
 "EMN22, daratumumab in stage IIIb (Kastritis)": "Serious adverse events: cardiac failure 25%, sudden cardiac death 10%, acute kidney injury 7.5%; quality of life stable.",
 "Lenalidomide-dexamethasone (Sanchorawala)": "25 mg/day poorly tolerated; fatigue and myelosuppression 35%; thromboembolism 9%.",
 "Bortezomib, once vs twice weekly (Reece)": "Grade ≥3 toxicity 50% (once weekly) vs 79% (twice weekly); discontinuation for toxicity 28% vs 38%, dose reduction 22% vs 53%.",
 "Pomalidomide-dexamethasone (Dispenzieri)": "Grade 3–5 neutropenia and fatigue the most common.",
 "Daratumumab monotherapy, relapsed (Roussel)": "No unexpected adverse events; rates not reported in abstract.",
 "Daratumumab monotherapy, relapsed (Sanchorawala)": "No grade 3–4 infusion reactions; grade ≥3 respiratory infections 18% and atrial fibrillation 18%.",
 "Bendamustine-dexamethasone (Lentzsch)": "Therapy-related grade 3–4 adverse events 65% (myelosuppression, fatigue, nausea and vomiting); no grade 5 events.",
 "Venetoclax, t(11;14) (Premkumar)": "Grade ≥3 adverse events 19%, 7% from infections.",
 "TOURMALINE-AL1 (Dispenzieri)": "Diarrhea 34% vs 30%, rash 33% vs 20%, cardiac arrhythmias 26% vs 15%, nausea 24% vs 14%.",
 "SWOG S1702, isatuximab (Parker)": "Treatment-related grade ≥3 lymphopenia 8.5% and infection 6%.",
 "NEOD001 (birtamimab) phase 1/2 (Gertz)": "No drug-related serious adverse events, dose-limiting toxicities or antidrug antibodies; fatigue, upper respiratory infection, cough and dyspnea most frequent.",
 "Doxycycline with CyBorD (Shen)": "Not reported in abstract.",
 "VITAL, birtamimab (Gertz)": "Treatment-emergent and serious adverse events similar between arms.",
 "CARES, anselamimab (Wechalekar)": "Generally well tolerated; safety comparable between arms."}
master = json.load(open('tools/moa_master.json', encoding='utf-8'))
MOA = {k: master[k] for k in ['pi', 'cd38', 'imid', 'bcl2', 'benda', 'fibril']}
P, D, I, F = ["pi"], ["cd38"], ["imid"], ["fibril"]
MOAMAP = {"Bortezomib-dexamethasone induction before transplantation (Huang)": P, "CyBorD, European study (Palladini)": P, "BMDex vs MDex (Kastritis)": P,
 "ANDROMEDA (Kastritis)": D, "EMN22, daratumumab in stage IIIb (Kastritis)": D, "Lenalidomide-dexamethasone (Sanchorawala)": I,
 "Bortezomib, once vs twice weekly (Reece)": P, "Pomalidomide-dexamethasone (Dispenzieri)": I, "Daratumumab monotherapy, relapsed (Roussel)": D,
 "Daratumumab monotherapy, relapsed (Sanchorawala)": D, "Bendamustine-dexamethasone (Lentzsch)": ["benda"], "Venetoclax, t(11;14) (Premkumar)": ["bcl2"],
 "TOURMALINE-AL1 (Dispenzieri)": P, "SWOG S1702, isatuximab (Parker)": D, "NEOD001 (birtamimab) phase 1/2 (Gertz)": F,
 "Doxycycline with CyBorD (Shen)": F, "VITAL, birtamimab (Gertz)": F, "CARES, anselamimab (Wechalekar)": F}
NEWD = json.load(open('tools/newdrugs/al.json', encoding='utf-8'))
WATCH = {"note": "Ongoing phase 3 trials, with up to three phase 2 trials designed to support an approval, selected from ClinicalTrials.gov (checked %s). Status and primary completion dates are as registered; some trials may already have presented results at meetings." % CHECKED,
 "items": [
  {"n": "S2213", "d": "Daratumumab-VCd induction followed by autologous transplantation vs daratumumab-VCd consolidation, both with daratumumab maintenance, in newly diagnosed AL amyloidosis", "ph": "Phase 3", "st": "Recruiting", "pcd": "2030-07-29 (estimated)", "ep": "Major organ deterioration progression-free survival", "nct": "NCT06022939"},
  {"n": "SCTC21C-B301", "d": "SCTC21C (subcutaneous) with bortezomib, cyclophosphamide and dexamethasone vs VCd alone in newly diagnosed AL amyloidosis", "ph": "Phase 3", "st": "Recruiting", "pcd": "2027-12 (estimated)", "ep": "Overall complete hematologic response", "nct": "NCT07388602"},
  {"n": "LINKER-AL1", "d": "Linvoseltamab (BCMA×CD3 bispecific) alone vs daratumumab-VCd in newly diagnosed AL amyloidosis", "ph": "Phase 3", "st": "Not yet recruiting", "pcd": "2035-07-25 (estimated)", "ep": "Safety; hematologic complete response by blinded independent review", "nct": "NCT07901725"},
  {"n": "M24-473", "d": "Etentamig (BCMA×CD3 bispecific, subcutaneous) vs daratumumab-CyBorD in newly diagnosed AL amyloidosis", "ph": "Phase 3", "st": "Not yet recruiting", "pcd": "2034-12 (estimated)", "ep": "Adverse events; hematologic complete response; MOD-PFS (randomized portion)", "nct": "NCT07793422"},
  {"n": "NEXICART-3", "d": "NXC-201 (BCMA CAR T cells) vs daratumumab-CyBorD in newly diagnosed AL amyloidosis", "ph": "Phase 3", "st": "Not yet recruiting", "pcd": "2028-12 (estimated)", "ep": "Overall complete hematologic response; MOD-PFS", "nct": "NCT07709715"},
  {"n": "LINKER-AL2", "d": "Linvoseltamab in relapsed or refractory AL amyloidosis", "ph": "Phase 1/2 (registrational)", "st": "Recruiting", "pcd": "2028-08-20 (estimated)", "ep": "Dose-limiting toxicity (phase 1); hematologic complete response by independent review (phase 2)", "nct": "NCT06292780"},
  {"n": "ALACRITY", "d": "AZD0120 (GC012F), CAR T cells targeting CD19 and BCMA, in relapsed or refractory AL amyloidosis", "ph": "Phase 1b/2 (registrational)", "st": "Recruiting", "pcd": "2029-08-15 (estimated)", "ep": "Adverse events (phase 1b); complete response (phase 2)", "nct": "NCT07081646"},
  {"n": "CM336-026101", "d": "CM336 (BCMA/CD3 bispecific antibody), two dose levels, in relapsed or refractory AL amyloidosis", "ph": "Phase 2 (registrational)", "st": "Recruiting", "pcd": "2026-06-30 (estimated)", "ep": "Efficacy (as registered)", "nct": "NCT07039578"}]}

def setconst(name, val):
    global s
    m = re.search(r'\nconst %s = (.*?);\n' % name, s)
    assert m and '\n' not in m.group(1), name
    s = s[:m.start(1)] + json.dumps(val, ensure_ascii=False) + s[m.end(1):]
for n, v in [('REG', REG), ('FT', FT), ('MOA', MOA), ('MOAMAP', MOAMAP), ('NEWD', NEWD), ('TOX', TOX), ('CORE', []), ('WATCH', WATCH)]:
    setconst(n, v)
sub1('const PAGEKEY = "flr";', 'const PAGEKEY = "%s";' % KEY)
sub1('const PAGETITLE = "Relapsed follicular lymphoma";', 'const PAGETITLE = "%s";' % TITLE)
for d in (REG, FT, TOX, MOAMAP):
    for k in d: assert k in names, k
for n in names: assert n in FT and n in TOX, n

GLOSS = {
 "AA amyloidosis": "Amyloidosis derived from serum amyloid A protein (chronic inflammation)", "AL amyloidosis": "Immunoglobulin light chain amyloidosis",
 "AL-ISS": "AL International Staging System", "ALECT2": "Amyloidosis derived from leukocyte chemotactic factor 2", "ATTR": "Transthyretin amyloidosis, wild-type (ATTRwt) or hereditary (variant)",
 "BCMA": "B-cell maturation antigen", "BMDex / VMDex": "Bortezomib, melphalan and dexamethasone", "BNP": "Brain (B-type) natriuretic peptide",
 "CAR": "Chimeric antigen receptor", "CI": "Confidence interval", "CIBMTR": "Center for International Blood and Marrow Transplant Research",
 "CRAB": "Hypercalcemia, renal failure, anemia and bone lesions (myeloma-defining features)", "CyBorD / VCd": "Cyclophosphamide, bortezomib and dexamethasone",
 "dFLC": "Difference between involved and uninvolved serum free light chains", "DPD": "99mTc-3,3-diphosphono-1,2-propanodicarboxylic acid, a bone scintigraphy tracer",
 "ECV": "Extracellular volume (cardiac MRI)", "eGFR": "Estimated glomerular filtration rate", "EHA": "European Hematology Association", "EMN": "European Myeloma Network",
 "ESC": "European Society of Cardiology", "FDA": "US Food and Drug Administration", "FISH": "Fluorescence in situ hybridization", "FLC": "Free light chain",
 "HR": "Hazard ratio", "IgM": "Immunoglobulin M", "IMiD": "Immunomodulatory drug (lenalidomide, pomalidomide)", "ISA": "International Society of Amyloidosis",
 "LV": "Left ventricular", "MDex": "Melphalan and high-dose dexamethasone", "MGUS": "Monoclonal gammopathy of undetermined significance",
 "MOD-PFS": "Major organ deterioration progression-free survival (hematologic progression, major organ deterioration or death)", "MRD": "Minimal residual disease",
 "MRI": "Magnetic resonance imaging", "NCCN": "National Comprehensive Cancer Network", "NT-proBNP": "N-terminal pro-brain natriuretic peptide",
 "NYHA": "New York Heart Association (heart failure class)", "OS": "Overall survival", "PFS": "Progression-free survival", "ROC": "Receiver operating characteristic",
 "SPECT": "Single-photon emission computed tomography", "SWOG": "SWOG Cancer Research Network", "TTR": "Transthyretin", "t(11;14)": "Translocation between chromosomes 11 and 14 (CCND1-IGH)",
 "κ / λ": "Kappa / lambda light chain isotype", "BCL2": "B-cell lymphoma 2 protein (target of venetoclax)", "CD19 / CD3 / CD38": "Cell-surface antigens: B-cell (CD19), T-cell receptor complex (CD3) and plasma cell (CD38, target of daratumumab and isatuximab)", "QRS": "Ventricular depolarization complex on the electrocardiogram", "T1": "Longitudinal relaxation time (cardiac MRI mapping)", "V122I": "Valine-to-isoleucine substitution at position 122 of transthyretin, a hereditary ATTR variant", "IMWG": "International Myeloma Working Group", "ESMO": "European Society for Medical Oncology", "ASCO": "American Society of Clinical Oncology", "AH": "Immunoglobulin heavy chain amyloidosis", "Complete hematologic response": "Normal free light chain ratio with negative serum and urine immunofixation",
 "Very good partial response": "dFLC below 40 mg/L", "Stage IIIb": "Mayo 2004 stage III with NT-proBNP above 8500 ng/L (European modification)"}
gl = '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl></details>' % (
    len(GLOSS), ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in sorted(GLOSS.items(), key=lambda kv: kv[0].lower())))
s, n = re.subn(r'<details class="gloss">.*?</details>', lambda m: gl, s, count=1, flags=re.S); assert n == 1

FOOT = ('Every result was checked against the paper\'s PubMed abstract on %(d)s; "not reported in abstract" means the figure needs the full text. '
 '"Key toxicity" summarizes the main adverse events reported in the abstract; it is not a complete safety profile. '
 '"Drug mechanism" links one recent review per drug or drug class on how it works and how resistance develops, chosen from peer-reviewed journals as the most recent, comprehensive and high-quality review available (no promotional material), with free full text preferred when quality was comparable. '
 '"★ Core" marks studies selected as essential for teaching. '
 'Studies included: AL amyloidosis has few randomized trials, so the list holds every phase 3 or randomized trial with a full report, phase 2 trials that defined a regimen in current use or were the basis of an approval or guideline recommendation (whatever the journal), large multicentre cohort studies that defined a regimen or the outcome of a high-risk group, and the diagnostic, typing, staging and response studies on which trials and practice rest. '
 'Because the diagnosis turns on proving that the amyloid is AL type, the first category covers the studies that separate AL from ATTR, AA, ALECT2 and hereditary amyloidoses: tissue typing, the monoclonal protein screen, bone scintigraphy and cardiac MRI. Supportive care, localized AL amyloidosis and IgM-related AL amyloidosis are not covered as separate cards. '
 'Each result is tagged "✓ abstract" or "✓ abstract + full paper" by what it was checked against. '
 '"Free full text" links open the article in PubMed Central; "Free at publisher" links open a publisher page that is free to read; "Publisher" links open the publisher\'s page, where a subscription or institutional access may be needed; "Free copy (repository)" links open a legal free copy in a university repository (sometimes the authors\' manuscript). Free copies were found with Unpaywall (%(d)s). '
 'Registry links (NCT numbers) open the trial\'s registry record and were taken from each paper\'s PubMed record or abstract. '
 'Source links go to the PubMed record (PMIDs checked against journal, volume, pages and first author). '
 '"Builds on", "Changed" and "Open questions" are interpretive summaries, not data from the papers. Commentaries are those PubMed links to each paper ("Comment in"); letters and author replies are not listed. '
 'FDA approval dates given in full were confirmed against FDA announcements (%(d)s); items marked "verify" could not be confirmed and will be checked at the next update. '
 'Guideline rows cite the EHA-ISA 2023 guideline on non-transplant chemotherapy (full text), the EHA-ISA 2022 transplant guideline (abstract) and the ESC 2021 position statement on cardiac amyloidosis (its diagnostic algorithm checked against published summaries; the full text could not be opened); placements marked "NCCN not checked" could not be confirmed, because the NCCN guidelines require a login. No public data report insurance approval rates; US coverage generally follows the FDA label and NCCN compendium listing. '
 'Last checked: %(d)s.') % {'d': CHECKED}
s, n = re.subn(r'(<footer>\s*)Every result was checked.*?(\s*<p class="sitedisc">)', lambda m: m.group(1) + FOOT + m.group(2), s, count=1, flags=re.S); assert n == 1
open(out, 'w', encoding='utf-8').write(s)
print('entries', len(names))
