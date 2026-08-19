# Bringing the Dispatches to torc.art

*Written 2026-08-18. Nothing here is built yet. This is the plan and the
measurements behind it, so the work can start cold.*

The Dispatches are a numbered newsletter Kyle and Jeannie ran on
`intentionallyconfusing.com` from 2021 to 2026. That site is retired and its
content is being dispersed to three destinations. The Dispatches come here.

The decision is not ours to relitigate — it is already recorded in
`machinery/sites/intentionallyconfusing.com/README.md`, § "Where the content
should go", as the second of three rules:

> **The Dispatches run stays whole.** All 40-odd numbered dispatches go to
> torc.art regardless of who wrote a given instalment. A numbered series split
> across two domains stops being a series.

Per-item disposition for the whole archive is in that repo's
`docs/content-index.csv` (179 rows, one per post, each with a `suggested_site`,
a `confidence` and a `why`). The rows for this work are the 34 whose `why`
reads `dispatch series — keep the run intact`.

## What is coming

34 posts — 33 published, 1 draft (`Dispatch № 000 · no Camera`). All 34 are
marked high confidence. The archive holds them as bundles under
`export/posts/<date>-<slug>/`, each an `index.md` with Ghost frontmatter
preserved: `original_url`, `ghost_id`, `ghost_uuid`, authors, tags, dates and
status. Provenance does not depend on anything we write.

**The run is № 2–34, with 1 and 21 missing**, plus one unnumbered member the
index still files with the series (`2026-03-13 Random Draw for Foliage &
Atmosphere`). If "keep the run intact" is the point, those three are the first
question to settle — are 1 and 21 lost, were they never numbered, and does the
unnumbered one belong.

Alongside the dispatches, 23 further published posts and 10 drafts are also
destined here on other grounds (joint bylines, shared expeditions). They are
out of scope for this pass but they are in the same CSV.

## The image load, measured

293 asset files, **216.9 MB**, 849 megapixels. Every file was hashed: there are
**no duplicates**, and nothing is missing — the nine entries in the archive's
`export/_missing-assets.txt` all belong to other posts, and the one apparently
broken reference in `dispatch-025` is a base64 download icon Ghost inlined, not
an asset.

It is three unrelated problems, not one:

| | Size | Share |
| --- | ---: | ---: |
| One PDF | 45.5 MB | 21% |
| Six GIFs | 43.9 MB | 20% |
| 285 ordinary photos | 127.5 MB | 59% |

**The six GIFs are single-frame.** All in
`2021-11-22-dispatch-13-trajectory-of-color`, all named `tempImage*.gif`, all
4032×3024, all palettized — iPhone stills exported as GIF by accident.
Re-encoded they go **43.9 MB → 2.0 MB**. That one page currently costs a
visitor 46.9 MB and becomes 3.2 MB. It is a fifth of the whole payload
recovered from six files with no judgement call involved. Note the source is
already reduced to 256 colours; re-encoding cannot restore what GIF threw away,
it only stops us paying for the loss twice.

**The PDF is real, not junk.** `JeannieOrtiz2021Creations-compressed.pdf` in
`2022-11-09-dispatch-025` — 84 pages, 504 embedded images, linked as a download
in the prose. It is Jeannie's 2021 portfolio. Nothing to delete. At 542 KB per
page its images were plainly never downsampled, but it is her portfolio, so
keep the original bytes and host it as a file rather than recompressing it.

**The photos are already half-sized.** Ghost capped most at 2000px — median
width is exactly 2000, 81 files are already ≤1600, only 6 exceed 2400. The win
here is re-encoding, not resizing.

### What re-encoding buys

Measured across all 292 images, not estimated:

| | Total | vs source |
| --- | ---: | ---: |
| Source | 171.4 MB | — |
| JPEG q82 @1600 | 84 MB | −51% |
| WebP q80 @2000 | 85 MB | −50% |
| **WebP q80 @1600** | **61 MB** | **−64%** |
| AVIF q62 @1600 | ~47 MB | −73% |

1600px is the right ceiling for this site. `main` is `80ch` and `p` is `60ch`,
so images render at roughly 700–800 CSS px; 1600 covers 2× retina exactly and
the 2000px sources are about 25% wider than the layout can ever use.

The median dispatch page goes **2.3 MB → 1.2 MB**. The heavy ones collapse
hardest: `dispatch-023` (47 images) 22 MB → 10.9 MB, `dispatch-029` 13.9 → 6.0.

WebP is the recommendation over AVIF: another 14 MB is not worth an encoder
that is roughly seven times slower and more annoying to regenerate.

## Where the images go

**`media.torc.art` is already live.** This was checked against the API, not the
dashboard, on 2026-08-18:

- the **`torc-media`** bucket exists on TorC (`0170b714b0ee025091fed8a088f7a65a`)
- `media.torc.art` is bound to it as an R2 custom domain, proxied, with ssl and
  ownership both `active`
- it answers 404 today only because the bucket is empty

`machinery/CLAUDE.md` already has this right: the *old* Analogkyle account's
claim on the hostname is the orphaned one, and TorC serves it. What the map
does not say, because it had no reason to, is that the bucket behind it is
still empty. This work is what fills it.

So there is nothing to stand up. The work is:

1. Derive WebP @1600 from the archive into a staging directory.
2. Upload ~292 objects under a `dispatches/<slug>/` key prefix, plus the PDF.
3. Rewrite the image references in the ported Markdown to absolute
   `https://media.torc.art/dispatches/…` URLs.

About 61 MB, comfortably inside R2's free tier.

**Derive, never edit in place.** `sites/intentionallyconfusing.com` is the
retirement copy and the master. Everything above reads from it and writes
elsewhere. Its bytes are not ours to change.

The fleet has a `*-originals` convention (`kpc-originals`,
`jeannieortiz-media-originals`) that `torc-media` lacks. Skip it here — the
archive repo already is the originals, and a second copy of 217 MB earns
nothing.

## Moving this site to Cloudflare

Wanted alongside the above: get `new.torc.art` off GitHub Pages and onto
Cloudflare while the site is still pre-launch.

Today it is a **DNS-only (grey cloud) CNAME** to `heirloompixels.github.io`.
Cloudflare is not in the path at all, which is exactly why there is no
certificate — the TLS handshake on `https://new.torc.art/` fails outright.
`static/CNAME` and `base_url` are both already written for the eventual https.

The house pattern to copy is **Workers static assets**, which
`atelier/gather` and `atelier/proofing` already use:

```jsonc
"account_id": "0170b714b0ee025091fed8a088f7a65a",
"assets": { "directory": "./public" },
"routes": [{ "pattern": "new.torc.art", "custom_domain": true }],
"observability": { "enabled": true }
```

Zola builds to `public/`, so it drops straight in. The cutover has the same
shape as gather's (see its `wrangler.jsonc`, note A6): delete the DNS-only
record, let wrangler claim the hostname. HTTPS arrives with the universal
certificate.

Two constraints found while checking:

- **Cloudflare Pages is not available with the current token** — the Pages
  endpoint returns an authentication error, so it would need a scope widening.
  Workers static assets works with the token as it stands and suits this tree
  better regardless.
- **Access (Zero Trust) is not enabled on the account** —
  `access.api.error.not_enabled`. Gating the pre-launch site behind Access
  needs someone to click "Enable Access" in the dashboard first. It is free up
  to 50 users.

## Open decisions

Nothing below should be guessed at. Each changes the work.

1. **Pre-launch privacy.** Three options: a small auth gate in the Worker
   itself (works with the current token, no dashboard step); Cloudflare Access
   with email OTP (cleaner and revocable, needs Access enabled); or leave it
   open as it already is on GitHub Pages, with `noindex` only.
2. **How it deploys.** Manual `wrangler deploy` from the laptop until launch
   keeps every secret on the machine and suits a site that changes in bursts.
   CI is the alternative, but only with a **new narrowly-scoped token** for
   this worker and route — the account-wide TorC token grants edit on Workers,
   D1, R2 and DNS, and does not belong in GitHub Actions secrets.
3. **URL shape and section design.** The dispatches need a Zola section, a
   list template and an item template. This site has no blog, no taxonomy and
   no search index today. Slugs matter: the archive's `docs/redirects.csv`
   assumes each post keeps its slug on the site it moves to.
4. **The gaps in the run** — № 1, № 21, and the unnumbered 2026 member.
5. **The 11 low-confidence rows** in the archive's index, which are not
   dispatches but sit next to them: joint-byline sale and auction announcements
   for Jeannie's weavings. Whether they land here or on her site is a question
   about what torc.art is for, and the tags cannot answer it.

## Redirects

The archive has drafted every redirect already — `docs/redirects.csv` and a
Cloudflare bulk-redirect list beside it — but they are blocked on
`intentionallyconfusing.com`'s nameservers moving off Namecheap. Today that
domain resolves straight to the droplet, so there is nowhere to load the list.
Ghost also left 419 `/r/<hash>` click-tracking URLs that live inside emails
already sent and cannot be edited; they are preserved in
`docs/legacy-redirects.csv`.

## Corrections owed to machinery/CLAUDE.md

Found while surveying, both verified by live DNS and `Server` headers on
2026-08-18:

- torc.art is **not** "the one site in this tree that does not deploy to
  Cloudflare". `kyleparkercunningham.com` and `larrypogreba.com` are on GitHub
  Pages too — same `shalzz/zola-deploy-action`, same `185.199.x` addresses,
  `Server: GitHub.com`. `jeannieortiz.com` is the one that is on Cloudflare.
  Moving this site makes it the first Zola site on Cloudflare, not the last
  holdout.
- `amp.torc.art` is a DNS-only CNAME to GitHub Pages, not a Cloudflare Worker;
  the map groups it with gather and proofing, which genuinely are. The same is
  true of `meteoric.torc.art`.

The map's § facts-that-cross-every-boundary entry on the decommissioned
account is **not** one of these. It says the old account's claims on
`media.kyleparkercunningham.com` and `media.torc.art` are orphaned and that
TorC serves both, which is exactly what the API confirms. It reads as a
warning about the old account, not a claim about the hostname, and it is
correct.
