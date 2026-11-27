"""Apply each Batch 2-6 patch (and the template-join fix) to a fresh copy of a mock repo that holds
the v6.0b source tree under site/ plus the 2026-11-25 .github/ files, and record what each one changes."""
import importlib.util, pathlib, shutil, subprocess, json, filecmp, os
P = pathlib.Path("/home/claude/pbp/patches"); OUT = pathlib.Path("/home/claude/pbp/sim/applytest")
base = OUT / "base"
shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir(parents=True)
shutil.copytree("/home/claude/pbp/src60b", base)
shutil.copytree("/home/claude/pbp/repo11-25/.github", base / ".github")
names = ["fix_html_template_join_and_aria_escaping_patch", "fix_manifest_webmanifest_and_pwa_paths_patch",
 "fix_static_seo_cloaking_redirect_patch", "mobile_tables_svgs_and_header_polish_patch", "explore_nav_grouped_cleanup_patch",
 "explore_nav_grouping_and_mobile_polish_patch", "card_grid_and_typography_polish_patch", "trace_storyboard_pill_picker_and_accordion_patch",
 "sticky_mobile_back_to_top_and_section_toc_patch", "catalogue_mobile_filter_drawer_patch", "drug_dossier_quick_glance_and_sections_patch",
 "compare_and_datasets_mobile_cards_patch", "quiz_classroom_mobile_ux_patch", "equipment_vendors_mobile_filters_patch",
 "search_glossary_mobile_polish_patch", "binding_3d_viewer_mobile_controls_patch", "families_and_atc_tree_mobile_accordions_patch",
 "origins_gallery_mobile_cards_patch"]
def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
before = snapshot(base)
report = {}
for n in names:
    work = OUT / n; shutil.copytree(base, work)
    f = P / f"2026-11-26_{n}.py"
    r = subprocess.run(["python3", "-I", str(f), "--apply", str(work)], capture_output=True, text=True, cwd=str(OUT))
    after = snapshot(work)
    added = sorted(k for k in after if k not in before)
    changed = sorted(k for k in after if k in before and after[k] != before[k])
    # are the new JS modules imported by anything?
    imported = {}
    for a in added:
        if a.endswith(".js"):
            stem = pathlib.Path(a).name
            users = [k for k in after if k.endswith((".js", ".html", ".py")) and k != a and stem in after[k].decode("utf-8", "ignore")]
            imported[stem] = users
    css_linked = {}
    for a in added:
        if a.endswith(".css"):
            stem = pathlib.Path(a).name
            css_linked[stem] = [k for k in after if k.endswith((".html", ".js", ".css", ".py")) and k != a and stem in after[k].decode("utf-8", "ignore")]
    syntax = {}
    for a in added + changed:
        if a.endswith(".js"):
            tmp = OUT / "chk.mjs"; tmp.write_bytes(after[a])
            c = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
            syntax[a] = "ok" if c.returncode == 0 else c.stderr.strip().splitlines()[-4:]
    report[n] = {"exit": r.returncode, "stderr_tail": r.stderr.strip().splitlines()[-1:] , "added": added, "changed": changed,
                 "new_js_used_by": imported, "new_css_referenced_by": css_linked, "js_syntax": syntax}
    shutil.rmtree(work)
json.dump(report, open(OUT / "report.json", "w"), indent=1)
for n, v in report.items():
    print(f"\n## {n}: exit {v['exit']} {v['stderr_tail']}")
    print("  added:", v["added"]); print("  changed:", v["changed"])
    if v["new_js_used_by"]: print("  new JS used by:", v["new_js_used_by"])
    if v["new_css_referenced_by"]: print("  new CSS referenced by:", v["new_css_referenced_by"])
    bad = {k: s for k, s in v["js_syntax"].items() if s != "ok"}
    if bad: print("  JS SYNTAX:", bad)
