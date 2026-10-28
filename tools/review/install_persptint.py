"""Give the Perspective bar a warm parchment tint with a matching left stripe, so it stands apart from
the navigation (tab bar) and draws the eye. The open Perspective's reading area stays white.
Usage: python3 install_persptint.py page.html [page.html ...]   Rerunnable."""
import sys, io

CSS = '''
/* Added Oct 28, 2026: warm parchment tint on the Perspective bar */
:root { --rv-bg: #fbf8f1; --rv-stripe: #ae915a; --rv-ink: #7a5a22; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --rv-bg: #221e18; --rv-stripe: #c9a56a; --rv-ink: #dcbd85; } }
:root[data-theme="dark"] { --rv-bg: #221e18; --rv-stripe: #c9a56a; --rv-ink: #dcbd85; }
.review { border-left: 4px solid var(--rv-stripe); }
.review > summary { background: var(--rv-bg); border-radius: 8px 11px 11px 8px; }
.review[open] > summary { border-radius: 8px 11px 0 0; border-bottom: 1px solid var(--rule); margin-bottom: 14px; }
.review .rv-kicker { color: var(--rv-ink); }
.review .rv-open { background: var(--surface); border-color: var(--rv-stripe); color: var(--rv-ink); }
@media print { .review > summary { background: none; } }
'''

for page in sys.argv[1:]:
    s = io.open(page, encoding='utf-8').read()
    if '--rv-bg' in s:
        print('skip (already done)', page); continue
    if '<details class="review"' not in s:
        raise SystemExit(page + ': no Perspective block')
    i = s.index('--font-display'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    io.open(page, 'w', encoding='utf-8').write(s)
    print('ok', page)
