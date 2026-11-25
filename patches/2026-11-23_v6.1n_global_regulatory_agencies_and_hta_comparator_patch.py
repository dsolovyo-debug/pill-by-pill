#!/usr/bin/env python3
"""Pill by Pill v6.1n Patch: Global Regulatory Agencies & HTA Reimbursement Comparator (#/ref/global-reg, #/explore/global-reg, /api/global-reg).

1. Adds `pipeline/build_global_reg_hta.py` -> `site/data/global_reg_hta.json` (6 global regulatory
   agencies, 6 international reliance/work-sharing frameworks, 6 global HTA/payer bodies, and
   6 global pricing/market-access mechanisms — 24 primary-sourced entries).
2. Adds `site/js/global_reg_hta.js` (`globalRegHtaPage` with inline Two-Gate Global Access SVG +
   4 section filters) and wires `#/ref/global-reg`, `#/explore/global-reg`, `/api/global-reg`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `global_reg_hta.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/global-reg/` static SEO page + sitemap entry -> 30
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1n_global_regulatory_agencies_and_hta_comparator_patch.py --selftest
  python3 2026-11-23_v6.1n_global_regulatory_agencies_and_hta_comparator_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_GLOBAL_REG_HTA_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1n Global Regulatory Agencies & HTA Reimbursement Comparator (`site/data/global_reg_hta.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Major Global Regulatory Agencies (6 agencies: US FDA, EU EMA, Japan PMDA/MHLW, Health Canada, UK MHRA, Australia TGA / Swissmedic)\n  2. International Reliance & Collaborative Frameworks (6 programs: FDA Project Orbis, Access Consortium, WHO Prequalification & WLA, ICH Harmonisation, EU HTAR Joint Clinical Assessment, cGMP Mutual Recognition Agreements)\n  3. Global Health Technology Assessment (HTA) & Payer Bodies (6 bodies: UK NICE, Germany G-BA/IQWiG AMNOG, France HAS SMR/ASMR, Canada CDA-AMC & pCPA, Australia PBAC, US ICER & CMS IRA)\n  4. Global Pricing & Market Access Mechanisms (6 mechanisms: International Reference Pricing, Managed Entry Agreements, Cost-Effectiveness QALY/ICER, EU Parallel Trade, Tenders & GPOs, Global Launch Sequencing)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, EMA, PMDA, Health Canada, MHRA, TGA, WHO, NICE, CMS, CBO).\n\nUsage:\n  python3 pipeline/build_global_reg_hta.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nREGULATORY_AGENCIES = [\n    {\n        "id": "reg-fda",\n        "name": "US FDA (CDER & CBER)",\n        "region": "United States",\n        "plain": "Reviews drugs (CDER) and biologics/vaccines/cell & gene therapies (CBER) for safety, efficacy, and manufacturing quality—without setting drug prices.",\n        "technical": "Statutory authority under FD&C Act and PHS Act; funded via PDUFA/GDUFA/BsUFA user fees (10-mo standard / 6-mo priority clock). Approves ~50+ novel drugs/year and conducts global OII cGMP inspections.",\n        "url": "https://www.fda.gov/patients/drug-development-process/step-4-fda-drug-review",\n    },\n    {\n        "id": "reg-ema",\n        "name": "EU EMA & European Commission (Centralised Procedure)",\n        "region": "European Union / EEA (30 countries)",\n        "plain": "Evaluates new medicines scientifically across all EU member states through a single Centralised Procedure, after which each country decides its own reimbursement and price.",\n        "technical": "CHMP issues scientific opinion within 210 active review days (150 days Accelerated Assessment), followed by legally binding European Commission Marketing Authorisation across all EEA states; national/MRP/DCP routes cover generics and older products.",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation",\n    },\n    {\n        "id": "reg-pmda",\n        "name": "Japan PMDA & MHLW",\n        "region": "Japan",\n        "plain": "PMDA conducts scientific reviews and safety checks while MHLW grants official approval and sets national insurance reimbursement prices—often requiring Japanese patient PK/bridging data.",\n        "technical": "Standard review target 12 months (9 months Priority; 6 months Sakigake pioneer designation). Emphasizes ICH E5/E17 ethnic-factor bridging, Early Post-marketing Phase Vigilance (EPPV), and NHI Drug Price Standard listing.",\n        "url": "https://www.pmda.go.jp/english/review-services/reviews/0001.html",\n    },\n    {\n        "id": "reg-hc",\n        "name": "Health Canada (HPFB)",\n        "region": "Canada",\n        "plain": "Approves medicines for sale in Canada via a Notice of Compliance (NOC), after which federal and provincial agencies review prices and decide public formulary coverage.",\n        "technical": "New Drug Submission (NDS) target 300 days (180 days Priority Review; NOC with Conditions — NOC/c — for serious unmet needs). Active participant in FDA Project Orbis and the Access Consortium.",\n        "url": "https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products.html",\n    },\n    {\n        "id": "reg-mhra",\n        "name": "UK MHRA (National & International Recognition Procedure)",\n        "region": "United Kingdom",\n        "plain": "Following Brexit, the UK\'s MHRA runs its own independent reviews alongside a fast-track International Recognition Procedure that leverages trusted FDA, EMA, PMDA, and Health Canada assessments.",\n        "technical": "Operates 150-day national assessments, Innovative Licensing and Access Pathway (ILAP) with NICE/SMC, and the International Recognition Procedure (IRP, 60-day or 110-day routes) relying on 7 Reference Regulators.",\n        "url": "https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency",\n    },\n    {\n        "id": "reg-tga-swiss",\n        "name": "Australia TGA & Swissmedic",\n        "region": "Australia & Switzerland",\n        "plain": "Stringent national regulators that maintain independent high standards while co-reviewing new medicines together with Canada, Singapore, and the UK through the Access Consortium.",\n        "technical": "TGA (255 working days standard; Provisional Approval pathway) and Swissmedic (330 days standard; temporary authorization) co-lead work-sharing reviews under the Access Consortium to accelerate multi-market access.",\n        "url": "https://www.tga.gov.au/products/medicines",\n    },\n]\n\nRELIANCE_FRAMEWORKS = [\n    {\n        "id": "rel-orbis",\n        "name": "FDA Project Orbis (Concurrent Global Oncology Review)",\n        "plain": "Allows the FDA and partner regulators in Canada, Australia, the UK, Switzerland, Singapore, Brazil, and Israel to review major cancer drugs at the same time instead of waiting years in line.",\n        "technical": "Coordinated by FDA Oncology Center of Excellence (OCE) since 2019; partners share review discussions and queries while each country retains independent sovereign approval and labeling authority.",\n        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/project-orbis",\n    },\n    {\n        "id": "rel-access",\n        "name": "Access Consortium (AU, CA, SG, CH, UK)",\n        "plain": "Five mid-sized regulatory agencies split the scientific workload—each reviewing different modules of a drug dossier—so patients get new medicines faster without duplicating work.",\n        "technical": "Work-sharing initiative among TGA (Australia), Health Canada, HSA (Singapore), Swissmedic, and MHRA (UK) covering New Active Substances (NAS), biosimilars, and generic work-sharing.",\n        "url": "https://www.tga.gov.au/international-activities/access-consortium",\n    },\n    {\n        "id": "rel-who-wla",\n        "name": "WHO Prequalification (PQ) & WHO-Listed Authorities (WLA)",\n        "plain": "The World Health Organization vets essential vaccines and medicines for HIV, TB, and malaria so UN agencies and lower-income countries can buy safe, quality-assured products with confidence.",\n        "technical": "WHO Prequalification evaluates dossiers and cGMP sites for global procurement (UNICEF, Global Fund, Gavi); the WHO-Listed Authorities (WLA) framework replaces legacy Stringent Regulatory Authority (SRA) designations for global regulatory reliance.",\n        "url": "https://www.who.int/teams/regulation-prequalification/regulation-and-safety/regulatory-convergence-networks/who-listed-authorities",\n    },\n    {\n        "id": "rel-ich",\n        "name": "ICH Global Harmonisation (Q, S, E & M Guidelines)",\n        "plain": "Sets one shared scientific playbook across the US, Europe, Japan, and dozens of partner nations so a single set of lab, animal, and human studies works worldwide.",\n        "technical": "International Council for Harmonisation (ICH) unifies Quality (Q1–Q14), Safety (S1–S12), Efficacy (E1–E20), and Multidisciplinary (M1–M14, including MedDRA and eCTD M4) technical standards.",\n        "url": "https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/international-council-harmonisation-ich",\n    },\n    {\n        "id": "rel-eu-jca",\n        "name": "EU HTA Regulation (HTAR) & Joint Clinical Assessment (JCA)",\n        "plain": "Starting in 2025 with cancer drugs and gene therapies, EU countries now pool their clinical-benefit review into one shared European report instead of making companies prove clinical value 27 separate times.",\n        "technical": "Regulation (EU) 2021/2282 phased in Joint Clinical Assessments (oncology & ATMPs Jan 2025 -> orphan drugs 2028 -> all centrally authorized medicines 2030); pricing and reimbursement decisions remain strictly national.",\n        "url": "https://health.ec.europa.eu/health-technology-assessment/regulation-health-technology-assessment_en",\n    },\n    {\n        "id": "rel-mra",\n        "name": "cGMP Mutual Recognition Agreements (US–EU / US–UK / US–CH)",\n        "plain": "Lets the FDA and European/UK/Swiss inspectors trust each other\'s factory inspection reports instead of flying teams across the ocean to inspect the exact same plant twice.",\n        "technical": "Mutual Recognition Agreements (MRAs) allow FDA and EU/UK/Swiss inspectorates to rely on partner cGMP inspection outcomes for human drug facilities, freeing FDA OII resources for higher-risk global sites.",\n        "url": "https://www.fda.gov/international-programs/international-arrangements/mutual-recognition-agreement-mra",\n    },\n]\n\nHTA_BODIES = [\n    {\n        "id": "hta-nice",\n        "name": "UK NICE (National Institute for Health and Care Excellence)",\n        "region": "England & Wales (NHS)",\n        "plain": "Evaluates whether a new medicine delivers enough extra healthy life-years (QALYs) for its price to justify NHS funding—typically expecting under £20,000–£30,000 per QALY.",\n        "technical": "Cost-utility HTA framework using Incremental Cost-Effectiveness Ratios (ICERs per QALY) with a £20k–£30k standard threshold, severity modifiers (1.2× / 1.7×), Highly Specialised Technologies (HST) route, and confidential Patient Access Scheme (PAS) discounts.",\n        "url": "https://www.nice.org.uk/about/what-we-do/our-programmes/nice-guidance/nice-technology-appraisal-guidance",\n    },\n    {\n        "id": "hta-gba",\n        "name": "Germany G-BA & IQWiG (AMNOG Process)",\n        "region": "Germany",\n        "plain": "New drugs launch immediately at the manufacturer\'s price for the first 6 months while IQWiG and G-BA grade how much \'added benefit\' the drug beats existing care—setting the stage for national price talks.",\n        "technical": "Under AMNOG, IQWiG performs an early benefit assessment and G-BA assigns a 6-tier Zusatznutzen rating (Major, Considerable, Minor, Non-quantifiable, None, Less), guiding GKV-SV reimbursement price negotiation.",\n        "url": "https://www.iqwig.de/en/about-us/responsibilities-and-objectives-of-iqwig/",\n    },\n    {\n        "id": "hta-has",\n        "name": "France HAS (SMR & ASMR Ratings)",\n        "region": "France",\n        "plain": "Scores every new medicine on two scales: whether it is useful enough to be covered at all (SMR) and how much better it is than existing drugs from I (major breakthrough) to V (no improvement) (ASMR).",\n        "technical": "Haute Autorité de Santé (Transparency Committee) assigns SMR (reimbursement rate: 65%/30%/15%) and ASMR I–V; ASMR I–III enables European reference pricing and faster access via CEPS negotiation, while ASMR V requires a price below comparators.",\n        "url": "https://www.has-sante.fr/jcms/c_2035649/en/health-technology-assessment-at-has",\n    },\n    {\n        "id": "hta-canada",\n        "name": "Canada CDA-AMC (formerly CADTH), INESSS & pCPA",\n        "region": "Canada",\n        "plain": "Reviews clinical value and cost-effectiveness for Canada\'s public drug plans, after which provinces band together (pCPA) to negotiate confidential discounts.",\n        "technical": "Canada\'s Drug Agency (CDA-AMC) and Quebec\'s INESSS issue reimbursement recommendations; the pan-Canadian Pharmaceutical Alliance (pCPA) negotiates Letter of Intent (LOI) net pricing across federal/provincial plans, alongside PMPRB patented price oversight.",\n        "url": "https://www.cda-amc.ca/",\n    },\n    {\n        "id": "hta-pbac",\n        "name": "Australia PBAC (Pharmaceutical Benefits Scheme)",\n        "region": "Australia",\n        "plain": "Independent expert committee that must recommend a medicine as both clinically effective and cost-effective before the Australian government can subsidize it on the PBS.",\n        "technical": "Pharmaceutical Benefits Advisory Committee (PBAC) evaluates comparative clinical efficacy and cost-effectiveness (CUA/CMA) for listing on the Pharmaceutical Benefits Scheme (PBS), often using risk-sharing Deeds of Agreement.",\n        "url": "https://www.pbs.gov.au/info/industry/listing/elements/pbac-guidelines",\n    },\n    {\n        "id": "hta-us-icer-cms",\n        "name": "US Fragmented Payers, Independent ICER & CMS IRA Negotiation",\n        "region": "United States",\n        "plain": "Unlike Europe or Canada, the U.S. has no single national HTA gatekeeper—private insurers and PBMs negotiate rebates separately, while ICER publishes independent value reports and Medicare now negotiates prices on select older top-spend drugs.",\n        "technical": "Private PBMs/health plans drive formulary access via rebates; the Institute for Clinical and Economic Review (ICER) publishes non-binding QALY/evLYG benchmarks; the Inflation Reduction Act (IRA) authorizes CMS to negotiate Maximum Fair Prices (MFPs) for high-spend single-source Medicare drugs (7+ yrs small molecule / 11+ yrs biologic post-approval).",\n        "url": "https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program",\n    },\n]\n\nACCESS_MECHANISMS = [\n    {\n        "id": "acc-irp",\n        "name": "International / External Reference Pricing (IRP / ERP)",\n        "plain": "Many countries cap what they will pay for a drug by checking a \'basket\' of published list prices in neighboring countries—which is why drugmakers prefer confidential rebates over lower list prices.",\n        "technical": "National payers benchmark maximum ex-factory prices against mean, median, or lowest prices in reference country baskets (e.g., EU cross-referencing), creating strong commercial incentives to keep list prices aligned and discount via confidential MEAs.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "acc-mea",\n        "name": "Managed Entry Agreements (MEAs: Financial vs. Outcomes-Based)",\n        "plain": "Creative payer contracts that lower financial risk—ranging from simple confidential volume discounts to \'pay-for-performance\' deals where the drugmaker refunds money if a gene therapy stops working.",\n        "technical": "Includes financial MEAs (confidential simple discounts, price-volume caps, budget caps) and performance-based / outcomes-based agreements (coverage with evidence development — CED, annuity milestone payments for curative CGTs).",\n        "url": "https://www.nice.org.uk/about/what-we-do/our-programmes/nice-guidance/nice-technology-appraisal-guidance",\n    },\n    {\n        "id": "acc-qaly-icer",\n        "name": "Cost-Effectiveness Modeling (QALY, evLYG & ICER)",\n        "plain": "Compares the extra cost of a new medicine against the extra healthy time it buys, helping public health systems decide where limited healthcare budgets do the most good.",\n        "technical": "Incremental Cost-Effectiveness Ratio = (Cost_new - Cost_std) / (QALY_new - QALY_std). Complemented by Equal Value of Life Years Gained (evLYG) to avoid penalizing life-extending therapies in disabled or elderly populations.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "acc-parallel-trade",\n        "name": "EU Parallel Trade & Price Convergence",\n        "plain": "Inside Europe\'s single market, licensed distributors can legally buy a medicine in a lower-priced EU country, relabel it, and resell it in a higher-priced EU country.",\n        "technical": "Protected under EU Treaty free-movement-of-goods principles; creates supply-allocation tensions and drives manufacturers toward uniform EU launch list prices paired with national confidential rebates.",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation",\n    },\n    {\n        "id": "acc-tenders",\n        "name": "National Tenders, Hospital GPOs & Biosimilar Bidding",\n        "plain": "When multiple generic or biosimilar versions compete, hospitals and national health systems run winner-take-all or multi-winner bidding auctions that slash prices dramatically.",\n        "technical": "Nordic/European national hospital tenders (e.g., Norway LIS, UK NHS framework tenders) and U.S. Group Purchasing Organizations (GPOs) drive rapid competitive price compression once multi-source competition opens.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "acc-launch-seq",\n        "name": "Global Launch Sequencing & Access Gaps",\n        "plain": "Because pricing rules and review timelines differ widely, companies typically launch new drugs first in the US, Germany, and Japan—while lower-income or strict-price countries may wait years.",\n        "technical": "Sequential launch strategy optimizes net present value while managing IRP spillover risks; mitigated in LMICs through tiered pricing, Medicines Patent Pool voluntary licenses, and WHO PQ procurement.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n]\n\n\ndef build_global_reg_hta(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced educational reference comparing global drug regulatory agencies, international reliance pathways, HTA reimbursement bodies, and global market access mechanisms (FDA, EMA, PMDA, Health Canada, MHRA, TGA, WHO, NICE, IQWiG, HAS, CMS, CBO). Educational reference only.",\n        "regulatory_agencies": REGULATORY_AGENCIES,\n        "reliance_frameworks": RELIANCE_FRAMEWORKS,\n        "hta_bodies": HTA_BODIES,\n        "access_mechanisms": ACCESS_MECHANISMS,\n    }\n    (data_dir / "global_reg_hta.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "regulatory_agencies": len(REGULATORY_AGENCIES),\n        "reliance_frameworks": len(RELIANCE_FRAMEWORKS),\n        "hta_bodies": len(HTA_BODIES),\n        "access_mechanisms": len(ACCESS_MECHANISMS),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_global_reg_hta(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
GLOBAL_REG_HTA_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderGlobalAccessSvg() {\n  const nodes = [\n    { x: 8, label: "1. Global Filing", sub: "FDA / EMA / PMDA / HC" },\n    { x: 140, label: "2. Reliance", sub: "Orbis / Access / ICH" },\n    { x: 272, label: "3. Approval", sub: "Safety & Efficacy" },\n    { x: 404, label: "4. HTA Value", sub: "NICE / G-BA / HAS" },\n    { x: 536, label: "5. Patient Access", sub: "Net Price / Formulary" },\n  ];\n  return html`<figure class="global-reg-flow" aria-label="Global regulatory approval to HTA reimbursement flow">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 3 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 3 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Two-gate global access reality: Gate 1 is regulatory approval (safety/efficacy); Gate 2 is HTA value &amp; payer reimbursement.</figcaption>\n  </figure>`;\n}\n\nexport async function globalRegHtaPage(query, mode = "ref") {\n  const doc = await getJSON("data/global_reg_hta.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/global-reg" : "#/ref/global-reg";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Global Regulatory Agencies & HTA Reimbursement Comparator",\n    body: html`\n      <h1>Global Regulatory Agencies &amp; HTA Reimbursement Comparator</h1>\n      <p class="lead">${mode === "explore"\n        ? "Why a medicine approved in the United States still needs separate approvals in Europe, Japan, Canada, and the UK—and how national health systems decide what a medicine is worth paying for."\n        : "Primary-sourced comparator covering 6 stringent regulatory agencies, 6 international reliance & work-sharing frameworks, 6 major HTA/payer bodies, and 6 global pricing/access mechanisms (checked " + doc.checked + ")."}</p>\n\n      ${renderGlobalAccessSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=agencies"${sec === "agencies" ? \' aria-current="page"\' : ""}>Regulatory Agencies (6)</a> ·\n        <a href="${base}?section=reliance"${sec === "reliance" ? \' aria-current="page"\' : ""}>Global Reliance (6)</a> ·\n        <a href="${base}?section=hta"${sec === "hta" ? \' aria-current="page"\' : ""}>HTA &amp; Payers (6)</a> ·\n        <a href="${base}?section=access"${sec === "access" ? \' aria-current="page"\' : ""}>Pricing &amp; Access (6)</a>\n      </p>\n\n      ${show("agencies") ? html`\n        <h2 id="agencies">1. Major Global Regulatory Agencies (Gate 1: Safety &amp; Efficacy)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Major global regulatory agencies">\n          <table class="tbl"><thead><tr><th>Agency</th><th>Jurisdiction</th><th>${mode === "explore" ? "How It Works" : "Review Clocks & Statutory Framework"}</th></tr></thead>\n          <tbody>${(doc.regulatory_agencies || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${a.region}</td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("reliance") ? html`\n        <h2 id="reliance">2. International Reliance &amp; Collaborative Review Frameworks (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="International regulatory reliance frameworks">\n          <table class="tbl"><thead><tr><th>Initiative</th><th>${mode === "explore" ? "What It Accomplishes" : "Scope & Operational Mechanism"}</th></tr></thead>\n          <tbody>${(doc.reliance_frameworks || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b></td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("hta") ? html`\n        <h2 id="hta">3. Global Health Technology Assessment (HTA) &amp; Payers (Gate 2: Value)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Global HTA reimbursement bodies">\n          <table class="tbl"><thead><tr><th>HTA Body / Payer</th><th>Market</th><th>${mode === "explore" ? "How Coverage Is Decided" : "Value Assessment & Pricing Framework"}</th></tr></thead>\n          <tbody>${(doc.hta_bodies || []).map((h) => html`<tr id="${h.id}">\n            <td><b><a href="${h.url}" target="_blank" rel="noopener">${h.name}</a></b></td>\n            <td>${h.region}</td>\n            <td>${mode === "explore" ? h.plain : html`${h.plain}<br><span class="muted small">${h.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("access") ? html`\n        <h2 id="access">4. Global Pricing, Contracting &amp; Market Access Mechanisms (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Global pricing and market access mechanisms">\n          <table class="tbl"><thead><tr><th>Mechanism</th><th>${mode === "explore" ? "How It Affects Prices & Access" : "Economic & Commercial Dynamics"}</th></tr></thead>\n          <tbody>${(doc.access_mechanisms || []).map((m) => html`<tr id="${m.id}">\n            <td><b><a href="${m.url}" target="_blank" rel="noopener">${m.name}</a></b></td>\n            <td>${mode === "explore" ? m.plain : html`${m.plain}<br><span class="muted small">${m.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/pathways">Approval Pathways &amp; Exclusivities</a> · <a href="#/ref/economics">Drug Economics &amp; GTN</a> · <a href="#/ref/ip">Patents &amp; IP</a> · <a href="#/ref/departments/regulatory">Stage 5: Regulatory Affairs</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { globalRegHtaPage } from "./global_reg_hta.js";\n'
    if "./global_reg_hta.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/global-reg"' not in txt:
        for anchor in ('if (path === "/ref/sterile")', 'if (path === "/ref/ip")', 'if (path === "/ref/safety")', 'if (path === "/ref/pathways")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/global-reg") return globalRegHtaPage(query, "ref");\n'
                    '  if (path === "/explore/global-reg") return globalRegHtaPage(query, "explore");\n'
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
    if "#/ref/global-reg" not in txt:
        for anchor in ('["#/ref/sterile", "Sterile & bioprocessing"]', '["#/ref/ip", "Patents & IP"]', '["#/ref/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/global-reg", "Global agencies & HTA"]', 1)
                changed = True
                break
    if "#/explore/global-reg" not in txt:
        for anchor in ('["#/explore/sterile", "Sterile & bioprocessing"]', '["#/explore/ip", "Patents & IP"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/global-reg", "Global agencies & HTA"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_global_reg_hta.py" in txt:
        return False
    hook = "\n# v6.1n: Global Regulatory Agencies & HTA Reimbursement Comparator\npython3 pipeline/build_global_reg_hta.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/global-reg"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/global-reg")\n'
        'def api_global_reg_hta():\n'
        '    return _read_json(SITE_DIR / "data" / "global_reg_hta.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"global_reg_hta.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    gr_ref = _load(data_dir / "global_reg_hta.json", {}) or {}\n'
        '    for sec_key, sec_q in [("regulatory_agencies", "agencies"), ("reliance_frameworks", "reliance"), ("hta_bodies", "hta"), ("access_mechanisms", "access")]:\n'
        '        for item in (gr_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "global_reg_hta",\n'
        '                "group": "Global Regulatory & HTA",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/global-reg?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/global-reg?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"global regulatory agency HTA reimbursement NICE AMNOG HAS PBAC Project Orbis {sec_key} {item.get(\'name\', \'\')} {item.get(\'region\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"global-reg", "#/ref/global-reg"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    gr_doc = _load_json(data_dir / "global_reg_hta.json")\n'
        '    if isinstance(gr_doc, dict) and gr_doc.get("regulatory_agencies"):\n'
        '        gr_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (gr_doc.get("regulatory_agencies") or []) + (gr_doc.get("hta_bodies") or []))\n'
        '        pages.append(("global-reg", "#/ref/global-reg", "Global Regulatory Agencies & HTA Reimbursement Comparator",\n'
        '                      "Primary-sourced comparison of FDA, EMA, PMDA, Health Canada, MHRA, TGA/Swissmedic, Project Orbis, EU HTAR JCA, and global HTA bodies (NICE, G-BA/AMNOG, HAS, CDA-AMC, PBAC, ICER/CMS).",\n'
        '                      f"<ul>{gr_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/global-reg"' in txt:
        return False
    for anchor in ('    "/#/explore/sterile",', '    "/#/explore/ip",', '    "/#/explore/safety",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/global-reg",\n    "/#/explore/global-reg",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_global_reg_hta_py": _write_if_changed(pipe_dir / "build_global_reg_hta.py", BUILD_GLOBAL_REG_HTA_PY),
        "global_reg_hta_js": _write_if_changed(js_dir / "global_reg_hta.js", GLOBAL_REG_HTA_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/sterile") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/sterile", "Sterile & bioprocessing"]] }];\nconst EXPLORE_NAV = [["#/explore/sterile", "Sterile & bioprocessing"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/sterile",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_global_reg_hta.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_global_reg_hta.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"regulatory_agencies": 6, "reliance_frameworks": 6, "hta_bodies": 6, "access_mechanisms": 6}, out

        doc = json.loads((root / "site" / "data" / "global_reg_hta.json").read_text(encoding="utf-8"))
        for k in ("regulatory_agencies", "reliance_frameworks", "hta_bodies", "access_mechanisms"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61N_GLOBAL_REG_HTA_COMPARATOR_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1n Global Regulatory Agencies & HTA Comparator patch.")
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
