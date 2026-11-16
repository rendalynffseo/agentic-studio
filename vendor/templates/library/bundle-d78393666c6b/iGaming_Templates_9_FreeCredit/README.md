# iGaming_Templates_9_FreeCredit

A free-credit slot casino site for a Malaysian brand (layout and page set inspired by ekplus8.pro), built on the
Templates_4 engine. **Bahasa Melayu is the default language**; every page has an English translation at `/en/`. 70 pages out of the box.

## What you get
- Dark charcoal nav with yellow active links and dropdowns; header band with a 900x500 banner and wide gold LOGIN / teal REGISTER buttons
- Home: square promo grid, game tiles, provider free-credit tiles, long-form article with an overview table, free credit table,
  provider guide table, payments, how to join, member features, guides by topic, FAQ, explore links
- 5 game pages, a free credit hub plus one free-credit guide per slot provider (generated from config), promo, app
- Brand/policy pages: about, mission & core values, security system, protection policy, responsible gambling, contact, privacy, terms
- Blog: 3 topic clusters (free credit, slots, account & payments), 9 guides per language, cluster boxes and cross-links
- SEO: per-page meta title/description/focus keyword/keywords, hreflang (ms-MY default, en-MY), sitemap with alternates, schema, llms.txt
- Build checks: meta lengths, focus keyword placement, one H1 per page, cluster links, orphan posts, broken links
- 9:16 popup every 30 s after close, floating Login/Register bar, generated logo + favicons, self-hosted Lato font
- Square images everywhere (banner, popup and og excepted); looks complete with no images

## Make a new site
1. Copy this folder, rename it to the domain, and run `./deploy.sh clean` in the copy.
2. Give Claude the brand, links, keyword list and an inspiration site (or fill in `NEW_SITE_BRIEF.md`).
3. `build/site_config.py` (incl. OVERVIEW, FREE_CREDITS, FC_PROVIDERS) → text in `build/content.py`, `build/pages.py`, `build/posts.py`.
4. Images in `images/src/` → `python3 build/images.py`; logo/favicons → `python3 build/icons.py`.
5. `./deploy.sh build` (fix all warnings) → `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.

| You want to… | Edit |
|---|---|
| Brand, links, offers, overview facts, providers, colours | `build/site_config.py` |
| Home, menu, footer, popup and banner text | `build/content.py` |
| Game, free-credit and policy pages | `build/pages.py` |
| Blog clusters and posts | `build/posts.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3`), a Cloudflare account.
