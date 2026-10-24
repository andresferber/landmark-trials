"""Build a Perspective block for a topic page from review/persp_<key>.py.
Usage: python3 build_persp.py <key> <page.html>
Every [[Trial name]] must match a trial on the page; it becomes a numbered reference that jumps to the card.
Rerunnable: replaces the existing <details class="review"> block."""
import re, html, sys, importlib.util

key, page = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('c', f'review/persp_{key}.py'); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

DISC = ('<p class="rv-disc"><b>Personal perspective, for education only.</b> This text reflects the author\'s own reading and opinion of the published evidence. '
        'It is not a clinical practice guideline, medical advice or a substitute for clinical judgment. Patient care should follow the primary literature, '
        'current guidelines (such as NCCN, ESMO, IMWG and ASCO), approved prescribing information and the individual patient\'s circumstances.</p>')

CSS = '''
/* Added Oct 24, 2026: Perspective (collapsible reader view) */
.review { margin-top: 18px; border: 1px solid var(--rule); border-radius: 12px; background: var(--surface); }
.review > summary { list-style: none; cursor: pointer; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; padding: 14px 18px; }
.review > summary::-webkit-details-marker { display: none; }
.review .rv-kicker { font: 500 11px/1 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
.review .rv-title { font-family: var(--font-display); font-weight: 650; font-size: 1.05rem; flex: 1 1 260px; }
.review .rv-open { font: 500 13px/1 var(--font-body); padding: 8px 14px; border-radius: 999px; border: 1px solid var(--rule); background: var(--bg); color: var(--fg); }
.review[open] .rv-open { font-size: 0; }
.review[open] .rv-open::before { content: "Close"; font-size: 13px; }
.review .rv-body { padding: 0 18px 18px; max-width: 72ch; font-size: 15.5px; line-height: 1.65; }
.review .rv-body h3 { font-family: var(--font-display); font-weight: 650; font-size: 1.12rem; margin: 22px 0 6px; }
.review .rv-body p { margin: 0 0 12px; }
.review .rv-body ul { margin: 0 0 12px; padding-left: 20px; }
.review .rv-body li { margin: 4px 0; }
.review .rv-meta { font-size: 12.5px; color: var(--muted); }
.review .rv-disc { font-size: 13px; line-height: 1.5; color: var(--fg); background: var(--s-old-bg); border: 1px solid var(--rule); border-radius: 8px; padding: 10px 12px; margin: 8px 0 14px; }
.review .rv-take { border-left: 3px solid var(--accent); background: var(--bg); padding: 4px 14px 6px; margin: 12px 0 16px; border-radius: 0 8px 8px 0; }
.review .rv-take h3 { margin-top: 10px; }
.review sup a { font: 600 11px var(--font-mono); text-decoration: none; color: var(--accent); padding: 0 1px; }
.review a { color: var(--accent); }
.review .rv-refs { font-size: 13.5px; padding-left: 22px; }
.rv-tl { margin: 8px 0 18px; }
.rv-tl figcaption { font: 500 11px/1.6 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
.rv-tl ol { list-style: none; margin: 0; padding: 0 0 0 4px; border-left: 2px solid var(--rule); }
.rv-tl li { position: relative; display: grid; grid-template-columns: 48px minmax(0, 1fr); gap: 10px; padding: 5px 0 5px 14px; font-size: 14px; line-height: 1.45; }
.rv-tl li::before { content: ""; position: absolute; left: -7px; top: 10px; width: 10px; height: 10px; border-radius: 50%; background: var(--surface); border: 2px solid var(--muted); }
.rv-tl li.tl-old::before { border-color: var(--s-old); background: var(--s-old-bg); }
.rv-tl li.tl-young::before { border-color: var(--s-young); background: var(--s-young-bg); }
.rv-tl li.tl-p2::before { border-color: var(--s-p2); background: var(--s-p2-bg); }
.rv-tl li.tl-rr::before { border-color: var(--s-rr); background: var(--s-rr-bg); }
.rv-tl .tl-y { font: 500 13px var(--font-mono); color: var(--muted); }
@media print { .review .rv-open { display: none; } }
'''

JUMP = '''
(function setupReviewRefs(){
  const listEl = document.getElementById("list");
  const box = listEl.parentNode.querySelector(".review");
  if (!box) return;
  box.addEventListener("click", e => {
    const a = e.target.closest("a.rref");
    if (!a) return;
    e.preventDefault();
    const first = chipsEl.querySelector(".chip");
    if (first && first.getAttribute("aria-pressed") !== "true") first.click();
    if (qEl.value) { qEl.value = ""; render(); }
    const li = listEl.querySelector('li[data-trial="' + a.getAttribute("data-slug") + '"]');
    if (!li) return;
    li.scrollIntoView({ behavior: "smooth", block: "start" });
    li.classList.remove("flash"); void li.offsetWidth; li.classList.add("flash");
  });
})();
'''

h = open(page, encoding='utf-8').read()
names = re.findall(r'n:"([^"]+)"', h)
cites = dict(re.findall(r'n:"([^"]+)"[^\n]*?c:"([^"]+)"', h))
for n in names:
    if n not in cites:
        m = re.search(r'n:"' + re.escape(n) + r'".*?c:"([^"]+)"', h, re.S)
        if m: cites[n] = m.group(1)
pmids = {}
for n in names:
    i = h.find('n:"' + n + '"'); seg = h[i:]; k = re.search(r'\n\s*\{y:|\n\];', seg); seg = seg[:k.start()] if k else seg[:3000]
    m = re.search(r'\bp:"?(\d{6,9})', seg) or re.search(r'\n\s*"' + re.escape(n) + r'": (\d{6,9}),', h)
    if m: pmids[n] = m.group(1)
slug = lambda s: re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', s.lower()))
order = []

def ref(m):
    n = m.group(1)
    if n not in names:
        sys.exit('unknown trial: ' + n)
    if n not in order:
        order.append(n)
    i = order.index(n) + 1
    return f'<sup><a class="rref" href="#t-{key}-{slug(n)}" data-slug="{slug(n)}" title="{html.escape(n)}">{i}</a></sup>'

body = re.sub(r'\s*\[\[([^\]]+)\]\]', ref, c.BODY.strip())
refs = ''.join(
    f'<li><a class="rref" href="#t-{key}-{slug(n)}" data-slug="{slug(n)}">{html.escape(n)}</a>. {html.escape(cites.get(n, ""))}.'
    + (f' <a href="https://pubmed.ncbi.nlm.nih.gov/{pmids[n]}/" target="_blank" rel="noopener">PubMed ↗</a>' if n in pmids else '') + '</li>' for n in order)
take = ''.join(f'<li>{html.escape(t)}</li>' for t in c.TAKE)
tl = ''.join(f'<li class="tl-{col}"><span class="tl-y">{y}</span><span class="tl-e">{html.escape(e)}</span></li>' for y, e, col in c.TIMELINE)
words = len(re.sub(r'<[^>]+>', ' ', body).split())
block = f'''  <details class="review" id="review">
    <summary><span class="rv-kicker">Perspective</span><span class="rv-title">{html.escape(c.TITLE)}</span><span class="rv-open">Read the perspective</span></summary>
    <div class="rv-body">
      <p class="rv-meta">Andres Ferber, MD, with the assistance of Claude (Anthropic) · Last updated {c.UPDATED} · About {round(words, -2):,} words. Numbers are taken from the verified trial entries on this page; numbered references jump to each trial.</p>
      {DISC}
      <div class="rv-take"><h3>Key points</h3><ul>{take}</ul></div>
      <figure class="rv-tl"><figcaption>{html.escape(c.TL_CAPTION)}</figcaption><ol>{tl}</ol></figure>
      {body}
      <h3>References</h3>
      <ol class="rv-refs">{refs}</ol>
    </div>
  </details>
'''
if '<details class="review"' in h:
    h = re.sub(r'  <details class="review".*?</details>\n', lambda m: block, h, count=1, flags=re.S)
else:
    a = '  </header>\n'
    assert h.count(a) == 1
    h = h.replace(a, a + '\n' + block, 1)
    i = h.index('--font-display'); j = h.index('</style>', i); h = h[:j] + CSS + h[j:]
    a = '(function setupShare(){'
    assert h.count(a) == 1
    h = h.replace(a, JUMP + a, 1)
open(page, 'w', encoding='utf-8').write(h)
missing = [n for n in order if n not in pmids]
print(key, 'refs', len(order), 'words', words, 'no PMID:', missing)
