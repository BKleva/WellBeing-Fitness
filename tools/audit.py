"""Quick QA over the built site: broken internal links/anchors/assets, duplicate or over-long titles and descriptions, H1 count.

Run:  python tools/audit.py      (from the wellbeing-fitness folder, after build.py)
"""
import glob
import html
import os
import re
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pages = {}
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
    if rel.startswith(("assets/", "tools/")):
        continue
    pages["/" + rel.replace("index.html", "")] = open(f, encoding="utf8").read()
print(len(pages), "pages")

ids = {p: set(re.findall(r'\bid="([^"]+)"', h)) for p, h in pages.items()}
bad, titles, descs = [], Counter(), Counter()
for p, h in pages.items():
    t = re.search(r"<title>(.*?)</title>", h).group(1)
    d = re.search(r'<meta name="description" content="(.*?)"', h).group(1)
    titles[t] += 1
    descs[d] += 1
    n1 = len(re.findall(r"<h1[ >]", h))
    if n1 != 1:
        bad.append((p, "h1 count", n1))
    if len(html.unescape(t)) > 65:
        bad.append((p, "title length", len(html.unescape(t))))
    if len(html.unescape(d)) > 165:
        bad.append((p, "description length", len(html.unescape(d))))
    for href in re.findall(r'href="([^"]+)"', h):
        if href.startswith(("http", "mailto:", "tel:")):
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in ids[p]:
                bad.append((p, "missing anchor", href))
            continue
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        if not path:
            continue
        last = path.split("/")[-1]
        if "." in last and not path.endswith(".html"):
            if not os.path.exists(ROOT + path):
                bad.append((p, "missing file", href))
            continue
        tgt = path if path.endswith(("/", ".html")) else path + "/"
        if tgt not in pages:
            bad.append((p, "broken link", href))
        elif frag and frag not in ids[tgt]:
            bad.append((p, "missing anchor", href))
    for src in re.findall(r'(?:src|srcset|href)="([^"]+)"', h):
        for s in re.findall(r"(/[^\s,\"]+\.(?:webp|png|jpg|js|css|svg))", src):
            if not os.path.exists(ROOT + s):
                bad.append((p, "missing asset", s))

print("duplicate titles:", [t for t, c in titles.items() if c > 1])
print("duplicate descriptions:", [t for t, c in descs.items() if c > 1])
for b in sorted(set(bad), key=str):
    print(b)
print("issues:", len(set(bad)))
