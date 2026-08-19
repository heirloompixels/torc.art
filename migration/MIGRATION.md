# Migrating non-shop content off Shopify

The shop should just be a shop. Everything that isn't commerce moves from the
Shopify store to this Zola site. Products, collections, cart and checkout stay on
Shopify at `shop.torc.art`.

## Where the content landed

The gallery, program and press pages now live here:

| Page | Path |
| --- | --- |
| About | `/about/` |
| Visit | `/visit/` |
| Artists | `/artists/` |
| Exhibitions | `/exhibitions/` |
| Calendar | `/calendar/` |
| Community Etching Press | `/etching-press/` |
| Agile Meteor Press | `/agile-meteor-press/` |
| Glyphs | `/glyphs/` |
| Press | `/press/` |

## Redirects

Every page that moves needs a redirect from its old Shopify URL.
[`redirects.csv`](redirects.csv) is in Shopify's bulk-import format — upload it at
*Online Store → Navigation → URL Redirects → Import*. Add a row in the same commit
that adds the page here, so the two never drift.

Only the two rows whose Shopify source URLs are confirmed are in the file today
(`/pages/about` and `/pages/contact`). The remaining pages above were written from
the store's content rather than migrated URL-for-URL, so their old paths need to be
read off the Shopify admin (*Content → Pages* and *Content → Blog posts*) before
they can be redirected. Don't guess them — a redirect pointing at a URL that was
never live is worse than none.

The targets currently point at `new.torc.art`, which is where this site deploys
(see `static/CNAME`). If the apex is ever repointed here, rewrite the targets to
`torc.art` and re-import.

## Blog content

`shop.torc.art/blogs/news` and `/blogs/archive` have not been migrated. The archive
in particular is a digital memex of the times we share doing this work, and it is
worth moving deliberately rather than in bulk. When it is time:

1. Enumerate the posts from the Shopify admin or from the `.atom` feeds.
2. Add a section here with one Markdown file per post.
3. Keep slugs identical, and add a redirect row for each.

## Getting the raw pages out of Shopify

Sandboxed builds have no outbound network access, so pages can't be fetched during
a session here. Run this locally from the repo root and the raw HTML lands in
`migration/raw/` (gitignored — it's a scratch area, not site content):

```sh
sh migration/fetch.sh
```

Images are the one thing it can't finish on its own: blog and page images are
served from `cdn.shopify.com`. Download the ones worth keeping into `static/` and
repoint the Markdown at local paths, otherwise this site stays dependent on the
store's CDN.

## Before flipping the apex

`torc.art` currently serves the Shopify store. Pointing the apex at GitHub Pages
takes the storefront off that domain, so sequence it deliberately:

1. Confirm the store is reachable and correct at `shop.torc.art`.
2. Complete the redirect table above and import it into Shopify.
3. Repoint apex DNS at GitHub Pages and update `static/CNAME`.
