"""Open every page of a prepared site the way GitHub Pages serves it (under /<repo>/) in a real
browser, follow the links on the main pages, and fail if any page shows "We couldn't find that
page", throws a script error, or asks for a file that does not exist.
Usage: python3 check_pages.py SITE_DIR --base /pill-by-pill"""
import asyncio, mimetypes, os, sys, re
from playwright.async_api import async_playwright
HOST, SITE = "https://pages.example", sys.argv[1]
BASE = "/" + (sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "pill-by-pill").strip("/") + "/"
SLUGS = re.findall(r'^  "([a-z0-9-]+)": M\(', open(os.path.join(SITE, "js/v6_routes.js")).read(), re.M)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await (await b.new_context()).new_page()
        bad404, errs, cons = [], [], []
        async def route(r):
            url = r.request.url
            if not url.startswith(HOST): return await r.abort()
            path = url[len(HOST):].split("?")[0].split("#")[0]
            f = os.path.join(SITE, path[len(BASE):]) if path.startswith(BASE) else None
            if f and os.path.isdir(f): f = os.path.join(f, "index.html")
            if f and os.path.isfile(f):
                return await r.fulfill(path=f, content_type="text/javascript" if f.endswith(".js") else (mimetypes.guess_type(f)[0] or "application/octet-stream"))
            bad404.append(path); return await r.fulfill(status=404, content_type="text/html", body="<h1>404</h1>")
        await pg.route("**/*", route)
        pg.on("pageerror", lambda e: errs.append(f"{pg.url}: {e}"))
        pg.on("console", lambda m: cons.append(f"{pg.url}: {m.text}") if m.type == "error" else None)
        todo = ["", "#/explore", "#/ref", "#/fund", "#/privacy", "#/share", "medicines/", "medicine/aspirin/", "#/explore/medicine/aspirin", "#/ref/drug/aspirin",
                "#/ref/drug/sotorasib/binding", "#/ref/families", "#/ref/compare", "#/explore/quiz", "#/ref/departments", "#/ref/routes", "#/ref/vendors", "#/ref/equipment", "#/explore/how-drugs-are-built"]
        todo += [f"#/{e}/{s}" for s in SLUGS for e in ("ref", "explore")]
        seen, failed = set(), []
        i = 0
        while i < len(todo):
            r = todo[i]; i += 1
            if r in seen: continue
            seen.add(r)
            await pg.goto(HOST + BASE + r)
            try: await pg.wait_for_function("document.getElementById('app')?.dataset.ready !== undefined", timeout=8000)
            except Exception: pass
            await pg.wait_for_timeout(250)
            h1 = (await pg.evaluate("document.querySelector('#app h1')?.textContent.trim() || ''"))[:70]
            if not h1 or "couldn't find" in h1 or "Connection" in h1:
                msg = await pg.evaluate("document.querySelector('#app .muted')?.textContent || ''")
                failed.append((r, h1, msg[:120]))
            if i <= 19:   # follow links found on the main pages
                for h in await pg.evaluate("[...document.querySelectorAll('#app a[href]')].map(a => a.getAttribute('href'))"):
                    h = h.replace(BASE, "", 1) if h.startswith(BASE) else h
                    if h.startswith("#/") and "?" not in h and h not in seen: todo.append(h)
        print("pages checked:", len(seen)); print("FAILED:", len(failed))
        for f in failed: print("  ", f)
        print("404s:", sorted(set(bad404))[:20]); print("page errors:", errs[:10]); print("console errors:", cons[:10])
        await b.close()
        return 1 if (failed or bad404 or errs or cons) else 0
sys.exit(asyncio.run(main()))
