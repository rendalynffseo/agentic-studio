# iGaming_Templates_10_RoseLounge

A cream, rose/pink casino lounge with a dark maroon sports band (design and page set inspired by mrgroup44.win), on the
Templates_4 engine. **Bahasa Melayu is the default**; every page has an English translation at `/en/`. 80 pages out of the box.

## What you get
- Home: 900x500 banner, rose gradient hero with H1, stats strip, 8 "why choose" cards, about, deposit & withdrawal with
  payment chips, dark sports band with 6 sport cards, live casino, app (icon list + Android/iOS buttons), bingo & winners,
  game category grid, promotions, responsible gaming cards, guides by topic, FAQ, latest guides, privacy callout
- Pages: casino hub, slots, bingo, live casino, sports, esports, fishing, card games, lottery, instant win, app, promotions,
  affiliate, deposit, withdrawal, winners, FAQ, register, login, about, contact, responsible gaming, privacy, terms, disconnect policy
- Blog: 4 topic clusters (pillar + supporting posts), 12 guides per language, cluster boxes and cross-links everywhere
- SEO: per-page meta title, description, focus keyword, keywords; hreflang (ms-MY default, en-MY); sitemap with alternates; schema; llms.txt
- Build checks: title/description length, focus keyword placement, one H1 per page, cluster links, orphan posts, unknown links
- 9:16 popup every 30 s after close, floating yellow/green Register/Login footer, floating language pill, generated logo + favicons, self-hosted Nunito
- Square images everywhere (banner 900x500, popup 9:16 and og excepted); looks complete with no images

## Make a new site
1. Copy this folder, rename it to the domain, and run `./deploy.sh clean` in the copy.
2. Give Claude the brand, links, keyword list and an inspiration site (or fill in `NEW_SITE_BRIEF.md`).
3. `build/site_config.py` → text in `build/content.py`, `build/pages.py`, `build/posts.py`.
4. Images in `images/src/` → `python3 build/images.py`; logo/favicons → `python3 build/icons.py`.
5. `./deploy.sh build` (fix all warnings) → `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.

| You want to… | Edit |
|---|---|
| Brand, links, logo, promos, stats, winners, payments, colours | `build/site_config.py` |
| Home, menu, footer, popup and banner text | `build/content.py` |
| Game, account, money and policy pages | `build/pages.py` |
| Blog clusters and posts | `build/posts.py` |
| Extra home block | `build/custom_sections.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3`), a Cloudflare account.
