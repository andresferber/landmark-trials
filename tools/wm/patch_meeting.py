"""Support for a card whose only report is a meeting abstract (no PMID): such an entry has p:0 plus murl (the abstract's
URL) and meet:1. The source link then opens the abstract, and the evidence tag reads "✓ meeting abstract".
Usage: python3 tools/wm/patch_meeting.py page.html "<trial name>" <url>   (rerunnable)"""
import sys, io, json
page, name, url = sys.argv[1:4]
s = io.open(page, encoding='utf-8').read()
key = 'n:' + json.dumps(name, ensure_ascii=False)
i = s.index(key); j = s.index(',p:0', i)
if 'murl:' not in s[j:j + 200]:
    s = s[:j] + ',p:0,murl:' + json.dumps(url) + ',meet:1' + s[j + 4:]
old = 't.url = PM(t.p);'
if old in s: s = s.replace(old, 't.url = t.murl || PM(t.p);')
old = 'function eviHTML(t) {\n  return t.full'
if old in s:
    s = s.replace(old, 'function eviHTML(t) {\n  if (t.meet) return \'<span class="ok meet" title="Checked against the meeting abstract; no full peer-reviewed report has been published">✓ meeting abstract</span>\';\n  return t.full')
io.open(page, 'w', encoding='utf-8').write(s)
print('ok')
