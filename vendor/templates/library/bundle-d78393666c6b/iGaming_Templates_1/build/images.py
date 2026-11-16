"""Turn raw images in images/src/ into the optimised WebP files the site uses.

Run:  python3 build/images.py
Needs Pillow (pip3 install pillow).

Put these in images/src/ (any of .png/.jpg/.jpeg/.webp):
  popup-banner.*   phone-size portrait promo for the popup (9:16, centre-cropped) -> popup-banner.webp 540x960 + .jpg
  showcase-1.*     wide banner beside the games grid    -> showcase-1.webp (799w)  [loads eagerly, top of page]
  showcase-2.*     second image beside it               -> showcase-2.webp (800w)
  showcase-3.*     "live transactions" style strip      -> showcase-3.webp (799w)
  preview.*        full platform screenshot             -> preview.webp (1100w) + .jpg (og:image)
  games/<slug>.*   square game tiles (slug = GAMES in site_config.py) -> games/<slug>.webp 170x170
"""
import glob
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "images", "src")
OUT = os.path.join(ROOT, "images")
WIDTHS = {"popup-banner": 684, "showcase-1": 799, "showcase-2": 800, "showcase-3": 799, "preview": 1100}
KEEP_JPG = {"popup-banner", "preview"}


def find(name):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(SRC, f"{name}.{ext}")
        if os.path.exists(p):
            return p


def main():
    for name, w in WIDTHS.items():
        src = find(name)
        if not src:
            print(f"skip {name} (not in images/src)")
            continue
        im = Image.open(src).convert("RGB")
        if name == "popup-banner":  # phone size 9:16
            th = round(im.width * 16 / 9)
            if th <= im.height:
                top = (im.height - th) // 2
                im = im.crop((0, top, im.width, top + th))
            else:
                tw = round(im.height * 9 / 16)
                left = (im.width - tw) // 2
                im = im.crop((left, 0, left + tw, im.height))
            im = im.resize((540, 960), Image.LANCZOS)
        elif im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT, f"{name}.webp"), "WEBP", quality=72, method=6)
        if name in KEEP_JPG:
            im.save(os.path.join(OUT, f"{name}.jpg"), quality=80, optimize=True)
        print(f"{name}.webp {im.size}")
    os.makedirs(os.path.join(OUT, "games"), exist_ok=True)
    for src in glob.glob(os.path.join(SRC, "games", "*")):
        slug = os.path.splitext(os.path.basename(src))[0]
        im = Image.open(src).convert("RGB")
        side = min(im.size)  # centre-crop to square
        left, top = (im.width - side) // 2, (im.height - side) // 2
        im = im.crop((left, top, left + side, top + side)).resize((170, 170), Image.LANCZOS)
        im.save(os.path.join(OUT, "games", f"{slug}.webp"), "WEBP", quality=78, method=6)
        print(f"games/{slug}.webp")


if __name__ == "__main__":
    main()
