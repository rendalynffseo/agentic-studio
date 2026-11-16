#!/bin/zsh
# Build the site, deploy it to Cloudflare Pages, then ping IndexNow.
#   ./deploy.sh          build + deploy + IndexNow
#   ./deploy.sh build    build only (output in dist/)
set -e
cd "$(dirname "$0")"

python3 build/build.py
KEY=$(python3 build/indexnow.py key)   # one key per site, created on first build (build/.indexnow_key)
rm -rf dist && mkdir dist
[ -f favicon.ico ] || python3 build/icons.py
cp -R index.html blog assets sitemap.xml robots.txt favicon.svg favicon.ico favicon-48.png favicon-192.png apple-touch-icon.png site.webmanifest _headers "$KEY.txt" dist/
mkdir -p dist/images && rsync -a --exclude src --exclude '.DS_Store' images/ dist/images/
find dist -name .DS_Store -delete
echo "dist/ ready ($(du -sh dist | cut -f1))"

[[ "$1" == "build" ]] && exit 0

PROJECT=$(python3 -c "import sys; sys.path.insert(0,'build'); import site_config as c; print(c.CF_PROJECT)")
npx --yes wrangler@3 whoami | grep -i email
npx --yes wrangler@3 pages project create "$PROJECT" --production-branch main 2>/dev/null || true
npx --yes wrangler@3 pages deploy dist --project-name "$PROJECT" --branch main --commit-dirty=true
sleep 5
python3 build/indexnow.py submit || echo "IndexNow submit failed (site still deployed); retry: python3 build/indexnow.py submit"
