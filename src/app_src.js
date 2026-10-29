(function () {
  var $ = function (id) { return document.getElementById(id); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // mobile menu
  var burger = $("burger"), mob = $("mobileNav");
  if (burger && mob) burger.addEventListener("click", function () {
    var open = mob.hidden; mob.hidden = !open; burger.setAttribute("aria-expanded", String(open));
  });

  // insight of the day
  var tips = [
    ["Security", "Your UPI PIN is only for sending money. Never for receiving it.", "If anyone asks you to scan a QR code or enter your PIN to receive money, it is a scam."],
    ["Security", "New number plus an urgent money request? Call the old number first.", "Scammers pretend to be family on WhatsApp. One call to the number you saved ends the scam."],
    ["AI", "Agree on a family code word.", "AI can copy a voice from a few seconds of audio. It can't copy a secret only your family knows."],
    ["Cloud", "Start with the official free learning paths.", "Microsoft Learn offers free beginner paths for Azure Fundamentals, with hands-on sandboxes."],
    ["Careers", "Show your work, not just your certificates.", "One small project on GitHub with a short write-up says more than a list of course badges."],
    ["Security", "Police never arrest anyone over a video call.", "There is no 'digital arrest'. Hang up, tell your family and report it."],
    ["Learning", "Teach what you learn.", "Explaining an idea to someone else is the fastest way to understand it yourself."]
  ];
  if ($("tipText")) {
    var ti = 0;
    var show = function (n) {
      ti = (n + tips.length) % tips.length;
      $("tipTopic").textContent = tips[ti][0]; $("tipText").textContent = tips[ti][1]; $("tipWhy").textContent = tips[ti][2];
      $("tipCount").textContent = String(ti + 1).padStart(2, "0") + " / " + String(tips.length).padStart(2, "0");
    };
    $("tipPrev").onclick = function () { show(ti - 1); };
    $("tipNext").onclick = function () { show(ti + 1); };
    show(Math.floor(Date.now() / 864e5) % tips.length);
  }

  // search
  function wireSearch(id) {
    var input = $(id), box = $(id + "-results");
    if (!input || !box || !window.GY_INDEX) return;
    var render = function () {
      var q = input.value.trim().toLowerCase();
      box.innerHTML = "";
      if (q.length < 2) { box.hidden = true; return; }
      var terms = q.split(/\s+/);
      var hits = window.GY_INDEX.map(function (r) {
        var hay = (r.t + " " + r.s).toLowerCase() + " " + r.k, score = 0;
        for (var i = 0; i < terms.length; i++) {
          if (hay.indexOf(terms[i]) < 0) return null;
          if (r.t.toLowerCase().indexOf(terms[i]) >= 0) score += 3; else score += 1;
        }
        return { r: r, s: score };
      }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 7);
      if (!hits.length) {
        var none = document.createElement("p"); none.className = "noresult";
        none.textContent = "No lessons match “" + input.value.trim() + "”. Try another word, like scam, cloud or prompts.";
        box.appendChild(none);
      }
      hits.forEach(function (h) {
        var a = document.createElement("a"); a.href = h.r.u;
        var b = document.createElement("b"); b.textContent = h.r.t;
        var s = document.createElement("span"); s.textContent = h.r.s;
        a.appendChild(b); a.appendChild(s); box.appendChild(a);
      });
      box.hidden = false;
    };
    input.addEventListener("input", render);
    input.addEventListener("focus", render);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { box.hidden = true; input.blur(); }
      if (e.key === "Enter") { var f = box.querySelector("a"); if (f) location.href = f.href; }
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search")) box.hidden = true; });
  }
  wireSearch("homeSearch"); wireSearch("pathSearch");

  // catalog filters
  var grid = $("pathGrid");
  if (grid) {
    var state = { topic: "all", level: "all" };
    var hash = decodeURIComponent(location.hash.slice(1));
    var apply = function () {
      var n = 0;
      grid.querySelectorAll(".pcard").forEach(function (c) {
        var ok = (state.topic === "all" || c.dataset.topic === state.topic) && (state.level === "all" || c.dataset.level === state.level);
        c.hidden = !ok; if (ok) n++;
      });
      $("pathCount").textContent = n + (n === 1 ? " path" : " paths");
      $("pathEmpty").hidden = n > 0;
    };
    [["fTopic", "topic"], ["fLevel", "level"]].forEach(function (g) {
      var wrap = $(g[0]);
      wrap.addEventListener("click", function (e) {
        var b = e.target.closest(".f"); if (!b) return;
        wrap.querySelectorAll(".f").forEach(function (x) { x.classList.toggle("on", x === b); });
        state[g[1]] = b.dataset.v; apply();
      });
      if (g[1] === "topic" && hash) {
        var match = wrap.querySelector('.f[data-v="' + hash.replace(/"/g, "") + '"]');
        if (match) match.click();
      }
    });
    apply();
  }

  // resource tabs
  var tabs = $("resTabs");
  if (tabs) tabs.addEventListener("click", function (e) {
    var b = e.target.closest(".f"); if (!b) return;
    tabs.querySelectorAll(".f").forEach(function (x) { x.classList.toggle("on", x === b); });
    document.querySelectorAll("#resList .row").forEach(function (r) { r.hidden = !(b.dataset.v === "all" || r.dataset.cat === b.dataset.v); });
  });

  // lesson progress
  var layout = document.querySelector(".path-layout");
  if (layout) {
    var slug = layout.dataset.path, total = +layout.dataset.total;
    var boxes = layout.querySelectorAll(".done input");
    var update = function () {
      var done = 0;
      boxes.forEach(function (b) {
        var link = layout.querySelector('.toc a[data-lesson="' + b.dataset.lesson + '"]');
        if (link) link.classList.toggle("is-done", b.checked);
        if (b.checked) done++;
      });
      $("progText").textContent = done + " / " + total;
      $("progBar").style.width = (done / total * 100) + "%";
    };
    boxes.forEach(function (b) {
      b.checked = store.get("gy:" + slug + ":" + b.dataset.lesson) === "1";
      b.addEventListener("change", function () { store.set("gy:" + slug + ":" + b.dataset.lesson, b.checked ? "1" : "0"); update(); });
    });
    update();
    // highlight current lesson
    if ("IntersectionObserver" in window) {
      var links = layout.querySelectorAll(".toc a");
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            var n = en.target.id.split("-")[1];
            links.forEach(function (l) { l.classList.toggle("is-current", l.dataset.lesson === n); });
          }
        });
      }, { rootMargin: "-30% 0px -60% 0px" });
      layout.querySelectorAll(".lesson").forEach(function (s) { io.observe(s); });
    }
  }
})();
