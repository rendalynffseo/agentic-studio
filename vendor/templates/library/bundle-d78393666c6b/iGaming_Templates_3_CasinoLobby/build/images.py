"""Turn raw images in images/src/ into optimised WebP files, and record their sizes for build.py.

Run:  python3 build/images.py      (needs Pillow: pip3 install pillow)

Put these in images/src/ (.png/.jpg/.jpeg/.webp). ALL optional: missing ones fall back to styled placeholders.
  logo.*             header wordmark (transparent PNG best)       -> logo.webp, 64px high
  banner-1.* ...     hero banner carousel (16:9, as many as you like) -> banner-N.webp 960w
  hero-casino.*      art for the "Casino" entry card (4:3)        -> 600x450
  hero-sports.*      art for the "Sports" entry card (4:3)        -> 600x450
  app.*              phone / app screenshot for App Download      -> app.webp 600w
  popup.*            phone-size promo for the popup (9:16)         -> popup.webp 540x960
  promos/<slug>.*    promo card image (16:9), slug = PROMOS in site_config -> 640x360
  games/<slug>.*     game tile (portrait 3:4), slug = GAMES in site_config  -> 300x400
  og.*               social share image (else made from banner-1) -> og.jpg 1200x630
"""
import glob
import json
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "images", "src")
OUT = os.path.join(ROOT, "images")
EXTS = (".png", ".jpg", ".jpeg", ".webp")


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def width(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im


def main():
    sizes = {}

    def save(im, name, q=76):
        os.makedirs(os.path.dirname(os.path.join(OUT, name)) or OUT, exist_ok=True)
        im.save(os.path.join(OUT, f"{name}.webp"), "WEBP", quality=q, method=6)
        sizes[name] = list(im.size)
        print(f"{name}.webp {im.size}")

    for path in sorted(glob.glob(os.path.join(SRC, "**", "*"), recursive=True)):
        rel, ext = os.path.splitext(os.path.relpath(path, SRC))
        if ext.lower() not in EXTS:
            continue
        rel = rel.replace(os.sep, "/")
        im = Image.open(path)
        if rel == "logo":
            im = im.convert("RGBA")
            save(im.resize((round(im.width * 64 / im.height), 64), Image.LANCZOS), "logo", 90)
            continue
        im = im.convert("RGB")
        if re.fullmatch(r"banner-\d+", rel):
            save(width(im, 960), rel)
        elif rel in ("hero-casino", "hero-sports"):
            save(cover(im, 600, 450), rel)
        elif rel == "popup":
            save(cover(im, 540, 960), rel, 78)
        elif rel == "app":
            save(width(im, 600), rel, 80)
        elif rel.startswith("promos/"):
            save(cover(im, 640, 360), rel)
        elif rel.startswith("games/"):
            save(cover(im, 300, 400), rel, 78)
    og_src = next((p for n in ("og", "banner-1", "hero-casino") for p in glob.glob(os.path.join(SRC, n + ".*"))), None)
    og = cover(Image.open(og_src).convert("RGB"), 1200, 630) if og_src else Image.new("RGB", (1200, 630), (15, 33, 46))
    og.save(os.path.join(OUT, "og.jpg"), quality=82, optimize=True)
    with open(os.path.join(OUT, "sizes.json"), "w") as fh:
        json.dump(sizes, fh, indent=1)
    print(f"og.jpg, sizes.json ({len(sizes)} images)")


if __name__ == "__main__":
    main()
