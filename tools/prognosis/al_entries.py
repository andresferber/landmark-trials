"""Prognosis tab for AL amyloidosis (added Nov 15, 2026 at Andres's request).
No new T entries: PROG records are attached to the existing "Staging, prognosis & response criteria" entries; PROGMAP links
trials to the staging or response measures that defined their eligibility, stratification or primary end point (each link
confirmed from the trial's abstract or verified card). Every statement comes from the verified cards or the abstracts named.
Markers to watch: tools/prognosis/al_markers.json (AL only, not shared with the myeloma topics).
Usage: python3 al_entries.py al.html   (rerunnable), then install_progtab.py tools/prognosis/al_markers.json al.html"""
import sys, json, re

page = sys.argv[1]
h = open(page, encoding="utf-8").read()
J = lambda o: json.dumps(o, ensure_ascii=False)

NEW = []
FT_NEW = {}
TOX_NEW = {}
CORE_ADD = []  # Andres chooses core trials
EXTRA_OLD = {}
M04, M12, IIIB = "Mayo 2004 cardiac staging (Dispenzieri)", "Revised Mayo 2012 staging (Kumar)", "European stage IIIb, NT-proBNP >8500 ng/L (Wechalekar)"
RESP = "Hematologic and cardiac response criteria (Palladini)"
PROG = {
 M04: {"pt": "model", "pk": "Prognostic", "sh": "Mayo 2004",
  "val": "Derived in 242 Mayo Clinic patients. Its stages became the basis of trial eligibility and stratification, and with the European modification (stage IIIb, NT-proBNP >8500 ng/L) they organize the first-line recommendations of the EHA-ISA 2023 guideline."},
 "Consensus organ involvement and response criteria (Gertz)": {"pt": "resp", "pk": "Consensus definition", "sh": "Consensus 2005",
  "val": "Consensus of the 10th International Symposium on Amyloid and Amyloidosis (2004). Its organ involvement definitions are still used for trial eligibility; its hematologic and cardiac response definitions were replaced by the criteria validated in 2012."},
 M12: {"pt": "model", "pk": "Prognostic", "sh": "Mayo 2012",
  "val": "Derived in 810 Mayo Clinic patients and tested in 303 transplanted patients and 103 patients in clinical trials. Used for long-term prognosis and in transplant series; the EHA-ISA 2023 guideline organizes first-line therapy by the cardiac stages instead."},
 RESP: {"pt": "resp", "pk": "Surrogate endpoint", "sh": "Response criteria",
  "val": "Derived in 816 patients from seven centres and validated in 374 patients at Pavia. Hematologic complete response was the primary end point of ANDROMEDA, whose result supported the accelerated FDA approval of daratumumab-hyaluronidase with VCd (January 2021); traditional approval followed in November 2025 on MOD-PFS and OS."},
 IIIB: {"pt": "model", "pk": "Prognostic", "sh": "Stage IIIb",
  "val": "Multicentre cohort of 346 patients from four countries. Adopted in the EHA-ISA 2023 guideline, which gives stage IIIb its own recommendations, and used to exclude or select patients in ANDROMEDA, BMDex vs MDex, EMN22 and CARES."},
 "Marrow plasma cells >10% (Kourelis)": {"pt": "bio", "pk": "Prognostic", "sh": "Marrow PCs",
  "val": "Single-centre cohort of 1,255 patients. A later Mayo Clinic series of 1,574 patients found only 20% or more marrow plasma cells independently prognostic (Muchtar, Leukemia 2020). Marrow plasma cell burden is not part of the staging systems."},
 "Renal staging and response (Palladini)": {"pt": "model", "pk": "Prognostic", "sh": "Renal stage",
  "val": "Derived at Pavia (461 patients) and validated at Heidelberg (271). Its renal response and progression criteria are the standard renal end points in trials."},
 "t(11;14) and bortezomib (Bochtler)": {"pt": "bio", "pk": "Predictive", "sh": "t(11;14)",
  "val": "Heidelberg cohort with a small validation group (32 patients treated with CyBorD). The EHA-ISA 2023 guideline notes that CyBorD may be less effective with t(11;14) and lists venetoclax as an option at relapse with t(11;14); in the venetoclax series on this page, response was 81% with t(11;14) vs 40% without (Premkumar 2021). No randomized trial has assigned treatment by t(11;14)."},
 "Boston University BNP staging (Lilleness)": {"pt": "model", "pk": "Prognostic", "sh": "BU staging",
  "val": "Derived and tested in two Boston University cohorts. It reproduces the Mayo 2004 stages with BNP (agreement κ 0.854), for centres that do not measure NT-proBNP."},
 "MRD by next-generation flow (Palladini)": {"pt": "resp", "pk": "Prognostic; surrogate candidate", "sh": "MRD",
  "val": "Pavia cohort of 92 complete responders. A Boston study with multiparametric flow (65 complete responders) also found a residual clone in 55%, with more renal responses without MRD (88% vs 64%, P=0.06) (Staron, Blood Adv 2020). The EHA-ISA 2023 guideline does not yet propose MRD negativity as the goal of therapy for all patients."},
 "Graded cardiac response criteria (Muchtar)": {"pt": "resp", "pk": "Prognostic", "sh": "Cardiac response",
  "val": "Multicentre validation in 651 patients; four levels predicted survival better than two from 12 months. Now reported in trials; not yet in the EHA-ISA 2023 guideline."},
 "Extracellular volume by cardiac MRI (Porcari)": {"pt": "bio", "pk": "Prognostic", "sh": "ECV",
  "val": "Single-centre cohort of 560 patients (UK National Amyloidosis Centre). Response targets by ECV have not been tested prospectively and are not in guidelines. A small South Asian series (22 patients with ECV) also linked abnormal ECV to death (Pattnaik, Indian J Hematol Blood Transfus 2026)."},
 "AL-ISS with stage IIIC (Khwaja)": {"pt": "model", "pk": "Prognostic", "sh": "AL-ISS",
  "val": "Derived at the UK National Amyloidosis Centre (573 patients) and validated in 1,920 patients from six countries, 43% treated first-line with daratumumab (Harrell C 0.69). Too recent for guidelines."}
}
PROGMAP = {
 "ANDROMEDA (Kastritis)": [[RESP, "Primary end point (hematologic complete response)"], [IIIB, "Eligibility (stage IIIb excluded)"]],
 "BMDex vs MDex (Kastritis)": [[M04, "Stratification (cardiac stage)"], [IIIB, "Eligibility (stage IIIb excluded)"]],
 "EMN22, daratumumab in stage IIIb (Kastritis)": [[IIIB, "Eligibility (stage IIIb only)"]],
 "CARES, anselamimab (Wechalekar)": [[M04, "Eligibility (stage IIIa or IIIb)"], [IIIB, "Eligibility (stage IIIa or IIIb, European modification)"]],
 "Doxycycline with CyBorD (Shen)": [[M04, "Eligibility (stage II–III)"]]
}
GLOSS = {
 "Harrell C": "Concordance statistic (how well a model ranks patients by risk; 0.5 = chance, 1 = perfect)",
 "FLC-MS": "Free light chain mass spectrometry (MALDI-TOF-based detection of the monoclonal light chain)",
 "MALDI-TOF": "Matrix-assisted laser desorption/ionization time-of-flight (a mass spectrometry method)",
 "MASS-FIX": "Immunoenrichment followed by MALDI-TOF mass spectrometry to detect and type monoclonal proteins",
 "N-glycosylation": "Attachment of a sugar chain to an asparagine residue of a protein"
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
