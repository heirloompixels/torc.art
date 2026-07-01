# torc.art

[Zola](https://www.getzola.org/) static site for Truth or Consequences Contemporary (TorC Contemporary) — the landing page for the TorC contemporary art ecosystem.

## Structure

- `content/` — pages and sections (home, exhibitions, artists, calendar) written in Markdown
- `templates/` — Tera templates (`base.html`, `head.html`, `index.html`, `section.html`)
- `static/` — images, fonts, and other files served as-is
- `config.toml` — site configuration

## Local development

```sh
zola serve
```

## Build

```sh
zola build
```

Deploys to GitHub Pages automatically on push to `main` via `.github/workflows/main.yml`.
