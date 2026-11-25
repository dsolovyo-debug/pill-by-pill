#!/usr/bin/env python3
"""Pill by Pill v6.1r Patch: Rare Diseases, Orphan Drugs & Pediatric Development (#/ref/rare-pediatric, #/explore/rare-pediatric, /api/rare-pediatric).

1. Adds `pipeline/build_rare_pediatric.py` -> `site/data/rare_pediatric.json` (6 Orphan Drug / EU COMP
   incentives, 6 small-population trial & natural-history frameworks, 6 PREA/BPCA/PIP pediatric
   regulations, and 6 care-network/access pillars — 24 primary-sourced entries).
2. Adds `site/js/rare_pediatric.js` (`rarePediatricPage` with inline Pathway SVG + 4 section filters)
   and wires `#/ref/rare-pediatric`, `#/explore/rare-pediatric`, `/api/rare-pediatric`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `rare_pediatric.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/rare-pediatric/` static SEO page + sitemap entry -> 34
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1r_rare_diseases_orphan_pediatric_patch.py --selftest
  python3 2026-11-24_v6.1r_rare_diseases_orphan_pediatric_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_RARE_PED_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1r Rare Diseases, Orphan Drugs & Pediatric Development (`site/data/rare_pediatric.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Orphan Drug Designation & Rare Disease Incentives (6 pillars: Orphan Drug Act of 1983, 7-Year Orphan Exclusivity & Clinical Superiority, EU Orphan Designation & 10-Year Market Exclusivity, Rare Pediatric Disease PRVs, FDA Humanitarian & Accelerated Flexibility, Ultra-Rare N-of-1 & Bespoke Therapies)\n  2. Rare Disease Trial Design & Natural History (6 pillars: Small-Population Trial Statistics, Natural History & Disease Registries, Surrogate & Multi-Domain Endpoints, Patient-Focused Drug Development PFDD, Expanded Access / Right to Try, Newborn Screening RUSP Integration)\n  3. Pediatric Drug Development & Regulation (6 pillars: PREA Mandatory Pediatric Studies, BPCA Written Requests & +6-Month Exclusivity, EU Paediatric Investigation Plan PIP, Pediatric Extrapolation ICH E11A, Age-Appropriate Formulations & Taste Masking, Pediatric Oncology RACE for Children Act)\n  4. Rare & Pediatric Access, Care Networks & Support (6 pillars: Centers of Excellence & ERNs, Patient Advocacy & Venture Philanthropy, Genetic Diagnosis & Odyssey Reduction, High-Cost Ultra-Rare Contracting, Dose Weight-Banding & Off-Label Reality, Global Rare Disease Equity)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, EMA, NIH/NCATS, HRSA).\n\nUsage:\n  python3 pipeline/build_rare_pediatric.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nORPHAN_INCENTIVES = [\n    {\n        "id": "orp-oda-1983",\n        "name": "U.S. Orphan Drug Act of 1983 (<200,000 Prevalence)",\n        "plain": "Created financial incentives so drugmakers would invest in rare diseases affecting fewer than 200,000 Americans—transforming rare-disease R&D from nearly zero approvals into hundreds of therapies.",\n        "technical": "Codified in 21 CFR Part 316; grants Orphan Drug Designation (ODD) for rare diseases affecting <200,000 U.S. patients (or with no reasonable expectation of recovering U.S. R&D costs), providing 25% qualified clinical trial tax credits, PDUFA fee waivers, and 7-year exclusivity.",\n        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/designating-orphan-product-drugs-and-biological-products",\n    },\n    {\n        "id": "orp-7yr-exclusivity",\n        "name": "7-Year Orphan Drug Exclusivity (ODE) & Clinical Superiority",\n        "plain": "Once an orphan drug is approved, the FDA blocks identical copies for that exact rare disease for 7 years—unless a rival proves its version is meaningfully safer, more effective, or easier for patients.",\n        "technical": "Under 21 CFR 316.31–316.34, ODE blocks approval of the \'same drug\' for the \'same disease or condition\' for 7 years; a second sponsor can break ODE only by demonstrating Clinical Superiority (greater efficacy, greater safety, or major contribution to patient care).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-316",\n    },\n    {\n        "id": "orp-eu-comp",\n        "name": "EU Orphan Designation (EMA COMP) & 10-Year Market Exclusivity",\n        "plain": "In Europe, a rare condition affects no more than 5 in 10,000 people; approved orphan medicines earn 10 years of market exclusivity (12 years if pediatric studies are completed) plus protocol assistance.",\n        "technical": "Regulation (EC) No 141/2000 administered by EMA\'s Committee for Orphan Medicinal Products (COMP) requires life-threatening/chronically debilitating condition, <=5/10,000 EU prevalence, and significant benefit over existing methods.",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/orphan-designation-overview",\n    },\n    {\n        "id": "orp-prv",\n        "name": "Priority Review Vouchers (PRVs: Rare Pediatric & Tropical)",\n        "plain": "Developing a medicine for a rare pediatric or neglected tropical disease can earn a transferable \'fast-pass\' voucher that cuts a future FDA review from 10 months to 6 months—often sold for $100M+ to fund more R&D.",\n        "technical": "FD&C Act §§ 524 and 529 award transferable Priority Review Vouchers upon NDA/BLA approval for qualifying neglected tropical diseases, rare pediatric diseases, or medical countermeasures (subject to statutory reauthorization windows).",\n        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs",\n    },\n    {\n        "id": "orp-flexibility",\n        "name": "FDA Regulatory Flexibility & Single Adequate Trial Evidence",\n        "plain": "Because you cannot enroll 3,000 patients for a disease that only 200 people have, FDA law allows approvals based on a single well-controlled trial backed by strong biological confirmatory evidence.",\n        "technical": "FDA\'s 2023 Substantial Evidence & Rare Disease Guidances clarify how one adequate and well-controlled study plus confirmatory evidence (mechanistic/PD, natural history, or related indication data) satisfies FD&C Act § 505(d).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/rare-diseases-considerations-development-drugs-and-biological-products",\n    },\n    {\n        "id": "orp-nof1",\n        "name": "Ultra-Rare & Individualized (\'N-of-1\') Genetic Therapies",\n        "plain": "For mutations unique to a single child or a handful of families worldwide, FDA built specialized guidance for custom antisense oligonucleotides (ASOs) and bespoke gene-editing treatments.",\n        "technical": "FDA\'s Individualized Antisense Oligonucleotide Drug Products Guidance and CBER\'s Support for Clinical Trials Advancing Rare Disease Therapeutics (START) Pilot streamline nonclinical tox, CMC, and IND filing for ultra-rare N-of-1 interventions.",\n        "url": "https://www.fda.gov/drugs/news-events-human-drugs/fda-rare-disease-innovation-hub",\n    },\n]\n\nRARE_TRIALS = [\n    {\n        "id": "rt-small-pop",\n        "name": "Small-Population Trial Designs (Crossover, Randomized Withdrawal & Bayesian)",\n        "plain": "When only a few dozen patients exist, trials use clever designs—like letting every patient try the active medicine during part of the study or borrowing prior data—to get clear answers without wasting samples.",\n        "technical": "Employs randomized withdrawal designs, delayed-start designs, n-of-1 crossover cycles, and Bayesian borrowing of historical or adult data to maximize statistical efficiency under tight sample constraints.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/rare-diseases-considerations-development-drugs-and-biological-products",\n    },\n    {\n        "id": "rt-natural-history",\n        "name": "Natural History Studies & External Control Arms",\n        "plain": "Carefully tracking how an untreated rare disease progresses over years gives researchers a scientific yardstick—sometimes serving as an external comparison group when a placebo is unethical.",\n        "technical": "FDA Natural History Guidance recommends prospective longitudinal cohorts using standardized outcome instruments, baseline genotyping, and harmonized visit schedules to serve as trial design inputs or external controls.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/rare-diseases-natural-history-studies-drug-development",\n    },\n    {\n        "id": "rt-endpoints",\n        "name": "Rare-Disease Surrogate & Multi-Domain Clinical Endpoints",\n        "plain": "Because rare diseases often affect walking, breathing, vision, and cognition differently in every patient, trials combine functional tests and early biological markers to measure real-world stabilization.",\n        "technical": "Uses motor/functional scales (6MWT, NSAA, CHOP-INTEND, SARA), disease-specific biomarkers (e.g., micro-dystrophin, GAGs, neurofilament light chain), and Multi-Domain Responder Indexes (MDRI).",\n        "url": "https://www.fda.gov/drugs/development-resources/table-surrogate-endpoints-were-basis-drug-approval-or-licensure",\n    },\n    {\n        "id": "rt-pfdd",\n        "name": "Patient-Focused Drug Development (PFDD) & Voice of the Patient",\n        "plain": "FDA hosts dedicated listening sessions with rare-disease patients and caregivers so regulators understand which symptoms—like fatigue, choking, or loss of hand use—matter most in daily life.",\n        "technical": "Externally-Led PFDD meetings and FDA Patient Listening Sessions directly inform benefit-risk tolerance, meaningful change thresholds, and fit-for-purpose Clinical Outcome Assessments (COAs).",\n        "url": "https://www.fda.gov/drugs/development-approval-process-drugs/fda-patient-focused-drug-development-guidance-series-enhancing-incorporation-patients-voice-medical",\n    },\n    {\n        "id": "rt-expanded-access",\n        "name": "Expanded Access (\'Compassionate Use\') & Right to Try",\n        "plain": "Provides a regulated pathway for patients with life-threatening illnesses who cannot join a clinical trial to try an investigational medicine outside a study with their doctor\'s and FDA\'s oversight.",\n        "technical": "FDA Expanded Access (21 CFR Part 312 Subpart I: single-patient/emergency, intermediate-size, and treatment INDs) ensures IRB oversight and safety reporting; federal Right to Try Act (2018) offers an alternative post-Phase 1 route.",\n        "url": "https://www.fda.gov/news-events/public-health-focus/expanded-access",\n    },\n    {\n        "id": "rt-newborn-screening",\n        "name": "Newborn Screening (RUSP) & Pre-Symptomatic Intervention",\n        "plain": "Many genetic diseases cause irreversible damage within months of birth—so adding a condition to routine heel-prick newborn screening lets doctors treat babies before symptoms ever appear.",\n        "technical": "HRSA\'s Recommended Uniform Screening Panel (RUSP) evaluates newborn screening additions (e.g., SMA, SCID, Pompe, Krabbe) where early pre-symptomatic gene/ASO/enzyme therapy dramatically alters natural history.",\n        "url": "https://www.hrsa.gov/advisory-committees/heritable-disorders/rusp",\n    },\n]\n\nPEDIATRIC_REG = [\n    {\n        "id": "ped-prea",\n        "name": "PREA — Mandatory Pediatric Research Equity Act (2003)",\n        "plain": "Requires drugmakers developing a new adult medicine to also study how it works in children—unless the disease doesn\'t occur in kids or FDA grants a formal waiver or deferral.",\n        "technical": "FD&C Act § 505B requires an agreed Initial Pediatric Study Plan (iPSP) by End-of-Phase 2 for any new active ingredient, indication, dosage form, dosing regimen, or route; historically exempts orphan indications except pediatric oncology.",\n        "url": "https://www.fda.gov/drugs/development-resources/pediatric-product-development",\n    },\n    {\n        "id": "ped-bpca",\n        "name": "BPCA — Best Pharmaceuticals for Children Act (+6-Month Exclusivity)",\n        "plain": "To encourage voluntary children\'s studies even when not legally required (including for orphan drugs), Congress rewards companies with 6 extra months of market exclusivity across all existing patents.",\n        "technical": "FD&C Act § 505A authorizes FDA to issue a Written Request (WR) for pediatric studies; fairly responding to the WR earns 6 months of Pediatric Exclusivity attached to existing Orange Book patents/exclusivities or BPCIA 12-year biologic exclusivity.",\n        "url": "https://www.fda.gov/drugs/development-resources/pediatric-product-development",\n    },\n    {\n        "id": "ped-eu-pip",\n        "name": "EU Paediatric Investigation Plan (PIP) & PDCO",\n        "plain": "In Europe, developers must submit a binding children\'s study plan early—right after initial adult Phase 1 studies—to EMA\'s Paediatric Committee before they can apply for adult approval.",\n        "technical": "EU Paediatric Regulation (EC) No 1901/2006 mandates an agreed PIP (or waiver) reviewed by EMA\'s PDCO; completion grants a 6-month Supplementary Protection Certificate (SPC) extension or +2 years on EU orphan exclusivity (10 -> 12 yrs).",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/paediatric-medicines-overview",\n    },\n    {\n        "id": "ped-extrapolation",\n        "name": "Pediatric Extrapolation & Modeling (ICH E11A)",\n        "plain": "When a disease behaves the same way in children and adults, scientists use blood-level (PK) matching and computer modeling so kids don\'t have to undergo unnecessary placebo trials.",\n        "technical": "ICH E11A establishes a continuum of extrapolation (exposure-matching PK/PD bridging vs. Bayesian borrowing vs. standalone efficacy) grounded in disease similarity and exposure-response concordance.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e11a-pediatric-extrapolation",\n    },\n    {\n        "id": "ped-formulations",\n        "name": "Age-Appropriate Formulations, Excipient Safety & Taste Masking",\n        "plain": "Toddlers cannot swallow large adult capsules and some common adult inactive ingredients (like certain alcohols or preservatives) are toxic to newborns—requiring mini-tablets, granules, or masked liquids.",\n        "technical": "Pediatric CMC engineering balances swallowability (sprinkles, mini-tablets, oral dispersible films), palatability/taste-masking, accurate weight-based dosing devices, and neonatal excipient toxicity limits (benzyl alcohol, propylene glycol).",\n        "url": "https://www.fda.gov/drugs/development-resources/pediatric-product-development",\n    },\n    {\n        "id": "ped-race-act",\n        "name": "RACE for Children Act (Molecularly Targeted Pediatric Oncology)",\n        "plain": "Closed a major loophole so adult cancer drugs targeting a specific molecular driver must now also be tested in children\'s cancers sharing that same target—even if the adult organ cancer never occurs in kids.",\n        "technical": "Effective August 2020 (FDARA § 504), amends PREA to require pediatric molecularly targeted cancer investigations whenever an adult oncology drug\'s target is substantially relevant to pediatric cancer growth/progression, removing the orphan exemption.",\n        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/pediatric-oncology",\n    },\n]\n\nRARE_ACCESS = [\n    {\n        "id": "ra-coe-ern",\n        "name": "Centers of Excellence & European Reference Networks (ERNs)",\n        "plain": "Because a local clinic might see a specific rare disorder once in a decade, specialized national and European networks connect experts so knowledge travels instead of forcing sick families to move.",\n        "technical": "24 virtual European Reference Networks (ERNs) and U.S. NORD Rare Disease Centers of Excellence coordinate multidisciplinary diagnosis, standardized clinical care guidelines, and cross-border trial recruitment.",\n        "url": "https://rarediseases.info.nih.gov/",\n    },\n    {\n        "id": "ra-advocacy",\n        "name": "Patient Advocacy Groups & Venture Philanthropy",\n        "plain": "Parent-led foundations frequently jumpstart rare-disease research—funding early lab work, building patient registries, and co-investing in biotech startups (famously pioneering cystic fibrosis drugs).",\n        "technical": "Venture philanthropy models (e.g., Cystic Fibrosis Foundation\'s investment in Vertex\'s CFTR modulators) de-risk early translational biology, natural history datasets, and biobanks before institutional VC enters.",\n        "url": "https://ncats.nih.gov/research/research-activities/rdcrn",\n    },\n    {\n        "id": "ra-diagnostic-odyssey",\n        "name": "Ending the Rare-Disease \'Diagnostic Odyssey\' (WGS / WES)",\n        "plain": "Families with rare genetic conditions historically waited 5–7 years and saw half a dozen specialists for a diagnosis; rapid whole-genome sequencing in NICUs can now deliver answers in days.",\n        "technical": "Rapid Whole-Genome Sequencing (rWGS) and Whole-Exome Sequencing (WES) shorten time-to-diagnosis, identify actionable metabolic/genetic therapies, and feed variants into NIH ClinVar and Undiagnosed Diseases Network (UDN).",\n        "url": "https://rarediseases.info.nih.gov/",\n    },\n    {\n        "id": "ra-contracting",\n        "name": "High-Cost Ultra-Rare Pricing & Reinsurance Pools",\n        "plain": "When a tiny patient population drives $300k/year chronic or $2M+ one-time prices, insurers use stop-loss reinsurance, Medicaid outcomes pools, and patient assistance hubs to prevent coverage gaps.",\n        "technical": "Payer risk-mitigation includes stop-loss/carve-out reinsurance for self-funded employers, CMS Cell & Gene Therapy Access Model multi-state Medicaid contracting, and manufacturer free-drug/copay foundations.",\n        "url": "https://www.cms.gov/priorities/innovation/innovation-models/cgt",\n    },\n    {\n        "id": "ra-offlabel",\n        "name": "Pediatric Off-Label Prescribing & Weight-Based Dosing Reality",\n        "plain": "Even with PREA and BPCA, many older generic medicines lack formal pediatric labels—requiring hospital pharmacists to rely on pediatric dosing compendia and specialized weight-based calculations.",\n        "technical": "Neonatal and pediatric ICU prescribing frequently relies on off-label evidence, developmental PK/ontogeny (maturing renal GFR and hepatic CYP enzymes), and NIH NICHD Best Pharmaceuticals for Children Act off-patent studies.",\n        "url": "https://www.fda.gov/drugs/development-resources/pediatric-product-development",\n    },\n    {\n        "id": "ra-global-equity",\n        "name": "Global Rare-Disease Equity & Access Gaps",\n        "plain": "Over 300 million people worldwide live with one of 7,000+ rare diseases, yet fewer than 10% have an FDA-approved therapy—and access in low- and middle-income countries lags sharply behind high-income markets.",\n        "technical": "Global initiatives (WHO Resolution on Rare Diseases, IRDiRC 2027 goals, humanitarian access programs) work to expand newborn screening, diagnostic sequencing, and sustainable pricing beyond the U.S./EU/Japan.",\n        "url": "https://rarediseases.info.nih.gov/",\n    },\n]\n\n\ndef build_rare_pediatric(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on rare diseases, Orphan Drug Act & EU COMP incentives, small-population trials, and PREA/BPCA/PIP pediatric drug development (FDA, eCFR, EMA, NIH/NCATS, HRSA, CMS). Educational reference only.",\n        "orphan_incentives": ORPHAN_INCENTIVES,\n        "rare_trials": RARE_TRIALS,\n        "pediatric_reg": PEDIATRIC_REG,\n        "rare_access": RARE_ACCESS,\n    }\n    (data_dir / "rare_pediatric.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "orphan_incentives": len(ORPHAN_INCENTIVES),\n        "rare_trials": len(RARE_TRIALS),\n        "pediatric_reg": len(PEDIATRIC_REG),\n        "rare_access": len(RARE_ACCESS),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_rare_pediatric(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
RARE_PEDIATRIC_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderRarePedSvg() {\n  const nodes = [\n    { x: 8, label: "1. Diagnosis", sub: "rWGS / RUSP Screen" },\n    { x: 140, label: "2. Designate", sub: "ODD / EU COMP" },\n    { x: 272, label: "3. Small Trial", sub: "Natural History / PFDD" },\n    { x: 404, label: "4. Pediatric Plan", sub: "PREA / BPCA / PIP" },\n    { x: 536, label: "5. Access", sub: "7-Yr ODE / CoE" },\n  ];\n  return html`<figure class="rare-ped-flow" aria-label="Rare disease and pediatric drug development pathway">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 1 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 1 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Rare-disease and pediatric development pathway from genetic diagnosis and orphan designation to PREA/BPCA/PIP compliance and patient access.</figcaption>\n  </figure>`;\n}\n\nexport async function rarePediatricPage(query, mode = "ref") {\n  const doc = await getJSON("data/rare_pediatric.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/rare-pediatric" : "#/ref/rare-pediatric";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Rare Diseases, Orphan Drugs & Pediatric Development",\n    body: html`\n      <h1>Rare Diseases, Orphan Drugs &amp; Pediatric Development</h1>\n      <p class="lead">${mode === "explore"\n        ? "How special laws encourage companies to build medicines for rare conditions affecting small groups of patients—and how regulators make sure medicines are safely tested and formulated for children."\n        : "Primary-sourced reference covering 6 Orphan Drug & rare-disease incentives, 6 small-population trial & natural-history strategies, 6 PREA/BPCA/PIP pediatric frameworks, and 6 care-network & access pillars (checked " + doc.checked + ")."}</p>\n\n      ${renderRarePedSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=orphan"${sec === "orphan" ? \' aria-current="page"\' : ""}>Orphan Incentives (6)</a> ·\n        <a href="${base}?section=trials"${sec === "trials" ? \' aria-current="page"\' : ""}>Small-Pop Trials (6)</a> ·\n        <a href="${base}?section=pediatric"${sec === "pediatric" ? \' aria-current="page"\' : ""}>Pediatric PREA/BPCA/PIP (6)</a> ·\n        <a href="${base}?section=access"${sec === "access" ? \' aria-current="page"\' : ""}>Care &amp; Access (6)</a>\n      </p>\n\n      ${show("orphan") ? html`\n        <h2 id="orphan">1. Orphan Drug Designation &amp; Rare-Disease Incentives (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Orphan drug incentives">\n          <table class="tbl"><thead><tr><th>Incentive / Pathway</th><th>${mode === "explore" ? "How It Encourages Rare R&D" : "Statutory & Regulatory Criteria"}</th></tr></thead>\n          <tbody>${(doc.orphan_incentives || []).map((o) => html`<tr id="${o.id}">\n            <td><b><a href="${o.url}" target="_blank" rel="noopener">${o.name}</a></b></td>\n            <td>${mode === "explore" ? o.plain : html`${o.plain}<br><span class="muted small">${o.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("trials") ? html`\n        <h2 id="trials">2. Rare-Disease Clinical Trials, Natural History &amp; PFDD (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Rare disease clinical trials">\n          <table class="tbl"><thead><tr><th>Methodology</th><th>${mode === "explore" ? "How It Works for Small Groups" : "Study Design & Evidence Standard"}</th></tr></thead>\n          <tbody>${(doc.rare_trials || []).map((t) => html`<tr id="${t.id}">\n            <td><b><a href="${t.url}" target="_blank" rel="noopener">${t.name}</a></b></td>\n            <td>${mode === "explore" ? t.plain : html`${t.plain}<br><span class="muted small">${t.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("pediatric") ? html`\n        <h2 id="pediatric">3. Pediatric Drug Development &amp; Regulation (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pediatric drug development">\n          <table class="tbl"><thead><tr><th>Pediatric Framework</th><th>${mode === "explore" ? "How It Protects Children" : "PREA, BPCA, PIP & Formulation Science"}</th></tr></thead>\n          <tbody>${(doc.pediatric_reg || []).map((p) => html`<tr id="${p.id}">\n            <td><b><a href="${p.url}" target="_blank" rel="noopener">${p.name}</a></b></td>\n            <td>${mode === "explore" ? p.plain : html`${p.plain}<br><span class="muted small">${p.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("access") ? html`\n        <h2 id="access">4. Rare &amp; Pediatric Care Networks, Advocacy &amp; Access (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Rare and pediatric access">\n          <table class="tbl"><thead><tr><th>Ecosystem Pillar</th><th>${mode === "explore" ? "How Families Get Support" : "Diagnosis, Care Networks & Contracting"}</th></tr></thead>\n          <tbody>${(doc.rare_access || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/pathways">Approval Pathways &amp; Exclusivities</a> · <a href="#/ref/atmp">Vaccines &amp; Cell/Gene Therapy</a> · <a href="#/ref/trials">Clinical Trials &amp; Endpoints</a> · <a href="#/ref/rwe">RWE &amp; Registries</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { rarePediatricPage } from "./rare_pediatric.js";\n'
    if "./rare_pediatric.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/rare-pediatric"' not in txt:
        for anchor in ('if (path === "/ref/rwe")', 'if (path === "/ref/atmp")', 'if (path === "/ref/cdx")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/rare-pediatric") return rarePediatricPage(query, "ref");\n'
                    '  if (path === "/explore/rare-pediatric") return rarePediatricPage(query, "explore");\n'
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
    if "#/ref/rare-pediatric" not in txt:
        for anchor in ('["#/ref/rwe", "RWE & digital health"]', '["#/ref/atmp", "Vaccines & cell/gene"]', '["#/ref/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/rare-pediatric", "Rare & pediatric"]', 1)
                changed = True
                break
    if "#/explore/rare-pediatric" not in txt:
        for anchor in ('["#/explore/rwe", "RWE & digital health"]', '["#/explore/atmp", "Vaccines & cell/gene"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/rare-pediatric", "Rare & pediatric"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_rare_pediatric.py" in txt:
        return False
    hook = "\n# v6.1r: Rare Diseases, Orphan Drugs & Pediatric Development\npython3 pipeline/build_rare_pediatric.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/rare-pediatric"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/rare-pediatric")\n'
        'def api_rare_pediatric():\n'
        '    return _read_json(SITE_DIR / "data" / "rare_pediatric.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rare_pediatric.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    rp_ref = _load(data_dir / "rare_pediatric.json", {}) or {}\n'
        '    for sec_key, sec_q in [("orphan_incentives", "orphan"), ("rare_trials", "trials"), ("pediatric_reg", "pediatric"), ("rare_access", "access")]:\n'
        '        for item in (rp_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "rare_pediatric",\n'
        '                "group": "Rare Diseases & Pediatric Development",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/rare-pediatric?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/rare-pediatric?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"rare disease orphan drug pediatric PREA BPCA PIP PRV RUSP newborn screening N-of-1 {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rare-pediatric", "#/ref/rare-pediatric"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    rp_doc = _load_json(data_dir / "rare_pediatric.json")\n'
        '    if isinstance(rp_doc, dict) and rp_doc.get("orphan_incentives"):\n'
        '        rp_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (rp_doc.get("orphan_incentives") or []) + (rp_doc.get("pediatric_reg") or []))\n'
        '        pages.append(("rare-pediatric", "#/ref/rare-pediatric", "Rare Diseases, Orphan Drugs & Pediatric Development",\n'
        '                      "Primary-sourced guide to the Orphan Drug Act, 7-year ODE, EU COMP, Priority Review Vouchers, small-population trials, PREA/BPCA/PIP pediatric regulations, and newborn screening.",\n'
        '                      f"<ul>{rp_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/rare-pediatric"' in txt:
        return False
    for anchor in ('    "/#/explore/rwe",', '    "/#/explore/atmp",', '    "/#/explore/cdx",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/rare-pediatric",\n    "/#/explore/rare-pediatric",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_rare_pediatric_py": _write_if_changed(pipe_dir / "build_rare_pediatric.py", BUILD_RARE_PED_PY),
        "rare_pediatric_js": _write_if_changed(js_dir / "rare_pediatric.js", RARE_PEDIATRIC_JS),
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
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/rwe", "RWE & digital health"]] }];\nconst EXPLORE_NAV = [["#/explore/rwe", "RWE & digital health"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/rwe",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_rare_pediatric.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_rare_pediatric.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"orphan_incentives": 6, "rare_trials": 6, "pediatric_reg": 6, "rare_access": 6}, out

        doc = json.loads((root / "site" / "data" / "rare_pediatric.json").read_text(encoding="utf-8"))
        for k in ("orphan_incentives", "rare_trials", "pediatric_reg", "rare_access"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61R_RARE_DISEASES_ORPHAN_PEDIATRIC_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1r Rare Diseases, Orphan Drugs & Pediatric Development patch.")
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
