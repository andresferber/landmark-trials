"""Clicking an open tab (Trials to watch, New drugs to watch, Drug mechanisms) closes it and returns to
the trial list, with the tab bar brought back into view. The open tab shows a small x as the cue.
Usage: python3 install_tabtoggle.py file [file ...]   (pages, or install_tabs.py itself). Rerunnable."""
import sys, io

OLD = '''    const b = e.target.closest("button[data-tab]"); if (!b) return;
    show(b.getAttribute("data-tab"));'''
NEW = '''    const b = e.target.closest("button[data-tab]"); if (!b) return;
    const w = b.getAttribute("data-tab");
    // Clicking the tab that is already open closes it and returns to the trial list.
    if (w !== "trials" && b.getAttribute("aria-selected") === "true") {
      show("trials");
      tabs.scrollIntoView({ behavior: "smooth", block: "nearest" });
      return;
    }
    show(w);'''

CSS = '''
/* Added Oct 28, 2026: an open tab closes on a second click; the x is the cue */
.tabs button[data-tab]:not([data-tab="trials"])[aria-selected="true"]::after { content: "\\00d7"; margin-left: 8px; font-weight: 500; color: var(--muted); }
.tabs button[data-tab]:not([data-tab="trials"])[aria-selected="true"]:hover::after { color: var(--fg); }
'''
TITLE_OLD = 'data-tab="watch">'
TITLE_NEW = 'data-tab="watch" title="Click again to return to the trial list">'

for f in sys.argv[1:]:
    s = io.open(f, encoding='utf-8').read()
    if 'Clicking the tab that is already open closes it' in s:
        print('skip (already done)', f); continue
    if s.count(OLD) != 1:
        raise SystemExit(f'{f}: expected 1 handler, found {s.count(OLD)}')
    s = s.replace(OLD, NEW)
    if f.endswith('.html'):
        for t in ('watch', 'newdrugs', 'mech'):
            a = f'data-tab="{t}">'
            if s.count(a) == 1:
                s = s.replace(a, f'data-tab="{t}" title="Click again to return to the trial list">')
        i = s.index('--font-display'); j = s.index('</style>', i)
        s = s[:j] + CSS + s[j:]
    io.open(f, 'w', encoding='utf-8').write(s)
    print('ok', f)
