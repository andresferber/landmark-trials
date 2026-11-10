"""Prognosis tab for relapsed myeloma (preview, Nov 9, 2026; not live until Andres approves).
Adds a Risk & response category with 5 entries (3 shared with the newly diagnosed page, 2 new: t(11;14) and
venetoclax; early relapse), PROG records and PROGMAP. Every number was checked against the PubMed abstract.
Usage: python3 rrmm_entries.py rrmm.html   (rerunnable)"""
import sys, json, re

page = sys.argv[1]
h = open(page, encoding="utf-8").read()
J = lambda o: json.dumps(o, ensure_ascii=False)

NEW = [
 {
  "y": 2025,
  "n": "IMS/IMWG high-risk consensus (Avet-Loiseau)",
  "s": "risk",
  "ph": "Consensus",
  "d": "New genomic definition of high-risk myeloma",
  "ep": "—",
  "r": "High risk = del(17p) >20% and/or TP53 mutation; t(4;14)/t(14;16)/t(14;20) with 1q+ and/or del(1p32); monoallelic del(1p32) with 1q+ or biallelic del(1p32); or β2M ≥5.5 mg/L with normal creatinine",
  "N": "n/a",
  "hr": "n/a",
  "fu": "n/a",
  "c": "J Clin Oncol 2025;43:2739",
  "p": 40489728,
  "extra": [
   "2016 IMWG definition (Sonneveld, Blood 2016)",
   27002115
  ],
  "b": "Updated the R-ISS-era definition with genomic and 1p/1q data.",
  "i": "Provides a common high-risk definition for trials and practice in the quadruplet era.",
  "q": "Should high-risk patients receive different therapy (tandem transplant, carfilzomib, anti-CD38 maintenance, early CAR-T)?",
  "cm": [],
  "reg": "—",
  "gl": "Consensus definition; NCCN adoption not checked.",
  "acc": "—"
 },
 {
  "y": 2016,
  "n": "IMWG response and MRD criteria (Kumar)",
  "s": "risk",
  "ph": "Consensus",
  "d": "IMWG consensus on response categories and minimal residual disease assessment",
  "ep": "—",
  "r": "MRD categories require a complete response: flow MRD-negative (next-generation flow, EuroFlow method, minimum sensitivity 1 in 10⁵ nucleated cells), sequencing MRD-negative (NGS, minimum 1 in 10⁵), imaging plus MRD-negative (marrow negativity plus resolution of PET-CT uptake) and sustained MRD-negative (marrow and imaging negativity confirmed at least 1 year apart); MRD testing starts at suspected complete response (full paper)",
  "N": "n/a",
  "hr": "n/a",
  "fu": "n/a",
  "c": "Lancet Oncol 2016;17:e328",
  "p": 27511158,
  "b": "Conventional complete response became too insensitive as treatment deepened responses.",
  "i": "Became the common definition of MRD response used in trials and regulatory discussions.",
  "q": "Which assay, threshold and timepoints matter most? Can MRD guide when to stop treatment?",
  "cm": [],
  "reg": "—",
  "gl": "Consensus criteria; guideline adoption not checked (NCCN not checked).",
  "acc": "—"
 },
 {
  "y": 2024,
  "n": "EVIDENCE meta-analysis (Landgren)",
  "s": "risk",
  "ph": "Meta-analysis",
  "d": "Randomized phase 2–3 trials with MRD at 12 ± 3 months, analyzed following FDA guidance on MRD as an endpoint",
  "ep": "Trial-level and patient-level association of 12-month MRD negativity with PFS",
  "r": "Trial level: R² 0.67 (weighted least squares; 95% CI 0.43–0.91) and 0.84 (copula); patient level: global OR 4.02 (2.57–5.46). Relapsed disease (4 trials): patient-level OR 7.67",
  "N": "4,907 (8 newly diagnosed trials)",
  "hr": "n/a",
  "fu": "n/a",
  "c": "Blood 2024;144:359",
  "p": 38768337,
  "b": "Earlier meta-analyses (Munshi) showed patient-level prognostic value; this tested whether a treatment effect on MRD predicts a treatment effect on PFS.",
  "i": "Concluded that MRD is reasonably likely to predict PFS benefit, supporting MRD as an accelerated-approval endpoint.",
  "q": "Does 12-month MRD predict OS? Does the relationship hold for new drug classes such as T-cell engagers?",
  "cm": [
   [
    39052265,
    "Costa LJ, Blood 2024",
    "MRD accelerating myeloma drug development"
   ]
  ],
  "reg": "Presented by its lead author at the FDA advisory committee (ODAC) meeting of April 12, 2024, alongside analyses by the FDA and i2TEAMM; ODAC voted 12–0 that the data support MRD as an accelerated-approval endpoint in myeloma (confirmed October 31, 2026).",
  "gl": "Guideline placement not checked (NCCN not checked).",
  "acc": "—"
 },
 {
  "y": 2017,
  "n": "t(11;14) and venetoclax (Kumar)",
  "s": "risk",
  "ph": "Predictive biomarker (phase 1)",
  "d": "Venetoclax monotherapy, up to 1,200 mg daily, in relapsed or refractory myeloma (median 5 prior therapies; 46% with t(11;14))",
  "ep": "Safety; response by t(11;14) status",
  "r": "ORR 21% overall (14 of 66); 12 of the 14 responses were in patients with t(11;14), in whom ORR was 40% and ≥VGPR 27%; response correlated with higher BCL2:BCL2L1 and BCL2:MCL1 expression ratios",
  "N": "66",
  "hr": "n/a (single arm)",
  "fu": "not reported in abstract",
  "c": "Blood 2017;130:2401",
  "p": 29018077,
  "b": "Laboratory work had shown that myeloma cells with t(11;14) depend on BCL-2 rather than MCL-1 or BCL-XL.",
  "i": "Made t(11;14) the first genetic marker used to select patients for a myeloma drug, and the basis for biomarker-selected venetoclax trials.",
  "q": "CANOVA, restricted to t(11;14), did not meet its PFS endpoint. Is BCL2 expression a better selector than the translocation, and which partner drug is needed?",
  "cm": [
   [
    29191974,
    "Kortüm KM, Blood 2017",
    "First targeted therapy in multiple myeloma"
   ]
  ],
  "reg": "No approval; venetoclax is not approved for myeloma.",
  "gl": "Guideline placement not checked (NCCN not checked).",
  "acc": "t(11;14) is detected by routine FISH."
 },
 {
  "y": 2016,
  "n": "Early relapse as functional high risk (Majithia)",
  "s": "risk",
  "ph": "Retrospective cohort",
  "d": "511 consecutive patients treated with novel agents at one center (2006–2014); early relapse defined as relapse within 12 months of starting treatment",
  "ep": "OS",
  "r": "Early relapse in 16.0% (82 patients): median OS 21.0 mo vs not reached with later relapse, regardless of depth of first response; relapse within 12 mo of early transplant: median OS 23.1 vs 122.2 mo",
  "N": "511",
  "hr": "not reported in abstract",
  "fu": "not reported in abstract",
  "c": "Leukemia 2016;30:2208",
  "p": 27211270,
  "extra": [
   "Myeloma XI analysis (Bygrave, Br J Haematol 2021)",
   32524584
  ],
  "b": "Staging and cytogenetics at diagnosis miss many patients who do badly.",
  "i": "Showed that early relapse marks poor prognosis in the novel-agent era, a group often called functional high risk.",
  "q": "Which definition (12 or 18 months, from the start of treatment or from transplant)? Should these patients move directly to T-cell redirecting therapy?",
  "cm": [],
  "reg": "—",
  "gl": "Guideline placement not checked (NCCN not checked).",
  "acc": "—"
 }
]
FT_NEW = {
 "IMS/IMWG high-risk consensus (Avet-Loiseau)": [
  "pmc",
  "PMC13445576"
 ],
 "IMWG response and MRD criteria (Kumar)": [
  "doi",
  "10.1016/S1470-2045(16)30206-6"
 ],
 "EVIDENCE meta-analysis (Landgren)": [
  "pmc",
  "PMC11418064"
 ],
 "t(11;14) and venetoclax (Kumar)": [
  "doi",
  "10.1182/blood-2017-06-788786"
 ],
 "Early relapse as functional high risk (Majithia)": [
  "pmc",
  "PMC5541860"
 ]
}
TOX_NEW = {
 "IMS/IMWG high-risk consensus (Avet-Loiseau)": "Not applicable (consensus definition)",
 "IMWG response and MRD criteria (Kumar)": "Not applicable (consensus definition)",
 "EVIDENCE meta-analysis (Landgren)": "Not applicable (meta-analysis)",
 "t(11;14) and venetoclax (Kumar)": "Mostly mild gastrointestinal events (nausea 47%, diarrhea 36%); grade 3–4 thrombocytopenia 32%, neutropenia 27%, anemia 23%",
 "Early relapse as functional high risk (Majithia)": "Not applicable (prognostic study)"
}
CORE_ADD = []  # Andres chooses core trials
EXTRA_OLD = {}
PROG = {
 "Early relapse as functional high risk (Majithia)": {
  "pt": "model",
  "pk": "Prognostic",
  "sh": "Early relapse",
  "val": "Single-center series, confirmed in the Myeloma XI trial: relapse within 12 months of transplant gave median OS 26 vs 91 months despite equal access to later therapies (Bygrave 2021)."
 },
 "IMS/IMWG high-risk consensus (Avet-Loiseau)": {
  "pt": "bio",
  "pk": "Consensus definition",
  "sh": "High risk",
  "val": "Consensus of IMS and IMWG; updates the 2016 IMWG definition (Sonneveld, Blood 2016)."
 },
 "t(11;14) and venetoclax (Kumar)": {
  "pt": "bio",
  "pk": "Predictive",
  "sh": "t(11;14)",
  "val": "Phase 1 finding. In the phase 3 CANOVA trial, limited to t(11;14)-positive disease, venetoclax-dexamethasone did not significantly improve PFS over pomalidomide-dexamethasone (HR 0.823), with ORR 62% vs 35%."
 },
 "IMWG response and MRD criteria (Kumar)": {
  "pt": "resp",
  "pk": "Consensus definition",
  "sh": "MRD",
  "val": "Consensus definition. Minimum sensitivity 1 in 10⁵ nucleated cells by flow or sequencing; sustained negativity requires confirmation at least 1 year apart, with the method annotated (full paper)."
 },
 "EVIDENCE meta-analysis (Landgren)": {
  "pt": "resp",
  "pk": "Surrogate endpoint",
  "sh": "EVIDENCE",
  "val": "The trial-level analysis used 8 randomized trials in newly diagnosed myeloma; for relapsed disease (4 trials) only the patient-level association was reported (OR 7.67)."
 }
}
PROGMAP = {
 "CANOVA (Popat)": [
  [
   "t(11;14) and venetoclax (Kumar)",
   "Eligibility (t(11;14)-positive disease only)"
  ]
 ],
 "EXCALIBER-RRMM (Lonial)": [
  [
   "IMWG response and MRD criteria (Kumar)",
   "Dual primary endpoint (MRD-negative complete response)"
  ]
 ]
}
GLOSS = {
 "C-index": "Concordance index (how well a model ranks patients by risk; 0.5 = chance, 1 = perfect)",
 "C-statistic": "Concordance statistic (same meaning as C-index)",
 "CI": "Confidence interval",
 "GEP": "Gene expression profiling",
 "IRMMa": "Individualized risk model for myeloma",
 "MAPK": "Mitogen-activated protein kinase",
 "APOBEC": "A family of DNA-editing enzymes whose activity leaves a characteristic mutation pattern",
 "PCL": "Plasma cell leukemia",
 "sBCMA": "Soluble B-cell maturation antigen",
 "TNFRSF17": "The gene that encodes BCMA",
 "PET-CT": "Positron emission tomography-computed tomography",
 "WHO": "World Health Organization",
 "ODAC": "Oncologic Drugs Advisory Committee (FDA)"
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
    h = h[:i] + "// Prognosis tab data. PROG: kind, type, validation and chip label for each prognostic entry; PROGMAP: trial -> prognostic entries used in its design.\n" + line + h[i:]
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
