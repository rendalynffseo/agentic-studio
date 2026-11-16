# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: A66 Slot (design inspired by a66slot.pro). Replace every value for a new site.
# ============================================================

# --- Brand (one consistent entity name everywhere: titles, schema, copy) ---
BRAND = "A66 Slot"
BRAND_ALT = ["A66Slot", "a66 slot"]   # alternateName in schema (spellings people search)
SLUG = "a66slot"
# Logo wordmark parts; colour "a" = accent (sky), "d" = light text on the dark header. Also used for logo PNGs.
LOGO_PARTS = [("A66", "a"), ("SLOT", "d")]
LOGO_ICON = "A6"
TAGLINE = {"ms": "Kasino Dalam Talian Terbaik Malaysia", "en": "Malaysia's Online Casino Destination"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://a66slot.pro"                          # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/a66slot"   # NEW SITE: replace
LOGIN_URL = REGISTER_URL
APP_URL = REGISTER_URL
LIVECHAT_URL = REGISTER_URL

# --- Entity / NAP (optional; only real data — empty values are left out of the page and schema) ---
EMAIL = ""
PHONE = ""
ADDRESS = []                  # e.g. ["Lot 1, Jalan ...", "50000 Kuala Lumpur, Malaysia"]
SAME_AS = []                  # official profiles of THIS brand: Facebook, Telegram, X, YouTube... (schema sameAs)

# --- Topic entities (schema about/mentions + glossary). key -> (name ms, name en, Wikipedia URL).
# Every URL was checked to exist. Add only URLs you have opened. Pages/posts reference keys in "about".
ENTITIES = {
    "malaysia": ("Malaysia", "Malaysia", "https://en.wikipedia.org/wiki/Malaysia"),
    "online_casino": ("Kasino dalam talian", "Online casino", "https://en.wikipedia.org/wiki/Online_casino"),
    "online_gambling": ("Perjudian dalam talian", "Online gambling", "https://en.wikipedia.org/wiki/Online_gambling"),
    "slot": ("Mesin slot", "Slot machine", "https://en.wikipedia.org/wiki/Slot_machine"),
    "rtp": ("Return to player (RTP)", "Return to player (RTP)", "https://en.wikipedia.org/wiki/Return_to_player"),
    "rng": ("Penjanaan nombor rawak", "Random number generation", "https://en.wikipedia.org/wiki/Random_number_generation"),
    "baccarat": ("Baccarat", "Baccarat", "https://en.wikipedia.org/wiki/Baccarat"),
    "roulette": ("Rolet", "Roulette", "https://en.wikipedia.org/wiki/Roulette"),
    "blackjack": ("Blackjack", "Blackjack", "https://en.wikipedia.org/wiki/Blackjack"),
    "sic_bo": ("Sic bo", "Sic bo", "https://en.wikipedia.org/wiki/Sic_bo"),
    "poker": ("Poker", "Poker", "https://en.wikipedia.org/wiki/Poker"),
    "sports_betting": ("Pertaruhan sukan", "Sports betting", "https://en.wikipedia.org/wiki/Sports_betting"),
    "fixed_odds": ("Pertaruhan odds tetap", "Fixed-odds betting", "https://en.wikipedia.org/wiki/Fixed-odds_betting"),
    "asian_handicap": ("Asian handicap", "Asian handicap", "https://en.wikipedia.org/wiki/Asian_handicap"),
    "esports": ("E-sukan", "Esports", "https://en.wikipedia.org/wiki/Esports"),
    "esports_betting": ("Pertaruhan e-sukan", "Esports betting", "https://en.wikipedia.org/wiki/Esports_betting"),
    "mlbb": ("Mobile Legends: Bang Bang", "Mobile Legends: Bang Bang", "https://en.wikipedia.org/wiki/Mobile_Legends:_Bang_Bang"),
    "bingo": ("Bingo", "Bingo", "https://en.wikipedia.org/wiki/Bingo_(American_version)"),
    "lottery": ("Loteri", "Lottery", "https://en.wikipedia.org/wiki/Lottery"),
    "4d": ("4D (empat digit)", "4-Digits (4D)", "https://en.wikipedia.org/wiki/4-Digits"),
    "ringgit": ("Ringgit Malaysia", "Malaysian ringgit", "https://en.wikipedia.org/wiki/Malaysian_ringgit"),
    "tng": ("Touch 'n Go eWallet", "Touch 'n Go eWallet", "https://en.wikipedia.org/wiki/Touch_%27n_Go"),
    "duitnow": ("DuitNow", "DuitNow", "https://en.wikipedia.org/wiki/DuitNow"),
    "digital_wallet": ("Dompet digital", "Digital wallet", "https://en.wikipedia.org/wiki/Digital_wallet"),
    "mobile_banking": ("Perbankan mudah alih", "Mobile banking", "https://en.wikipedia.org/wiki/Mobile_banking"),
    "mobile_app": ("Aplikasi mudah alih", "Mobile app", "https://en.wikipedia.org/wiki/Mobile_app"),
    "2fa": ("Pengesahan dua faktor", "Two-factor authentication", "https://en.wikipedia.org/wiki/Two-factor_authentication"),
    "rebate": ("Rebat", "Rebate", "https://en.wikipedia.org/wiki/Rebate_(marketing)"),
    "problem_gambling": ("Masalah perjudian", "Problem gambling", "https://en.wikipedia.org/wiki/Problem_gambling"),
    "responsible_gambling": ("Perjudian bertanggungjawab", "Responsible gambling", "https://en.wikipedia.org/wiki/Responsible_gambling"),
}
ORG_KNOWS_ABOUT = ["online_casino", "slot", "baccarat", "sports_betting", "esports_betting", "bingo", "responsible_gambling"]

# --- Languages: LOCAL language first = default (x-default, "/"); English at /en/ ---
LANGS = ["ms", "en"]

# --- SEO keywords (from the user's keyword list; main language first) ---
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "a66slot", "__BRAND__ login", "__BRAND__ daftar", "kasino dalam talian Malaysia", "slot online Malaysia"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "a66slot", "__BRAND__ login", "__BRAND__ register", "online casino Malaysia", "online slots Malaysia"],
}

# --- Dates ---
PUBLISHED = "2026-11-02"
UPDATED = "2026-11-02"

# --- Verification & analytics ("" to skip) ---
GSC_VERIFICATION = ""
BING_VERIFICATION = ""
GA4_ID = ""                   # loads after first interaction only (keeps PageSpeed 100)
EXTRA_BODY_END = ""

# --- Cloudflare Pages ---
CF_PROJECT = "a66slot"

# --- Stats band under the hero. EXAMPLE values shown on a66slot.pro — confirm before launch. (value, {lang: label}) ---
STATS = [
    ("500+", {"ms": "Permainan slot", "en": "Slot games"}),
    ("24/7", {"ms": "Sokongan pelanggan", "en": "Customer support"}),
    ("MYR", {"ms": "Mata wang rasmi", "en": "Official currency"}),
    ("SSL", {"ms": "Penyulitan selamat", "en": "Secure encryption"}),
]

# --- Promotions (real, current offers only; the reference lists no amounts, so none here). ---
# (key, image in images/src/promos/ or "", {lang: (title, text)})
PROMOS = [
    ("welcome", "promo-1", {"ms": ("Bonus Alu-aluan", "Tawaran untuk ahli baharu pada deposit pertama. Semak jumlah dan turnover di laman rasmi."),
                            "en": ("Welcome Bonus", "An offer for new members on the first deposit. Check the amount and turnover on the official site.")}),
    ("daily", "promo-2", {"ms": ("Bonus Harian", "Tawaran harian untuk ahli aktif. Baca terma sebelum menuntut."),
                          "en": ("Daily Bonus", "A daily offer for active members. Read the terms before claiming.")}),
    ("rebate", "promo-3", {"ms": ("Rebat Mingguan", "Sebahagian turnover yang layak dipulangkan setiap minggu."),
                           "en": ("Weekly Rebate", "Part of your eligible turnover returned every week.")}),
]

# --- Payment methods (chips) and providers ---
PAYMENTS = ["DuitNow", "FPX", "Touch 'n Go eWallet", "Boost", "GrabPay", "Bank Transfer"]
PROVIDERS = ["Pragmatic Play", "Evolution", "PG Soft", "Jili", "Spadegaming", "Playtech", "SBOBET", "Joker"]

# --- Malaysian states served (shown in "We serve all of Malaysia"; plain text, no claims) ---
STATES = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Pulau Pinang",
          "Sabah", "Sarawak", "Selangor", "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = navy + sky glow. ---
# Keep "accent-rgb" in sync with "accent"; "accent-ink" must pass 4.5:1 contrast on white.
THEME = {}
