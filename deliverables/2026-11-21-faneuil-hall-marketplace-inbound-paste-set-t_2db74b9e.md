# /faneuil-hall-marketplace/ — the three live-page inbound placements, paste-ready

**Card:** `t_2db74b9e` (wl-writer) · **Branch:** `content/faneuil-hall-marketplace-20261121`
**Written:** 2026-11-21 · Target of all three links: `https://www.quincy-market.com/faneuil-hall-marketplace/`

## Why these three are paste instructions and not commits

The §5 inbound plan names five source pages. Two exist in the repo and are committed on this branch
(`index.html`, `quincy-market-vs-faneuil-hall.html`). The other three **have no file in this
repository** — they are WordPress/Divi pages, and this repo is drafts only, so a merge here
publishes nothing. The links only exist once they are pasted into those three pages.

| source page | file on this branch? | live status 2026-11-21 |
|---|---|---|
| `/` | `index.html` — **added on the branch** | 200 |
| `/quincy-market-vs-faneuil-hall/` | `quincy-market-vs-faneuil-hall.html` — **added on the branch** | 200 |
| `/shopping/` | **none** | 200 (WordPress) |
| `/restaurants-and-eateries-in-quincy-market/` | **none** | 200 (WordPress) |
| `/markets-in-boston-ma/` | **none** | 200 (WordPress) |

Each "before" string was read from the live HTML on 2026-11-21 with a browser user agent and occurs
**exactly once** on its page (`str.count()`):

```
GET https://www.quincy-market.com/shopping/                                  → 158,509 B, anchor count = 1
GET https://www.quincy-market.com/restaurants-and-eateries-in-quincy-market/ → 166,007 B, anchor count = 1
GET https://www.quincy-market.com/markets-in-boston-ma/                      → 167,005 B, anchor count = 1
```

## Placement 1 — `/shopping/`

Anchor: **which building each shop is in**

**Before** (only the tail of the paragraph the sentence follows):

```
other interesting and unique products.</p>
```

**After:**

```
other interesting and unique products.</p>
<p>Every shop here sits in one of four buildings, and which one decides where you walk: <a href="https://www.quincy-market.com/faneuil-hall-marketplace/">which building each shop is in</a> covers the North Market, the South Market, Quincy Market and Faneuil Hall, with the shops grouped by building.</p>
```

## Placement 2 — `/restaurants-and-eateries-in-quincy-market/`

Anchor: **the other buildings' restaurants**

**Before:**

```
and the full counter roster.</p>
```

**After:**

```
and the full counter roster.</p>
<p>Most of what is listed here is on the Quincy Market colonnade; if you want a table rather than a counter, <a href="https://www.quincy-market.com/faneuil-hall-marketplace/">the other buildings' restaurants</a> has the sit-down places in the North and South Market buildings and in the Quincy Market building itself.</p>
```

## Placement 3 — `/markets-in-boston-ma/`

Anchor: **the Marketplace is one of Boston's markets**

**Before:**

```
1-minute drive or 4-minute walk from the Quincy Market.</p>
```

**After:**

```
1-minute drive or 4-minute walk from the Quincy Market.</p>
<p>Faneuil Hall Marketplace is one of Boston's markets too — four buildings on that same block, with the food hall in Quincy Market and the shops in the North and South Market buildings. <a href="https://www.quincy-market.com/faneuil-hall-marketplace/">The Marketplace is one of Boston's markets</a> sets out which building holds what.</p>
```

## Order of operations

1. Publish `https://www.quincy-market.com/faneuil-hall-marketplace/` in WordPress first; all three
   links above 404 until the page exists at that URL.
2. Then paste the three placements, and re-run the inbound count.

## Guardrail this PR must respect (deck §3.3)

The new page must not become a second directory. It prints counts and a handful of named examples
per building, and links out to `/shopping/` and `/restaurants-and-eateries-in-quincy-market/` for the
lists. If GSC later shows `quincy market directory` impressions moving off those two pages and onto
the new URL, the fix is a 301 into `/shopping/` — reported by wl-seo, decided by wl-production — not
more content here.
