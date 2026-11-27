"""Reduced end-to-end test of the v6.2s-x route fix.
tree = v6.0b source + the six v6.2s-x patches (+ their builders) + the v58 sanitizer, then
prepare_pages.py (2026-11-25 version vs fixed version) and a browser check of the 12 new routes
served the way GitHub Pages serves a project site (/pill-by-pill/)."""
import importlib.util, pathlib, shutil, subprocess, sys, asyncio, os, mimetypes, json
PB = pathlib.Path("/home/claude/pbp"); P = PB / "patches"; W = PB / "sim/e2e"
def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_").replace("-", "_"), P / name)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ORDER = ["2026-11-25_v6.2s_drug_discovery_hts_sbdd_protacs_alphafold_patch.py",
 "2026-11-25_v6.2t_packaging_ccs_ich_q3e_el_dscsa_edds_patch.py",
 "2026-11-26_v6.2u_user_fees_pdufa_gdufa_bsufa_omufa_prv_expedited_patch.py",
 "2026-11-26_v6.2v_pharmacovigilance_faers_sentinel_ich_e2_patch.py",
 "2026-11-26_v6.2w_pharma_microbiology_sterility_endotoxin_ccit_patch.py",
 "2026-11-26_v6.2x_dmepa_medication_errors_poca_container_labels_patch.py"]
SLUGS = ["discovery-sbdd-protacs", "packaging-el-dscsa", "user-fees-prv", "pv-faers-sentinel", "microbiology-sterility", "dmepa-med-errors"]
def build(tag, gh):
    t = W / tag; shutil.rmtree(t, ignore_errors=True); shutil.copytree(PB / "src60b", t / "src")
    for f in ORDER:
        load(f).apply_patch(t / "src")
    for b in sorted((t / "src/pipeline").glob("build_*.py")):
        if any(s.replace("-", "_") in b.name or b.name.startswith(("build_discovery", "build_packaging", "build_user_fees", "build_pv_", "build_microbiology", "build_dmepa")) for s in SLUGS):
            subprocess.run([sys.executable, "-I", str(b), str(t / "src/site/data")], check=True, capture_output=True, cwd=t / "src")
    load("2026-11-26_apply_v6.1_unified_release_v58.py")._sanitize_js_and_routes(t / "src")
    shutil.copytree(gh, t / "repo/.github")
    r = subprocess.run([sys.executable, "-I", str(t / "repo/.github/scripts/prepare_pages.py"), str(t / "src/site"),
                        "--base", "/pill-by-pill", "--url", "https://dsolovyo-debug.github.io/pill-by-pill"], capture_output=True, text=True)
    return t / "src/site", r
async def check(site):
    from playwright.async_api import async_playwright
    HOST, BASE = "https://pages.example", "/pill-by-pill/"
    out = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); ctx = await b.new_context(viewport={"width": 390, "height": 844}); pg = await ctx.new_page()
        errs, b404 = [], []
        async def route(r):
            url = r.request.url
            if not url.startswith(HOST): return await r.abort()
            path = url[len(HOST):].split("?")[0].split("#")[0]
            f = os.path.join(site, path[len(BASE):]) if path.startswith(BASE) else None
            if f and os.path.isdir(f): f = os.path.join(f, "index.html")
            if f and os.path.isfile(f):
                return await r.fulfill(path=f, content_type="text/javascript" if f.endswith(".js") else (mimetypes.guess_type(f)[0] or "application/octet-stream"))
            b404.append(path); return await r.fulfill(status=404, content_type="text/html", body="<h1>404</h1>")
        await pg.route("**/*", route)
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        for s in SLUGS:
            for env in ("ref", "explore"):
                errs.clear()
                await pg.goto(HOST + BASE + f"#/{env}/{s}")
                try: await pg.wait_for_function("document.getElementById('app')?.dataset.ready !== undefined", timeout=8000)
                except Exception: pass
                await pg.wait_for_timeout(600)
                info = await pg.evaluate("""() => ({h1: (document.querySelector('#app h1')?.textContent || '').trim().slice(0,70),
                    entries: document.querySelectorAll('#v6-mount [data-sec], #v6-mount article, #v6-mount .entry, #v6-mount li').length,
                    text: (document.querySelector('#v6-mount')?.textContent || '').length})""")
                out.append({"route": f"#/{env}/{s}", **info, "page_errors": list(errs)})
        await b.close()
    return out, sorted(set(b404))
if __name__ == "__main__":
    shutil.rmtree(W, ignore_errors=True); W.mkdir(parents=True)
    res = {}
    for tag, gh in (("old_prepare_pages", PB / "repo11-25/.github"), ("fixed", PB / "fix/.github")):
        site, r = build(tag, gh)
        print(f"== {tag}: prepare_pages exit {r.returncode}"); print("   ", (r.stdout + r.stderr).strip().replace("\n", "\n    ")[:600])
        if r.returncode == 0:
            rows, b404 = asyncio.run(check(str(site)))
            for row in rows: print("   ", json.dumps(row))
            print("    404s:", b404)
            res[tag] = {"rows": rows, "404s": b404}
        else:
            res[tag] = {"prepare_pages_exit": r.returncode, "out": (r.stdout + r.stderr)[-400:]}
    json.dump(res, open(W / "e2e_result.json", "w"), indent=1)
