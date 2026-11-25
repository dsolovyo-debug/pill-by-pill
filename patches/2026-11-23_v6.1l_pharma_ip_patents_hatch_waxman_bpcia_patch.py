#!/usr/bin/env python3
"""Pill by Pill v6.1l Patch: Pharma IP, Patents, Hatch-Waxman & BPCIA Reference (#/ref/ip, #/explore/ip, /api/ip).

1. Adds `pipeline/build_ip_patents.py` -> `site/data/ip_patents.json` (6 patent layers, 6 Hatch-Waxman /
   Orange Book mechanics, 6 BPCIA / Purple Book biologic frameworks, and 6 LOE/antitrust doctrines —
   24 primary-sourced entries anchored to FDA/eCFR/USPTO/FTC/CBO/EMA/PMC).
2. Adds `site/js/ip_patents.js` (`ipPatentsPage` with inline Patent & Exclusivity Lifecycle SVG +
   4 section filters) and wires `#/ref/ip`, `#/explore/ip`, `/api/ip`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `ip_patents.json` into `pipeline/build_global_search.py`, `pipeline/build_v60_static_pages.py`
   (`/ip/` static SEO page + sitemap entry -> 28 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1l_pharma_ip_patents_hatch_waxman_bpcia_patch.py --selftest
  python3 2026-11-23_v6.1l_pharma_ip_patents_hatch_waxman_bpcia_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_IP_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1l Pharma IP, Patents, Hatch-Waxman & BPCIA Reference (`site/data/ip_patents.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Pharmaceutical Patent Layers & Lifecycle Clocks (6 patent types: Composition of Matter, Method of Use, Formulation/Delivery, Polymorph/Salt, Manufacturing Process, Patent Term Adjustment & Restoration/PTE)\n  2. Hatch-Waxman Act & FDA Orange Book Mechanics (6 pillars: Orange Book Listing Rules, Paragraph I–IV Certifications, 30-Month Stay, 180-Day First-Filer Exclusivity, Section viii Skinny Labeling, Authorized Generics & FTC Scrutiny)\n  3. BPCIA & FDA Purple Book Biologic Litigation (6 pillars: 12-Year Reference Exclusivity vs. 4-Year Filing Bar, The Patent Dance 42 U.S.C. § 262(l), 180-Day Notice of Commercial Marketing, Interchangeability & First Interchangeable Exclusivity, Patent Thickets & Submarine/Continuation Patents, Global SPCs & Data Exclusivity)\n  4. Patent Cliffs, Lifecycle Strategies & Antitrust Boundaries (6 concepts: Loss of Exclusivity Curves, Product Hopping & Hard vs. Soft Switches, Reverse-Payment / Pay-for-Delay Settlements, Citizen Petitions & 505(q), March-In Rights / Bayh-Dole Act, Compulsory Licensing & Medicines Patent Pool)\n\nAll legal anchors are verified HTTPS primary sources (FDA, eCFR, USPTO, FTC, CMS, PMC).\n\nUsage:\n  python3 pipeline/build_ip_patents.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nPATENT_LAYERS = [\n    {\n        "id": "ip-com",\n        "name": "Composition of Matter (Primary Compound) Patent",\n        "strength": "Strongest (\'Crown Jewel\')",\n        "plain": "Protects the exact new active chemical molecule or biologic sequence itself—nobody else can make or sell that molecule for any disease until it expires.",\n        "technical": "Filed early in discovery (often 8–12 years before FDA approval) under 35 U.S.C. § 101/102/103 with a statutory 20-year term from earliest non-provisional filing date. Hardest patent to design around or invalidate.",\n        "url": "https://www.uspto.gov/patents/basics",\n    },\n    {\n        "id": "ip-method-of-use",\n        "name": "Method-of-Use (Indication & Dosing) Patent",\n        "strength": "Moderate (vulnerable to skinny labeling)",\n        "plain": "Covers using a known medicine to treat a specific disease or at a specific dose—allowing companies to protect newly discovered uses years after the original molecule was invented.",\n        "technical": "Listed in the FDA Orange Book with specific \'use codes\' (21 CFR 314.53). Generic ANDAs can often carve out patented indications via Section viii statements while launching for unpatented uses.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "ip-formulation",\n        "name": "Formulation, Delivery & Device Patents",\n        "strength": "Moderate–High (for complex delivery)",\n        "plain": "Protects the recipe or device that delivers the drug—such as a once-daily extended-release tablet, an auto-injector pen, an inhaler, or an LNP fat bubble.",\n        "technical": "Covers excipients, release profiles, amorphous solid dispersions, dry-powder inhalers, and autoinjector mechanisms. Must claim the drug product (not purely standalone device packaging) to be Orange Book listable.",\n        "url": "https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface",\n    },\n    {\n        "id": "ip-polymorph",\n        "name": "Polymorph, Salt, Enantiomer & Crystalline Form Patents",\n        "strength": "Moderate (design-around risk)",\n        "plain": "Protects a specific crystal packing shape, salt form, or mirror-image version of the molecule that dissolves better or stays more stable on pharmacy shelves.",\n        "technical": "Secondary patents covering specific hydrated/anhydrous polymorphs, mesylate/besylate salts, or single enantiomers (e.g., esomeprazole from omeprazole); generics may develop non-infringing polymorphs if bioequivalent.",\n        "url": "https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface",\n    },\n    {\n        "id": "ip-process",\n        "name": "Manufacturing Process & Bioprocess Patents",\n        "strength": "High for Biologics / Moderate for Small Molecules",\n        "plain": "Covers the specific factory recipe—like how cells are fed in a bioreactor or how a chemical reaction is purified—rather than the final pill itself.",\n        "technical": "Cannot be listed in the FDA Orange Book for small molecules (21 CFR 314.53(b)(1)), but plays a central role in BPCIA biologic \'patent dance\' litigation (cell culture media, purification resins, analytical assays).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "ip-pte-pta",\n        "name": "Patent Term Extension (PTE, 35 U.S.C. § 156) & Adjustment (PTA)",\n        "strength": "Restores up to 5 years of lost review time",\n        "plain": "Because FDA clinical trials and reviews eat up half of a 20-year patent before a drug ever reaches patients, U.S. law lets a sponsor restore up to 5 years on one key patent.",\n        "technical": "Hatch-Waxman PTE (35 U.S.C. § 156) restores half of clinical testing time plus full FDA review time on ONE patent per approved active ingredient, capped at 5 years added and 14 years total remaining post-approval. PTA (35 U.S.C. § 154) separately compensates for USPTO examination delays.",\n        "url": "https://www.fda.gov/drugs/development-approval-process-drugs/small-business-assistance-frequently-asked-questions-patent-term-restoration-program",\n    },\n]\n\nHATCH_WAXMAN = [\n    {\n        "id": "hw-orange-book",\n        "name": "FDA Orange Book & Patent Listing Rules",\n        "plain": "The FDA\'s official public registry of approved chemical drugs, their bioequivalent generics, and the patents brand companies claim cover each product.",\n        "technical": "Approved Drug Products with Therapeutic Equivalence Evaluations (Orange Book). Sponsors must submit drug substance, drug product, and method-of-use patents on Form FDA 3542 within 30 days of NDA approval or patent issuance (21 CFR 314.53); process, packaging, and metabolite patents are barred.",\n        "url": "https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface",\n    },\n    {\n        "id": "hw-para-iv",\n        "name": "Paragraph I, II, III & IV Patent Certifications",\n        "plain": "When a generic company applies to copy a brand pill, it must tell the FDA whether it will wait for patents to expire (Paragraph III) or challenge them in court right away (Paragraph IV).",\n        "technical": "Under FD&C Act § 505(j)(2)(A)(vii): Para I (no patent listed), Para II (patent expired), Para III (wait until expiry), Para IV (patent is invalid, unenforceable, or not infringed—constituting a statutory artificial act of infringement under 35 U.S.C. § 271(e)(2)).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "hw-30mo-stay",\n        "name": "The Automatic 30-Month Stay of Generic Approval",\n        "plain": "If a brand drugmaker sues a generic challenger within 45 days of a Paragraph IV notice, the FDA automatically pauses final generic approval for up to 30 months while the court decides the patent fight.",\n        "technical": "Triggered once per NDA under 21 U.S.C. § 355(j)(5)(B)(iii) if the brand holder files an infringement suit within 45 days of receiving the Paragraph IV notice letter; expires earlier if a court rules the patent invalid/not infringed.",\n        "url": "https://www.fda.gov/drugs/abbreviated-new-drug-application-anda/patent-certifications-and-suitability-petitions",\n    },\n    {\n        "id": "hw-180day",\n        "name": "180-Day First-to-File Generic Exclusivity",\n        "plain": "To reward generic companies for spending millions challenging weak patents in court, the first generic filer gets a 6-month head start as the only generic copy on the market.",\n        "technical": "Under 21 U.S.C. § 355(j)(5)(B)(iv), the first substantially complete ANDA submitting a Paragraph IV certification earns 180 days of shared/sole generic market exclusivity from first commercial marketing, subject to MMA forfeiture triggers.",\n        "url": "https://www.fda.gov/drugs/abbreviated-new-drug-application-anda/patent-certifications-and-suitability-petitions",\n    },\n    {\n        "id": "hw-skinny-label",\n        "name": "Section viii \'Skinny Labeling\' (Indication Carve-Out)",\n        "plain": "If a pill\'s original disease use is off-patent but a newer use is still patented, a generic can strip the patented use off its label and launch legally for the older use.",\n        "technical": "21 U.S.C. § 355(j)(2)(A)(viii) statement permits an ANDA applicant to omit a method-of-use patented indication from its labeling without triggering a Paragraph IV 30-month stay (subject to induced-infringement scrutiny in promotional/court disputes).",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314",\n    },\n    {\n        "id": "hw-authorized-generic",\n        "name": "Authorized Generics & FTC Orange Book Oversight",\n        "plain": "Brand companies can launch their own unbranded copy (\'authorized generic\') during a rival\'s 180-day exclusivity window, while the FTC polices improper Orange Book patent listings.",\n        "technical": "Authorized generics are marketed under the original NDA (bypassing ANDA 180-day blocks). Since 2023–2026, the FTC has actively challenged improper device/inhaler Orange Book patent listings as unfair methods of competition.",\n        "url": "https://www.ftc.gov/news-events/topics/competition-enforcement/health-care",\n    },\n]\n\nBPCIA_BIOLOGICS = [\n    {\n        "id": "bpcia-12yr",\n        "name": "BPCIA 12-Year Reference Exclusivity & 4-Year Filing Bar",\n        "plain": "Complex biologic medicines get 12 full years of statutory protection in the U.S. before a biosimilar can be approved—even if their patents expire sooner.",\n        "technical": "Under 42 U.S.C. § 262(k)(7), FDA cannot accept a 351(k) biosimilar application until 4 years after reference BLA first licensure and cannot make approval effective until 12 years after first licensure (+6 months if pediatric exclusivity is earned).",\n        "url": "https://www.fda.gov/drugs/biosimilars/biosimilar-product-information",\n    },\n    {\n        "id": "bpcia-patent-dance",\n        "name": "The BPCIA \'Patent Dance\' (42 U.S.C. § 262(l))",\n        "plain": "Unlike pills, biologics don\'t have a single public patent list with automatic 30-month stays—instead, the biosimilar maker and brand company exchange confidential patent and manufacturing lists in a choreographed legal \'dance.\'",\n        "technical": "Structured multi-step information exchange (application & manufacturing process disclosure within 20 days of FDA acceptance -> Wave 1 immediate litigation list -> Wave 2 notice-of-commercial-marketing patents). Ruled optional by the U.S. Supreme Court in Sandoz v. Amgen (2017).",\n        "url": "https://www.fda.gov/drugs/biosimilars/purple-book-lists-licensed-biological-products-reference-product-exclusivity-and-biosimilarity-or",\n    },\n    {\n        "id": "bpcia-180notice",\n        "name": "180-Day Notice of Commercial Marketing",\n        "plain": "A biosimilar developer must give the brand biologic company at least 180 days\' advance warning before launching on the market so any remaining patent disputes can be heard.",\n        "technical": "Under 42 U.S.C. § 262(l)(8)(A), the 351(k) applicant must provide 180-day pre-marketing notice (which per Sandoz v. Amgen may be delivered before FDA licensure), opening Wave 2 preliminary-injunction litigation.",\n        "url": "https://www.fda.gov/drugs/biosimilars/biosimilar-product-information",\n    },\n    {\n        "id": "bpcia-interchangeable",\n        "name": "Purple Book, Interchangeability & First-Interchangeable Exclusivity",\n        "plain": "The FDA Purple Book tracks biologic licenses and marks which biosimilars are \'interchangeable\'—meaning a pharmacist can substitute them at the counter without calling the doctor first.",\n        "technical": "Purple Book lists reference BLAs, exclusivities, and 351(k) biosimilars. Under 42 U.S.C. § 262(k)(6), the first interchangeable biosimilar receives 12–42 months of exclusivity against subsequent interchangeable approvals (not against non-interchangeable biosimilars).",\n        "url": "https://purplebooksearch.fda.gov/",\n    },\n    {\n        "id": "bpcia-thickets",\n        "name": "Biologic \'Patent Thickets\' & Continuation Estates",\n        "plain": "Major biologic drugs are often surrounded by dozens or over a hundred overlapping patents covering manufacturing tweaks, doses, and buffers—delaying biosimilar launch well past year 12.",\n        "technical": "Dense continuation patent portfolios (e.g., adalimumab/Humira\'s 100+ patents) raise litigation cost and uncertainty, frequently resulting in staggered global biosimilar settlement entry dates (Europe often 4–5 years ahead of the U.S.).",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "bpcia-global-spc",\n        "name": "Global Equivalents: EU Data Exclusivity (8+2+1) & SPCs",\n        "plain": "Outside the U.S., Europe uses an \'8+2+1\' rule—8 years of data protection, 2 years of market exclusivity, plus 1 extra year for major new uses—alongside Supplementary Protection Certificates (SPCs).",\n        "technical": "EU Regulation (EC) No 726/2004 provides 8 years data exclusivity + 2 years market protection (+1 year for significant new indication) uniformly for both small molecules and biologics, plus up to 5-year SPC patent restoration (+6 mo pediatric).",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/marketing-authorisation/data-exclusivity-market-protection-orphan-and-paediatric-rewards",\n    },\n]\n\nLIFECYCLE_ANTITRUST = [\n    {\n        "id": "la-loe-cliff",\n        "name": "Loss of Exclusivity (LOE) & Small-Molecule vs. Biologic Curves",\n        "plain": "When a blockbuster pill loses patent protection, generic pharmacies switch patients almost overnight and prices drop 80–90%—whereas biosimilars usually erode prices more gradually.",\n        "technical": "State automatic generic substitution laws drive rapid >80% unit share loss within months of multi-source ANDA entry. Biologics face slower physician/PBM-driven switching and rebate walls, though PBMs increasingly drive sharp biosimilar shifts.",\n        "url": "https://www.cbo.gov/publication/57025",\n    },\n    {\n        "id": "la-product-hopping",\n        "name": "Lifecycle Management & \'Product Hopping\' (Soft vs. Hard Switches)",\n        "plain": "Before a pill goes generic, companies often launch an improved version—like a once-daily tablet or injection. Persuading doctors to switch is normal (\'soft switch\'), while pulling the old pill off shelves to block generics (\'hard switch\') triggers antitrust lawsuits.",\n        "technical": "Distinguishes lawful follow-on innovation (extended-release, fixed-dose combinations) from anticompetitive \'hard switch\' withdrawal of the legacy reference product before AB-rated generic entry (FTC / Sherman Act § 2 scrutiny).",\n        "url": "https://www.ftc.gov/news-events/topics/competition-enforcement/health-care",\n    },\n    {\n        "id": "la-pay-for-delay",\n        "name": "Reverse-Payment (\'Pay-for-Delay\') Patent Settlements",\n        "plain": "A controversial settlement where a brand drugmaker pays a generic challenger to drop its patent lawsuit and delay launching its cheaper copy—now tightly policed by the FTC and courts.",\n        "technical": "In FTC v. Actavis (2013), the U.S. Supreme Court held that large, unjustified reverse-payment settlements are subject to antitrust \'rule of reason\' scrutiny; MMA mandates filing all brand-generic settlement agreements with the FTC and DOJ.",\n        "url": "https://www.ftc.gov/news-events/topics/competition-enforcement/health-care",\n    },\n    {\n        "id": "la-citizen-petitions",\n        "name": "FDA Citizen Petitions & FD&C Act § 505(q)",\n        "plain": "Anyone can file a formal scientific petition asking the FDA to require extra testing on a pending generic—so Congress passed a 150-day deadline rule to stop sham petitions from stalling generics.",\n        "technical": "21 U.S.C. § 355(q) prevents FDA from delaying ANDA/505(b)(2)/351(k) approval due to a citizen petition unless necessary to protect public health, requires FDA response within 150 days, and mandates annual Congressional reporting.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/citizen-petitions-and-petitions-stay-action-subject-section-505q-federal-food-drug-and-cosmetic-act",\n    },\n    {\n        "id": "la-bayh-dole",\n        "name": "Bayh-Dole Act (1980) & Government \'March-In\' Rights",\n        "plain": "Allows universities and startups to patent discoveries funded by federal NIH grants so private companies will invest in turning them into medicines, while reserving an emergency government \'march-in\' clause.",\n        "technical": "35 U.S.C. §§ 200–212 governs federally funded inventions; § 203 march-in rights permit agencies to grant non-exclusive licenses if practical application or health/safety needs are unmet (historically never exercised on drug pricing alone, though actively debated).",\n        "url": "https://www.uspto.gov/patents/basics",\n    },\n    {\n        "id": "la-mpp-compulsory",\n        "name": "Voluntary Licensing (Medicines Patent Pool) & TRIPS Flexibilities",\n        "plain": "To get patented life-saving medicines to lower-income countries years early, patent holders often license them voluntarily through the UN-backed Medicines Patent Pool so generic makers can sell them at low cost.",\n        "technical": "WTO TRIPS Agreement permits compulsory licensing in public health emergencies, while the Unitaid-founded Medicines Patent Pool (MPP) negotiates voluntary non-exclusive generic sublicenses across HIV, HCV, TB, and COVID-19 antivirals.",\n        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5444652/",\n    },\n]\n\n\ndef build_ip_patents(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced educational reference on pharmaceutical patents, FDA Orange Book / Hatch-Waxman, Purple Book / BPCIA, and competition law (FDA, eCFR, USPTO, FTC, CBO, EMA). Educational reference only—not legal advice.",\n        "patent_layers": PATENT_LAYERS,\n        "hatch_waxman": HATCH_WAXMAN,\n        "bpcia_biologics": BPCIA_BIOLOGICS,\n        "lifecycle_antitrust": LIFECYCLE_ANTITRUST,\n    }\n    (data_dir / "ip_patents.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "patent_layers": len(PATENT_LAYERS),\n        "hatch_waxman": len(HATCH_WAXMAN),\n        "bpcia_biologics": len(BPCIA_BIOLOGICS),\n        "lifecycle_antitrust": len(LIFECYCLE_ANTITRUST),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_ip_patents(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
IP_PATENTS_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderIpTimelineSvg() {\n  const nodes = [\n    { x: 8, label: "1. Patent Filing", sub: "20-Yr Statutory Clock" },\n    { x: 140, label: "2. FDA Approval", sub: "5-Yr NCE / 12-Yr BLA" },\n    { x: 272, label: "3. PTE Restore", sub: "Up to +5 Yrs (§ 156)" },\n    { x: 404, label: "4. Challenge", sub: "Para IV / Patent Dance" },\n    { x: 536, label: "5. LOE Entry", sub: "Generic / Biosimilar" },\n  ];\n  return html`<figure class="ip-flow" aria-label="Pharmaceutical patent and statutory exclusivity lifecycle">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 4 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 4 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Typical pharmaceutical IP &amp; regulatory exclusivity timeline from discovery patent filing to Loss of Exclusivity (LOE).</figcaption>\n  </figure>`;\n}\n\nexport async function ipPatentsPage(query, mode = "ref") {\n  const doc = await getJSON("data/ip_patents.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/ip" : "#/ref/ip";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Pharma IP, Patents, Hatch-Waxman & BPCIA Reference",\n    body: html`\n      <h1>Pharmaceutical IP, Patents, Hatch-Waxman &amp; BPCIA</h1>\n      <p class="lead">${mode === "explore"\n        ? "How drug patents work, why brand medicines have a temporary window before generic copies arrive, and how the rules differ between chemical pills (Orange Book) and biologic injections (Purple Book)."\n        : "Primary-sourced reference covering 6 pharmaceutical patent layers, 6 Hatch-Waxman & Orange Book mechanics, 6 BPCIA & Purple Book biologic frameworks, and 6 lifecycle/antitrust doctrines (checked " + doc.checked + ")."}</p>\n\n      ${renderIpTimelineSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=layers"${sec === "layers" ? \' aria-current="page"\' : ""}>Patent Layers (6)</a> ·\n        <a href="${base}?section=hatch"${sec === "hatch" ? \' aria-current="page"\' : ""}>Hatch-Waxman / Orange Book (6)</a> ·\n        <a href="${base}?section=bpcia"${sec === "bpcia" ? \' aria-current="page"\' : ""}>BPCIA / Purple Book (6)</a> ·\n        <a href="${base}?section=antitrust"${sec === "antitrust" ? \' aria-current="page"\' : ""}>LOE &amp; Antitrust (6)</a>\n      </p>\n\n      ${show("layers") ? html`\n        <h2 id="layers">1. Pharmaceutical Patent Layers &amp; Term Restoration (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Pharmaceutical patent layers">\n          <table class="tbl"><thead><tr><th>Patent Layer</th><th>Relative Strength</th><th>${mode === "explore" ? "What It Protects" : "Legal Scope & Statutory Basis"}</th></tr></thead>\n          <tbody>${(doc.patent_layers || []).map((p) => html`<tr id="${p.id}">\n            <td><b><a href="${p.url}" target="_blank" rel="noopener">${p.name}</a></b></td>\n            <td>${p.strength}</td>\n            <td>${mode === "explore" ? p.plain : html`${p.plain}<br><span class="muted small">${p.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("hatch") ? html`\n        <h2 id="hatch">2. Hatch-Waxman Act &amp; FDA Orange Book Mechanics (Small Molecules)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Hatch-Waxman and Orange Book">\n          <table class="tbl"><thead><tr><th>Mechanism</th><th>${mode === "explore" ? "How It Works" : "Plain & Statutory Mechanics"}</th></tr></thead>\n          <tbody>${(doc.hatch_waxman || []).map((h) => html`<tr id="${h.id}">\n            <td><b><a href="${h.url}" target="_blank" rel="noopener">${h.name}</a></b></td>\n            <td>${mode === "explore" ? h.plain : html`${h.plain}<br><span class="muted small">${h.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("bpcia") ? html`\n        <h2 id="bpcia">3. BPCIA, Purple Book &amp; Global Biologic Exclusivities</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="BPCIA and Purple Book">\n          <table class="tbl"><thead><tr><th>Framework</th><th>${mode === "explore" ? "How It Works" : "Plain & Statutory Mechanics"}</th></tr></thead>\n          <tbody>${(doc.bpcia_biologics || []).map((b) => html`<tr id="${b.id}">\n            <td><b><a href="${b.url}" target="_blank" rel="noopener">${b.name}</a></b></td>\n            <td>${mode === "explore" ? b.plain : html`${b.plain}<br><span class="muted small">${b.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("antitrust") ? html`\n        <h2 id="antitrust">4. Patent Cliffs (LOE), Lifecycle Strategies &amp; Antitrust Boundaries</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="LOE and antitrust boundaries">\n          <table class="tbl"><thead><tr><th>Doctrine / Dynamic</th><th>${mode === "explore" ? "Why It Matters" : "Economic & Antitrust Analysis"}</th></tr></thead>\n          <tbody>${(doc.lifecycle_antitrust || []).map((a) => html`<tr id="${a.id}">\n            <td><b><a href="${a.url}" target="_blank" rel="noopener">${a.name}</a></b></td>\n            <td>${mode === "explore" ? a.plain : html`${a.plain}<br><span class="muted small">${a.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/pathways">Approval Pathways &amp; Exclusivities</a> · <a href="#/ref/economics">Drug Economics &amp; GTN</a> · <a href="#/ref/departments/commercial">Stage 7: Commercial &amp; Market Access</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { ipPatentsPage } from "./ip_patents.js";\n'
    if "./ip_patents.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/ip"' not in txt:
        for anchor in ('if (path === "/ref/safety")', 'if (path === "/ref/adme")', 'if (path === "/ref/trials")', 'if (path === "/ref/pathways")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/ip") return ipPatentsPage(query, "ref");\n'
                    '  if (path === "/explore/ip") return ipPatentsPage(query, "explore");\n'
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
    if "#/ref/ip" not in txt:
        for anchor in ('["#/ref/safety", "Drug safety & PV"]', '["#/ref/economics", "Drug economics"]', '["#/ref/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/ip", "Patents & IP"]', 1)
                changed = True
                break
    if "#/explore/ip" not in txt:
        for anchor in ('["#/explore/safety", "Drug safety & PV"]', '["#/explore/economics", "Funding & pricing"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/ip", "Patents & IP"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_ip_patents.py" in txt:
        return False
    hook = "\n# v6.1l: Pharma IP, Patents, Hatch-Waxman & BPCIA Reference\npython3 pipeline/build_ip_patents.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/ip"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/ip")\n'
        'def api_ip_patents():\n'
        '    return _read_json(SITE_DIR / "data" / "ip_patents.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"ip_patents.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    ip_ref = _load(data_dir / "ip_patents.json", {}) or {}\n'
        '    for sec_key, sec_q in [("patent_layers", "layers"), ("hatch_waxman", "hatch"), ("bpcia_biologics", "bpcia"), ("lifecycle_antitrust", "antitrust")]:\n'
        '        for item in (ip_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "ip_patent",\n'
        '                "group": "Patents, Hatch-Waxman & BPCIA",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/ip?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/ip?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"patent IP Hatch-Waxman Orange Book BPCIA Purple Book {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"ip", "#/ref/ip"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    ip_doc = _load_json(data_dir / "ip_patents.json")\n'
        '    if isinstance(ip_doc, dict) and ip_doc.get("patent_layers"):\n'
        '        ip_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (ip_doc.get("patent_layers") or []) + (ip_doc.get("hatch_waxman") or []))\n'
        '        pages.append(("ip", "#/ref/ip", "Pharmaceutical IP, Patents, Hatch-Waxman & BPCIA",\n'
        '                      "Primary-sourced guide to composition-of-matter & secondary patents, Patent Term Extension, FDA Orange Book Paragraph IV & 30-month stays, Purple Book BPCIA patent dance, and LOE antitrust.",\n'
        '                      f"<ul>{ip_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/ip"' in txt:
        return False
    for anchor in ('    "/#/explore/safety",', '    "/#/explore/adme",', '    "/#/explore/trials",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/ip",\n    "/#/explore/ip",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_ip_patents_py": _write_if_changed(pipe_dir / "build_ip_patents.py", BUILD_IP_PY),
        "ip_patents_js": _write_if_changed(js_dir / "ip_patents.js", IP_PATENTS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/safety") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/safety", "Drug safety & PV"]] }];\nconst EXPLORE_NAV = [["#/explore/safety", "Drug safety & PV"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/safety",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_ip_patents.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_ip_patents.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"patent_layers": 6, "hatch_waxman": 6, "bpcia_biologics": 6, "lifecycle_antitrust": 6}, out

        doc = json.loads((root / "site" / "data" / "ip_patents.json").read_text(encoding="utf-8"))
        for k in ("patent_layers", "hatch_waxman", "bpcia_biologics", "lifecycle_antitrust"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61L_PHARMA_IP_PATENTS_HATCH_WAXMAN_BPCIA_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1l Pharma IP, Patents, Hatch-Waxman & BPCIA patch.")
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
