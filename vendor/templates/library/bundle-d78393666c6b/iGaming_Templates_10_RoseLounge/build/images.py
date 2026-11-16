"""Turn raw images in images/src/ into optimised WebP files and record their sizes for build.py.

Run:  python3 build/images.py      (needs Pillow: pip3 install pillow)

ALL images are SQUARE (centre-cropped) except the banner, popup and og. All optional: missing ones get a styled fallback.
  banner.*                 promo banner above the hero            -> banner.webp 900x500 (exact)
  popup.*                  phone-size popup                       -> popup.webp 540x960 (9:16)
  hero.*                   home hero art                          -> hero.webp 640x640
  about, deposit, sports, live, app, bingo, responsible  home split-section art (any other top-level name) -> 640x640
  logo.*                   header logo (transparent PNG) instead of the text wordmark -> logo.webp 88px high
  categories/<page key>.*  game/info page art (keys in pages.py)  -> 480x480
  promos/<image name>.*    promo cards (PROMOS in site_config)    -> 480x480
  posts/<post key>.*       blog post image (keys in posts.py)     -> 600x600
  og.*                     social share 1200x630 (else made from banner)
"""
import glob
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "images", "src")
OUT = os.path.join(ROOT, "images")
SQUARE = {"hero": 640, "about": 640, "app": 640, "categories": 480, "promos": 480, "posts": 600}


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def main():
    sizes = {}

    def save(im, name, q=78):
        os.makedirs(os.path.dirname(os.path.join(OUT, name)), exist_ok=True)
        im.save(os.path.join(OUT, f"{name}.webp"), "WEBP", quality=q, method=6)
        sizes[name] = list(im.size)
        print(f"{name}.webp {im.size}")

    for path in sorted(glob.glob(os.path.join(SRC, "**", "*"), recursive=True)):
        rel, ext = os.path.splitext(os.path.relpath(path, SRC))
        if ext.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        rel = rel.replace(os.sep, "/")
        group = rel.split("/")[0]
        im = Image.open(path)
        if rel == "logo":
            im = im.convert("RGBA")
            save(im.resize((round(im.width * 88 / im.height), 88), Image.LANCZOS), "logo", 90)
            continue
        im = im.convert("RGB")
        if rel == "banner":
            save(cover(im, 900, 500), rel, 80)
        elif rel == "popup":
            save(cover(im, 540, 960), rel)
        elif rel != "og" and (group in SQUARE or "/" not in rel):
            side = SQUARE.get(group, 640)
            save(cover(im, side, side), rel)
    og_src = next((p for n in ("og", "banner", "hero") for p in glob.glob(os.path.join(SRC, n + ".*"))), None)
    og = cover(Image.open(og_src).convert("RGB"), 1200, 630) if og_src else Image.new("RGB", (1200, 630), (251, 113, 133))
    og.save(os.path.join(OUT, "og.jpg"), quality=82, optimize=True)
    with open(os.path.join(OUT, "sizes.json"), "w") as fh:
        json.dump(sizes, fh, indent=1)
    print(f"og.jpg + sizes.json ({len(sizes)} images)")


if __name__ == "__main__":
    main()
