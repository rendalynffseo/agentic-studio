"""Generate favicons and the square brand logo from the logo text.

Run:  python3 build/icons.py   (re-run only when the logo text or colours change)
Outputs (project root):
  favicon.ico (16/32/48), favicon-48.png, favicon-192.png, apple-touch-icon.png (180),
  images/logo-512.png (square logo used in Organization schema), site.webmanifest, favicon.svg
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
try:
    from site_config import BRAND, LOGO_A, LOGO_B  # template layout
except ImportError:
    BRAND, LOGO_A, LOGO_B = "RA88", "RA", "88"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RED_TOP, RED_BOTTOM, GOLD, WHITE = (199, 44, 44), (90, 13, 15), (255, 215, 0), (255, 255, 255)
FONT_PATHS = ["/System/Library/Fonts/Supplemental/Arial Black.ttf",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def font(size):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def fit(draw, parts, box_w, box_h):
    """Largest font size at which the text parts fit the box."""
    size = box_h
    while size > 6:
        f = font(size)
        w = sum(draw.textlength(t, font=f) for t, _ in parts)
        bb = f.getbbox("".join(t for t, _ in parts))
        if w <= box_w and bb[3] - bb[1] <= box_h:
            return f
        size -= 2
    return font(size)


def tile(n, parts, scale=4):
    s = n * scale  # draw large, then downsample for smooth edges
    grad = Image.new("RGB", (1, s))
    for y in range(s):
        t = y / (s - 1)
        grad.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(RED_TOP, RED_BOTTOM)))
    bg = grad.resize((s, s))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), radius=s // 5, fill=255)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    im.paste(bg, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * .04, s * .04, s * .96, s * .96), radius=s // 6, outline=GOLD, width=max(1, s // 28))
    f = fit(d, parts, s * .78, s * .5)
    total = sum(d.textlength(t, font=f) for t, _ in parts)
    bb = f.getbbox("".join(t for t, _ in parts))
    x, y = (s - total) / 2, (s - (bb[3] - bb[1])) / 2 - bb[1]
    for t, colour in parts:
        d.text((x, y), t, font=f, fill=colour)
        x += d.textlength(t, font=f)
    return im.resize((n, n), Image.LANCZOS)


def main():
    small = [(LOGO_B, GOLD)]               # favicons: short part only, readable at 16px
    full = [(LOGO_A, GOLD), (LOGO_B, WHITE)]  # logo + touch icon: full wordmark
    tile(48, small).save(os.path.join(ROOT, "favicon-48.png"))
    tile(192, full).save(os.path.join(ROOT, "favicon-192.png"))
    tile(180, full).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"))
    tile(512, full).save(os.path.join(ROOT, "images", "logo-512.png"))
    tile(256, small).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    with open(os.path.join(ROOT, "site.webmanifest"), "w") as fh:
        json.dump({"name": BRAND, "short_name": BRAND, "icons": [
            {"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/images/logo-512.png", "sizes": "512x512", "type": "image/png"}],
            "theme_color": "#5a0d0f", "background_color": "#5a0d0f", "display": "browser"}, fh)
    with open(os.path.join(ROOT, "favicon.svg"), "w") as fh:
        fh.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
                 '<stop offset="0" stop-color="#c72c2c"/><stop offset="1" stop-color="#5a0d0f"/></linearGradient></defs>'
                 '<rect width="64" height="64" rx="13" fill="url(#g)"/><rect x="3" y="3" width="58" height="58" rx="11" fill="none" stroke="#ffd700" stroke-width="3"/>'
                 f'<text x="32" y="43" font-family="Arial Black,Arial,sans-serif" font-size="{28 if len(LOGO_B) <= 2 else 18}" font-weight="900" text-anchor="middle" fill="#ffd700">{LOGO_B}</text></svg>')
    print("icons written")


if __name__ == "__main__":
    main()
