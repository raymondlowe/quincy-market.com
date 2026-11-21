# `/boston-public-market-vs-quincy-market/` — Haymarket hours: the two false claims, as paste-ready WordPress edits

**Card:** `t_7b56a800` (copy-edit) · **Written:** 2026-11-21 · **Page:** `https://www.quincy-market.com/boston-public-market-vs-quincy-market/`
**Repo:** raymondlowe/quincy-market.com (drafts only) · **Branch:** `fix/haymarket-hours-window-20261121`

## Read this first — why this file and not a page commit

The page has **no file in this repository and no file on any branch of it**. Measured 2026-11-21 with
`git ls-tree -r --name-only <ref> | grep boston-public-market-vs-quincy-market.html` across every local
and remote branch: zero hits. The served page exists only in WordPress (Divi) and in the publishing
record at
`~/wl-knowledge/sites/quincy-market/findings/evidence/2026-11-12-wp-publish-boston-public-market-t_5225ef74/published-boston-public-market-vs-quincy-market.html`.

This repo is a **drafts surface and nothing here is served** (`README.md` on `main`; standing rule
`rules/2026-10-06-pantheon-rome-wordpress-repo-is-drafts-only.md`). So the correction is specified
below as exact find/replace strings for the WordPress page. Committing here fixes nothing for
readers; the live page keeps both false sentences until the paste is made and the Cloudflare cache is
purged.

## STEP 0 — live page re-fetched, strings unchanged

`curl -sS https://www.quincy-market.com/boston-public-market-vs-quincy-market/` → **200**, **149,021 B**,
sha256 `ad844681ba2c20d7fa0bc25cfd7e2474f78570010a60c65fc0c5df14b6dd94db`.

Each FIND below was `count()`-checked against those bytes and occurs **exactly once**. None of the
three spans contains an apostrophe or any other character WordPress re-encodes, so the **served form
and the editor-source form are byte-identical here** — one pair serves both.

## Why it is wrong

| claim, as served | what the primaries publish (both read 2026-11-21) |
|---|---|
| "There are no official opening hours" | **False.** The operator, the Haymarket Pushcart Association (`haymarketboston.org/new-page`), publishes "HOURS: EVERY FRIDAY // 3:00 AM - CLOSE / EVERY SATURDAY // 4:00 AM - CLOSE". The City of Boston (`boston.gov/departments/food-justice/food-resources`, page last updated **11/12/26**) publishes "Market runs year-round, every Friday and Saturday from 4am-7pm. Bring cash!" |
| "from dawn to dusk" (and "vendors set up from around 6am") | An unsourced hedge in place of a sourced window. The City's **04:00–19:00** is the trading window; the operator's Friday set-up from **03:00** is why a Friday morning looks open before it officially is. Both primaries contradict "around 6am". |

Source of record: `~/wl-knowledge/sites/quincy-market/findings/2026-11-21-haymarket-boston-gate-clearance-t_e3ddd876.md`
§1 and §5 constraints 1–2 (18/18 quotes verified).

**Deliberately not written:** no half-price comparison, no claim that cards are or are not accepted, no
Wikipedia "6 AM to 7 PM", and **no link to `/haymarket-boston/`** — that URL returns 404 today; a
separate card builds the page and the inbound link is owed after it answers 200.

## 1. "Where Haymarket fits" — the body paragraph (the two claims)

OLD (1 occurrence):

```html
It trades on <strong>Fridays and Saturdays only, from dawn to dusk, all year</strong>, on Blackstone Street. There are no official opening hours: vendors set up from around 6am and pack away when they sell out or the weather turns, so a wet Saturday afternoon is not the time to plan around it.
```

NEW:

```html
It trades on <strong>Fridays and Saturdays only, all year</strong>, on Blackstone Street. The City of Boston puts the trading window at <strong>04:00–19:00</strong>; the Haymarket Pushcart Association, which runs the market, opens its Friday set-up at 03:00 — that is why a Friday morning can look open before it officially is. Stalls still pack away when they sell out or the weather turns, so a wet Saturday afternoon is not the time to plan around it.
```

The two flanking sentences are untouched; "all year" is kept in the page's own form.

## 2. The comparison table — Haymarket "Days and hours" cell (same two claims, same page)

This is the same defect in the table that sits directly above the section, and leaving it would put
the page in contradiction with itself (table: dawn-to-dusk / no official hours; prose: 04:00–19:00).

OLD (1 occurrence):

```html
<td>Fridays and Saturdays only, dawn to dusk, all year. No official hours — vendors set up from around 6am and pack away when they sell out or the weather turns</td>
```

NEW:

```html
<td>Fridays and Saturdays only, all year. City of Boston trading window 04:00–19:00 · Friday set-up from 03:00. Stalls pack away when they sell out or the weather turns</td>
```

## 3. "If you only have an hour", step 4 — "before dusk"

Same hedge, one phrase: with a 19:00 close, "before dusk" sends a summer reader after the market has
shut. Consistency-only edit, no new fact.

OLD (1 occurrence):

```html
and worth the detour before dusk if you have a kitchen at the other end.
```

NEW:

```html
and worth the detour before 19:00 if you have a kitchen at the other end.
```

## Form check

Times follow the page's own 24-hour form (`Sun–Tue 08:00–18:00`, `closes at 21:00`) and its en dash.
Voice check: `voice_redflags.py` on the article body → **RED 0 / AMBER 0, CLEAR**; the new sentences add
no process commentary and no source-gap confession.

## Owed elsewhere — not in this card's scope, flagged to the director

- `boston-markets-faq.html` line 63 (FAQ answer, and its JSON-LD twin) still carries "trades on Fridays
  and Saturdays only, from dawn to dusk. There are no official opening hours: vendors set up from
  around 6am…" — the same two false claims on a second indexed page. Needs its own card.
- `boston-food-and-markets.html` line 71 says "The market has no official hours" and then lists them
  in the next clause, and asserts Christmas Day / New Year's Day closures that neither primary
  supports. Needs its own card, fact-checked.
