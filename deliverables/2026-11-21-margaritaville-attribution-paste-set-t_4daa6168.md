# Margaritaville attribution — the one-sentence WordPress paste, re-cut off `main`

**Card:** `t_4daa6168` (wl-copy-editor) · **Supersedes:** raymondlowe/quincy-market.com#21 · **Written:** 2026-11-21Z
**Cut from:** `origin/main` @ `706e24152a92dca6c9ea398b3261427c55b80a36` (merge-base = that same commit: the branch is main plus one file)

## Read this first — the change cannot travel as a page commit

PR #21 stacked the same correction on `content/whats-inside-quincy-market-20261109`, a branch that is **not
contained in `main`** — measured today:

    $ gh api repos/raymondlowe/quincy-market.com/compare/main...content/whats-inside-quincy-market-20261109
    status: diverged · ahead_by: 1 · behind_by: 26 · merge_base: 01fc9f35e10e06a6110c2901fa0c8f83a8bd32ec

A one-line fix stacked on a base that will never land cannot itself land; and if the paste were taken from PR
#21's bytes, it would carry a 26-commit-old version of the page into WordPress. So this branch is cut from `main`
and carries **no page file at all**.

`whats-inside-quincy-market.html` **has no file on `main`** (`git ls-tree -r --name-only origin/main | grep -i
whats-inside` → 0 rows). The only copy in the repository lives on that unmerged content branch and on PR #21's
head. This repository is drafts-only — the README and the standing rule say a merge here publishes nothing, and
the live page is WordPress (7.1.4, Divi), published by profile `wl-wp`.

So the correction travels the way this repository's other live edits do: as an exact before/after paste pair,
applied by hand in WordPress. Same form as `deliverables/2026-11-15-inbound-links-paste-set-t_e4f18818.md`.

## The served page, re-read 2026-11-21T09:45Z

| | |
|---|---|
| URL | `https://www.quincy-market.com/whats-inside-quincy-market/` |
| Status | **200** |
| Body bytes | **163,869** (gzip/zstd-decoded, three fetches, identical length) |
| Page sha256 | **not stable** — three fetches in the same minute gave `430b9049…`, `cedf9bbe…`, `da701156…` |

The page-level hash is not a usable handle: each response carries per-request hex tokens (nonces /
cache-busters) in its inline scripts, so the bytes move while the copy does not. The stable handle is the
sentence itself, hashed below. (An earlier note on this card quoted `149,021 B` / `ad844681…` for the same URL;
that figure is not reproducible here and no longer describes the page — the byte count above matches the
163,869 B recorded by `t_eced71dc`.)

**The defect is still there, unchanged.** On today's served bytes the old sentence occurs **exactly once**
(plain-text occurrence count: 1). No STOP condition; nothing has been pasted over.

## The edit — replace one paragraph

Locate the paragraph that **starts** `<p>The counters do not publish hours of their own:` and **ends**
`are not the hall&#8217;s.</p>` — it is the third paragraph after the building-wide hours table, immediately
above the "There is no 2026 closure or special-hours notice" paragraph. It is 260 characters long in the served
form and contains the hours sentence plus the one sentence being replaced.

| handle | before | after |
|---|---|---|
| paragraph sha256 (served form) | `48fa049ccd1f6fa67e79cf5047bcbac60ebabafa7dbaf78d9636b467771d84b7` | `166b16a4086c8819f31ec889940e2765353804cec9bc5cae3a82a51e463e6827` |
| sentence sha256 (plain text) | `9c90ea252b183c9d8baabd31e0b36ff13a9b5e749d36d20f4c0f407a77a0f1d8` | `2009f019412311b55190cd93d1da882ea3c91ef4515336200019ca48ac253dca` |

Byte delta: **+22 B** (163,869 → 163,891 on the same fetch). Character offset of the sentence in that fetch:
146,695 — indicative only, it shifts with the nonce lengths; use the paragraph anchor.

### The payload — paste ONE of these two forms

Both are the same sentence. Use the first in the WordPress **visual/text editor** as plain text; use the second
only if you are editing the **HTML/code** tab, where the rest of the page writes its apostrophes as `&#8217;`.

Plain form:

```
The exception is the restaurant Margaritaville, which the operator lists separately at daily 11am to midnight — a reminder that a restaurant’s hours are not the hall’s.
```

Served HTML form (the sentence as it lands in the page source, escaping only the two apostrophes):

```html
The exception is the restaurant Margaritaville, which the operator lists separately at daily 11am to midnight — a reminder that a restaurant&#8217;s hours are not the hall&#8217;s.
```

Leave the preceding sentence — "The counters do not publish hours of their own: their pages carry that same
building-wide block." — untouched. The replacement carries the em dash as a literal character, as the page
already does.

## Verification

| measure | on the served bytes (before) | on those bytes with the payload applied (after) | on this committed file |
|---|---|---|---|
| old sentence, plain form | 1 | **0** | **0** |
| old sentence, served/entity form | 1 | **0** | **0** |
| new sentence, plain form | 0 | **1** | **1** |
| new sentence, served/entity form | 0 | **1** | **1** |
| `qc_html.py` | 0 FAIL · 2 WARN | 0 FAIL · 2 WARN | n/a (not a page) |
| `voice_redflags.py` | 0 RED · 4 AMBER | 0 RED · 4 AMBER | n/a (not a page) |

The "after" column is the fetched live HTML with this one sentence swapped — the page as it will read once the
paste is made — not a claim that the live site has changed.

Reproduce:

    P=~/.hermes/profiles/wl-copy-editor/skills
    curl -sS --compressed -o live_page.html https://www.quincy-market.com/whats-inside-quincy-market/
    # live_after.html = live_page.html with the payload applied to that one paragraph
    python3 $P/deliverable-qc/scripts/qc_html.py live_page.html            # 0 FAIL, 2 WARN
    python3 $P/wl-house-style/scripts/voice_redflags.py live_page.html     # 0 RED, 4 AMBER
    python3 $P/wl-house-style/scripts/voice_redflags.py live_after.html    # 0 RED, 4 AMBER

The two `qc_html.py` WARNs (`missing-meta-description`, `loader-without-client`) are present before and after and
are meta/ad-plumbing rows — the estate block list, untouched. The four `voice_redflags.py` AMBERs are pre-existing
on the live page (three dated-currency "read on 9 November 2026" lines and one "no published seat count") and are
outside this card's one-sentence scope; reported to the director, not changed here.

## Internal consistency

The table three paragraphs above the sentence already prints `Margaritaville (North Market building restaurant) |
Daily 11am–midnight`, and the operator's building-wide block above it prints `Mon–Sat 10am–9pm · Sun 11am–7pm`.
The new sentence agrees with both: it attributes the later closing to the operator's separate listing and does
not restate the hall's hours. No figure changes in this edit — 11am to midnight is the same figure the page
already prints; only the attribution moves from "the restaurant publishes its own" to "the operator lists it
separately". That attribution rests on the two primaries `t_eced71dc` re-read (operator listing
`faneuilhallmarketplace.com/go/margaritaville`, "Daily: 11am-Midnight"; the restaurant's own page, which is
stale) and is **not** re-verified here — wl-factcheck owns that.

## What this does and does not do

- Merging this PR publishes **nothing**. The live page keeps the old sentence — and keeps telling readers the
  restaurant publishes hours its own page contradicts — until the pair above is pasted into WordPress.
- The paste belongs to `wl-wp`. One sentence, one paragraph, no restructuring, no new page.
- PR #21 is superseded, not repaired: its base branch is 26 commits behind `main` and diverged. Closing it is
  Raymond's/Winnie's call; this branch does not touch it.
