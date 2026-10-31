"""Prognosis pilot (NDMM, Oct 31, 2026): add the new Established entries to T (category "risk"), with FT, TOX,
two CORE names, extras on existing cards, the PROG fields (kind, type, validation, chip label) for every
risk entry, PROGMAP (trial -> prognostic entries used in its design) and new abbreviations.
Every number was checked against the PubMed abstract on Oct 31, 2026.
Usage: python3 tools/prognosis/ndmm_entries.py source/ndmm.html   (rerunnable: skips what is already there)"""
import sys, json, re

page = sys.argv[1]
h = open(page, encoding="utf-8").read()
J = lambda o: json.dumps(o, ensure_ascii=False)

NEW = [
 dict(y=2015, n="IMWG frailty score (Palumbo)", s="risk", ph="Prognostic model",
      d="Pooled geriatric assessment data from 3 prospective trials in older patients with newly diagnosed myeloma",
      ep="OS; grade ≥3 nonhematologic AEs; treatment discontinuation",
      r="Fit (score 0), intermediate (1) and frail (≥2): 3-yr OS 84%, 76% and 57%; grade ≥3 nonhematologic AEs at 12 mo 22.2%, 26.4% and 34.0%; discontinuation at 12 mo 16.5%, 20.8% and 31.2%",
      N="869", hr="3.57 (OS, frail vs fit)", fu="not reported in abstract",
      c="Blood 2015;125:2068", p=25628469, extra=["Simplified frailty scale (Facon, Leukemia 2020)", 31427722],
      b="Brought geriatric assessment (age, comorbidities, cognitive and physical function) into myeloma risk assessment.",
      i="Predicts both survival and toxicity; IMWG proposed it for designing trials in older patients.",
      q="Does frailty-adapted dosing improve outcomes with anti-CD38 combinations? Which simplified version should practice use?",
      cm=[[25814486, "Mellqvist UH, Blood 2015", "New prognostic tools for myeloma"], [29732537, "Larocca A, Br J Haematol 2018", "Gentle yet effective combination therapy with novel agents in elderly multiple myeloma patients"]],
      reg="—", gl="Guideline placement not checked (NCCN not checked).", acc="—"),
 dict(y=2019, n="UK MRA Myeloma Risk Profile (Cook)", s="risk", ph="Prognostic model",
      d="Transplant-ineligible newly diagnosed myeloma; developed in Myeloma XI, externally validated in MRC Myeloma IX",
      ep="OS",
      r="WHO performance status, ISS, age and CRP define low-, medium- and high-risk groups, also associated with PFS and early mortality; prognostic across regimens and in genetic high-risk disease",
      N="1,852 (development); 520 (validation)", hr="not reported in abstract", fu="not reported in abstract",
      c="Lancet Haematol 2019;6:e154", p=30738834, extra=["Danish registry validation (Redder, Br J Haematol 2021)", 32515050],
      b="Uses routine clinical data rather than a geriatric assessment questionnaire.",
      i="A frailty-type risk estimate from data available at diagnosis, externally validated in trial and registry cohorts.",
      q="Does it keep its value with daratumumab-based regimens, and does it add to the IMWG frailty score?",
      cm=[], reg="—", gl="Guideline placement not checked (NCCN not checked).", acc="—"),
 dict(y=2019, n="Double-hit myeloma (Walker)", s="risk", ph="Genomic risk group",
      d="Whole-genome and exome data from the Myeloma Genome Project",
      ep="PFS, OS",
      r="Biallelic TP53 inactivation, or CKS1B (1q21) amplification (≥4 copies) with ISS III: 6.1% of patients; median PFS 15.4 mo and OS 20.7 mo",
      N="1,273 (genomic); 784 (model)", hr="n/a", fu="not reported in abstract",
      c="Leukemia 2019;33:159", p=29967379,
      b="Moved from single FISH abnormalities to combinations defined by sequencing.",
      i="Defined a small group with very poor outcomes despite modern therapy; TP53 inactivation is part of the 2025 IMS/IMWG high-risk definition.",
      q="Does any current approach, including early T-cell redirection, overcome double-hit disease?",
      cm=[[30464803, "Walker BA, Oncotarget 2018", "The genomic features associated with high-risk multiple myeloma"]],
      reg="—", gl="Guideline placement not checked (NCCN not checked).", acc="Requires sequencing; not routine."),
 dict(y=2022, n="Circulating tumor cells and plasma cell leukemia (Garcés)", s="risk", ph="Biomarker",
      d="Circulating tumor cells by next-generation flow at diagnosis, GEM2012MENOS65 and GEM2014MAIN (transplant-eligible)",
      ep="PFS",
      r="Circulating tumor cells detected in 92%; ≥0.01% independently prognostic for PFS with ISS, LDH and cytogenetics; patients with undetectable cells had excellent PFS regardless of CR or MRD",
      N="374", hr="2.02 (95% CI 1.3–3.1)", fu="not reported in abstract",
      c="J Clin Oncol 2022;40:3151", p=35666958, extra=["PERSEUS validation (Bertamini, Blood 2026)", 41060326],
      b="IMWG redefined primary plasma cell leukemia as ≥5% circulating plasma cells (2021), previously ≥20%.",
      i="Showed that far lower levels, measured by flow cytometry in blood, carry independent prognostic weight.",
      q="Which threshold (0.01% here, 0.175% in PERSEUS) and which assay? Should circulating tumor cells enter staging?",
      cm=[[35759726, "Chakraborty R, J Clin Oncol 2022", "Circulating tumor cell burden as a component of staging in multiple myeloma: ready for prime time?"], [36179274, "Kostopoulos IV, J Clin Oncol 2023", "Circulating plasma cells in newly diagnosed multiple myeloma: prognostic and more"]],
      reg="—", gl="Primary plasma cell leukemia threshold per IMWG 2021; guideline placement not checked (NCCN not checked).", acc="—"),
 dict(y=2016, n="IMWG response and MRD criteria (Kumar)", s="risk", ph="Consensus",
      d="IMWG consensus on response categories and minimal residual disease assessment",
      ep="—",
      r="MRD categories require a complete response: flow MRD-negative (next-generation flow, EuroFlow method, minimum sensitivity 1 in 10⁵ nucleated cells), sequencing MRD-negative (NGS, minimum 1 in 10⁵), imaging plus MRD-negative (marrow negativity plus resolution of PET-CT uptake) and sustained MRD-negative (marrow and imaging negativity confirmed at least 1 year apart); MRD testing starts at suspected complete response (full paper)",
      N="n/a", hr="n/a", fu="n/a",
      c="Lancet Oncol 2016;17:e328", p=27511158,
      b="Conventional complete response became too insensitive as treatment deepened responses.",
      i="Became the common definition of MRD response used in trials and regulatory discussions.",
      q="Which assay, threshold and timepoints matter most? Can MRD guide when to stop treatment?",
      cm=[], reg="—", gl="Consensus criteria; guideline adoption not checked (NCCN not checked).", acc="—"),
 dict(y=2024, n="EVIDENCE meta-analysis (Landgren)", s="risk", ph="Meta-analysis",
      d="Randomized phase 2–3 trials with MRD at 12 ± 3 months, analyzed following FDA guidance on MRD as an endpoint",
      ep="Trial-level and patient-level association of 12-month MRD negativity with PFS",
      r="Trial level: R² 0.67 (weighted least squares; 95% CI 0.43–0.91) and 0.84 (copula); patient level: global OR 4.02 (2.57–5.46). Relapsed disease (4 trials): patient-level OR 7.67",
      N="4,907 (8 newly diagnosed trials)", hr="n/a", fu="n/a",
      c="Blood 2024;144:359", p=38768337,
      b="Earlier meta-analyses (Munshi) showed patient-level prognostic value; this tested whether a treatment effect on MRD predicts a treatment effect on PFS.",
      i="Concluded that MRD is reasonably likely to predict PFS benefit, supporting MRD as an accelerated-approval endpoint.",
      q="Does 12-month MRD predict OS? Does the relationship hold for new drug classes such as T-cell engagers?",
      cm=[[39052265, "Costa LJ, Blood 2024", "MRD accelerating myeloma drug development"]],
      reg="Presented by its lead author at the FDA advisory committee (ODAC) meeting of April 12, 2024, alongside analyses by the FDA and i2TEAMM; ODAC voted 12–0 that the data support MRD as an accelerated-approval endpoint in myeloma (confirmed October 31, 2026).",
      gl="Guideline placement not checked (NCCN not checked).", acc="—"),
 dict(y=2022, n="Sustained MRD in MAIA and ALCYONE (San-Miguel)", s="risk", ph="Secondary analysis",
      d="MRD by NGS (10⁻⁵) in patients reaching ≥CR in two phase 3 transplant-ineligible trials",
      ep="PFS by MRD status and by sustained MRD negativity (≥6 and ≥12 mo)",
      r="MRD negativity and sustained negativity associated with better PFS in all arms; MRD negativity sustained ≥12 mo: D-Rd 10.9% vs Rd 2.4%, D-VMP 14.0% vs VMP 2.8%",
      N="MAIA 368 vs 369; ALCYONE 350 vs 356", hr="not reported in abstract", fu="36.4 mo (MAIA); 40.1 mo (ALCYONE)",
      c="Blood 2022;139:492", p=34269818,
      b="Moved from MRD at one time point to its durability.",
      i="Showed that treatment can raise sustained MRD negativity and that durable negativity tracks with PFS.",
      q="How long must negativity last before therapy can be stopped?",
      cm=[[35084473, "Bianchi G, Blood 2022", "Sustained minimal residual disease in myeloma"]],
      reg="—", gl="Guideline placement not checked (NCCN not checked).", acc="—"),
 dict(y=2018, n="MRD at 10⁻⁶ in IFM 2009 (Perrot)", s="risk", ph="Secondary analysis",
      d="NGS MRD (<10⁻⁶) during lenalidomide maintenance in IFM 2009 (RVd with or without transplant)",
      ep="PFS, OS",
      r="MRD-negative at least once during maintenance in 25%; MRD at the start of maintenance: adjusted HR 0.22 for PFS and 0.24 for OS, regardless of arm, cytogenetic risk or ISS",
      N="127 MRD-negative (total not reported in abstract)", hr="0.22 (PFS); 0.24 (OS), adjusted", fu="not reported in abstract",
      c="Blood 2018;132:2456", p=30249784,
      b="Used a deeper threshold (10⁻⁶) than the IMWG minimum of 10⁻⁵.",
      i="Supported MRD by NGS as a major prognostic factor and as a basis for MRD-adapted trials.",
      q="Is 10⁻⁶ worth the extra effort compared with 10⁻⁵?",
      cm=[[30523123, "San-Miguel JF, Blood 2018", "How deep is the myeloma iceberg?"]],
      reg="—", gl="Guideline placement not checked (NCCN not checked).", acc="MRD test coverage varies."),
 dict(y=2017, n="PET-CT in IMAJEM (Moreau)", s="risk", ph="Prospective imaging study",
      d="MRI and FDG PET-CT at diagnosis, after 3 cycles of RVd and before maintenance, within IFM/DFCI 2009",
      ep="Bone lesion detection (primary); PFS, OS",
      r="PET-CT normalized after 3 cycles in 32%, with 30-mo PFS 78.7% vs 56.8%; normalization before maintenance independently prognostic for PFS; MRI normalization not predictive; extramedullary disease at diagnosis independently prognostic for PFS and OS",
      N="134", hr="not reported in abstract", fu="not reported in abstract",
      c="J Clin Oncol 2017;35:2911", p=28686535, extra=["IMWG PET/CT consensus (Cavo, Lancet Oncol 2017)", 28368259],
      b="MRI and PET-CT detected bone lesions equally well at diagnosis (95% vs 91%); the question was which one tracks response.",
      i="Supported PET-CT rather than MRI for assessing response; IMWG named PET-CT the preferred functional imaging to monitor therapy.",
      q="Does PET negativity add to marrow MRD negativity in the quadruplet era?",
      cm=[], reg="—", gl="Guideline placement not checked (NCCN not checked).", acc="—"),
]

FT_NEW = {
 "IMWG frailty score (Palumbo)": ["pmc", "PMC4375104"],
 "UK MRA Myeloma Risk Profile (Cook)": ["pmc", "PMC6391517"],
 "Double-hit myeloma (Walker)": ["pmc", "PMC6326953"],
 "Circulating tumor cells and plasma cell leukemia (Garcés)": ["doi", "10.1200/JCO.21.01365", "free"],
 "IMWG response and MRD criteria (Kumar)": ["doi", "10.1016/S1470-2045(16)30206-6"],
 "EVIDENCE meta-analysis (Landgren)": ["pmc", "PMC11418064"],
 "Sustained MRD in MAIA and ALCYONE (San-Miguel)": ["pmc", "PMC8796656"],
 "MRD at 10⁻⁶ in IFM 2009 (Perrot)": ["pmc", "PMC6284215"],
 "PET-CT in IMAJEM (Moreau)": ["pmc", "PMC5578392"],
}
TOX_NEW = {
 "IMWG frailty score (Palumbo)": "Not applicable (prognostic model)",
 "UK MRA Myeloma Risk Profile (Cook)": "Not applicable (prognostic model)",
 "Double-hit myeloma (Walker)": "Not applicable (genomic risk group)",
 "Circulating tumor cells and plasma cell leukemia (Garcés)": "Not applicable (biomarker)",
 "IMWG response and MRD criteria (Kumar)": "Not applicable (consensus definition)",
 "EVIDENCE meta-analysis (Landgren)": "Not applicable (meta-analysis)",
 "Sustained MRD in MAIA and ALCYONE (San-Miguel)": "Not applicable (secondary analysis)",
 "MRD at 10⁻⁶ in IFM 2009 (Perrot)": "Not applicable (secondary analysis)",
 "PET-CT in IMAJEM (Moreau)": "Not applicable (imaging study)",
}
CORE_ADD = ["IMWG response and MRD criteria (Kumar)", "EVIDENCE meta-analysis (Landgren)"]
EXTRA_OLD = {
 "MRD meta-analysis (Munshi)": ["2020 update (Munshi, Blood Adv 2020)", 33284948],
 "IMS/IMWG high-risk consensus (Avet-Loiseau)": ["2016 IMWG definition (Sonneveld, Blood 2016)", 27002115],
}
# pt: model | bio | resp.  pk: kind.  val: validation.  sh: short chip label.
PROG = {
 "International Staging System (Greipp)": dict(pt="model", pk="Prognostic", sh="ISS",
   val="Training and validation sets within the original international dataset (10,750 patients, full paper); the base of R-ISS and R2-ISS."),
 "Revised ISS (Palumbo)": dict(pt="model", pk="Prognostic", sh="R-ISS",
   val="Pooled data from 11 international trials (3,060 of 4,445 patients had complete data); refined by R2-ISS for the large intermediate group."),
 "R2-ISS (D'Agostino)": dict(pt="model", pk="Prognostic", sh="R2-ISS",
   val="Training set of 7,072 patients from 16 trials; validated in an independent set of 3,771 patients (1,214 with complete data)."),
 "IMWG frailty score (Palumbo)": dict(pt="model", pk="Prognostic", sh="Frailty",
   val="Developed in pooled trial data. A simplified version (age, Charlson comorbidity index, ECOG) was tested retrospectively in the FIRST trial (ECOG data in 1,618 patients)."),
 "UK MRA Myeloma Risk Profile (Cook)": dict(pt="model", pk="Prognostic", sh="MRP",
   val="Externally validated in MRC Myeloma IX (D-statistic 0.654) and in the Danish national registry (1,377 patients; HR 2.91 for early death, high vs low risk)."),
 "IMS/IMWG high-risk consensus (Avet-Loiseau)": dict(pt="bio", pk="Consensus definition", sh="High risk",
   val="Consensus of IMS and IMWG; updates the 2016 IMWG definition (Sonneveld, Blood 2016)."),
 "Double-hit myeloma (Walker)": dict(pt="bio", pk="Prognostic", sh="Double hit",
   val="Validated in an independent dataset (per abstract)."),
 "Circulating tumor cells and plasma cell leukemia (Garcés)": dict(pt="bio", pk="Prognostic", sh="CTC",
   val="Confirmed in PERSEUS (451 patients): HR 1.36 per unit as a continuous variable, optimal threshold 0.175%; D-VRd improved PFS in patients with low counts (HR 0.42). IMWG 2021: ≥5% circulating plasma cells defines primary plasma cell leukemia (Fernández de Larrea, Blood Cancer J 2021)."),
 "IMWG response and MRD criteria (Kumar)": dict(pt="resp", pk="Consensus definition", sh="MRD",
   val="Consensus definition. Minimum sensitivity 1 in 10⁵ nucleated cells by flow or sequencing; sustained negativity requires confirmation at least 1 year apart, with the method annotated (full paper)."),
 "MRD meta-analysis (Munshi)": dict(pt="resp", pk="Prognostic; surrogate candidate", sh="MRD meta",
   val="Patient-level association. The 2020 update (44 studies, 8,098 patients) found HR 0.33 for PFS and 0.45 for OS; trial-level surrogacy was tested by the EVIDENCE meta-analysis (2024)."),
 "EVIDENCE meta-analysis (Landgren)": dict(pt="resp", pk="Surrogate endpoint", sh="EVIDENCE",
   val="Trial-level analysis across 8 randomized trials in newly diagnosed myeloma, following FDA guidance."),
 "Sustained MRD in MAIA and ALCYONE (San-Miguel)": dict(pt="resp", pk="Prognostic", sh="Sustained MRD",
   val="Two randomized trials; the association held in every treatment arm."),
 "MRD at 10⁻⁶ in IFM 2009 (Perrot)": dict(pt="resp", pk="Prognostic", sh="MRD 10⁻⁶",
   val="One randomized trial; held regardless of arm, cytogenetic risk and ISS."),
 "PET-CT in IMAJEM (Moreau)": dict(pt="resp", pk="Prognostic", sh="PET-CT",
   val="One prospective study (134 patients); IMWG consensus (2017) on PET-CT in response assessment."),
}
# Trial -> [[prognostic entry, how the trial used it]]: design-level use only (endpoint, eligibility, stratification,
# treatment assignment), taken from each card's verified endpoint.
PROGMAP = {
 "MASTER (Costa)": [["IMWG response and MRD criteria (Kumar)", "Primary endpoint; MRD guided consolidation and stopping therapy"]],
 "GMMG-HD7 (Goldschmidt)": [["IMWG response and MRD criteria (Kumar)", "Primary endpoint (MRD negativity after induction)"]],
 "EMN24 IsKia (Gay)": [["IMWG response and MRD criteria (Kumar)", "Primary endpoint (NGS MRD after consolidation)"]],
 "CEPHEUS (Usmani)": [["IMWG response and MRD criteria (Kumar)", "Primary endpoint (MRD negativity at 10⁻⁵)"]],
}
GLOSS = {
 "C-index": "Concordance index (how well a model ranks patients by risk; 0.5 = chance, 1 = perfect)",
 "CI": "Confidence interval",
 "CRP": "C-reactive protein",
 "CTC": "Circulating tumor cells",
 "FDG": "Fluorodeoxyglucose",
 "GEP": "Gene expression profiling",
 "IRMMa": "Individualized risk model for myeloma",
 "MRI": "Magnetic resonance imaging",
 "MRP": "Myeloma Risk Profile (UK Myeloma Research Alliance)",
 "ODAC": "Oncologic Drugs Advisory Committee (FDA)",
 "PET-CT": "Positron emission tomography-computed tomography",
 "WHO": "World Health Organization",
}

def jsobj(t):
    keys = ["y","n","s","ph","d","ep","r","N","hr","fu","c","p","extra","b","i","q","cm","reg","gl","acc"]
    return "{" + ",".join(k + ":" + J(t[k]) for k in keys if k in t) + "}"

changed = []
# 1. New T entries, appended at the end of T.
a = h.index("const T = [")
end = h.index("\n];", a)
for t in NEW:
    if 'n:' + J(t["n"]) in h[a:end] or ('n:"' + t["n"] + '"') in h[a:end]:
        continue
    h = h[:end] + ",\n" + jsobj(t) + h[end:]
    end = h.index("\n];", a)
    changed.append("T+" + t["n"])
# 2. Extras on existing cards.
for name, ex in EXTRA_OLD.items():
    m = re.search(r'\{y:\d+,n:' + re.escape(J(name)) + r'.*?\n c:"[^"]*",p:\d+,', h, re.S)
    if m and "extra:" not in h[m.start():m.end() + 40]:
        h = h[:m.end()] + "extra:" + J(ex) + "," + h[m.end():]
        changed.append("extra:" + name)
# 3. FT and TOX.
def merge(objname, add):
    global h
    m = re.search(r'const ' + objname + r' = (\{.*?\});\n', h)
    d = json.loads(m.group(1))
    n0 = len(d); d.update({k: v for k, v in add.items() if k not in d})
    if len(d) != n0:
        h = h[:m.start()] + "const " + objname + " = " + J(d) + ";\n" + h[m.end():]
        changed.append(objname)
merge("FT", FT_NEW); merge("TOX", TOX_NEW)
# 4. CORE.
m = re.search(r'const CORE = (\[.*?\]);\n', h)
core = json.loads(m.group(1))
add = [c for c in CORE_ADD if c not in core]
if add:
    h = h[:m.start()] + "const CORE = " + J(core + add) + ";\n" + h[m.end():]
    changed.append("CORE")
# 5. PROG and PROGMAP (replaced each run).
line = "const PROG = " + J(PROG) + ";\nconst PROGMAP = " + J(PROGMAP) + ";\n"
if "const PROG = " in h:
    h = re.sub(r'const PROG = .*?;\nconst PROGMAP = .*?;\n', lambda _: line, h, count=1)
else:
    i = h.index("const PAGEKEY")
    h = h[:i] + "// Added Oct 31, 2026 (Prognosis pilot). PROG: kind, type, validation and chip label for each prognostic entry; PROGMAP: trial -> prognostic entries used in its design.\n" + line + h[i:]
changed.append("PROG")
# 6. Abbreviations.
g = re.search(r'<details class="gloss"><summary>Abbreviations \((\d+)\)</summary><dl>(.*?)</dl>', h, re.S)
pairs = re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', g.group(2))
have = {k for k, _ in pairs}
pairs += [(k, v) for k, v in GLOSS.items() if k not in have]
pairs.sort(key=lambda kv: kv[0].lower())
dl = "".join("<dt>%s</dt><dd>%s</dd>" % kv for kv in pairs)
h = h[:g.start()] + '<details class="gloss"><summary>Abbreviations (%d)</summary><dl>%s</dl>' % (len(pairs), dl) + h[g.end():]

# Every PROG/PROGMAP name must exist in T.
names = set(re.findall(r'\{y:\d+,n:"((?:[^"\\]|\\.)*)"', h))
for k in list(PROG) + [x[0] for v in PROGMAP.values() for x in v] + list(PROGMAP):
    assert json.loads('"' + k.replace('"', '\\"') + '"') in names or k in names, "missing in T: " + k
open(page, "w", encoding="utf-8").write(h)
print("ok:", ", ".join(changed))
