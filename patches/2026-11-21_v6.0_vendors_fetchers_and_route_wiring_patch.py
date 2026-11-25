#!/usr/bin/env python3
"""Pill by Pill v6.0a+c Integration Patch: FDA/EMA Live Fetchers, Vendor Dossier Page, & Route Wiring.

Applies cleanly on top of `2026-11-21_pill-by-pill-source_v6.0b.zip` (or v5.26+):
  1. Adds 4 stdlib-only live/CSV fetchers in `pipeline/`:
     - `pipeline/fetch_fda_inspections.py` (FDA Data Dashboard API v1 + CSV fallback)
     - `pipeline/fetch_fda_decrs.py` (FDA DECRS bulk zip/CSV parser)
     - `pipeline/fetch_fda_warning_letters.py` (FDA Compliance Actions API v1 + CSV fallback)
     - `pipeline/fetch_ema_eudragmdp.py` (EMA EudraGMDP CSV/JSON parser)
  2. Upgrades `pipeline/build_vendors.py` (if present) to use the 2026 FDA OII Firm Profile deep link
     (`https://datadashboard.fda.gov/oii/firmprofile.htm?FEIs=<fei>`).
  3. Appends `vendorSitePage(fei)` to `site/js/vendors.js` (if present) for `#/ref/vendor/<fei>`.
  4. Idempotently wires `#/ref/vendors`, `#/ref/vendor/<fei>`, `#/ref/vendors/compare/<fei1>/<fei2>[/<fei3>]`,
     and `#/ref/equipment` into `site/js/app.js` and `site/js/layout.js` (preserving v6.0b department/route links).
  5. Adds optional `build_vendors.py` and `build_equipment_catalog.py` hooks to `pipeline/run_all.sh`.

Usage:
  python3 2026-11-21_v6.0_vendors_fetchers_and_route_wiring_patch.py --selftest
  python3 2026-11-21_v6.0_vendors_fetchers_and_route_wiring_patch.py --apply /path/to/unpacked_v6.0b_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

FETCH_FDA_INSPECTIONS_PY = '#!/usr/bin/env python3\n"""Fetch or parse FDA Data Dashboard Inspections & Form 483 Citations (Pill by Pill v6.0a).\n\nSupports two modes (stdlib only):\n  1. Live FDA Data Dashboard API (requires free OII Unified Logon credentials in env vars\n     FDA_DD_USER and FDA_DD_KEY; see https://datadashboard.fda.gov/oii/api/index.htm):\n       python3 pipeline/fetch_fda_inspections.py --api raw/\n  2. Local CSV export downloaded from https://datadashboard.fda.gov/oii/cd/inspections.htm:\n       python3 pipeline/fetch_fda_inspections.py --inspections-csv ins.csv --citations-csv cites.csv raw/\n\nWrites:\n  - <out_dir>/fda_inspections.json\n  - <out_dir>/fda_citations.json\n"""\nimport argparse\nimport csv\nimport json\nimport os\nimport pathlib\nimport re\nimport sys\nimport urllib.request\n\nAPI_BASE = "https://api-datadashboard.fda.gov/v1"\nUSER_AGENT = "PillByPill/6.0a (educational pharmaceutical reference; https://pillbypill.netlify.app)"\n\nCLASS_MAP = {\n    "NO ACTION INDICATED": "NAI",\n    "NO ACTION INDICATED (NAI)": "NAI",\n    "NAI": "NAI",\n    "VOLUNTARY ACTION INDICATED": "VAI",\n    "VOLUNTARY ACTION INDICATED (VAI)": "VAI",\n    "VAI": "VAI",\n    "OFFICIAL ACTION INDICATED": "OAI",\n    "OFFICIAL ACTION INDICATED (OAI)": "OAI",\n    "OAI": "OAI",\n}\n\n\ndef _norm_fei(v) -> str:\n    return re.sub(r"\\D+", "", str(v or "")).strip()\n\n\ndef _norm_class(v) -> str:\n    s = str(v or "").strip().upper()\n    return CLASS_MAP.get(s, s if s in ("NAI", "VAI", "OAI") else "OTHER")\n\n\ndef _pick(row: dict, *keys) -> str:\n    low = {k.strip().lower(): v for k, v in row.items() if k}\n    for k in keys:\n        if k.lower() in low and str(low[k.lower()] or "").strip():\n            return str(low[k.lower()]).strip()\n    return ""\n\n\ndef normalize_inspection_row(row: dict) -> dict | None:\n    fei = _norm_fei(_pick(row, "FEINumber", "FEI Number", "fei", "FEI"))\n    if not fei:\n        return None\n    proj = _pick(row, "ProjectArea", "Project Area", "ProductType", "Product Type", "project_area")\n    if proj and not re.search(r"drug|biolog|cder|cber|pharma|compounding", proj, re.I):\n        return None\n    return {\n        "fei": fei,\n        "firm_name": _pick(row, "LegalName", "Legal Name", "FirmName", "Firm Name", "firm_name"),\n        "city": _pick(row, "City", "city"),\n        "state": _pick(row, "State", "state"),\n        "country": _pick(row, "CountryName", "Country/Area", "Country", "country"),\n        "end_date": _pick(row, "InspectionEndDate", "Inspection End Date", "end_date", "date"),\n        "classification": _norm_class(_pick(row, "Classification", "ClassificationCode", "classification")),\n        "project_area": proj or "Drugs",\n        "inspection_id": _pick(row, "InspectionID", "Inspection ID", "inspection_id"),\n    }\n\n\ndef normalize_citation_row(row: dict) -> dict | None:\n    fei = _norm_fei(_pick(row, "FEINumber", "FEI Number", "fei", "FEI"))\n    if not fei:\n        return None\n    return {\n        "fei": fei,\n        "inspection_id": _pick(row, "InspectionID", "Inspection ID", "inspection_id"),\n        "date": _pick(row, "InspectionEndDate", "Inspection End Date", "date"),\n        "cfr": _pick(row, "ActCFRNumber", "Act/CFR Number", "cfr", "CFR"),\n        "description": _pick(row, "ShortDescription", "Short Description", "LongDescription", "description"),\n    }\n\n\ndef parse_csv(path: pathlib.Path, normalizer) -> list:\n    out = []\n    with path.open("r", encoding="utf-8-sig", newline="") as fh:\n        for row in csv.DictReader(fh):\n            rec = normalizer(row)\n            if rec:\n                out.append(rec)\n    return out\n\n\ndef _post_dd(endpoint: str, body: dict, user: str, key: str) -> list:\n    req = urllib.request.Request(\n        f"{API_BASE}/{endpoint}",\n        data=json.dumps(body).encode("utf-8"),\n        headers={\n            "Content-Type": "application/json",\n            "User-Agent": USER_AGENT,\n            "Authorization-User": user,\n            "Authorization-Key": key,\n        },\n        method="POST",\n    )\n    with urllib.request.urlopen(req, timeout=45) as r:\n        data = json.loads(r.read().decode("utf-8"))\n    return data.get("result") or []\n\n\ndef fetch_api(user: str, key: str, max_rows: int = 5000) -> tuple[list, list]:\n    ins_body = {\n        "start": 1, "rows": max_rows, "returntotalcount": True,\n        "sort": "InspectionEndDate", "sortorder": "DESC",\n        "filters": {"ProductType": ["Drugs", "Biologics"]},\n        "columns": ["FEINumber", "LegalName", "City", "State", "CountryName",\n                    "InspectionID", "InspectionEndDate", "Classification", "ProjectArea"],\n    }\n    cit_body = {\n        "start": 1, "rows": max_rows, "returntotalcount": True,\n        "sort": "InspectionEndDate", "sortorder": "DESC",\n        "filters": {"ProductType": ["Drugs", "Biologics"]},\n        "columns": ["FEINumber", "InspectionID", "InspectionEndDate", "ActCFRNumber", "ShortDescription"],\n    }\n    ins = [r for r in (normalize_inspection_row(x) for x in _post_dd("inspections_classifications", ins_body, user, key)) if r]\n    cits = [r for r in (normalize_citation_row(x) for x in _post_dd("inspections_citations", cit_body, user, key)) if r]\n    return ins, cits\n\n\ndef main(argv=None) -> int:\n    ap = argparse.ArgumentParser(description="Fetch or parse FDA Data Dashboard Inspections & 483 Citations.")\n    ap.add_argument("out_dir", type=pathlib.Path, help="Output directory (e.g., raw/)")\n    ap.add_argument("--api", action="store_true", help="Pull from api-datadashboard.fda.gov/v1 (needs FDA_DD_USER & FDA_DD_KEY)")\n    ap.add_argument("--inspections-csv", type=pathlib.Path, help="Local FDA Data Dashboard Inspections CSV")\n    ap.add_argument("--citations-csv", type=pathlib.Path, help="Local FDA Data Dashboard Citations CSV")\n    ap.add_argument("--max-rows", type=int, default=5000)\n    args = ap.parse_args(argv)\n\n    args.out_dir.mkdir(parents=True, exist_ok=True)\n    ins, cits = [], []\n    if args.api:\n        user, key = os.environ.get("FDA_DD_USER", ""), os.environ.get("FDA_DD_KEY", "")\n        if not (user and key):\n            sys.exit("Error: set FDA_DD_USER and FDA_DD_KEY (see https://datadashboard.fda.gov/oii/api/index.htm) or use --inspections-csv.")\n        ins, cits = fetch_api(user, key, args.max_rows)\n    else:\n        if args.inspections_csv:\n            ins = parse_csv(args.inspections_csv, normalize_inspection_row)\n        if args.citations_csv:\n            cits = parse_csv(args.citations_csv, normalize_citation_row)\n\n    (args.out_dir / "fda_inspections.json").write_text(json.dumps(ins, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    (args.out_dir / "fda_citations.json").write_text(json.dumps(cits, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    print(json.dumps({"inspections": len(ins), "citations": len(cits), "out_dir": str(args.out_dir)}, indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
FETCH_FDA_DECRS_PY = '#!/usr/bin/env python3\n"""Parse FDA Drug Establishments Current Registration Site (DECRS) bulk registration export.\n\nReads a DECRS bulk zip or delimited CSV/TXT file (from https://www.accessdata.fda.gov/scripts/cder/drls/)\nand writes FEI-keyed facility capabilities into `raw/fda_decrs.json`.\n\nUsage:\n  python3 pipeline/fetch_fda_decrs.py --file decrs_current.csv raw/fda_decrs.json\n"""\nimport argparse\nimport csv\nimport io\nimport json\nimport pathlib\nimport re\nimport sys\nimport zipfile\n\n\ndef _norm_fei(v) -> str:\n    return re.sub(r"\\D+", "", str(v or "")).strip()\n\n\ndef _pick(row: dict, *keys) -> str:\n    low = {k.strip().lower(): v for k, v in row.items() if k}\n    for k in keys:\n        if k.lower() in low and str(low[k.lower()] or "").strip():\n            return str(low[k.lower()]).strip()\n    return ""\n\n\ndef parse_decrs_text(text: str) -> list:\n    sample = text[:4096]\n    delim = "\\t" if sample.count("\\t") > sample.count(",") else ","\n    reader = csv.DictReader(io.StringIO(text), delimiter=delim)\n    by_fei = {}\n    for row in reader:\n        fei = _norm_fei(_pick(row, "FEI_NUMBER", "FEI NUMBER", "FEI", "fei"))\n        if not fei:\n            continue\n        firm = _pick(row, "FIRM_NAME", "FIRM NAME", "ESTABLISHMENT_NAME", "firm_name")\n        ops_raw = _pick(row, "BUSINESS_OPERATIONS", "BUSINESS OPERATIONS", "OPERATIONS", "operations")\n        ops = [o.strip() for o in re.split(r"[;|,]", ops_raw) if o.strip()]\n        if fei not in by_fei:\n            by_fei[fei] = {\n                "fei": fei,\n                "firm_name": firm,\n                "parent_company": _pick(row, "PARENT_COMPANY", "parent_company") or firm,\n                "city": _pick(row, "CITY", "city"),\n                "state": _pick(row, "STATE_PROVINCE", "STATE", "state"),\n                "country": _pick(row, "COUNTRY_CODE", "COUNTRY", "country"),\n                "operations": [],\n                "url": "https://www.accessdata.fda.gov/scripts/cder/drls/",\n            }\n        by_fei[fei]["operations"] = sorted(set(by_fei[fei]["operations"] + ops))\n    return sorted(by_fei.values(), key=lambda x: x["fei"])\n\n\ndef load_decrs_file(path: pathlib.Path) -> list:\n    if path.suffix.lower() == ".zip":\n        with zipfile.ZipFile(path, "r") as z:\n            members = [n for n in z.namelist() if n.lower().endswith((".csv", ".txt", ".tsv")) and "excluded" not in n.lower()]\n            if not members:\n                raise ValueError(f"No CSV/TXT registration file found in {path}")\n            return parse_decrs_text(z.read(members[0]).decode("utf-8-sig", errors="replace"))\n    return parse_decrs_text(path.read_text(encoding="utf-8-sig", errors="replace"))\n\n\ndef main(argv=None) -> int:\n    ap = argparse.ArgumentParser(description="Parse FDA DECRS bulk establishment registration file.")\n    ap.add_argument("out_json", type=pathlib.Path, help="Output path (e.g., raw/fda_decrs.json)")\n    ap.add_argument("--file", required=True, type=pathlib.Path, help="Local DECRS .zip, .csv, or .txt export")\n    args = ap.parse_args(argv)\n    rows = load_decrs_file(args.file)\n    args.out_json.parent.mkdir(parents=True, exist_ok=True)\n    args.out_json.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    print(json.dumps({"sites": len(rows), "written": str(args.out_json)}, indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
FETCH_FDA_WARNING_LETTERS_PY = '#!/usr/bin/env python3\n"""Fetch or parse FDA Drug & Biologics Warning Letters (Pill by Pill v6.0a).\n\nSupports:\n  1. Live FDA Data Dashboard Compliance Actions API (`--api`, uses FDA_DD_USER / FDA_DD_KEY)\n  2. Local CSV export from https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters (`--file`)\n\nWrites `raw/fda_warning_letters.json`.\n"""\nimport argparse\nimport csv\nimport json\nimport os\nimport pathlib\nimport re\nimport sys\nimport urllib.request\n\nAPI_URL = "https://api-datadashboard.fda.gov/v1/compliance_actions"\nDEFAULT_WL_URL = "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters"\n\n\ndef _norm_fei(v) -> str:\n    return re.sub(r"\\D+", "", str(v or "")).strip()\n\n\ndef _pick(row: dict, *keys) -> str:\n    low = {k.strip().lower(): v for k, v in row.items() if k}\n    for k in keys:\n        if k.lower() in low and str(low[k.lower()] or "").strip():\n            return str(low[k.lower()]).strip()\n    return ""\n\n\ndef normalize_wl_row(row: dict) -> dict | None:\n    fei = _norm_fei(_pick(row, "FEINumber", "FEI Number", "fei", "FEI"))\n    if not fei:\n        return None\n    closeout = _pick(row, "CloseoutDate", "Closeout Letter", "Closeout Date")\n    status = "Closed" if closeout else (_pick(row, "Status", "status") or "Open")\n    url = _pick(row, "ActionURL", "URL", "url")\n    if not url.startswith("https://"):\n        url = DEFAULT_WL_URL\n    return {\n        "fei": fei,\n        "firm_name": _pick(row, "LegalName", "Company Name", "Firm Name", "firm_name"),\n        "date": _pick(row, "ActionTakenDate", "Letter Issue Date", "date"),\n        "subject": _pick(row, "Subject", "Issuing Office", "subject") or "CGMP / Drug Manufacturing",\n        "status": status,\n        "url": url,\n    }\n\n\ndef parse_wl_csv(path: pathlib.Path) -> list:\n    out = []\n    with path.open("r", encoding="utf-8-sig", newline="") as fh:\n        for row in csv.DictReader(fh):\n            rec = normalize_wl_row(row)\n            if rec:\n                out.append(rec)\n    return out\n\n\ndef fetch_api(user: str, key: str, max_rows: int = 3000) -> list:\n    body = {\n        "start": 1, "rows": max_rows, "returntotalcount": True,\n        "sort": "ActionTakenDate", "sortorder": "DESC",\n        "filters": {"ActionType": ["Warning Letter"], "ProductType": ["Drugs", "Biologics"]},\n        "columns": ["FEINumber", "LegalName", "ActionTakenDate", "ActionType", "CaseInjunctionID", "ProductType"],\n    }\n    req = urllib.request.Request(\n        API_URL,\n        data=json.dumps(body).encode("utf-8"),\n        headers={"Content-Type": "application/json", "Authorization-User": user, "Authorization-Key": key},\n        method="POST",\n    )\n    with urllib.request.urlopen(req, timeout=45) as r:\n        rows = json.loads(r.read().decode("utf-8")).get("result") or []\n    return [r for r in (normalize_wl_row(x) for x in rows) if r]\n\n\ndef main(argv=None) -> int:\n    ap = argparse.ArgumentParser(description="Fetch or parse FDA Drug/Biologics Warning Letters.")\n    ap.add_argument("out_json", type=pathlib.Path)\n    ap.add_argument("--api", action="store_true")\n    ap.add_argument("--file", type=pathlib.Path)\n    args = ap.parse_args(argv)\n    if args.api:\n        user, key = os.environ.get("FDA_DD_USER", ""), os.environ.get("FDA_DD_KEY", "")\n        if not (user and key):\n            sys.exit("Error: set FDA_DD_USER and FDA_DD_KEY or pass --file <warning_letters.csv>.")\n        rows = fetch_api(user, key)\n    elif args.file:\n        rows = parse_wl_csv(args.file)\n    else:\n        rows = []\n    args.out_json.parent.mkdir(parents=True, exist_ok=True)\n    args.out_json.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    print(json.dumps({"warning_letters": len(rows), "written": str(args.out_json)}, indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
FETCH_EMA_EUDRAGMDP_PY = '#!/usr/bin/env python3\n"""Parse EMA EudraGMDP GMP Certificates / Non-Compliance Reports into FEI-keyed JSON (Pill by Pill v6.0a).\n\nReads a local EudraGMDP CSV or JSON export (from https://eudragmdp.ema.europa.eu/) and writes\na mapping `{ "<fei>": { "status": ..., "certificate_no": ..., "inspection_date": ..., "url": ... } }`\ninto `raw/ema_eudragmdp.json`.\n"""\nimport argparse\nimport csv\nimport json\nimport pathlib\nimport re\n\nDEFAULT_URL = "https://eudragmdp.ema.europa.eu/"\n\n\ndef _norm_fei(v) -> str:\n    return re.sub(r"\\D+", "", str(v or "")).strip()\n\n\ndef parse_eudragmdp(path: pathlib.Path) -> dict:\n    out = {}\n    if path.suffix.lower() == ".json":\n        raw = json.loads(path.read_text(encoding="utf-8"))\n        items = raw.values() if isinstance(raw, dict) else raw\n    else:\n        with path.open("r", encoding="utf-8-sig", newline="") as fh:\n            items = list(csv.DictReader(fh))\n\n    for row in items:\n        low = {k.strip().lower(): v for k, v in row.items() if k}\n        fei = _norm_fei(low.get("fei") or low.get("feinumber") or low.get("fei number"))\n        if not fei:\n            continue\n        url = str(low.get("url") or DEFAULT_URL).strip()\n        if not url.startswith("https://"):\n            url = DEFAULT_URL\n        out[fei] = {\n            "status": str(low.get("status") or low.get("gmp_status") or "Valid EU GMP Certificate").strip(),\n            "certificate_no": str(low.get("certificate_no") or low.get("certificate") or "").strip(),\n            "inspection_date": str(low.get("inspection_date") or low.get("date") or "").strip(),\n            "url": url,\n        }\n    return out\n\n\ndef main(argv=None) -> int:\n    ap = argparse.ArgumentParser(description="Parse EMA EudraGMDP export into FEI-keyed JSON.")\n    ap.add_argument("out_json", type=pathlib.Path)\n    ap.add_argument("--file", required=True, type=pathlib.Path)\n    args = ap.parse_args(argv)\n    data = parse_eudragmdp(args.file)\n    args.out_json.parent.mkdir(parents=True, exist_ok=True)\n    args.out_json.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    print(json.dumps({"ema_sites": len(data), "written": str(args.out_json)}, indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
VENDOR_SITE_PAGE_JS = '\nexport async function vendorSitePage(fei) {\n  const s = await vendorSite(fei);\n  const fdaProfile = `https://datadashboard.fda.gov/oii/firmprofile.htm?FEIs=${encodeURIComponent(s.fei)}`;\n  const body = html`\n    <p><a href="#/ref/vendors">← Back to Manufacturers &amp; CDMOs</a> · <a href="${fdaProfile}" target="_blank" rel="noopener">Open live FDA Firm Profile ↗</a></p>\n    <dl class="facts">\n      <div><dt>FEI Number</dt><dd>${s.fei}</dd></div>\n      <div><dt>Location</dt><dd>${s.city ? `${s.city}, ` : ""}${s.state ? `${s.state}, ` : ""}${s.country}</dd></div>\n      <div><dt>Latest FDA Audit</dt><dd>${s.latest_inspection ? `${s.latest_inspection} (${s.latest_classification})` : "None on record"}</dd></div>\n      <div><dt>NAI / VAI / OAI</dt><dd>${s.counts.NAI} / ${s.counts.VAI} / ${s.counts.OAI} (${s.counts.total} total)</dd></div>\n      <div><dt>Form 483 Inspections</dt><dd>${s.form_483_count}</dd></div>\n      <div><dt>EU GMP (EudraGMDP)</dt><dd>${(s.ema_gmp && s.ema_gmp.status) || "Not matched"}</dd></div>\n    </dl>\n    <h2>Registered Capabilities (FDA DECRS)</h2>\n    <p>${(s.operations || []).join(" · ") || "No operations listed in DECRS export."}</p>\n    <h2>FDA Inspection History</h2>\n    ${s.inspections.length ? html`<div class="tbl-wrap" tabindex="0" role="region" aria-label="Inspection history">\n      <table class="tbl"><thead><tr><th>End Date</th><th>Classification</th><th>Project Area</th><th>Inspection ID</th></tr></thead>\n      <tbody>${s.inspections.map((i) => html`<tr><td>${i.date || "—"}</td><td><b>${i.classification}</b></td><td>${i.project_area}</td><td>${i.inspection_id || "—"}</td></tr>`)}</tbody></table>\n    </div>` : html`<p class="muted">No FDA inspections loaded for this FEI.</p>`}\n    <h2>Top Form 483 Citation Themes (21 CFR)</h2>\n    ${(s.top_483_themes || []).length ? html`<ul class="plain">${s.top_483_themes.map((t) => html`<li><b>${t.theme}:</b> ${t.count} observation(s)</li>`)}</ul>` : html`<p class="muted">No Form 483 citation themes on record.</p>`}\n    <h2>FDA Warning Letters</h2>\n    ${(s.warning_letters || []).length ? html`<ul class="plain">${s.warning_letters.map((w) => html`<li>${w.date} — <a href="${w.url}" target="_blank" rel="noopener">${w.subject}</a> (${w.status})</li>`)}</ul>` : html`<p class="muted">No FDA Warning Letters on record.</p>`}\n    <h2>Drugs@FDA Sponsor Approvals*</h2>\n    <p>${(s.sponsor_approvals && s.sponsor_approvals.drugs_count) || 0} drugs with this firm listed as application holder.</p>\n    <p class="muted small">*${s.sponsor_approvals.note} Checked ${s.checked}.</p>`;\n  return {\n    html: page({\n      trail: [HOME, ["Manufacturers & CDMOs", "#/ref/vendors"], [s.firm_name]],\n      kicker: `FEI ${s.fei} · ${s.region}`,\n      title: s.firm_name,\n      lede: "Site-level FDA inspection outcomes, Form 483 21 CFR themes, Warning Letters, and registered manufacturing capabilities.",\n      body,\n    }),\n  };\n}\n'

APP_IMPORT_LINE = 'import * as vendors from "./vendors.js";\nimport * as equipment from "./equipment.js";'
APP_ROUTES_BLOCK = (
    '    if (a === "vendors" && b === "compare") return wrap(await vendors.vendorComparePage(parts.slice(3)), "#/ref/vendors");\n'
    '    if (a === "vendors") return wrap(await vendors.vendorsPage(query), "#/ref/vendors");\n'
    '    if (a === "vendor" && b) return wrap(await vendors.vendorSitePage(b), "#/ref/vendors");\n'
    '    if (a === "equipment") return wrap(await equipment.equipmentPage(query), "#/ref/equipment");'
)


def _wire_app_js(app_js: pathlib.Path) -> bool:
    if not app_js.is_file():
        return False
    txt = app_js.read_text(encoding="utf-8")
    changed = False
    if 'from "./vendors.js"' not in txt:
        anchor = 'import * as reference from "./reference.js";'
        if anchor not in txt:
            raise ValueError(f"Could not find reference import anchor in {app_js}")
        txt = txt.replace(anchor, anchor + "\n" + APP_IMPORT_LINE, 1)
        changed = True
    if 'a === "vendors"' not in txt:
        for anchor in [
            'if (a === "routes") return wrap(await departments.routesRefPage(), "#/ref/routes");',
            'if (a === "compare") return wrap(await reference.comparePage(b, c), "#/ref/compare");',
        ]:
            if anchor in txt:
                txt = txt.replace(anchor, anchor + "\n" + APP_ROUTES_BLOCK, 1)
                changed = True
                break
        else:
            raise ValueError(f"Could not find ref route anchor in {app_js}")
    if changed:
        app_js.write_text(txt, encoding="utf-8")
    return changed


def _wire_layout_js(layout_js: pathlib.Path) -> bool:
    if not layout_js.is_file():
        return False
    txt = layout_js.read_text(encoding="utf-8")
    if '"#/ref/vendors"' in txt and '"#/ref/equipment"' in txt:
        return False
    anchor = '["#/ref/data", "Sources and method"]'
    if anchor not in txt:
        raise ValueError(f"Could not find REF_NAV anchor in {layout_js}")
    addition = '["#/ref/vendors", "Manufacturers & CDMOs"], ["#/ref/equipment", "Equipment market"], ' + anchor
    layout_js.write_text(txt.replace(anchor, addition, 1), encoding="utf-8")
    return True


def _wire_run_all_sh(run_all: pathlib.Path) -> bool:
    if not run_all.is_file():
        return False
    txt = run_all.read_text(encoding="utf-8")
    if "build_equipment_catalog.py" in txt and "build_vendors.py" in txt:
        return False
    hook = (
        "\n# v6.0a & v6.0c: Vendors/CDMOs and Equipment Market (graceful when raw feeds absent)\n"
        "[ -f pipeline/build_vendors.py ] && python3 pipeline/build_vendors.py raw site/data\n"
        "[ -f pipeline/build_equipment_catalog.py ] && python3 pipeline/build_equipment_catalog.py raw site/data\n"
    )
    run_all.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    pipe_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for fname, content in [
        ("fetch_fda_inspections.py", FETCH_FDA_INSPECTIONS_PY),
        ("fetch_fda_decrs.py", FETCH_FDA_DECRS_PY),
        ("fetch_fda_warning_letters.py", FETCH_FDA_WARNING_LETTERS_PY),
        ("fetch_ema_eudragmdp.py", FETCH_EMA_EUDRAGMDP_PY),
    ]:
        fp = pipe_dir / fname
        if not fp.is_file() or fp.read_text(encoding="utf-8") != content:
            fp.write_text(content, encoding="utf-8")
            written.append(f"pipeline/{fname}")

    # Upgrade OII Firm Profile deep link in build_vendors.py if present
    bv = pipe_dir / "build_vendors.py"
    bv_updated = False
    if bv.is_file():
        btxt = bv.read_text(encoding="utf-8")
        old_u = 'https://datadashboard.fda.gov/ora/cd/inspections.htm'
        new_u = 'https://datadashboard.fda.gov/oii/firmprofile.htm?FEIs={fei}'
        if old_u in btxt:
            bv.write_text(btxt.replace(old_u, new_u), encoding="utf-8")
            bv_updated = True

    # Append vendorSitePage(fei) to site/js/vendors.js if present
    vj = js_dir / "vendors.js"
    vj_updated = False
    if vj.is_file():
        vtxt = vj.read_text(encoding="utf-8")
        if "export async function vendorSitePage" not in vtxt:
            vj.write_text(vtxt.rstrip() + "\n" + VENDOR_SITE_PAGE_JS, encoding="utf-8")
            vj_updated = True

    return {
        "fetchers_written": written,
        "build_vendors_oii_link_updated": bv_updated,
        "vendors_js_site_page_added": vj_updated,
        "app_js_wired": _wire_app_js(js_dir / "app.js"),
        "layout_js_wired": _wire_layout_js(js_dir / "layout.js"),
        "run_all_sh_wired": _wire_run_all_sh(pipe_dir / "run_all.sh"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "raw").mkdir()

        # Minimal v6.0b-shaped app.js, layout.js, vendors.js, run_all.sh
        (root / "site" / "js" / "app.js").write_text(
            'import * as reference from "./reference.js";\n'
            'import * as departments from "./departments.js";\n'
            'if (a === "routes") return wrap(await departments.routesRefPage(), "#/ref/routes");\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "layout.js").write_text(
            'const REF_NAV = [["#/ref", "Overview"], ["#/ref/departments", "Departments"], ["#/ref/data", "Sources and method"]];\n',
            encoding="utf-8",
        )
        (root / "site" / "js" / "vendors.js").write_text(
            'export async function vendorsPage() {}\n',
            encoding="utf-8",
        )
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\npython3 pipeline/build_departments.py site/data\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert len(r1["fetchers_written"]) == 4 and r1["app_js_wired"] and r1["layout_js_wired"] and r1["vendors_js_site_page_added"] and r1["run_all_sh_wired"], r1

        # Idempotency pass
        r2 = apply_patch(root)
        assert not r2["fetchers_written"] and not r2["app_js_wired"] and not r2["layout_js_wired"] and not r2["vendors_js_site_page_added"] and not r2["run_all_sh_wired"], r2

        # Test all 4 fetcher CSV parsers on synthetic FDA/EMA exports
        ins_csv = root / "ins.csv"
        ins_csv.write_text(
            "FEINumber,LegalName,City,State,CountryName,InspectionID,InspectionEndDate,Classification,ProjectArea\n"
            "3002807001,Alpha Biologics CDMO,Visp,,Switzerland,101,2026-04-12,No Action Indicated (NAI),Biologics\n"
            "3009999999,Snack Foods LLC,Chicago,IL,United States,102,2026-01-10,NAI,Human Foods\n",
            encoding="utf-8",
        )
        cit_csv = root / "cit.csv"
        cit_csv.write_text(
            "FEINumber,InspectionID,InspectionEndDate,ActCFRNumber,ShortDescription\n"
            "3002807001,101,2026-04-12,21 CFR 211.113(b),Aseptic controls\n",
            encoding="utf-8",
        )
        subprocess.run(
            [sys.executable, str(root / "pipeline" / "fetch_fda_inspections.py"), "--inspections-csv", str(ins_csv), "--citations-csv", str(cit_csv), str(root / "raw")],
            check=True, capture_output=True, text=True,
        )
        ins_out = json.loads((root / "raw" / "fda_inspections.json").read_text(encoding="utf-8"))
        assert len(ins_out) == 1 and ins_out[0]["classification"] == "NAI", ins_out  # Human Foods filtered out

        decrs_csv = root / "decrs.csv"
        decrs_csv.write_text(
            "FEI_NUMBER,FIRM_NAME,CITY,STATE_PROVINCE,COUNTRY_CODE,BUSINESS_OPERATIONS\n"
            "3002807001,Alpha Biologics CDMO,Visp,,CH,Biologics Manufacture; Sterile Fill-Finish\n",
            encoding="utf-8",
        )
        subprocess.run(
            [sys.executable, str(root / "pipeline" / "fetch_fda_decrs.py"), "--file", str(decrs_csv), str(root / "raw" / "fda_decrs.json")],
            check=True, capture_output=True, text=True,
        )
        decrs_out = json.loads((root / "raw" / "fda_decrs.json").read_text(encoding="utf-8"))
        assert len(decrs_out) == 1 and len(decrs_out[0]["operations"]) == 2, decrs_out

        wl_csv = root / "wl.csv"
        wl_csv.write_text(
            "FEI Number,Company Name,Letter Issue Date,Subject,Closeout Date\n"
            "3002807001,Alpha Biologics CDMO,2026-02-01,CGMP/Finished Pharmaceuticals,\n",
            encoding="utf-8",
        )
        subprocess.run(
            [sys.executable, str(root / "pipeline" / "fetch_fda_warning_letters.py"), "--file", str(wl_csv), str(root / "raw" / "fda_warning_letters.json")],
            check=True, capture_output=True, text=True,
        )
        wl_out = json.loads((root / "raw" / "fda_warning_letters.json").read_text(encoding="utf-8"))
        assert len(wl_out) == 1 and wl_out[0]["status"] == "Open", wl_out

        ema_csv = root / "ema.csv"
        ema_csv.write_text(
            "FEI,Status,Certificate,Date\n"
            "3002807001,Valid EU GMP Certificate,EU-GMP-2026-001,2026-03-15\n",
            encoding="utf-8",
        )
        subprocess.run(
            [sys.executable, str(root / "pipeline" / "fetch_ema_eudragmdp.py"), "--file", str(ema_csv), str(root / "raw" / "ema_eudragmdp.json")],
            check=True, capture_output=True, text=True,
        )
        ema_out = json.loads((root / "raw" / "ema_eudragmdp.json").read_text(encoding="utf-8"))
        assert "3002807001" in ema_out and ema_out["3002807001"]["certificate_no"] == "EU-GMP-2026-001", ema_out

        print("V60_FETCHERS_AND_ROUTE_WIRING_SELFTEST_PASSED", json.dumps(r1, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0a+c Fetchers & Route Wiring patch.")
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
