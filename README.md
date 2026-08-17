Website for Truth or Consequences Contemporary (torc.art).

Static site built with [Zola](https://www.getzola.org/). Pushes to `main` are built
and deployed to GitHub Pages by `.github/workflows/main.yml`.

- `content/` — page copy (Markdown)
- `templates/` — Tera templates
- `static/` — stylesheet, logo, favicons, `CNAME`
- `config.toml` — site config; landing-page project cards live under `[[extra.projects]]`

Local preview: `zola serve`
