# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: BILA2WIN (structure from bila2win.my). Replace every value for a new site.
# ============================================================

# --- Brand ---
BRAND = "BILA2WIN"            # replaces __BRAND__ everywhere
SLUG = "bila2win"             # lowercase, used in some post slugs via __SLUG__
# Logo wordmark = parts drawn in order; colour "a" = accent (THEME accent), "d" = dark text. Also used for logo.png.
LOGO_PARTS = [("BILA", "d"), ("2", "a"), ("WIN", "d")]
LOGO_ICON = "B2"              # 1-2 characters for favicon / app icon
TAGLINE = {"ms": "Kasino Dalam Talian Rasmi Malaysia", "en": "Malaysia's Official Online Casino"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://bila2win.my"                         # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/bila2win"  # NEW SITE: replace
LOGIN_URL = REGISTER_URL
APP_URL = REGISTER_URL
LIVECHAT_URL = REGISTER_URL   # "" hides chat links
EMAIL = ""                    # contact page + footer if set
PHONE = ""                    # contact page if set
ADDRESS = []                  # contact page lines if set; must be real

# --- Languages: LOCAL language first = default (x-default, "/"); English at /en/ ---
LANGS = ["ms", "en"]

# --- SEO keywords (from the user's keyword list; main language first) ---
# Home <meta name="keywords">; every other page/post has its own "focus" + "kw" in pages.py / posts.py.
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ daftar", "kasino dalam talian Malaysia", "slot online Malaysia", "pertaruhan sukan Malaysia"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ register", "online casino Malaysia", "online slots Malaysia", "sports betting Malaysia"],
}

# --- Dates ---
PUBLISHED = "2026-11-01"
UPDATED = "2026-11-01"

# --- Verification & analytics ("" to skip) ---
GSC_VERIFICATION = ""
BING_VERIFICATION = ""
GA4_ID = ""
EXTRA_BODY_END = ""

# --- Cloudflare Pages ---
CF_PROJECT = "bila2win"

# --- Promotions (real, current offers only). (key, image in images/src/promos/ or "", {lang: (title, text)}) ---
PROMOS = [
    ("live-welcome-50", "promo-1", {"ms": ("Bonus Alu-aluan Live 50%", "Bonus 50% pada deposit pertama untuk permainan kasino langsung. Turnover dikenakan."),
                                    "en": ("50% Live Game Welcome Bonus", "50% on your first deposit for live casino games. Turnover applies.")}),
    ("live-daily-20", "promo-2", {"ms": ("Bonus Harian Live 20%", "Bonus 20% sekali sehari untuk permainan kasino langsung. Baca terma sebelum menuntut."),
                                  "en": ("20% Live Game Daily Bonus", "A 20% bonus once a day for live casino games. Read the terms before claiming.")}),
    ("rebate", "promo-3", {"ms": ("Rebat Mingguan", "Sebahagian turnover yang layak dipulangkan setiap minggu."),
                           "en": ("Weekly Rebate", "Part of your eligible turnover returned every week.")}),
]

# --- Payment methods shown on the site ---
PAYMENTS = ["Touch 'n Go eWallet", "DuitNow", "FPX", "GrabPay", "Boost", "Maybank", "CIMB", "Public Bank", "USDT"]
PROVIDERS = ["Pragmatic Play", "Evolution", "PG Soft", "Jili", "Spadegaming", "Playtech", "SBOBET", "Sexy Gaming", "Joker", "Mega888"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = white + orange. ---
# Keep "accent-rgb" in sync with "accent". Example blue: {"accent": "#1E6BFF", "accent-2": "#4C8DFF", "accent-rgb": "30,107,255"}
THEME = {}
