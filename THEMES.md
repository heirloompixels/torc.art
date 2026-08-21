# Themes

The site's look is a theme, and the theme is one word in `config.toml`:

```toml
[extra]
theme = "poster"
```

Change that word, run `zola build`, and the whole site changes. Nothing in
`content/` moves, no copy is rewritten, and no other file needs an edit.

Two themes exist today:

| Name | What it is |
|---|---|
| `poster` | From `mockups/12-poster.html`. The landing page is a type poster — the name at 18vw, a running ticker, a three-column band, an index you slide a finger down. The interior pages are the quiet opposite: one left-aligned column, the same palette, the orange demoted to rules and labels. |
| `plain` | The site's first look — a centred column on warm grey. Kept as the quiet fallback, and as the proof that the swap works. |

## Why it is built this way

The thirty-four designs in `mockups/` are not thirty-four stylesheets over one
page. They are thirty-four different documents: the poster wants the gallery's
name split across three lines at three sizes, the blueprint wants a title block
and a schedule table, the split-screen wants a fixed panel wrapping everything.
No stylesheet swap gets you from one to another.

So the landing page's **copy** is data and its **layout** is a theme. Every
piece of the front page is a named field in `content/_index.md` — the title
lines, the ticker phrases, the pull quote, the statement, the standing notice,
the hero image. A theme reads the slots it has room for and ignores the rest.
That is the whole trick: swapping themes cannot damage the copy, because the
copy is not in the theme.

The interior pages need no per-theme markup at all. They are Markdown through
`templates/page.html`, and a theme styles them with CSS.

The header and the footer are shared markup for the same reason
(`templates/chrome/`). A theme changes how they look, not what they are. Nav
membership and order come from the pages themselves — `weight` orders,
`extra.nav` admits to the header — so adding a page updates the header and the
landing-page index at once, and no theme hardcodes a list of links.

## Adding a theme

Four steps, none of which touches `content/`:

1. **The layout.** Write `templates/homes/<name>.html`, reading the slots
   from `section.extra`. Copy `templates/homes/poster.html` and start
   deleting — it uses every slot there is.
2. **The look.** Write `static/themes/<name>.css`. It loads after
   `static/base.css`, which is the reset and the geometry every theme needs;
   everything visual is yours. Style the shared chrome (`.site-head`,
   `.site-nav`, `.site-foot`) and the interior column (`.prose`) as well as
   your own landing-page classes, or the interior pages will be unstyled.
3. **The dispatch.** Add one `{% elif %}` to `templates/index.html`. Tera
   takes a literal include path only — `{% include "homes/" ~ theme ~ ".html" %}`
   is a parse error on zola 0.22.1 — so the registry is written out by hand.
   An unknown theme name renders a visible error and falls back to `plain`.
4. **The registry.** Add a `[extra.themes.<name>]` block to `config.toml`
   with a `label`, a one-line `description` and a `color` — the `color` is
   the browser's `theme-color`, so it should be the theme's page background.

Then set `extra.theme` to the new name.

## Adding a slot

If a design needs something the data does not have — a list of opening hours,
a second image — add the field to `[extra]` in `content/_index.md` and guard
it in the themes that use it (`{% if x.hours %}`). Themes that do not know
about it are unaffected. Never put copy in a theme template: the next swap
would lose it.

## What is not themed

- The `<head>` metadata, the JSON-LD and the favicons (`templates/head.html`).
  A theme supplies only its `color`.
- `content/` — every page's prose, and the honest authorship record in
  `extra.author` that `/manifest/` renders.
- The two facts a theme must not invent: the gallery opened at 312 Main in
  2023 but the practice is fourteen years older, and the ticker and footer
  strips are gallery copy, not decoration. Both come from `_index.md`.
