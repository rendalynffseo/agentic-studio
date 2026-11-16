"""Generate favicons (from LOGO_ICON) and the logo PNGs (from LOGO_PARTS) in the THEME accent.

Run:  python3 build/icons.py   (re-run when LOGO_PARTS, LOGO_ICON or THEME accent changes)
Outputs: images/logo-512.png (square, Organization schema), images/logo-wordmark.png (wide, 1200x300),
         favicon.ico, favicon.svg, favicon-48.png, favicon-192.png, apple-touch-icon.png, site.webmanifest
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from site_config import BRAND, LOGO_PARTS, LOGO_ICON, THEME  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCENT = THEME.get("accent", "#FF8C00")
ACCENT2 = THEME.get("accent-2", "#FFB020")
DARK = "#1B1B1F"
FONTS = [os.path.join(ROOT, "assets", "fonts", "outfit-800.ttf"), "/System/Library/Fonts/Supplemental/Arial Black.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def gradient(s):
    a, b = rgb(ACCENT2), rgb(ACCENT)
    g = Image.new("RGB", (1, s))
    for y in range(s):
        t = y / max(1, s - 1)
        g.putpixel((0, y), tuple(round(p + (q - p) * t) for p, q in zip(a, b)))
    return g.resize((s, s))


def icon(n, text, scale=4):
    s = n * scale
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), radius=round(s * .24), fill=255)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    im.paste(gradient(s), (0, 0), mask)
    d = ImageDraw.Draw(im)
    size = round(s * (.62 if len(text) == 1 else .46))
    f = font(size)
    while d.textlength(text, font=f) > s * .8 and size > 8:
        size -= 4
        f = font(size)
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((s - (bb[2] - bb[0])) / 2 - bb[0], (s - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill=(255, 255, 255))
    return im.resize((n, n), Image.LANCZOS)


def wordmark(w=1200, h=300):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    size = 220
    f = font(size)
    while sum(d.textlength(t, font=f) for t, _ in LOGO_PARTS) > w * .92 and size > 20:
        size -= 6
        f = font(size)
    total = sum(d.textlength(t, font=f) for t, _ in LOGO_PARTS)
    bb = d.textbbox((0, 0), "".join(t for t, _ in LOGO_PARTS), font=f)
    x, y = (w - total) / 2, (h - (bb[3] - bb[1])) / 2 - bb[1]
    for t, c in LOGO_PARTS:
        d.text((x, y), t, font=f, fill=rgb(ACCENT if c == "a" else DARK))
        x += d.textlength(t, font=f)
    return im


def main():
    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    icon(512, LOGO_ICON).save(os.path.join(ROOT, "images", "logo-512.png"))
    wordmark().save(os.path.join(ROOT, "images", "logo-wordmark.png"))
    icon(48, LOGO_ICON).save(os.path.join(ROOT, "favicon-48.png"))
    icon(192, LOGO_ICON).save(os.path.join(ROOT, "favicon-192.png"))
    bg = Image.new("RGB", (180, 180), (255, 255, 255))
    t = icon(180, LOGO_ICON)
    bg.paste(t, (0, 0), t)
    bg.save(os.path.join(ROOT, "apple-touch-icon.png"))
    icon(256, LOGO_ICON).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    fs = 19 if len(LOGO_ICON) == 1 else 14
    with open(os.path.join(ROOT, "favicon.svg"), "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="{ACCENT2}"/><stop offset="1" stop-color="{ACCENT}"/></linearGradient></defs>'
                 f'<rect width="32" height="32" rx="8" fill="url(#g)"/><text x="16" y="{16 + fs * .36:.0f}" font-size="{fs}" '
                 f'font-family="Arial Black,Arial" font-weight="900" text-anchor="middle" fill="#fff">{LOGO_ICON}</text></svg>')
    with open(os.path.join(ROOT, "site.webmanifest"), "w") as fh:
        json.dump({"name": f"{BRAND} Malaysia", "short_name": BRAND, "background_color": "#ffffff", "theme_color": ACCENT, "display": "standalone",
                   "icons": [{"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"},
                             {"src": "/images/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, fh)
    print("logo-512, logo-wordmark, favicons written")


if __name__ == "__main__":
    main()
