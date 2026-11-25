#!/usr/bin/env python3
"""Pill by Pill v6.0k Patch: Pharmaceutical Partner Ecosystem (CROs, Central Labs, CDMOs, 3PLs, Wholesalers & Specialty/REMS Hubs).

Closes Gap C of the end-to-end pharmaceutical encyclopedia:
  1. Adds `pipeline/build_partners.py` -> `site/data/partners.json` (6 partner archetypes across all 8 stages).
  2. Adds `site/js/partners.js` (`partnersPage` for `#/ref/partners`, `partnersExplorePage` for `#/explore/partners`) with inline flow SVG.
  3. Wires `#/ref/partners` and `#/explore/partners` into `site/js/app.js` and `site/js/layout.js`.
  4. Hooks `build_partners.py` into `pipeline/run_all.sh` and adds `/api/partners` to `app.py`.

Usage:
  python3 2026-11-21_v6.0k_partner_ecosystem_patch.py --selftest
  python3 2026-11-21_v6.0k_partner_ecosystem_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_PARTNERS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.0k Pharmaceutical Partner Ecosystem dataset (`site/data/partners.json`).\n\nCovers the 6 core execution & channel partner archetypes that operate alongside drug sponsors\nfrom preclinical discovery through clinical trials, cGMP manufacturing, and patient delivery:\n  1. Contract Research Organizations (CROs)\n  2. Central & Bioanalytical Laboratories\n  3. CDMOs / CMOs (cross-linked to `#/ref/vendors`)\n  4. Third-Party Logistics (3PL) & Cold-Chain Carriers\n  5. Full-Line Pharmaceutical Wholesalers\n  6. Specialty Pharmacies & REMS Patient Support Hubs\n\nAll regulatory anchors are verified HTTPS FDA/eCFR/CMS references. Zero fabricated market shares or fees.\n\nUsage:\n  python3 pipeline/build_partners.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-21"\n\nPARTNER_ECOSYSTEM = [\n    {\n        "id": "partner-cro",\n        "name": "Contract Research Organizations (CROs)",\n        "stages": ["discovery", "clinical", "regulatory"],\n        "plain_summary": "Specialized research companies hired by drug developers to run animal safety studies, recruit hospitals and patients for Phase 1–3 clinical trials, and monitor trial data.",\n        "technical_spec": "Execute preclinical GLP toxicology and global Phase 1–4 clinical operations: site selection, IRB/ethics submissions, clinical research associate (CRA) site monitoring, biostatistics, medical writing, and pharmacovigilance.",\n        "regulatory_framework": "21 CFR Part 58 (GLP); 21 CFR Part 312 (IND / Transfer of Regulatory Obligations, 21 CFR 312.52); ICH E6 Good Clinical Practice (GCP)",\n        "commercial_model": "Full-service outsourcing (FSO) or Functional Service Provider (FSP) contracts; unit-price + pass-through investigator grants and milestone payments.",\n        "examples": ["IQVIA", "Labcorp Drug Development (Fortrea)", "ICON", "PPD (Thermo Fisher)", "Syneos Health", "Charles River Laboratories (Preclinical)"],\n        "cross_link": "#/ref/departments/clinical",\n        "sources": [\n            {"label": "eCFR — 21 CFR Part 312 (IND & Transfer of Obligations)", "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312"},\n            {"label": "FDA — Step 3: Clinical Research", "url": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research"},\n        ],\n    },\n    {\n        "id": "partner-central-lab",\n        "name": "Central & Bioanalytical Laboratories",\n        "stages": ["discovery", "analytical", "clinical"],\n        "plain_summary": "Standardized global testing labs that analyze blood, tissue, and biomarker samples shipped from hundreds of clinical trial hospitals so every patient is measured on the exact same calibrated instruments.",\n        "technical_spec": "Provides clinical trial kitting, global specimen logistics, standardized safety chemistry/hematology, genomic/companion diagnostic (CDx) assays, and GLP/GCP bioanalytical LC-MS/MS pharmacokinetic (PK) and immunogenicity (ADA) testing.",\n        "regulatory_framework": "CLIA / CAP accreditation; FDA Bioanalytical Method Validation Guidance (ICH M10); 21 CFR Part 58 / ICH E6 GCP",\n        "commercial_model": "Per-sample assay pricing, custom method development & validation fees, and long-term biorepository storage fees.",\n        "examples": ["Labcorp Central Labs", "Q2 Solutions (IQVIA)", "Eurofins BioPharma", "PPD Laboratories", "ACM Global Laboratories"],\n        "cross_link": "#/ref/equipment?dept=analytical",\n        "sources": [\n            {"label": "FDA — Step 3: Clinical Research", "url": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research"},\n            {"label": "eCFR — 21 CFR Part 58 (GLP)", "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-58"},\n        ],\n    },\n    {\n        "id": "partner-cdmo",\n        "name": "Contract Development & Manufacturing Organizations (CDMOs / CMOs)",\n        "stages": ["formulation", "analytical", "manufacturing"],\n        "plain_summary": "Specialized factories that formulate, brew, purify, and package medicines under strict FDA cleanroom rules on behalf of biotech and pharma sponsors.",\n        "technical_spec": "Executes process development, scale-up, cGMP API synthesis or biologic cell culture, sterile fill-finish/lyophilization, ICH stability testing, PPQ validation, and commercial supply.",\n        "regulatory_framework": "21 CFR Parts 210 & 211 (cGMP); FDA DECRS Establishment Registration; FDA OII Inspections (NAI/VAI/OAI) & Form 483; EMA EudraGMDP",\n        "commercial_model": "Fee-for-service development milestones, dedicated suite/capacity reservation fees, and per-batch commercial supply agreements.",\n        "examples": ["Lonza", "Catalent", "Thermo Fisher Patheon", "Samsung Biologics", "WuXi AppTec / WuXi Biologics", "Siegfried", "Recipharm"],\n        "cross_link": "#/ref/vendors",\n        "sources": [\n            {"label": "eCFR — 21 CFR Part 211 (cGMP for Finished Pharmaceuticals)", "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211"},\n            {"label": "FDA — Data Dashboard (Inspections & Compliance)", "url": "https://datadashboard.fda.gov/oii/cd/inspections.htm"},\n        ],\n    },\n    {\n        "id": "partner-3pl",\n        "name": "Third-Party Logistics (3PL) & Cold-Chain Carriers",\n        "stages": ["distribution"],\n        "plain_summary": "Temperature-controlled warehouses and specialized freight networks that store finished medicines after factory release and ship them safely to wholesalers, hospitals, and specialty pharmacies.",\n        "technical_spec": "Manages title-neutral order-to-cash warehousing, validated 2–8°C / -20°C / -80°C / cryogenic LN2 storage and shipping, DSCSA EPCIS serialization aggregation, returns/recalls processing, and state licensing.",\n        "regulatory_framework": "Drug Supply Chain Security Act (DSCSA); FDA 21 CFR Part 205 (Wholesale & 3PL Licensing); GDP (Good Distribution Practice)",\n        "commercial_model": "Pallet/storage fees, pick-and-pack transaction fees, and validated thermal-lane freight charges.",\n        "examples": ["ICS (Cencora)", "Cardinal Health 3PL", "McKesson RxCrossroads 3PL", "UPS Healthcare / Marken", "DHL Supply Chain Life Sciences", "Cryoport"],\n        "cross_link": "#/ref/departments/distribution",\n        "sources": [\n            {"label": "FDA — Drug Supply Chain Security Act (DSCSA)", "url": "https://www.fda.gov/media/77516/download"},\n        ],\n    },\n    {\n        "id": "partner-wholesaler",\n        "name": "Full-Line Pharmaceutical Wholesalers",\n        "stages": ["commercial", "distribution"],\n        "plain_summary": "Large national distributors that buy medicines from hundreds of manufacturers and deliver daily next-day replenishment orders to tens of thousands of retail and hospital pharmacies.",\n        "technical_spec": "Aggregates nationwide pharmacy demand, takes title to inventory, processes hospital/GPO contract chargebacks, verifies DSCSA product identifiers, and manages daily multi-temperature last-mile delivery.",\n        "regulatory_framework": "DSCSA Authorized Trading Partner (ATP) & Verification Requirements; 21 CFR Part 205; DEA Controlled Substance Suspicious Order Monitoring (CSOS)",\n        "commercial_model": "Distribution Service Agreements (DSA) fee-for-service (% of WAC), prompt-pay discounts, and generic sourcing margins.",\n        "examples": ["McKesson", "Cencora (formerly AmerisourceBergen)", "Cardinal Health"],\n        "cross_link": "#/ref/economics",\n        "sources": [\n            {"label": "FDA — Drug Supply Chain Security Act (DSCSA)", "url": "https://www.fda.gov/media/77516/download"},\n            {"label": "CMS — Medicare Drug Price Negotiation & Supply Chain Context", "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program"},\n        ],\n    },\n    {\n        "id": "partner-specialty-rems",\n        "name": "Specialty Pharmacies & REMS Patient Support Hubs",\n        "stages": ["commercial", "distribution"],\n        "plain_summary": "High-touch pharmacies and patient-support centers that handle complex, expensive, or high-risk medicines—coordinating insurance prior authorizations, nurse injection training, cold-chain home delivery, and FDA safety checks.",\n        "technical_spec": "Operates limited-distribution networks (LDNs) for biologics, oncology, and rare-disease therapies; executes payer benefit verification, prior authorization, copay/foundation assistance routing, adherence monitoring, and mandatory FDA REMS Elements to Assure Safe Use (ETASU) verification.",\n        "regulatory_framework": "FDA Risk Evaluation and Mitigation Strategies (REMS, FD&C Act § 505-1); State Boards of Pharmacy; URAC / ACHC Specialty Accreditation; HIPAA",\n        "commercial_model": "Dispensing fees, limited-distribution data/reporting fees, and hub patient-services program fees.",\n        "examples": ["CVS Specialty", "Accredo (Express Scripts)", "Optum Specialty Pharmacy", "AllianceRx Walgreens", "Biologics by McKesson", "PANTHERx Rare"],\n        "cross_link": "#/ref/departments/distribution",\n        "sources": [\n            {"label": "FDA — Step 5: Post-Market Drug Safety Monitoring & REMS", "url": "https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring"},\n        ],\n    },\n]\n\n\ndef build_partners(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    out_path = data_dir / "partners.json"\n    payload = {\n        "checked": CHECKED,\n        "count": len(PARTNER_ECOSYSTEM),\n        "scope_note": "Describes the functional roles and regulatory frameworks of pharmaceutical execution and distribution partners. Pill by Pill does not endorse commercial vendors or fabricate contract pricing.",\n        "partners": PARTNER_ECOSYSTEM,\n    }\n    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {"partner_archetypes": len(PARTNER_ECOSYSTEM)}\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_partners(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
PARTNERS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderPartnerFlowSvg() {\n  const nodes = [\n    { x: 8, label: "CROs & Labs", sub: "Trials & Assays" },\n    { x: 140, label: "CDMOs / CMOs", sub: "cGMP Factories" },\n    { x: 272, label: "3PL & Cold-Chain", sub: "Storage & Freight" },\n    { x: 404, label: "Wholesalers", sub: "National Dist." },\n    { x: 536, label: "Specialty / REMS", sub: "Patient Delivery" },\n  ];\n  return html`<figure class="partner-map" aria-label="Pharmaceutical partner ecosystem from clinical trials to patient delivery">\n    <svg viewBox="0 0 662 84" width="662" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="118" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="var(--line,#94a3b8)" stroke-width="1.5"/>\n        <text x="${n.x + 59}" y="35" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 59}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 118}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Who executes each link in the pharmaceutical value chain alongside the drug sponsor.</figcaption>\n  </figure>`;\n}\n\nexport async function partnersPage(query) {\n  const doc = await getJSON("data/partners.json");\n  const items = doc.partners || [];\n  const stage = (query && query.get("stage")) || "";\n  const filtered = stage ? items.filter((p) => (p.stages || []).includes(stage)) : items;\n  return {\n    title: "Pharma Partner Ecosystem (CROs, CDMOs, 3PLs & Specialty)",\n    body: html`\n      <h1>Pharmaceutical Partner Ecosystem</h1>\n      <p class="lead">No single drug company does everything in-house. Explore the ${items.length} specialized partner types that execute clinical trials, laboratory testing, cGMP manufacturing, cold-chain logistics, and specialty patient delivery (checked ${doc.checked}).</p>\n      ${renderPartnerFlowSvg()}\n      <p class="small">Filter by stage:\n        <a href="#/ref/partners">All</a> ·\n        <a href="#/ref/partners?stage=discovery">Discovery</a> ·\n        <a href="#/ref/partners?stage=clinical">Clinical Trials</a> ·\n        <a href="#/ref/partners?stage=manufacturing">Manufacturing</a> ·\n        <a href="#/ref/partners?stage=commercial">Commercial</a> ·\n        <a href="#/ref/partners?stage=distribution">Distribution</a>\n      </p>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharmaceutical partner ecosystem">\n        <table class="tbl"><thead><tr>\n          <th>Partner Archetype</th><th>Stages</th><th>Operational Scope &amp; Regulation</th><th>Contract Model &amp; Examples</th>\n        </tr></thead>\n        <tbody>${filtered.map((p) => html`<tr id="${p.id}">\n          <td><b>${p.name}</b><br><span class="muted small">${p.plain_summary}</span><br><a class="small" href="${p.cross_link}">Related view →</a></td>\n          <td>${(p.stages || []).map((st) => html`<a href="#/ref/departments/${st}">${st}</a>`).join(", ")}</td>\n          <td>${p.technical_spec}<br><span class="muted small"><b>Oversight:</b> ${p.regulatory_framework}</span></td>\n          <td>${p.commercial_model}<br><span class="muted small"><b>Examples:</b> ${(p.examples || []).join(", ")}</span></td>\n        </tr>`)}</tbody></table>\n      </div>\n      <p class="muted small">${doc.scope_note}</p>\n    `,\n  };\n}\n\nexport async function partnersExplorePage() {\n  const doc = await getJSON("data/partners.json");\n  const items = doc.partners || [];\n  return {\n    title: "Who Helps Build & Deliver Medicines",\n    body: html`\n      <h1>Who Helps Build &amp; Deliver Medicines</h1>\n      <p class="lead">Turning a scientific idea into a medicine on a pharmacy shelf takes a whole relay team of specialized organizations.</p>\n      ${renderPartnerFlowSvg()}\n      <ol>${items.map((p) => html`<li><b>${p.name}:</b> ${p.plain_summary}</li>`)}</ol>\n      <p class="muted small">Explore more: <a href="#/explore/how-drugs-are-built">8-Stage Drug Lifecycle</a> · <a href="#/explore/economics">How Medicines Are Funded &amp; Priced</a> · <a href="#/ref/partners">Reference Partner Guide</a>.</p>\n    `,\n  };\n}\n'


def _patch_app_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    imp = 'import { partnersPage, partnersExplorePage } from "./partners.js";\n'
    if "./partners.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/partners"' not in txt:
        anchor = 'if (path === "/ref/software")'
        if anchor not in txt:
            anchor = 'if (path === "/ref/equipment")'
        rep = (
            'if (path === "/ref/partners") return partnersPage(query);\n'
            '  if (path === "/explore/partners") return partnersExplorePage();\n'
            '  ' + anchor
        )
        if anchor in txt:
            txt = txt.replace(anchor, rep, 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_layout_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "#/ref/partners" in txt:
        return False
    anchor = '["#/ref/economics", "Drug economics"]'
    if anchor not in txt:
        anchor = '["#/ref/equipment", "Equipment market"]'
    if anchor in txt:
        rep = anchor + ',\n  ["#/ref/partners", "Partner ecosystem"]'
        path.write_text(txt.replace(anchor, rep, 1), encoding="utf-8")
        return True
    return False


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_partners.py" in txt:
        return False
    hook = "\n# v6.0k: Pharmaceutical Partner Ecosystem (CROs, Central Labs, CDMOs, 3PLs, Wholesalers & Specialty/REMS)\npython3 pipeline/build_partners.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/partners"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/partners")\n'
        'def api_partners():\n'
        '    return _read_json(SITE_DIR / "data" / "partners.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    pipe_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)

    fp_py = pipe_dir / "build_partners.py"
    py_written = (not fp_py.is_file()) or (fp_py.read_text(encoding="utf-8") != BUILD_PARTNERS_PY)
    if py_written:
        fp_py.write_text(BUILD_PARTNERS_PY, encoding="utf-8")

    fp_js = js_dir / "partners.js"
    js_written = (not fp_js.is_file()) or (fp_js.read_text(encoding="utf-8") != PARTNERS_JS)
    if js_written:
        fp_js.write_text(PARTNERS_JS, encoding="utf-8")

    return {
        "build_partners_py": py_written,
        "partners_js": js_written,
        "app_js_wired": _patch_app_js(js_dir / "app.js"),
        "layout_js_wired": _patch_layout_js(js_dir / "layout.js"),
        "run_all_sh_hooked": _patch_run_all(pipe_dir / "run_all.sh"),
        "app_py_api_added": _patch_app_py(root / "app.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data").mkdir(parents=True)

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/software") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV = [\n  ["#/ref/economics", "Drug economics"]\n];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_partners.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_partners.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out["partner_archetypes"] == 6, out

        doc = json.loads((root / "site" / "data" / "partners.json").read_text(encoding="utf-8"))
        for p in doc["partners"]:
            assert p["sources"] and all(s["url"].startswith("https://") for s in p["sources"]), p

        print("V60K_PARTNER_ECOSYSTEM_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0k Partner Ecosystem patch.")
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
