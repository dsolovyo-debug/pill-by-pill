#!/usr/bin/env python3
"""Build the Pill by Pill source tree for the GitHub Pages deploy (Claude, 2026-11-28).

Gemini's integrators split into two lines on 2026-11-24/25:
  * v52 ("v6.2"): v6.0a-v6.2o + careers, quiz 80/glossary 60, history & safety laws,
    BD/licensing, quiz 100/glossary 80, worksheets 6/storyboards 7   <- what the live site ran
  * v54-v59 ("v6.1"): v6.0a-v6.2o + MIDD, labeling/SPL, inspections/483, discovery/SBDD,
    packaging/DSCSA, user fees/PRV, PV/FAERS, microbiology/sterility, DMEPA
Switching deploy.yml to v59 alone would drop the careers, history-laws and bd-deals pages
(and the quiz/glossary/worksheet expansions) from the live site. This script applies the union:
v59's patch list with v52's six extra patches in their v52 position (after v6.2o), and runs
the builders of both. It reuses v59's helpers (unpack, sanitizer, pack).

Usage (from the repo root): python3 .github/scripts/integrate_release.py /tmp/pill-by-pill-v6.2.zip
"""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

PATCHES = pathlib.Path("patches")
V59 = PATCHES / "2026-11-27_apply_v6.1_unified_release_v59.py"
V52 = PATCHES / "2026-11-24_apply_v6.2_unified_release_v52.py"
SOURCE_ZIP = PATCHES / "2026-11-21_pill-by-pill-source_v6.0b.zip"

V52_ONLY = [
    ("v52_careers_roles", "2026-11-24_v6.1u_pharma_careers_roles_pathways_patch.py"),
    ("v52_quiz80_glossary60", "2026-11-24_v6.1v_quiz80_and_glossary60_expansion_patch.py"),
    ("v52_history_safety_laws", "2026-11-24_v6.1w_pharma_history_safety_laws_patch.py"),
    ("v52_bd_licensing_ma", "2026-11-24_v6.1z_pharma_bd_licensing_ma_valuation_patch.py"),
    ("v52_quiz100_glossary80", "2026-11-24_v6.2t_quiz100_and_glossary80_expansion_patch.py"),
    ("v52_worksheets6_storyboards7", "2026-11-24_v6.2u_worksheets6_and_storyboards7_expansion_patch.py"),
]
V52_ONLY_BUILDERS = ["build_careers.py", "build_history_laws.py", "build_bd_deals.py"]

# Gemini's 2026-11-26/27 UI batch: only the manifest fix and the CSS-only patches (checked by Claude
# 2026-11-27). The rest of the batch stages helper modules no page imports yet, or should not be
# applied (see 04 Docs: 2026-11-27 Pre-deploy check of Gemini's Batches 1-6, Claude).
UI_DIR = "2026-11-26 Gemini UI & Routing Patches for Claude"
UI_PATCHES = [
    ("ui_manifest_fix", f"{UI_DIR}/2026-11-26_fix_manifest_webmanifest_and_pwa_paths_patch.py"),
    ("ui_mobile_tables_svgs_header", f"{UI_DIR}/2026-11-26_mobile_tables_svgs_and_header_polish_patch.py"),
    ("ui_card_grid_typography_v2", f"{UI_DIR}/2026-11-27_card_grid_and_typography_polish_v2_patch.py"),
    ("ui_compare_datasets_mobile", f"{UI_DIR}/2026-11-26_compare_and_datasets_mobile_cards_patch.py"),
]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def patch_order(v59):
    order = list(v59.PATCH_ORDER)
    i = [label for label, _ in order].index("v6.2o_babe_bcs_nti") + 1
    return order[:i] + V52_ONLY + order[i:]


def builders(v59_src: str):
    """v59's builder list (read from integrate_v61) plus v52's three, before global search / static pages."""
    import ast
    tree = ast.parse(v59_src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "integrate_v61")
    names = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Tuple) and node.elts and isinstance(node.elts[0], ast.Constant) \
                and isinstance(node.elts[0].value, str) and node.elts[0].value.startswith("build_"):
            names.append(node.elts[0].value)
    i = names.index("build_global_search.py")
    return names[:i] + V52_ONLY_BUILDERS + names[i:]


def builder_args(name, tree, data_dir, raw_src):
    if name in ("build_vendors.py", "build_equipment_catalog.py"):
        return [str(raw_src), str(data_dir)]
    if name == "build_origins_gallery.py":
        return [str(tree / "pipeline" / "origin_stories.json"), str(data_dir)]
    if name == "build_v60_static_pages.py":
        return [str(tree / "site")]
    return [str(data_dir)]


SHIM = '''

# --- added by .github/scripts/integrate_release.py (Claude, 2026-11-28) ---
# The v6.2v/w/x patches call _write_landing() and BASE_URL, which no patch defines; before
# 2026-11-28 those patches never ran (see integrate()), so nothing failed. Same page shape as
# the other landing pages (_render_page): title, description, a list of the entries, app link.
BASE_URL = "https://pillbypill.netlify.app"


def _write_landing(path, title, description, hash_route, entries):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    title = str(title).replace(" | Pill by Pill", "")
    lis = "".join(
        f"<li><b>{_esc(e.get('name') or e.get('title') or '')}</b> — {_esc(e.get('plain') or e.get('summary') or e.get('description') or '')}</li>"
        for e in (entries or []) if isinstance(e, dict))
    path.write_text(_render_page(base_url=BASE_URL, rel_path=path.parent.name, hash_route=hash_route,
                                 title=title, description=str(description or title), body_html=f"<ul>{lis}</ul>"),
                    encoding="utf-8")
'''


def shim_static_pages(tree: pathlib.Path) -> bool:
    sp = tree / "pipeline" / "build_v60_static_pages.py"
    if not sp.is_file():
        return False
    src = sp.read_text(encoding="utf-8")
    if "_write_landing(" not in src or "def _write_landing" in src:
        return False
    anchor = "\ndef build_v60_static_pages("
    if anchor not in src:
        sys.exit("build_v60_static_pages.py: could not find build_v60_static_pages()")
    sp.write_text(src.replace(anchor, SHIM + anchor, 1), encoding="utf-8")
    return True


NEW_REF_LINKS = [
    ("#/ref/pv-faers-sentinel", "Pharmacovigilance & Sentinel"),
    ("#/ref/microbiology-sterility", "Microbiology, Endotoxins & CCIT"),
    ("#/ref/dmepa-med-errors", "Medication Errors & POCA Names"),
]


def repair_layout(tree: pathlib.Path) -> int:
    """v6.2v/w/x append '{ label, href }' objects after the last EXPLORE_NAV entry, without a comma
    and in the wrong shape (the nav arrays hold [href, label] pairs): a SyntaxError that stops the
    whole site. Remove them and add their three pages to REF_NAV as [href, label]."""
    import re
    lay = tree / "site" / "js" / "layout.js"
    src = lay.read_text(encoding="utf-8")
    start = src.index("const EXPLORE_NAV = [")
    end = src.index("/** Simple environment", start)
    nav = src[start:end]
    obj = re.compile(r'[ \t]*\{ label: "[^"]*", href: "#/(?:ref|explore)/[a-z0-9-]+" \},?')
    n = len(obj.findall(nav))
    nav = obj.sub("", nav)
    nav = re.sub(r'\][ \t]*\n(?:[ \t]*\n)*\];', ']\n];', nav)   # tidy the blank lines left behind
    tail = '["#/ref/glossary", "Acronym glossary"]'
    if tail not in nav:
        sys.exit("layout.js: could not find the end of REF_NAV")
    add = "".join(f'["{h}", "{l}"], ' for h, l in NEW_REF_LINKS if f'"{h}"' not in nav.split("const REF_NAV")[1])
    nav = nav.replace(tail, add + tail, 1)
    lay.write_text(src[:start] + nav + src[end:], encoding="utf-8")
    return n


def integrate(tree: pathlib.Path, v59) -> dict:
    applied = {}
    for label, fname in patch_order(v59) + UI_PATCHES:
        p = PATCHES / fname
        if not p.is_file():
            raise FileNotFoundError(f"Missing required patch file: {p}")
        if label == "v6.0b" and (tree / "pipeline" / "build_departments.py").is_file():
            continue
        # v6.2v, v6.2w and v6.2x read their first argument as the tree, so "--apply <tree>" made them
        # write into a folder named "--apply" and their pages were never built (v56-v59 integrators).
        argv = ["--apply", str(tree)] if "--apply" in p.read_text(encoding="utf-8") else [str(tree)]
        subprocess.run([sys.executable, str(p), *argv], capture_output=True, text=True, check=True)
        applied[label] = "ok"
    raw_src = tree / "raw"
    raw_src.mkdir(parents=True, exist_ok=True)
    data_dir = tree / "site" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    stray = pathlib.Path("--apply")
    if stray.exists():
        sys.exit("a patch wrote into ./--apply instead of the source tree")
    shimmed = shim_static_pages(tree)
    layout_fixed = repair_layout(tree)
    v59._sanitize_js_and_routes(tree)
    ran = []
    for b in builders(V59.read_text(encoding="utf-8")):
        bpath = tree / "pipeline" / b
        if bpath.is_file():
            subprocess.run([sys.executable, str(bpath), *builder_args(b, tree, data_dir, raw_src)],
                           capture_output=True, text=True, check=True)
            ran.append(b)
    test_v60 = tree / "tests" / "test_v60.py"
    if test_v60.is_file():
        subprocess.run([sys.executable, str(test_v60)], capture_output=True, text=True, check=True)
    return {"patches": len(applied), "builders": len(ran), "static_pages_shim": shimmed, "layout_objects_removed": layout_fixed, "test_v60": "PASSED" if test_v60.is_file() else "absent"}


def main(out_zip: str) -> None:
    v59 = load(V59, "v59")
    with tempfile.TemporaryDirectory() as td:
        tree = v59._unpack_clean(SOURCE_ZIP, pathlib.Path(td) / "tree")
        eq = tree / "pipeline" / "build_equipment_catalog.py"
        if eq.is_file():
            eq.write_text(eq.read_text(encoding="utf-8").replace('item["search_query"]', 'item.get("search_query", item.get("name", ""))'), encoding="utf-8")
        try:
            print(json.dumps(integrate(tree, v59)))
        except subprocess.CalledProcessError as e:
            print("=== FAILED CMD ===", e.cmd)
            print("=== STDOUT ===\n", e.stdout)
            print("=== STDERR ===\n", e.stderr)
            sys.exit(1)
        v59._pack_clean(tree, pathlib.Path(out_zip))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/pill-by-pill-v6.2.zip")
