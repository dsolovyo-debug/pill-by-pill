#!/usr/bin/env python3
"""Pill by Pill v6.0d Patch: Drug-to-Route Cross-Linking, Used-Equipment Price-History Importer & SVG Chart, and v6.0 FastAPI Parity.

Layers cleanly on top of v6.0a + v6.0b + v6.0c:
  1. `site/js/route_links.js` + `site/js/reference.js` + `site/js/departments.js`:
     Links every medicine's US Drugs@FDA dosage forms/routes directly to `#/ref/routes#<route-id>`,
     `#/ref/departments/formulation`, and `#/ref/equipment?modality=...`.
  2. `pipeline/import_used_equipment.py` + `site/js/equipment.js`:
     Adds a stdlib CSV/JSON time-series importer for secondary-market equipment listings
     (`raw/used_equipment_snapshots.json`) and a zero-dependency inline SVG price-band trend
     visualizer (`renderPriceHistorySvg`) in `site/js/equipment.js`.
  3. `app.py`:
     Adds FastAPI v6.0 parity endpoints (`/api/departments`, `/api/routes`, `/api/equipment`,
     `/api/vendors`, `/api/vendors/{fei}`) reading directly from `site/data/` with zero data drift.

Usage:
  python3 2026-11-21_v6.0d_crosslinks_price_charts_and_api_patch.py --selftest
  python3 2026-11-21_v6.0d_crosslinks_price_charts_and_api_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

ROUTE_LINKS_JS = '// Cross-link any medicine\'s Drugs@FDA dosage forms/routes and modality to the v6.0\n// Pharmaceutical Encyclopedia (#/ref/routes, #/ref/departments/<id>) and Equipment Market.\nimport { html } from "./ui.js";\n\nconst ROUTE_RULES = [\n  { id: "oral-solid", label: "Oral Solid Dosage", rx: /\\boral\\b|tablet|capsule|lozenge|granule|pellet/i, modality: "oral_solid" },\n  { id: "sterile-parenteral", label: "Sterile Parenteral (IV/SC/IM)", rx: /intravenous|subcutaneous|intramuscular|inject|parenteral|infusion|intrathecal|intravitreal/i, modality: "sterile" },\n  { id: "lnp-oligo", label: "LNP & Oligonucleotide Delivery", rx: /oligonucleotide|sirna|antisense|lipid nanoparticle|mrna/i, modality: "oligo_peptide" },\n  { id: "inhaled-pulmonary", label: "Inhaled & Pulmonary", rx: /inhal|aerosol|nebul|pulmonary|nasal|respiratory/i, modality: "small_molecule" },\n  { id: "ophthalmic-transdermal", label: "Ophthalmic, Topical & Transdermal", rx: /ophthalmic|topical|transdermal|patch|cream|ointment|gel|otic/i, modality: "small_molecule" },\n];\n\nexport function inferRoutesForDrug(d) {\n  const us = (d && d.us) || {};\n  const blob = [\n    ...(us.routes || []),\n    ...(us.forms || []),\n    (d && d.type) || "",\n  ].join(" ; ");\n  const matched = [];\n  for (const r of ROUTE_RULES) {\n    if (r.rx.test(blob)) matched.push(r);\n  }\n  return matched;\n}\n\nexport function renderRouteLinksHtml(d) {\n  const routes = inferRoutesForDrug(d);\n  if (!routes.length) return "";\n  const firstMod = routes[0].modality;\n  return html`<p class="muted small">Formulation &amp; delivery guides: ${routes.map((r, i) =>\n    html`${i ? " · " : ""}<a href="#/ref/routes#${r.id}">${r.label}</a>`)} · <a href="#/ref/departments/formulation">Formulation Dept</a> · <a href="#/ref/equipment?modality=${firstMod}">Related equipment</a></p>`;\n}\n'
IMPORT_USED_EQUIPMENT_PY = '#!/usr/bin/env python3\n"""Import periodic secondary/used pharmaceutical equipment marketplace listings into time-series snapshots.\n\nReads a CSV or JSON export of used-equipment asking prices (e.g., from EquipNet, LabX,\nFederal Equipment Co., or Surplus Solutions) with columns/fields:\n  `equipment_id` (e.g., `eq-hplc-uplc`), `snapshot_period` (e.g., `2026-11`), `price_usd`,\n  and optional `platform`, `condition`.\n\nTrims 10th-90th percentile outliers when sample_size >= 10, merges chronologically into\n`raw/used_equipment_snapshots.json` (preserving prior snapshot periods so price bands can\nbe tracked over time), and updates each category\'s latest `used_market_range_usd`.\n\nUsage:\n  python3 pipeline/import_used_equipment.py --file listings_2026_11.csv raw/used_equipment_snapshots.json\n"""\nimport argparse\nimport collections\nimport csv\nimport json\nimport pathlib\nimport re\nimport statistics\nimport sys\n\n\ndef _trim_band(amounts: list) -> dict | None:\n    vals = sorted(float(a) for a in amounts if a is not None and float(a) > 0)\n    if not vals:\n        return None\n    if len(vals) >= 10:\n        lo_i = int(len(vals) * 0.10)\n        hi_i = max(lo_i + 1, int(len(vals) * 0.90))\n        vals = vals[lo_i:hi_i]\n    return {\n        "low": round(vals[0], 2),\n        "median": round(statistics.median(vals), 2),\n        "high": round(vals[-1], 2),\n        "sample_size": len(vals),\n    }\n\n\ndef _parse_price(v) -> float | None:\n    s = re.sub(r"[^0-9.]", "", str(v or ""))\n    if not s:\n        return None\n    val = float(s)\n    return val if val > 0 else None\n\n\ndef load_listings(path: pathlib.Path) -> list:\n    if path.suffix.lower() == ".json":\n        data = json.loads(path.read_text(encoding="utf-8"))\n        return data if isinstance(data, list) else data.get("listings", [])\n    with path.open("r", encoding="utf-8-sig", newline="") as fh:\n        return list(csv.DictReader(fh))\n\n\ndef merge_snapshots(listings: list, existing: dict) -> dict:\n    grouped = collections.defaultdict(lambda: collections.defaultdict(list))\n    for row in listings:\n        low = {k.strip().lower(): v for k, v in row.items() if k}\n        eid = str(low.get("equipment_id") or low.get("id") or "").strip()\n        period = str(low.get("snapshot_period") or low.get("period") or "").strip()\n        price = _parse_price(low.get("price_usd") or low.get("price"))\n        if not (eid and re.match(r"^eq-[a-z0-9-]+$", eid) and period and price):\n            continue\n        grouped[eid][period].append(price)\n\n    out = json.loads(json.dumps(existing or {}))\n    for eid, periods in grouped.items():\n        cur = out.get(eid) or {"used_market_range_usd": None, "price_history": []}\n        hist_by_period = {h["snapshot_period"]: h for h in (cur.get("price_history") or []) if h.get("snapshot_period")}\n        for period, prices in periods.items():\n            band = _trim_band(prices)\n            if not band:\n                continue\n            hist_by_period[period] = {\n                "snapshot_period": period,\n                "low_usd": band["low"],\n                "median_usd": band["median"],\n                "high_usd": band["high"],\n                "sample_size": band["sample_size"],\n            }\n        ordered = [hist_by_period[p] for p in sorted(hist_by_period)]\n        latest = ordered[-1] if ordered else None\n        out[eid] = {\n            "used_market_range_usd": (\n                {"low": latest["low_usd"], "median": latest["median_usd"], "high": latest["high_usd"], "sample_size": latest["sample_size"]}\n                if latest else None\n            ),\n            "price_history": ordered,\n        }\n    return out\n\n\ndef main(argv=None) -> int:\n    ap = argparse.ArgumentParser(description="Merge secondary-market used equipment listings into time-series snapshots.")\n    ap.add_argument("out_json", type=pathlib.Path, help="Target snapshot file (e.g., raw/used_equipment_snapshots.json)")\n    ap.add_argument("--file", required=True, type=pathlib.Path, help="Input CSV or JSON listings file")\n    args = ap.parse_args(argv)\n    existing = json.loads(args.out_json.read_text(encoding="utf-8")) if args.out_json.is_file() else {}\n    merged = merge_snapshots(load_listings(args.file), existing)\n    args.out_json.parent.mkdir(parents=True, exist_ok=True)\n    args.out_json.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    print(json.dumps({"categories_tracked": len(merged), "written": str(args.out_json)}, indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
PRICE_SVG_HELPER_JS = '\nexport function renderPriceHistorySvg(history = []) {\n  if (!Array.isArray(history) || !history.length) return "";\n  const w = 360, h = 92, pad = 16;\n  const maxVal = Math.max(...history.map((p) => Number(p.high_usd || p.median_usd || 0)), 1);\n  const minVal = Math.min(...history.map((p) => Number(p.low_usd || p.median_usd || 0)), maxVal);\n  const span = Math.max(maxVal - minVal, 1);\n  const y = (v) => (h - pad - ((Number(v) - minVal) / span) * (h - 2 * pad)).toFixed(1);\n  const x = (i) => (history.length === 1 ? w / 2 : pad + (i / (history.length - 1)) * (w - 2 * pad)).toFixed(1);\n\n  const medPts = history.map((p, i) => `${x(i)},${y(p.median_usd)}`).join(" ");\n  const bandPoly = [\n    ...history.map((p, i) => `${x(i)},${y(p.high_usd)}`),\n    ...[...history].reverse().map((p, ri) => `${x(history.length - 1 - ri)},${y(p.low_usd)}`),\n  ].join(" ");\n  const first = history[0].snapshot_period;\n  const last = history[history.length - 1].snapshot_period;\n  return html`<figure class="price-chart" aria-label="Used equipment price trend ${first} to ${last}">\n    <svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" style="max-width:100%;height:auto;display:block">\n      ${history.length >= 2 ? html`<polygon points="${bandPoly}" fill="currentColor" opacity="0.14"/>\n      <polyline points="${medPts}" fill="none" stroke="var(--accent,#cc2f5a)" stroke-width="2.5"/>` : ""}\n      ${history.map((p, i) => html`<circle cx="${x(i)}" cy="${y(p.median_usd)}" r="3.5" fill="var(--accent,#cc2f5a)"><title>${p.snapshot_period}: median ${fmtUsd(p.median_usd)} (${fmtUsd(p.low_usd)}–${fmtUsd(p.high_usd)}, n=${p.sample_size || "?"})</title></circle>`)}\n    </svg>\n    <figcaption class="muted small">Tracked secondary-market band (${first}${last !== first ? ` → ${last}` : ""}): low ${fmtUsd(minVal)} · high ${fmtUsd(maxVal)}</figcaption>\n  </figure>`;\n}\n'
APP_V60_ENDPOINTS = '\n\n# v6.0 endpoints: Pharmaceutical Encyclopedia (departments/routes), Equipment Market, & Vendors/CDMOs\n@app.get("/api/departments")\ndef api_departments():\n    return load("departments.json")\n\n\n@app.get("/api/routes")\ndef api_routes():\n    return load("departments.json").get("routes", [])\n\n\n@app.get("/api/equipment")\ndef api_equipment(dept: str = "", stage: str = "", modality: str = "", q: str = ""):\n    items = load("equipment.json")\n    ql = q.strip().lower()\n    rows = [\n        e for e in items\n        if (not dept or e.get("department") == dept)\n        and (not stage or stage in (e.get("stages") or []))\n        and (not modality or modality in (e.get("modalities") or []))\n        and (not ql or ql in f"{e.get(\'name\',\'\')} {e.get(\'id\',\'\')} {e.get(\'department\',\'\')} {e.get(\'plain_summary\',\'\')} {\' \'.join(o.get(\'name\',\'\') for o in (e.get(\'leading_oems\') or []))}".lower())\n    ]\n    return {"total": len(rows), "rows": rows}\n\n\n@app.get("/api/vendors")\ndef api_vendors(stage: str = "", modality: str = "", region: str = "", compliance: str = "", q: str = "", limit: int = Query(100, le=1000), offset: int = 0):\n    idx = load("vendors_index.json")\n    ql = q.strip().lower()\n    rows = [\n        r for r in (idx.get("rows") or [])\n        if (not stage or stage in (r.get("stages") or []))\n        and (not modality or modality in (r.get("modalities") or []))\n        and (not region or r.get("region") == region)\n        and (compliance != "nai_latest" or r.get("latest_classification") == "NAI")\n        and (compliance != "has_oai" or (r.get("oai") or 0) > 0)\n        and (compliance != "has_wl" or (r.get("warning_letter_count") or 0) > 0)\n        and (not ql or ql in f"{r.get(\'firm_name\',\'\')} {r.get(\'parent_company\',\'\')} {r.get(\'fei\',\'\')} {r.get(\'city\',\'\')} {r.get(\'country\',\'\')}".lower())\n    ]\n    return {"total": len(rows), "scope_note": idx.get("scope_note", ""), "checked": idx.get("checked", ""), "rows": rows[offset:offset + limit]}\n\n\n@app.get("/api/vendors/{fei}")\ndef api_vendor_site(fei: str):\n    return load(f"vendors/{fei}.json")\n'


def _patch_reference_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if 'from "./route_links.js"' not in txt:
        imp_anchor = 'import { worldRows, usSummary, howTaken, worldTimeline } from "./drugfacts.js";'
        if imp_anchor not in txt:
            raise ValueError(f"Missing import anchor in {path}")
        txt = txt.replace(imp_anchor, imp_anchor + '\nimport { renderRouteLinksHtml } from "./route_links.js";', 1)
        changed = True
    if "renderRouteLinksHtml(d)" not in txt:
        dosage_anchor = '<p class="muted">Dosage forms: ${us.forms.join(", ") || "not recorded"}. Routes: ${us.routes.join(", ") || "not recorded"}.</p>'
        if dosage_anchor not in txt:
            raise ValueError(f"Missing dosage forms anchor in {path}")
        txt = txt.replace(dosage_anchor, dosage_anchor + "\n      ${renderRouteLinksHtml(d)}", 1)
        changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_departments_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    old_tr = '<tbody>${doc.routes.map((r) => html`<tr>'
    new_tr = '<tbody>${doc.routes.map((r) => html`<tr id="${r.id}">'
    if new_tr in txt:
        return False
    if old_tr not in txt:
        return False
    path.write_text(txt.replace(old_tr, new_tr, 1), encoding="utf-8")
    return True


def _patch_equipment_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "export function renderPriceHistorySvg" not in txt:
        anchor = "export function filterEquipment"
        if anchor not in txt:
            raise ValueError(f"Missing filterEquipment anchor in {path}")
        txt = txt.replace(anchor, PRICE_SVG_HELPER_JS.lstrip() + "\n" + anchor, 1)
        changed = True
    if "renderPriceHistorySvg(e.pricing.price_history)" not in txt:
        slot = '<div><dt>Used market range</dt><dd>${fmtBand(e.pricing.used_market_range_usd)}</dd></div>\n        </dl>'
        if slot in txt:
            txt = txt.replace(slot, slot + "\n        ${renderPriceHistorySvg(e.pricing.price_history)}", 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '@app.get("/api/equipment")' in txt and '@app.get("/api/vendors")' in txt:
        return False
    anchor = 'app.mount("/", StaticFiles(directory=SITE, html=True), name="site")'
    if anchor not in txt:
        raise ValueError(f"Missing StaticFiles mount anchor in {path}")
    txt = txt.replace(anchor, APP_V60_ENDPOINTS.lstrip() + "\n\n" + anchor, 1)
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    pipe_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)

    rl = js_dir / "route_links.js"
    rl_written = (not rl.is_file()) or (rl.read_text(encoding="utf-8") != ROUTE_LINKS_JS)
    if rl_written:
        rl.write_text(ROUTE_LINKS_JS, encoding="utf-8")

    imp = pipe_dir / "import_used_equipment.py"
    imp_written = (not imp.is_file()) or (imp.read_text(encoding="utf-8") != IMPORT_USED_EQUIPMENT_PY)
    if imp_written:
        imp.write_text(IMPORT_USED_EQUIPMENT_PY, encoding="utf-8")

    return {
        "route_links_js_written": rl_written,
        "import_used_equipment_py_written": imp_written,
        "reference_js_crosslinked": _patch_reference_js(js_dir / "reference.js"),
        "departments_js_route_anchors_added": _patch_departments_js(js_dir / "departments.js"),
        "equipment_js_svg_chart_added": _patch_equipment_js(js_dir / "equipment.js"),
        "app_py_v60_endpoints_added": _patch_app_py(root / "app.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "raw").mkdir()

        (root / "site" / "js" / "reference.js").write_text(
            'import { worldRows, usSummary, howTaken, worldTimeline } from "./drugfacts.js";\n'
            '      <p class="muted">Dosage forms: ${us.forms.join(", ") || "not recorded"}. Routes: ${us.routes.join(", ") || "not recorded"}.</p>\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "departments.js").write_text(
            '<tbody>${doc.routes.map((r) => html`<tr><td>${r.name}</td></tr>`)}</tbody>\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "equipment.js").write_text(
            'export function filterEquipment(items) { return items; }\n'
            '<div><dt>Used market range</dt><dd>${fmtBand(e.pricing.used_market_range_usd)}</dd></div>\n        </dl>\n',
            encoding="utf-8",
        )
        (root / "app.py").write_text(
            'from fastapi import FastAPI, Query\nfrom fastapi.staticfiles import StaticFiles\n'
            'app = FastAPI()\ndef load(r): return {}\nSITE = "."\n'
            'app.mount("/", StaticFiles(directory=SITE, html=True), name="site")\n',
            encoding="utf-8",
        )

        r1 = apply_patch(root)
        assert all(r1.values()), f"Expected all True on first pass: {r1}"
        r2 = apply_patch(root)
        assert not any(r2.values()), f"Expected all False on idempotency pass: {r2}"

        subprocess.run([sys.executable, "-m", "py_compile", str(root / "app.py")], check=True)
        subprocess.run([sys.executable, "-m", "py_compile", str(root / "pipeline" / "import_used_equipment.py")], check=True)

        c1 = root / "used_oct.csv"
        c1.write_text(
            "equipment_id,snapshot_period,price_usd,platform\n"
            "eq-hplc-uplc,2026-10,$18000,EquipNet\n"
            "eq-hplc-uplc,2026-10,$24000,LabX\n"
            "eq-hplc-uplc,2026-10,$32000,Federal Equipment Co.\n",
            encoding="utf-8",
        )
        c2 = root / "used_nov.csv"
        c2.write_text(
            "equipment_id,snapshot_period,price_usd,platform\n"
            "eq-hplc-uplc,2026-11,$16000,EquipNet\n"
            "eq-hplc-uplc,2026-11,$26000,LabX\n"
            "eq-hplc-uplc,2026-11,$38000,Surplus Solutions\n",
            encoding="utf-8",
        )
        snap = root / "raw" / "used_equipment_snapshots.json"
        subprocess.run([sys.executable, str(root / "pipeline" / "import_used_equipment.py"), "--file", str(c1), str(snap)], check=True, capture_output=True)
        subprocess.run([sys.executable, str(root / "pipeline" / "import_used_equipment.py"), "--file", str(c2), str(snap)], check=True, capture_output=True)
        data = json.loads(snap.read_text(encoding="utf-8"))
        assert len(data["eq-hplc-uplc"]["price_history"]) == 2
        assert data["eq-hplc-uplc"]["used_market_range_usd"]["median"] == 26000.0
        assert data["eq-hplc-uplc"]["price_history"][0]["snapshot_period"] == "2026-10"
        assert data["eq-hplc-uplc"]["price_history"][1]["snapshot_period"] == "2026-11"

        print("V60D_CROSSLINKS_PRICE_CHARTS_API_SELFTEST_PASSED", json.dumps(r1, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0d Cross-Links, Equipment Price Charts, & API Parity patch.")
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
