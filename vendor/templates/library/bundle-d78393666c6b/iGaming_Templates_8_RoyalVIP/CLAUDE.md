# iGaming_Templates_8_RoyalVIP · Claude instructions

White lobby with royal purple + gold stroked display headings (design + section set from mrace88my.com), built on the
Template 4 engine (every feature of Templates 1-4).
Bahasa Melayu is the default (`/`, x-default); English translation of EVERY page at `/en/` with English URLs.
68 pages out of the box (34 per language). Python 3 + Pillow; deploy to Cloudflare Pages with `npx wrangler@3`.

## Golden rule: the STRUCTURE IS FIXED
- Per language: home, casino hub + 8 game categories, app, promotions, VIP, affiliate, 6 policies, blog hub, 12 posts (4 clusters), contents. Plus 404, sitemap (with hreflang alternates), robots, llms.txt.
- Home order: banner 900x500 → marquee ticker → Recommended Games (CSS tabs: featured square tile + provider grid) → Popular Games (framed tiles, APPS ribbon) → Live Casino provider row → H1 split (intro + square art) → "Why choose" 8 cards → slots/sports duo → 4 steps + Quick Start card → mobile & app list → VIP tier table + promos → purple SEO band → guides by topic → FAQ → latest guides → CTA band
- Slot / Live Casino / Sports pages also show their GAME_TABS provider grid; the VIP page shows the VIP_TIERS table
- Game/info pages: banner → breadcrumb → hero (H1, intro, CTAs, square art) → sections → steps/promos/child grid → related cluster box → FAQ → CTA band
- Every page: header (stroked wordmark logo, nav with Slot/Sukan/Tentang dropdowns, BM/EN switch to the SAME page, Daftar + Log Masuk), footer, floating Login/Register footer, 9:16 popup every 30 s
- Everything builds into `dist/` (wiped each build). Never edit dist/.

## Files
- `build/site_config.py`: brand, LOGO_PARTS/LOGO_ICON, links, LANGS, KEYWORDS, dates, tracking, CF_PROJECT, TICKER, GAME_TABS, POPULAR, LIVE_PROVIDERS, PROMOS, VIP_TIERS, PAYMENTS, PROVIDERS, LICENSES (only real ones), SOCIAL, THEME
- `build/content.py`: UI strings + HOME (ms, en)
- `build/pages.py`: PAGES — one entry per page, each with ms + en dicts (slug, title, desc, focus, kw, h1, intro, sections, faq)
- `build/posts.py`: CLUSTERS + POSTS (same per-language shape)
- `build/custom_sections.py`: AFTER_HERO / BEFORE_FAQ / EXTRA_CSS
- `build/images.py` (all square except banner 900x500, popup 9:16, og; also providers/<slug>, games/<slug>, featured-<tab>, vip-badge), `build/icons.py` (logo PNGs + favicons)

## Link syntax (everywhere in content)
`[[key|anchor]]`: key = page key, post key, `home`, `home#id`, `blog`, `contents`, or `@register @login @app @chat` (sponsored, new tab).
Keys are language-neutral: the build links to the same language's URL. Unknown key = build error.

## SEO rules the build enforces (fix every warning before deploy)
- `meta`: title <= 60 chars, description 120-160 chars (write for CTR: year, number, benefit, action verb, brand)
- `focus`: the focus keyword must appear in title, desc, h1 and intro
- `h1`: exactly one H1 per page
- `cluster`: supporting -> pillar, pillar -> all its supporting posts, each post -> another cluster AND a site page, no orphans
- `<meta name="keywords">` = page `kw` + brand (home also gets KEYWORDS)

## New site workflow (token-cheap: DON'T read build.py unless the task needs it)
1. `cp -R iGaming_Templates_8_RoyalVIP ../<domain>` then in the copy run `./deploy.sh clean`.
2. Follow "From keywords to site" below; edit site_config.py, then content/pages/posts text.
3. Images → `images/src/` → `python3 build/images.py`; `python3 build/icons.py`.
4. `./deploy.sh build` → fix all warnings → preview `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.
5. `npx wrangler@3 whoami` must show the site's Cloudflare account. IndexNow is automatic (own key per site).

## Standing rules for every site (user's requirements — always apply)
1. **Local language is the main language** (Malaysia = BM at `/`, x-default); English translation for every page.
2. **Meta title, description, focus keyword and keywords on every page**, written for high CTR.
3. **Popup:** 9:16 phone-size image, opens ~1.5 s after load and 30 s after every close.
4. **Floating footer** with Login + Register on every page.
5. **Banner 900x500 above the hero**; all other content images square; logo + favicons generated.
6. **Inspiration website:** fetch it first (curl; if blocked, headless Chrome screenshot), carry colours into THEME and section ideas into copy/custom sections. Never copy its logo, brand name or text.
7. **Blog = topical authority** with clusters and internal links across pages (home, hubs, category pages, footer, posts).
8. **At least 50 pages** total.
9. VIP tier values, offers and licences must be the operator's real ones — the example values came from the reference site.

## From keywords to site (the normal way a new site is requested)
The user gives brand + domain + links, a **keyword list** and usually an **inspiration website**. NEW_SITE_BRIEF.md is optional — fill it in yourself as the record.
1. Group keywords by intent. Product terms (slot, live casino, sports…) -> the matching page in pages.py (`focus` + `kw`). Brand/how-to terms -> blog clusters: head term = pillar, long-tail = supporting posts.
2. Top 6-10 terms -> `KEYWORDS`; head terms -> home title/desc/H1.
3. Rewrite titles/descs for CTR in BM first, then EN. Keep page keys; change slugs only if the keyword calls for it.
4. Replace starter posts with keyword posts; keep >= 3 clusters and the link rules.
5. Apply the inspiration site, build, fix every warning, deploy.
