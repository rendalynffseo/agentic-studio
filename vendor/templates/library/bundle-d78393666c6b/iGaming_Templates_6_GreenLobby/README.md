# iGaming_Templates_6_GreenLobby

A green-and-yellow casino lobby for a Malaysian iGaming brand (layout inspired by mrcoin88a.com), built on the Template 4 engine.
**Bahasa Melayu is the default language**; every page also has an English translation at `/en/`. 72 pages out of the box.

## What you get
- Two-row green header (logo bar + nav bar with live GMT+8 clock and BM/EN switch), mobile app-download strip
- Home: 900x500 banner on a green stage, scrolling announcement, H1 hero with wallet preview card, category icon strip,
  Recommended Games tabs (featured provider + provider grid), Top Picks and Casino Hits rows, invite-a-friend card,
  app box with phone mock and feature tiles, promotions, 3 steps, guides by topic, FAQ, latest guides
- 10 game pages (casino hub, slots, live casino, sports, esports, crash, fishing, cards, lottery, instant win), app, promotions,
  VIP (tier cards), refer-a-friend, affiliate, 6 policy pages, contents page
- Blog: 4 topic clusters (pillar + supporting posts), 12 guides per language, cluster boxes and cross-links everywhere
- SEO: per-page meta title/description/focus keyword/keywords, hreflang (ms-MY default, en-MY), sitemap with alternates, schema, llms.txt
- Build checks: lengths, focus keyword placement, one H1, cluster links, orphans, broken links
- 9:16 popup every 30 s after close, floating Login/Register footer, generated logo + favicons, self-hosted Montserrat
- Square images (banner, popup and og excepted); complete with no images (letter tiles and styled fallbacks)

## Make a new site
1. Copy this folder, rename it to the domain, and run `./deploy.sh clean` in the copy.
2. Give Claude the brand, links, keyword list and an inspiration site (or fill in `NEW_SITE_BRIEF.md`).
3. `build/site_config.py` → text in `build/content.py`, `build/pages.py`, `build/posts.py`.
4. Images in `images/src/` → `python3 build/images.py`; logo/favicons → `python3 build/icons.py`.
5. `./deploy.sh build` (fix all warnings) → `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.

| You want to… | Edit |
|---|---|
| Brand, links, logo, announcement, game tabs, game rows, promos, VIP tiers, colours | `build/site_config.py` |
| Home, menu, footer, popup and banner text | `build/content.py` |
| Game, info, VIP and policy pages | `build/pages.py` |
| Blog clusters and posts | `build/posts.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3`), a Cloudflare account.
