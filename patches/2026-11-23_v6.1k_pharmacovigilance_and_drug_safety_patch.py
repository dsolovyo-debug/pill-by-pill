#!/usr/bin/env python3
"""Pill by Pill v6.1k Patch: Pharmacovigilance, Drug Safety & Post-Market Surveillance Reference (#/ref/safety, #/explore/safety, /api/safety).

1. Adds `pipeline/build_safety.py` -> `site/data/safety.json` (6 global PV systems, 6 signal
   detection & pharmacoepidemiology methods, 6 major organ toxicity frameworks, and 6 regulatory
   safety actions — 24 primary-sourced entries anchored to FDA/eCFR/EMA/PMDA/WHO/PMC).
2. Adds `site/js/safety.js` (`safetyPage` with inline signal-to-action SVG + 4 section filters)
   and wires `#/ref/safety`, `#/explore/safety`, `/api/safety`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `safety.json` into `pipeline/build_global_search.py`, `pipeline/build_v60_static_pages.py`
   (`/safety/` static SEO page + sitemap entry -> 27 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1k_pharmacovigilance_and_drug_safety_patch.py --selftest
  python3 2026-11-23_v6.1k_pharmacovigilance_and_drug_safety_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_SAFETY_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1k Pharmacovigilance, Drug Safety & Post-Market Surveillance dataset (`site/data/safety.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Global Pharmacovigilance & Surveillance Systems (6 systems: FDA AEMS/MedWatch, Sentinel, EMA EudraVigilance, UK Yellow Card, PMDA JADER, WHO VigiBase)\n  2. Signal Detection, Causality & Pharmacoepidemiology (6 methods: Spontaneous Reporting Limits, PRR/ROR/EBGM, Naranjo/WHO-UMC, Active RWE/SCCS, MedDRA/ICH E2B(R3), PSUR/PBRER/DSUR)\n  3. Major Organ Toxicities & Safety Biomarkers (6 frameworks: DILI/Hy\'s Law, hERG/QTc ICH E14, SCARs/HLA, Immunogenicity/CRS, PLLR/Teratogenicity, Genotoxicity/ICH M7/Nitrosamines)\n  4. Regulatory Safety Actions, REMS & Recall Anatomy (6 actions: Boxed Warnings, REMS ETASU, Recall Classes I–III, Safety Labeling Changes/DHCP, cGMP Safety Enforcement, LASA/Medication Errors)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, EMA, WHO, PMC).\n\nUsage:\n  python3 pipeline/build_safety.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nPV_SYSTEMS = [\n    {\n        "id": "pv-fda-aems",\n        "name": "US FDA AEMS (formerly FAERS) & MedWatch",\n        "region": "United States",\n        "plain": "The FDA\'s national safety inbox where doctors, patients, and drugmakers report suspected side effects so regulators can spot rare dangers after a medicine hits pharmacies.",\n        "technical": "In March 2026 FDA transitioned legacy FAERS to the Adverse Event Monitoring System (AEMS) with real-time daily reporting. Mandatory 15-day Alert Reports (21 CFR 314.80) cover serious, unexpected adverse experiences; voluntary reports enter via MedWatch Form 3500.",\n        "url": "https://www.fda.gov/drugs/surveillance-post-drug-approval-activities/fda-adverse-event-monitoring-system-aems",\n    },\n    {\n        "id": "pv-sentinel",\n        "name": "FDA Sentinel Initiative (Active Surveillance)",\n        "region": "United States",\n        "plain": "Instead of waiting for people to mail in side-effect reports, Sentinel actively scans anonymized electronic health records and insurance claims across tens of millions of patients.",\n        "technical": "Distributed data network mandated by FDAAA 2007 using the Sentinel Common Data Model (SCDM) to run rapid active-surveillance cohort and self-controlled analyses with true exposed denominators.",\n        "url": "https://www.fda.gov/safety/fdas-sentinel-initiative",\n    },\n    {\n        "id": "pv-eudravigilance",\n        "name": "EU EMA EudraVigilance, PRAC & Black Triangle (▼)",\n        "region": "European Union",\n        "plain": "Europe\'s central side-effect database, overseen by a dedicated safety committee (PRAC); brand-new medicines carry an inverted black triangle (▼) on their leaflets to encourage reporting.",\n        "technical": "Centralized EU ICSR database aligned to ICH E2B(R3); EMA\'s Pharmacovigilance Risk Assessment Committee (PRAC) evaluates signals, Risk Management Plans (RMPs), and Post-Authorisation Safety Studies (PASS).",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/pharmacovigilance-research-development/eudravigilance",\n    },\n    {\n        "id": "pv-yellow-card",\n        "name": "UK MHRA Yellow Card Scheme (1964)",\n        "region": "United Kingdom",\n        "plain": "One of the world\'s oldest medicine safety reporting systems, created in 1964 right after the thalidomide tragedy so clinicians and patients can flag suspected reactions quickly.",\n        "technical": "National spontaneous reporting system for medicines, vaccines, medical devices, and defective products operated by the UK MHRA.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10087031/",\n    },\n    {\n        "id": "pv-pmda-jader",\n        "name": "Japan PMDA JADER, All-Case Surveillance & ADR Relief",\n        "region": "Japan",\n        "plain": "Japan\'s safety database—unique for often requiring companies to track every single early patient taking a new drug and running a public relief fund for severe, unavoidable side effects.",\n        "technical": "Japanese Adverse Drug Event Report (JADER) database paired with Early Post-marketing Phase Vigilance (EPPV, first 6 months), mandatory All-Case Surveillance for selected novel drugs, and the PMDA ADR Relief System.",\n        "url": "https://www.pmda.go.jp/english/safety/info-services/drugs/0001.html",\n    },\n    {\n        "id": "pv-who-vigibase",\n        "name": "WHO PIDM & Uppsala Monitoring Centre (VigiBase)",\n        "region": "Global (170+ countries)",\n        "plain": "A global safety network run out of Uppsala, Sweden, that pools side-effect reports from over 170 countries to catch rare worldwide patterns faster than any single country could alone.",\n        "technical": "Established in 1968 under the WHO Programme for International Drug Monitoring (PIDM); VigiBase houses tens of millions of ICSRs analyzed with Bayesian disproportionality (Information Component, IC).",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13160990/",\n    },\n]\n\nSIGNAL_METHODS = [\n    {\n        "id": "sig-spontaneous-limits",\n        "name": "Spontaneous Reporting Limitations (No True Denominator)",\n        "plain": "A pile of side-effect reports cannot tell you how common a reaction is—because you don\'t know how many millions of people took the pill safely or how many reactions went unreported.",\n        "technical": "Spontaneous systems suffer from under-reporting, stimulated reporting (media/notoriety bias), the Weber effect (peak reporting in year 2 post-launch), and lack of an exact exposed denominator—hence counts cannot establish incidence or prove causation.",\n        "url": "https://www.fda.gov/drugs/surveillance-post-drug-approval-activities/fda-adverse-event-monitoring-system-aems",\n    },\n    {\n        "id": "sig-disproportionality",\n        "name": "Quantitative Signal Detection (PRR, ROR, EBGM & IC)",\n        "plain": "Safety scientists use math to ask: \'Is this side effect showing up way more often with Drug X than with all other drugs in the database?\'",\n        "technical": "2×2 contingency-table disproportionality analyses: frequentist Proportional Reporting Ratio (PRR) and Reporting Odds Ratio (ROR), plus Bayesian shrinkage estimators (Multi-item Gamma Poisson Shrinker / EBGM at FDA; Information Component / IC at WHO-UMC).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-pharmacovigilance-practices-and-pharmacoepidemiologic-assessment",\n    },\n    {\n        "id": "sig-causality",\n        "name": "Causality Assessment (Naranjo, WHO-UMC & Bradford Hill)",\n        "plain": "Just because a symptom happened after taking a pill doesn\'t mean the pill caused it. Experts check timing, whether stopping the drug helps (dechallenge), and whether restarting brings it back (rechallenge).",\n        "technical": "Structured case-level causality via WHO-UMC categories (Certain, Probable, Possible, Unlikely) and the Naranjo Adverse Drug Reaction Probability Scale, complemented at population scale by Bradford Hill criteria.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-pharmacovigilance-practices-and-pharmacoepidemiologic-assessment",\n    },\n    {\n        "id": "sig-rwe-sccs",\n        "name": "Active Pharmacoepidemiology (Cohort, Case-Control & SCCS)",\n        "plain": "Once a warning signal appears, researchers test it in real hospital records—including designs where each patient is compared against themselves during exposed vs. unexposed months.",\n        "technical": "New-user active-comparator cohort designs (with propensity-score matching to limit confounding by indication), nested case-control studies, and Self-Controlled Case Series (SCCS) controlling time-invariant confounders.",\n        "url": "https://www.fda.gov/science-research/science-and-research-special-topics/real-world-evidence",\n    },\n    {\n        "id": "sig-meddra-e2b",\n        "name": "MedDRA Coding & ICH E2B(R3) Electronic Exchange",\n        "plain": "A standardized medical dictionary ensures that \'hives\', \'welts\', and \'urticaria\' reported in different countries are grouped under one exact term so computers don\'t miss a pattern.",\n        "technical": "Medical Dictionary for Regulatory Activities (MedDRA) 5-level hierarchy (SOC -> HLGT -> HLT -> Preferred Term -> Lowest Level Term) transmitted via ICH E2B(R3) XML Individual Case Safety Reports (ICSRs).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2br3-electronic-transmission-individual-case-safety-reports-icsrs-implementation-guide-data",\n    },\n    {\n        "id": "sig-aggregate",\n        "name": "Aggregate Benefit-Risk Reports (DSUR, PSUR / PBRER & RMP)",\n        "plain": "Drugmakers must regularly step back and submit full \'report cards\' weighing all new safety findings against the medicine\'s proven benefits.",\n        "technical": "Development Safety Update Report (DSUR, ICH E2F) during clinical trials; Periodic Benefit-Risk Evaluation Report (PBRER/PSUR, ICH E2C(R2)) and Periodic Adverse Drug Experience Report (PADER, 21 CFR 314.80) post-approval.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2cr2-periodic-benefit-risk-evaluation-report",\n    },\n]\n\nORGAN_TOXICITIES = [\n    {\n        "id": "tox-dili-hys-law",\n        "name": "Drug-Induced Liver Injury (DILI) & Hy\'s Law",\n        "plain": "Because the liver processes most oral medicines, liver injury is a top reason drugs fail or get pulled. \'Hy\'s Law\' flags a dangerous combo of liver-cell breakdown plus yellowing jaundice.",\n        "technical": "FDA DILI Guidance defines Hy\'s Law as: (1) hepatocellular injury (ALT or AST >3× ULN), (2) total bilirubin >2× ULN without cholestasis (ALP <2× ULN), and (3) no alternative explanation—predicting >=10% risk of fatal liver failure or transplant.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/drug-induced-liver-injury-premarketing-clinical-evaluation",\n    },\n    {\n        "id": "tox-herg-qtc",\n        "name": "Cardiac Safety: hERG Blockade & QTc Prolongation (ICH S7B / E14)",\n        "plain": "Certain molecules accidentally plug a potassium channel in heart muscle (hERG), stretching the heart\'s electrical recharge time (QT interval) and risking a dangerous rhythm called Torsades de Pointes.",\n        "technical": "Preclinical hERG patch-clamp and telemetry (ICH S7B) paired with clinical Thorough QT/QTc (TQT) or concentration-QTc modeling (ICH E14) checking whether upper 90% CI of ddQTc exceeds 10 ms.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e14-clinical-evaluation-qtqtc-interval-prolongation-and-proarrhythmic-potential-non-antiarrhythmic",\n    },\n    {\n        "id": "tox-scars-hla",\n        "name": "Severe Cutaneous Adverse Reactions (SCARs: SJS/TEN & DRESS)",\n        "plain": "Rare but life-threatening immune skin reactions triggered by specific drugs—some of which can now be prevented by a simple genetic blood test before taking the first pill.",\n        "technical": "Stevens-Johnson Syndrome (SJS), Toxic Epidermal Necrolysis (TEN), and DRESS are T-cell-mediated hypersensitivities strongly linked to HLA alleles (e.g., HLA-B*57:01 for abacavir; HLA-B*15:02 for carbamazepine).",\n        "url": "https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling",\n    },\n    {\n        "id": "tox-immunogenicity-crs",\n        "name": "Biologic Immunogenicity, Infusion Reactions & CRS / ICANS",\n        "plain": "Because antibodies and engineered CAR-T cells are large proteins or living cells, the immune system can attack them or trigger an intense inflammatory \'cytokine storm\' that hospitals monitor closely.",\n        "technical": "Anti-drug antibodies (ADAs) and neutralizing antibodies (NAbs) can alter PK/efficacy or cause anaphylaxis; T-cell engagers and CAR-T therapies carry structured Cytokine Release Syndrome (CRS) and neurotoxicity (ICANS) grading and tocilizumab rescue protocols.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/immunogenicity-testing-therapeutic-protein-products-developing-and-validating-assays-anti-drug",\n    },\n    {\n        "id": "tox-teratogenicity-pllr",\n        "name": "Teratogenicity, Embryo-Fetal Risk & FDA PLLR",\n        "plain": "Lessons from thalidomide led to strict reproductive safety testing and modern pregnancy labels that explain real human and animal data in plain narrative instead of confusing A–X letter grades.",\n        "technical": "ICH S5(R3) reproductive/developmental toxicology paired with the 2014 Pregnancy and Lactation Labeling Rule (PLLR, 21 CFR 201.57) replacing legacy A/B/C/D/X categories with Pregnancy Exposure Registry and Risk Summary narratives.",\n        "url": "https://www.fda.gov/drugs/labeling-information-drug-products/pregnancy-and-lactation-labeling-drugs-final-rule",\n    },\n    {\n        "id": "tox-genotox-nitrosamines",\n        "name": "Genotoxicity, Mutagenic Impurities & Nitrosamines (ICH M7)",\n        "plain": "Even trace chemical impurities left over from manufacturing must be kept below tiny parts-per-billion limits so they cannot damage DNA over years of daily pill use.",\n        "technical": "ICH S2(R1) genotoxicity battery (Ames, micronucleus) plus ICH M7(R2) Threshold of Toxicological Concern (TTC = 1.5 µg/day) and FDA\'s Acceptable Intake (AI) limits for N-nitrosamine drug substance-related impurities (NDSRIs).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/control-nitrosamine-impurities-human-drugs",\n    },\n]\n\nREGULATORY_ACTIONS = [\n    {\n        "id": "act-boxed-warning",\n        "name": "Boxed Warning (\'Black Box\') vs. Contraindication",\n        "plain": "A bold black border at the very top of a prescribing label alerts doctors and patients to the most serious or life-threatening risks—while a Contraindication means \'never use in this group.\'",\n        "technical": "Defined under 21 CFR 201.57(c)(1) for serious adverse reactions that can be fatal or life-threatening, or prevented/reduced by patient selection, monitoring, or avoiding concomitant drugs.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-201",\n    },\n    {\n        "id": "act-rems-etasu",\n        "name": "FDA REMS & Elements to Assure Safe Use (ETASU)",\n        "plain": "For high-risk but essential medicines, FDA can require extra safety guardrails—like certified doctors, mandatory blood tests, or special pharmacy registries—before a prescription is dispensed.",\n        "technical": "Authorized under FD&C Act § 505-1; escalates from Medication Guides and Communication Plans to ETASU (prescriber/pharmacy certification, safe-use documentation such as negative pregnancy tests or ANC lab checks, patient registries).",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/risk-evaluation-and-mitigation-strategies-rems",\n    },\n    {\n        "id": "act-recalls",\n        "name": "FDA Drug Recall Classes I, II & III (21 CFR Part 7)",\n        "plain": "When a batch has a defect—like glass particles, failed sterility, or a misprinted label—it is pulled from shelves under Class I (most dangerous), Class II (reversible harm), or Class III (minor defect).",\n        "technical": "Class I: reasonable probability of serious adverse health consequences or death; Class II: temporary or medically reversible health consequences; Class III: unlikely to cause adverse health consequences.",\n        "url": "https://www.fda.gov/drugs/drug-recalls/understanding-drug-recalls-what-know-and-what-do",\n    },\n    {\n        "id": "act-slc-dhcp",\n        "name": "Safety Labeling Changes (SLC) & Dear Healthcare Provider Letters",\n        "plain": "When new post-market risks emerge, FDA can order drugmakers to update warning labels and send direct urgent safety alerts to doctors and pharmacists.",\n        "technical": "FDAAA Section 901 empowers FDA to mandate Safety Labeling Changes (SLCs) based on new safety information, supported by Drug Safety Communications (DSCs) and Dear Healthcare Provider (DHCP) letters.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-communications",\n    },\n    {\n        "id": "act-cgmp-enforcement",\n        "name": "Factory Safety Enforcement (Form 483, Warning Letters & Import Alerts)",\n        "plain": "Safety isn\'t just about the molecule—if a factory fails sterility or data-integrity checks, FDA can issue public Warning Letters or block shipments at the border.",\n        "technical": "FDA OII inspections yielding Official Action Indicated (OAI) can trigger Warning Letters, Import Alerts (detention without physical examination), consent decrees, or NDA/BLA approval holds (cross-linked to #/ref/vendors).",\n        "url": "https://datadashboard.fda.gov/oii/cd/inspections.htm",\n    },\n    {\n        "id": "act-lasa-human-factors",\n        "name": "Medication Errors, LASA Names & Human Factors (DMEPA)",\n        "plain": "Before approving a brand name or injector pen, FDA tests whether the name sounds too much like another drug or if patients could accidentally misread the dose.",\n        "technical": "FDA\'s Division of Medication Error Prevention and Analysis (DMEPA) evaluates Look-Alike/Sound-Alike (LASA) proprietary names (POCA scoring), Tall Man Lettering (e.g., hydrOXYzine vs. hydrALAZINE), and human-factors usability validation.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/medication-errors-related-cder-regulated-drug-products",\n    },\n]\n\n\ndef build_safety(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on global pharmacovigilance, signal detection, organ toxicities, REMS, and drug recalls (FDA, eCFR, EMA, PMDA, WHO). Educational reference only—not medical advice.",\n        "pv_systems": PV_SYSTEMS,\n        "signal_methods": SIGNAL_METHODS,\n        "organ_toxicities": ORGAN_TOXICITIES,\n        "regulatory_actions": REGULATORY_ACTIONS,\n    }\n    (data_dir / "safety.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "pv_systems": len(PV_SYSTEMS),\n        "signal_methods": len(SIGNAL_METHODS),\n        "organ_toxicities": len(ORGAN_TOXICITIES),\n        "regulatory_actions": len(REGULATORY_ACTIONS),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_safety(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
SAFETY_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderSafetyLoopSvg() {\n  const nodes = [\n    { x: 8, label: "1. Report Intake", sub: "AEMS / MedWatch" },\n    { x: 140, label: "2. MedDRA Code", sub: "ICH E2B(R3)" },\n    { x: 272, label: "3. Signal Detect", sub: "PRR / EBGM / IC" },\n    { x: 404, label: "4. Active Verify", sub: "Sentinel / RWE" },\n    { x: 536, label: "5. Safety Action", sub: "Label / REMS / Recall" },\n  ];\n  return html`<figure class="safety-flow" aria-label="Post-market pharmacovigilance signal-to-action loop">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 4 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 4 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Continuous post-market pharmacovigilance lifecycle from adverse-event intake to regulatory risk mitigation.</figcaption>\n  </figure>`;\n}\n\nexport async function safetyPage(query, mode = "ref") {\n  const doc = await getJSON("data/safety.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/safety" : "#/ref/safety";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Pharmacovigilance, Drug Safety & Post-Market Surveillance",\n    body: html`\n      <h1>Pharmacovigilance, Drug Safety &amp; Post-Market Surveillance</h1>\n      <p class="lead">${mode === "explore"\n        ? "How regulators and scientists keep watching medicines after approval—catching rare side effects, protecting the liver and heart, requiring extra safety programs, and issuing recalls when batches go wrong."\n        : "Primary-sourced reference covering 6 global surveillance systems, 6 signal-detection & pharmacoepidemiology frameworks, 6 major organ toxicity standards, and 6 regulatory safety actions (checked " + doc.checked + ")."}</p>\n\n      ${renderSafetyLoopSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=systems"${sec === "systems" ? \' aria-current="page"\' : ""}>Global PV Systems (6)</a> ·\n        <a href="${base}?section=signals"${sec === "signals" ? \' aria-current="page"\' : ""}>Signal Detection (6)</a> ·\n        <a href="${base}?section=toxicities"${sec === "toxicities" ? \' aria-current="page"\' : ""}>Organ Toxicities (6)</a> ·\n        <a href="${base}?section=actions"${sec === "actions" ? \' aria-current="page"\' : ""}>REMS, Labels &amp; Recalls (6)</a>\n      </p>\n\n      ${show("systems") ? html`\n        <h2 id="systems">1. Global Pharmacovigilance &amp; Surveillance Systems (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Global pharmacovigilance systems">\n          <table class="tbl"><thead><tr><th>System</th><th>Region</th><th>${mode === "explore" ? "How It Protects Patients" : "Architecture & Legal Basis"}</th></tr></thead>\n          <tbody>${(doc.pv_systems || []).map((s) => html`<tr id="${s.id}">\n            <td><b><a href="${s.url}" target="_blank" rel="noopener">${s.name}</a></b></td>\n            <td>${s.region}</td>\n            <td>${mode === "explore" ? s.plain : html`${s.plain}<br><span class="muted small">${s.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("signals") ? html`\n        <h2 id="signals">2. Signal Detection, Causality &amp; Pharmacoepidemiology (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Signal detection and pharmacoepidemiology">\n          <table class="tbl"><thead><tr><th>Method / Standard</th><th>${mode === "explore" ? "Plain-Language Meaning" : "Plain & Technical Standard"}</th></tr></thead>\n          <tbody>${(doc.signal_methods || []).map((m) => html`<tr id="${m.id}">\n            <td><b><a href="${m.url}" target="_blank" rel="noopener">${m.name}</a></b></td>\n            <td>${mode === "explore" ? m.plain : html`${m.plain}<br><span class="muted small">${m.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("toxicities") ? html`\n        <h2 id="toxicities">3. Major Organ Toxicities &amp; Safety Biomarkers (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Major organ toxicities">\n          <table class="tbl"><thead><tr><th>Toxicity Framework</th><th>${mode === "explore" ? "Why Scientists Watch For It" : "Clinical Thresholds & Regulatory Guidance"}</th></tr></thead>\n          <tbody>${(doc.organ_toxicities || []).map((t) => html`<tr id="${t.id}">\n            <td><b><a href="${t.url}" target="_blank" rel="noopener">${t.name}</a></b></td>\n            <td>${mode === "explore" ? t.plain : html`${t.plain}<br><span class="muted small">${t.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("actions") ? html`\n        <h2 id="actions">4. Regulatory Safety Actions, REMS &amp; Recall Anatomy (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Regulatory safety actions">\n          <table class="tbl"><thead><tr><th>Regulatory Action</th><th>${mode === "explore" ? "What It Does" : "Statutory Mechanism & Scope"}</th></tr></thead>\n          <tbody>${(doc.regulatory_actions || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/departments/distribution">Stage 8: Supply Chain &amp; Safety</a> · <a href="#/ref/vendors">FDA/EMA Facility Audits</a> · <a href="#/ref/trials">Clinical Trials &amp; Endpoints</a> · <a href="#/ref/adme">ADME/PK &amp; DDIs</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { safetyPage } from "./safety.js";\n'
    if "./safety.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/safety"' not in txt:
        for anchor in ('if (path === "/ref/adme")', 'if (path === "/ref/trials")', 'if (path === "/ref/pathways")', 'if (path === "/ref/classes")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/safety") return safetyPage(query, "ref");\n'
                    '  if (path === "/explore/safety") return safetyPage(query, "explore");\n'
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
    if "#/ref/safety" not in txt:
        for anchor in ('["#/ref/adme", "ADME/PK & delivery"]', '["#/ref/trials", "Clinical trials & endpoints"]', '["#/ref/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/safety", "Drug safety & PV"]', 1)
                changed = True
                break
    if "#/explore/safety" not in txt:
        for anchor in ('["#/explore/adme", "ADME/PK & delivery"]', '["#/explore/trials", "Clinical trials & endpoints"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/safety", "Drug safety & PV"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_safety.py" in txt:
        return False
    hook = "\n# v6.1k: Pharmacovigilance, Drug Safety & Post-Market Surveillance Reference\npython3 pipeline/build_safety.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/safety"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/safety")\n'
        'def api_safety():\n'
        '    return _read_json(SITE_DIR / "data" / "safety.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"safety.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    sf_ref = _load(data_dir / "safety.json", {}) or {}\n'
        '    for sec_key, sec_q in [("pv_systems", "systems"), ("signal_methods", "signals"), ("organ_toxicities", "toxicities"), ("regulatory_actions", "actions")]:\n'
        '        for item in (sf_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "drug_safety",\n'
        '                "group": "Pharmacovigilance & Drug Safety",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/safety?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/safety?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"pharmacovigilance drug safety {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')} {item.get(\'region\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"safety", "#/ref/safety"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    sf_doc = _load_json(data_dir / "safety.json")\n'
        '    if isinstance(sf_doc, dict) and sf_doc.get("pv_systems"):\n'
        '        sf_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (sf_doc.get("pv_systems") or []) + (sf_doc.get("organ_toxicities") or []))\n'
        '        pages.append(("safety", "#/ref/safety", "Pharmacovigilance, Drug Safety & Post-Market Surveillance",\n'
        '                      "Primary-sourced guide to global pharmacovigilance (FDA AEMS, Sentinel, EMA EudraVigilance, VigiBase), PRR/ROR/EBGM signal detection, DILI/Hy\'s Law, hERG/QTc, REMS ETASU, and FDA Recall Classes I–III.",\n'
        '                      f"<ul>{sf_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/safety"' in txt:
        return False
    for anchor in ('    "/#/explore/adme",', '    "/#/explore/trials",', '    "/#/explore/pathways",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/safety",\n    "/#/explore/safety",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_safety_py": _write_if_changed(pipe_dir / "build_safety.py", BUILD_SAFETY_PY),
        "safety_js": _write_if_changed(js_dir / "safety.js", SAFETY_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/adme") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/adme", "ADME/PK & delivery"]] }];\nconst EXPLORE_NAV = [["#/explore/adme", "ADME/PK & delivery"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/adme",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_safety.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_safety.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"pv_systems": 6, "signal_methods": 6, "organ_toxicities": 6, "regulatory_actions": 6}, out

        doc = json.loads((root / "site" / "data" / "safety.json").read_text(encoding="utf-8"))
        for k in ("pv_systems", "signal_methods", "organ_toxicities", "regulatory_actions"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61K_PHARMACOVIGILANCE_SAFETY_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1k Pharmacovigilance & Drug Safety patch.")
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
