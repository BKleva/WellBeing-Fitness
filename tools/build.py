"""Static site generator for WellBeing Fitness (wellbeing-fitness.com).

Run:  python tools/build.py [--products tools/shopify_products.json]      (from the wellbeing-fitness folder)

Content lives in tools/data.py.  The Fit Shop reads tools/shopify_products.json (written by tools/sync_shopify.py)
when it exists; otherwise it shows the studio's current Bonfire merch with links out.
"""
import argparse
import datetime
import html
import json
import os
import glob
import hashlib
import re
from urllib.parse import quote_plus

from PIL import Image

from data import (CLASS_STYLES, HOME_FAQ, LOCATIONS, MB_LINK, PLANS_COACH, PLANS_GROUP, PLANS_PRIVATE, POLICY_FAQ, REFORMER_MONTHLY,
                  REFORMER_PACKS, REFORMER_SINGLE, SERVICES, TEAM, TEAM_FILTERS, TRIAL)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://www.wellbeing-fitness.com"
NAME = "WellBeing Fitness"
PHONE = "978-496-1846"
PHONE_TEL = "+19784961846"
EMAIL = "info@wellbeing-fitness.com"
TODAY = datetime.date.today().isoformat()

# Systems that live outside this static site -- change here if they move.
SCHEDULE_URL = "/schedule/"   # native schedule page; reservations hand off to Mindbody
MB_SCHEDULE = "https://clients.mindbodyonline.com/classic/ws?studioid=729963&stype=-7&sView=day&sLoc=0"
MB_EVENTS = "https://clients.mindbodyonline.com/asp/main_enroll.asp?studioid=729963&tabID=103"
ACCOUNT_URL = "https://clients.mindbodyonline.com/consumermyinfo/?studioid=729963&tabID=2"
BONFIRE_URL = "https://www.bonfire.com/store/wellbeing-fit-shop/"
SOCIAL = {
    "Instagram": "https://instagram.com/wellbeingfitnessteam",
    "Facebook": "https://www.facebook.com/WellBeingFitnessTeam",
    "LinkedIn": "https://www.linkedin.com/company/wellbeingfitness",
}

esc = html.escape
SVC = {s["slug"]: s for s in SERVICES}
TEAM_BY_NAME = {t["name"]: t for t in TEAM}


def qs(interest):
    return "?interest=" + quote_plus(interest) if interest else ""


def og(stem):
    """1200x630 JPG for social cards (Facebook/LinkedIn don't read WebP reliably)."""
    out = os.path.join(ROOT, "images", f"og-{stem}.jpg")
    if not os.path.exists(out):
        im = Image.open(os.path.join(ROOT, "images", f"{stem}-1400.webp")).convert("RGB")
        w, h = im.size
        nh = min(h, int(w * 630 / 1200))
        top = (h - nh) // 2
        im.crop((0, top, w, top + nh)).resize((1200, 630), Image.LANCZOS).save(out, quality=82)
    return f"/images/og-{stem}.jpg"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ------------------------------------------------------------------------------------------------
# Icons
# ------------------------------------------------------------------------------------------------
def _svg(inner, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')


ICON = {
    "arrow": _svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "up": _svg('<path d="M12 19V5M5 12l7-7 7 7"/>'),
    "arrow-up": _svg('<path d="M7 17 17 7M8 7h9v9"/>'),
    "phone": _svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    "mail": _svg('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'),
    "pin": _svg('<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    "calendar": _svg('<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
    "check": _svg('<path d="m4 12 5 5L20 6"/>'),
    "plus": _svg('<path d="M12 5v14M5 12h14"/>'),
    "minus": _svg('<path d="M5 12h14"/>'),
    "close": _svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    "bag": _svg('<path d="M6 7h12l1 13H5z"/><path d="M9 7a3 3 0 0 1 6 0"/>'),
    "sparkle": _svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>'),
    "dumbbell": _svg('<path d="M6.5 6.5v11M17.5 6.5v11M3.5 9v6M20.5 9v6M6.5 12h11"/>'),
    "ring": _svg('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.5"/>'),
    "leaf": _svg('<path d="M5 19C5 10 10 4 20 4c0 10-6 15-15 15z"/><path d="M5 19 13 11"/>'),
    "heart": _svg('<path d="M12 21s-8-5.2-8-11a4.6 4.6 0 0 1 8-3 4.6 4.6 0 0 1 8 3c0 5.800-8 11-8 11z"/>'),
    "shield": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
    "wave": _svg('<path d="M2 8c2.500 0 2.500-2 5-2s2.500 2 5 2 2.500-2 5-2 2.500 2 5 2M2 14c2.500 0 2.500-2 5-2s2.500 2 5 2 2.500-2 5-2 2.500 2 5 2M2 20c2.500 0 2.500-2 5-2s2.500 2 5 2 2.500-2 5-2 2.500 2 5 2"/>'),
    "briefcase": _svg('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>'),
    "lotus": _svg('<path d="M12 4c2.500 2.500 3.500 5 0 9-3.500-4-2.500-6.500 0-9zM12 13c-1-4.500-5-6-9-6 0 5 3 8.500 9 9 6-.5 9-4 9-9-4 0-8 1.500-9 6zM4 19h16"/>'),
    "sun": _svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.900 4.900l1.400 1.400M17.700 17.700l1.400 1.400M2 12h2M20 12h2M4.900 19.100l1.400-1.400M17.700 6.300l1.400-1.400"/>'),
    "people": _svg('<circle cx="9" cy="8" r="3.500"/><path d="M2.500 20c0-3.600 2.900-6 6.500-6s6.500 2.400 6.500 6"/><circle cx="17.500" cy="9" r="2.500"/><path d="M17 14c2.800 0 4.500 1.800 4.500 4.500"/>'),
    "instagram": _svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.500" cy="6.500" r=".8" fill="currentColor"/>'),
    "facebook": _svg('<path d="M14 8V6.500c0-.8.2-1.200 1.300-1.200H17V2.200C16.600 2.100 15.700 2 14.700 2 12.300 2 10.700 3.400 10.700 6v2H8v3.400h2.700V22H14V11.400h2.600L17 8z"/>'),
    "linkedin": _svg('<path d="M6.500 9v11M6.500 4.500v.1M11 20v-6.500c0-2 1.200-3.500 3.200-3.500s3.300 1.400 3.300 3.500V20M11 9v11"/>'),
    "external": _svg('<path d="M14 4h6v6M20 4 10 14M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
}


# ------------------------------------------------------------------------------------------------
# Images
# ------------------------------------------------------------------------------------------------
_dims = {}


def _dim(fname):
    if fname not in _dims:
        _dims[fname] = Image.open(os.path.join(ROOT, "images", fname)).size
    return _dims[fname]


def pic(stem, alt, sizes="100vw", cls="", eager=False, style=""):
    """<img> with srcset for scene images (-800/-1400) or a single file for portraits/merch."""
    big = os.path.join(ROOT, "images", stem + "-1400.webp")
    attrs = f'class="{cls}" ' if cls else ""
    attrs += f'alt="{esc(alt)}" '
    attrs += 'fetchpriority="high" ' if eager else 'loading="lazy" decoding="async" '
    if style:
        attrs += f'style="{style}" '
    if os.path.exists(big):
        w, h = _dim(stem + "-1400.webp")
        w8, _ = _dim(stem + "-800.webp")
        return (f'<img src="/images/{stem}-1400.webp" srcset="/images/{stem}-800.webp {w8}w, /images/{stem}-1400.webp {w}w" '
                f'sizes="{sizes}" width="{w}" height="{h}" {attrs}>')
    w, h = _dim(stem + ".webp")
    return f'<img src="/images/{stem}.webp" width="{w}" height="{h}" {attrs}>'


# ------------------------------------------------------------------------------------------------
# Layout
# ------------------------------------------------------------------------------------------------
def head(title, desc, path, og_img="/images/og-card.jpg", schema=None, noindex=False, preload=None):
    url = SITE + path
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f7f2ea">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="US-MA">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
{pre}
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="/css/styles.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active=""):
    def link(href, label, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'

    mega = "".join(
        f'<a class="mega__item" href="/{s["slug"]}/">{ICON[s["icon"]]}<span><strong>{esc(s["nav"])}</strong>'
        f'<small>{esc(s["locs"])}</small></span></a>' for s in SERVICES)
    drawer_services = "".join(f'<a href="/{s["slug"]}/">{esc(s["nav"])}</a>' for s in SERVICES)
    return f"""<header class="site-header" data-header>
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="{NAME} home"><img src="/images/logo-navy.png" alt="{NAME}" width="168" height="40"></a>
    <nav class="primary" aria-label="Primary">
      <ul>
        {link("/classes/", "Classes", "classes")}
        <li class="has-menu"><button type="button" aria-expanded="false" aria-controls="menu-services" data-menu-btn{' aria-current="true"' if active == "services" else ""}>Services {_svg('<path d="m6 9 6 6 6-6"/>', "ico ico--sm")}</button>
          <div class="mega" id="menu-services"><div class="mega__grid">{mega}</div>
          <a class="mega__foot" href="/contact/">Not sure where to start? <strong>Book a free consultation</strong> {ICON["arrow"]}</a></div></li>
        {link("/team/", "Team", "team")}
        <li class="has-menu"><button type="button" aria-expanded="false" aria-controls="menu-studios" data-menu-btn{' aria-current="true"' if active == "locations" else ""}>Studios {_svg('<path d="m6 9 6 6 6-6"/>', "ico ico--sm")}</button>
          <div class="mega mega--sm" id="menu-studios"><div class="mega__grid mega__grid--one">
            <a class="mega__item" href="/westford/">{ICON["pin"]}<span><strong>Westford</strong><small>203 B Littleton Rd</small></span></a>
            <a class="mega__item" href="/groton/">{ICON["pin"]}<span><strong>Groton</strong><small>134 Main St</small></span></a>
          </div></div></li>
        {link("/memberships/", "Memberships", "memberships")}
        {link("/events/", "Events", "events")}
        {link("/shop/", "Shop", "shop")}
      </ul>
    </nav>
    <div class="bar__cta">
      <a class="btn btn--sm" href="{SCHEDULE_URL}">Reserve a class</a>
    </div>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer" data-burger><span></span><span></span></button>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <nav aria-label="Mobile">
    <a href="/classes/">Classes</a>
    <details><summary>Services</summary><div class="drawer__sub">{drawer_services}</div></details>
    <a href="/team/">Our Team</a>
    <details><summary>Studios</summary><div class="drawer__sub"><a href="/westford/">Westford</a><a href="/groton/">Groton</a></div></details>
    <a href="/memberships/">Memberships</a>
    <a href="/events/">Events</a>
    <a href="/shop/">Shop</a>
    <a href="/contact/">Contact</a>
  </nav>
  <div class="drawer__cta">
    <a class="btn" href="{SCHEDULE_URL}">Reserve a class</a>
    <a class="drawer__tel" href="tel:{PHONE_TEL}">{ICON["phone"]} {PHONE}</a>
  </div>
</div>
<main id="main">
"""


def footer():
    svc = " · ".join(f'<a href="/{s["slug"]}/">{esc(s["nav"])}</a>' for s in SERVICES)
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICON[n.lower()]}</a>' for n, u in SOCIAL.items())
    return f"""</main>
<footer class="site-footer">
  <div class="wrap footer__main">
    <div class="footer__brand">
      <img src="/images/logo-white.png" alt="{NAME}" width="168" height="40" loading="lazy">
      <p>Yoga, Pilates, Barre, training, nutrition and recovery in Westford and Groton, MA.</p>
      <div class="social">{soc}</div>
    </div>
    <div class="footer__cols">
      <div><h3>Studios</h3>
        <address><a href="/westford/"><strong>Westford</strong></a><br>203 B Littleton Rd, 01886</address>
        <address><a href="/groton/"><strong>Groton</strong></a><br>134 Main St, 01450</address></div>
      <div><h3>Contact</h3><ul>
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{ACCOUNT_URL}" target="_blank" rel="noopener">Member login</a></li></ul></div>
      <div><h3>Explore</h3><ul>
        <li><a href="/schedule/">Class schedule</a></li><li><a href="/memberships/">Memberships</a></li><li><a href="/team/">Our team</a></li>
        <li><a href="/events/">Events</a></li><li><a href="/shop/">Fit Shop</a></li><li><a href="/policies/">Policies &amp; FAQ</a></li></ul></div>
    </div>
  </div>
  <div class="wrap footer__base"><span>© {datetime.date.today().year} {NAME}</span>
    <a class="credit" href="https://shoreworksnj.com" target="_blank" rel="noopener">Site by <img src="/images/shoreworks-logo-light.png" width="600" height="97" alt="Shore Works" loading="lazy"></a></div>
</footer>
<button class="totop" type="button" aria-label="Back to top" data-totop>{ICON["up"]}</button>
<script src="/js/main.js" defer></script>
"""


def shop_scripts(cfg):
    return f'<script>window.WB_SHOP={json.dumps(cfg)};</script><script src="/js/shop.js" defer></script>'


def close():
    return "</body>\n</html>\n"


def asset_version():
    h = hashlib.md5()
    for f in sorted(glob.glob(os.path.join(ROOT, "css", "*.css")) + glob.glob(os.path.join(ROOT, "js", "*.js"))):
        h.update(open(f, "rb").read())
    return h.hexdigest()[:8]


def write(path, content):
    content = re.sub(r'((?:href|src)=")(/(?:css|js)/[\w.-]+\.(?:css|js))(")', rf"\1\2?v={asset_version()}\3", content)
    full = os.path.join(ROOT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


# ------------------------------------------------------------------------------------------------
# Reusable blocks
# ------------------------------------------------------------------------------------------------
def crumbs(items):
    """items: [(label, path)] ending with the current page. Returns (html, jsonld)."""
    ld = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    lis = []
    for i, (label, path) in enumerate(items, start=2):
        ld.append({"@type": "ListItem", "position": i, "name": label, "item": SITE + path})
        if i - 2 < len(items) - 1:
            lis.append(f'<li><a href="{path}">{esc(label)}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
    h = f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>{"".join(lis)}</ol></nav>'
    return h, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld}


def faq_block(items, heading="Good to know", intro=""):
    rows = "".join(f'<details class="faq__item"><summary>{esc(q)}<span class="faq__icon">{ICON["plus"]}</span></summary><div class="faq__a"><p>{esc(a)}</p></div></details>' for q, a in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return (f'<section class="section faq"><div class="wrap faq__wrap"><div class="faq__head reveal"><p class="eyebrow">FAQ</p>'
            f'<h2>{heading}</h2>{f"<p>{intro}</p>" if intro else ""}</div><div class="faq__list reveal">{rows}</div></div></section>'), ld


def consult_form(form_id="consult", interest="", compact=False, heading=True):
    interests = ["Not sure yet", "Personal Training", "Private Pilates", "Yoga & group classes", "Nutrition & Health Coaching", "Women's Wellness",
                 "Oncology Exercise", "Recovery · Reiki · Physical Therapy", "Corporate Wellness", "Private Event", "Something else"]
    opts = "".join(f'<option{" selected" if o == interest else ""}>{esc(o)}</option>' for o in interests)
    msg = "" if compact else '<label class="field field--full"><span>Anything we should know?</span><textarea name="message" rows="4" placeholder="Goals, injuries, schedule, questions…"></textarea></label>'
    return f"""<form class="form" name="{form_id}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field" data-interest-form>
  <input type="hidden" name="form-name" value="{form_id}">
  <p class="hp"><label>Don't fill this out <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <div class="form__grid">
    <label class="field"><span>Your name</span><input name="name" required autocomplete="name" placeholder="Jane Doe"></label>
    <label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email" placeholder="you@email.com"></label>
    <label class="field"><span>Phone <em>(optional)</em></span><input type="tel" name="phone" autocomplete="tel" placeholder="978-555-0123"></label>
    <label class="field"><span>I'm interested in</span><select name="interest" data-interest>{opts}</select></label>
    <label class="field field--full"><span>Preferred studio</span>
      <span class="radios"><label><input type="radio" name="studio" value="Westford"> Westford</label><label><input type="radio" name="studio" value="Groton"> Groton</label><label><input type="radio" name="studio" value="No preference" checked> No preference</label></span></label>
    {msg}
  </div>
  <button class="btn btn--lg" type="submit">Request my free consultation {ICON["arrow"]}</button>
  <p class="form__note">We'll reply within one business day. Prefer to talk? Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
</form>"""


def cta_band(title="Ready to feel your best?", text="Book a free consultation and we'll help you find the right starting point, whether that's a class, a coach or a custom plan.", interest=""):
    q = qs(interest)
    return f"""<section class="cta-band"><div class="wrap cta-band__inner reveal">
  <div><p class="eyebrow eyebrow--light">Start here</p><h2>{title}</h2><p>{text}</p></div>
  <div class="cta-band__btns"><a class="btn btn--light btn--lg" href="/contact/{q}">Free consultation {ICON["arrow"]}</a>
  <a class="btn btn--outline-light btn--lg" href="{SCHEDULE_URL}">Browse classes</a></div></div></section>"""


def team_card(t, compact=False):
    slug = slugify(t["name"].split(",")[0])
    img = pic("team-" + t["img"], f'{t["name"]}, {t["role"]} at WellBeing Fitness', "(min-width:900px) 22vw, 46vw") if t["img"] else \
        f'<div class="monogram" aria-hidden="true">{esc(t["name"][0])}</div>'
    if compact:
        return f'<a class="mini" href="/team/#{slug}"><span class="mini__img">{img}</span><strong>{esc(t["name"].split(",")[0])}</strong><small>{esc(t["role"].split(" · ")[0])}</small></a>'
    bio = "".join(f"<p>{esc(p)}</p>" for p in t["bio"])
    return f"""<article class="person reveal" id="{slug}" data-tags="{' '.join(t['tags'])}">
  <div class="person__img">{img}</div>
  <div class="person__body"><h3>{esc(t['name'])}</h3><p class="person__role">{esc(t['role'])}</p><p>{esc(t['short'])}</p>
  <details class="person__more"><summary>Read full bio <span>{ICON["plus"]}</span></summary><div>{bio}</div></details></div></article>"""


def service_card(s, feature=False):
    cls = " card--feature" if feature else ""
    return f"""<a class="card card--text{cls} reveal" href="/{s['slug']}/">
  <span class="card__ico">{ICON[s['icon']]}</span><h3>{esc(s['card'])}</h3><p>{esc(s['short'])}</p>
  <span class="card__more">Explore {ICON["arrow"]}</span></a>"""


def org_ld():
    locs = []
    for l in LOCATIONS:
        locs.append({"@type": "HealthClub", "@id": f"{SITE}/{l['slug']}/#club", "name": f"WellBeing Fitness {l['name']}",
                     "url": f"{SITE}/{l['slug']}/", "telephone": "+1" + PHONE.replace("-", ""), "email": EMAIL,
                     "image": f"{SITE}/images/{l['img']}-1400.webp", "priceRange": "$$",
                     "address": {"@type": "PostalAddress", "streetAddress": l["street"], "addressLocality": l["city"],
                                 "addressRegion": l["state"], "postalCode": l["zip"], "addressCountry": "US"},
                     "parentOrganization": {"@id": SITE + "/#org"}})
    return locs


# ------------------------------------------------------------------------------------------------
# Pages
# ------------------------------------------------------------------------------------------------
def page_home(shop):
    title = "WellBeing Fitness | Yoga, Pilates & Training in Westford, MA"
    desc = "A whole-life wellness studio in Westford & Groton, MA: yoga, Pilates, Barre, personal training, nutrition and recovery for every age. Free consultation."
    org = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
           "logo": SITE + "/images/logo-navy.png", "image": SITE + "/images/og-card.jpg", "telephone": "+1" + PHONE.replace("-", ""),
           "email": EMAIL, "founder": {"@type": "Person", "name": "Scott Cassa"}, "sameAs": list(SOCIAL.values()),
           "description": desc}
    site = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME, "publisher": {"@id": SITE + "/#org"}}
    h = head(title, desc, "/", schema=[org, site] + [dict(l, **{"@context": "https://schema.org"}) for l in org_ld()])
    h += header()

    classes_card = f"""<a class="card card--text card--feature card--classes reveal" href="/classes/">
  <span class="card__ico">{ICON["lotus"]}</span><h3>Yoga, Pilates &amp; Barre Classes</h3>
  <p>Expertly taught group classes in Westford and Groton, from gentle and restorative to dynamic vinyasa and barre cardio.</p>
  <span class="card__more">See classes &amp; schedule {ICON["arrow"]}</span></a>"""
    cards = classes_card + "".join(service_card(s) for s in SERVICES)

    stud = ""
    for l in LOCATIONS:
        stud += f"""<article class="studio reveal"><a class="studio__img" href="/{l['slug']}/">{pic(l['img'], f"WellBeing Fitness {l['name']} studio exterior", "(min-width:900px) 50vw, 100vw")}</a>
  <div class="studio__body"><p class="eyebrow">{esc(l['name'])}, MA</p><h3>{esc(l['street'])}</h3><p>{esc(l['near'])}.</p>
  <ul class="tags">{"".join(f"<li>{esc(x)}</li>" for x in l['services'][:5])}</ul>
  <div class="studio__links"><a class="link" href="/{l['slug']}/">Studio details {ICON["arrow"]}</a>
  <a class="link" href="https://www.google.com/maps/dir/?api=1&destination={l['map_q']}" target="_blank" rel="noopener">Get directions {ICON["external"]}</a></div></div></article>"""

    body = f"""
<section class="hero hero--text">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="eyebrow reveal">Westford &amp; Groton, Massachusetts</p>
      <h1 class="reveal">A <em>whole-life</em> approach to feeling your best.</h1>
      <p class="lede reveal">Yoga, Pilates, Barre, personal training, nutrition and recovery under one roof. Guided by a team of specialists who see you as an individual, at any age and any stage of your health journey.</p>
      <div class="hero__btns reveal"><a class="btn btn--lg" href="{SCHEDULE_URL}">Register for a class {ICON["arrow"]}</a>
      <a class="btn btn--ghost btn--lg" href="/contact/">Free consultation</a></div>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap"><div class="section__head reveal"><p class="eyebrow">What we offer</p><h2>Everything you need for a <em>lifestyle of good health.</em></h2></div>
  <div class="cards">{cards}</div></div>
</section>

<section class="section section--sand">
  <div class="wrap split">
    <div class="split__media reveal"><div class="plainimg">{pic("studio-yoga-light", "Bright WellBeing yoga room with mats and props", "(min-width:900px) 40vw, 90vw")}</div></div>
    <div class="split__copy reveal"><p class="eyebrow">Our philosophy</p><h2>Wellness that fits your <em>whole life.</em></h2>
    <p>Founded by Scott Cassa, a fitness trainer for more than twenty years, WellBeing Fitness grew from a simple idea: every client is an individual with their own goals, interests, health history and fitness level. That's the key to results that last a lifetime.</p>
    <a class="btn" href="/team/">Meet the team {ICON["arrow"]}</a></div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap"><div class="section__head reveal"><p class="eyebrow">Our studios</p><h2>Two welcoming homes for <em>your practice.</em></h2></div>
  <div class="studios">{stud}</div></div>
</section>

<section class="section section--forest radiance" id="radiance">
  <div class="wrap split split--rev">
    <div class="split__media reveal"><div class="poster">{pic("radiance-poster", "Radiance Wellness Living announcement poster: cold plunge, red light therapy, saunas, hyperbaric and compression, coming soon to 100 Boston Rd, Groton", "(min-width:900px) 34vw, 80vw")}</div></div>
    <div class="split__copy reveal"><p class="eyebrow eyebrow--light">Coming soon to Groton</p><h2>Radiance <em>Wellness Living</em></h2>
    <p>A new recovery and wellness experience designed to help you restore, recharge and feel your best, at 100 Boston Rd in Groton.</p>
    <ul class="ticks"><li>{ICON["check"]}Cold plunge</li><li>{ICON["check"]}Red light therapy</li><li>{ICON["check"]}Saunas</li><li>{ICON["check"]}Hyperbaric</li><li>{ICON["check"]}Compression &amp; more</li></ul>
    <a class="btn btn--light" href="/recovery/#radiance">Be the first to know {ICON["arrow"]}</a></div>
  </div>
</section>

<section class="section consult" id="consult">
  <div class="wrap consult__grid">
    <div class="reveal"><p class="eyebrow">Free consultation</p><h2>Let's find your <em>starting point.</em></h2>
    <p>Tell us a little about your goals and we'll help you choose the right class, coach or program. No pressure, just a conversation.</p>
    <ul class="contact-list"><li>{ICON["phone"]}<a href="tel:{PHONE_TEL}">{PHONE}</a></li><li>{ICON["mail"]}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ICON["pin"]}<span>203 B Littleton Rd, Westford · 134 Main St, Groton</span></li></ul></div>
    <div class="consult__card reveal">{consult_form("home-consult", compact=True)}</div>
  </div>
</section>
"""
    scripts = shop_scripts(shop["cfg"]) if shop["mode"] == "shopify" else ""
    write("/", h + body + footer() + scripts + close())


def page_service(s):
    path = f"/{s['slug']}/"
    cr, cr_ld = crumbs([("Services", "/#services"), (s["nav"], path)])
    faq, faq_ld = faq_block(s["faq"], f"{s['card']}: common questions")
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["card"], "serviceType": s["card"], "description": s["desc"],
              "url": SITE + path, "provider": {"@id": SITE + "/#org"},
              "areaServed": [{"@type": "City", "name": "Westford, MA"}, {"@type": "City", "name": "Groton, MA"}]}
    h = head(s["title"], s["desc"], path, og_img=og(s["img"]), schema=[svc_ld, cr_ld, faq_ld], preload=f"/images/{s['img']}-800.webp")
    h += header("services")

    facts = "".join(f"<div><small>{esc(k)}</small><strong>{esc(v)}</strong></div>" for k, v in s["facts"])
    q = qs(s["interest"])

    secs = ""
    for sh, paras in s["sections"]:
        secs += f'<section class="prose reveal"><h2>{esc(sh)}</h2>{"".join(f"<p>{p}</p>" for p in paras)}</section>'
    if s["focus"]:
        secs += f'<section class="prose reveal"><h3 class="h4">Areas of focus</h3><ul class="chips">{"".join(f"<li>{esc(x)}</li>" for x in s["focus"])}</ul></section>'
    if s.get("includes"):
        inc = "".join(f"<li>{ICON['check']}{esc(x)}</li>" for x in s["includes"])
        secs += f'<section class="prose reveal"><h3 class="h4">What is included</h3><ul class="ticks ticks--dark">{inc}</ul></section>'
    if s.get("extra"):
        eh, ep = s["extra"]
        ext = ""
        if s.get("ext_cta"):
            ext = f'<p><a class="btn btn--forest" href="{s["ext_cta"][1]}" target="_blank" rel="noopener">{s["ext_cta"][0]} {ICON["external"]}</a></p>'
        secs += f'<section class="prose prose--callout reveal"><h2>{esc(eh)}</h2>{"".join(f"<p>{p}</p>" for p in ep)}{ext}</section>'

    sub = ""
    for i, ss in enumerate(s.get("subservices", [])):
        paras = "".join(f"<p>{esc(p)}</p>" for p in ss["text"])
        if ss.get("mailto"):
            btn = f'<a class="btn" href="mailto:{ss["mailto"]}?subject={ss["cta"][1].replace(" ", "%20")}%20Appointment%20Request">{ss["cta"][0]}</a>'
        else:
            btn = f'<a class="btn" href="/contact/{qs(s["interest"])}">{ss["cta"][0]}</a>'
        sub += f"""<article class="sub{' sub--rev' if i % 2 else ''} reveal" id="{ss['id']}"><div class="sub__img">{pic(ss['img'], ss['alt'], "(min-width:900px) 40vw, 90vw")}</div>
  <div class="sub__copy"><p class="eyebrow">{esc(ss['meta'])}</p><h2>{esc(ss['title'])}</h2>{paras}{btn}</div></article>"""
    rad = ""
    if s.get("radiance"):
        rad = f"""<section class="section section--forest radiance" id="radiance"><div class="wrap split split--rev">
  <div class="split__media reveal"><div class="poster">{pic("radiance-poster", "Radiance Wellness Living coming soon to 100 Boston Rd, Groton", "(min-width:900px) 34vw, 80vw")}</div></div>
  <div class="split__copy reveal"><p class="eyebrow eyebrow--light">Coming soon to 100 Boston Rd, Groton</p><h2>Radiance <em>Wellness Living</em></h2>
  <p>A new recovery and wellness experience designed to help you restore, recharge and feel your best. Alongside the movement, mindfulness and community of WellBeing Studios, Radiance adds a dedicated space for recovery therapies.</p>
  <ul class="ticks"><li>{ICON["check"]}Cold plunge</li><li>{ICON["check"]}Red light therapy</li><li>{ICON["check"]}Saunas</li><li>{ICON["check"]}Hyperbaric</li><li>{ICON["check"]}Compression &amp; more</li></ul>
  <p class="small">Ask about the WellBeing + Radiance Complete unlimited membership.</p>
  <a class="btn btn--light" href="/contact/{qs(s["interest"])}">Join the interest list {ICON["arrow"]}</a></div></div></section>"""

    steps = ""
    if s["steps"]:
        steps = '<section class="prose reveal"><h3 class="h4">How it works</h3><ol class="steps">' + "".join(
            f'<li><span>{i}</span><div><strong>{esc(t)}</strong><p>{esc(d)}</p></div></li>' for i, (t, d) in enumerate(s["steps"], 1)) + "</ol></section>"

    reformer = reformer_table() if s.get("show_reformer") else ""
    team = "".join(f'<li><a href="/team/#{slugify(n.split(",")[0])}">{esc(n.split(",")[0])}</a></li>' for n in s["team"])
    consult_title = {"recovery": "Book recovery"}.get(s["slug"], "Get started")

    body = f"""
<section class="page-hero">
  <div class="wrap page-hero__grid">
    <div class="page-hero__copy">{cr}<p class="eyebrow reveal">{esc(s['eyebrow'])}</p><h1 class="reveal">{s['h1']}</h1><p class="lede reveal">{esc(s['lede'])}</p>
    <div class="hero__btns reveal"><a class="btn btn--lg" href="/contact/{q}">Free consultation {ICON["arrow"]}</a><a class="btn btn--ghost btn--lg" href="tel:{PHONE_TEL}">{ICON["phone"]} {PHONE}</a></div></div>
    <div class="page-hero__art reveal"><div class="arch arch--wide">{pic(s['img'], s['img_alt'], "(min-width:900px) 40vw, 90vw", eager=True)}</div></div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap detail">
    <div class="detail__main">{secs}{steps}</div>
    <aside class="detail__side reveal"><div class="sidecard"><h3>{consult_title}</h3><p>Talk with our team about your goals. The first conversation is always free.</p>
      <a class="btn btn--block" href="/contact/{q}">Request a consultation</a>
      <a class="btn btn--ghost btn--block" href="{SCHEDULE_URL}">See class schedule</a>
      <ul class="contact-list contact-list--sm"><li>{ICON["phone"]}<a href="tel:{PHONE_TEL}">{PHONE}</a></li><li>{ICON["mail"]}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>{ICON["pin"]}<span>{esc(s['locs'])}</span></li></ul></div></aside>
  </div>
</section>
{sub}
{rad}
{reformer}
<section class="section section--tight"><div class="wrap"><p class="eyebrow">Your team</p><ul class="names reveal">{team}</ul></div></section>
{faq}
{cta_band(interest=s["interest"])}
"""
    write(path, h + body + footer() + close())


def reformer_table():
    monthly = "".join(f"""<div class="price{' price--hl' if m['badge'] else ''}">{f'<span class="price__badge">{m["badge"]}</span>' if m['badge'] else ''}<h4>{m['name']}</h4>
    <p class="price__amt">{m['price']}<small>/mo</small></p><p class="price__note">{m['note']}</p><ul>{"".join(f"<li>{ICON['check']}{p}</li>" for p in m['perks'])}</ul></div>""" for m in REFORMER_MONTHLY)
    packs = "".join(f"""<div class="price price--sm{' price--hl' if p['badge'] == 'Most popular' else ''}">{f'<span class="price__badge">{p["badge"]}</span>' if p['badge'] else ''}<h4>{p['name']}</h4>
    <p class="price__amt">{p['price']}</p><p class="price__note">{p['per']}</p><p class="price__note">{p['note']}</p></div>""" for p in REFORMER_PACKS)
    single = f"""<div class="price price--sm"><h4>{REFORMER_SINGLE['name']}</h4><p class="price__amt">{REFORMER_SINGLE['price']}</p><p class="price__note">{REFORMER_SINGLE['note']}</p></div>"""
    return f"""<section class="section" id="reformer"><div class="wrap"><div class="section__head reveal"><p class="eyebrow">Reformer Pilates packages</p><h2>Choose your <em>rhythm.</em></h2>
<p>Introductory pricing for private reformer training. Monthly plans auto-renew; session packages offer the lowest per-session rates and early-renewal bonus sessions on 12 and 24 packs.</p></div>
<h3 class="h4 reveal">Monthly payment options</h3><div class="prices prices--2 reveal">{monthly}</div>
<h3 class="h4 reveal">Session packages</h3><div class="prices prices--4 reveal">{packs}{single}</div>
<p class="fine reveal">Introductory prices shown; rates may change. Contact us to confirm current pricing and availability.</p>
<p class="center"><a class="btn" href="/contact/?interest=Private+Pilates">Book a first session {ICON["arrow"]}</a></p></div></section>"""


def page_classes():
    path = "/classes/"
    title = "Yoga & Pilates Classes, Westford & Groton MA | WellBeing"
    desc = "Yoga, Pilates & Barre classes in Westford and Groton, MA for every level. Slow Flow, Restorative, Yin, Pilates Mat, Barre & more. See the live schedule."
    cr, cr_ld = crumbs([("Classes", path)])
    faq, faq_ld = faq_block(POLICY_FAQ[:5] + [HOME_FAQ[3]], "Your first visit, covered")
    cls_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Group class styles at WellBeing Fitness",
              "itemListElement": [{"@type": "ListItem", "position": i, "name": c["name"], "description": c["text"]} for i, c in enumerate(CLASS_STYLES, 1)]}
    h = head(title, desc, path, og_img=og("class-warrior"), schema=[cr_ld, faq_ld, cls_ld], preload="/images/class-warrior-800.webp") + header("classes")
    chips = '<button class="chip is-on" data-filter="all" type="button">All styles</button><button class="chip" data-filter="yoga" type="button">Yoga</button><button class="chip" data-filter="pilates" type="button">Pilates &amp; Barre</button>'
    grid = "".join(f"""<article class="style reveal" data-group="{c['group']}"><div class="style__top"><h3>{esc(c['name'])}</h3><span class="badge">{esc(c['level'])}</span></div><p>{esc(c['text'])}</p></article>""" for c in CLASS_STYLES)
    inst = "".join(f'<li><a href="/team/#{slugify(t["name"].split(",")[0])}">{esc(t["name"].split(",")[0])}</a></li>' for t in TEAM if set(t["tags"]) & {"yoga", "pilates"})
    body = f"""
<section class="page-hero"><div class="wrap page-hero__grid">
  <div class="page-hero__copy">{cr}<p class="eyebrow reveal">Group classes</p><h1 class="reveal">Move with ease. <em>Feel stronger.</em></h1>
  <p class="lede reveal">Expertly taught yoga, fitness, Pilates and Barre classes at our welcoming studio communities in Westford and Groton. Take time for yourself and find everything you need to support your well-being.</p>
  <div class="hero__btns reveal"><a class="btn btn--lg" href="{SCHEDULE_URL}">View the schedule {ICON["arrow"]}</a><a class="btn btn--ghost btn--lg" href="/memberships/">Passes &amp; memberships</a></div></div>
  <div class="page-hero__art reveal"><div class="arch arch--wide">{pic("class-warrior", "Group yoga class in warrior pose", "(min-width:900px) 40vw, 90vw", eager=True)}</div></div></div></section>

<section class="section section--sand" id="styles"><div class="wrap">
  <div class="section__head reveal"><p class="eyebrow">Class styles</p><h2>Find the practice that <em>fits you.</em></h2><p>Every class offers modifications, so you can meet yourself where you are.</p></div>
  <div class="chips-row reveal" role="group" aria-label="Filter class styles" data-filter-group="styles">{chips}</div>
  <div class="styles" data-filter-target="styles">{grid}</div></div></section>

<section class="section"><div class="wrap split">
  <div class="split__media reveal"><div class="plainimg">{pic("studio-om-room", "Candlelit yoga studio set for class", "(min-width:900px) 40vw, 90vw")}</div></div>
  <div class="split__copy reveal"><p class="eyebrow">Your first visit</p><h2>Come as you are.</h2>
  <ul class="ticks ticks--dark"><li>{ICON["check"]}<span><strong>What to bring:</strong> a mat and water bottle if you like. We have mats, water and all the props you need: blankets, blocks and more.</span></li>
  <li>{ICON["check"]}<span><strong>What to wear:</strong> anything that feels comfortable to move and relax in.</span></li>
  <li>{ICON["check"]}<span><strong>Where to put things:</strong> cubbies and hangers in the studio lobby for belongings and shoes.</span></li>
  <li>{ICON["check"]}<span><strong>Who can join:</strong> weekly classes are for ages 15+, with Teen and Tween programs for ages 11+.</span></li></ul>
  <a class="btn btn--ghost" href="/policies/">Studio policies {ICON["arrow"]}</a></div></div></section>

<section class="section"><div class="wrap"><div class="section__head reveal"><p class="eyebrow">Your teachers</p><h2>Yoga, Pilates &amp; Barre <em>instructors.</em></h2></div>
<ul class="names reveal">{inst}</ul></div></section>
{faq}
{cta_band("Not sure where to begin?", "Tell us what you're looking for and we'll recommend the right class, level and studio.")}
"""
    write(path, h + body + footer() + close())


def money0(v):
    return f"${v:,.0f}"


def price_list(title, rows, link_key, cta):
    items = "".join(f'<li><span>{esc(n)}<small>{esc(sub)}</small></span><strong>{money0(pr)}{"<em>/mo</em>" if mo else ""}</strong></li>' for n, sub, pr, mo in rows)
    return (f'<article class="plist reveal"><h3>{title}</h3><ul>{items}</ul>'
            f'<a class="btn btn--ghost btn--block" href="{MB_LINK[link_key]}" target="_blank" rel="noopener">{cta} {ICON["external"]}</a></article>')


def page_memberships():
    path = "/memberships/"
    title = "Memberships & Class Passes from $25 | WellBeing Fitness"
    desc = "Class passes from $25, memberships from $80 a month and private training plans. Compare every WellBeing Fitness option and find your best value."
    cr, cr_ld = crumbs([("Memberships", path)])
    faq, faq_ld = faq_block([POLICY_FAQ[4], POLICY_FAQ[5], POLICY_FAQ[2], POLICY_FAQ[3], HOME_FAQ[1]], "Membership questions")
    offers = [(p["name"], p["price"], MB_LINK[p["link"]]) for p in PLANS_GROUP + PLANS_COACH] + \
             [(p["name"] + " (private)", p["price"], MB_LINK[p["link"]] if p["mb"] == "mindbody" else SITE + "/contact/") for p in PLANS_PRIVATE]
    cat_ld = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "WellBeing Fitness memberships and passes",
              "itemListElement": [{"@type": "Offer", "name": n, "price": str(pr), "priceCurrency": "USD", "url": u, "seller": {"@id": SITE + "/#org"}} for n, pr, u in offers]}
    h = head(title, desc, path, schema=[cr_ld, faq_ld, cat_ld]) + header("memberships")
    plans = {"group": PLANS_GROUP, "private": PLANS_PRIVATE, "coach": PLANS_COACH, "trial": TRIAL, "links": MB_LINK}
    mem_rows = [(p["name"], "Group classes · auto-renew", p["price"], True) for p in PLANS_GROUP if p["kind"] == "member"]
    pass_rows = [(p["name"], f'{p["valid"]}-month validity' if p.get("valid") else "No expiry", p["price"], False) for p in PLANS_GROUP if p["kind"] != "member"]
    pass_rows.append((TRIAL["name"], "For new clients", TRIAL["price"], False))
    priv_rows = [(p["name"], p["sub"].split(" · ")[0], p["price"], p["kind"] == "member") for p in PLANS_PRIVATE] + [(c["name"], c["sub"], c["price"], True) for c in PLANS_COACH]
    body = f"""
<section class="page-hero page-hero--plain"><div class="wrap">{cr}<p class="eyebrow reveal">Memberships &amp; pricing</p><h1 class="reveal">Design your <em>membership.</em></h1>
<p class="lede reveal">Tell us how you like to move and we'll show what each option really costs. Real prices, no surprises, and checkout is a click away on Mindbody.</p></div></section>

<section class="section section--tight" id="plan-studio"><div class="wrap">
  <div class="pstudio" data-plans>
    <div class="pstudio__main">
      <div class="ptabs" role="tablist" aria-label="Choose what you're shopping for">
        <button class="ptab is-on" role="tab" aria-selected="true" aria-controls="panel-group" id="tab-group" data-tab="group" type="button">{ICON["lotus"]}<span>Group<i> classes</i></span></button>
        <button class="ptab" role="tab" aria-selected="false" aria-controls="panel-private" id="tab-private" data-tab="private" type="button" tabindex="-1">{ICON["ring"]}<span>Private<i> &amp; reformer</i></span></button>
        <button class="ptab" role="tab" aria-selected="false" aria-controls="panel-coach" id="tab-coach" data-tab="coach" type="button" tabindex="-1">{ICON["leaf"]}<span>Coaching</span></button>
      </div>

      <div class="ppanel" id="panel-group" role="tabpanel" aria-labelledby="tab-group" data-panel="group">
        <div class="dial">
          <label for="dial" class="dial__q">How many classes would you like each month?</label>
          <div class="dial__row"><output class="dial__n" for="dial" data-dial-n>4</output><span class="dial__u">classes<br>a month<em data-dial-sub>about once a week</em></span></div>
          <input class="dial__range" id="dial" type="range" min="1" max="12" step="1" value="4" aria-describedby="dial-hint">
          <div class="dial__ticks" aria-hidden="true"><span>1</span><span>4</span><span>8</span><span>12+</span></div>
          <p class="dial__hint" id="dial-hint">Drag to see what each option would cost at your pace.</p>
        </div>
        <fieldset class="opts" data-opts="group"><legend class="sr">Choose a group-class plan</legend></fieldset>
        <div class="trial"><span>{ICON["sparkle"]}</span><p><strong>New to WellBeing?</strong> {esc(TRIAL["note"])} <a href="{MB_LINK["pass"]}" target="_blank" rel="noopener">Get the trial {ICON["external"]}</a></p></div>
      </div>

      <div class="ppanel" id="panel-private" role="tabpanel" aria-labelledby="tab-private" data-panel="private" hidden>
        <div class="dial">
          <p class="dial__q" id="freq-q">How often would you like to train one-to-one?</p>
          <div class="freq" role="group" aria-labelledby="freq-q">
            <button class="freq__b" type="button" data-freq="weekly"><strong>Weekly</strong><small>about 4 a month</small></button>
            <button class="freq__b" type="button" data-freq="twice"><strong>Twice a week</strong><small>about 8 a month</small></button>
            <button class="freq__b" type="button" data-freq="flex"><strong>Flexible</strong><small>use a package</small></button>
          </div>
        </div>
        <fieldset class="opts" data-opts="private"><legend class="sr">Choose a private training plan</legend></fieldset>
      </div>

      <div class="ppanel" id="panel-coach" role="tabpanel" aria-labelledby="tab-coach" data-panel="coach" hidden>
        <div class="dial"><p class="dial__q">Health &amp; nutrition coaching, built around you.</p><p class="dial__hint">Work one-to-one with our coaching team. Not sure it's right? Start with a <a href="/contact/?interest=Nutrition+%26+Health+Coaching">free 30-minute consultation</a>.</p></div>
        <fieldset class="opts" data-opts="coach"><legend class="sr">Coaching program</legend></fieldset>
      </div>
    </div>
    <aside class="pticket" aria-live="polite" aria-label="Your selected plan" data-ticket></aside>
  </div>
  <script type="application/json" id="plans-data">{json.dumps(plans)}</script>
</div></section>


{gifts_block()}
<section class="section section--tight"><div class="wrap plans plans--2">
  <article class="plan plan--big reveal"><span class="plan__ico">{ICON["wave"]}</span><h2>WellBeing + Radiance</h2><p>An unlimited membership pairing group classes with Radiance Wellness Living recovery services is on the way. Join the interest list and we will tell you first.</p><a class="btn btn--ghost" href="/contact/?interest=Recovery+%C2%B7+Reiki+%C2%B7+Physical+Therapy">Join the interest list {ICON["arrow"]}</a></article>
</div></section>
{faq}
{cta_band("Questions about the right plan?", "We'll help you choose the membership, pass or package that fits your goals and your schedule.")}
"""
    scripts = '<script src="/js/plans.js" defer></script>'
    h = h.replace('<link rel="stylesheet" href="/css/styles.css">', '<link rel="stylesheet" href="/css/styles.css">\n<link rel="stylesheet" href="/css/plans.css">\n<link rel="stylesheet" href="/css/schedule.css">')
    write(path, h + body + footer() + scripts + close())


def page_team():
    path = "/team/"
    title = "Our Team: Trainers & Yoga Instructors | WellBeing Fitness"
    desc = "Meet the WellBeing Fitness team in Westford & Groton, MA: NASM trainers, 500-hour yoga teachers, Pilates & Barre instructors, a health coach and a PT."
    cr, cr_ld = crumbs([("Our Team", path)])
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "WellBeing Fitness team",
          "itemListElement": [{"@type": "ListItem", "position": i, "item": {"@type": "Person", "name": t["name"].split(",")[0], "jobTitle": t["role"], "worksFor": {"@id": SITE + "/#org"}}} for i, t in enumerate(TEAM, 1)]}
    h = head(title, desc, path, og_img=og("studio-weights"), schema=[cr_ld, ld]) + header("team")
    chips = "".join(f'<button class="chip{" is-on" if k == "all" else ""}" data-filter="{k}" type="button">{v}</button>' for k, v in TEAM_FILTERS)
    people = "".join(team_card(t) for t in TEAM)
    body = f"""
<section class="page-hero page-hero--plain"><div class="wrap">{cr}<p class="eyebrow reveal">Who we are</p><h1 class="reveal">Specialists who see <em>you,</em> not a template.</h1>
<p class="lede reveal">A dedicated team of trainers, teachers, coaches and therapists, each bringing deep training and a personal story to the work.</p></div></section>
<section class="section section--tight"><div class="wrap">
  <div class="chips-row reveal" role="group" aria-label="Filter team by specialty" data-filter-group="team">{chips}</div>
  <div class="people" data-filter-target="team">{people}</div></div></section>
{cta_band("Find the right guide for your goals.", "Not sure who to work with? Tell us what you're after and we'll match you with the right person on our team.")}
"""
    write(path, h + body + footer() + close())


def map_embed(q, label):
    return f'<iframe class="map" title="Map of {esc(label)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={q}&output=embed"></iframe>'


def page_location(l):
    path = f"/{l['slug']}/"
    cr, cr_ld = crumbs([("Studios", "/locations/"), (l["name"], path)])
    other = [x for x in LOCATIONS if x is not l][0]
    club = dict(org_ld()[LOCATIONS.index(l)], **{"@context": "https://schema.org"})
    h = head(l["title"], l["desc"], path, og_img=og(l["img"]), schema=[club, cr_ld], preload=f"/images/{l['img']}-800.webp") + header("locations")
    notes = "".join(f"<div><h3>{esc(k)}</h3><p>{esc(v)}</p></div>" for k, v in l["notes"])
    svc = "".join(f"<li>{ICON['check']}{esc(x)}</li>" for x in l["services"])
    body = f"""
<section class="page-hero"><div class="wrap page-hero__grid">
  <div class="page-hero__copy">{cr}<p class="eyebrow reveal">WellBeing {esc(l['name'])}</p><h1 class="reveal">Your studio in <em>{esc(l['name'])}, MA.</em></h1><p class="lede reveal">{esc(l['blurb'])}</p>
  <address class="addr reveal">{ICON['pin']}<span>{esc(l['street'])}<br>{esc(l['city'])}, {l['state']} {l['zip']}</span></address>
  <div class="hero__btns reveal"><a class="btn btn--lg" href="https://www.google.com/maps/dir/?api=1&destination={l['map_q']}" target="_blank" rel="noopener">Get directions {ICON['external']}</a><a class="btn btn--ghost btn--lg" href="{SCHEDULE_URL}">Class schedule</a></div></div>
  <div class="page-hero__art reveal"><div class="arch arch--wide">{pic(l['img'], f"WellBeing Fitness {l['name']} studio", "(min-width:900px) 40vw, 90vw", eager=True)}</div></div></div></section>
<section class="section section--tight"><div class="wrap loc">
  <div class="loc__info reveal"><h2>Services at {esc(l['name'])}</h2><ul class="ticks ticks--dark ticks--cols">{svc}</ul><div class="notes">{notes}</div>
  <p class="fine">Services vary by day and studio. See the <a href="{SCHEDULE_URL}">class schedule</a> or <a href="/contact/">contact us</a> to confirm.</p></div>
  <div class="loc__map reveal">{map_embed(l['map_q'], l['name'] + ' studio')}</div></div></section>
<section class="section section--sand"><div class="wrap split">
  <div class="split__media reveal"><div class="arch">{pic(l['img2'], f"Inside the WellBeing {l['name']} studio", "(min-width:900px) 34vw, 80vw")}</div></div>
  <div class="split__copy reveal"><p class="eyebrow">Also visit</p><h2>WellBeing {esc(other['name'])}</h2><p>{esc(other['blurb'])}</p><a class="btn" href="/{other['slug']}/">{esc(other['name'])} studio details {ICON['arrow']}</a></div></div></section>
{cta_band(f"Come visit us in {l['name']}.", "Take a class, meet a coach or tour the studio. We'd love to welcome you.")}
"""
    write(path, h + body + footer() + close())


def page_locations():
    path = "/locations/"
    title = "Studio Locations: Westford & Groton, MA | WellBeing Fitness"
    desc = "Visit WellBeing Fitness at 203 B Littleton Rd, Westford or 134 Main St, Groton, MA. Directions, parking, entrances and services at each studio."
    cr, cr_ld = crumbs([("Studios", path)])
    h = head(title, desc, path, schema=[cr_ld] + [dict(c, **{"@context": "https://schema.org"}) for c in org_ld()]) + header("locations")
    stud = ""
    for l in LOCATIONS:
        stud += f"""<article class="studio reveal"><a class="studio__img" href="/{l['slug']}/">{pic(l['img'], f"WellBeing Fitness {l['name']} studio", "(min-width:900px) 50vw, 100vw")}</a>
  <div class="studio__body"><p class="eyebrow">{esc(l['name'])}, MA</p><h2 class="h3">{esc(l['street'])}, {esc(l['city'])}, {l['state']} {l['zip']}</h2><p>{esc(l['blurb'])}</p>
  <ul class="tags">{"".join(f"<li>{esc(x)}</li>" for x in l['services'])}</ul>
  <div class="studio__links"><a class="link" href="/{l['slug']}/">Studio details {ICON['arrow']}</a><a class="link" href="https://www.google.com/maps/dir/?api=1&destination={l['map_q']}" target="_blank" rel="noopener">Get directions {ICON['external']}</a></div></div></article>"""
    body = f"""<section class="page-hero page-hero--plain"><div class="wrap">{cr}<p class="eyebrow reveal">Our studios</p><h1 class="reveal">Two studios. <em>One community.</em></h1>
<p class="lede reveal">Find movement, mindfulness and community in Westford and Groton. Radiance Wellness Living arrives soon at 100 Boston Rd in Groton.</p></div></section>
<section class="section section--tight"><div class="wrap studios">{stud}</div></section>
{cta_band("Not sure which studio is right for you?", "Tell us what you're looking for and we'll point you to the right location and schedule.")}"""
    write(path, h + body + footer() + close())


LOC_FULL = {"Westford": "Westford studio", "Groton": "Groton studio"}


def mb_data():
    p = os.path.join(ROOT, "data", "mindbody.json")
    return json.load(open(p, encoding="utf8")) if os.path.exists(p) else {"generated": "", "from": "", "to": "", "classes": [], "events": []}


def teacher_map(names):
    alias = {"Shagufta Rahman": "Shagufta Rahmen", "Darlene Murray": "Darleen Murray", "Julia Lefebvre": "Julia"}
    out = {}
    for n in sorted({x for x in names if x}):
        t = TEAM_BY_NAME.get(alias.get(n, n))
        if t:
            out[n] = {"slug": slugify(t["name"].split(",")[0]), "img": f"/images/team-{t['img']}.webp" if t["img"] else ""}
    return out


def tz_offset(iso_date):
    """US Eastern offset for the dates this studio schedules (DST 2026-03-08 to 2026-11-01, 2027-03-14 onward)."""
    return "-04:00" if ("2026-03-08" <= iso_date < "2026-11-01" or iso_date >= "2027-03-14") else "-05:00"


def fmt_time(hhmm_):
    h, m = (int(x) for x in hhmm_.split(":"))
    return f"{(h % 12) or 12}:{m:02d} {'pm' if h >= 12 else 'am'}"


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%A, %B ") + str(d.day)


def event_kind(e):
    t = (e["title"] + " " + e["desc"]).lower()
    if "family" in t or "story" in t:
        return "family"
    if "sound" in t or "meditation" in t:
        return "sound"
    if "women" in t or "understanding" in t or "menopaus" in t:
        return "wellness"
    return "yoga"


EVENT_KINDS = [("all", "All events"), ("family", "Family"), ("sound", "Sound & meditation"), ("yoga", "Yoga experiences"), ("wellness", "Wellness talks")]


def mb_reserve(e):
    if not e.get("id"):
        return MB_EVENTS
    d = datetime.date.fromisoformat(e["date"])
    return (f"https://clients.mindbodyonline.com/ASP/res_a.asp?tg={e['tg']}&classId={e['id']}&classDate={d.month}/{d.day}/{d.year}"
            f"&clsLoc={e['clsLoc']}&studioid=729963")


def page_schedule():
    path = "/schedule/"
    title = "Class Schedule: Yoga, Pilates & Barre | WellBeing Fitness"
    desc = "See the WellBeing Fitness class schedule for Westford and Groton, MA. Filter by studio and style, then reserve your spot in yoga, Pilates, Barre and fitness classes."
    cr, cr_ld = crumbs([("Class Schedule", path)])
    mb = mb_data()
    tmap = teacher_map([c["teacher"] for c in mb["classes"]])
    payload = {"generated": mb["generated"], "from": mb["from"], "to": mb["to"], "teachers": tmap, "mb": MB_SCHEDULE,
               "classes": [[c["date"], c["start"], c["name"], c["teacher"], c["loc"], c["min"], c["id"], c["tg"], c["clsLoc"]] for c in mb["classes"]]}
    # crawlable typical week (the most recent complete week in the snapshot), replaced by the interactive list once JS runs
    last = [c for c in mb["classes"] if c["date"] > (datetime.date.fromisoformat(mb["to"]) - datetime.timedelta(days=7)).isoformat()] if mb["to"] else []
    days = {}
    for c in last:
        days.setdefault(c["date"], []).append(c)
    ssr = ""
    for d in sorted(days):
        rows = "".join(f'<li><span>{fmt_time(c["start"])}</span><strong>{esc(c["name"])}</strong><em>{esc(c["teacher"] or "WellBeing team")}</em><i>{esc(c["loc"] or "Online")}</i></li>' for c in days[d])
        ssr += f'<div class="ssr-day"><h3>{datetime.date.fromisoformat(d).strftime("%A")}</h3><ul>{rows}</ul></div>'
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "WellBeing Fitness weekly class schedule",
          "itemListElement": [{"@type": "ListItem", "position": i, "name": c["name"]} for i, c in enumerate(last[:40], 1)]}
    h = head(title, desc, path, og_img=og("class-warrior"), schema=[cr_ld, ld]) + header("schedule")
    h = h.replace('<link rel="stylesheet" href="/css/styles.css">', '<link rel="stylesheet" href="/css/styles.css">\n<link rel="stylesheet" href="/css/schedule.css">')
    body = f"""
<section class="page-hero page-hero--plain"><div class="wrap">{cr}<p class="eyebrow reveal">Class schedule</p><h1 class="reveal">Find your <em>class.</em></h1>
<p class="lede reveal">Pick a day, choose a studio and a style, and reserve your spot. We'll take you to secure checkout to finish.</p></div></section>

<section class="section section--tight" id="schedule"><div class="wrap">
  <div class="sched" data-schedule>
    <div class="sched__top">
      <div class="days" data-days role="tablist" aria-label="Choose a day"></div>
    </div>
    <div class="sched__filters">
      <div class="seg" role="group" aria-label="Studio" data-seg="loc">
        <button type="button" class="is-on" data-v="all">Both studios</button><button type="button" data-v="Westford">Westford</button><button type="button" data-v="Groton">Groton</button></div>
      <div class="chips-row chips-row--tight" role="group" aria-label="Class style" data-seg="type">
        <button class="chip is-on" type="button" data-v="all">All styles</button><button class="chip" type="button" data-v="yoga">Yoga</button>
        <button class="chip" type="button" data-v="pilates">Pilates &amp; Barre</button><button class="chip" type="button" data-v="fitness">Fitness</button>
        <button class="chip" type="button" data-v="meditation">Meditation</button><button class="chip chip--star" type="button" data-v="easy">Beginner friendly</button></div>
    </div>
    <h2 class="sched__day" data-day-title aria-live="polite"></h2>
    <div class="sched__list" data-list>
      <div class="ssr">{ssr}</div>
    </div>
    <p class="sched__note" data-note></p>
  </div>
  <script type="application/json" id="sched-data">{json.dumps(payload, ensure_ascii=False)}</script>
</div></section>

{cta_band("New to WellBeing?", "Tell us your goals and we'll point you to the right class, level and studio.")}
"""
    scripts = '<script src="/js/schedule.js" defer></script>'
    write(path, h + body + footer() + scripts + close())


def page_events():
    path = "/events/"
    title = "Workshops, Sound Baths & Special Events | WellBeing Fitness"
    desc = "Upcoming WellBeing Fitness events in Groton and Westford, MA: sound baths, Full Moon Flow, family yoga, spa yoga and wellness workshops. Reserve your spot."
    cr, cr_ld = crumbs([("Events", path)])
    mb = mb_data()
    today = datetime.date.today().isoformat()
    g = datetime.date.fromisoformat(mb["generated"]) if mb["generated"] else None
    upd = f"{g.strftime('%B')} {g.day}" if g else ""
    evs = [e for e in mb["events"]]
    cards, ld_events, last_month = "", [], ""
    for e in evs:
        d = datetime.date.fromisoformat(e["date"])
        month = d.strftime("%B %Y")
        if month != last_month:
            cards += f'<h2 class="ev-month" data-month>{month}</h2>'
            last_month = month
        kind = event_kind(e)
        who = e["teacher"]
        chips = "".join(f'<span class="ev__price">{esc(re.sub(r"[ (]+$", "", p))}</span>' for p in e["price"][:2])
        desc_full = esc(e["desc"])
        short = esc(e["desc"][:200].rsplit(" ", 1)[0] + "…") if len(e["desc"]) > 230 else desc_full
        more = f'<details class="ev__more"><summary>Read more {ICON["plus"]}</summary><p>{desc_full}</p></details>' if len(e["desc"]) > 230 else ""
        cards += f"""<article class="ev reveal" data-date="{e['date']}" data-kind="{kind}" data-loc="{esc(e['loc'])}">
  <div class="ev__date"><span>{d.strftime('%b')}</span><strong>{d.day}</strong><small>{d.strftime('%a')}</small></div>
  <div class="ev__body"><div class="ev__meta"><span class="ev__loc">{ICON['pin']}{esc(e['loc'])} studio</span><span>{fmt_time(e['start'])}{' – ' + fmt_time(e['end']) if e['end'] else ''}</span>{f'<span>with {esc(who)}</span>' if who else ''}</div>
  <h3>{esc(e['title'])}</h3><p class="ev__desc">{short}</p>{more}{f'<div class="ev__prices">{chips}</div>' if chips else ''}</div>
  <div class="ev__cta"><a class="btn" href="{mb_reserve(e)}" target="_blank" rel="noopener">Reserve {ICON['arrow']}</a></div></article>"""
        if e["date"] >= today:
            ld_events.append({"@context": "https://schema.org", "@type": "Event", "name": e["title"], "description": e["desc"][:300],
                              "startDate": f"{e['date']}T{e['start']}:00{tz_offset(e['date'])}", "eventStatus": "https://schema.org/EventScheduled",
                              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                              "location": {"@type": "Place", "name": f"WellBeing Fitness {e['loc']}", "address": {"@type": "PostalAddress", "addressLocality": e["loc"], "addressRegion": "MA", "addressCountry": "US"}},
                              "organizer": {"@id": SITE + "/#org"}, "url": SITE + path})
            if e["end"]:
                ld_events[-1]["endDate"] = f"{e['date']}T{e['end']}:00{tz_offset(e['date'])}"
    chips = "".join(f'<button class="chip{" is-on" if k == "all" else ""}" type="button" data-v="{k}">{v}</button>' for k, v in EVENT_KINDS)
    h = head(title, desc, path, og_img=og("friends"), schema=[cr_ld] + ld_events) + header("events")
    h = h.replace('<link rel="stylesheet" href="/css/styles.css">', '<link rel="stylesheet" href="/css/styles.css">\n<link rel="stylesheet" href="/css/schedule.css">')
    items = [("lotus", "Monthly workshops", "Specialty workshops and programs focused on lifestyle wellness for the whole family."),
             ("people", "Private parties & groups", "Celebrate with a private yoga, fitness, Pilates, Barre or Reiki experience for your group."),
             ("briefcase", "Corporate workshops", "Stretch & Strengthen, stress relief, meditation and nutrition workshops for your team.")]
    ways = "".join(f'<div class="plan reveal"><span class="plan__ico">{ICON[ic]}</span><h3>{t}</h3><p>{d_}</p></div>' for ic, t, d_ in items)
    body = f"""<section class="page-hero"><div class="wrap page-hero__grid"><div class="page-hero__copy">{cr}<p class="eyebrow reveal">Events &amp; workshops</p><h1 class="reveal">Gather. Learn. <em>Grow together.</em></h1>
<p class="lede reveal">Sound baths, full-moon flows, family yoga and wellness talks. Browse what's coming up and reserve your spot.</p>
<div class="hero__btns reveal"><a class="btn btn--lg" href="#upcoming">See upcoming events {ICON['arrow']}</a><a class="btn btn--ghost btn--lg" href="/contact/?interest=Private+Event">Plan a private event</a></div></div>
<div class="page-hero__art reveal"><div class="arch arch--wide">{pic("friends", "Two friends laughing together outdoors", "(min-width:900px) 40vw, 90vw", eager=True)}</div></div></div></section>

<section class="section section--tight" id="upcoming"><div class="wrap">
  <div class="section__head reveal"><p class="eyebrow">Upcoming</p><h2>On the <em>calendar.</em></h2></div>
  <div class="events" data-events>
    <div class="sched__filters">
      <div class="seg" role="group" aria-label="Studio" data-seg="loc"><button type="button" class="is-on" data-v="all">Both studios</button><button type="button" data-v="Westford">Westford</button><button type="button" data-v="Groton">Groton</button></div>
      <div class="chips-row chips-row--tight" role="group" aria-label="Event type" data-seg="kind">{chips}</div>
    </div>
    <div class="ev-list" data-ev-list>{cards}</div>
    <p class="sched__empty" data-ev-empty hidden>No events match right now. Check back soon, or <a href="/contact/?interest=Private+Event">ask about a private event</a>.</p>
    <p class="sched__note">Events last updated {upd}. Reservations are completed securely on Mindbody.</p>
  </div>
</div></section>

{cta_band("Hosting something special?", "Tell us about your group, date and goals and we'll help design the experience.", "Private Event")}"""
    scripts = '<script src="/js/events.js" defer></script>'
    write(path, h + body + footer() + scripts + close())


GIFTS = [("Class pass gift", "5 Class Pass, Yoga", 99, "heart"), ("Private training", "3 Private Session Starter Pack", 270, "dumbbell"),
         ("Health coaching", "Health & Nutrition Coaching Session", 89, "leaf"), ("Spa yoga", "Spa Yoga Class for up to 6", 150, "wave")]


def gifts_block():
    cards = "".join(f"""<a class="gift reveal" href="{MB_LINK['gift']}" target="_blank" rel="noopener"><span class="plan__ico">{ICON[ic]}</span><small>{esc(k)}</small><strong>{esc(n)}</strong><em>{money0(pr)}</em><span class="card__more">Send as a gift {ICON['external']}</span></a>""" for k, n, pr, ic in GIFTS)
    return f"""<section class="section section--tight"><div class="wrap">
  <div class="section__head reveal"><p class="eyebrow">Gift cards</p><h2>Give the gift of <em>wellness.</em></h2><p>Choose a gift, then finish checkout securely on Mindbody. You can also send a custom amount good for any service.</p></div>
  <div class="gifts">{cards}<a class="gift gift--custom reveal" href="{MB_LINK['gift']}" target="_blank" rel="noopener"><span class="plan__ico">{ICON['sparkle']}</span><small>Any amount</small><strong>Custom gift card</strong><em>You choose</em><span class="card__more">Create a gift card {ICON['external']}</span></a></div>
</div></section>"""


def page_policies():
    path = "/policies/"
    title = "Studio Policies & FAQ | WellBeing Fitness"
    desc = "WellBeing Fitness studio information and policies: class registration, cancellations, passes, memberships, waivers, age requirements, parking and weather closures."
    cr, cr_ld = crumbs([("Policies & FAQ", path)])
    faq, faq_ld = faq_block(POLICY_FAQ, "Studio information & policies", "Thank you for helping us maintain a thriving fitness and wellness community.")
    h = head(title, desc, path, schema=[cr_ld, faq_ld]) + header()
    body = f"""<section class="page-hero page-hero--plain"><div class="wrap">{cr}<p class="eyebrow reveal">Studio information</p><h1 class="reveal">Policies &amp; <em>FAQ</em></h1>
<p class="lede reveal">Everything you need to know about registering, cancelling, parking and more.</p></div></section>
{faq}
{cta_band("Still have a question?", "Call, email or send us a message. We're happy to help.")}"""
    write(path, h + body + footer() + close())


def page_contact():
    path = "/contact/"
    title = "Free Consultation & Contact | WellBeing Fitness, MA"
    desc = "Request a free consultation with WellBeing Fitness. Call 978-496-1846. Studios in Westford (203 B Littleton Rd) and Groton (134 Main St), MA."
    cr, cr_ld = crumbs([("Contact", path)])
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact WellBeing Fitness", "url": SITE + path}
    h = head(title, desc, path, schema=[cr_ld, contact_ld]) + header("contact")
    maps = "".join(f'<div class="reveal"><h3 class="h4">{l["name"]}</h3><p class="small">{l["street"]}, {l["city"]}, {l["state"]} {l["zip"]}</p>{map_embed(l["map_q"], l["name"] + " studio")}</div>' for l in LOCATIONS)
    body = f"""<section class="page-hero page-hero--plain"><div class="wrap">{cr}<p class="eyebrow reveal">Get in touch</p><h1 class="reveal">Let's start with a <em>conversation.</em></h1>
<p class="lede reveal">Request your free consultation and we'll help you find the right starting point.</p></div></section>
<section class="section section--tight"><div class="wrap consult__grid">
  <div class="reveal"><ul class="contact-list contact-list--lg"><li>{ICON['phone']}<div><small>Call or text</small><a href="tel:{PHONE_TEL}">{PHONE}</a></div></li>
  <li>{ICON['mail']}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
  <li>{ICON['pin']}<div><small>Westford</small>203 B Littleton Rd, Westford, MA 01886</div></li>
  <li>{ICON['pin']}<div><small>Groton</small>134 Main St, Groton, MA 01450</div></li></ul>
  <p class="small">Health coaching &amp; nutrition: <a href="mailto:melissa@wellbeing-fitness.com">melissa@wellbeing-fitness.com</a></p></div>
  <div class="consult__card reveal">{consult_form("contact")}</div></div></section>"""
    write(path, h + body + footer() + close())


def page_thanks():
    h = head("Thank you | WellBeing Fitness", "Thanks for reaching out to WellBeing Fitness.", "/thanks/", noindex=True) + header()
    body = f"""<section class="page-hero page-hero--plain page-hero--center"><div class="wrap"><p class="eyebrow">Message received</p><h1>Thank you. <em>We'll be in touch.</em></h1>
<p class="lede">Expect a reply within one business day. In the meantime, explore classes or meet the team.</p>
<div class="hero__btns hero__btns--center"><a class="btn btn--lg" href="{SCHEDULE_URL}">Browse classes</a><a class="btn btn--ghost btn--lg" href="/team/">Meet the team</a></div></div></section>"""
    write("/thanks/", h + body + footer() + close())


def page_404():
    h = head("Page not found | WellBeing Fitness", "Page not found.", "/404.html", noindex=True) + header()
    body = f"""<section class="page-hero page-hero--plain page-hero--center"><div class="wrap"><p class="eyebrow">404</p><h1>This page wandered <em>off the mat.</em></h1>
<p class="lede">Let's get you back on track.</p><div class="hero__btns hero__btns--center"><a class="btn btn--lg" href="/">Back to home</a><a class="btn btn--ghost btn--lg" href="/classes/">Browse classes</a></div></div></section>"""
    write("/404.html", h + body + footer() + close())


# ------------------------------------------------------------------------------------------------
# Shop
# ------------------------------------------------------------------------------------------------
FALLBACK_MERCH = [
    ("Women's Scoop-Neck Blues Yoga Logo Tee", "merch-blues-tee"), ("Women's Scoop-Neck Yoga Logo Tee", "merch-white-tee"),
    ("WB Runner Logo Zip Hoodie", "merch-runner-hoodie"), ("Front & Back Logo Zip Up", "merch-zip-up"),
    ("Fleece Logo Jogger", "merch-jogger"), ("PEACE Sign Crewneck", "merch-peace-crewneck"),
    ("WellBeing Fitness Tote", "merch-tote"), ("Peace · Health · Community Tank", "merch-tank"),
]


def load_shop(products_path):
    """Returns {"mode": "shopify"|"bonfire", "cfg": {...}, "items": [...]}."""
    if products_path and os.path.exists(products_path):
        data = json.load(open(products_path, encoding="utf-8"))
        return {"mode": "shopify", "cfg": {"domain": data["domain"], "currency": data.get("currency", "USD")}, "items": data["products"]}
    return {"mode": "bonfire", "cfg": {}, "items": [{"title": t, "img": i} for t, i in FALLBACK_MERCH]}


def money(v):
    return f"${float(v):,.2f}".replace(".00", "") if float(v) == int(float(v)) else f"${float(v):,.2f}"


def shop_cards(shop, limit=None):
    items = shop["items"][:limit] if limit else shop["items"]
    out = ""
    if shop["mode"] == "bonfire":
        for it in items:
            out += f"""<article class="product reveal"><a class="product__media" href="{BONFIRE_URL}" target="_blank" rel="noopener">{pic(it['img'], it['title'] + ' from the WellBeing Fit Shop', "(min-width:900px) 22vw, 46vw")}</a>
  <div class="product__body"><h3>{esc(it['title'])}</h3><a class="link" href="{BONFIRE_URL}" target="_blank" rel="noopener">Shop at Bonfire {ICON['external']}</a></div></article>"""
        return out
    for p in items:
        v0 = p["variants"][0]
        opts = ""
        if len(p["variants"]) > 1:
            opts = '<select class="variant-select" aria-label="Choose an option">' + "".join(
                f'<option value="{v["id"]}" data-price="{v["price"]}"{" disabled" if not v["available"] else ""}>{esc(v["title"])}{" (sold out)" if not v["available"] else ""} · {money(v["price"])}</option>' for v in p["variants"]) + "</select>"
        img = f'<img src="{esc(p["image"])}" alt="{esc(p["title"])}" loading="lazy" decoding="async" width="600" height="750">' if p.get("image") else ""
        out += f"""<article class="product reveal" data-pid="{p['id']}" data-title="{esc(p['title'])}" data-image="{esc(p.get('image', ''))}" data-type="{esc(p.get('type', ''))}">
  <a class="product__media" href="https://{shop['cfg']['domain']}/products/{p['handle']}" target="_blank" rel="noopener">{img}</a>
  <div class="product__body"><h3>{esc(p['title'])}</h3><p class="price">{money(v0['price'])}</p>{opts}
  <button class="btn btn--sm btn--block" type="button" data-add data-variant="{v0['id']}" data-price="{v0['price']}" data-vtitle="{esc(v0['title'])}">Add to bag</button></div></article>"""
    return out


def page_shop(shop):
    path = "/shop/"
    title = "Fit Shop: WellBeing Fitness Apparel & Wellness Gear"
    desc = "Shop the WellBeing Fit Shop: studio apparel, comfortable active wear and more for a wellness life, from the team at WellBeing Fitness in Westford and Groton, MA."
    cr, cr_ld = crumbs([("Fit Shop", path)])
    ld = [cr_ld]
    if shop["mode"] == "shopify":
        for p in shop["items"]:
            ld.append({"@context": "https://schema.org", "@type": "Product", "name": p["title"], "description": p.get("description", ""),
                       "image": p.get("image"), "brand": {"@type": "Brand", "name": NAME},
                       "offers": {"@type": "Offer", "priceCurrency": shop["cfg"]["currency"], "price": p["variants"][0]["price"],
                                  "availability": "https://schema.org/InStock" if any(v["available"] for v in p["variants"]) else "https://schema.org/OutOfStock",
                                  "url": f"https://{shop['cfg']['domain']}/products/{p['handle']}"}})
    h = head(title, desc, path, og_img="/images/og-card.jpg", schema=ld) + header("shop")
    chips = ""
    if shop["mode"] == "shopify":
        types = sorted({p.get("type") for p in shop["items"] if p.get("type")})
        if len(types) > 1:
            chips = '<div class="chips-row" role="group" aria-label="Filter products" data-filter-group="shop"><button class="chip is-on" data-filter="all" type="button">All</button>' + "".join(
                f'<button class="chip" data-filter="{esc(t)}" type="button">{esc(t)}</button>' for t in types) + "</div>"
    notice = ("Checkout is handled securely by Shopify." if shop["mode"] == "shopify" else "Orders are printed and shipped by Bonfire, with 90-day hassle-free returns.")
    cart = ""
    if shop["mode"] == "shopify":
        cart = f"""<button class="cart-fab" type="button" data-cart-open aria-label="Open bag">{ICON['bag']}<span class="cart-fab__n" data-cart-count>0</span></button>
<div class="cart" id="cart" hidden><div class="cart__scrim" data-cart-close></div><aside class="cart__panel" role="dialog" aria-label="Shopping bag" aria-modal="true">
  <div class="cart__head"><h2>Your bag</h2><button type="button" data-cart-close aria-label="Close bag">{ICON['close']}</button></div>
  <ul class="cart__list" data-cart-list></ul><p class="cart__empty" data-cart-empty>Your bag is empty.</p>
  <div class="cart__foot"><div class="cart__sub"><span>Subtotal</span><strong data-cart-sub>$0</strong></div><p class="small">Shipping and taxes are calculated at checkout.</p>
  <a class="btn btn--lg btn--block" href="#" data-cart-checkout>Checkout {ICON['arrow']}</a></div></aside></div>"""
    body = f"""<section class="page-hero page-hero--plain"><div class="wrap">{cr}<p class="eyebrow reveal">The Fit Shop</p><h1 class="reveal">Comfort active wear for a <em>wellness life.</em></h1>
<p class="lede reveal">Official WellBeing Fitness apparel and more. Wear the studio to class, on the trail or around town.</p>
{'' if shop['mode'] == 'shopify' else f'<div class="hero__btns reveal"><a class="btn btn--lg" href="{BONFIRE_URL}" target="_blank" rel="noopener">Shop on Bonfire {ICON["external"]}</a></div>'}</div></section>
<section class="section section--tight"><div class="wrap">{chips}<div class="products" data-filter-target="shop">{shop_cards(shop)}</div>
<p class="fine center reveal">{notice}</p>
{'' if shop['mode'] == 'shopify' else f'<p class="center reveal"><a class="btn btn--lg" href="{BONFIRE_URL}" target="_blank" rel="noopener">Visit the full shop {ICON["external"]}</a></p>'}</div></section>
{cart}{cta_band("Looking for something specific?", "Ask us about studio gear, gift ideas and custom orders for your group.")}"""
    scripts = shop_scripts(shop["cfg"]) if shop["mode"] == "shopify" else ""
    write(path, h + body + footer() + scripts + close())


# ------------------------------------------------------------------------------------------------
# Static files
# ------------------------------------------------------------------------------------------------
REDIRECTS = [
    ("/private-fitness", "/personal-training/"), ("/yoga-mindfulness", "/classes/"), ("/yoga-minfulness-class-schedule", "/classes/"),
    ("/group-conditioning-classes", "/classes/"), ("/class-descriptions", "/classes/#styles"), ("/trainers", "/team/"),
    ("/copy-of-trainers-and-instructors", "/locations/"), ("/nutrition", "/nutrition-coaching/"), ("/fuel-your-life", "/nutrition-coaching/"),
    ("/kitchen-consultation-clean-out", "/nutrition-coaching/"), ("/meal-planning", "/nutrition-coaching/"),
    ("/women-wellness", "/womens-wellness/"), ("/copy-of-women-s-health-peri-menopause", "/oncology-exercise/"),
    ("/recovery-therapeutics", "/recovery/"), ("/copy-of-recovery-therapeutics", "/recovery/#assisted-stretch"), ("/reiki", "/recovery/#reiki"),
    ("/physical-therapy", "/recovery/#physical-therapy"), ("/private-pilates", "/pilates/"), ("/corporate", "/corporate-wellness/"),
    ("/services-9", "/memberships/"), ("/special-events", "/events/"), ("/fit-shop", "/shop/"), ("/studio-and-program-policies", "/policies/"),
    ("/testimonials", "/"), ("/our-services", "/"), ("/general-1", "/"), ("/fitness", "/personal-training/"),
    ("/summerprograms", "/events/"), ("/fall-outdoor-programs", "/events/"), ("/online-offerings", "/classes/"), ("/fitplay-with-caregiver", "/events/"),
]


def write_static():
    pages = ["/", "/classes/", "/schedule/", "/memberships/", "/team/", "/locations/", "/westford/", "/groton/", "/events/", "/shop/", "/policies/", "/contact/"] + [f"/{s['slug']}/" for s in SERVICES]
    pri = {"/": "1.0", "/classes/": "0.9", "/contact/": "0.8"}
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><changefreq>{'weekly' if p in ('/', '/shop/') else 'monthly'}</changefreq><priority>{pri.get(p, '0.7')}</priority></url>\n" for p in pages)
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: {SITE}/sitemap.xml\n")
    redirects = "".join(f'[[redirects]]\n  from = "{a}"\n  to = "{b}"\n  status = 301\n  force = true\n\n' for a, b in REDIRECTS)
    toml = f"""[build]
  publish = "."

{redirects}[[headers]]
  for = "/images/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/js/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"

[[redirects]]
  from = "/assets/*"
  to = "/404.html"
  status = 404
  force = true

[[redirects]]
  from = "/data/*"
  to = "/404.html"
  status = 404
  force = true

[[redirects]]
  from = "/tools/*"
  to = "/404.html"
  status = 404
  force = true

[[redirects]]
  from = "/*"
  to = "/404.html"
  status = 404
"""
    open(os.path.join(ROOT, "netlify.toml"), "w").write(toml)
    mark = Image.open(os.path.join(ROOT, "images", "logo-mark.png")).convert("RGBA")
    bg = Image.new("RGBA", (180, 180), (247, 242, 234, 255))
    m = mark.resize((150, 150), Image.LANCZOS)
    bg.paste(m, (15, 15), m)
    bg.convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"))
    bg.resize((32, 32), Image.LANCZOS).convert("RGB").save(os.path.join(ROOT, "favicon-32.png"))
    import base64
    import io
    buf = io.BytesIO()
    mark.resize((128, 128), Image.LANCZOS).save(buf, "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    open(os.path.join(ROOT, "favicon.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><image href="data:image/png;base64,{b64}" width="128" height="128"/></svg>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--products", default=os.path.join(ROOT, "tools", "shopify_products.json"))
    args = ap.parse_args()
    shop = load_shop(args.products)
    page_home(shop)
    for s in SERVICES:
        page_service(s)
    page_classes()
    page_schedule()
    page_memberships()
    page_team()
    page_locations()
    for l in LOCATIONS:
        page_location(l)
    page_events()
    page_policies()
    page_contact()
    page_thanks()
    page_404()
    page_shop(shop)
    write_static()
    print(f"built {len(SERVICES) + 13} pages; shop mode: {shop['mode']}")


if __name__ == "__main__":
    main()
