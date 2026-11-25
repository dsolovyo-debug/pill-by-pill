#!/usr/bin/env python3
"""Pill by Pill v6.1q Patch: Real-World Evidence (RWE), Registries & Digital Health Technologies (DHTs) (#/ref/rwe, #/explore/rwe, /api/rwe).

1. Adds `pipeline/build_rwe_dht.py` -> `site/data/rwe_dht.json` (6 RWD sources & Common Data Models,
   6 regulatory RWE causal designs, 6 DHT & Decentralized Clinical Trial frameworks, and 6 SaMD /
   AI-ML regulatory pillars — 24 primary-sourced entries anchored to FDA/eCFR/EMA).
2. Adds `site/js/rwe_dht.js` (`rweDhtPage` with inline RWD-to-RWE Pipeline SVG + 4 section
   filters) and wires `#/ref/rwe`, `#/explore/rwe`, `/api/rwe`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `rwe_dht.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/rwe/` static SEO page + sitemap entry -> 33
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1q_rwe_registries_and_digital_health_patch.py --selftest
  python3 2026-11-23_v6.1q_rwe_registries_and_digital_health_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_RWE_DHT_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1q Real-World Evidence (RWE), Registries & Digital Health Technologies (DHTs) (`site/data/rwe_dht.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Real-World Data (RWD) Sources & Data Standards (6 pillars: EHR & Claims Data, Disease & Product Registries, Natural History Studies, Common Data Models OMOP/SCDM/PCORnet, Data Fitness Reliability & Relevance, Tokenization & Privacy Linkage)\n  2. Regulatory RWE Study Designs & Bias Mitigation (6 frameworks: Target Trial Emulation, Externally Controlled Trials, Pragmatic & Registry-Based RCTs, Confounding & Propensity Scoring, Immortal Time & Selection Bias, FDA/EMA RWE Frameworks & DARWIN EU)\n  3. Digital Health Technologies (DHTs) & Decentralized Trials (6 pillars: Wearables & Remote Sensors, Verification Analytical & Clinical Validation V3, Decentralized Trial Elements DCTs, eConsent & ePRO/eCOA, Digital Endpoints & Actigraphy, Data Integrity 21 CFR Part 11 for DHTs)\n  4. Software as a Medical Device (SaMD), AI/ML & Digital Therapeutics (6 pillars: SaMD & IMDRF Risk Classification, AI/ML-Enabled Medical Devices & PCCP, Prescription Digital Therapeutics PDTs, Companion Apps & Adherence Sensors, FDA/EMA AI in Drug Development, Cybersecurity & Post-Market AI Drift)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, EMA).\n\nUsage:\n  python3 pipeline/build_rwe_dht.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nRWD_SOURCES = [\n    {\n        "id": "rwd-ehr-claims",\n        "name": "Electronic Health Records (EHRs) & Administrative Claims Data",\n        "plain": "Everyday doctor notes, lab results, and insurance billing records—anonymized across millions of patients—help researchers see how medicines perform outside strict clinical trials.",\n        "technical": "FDA EHR & Medical Claims Guidance evaluates longitudinal completeness, ICD-10/SNOMED/RxNorm/LOINC coding validity, unstructured NLP extraction (e.g., oncology progression), and pharmacy fill vs. actual adherence gaps.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-data-assessing-electronic-health-records-and-medical-claims-data-support-regulatory",\n    },\n    {\n        "id": "rwd-registries",\n        "name": "Patient, Disease & Product Registries",\n        "plain": "Organized long-term databases that follow everyone with a specific disease or taking a specific medicine (like a rare-disease gene therapy or pregnancy exposure) over many years.",\n        "technical": "FDA Registries Guidance defines governance, standardized case-report forms, active follow-up for loss-to-retention, and source-data verification required to support regulatory label expansions or post-marketing commitments.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-data-assessing-registries-support-regulatory-decision-making-drug-and-biological-products",\n    },\n    {\n        "id": "rwd-natural-history",\n        "name": "Rare-Disease Natural History Studies",\n        "plain": "Before testing a drug for a rare condition with no existing treatment, researchers track how the disease naturally progresses over time so they know whether a new medicine truly slows it down.",\n        "technical": "Prospective or retrospective observational cohorts establishing baseline progression trajectories, biomarker kinetics, and validated clinical endpoints for ultra-rare pediatric and genetic disorders.",\n        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",\n    },\n    {\n        "id": "rwd-cdm",\n        "name": "Common Data Models (OMOP, FDA Sentinel SCDM & PCORnet)",\n        "plain": "Because every hospital formats its computer records differently, Common Data Models translate records into one shared grammar so studies can run across dozens of health systems without moving raw patient files.",\n        "technical": "Federated analytics via OHDSI OMOP CDM, FDA Sentinel Common Data Model (SCDM), and PCORnet CDM enable standardized distributed queries while preserving local patient privacy.",\n        "url": "https://www.fda.gov/safety/fdas-sentinel-initiative",\n    },\n    {\n        "id": "rwd-fitness",\n        "name": "FDA \'Fit-for-Use\' Standard (Reliability & Relevance)",\n        "plain": "Not all real-world data is good enough for an FDA decision—regulators check whether the records are accurate and complete (reliable) and actually capture the right patients and outcomes (relevant).",\n        "technical": "FDA RWE Framework mandates formal data-fitness assessments covering data accrual, provenance, quality assurance/audit trails (reliability) alongside key exposure, covariate, and endpoint availability (relevance).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-real-world-data-and-real-world-evidence-support-regulatory-decision-making-drug",\n    },\n    {\n        "id": "rwd-linkage",\n        "name": "Privacy-Preserving Record Linkage (PPRL) & Tokenization",\n        "plain": "Uses encrypted one-way \'tokens\' so researchers can connect a patient\'s hospital visits, lab tests, and pharmacy fills across separate systems without ever seeing their name or Social Security number.",\n        "technical": "HIPAA-compliant cryptographic hashing/tokenization links EHR, claims, genomic, and mortality registries (NDI) while mitigating re-identification risk and verifying linkage sensitivity/specificity.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-world-data-assessing-electronic-health-records-and-medical-claims-data-support-regulatory",\n    },\n]\n\nRWE_DESIGNS = [\n    {\n        "id": "rwe-target-trial",\n        "name": "Target Trial Emulation (Causal Inference from RWD)",\n        "plain": "Designs an observational database study by writing down the exact rules of an ideal randomized trial first—eligibility, start date, treatment arms, and outcomes—to avoid classic data-mining traps.",\n        "technical": "Explicitly aligns eligibility criteria, treatment assignment, and time-zero (index date) in new-user active-comparator cohorts to estimate intention-to-treat and per-protocol causal effects from observational RWD.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-real-world-data-and-real-world-evidence-support-regulatory-decision-making-drug",\n    },\n    {\n        "id": "rwe-external-control",\n        "name": "Externally Controlled Trials (Historical & Contemporaneous)",\n        "plain": "When giving a placebo would be unethical in a fatal rare disease, real-world patient records can serve as an external comparison group for a single-arm trial.",\n        "technical": "FDA External Control Guidance requires contemporaneous RWD matching baseline prognostic factors, standardized outcome assessment timing, and quantitative bias / E-value sensitivity analyses.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-design-and-conduct-externally-controlled-trials-drug-and-biological-products",\n    },\n    {\n        "id": "rwe-pragmatic-rct",\n        "name": "Pragmatic & Registry-Based Randomized Trials (rRCTs)",\n        "plain": "Combines the scientific power of random assignment with routine doctor visits and electronic health records, making large trials faster and closer to everyday medical practice.",\n        "technical": "Randomizes participants within existing clinical care networks or disease registries, capturing follow-up outcomes passively via EHR/claims/registries with simplified eligibility.",\n        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",\n    },\n    {\n        "id": "rwe-confounding",\n        "name": "Confounding by Indication & Propensity Score Methods",\n        "plain": "In real life, doctors give stronger medicines to sicker patients—so raw comparisons can falsely make a good drug look worse unless statisticians carefully balance patient sickness levels.",\n        "technical": "Mitigates measured confounding via propensity-score matching, inverse probability of treatment weighting (IPTW), high-dimensional propensity scores (hdPS), and negative-control outcomes to detect residual unmeasured confounding.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-real-world-data-and-real-world-evidence-support-regulatory-decision-making-drug",\n    },\n    {\n        "id": "rwe-immortal-time",\n        "name": "Immortal Time Bias & Protocol Pre-Registration",\n        "plain": "A subtle statistical trap where patients who had to survive long enough to fill a prescription get unfairly credited with \'extra survival time\'—prevented by locking study protocols before looking at outcomes.",\n        "technical": "Avoided via strict time-zero alignment, cloning/censoring/weighting, and pre-specifying protocols and Statistical Analysis Plans (SAPs) in public registries (e.g., ClinicalTrials.gov / HMA-EMA Catalogues) prior to execution.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-real-world-data-and-real-world-evidence-support-regulatory-decision-making-drug",\n    },\n    {\n        "id": "rwe-fda-darwin",\n        "name": "FDA RWE Program (21st Century Cures) & EMA DARWIN EU",\n        "plain": "Both the US FDA and Europe\'s EMA have built dedicated Real-World Evidence networks to use routine healthcare data for safety checks, label updates, and rare-disease approvals.",\n        "technical": "FDA\'s 21st Century Cures RWE Program (and Advancing RWE Pilot) aligns with EMA\'s Data Analysis and Real World Interrogation Network (DARWIN EU), federated across OMOP-mapped European data partners.",\n        "url": "https://www.ema.europa.eu/en/about-us/how-we-work/data-analytics-and-methods/real-world-evidence",\n    },\n]\n\nDHT_DECENTRALIZED = [\n    {\n        "id": "dht-wearables",\n        "name": "Wearables, Continuous Sensors & Connected Devices",\n        "plain": "Smartwatches, continuous glucose monitors, adhesive ECG patches, and connected inhalers capture real-life patient health continuously at home instead of a 15-minute snapshot in a clinic.",\n        "technical": "FDA DHT Guidance covers wrist actigraphs, continuous glucose monitors (CGMs), digital spirometers, and smartphone vocal/gait sensors capturing high-frequency longitudinal data.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations",\n    },\n    {\n        "id": "dht-v3",\n        "name": "DHT Verification, Analytical Validation & Clinical Validation (V3)",\n        "plain": "Before a clinical trial trusts a smartwatch or sensor, developers prove the hardware measures accurately, the software translates signals into the right metric, and that metric reflects real patient health.",\n        "technical": "Three-part evidentiary framework: Verification (sensor bench accuracy), Analytical Validation (algorithm accuracy against reference standard like polysomnography), and Clinical Validation (meaningful link to disease state/outcomes).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations",\n    },\n    {\n        "id": "dht-dct",\n        "name": "Decentralized Clinical Trials (DCTs) & Hybrid Models",\n        "plain": "Brings clinical trials to patients\' homes through video visits, local blood-draw labs, mobile nurses, and direct-to-patient medication shipping—widening access for rural and busy patients.",\n        "technical": "FDA DCT Guidance defines investigator oversight over local HCPs, remote telehealth visits, direct-to-participant investigational product (IP) shipment under stability control, and hybrid site/remote workflows.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements",\n    },\n    {\n        "id": "dht-econsent-ecoa",\n        "name": "Electronic Informed Consent (eConsent) & ePRO / eCOA",\n        "plain": "Interactive digital consent forms with plain-language videos and smartphone symptom diaries that timestamp every patient entry immediately instead of relying on paper diaries filled out in the parking lot.",\n        "technical": "Eliminates \'parking-lot compliance\' via contemporaneous timestamped ePRO/eCOA capture under 21 CFR Parts 11 and 50, requiring bring-your-own-device (BYOD) equivalence or provisioned devices.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements",\n    },\n    {\n        "id": "dht-endpoints",\n        "name": "Novel Digital Endpoints (Stride Velocity, Nocturnal Scratch, TIR)",\n        "plain": "Continuous home sensors unlock brand-new ways to measure progress—such as walking speed in neuromuscular disease, nighttime scratching in eczema, or Time-in-Range (TIR) blood sugar.",\n        "technical": "Examples include EMA-qualified Stride Velocity 95th Centile (SV95C) as a primary/secondary endpoint in Duchenne muscular dystrophy, CGM Time-in-Range (70–180 mg/dL), and wrist-actigraphy nocturnal scratch.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations",\n    },\n    {\n        "id": "dht-part11",\n        "name": "DHT Data Integrity, Attribution & 21 CFR Part 11",\n        "plain": "Ensures data streamed from a patient\'s wrist or phone reaches the trial database securely, encrypted, and linked to the right participant without gaps or tampering.",\n        "technical": "Requires end-to-end encryption, durable source-data repositories, firmware/OS version-change impact assessments, and auditable metadata trails under 21 CFR Part 11 and ICH E6(R3).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11",\n    },\n]\n\nSAMD_AI = [\n    {\n        "id": "ai-samd",\n        "name": "Software as a Medical Device (SaMD) & IMDRF Risk Tiers",\n        "plain": "Standalone software—without any physical hardware of its own—that diagnoses, monitors, or treats a medical condition is regulated by the FDA just like a physical medical device.",\n        "technical": "IMDRF 4-tier risk matrix (Classes I–IV) crossing significance of information (Inform / Drive / Treat-Diagnose) with healthcare state (Non-serious / Serious / Critical), cleared via FDA 510(k), De Novo, or PMA.",\n        "url": "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices",\n    },\n    {\n        "id": "ai-pccp",\n        "name": "AI/ML-Enabled Devices & Predetermined Change Control Plans (PCCP)",\n        "plain": "Because AI software improves as it learns from new data, the FDA created a \'pre-approved upgrade plan\' (PCCP) so validated updates can roll out safely without filing a brand-new application every time.",\n        "technical": "Authorized by FDORA (2022), FDA\'s PCCP framework pre-specifies bounded model modifications, retraining protocols, and real-world performance guardrails alongside Good Machine Learning Practice (GMLP) principles.",\n        "url": "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices",\n    },\n    {\n        "id": "ai-pdt",\n        "name": "Prescription Digital Therapeutics (PDTs) & Drug–Software Pairs",\n        "plain": "Clinically tested software apps prescribed by a doctor—either alone or paired with a medicine—to deliver behavioral therapy or precision dosing support.",\n        "technical": "FDA-cleared SaMD apps requiring clinical trial evidence of efficacy (e.g., cognitive behavioral therapy for insomnia, substance use, or adjunctive depression care) and regulated promotional labeling (PDURS framework).",\n        "url": "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices",\n    },\n    {\n        "id": "ai-adherence",\n        "name": "Smart Inhalers, Connected Pens & Adherence Telemetry",\n        "plain": "Bluetooth caps and smart injector pens automatically log when a patient took a dose—helping doctors tell the difference between a medicine that isn\'t working and missed doses.",\n        "technical": "Combination-product connectivity (21 CFR Part 4) records timestamped actuation, inspiratory flow technique, and dose history to improve clinical trial adherence and chronic asthma/diabetes management.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations",\n    },\n    {\n        "id": "ai-drug-dev",\n        "name": "AI / ML in Drug Discovery, Trials & Pharmacovigilance",\n        "plain": "Pharmaceutical teams use machine learning to predict 3D protein shapes, design new molecules, match patients to clinical trials, and scan millions of safety reports for hidden patterns.",\n        "technical": "FDA\'s risk-based AI credibility framework assesses context of use (COU) and model risk across structure prediction, PK/PD modeling, trial site selection, automated MedDRA safety triage, and visual inspection.",\n        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",\n    },\n    {\n        "id": "ai-cyber-drift",\n        "name": "Medical Device Cybersecurity & Post-Market AI Drift Monitoring",\n        "plain": "Connected medical apps and AI models must be protected against hackers and monitored continuously after launch to make sure their accuracy never degrades on new hospital equipment or patient groups.",\n        "technical": "FDORA § 524B mandates Software Bills of Materials (SBOMs) and cybersecurity lifecycle plans for cyber devices; AI/ML models require ongoing post-market drift detection and subgroup fairness audits.",\n        "url": "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices",\n    },\n]\n\n\ndef build_rwe_dht(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on Real-World Data/Evidence (RWD/RWE), registries, Decentralized Clinical Trials (DCTs), Digital Health Technologies (DHTs), and AI/ML SaMD regulation (FDA, eCFR, EMA). Educational reference only.",\n        "rwd_sources": RWD_SOURCES,\n        "rwe_designs": RWE_DESIGNS,\n        "dht_decentralized": DHT_DECENTRALIZED,\n        "samd_ai": SAMD_AI,\n    }\n    (data_dir / "rwe_dht.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "rwd_sources": len(RWD_SOURCES),\n        "rwe_designs": len(RWE_DESIGNS),\n        "dht_decentralized": len(DHT_DECENTRALIZED),\n        "samd_ai": len(SAMD_AI),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_rwe_dht(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
RWE_DHT_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderRwePipelineSvg() {\n  const nodes = [\n    { x: 8, label: "1. RWD / Sensors", sub: "EHR / Claims / DHT" },\n    { x: 140, label: "2. Harmonize", sub: "OMOP / SCDM / PPRL" },\n    { x: 272, label: "3. Fit-for-Use", sub: "Reliability & V3" },\n    { x: 404, label: "4. Causal Design", sub: "Target Trial / IPTW" },\n    { x: 536, label: "5. Reg Evidence", sub: "Label / Safety / HTA" },\n  ];\n  return html`<figure class="rwe-flow" aria-label="Real-world data to regulatory real-world evidence pipeline">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 4 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 4 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Transforming routine clinical records and digital sensor streams into regulatory-grade Real-World Evidence (RWE).</figcaption>\n  </figure>`;\n}\n\nexport async function rweDhtPage(query, mode = "ref") {\n  const doc = await getJSON("data/rwe_dht.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/rwe" : "#/ref/rwe";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Real-World Evidence (RWE), Registries & Digital Health Technologies (DHTs)",\n    body: html`\n      <h1>Real-World Evidence (RWE), Registries &amp; Digital Health Technologies</h1>\n      <p class="lead">${mode === "explore"\n        ? "How everyday hospital records, patient registries, smartwatches, at-home trials, and medical AI help scientists study medicines faster and measure how well they work in real life."\n        : "Primary-sourced reference covering 6 RWD sources & Common Data Models, 6 regulatory RWE causal study designs, 6 DHT & Decentralized Trial frameworks, and 6 SaMD / AI-ML regulatory standards (checked " + doc.checked + ")."}</p>\n\n      ${renderRwePipelineSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=rwd"${sec === "rwd" ? \' aria-current="page"\' : ""}>RWD &amp; Registries (6)</a> ·\n        <a href="${base}?section=rwe"${sec === "rwe" ? \' aria-current="page"\' : ""}>RWE Causal Designs (6)</a> ·\n        <a href="${base}?section=dht"${sec === "dht" ? \' aria-current="page"\' : ""}>DHTs &amp; DCTs (6)</a> ·\n        <a href="${base}?section=ai"${sec === "ai" ? \' aria-current="page"\' : ""}>SaMD &amp; Medical AI (6)</a>\n      </p>\n\n      ${show("rwd") ? html`\n        <h2 id="rwd">1. Real-World Data (RWD) Sources &amp; Standards (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Real-world data sources">\n          <table class="tbl"><thead><tr><th>Data Source / Standard</th><th>${mode === "explore" ? "What It Captures" : "Data Fitness & Interoperability Standard"}</th></tr></thead>\n          <tbody>${(doc.rwd_sources || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b></td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("rwe") ? html`\n        <h2 id="rwe">2. Regulatory RWE Study Designs &amp; Bias Mitigation (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="RWE study designs">\n          <table class="tbl"><thead><tr><th>Design / Method</th><th>${mode === "explore" ? "Why It Matters" : "Causal Inference & Regulatory Criteria"}</th></tr></thead>\n          <tbody>${(doc.rwe_designs || []).map((d) => html`<tr id="${d.id}">\n            <td><b><a href="${d.url}" target="_blank" rel="noopener">${d.name}</a></b></td>\n            <td>${mode === "explore" ? d.plain : html`${d.plain}<br><span class="muted small">${d.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("dht") ? html`\n        <h2 id="dht">3. Digital Health Technologies (DHTs) &amp; Decentralized Trials (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Digital health technologies and DCTs">\n          <table class="tbl"><thead><tr><th>Technology / Pillar</th><th>${mode === "explore" ? "How It Helps Patients" : "Validation (V3), Oversight & Part 11"}</th></tr></thead>\n          <tbody>${(doc.dht_decentralized || []).map((t) => html`<tr id="${t.id}">\n            <td><b><a href="${t.url}" target="_blank" rel="noopener">${t.name}</a></b></td>\n            <td>${mode === "explore" ? t.plain : html`${t.plain}<br><span class="muted small">${t.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("ai") ? html`\n        <h2 id="ai">4. Software as a Medical Device (SaMD), AI/ML &amp; Digital Therapeutics (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="SaMD and medical AI">\n          <table class="tbl"><thead><tr><th>Regulatory Pillar</th><th>${mode === "explore" ? "How Software Is Regulated" : "FDA/IMDRF Classification, PCCP & Cybersecurity"}</th></tr></thead>\n          <tbody>${(doc.samd_ai || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/trials">Clinical Trials &amp; Endpoints</a> · <a href="#/ref/safety">Pharmacovigilance &amp; Sentinel</a> · <a href="#/ref/cdx">CDx &amp; Digital Biomarkers</a> · <a href="#/ref/software">Pharma Software Stack</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { rweDhtPage } from "./rwe_dht.js";\n'
    if "./rwe_dht.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/rwe"' not in txt:
        for anchor in ('if (path === "/ref/atmp")', 'if (path === "/ref/cdx")', 'if (path === "/ref/global-reg")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/rwe") return rweDhtPage(query, "ref");\n'
                    '  if (path === "/explore/rwe") return rweDhtPage(query, "explore");\n'
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
    if "#/ref/rwe" not in txt:
        for anchor in ('["#/ref/atmp", "Vaccines & cell/gene"]', '["#/ref/cdx", "CDx & precision medicine"]', '["#/ref/trials", "Clinical trials & endpoints"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/rwe", "RWE & digital health"]', 1)
                changed = True
                break
    if "#/explore/rwe" not in txt:
        for anchor in ('["#/explore/atmp", "Vaccines & cell/gene"]', '["#/explore/cdx", "CDx & precision medicine"]', '["#/explore/trials", "Clinical trials & endpoints"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/rwe", "RWE & digital health"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_rwe_dht.py" in txt:
        return False
    hook = "\n# v6.1q: Real-World Evidence (RWE), Registries & Digital Health Technologies (DHTs)\npython3 pipeline/build_rwe_dht.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/rwe"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/rwe")\n'
        'def api_rwe_dht():\n'
        '    return _read_json(SITE_DIR / "data" / "rwe_dht.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rwe_dht.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    rwe_ref = _load(data_dir / "rwe_dht.json", {}) or {}\n'
        '    for sec_key, sec_q in [("rwd_sources", "rwd"), ("rwe_designs", "rwe"), ("dht_decentralized", "dht"), ("samd_ai", "ai")]:\n'
        '        for item in (rwe_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "rwe_dht",\n'
        '                "group": "Real-World Evidence & Digital Health",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/rwe?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/rwe?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"real world evidence RWE RWD registry OMOP target trial DHT wearable DCT decentralized SaMD AI ML PCCP {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rwe", "#/ref/rwe"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    rwe_doc = _load_json(data_dir / "rwe_dht.json")\n'
        '    if isinstance(rwe_doc, dict) and rwe_doc.get("rwd_sources"):\n'
        '        r_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (rwe_doc.get("rwd_sources") or []) + (rwe_doc.get("dht_decentralized") or []))\n'
        '        pages.append(("rwe", "#/ref/rwe", "Real-World Evidence (RWE), Registries & Digital Health Technologies",\n'
        '                      "Primary-sourced guide to EHR/claims & registries, OMOP/SCDM Common Data Models, Target Trial Emulation, Decentralized Clinical Trials (DCTs), DHT V3 validation, and AI/ML SaMD PCCP.",\n'
        '                      f"<ul>{r_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/rwe"' in txt:
        return False
    for anchor in ('    "/#/explore/atmp",', '    "/#/explore/cdx",', '    "/#/explore/global-reg",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/rwe",\n    "/#/explore/rwe",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_rwe_dht_py": _write_if_changed(pipe_dir / "build_rwe_dht.py", BUILD_RWE_DHT_PY),
        "rwe_dht_js": _write_if_changed(js_dir / "rwe_dht.js", RWE_DHT_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/atmp") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/atmp", "Vaccines & cell/gene"]] }];\nconst EXPLORE_NAV = [["#/explore/atmp", "Vaccines & cell/gene"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/atmp",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_rwe_dht.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_rwe_dht.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"rwd_sources": 6, "rwe_designs": 6, "dht_decentralized": 6, "samd_ai": 6}, out

        doc = json.loads((root / "site" / "data" / "rwe_dht.json").read_text(encoding="utf-8"))
        for k in ("rwd_sources", "rwe_designs", "dht_decentralized", "samd_ai"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61Q_RWE_REGISTRIES_DIGITAL_HEALTH_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1q RWE, Registries & Digital Health Technologies patch.")
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
