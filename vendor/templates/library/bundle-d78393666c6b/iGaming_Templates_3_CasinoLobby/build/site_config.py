# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) and nothing else.
#  Example values: a BK8 lobby (structure from bk8masd.com). Replace every value for a new site.
# ============================================================

# --- Brand ---
BRAND = "BK8"                 # replaces __BRAND__ everywhere
SLUG = "bk8"                  # lowercase, used in blog URLs, e.g. /blog/cara-daftar-__SLUG__/
LOGO_TEXT = "BK8"             # wordmark in the header + favicon/schema logo (1-4 characters look best)
TAGLINE = "Trusted Online Casino in Malaysia"   # used in titles, schema and the hero

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://bk8masd.com"                        # no trailing slash. NEW SITE: replace
REGISTER_URL = "https://hideyourmess.com/go/bk8"    # NEW SITE: replace
LOGIN_URL = REGISTER_URL      # topbar + floating footer "Login"
APP_URL = REGISTER_URL        # app download button
LIVECHAT_URL = REGISTER_URL   # chat bubble + support links; "" hides the bubble
# Popup: images/src/popup.* (phone size 9:16) opens after load and again 30 s after every close; links to REGISTER_URL.
# No image = styled promo card.
EMAIL = ""                    # shown in footer + policies if set

# --- Languages: the LOCAL language is always first (main, at "/"); others at "/<code>/". Available: ms, en, zh ---
# pages.py + posts.py are written in the main language.
LANGS = ["ms", "en", "zh"]

# --- SEO keywords: built from the keyword list the user gives for this site (main language first) ---
# Home <meta name="keywords"> per language; blog hub/policies use the main list; posts set their own "kw".
# The same keywords drive the blog clusters in posts.py (see CLAUDE.md "From keywords to site").
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ daftar", "kasino dalam talian Malaysia", "slot online Malaysia", "__BRAND__ apk"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ register", "online casino Malaysia", "__BRAND__ app"],
    "zh": ["__BRAND__", "__BRAND__ 马来西亚", "__BRAND__ 登录", "__BRAND__ 注册", "马来西亚在线娱乐场"],
}

# --- Dates (YYYY-MM-DD) ---
PUBLISHED = "2026-10-31"
UPDATED = "2026-10-31"

# --- Verification & analytics ("" to skip) ---
GSC_VERIFICATION = ""
BING_VERIFICATION = ""
GA4_ID = ""                   # loaded after first interaction (keeps PageSpeed high)
EXTRA_BODY_END = ""           # raw HTML before </body> (tracker scripts)

# --- Cloudflare Pages ---
CF_PROJECT = "bk8masd"

# --- News ticker (one line per language; "" hides the bar) ---
TICKER = {
    "en": "__BRAND__ will NEVER ask you to deposit via WhatsApp, Telegram or LINE. Only deposit through the official site after logging in.",
    "ms": "__BRAND__ TIDAK AKAN meminta anda deposit melalui WhatsApp, Telegram atau LINE. Deposit hanya melalui laman rasmi selepas log masuk.",
    "zh": "__BRAND__ 绝不会要求您通过 WhatsApp、Telegram 或 LINE 存款。请仅在登录官方网站后存款。",
}

# --- Game tiles: (slug, name, provider, row, badge) ---
# row = slots | live | instant | fishing (rows in that order; empty rows are hidden). badge = "" | "hot" | "new"
# Image: images/src/games/<slug>.* -> portrait tile. No image = styled letter tile (still looks good).
GAMES = [
    ("gates-of-olympus-1000", "Gates of Olympus 1000", "Pragmatic Play", "slots", "hot"),
    ("sugar-rush", "Sugar Rush", "Pragmatic Play", "slots", ""),
    ("starlight-princess-1000", "Starlight Princess 1000", "Pragmatic Play", "slots", "hot"),
    ("mahjong-ways-2", "Mahjong Ways 2", "PG Soft", "slots", ""),
    ("legacy-of-kong-maxways", "Legacy of Kong Maxways", "Spadegaming", "slots", ""),
    ("sweet-bonanza", "Sweet Bonanza", "Pragmatic Play", "slots", ""),
    ("live-baccarat", "Baccarat", "Evolution", "live", "hot"),
    ("live-roulette", "Roulette", "Pragmatic Play Live", "live", ""),
    ("live-blackjack", "Blackjack", "Evolution", "live", ""),
    ("speed-roulette", "Speed Roulette", "Pragmatic Play Live", "live", ""),
    ("dragon-tiger", "Dragon Tiger", "Evolution", "live", ""),
    ("sic-bo", "Sic Bo", "Evolution", "live", ""),
    ("aviator", "Aviator", "Spribe", "instant", "new"),
    ("plinko", "Plinko", "Spribe", "instant", "new"),
    ("keno", "Keno", "Spribe", "instant", ""),
    ("mini-roulette", "Mini Roulette", "Spribe", "instant", ""),
    ("hilo", "Hilo", "Spribe", "instant", ""),
    ("hotline", "Hotline", "Spribe", "instant", ""),
    ("fishing-god", "Fishing God", "Spadegaming", "fishing", ""),
    ("fishing-war", "Fishing War", "Spadegaming", "fishing", ""),
]

# --- Promotions: (title, short text, image slug in images/src/promos/ or "") ---
# Only real, current offers. Terms change: the card always says "T&Cs apply".
PROMOS = [  # main (local) language
    ("Bonus Alu-aluan", "Bonus padanan pada deposit pertama untuk ahli baharu.", "promo-1"),
    ("Bonus Deposit Mingguan", "Bonus tambahan pada deposit mingguan terpilih.", "promo-2"),
    ("Rebat Tunai Harian", "Peratusan turnover yang layak dipulangkan sebagai rebat.", "promo-3"),
    ("Program VIP", "Ganjaran mengikut tahap, sokongan keutamaan dan tawaran eksklusif.", "promo-4"),
]

# --- Upcoming matches (optional; [] hides the section). Update before each deploy or leave empty. ---
# (league, "DD/MM HH:MM", home, away)  -- no odds: they change by the minute.
MATCHES = []
# MATCHES = [("England - Premier League", "01/11 03:00", "Aston Villa", "Fulham")]

# --- Trust strip ---
PROVIDERS = ["Pragmatic Play", "Evolution", "PG Soft", "Spadegaming", "Spribe", "Playtech", "Jili", "SBOBET", "Sexy Gaming", "Microgaming"]
PAYMENTS = ["FPX", "DuitNow", "Touch 'n Go eWallet", "Bank Transfer", "USDT", "Bitcoin", "Ethereum"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = navy + blue/green. ---
# Example red/gold: {"accent": "#e0262b", "accent-hover": "#ff3b40", "go": "#ffc93c", "go-ink": "#1a1200"}
THEME = {}
