"""Static site generator (iGaming_Templates_2_AppGuide).

Run:  python3 build/build.py      -> writes the whole site to dist/ (wiped first)
Per-site settings: site_config.py. Text: content.py (home + UI), pages.py (hubs, author, policies), posts.py.
"""
import hashlib
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from site_config import *  # noqa: E402,F401,F403
from content import UI, HOME  # noqa: E402
from pages import BLOG_HUB, GAMES_HUB, AUTHOR_PAGE, POLICIES  # noqa: E402
from posts import POSTS, CLUSTERS, GAMES_CLUSTER  # noqa: E402
import custom_sections  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
IMG = os.path.join(ROOT, "images")
BY_SLUG = {p["slug"]: p for p in POSTS}
MAIN_LANG = LANGS[0]
DOMAIN = SITE.split("//", 1)[1]
TOKENS = {"__BRAND__": BRAND, "__SITE__": SITE_NAME, "__SLUG__": SLUG, "__AUTHOR__": AUTHOR["name"],
          "__EMAIL__": EMAIL, "__DOMAIN__": DOMAIN}
SIZES = json.load(open(os.path.join(IMG, "sizes.json"))) if os.path.exists(os.path.join(IMG, "sizes.json")) else {}
e = html.escape

with open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8") as _f:
    CSS = " ".join(_f.read().split())
CSS += ":root{" + "".join(f"--{k}:{v};" for k, v in THEME.items()) + "}" + " ".join(custom_sections.EXTRA_CSS.split())
JS_VER = hashlib.md5(open(os.path.join(ROOT, "assets", "main.js"), "rb").read()).hexdigest()[:8]


def per_lang(value, lang):
    """custom_sections values may be a plain string or a {lang: string} dict."""
    return value.get(lang, "") if isinstance(value, dict) else value


def has_img(name):
    return name in SIZES


def wh(name):
    w, h = SIZES[name]
    return f'width="{w}" height="{h}"'


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def ui_lang(lang):
    return lang if lang in UI else MAIN_LANG


def home_path(lang):
    return "/" if lang == MAIN_LANG or lang not in LANGS else f"/{lang}/"


def href(target, lang, on_home=False):
    """'#id' links point at the home page of that language unless we're already on it."""
    if target.startswith("#") and not on_home:
        return home_path(lang) + target
    return target


# ---------------------------------------------------------------- internal links in posts
LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")


def link_href(target, lang):
    if target == "home":
        return home_path(lang)
    if target.startswith("home#"):
        return home_path(lang) + "#" + target[5:]
    if target in ("blog", "games"):
        return f"/{target}/"
    if target not in BY_SLUG:
        raise ValueError(f"unknown internal link target: {target}")
    return f"/blog/{target}/"


def render_block(text, lang):
    def linkify(s):
        return LINK_RE.sub(lambda m: f'<a href="{link_href(m.group(1), lang)}">{m.group(2)}</a>', e(s, quote=False))
    out = []
    for chunk in text.split("\n\n"):
        lines = chunk.split("\n")
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{linkify(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"\d+\. ", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{linkify(l.split('. ', 1)[1])}</li>" for l in lines) + "</ol>")
        else:
            out.append(f"<p>{linkify(chunk)}</p>")
    return "".join(out)


# ---------------------------------------------------------------- schema
def graph(*nodes):
    return '<script type="application/ld+json">' + json.dumps(
        {"@context": "https://schema.org", "@graph": list(nodes)}, ensure_ascii=False) + "</script>"


def org():
    o = {"@type": "Organization", "@id": SITE + "/#org", "name": SITE_NAME, "url": SITE + "/",
         "logo": {"@type": "ImageObject", "url": SITE + "/images/logo-512.png", "width": 512, "height": 512},
         "description": f"Independent informational guide to the {BRAND} mobile app.",
         "contactPoint": {"@type": "ContactPoint", "contactType": "editorial", "email": EMAIL,
                          "availableLanguage": [UI[l]["name"] for l in LANGS]}}
    if ADDRESS:
        o["address"] = {"@type": "PostalAddress", "streetAddress": " ".join(ADDRESS), "addressCountry": "MY"}
    if PHONE:
        o["contactPoint"]["telephone"] = PHONE
    return o


def person():
    p = {"@type": "Person", "@id": SITE + "/about-author/#person", "name": AUTHOR["name"], "url": SITE + "/about-author/",
         "jobTitle": AUTHOR["role"], "worksFor": {"@id": SITE + "/#org"},
         "homeLocation": {"@type": "Place", "name": AUTHOR["city"]}}
    if AUTHOR.get("same_as"):
        p["sameAs"] = AUTHOR["same_as"]
    return p


def website():
    return {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": SITE_NAME,
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": [UI[l]["hreflang"] for l in LANGS]}


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def faq_schema(pairs, lang):
    return {"@type": "FAQPage", "inLanguage": UI[lang]["hreflang"], "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}


# ---------------------------------------------------------------- chrome
def analytics():
    if not GA4_ID:
        return ""
    return f"""<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA4_ID}");
(function(){{var l=false,e=["scroll","mousemove","touchstart","keydown","click"];function load(){{if(l)return;l=true;e.forEach(function(x){{window.removeEventListener(x,load,{{passive:true}});}});
var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}";document.head.appendChild(s);}}
e.forEach(function(x){{window.addEventListener(x,load,{{passive:true}});}});window.addEventListener("load",function(){{setTimeout(load,3500);}});}})();</script>"""


def page(lang, title, desc, path, body, schema, og_type="website", alternates=None, og_title=None, extra_head="", keywords=None):
    u = UI[ui_lang(lang)]
    check_meta(path, title, desc)
    kw = ", ".join(dict.fromkeys(keywords or KEYWORDS.get(ui_lang(lang)) or KEYWORDS[MAIN_LANG]))
    url = SITE + path
    alternates = alternates or {lang: path}
    alt = "".join(f'<link rel="alternate" hreflang="{UI[l]["hreflang"]}" href="{SITE}{p}">' for l, p in alternates.items())
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alternates.get(MAIN_LANG, path)}">'
    og_alt = "".join(f'<meta property="og:locale:alternate" content="{UI[l]["og_locale"]}">' for l in alternates if l != lang)
    geo = (f'<meta name="geo.region" content="{GEO["region"]}"><meta name="geo.placename" content="{GEO["place"]}">'
           f'<meta name="geo.position" content="{GEO["lat"]};{GEO["lng"]}"><meta name="ICBM" content="{GEO["lat"]}, {GEO["lng"]}">') if GEO else ""
    og_img = SITE + "/images/og.jpg"
    verify = (f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">' if GSC_VERIFICATION else "") + \
             (f'<meta name="msvalidate.01" content="{BING_VERIFICATION}">' if BING_VERIFICATION else "")
    og_title = og_title or title
    return f"""<!doctype html>
<html lang="{u['html_lang'] if lang in UI else lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{verify}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(kw)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="{THEME.get('ink', '#0B0D12')}">
<meta name="author" content="{e(AUTHOR['name'])}">
<meta name="publisher" content="{e(SITE_NAME)}">
{geo}
<link rel="canonical" href="{url}">
{alt}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(SITE_NAME)}">
<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{UI[ui_lang(lang)]['og_locale']}">{og_alt}
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(og_title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="text/markdown" title="llms.txt" href="/llms.txt">
{extra_head}
<style>{CSS}</style>
{analytics()}
{schema}
</head>
<body>
{body}
{float_bar(lang)}
{popup(lang)}
<script src="/assets/main.js?v={JS_VER}" defer></script>
{EXTRA_BODY_END}
</body>
</html>"""


META_WARN = []


def check_meta(path, title, desc):
    """SEO length warnings (after tokens): title <= 65 chars, description 70-165 chars."""
    t, d = replace_tokens(title), replace_tokens(desc)
    if path == "/404":
        return
    cjk = re.search(r"[\u4e00-\u9fff]", t + d)  # Chinese: shorter limits (each char is wider)
    tmax, dmin, dmax = (40, 35, 100) if cjk else (65, 70, 165)
    if len(t) > tmax:
        META_WARN.append(f"{path}: title {len(t)} chars")
    if not dmin <= len(d) <= dmax:
        META_WARN.append(f"{path}: description {len(d)} chars")


def float_bar(lang):
    """Floating footer: Login + Register on every page."""
    u = UI[ui_lang(lang)]
    return (f'<div class="float-cta" role="navigation" aria-label="{u["login"]} / {u["float_register"]}">'
            f'<a class="btn btn-ghost" data-wt-event="login_click" href="{LOGIN_URL}" target="_blank" rel="nofollow sponsored noopener">{u["login"]}</a>'
            f'<a class="btn btn-gold" data-wt-event="register_click" href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">{u["float_register"]}</a></div>')


def popup(lang):
    """Phone-size (9:16) promo popup: opens after load, then again 30 s after every close (assets/main.js)."""
    u = UI[ui_lang(lang)]
    if has_img("popup"):
        inner = f'<img src="/images/popup.webp" alt="{e(u["popup_alt"])}" {wh("popup")} decoding="async">'
    else:
        inner = (f'<div class="popup-card"><img src="/images/logo.webp" alt="" width="68" height="68"><b>{e(SITE_NAME)}</b>'
                 f'<span class="kicker">{u["popup_title"]}</span><p>{u["popup_text"]}</p><span class="btn btn-gold">{u["float_register"]}</span></div>')
    return (f'<div class="popup" id="promo-popup" role="dialog" aria-modal="true" aria-label="{e(u["popup_title"])}"><div class="popup-inner">'
            f'<button class="popup-close" type="button" aria-label="{u["popup_close"]}">&times;</button>'
            f'<a href="{REGISTER_URL}" data-wt-event="popup_click" target="_blank" rel="nofollow sponsored noopener">{inner}</a></div></div>')


def logo_img():
    return '<img class="logo" src="/images/logo.webp" alt="" width="34" height="34">'


def brand_link():
    return f'<a class="brand" href="/">{logo_img()}<span>{e(SITE_NAME)}<small>{e(TAGLINE)}</small></span></a>'


def lang_switch(lang):
    if len(LANGS) < 2:
        return ""
    links = "".join(
        f'<a href="{home_path(l)}" hreflang="{UI[l]["hreflang"]}" lang="{UI[l]["html_lang"]}"'
        + (' aria-current="true"' if l == lang else "") + f'>{UI[l]["label"]}</a>' for l in LANGS)
    return f'<div class="lang" aria-label="Language">{links}</div>'


def top(lang, path, on_home=False):
    u = UI[ui_lang(lang)]
    nav = "".join(
        f'<a href="{href(h, lang, on_home)}"' + (' aria-current="page"' if h == path else "") + f'>{t}</a>' for t, h in u["nav"])
    if has_img("banner"):
        load = 'loading="eager" fetchpriority="high"' if on_home else 'loading="lazy" decoding="async"'
        srcset = 'srcset="/images/banner-900.webp 900w, /images/banner.webp 1600w" sizes="(max-width:1200px) 100vw, 1160px" ' if has_img("banner-900") else ""
        banner = (f'<div class="promo-banner"><div class="wrap"><a href="{REGISTER_URL}" data-wt-event="banner_click" target="_blank" rel="nofollow sponsored noopener">'
                  f'<img src="/images/banner.webp" {srcset}alt="{e(u["banner_alt"])}" {wh("banner")} {load}></a></div></div>')
    else:
        banner = ""
    return f"""<a class="skip" href="#main">{u['skip']}</a>
<div class="topbar"></div>
<div class="discbar"><div class="wrap discbar-in"><span class="tag18">18+</span><p>{u['disc']}</p></div></div>
<header class="site-header"><div class="wrap nav">
{brand_link()}
<nav class="menu" id="menu" aria-label="Primary">{nav}</nav>
<div class="nav-right">{lang_switch(lang)}<a class="btn btn-gold" data-wt-event="register_click" href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">{u['register']}</a>
<button class="menu-toggle" aria-label="{u['menu']}" aria-expanded="false" aria-controls="menu">☰</button></div>
</div></header>
{banner}"""


def footer(lang, on_home=False):
    u = UI[ui_lang(lang)]

    def col(title, links):
        return f'<div><h2>{title}</h2><ul>' + "".join(f'<li><a href="{href(h, lang, on_home)}">{t}</a></li>' for t, h in links) + "</ul></div>"
    contact = ""
    if ADDRESS or PHONE or EMAIL:
        bits = "<br>".join(e(a) for a in ADDRESS)
        links = " · ".join(x for x in [f'<a href="tel:{PHONE.replace("-", "")}">{PHONE}</a>' if PHONE else "",
                                         f'<a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL else ""] if x)
        contact = f'<address class="foot-contact">{bits}{"<br>" if bits and links else ""}{links}</address>'
    mapf = (f'<iframe class="foot-map" title="{e(SITE_NAME)} location" src="https://www.google.com/maps?q={MAP_QUERY.replace(" ", "+")}&amp;z=15&amp;output=embed" '
            'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>') if ADDRESS and MAP_QUERY else ""
    guides = col(u["foot_guides"], [(e(cname(k, lang)), f"/blog/{CLUSTERS[k]['pillar']}/") for k in CLUSTERS])
    legal = "".join(f'<a href="/{p["slug"]}/">{p["title"]}</a>' for p in POLICIES) + f'<a href="/contents/">{u["contents"]}</a>'
    if len(LANGS) > 1:
        legal += "".join(f'<a href="{home_path(l)}" hreflang="{UI[l]["hreflang"]}">{UI[l]["name"]}</a>' for l in LANGS)
    return f"""<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div class="foot-about">{brand_link()}<p>{u['foot_about']}</p>{contact}{mapf}</div>
{col(u['foot_guide'], u['foot_guide_links'])}{guides}{col(u['foot_res'], u['foot_res_links'])}
</div>
<nav class="foot-legal" aria-label="Policies">{legal}</nav>
<div class="foot-bottom"><span>© {UPDATED[:4]} {e(SITE_NAME)} · {u['copyright']} <a href="/about-author/" rel="author">{e(AUTHOR['name'])}</a> · <time datetime="{UPDATED}">{u['last_updated']} {fmt_date(UPDATED, lang)}</time></span>
<span class="rg"><span class="badge18 sm">18+</span> {u['rg_line']}</span></div>
<p class="disclaimer">{u['disclaimer']}</p>
</div></footer>"""


MONTHS = {"en": "January February March April May June July August September October November December".split(),
          "ms": "Januari Februari Mac April Mei Jun Julai Ogos September Oktober November Disember".split()}


def fmt_date(d, lang):
    y, m, dd = d.split("-")
    if lang == "zh":
        return f"{y}年{int(m)}月{int(dd)}日"
    return f"{int(dd)} {MONTHS.get(lang, MONTHS['en'])[int(m) - 1]} {y}"


def byline(lang, updated=True):
    u = UI[ui_lang(lang)]
    s = (f'{u["by"]} <a href="/about-author/" rel="author">{e(AUTHOR["name"])}</a>, {e(AUTHOR["role"])} · {e(AUTHOR["city"])} &nbsp;·&nbsp; '
         f'<time datetime="{PUBLISHED}">{u["published"]} {fmt_date(PUBLISHED, lang)}</time>')
    if updated and UPDATED != PUBLISHED:
        s += f' &middot; <time datetime="{UPDATED}">{u["updated"]} {fmt_date(UPDATED, lang)}</time>'
    return f'<p class="byline">{s}</p>'


def rg_callout(lang):
    u = UI[ui_lang(lang)]
    return f'<div class="callout warn"><h3>{u["rg_title"]}</h3><p>{u["post_rg"]}</p></div>'


def breadcrumb_nav(lang, items):
    li = "".join(f'<li><a href="{u}"' + (' aria-current="page"' if i == len(items) - 1 else "") + f'>{e(n)}</a></li>'
                 for i, (n, u) in enumerate(items))
    return f'<nav class="wrap crumbs" aria-label="Breadcrumb"><ol>{li}</ol></nav>'


def page_head(kicker, h1, p="", byl=""):
    return f'<div class="wrap page-head"><span class="kicker">{kicker}</span><h1>{h1}</h1>{f"<p>{p}</p>" if p else ""}{byl}</div>'


# ---------------------------------------------------------------- home
def home(lang):
    h, u = HOME[lang], UI[lang]
    alt_note = (u["alt_note"] % BRAND_ALT) if BRAND_ALT else ""
    H = lambda s: s.replace("__ALT_NOTE__", alt_note)  # noqa: E731
    promo = (f'<a class="hero-promo" data-wt-event="register_click" href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">'
             f'<img src="/images/promo.webp" alt="{e(h["promo_alt"])}" {wh("promo")} loading="lazy" decoding="async"></a>') if has_img("promo") else ""
    cta = lambda items: "".join(f'<a class="btn {"btn-gold" if i == 0 else "btn-ghost"}" href="{l}">{t}</a>' for i, (t, l) in enumerate(items))  # noqa: E731
    cards = lambda cs: '<div class="cards">' + "".join(f'<div class="card"><div class="ic">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in cs) + "</div>"  # noqa: E731
    table = lambda head, rows: ('<div class="tbl-wrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead><tbody>"  # noqa: E731
                                + "".join("<tr><td><b>" + r[0] + "</b></td>" + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in rows) + "</tbody></table></div>")
    a, f, ins, g, s = h["about"], h["features"], h["install"], h["games"], h["safety"]
    ids = ["about", "features", "install", "games", "safety", "guides", "faq"]
    toc_labels = h["toc"][:5] + [u["guides_kicker"]] + h["toc"][5:]
    facts = "".join(f"<li><span>{k}</span><b>{v}</b></li>" for k, v in QUICK_FACTS.get(lang, []))
    sc = h["side_cta"]
    body = f"""{top(lang, home_path(lang), on_home=True)}
<section class="hero"><div class="wrap hero-grid{'' if promo else ' solo'}"><div>
<span class="eyebrow">{h['eyebrow']}</span>
<h1>{h['h1']}</h1>
{byline(lang)}
<p class="lead">{h['lead']}</p>
<div class="hero-cta">{cta(h['cta'])}</div>
<div class="trust">{''.join(f'<span>{t}</span>' for t in h['trust'])}</div>
</div>{promo}</div></section>
{per_lang(custom_sections.AFTER_HERO, lang)}
<main id="main" class="wrap layout"><article>
<section id="about" class="section"><span class="kicker">{a['kicker']}</span><h2>{a['h2']}</h2>
{''.join(f'<p>{H(p)}</p>' for p in a['p'])}<p class="muted">{a['muted']}</p>
<div class="callout"><h3>{a['callout'][0]}</h3><p>{a['callout'][1]}</p></div></section>
<section id="features" class="section"><span class="kicker">{f['kicker']}</span><h2>{f['h2']}</h2><p>{f['p']}</p>{cards(f['cards'])}</section>
<section id="install" class="section"><span class="kicker">{ins['kicker']}</span><h2>{ins['h2']}</h2><p>{ins['p']}</p>
<div class="os-tabs">{''.join(f'<span class="chip{" on" if i == 0 else ""}">{c}</span>' for i, c in enumerate(ins['chips']))}</div>
<ol class="steps">{''.join(f'<li><b>{b}</b> <span>{t}</span></li>' for b, t in ins['steps'])}</ol>
<div class="callout warn"><h3>{ins['warn'][0]}</h3><p>{ins['warn'][1]}</p></div>
<h3 style="margin-top:30px">{ins['perm_h3']}</h3><p>{ins['perm_p']}</p>{table(ins['perm_head'], ins['perm_rows'])}<p class="muted">{ins['perm_note']}</p></section>
<section id="games" class="section"><span class="kicker">{g['kicker']}</span><h2>{g['h2']}</h2><p>{g['p']}</p>{table(g['head'], g['rows'])}<p class="muted">{g['note']}</p></section>
<section id="safety" class="section"><span class="kicker">{s['kicker']}</span><h2>{s['h2']}</h2><p>{s['p']}</p>{cards(s['cards'])}
<div class="callout warn"><h3>{s['warn'][0]}</h3><p>{s['warn'][1]}</p></div></section>
{guides_section(lang)}
{per_lang(custom_sections.BEFORE_FAQ, lang)}
<section id="faq" class="section faq"><span class="kicker">FAQ</span><h2>{h['faq_h2']}</h2>
{''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{ans}</p></details>' for i, (q, ans) in enumerate(h['faq']))}</section>
</article>
<aside class="sidebar" aria-label="Sidebar">
<nav class="widget" aria-label="{u['toc']}"><h2>{u['toc']}</h2><ul class="toc">{''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in zip(ids, toc_labels))}</ul></nav>
{f'<div class="widget"><h2>{u["facts"]}</h2><ul class="facts">{facts}</ul></div>' if facts else ''}
<div class="widget cta-card"><h2>{sc[0]}</h2><p>{sc[1]}</p><a class="btn btn-gold" href="#install">{sc[2]}</a></div>
{per_lang(custom_sections.SIDEBAR, lang)}
<div class="widget rg-widget"><span class="badge18">18+</span><p>{u['rg_widget']}</p></div>
</aside></main>
<section class="ctaband"><div class="wrap"><h2>{h['band'][0]}</h2><p>{h['band'][1]}</p><div class="hero-cta">{cta(h['band'][2])}</div></div></section>
{footer(lang, on_home=True)}"""
    path = home_path(lang)
    webpage = {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": h["title"],
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@type": "Thing", "name": BRAND},
               "author": {"@id": SITE + "/about-author/#person"}, "publisher": {"@id": SITE + "/#org"},
               "datePublished": PUBLISHED, "dateModified": UPDATED, "inLanguage": u["hreflang"]}
    app = {"@type": "SoftwareApplication", "name": BRAND, "applicationCategory": "GameApplication",
           "operatingSystem": "Android, iOS", "description": strip_tags(h["desc"]),
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "MYR"}}
    schema = graph(org(), person(), website(), webpage, app, crumbs_schema([(u["home"], path)]),
                   faq_schema([(q, strip_tags(a)) for q, a in h["faq"]], lang))
    head = '<link rel="preload" as="image" href="/images/banner.webp" fetchpriority="high">' if has_img("banner") else ""
    return page(lang, h["title"], h["desc"], path, body, schema, alternates={l: home_path(l) for l in LANGS},
                og_title=h["og_title"], extra_head=head)


# ---------------------------------------------------------------- clusters (topical authority)
def cluster_posts(key):
    """Pillar first, then its supporting posts."""
    pillar = BY_SLUG[CLUSTERS[key]["pillar"]]
    return [pillar] + [p for p in POSTS if p["cluster"] == key and p is not pillar]


def cname(key, lang):
    n = CLUSTERS[key]["name"]
    return n.get(lang) or n[MAIN_LANG]


def is_pillar(p):
    return CLUSTERS[p["cluster"]]["pillar"] == p["slug"]


def guides_section(lang):
    """Home: every cluster with its pillar + supporting posts (home -> blog internal links)."""
    u = UI[ui_lang(lang)]
    cards = ""
    for k in CLUSTERS:
        lis = ""
        for p in cluster_posts(k):
            cls = ' class="pillar"' if is_pillar(p) else ""
            lis += f'<li{cls}><a href="/blog/{p["slug"]}/">{e(p["title"])}</a></li>'
        cards += f'<div class="card guide-card"><h3><a href="/blog/{CLUSTERS[k]["pillar"]}/">{e(cname(k, lang))}</a></h3><ul>{lis}</ul></div>'
    return (f'<section id="guides" class="section"><span class="kicker">{u["guides_kicker"]}</span><h2>{u["guides_h2"]}</h2>'
            f'<p>{u["guides_p"]}</p><div class="cards">{cards}</div><p><a class="btn btn-ghost" href="/blog/">{u["guides_all"]}</a></p></section>')


# ---------------------------------------------------------------- blog
def post_card(p):
    u = UI[ui_lang(p["lang"])]
    url = f"/blog/{p['slug']}/"
    pil = is_pillar(p)
    label = f'{u["pillar_badge"]} · {e(p["card"])}' if pil and p["card"] != u["pillar_badge"] else e(p["card"])
    return (f'<article class="post-card{" pillar" if pil else ""}"><span class="cat">{label}</span><h2><a href="{url}">{e(p["title"])}</a></h2>'
            f'<p>{e(p["desc"])}</p><a class="more" href="{url}">{u["read"]}</a></article>')


def grid(posts):
    return '<div class="post-grid">' + "".join(post_card(p) for p in posts) + "</div>"


def hub(path, data, groups, extra=""):
    lang = MAIN_LANG
    items = [(UI[lang]["home"], "/"), (data["crumb"], path)]
    body = f"""{top(lang, path)}
{breadcrumb_nav(lang, items)}
{page_head(data['kicker'], data['h1'], data['p'], byline(lang))}
<main id="main" class="wrap sub-main">
{''.join(f'<div class="section-label"><h2>{label}</h2></div>{grid(ps)}' for label, ps in groups if ps)}
{extra}
</main>
{footer(lang)}"""
    listed = [p for _, ps in groups for p in ps]
    coll = {"@type": "CollectionPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": data["title"],
            "isPartOf": {"@id": SITE + "/#website"}, "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{p['slug']}/"} for i, p in enumerate(listed)]}}
    return page(lang, data["title"], data["desc"], path, body, graph(org(), website(), coll, crumbs_schema(items)))


def blog_index():
    return hub("/blog/", BLOG_HUB, [(e(cname(k, MAIN_LANG)), cluster_posts(k)) for k in CLUSTERS])


def games_index():
    note = f'<div class="callout warn"><h3>{UI[MAIN_LANG]["rg_title"]}</h3><p>{GAMES_HUB["note"]}</p></div>'
    return hub("/games/", GAMES_HUB, [(e(cname(GAMES_CLUSTER, MAIN_LANG)), cluster_posts(GAMES_CLUSTER))], note)


def post_page(p):
    lang = p["lang"]
    u = UI[ui_lang(lang)]
    path = f"/blog/{p['slug']}/"
    k = p["cluster"]
    group = cluster_posts(k)
    pillar = group[0]
    up = "" if p is pillar else f'<p class="pillar-note">{u["pillar_note"]}: <a href="/blog/{pillar["slug"]}/">{e(pillar["title"])}</a></p>'
    lis = ""
    for q in group:
        cls = ' class="pillar"' if q is pillar else ""
        lis += f"<li{cls}>" + (f"<b>{e(q['title'])}</b>" if q is p else f'<a href="/blog/{q["slug"]}/">{e(q["title"])}</a>') + "</li>"
    box = f'<nav class="cluster" aria-label="{e(cname(k, lang))}"><h2>{u["cluster_h"]}: {e(cname(k, lang))}</h2><ol>{lis}</ol></nav>'
    others = "".join(f'<li><a href="/blog/{CLUSTERS[o]["pillar"]}/">{e(cname(o, lang))}</a></li>' for o in CLUSTERS if o != k)
    rel = "".join(f'<li><a href="/blog/{q["slug"]}/">{e(q["title"])}</a></li>' for q in group if q is not p)
    start = "".join(f'<li><a href="{href(h, lang)}">{t}</a></li>' for t, h in u["start_links"])
    sections = "".join(f"<h2>{e(h)}</h2>" + "".join(render_block(b, lang) for b in blocks) for h, blocks in p["sections"])
    items = [(u["home"], home_path(lang)), ("Blog", "/blog/")] + ([] if p is pillar else [(cname(k, lang), f"/blog/{pillar['slug']}/")]) + [(p["card"], path)]
    body = f"""{top(lang, '/blog/')}
{breadcrumb_nav(lang, items)}
{page_head(e(cname(k, lang)), e(p['title']), '', byline(lang, updated=False))}
<main id="main" class="wrap"><div class="article">
<article class="prose">{up}{render_block(p['intro'], lang)}{sections}
{box}
{rg_callout(lang)}<p><a href="/blog/">{u['back']}</a></p></article>
<aside class="aside"><div class="widget"><h2>{u['related']}</h2><ul>{rel}</ul></div>
<div class="widget"><h2>{u['other_topics']}</h2><ul>{others}</ul></div>
<div class="widget"><h2>{u['start']}</h2><ul>{start}</ul></div></aside>
</div></main>
{footer(lang)}"""
    art = {"@type": "BlogPosting", "@id": SITE + path + "#article", "headline": p["title"], "description": p["desc"],
           "url": SITE + path, "mainEntityOfPage": SITE + path, "inLanguage": u["hreflang"], "keywords": ", ".join(p["kw"]),
           "articleSection": cname(k, lang), "datePublished": PUBLISHED, "dateModified": UPDATED, "image": SITE + "/images/og.jpg",
           "author": {"@id": SITE + "/about-author/#person"}, "publisher": {"@id": SITE + "/#org"}}
    if p is not pillar:
        art["isPartOf"] = {"@id": f"{SITE}/blog/{pillar['slug']}/#article"}
    head = (f'<meta property="article:author" content="{e(AUTHOR["name"])}">'
            f'<meta property="article:published_time" content="{PUBLISHED}T08:00:00+08:00">'
            f'<meta property="article:modified_time" content="{UPDATED}T08:00:00+08:00">')
    kw = p["kw"] + pillar["kw"][:1] + [BRAND]
    return page(lang, f"{p['title']} | {SITE_NAME}", p["desc"], path, body, graph(org(), person(), art, crumbs_schema(items)),
                og_type="article", extra_head=head, keywords=kw)


def audit_clusters():
    """Topical-authority link rules. Returns warnings (the build still succeeds)."""
    out, inbound = [], {}
    for key, c in CLUSTERS.items():
        assert c["pillar"] in BY_SLUG and BY_SLUG[c["pillar"]]["cluster"] == key, f"cluster {key}: pillar post missing or in another cluster"
    for p in POSTS:
        assert p["cluster"] in CLUSTERS, f"{p['slug']}: unknown cluster {p['cluster']}"
        targets = {t for t, _ in LINK_RE.findall("\n".join([p["intro"]] + [b for _, blocks in p["sections"] for b in blocks]))}
        for t in targets:
            inbound.setdefault(t, set()).add(p["slug"])
        if is_pillar(p):
            out += [f"pillar {p['slug']} does not link supporting post {q['slug']}" for q in cluster_posts(p["cluster"])[1:] if q["slug"] not in targets]
        elif CLUSTERS[p["cluster"]]["pillar"] not in targets:
            out.append(f"{p['slug']} does not link its pillar")
        if not any(t in BY_SLUG and BY_SLUG[t]["cluster"] != p["cluster"] for t in targets):
            out.append(f"{p['slug']} has no link to another cluster")
        if not any(t.startswith("home") for t in targets):
            out.append(f"{p['slug']} has no link to a home section")
    out += [f"orphan: no post links to {p['slug']}" for p in POSTS if p["slug"] not in inbound]
    return out


# ---------------------------------------------------------------- author + policies + contents
def author_page():
    lang, d = MAIN_LANG, AUTHOR_PAGE
    path = "/about-author/"
    initials = "".join(w[0] for w in AUTHOR["name"].split()[:2]).upper()
    photo = (f'<img class="author-photo" src="/images/author.webp" {wh("author")} alt="{e(AUTHOR["name"])}, {e(AUTHOR["role"])}" fetchpriority="high">'
             if AUTHOR.get("photo") and has_img("author") else f'<div class="author-photo" aria-hidden="true">{initials}</div>')
    items = [(UI[lang]["home"], "/"), (d["crumb"], path)]
    secs = "".join(f"<h2>{h}</h2>{b}" for h, b in d["sections"])
    addr = f" {d['address']} {e(' '.join(ADDRESS))}" if ADDRESS else ""
    body = f"""{top(lang, path)}
{breadcrumb_nav(lang, items)}
<main id="main" class="wrap"><div class="author-hero">{photo}<div>
<span class="kicker">{d['kicker']}</span><h1>{e(AUTHOR['name'])}</h1><p class="role">{e(AUTHOR['role'])} · {e(AUTHOR['city'])}</p><p>{AUTHOR['bio']}</p></div></div>
<section class="article" style="grid-template-columns:1fr;padding-top:0"><div class="prose">{secs}
<div class="callout"><h3>{d['corrections_h']}</h3><p>{d['corrections']}{addr}</p></div>
{rg_callout(lang)}</div></section></main>
{footer(lang)}"""
    prof = {"@type": "ProfilePage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": d["title"],
            "mainEntity": {"@id": SITE + "/about-author/#person"}, "dateModified": UPDATED}
    return page(lang, d["title"], d["desc"], path, body, graph(org(), person(), prof, crumbs_schema(items)), og_type="profile")


def policy_page(p):
    lang = MAIN_LANG
    u = UI[lang]
    path = f"/{p['slug']}/"
    items = [(u["home"], "/"), (p["title"], path)]
    toc = "".join(f'<li><a href="#{i}">{h}</a></li>' for i, h, _ in p["body"])
    secs = "".join(f'<h2 id="{i}">{h}</h2>{b}' for i, h, b in p["body"])
    byl = (f'<p class="byline">{u["maintained"]} <a href="/about-author/" rel="author">{e(AUTHOR["name"])}</a>, {e(AUTHOR["city"])} · '
           f'<time datetime="{UPDATED}">{u["updated"]} {fmt_date(UPDATED, lang)}</time></p>')
    body = f"""{top(lang, path)}
{breadcrumb_nav(lang, items)}
{page_head(p['kicker'], p['title'], '', byl)}
<main id="main" class="wrap sub-main"><article class="prose solo">
<div class="ai-sum"><b>{u['in_short']}</b><p>{p['summary']}</p></div>
<nav class="toc-inline" aria-label="{u['on_page']}"><b>{u['on_page']}</b><ol>{toc}</ol></nav>
{secs}</article></main>
{footer(lang)}"""
    wp = {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": p["title"],
          "description": strip_tags(p["desc"]), "isPartOf": {"@id": SITE + "/#website"}, "dateModified": UPDATED}
    return page(lang, f"{p['title']} | {SITE_NAME}", p["desc"], path, body, graph(org(), wp, crumbs_schema(items)))


def all_pages():
    """(path, title) for every public page; drives contents page, sitemap and llms.txt."""
    out = [(home_path(l), HOME[l]["title"]) for l in LANGS]
    out += [("/blog/", BLOG_HUB["title"]), ("/games/", GAMES_HUB["title"]), ("/about-author/", AUTHOR_PAGE["title"])]
    out += [(f"/{p['slug']}/", p["title"]) for p in POLICIES]
    out += [("/contents/", UI[MAIN_LANG]["contents"])]
    out += [(f"/blog/{p['slug']}/", p["title"]) for k in CLUSTERS for p in cluster_posts(k)]
    return out


def contents_page():
    lang, path = MAIN_LANG, "/contents/"
    u = UI[lang]
    items = [(u["home"], "/"), (u["contents"], path)]
    groups = [(u["main_pages"], [x for x in all_pages() if not x[0].startswith("/blog/") or x[0] == "/blog/"])]
    groups += [(e(cname(k, lang)), [(f"/blog/{p['slug']}/", p["title"]) for p in cluster_posts(k)]) for k in CLUSTERS]
    secs = "".join(f"<h2>{g}</h2><ul>" + "".join(f'<li><a href="{x}">{e(t)}</a></li>' for x, t in links) + "</ul>" for g, links in groups if links)
    body = f"""{top(lang, path)}
{breadcrumb_nav(lang, items)}
{page_head(u['site_map'], u['contents'], u['contents_p'])}
<main id="main" class="wrap sub-main"><div class="prose solo">{secs}</div></main>
{footer(lang)}"""
    return page(lang, f"{u['contents']} | {SITE_NAME}", u["contents_p"] + " " + u["guides_p"], path, body, graph(org(), crumbs_schema(items)))


def not_found():
    lang = MAIN_LANG
    u = UI[lang]
    body = f"""{top(lang, '/404')}
{page_head('404', u['nf_title'], u['nf_p'])}
<main id="main" class="wrap sub-main"><p><a class="btn btn-gold" href="/">{u['home']}</a> <a class="btn btn-ghost" href="/blog/">{u['nf_blog']}</a></p>{guides_section(lang)}</main>
{footer(lang)}"""
    return page(lang, f"{u['nf_title']} | {SITE_NAME}", u["nf_p"] + " " + BLOG_HUB["desc"], "/404", body, "").replace(
        '<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex">')


# ---------------------------------------------------------------- output
def replace_tokens(s):
    for k, v in TOKENS.items():
        s = s.replace(k, v)
    return s


def write(rel, content):
    path = os.path.join(DIST, replace_tokens(rel).lstrip("/"))
    if path.endswith("/"):
        path += "index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(replace_tokens(content))


def sitemap():
    urls = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod></url>" for u, _ in all_pages())
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def llms_txt():
    lines = [f"# {SITE_NAME}", "", f"> Independent informational guide to the {BRAND} mobile app (features, safe install, games, safety, responsible gaming). "
             f"Edited by {AUTHOR['name']}, {AUTHOR['city']}. Does not distribute software or offer gambling. 18+.", ""]
    lines += [f"- [{strip_tags(t)}]({SITE}{u})" for u, t in all_pages()]
    return "\n".join(lines) + "\n"


def copy_static():
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"), ignore=shutil.ignore_patterns("style.css", ".DS_Store"))
    shutil.copytree(IMG, os.path.join(DIST, "images"), ignore=shutil.ignore_patterns("src", "sizes.json", ".DS_Store"))
    for f in os.listdir(ROOT):
        if f in ("_headers", "favicon.ico", "favicon.svg", "site.webmanifest") or re.fullmatch(r"(favicon-\d+|apple-touch-icon)\.png|[0-9a-f]{32}\.txt", f):
            shutil.copy(os.path.join(ROOT, f), DIST)


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    for lang in LANGS:
        write(home_path(lang), home(lang))
    write("/blog/", blog_index())
    write("/games/", games_index())
    for p in POSTS:
        write(f"/blog/{p['slug']}/", post_page(p))
    write("/about-author/", author_page())
    for p in POLICIES:
        write(f"/{p['slug']}/", policy_page(p))
    write("/contents/", contents_page())
    write("/404.html", not_found())
    write("/sitemap.xml", sitemap())
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("/llms.txt", llms_txt())
    copy_static()
    leftover = [t for t in ("__BRAND__", "__SLUG__", "__SITE__", "__ALT_NOTE__") for root, _, fs in os.walk(DIST)
                for f in fs if f.endswith((".html", ".xml", ".txt")) and t in open(os.path.join(root, f), encoding="utf-8").read()]
    if leftover:
        sys.exit(f"unreplaced tokens: {set(leftover)}")
    for w in audit_clusters():
        print("  cluster:", w)
    for w in META_WARN:
        print("  meta:", w)
    missing = [n for n in ("banner", "promo", "popup", "og") if not has_img(n)]
    print(f"built {len(all_pages())} pages in dist/" + (f"  (no image yet: {', '.join(missing)}; run build/images.py)" if missing else ""))


if __name__ == "__main__":
    main()
