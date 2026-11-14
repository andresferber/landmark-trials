"""Marginal zone lymphomas: values completed from full papers Andres supplied as PDFs on Nov 14, 2026
(ESMO 2020 guideline with its corrigendum; MALT2008-01 long-term letter; Kalpadakis Blood 2018 letter; IELSG-19 final report;
StiL NHL 1-2003; BRIGHT; FoRT long-term report; CHRONOS-3). Edits the master page in place; rerunnable (each edit checks its old text)."""
import io, json, re, sys
p = sys.argv[1]; s = io.open(p, encoding='utf-8').read()
J = lambda v: json.dumps(v, ensure_ascii=False)
def line(n):
    m = re.search(r'^\{y:\d+,n:' + re.escape(J(n)) + r'.*$', s, re.M); assert m, n; return m
def setf(n, f, v):
    global s
    m = line(n); e = m.group(0)
    fm = re.search(r',%s:("(?:[^"\\]|\\.)*"|\[[^\]]*\]|\d+)' % f, e)
    new = e[:fm.start(1)] + J(v) + e[fm.end(1):] if fm else e.replace(',b:', ',%s:%s,b:' % (f, J(v)), 1)
    s = s[:m.start()] + new + s[m.end():]
def getf(n, f):
    fm = re.search(r',%s:("(?:[^"\\]|\\.)*")' % f, line(n).group(0)); return json.loads(fm.group(1))
def setj(name, key, val):
    global s
    m = re.search(r'\nconst %s = (\{.*?\});\n' % name, s); o = json.loads(m.group(1)); o[key] = val
    s = s[:m.start(1)] + J(o) + s[m.end(1):]
def tox(n): return json.loads(re.search(r'\nconst TOX = (\{.*?\});\n', s).group(1)).get(n, '')

# MALT2008-01
n = "MALT2008-01 (Salar)"
setf(n, 'sub', "MALT lymphoma of any site and stage, including gastric disease after failed eradication and cutaneous disease after local therapy: stomach 33%, extragastric 57%, multifocal 10% of 57 evaluable; t(11;18) in 16% (full paper)")
setf(n, 'r', "2-year EFS 93% (95% CI 84-97); 4-year EFS 88% (95% CI 74-95); only 25% of patients needed more than four cycles. Long-term report (full paper): CR or unconfirmed CR 75% after 3 cycles (gastric 90% vs non-gastric 62%) and 98% at the end of treatment; 7-year EFS 87.7% (95% CI 76.0-94.0), gastric 89.5% and non-gastric 84.4% (P=.64); 7-year PFS 92.8%, not different by site, stage, number of cycles or t(11;18); 5 relapses, 3 with transformation to diffuse large B-cell lymphoma; MALT-IPI separated 7-year EFS (96%, 88% and 50%)")
setf(n, 'fu', "43 mo; 82 mo in the long-term report (full paper)")
setf(n, 'gl', "Bendamustine-rituximab is listed among systemic options for MALT lymphoma [III, A] (ESMO 2020; NCCN not checked).")
setj('TOX', n, "Grade 3-4 lymphopenia 33%, neutropenia 20%, leukopenia 5%; febrile neutropenia 5%; grade 3-4 infections 7%. Long-term report (full paper): grade 3-4 adverse events in 60% during treatment, mostly hematologic; 3 late opportunistic infections (herpes zoster, cytomegalovirus, Nocardia); no myelodysplasia or acute leukemia; other cancers in 3 patients and nonmelanoma skin cancer in 3")

# Kalpadakis
n = "Rituximab monotherapy (Kalpadakis)"
setf(n, 'r', "ORR to rituximab 95% two months after induction (complete 45%, unconfirmed complete 26%, partial 24%); median time to hematological response 2 weeks. 85% of splenectomized patients responded. 5-year overall survival 92% vs 77% (P=.09) and PFS 73% vs 58% (P=.06) for rituximab vs splenectomy. With maintenance, 5-year PFS 84% vs 36% without (P<.0001). Long-term report on 108 rituximab-treated patients (Blood 2018, full paper): ORR 92% after induction (complete 44%, unconfirmed complete 21%); 5- and 10-year freedom from progression 71% and 64%, overall survival 93% and 85%; in responders, 5-year freedom from progression 79% with maintenance vs 52% without (P=.0006; HR 0.18 in multivariable analysis), with no difference in overall survival and none between 1 and 2 years of maintenance")
setf(n, 'N', "85 (58 rituximab; 27 splenectomy); 108 in the long-term report")
setf(n, 'fu', "not reported in abstract; 57 mo in the long-term report (full paper)")
setf(n, 'gl', "Rituximab alone is the preferred initial therapy [III, A]; splenectomy may be considered when rituximab is not indicated or ineffective [IV, B]; rituximab maintenance is not recommended as routine (ESMO 2020; NCCN not checked).")
setj('TOX', n, "Described as well tolerated; rates not reported in abstract. Long-term report: toxicity described as minimal, without rates (full paper)")

# IELSG-19
n = "IELSG-19 (Zucca)"
setf(n, 'sub', "MALT lymphoma of any site, not responding to or not suitable for local therapy: gastric 171 (42.6%) and non-gastric 230 of 401 (lung 42, orbit 38, salivary gland 25, intestine 25, skin 23) (full paper)")
setf(n, 'r', getf(n, 'r') + ". Complete response higher in gastric than non-gastric disease (72% vs 61%; P=.015), and EFS better with the combination in both (full paper)")
setf(n, 'gl', "Rituximab-chlorambucil is the systemic option with the strongest evidence [I, A] (ESMO 2020; NCCN not checked).")

# StiL NHL 1-2003
n = "StiL NHL 1-2003 (Rummel)"
setf(n, 'sub', "Indolent and mantle cell lymphomas, stage III-IV, untreated; marginal zone lymphoma 67 of 514 (37 bendamustine-rituximab, 30 R-CHOP; subtypes not reported) (full paper)")
setf(n, 'r', "All histologies: median PFS 69.5 vs 31.2 months (HR 0.58, 95% CI 0.44-0.74). Marginal zone lymphoma (67; full paper): median PFS 57.2 vs 47.2 months (HR 0.70, 95% CI 0.34-1.43; P=.32), not significantly different")
setf(n, 'gl', "Bendamustine-rituximab is listed among systemic options for MALT lymphoma [III, A] and nodal disease [IV, B] (ESMO 2020; NCCN not checked).")

# BRIGHT
n = "BRIGHT (Flinn)"
setf(n, 'sub', "Indolent non-Hodgkin lymphoma or mantle cell lymphoma, untreated; splenic, MALT and nodal marginal zone lymphoma eligible: marginal zone 46 of 447 (28 bendamustine-rituximab, 18 R-CHOP or R-CVP; subtype numbers not reported) (full paper)")
setf(n, 'r', "All histologies: complete response 31% vs 25% (non-inferior); ORR 97% vs 91%. 5-year follow-up: PFS 65.5% vs 55.8% (HR 0.61, 95% CI 0.45-0.85); no difference in overall survival; more second malignancies with bendamustine-rituximab. Marginal zone lymphoma (independent review, evaluable patients; full paper): complete response 20% (5 of 25) vs 24% (4 of 17); ORR 92% vs 71%; PFS for marginal zone lymphoma alone not reported")
setf(n, 'gl', "Bendamustine-rituximab is listed among systemic options for MALT lymphoma [III, A] and nodal disease [IV, B] (ESMO 2020; NCCN not checked).")

# FoRT
n = "FoRT (Hoskin)"
setf(n, 'sub', "Follicular or marginal zone lymphoma needing local radiotherapy, radical or palliative; marginal zone lymphoma 84 of 614 sites as recorded at randomization (41 at 24 Gy, 43 at 4 Gy), 46 confirmed on central review; subtypes not reported (long-term report, full paper)")
setf(n, 'r', "4 Gy was not non-inferior: local progression at 21 sites after 24 Gy vs 70 after 4 Gy (HR 3.42, 95% CI 2.09-5.55). Long-term: 2-year local progression-free rate 94.1% vs 79.8%, and 5-year 89.9% vs 70.4% (HR 3.46, 95% CI 2.25-5.33). Marginal zone sites (post hoc; full paper): local progression at 0 of 41 sites after 24 Gy vs 6 of 43 after 4 Gy; 5-year local progression-free rate 100% vs 88.0% (P=.015)")
setf(n, 'gl', "24 Gy remains the standard dose for localized MALT lymphoma [II, A]; 4 Gy may be considered in the elderly, for palliation or at critical sites (ESMO 2020; NCCN not checked).")

# CHRONOS-3
n = "CHRONOS-3 (Matasar)"
setf(n, 'sub', "Relapsed indolent B-cell lymphoma, stratified by histology; marginal zone lymphoma 95 of 458 (nodal 37, extranodal 35, splenic 23; 66 copanlisib-rituximab, 29 placebo-rituximab) (full paper)")
setf(n, 'r', "All histologies: median PFS 21.5 vs 13.8 months (HR 0.52, 95% CI 0.39-0.69). Marginal zone lymphoma (95; full paper): median PFS 22.1 vs 11.5 months (HR 0.48, 95% CI 0.25-0.92)")

# ESMO
n = "ESMO guidelines (Zucca)"
setf(n, 'r', "Main recommendations (full paper, with its corrigendum): gastric MALT lymphoma: H. pylori eradication for all patients, whatever the stage [II, A]; FISH for t(11;18) may identify patients unlikely to respond [III, B]; watch and wait for persistent stable residual disease [IV, C]. Localized MALT lymphoma: involved-site radiotherapy is preferred, 24 Gy standard (24-30 Gy to the stomach), 4 Gy possible in the elderly, for palliation or at critical sites; antibiotics may be considered for ocular adnexal disease. Systemic options for MALT lymphoma: rituximab-chlorambucil [I, A], bendamustine-rituximab [III, A], rituximab alone [III, B], lenalidomide-rituximab [III, C], R-CHOP for transformation; no published data support rituximab maintenance [III, D]. Splenic: watch and wait if asymptomatic; rituximab alone is the preferred initial therapy [III, A]; splenectomy in selected cases [IV, B]. Nodal: treat on the principles used for follicular lymphoma [IV, B]. HCV-associated disease: antiviral therapy first [IV, B]. Prognostic scores (HPLL, MALT-IPI) should be applied to estimate clinical behaviour [III-IV, C]; BTK and PI3K inhibitors may become options after short remissions [III, B]")
setf(n, 'gl', "This is the guideline; a corrigendum (t(11;18)(q21;q21), not p21) is part of the record.")

# Guideline rows: statements checked against the ESMO 2020 text
G = {
 "t(11;18) and response to eradication (Liu)": "FISH for t(11;18) may be useful to identify gastric MALT lymphoma unlikely to respond to antibiotics [III, B] (ESMO 2020; NCCN not checked).",
 "GELA histological grading (Copie-Bergman)": "Recommended for post-treatment gastric biopsies as a reproducible method [IV, B] (ESMO 2020) and in the EGILS consensus report; NCCN not checked.",
 "Long-term follow-up after eradication (Wündisch)": "H. pylori eradication for all patients with gastric MALT lymphoma, whatever the stage [II, A] (ESMO 2020; NCCN not checked).",
 "Rituximab in gastric MALT lymphoma (Martinelli)": "Rituximab alone [III, B], or with chemotherapy, for disease that needs systemic treatment (ESMO 2020; NCCN not checked).",
 "Antibiotics in H. pylori-negative disease (Raderer)": "A trial of eradication therapy may still be worthwhile in H. pylori-negative cases [IV, C], with specific treatment, usually radiotherapy, if there is no regression after 3-6 months (ESMO 2020; NCCN not checked).",
 "Watch and wait for histological residuals (Fischbach)": "Watch and wait appears safe for persistent but stable residual disease [IV, C] (ESMO 2020; EGILS consensus); NCCN not checked.",
 "LY03 (Hancock)": "Consolidation chlorambucil is not beneficial after response to eradication [II, D] (ESMO 2020; NCCN not checked).",
 "Pooled analysis of eradication (Zullo)": "Supports eradication as first treatment and long-term endoscopic follow-up, as recommended (ESMO 2020; NCCN not checked).",
 "EGILS consensus (Ruskoné-Fourmestraux)": "This is the guideline; the ESMO 2020 guideline is the later reference and endorses the GELA grading it recommends (NCCN not checked).",
 "Japanese multicenter cohort (Nakamura)": "Supports eradication first and observation of non-progressive residual disease (ESMO 2020; NCCN not checked).",
 "Radiotherapy, IELSG series (Wirth)": "Involved-site radiotherapy is the preferred treatment for localized disease [II-IV, A-B], including gastric disease that does not respond to antibiotics (ESMO 2020; NCCN not checked).",
 "HELYX I and II (Schmelz)": "24-30 Gy to the stomach and perigastric nodes over 3-4 weeks [II-IV, A-B] (ESMO 2020; NCCN not checked).",
 "IELSG non-gastric series (Zucca)": "Background for site-specific management (ESMO 2020; NCCN not checked).",
 "IELSG-27 (Ferreri)": "Antibiotic therapy may be considered as first treatment of ocular adnexal MALT lymphoma that does not need urgent treatment (ESMO 2020; NCCN not checked).",
 "TROG 05.02/ALLG NHL15 (MacManus)": "Involved-site radiotherapy, 24 Gy as the standard dose, for localized non-gastric disease (ESMO 2020; NCCN not checked).",
 "Rituximab, IELSG phase 2 (Conconi)": "Rituximab alone can be considered when the toxicity of chemotherapy is a concern [III, B] (ESMO 2020; NCCN not checked).",
 "Radiotherapy, Princess Margaret series (Goda)": "Supports radiotherapy as the preferred treatment for localized MALT lymphoma (ESMO 2020; NCCN not checked).",
 "Radiotherapy, Memorial Sloan Kettering series (Teckie)": "Supports radiotherapy for stage IE-IIE disease (ESMO 2020; NCCN not checked).",
 "ILROG radiotherapy guidelines (Yahalom)": "The radiotherapy guideline cited by ESMO 2020 for treatment volumes at each extranodal site (NCCN not checked).",
 "MALT-IPI (Thieblemont)": "Prognostic scores, including MALT-IPI, should be applied to estimate clinical behaviour [III-IV, C], not to choose treatment (ESMO 2020; NCCN not checked).",
 "AGMT MALT-2, lenalidomide-rituximab (Kiesewetter)": "Lenalidomide-rituximab is listed among systemic options for MALT lymphoma [III, C], citing this trial (ESMO 2020; NCCN not checked).",
 "Two-institution series (Starr)": "Nodal disease is treated on the principles used for follicular lymphoma [IV, B] (ESMO 2020; NCCN not checked).",
 "Memorial Sloan Kettering series (Stuver)": "Watch and wait may be followed in nodal disease with low tumour burden and no symptoms (ESMO 2020; NCCN not checked).",
 "Antiviral therapy in HCV-associated disease (Hermine)": "Antiviral therapy should be considered first in HCV-positive patients who do not need immediate treatment [IV, B] (ESMO 2020; NCCN not checked).",
 "IIL prognostic score (Arcaini)": "One of the prognostic models described for splenic disease (ESMO 2020; NCCN not checked).",
 "Rituximab-based treatment, MD Anderson series (Tsimberidou)": "Rituximab alone is the preferred initial therapy of splenic disease [III, A] (ESMO 2020; NCCN not checked).",
 "Rituximab vs other treatment, two-center series (Else)": "Rituximab alone is the preferred initial therapy of splenic disease [III, A] (ESMO 2020; NCCN not checked).",
 "Diagnostic and treatment guidelines (Matutes)": "These criteria are those used by later guidelines and trials (ESMO 2020; NCCN not checked).",
 "HPLL score (Montalbán)": "Cited for risk stratification of splenic disease [IV, C] (ESMO 2020; NCCN not checked).",
 "Splenectomy, 100 patients (Lenglet)": "Splenectomy may be considered in selected cases, when rituximab is not indicated or ineffective [IV, B], and may be needed when the diagnosis is uncertain (ESMO 2020; NCCN not checked).",
 "BRISMA/IELSG36 (Iannitto)": "Chemoimmunotherapy is indicated for fit patients with symptomatic disseminated disease, constitutional symptoms or signs of transformation [III, B] (ESMO 2020; NCCN not checked).",
 "Histologic transformation (Conconi)": "PET should be considered when transformation is suspected, to guide biopsy [IV, B]; proven transformation is treated as diffuse large B-cell lymphoma [II, A] (ESMO 2020; NCCN not checked).",
 "E4402 RESORT, non-follicular cohort (Williams)": "Rituximab maintenance is controversial and not supported by published data in MALT lymphoma [III, D], and optional in nodal disease (ESMO 2020; NCCN not checked).",
 "Direct-acting antivirals in HCV-associated lymphoma (Arcaini)": "Antiviral therapy first in HCV-associated marginal zone lymphoma that does not need immediate treatment [IV, B] (ESMO 2020; NCCN not checked).",
 "POD24 in the NF10 registry (Luminari)": "Not addressed by the ESMO 2020 guideline; NCCN not checked.",
}
for n, v in G.items():
    old = getf(n, 'gl'); assert 'not checked' in old, n; setf(n, 'gl', v)
left = re.findall(r'ESMO 2020 guideline full text and NCCN not checked', s); print('unchecked left:', len(left))
for m in re.finditer(r'^\{y:\d+,n:"([^"]*)".*ESMO 2020 guideline full text', s, re.M): print('  left:', m.group(1))
old = 'efer to the ESMO 2020 guideline, whose full text could not be read for this page, and are marked "not checked"'
if old in s: s = s.replace(old, 'efer to the ESMO 2020 guideline (with its corrigendum), checked against its full text on November 14, 2026')
io.open(p, 'w', encoding='utf-8').write(s)
