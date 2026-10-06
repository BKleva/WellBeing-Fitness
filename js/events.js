/* WellBeing Fitness: events list filters. Hides events that have already happened and filters by studio / type. */
(function () {
  "use strict";
  var root = document.querySelector("[data-events]");
  if (!root) return;
  var list = root.querySelector("[data-ev-list]");
  var empty = root.querySelector("[data-ev-empty]");
  var state = { loc: "all", kind: "all" };
  var t = new Date();
  var today = t.getFullYear() + "-" + String(t.getMonth() + 1).padStart(2, "0") + "-" + String(t.getDate()).padStart(2, "0");

  function apply() {
    var shown = 0, month = null;
    Array.prototype.forEach.call(list.children, function (el) {
      if (el.hasAttribute("data-month")) { month = el; month.hidden = true; return; }
      var ok = el.getAttribute("data-date") >= today &&
        (state.loc === "all" || el.getAttribute("data-loc") === state.loc) &&
        (state.kind === "all" || el.getAttribute("data-kind") === state.kind);
      el.hidden = !ok;
      el.classList.add("is-in");
      if (ok) { shown++; if (month) month.hidden = false; }
    });
    empty.hidden = shown > 0;
  }

  root.querySelectorAll("[data-seg]").forEach(function (g) {
    g.addEventListener("click", function (e) {
      var b = e.target.closest("[data-v]"); if (!b) return;
      state[g.getAttribute("data-seg")] = b.getAttribute("data-v");
      g.querySelectorAll("[data-v]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      apply();
    });
  });
  apply();
})();
