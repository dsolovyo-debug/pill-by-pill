#!/usr/bin/env python3
"""Pill by Pill v6.1q Patch: Pharmaceutical Supply Chain, Serialization (DSCSA), Cold Chain & Quality Agreements Reference (#/ref/supply-chain, #/explore/supply-chain, /api/supply-chain).

1. Adds `pipeline/build_supply_chain.py` -> `site/data/supply_chain.json` (6 DSCSA serialization &
   traceability pillars, 6 cold chain / GDP / excursion pillars, 6 quality agreements & supplier
   qualification pillars, and 6 drug shortages & resilience pillars — 24 primary-sourced entries).
2. Adds `site/js/supply_chain.js` (`supplyChainPage` with inline Manufacturer-to-Patient Supply
   Chain & Serialization SVG + 4 section filters) and wires `#/ref/supply-chain`,
   `#/explore/supply-chain`, `/api/supply-chain`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `supply_chain.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/supply-chain/` static SEO page + sitemap entry -> 33
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1q_supply_chain_dscsa_cold_chain_patch.py --selftest
  python3 2026-11-23_v6.1q_supply_chain_dscsa_cold_chain_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_SUPPLY_CHAIN_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1q Pharmaceutical Supply Chain, DSCSA, Cold Chain & Quality Agreements Reference (`site/data/supply_chain.json`).

Comprehensive, primary-sourced reference covering:
  1. DSCSA Serialization & Electronic Track-and-Trace (6 pillars)
  2. Cold Chain, Good Distribution Practice (GDP) & Excursion Control (6 pillars)
  3. Quality Agreements & Supplier / CDMO Qualification (6 pillars)
  4. Drug Shortages, Section 506C & Supply Chain Resilience (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA, WHO).

Usage:
  python3 pipeline/build_supply_chain.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

DSCSA_SERIALIZATION = [
    {
        "id": "sc-dscsa-overview",
        "name": "Drug Supply Chain Security Act (DSCSA) — Electronic Package Tracing",
        "pillar": "Track & Trace",
        "plain": "Every prescription medicine bottle or carton carries a scannable 2D barcode with a unique serial number so wholesalers and pharmacies can verify it came from the real manufacturer.",
        "technical": "Title II of the Drug Quality and Security Act (2013) mandates interoperable, electronic package-level tracing across manufacturers, repackagers, wholesale distributors, and dispensers using GS1 EPCIS transaction data.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-integrity/drug-supply-chain-security-act-dscsa",
    },
    {
        "id": "sc-product-identifier",
        "name": "2D DataMatrix Product Identifier (GTIN, Serial, Lot, Expiry)",
        "pillar": "Serialization",
        "plain": "A tiny square barcode on each package encodes four facts—the product's NDC/GTIN, a unique serial number, the batch/lot code, and the expiration date.",
        "technical": "FD&C Act § 582 requires a standardized numerical identifier (NDC + unique serial number), lot number, and expiration date in both human-readable text and a machine-readable 2D DataMatrix barcode on each homogeneous case and salable unit.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/fdas-implementation-drug-supply-chain-security-act-dscsa-requirements",
    },
    {
        "id": "sc-atp",
        "name": "Authorized Trading Partners (ATPs) & Licensing Verification",
        "pillar": "Partner Eligibility",
        "plain": "Drugmakers, distributors, and pharmacies are legally allowed to buy and sell prescription medicines only with other licensed, verified trading partners.",
        "technical": "Under DSCSA, manufacturers, wholesalers, 3PLs, repackagers, and dispensers must verify that every trading partner holds valid FDA registration or state licensure before transferring product ownership.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/drug-supply-chain-security-act-law-and-policies",
    },
    {
        "id": "sc-suspect-illegitimate",
        "name": "Suspect & Illegitimate Product Quarantine and 24-Hour Notification",
        "pillar": "Counterfeit Defense",
        "plain": "If a distributor or pharmacy spots a tampered seal, wrong barcode, or suspicious package, they must lock it in quarantine and alert FDA and trading partners within 24 hours.",
        "technical": "Trading partners must quarantine suspect product, investigate, and—upon determining a product is illegitimate (counterfeit, diverted, stolen, or adulterated)—notify FDA (Form 3911) and immediate trading partners within 24 hours.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products",
    },
    {
        "id": "sc-salable-returns",
        "name": "Verification Router Service (VRS) & Salable Returns",
        "pillar": "Returns Verification",
        "plain": "Before a wholesaler can resell an unopened medicine bottle returned by a pharmacy, it pings the manufacturer's database in milliseconds to confirm the serial number is genuine.",
        "technical": "DSCSA requires wholesale distributors to verify the product identifier of returned salable units with the manufacturer prior to redistribution, typically via interoperable VRS lookup networks.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/drug-supply-chain-security-act-product-tracing-requirements-frequently-asked-questions",
    },
    {
        "id": "sc-dispensers",
        "name": "Hospital & Retail Pharmacy (Dispenser) Verification Duties",
        "pillar": "Last-Mile Check",
        "plain": "Pharmacists check incoming electronic tracing records and confirm lot/serial numbers match before dispensing medicines to patients.",
        "technical": "Dispensers must capture and store Transaction Information (TI) and Transaction Statements (TS) for 6 years, verify ATP status, and maintain systems to respond to recall/suspect-product requests.",
        "url": "https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/pharmacists-utilize-dscsa-requirements-protect-your-patients",
    },
]

COLD_CHAIN_GDP = [
    {
        "id": "gdp-who-standards",
        "name": "WHO Good Storage & Distribution Practices (GSP / GDP)",
        "pillar": "Global Baseline",
        "plain": "Good Distribution Practice ensures medicines stay safe, uncontaminated, and at the right temperature all the way from the factory loading dock to the pharmacy shelf.",
        "technical": "WHO Technical Report Series quality assurance standards governing warehouse mapping, FEFO (First Expiry / First Out) rotation, quarantine controls, recalls, and anti-falsification chain-of-custody.",
        "url": "https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs957-annex5-who-good-distribution-practices-for-pharmaceutical-products.pdf",
    },
    {
        "id": "gdp-thermal-zones",
        "name": "Pharmaceutical Thermal Bands (CRT, 2–8 °C, -20 °C, -70 °C)",
        "pillar": "Storage Regimes",
        "plain": "Different medicines need wildly different climates—from Controlled Room Temperature pills (20–25 °C) to refrigerated biologics (2–8 °C) and ultra-cold mRNA vaccines (-70 °C).",
        "technical": "Active refrigerated containers, phase-change passive shippers, and dry-ice/cryogenic dewars are qualified against worst-case summer/winter ambient lane profiles (e.g., ISTA 7D/7E) to prevent freezing of 2–8 °C biologics.",
        "url": "https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs961-annex9-supp12.pdf",
    },
    {
        "id": "gdp-excursions",
        "name": "Temperature Excursion Management & Mean Kinetic Temperature",
        "pillar": "Deviation Disposition",
        "plain": "If a truck's cooler warms up during a flight delay, quality engineers check electronic temperature loggers against stability data before deciding whether the batch is still safe or must be scrapped.",
        "technical": "Continuous calibrated data loggers record excursion duration and peak/minimum temperatures; QA disposition evaluates ICH Q1A/Q1E stability excursion budgets and freeze-thaw limits before release or rejection.",
        "url": "https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs961-annex9-supp12.pdf",
    },
    {
        "id": "gdp-lane-mapping",
        "name": "Warehouse Thermal Mapping & Transport Lane Qualification",
        "pillar": "Infrastructure Qualification",
        "plain": "Before storing or shipping temperature-sensitive drugs, companies place dozens of sensors inside warehouses and shipping routes to find hot spots near loading doors or cold spots near vents.",
        "technical": "Seasonal (summer/winter) 3D temperature/humidity mapping of warehouses, cold rooms, and air/road freight lanes establishes worst-case monitoring probe locations and qualified hold times.",
        "url": "https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs961-annex9-supp12.pdf",
    },
    {
        "id": "gdp-fefo-quarantine",
        "name": "FEFO Stock Rotation, Physical Quarantine & Recall Readiness",
        "pillar": "Inventory Control",
        "plain": "Warehouses ship older-expiring lots first (FEFO) and physically or electronically lock down unapproved, returned, or recalled pallets so they can never be shipped by mistake.",
        "technical": "Validated WMS/ERP inventory controls enforce First Expiry / First Out (FEFO) picking, segregated quarantine status pending QC release or investigation, and mock-recall traceability drills.",
        "url": "https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs957-annex5-who-good-distribution-practices-for-pharmaceutical-products.pdf",
    },
    {
        "id": "gdp-3pl-customs",
        "name": "3PLs, Customs Clearance & Tarmac Hold Mitigation",
        "pillar": "Logistics Risk",
        "plain": "International biologics shipments face their biggest temperature risk sitting on airport tarmacs or waiting in customs—requiring pre-cleared paperwork and priority cold-room handoffs.",
        "technical": "Requires GDP-audited Third-Party Logistics (3PL) providers, real-time IoT cellular/GPS telemetry, pre-arrival customs brokerage, and contingency dry-ice replenishment SOPs.",
        "url": "https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/distribution/trs961-annex9-supp12.pdf",
    },
]

QUALITY_AGREEMENTS = [
    {
        "id": "qa-fda-guidance",
        "name": "FDA Quality Agreements for Contract Manufacturing (Nov 2016)",
        "pillar": "Owner vs. CDMO",
        "plain": "When a drug company hires a contract factory (CDMO) to make or test a medicine, a Quality Agreement spells out in writing who is responsible for every safety check—and it must stay separate from business pricing contracts.",
        "technical": "FDA Final Guidance (Contract Manufacturing Arrangements for Drugs: Quality Agreements) recommends a written Quality Agreement—distinct or severable from MSAs/commercial terms—defining cGMP responsibilities under 21 CFR 210/211, 600–680, 820, and 1271.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contract-manufacturing-arrangements-drugs-quality-agreements-guidance-industry",
    },
    {
        "id": "qa-owner-liability",
        "name": "Ultimate Owner Quality Unit Responsibility (21 CFR 211.22)",
        "pillar": "Non-Delegable Duty",
        "plain": "A drug owner cannot outsource legal responsibility for quality: even if a contract lab makes a mistake, FDA holds both the contractor and the drug owner accountable.",
        "technical": "Under FD&C Act § 501(a)(2)(B) and 21 CFR 211.22(a), the owner's Quality Unit remains ultimately responsible for approving or rejecting batches manufactured by contract facilities, while contractors remain independently liable for cGMP compliance.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contract-manufacturing-arrangements-drugs-quality-agreements-guidance-industry",
    },
    {
        "id": "qa-change-control",
        "name": "Change Control, Deviations, CAPA & Field Alert Reports",
        "pillar": "Communication Clocks",
        "plain": "Quality Agreements set strict clocks—often 24 to 72 hours—for a contract factory to tell the drug owner if a batch fails a test, equipment breaks down, or a recall might be needed.",
        "technical": "Defines notification timelines and approval authority for major/minor process changes, OOS/deviation investigations, CAPAs, NDA Field Alert Reports (FARs), Biological Product Deviation Reports (BPDRs), and recalls.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contract-manufacturing-arrangements-drugs-quality-agreements-guidance-industry",
    },
    {
        "id": "qa-supplier-audit",
        "name": "API, Excipient & Primary Packaging Supplier Qualification",
        "pillar": "Upstream Controls",
        "plain": "Before buying raw active ingredients, glass vials, or excipients, drugmakers audit those suppliers and test incoming deliveries so contaminated materials never enter the factory.",
        "technical": "Applies ICH Q7 (APIs) and 21 CFR 211.84 incoming component testing: risk-ranked supplier audits, Certificate of Analysis (CoA) verification, identity testing on every container/lot, and nitrosamine/elemental-impurity supply-chain risk assessments.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contract-manufacturing-arrangements-drugs-quality-agreements-guidance-industry",
    },
    {
        "id": "qa-subcontracting",
        "name": "Subcontractor & Analytical Testing Lab Flow-Downs",
        "pillar": "Tier-2 Visibility",
        "plain": "A contract manufacturer cannot quietly hand work off to a third-party lab or sterilizer without the drug owner's written approval and audit.",
        "technical": "Quality Agreements prohibit unapproved subcontracting of testing, sterilization, packaging, or labeling operations and mandate flow-down of cGMP, data integrity (21 CFR Part 11), and record-retention obligations.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contract-manufacturing-arrangements-drugs-quality-agreements-guidance-industry",
    },
    {
        "id": "qa-tech-transfer",
        "name": "Technology Transfer & Comparability Protocols",
        "pillar": "Site-to-Site Move",
        "plain": "Moving a medicine's recipe from one factory to another requires side-by-side batch testing to prove the new site makes the exact same product.",
        "technical": "Structured transfer of Critical Process Parameters (CPPs), analytical methods (ICH Q2), and PPQ/comparability data (ICH Q10) across sending and receiving sites prior to regulatory CBE-30 / PAS supplement filing.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contract-manufacturing-arrangements-drugs-quality-agreements-guidance-industry",
    },
]

SHORTAGES_RESILIENCE = [
    {
        "id": "sr-506c-notify",
        "name": "Section 506C Mandatory Drug Shortage Notification",
        "pillar": "Early Warning",
        "plain": "By law, drugmakers must warn FDA at least 6 months ahead—or within 5 business days of an unexpected breakdown—if a manufacturing problem could cause a US medicine shortage.",
        "technical": "FD&C Act § 506C (21 U.S.C. 356c) requires manufacturers of covered prescription drugs/biologics to notify FDA of permanent discontinuances or temporary interruptions likely to cause a meaningful supply disruption.",
        "url": "https://www.fda.gov/drugs/drug-shortages/drug-shortages-non-compliance-notification-requirement",
    },
    {
        "id": "sr-cares-rmp",
        "name": "CARES Act Supply Chain Redundancy Risk Management Plans (RMPs)",
        "pillar": "Proactive Resilience",
        "plain": "After pandemic supply shocks, federal law required makers of essential drugs and APIs to maintain written backup plans—identifying weak links before a factory outage hits patients.",
        "technical": "CARES Act (2020) amended FD&C Act § 506C(j), requiring manufacturers of essential drugs, APIs, and associated preparation/administration devices to develop, maintain, and implement redundancy Risk Management Plans (May 2022 FDA Draft Guidance).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-management-plans-mitigate-potential-drug-shortages",
    },
    {
        "id": "sr-mitigation",
        "name": "FDA Drug Shortage Mitigation Toolkit (Expedited Reviews & Enforcement)",
        "pillar": "Crisis Response",
        "plain": "When a critical medicine runs low, FDA can fast-track approval of a backup factory, extend safe expiration dates after testing, or temporarily allow imports from trusted foreign plants.",
        "technical": "FDA Drug Shortage Staff coordinates expedited review of manufacturing supplements/ANDAs, prioritized cGMP inspections, stability-supported shelf-life extensions, and temporary controlled importation under regulatory discretion.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/7-things-know-about-drug-shortage-management",
    },
    {
        "id": "sr-dual-sourcing",
        "name": "Dual-Sourcing, Buffer Stock & Geographic Concentration Risk",
        "pillar": "Network Design",
        "plain": "Relying on a single chemical plant in one country for a key ingredient creates fragility; qualifying two independent factories and holding safety stock protects hospitals.",
        "technical": "Reduces single-point-of-failure exposure across KSMs (Key Starting Materials), APIs, sterile fill-finish lines, and primary glass/elastomer components via qualified secondary suppliers and strategic safety-stock buffers.",
        "url": "https://www.fda.gov/drugs/drug-shortages/coronavirus-aid-relief-and-economic-security-act-cares-act-drug-shortage-mitigation-efforts",
    },
    {
        "id": "sr-sterile-injectables",
        "name": "Why Sterile Generic Injectables Face the Highest Shortage Risk",
        "pillar": "Economic & cGMP Drivers",
        "plain": "Low-margin generic hospital IV drugs are especially vulnerable to shortages because sterile factories are expensive to maintain and any quality shutdown removes huge market share overnight.",
        "technical": "FDA Drug Shortages Reports highlight that older sterile injectables experience disproportionate disruptions driven by thin pricing margins, limited spare aseptic fill-finish capacity, and cGMP remediation delays.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/7-things-know-about-drug-shortage-management",
    },
    {
        "id": "sr-quality-maturity",
        "name": "Quality Management Maturity (QMM) & Predictive Supply Health",
        "pillar": "Beyond Baseline cGMP",
        "plain": "Rather than only checking whether a factory passes minimum rules on inspection day, QMM measures whether a site continuously invests in modern equipment and prevents shortages before they happen.",
        "technical": "FDA CDER Quality Management Maturity framework evaluates leadership, business continuity, advanced pharmaceutical quality systems (ICH Q10), and supply-chain reliability beyond baseline 21 CFR 211 compliance.",
        "url": "https://www.fda.gov/drugs/drug-shortages/coronavirus-aid-relief-and-economic-security-act-cares-act-drug-shortage-mitigation-efforts",
    },
]


def build_supply_chain(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "dscsa_serialization": len(DSCSA_SERIALIZATION),
            "cold_chain_gdp": len(COLD_CHAIN_GDP),
            "quality_agreements": len(QUALITY_AGREEMENTS),
            "shortages_resilience": len(SHORTAGES_RESILIENCE),
        },
        "dscsa_serialization": DSCSA_SERIALIZATION,
        "cold_chain_gdp": COLD_CHAIN_GDP,
        "quality_agreements": QUALITY_AGREEMENTS,
        "shortages_resilience": SHORTAGES_RESILIENCE,
    }
    (data_dir / "supply_chain.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_supply_chain.py <site/data>")
    print(json.dumps(build_supply_chain(pathlib.Path(sys.argv[1])), indent=2))
'''

SUPPLY_CHAIN_JS = '''// Pill by Pill v6.1q: Pharmaceutical Supply Chain, Serialization (DSCSA), Cold Chain & Quality Agreements Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["dscsa", "DSCSA Serialization", "dscsa_serialization"],
  ["gdp", "Cold Chain & GDP", "cold_chain_gdp"],
  ["quality", "Quality Agreements", "quality_agreements"],
  ["shortages", "Shortages & Resilience", "shortages_resilience"],
];

function supplyChainSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Serialized and temperature-controlled pharmaceutical supply chain flow">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. API &amp; CDMO</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Quality Agreements</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">21 CFR 211 / ICH Q7</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sc-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. 2D Serialization</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">GTIN + Serial + Lot + Exp</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">DSCSA EPCIS Exchange</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sc-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Cold Chain &amp; 3PL</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">WHO GDP / 2–8 °C / -70 °C</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">VRS Returns Verification</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sc-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Patient Access</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Dispenser Check &amp; FEFO</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">§ 506C / CARES RMPs</text>
      <defs><marker id="sc-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">End-to-end pharmaceutical distribution pairs DSCSA electronic package tracing with GDP cold-chain control and § 506C shortage resilience.</figcaption>
  </figure>`;
}

export async function supplyChainPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/supply_chain.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/supply-chain" : "#/ref/supply-chain";

  const pills = html`<div class="chips" role="navigation" aria-label="Supply chain sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Control / Standard</th><th>Pillar</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.pillar}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${supplyChainSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA DSCSA, Contract Manufacturing Quality Agreements, § 506C/CARES Act, and WHO GDP standards.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Supply Chain & Cold Chain"]] : [REF_HOME, ["Supply Chain & Cold Chain"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Pharmaceutical Supply Chain, DSCSA, Cold Chain & Quality Agreements",
      lede: env === "explore"
        ? "How medicines are barcoded, kept cold on trucks and planes, and protected from counterfeits and factory shortages."
        : "DSCSA electronic serialization, WHO GDP cold-chain controls, CDMO Quality Agreements, and § 506C/CARES Act shortage resilience.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on supply chain and serialization.", href: env === "explore" ? "#/ref/supply-chain" : "#/explore/supply-chain" },
        { title: "Sterile Manufacturing & Bioprocessing", text: "Cleanrooms, Annex 1 CCS, aseptic fill-finish, and validation.", href: "#/ref/sterile" },
        { title: "Manufacturers, CDMOs & Site Audits", text: "Inspect real facility FDA Form 483 and recall histories.", href: "#/ref/vendors" },
      ],
    }),
  };
}
'''


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
    if 'supply_chain.js' not in txt:
        for anchor in ('import * as rwe from "./rwe.js";\n', 'import * as diagnostics from "./diagnostics.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as supplyChain from "./supply_chain.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as supplyChain from "./supply_chain.js";\n' + txt
            changed = True
    if '"/ref/supply-chain"' not in txt:
        for anchor in ('if (path === "/ref/rwe")', 'if (path === "/ref/diagnostics")', 'if (path === "/ref/global-reg")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/supply-chain") return { env: "ref", current: "#/ref/supply-chain", ...(await supplyChain.supplyChainPage(query, "ref")) };\n  if (path === "/explore/supply-chain") return { env: "explore", current: "#/explore/supply-chain", ...(await supplyChain.supplyChainPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/supply-chain" not in txt:
        for anchor in ('["#/ref/rwe", "Real-World Evidence"]', '["#/ref/diagnostics", "Diagnostics & CDx"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/supply-chain", "Supply chain & DSCSA"]', 1)
                changed = True
                break
    if "#/explore/supply-chain" not in txt:
        for anchor in ('["#/explore/rwe", "Real-World Evidence"]', '["#/explore/diagnostics", "Diagnostics & CDx"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/supply-chain", "Supply chain & DSCSA"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_supply_chain.py" in txt:
        return False
    line = "python3 pipeline/build_supply_chain.py site/data\n"
    if "build_global_search.py" in txt:
        txt = txt.replace("python3 pipeline/build_global_search.py", line + "python3 pipeline/build_global_search.py", 1)
    else:
        txt = txt + ("" if txt.endswith("\n") else "\n") + line
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/supply-chain"' in txt:
        return False
    route = (
        '\n@app.get("/api/supply-chain")\n'
        'def api_supply_chain():\n'
        '    p = DATA_DIR / "supply_chain.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "supply_chain.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"supply_chain.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    sc_ref = _load(data_dir / "supply_chain.json", {}) or {}\n'
        '    for sec_key, sec_q in [("dscsa_serialization", "dscsa"), ("cold_chain_gdp", "gdp"), ("quality_agreements", "quality"), ("shortages_resilience", "shortages")]:\n'
        '        for item in (sc_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "supply_chain",\n'
        '                "group": "Supply Chain & DSCSA",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/supply-chain?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/supply-chain?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"supply chain DSCSA serialization 2D DataMatrix EPCIS cold chain GDP quality agreement CDMO shortage 506C CARES {sec_key} {item.get(\'name\', \'\')} {item.get(\'pillar\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"supply-chain", "#/ref/supply-chain"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    sc_doc = _load_json(data_dir / "supply_chain.json")\n'
        '    if isinstance(sc_doc, dict) and sc_doc.get("dscsa_serialization"):\n'
        '        sc_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (sc_doc.get("dscsa_serialization") or []) + (sc_doc.get("cold_chain_gdp") or []))\n'
        '        pages.append(("supply-chain", "#/ref/supply-chain", "Pharmaceutical Supply Chain, DSCSA, Cold Chain & Quality Agreements",\n'
        '                      "Primary-sourced guide to DSCSA electronic serialization, WHO GDP cold-chain distribution, CDMO Quality Agreements, and § 506C drug shortage resilience.",\n'
        '                      f"<ul>{sc_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/supply-chain"' in txt:
        return False
    for anchor in ('    "/#/explore/rwe",', '    "/#/explore/diagnostics",', '    "/#/explore/global-reg",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/supply-chain",\n    "/#/explore/supply-chain",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_supply_chain_py": _write_if_changed(pipe_dir / "build_supply_chain.py", BUILD_SUPPLY_CHAIN_PY),
        "supply_chain_js": _write_if_changed(js_dir / "supply_chain.js", SUPPLY_CHAIN_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/rwe") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/rwe", "Real-World Evidence"]] }];\nconst EXPLORE_NAV = [["#/explore/rwe", "Real-World Evidence"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/rwe",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_supply_chain.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_supply_chain.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"dscsa_serialization": 6, "cold_chain_gdp": 6, "quality_agreements": 6, "shortages_resilience": 6}, out

        doc = json.loads((root / "site" / "data" / "supply_chain.json").read_text(encoding="utf-8"))
        for k in ("dscsa_serialization", "cold_chain_gdp", "quality_agreements", "shortages_resilience"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "supply_chain.js").read_text(encoding="utf-8")
        print("V61Q_SUPPLY_CHAIN_DSCSA_COLD_CHAIN_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1q Supply Chain, DSCSA, Cold Chain & Quality Agreements patch.")
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
