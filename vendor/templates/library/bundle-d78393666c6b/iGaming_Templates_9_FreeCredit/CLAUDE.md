# iGaming_Templates_9_FreeCredit · Claude instructions

Free-credit slot casino (layout + page set from ekplus8.pro) built on the Templates_4 engine, with every feature of Templates 1-4.
Bahasa Melayu is the default (`/`, x-default); English translation of EVERY page at `/en/` with English URLs.
70 pages out of the box (35 per language). Python 3 + Pillow; deploy to Cloudflare Pages with `npx wrangler@3`.

## Golden rule: the STRUCTURE IS FIXED
- Per language: home, 5 game pages (slots, casino online, sportsbook, fish games, jackpot & Hot 1:100), free credit hub + 1 page per provider in FC_PROVIDERS (7), promo, app, 8 brand/policy pages (about, mission & core values, security system, protection policy, responsible gambling, contact, privacy, terms), blog hub, 9 posts (3 clusters), contents. Plus 404, sitemap (hreflang alternates), robots, llms.txt.
- Header: charcoal bar, uppercase links, yellow active, dropdowns (Slot, Kredit Percuma), BM/EN switch to the SAME page
- Header band (home + game/info pages): banner 900x500 + two wide buttons, gold LOGIN / teal REGISTER
- Home order: band → promo grid (square) → game tiles → provider free-credit tiles → long-form article (H1, intro, what is, overview table, free credit table + how it works, games, provider guide table, payments, how to join, member features) → guides by topic → FAQ → responsible + explore links → latest guides → CTA band
- Game/free-credit pages: band → breadcrumb → hero card (H1, intro, CTAs, square art) → sections → steps / free-credit table / provider tiles / promos → related cluster box → FAQ → CTA band
- Every page: footer, floating Login/Register bar, 9:16 popup every 30 s. Everything builds into `dist/`. Never edit dist/.

## Files
- `build/site_config.py`: brand, LOGO_PARTS/LOGO_ICON, links (+ TELEGRAM_URL / FACEBOOK_URL), LANGS, KEYWORDS, OVERVIEW (home facts table), FREE_CREDITS (offer table), FC_PROVIDERS (one guide page each), PROMOS, PAYMENTS, PROVIDERS, THEME
- `build/content.py`: UI strings + HOME (ms, en)
- `build/pages.py`: PAGES (ms + en dicts) + FC_NOTES; provider free-credit pages are generated from FC_PROVIDERS
- `build/posts.py`: CLUSTERS + POSTS
- `build/custom_sections.py`: AFTER_HERO (after the tile grids) / BEFORE_FAQ / EXTRA_CSS
- `build/images.py` (all square except banner 900x500, popup 9:16, og; providers/<key> for provider tiles), `build/icons.py` (logo PNGs + favicons, yellow on charcoal)

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
1. `cp -R iGaming_Templates_9_FreeCredit ../<domain>` then in the copy run `./deploy.sh clean`.
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

## From keywords to site (the normal way a new site is requested)
The user gives brand + domain + links, a **keyword list** and usually an **inspiration website**. NEW_SITE_BRIEF.md is optional — fill it in yourself as the record.
1. Group keywords by intent. Product terms (slot, live casino, sports…) -> the matching page in pages.py (`focus` + `kw`). "free credit <provider>" terms -> FC_PROVIDERS (+ FC_NOTES). Brand/how-to terms -> blog clusters: head term = pillar, long-tail = supporting posts.
2. Top 6-10 terms -> `KEYWORDS`; head terms -> home title/desc/H1.
3. Rewrite titles/descs for CTR in BM first, then EN. Keep page keys; change slugs only if the keyword calls for it.
4. Replace starter posts with keyword posts; keep >= 3 clusters and the link rules.
5. Apply the inspiration site, build, fix every warning, deploy.
