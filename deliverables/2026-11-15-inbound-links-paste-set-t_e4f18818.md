# PR #17 — the four inbound placements, as paste-ready WordPress edits

**Card:** `t_e4f18818` (wl-production) · **PR:** raymondlowe/quincy-market.com#17 · **Written:** 2026-11-15T11:19Z

## Read this first — why this file and not four HTML commits

PR #17's premise says "add links from the four existing pages … on the PR's own branch". Three of
the four source pages **have no file in this repository**, and the fourth has a file that is **not
the live page**:

| source | file on the PR branch? | what the live URL actually serves |
|---|---|---|
| `/` | `index.html` — **a different document** (draft title "Quincy Market Boston — Historic Food Hall…"; live `<title>` is "Quincy Market \| All about the historic Quincy Market in Boston") | WordPress 7.1.4, Divi |
| `/quincy-market-boston-events/` | **none** | WordPress 7.1.4, Divi |
| `/whats-inside-quincy-market/` | **none** | WordPress 7.1.4, Divi |
| `/quincy-market-hours/` | **none** | WordPress 7.1.4, Divi |

This repo is **drafts only** — `README.md` on `chore/repo-is-drafts-only-readme-20261014` and the
standing rule `rules/2026-10-06-pantheon-rome-wordpress-repo-is-drafts-only.md`: *"No repo change may
be presented as a live fix, and no PR merge on these repos publishes anything."* Publication is
WordPress (profile `wl-wp`).

So: the home placement is committed in-repo against the home **draft** (`index.html`), and the four
**live** edits are specified below as exact before/after strings, ready to paste into the WordPress
pages. Applying them is what de-orphans the live page; committing here does not.

Anchors below are **wl-seo's signed set** (PR #17 comment, card `t_7a3786a6`, signed head
`ff64097`), not the writer's earlier wording in the PR body — three of the four labels differ
("Holiday Market" capitalised, and different text on `/whats-inside-…/` and `/quincy-market-hours/`).

Every "before" string was copied out of the live HTML read **2026-11-15T11:16Z**, browser UA:

| page | sha256 of the bytes read |
|---|---|
| `https://www.quincy-market.com/` | `80389524b2099ca7c0d28229fd04d68250f8f4ba3baf01481220d18326621953` |
| `https://www.quincy-market.com/quincy-market-boston-events/` | `46f9b7cbc431b665b120190ccb8bf682d3f56c7ad60e47c8818426e3a389a17b` |
| `https://www.quincy-market.com/whats-inside-quincy-market/` | `cc6a4de2416a711a541b0f41aeb1f5064b81152365eb0d1509f00ce80fce69f8` |
| `https://www.quincy-market.com/quincy-market-hours/` | `c1c26527edd84caa6899fad104b74cab36d9219a80d1e3b06891469e1ee1e103` |

Target of all four: `https://www.quincy-market.com/quincy-market-christmas/` — absolute,
trailing-slash, per the ruled live link form (`.html` 404s on this host; the WordPress permalink is
the only live form). **That URL is 404 until `/quincy-market-christmas/` is published.** Paste these
only at or after publication, never before — otherwise all four placements become live 404 links.

---

## 1. `/` (home) — new seasonal line in the intro text module

Widget: `et_pb_text_1` (the centred intro pair under "QUINCY MARKET / VISIT TODAY").

**Before** (last line of that module's inner div):

```html
<p style="text-align: center;">Not sure whether Quincy Market and Faneuil Hall are the same place? They are two separate buildings at opposite ends of one block — <a href="https://www.quincy-market.com/quincy-market-vs-faneuil-hall/">the two buildings, compared</a>.</p></div>
```

**After:**

```html
<p style="text-align: center;">Not sure whether Quincy Market and Faneuil Hall are the same place? They are two separate buildings at opposite ends of one block — <a href="https://www.quincy-market.com/quincy-market-vs-faneuil-hall/">the two buildings, compared</a>.</p>
<p style="text-align: center;">Christmas 2026: the Holiday Market on the second floor is five separate windows, not one continuous run, and the tree is lit on Saturday 21 November at 18:00. Our <a href="https://www.quincy-market.com/quincy-market-christmas/">Christmas at Quincy Market: the 2026 dates and the tree lighting</a> sets out the dates and what is open on each day.</p></div>
```

Why here: the live home page contains **0** occurrences of "Christmas" (counted in the bytes above)
while carrying 75 impressions for `christmas market boston`. The two facts in the line — five
separate windows, tree lit 21 Nov 2026 at 18:00 — are both `CLEAR` rows in wl-factcheck's ruling of
2026-11-15; nothing else is asserted.

---

## 2. `/quincy-market-boston-events/` — the calendar's first entry

**No duplicate removal is owed on this page.** The card's evidence says the events page "ALREADY
repeat[s] the five holiday windows". Measured on the bytes above, it does not: **0** hits for
`November 20`/`22 November`/`24 December`, **0** for `11:00` and **0** for `11am`, **0** for
`second floor`, and the only "Holiday Market" string on the page is "Brighton Bazaar Holiday
Market", a December 2025 event. There is nothing here to replace — only a link to add.

The competing element on this page is instead the entry's own `href`, which sends the tree-lighting
query to `/quincy-market-hours/` — the page that duplicates the windows. This edit repoints it.

**Before** (the `<li>` opening the `ul.event-list` inside `et_pb_code_1`; note the trailing space
after `</a>`, it is in the live source):

```html
  <li>
    <a class="event-link" href="https://www.quincy-market.com/quincy-market-hours/">Quincy Market Holiday Tree Lighting</a> 
    <span class="event-date">Nov 21, 2026</span>
  </li>
```

**After:**

```html
  <li>
    <a class="event-link" href="https://www.quincy-market.com/quincy-market-christmas/">Quincy Market Holiday Tree Lighting</a> 
    <span class="event-date">Nov 21, 2026</span>
    <p><a href="https://www.quincy-market.com/quincy-market-christmas/">the 2026 Christmas dates, the tree lighting and the Holiday Market</a> — the windows, what is open on each day, and Christmas Day.</p>
  </li>
```

Two anchors, one target: the event name, and the signed hand-over text. Both are needed — the
signed anchor is what has to appear, and the event name has to keep working.

---

## 3. `/whats-inside-quincy-market/` — the sentence that promises a URL and names none

**Before** (exact, `&#8217;` as served):

```html
<p>There is no 2026 closure or special-hours notice: the operator&#8217;s 2026 holiday programming is published as events, not as hours.</p>
```

**After:**

```html
<p>There is no 2026 closure or special-hours notice: the operator&#8217;s 2026 holiday programming is published as events, not as hours. The dates and what is open on each day are on <a href="https://www.quincy-market.com/quincy-market-christmas/">Quincy Market&#8217;s 2026 Christmas dates — the Holiday Market on the second floor and the tree lighting</a>.</p>
```

The page has **0** occurrences of "Christmas" today (counted above), so this link is also the page's
only route to the season. wl-seo's anchor says the market is upstairs, which is the fact this page is
about.

---

## 4. `/quincy-market-hours/` — replace the duplicated five windows with the link

This is the **only** page carrying the duplicate. The paragraph below prints all five windows with
their hours plus the lighting time, i.e. the new page's whole answer, in competition with it.

**Before** (exact, in `et_pb_text_5`, the "Holiday Hours and Closures" module — `&#8212;` em dash,
`&#8211;` en dashes, as served):

```html
<p>Separately, the operator runs <strong>seasonal holiday events with their own hours</strong> &#8212; these are events, not changes to the complex schedule. For the 2026 season these include a Holiday Market on the second floor of Quincy Market over several weekends (Friday 20&#8211;Sunday 22 November; Friday 27&#8211;Sunday 29 November; Friday 4&#8211;Sunday 6 December; Friday 11&#8211;Sunday 13 December; Friday 18&#8211;Thursday 24 December 2026, 11:00&#8211;19:00) and the annual Holiday Tree Lighting on Saturday 21 November 2026, 14:00&#8211;18:00.</p>
```

**After:**

```html
<p>Separately, the operator runs <strong>seasonal holiday events with their own hours</strong> &#8212; these are events, not changes to the complex schedule. For the 2026 season that is a Holiday Market on the second floor of Quincy Market and the annual Holiday Tree Lighting; <a href="https://www.quincy-market.com/quincy-market-christmas/">the Christmas dates and what is open on each</a> are on our Christmas page, which carries the five windows and the lighting time.</p>
```

What is removed: the five dated windows, the `11:00–19:00` market hours and the
`14:00–18:00` lighting time. What is kept: that these are events rather than schedule changes (which
is this page's actual subject), the fact that both exist in 2026, and a pointer that names what the
reader will find.

**Reader cost, stated rather than hidden:** before this edit a reader on the hours page could read
the five windows and the lighting time without a click; after it they need one click. That is the
edit the card orders (the duplicate is what competes), and the reader loses nothing that is not on
the linked page — but it is a real cost on a page whose job is answering "when".

**Placement note.** wl-seo named "Closed on Thanksgiving Day and Christmas Day." as this page's host
sentence. That bullet is in the **Faneuil Hall Visitor Center / Great Hall** list (National Park
Service building hours), so a market-Christmas link there would sit inside a different building's
schedule. This paragraph is the page's holiday-events paragraph and is where the duplication lives,
so the anchor goes here instead. The signed **anchor text** is unchanged.

---

## Not done here, and why

- **No sitemap, meta, canonical, robots or schema work.** Block list, `~/wl-knowledge/BLOCKLIST.md`.
- **The page's body still carries wl-factcheck's blocking EDIT ORDER** (PR #17 comment, card
  `t_884303ce`, three exact replacements for the 26 November row, the weekday `<li>` and the "one
  date" clause). Not applied here — this card's work order is the four inbound placements and does
  not name it. As of 2026-11-15 no card exists for applying it; PR #17 stays draft and merge-held
  until a `CLEAR` is recorded at a head carrying those three edits.
- **Observation for the factcheck lane, not actioned:** `/quincy-market-hours/` states the
  marketplace was closed on Thanksgiving Day and Christmas Day "in both 2024 and 2025". wl-factcheck
  measured that the operator carries exactly two "property closed" notices and both are stamped
  **2025** (`…/do/thanksgiving-property-closed`, `…/do/christmas-property-closed`, 2026-11-15). The
  2024 half of that sentence is not supported by the notices that exist.
