/* WellBeing Fitness: interactive membership "Plan Studio".
   Prices come from the JSON block on the page (read from the Mindbody store at build time).
   Group tab: a classes-per-month slider prices every option at your pace and highlights the best value.
   Checkout hands off to the Mindbody store (or the contact form for packages that are booked with the team). */
(function () {
  "use strict";
  var root = document.querySelector("[data-plans]");
  var dataEl = document.getElementById("plans-data");
  if (!root || !dataEl) return;

  var D = JSON.parse(dataEl.textContent);
  var ticketEl = root.querySelector("[data-ticket]");
  var tabs = root.querySelectorAll("[data-tab]");
  var panels = root.querySelectorAll("[data-panel]");
  var state = { open: false, tab: "group", n: 4, sel: { group: null, private: null, coach: "coach" }, manual: { group: false, private: false } };

  function $(sel, ctx) { return (ctx || root).querySelector(sel); }
  function money(v, dp) { return "$" + Number(v).toLocaleString("en-US", { minimumFractionDigits: dp ? 2 : 0, maximumFractionDigits: dp ? 2 : 0 }); }
  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  function money2(v) { return money(v, Math.round(v * 100) % 100 !== 0); }

  /* ---------- pricing logic ---------- */
  function groupCost(p, n) {
    if (p.kind === "single") return { ok: true, cost: n * p.price };
    if (p.kind === "pack") {
      if (n * p.valid < p.size) return { ok: false, why: "At " + n + " a month you'd use about " + n * p.valid + " of " + p.size + " before it expires" };
      return { ok: true, cost: n * (p.price / p.size) };
    }
    if (n > p.cap) return { ok: false, why: "Covers up to " + p.cap + " classes a month" };
    return { ok: true, cost: p.price };
  }

  function paceLabel(n) {
    if (n <= 1) return "about once a month";
    if (n === 2) return "about every other week";
    if (n <= 4) return n === 4 ? "about once a week" : "about " + n + " a month";
    if (n <= 6) return "about 1–2 times a week";
    if (n <= 9) return "about twice a week";
    if (n <= 11) return "2–3 times a week";
    return "3 or more times a week";
  }

  /* ---------- render options ---------- */
  function renderGroup() {
    var n = state.n, list = D.group, rows = [], best = null;
    list.forEach(function (p) {
      var r = groupCost(p, n); r.p = p; rows.push(r);
      if (r.ok && (!best || r.cost < best.cost)) best = r;
    });
    if (!state.manual.group || !state.sel.group) state.sel.group = best.p.id;
    var max = Math.max.apply(null, rows.filter(function (r) { return r.ok; }).map(function (r) { return r.cost; }));
    var html = rows.map(function (r) {
      var p = r.p, on = state.sel.group === p.id;
      var meta = p.kind === "member" ? "Monthly" : (p.kind === "pack" ? "One-time pass" : "Pay as you go");
      var right = r.ok
        ? '<span class="opt__cost"><strong>' + money2(r.cost) + '</strong><small>/mo at your pace</small></span>'
        : '<span class="opt__cost opt__cost--off"><small>' + esc(r.why) + "</small></span>";
      var meter = r.ok ? '<span class="opt__meter" aria-hidden="true"><i style="width:' + Math.max(6, Math.round(r.cost / max * 100)) + '%"></i></span>' : "";
      return '<label class="opt' + (on ? " is-on" : "") + (r.ok ? "" : " is-off") + '">' +
        '<input type="radio" name="g-plan" value="' + p.id + '"' + (on ? " checked" : "") + '>' +
        '<span class="opt__dot" aria-hidden="true"></span>' +
        '<span class="opt__main"><span class="opt__name">' + esc(p.name) + (best.p.id === p.id ? '<em class="opt__badge">Best value</em>' : "") + '</span>' +
        '<span class="opt__sub">' + meta + " · " + (p.kind === "member" ? money(p.price) + "/mo" : money(p.price) + (p.size > 1 ? " for " + p.size : "")) + "</span>" + meter + "</span>" + right + "</label>";
    }).join("");
    $('[data-opts="group"]').innerHTML = '<legend class="sr">Choose a group-class plan</legend>' + html;
  }

  function renderPrivate(freq) {
    var list = D.private;
    if (freq) {
      var map = { weekly: "m4p", twice: "m8p", flex: "p12" };
      state.sel.private = map[freq]; state.manual.private = false; state.freq = freq;
      root.querySelectorAll("[data-freq]").forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-freq") === freq); });
    }
    if (!state.sel.private) state.sel.private = "m8p";
    var html = list.map(function (p) {
      var on = state.sel.private === p.id;
      var right = '<span class="opt__cost"><strong>' + money(p.price) + '</strong><small>' + (p.kind === "member" ? "/month" : (p.kind === "single" ? "one session" : "one-time")) + "</small></span>";
      return '<label class="opt' + (on ? " is-on" : "") + '"><input type="radio" name="p-plan" value="' + p.id + '"' + (on ? " checked" : "") + ">" +
        '<span class="opt__dot" aria-hidden="true"></span><span class="opt__main"><span class="opt__name">' + esc(p.name) + (p.badge ? '<em class="opt__badge">' + esc(p.badge) + "</em>" : "") + "</span>" +
        '<span class="opt__sub">' + esc(p.sub) + " · " + money(p.per) + " per session</span></span>" + right + "</label>";
    }).join("");
    $('[data-opts="private"]').innerHTML = '<legend class="sr">Choose a private training plan</legend>' + html;
  }

  function renderCoach() {
    var p = D.coach[0];
    $('[data-opts="coach"]').innerHTML = '<legend class="sr">Coaching program</legend><label class="opt is-on"><input type="radio" name="c-plan" value="coach" checked><span class="opt__dot" aria-hidden="true"></span>' +
      '<span class="opt__main"><span class="opt__name">' + esc(p.name) + '</span><span class="opt__sub">' + esc(p.sub) + " · " + p.months + " months</span></span>" +
      '<span class="opt__cost"><strong>' + money(p.price) + '</strong><small>/month for ' + p.months + "</small></span></label>";
  }

  /* ---------- ticket (summary + checkout) ---------- */
  function current() {
    var tab = state.tab, id = state.sel[tab];
    var list = tab === "group" ? D.group : (tab === "private" ? D.private : D.coach);
    return list.filter(function (p) { return p.id === id; })[0] || list[0];
  }

  function renderTicket() {
    var p = current(), tab = state.tab, price, unit, pace = "", fine;
    if (p.kind === "member") { price = money(p.price); unit = p.months ? "/month × " + p.months : "/month"; }
    else { price = money(p.price); unit = p.kind === "single" ? "one session" : "one-time"; }
    if (tab === "group") {
      var r = groupCost(p, state.n);
      if (r.ok) pace = "At " + state.n + (state.n === 12 ? "+" : "") + " class" + (state.n === 1 ? "" : "es") + " a month, that's about <strong>" + money2(r.cost / state.n) + " per class</strong> (" + money2(r.cost) + " a month).";
      else pace = '<span class="ticket__warn">' + esc(r.why) + ".</span>";
    } else if (tab === "private") {
      pace = "That works out to <strong>" + money(p.per) + " per session</strong>.";
    } else {
      pace = "Total over the program: <strong>" + money(p.price * p.months) + "</strong>.";
    }
    fine = p.kind === "member"
      ? "Auto-renewing. Contract terms are shown before you confirm."
      : "All sales on passes and training are final.";

    var cta, how;
    if (p.mb === "contact") {
      cta = '<a class="btn btn--light btn--lg btn--block" href="/contact/?interest=Private+Pilates">Request this package ' + arrow() + "</a>";
      how = "This package is booked with our team. Send a quick note and we'll set it up and schedule your first session.";
    } else {
      var url = D.links[p.link];
      cta = '<a class="btn btn--light btn--lg btn--block" href="' + url + '" target="_blank" rel="noopener">Continue on Mindbody ' + ext() + "</a>";
      how = "On Mindbody, choose <strong>" + esc(p.mbName) + "</strong>. You'll sign in or create an account to finish.";
    }
    var perks = (p.perks || []).map(function (x) { return "<li>" + check() + esc(x) + "</li>"; }).join("");

    ticketEl.innerHTML =
      '<div class="ticket"><div class="ticket__top"><img src="/images/logo-white.png" alt="WellBeing Fitness" width="150" height="36"><span class="ticket__tag">Your plan</span></div>' +
      '<h3 class="ticket__name">' + esc(p.name) + '</h3><p class="ticket__sub">' + esc(p.sub) + "</p>" +
      '<p class="ticket__price"><strong>' + price + "</strong><span>" + unit + "</span></p>" +
      (pace ? '<p class="ticket__pace">' + pace + "</p>" : "") +
      '<ul class="ticket__perks">' + perks + "</ul>" +
      '<div class="ticket__cut" aria-hidden="true"></div>' +
      cta + '<p class="ticket__how">' + how + '</p><p class="ticket__fine">' + fine + "</p>" +
      '<button class="ticket__toggle" type="button" aria-expanded="' + state.open + '"><span>' + (state.open ? "Hide details" : "Plan details") + "</span>" + chevron() + "</button></div>";
    ticketEl.firstChild.classList.toggle("is-open", state.open);
  }
  function chevron() { return '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'; }
  function arrow() { return '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'; }
  function ext() { return '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4 10 14M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>'; }
  function check() { return '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 12 5 5L20 6"/></svg>'; }

  /* ---------- wiring ---------- */
  function setTab(tab, focus) {
    state.tab = tab;
    tabs.forEach(function (t) {
      var on = t.getAttribute("data-tab") === tab;
      t.classList.toggle("is-on", on); t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    panels.forEach(function (p) { p.hidden = p.getAttribute("data-panel") !== tab; });
    renderTicket();
  }

  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { setTab(t.getAttribute("data-tab")); });
    t.addEventListener("keydown", function (e) {
      var k = e.key, j = k === "ArrowRight" ? i + 1 : k === "ArrowLeft" ? i - 1 : k === "Home" ? 0 : k === "End" ? tabs.length - 1 : null;
      if (j === null) return;
      e.preventDefault(); setTab(tabs[(j + tabs.length) % tabs.length].getAttribute("data-tab"), true);
    });
  });

  function keepFocus(name) { var c = root.querySelector('input[name="' + name + '"]:checked'); if (c) c.focus(); }

  ticketEl.addEventListener("click", function (e) {
    var t = e.target.closest(".ticket__toggle");
    if (!t) return;
    state.open = !state.open;
    renderTicket();
  });
  document.body.classList.add("has-fab");

  var dial = $("#dial"), dialN = $("[data-dial-n]"), dialSub = $("[data-dial-sub]");
  function paintDial() {
    var pct = (dial.value - dial.min) / (dial.max - dial.min) * 100;
    dial.style.setProperty("--pct", pct + "%");
    dialN.textContent = state.n === 12 ? "12+" : state.n;
    dialSub.textContent = paceLabel(state.n);
  }
  dial.addEventListener("input", function () {
    state.n = parseInt(dial.value, 10); state.manual.group = false;
    paintDial(); renderGroup(); renderTicket();
  });

  root.addEventListener("change", function (e) {
    var r = e.target;
    if (r.name === "g-plan") { state.sel.group = r.value; state.manual.group = true; renderGroup(); renderTicket(); keepFocus("g-plan"); }
    if (r.name === "p-plan") { state.sel.private = r.value; state.manual.private = true; renderPrivate(); renderTicket(); keepFocus("p-plan"); }
  });
  root.querySelectorAll("[data-freq]").forEach(function (b) {
    b.addEventListener("click", function () { renderPrivate(b.getAttribute("data-freq")); renderTicket(); });
  });

  // Deep links such as /memberships/?tab=private open straight to a tab
  var want = new URLSearchParams(location.search).get("tab");
  paintDial(); renderGroup(); renderPrivate("twice"); renderCoach();
  setTab(want && /^(group|private|coach)$/.test(want) ? want : "group");
})();
