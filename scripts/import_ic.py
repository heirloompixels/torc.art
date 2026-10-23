#!/usr/bin/env python3
"""Bring the joint posts from intentionallyconfusing.com to torc.art.

intentionallyconfusing.com was the Ghost site Kyle and Jeannie ran together
(2021-2026); it is retiring. Its posts were read in full on 2026-10-19 and
routed by what each one says rather than its byline. docs/ic-routing.tsv
lists the rows that come here (slug, destination, confidence only: this repo
is public, and the full reading, with its notes on people, stays in the
archive's docs/content-routing.tsv on disk): the numbered Dispatches (the run
stays whole, whoever wrote an instalment), the gallery's announcements and
the shared trails. dispatches/DISPATCHES.md is the plan this follows.

    python3 scripts/import_ic.py             # write content/journal/ + stage images
    python3 scripts/import_ic.py --dry-run
    scripts/upload_media.sh                  # then put the staged images on R2

Decisions, so they live here and not in a session:

- **Each post keeps its slug at the root** (`path`), so the archive's
  redirect map, which assumed that, holds. One slug that is taken here (the
  old project's About page) is renamed, in RENAMED.
- **Images are WebP at 1600 px**, one width, under `dispatches/<slug>/` on
  media.torc.art: DISPATCHES.md measured that ceiling against this site's
  column and the saving (64%). GIFs are single iPhone frames saved as GIF by
  accident and are re-encoded the same way. PDFs are hosted as they are.
- **Six posts are held back** (HELD), not imported.
- **Drafts stay drafts**, and the two posts that were for paying supporters
  only are drafts too: torc.art has no members' side to put them behind.
- **Links to other intentionallyconfusing.com posts** point at where that
  post lives now when it is known (here, or jeannieortiz.com via that site's
  docs/ic-imported.tsv); otherwise at the old address, which will redirect.

Needs Pillow (uv run --with pillow).
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parent.parent
IC = SITE.parent / "intentionallyconfusing.com"
JO_IMPORTED = SITE.parent / "jeannieortiz.com" / "docs" / "ic-imported.tsv"
ROUTING = SITE / "docs" / "ic-routing.tsv"
RECORD = SITE / "docs" / "ic-imported.tsv"
OUT = SITE / "content" / "journal"
MEDIA = "https://media.torc.art"
WIDTH = 1600

RENAMED = {"about": "intentionally-confusing"}

# Not imported at all: each needs Kyle and Jeannie's word before it is public
# again, and this repo is public, so even a draft here would publish it. They
# stay in the archive; the reasons are kept general for the same reason, and
# the full reading is in the archive's docs/content-routing.tsv on disk.
HELD = {
    "dispatch-10-moss-mushrooms": "names a child",
    "dispatch-023": "written for a closer circle; private place and people",
    "dispatch-024": "family news the post says to agree on first",
    "dispatch-030": "quotes a third party",
    "dispatch-032": "names family members, children among them",
    "desert-archaic": "names friends of the gallery",
}

GHOST_ASSET = re.compile(r"(?:__GHOST_URL__|https?://(?:www\.)?intentionallyconfusing\.com)/content/(images|files|media)/((?:size/w\d+/)?[^\"'\s)<>]+)")
GHOST_LINK = re.compile(r"(?:__GHOST_URL__|https?://(?:www\.)?intentionallyconfusing\.com)/([a-z0-9-]+)/?(?=[\"'#?])")
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
ATTR = re.compile(r'([\w:-]+)="([^"]*)"')


def webp(src, dest, dry):
    with Image.open(src) as im:
        w, h = im.size
        tw = min(w, WIDTH)
        th = round(h * tw / w)
        if not dry and not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            im.seek(0)
            im.convert("RGB").resize((tw, th), Image.LANCZOS).save(dest, "WEBP", quality=80, method=5)
        return tw, th


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stage", type=Path, default=Path.home() / ".cache" / "torc.art" / "ic-media")
    args = ap.parse_args()

    ghost = {json.loads(l)["slug"]: json.loads(l) for l in (IC / "archive" / "database" / "posts.jsonl").open()}
    rows = [r for r in csv.DictReader(ROUTING.open(), delimiter="\t") if r["destination"] == "torc.art"]

    here = {r["slug"]: RENAMED.get(r["slug"], r["slug"]) for r in rows}
    elsewhere = {}
    if JO_IMPORTED.exists():
        for r in csv.DictReader(JO_IMPORTED.open(), delimiter="\t"):
            elsewhere[r["ic_slug"]] = "https://jeannieortiz.com" + r["path"]

    taken = {f.stem for f in (SITE / "content").glob("*.md")}
    clash = [s for s in here.values() if s in taken]
    if clash:
        sys.exit(f"slugs taken by pages here: {clash}; add them to RENAMED")

    OUT.mkdir(parents=True, exist_ok=True)
    record, missing = [], []
    for r in rows:
        if r["slug"] in HELD:
            (OUT / f"{here[r['slug']]}.md").unlink(missing_ok=True)
            record.append([r["slug"], "", "held", HELD[r["slug"]]])
            continue
        g = ghost[r["slug"]]
        slug = here[r["slug"]]
        dims = {}

        def asset(m):
            kind, rel = m.group(1), re.sub(r"^size/w\d+/", "", m.group(2))
            src = IC / "archive" / "content" / kind / rel
            if not src.exists():
                missing.append(f"{slug}: {kind}/{rel}")
                return f"https://intentionallyconfusing.com/content/{kind}/{rel}"
            # A key ending in ".." is refused by R2's upload, so trailing dots go.
            name = re.sub(r"\.+(?=\.[^.]+$)", "", Path(rel).name)
            if kind == "images" and src.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"):
                key = f"dispatches/{slug}/{Path(name).stem}.webp"
                try:
                    dims[key] = webp(src, args.stage / key, args.dry_run)
                except Exception as e:
                    missing.append(f"{slug}: {rel} ({e})")
                    return f"https://intentionallyconfusing.com/content/{kind}/{rel}"
            else:
                key = f"dispatches/{slug}/{name}"
                dest = args.stage / key
                if not args.dry_run and not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(src.read_bytes())
            return f"{MEDIA}/{key}"

        def img(m):
            attrs = dict(ATTR.findall(m.group(0)))
            key = attrs.get("src", "").removeprefix(MEDIA + "/")
            if key not in dims:
                return m.group(0)
            attrs["width"], attrs["height"] = map(str, dims[key])
            attrs.pop("srcset", None)
            attrs.pop("sizes", None)
            attrs.setdefault("loading", "lazy")
            return "<img " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + ">"

        def link(m):
            s = m.group(1)
            if s in here:
                return f"/{here[s]}/" if s not in HELD else f"https://intentionallyconfusing.com/{s}/"
            if s in elsewhere:
                return elsewhere[s]
            return f"https://intentionallyconfusing.com/{s}/"

        body = g["html"] or ""
        body = GHOST_ASSET.sub(asset, body)
        body = IMG_TAG.sub(img, body)
        body = GHOST_LINK.sub(link, body)
        body = re.sub(r"\n\s*\n+", "\n", body)
        feature = GHOST_ASSET.sub(asset, g["feature_image"]) if g.get("feature_image") else ""

        held = None
        draft = g["status"] != "published" or g["visibility"] != "public"
        date = (g["published_at"] or g["created_at"])[:19].replace(" ", "T") + "Z"
        tags = [t["name"] for t in (g.get("tags") or []) if not t["name"].startswith("#")]
        authors = [a["name"] for a in (g.get("authors") or [])]
        fm = ["+++", f"title = {json.dumps(g['title'])}", f"date = {date}", f"path = {json.dumps(slug)}"]
        if draft:
            fm.append("draft = true")
        if g.get("custom_excerpt"):
            fm.append(f"description = {json.dumps(g['custom_excerpt'])}")
        fm += ["", "[extra]", 'author = "gallery"']
        if authors:
            fm.append("byline = [" + ", ".join(json.dumps(a) for a in authors) + "]")
        if tags:
            fm.append("tags = [" + ", ".join(json.dumps(t) for t in tags) + "]")
        if feature:
            fm.append(f"image = {json.dumps(feature)}")
        fm.append(f"original_url = {json.dumps('https://intentionallyconfusing.com/' + r['slug'] + '/')}")
        fm.append(f"ghost_id = {json.dumps(g['id'])}")
        fm.append("+++")
        if not args.dry_run:
            (OUT / f"{slug}.md").write_text("\n".join(fm) + "\n\n" + body + "\n")
        why = held or ("not public on the old site" if draft else "")
        record.append([r["slug"], f"/{slug}/", "draft" if draft else "public", why])

    if not args.dry_run:
        with RECORD.open("w", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["ic_slug", "path", "state", "why"])
            w.writerows(record)
    n = sum(1 for p in args.stage.rglob("*") if p.is_file()) if args.stage.exists() else 0
    print(f"{len(record)} posts ({sum(1 for x in record if x[2] == 'draft')} drafts, {sum(1 for x in record if x[2] == 'held')} held back), {n} files staged in {args.stage}",
          file=sys.stderr)
    for m in missing:
        print("  not found:", m, file=sys.stderr)


if __name__ == "__main__":
    main()
