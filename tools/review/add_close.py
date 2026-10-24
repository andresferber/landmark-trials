"""Add a 'Close the perspective' button at the end of the Perspective block (pages and builder templates). Idempotent."""
import sys
JS_OLD = '''    const a = e.target.closest("a.rref");
    if (!a) return;'''
JS_NEW = '''    if (e.target.closest(".rv-close")) {
      box.open = false;
      box.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    const a = e.target.closest("a.rref");
    if (!a) return;'''
CSS_ANCHOR = '.review .rv-refs { font-size: 13.5px; padding-left: 22px; }'
CSS_ADD = CSS_ANCHOR + '\n.review .rv-endbar { display: flex; justify-content: center; margin: 18px 0 2px; }\n.review .rv-close { all: unset; cursor: pointer; font: 500 13px/1 var(--font-body); padding: 9px 16px; border-radius: 999px; border: 1px solid var(--rule); background: var(--bg); color: var(--fg); }\n.review .rv-close:hover { border-color: var(--accent); color: var(--accent); }\n.review .rv-close:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }\n@media print { .review .rv-endbar { display: none; } }'
BTN = '<div class="rv-endbar"><button type="button" class="rv-close">Close the perspective ▴</button></div>'
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'rv-close' in s:
        print('skip', f); continue
    assert s.count(JS_OLD) == 1 and s.count(CSS_ANCHOR) == 1, f
    s = s.replace(JS_OLD, JS_NEW).replace(CSS_ANCHOR, CSS_ADD)
    if f.endswith('.py'):
        old = '<ol class="rv-refs">{refs}</ol>'
        assert s.count(old) == 1, f
        s = s.replace(old, old + '\n      ' + BTN)
    else:
        i = s.index('<ol class="rv-refs">'); j = s.index('</ol>', i) + 5
        s = s[:j] + '\n      ' + BTN + s[j:]
    open(f, 'w', encoding='utf-8').write(s); print('ok', f)
