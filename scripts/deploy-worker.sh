#!/usr/bin/env bash
# Build the site and deploy it to the torc-art Worker by hand (README.md §
# deployment). CI does the same on every push to main; this is for the
# cutover and for when CI is down.
#
#   scripts/deploy-worker.sh            build and deploy
#   scripts/deploy-worker.sh --dry-run  build, and only show the upload
#
# Zola must be 0.22.1. Credentials come from ~/.config/cloudflare/torc.env.
set -euo pipefail
cd "$(dirname "$0")/.."

ZOLA="${ZOLA:-zola}"
case "$("$ZOLA" --version)" in
  "zola 0.22.1") ;;
  *) echo "need zola 0.22.1, found: $("$ZOLA" --version) (set ZOLA=/path/to/zola)" >&2; exit 1 ;;
esac
"$ZOLA" build

# wrangler.jsonc names the domains, so a real deploy attaches them, which
# fails while Shopify and GitHub Pages still hold the names. A dry run never
# attaches anything.
case " $* " in
  *" --dry-run "*) ;;
  *) python3 scripts/cutover.py --check || {
       echo "Shopify or GitHub Pages still holds a name: cut over first (scripts/cutover.py)" >&2; exit 1; } ;;
esac

set -a; . "$HOME/.config/cloudflare/torc.env"; set +a
WRANGLER="${WRANGLER:-npx --yes wrangler@4}"
$WRANGLER deploy "$@"
