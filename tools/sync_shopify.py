"""Pull the product catalog from a Shopify store into tools/shopify_products.json, then rebuild the site.

Run:  python tools/sync_shopify.py yourstore.myshopify.com        (or your custom shop domain)
      python tools/build.py

Uses the store's public /products.json feed, so no API key is needed. The build then renders the Fit Shop
(server-side, so Google can index every product) and wires "Add to bag" to a Shopify cart permalink.
Re-run both commands whenever products change, or add them to a scheduled Netlify build hook.
"""
import json
import os
import re
import sys
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "shopify_products.json")


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def main(domain):
    domain = domain.replace("https://", "").replace("http://", "").strip("/")
    products, page = [], 1
    while True:
        url = f"https://{domain}/products.json?limit=250&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (WellBeing site sync)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            batch = json.load(r)["products"]
        if not batch:
            break
        for p in batch:
            products.append({
                "id": p["id"], "handle": p["handle"], "title": p["title"], "type": p.get("product_type", ""),
                "description": strip_tags(p.get("body_html"))[:500],
                "image": (p["images"][0]["src"] if p.get("images") else ""),
                "variants": [{"id": v["id"], "title": v["title"], "price": v["price"], "available": v.get("available", True)} for v in p["variants"]],
            })
        page += 1
    json.dump({"domain": domain, "currency": "USD", "products": products}, open(OUT, "w", encoding="utf-8"), indent=1)
    print(f"wrote {len(products)} products from {domain} -> {OUT}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
