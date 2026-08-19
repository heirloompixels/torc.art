#!/bin/sh
# Fetch the non-shop pages from the Shopify store into migration/raw/.
# Run locally (this repo's build sandbox has no outbound network access):
#
#     sh migration/fetch.sh
#
# Then hand the files in migration/raw/ over for conversion to Markdown.
# migration/raw/ is gitignored — it is a scratch area, not site content.

set -eu

SRC="https://shop.torc.art"
OUT="$(dirname "$0")/raw"

mkdir -p "$OUT"

# Known non-shop URLs. Add rows here as more turn up in the Shopify admin.
PATHS="
/pages/about
/pages/contact
/blogs/news
/blogs/news/312-main-st
/blogs/archive
"

for p in $PATHS; do
    name="$(echo "$p" | sed 's|^/||; s|/|_|g')"
    printf 'fetching %s ... ' "$p"
    if curl -fsSL "$SRC$p" -o "$OUT/$name.html"; then
        echo "ok"
    else
        echo "FAILED"
    fi
done

# The blog feeds enumerate posts, including any not listed above.
for blog in news archive; do
    printf 'fetching /blogs/%s.atom ... ' "$blog"
    if curl -fsSL "$SRC/blogs/$blog.atom" -o "$OUT/feed_$blog.atom"; then
        echo "ok"
    else
        echo "FAILED"
    fi
done

echo
echo "Saved to $OUT"
echo "Post URLs found in the feeds:"
grep -ho 'href="[^"]*/blogs/[^"]*"' "$OUT"/feed_*.atom 2>/dev/null \
    | sed 's/href="//; s/"$//' | sort -u || echo "  (none — check the feeds manually)"
