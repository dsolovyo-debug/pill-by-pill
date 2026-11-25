#!/usr/bin/env python3
"""Pill by Pill v6.1t Patch: Drug-Device Combination Products & Delivery Engineering (#/ref/combo-devices, #/explore/combo-devices, /api/combo-devices).

1. Adds `pipeline/build_combo_devices.py` -> `site/data/combo_devices.json` (6 Part 3/4 & EU MDR
   regulatory pillars, 6 injectable device engineering pillars, 6 inhalation/nasal/ophthalmic
   pillars, and 6 transdermal/depot/Human Factors Engineering pillars — 24 primary-sourced entries).
2. Adds `site/js/combo_devices.js` (`comboDevicesPage` with inline Lifecycle SVG + 4 section
   filters) and wires `#/ref/combo-devices`, `#/explore/combo-devices`, `/api/combo-devices`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `combo_devices.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/combo-devices/` static SEO page + sitemap entry -> 36
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.1t_combination_products_delivery_engineering_patch.py --selftest
  python3 2026-11-24_v6.1t_combination_products_delivery_engineering_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_COMBO_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1t Drug-Device Combination Products & Delivery Engineering (`site/data/combo_devices.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Combination Product Regulation & Primary Mode of Action (6 pillars: 21 CFR Part 3 PMOA & OCP RFD, 21 CFR Part 4 Streamlined cGMP/QSR, Cross-Labeled vs. Single-Entity vs. Co-Packaged, Lead Center Assignment CDER/CBER/CDRH, EU MDR Article 117 Notified Body Opinion, Post-Market Safety Reporting 21 CFR Part 4 Subpart B)\n  2. Injectable Delivery Engineering (6 pillars: Prefilled Syringes & Silicone/Tungsten Control, Spring & Motor-Driven Autoinjectors, On-Body Large-Volume Wearable Injectors, Multi-Dose Pen Injectors & Cartridges, Needle Safety & ISO 11608 Standards, High-Concentration Viscosity & Glide Force Engineering)\n  3. Inhalation, Nasal & Ophthalmic Delivery (6 pillars: Pressurized Metered-Dose Inhalers pMDIs & Low-GWP Propellants, Dry Powder Inhalers DPIs & Aerodynamic Particle Size, Soft-Mist Inhalers & Nebulizers, Nasal Sprays & Nose-to-Brain Rescue Delivery, Ophthalmic Preservative-Free Multi-Dose Dispensers, Emitted Dose & Cascade Impaction QC)\n  4. Transdermal, Implantable & Human-Factors Engineering (6 pillars: Transdermal Matrix & Reservoir Patches, Long-Acting Depot Injectables & Subdermal Implants, Drug-Eluting Stents & Local Polymer Release, Human Factors & Usability Engineering HFE, Use-Related Risk Analysis uFMEA & Summative Studies, Connected Combination Products & Sustainability)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, eCFR, EMA).\n\nUsage:\n  python3 pipeline/build_combo_devices.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-24"\n\nCOMBO_REGULATION = [\n    {\n        "id": "cmb-pmoa-ocp",\n        "name": "Primary Mode of Action (PMOA) & Office of Combination Products (21 CFR Part 3)",\n        "plain": "When a product combines a medicine and a medical device—like an EpiPen or asthma inhaler—the FDA decides which center leads the review based on whichever part does the main therapeutic job (the drug or the device).",\n        "technical": "Under 21 CFR Part 3, the FDA Office of Combination Products (OCP) assigns lead jurisdiction (CDER, CBER, or CDRH) via Request for Designation (RFD) or Pre-RFD based on the Primary Mode of Action (PMOA), with mandatory inter-center consultation.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-3",\n    },\n    {\n        "id": "cmb-types",\n        "name": "Single-Entity, Co-Packaged & Cross-Labeled Combination Products",\n        "plain": "Combination products come in three forms: fused together in one unit (a prefilled autoinjector), boxed together (a vial plus a special syringe), or sold separately but labeled to be used together.",\n        "technical": "21 CFR 3.2(e) defines Single-Entity (chemically/physically combined, e.g., drug-eluting stent, prefilled syringe), Co-Packaged (kit), and Cross-Labeled (separate products mutually required for intended use).",\n        "url": "https://www.fda.gov/combination-products/about-combination-products",\n    },\n    {\n        "id": "cmb-part4-cgmp",\n        "name": "Streamlined cGMP & Quality System Compliance (21 CFR Part 4 Subpart A)",\n        "plain": "Factories making drug-device combinations don\'t have to build two completely separate quality manuals—they follow drug cGMP plus specific medical-device design-control rules.",\n        "technical": "21 CFR Part 4 Subpart A allows a streamlined compliance model: Drug cGMP (21 CFR 210/211) supplemented by core Device Quality Management System Regulation (QMSR / 21 CFR 820, harmonized with ISO 13485) design controls, purchasing, and CAPA.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-4",\n    },\n    {\n        "id": "cmb-design-controls",\n        "name": "Device Design Controls (Design History File, Verification & Validation)",\n        "plain": "Every spring, plunger, and safety cap must be engineered with formal blueprints, drop tests, and real-patient usability checks before the first commercial unit ever ships.",\n        "technical": "Design Controls (User Needs -> Design Inputs -> Design Outputs -> Design Verification -> Design Validation -> Design Transfer) documented in a Design History File (DHF) and Device Master Record (DMR).",\n        "url": "https://www.fda.gov/combination-products/guidance-regulatory-information/combination-products-guidance-documents",\n    },\n    {\n        "id": "cmb-eu-mdr-117",\n        "name": "EU MDR Article 117 (Notified Body Opinion for Integral Drug-Device Products)",\n        "plain": "In Europe, a drug-led prefilled pen or inhaler cannot be approved by the EMA alone—an independent medical-device Notified Body must first certify that the device hardware meets EU safety standards.",\n        "technical": "Regulation (EU) 2017/745 (MDR) Article 117 requires Marketing Authorisation Applications for integral drug-device combination products to include a Notified Body Opinion (NBOp) verifying General Safety and Performance Requirements (GSPRs).",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/medical-devices/medical-devices-legislation",\n    },\n    {\n        "id": "cmb-pmsr",\n        "name": "Post-Market Safety Reporting (PMSR, 21 CFR Part 4 Subpart B)",\n        "plain": "If a spring jams, a needle bends, or a dose fails to fire at home, the company must report both drug side effects AND device malfunctions to the FDA under strict timelines.",\n        "technical": "21 CFR Part 4 Subpart B mandates constituent-part-based post-market reporting combining 15-day drug Alert Reports (AEMS) with 5-day/30-day Medical Device Reports (MDRs) and field-alert / correction-removal notices.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-4",\n    },\n]\n\nINJECTABLE_DEVICES = [\n    {\n        "id": "inj-pfs",\n        "name": "Prefilled Syringes (PFS) & Silicone / Tungsten Control",\n        "plain": "Ready-to-use glass or plastic syringes filled in the factory reduce dosing errors and needle sticks—but engineers must carefully control tiny traces of silicone lubricant and tungsten so fragile biologic proteins don\'t clump.",\n        "technical": "Type I borosilicate glass or cyclic olefin polymer (COP) barrels; baked-on silicone or silicone-free elastomer plungers minimize subvisible silicone-oil droplets (USP <788>) and tungsten-induced protein aggregation.",\n        "url": "https://www.fda.gov/combination-products/guidance-regulatory-information/combination-products-guidance-documents",\n    },\n    {\n        "id": "inj-autoinjectors",\n        "name": "Spring- & Motor-Driven Autoinjectors (Home Self-Injection)",\n        "plain": "Hides the needle inside a pen-like body so patients just press against their skin, hear a click, and receive a precise dose automatically—turning hospital infusions into 10-second home injections.",\n        "technical": "Two-step push-on-skin autoinjectors incorporate primary PFS/cartridge, spring or electromechanical drive, needle-shield lockout, audible/visual/tactile feedback, and essential performance testing per ISO 11608.",\n        "url": "https://www.fda.gov/combination-products/about-combination-products",\n    },\n    {\n        "id": "inj-onbody",\n        "name": "On-Body Delivery Systems (OBDS / Large-Volume Wearable Injectors)",\n        "plain": "Adhesive patch-pumps that stick to the stomach or arm and slowly infuse larger volumes (3–20+ mL) of antibody medicines under the skin over minutes while the patient goes about their day.",\n        "technical": "Overcomes the ~2 mL subcutaneous bolus limit via programmable micro-pumps or co-formulation with recombinant human hyaluronidase (rHuPH20) to transiently open subcutaneous extracellular matrix.",\n        "url": "https://www.fda.gov/combination-products/about-combination-products",\n    },\n    {\n        "id": "inj-pens",\n        "name": "Multi-Dose Pen Injectors & Glass Cartridges",\n        "plain": "Reusable or disposable dial-a-dose pens (used for insulin and GLP-1 medicines) let patients click to their exact dose and swap a fresh tiny pen needle for each injection.",\n        "technical": "Variable- or fixed-dose mechanical/connected pens housing preserved multi-dose glass cartridges (typically 1.5–3 mL) validated for dose accuracy across cold, room, and elevated temperature extremes (ISO 11608-1).",\n        "url": "https://www.fda.gov/combination-products/guidance-regulatory-information/combination-products-guidance-documents",\n    },\n    {\n        "id": "inj-iso11608",\n        "name": "Essential Performance, Dose Accuracy & ISO 11608 Standards",\n        "plain": "Every injector design must pass brutal real-world stress tests—surviving drops onto concrete, hot car trunks, freezing shipping, and thousands of cycles while still delivering the exact dose.",\n        "technical": "FDA-recognized ISO 11608 series governs needle-based injection systems (NIS): dose accuracy, break-loose and glide forces, actuation force, injection time, extended needle length, and free-fall/vibration preconditioning.",\n        "url": "https://www.fda.gov/medical-devices/standards-and-conformity-assessment-program/recognized-consensus-standards",\n    },\n    {\n        "id": "inj-viscosity",\n        "name": "High-Concentration Biologic Viscosity & Glide-Force Engineering",\n        "plain": "Packing a high antibody dose into a tiny syringe makes the liquid thick like honey—requiring thin-wall needles, special viscosity-lowering amino acids, and stronger springs so patients can still inject comfortably.",\n        "technical": "Hagen-Poiseuille fluid dynamics dictate injection force scales inversely with the fourth power of needle inner radius; engineers pair ultra-thin-wall 27G/29G needles with arginine/proline excipients to keep viscosity manageable (<15–20 cP).",\n        "url": "https://www.fda.gov/combination-products/guidance-regulatory-information/combination-products-guidance-documents",\n    },\n]\n\nINHALATION_NASAL = [\n    {\n        "id": "inh-pmdi",\n        "name": "Pressurized Metered-Dose Inhalers (pMDIs) & Low-GWP Propellants",\n        "plain": "Pressurized spray canisters that deliver a measured mist of asthma or COPD medicine with each press—currently transitioning to next-generation climate-friendly propellants.",\n        "technical": "Metering valve + pressurized canister + actuator orifice; after the CFC-to-HFA phase-out, manufacturers are reformulating from high-GWP HFA-134a/227ea to near-zero-GWP HFA-152a and HFO-1234ze(E) propellants.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/metered-dose-inhaler-mdi-and-dry-powder-inhaler-dpi-drug-products-quality-considerations",\n    },\n    {\n        "id": "inh-dpi",\n        "name": "Dry Powder Inhalers (DPIs) & Aerodynamic Particle Engineering",\n        "plain": "Breath-actuated inhalers with no propellant spray—the patient\'s own inhale pulls microscopic dry powder particles (1–5 microns) deep into the lungs without needing hand-breath coordination.",\n        "technical": "Passive breath-actuated devices (reservoir, blister strip, or capsule-based) rely on micronized API blended with lactose carrier or spray-dried porous particles targeting Mass Median Aerodynamic Diameter (MMAD) of 1–5 µm.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/metered-dose-inhaler-mdi-and-dry-powder-inhaler-dpi-drug-products-quality-considerations",\n    },\n    {\n        "id": "inh-smi-neb",\n        "name": "Soft-Mist Inhalers (SMIs) & Vibrating-Mesh Nebulizers",\n        "plain": "Generates a slow-moving, gentle cloud of liquid droplets that hangs in the air longer—making deep lung delivery far easier for young children, older adults, or patients with weak breaths.",\n        "technical": "Propellant-free mechanical nozzle collision (SMI) or piezoelectric vibrating-mesh nebulizers produce high Fine Particle Fraction (FPF) at low plume velocity, reducing oropharyngeal deposition.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/metered-dose-inhaler-mdi-and-dry-powder-inhaler-dpi-drug-products-quality-considerations",\n    },\n    {\n        "id": "inh-nasal",\n        "name": "Nasal Sprays & Rapid Emergency Rescue Delivery",\n        "plain": "Because the inside of the nose is packed with blood vessels, unit-dose nasal sprays deliver life-saving rescue drugs (like naloxone for overdose or epinephrine for anaphylaxis) into the bloodstream in minutes without a needle.",\n        "technical": "FDA Nasal Spray BA/BE Guidance controls spray pattern, plume geometry, droplet size distribution (Dv10/Dv50/Dv90 via laser diffraction), and shot-weight uniformity for both local (allergic rhinitis) and systemic rescue drugs.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/bioavailability-and-bioequivalence-studies-nasal-aerosols-and-nasal-sprays-local-action",\n    },\n    {\n        "id": "inh-ophthalmic",\n        "name": "Preservative-Free Multi-Dose Ophthalmic Dispensers",\n        "plain": "Special one-way valve eye-drop bottles keep sterile liquid germ-free for months without harsh chemical preservatives (like BAK) that irritate dry or glaucoma-treated eyes.",\n        "technical": "Engineered microbial-barrier tip valves and airless pump systems prevent suck-back contamination while delivering consistent microliter drop volume and passing USP <51>/<71> container-closure sterility.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/quality-considerations-topical-ophthalmic-drug-products",\n    },\n    {\n        "id": "inh-cascade",\n        "name": "Inhaler QC: Delivered Dose Uniformity & Cascade Impaction",\n        "plain": "Lab machines \'breathe\' through every test inhaler and sort the mist across metal plates mimicking the throat and lungs to prove the exact fraction reaches the deep airways.",\n        "technical": "Aerodynamic Particle Size Distribution (APSD) via Next Generation Impactor (NGI) or Andersen Cascade Impactor (ACI) per USP <601>, plus Delivered Dose Uniformity (DDU) across beginning, middle, and end of canister life.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/metered-dose-inhaler-mdi-and-dry-powder-inhaler-dpi-drug-products-quality-considerations",\n    },\n]\n\nTRANSDERMAL_HFE = [\n    {\n        "id": "td-patches",\n        "name": "Transdermal Delivery Systems (TDS: Matrix & Reservoir Patches)",\n        "plain": "Medicated skin patches slowly release steady drug levels through the skin over 1 to 7 days—avoiding stomach upset and liver breakdown while keeping blood levels smooth.",\n        "technical": "Drug-in-adhesive matrix or rate-controlling membrane patches require FDA adhesion studies, cold-flow/crystallization control, residual drug minimization (especially for fentanyl/opioids), and heat-effect PK testing.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/transdermal-and-topical-delivery-systems-product-development-and-quality-considerations",\n    },\n    {\n        "id": "td-depots-implants",\n        "name": "Long-Acting Injectable Depots (PLGA Microspheres) & Implants",\n        "plain": "Biodegradable microscopic spheres or tiny under-the-skin rods dissolve slowly over 1 to 6 months—replacing daily pills with a few clinic visits a year for mental health, contraception, or HIV prevention.",\n        "technical": "Poly(lactic-co-glycolic acid) (PLGA) microspheres, in situ forming gels, nanocrystal suspensions, and solid rods engineered for controlled tri-phasic release without burst-release toxicity.",\n        "url": "https://www.fda.gov/combination-products/about-combination-products",\n    },\n    {\n        "id": "td-des",\n        "name": "Drug-Eluting Stents (DES) & Local Polymer Release Devices",\n        "plain": "Tiny wire mesh tubes propping open blocked heart arteries coated with a slow-release medicine that stops scar tissue from re-clogging the artery.",\n        "technical": "Device-led (CDRH PMOA) single-entity combination products coating metal scaffolds with antiproliferative drugs (e.g., everolimus, zotarolimus) in durable or bioabsorbable polymers.",\n        "url": "https://www.fda.gov/combination-products/about-combination-products",\n    },\n    {\n        "id": "td-hfe",\n        "name": "Human Factors & Usability Engineering (HFE / IEC 62366)",\n        "plain": "Designs devices for real, stressed, arthritic, or visually impaired humans—not lab engineers—so a patient can\'t accidentally inject their thumb, forget to remove a cap, or miss a dose.",\n        "technical": "FDA Human Factors Guidance and IEC 62366-1 mandate iterative formative usability testing followed by a Summative Human Factors Validation Study (>=15 representative users per distinct user group) in simulated real-world environments.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices",\n    },\n    {\n        "id": "td-ufmea",\n        "name": "Use-Related Risk Analysis (uFMEA) & Critical Tasks",\n        "plain": "Maps out every single step a patient takes—from opening the fridge to pressing the button—and fixes every step where a predictable mistake could cause harm or a missed dose.",\n        "technical": "Use-Failure Modes and Effects Analysis (uFMEA) identifies critical tasks whose failure could cause serious injury or compromised therapy; FDA requires engineering/design mitigations before relying solely on instructions or training.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/human-factors-studies-and-related-clinical-study-considerations-combination-product-design-and",\n    },\n    {\n        "id": "td-connected-green",\n        "name": "Connected Combination Products & Device Sustainability",\n        "plain": "Next-generation reusable pen bases, Bluetooth dose-logging add-ons, and recyclable cartridge systems reduce single-use plastic waste while helping patients track adherence.",\n        "technical": "Separates reusable electromechanical/Bluetooth modules from disposable sterile primary drug cartridges, balancing wireless cybersecurity (FDORA § 524B) with environmental lifecycle reduction.",\n        "url": "https://www.fda.gov/combination-products/about-combination-products",\n    },\n]\n\n\ndef build_combo_devices(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on FDA/EU drug-device combination products, injectable/inhalation/transdermal delivery engineering, ISO 11608, and Human Factors Engineering (FDA, eCFR, EMA). Educational reference only.",\n        "combo_regulation": COMBO_REGULATION,\n        "injectable_devices": INJECTABLE_DEVICES,\n        "inhalation_nasal": INHALATION_NASAL,\n        "transdermal_hfe": TRANSDERMAL_HFE,\n    }\n    (data_dir / "combo_devices.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "combo_regulation": len(COMBO_REGULATION),\n        "injectable_devices": len(INJECTABLE_DEVICES),\n        "inhalation_nasal": len(INHALATION_NASAL),\n        "transdermal_hfe": len(TRANSDERMAL_HFE),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_combo_devices(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
COMBO_DEVICES_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderComboSvg() {\n  const nodes = [\n    { x: 8, label: "1. PMOA & OCP", sub: "21 CFR Part 3" },\n    { x: 140, label: "2. Design & uFMEA", sub: "Part 4 / ISO 11608" },\n    { x: 272, label: "3. Human Factors", sub: "Summative HFE" },\n    { x: 404, label: "4. Joint Review", sub: "CDER + CDRH / MDR" },\n    { x: 536, label: "5. PMSR Monitor", sub: "AEMS + MDRs" },\n  ];\n  return html`<figure class="combo-flow" aria-label="Drug-device combination product development and regulatory lifecycle">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 2 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 2 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Drug-device combination product lifecycle from PMOA designation and design controls through summative Human Factors validation and post-market reporting.</figcaption>\n  </figure>`;\n}\n\nexport async function comboDevicesPage(query, mode = "ref") {\n  const doc = await getJSON("data/combo_devices.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/combo-devices" : "#/ref/combo-devices";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Drug-Device Combination Products & Delivery Engineering",\n    body: html`\n      <h1>Drug-Device Combination Products &amp; Delivery Engineering</h1>\n      <p class="lead">${mode === "explore"\n        ? "How modern delivery devices—autoinjector pens, wearable patch pumps, asthma inhalers, nasal rescue sprays, and medicated skin patches—are engineered and human-tested so patients can use them safely at home."\n        : "Primary-sourced reference covering 21 CFR Parts 3 & 4 / EU MDR Art. 117 regulation, injectable device engineering (ISO 11608), inhalation/nasal/ophthalmic delivery, and transdermal/depot/Human Factors Engineering (checked " + doc.checked + ")."}</p>\n\n      ${renderComboSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=regulation"${sec === "regulation" ? \' aria-current="page"\' : ""}>21 CFR 3/4 &amp; MDR (6)</a> ·\n        <a href="${base}?section=injectables"${sec === "injectables" ? \' aria-current="page"\' : ""}>Pens &amp; Autoinjectors (6)</a> ·\n        <a href="${base}?section=inhalation"${sec === "inhalation" ? \' aria-current="page"\' : ""}>Inhalers &amp; Nasal (6)</a> ·\n        <a href="${base}?section=hfe"${sec === "hfe" ? \' aria-current="page"\' : ""}>Patches, Depots &amp; HFE (6)</a>\n      </p>\n\n      ${show("regulation") ? html`\n        <h2 id="regulation">1. Combination Product Regulation &amp; Quality Systems (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Combination product regulation">\n          <table class="tbl"><thead><tr><th>Regulatory Pillar</th><th>${mode === "explore" ? "How It Is Regulated" : "PMOA, Part 4 cGMP/QMSR & EU MDR"}</th></tr></thead>\n          <tbody>${(doc.combo_regulation || []).map((r) => html`<tr id="${r.id}">\n            <td><b><a href="${r.url}" target="_blank" rel="noopener">${r.name}</a></b></td>\n            <td>${mode === "explore" ? r.plain : html`${r.plain}<br><span class="muted small">${r.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("injectables") ? html`\n        <h2 id="injectables">2. Injectable Delivery Engineering: PFS, Autoinjectors &amp; OBDS (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Injectable delivery devices">\n          <table class="tbl"><thead><tr><th>Device Technology</th><th>${mode === "explore" ? "How It Works for Patients" : "Engineering & ISO 11608 Standards"}</th></tr></thead>\n          <tbody>${(doc.injectable_devices || []).map((i) => html`<tr id="${i.id}">\n            <td><b><a href="${i.url}" target="_blank" rel="noopener">${i.name}</a></b></td>\n            <td>${mode === "explore" ? i.plain : html`${i.plain}<br><span class="muted small">${i.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("inhalation") ? html`\n        <h2 id="inhalation">3. Inhalation, Nasal Rescue &amp; Ophthalmic Delivery (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Inhalation, nasal, and ophthalmic delivery">\n          <table class="tbl"><thead><tr><th>Delivery System</th><th>${mode === "explore" ? "How It Delivers Medicine" : "Aerosol Physics & USP <601> QC"}</th></tr></thead>\n          <tbody>${(doc.inhalation_nasal || []).map((n) => html`<tr id="${n.id}">\n            <td><b><a href="${n.url}" target="_blank" rel="noopener">${n.name}</a></b></td>\n            <td>${mode === "explore" ? n.plain : html`${n.plain}<br><span class="muted small">${n.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("hfe") ? html`\n        <h2 id="hfe">4. Transdermal Patches, Depots &amp; Human Factors Engineering (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Transdermal, depots, and human factors engineering">\n          <table class="tbl"><thead><tr><th>Engineering Pillar</th><th>${mode === "explore" ? "Why It Matters" : "Release Kinetics, uFMEA & IEC 62366"}</th></tr></thead>\n          <tbody>${(doc.transdermal_hfe || []).map((h) => html`<tr id="${h.id}">\n            <td><b><a href="${h.url}" target="_blank" rel="noopener">${h.name}</a></b></td>\n            <td>${mode === "explore" ? h.plain : html`${h.plain}<br><span class="muted small">${h.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/routes">Routes of Administration</a> · <a href="#/ref/sterile">Sterile &amp; Bioprocessing</a> · <a href="#/ref/adme">ADME/PK &amp; Formulation</a> · <a href="#/ref/safety">Drug Safety &amp; DMEPA</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { comboDevicesPage } from "./combo_devices.js";\n'
    if "./combo_devices.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/combo-devices"' not in txt:
        for anchor in ('if (path === "/ref/otc")', 'if (path === "/ref/rare-pediatric")', 'if (path === "/ref/rwe")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/combo-devices") return comboDevicesPage(query, "ref");\n'
                    '  if (path === "/explore/combo-devices") return comboDevicesPage(query, "explore");\n'
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
    if "#/ref/combo-devices" not in txt:
        for anchor in ('["#/ref/otc", "OTC & compounding"]', '["#/ref/sterile", "Sterile & bioprocessing"]', '["#/ref/routes", "Routes of administration"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/combo-devices", "Combination devices"]', 1)
                changed = True
                break
    if "#/explore/combo-devices" not in txt:
        for anchor in ('["#/explore/otc", "OTC & compounding"]', '["#/explore/sterile", "Sterile & bioprocessing"]', '["#/explore/pathways", "Approval pathways"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/combo-devices", "Combination devices"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_combo_devices.py" in txt:
        return False
    hook = "\n# v6.1t: Drug-Device Combination Products & Delivery Engineering\npython3 pipeline/build_combo_devices.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/combo-devices"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/combo-devices")\n'
        'def api_combo_devices():\n'
        '    return _read_json(SITE_DIR / "data" / "combo_devices.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"combo_devices.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    cb_ref = _load(data_dir / "combo_devices.json", {}) or {}\n'
        '    for sec_key, sec_q in [("combo_regulation", "regulation"), ("injectable_devices", "injectables"), ("inhalation_nasal", "inhalation"), ("transdermal_hfe", "hfe")]:\n'
        '        for item in (cb_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "combo_device",\n'
        '                "group": "Combination Products & Delivery Devices",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/combo-devices?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/combo-devices?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"combination product PMOA 21 CFR Part 4 autoinjector prefilled syringe inhaler pMDI DPI transdermal patch human factors HFE ISO 11608 {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"combo-devices", "#/ref/combo-devices"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    cb_doc = _load_json(data_dir / "combo_devices.json")\n'
        '    if isinstance(cb_doc, dict) and cb_doc.get("combo_regulation"):\n'
        '        cb_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (cb_doc.get("combo_regulation") or []) + (cb_doc.get("injectable_devices") or []))\n'
        '        pages.append(("combo-devices", "#/ref/combo-devices", "Drug-Device Combination Products & Delivery Engineering",\n'
        '                      "Primary-sourced guide to 21 CFR Parts 3 & 4, EU MDR Art. 117, prefilled syringes, autoinjectors, pMDI/DPI inhalers, transdermal patches, and Human Factors Engineering (HFE).",\n'
        '                      f"<ul>{cb_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/combo-devices"' in txt:
        return False
    for anchor in ('    "/#/explore/otc",', '    "/#/explore/rare-pediatric",', '    "/#/explore/rwe",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/combo-devices",\n    "/#/explore/combo-devices",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_combo_devices_py": _write_if_changed(pipe_dir / "build_combo_devices.py", BUILD_COMBO_PY),
        "combo_devices_js": _write_if_changed(js_dir / "combo_devices.js", COMBO_DEVICES_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/otc") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/otc", "OTC & compounding"]] }];\nconst EXPLORE_NAV = [["#/explore/otc", "OTC & compounding"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/otc",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_combo_devices.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_combo_devices.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"combo_regulation": 6, "injectable_devices": 6, "inhalation_nasal": 6, "transdermal_hfe": 6}, out

        doc = json.loads((root / "site" / "data" / "combo_devices.json").read_text(encoding="utf-8"))
        for k in ("combo_regulation", "injectable_devices", "inhalation_nasal", "transdermal_hfe"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61T_COMBINATION_PRODUCTS_DELIVERY_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1t Combination Products & Delivery Engineering patch.")
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
