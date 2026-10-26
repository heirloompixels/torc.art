+++
title = "Truth or Consequences Contemporary"
description = "A gallery in the middle of nowhere. Contemporary art in the oasis — Truth or Consequences, New Mexico."
sort_by = "weight"

# ── The landing page is data, not prose ──────────────────────────────────
#
# Every field below is a named slot. A theme reads the slots it has room for
# and ignores the rest, so changing `extra.theme` in config.toml never
# touches this file and never rewrites a word of the gallery's copy. The
# page body is deliberately empty: if copy lived down there, the layout
# would live down there with it and the themes could not be swapped.
#
# Strings marked "markdown" below are rendered through the markdown filter,
# so links and emphasis work in them.
[extra]
author = "gallery + claude"

# The name, broken where a display theme wants to break it. Themes that set
# it as one line join these with a space.
title_lines = ["Truth or", "Consequences", "Contemporary"]

# Short phrases. The poster runs them as a ticker; quieter themes may set
# them as a single rule of small caps, or drop them.
marquee = [
  "A Gallery in the Middle of Nowhere",
  "Art in the Oasis",
  "312 Main Ave",
  "Truth or Consequences NM",
]

# The one sentence a theme can afford to set very large.
pull_quote = "Obsessed with the transmission of lived emotions from one human being to another."

# markdown
statement = """
Contemporary art space focusing on experiment and experiential works. We bring
cutting edge projects to life in the strange vortex which is Truth or
Consequences, New Mexico.

Handloom, sculpture, intaglio, painting, printmaking, art clothing, adornment,
knives, and books.
"""

# The list under the footer rule — what the gallery does, in a breath.
activities = [
  "Exhibition Space", "Agile Meteor Press", "Workshops", "Performance",
  "Dance", "Art Equipment", "MeTeORiC", "Idea Idea", "Printmaking",
  "Stone Sculpture",
]

[extra.hero]
src = "/box_prints.jpg"
alt = "Intaglio prints laid out on a wooden table around a deep red presentation box"

# The standing notice. Empty `title` retires it and every theme drops the
# block; nothing else needs editing when the season changes.
[extra.notice]
title = "Fieldwork"
subtitle = "Summer 2026"
url = "/fieldwork/"
# markdown
body = """
We are in and out of the gallery this summer as we do our annual
[Fieldwork](/fieldwork/) — creating and rejuvenating out in the wild. Orders
from the [shop](https://shop.torc.art) will ship slower than normal — please
get in touch if you need a rush order.
"""
signature = "Jeannie & Kyle"
+++
