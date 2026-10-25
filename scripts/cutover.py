#!/usr/bin/env python3
"""Move torc.art and www.torc.art from Shopify, and new.torc.art from GitHub Pages, to the torc-art Worker.

    scripts/cutover.py           build, swap the records, deploy with the domains
    scripts/cutover.py --undo    detach the Worker's domains and put the saved records back
    scripts/cutover.py --check   exit 1 while Shopify or GitHub Pages still holds a name

README.md § cutover is the why. In order, so that nothing is deleted until
everything that can fail without harm has passed:

1. The staged Worker must answer and redirect, and the site is built
   (deploy-worker.sh --dry-run), before any record moves.
2. The apex A record and the www CNAME to Shopify, and the new.torc.art
   CNAME to GitHub Pages, are saved to docs/cutover-records.json, then deleted.
3. The Worker is deployed with all three names attached (wrangler.jsonc routes);
   Cloudflare makes the records and the certificate. Resolvers holding no
   answer get none from step 2 until this lands, about a minute.

Nothing else in the zone is touched: the apex MX, SPF and site verification,
shop and account (still Shopify), amp and meteoric (still GitHub Pages),
media, and the Workers and OpenBSD subdomains.
"""
import json, os, subprocess, sys, time, urllib.error, urllib.request

ACCOUNT = "0170b714b0ee025091fed8a088f7a65a"
ZONE = "e3b7f1f43cdd15174bf01582c3de2434"
APEX = "torc.art"
NEW = "new.torc.art"
WWW = "www.torc.art"
WORKER = "torc-art"
STAGED = "https://torc-art.torc.workers.dev"
SHOPIFY = "23.227.38.65"
SHOPIFY_CNAME = "shops.myshopify.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED = os.path.join(ROOT, "docs", "cutover-records.json")
UA = "torc-art-cutover/1 (+https://torc.art)"


def token():
    # Read the token from the file, never from argv, and never print it.
    for line in open(os.path.expanduser("~/.config/cloudflare/torc.env")):
        line = line.strip()
        if line.startswith("export "):
            line = line[len("export "):]
        key, _, value = line.partition("=")
        if key.strip() == "CLOUDFLARE_API_TOKEN":
            return value.strip().strip('"').strip("'")
    sys.exit("no CLOUDFLARE_API_TOKEN in ~/.config/cloudflare/torc.env")


def cf(method, path, body=None, missing_ok=False):
    req = urllib.request.Request(
        "https://api.cloudflare.com/client/v4" + path,
        method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json", "User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        if missing_ok and e.code == 404:
            return None
        d = json.load(e)
    if not d.get("success"):
        sys.exit(f"{method} {path} failed: {d.get('errors')}")
    return d["result"]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def get(url):
    """Status, Server header and Location of one request, never following a redirect."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        r = urllib.request.build_opener(NoRedirect).open(req, timeout=20)
    except urllib.error.HTTPError as e:
        r = e
    return r.status, r.headers.get("Server", ""), r.headers.get("Location", "")


def name_records():
    found = []
    for host in (APEX, NEW, WWW):
        for r in cf("GET", f"/zones/{ZONE}/dns_records?name={host}&per_page=100"):
            if r["type"] in ("A", "AAAA", "CNAME"):
                found.append({k: r[k] for k in ("id", "type", "name", "content", "ttl", "proxied")})
    return found


def is_old(r):
    """Shopify's A record on the apex and CNAME on www, or GitHub Pages' CNAME on new.torc.art."""
    return (r["name"] == APEX and r["type"] == "A" and r["content"] == SHOPIFY) or (
        r["name"] == WWW and r["type"] == "CNAME" and r["content"] == SHOPIFY_CNAME) or (
        r["name"] == NEW and r["type"] == "CNAME" and r["content"] == "heirloompixels.github.io")


def old_records():
    return [r for r in name_records() if is_old(r)]


def wrangler_env():
    env = dict(os.environ, CLOUDFLARE_API_TOKEN=token())
    return env


def cut_over():
    status, _, _ = get(STAGED + "/dispatch-20/")
    redirect = get(STAGED + "/products/anything")
    if status != 200 or redirect[0] != 301 or redirect[2] != "https://shop.torc.art/products/anything":
        sys.exit(f"the staged Worker is not right ({status}, {redirect}); nothing done")

    records = name_records()
    old = [r for r in records if is_old(r)]
    other = [r for r in records if not is_old(r)]
    if not old:
        sys.exit("Shopify and GitHub Pages hold none of the names: already cut over? Nothing done.")
    if other:
        sys.exit(f"unexpected records on the names; nothing done:\n{json.dumps(other, indent=2)}")

    print("building (deploy-worker.sh --dry-run)")
    if subprocess.call([os.path.join(ROOT, "scripts", "deploy-worker.sh"), "--dry-run"], cwd=ROOT) != 0:
        sys.exit("the build failed; nothing done")

    with open(SAVED, "w") as f:
        json.dump(old, f, indent=2)
        f.write("\n")
    print(f"saved {len(old)} records to {os.path.relpath(SAVED, ROOT)}")
    for r in old:
        cf("DELETE", f"/zones/{ZONE}/dns_records/{r['id']}")
        print(f"deleted {r['type']} {r['name']} {r['content']}")

    print("deploying with all three names attached")
    wrangler = os.environ.get("WRANGLER", "npx --yes wrangler@4").split()
    if subprocess.call(wrangler + ["deploy"], cwd=ROOT, env=wrangler_env()) != 0:
        sys.exit("the deploy failed after the records were deleted: run scripts/cutover.py --undo")

    # Resolvers may hold the old addresses for up to five minutes, and the
    # certificate takes a moment, so wait for Cloudflare to answer each check.
    checks = [
        (f"https://{APEX}/", lambda s, srv, loc: s == 200 and srv.lower() == "cloudflare"),
        (f"https://{APEX}/dispatch-20/", lambda s, srv, loc: s == 200 and srv.lower() == "cloudflare"),
        (f"https://{NEW}/about/", lambda s, srv, loc: s == 301 and loc == f"https://{APEX}/about/"),
        (f"https://{WWW}/about/", lambda s, srv, loc: s == 301 and loc == f"https://{APEX}/about/"),
        (f"https://{WWW}/products/x", lambda s, srv, loc: s == 301 and loc == "https://shop.torc.art/products/x"),
        (f"http://{APEX}/", lambda s, srv, loc: s == 301 and loc.startswith(f"https://{APEX}/")),
        (f"https://{APEX}/products/x", lambda s, srv, loc: s == 301 and loc == "https://shop.torc.art/products/x"),
    ]
    for url, good in checks:
        for _ in range(40):
            try:
                s, srv, loc = get(url)
            except Exception as e:  # certificate not issued yet, connection reset
                s, srv, loc = 0, repr(e)[:60], ""
            if good(s, srv, loc):
                print(f"ok   {url} -> {s} {loc or srv}")
                break
            time.sleep(15)
        else:
            print(f"WAIT {url} -> {s} {loc or srv} (this resolver may still hold the old address)")
    print("next: README.md § cutover, the steps after the script")


def undo():
    if not os.path.exists(SAVED):
        sys.exit(f"{os.path.relpath(SAVED, ROOT)} is missing; nothing to put back")
    for host in (APEX, NEW, WWW):
        for d in cf("GET", f"/accounts/{ACCOUNT}/workers/domains?hostname={host}"):
            if d.get("service") == WORKER:
                cf("DELETE", f"/accounts/{ACCOUNT}/workers/domains/{d['id']}")
                print(f"detached {host} from {WORKER}")
    present = {(r["type"], r["name"], r["content"]) for r in name_records()}
    for r in json.load(open(SAVED)):
        if (r["type"], r["name"], r["content"]) in present:
            continue
        cf("POST", f"/zones/{ZONE}/dns_records",
           {"type": r["type"], "name": r["name"], "content": r["content"], "ttl": r["ttl"], "proxied": r["proxied"]})
        print(f"restored {r['type']} {r['name']} {r['content']}")
    print("Shopify and GitHub Pages answer again once resolvers catch up (up to five minutes).")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--undo"]:
        undo()
    elif args == ["--check"]:
        sys.exit(1 if old_records() else 0)
    elif not args:
        cut_over()
    else:
        sys.exit(__doc__)
