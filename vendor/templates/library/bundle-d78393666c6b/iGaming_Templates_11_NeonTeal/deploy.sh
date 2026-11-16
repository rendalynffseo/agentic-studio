#!/bin/zsh
# Build the site into dist/, deploy it to Cloudflare Pages, then ping IndexNow.
#   ./deploy.sh          build + deploy + IndexNow
#   ./deploy.sh clean    delete all generated files (run in a fresh copy of the template)
#   ./deploy.sh build    build only (preview: cd dist && python3 -m http.server 8000)
set -e
cd "$(dirname "$0")"

if [[ "$1" == "clean" ]]; then
  setopt nullglob
  rm -rf dist build/.indexnow_key build/__pycache__ [0-9a-f]*.txt images/*.webp images/*.jpg images/*.png images/sizes.json images/games images/promos images/categories images/posts favicon* apple-touch-icon.png site.webmanifest
  echo "clean: only sources left"; exit 0
fi

[ -f favicon.ico ] || python3 build/icons.py
[ -f images/sizes.json ] || python3 build/images.py
python3 build/indexnow.py key > /dev/null   # one key per site, created on first build (build/.indexnow_key)
python3 build/build.py
find dist -name .DS_Store -delete
echo "dist/ ready ($(du -sh dist | cut -f1))"

[[ "$1" == "build" ]] && exit 0

PROJECT=$(python3 -c "import sys; sys.path.insert(0,'build'); import site_config as c; print(c.CF_PROJECT)")
npx --yes wrangler@3 whoami | grep -i email
npx --yes wrangler@3 pages project create "$PROJECT" --production-branch main 2>/dev/null || true
npx --yes wrangler@3 pages deploy dist --project-name "$PROJECT" --branch main --commit-dirty=true
sleep 5
python3 build/indexnow.py submit || echo "IndexNow submit failed (site still deployed); retry: python3 build/indexnow.py submit"
