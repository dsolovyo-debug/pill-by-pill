"""Turn a built Pill by Pill site into one that works on GitHub Pages under a sub-path.

GitHub Pages serves this repo at https://<owner>.github.io/<repo>/, so every root-absolute
path ("/js/app.js", "/data/x.json", <base href="/">) must gain the "/<repo>" prefix.

Usage: python3 prepare_pages.py SITE_DIR --base /pill-by-pill --url https://dsolovyo-debug.github.io/pill-by-pill
       [--underlay BASE_SITE_ZIP]   copy a fully built older site underneath (catalogue data,
                                    medicine pages, images) before the new files go on top.
"""
import argparse, pathlib, re, shutil, sys, tempfile, zipfile

OLD_URLS = ("https://pillbypill.netlify.app",)

def underlay(site: pathlib.Path, zpath: pathlib.Path) -> int:
    """Files in the zip that the new build does not have are added; the new build always wins."""
    added = 0
    with zipfile.ZipFile(zpath) as z:
        for n in z.namelist():
            if n.endswith("/"):
                continue
            rel = n.split("site/", 1)[1] if n.startswith("site/") else n
            dst = site / rel
            if dst.exists():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            with z.open(n) as src, open(dst, "wb") as out:
                shutil.copyfileobj(src, out)
            added += 1
    return added

def fix_missing_imports(site: pathlib.Path) -> list:
    """Point relative ES-module imports at files that exist. A missing module makes GitHub serve its
    HTML 404 page, which Chrome blocks ("strict MIME type checking") and which stops every script."""
    exports = {}
    for js in (site / "js").glob("*.js"):
        for name in re.findall(r"export\s+(?:const|function|let|async function)\s+(\w+)", js.read_text(encoding="utf-8")):
            exports.setdefault(name, js.name)
    fixed = []
    for js in (site / "js").glob("*.js"):
        txt = js.read_text(encoding="utf-8")
        def repl(m):
            names, mod = m.group(1), m.group(2)
            if (js.parent / mod).is_file():
                return m.group(0)
            wanted = [n.strip().split(" as ")[0] for n in names.strip("{} ").split(",") if n.strip()]
            homes = {exports.get(n) for n in wanted}
            if len(homes) == 1 and None not in homes:
                fixed.append(f"{js.name}: {mod} -> ./{homes.pop()}")
                return m.group(0).replace(mod, "./" + exports[wanted[0]])
            sys.exit(f"{js.name} imports {mod}, which does not exist, and {wanted} has no single home")
        txt2 = re.sub(r'import\s*(\{[^}]*\})\s*from\s*["\'](\./[^"\']+)["\']', repl, txt)
        if txt2 != txt:
            js.write_text(txt2, encoding="utf-8")
    return fixed

def prefix_paths(site: pathlib.Path, base: str, url: str) -> None:
    root_abs = r'/(?!/|' + re.escape(base.strip("/")) + r'/)'
    for p in site.rglob("*"):
        if not p.is_file() or p.suffix not in (".html", ".js", ".css", ".xml", ".json", ".webmanifest", ".txt"):
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        new = txt
        for old in OLD_URLS:                      # canonical, og:url, sitemap, feed, share links
            new = new.replace(old, url)
        if p.suffix == ".html":
            new = re.sub(r'(\s(?:href|src|action|content)=["\'])' + root_abs, r'\1' + base + '/', new)
            # inline redirects such as location.replace("/#/ref/adme") in the static encyclopedia pages
            new = re.sub(r'(location\.(?:replace|assign)\(\s*["\'])' + root_abs, r'\1' + base + '/', new)
            new = re.sub(r'(location\.href\s*=\s*["\'])' + root_abs, r'\1' + base + '/', new)
        elif p.suffix == ".css":
            new = re.sub(r'(url\(["\']?)' + root_abs, r'\1' + base + '/', new)
        elif p.suffix == ".js":
            # module imports and string literals that start with a root path such as "/data/..."
            new = re.sub(r'((?:\bfrom\s+|\bimport\s*\(\s*)["\'`])' + root_abs, r'\1' + base + '/', new)
            new = re.sub(r'((?:fetch\(\s*|href\s*[:=]\s*|src\s*[:=]\s*|url\s*[:=]\s*|getJSON\(\s*|load\(\s*)["\'`])' + root_abs, r'\1' + base + '/', new)
        elif p.name == "manifest.webmanifest":
            new = re.sub(r'("(?:start_url|scope|src)"\s*:\s*")' + root_abs, r'\1' + base + '/', new)
        elif p.name == "robots.txt":
            new = re.sub(r'(?m)^((?:Allow|Disallow):\s*)' + root_abs, r'\1' + base + '/', new)
        if new != txt:
            p.write_text(new, encoding="utf-8")

def patch_runtime(site: pathlib.Path, base: str) -> None:
    """Every page loads js/app.js as a module. Put one small module in front of it that
    (1) sends root-absolute fetch() calls to the sub-path and (2) lets the router see real paths
    like /pill-by-pill/medicine/aspirin/ as /medicine/aspirin/. No inline script, so a strict
    Content-Security-Policy never blocks it."""
    (site / "js" / "base_path.js").write_text(
        f'export const BASE = "{base}";\n'
        "const f = window.fetch.bind(window);\n"
        'window.fetch = (u, o) => f(typeof u === "string" && u.startsWith("/") && !u.startsWith("//") && !u.startsWith(BASE + "/") ? BASE + u : u, o);\n'
        "export const sitePath = () => location.pathname.startsWith(BASE + \"/\") ? location.pathname.slice(BASE.length) : location.pathname;\n",
        encoding="utf-8")
    app = site / "js" / "app.js"
    txt = app.read_text(encoding="utf-8")
    if "base_path.js" not in txt:
        txt = f'import {{ sitePath }} from "{base}/js/base_path.js";\n' + txt
        txt = re.sub(r"location\.pathname(?=\.match|\))", "sitePath()", txt)
        txt = txt.replace("/.test(location.pathname)", "/.test(sitePath())")
        app.write_text(txt, encoding="utf-8")


FIXES = pathlib.Path(__file__).resolve().parent.parent / "site-fixes"

def apply_site_fixes(site: pathlib.Path) -> None:
    """Copy .github/site-fixes/ into the site and wire the v6.x routes into app.js."""
    for f in FIXES.rglob("*"):
        if f.is_file():
            dst = site / f.relative_to(FIXES)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f, dst)
    # Grouped, role-aware Reference navigation (js/ref_nav.js) in place of the flat 55-link sidebar
    css = site / "css" / "reference.css"
    extra = (FIXES / "css" / "ref_nav.css").read_text(encoding="utf-8")
    if "js/ref_nav.js" not in css.read_text(encoding="utf-8"):
        css.write_text(css.read_text(encoding="utf-8") + "\n" + extra, encoding="utf-8")
    lay = site / "js" / "layout.js"
    ltxt = lay.read_text(encoding="utf-8")
    if "ref_nav.js" not in ltxt:
        ltxt, n = re.subn(r'\$\{REF_NAV\.map\(\(\[href, label\]\) =>\s*html`<a href="\$\{href\}"\$\{current === href \? html` aria-current="page"` : ""\}>\$\{label\}</a>`\)\}<a href="#/fund">Funding</a>',
                          "${refNav(REF_NAV, current, role)}", ltxt)
        if n != 1:
            sys.exit("layout.js: could not find the Reference side navigation in refShell()")
        lay.write_text('import { refNav } from "./ref_nav.js";\n' + ltxt, encoding="utf-8")
    app = site / "js" / "app.js"
    txt = app.read_text(encoding="utf-8")
    # 1. Lines a patch appended after the final route(); call. A top-level `return` is a syntax error
    #    ("Illegal return statement") that stops the whole site from starting.
    m = re.search(r'addEventListener\("hashchange",\s*route\);\s*\n\s*route\(\);', txt)
    if not m:
        sys.exit("app.js: could not find the closing route(); call")
    tail = txt[m.end():]
    if tail.strip():
        print("app.js: removed", len([l for l in tail.splitlines() if l.strip()]), "stray lines after route();")
    txt = txt[:m.end()] + "\n"
    # 2. Send unknown #/ref/<slug> and #/explore/<slug> pages to the v6 route table
    if "v6_routes.js" not in txt:
        txt = 'import { v6Route } from "./v6_routes.js";\n' + txt
        anchor = '  throw new Error("Page not found");'
        if anchor not in txt:
            sys.exit("app.js: could not find the Page not found line in resolve()")
        txt = txt.replace(anchor, '  if ((area === "ref" || area === "explore") && a) { const v6 = await v6Route(area, a, query); if (v6) return v6; }\n' + anchor, 1)
    app.write_text(txt, encoding="utf-8")


def merge_sitemap(site: pathlib.Path, base_zip, url: str) -> int:
    """One sitemap with absolute addresses: every page in the new build's sitemap plus the medicine
    pages from the underlay site (search engines ignore relative <loc> values such as "/adme/")."""
    locs = {}
    def take(xml):
        for loc, mod in re.findall(r"<loc>([^<]+)</loc>(?:\s*<lastmod>([^<]+)</lastmod>)?", xml):
            for old in OLD_URLS:
                loc = loc.replace(old, url)
            if loc.startswith("/"):
                loc = url + loc
            locs[loc] = mod or locs.get(loc, "")
    if base_zip:
        with zipfile.ZipFile(base_zip) as z:
            n = next((n for n in z.namelist() if n.split("site/", 1)[-1] == "sitemap.xml"), None)
            if n:
                take(z.read(n).decode("utf-8"))
    sm = site / "sitemap.xml"
    if sm.is_file():
        take(sm.read_text(encoding="utf-8"))
    rows = "".join(f"  <url><loc>{l}</loc>" + (f"<lastmod>{m}</lastmod>" if m else "") + "</url>\n" for l, m in sorted(locs.items()))
    sm.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "</urlset>\n", encoding="utf-8")
    return len(locs)

def verification_tags(site: pathlib.Path) -> None:
    """Put the Search Console / Bing tags from config/site.json on the home page if a build dropped them."""
    import json
    cfg = site / "config" / "site.json"
    if not cfg.is_file():
        return
    c = json.loads(cfg.read_text(encoding="utf-8"))
    idx = site / "index.html"
    txt = idx.read_text(encoding="utf-8")
    for key, name in (("google_site_verification", "google-site-verification"), ("bing_site_verification", "msvalidate.01")):
        if c.get(key) and name not in txt:
            txt = txt.replace("</head>", f'<meta name="{name}" content="{c[key]}">\n</head>', 1)
    idx.write_text(txt, encoding="utf-8")

def main():
    a = argparse.ArgumentParser()
    a.add_argument("site"); a.add_argument("--base", required=True); a.add_argument("--url", required=True)
    a.add_argument("--underlay")
    o = a.parse_args()
    site, base, url = pathlib.Path(o.site), "/" + o.base.strip("/"), o.url.rstrip("/")
    if o.underlay:
        print("underlay added", underlay(site, pathlib.Path(o.underlay)), "files")
    apply_site_fixes(site)
    for f in fix_missing_imports(site):
        print("import fixed:", f)
    prefix_paths(site, base, url)
    print("sitemap pages:", merge_sitemap(site, o.underlay, url))
    verification_tags(site)
    patch_runtime(site, base)
    (site / ".nojekyll").touch()
    (site / "_headers").unlink(missing_ok=True)   # Netlify-only file; GitHub Pages ignores it
    print("ready:", url + "/")

main()
