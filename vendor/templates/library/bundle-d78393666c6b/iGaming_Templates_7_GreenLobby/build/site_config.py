# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: MrMart88 (structure from mrmart88.com). Replace every value for a new site.
#  Offers/facts below are EXAMPLES taken from the reference site — confirm they are current before going live.
# ============================================================

# --- Brand ---
BRAND = "MrMart88"            # replaces __BRAND__ everywhere
SLUG = "mrmart88"             # lowercase, used in some slugs via __SLUG__
# Logo wordmark parts: "d" = white/dark text (depends on background), "a" = gold accent, "g" = green accent.
LOGO_PARTS = [("Mr", "d"), ("Mart", "g"), ("88", "a")]
LOGO_ICON = "M8"              # 1-2 characters for favicon / app icon
TAGLINE = {"ms": "Kasino Kredit Percuma Malaysia", "en": "Malaysia's Free Credit Online Casino"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://mrmart88.com"                        # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/mrmart88"  # NEW SITE: replace
LOGIN_URL = REGISTER_URL
APP_URL = REGISTER_URL
LIVECHAT_URL = REGISTER_URL
EMAIL = ""                    # contact page if set
PHONE = ""
ADDRESS = []                  # real only

# --- Languages: LOCAL language first = default (x-default, "/"); English at /en/ ---
LANGS = ["ms", "en"]

# --- SEO keywords (from the user's keyword list; main language first) ---
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "kredit percuma Malaysia", "free credit no deposit", "__BRAND__ login", "__BRAND__ daftar", "kasino dalam talian Malaysia"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "free credit casino Malaysia", "free credit no deposit", "__BRAND__ login", "__BRAND__ register", "online casino Malaysia"],
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
CF_PROJECT = "mrmart88"

# --- Numbers shown in the account card + copy (tokens __MIN_DEPOSIT__ / __MIN_WITHDRAW__) ---
MIN_DEPOSIT = "RM1"
MIN_WITHDRAW = "RM25"

# --- Marquee ticker under the header (per language, short phrases) ---
TICKER = {
    "ms": ["Deposit & Pengeluaran Pantas", "Sokongan 24/7", "Kredit Percuma RM5", "Slot Dalam Talian", "Kasino Langsung", "Sukan Langsung", "Deposit dari __MIN_DEPOSIT__"],
    "en": ["Fast Deposit & Withdrawal", "24/7 Support", "RM5 Free Credit", "Online Slots", "Live Casino", "Live Sports", "Deposit from __MIN_DEPOSIT__"],
}

# --- Overview "quick facts" table (home + sidebar). Only facts you can confirm. ---
FACTS = {
    "ms": [("Kredit percuma", "RM5 semasa daftar, tanpa deposit"), ("Ganjaran harian", "Free 365 setiap hari"), ("Rebat & komisen", "6%, tanpa turnover"),
           ("Deposit minimum", "__MIN_DEPOSIT__"), ("Pengeluaran minimum", "__MIN_WITHDRAW__"), ("Permainan", "30+ studio: slot, live, sukan, ikan")],
    "en": [("Free credit", "RM5 on registration, no deposit"), ("Daily reward", "Free 365 every day"), ("Rebate & commission", "6%, zero turnover"),
           ("Minimum deposit", "__MIN_DEPOSIT__"), ("Minimum withdrawal", "__MIN_WITHDRAW__"), ("Games", "30+ studios: slots, live, sports, fishing")],
}

# --- Game tiles (square). (slug, name, provider, tab, badge) tab = slot | live | fish | table | fast. badge "" | "hot" | "new"
# Image: images/src/games/<slug>.* (square). No image = styled letter tile.
GAMES = [
    ("circus-joker-4096", "Circus Joker 4096", "Jili", "slot", "hot"), ("gates-of-olympus-1000", "Gates of Olympus 1000", "Pragmatic Play", "slot", "hot"),
    ("roma", "Roma", "Joker", "slot", ""), ("aztec-gems", "Aztec Gems", "Pragmatic Play", "slot", ""), ("night-city", "Night City", "Jili", "slot", "new"),
    ("mahjong-ways-2", "Mahjong Ways 2", "PG Soft", "slot", "hot"), ("fortune-gems-2", "Fortune Gems 2", "Jili", "slot", ""), ("sweet-bonanza", "Sweet Bonanza", "Pragmatic Play", "slot", ""),
    ("super-ace", "Super Ace", "Jili", "slot", ""), ("great-rhino", "Great Rhino", "Pragmatic Play", "slot", ""), ("golden-express", "Golden Express", "AceWin", "slot", "new"),
    ("legacy-of-egypt", "Legacy of Egypt", "Playtech", "slot", ""),
    ("baccarat", "Baccarat", "Evolution", "live", "hot"), ("roulette", "Roulette", "Pragmatic Play Live", "live", ""), ("blackjack", "Blackjack", "Evolution", "live", ""),
    ("dragon-tiger", "Dragon Tiger", "Sexy Gaming", "live", ""),
    ("fishing-god", "Fishing God", "Spadegaming", "fish", ""), ("jackpot-fishing", "Jackpot Fishing", "Jili", "fish", "hot"), ("ocean-king", "Ocean King", "Kiss918", "fish", ""),
    ("teen-patti", "Teen Patti", "Jili", "table", ""), ("sic-bo", "Sic Bo", "Kingmaker", "table", ""), ("blackjack-vip", "Blackjack VIP", "Jili", "table", ""),
    ("aviator", "Aviator", "Spribe", "fast", "new"), ("plinko", "Plinko", "Spribe", "fast", ""), ("mines", "Mines", "Spribe", "fast", ""),
]

# --- Promotions (EXAMPLES from the reference; real current offers only). (key, image in images/src/promos/ or "", {lang: (title, text, how)}) ---
PROMOS = [
    ("register-free", "promo-1", {"ms": ("Daftar Percuma RM5", "Kredit RM5 tanpa deposit untuk ahli baharu.", "Automatik selepas daftar dan sahkan telefon"),
                                  "en": ("New Register Free RM5", "RM5 credit with no deposit for new members.", "Automatic after registering and verifying your phone")}),
    ("free-365", "promo-2", {"ms": ("Free 365 Harian", "Kredit percuma kecil setiap hari untuk slot.", "Tuntut di halaman promosi setiap hari"),
                             "en": ("Free 365 Daily", "A small free credit every day for slots.", "Claim on the promotions page every day")}),
    ("rebate-6", "promo-3", {"ms": ("Rebat 6% Tanpa Turnover", "Rebat dan komisen 6% yang boleh terus dikeluarkan.", "Dikreditkan mengikut jadual rebat"),
                             "en": ("6% Rebate, Zero Turnover", "6% rebate and commission you can withdraw directly.", "Credited on the rebate schedule")}),
    ("referral", "promo-4", {"ms": ("Rujuk Rakan: RM10 + 6% + RM3", "Ganjaran apabila rakan anda mendaftar dan bermain.", "Kongsi pautan rujukan dari akaun anda"),
                             "en": ("Refer a Friend: RM10 + 6% + RM3", "Rewards when your friends register and play.", "Share the referral link from your account")}),
]

# --- Lucky draw prizes shown on the lucky draw page/card (EXAMPLE from the reference) ---
LUCKY_DRAW = {"rule": {"ms": "Setiap deposit RM10 = 1 nombor bertuah", "en": "Every RM10 deposit = 1 lucky number"},
              "prizes": [("1st", "RM300"), ("2nd", "RM200"), ("3rd", "RM100"), ("Special", "RM20"), ("Consolation", "RM10")]}

PAYMENTS = ["Touch 'n Go eWallet", "DuitNow", "FPX", "Maybank", "CIMB", "Public Bank", "RHB", "Hong Leong", "USDT", "SGD"]
PROVIDERS = ["Jili", "Pragmatic Play", "PG Soft", "Joker", "Mega888", "Kiss918", "Playtech", "Evolution", "Sexy Gaming", "Spadegaming", "AceWin", "VPlus"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = deep green + gold. ---
# Keep "accent-rgb" in sync with "accent". Example red: {"green-deep": "#3D0A0A", "green": "#7A0E0E", "green-2": "#BF2F2F", "accent-rgb": "191,47,47"}
THEME = {}
