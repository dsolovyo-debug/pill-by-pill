#!/usr/bin/env python3
"""Pill by Pill v6.1s Patch: OTC Monographs, Rx-to-OTC Switches & Pharmacy Compounding 503A/503B (#/ref/otc, #/explore/otc, /api/otc).

1. Adds `pipeline/build_otc_compounding.py` -> `site/data/otc_compounding.json` (6 OTC Monograph /
   CARES Act / DSHEA pillars, 6 Rx-to-OTC switch & ACNU frameworks, 6 503A/503B compounding &
   USP <795>/<797>/<800> standards, and 6 consumer safety / DEA / BeSafeRx pillars — 24 entries).
2. Adds `site/js/otc_compounding.js` (`otcCompoundingPage` with inline Flow SVG + 4 section filters)
   and wires `#/ref/otc`, `#/explore/otc`, `/api/otc`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `otc_compounding.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/otc/` static SEO page + sitemap entry -> 35
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1s_otc_monographs_switches_compounding_patch.py --selftest
  python3 2026-11-24_v6.1s_otc_monographs_switches_compounding_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_OTC_COMP_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1s OTC Monographs, Rx-to-OTC Switches & Pharmacy Compounding (503A/503B) (`site/data/otc_compounding.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. OTC Monograph System & CARES Act Reform (6 pillars: GRASE & Monograph \'Recipe Books\', CARES Act 2020 Administrative Orders & OMUFA, Drug Facts Label 21 CFR 201.66, OTC Monograph vs. OTC NDA, Behind-the-Counter & State Controls, Dietary Supplements DSHEA vs. OTC Drugs)\n  2. Rx-to-OTC Switches & Consumer Self-Selection (6 pillars: Durham-Humphrey Rx/OTC Boundary, Label Comprehension Studies, Self-Selection & Actual Use Studies, 3-Year Hatch-Waxman Switch Exclusivity, ACNU Additional Condition for Nonprescription Use, Landmark Switches: Ibuprofen/Omeprazole/Naloxone/Opill)\n  3. Pharmacy Compounding: 503A vs. 503B Outsourcing Facilities (6 pillars: Why Compounding Exists, Section 503A Traditional Pharmacies, Section 503B Outsourcing Facilities & cGMP, Drug Quality and Security Act DQSA 2013, USP <795>/<797>/<800> Standards, FDA Shortages & \'Essentially a Copy\' Rules)\n  4. Consumer Safety, Misuse Prevention & Counterfeits (6 pillars: Acetaminophen & Multi-Symptom Duplication, Child-Resistant Packaging PPPA, Tamper-Evident Packaging 21 CFR 211.132, DEA Controlled Substance Schedules I–V, Online Pharmacy & Counterfeit Risks BeSafeRx, Unapproved / Adulterated Product Alerts)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, DEA).\n\nUsage:\n  python3 pipeline/build_otc_compounding.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nOTC_MONOGRAPHS = [\n    {\n        "id": "otc-grase",\n        "name": "OTC Monographs & GRASE (\'Recipe Books\' for Store-Shelf Drugs)",\n        "plain": "Instead of reviewing every single store-brand aspirin or sunscreen individually, the FDA publishes official \'recipe books\' (monographs) listing safe active ingredients, doses, and warnings.",\n        "technical": "Products conforming to an OTC Monograph are Generally Recognized as Safe and Effective (GRASE) under FD&C Act § 505G and may be marketed without an individual NDA, while remaining subject to cGMP and listing.",\n        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/over-counter-otc-drug-monograph-process",\n    },\n    {\n        "id": "otc-cares-omufa",\n        "name": "CARES Act (2020) Reform, Administrative Orders & OMUFA",\n        "plain": "For decades, updating an OTC rule took years of slow federal rulemaking; a 2020 law replaced that with faster FDA Administrative Orders funded by OTC user fees (OMUFA)—used to update sunscreens and decongestants.",\n        "technical": "Section 505G (CARES Act) replaced notice-and-comment rulemaking with Administrative Orders (including 18-month exclusivity for qualifying OTC Monograph Order Requests, OMORs) and established the OTC Monograph Drug User Fee Program (OMUFA).",\n        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/over-counter-otc-drug-monograph-process",\n    },\n    {\n        "id": "otc-drug-facts",\n        "name": "Standardized \'Drug Facts\' Label (21 CFR 201.66)",\n        "plain": "Every U.S. nonprescription box carries the same standardized black-and-white \'Drug Facts\' table—listing Active Ingredient, Uses, Warnings, Directions, and Inactive Ingredients so consumers can compare products safely.",\n        "technical": "Mandated under 21 CFR 201.66 with strict typography, section ordering, and plain-language formatting to prevent accidental overdose and drug-drug interactions without a clinician present.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-201",\n    },\n    {\n        "id": "otc-monograph-vs-nda",\n        "name": "OTC Monograph vs. OTC NDA Pathway",\n        "plain": "Classic ingredients like acetaminophen or hydrocortisone follow a shared monograph, whereas newer switched drugs or novel strengths require a full individual FDA NDA approval.",\n        "technical": "OTC NDAs (505(b)(1)/505(b)(2)) undergo full CMC, safety, and consumer-behavior review and can qualify for 3-year Hatch-Waxman exclusivity, after which OTC ANDA generics may enter.",\n        "url": "https://www.fda.gov/drugs/drug-application-process-nonprescription-drugs/drug-applications-over-counter-otc-drugs",\n    },\n    {\n        "id": "otc-btc",\n        "name": "Behind-the-Counter & Statutory Purchase Controls (CMEA)",\n        "plain": "Certain nonprescription medicines—like pseudoephedrine cold pills—sit behind the pharmacy counter with ID and quantity limits to prevent misuse without requiring a doctor\'s prescription.",\n        "technical": "Combat Methamphetamine Epidemic Act (CMEA) enforces daily/monthly gram caps and logbooks for ephedrine/pseudoephedrine; unlike the UK/Canada/Australia, the U.S. has no general \'pharmacist-only\' third drug class.",\n        "url": "https://www.fda.gov/drugs/information-drug-class/legal-requirements-sale-and-purchase-drug-products-containing-pseudoephedrine-ephedrine-and",\n    },\n    {\n        "id": "otc-dshea",\n        "name": "OTC Drugs vs. Dietary Supplements (DSHEA 1994)",\n        "plain": "Vitamins, herbs, and supplements sit right next to OTC medicines on pharmacy shelves, but by law they are regulated as foods—meaning they do NOT prove safety or effectiveness to the FDA before going on sale.",\n        "technical": "Under the Dietary Supplement Health and Education Act (DSHEA, 21 U.S.C. § 343), supplements cannot make disease-treatment claims (only structure/function claims with mandatory disclaimer) and follow 21 CFR Part 111 cGMP rather than drug NDAs.",\n        "url": "https://www.fda.gov/food/dietary-supplements",\n    },\n]\n\nRX_TO_OTC = [\n    {\n        "id": "sw-durham-humphrey",\n        "name": "Durham-Humphrey Amendment (1951) — The Rx vs. OTC Legal Line",\n        "plain": "A medicine can be sold over the counter only if everyday consumers can safely diagnose their own symptoms, pick the right product, and take it correctly using just the box label—without a doctor\'s supervision.",\n        "technical": "FD&C Act § 503(b)(1) requires prescription status whenever toxicity, method of use, or collateral measures make a drug unsafe except under a licensed practitioner\'s supervision.",\n        "url": "https://www.fda.gov/drugs/drug-application-process-nonprescription-drugs/prescription-over-counter-otc-switch-list",\n    },\n    {\n        "id": "sw-label-comp",\n        "name": "Label Comprehension Studies (LCS)",\n        "plain": "Before moving a prescription pill to store shelves, developers test the draft Drug Facts box with hundreds of everyday shoppers—including people with lower reading literacy—to confirm they understand key warnings.",\n        "technical": "FDA Label Comprehension Guidance evaluates primary communication objectives (contraindications, stop-use warnings, dosing limits) across general and low-literacy cohorts before Actual Use trials.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/label-comprehension-studies-nonprescription-drug-products",\n    },\n    {\n        "id": "sw-self-selection",\n        "name": "Self-Selection & Actual Use Studies (AUS)",\n        "plain": "Shoppers decide on their own whether the medicine is right for them—and in Actual Use trials, take it home and use it in real life without doctor coaching—to prove real-world safety.",\n        "technical": "Self-selection studies measure correct \'do/do not use\' decisions against medical history; Actual Use Studies simulate unassisted retail purchase and dosing to confirm low misuse and safe clinical behavior.",\n        "url": "https://www.fda.gov/drugs/drug-application-process-nonprescription-drugs/drug-applications-over-counter-otc-drugs",\n    },\n    {\n        "id": "sw-3yr-excl",\n        "name": "3-Year Hatch-Waxman Switch Exclusivity",\n        "plain": "Running consumer label and actual-use trials costs tens of millions of dollars, so U.S. law grants 3 years of OTC market exclusivity to the sponsor that proves a prescription drug is safe for store shelves.",\n        "technical": "Under 21 CFR 314.108, new clinical investigations (such as Actual Use Studies) essential for approval of an Rx-to-OTC switch NDA qualify for 3-year exclusivity against OTC generic copies.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "sw-acnu",\n        "name": "ACNU — Additional Condition for Nonprescription Use (2024 Final Rule)",\n        "plain": "A landmark new FDA pathway allowing more complex chronic medicines (like blood-pressure or cholesterol drugs) to go over the counter if consumers first complete a validated smartphone or kiosk screening questionnaire.",\n        "technical": "FDA\'s December 2024 Final Rule (21 CFR Parts 201 & 314) enables approval of nonprescription drugs with an Additional Condition for Nonprescription Use (ACNU) when labeling alone is insufficient for safe self-selection.",\n        "url": "https://www.fda.gov/drugs/over-counter-otc-nonprescription-drugs/nonprescription-drug-product-additional-condition-nonprescription-use",\n    },\n    {\n        "id": "sw-landmarks",\n        "name": "Landmark Switches (Ibuprofen, Omeprazole, Naloxone & Opill)",\n        "plain": "Many household staples started as prescription-only—from ibuprofen (1984) and omeprazole (2003) to life-saving Narcan naloxone nasal spray (2023) and Opill, the first U.S. OTC daily birth control pill (2023).",\n        "technical": "FDA\'s Prescription-to-OTC Switch List documents partial switches (specific lower strengths/indications move OTC while higher strengths remain Rx) and full switches transforming public health access.",\n        "url": "https://www.fda.gov/drugs/drug-application-process-nonprescription-drugs/prescription-over-counter-otc-switch-list",\n    },\n]\n\nCOMPOUNDING = [\n    {\n        "id": "cmp-why",\n        "name": "What Pharmacy Compounding Is (and Is Not)",\n        "plain": "Compounding means a licensed pharmacist mixes or alters ingredients to meet an individual patient\'s unique medical need—like making a dye-free liquid for a child allergic to a commercial tablet. Compounded drugs are NOT FDA-approved.",\n        "technical": "Because compounded preparations do not undergo FDA premarket NDA/ANDA review for safety, effectiveness, or bioequivalence, federal law restricts when they may be made and dispensed.",\n        "url": "https://www.fda.gov/drugs/human-drug-compounding/compounding-and-fda-questions-and-answers",\n    },\n    {\n        "id": "cmp-503a",\n        "name": "Section 503A Traditional Compounding Pharmacies",\n        "plain": "Neighborhood or specialty compounding pharmacies that prepare custom prescriptions one patient at a time based on an individual doctor\'s prescription, regulated primarily by state boards of pharmacy.",\n        "technical": "FD&C Act § 503A exempts patient-specific compounded drugs from NDA approval and federal cGMP (21 CFR 211) if compounded by a licensed pharmacist/physician using USP/NF or FDA bulk-list substances under state pharmacy oversight.",\n        "url": "https://www.fda.gov/drugs/human-drug-compounding/fdca-provisions-apply-human-drug-compounding",\n    },\n    {\n        "id": "cmp-503b",\n        "name": "Section 503B Outsourcing Facilities (Hospital Bulk Supply & cGMP)",\n        "plain": "Registered large-scale compounding facilities that can produce sterile hospital syringes and IV bags in bulk without individual prescriptions—but must obey strict FDA factory cGMP rules and routine FDA inspections.",\n        "technical": "Created under FD&C Act § 503B; facilities register with FDA, report products/adverse events, comply with cGMP, and appear on FDA\'s public Outsourcing Facilities inspection/Form 483 list.",\n        "url": "https://www.fda.gov/drugs/human-drug-compounding/registered-outsourcing-facilities",\n    },\n    {\n        "id": "cmp-dqsa-2013",\n        "name": "Drug Quality and Security Act (DQSA, 2013)",\n        "plain": "Passed by Congress after the tragic 2012 New England Compounding Center fungal meningitis outbreak—creating the strict 503B outsourcing facility framework alongside DSCSA supply-chain serialization.",\n        "technical": "Title I (Compounding Quality Act) clarified § 503A and established § 503B FDA oversight; Title II (DSCSA) established electronic unit-level track-and-trace across the U.S. prescription supply chain.",\n        "url": "https://www.fda.gov/drugs/human-drug-compounding/compounding-laws-and-policies",\n    },\n    {\n        "id": "cmp-usp-795-797-800",\n        "name": "USP <795>, <797> & <800> Compounding Quality Standards",\n        "plain": "The official quality rulebooks for pharmacies: <795> covers non-sterile creams and liquids, <797> covers sterile cleanroom injectables, and <800> protects healthcare workers handling hazardous chemotherapy drugs.",\n        "technical": "Enforced by State Boards of Pharmacy and Joint Commission; revised 2023 USP <795>/<797> define Beyond-Use Dates (BUDs), ISO 5 primary engineering controls, and personnel garbing/gloved-fingertip testing.",\n        "url": "https://www.fda.gov/drugs/human-drug-compounding/compounding-and-fda-questions-and-answers",\n    },\n    {\n        "id": "cmp-shortages-copy",\n        "name": "FDA Drug Shortages & \'Essentially a Copy\' Restrictions",\n        "plain": "Compounders normally cannot mass-produce copies of commercially available brand drugs—EXCEPT when the FDA officially declares a drug in shortage (as seen during recent GLP-1 shortages), and that exception ends once the shortage resolves.",\n        "technical": "Under §§ 503A(b)(1)(D) and 503B(a)(5), compounding \'essentially a copy\' of an approved drug is prohibited unless the drug appears on the FDA Drug Shortage List (FD&C Act § 506E) or a prescriber documents a specific patient clinical difference.",\n        "url": "https://www.fda.gov/drugs/human-drug-compounding/compounding-when-drugs-are-fdas-drug-shortages-list",\n    },\n]\n\nCONSUMER_SAFETY = [\n    {\n        "id": "cs-acetaminophen",\n        "name": "Multi-Symptom Duplication & Acetaminophen Liver Safety",\n        "plain": "A common hidden danger on OTC shelves: taking a pain reliever plus a cold/flu syrup that both contain acetaminophen can silently exceed the safe daily liver limit.",\n        "technical": "FDA limits prescription combination acetaminophen to 325 mg per dosage unit and mandates prominent liver-warning language on OTC Drug Facts labels (adult maximum 4,000 mg/day across all sources).",\n        "url": "https://www.fda.gov/drugs/information-drug-class/acetaminophen",\n    },\n    {\n        "id": "cs-pppa",\n        "name": "Child-Resistant Packaging (Poison Prevention Packaging Act)",\n        "plain": "Push-and-turn caps and blister packs required on most prescription and OTC bottles have saved thousands of young children from accidental household poisonings since 1970.",\n        "technical": "Administered by CPSC under 16 CFR Part 1700; requires special packaging that 85% of children under 5 cannot open while 90% of senior adults can open.",\n        "url": "https://www.fda.gov/drugs/buying-using-medicine-safely/understanding-over-counter-medicines",\n    },\n    {\n        "id": "cs-tamper-evident",\n        "name": "Tamper-Evident Packaging (21 CFR 211.132)",\n        "plain": "Born out of the 1982 Tylenol cyanide tampering crisis, federal law requires foil seals, shrink bands, or glued cartons on OTC medicines so shoppers can immediately spot if a package was opened.",\n        "technical": "21 CFR 211.132 mandates tamper-evident packaging features with a prominent label statement alerting consumers not to use the product if the safety seal is broken or missing.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",\n    },\n    {\n        "id": "cs-dea-schedules",\n        "name": "DEA Controlled Substance Schedules (I–V)",\n        "plain": "Medicines with abuse or dependence risk are classified by federal law into five Schedules—from Schedule I (no accepted medical use) to Schedule II (strictest prescriptions like opioids/stimulants) down to Schedule V.",\n        "technical": "Controlled Substances Act (21 U.S.C. § 812) jointly assessed by FDA (8-factor scientific analysis) and DEA; governs manufacturing quotas, prescribing refills, EPCS electronic prescriptions, and pharmacy record-keeping.",\n        "url": "https://www.dea.gov/drug-information/drug-scheduling",\n    },\n    {\n        "id": "cs-besaferx",\n        "name": "Online Pharmacies & Counterfeit Risks (FDA BeSafeRx)",\n        "plain": "Rogue websites selling \'no-prescription-needed\' pills often ship fake tablets containing zero active drug—or lethal fentanyl. FDA\'s BeSafeRx campaign teaches consumers to verify state-licensed pharmacies.",\n        "technical": "Legitimate U.S. online pharmacies require a valid prescription, hold active State Board of Pharmacy licensure, display a physical U.S. address/pharmacist contact, and carry NABP .pharmacy verification.",\n        "url": "https://www.fda.gov/drugs/besaferx-your-source-online-pharmacy-information",\n    },\n    {\n        "id": "cs-tainted-alerts",\n        "name": "FDA Health Fraud & Tainted Product Alerts",\n        "plain": "Some sketchy gas-station or online \'natural\' weight-loss or sexual-enhancement capsules secretly spike hidden prescription drugs inside—tracked in FDA\'s public Health Fraud database.",\n        "technical": "FDA laboratory testing routinely uncovers undeclared APIs (e.g., sildenafil, sibutramine, corticosteroids) in unapproved supplements/creams, triggering Warning Letters, recalls, and Import Alerts.",\n        "url": "https://www.fda.gov/consumers/health-fraud-scams/health-fraud-product-database",\n    },\n]\n\n\ndef build_otc_compounding(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on FDA OTC Monographs (CARES Act/OMUFA), Rx-to-OTC switches (ACNU), 503A/503B pharmacy compounding, and consumer medication safety (FDA, eCFR, DEA). Educational reference only.",\n        "otc_monographs": OTC_MONOGRAPHS,\n        "rx_to_otc": RX_TO_OTC,\n        "compounding": COMPOUNDING,\n        "consumer_safety": CONSUMER_SAFETY,\n    }\n    (data_dir / "otc_compounding.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "otc_monographs": len(OTC_MONOGRAPHS),\n        "rx_to_otc": len(RX_TO_OTC),\n        "compounding": len(COMPOUNDING),\n        "consumer_safety": len(CONSUMER_SAFETY),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_otc_compounding(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
OTC_COMPOUNDING_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderOtcCompSvg() {\n  const nodes = [\n    { x: 8, label: "1. OTC Monograph", sub: "GRASE / OMUFA" },\n    { x: 140, label: "2. Rx -> OTC", sub: "LCS / AUS / ACNU" },\n    { x: 272, label: "3. 503A Custom", sub: "Patient Rx / USP" },\n    { x: 404, label: "4. 503B Bulk", sub: "FDA cGMP / Shortages" },\n    { x: 536, label: "5. Safe Use", sub: "Drug Facts / BeSafeRx" },\n  ];\n  return html`<figure class="otc-flow" aria-label="OTC nonprescription, Rx-to-OTC switch, and 503A/503B compounding landscape">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 1 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 1 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">How nonprescription OTC drugs, Rx-to-OTC switches, and 503A/503B compounded preparations are regulated alongside standard prescription NDAs.</figcaption>\n  </figure>`;\n}\n\nexport async function otcCompoundingPage(query, mode = "ref") {\n  const doc = await getJSON("data/otc_compounding.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/otc" : "#/ref/otc";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "OTC Monographs, Rx-to-OTC Switches & Pharmacy Compounding (503A/503B)",\n    body: html`\n      <h1>OTC Monographs, Rx-to-OTC Switches &amp; Pharmacy Compounding</h1>\n      <p class="lead">${mode === "explore"\n        ? "How store-shelf medicines are regulated without a prescription, how prescription drugs earn FDA permission to move over the counter, how custom compounding pharmacies (503A vs. 503B) work, and how to stay safe."\n        : "Primary-sourced reference covering 6 OTC Monograph & CARES Act/OMUFA pillars, 6 Rx-to-OTC switch & ACNU frameworks, 6 503A/503B compounding & USP standards, and 6 consumer medication safety rules (checked " + doc.checked + ")."}</p>\n\n      ${renderOtcCompSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=monographs"${sec === "monographs" ? \' aria-current="page"\' : ""}>OTC Monographs (6)</a> ·\n        <a href="${base}?section=switches"${sec === "switches" ? \' aria-current="page"\' : ""}>Rx-to-OTC Switches (6)</a> ·\n        <a href="${base}?section=compounding"${sec === "compounding" ? \' aria-current="page"\' : ""}>503A / 503B Compounding (6)</a> ·\n        <a href="${base}?section=safety"${sec === "safety" ? \' aria-current="page"\' : ""}>Consumer Safety &amp; DEA (6)</a>\n      </p>\n\n      ${show("monographs") ? html`\n        <h2 id="monographs">1. OTC Monograph System, CARES Act &amp; Supplements (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="OTC monograph system">\n          <table class="tbl"><thead><tr><th>Regulatory Pillar</th><th>${mode === "explore" ? "How Store-Shelf Drugs Are Regulated" : "Statutory & Labeling Framework"}</th></tr></thead>\n          <tbody>${(doc.otc_monographs || []).map((m) => html`<tr id="${m.id}">\n            <td><b><a href="${m.url}" target="_blank" rel="noopener">${m.name}</a></b></td>\n            <td>${mode === "explore" ? m.plain : html`${m.plain}<br><span class="muted small">${m.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("switches") ? html`\n        <h2 id="switches">2. Rx-to-OTC Switches, Self-Selection &amp; ACNU (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Rx to OTC switches">\n          <table class="tbl"><thead><tr><th>Switch Requirement / Milestone</th><th>${mode === "explore" ? "How a Prescription Drug Goes OTC" : "Consumer Behavior Studies & Exclusivity"}</th></tr></thead>\n          <tbody>${(doc.rx_to_otc || []).map((s) => html`<tr id="${s.id}">\n            <td><b><a href="${s.url}" target="_blank" rel="noopener">${s.name}</a></b></td>\n            <td>${mode === "explore" ? s.plain : html`${s.plain}<br><span class="muted small">${s.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("compounding") ? html`\n        <h2 id="compounding">3. Pharmacy Compounding: 503A vs. 503B &amp; Drug Shortages (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="503A and 503B compounding">\n          <table class="tbl"><thead><tr><th>Compounding Rule / Standard</th><th>${mode === "explore" ? "How Custom Pharmacies Are Overseen" : "DQSA, cGMP, USP <795>/<797>/<800> & Shortages"}</th></tr></thead>\n          <tbody>${(doc.compounding || []).map((c) => html`<tr id="${c.id}">\n            <td><b><a href="${c.url}" target="_blank" rel="noopener">${c.name}</a></b></td>\n            <td>${mode === "explore" ? c.plain : html`${c.plain}<br><span class="muted small">${c.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("safety") ? html`\n        <h2 id="safety">4. Consumer Safety, Packaging, DEA Schedules &amp; Counterfeits (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Consumer medication safety">\n          <table class="tbl"><thead><tr><th>Safety Control</th><th>${mode === "explore" ? "How It Protects Shoppers" : "Statutory & Enforcement Standard"}</th></tr></thead>\n          <tbody>${(doc.consumer_safety || []).map((x) => html`<tr id="${x.id}">\n            <td><b><a href="${x.url}" target="_blank" rel="noopener">${x.name}</a></b></td>\n            <td>${mode === "explore" ? x.plain : html`${x.plain}<br><span class="muted small">${x.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/pathways">Approval Pathways</a> · <a href="#/ref/safety">Drug Safety &amp; Recalls</a> · <a href="#/ref/vendors">FDA/EMA Facility Audits</a> · <a href="#/ref/departments/distribution">Stage 8: Supply Chain</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { otcCompoundingPage } from "./otc_compounding.js";\n'
    if "./otc_compounding.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/otc"' not in txt:
        for anchor in ('if (path === "/ref/rare-pediatric")', 'if (path === "/ref/rwe")', 'if (path === "/ref/atmp")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/otc") return otcCompoundingPage(query, "ref");\n'
                    '  if (path === "/explore/otc") return otcCompoundingPage(query, "explore");\n'
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
    if "#/ref/otc" not in txt:
        for anchor in ('["#/ref/rare-pediatric", "Rare & pediatric"]', '["#/ref/rwe", "RWE & digital health"]', '["#/ref/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/otc", "OTC & compounding"]', 1)
                changed = True
                break
    if "#/explore/otc" not in txt:
        for anchor in ('["#/explore/rare-pediatric", "Rare & pediatric"]', '["#/explore/rwe", "RWE & digital health"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/otc", "OTC & compounding"]', 1)
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
    hook = "\n# v6.1s: OTC Monographs, Rx-to-OTC Switches & Pharmacy Compounding (503A/503B)\npython3 pipeline/build_otc_compounding.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/otc"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/otc")\n'
        'def api_otc_compounding():\n'
        '    return _read_json(SITE_DIR / "data" / "otc_compounding.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
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
        '    for sec_key, sec_q in [("otc_monographs", "monographs"), ("rx_to_otc", "switches"), ("compounding", "compounding"), ("consumer_safety", "safety")]:\n'
        '        for item in (otc_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "otc_compounding",\n'
        '                "group": "OTC Monographs & Compounding",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/otc?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/otc?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"OTC monograph GRASE OMUFA Rx to OTC switch ACNU compounding 503A 503B DQSA USP 797 DEA schedule DSHEA {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"otc", "#/ref/otc"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    otc_doc = _load_json(data_dir / "otc_compounding.json")\n'
        '    if isinstance(otc_doc, dict) and otc_doc.get("otc_monographs"):\n'
        '        o_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (otc_doc.get("otc_monographs") or []) + (otc_doc.get("compounding") or []))\n'
        '        pages.append(("otc", "#/ref/otc", "OTC Monographs, Rx-to-OTC Switches & Pharmacy Compounding (503A/503B)",\n'
        '                      "Primary-sourced guide to FDA OTC Monographs (CARES Act/OMUFA), Rx-to-OTC switches & ACNU, 503A vs. 503B compounding & USP <797>, DEA schedules, and consumer medication safety.",\n'
        '                      f"<ul>{o_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/otc"' in txt:
        return False
    for anchor in ('    "/#/explore/rare-pediatric",', '    "/#/explore/rwe",', '    "/#/explore/atmp",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/otc",\n    "/#/explore/otc",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_otc_compounding_py": _write_if_changed(pipe_dir / "build_otc_compounding.py", BUILD_OTC_COMP_PY),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/rare-pediatric") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/rare-pediatric", "Rare & pediatric"]] }];\nconst EXPLORE_NAV = [["#/explore/rare-pediatric", "Rare & pediatric"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/rare-pediatric",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_otc_compounding.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_otc_compounding.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"otc_monographs": 6, "rx_to_otc": 6, "compounding": 6, "consumer_safety": 6}, out

        doc = json.loads((root / "site" / "data" / "otc_compounding.json").read_text(encoding="utf-8"))
        for k in ("otc_monographs", "rx_to_otc", "compounding", "consumer_safety"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61S_OTC_MONOGRAPHS_SWITCHES_COMPOUNDING_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1s OTC Monographs, Rx-to-OTC Switches & Compounding patch.")
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
