#!/usr/bin/env python3
"""Pill by Pill v6.2b Patch: Combination Products, Drug-Device Co-Development, 21 CFR Part 4 cGMP & Human Factors Reference (#/ref/combo-products, #/explore/combo-products, /api/combo-products).

1. Adds `pipeline/build_combo_products.py` -> `site/data/combo_products.json` (6 OCP Jurisdiction,
   PMOA & RFD/Pre-RFD pillars, 6 Combination Product cGMP [21 CFR Part 4] & Streamlined QMSR
   pillars, 6 Drug-Device Bridging, EDDCs & Emergency-Use Injectors pillars, and 6 Human Factors
   Engineering & Postmarketing Safety Reporting [PMSR] pillars — 24 primary-sourced entries).
2. Adds `site/js/combo_products.js` (`comboProductsPage` with inline Drug-Device Combination
   Product Lifecycle SVG + 4 section filters) and wires `#/ref/combo-products`,
   `#/explore/combo-products`, `/api/combo-products`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `combo_products.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/combo-products/` static SEO page + sitemap entry -> 44
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.2b_combination_products_drug_device_human_factors_patch.py --selftest
  python3 2026-11-23_v6.2b_combination_products_drug_device_human_factors_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_COMBO_PRODUCTS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2b Combination Products, 21 CFR Part 4 cGMP & Human Factors Reference (`site/data/combo_products.json`).

Comprehensive, primary-sourced reference covering:
  1. OCP Jurisdiction, Primary Mode of Action (PMOA) & RFD / Pre-RFD (6 pillars)
  2. Combination Product cGMP (21 CFR Part 4) & Streamlined QMSR (6 pillars)
  3. Drug-Device Bridging, EDDCs & Emergency-Use Injectors (6 pillars)
  4. Human Factors Engineering (HFE) & Postmarketing Safety Reporting (PMSR) (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA OCP, CDER, CBER, CDRH).

Usage:
  python3 pipeline/build_combo_products.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

OCP_PMOA_RFD = [
    {
        "id": "cmb-21cfr3-types",
        "name": "Four Statutory Combination Product Configurations (21 CFR 3.2(e))",
        "category": "Product Definition",
        "plain": "A combination product pairs a drug or biologic with a medical device—like a pre-filled syringe, asthma inhaler, auto-injector pen, or drug-eluting stent.",
        "technical": "21 CFR 3.2(e) defines four combination product types: single-entity (e.g., prefilled syringe, drug-eluting stent), co-packaged kit, cross-labeled approved products, and cross-labeled investigational products.",
        "url": "https://www.fda.gov/media/156663/download",
    },
    {
        "id": "cmb-ocp-pmoa",
        "name": "Office of Combination Products (OCP) & Primary Mode of Action (PMOA)",
        "category": "Center Assignment",
        "plain": "When a product is part drug and part device, FDA's Office of Combination Products assigns the lead review center (CDER, CBER, or CDRH) based on whichever part does the main medical job.",
        "technical": "Under 21 CFR 3.2(m), OCP assigns the lead FDA Center according to the Primary Mode of Action (PMOA)—the single mode of action expected to make the greatest contribution to the overall intended therapeutic effects.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/how-write-request-designation-rfd",
    },
    {
        "id": "cmb-rfd-prerfd",
        "name": "Request for Designation (RFD) vs. Informal Pre-RFD",
        "category": "Jurisdiction Ruling",
        "plain": "If a company isn't sure whether FDA will regulate a novel drug-device combo as a drug or a device, it can ask OCP informally (Pre-RFD) or get a binding 60-day ruling (RFD).",
        "technical": "Sponsors submit an informal Pre-RFD for preliminary feedback or a formal Request for Designation (RFD) under 21 CFR Part 3 to obtain a binding written Center assignment determination from OCP.",
        "url": "https://www.fda.gov/combination-products/rfd-process",
    },
    {
        "id": "cmb-premarket-pathways",
        "name": "Single-Application vs. Separate Constituent Pathways (NDA/BLA/PMA)",
        "category": "Filing Strategy",
        "plain": "Most pre-filled injectors file a single drug application (NDA or BLA) with device engineering data inside, while other combos coordinate across two Centers.",
        "technical": "FDA's Principles of Premarket Pathways guidance explains how a single marketing application (NDA, BLA, 510(k), De Novo, PMA) typically covers a combination product, with inter-Center consults from CDRH/CDER/CBER.",
        "url": "https://www.fda.gov/media/119958/download",
    },
    {
        "id": "cmb-intercenter-feedback",
        "name": "Requesting Aligned Multi-Center FDA Feedback (Q-Sub / Type C)",
        "category": "Agency Coordination",
        "plain": "Instead of getting conflicting advice from FDA's drug reviewers and device engineers, sponsors can request unified combination-product meetings.",
        "technical": "FDA's Requesting Feedback guidance details coordinated Pre-IND/Type C and Q-Submission pathways so CDER, CBER, and CDRH review device design, human factors, and clinical bridging together.",
        "url": "https://www.fda.gov/media/133768/download",
    },
    {
        "id": "cmb-500-apps",
        "name": "500+ Original Combination Product Applications Per Year",
        "category": "Industry Volume",
        "plain": "Over 500 new drug-device and biologic-device applications reach FDA every year, driven by self-administered biologics, GLP-1 pens, and wearable injectors.",
        "technical": "Per OCP Performance Reports, FDA receives >500 original premarket combination product applications annually across CDER, CBER, and CDRH, spanning injectors, inhalers, transdermal patches, and drug-eluting devices.",
        "url": "https://www.fda.gov/media/144887/download",
    },
]

COMBO_CGMP_PART4 = [
    {
        "id": "cmb-21cfr4-rule",
        "name": "21 CFR Part 4 Subpart A: Combination Product cGMP Final Rule",
        "category": "Unified Quality",
        "plain": "Because a combination product is both a drug and a device, 21 CFR Part 4 lets factories follow one base quality system plus a short checklist of rules from the other side.",
        "technical": "21 CFR Part 4 clarifies that drug cGMPs (21 CFR 210/211), device Quality System Regulation / QMSR (21 CFR 820), and biologic cGMPs (21 CFR 600–680) apply—establishing a 'streamlined approach' to avoid duplicate systems.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/current-good-manufacturing-practice-requirements-combination-products",
    },
    {
        "id": "cmb-streamlined-drug",
        "name": "Drug-Led Streamlined Approach (21 CFR 210/211 + 820 Call-Outs)",
        "category": "CDER/CBER Factory",
        "plain": "A pharma plant making pre-filled syringes follows full drug cGMPs plus six key medical-device rules—like Design Controls, CAPA, and purchasing controls.",
        "technical": "Under 21 CFR 4.4(b)(1), drug-led combo manufacturers comply fully with 21 CFR 210/211 plus called-out 21 CFR 820 provisions: Management Responsibility, Design Controls (820.30), Purchasing, CAPA (820.100), Installation, and Servicing.",
        "url": "https://www.fda.gov/media/138592/download",
    },
    {
        "id": "cmb-streamlined-device",
        "name": "Device-Led Streamlined Approach (21 CFR 820 + 211 Call-Outs)",
        "category": "CDRH Factory",
        "plain": "A medtech plant making drug-coated stents follows full device quality rules plus essential pharma checks—like stability testing, expiration dating, and reserve samples.",
        "technical": "Under 21 CFR 4.4(b)(2), device-led combo manufacturers comply fully with 21 CFR 820 plus called-out 21 CFR 211 provisions: component testing/approval (211.84), yield calculation, tamper-evident OTC packaging, stability (211.166), expiration, and reserve samples.",
        "url": "https://www.fda.gov/media/138592/download",
    },
    {
        "id": "cmb-biologic-600",
        "name": "Additional 21 CFR Parts 600–680 Rules for Biologic-Device Combos",
        "category": "Biologic Combos",
        "plain": "If a syringe or auto-injector holds a monoclonal antibody or vaccine, the factory must also satisfy biologic-specific sterility, lot-release, and potency rules.",
        "technical": "Per 21 CFR 4.4(b)(3), biologic-device combination products must satisfy applicable 21 CFR Parts 600–680 biologic cGMP requirements in addition to streamlined drug/device Part 4 provisions.",
        "url": "https://www.fda.gov/media/137158/download",
    },
    {
        "id": "cmb-design-history",
        "name": "Design Controls (21 CFR 820.30) & Constituent Interaction Testing",
        "category": "Design History File",
        "plain": "Pharma companies must maintain a formal Design History File proving the needle, spring, glass barrel, and liquid medicine don't leach chemicals or jam together.",
        "technical": "21 CFR 820.30 Design Controls require Design Inputs/Outputs, Design Verification/Validation, Design Transfer, and Risk Management assessing drug-device chemical compatibility, extractables/leachables, and mechanical reliability.",
        "url": "https://www.fda.gov/media/138592/download",
    },
    {
        "id": "cmb-qmsr-iso13485",
        "name": "Alignment with Revised 21 CFR 820 Quality Management System Regulation (QMSR)",
        "category": "ISO 13485 Harmonization",
        "plain": "FDA updated its device quality rules to align with international ISO 13485 standards, harmonizing how drug-device factories document risk and supplier controls.",
        "technical": "Recent FDA combination-product guidance aligns device drug-delivery control expectations with the revised 21 CFR Part 820 Quality Management System Regulation (QMSR) incorporating ISO 13485.",
        "url": "https://www.fda.gov/media/179545/download",
    },
]

BRIDGING_EDDC_INJECTORS = [
    {
        "id": "cmb-bridging-pathway",
        "name": "Bridging Studies for Drug-Device & Biologic-Device Switches",
        "category": "Lifecycle Changes",
        "plain": "When a company switches a drug from a clinic vial-and-syringe to an at-home auto-injector pen, bridging studies prove the pen delivers the exact same blood levels without repeating huge Phase 3 trials.",
        "technical": "FDA's Bridging guidance details how sponsors use risk analysis, in vitro device performance, PK bioequivalence, and human factors data to bridge clinical data from an earlier presentation (e.g., vial) to a to-be-marketed device.",
        "url": "https://www.fda.gov/combination-products/guidance-regulatory-information/combination-products-guidance-documents",
    },
    {
        "id": "cmb-eddc-guidance",
        "name": "Essential Drug Delivery Performance Characteristics (EDDCs)",
        "category": "Device CQAs",
        "plain": "Every injector or inhaler has 'make-or-break' mechanical specs—like delivered dose accuracy, injection time, and needle extension—that FDA treats like drug Critical Quality Attributes.",
        "technical": "FDA's EDDC guidance defines Essential Drug Delivery Performance Characteristics analogous to ICH Q8(R2) CQAs (and ICH Q12 Established Conditions), covering verification, lot-release, and post-expiry aging tests.",
        "url": "https://www.fda.gov/media/179545/download",
    },
    {
        "id": "cmb-emergency-injectors",
        "name": "High-Reliability Standard for Emergency-Use Injectors (Epinephrine / Naloxone)",
        "category": "99.99%+ Reliability",
        "plain": "If an EpiPen or emergency naloxone auto-injector jams during a crisis, a patient can die—so FDA demands extreme statistical reliability testing through the end of shelf life.",
        "technical": "FDA's Emergency-Use Injectors guidance requires demonstrating high reliability of essential performance outputs across initial lots and worst-case environmental/shipping/expiry conditioning under 21 CFR 4.4.",
        "url": "https://www.fda.gov/media/137158/download",
    },
    {
        "id": "cmb-extractables-leachables",
        "name": "Container Closure Integrity (CCI) & Extractables / Leachables",
        "category": "Material Compatibility",
        "plain": "Silicone oil, rubber stoppers, and plastic plungers inside a pre-filled syringe must be tested so they never react with delicate biologic molecules or break sterility.",
        "technical": "Combination product CMC packages evaluate container-closure integrity, syringe glide force, silicone oil migration, and extractables/leachables across real-time stability.",
        "url": "https://www.fda.gov/media/179545/download",
    },
    {
        "id": "cmb-generic-anda-device",
        "name": "Generic Drug-Device ANDA User-Interface Sameness (Naloxone / GLP-1 Pens)",
        "category": "Generic Combos",
        "plain": "A generic copy of an auto-injector or nasal spray doesn't have to be identical inside, but patients must be able to pick it up and use it safely without retraining.",
        "technical": "ANDA combination products evaluate comparative analyses (labeling, external critical design attributes, physical characteristics) and threshold/comparative human factors studies when device user interfaces differ from the RLD.",
        "url": "https://www.fda.gov/media/171855/download",
    },
    {
        "id": "cmb-ich-q12-eddc",
        "name": "ICH Q12 Established Conditions for Device Design Changes",
        "category": "Post-Approval CMC",
        "plain": "Mapping which device specs are 'Established Conditions' helps companies upgrade an injector spring or molding supplier after approval with predictable FDA filing tiers.",
        "technical": "FDA's EDDC guidance aligns EDDCs and their control strategies with ICH Q12 Established Conditions to streamline post-approval device constituent manufacturing and design changes.",
        "url": "https://www.fda.gov/media/179545/download",
    },
]

HFE_PMSR_SAFETY = [
    {
        "id": "cmb-hfe-guidance",
        "name": "Human Factors Engineering (HFE) & Usability Validation (Sept 2023 Q&A)",
        "category": "Use-Related Risk",
        "plain": "Before an auto-injector or inhaler is approved, real patients and caregivers must test it in simulated-use studies to prove they won't accidentally inject into a thumb or skip a dose.",
        "technical": "FDA's September 2023 Combination Products HFE Q&A and Applying HFE guidance mandate Use-Related Risk Analysis (URRA), formative evaluations, and summative Human Factors validation testing with representative users.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/application-human-factors-engineering-principles-combination-products-questions-and-answers",
    },
    {
        "id": "cmb-hfe-critical-tasks",
        "name": "Critical Tasks, Labeling Comprehension & Simulated-Use Testing",
        "category": "Summative HFE",
        "plain": "HFE testing focuses on 'critical tasks'—like removing the safety cap, holding the pen for 10 seconds, and checking the viewing window—where a slip-up causes harm.",
        "technical": "Summative HFE validation evaluates critical tasks (tasks whose failure or omission causes serious harm or compromised therapy) across untrained/trained user groups using final production-equivalent user interfaces and IFUs.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",
    },
    {
        "id": "cmb-pmsr-21cfr4",
        "name": "Postmarketing Safety Reporting (PMSR) for Combination Products (21 CFR 4.102)",
        "category": "Unified Safety",
        "plain": "If a patient suffers a side effect OR a mechanical device jam with a combo product, the manufacturer must report both drug safety and device malfunction events under one rulebook.",
        "technical": "21 CFR 4.102 requires Combination Product Applicants to submit constituent-part PMSR reports covering both application-type adverse drug experiences and device-specific Five-Day / Malfunction / Correction-Removal reports.",
        "url": "https://www.fda.gov/media/111788/download",
    },
    {
        "id": "cmb-pmsr-sharing",
        "name": "Constituent-Part Information Sharing & Recordkeeping (21 CFR 4.103 / 4.105)",
        "category": "Co-Packaged Partners",
        "plain": "When two separate companies supply a cross-labeled drug and device, federal rules require them to share adverse-event complaints with each other within 5 calendar days.",
        "technical": "21 CFR 4.103 mandates Constituent Part Applicants to share safety/malfunction information with partner constituent holders within 5 calendar days of receipt, with recordkeeping governed by 21 CFR 4.105.",
        "url": "https://www.fda.gov/media/111788/download",
    },
    {
        "id": "cmb-pmsr-streamlined",
        "name": "Streamlined Single-Report PMSR Submissions (FAERS & eMDR)",
        "category": "Reporting Mechanics",
        "plain": "To avoid filing duplicate paperwork for the same incident, FDA allows manufacturers to combine drug and device safety details into a single electronic report.",
        "technical": "Under 21 CFR 4.102, Combination Product Applicants may streamline reporting when the same event triggers both drug (15-day expedited) and device (30-day MDR malfunction) criteria, referencing the Combination Product Identifier.",
        "url": "https://www.fda.gov/media/111788/download",
    },
    {
        "id": "cmb-hfe-device-benefits",
        "name": "Reducing Recalls & Use Errors Through Usability Engineering",
        "category": "Patient Safety",
        "plain": "Clearer injector windows, audible clicks, and color-coded caps cut down dosing mistakes, lessen reliance on dense paper manuals, and prevent costly product recalls.",
        "technical": "FDA's HFE framework demonstrates that proactive usability engineering reduces use-related adverse events, alarm/display misinterpretation, and postmarket recalls across home-use and clinical combination products.",
        "url": "https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/human-factors-and-medical-devices",
    },
]


def build_combo_products(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "ocp_pmoa_rfd": len(OCP_PMOA_RFD),
            "combo_cgmp_part4": len(COMBO_CGMP_PART4),
            "bridging_eddc_injectors": len(BRIDGING_EDDC_INJECTORS),
            "hfe_pmsr_safety": len(HFE_PMSR_SAFETY),
        },
        "ocp_pmoa_rfd": OCP_PMOA_RFD,
        "combo_cgmp_part4": COMBO_CGMP_PART4,
        "bridging_eddc_injectors": BRIDGING_EDDC_INJECTORS,
        "hfe_pmsr_safety": HFE_PMSR_SAFETY,
    }
    (data_dir / "combo_products.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_combo_products.py <site/data>")
    print(json.dumps(build_combo_products(pathlib.Path(sys.argv[1])), indent=2))
'''

COMBO_PRODUCTS_JS = '''// Pill by Pill v6.2b: Combination Products, Drug-Device Co-Development, 21 CFR Part 4 cGMP & Human Factors Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["ocp", "OCP, PMOA & RFD", "ocp_pmoa_rfd"],
  ["cgmp", "21 CFR Part 4 cGMP", "combo_cgmp_part4"],
  ["bridging", "Bridging, EDDC & Injectors", "bridging_eddc_injectors"],
  ["hfe", "Human Factors & PMSR", "hfe_pmsr_safety"],
];

function comboProductsSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Combination product lifecycle: OCP PMOA/RFD, 21 CFR Part 4 cGMP, Bridging/EDDCs, and Human Factors/PMSR">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. OCP &amp; PMOA</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">21 CFR Part 3 &amp; RFD</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">CDER / CBER / CDRH</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cmb-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Part 4 cGMP</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Streamlined 211 + 820</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Design Controls &amp; QMSR</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cmb-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Bridging &amp; EDDCs</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">PK Vial-to-Pen Bridge</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Emergency Injector Spec</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#cmb-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. HFE &amp; PMSR</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">URRA &amp; Summative Use</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">21 CFR 4.102 Safety</text>
      <defs><marker id="cmb-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">FDA's Office of Combination Products coordinates drug, biologic, and device requirements from PMOA assignment through 21 CFR Part 4 cGMP, bridging, HFE, and PMSR.</figcaption>
  </figure>`;
}

export async function comboProductsPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/combo_products.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/combo-products" : "#/ref/combo-products";

  const pills = html`<div class="chips" role="navigation" aria-label="Combination products sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Standard / Provision</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${comboProductsSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Office of Combination Products (21 CFR Part 3 &amp; Part 4), EDDC, Emergency-Use Injectors, HFE, and PMSR documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Combination Products & Devices"]] : [REF_HOME, ["Combination Products & Devices"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Combination Products, Drug-Device Co-Dev, Part 4 cGMP & HFE",
      lede: env === "explore"
        ? "How pre-filled syringes, auto-injector pens, asthma inhalers, and drug-eluting stents are approved, manufactured, and usability-tested."
        : "OCP PMOA & RFD (21 CFR Part 3), 21 CFR Part 4 streamlined cGMP/QMSR, vial-to-pen bridging, EDDCs, Human Factors, and 21 CFR 4.102 PMSR.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on combination products.", href: env === "explore" ? "#/ref/combo-products" : "#/explore/combo-products" },
        { title: "Sterile Manufacturing & Cleanrooms", text: "Aseptic filling of pre-filled syringes and cartridges.", href: "#/ref/sterile" },
        { title: "Digital Health, SaMD & AI/ML", text: "Connected injectors, PDURS, and device software.", href: "#/ref/digital-health" },
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
    if 'combo_products.js' not in txt:
        for anchor in ('import * as radiopharma from "./radiopharma.js";\n', 'import * as specialPopulations from "./special_populations.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as comboProducts from "./combo_products.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as comboProducts from "./combo_products.js";\n' + txt
            changed = True
    if '"/ref/combo-products"' not in txt:
        for anchor in ('if (path === "/ref/radiopharma")', 'if (path === "/ref/special-populations")', 'if (path === "/ref/pricing-access")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/combo-products") return { env: "ref", current: "#/ref/combo-products", ...(await comboProducts.comboProductsPage(query, "ref")) };\n  if (path === "/explore/combo-products") return { env: "explore", current: "#/explore/combo-products", ...(await comboProducts.comboProductsPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/combo-products" not in txt:
        for anchor in ('["#/ref/radiopharma", "Radiopharma & theranostics"]', '["#/ref/special-populations", "Special populations"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/combo-products", "Combination products"]', 1)
                changed = True
                break
    if "#/explore/combo-products" not in txt:
        for anchor in ('["#/explore/radiopharma", "Radiopharma & theranostics"]', '["#/explore/special-populations", "Special populations"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/combo-products", "Combination products"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_combo_products.py" in txt:
        return False
    line = "python3 pipeline/build_combo_products.py site/data\n"
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
    if '"/api/combo-products"' in txt:
        return False
    route = (
        '\n@app.get("/api/combo-products")\n'
        'def api_combo_products():\n'
        '    p = DATA_DIR / "combo_products.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "combo_products.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"combo_products.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    cmb_ref = _load(data_dir / "combo_products.json", {}) or {}\n'
        '    for sec_key, sec_q in [("ocp_pmoa_rfd", "ocp"), ("combo_cgmp_part4", "cgmp"), ("bridging_eddc_injectors", "bridging"), ("hfe_pmsr_safety", "hfe")]:\n'
        '        for item in (cmb_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "combo_products",\n'
        '                "group": "Combination Products & Devices",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/combo-products?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/combo-products?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"combination product drug device OCP PMOA RFD 21 CFR Part 3 Part 4 cGMP QMSR ISO 13485 auto-injector prefilled syringe bridging EDDC emergency injector human factors HFE PMSR {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"combo-products", "#/ref/combo-products"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    cmb_doc = _load_json(data_dir / "combo_products.json")\n'
        '    if isinstance(cmb_doc, dict) and cmb_doc.get("ocp_pmoa_rfd"):\n'
        '        cmb_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (cmb_doc.get("ocp_pmoa_rfd") or []) + (cmb_doc.get("hfe_pmsr_safety") or []))\n'
        '        pages.append(("combo-products", "#/ref/combo-products", "Combination Products, Drug-Device Co-Dev, Part 4 cGMP & HFE",\n'
        '                      "Primary-sourced guide to OCP PMOA/RFD, 21 CFR Part 4 streamlined cGMP/QMSR, drug-device bridging, EDDCs, Human Factors, and PMSR.",\n'
        '                      f"<ul>{cmb_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/combo-products"' in txt:
        return False
    for anchor in ('    "/#/explore/radiopharma",', '    "/#/explore/special-populations",', '    "/#/explore/pricing-access",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/combo-products",\n    "/#/explore/combo-products",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_combo_products_py": _write_if_changed(pipe_dir / "build_combo_products.py", BUILD_COMBO_PRODUCTS_PY),
        "combo_products_js": _write_if_changed(js_dir / "combo_products.js", COMBO_PRODUCTS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/radiopharma") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/radiopharma", "Radiopharma & theranostics"]] }];\nconst EXPLORE_NAV = [["#/explore/radiopharma", "Radiopharma & theranostics"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/radiopharma",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_combo_products.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_combo_products.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ocp_pmoa_rfd": 6, "combo_cgmp_part4": 6, "bridging_eddc_injectors": 6, "hfe_pmsr_safety": 6}, out

        doc = json.loads((root / "site" / "data" / "combo_products.json").read_text(encoding="utf-8"))
        for k in ("ocp_pmoa_rfd", "combo_cgmp_part4", "bridging_eddc_injectors", "hfe_pmsr_safety"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "combo_products.js").read_text(encoding="utf-8")
        print("V62B_COMBO_PRODUCTS_HFE_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2b Combination Products, Part 4 cGMP & Human Factors patch.")
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
