"""One-off image prep: turns the raw downloads in assets/raw into optimized WebP files in /images.

Run:  python tools/prep_images.py      (from the wellbeing-fitness folder)
The raw files are numbered in the order they appear in assets/manifest.txt (pulled from the live Wix site).
"""
import glob
import os

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "assets", "raw")
OUT = os.path.join(ROOT, "images")
os.makedirs(OUT, exist_ok=True)


def raw(n):
    return Image.open(glob.glob(os.path.join(RAW, f"{n:03d}.*"))[0]).convert("RGB")


def save(im, name, width=None, q=80):
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=q, method=6)


# --- scenes: large + medium variants ----------------------------------------------------------
SCENES = {
    "hero-meditate": 0, "studio-om-room": 9, "studio-yoga-light": 15, "studio-fitness-floor": 14,
    "studio-weights": 18, "studio-yoga-room": 59, "class-core": 19, "class-warrior": 20,
    "runners": 2, "shoelace": 4, "nutrition-market": 1, "nutrition-prep": 11, "meal-prep": 29,
    "nutrition-bowl": 30, "sunrise": 16, "friends": 23, "reiki": 25, "yin-block": 66,
    "private-training": 67, "assisted-stretch": 68, "physical-therapy": 47, "oncology": 43,
    "womens-wellness": 27, "corporate-meeting": 24, "corporate-planning": 10, "pilates-ring": 58,
    "reformer": 60, "prop-shelf": 61, "kettlebells": 65, "skyline": 70, "groton-building": 28,
    "westford-building": 45, "yoga-class-wide": 17, "yoga-class": 12, "radiance-poster": 8,
}
for name, n in SCENES.items():
    im = raw(n)
    save(im, name + "-1400", 1400, 78)
    save(im, name + "-800", 800, 76)

# --- team portraits -------------------------------------------------------------------------------
PEOPLE = {
    "scott-cassa": 44, "melissa-matheson": 3, "ron-rigazio": 7, "meghan-kwartler": 6,
    "chris-kandianis": 13, "shagufta-rahmen": 12, "melissa-ackerman": 57, "mackenzie-fitzgerald": 55,
    "violet-young": 41, "lisa-siemaszko": 33, "erica-cahill": 64, "eleonora-cordovani": 62,
    "nancy-slocum": 42, "dan-digiacomo": 48, "megan-willwerth": 50, "darleen-murray": 52,
    "nancy-bonanno": 56, "val-templeton": 37, "denise-legrow": 53, "brenda-doben": 26,
    "jason-brady": 31, "krista-simon": 39, "julia": 63,
}
for name, n in PEOPLE.items():
    save(raw(n), "team-" + name, 720, 80)

# --- merch crops (from the Bonfire catalog screenshots on the Wix site) ----------------------------------
def crop(n, box, name):
    im = raw(n).crop(box)
    save(im, name, 700, 85)

crop(46, (80, 85, 360, 340), "merch-blues-tee")
crop(46, (390, 85, 660, 340), "merch-white-tee")
crop(46, (690, 55, 970, 340), "merch-runner-hoodie")
crop(54, (55, 55, 350, 318), "merch-zip-up")
crop(54, (400, 70, 640, 318), "merch-jogger")
crop(54, (680, 70, 965, 310), "merch-peace-crewneck")
save(raw(34), "merch-tote", 700, 85)
save(raw(51), "merch-tank", 700, 85)

# --- logo: pull the mark out of the pricing flyer and make transparent navy / white versions -----------------
flyer = Image.open(glob.glob(os.path.join(RAW, "040.*"))[0]).convert("RGB")
logo = flyer.crop((16, 148, 404, 240))
NAVY = (22, 41, 97)
gray = logo.convert("L")
for tag, colour in (("navy", NAVY), ("white", (255, 255, 255))):
    out = Image.new("RGBA", logo.size, colour + (0,))
    alpha = gray.point(lambda v: 0 if v > 228 else max(0, min(255, int((235 - v) * 1.5))))
    out.putalpha(alpha)
    bbox = out.getbbox()
    out = out.crop(bbox)
    out = out.resize((out.width * 2, out.height * 2), Image.LANCZOS)
    out.save(os.path.join(OUT, f"logo-{tag}.png"), optimize=True)
    if tag == "navy":
        out.crop((0, 0, out.height, out.height)).save(os.path.join(OUT, "logo-mark.png"), optimize=True)
    print("logo", tag, out.size)

# --- open-graph card (1200x630 crop of the om room) ---------------------------------------------------------------
og = raw(9)
w, h = og.size
target = 1200 / 630
nh = int(w / target)
top = max(0, (h - nh) // 2)
og = og.crop((0, top, w, top + nh)).resize((1200, 630), Image.LANCZOS)
og.save(os.path.join(OUT, "og-card.jpg"), quality=82)
print("done", len(os.listdir(OUT)), "files")
