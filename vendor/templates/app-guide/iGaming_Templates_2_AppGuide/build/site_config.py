# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) and nothing else.
#  Example values below are from the Mega88 Mobi site (mega88mobi.com).
# ============================================================

# --- Brand ---
BRAND = "Mega88"              # the app/brand the guide is about; replaces __BRAND__ everywhere
BRAND_ALT = "Mega888"         # common alternative spelling, used once in the overview ("" to skip)
SLUG = "mega88"               # lowercase, used in blog URLs, e.g. /blog/__SLUG__-login-fix/
SITE_NAME = "Mega88 Mobi"     # name of THIS guide site (header, schema, titles); replaces __SITE__
TAGLINE = "App Guide & Review"  # small text under the site name in the header
LOGO_TEXT = "M"               # 1-2 characters on the generated logo/favicon

# --- Domain & links ---
SITE = "https://mega88mobi.com"                      # no trailing slash
REGISTER_URL = "https://hideyourmess.com/go/mega88mobi"  # header button, banner, hero promo, popup, floating footer (rel=sponsored)
LOGIN_URL = REGISTER_URL  # floating footer "Login" button
EMAIL = "support@mega88mobi.com"

# --- Languages ---
# The LOCAL language is always first (main): it lives at "/", the others at "/<code>/".
# Available: "ms", "en", "zh" (text in build/content.py). pages.py + posts.py are written in the main language.
LANGS = ["ms", "en", "zh"]

# --- SEO keywords: built from the keyword list the user gives for this site (main language first) ---
# Home <meta name="keywords"> per language; hubs/policies use the main language list. Posts set their own "kw".
# The same keywords drive the blog clusters in posts.py (see CLAUDE.md "From keywords to site").
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "aplikasi __BRAND__", "__BRAND__ apk", "download __BRAND__", "__BRAND__ login", "__BRAND__ daftar"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ app", "__BRAND__ apk download", "__BRAND__ login", "__BRAND__ register"],
    "zh": ["__BRAND__", "__BRAND__ 马来西亚", "__BRAND__ 应用", "__BRAND__ 下载", "__BRAND__ 登录"],
}

# --- Author / editor (E-E-A-T). Use a real person and real details. ---
AUTHOR = {
    "name": "Amirul Hafiz bin Razali",
    "role": "Penganalisis Permainan Mudah Alih",
    "city": "Kuala Lumpur",
    "photo": "author",   # images/author.webp (from images/src/author.*); "" = initials tile
    "bio": "Amirul menyunting panduan bebas __SITE__. Fokusnya ialah sisi praktikal aplikasi kasino mudah alih yang boleh disahkan: cara pemasang berfungsi, cara FPX, DuitNow dan e-dompet menggerakkan wang, maksud sebenar RTP dan volatiliti, serta cara mengenal pasti penipuan dan kekal terkawal.",  # main language
    "same_as": [],       # e.g. ["https://www.linkedin.com/in/..."]
}

# --- Contact block in footer + Organization schema. Leave ADDRESS = [] to hide address and map. ---
ADDRESS = ["Suite 15-01, Menara Kuala Lumpur, Jalan Puncak,", "50250 Kuala Lumpur, Wilayah Persekutuan, Malaysia"]
PHONE = "+603-2026-8888"           # "" to hide
MAP_QUERY = "Menara Kuala Lumpur"  # Google Maps embed query; "" to hide the map
GEO = {"region": "MY-14", "place": "Kuala Lumpur", "lat": "3.1390", "lng": "101.6869"}  # {} to skip geo meta

# --- Dates (YYYY-MM-DD) ---
PUBLISHED = "2026-07-10"
UPDATED = "2026-09-28"

# --- Verification & analytics ("" to skip each) ---
GSC_VERIFICATION = "x0ko_VqbaAYgoYp1NT2TSjaCfgmtbAJDTf7QC7PpzRk"   # NEW SITE: replace or ""
BING_VERIFICATION = "178CB0AC75C0A1B4491D8189E8B84F6A"             # NEW SITE: replace or ""
GA4_ID = "G-0F3KRKBTR7"            # loaded after first interaction (keeps PageSpeed high). NEW SITE: replace or ""
EXTRA_BODY_END = '<script src="https://walangtalo.com/js/wt-tracker.js" defer></script>'  # raw HTML before </body>

# --- Cloudflare Pages ---
CF_PROJECT = "mega88mobi"

# --- Sidebar "Quick facts" (label, value) per language; keep to facts you can stand behind ---
QUICK_FACTS = {
    "en": [("Platforms", "Android · iOS"), ("Category", "Slots · Arcade"), ("Install", "Side-load"), ("Age rating", "18+"), ("Cost of guide", "Free")],
    "ms": [("Platform", "Android · iOS"), ("Kategori", "Slot · Arked"), ("Pemasangan", "Side-load"), ("Had umur", "18+"), ("Kos panduan", "Percuma")],
    "zh": [("平台", "Android · iOS"), ("类别", "老虎机 · 街机"), ("安装方式", "侧载安装"), ("年龄限制", "18+"), ("指南费用", "免费")],
}

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} keeps ink + gold. ---
# Keep "gold-rgb" in sync with "gold". Example emerald: {"gold": "#2EC27E", "gold-soft": "#7DF0B5", "gold-deep": "#1A8F57", "gold-rgb": "46,194,126"}
THEME = {}
