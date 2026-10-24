/* Landmark trials loader.
   Usage on any web page:
     <div id="landmark-trials"></div>
     <script src="https://andresferber.github.io/landmark-trials/loader.js"></script>
   Reads topics.json (sections, in order), news.json ("What's new") and
   index.json (search across all topics) next to this file, and builds an
   accordion. Each topic's content (topics/<key>.html) is fetched the first
   time its section is opened. Deep links: #topic-<key> opens a section,
   #t-<key>-<trial-slug> opens it at one trial. */
(function () {
  var GROUP_COLORS = {
    Lymphoma: { main: "#0f6b6b", dark: "#0a5050", tint: "#eef7f6" },
    Myeloma:  { main: "#5b3e96", dark: "#46307a", tint: "#f3effa" },
    _default: { main: "#2c4a8a", dark: "#22396b", tint: "#eef2fa" }
  };

  var me = document.currentScript;
  var base = me && me.src ? me.src.replace(/[^\/]*(\?.*)?$/, "") : "";
  var mount = document.getElementById("landmark-trials");
  if (!mount) {
    mount = document.createElement("div");
    mount.id = "landmark-trials";
    if (me && me.parentNode) me.parentNode.insertBefore(mount, me);
    else document.body.appendChild(mount);
  }
  var bust = "?v=" + Math.floor(Date.now() / 600000);
  var CHEV = '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M5 7.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  var css = [
    ".lta{--lta-fg:#1b2230;--lta-muted:#5d6677;--lta-rule:#e1e4ea;",
    "font-family:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--lta-fg);text-align:left;display:flex;flex-direction:column;gap:12px}",
    ".lta *{box-sizing:border-box}",
    /* search */
    ".lta .lta-search{position:relative;margin-bottom:4px}",
    ".lta .lta-search input{all:unset;box-sizing:border-box;display:block;width:100%;font:400 16px/1.3 'IBM Plex Sans',system-ui,sans-serif;color:var(--lta-fg);background:#fff;border:1px solid var(--lta-rule);border-radius:12px;padding:13px 16px 13px 44px;box-shadow:0 1px 2px rgba(16,24,40,.05)}",
    ".lta .lta-search input:focus{border-color:#2c4a8a;box-shadow:0 0 0 3px rgba(44,74,138,.18)}",
    ".lta .lta-search .lta-mag{position:absolute;left:15px;top:50%;transform:translateY(-50%);color:var(--lta-muted);pointer-events:none}",
    ".lta .lta-results{margin-top:6px;background:#fff;border:1px solid var(--lta-rule);border-radius:12px;box-shadow:0 8px 24px -8px rgba(16,24,40,.18);max-height:420px;overflow:auto}",
    ".lta .lta-results[hidden]{display:none}",
    ".lta .lta-rg{font:600 11px/1 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--lta-muted);padding:12px 16px 6px}",
    ".lta button.lta-hit{all:unset;box-sizing:border-box;display:flex;gap:10px;align-items:baseline;width:100%;padding:8px 16px;cursor:pointer;font-size:14.5px;line-height:1.35}",
    ".lta button.lta-hit:hover,.lta button.lta-hit:focus-visible{background:#f2f4f8}",
    ".lta .lta-hit .y{font:500 12px 'IBM Plex Mono',ui-monospace,monospace;color:var(--lta-muted);flex:none;width:36px}",
    ".lta .lta-hit .t{font-weight:600}",
    ".lta .lta-hit .d{color:var(--lta-muted)}",
    ".lta .lta-hit .c{color:#8a5a12;font-size:12px;flex:none}",
    ".lta .lta-none{padding:14px 16px;color:var(--lta-muted);font-size:14px}",
    /* what's new */
    ".lta .lta-news{background:#fff;border:1px solid var(--lta-rule);border-radius:12px;padding:12px 16px;display:flex;flex-direction:column;gap:6px}",
    ".lta .lta-news h3{margin:0;font:600 12px/1 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:#2c4a8a}",
    ".lta .lta-news ul{margin:0;padding:0;list-style:none}",
    ".lta .lta-news li{margin:0;padding:3px 0;font-size:14px;line-height:1.4;list-style:none}",
    ".lta .lta-news .nd{font:500 12px 'IBM Plex Mono',ui-monospace,monospace;color:var(--lta-muted);margin-right:8px}",
    ".lta .lta-news button{all:unset;cursor:pointer;color:#2c4a8a;text-decoration:underline;text-underline-offset:2px}",
    /* groups and sections */
    ".lta .lta-group{font:600 13px/1.4 'IBM Plex Sans',system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--g);margin:16px 2px 0;display:flex;align-items:center;gap:10px}",
    ".lta .lta-group::after{content:'';flex:1;height:2px;background:var(--g);opacity:.2;border-radius:2px}",
    ".lta .lta-sec{border:1px solid var(--lta-rule);border-radius:14px;background:#fff;box-shadow:0 1px 2px rgba(16,24,40,.05);transition:box-shadow .2s ease}",
    ".lta .lta-sec:hover{box-shadow:0 6px 18px -8px rgba(16,24,40,.18)}",
    ".lta button.lta-head{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:16px;width:100%;padding:16px 16px 16px 20px;cursor:pointer;background:linear-gradient(90deg,var(--gt),#fff 70%);color:var(--lta-fg);border-radius:14px;border-left:5px solid var(--g)}",
    ".lta button.lta-head:focus-visible{outline:3px solid var(--g);outline-offset:2px}",
    ".lta button.lta-head[aria-expanded='true']{border-radius:14px 14px 0 0;border-bottom:1px solid var(--lta-rule)}",
    ".lta button.lta-head.lta-pinned{position:fixed;z-index:9999;border-radius:0;box-shadow:0 6px 14px -6px rgba(0,0,0,.35);background:linear-gradient(90deg,var(--gt),#fff 70%)}",
    ".lta .lta-tt{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}",
    ".lta .lta-title{font-size:18px;font-weight:600;line-height:1.3;color:var(--lta-fg)}",
    ".lta .lta-meta{font:500 12.5px/1.4 'IBM Plex Mono',ui-monospace,Menlo,monospace;color:var(--lta-muted)}",
    ".lta .lta-btn{flex:none;display:inline-flex;align-items:center;gap:6px;padding:9px 14px 9px 16px;border-radius:999px;background:var(--g);color:#fff;font:600 14px/1 'IBM Plex Sans',system-ui,sans-serif;box-shadow:0 2px 6px -2px var(--g);transition:background .15s ease,transform .15s ease}",
    ".lta button.lta-head:hover .lta-btn{background:var(--gd);transform:translateY(-1px)}",
    ".lta .lta-btn svg{transition:transform .25s ease}",
    ".lta button.lta-head[aria-expanded='true'] .lta-btn{background:#fff;color:var(--g);box-shadow:inset 0 0 0 1.5px var(--g)}",
    ".lta button.lta-head[aria-expanded='true'] .lta-btn svg{transform:rotate(180deg)}",
    ".lta button.lta-head[aria-expanded='false'] .lta-btn{animation:lta-nudge 2.6s ease-in-out 1.2s 1}",
    "@keyframes lta-nudge{0%,100%{transform:translateY(0)}30%{transform:translateY(2px)}60%{transform:translateY(-1px)}}",
    ".lta .lta-body .ltw{border-radius:0}",
    ".lta .lta-foot{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;padding:14px;border-top:1px solid var(--lta-rule);background:var(--gt);border-radius:0 0 14px 14px}",
    ".lta button.lta-close,.lta button.lta-print{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:8px;padding:9px 18px;border-radius:999px;font:600 14px/1 'IBM Plex Sans',system-ui,sans-serif}",
    ".lta button.lta-close{background:var(--g);color:#fff}",
    ".lta button.lta-print{background:#fff;color:var(--g);box-shadow:inset 0 0 0 1.5px var(--g)}",
    ".lta button.lta-close:focus-visible,.lta button.lta-print:focus-visible{outline:3px solid var(--lta-fg);outline-offset:2px}",
    ".lta .lta-note{padding:18px;color:var(--lta-muted);font-size:14px}",
    "@media (max-width:560px){.lta .lta-title{font-size:16px}.lta .lta-btn span{display:none}.lta .lta-btn{padding:9px}.lta button.lta-head{gap:10px;padding:14px 12px 14px 16px}}",
    "@media (prefers-reduced-motion:reduce){.lta *{animation:none!important;transition:none!important}}"
  ].join("");
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);

  mount.className = "lta";
  mount.innerHTML = '<div class="lta-note">Loading landmark trials…</div>';

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function insertFragment(target, html) {
    var tpl = document.createElement("template");
    tpl.innerHTML = html;
    var scripts = Array.prototype.slice.call(tpl.content.querySelectorAll("script"));
    scripts.forEach(function (s) { s.parentNode.removeChild(s); });
    target.appendChild(tpl.content);
    scripts.forEach(function (s) {
      var n = document.createElement("script");
      n.textContent = s.textContent;
      target.appendChild(n);
    });
  }

  function fmtDate(iso) {
    if (!iso) return "";
    var d = new Date(iso + "T12:00:00");
    return isNaN(d) ? iso : d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  }

  /* Pin the open section's title bar to the top while scrolling through it.
     Done in script (not CSS sticky) because site themes often wrap content in
     containers that disable CSS sticky. Allows for fixed site headers. */
  var heads = [];
  function siteHeaderOffset() {
    var off = 0;
    try {
      var xs = [window.innerWidth * 0.25, window.innerWidth * 0.5, window.innerWidth * 0.75];
      xs.forEach(function (x) {
        (document.elementsFromPoint(x, 2) || []).forEach(function (el) {
          if (mount.contains(el)) return;
          for (var n = el; n && n !== document.body; n = n.parentElement) {
            var pos = getComputedStyle(n).position;
            if (pos === "fixed" || pos === "sticky") {
              var r = n.getBoundingClientRect();
              if (r.top <= 2 && r.bottom > off && r.bottom < window.innerHeight * 0.4) off = r.bottom;
              break;
            }
          }
        });
      });
    } catch (e) {}
    return off;
  }
  var ticking = false;
  function updatePins() {
    ticking = false;
    var off = null;
    heads.forEach(function (o) {
      var open = o.head.getAttribute("aria-expanded") === "true";
      var sr = o.sec.getBoundingClientRect();
      if (off === null) off = siteHeaderOffset();
      var h = o.ph.offsetHeight || o.head.offsetHeight;
      var pin = open && sr.top < off && sr.bottom > off + h + 40;
      if (pin) {
        if (!o.pinned) {
          o.ph.style.height = o.head.offsetHeight + "px";
          o.ph.hidden = false;
          o.head.classList.add("lta-pinned");
          o.pinned = true;
        }
        o.head.style.top = off + "px";
        o.head.style.left = sr.left + "px";
        o.head.style.width = sr.width + "px";
      } else if (o.pinned) {
        o.head.classList.remove("lta-pinned");
        o.head.style.top = o.head.style.left = o.head.style.width = "";
        o.ph.hidden = true;
        o.pinned = false;
      }
    });
  }
  function requestPins() { if (!ticking) { ticking = true; requestAnimationFrame(updatePins); } }
  window.addEventListener("scroll", requestPins, { passive: true });
  window.addEventListener("resize", requestPins);
  document.addEventListener("scroll", requestPins, { passive: true, capture: true });

  /* Scroll an element to just below any fixed site header. */
  function scrollToEl(el, extra) {
    var y = el.getBoundingClientRect().top + window.pageYOffset - siteHeaderOffset() - (extra || 0);
    window.scrollTo(0, Math.max(0, y));
  }

  var sections = {};   /* key -> { open(), loaded: Promise, sec, title } */

  function goToTrial(key, slug) {
    var s = sections[key];
    if (!s) return;
    s.open(true).then(function () {
      var li = slug ? s.sec.querySelector('[data-trial="' + slug + '"]') : null;
      if (!li) { scrollToEl(s.sec); return; }
      var head = s.sec.querySelector(".lta-head");
      scrollToEl(li, (head ? head.offsetHeight : 0) + 12);
      li.classList.remove("flash"); void li.offsetWidth; li.classList.add("flash");
      requestPins();
    });
  }

  function buildSearch(index, topicsByKey) {
    var box = document.createElement("div");
    box.className = "lta-search";
    var n = index.length;
    box.innerHTML = '<svg class="lta-mag" viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 13l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
      '<input type="search" aria-label="Search all trials" placeholder="Search all ' + n + ' trials: drug, trial name, setting…">' +
      '<div class="lta-results" hidden role="listbox"></div>';
    var input = box.querySelector("input"), res = box.querySelector(".lta-results");
    function run() {
      var q = input.value.trim().toLowerCase();
      if (q.length < 2) { res.hidden = true; res.innerHTML = ""; return; }
      var terms = q.split(/\s+/);
      var hits = index.filter(function (t) { var hay = t.h; return terms.every(function (w) { return hay.indexOf(w) >= 0; }); });
      if (!hits.length) { res.innerHTML = '<div class="lta-none">No trials match “' + esc(input.value) + '”.</div>'; res.hidden = false; return; }
      var html = "", last = null;
      hits.slice(0, 40).forEach(function (t) {
        if (t.k !== last) { html += '<div class="lta-rg">' + esc((topicsByKey[t.k] || {}).title || t.k) + "</div>"; last = t.k; }
        html += '<button type="button" class="lta-hit" data-k="' + esc(t.k) + '" data-s="' + esc(t.s) + '"><span class="y">' + esc(t.y) + '</span><span><span class="t">' + esc(t.n) + "</span> " +
          '<span class="d">' + esc(t.d) + "</span></span>" + (t.c ? '<span class="c">★ Core</span>' : "") + "</button>";
      });
      if (hits.length > 40) html += '<div class="lta-none">' + (hits.length - 40) + " more; refine the search.</div>";
      res.innerHTML = html; res.hidden = false;
    }
    input.addEventListener("input", run);
    input.addEventListener("keydown", function (e) { if (e.key === "Escape") { input.value = ""; run(); } });
    res.addEventListener("click", function (e) {
      var b = e.target.closest(".lta-hit");
      if (!b) return;
      res.hidden = true;
      goToTrial(b.getAttribute("data-k"), b.getAttribute("data-s"));
    });
    return box;
  }

  function buildNews(news, topicsByKey) {
    var items = (news && news.items) || [];
    if (!items.length) return null;
    var box = document.createElement("div");
    box.className = "lta-news";
    var html = "<h3>What's new</h3><ul>";
    items.slice(0, 5).forEach(function (it, i) {
      var t = topicsByKey[it.key];
      html += '<li><span class="nd">' + esc(fmtDate(it.date)) + "</span>" + esc(it.text) +
        (t ? ' <button type="button" data-i="' + i + '">' + esc(t.title) + "</button>" : "") + "</li>";
    });
    box.innerHTML = html + "</ul>";
    box.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-i]");
      if (!b) return;
      var it = items[+b.getAttribute("data-i")];
      goToTrial(it.key, it.slug || null);
    });
    return box;
  }

  function build(data, news, index) {
    mount.innerHTML = "";
    var topicsByKey = {};
    (data.topics || []).forEach(function (t) { topicsByKey[t.key] = t; });
    if (index && index.length) mount.appendChild(buildSearch(index, topicsByKey));
    var nb = buildNews(news, topicsByKey);
    if (nb) mount.appendChild(nb);
    var coreCount = {};
    (index || []).forEach(function (t) { if (t.c) coreCount[t.k] = (coreCount[t.k] || 0) + 1; });

    var lastGroup = null;
    (data.topics || []).forEach(function (t) {
      var col = GROUP_COLORS[t.group] || GROUP_COLORS._default;
      if (t.group && t.group !== lastGroup) {
        var g = document.createElement("div");
        g.className = "lta-group";
        g.style.setProperty("--g", col.main);
        g.textContent = t.group;
        mount.appendChild(g);
        lastGroup = t.group;
      }
      var sec = document.createElement("section");
      sec.className = "lta-sec";
      sec.id = "topic-" + t.key;
      sec.style.setProperty("--g", col.main);
      sec.style.setProperty("--gd", col.dark);
      sec.style.setProperty("--gt", col.tint);

      var head = document.createElement("button");
      head.type = "button";
      head.className = "lta-head";
      head.setAttribute("aria-expanded", "false");
      head.innerHTML = '<span class="lta-tt"><span class="lta-title"></span><span class="lta-meta"></span></span><span class="lta-btn"><span>Open</span>' + CHEV + "</span>";
      head.querySelector(".lta-title").textContent = t.title;
      head.querySelector(".lta-meta").textContent = [t.count, coreCount[t.key] ? coreCount[t.key] + " core" : "", t.updated ? "updated " + fmtDate(t.updated) : ""].filter(Boolean).join(" · ");

      var body = document.createElement("div");
      body.className = "lta-body";
      body.hidden = true;
      var content = document.createElement("div");
      var foot = document.createElement("div");
      foot.className = "lta-foot";
      foot.innerHTML = '<button type="button" class="lta-print">Print / PDF</button><button type="button" class="lta-close"><span aria-hidden="true">▲</span> Close section</button>';
      body.appendChild(content);
      body.appendChild(foot);

      var loading = null;
      function load() {
        if (loading) return loading;
        content.innerHTML = '<div class="lta-note">Loading…</div>';
        loading = fetch(base + t.file + bust).then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.text();
        }).then(function (html) {
          content.innerHTML = "";
          insertFragment(content, html);
        }).catch(function () {
          loading = null;
          content.innerHTML = '<div class="lta-note">This section could not be loaded. Check your connection and open it again.</div>';
        });
        return loading;
      }
      function setOpen(open) {
        head.setAttribute("aria-expanded", String(open));
        head.querySelector(".lta-btn span").textContent = open ? "Close" : "Open";
        body.hidden = !open;
        requestPins();
        return open ? load() || Promise.resolve() : Promise.resolve();
      }
      function closeAndReturn() {
        setOpen(false);
        scrollToEl(sec, 8);
        requestPins();
      }
      head.addEventListener("click", function () {
        var open = head.getAttribute("aria-expanded") === "true";
        if (open) closeAndReturn();
        else setOpen(true);
      });
      foot.querySelector(".lta-close").addEventListener("click", closeAndReturn);
      foot.querySelector(".lta-print").addEventListener("click", function () {
        var b = content.querySelector(".printbtn");
        if (b) b.click();
      });

      var ph = document.createElement("div");
      ph.hidden = true;
      sec.appendChild(head);
      sec.appendChild(ph);
      sec.appendChild(body);
      heads.push({ head: head, sec: sec, body: body, ph: ph, pinned: false });
      sections[t.key] = { sec: sec, open: setOpen };
      mount.appendChild(sec);
    });

    var h = (location.hash || "").replace("#", "");
    var m = h.match(/^t-([a-z0-9]+)-(.+)$/);
    if (m && sections[m[1]]) goToTrial(m[1], m[2]);
    else if (/^topic-/.test(h) && sections[h.slice(6)]) goToTrial(h.slice(6), null);
  }

  function getJSON(name, fallback) {
    return fetch(base + name + bust).then(function (r) { if (!r.ok) throw 0; return r.json(); }).catch(function () { return fallback; });
  }
  Promise.all([getJSON("topics.json", null), getJSON("news.json", null), getJSON("index.json", [])]).then(function (v) {
    if (!v[0]) throw new Error("topics");
    build(v[0], v[1], v[2]);
  }).catch(function () {
    mount.innerHTML = '<div class="lta-note">The landmark trials could not be loaded. Please refresh the page.</div>';
  });
})();
