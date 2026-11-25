#!/usr/bin/env python3
"""Pill by Pill v6.0j Patch: Enterprise Pharma Software Stack (10 Categories) & Drug Development Economics / Capital Formation / Gross-to-Net Waterfall.

Closes Gap A (regulated enterprise software parallel to the 18 hardware classes) and Gap B
(end-to-end drug development economics, capital formation, CBO/JAMA R&D benchmarks, and
Gross-to-Net payer waterfall):
  1. Adds `pipeline/build_software_and_economics.py` -> `site/data/software_stack.json` & `site/data/economics.json`.
  2. Adds `site/js/economics.js` (`softwareStackPage`, `economicsPage`, `economicsExplorePage`) with inline GTN SVG.
  3. Wires `#/ref/software`, `#/ref/economics`, and `#/explore/economics` into `site/js/app.js` and `site/js/layout.js`.
  4. Hooks `build_software_and_economics.py` into `pipeline/run_all.sh` and adds `/api/software` + `/api/economics` to `app.py`.
  5. Adds static SEO landing pages (`/software/`, `/economics/`, `/how-drugs-are-funded/`) in `pipeline/build_v60_static_pages.py`.

Usage:
  python3 2026-11-21_v6.0j_pharma_software_and_economics_patch.py --selftest
  python3 2026-11-21_v6.0j_pharma_software_and_economics_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_SW_ECON_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.0j Enterprise Pharma Software Stack & Drug Development Economics datasets.\n\nWrites:\n  - `site/data/software_stack.json` (10 regulated enterprise software categories across all 8 stages)\n  - `site/data/economics.json` (Capital Formation lifecycle, CBO/JAMA R&D benchmarks, Gross-to-Net waterfall)\n\nAll figures and regulatory references are strictly primary-sourced (FDA, eCFR, CBO, CMS, PMC).\nZero fabricated pricing or financial forecasts.\n\nUsage:\n  python3 pipeline/build_software_and_economics.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-21"\n\nSOFTWARE_STACK = [\n    {\n        "id": "sw-eln",\n        "name": "Electronic Lab Notebook (ELN)",\n        "stages": ["discovery", "formulation"],\n        "plain_summary": "Digital science notebooks where chemists and biologists record experiments, chemical recipes, and observations with permanent time stamps.",\n        "technical_spec": "Replaces paper lab notebooks with searchable, version-controlled experiment records, chemical structure registration, assay templates, and witnessed electronic signatures.",\n        "compliance": "21 CFR Part 11 (Electronic Records & Signatures); ALCOA+ data integrity",\n        "leading_vendors": ["Benchling", "Revvity Signals (PerkinElmer)", "Dotmatics", "LabWare"],\n        "sources": ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11"],\n    },\n    {\n        "id": "sw-lims",\n        "name": "Laboratory Information Management System (LIMS)",\n        "stages": ["analytical", "manufacturing"],\n        "plain_summary": "Tracks every physical sample tube, stability vial, and quality-control test result from the moment a sample arrives in the lab until a batch is approved for release.",\n        "technical_spec": "Manages sample accessioning, chain of custody, specification limits, stability pull schedules, out-of-specification (OOS) workflows, and automated Certificates of Analysis (CoA).",\n        "compliance": "21 CFR Part 211; 21 CFR Part 11; ICH Q2 / Q1A stability tracking",\n        "leading_vendors": ["LabWare", "Thermo Fisher SampleManager", "STARLIMS", "LabVantage"],\n        "sources": [\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11",\n        ],\n    },\n    {\n        "id": "sw-cds",\n        "name": "Chromatography Data System (CDS)",\n        "stages": ["analytical"],\n        "plain_summary": "Controls HPLC and UPLC lab instruments directly and locks every purity chromatogram into a tamper-evident audit trail so results cannot be cherry-picked.",\n        "technical_spec": "Direct instrument control, raw signal acquisition, peak integration, impurity quantitation, and immutable audit trails preventing unlogged re-integration.",\n        "compliance": "21 CFR Part 11; FDA Data Integrity and Compliance With Drug CGMP Guidance",\n        "leading_vendors": ["Waters Empower", "Agilent OpenLab CDS", "Thermo Fisher Chromeleon"],\n        "sources": ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11"],\n    },\n    {\n        "id": "sw-edc",\n        "name": "Electronic Data Capture (EDC)",\n        "stages": ["clinical"],\n        "plain_summary": "The secure system hospital nurses and doctors use to enter patient measurements, lab values, and side effects during Phase 1–3 clinical trials.",\n        "technical_spec": "Electronic Case Report Forms (eCRFs), automated edit checks, query management, medical coding (MedDRA/WHODrug), and database lock for biostatistical analysis.",\n        "compliance": "21 CFR Part 11; 21 CFR Part 312; ICH E6 Good Clinical Practice (GCP)",\n        "leading_vendors": ["Medidata Rave (Dassault Systèmes)", "Veeva Vault EDC", "Oracle Clinical One"],\n        "sources": [\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312",\n            "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n        ],\n    },\n    {\n        "id": "sw-ctms-etmf",\n        "name": "CTMS & Electronic Trial Master File (eTMF)",\n        "stages": ["clinical"],\n        "plain_summary": "Manages clinical trial budgets, hospital site activations, and the official inspection-ready archive of ethics approvals and consent forms.",\n        "technical_spec": "Clinical Trial Management Systems (CTMS) track site enrollment, monitoring visits, and investigator payments; eTMF maintains the DIA Reference Model archive required for FDA/EMA GCP inspections.",\n        "compliance": "21 CFR Part 312; ICH E6(R2)/E6(R3) GCP Essential Documents",\n        "leading_vendors": ["Veeva Vault Clinical", "Medidata", "IQVIA", "Oracle"],\n        "sources": ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312"],\n    },\n    {\n        "id": "sw-rim-ectd",\n        "name": "Regulatory Information Management (RIM) & eCTD Publishing",\n        "stages": ["regulatory"],\n        "plain_summary": "Assembles thousands of lab, factory, and clinical documents into the exact digital format required by the FDA, EMA, and PMDA and tracks every global approval commitment.",\n        "technical_spec": "Compiles, validates, and publishes ICH M4 electronic Common Technical Document (eCTD) Modules 1–5 for IND, NDA, BLA, ANDA, and MAA filings, plus global registration and labeling tracking.",\n        "compliance": "21 CFR Part 314; FDA eCTD Technical Conformance Guide; ICH M4",\n        "leading_vendors": ["Veeva Vault RIM", "LORENZ docuBridge", "IQVIA RIM Smart", "EXTEDO"],\n        "sources": ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314"],\n    },\n    {\n        "id": "sw-qms",\n        "name": "Quality Management System (QMS)",\n        "stages": ["analytical", "manufacturing", "regulatory"],\n        "plain_summary": "Tracks factory deviations, root-cause investigations, corrective actions, and standard operating procedures (SOPs) to keep medicine manufacturing compliant.",\n        "technical_spec": "Manages CAPA (Corrective and Preventive Action), deviations, change control, supplier quality audits, training records, and controlled SOP lifecycle.",\n        "compliance": "21 CFR Part 211; ICH Q10 Pharmaceutical Quality System",\n        "leading_vendors": ["Veeva Vault QMS", "MasterControl", "Honeywell TrackWise Digital"],\n        "sources": ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211"],\n    },\n    {\n        "id": "sw-mes",\n        "name": "Manufacturing Execution System (MES) & Electronic Batch Records (eBR)",\n        "stages": ["manufacturing"],\n        "plain_summary": "Guides factory operators step-by-step on the cleanroom floor, verifying raw material barcodes, weights, and machine settings in real time.",\n        "technical_spec": "Enforces master batch recipes, automated weigh-and-dispense, equipment status verification, and review-by-exception Electronic Batch Records (eBR).",\n        "compliance": "21 CFR Part 211 Subpart J (Records and Reports); 21 CFR Part 11",\n        "leading_vendors": ["Rockwell Automation PharmaSuite", "Körber Werum PAS-X", "Siemens Opcenter", "Emerson Syncade"],\n        "sources": ["https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211"],\n    },\n    {\n        "id": "sw-pv",\n        "name": "Pharmacovigilance & Drug Safety Database",\n        "stages": ["clinical", "distribution"],\n        "plain_summary": "Collects and analyzes side-effect reports from doctors, patients, and clinical trials worldwide so companies and regulators can spot safety signals early.",\n        "technical_spec": "Individual Case Safety Report (ICSR) intake, MedDRA coding, aggregate periodic safety reports (PSUR/PBRER), signal detection, and automated ICH E2B(R3) transmission to FDA AEMS/FAERS and EMA EudraVigilance.",\n        "compliance": "21 CFR 314.80 (Postmarketing Reporting of Adverse Drug Experiences); ICH E2B(R3)",\n        "leading_vendors": ["Oracle Argus Safety", "Veeva Vault Safety", "ArisGlobal LifeSphere Safety"],\n        "sources": [\n            "https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring",\n            "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n        ],\n    },\n    {\n        "id": "sw-dscsa",\n        "name": "DSCSA Serialization & Cold-Chain Track-and-Trace",\n        "stages": ["distribution"],\n        "plain_summary": "Assigns a unique serial number to every prescription bottle or carton and logs its handoffs and temperature from factory to pharmacy to block counterfeits.",\n        "technical_spec": "Unit-level 2D DataMatrix serialization (GTIN, serial number, lot, expiry), GS1 EPCIS electronic transaction exchange across trading partners, and real-time thermal excursion telemetry.",\n        "compliance": "Drug Supply Chain Security Act (DSCSA); FDA Verification & Interoperability Requirements",\n        "leading_vendors": ["TraceLink", "SAP ATTP", "Antares Vision (rfxcel)"],\n        "sources": ["https://www.fda.gov/media/77516/download"],\n    },\n]\n\nECONOMICS_DATA = {\n    "checked": CHECKED,\n    "scope_note": "All economic benchmarks below cite published government (CBO, CMS) or peer-reviewed (JAMA/PMC) sources. Pill by Pill does not fabricate proprietary drug-level R&D or net-price figures.",\n    "capital_formation": [\n        {\n            "stage": "1. Basic Science & Target Discovery",\n            "primary_funders": "Public grants (NIH, NSF), university endowments, and disease foundations",\n            "plain": "Governments and charities fund most early biology—figuring out which protein or gene drives a disease—years before a company ever forms.",\n            "technical": "Non-dilutive foundational biomedical research (NIH R01/U01, academic tech transfer) de-risks target biology and generates foundational IP licensed into startups or pharma.",\n        },\n        {\n            "stage": "2. Preclinical & IND-Enabling",\n            "primary_funders": "Biotech Venture Capital (Seed / Series A), SBIR/STTR grants, angel syndicates",\n            "plain": "Venture capital investors fund small biotech startups to turn a lab discovery into a drug candidate and run the animal safety tests needed to enter human trials.",\n            "technical": "Dilutive private equity funds lead optimization, GLP toxicology, and initial cGMP batch manufacture to reach IND clearance.",\n        },\n        {\n            "stage": "3. Phase 1–2 Clinical Proof-of-Concept",\n            "primary_funders": "Series B/C Venture Capital, Biotech IPOs, Big Pharma licensing & option deals",\n            "plain": "Human trials cost tens to hundreds of millions of dollars. Biotechs raise larger VC rounds, go public on stock exchanges, or partner with large pharma companies.",\n            "technical": "Cross-over rounds, Nasdaq IPOs, and strategic collaborations (upfront payments + clinical/regulatory milestones + tiered royalties) fund Phase 1/2 proof-of-concept.",\n        },\n        {\n            "stage": "4. Phase 3 Pivotal, Launch & Lifecycle",\n            "primary_funders": "Large Biopharma operating cash flow, M&A acquisitions, follow-on public equity",\n            "plain": "Global Phase 3 trials and worldwide commercial launches are usually funded by established pharmaceutical companies—or by acquiring the biotech that discovered the drug.",\n            "technical": "Large-scale multicenter RCTs, commercial scale-up/PPQ, global HTA/payer access teams, and post-marketing commitments are financed via commercial P&L or M&A.",\n        },\n    ],\n    "rd_benchmarks": [\n        {\n            "study": "Congressional Budget Office (CBO, 2021) — Research and Development in the Pharmaceutical Industry",\n            "metric": "Under $1B to over $2B capitalized per new approved drug (range across published studies)",\n            "key_drivers": "Clinical trial execution, high Phase 2 attrition (cost of failed candidates), and the multi-year time cost of capital.",\n            "url": "https://www.cbo.gov/publication/57025",\n        },\n        {\n            "study": "Wouters, McKee & Luyten (2020, JAMA) — Estimated Research and Development Investment Needed to Bring a New Medicine to Market, 2009–2018",\n            "metric": "Median $985.3M (mean $1,335.9M) capitalized R&D investment across 63 new therapeutic agents",\n            "key_drivers": "Varies widely by therapeutic area (e.g., oncology and immunomodulators vs. nervous system and infectious disease).",\n            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7054832/",\n        },\n    ],\n    "gross_to_net_waterfall": [\n        {"step": "1. Wholesale Acquisition Cost (WAC)", "role": "Published list price set by the manufacturer before any discounts or rebates."},\n        {"step": "2. Wholesaler Distribution & Prompt-Pay Fees", "role": "Fees paid to 3PLs and national wholesalers (e.g., McKesson, Cencora, Cardinal Health) for logistics and inventory."},\n        {"step": "3. Commercial PBM Formulary Rebates", "role": "Negotiated rebates paid to Pharmacy Benefit Managers (PBMs) and insurers for preferred formulary placement."},\n        {"step": "4. Statutory Government Discounts", "role": "Mandatory discounts under Medicaid Best Price, the 340B Drug Pricing Program, VA/DoD, and CMS Medicare Drug Price Negotiation."},\n        {"step": "5. Patient Copay Support & Chargebacks", "role": "Manufacturer copay assistance (commercial plans only) and hospital/clinic contract chargebacks."},\n        {"step": "6. Manufacturer Net Revenue -> Loss of Exclusivity (LOE)", "role": "Actual revenue retained by the sponsor to fund operations and next-generation R&D until patent/exclusivity expiry triggers generic or biosimilar entry."},\n    ],\n    "sources": [\n        {"label": "CBO (2021) — Research and Development in the Pharmaceutical Industry", "url": "https://www.cbo.gov/publication/57025"},\n        {"label": "Wouters et al. (2020), JAMA — PMC7054832", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7054832/"},\n        {"label": "CMS — Medicare Drug Price Negotiation Program", "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program"},\n    ],\n}\n\n\ndef build_software_and_economics(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    sw_path = data_dir / "software_stack.json"\n    ec_path = data_dir / "economics.json"\n    sw_payload = {"checked": CHECKED, "count": len(SOFTWARE_STACK), "items": SOFTWARE_STACK}\n    sw_path.write_text(json.dumps(sw_payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    ec_path.write_text(json.dumps(ECONOMICS_DATA, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "software_categories": len(SOFTWARE_STACK),\n        "capital_stages": len(ECONOMICS_DATA["capital_formation"]),\n        "rd_benchmarks": len(ECONOMICS_DATA["rd_benchmarks"]),\n        "gtn_steps": len(ECONOMICS_DATA["gross_to_net_waterfall"]),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_software_and_economics(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
ECONOMICS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderGrossToNetSvg() {\n  const steps = [\n    { x: 10, label: "WAC List", sub: "100% List" },\n    { x: 140, label: "Wholesalers", sub: "Logistics Fees" },\n    { x: 270, label: "PBM Rebates", sub: "Formulary" },\n    { x: 400, label: "Gov Discounts", sub: "340B / CMS" },\n    { x: 530, label: "Net Revenue", sub: "Funds R&D" },\n  ];\n  return html`<figure class="gtn-map" aria-label="Pharmaceutical Gross-to-Net revenue waterfall">\n    <svg viewBox="0 0 660 84" width="660" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${steps.map((s, i) => html`\n        <rect x="${s.x}" y="10" width="118" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 4 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 4 ? "2" : "1.5"}"/>\n        <text x="${s.x + 59}" y="35" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">${s.label}</text>\n        <text x="${s.x + 59}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${s.sub}</text>\n        ${i < steps.length - 1 ? html`<line x1="${s.x + 118}" y1="41" x2="${s.x + 130}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Conceptual Gross-to-Net flow from published list price (WAC) to net manufacturer revenue.</figcaption>\n  </figure>`;\n}\n\nexport async function softwareStackPage(query) {\n  const doc = await getJSON("data/software_stack.json");\n  const items = doc.items || [];\n  const stage = (query && query.get("stage")) || "";\n  const q = ((query && query.get("q")) || "").trim().toLowerCase();\n  const filtered = items.filter((it) => {\n    if (stage && !(it.stages || []).includes(stage)) return false;\n    if (q && !(`${it.name} ${it.plain_summary} ${it.technical_spec} ${(it.leading_vendors || []).join(" ")}`.toLowerCase().includes(q))) return false;\n    return true;\n  });\n  return {\n    title: "Pharma Software & Informatics Stack",\n    body: html`\n      <h1>Enterprise Pharma Software &amp; Informatics Stack</h1>\n      <p class="lead">Regulated digital systems that run modern drug discovery, clinical trials, regulatory submissions, cGMP manufacturing, and supply-chain serialization (${filtered.length} of ${items.length} categories shown; checked ${doc.checked}).</p>\n      <p class="small">Filter by stage:\n        <a href="#/ref/software">All</a> ·\n        <a href="#/ref/software?stage=discovery">Discovery</a> ·\n        <a href="#/ref/software?stage=analytical">Analytical QC</a> ·\n        <a href="#/ref/software?stage=clinical">Clinical Trials</a> ·\n        <a href="#/ref/software?stage=regulatory">Regulatory</a> ·\n        <a href="#/ref/software?stage=manufacturing">Manufacturing</a> ·\n        <a href="#/ref/software?stage=distribution">Distribution</a>\n      </p>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharmaceutical software stack">\n        <table class="tbl"><thead><tr>\n          <th>System Category</th><th>Lifecycle Stages</th><th>Technical Scope &amp; Compliance</th><th>Leading Platforms</th>\n        </tr></thead>\n        <tbody>${filtered.map((s) => html`<tr id="${s.id}">\n          <td><b>${s.name}</b><br><span class="muted small">${s.plain_summary}</span></td>\n          <td>${(s.stages || []).map((st) => html`<a href="#/ref/departments/${st}">${st}</a>`).join(", ")}</td>\n          <td>${s.technical_spec}<br><span class="muted small"><b>Standards:</b> ${s.compliance}</span></td>\n          <td>${(s.leading_vendors || []).join(", ")}</td>\n        </tr>`)}</tbody></table>\n      </div>\n      <p class="muted small">See also: <a href="#/ref/equipment">18 Physical Lab &amp; Factory Hardware Classes</a> · <a href="#/ref/departments">8-Stage Drug Lifecycle Encyclopedia</a>.</p>\n    `,\n  };\n}\n\nexport async function economicsPage() {\n  const ec = await getJSON("data/economics.json");\n  return {\n    title: "Drug Development Economics & Capital Formation",\n    body: html`\n      <h1>Drug Development Economics, Capital Formation &amp; Pricing</h1>\n      <p class="lead">How biomedical innovation is financed from NIH grants to commercial launch, what published studies show about R&amp;D costs, and how Gross-to-Net payer economics work.</p>\n      <h2>1. Who Pays at Each Stage (Capital Formation)</h2>\n      <div class="tbl-wrap" tabindex="0" role="region" aria-label="Capital formation by stage">\n        <table class="tbl"><thead><tr><th>Lifecycle Stage</th><th>Primary Funders</th><th>Economic Mechanism</th></tr></thead>\n        <tbody>${(ec.capital_formation || []).map((c) => html`<tr>\n          <td><b>${c.stage}</b></td>\n          <td>${c.primary_funders}</td>\n          <td>${c.technical}</td>\n        </tr>`)}</tbody></table>\n      </div>\n      <h2>2. Published R&amp;D Cost &amp; Attrition Benchmarks</h2>\n      <ul class="plain">${(ec.rd_benchmarks || []).map((b) => html`<li>\n        <b>${b.study}</b> — ${b.metric}. <span class="muted">${b.key_drivers}</span>\n        (<a href="${b.url}" target="_blank" rel="noopener">Primary source</a>)\n      </li>`)}</ul>\n      <h2>3. Commercial Gross-to-Net (GTN) Waterfall</h2>\n      ${renderGrossToNetSvg()}\n      <ol>${(ec.gross_to_net_waterfall || []).map((g) => html`<li><b>${g.step}:</b> ${g.role}</li>`)}</ol>\n      <p class="muted small">${ec.scope_note} (Checked ${ec.checked}).</p>\n    `,\n  };\n}\n\nexport async function economicsExplorePage() {\n  const ec = await getJSON("data/economics.json");\n  return {\n    title: "How New Medicines Are Funded & Priced",\n    body: html`\n      <h1>How New Medicines Are Funded &amp; Priced</h1>\n      <p class="lead">Developing a new medicine takes years of lab work, human trials, and factory checks. Here is who pays for each step and why a medicine\'s list price is different from what insurers actually pay.</p>\n      <h2>Who Pays Along the Way</h2>\n      <ol>${(ec.capital_formation || []).map((c) => html`<li><b>${c.stage}</b> (${c.primary_funders}): ${c.plain}</li>`)}</ol>\n      <h2>From List Price to Net Revenue</h2>\n      ${renderGrossToNetSvg()}\n      <ol>${(ec.gross_to_net_waterfall || []).map((g) => html`<li><b>${g.step}:</b> ${g.role}</li>`)}</ol>\n      <p class="muted small">Want the full technical details? <a href="#/ref/economics">Open Reference Economics</a> · <a href="#/explore/how-drugs-are-built">Back to 8-Stage Lifecycle</a>.</p>\n    `,\n  };\n}\n'


def _patch_app_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    imp = 'import { softwareStackPage, economicsPage, economicsExplorePage } from "./economics.js";\n'
    if "./economics.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/software"' not in txt and "#/ref/software" not in txt:
        anchor = 'if (path === "/ref/equipment")'
        rep = (
            'if (path === "/ref/software") return softwareStackPage(query);\n'
            '  if (path === "/ref/economics") return economicsPage();\n'
            '  if (path === "/explore/economics") return economicsExplorePage();\n'
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
    if "#/ref/software" in txt:
        return False
    anchor = '["#/ref/equipment", "Equipment market"]'
    if anchor in txt:
        rep = (
            '["#/ref/equipment", "Equipment market"],\n'
            '  ["#/ref/software", "Software stack"],\n'
            '  ["#/ref/economics", "Drug economics"]'
        )
        path.write_text(txt.replace(anchor, rep, 1), encoding="utf-8")
        return True
    return False


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_software_and_economics.py" in txt:
        return False
    hook = "\n# v6.0j: Enterprise Pharma Software Stack & Drug Development Economics\npython3 pipeline/build_software_and_economics.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/software"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/software")\n'
        'def api_software():\n'
        '    return _read_json(SITE_DIR / "data" / "software_stack.json")\n\n'
        '@app.get("/api/economics")\n'
        'def api_economics():\n'
        '    return _read_json(SITE_DIR / "data" / "economics.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    pipe_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)

    fp_py = pipe_dir / "build_software_and_economics.py"
    py_written = (not fp_py.is_file()) or (fp_py.read_text(encoding="utf-8") != BUILD_SW_ECON_PY)
    if py_written:
        fp_py.write_text(BUILD_SW_ECON_PY, encoding="utf-8")

    fp_js = js_dir / "economics.js"
    js_written = (not fp_js.is_file()) or (fp_js.read_text(encoding="utf-8") != ECONOMICS_JS)
    if js_written:
        fp_js.write_text(ECONOMICS_JS, encoding="utf-8")

    return {
        "build_software_and_economics_py": py_written,
        "economics_js": js_written,
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/equipment") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV = [\n  ["#/ref/equipment", "Equipment market"],\n];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_software_and_economics.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_software_and_economics.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out["software_categories"] == 10 and out["capital_stages"] == 4 and out["gtn_steps"] == 6, out

        sw = json.loads((root / "site" / "data" / "software_stack.json").read_text(encoding="utf-8"))
        for it in sw["items"]:
            assert all(u.startswith("https://") for u in it["sources"]), it
        ec = json.loads((root / "site" / "data" / "economics.json").read_text(encoding="utf-8"))
        for b in ec["rd_benchmarks"]:
            assert b["url"].startswith("https://"), b

        print("V60J_SOFTWARE_STACK_AND_ECONOMICS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0j Software Stack & Drug Economics patch.")
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
