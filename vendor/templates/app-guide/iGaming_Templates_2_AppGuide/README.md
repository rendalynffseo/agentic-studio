# iGaming_Templates_2_AppGuide

An "independent app guide" site for iGaming brands in Malaysia: dark ink and gold design, trustworthy review style,
Bahasa Melayu home page (main, local language) plus English (`/en/`) and 中文 (`/zh/`) versions.
Live example: https://mega88mobi.com

## What you get (the same on every site)
- Home: 18+ disclosure bar, promo banner, hero with square promo, overview, features, safe-install steps + permissions table,
  games table, safety cards, FAQ, sticky sidebar (table of contents, quick facts, CTA), CTA band, full footer
- Blog built for topical authority: 4 topic clusters (pillar + supporting posts, 12 BM starter guides) with automatic cluster links, plus a `/games/` hub
- Phone-size popup (9:16) that reappears 30 s after closing, floating Login/Register footer
- Meta title, description and keywords on every page; the build warns about lengths, missing pillar links and orphan posts
- Author page and 7 policy pages (about, affiliate disclosure, privacy, responsible gaming, support, disclaimer, AI overview), contents page, 404
- SEO: schema (Organization, Person, WebSite, WebPage, SoftwareApplication, FAQPage, BlogPosting, Breadcrumbs), hreflang, sitemap, robots.txt, llms.txt
- IndexNow on every deploy; GA4 loads only after first interaction (fast PageSpeed)

## Make a new site
1. **Copy** this folder, rename it to the new domain and run `./deploy.sh clean` in the copy.
2. **Fill in** `NEW_SITE_BRIEF.md` (hand it to Claude or a developer).
3. **Settings:** `build/site_config.py`.
4. **Images:** put `banner`, `promo`, `author`, `og` in `images/src/` → `python3 build/images.py`. **Logo:** `python3 build/icons.py`.
5. **Check:** `./deploy.sh build`, then `python3 -m http.server 8000 --directory dist` and open http://localhost:8000
6. **Deploy:** `./deploy.sh`, then add the domain in Cloudflare → Workers & Pages → project → Custom domains.

## Where to customise
| You want to… | Edit |
|---|---|
| Brand, links, author, address, languages, colours | `build/site_config.py` |
| Home page / menu / footer wording | `build/content.py` |
| Blog posts | `build/posts.py` |
| Author bio sections, policy pages, hub intros | `build/pages.py` |
| Extra promo block or sidebar widget | `build/custom_sections.py` |

Requirements: Python 3, Pillow (`pip3 install pillow`), Node (for `npx wrangler@3`), a Cloudflare account.
