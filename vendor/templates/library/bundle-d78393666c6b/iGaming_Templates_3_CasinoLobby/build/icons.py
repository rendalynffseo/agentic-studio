"""Generate favicons + schema logo from LOGO_TEXT (accent tile, white italic text).

Run:  python3 build/icons.py   (re-run when LOGO_TEXT or THEME accent changes)
Outputs: images/logo-512.png, favicon.ico, favicon.svg, favicon-48.png, favicon-192.png, apple-touch-icon.png, site.webmanifest
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from site_config import BRAND, LOGO_TEXT, THEME  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCENT = THEME.get("accent", "#1475e1")
BG = THEME.get("side", "#0f212e")
FONT_PATHS = ["/System/Library/Fonts/Supplemental/Arial Black.ttf", "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(size):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def tile(n, text, scale=4):
    s = n * scale
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=round(s * .22), fill=rgb(ACCENT))
    size = round(s * .7)
    f = font(size)
    while d.textlength(text, font=f) > s * .8 and size > 8:
        size -= 4
        f = font(size)
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((s - (bb[2] - bb[0])) / 2 - bb[0], (s - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=(255, 255, 255))
    return im.resize((n, n), Image.LANCZOS)


def main():
    short = LOGO_TEXT[:2] if len(LOGO_TEXT) > 3 else LOGO_TEXT
    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    tile(512, LOGO_TEXT).save(os.path.join(ROOT, "images", "logo-512.png"))
    tile(48, short).save(os.path.join(ROOT, "favicon-48.png"))
    tile(192, LOGO_TEXT).save(os.path.join(ROOT, "favicon-192.png"))
    bg = Image.new("RGB", (180, 180), rgb(BG))
    t = tile(180, LOGO_TEXT)
    bg.paste(t, (0, 0), t)
    bg.save(os.path.join(ROOT, "apple-touch-icon.png"))
    tile(256, short).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    fs = {1: 20, 2: 15, 3: 11}.get(len(short), 9)
    with open(os.path.join(ROOT, "favicon.svg"), "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="{ACCENT}"/>'
                 f'<text x="16" y="{16 + fs * .36:.0f}" font-size="{fs}" font-family="Arial Black,Arial" font-weight="900" font-style="italic" text-anchor="middle" fill="#fff">{short}</text></svg>')
    with open(os.path.join(ROOT, "site.webmanifest"), "w") as fh:
        json.dump({"name": BRAND, "short_name": BRAND, "background_color": BG, "theme_color": BG, "display": "standalone",
                   "icons": [{"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"},
                             {"src": "/images/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, fh)
    print("favicons + logo-512 written")


if __name__ == "__main__":
    main()
