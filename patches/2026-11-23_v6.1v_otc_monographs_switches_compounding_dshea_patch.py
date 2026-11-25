#!/usr/bin/env python3
"""Pill by Pill v6.1v Patch: OTC Monographs, Rx-to-OTC Switches (ACNU), Compounding (§ 503A/§ 503B) & Dietary Supplements (DSHEA) Reference (#/ref/otc-compounding, #/explore/otc-compounding, /api/otc-compounding).

1. Adds `pipeline/build_otc_compounding.py` -> `site/data/otc_compounding.json` (6 OTC Monograph
   § 505G pillars, 6 Rx-to-OTC Switch & ACNU pillars, 6 § 503A/§ 503B compounding pillars, and
   6 DSHEA/NDI dietary supplement pillars — 24 primary-sourced entries).
2. Adds `site/js/otc_compounding.js` (`otcCompoundingPage` with inline Non-Prescription,
   Compounding & Supplement Spectrum SVG + 4 section filters) and wires `#/ref/otc-compounding`,
   `#/explore/otc-compounding`, `/api/otc-compounding`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `otc_compounding.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/otc-compounding/` static SEO page + sitemap entry -> 38
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1v_otc_monographs_switches_compounding_dshea_patch.py --selftest
  python3 2026-11-23_v6.1v_otc_monographs_switches_compounding_dshea_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_OTC_COMPOUNDING_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1v OTC Monographs, Rx-to-OTC Switches, Compounding & DSHEA Reference (`site/data/otc_compounding.json`).

Comprehensive, primary-sourced reference covering:
  1. OTC Monograph Reform (§ 505G CARES Act) (6 pillars)
  2. Rx-to-OTC Switches & ACNU Final Rule (6 pillars)
  3. Human Drug Compounding (§ 503A Pharmacies vs. § 503B Outsourcing) (6 pillars)
  4. Dietary Supplements (DSHEA, NDI Notifications & Labeling) (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER, HFP).

Usage:
  python3 pipeline/build_otc_compounding.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

OTC_MONOGRAPHS = [
    {
        "id": "otc-505g-reform",
        "name": "CARES Act OTC Monograph Reform (FD&C Act § 505G)",
        "category": "Administrative Orders",
        "plain": "Over-the-counter staples like ibuprofen, sunscreens, and antacids follow public 'recipe books' called OTC monographs—modernized in 2020 so FDA can update safety rules via administrative orders instead of slow multi-year rulemaking.",
        "technical": "CARES Act (2020) added FD&C Act § 505G (21 U.S.C. 355h), replacing legacy notice-and-comment rulemaking with proposed/final administrative orders and establishing OMUFA user fees.",
        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/over-counter-otc-drug-review-otc-monograph-reform-cares-act",
    },
    {
        "id": "otc-grase",
        "name": "GRASE Conditions (Active Ingredients, Doses, Labeling & Testing)",
        "category": "Monograph Standards",
        "plain": "If an OTC medicine uses an approved ingredient at the exact strength, dose, and warning label in the monograph, the maker can sell it without filing a separate New Drug Application.",
        "technical": "An OTC monograph defines conditions under which a therapeutic category is Generally Recognized as Safe and Effective (GRASE)—covering active ingredients, indications, doses, routes, Drug Facts labeling, and testing.",
        "url": "https://www.fda.gov/drugs/otc-drug-review-process-otc-drug-monographs",
    },
    {
        "id": "otc-omor",
        "name": "OTC Monograph Order Requests (OMORs) & 18-Month Exclusivity",
        "category": "Industry Requests",
        "plain": "A company can ask FDA to add a new OTC ingredient or change a warning label through an OMOR—earning 18 months of exclusivity for certain genuinely new OTC additions.",
        "technical": "Tier 1 (significant changes such as new active ingredients/indications) and Tier 2 (minor labeling/testing updates) OMORs submitted electronically; qualifying Tier 1 innovations may receive 18-month § 505G(b)(5)(C) exclusivity.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/over-counter-monograph-order-requests-format-and-content",
    },
    {
        "id": "otc-drug-facts",
        "name": "Standardized Drug Facts Label (21 CFR 201.66)",
        "category": "Consumer Safety",
        "plain": "Every US over-the-counter box uses the familiar black-and-white 'Drug Facts' box so shoppers can compare active ingredients, warnings, and dosing across brands in seconds.",
        "technical": "21 CFR 201.66 mandates standardized typography, section order (Active Ingredient, Purpose, Uses, Warnings, Directions, Inactive Ingredients), and readability for all nonprescription drug products.",
        "url": "https://www.fda.gov/drugs/how-drugs-are-developed-and-approved/over-counter-otc-nonprescription-drugs",
    },
    {
        "id": "otc-monographs-portal",
        "name": "OTC Monographs@FDA Public Order Portal",
        "category": "Public Registry",
        "plain": "FDA publishes every final and proposed OTC monograph administrative order online so manufacturers, pharmacists, and patients can check current rules.",
        "technical": "Central repository of deemed final administrative orders (e.g., M020 Sunscreen, M013 Internal Analgesics) and active proposed orders under § 505G.",
        "url": "https://www.fda.gov/drugs/otc-drug-review-process-otc-drug-monographs",
    },
    {
        "id": "otc-safety-orders",
        "name": "Rapid OTC Safety Orders & Pediatric Cough/Cold Actions",
        "category": "Post-Market Safety",
        "plain": "Under the modernized system, FDA can act much faster when new safety data emerges—such as updating pediatric dosing warnings or removing unsafe ingredients.",
        "technical": "FD&C Act § 505G(b)(4) authorizes expedited administrative orders when an OTC monograph drug poses an imminent hazard or requires prompt safety labeling updates.",
        "url": "https://www.fda.gov/drugs/cder-small-business-industry-assistance-sbia/small-business-assistance-frequently-asked-questions-regulatory-process-over-counter-otc-drugs",
    },
]

RX_TO_OTC_SWITCHES = [
    {
        "id": "sw-rx-to-otc",
        "name": "Full vs. Partial Prescription-to-Nonprescription (Rx-to-OTC) Switch",
        "category": "NDA / Efficacy Supplement",
        "plain": "Medicines like Claritin, Prilosec, and Narcan nasal spray started as prescription-only drugs and later proved safe enough for self-selection on pharmacy shelves.",
        "technical": "Under 21 CFR 310.200(b), FDA approves an Rx-to-OTC switch when prescription control is no longer necessary for public health and the drug is safe/effective for self-medication; may be a full switch or partial (indication/strength-specific) switch.",
        "url": "https://www.fda.gov/drugs/drug-application-process-nonprescription-drugs/prescription-nonprescription-rx-otc-switches",
    },
    {
        "id": "sw-consumer-studies",
        "name": "Label Comprehension, Self-Selection & Actual Use Studies",
        "category": "Behavioral Evidence",
        "plain": "Before a prescription drug can go over the counter, companies must test real shoppers to prove people understand the box warnings and can correctly decide whether the drug is right for them.",
        "technical": "Specialized OTC behavioral studies—Label Comprehension (communication of key messages), Self-Selection (appropriate purchase decision by target vs. contraindicated users), and Actual Use (simulated real-world dosing without clinician oversight).",
        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/engaging-stakeholders-bring-nonprescription-drug-products-market",
    },
    {
        "id": "sw-acnu-rule",
        "name": "Nonprescription Drug Product with an ACNU (Final Rule)",
        "category": "Digital Self-Selection",
        "plain": "A landmark FDA rule lets a drug be sold without a prescription if the consumer first completes an extra safety step—like an app or kiosk questionnaire—to confirm the medicine is right for them.",
        "technical": "ACNU (Additional Condition for Nonprescription Use) Final Rule creates a pathway where an NDA applicant implements a validated extra condition (e.g., interactive digital/kiosk questionnaire) ensuring appropriate self-selection or actual use when Drug Facts labeling alone is insufficient.",
        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/nonprescription-drug-product-additional-condition-nonprescription-use",
    },
    {
        "id": "sw-3yr-exclusivity",
        "name": "3-Year Hatch-Waxman New Clinical Investigation Exclusivity",
        "category": "Switch Incentive",
        "plain": "Companies that run new Actual Use or clinical studies to move a prescription drug over the counter can earn 3 years of market protection for the OTC version.",
        "technical": "Under FD&C Act § 505(c)(3)(E)(iii)/(iv), a switch NDA/supplement supported by new clinical investigations essential to approval receives 3-year marketing exclusivity blocking generic ANDAs for the OTC product.",
        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/prescription-nonprescription-switch-list",
    },
    {
        "id": "sw-switch-list",
        "name": "FDA Prescription-to-Nonprescription Switch Registry",
        "category": "Approved Switches",
        "plain": "FDA publishes a public list of every medicine that successfully switched from prescription to over-the-counter status—spanning allergy pills, heartburn drugs, topical retinoids, and naloxone.",
        "technical": "Tracks NDA approvals and supplemental switches changing marketing status from Rx to OTC, including active ingredient, switched dosage form/strength, and approval date.",
        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/prescription-nonprescription-switch-list",
    },
    {
        "id": "sw-chronic-access",
        "name": "Expanding Nonprescription Access for Chronic Conditions",
        "category": "Public Health Goal",
        "plain": "By pairing clear Drug Facts boxes with ACNU screening tools, regulators aim to safely widen OTC access for under-treated chronic conditions like high cholesterol or migraines.",
        "technical": "FDA's Nonprescription Drug Engagement Plan outlines stakeholder workshops and CDER/NDAB review coordination for chronic-disease switches and ACNU applications under FD&C Act § 505(b)(7).",
        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/engaging-stakeholders-bring-nonprescription-drug-products-market",
    },
]

COMPOUNDING_503A_503B = [
    {
        "id": "cmp-503a",
        "name": "Traditional Pharmacy Compounding (FD&C Act § 503A)",
        "category": "Patient-Specific Rx",
        "plain": "A local compounding pharmacy mixes a custom medicine for one specific patient's prescription—such as a dye-free liquid for a child with an allergy—without needing FDA drug approval.",
        "technical": "Applies to state-licensed pharmacies/physicians compounding for an identified individual patient pursuant to a valid prescription; exempt from cGMP (21 CFR 211), NDA approval, and DSCSA if meeting § 503A conditions, including USP <795>/<797>.",
        "url": "https://www.fda.gov/drugs/human-drug-compounding/fdc-act-provisions-apply-human-drug-compounding",
    },
    {
        "id": "cmp-503b",
        "name": "Registered Outsourcing Facilities (FD&C Act § 503B)",
        "category": "Hospital Bulk Supply",
        "plain": "Outsourcing facilities are larger sterile compounding factories registered with FDA that can ship ready-to-use hospital IV bags and syringes in bulk without individual patient prescriptions.",
        "technical": "Created by the Drug Quality and Security Act (2013): § 503B facilities compound sterile drugs with or without patient-specific prescriptions, are NOT exempt from cGMP (21 CFR 211), undergo risk-based FDA inspections, and report adverse events.",
        "url": "https://www.fda.gov/drugs/human-drug-compounding/fdc-act-provisions-apply-human-drug-compounding",
    },
    {
        "id": "cmp-copies-shortage",
        "name": "'Essentially a Copy' Restriction & FDA Drug Shortage Exception",
        "category": "Anti-Bypass Guardrail",
        "plain": "Compounders cannot mass-produce cheap knockoffs of normal FDA-approved drugs—unless the approved brand drug is officially on FDA's Drug Shortage List.",
        "technical": "§ 503A bars compounding 'essentially a copy' of a commercially available drug regularly or in inordinate amounts; § 503B bars compounding copies of FDA-approved drugs unless the drug currently appears on FDA's § 506E drug shortage list.",
        "url": "https://www.fda.gov/drugs/drug-alerts-and-statements/fda-clarifies-policies-compounders-national-glp-1-supply-begins-stabilize",
    },
    {
        "id": "cmp-bulks-list",
        "name": "503A & 503B Bulk Drug Substances Lists (API Sourcing)",
        "category": "Ingredient Rules",
        "plain": "To prevent unsafe raw chemicals from entering custom medicines, FDA restricts which bulk active powders compounders can use when they aren't starting from an already-approved pill or vial.",
        "technical": "§ 503A requires bulk APIs with USP/NF monographs, FDA-approved components, or inclusion on the 503A Bulks List; § 503B restricts bulk APIs to the 503B Clinical Need Bulks List or active FDA Drug Shortage List.",
        "url": "https://www.fda.gov/drugs/drug-alerts-and-statements/fda-clarifies-policies-compounders-national-glp-1-supply-begins-stabilize",
    },
    {
        "id": "cmp-unapproved-status",
        "name": "Compounded Drugs Are Not FDA-Approved (Quality & Labeling)",
        "category": "Patient Disclosure",
        "plain": "Unlike commercial pharmacy drugs, compounded medicines have not been reviewed by FDA for safety, effectiveness, or label accuracy—making sterile cGMP and USP standards critical.",
        "technical": "Compounded drugs bypass premarket NDA/ANDA review; § 503B products require prominent 'This is a compounded drug' labeling and adverse-event reporting to FDA.",
        "url": "https://www.fda.gov/drugs/human-drug-compounding/questions-and-answers-related-guidance-entities-considering-whether-register-outsourcing-facilities",
    },
    {
        "id": "cmp-glp1-enforcement",
        "name": "Shortage Resolution Transitions & Compounding Enforcement",
        "category": "Recent Case Study",
        "plain": "When a major drug shortage—such as recent GLP-1 shortages—ends and factories catch up, temporary compounding permissions wind down and standard copy restrictions snap back.",
        "technical": "Once FDA removes a drug from the Drug Shortage List, the product is commercially available again, ending § 503A/§ 503B copy exceptions after transition wind-down windows.",
        "url": "https://www.fda.gov/drugs/drug-alerts-and-statements/fda-clarifies-policies-compounders-national-glp-1-supply-begins-stabilize",
    },
]

DIETARY_SUPPLEMENTS = [
    {
        "id": "ds-dshea-1994",
        "name": "Dietary Supplement Health and Education Act (DSHEA, 1994)",
        "category": "Statutory Boundary",
        "plain": "Vitamins, minerals, herbs, and amino acids sold as dietary supplements are regulated like a special category of food—not as drugs—so FDA does not pre-approve them for effectiveness before sale.",
        "technical": "Under DSHEA (1994), dietary supplements are regulated under food authorities (21 CFR Part 111 cGMPs); manufacturers are responsible for safety and truthful labeling, while FDA enforces post-market adulteration/misbranding actions.",
        "url": "https://www.fda.gov/food/dietary-supplements",
    },
    {
        "id": "ds-dietary-ing",
        "name": "Statutory Definition of a 'Dietary Ingredient'",
        "category": "Eligible Substances",
        "plain": "To legally be a dietary supplement, a product must contain a vitamin, mineral, herb/botanical, amino acid, or dietary substance—and cannot be an already-approved prescription drug.",
        "technical": "FD&C Act § 201(ff) defines dietary ingredients across 6 categories and excludes articles previously authorized as an investigational new drug (IND) or approved drug prior to supplement marketing (the drug-exclusion clause).",
        "url": "https://www.fda.gov/food/information-consumers-using-dietary-supplements/questions-and-answers-dietary-supplements",
    },
    {
        "id": "ds-ndi",
        "name": "New Dietary Ingredient (NDI) 75-Day Premarket Notification",
        "category": "Safety Review",
        "plain": "If a supplement introduces a brand-new ingredient that was not sold in US supplements before October 15, 1994, the company must notify FDA with safety data at least 75 days before launching.",
        "technical": "FD&C Act § 413 requires an NDI Notification (NDIN) demonstrating history of safe use or toxicological evidence establishing a reasonable expectation of safety at least 75 days prior to interstate marketing.",
        "url": "https://www.fda.gov/food/dietary-supplements/new-dietary-ingredient-ndi-notification-process",
    },
    {
        "id": "ds-ndi-identity",
        "name": "FDA Final Guidance on NDI Identity & Safety Information",
        "category": "CMC & Toxicology",
        "plain": "FDA updated its NDI guidance to explain exactly how supplement makers must prove what is in their botanical extract or capsule and back up its safety.",
        "technical": "Final Guidance (Identity and Safety Information for NDINs) details chemical/botanical characterization, manufacturing process controls, specification limits, and safety/toxicology data packages.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-industry-new-dietary-ingredient-ndi-notifications-and-related-issues-identity-and-safety",
    },
    {
        "id": "ds-claims-disclaimer",
        "name": "Structure/Function Claims vs. Prohibited Disease Claims",
        "category": "Labeling Boundary",
        "plain": "A supplement bottle can say 'supports immune health' with the standard FDA disclaimer, but saying 'prevents flu' or 'treats diabetes' turns it into an unapproved illegal drug.",
        "technical": "Structure/function claims (21 CFR 101.93) require notification within 30 days of marketing and the mandatory DSHEA disclaimer ('This statement has not been evaluated by the FDA... not intended to diagnose, treat, cure, or prevent any disease').",
        "url": "https://www.fda.gov/food/information-consumers-using-dietary-supplements/questions-and-answers-dietary-supplements",
    },
    {
        "id": "ds-master-files",
        "name": "NDIN Master Files & Serious Adverse Event Reporting",
        "category": "IP & Safety",
        "plain": "Ingredient suppliers can now protect proprietary manufacturing recipes in confidential FDA Master Files while letting finished-brand customers reference the safety data.",
        "technical": "2024 Draft Guidance on NDIN Master Files mirrors drug DMFs for confidential identity/safety data; Dietary Supplement and Nonprescription Drug Consumer Protection Act (2006) mandates 15-day reporting of serious adverse events.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/draft-guidance-industry-new-dietary-ingredient-notification-master-files-dietary-supplements",
    },
]


def build_otc_compounding(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "otc_monographs": len(OTC_MONOGRAPHS),
            "rx_to_otc_switches": len(RX_TO_OTC_SWITCHES),
            "compounding_503a_503b": len(COMPOUNDING_503A_503B),
            "dietary_supplements": len(DIETARY_SUPPLEMENTS),
        },
        "otc_monographs": OTC_MONOGRAPHS,
        "rx_to_otc_switches": RX_TO_OTC_SWITCHES,
        "compounding_503a_503b": COMPOUNDING_503A_503B,
        "dietary_supplements": DIETARY_SUPPLEMENTS,
    }
    (data_dir / "otc_compounding.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_otc_compounding.py <site/data>")
    print(json.dumps(build_otc_compounding(pathlib.Path(sys.argv[1])), indent=2))
'''

OTC_COMPOUNDING_JS = '''// Pill by Pill v6.1v: OTC Monographs, Rx-to-OTC Switches (ACNU), Compounding (§ 503A/§ 503B) & Dietary Supplements (DSHEA) Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["otc", "OTC Monographs (§ 505G)", "otc_monographs"],
  ["switches", "Rx-to-OTC & ACNU", "rx_to_otc_switches"],
  ["compounding", "Compounding (503A/503B)", "compounding_503a_503b"],
  ["supplements", "Supplements (DSHEA/NDI)", "dietary_supplements"],
];

function otcSpectrumSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Nonprescription OTC, Rx-to-OTC switch, compounding, and dietary supplement regulatory spectrum">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. OTC Monographs</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">CARES Act § 505G</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">GRASE &amp; Drug Facts</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#otc-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Rx-to-OTC &amp; ACNU</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Actual Use &amp; Self-Select</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">3-Yr NDA Exclusivity</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#otc-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Compounding</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">§ 503A Rx vs. § 503B cGMP</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Bulks &amp; Shortage Lists</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#otc-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Supplements</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">DSHEA (Food Framework)</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">75-Day NDI &amp; No Rx Claims</text>
      <defs><marker id="otc-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">FDA oversees non-prescription drugs, custom-compounded medications, and dietary supplements under distinct statutory standards.</figcaption>
  </figure>`;
}

export async function otcCompoundingPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/otc_compounding.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/otc-compounding" : "#/ref/otc-compounding";

  const pills = html`<div class="chips" role="navigation" aria-label="OTC, compounding, and supplements sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Framework / Provision</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${otcSpectrumSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA OTC Monograph Reform (§ 505G), ACNU Final Rule, § 503A/§ 503B Compounding, and DSHEA/NDI documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["OTC, Compounding & Supplements"]] : [REF_HOME, ["OTC, Compounding & Supplements"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "OTC Monographs, Rx-to-OTC Switches, Compounding & Supplements",
      lede: env === "explore"
        ? "How over-the-counter medicines, custom-mixed prescriptions, and vitamins or herbal supplements are regulated differently from prescription drugs."
        : "CARES Act § 505G OTC monographs, Rx-to-OTC switches & ACNU, § 503A/§ 503B compounding, and DSHEA / 75-day NDI dietary supplements.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on OTC, compounding, and supplements.", href: env === "explore" ? "#/ref/otc-compounding" : "#/explore/otc-compounding" },
        { title: "Regulatory Pathways & Exclusivity", text: "NDA/ANDA, 505(b)(2), and 3-year clinical investigation exclusivity.", href: "#/ref/pathways" },
        { title: "Supply Chain, DSCSA & Shortages", text: "How drug shortages temporarily enable § 503A/§ 503B compounding.", href: "#/ref/supply-chain" },
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
    if 'otc_compounding.js' not in txt:
        for anchor in ('import * as digitalHealth from "./digital_health.js";\n', 'import * as orphan from "./orphan.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as otcCompounding from "./otc_compounding.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as otcCompounding from "./otc_compounding.js";\n' + txt
            changed = True
    if '"/ref/otc-compounding"' not in txt:
        for anchor in ('if (path === "/ref/digital-health")', 'if (path === "/ref/orphan")', 'if (path === "/ref/vaccines")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/otc-compounding") return { env: "ref", current: "#/ref/otc-compounding", ...(await otcCompounding.otcCompoundingPage(query, "ref")) };\n  if (path === "/explore/otc-compounding") return { env: "explore", current: "#/explore/otc-compounding", ...(await otcCompounding.otcCompoundingPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/otc-compounding" not in txt:
        for anchor in ('["#/ref/digital-health", "Digital health & AI"]', '["#/ref/orphan", "Orphan & pediatric"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/otc-compounding", "OTC & compounding"]', 1)
                changed = True
                break
    if "#/explore/otc-compounding" not in txt:
        for anchor in ('["#/explore/digital-health", "Digital health & AI"]', '["#/explore/orphan", "Orphan & pediatric"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/otc-compounding", "OTC & compounding"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_otc_compounding.py" in txt:
        return False
    line = "python3 pipeline/build_otc_compounding.py site/data\n"
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
    if '"/api/otc-compounding"' in txt:
        return False
    route = (
        '\n@app.get("/api/otc-compounding")\n'
        'def api_otc_compounding():\n'
        '    p = DATA_DIR / "otc_compounding.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "otc_compounding.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"otc_compounding.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    otc_ref = _load(data_dir / "otc_compounding.json", {}) or {}\n'
        '    for sec_key, sec_q in [("otc_monographs", "otc"), ("rx_to_otc_switches", "switches"), ("compounding_503a_503b", "compounding"), ("dietary_supplements", "supplements")]:\n'
        '        for item in (otc_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "otc_compounding",\n'
        '                "group": "OTC, Compounding & Supplements",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/otc-compounding?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/otc-compounding?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"OTC monograph 505G GRASE Drug Facts Rx-to-OTC switch ACNU compounding 503A 503B outsourcing dietary supplement DSHEA NDI {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"otc-compounding", "#/ref/otc-compounding"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    otc_doc = _load_json(data_dir / "otc_compounding.json")\n'
        '    if isinstance(otc_doc, dict) and otc_doc.get("otc_monographs"):\n'
        '        otc_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (otc_doc.get("otc_monographs") or []) + (otc_doc.get("compounding_503a_503b") or []))\n'
        '        pages.append(("otc-compounding", "#/ref/otc-compounding", "OTC Monographs, Rx-to-OTC Switches, Compounding & Supplements",\n'
        '                      "Primary-sourced guide to CARES Act § 505G OTC monographs, Rx-to-OTC switches & ACNU, § 503A/§ 503B compounding, and DSHEA dietary supplements.",\n'
        '                      f"<ul>{otc_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/otc-compounding"' in txt:
        return False
    for anchor in ('    "/#/explore/digital-health",', '    "/#/explore/orphan",', '    "/#/explore/vaccines",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/otc-compounding",\n    "/#/explore/otc-compounding",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_otc_compounding_py": _write_if_changed(pipe_dir / "build_otc_compounding.py", BUILD_OTC_COMPOUNDING_PY),
        "otc_compounding_js": _write_if_changed(js_dir / "otc_compounding.js", OTC_COMPOUNDING_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/digital-health") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/digital-health", "Digital health & AI"]] }];\nconst EXPLORE_NAV = [["#/explore/digital-health", "Digital health & AI"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/digital-health",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_otc_compounding.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_otc_compounding.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"otc_monographs": 6, "rx_to_otc_switches": 6, "compounding_503a_503b": 6, "dietary_supplements": 6}, out

        doc = json.loads((root / "site" / "data" / "otc_compounding.json").read_text(encoding="utf-8"))
        for k in ("otc_monographs", "rx_to_otc_switches", "compounding_503a_503b", "dietary_supplements"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "otc_compounding.js").read_text(encoding="utf-8")
        print("V61V_OTC_MONOGRAPHS_SWITCHES_COMPOUNDING_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1v OTC Monographs, Switches, Compounding & DSHEA patch.")
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
