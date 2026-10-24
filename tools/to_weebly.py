#!/usr/bin/env python3
"""Convert a Landmark-trials artifact page into a Weebly-safe embed.
Usage: python3 to_weebly.py <page.html> <key> <out.html>
Works on the authored file or on the full page returned by an artifact read."""
import re, sys

def block_end(css, j):
    depth = 0; k = j
    while True:
        if css[k] == "{": depth += 1
        elif css[k] == "}":
            depth -= 1
            if depth == 0: return k
        k += 1

def strip_blocks(css, pat):
    out = []; i = 0
    while True:
        m = re.search(pat, css[i:])
        if not m: out.append(css[i:]); return "".join(out)
        s = i + m.start(); out.append(css[i:s])
        i = block_end(css, css.index("{", s)) + 1

def prefix_sel(sel):
    sel = sel.strip()
    if sel in (":root", "body"): return ".ltw"
    sel = re.sub(r"^footer\b", ".lt-foot", sel)
    sel = re.sub(r"^header\b", ".lt-head", sel)
    return ".ltw " + sel

def prefix_rules(css):
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sels, body = m.group(1), m.group(2)
        if "body::before" in sels or not sels.strip(): continue
        out.append(", ".join(prefix_sel(s) for s in sels.split(",")) + " {" + body + "}")
    return "\n".join(out)

def convert_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = strip_blocks(css, r"@media \(prefers-color-scheme: dark\)")
    css = strip_blocks(css, r':root\[data-theme="dark"\]')
    medias = []; rest = []; i = 0
    while True:
        m = re.search(r"@media[^{]+\{", css[i:])
        if not m: rest.append(css[i:]); break
        s = i + m.start(); rest.append(css[i:s])
        j = css.index("{", s); k = block_end(css, j)
        medias.append((css[s:j].strip(), css[j + 1:k])); i = k + 1
    out = prefix_rules("".join(rest))
    for head, inner in medias:
        out += "\n" + head + " {\n" + prefix_rules(inner) + "\n}"
    return out.replace("position: sticky;", "position: static;")

GUARD = """
.ltw { display: block; text-align: left; border-radius: 6px; }
.ltw, .ltw * { box-sizing: border-box; }
.ltw .lt-head h1 { color: var(--fg) !important; font-family: var(--font-display) !important; text-transform: none !important; background: none !important; }
.ltw h2.name { color: var(--fg) !important; font-family: var(--font-display) !important; text-transform: none !important; letter-spacing: normal !important; }
.ltw .eyebrow { color: var(--accent) !important; }
.ltw p, .ltw dd, .ltw li, .ltw span, .ltw div { font-family: var(--font-body); }
.ltw .lt-head p, .ltw .lt-foot, .ltw .credit { color: var(--muted) !important; }
.ltw .design, .ltw dd { color: var(--fg) !important; }
.ltw dd.qs { color: var(--accent) !important; }
.ltw dt, .ltw .yr, .ltw .phase, .ltw .count, .ltw .stats b, .ltw .rec .rk { color: var(--muted) !important; }
.ltw a { color: var(--accent) !important; }
.ltw ol.list, .ltw ol.list > li { list-style: none !important; margin-left: 0 !important; padding-left: 0 !important; background: none !important; }
.ltw .rec ul { list-style: disc !important; padding-left: 16px !important; }
.ltw button.chip { color: var(--fg) !important; background: var(--surface) !important; text-transform: none !important; box-shadow: none !important; height: auto !important; }
.ltw button.chip[aria-pressed="true"] { color: var(--bg) !important; background: var(--fg) !important; }
.ltw input[type="search"], .ltw select { color: var(--fg) !important; background: var(--surface) !important; height: auto !important; box-shadow: none !important; }
.ltw button.printbtn { color: var(--fg) !important; background: var(--surface) !important; text-transform: none !important; box-shadow: none !important; height: auto !important; }
.ltw .watch ul, .ltw .watch li { list-style: none !important; margin-left: 0 !important; padding-left: 0 !important; background: none !important; }
.ltw button.share { background: none !important; box-shadow: none !important; color: var(--muted) !important; height: auto !important; padding: 4px 6px !important; text-transform: none !important; min-width: 0 !important; }
.ltw .gloss dt { color: var(--fg) !important; text-transform: none !important; }
.ltw .gloss summary { color: var(--fg) !important; list-style: revert !important; }
.ltw a.report { color: var(--muted) !important; font-size: 12px !important; }
.ltw .reportall { margin: 12px 0 0; }
.ltw .moafree { color: var(--s-young) !important; }
.ltw .moa b { color: var(--fg) !important; }
.ltw .review .rv-title, .ltw .review h3 { color: var(--fg) !important; font-family: var(--font-display) !important; text-transform: none !important; letter-spacing: normal !important; }
.ltw .review > summary { list-style: none !important; }
.ltw .review .rv-body ul { list-style: disc !important; padding-left: 20px !important; }
.ltw .review .rv-refs { list-style: decimal !important; padding-left: 22px !important; }
.ltw .rv-tl ol, .ltw .rv-tl li { list-style: none !important; background: none !important; }
.ltw .review sup a { text-decoration: none !important; }
.ltw .sitedisc { color: var(--muted) !important; }
.ltw .review .rv-disc { color: var(--fg) !important; }
.ltw .watch h2 { color: var(--fg) !important; font-family: var(--font-display) !important; text-transform: none !important; }
"""

def main(src, key, dst):
    s = open(src, encoding="utf-8").read()
    fonts = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]+>', s).group(0)
    styles = re.findall(r"<style>(.*?)</style>", s, flags=re.S)
    css = next(c for c in styles if "--font-display" in c)
    scripts = re.findall(r"<script>(.*?)</script>", s, flags=re.S)
    js = next(x for x in scripts if "const T" in x and "function render" in x)
    start = s.index('<div class="wrap">')
    html = s[start:s.index("<script>", start)].replace("</style>", "")
    # Blocks marked as pilots stay off the website until Andres approves them.
    html = re.sub(r"<!--pilot-start-->.*?<!--pilot-end-->\n?", "", html, flags=re.S)
    # A review still marked as a pilot draft stays off the website until Andres approves it.
    if "Pilot draft, pending review" in html:
        html = re.sub(r'  <details class="review".*?</details>\n', "", html, flags=re.S)
    html = html.replace("<header>", '<div class="lt-head">').replace("</header>", "</div>")
    html = html.replace("<footer>", '<div class="lt-foot">').replace("</footer>", "</div>")
    for el in ["chips", "q", "sort", "count", "list"]:
        html = html.replace(f'id="{el}"', f'id="{key}-{el}"')
        js = js.replace(f'getElementById("{el}")', f'getElementById("{key}-{el}")')
    js = js.replace('"chip-"', f'"{key}-chip-"')
    out = (f"<!-- Landmark trials embed: {key}. Paste into a Weebly Embed Code element. -->\n"
           f'<link rel="preconnect" href="https://fonts.googleapis.com">\n{fonts}\n'
           f"<style>\n{convert_css(css)}\n{GUARD}\n</style>\n"
           f'<div class="ltw" id="lt-{key}">\n{html.strip()}\n</div>\n'
           f"<script>\n(function(){{\n{js}\n}})();\n</script>\n")
    open(dst, "w", encoding="utf-8").write(out)

if __name__ == "__main__":
    main(*sys.argv[1:4])
