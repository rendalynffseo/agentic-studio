# iGaming_Templates_2_AppGuide · Claude instructions

"Independent app guide / review" site: dark ink + gold, main column + sticky sidebar, EN/BM/中文 home pages,
blog + games hub, author page (E-E-A-T), policy pages, full schema. Deployed to Cloudflare Pages.
Reference build: https://mega88mobi.com. Python 3 + Pillow; deploy uses `npx wrangler@3`.

## Golden rule: the STRUCTURE IS FIXED
- Pages: `/` (BM) + `/en/` + `/zh/`, `/blog/`, `/blog/<slug>/`, `/games/`, `/about-author/`, policy pages
  (`/about/ /affiliate-disclosure/ /privacy-policy/ /responsible-gaming/ /support/ /disclaimer/ /ai-overview/`), `/contents/`, 404, sitemap.xml, robots.txt, llms.txt
- Home order: 18+ disclosure bar → header (menu, lang switch, Register) → promo banner → hero (+ square promo) →
  main [about, features, install (steps + permissions table), games table, safety, FAQ] + sidebar [TOC, quick facts, CTA, 18+] → CTA band → footer
- Everything builds into `dist/` (wiped each build). Never edit dist/.

## What changes per site (only this, unless the user asks for more)
1. `build/site_config.py`: brand, SITE_NAME, domain, REGISTER_URL, LANGS, AUTHOR, ADDRESS/PHONE/MAP, dates, verification + GA4, CF_PROJECT, QUICK_FACTS, THEME
2. Images in `images/src/` (banner, promo, author, og; all optional) → `python3 build/images.py`
3. Logo/favicons: `python3 build/icons.py` (from LOGO_TEXT + THEME gold)
4. Site inspiration: THEME tokens (keep `gold-rgb` in sync with `gold`). Text tweaks: `build/content.py` (home, per language)
5. Extra blocks: `build/custom_sections.py` (AFTER_HERO, BEFORE_FAQ, SIDEBAR, EXTRA_CSS). Don't restructure build.py.

## New site workflow (token-cheap: DON'T read build.py, content.py or posts.py unless the task needs it)
1. `cp -R iGaming_Templates_2_AppGuide ../<domain>` then in the copy run `./deploy.sh clean` (removes the old site's build, key and images)
2. Read `NEW_SITE_BRIEF.md` if filled in → edit `build/site_config.py` only.
3. Images → `images/src/` → `python3 build/images.py`; `python3 build/icons.py`.
4. `./deploy.sh build` → preview `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.
5. Before deploy: `npx wrangler@3 whoami` must show the site's Cloudflare account (else `npx wrangler@3 login`).
6. IndexNow automatic (own key per site in build/.indexnow_key; never copy between sites). Resubmit: `python3 build/indexnow.py submit`.
7. Domain: zone in Cloudflare → Pages project → Custom domains (apex + www).

## Tokens (replaced at write time, everywhere)
`__BRAND__ __SITE__ __SLUG__ __AUTHOR__ __EMAIL__ __DOMAIN__`; `__ALT_NOTE__` (home only, from BRAND_ALT).

## Content files
- `content.py`: UI (nav, footer, disclaimers) + HOME, per lang. Section ids are fixed. FAQ answers plain text (FAQPage schema).
- `pages.py`: blog/games hub intros, author page, POLICIES — written in the main language (BM).
- `posts.py`: CLUSTERS + POSTS (`cluster`, `kw` list). GAMES_CLUSTER is also listed on /games/.
  Links: `[[target|anchor]]`, target = post slug, `home`, `home#<id>`, `blog`, `games`. Unknown target = build error (intended).
- Adding a language: add UI + HOME entries in content.py, QUICK_FACTS in site_config, then add the code to LANGS.

## Rules
- Don't invent facts (fees, payout times, licences, RTP numbers, bonus %). Keep 18+ / helpline lines and affiliate disclosure.
- AUTHOR and ADDRESS must be real for the new site; ADDRESS = [] hides address + map.
- Register links: `rel="nofollow sponsored noopener"`. Every <img>: alt + width/height (build reads images/sizes.json).
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
