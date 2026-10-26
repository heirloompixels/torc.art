// The only code in front of the Zola build. new.torc.art was the site's
// address while it was on GitHub Pages, and torc.art and www.torc.art 301'd to
// the shop until this Worker took them, so every kind of old link is sent on.
// The zone does not force https (always_use_https would change every
// subdomain), so the Worker does. Everything else goes to the static assets
// and the 404 page.
const APEX = 'torc.art';
const SHOP = 'shop.torc.art';
const OLD_HOSTS = new Set([`new.${APEX}`, `www.${APEX}`]);

// Shopify's own paths. Before the cutover torc.art/<anything> landed on the
// shop with its path kept; these are the ones that ever meant something there.
// Checked before the host, so www.torc.art/products/x reaches the shop in one hop.
const SHOP_PATHS = /^\/(products|collections|cart|checkouts?|account|pages|blogs|policies|search|apps|cdn)(\/|$)/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (SHOP_PATHS.test(url.pathname)) {
      url.hostname = SHOP;
      url.protocol = 'https:';
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }
    // workers.dev and a local preview are left alone, so a build can be checked.
    if (OLD_HOSTS.has(url.hostname) || (url.hostname === APEX && url.protocol === 'http:')) {
      url.hostname = APEX;
      url.protocol = 'https:';
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }
    // intentionallyconfusing.com's feed was /rss/; the redirects keep its path.
    if (url.pathname === '/rss/' || url.pathname === '/rss') {
      url.pathname = '/rss.xml';
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
