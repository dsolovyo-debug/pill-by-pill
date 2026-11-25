#!/usr/bin/env python3
"""Pill by Pill v6.1x Patch: Antimicrobial Resistance (AMR), Stewardship & Anti-Infective Economics (#/ref/amr, #/explore/amr, /api/amr).

1. Adds `pipeline/build_amr.py` -> `site/data/amr.json` (6 AMR biological mechanisms, 6 broken-market
   & push/pull incentive policies, 6 stewardship/One Health/WHO AWaRe pillars, and 6 next-gen
   anti-infective modalities — 24 primary-sourced entries anchored to CDC/FDA/WHO/NICE/PMC).
2. Adds `site/js/amr.js` (`amrPage` with inline AMR Cycle SVG + 4 section filters) and wires
   `#/ref/amr`, `#/explore/amr`, `/api/amr`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `amr.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/amr/` static SEO page + sitemap -> 39 encyclopedia SEO pages),
   and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1x_amr_stewardship_antiinfective_economics_patch.py --selftest
  python3 2026-11-24_v6.1x_amr_stewardship_antiinfective_economics_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_AMR_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1x Antimicrobial Resistance (AMR), Stewardship & Anti-Infective Economics (`site/data/amr.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Mechanisms of Antimicrobial Resistance (6 pillars: Beta-Lactamases/ESBL/CRE, Efflux Pumps & Porin Loss, Target-Site Modification MRSA/VRE, Biofilms & Persisters, Horizontal Gene Transfer, WHO Priority & ESKAPE Pathogens)\n  2. The Broken Antibiotic Market & Policy Incentives (6 pillars: Stewardship Paradox & Volume Trap, Push Incentives CARB-X/BARDA/GARDP, Pull Incentives UK NHS Subscription / PASTEUR, GAIN Act QIDP +5-Yr Exclusivity, FDA LPAD Limited Population Pathway, Generic Antibiotic Supply Fragility)\n  3. Antimicrobial Stewardship & Rapid Diagnostics (6 pillars: CDC Core Elements of Hospital ASP, Rapid Molecular AST Diagnostics, PK/PD Dosing Optimization, WHO AWaRe Classification, One Health Agricultural Stewardship, Global WHO GLASS Surveillance)\n  4. Next-Generation Anti-Infective Modalities (6 pillars: Beta-Lactam / Beta-Lactamase Inhibitor Combos, Bacteriophage Therapy, Anti-Infective Monoclonal Antibodies, Microbiome & Live Biotherapeutic Products LBPs, Broad-Spectrum Antivirals, AI-Guided Antibiotic Discovery)\n\nAll anchors are verified HTTPS primary sources (CDC, FDA, WHO, NICE, NIH/PMC).\n\nUsage:\n  python3 pipeline/build_amr.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nAMR_MECHANISMS = [\n    {\n        "id": "amr-betalactamase",\n        "name": "Drug-Destroying Enzymes (Beta-Lactamases, ESBL & CRE)",\n        "plain": "Resistant bacteria evolve molecular scissors—like carbapenemases—that slice open penicillin and cephalosporin rings before the antibiotic can ever reach its target.",\n        "technical": "Extended-Spectrum Beta-Lactamases (ESBLs) and Carbapenem-Resistant Enterobacterales (CRE: KPC, NDM, OXA-48) hydrolyze beta-lactam rings, requiring novel beta-lactamase inhibitors.",\n        "url": "https://www.cdc.gov/antimicrobial-resistance/about/index.html",\n    },\n    {\n        "id": "amr-efflux-porin",\n        "name": "Efflux Pumps & Outer-Membrane Porin Loss",\n        "plain": "Gram-negative bacteria can slam shut the microscopic doors (porins) that let antibiotics in—or run cellular bilge pumps (efflux pumps) that eject the drug faster than it enters.",\n        "technical": "RND-family multidrug efflux pumps (e.g., MexAB-OprM in Pseudomonas aeruginosa) paired with OprD porin downregulation confer broad cross-resistance across multiple antibiotic classes.",\n        "url": "https://www.cdc.gov/antimicrobial-resistance/about/index.html",\n    },\n    {\n        "id": "amr-target-mod",\n        "name": "Target-Site Modification (MRSA, VRE & Ribosomal Mutations)",\n        "plain": "Bacteria subtly reshape the protein lock an antibiotic binds to—so the drug key no longer fits, while the bacterium keeps growing normally.",\n        "technical": "Examples include mecA-encoded PBP2a in MRSA (low beta-lactam affinity), VanA/VanB D-Ala-D-Lac cell-wall remodeling in VRE, and gyrA/parC mutations conferring fluoroquinolone resistance.",\n        "url": "https://www.cdc.gov/antimicrobial-resistance/about/index.html",\n    },\n    {\n        "id": "amr-biofilms",\n        "name": "Biofilms & Dormant Persister Cells",\n        "plain": "Bacteria coating artificial joints, catheters, or chronic wounds build a slimy shield (biofilm) and enter a slow-growing state where standard antibiotics struggle to kill them.",\n        "technical": "Extracellular polymeric substance (EPS) matrices restrict antibiotic diffusion and harbor metabolically tolerant persister subpopulations requiring prolonged therapy or hardware removal.",\n        "url": "https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance",\n    },\n    {\n        "id": "amr-hgt",\n        "name": "Horizontal Gene Transfer (Plasmids & Transposons)",\n        "plain": "Bacteria don\'t have to wait for slow random mutations—they can trade mobile loops of resistance DNA (plasmids) directly with neighboring species like swapping trading cards.",\n        "technical": "Conjugative plasmids, integrons, and transposons rapidly disseminate multi-drug resistance cassettes (e.g., blaNDM-1, mcr-1) across unrelated Gram-negative species.",\n        "url": "https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance",\n    },\n    {\n        "id": "amr-eskape",\n        "name": "ESKAPE Pathogens & WHO Bacterial Priority Pathogens List",\n        "plain": "Six notorious hospital bacteria (Enterococcus, Staph, Klebsiella, Acinetobacter, Pseudomonas, Enterobacter) account for the bulk of hard-to-treat, life-threatening resistant infections.",\n        "technical": "WHO\'s 2024 Bacterial Priority Pathogens List (BPPL) ranks Critical-priority threats (carbapenem-resistant Acinetobacter baumannii, CRE, rifampin-resistant TB) to focus global R&D.",\n        "url": "https://www.who.int/publications/i/item/9789240093461",\n    },\n]\n\nAMR_ECONOMICS = [\n    {\n        "id": "econ-stewardship-paradox",\n        "name": "The Stewardship Paradox & Broken Volume-Based Revenue",\n        "plain": "When a company spends $1 billion inventing a life-saving new reserve antibiotic, hospitals wisely lock it in the cabinet for rare emergencies—causing the company to go bankrupt from tiny sales.",\n        "technical": "Unlike chronic oncology or metabolic drugs, novel reserve antibiotics are used for 7–14 days in small numbers of resistant cases, decoupling public-health insurance value from unit sales volume.",\n        "url": "https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance",\n    },\n    {\n        "id": "econ-push",\n        "name": "Push Incentives (CARB-X, BARDA & GARDP)",\n        "plain": "Governments and global charities fund early antibiotic lab work and clinical trials directly so small biotech teams can survive the expensive early years.",\n        "technical": "Non-dilutive R&D grants from CARB-X (preclinical/Phase 1), HHS BARDA (late-stage/biodefense), and GARDP (global access) lower upfront developer capital risk.",\n        "url": "https://www.fda.gov/emergency-preparedness-and-response/mcm-issues/antimicrobial-resistance-information-fda",\n    },\n    {\n        "id": "econ-pull-subscription",\n        "name": "Pull Incentives: UK NHS Subscription Model & Delinked Payments",\n        "plain": "Instead of paying per pill, the UK NHS pays a fixed annual \'fire-department subscription fee\' for access to a breakthrough reserve antibiotic—rewarding readiness without encouraging overuse.",\n        "technical": "NICE/NHS England\'s delinked subscription model pays up to £20M/year based on health-technology value rather than volume; similar U.S. proposals (PASTEUR Act) aim to stabilize the global pipeline.",\n        "url": "https://www.nice.org.uk/about/what-we-do/life-sciences/nice-advice-service/models-for-the-evaluation-and-purchase-of-antimicrobials",\n    },\n    {\n        "id": "econ-gain-qidp",\n        "name": "GAIN Act (2012) — QIDP +5-Year Exclusivity",\n        "plain": "Gives Qualified Infectious Disease Products (QIDPs) targeting serious resistant pathogens Priority Review, Fast Track, and 5 extra years of statutory exclusivity.",\n        "technical": "Generating Antibiotic Incentives Now (GAIN) Act adds +5 years to NCE/3-year/Orphan exclusivity, though market experience showed extra exclusivity alone cannot fix low early sales volume.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-3-clinical-research",\n    },\n    {\n        "id": "econ-lpad",\n        "name": "FDA LPAD (Limited Population Pathway for Antibacterial & Antifungal Drugs)",\n        "plain": "Lets FDA approve a desperately needed antibiotic for a small, high-risk group of patients with no other options using smaller, faster clinical trials—clearly labeled \'Limited Population.\'",\n        "technical": "Enacted under the 21st Century Cures Act (FD&C Act § 506(h)); streamlines benefit-risk review for serious/life-threatening infections in narrow patient populations.",\n        "url": "https://www.fda.gov/drugs/development-resources/limited-population-pathway-antibacterial-and-antifungal-drugs-lpad-pathway",\n    },\n    {\n        "id": "econ-generic-fragility",\n        "name": "Generic Antibiotic Supply-Chain Fragility & Shortages",\n        "plain": "Older workhorse antibiotics (like amoxicillin or injectable penicillin) sell for pennies, leaving only a handful of global API factories—so one plant shutdown can trigger nationwide shortages.",\n        "technical": "Low-margin generic sterile injectables face chronic shortage risk tracked on the FDA Drug Shortages database, driving policy focus on domestic/diversified API manufacturing.",\n        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages",\n    },\n]\n\nSTEWARDSHIP_DX = [\n    {\n        "id": "stew-cdc-asp",\n        "name": "CDC Core Elements of Hospital Antibiotic Stewardship (ASP)",\n        "plain": "Hospital teams of infectious-disease doctors and pharmacists review prescriptions daily to make sure patients get the right drug, right dose, and shortest effective duration.",\n        "technical": "CMS Conditions of Participation require U.S. hospitals to maintain Antimicrobial Stewardship Programs (ASPs) implementing CDC Core Elements (leadership, pharmacy expertise, tracking, reporting, education).",\n        "url": "https://www.cdc.gov/antibiotic-use/hcp/core-elements/hospital.html",\n    },\n    {\n        "id": "stew-rapid-dx",\n        "name": "Rapid Molecular Diagnostics & Phenotypic AST",\n        "plain": "Traditional petri-dish lab cultures take 2–3 days—forcing doctors to guess with broad antibiotics first. Rapid molecular tests identify the bug and resistance genes in 1–4 hours.",\n        "technical": "Multiplex PCR blood-culture panels, MALDI-TOF mass spectrometry, and rapid phenotypic Antimicrobial Susceptibility Testing (AST) accelerate targeted de-escalation.",\n        "url": "https://www.cdc.gov/antimicrobial-resistance/about/index.html",\n    },\n    {\n        "id": "stew-pkpd",\n        "name": "PK/PD Dosing Optimization (fT>MIC, AUC/MIC, Cmax/MIC)",\n        "plain": "Giving the exact same antibiotic as a slower extended IV drip instead of a quick push can keep blood levels above the bacteria-killing threshold longer and prevent resistance.",\n        "technical": "Optimizes time-dependent (beta-lactam fT>MIC via extended/continuous infusion), concentration-dependent (aminoglycoside Cmax/MIC), and exposure-dependent (vancomycin AUC/MIC) pharmacodynamics.",\n        "url": "https://www.fda.gov/drugs/development-resources/antibacterial-susceptibility-test-interpretive-criteria",\n    },\n    {\n        "id": "stew-who-aware",\n        "name": "WHO AWaRe Classification (Access, Watch, Reserve)",\n        "plain": "WHO sorts antibiotics into three traffic-light tiers: Access (everyday first-choice drugs), Watch (higher resistance risk), and Reserve (last-resort hospital drugs).",\n        "technical": "Global stewardship benchmark targeting >=60–70% of national human antibiotic consumption from the Access group while protecting Reserve agents.",\n        "url": "https://www.who.int/publications/i/item/WHO-MHP-HPS-EML-2023.04",\n    },\n    {\n        "id": "stew-one-health",\n        "name": "One Health: Human, Veterinary & Environmental Stewardship",\n        "plain": "Because resistant bacteria move freely between farms, food, wastewater, and hospitals, FDA phased out medically important antibiotics for livestock growth promotion.",\n        "technical": "FDA Guidance for Industry #213 and #263 transitioned medically important veterinary antimicrobials to Veterinary Feed Directive (VFD) / prescription oversight.",\n        "url": "https://www.fda.gov/animal-veterinary/antimicrobial-resistance",\n    },\n    {\n        "id": "stew-glass",\n        "name": "Global Resistance Surveillance (WHO GLASS & CDC AR Lab Network)",\n        "plain": "Tracks resistant superbugs across countries and hospital networks in real time so public-health teams can contain new outbreaks before they spread worldwide.",\n        "technical": "WHO Global Antimicrobial Resistance and Use Surveillance System (GLASS) and CDC\'s Antimicrobial Resistance Laboratory Network standardize susceptibility and genomic tracking.",\n        "url": "https://www.who.int/initiatives/glass",\n    },\n]\n\nNEXTGEN_ANTIINFECTIVES = [\n    {\n        "id": "ng-bl-bli",\n        "name": "Novel Beta-Lactam / Beta-Lactamase Inhibitor Combinations",\n        "plain": "Pairs a proven antibiotic with a \'bodyguard\' molecule that blocks bacterial resistance enzymes so the antibiotic can kill superbugs again.",\n        "technical": "Modern combinations (e.g., ceftazidime-avibactam, meropenem-vaborbactam, cefepime-enmetazobactam, sulbactam-durlobactam) restore activity against ESBL, KPC, and carbapenem-resistant Acinetobacter.",\n        "url": "https://www.fda.gov/emergency-preparedness-and-response/mcm-issues/antimicrobial-resistance-information-fda",\n    },\n    {\n        "id": "ng-phage",\n        "name": "Bacteriophage Therapy (Viruses That Hunt Specific Bacteria)",\n        "plain": "Uses natural or engineered viruses that infect ONLY a specific disease-causing bacterium—leaving human cells and helpful gut bacteria untouched.",\n        "technical": "Regulated by FDA CBER as biological products; currently advancing through Phase 1/2 clinical trials and single-patient Expanded Access INDs for refractory prosthetic-joint and cystic fibrosis infections.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products",\n    },\n    {\n        "id": "ng-mabs",\n        "name": "Anti-Infective Monoclonal Antibodies",\n        "plain": "Engineered antibodies neutralize bacterial toxins (like C. difficile toxin) or block viruses (like RSV in infants) without driving classic broad-spectrum bacterial resistance.",\n        "technical": "Long-half-life Fc-engineered mAbs (e.g., nirsevimab for RSV, bezlotoxumab for C. difficile) provide targeted passive prophylaxis or adjunct toxin neutralization.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n    {\n        "id": "ng-lbp",\n        "name": "Microbiome & Live Biotherapeutic Products (LBPs)",\n        "plain": "Restores healthy protective gut bacteria after heavy antibiotic courses to crowd out recurrent, life-threatening C. difficile infections.",\n        "technical": "FDA CBER-approved microbiota therapies (e.g., fecal microbiota live-jslm and live-brpk) regulated under Live Biotherapeutic Products CMC and donor-screening standards.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/fecal-microbiota-products",\n    },\n    {\n        "id": "ng-antivirals",\n        "name": "Direct-Acting & Broad-Spectrum Antiviral Platforms",\n        "plain": "Targets conserved viral enzymes (polymerases and proteases) so oral pills can stop respiratory or pandemic viruses early before severe hospitalization.",\n        "technical": "Structure-guided protease and nucleoside-analog polymerase inhibitors (e.g., nirmatrelvir, remdesivir, sofosbuvir) paired with rapid resistance-barrier profiling.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9425786/",\n    },\n    {\n        "id": "ng-ai-abx",\n        "name": "AI-Guided Structural Antibiotic Discovery",\n        "plain": "Deep-learning models screen hundreds of millions of virtual chemical structures in days to spot brand-new antibiotic scaffolds that don\'t look like any older drug.",\n        "technical": "Graph neural networks and generative models (e.g., halicin, abaucin research milestones) expand chemical space beyond legacy soil-actinomycete scaffolds.",\n        "url": "https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance",\n    },\n]\n\n\ndef build_amr(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on antimicrobial resistance (AMR) biology, broken antibiotic market economics, push/pull incentives, hospital stewardship, and next-generation anti-infectives (CDC, FDA, WHO, NICE, NIH PMC). Educational reference only.",\n        "amr_mechanisms": AMR_MECHANISMS,\n        "amr_economics": AMR_ECONOMICS,\n        "stewardship_dx": STEWARDSHIP_DX,\n        "nextgen_antiinfectives": NEXTGEN_ANTIINFECTIVES,\n    }\n    (data_dir / "amr.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "amr_mechanisms": len(AMR_MECHANISMS),\n        "amr_economics": len(AMR_ECONOMICS),\n        "stewardship_dx": len(STEWARDSHIP_DX),\n        "nextgen_antiinfectives": len(NEXTGEN_ANTIINFECTIVES),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_amr(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
AMR_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderAmrSvg() {\n  const nodes = [\n    { x: 8, label: "1. Resistance", sub: "ESKAPE / Plasmids" },\n    { x: 140, label: "2. Push / Pull", sub: "CARB-X / NHS Sub" },\n    { x: 272, label: "3. Fast Review", sub: "QIDP / LPAD" },\n    { x: 404, label: "4. Stewardship", sub: "AWaRe / Rapid AST" },\n    { x: 536, label: "5. Next-Gen", sub: "BLI / Phage / LBP" },\n  ];\n  return html`<figure class="amr-flow" aria-label="Antimicrobial resistance, incentives, and stewardship cycle">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 1 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 1 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Addressing Antimicrobial Resistance (AMR) requires pairing molecular biology with delinked market incentives and hospital stewardship.</figcaption>\n  </figure>`;\n}\n\nexport async function amrPage(query, mode = "ref") {\n  const doc = await getJSON("data/amr.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/amr" : "#/ref/amr";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Antimicrobial Resistance (AMR), Stewardship & Anti-Infective Economics",\n    body: html`\n      <h1>Antimicrobial Resistance (AMR), Stewardship &amp; Anti-Infective Economics</h1>\n      <p class="lead">${mode === "explore"\n        ? "How bacteria evolve resistance to antibiotics, why inventing new antibiotics is economically broken, how hospitals protect existing drugs, and what next-generation therapies are coming."\n        : "Primary-sourced reference covering 6 AMR molecular mechanisms, 6 antibiotic market/push-pull incentive frameworks, 6 stewardship & rapid-diagnostic pillars, and 6 next-generation anti-infective modalities (checked " + doc.checked + ")."}</p>\n\n      ${renderAmrSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=mechanisms"${sec === "mechanisms" ? \' aria-current="page"\' : ""}>AMR Biology (6)</a> ·\n        <a href="${base}?section=economics"${sec === "economics" ? \' aria-current="page"\' : ""}>Market &amp; Incentives (6)</a> ·\n        <a href="${base}?section=stewardship"${sec === "stewardship" ? \' aria-current="page"\' : ""}>Stewardship &amp; One Health (6)</a> ·\n        <a href="${base}?section=nextgen"${sec === "nextgen" ? \' aria-current="page"\' : ""}>Next-Gen Modalities (6)</a>\n      </p>\n\n      ${show("mechanisms") ? html`\n        <h2 id="mechanisms">1. Mechanisms of Antimicrobial Resistance (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="AMR mechanisms">\n          <table class="tbl"><thead><tr><th>Mechanism / Threat</th><th>${mode === "explore" ? "How Bacteria Evade Drugs" : "Molecular Biology & Clinical Impact"}</th></tr></thead>\n          <tbody>${(doc.amr_mechanisms || []).map((m) => html`<tr id="${m.id}">\n            <td><b><a href="${m.url}" target="_blank" rel="noopener">${m.name}</a></b></td>\n            <td>${mode === "explore" ? m.plain : html`${m.plain}<br><span class="muted small">${m.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("economics") ? html`\n        <h2 id="economics">2. The Broken Antibiotic Market &amp; Policy Incentives (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Antibiotic economics and incentives">\n          <table class="tbl"><thead><tr><th>Economic Dynamic / Policy</th><th>${mode === "explore" ? "Why New Antibiotics Need Special Support" : "Push/Pull Incentives & Regulatory Pathways"}</th></tr></thead>\n          <tbody>${(doc.amr_economics || []).map((e) => html`<tr id="${e.id}">\n            <td><b><a href="${e.url}" target="_blank" rel="noopener">${e.name}</a></b></td>\n            <td>${mode === "explore" ? e.plain : html`${e.plain}<br><span class="muted small">${e.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("stewardship") ? html`\n        <h2 id="stewardship">3. Antimicrobial Stewardship, Rapid Diagnostics &amp; One Health (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Antimicrobial stewardship">\n          <table class="tbl"><thead><tr><th>Stewardship Pillar</th><th>${mode === "explore" ? "How It Preserves Antibiotics" : "Clinical, Diagnostic & Surveillance Standards"}</th></tr></thead>\n          <tbody>${(doc.stewardship_dx || []).map((s) => html`<tr id="${s.id}">\n            <td><b><a href="${s.url}" target="_blank" rel="noopener">${s.name}</a></b></td>\n            <td>${mode === "explore" ? s.plain : html`${s.plain}<br><span class="muted small">${s.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("nextgen") ? html`\n        <h2 id="nextgen">4. Next-Generation Anti-Infective Modalities (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Next-generation anti-infectives">\n          <table class="tbl"><thead><tr><th>Modality</th><th>${mode === "explore" ? "How It Fights Resistant Infections" : "Scientific & Regulatory Status"}</th></tr></thead>\n          <tbody>${(doc.nextgen_antiinfectives || []).map((n) => html`<tr id="${n.id}">\n            <td><b><a href="${n.url}" target="_blank" rel="noopener">${n.name}</a></b></td>\n            <td>${mode === "explore" ? n.plain : html`${n.plain}<br><span class="muted small">${n.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/economics">Drug Economics</a> · <a href="#/ref/pathways">Approval Pathways (QIDP)</a> · <a href="#/ref/atmp">Vaccines &amp; Biologics</a> · <a href="#/ref/history-laws">History &amp; Penicillin Era</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { amrPage } from "./amr.js";\n'
    if "./amr.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/amr"' not in txt:
        for anchor in ('if (path === "/ref/history-laws")', 'if (path === "/ref/careers")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/amr") return amrPage(query, "ref");\n'
                    '  if (path === "/explore/amr") return amrPage(query, "explore");\n'
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
    if "#/ref/amr" not in txt:
        for anchor in ('["#/ref/history-laws", "History & safety laws"]', '["#/ref/careers", "Careers & roles"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/amr", "AMR & antibiotics"]', 1)
                changed = True
                break
    if "#/explore/amr" not in txt:
        for anchor in ('["#/explore/history-laws", "History & safety laws"]', '["#/explore/careers", "Careers & roles"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/amr", "AMR & antibiotics"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_amr.py" in txt:
        return False
    hook = "\n# v6.1x: Antimicrobial Resistance (AMR), Stewardship & Anti-Infective Economics\npython3 pipeline/build_amr.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/amr"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/amr")\n'
        'def api_amr():\n'
        '    return _read_json(SITE_DIR / "data" / "amr.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"amr.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    amr_ref = _load(data_dir / "amr.json", {}) or {}\n'
        '    for sec_key, sec_q in [("amr_mechanisms", "mechanisms"), ("amr_economics", "economics"), ("stewardship_dx", "stewardship"), ("nextgen_antiinfectives", "nextgen")]:\n'
        '        for item in (amr_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "amr",\n'
        '                "group": "AMR & Anti-Infectives",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/amr?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/amr?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"AMR antimicrobial resistance antibiotic ESKAPE MRSA CRE CARB-X QIDP LPAD stewardship AWaRe phage microbiome {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"amr", "#/ref/amr"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    amr_doc = _load_json(data_dir / "amr.json")\n'
        '    if isinstance(amr_doc, dict) and amr_doc.get("amr_mechanisms"):\n'
        '        am_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (amr_doc.get("amr_mechanisms") or []) + (amr_doc.get("amr_economics") or []))\n'
        '        pages.append(("amr", "#/ref/amr", "Antimicrobial Resistance (AMR), Stewardship & Anti-Infective Economics",\n'
        '                      "Primary-sourced guide to AMR mechanisms, ESKAPE pathogens, broken antibiotic economics, CARB-X/NHS subscription pull incentives, WHO AWaRe stewardship, and phage/LBP therapies.",\n'
        '                      f"<ul>{am_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/amr"' in txt:
        return False
    for anchor in ('    "/#/explore/history-laws",', '    "/#/explore/careers",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/amr",\n    "/#/explore/amr",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_amr_py": _write_if_changed(pipe_dir / "build_amr.py", BUILD_AMR_PY),
        "amr_js": _write_if_changed(js_dir / "amr.js", AMR_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/history-laws") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/history-laws", "History & safety laws"]] }];\nconst EXPLORE_NAV = [["#/explore/history-laws", "History & safety laws"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/history-laws",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_amr.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_amr.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"amr_mechanisms": 6, "amr_economics": 6, "stewardship_dx": 6, "nextgen_antiinfectives": 6}, out

        doc = json.loads((root / "site" / "data" / "amr.json").read_text(encoding="utf-8"))
        for k in ("amr_mechanisms", "amr_economics", "stewardship_dx", "nextgen_antiinfectives"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61X_AMR_STEWARDSHIP_ECONOMICS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1x AMR, Stewardship & Anti-Infective Economics patch.")
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
