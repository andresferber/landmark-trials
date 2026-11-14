"""Add entries to the marginal zone lymphoma page (fields sub and also), in category and year order, plus TOX, REG, FT, MOAMAP
and any missing MOA key from tools/moa_master.json. Usage: python3 tools/mzl/add_mzl_entries.py <data module> <page.html>. Rerunnable."""
import sys, io, json, re, importlib.util, os
spec = importlib.util.spec_from_file_location('data', sys.argv[1]); data = importlib.util.module_from_spec(spec); spec.loader.exec_module(data)
page = sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MASTER = json.load(open(os.path.join(ROOT, 'tools/moa_master.json'), encoding='utf-8'))
J = lambda v: json.dumps(v, ensure_ascii=False)
KEYS = ['y', 'n', 's', 'also', 'sub', 'ph', 'd', 'ep', 'r', 'N', 'hr', 'fu', 'c', 'p', 'extra', 'rel', 'b', 'i', 'q', 'cm', 'reg', 'gl', 'acc']
def entry(e): return '{' + ','.join('%s:%s' % (k, J(e[k])) for k in KEYS if k in e) + '},'
def setj(s, name, key, val):
    m = re.search(r'\nconst %s = (\{.*?\});\n' % name, s); assert m, name
    o = json.loads(m.group(1)); o[key] = val
    return s[:m.start(1)] + J(o) + s[m.end(1):]
s = io.open(page, encoding='utf-8').read()
for e in data.E:
    if ('n:' + J(e['n'])) in s: print('skip', e['n']); continue
    i = s.index('const T = ['); j = s.index('\n];', i)
    ents = [(m.start() + i, int(m.group(1)), m.group(2)) for m in re.finditer(r'^\{y:(\d{4}),n:"[^"]*",s:"(\w+)"', s[i:j], re.M)]
    same = [x for x in ents if x[2] == e['s']]; assert same, e['s']
    after = [x for x in same if x[1] > e['y']]
    if after: pos = after[0][0]
    else:
        k = ents.index(same[-1]); pos = ents[k + 1][0] if k + 1 < len(ents) else j + 1
    s = s[:pos] + entry(e) + '\n' + s[pos:]
    s = setj(s, 'TOX', e['n'], e['tox']); s = setj(s, 'FT', e['n'], e['ft']); s = setj(s, 'MOAMAP', e['n'], e['moa'])
    if e['reg_ids']: s = setj(s, 'REG', e['n'], e['reg_ids'])
    m = re.search(r'\nconst MOA = (\{.*?\});\n', s); moa = json.loads(m.group(1))
    for k in e['moa']:
        if k not in moa: s = setj(s, 'MOA', k, MASTER[k]); print('MOA added', k)
    print('added', e['n'])
io.open(page, 'w', encoding='utf-8').write(s)
