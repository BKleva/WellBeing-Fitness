/* WellBeing Fit Shop: lightweight bag that hands off to Shopify checkout via a cart permalink.
   Needs window.WB_SHOP = { domain: "yourstore.myshopify.com", currency: "USD" } (written by tools/build.py when
   tools/shopify_products.json exists). No API keys or tokens are required. */
(function () {
  "use strict";
  var cfg = window.WB_SHOP;
  if (!cfg || !cfg.domain) return;

  var KEY = "wb-bag-v1";
  var fmt = new Intl.NumberFormat("en-US", { style: "currency", currency: cfg.currency || "USD" });
  var bag = [];
  try { bag = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { bag = []; }

  var panel = document.getElementById("cart");
  var list = document.querySelector("[data-cart-list]");
  var empty = document.querySelector("[data-cart-empty]");
  var sub = document.querySelector("[data-cart-sub]");
  var count = document.querySelector("[data-cart-count]");
  var checkout = document.querySelector("[data-cart-checkout]");
  if (!panel || !list) return;

  function save() { try { localStorage.setItem(KEY, JSON.stringify(bag)); } catch (e) { /* storage blocked: bag lasts for this page view */ } }

  function render() {
    list.innerHTML = "";
    var total = 0, n = 0;
    bag.forEach(function (it, i) {
      total += it.price * it.qty; n += it.qty;
      var li = document.createElement("li");
      li.className = "cart__item";
      li.innerHTML =
        (it.image ? '<img src="' + it.image + '" alt="" width="72" height="72">' : "<span></span>") +
        "<div><h3></h3><small></small><div class=\"qty\"><button type=\"button\" aria-label=\"Decrease quantity\">−</button><span></span><button type=\"button\" aria-label=\"Increase quantity\">+</button></div></div>" +
        "<strong></strong>";
      li.querySelector("h3").textContent = it.title;
      li.querySelector("small").textContent = it.vtitle && it.vtitle !== "Default Title" ? it.vtitle : "";
      li.querySelector(".qty span").textContent = it.qty;
      li.querySelector("strong").textContent = fmt.format(it.price * it.qty);
      var btns = li.querySelectorAll(".qty button");
      btns[0].addEventListener("click", function () { change(i, -1); });
      btns[1].addEventListener("click", function () { change(i, 1); });
      list.appendChild(li);
    });
    empty.hidden = bag.length > 0;
    sub.textContent = fmt.format(total);
    count.textContent = n;
    count.hidden = n === 0;
    checkout.setAttribute("aria-disabled", String(bag.length === 0));
    checkout.style.opacity = bag.length ? "1" : ".5";
    checkout.style.pointerEvents = bag.length ? "auto" : "none";
    checkout.href = "https://" + cfg.domain + "/cart/" + bag.map(function (it) { return it.id + ":" + it.qty; }).join(",");
  }

  function change(i, d) {
    bag[i].qty += d;
    if (bag[i].qty <= 0) bag.splice(i, 1);
    save(); render();
  }

  function open() { panel.hidden = false; document.body.style.overflow = "hidden"; var c = panel.querySelector("[data-cart-close]"); if (c) c.focus(); }
  function close() { panel.hidden = true; document.body.style.overflow = ""; }

  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-cart-open]")) return open();
    if (e.target.closest("[data-cart-close]")) return close();
    var add = e.target.closest("[data-add]");
    if (!add) return;
    var card = add.closest(".product");
    var select = card.querySelector(".variant-select");
    var opt = select ? select.options[select.selectedIndex] : null;
    var id = opt ? opt.value : add.getAttribute("data-variant");
    var price = parseFloat(opt ? opt.getAttribute("data-price") : add.getAttribute("data-price"));
    var vtitle = opt ? opt.text.split(" · ")[0] : add.getAttribute("data-vtitle");
    var found = bag.filter(function (b) { return b.id === id; })[0];
    if (found) found.qty += 1;
    else bag.push({ id: id, title: card.getAttribute("data-title"), vtitle: vtitle, price: price, qty: 1, image: card.getAttribute("data-image") });
    save(); render(); open();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) close(); });

  // Update the displayed price when a different variant is chosen
  document.querySelectorAll(".variant-select").forEach(function (s) {
    s.addEventListener("change", function () {
      var price = s.options[s.selectedIndex].getAttribute("data-price");
      var el = s.closest(".product").querySelector(".price");
      if (el && price) el.textContent = fmt.format(parseFloat(price));
    });
  });

  document.body.classList.add("has-fab");
  render();
})();
