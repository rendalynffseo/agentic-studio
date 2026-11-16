# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file and nothing else.
#  Example values below are from the RA88 site (ra88.lol).
# ============================================================

# --- Brand ---
BRAND = "RA88"            # replaces every __BRAND__ in pages and blog posts
SLUG = "ra88"             # lowercase brand, used in blog URLs, e.g. /blog/cara-daftar-ra88/
LOGO_A = "RA"             # logo first part (gold)
LOGO_B = "88"             # logo second part (white)

# --- Domain & links ---
SITE = "https://ra88.lol"                        # no trailing slash
REGISTER_URL = "https://hideyourmess.com/go/RA88"
LOGIN_URL = REGISTER_URL
WHATSAPP_URL = REGISTER_URL                      # or "https://wa.me/60XXXXXXXXX"
POPUP_IMAGE = "/images/popup-banner.webp"
POPUP_LINK = REGISTER_URL

# --- Numbers shown in copy ---
MIN_DEPOSIT = "RM1"
MIN_WITHDRAW = "RM20"

# --- Dates ---
PUBLISHED = "2026-10-31"   # shown on blog posts + schema + sitemap

# --- Google Search Console ---
GSC_VERIFICATION = "HIfwU_M3ccnppHoCXIfpDLM_6o5TFr2q0hBl0sQxW4Q"  # content value of the google-site-verification meta tag; NEW SITE: replace or set ""

# --- Cloudflare Pages ---
CF_PROJECT = "ra88"        # Pages project name (deploy.sh reads this)

# --- Game tiles (images/games/<slug>.webp, 170x170) ---
GAMES = [
    ("mahjong-ultimate", "Mahjong Ultimate"), ("boxing-fighter", "Boxing Fighter"), ("chibi-4096x", "Chibi 4096x"),
    ("money-heist", "Money Heist"), ("power-of-anubis", "Power of Anubis"), ("aztec-wish", "Aztec Wish"),
    ("ace-supreme", "Ace Supreme"), ("mighty-blue", "Mighty Blue"), ("golden-lion-gate", "Golden Lion Gate"),
    ("dolphin-splash", "Dolphin Splash"), ("bombbomb-slime", "Bombbomb Slime"), ("prank-punk", "Prank Punk"),
    ("tanzania-king", "Tanzania King"), ("aquatic-bonanza", "Aquatic Bonanza"), ("golden-rails-express", "Golden Rails Express"),
    ("snitches-get-riches", "Snitches Get Riches"), ("wild-cherry", "Wild Cherry"), ("poseidons-legacy", "Poseidon's Legacy"),
]

# --- SEO keywords (from the keyword list the user gives for this site; main/local language first) ---
# Used in <meta name="keywords"> on home + blog hub, and to plan blog clusters (see CLAUDE.md).
KEYWORDS = ["__BRAND__", "__BRAND__ Malaysia", "__BRAND__ login", "__BRAND__ daftar", "slot online Malaysia",
            "kasino dalam talian Malaysia", "__BRAND__ deposit", "__BRAND__ bonus"]

# --- Theme (site inspiration) ---
# Overrides the CSS colour tokens in assets/style.css :root. Leave {} to keep the default red/gold.
# Example green/gold: {"red": "#1f7a3a", "red-dark": "#14502a", "red-deep": "#0a2e18", "gold": "#ffd54a"}
THEME = {}
