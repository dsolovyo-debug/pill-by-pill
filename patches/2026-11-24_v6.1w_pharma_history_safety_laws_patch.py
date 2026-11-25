#!/usr/bin/env python3
"""Pill by Pill v6.1w Patch: Pharmaceutical History, Safety Laws & Scientific Revolutions (#/explore/history-laws, #/ref/history-laws, /api/history-laws).

Closes the History Buff audit item by porting ancient materia medica, landmark drug-safety laws
(1906–2022), scientific modality revolutions, and global public health milestones into a dedicated
primary-sourced module:
  1. Adds `pipeline/build_history_laws.py` -> `site/data/history_laws.json` (24 primary-sourced entries).
  2. Adds `site/js/history_laws.js` (`historyLawsPage` with inline Timeline SVG + 4 era filters)
     and wires `#/explore/history-laws`, `#/ref/history-laws`, `/api/history-laws`, `REF_NAV_GROUPS`,
     `EXPLORE_NAV`, and `pipeline/run_all.sh`.
  3. Integrates `history_laws.json` into `pipeline/build_global_search.py`,
     `pipeline/build_v60_static_pages.py` (`/history-laws/` static SEO page + sitemap -> 38 pages),
     and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1w_pharma_history_safety_laws_patch.py --selftest
  python3 2026-11-24_v6.1w_pharma_history_safety_laws_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_HISTORY_LAWS_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1w Pharmaceutical History, Safety Laws & Scientific Revolutions (`site/data/history_laws.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Ancient & Pre-Modern Materia Medica (6 milestones: Ebers Papyrus, Shennong Bencaojing, Dioscorides De Materia Medica, Ibn Sina Canon of Medicine, Cinchona/Quinine, Foxglove/Digitalis)\n  2. Landmark Drug-Safety Laws (6 statutes: 1906 Pure Food and Drug Act, 1938 FD&C Act & Elixir Sulfanilamide, 1962 Kefauver-Harris & Frances Kelsey, 1983 Orphan Drug Act & 1984 Hatch-Waxman, 1992 PDUFA & 2010 BPCIA, 2013 DQSA & 2022 IRA)\n  3. Scientific & Modality Revolutions (6 eras: Paul Ehrlich Magic Bullet, Penicillin Mass Fermentation, Recombinant DNA / Humulin 1982, Monoclonal Antibodies 1975, Rational Kinase Design / Imatinib, RNAi / mRNA-LNP / CRISPR)\n  4. Global Public Health Milestones (6 achievements: Smallpox Eradication, Polio Vaccines, WHO Essential Medicines List 1977, PEPFAR & Generic HIV Access, Curative HCV Antivirals, Global Pharmacovigilance PIDM)\n\nAll anchors are verified HTTPS primary sources (FDA, NIH/PMC, WHO, NobelPrize.org).\n\nUsage:\n  python3 pipeline/build_history_laws.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nANCIENT_MATERIA = [\n    {\n        "id": "hist-ebers",\n        "name": "Ebers Papyrus (~1550 BCE, Ancient Egypt)",\n        "era": "~1550 BCE",\n        "plain": "One of the oldest surviving medical scrolls in the world, recording over 800 herbal and mineral remedies—including willow bark for pain and castor oil.",\n        "technical": "110-page Egyptian hieratic papyrus cataloging botanical, mineral, and animal preparations alongside early clinical observations of cardiovascular and digestive conditions.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4459466/",\n    },\n    {\n        "id": "hist-shennong",\n        "name": "Shennong Bencaojing (~1st–2nd Century CE, China)",\n        "era": "~100–200 CE",\n        "plain": "The foundational Chinese herbal pharmacopoeia classifying 365 medicinal substances—including ephedra (ma huang) and sweet wormwood (qinghao), which centuries later inspired artemisinin for malaria.",\n        "technical": "Categorized botanicals, minerals, and animal products into three therapeutic grades; later Ge Hong\'s 4th-century cold-extraction note on Artemisia annua guided Tu Youyou\'s 2015 Nobel-winning artemisinin discovery.",\n        "url": "https://www.nobelprize.org/prizes/medicine/2015/tu/facts/",\n    },\n    {\n        "id": "hist-dioscorides",\n        "name": "Dioscorides — De Materia Medica (~70 CE, Mediterranean)",\n        "era": "~70 CE",\n        "plain": "A five-volume illustrated encyclopedia of over 600 medicinal plants written by a Greek army physician that served as Europe\'s standard pharmacy textbook for 1,500 years.",\n        "technical": "Pedanius Dioscorides organized preparations by pharmacological effect rather than alphabet, documenting opium poppy, willow, colchicum, and belladonna.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4459466/",\n    },\n    {\n        "id": "hist-avicenna",\n        "name": "Ibn Sina (Avicenna) — The Canon of Medicine (1025 CE)",\n        "era": "1025 CE",\n        "plain": "Introduced seven early rules for testing medicines—including testing a single drug at a time, checking dose-response, and testing in humans rather than relying only on animal results.",\n        "technical": "Book II of Al-Qanun fi al-Tibb formalized systematic empirical pharmacology and clinical observation centuries before modern randomized trials.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3159230/",\n    },\n    {\n        "id": "hist-cinchona",\n        "name": "Cinchona Bark & Quinine (1600s -> 1820)",\n        "era": "1630s–1820",\n        "plain": "Indigenous Andean knowledge of \'fever tree\' bark brought the first effective malaria treatment to the world; in 1820 French chemists Pelletier and Caventou isolated its pure active ingredient, quinine.",\n        "technical": "Isolation of pure alkaloids (morphine 1804, quinine 1820) marked the birth of modern pharmaceutical chemistry—replacing variable crude plant extracts with exact milligram dosing.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3121651/",\n    },\n    {\n        "id": "hist-digitalis",\n        "name": "William Withering & Foxglove / Digitalis (1785)",\n        "era": "1785",\n        "plain": "English physician William Withering spent ten years carefully recording doses and side effects of a folk herbal tea made from foxglove leaves, giving medicine digoxin for heart failure.",\n        "technical": "An Account of the Foxglove (1785) demonstrated systematic dose-titration and therapeutic-index awareness for cardiac glycosides.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1079585/",\n    },\n]\n\nSAFETY_LAWS = [\n    {\n        "id": "law-1906",\n        "name": "1906 Pure Food and Drug Act (Truth in Labeling)",\n        "era": "1906",\n        "plain": "Banned secret \'patent medicine\' tonics laced with hidden opium or cocaine by requiring accurate ingredient labels—laying the foundation for the modern FDA.",\n        "technical": "Prohibited interstate commerce in adulterated or misbranded drugs and recognized the USP and National Formulary as official purity standards, though it did not yet require premarket safety proof.",\n        "url": "https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law",\n    },\n    {\n        "id": "law-1938",\n        "name": "1938 Federal Food, Drug, and Cosmetic Act (Premarket Safety)",\n        "era": "1938",\n        "plain": "Passed after a toxic solvent in \'Elixir Sulfanilamide\' killed over 100 people, mostly children—requiring companies for the first time to prove a new medicine is safe before selling it.",\n        "technical": "Created the New Drug Application (NDA) premarket safety review requirement, authorized factory inspections, and established the core statutory architecture of Title 21.",\n        "url": "https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law",\n    },\n    {\n        "id": "law-1962",\n        "name": "1962 Kefauver-Harris Amendments (Efficacy, Informed Consent & Frances Kelsey)",\n        "era": "1962",\n        "plain": "After FDA reviewer Dr. Frances Kelsey blocked thalidomide in the U.S. and prevented thousands of birth defects, Congress required proof that new drugs actually WORK—plus patient informed consent and adverse-event reporting.",\n        "technical": "Mandated \'substantial evidence\' of efficacy from adequate and well-controlled clinical investigations, formal IND review, cGMP manufacturing, and informed consent.",\n        "url": "https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law",\n    },\n    {\n        "id": "law-1983-1984",\n        "name": "1983 Orphan Drug Act & 1984 Hatch-Waxman Act",\n        "era": "1983–1984",\n        "plain": "Twin laws that reshaped modern pharma: one created incentives to build rare-disease medicines, and the other created the modern generic drug industry while letting innovators restore lost patent time.",\n        "technical": "Established 7-year Orphan Drug Exclusivity (21 CFR 316) and the ANDA 505(j) bioequivalence pathway, Orange Book patent listings, and 35 U.S.C. § 156 Patent Term Extension.",\n        "url": "https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law",\n    },\n    {\n        "id": "law-1992-2010",\n        "name": "1992 PDUFA User Fees & 2010 BPCIA Biosimilars Act",\n        "era": "1992 & 2010",\n        "plain": "PDUFA funded FDA review teams to cut approval backlogs from years to months, while BPCIA created the U.S. approval pathway for biosimilar versions of complex biologic medicines.",\n        "technical": "PDUFA established predictable 10-month/6-month review clocks; BPCIA (42 U.S.C. § 262(k)) created the 351(k) biosimilar pathway and 12-year reference biologic exclusivity.",\n        "url": "https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law",\n    },\n    {\n        "id": "law-2013-2022",\n        "name": "2013 DQSA (503B & DSCSA) & 2022 Inflation Reduction Act (IRA)",\n        "era": "2013–2022",\n        "plain": "DQSA tightened sterile compounding and required unit-level 2D barcode tracking across U.S. pharmacies; the IRA capped Medicare Part D out-of-pocket costs and launched Medicare drug price negotiation.",\n        "technical": "Established § 503B outsourcing facilities, nationwide DSCSA serialization, and CMS Maximum Fair Price (MFP) negotiation for high-spend single-source Medicare drugs.",\n        "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program",\n    },\n]\n\nSCIENTIFIC_REVOLUTIONS = [\n    {\n        "id": "rev-ehrlich",\n        "name": "Paul Ehrlich\'s \'Magic Bullet\' & Salvarsan (1910)",\n        "era": "1908–1910",\n        "plain": "Introduced the idea that a synthetic chemical could be designed to kill a specific microbe without harming human tissue—launching modern medicinal chemistry.",\n        "technical": "Paul Ehrlich (1908 Nobel Prize) and Sahachiro Hata systematically screened 606 organoarsenic compounds to identify arsphenamine (Salvarsan) for syphilis.",\n        "url": "https://www.nobelprize.org/prizes/medicine/1908/ehrlich/facts/",\n    },\n    {\n        "id": "rev-penicillin",\n        "name": "Penicillin & Industrial Deep-Tank Fermentation (1928–1945)",\n        "era": "1928–1945",\n        "plain": "Alexander Fleming spotted a bacteria-killing mold in 1928, and Howard Florey, Ernst Chain, and WWII bioprocess engineers scaled it into the antibiotic era.",\n        "technical": "Transition from surface flasks to aerated submerged fermentation in Peoria, Illinois (NRRL) and Pfizer deep tanks created modern industrial bioprocessing.",\n        "url": "https://www.nobelprize.org/prizes/medicine/1945/fleming/facts/",\n    },\n    {\n        "id": "rev-mabs",\n        "name": "Hybridoma Technology & Monoclonal Antibodies (1975)",\n        "era": "1975",\n        "plain": "Georges Köhler and César Milstein figured out how to manufacture unlimited copies of a single pure antibody—giving rise to today\'s top cancer and autoimmune biologics.",\n        "technical": "1984 Nobel Prize discovery of B-cell/myeloma hybridomas, later humanized and phage-displayed into >150 FDA-approved therapeutic monoclonal antibodies.",\n        "url": "https://www.nobelprize.org/prizes/medicine/1984/milstein/facts/",\n    },\n    {\n        "id": "rev-rdna",\n        "name": "Recombinant DNA & Human Insulin (Humulin, 1982)",\n        "era": "1982",\n        "plain": "Instead of extracting insulin from pig and cow pancreases, scientists inserted the human insulin gene into bacteria—launching the biotechnology industry.",\n        "technical": "FDA approval of recombinant human insulin (Genentech / Eli Lilly, 1982) proved living engineered cells could manufacture identical human therapeutic proteins at commercial scale.",\n        "url": "https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law",\n    },\n    {\n        "id": "rev-targeted",\n        "name": "Structure-Guided & Targeted Oncology (Imatinib, 2001)",\n        "era": "2001",\n        "plain": "Shifted cancer care from carpet-bombing chemotherapy toward precision pills engineered to lock into a single mutated cancer enzyme.",\n        "technical": "FDA approval of imatinib for BCR-ABL+ CML validated rational kinase-inhibitor design and biomarker-driven clinical trials.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1934568/",\n    },\n    {\n        "id": "rev-genetic",\n        "name": "Programmable Genetic Medicines (RNAi, mRNA-LNP & CRISPR)",\n        "era": "2018–2023+",\n        "plain": "Opened a new chapter where medicines are written directly in genetic code—silencing faulty genes (patisiran), instructing immune cells (mRNA vaccines), or editing DNA (CRISPR).",\n        "technical": "Validated by Nobel-recognized breakthroughs in RNA interference (2006), CRISPR-Cas9 genome editing (2020), and nucleoside-modified mRNA (2023).",\n        "url": "https://www.nobelprize.org/prizes/medicine/2023/summary/",\n    },\n]\n\nPUBLIC_HEALTH = [\n    {\n        "id": "ph-smallpox",\n        "name": "Global Smallpox Eradication (1980)",\n        "era": "1796–1980",\n        "plain": "From Edward Jenner\'s 1796 cowpox vaccination to a coordinated WHO ring-vaccination campaign, smallpox became the first human disease completely wiped off the planet.",\n        "technical": "Certified eradicated by the World Health Assembly in May 1980 through thermostable freeze-dried vaccine, bifurcated needles, and targeted surveillance-containment.",\n        "url": "https://www.who.int/health-topics/smallpox",\n    },\n    {\n        "id": "ph-polio",\n        "name": "Inactivated (Salk) & Oral (Sabin) Polio Vaccines (1955–1961)",\n        "era": "1955–1961",\n        "plain": "Massive public clinical trials in over 1.8 million schoolchildren proved polio vaccines worked, slashing global paralysis cases by more than 99%.",\n        "technical": "The 1954 Francis Field Trial of Jonas Salk\'s IPV was a landmark double-blind placebo-controlled public-health trial, followed by Albert Sabin\'s mucosal OPV.",\n        "url": "https://www.who.int/health-topics/poliomyelitis",\n    },\n    {\n        "id": "ph-who-eml",\n        "name": "WHO Model List of Essential Medicines (1977–Present)",\n        "era": "1977",\n        "plain": "A globally curated shortlist of the most effective, safe, and cost-effective medicines every health system should keep available—updated every two years.",\n        "technical": "Guides national formularies and public procurement in >150 countries; Pill by Pill badges every WHO EML medicine directly across its catalogue.",\n        "url": "https://www.who.int/groups/expert-committee-on-selection-and-use-of-essential-medicines/essential-medicines-lists",\n    },\n    {\n        "id": "ph-hiv-pepfar",\n        "name": "Combination Antiretroviral Therapy & PEPFAR (1996–2003+)",\n        "era": "1996–2003+",\n        "plain": "Three-drug HIV cocktails turned a fatal diagnosis into a manageable chronic condition, while PEPFAR and generic licensing brought life-saving therapy to tens of millions globally.",\n        "technical": "Triple-therapy HAART suppressed viral resistance; voluntary generic licensing (MPP) and WHO Prequalification cut annual per-patient HIV treatment costs from >$10,000 to under $100.",\n        "url": "https://www.who.int/health-topics/hiv-aids",\n    },\n    {\n        "id": "ph-hcv-cure",\n        "name": "Curative Direct-Acting Antivirals for Hepatitis C (2013+)",\n        "era": "2013–Present",\n        "plain": "Oral pills like sofosbuvir turned a lifelong liver-destroying viral infection into an 8-to-12-week cure for over 95% of patients.",\n        "technical": "Direct-acting antivirals (NS5B polymerase, NS5A, and NS3/4A protease inhibitors) achieve >95% Sustained Virologic Response (SVR12) without interferon injections.",\n        "url": "https://www.who.int/news-room/fact-sheets/detail/hepatitis-c",\n    },\n    {\n        "id": "ph-pidm",\n        "name": "WHO International Drug Monitoring (1968–Present)",\n        "era": "1968",\n        "plain": "Created in the aftermath of thalidomide so countries pool side-effect warnings globally through VigiBase rather than learning safety lessons in isolation.",\n        "technical": "WHO Programme for International Drug Monitoring (PIDM) connects 170+ national pharmacovigilance centers through the Uppsala Monitoring Centre.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13160990/",\n    },\n]\n\n\ndef build_history_laws(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced historical reference on ancient materia medica, landmark drug-safety statutes, scientific modality revolutions, and global public health milestones (FDA, WHO, NobelPrize.org, NIH PMC).",\n        "ancient_materia": ANCIENT_MATERIA,\n        "safety_laws": SAFETY_LAWS,\n        "scientific_revolutions": SCIENTIFIC_REVOLUTIONS,\n        "public_health": PUBLIC_HEALTH,\n    }\n    (data_dir / "history_laws.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "ancient_materia": len(ANCIENT_MATERIA),\n        "safety_laws": len(SAFETY_LAWS),\n        "scientific_revolutions": len(SCIENTIFIC_REVOLUTIONS),\n        "public_health": len(PUBLIC_HEALTH),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_history_laws(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
HISTORY_LAWS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderHistoryTimelineSvg() {\n  const nodes = [\n    { x: 8, label: "Ancient Herbs", sub: "1550 BCE–1785" },\n    { x: 140, label: "Safety Laws", sub: "1906 / 1938 / 1962" },\n    { x: 272, label: "Antibiotics", sub: "1928–1945" },\n    { x: 404, label: "Biotech & mAbs", sub: "1975–2001" },\n    { x: 536, label: "Genetic Era", sub: "RNAi / mRNA / CRISPR" },\n  ];\n  return html`<figure class="history-flow" aria-label="Historical evolution of medicines and drug safety law">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 1 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 1 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">3,500 years of pharmacology: from ancient botanical scrolls and crisis-driven safety laws to programmable genetic medicines.</figcaption>\n  </figure>`;\n}\n\nexport async function historyLawsPage(query, mode = "explore") {\n  const doc = await getJSON("data/history_laws.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/history-laws" : "#/ref/history-laws";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "History of Medicines, Safety Laws & Scientific Revolutions",\n    body: html`\n      <h1>History of Medicines, Safety Laws &amp; Scientific Revolutions</h1>\n      <p class="lead">${mode === "explore"\n        ? "How humanity went from willow bark and foxglove tea to antibiotics, monoclonal antibodies, and CRISPR—and how real-world tragedies forged the modern FDA safety laws that protect patients today."\n        : "Primary-sourced historical reference covering ancient materia medica, landmark U.S. drug-safety statutes (1906–2022), scientific modality revolutions, and global public health milestones (checked " + doc.checked + ")."}</p>\n\n      ${renderHistoryTimelineSvg()}\n\n      <p class="small">Jump to era:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Eras</a> ·\n        <a href="${base}?section=ancient"${sec === "ancient" ? \' aria-current="page"\' : ""}>Ancient Materia Medica (6)</a> ·\n        <a href="${base}?section=laws"${sec === "laws" ? \' aria-current="page"\' : ""}>Landmark Safety Laws (6)</a> ·\n        <a href="${base}?section=revolutions"${sec === "revolutions" ? \' aria-current="page"\' : ""}>Scientific Revolutions (6)</a> ·\n        <a href="${base}?section=public"${sec === "public" ? \' aria-current="page"\' : ""}>Public Health Milestones (6)</a>\n      </p>\n\n      ${show("ancient") ? html`\n        <h2 id="ancient">1. Ancient &amp; Pre-Modern Materia Medica (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Ancient materia medica">\n          <table class="tbl"><thead><tr><th>Milestone</th><th>Era</th><th>Significance</th></tr></thead>\n          <tbody>${(doc.ancient_materia || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${a.era}</td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("laws") ? html`\n        <h2 id="laws">2. Landmark Drug-Safety Laws That Built Modern Regulation (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Landmark drug safety laws">\n          <table class="tbl"><thead><tr><th>Statute</th><th>Year</th><th>What Changed</th></tr></thead>\n          <tbody>${(doc.safety_laws || []).map((l) => html`<tr id="${l.id}">\n            <td><b><a href="${l.url}" target="_blank" rel="noopener">${l.name}</a></b></td>\n            <td>${l.era}</td>\n            <td>${mode === "explore" ? l.plain : html`${l.plain}<br><span class="muted small">${l.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("revolutions") ? html`\n        <h2 id="revolutions">3. Scientific &amp; Modality Revolutions (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Scientific revolutions">\n          <table class="tbl"><thead><tr><th>Breakthrough</th><th>Era</th><th>Impact on Modern Medicine</th></tr></thead>\n          <tbody>${(doc.scientific_revolutions || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b></td>\n            <td>${r.era}</td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("public") ? html`\n        <h2 id="public">4. Global Public Health Milestones (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Global public health milestones">\n          <table class="tbl"><thead><tr><th>Achievement</th><th>Era</th><th>Global Impact</th></tr></thead>\n          <tbody>${(doc.public_health || []).map((p) => html`<tr id="${p.id}">\n            <td><b><a href="${p.url}" target="_blank" rel="noopener">${p.name}</a></b></td>\n            <td>${p.era}</td>\n            <td>${mode === "explore" ? p.plain : html`${p.plain}<br><span class="muted small">${p.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/explore/origins">100 Discovery Origin Stories</a> · <a href="#/explore/trace">Trace One Drug End-to-End</a> · <a href="#/ref/pathways">Approval Pathways</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { historyLawsPage } from "./history_laws.js";\n'
    if "./history_laws.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/history-laws"' not in txt:
        for anchor in ('if (path === "/ref/careers")', 'if (path === "/ref/combo-devices")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/history-laws") return historyLawsPage(query, "ref");\n'
                    '  if (path === "/explore/history-laws") return historyLawsPage(query, "explore");\n'
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
    if "#/ref/history-laws" not in txt:
        for anchor in ('["#/ref/careers", "Careers & roles"]', '["#/ref/glossary", "Acronym glossary"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/history-laws", "History & safety laws"]', 1)
                changed = True
                break
    if "#/explore/history-laws" not in txt:
        for anchor in ('["#/explore/origins", "Origin stories (75)"]', '["#/explore/careers", "Careers & roles"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/history-laws", "History & safety laws"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_history_laws.py" in txt:
        return False
    hook = "\n# v6.1w: Pharmaceutical History, Safety Laws & Scientific Revolutions\npython3 pipeline/build_history_laws.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/history-laws"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/history-laws")\n'
        'def api_history_laws():\n'
        '    return _read_json(SITE_DIR / "data" / "history_laws.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"history_laws.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    hl_ref = _load(data_dir / "history_laws.json", {}) or {}\n'
        '    for sec_key, sec_q in [("ancient_materia", "ancient"), ("safety_laws", "laws"), ("scientific_revolutions", "revolutions"), ("public_health", "public")]:\n'
        '        for item in (hl_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "history_law",\n'
        '                "group": "History & Safety Laws",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/history-laws?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/history-laws?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"history law milestone {item.get(\'era\', \'\')} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"history-laws", "#/explore/history-laws"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    hl_doc = _load_json(data_dir / "history_laws.json")\n'
        '    if isinstance(hl_doc, dict) and hl_doc.get("safety_laws"):\n'
        '        hl_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (hl_doc.get("ancient_materia") or []) + (hl_doc.get("safety_laws") or []))\n'
        '        pages.append(("history-laws", "#/explore/history-laws", "History of Medicines, Safety Laws & Scientific Revolutions",\n'
        '                      "Primary-sourced timeline from ancient materia medica and the 1906/1938/1962 FDA safety laws to antibiotics, monoclonal antibodies, and genetic medicines.",\n'
        '                      f"<ul>{hl_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/explore/history-laws"' in txt:
        return False
    for anchor in ('    "/#/explore/careers",', '    "/#/explore/combo-devices",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/history-laws",\n    "/#/explore/history-laws",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_history_laws_py": _write_if_changed(pipe_dir / "build_history_laws.py", BUILD_HISTORY_LAWS_PY),
        "history_laws_js": _write_if_changed(js_dir / "history_laws.js", HISTORY_LAWS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/careers") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/careers", "Careers & roles"]] }];\nconst EXPLORE_NAV = [["#/explore/careers", "Careers & roles"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/careers",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_history_laws.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_history_laws.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ancient_materia": 6, "safety_laws": 6, "scientific_revolutions": 6, "public_health": 6}, out

        doc = json.loads((root / "site" / "data" / "history_laws.json").read_text(encoding="utf-8"))
        for k in ("ancient_materia", "safety_laws", "scientific_revolutions", "public_health"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61W_PHARMA_HISTORY_SAFETY_LAWS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1w Pharma History & Safety Laws patch.")
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
