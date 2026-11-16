# iGaming_Templates_13_SkyGlow · Claude instructions

Eye-catching navy + sky-blue glow casino site (design inspired by a66slot.pro) on the Template 4 engine, tuned for
**PageSpeed 100** and **entity SEO**. Bahasa Melayu is the default (`/`, x-default ms-MY); English translation of EVERY page
at `/en/` with English URLs. 68 pages out of the box (34 per language). Python 3 + Pillow; deploy to Cloudflare Pages with `npx wrangler@3`.

## Golden rule: the STRUCTURE IS FIXED
- Per language: home, casino hub + 8 game categories, app, promotions, affiliate, glossary, 6 policies, blog hub, 12 posts (4 clusters), contents. Plus 404, sitemap (hreflang alternates), robots, llms.txt.
- Home order: dark hero band [banner 900x500 → H1 + square art] → stats band → about split → 8 feature cards → game grid + slot/live duo cards → desktop-vs-app comparison table → bingo/sports split → payments split (chips) → promotions → app split → 3 steps → responsible-gaming cards → "we serve all of Malaysia" states → guides by topic → FAQ → latest guides → CTA band
- Sub pages: dark hero band (banner → breadcrumb → H1/intro/CTAs/square art) → sections → steps/promos/child grid/glossary → related cluster → FAQ → CTA band
- Every page: dark header (logo, nav with Casino dropdown, BM/EN switch to the SAME page, Daftar + Log Masuk), footer, floating Login/Register banner, 9:16 popup
- Everything builds into `dist/` (wiped each build). Never edit dist/.

## Files
- `build/site_config.py`: brand + BRAND_ALT, LOGO_PARTS/LOGO_ICON, links, NAP (optional), SAME_AS, ENTITIES, ORG_KNOWS_ABOUT, LANGS, KEYWORDS, dates, tracking, CF_PROJECT, STATS, PROMOS, PAYMENTS, PROVIDERS, STATES, THEME
- `build/content.py`: UI strings + HOME (ms, en). `<em>` in h1/h2 = sky highlight.
- `build/pages.py`: PAGES (each with `about` entity keys and ms + en dicts). The glossary page has `terms` (entity key, BM def, EN def).
- `build/posts.py`: CLUSTERS + POSTS (each with `about` entity keys)
- `build/images.py` (all square except banner 900x500, popup 9:16, og), `build/icons.py` (logo PNGs + favicons)

## Entity SEO (schema, all JSON-LD connected by @id)
- One brand entity: `Organization` `#org` + `Brand` `#brand` + `#logo`, with alternateName, areaServed Malaysia (Wikipedia), knowsAbout, sameAs (SAME_AS), optional email/phone/address. Every graph includes Organization, Brand and WebSite `#website`.
- Pages: WebPage / CollectionPage with `about` (first 2 entity keys) + `mentions` (rest) -> Wikipedia `sameAs`; BreadcrumbList `#crumbs`; FAQPage when the page has FAQ.
- Home: ItemList `#games` of game categories. Casino hub: ItemList `#list`. App page: SoftwareApplication `#app` (free offer, no rating — never add fake ratings). Glossary: DefinedTermSet `#terms` with DefinedTerm + sameAs. Posts: BlogPosting with about/mentions, isPartOf pillar.
- ENTITIES URLs were each checked to exist (curl 200). Add new ones only after opening them. No WebSite SearchAction (there's no site search).

## PageSpeed 100 rules (verified: Lighthouse 12, mobile + desktop, home / category / post / glossary / app = 100·100·100·100, also with 20 real images)
- CSS is inlined; one font (Outfit 800, `font-display:optional` + preload → no layout shift); everything else system fonts.
- JS is one small deferred file. GA4 loads only after first interaction.
- **Popup choice:** the first popup opens 1.2 s after the visitor's first interaction (scroll/tap/key) or after 20 s, then 30 s after each close. Its image uses `data-src` and loads only when it opens, so it never becomes the LCP element or shifts layout.
- Banner = LCP: eager + preloaded when an image exists; other images lazy with width/height. Floating bar is fixed and the body reserves its height (no CLS).
- Animations use transform/opacity only and stop under `prefers-reduced-motion`.
- Contrast: text on white uses `--accent-ink` (#0369A1), never the bright sky (#38BDF8, used only on dark or as backgrounds). Tap targets >= 40px. Logo has no aria-label (its visible text is the name).
- Re-test after design changes: `npx --yes lighthouse@12 http://localhost:8000/ --only-categories=performance,accessibility,best-practices,seo --chrome-flags="--headless=new"` (+ `--preset=desktop`). Local text-compression/cache warnings are from python http.server; Cloudflare compresses and `_headers` sets caching.

## Link syntax (everywhere in content)
`[[key|anchor]]`: key = page key, post key, `home`, `home#id`, `blog`, `contents`, or `@register @login @app @chat` (sponsored, new tab). Unknown key = build error.

## SEO rules the build enforces (fix every warning before deploy)
- `meta`: title <= 60 chars, description 120-160 chars (CTR: year, number, benefit, action verb, brand)
- `focus`: focus keyword must appear in title, desc, h1 and intro
- `h1`: exactly one H1 per page
- `cluster`: supporting -> pillar, pillar -> all its supporting posts, each post -> another cluster AND a site page, no orphans
- When the brand itself contains a product word (e.g. "A66 **Slot**"), phrase focus keywords so they don't repeat it ("Slot Online di A66 Slot").

## New site workflow (token-cheap: DON'T read build.py unless the task needs it)
1. `cp -R iGaming_Templates_13_SkyGlow ../<domain>` then in the copy run `./deploy.sh clean`.
2. Follow "From keywords to site"; edit site_config.py, then content/pages/posts text.
3. Images → `images/src/` → `python3 build/images.py`; `python3 build/icons.py`.
4. `./deploy.sh build` → fix all warnings → preview `python3 -m http.server 8000 --directory dist` → Lighthouse → `./deploy.sh`.
5. `npx wrangler@3 whoami` must show the site's Cloudflare account. IndexNow is automatic (own key per site).

## Standing rules for every site (user's requirements — always apply)
1. **Local language is the main language** (Malaysia = BM at `/`, x-default); English translation for every page.
2. **High-CTR meta title, description, focus keyword and keywords on every page.**
3. **Popup:** 9:16 phone-size image, reopens 30 s after every close (first open as above, for PageSpeed).
4. **Floating footer banner** with Login + Register on every page.
5. **Banner 900x500 above the hero**; all other content images square; logo + favicons generated.
6. **Inspiration website:** fetch it first (curl; if blocked, headless Chrome screenshot), carry colours into THEME and section ideas into copy. Never copy its logo, brand name or text.
7. **Blog = topical authority** with clusters and internal links across pages; **entity SEO** via ENTITIES/about/SAME_AS.
8. **At least 50 pages** total. **PageSpeed 100** — re-run Lighthouse before deploy.
9. Don't invent facts: STATS and PROMOS are examples from the reference until the brief confirms them; no fake ratings, winners or licences.

## From keywords to site (the normal way a new site is requested)
The user gives brand + domain + links, a **keyword list** and usually an **inspiration website**. NEW_SITE_BRIEF.md is optional — fill it in yourself as the record.
1. Group keywords by intent. Product terms -> the matching page in pages.py (`focus` + `kw` + `about` entities). Brand/how-to terms -> blog clusters: head term = pillar, long-tail = supporting posts.
2. Top 6-10 terms -> `KEYWORDS`; head terms -> home title/desc/H1. Brand spellings -> `BRAND_ALT`; official profiles -> `SAME_AS`.
3. Rewrite titles/descs for CTR in BM first, then EN. Keep page keys; change slugs only if the keyword calls for it.
4. Replace starter posts with keyword posts; keep >= 3 clusters and the link rules; tag each with `about` entities.
5. Apply the inspiration site, build, fix every warning, run Lighthouse, deploy.
