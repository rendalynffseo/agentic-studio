# iGaming_Templates_5_TealGlow

A dark teal casino lobby with teal→gold gradient headings for a Malaysian iGaming brand (design and page set inspired by jomtekan44.app),
built on the Templates_4 engine. **Bahasa Melayu is the default language**; every page also has an English translation at `/en/`. 88 pages out of the box.

## What you get
- Home: 900x500 banner, gradient hero with live card, sticky "Sections" chip bar, popular-game cards, lobby split, studios grid,
  numbered offers carousel, reward cards, local wallet cards, 5 numbered steps, account areas + app card, check cards, guides by topic,
  contact cards, numbered FAQ
- Popular-games hub + 6 game review pages (quick-facts table), casino hub + 8 categories, login, register, FAQ (all answers), legal hub,
  app, promotions, affiliate, 6 policy pages, contents page
- Blog: 4 topic clusters (pillar + supporting posts), 12 guides per language, cluster boxes and cross-links everywhere
- SEO: per-page meta title, description, focus keyword and keywords; hreflang (ms-MY default, en-MY), sitemap with alternates,
  schema (Organization, WebSite, WebPage, CollectionPage, BlogPosting, FAQPage, Breadcrumbs), llms.txt
- Build checks: title/description length, focus keyword placement, one H1 per page, cluster links, orphan posts, broken links
- Phone-size (9:16) popup every 30 s after close, floating Login/Register footer, back-to-top, generated logo + favicons, self-hosted Poppins font
- Square images everywhere (banner 900x500, popup 9:16 and og excepted); looks complete with no images at all

## Make a new site
1. Copy this folder, rename it to the domain, and run `./deploy.sh clean` in the copy.
2. Give Claude the brand, links, keyword list and an inspiration site (or fill in `NEW_SITE_BRIEF.md`).
3. `build/site_config.py` → text in `build/content.py`, `build/pages.py`, `build/posts.py`.
4. Images in `images/src/` → `python3 build/images.py`; logo/favicons → `python3 build/icons.py`.
5. `./deploy.sh build` (fix all warnings) → `python3 -m http.server 8000 --directory dist` → `./deploy.sh`.

| You want to… | Edit |
|---|---|
| Brand, links, logo text, promos, payments, colours | `build/site_config.py` |
| Home, menu, footer, popup and banner text | `build/content.py` |
| Game, info and policy pages | `build/pages.py` |
| Blog clusters and posts | `build/posts.py` |
| Extra home block | `build/custom_sections.py` |

Requirements: Python 3, Pillow, Node (for `npx wrangler@3`), a Cloudflare account.
