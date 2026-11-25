#!/usr/bin/env python3
"""Pill by Pill v6.1u Patch: Pharmaceutical Careers, Roles & Training Pathways (#/explore/careers, #/ref/careers, /api/careers).

1. Adds `pipeline/build_careers.py` -> `site/data/careers.json` mapping 24 real-world pharma,
   biotech, engineering, regulatory, legal, and healthcare roles across all 8 lifecycle stages
   with degrees/credentials and verified BLS / FDA / USPTO links (zero fabricated salary figures).
2. Adds `site/js/careers.js` (`careersPage` with inline 4-Cluster Career SVG + 4 track filters)
   and wires `#/explore/careers`, `#/ref/careers`, `/api/careers`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `careers.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/careers/` static SEO page + sitemap entry -> 37
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1u_pharma_careers_roles_pathways_patch.py --selftest
  python3 2026-11-24_v6.1u_pharma_careers_roles_pathways_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_CAREERS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1u Pharmaceutical Careers, Roles & Training Pathways (`site/data/careers.json`).\n\nMaps all 8 pharmaceutical lifecycle stages to real-world job roles, typical degrees/credentials,\nday-to-day responsibilities, and official U.S. Bureau of Labor Statistics (BLS) / professional\nresources (zero fabricated salary figures):\n  1. Discovery, Formulation & Analytical R&D Roles (6 roles)\n  2. Clinical Trials, Biostatistics & Regulatory Roles (6 roles)\n  3. Manufacturing, Engineering & Quality (CMC) Roles (6 roles)\n  4. Medical Affairs, Market Access, Safety & Pharmacy Roles (6 roles)\n\nAll anchors are verified HTTPS primary sources (BLS Occupational Outlook Handbook, FDA, NIH).\n\nUsage:\n  python3 pipeline/build_careers.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nRD_ROLES = [\n    {\n        "id": "car-medchem",\n        "name": "Medicinal Chemist & Computational Chemist",\n        "stage": "Stage 1: Discovery",\n        "degrees": "PhD or MS/BS in Organic, Medicinal, or Computational Chemistry",\n        "plain": "Designs and synthesizes brand-new drug molecules atom-by-atom so they lock tightly into a disease target while staying safe and absorbable in the human body.",\n        "technical": "Executes structure-activity relationship (SAR) optimization, structure-based drug design (SBDD), ADME/PK tuning, and synthetic route scouting.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/chemists-and-materials-scientists.htm",\n    },\n    {\n        "id": "car-biologist",\n        "name": "Discovery Biologist, Pharmacologist & Toxicologist",\n        "stage": "Stage 1: Discovery & Preclinical",\n        "degrees": "PhD, DVM, or MS/BS in Biology, Pharmacology, or Toxicology (DABT)",\n        "plain": "Tests whether a candidate molecule actually shuts down a disease pathway in living cells and checks organ safety before any human ever receives a dose.",\n        "technical": "Runs target validation, high-throughput screening (HTS), in vivo PK/PD models, and IND-enabling 21 CFR Part 58 GLP safety pharmacology and toxicology.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/medical-scientists.htm",\n    },\n    {\n        "id": "car-formulation",\n        "name": "Formulation Scientist & Drug-Delivery Engineer",\n        "stage": "Stage 2: Formulation",\n        "degrees": "PhD, PharmD, MS, or BS in Pharmaceutics, Chemical Engineering, or Materials Science",\n        "plain": "Turns a raw powder or fragile protein into a real pill, sterile vial, inhaler, or lipid nanoparticle that stays stable on shelves and releases properly inside the body.",\n        "technical": "Develops oral solid dosage forms, amorphous solid dispersions, sterile parenteral/lyophilized formulations, LNP mixing processes, and combination-product delivery systems.",\n        "url": "https://www.bls.gov/ooh/architecture-and-engineering/chemical-engineers.htm",\n    },\n    {\n        "id": "car-analytical",\n        "name": "Analytical Development & QC Chemist",\n        "stage": "Stage 3: Analytical QC",\n        "degrees": "BS, MS, or PhD in Analytical Chemistry, Biochemistry, or Chemistry",\n        "plain": "Operates HPLC, mass spectrometers, and dissolution baths to measure exact drug strength and verify every batch is free of harmful impurities.",\n        "technical": "Validates ICH Q2(R2) chromatographic/mass-spec/bioassay methods, manages ICH Q1A stability chambers, and investigates out-of-specification (OOS) lab results under cGMP.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/chemists-and-materials-scientists.htm",\n    },\n    {\n        "id": "car-bioinformatics",\n        "name": "Bioinformatician, Structural Biologist & AI/ML Scientist",\n        "stage": "Stage 1: Discovery & Biomarkers",\n        "degrees": "PhD or MS in Bioinformatics, Structural Biology, Biophysics, or Computer Science",\n        "plain": "Uses cryo-EM, genomic databases, and machine learning to map 3D protein targets and spot which patient groups are most likely to respond to a new medicine.",\n        "technical": "Performs X-ray/cryo-EM structure determination (PDB), multi-omics target discovery, generative molecular modeling, and translational biomarker stratification.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/biochemists-and-biophysicists.htm",\n    },\n    {\n        "id": "car-dmpk",\n        "name": "DMPK & Clinical Pharmacologist",\n        "stage": "Stages 1–4: Preclinical & Clinical",\n        "degrees": "PhD or PharmD in Pharmacokinetics, Clinical Pharmacology, or Pharmaceutical Sciences",\n        "plain": "Measures how fast the body absorbs, metabolizes, and clears a medicine—calculating the exact starting dose and checking for drug-drug interactions.",\n        "technical": "Builds PopPK and PBPK models, evaluates CYP450/transporter DDI risk, conducts exposure-response modeling, and supports pediatric extrapolation (ICH E11A).",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/medical-scientists.htm",\n    },\n]\n\nCLINICAL_REG_ROLES = [\n    {\n        "id": "car-cra-ctm",\n        "name": "Clinical Research Associate (CRA) & Clinical Trial Manager (CTM)",\n        "stage": "Stage 4: Clinical Trials",\n        "degrees": "BS/MS in Life Sciences or Nursing (RN); ACRP / SOCRA certification",\n        "plain": "Visits hospitals running clinical trials to ensure patient safety, verify consent forms, and check that every trial measurement matches real medical charts.",\n        "technical": "Executes ICH E6 GCP site monitoring, Risk-Based Monitoring (RBM), EDC/CTMS/eTMF oversight, and inspection readiness across sponsor and CRO teams.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/medical-scientists.htm",\n    },\n    {\n        "id": "car-medical-monitor",\n        "name": "Clinical Development Physician (Medical Monitor)",\n        "stage": "Stage 4: Clinical Trials",\n        "degrees": "MD, DO, or MD/PhD with specialty clinical training",\n        "plain": "Designs the clinical trial protocol, answers doctors\' medical questions during the study, and reviews patient safety events in real time.",\n        "technical": "Authors Phase 1–3 protocols, oversees medical eligibility and SAE/SUSAR causality, interacts with DSMBs, and presents clinical evidence to FDA/EMA advisory committees.",\n        "url": "https://www.bls.gov/ooh/healthcare/physicians-and-surgeons.htm",\n    },\n    {\n        "id": "car-biostatistician",\n        "name": "Biostatistician & Statistical Programmer (SAS / R)",\n        "stage": "Stage 4: Clinical Trials",\n        "degrees": "PhD or MS in Biostatistics, Statistics, or Data Science",\n        "plain": "Calculates how many patients a trial needs, guards against statistical bias, and analyzes the final unblinded data to prove whether the medicine truly worked.",\n        "technical": "Authors Statistical Analysis Plans (SAPs), implements ICH E9(R1) estimands, adaptive/multiplicity controls, and CDISC SDTM/ADaM submission datasets.",\n        "url": "https://www.bls.gov/ooh/math/mathematicians-and-statisticians.htm",\n    },\n    {\n        "id": "car-reg-affairs",\n        "name": "Regulatory Affairs Specialist & CMC Regulatory Lead",\n        "stage": "Stage 5: Regulatory & Approval",\n        "degrees": "BS, MS, PharmD, or PhD in Life Sciences / Regulatory Science (RAC credential)",\n        "plain": "Acts as the bridge between the company and the FDA/EMA—planning agency meetings, assembling approval dossiers, and keeping labels and factory changes legally compliant.",\n        "technical": "Leads Pre-IND/End-of-Phase 2 meetings, eCTD Modules 1–5 publishing, expedited pathway filings (Breakthrough/Orphan/RMAT), and post-approval ICH Q12 lifecycle variations.",\n        "url": "https://www.fda.gov/about-fda/jobs-and-training-fda",\n    },\n    {\n        "id": "car-med-writer",\n        "name": "Regulatory Medical Writer",\n        "stage": "Stages 4–5: Clinical & Regulatory",\n        "degrees": "PhD, PharmD, MS, or BS in Life Sciences (AMWA / EMWA credentials)",\n        "plain": "Translates massive clinical trial tables and lab reports into clear, accurate protocols, investigator brochures, and FDA approval documents.",\n        "technical": "Authors clinical protocols, Clinical Study Reports (ICH E3 CSRs), Investigator\'s Brochures, eCTD Module 2 clinical/nonclinical summaries, and lay trial summaries.",\n        "url": "https://www.bls.gov/ooh/media-and-communication/technical-writers.htm",\n    },\n    {\n        "id": "car-cdm",\n        "name": "Clinical Data Manager (CDM)",\n        "stage": "Stage 4: Clinical Trials",\n        "degrees": "BS/MS in Life Sciences, Health Informatics, or Data Management (CCDM)",\n        "plain": "Builds the digital trial forms hospitals fill out and cleans millions of patient data points before database lock.",\n        "technical": "Designs eCRFs and edit checks in EDC (Medidata Rave, Veeva Vault), manages medical coding (MedDRA/WHODrug), reconciles SAE/central lab feeds, and enforces 21 CFR Part 11.",\n        "url": "https://www.bls.gov/ooh/math/data-scientists.htm",\n    },\n]\n\nMFG_QUALITY_ROLES = [\n    {\n        "id": "car-bioprocess-eng",\n        "name": "Bioprocess & Process Development Engineer (USP / DSP)",\n        "stage": "Stage 6: Manufacturing",\n        "degrees": "BS, MS, or PhD in Chemical, Biochemical, or Biomedical Engineering",\n        "plain": "Scales up a medicine from a tiny 2-liter lab flask to a 15,000-liter factory bioreactor or commercial synthesis plant without changing its purity.",\n        "technical": "Designs upstream cell-culture feeds, downstream Protein A/IEX/TFF purification trains, tech transfers to CDMOs, and Stage 1–2 Process Performance Qualification (PPQ).",\n        "url": "https://www.bls.gov/ooh/architecture-and-engineering/chemical-engineers.htm",\n    },\n    {\n        "id": "car-qa-qp",\n        "name": "Quality Assurance (QA) Specialist & EU Qualified Person (QP)",\n        "stage": "Stages 3 & 6: Quality & Manufacturing",\n        "degrees": "BS/MS/PharmD in Pharmacy, Chemistry, or Biology (ASQ CQA / EU QP license)",\n        "plain": "The independent referee inside every factory—reviewing batch records, investigating any deviation, and signing off before a single bottle can ship to pharmacies.",\n        "technical": "Manages QMS deviations, CAPA, change control, supplier/CDMO audits, FDA/EMA inspection hosting, and statutory batch disposition (21 CFR 211.22 / EU Annex 16 QP).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",\n    },\n    {\n        "id": "car-cqv-eng",\n        "name": "Commissioning, Qualification & Validation (CQV) Engineer",\n        "stage": "Stage 6: Manufacturing",\n        "degrees": "BS in Mechanical, Electrical, Chemical, or Biomedical Engineering",\n        "plain": "Tests and documents that every cleanroom HVAC unit, autoclave, freeze-dryer, and filling line works reliably before it ever touches a real patient batch.",\n        "technical": "Executes URS, Design/Installation/Operational/Performance Qualification (DQ/IQ/OQ/PQ), computer-system validation (CSV/CSA), and cleanroom ISO 14644 certification.",\n        "url": "https://www.bls.gov/ooh/architecture-and-engineering/industrial-engineers.htm",\n    },\n    {\n        "id": "car-microbiologist",\n        "name": "QC Microbiologist & Sterility Assurance Specialist",\n        "stage": "Stages 3 & 6: Analytical & Sterile Mfg",\n        "degrees": "BS or MS in Microbiology, Biology, or Biotechnology",\n        "plain": "Guards sterile factories against invisible bacteria, fungi, and endotoxins by testing cleanroom air, Water for Injection, and finished vials.",\n        "technical": "Runs Environmental Monitoring (EM), USP <71> sterility, USP <85> LAL/rFC endotoxin, aseptic media-fill (APS) oversight, and EU Annex 1 Contamination Control Strategies.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/microbiologists.htm",\n    },\n    {\n        "id": "car-mfg-tech",\n        "name": "cGMP Biomanufacturing & Aseptic Operator / Technician",\n        "stage": "Stage 6: Manufacturing",\n        "degrees": "Associate degree, Biotech Certificate, or BS (strong hands-on entry pathway)",\n        "plain": "The skilled technicians gowned up inside cleanrooms operating bioreactors, tablet presses, isolators, and filling lines every day to produce the world\'s medicine supply.",\n        "technical": "Executes Master/Electronic Batch Records (MES/eBR), aseptic gowning and isolator interventions, single-use manifold assembly, and in-process control checks.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/chemical-technicians.htm",\n    },\n    {\n        "id": "car-automation-csv",\n        "name": "Pharma Automation, MES & Building Controls Engineer",\n        "stage": "Stage 6: Manufacturing",\n        "degrees": "BS in Electrical, Mechanical, Computer, or Chemical Engineering",\n        "plain": "Builds and maintains the automated control systems that regulate cleanroom airflow, bioreactor temperatures, and electronic batch records around the clock.",\n        "technical": "Engineers DCS/PLC/SCADA bioprocess automation, cGMP Building Automation Systems (BAS) / Environmental Monitoring Systems (EMS), MES/eBR integration, and GAMP 5 validation.",\n        "url": "https://www.bls.gov/ooh/architecture-and-engineering/electrical-and-electronics-engineers.htm",\n    },\n]\n\nCOMMERCIAL_SAFETY_ROLES = [\n    {\n        "id": "car-pv-safety",\n        "name": "Pharmacovigilance (Drug Safety) Scientist & Safety Physician",\n        "stage": "Stages 4 & 8: Clinical & Post-Market Safety",\n        "degrees": "PharmD, MD, RN, or MS/PhD in Epidemiology or Life Sciences",\n        "plain": "Monitors side-effect reports from doctors and patients worldwide, investigates safety signals, and updates warning labels when new risks emerge.",\n        "technical": "Processes ICH E2B(R3) ICSRs, conducts MedDRA coding and PRR/EBGM signal detection, authors DSUR/PBRERs, and manages FDA REMS / EU RMP programs.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/epidemiologists.htm",\n    },\n    {\n        "id": "car-msl",\n        "name": "Medical Science Liaison (MSL) & Medical Affairs",\n        "stage": "Stage 7: Commercial & Medical Exchange",\n        "degrees": "PharmD, PhD, or MD",\n        "plain": "Field-based scientists who share peer-reviewed clinical data with hospital specialists and bring real-world doctor feedback back to R&D—strictly separate from sales.",\n        "technical": "Leads non-promotional peer-to-peer scientific exchange with Key Opinion Leaders (KOLs), supports investigator-initiated trials (IITs), and generates real-world evidence.",\n        "url": "https://www.bls.gov/ooh/healthcare/pharmacists.htm",\n    },\n    {\n        "id": "car-heor-access",\n        "name": "HEOR Scientist & Market Access / Pricing Lead",\n        "stage": "Stage 7: Economics & Market Access",\n        "degrees": "PhD, PharmD, MPH, or MS in Health Economics, Outcomes Research, or MBA",\n        "plain": "Measures whether a new medicine saves hospitalizations or improves quality of life enough to justify insurance coverage—and builds evidence packages for payers and HTA bodies.",\n        "technical": "Develops cost-effectiveness (QALY/ICER) and budget-impact models, manages NICE/G-BA/HAS/PBAC HTA dossiers, and models U.S. Gross-to-Net PBM/340B/CMS economics.",\n        "url": "https://www.bls.gov/ooh/life-physical-and-social-science/economists.htm",\n    },\n    {\n        "id": "car-patent-attorney",\n        "name": "Pharmaceutical Patent Attorney & Patent Agent",\n        "stage": "Stages 1 & 7: IP & Exclusivity",\n        "degrees": "JD + USPTO Patent Bar (Attorney) or STEM PhD/MS + USPTO Patent Bar (Agent)",\n        "plain": "Drafts scientific patent applications covering new molecules and formulations and navigates Hatch-Waxman Orange Book and BPCIA biologic disputes.",\n        "technical": "Handles USPTO patent prosecution, Freedom-to-Operate (FTO) opinions, Patent Term Extension (35 U.S.C. § 156), Orange Book listings, and Paragraph IV / BPCIA litigation.",\n        "url": "https://www.uspto.gov/learning-and-resources/patent-and-trademark-practitioners/becoming-patent-practitioner",\n    },\n    {\n        "id": "car-supply-chain",\n        "name": "Pharma Supply Chain, Cold-Chain & DSCSA Serialization Manager",\n        "stage": "Stage 8: Distribution",\n        "degrees": "BS/MS in Supply Chain Management, Industrial Engineering, or Business",\n        "plain": "Plans global factory capacity, coordinates ultra-cold shipping lanes, and ensures pharmacies never run out of essential medicines.",\n        "technical": "Manages S&OP demand forecasting, API/CDMO dual-sourcing, qualified 2–8°C / -80°C / LN2 cold-chain lanes, and DSCSA EPCIS serialization compliance.",\n        "url": "https://www.bls.gov/ooh/business-and-financial/logisticians.htm",\n    },\n    {\n        "id": "car-pharmacist",\n        "name": "Clinical, Hospital, Specialty & Industry Pharmacist",\n        "stage": "Stages 4, 7 & 8: Patient Care & Industry",\n        "degrees": "Doctor of Pharmacy (PharmD) + State Licensure (PGY1/PGY2 or Industry Fellowship)",\n        "plain": "The medication expert at the final mile—checking drug interactions, dosing chemotherapy in hospitals, guiding specialty/REMS patients, and serving across pharma R&D and safety.",\n        "technical": "Spans retail/community care, hospital clinical pharmacy (oncology, ICU, infectious disease, pharmacogenomics), specialty pharmacy hubs, and pharma industry fellowships.",\n        "url": "https://www.bls.gov/ooh/healthcare/pharmacists.htm",\n    },\n]\n\n\ndef build_careers(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Educational career map linking all 8 pharmaceutical lifecycle stages to real-world scientific, engineering, regulatory, and healthcare roles, anchored to official U.S. Bureau of Labor Statistics (BLS), FDA, and USPTO resources (zero fabricated salary numbers).",\n        "rd_roles": RD_ROLES,\n        "clinical_reg_roles": CLINICAL_REG_ROLES,\n        "mfg_quality_roles": MFG_QUALITY_ROLES,\n        "commercial_safety_roles": COMMERCIAL_SAFETY_ROLES,\n    }\n    (data_dir / "careers.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "rd_roles": len(RD_ROLES),\n        "clinical_reg_roles": len(CLINICAL_REG_ROLES),\n        "mfg_quality_roles": len(MFG_QUALITY_ROLES),\n        "commercial_safety_roles": len(COMMERCIAL_SAFETY_ROLES),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_careers(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
CAREERS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderCareersSvg() {\n  const nodes = [\n    { x: 8, label: "Discovery & Lab", sub: "Chemists / Biologists" },\n    { x: 174, label: "Clinical & Reg", sub: "CRAs / Stats / RAC" },\n    { x: 340, label: "Factory & QA", sub: "Eng / QA / Techs" },\n    { x: 506, label: "Access & Care", sub: "PV / HEOR / PharmD" },\n  ];\n  return html`<figure class="careers-flow" aria-label="Pharmaceutical career clusters across the drug lifecycle">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="152" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 0 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 0 ? "2" : "1.5"}"/>\n        <text x="${n.x + 76}" y="35" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 76}" y="53" text-anchor="middle" font-size="10.5" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 152}" y1="41" x2="${n.x + 166}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">24 core careers spanning chemistry, biology, engineering, statistics, law, manufacturing, and patient care—from associate certificates to PhD/PharmD/MD.</figcaption>\n  </figure>`;\n}\n\nexport async function careersPage(query, mode = "explore") {\n  const doc = await getJSON("data/careers.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/careers" : "#/ref/careers";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Pharmaceutical Careers, Roles & Training Pathways",\n    body: html`\n      <h1>Pharmaceutical Careers, Roles &amp; Training Pathways</h1>\n      <p class="lead">${mode === "explore"\n        ? "Curious who actually builds, tests, regulates, and delivers a medicine? Explore 24 real-world careers across all 8 lifecycle stages—from cleanroom technicians and chemists to statisticians, patent attorneys, and pharmacists."\n        : "Lifecycle-mapped directory of 24 pharmaceutical, biotech, engineering, regulatory, and healthcare roles with typical credentials and official BLS/FDA/USPTO occupational links (checked " + doc.checked + ")."}</p>\n\n      ${renderCareersSvg()}\n\n      <p class="small">Jump to track:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All 24 Roles</a> ·\n        <a href="${base}?section=rd"${sec === "rd" ? \' aria-current="page"\' : ""}>Discovery &amp; Lab R&amp;D (6)</a> ·\n        <a href="${base}?section=clinical"${sec === "clinical" ? \' aria-current="page"\' : ""}>Clinical &amp; Regulatory (6)</a> ·\n        <a href="${base}?section=mfg"${sec === "mfg" ? \' aria-current="page"\' : ""}>Manufacturing, Eng &amp; QA (6)</a> ·\n        <a href="${base}?section=commercial"${sec === "commercial" ? \' aria-current="page"\' : ""}>Safety, Access, IP &amp; Pharmacy (6)</a>\n      </p>\n\n      ${show("rd") ? html`\n        <h2 id="rd">1. Discovery, Formulation &amp; Analytical R&amp;D Roles (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Discovery and R&D roles">\n          <table class="tbl"><thead><tr><th>Role &amp; Lifecycle Stage</th><th>Typical Training / Credentials</th><th>What They Do</th></tr></thead>\n          <tbody>${(doc.rd_roles || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b><br><span class="muted small">${r.stage}</span></td>\n            <td>${r.degrees}</td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("clinical") ? html`\n        <h2 id="clinical">2. Clinical Trials, Biostatistics &amp; Regulatory Roles (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Clinical and regulatory roles">\n          <table class="tbl"><thead><tr><th>Role &amp; Lifecycle Stage</th><th>Typical Training / Credentials</th><th>What They Do</th></tr></thead>\n          <tbody>${(doc.clinical_reg_roles || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b><br><span class="muted small">${r.stage}</span></td>\n            <td>${r.degrees}</td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("mfg") ? html`\n        <h2 id="mfg">3. Manufacturing, Engineering &amp; Quality (CMC) Roles (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Manufacturing and quality roles">\n          <table class="tbl"><thead><tr><th>Role &amp; Lifecycle Stage</th><th>Typical Training / Credentials</th><th>What They Do</th></tr></thead>\n          <tbody>${(doc.mfg_quality_roles || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b><br><span class="muted small">${r.stage}</span></td>\n            <td>${r.degrees}</td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("commercial") ? html`\n        <h2 id="commercial">4. Safety, Medical Affairs, Access, IP &amp; Pharmacy Roles (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Safety, market access, IP, and pharmacy roles">\n          <table class="tbl"><thead><tr><th>Role &amp; Lifecycle Stage</th><th>Typical Training / Credentials</th><th>What They Do</th></tr></thead>\n          <tbody>${(doc.commercial_safety_roles || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b><br><span class="muted small">${r.stage}</span></td>\n            <td>${r.degrees}</td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/explore/how-drugs-are-built">8-Stage Lifecycle</a> · <a href="#/explore/worksheets">Printable Classroom Worksheets</a> · <a href="#/ref/partners">Partner Ecosystem</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { careersPage } from "./careers.js";\n'
    if "./careers.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/careers"' not in txt:
        for anchor in ('if (path === "/ref/combo-devices")', 'if (path === "/ref/otc")', 'if (path === "/ref/rare-pediatric")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/careers") return careersPage(query, "ref");\n'
                    '  if (path === "/explore/careers") return careersPage(query, "explore");\n'
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
    if "#/ref/careers" not in txt:
        for anchor in ('["#/ref/combo-devices", "Combination devices"]', '["#/ref/partners", "Partner ecosystem"]', '["#/ref/otc", "OTC & compounding"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/careers", "Careers & roles"]', 1)
                changed = True
                break
    if "#/explore/careers" not in txt:
        for anchor in ('["#/explore/combo-devices", "Combination devices"]', '["#/explore/worksheets", "Teacher worksheets"]', '["#/explore/otc", "OTC & compounding"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/careers", "Careers & roles"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_careers.py" in txt:
        return False
    hook = "\n# v6.1u: Pharmaceutical Careers, Roles & Training Pathways\npython3 pipeline/build_careers.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/careers"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/careers")\n'
        'def api_careers():\n'
        '    return _read_json(SITE_DIR / "data" / "careers.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"careers.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    car_ref = _load(data_dir / "careers.json", {}) or {}\n'
        '    for sec_key, sec_q in [("rd_roles", "rd"), ("clinical_reg_roles", "clinical"), ("mfg_quality_roles", "mfg"), ("commercial_safety_roles", "commercial")]:\n'
        '        for item in (car_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "career",\n'
        '                "group": "Careers & Training Pathways",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": f"{item.get(\'stage\', \'\')} · {item.get(\'plain\', \'\')}",\n'
        '                "href_ref": f"#/ref/careers?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/careers?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"career job role degree training {item.get(\'stage\', \'\')} {item.get(\'degrees\', \'\')} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"careers", "#/explore/careers"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    car_doc = _load_json(data_dir / "careers.json")\n'
        '    if isinstance(car_doc, dict) and car_doc.get("rd_roles"):\n'
        '        car_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> ({_esc(x.get("stage",""))}) — {_esc(x.get("plain",""))}</li>\' for x in (car_doc.get("rd_roles") or []) + (car_doc.get("clinical_reg_roles") or []))\n'
        '        pages.append(("careers", "#/explore/careers", "Pharmaceutical Careers, Roles & Training Pathways",\n'
        '                      "Explore 24 real-world pharmaceutical, biotech, engineering, regulatory, legal, and healthcare careers mapped across all 8 lifecycle stages.",\n'
        '                      f"<ul>{car_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/explore/careers"' in txt:
        return False
    for anchor in ('    "/#/explore/combo-devices",', '    "/#/explore/otc",', '    "/#/explore/rare-pediatric",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/careers",\n    "/#/explore/careers",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_careers_py": _write_if_changed(pipe_dir / "build_careers.py", BUILD_CAREERS_PY),
        "careers_js": _write_if_changed(js_dir / "careers.js", CAREERS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/combo-devices") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/combo-devices", "Combination devices"]] }];\nconst EXPLORE_NAV = [["#/explore/combo-devices", "Combination devices"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/combo-devices",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_careers.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_careers.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"rd_roles": 6, "clinical_reg_roles": 6, "mfg_quality_roles": 6, "commercial_safety_roles": 6}, out

        doc = json.loads((root / "site" / "data" / "careers.json").read_text(encoding="utf-8"))
        for k in ("rd_roles", "clinical_reg_roles", "mfg_quality_roles", "commercial_safety_roles"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61U_PHARMA_CAREERS_ROLES_PATHWAYS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1u Pharmaceutical Careers, Roles & Training Pathways patch.")
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
