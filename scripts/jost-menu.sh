#!/usr/bin/env bash
# Rebuild static/fonts/Jost-Menu.woff2: Jost trimmed to the characters the
# sans labels use (menu, footer, margin labels, dates) (THEMES.md § the menu's sans). Run it if the menu ever needs a
# character outside the set below. Needs fontTools; the coelacanth lab's
# venv has it. Source: Jost 3.710, OFL (static/fonts/OFL-Jost.md).
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="${1:-../../atelier/desk/public/assets/fonts/jost.woff2}"
PYFTSUBSET="${PYFTSUBSET:-../../lab/coelacanth/.venv/bin/pyftsubset}"
"$PYFTSUBSET" "$SRC" \
  --text="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,:/()@·&'’+-–—↗ " \
  --layout-features=kern --flavor=woff2 \
  --output-file=static/fonts/Jost-Menu.woff2
ls -l static/fonts/Jost-Menu.woff2
