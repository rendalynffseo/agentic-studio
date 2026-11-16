# iGaming Template 12 · Red Gold Guide

Educational, fact-safe guide site in Bahasa Melayu (black, warm charcoal, red and gold). Built from eu9slots.com.

```bash
./deploy.sh build    # npm install if needed, generate images, build dist/ (noindex) and preview/ (with drafts)
npm run serve        # http://localhost:4173 with real 404s (add -- --preview for drafts)
./deploy.sh check    # production build + launch checks + external source links
./deploy.sh          # production build, checks, deploy to Cloudflare Pages (cfProject in src/config.js)
./deploy.sh clean    # remove dist/, preview/, generated images, node_modules
```

- Content inventory: `src/inventory.js` (6 clusters, 30 articles, published/draft) · bodies: `src/articles/NN.html`
- Settings: `src/config.js` · disclosure wording: `src/relationship.js` · info pages: `src/pages.js`
- Optional owner images: `assets-src/owner/` (logo.png, hero-banner.png, popup.png, screenshots) then `./deploy.sh images`
- `npm run inventory` writes CONTENT-INVENTORY.md / content-inventory.csv

See CLAUDE.md for the full workflow and conventions.
