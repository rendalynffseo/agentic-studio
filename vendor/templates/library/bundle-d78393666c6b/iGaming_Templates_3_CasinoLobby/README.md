# iGaming_Templates_3_CasinoLobby

A casino-lobby landing site for an iGaming brand in Malaysia. Page sections follow bk8masd.com; the look follows modern
crypto-casino lobbies: dark navy, a fixed left sidebar, blue/green buttons, portrait game tiles in swipeable rows,
and a bottom tab bar on mobile. Bahasa Melayu home page (main, local language) plus English (`/en/`) and 中文 (`/zh/`).

## What you get
- Home: welcome hero with Casino/Sports cards, banner carousel, news ticker, category chips, 4 game rows,
  optional upcoming matches, How to Register, promotions, app download, providers & payments, long SEO article with "Read more", FAQ
- Blog built for topical authority: 3 topic clusters (pillar + supporting posts, 9 BM starter guides), guides section on home, 4 BM policy pages, contents page, 404
- Phone-size popup (9:16) that reappears 30 s after closing; floating Login/Register footer (desktop) and tab bar (mobile)
- Meta title, description and keywords on every page; the build warns about lengths, missing pillar links and orphan posts
- Schema (Organization, WebSite, WebPage, FAQPage, BlogPosting, Breadcrumbs), hreflang, sitemap, robots.txt, llms.txt
- IndexNow on every deploy; GA4 loads after first interaction
- Looks complete with **no images**: game tiles fall back to coloured letter tiles

## Make a new site
1. Copy this folder, rename to the new domain and run `./deploy.sh clean` in the copy.
2. Fill in `NEW_SITE_BRIEF.md`.
3. Edit `build/site_config.py` (brand, links, games, promos, colours).
4. Optional images in `images/src/` → `python3 build/images.py`; then `python3 build/icons.py`.
5. `./deploy.sh build` → `python3 -m http.server 8000 --directory dist` → check http://localhost:8000
6. `./deploy.sh`, then add the domain in Cloudflare → Workers & Pages → Custom domains.

| You want to… | Edit |
|---|---|
| Brand, links, games, promos, providers, colours | `build/site_config.py` |
| Home / menu / footer wording, SEO article, FAQ | `build/content.py` |
| Blog posts | `build/posts.py` |
| Policy pages, blog intro | `build/pages.py` |
| Extra block on the home page | `build/custom_sections.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3`), a Cloudflare account.
