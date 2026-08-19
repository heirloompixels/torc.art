# Design mockups

Thirty-four homepage designs for Truth or Consequences Contemporary. Every
mockup is a standalone HTML file with its CSS inline — no build step, no shared
stylesheet, nothing to install. Open `index.html` for a contact sheet of all
thirty-four with live thumbnails and a filter, or open any file directly.

## What they have in common

- **The real content.** Statement, the Fieldwork notice, the "Here" index, the
  Projects list, and — where a design has room for it — exhibitions, the
  calendar, etching press rates, and the Agile Meteor Press catalog, all taken
  from `content/*.md`.
- **The site's typefaces.** Jost for display, Inter for interface text, EB
  Garamond for anything read at length — the same three the current site uses,
  loaded here from Google Fonts.
- **The site's images.** `../static/box_prints.jpg` and `../static/logo.svg`.
  These are the only two images the repo has, so every mockup reuses them; real
  installation and exhibition photography would change several of these designs
  substantially.
- **Responsive.** Each collapses to a single column on a phone.

Nothing here touches `templates/` or `static/style.css`. Picking a direction is
a separate step from building it.

## The thirty-four

| | Design | Direction |
|---|---|---|
| 01 | Kunsthalle | Stark white, hairline rules, oversized Jost over a two-column editorial grid |
| 02 | Desert Ledger | Warm sand on ruled paper, entries numbered like a field ledger |
| 03 | Broadsheet | Newspaper front page — flag, dateline, justified columns, on-the-walls sidebar |
| 04 | Monolith | Near-black full bleed, thin display type, hover-shifting index |
| 05 | Swiss Grid | Visible 12-column grid, red accent, everything flush |
| 06 | Marginalia | Asymmetric column with true margin notes down both sides |
| 07 | Lightning | Night blue and electric yellow, built on the cloud-and-bolt mark |
| 08 | Vitrine | Floating white panels on wall grey; exhibitions as museum labels |
| 09 | Oasis | Sky-to-sand gradient, arched images, water-green accents |
| 10 | Terracotta | Adobe clay palette, arch forms, drawn sun |
| 11 | Index | Monospaced database view — records, field names, coordinates |
| 12 | Poster | Full-width type poster, running ticker, giant hover-slide menu |
| 13 | Riso | Two-colour risograph misregistration on stock |
| 14 | Archive | Filing tabs on a manila folder, record card, rubber stamp |
| 15 | Horizon | Letterspaced horizontal bands, full-bleed image strip |
| 16 | Manifesto | Single centred column, drop caps, ornaments |
| 17 | Nocturne | Charcoal and warm amber, framed plate, two-column calendar |
| 18 | Blueprint | Architectural sheet — title block, dimension lines, schedules |
| 19 | Salt Flat | Barely-there hairlines, enormous whitespace. The most restrained |
| 20 | Split Screen | Fixed dark nav panel left, scrolling content right |
| 21 | Letterpress | Double-ruled border, fleurons, printer's bill of contents |
| 22 | Meteor | Starfield night, catalog as book spines. Leads with the press |
| 23 | Bauhaus | Hard-ruled mosaic of primary blocks, circle and square |
| 24 | Contact Sheet | Film contact sheet — sprocket edges, numbered frames, dark base |
| 25 | Zine | Photocopy contrast, inverted type, marquee. The loudest |
| 26 | Editorial | Magazine feature: kicker, standfirst, drop cap, pull quote, rails |
| 27 | Neue Gallery | Small caps, centred rules, italic titles. Old-world restraint |
| 28 | Topographic | Contour lines behind the page, sections as map symbols |
| 29 | Monsoon | Storm-sky gradient with rain, clearing to desert paper |
| 30 | Kiosk | Rounded tiles, deep green hero, big targets and stat blocks |
| 31 | Catalogue | Catalogue raisonné — numbered entries, plates, artist columns |
| 32 | Marquee | Three counter-scrolling type bands as masthead |
| 33 | Concrete | Concrete poetry — title broken across a stepped typographic field |
| 34 | Sun Bleached | Warm bleached gradient, soft sun disc, offset rose shadows |

## How to look at these

`index.html` is the contact sheet — all thirty-four with thumbnails and a filter
by temperament. The thumbnails in `thumbs/` are the top 1440×900 of each page,
rendered from the files themselves; they are generated output, not hand-made, so
regenerate them if you edit a design.

Every design was rendered in Chromium at 1440, 768 and 390 px and checked for
horizontal overflow. All thirty-four are clean at all three.

## Notes on choosing

A few are close cousins and probably shouldn't both survive: 01/15/19 are three
temperatures of the same restraint; 03/26/31 are three kinds of editorial; 09,
10, 34 all work the desert palette; 04, 17, 22 are the dark options.

Motion in 12, 25 and 32 respects `prefers-reduced-motion`.

## Before any of this ships

Two mockups carry text that is not from `content/`: **11 Index** prints a
coordinates/elevation block, and **18 Blueprint** repeats the same location
facts in its specification table. Those numbers were written to give the layout
something to hold. Check them against a real source before they go anywhere
near production.
