# iGaming_Templates_1 · Claude instructions

Bilingual (BM default + EN) iGaming landing site + 21-post FAQ blog, full schema, deployed to Cloudflare Pages.
Reference build: https://ra88.lol (RA88). Python 3 + Pillow; deploy uses `npx wrangler@3`.

## Golden rule: the STRUCTURE IS FIXED
Every site made from this template keeps the same structure:
- Pages: home, /blog/ (grouped by topic), 21 blog posts (same slug pattern, `-__SLUG__` brand part), sitemap.xml, robots.txt
- Home section order: top banner (1200x100 SVG) → hero → slot showcase → game tiles → live transactions → platform preview → features → 4-step join → FAQ → key guides
- Floating CTA bar, popup (reopens 30s after close), BM/EN toggle, footer with 18+ notice
- Schema, internal-link system, performance setup (inlined CSS, self-hosted font, WebP, popup = LCP preloaded)
- Blog post content in posts_1/2/3.py (brand-neutral via tokens)

What a new developer CHANGES per site (and only this, unless the user asks for more):
1. `build/site_config.py`: brand, slug, logo, domain, CTA links, min deposit/withdraw, date, GSC_VERIFICATION, CF project, KEYWORDS, GAMES, THEME colours
   Then `python3 build/icons.py` (favicons + 512px schema logo from LOGO_A/LOGO_B).
2. Images in `images/src/` → `python3 build/images.py`
3. Site inspiration: THEME colours in site_config; copy tweaks to hero/banner text in `build/build.py` (`home()`, `top_banner()`) only if the brief asks
4. Extra content: `build/custom_sections.py` (AFTER_HERO, BEFORE_FAQ, EXTRA_CSS). Never restructure build.py to add sections.

## New site workflow (token-cheap: don't re-read build.py unless needed)
1. Copy this folder to `../<domain>/`. Read `NEW_SITE_BRIEF.md` if the user filled it in.
2. Edit `build/site_config.py`.
3. Images → `images/src/` (names in `build/images.py` docstring) → `python3 build/images.py`. Game tiles: `images/src/games/<slug>.*`, slugs must match GAMES.
4. `./deploy.sh build` → check `dist/` (`cd dist && python3 -m http.server 8000`) → `./deploy.sh`.
5. IndexNow is automatic: deploy.sh creates the site's own key (build/.indexnow_key + <key>.txt in root) and submits sitemap URLs after deploy. Never copy .indexnow_key between sites. Manual resubmit: `python3 build/indexnow.py submit`.
6. Before deploying: `npx wrangler@3 whoami` must show the site's Cloudflare account; otherwise `npx wrangler@3 login`.
7. Domain: zone in Cloudflare, nameservers at registrar → Pages project → Custom domains (apex + www) → CNAME `@` and `www` → `<project>.pages.dev`, proxied.

## Tokens (replaced at write time, work in f-strings and plain strings)
`__BRAND__ __SLUG__ __LOGO_A__ __LOGO_B__ __MIN_DEPOSIT__ __MIN_WITHDRAW__`

## Internal links
In post text: `[[target|anchor]]`. target = post slug (with `__SLUG__`), `home`, `home#<section-id>`, or `blog`. Unknown target = build error (intended).
Not inside FAQ answers (they feed FAQPage schema). Blog categories: CATS in build.py; each post has `cat`.

## Rules
- Never edit generated HTML (index.html, blog/); edit build files and rebuild.
- Don't invent facts in copy (fees, processing times, licences, bonus %). Keep 18+/responsible gaming lines.
- If CSS/JS changes, bump `?v=` on main.js in `page()`.
- Every <img> needs alt (use `bi_alt(ms, en)`), width, height; lazy unless above the fold.

## Standing rules for every site (user's requirements — always apply)
1. **Local language is the main language.** Malaysia = Bahasa Melayu at `/`; other languages are secondary. Write new copy, posts and policies in the main language first.
2. **Meta title, description and keywords on every page.** Title <= 65 chars, description 70-165 chars (the build prints `meta:` warnings — fix them all). Keywords come from the user's keyword list.
3. **Popup:** phone-size 9:16 image (`images/src/popup-banner.*`, 540x960), opens ~1.5 s after load and again 30 s after every close, links to the register URL. No image = styled fallback card.
4. **Floating footer** with Login + Register on every page.
5. **Inspiration website:** when the user names a site for inspiration, fetch it first (curl; if blocked, headless Chrome screenshot) and carry its colours into THEME and its section ideas into custom sections/copy. Never copy its logo, brand name or text.
6. **Blog = topical authority.** Clusters = `CATS` in build/build.py, pillar of each = `PILLARS`; posts in build/posts_1/2/3.py (`cat`). One pillar per cluster + 2-6 supporting posts. Supporting -> pillar, pillar -> every supporting post, every post -> at least one other cluster and one home section, no orphans. The build prints `cluster:` warnings — fix them all before deploying.
7. **Internal linking across pages:** home guides section, footer, blog hub, post sidebars and policy pages all link pillars; keep it that way when adding pages.

## From keywords to site (the normal way a new site is requested)
The user gives: brand + domain + links, a **keyword list**, and usually an **inspiration website**. NEW_SITE_BRIEF.md is optional/manual — fill it in yourself from what the user gave, as the record for the site.
1. Copy the template + `./deploy.sh clean` (see workflow above).
2. Group the keywords by search intent -> 3-6 clusters. Head term of each group = pillar post; long-tail terms = supporting posts (one focus keyword each, in `kw`).
3. Put the top 6-10 keywords in `KEYWORDS` (site_config.py); use the head terms in the home title/description.
4. Write the posts in the main language (build/posts_1.py, posts_2.py, posts_3.py; BM `ms` block first, `en` block second), following the link rules in 6. Replace the starter posts; don't keep posts for keywords the user didn't give.
5. Apply the inspiration site (rule 5), build, fix every `meta:` and `cluster:` warning, then deploy.
