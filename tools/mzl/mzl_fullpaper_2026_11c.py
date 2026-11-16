"""Marginal zone lymphomas: values completed from the two letters Andres supplied as PDFs on Nov 15, 2026
(Kiesewetter, Blood 2017;129:383, AGMT MALT-2; Copie-Bergman, Gut 2003;52:1656, GELA grading). Edits the master page in place;
rerunnable (each edit checks its old text)."""
import io, json, re, sys
p = sys.argv[1]; s = io.open(p, encoding='utf-8').read()
J = lambda v: json.dumps(v, ensure_ascii=False)
def line(n):
    m = re.search(r'^\{y:\d+,n:' + re.escape(J(n)) + r'.*$', s, re.M); assert m, n; return m
def setf(n, f, v):
    global s
    m = line(n); e = m.group(0)
    fm = re.search(r',%s:("(?:[^"\\]|\\.)*"|\[[^\]]*\]|\d+)' % f, e); assert fm, (n, f)
    new = e[:fm.start(1)] + J(v) + e[fm.end(1):]
    s = s[:m.start()] + new + s[m.end():]
def setj(name, key, val):
    global s
    m = re.search(r'\nconst %s = (\{.*?\});\n' % name, s); o = json.loads(m.group(1)); o[key] = val
    s = s[:m.start(1)] + J(o) + s[m.end(1):]

n = "AGMT MALT-2, lenalidomide-rituximab (Kiesewetter)"
setf(n, 'sub', "MALT lymphoma: stomach 14 (30%) and extragastric 32 (70%) of 46 evaluable (ocular adnexa 28%, lung 11%, parotid 7%, other 13%, multiple extranodal sites 11%); 39% stage III-IV; 11 (24%) had prior systemic treatment, 9 of them with rituximab (full paper)")
setf(n, 'r', "Letter without an abstract; values from the full letter (full paper). Overall response 80% (37 of 46; 95% CI 69-92): complete 54% (25 of 46; 95% CI 40-69), partial 26% (12), stable disease 17% (8); disease control 97%. One gastric patient progressed at the first restaging and was salvaged with bendamustine-rituximab. Median time to best response 3.6 mo (interquartile range 2.8-5.8); 11 patients (24%) improved between the first and second restaging and 3 more between cycles 6 and 8. Response did not differ by sex, site, stage or prior treatment; a trend to worse response with elevated LDH (P=.079), and none of these patients reached complete response. 3 relapses, at 5.0-8.8 mo after response; progression-free survival 91% at 27 mo")
setf(n, 'fu', "27.0 mo (range 13.2-36.3) (full paper)")
setj('TOX', n, "Grade 3-4 neutropenia 18.8% (grade 3 in 7 patients, grade 4 in 2 of 48); no grade 4 nonhematologic events. Rash 46% (grade 3 in 3), musculoskeletal pain 42% (grade 3 in 2), fatigue 33%, cough or respiratory infection 33% (grade 3 in 3), diarrhea 23% (grade 3 in 1), vertigo 23% (grade 3 in 2), mild infusion reactions 38% (full paper). Lenalidomide dose reduced in 34.8%; no second malignancies (meeting abstract)")

n = "GELA histological grading (Copie-Bergman)"
setf(n, 'd', "Proposal of a histological grading system for gastric biopsies taken after treatment, read on haematoxylin-eosin sections from three features (lymphoid infiltrate, lymphoepithelial lesions, stromal changes); reproducibility tested by 7 pathologists blind to follow-up on 45 biopsy sets from 10 GELA trial patients (original letter); validated later by the IELSG with 7 pathologists from four European countries reading 154 biopsy sets from 21 patients (full paper)")
setf(n, 'r', "Letter without an abstract; values from the full letter (full paper). Four categories: complete histological remission, probable minimal residual disease (pMRD), responding residual disease (rRD) and no change. Reproducibility in the original test: weighted kappa above 0.84 among 7 observers (very good agreement). The authors call for testing in larger series. Later IELSG validation: overall concordance 83% (kappa 0.64); most disagreements were between complete remission and pMRD, and with those two combined concordance was 89% (kappa 0.83)")
setf(n, 'N', "10 patients, 45 biopsy sets (original test); 21 patients, 154 biopsy sets (validation)")
setf(n, 'fu', "mean 19 mo after H. pylori eradication in the original test set, 3-6 sequential biopsy sets per patient (full paper)")
setf(n, 'q', "The original reproducibility test was small (10 patients, one trial). Complete remission and probable minimal residual disease are hard to tell apart, though both are managed in the same way.")

old = 'AGMT MALT-2 was published as a letter without an abstract; its figures come from the final results presented at ASH 2015 (abstract 3973) and the ClinicalTrials.gov results record.'
new = 'AGMT MALT-2 and the GELA grading proposal were published as letters without an abstract; their figures were checked against the full letters (November 15, 2026), except lenalidomide dose reductions and second malignancies in AGMT MALT-2, which come from the ASH 2015 abstract (3973).'
assert old in s or new in s
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8').write(s)
