"""Simulate what moving deploy.yml to the v58 integrator does to app.js and v6_routes.js.
Uses the real v6.0b app.js, the real v6.2s-x patch functions, the real v58 sanitizer,
the real prepare_pages.py anchor regex (2026-11-25 version) and Gemini's v62s-v62v wiring patch."""
import importlib.util, pathlib, re, shutil, subprocess, sys, json
P = pathlib.Path("/home/claude/pbp/patches")
SIM = pathlib.Path("/home/claude/pbp/sim")
def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_").replace("-", "_"), P / name)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
shutil.rmtree(SIM, ignore_errors=True); (SIM / "site/js").mkdir(parents=True)
shutil.copy("/home/claude/pbp/src60b/site/js/app.js", SIM / "site/js/app.js")
order = ["2026-11-25_v6.2s_drug_discovery_hts_sbdd_protacs_alphafold_patch.py",
         "2026-11-25_v6.2t_packaging_ccs_ich_q3e_el_dscsa_edds_patch.py",
         "2026-11-26_v6.2u_user_fees_pdufa_gdufa_bsufa_omufa_prv_expedited_patch.py",
         "2026-11-26_v6.2v_pharmacovigilance_faers_sentinel_ich_e2_patch.py",
         "2026-11-26_v6.2w_pharma_microbiology_sterility_endotoxin_ccit_patch.py",
         "2026-11-26_v6.2x_dmepa_medication_errors_poca_container_labels_patch.py"]
app = SIM / "site/js/app.js"
for f in order:
    load(f)._patch_app_js(app)
txt = app.read_text()
fin = txt.index('addEventListener("hashchange", route);')
print("route lines before the final route(); call:", txt[:fin].count('if (path === "/'))
print("route lines after it:", txt[fin:].count('if (path === "/'))
integ = load("2026-11-26_apply_v6.1_unified_release_v58.py")
print("v58 sanitizer:", integ._sanitize_js_and_routes(SIM))
txt = app.read_text()
anchor_ok = bool(re.search(r'addEventListener\("hashchange",\s*route\);\s*\n\s*route\(\);', txt))
print("prepare_pages.py finds its closing route(); anchor:", anchor_ok)
tail = txt[txt.index('addEventListener("hashchange", route);'):]
print("--- end of app.js after the v58 sanitizer ---"); print(tail)
# syntax check of the top-level return (strip imports so node only parses)
chk = SIM / "check_app.mjs"; chk.write_text(re.sub(r'^import .*$', '', txt, flags=re.M))
r = subprocess.run(["node", "--check", str(chk)], capture_output=True, text=True)
print("node --check app.js:", "OK" if r.returncode == 0 else r.stderr.strip().splitlines()[-1])
# Gemini's v62s-v62v wiring patch on the real v6_routes.js
root = SIM / "repo"; (root / ".github/site-fixes/js").mkdir(parents=True)
shutil.copy("/home/claude/pbp/repo11-25/.github/site-fixes/js/v6_routes.js", root / ".github/site-fixes/js/v6_routes.js")
w = load("2026-11-26_v62s_to_v62v_route_and_nav_wiring_patch.py")
print("wiring patch:", w.apply_patch(root))
vr = (root / ".github/site-fixes/js/v6_routes.js").read_text()
r = subprocess.run(["node", "--check", str(root / ".github/site-fixes/js/v6_routes.js")], capture_output=True, text=True)
print("node --check v6_routes.js after the wiring patch:", "OK" if r.returncode == 0 else r.stderr.strip())
i = vr.find('"discovery-sbdd-protacs": discoverySbddProtacsPage')
print("--- where the entries landed ---"); print(vr[max(0, i-400):i+250])
