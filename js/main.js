/* WellBeing Fitness: navigation, reveal-on-scroll, filters, form prefill */
(function () {
  "use strict";

  var header = document.querySelector("[data-header]");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-stuck", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Mobile drawer
  var burger = document.querySelector("[data-burger]");
  var drawer = document.getElementById("drawer");
  if (burger && drawer) {
    var setDrawer = function (open) {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      drawer.hidden = !open;
      document.body.classList.toggle("menu-open", open);
      document.body.style.overflow = open ? "hidden" : "";
    };
    burger.addEventListener("click", function () { setDrawer(drawer.hidden); });
    drawer.addEventListener("click", function (e) { if (e.target.closest("a")) setDrawer(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1020) setDrawer(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !drawer.hidden) setDrawer(false); });
  }

  // Desktop dropdowns: click/tap toggle (hover and focus are handled in CSS)
  var menus = document.querySelectorAll(".has-menu");
  menus.forEach(function (li) {
    var btn = li.querySelector("[data-menu-btn]");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var open = !li.classList.contains("is-open");
      menus.forEach(function (m) { m.classList.remove("is-open"); var b = m.querySelector("[data-menu-btn]"); if (b) b.setAttribute("aria-expanded", "false"); });
      li.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-menu")) menus.forEach(function (m) { m.classList.remove("is-open"); var b = m.querySelector("[data-menu-btn]"); if (b) b.setAttribute("aria-expanded", "false"); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") menus.forEach(function (m) { m.classList.remove("is-open"); });
  });

  // Reveal on scroll
  document.documentElement.classList.add("js");
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
    // Safety net: never leave content hidden
    setTimeout(function () { reveals.forEach(function (el) { el.classList.add("is-in"); }); }, 4000);
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  // Filter chips (class styles, team, shop)
  document.querySelectorAll("[data-filter-group]").forEach(function (group) {
    var target = document.querySelector('[data-filter-target="' + group.getAttribute("data-filter-group") + '"]');
    if (!target) return;
    group.addEventListener("click", function (e) {
      var chip = e.target.closest("[data-filter]");
      if (!chip) return;
      var val = chip.getAttribute("data-filter");
      group.querySelectorAll(".chip").forEach(function (c) { c.classList.toggle("is-on", c === chip); });
      Array.prototype.forEach.call(target.children, function (item) {
        var tags = (item.getAttribute("data-tags") || item.getAttribute("data-group") || item.getAttribute("data-type") || "").split(" ");
        item.classList.toggle("is-hidden", val !== "all" && tags.indexOf(val) === -1);
        item.classList.add("is-in");
      });
    });
  });

  // Open a team bio when arriving via /team/#name
  var openBio = function () {
    if (!location.hash) return;
    var t = document.getElementById(location.hash.slice(1));
    if (t && t.classList.contains("person")) { var d = t.querySelector("details"); if (d) d.open = true; }
  };
  openBio();
  window.addEventListener("hashchange", openBio);

  // Prefill the "I'm interested in" select from ?interest=
  var select = document.querySelector("[data-interest]");
  if (select) {
    var want = new URLSearchParams(location.search).get("interest");
    if (want) {
      Array.prototype.forEach.call(select.options, function (o) { if (o.text === want) select.value = o.value; });
    }
  }
})();
