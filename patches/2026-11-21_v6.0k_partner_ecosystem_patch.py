#!/usr/bin/env python3
"""Pill by Pill v6.0k Patch: Pharma Execution Partner Ecosystem (CROs, Central Labs, GLP CTLs, 3PLs, Wholesalers & Specialty/REMS).

Closes Gap C of the end-to-end pharmaceutical encyclopedia so users understand who actually
executes every preclinical, clinical, and distribution step alongside CDMOs (`#/ref/vendors`):
  1. Adds `pipeline/build_partners.py` -> `site/data/partners.json`.
  2. Adds `site/js/partners.js` (`partnersPage`, `partnersExplorePage`).
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

BUILD_PARTNERS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.0k Pharma Partner Ecosystem dataset (`site/data/partners.json`).\n\nCovers the 6 core non-CDMO execution partner categories that run clinical trials,\npreclinical/bioanalytical testing, cold-chain logistics, wholesale replenishment,\nand specialty pharmacy / REMS distribution alongside CDMOs (`#/ref/vendors`).\n\nAll regulatory citations are verified HTTPS primary sources (FDA, eCFR).\n\nUsage:\n  python3 pipeline/build_partners.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-21"\n\nPARTNER_CATEGORIES = [\n    {\n        "id": "partner-preclinical-glp",\n        "name": "Preclinical GLP Toxicology & Contract Testing Labs (CTLs)",\n        "stages": ["discovery", "analytical"],\n        "plain_summary": "Independent labs that run required animal safety tests before human trials and perform specialized purity, sterility, and stability tests.",\n        "technical_scope": "Executes IND-enabling GLP toxicology, safety pharmacology (hERG, telemetry), bioanalysis, extractables & leachables (E&L), microbiology, and ICH stability testing.",\n        "regulatory_framework": "21 CFR Part 58 (Good Laboratory Practice — GLP); ICH M3(R2); 21 CFR Part 211 (for cGMP QC testing)",\n        "major_players": ["Charles River Laboratories", "Labcorp Early Development", "WuXi AppTec", "Eurofins BioPharma Product Testing"],\n        "sources": [\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-58",\n            "https://www.fda.gov/patients/drug-development-process/step-2-preclinical-research",\n        ],\n    },\n    {\n        "id": "partner-cro",\n        "name": "Contract Research Organizations (CROs)",\n        "stages": ["clinical", "regulatory"],\n        "plain_summary": "Specialized research companies that recruit hospitals, train study doctors, monitor patient data, and run Phase 1–3 clinical trials worldwide on behalf of drug developers.",\n        "technical_scope": "Full-service or functional clinical trial execution: protocol design, IRB/ethics submissions, site selection & monitoring (CRAs), EDC/CTMS/eTMF operations, biostatistics, and clinical study report (CSR) medical writing.",\n        "regulatory_framework": "21 CFR 312.52 (Transfer of Sponsor Obligations to a CRO); ICH E6(R2)/E6(R3) Good Clinical Practice (GCP)",\n        "major_players": ["IQVIA", "ICON", "PPD (Thermo Fisher Scientific)", "Parexel", "Fortrea", "Syneos Health"],\n        "sources": [\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312",\n            "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n        ],\n    },\n    {\n        "id": "partner-central-lab",\n        "name": "Clinical Trial Central Laboratories & Bioanalytical Labs",\n        "stages": ["clinical", "analytical"],\n        "plain_summary": "Centralized testing hubs that receive blood and tissue samples from hundreds of hospitals in a clinical trial so every patient\'s results are measured on the exact same calibrated machines.",\n        "technical_scope": "Global specimen kitting, ambient/frozen logistics, standardized clinical chemistry/hematology, genomic/biomarker assays, and LC-MS/MS or ligand-binding PK/immunogenicity bioanalysis.",\n        "regulatory_framework": "CLIA / CAP accreditation; FDA Bioanalytical Method Validation Guidance; ICH M10",\n        "major_players": ["Labcorp Central Laboratory Services", "Q² Solutions (IQVIA)", "Eurofins Central Laboratory", "Frontage Laboratories"],\n        "sources": [\n            "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312",\n        ],\n    },\n    {\n        "id": "partner-3pl",\n        "name": "Third-Party Logistics (3PL) & Cold-Chain Specialty Couriers",\n        "stages": ["distribution"],\n        "plain_summary": "Temperature-controlled warehouses and specialized medical couriers that store finished medicines after they leave the factory and ship them safely—even at ultra-cold temperatures—to wholesalers and clinics.",\n        "technical_scope": "Title and non-title pharmaceutical warehousing, order-to-cash processing, DSCSA EPCIS serialization aggregation, and qualified 2–8°C, -20°C/-80°C, and cryogenic LN2 cell/gene therapy logistics.",\n        "regulatory_framework": "Drug Supply Chain Security Act (DSCSA); Good Distribution Practice (GDP); 21 CFR Part 205",\n        "major_players": ["ICS (Cencora)", "Cardinal Health 3PL Services", "McKesson RxCrossroads", "Marken (UPS Healthcare)", "Cryoport"],\n        "sources": [\n            "https://www.fda.gov/media/77516/download",\n            "https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring",\n        ],\n    },\n    {\n        "id": "partner-wholesaler",\n        "name": "Full-Line Pharmaceutical Wholesalers",\n        "stages": ["distribution", "commercial"],\n        "plain_summary": "Massive national distributors that buy medicines in bulk from hundreds of manufacturers and deliver daily restocks to local retail pharmacies and hospitals.",\n        "technical_scope": "High-volume inventory consolidation, daily next-day replenishment to retail chains and health systems, DSCSA Authorized Trading Partner verification, and hospital/GPO contract chargeback administration.",\n        "regulatory_framework": "DSCSA Authorized Trading Partner (ATP) licensure; 21 CFR Part 205 (Wholesale Prescription Drug Distributors)",\n        "major_players": ["McKesson", "Cencora (formerly AmerisourceBergen)", "Cardinal Health"],\n        "sources": [\n            "https://www.fda.gov/media/77516/download",\n        ],\n    },\n    {\n        "id": "partner-specialty-rems",\n        "name": "Specialty Pharmacies & REMS / Patient Support Hubs",\n        "stages": ["commercial", "distribution"],\n        "plain_summary": "Dedicated pharmacies and support centers that handle complex, high-cost, or closely monitored medicines—helping with insurance approvals, cold-chain home delivery, and mandatory FDA safety checks.",\n        "technical_scope": "Limited-distribution network (LDN) dispensing for biologics, oncology, and rare diseases; benefit verification & prior authorization hubs; nurse adherence coaching; and mandatory FDA REMS prescriber/patient registry enforcement.",\n        "regulatory_framework": "FDA Risk Evaluation and Mitigation Strategies (REMS, FD&C Act § 505-1); State Boards of Pharmacy; HIPAA",\n        "major_players": ["CVS Specialty", "Accredo (Express Scripts)", "Optum Specialty Pharmacy", "Biologics by McKesson", "CareMetx / Sonexus (Hubs)"],\n        "sources": [\n            "https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring",\n        ],\n    },\n]\n\n\ndef build_partners(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    out_path = data_dir / "partners.json"\n    payload = {\n        "checked": CHECKED,\n        "count": len(PARTNER_CATEGORIES),\n        "scope_note": "Describes the functional execution ecosystem that operates alongside Sponsors and CDMOs (#/ref/vendors). Naming major industry operators is for educational orientation only and is not an endorsement.",\n        "categories": PARTNER_CATEGORIES,\n    }\n    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {"partner_categories": len(PARTNER_CATEGORIES)}\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_partners(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
PARTNERS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nexport async function partnersPage(query) {\n  const doc = await getJSON("data/partners.json");\n  const cats = doc.categories || [];\n  const stage = (query && query.get("stage")) || "";\n  const filtered = cats.filter((c) => !stage || (c.stages || []).includes(stage));\n  return {\n    title: "Pharma Execution Partner Ecosystem (CROs, Labs, 3PLs & Specialty)",\n    body: html`\n      <h1>Pharma Execution Partner Ecosystem</h1>\n      <p class="lead">Drug sponsors rarely execute every stage alone. Alongside <a href="#/ref/vendors">CDMOs &amp; Manufacturing Facilities</a>, six specialized partner sectors run preclinical toxicology, global clinical trials, central labs, cold-chain logistics, wholesale replenishment, and specialty/REMS dispensing (${filtered.length} of ${cats.length} shown; checked ${doc.checked}).</p>\n      <p class="small">Filter by stage:\n        <a href="#/ref/partners">All</a> ·\n        <a href="#/ref/partners?stage=discovery">Discovery</a> ·\n        <a href="#/ref/partners?stage=analytical">Analytical</a> ·\n        <a href="#/ref/partners?stage=clinical">Clinical Trials</a> ·\n        <a href="#/ref/partners?stage=commercial">Commercial</a> ·\n        <a href="#/ref/partners?stage=distribution">Distribution</a>\n      </p>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharmaceutical execution partner ecosystem">\n        <table class="tbl"><thead><tr>\n          <th>Partner Sector</th><th>Lifecycle Stages</th><th>Technical Scope &amp; Regulation</th><th>Major Industry Operators</th>\n        </tr></thead>\n        <tbody>${filtered.map((c) => html`<tr id="${c.id}">\n          <td><b>${c.name}</b><br><span class="muted small">${c.plain_summary}</span></td>\n          <td>${(c.stages || []).map((st) => html`<a href="#/ref/departments/${st}">${st}</a>`).join(", ")}</td>\n          <td>${c.technical_scope}<br><span class="muted small"><b>Standards:</b> ${c.regulatory_framework}</span></td>\n          <td>${(c.major_players || []).join(", ")}</td>\n        </tr>`)}</tbody></table>\n      </div>\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/vendors">Manufacturers &amp; CDMOs (FDA/EMA Audits)</a> · <a href="#/ref/software">Software Stack</a> · <a href="#/ref/economics">Drug Economics</a>.</p>\n    `,\n  };\n}\n\nexport async function partnersExplorePage() {\n  const doc = await getJSON("data/partners.json");\n  const cats = doc.categories || [];\n  return {\n    title: "Who Builds, Tests & Delivers a Medicine",\n    body: html`\n      <h1>Who Builds, Tests &amp; Delivers a Medicine</h1>\n      <p class="lead">Bringing a medicine from a lab bench to a local pharmacy takes an entire relay team of specialized companies—from clinical trial organizers and central blood-testing labs to cold-chain shippers and specialty pharmacies.</p>\n      <ol>${cats.map((c) => html`<li><b>${c.name}:</b> ${c.plain_summary}</li>`)}</ol>\n      <p class="muted small">Want the full technical &amp; regulatory breakdown? <a href="#/ref/partners">Open Reference Partner Ecosystem</a> · <a href="#/explore/how-drugs-are-built">Back to 8-Stage Lifecycle</a>.</p>\n    `,\n  };\n}\n'


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
        if anchor in txt:
            rep = (
                'if (path === "/ref/partners") return partnersPage(query);\n'
                '  if (path === "/explore/partners") return partnersExplorePage();\n'
                '  ' + anchor
            )
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
    hook = "\n# v6.0k: Pharma Execution Partner Ecosystem (CROs, Labs, 3PLs, Wholesalers, Specialty/REMS)\npython3 pipeline/build_partners.py site/data\n"
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
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV = [\n  ["#/ref/economics", "Drug economics"],\n];\n', encoding="utf-8")
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
        assert out["partner_categories"] == 6, out

        doc = json.loads((root / "site" / "data" / "partners.json").read_text(encoding="utf-8"))
        for c in doc["categories"]:
            assert c["sources"] and all(u.startswith("https://") for u in c["sources"]), c

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
