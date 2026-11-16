"""Values completed from four full papers Andres supplied as PDFs on Nov 15-16, 2026 (values marked "(full paper)"):
relapsed DLBCL (BELINDA), AL amyloidosis (VITAL, CARES), Waldenstrom (Treon ibrutinib, previously treated).
Usage: python3 fullpaper_2026_11_16.py <key> <page>. Rerunnable: each edit sets a value, never appends twice."""
import io, json, re, sys
key, p = sys.argv[1], sys.argv[2]
s = io.open(p, encoding='utf-8').read()
J = lambda v: json.dumps(v, ensure_ascii=False)
def line(n):
    m = re.search(r'^\{y:\d+,n:' + re.escape(J(n)) + r'.*?(?=^\{y:\d+,n:|^\]\s*;)', s, re.M | re.S); assert m, n; return m
def setf(n, f, v):
    global s
    m = line(n); e = m.group(0)
    fm = re.search(r'(?:^|[,\n ])%s:("(?:[^"\\]|\\.)*"|\[[^\]]*\]|\d+)' % f, e); assert fm, (n, f)
    s = s[:m.start()] + e[:fm.start(1)] + J(v) + e[fm.end(1):] + s[m.end():]
def getf(n, f):
    return json.loads(re.search(r'(?:^|[,\n ])%s:("(?:[^"\\]|\\.)*")' % f, line(n).group(0)).group(1))
def addr(n, extra):
    r = getf(n, 'r')
    if extra not in r: setf(n, 'r', r.rstrip('.') + '. ' + extra)
def setj(name, key_, val):
    global s
    m = re.search(r'\nconst %s = (\{.*?\});\n' % name, s); o = json.loads(m.group(1)); o[key_] = val
    s = s[:m.start(1)] + J(o) + s[m.end(1):]
if key == 'dlbr':
    n = "BELINDA (Bishop)"
    setf(n, 'hr', "1.07 (event-free survival, stratified unadjusted; 95% CI 0.82-1.40; P=0.61); adjusted 0.95 (0.72-1.25). Overall survival (immature): unadjusted 1.24 (0.83-1.85), adjusted 0.99 (0.64-1.52) (full paper)")
    setf(n, 'fu', "10.0 mo median from randomization to data cutoff (range 2.9-23.2) (full paper)")
    addr(n, "By data cutoff 81 patients (50.6%) in the standard-care group had crossed over to receive tisagenlecleucel (full paper)")
    setj('TOX', n, "Deaths from adverse events: 10 with tisagenlecleucel and 13 with standard care. Grade 3 or higher adverse events 84.0% vs 90.0%. Among 155 infused patients: cytokine release syndrome 61.3% (grade 3 or higher 5.2%), neurologic events 10.3% (grade 3 or higher 1.9%) (full paper)")
elif key == 'al':
    n = "VITAL, birtamimab (Gertz)"
    setf(n, 'hr', "0.826 (primary end point; 95% CI 0.574-1.189). Post hoc, Mayo stage IV (77 patients: 38 vs 39), all-cause mortality at 9 months: 0.413 (0.191-0.895; log-rank P=.021) (full paper)")
    setf(n, 'fu', "15.7 mo (Q1-Q3 12.0-22.1) with birtamimab vs 14.5 mo (10.3-19.8) with placebo; Mayo stage IV 15.2 vs 11.3 mo (full paper)")
    setj('TOX', n, "Treatment-emergent grade 3 or higher events 74% vs 78% (stage IV 79% vs 90%); serious events 68% vs 70%; events leading to study drug withdrawal 5% vs 11% (full paper)")
    n = "CARES, anselamimab (Wechalekar)"
    setf(n, 'fu', "Median follow-up not reported; primary analysis 18 months after the last patient was enrolled in each trial; median treatment duration 21.4 mo with anselamimab vs 21.1 mo with placebo (kappa isotype: 22.3 vs 11.8 mo) (full paper)")
    setj('TOX', n, "Serious adverse events 75.6% vs 75.4%; grade 3 or higher 80.4% vs 84.3%; adverse events leading to death 27.7% vs 30.6% and to discontinuation 13.3% vs 10.4% (anselamimab vs placebo) (full paper)")
elif key == 'wm':
    n = "Ibrutinib, previously treated (Treon)"
    setf(n, 'fu', "Median follow-up not reported in the primary report; median treatment duration 19.1 mo (range 0.5-29.7), database lock December 19, 2014, 68% still on treatment (full paper); 59 mo (final analysis)")
io.open(p, 'w', encoding='utf-8').write(s)
print(key, 'done')
