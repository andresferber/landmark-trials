"""Values completed from ten full papers Andres supplied as PDFs on Nov 15, 2026 (values marked "(full paper)"):
untreated DLBCL (ECOG 4494, MInT, FLYER, Alizadeh, Hans, R-IPI), relapsed DLBCL (CORAL), Waldenstrom (ASPEN, WM1, ECWM-1).
Usage: python3 fullpaper_2026_11_15.py <key> <page>. Rerunnable: each edit sets a value, never appends twice."""
import io, json, re, sys
key, p = sys.argv[1], sys.argv[2]
s = io.open(p, encoding='utf-8').read()
J = lambda v: json.dumps(v, ensure_ascii=False)
def line(n):
    # entries may span several lines: take the block up to the next entry or the end of the array
    m = re.search(r'^\{y:\d+,n:' + re.escape(J(n)) + r'.*?(?=^\{y:\d+,n:|^\]\s*;)', s, re.M | re.S); assert m, n; return m
def setf(n, f, v):
    global s
    m = line(n); e = m.group(0)
    fm = re.search(r'(?:^|[,\n ])%s:("(?:[^"\\]|\\.)*"|\[[^\]]*\]|\d+)' % f, e); assert fm, (n, f)
    s = s[:m.start()] + e[:fm.start(1)] + J(v) + e[fm.end(1):] + s[m.end():]
def getf(n, f):
    return json.loads(re.search(r'(?:^|[,\n ])%s:("(?:[^"\\]|\\.)*")' % f, line(n).group(0)).group(1))
def addr(n, base_start, extra):
    """append `extra` to r once (idempotent)"""
    r = getf(n, 'r')
    if extra not in r: setf(n, 'r', r.rstrip('.') + '. ' + extra)
E = {}
if key == 'dlbu':
    n = "ECOG 4494 / CALGB 9793 (Habermann)"
    setf(n, 'hr', "R-CHOP vs CHOP: failure-free survival 0.78 (95% CI 0.61-0.99; P=.04), overall survival 0.83 (0.63-1.09; P=.18). Rituximab maintenance vs observation: failure-free survival 0.63 (0.44-0.90; P=.009), overall survival 0.96 (0.63-1.47; P=.85); after CHOP 0.45 (0.29-0.71), after R-CHOP 0.93 (0.53-1.66; P=.81) (full paper)")
    n = "MInT (Pfreundschuh)"
    setf(n, 'hr', "Event-free survival with rituximab, multivariable (adjusted for bulky disease and age-adjusted IPI): 0.44 (95% CI 0.34-0.59; P<0.0001) (full paper)")
    n = "FLYER (Poeschel)"
    setf(n, 'hr', "4 vs 6 cycles, adjusted for strata and B symptoms: progression-free survival 0.9 (95% CI 0.5-1.6; P=0.81); overall survival 0.9 (0.4-1.9; P=0.72) (full paper)")
    addr(n, 0, "3-year event-free survival 89% in both groups; 3-year overall survival 99% vs 98%; 5-year progression-free survival 94% in both (post hoc) (full paper)")
    n = "Cell of origin by gene expression (Alizadeh)"
    setf(n, 'N', "42 DLBCL cases from two centers (34 Nebraska, 8 Stanford; clinical data missing for 2), among 96 normal and malignant samples (full paper)")
    setf(n, 'hr', "Not reported; Kaplan-Meier comparison of overall survival, P<0.01, and within low clinical risk (IPI 0-2) P<0.05 (full paper)")
    setf(n, 'fu', "Not reported in the paper (5-year survival estimates) (full paper)")
    addr(n, 0, "Five-year survival 76% with germinal centre B-like vs 16% with activated B-like disease (52% overall) (full paper)")
    n = "Hans algorithm (Hans)"
    setf(n, 'hr', "Multivariate analysis (128 patients): non-GCB 3.6-fold risk of death (95% CI 1.9-6.6; P<.001); high IPI (3-5) 4.2-fold (2.3-7.5) (full paper)")
    setf(n, 'fu', "6.4 y median in surviving patients (range 0.8-21.8) (full paper)")
    n = "R-IPI (Sehn)"
    setf(n, 'N', "365 (full paper)")
    setf(n, 'hr', "Not reported; Kaplan-Meier comparison of the three groups, P<.001 (full paper)")
    setf(n, 'fu', "33 mo median in living patients (range 7-64) (full paper)")
elif key == 'dlbr':
    n = "CORAL (Gisselbrecht)"
    setf(n, 'hr', "No treatment-arm hazard ratio reported; in the Cox model the treatment arm was not significant, while early relapse, prior rituximab and secondary age-adjusted IPI were (P<.001 for EFS, PFS and OS; prior rituximab P=.01) (full paper)")
    setf(n, 'fu', "27 mo (3-year estimates); 44 mo (maintenance part) (full paper)")
    addr(n, 0, "3-year EFS 31% (R-ICE 26%, R-DHAP 35%; P=.6), PFS 37% (31% vs 42%; P=.4), OS 49% (47% vs 51%; P=.4) (full paper)")
elif key == 'wm':
    n = "ASPEN (Tam)"
    setf(n, 'hr', "No hazard ratio for PFS or OS in the primary report (18-month event-free rates only). Time-to-event hazard ratios, zanubrutinib vs ibrutinib: atrial fibrillation or flutter 0.14 (95% CI 0.04-0.48); neutropenia 2.18 (1.15-4.12); pneumonia 0.37 (0.14-0.99); all infections 1.00 (0.73-1.38) (full paper; Figure 4)")
    setf(n, 'fu', "19.4 mo in the primary report (full paper); 44.4 mo in the final analysis")
    n = "WM1 (Leblond)"
    setf(n, 'hr', "Fludarabine vs chlorambucil, all 414 patients: PFS, adjusted hazard ratio for chlorambucil 1.34 (95% CI 1.04-1.71); duration of response 1.93 (1.31-2.85; P<.001); overall survival, hazard ratio of death on chlorambucil 1.44 (1.00-2.10; P=.046) (full paper)")
    n = "ECWM-1 (Buske)"
    setf(n, 'hr', "Not reported in the results; the design assumed a hazard ratio of 0.518, and 53 events had occurred at the data cutoff (full paper)")
    setf(n, 'fu', "27.5 mo (interquartile range 17.2-36.1) (full paper)")
io.open(p, 'w', encoding='utf-8').write(s)
print(key, 'done')
