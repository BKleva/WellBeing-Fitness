/* WellBeing Fitness: native class schedule.
   Reads the schedule snapshot embedded in the page (pulled from the studio's Mindbody schedule), shows the next
   14 days, and hands each reservation off to Mindbody checkout. Days beyond the snapshot show the regular weekly
   lineup (the most recent complete week) and say so. */
(function () {
  "use strict";
  var root = document.querySelector("[data-schedule]");
  var dataEl = document.getElementById("sched-data");
  if (!root || !dataEl) return;

  var D = JSON.parse(dataEl.textContent);
  var classes = D.classes.map(function (a) { return { date: a[0], start: a[1], name: a[2], teacher: a[3], loc: a[4], min: a[5], id: a[6], tg: a[7], clsLoc: a[8] }; });
  var byDate = {};
  classes.forEach(function (c) { (byDate[c.date] = byDate[c.date] || []).push(c); });

  var DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var DOWL = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  var MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function fromIso(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function mdy(d) { return (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear(); }
  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }

  // regular weekly lineup = last 7 days of the snapshot, keyed by weekday
  var tpl = {};
  if (D.to) {
    var end = fromIso(D.to);
    for (var i = 0; i < 7; i++) {
      var day = addDays(end, -i), key = iso(day);
      (byDate[key] || []).forEach(function (c) { (tpl[day.getDay()] = tpl[day.getDay()] || []).push(c); });
    }
  }

  function kind(n) {
    n = n.toLowerCase();
    if (/pilates|barre/.test(n)) return "pilates";
    if (/sound|meditat|nidra/.test(n)) return "meditation";
    if (/strong|burn|build|core|total body|strength|fitness|bootcamp|hiit|conditioning|workday/.test(n)) return "fitness";
    return "yoga";
  }
  var KIND_LABEL = { yoga: "Yoga", pilates: "Pilates & Barre", fitness: "Fitness", meditation: "Meditation" };
  function easy(n) { return /gentle|slow|restor|foundation|beginner|all levels|mat\b|yin|pop-up|family|mindful/i.test(n); }

  function endTime(c) {
    var p = c.start.split(":"), m = +p[0] * 60 + +p[1] + (c.min || 0);
    return fmt(String(Math.floor(m / 60) % 24).padStart(2, "0") + ":" + String(m % 60).padStart(2, "0"));
  }
  function fmt(t) { var p = t.split(":"), h = +p[0], ap = h >= 12 ? "pm" : "am"; return ((h % 12) || 12) + ":" + p[1] + " " + ap; }

  function listFor(dayIso) {
    if (D.from && dayIso >= D.from && dayIso <= D.to) return { items: (byDate[dayIso] || []), actual: true };
    var t = (tpl[fromIso(dayIso).getDay()] || []).map(function (c) { var x = {}; for (var k in c) x[k] = c[k]; x.date = dayIso; x.id = ""; return x; });
    return { items: t, actual: false };
  }

  function reserveUrl(c) {
    var d = fromIso(c.date);
    if (c.id) return "https://clients.mindbodyonline.com/ASP/res_a.asp?tg=" + c.tg + "&classId=" + c.id + "&classDate=" + mdy(d) + "&clsLoc=" + c.clsLoc + "&studioid=729963";
    return D.mb + "&date=" + mdy(d);
  }

  var state = { day: null, loc: "all", type: "all" };
  var today = new Date(), todayIso = iso(today);
  var dayEls = [], days = [];
  for (var n = 0; n < 14; n++) days.push(addDays(today, n));

  var strip = root.querySelector("[data-days]");
  var list = root.querySelector("[data-list]");
  var title = root.querySelector("[data-day-title]");
  var note = root.querySelector("[data-note]");

  function nowMinutes() { return today.getHours() * 60 + today.getMinutes(); }
  function visibleFor(dayIso) {
    var l = listFor(dayIso), items = l.items.filter(function (c) {
      if (state.loc !== "all" && c.loc !== state.loc) return false;
      var k = kind(c.name);
      if (state.type === "easy") { if (!easy(c.name)) return false; } else if (state.type !== "all" && k !== state.type) return false;
      if (dayIso === todayIso) { var p = c.start.split(":"); if (+p[0] * 60 + +p[1] < nowMinutes()) return false; }
      return true;
    });
    return { items: items, actual: l.actual };
  }

  function buildStrip() {
    strip.innerHTML = "";
    days.forEach(function (d, i) {
      var key = iso(d), b = document.createElement("button");
      b.type = "button"; b.className = "day"; b.setAttribute("role", "tab"); b.setAttribute("data-day", key);
      b.innerHTML = "<small>" + (i === 0 ? "Today" : DOW[d.getDay()]) + "</small><strong>" + d.getDate() + "</strong><i></i>";
      b.addEventListener("click", function () { state.day = key; render(); });
      strip.appendChild(b); dayEls.push(b);
    });
  }

  function render() {
    var vis = visibleFor(state.day);
    dayEls.forEach(function (b) {
      var key = b.getAttribute("data-day"), c = visibleFor(key).items.length, on = key === state.day;
      b.classList.toggle("is-on", on); b.setAttribute("aria-selected", String(on)); b.classList.toggle("is-empty", c === 0);
      b.querySelector("i").textContent = c ? c + (c === 1 ? " class" : " classes") : "–";
      if (on && b.scrollIntoView) { var s = strip; s.scrollTo({ left: b.offsetLeft - (s.clientWidth - b.clientWidth) / 2, behavior: "smooth" }); }
    });
    var d = fromIso(state.day);
    title.textContent = DOWL[d.getDay()] + ", " + MON[d.getMonth()] + " " + d.getDate();
    if (!vis.items.length) {
      list.innerHTML = '<div class="sched__empty"><strong>No classes match on this day.</strong><p>Try another day, or switch to both studios and all styles.</p></div>';
    } else {
      list.innerHTML = vis.items.map(function (c) {
        var k = kind(c.name), t = D.teachers[c.teacher], who = c.teacher || "WellBeing team";
        var av = t && t.img ? '<img src="' + t.img + '" alt="" width="28" height="28" loading="lazy">' : '<b>' + esc((c.teacher || "W").charAt(0)) + "</b>";
        var name = t ? '<a href="/team/#' + t.slug + '">' + esc(who) + "</a>" : esc(who);
        var loc = c.loc || "Online";
        var p = fmt(c.start).split(" ");
        return '<article class="cls"><div class="cls__time"><strong>' + p[0] + "</strong><span>" + p[1] + '</span><small>' + (c.min || "") + (c.min ? " min" : "") + "</small></div>" +
          '<div class="cls__main"><h3>' + esc(c.name) + '</h3><div class="cls__tags"><span class="tag tag--' + k + '">' + KIND_LABEL[k] + "</span>" + (easy(c.name) ? '<span class="tag tag--easy">Beginner friendly</span>' : "") + "</div>" +
          '<div class="cls__who"><span class="av">' + av + "</span><span>" + name + '</span><span class="cls__loc"><i class="dot dot--' + (loc === "Westford" ? "w" : "g") + '"></i>' + esc(loc) + "</span><span class=\"cls__end\">until " + endTime(c) + "</span></div></div>" +
          '<a class="btn btn--sm cls__btn" href="' + reserveUrl(c) + '" target="_blank" rel="noopener">Reserve <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4 10 14M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg></a></article>';
      }).join("");
    }
    var gen = D.generated ? fromIso(D.generated) : null;
    note.innerHTML = (vis.actual ? "" : "This day shows our regular weekly lineup. ") +
      "Schedule synced " + (gen ? MON[gen.getMonth()] + " " + gen.getDate() : "recently") + ". Final availability is confirmed when you reserve on Mindbody. " +
      '<a href="' + D.mb + "&date=" + mdy(d) + '" target="_blank" rel="noopener">Open the live schedule</a>.';
  }

  root.querySelectorAll("[data-seg]").forEach(function (g) {
    g.addEventListener("click", function (e) {
      var b = e.target.closest("[data-v]"); if (!b) return;
      state[g.getAttribute("data-seg")] = b.getAttribute("data-v");
      g.querySelectorAll("[data-v]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      render();
    });
  });

  buildStrip();
  // open on the first day that still has classes
  for (var j = 0; j < days.length; j++) { if (visibleFor(iso(days[j])).items.length) { state.day = iso(days[j]); break; } }
  if (!state.day) state.day = todayIso;
  render();
})();
