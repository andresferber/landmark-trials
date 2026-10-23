/* Landmark trials loader.
   Usage on any web page:
     <div id="landmark-trials"></div>
     <script src="https://andresferber.github.io/landmark-trials/loader.js"></script>
   Reads topics.json next to this file and builds an accordion; each topic's
   content (topics/<key>.html) is fetched the first time its section is opened.
   Order of sections = order in topics.json. Optional "group" adds a group label
   and colour (see GROUP_COLORS). */
(function () {
  var GROUP_COLORS = {
    Lymphoma: { main: "#0f6b6b", tint: "#e6f3f2" },
    Myeloma:  { main: "#5b3e96", tint: "#efeaf8" },
    _default: { main: "#2c4a8a", tint: "#e9eef8" }
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

  var css = [
    ".lta{--lta-fg:#1b2230;--lta-muted:#5d6677;--lta-rule:#dde1e8;",
    "font-family:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--lta-fg);text-align:left;display:flex;flex-direction:column;gap:10px}",
    ".lta *{box-sizing:border-box}",
    ".lta .lta-group{font:600 13px/1.4 'IBM Plex Sans',system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--g);margin:14px 2px 0;display:flex;align-items:center;gap:10px}",
    ".lta .lta-group:first-child{margin-top:0}",
    ".lta .lta-group::after{content:'';flex:1;height:2px;background:var(--g);opacity:.25}",
    ".lta .lta-sec{border:1px solid var(--lta-rule);border-left:6px solid var(--g);border-radius:10px;background:#fff}",
    ".lta button.lta-head{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:14px;width:100%;padding:14px 16px 14px 18px;cursor:pointer;background:var(--gt);color:var(--lta-fg);border-radius:0 9px 9px 0}",
    ".lta button.lta-head:hover{filter:brightness(.97)}",
    ".lta button.lta-head:focus-visible{outline:3px solid var(--g);outline-offset:-3px}",
    ".lta button.lta-head[aria-expanded='true']{position:sticky;top:0;z-index:30;border-radius:0 9px 0 0;border-bottom:1px solid var(--lta-rule);box-shadow:0 4px 10px -6px rgba(0,0,0,.25)}",
    ".lta .lta-title{flex:1;min-width:0;font-size:18px;font-weight:600;line-height:1.3;color:var(--lta-fg)}",
    ".lta .lta-meta{font:500 12px/1.4 'IBM Plex Mono',ui-monospace,Menlo,monospace;color:var(--lta-muted);white-space:nowrap}",
    ".lta .lta-icon{flex:none;width:38px;height:38px;border-radius:50%;background:var(--g);color:#fff;display:flex;align-items:center;justify-content:center;font:400 30px/1 system-ui,sans-serif;transition:transform .2s ease}",
    ".lta button.lta-head[aria-expanded='false'] .lta-icon{animation:lta-pulse 2.4s ease-in-out 1s 2}",
    "@keyframes lta-pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}",
    ".lta .lta-body .ltw{border-radius:0}",
    ".lta .lta-foot{display:flex;justify-content:center;padding:14px;border-top:1px solid var(--lta-rule);background:var(--gt);border-radius:0 0 9px 0}",
    ".lta button.lta-close{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:8px;padding:9px 18px;border-radius:999px;background:var(--g);color:#fff;font:600 14px/1 'IBM Plex Sans',system-ui,sans-serif}",
    ".lta button.lta-close:focus-visible{outline:3px solid var(--lta-fg);outline-offset:2px}",
    ".lta .lta-note{padding:18px;color:var(--lta-muted);font-size:14px}",
    "@media (max-width:560px){.lta .lta-meta{display:none}.lta .lta-title{font-size:16px}}",
    "@media (prefers-reduced-motion:reduce){.lta .lta-icon{animation:none!important;transition:none}}"
  ].join("");
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);

  mount.className = "lta";
  mount.innerHTML = '<div class="lta-note">Loading landmark trials…</div>';

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

  function build(data) {
    mount.innerHTML = "";
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
      sec.style.setProperty("--gt", col.tint);

      var head = document.createElement("button");
      head.type = "button";
      head.className = "lta-head";
      head.setAttribute("aria-expanded", "false");
      head.innerHTML = '<span class="lta-title"></span><span class="lta-meta"></span><span class="lta-icon" aria-hidden="true">+</span>';
      head.querySelector(".lta-title").textContent = t.title;
      head.querySelector(".lta-meta").textContent = [t.count, t.updated ? "updated " + fmtDate(t.updated) : ""].filter(Boolean).join(" · ");

      var body = document.createElement("div");
      body.className = "lta-body";
      body.hidden = true;
      var content = document.createElement("div");
      var foot = document.createElement("div");
      foot.className = "lta-foot";
      foot.innerHTML = '<button type="button" class="lta-close"><span aria-hidden="true">▲</span> Close ' + "section" + '</button>';
      body.appendChild(content);
      body.appendChild(foot);

      var loaded = false;
      function setOpen(open) {
        head.setAttribute("aria-expanded", String(open));
        head.querySelector(".lta-icon").textContent = open ? "−" : "+";
        body.hidden = !open;
        if (open && !loaded) {
          loaded = true;
          content.innerHTML = '<div class="lta-note">Loading…</div>';
          fetch(base + t.file + bust).then(function (r) {
            if (!r.ok) throw new Error(r.status);
            return r.text();
          }).then(function (html) {
            content.innerHTML = "";
            insertFragment(content, html);
          }).catch(function () {
            loaded = false;
            content.innerHTML = '<div class="lta-note">This section could not be loaded. Check your connection and open it again.</div>';
          });
        }
      }
      head.addEventListener("click", function () {
        var open = head.getAttribute("aria-expanded") === "true";
        setOpen(!open);
        if (open) sec.scrollIntoView({ block: "nearest" });
      });
      foot.querySelector(".lta-close").addEventListener("click", function () {
        setOpen(false);
        sec.scrollIntoView({ block: "start", behavior: "smooth" });
      });

      sec.appendChild(head);
      sec.appendChild(body);
      mount.appendChild(sec);
    });
    var h = (location.hash || "").replace("#", "");
    if (h) {
      var target = document.getElementById(h);
      if (target && target.classList.contains("lta-sec")) target.querySelector(".lta-head").click();
    }
  }

  fetch(base + "topics.json" + bust).then(function (r) { return r.json(); }).then(build).catch(function () {
    mount.innerHTML = '<div class="lta-note">The landmark trials could not be loaded. Please refresh the page.</div>';
  });
})();
