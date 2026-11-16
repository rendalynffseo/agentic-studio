# iGaming_Templates_11_NeonTeal

A dark navy + teal neon casino portal for a Malaysian iGaming brand (design, home sections and page set inspired by kingroup88.net).
**Bahasa Melayu is the default language**; every page also has an English translation at `/en/`. 84 pages out of the box.

## What you get
- Home: marquee ticker, 900x500 banner above the hero, neon hero, trust bar, stats bar, promo carousel, game wall with hover
  overlay, sports markets, step cards, advantage cards, comparison table, app section with phone mockup, membership tiers,
  guides by topic, SEO text, states served, FAQ, latest guides
- Casino hub + slots, poker, table games, jackpot, fishing, lottery, instant win; live casino, sports, esports
- Welcome bonus, promotions, VIP membership, register, login, betting tips, FAQ page, app, affiliate, 6 policy pages, contents
- Blog: 4 topic clusters (pillar + supporting posts), 13 guides per language, cluster boxes and cross-links everywhere
- SEO: per-page meta title, description, focus keyword and keywords; hreflang (ms-MY default, en-MY), sitemap with alternates, schema, llms.txt
- Build checks: title/description length, focus keyword placement, one H1 per page, cluster links, orphan posts
- 9:16 popup every 30 s after close, floating Login/Register footer, generated logo + favicons, square images, IndexNow

## Make a new site
1. Copy this folder, rename it to the domain, and run `./deploy.sh clean` in the copy.
2. Give Claude the brand, links, keyword list and an inspiration site (or fill in `NEW_SITE_BRIEF.md`).
3. `build/site_config.py` → text in `build/content.py`, `build/pages.py`, `build/posts.py`.
4. Images in `images/src/` → `python3 build/images.py`; logo/favicons → `python3 build/icons.py`.
5. `./deploy.sh build` (fix all warnings) → `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.

| You want to… | Edit |
|---|---|
| Brand, links, logo, promos, ticker, stats, matches, colours | `build/site_config.py` |
| Home sections, menu, footer, tiers, popup and banner text | `build/content.py` |
| Game, bonus, info and policy pages | `build/pages.py` |
| Blog clusters and posts | `build/posts.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3`), a Cloudflare account.
