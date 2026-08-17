# Migrating non-shop content off Shopify

Moving everything that isn't commerce from the Shopify store to this site.
Products, collections, and cart stay on Shopify at `shop.torc.art`.

**Every page that moves gets a redirect.** The authoritative list is
[`redirects.csv`](redirects.csv), in Shopify's bulk-import format — upload it at
*Online Store → Navigation → URL Redirects → Import*. Add a row there in the same
commit that adds the page here, so the two never drift.

## Status

| Shopify URL | Moves to | Content in hand? | Redirect row? |
| --- | --- | --- | --- |
| `/pages/about` | `/about/` | Reconstructed — needs real copy | Yes |
| `/pages/contact` | `/visit/` | Rewritten (form → `hello@torc.art`) | Yes |
| `/blogs/news` | `/news/` | Section exists, posts missing | Yes |
| `/blogs/news/312-main-st` | `/news/312-main-st/` | Stub only | Yes |
| `/blogs/archive` | `/archive/` | Section exists, posts missing | Yes |
| `/blogs/archive/<post>` | `/archive/<post>` | **Not yet enumerated** | Not yet |

Keep slugs identical wherever possible — it makes each redirect a one-liner and
preserves whatever search ranking the old URLs have.

## What is not moving

Products, collections (`/collections/*`), cart, and checkout stay on Shopify.
Artist collections such as `/collections/lucas-beau-leone` are commerce pages;
if a represented artist needs a non-commerce page here, that is a new page rather
than a migration.

## Getting the content out of Shopify

This repo is built in a sandbox with no outbound network access, so the pages
could not be fetched here. Run this locally from the repo root and the raw pages
land in `migration/raw/`, ready to be converted to Markdown:

```sh
sh migration/fetch.sh
```

Two things it cannot get on its own:

1. **The full archive post list.** Get it from the Shopify admin (*Content →
   Blog posts*), or from `https://shop.torc.art/blogs/archive.atom`, which lists
   recent posts. Add each one to the table above and to `redirects.csv`.
2. **Images.** Blog and page images are served from `cdn.shopify.com`. Download
   the ones worth keeping into `static/`, and update the Markdown to point at
   local paths — otherwise the new site stays dependent on the store's CDN.

## Before flipping the domain

`torc.art` currently serves the Shopify store — `torc.art/collections/home`,
`torc.art/products/teardrop`, and `torc.art/blogs/news/312-main-st` all resolve
there today. Pointing the apex at GitHub Pages takes the storefront off that
domain. Sequence it deliberately:

1. Confirm the store is reachable and correct at `shop.torc.art`.
2. Load `redirects.csv` into Shopify, so old links survive the move.
3. Repoint apex DNS at GitHub Pages (`static/CNAME` already says `torc.art`).
4. Re-check every row in the table above against the live site.
