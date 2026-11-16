# iGaming_Templates_13_SkyGlow

An eye-catching navy + sky-blue glow casino site for a Malaysian iGaming brand (design inspired by a66slot.pro),
built for **PageSpeed 100** and **entity SEO**. Bahasa Melayu is the default language; every page also has an English
translation at `/en/`. 68 pages out of the box.

## What you get
- Home: glowing dark hero band with a 900x500 banner, H1 and square art; stats band; 8 feature cards; game category grid;
  slot/live cards; desktop-vs-app comparison table; bingo & sports; MYR payments chips; promotions; app; 3 steps;
  responsible gaming; "we serve all of Malaysia"; guides by topic; FAQ; latest guides
- 9 game pages, app (SoftwareApplication schema), promotions, affiliate, **glossary** (DefinedTermSet), 6 policies, contents
- Blog: 4 topic clusters (pillar + supporting posts), 12 guides per language, cluster boxes and cross-links everywhere
- SEO: per-page high-CTR meta title/description, focus keyword, keywords; hreflang (ms-MY default + x-default, en-MY);
  connected JSON-LD (Organization + Brand + WebSite on every page, WebPage/CollectionPage with about/mentions → Wikipedia,
  ItemList, FAQPage, BlogPosting, BreadcrumbList); sitemap with alternates; llms.txt; IndexNow
- Build checks: meta length, focus keyword placement, one H1, cluster links, orphan posts
- Phone-size 9:16 popup (loads on demand, reopens 30 s after close), floating Login/Register banner, generated logo + favicons
- Lighthouse 12: 100 / 100 / 100 / 100 on mobile and desktop (home, category, post, glossary, app — with and without images)

## Make a new site
1. Copy this folder, rename it to the domain, and run `./deploy.sh clean` in the copy.
2. Give Claude the brand, links, keyword list and an inspiration site (or fill in `NEW_SITE_BRIEF.md`).
3. `build/site_config.py` → text in `build/content.py`, `build/pages.py`, `build/posts.py`.
4. Images in `images/src/` → `python3 build/images.py`; logo/favicons → `python3 build/icons.py`.
5. `./deploy.sh build` (fix all warnings) → preview + Lighthouse → `./deploy.sh`.

| You want to… | Edit |
|---|---|
| Brand, links, entities, social profiles, stats, promos, colours | `build/site_config.py` |
| Home, menu, footer, popup and banner text | `build/content.py` |
| Game, info, glossary and policy pages | `build/pages.py` |
| Blog clusters and posts | `build/posts.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3` and Lighthouse), a Cloudflare account.
