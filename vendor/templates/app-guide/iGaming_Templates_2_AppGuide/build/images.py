"""Turn raw images in images/src/ into the optimised files the site uses, and record their sizes.

Run:  python3 build/images.py      (needs Pillow: pip3 install pillow)

Put these in images/src/ (any of .png/.jpg/.jpeg/.webp). All optional; missing ones are simply left out of the page.
  banner.*   wide promo banner above the hero (LCP on home, links to REGISTER_URL) -> banner.webp 1600w + banner-900.webp
  promo.*    square promo beside the hero headline (links to REGISTER_URL)       -> promo.webp 720x720
  popup.*    phone-size promo for the popup (9:16, centre-cropped)          -> popup.webp 540x960
  author.*   editor photo for /about-author/                                     -> author.webp 300x300
  og.*       social share image                                                  -> og.jpg 1200x630
             (no og.*: made from banner, else promo, else a plain ink tile)
Writes images/sizes.json, which build.py reads for width/height attributes.
"""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "images", "src")
OUT = os.path.join(ROOT, "images")
SIZES_FILE = os.path.join(OUT, "sizes.json")


def find(name):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(SRC, f"{name}.{ext}")
        if os.path.exists(p):
            return p


def resize_w(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im


def square(im, side):
    s = min(im.size)
    left, top = (im.width - s) // 2, (im.height - s) // 2
    return im.crop((left, top, left + s, top + s)).resize((side, side), Image.LANCZOS)


def cover(im, w, h):
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def main():
    sizes = json.load(open(SIZES_FILE)) if os.path.exists(SIZES_FILE) else {}

    def save(im, name, ext="webp", q=74):
        im.save(os.path.join(OUT, f"{name}.{ext}"), "WEBP" if ext == "webp" else "JPEG", quality=q, **({"method": 6} if ext == "webp" else {"optimize": True}))
        sizes[name] = list(im.size)
        print(f"{name}.{ext} {im.size}")

    srcs = {n: find(n) for n in ("banner", "promo", "popup", "author", "og")}
    if srcs["banner"]:
        im = Image.open(srcs["banner"]).convert("RGB")
        save(resize_w(im, 1600), "banner")
        save(resize_w(im, 900), "banner-900")
    if srcs["promo"]:
        save(square(Image.open(srcs["promo"]).convert("RGB"), 720), "promo", q=78)
    if srcs["popup"]:
        save(cover(Image.open(srcs["popup"]).convert("RGB"), 540, 960), "popup", q=78)
    if srcs["author"]:
        save(square(Image.open(srcs["author"]).convert("RGB"), 300), "author", q=80)
    og_src = srcs["og"] or srcs["banner"] or srcs["promo"]
    og = cover(Image.open(og_src).convert("RGB"), 1200, 630) if og_src else Image.new("RGB", (1200, 630), (11, 13, 18))
    save(og, "og", "jpg", 82)
    with open(SIZES_FILE, "w") as fh:
        json.dump(sizes, fh, indent=1)


if __name__ == "__main__":
    main()
