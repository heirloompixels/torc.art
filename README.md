Website for Truth or Consequences Contemporary.

Static site built with [Zola](https://www.getzola.org/). Pushes to `main` are built
and deployed to GitHub Pages by `.github/workflows/main.yml`, which serves the
domain in `static/CNAME`.

- `content/` — page copy (Markdown)
- `templates/` — Tera templates
- `static/` — stylesheet, logo, favicons, `CNAME`
- `config.toml` — site config
- `migration/` — notes and tooling for moving non-shop content off Shopify;
  see [`migration/MIGRATION.md`](migration/MIGRATION.md)

Local preview: `zola serve`
