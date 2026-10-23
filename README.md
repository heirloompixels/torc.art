# torc.art

Zola site for Truth or Consequences Contemporary, a contemporary art space in
Truth or Consequences, New Mexico, focused on experiment and experiential work.

**This site is the gallery's home and its archive of everything the gallery
does; the shop is just the shop** (Kyle, 2026-10-23). Shows, events, the
Dispatches, the press, the press kit, and anything the gallery has said about
itself belong here, in its own words. shop.torc.art sells, and its pages
carry only what selling needs. When something gallery-shaped turns up on the
shop, it moves here.

`content/` holds the page copy: `_index.md` is the landing page — data, not
prose, see **The look is a theme** below — and a flat set of Markdown files
beside it are the sections — about, history, artists,
exhibitions, calendar, the community etching press, Agile Meteor Press,
MeTeORiC, fieldwork, glyphs, members, projects, press, visit and the
manifest. `migration/` holds the notes and tooling for moving the non-shop
content off Shopify; see [`migration/MIGRATION.md`](migration/MIGRATION.md).
There is no search index.

Each page's front matter carries three fields the site's furniture is built
from: `weight` orders it, `extra.nav` admits it to the header, and
`extra.blurb` is the one-line hook the landing page's index prints beside it.
A page with no `weight` is not merely unsorted — the section is sorted, so an
unweighted page is **not built at all**.

Every page carries an `extra.author` field in its front matter — `gallery`
for Jeannie's and Kyle's own copy, `claude` for pages an AI assistant
composed from the gallery's archives, `gallery + claude` for a mix — and
`/manifest/` renders the honest who-wrote-what list, following the
convention on kyleparkercunningham.com. The deep-history pages (history,
meteoric, members, projects, fieldwork) were written 2026-08-20 from the
kpc-brain's sources; editorial holds and unverified facts are recorded as
HTML comments at the top of the affected pages — read those before editing.

`content/journal/` holds the Dispatches and the other joint posts from the
retired `intentionallyconfusing.com` (2021–2026), imported 2026-10-19 by
`scripts/import_ic.py` and listed on `/dispatches/`; they are the one part of
the site with dates, so they are a section of their own, sorted by date, and
the only pages that use `templates/post.html`. See
[`dispatches/DISPATCHES.md`](dispatches/DISPATCHES.md).

## The look is a theme

The whole look of the site is one word in `config.toml`:

```toml
[extra]
theme = "poster"
```

Change it, rebuild, and everything changes — the landing page's layout and
every page's styling — without touching `content/` or rewriting a word of
copy. `poster` is the current one, from `mockups/12-poster.html`: a type
poster on the way in, and a deliberately quiet single column for the fourteen
years of prose behind it. `plain` is the site's first look, kept as the
fallback.

The landing page's copy lives as named slots in `content/_index.md` and its
layout lives in `templates/homes/<theme>.html`, so a theme can never take the
copy with it when it goes. [`THEMES.md`](THEMES.md) is the manual: why it is
built this way, how to add a theme, and how to add a slot.

## Local development

```sh
zola serve
```

## Build

```sh
zola build
```

## Deployment

The site is the `torc-art` Cloudflare Worker on the TorC account, serving the
Zola build as static assets at **torc.art** (`wrangler.jsonc`). It was on
GitHub Pages at new.torc.art, over http only, until 2026-10-23.

- **Every push to `main` deploys** (`.github/workflows/deploy.yml`): Zola
  0.22.1 builds, then `wrangler deploy`, with a narrow token in the repo
  secret `CLOUDFLARE_API_TOKEN` (Account: Workers Scripts edit; zone
  torc.art: Workers Routes edit, DNS edit). So this repo keeps **draft PRs**:
  a merge is a deploy, and someone should be at the keyboard.
- **By hand:** `scripts/deploy-worker.sh` (or `--dry-run`), with the
  laptop's TorC credentials.
- **`src/worker.js`** sits in front of the assets: new.torc.art and plain
  http go to https://torc.art; Shopify's old paths on the apex (`/products`,
  `/collections`, `/cart`, `/pages`, `/blogs` and the rest) go to
  shop.torc.art with the path kept, because until this site took it, every
  torc.art address landed on the shop; and `/rss/`, the old
  intentionallyconfusing.com feed address, goes to `/rss.xml`.
- intentionallyconfusing.com's bulk redirects (111 of them) land on this
  site's root paths: every imported post keeps its old slug.

### Cutover

Shopify holds the apex (an A record to `23.227.38.65`) and GitHub Pages holds
new.torc.art (a CNAME), so the Worker cannot attach either name until they
go. In order:

1. Remove torc.art from the shop's domains in Shopify admin. shop.torc.art
   and www.torc.art stay with Shopify.
2. `scripts/cutover.py` checks the Worker on workers.dev, builds, saves both
   records to `docs/cutover-records.json`, deletes them, deploys with the
   names attached, and checks the live site. `--undo` puts the records back.
3. Turn off GitHub Pages in the repo's settings, and add the CI token.
4. Merge PR #4. From then on CI deploys.

The apex's MX and TXT records (Email Routing, the site verification) are not
touched. The other subdomains are not this repo: gather, proofing, futures
and members are their own Workers, amp and meteoric are GitHub Pages, media
is R2, and shop, www and account are Shopify.

## Project structure

- `content/`: page copy (Markdown) — one file per section, plus `_index.md`,
  which is the landing page's data rather than its prose
- `templates/`: `base.html` (the shell), `head.html` (metadata and the theme's
  stylesheet), `chrome/` (the header and footer every theme shares),
  `index.html` (the landing page's theme dispatch), `homes/` (one landing-page
  layout per theme), `page.html` (every other page), `404.html`
- `static/`: assets copied verbatim — logo, favicons, `CNAME`, `base.css` (the
  reset and geometry every theme needs) and `themes/<name>.css` (the looks)
- `THEMES.md`: how the theme system works and how to add one
- `config.toml`: Zola site configuration
- `migration/`: notes and tooling for the move off Shopify
- `dispatches/`: the plan for importing the Dispatches run (not built)
- `.github/workflows/main.yml`: build and deploy workflow

## What was repaired, 2026-08-18

The repo was initialized from a personal-site template (nnix.com) and kept that
template's identity and dead ends. All of the following were the template's,
not the gallery's:

- **It did not build.** `config.toml` set `markdown.highlight_code`, a field
  Zola removed; 0.22 refuses the config outright.
- **The page overflowed narrow viewports.** `h1` was a fixed `4.07em`, wider
  than the column on a phone, which widened the whole document and dragged
  everything else off the right edge with it — 114px of overflow at 320px wide,
  59px at 375px, 20px at 414px. It is now
  `clamp(2.25rem, 11vw, 4.07em)`, which measures zero overflow at 320, 375,
  414, 500 and 768 and leaves the desktop size unchanged.
- **Five `@font-face` rules pointed at `/fonts/nnix*.woff2`, which do not
  exist**, and declared families (`ampbook`, `ampmono`, …) that nothing
  referenced. Everything that *did* ask for a font asked for the old `nnix*`
  names, so those rules never applied either. Both halves are gone; the mono
  face is now a system stack.
- **The build date read `PLACEHOLDER`.** `config.extra.epoch` was a literal
  string. The footer now renders Zola's `now()`.
- **The footer's "submissions" link pointed at a bare `https://`.** Removed,
  with a comment in `base.html` marking where it goes when there is a real
  destination.
- **`.subtle-mono` was `#d9d9d9` on a `#f2f2f2` ground** — about 1.2:1, that
  is, invisible. Now `#6b6b6b`, which clears 4.5:1.
- **The JSON-LD block described someone else.** It named "agile meteor press"
  and its `sameAs` listed cherubgyre.com, refmark.com and a David Emerson's
  LinkedIn and GitHub. It is now an `ArtGallery` record for this gallery, with
  its locality and its Instagram.
- **`site.webmanifest` was Agile Meteor Press**, with a background colour the
  site does not use.
- `apple-mobile-web-app-title` was `MyWebSite`.
- `og:image` never rendered — the template tested an `image` variable nothing
  ever set, so links to the site had no card. It now defaults to
  `config.extra.default_image` and takes a per-page override from
  `extra.image`. Twitter card tags are wired to the existing
  `config.extra.twitter_card`.
- A `<style>` block set `cursor: url("/icons/cursor.png")`; there is no
  `static/icons/`.
- `config.toml` declared taxonomies for a bookshelf — `recommender`,
  `authorname`, `pubyear`, `rating`, `readstate`. Nothing used them.
- `templates/index.html` carried a stray `<h1>Something</h1>` outside any
  block, and `templates/index.html.old` was a dead copy. Both gone.
- A duplicate `a:link` rule set Courier and was immediately overridden by the
  next line; `h1`'s stack said `san-serif`; an `emph` selector matched no
  element. All dead, all removed.
- The two images had no `alt` text, and the site footer was a `<p>` inside
  `<main>`. It is a `<footer>` now, and `main`'s `min-height` moved to `body`
  so the column geometry survived the move.

`extra.author` changed from `kpc` to the gallery's name, since the site speaks
for the gallery. Revert that if the byline was deliberate.

## Still open

- **The press kit's photographs.** Only one image is in it. The 2024 gallery
  photographs made for the Southwest Contemporary field guide are on the
  double pink drive (`Design/torCc/SWC-FieldGuide`) and wait for Kyle.
- **The redrafted copy.** The pages marked `claude` in /manifest/ are drafts
  in Jeannie's and Kyle's voice and wait on their read.
- **The fonts are not ours.** EB Garamond and Inter come from Google Fonts and
  Jost from indestructibletype.com on every page load. For something meant to
  be the gallery's record, all three are open-licensed and should be
  self-hosted in `static/fonts/` so the page does not depend on two other
  people's uptime.
- **The webring link is unverified.** The footer links to
  `webring.xxiivv.com/#xxiivv` under the label "torc". That anchor is the
  template's, not the gallery's. Either the gallery is a member and the anchor
  is wrong, or it is not and the link should go.
- The pages are copy, not records. Exhibitions and artists are prose on a
  page; if this is to be the gallery's record they want structure behind
  them — a work, a show and a date that can be listed, sorted and linked.
