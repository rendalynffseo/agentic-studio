# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: KINGROUP88 (structure from kingroup88.net). Replace every value for a new site.
# ============================================================

# --- Brand ---
BRAND = "KINGROUP88"          # replaces __BRAND__ everywhere
SLUG = "kingroup88"           # lowercase, used in some post slugs via __SLUG__
# Logo wordmark = parts drawn in order; colour "a" = accent (teal), "d" = light text. Also used for logo PNGs.
LOGO_PARTS = [("KINGROUP", "d"), ("88", "a")]
LOGO_ICON = "K8"              # 1-2 characters for favicon / app icon
TAGLINE = {"ms": "Kasino Online Malaysia", "en": "Malaysia Online Casino"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://kingroup88.net"                        # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/kingroup88"  # NEW SITE: replace
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
CF_PROJECT = "kingroup88"

# --- Promotions (real, current offers only — these are EXAMPLES from kingroup88.net; verify before going live) ---
# (key, image in images/src/promos/ or "", {lang: (title, text)}). Shown in the home carousel, promotions page and welcome-bonus page.
PROMOS = [
    ("welcome-150", "promo-1", {"ms": ("Bonus Selamat Datang 150%", "Bonus deposit pertama untuk ahli baharu. Turnover dan had maksimum dikenakan."),
                                "en": ("150% Welcome Bonus", "First-deposit bonus for new members. Turnover and a maximum cap apply.")}),
    ("cashback-15", "promo-2", {"ms": ("Cashback Mingguan 15%", "Sebahagian kerugian bersih mingguan yang layak dipulangkan. Baca terma."),
                                "en": ("15% Weekly Cashback", "Part of your eligible weekly net loss returned. Read the terms.")}),
    ("app-bonus", "promo-3", {"ms": ("Bonus Aplikasi", "Ganjaran untuk pemain yang memasang aplikasi rasmi. Terma terpakai."),
                              "en": ("App Bonus", "A reward for players who install the official app. T&Cs apply.")}),
    ("jackpot", "promo-4", {"ms": ("Jackpot Progresif", "Slot jackpot dengan hadiah terkumpul yang terus meningkat."),
                            "en": ("Progressive Jackpot", "Jackpot slots with a pooled prize that keeps growing.")}),
]

# --- Marquee ticker under the header (per language). Real notices/offers only — no fake wins or live scores. ---
TICKER = {
    "ms": ["🎁 Bonus Selamat Datang untuk ahli baharu — terma terpakai", "⚽ Pasaran Liga Super & EPL dibuka setiap minggu", "🔒 Staf tidak akan meminta OTP anda",
           "📱 Aplikasi Android & iOS tersedia", "💳 Deposit RM melalui DuitNow & Touch 'n Go", "🔞 18+ sahaja · Bermain secara bertanggungjawab"],
    "en": ["🎁 Welcome Bonus for new members — T&Cs apply", "⚽ Liga Super & EPL markets open every week", "🔒 Staff never ask for your OTP",
           "📱 Android & iOS app available", "💳 Deposit RM via DuitNow & Touch 'n Go", "🔞 18+ only · Play responsibly"],
}

# --- Stats bar (value, label per language). Use only numbers you can stand behind. ---
STATS = [("24/7", {"ms": "Sokongan langsung", "en": "Live support"}), ("RM", {"ms": "Mata wang akaun", "en": "Account currency"}),
         ("2 min", {"ms": "Pendaftaran", "en": "Registration"}), ("BM/EN", {"ms": "Bahasa", "en": "Languages"}),
         ("SSL", {"ms": "Sambungan selamat", "en": "Secure connection"}), ("18+", {"ms": "Dewasa sahaja", "en": "Adults only"})]

# --- Upcoming matches for the sports section (optional; [] shows a markets card instead). No odds/scores. ---
MATCHES = []
# MATCHES = [("Liga Super", "Sab 20:45", "Selangor FC", "JDT")]

# --- Payment methods shown on the site ---
PAYMENTS = ["Touch 'n Go eWallet", "DuitNow", "FPX", "GrabPay", "Boost", "Maybank", "CIMB", "Public Bank", "USDT"]
PROVIDERS = ["Pragmatic Play", "Evolution", "PG Soft", "Jili", "Spadegaming", "Playtech", "SBOBET", "Sexy Gaming", "Joker", "Mega888"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = navy + teal neon. ---
# Keep "accent-rgb" in sync with "accent". Example gold: {"accent": "#F5B301", "accent-2": "#FFD65A", "accent-rgb": "245,179,1"}
THEME = {}
