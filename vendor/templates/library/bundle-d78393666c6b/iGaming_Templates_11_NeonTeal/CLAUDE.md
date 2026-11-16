# iGaming_Templates_11_NeonTeal · Claude instructions

Dark navy + teal neon casino portal (design, home sections and page set from kingroup88.net) on the Templates_4 engine.
Bahasa Melayu is the default (`/`, x-default); English translation of EVERY page at `/en/` with English URLs.
84 pages out of the box (42 per language). Python 3 + Pillow; deploy to Cloudflare Pages with `npx wrangler@3`.

## Golden rule: the STRUCTURE IS FIXED
- Per language: home; casino hub + slots, poker, table games, jackpot, fishing, lottery, instant win; live casino, sports, esports;
  welcome bonus, promotions, VIP membership; register, login, betting tips, FAQ, app, affiliate; 6 policies; blog hub; 13 posts (4 clusters); contents.
  Plus 404, sitemap (with hreflang alternates), robots, llms.txt.
- Home order: header → marquee ticker → banner 900x500 → hero (badge, H1 with teal <span>, square art) → trust bar (5) → stats bar (6) →
  promo carousel → game wall (hover overlay) → sports (markets or MATCHES) → 4 step cards → 6 advantage cards → comparison table →
  app + phone mockup → membership tiers → guides by topic → SEO text → states served → FAQ → latest guides → CTA band
- Page types: hub, game, info, promos, vip (tier cards), faq (FAQ list), policy.
- Every page: sticky header (nav with Casino/Sports/Bonus dropdowns, BM/EN switch to the SAME page, Daftar + Log Masuk), marquee,
  footer, floating Login/Register footer, 9:16 popup every 30 s
- Everything builds into `dist/` (wiped each build). Never edit dist/.

## Files
- `build/site_config.py`: brand, LOGO_PARTS/LOGO_ICON, links, LANGS, KEYWORDS, dates, tracking, CF_PROJECT, PROMOS (carousel), TICKER, STATS, MATCHES, PAYMENTS, PROVIDERS, THEME
- `build/content.py`: UI strings (incl. membership tiers) + HOME (ms, en): trust, sports, advantages, compare, app, SEO text, states, FAQ
- `build/pages.py`: PAGES — one entry per page, each with ms + en dicts (slug, title, desc, focus, kw, h1, intro, sections, faq)
- `build/posts.py`: CLUSTERS + POSTS (same per-language shape)
- `build/custom_sections.py`: AFTER_HERO / BEFORE_FAQ / EXTRA_CSS
- `build/images.py` (all square except banner 900x500, popup 9:16, og), `build/icons.py` (logo PNGs + favicons)

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
1. `cp -R iGaming_Templates_11_NeonTeal ../<domain>` then in the copy run `./deploy.sh clean`.
2. Follow "From keywords to site" below; edit site_config.py, then content/pages/posts text.
3. Images → `images/src/` → `python3 build/images.py`; `python3 build/icons.py`.
4. `./deploy.sh build` → fix all warnings → preview `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.
5. `npx wrangler@3 whoami` must show the site's Cloudflare account. IndexNow is automatic (own key per site).

## Standing rules for every site (user's requirements — always apply)
1. **Local language is the main language** (Malaysia = BM at `/`, x-default); English translation for every page.
2. **Meta title, description, focus keyword and keywords on every page**, written for high CTR.
   No fake live scores, odds or win feeds in TICKER / STATS / MATCHES — real notices and verifiable numbers only.
3. **Popup:** 9:16 phone-size image, opens ~1.5 s after load and 30 s after every close.
4. **Floating footer** with Login + Register on every page.
5. **Banner 900x500 above the hero**; all other content images square; logo + favicons generated.
6. **Inspiration website:** fetch it first (curl; if blocked, headless Chrome screenshot), carry colours into THEME and section ideas into copy/custom sections. Never copy its logo, brand name or text.
7. **Blog = topical authority** with clusters and internal links across pages (home, hubs, category pages, footer, posts).
8. **At least 50 pages** total.

## From keywords to site (the normal way a new site is requested)
The user gives brand + domain + links, a **keyword list** and usually an **inspiration website**. NEW_SITE_BRIEF.md is optional — fill it in yourself as the record.
1. Group keywords by intent. Product terms (slot, live casino, sports…) -> the matching page in pages.py (`focus` + `kw`). Brand/how-to terms -> blog clusters: head term = pillar, long-tail = supporting posts.
2. Top 6-10 terms -> `KEYWORDS`; head terms -> home title/desc/H1.
3. Rewrite titles/descs for CTR in BM first, then EN. Keep page keys; change slugs only if the keyword calls for it.
4. Replace starter posts with keyword posts; keep >= 3 clusters and the link rules.
5. Apply the inspiration site, build, fix every warning, deploy.
