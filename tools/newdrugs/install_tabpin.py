"""Keep the tab bar pinned to the top of the screen while Trials to watch, New drugs to watch or Drug
mechanisms is open, so a tab can be switched or closed from anywhere in a long list. Done in script
(not CSS sticky) because the website turns sticky off; on the website the bar sits just below the
pinned topic title bar and any fixed site header.
Usage: python3 install_tabpin.py file [file ...]   (pages, install_tabs.py, install_mechtab.py). Rerunnable."""
import sys, io

TOGGLE_OLD = '''    if (w !== "trials" && b.getAttribute("aria-selected") === "true") {
      show("trials");
      tabs.scrollIntoView({ behavior: "smooth", block: "nearest" });
      return;
    }
    show(w);'''
TOGGLE_NEW = '''    if (w !== "trials" && b.getAttribute("aria-selected") === "true") {
      show("trials");
      tabs.dispatchEvent(new Event("tabschange"));
      if (tabs._scrollHome) tabs._scrollHome(); else tabs.scrollIntoView({ behavior: "smooth", block: "nearest" });
      return;
    }
    show(w);
    tabs.dispatchEvent(new Event("tabschange"));'''

MECH_OLD = '''      e.preventDefault();
      show("trials");
      const first = chipsEl.querySelector(".chip");'''
MECH_NEW = '''      e.preventDefault();
      show("trials");
      tabs.dispatchEvent(new Event("tabschange"));
      const first = chipsEl.querySelector(".chip");'''

PIN_JS = '''(function pinTabs(){
  // Pin the tab bar while a tab other than Landmark trials is open.
  const listEl = document.getElementById("list");
  const root = listEl.parentNode;
  const tabs = root.querySelector(".tabs");
  if (!tabs) return;
  const ph = document.createElement("div");
  ph.className = "tabs-ph"; ph.hidden = true;
  tabs.parentNode.insertBefore(ph, tabs);
  let pinned = false;
  function topOffset() {
    // Below the website's pinned topic title bar, or any fixed site header; 0 on the standalone page.
    const h = document.querySelector(".lta-head.lta-pinned");
    if (h) return Math.max(0, h.getBoundingClientRect().bottom);
    let off = 0;
    try {
      (document.elementsFromPoint(window.innerWidth / 2, 2) || []).forEach(el => {
        if (root.contains(el)) return;
        for (let n = el; n && n !== document.body; n = n.parentElement) {
          const p = getComputedStyle(n).position;
          if (p === "fixed" || p === "sticky") {
            const r = n.getBoundingClientRect();
            if (r.top <= 2 && r.bottom > off && r.bottom < window.innerHeight * 0.4) off = r.bottom;
            break;
          }
        }
      });
    } catch (e) {}
    return off;
  }
  function unpin() {
    if (!pinned) return;
    tabs.classList.remove("tabs-pinned");
    tabs.style.top = tabs.style.left = tabs.style.width = "";
    ph.hidden = true; pinned = false;
  }
  function update() {
    const sel = tabs.querySelector('button[aria-selected="true"]');
    const active = !!sel && sel.getAttribute("data-tab") !== "trials";
    const off = topOffset();
    const r = (pinned ? ph : tabs).getBoundingClientRect();
    const rr = root.getBoundingClientRect();
    const h = tabs.offsetHeight;
    if (active && r.top < off && rr.bottom > off + h + 40) {
      if (!pinned) { ph.style.height = h + "px"; ph.hidden = false; tabs.classList.add("tabs-pinned"); pinned = true; }
      const pr = ph.getBoundingClientRect();
      tabs.style.top = off + "px"; tabs.style.left = pr.left + "px"; tabs.style.width = pr.width + "px";
    } else unpin();
  }
  let ticking = false;
  const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; update(); }); } };
  window.addEventListener("scroll", req, { passive: true });
  document.addEventListener("scroll", req, { passive: true, capture: true });
  window.addEventListener("resize", req);
  tabs.addEventListener("tabschange", () => { unpin(); req(); });
  // Closing a tab returns to the top of the trial list, just below any pinned header.
  tabs._scrollHome = () => {
    const y = tabs.getBoundingClientRect().top + window.pageYOffset - topOffset() - 8;
    if (tabs.getBoundingClientRect().top < topOffset()) window.scrollTo({ top: Math.max(0, y), behavior: "smooth" });
  };
})();
'''
PIN_ANCHOR = '(function setupShare(){'

CSS = '''
/* Added Oct 28, 2026: tab bar pinned while a tab other than Landmark trials is open */
.tabs-ph { margin-top: 18px; }
.tabs.tabs-pinned { position: fixed; z-index: 9000; margin-top: 0; border-radius: 0 0 10px 10px; box-shadow: 0 6px 14px -8px rgba(16,24,40,.35); }
@media print { .tabs.tabs-pinned { position: static; } }
@media (max-width: 560px) { .tabs.tabs-pinned { padding-top: 2px; } .tabs.tabs-pinned button { padding: 8px 10px; } .tabs.tabs-pinned .tabmail { display: none; } }
'''

for f in sys.argv[1:]:
    s = io.open(f, encoding='utf-8').read()
    if 'tabschange' in s:
        print('skip (already done)', f); continue
    did = []
    if s.count(TOGGLE_OLD) == 1:
        s = s.replace(TOGGLE_OLD, TOGGLE_NEW); did.append('toggle')
    if s.count(MECH_OLD) == 1:
        s = s.replace(MECH_OLD, MECH_NEW); did.append('mech')
    if f.endswith('.html'):
        if 'toggle' not in did:
            raise SystemExit(f + ': tab handler not found (run install_tabtoggle.py first)')
        assert s.count(PIN_ANCHOR) == 1, f
        s = s.replace(PIN_ANCHOR, PIN_JS + PIN_ANCHOR)
        i = s.index('--font-display'); j = s.index('</style>', i)
        s = s[:j] + CSS + s[j:]
        did.append('pin')
    io.open(f, 'w', encoding='utf-8').write(s)
    print('ok', f, did)
