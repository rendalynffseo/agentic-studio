#!/bin/zsh
# Usage: ./deploy.sh build | clean | images | check | (no arg = production build + deploy)
set -e
cd "$(dirname "$0")"
PROJECT=$(node -e "import('./src/config.js').then(m => console.log(m.default.cfProject || ''))")
[ -d node_modules ] || npm install --no-audit --no-fund --silent
case "$1" in
  clean)  rm -rf dist preview src/img node_modules ;;
  images) node scripts/images.js ;;
  build)  [ -d src/img ] || node scripts/images.js; node scripts/build.js ;;
  check)  [ -d src/img ] || node scripts/images.js; SITE_ENV=production node scripts/build.js && node scripts/check.js --external ;;
  "")
    [ -n "$PROJECT" ] || { echo "Set cfProject in src/config.js"; exit 1; }
    [ -d src/img ] || node scripts/images.js
    SITE_ENV=production node scripts/build.js && node scripts/check.js
    npx wrangler pages deploy dist --project-name="$PROJECT" --branch=main --commit-dirty=true ;;
  *) echo "Usage: ./deploy.sh [build|clean|images|check]"; exit 1 ;;
esac
