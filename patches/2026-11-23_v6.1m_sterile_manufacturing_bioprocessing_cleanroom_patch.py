#!/usr/bin/env python3
"""Pill by Pill v6.1m Patch: Sterile Manufacturing, Bioprocessing & Cleanroom Engineering Reference (#/ref/sterile, #/explore/sterile, /api/sterile).

1. Adds `pipeline/build_sterile_mfg.py` -> `site/data/sterile_mfg.json` (6 cleanroom/HVAC/Annex 1
   pillars, 6 upstream/downstream bioprocessing operations, 6 aseptic fill-finish/lyophilization
   controls, and 6 validation/PAT/ICH Q13 frameworks — 24 primary-sourced entries).
2. Adds `site/js/sterile_mfg.js` (`sterileMfgPage` with inline Bioprocessing-to-Release SVG +
   4 section filters) and wires `#/ref/sterile`, `#/explore/sterile`, `/api/sterile`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `sterile_mfg.json` into `pipeline/build_global_search.py`, `pipeline/build_v60_static_pages.py`
   (`/sterile/` static SEO page + sitemap entry -> 29 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1m_sterile_manufacturing_bioprocessing_cleanroom_patch.py --selftest
  python3 2026-11-23_v6.1m_sterile_manufacturing_bioprocessing_cleanroom_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_STERILE_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1m Sterile Manufacturing, Bioprocessing & Cleanroom Engineering Reference (`site/data/sterile_mfg.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Cleanroom Classification, HVAC & Contamination Control (6 pillars: ISO 5–8 / EU Grade A–D, Pressure Cascades & HEPA/ULPA, EU GMP Annex 1 CCS, Isolators vs. RABS, Environmental Monitoring EM, WFI & Clean Steam Utilities)\n  2. Upstream & Downstream Bioprocessing (6 pillars: Cell Banking MCB/WCB, Single-Use vs. Stainless Bioreactors, Harvest & Depth Filtration, Preparative Chromatography Protein A/IEX/HIC, Viral Clearance ICH Q5A, TFF/UFDF Concentration & Buffer Exchange)\n  3. Aseptic Fill-Finish, Sterilization & Lyophilization (6 pillars: Terminal Sterilization vs. Aseptic Processing, Sterilizing-Grade 0.22 µm Filtration & PUPSIT, Aseptic Media Fills / APS, Lyophilization Freeze-Drying Cycles, 100% Visual Inspection & CCIT, Primary Packaging Extractables & Leachables)\n  4. Process Validation, PAT & Continuous Manufacturing (6 pillars: FDA 3-Stage Process Validation Design/PPQ/CPV, Process Analytical Technology PAT, Continuous Manufacturing ICH Q13, Cleaning Validation & CIP/SIP, Single-Use Systems & Leachables, Data Integrity & MES/eBR)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, EMA/EU GMP, ICH).\n\nUsage:\n  python3 pipeline/build_sterile_mfg.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nCLEANROOM_CONTAMINATION = [\n    {\n        "id": "cln-iso-grades",\n        "name": "ISO 5–8 / EU GMP Grade A–D Cleanroom Classification",\n        "plain": "Sterile drug factories nest rooms inside rooms like Russian dolls—from Grade D corridors up to Grade A (ISO 5) sterile zones where open vials sit under ultra-clean filtered air.",\n        "technical": "ISO 14644-1 and FDA Aseptic Processing Guidance define ISO 5 (Grade A, <=3,520 particles >=0.5 µm/m³) for critical aseptic filling, surrounded by ISO 7 (Grade B) background, ISO 8 (Grade C) compounding, and Grade D support areas.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice",\n    },\n    {\n        "id": "cln-hvac-cascades",\n        "name": "HVAC Pressure Cascades, Air Changes & HEPA Filtration",\n        "plain": "Cleaner rooms are kept at slightly higher air pressure than dirtier rooms, so whenever a door opens, air flows outward—pushing dust and microbes away from the medicine.",\n        "technical": "Unidirectional (laminar) airflow at 0.36–0.54 m/s (Grade A) through terminal H14 HEPA filters (>=99.995% at MPPS), differential pressure cascades (>=10–15 Pa between adjacent grades), and controlled temperature/humidity.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice",\n    },\n    {\n        "id": "cln-annex1-ccs",\n        "name": "EU GMP Annex 1 (2022/2023) Contamination Control Strategy (CCS)",\n        "plain": "A holistic master safety plan connecting facility design, air handling, water purity, gowning, and sterilization so contamination is prevented by design rather than caught after the fact.",\n        "technical": "Revised EU GMP Annex 1 mandates a documented, site-wide Contamination Control Strategy (CCS) applying ICH Q9 Quality Risk Management across microbial, endotoxin/pyrogen, and particulate contamination sources.",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/compliance-research-development/good-manufacturing-practice",\n    },\n    {\n        "id": "cln-isolators-rabs",\n        "name": "Barrier Isolators vs. Restricted Access Barrier Systems (RABS)",\n        "plain": "Because human skin is the #1 source of cleanroom bacteria, modern fill lines seal vials inside glass-and-steel gloveboxes (isolators) sterilized with hydrogen peroxide vapor.",\n        "technical": "Closed isolators provide continuous physical separation with automated Vaporized Hydrogen Peroxide (VHP) biodecontamination (6-log spore reduction) in an ISO 8/Grade C/D background; RABS use rigid barriers with glove ports inside a Grade B room.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice",\n    },\n    {\n        "id": "cln-em",\n        "name": "Environmental Monitoring (EM) & Personnel Qualification",\n        "plain": "Sensors continuously count airborne particles while technicians sample air, surfaces, and gloved fingertips to prove zero microbes entered the sterile zone during a batch.",\n        "technical": "Continuous non-viable particle counters (0.5 µm and 5.0 µm) paired with active air samplers, settle plates, contact (RODAC) plates, and gowning/glove-print viable monitoring with strict alert/action limits (Grade A: <1 CFU).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",\n    },\n    {\n        "id": "cln-wfi-utilities",\n        "name": "Water for Injection (WFI), Clean Steam & Process Gases",\n        "plain": "Injectable medicines cannot use ordinary purified water—they require ultra-pure Water for Injection kept circulating hot or ozonated so bacteria and fever-causing endotoxins cannot grow.",\n        "technical": "WFI meets USP <1231> / Ph. Eur. conductivity, TOC (<500 ppb), microbial (<10 CFU/100 mL), and bacterial endotoxin (<0.25 EU/mL) limits via multi-effect distillation or validated membrane (RO+EDI+UF) loops, alongside pyrogen-free Clean Steam.",\n        "url": "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-guides/high-purity-water-system-793",\n    },\n]\n\nBIOPROCESSING = [\n    {\n        "id": "bio-cell-banks",\n        "name": "Master & Working Cell Banks (MCB / WCB, ICH Q5D)",\n        "plain": "Before brewing a biologic medicine, scientists freeze hundreds of identical vials of the engineered master cells in liquid nitrogen so every batch for the next 20 years starts from the exact same cell line.",\n        "technical": "Two-tier cGMP cell banking (MCB -> WCB) characterized per ICH Q5D for identity, genetic stability, clonality, sterility, mycoplasma, and absence of adventitious viruses.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q5d-quality-biotechnologicalbiological-products-derivation-and-characterization-cell-substrates-used",\n    },\n    {\n        "id": "bio-bioreactors",\n        "name": "Upstream Bioreactors: Single-Use (SUB) vs. Stainless Steel",\n        "plain": "Living cells (like CHO cells) grow in nutrient broth inside giant stirred tanks—either reusable 15,000-liter stainless steel vats or disposable 2,000-liter sterile plastic bags for fast product changeovers.",\n        "technical": "Fed-batch or continuous perfusion cell culture controlling dissolved oxygen (DO), pH, temperature, sparging, and metabolite feeds. Single-Use Bioreactors (SUBs) eliminate CIP/SIP turnaround; stainless steel dominates mega-scale commercial mAbs.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q11-development-and-manufacture-drug-substances",\n    },\n    {\n        "id": "bio-harvest",\n        "name": "Primary Harvest, Centrifugation & Depth Filtration",\n        "plain": "Once the cells finish producing the antibody or protein, spinning centrifuges and layered depth filters gently separate the spent cells and debris from the clear protein-rich liquid.",\n        "technical": "Disk-stack continuous centrifugation (or alternating tangential flow / ATF for perfusion) followed by charged depth filtration and 0.2 µm bioburden reduction to yield clarified harvest.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q11-development-and-manufacture-drug-substances",\n    },\n    {\n        "id": "bio-chromatography",\n        "name": "Downstream Preparative Chromatography (Protein A, IEX & HIC)",\n        "plain": "The liquid flows through tall columns packed with microscopic beads that grab the exact medicine molecule while washing away host-cell proteins, DNA, and process impurities.",\n        "technical": "Platform mAb purification: Protein A affinity capture (>95% purity in one step), followed by anion-exchange (AEX) flow-through (removing DNA/endotoxin/viruses) and cation-exchange (CEX) or HIC polishing (removing aggregates/charge variants).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q11-development-and-manufacture-drug-substances",\n    },\n    {\n        "id": "bio-viral-clearance",\n        "name": "Orthogonal Viral Inactivation & Filtration (ICH Q5A)",\n        "plain": "Because biologics come from living cells, factories build in at least two completely different virus-killing and virus-trapping steps—like an acid bath plus a 20-nanometer sieve—to guarantee viral safety.",\n        "technical": "ICH Q5A(R2) requires orthogonal viral clearance steps (e.g., low-pH hold or solvent/detergent inactivation for enveloped viruses + 20 nm parvovirus-retentive nanofiltration) validated with scaled-down viral spiking studies (log reduction values, LRV).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q5ar2-viral-safety-evaluation-biotechnology-products-derived-cell-lines-human-or-animal-origin",\n    },\n    {\n        "id": "bio-tff-ufdf",\n        "name": "Tangential Flow Filtration (TFF / UFDF) & Bulk Drug Substance",\n        "plain": "Pumps the purified protein sideways across ultra-fine membranes to concentrate it to the exact clinical strength and swap it into its final stabilizing buffer before freezing or filling.",\n        "technical": "Ultrafiltration/Diafiltration (UFDF) using regenerated cellulose or PES cassettes/hollow fibers controls transmembrane pressure (TMP), protein concentration, excipient exchange (Donnan effect), and bulk drug substance (BDS) freezing.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q5e-comparability-biotechnologicalbiological-products-subject-changes-their-manufacturing-process",\n    },\n]\n\nASEPTIC_FILL_FINISH = [\n    {\n        "id": "ff-terminal-vs-aseptic",\n        "name": "Terminal Sterilization vs. Aseptic Processing",\n        "plain": "Whenever a medicine can survive high heat or radiation, factories sterilize it inside its sealed final vial. Fragile proteins and mRNA would melt, so they must be filtered sterile and filled in germ-free isolators.",\n        "technical": "FDA and EMA mandate terminal sterilization (e.g., moist heat autoclave achieving SAL <= 10^-6, F0 >= 8–12 min) unless product degradation requires aseptic processing under 21 CFR 211.113.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice",\n    },\n    {\n        "id": "ff-sterile-filtration",\n        "name": "0.22 µm Sterilizing Filtration & PUPSIT Integrity Testing",\n        "plain": "Liquid biologics pass through redundant 0.22-micron membranes—small enough to trap every bacterium—and each filter is pressure-tested before and after use to prove it never tore.",\n        "technical": "Bacterial-retentive 0.22 µm filters validated with Brevundimonas diminuta (>=10^7 CFU/cm²). EU Annex 1 requires Pre-Use Post-Sterilization Integrity Testing (PUPSIT) via bubble-point or diffusive-flow testing.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice",\n    },\n    {\n        "id": "ff-media-fills",\n        "name": "Aseptic Process Simulation (APS / Media Fills)",\n        "plain": "Twice a year, sterile lines fill thousands of vials with bacterial growth broth instead of drug, then incubate them for two weeks—proving the entire line and team can run with zero contaminated vials.",\n        "technical": "Simulates worst-case commercial aseptic filling (line speed, container size, shift changes, routine/non-routine interventions) using soybean-casein digest medium (TSB) incubated 14 days (20–25°C and 30–35°C) with a target of zero positives.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice",\n    },\n    {\n        "id": "ff-lyophilization",\n        "name": "Lyophilization (Freeze-Drying) Cycle Engineering",\n        "plain": "For unstable injectables, factories freeze vials solid and apply a deep vacuum so ice turns straight into vapor—leaving a dry, shelf-stable powder cake that nurses dissolve with sterile water before injection.",\n        "technical": "Three-stage cycle: Freezing (below Tg\' or eutectic point), Primary Drying (ice sublimation under vacuum while keeping product below collapse temperature Tc), and Secondary Drying (desorption of bound water to <1–2% residual moisture).",\n        "url": "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-guides/lyophilization-parenteral-793",\n    },\n    {\n        "id": "ff-visual-ccit",\n        "name": "100% Visual Inspection & Container Closure Integrity Testing (CCIT)",\n        "plain": "Every single filled vial or syringe is spun under high-speed cameras or trained inspectors to catch microscopic glass specks, fibers, or hairline cracks that could let bacteria in.",\n        "technical": "USP <790>/<1790> 100% visual inspection (automated/semi-automated/manual) for visible particulates and defects, paired with deterministic USP <1207> CCIT (HVLD, vacuum decay, laser headspace analysis) replacing legacy dye ingress.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/inspection-injectable-products-visible-particulates",\n    },\n    {\n        "id": "ff-extractables",\n        "name": "Primary Packaging, Elastomers & Extractables / Leachables (E&L)",\n        "plain": "Glass vials, rubber stoppers, and plastic syringes are tested to make sure no trace chemicals, glue, or silicone oil ever leach into the liquid medicine over its multi-year shelf life.",\n        "technical": "Type I borosilicate or cyclic olefin polymer (COP) vials, fluoropolymer-coated stoppers, and USP <1663>/<1664> E&L risk assessments using LC-MS, GC-MS, and ICP-MS against Safety Concern Thresholds (SCT).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/container-closure-systems-packaging-human-drugs-and-biologics",\n    },\n]\n\nVALIDATION_PAT = [\n    {\n        "id": "val-3stage",\n        "name": "FDA 3-Stage Process Validation (Design -> PPQ -> CPV)",\n        "plain": "Factories don\'t just test the final pills—they engineer the process, prove it across consecutive full-scale batches (PPQ), and monitor every future batch statistically for life.",\n        "technical": "FDA 2011 Process Validation Guidance: Stage 1 (Process Design — QbD/DoE), Stage 2 (Process Qualification — IQ/OQ/PQ & PPQ batches), and Stage 3 (Continued Process Verification — CPV statistical process control / Cpk).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/process-validation-general-principles-and-practices",\n    },\n    {\n        "id": "val-pat",\n        "name": "Process Analytical Technology (PAT) & Real-Time Release Testing",\n        "plain": "Instead of scooping samples out of a blender and waiting days for a lab result, inline optical sensors measure moisture, potency, and mixing uniformity inside the machine every second.",\n        "technical": "FDA PAT Framework uses inline NIR/Raman spectroscopy, focused beam reflectance (FBRM), and multivariate control models to enable Real-Time Release Testing (RTRT) and feed-forward process control.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pat-framework-innovative-pharmaceutical-development-manufacturing-and-quality-assurance",\n    },\n    {\n        "id": "val-continuous",\n        "name": "Continuous Manufacturing (ICH Q13)",\n        "plain": "Traditional factories make drugs in stop-and-go batches that sit in drums between steps; continuous lines feed raw materials in one end and press finished tablets out the other nonstop.",\n        "technical": "ICH Q13 defines continuous manufacturing control strategies, Residence Time Distribution (RTD) material traceability, state-of-control diversion of out-of-spec segments, and flexible batch-size scaling.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q13-continuous-manufacturing-drug-substances-and-drug-products",\n    },\n    {\n        "id": "val-cip-sip",\n        "name": "Cleaning Validation, CIP / SIP & Cross-Contamination Control",\n        "plain": "When a multi-product factory switches from Medicine A to Medicine B, automated wash-and-steam cycles scrub every pipe and swab tests prove less than parts-per-million traces remain.",\n        "technical": "Clean-in-Place (CIP) and Steam-in-Place (SIP) validated against Health-Based Exposure Limits (HBEL / Permitted Daily Exposure, PDE) via swab/rinse TOC and HPLC recovery studies (21 CFR 211.67).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211",\n    },\n    {\n        "id": "val-single-use",\n        "name": "Single-Use Systems (SUS) & Closed Processing",\n        "plain": "Pre-sterilized disposable tubing, bags, and filter manifolds snap together with sterile connectors—cutting water/energy use and eliminating cross-contamination between biologic products.",\n        "technical": "Gamma- or X-ray-irradiated single-use assemblies require film integrity testing, particulate control (USP <788>), extractables profiling (BPOG/USP <665>), and supply-chain dual-sourcing.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/process-validation-general-principles-and-practices",\n    },\n    {\n        "id": "val-data-integrity",\n        "name": "Data Integrity (ALCOA+), MES & Electronic Batch Records",\n        "plain": "Every temperature reading, scale weight, and operator signature is locked automatically into a digital batch record so nothing can be erased, backdated, or mis-transcribed.",\n        "technical": "FDA Data Integrity Guidance enforces ALCOA+ (Attributable, Legible, Contemporaneous, Original, Accurate + Complete, Consistent, Enduring, Available) under 21 CFR Parts 11 and 211 via MES/eBR.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/data-integrity-and-compliance-drug-cgmp-questions-and-answers",\n    },\n]\n\n\ndef build_sterile_mfg(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on sterile pharmaceutical manufacturing, bioprocessing, ISO/EU Annex 1 cleanroom engineering, aseptic fill-finish, and process validation (FDA, eCFR, EMA, ICH). Educational reference only.",\n        "cleanroom_contamination": CLEANROOM_CONTAMINATION,\n        "bioprocessing": BIOPROCESSING,\n        "aseptic_fill_finish": ASEPTIC_FILL_FINISH,\n        "validation_pat": VALIDATION_PAT,\n    }\n    (data_dir / "sterile_mfg.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "cleanroom_contamination": len(CLEANROOM_CONTAMINATION),\n        "bioprocessing": len(BIOPROCESSING),\n        "aseptic_fill_finish": len(ASEPTIC_FILL_FINISH),\n        "validation_pat": len(VALIDATION_PAT),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_sterile_mfg(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
STERILE_MFG_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderBioprocessSvg() {\n  const nodes = [\n    { x: 8, label: "1. Cell Bank", sub: "MCB / WCB" },\n    { x: 140, label: "2. Bioreactor", sub: "SUB / Stainless" },\n    { x: 272, label: "3. Purify & Viral", sub: "Chrom / ICH Q5A" },\n    { x: 404, label: "4. ISO 5 Fill", sub: "Isolator / Lyo" },\n    { x: 536, label: "5. Inspect & CPV", sub: "CCIT / Release" },\n  ];\n  return html`<figure class="sterile-flow" aria-label="Sterile bioprocessing and aseptic fill-finish flow">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 3 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 3 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">End-to-end sterile biologics manufacturing from Master Cell Bank to ISO 5 aseptic fill-finish and CPV release.</figcaption>\n  </figure>`;\n}\n\nexport async function sterileMfgPage(query, mode = "ref") {\n  const doc = await getJSON("data/sterile_mfg.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/sterile" : "#/ref/sterile";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Sterile Manufacturing, Bioprocessing & Cleanroom Engineering",\n    body: html`\n      <h1>Sterile Manufacturing, Bioprocessing &amp; Cleanroom Engineering</h1>\n      <p class="lead">${mode === "explore"\n        ? "Inside modern sterile drug factories: how cleanrooms keep germs out, how living cells brew biologic medicines, how vials are filled and freeze-dried, and how factories prove every batch is identical."\n        : "Primary-sourced reference covering ISO 5–8 / EU Annex 1 cleanrooms & CCS, upstream/downstream bioprocessing, aseptic fill-finish & lyophilization, and 3-stage Process Validation / PAT / ICH Q13 continuous manufacturing (checked " + doc.checked + ")."}</p>\n\n      ${renderBioprocessSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=cleanroom"${sec === "cleanroom" ? \' aria-current="page"\' : ""}>Cleanrooms &amp; Annex 1 (6)</a> ·\n        <a href="${base}?section=bioprocessing"${sec === "bioprocessing" ? \' aria-current="page"\' : ""}>Bioprocessing (6)</a> ·\n        <a href="${base}?section=fillfinish"${sec === "fillfinish" ? \' aria-current="page"\' : ""}>Aseptic Fill &amp; Lyo (6)</a> ·\n        <a href="${base}?section=validation"${sec === "validation" ? \' aria-current="page"\' : ""}>Validation, PAT &amp; ICH Q13 (6)</a>\n      </p>\n\n      ${show("cleanroom") ? html`\n        <h2 id="cleanroom">1. Cleanroom Engineering, HVAC &amp; Contamination Control (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Cleanroom and contamination control">\n          <table class="tbl"><thead><tr><th>Engineering Pillar</th><th>${mode === "explore" ? "How It Keeps Medicine Sterile" : "Design & Regulatory Standard"}</th></tr></thead>\n          <tbody>${(doc.cleanroom_contamination || []).map((c) => html`<tr id="${c.id}">\n            <td><b><a href="${c.url}" target="_blank" rel="noopener">${c.name}</a></b></td>\n            <td>${mode === "explore" ? c.plain : html`${c.plain}<br><span class="muted small">${c.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("bioprocessing") ? html`\n        <h2 id="bioprocessing">2. Upstream &amp; Downstream Bioprocessing (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Upstream and downstream bioprocessing">\n          <table class="tbl"><thead><tr><th>Unit Operation</th><th>${mode === "explore" ? "What Happens" : "Process Engineering & ICH Standard"}</th></tr></thead>\n          <tbody>${(doc.bioprocessing || []).map((b) => html`<tr id="${b.id}">\n            <td><b><a href="${b.url}" target="_blank" rel="noopener">${b.name}</a></b></td>\n            <td>${mode === "explore" ? b.plain : html`${b.plain}<br><span class="muted small">${b.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("fillfinish") ? html`\n        <h2 id="fillfinish">3. Aseptic Fill-Finish, Sterilization &amp; Lyophilization (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Aseptic fill-finish and lyophilization">\n          <table class="tbl"><thead><tr><th>Fill-Finish Control</th><th>${mode === "explore" ? "How It Works" : "Technical & USP/FDA Requirement"}</th></tr></thead>\n          <tbody>${(doc.aseptic_fill_finish || []).map((f) => html`<tr id="${f.id}">\n            <td><b><a href="${f.url}" target="_blank" rel="noopener">${f.name}</a></b></td>\n            <td>${mode === "explore" ? f.plain : html`${f.plain}<br><span class="muted small">${f.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("validation") ? html`\n        <h2 id="validation">4. Process Validation, PAT &amp; Continuous Manufacturing (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Process validation and PAT">\n          <table class="tbl"><thead><tr><th>Quality &amp; Control System</th><th>${mode === "explore" ? "Why It Matters" : "Validation & Lifecycle Framework"}</th></tr></thead>\n          <tbody>${(doc.validation_pat || []).map((v) => html`<tr id="${v.id}">\n            <td><b><a href="${v.url}" target="_blank" rel="noopener">${v.name}</a></b></td>\n            <td>${mode === "explore" ? v.plain : html`${v.plain}<br><span class="muted small">${v.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/departments/manufacturing">Stage 6: Commercial Manufacturing</a> · <a href="#/ref/equipment">18 Hardware Classes</a> · <a href="#/ref/vendors">CDMO / Site Audits</a> · <a href="#/ref/ich">ICH Q1–Q12 Matrix</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { sterileMfgPage } from "./sterile_mfg.js";\n'
    if "./sterile_mfg.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/sterile"' not in txt:
        for anchor in ('if (path === "/ref/ip")', 'if (path === "/ref/safety")', 'if (path === "/ref/adme")', 'if (path === "/ref/trials")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/sterile") return sterileMfgPage(query, "ref");\n'
                    '  if (path === "/explore/sterile") return sterileMfgPage(query, "explore");\n'
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
    if "#/ref/sterile" not in txt:
        for anchor in ('["#/ref/ip", "Patents & IP"]', '["#/ref/safety", "Drug safety & PV"]', '["#/ref/equipment", "Equipment market"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/sterile", "Sterile & bioprocessing"]', 1)
                changed = True
                break
    if "#/explore/sterile" not in txt:
        for anchor in ('["#/explore/ip", "Patents & IP"]', '["#/explore/safety", "Drug safety & PV"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/sterile", "Sterile & bioprocessing"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_sterile_mfg.py" in txt:
        return False
    hook = "\n# v6.1m: Sterile Manufacturing, Bioprocessing & Cleanroom Engineering Reference\npython3 pipeline/build_sterile_mfg.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/sterile"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/sterile")\n'
        'def api_sterile_mfg():\n'
        '    return _read_json(SITE_DIR / "data" / "sterile_mfg.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"sterile_mfg.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    st_ref = _load(data_dir / "sterile_mfg.json", {}) or {}\n'
        '    for sec_key, sec_q in [("cleanroom_contamination", "cleanroom"), ("bioprocessing", "bioprocessing"), ("aseptic_fill_finish", "fillfinish"), ("validation_pat", "validation")]:\n'
        '        for item in (st_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "sterile_mfg",\n'
        '                "group": "Sterile Manufacturing & Bioprocessing",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/sterile?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/sterile?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"sterile cleanroom ISO Annex 1 bioprocessing aseptic lyophilization PAT {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"sterile", "#/ref/sterile"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    st_doc = _load_json(data_dir / "sterile_mfg.json")\n'
        '    if isinstance(st_doc, dict) and st_doc.get("cleanroom_contamination"):\n'
        '        st_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (st_doc.get("cleanroom_contamination") or []) + (st_doc.get("bioprocessing") or []))\n'
        '        pages.append(("sterile", "#/ref/sterile", "Sterile Manufacturing, Bioprocessing & Cleanroom Engineering",\n'
        '                      "Primary-sourced guide to ISO 5–8 / EU Annex 1 cleanrooms & CCS, isolators, upstream/downstream bioprocessing, ICH Q5A viral clearance, aseptic fill-finish, lyophilization, and PAT / ICH Q13.",\n'
        '                      f"<ul>{st_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/sterile"' in txt:
        return False
    for anchor in ('    "/#/explore/ip",', '    "/#/explore/safety",', '    "/#/explore/adme",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/sterile",\n    "/#/explore/sterile",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_sterile_mfg_py": _write_if_changed(pipe_dir / "build_sterile_mfg.py", BUILD_STERILE_PY),
        "sterile_mfg_js": _write_if_changed(js_dir / "sterile_mfg.js", STERILE_MFG_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/ip") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/ip", "Patents & IP"]] }];\nconst EXPLORE_NAV = [["#/explore/ip", "Patents & IP"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/ip",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_sterile_mfg.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_sterile_mfg.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"cleanroom_contamination": 6, "bioprocessing": 6, "aseptic_fill_finish": 6, "validation_pat": 6}, out

        doc = json.loads((root / "site" / "data" / "sterile_mfg.json").read_text(encoding="utf-8"))
        for k in ("cleanroom_contamination", "bioprocessing", "aseptic_fill_finish", "validation_pat"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61M_STERILE_BIOPROCESSING_CLEANROOM_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1m Sterile Manufacturing, Bioprocessing & Cleanroom Engineering patch.")
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
