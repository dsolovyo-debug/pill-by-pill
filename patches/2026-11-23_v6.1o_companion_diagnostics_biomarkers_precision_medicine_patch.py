#!/usr/bin/env python3
"""Pill by Pill v6.1o Patch: Companion Diagnostics (CDx), Biomarkers & Precision Medicine Reference (#/ref/cdx, #/explore/cdx, /api/cdx).

1. Adds `pipeline/build_cdx.py` -> `site/data/cdx.json` (6 FDA-NIH BEST biomarker pillars,
   6 diagnostic assay platforms including IHC/FISH/NGS/ctDNA, 6 FDA/EU CDx co-development &
   LDT/CLIA regulatory frameworks, and 6 pharmacogenomics/CPIC/CMS reimbursement pillars — 24 entries).
2. Adds `site/js/cdx.js` (`cdxPage` with inline Drug-Diagnostic Co-Development SVG + 4 section
   filters) and wires `#/ref/cdx`, `#/explore/cdx`, `/api/cdx`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `cdx.json` into `pipeline/build_global_search.py`, `pipeline/build_v60_static_pages.py`
   (`/cdx/` static SEO page + sitemap entry -> 31 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1o_companion_diagnostics_biomarkers_precision_medicine_patch.py --selftest
  python3 2026-11-23_v6.1o_companion_diagnostics_biomarkers_precision_medicine_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_CDX_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1o Companion Diagnostics (CDx), Biomarkers & Precision Medicine Reference (`site/data/cdx.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Biomarker Taxonomy & FDA-NIH BEST Framework (6 pillars: Diagnostic/Predictive, Prognostic/Monitoring, PD/Safety, FDA BQP Qualification, Tissue-Agnostic Approvals, Digital/Quantitative Biomarkers)\n  2. Diagnostic Technologies & Assay Platforms (6 platforms: IHC/FISH, PCR/ddPCR, Tissue NGS/CGP, Liquid Biopsy/ctDNA, Mass Spec/Proteomics, AI Digital Pathology/Multi-Omics)\n  3. Regulatory Co-Development: FDA CDx, PMA, 510(k) & LDTs (6 frameworks: Companion vs. Complementary Diagnostics, Contemporaneous Co-Development, IVD PMA/De Novo/510(k), Analytical vs. Clinical Validation, LDTs & CLIA, EU IVDR)\n  4. Pharmacogenomics (PGx), Clinical Implementation & Access (6 pillars: FDA PGx Tables, CPIC/DPWG Dosing Guidelines, Germline vs. Somatic Testing, Molecular Tumor Boards & EHR Alerts, CMS NGS NCD 90.2 & MolDX Reimbursement, Genomic Equity & Reference Diversity)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, NIH/NCBI, CMS, EU, PMC).\n\nUsage:\n  python3 pipeline/build_cdx.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nBIOMARKER_TAXONOMY = [\n    {\n        "id": "bm-predictive",\n        "name": "Predictive & Diagnostic Biomarkers (Patient Selection)",\n        "plain": "Tests that check whether a patient\'s tumor or biology has the exact target a precision medicine is designed to hit—sparing non-responders from needless side effects and cost.",\n        "technical": "Under the FDA-NIH BEST Resource, diagnostic biomarkers confirm disease presence/subtype while predictive biomarkers identify individuals more likely to experience a favorable or unfavorable effect from a specific therapy (e.g., HER2, EGFR del19/L858R/T790M, ALK, BRAF V600E, PD-L1).",\n        "url": "https://www.ncbi.nlm.nih.gov/books/NBK326791/",\n    },\n    {\n        "id": "bm-prognostic-monitoring",\n        "name": "Prognostic & Monitoring Biomarkers (MRD / ctDNA)",\n        "plain": "Measures that predict how aggressive a disease is likely to be or track tiny traces of leftover cancer DNA in the blood months before a CT scan can see a relapse.",\n        "technical": "Prognostic biomarkers estimate likelihood of clinical events independent of therapy; monitoring biomarkers are measured serially to assess disease status or Minimal Residual Disease (MRD) via flow cytometry, NGS, or ctDNA.",\n        "url": "https://www.ncbi.nlm.nih.gov/books/NBK326791/",\n    },\n    {\n        "id": "bm-pd-safety",\n        "name": "Pharmacodynamic (Response) & Safety Biomarkers",\n        "plain": "Shows whether a medicine actually flipped its biological switch inside the body—or flags a genetic risk of a severe side effect before the patient takes the first pill.",\n        "technical": "PD/response biomarkers prove biological target engagement (e.g., HbA1c, INR, serum TTR knockdown); safety biomarkers detect or predict toxicity (e.g., HLA-B*57:01 for abacavir hypersensitivity, ALT/bilirubin for DILI).",\n        "url": "https://www.ncbi.nlm.nih.gov/books/NBK326791/",\n    },\n    {\n        "id": "bm-fda-bqp",\n        "name": "FDA Biomarker Qualification Program (BQP)",\n        "plain": "A formal FDA pathway that lets academic consortia and drugmakers get a shared biomarker officially certified once so any future clinical trial can rely on it.",\n        "technical": "Three-stage 21st Century Cures Act process (Letter of Intent -> Qualification Plan -> Full Qualification Package) qualifying a Drug Development Tool (DDT) for a defined Context of Use (COU).",\n        "url": "https://www.fda.gov/drugs/drug-development-tool-ddt-qualification-programs/biomarker-qualification-program",\n    },\n    {\n        "id": "bm-tissue-agnostic",\n        "name": "Tissue-Agnostic (Site-Agnostic) Biomarker Approvals",\n        "plain": "Instead of approving a cancer drug only for lung or breast cancer, regulators approve it for any solid tumor anywhere in the body that carries a specific genetic signature.",\n        "technical": "Pioneered by pembrolizumab for MSI-H/dMMR tumors (2017) and expanded to NTRK fusions (larotrectinib, entrectinib), TMB-H, BRAF V600E, RET fusions, and HER2-positive (IHC 3+) solid tumors via basket trials.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/tissue-agnostic-drug-development-oncology",\n    },\n    {\n        "id": "bm-digital",\n        "name": "Quantitative Imaging & Digital Biomarkers (DHTs)",\n        "plain": "Uses wearables, smartphone sensors, or standardized medical scans to measure walking speed, tremor, heart rhythm, or lung function continuously in daily life.",\n        "technical": "FDA Digital Health Technologies (DHTs) Guidance defines verification, analytical validation, and clinical validation for remote continuous endpoints in clinical investigations.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/digital-health-technologies-remote-data-acquisition-clinical-investigations",\n    },\n]\n\nASSAY_PLATFORMS = [\n    {\n        "id": "assay-ihc-fish",\n        "name": "Immunohistochemistry (IHC) & In Situ Hybridization (FISH)",\n        "plain": "Stains thin slices of tumor biopsy tissue with glowing antibodies or DNA probes under a microscope to see how much target protein is present or whether a gene is amplified.",\n        "technical": "Workhorse pathology platforms for protein expression scoring (e.g., HER2 IHC 0/1+/2+/3+ including HER2-low/ultralow, PD-L1 TPS/CPS) and chromosomal rearrangements/amplifications (HER2 FISH, ALK/ROS1).",\n        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-cleared-or-approved-companion-diagnostic-devices-in-vitro-and-imaging-tools",\n    },\n    {\n        "id": "assay-pcr",\n        "name": "Real-Time PCR & Digital Droplet PCR (ddPCR)",\n        "plain": "Rapidly amplifies specific stretches of DNA or RNA to detect known hotspot mutations or viral loads in hours with high sensitivity and low cost.",\n        "technical": "Quantitative RT-PCR and ddPCR deliver rapid turnaround and ultra-low limits of detection for targeted single-gene variants (EGFR, BRAF, KRAS, BCR-ABL1 monitoring) and gene-therapy vector copy number.",\n        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-cleared-or-approved-companion-diagnostic-devices-in-vitro-and-imaging-tools",\n    },\n    {\n        "id": "assay-ngs-tissue",\n        "name": "Tissue Next-Generation Sequencing (NGS / CGP)",\n        "plain": "Reads hundreds of cancer genes simultaneously from a single biopsy sample so doctors don\'t burn through precious tissue running one single-gene test at a time.",\n        "technical": "Comprehensive Genomic Profiling (CGP) panels (e.g., FoundationOne CDx, MSK-IMPACT) detect SNVs, indels, copy-number alterations, gene fusions, MSI, and Tumor Mutational Burden (TMB) in one workflow.",\n        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-cleared-or-approved-companion-diagnostic-devices-in-vitro-and-imaging-tools",\n    },\n    {\n        "id": "assay-liquid-biopsy",\n        "name": "Liquid Biopsy & Circulating Tumor DNA (ctDNA)",\n        "plain": "A simple blood draw that captures tiny fragments of tumor DNA shed into the bloodstream—useful when a tissue biopsy is too risky or to track emerging drug-resistance mutations.",\n        "technical": "Cell-free DNA (cfDNA/ctDNA) NGS assays (e.g., Guardant360 CDx, FoundationOne Liquid CDx) detect actionable mutations and resistance clones non-invasively; negative liquid results often reflex to tissue testing due to variable tumor shedding.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-circulating-tumor-deoxyribonucleic-acid-early-stage-solid-tumor-drug-development-draft-guidance",\n    },\n    {\n        "id": "assay-ms-proteomics",\n        "name": "Clinical Mass Spectrometry, Proteomics & Metabolomics",\n        "plain": "Measures exact drug levels, hormone panels, or protein signatures directly in blood or tissue without relying on antibody stains that can cross-react.",\n        "technical": "LC-MS/MS and affinity proteomics enable multiplexed protein biomarker quantitation, therapeutic drug monitoring (TDM), and newborn screening for inherited metabolic disorders.",\n        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/precision-medicine",\n    },\n    {\n        "id": "assay-ai-pathology",\n        "name": "AI-Assisted Digital Pathology & Spatial Multi-Omics",\n        "plain": "Software trained on tens of thousands of digitized biopsy slides helps pathologists score subtle protein patterns consistently and map how immune cells interact inside tumors.",\n        "technical": "Whole-slide imaging (WSI) combined with FDA-cleared/SaMD computer-aided pathology algorithms reduces inter-pathologist scoring variability (e.g., continuous HER2-low/PD-L1 quantitation) alongside spatial transcriptomics.",\n        "url": "https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices",\n    },\n]\n\nREGULATORY_CODEV = [\n    {\n        "id": "cdx-vs-comp",\n        "name": "Companion Diagnostic (CDx) vs. Complementary Diagnostic",\n        "plain": "A Companion Diagnostic is legally required on the drug label before prescribing; a Complementary Diagnostic gives helpful extra context on who benefits most, without being strictly mandatory.",\n        "technical": "FDA CDx Guidance defines an IVD companion diagnostic as essential for the safe and effective use of a corresponding therapeutic product (named in Indications & Usage); complementary diagnostics inform benefit-risk without restricting eligibility.",\n        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/companion-diagnostics",\n    },\n    {\n        "id": "cdx-codev",\n        "name": "Contemporaneous Drug–Diagnostic Co-Development",\n        "plain": "Drugmakers and diagnostic companies develop the medicine and its matching test side-by-side so both win FDA approval on the exact same day.",\n        "technical": "Joint coordination between FDA CDER/CBER (NDA/BLA) and CDRH (PMA/510(k)), using Investigational Device Exemptions (IDE, 21 CFR Part 812) for significant-risk clinical trial assays (CTAs) and concordance bridging studies if the commercial CDx differs from the trial assay.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/principles-codevelopment-in-vitro-companion-diagnostic-device-therapeutic-product",\n    },\n    {\n        "id": "cdx-pma-510k",\n        "name": "FDA IVD Pathways: PMA (Class III), De Novo & 510(k) (Class II)",\n        "plain": "High-risk tests that decide whether a cancer patient gets a life-saving targeted drug must pass the FDA\'s toughest medical-device approval (PMA), while lower-risk tests use De Novo or 510(k) clearance.",\n        "technical": "Most oncology CDx assays are Class III devices requiring Premarket Approval (PMA, 21 CFR Part 814) with clinical safety/effectiveness evidence and manufacturing inspection; moderate-risk IVDs use 510(k) substantial equivalence (21 CFR Part 807) or De Novo classification.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-814",\n    },\n    {\n        "id": "cdx-validation",\n        "name": "Analytical Validation vs. Clinical Validation & Utility",\n        "plain": "First the lab proves the test measures the biomarker accurately every time (analytical); next clinical trials prove that picking patients with the test actually improves health outcomes (clinical).",\n        "technical": "Analytical validation establishes Limit of Detection (LoD), precision/reproducibility, accuracy, and interfering substances; clinical validation establishes diagnostic sensitivity, specificity, PPV/NPV, and clinical utility in target populations.",\n        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/companion-diagnostics",\n    },\n    {\n        "id": "cdx-ldt-clia",\n        "name": "Laboratory Developed Tests (LDTs) & CLIA Oversight",\n        "plain": "Many hospital and specialty labs build their own in-house genetic tests under federal lab quality rules (CLIA) rather than buying an FDA-approved kit—an area of ongoing legal and regulatory debate.",\n        "technical": "Clinical labs operate under CMS CLIA certification (42 CFR Part 493) covering analytical validity and lab operations; FDA\'s 2024 LDT Final Rule seeking phased IVD regulation was vacated by federal court in 2025, keeping CLIA and Congressional VALID-style legislation central.",\n        "url": "https://www.cms.gov/medicare/quality/clinical-laboratory-improvement-amendments",\n    },\n    {\n        "id": "cdx-eu-ivdr",\n        "name": "EU In Vitro Diagnostic Regulation (IVDR, 2017/746)",\n        "plain": "Europe overhauled its diagnostic rules so companion diagnostics can no longer be self-certified—they now require independent Notified Body review plus consultation with the EMA.",\n        "technical": "Under Regulation (EU) 2017/746, companion diagnostics are classified as Class C devices requiring Notified Body conformity assessment, clinical performance studies, and mandatory EMA / national medicines authority consultation.",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/medical-devices/in-vitro-diagnostics",\n    },\n]\n\nPGX_IMPLEMENTATION = [\n    {\n        "id": "pgx-fda-tables",\n        "name": "FDA Pharmacogenomic Biomarker & Association Tables",\n        "plain": "The FDA maintains public lists showing hundreds of approved medicines whose labels include genetic testing advice—telling doctors when to adjust doses or pick a safer alternative.",\n        "technical": "FDA publishes both the Table of Pharmacogenomic Biomarkers in Drug Labeling (500+ drug-biomarker pairs) and the Table of Pharmacogenetic Associations stratified by evidence supporting therapeutic management recommendations.",\n        "url": "https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling",\n    },\n    {\n        "id": "pgx-cpic",\n        "name": "CPIC & DPWG Actionable Gene–Drug Dosing Guidelines",\n        "plain": "International expert consortia translate raw DNA results (like \'CYP2C19 poor metabolizer\') into concrete prescribing steps—for example, switching clopidogrel or lowering chemotherapy doses.",\n        "technical": "Clinical Pharmacogenetics Implementation Consortium (CPIC) and Dutch Pharmacogenetics Working Group (DPWG) publish peer-reviewed dosing rules for high-impact pairs: CYP2C19/clopidogrel, CYP2D6/codeine-tramadol, DPYD/fluoropyrimidines, TPMT+NUDT15/thiopurines, and SLCO1B1/statins.",\n        "url": "https://cpicpgx.org/guidelines/",\n    },\n    {\n        "id": "pgx-germline-somatic",\n        "name": "Germline (Inherited) vs. Somatic (Tumor) Genomic Testing",\n        "plain": "Germline tests look at DNA inherited from your parents (affecting drug metabolism or hereditary cancer risk like BRCA1/2), while somatic tests look at mutations that happened only inside a tumor.",\n        "technical": "Distinguishing germline variants (e.g., BRCA1/2 for PARP inhibitors, Lynch syndrome, CYP450/DPYD pharmacogenes) from somatic driver mutations guides both targeted therapy eligibility and family genetic counseling.",\n        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/precision-medicine",\n    },\n    {\n        "id": "pgx-mtb-cds",\n        "name": "Molecular Tumor Boards (MTBs) & EHR Clinical Decision Support",\n        "plain": "Hospitals convene multidisciplinary teams to interpret complex 500-gene tumor reports and build automated alerts inside electronic health records that warn doctors before prescribing a genetically mismatched drug.",\n        "technical": "MTBs match complex genomic alterations to approved targeted therapies, off-label precision options, or biomarker-driven clinical trials; preemptive PGx panels integrate via HL7 FHIR/CDS Hooks into EHR order entry.",\n        "url": "https://www.ncbi.nlm.nih.gov/books/NBK326791/",\n    },\n    {\n        "id": "pgx-reimbursement",\n        "name": "Diagnostic Reimbursement: CMS NCD 90.2, MolDX & PLA Codes",\n        "plain": "Even when a precision test is FDA-approved, getting insurers to pay for it requires specific Medicare coverage policies and billing codes—making diagnostic reimbursement a distinct hurdle from drug coverage.",\n        "technical": "CMS National Coverage Determination (NCD 90.2) provides nationwide Medicare coverage for FDA-approved/cleared NGS CDx in advanced cancer; regional MolDX MACs evaluate technical assessments and CPT Proprietary Laboratory Analyses (PLA) codes.",\n        "url": "https://www.cms.gov/medicare-coverage-database/view/ncd.aspx?ncdid=372",\n    },\n    {\n        "id": "pgx-equity",\n        "name": "Genomic Reference Diversity & Ancestry Equity",\n        "plain": "Because early genetic databases mostly enrolled people of European ancestry, some drug-metabolism variants common in African, Asian, or Indigenous populations were historically missed.",\n        "technical": "Allele frequencies for key pharmacogenes (e.g., CYP2C19*2/*3, HLA-B*15:02, CYP2D6 structural variants, VKORC1) vary substantially across ancestries; initiatives like NIH\'s All of Us Research Program expand multi-ancestry reference panels.",\n        "url": "https://allofus.nih.gov/",\n    },\n]\n\n\ndef build_cdx(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced educational reference on biomarkers, diagnostic assay platforms, FDA/EU companion diagnostic co-development, and clinical pharmacogenomics (FDA, eCFR, NIH/NCBI, CPIC, CMS, EMA). Educational reference only—not medical advice.",\n        "biomarker_taxonomy": BIOMARKER_TAXONOMY,\n        "assay_platforms": ASSAY_PLATFORMS,\n        "regulatory_codev": REGULATORY_CODEV,\n        "pgx_implementation": PGX_IMPLEMENTATION,\n    }\n    (data_dir / "cdx.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "biomarker_taxonomy": len(BIOMARKER_TAXONOMY),\n        "assay_platforms": len(ASSAY_PLATFORMS),\n        "regulatory_codev": len(REGULATORY_CODEV),\n        "pgx_implementation": len(PGX_IMPLEMENTATION),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_cdx(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
CDX_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderCdxCodevSvg() {\n  const nodes = [\n    { x: 8, label: "1. Biomarker", sub: "BEST Framework" },\n    { x: 140, label: "2. Assay Build", sub: "IHC / NGS / ctDNA" },\n    { x: 272, label: "3. Trial Bridge", sub: "IDE / Concordance" },\n    { x: 404, label: "4. Joint Review", sub: "CDER + CDRH PMA" },\n    { x: 536, label: "5. Precision Care", sub: "CDx / CPIC / MTB" },\n  ];\n  return html`<figure class="cdx-flow" aria-label="Drug and companion diagnostic co-development workflow">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 3 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 3 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Contemporaneous drug–diagnostic co-development from biomarker discovery through joint FDA CDER/CDRH review and precision prescribing.</figcaption>\n  </figure>`;\n}\n\nexport async function cdxPage(query, mode = "ref") {\n  const doc = await getJSON("data/cdx.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/cdx" : "#/ref/cdx";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Companion Diagnostics (CDx), Biomarkers & Precision Medicine",\n    body: html`\n      <h1>Companion Diagnostics (CDx), Biomarkers &amp; Precision Medicine</h1>\n      <p class="lead">${mode === "explore"\n        ? "How genetic and protein tests match the right medicine to the right patient—from biopsy stains and liquid-biopsy blood draws to FDA co-approval and pharmacogenomic dosing."\n        : "Primary-sourced reference covering the FDA-NIH BEST biomarker taxonomy, 6 diagnostic assay platforms, FDA/EU CDx co-development & LDT/CLIA regulation, and clinical pharmacogenomics implementation (checked " + doc.checked + ")."}</p>\n\n      ${renderCdxCodevSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=biomarkers"${sec === "biomarkers" ? \' aria-current="page"\' : ""}>Biomarkers &amp; BEST (6)</a> ·\n        <a href="${base}?section=assays"${sec === "assays" ? \' aria-current="page"\' : ""}>Assay Platforms (6)</a> ·\n        <a href="${base}?section=codev"${sec === "codev" ? \' aria-current="page"\' : ""}>CDx Co-Dev &amp; IVDR (6)</a> ·\n        <a href="${base}?section=pgx"${sec === "pgx" ? \' aria-current="page"\' : ""}>Pharmacogenomics &amp; Access (6)</a>\n      </p>\n\n      ${show("biomarkers") ? html`\n        <h2 id="biomarkers">1. Biomarker Taxonomy &amp; FDA-NIH BEST Framework (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Biomarker taxonomy and BEST framework">\n          <table class="tbl"><thead><tr><th>Biomarker Pillar</th><th>${mode === "explore" ? "What It Tells Doctors" : "Definition & Regulatory Qualification"}</th></tr></thead>\n          <tbody>${(doc.biomarker_taxonomy || []).map((b) => html`<tr id="${b.id}">\n            <td><b><a href="${b.url}" target="_blank" rel="noopener">${b.name}</a></b></td>\n            <td>${mode === "explore" ? b.plain : html`${b.plain}<br><span class="muted small">${b.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("assays") ? html`\n        <h2 id="assays">2. Diagnostic Technologies &amp; Assay Platforms (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Diagnostic assay platforms">\n          <table class="tbl"><thead><tr><th>Platform</th><th>${mode === "explore" ? "How the Test Works" : "Clinical Scope & Analytical Tradeoffs"}</th></tr></thead>\n          <tbody>${(doc.assay_platforms || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("codev") ? html`\n        <h2 id="codev">3. Regulatory Co-Development: FDA CDx, PMA, 510(k) &amp; LDTs (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="CDx regulatory co-development">\n          <table class="tbl"><thead><tr><th>Regulatory Framework</th><th>${mode === "explore" ? "How Tests Are Approved" : "Statutory & Validation Requirements"}</th></tr></thead>\n          <tbody>${(doc.regulatory_codev || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b></td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("pgx") ? html`\n        <h2 id="pgx">4. Pharmacogenomics (PGx), Clinical Implementation &amp; Access (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharmacogenomics and precision access">\n          <table class="tbl"><thead><tr><th>Implementation Pillar</th><th>${mode === "explore" ? "How It Reaches Patients" : "Clinical Guidelines, Coding & Equity"}</th></tr></thead>\n          <tbody>${(doc.pgx_implementation || []).map((p) => html`<tr id="${p.id}">\n            <td><b><a href="${p.url}" target="_blank" rel="noopener">${p.name}</a></b></td>\n            <td>${mode === "explore" ? p.plain : html`${p.plain}<br><span class="muted small">${p.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/trials">Clinical Trials &amp; Endpoints</a> · <a href="#/ref/adme">ADME/PK &amp; Pharmacogenomics</a> · <a href="#/ref/safety">Drug Safety &amp; HLA Biomarkers</a> · <a href="#/ref/pathways">Approval Pathways</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { cdxPage } from "./cdx.js";\n'
    if "./cdx.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/cdx"' not in txt:
        for anchor in ('if (path === "/ref/global-reg")', 'if (path === "/ref/sterile")', 'if (path === "/ref/ip")', 'if (path === "/ref/trials")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/cdx") return cdxPage(query, "ref");\n'
                    '  if (path === "/explore/cdx") return cdxPage(query, "explore");\n'
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
    if "#/ref/cdx" not in txt:
        for anchor in ('["#/ref/global-reg", "Global agencies & HTA"]', '["#/ref/trials", "Clinical trials & endpoints"]', '["#/ref/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/cdx", "CDx & precision medicine"]', 1)
                changed = True
                break
    if "#/explore/cdx" not in txt:
        for anchor in ('["#/explore/global-reg", "Global agencies & HTA"]', '["#/explore/trials", "Clinical trials & endpoints"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/cdx", "CDx & precision medicine"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_cdx.py" in txt:
        return False
    hook = "\n# v6.1o: Companion Diagnostics (CDx), Biomarkers & Precision Medicine Reference\npython3 pipeline/build_cdx.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/cdx"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/cdx")\n'
        'def api_cdx():\n'
        '    return _read_json(SITE_DIR / "data" / "cdx.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"cdx.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    cdx_ref = _load(data_dir / "cdx.json", {}) or {}\n'
        '    for sec_key, sec_q in [("biomarker_taxonomy", "biomarkers"), ("assay_platforms", "assays"), ("regulatory_codev", "codev"), ("pgx_implementation", "pgx")]:\n'
        '        for item in (cdx_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "cdx_biomarker",\n'
        '                "group": "Companion Diagnostics & Precision Medicine",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/cdx?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/cdx?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"companion diagnostic CDx biomarker precision medicine NGS liquid biopsy ctDNA pharmacogenomics CPIC IVDR {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"cdx", "#/ref/cdx"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    cdx_doc = _load_json(data_dir / "cdx.json")\n'
        '    if isinstance(cdx_doc, dict) and cdx_doc.get("biomarker_taxonomy"):\n'
        '        cdx_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (cdx_doc.get("biomarker_taxonomy") or []) + (cdx_doc.get("assay_platforms") or []))\n'
        '        pages.append(("cdx", "#/ref/cdx", "Companion Diagnostics (CDx), Biomarkers & Precision Medicine",\n'
        '                      "Primary-sourced guide to FDA-NIH BEST biomarkers, IHC/FISH/PCR/NGS/ctDNA liquid biopsy platforms, FDA PMA & EU IVDR companion diagnostic co-development, and CPIC pharmacogenomics.",\n'
        '                      f"<ul>{cdx_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/cdx"' in txt:
        return False
    for anchor in ('    "/#/explore/global-reg",', '    "/#/explore/sterile",', '    "/#/explore/ip",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/cdx",\n    "/#/explore/cdx",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_cdx_py": _write_if_changed(pipe_dir / "build_cdx.py", BUILD_CDX_PY),
        "cdx_js": _write_if_changed(js_dir / "cdx.js", CDX_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/global-reg") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/global-reg", "Global agencies & HTA"]] }];\nconst EXPLORE_NAV = [["#/explore/global-reg", "Global agencies & HTA"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/global-reg",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_cdx.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_cdx.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"biomarker_taxonomy": 6, "assay_platforms": 6, "regulatory_codev": 6, "pgx_implementation": 6}, out

        doc = json.loads((root / "site" / "data" / "cdx.json").read_text(encoding="utf-8"))
        for k in ("biomarker_taxonomy", "assay_platforms", "regulatory_codev", "pgx_implementation"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61O_CDX_BIOMARKERS_PRECISION_MEDICINE_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1o Companion Diagnostics, Biomarkers & Precision Medicine patch.")
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
