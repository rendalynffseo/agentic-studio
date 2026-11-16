"""Static site generator (iGaming_Templates_9_FreeCredit).

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
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [n for n in nodes if n]}, ensure_ascii=False) + "</script>"


def org():
    return {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": SITE + "/images/logo-512.png", "width": 512, "height": 512}}


def website():
    return {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": f"{BRAND} Malaysia",
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": [UI[l]["hreflang"] for l in LANGS]}


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
    return f'<a class="logo" href="{url("home", lang)}" aria-label="{e(BRAND)}">{inner}</a>'


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
    return f"""<footer class="site-footer"><div class="wrap">
<div class="foot-grid"><div class="foot-about">{logo(lang)}<p>{tok(u['foot_about'], lang)}</p><div class="pills">{pays}</div></div>{cols}{guides}</div>
<div class="foot-bottom">{social()}<span class="r18">18+</span><span>{u['foot_rg']}</span><span>© {UPDATED[:4]} {e(BRAND)} Malaysia</span><span>{langs}</span></div>
<p class="foot-disc">{u['foot_disc']}</p>
</div></footer>"""


def social():
    links = [(u, n) for u, n in ((TELEGRAM_URL, "Telegram"), (FACEBOOK_URL, "Facebook"), (LIVECHAT_URL, "Live Chat")) if u]
    return "".join(f'<a class="soc" href="{u}" target="_blank" rel="nofollow noopener">{n}</a>' for u, n in links)


def float_bar(lang):
    u = UI[lang]
    return (f'<div class="float-cta" role="navigation" aria-label="{u["login"]} / {u["register"]}">'
            f'{link("@login", u["login"], lang, "btn btn-login")}{link("@register", u["float_register"], lang, "btn btn-reg")}</div>')


def popup(lang):
    """Phone-size (9:16) popup: opens after load, then again 30 s after every close (assets/main.js)."""
    u = UI[lang]
    inner = img("popup", u["popup_alt"]) if has_img("popup") else (
        f'<div class="popup-card"><span class="logo">{"".join(f"<span class={c}>{e(t)}</span>" for t, c in LOGO_PARTS)}</span>'
        f'<b>{u["popup_title"]}</b><p>{u["popup_text"]}</p><span class="btn btn-reg">{u["float_register"]}</span></div>')
    return (f'<div class="popup" id="promo-popup" role="dialog" aria-modal="true" aria-label="{e(u["popup_title"])}"><div class="popup-inner">'
            f'<button class="popup-close" type="button" aria-label="{u["close"]}">&times;</button>'
            f'<a href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">{inner}</a></div></div>')


def banner(lang, eager):
    """Header band: 900x500 promo banner + the reference's two wide LOGIN / REGISTER buttons."""
    u = UI[lang]
    if has_img("banner"):
        inner = img("banner", u["banner_alt"], lazy=not eager)
    else:
        inner = (f'<div class="banner-card"><span class="logo">{"".join(f"<span class={c}>{e(t)}</span>" for t, c in LOGO_PARTS)}</span>'
                 f'<b>{u["banner_title"]}</b><p>{u["banner_sub"]}</p><span class="btn btn-reg">{u["float_register"]}</span></div>')
    return (f'<div class="band-top"><div class="wrap"><a class="banner" href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">{inner}</a>'
            f'<div class="duo">{link("@login", u["login"], lang, "btn btn-login")}{link("@register", u["register"], lang, "btn btn-reg")}</div></div></div>')


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
<meta name="theme-color" content="{THEME.get('dark', '#313131')}">
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
<link rel="preload" href="/assets/fonts/lato-900.woff2" as="font" type="font/woff2" crossorigin>
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


def cta_band(lang):
    u = UI[lang]
    return (f'<section class="band"><div class="wrap"><h2>{u["cta_h"]}</h2><p>{tok(u["cta_p"], lang)}</p>'
            f'<div class="cta-row">{link("@register", u["float_register"], lang, "btn btn-white")}{link("@login", u["login"], lang, "btn btn-ghost-w")}</div></div></section>')


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
            f'<div class="guides">{cards}</div><p class="center">{link("blog", u["all_guides"], lang, "btn btn-login")}</p></section>')


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
def tiles(pages, lang, key_img=None):
    """Square image tiles linking to pages (game categories or provider free-credit guides)."""
    out = ""
    for p in pages:
        name = key_img(p) if key_img else "categories/" + p["key"]
        out += f'<a class="tile" href="{url(p["key"], lang)}">{square(name, p[lang]["nav"], p["icon"])}<span>{e(p[lang]["nav"])}</span></a>'
    return out


def prov_img(p):
    return "providers/" + p["img"]


def fc_table(lang):
    u = UI[lang]
    return ('<div class="tbl-wrap"><table class="tbl"><thead><tr>' + "".join(f"<th>{c}</th>" for c in u["fc_head"]) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{tok(c, lang)}</td>" for c in r) + "</tr>" for r in FREE_CREDITS[lang]) + "</tbody></table></div>")


def home(lang):
    h, u = HOME[lang], UI[lang]
    path = url("home", lang)
    games = [p for p in PAGES if p["type"] == "game"]
    fcs = [p for p in PAGES if p["type"] == "freecredit"]
    overview = ('<div class="tbl-wrap"><table class="tbl"><thead><tr>' + f'<th>{u["table_item"]}</th><th>{u["table_detail"]}</th></tr></thead><tbody>'
                + "".join(f"<tr><td>{a}</td><td>{tok(b, lang)}</td></tr>" for a, b in OVERVIEW[lang]) + "</tbody></table></div>")
    fc = h["fc"]
    game_secs = "".join(f'<h3>{e(p[lang]["nav"])}</h3><p>{e(p[lang]["card"])} {link(p["key"], p[lang]["nav"] + " →", lang)}</p>' for p in games)
    prov_rows = "".join(f'<tr><td>{e(p[lang]["nav"].replace("Kredit Percuma ", "").replace(" Free Credit", ""))}</td><td>{link(p["key"], p[lang]["nav"], lang)}</td></tr>' for p in fcs)
    prov_table = (f'<div class="tbl-wrap"><table class="tbl"><thead><tr><th>{u["prov_head"][0]}</th><th>{u["prov_head"][1]}</th></tr></thead><tbody>{prov_rows}</tbody></table></div>')
    pays = "".join(f"<span>{e(x)}</span>" for x in PAYMENTS)
    feats = "".join(f'<div class="feature"><span class="ic">{i}</span><h3>{t}</h3><p>{linkify(d, lang)}</p></div>' for i, t, d in h["features"]["items"])
    explore = "".join(f'<li>{link(p["key"], p[lang]["nav"], lang)}</li>' for p in PAGES)
    latest = "".join(post_card(POST[c["pillar"]], lang) for c in CLUSTERS.values())
    main = f"""{banner(lang, True)}
<div class="wrap">
<section class="promo-grid">{''.join(promo_card(pr, lang) for pr in PROMOS)}</section>
<section class="tile-block"><h2 class="strip-h">{u['tiles_h']}</h2><div class="tiles">{tiles(games, lang)}</div></section>
<section class="tile-block"><h2 class="strip-h">{u['fc_tiles_h']}</h2><div class="tiles prov">{tiles(fcs, lang, prov_img)}</div></section>
{custom_sections.per_lang(custom_sections.AFTER_HERO, lang)}
<article class="longform">
<h1>{tok(h['h1'], lang)}</h1>
<p class="lead">{tok(h['intro'], lang)}</p>
<h2>{tok(h['what'][0], lang)}</h2><p>{linkify(tok(h['what'][1], lang), lang)}</p>
<h2>{tok(h['overview_h'], lang)}</h2>{overview}
<h2 id="free-credit">{tok(fc['h2'], lang)}</h2><p>{fc['p']}</p>{fc_table(lang)}<p class="small">{linkify(fc['note'], lang)}</p>
<h3>{fc['how_h']}</h3><ul>{''.join(f'<li>{x}</li>' for x in fc['how'])}</ul>
<h2 id="games">{tok(h['games']['h2'], lang)}</h2><p>{h['games']['p']}</p>{game_secs}
<h2>{h['prov']['h2']}</h2><p>{h['prov']['p']}</p>{prov_table}
<h2>{h['pay']['h2']}</h2><p>{linkify(h['pay']['p'], lang)}</p><div class="pills light">{pays}</div>
<h2 id="start">{tok(h['join_h'], lang)}</h2>
<div class="steps">{''.join(f'<div class="step"><span class="ic">{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in u['steps'])}</div>
<p class="center">{link('@register', u['float_register'], lang, 'btn btn-reg')}</p>
<h2>{tok(h['features']['h2'], lang)}</h2><div class="features">{feats}</div>
</article>
{guides_section(lang)}
{custom_sections.per_lang(custom_sections.BEFORE_FAQ, lang)}
{faq_html(h['faq'], lang, tok(h['faq_h2'], lang)).replace('<section class="block faq">', '<section class="block faq" id="faq">')}
<section class="longform"><h2>{h['rg'][0]}</h2><p>{linkify(h['rg'][1], lang)}</p>
<h2>{tok(u['explore_h'], lang)}</h2><ul class="explore">{explore}</ul></section>
<section class="block"><div class="head"><h2>{u['latest_h']}</h2></div><div class="post-grid">{latest}</div></section>
</div>
{cta_band(lang)}"""
    wp = {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": tok(h["title"], lang), "isPartOf": {"@id": SITE + "/#website"},
          "about": {"@id": SITE + "/#org"}, "inLanguage": u["hreflang"], "datePublished": PUBLISHED, "dateModified": UPDATED}
    head = '<link rel="preload" as="image" href="/images/banner.webp" fetchpriority="high">' if has_img("banner") else ""
    return page(lang, "home", h, path, main, graph(org(), website(), wp, faq_schema(h["faq"], lang), crumbs_schema([(u["home"], path)])),
                kw=h["kw"] + KEYWORDS[lang], extra_head=head)


def promo_card(pr, lang):
    key, im, txt = pr
    t, d = txt[lang]
    pic = square("promos/" + im, t, "🎁") if im else '<div class="sq-fallback">🎁</div>'
    return (f'<div class="promo">{pic}<div class="body"><h3>{e(t)}</h3><p>{e(d)}</p><small>{UI[lang]["promo_tcs"]}</small>'
            f'{link("@register", UI[lang]["claim"], lang, "btn btn-reg")}</div></div>')


# ---------------------------------------------------------------- site pages
def page_view(p, lang):
    d, u = p[lang], UI[lang]
    key = p["key"]
    path = url(key, lang)
    items = [(u["home"], url("home", lang))] + ([(label(p["parent"], lang), url(p["parent"], lang))] if p["parent"] else []) + [(d["nav"], path)]
    secs = "".join(f"<h2>{e(h)}</h2>{blocks_html(bl, lang)}" for h, bl in d.get("sections", []))
    extra = ""
    if p["type"] == "game":
        extra = (f'<section class="block"><div class="head"><h2>{u["steps_h"]}</h2></div><div class="steps">'
                 + "".join(f'<div class="step"><span class="ic">{i}</span><h3>{t}</h3><p>{dd}</p></div>' for i, t, dd in u["steps"]) + "</div></section>")
    elif p["type"] == "fchub":
        fcs = [c for c in PAGES if c["type"] == "freecredit"]
        extra = f'{fc_table(lang)}<h2 class="strip-h">{u["fc_tiles_h"]}</h2><div class="tiles prov">{tiles(fcs, lang, prov_img)}</div>'
    elif p["type"] == "freecredit":
        extra = f'<h2 class="strip-h">{u["fc_rule_h"]}</h2>{fc_table(lang)}'
    elif p["type"] == "promos":
        extra = '<div class="promo-grid">' + "".join(promo_card(pr, lang) for pr in PROMOS) + "</div>"
    related = cluster_box(p["cluster"], lang) if p.get("cluster") else ""
    art = ("providers/" + p["img"]) if p["type"] == "freecredit" else ("categories/" + key)
    if p["type"] != "policy":
        top = f"""{banner(lang, True)}{crumbs(items)}
<section class="page-hero"><div class="wrap hero-grid"><div><h1>{tok(d['h1'], lang)}</h1><p class="lead">{linkify(tok(d['intro'], lang), lang)}</p>
<div class="cta-row">{link('@register', u['float_register'], lang, 'btn btn-reg')}{link('@login', u['login'], lang, 'btn btn-login')}</div></div>
<div class="hero-art">{square(art, d['nav'], p['icon'], lazy=False)}</div></div></section>"""
    else:
        top = f'{crumbs(items)}<div class="wrap page-head"><h1>{tok(d["h1"], lang)}</h1><p class="lead">{linkify(tok(d["intro"], lang), lang)}</p></div>'
    main = f"""{top}
<div class="wrap"><article class="prose">{secs}</article>{extra}{related}{faq_html(d.get('faq'), lang, u['faq_h'])}</div>
{cta_band(lang)}"""
    wp = {"@type": "CollectionPage" if p["type"] == "fchub" else "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": tok(d["title"], lang),
          "description": tok(d["desc"], lang), "inLanguage": u["hreflang"], "isPartOf": {"@id": SITE + "/#website"}, "dateModified": UPDATED}
    return page(lang, key, d, path, main, graph(org(), wp, faq_schema(d.get("faq"), lang), crumbs_schema(items)), kw=d["kw"] + [BRAND])


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
    cats = "".join(f'<li><a href="{url(g["key"], lang)}">{e(g[lang]["nav"])}</a></li>' for g in PAGES if g["type"] in ("game", "fchub"))
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
           "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}}
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
    main = f'<div class="wrap page-head"><h1>{u["nf_title"]}</h1><p class="lead">{u["nf_p"]}</p><p>{link("home", u["home"], MAIN, "btn btn-reg")}</p></div><div class="wrap">{guides_section(MAIN)}</div>'
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
