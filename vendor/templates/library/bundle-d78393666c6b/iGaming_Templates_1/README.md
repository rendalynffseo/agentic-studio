# iGaming_Templates_1

A ready-made landing site + blog for iGaming brands in Malaysia. Bahasa Melayu by default, with an English toggle.
Live example: https://ra88.lol

## What you get (the same on every site)
- Home page: promo banner, hero, slot showcase, 18 game tiles, live transactions, platform preview, features, 4-step sign-up, FAQ
- Floating CTA bar (Login / Register / WhatsApp) and a phone-size (9:16) popup banner that reappears 30 seconds after closing
- Blog with 21 bilingual FAQ guides in 6 topic clusters (one pillar each, `PILLARS` in build.py), cluster boxes on every post, internal links between posts and the home page
- Meta title, description and keywords on every page (`KEYWORDS` in site_config.py); the build warns about lengths, missing pillar links and orphan posts
- SEO: schema (Organization, WebSite, FAQPage, BlogPosting, Breadcrumbs), sitemap, robots.txt, canonical + Open Graph tags
- IndexNow: every deploy pings Bing/Yandex/Naver with all URLs (own key per site, created automatically)
- Speed: inlined CSS, self-hosted font, WebP images, cache headers

**The structure stays the same for every site.** What changes per site: the settings, the images, the colours (site inspiration) and any extra sections the developer adds.

## Make a new site in 6 steps
1. **Copy** this folder and rename it to the new domain, e.g. `newbrand.com`.
2. **Fill in** `NEW_SITE_BRIEF.md` (optional, but it's what you hand to Claude or a developer).
3. **Settings:** edit `build/site_config.py` (brand, domain, CTA link, min deposit/withdraw, Cloudflare project, game list, colours).
4. **Icons:** run `python3 build/icons.py` to make the favicons and square logo from your logo text.
5. **Images:** put raw images in `images/src/`, then run `python3 build/images.py`
   - `popup-banner`: portrait promo (shown in the popup)
   - `showcase-1`, `showcase-2`: banner + games screenshot
   - `showcase-3`: live transactions strip
   - `preview`: full platform screenshot
   - `games/<name>`: square game tiles (names must match the GAMES list)
6. **Deploy:** `./deploy.sh` (or `./deploy.sh build` to check locally first). It also submits all URLs to IndexNow after the deploy. Then add the domain in Cloudflare → Workers & Pages → project → Custom domains.

## Where to customise
| You want to… | Edit |
|---|---|
| Change brand, links, numbers | `build/site_config.py` |
| Change colours to match a reference site | `THEME` in `build/site_config.py` |
| Add a promo block or extra section | `build/custom_sections.py` |
| Change images | `images/src/` → `python3 build/images.py` |
| Edit blog posts | `build/posts_1.py`, `posts_2.py`, `posts_3.py` |
| Change hero / banner wording | `home()` / `top_banner()` in `build/build.py` |

Never edit `index.html` or `blog/` directly; they are regenerated on every build.
When copying the template for a new site, don't copy `build/.indexnow_key` from another site; a fresh key is created on the first build.

## Requirements
Python 3, Pillow (`pip3 install pillow`), Node (for `npx wrangler@3`), a Cloudflare account.
