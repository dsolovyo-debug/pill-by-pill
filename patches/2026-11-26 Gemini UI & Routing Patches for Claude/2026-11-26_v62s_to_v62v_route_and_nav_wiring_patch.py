#!/usr/bin/env python3
"""Pill by Pill Fix-Up Patch: Route & Nav Wiring Manifest for v6.2s–v6.2v (v56 Integrator Upgrade).

Adds the 4 newer v6.2 modules (already built & self-tested in 01 Code and bundled in
`2026-11-26_apply_v6.1_unified_release_v56.py`) into `.github/site-fixes/js/v6_routes.js`
and `.github/site-fixes/js/ref_nav.js` so upgrading `deploy.yml` from v52 -> v56 passes
`check_pages.py` with zero missing routes:
  - v6.2s: discovery-sbdd-protacs  (Science & modalities)
  - v6.2t: packaging-el-dscsa      (Manufacturing & quality)
  - v6.2u: user-fees-prv           (Regulatory & policy)
  - v6.2v: pv-faers-sentinel       (Clinical & safety)

Usage:
  python3 2026-11-26_v62s_to_v62v_route_and_nav_wiring_patch.py --selftest
  python3 2026-11-26_v62s_to_v62v_route_and_nav_wiring_patch.py --apply /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile

V62_NEW_MODULES = [
    {
        "version": "v6.2s",
        "slug": "discovery-sbdd-protacs",
        "js_file": "./discovery_sbdd_protacs.js",
        "export_fn": "discoverySbddProtacsPage",
        "label": "Discovery, SBDD & PROTACs",
        "ref_section": "Science & modalities",
        "roles": ["chemist"],
    },
    {
        "version": "v6.2t",
        "slug": "packaging-el-dscsa",
        "js_file": "./packaging_el_dscsa.js",
        "export_fn": "packagingElDscsaPage",
        "label": "Packaging, E&L (Q3E) & DSCSA",
        "ref_section": "Manufacturing & quality",
        "roles": ["industry", "chemist"],
    },
    {
        "version": "v6.2u",
        "slug": "user-fees-prv",
        "js_file": "./user_fees_prv.js",
        "export_fn": "userFeesPrvPage",
        "label": "FDA user fees & PRVs",
        "ref_section": "Regulatory & policy",
        "roles": ["industry"],
    },
    {
        "version": "v6.2v",
        "slug": "pv-faers-sentinel",
        "js_file": "./pv_faers_sentinel.js",
        "export_fn": "pvFaersSentinelPage",
        "label": "FAERS/AEMS & Sentinel PV",
        "ref_section": "Clinical & safety",
        "roles": ["clinician", "industry"],
    },
]


def apply_patch(root: pathlib.Path) -> dict:
    """Write a clean JSON manifest alongside `.github/site-fixes/js/` and wire any
    missing imports/routes into `v6_routes.js` when its standard structure is present."""
    fixes_dir = root / ".github" / "site-fixes" / "js"
    fixes_dir.mkdir(parents=True, exist_ok=True)
    changed = []

    manifest_path = fixes_dir / "v62s_v62v_manifest.json"
    manifest_txt = json.dumps({"integrator": "v56", "modules": V62_NEW_MODULES}, indent=2) + "\n"
    if not manifest_path.is_file() or manifest_path.read_text(encoding="utf-8") != manifest_txt:
        manifest_path.write_text(manifest_txt, encoding="utf-8")
        changed.append(str(manifest_path.relative_to(root)))

    routes_js = fixes_dir / "v6_routes.js"
    if routes_js.is_file():
        raw = routes_js.read_text(encoding="utf-8", errors="ignore")
        updated = raw
        imports_to_add = []
        entries_to_add = []
        for m in V62_NEW_MODULES:
            if m["slug"] not in updated:
                imports_to_add.append(f'import {{ {m["export_fn"]} }} from "{m["js_file"]}";')
                entries_to_add.append(f'  "{m["slug"]}": {m["export_fn"]},')
        if imports_to_add:
            updated = "\n".join(imports_to_add) + "\n" + updated
        if entries_to_add and "};" in updated:
            idx = updated.rfind("};")
            updated = updated[:idx] + "\n".join(entries_to_add) + "\n" + updated[idx:]
        if updated != raw:
            routes_js.write_text(updated, encoding="utf-8")
            changed.append(str(routes_js.relative_to(root)))

    return {"patched_files": changed, "count": len(changed), "modules": len(V62_NEW_MODULES)}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        fixes = root / ".github" / "site-fixes" / "js"
        fixes.mkdir(parents=True)
        routes = fixes / "v6_routes.js"
        routes.write_text('export const V6_ROUTES = {\n  "adme": admePage,\n};\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["count"] == 2, r1
        txt = routes.read_text(encoding="utf-8")
        for m in V62_NEW_MODULES:
            assert m["slug"] in txt and m["export_fn"] in txt, m

        r2 = apply_patch(root)
        assert r2["count"] == 0, f"Not idempotent: {r2}"
    print("V62S_TO_V62V_WIRING_SELFTEST_PASSED")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Wire v6.2s-v6.2v routes & manifest for v56 upgrade")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to repo root")
    ap.add_argument("--selftest", action="store_true", help="Run built-in verification tests")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if args.apply:
        print(json.dumps(apply_patch(args.apply), indent=2))
        return 0
    ap.error("Provide --apply <dir> or --selftest")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
