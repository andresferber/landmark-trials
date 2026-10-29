"""Add a "Drug mechanisms" tab: one entry per drug class tested in the trials on the page, with a
plain one-line description of how it works, the mechanism review already linked on the cards, and the
trials that used it (each jumps to its card). Built from MOA and MOAMAP on the page plus descriptions
in mech_master.json (shared across pages, keyed by MOA key).
Usage: python3 install_mechtab.py mech_master.json page.html [page.html ...]
Rerunnable: on a page that already has the tab it refreshes MECH from mech_master.json."""
import sys, io, json, re

master = json.load(open(sys.argv[1], encoding='utf-8'))

BTN_ANCHOR = '<a class="tabmail"'
BTN = '<button type="button" role="tab" aria-selected="false" data-tab="mech">Drug mechanisms<span class="tcount"></span></button>\n    '
SEC_ANCHOR = '<section class="newdrugs" hidden aria-label="New drugs to watch"></section>'
SEC = SEC_ANCHOR + '\n  <section class="mechs" hidden aria-label="Drug mechanisms"></section>'

JS_OLD_SHOW = '''    if (panel) panel.hidden = which !== "newdrugs";
  }'''
JS_NEW_SHOW = '''    if (panel) panel.hidden = which !== "newdrugs";
    if (mpanel) mpanel.hidden = which !== "mech";
    if (watch && which === "mech") watch.style.display = "none";
  }
  // Drug mechanisms tab: classes tested on this page, how they work, the review, and the trials that used them.
  const mpanel = root.querySelector(".mechs");
  const mKeys = (typeof MOA !== "undefined" && typeof MOAMAP !== "undefined" && typeof MECH !== "undefined")
    ? Object.keys(MOA).filter(k => MECH[k] && T.some(t => (MOAMAP[t.n] || []).includes(k))) : [];
  const cm = tabs.querySelector('[data-tab="mech"] .tcount'); if (cm) cm.textContent = mKeys.length;
  if (mpanel && mKeys.length) {
    mpanel.innerHTML = '<p class="mx-note">Each drug class tested in the trials on this page: how it works, a recent peer-reviewed review on mechanism and resistance, and the trials that used it. Select a trial to jump to its card.</p>' +
      mKeys.map(k => { const m = MOA[k];
        const trials = T.filter(t => (MOAMAP[t.n] || []).includes(k)).sort((a, b) => a.y - b.y);
        return '<div class="mx-item"><h2 class="mx-name">' + esc(m.l) + '</h2><p class="mx-desc">' + esc(MECH[k]) + '</p>' +
          '<p class="mx-rev"><span class="mx-k">Review</span> <a href="' + esc(MOAURL(m)) + '" target="_blank" rel="noopener">' + esc(m.a + ', ' + m.j + ' ' + m.y) + ' ↗</a>' + (m.pmc ? ' <span class="moafree">free</span>' : '') + '</p>' +
          '<p class="mx-trials"><span class="mx-k">Trials on this page</span> ' + trials.map(t => '<a class="mt" href="#t-' + PAGEKEY + '-' + t.slug + '" data-slug="' + t.slug + '">' + esc(t.n) + ' <span class="mt-y">' + t.y + '</span></a>').join("") + '</p></div>'; }).join("");
    mpanel.addEventListener("click", e => {
      const a = e.target.closest("a.mt"); if (!a) return;
      e.preventDefault();
      show("trials");
      tabs.dispatchEvent(new Event("tabschange"));
      const first = chipsEl.querySelector(".chip");
      if (first && first.getAttribute("aria-pressed") !== "true") first.click();
      if (qEl.value) { qEl.value = ""; render(); }
      const li = listEl.querySelector('li[data-trial="' + a.getAttribute("data-slug") + '"]');
      if (!li) return;
      li.scrollIntoView({ behavior: "smooth", block: "start" });
      li.classList.remove("flash"); void li.offsetWidth; li.classList.add("flash");
    });
  }'''

CSS = '''
/* Added Oct 28, 2026: Drug mechanisms tab */
.mechs { margin-top: 14px; }
.mechs a { color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
.mechs .mx-note { font-size: 14px; color: var(--muted); margin: 0 0 6px; max-width: 72ch; }
.mechs .mx-item { padding: 16px 0; border-bottom: 1px solid var(--rule); }
.mechs .mx-name { font-family: var(--font-display); font-weight: 650; font-size: 1.08rem; margin: 0 0 6px; }
.mechs .mx-desc { margin: 0 0 8px; max-width: 78ch; font-size: 14.5px; line-height: 1.55; }
.mechs .mx-rev, .mechs .mx-trials { margin: 4px 0 0; font-size: 14px; }
.mechs .mx-k { font: 500 11px/1.9 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-right: 8px; }
.mechs .mx-trials { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
.mechs a.mt { display: inline-block; text-decoration: none; color: var(--fg); border: 1px solid var(--rule); background: var(--surface); border-radius: 999px; padding: 3px 10px; font-size: 13px; }
.mechs a.mt:hover { border-color: var(--accent); color: var(--accent); }
.mechs .mt-y { font: 500 11px var(--font-mono); color: var(--muted); margin-left: 4px; }
@media print { .mechs { display: none; } }
'''

for page in sys.argv[2:]:
    s = io.open(page, encoding='utf-8').read()
    moa = json.loads(re.search(r'const MOA = (\{.*?\});\n', s, re.S).group(1))
    mm = json.loads(re.search(r'const MOAMAP = (\{.*?\});\n', s, re.S).group(1))
    used = sorted({k for v in mm.values() for k in v})
    missing = [k for k in used if k in moa and k not in master]
    if missing:
        raise SystemExit(f'{page}: write descriptions in mech_master.json first for {missing}')
    mech = {k: master[k] for k in used if k in moa}
    if 'data-tab="mech"' in s:
        # Already installed: refresh the descriptions so new classes and edits appear.
        s = re.sub(r'const MECH = \{.*?\};\n', lambda _: 'const MECH = ' + json.dumps(mech, ensure_ascii=False) + ';\n', s, count=1)
        io.open(page, 'w', encoding='utf-8').write(s)
        print('refreshed', page, len(mech), 'classes'); continue
    for old, new in [(BTN_ANCHOR, BTN + BTN_ANCHOR), (SEC_ANCHOR, SEC), (JS_OLD_SHOW, JS_NEW_SHOW)]:
        if s.count(old) != 1:
            raise SystemExit(f'{page}: expected 1 match for {old[:40]!r}, found {s.count(old)}')
        s = s.replace(old, new)
    m = re.search(r'const MOAMAP = \{.*?\};\n', s, re.S)
    s = s[:m.end()] + 'const MECH = ' + json.dumps(mech, ensure_ascii=False) + ';\n' + s[m.end():]
    i = s.index('--font-display'); j = s.index('</style>', i)
    s = s[:j] + CSS + s[j:]
    io.open(page, 'w', encoding='utf-8').write(s)
    print('ok', page, len(mech), 'classes')
