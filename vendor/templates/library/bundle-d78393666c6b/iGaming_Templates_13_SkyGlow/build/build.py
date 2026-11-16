"""Static site generator (iGaming_Templates_4_CasinoPortal).

Run:  python3 build/build.py      -> writes the whole site to dist/ (wiped first)
Every page is built in every language of LANGS (ms = default at "/", en at "/en/"), linked with hreflang.
Settings: site_config.py. Text: content.py (UI + home), pages.py (site pages), posts.py (blog clusters).
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
from pages import PAGES  # noqa: E402
from posts import POSTS, CLUSTERS  # noqa: E402
import custom_sections  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
IMG = os.path.join(ROOT, "images")
MAIN = LANGS[0]
PAGE = {p["key"]: p for p in PAGES}
POST = {p["key"]: p for p in POSTS}
EXTERNAL = {"@register": REGISTER_URL, "@login": LOGIN_URL, "@app": APP_URL, "@chat": LIVECHAT_URL or REGISTER_URL}
FIXED = {"blog": {"ms": "blog", "en": "blog"}, "contents": {"ms": "kandungan", "en": "contents"}}
SIZES = json.load(open(os.path.join(IMG, "sizes.json"))) if os.path.exists(os.path.join(IMG, "sizes.json")) else {}
TOKENS = {"__BRAND__": BRAND, "__SLUG__": SLUG, "__EMAIL__": EMAIL or "—", "__PHONE__": PHONE or "—"}
WARN = []
e = html.escape

with open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8") as _f:
    CSS = " ".join(_f.read().split())
CSS += ":root{" + "".join(f"--{k}:{v};" for k, v in THEME.items()) + "}" + " ".join(custom_sections.EXTRA_CSS.split())
JS_VER = hashlib.md5(open(os.path.join(ROOT, "assets", "main.js"), "rb").read()).hexdigest()[:8]


# ---------------------------------------------------------------- helpers
def tok(s, lang=MAIN):
    s = s.replace("__TAGLINE__", TAGLINE.get(lang, TAGLINE[MAIN]))
    for k, v in TOKENS.items():
        s = s.replace(k, v)
    return s


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def has_img(name):
    return name in SIZES


def img(name, alt, lazy=True, cls=""):
    w, h = SIZES[name]
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/images/{name}.webp" alt="{e(alt)}" width="{w}" height="{h}" {load}{c}>'


def prefix(lang):
    return "" if lang == MAIN else f"/{lang}"


def url(key, lang):
    """Path of any page key in a language."""
    if key == "home":
        return prefix(lang) + "/"
    if key in PAGE:
        return f"{prefix(lang)}/{PAGE[key][lang]['slug']}/"
    if key in POST:
        return f"{prefix(lang)}/blog/{POST[key][lang]['slug']}/"
    if key in FIXED:
        return f"{prefix(lang)}/{FIXED[key][lang]}/"
    raise ValueError(f"unknown link target: {key}")


def label(key, lang):
    if key in PAGE:
        return PAGE[key][lang]["nav"]
    if key in POST:
        return POST[key][lang]["title"]
    return {"blog": UI[lang]["blog"], "contents": UI[lang]["contents"], "home": UI[lang]["home"]}[key]


def href(target, lang):
    if target.startswith("home#"):
        return url("home", lang) + target[4:]
    return url(target, lang)


def link(target, text, lang, cls=""):
    c = f' class="{cls}"' if cls else ""
    if target in EXTERNAL:
        return f'<a{c} href="{EXTERNAL[target]}" target="_blank" rel="nofollow sponsored noopener">{text}</a>'
    if target.startswith("#"):
        return f'<a{c} href="{target}">{text}</a>'
    return f'<a{c} href="{href(target, lang)}">{text}</a>'


LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")


def linkify(s, lang):
    return LINK_RE.sub(lambda m: link(m.group(1), m.group(2), lang), s)


def blocks_html(blocks, lang):
    out = []
    for text in blocks:
        for chunk in text.split("\n\n"):
            lines = chunk.split("\n")
            if all(l.startswith("- ") for l in lines):
                out.append("<ul>" + "".join(f"<li>{linkify(e(l[2:], quote=False), lang)}</li>" for l in lines) + "</ul>")
            elif all(re.match(r"\d+\. ", l) for l in lines):
                out.append("<ol>" + "".join(f"<li>{linkify(e(l.split('. ', 1)[1], quote=False), lang)}</li>" for l in lines) + "</ol>")
            else:
                out.append(f"<p>{linkify(e(chunk, quote=False), lang)}</p>")
    return "".join(out)


def check_seo(path, lang, d):
    """High-CTR meta rules + focus keyword placement (after tokens)."""
    t, ds, f = tok(d["title"], lang), tok(d["desc"], lang), tok(d["focus"], lang).lower()
    if len(t) > 60:
        WARN.append(f"meta {path}: title {len(t)} chars (max 60)")
    if not 120 <= len(ds) <= 160:
        WARN.append(f"meta {path}: description {len(ds)} chars (120-160)")
    for field in ("title", "desc", "h1", "intro"):
        if f not in strip_tags(tok(d[field], lang)).lower():
            WARN.append(f"focus {path}: '{f}' missing from {field}")


# ---------------------------------------------------------------- schema
def graph(*nodes):
    nodes = [n for n in nodes if n]
    if any(n.get("@id") == SITE + "/#org" for n in nodes):
        nodes.insert(1, brand_node())
        if not any(n.get("@id") == SITE + "/#website" for n in nodes):
            nodes.insert(2, website())
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False) + "</script>"


def ent(key, lang):
    """One topic entity as a schema Thing linked to its (verified) Wikipedia page."""
    ms, en, wiki = ENTITIES[key]
    return {"@type": "Thing", "name": ms if lang == "ms" else en, "sameAs": wiki}


def about_mentions(keys, lang):
    keys = [k for k in (keys or []) if k in ENTITIES]
    out = {}
    if keys:
        out["about"] = [ent(k, lang) for k in keys[:2]]
    if keys[2:]:
        out["mentions"] = [ent(k, lang) for k in keys[2:]]
    return out


def org():
    """The ONE brand entity. Every page, post and the app point to it by @id."""
    o = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "alternateName": BRAND_ALT, "url": SITE + "/",
         "logo": {"@type": "ImageObject", "@id": SITE + "/#logo", "url": SITE + "/images/logo-512.png", "width": 512, "height": 512},
         "image": {"@id": SITE + "/#logo"}, "brand": {"@id": SITE + "/#brand"},
         "areaServed": {"@type": "Country", "name": "Malaysia", "sameAs": ENTITIES["malaysia"][2]},
         "knowsAbout": [ent(k, "en") for k in ORG_KNOWS_ABOUT], "slogan": TAGLINE["en"]}
    if SAME_AS:
        o["sameAs"] = SAME_AS
    if EMAIL:
        o["email"] = EMAIL
    if PHONE:
        o["telephone"] = PHONE
    if ADDRESS:
        o["address"] = {"@type": "PostalAddress", "streetAddress": ", ".join(ADDRESS), "addressCountry": "MY"}
    return o


def brand_node():
    return {"@type": "Brand", "@id": SITE + "/#brand", "name": BRAND, "alternateName": BRAND_ALT, "logo": {"@id": SITE + "/#logo"}, "url": SITE + "/"}


def website():
    return {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": f"{BRAND} Malaysia", "alternateName": BRAND_ALT,
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": [UI[l]["hreflang"] for l in LANGS]}


def item_list(pid, entries):
    return {"@type": "ItemList", "@id": pid, "numberOfItems": len(entries),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + u} for i, (n, u) in enumerate(entries)]}


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": strip_tags(n), "item": SITE + u}
                                                           for i, (n, u) in enumerate(items)]}


def faq_schema(faq, lang):
    return {"@type": "FAQPage", "inLanguage": UI[lang]["hreflang"], "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(linkify(a, lang))}} for q, a in faq]} if faq else None


# ---------------------------------------------------------------- shell
def analytics():
    if not GA4_ID:
        return ""
    return f"""<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA4_ID}");
(function(){{var l=false,e=["scroll","mousemove","touchstart","keydown","click"];function load(){{if(l)return;l=true;e.forEach(function(x){{window.removeEventListener(x,load,{{passive:true}});}});
var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}";document.head.appendChild(s);}}
e.forEach(function(x){{window.addEventListener(x,load,{{passive:true}});}});window.addEventListener("load",function(){{setTimeout(load,3500);}});}})();</script>"""


def logo(lang):
    inner = img("logo", BRAND, lazy=False) if has_img("logo") else "".join(f'<span class="{c}">{e(t)}</span>' for t, c in LOGO_PARTS)
    return f'<a class="logo" href="{url("home", lang)}">{inner}</a>'  # visible text (or img alt) is the accessible name


def header(lang, key):
    u = UI[lang]
    items = ""
    for lbl, k, kids in u["nav"]:
        cur = ' aria-current="page"' if k == key else ""
        if kids:
            sub = "".join(f'<a href="{url(c, lang)}">{e(label(c, lang))}</a>' for c in kids)
            items += f'<div class="dd"><a href="{url(k, lang)}"{cur}>{lbl} <span aria-hidden="true">▾</span></a><div class="dd-menu">{sub}</div></div>'
        else:
            items += f'<a href="{url(k, lang)}"{cur}>{lbl}</a>'
    langs = "".join(f'<a href="{url(key, l)}" hreflang="{UI[l]["hreflang"]}" lang="{UI[l]["html_lang"]}"' + (' aria-current="true"' if l == lang else "")
                    + f'>{UI[l]["label"]}</a>' for l in LANGS)
    return f"""<header class="site-header"><div class="wrap nav">
{logo(lang)}
<nav class="menu" id="menu" aria-label="Menu">{items}</nav>
<div class="nav-right"><div class="lang" aria-label="Language">{langs}</div>
{link('@register', u['register'], lang, 'btn btn-line')}{link('@login', u['login'], lang, 'btn btn-fill')}
<button class="menu-toggle" aria-controls="menu" aria-expanded="false" aria-label="{u['menu']}">☰</button></div>
</div></header>"""


def footer(lang):
    u = UI[lang]
    cols = "".join(f"<div><h2>{t}</h2><ul>" + "".join(f'<li><a href="{url(k, lang)}">{e(label(k, lang))}</a></li>' for k in keys) + "</ul></div>"
                   for t, keys in u["foot_cols"])
    guides = f'<div><h2>{u["foot_guides"]}</h2><ul>' + "".join(
        f'<li><a href="{url(c["pillar"], lang)}">{e(c["name"][lang])}</a></li>' for c in CLUSTERS.values()) + "</ul></div>"
    pays = "".join(f"<span>{e(p)}</span>" for p in PAYMENTS)
    langs = " · ".join(f'<a href="{url("home", l)}" hreflang="{UI[l]["hreflang"]}">{UI[l]["name"]}</a>' for l in LANGS)
    social = "".join(f'<a href="{x}" rel="me noopener" target="_blank">{e(x.split("//")[-1].split("/")[0])}</a>' for x in SAME_AS)
    if social:
        langs += f' · <span class="social">{social}</span>' 
    return f"""<footer class="site-footer"><div class="wrap">
<div class="foot-grid"><div class="foot-about">{logo(lang)}<p>{tok(u['foot_about'], lang)}</p><div class="pills">{pays}</div></div>{cols}{guides}</div>
<div class="foot-bottom"><span class="r18">18+</span><span>{u['foot_rg']}</span><span>© {UPDATED[:4]} {e(BRAND)} Malaysia</span><span>{langs}</span></div>
<p class="foot-disc">{u['foot_disc']}</p>
</div></footer>"""


def float_bar(lang):
    u = UI[lang]
    return (f'<div class="float-cta" role="navigation" aria-label="{u["login"]} / {u["register"]}"><div class="float-in">'
            f'{link("@login", "🔑 " + u["login"], lang, "btn btn-sky")}{link("@register", "🎁 " + u["float_register"], lang, "btn btn-gold")}</div></div>')


def popup(lang):
    """Phone-size (9:16) popup. First open after the visitor's first interaction (or 20 s), then 30 s after every
    close (assets/main.js). Its image is only requested when it opens, so it never affects LCP/CLS."""
    u = UI[lang]
    if has_img("popup"):
        w, h = SIZES["popup"]
        inner = f'<img data-src="/images/popup.webp" alt="{e(u["popup_alt"])}" width="{w}" height="{h}" decoding="async">'
    else:
        inner = (
        f'<div class="popup-card"><span class="logo">{"".join(f"<span class={c}>{e(t)}</span>" for t, c in LOGO_PARTS)}</span>'
        f'<b>{u["popup_title"]}</b><p>{u["popup_text"]}</p><span class="btn btn-fill">{u["float_register"]}</span></div>')
    return (f'<div class="popup" id="promo-popup" role="dialog" aria-modal="true" aria-label="{e(u["popup_title"])}"><div class="popup-inner">'
            f'<button class="popup-close" type="button" aria-label="{u["close"]}">&times;</button>'
            f'<a href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">{inner}</a></div></div>')


def banner(lang, eager):
    """Promo banner above the hero, 900x500."""
    u = UI[lang]
    if has_img("banner"):
        inner = img("banner", u["banner_alt"], lazy=not eager)
    else:
        inner = (f'<div class="banner-card"><span class="logo">{"".join(f"<span class={c}>{e(t)}</span>" for t, c in LOGO_PARTS)}</span>'
                 f'<b>{u["banner_title"]}</b><p>{u["banner_sub"]}</p><span class="btn btn-white">{u["float_register"]}</span></div>')
    return f'<div class="wrap"><a class="banner" href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">{inner}</a></div>'


def page(lang, key, d, path, main, schema, og_type="website", kw=None, extra_head=""):
    u = UI[lang]
    check_seo(path, lang, d)
    alts = "".join(f'<link rel="alternate" hreflang="{UI[l]["hreflang"]}" href="{SITE}{url(key, l)}">' for l in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}{url(key, MAIN)}">'
    og_alt = "".join(f'<meta property="og:locale:alternate" content="{UI[l]["og_locale"]}">' for l in LANGS if l != lang)
    verify = (f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">' if GSC_VERIFICATION else "") + \
             (f'<meta name="msvalidate.01" content="{BING_VERIFICATION}">' if BING_VERIFICATION else "")
    keywords = ", ".join(dict.fromkeys(kw or d.get("kw") or KEYWORDS[lang]))
    title, desc = d["title"], d["desc"]
    return f"""<!doctype html>
<html lang="{u['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{verify}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="{THEME.get('accent', '#FF8C00')}">
<link rel="canonical" href="{SITE}{path}">
{alts}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(BRAND)} Malaysia">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:locale" content="{u['og_locale']}">{og_alt}
<meta property="og:image" content="{SITE}/images/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/outfit-800.woff2" as="font" type="font/woff2" crossorigin>
{extra_head}
<style>{CSS}</style>
{analytics()}
{schema}
</head>
<body>
<a class="skip" href="#main">{u['skip']}</a>
{header(lang, key)}
<main id="main">{main}</main>
{footer(lang)}
{float_bar(lang)}
{popup(lang)}
<script src="/assets/main.js?v={JS_VER}" defer></script>
{EXTRA_BODY_END}
</body>
</html>"""


def crumbs(items):
    li = "".join(f'<li><a href="{u}"' + (' aria-current="page"' if i == len(items) - 1 else "") + f'>{e(strip_tags(n))}</a></li>' for i, (n, u) in enumerate(items))
    return f'<nav class="wrap crumbs" aria-label="Breadcrumb"><ol>{li}</ol></nav>'


def square(name, alt, icon, lazy=True):
    """Square image or a styled square fallback with an icon."""
    return img(name, alt, lazy) if has_img(name) else f'<div class="sq-fallback" aria-hidden="true">{icon}</div>'


def faq_html(faq, lang, title):
    if not faq:
        return ""
    return (f'<section class="block faq"><h2>{title}</h2>' + "".join(f"<details><summary>{q}</summary><p>{linkify(a, lang)}</p></details>" for q, a in faq)
            + "</section>")


def cta_band(lang, band=None):
    u = UI[lang]
    t, d = band or (u["cta_h"], u["cta_p"])
    return (f'<section class="band"><div class="wrap"><h2>{tok(t, lang)}</h2><p>{tok(d, lang)}</p>'
            f'<div class="cta-row">{link("@register", u["float_register"], lang, "btn btn-gold")}{link("@login", u["login"], lang, "btn btn-ghost")}</div></div></section>')


# ---------------------------------------------------------------- clusters
def cluster_posts(k):
    pillar = POST[CLUSTERS[k]["pillar"]]
    return [pillar] + [p for p in POSTS if p["cluster"] == k and p is not pillar]


def cluster_box(k, lang, current=None):
    u = UI[lang]
    lis = ""
    for p in cluster_posts(k):
        cls = ' class="pillar"' if p["key"] == CLUSTERS[k]["pillar"] else ""
        t = e(p[lang]["title"])
        lis += f"<li{cls}>" + (f"<b>{t}</b>" if p is current else f'<a href="{url(p["key"], lang)}">{t}</a>') + "</li>"
    return f'<nav class="cluster" aria-label="{e(CLUSTERS[k]["name"][lang])}"><h2>{u["cluster_h"]}: {e(CLUSTERS[k]["name"][lang])}</h2><ol>{lis}</ol></nav>'


def post_card(p, lang):
    d = p[lang]
    pil = p["key"] == CLUSTERS[p["cluster"]]["pillar"]
    thumb = f'<a class="thumb" href="{url(p["key"], lang)}">{img("posts/" + p["key"], d["title"])}</a>' if has_img("posts/" + p["key"]) else ""
    return (f'<article class="post-card{" pillar" if pil else ""}">{thumb}<span class="cat">{e(d["card"])}</span>'
            f'<h3><a href="{url(p["key"], lang)}">{e(d["title"])}</a></h3><p>{e(d["desc"])}</p><a class="more" href="{url(p["key"], lang)}">{UI[lang]["read"]}</a></article>')


def guides_section(lang):
    u = UI[lang]
    cards = ""
    for k, c in CLUSTERS.items():
        lis = "".join(f'<li{" class=pillar" if p["key"] == c["pillar"] else ""}><a href="{url(p["key"], lang)}">{e(p[lang]["title"])}</a></li>' for p in cluster_posts(k))
        cards += f'<div class="guide-card"><h3><a href="{url(c["pillar"], lang)}">{e(c["name"][lang])}</a></h3><ul>{lis}</ul></div>'
    return (f'<section class="block" id="guides"><div class="head"><small>{u["guides_small"]}</small><h2>{tok(u["guides_h2"], lang)}</h2></div>'
            f'<div class="guides">{cards}</div><p class="center">{link("blog", u["all_guides"], lang, "btn btn-line")}</p></section>')


def audit():
    """Topical-authority link rules (posts) + every page reachable."""
    inbound = {}
    sources = [(p["key"], p, "post") for p in POSTS] + [(p["key"], p, "page") for p in PAGES]
    for key, p, kind in sources:
        d = p[MAIN]
        text = "\n".join([d["intro"]] + [b for _, bl in d.get("sections", []) for b in bl] + [a for _, a in d.get("faq", [])])
        targets = {t for t, _ in LINK_RE.findall(text)}
        for t in targets:
            if not t.startswith("@") and not t.startswith("home#"):
                url(t, MAIN)  # raises on unknown targets
            inbound.setdefault(t, set()).add(key)
        if kind != "post":
            continue
        c = CLUSTERS[p["cluster"]]
        if key == c["pillar"]:
            WARN.extend(f"cluster: pillar {key} does not link {q['key']}" for q in cluster_posts(p["cluster"])[1:] if q["key"] not in targets)
        elif c["pillar"] not in targets:
            WARN.append(f"cluster: {key} does not link its pillar {c['pillar']}")
        if not any(t in POST and POST[t]["cluster"] != p["cluster"] for t in targets):
            WARN.append(f"cluster: {key} has no link to another cluster")
        if not any(t in PAGE or t.startswith("home") for t in targets):
            WARN.append(f"cluster: {key} has no link to a site page")
    WARN.extend(f"cluster: orphan post {p['key']} (no inline link from any page/post)" for p in POSTS if p["key"] not in inbound)


# ---------------------------------------------------------------- home
def head_html(d, lang, center=True):
    """Section heading: pill kicker, h2 (with <em> highlight), accent bar, optional intro."""
    intro = f'<p>{linkify(tok(d["p"], lang), lang)}</p>' if isinstance(d.get("p"), str) else ""
    return (f'<div class="head{" center" if center else ""}"><span class="kicker">{tok(d["kicker"], lang)}</span>'
            f'<h2>{tok(d["h2"], lang)}</h2><span class="bar" aria-hidden="true"></span>{intro}</div>')


def home(lang):
    h, u = HOME[lang], UI[lang]
    path = url("home", lang)
    games = [p for p in PAGES if p["type"] == "game"]
    game_cards = "".join(
        f'<a class="game-card" href="{url(p["key"], lang)}">{square("categories/" + p["key"], p[lang]["nav"], p["icon"])}'
        f'<h3>{e(p[lang]["nav"])}</h3><p>{e(p[lang]["card"])}</p></a>' for p in games)
    stats = "".join(f'<div class="stat"><b>{e(v)}</b><span>{e(t[lang])}</span></div>' for v, t in STATS)
    a, f, cmp_, mo, pay, ap, rg, sv = h["about"], h["features"], h["compare"], h["more"], h["pay"], h["app"], h["rg"], h["serve"]
    feats = "".join(f'<div class="feature"><span class="ic" aria-hidden="true">{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in f["items"])
    duo = "".join(f'<article class="duo-card">{square(im, t, ic)}<h3>{t}</h3><p>{linkify(d, lang)}</p>{link(k, label(k, lang) + " →", lang, "more")}</article>'
                  for im, ic, t, d, k in h["splits"])
    table = ('<div class="tbl-wrap"><table class="tbl"><thead><tr>' + "".join(f"<th scope=\"col\">{c}</th>" for c in cmp_["head"]) + "</tr></thead><tbody>"
             + "".join("<tr><th scope=\"row\">" + r[0] + "</th>" + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in cmp_["rows"]) + "</tbody></table></div>")
    chips = "".join(f"<li>{e(x)}</li>" for x in PAYMENTS)
    promos = "".join(promo_card(pr, lang) for pr in PROMOS)
    rgc = "".join(f'<div class="rg-card"><span class="ic" aria-hidden="true">{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in rg["cards"])
    states = "".join(f"<li>{e(x)}</li>" for x in STATES)
    steps = "".join(f'<li class="step"><span class="ic" aria-hidden="true">{i}</span><h3>{t}</h3><p>{d}</p></li>' for i, t, d in u["steps"])
    latest = "".join(post_card(POST[c["pillar"]], lang) for c in CLUSTERS.values())
    main = f"""<section class="hero-band">{banner(lang, True)}
<div class="wrap hero-grid"><div><span class="pill">{h['eyebrow']}</span><h1>{tok(h['h1'], lang)}</h1><p class="lead">{tok(h['intro'], lang)}</p>
<div class="cta-row">{''.join(link(t, l, lang, 'btn btn-glow' if i == 0 else 'btn btn-ghost') for i, (l, t) in enumerate(h['cta']))}</div></div>
<div class="hero-art">{square("hero", BRAND, "🎰", lazy=False)}</div></div></section>
<section class="stats" aria-label="{BRAND}"><div class="wrap stats-grid">{stats}</div></section>
<section class="sec"><div class="wrap split"><div>{head_html(a, lang, False)}{''.join(f'<p>{linkify(tok(x, lang), lang)}</p>' for x in a['p'])}<p>{linkify(a['more'], lang)}</p></div>
<div class="split-img">{square("about", tok(a['kicker'], lang), "🎲")}</div></div></section>
<section class="sec tint"><div class="wrap">{head_html(f, lang)}<div class="features">{feats}</div></div></section>
{custom_sections.per_lang(custom_sections.AFTER_HERO, lang)}
<section class="sec" id="games"><div class="wrap">{head_html(h['games'], lang)}<div class="game-grid">{game_cards}</div><div class="duo">{duo}</div></div></section>
<section class="sec tint"><div class="wrap">{head_html(cmp_, lang)}{table}</div></section>
<section class="sec"><div class="wrap split rev"><div class="split-img">{square("more", tok(mo['kicker'], lang), "🎱")}</div><div>{head_html(mo, lang, False)}{''.join(f'<p>{linkify(x, lang)}</p>' for x in mo['p'])}</div></div></section>
<section class="sec tint" id="pay"><div class="wrap split"><div>{head_html(pay, lang, False)}<ul class="chips">{chips}</ul></div><div class="split-img">{square("pay", tok(pay['kicker'], lang), "💳")}</div></div></section>
<section class="sec" id="promos"><div class="wrap">{head_html(h['promos'], lang)}<div class="promos">{promos}</div></div></section>
<section class="sec tint" id="app"><div class="wrap split rev"><div class="split-img">{square("app", tok(ap['kicker'], lang), "📱")}</div><div>{head_html(ap, lang, False)}
<ul class="ticks">{''.join(f'<li>{x}</li>' for x in ap['bullets'])}</ul><div class="cta-row">{link('@app', u['float_register'], lang, 'btn btn-glow')}{link(ap['target'], ap['btn'], lang, 'btn btn-line')}</div></div></div></section>
<section class="sec" id="start"><div class="wrap">{head_html(h['start'], lang)}<ol class="steps">{steps}</ol></div></section>
<section class="sec tint"><div class="wrap">{head_html(rg, lang)}<div class="rg-grid">{rgc}</div><p class="center">{linkify(rg['more'], lang)}</p></div></section>
<section class="sec"><div class="wrap">{head_html(sv, lang)}<ul class="states">{states}</ul></div></section>
<section class="sec tint"><div class="wrap">{guides_section(lang)}</div></section>
{custom_sections.per_lang(custom_sections.BEFORE_FAQ, lang)}
<div class="wrap">{faq_html(h['faq'], lang, tok(h['faq_h2'], lang)).replace('<section class="block faq">', '<section class="block faq" id="faq">')}
<section class="block"><div class="head center"><h2>{u['latest_h']}</h2></div><div class="post-grid">{latest}</div></section></div>
{cta_band(lang, h['band'])}"""
    wp = {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": tok(h["title"], lang), "isPartOf": {"@id": SITE + "/#website"},
          "about": [{"@id": SITE + "/#org"}] + [ent(k, lang) for k in ("online_casino", "malaysia")],
          "mentions": [ent(k, lang) for k in ("slot", "baccarat", "sports_betting", "bingo", "ringgit")],
          "mainEntity": {"@id": SITE + path + "#games"}, "publisher": {"@id": SITE + "/#org"},
          "inLanguage": u["hreflang"], "datePublished": PUBLISHED, "dateModified": UPDATED}
    cats = item_list(SITE + path + "#games", [(tok(p[lang]["nav"], lang), url(p["key"], lang)) for p in games])
    head = '<link rel="preload" as="image" href="/images/banner.webp" fetchpriority="high">' if has_img("banner") else ""
    return page(lang, "home", h, path, main, graph(org(), website(), wp, cats, faq_schema(h["faq"], lang), crumbs_schema([(u["home"], path)])),
                kw=h["kw"] + KEYWORDS[lang], extra_head=head)


def promo_card(pr, lang):
    key, im, txt = pr
    t, d = txt[lang]
    pic = square("promos/" + im, t, "🎁") if im else '<div class="sq-fallback">🎁</div>'
    return (f'<div class="promo">{pic}<div class="body"><h3>{e(t)}</h3><p>{e(d)}</p><small>{UI[lang]["promo_tcs"]}</small>'
            f'{link("@register", UI[lang]["claim"], lang, "btn btn-fill")}</div></div>')


# ---------------------------------------------------------------- site pages
def page_view(p, lang):
    d, u = p[lang], UI[lang]
    key = p["key"]
    path = url(key, lang)
    items = [(u["home"], url("home", lang))] + ([(label(p["parent"], lang), url(p["parent"], lang))] if p["parent"] else []) + [(d["nav"], path)]
    secs = "".join(f"<h2>{e(h)}</h2>{blocks_html(bl, lang)}" for h, bl in d.get("sections", []))
    extra = ""
    if p["type"] == "hub":
        kids = [c for c in PAGES if c.get("parent") == key] + [PAGE[k] for k in ("live", "sports", "esports") if k in PAGE]
        extra = '<div class="game-grid">' + "".join(
            f'<a class="game-card" href="{url(c["key"], lang)}">{square("categories/" + c["key"], c[lang]["nav"], c["icon"])}<h3>{e(c[lang]["nav"])}</h3><p>{e(c[lang]["card"])}</p></a>'
            for c in kids) + "</div>"
    elif p["type"] == "game":
        extra = (f'<section class="block"><div class="head"><h2>{u["steps_h"]}</h2></div><div class="steps">'
                 + "".join(f'<div class="step"><span class="ic">{i}</span><h3>{t}</h3><p>{dd}</p></div>' for i, t, dd in u["steps"]) + "</div></section>")
    elif p["type"] == "promos":
        extra = '<div class="promos">' + "".join(promo_card(pr, lang) for pr in PROMOS) + "</div>"
    elif p["type"] == "glossary":
        extra = '<dl class="glossary">' + "".join(
            f'<div id="{k}"><dt>{e(ENTITIES[k][0 if lang == "ms" else 1])}</dt><dd>{e(dm if lang == "ms" else de)} '
            f'<a href="{ENTITIES[k][2]}" target="_blank" rel="noopener">{"Rujukan" if lang == "ms" else "Reference"} ↗</a></dd></div>'
            for k, dm, de in p["terms"]) + "</dl>"
    related = cluster_box(p["cluster"], lang) if p.get("cluster") else ""
    with_hero = p["type"] not in ("policy", "glossary")
    if with_hero:
        top = f"""<section class="hero-band page-hero">{banner(lang, True)}{crumbs(items)}
<div class="wrap hero-grid"><div><h1>{tok(d['h1'], lang)}</h1><p class="lead">{linkify(tok(d['intro'], lang), lang)}</p>
<div class="cta-row">{link('@register', u['float_register'], lang, 'btn btn-glow')}{link('@login', u['login'], lang, 'btn btn-ghost')}</div></div>
<div class="hero-art">{square("categories/" + key, d['nav'], p['icon'], lazy=False)}</div></div></section>"""
    else:
        top = f'{crumbs(items)}<div class="wrap page-head"><h1>{tok(d["h1"], lang)}</h1><p class="lead">{linkify(tok(d["intro"], lang), lang)}</p></div>'
    main = f"""{top}
<div class="wrap"><article class="prose">{secs}</article>{extra}{related}{faq_html(d.get('faq'), lang, u['faq_h'])}</div>
{cta_band(lang)}"""
    wp = {"@type": "CollectionPage" if p["type"] in ("hub", "glossary") else "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path,
          "name": tok(d["title"], lang), "description": tok(d["desc"], lang), "inLanguage": u["hreflang"], "isPartOf": {"@id": SITE + "/#website"},
          "publisher": {"@id": SITE + "/#org"}, "breadcrumb": {"@id": SITE + path + "#crumbs"}, "dateModified": UPDATED, **about_mentions(p.get("about"), lang)}
    nodes = [org(), wp]
    if p["type"] == "hub":
        kids_l = [c for c in PAGES if c.get("parent") == key] + [PAGE[k] for k in ("live", "sports", "esports") if k in PAGE]
        nodes.append(item_list(SITE + path + "#list", [(tok(c[lang]["nav"], lang), url(c["key"], lang)) for c in kids_l]))
        wp["mainEntity"] = {"@id": SITE + path + "#list"}
    if p["type"] == "glossary":
        tid = SITE + path + "#terms"
        nodes.append({"@type": "DefinedTermSet", "@id": tid, "name": tok(d["h1"], lang), "inLanguage": u["hreflang"], "publisher": {"@id": SITE + "/#org"},
                      "hasDefinedTerm": [{"@type": "DefinedTerm", "@id": SITE + path + "#" + k, "name": ENTITIES[k][0 if lang == "ms" else 1],
                                          "description": dm if lang == "ms" else de, "sameAs": ENTITIES[k][2], "inDefinedTermSet": {"@id": tid}}
                                         for k, dm, de in p["terms"]]})
        wp["mainEntity"] = {"@id": tid}
    if key == "app":
        nodes.append({"@type": "SoftwareApplication", "@id": SITE + path + "#app", "name": f"{BRAND} App", "operatingSystem": "Android, iOS",
                      "applicationCategory": "GameApplication", "inLanguage": [UI[l]["hreflang"] for l in LANGS], "url": SITE + path,
                      "offers": {"@type": "Offer", "price": "0", "priceCurrency": "MYR"}, "publisher": {"@id": SITE + "/#org"},
                      "author": {"@id": SITE + "/#org"}})
        wp["mainEntity"] = {"@id": SITE + path + "#app"}
    cr = crumbs_schema(items)
    cr["@id"] = SITE + path + "#crumbs"
    nodes += [faq_schema(d.get("faq"), lang), cr]
    return page(lang, key, d, path, main, graph(*nodes), kw=d["kw"] + [BRAND])


# ---------------------------------------------------------------- blog
def blog_index(lang):
    u = UI[lang]
    path = url("blog", lang)
    items = [(u["home"], url("home", lang)), (u["blog"], path)]
    d = {"title": f"Blog {BRAND} Malaysia: Panduan Daftar, Bonus & Slot" if lang == "ms" else f"{BRAND} Malaysia Blog: Register, Bonus & Slot Guides",
         "desc": (f"Blog {BRAND} Malaysia: panduan mengikut topik untuk daftar, login, deposit, bonus, slot, kasino langsung dan sukan. Mula dengan panduan utama."
                  if lang == "ms" else f"{BRAND} Malaysia blog: guides by topic for registering, login, deposits, bonuses, slots, live casino and sports. Start with a main guide."),
         "focus": f"Blog {BRAND}" if lang == "ms" else f"{BRAND} Malaysia Blog",
         "h1": f"Blog {BRAND}: Panduan Mengikut Topik" if lang == "ms" else f"{BRAND} Malaysia Blog: Guides by Topic",
         "intro": (f"Blog {BRAND} menyusun panduan mengikut topik. Mulakan dengan panduan utama setiap topik, kemudian baca panduan berkaitan."
                   if lang == "ms" else f"The {BRAND} Malaysia Blog groups guides by topic. Start with each topic's main guide, then read the related guides.")}
    groups = "".join(f'<h2 class="section-label">{e(c["name"][lang])}</h2><div class="post-grid">' + "".join(post_card(p, lang) for p in cluster_posts(k)) + "</div>"
                     for k, c in CLUSTERS.items())
    main = f'{crumbs(items)}<div class="wrap page-head"><h1>{d["h1"]}</h1><p class="lead">{d["intro"]}</p></div><div class="wrap">{groups}</div>{cta_band(lang)}'
    coll = {"@type": "CollectionPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": d["title"], "inLanguage": u["hreflang"],
            "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + url(p["key"], lang)}
                                                                    for i, p in enumerate(q for k in CLUSTERS for q in cluster_posts(k))]}}
    return page(lang, "blog", d, path, main, graph(org(), coll, crumbs_schema(items)), kw=KEYWORDS[lang])


def post_view(p, lang):
    d, u = p[lang], UI[lang]
    key, k = p["key"], p["cluster"]
    path = url(key, lang)
    pillar = POST[CLUSTERS[k]["pillar"]]
    items = [(u["home"], url("home", lang)), (u["blog"], url("blog", lang))] + ([] if p is pillar else [(CLUSTERS[k]["name"][lang], url(pillar["key"], lang))]) + [(d["card"], path)]
    up = "" if p is pillar else f'<p class="pillar-note">{u["pillar_note"]}: <a href="{url(pillar["key"], lang)}">{e(pillar[lang]["title"])}</a></p>'
    secs = "".join(f"<h2>{e(h)}</h2>{blocks_html(bl, lang)}" for h, bl in d["sections"])
    others = "".join(f'<li><a href="{url(c["pillar"], lang)}">{e(c["name"][lang])}</a></li>' for ck, c in CLUSTERS.items() if ck != k)
    cats = "".join(f'<li><a href="{url(g["key"], lang)}">{e(g[lang]["nav"])}</a></li>' for g in PAGES if g["type"] in ("hub", "game"))
    pic = f'<div class="post-img">{img("posts/" + key, d["title"], lazy=False)}</div>' if has_img("posts/" + key) else ""
    main = f"""{crumbs(items)}
<div class="wrap page-head"><span class="cat">{e(CLUSTERS[k]['name'][lang])}</span><h1>{tok(d['h1'], lang)}</h1>
<p class="byline">{tok(u['by'], lang)} · <time datetime="{PUBLISHED}">{u['published']} {PUBLISHED}</time></p></div>
<div class="wrap article"><article class="prose">{pic}{up}{blocks_html([d['intro']], lang)}{secs}{cluster_box(k, lang, p)}
{faq_html(d.get('faq'), lang, u['faq_h'])}<div class="note">{u['rg_note']}</div></article>
<aside class="aside"><div class="widget cta-widget"><h2>{u['cta_h']}</h2><p>{tok(u['cta_p'], lang)}</p>{link('@register', u['float_register'], lang, 'btn btn-white')}</div>
<div class="widget"><h2>{u['other_topics']}</h2><ul>{others}</ul></div><div class="widget"><h2>{u['games_h']}</h2><ul>{cats}</ul></div></aside></div>"""
    art = {"@type": "BlogPosting", "@id": SITE + path + "#article", "headline": tok(d["title"], lang), "description": tok(d["desc"], lang),
           "url": SITE + path, "mainEntityOfPage": SITE + path, "inLanguage": u["hreflang"], "keywords": ", ".join(d["kw"]),
           "articleSection": CLUSTERS[k]["name"][lang], "datePublished": PUBLISHED, "dateModified": UPDATED,
           "image": SITE + (f"/images/posts/{key}.webp" if has_img("posts/" + key) else "/images/og.jpg"),
           "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, **about_mentions(p.get("about"), lang)}
    if p is not pillar:
        art["isPartOf"] = {"@id": SITE + url(pillar["key"], lang) + "#article"}
    return page(lang, key, d, path, main, graph(org(), art, faq_schema(d.get("faq"), lang), crumbs_schema(items)), og_type="article",
                kw=d["kw"] + pillar[lang]["kw"][:1] + [BRAND])


# ---------------------------------------------------------------- contents + 404
def all_keys():
    return ["home"] + [p["key"] for p in PAGES] + ["blog"] + [p["key"] for k in CLUSTERS for p in cluster_posts(k)] + ["contents"]


def page_title(key, lang):
    if key == "home":
        return HOME[lang]["title"]
    if key in PAGE:
        return PAGE[key][lang]["title"]
    if key in POST:
        return POST[key][lang]["title"]
    return label(key, lang)


def contents_view(lang):
    u = UI[lang]
    path = url("contents", lang)
    items = [(u["home"], url("home", lang)), (u["contents"], path)]
    groups = [(u["main_pages"], ["home"] + [p["key"] for p in PAGES] + ["blog"])] + [(c["name"][lang], [p["key"] for p in cluster_posts(k)]) for k, c in CLUSTERS.items()]
    secs = "".join(f"<h2>{e(g)}</h2><ul>" + "".join(f'<li><a href="{url(k, lang)}">{e(tok(page_title(k, lang), lang))}</a></li>' for k in keys) + "</ul>" for g, keys in groups)
    d = {"title": f"{u['contents']} {BRAND} Malaysia | Semua Halaman" if lang == "ms" else f"{BRAND} Malaysia {u['contents']} | All Pages",
         "desc": tok(u["contents_p"], lang) + (" Cari panduan dengan pantas." if lang == "ms" else " Find any guide or game category fast."),
         "focus": u["contents"], "h1": f"{u['contents']} {BRAND} Malaysia" if lang == "ms" else f"{BRAND} Malaysia {u['contents']}", "intro": tok(u["contents_p"], lang)}
    main = f'{crumbs(items)}<div class="wrap page-head"><h1>{d["h1"]}</h1><p class="lead">{d["intro"]}</p></div><div class="wrap"><div class="prose">{secs}</div></div>'
    return page(lang, "contents", d, path, main, graph(org(), crumbs_schema(items)), kw=KEYWORDS[lang])


def not_found():
    u = UI[MAIN]
    d = {"title": f"{u['nf_title']} | {BRAND}", "desc": u["nf_p"], "focus": "", "h1": u["nf_title"], "intro": u["nf_p"]}
    main = f'<div class="wrap page-head"><h1>{u["nf_title"]}</h1><p class="lead">{u["nf_p"]}</p><p>{link("home", u["home"], MAIN, "btn btn-fill")}</p></div><div class="wrap">{guides_section(MAIN)}</div>'
    out = page(MAIN, "home", d, "/404", main, "")
    WARN[:] = [w for w in WARN if "/404" not in w]
    return out.replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex">')


# ---------------------------------------------------------------- output
def write(path, content):
    path = tok(path)
    full = os.path.join(DIST, path.lstrip("/"))
    if full.endswith("/"):
        full += "index.html"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    content = tok(content, "en" if path.startswith("/en/") else MAIN)
    if full.endswith(".html") and path != "/404.html" and content.count("<h1") != 1:
        WARN.append(f"h1 {path}: {content.count('<h1')} H1 tags (must be exactly 1)")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def sitemap():
    rows = ""
    for k in all_keys():
        for l in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{UI[x]["hreflang"]}" href="{SITE}{url(k, x)}"/>' for x in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{url(k, MAIN)}"/>'
            rows += f"<url><loc>{SITE}{url(k, l)}</loc><lastmod>{UPDATED}</lastmod>{alts}</url>"
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{rows}</urlset>\n')


def copy_static():
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"), ignore=shutil.ignore_patterns("style.css", ".DS_Store"))
    shutil.copytree(IMG, os.path.join(DIST, "images"), ignore=shutil.ignore_patterns("src", "sizes.json", ".DS_Store"))
    for f in os.listdir(ROOT):
        if f in ("_headers", "favicon.ico", "favicon.svg", "site.webmanifest") or re.fullmatch(r"(favicon-\d+|apple-touch-icon)\.png|[0-9a-f]{32}\.txt", f):
            shutil.copy(os.path.join(ROOT, f), DIST)


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    audit()
    n = 0
    for lang in LANGS:
        write(url("home", lang), home(lang))
        for p in PAGES:
            write(url(p["key"], lang), page_view(p, lang))
        write(url("blog", lang), blog_index(lang))
        for p in POSTS:
            write(url(p["key"], lang), post_view(p, lang))
        write(url("contents", lang), contents_view(lang))
        n += 3 + len(PAGES) + len(POSTS)
    write("/404.html", not_found())
    write("/sitemap.xml", sitemap())
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("/llms.txt", f"# {BRAND} Malaysia\n\n> {TAGLINE['en']}. Default language Bahasa Melayu, English at /en/. 18+.\n\n"
          + "\n".join(f"- [{tok(page_title(k, l), l)}]({SITE}{url(k, l)})" for l in LANGS for k in all_keys()) + "\n")
    copy_static()
    left = {t for root, _, fs in os.walk(DIST) for f in fs if f.endswith((".html", ".xml", ".txt"))
            for t in re.findall(r"__[A-Z_]+__", open(os.path.join(root, f), encoding="utf-8").read())}
    if left:
        sys.exit(f"unreplaced tokens: {left}")
    for w in WARN:
        print("  " + w)
    print(f"built {n} pages ({len(LANGS)} languages) in dist/" + ("" if SIZES else "  (no images yet; run build/images.py)"))


if __name__ == "__main__":
    main()
