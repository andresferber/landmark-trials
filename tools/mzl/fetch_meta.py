"""Fetch registry IDs, full-text links (PubMed Central or DOI, with Unpaywall) and commentaries for the mzl entries.
Usage (repository root): python3 tools/mzl/fetch_meta.py  -> writes tools/mzl/meta.json. Needs network access."""
import sys, json, re, time, subprocess, urllib.parse
sys.path.insert(0, 'tools/mzl'); sys.path.insert(0, '/home/claude/mzl')
import mzl_data as M
from pm import fetch, summ
pm = [x['p'] for x in M.E]
F, S = {}, {}
for i in range(0, len(pm), 20):
    F.update(fetch(pm[i:i+20])); S.update({d['pmid']: d for d in summ(pm[i:i+20])})
cmids = sorted({c[0] for v in F.values() for c in v['cm'] if c[0]})
CS = {}
for i in range(0, len(cmids), 40): CS.update({d['pmid']: d for d in summ(cmids[i:i+40])})
REG, FT, CM, CHK = {}, {}, {}, {}
for x in M.E:
    p = str(x['p']); f, s = F[p], S[p]
    CHK[x['n']] = '%s %s;%s:%s | %s' % (s['j'], s['y'], s['v'], s['pg'], s['au'])
    ids = [r for r in f['reg'] if re.match(r'NCT\d{8}$|ISRCTN\d+$', r)]
    if ids: REG[x['n']] = ids
    cm = []
    for cid, _ in f['cm']:
        c = CS.get(cid)
        if not c: continue
        pt = ' '.join(c.get('pt') or [])
        if 'Letter' in pt or 'reply' in c['t'].lower(): continue
        cm.append([int(cid), '%s, %s %s' % (c['au'], c['j'], c['y']), c['t'].rstrip('.')])
    CM[x['n']] = cm
    if s['pmc']: FT[x['n']] = ['pmc', s['pmc']]
    elif s['doi']:
        ft = ['doi', s['doi']]
        try:
            r = subprocess.run(['curl', '-sS', '--max-time', '30', 'https://api.unpaywall.org/v2/%s?email=andresferber@hotmail.com' % urllib.parse.quote(s['doi'], safe='/')], capture_output=True, text=True)
            b = (json.loads(r.stdout).get('best_oa_location') or {}); time.sleep(0.3)
            if b.get('host_type') == 'publisher': ft.append('free')
            elif b.get('host_type') == 'repository':
                u = b.get('url_for_pdf') or b.get('url') or ''
                host = urllib.parse.urlparse(u).netloc
                if u and 'pubmed' not in host and 'ncbi' not in host and not re.search(r'ascopubs|ashpublications|thelancet|wiley|elsevier|nejm|bmj|springer|nature|oup\.com|tandfonline|haematologica|aacrjournals', host):
                    ft += ['repo', u]
        except Exception as ex: print('unpaywall failed', x['n'], ex)
        FT[x['n']] = ft
json.dump({'REG': REG, 'FT': FT, 'CM': CM, 'CHK': CHK}, open('tools/mzl/meta.json', 'w'), ensure_ascii=False, indent=1)
for x in M.E: print(x['c'], '||', CHK[x['n']], '||', FT.get(x['n']), REG.get(x['n'], ''), len(CM[x['n']]))
