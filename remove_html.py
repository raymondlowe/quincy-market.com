#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""remove_html.py v2.1.0 - the estate build step.

Version history
  2.0.0  build-time ``sitemap.xml`` + the ``sitemap.html`` list region.
  2.0.1  the ``sitemap.html`` list region is narrowed to a reader-facing wayfinding view
         of the loc set: photo leaves (camera filenames, ``/pages/`` leaves, leaves under a
         photo-container segment) are omitted from the HTML index. ``sitemap.xml`` is NOT
         narrowed - it keeps the complete loc set. The two sets are deliberately different:
         the XML is for crawlers, the HTML index is for a reader standing on the page.
         Also: ``_label_for()`` keeps acronyms upper-case (HK, MTR, LRT, UNESCO, DWT, GSC,
         HKIA) instead of flattening them to "Hk"/"Mtr".
         Ruling: ``~/wl-knowledge/rules/2026-11-06-sitemap-html-index-narrowed-not-retired.md``
  2.1.0  the UNION of the two lineages, in one canonical file (ruling 2026-11-06). Three
         things that had been living on separate, mutually exclusive branches and had never
         been in the same file:
           * phase 1 gains the R1.1 own-origin guard (ruling 2026-10-16): a scheme-less
             ``href`` is this site's and strips; an absolute or protocol-relative ``href``
             strips only when its host is this site's, resolved from the page's own
             canonical then the checkout directory name, ``www.`` normalised away. A
             citation to another origin keeps its ``.html`` - rewriting another site's
             routing dead-ends the reader on that site.
           * phase 3 is new: under ``CF_PAGES``/``CF_PAGES_URL`` the build-only files -
             ``*-description.txt`` image sidecars and this script itself - are deleted from
             the built tree (ruling 2026-10-06).
           * phase 2 is v2.0.1's sitemap work, unchanged and byte-for-byte the same output.
         Ruling: ``~/wl-knowledge/rules/2026-11-06-remove-html-py-one-canonical-union-of-six-rulings.md``

Runs as the Cloudflare Pages ``build_command`` (``python remove_html.py``) from the
repo root. Three phases, in this order:

PHASE 1 - v1 behaviour, plus the own-origin guard (2.1.0)
  * delete ``.private/`` and ``.github/`` from the build tree;
  * strip the ``.html``/``.htm`` suffix from ``href="..."`` in every ``*.html``/``*.htm``
    (that is what makes this site's links extensionless - Cloudflare Pages 308s a
    ``.html`` path to its extensionless form) - but ONLY for this site's own origin:
    a scheme-less value always strips, an absolute one only when its host is this site's
    (own canonical, then checkout directory name; ``www.`` normalised away). A foreign
    citation keeps its extension, because another origin's routing is not ours to rewrite;
  * preserve ``google-site-verification`` files verbatim.

PHASE 2 - build-time sitemaps (new in 2.0.0)
  * ``sitemap.xml`` from the BUILT page set - the tree as phase 1 has just left it, so
    the canonical each page carries is the canonical that is actually served;
  * the list region of ``sitemap.html``, but ONLY between
    ``<!-- #BeginSitemapList -->`` and ``<!-- #EndSitemapList -->``. No markers, no edit;
  * that region carries the *wayfinding* subset of the loc set - photo leaves are omitted
    (``_is_photo_leaf``), because a reader cannot recognise "Dsc 0323" and a crawler does
    not need the HTML index. ``sitemap.xml`` keeps every loc;
  * ``robots.txt`` but ONLY when it is absent or 0 bytes - a non-empty file is never
    overwritten.

PHASE 3 - build-only cleanup (new in 2.1.0)
  * delete every ``*-description.txt`` image-description sidecar from the built tree, and
    then this script itself, from the output tree;
  * ONLY when ``CF_PAGES``/``CF_PAGES_URL`` is set, i.e. only inside the Cloudflare Pages
    build. A local run never deletes anything, so the script stays runnable by hand;
  * ruling 2026-10-06: these are build inputs sitting in the served tree. Without this
    phase ``remove_html.py`` is published and answers 200 on every site.

Loc set: a served page is in the sitemap iff it is not an error document (404/403/500),
not a verification file, not a backup/junk duplicate, does not carry
``<meta name="robots" content="noindex">``, and its canonical resolves to this site's own
host. A page with no canonical is kept, with its URL computed from its path (counted as a
fallback) - a missing canonical is not a reason to de-list a page.

The canonical host is derived from the pages' own canonicals (majority vote), never from
the repo name and never hardcoded ``www``: built on the repo name this script emitted apex
URLs that 301 to ``www`` on 44 measured pages.

``lastmod`` is deliberately not emitted: a shallow build clone yields one commit date for
every file, and a value that changes for every URL on every deploy is worse than no value.
``<changefreq>``/``<priority>`` are ignored by Google and are not emitted either.

A generator failure must never fail the deploy: phase 2 is wrapped and logs a line instead
of raising. Phase 1 keeps v1's own error handling. Phase 3 deletes files and so is the one
place that reports rather than raises too.

Ruling and measurements: ``~/wl-knowledge/rules/2026-11-05-sitemap-generated-at-build.md``
Canonical copy: ``wlmedia-adsense-sites/scripts/python/remove_html.py``
"""

import html
import os
import re
import shutil
import sys
import urllib.parse

VERSION = "2.1.0"

BEGIN_MARK = "<!-- #BeginSitemapList -->"
END_MARK = "<!-- #EndSitemapList -->"

_HTML_EXTS = (".html", ".htm")
_SKIP_DIRS = (".private", ".github", "node_modules")
_ERROR_DOC = re.compile(r"(^|/)(404|403|500)\.(html|htm)$", re.I)
_VERIFY_DOC = re.compile(r"(^|/)(google[0-9a-z]*|pinterest-?[0-9a-z]*)\.(html|htm)$", re.I)
_BACKUP_DOC = re.compile(r"(\.backup$|\.bak$|_old|_copy|~$)", re.I)
_JUNK_DOC = re.compile(r"(^\.[^/]*$|/\.| copy(\.|$)|\([0-9]+\))", re.I)
_LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
_NOINDEX_META = re.compile(
    r"""<meta\b[^>]*\bname\s*=\s*["']?robots["']?[^>]*\bcontent\s*=\s*["'][^"']*noindex""",
    re.I,
)
_HREF_HTML = re.compile(r'href="([^"]*?\.(?:html|htm))"')
_HREF_STRIP = re.compile(r"(\.html|\.htm)$")
_VERIFY_LINE = re.compile(r"^google-site-verification: google.*\.html$")

# --------------------------------------------------------------------------------------
# the HTML-index photo-leaf test (v2.0.1) - ruling 2026-11-06 §4.1, tests (a) (b) (c)
# --------------------------------------------------------------------------------------
_PAGES_SEG = re.compile(r"/pages/", re.I)
_CONTAINER_SEG = re.compile(
    r"^/(gallery|galleries|photos|pictures|images|photo-gallery|album)(/|$)", re.I
)
# (c) anchored at the START of the leaf on purpose. A ``-[0-9]{3}$`` frame suffix is only a
# photo when a camera token precedes it: read with re.search, it also ate a live content
# page (hk-victoria-peak's ``/sky-terrace-428``, lantau-island's ``/ngong-ping-360``).
_CAMERA_LEAF = re.compile(
    r"^(?:dsc|dscn|img|photo|pic)(?:[_-]?\d|[_-][a-z]*\d)"
    r"|^p\d{7}$"                                            # P1234567
    r"|^\d{8}[_-]\d{6}$"                                    # YYYYMMDD_HHMMSS
    r"|^\d{4}-\d\d-\d\d[_-]\d{6}$"                          # YYYY-MM-DD_HHMMSS
    r"|^(?:dsc|dscn|img|photo|pic)[\w-]*-[0-9]{3}$",        # camera token + -NNN frame
    re.I,
)
_UPPER_TOKENS = frozenset(("HK", "MTR", "LRT", "UNESCO", "DWT", "GSC", "HKIA"))


# --------------------------------------------------------------------------------------
# phase 1 - v1 behaviour (do not change: gate 1 of the ruling is byte-equivalence)
# --------------------------------------------------------------------------------------

def remove_private_folders():
    """Delete .private and .github folders in the current directory, as v1 did."""
    for folder in (".private", ".github"):
        folder_path = os.path.join(os.getcwd(), folder)
        try:
            shutil.rmtree(folder_path)
            print("Deleted %s folder: %s" % (folder, folder_path))
        except FileNotFoundError:
            pass
        except Exception as e:  # noqa: BLE001 - v1 behaviour: never fail the build
            print("Failed to delete %s folder: %s" % (folder, e))


def _is_verification_file(filename, text):
    """True for the single-line google-site-verification file v1 refuses to touch."""
    basename = os.path.basename(filename)
    if not (basename.startswith("google") and basename.endswith(".html")):
        return False
    lines = text.strip().splitlines()
    return len(lines) == 1 and bool(_VERIFY_LINE.match(lines[0]))


def _norm_host(host):
    """Lower-case a host and drop a leading ``www.`` so apex and www compare equal."""
    host = (host or "").strip().lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def _url_host(url):
    """Host of an absolute/protocol-relative URL, or None for a relative/scheme-less one."""
    m = re.match(r"^(?:[a-z][a-z0-9+.-]*:)?//(?:[^@/]*@)?([^/:?#]+)", url, re.I)
    return _norm_host(m.group(1)) if m else None


def _own_hosts(text):
    """This page's own host(s): its own canonical first, then the checkout directory name.

    On Pages the cwd is the repo root and the repo name IS the domain, which is why the
    directory is a fallback rather than the primary source - a page states its own host.
    """
    hosts = set()
    canon = _canonical_of(text)
    host = _url_host(canon) if canon else None
    if host:
        hosts.add(host)
    checkout = _norm_host(os.path.basename(os.path.abspath(os.getcwd())))
    if checkout:
        hosts.add(checkout)
    return hosts


def _is_own_origin(url, own_hosts):
    """R1.1 (ruling 2026-10-16, host only): is this href value this site's own?

    Scheme-less values (``/about.html``, ``about.html``) are always ours. An absolute or
    protocol-relative value is ours only when its host is this site's. The file rule was
    removed in R1.1 - host only, no path inspection.
    """
    if not re.match(r"^(?:https?:)?//", url, re.I):
        return True
    host = _url_host(url)
    return host is not None and host in own_hosts


def strip_html_hrefs():
    """Rewrite href="...html|.htm" -> extensionless in every .html/.htm file (v1 behaviour).

    v2.1.0 adds the own-origin guard: the strip exists so THIS site's links are served
    extensionless (Cloudflare Pages 308s a .html path to its extensionless form). Another
    origin's routing is not ours to rewrite - a foreign citation keeps its extension, or
    the reader dead-ends on that site's 404 or a generic hub.
    """
    filenames = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html") or file.endswith(".htm"):
                filenames.append(os.path.join(root, file))

    print("Found %d html files in current directory" % len(filenames))
    print(*filenames, sep="\n")

    for filename in filenames:
        try:
            print("Read file", filename)
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()

            if _is_verification_file(filename, text):
                print("Special case: preserving .html in %s" % filename)
                continue

            own_hosts = _own_hosts(text)

            def remove_html_from_href(match, own_hosts=own_hosts):
                url = match.group(1)
                if not _is_own_origin(url, own_hosts):
                    return match.group(0)  # FOREIGN origin: citation intact, extension kept
                url = _HREF_STRIP.sub("", url)
                return 'href="%s"' % url

            new_text = _HREF_HTML.sub(remove_html_from_href, text)

            with open(filename, "w", encoding="utf-8") as f:
                print("Write file", filename)
                f.write(new_text)
        except Exception:  # noqa: BLE001 - v1 behaviour
            print("failed ", filename)


# --------------------------------------------------------------------------------------
# phase 2 - build-time sitemap generation
# --------------------------------------------------------------------------------------

def _read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _iter_pages(root):
    """Yield rel paths ('/'-separated) of *.html/*.htm in the built tree."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in _SKIP_DIRS)
        for fn in sorted(filenames):
            if fn.lower().endswith(_HTML_EXTS):
                yield os.path.relpath(os.path.join(dirpath, fn), root).replace(os.sep, "/")


def _canonical_of(text):
    for tag in _LINK_TAG.findall(text):
        if not re.search(r"""rel\s*=\s*["']?[^"'>]*canonical""", tag, re.I):
            continue
        m = re.search(r"""href\s*=\s*["']([^"']+)["']""", tag, re.I)
        if m:
            return m.group(1).strip()
    return None


def _normalise(value):
    """(host, path) for a canonical value. Host '' means a site-relative value.

    The path keeps its trailing slash when the canonical declares one: a directory index is
    served at ``.../gallery/`` and the extensionless form ``.../gallery`` 308s to it. The
    canonical is the site's own statement of its served URL, so the generator must not
    "tidy" it into a redirect.
    """
    parts = urllib.parse.urlparse(value)
    host = (parts.netloc or "").lower().rstrip(".")
    path = parts.path or "/"
    path = re.sub(r"\.(html|htm)$", "", path, flags=re.I)
    path = re.sub(r"/index$", "/", path)
    return host, (path or "/")


def _fallback_path(rel):
    """URL path computed from a page's place in the tree (page has no canonical)."""
    path = re.sub(r"\.(html|htm)$", "", rel, flags=re.I)
    if path == "index":
        path = ""
    elif path.endswith("/index"):
        path = path[: -len("index")]
    path = "/" + path.lstrip("/")
    if rel.lower().endswith("index.html") or rel.lower().endswith("index.htm"):
        if path and not path.endswith("/"):
            path += "/"
    return path


def _quote_path(path):
    """Percent-encode a path, tolerating values that are already encoded."""
    return urllib.parse.quote(urllib.parse.unquote(path), safe="/")


def _xml_escape(value):
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _label_for(path):
    trimmed = path.strip("/")
    if not trimmed:
        return "Home"
    slug = trimmed.rsplit("/", 1)[-1]
    label = re.sub(r"[-_.]+", " ", slug).strip().title()
    # str.title() flattens acronyms to "Hk"/"Mtr"/"Unesco"; the index is read by a person.
    label = " ".join(w.upper() if w.upper() in _UPPER_TOKENS else w for w in label.split())
    return label or "Home"


def _is_photo_leaf(path):
    """True iff this loc is a photo leaf and must stay out of the HTML index (v2.0.1).

    Ruling 2026-11-06 §4.1 - three tests, any one of which omits the loc from the HTML
    index. ``sitemap.xml`` is unaffected: it keeps every loc.

      (a) a ``/pages/`` segment anywhere in the path - the estate's convention for a
          photo/pagination leaf directory, which is how a topical section's photo block
          (``/circular-walk/pages/DSC_0171``) is caught;
      (b) a photo-container segment with something after it - the container index itself
          (``/gallery/``, ``/pictures``, ``/photos/``) stays, so the reader keeps one
          recognisable "Gallery"/"Pictures" entry and can walk in;
      (c) the leaf is a camera filename or timestamp.

    A fragment (``#...``) never reaches here - callers pass ``urlparse(url).path``.
    """
    path = path or "/"
    if _PAGES_SEG.search(path):
        return True
    m = _CONTAINER_SEG.match(path)
    if m and path[m.end():].strip("/"):
        return True
    leaf = path.rstrip("/").rsplit("/", 1)[-1]
    return bool(_CAMERA_LEAF.match(leaf))


def _build_locs(root):
    """Walk the built tree and return (locs, stats). Pure: no writes."""
    stats = dict(
        pages=0, locs=0, fallback=0, noindex=0, offhost=0, dups=0,
        junk=0, error_docs=0, verification=0, backups=0, host="",
    )
    candidates = []          # (rel, canonical or None)
    hosts = {}

    for rel in _iter_pages(root):
        if _ERROR_DOC.search(rel):
            stats["error_docs"] += 1
            continue
        if _VERIFY_DOC.search(rel):
            stats["verification"] += 1
            continue
        if _BACKUP_DOC.search(rel):
            stats["backups"] += 1
            continue
        if _JUNK_DOC.search(rel):
            stats["junk"] += 1
            continue

        stats["pages"] += 1
        text = _read(os.path.join(root, rel))
        if _NOINDEX_META.search(text):
            stats["noindex"] += 1
            continue
        canon = _canonical_of(text)
        if canon:
            host, _ = _normalise(canon)
            if host:
                hosts[host] = hosts.get(host, 0) + 1
        candidates.append((rel, canon))

    if hosts:
        # majority host among the pages that do carry a canonical; deterministic tiebreak
        stats["host"] = sorted(hosts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]

    site_host = stats["host"]
    locs, seen = [], set()
    for rel, canon in candidates:
        if canon:
            host, path = _normalise(canon)
            if site_host and host and host != site_host:
                stats["offhost"] += 1
                continue
            url = "https://%s%s" % (host or site_host, _quote_path(path))
        else:
            stats["fallback"] += 1
            if not site_host:
                continue
            url = "https://%s%s" % (site_host, _quote_path(_fallback_path(rel)))

        key = urllib.parse.urlparse(url).path.rstrip("/").lower() or "/"
        if key in seen:
            stats["dups"] += 1
            continue
        seen.add(key)
        locs.append(url)

    locs.sort(key=lambda u: (urllib.parse.urlparse(u).path.count("/"), u))
    stats["locs"] = len(locs)
    return locs, stats


def _write_sitemap_xml(root, locs):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!-- generated at build by remove_html.py v%s from the built canonical set; "
        "do not hand-edit -->" % VERSION,
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in locs:
        lines.append("  <url><loc>%s</loc></url>" % _xml_escape(url))
    lines.append("</urlset>")
    with open(os.path.join(root, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _write_sitemap_html(root, locs):
    path = os.path.join(root, "sitemap.html")
    if not os.path.exists(path):
        return "absent"
    page = _read(path)
    head, sep, tail = page.partition(BEGIN_MARK)
    if not sep:
        return "no-markers"
    body, sep2, rest = tail.partition(END_MARK)
    if not sep2:
        return "no-markers"

    items = []
    for url in locs:
        url_path = urllib.parse.urlparse(url).path or "/"
        if _is_photo_leaf(url_path):
            continue  # wayfinding view, not the crawler set - sitemap.xml keeps this loc
        href = _quote_path(url_path)
        items.append(
            '        <li><a href="%s">%s</a></li>'
            % (html.escape(href, quote=True), html.escape(_label_for(url_path)))
        )
    region = "\n    <ul>\n" + "\n".join(items) + "\n    </ul>\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(head + BEGIN_MARK + region + END_MARK + rest)
    return "rewritten(%d)" % len(items)


def _write_robots(root, site_host):
    if not site_host:
        return "no-host"
    path = os.path.join(root, "robots.txt")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return "kept"
    with open(path, "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://%s/sitemap.xml\n" % site_host)
    return "written"


def generate_sitemaps(root="."):
    """Generate sitemap.xml / the sitemap.html list region / robots.txt. Never raises."""
    stats = dict(
        pages=0, locs=0, fallback=0, noindex=0, offhost=0, dups=0,
        junk=0, error_docs=0, verification=0, backups=0, host="",
        html_index="absent", robots="left",
    )
    try:
        locs, built = _build_locs(root)
        stats.update(built)
    except Exception as e:  # noqa: BLE001 - a generator failure must never fail the deploy
        print("sitemap: generation FAILED (%s: %s) - deploy continues" % (type(e).__name__, e))
        return stats

    if not stats["host"]:
        print("sitemap: no canonical host derivable - generation skipped, deploy continues")
        return stats

    try:
        _write_sitemap_xml(root, locs)
    except Exception as e:  # noqa: BLE001
        print("sitemap: sitemap.xml write FAILED (%s: %s) - deploy continues" % (type(e).__name__, e))

    try:
        stats["html_index"] = _write_sitemap_html(root, locs)
    except Exception as e:  # noqa: BLE001
        stats["html_index"] = "error"
        print("sitemap: sitemap.html write FAILED (%s: %s) - deploy continues" % (type(e).__name__, e))

    try:
        stats["robots"] = _write_robots(root, stats["host"])
    except Exception as e:  # noqa: BLE001
        stats["robots"] = "error"
        print("sitemap: robots.txt write FAILED (%s: %s) - deploy continues" % (type(e).__name__, e))

    print(
        "sitemap: pages=%d locs=%d fallback=%d noindex=%d offhost=%d dups=%d "
        "html_index=%s robots=%s lastmod=omitted"
        % (
            stats["pages"], stats["locs"], stats["fallback"], stats["noindex"],
            stats["offhost"], stats["dups"], stats["html_index"], stats["robots"],
        )
    )
    return stats


def remove_build_only_files():
    """Delete build-only files from the built tree - only inside the Pages build.

    Ruling 2026-10-06: ``*-description.txt`` image-description sidecars are working notes
    that sit in the SERVED image directories, and this script is itself a build input
    living in the output tree. ``CF_PAGES``/``CF_PAGES_URL`` are set by the Cloudflare
    Pages build, so none of this ever touches a local working tree - run by hand, the
    script deletes nothing and stays runnable.
    """
    if not (os.environ.get("CF_PAGES") or os.environ.get("CF_PAGES_URL")):
        return "skipped"
    removed_sidecars = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith("-description.txt"):
                try:
                    os.remove(os.path.join(root, file))
                    removed_sidecars += 1
                except Exception as e:  # noqa: BLE001
                    print("Failed to delete description sidecar %s: %s" % (file, e))
    print("Deleted %d image-description sidecar file(s)" % removed_sidecars)

    try:
        os.remove(os.path.join(os.getcwd(), "remove_html.py"))
        print("Deleted build-only file: remove_html.py")
    except FileNotFoundError:
        pass
    except Exception as e:  # noqa: BLE001
        print("Failed to delete build-only file remove_html.py: %s" % e)
    return "deleted"


def main():
    remove_private_folders()
    strip_html_hrefs()
    generate_sitemaps(".")
    remove_build_only_files()
    return 0


if __name__ == "__main__":
    sys.exit(main())
