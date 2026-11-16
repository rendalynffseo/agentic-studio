# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: MRGROUP44 (design + page set from mrgroup44.win). Replace every value for a new site.
# ============================================================

# --- Brand ---
BRAND = "MRGROUP44"           # replaces __BRAND__ everywhere
SLUG = "mrgroup44"            # lowercase, used in some post slugs via __SLUG__
# Logo wordmark = parts drawn in order; colour "a" = accent, "d" = dark, "g" = gold. Also used for logo PNGs.
LOGO_PARTS = [("mr", "d"), ("group", "a"), ("44", "g")]
LOGO_ICON = "44"              # 1-2 characters for favicon / app icon
TAGLINE = {"ms": "Kasino Langsung, Taruhan Sukan & Bingo Malaysia", "en": "Live Casino, Sports Betting & Bingo in Malaysia"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://mrgroup44.win"                       # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/mrgroup44"  # NEW SITE: replace
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
CF_PROJECT = "mrgroup44"

# --- Promotions (real, current offers only). (key, image in images/src/promos/ or "", {lang: (title, text)}) ---
# Generic examples (the reference site names no specific %); replace with the brand's real offers.
PROMOS = [
    ("welcome", "promo-1", {"ms": ("Bonus Alu-aluan", "Bonus untuk ahli baharu pada deposit pertama. Turnover dan terma terpakai."),
                            "en": ("Welcome Bonus", "A bonus for new members on the first deposit. Turnover and terms apply.")}),
    ("cashback", "promo-2", {"ms": ("Cashback Harian", "Sebahagian kerugian layak dipulangkan sebagai cashback. Baca terma."),
                             "en": ("Daily Cashback", "Part of eligible losses returned as cashback. Read the terms.")}),
    ("bingo-jackpot", "promo-3", {"ms": ("Jackpot Bingo Progresif", "Bilik bingo dengan jackpot yang terus meningkat setiap pusingan."),
                                  "en": ("Progressive Bingo Jackpot", "Bingo rooms with a jackpot that grows every round.")}),
]

# --- Stats strip under the hero: (value, {lang: label}). Must be TRUE for the brand; [] hides the strip. ---
# Example values copied from the reference home page.
STATS = [("500K+", {"ms": "Ahli aktif", "en": "Active members"}), ("1,200+", {"ms": "Permainan tersedia", "en": "Games available"}),
         ("99.8%", {"ms": "Kadar uptime", "en": "Uptime"}), ("24/7", {"ms": "Sokongan pelanggan", "en": "Customer support"})]

# --- Winners table on the winners page: (date, game, masked user, amount). REAL records only; [] shows the explainer only. ---
WINNERS = []
# WINNERS = [("2026-10-30", "Bingo 75-bola", "ah***88", "RM 2,450")]

# --- Payment methods shown on the site ---
PAYMENTS = ["DuitNow", "FPX / Perbankan Dalam Talian", "Touch 'n Go eWallet", "Boost", "GrabPay", "Kad Bank", "MYR", "E-Wallet Lain"]
PROVIDERS = ["Pragmatic Play", "Evolution", "PG Soft", "Jili", "Spadegaming", "Playtech", "SBOBET", "Sexy Gaming", "Joker", "Mega888"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = cream + rose/pink + maroon. ---
# Keep "accent-rgb" in sync with "accent". Example teal: {"accent": "#14B8A6", "accent-2": "#5EEAD4", "accent-rgb": "20,184,166", "dark": "#123B3A"}
THEME = {}
