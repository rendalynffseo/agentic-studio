# iGaming_Templates_7_GreenLobby · Claude instructions

Green 3-column casino lobby dashboard (design + page set from mrmart88.com) on the Templates_4 engine.
Bahasa Melayu is the default (`/`, x-default); English translation of EVERY page at `/en/` with English URLs.
74 pages out of the box (37 per language). Python 3 + Pillow; deploy to Cloudflare Pages with `npx wrangler@3`.

## Golden rule: the STRUCTURE IS FIXED
- Per language: home, games hub + 6 game pages (slots, live, sports, fishing, table, fast), promotions, free credit, VIP, referral,
  lucky draw, app, help centre (FAQ), about, contact, responsible gaming, privacy, terms, blog hub, 15 posts (5 clusters), contents.
  Plus 404, sitemap (with hreflang alternates), robots, llms.txt.
- Shell on every page: app-download strip → green header (logo, nav with Promosi/Lagi dropdowns, BM/EN switch to the SAME page, Log Masuk + Daftar)
  → marquee ticker → [page] → footer → floating Login/Register footer (desktop) / bottom tab bar with Daftar centre + Log Masuk (mobile) → 9:16 popup every 30 s
- Home: banner 900x500 → dashboard [left: quick facts, lucky pick spinner, providers | centre: H1 hero, category tabs (All/Hot/Slot/Live/Fish/Table/Fast),
  deposit bar, search, square game tiles with PLAY | right: login/register, account card (min deposit/withdraw), referral, lucky draw, game tips]
  → article panel: overview facts table, why cards, free credit table, no-turnover rebate, game categories, banking, mobile, how to claim, support,
  guides by topic, FAQ, latest guides → CTA band
- Game pages show a filtered game board for their tab; promotions page = promo table + cards; lucky draw page = rule + prize grid.
- No fake live data: the reference's live transaction feed / balance widgets are replaced by config-driven facts. Keep it that way.
- Everything builds into `dist/` (wiped each build). Never edit dist/.

## Files
- `build/site_config.py`: brand, LOGO_PARTS (d/g/a colours)/LOGO_ICON, links, LANGS, KEYWORDS, MIN_DEPOSIT/MIN_WITHDRAW, TICKER, FACTS,
  GAMES (square tiles, tab, badge), PROMOS (title/text/how), LUCKY_DRAW, PAYMENTS, PROVIDERS, THEME
- `build/content.py`: UI strings (nav, tabs, widgets, tab bar) + HOME (ms, en)
- `build/pages.py`: PAGES — one entry per page with ms + en dicts (slug, title, desc, focus, kw, h1, intro, sections, faq)
- `build/posts.py`: CLUSTERS + POSTS (same per-language shape)
- `build/custom_sections.py`: AFTER_HERO (top of article panel) / BEFORE_FAQ / EXTRA_CSS
- `build/images.py` (all square except banner 900x500, popup 9:16, og), `build/icons.py` (logo PNGs + favicons, green/gold)

## Link syntax (everywhere in content)
`[[key|anchor]]`: key = page key, post key, `home`, `home#id`, `blog`, `contents`, or `@register @login @app @chat` (sponsored, new tab).
Keys are language-neutral. Unknown key = build error.

## SEO rules the build enforces (fix every warning before deploy)
- `meta`: title <= 60 chars, description 120-160 chars (CTR: year, number, benefit, action verb, brand)
- `focus`: focus keyword in title, desc, h1 and intro
- `h1`: exactly one H1 per page
- `cluster`: supporting -> pillar, pillar -> all its supporting posts, each post -> another cluster AND a site page, no orphans

## New site workflow (token-cheap: DON'T read build.py unless the task needs it)
1. `cp -R iGaming_Templates_7_GreenLobby ../<domain>` then in the copy run `./deploy.sh clean`.
2. Follow "From keywords to site" below; edit site_config.py, then content/pages/posts text.
3. Images → `images/src/` (games/<slug>, categories/<page key>, promos/<name>, posts/<post key>, banner, popup, app, logo) → `python3 build/images.py`; `python3 build/icons.py`.
4. `./deploy.sh build` → fix all warnings → preview `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.
5. `npx wrangler@3 whoami` must show the site's Cloudflare account. IndexNow is automatic (own key per site).

## Standing rules for every site (user's requirements — always apply)
1. **Local language is the main language** (Malaysia = BM at `/`, x-default); English translation for every page.
2. **Meta title, description, focus keyword and keywords on every page**, written for high CTR.
3. **Popup:** 9:16 phone-size image, opens ~1.5 s after load and 30 s after every close.
4. **Floating footer** with Login + Register on every page (tab bar on mobile).
5. **Banner 900x500 above the hero**; all other content images square; logo + favicons generated.
6. **Inspiration website:** fetch it first (curl; if blocked, headless Chrome screenshot), carry colours into THEME and section ideas into copy/custom sections. Never copy its logo, brand name or text.
7. **Blog = topical authority** with clusters and internal links across pages (home, hubs, game pages, footer, posts).
8. **At least 50 pages** total; blogs and important pages (help, policies, promotions, rewards) always included.

## From keywords to site (the normal way a new site is requested)
The user gives brand + domain + links, a **keyword list** and usually an **inspiration website**. NEW_SITE_BRIEF.md is optional — fill it in yourself as the record.
1. Group keywords by intent. Product terms (slot, live casino, free credit…) -> the matching page in pages.py (`focus` + `kw`). Brand/how-to terms -> blog clusters: head term = pillar, long-tail = supporting posts.
2. Top 6-10 terms -> `KEYWORDS`; head terms -> home title/desc/H1.
3. Rewrite titles/descs for CTR in BM first, then EN. Keep page keys; change slugs only if the keyword calls for it.
4. Replace starter posts with keyword posts; keep >= 3 clusters and the link rules. Update FACTS/PROMOS/LUCKY_DRAW to the brand's real offers.
5. Apply the inspiration site, build, fix every warning, deploy.
