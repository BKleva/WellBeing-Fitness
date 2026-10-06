"""Turn raw Mindbody extractions into data/mindbody.json (the schedule + events snapshot the site is built from).

Run:  python tools/import_mindbody.py <folder with sched_w*.json and ev_*.json>
See tools/mindbody_refresh.md for how those raw files are captured from the studio's Mindbody pages.
"""
import datetime
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "data", "mindbody.json")
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 1)}

LOC = {"1": "Westford", "2": "Groton"}


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


def loc_of(name, code=""):
    n = name.lower()
    if "westford" in n:
        return "Westford"
    if "groton" in n:
        return "Groton"
    return LOC.get(code, "")


def iso_from_day(label):
    m = re.search(r"([A-Za-z]+) (\d+), (\d{4})", label)
    return datetime.date(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2))).isoformat()


def hhmm(label):
    m = re.search(r"(\d+):(\d+)\s*(am|pm)", label, re.I)
    h, mi, ap = int(m.group(1)) % 12, int(m.group(2)), m.group(3).lower()
    return f"{h + (12 if ap == 'pm' else 0):02d}:{mi:02d}"


def minutes(label):
    h = re.search(r"(\d+)\s*hour", label or "")
    m = re.search(r"(\d+)\s*minute", label or "")
    return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)


def classes(path):
    out = []
    for r in json.load(open(path, encoding="utf8")):
        name = clean(r["name"])
        name = re.sub(r"\s*-\s*(Groton|Westford)( Studio)?$", "", name)
        name = re.sub(r"\s*-\s*$", "", name)
        out.append({
            "date": iso_from_day(r["day"]), "start": hhmm(r["time"]), "name": name, "teacher": clean(r["teacher"]),
            "loc": loc_of(r["loc"], r.get("clsLoc", "")), "min": minutes(r["dur"]),
            "id": r.get("classId", ""), "tg": r.get("tg", ""), "clsLoc": r.get("clsLoc", ""),
            "open": int(r["open"]) if r.get("open") not in ("", None) else None,
        })
    return out


def events(paths):
    seen, out = set(), []
    for p in paths:
        for e in json.load(open(p, encoding="utf8")):
            m, d, y = (int(x) for x in e["date"].split("/"))
            iso = datetime.date(y, m, d).isoformat()
            times = re.split(r"\s*-\s*", e["time"])
            key = (e["title"], iso, e["time"])
            if key in seen:
                continue
            seen.add(key)
            desc = clean(e["desc"])
            price = re.findall(r"\$\d[\d,.]*[^$]{0,60}", desc)
            out.append({
                "title": clean(e["title"]), "teacher": clean(e["teacher"]), "loc": loc_of(e["loc"], e.get("clsLoc", "")),
                "date": iso, "start": hhmm(times[0]), "end": hhmm(times[-1]) if len(times) > 1 else "", "desc": desc,
                "notes": clean(e.get("notes", "")), "id": e.get("classId", ""), "tg": e.get("tg", ""), "clsLoc": e.get("clsLoc", ""),
                "img": e.get("img", ""), "price": [clean(x) for x in price][:2],
            })
    return sorted(out, key=lambda e: (e["date"], e["start"]))


def main(folder):
    sched = []
    for p in sorted(glob.glob(os.path.join(folder, "sched_w*.json"))):
        sched += classes(p)
    sched.sort(key=lambda c: (c["date"], c["start"]))
    ev = events(sorted(glob.glob(os.path.join(folder, "ev_*.json"))))
    data = {"generated": datetime.date.today().isoformat(), "from": sched[0]["date"], "to": sched[-1]["date"], "classes": sched, "events": ev}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(f"{len(sched)} classes ({data['from']} to {data['to']}), {len(ev)} events -> {OUT}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
