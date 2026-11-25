#!/usr/bin/env python3
"""Pill by Pill v6.2d Patch: Drug Shortages, Supply Chain Resilience, Essential Medicines & Domestic Onshoring Reference (#/ref/shortages-resilience, #/explore/shortages-resilience, /api/shortages-resilience).

1. Adds `pipeline/build_shortages_resilience.py` -> `site/data/shortages_resilience.json` (6 Drug
   Shortages & FDASIA 506C pillars, 6 CARES Act RMPs & CDER QMM pillars, 6 EO 13944 / 14017
   Essential Medicines & Domestic Onshoring pillars, and 6 ASPR SNS & BARDA IBMSC pillars — 24
   primary-sourced entries).
2. Adds `site/js/shortages_resilience.js` (`shortagesResiliencePage` with inline Supply Resilience
   & Essential Medicines SVG + 4 section filters) and wires `#/ref/shortages-resilience`,
   `#/explore/shortages-resilience`, `/api/shortages-resilience`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `shortages_resilience.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/shortages-resilience/` static SEO page + sitemap entry ->
   46 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2d_drug_shortages_supply_resilience_essential_meds_patch.py --selftest
  python3 2026-11-24_v6.2d_drug_shortages_supply_resilience_essential_meds_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_SHORTAGES_RESILIENCE_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2d Drug Shortages, Supply Chain Resilience, Essential Medicines & Domestic Onshoring Reference (`site/data/shortages_resilience.json`).

Comprehensive, primary-sourced reference covering:
  1. Drug Shortages & FDASIA Section 506C Reporting (6 pillars)
  2. CARES Act Risk Management Plans (RMPs) & CDER QMM (6 pillars)
  3. EO 13944 / EO 14017 Essential Medicines & Domestic Onshoring (6 pillars)
  4. ASPR Strategic National Stockpile (SNS) & BARDA IBMSC (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER/OPQ, HHS ASPR, BARDA).

Usage:
  python3 pipeline/build_shortages_resilience.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

SHORTAGES_506C = [
    {
        "id": "shr-fda-shortages-portal",
        "name": "FDA Drug Shortages Database & Mitigation Portal",
        "category": "Live Shortage Tracking",
        "plain": "FDA maintains a public live database tracking prescription medicines in short supply, why they ran out, and when manufacturers expect shipments to resume.",
        "technical": "CDER's Drug Shortage Staff coordinates with NDA/ANDA/BLA holders to track current and resolved shortages, post alternative therapeutic options, and expedite regulatory reviews.",
        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",
    },
    {
        "id": "shr-shortages-faq",
        "name": "FDA Drug Shortages FAQ: Regulatory Flexibility & Importation",
        "category": "Mitigation Tools",
        "plain": "When a critical medicine runs dry, FDA can extend expiration dates based on stability data or allow temporary emergency imports from vetted foreign plants.",
        "technical": "FDA's shortage mitigation toolkit includes expedited ANDA/PAS reviews, stability-backed shelf-life extensions, temporary controlled importation under enforcement discretion, and inter-agency coordination.",
        "url": "https://www.fda.gov/drugs/drug-shortages/frequently-asked-questions-about-drug-shortages",
    },
    {
        "id": "shr-root-causes-2019",
        "name": "FDA Inter-Agency Drug Shortages Root Causes Report",
        "category": "Economic & Quality Drivers",
        "plain": "FDA found that most drug shortages aren't caused by factory breakdowns alone—rock-bottom generic prices leave little incentive to invest in backup lines or quality upgrades.",
        "technical": "FDA's Drug Shortages: Root Causes and Potential Solutions report identifies three core drivers: lack of incentives for less-profitable generics, market inability to recognize/reward quality maturity, and logistical/regulatory challenges.",
        "url": "https://www.fda.gov/media/132058/download",
    },
    {
        "id": "shr-compounding-shortage",
        "name": "503A / 503B Compounding During Official FDA Drug Shortages",
        "category": "Emergency Supply Bridge",
        "plain": "When a drug is officially listed as 'Currently in Shortage' on FDA's list, licensed outsourcing facilities can temporarily compound copies to keep hospitals supplied.",
        "technical": "Under FD&C Act § 503A and § 503B, compounders may produce essentially a copy of an approved drug only while it appears on FDA's Drug Shortages list in 'Currently in Shortage' status.",
        "url": "https://www.fda.gov/drugs/human-drug-compounding/compounding-when-drugs-are-fdas-drug-shortages-list",
    },
    {
        "id": "shr-fdasia-506c",
        "name": "FDASIA Section 506C Mandatory Early Notification (6 Months Ahead)",
        "category": "Statutory Reporting",
        "plain": "By law, drugmakers must warn FDA at least 6 months before discontinuing or interrupting a life-supporting, life-sustaining, or critical medicine.",
        "technical": "FD&C Act § 506C (enacted via FDASIA, expanded by CARES Act) requires manufacturers of covered drugs to notify FDA ≥6 months in advance—or as soon as practicable—of permanent discontinuances or meaningful supply interruptions.",
        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/guidance-notifying-fda-permanent-discontinuance-or-interruption-manufacturing-under-section-506c-fdc",
    },
    {
        "id": "shr-506c-noncompliance",
        "name": "Section 506C Non-Compliance Letters & Public Accountability",
        "category": "Enforcement",
        "plain": "If a manufacturer fails to warn FDA on time about a supply disruption, FDA sends an official non-compliance letter and posts it publicly.",
        "technical": "Under FD&C Act § 506C(f), FDA issues and publicly posts noncompliance letters to manufacturers that fail to submit timely discontinuance or interruption notifications within 30 days.",
        "url": "https://www.fda.gov/drugs/drug-shortages/drug-shortages-non-compliance-notification-requirement",
    },
]

CARES_RMP_QMM = [
    {
        "id": "shr-cares-mitigation",
        "name": "CARES Act Drug Shortage Mitigation & API Scope Expansion",
        "category": "CARES Act Mandate",
        "plain": "The 2020 CARES Act closed major blind spots by requiring shortage warnings for medical-device-linked drugs and for active ingredients—not just finished pills.",
        "technical": "The CARES Act amended FD&C Act § 506C and added § 506J and § 510(j)(3), extending shortage reporting to APIs, critical medical devices, and annual manufacturing volume disclosures.",
        "url": "https://www.fda.gov/drugs/drug-shortages/coronavirus-aid-relief-and-economic-security-act-cares-act-drug-shortage-mitigation-efforts",
    },
    {
        "id": "shr-rmp-guidance",
        "name": "Supply Chain Risk Management Plans (RMPs) — FD&C Act § 506C(j)",
        "category": "Proactive Continuity",
        "plain": "Makers of life-saving drugs and their active ingredients must maintain written disaster-playbook Risk Management Plans covering backup suppliers and inventory buffers.",
        "technical": "FDA's Risk Management Plans to Mitigate the Potential for Drug Shortages guidance implements CARES Act § 3112(b), requiring stakeholders for § 506C(a) drugs and APIs to maintain ICH Q9-aligned RMPs.",
        "url": "https://www.fda.gov/media/158487/download",
    },
    {
        "id": "shr-cares-volume-reporting",
        "name": "CARES Act Annual Drug & API Volume Reporting (§ 510(j)(3))",
        "category": "Supply Visibility",
        "plain": "Every registered pharmaceutical factory worldwide must now report how much of each drug or active ingredient it made for the U.S. market each year.",
        "technical": "FD&C Act § 510(j)(3) requires registrants to report annually the amount of each listed drug manufactured, prepared, propagated, compounded, or processed for commercial distribution.",
        "url": "https://www.fda.gov/drugs/drug-shortages/coronavirus-aid-relief-and-economic-security-act-cares-act-drug-shortage-mitigation-efforts",
    },
    {
        "id": "shr-cder-qmm",
        "name": "CDER Quality Management Maturity (QMM) Program",
        "category": "Quality Culture",
        "plain": "Meeting minimum GMP inspection rules isn't enough to prevent shortages—FDA's QMM program scores plants that invest in strong quality culture and proactive reliability.",
        "technical": "CDER's Quality Management Maturity (QMM) program evaluates manufacturing sites beyond baseline cGMP compliance across leadership commitment, business continuity, advanced PQS, and supply-chain resilience.",
        "url": "https://www.fda.gov/drugs/pharmaceutical-quality-resources/cder-quality-management-maturity",
    },
    {
        "id": "shr-quality-metrics",
        "name": "FDA Quality Metrics & Predictive Shortage Early Warning",
        "category": "Site KPIs",
        "plain": "Tracking factory KPIs like lot acceptance rates, invalidated lab results, and complaint rates helps spot fragile plants before a shortage hits patients.",
        "technical": "FDA's Quality Metrics for Drug Manufacturing initiative monitors objective site indicators (Lot Acceptance Rate, Invalidated OOS Rate, Product Quality Complaint Rate) to inform risk-based surveillance.",
        "url": "https://www.fda.gov/drugs/pharmaceutical-quality-resources/quality-metrics-drug-manufacturing",
    },
    {
        "id": "shr-economic-incentives",
        "name": "Group Purchasing Organizations (GPOs) & Quality-Linked Contracting",
        "category": "Market Reform",
        "plain": "FDA recommends that hospital buyers and insurers reward reliable, transparent factories instead of awarding winner-take-all contracts purely on the lowest penny price.",
        "technical": "FDA's Root Causes framework urges purchasers and GPOs to incorporate QMM ratings, multi-source redundancy, and reliable-supply commitments into contracting rather than pure price-driven tenders.",
        "url": "https://www.fda.gov/media/132058/download",
    },
]

ESSENTIAL_MEDS_ONSHORING = [
    {
        "id": "shr-eo-13944",
        "name": "Executive Order 13944 List of Essential Medicines & Critical Inputs",
        "category": "National Essential List",
        "plain": "FDA published an official list of the most medically necessary drugs, IV fluids, antibiotics, and raw chemical inputs that the U.S. must protect from foreign choke points.",
        "technical": "Under EO 13944, FDA identified 227 Essential Medicines and Medical Countermeasures plus 96 device/input categories clinically necessary for acute care, emergency readiness, and public health.",
        "url": "https://www.fda.gov/about-fda/reports/executive-order-13944-list-essential-medicines-medical-countermeasures-and-critical-inputs",
    },
    {
        "id": "shr-eo-14017-supply",
        "name": "Executive Order 14017 Pharmaceutical Supply Chain 100-Day Review",
        "category": "Federal Strategy",
        "plain": "A landmark White House and FDA review mapped how heavily U.S. antibiotics and generic pills depend on overseas API and starting-material factories.",
        "technical": "HHS/FDA's 100-Day Supply Chain Report under EO 14017 diagnosed single-point foreign concentration in Key Starting Materials (KSMs) and APIs and laid out onshoring and stockpiling pillars.",
        "url": "https://www.fda.gov/about-fda/reports/executive-order-14017-americas-supply-chains",
    },
    {
        "id": "shr-api-ksm-mapping",
        "name": "Geographic Concentration of APIs & Key Starting Materials (KSMs)",
        "category": "Upstream Risk",
        "plain": "Even when a pill is pressed in the U.S. or Europe, its underlying chemical building blocks often trace back to just one or two overseas chemical plants.",
        "technical": "FDA's EO 14017 assessment highlights multi-tier supply opacity where finished dosage forms rely on concentrated foreign API and KSM synthesis hubs vulnerable to export bans or disruptions.",
        "url": "https://www.fda.gov/about-fda/reports/executive-order-14017-americas-supply-chains",
    },
    {
        "id": "shr-critical-inputs-list",
        "name": "Critical Inputs, Excipients & Sterile Vial Component Security",
        "category": "Input Bottlenecks",
        "plain": "Shortages often happen not because of the drug itself, but because of missing borosilicate glass vials, rubber stoppers, sterile filters, or saline bags.",
        "technical": "EO 13944 and FDA supply reviews prioritize critical primary packaging, single-use bioprocessing consumables, and key excipients alongside APIs as essential supply-chain nodes.",
        "url": "https://www.fda.gov/about-fda/reports/executive-order-13944-list-essential-medicines-medical-countermeasures-and-critical-inputs",
    },
    {
        "id": "shr-onshoring-flexibility",
        "name": "Domestic Onshoring & Advanced Manufacturing Technology (AMT)",
        "category": "Reshoring & Tech",
        "plain": "To make U.S. chemical manufacturing cost-competitive, federal initiatives back continuous flow chemistry, modular factories, and automated sterile fill-finish.",
        "technical": "FDA CDER supports domestic onshoring through Advanced Manufacturing Technologies (AMT) designation, continuous manufacturing guidances, and expedited review of domestic site-transfer supplements.",
        "url": "https://www.fda.gov/drugs/pharmaceutical-quality-resources/cder-quality-management-maturity",
    },
    {
        "id": "shr-redundant-sourcing",
        "name": "Dual-Sourcing Qualification & Geographic Diversification",
        "category": "Redundancy Design",
        "plain": "Resilient pharma supply chains qualify at least two independent active-ingredient suppliers and two separate fill-finish sites in different regions.",
        "technical": "FDA's RMP and supply resilience frameworks emphasize pre-approved backup API/excipient suppliers, redundant fill-finish lines, and safety-stock buffers across geographically separated sites.",
        "url": "https://www.fda.gov/media/158487/download",
    },
]

ASPR_SNS_BARDA = [
    {
        "id": "shr-aspr-sns-center",
        "name": "HHS ASPR Center for the Strategic National Stockpile (SNS)",
        "category": "National Reserve",
        "plain": "The Strategic National Stockpile is America's federal emergency warehouse network of vaccines, antibiotics, antidotes, and ICU supplies ready to deploy within hours.",
        "technical": "Managed by HHS ASPR, the Strategic National Stockpile (SNS) maintains rapid-deployment medical countermeasures (MCMs), pharmaceuticals, and ancillaries to supplement state/local supplies during emergencies.",
        "url": "https://aspr.hhs.gov/SNS/Pages/default.aspx",
    },
    {
        "id": "shr-sns-products",
        "name": "SNS Formulary: Anthrax, Smallpox, Nerve Agent & Pandemic Stock",
        "category": "Stockpile Inventory",
        "plain": "The SNS holds specialized treatments most hospitals don't keep on hand—from botulism antitoxins and radiation antidotes to pandemic antivirals and ventilators.",
        "technical": "ASPR's SNS formulary spans CBRN medical countermeasures, broad-spectrum antibiotics, antivirals, burn/trauma supplies, and cold-chain distribution infrastructure coordinated with state health agencies.",
        "url": "https://www.aspr.gov/readiness-response/medical-countermeasures-biodefense/sns/stockpile-products",
    },
    {
        "id": "shr-barda-ibmsc",
        "name": "BARDA Industrial Base Management & Supply Chain (IBMSC)",
        "category": "Industrial Base",
        "plain": "BARDA's IBMSC division invests directly in U.S. pharmaceutical factories, glass vial lines, and domestic chemical precursors so critical drugs can be made at home.",
        "technical": "Within HHS ASPR, BARDA's Industrial Base Management and Supply Chain (IBMSC) executes public-private partnerships and DPA investments to expand domestic API, KSM, fill-finish, and ancillary capacity.",
        "url": "https://aspr.hhs.gov/AboutASPR/ProgramOffices/BARDA/Pages/Doing-Business-with-BARDA.aspx",
    },
    {
        "id": "shr-barda-domestic-mfg",
        "name": "BARDA Warm-Base Domestic Vaccine & Surge Manufacturing",
        "category": "Warm-Base Capacity",
        "plain": "Rather than building factories only after a crisis starts, BARDA pays to keep U.S. 'warm-base' facilities running year-round so they can pivot to surge production.",
        "technical": "BARDA's pandemic preparedness and Center for Industrial Base Expansion maintain domestic warm-base manufacturing networks for recombinant/mRNA vaccines, adjuvants, and sterile fill-finish surge capacity.",
        "url": "https://www.aspr.gov/about/centers/barda/bardas-pandemic-influenza-programs",
    },
    {
        "id": "shr-sns-vmi-rotation",
        "name": "Vendor-Managed Inventory (VMI) & Shelf-Life Extension (SLEP)",
        "category": "Stockpile Lifecycle",
        "plain": "To avoid wasting billions on expired pills, federal stockpiles rotate stock through commercial distributors and test lots under the Shelf-Life Extension Program.",
        "technical": "ASPR SNS leverages Vendor-Managed Inventory (VMI) rotation agreements and FDA/DoD Shelf-Life Extension Program (SLEP) stability testing to preserve readiness and minimize replacement waste.",
        "url": "https://aspr.hhs.gov/SNS/Pages/default.aspx",
    },
    {
        "id": "shr-mcm-surge-capacity",
        "name": "Defense Production Act (DPA) Priority Ratings & Surge Contracting",
        "category": "Emergency Powers",
        "plain": "During national health emergencies, HHS can invoke Defense Production Act priority ratings to move raw materials and bioreactor bags to the front of the line.",
        "technical": "Under the Defense Production Act (DPA) Title I and Title III authorities, ASPR/BARDA issues DX/DO priority-rated contracts and capital grants to secure domestic pharmaceutical inputs during crises.",
        "url": "https://aspr.hhs.gov/AboutASPR/ProgramOffices/BARDA/Pages/Doing-Business-with-BARDA.aspx",
    },
]


def build_shortages_resilience(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "shortages_506c": len(SHORTAGES_506C),
            "cares_rmp_qmm": len(CARES_RMP_QMM),
            "essential_meds_onshoring": len(ESSENTIAL_MEDS_ONSHORING),
            "aspr_sns_barda": len(ASPR_SNS_BARDA),
        },
        "shortages_506c": SHORTAGES_506C,
        "cares_rmp_qmm": CARES_RMP_QMM,
        "essential_meds_onshoring": ESSENTIAL_MEDS_ONSHORING,
        "aspr_sns_barda": ASPR_SNS_BARDA,
    }
    (data_dir / "shortages_resilience.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_shortages_resilience.py <site/data>")
    print(json.dumps(build_shortages_resilience(pathlib.Path(sys.argv[1])), indent=2))
'''

SHORTAGES_RESILIENCE_JS = '''// Pill by Pill v6.2d: Drug Shortages, Supply Chain Resilience, Essential Medicines & Domestic Onshoring Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["shortages", "Drug Shortages & 506C", "shortages_506c"],
  ["cares", "CARES RMPs & CDER QMM", "cares_rmp_qmm"],
  ["essential", "EO 13944 / 14017 & Onshoring", "essential_meds_onshoring"],
  ["stockpile", "ASPR SNS & BARDA IBMSC", "aspr_sns_barda"],
];

function shortagesResilienceSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Drug shortage mitigation and supply resilience: FDASIA 506C, CARES RMP and QMM, EO 13944/14017 Essential Medicines, and ASPR SNS and BARDA">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. FDASIA 506C</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">6-Mo Shortage Notice</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">503B &amp; Imports</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sr-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. CARES &amp; QMM</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">RMPs (§506C(j))</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">CDER Quality Maturity</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sr-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. EO 13944 / 14017</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Essential Meds &amp; KSMs</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Domestic Onshoring</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sr-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. ASPR &amp; BARDA</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">SNS Stockpile &amp; VMI</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">IBMSC Warm-Base</text>
      <defs><marker id="sr-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Pharmaceutical supply resilience integrates early 506C shortage alerts, CARES Act Risk Management Plans and QMM, EO 13944/14017 onshoring, and ASPR/BARDA stockpiling.</figcaption>
  </figure>`;
}

export async function shortagesResiliencePage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/shortages_resilience.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/shortages-resilience" : "#/ref/shortages-resilience";

  const pills = html`<div class="chips" role="navigation" aria-label="Drug shortages, supply resilience, and essential medicines sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Standard / Program</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.category}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${shortagesResilienceSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Drug Shortages (FDASIA 506C / CARES Act), CDER QMM, EO 13944 / 14017, and HHS ASPR SNS / BARDA IBMSC documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Drug Shortages, Supply Resilience & Essential Meds"]] : [REF_HOME, ["Drug Shortages, Supply Resilience & Essential Meds"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Drug Shortages, Supply Chain Resilience & Essential Medicines",
      lede: env === "explore"
        ? "Why medicines run short, how FDA and manufacturers prevent disruptions, and how federal stockpiles and domestic onshoring protect essential drugs."
        : "FDASIA § 506C shortage reporting, CARES Act RMPs (§ 506C(j)) & CDER QMM, EO 13944/14017 essential medicines & KSM onshoring, and ASPR SNS / BARDA IBMSC.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on drug shortages, QMM, and essential medicines.", href: env === "explore" ? "#/ref/shortages-resilience" : "#/explore/shortages-resilience" },
        { title: "Supply Chain, DSCSA & Cold Chain", text: "Serialization, track-and-trace, and cold-chain distribution controls.", href: "#/ref/supply-chain" },
        { title: "Complex Generics & Nitrosamines", text: "PSGs, GDUFA III, and temporary nitrosamine limits to avert shortages.", href: "#/ref/complex-quality" },
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
    if 'shortages_resilience.js' not in txt:
        for anchor in ('import * as complexQuality from "./complex_quality.js";\n', 'import * as comboProducts from "./combo_products.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as shortagesResilience from "./shortages_resilience.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as shortagesResilience from "./shortages_resilience.js";\n' + txt
            changed = True
    if '"/ref/shortages-resilience"' not in txt:
        for anchor in ('if (path === "/ref/complex-quality")', 'if (path === "/ref/combo-products")', 'if (path === "/ref/supply-chain")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/shortages-resilience") return { env: "ref", current: "#/ref/shortages-resilience", ...(await shortagesResilience.shortagesResiliencePage(query, "ref")) };\n  if (path === "/explore/shortages-resilience") return { env: "explore", current: "#/explore/shortages-resilience", ...(await shortagesResilience.shortagesResiliencePage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/shortages-resilience" not in txt:
        for anchor in ('["#/ref/complex-quality", "Complex generics & impurities"]', '["#/ref/combo-products", "Combination products"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/shortages-resilience", "Shortages & essential meds"]', 1)
                changed = True
                break
    if "#/explore/shortages-resilience" not in txt:
        for anchor in ('["#/explore/complex-quality", "Complex generics & impurities"]', '["#/explore/combo-products", "Combination products"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/shortages-resilience", "Shortages & essential meds"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_shortages_resilience.py" in txt:
        return False
    line = "python3 pipeline/build_shortages_resilience.py site/data\n"
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
    if '"/api/shortages-resilience"' in txt:
        return False
    route = (
        '\n@app.get("/api/shortages-resilience")\n'
        'def api_shortages_resilience():\n'
        '    p = DATA_DIR / "shortages_resilience.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "shortages_resilience.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"shortages_resilience.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    sr_ref = _load(data_dir / "shortages_resilience.json", {}) or {}\n'
        '    for sec_key, sec_q in [("shortages_506c", "shortages"), ("cares_rmp_qmm", "cares"), ("essential_meds_onshoring", "essential"), ("aspr_sns_barda", "stockpile")]:\n'
        '        for item in (sr_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "shortages_resilience",\n'
        '                "group": "Drug Shortages, Supply Resilience & Essential Meds",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/shortages-resilience?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/shortages-resilience?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"drug shortage FDASIA 506C CARES Act RMP risk management plan CDER QMM quality management maturity EO 13944 EO 14017 essential medicines KSM onshoring ASPR SNS strategic national stockpile BARDA IBMSC {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"shortages-resilience", "#/ref/shortages-resilience"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    sr_doc = _load_json(data_dir / "shortages_resilience.json")\n'
        '    if isinstance(sr_doc, dict) and sr_doc.get("shortages_506c"):\n'
        '        sr_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (sr_doc.get("shortages_506c") or []) + (sr_doc.get("essential_meds_onshoring") or []))\n'
        '        pages.append(("shortages-resilience", "#/ref/shortages-resilience", "Drug Shortages, Supply Chain Resilience & Essential Medicines",\n'
        '                      "Primary-sourced guide to FDA Drug Shortages (FDASIA 506C), CARES Act RMPs & CDER QMM, EO 13944/14017 essential medicines & onshoring, and ASPR SNS / BARDA IBMSC.",\n'
        '                      f"<ul>{sr_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/shortages-resilience"' in txt:
        return False
    for anchor in ('    "/#/explore/complex-quality",', '    "/#/explore/combo-products",', '    "/#/explore/radiopharma",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/shortages-resilience",\n    "/#/explore/shortages-resilience",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_shortages_resilience_py": _write_if_changed(pipe_dir / "build_shortages_resilience.py", BUILD_SHORTAGES_RESILIENCE_PY),
        "shortages_resilience_js": _write_if_changed(js_dir / "shortages_resilience.js", SHORTAGES_RESILIENCE_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/complex-quality") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/complex-quality", "Complex generics & impurities"]] }];\nconst EXPLORE_NAV = [["#/explore/complex-quality", "Complex generics & impurities"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/complex-quality",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_shortages_resilience.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_shortages_resilience.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"shortages_506c": 6, "cares_rmp_qmm": 6, "essential_meds_onshoring": 6, "aspr_sns_barda": 6}, out

        doc = json.loads((root / "site" / "data" / "shortages_resilience.json").read_text(encoding="utf-8"))
        for k in ("shortages_506c", "cares_rmp_qmm", "essential_meds_onshoring", "aspr_sns_barda"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "shortages_resilience.js").read_text(encoding="utf-8")
        print("V62D_SHORTAGES_RESILIENCE_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2d Drug Shortages, Supply Chain Resilience & Essential Medicines patch.")
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
