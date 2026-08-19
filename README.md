# torc.art

Zola site for Truth or Consequences Contemporary — the gallery's own page.
A contemporary art space in Truth or Consequences, New Mexico, focused on
experiment and experiential work.

`content/` holds the page copy: `_index.md` is the landing page, and a flat
set of Markdown files beside it are the sections — about, artists,
exhibitions, calendar, the community etching press, Agile Meteor Press,
glyphs, press and visit. `migration/` holds the notes and tooling for moving
the non-shop content off Shopify; see
[`migration/MIGRATION.md`](migration/MIGRATION.md). There is no blog and no
search index.

## Local development

```sh
zola serve
```

## Build

```sh
zola build
```

## Deployment

This is the one site in `machinery/sites/` that does not deploy to Cloudflare.

- Source repo: `git@github.com:heirloompixels/torc.art.git`
- GitHub Actions builds on pushes to `main` (`shalzz/zola-deploy-action@master`),
  authenticating with the automatic per-run `GITHUB_TOKEN`
- Published branch: `gh-pages`, served by GitHub Pages
- Public URL: `http://new.torc.art` — http only for now, the certificate is
  not provisioned yet. `static/CNAME` holds that hostname and `base_url` in
  `config.toml` already claims https, which is correct once the certificate
  lands.

The apex `torc.art` is not this repo. It 301s to `shop.torc.art`, which lives
outside the machinery tree. The gallery subdomains that are ours —
gather.torc.art, proofing.torc.art, amp.torc.art — are Cloudflare Workers and
have nothing to do with this build.

**The certificate is the outstanding deployment problem.** GitHub Pages has
never provisioned one for new.torc.art, so https does not answer at all. That
is not cosmetic: `base_url` is https, and Zola's `get_url()` builds absolute
URLs from it, so from 26c6c85 until 2026-08-18 the page linked its stylesheet
at `https://new.torc.art/style.css` — an address that refuses connections —
and every visitor got unstyled HTML with no visible error. The stylesheet is
root-relative now so it cannot happen again, but until the certificate is
provisioned, `og:image` still points at an https URL that does not answer and
link previews have no image. Provision it in the repo's Pages settings.

**CI has not run since 2025-06-01.** The action tracks `master`, so the next
push builds on a Zola it has never used here. Watch the first one.

## Project structure

- `content/`: page copy (Markdown) — `_index.md` plus one file per section
- `templates/`: `base.html` (shell, nav and footer), `head.html` (metadata),
  `index.html` (the landing section), `page.html` (every other page)
- `static/`: assets copied verbatim — logo, favicons, `style.css`, `CNAME`
- `config.toml`: Zola site configuration
- `migration/`: notes and tooling for the move off Shopify
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

- **https.** See above — the certificate is unprovisioned, so the site is
  http-only and its social-card image is unreachable.
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
