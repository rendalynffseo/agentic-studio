# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: MRCOIN88 (layout from mrcoin88a.com). Replace every value for a new site.
# ============================================================

# --- Brand ---
BRAND = "MRCOIN88"
SLUG = "mrcoin88"
# Logo wordmark parts: "a" = accent yellow, "d" = white (logo sits on the green header/footer). Also drawn into logo PNGs.
LOGO_PARTS = [("MR", "a"), ("COIN", "d"), ("88", "a")]
LOGO_ICON = "MC"              # favicon letters
TAGLINE = {"ms": "Kasino Dalam Talian Malaysia", "en": "Malaysia Online Casino"}

# --- Links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://mrcoin88a.com"                       # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/mrcoin88"  # NEW SITE: replace
LOGIN_URL = REGISTER_URL
APP_URL = REGISTER_URL
LIVECHAT_URL = REGISTER_URL
EMAIL = ""
PHONE = ""
ADDRESS = []

# --- Languages: LOCAL language first = default (x-default, "/"); English at /en/ ---
LANGS = ["ms", "en"]

# --- SEO keywords (from the user's keyword list; main language first) ---
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ daftar", "kasino dalam talian Malaysia", "slot online Malaysia", "__BRAND__ apk"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ register", "online casino Malaysia", "online slots Malaysia", "__BRAND__ app"],
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
CF_PROJECT = "mrcoin88"

# --- Announcement marquee under the header (one line per language; "" hides it) ---
ANNOUNCE = {
    "ms": "__BRAND__ tidak akan meminta OTP atau kata laluan anda. Deposit hanya melalui juruwang rasmi selepas log masuk. 18+ sahaja.",
    "en": "__BRAND__ will never ask for your OTP or password. Only deposit through the official cashier after logging in. 18+ only.",
}

# --- Recommended Games tabs: (page key, provider names). First provider = big featured tile. ---
# Provider tile images: images/src/providers/<slug>.* (square); no image = coloured letter tile.
TABS = [
    ("slots", ["Pragmatic Play", "JILI", "Joker", "CQ9", "Dragoon Soft", "Fachai", "Playstar", "Rich88", "Playtech", "KA Gaming", "Meta Gaming", "Mega H5"]),
    ("live", ["Evolution", "Sexy Baccarat", "Dream Gaming", "WM Casino", "King855", "YeeBet"]),
    ("sports", ["SBOBET", "Saba Sports", "AFB Sports"]),
    ("crash", ["Spribe", "JILI", "Pragmatic Play"]),
    ("fishing", ["JILI", "Fachai", "CQ9", "Spadegaming"]),
    ("lottery", ["4D Lottery", "Kaiyuan"]),
]

# --- Game rows (square tiles). (slug, name, provider, row) row = picks | hits. Image: images/src/games/<slug>.* ---
GAMES = [
    ("sweet-bonanza", "Sweet Bonanza", "Pragmatic Play", "picks"), ("gates-of-olympus", "Gates of Olympus", "Pragmatic Play", "picks"),
    ("starlight-princess", "Starlight Princess", "Pragmatic Play", "picks"), ("sweet-bonanza-xmas", "Sweet Bonanza Xmas", "Pragmatic Play", "picks"),
    ("power-of-thor-megaways", "Power of Thor Megaways", "Pragmatic Play", "picks"), ("the-dog-house-megaways", "The Dog House Megaways", "Pragmatic Play", "picks"),
    ("blackjack-live", "Blackjack Live", "Evolution", "hits"), ("lightning-baccarat", "Lightning Baccarat", "Evolution", "hits"),
    ("lightning-roulette", "Lightning Roulette", "Evolution", "hits"), ("sic-bo", "Sic Bo", "Evolution", "hits"),
    ("crazy-time", "Crazy Time", "Evolution", "hits"), ("mega-roulette", "Mega Roulette", "Pragmatic Play", "hits"),
]

# --- Promotions (real, current offers only; example values from the reference site). (key, image, {lang: (title, text)}) ---
PROMOS = [
    ("first-deposit", "promo-1", {"ms": ("Bonus Deposit Pertama 188%", "Bonus untuk deposit pertama ahli baharu. Turnover dan had maksimum dikenakan."),
                                  "en": ("188% First Deposit Bonus", "A bonus on new members' first deposit. Turnover and a maximum apply.")}),
    ("daily-credit", "promo-2", {"ms": ("Kredit Harian MYR 88", "Kredit harian untuk ahli yang layak. Baca syarat sebelum menuntut."),
                                 "en": ("Daily MYR 88 Credit", "Daily credit for eligible members. Read the terms before claiming.")}),
    ("referral", "promo-3", {"ms": ("Ganjaran Rujuk Rakan", "Jemput rakan dewasa dan terima ganjaran apabila mereka bermain."),
                             "en": ("Refer-a-Friend Reward", "Invite adult friends and get rewarded when they play.")}),
]

# --- VIP tiers shown on the VIP page (names only; perks live in pages.py text) ---
VIP_TIERS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond"]

# --- Payment methods & certification labels for the footer ---
PAYMENTS = ["USDT", "Bitcoin", "Ethereum", "FPX", "DuitNow", "Touch 'n Go", "Visa", "Mastercard"]
PROVIDERS = ["Pragmatic Play", "JILI", "Joker", "Evolution", "Playtech", "CQ9", "SBOBET", "Saba Sports"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = green + yellow. ---
# Keep "accent-rgb" in sync with "accent". Example red: {"green": "#B3122E", "green-2": "#D81E3A", "green-deep": "#7E0A1E"}
THEME = {}
