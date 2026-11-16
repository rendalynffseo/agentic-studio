# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: jomtekan44 (design + structure from jomtekan44.app). Replace every value for a new site.
# ============================================================

# --- Brand ---
BRAND = "jomtekan44"            # replaces __BRAND__ everywhere
SLUG = "jomtekan44"             # lowercase, used in some post slugs via __SLUG__
# Logo wordmark = parts drawn in order; colour "d" = light text, "a" = accent (teal), "g" = gold. Also used for logo PNGs.
LOGO_PARTS = [("jom", "d"), ("tekan", "a"), ("44", "g")]
LOGO_ICON = "J4"              # 1-2 characters for favicon / app icon
TAGLINE = {"ms": "Kasino Dalam Talian Malaysia dengan Akses Tempatan", "en": "Malaysia Online Casino with Quick Local Access"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://jomtekan44.app"                         # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/jomtekan44"  # NEW SITE: replace
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
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ daftar", "kasino dalam talian Malaysia", "__BRAND__ apk", "slot online Malaysia"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ register", "online casino Malaysia", "__BRAND__ app", "online slots Malaysia"],
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
CF_PROJECT = "jomtekan44"

# --- Offers carousel (numbered slides). Real, current offers only; no % unless the operator shows it. ---
# (key, image in images/src/promos/ or "", {lang: (title, text)})
PROMOS = [
    ("slot-rounds", "promo-1", {"ms": ("Pusingan ciri slot", "Promosi slot semasa dengan permainan layak dan syarat dipaparkan di setiap tawaran. Terma terpakai."),
                                "en": ("Slot feature rounds", "Current slot promotions with qualifying games and conditions shown on each offer. Terms apply.")}),
    ("live-tables", "promo-2", {"ms": ("Tawaran meja langsung", "Tawaran kasino langsung dengan had meja dan syarat yang jelas. Terma terpakai."),
                                "en": ("Live table offers", "Live casino offers with clear table limits and conditions. Terms apply.")}),
    ("sportsbook", "promo-3", {"ms": ("Pilihan sportsbook", "Promosi sukan semasa dengan pasaran layak dan syarat penyelesaian. Terma terpakai."),
                               "en": ("Sportsbook selections", "Current sportsbook promotions with eligible markets and settlement conditions. Terms apply.")}),
]

# --- Local wallets (payment cards) and studios grid ---
PAYMENTS = ["Touch 'n Go", "GrabPay", "Boost", "FPX"]
PROVIDERS = ["Pragmatic Play", "PG Soft", "Habanero", "Microgaming", "CQ9", "Joker", "Spadegaming", "JDB"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = dark teal + gold. ---
# Keep "accent-rgb" in sync with "accent". Example purple/gold: {"accent": "#9B5CFF", "accent-rgb": "155,92,255", "bg": "#0E0A18", "panel": "#1A1230"}
THEME = {}
