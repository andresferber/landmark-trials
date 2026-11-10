"""Prognosis tab for smoldering myeloma (preview, Nov 9, 2026; not live until Andres approves).
No new T entries: PROG records are attached to the existing Definition & risk entries; PROGMAP links QuiRedex to the
models that defined its eligibility. Every statement comes from the verified cards.
Usage: python3 smm_entries.py smm.html   (rerunnable)"""
import sys, json, re

page = sys.argv[1]
h = open(page, encoding="utf-8").read()
J = lambda o: json.dumps(o, ensure_ascii=False)

NEW = []
FT_NEW = {}
TOX_NEW = {}
CORE_ADD = []  # Andres chooses core trials
EXTRA_OLD = {}
PROG = {
 "Mayo natural history (Kyle)": {
  "pt": "model",
  "pk": "Prognostic",
  "sh": "Mayo 2007",
  "val": "Single-center cohort (276 patients). Its groups by marrow plasma cells and M-protein were the Mayo criteria used, with the PETHEMA criteria, to define high risk in QuiRedex."
 },
 "PETHEMA flow-cytometry risk (Pérez-Persona)": {
  "pt": "model",
  "pk": "Prognostic",
  "sh": "PETHEMA",
  "val": "One prospective cohort (93 patients with smoldering myeloma, 407 with MGUS); used, with the Mayo criteria, to define high risk in QuiRedex."
 },
 "Free light chain ratio (Dispenzieri)": {
  "pt": "bio",
  "pk": "Prognostic",
  "sh": "FLC ratio",
  "val": "One cohort (273 Mayo patients). The involved to uninvolved FLC ratio later entered the Mayo 20/2/20 and IMWG 2/20/20 models at a cutoff of 20, and a ratio of 100 or more became a myeloma-defining event (IMWG 2014)."
 },
 "IMWG updated criteria (Rajkumar)": {
  "pt": "bio",
  "pk": "Consensus definition",
  "sh": "SLiM-CRAB",
  "val": "IMWG consensus. The three biomarkers were chosen because they were associated with near-inevitable development of CRAB features (per abstract)."
 },
 "Mayo 20/2/20 model (Lakshman)": {
  "pt": "model",
  "pk": "Prognostic",
  "sh": "20/2/20",
  "val": "Single-center cohort (421 patients); the same three factors were confirmed in the IMWG international cohort of 1,996 patients (Mateos 2020)."
 },
 "IMWG 2/20/20 risk model (Mateos)": {
  "pt": "model",
  "pk": "Prognostic",
  "sh": "IMWG 2/20/20",
  "val": "International multicenter cohort (1,996 patients). Adding cytogenetic abnormalities gave four groups with 6% to 63% progression at 2 years."
 },
 "PANGEA-SMM dynamic risk (Chabrun)": {
  "pt": "model",
  "pk": "Prognostic",
  "sh": "PANGEA-SMM",
  "val": "Trained and validated in 2,344 patients from seven international centers; C-statistic 0.79, higher than the 20/2/20 and IMWG models (per abstract). Published in 2026; not yet in a consensus or guideline."
 }
}
PROGMAP = {
 "QuiRedex (Mateos)": [
  [
   "Mayo natural history (Kyle)",
   "Eligibility (high risk by Mayo and/or PETHEMA criteria)"
  ],
  [
   "PETHEMA flow-cytometry risk (Pérez-Persona)",
   "Eligibility (high risk by Mayo and/or PETHEMA criteria)"
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
