#!/usr/bin/env python3
"""Pill by Pill v6.0e Patch: Corporate Parent CDMO Rollups, OEM Market Dominance & Lab Kits, & Visual Lifecycle Map.

Layers cleanly on top of v6.0a–v6.0d:
  1. Corporate Parent Rollups (`pipeline/build_vendors.py` + `site/js/vendors.js`):
     Adds `parent_rollups` to `site/data/vendors_index.json` (grouping multi-site CDMOs by parent
     company with combined NAI/VAI/OAI/483/Warning Letter counts) and a `?view=parents` switcher
     on `#/ref/vendors` (completing Section 3.1 of the v6.0 Spec).
  2. OEM Dominance Matrix & Lab-Suite Hardware Kits (`site/js/equipment.js`):
     Adds `?view=oems` (grouping all 12 hardware categories by leading OEM) and `?view=kits`
     (4 curated pharmaceutical lab/suite stacks with zero fabricated price totals).
  3. Interactive Visual Lifecycle SVG (`site/js/departments.js`) & Explore-Mode Delivery Links (`site/js/route_links.js`):
     Adds clickable inline SVG lifecycle map (`Discovery -> Formulation -> Analytical QC -> Manufacturing`)
     to `#/explore/how-drugs-are-built` and `#/ref/departments`, plus plain-language Explore delivery helper.

Usage:
  python3 2026-11-21_v6.0e_parent_rollups_oem_matrix_and_lifecycle_svg_patch.py --selftest
  python3 2026-11-21_v6.0e_parent_rollups_oem_matrix_and_lifecycle_svg_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

PARENT_ROLLUPS_PY_SNIPPET = '\n    # v6.0e: Corporate parent-company rollups (Section 3.1 of v6.0 Spec)\n    parents = {}\n    for r in index_rows:\n        p = (r.get("parent_company") or r.get("firm_name") or "Unknown").strip()\n        pk = p.upper()\n        if pk not in parents:\n            parents[pk] = {\n                "parent_company": p,\n                "site_count": 0,\n                "feis": [],\n                "regions": set(),\n                "modalities": set(),\n                "stages": set(),\n                "total_inspections": 0,\n                "nai": 0,\n                "vai": 0,\n                "oai": 0,\n                "form_483_count": 0,\n                "warning_letter_count": 0,\n            }\n        pr = parents[pk]\n        pr["site_count"] += 1\n        pr["feis"].append(r["fei"])\n        if r.get("region"):\n            pr["regions"].add(r["region"])\n        pr["modalities"].update(r.get("modalities") or [])\n        pr["stages"].update(r.get("stages") or [])\n        pr["total_inspections"] += r.get("total_inspections") or 0\n        pr["nai"] += r.get("nai") or 0\n        pr["vai"] += r.get("vai") or 0\n        pr["oai"] += r.get("oai") or 0\n        pr["form_483_count"] += r.get("form_483_count") or 0\n        pr["warning_letter_count"] += r.get("warning_letter_count") or 0\n\n    parent_rollups = [\n        {\n            **{k: v for k, v in pr.items() if not isinstance(v, set)},\n            "regions": sorted(pr["regions"]),\n            "modalities": sorted(pr["modalities"]),\n            "stages": sorted(pr["stages"]),\n        }\n        for pr in sorted(parents.values(), key=lambda x: (-x["site_count"], x["parent_company"]))\n    ]\n'
VENDORS_PARENT_VIEW_JS = '\nexport function renderParentRollupsHtml(rollups = []) {\n  if (!rollups.length) return html`<p class="muted">No corporate parent records loaded yet.</p>`;\n  return html`<div class="tbl-wrap" tabindex="0" role="region" aria-label="Corporate parent rollups">\n    <table class="tbl"><thead><tr>\n      <th>Corporate Parent</th><th>Sites</th><th>Regions</th><th>Modalities</th><th>NAI / VAI / OAI</th><th>483s</th><th>Warning Letters</th><th>Actions</th>\n    </tr></thead>\n    <tbody>${rollups.map((p) => html`<tr>\n      <td><b>${p.parent_company}</b></td>\n      <td>${p.site_count}</td>\n      <td>${(p.regions || []).join(", ") || "—"}</td>\n      <td>${(p.modalities || []).join(", ") || "—"}</td>\n      <td>${p.nai} / ${p.vai} / ${p.oai}</td>\n      <td>${p.form_483_count}</td>\n      <td>${p.warning_letter_count}</td>\n      <td><a href="#/ref/vendors?q=${encodeURIComponent(p.parent_company)}">View sites</a>${(p.feis || []).length >= 2 ? html` · <a href="#/ref/vendors/compare/${p.feis.slice(0, 3).join("/")}">Compare top ${Math.min(3, p.feis.length)}</a>` : ""}</td>\n    </tr>`)}</tbody></table>\n  </div>`;\n}\n'
EQUIPMENT_VIEWS_JS = '\nexport const LAB_SUITE_KITS = [\n  {\n    id: "kit-discovery",\n    name: "Early-Stage Discovery & Bioanalytical Screening Lab",\n    stage: "Preclinical / Target-to-Lead",\n    summary: "Core automated screening and mass-spec assay stack for hit identification and preclinical PK.",\n    equipment_ids: ["eq-hts-liquid-handler", "eq-lc-ms-ms", "eq-hplc-uplc"],\n  },\n  {\n    id: "kit-osd-formulation",\n    name: "Oral Solid Dosage (OSD) Formulation & Scale-Up Suite",\n    stage: "Phase I–Commercial OSD",\n    summary: "Granulation, rotary tablet compression, and USP dissolution release testing for tablets and capsules.",\n    equipment_ids: ["eq-fluid-bed-granulator", "eq-rotary-tablet-press", "eq-dissolution-bath", "eq-karl-fischer"],\n  },\n  {\n    id: "kit-analytical-qc",\n    name: "cGMP Analytical Development & QC Release Laboratory",\n    stage: "Phase I–Commercial Release",\n    summary: "Full ICH Q1A/Q2/Q3D analytical release suite covering potency, trace impurities, moisture, heavy metals, and shelf-life stability.",\n    equipment_ids: ["eq-hplc-uplc", "eq-lc-ms-ms", "eq-icp-ms", "eq-karl-fischer", "eq-stability-chamber", "eq-dissolution-bath"],\n  },\n  {\n    id: "kit-sterile-biologics",\n    name: "Sterile Biologics & Aseptic Fill-Finish Suite",\n    stage: "Phase I–Commercial Biologics",\n    summary: "Single-use cell culture upstream paired with isolator-enclosed aseptic fill-finish and SIP lyophilization.",\n    equipment_ids: ["eq-single-use-bioreactor", "eq-sterile-fill-finish", "eq-lyophilizer", "eq-hplc-uplc"],\n  },\n];\n\nexport function groupEquipmentByOem(items = []) {\n  const byOem = new Map();\n  for (const e of items) {\n    for (const o of (e.leading_oems || [])) {\n      const key = o.name.trim();\n      if (!byOem.has(key)) byOem.set(key, { name: key, items: [], departments: new Set() });\n      const rec = byOem.get(key);\n      rec.items.push({ id: e.id, name: e.name, department: e.department, evidence: o.market_evidence });\n      rec.departments.add(e.department);\n    }\n  }\n  return [...byOem.values()]\n    .map((r) => ({ ...r, departments: [...r.departments].sort() }))\n    .sort((a, b) => b.items.length - a.items.length || a.name.localeCompare(b.name));\n}\n\nexport function renderOemDominanceHtml(items = []) {\n  const oems = groupEquipmentByOem(items);\n  return html`<div class="tbl-wrap" tabindex="0" role="region" aria-label="OEM market dominance matrix">\n    <table class="tbl"><thead><tr><th>Leading OEM</th><th>Categories</th><th>Departments</th><th>Instruments &amp; Market Evidence</th></tr></thead>\n    <tbody>${oems.map((o) => html`<tr>\n      <td><b>${o.name}</b></td>\n      <td>${o.items.length}</td>\n      <td>${o.departments.join(", ")}</td>\n      <td><ul class="plain">${o.items.map((it) => html`<li><a href="#/ref/equipment?q=${encodeURIComponent(o.name)}#${it.id}"><b>${it.name}</b></a>: ${it.evidence}</li>`)}</ul></td>\n    </tr>`)}</tbody></table>\n  </div>`;\n}\n\nexport function renderLabSuiteKitsHtml(items = []) {\n  const byId = new Map(items.map((e) => [e.id, e]));\n  return html`${LAB_SUITE_KITS.map((k) => {\n    const eqs = k.equipment_ids.map((id) => byId.get(id)).filter(Boolean);\n    const pricedNew = eqs.map((e) => e.pricing && e.pricing.new_public_award_range_usd).filter((b) => b && b.median != null);\n    const newSum = pricedNew.length === eqs.length && eqs.length\n      ? fmtUsd(pricedNew.reduce((acc, b) => acc + Number(b.median), 0))\n      : "Awaiting full live public award coverage";\n    return html`<section class="x-panel" id="${k.id}">\n      <h2>${k.name}</h2>\n      <p class="muted small">${k.stage} · ${eqs.length} core hardware classes · Sum of live public medians: ${newSum}</p>\n      <p>${k.summary}</p>\n      <ul class="plain">${eqs.map((e) => html`<li><a href="#/ref/equipment#${e.id}"><b>${e.name}</b></a> — ${e.technical_spec.gmp_compliance}</li>`)}</ul>\n    </section>`;\n  })}`;\n}\n'
LIFECYCLE_SVG_JS = '\nexport function renderLifecycleSvg(mode = "ref") {\n  const base = mode === "explore" ? "#/explore/departments/" : "#/ref/departments/";\n  const nodes = [\n    { id: "discovery", x: 10, label: "1. Discovery", sub: "Target & Preclinical" },\n    { id: "formulation", x: 175, label: "2. Formulation", sub: "Dosage & Routes" },\n    { id: "analytical", x: 340, label: "3. Analytical QC", sub: "Purity & Stability" },\n    { id: "manufacturing", x: 505, label: "4. Manufacturing", sub: "Scale-Up & cGMP" },\n  ];\n  return html`<figure class="lifecycle-map" aria-label="Pharmaceutical development lifecycle">\n    <svg viewBox="0 0 665 86" width="665" height="86" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <a href="${base}${n.id}">\n          <rect x="${n.x}" y="8" width="150" height="66" rx="10" fill="var(--paper,#f8fafc)" stroke="var(--line,#94a3b8)" stroke-width="1.5"/>\n          <text x="${n.x + 75}" y="35" text-anchor="middle" font-size="13" font-weight="700" fill="currentColor">${n.label}</text>\n          <text x="${n.x + 75}" y="54" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.75">${n.sub}</text>\n        </a>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 150}" y1="41" x2="${n.x + 165}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Click any department stage to inspect its workflows, regulatory standards, and equipment.</figcaption>\n  </figure>`;\n}\n'
EXPLORE_ROUTE_HELPER_JS = '\nexport function renderExploreDeliveryLinkHtml(d) {\n  const routes = inferRoutesForDrug(d);\n  if (!routes.length) return "";\n  return html`<p class="muted small">How this dosage form is engineered: ${routes.map((r) => r.label).join(", ")} — <a href="#/explore/departments/formulation">Inside Formulation Development</a> · <a href="#/explore/departments/analytical">How QC Tests Every Batch</a></p>`;\n}\n'


def _patch_build_vendors(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"parent_rollups": parent_rollups' in txt:
        return False
    anchor = '    index_payload = {\n        "checked": CHECKED,'
    if anchor not in txt:
        raise ValueError(f"Missing index_payload anchor in {path}")
    rep = (
        PARENT_ROLLUPS_PY_SNIPPET.lstrip("\n") + "\n"
        '    index_payload = {\n        "checked": CHECKED,\n        "parent_rollups": parent_rollups,'
    )
    path.write_text(txt.replace(anchor, rep, 1), encoding="utf-8")
    return True


def _patch_vendors_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "export function renderParentRollupsHtml" not in txt:
        txt = txt.rstrip() + "\n" + VENDORS_PARENT_VIEW_JS
        changed = True
    if 'const view = query.get("view") || "sites";' not in txt:
        old = '  const q = query.get("q") || "";'
        new = '  const q = query.get("q") || "";\n  const view = query.get("view") || "sites";'
        if old in txt:
            txt = txt.replace(old, new, 1)
            changed = True
    if 'id="v-view-switch"' not in txt:
        old_bar = '<p id="v-compare-bar" class="muted small">'
        switch_bar = (
            '<p id="v-view-switch" class="small">View by: '
            '<a href="#/ref/vendors"${view === "sites" ? \' aria-current="page"\' : ""}><b>Individual Sites (FEI)</b></a> · '
            '<a href="#/ref/vendors?view=parents"${view === "parents" ? \' aria-current="page"\' : ""}><b>Corporate Parents (${(idx.parent_rollups || []).length})</b></a></p>\n    '
            '${view === "parents" ? renderParentRollupsHtml(idx.parent_rollups || []) : ""}\n    '
        )
        if old_bar in txt:
            txt = txt.replace(old_bar, switch_bar + old_bar, 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_equipment_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "export function renderOemDominanceHtml" not in txt:
        anchor = "export async function equipmentPage"
        if anchor not in txt:
            raise ValueError(f"Missing equipmentPage anchor in {path}")
        txt = txt.replace(anchor, EQUIPMENT_VIEWS_JS.lstrip("\n") + "\n" + anchor, 1)
        changed = True
    if 'const view = query.get("view") || "catalog";' not in txt:
        old_q = '  const q = query.get("q") || "";'
        new_q = '  const q = query.get("q") || "";\n  const view = query.get("view") || "catalog";'
        if old_q in txt:
            txt = txt.replace(old_q, new_q, 1)
            changed = True
    if 'id="e-view-switch"' not in txt:
        old_f = '<section class="filters" aria-label="Filter pharmaceutical equipment">'
        bar = (
            '<p id="e-view-switch" class="small">View: '
            '<a href="#/ref/equipment"${view === "catalog" ? \' aria-current="page"\' : ""}><b>Equipment Catalog</b></a> · '
            '<a href="#/ref/equipment?view=oems"${view === "oems" ? \' aria-current="page"\' : ""}><b>Leading OEMs</b></a> · '
            '<a href="#/ref/equipment?view=kits"${view === "kits" ? \' aria-current="page"\' : ""}><b>Lab &amp; Suite Kits</b></a></p>\n    '
            '${view === "oems" ? renderOemDominanceHtml(items) : view === "kits" ? renderLabSuiteKitsHtml(items) : ""}\n    '
        )
        if old_f in txt:
            txt = txt.replace(old_f, bar + old_f, 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_departments_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "export function renderLifecycleSvg" not in txt:
        anchor = "export async function departmentsExplorePage"
        if anchor not in txt:
            raise ValueError(f"Missing departmentsExplorePage anchor in {path}")
        txt = txt.replace(anchor, LIFECYCLE_SVG_JS.lstrip("\n") + "\n" + anchor, 1)
        changed = True
    if 'renderLifecycleSvg("explore")' not in txt:
        old = 'body: html`${cards}`,'
        if old in txt:
            txt = txt.replace(old, 'body: html`${renderLifecycleSvg("explore")}${cards}`,', 1)
            changed = True
    if 'renderLifecycleSvg("ref")' not in txt:
        old = '<div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharmaceutical departments">'
        if old in txt:
            txt = txt.replace(old, '${renderLifecycleSvg("ref")}\n      ' + old, 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_route_links_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "export function renderExploreDeliveryLinkHtml" in txt:
        return False
    path.write_text(txt.rstrip() + "\n" + EXPLORE_ROUTE_HELPER_JS, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    return {
        "build_vendors_parent_rollups": _patch_build_vendors(root / "pipeline" / "build_vendors.py"),
        "vendors_js_parent_view": _patch_vendors_js(root / "site" / "js" / "vendors.js"),
        "equipment_js_oems_and_kits": _patch_equipment_js(root / "site" / "js" / "equipment.js"),
        "departments_js_lifecycle_svg": _patch_departments_js(root / "site" / "js" / "departments.js"),
        "route_links_explore_helper": _patch_route_links_js(root / "site" / "js" / "route_links.js"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "raw").mkdir()
        (root / "site" / "data").mkdir(parents=True)

        (root / "pipeline" / "build_vendors.py").write_text(
            'import json, pathlib, sys\nCHECKED = "2026-11-21"\n'
            'def build_vendors(raw_dir, data_dir):\n'
            '    index_rows = [\n'
            '        {"fei": "1001", "firm_name": "Lonza Visp", "parent_company": "Lonza Group", "region": "Europe", "modalities": ["biologics"], "stages": ["commercial"], "total_inspections": 2, "nai": 2, "vai": 0, "oai": 0, "form_483_count": 0, "warning_letter_count": 0},\n'
            '        {"fei": "1002", "firm_name": "Lonza Portsmouth", "parent_company": "Lonza Group", "region": "US", "modalities": ["biologics"], "stages": ["commercial"], "total_inspections": 1, "nai": 1, "vai": 0, "oai": 0, "form_483_count": 0, "warning_letter_count": 0},\n'
            '    ]\n'
            '    index_payload = {\n'
            '        "checked": CHECKED,\n'
            '        "count": len(index_rows),\n'
            '        "rows": index_rows,\n'
            '    }\n'
            '    (data_dir / "vendors_index.json").write_text(json.dumps(index_payload, indent=2), encoding="utf-8")\n'
            'if __name__ == "__main__": build_vendors(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "vendors.js").write_text(
            'export async function vendorsPage(query) {\n  const q = query.get("q") || "";\n  const b = `<p id="v-compare-bar" class="muted small"></p>`;\n}\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "equipment.js").write_text(
            'export async function equipmentPage(query) {\n  const q = query.get("q") || "";\n  const b = `<section class="filters" aria-label="Filter pharmaceutical equipment"></section>`;\n}\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "departments.js").write_text(
            'export async function departmentsExplorePage() { return { body: html`${cards}`, }; }\n'
            'export async function departmentsRefPage() { return `<div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharmaceutical departments">`; }\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "route_links.js").write_text(
            'export function inferRoutesForDrug(d) { return []; }\n',
            encoding="utf-8",
        )

        r1 = apply_patch(root)
        assert all(r1.values()), f"Expected all True on pass 1: {r1}"
        r2 = apply_patch(root)
        assert not any(r2.values()), f"Expected all False on pass 2: {r2}"

        subprocess.run([sys.executable, str(root / "pipeline" / "build_vendors.py"), str(root / "raw"), str(root / "site" / "data")], check=True)
        idx = json.loads((root / "site" / "data" / "vendors_index.json").read_text(encoding="utf-8"))
        assert len(idx["parent_rollups"]) == 1
        pr = idx["parent_rollups"][0]
        assert pr["parent_company"] == "Lonza Group" and pr["site_count"] == 2 and pr["nai"] == 3 and pr["regions"] == ["Europe", "US"], pr

        print("V60E_PARENT_ROLLUPS_OEM_MATRIX_LIFECYCLE_SELFTEST_PASSED", json.dumps(r1, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0e Parent Rollups, OEM Matrix & Lifecycle SVG patch.")
    ap.add_argument("--apply", type=pathlib.Path, help="Path to unpacked source directory")
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
