"""Generate the logo, favicons and schema logo from LOGO_TEXT (gold tile, dark letter, like the reference site).

Run:  python3 build/icons.py   (re-run when LOGO_TEXT or THEME gold changes)
Outputs: images/logo.webp (68px, shown at 34px), images/logo-512.png (Organization schema),
         favicon.ico, favicon.svg, favicon-48.png, favicon-192.png, apple-touch-icon.png, site.webmanifest (project root)
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from site_config import SITE_NAME, LOGO_TEXT, THEME  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = THEME.get("ink", "#0B0D12")
GOLD = THEME.get("gold", "#F5B301")
GOLD_DEEP = THEME.get("gold-deep", "#C88E00")
FONT_PATHS = ["/System/Library/Fonts/Supplemental/Arial Black.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(size):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def tile(n, scale=4):
    s = n * scale  # draw large, downsample for smooth edges
    a, b = rgb(GOLD), rgb(GOLD_DEEP)
    grad = Image.new("RGB", (s, s))
    px = grad.load()
    for y in range(s):
        for x in range(0, s, 4):
            t = (x + y) / (2 * s)
            c = tuple(round(p + (q - p) * t) for p, q in zip(a, b))
            for k in range(4):
                if x + k < s:
                    px[x + k, y] = c
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), radius=round(s * .26), fill=255)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    size = round(s * (.62 if len(LOGO_TEXT) == 1 else .44))
    f = font(size)
    while d.textlength(LOGO_TEXT, font=f) > s * .8 and size > 8:
        size -= 4
        f = font(size)
    bb = d.textbbox((0, 0), LOGO_TEXT, font=f)
    d.text(((s - (bb[2] - bb[0])) / 2 - bb[0], (s - (bb[3] - bb[1])) / 2 - bb[1]), LOGO_TEXT, font=f, fill=rgb(INK))
    return im.resize((n, n), Image.LANCZOS)


def main():
    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    tile(68).save(os.path.join(ROOT, "images", "logo.webp"), "WEBP", quality=90)
    tile(512).save(os.path.join(ROOT, "images", "logo-512.png"))
    tile(48).save(os.path.join(ROOT, "favicon-48.png"))
    tile(192).save(os.path.join(ROOT, "favicon-192.png"))
    bg = Image.new("RGB", (180, 180), rgb(INK))
    bg.paste(tile(180), (0, 0), tile(180))
    bg.save(os.path.join(ROOT, "apple-touch-icon.png"))
    tile(256).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    fs = 18 if len(LOGO_TEXT) == 1 else 13
    with open(os.path.join(ROOT, "favicon.svg"), "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="{GOLD}"/>'
                 f'<text x="16" y="{16 + fs * .36:.0f}" font-size="{fs}" font-family="Arial Black,Arial" font-weight="900" text-anchor="middle" fill="{INK}">{LOGO_TEXT}</text></svg>')
    with open(os.path.join(ROOT, "site.webmanifest"), "w") as fh:
        json.dump({"name": SITE_NAME, "short_name": SITE_NAME, "background_color": INK, "theme_color": INK, "display": "standalone",
                   "icons": [{"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"},
                             {"src": "/images/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, fh)
    print("logo + favicons written")


if __name__ == "__main__":
    main()
