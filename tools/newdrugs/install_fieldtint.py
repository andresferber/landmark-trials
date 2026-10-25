"""Tint the Endpoint, Result and Key toxicity rows with the same subtle colour on every trial card,
on every topic page (and the matching "Key data" and "Safety" rows in New drugs to watch).
Usage: python3 install_fieldtint.py page.html [page.html ...]   Rerunnable (skips pages already done)."""
import sys, io

ROWS = [
    ('<dt>Endpoint</dt><dd>${esc(t.ep)}</dd>',
     '<dt class="f-ep">Endpoint</dt><dd class="f-ep">${esc(t.ep)}</dd>'),
    ('<dt>Result</dt><dd class="result">',
     '<dt class="f-res">Result</dt><dd class="result f-res">'),
    ('<dt>Key toxicity</dt><dd class="tox">',
     '<dt class="f-tox">Key toxicity</dt><dd class="tox f-tox">'),
    ("<dt>Key data</dt><dd>' + esc(d.data) + '</dd><dt>Safety</dt><dd>' + esc(d.safety)",
     "<dt class=\"f-res\">Key data</dt><dd class=\"f-res\">' + esc(d.data) + '</dd><dt class=\"f-tox\">Safety</dt><dd class=\"f-tox\">' + esc(d.safety)"),
]

CSS = '''
/* Added Oct 25, 2026: the same subtle tint for Endpoint, Result and Key toxicity on every card and page */
:root { --f-ep-bg: #eef1f5; --f-res-bg: #e7effb; --f-tox-bg: #fcf8e6; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --f-ep-bg: #1e242e; --f-res-bg: #18253d; --f-tox-bg: #2d2915; } }
:root[data-theme="dark"] { --f-ep-bg: #1e242e; --f-res-bg: #18253d; --f-tox-bg: #2d2915; }
ol.list dl, .newdrugs dl { column-gap: 0; }
ol.list dt, .newdrugs dt { padding-right: 12px; }
dt.f-ep, dd.f-ep { background: var(--f-ep-bg); }
dt.f-res, dd.f-res { background: var(--f-res-bg); }
dt.f-tox, dd.f-tox { background: var(--f-tox-bg); }
dt.f-ep, dt.f-res, dt.f-tox { padding: 2px 12px 2px 8px; border-radius: 6px 0 0 6px; }
dd.f-ep, dd.f-res, dd.f-tox { padding: 2px 8px 2px 0; border-radius: 0 6px 6px 0; }
@media (max-width: 480px) {
  dt.f-ep, dt.f-res, dt.f-tox { border-radius: 6px 6px 0 0; padding-bottom: 0; }
  dd.f-ep, dd.f-res, dd.f-tox { border-radius: 0 0 6px 6px; padding: 0 8px 4px 8px; }
}
'''

for page in sys.argv[1:]:
    s = io.open(page, encoding='utf-8').read()
    if 'class="f-ep"' in s:
        print('skip (already done)', page); continue
    for old, new in ROWS:
        if s.count(old) != 1:
            raise SystemExit(f'{page}: expected 1 match, found {s.count(old)} for {old[:50]}')
        s = s.replace(old, new)
    i = s.index('--font-display'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    io.open(page, 'w', encoding='utf-8').write(s)
    print('ok', page)
