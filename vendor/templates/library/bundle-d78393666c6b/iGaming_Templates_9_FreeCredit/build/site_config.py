# ============================================================
#  PER-SITE SETTINGS. For a new site, edit this file (and images/src/) — text lives in content/pages/posts.
#  Example values: EKPLUS8 (structure from ekplus8.pro). Replace every value for a new site.
#  Numbers below (free credit, cuci, minimums) were shown on the reference site — re-check them per site.
# ============================================================

# --- Brand ---
BRAND = "EKPLUS8"
SLUG = "ekplus8"
LOGO_PARTS = [("EK", "a"), ("PLUS", "d"), ("8", "a")]   # "a" = accent colour, "d" = light text on the dark header
LOGO_ICON = "E8"
TAGLINE = {"ms": "Kasino Slot Kredit Percuma Malaysia", "en": "Free Credit Slot Casino Malaysia"}

# --- Domain & links (all CTAs are rel="nofollow sponsored") ---
SITE = "https://ekplus8.pro"
REGISTER_URL = "https://hideyourmess.com/go/ekplus8"
LOGIN_URL = REGISTER_URL
APP_URL = REGISTER_URL
LIVECHAT_URL = REGISTER_URL
TELEGRAM_URL = ""             # social links in the footer ("" hides)
FACEBOOK_URL = ""
EMAIL = ""
PHONE = ""
ADDRESS = []

# --- Languages: LOCAL language first = default (x-default, "/"); English at /en/ ---
LANGS = ["ms", "en"]

# --- SEO keywords (from the user's keyword list; main language first) ---
KEYWORDS = {
    "ms": ["__BRAND__", "__BRAND__ Malaysia", "kredit percuma", "free credit slot Malaysia", "slot kredit percuma", "__BRAND__ login", "__BRAND__ daftar"],
    "en": ["__BRAND__", "__BRAND__ Malaysia", "free credit slot Malaysia", "free credit casino", "RM5 free credit", "__BRAND__ login", "__BRAND__ register"],
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
CF_PROJECT = "ekplus8"

# --- Casino overview table on the home page: (label, value) per language. Only facts the operator publishes. ---
OVERVIEW = {
    "ms": [("Jenama", "__BRAND__"), ("Pasaran", "Malaysia, dalam Ringgit (RM)"), ("Deposit minimum", "RM1"), ("Pengeluaran minimum", "RM25"),
           ("Bahagian permainan", "Jackpot, Hot 1:100, Slot, Live, Ikan, Sukan"), ("Kaedah deposit", "E-dompet, perbankan dalam talian, PIN telco, USDT"),
           ("Bonus tanpa deposit", "Kredit percuma RM5 untuk ahli baharu"), ("Mudah alih", "Pelayar telefon dan aplikasi Android"), ("Sokongan", "Sembang langsung")],
    "en": [("Brand", "__BRAND__"), ("Market", "Malaysia, in ringgit (RM)"), ("Minimum deposit", "RM1"), ("Minimum withdrawal", "RM25"),
           ("Game sections", "Jackpot, Hot 1:100, Slot, Live, Fish, Sport"), ("Deposit routes", "E-wallet, online banking, telco PIN, USDT"),
           ("No-deposit bonus", "RM5 free credit for new members"), ("Mobile", "Mobile browser plus an Android app"), ("Support", "Live chat")],
}

# --- Free credit promotions table: per language rows (promotion, amount, deposit, main rule). Examples from the reference. ---
FREE_CREDITS = {
    "ms": [("Daftar Baharu Percuma (Semua Slot)", "RM5", "Tiada", "Tiada turnover. Cuci min RM100, maks 5% (maks RM50)"),
           ("Kredit Percuma 365 Hari (Semua Slot)", "RM1 sehari", "Tiada", "Peraturan cuci sama seperti RM5"),
           ("Min Masuk RM1 Putaran Percuma", "RM5 sehari", "Dari RM1", "Cuci min RM100, maks 5% (RM50)")],
    "en": [("New Register Free (All Slots)", "RM5", "None", "No turnover. Min cuci RM100, max 5% (max RM50)"),
           ("Free Credit 365 Days (All Slots)", "RM1 a day", "None", "Same cuci rules as the RM5"),
           ("Min In RM1 Free Spin", "RM5 a day", "From RM1", "Min cuci RM100, max 5% (RM50)")],
}

# --- Slot providers with their own free credit guide page (key, display name). Image: images/src/providers/<key>.* (square). ---
FC_PROVIDERS = [("mega888", "Mega888"), ("918kiss", "918Kiss"), ("pussy888", "Pussy888"), ("megah5", "MegaH5"),
                ("acewin", "AceWin"), ("vpower", "VPower"), ("epicwin", "EpicWin")]

# --- Promotions (real, current offers only). (key, image in images/src/promos/ or "", {lang: (title, text)}) ---
PROMOS = [
    ("register-rm5", "promo-1", {"ms": ("Kredit Percuma RM5 Daftar Baharu", "Kredit percuma RM5 untuk ahli baharu, untuk semua slot. Cuci min RM100, maks RM50."),
                                 "en": ("RM5 New Register Free Credit", "RM5 free credit for new members on all slots. Min cuci RM100, max RM50.")}),
    ("free-365", "promo-2", {"ms": ("Kredit Percuma 365 Hari", "RM1 kredit percuma sekali sehari untuk semua slot. Baca terma cuci."),
                             "en": ("Free Credit 365 Days", "RM1 free credit once a day on all slots. Read the cuci rules.")}),
    ("rebate-6", "promo-3", {"ms": ("Rebat Istimewa 6%", "Rebat atas turnover yang layak. Terma semasa terpakai."),
                             "en": ("6% Special Rebate", "Rebate on eligible turnover. Current terms apply.")}),
    ("usdt", "promo-4", {"ms": ("Deposit & Keluar dengan USDT", "Deposit dan pengeluaran kripto USDT tersedia."),
                         "en": ("Deposit & Withdraw with USDT", "USDT crypto deposits and withdrawals are available.")}),
]

PAYMENTS = ["Touch 'n Go eWallet", "DuitNow", "FPX", "Boost", "GrabPay", "Telco PIN (Digi / Maxis / Celcom)", "USDT"]
PROVIDERS = ["Mega888", "918Kiss", "Pussy888", "MegaH5", "AceWin", "VPower", "EpicWin", "JILI", "Pragmatic Play", "Evolution", "Joker", "FA CHAI"]

# --- Theme (site inspiration). Overrides tokens in assets/style.css :root. {} = charcoal + yellow + teal. ---
# Keep "accent-rgb" in sync with "accent". Example red: {"accent": "#FF3B3B", "accent-rgb": "255,59,59", "teal": "#7A1010"}
THEME = {}
