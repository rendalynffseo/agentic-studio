"""Static landing-site generator (iGaming_Templates_1).

Run:  python3 build/build.py
Outputs index.html, blog/, sitemap.xml and robots.txt in the project root.
Edit the CONFIG block below to change links, then rebuild.
"""
import html
import re
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from posts_1 import POSTS_1  # noqa: E402
from posts_2 import POSTS_2  # noqa: E402
from posts_3 import POSTS_3  # noqa: E402

from site_config import *  # noqa: E402,F401,F403  (all per-site settings live in site_config.py)
import custom_sections  # noqa: E402  (developer-added sections, see build/custom_sections.py)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = POSTS_1 + POSTS_2 + POSTS_3
BY_SLUG = {p["slug"]: p for p in POSTS}
CATS = {  # blog topic clusters, in display order
    "umum": ("Panduan Umum", "General Guides"),
    "akaun": ("Pendaftaran & Akaun", "Registration & Account"),
    "login": ("Log Masuk & Akses", "Login & Access"),
    "transaksi": ("Deposit & Pengeluaran", "Deposits & Withdrawals"),
    "bonus": ("Bonus & Turnover", "Bonus & Turnover"),
    "keselamatan": ("Keselamatan & Bantuan", "Security & Support"),
}
PILLARS = {  # topic cluster -> its pillar post (one per CATS key). Supporting posts link up to it; it links down to all of them.
    "umum": "__SLUG__-malaysia-faq", "akaun": "cara-daftar-__SLUG__", "login": "cara-login-__SLUG__",
    "transaksi": "deposit-__SLUG__-faq", "bonus": "bonus-__SLUG__-faq", "keselamatan": "keselamatan-akaun-__SLUG__",
}
KEY_POSTS = list(PILLARS.values())  # shown on home + footer
e = html.escape
with open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8") as _f:
    CSS = " ".join(_f.read().split())
CSS += ":root{" + "".join(f"--{k}:{v};" for k, v in THEME.items()) + "}" + " ".join(custom_sections.EXTRA_CSS.split())


def bi(ms, en, tag="span"):
    """Bilingual inline text: BM shown by default, EN when toggled."""
    return f'<{tag} class="ms">{ms}</{tag}><{tag} class="en" lang="en">{en}</{tag}>'


def bi_alt(ms, en):
    """Alt text can't hold markup, so use BM (the default language) with EN appended."""
    return e(f"{ms} / {en}")


LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")


def link_href(target):
    if target == "home":
        return "/"
    if target.startswith("home#"):
        return "/#" + target[5:]
    if target == "blog":
        return "/blog/"
    if target not in BY_SLUG:
        raise ValueError(f"unknown internal link target: {target}")
    return f"/blog/{target}/"


def linkify(escaped):
    """Turn [[target|anchor]] into internal links (text is already HTML-escaped)."""
    return LINK_RE.sub(lambda m: f'<a href="{link_href(m.group(1))}">{m.group(2)}</a>', escaped)


def render_block(text):
    out = []
    for chunk in text.split("\n\n"):
        lines = chunk.split("\n")
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{linkify(e(l[2:]))}</li>" for l in lines) + "</ul>")
        elif all(l[:1].isdigit() and ". " in l[:4] for l in lines):
            out.append("<ol>" + "".join(f"<li>{linkify(e(l.split('. ', 1)[1]))}</li>" for l in lines) + "</ol>")
        else:
            out.append(f"<p>{linkify(e(chunk))}</p>")
    return "".join(out)


META_WARN = []


def check_meta(path, title, desc):
    """Collect SEO length warnings (title <= 65, description 70-165 chars) after token replacement."""
    t, d = replace_tokens(title), replace_tokens(desc)
    if len(t) > 65:
        META_WARN.append(f"{path}: title {len(t)} chars")
    if not 70 <= len(d) <= 165:
        META_WARN.append(f"{path}: description {len(d)} chars")


def replace_tokens(s):
    for k, v in TOKENS.items():
        s = s.replace(k, v)
    return s


def jsonld(*objs):
    return "".join(
        f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in objs
    )


ORG = {
    "@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#org",
    "name": BRAND, "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/images/logo-512.png", "width": 512, "height": 512},
    "contactPoint": {"@type": "ContactPoint", "contactType": "customer service",
                     "availableLanguage": ["Malay", "English"], "areaServed": "MY", "hoursAvailable": "Mo-Su 00:00-23:59"},
}
WEBSITE = {
    "@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website",
    "name": BRAND + " Malaysia", "url": SITE + "/", "inLanguage": ["ms-MY", "en-MY"], "publisher": {"@id": SITE + "/#org"},
}


def faq_schema(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "ms-MY",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}


def breadcrumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def page(title, desc, path, body, schema, og_type="website", extra_head="", keywords=None):
    url = SITE + path
    check_meta(path, title, desc)
    kw = ", ".join(dict.fromkeys(keywords or KEYWORDS))
    return f"""<!doctype html>
<html lang="ms" data-lang="ms">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(kw)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ms-MY" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#5a0d0f">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="ms_MY">
<meta property="og:locale:alternate" content="en_MY">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/preview.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">' if GSC_VERIFICATION else ""}
<link rel="preload" href="/assets/fonts/quicksand-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/quicksand-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="{POPUP_IMAGE}" fetchpriority="high">
{extra_head}<style>{CSS}</style>
{jsonld(*schema)}
</head>
<body>
{header()}
<main>
{body}
</main>
{footer()}
{float_cta()}
{popup()}
<script src="/assets/main.js?v=4" defer></script>
</body>
</html>
"""


def header():
    return f"""<header class="site-header"><div class="wrap">
<a class="logo" href="/">__LOGO_A__<span>__LOGO_B__</span></a>
<nav class="nav" aria-label="Utama">
<a class="nav-link" href="/#kelebihan">{bi("Kelebihan", "Features")}</a>
<a class="nav-link" href="/#cara-daftar">{bi("Cara Daftar", "How to Join")}</a>
<a class="nav-link" href="/#faq">FAQ</a>
<a class="nav-link" href="/blog/">Blog</a>
<div class="lang-switch" role="group" aria-label="Bahasa / Language">
<button type="button" data-set-lang="ms">BM</button><button type="button" data-set-lang="en">EN</button>
</div>
</nav></div></header>"""


def footer():
    links = "".join(f'<a href="/blog/{p["slug"]}/">{bi(e(p["ms"]["title"].split(":")[0].split("?")[0]), e(p["en"]["title"].split(":")[0].split("?")[0]))}</a>' for p in (BY_SLUG[k] for k in KEY_POSTS))
    return f"""<footer class="site-footer"><div class="wrap">
<div class="cols">
<div><h4>{BRAND} Malaysia</h4><p>{bi("Platform hiburan dalam talian untuk pengguna dewasa di Malaysia. Deposit pantas, pengeluaran pantas, sokongan 24 jam.", "Online entertainment platform for adult users in Malaysia. Fast deposits, fast withdrawals, 24-hour support.")}</p></div>
<div><h4>{bi("Panduan Popular", "Popular Guides")}</h4>{links}</div>
<div><h4>{bi("Pautan", "Links")}</h4>
<a href="{REGISTER_URL}" rel="nofollow sponsored">{bi("Daftar", "Register")}</a>
<a href="{LOGIN_URL}" rel="nofollow sponsored">{bi("Log Masuk", "Login")}</a>
<a href="/blog/">Blog</a><a href="{WHATSAPP_URL}" rel="nofollow">WhatsApp</a></div>
</div>
<p class="rg">18+ | {bi("Sila bermain secara bertanggungjawab. Perjudian boleh menyebabkan ketagihan. Pastikan anda mematuhi undang-undang di tempat anda.", "Please play responsibly. Gambling can be addictive. Make sure you comply with the laws where you live.")}<br>&copy; {date.today().year} {BRAND}. {bi("Hak cipta terpelihara.", "All rights reserved.")}</p>
</div></footer>"""


def float_cta():
    return f"""<div class="float-cta" role="navigation" aria-label="CTA">
<a class="f-login" href="{LOGIN_URL}" rel="nofollow sponsored">{bi("Log Masuk", "Login")}</a>
<a class="f-register" href="{REGISTER_URL}" rel="nofollow sponsored">{bi("Daftar Sekarang", "Register Now")}</a>
<a class="f-chat" href="{WHATSAPP_URL}" rel="nofollow" aria-label="WhatsApp">💬</a>
</div>"""


def popup():
    return f"""<div class="popup" id="promo-popup" role="dialog" aria-modal="true" aria-label="Promosi">
<div class="popup-inner">
<button class="popup-close" type="button" aria-label="Tutup / Close">&times;</button>
<a href="{POPUP_LINK}" rel="nofollow sponsored"><img src="{POPUP_IMAGE}" alt="Promosi __BRAND__ / __BRAND__ promotion" width="540" height="960" fetchpriority="high" decoding="async"></a>
</div></div>"""




def games_grid():
    return "".join(
        f'<a class="game" href="{REGISTER_URL}" rel="nofollow sponsored">'
        f'<img src="/images/games/{slug}.webp" alt="{bi_alt(f"Permainan slot {name} di __BRAND__ Malaysia", f"{name} slot game on __BRAND__ Malaysia")}" width="170" height="170" loading="lazy">'
        f'<span>{e(name)}</span></a>'
        for slug, name in GAMES)


def top_banner():
    """Original 1200x100 promo banner as inline SVG: no extra request, sharp at any size, follows the language toggle."""
    coins = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#tb-coin)" stroke="#a87b00" stroke-width="1.5"/>'
        f'<circle cx="{x}" cy="{y}" r="{r*0.62:.1f}" fill="none" stroke="#fff3b0" stroke-opacity=".6"/>'
        for x, y, r in [(250, 22, 9), (276, 80, 7), (905, 18, 6), (935, 84, 8), (560, 90, 5)])
    sparks = "".join(
        f'<path d="M{x} {y-s}L{x+s*.3} {y-s*.3}L{x+s} {y}L{x+s*.3} {y+s*.3}L{x} {y+s}L{x-s*.3} {y+s*.3}L{x-s} {y}L{x-s*.3} {y-s*.3}Z" fill="#fff6c2" opacity=".9"/>'
        for x, y, s in [(232, 58, 6), (330, 16, 4), (612, 14, 5), (870, 60, 5), (1180, 14, 4), (700, 86, 4)])
    return f"""<a class="top-banner" href="{REGISTER_URL}" rel="nofollow sponsored" aria-label="{bi_alt('Daftar __BRAND__ sekarang', 'Register __BRAND__ now')}">
<svg viewBox="0 0 1200 100" width="1200" height="100" role="img" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="tb-bg" x1="0" x2="1"><stop offset="0" stop-color="#3d0709"/><stop offset=".45" stop-color="#b3242a"/><stop offset=".7" stop-color="#941a1c"/><stop offset="1" stop-color="#3d0709"/></linearGradient>
<linearGradient id="tb-gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6c2"/><stop offset=".45" stop-color="#ffd700"/><stop offset="1" stop-color="#c99700"/></linearGradient>
<radialGradient id="tb-coin"><stop offset="0" stop-color="#fff3b0"/><stop offset=".7" stop-color="#ffd700"/><stop offset="1" stop-color="#d4a200"/></radialGradient>
<pattern id="tb-stripes" width="22" height="100" patternUnits="userSpaceOnUse" patternTransform="skewX(-30)"><rect width="6" height="100" fill="#ffd700" opacity=".07"/></pattern>
</defs>
<rect width="1200" height="100" fill="url(#tb-bg)"/>
<rect width="1200" height="100" fill="url(#tb-stripes)"/>
<rect y="0" width="1200" height="3" fill="url(#tb-gold)"/><rect y="97" width="1200" height="3" fill="url(#tb-gold)"/>
{coins}{sparks}
<g font-family="Quicksand, Arial, sans-serif" font-weight="700">
<text x="40" y="68" font-size="54" fill="url(#tb-gold)" stroke="#5a0d0f" stroke-width="1.5">__LOGO_A__<tspan fill="#fff">__LOGO_B__</tspan></text>
<line x1="205" y1="22" x2="205" y2="78" stroke="#ffd700" stroke-opacity=".5" stroke-width="2"/>
<g class="ms"><text x="300" y="46" font-size="27" fill="#fff">Deposit Min <tspan fill="#ffd700">__MIN_DEPOSIT__</tspan> · Pengeluaran Pantas</text>
<text x="300" y="76" font-size="17" fill="#ffe680">Slot · Live Casino · Sukan · Sokongan 24 Jam</text></g>
<g class="en"><text x="300" y="46" font-size="27" fill="#fff">Min Deposit <tspan fill="#ffd700">__MIN_DEPOSIT__</tspan> · Fast Withdrawal</text>
<text x="300" y="76" font-size="17" fill="#ffe680">Slots · Live Casino · Sports · 24/7 Support</text></g>
<g class="tb-cta"><rect x="960" y="24" width="210" height="52" rx="26" fill="url(#tb-gold)" stroke="#fff6c2" stroke-width="2"/>
<text class="ms" x="1065" y="57" font-size="19" fill="#5a0d0f" text-anchor="middle">DAFTAR SEKARANG</text>
<text class="en" x="1065" y="57" font-size="19" fill="#5a0d0f" text-anchor="middle">REGISTER NOW</text></g>
</g>
</svg></a>"""


# ---------------- pages ----------------
HOME_FAQ = [
    (("Apa itu __BRAND__?", "__BRAND__ ialah platform hiburan dalam talian untuk pengguna dewasa di Malaysia dengan permainan slot dan kasino langsung serta sokongan pelanggan 24 jam."),
     ("What is __BRAND__?", "__BRAND__ is an online entertainment platform for adult users in Malaysia offering slot and live casino games with 24-hour customer support.")),
    (("Bagaimana cara daftar __BRAND__?", "Tekan butang Daftar, isi nama seperti dalam akaun bank, sahkan nombor telefon dengan OTP dan cipta kata laluan."),
     ("How do I register on __BRAND__?", "Tap Register, enter your name as on your bank account, verify your phone number with OTP and create a password.")),
    (("Berapa lama deposit dan pengeluaran diproses?", "Kebanyakan deposit dikreditkan dalam beberapa minit. Masa pengeluaran bergantung pada bank dan semakan akaun."),
     ("How long do deposits and withdrawals take?", "Most deposits are credited within minutes. Withdrawal time depends on the bank and account checks.")),
    (("Bolehkah saya bermain melalui telefon bimbit?", "Ya. __BRAND__ boleh diakses melalui pelayar di Android dan iPhone tanpa perlu memuat turun aplikasi."),
     ("Can I play on my mobile phone?", "Yes. __BRAND__ works in the browser on Android and iPhone without downloading an app.")),
    (("Bagaimana menghubungi khidmat pelanggan?", "Khidmat pelanggan tersedia 24 jam melalui live chat dan WhatsApp dalam Bahasa Melayu dan Inggeris."),
     ("How do I contact customer service?", "Customer service is available 24 hours via live chat and WhatsApp in Bahasa Melayu and English.")),
]


HOME_FAQ_LINKS = ["apa-itu-__SLUG__", "cara-daftar-__SLUG__", "deposit-__SLUG__-faq", "__SLUG__-mobile-android-iphone", "khidmat-pelanggan-__SLUG__"]


def guide_link(slug):
    t = BY_SLUG[slug]
    return f'<a class="more" href="/blog/{slug}/">{bi("Baca panduan: " + e(t["ms"]["title"]), "Read the guide: " + e(t["en"]["title"]))} →</a>'


def home():
    feats = [
        ("⚡", ("Deposit Pantas", "Fast Deposit"), ("Baki dikreditkan dalam beberapa minit melalui bank dalam talian dan e-dompet.", "Balance credited within minutes via online banking and e-wallets.")),
        ("💸", ("Pengeluaran Pantas", "Fast Withdrawal"), ("Permintaan pengeluaran diproses dengan cepat terus ke akaun bank anda.", "Withdrawal requests processed quickly straight to your bank account.")),
        ("🎰", ("Pelbagai Permainan", "Wide Game Selection"), ("Slot, kasino langsung dan permainan baharu.", "Slots, live casino and new titles.")),
        ("🛡️", ("Selamat & Dipercayai", "Safe & Trusted"), ("Sambungan HTTPS dan pengesahan akaun untuk melindungi pengguna.", "HTTPS connection and account verification to protect users.")),
        ("📱", ("Mesra Telefon", "Mobile Friendly"), ("Main di Android, iPhone atau komputer tanpa muat turun.", "Play on Android, iPhone or desktop with no download.")),
        ("🕐", ("Sokongan 24 Jam", "24/7 Support"), ("Pasukan khidmat pelanggan sedia membantu setiap masa.", "Customer service team ready to help any time.")),
    ]
    feat_html = "".join(f'<div class="card"><div class="icon">{i}</div><h3>{bi(*t)}</h3><p>{bi(*d)}</p></div>' for i, t, d in feats)
    steps = [
        (("Tekan Daftar", "Tap Register"), ("Klik butang Daftar Sekarang di bahagian bawah skrin.", "Click the Register Now button at the bottom of the screen.")),
        (("Isi Maklumat", "Fill in Details"), ("Masukkan nama, nombor telefon dan maklumat bank anda.", "Enter your name, phone number and bank details.")),
        (("Sahkan OTP", "Verify OTP"), ("Sahkan nombor telefon dengan kod OTP yang dihantar.", "Verify your phone number with the OTP code sent.")),
        (("Deposit & Main", "Deposit & Play"), ("Buat deposit pertama dan mula bermain.", "Make your first deposit and start playing.")),
    ]
    step_html = "".join(f'<div class="card"><h3>{bi(*t)}</h3><p>{bi(*d)}</p></div>' for t, d in steps)
    faq_html = "".join(f'<details><summary>{bi(e(m[0]), e(n[0]))}</summary><p>{bi(e(m[1]), e(n[1]))}</p><p>{guide_link(slug)}</p></details>'
                       for (m, n), slug in zip(HOME_FAQ, HOME_FAQ_LINKS))
    posts_html = "".join(post_card(BY_SLUG[k]) for k in KEY_POSTS)
    body = f"""
{top_banner()}
<section class="hero"><div class="wrap">
<h1>{bi("__BRAND__ Malaysia – Slot & Kasino Dalam Talian yang Dipercayai", "__BRAND__ Malaysia – Trusted Online Slot & Casino")}</h1>
<p>{bi("Deposit pantas, pengeluaran pantas dan khidmat pelanggan 24 jam. Daftar dalam masa kurang 5 minit dan nikmati permainan terbaharu.", "Fast deposits, fast withdrawals and 24-hour customer service. Register in under 5 minutes and enjoy the latest games.")}</p>
<div class="actions">
<a class="btn btn-gold" href="{REGISTER_URL}" rel="nofollow sponsored">{bi("Daftar Sekarang", "Register Now")}</a>
<a class="btn btn-outline" href="{LOGIN_URL}" rel="nofollow sponsored">{bi("Log Masuk", "Login")}</a>
</div>
<div class="badges"><span class="badge">⚡ {bi("Deposit Pantas", "Fast Deposit")}</span><span class="badge">💸 {bi("Pengeluaran Pantas", "Fast Withdraw")}</span><span class="badge">🕐 24/7</span><span class="badge">🔞 18+</span></div>
</div></section>

{custom_sections.AFTER_HERO}
<section id="permainan"><div class="wrap">
<h2>{bi("Permainan Slot Popular di __BRAND__", "Popular Slot Games on __BRAND__")}</h2>
<p class="lead">{bi("Ratusan permainan slot daripada penyedia terkenal seperti JILI, Playtech dan Pragmatic Play, dengan tajuk baharu setiap minggu.", "Hundreds of slot games from well-known providers such as JILI, Playtech and Pragmatic Play, with new titles every week.")}</p>
<div class="showcase">
<a href="{REGISTER_URL}" rel="nofollow sponsored"><img src="/images/showcase-1.webp" alt="{bi_alt('Permainan terbaharu di __BRAND__', 'Newest game on __BRAND__')}" width="799" height="396"></a>
<a href="{REGISTER_URL}" rel="nofollow sponsored"><img src="/images/showcase-2.webp" alt="{bi_alt('Senarai permainan slot __BRAND__', '__BRAND__ slot games list')}" width="800" height="525" loading="lazy"></a>
</div>
<p style="text-align:center;margin-top:24px"><a class="btn btn-gold" href="{REGISTER_URL}" rel="nofollow sponsored">{bi("Main Sekarang", "Play Now")}</a></p>
</div></section>

<section id="game-popular"><div class="wrap">
<h2>{bi("Game Slot Paling Hangat Minggu Ini", "Hottest Slot Games This Week")}</h2>
<p class="lead">{bi("Pilih permainan kegemaran anda dan mula bermain dengan satu klik.", "Pick your favourite game and start playing in one click.")}</p>
<div class="games">{games_grid()}</div>
<p class="inline-links">{bi('Sebelum bermain, fahami <a href="/blog/bonus-__SLUG__-faq/">syarat bonus __BRAND__</a> dan <a href="/blog/maksud-turnover-bonus-__SLUG__/">maksud turnover</a>. Main secara bertanggungjawab, 18+.', 'Before you play, understand the <a href="/blog/bonus-__SLUG__-faq/">__BRAND__ bonus terms</a> and <a href="/blog/maksud-turnover-bonus-__SLUG__/">what turnover means</a>. Play responsibly, 18+.')}</p>
</div></section>

<section id="transaksi"><div class="wrap">
<h2>{bi("Transaksi Langsung: Deposit & Pengeluaran Pantas", "Live Transactions: Fast Deposits & Withdrawals")}</h2>
<p class="lead">{bi("Deposit minimum __MIN_DEPOSIT__ dan pengeluaran minimum __MIN_WITHDRAW__. Lihat transaksi pengguna secara langsung di dalam platform.", "Minimum deposit __MIN_DEPOSIT__ and minimum withdrawal __MIN_WITHDRAW__. See user transactions live inside the platform.")}</p>
<div class="showcase single"><img src="/images/showcase-3.webp" alt="{bi_alt('Transaksi langsung deposit dan pengeluaran __BRAND__', '__BRAND__ live deposit and withdrawal transactions')}" width="799" height="300" loading="lazy"></div>
<p class="inline-links">{bi('Panduan lanjut: <a href="/blog/deposit-__SLUG__-faq/">deposit __BRAND__</a> · <a href="/blog/pengeluaran-__SLUG__-faq/">pengeluaran __BRAND__</a> · <a href="/blog/pengeluaran-__SLUG__-pending/">pengeluaran pending</a>', 'More guides: <a href="/blog/deposit-__SLUG__-faq/">__BRAND__ deposits</a> · <a href="/blog/pengeluaran-__SLUG__-faq/">__BRAND__ withdrawals</a> · <a href="/blog/pengeluaran-__SLUG__-pending/">pending withdrawals</a>')}</p>
</div></section>

<section id="platform"><div class="wrap">
<h2>{bi("Paparan Platform __BRAND__", "__BRAND__ Platform Preview")}</h2>
<p class="lead">{bi("Slot, permainan crash, sukan dan dompet tunggal dalam satu paparan yang mudah digunakan.", "Slots, crash games, sports and a single wallet in one easy-to-use screen.")}</p>
<div class="showcase single wide"><a href="{REGISTER_URL}" rel="nofollow sponsored"><img src="/images/preview.webp" alt="{bi_alt('Paparan laman utama platform __BRAND__', '__BRAND__ platform home screen')}" width="1100" height="563" loading="lazy"></a></div>
</div></section>

<section id="kelebihan"><div class="wrap">
<h2>{bi("Kenapa Pilih __BRAND__?", "Why Choose __BRAND__?")}</h2>
<p class="lead">{bi("Semua yang anda perlukan untuk pengalaman hiburan dalam talian yang lancar.", "Everything you need for a smooth online entertainment experience.")}</p>
<div class="grid">{feat_html}</div>
</div></section>

<section id="cara-daftar"><div class="wrap">
<h2>{bi("Cara Daftar __BRAND__ dalam 4 Langkah", "How to Join __BRAND__ in 4 Steps")}</h2>
<div class="grid steps">{step_html}</div>
<p style="text-align:center;margin-top:24px"><a class="btn btn-gold" href="{REGISTER_URL}" rel="nofollow sponsored">{bi("Mula Sekarang", "Get Started")}</a></p>
<p class="inline-links">{bi('Perlukan bantuan? Baca <a href="/blog/cara-daftar-__SLUG__/">panduan lengkap cara daftar __BRAND__</a>, semak <a href="/blog/pendaftaran-__SLUG__-gagal/">punca pendaftaran gagal</a> atau ketahui tentang <a href="/blog/pengesahan-akaun-__SLUG__/">pengesahan akaun</a>.', 'Need help? Read the <a href="/blog/cara-daftar-__SLUG__/">full __BRAND__ registration guide</a>, check <a href="/blog/pendaftaran-__SLUG__-gagal/">why registration fails</a> or learn about <a href="/blog/pengesahan-akaun-__SLUG__/">account verification</a>.')}</p>
</div></section>

{custom_sections.BEFORE_FAQ}
<section id="faq" class="faq"><div class="wrap" style="max-width:820px">
<h2>{bi("Soalan Lazim __BRAND__", "__BRAND__ FAQ")}</h2>
{faq_html}
</div></section>

<section><div class="wrap">
<h2>{bi("Panduan & Soalan Lazim Terkini", "Latest Guides & FAQs")}</h2>
<div class="grid">{posts_html}</div>
<p style="text-align:center;margin-top:24px"><a class="btn btn-outline" href="/blog/">{bi("Lihat Semua Artikel", "View All Articles")}</a></p>
</div></section>
"""
    schema = [ORG, WEBSITE,
              {"@context": "https://schema.org", "@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/",
               "name": "__BRAND__ Malaysia", "inLanguage": "ms-MY", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"}},
              faq_schema([m for m, _ in HOME_FAQ])]
    return page("__BRAND__ Malaysia | Slot & Kasino Online – Daftar & Login",
                "__BRAND__ Malaysia: slot dan kasino dalam talian dipercayai dengan deposit pantas, pengeluaran pantas dan khidmat pelanggan 24 jam. Panduan daftar, login dan FAQ.",
                "/", body, schema,
                extra_head="")


def post_card(p):
    return f"""<a class="card post-card" href="/blog/{p['slug']}/">
<span class="kw">{e(p['kw'])}</span>
<h3>{bi(e(p['ms']['title']), e(p['en']['title']))}</h3>
<p>{bi(e(p['ms']['desc']), e(p['en']['desc']))}</p></a>"""


def blog_index():
    topic_nav = "".join(f'<a href="#{k}">{bi(*v)}</a>' for k, v in CATS.items())
    groups = "".join(
        f'<h2 id="{k}" class="topic-h">{bi(*v)}</h2><div class="grid">'
        + "".join(post_card(p) for p in POSTS if p["cat"] == k) + "</div>"
        for k, v in CATS.items())
    body = f"""<section><div class="wrap">
<nav class="crumbs"><a href="/">{bi("Utama", "Home")}</a> › Blog</nav>
<h1 style="text-align:center;color:var(--gold);margin-bottom:12px">{bi("Blog __BRAND__: Panduan & Soalan Lazim", "__BRAND__ Blog: Guides & FAQs")}</h1>
<p class="lead">{bi("Panduan __BRAND__ tentang daftar, log masuk, deposit, pengeluaran, bonus dan keselamatan akaun.", "__BRAND__ guides on registration, login, deposits, withdrawals, bonuses and account security.")}</p>
<nav class="topic-nav">{topic_nav}</nav>
{groups}
</div></section>"""
    schema = [ORG,
              {"@context": "https://schema.org", "@type": "Blog", "name": "Blog __BRAND__", "url": SITE + "/blog/", "inLanguage": "ms-MY",
               "publisher": {"@id": SITE + "/#org"},
               "blogPost": [{"@type": "BlogPosting", "headline": p["ms"]["title"], "url": f"{SITE}/blog/{p['slug']}/"} for p in POSTS]},
              breadcrumbs([("Utama", SITE + "/"), ("Blog", SITE + "/blog/")])]
    return page("Blog __BRAND__ Malaysia | Panduan & Soalan Lazim __BRAND__",
                "Panduan __BRAND__ dan soalan lazim: cara daftar, login, deposit, pengeluaran, bonus, turnover dan keselamatan akaun __BRAND__ Malaysia.",
                "/blog/", body, schema)


def post_page(i, p):
    ms, en = p["ms"], p["en"]

    def content(d):
        s = f'<p>{linkify(e(d["intro"]))}</p>'
        for h, paras in d["sections"]:
            s += f"<h2>{e(h)}</h2>" + "".join(render_block(x) for x in paras)
        s += "<h2>FAQ</h2>" + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in d["faq"])
        return s

    # related: same topic first, then the next posts in order
    same = [r for r in POSTS if r["cat"] == p["cat"] and r is not p]
    rest = [POSTS[(i + k) % len(POSTS)] for k in range(1, len(POSTS))]
    related = list(dict.fromkeys(r["slug"] for r in same + rest))[:5]
    related = [BY_SLUG[r] for r in related]
    cat_ms, cat_en = CATS[p["cat"]]
    rel_html = "".join(f'<a href="/blog/{r["slug"]}/">{bi(e(r["ms"]["title"]), e(r["en"]["title"]))}</a>' for r in related)
    url = f"{SITE}/blog/{p['slug']}/"
    pillar = BY_SLUG[PILLARS[p["cat"]]]
    cluster = [pillar] + [r for r in POSTS if r["cat"] == p["cat"] and r is not pillar]
    up = "" if p is pillar else (f'<p class="pillar-note">{bi("Sebahagian daripada panduan utama", "Part of the main guide")}: '
                                 f'<a href="/blog/{pillar["slug"]}/">{bi(e(pillar["ms"]["title"]), e(pillar["en"]["title"]))}</a></p>')
    cluster_html = (f'<nav class="cluster" aria-label="Topik"><h2>{bi("Semua panduan topik ini: " + cat_ms, "All guides in this topic: " + cat_en)}</h2><ol>'
                    + "".join(("<li class=\"pillar\">" if r is pillar else "<li>") + (f'<b>{bi(e(r["ms"]["title"]), e(r["en"]["title"]))}</b>' if r is p else
                              f'<a href="/blog/{r["slug"]}/">{bi(e(r["ms"]["title"]), e(r["en"]["title"]))}</a>') + "</li>" for r in cluster)
                    + "</ol></nav>")
    body = f"""<article class="article faq">
<nav class="crumbs"><a href="/">{bi("Utama", "Home")}</a> › <a href="/blog/">Blog</a> › <a href="/blog/#{p['cat']}">{bi(cat_ms, cat_en)}</a></nav>
<h1>{bi(e(ms['title']), e(en['title']))}</h1>
<p class="meta">{bi("Dikemas kini", "Updated")}: <time datetime="{PUBLISHED}">{PUBLISHED}</time> · {BRAND}</p>
{up}
<div class="ms">{content(ms)}</div>
<div class="en" lang="en">{content(en)}</div>
{cluster_html}
<div class="cta-box">
<h2 style="text-align:center;margin:0 0 12px">{bi("Sedia untuk bermula?", "Ready to get started?")}</h2>
<a class="btn btn-gold" href="{REGISTER_URL}" rel="nofollow sponsored">{bi("Daftar __BRAND__ Sekarang", "Register __BRAND__ Now")}</a>
</div>
<div class="related"><h2>{bi("Artikel Berkaitan", "Related Articles")}</h2>{rel_html}
<p class="hub-links"><a href="/blog/#{p['cat']}">{bi("Semua panduan " + cat_ms, "All " + cat_en + " guides")} →</a> · <a href="/blog/">{bi("Semua artikel blog", "All blog articles")} →</a> · <a href="/">{bi("Halaman utama __BRAND__", "__BRAND__ home page")} →</a></p></div>
</article>"""
    schema = [ORG,
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": ms["title"], "description": ms["desc"],
               "inLanguage": "ms-MY", "url": url, "mainEntityOfPage": url, "image": SITE + "/images/preview.jpg",
               "datePublished": PUBLISHED, "dateModified": PUBLISHED, "keywords": p["kw"],
               "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"}, "publisher": {"@id": SITE + "/#org"}},
              faq_schema(ms["faq"]),
              breadcrumbs([("Utama", SITE + "/"), ("Blog", SITE + "/blog/"), (ms["title"], url)])]
    return page(f"{ms['title']} | {BRAND}", ms["desc"], f"/blog/{p['slug']}/", body, schema, og_type="article",
                keywords=[p["kw"], pillar["kw"], f"{BRAND} {cat_ms.lower()}", BRAND])


TOKENS = {"__BRAND__": BRAND, "__SLUG__": SLUG, "__LOGO_A__": LOGO_A, "__LOGO_B__": LOGO_B,
          "__MIN_DEPOSIT__": MIN_DEPOSIT, "__MIN_WITHDRAW__": MIN_WITHDRAW}


def write(rel, content):
    for k, v in TOKENS.items():
        content = content.replace(k, v)
        rel = rel.replace(k, v)
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def audit_clusters():
    """Topical-authority checks: every cat has a pillar, every supporting post links its pillar inline, no orphan posts."""
    assert set(PILLARS) == set(CATS), "PILLARS must have one pillar per CATS key"
    def text_of(p):
        return "\n".join([p["ms"]["intro"]] + [b for _, blocks in p["ms"]["sections"] for b in blocks])
    linked = {t for p in POSTS for t, _ in LINK_RE.findall(text_of(p))}
    for p in POSTS:
        assert PILLARS[p["cat"]] in BY_SLUG, f"pillar missing for {p['cat']}"
        text = text_of(p)
        if p["slug"] != PILLARS[p["cat"]] and f"[[{PILLARS[p['cat']]}|" not in text:
            print(f"  cluster: {p['slug']} has no inline link to its pillar {PILLARS[p['cat']]}")
        if p["slug"] not in linked:
            print(f"  cluster: orphan (no inline link from other posts): {p['slug']}")


def main():
    write("index.html", home())
    write("blog/index.html", blog_index())
    for i, p in enumerate(POSTS):
        write(f"blog/{p['slug']}/index.html", post_page(i, p))
    urls = ["/", "/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{PUBLISHED}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    audit_clusters()
    print(f"Built {len(urls)} pages")
    for w in META_WARN:
        print("  meta:", w)


if __name__ == "__main__":
    main()
