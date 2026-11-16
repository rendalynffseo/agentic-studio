"""Static site generator (iGaming_Templates_3_CasinoLobby).

Run:  python3 build/build.py      -> writes the whole site to dist/ (wiped first)
Per-site settings: site_config.py. Text: content.py (home + UI), pages.py (blog hub, policies), posts.py.
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
from pages import BLOG_HUB, POLICIES  # noqa: E402
from posts import POSTS, CLUSTERS  # noqa: E402
import custom_sections  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
IMG = os.path.join(ROOT, "images")
BY_SLUG = {p["slug"]: p for p in POSTS}
ROWS = ["slots", "live", "instant", "fishing"]
MAIN_LANG = LANGS[0]
EXTERNAL = {"@register": REGISTER_URL, "@login": LOGIN_URL, "@app": APP_URL, "@chat": LIVECHAT_URL or REGISTER_URL}
TOKENS = {"__BRAND__": BRAND, "__SLUG__": SLUG, "__TAGLINE__": TAGLINE, "__SITE_URL__": SITE,
          "__EMAIL_LINE__": f'Email: <a href="mailto:{EMAIL}">{EMAIL}</a>' if EMAIL else "Use the live support link at the bottom of any page."}
SIZES = json.load(open(os.path.join(IMG, "sizes.json"))) if os.path.exists(os.path.join(IMG, "sizes.json")) else {}
e = html.escape

with open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8") as _f:
    CSS = " ".join(_f.read().split())
CSS += ":root{" + "".join(f"--{k}:{v};" for k, v in THEME.items()) + "}" + " ".join(custom_sections.EXTRA_CSS.split())
JS_VER = hashlib.md5(open(os.path.join(ROOT, "assets", "main.js"), "rb").read()).hexdigest()[:8]


def per_lang(value, lang):
    return value.get(lang, "") if isinstance(value, dict) else value


def has_img(name):
    return name in SIZES


def img(name, alt, cls="", lazy=True):
    w, h = SIZES[name]
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<img src="/images/{name}.webp" alt="{e(alt)}" width="{w}" height="{h}" {load}{cls_attr}>'


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def ui_lang(lang):
    return lang if lang in UI else MAIN_LANG


def home_path(lang):
    return "/" if lang == MAIN_LANG or lang not in LANGS else f"/{lang}/"


def a(target, label, lang, on_home=False, cls=""):
    """Link helper: '@register' etc -> sponsored external link; '#id' -> home section; else internal path."""
    c = f' class="{cls}"' if cls else ""
    if target in EXTERNAL:
        return f'<a{c} href="{EXTERNAL[target]}" target="_blank" rel="nofollow sponsored noopener">{label}</a>'
    if target.startswith("#") and not on_home:
        target = home_path(lang) + target
    return f'<a{c} href="{target}">{label}</a>'


# ---------------------------------------------------------------- internal links in posts
LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")


def link_href(target, lang):
    if target == "home":
        return home_path(lang)
    if target.startswith("home#"):
        return home_path(lang) + "#" + target[5:]
    if target == "blog":
        return "/blog/"
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
        {"@context": "https://schema.org", "@graph": [n for n in nodes if n]}, ensure_ascii=False) + "</script>"


def org():
    return {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": SITE + "/images/logo-512.png", "width": 512, "height": 512},
            "description": TAGLINE}


def website():
    return {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": f"{BRAND} Malaysia",
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": [UI[l]["hreflang"] for l in LANGS]}


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": strip_tags(n), "item": SITE + u} for i, (n, u) in enumerate(items)]}


# ---------------------------------------------------------------- page shell
def analytics():
    if not GA4_ID:
        return ""
    return f"""<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA4_ID}");
(function(){{var l=false,e=["scroll","mousemove","touchstart","keydown","click"];function load(){{if(l)return;l=true;e.forEach(function(x){{window.removeEventListener(x,load,{{passive:true}});}});
var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}";document.head.appendChild(s);}}
e.forEach(function(x){{window.addEventListener(x,load,{{passive:true}});}});window.addEventListener("load",function(){{setTimeout(load,3500);}});}})();</script>"""


def logo():
    return f'<a class="logo" href="/">{img("logo", BRAND, lazy=False) if has_img("logo") else e(LOGO_TEXT)}</a>'


def sidebar(lang, on_home):
    u = UI[ui_lang(lang)]
    tabs = a("#slots", u["casino"], lang, on_home, "on") + a("@register", u["sports"], lang, on_home)
    groups = "".join('<nav class="side-group">' + "".join(
        a(t, f'<span class="ico">{i}</span>{lbl}' + (f'<span class="tag">{tag}</span>' if tag else ""), lang, on_home)
        for i, lbl, t, tag in g) + "</nav>" for g in u["side"])
    langs = "".join(f'<a href="{home_path(l)}" hreflang="{UI[l]["hreflang"]}"' + (' aria-current="true"' if l == lang else "")
                    + f'>{UI[l]["label"]}</a>' for l in LANGS) if len(LANGS) > 1 else ""
    return f"""<aside class="sidebar" id="sidebar" aria-label="Main menu">
<div class="side-top">{logo()}<button class="side-close" aria-label="{u['close']}">✕</button></div>
<div class="side-tabs">{tabs}</div>{groups}
{f'<div class="side-group side-lang" aria-label="Language">{langs}</div>' if langs else ''}
</aside><div class="scrim"></div>"""


def footer(lang, on_home):
    u = UI[ui_lang(lang)]
    cols = "".join(f'<div><h2>{t}</h2><ul>' + "".join(f"<li>{a(h, l, lang, on_home)}</li>" for l, h in links) + "</ul></div>"
                   for t, links in u["foot_cols"])
    cols += f'<div><h2>{u["foot_guides"]}</h2><ul>' + "".join(
        f'<li><a href="/blog/{CLUSTERS[k]["pillar"]}/">{e(cname(k, lang))}</a></li>' for k in CLUSTERS) + "</ul></div>"
    return f"""<footer class="site-footer"><div class="wrap">
<div class="foot-grid"><div class="foot-about">{logo()}<p>{u['foot_about']}</p></div>{cols}</div>
<div class="foot-legal"><span class="r18">18+</span><span>{u['foot_rg']}</span><span>© {UPDATED[:4]} {e(BRAND)} Malaysia</span></div>
<p class="foot-disc">{u['foot_disc']}</p>
</div></footer>"""


def tabbar(lang, on_home):
    u = UI[ui_lang(lang)]
    out = []
    for i, (ico, lbl, t) in enumerate(u["tabs"]):
        inner = f'<span class="i">{ico}</span>{lbl}'
        if t == "nav":
            out.append(f'<button data-nav aria-controls="sidebar" aria-expanded="false">{inner}</button>')
        else:
            out.append(a(t, inner, lang, on_home, "reg" if i == len(u["tabs"]) - 1 else ""))
    return '<nav class="tabbar" aria-label="Quick menu">' + "".join(out) + "</nav>"


def page(lang, title, desc, path, main, schema, on_home=False, og_type="website", alternates=None, extra_head="", keywords=None):
    u = UI[ui_lang(lang)]
    check_meta(path, title, desc)
    kw = ", ".join(dict.fromkeys(keywords or KEYWORDS.get(ui_lang(lang)) or KEYWORDS[MAIN_LANG]))
    url = SITE + path
    alternates = alternates or {lang: path}
    alt = "".join(f'<link rel="alternate" hreflang="{UI[l]["hreflang"]}" href="{SITE}{p}">' for l, p in alternates.items())
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alternates.get(MAIN_LANG, path)}">'
    verify = (f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">' if GSC_VERIFICATION else "") + \
             (f'<meta name="msvalidate.01" content="{BING_VERIFICATION}">' if BING_VERIFICATION else "")
    chat = f'<a class="chat" href="{LIVECHAT_URL}" target="_blank" rel="nofollow sponsored noopener" aria-label="{u["chat"]}">💬</a>' if LIVECHAT_URL else ""
    return f"""<!doctype html>
<html lang="{u['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{verify}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(kw)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="{THEME.get('side', '#0f212e')}">
<link rel="canonical" href="{url}">
{alt}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(BRAND)} Malaysia">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{u['og_locale']}">
<meta property="og:image" content="{SITE}/images/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{extra_head}
<style>{CSS}</style>
{analytics()}
{schema}
</head>
<body>
<a class="skip" href="#main">{u['skip']}</a>
{sidebar(lang, on_home)}
<div class="shell">
<header class="topbar"><div class="wrap">
<button class="menu-btn" data-nav aria-controls="sidebar" aria-expanded="false" aria-label="{u['menu']}">☰</button>{logo()}
<div class="top-right">{a('@login', u['login'], lang, on_home, 'btn btn-ghost')}{a('@register', u['register'], lang, on_home, 'btn btn-blue')}</div>
</div></header>
<main id="main">{main}</main>
{footer(lang, on_home)}
</div>
{tabbar(lang, on_home)}{float_bar(lang)}{chat}
{popup(lang)}
<script src="/assets/main.js?v={JS_VER}" defer></script>
{EXTRA_BODY_END}
</body>
</html>"""


# ---------------------------------------------------------------- SEO helpers, popup, floating footer
META_WARN = []


def check_meta(path, title, desc):
    """SEO length warnings (after tokens): title <= 65 chars, description 70-165 (Chinese: 40 / 35-100)."""
    if path == "/404":
        return
    t, d = replace_tokens(title), replace_tokens(desc)
    cjk = re.search(r"[\u4e00-\u9fff]", t + d)
    tmax, dmin, dmax = (40, 35, 100) if cjk else (65, 70, 165)
    if len(t) > tmax:
        META_WARN.append(f"{path}: title {len(t)} chars")
    if not dmin <= len(d) <= dmax:
        META_WARN.append(f"{path}: description {len(d)} chars")


def float_bar(lang):
    """Floating footer (desktop): Login + Register. On mobile the tab bar carries both instead."""
    u = UI[ui_lang(lang)]
    return (f'<div class="float-cta" role="navigation" aria-label="{u["login"]} / {u["register"]}">'
            f'{a("@login", u["login"], lang, cls="btn btn-dark")}{a("@register", u["float_register"], lang, cls="btn btn-blue")}</div>')


def popup(lang):
    """Phone-size (9:16) promo popup: opens after load, then again 30 s after every close (assets/main.js)."""
    u = UI[ui_lang(lang)]
    if has_img("popup"):
        inner = img("popup", u["popup_alt"])
    else:
        inner = (f'<div class="popup-card"><span class="logo">{e(LOGO_TEXT)}</span><b>{u["popup_title"]}</b>'
                 f'<p>{u["popup_text"]}</p><span class="btn btn-go btn-lg">{u["float_register"]}</span></div>')
    return (f'<div class="popup" id="promo-popup" role="dialog" aria-modal="true" aria-label="{e(u["popup_title"])}"><div class="popup-inner">'
            f'<button class="popup-close" type="button" aria-label="{u["popup_close"]}">&times;</button>'
            f'<a href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">{inner}</a></div></div>')


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
    """Home: each cluster with its pillar + supporting posts (home -> blog internal links)."""
    u = UI[ui_lang(lang)]
    cards = ""
    for k in CLUSTERS:
        lis = "".join(f'<li{" class=pillar" if is_pillar(p) else ""}><a href="/blog/{p["slug"]}/">{e(p["title"])}</a></li>' for p in cluster_posts(k))
        cards += f'<div class="guide-card"><h3><a href="/blog/{CLUSTERS[k]["pillar"]}/">{e(cname(k, lang))}</a></h3><ul>{lis}</ul></div>'
    return (f'<section class="block" id="guides"><div class="block-head"><small>{u["guides_small"]}</small><h2>{u["guides_h2"]}</h2></div>'
            f'<div class="guides">{cards}</div><p class="guides-all"><a class="btn btn-dark" href="/blog/">{u["guides_all"]}</a></p></section>')


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


# ---------------------------------------------------------------- home
def tile(g):
    slug, name, provider, _, badge = g
    key = f"games/{slug}"
    if has_img(key):
        pic = img(key, f"{name} — {provider}")
    else:
        letters = re.sub(r"[^A-Za-z0-9]", "", name)[:2].title() or name[:2]
        pic = f'<div class="letters g{sum(map(ord, slug)) % 6}"><b>{e(letters)}</b><span>{e(name)}</span></div>'
    b = f'<span class="badge {badge}">{badge}</span>' if badge else ""
    return (f'<a class="tile" href="{REGISTER_URL}" target="_blank" rel="nofollow sponsored noopener">'
            f'<div class="pic">{pic}{b}</div><div class="meta"><b>{e(name)}</b><span>{e(provider)}</span></div></a>')


def game_row(rid, ico, title, lang):
    games = [g for g in GAMES if g[3] == rid]
    if not games:
        return ""
    u = UI[lang]
    return f"""<section class="row" id="{rid}"><div class="row-head"><h2><span class="ico">{ico}</span>{title}</h2>
<div class="row-nav">{a('@register', u['see_all'], lang, True)}<button data-scroll="-1" aria-label="{u['prev']}">‹</button><button data-scroll="1" aria-label="{u['next']}">›</button></div></div>
<div class="row-track">{''.join(tile(g) for g in games)}</div></section>"""


def home(lang):
    h, u = HOME[lang], UI[lang]
    path = home_path(lang)
    entries = "".join(
        a(t, f'<div class="art">{img("hero-" + ("casino" if i == 0 else "sports"), lbl) if has_img("hero-" + ("casino" if i == 0 else "sports")) else ico}</div>'
             f'<div class="cap">{lbl}<span>{live}</span></div>', lang, True)
        for i, (ico, lbl, t, live) in enumerate(h["entry"]))
    banners = [n for n in sorted(SIZES) if re.fullmatch(r"banner-\d+", n)]
    banner_html = ('<div class="banners">' + "".join(a("@register", img(n, f"{BRAND} promotion", lazy=i > 0), lang, True)
                                                    for i, n in enumerate(banners)) + "</div>") if banners else ""
    ticker = per_lang(TICKER, lang)
    matches = ""
    if MATCHES:
        matches = (f'<section class="block" id="matches"><div class="row-head"><h2><span class="ico">⚽</span>{h["matches_h2"]}</h2></div><div class="matches">'
                   + "".join(f'<div class="match"><header><span>{e(lg)}</span><span>{e(t)}</span></header><p>{e(hm)}</p><p>{e(aw)}</p>'
                             f'{a("@register", h["bet"], lang, True, "btn btn-go")}</div>' for lg, t, hm, aw in MATCHES) + "</div></section>")
    rs, rt, steps = h["register"]
    promos = "".join(
        f'<div class="promo"><div class="pimg">{img("promos/" + im, t) if im and has_img("promos/" + im) else "🎁"}</div><div class="body">'
        f'<h3>{e(t)}</h3><p>{e(d)}</p><small>{u["tcs"]}</small>{a("@register", u["claim"], lang, True, "btn btn-blue")}</div></div>'
        for t, d, im in PROMOS)
    ak, ah, ap, al, ab = h["app"]
    phone = img("app", f"{BRAND} app", "") if has_img("app") else f'<div class="phone-mock">{e(LOGO_TEXT)}</div>'
    pills = lambda xs: '<div class="pills">' + "".join(f"<span>{e(x)}</span>" for x in xs) + "</div>"  # noqa: E731
    main = f"""<section class="hero"><div class="wrap hero-grid">
<div><h1>{h['h1']}</h1><p class="lead">{h['lead']}</p>{a('@register', h['cta'], lang, True, 'btn btn-blue btn-lg')}<p class="sub">{h['sub']}</p></div>
<div class="entry">{entries}</div></div></section>
<div class="wrap">
{banner_html}
{f'<div class="ticker"><b>{u["news"]}</b><span>{ticker}</span></div>' if ticker else ''}
<nav class="chips" aria-label="Categories">{''.join(a(t, f'{i} {l}', lang, True) for i, l, t in h['chips'])}</nav>
{per_lang(custom_sections.AFTER_HERO, lang)}
{''.join(game_row(r, *h['rows'][r], lang) for r in ROWS)}
{matches}
<section class="block" id="register"><div class="block-head"><small>{rs}</small><h2>{rt}</h2></div>
<div class="steps">{''.join(f'<div class="step"><div class="ico">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in steps)}</div></section>
{f'<section class="block" id="promos"><div class="block-head"><small>{h["promos"][0]}</small><h2>{h["promos"][1]}</h2></div><div class="promos">{promos}</div></section>' if PROMOS else ''}
<section class="block" id="app"><div class="app"><div><small class="byline">{ak}</small><h2>{ah}</h2><p>{ap}</p>
<ul>{''.join(f'<li>{x}</li>' for x in al)}</ul>{a('@app', ab, lang, True, 'btn btn-go btn-lg')}</div><div class="phone">{phone}</div></div></section>
<section class="block trust" id="payments"><div><h3>{h['trust'][0]}</h3>{pills(PROVIDERS)}</div><div><h3>{h['trust'][1]}</h3>{pills(PAYMENTS)}</div></section>
{guides_section(lang)}
{per_lang(custom_sections.BEFORE_FAQ, lang)}
<section class="block seo">{h['seo_intro']}<details><summary class="btn btn-dark"><span class="show">{u['more']}</span><span class="hide">{u['hide']}</span></summary><div class="more">{h['seo_more']}</div></details></section>
<section class="block faq" id="faq"><div class="block-head"><h2>{h['faq_h2']}</h2></div>
{''.join(f'<details><summary>{q}</summary><p>{ans}</p></details>' for q, ans in h['faq'])}</section>
</div>"""
    webpage = {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": h["title"],
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"},
               "datePublished": PUBLISHED, "dateModified": UPDATED, "inLanguage": u["hreflang"]}
    faq = {"@type": "FAQPage", "inLanguage": u["hreflang"], "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(ans)}} for q, ans in h["faq"]]}
    head = f'<link rel="preload" as="image" href="/images/{banners[0]}.webp">' if banners else ""
    return page(lang, h["title"], h["desc"], path, main, graph(org(), website(), webpage, faq, crumbs_schema([(u["home"], path)])),
                on_home=True, alternates={l: home_path(l) for l in LANGS}, extra_head=head)


# ---------------------------------------------------------------- blog, policies, contents
def crumbs(items):
    li = "".join(f'<li><a href="{u}"' + (' aria-current="page"' if i == len(items) - 1 else "") + f'>{e(n)}</a></li>' for i, (n, u) in enumerate(items))
    return f'<nav class="wrap crumbs" aria-label="Breadcrumb"><ol>{li}</ol></nav>'


def head_block(kicker, h1, p="", extra=""):
    return f'<div class="wrap page-head"><span class="kicker">{kicker}</span><h1>{h1}</h1>{f"<p>{p}</p>" if p else ""}{extra}</div>'


def post_card(p):
    u = UI[ui_lang(p["lang"])]
    url = f"/blog/{p['slug']}/"
    pil = is_pillar(p)
    label = e(p["card"]) if not pil or p["card"] == u["pillar_badge"] else f'{u["pillar_badge"]} · {e(p["card"])}'
    return (f'<article class="post-card{" pillar" if pil else ""}"><span class="cat">{label}</span><h2><a href="{url}">{e(p["title"])}</a></h2>'
            f'<p>{e(p["desc"])}</p><a class="more" href="{url}">{u["read"]}</a></article>')


def blog_index():
    lang, path = MAIN_LANG, "/blog/"
    u = UI[lang]
    items = [(u["home"], "/"), (BLOG_HUB["kicker"], path)]
    groups = "".join(f'<h2 class="section-label">{e(cname(k, lang))}</h2><div class="post-grid">' + "".join(post_card(p) for p in cluster_posts(k)) + "</div>"
                     for k in CLUSTERS)
    main = f"{crumbs(items)}{head_block(BLOG_HUB['kicker'], BLOG_HUB['h1'], BLOG_HUB['p'])}<div class=\"wrap\">{groups}</div>"
    coll = {"@type": "CollectionPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": BLOG_HUB["title"], "isPartOf": {"@id": SITE + "/#website"},
            "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{p['slug']}/"}
                                                                    for i, p in enumerate(q for k in CLUSTERS for q in cluster_posts(k))]}}
    return page(lang, BLOG_HUB["title"], BLOG_HUB["desc"], path, main, graph(org(), website(), coll, crumbs_schema(items)))


def post_page(p):
    lang = p["lang"]
    u = UI[ui_lang(lang)]
    path = f"/blog/{p['slug']}/"
    k = p["cluster"]
    group = cluster_posts(k)
    pillar = group[0]
    up = "" if p is pillar else f'<p class="pillar-note">{u["pillar_note"]}: <a href="/blog/{pillar["slug"]}/">{e(pillar["title"])}</a></p>'
    lis = "".join(f'<li{" class=pillar" if q is pillar else ""}>' + (f"<b>{e(q['title'])}</b>" if q is p else f'<a href="/blog/{q["slug"]}/">{e(q["title"])}</a>') + "</li>"
                  for q in group)
    box = f'<nav class="cluster" aria-label="{e(cname(k, lang))}"><h2>{u["cluster_h"]}: {e(cname(k, lang))}</h2><ol>{lis}</ol></nav>'
    rel = "".join(f'<li><a href="/blog/{q["slug"]}/">{e(q["title"])}</a></li>' for q in group if q is not p)
    others = "".join(f'<li><a href="/blog/{CLUSTERS[o]["pillar"]}/">{e(cname(o, lang))}</a></li>' for o in CLUSTERS if o != k)
    secs = "".join(f"<h2>{e(h)}</h2>" + "".join(render_block(b, lang) for b in blocks) for h, blocks in p["sections"])
    items = [(u["home"], home_path(lang)), (u["blog"], "/blog/")] + ([] if p is pillar else [(cname(k, lang), f"/blog/{pillar['slug']}/")]) + [(p["card"], path)]
    by = f'<p class="byline">{u["by"]} {e(BRAND)} {u["team"]} · <time datetime="{PUBLISHED}">{u["published"]} {PUBLISHED}</time></p>'
    main = f"""{crumbs(items)}{head_block(e(cname(k, lang)), e(p['title']), '', by)}
<div class="wrap article"><article class="prose">{up}{render_block(p['intro'], lang)}{secs}{box}<div class="note">{u['rg_note']}</div><p><a href="/blog/">{u['back']}</a></p></article>
<aside class="aside"><div class="widget cta-widget"><h2>{u['start']}</h2><p>{u['start_p']}</p>{a('@register', u['register'], lang, cls='btn btn-go')}</div>
<div class="widget"><h2>{u['related']}</h2><ul>{rel}</ul></div>
<div class="widget"><h2>{u['other_topics']}</h2><ul>{others}</ul></div></aside></div>"""
    art = {"@type": "BlogPosting", "@id": SITE + path + "#article", "headline": p["title"], "description": p["desc"], "url": SITE + path,
           "mainEntityOfPage": SITE + path, "inLanguage": u["hreflang"], "keywords": ", ".join(p["kw"]), "articleSection": cname(k, lang),
           "datePublished": PUBLISHED, "dateModified": UPDATED, "image": SITE + "/images/og.jpg", "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}}
    if p is not pillar:
        art["isPartOf"] = {"@id": f"{SITE}/blog/{pillar['slug']}/#article"}
    return page(lang, f"{p['title']} | {BRAND}", p["desc"], path, main, graph(org(), art, crumbs_schema(items)), og_type="article",
                keywords=p["kw"] + pillar["kw"][:1] + [BRAND])


def policy_page(p):
    lang, path = MAIN_LANG, f"/{p['slug']}/"
    u = UI[lang]
    items = [(u["home"], "/"), (p["title"], path)]
    body = "".join(f"<h2>{h}</h2>{b}" for h, b in p["body"])
    main = f'{crumbs(items)}{head_block(u["info"], p["title"])}<div class="wrap"><article class="prose">{body}</article></div>'
    wp = {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": p["title"], "isPartOf": {"@id": SITE + "/#website"}}
    return page(lang, f"{p['title']} | {BRAND} Malaysia", p["desc"], path, main, graph(org(), wp, crumbs_schema(items)))


def all_pages():
    out = [(home_path(l), HOME[l]["title"]) for l in LANGS] + [("/blog/", BLOG_HUB["title"])]
    out += [(f"/{p['slug']}/", p["title"]) for p in POLICIES] + [("/contents/", UI[MAIN_LANG]["contents"])]
    return out + [(f"/blog/{p['slug']}/", p["title"]) for k in CLUSTERS for p in cluster_posts(k)]


def contents_page():
    lang, path = MAIN_LANG, "/contents/"
    u = UI[lang]
    items = [(u["home"], "/"), (u["contents"], path)]
    main_pages = [x for x in all_pages() if not x[0].startswith("/blog/") or x[0] == "/blog/"]
    groups = [(u["site_map"], main_pages)] + [(cname(k, lang), [(f"/blog/{p['slug']}/", p["title"]) for p in cluster_posts(k)]) for k in CLUSTERS]
    secs = "".join(f"<h2>{e(g)}</h2><ul>" + "".join(f'<li><a href="{x}">{e(t)}</a></li>' for x, t in links) + "</ul>" for g, links in groups)
    main = f'{crumbs(items)}{head_block(u["site_map"], u["contents"])}<div class="wrap"><div class="prose">{secs}</div></div>'
    return page(lang, f"{u['contents']} | {BRAND} Malaysia", u["contents_p"], path, main, graph(org(), crumbs_schema(items)))


def not_found():
    u = UI[MAIN_LANG]
    main = head_block("404", u["nf_title"], u["nf_p"]) + \
        f'<div class="wrap"><a class="btn btn-blue" href="/">{u["nf_home"]}</a>{guides_section(MAIN_LANG)}</div>'
    return page(MAIN_LANG, f"{u['nf_title']} | {BRAND}", u["nf_p"], "/404", main, "").replace(
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
    for p in POSTS:
        write(f"/blog/{p['slug']}/", post_page(p))
    for p in POLICIES:
        write(f"/{p['slug']}/", policy_page(p))
    write("/contents/", contents_page())
    write("/404.html", not_found())
    urls = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod></url>" for u, _ in all_pages())
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("/llms.txt", f"# {BRAND} Malaysia\n\n> {TAGLINE}: slots, live casino, sports, fishing and instant games. 18+.\n\n"
          + "\n".join(f"- [{strip_tags(t)}]({SITE}{u})" for u, t in all_pages()) + "\n")
    copy_static()
    left = {t for root, _, fs in os.walk(DIST) for f in fs if f.endswith((".html", ".xml", ".txt"))
            for t in re.findall(r"__[A-Z_]+__", open(os.path.join(root, f), encoding="utf-8").read())}
    if left:
        sys.exit(f"unreplaced tokens: {left}")
    for w in audit_clusters():
        print("  cluster:", w)
    for w in META_WARN:
        print("  meta:", w)
    print(f"built {len(all_pages())} pages in dist/" + ("" if SIZES else "  (no images yet; run build/images.py)"))


if __name__ == "__main__":
    main()
