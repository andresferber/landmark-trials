/* Landmark trials loader.
   Usage on any web page:
     <div id="landmark-trials"></div>
     <script src="https://USERNAME.github.io/landmark-trials/loader.js"></script>
   Reads topics.json next to this file and builds an accordion; each topic's
   content (topics/<key>.html) is fetched the first time its section is opened. */
(function () {
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
    ".lta{--lta-fg:#1b2230;--lta-muted:#5d6677;--lta-rule:#dde1e8;--lta-bg:#f6f7f9;--lta-accent:#2c4a8a;",
    "font-family:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--lta-fg);text-align:left;display:flex;flex-direction:column;gap:8px}",
    ".lta *{box-sizing:border-box}",
    ".lta .lta-sec{border:1px solid var(--lta-rule);border-radius:8px;background:#fff;overflow:hidden}",
    ".lta button.lta-head{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:12px;width:100%;padding:14px 18px;cursor:pointer;background:#fff;color:var(--lta-fg)}",
    ".lta button.lta-head:hover{background:var(--lta-bg)}",
    ".lta button.lta-head:focus-visible{outline:2px solid var(--lta-accent);outline-offset:-2px}",
    ".lta .lta-title{flex:1;min-width:0;font-size:17px;font-weight:600;line-height:1.3;color:var(--lta-fg)}",
    ".lta .lta-meta{font:500 12px/1.4 'IBM Plex Mono',ui-monospace,Menlo,monospace;color:var(--lta-muted);white-space:nowrap}",
    ".lta .lta-icon{font-size:20px;line-height:1;color:var(--lta-muted);width:20px;text-align:center}",
    ".lta .lta-body{border-top:1px solid var(--lta-rule)}",
    ".lta .lta-body .ltw{border-radius:0}",
    ".lta .lta-note{padding:18px;color:var(--lta-muted);font-size:14px}",
    "@media (max-width:560px){.lta .lta-meta{display:none}}"
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
    (data.topics || []).forEach(function (t) {
      var sec = document.createElement("section");
      sec.className = "lta-sec";
      sec.id = "topic-" + t.key;
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
      var loaded = false;
      head.addEventListener("click", function () {
        var open = head.getAttribute("aria-expanded") === "true";
        head.setAttribute("aria-expanded", String(!open));
        head.querySelector(".lta-icon").textContent = open ? "+" : "−";
        body.hidden = open;
        if (!open && !loaded) {
          loaded = true;
          body.innerHTML = '<div class="lta-note">Loading…</div>';
          fetch(base + t.file + bust).then(function (r) {
            if (!r.ok) throw new Error(r.status);
            return r.text();
          }).then(function (html) {
            body.innerHTML = "";
            insertFragment(body, html);
          }).catch(function () {
            loaded = false;
            body.innerHTML = '<div class="lta-note">This section could not be loaded. Check your connection and open it again.</div>';
          });
        }
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
