# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: MRACE88 (structure from mrace88my.com). Replace every value for a new site.
# ============================================================

# --- Brand ---
BRAND = "MRACE88"             # replaces __BRAND__ everywhere
SLUG = "mrace88"              # lowercase, used in some post slugs via __SLUG__
# Logo wordmark parts; colour "a" = gold accent, "d" = purple. Also used for logo-wordmark.png.
LOGO_PARTS = [("MR.", "d"), ("ACE", "a"), ("88", "d")]
LOGO_ICON = "A8"              # 1-2 characters for favicon / app icon
TAGLINE = {"ms": "Destinasi Permainan & Pertaruhan Malaysia", "en": "Malaysia's Gaming & Betting Destination"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://mrace88my.com"                         # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/mrace88"   # NEW SITE: replace
LOGIN_URL = REGISTER_URL
APP_URL = REGISTER_URL
LIVECHAT_URL = REGISTER_URL   # "" hides chat links
EMAIL = ""                    # contact page if set
PHONE = ""
ADDRESS = []                  # must be real

# --- Languages: LOCAL language first = default (x-default, "/"); English at /en/ ---
LANGS = ["ms", "en"]

# --- SEO keywords (from the user's keyword list; main language first) ---
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ daftar", "kasino dalam talian Malaysia", "slot online Malaysia", "free credit Malaysia"],
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
CF_PROJECT = "mrace88"

# --- Marquee ticker under the banner (per language; "" hides it) ---
TICKER = {
    "ms": "__BRAND__ MALAYSIA: Tuntut Bonus Alu-aluan 100% dan putaran percuma pada slot terpilih ⚡ Deposit FPX, TNG eWallet & DuitNow ⚡ Staf tidak akan meminta OTP anda ⚡ 18+ sahaja",
    "en": "__BRAND__ MALAYSIA: Claim the 100% Welcome Bonus and free spins on selected slots ⚡ Deposit via FPX, TNG eWallet & DuitNow ⚡ Staff never ask for your OTP ⚡ 18+ only",
}

# --- "Recommended games" tabs: tab key -> (label per lang, featured title, provider names). Provider tiles use
#     images/src/providers/<slug>.* (square) or a styled letter tile. Featured tile: images/src/featured-<tab>.* ---
GAME_TABS = [
    ("slot", {"ms": "Slot", "en": "Slot Game"}, "Dolphin Reef", ["Playtech", "Mega H5", "Jili", "Joker", "Spribe", "Pragmatic Play", "Meta Gaming", "Lucky Win", "Spadegaming", "Mega888"]),
    ("casino", {"ms": "Kasino", "en": "Casino"}, "Live Baccarat", ["Evolution", "Pragmatic Play Live", "AllBet", "King855", "Sexy Gaming", "WM Casino", "Dream Gaming", "SA Gaming"]),
    ("sports", {"ms": "Sukan", "en": "Sports"}, "Football", ["SBOBET", "M8 Bet", "CMD368", "IBC", "SABA Sports", "TF Gaming"]),
]

# --- "Popular games" row: (slug, name, badge) — badge "APPS" for downloadable app games, "" for none.
#     Square images: images/src/games/<slug>.* (else styled letter tile). ---
POPULAR = [("mega-h5", "Mega H5", ""), ("fachai", "Fa Chai", ""), ("lion-king", "Lion King", "APPS"),
           ("mega888", "Mega888", "APPS"), ("pussy888", "Pussy888", "APPS"), ("918kiss", "918Kiss", "APPS")]

# --- Live casino provider strip (names; images/src/providers/<slug>.* optional) ---
LIVE_PROVIDERS = ["AllBet", "King855", "Pragmatic Play Live"]

# --- Promotions (real, current offers only — examples shown on the reference). (key, image, {lang: (title, text)}) ---
PROMOS = [
    ("welcome-100", "promo-1", {"ms": ("Bonus Alu-aluan 100%", "Bonus padanan 100% pada deposit pertama, termasuk putaran percuma slot terpilih. Turnover dikenakan."),
                                "en": ("100% Welcome Bonus", "A 100% match on your first deposit, plus free spins on selected slots. Turnover applies.")}),
    ("daily-credit", "promo-2", {"ms": ("Kredit Percuma RM6 Setiap Hari", "Kredit percuma harian dalam dua sesi, 365 hari setahun. Tertakluk kepada terma."),
                                 "en": ("RM6 Free Credit Every Day", "Daily free credit in two sessions, 365 days a year. Subject to terms.")}),
    ("weekly-cashback", "promo-3", {"ms": ("Pulangan Tunai Mingguan", "Peratus pulangan tunai mingguan mengikut tahap VIP anda."),
                                    "en": ("Weekly Cashback", "A weekly cashback percentage based on your VIP tier.")}),
]

# --- VIP tiers table (home + VIP page). Columns are fixed: welcome, cashback, withdrawals, tourneys, manager, limit.
#     Values: text, True (tick) or False (cross). Example values from the reference — confirm before publishing. ---
VIP_TIERS = [
    ({"ms": "Ahli Biasa", "en": "Regular Member"}, "🥉", ["100%", "3%", {"ms": "Biasa", "en": "Standard"}, False, False, {"ms": "Biasa", "en": "Standard"}]),
    ({"ms": "Ahli Silver", "en": "Silver Member"}, "🥈", ["150%", "5%", {"ms": "Keutamaan", "en": "Priority"}, True, False, {"ms": "Tinggi", "en": "High"}]),
    ({"ms": "VIP Gold", "en": "VIP Gold"}, "🥇", ["200%", "8%", {"ms": "VIP Segera", "en": "VIP Instant"}, True, True, {"ms": "Premium", "en": "Premium Tier"}]),
]

# --- Footer trust row ---
PAYMENTS = ["FPX", "Touch 'n Go eWallet", "DuitNow", "GrabPay", "Boost", "Maybank", "CIMB", "Public Bank", "USDT"]
PROVIDERS = ["Pragmatic Play", "Playtech", "Jili", "Joker", "Spribe", "Evolution", "AllBet", "SBOBET", "Mega888", "918Kiss"]
LICENSES = []   # licence / testing-lab names the operator REALLY holds, e.g. ["PAGCOR"]; [] hides the block
SOCIAL = [("Facebook", ""), ("Telegram", ""), ("Instagram", ""), ("YouTube", "")]  # (name, url); empty url = hidden

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = white + royal purple + gold. ---
# Keep "accent-rgb" in sync with "accent". Example red: {"accent": "#C8102E", "accent-2": "#E8344F", "accent-deep": "#8A0B20", "accent-rgb": "200,16,46"}
THEME = {}
