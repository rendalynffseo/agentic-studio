# iGaming_Templates_3_CasinoLobby · Claude instructions

Operator-style casino lobby. Sections/content from bk8masd.com, look from Stake-style lobbies (navy, fixed left sidebar,
blue/green buttons, portrait game tiles in swipe rows, mobile bottom tab bar). EN/BM/中文 home pages + blog + policies.
Python 3 + Pillow; deploy to Cloudflare Pages with `npx wrangler@3`. Works with zero images (styled placeholders).

## Golden rule: the STRUCTURE IS FIXED
- Pages: `/` (BM, main) + `/en/` + `/zh/`, `/blog/`, `/blog/<slug>/`, `/about/ /responsible-gaming/ /privacy-policy/ /terms/ /contents/`, 404, sitemap, robots, llms.txt
- Home order: hero (welcome + Casino/Sports cards) → banner carousel → news ticker → category chips → game rows
  (slots, live, instant, fishing) → upcoming matches (only if MATCHES) → How to Register (4 steps) → promotions →
  app download → providers + payments → guides by topic (clusters) → SEO article ("Read more") → FAQ
- Shell on every page: left sidebar (drawer on mobile), sticky topbar (Login / Join), footer, floating footer (desktop) / bottom tab bar with Login + Join (mobile), chat bubble, 9:16 popup
- Everything builds into `dist/` (wiped each build). Never edit dist/.

## What changes per site (only this, unless the user asks)
1. `build/site_config.py`: brand, links, LANGS, dates, tracking, CF_PROJECT, TICKER, GAMES, PROMOS, MATCHES, PROVIDERS, PAYMENTS, THEME
2. Images (all optional) in `images/src/` → `python3 build/images.py` (names: docstring of build/images.py)
3. `python3 build/icons.py` (favicons from LOGO_TEXT + THEME accent)
4. Text tweaks: `build/content.py` (per language). Extra blocks: `build/custom_sections.py`. Don't restructure build.py.

## New site workflow (token-cheap: DON'T read build.py, content.py or posts.py unless the task needs it)
1. `cp -R iGaming_Templates_3_CasinoLobby ../<domain>` then in the copy run `./deploy.sh clean` (removes the old site's build, key and images)
2. Read `NEW_SITE_BRIEF.md` if filled in → edit `build/site_config.py` only.
3. Images → `python3 build/images.py`; `python3 build/icons.py`.
4. `./deploy.sh build` → preview `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.
5. `npx wrangler@3 whoami` must show the site's Cloudflare account. IndexNow is automatic (own key per site; never copy build/.indexnow_key).

## Link targets (content.py, custom sections)
`#slots` etc = home section of that language · `@register @login @app @chat` = config URLs (rendered sponsored/nofollow, new tab) · `/path/` = internal.
Posts: `[[target|anchor]]`, target = post slug, `home`, `home#<id>`, `blog`. Unknown target = build error (intended).
Blog groups: CLUSTERS in build/posts.py.

## Tokens
`__BRAND__ __SLUG__ __TAGLINE__` everywhere; `__SITE_URL__ __EMAIL_LINE__` in pages.py. Leftover `__X__` tokens fail the build.

## Rules
- Don't invent facts: no licences, bonus %, minimums, payout times, odds or win feeds unless the brief supplies them.
- MATCHES must be real fixtures (no odds); leave [] otherwise. PROMOS only real current offers.
- Keep 18+, Talian Kasih 15999, footer disclaimer and "T&Cs apply" on promos.
- CSS is inlined from assets/style.css; main.js is cache-busted automatically.

## Standing rules for every site (user's requirements — always apply)
1. **Local language is the main language.** Malaysia = Bahasa Melayu at `/`; other languages are secondary. Write new copy, posts and policies in the main language first.
2. **Meta title, description and keywords on every page.** Title <= 65 chars, description 70-165 chars (the build prints `meta:` warnings — fix them all). Keywords come from the user's keyword list.
3. **Popup:** phone-size 9:16 image (`images/src/popup.*`, 540x960), opens ~1.5 s after load and again 30 s after every close, links to the register URL. No image = styled fallback card.
4. **Floating footer** with Login + Register on every page.
5. **Inspiration website:** when the user names a site for inspiration, fetch it first (curl; if blocked, headless Chrome screenshot) and carry its colours into THEME and its section ideas into custom sections/copy. Never copy its logo, brand name or text.
6. **Blog = topical authority.** Clusters = `CLUSTERS` in build/posts.py (`pillar` slug per cluster); each post has `cluster`. One pillar per cluster + 2-6 supporting posts. Supporting -> pillar, pillar -> every supporting post, every post -> at least one other cluster and one home section, no orphans. The build prints `cluster:` warnings — fix them all before deploying.
7. **Internal linking across pages:** home guides section, footer, blog hub, post sidebars and policy pages all link pillars; keep it that way when adding pages.

## From keywords to site (the normal way a new site is requested)
The user gives: brand + domain + links, a **keyword list**, and usually an **inspiration website**. NEW_SITE_BRIEF.md is optional/manual — fill it in yourself from what the user gave, as the record for the site.
1. Copy the template + `./deploy.sh clean` (see workflow above).
2. Group the keywords by search intent -> 3-6 clusters. Head term of each group = pillar post; long-tail terms = supporting posts (one focus keyword each, in `kw`).
3. Put the top 6-10 keywords in `KEYWORDS` (site_config.py); use the head terms in the home title/description.
4. Write the posts in the main language (build/posts.py), following the link rules in 6. Replace the starter posts; don't keep posts for keywords the user didn't give.
5. Apply the inspiration site (rule 5), build, fix every `meta:` and `cluster:` warning, then deploy.
