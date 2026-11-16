# iGaming_Templates_7_GreenLobby

A green, 3-column casino lobby dashboard for a Malaysian iGaming brand (design and page set inspired by mrmart88.com).
**Bahasa Melayu is the default language**; every page also has an English translation at `/en/`. 74 pages out of the box.

## What you get
- App-download strip, green header with dropdowns, marquee ticker, 900x500 banner above the dashboard
- Home dashboard: quick facts, lucky-pick spinner and providers (left); H1 hero, category tabs, game search and square game tiles
  with PLAY buttons (centre); login/register, account card, referral, lucky draw and game tips cards (right)
- Article sections below: overview table, why us, free credit table, zero-turnover rebate, game categories, banking, mobile, how to claim, support, FAQ
- Important pages: games hub + 6 game pages, promotions, free credit, VIP, referral, lucky draw, app, help centre (FAQ), about, contact,
  responsible gaming, privacy, terms, contents
- Blog: 5 topic clusters (start, free credit, payments, casino, sports), 15 guides per language, cluster boxes and cross-links everywhere
- SEO: per-page meta title, description, focus keyword and keywords; hreflang (ms-MY default, en-MY), sitemap with alternates, schema, llms.txt
- Build checks: lengths, focus keyword placement, one H1 per page, cluster links, orphan posts, broken links
- Phone-size (9:16) popup every 30 s after close; floating Login/Register footer (desktop) and tab bar (mobile)
- Square images everywhere (banner, popup and og excepted); looks complete with no images (letter tiles + icon fallbacks)

## Make a new site
1. Copy this folder, rename it to the domain, and run `./deploy.sh clean` in the copy.
2. Give Claude the brand, links, keyword list and an inspiration site (or fill in `NEW_SITE_BRIEF.md`).
3. `build/site_config.py` → text in `build/content.py`, `build/pages.py`, `build/posts.py`.
4. Images in `images/src/` → `python3 build/images.py`; logo/favicons → `python3 build/icons.py`.
5. `./deploy.sh build` (fix all warnings) → `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.

| You want to… | Edit |
|---|---|
| Brand, links, games, offers, facts, colours | `build/site_config.py` |
| Menu, tabs, widgets, home text | `build/content.py` |
| Game, reward, help and policy pages | `build/pages.py` |
| Blog clusters and posts | `build/posts.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3`), a Cloudflare account.
