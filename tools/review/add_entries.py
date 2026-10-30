"""Add new trial entries (from a data module such as p2_entries_2026_10.py) to the topic pages.
Each entry goes into T within its category, in year order, plus TOX, REG, FT and MOAMAP; on the MCL
page also into M, P, X, R and EXTRA. Missing MOA keys are copied from tools/moa_master.json.
Usage: python3 tools/review/add_entries.py <data module> page.html [...]  (page key from the file name)
Skips an entry whose name is already on the page. Rerunnable."""
import sys, io, json, re, importlib.util, os

spec = importlib.util.spec_from_file_location('data', sys.argv[1]); data = importlib.util.module_from_spec(spec); spec.loader.exec_module(data)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MOA_MASTER = json.load(open(os.path.join(ROOT, 'tools/moa_master.json'), encoding='utf-8'))
J = lambda v: json.dumps(v, ensure_ascii=False)

def js_cm(cm):
    return '[' + ','.join('[%d,%s,%s]' % (c[0], J(c[1]), J(c[2])) for c in cm) + ']'

def t_full(e):
    s = '{y:%d,n:%s,s:%s,ph:%s,d:%s,ep:%s,\n r:%s,N:%s,hr:%s,fu:%s,\n c:%s,p:%d' % (
        e['y'], J(e['n']), J(e['s']), J(e['ph']), J(e['d']), J(e['ep']), J(e['r']), J(e['N']), J(e['hr']), J(e['fu']), J(e['c']), e['p'])
    if e.get('extra'): s += ',extra:[%s,%d]' % (J(e['extra'][0]), e['extra'][1])
    s += ',\n b:%s,\n i:%s,\n q:%s,\n cm:%s,\n reg:%s,gl:%s,acc:%s}' % (
        J(e['b']), J(e['i']), J(e['q']), js_cm(e['cm']), J(e['reg']), J(e['gl']), J(e['acc']))
    return s

def t_mcl(e):
    return '  {y:%d,n:%s,s:%s,ph:%s,d:%s,ep:%s,r:%s,i:%s,c:%s}' % (
        e['y'], J(e['n']), J(e['s']), J(e['ph']), J(e['d']), J(e['ep']), J(e['r']), J(e['i']), J(e['c']))

def insert_T(s, e, text):
    i = s.index('const T = ['); j = s.index('\n];', i)
    block = s[i:j]
    ents = [(m.start() + i, int(m.group(1)), m.group(2)) for m in re.finditer(r'^[ \t]*\{y:(\d{4}),n:"[^"]*",s:"(\w+)"', block, re.M)]
    same = [x for x in ents if x[2] == e['s']]
    assert same, 'no entries in category ' + e['s']
    before = [x for x in same if x[1] <= e['y']]
    if before:
        k = ents.index(before[-1])
        if k + 1 < len(ents):
            pos = ents[k + 1][0]
        else:
            pos = j
    else:
        pos = same[0][0]
    # Insert at pos (start of the next entry or a comment line before it, or the end of the array).
    if pos == j:
        prev = s[:pos].rstrip()
        if not prev.endswith(','): s = prev + ',' + s[len(prev):]; pos = s.index('\n];', i)
        return s[:pos] + '\n' + text + s[pos:]
    # Keep any category comment above the next entry attached to it.
    line_start = s.rfind('\n', 0, pos) + 1
    return s[:line_start] + text + ',\n' + s[line_start:]

def json_obj(s, name):
    m = re.search(r'const ' + name + r' = (\{.*?\});\n', s, re.S)
    return m, json.loads(m.group(1))

def set_json(s, name, key, val):
    m, obj = json_obj(s, name)
    obj[key] = val
    return s[:m.start(1)] + json.dumps(obj, ensure_ascii=False) + s[m.end(1):]

def append_js(s, name, line):
    i = s.index('const ' + name + ' = {'); j = s.index('\n};', i)
    return s[:j] + ',\n' + line + s[j:]

for page in sys.argv[2:]:
    key = os.path.basename(page).split('.')[0]
    s = io.open(page, encoding='utf-8').read()
    added = []
    for e in data.PAGES[key]:
        if ('n:' + J(e['n'])) in s:
            print('skip (present)', key, e['n']); continue
        if key == 'mcl':
            s = insert_T(s, e, t_mcl(e))
            n = J(e['n'])
            s = append_js(s, 'M', '  %s: [%s,%s,%s]' % (n, J(e['N']), J(e['hr']), J(e['fu'])))
            s = append_js(s, 'P', '  %s: %d' % (n, e['p']))
            s = append_js(s, 'X', '  %s: {\n    b:%s,\n    i:%s,\n    q:%s}' % (n, J(e['b']), J(e['i']), J(e['q'])))
            s = append_js(s, 'R', '  %s: {cm:%s, reg:%s, gl:%s, acc:%s}' % (n, js_cm(e['cm']), J(e['reg']), J(e['gl']), J(e['acc'])))
            # The "✓ abstract" tag on the MCL page shows only for trials with a V entry.
            s = append_js(s, 'V', '  %s: {r:%s, N:%s, fu:%s}' % (n, J(e['r']), J(e['N']), J(e['fu'])))
            if e.get('extra'):
                s = append_js(s, 'EXTRA', '  %s: [%s, PMID(%d)]' % (n, J(e['extra'][0]), e['extra'][1]))
        else:
            s = insert_T(s, e, t_full(e))
        s = set_json(s, 'TOX', e['n'], e['tox'])
        if e['reg_ids']: s = set_json(s, 'REG', e['n'], e['reg_ids'])
        s = set_json(s, 'FT', e['n'], e['ft'])
        s = set_json(s, 'MOAMAP', e['n'], e['moa'])
        _, moa = json_obj(s, 'MOA')
        for k in e['moa']:
            if k not in moa:
                s = set_json(s, 'MOA', k, MOA_MASTER[k]); print('  MOA key added', key, k)
        added.append(e['n'])
    io.open(page, 'w', encoding='utf-8').write(s)
    print('ok', key, added)
