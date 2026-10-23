#!/usr/bin/env bash
# Put the images and files scripts/import_ic.py staged onto R2, behind
# media.torc.art (bucket torc-media on TorC; dispatches/DISPATCHES.md § where
# the images go). Each key goes up once: one already answering on
# media.torc.art is skipped, so this can be run again after a partial run.
#
#   scripts/upload_media.sh [stage]    default ~/.cache/torc.art/ic-media
set -euo pipefail

if [ "${1:-}" = "--one" ]; then        # one key, run by xargs below
  key="$2"
  [ "$(curl -s -o /dev/null -w '%{http_code}' "https://media.torc.art/$key")" = 200 ] && exit 0
  case "$key" in
    *.webp) ct=image/webp ;; *.pdf) ct=application/pdf ;; *.mp4) ct=video/mp4 ;;
    *.jpg|*.jpeg) ct=image/jpeg ;; *.png) ct=image/png ;; *) ct=application/octet-stream ;;
  esac
  if $WRANGLER r2 object put "torc-media/$key" --file "$key" --remote --content-type "$ct" \
       --cache-control "public, max-age=31536000, immutable" >/dev/null 2>&1; then
    echo "up   $key"
  else
    echo "FAIL $key"
  fi
  exit 0
fi

STAGE="${1:-$HOME/.cache/torc.art/ic-media}"
set -a; . "$HOME/.config/cloudflare/torc.env"; set +a
export WRANGLER="${WRANGLER:-npx --yes wrangler@4}"
self="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
cd "$STAGE"
find dispatches -type f | sort | xargs -n 1 -P 8 "$self" --one
