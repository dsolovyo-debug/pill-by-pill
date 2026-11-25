#!/usr/bin/env python3
"""Pill by Pill v6.1y Patch: Drug Shortages, Supply Chain Resilience & Essential Medicines Economics (#/ref/shortages, #/explore/shortages, /api/shortages).

1. Adds `pipeline/build_shortages.py` -> `site/data/shortages.json` (6 shortage root causes,
   6 FDA FDASIA/CARES Act mitigations, 6 resilience/QMM frameworks, and 6 essential-generic
   economic reforms — 24 primary-sourced entries anchored to FDA/eCFR/HHS ASPE/WHO/CMS).
2. Adds `site/js/shortages.js` (`shortagesPage` with inline Resilience SVG + 4 section filters)
   and wires `#/ref/shortages`, `#/explore/shortages`, `/api/shortages`, `REF_NAV_GROUPS`,
   `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `shortages.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/shortages/` static SEO page + sitemap -> 40 pages),
   and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1y_drug_shortages_supply_chain_resilience_patch.py --selftest
  python3 2026-11-24_v6.1y_drug_shortages_supply_chain_resilience_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_SHORTAGES_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1y Drug Shortages, Supply Chain Resilience & Essential Medicines Economics (`site/data/shortages.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Root Causes of Drug Shortages (6 drivers: Sterile Generic Price Compression, Manufacturing Quality & OAI Disruptions, Single-Source API & KSM Geographic Concentration, Sudden Demand Spikes & Off-Label Shifts, GPO Contracting & Failure-to-Supply Penalties, Natural Disasters & Logistics Bottlenecks)\n  2. FDA Shortage Authority & Regulatory Mitigations (6 tools: FDASIA 2012 Mandatory Notification, CARES Act 2020 Risk Management Plans, Expiration Date Extensions, Temporary Foreign Importation Discretion, Expedited Prior-Approval Supplements & ANDAs, FDA Drug Shortages Database & ASHP Tracking)\n  3. Supply Chain Resilience & Redundancy Engineering (6 strategies: Dual-Sourcing API & Fill-Finish Sites, Domestic Onshoring & Advanced Manufacturing, Strategic National Stockpile & Buffer Inventory, Quality Management Maturity QMM Program, Essential Medicines Lists EO 13944 / WHO EML, Real-Time Visibility & DSCSA Serialization)\n  4. Essential Generic Economics & Policy Reforms (6 mechanisms: Hospital Sterile Injectable Fragility, Non-Profit Generic Models e.g. Civica Rx, CMS Hospital Buffer-Stock Incentives, Quality-Tiered Purchasing & Reliability Scoring, Pediatric & Oncology Shortage Impacts, Global Essential Medicine Access)\n\nAll anchors are verified HTTPS primary sources (FDA, eCFR, HHS/ASPE, WHO, CMS, CBO).\n\nUsage:\n  python3 pipeline/build_shortages.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nROOT_CAUSES = [\n    {\n        "id": "sh-price-compression",\n        "name": "Sterile Generic Price Compression & \'Race to the Bottom\'",\n        "plain": "Old, life-saving hospital IV drugs (like basic chemotherapy or saline) often sell for a few dollars a vial—leaving razor-thin profits so companies stop investing in factory upgrades or exit the market altogether.",\n        "technical": "FDA\'s 2019 Drug Shortages Task Force Report identified lack of incentives to produce less-profitable older sterile injectables as the primary economic root cause of persistent U.S. shortages.",\n        "url": "https://www.fda.gov/drugs/drug-shortages/report-drug-shortages-root-causes-and-potential-solutions",\n    },\n    {\n        "id": "sh-quality-oai",\n        "name": "Manufacturing Quality Failures & Facility Shutdowns",\n        "plain": "Because sterile injectable factories run near 100% capacity with little spare room, a single sterility failure, glass-particulate recall, or FDA shutdown at one plant can trigger a nationwide hospital shortage overnight.",\n        "technical": "Over 60% of historical sterile injectable shortages stem from cGMP quality/remediation disruptions (Form 483/OAI/Warning Letters) where remaining manufacturers lack surge capacity.",\n        "url": "https://www.fda.gov/drugs/drug-shortages/report-drug-shortages-root-causes-and-potential-solutions",\n    },\n    {\n        "id": "sh-api-concentration",\n        "name": "Geographic Concentration of APIs & Key Starting Materials (KSMs)",\n        "plain": "Even when a pill is pressed in the U.S. or Europe, the raw chemical ingredients (APIs and starting chemicals) often come from just one or two factories overseas—creating single points of failure.",\n        "technical": "FDA CDER global facility tracking highlights heavy geographic concentration of small-molecule APIs and KSMs in India and China, exposing downstream finished-dosage manufacturers to geopolitical, trade, and single-site disruptions.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n    {\n        "id": "sh-demand-spikes",\n        "name": "Sudden Demand Surges & Device-Component Bottlenecks",\n        "plain": "When prescriptions for a medicine suddenly triple—such as pediatric respiratory seasons or GLP-1 autoinjector demand—factories cannot build new sterile pen-filling lines in a few months.",\n        "technical": "Multi-year lead times for ISO 5 aseptic fill-finish lines, glass cartridges, elastomer stoppers, and autoinjector sub-assemblies create rigid short-term supply ceilings.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n    {\n        "id": "sh-gpo-contracting",\n        "name": "Hospital GPO Contracting & Low-Price Procurement Incentives",\n        "plain": "Hospital buying groups (GPOs) historically rewarded whichever generic maker offered the absolute lowest price—without paying extra for backup factories, higher quality scores, or extra buffer stock.",\n        "technical": "HHS ASPE analyses note that sole-source or lowest-price GPO contracts with weak failure-to-supply penalties fail to price supply-chain reliability into generic purchasing.",\n        "url": "https://aspe.hhs.gov/reports/policy-considerations-prevent-drug-shortages",\n    },\n    {\n        "id": "sh-disasters",\n        "name": "Extreme Weather, Disasters & Cold-Chain Disruptions",\n        "plain": "Hurricanes hitting major IV-fluid hubs (like Puerto Rico or North Carolina) or port shutdowns can abruptly cut off basic hospital fluids and sterile injectables.",\n        "technical": "Single-region manufacturing clusters for high-volume parenterals (IV dextrose/saline/peritoneal dialysis) amplify vulnerability to severe weather and infrastructure outages.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n]\n\nFDA_MITIGATIONS = [\n    {\n        "id": "mit-fdasia",\n        "name": "FDASIA (2012) Mandatory Shortage & Discontinuance Notification",\n        "plain": "Requires manufacturers of life-supporting or life-sustaining medicines to warn the FDA at least 6 months before discontinuing a drug—or immediately when a factory disruption hits.",\n        "technical": "FD&C Act § 506C (21 CFR 314.81(b)(3)(iii)) mandates early reporting of permanent discontinuances or meaningful manufacturing interruptions, enabling FDA CDER Drug Shortage Staff to prevent hundreds of shortages annually.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "mit-cares-rmp",\n        "name": "CARES Act (2020) Supply-Chain Risk Management Plans (RMPs)",\n        "plain": "Expanded shortage rules so manufacturers must maintain formal backup plans for their factories and report annual production volumes to the FDA.",\n        "technical": "FD&C Act § 506C(j) and § 510(j)(3) require Risk Management Plans (RMPs) for essential/life-supporting drug facilities and annual drug-amount reporting to improve FDA supply visibility.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-management-plans-mitigate-potential-drug-shortages",\n    },\n    {\n        "id": "mit-expiry-ext",\n        "name": "Stability-Backed Expiration Date Extensions",\n        "plain": "During an acute shortage, FDA can review real-time stability data and authorize hospitals to safely use unopened vials beyond their printed expiration date instead of throwing away good medicine.",\n        "technical": "Manufacturer-submitted ICH Q1A stability data verified by FDA CDER allows lot-specific shelf-life extensions posted publicly on FDA\'s Drug Shortages portal.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n    {\n        "id": "mit-foreign-import",\n        "name": "Temporary Foreign Importation Enforcement Discretion",\n        "plain": "In severe emergencies (such as pediatric cancer chemotherapy shortages), FDA can temporarily allow vetted overseas versions approved in Europe, Canada, or Australia into U.S. hospitals.",\n        "technical": "Case-by-case FDA enforcement discretion following quality/labeling review of foreign-registered products (e.g., cisplatin/carboplatin) paired with Dear Healthcare Provider letters.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n    {\n        "id": "mit-expedited-pas",\n        "name": "Expedited ANDA & Prior-Approval Supplement (PAS) Reviews",\n        "plain": "FDA puts new generic applications, backup factory sites, and new raw-material suppliers at the front of the review line whenever a medicine is in shortage.",\n        "technical": "Priority GDUFA/PDUFA review for new manufacturing lines, alternate API Drug Master Files (DMFs), and site transfers to restore market supply rapidly.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n    {\n        "id": "mit-fda-database",\n        "name": "FDA Drug Shortages Database & 503B Compounding Relief",\n        "plain": "FDA\'s public Shortage List tells hospitals which NDCs are available—and legally unlocks temporary Section 503B bulk compounding until commercial supply recovers.",\n        "technical": "Maintained under FD&C Act § 506E; active listing temporarily lifts the \'essentially a copy\' restriction for § 503A/503B compounders (cross-linked to #/ref/otc).",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n]\n\nRESILIENCE_ENGINEERING = [\n    {\n        "id": "res-dual-source",\n        "name": "Dual-Sourcing API, Excipients & Sterile Fill-Finish Sites",\n        "plain": "Qualifying at least two independent factories in different regions so a fire, flood, or inspection hold at one plant never cuts off patients.",\n        "technical": "Requires parallel Drug Master File (DMF) qualification, ICH Q5E/SUPAC comparability testing, and ongoing minimum volume allocations to keep backup lines warm.",\n        "url": "https://www.fda.gov/drugs/drug-shortages/report-drug-shortages-root-causes-and-potential-solutions",\n    },\n    {\n        "id": "res-advanced-mfg",\n        "name": "Domestic Onshoring & Continuous / Modular Manufacturing",\n        "plain": "Modern compact continuous-flow reactors and modular cleanrooms take a fraction of the footprint and cost of legacy mega-factories, making domestic essential-medicine production more viable.",\n        "technical": "Supported by FDA\'s Emerging Technology Program (ETP) and ICH Q13 Continuous Manufacturing guidelines to improve yield, consistency, and rapid surge scaling.",\n        "url": "https://www.fda.gov/drugs/pharmaceutical-quality-resources/emerging-technology-program",\n    },\n    {\n        "id": "res-sns-buffers",\n        "name": "Strategic National Stockpile (SNS) & Hospital Buffer Inventory",\n        "plain": "Holding rotating emergency reserves of critical hospital injectables, antibiotics, and antidotes—replacing fragile \'just-in-time\' inventory with \'just-in-case\' buffers.",\n        "technical": "Vendor-managed inventory (VMI) rotation prevents buffer expiration while absorbing 60-to-90-day supply shocks across acute-care health systems.",\n        "url": "https://aspe.hhs.gov/reports/policy-considerations-prevent-drug-shortages",\n    },\n    {\n        "id": "res-qmm",\n        "name": "FDA Quality Management Maturity (QMM) Program",\n        "plain": "Historically, buyers only saw pass/fail FDA inspections—so they couldn\'t tell a bare-minimum factory from an ultra-reliable one. FDA\'s QMM program measures proactive quality culture.",\n        "technical": "CDER\'s Quality Management Maturity (QMM) initiative assesses sustainable cGMP practices, business continuity, and robust supply-chain risk controls beyond baseline 21 CFR 211 compliance.",\n        "url": "https://www.fda.gov/drugs/pharmaceutical-quality-resources/cder-quality-management-maturity",\n    },\n    {\n        "id": "res-essential-lists",\n        "name": "FDA Essential Medicines List (EO 13944) & WHO EML",\n        "plain": "Identifies the core shortlist of ~220+ acute-care U.S. essential medicines and ~500+ global WHO Essential Medicines that health systems must prioritize for supply security.",\n        "technical": "FDA\'s Essential Medicines, Medical Countermeasures, and Critical Inputs List prioritizes domestic resilience investments alongside the biennial WHO Model List of Essential Medicines.",\n        "url": "https://www.fda.gov/about-fda/reports/executive-order-13944-list-essential-medicines-medical-countermeasures-and-critical-inputs",\n    },\n    {\n        "id": "res-visibility",\n        "name": "End-to-End Supply Visibility & DSCSA Serialization Telemetry",\n        "plain": "Digital unit-level barcode tracking and wholesaler inventory analytics help spot regional stockouts weeks earlier instead of waiting for hospital pharmacists to sound the alarm.",\n        "technical": "Combines DSCSA EPCIS unit-level event data with upstream API/excipient bill-of-materials (BOM) mapping to detect multi-tier sub-supplier bottlenecks.",\n        "url": "https://www.fda.gov/media/77516/download",\n    },\n]\n\nECONOMICS_REFORM = [\n    {\n        "id": "erf-hospital-steriles",\n        "name": "Why Sterile Generic Injectables Are Most Vulnerable",\n        "plain": "Sterile IV drugs are expensive to manufacture (ISO 5 cleanrooms, media fills, 100% inspection) yet priced like commodities—creating the sharpest mismatch between manufacturing cost and reimbursement.",\n        "technical": "Hospital DRG bundled inpatient payments incentivize hospitals and GPOs to minimize generic injectable acquisition cost rather than reward redundant sterile capacity.",\n        "url": "https://aspe.hhs.gov/reports/policy-considerations-prevent-drug-shortages",\n    },\n    {\n        "id": "erf-nonprofit-generics",\n        "name": "Non-Profit & Hospital-Consortium Models (e.g., Civica Rx)",\n        "plain": "Groups of hospital systems banded together to form non-profit generic suppliers with long-term volume commitments and 6-month safety stock—removing the incentive to abandon low-margin drugs.",\n        "technical": "Long-term take-or-pay multi-year hospital contracts guarantee predictable demand and fund dual-sourced API/fill-finish redundancy for shortage-prone essential injectables.",\n        "url": "https://aspe.hhs.gov/reports/policy-considerations-prevent-drug-shortages",\n    },\n    {\n        "id": "erf-cms-buffer",\n        "name": "CMS Medicare Buffer-Stock & Resilient-Purchasing Proposals",\n        "plain": "Federal health policy proposals explore paying hospitals a small separate add-on under Medicare when they maintain emergency buffer stocks of essential generic medicines.",\n        "technical": "HHS/CMS policy frameworks evaluate separate IPPS/OPPS add-on payments tied to minimum 3–6 month essential-medicine buffer stocks and transparent manufacturer quality/reliability metrics.",\n        "url": "https://aspe.hhs.gov/reports/policy-considerations-prevent-drug-shortages",\n    },\n    {\n        "id": "erf-quality-purchasing",\n        "name": "Quality-Tiered Purchasing & Reliability Contracting",\n        "plain": "Shifts hospital procurement away from \'lowest price wins\' toward balanced scorecards that reward FDA inspection history, QMM scores, dual-sourcing, and on-time delivery.",\n        "technical": "Pairs multi-award GPO contracts (avoiding winner-take-all market exits) with objective manufacturer reliability and FDA OII inspection track records (#/ref/vendors).",\n        "url": "https://www.fda.gov/drugs/pharmaceutical-quality-resources/cder-quality-management-maturity",\n    },\n    {\n        "id": "erf-clinical-impact",\n        "name": "Clinical Impact on Oncology, Pediatrics & Emergency Care",\n        "plain": "When a generic chemotherapy drug like cisplatin or methotrexate goes into shortage, hospitals face agonizing rationing decisions, delayed surgeries, and higher medication-error risks from unfamiliar substitutes.",\n        "technical": "Clinical ethics frameworks and ASHP/FDA shortage mitigation protocols manage therapeutic substitution, dose rounding, and vial-sharing while guarding against unfamiliar-concentration dosing errors.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n    {\n        "id": "erf-global-essential",\n        "name": "Global Essential Medicines & Pooled Procurement",\n        "plain": "Internationally, agencies like UNICEF, PAHO, and the Global Fund pool demand across dozens of countries to guarantee steady, quality-assured supply of WHO Essential Medicines.",\n        "technical": "Multi-year pooled tenders paired with WHO Prequalification (PQ) stabilize global generic API manufacturing for vaccines, antiretrovirals, TB, and maternal-health injectables.",\n        "url": "https://www.who.int/groups/expert-committee-on-selection-and-use-of-essential-medicines/essential-medicines-lists",\n    },\n]\n\n\ndef build_shortages(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on drug shortage root causes, FDA FDASIA/CARES Act authorities, supply-chain resilience engineering, and essential generic economics (FDA, eCFR, HHS ASPE, WHO, CMS). Educational reference only.",\n        "root_causes": ROOT_CAUSES,\n        "fda_mitigations": FDA_MITIGATIONS,\n        "resilience_engineering": RESILIENCE_ENGINEERING,\n        "economics_reform": ECONOMICS_REFORM,\n    }\n    (data_dir / "shortages.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "root_causes": len(ROOT_CAUSES),\n        "fda_mitigations": len(FDA_MITIGATIONS),\n        "resilience_engineering": len(RESILIENCE_ENGINEERING),\n        "economics_reform": len(ECONOMICS_REFORM),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_shortages(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
SHORTAGES_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderShortagesSvg() {\n  const nodes = [\n    { x: 8, label: "1. Fragile Margin", sub: "Low-Price Generics" },\n    { x: 140, label: "2. Disruption", sub: "OAI / API / Surge" },\n    { x: 272, label: "3. Early Alert", sub: "FDASIA § 506C" },\n    { x: 404, label: "4. FDA Relief", sub: "PAS / Ext / 503B" },\n    { x: 536, label: "5. Resilience", sub: "QMM / Dual-Source" },\n  ];\n  return html`<figure class="shortages-flow" aria-label="Drug shortage cycle and supply-chain resilience architecture">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 4 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 4 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">How low-margin generic vulnerability turns into hospital shortages—and how FDA mitigations, QMM, and dual-sourcing build resilience.</figcaption>\n  </figure>`;\n}\n\nexport async function shortagesPage(query, mode = "ref") {\n  const doc = await getJSON("data/shortages.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/shortages" : "#/ref/shortages";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Drug Shortages, Supply Chain Resilience & Essential Medicines Economics",\n    body: html`\n      <h1>Drug Shortages, Supply Chain Resilience &amp; Essential Medicines</h1>\n      <p class="lead">${mode === "explore"\n        ? "Why everyday hospital medicines like basic chemotherapy, antibiotics, and IV fluids sometimes vanish from pharmacy shelves—and how regulators and health systems work to keep supply steady."\n        : "Primary-sourced reference covering 6 shortage root causes, 6 FDA FDASIA/CARES Act mitigation authorities, 6 supply-chain resilience & QMM frameworks, and 6 essential-generic economic reforms (checked " + doc.checked + ")."}</p>\n\n      ${renderShortagesSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=causes"${sec === "causes" ? \' aria-current="page"\' : ""}>Root Causes (6)</a> ·\n        <a href="${base}?section=mitigations"${sec === "mitigations" ? \' aria-current="page"\' : ""}>FDA Authorities (6)</a> ·\n        <a href="${base}?section=resilience"${sec === "resilience" ? \' aria-current="page"\' : ""}>Resilience &amp; QMM (6)</a> ·\n        <a href="${base}?section=reforms"${sec === "reforms" ? \' aria-current="page"\' : ""}>Generic Economics (6)</a>\n      </p>\n\n      ${show("causes") ? html`\n        <h2 id="causes">1. Root Causes of Drug Shortages (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Drug shortage root causes">\n          <table class="tbl"><thead><tr><th>Driver</th><th>${mode === "explore" ? "Why Shortages Happen" : "Economic & Manufacturing Mechanism"}</th></tr></thead>\n          <tbody>${(doc.root_causes || []).map((c) => html`<tr id="${c.id}">\n            <td><b><a href="${c.url}" target="_blank" rel="noopener">${c.name}</a></b></td>\n            <td>${mode === "explore" ? c.plain : html`${c.plain}<br><span class="muted small">${c.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("mitigations") ? html`\n        <h2 id="mitigations">2. FDA Shortage Authority &amp; Regulatory Mitigations (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="FDA shortage mitigations">\n          <table class="tbl"><thead><tr><th>Regulatory Tool</th><th>${mode === "explore" ? "How FDA Responds" : "Statutory Authority & Operational Relief"}</th></tr></thead>\n          <tbody>${(doc.fda_mitigations || []).map((m) => html`<tr id="${m.id}">\n            <td><b><a href="${m.url}" target="_blank" rel="noopener">${m.name}</a></b></td>\n            <td>${mode === "explore" ? m.plain : html`${m.plain}<br><span class="muted small">${m.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("resilience") ? html`\n        <h2 id="resilience">3. Supply Chain Resilience &amp; Redundancy Engineering (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Supply chain resilience engineering">\n          <table class="tbl"><thead><tr><th>Resilience Strategy</th><th>${mode === "explore" ? "How It Prevents Outages" : "Engineering, QMM & Visibility Standards"}</th></tr></thead>\n          <tbody>${(doc.resilience_engineering || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b></td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("reforms") ? html`\n        <h2 id="reforms">4. Essential Generic Economics &amp; Policy Reforms (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Essential generic economics and reforms">\n          <table class="tbl"><thead><tr><th>Economic Model / Reform</th><th>${mode === "explore" ? "How It Fixes the Market" : "Procurement, Contracting & Global Access"}</th></tr></thead>\n          <tbody>${(doc.economics_reform || []).map((e) => html`<tr id="${e.id}">\n            <td><b><a href="${e.url}" target="_blank" rel="noopener">${e.name}</a></b></td>\n            <td>${mode === "explore" ? e.plain : html`${e.plain}<br><span class="muted small">${e.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/vendors">FDA/EMA Facility Audits</a> · <a href="#/ref/sterile">Sterile Manufacturing</a> · <a href="#/ref/otc">503B Compounding &amp; Shortages</a> · <a href="#/ref/economics">Drug Economics</a>.</p>\n    `,\n  };\n}\n'


def _write_if_changed(path: pathlib.Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def _patch_app_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    imp = 'import { shortagesPage } from "./shortages.js";\n'
    if "./shortages.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/shortages"' not in txt:
        for anchor in ('if (path === "/ref/amr")', 'if (path === "/ref/history-laws")', 'if (path === "/ref/careers")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/shortages") return shortagesPage(query, "ref");\n'
                    '  if (path === "/explore/shortages") return shortagesPage(query, "explore");\n'
                    '  ' + anchor
                )
                txt = txt.replace(anchor, rep, 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_layout_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "#/ref/shortages" not in txt:
        for anchor in ('["#/ref/amr", "AMR & antibiotics"]', '["#/ref/partners", "Partner ecosystem"]', '["#/ref/vendors", "Manufacturers & CDMOs"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/shortages", "Drug shortages & supply"]', 1)
                changed = True
                break
    if "#/explore/shortages" not in txt:
        for anchor in ('["#/explore/amr", "AMR & antibiotics"]', '["#/explore/history-laws", "History & safety laws"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/shortages", "Drug shortages & supply"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_shortages.py" in txt:
        return False
    hook = "\n# v6.1y: Drug Shortages, Supply Chain Resilience & Essential Medicines Economics\npython3 pipeline/build_shortages.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/shortages"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/shortages")\n'
        'def api_shortages():\n'
        '    return _read_json(SITE_DIR / "data" / "shortages.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"shortages.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    sh_ref = _load(data_dir / "shortages.json", {}) or {}\n'
        '    for sec_key, sec_q in [("root_causes", "causes"), ("fda_mitigations", "mitigations"), ("resilience_engineering", "resilience"), ("economics_reform", "reforms")]:\n'
        '        for item in (sh_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "shortage",\n'
        '                "group": "Drug Shortages & Supply Resilience",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/shortages?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/shortages?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"drug shortage supply chain resilience QMM FDASIA CARES Act GPO essential medicines generic sterile {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"shortages", "#/ref/shortages"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    sh_doc = _load_json(data_dir / "shortages.json")\n'
        '    if isinstance(sh_doc, dict) and sh_doc.get("root_causes"):\n'
        '        sh_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (sh_doc.get("root_causes") or []) + (sh_doc.get("fda_mitigations") or []))\n'
        '        pages.append(("shortages", "#/ref/shortages", "Drug Shortages, Supply Chain Resilience & Essential Medicines",\n'
        '                      "Primary-sourced guide to drug shortage root causes, FDA FDASIA/CARES Act authorities, Quality Management Maturity (QMM), dual-sourcing, and essential generic economics.",\n'
        '                      f"<ul>{sh_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/shortages"' in txt:
        return False
    for anchor in ('    "/#/explore/amr",', '    "/#/explore/history-laws",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/shortages",\n    "/#/explore/shortages",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_shortages_py": _write_if_changed(pipe_dir / "build_shortages.py", BUILD_SHORTAGES_PY),
        "shortages_js": _write_if_changed(js_dir / "shortages.js", SHORTAGES_JS),
        "app_js_wired": _patch_app_js(js_dir / "app.js"),
        "layout_js_wired": _patch_layout_js(js_dir / "layout.js"),
        "run_all_sh_hooked": _patch_run_all(pipe_dir / "run_all.sh"),
        "app_py_api_added": _patch_app_py(root / "app.py"),
        "global_search_indexed": _patch_global_search(pipe_dir / "build_global_search.py"),
        "static_seo_added": _patch_static_pages(pipe_dir / "build_v60_static_pages.py"),
        "test_v60_site_updated": _patch_test_v60_site(root / "tests" / "test_v60_site.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data").mkdir(parents=True)
        (root / "tests").mkdir()

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/amr") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/amr", "AMR & antibiotics"]] }];\nconst EXPLORE_NAV = [["#/explore/amr", "AMR & antibiotics"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/amr",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_shortages.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_shortages.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"root_causes": 6, "fda_mitigations": 6, "resilience_engineering": 6, "economics_reform": 6}, out

        doc = json.loads((root / "site" / "data" / "shortages.json").read_text(encoding="utf-8"))
        for k in ("root_causes", "fda_mitigations", "resilience_engineering", "economics_reform"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61Y_DRUG_SHORTAGES_RESILIENCE_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1y Drug Shortages & Supply Chain Resilience patch.")
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
