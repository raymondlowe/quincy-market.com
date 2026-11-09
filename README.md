# quincy-market.com — drafting repository

## Read this first

The live site **https://www.quincy-market.com/ is a WordPress site** (WordPress 7.1.4,
Cloudflare-fronted). **Nothing in this repository is served.** This repo is a drafting surface —
a place to hold new material while it is written, checked and reviewed — and *not* a publication
target.

Consequences, and they are the reason this file exists:

- **A commit or a merged pull request here does not change the live site.** No repo change fixes
  anything for readers, and no PR may be described as a live fix.
- **Do not source live URLs, prices or vendor lists from this repo.** Its `.html` URL shape is not
  the live URL shape (WordPress permalinks are extensionless), and its contents are unpublished
  drafts that may be stale or superseded.
- **Publication happens in WordPress** (profile `wl-wp`). Material meant to reach readers is
  published there. When a draft from this repo is published, anything the draft carries — its
  images, its attribution, its structure — has to travel with it into WordPress.
- **Do not delete the drafts once published.** They are the record of what was written and the
  source for any later re-publication.
- **Do not deploy this repository** — not the drafts, and not its `sitemap.xml` or `robots.txt`.
  The live sitemap is WordPress's own. See "Do not deploy this repository" below.

Standing rule, which names this site explicitly:
`~/wl-knowledge/rules/2026-10-06-pantheon-rome-wordpress-repo-is-drafts-only.md` (Raymond,
2026-10-06):

> "For all five: the GitHub repo, where one exists, is **drafts only**. No repo change may be presented as a live fix, and no PR merge on these repos publishes anything."

> "**Publication path:** material that is meant to reach readers is published in **WordPress** (profile `wl-wp`), not by merging a PR in this repo."

## What the live site actually serves (measured 2026-11-08)

| URL | Status |
|---|---|
| `https://www.quincy-market.com/` | 200 — WordPress (`<meta name="generator" content="WordPress 7.1.4">`) |
| `https://www.quincy-market.com/quincy-market-food-guide.html` | **404** (this repo's food guide is not published) |
| `https://www.quincy-market.com/quincy-market-food-guide/` | **404** |
| `https://www.quincy-market.com/best-food.html` | **404** |
| `https://www.quincy-market.com/best-food/` | 200 — a live WordPress page on the same subject, but **a different document** from this repo's `best-food.html` |
| `https://www.quincy-market.com/index.html` | **404** |
| `https://www.quincy-market.com/how-to-get-to-quincy-market.html` | **404** |
| `https://www.quincy-market.com/quincy-market-vs-faneuil-hall.html` | **404** |
| `https://www.quincy-market.com/boston-markets-faq.html` | **404** |
| `https://www.quincy-market.com/restaurants-and-eateries-in-quincy-market/` · `/shopping/` · `/dog-friendly-quincy-market/` | 200 — WordPress pages with no file in this repo |

`https://www.quincy-market.com/wp-sitemap.xml` resolves to **one** child sitemap
(`wp-sitemap-posts-page-1.xml`, **31 page URLs**). No `.html` filename appears among them, and
**29 of the 31 URLs have no file here** — the two that do, `/` and `/best-food/`, are served by
different WordPress documents.

## What is in here, and its publication status

| Path | What it is |
|---|---|
| `index.html` | draft — the live `/` is a different document |
| `best-food.html` | draft — a live `/best-food/` page exists on the same subject and is a different document |
| `quincy-market-food-guide.html` | draft — **not published anywhere** (`/quincy-market-food-guide/` is 404). `origin/main` carries the fact-checked copy; the corrected body is ruled to publish onto the live `/best-food/` page, not at its own URL |
| `how-to-get-to-quincy-market.html` | draft — not published; the live site carries separate `/quincy-market-parking/` and `/quincy-market-public-transport/` pages |
| `quincy-market-vs-faneuil-hall.html` | draft — not published anywhere |
| `boston-markets-faq.html` | draft — not published; the live site's related page is `/markets-in-boston-ma/` |
| `boston-food-and-markets.html` | draft — not published (`/boston-food-and-markets.html` is **404**) |
| `things-to-do-in-boston.html` | draft — not published (`/things-to-do-in-boston.html` is **404**) |
| `quincy-market-freedom-trail.html` | draft — not published (`/quincy-market-freedom-trail.html` is **404**) |
| `styles.css`, `mobile.css`, `fonts.css`, `jquery.min.js`, `*.ttf` | shared static assets for the drafts; **not on the host** |
| `.private/tools/dwt_tool.py` | template-sync tooling. This site carries no Dreamweaver template marker, so the sync is a no-op here |

## Where the facts of record are

Not in this repo. Facts, prices and vendor line-ups are verified by wl-factcheck in
`~/wl-knowledge/sites/quincy-market/facts.yaml` (appended by card, with a `verified_date` and a
confidence per fact), and the site's rulings live in `~/wl-knowledge/sites/quincy-market/findings/`.
This repo's drafts are downstream of those, not a source of truth for them.

If you are working from the estate clone at `~/wlmedia-sites/quincy-market.com`, check it against
`origin/main` **before** reading anything out of it: on 2026-11-08 it was checked out on
`articles/quincy-hours-20261027` (`e074f96`) — 1 commit ahead of and 1 behind `origin/main`
`01fc9f35` — and a clone's checked-out branch is not `main`. Read the remote, not the clone.

## Working rules for this repo

- One draft PR per branch, opened as a draft. Human merge only — agents never merge.
- Do not present a change here as a live outcome; if a change needs to reach readers, it belongs in
  WordPress.
- Internal structure, copy, image provenance and the drafts themselves are fair game to work on.

### Do not deploy this repository

Copying these files into the WordPress docroot is not a publish step. Do not add the nine `.html`
files to the web root, do not add a root `.htaccess`, and do not purge Cloudflare for this domain.

The concrete proposal — `DirectoryIndex index.html index.php` plus a `^<slug>/$ → <slug>.html`
rewrite — was refused on 2026-11-08:
`~/wl-knowledge/pipeline/director/2026-11-08-quincy-htaccess-deploy-refused-t_8028ff0c.md`.
Re-measured 2026-11-09:

- **The build covers 2 of the 31 live page URLs.** `wp-json/wp/v2/pages` reports `X-WP-Total: 31`
  and `wp-sitemap-posts-page-1.xml` carries 31 `<loc>` entries; this repo has nine `.html` files,
  and only `/` (`index.html`) and `/best-food/` (`best-food.html`) name a URL the live site serves.
  **29 of the 31 live URLs have no file here.** A docroot holding this build would answer for nine
  documents where WordPress answers for 31.
- **Those two URLs are the property's traffic.** Search Console,
  `https://www.quincy-market.com/`, 2026-08-09 → 2026-11-06, 39 page rows: `/` = 27,056 clicks /
  379,853 impressions; `/best-food/` = 804 / 129,312 — together 27,860 of the window's 35,982
  clicks (77.4%).
- **Neither draft is the live document.** `/` is
  `<title>Quincy Market | All about the historic Quincy Market in Boston</title>`, 263,673 bytes;
  `index.html` is `<title>Quincy Market Boston — Historic Food Hall at Faneuil Hall Marketplace</title>`,
  5,743 bytes. `/best-food/` is `<title>Best Food | Quincy Market</title>`, 150,486 bytes;
  `best-food.html` is `<title>Quincy Market Boston 2027 — Complete Food Guide with Price List</title>`,
  20,362 bytes. `DirectoryIndex index.html index.php` serves the second at `/` the moment it is on
  disk, and the rewrite serves the draft at `/best-food/`.
- **Ad units are removed as a side effect.** The live `/` carries three hand-placed
  `<ins class="adsbygoogle">` units and the live `/best-food/` carries two; neither draft carries
  any — they carry the Auto Ads loader only. A revenue change arriving inside an infrastructure
  edit is what the AdSense rule exists to stop.
- **The sitemap and robots file are draft material too.** The live sitemap is WordPress's own:
  `/sitemap.xml` 301s to `/wp-sitemap.xml`, which lists one child,
  `/wp-sitemap-posts-page-1.xml`, with 31 page URLs. Do not copy a `sitemap.xml` or `robots.txt`
  from this repo into the docroot, and do not give this repo a build step that generates them: a
  hand-maintained file here names fewer URLs than WordPress already advertises.

What is owed on this site is not a host action. Publication runs through WordPress (profile
`wl-wp`), and the credential that unblocks the publication queue is tracked in card `t_b7b886cf`.
