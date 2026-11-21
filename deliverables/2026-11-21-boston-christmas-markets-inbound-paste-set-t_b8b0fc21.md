# /boston-christmas-markets/ — the two live-page inbound placements, paste-ready

**Card:** `t_b8b0fc21` (wl-writer) · **Branch:** `content/boston-christmas-markets-20261121`
**Written:** 2026-11-21 · Target of both links: `https://www.quincy-market.com/boston-christmas-markets/`

## Why two of the four placements are in this file and not in the commit

The §5 inbound plan names four source pages. Two of them exist in this repository and are committed
on the branch (`index.html`, `boston-food-and-markets.html`). The other two **have no file in the
repo at all** — they are WordPress pages served by Divi:

| source page | file on this branch? | live |
|---|---|---|
| `/` | `index.html` — **added on the branch** | 200 |
| `/boston-food-and-markets/` | `boston-food-and-markets.html` — **added on the branch** | 200 |
| `/quincy-market-boston-events/` | **none** | 200 (WordPress) |
| `/markets-in-boston-ma/` | **none** | 200 (WordPress) |

This repo is drafts only (`README.md`, and the standing rule
`rules/2026-10-06-pantheon-rome-wordpress-repo-is-drafts-only.md`): merging a PR here publishes
nothing. A commit cannot de-orphan the new page; the WordPress paste does.

Both "before" strings below were read from the live HTML on **2026-11-21** with a browser user agent,
and each occurs **exactly once** on its page (`str.count()` in Python):

```
GET https://www.quincy-market.com/quincy-market-boston-events/   → 166,697 B, anchor count = 1
GET https://www.quincy-market.com/markets-in-boston-ma/          → 167,005 B, anchor count = 1
```

## Placement 1 — `/quincy-market-boston-events/`

Anchor: **the other Christmas markets in Boston, with dates**

The events page is a single Divi code block holding an `<ul class="event-list">` of dated events.
The insertion goes immediately after that list closes, inside the same code block.

**Before** (unique on the page):

```
</ul>

<style>
```

**After:**

```
</ul>
<p>Four other Christmas markets run in Boston in 2026, indoors and out: <a href="https://www.quincy-market.com/boston-christmas-markets/">the other Christmas markets in Boston, with dates</a> — Snowport, the SoWa Christmas Market, the Harvard Square Holiday Fair and the Downtown Boston Seasonal Market.</p>

<style>
```

## Placement 2 — `/markets-in-boston-ma/`

Anchor: **which Boston market is on which December weekend**

The markets hub ends its farmers-market section with the South End Farmers Market at SoWa. The
insertion goes straight after that market's address/hours paragraph, before the empty spacer
paragraph that closes the block.

**Before** (unique on the page):

```
Opening hours: Sun 10:00am &#8211; 4pm</p>
```

**After:**

```
Opening hours: Sun 10:00am &#8211; 4pm</p>
<p>In December most of these close for the season and the city's markets move onto a Christmas timetable. <a href="https://www.quincy-market.com/boston-christmas-markets/">Which Boston market is on which December weekend</a> sets out Snowport, the SoWa Christmas Market, the Harvard Square Holiday Fair, the Downtown Boston Seasonal Market and the Holiday Market at Quincy Market, with 2026 dates, hours and which ones are indoors.</p>
```

## Order of operations, and the one thing that breaks

1. Publish `https://www.quincy-market.com/boston-christmas-markets/` in WordPress first. Both links
   above 404 until the page exists at that URL.
2. Then paste the two placements.
3. The page links to `https://www.quincy-market.com/quincy-market-christmas/`, which returns **404
   live today** even though it is merged in this repo (PR #17, `a80e1b3`) — the Christmas page has
   not been pasted into WordPress. **Publish the two Christmas pages in the same WP session**, or
   the pair carries a dead link in both directions. This is stated again in the PR body.
