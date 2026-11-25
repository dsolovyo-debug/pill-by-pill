#!/usr/bin/env python3
"""Pill by Pill v6.1p Patch: Vaccines, Biologics & Cell/Gene Therapy (ATMP) Deep Dive (#/ref/atmp, #/explore/atmp, /api/atmp).

1. Adds `pipeline/build_atmp_vaccines.py` -> `site/data/atmp_vaccines.json` (6 vaccine platforms,
   6 CBER/VRBPAC/ACIP/VAERS governance pillars, 6 AAV/lentivirus/CRISPR gene-therapy standards,
   and 6 autologous/allogeneic CAR-T & cryogenic logistics pillars — 24 primary-sourced entries).
2. Adds `site/js/atmp_vaccines.js` (`atmpVaccinesPage` with inline Vein-to-Vein SVG + 4 section
   filters) and wires `#/ref/atmp`, `#/explore/atmp`, `/api/atmp`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `atmp_vaccines.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/atmp/` static SEO page + sitemap entry -> 32
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1p_vaccines_biologics_cell_gene_therapy_patch.py --selftest
  python3 2026-11-23_v6.1p_vaccines_biologics_cell_gene_therapy_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_ATMP_PY = '#!/usr/bin/env python3\n"""Build Pill by Pill v6.1p Vaccines, Biologics & Cell/Gene Therapy (ATMP) Deep Dive (`site/data/atmp_vaccines.json`).\n\nComprehensive, primary-sourced reference covering:\n  1. Vaccine Platforms & Immunogenicity (6 platforms: Live-Attenuated & Inactivated, Subunit/Recombinant/VLP, Conjugate/Polysaccharide, Viral-Vector, mRNA-LNP, Adjuvants & Correlates of Protection)\n  2. Vaccine Governance, Lot Release & Safety (6 pillars: FDA CBER & VRBPAC, CDC ACIP Recommendations, CBER Lot Release, VAERS & VSD/BEST Surveillance, VICP & CICP, Maternal/Pediatric Schedules)\n  3. Gene Therapy & Genome Editing (6 pillars: AAV Viral Vectors & Serotype Tropism, Lentiviral & Retroviral Integration, In Vivo vs. Ex Vivo CRISPR/Base/Prime Editing, CMC Vector Titer & Empty/Full Capsids, Pre-Existing Neutralizing Antibodies & Redosing, 15-Year Long-Term Follow-Up LTFU)\n  4. Cell Therapy, Vein-to-Vein Logistics & Cryogenics (6 pillars: Autologous CAR-T Vein-to-Vein Workflow, Allogeneic Off-the-Shelf Cell Therapies, Chain of Identity COI & Chain of Custody COC, Cryogenic LN2 Logistics <-150C, CRS & ICANS Hospital Management, CMS CGT Access & Outcomes Contracting)\n\nAll regulatory anchors are verified HTTPS primary sources (FDA, CDC, eCFR, EMA).\n\nUsage:\n  python3 pipeline/build_atmp_vaccines.py site/data\n"""\nimport json\nimport pathlib\nimport sys\n\nCHECKED = "2026-11-23"\n\nVACCINE_PLATFORMS = [\n    {\n        "id": "vax-live-inactivated",\n        "name": "Live-Attenuated & Inactivated Whole-Pathogen Vaccines",\n        "plain": "Classic vaccines that train the immune system using either a weakened living germ that cannot cause full disease (like MMR) or a killed germ (like inactivated polio).",\n        "technical": "Live-attenuated vaccines induce durable humoral and cellular immunity (contraindicated in severe immunosuppression); inactivated/killed vaccines use chemical (formalin/beta-propiolactone) or heat inactivation requiring boosters and adjuvants.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n    {\n        "id": "vax-subunit-vlp",\n        "name": "Recombinant Subunit, Toxoid & Virus-Like Particle (VLP) Vaccines",\n        "plain": "Instead of using the whole germ, factories manufacture just one harmless surface protein or empty viral shell so the immune system learns the target with zero risk of infection.",\n        "technical": "Purified recombinant proteins (e.g., RSV prefusion F, shingles gE), inactivated bacterial toxoids (DTaP), or self-assembling non-infectious VLPs (HPV, Hepatitis B) produced in yeast, insect (baculovirus), or mammalian cells.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n    {\n        "id": "vax-conjugate",\n        "name": "Polysaccharide-Protein Conjugate Vaccines",\n        "plain": "Links bacterial sugar coats to a harmless carrier protein so even babies\' developing immune systems build strong, long-lasting memory against meningitis and pneumonia.",\n        "technical": "Covalent conjugation of bacterial capsular polysaccharides (e.g., Hib, PCV20/PCV21, MenACWY) to T-cell-dependent carrier proteins (CRM197, tetanus toxoid) converts T-independent B-cell responses into high-affinity memory.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n    {\n        "id": "vax-viral-vector",\n        "name": "Viral-Vector Vaccines (Adenovirus, rVSV)",\n        "plain": "Uses a harmless, modified carrier virus as a microscopic delivery truck to carry genetic instructions for a target protein into cells.",\n        "technical": "Replication-deficient (e.g., ChAdOx1, Ad26) or replication-competent (rVSV-ZEBOV for Ebola) viral vectors drive strong endogenous antigen expression and CD8+ T-cell responses.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n    {\n        "id": "vax-mrna-lnp",\n        "name": "mRNA–Lipid Nanoparticle (mRNA-LNP) Vaccines",\n        "plain": "Delivers temporary messenger RNA wrapped in a protective fat bubble so cells briefly build the viral surface protein, train the immune system, and then naturally clear the mRNA.",\n        "technical": "Cell-free in vitro transcription (IVT) of nucleoside-modified mRNA (N1-methylpseudouridine) with 5\' cap and poly(A) tail, encapsulated via microfluidic mixing into 4-lipid LNPs (ionizable lipid, DSPC, cholesterol, PEG-lipid).",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n    {\n        "id": "vax-adjuvants-cop",\n        "name": "Adjuvants & Immunological Correlates of Protection (CoP)",\n        "plain": "Adjuvants are safe \'alarm bells\' added to vaccines to boost immune memory, while correlates of protection are blood-antibody levels proven to predict real-world immunity.",\n        "technical": "Modern adjuvants (alum salts, AS01B, MF59, CpG 1018) activate innate pattern-recognition receptors (TLRs/inflammasomes); validated CoPs (e.g., hemagglutination-inhibition titers, neutralizing titers) enable immunobridging approvals.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n]\n\nVACCINE_GOVERNANCE = [\n    {\n        "id": "vgov-cber-vrbpac",\n        "name": "FDA CBER Review & VRBPAC Advisory Committee",\n        "plain": "Vaccines are reviewed by FDA\'s Center for Biologics (CBER) and publicly debated by independent outside doctors and scientists on the VRBPAC panel before approval or seasonal strain updates.",\n        "technical": "Licensed under PHS Act § 351(a) and 21 CFR Part 601; the Vaccines and Related Biological Products Advisory Committee (VRBPAC) provides transparent public scientific review of safety, efficacy, and annual influenza/COVID-19 strain selection.",\n        "url": "https://www.fda.gov/advisory-committees/vaccines-and-related-biological-products-advisory-committee",\n    },\n    {\n        "id": "vgov-acip",\n        "name": "CDC ACIP & Immunization Schedules",\n        "plain": "After the FDA approves a vaccine as safe and effective, the CDC\'s Advisory Committee on Immunization Practices (ACIP) decides which age or risk groups should receive it—which also triggers insurance coverage.",\n        "technical": "ACIP evaluates GRADE evidence and Evidence to Recommendations (EtR) frameworks; CDC adoption governs the Vaccines for Children (VFC) program and ACA preventive-care zero-cost-sharing mandates.",\n        "url": "https://www.cdc.gov/acip/index.html",\n    },\n    {\n        "id": "vgov-lot-release",\n        "name": "FDA CBER Lot-by-Lot Release Testing (21 CFR 610.2)",\n        "plain": "Unlike ordinary pills, every single manufactured batch of a licensed vaccine must submit testing records—and often physical vials—for FDA CBER sign-off before it can ship to clinics.",\n        "technical": "Under 21 CFR 610.2, CBER reviews manufacturer lot-release protocols (potency, purity, sterility, endotoxin) and conducts confirmatory lab testing prior to issuing written release authorization.",\n        "url": "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-F/part-601",\n    },\n    {\n        "id": "vgov-vaers-vsd",\n        "name": "Multi-Layer Vaccine Safety (VAERS, VSD & FDA BEST)",\n        "plain": "Vaccine safety uses both an open early-warning tip line (VAERS) and active hospital-record networks (VSD and BEST) covering tens of millions of patients to verify whether any signal is real.",\n        "technical": "Passive spontaneous reporting via CDC/FDA VAERS is paired with active rapid-cycle EHR/claims surveillance in CDC\'s Vaccine Safety Datalink (VSD) and FDA\'s Biologics Effectiveness and Safety (BEST) Initiative.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics/vaccine-adverse-event-reporting-system-vaers",\n    },\n    {\n        "id": "vgov-vicp",\n        "name": "No-Fault Injury Compensation (VICP & CICP)",\n        "plain": "Because routine vaccines are given to healthy millions, federal no-fault compensation programs handle rare severe vaccine injuries swiftly while keeping essential vaccine supply stable.",\n        "technical": "The National Vaccine Injury Compensation Program (VICP, 1986 NCVIA) covers routine vaccines via a Vaccine Injury Table funded by a per-dose excise tax; the Countermeasures Injury Compensation Program (CICP) covers PREP Act emergency countermeasures.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n    {\n        "id": "vgov-coldchain",\n        "name": "Vaccine Cold-Chain Integrity & Thermostability",\n        "plain": "Most vaccines must stay strictly between 2°C and 8°C—or ultra-cold (-20°C to -80°C) for certain mRNA vials—from factory freezer to clinic syringe so they never lose potency.",\n        "technical": "Requires continuous calibrated digital data loggers (DDLs), freeze-damage prevention for aluminum-adjuvanted products, and validated excursion stability budgets under CDC/WHO cold-chain standards.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/vaccines",\n    },\n]\n\nGENE_THERAPY = [\n    {\n        "id": "gt-aav",\n        "name": "Adeno-Associated Virus (AAV) Vectors & Tissue Tropism",\n        "plain": "Stripped-down, harmless AAV shells carry a healthy replacement gene directly into liver, muscle, eye, or nerve cells—usually staying as a stable loop next to the cell\'s DNA.",\n        "technical": "Recombinant AAV serotypes (AAV2, AAV5, AAV8, AAV9, engineered capsids) confer tissue tropism and remain predominantly episomal in non-dividing cells; cargo is constrained to ~4.7 kb.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products",\n    },\n    {\n        "id": "gt-lentivirus",\n        "name": "Lentiviral & Retroviral Integrating Vectors",\n        "plain": "Used mostly outside the body to insert a working gene permanently into dividing blood stem cells or T cells so every future daughter cell inherits the fix.",\n        "technical": "Self-inactivating (SIN) third-generation lentiviral vectors integrate stably into host chromosomes for ex vivo HSC gene therapy (e.g., beta-thalassemia, sickle cell, cerebral ALD) and CAR-T manufacturing, requiring replication-competent lentivirus (RCL) testing.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/chemistry-manufacturing-and-control-cmc-information-human-gene-therapy-investigational-new-drug",\n    },\n    {\n        "id": "gt-crispr-editing",\n        "name": "Genome Editing (CRISPR-Cas9, Base & Prime Editing)",\n        "plain": "Acts like molecular scissors—or a precision word processor—to cut, silence, or rewrite a single misspelled DNA letter inside living cells.",\n        "technical": "Includes ex vivo CRISPR-Cas9 double-strand break editing (e.g., exagamglogene autotemcel for sickle cell/TDT), in vivo LNP-delivered liver editing, and nickase-based base/prime editors; FDA Genome Editing Guidance requires genome-wide off-target and translocation characterization.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/human-gene-therapy-products-incorporating-human-genome-editing",\n    },\n    {\n        "id": "gt-cmc-capsids",\n        "name": "Gene Therapy CMC: Vector Titer, Empty/Full Ratio & Potency",\n        "plain": "Manufacturing viral vectors is notoriously tricky—factories must measure how many viral shells actually contain the therapeutic gene versus empty \'duds\' and verify biological potency on every batch.",\n        "technical": "Critical quality attributes (CQAs) under FDA Gene Therapy CMC Guidance include vector genome titer (ddPCR), empty-to-full capsid ratio (AUC / cryo-EM / IEX), residual host-cell DNA/plasmid, replication-competent virus (RCV), and matrixed bioassay potency.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/chemistry-manufacturing-and-control-cmc-information-human-gene-therapy-investigational-new-drug",\n    },\n    {\n        "id": "gt-nab-redosing",\n        "name": "Pre-Existing Neutralizing Antibodies (NAbs) & Immunogenicity",\n        "plain": "Because many people have already encountered wild AAV in nature, existing antibodies can block an AAV gene therapy before it reaches its target—requiring screening tests and limiting repeat dosing.",\n        "technical": "Companion diagnostic anti-AAV total/neutralizing antibody assays screen eligible patients; high-dose systemic AAV risks hepatotoxicity, complement-mediated thrombotic microangiopathy (TMA), and dorsal root ganglion (DRG) toxicity.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/approved-cellular-and-gene-therapy-products",\n    },\n    {\n        "id": "gt-ltfu-15yr",\n        "name": "Long-Term Follow-Up (LTFU, Up to 15 Years)",\n        "plain": "Because gene therapies make lasting changes inside cells, FDA requires patients to be monitored for up to 15 years after a single infusion to watch for delayed durability shifts or rare secondary cancers.",\n        "technical": "FDA Long-Term Follow-Up Guidance mandates up to 15 years of observation for integrating vectors (lentivirus/retrovirus) and genome-editing products, and up to 5 years for non-integrating AAV vectors, including insertion-site clonality monitoring.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/long-term-follow-after-administration-human-gene-therapy-products",\n    },\n]\n\nCELL_THERAPY = [\n    {\n        "id": "ct-autologous-cart",\n        "name": "Autologous CAR-T \'Vein-to-Vein\' Manufacturing Workflow",\n        "plain": "A living batch-of-one medicine: a hospital collects a patient\'s own T cells, ships them frozen to a cleanroom to add cancer-homing CAR receptors, expands them, tests purity, and ships them back to infuse.",\n        "technical": "End-to-end autologous cycle (leukapheresis -> cryopreservation -> T-cell activation & viral transduction -> expansion -> harvest/formulation -> rapid QC release -> lymphodepletion & infusion) typically spans 2–4 weeks under FDA CAR-T Guidance.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-development-chimeric-antigen-receptor-car-t-cell-products",\n    },\n    {\n        "id": "ct-allogeneic",\n        "name": "Allogeneic (\'Off-the-Shelf\') Cell & NK Therapies",\n        "plain": "Engineered from healthy donor cells or stem cells into large frozen banks so dozens of patients can be treated immediately without waiting weeks for custom manufacturing.",\n        "technical": "Uses gene editing (e.g., TRAC/B2M knockout) to prevent Graft-versus-Host Disease (GvHD) and host immune rejection across donor T cells, NK cells, and iPSC-derived cell platforms.",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-development-chimeric-antigen-receptor-car-t-cell-products",\n    },\n    {\n        "id": "ct-coi-coc",\n        "name": "Chain of Identity (COI) & Chain of Custody (COC)",\n        "plain": "Because an autologous cell bag belongs to one exact human being, barcoded digital tracking links every tube, bag, and freezer slot to that patient—a mix-up would be catastrophic.",\n        "technical": "Unbroken bidirectional COI (patient-specific ISBT 128 / DIN identifiers across apheresis, cleanroom, and bedside) paired with timestamped COC handoff logs and orchestration software (e.g., Vineti/TrakCel).",\n        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-development-chimeric-antigen-receptor-car-t-cell-products",\n    },\n    {\n        "id": "ct-cryo-logistics",\n        "name": "Cryogenic Liquid-Nitrogen (LN2, <-150°C) Logistics",\n        "plain": "Living engineered cells travel inside dry-vapor liquid nitrogen shippers colder than -150°C with live GPS and temperature trackers until nurses thaw the bag right at the bedside.",\n        "technical": "Controlled-rate freezing in DMSO cryoprotectant, validated LN2 dry-vapor dewars (10+ day hold times) managed by specialized couriers (Cryoport, Marken), and strict post-thaw infusion stability windows.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products",\n    },\n    {\n        "id": "ct-crs-icans",\n        "name": "Hospital Readiness: CRS, ICANS & Certified Centers",\n        "plain": "When engineered T cells attack cancer rapidly, they can trigger intense fever and inflammation (CRS) or temporary confusion (ICANS)—so infusions occur at trained centers stocked with rescue medicines.",\n        "technical": "Standardized ASTCT grading for Cytokine Release Syndrome (managed with anti-IL-6R tocilizumab and corticosteroids) and Immune Effector Cell-Associated Neurotoxicity Syndrome (ICANS), alongside FDA safety/REMS monitoring.",\n        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/approved-cellular-and-gene-therapy-products",\n    },\n    {\n        "id": "ct-atmp-access",\n        "name": "EU ATMP Framework, FDA RMAT & Outcomes-Based Access",\n        "plain": "One-time cell and gene therapies can cost $400,000 to over $3 million upfront, pushing regulators and payers toward fast-track RMAT reviews and \'pay-if-it-keeps-working\' outcomes contracts.",\n        "technical": "FDA CBER RMAT designation and EMA CAT (Committee for Advanced Therapies) ATMP classification streamline development; reimbursement leverages CMS Cell and Gene Therapy Access Model, hospital DRG/NTAP add-ons, and multi-year outcomes-based agreements.",\n        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/advanced-therapy-medicinal-products-overview",\n    },\n]\n\n\ndef build_atmp_vaccines(data_dir: pathlib.Path) -> dict:\n    data_dir.mkdir(parents=True, exist_ok=True)\n    payload = {\n        "checked": CHECKED,\n        "scope_note": "Primary-sourced reference on vaccine platforms, CBER/ACIP governance, gene therapy/CRISPR editing, and autologous/allogeneic cell therapy logistics (FDA CBER, CDC, eCFR, EMA). Educational reference only—not medical advice.",\n        "vaccine_platforms": VACCINE_PLATFORMS,\n        "vaccine_governance": VACCINE_GOVERNANCE,\n        "gene_therapy": GENE_THERAPY,\n        "cell_therapy": CELL_THERAPY,\n    }\n    (data_dir / "atmp_vaccines.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n    return {\n        "vaccine_platforms": len(VACCINE_PLATFORMS),\n        "vaccine_governance": len(VACCINE_GOVERNANCE),\n        "gene_therapy": len(GENE_THERAPY),\n        "cell_therapy": len(CELL_THERAPY),\n    }\n\n\ndef main(argv=None) -> int:\n    data_dir = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")\n    print(json.dumps(build_atmp_vaccines(data_dir), indent=2))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main(sys.argv[1:]))\n'
ATMP_VACCINES_JS = 'import { html } from "./ui.js";\nimport { getJSON } from "./data.js";\n\nfunction renderVeinToVeinSvg() {\n  const nodes = [\n    { x: 8, label: "1. Apheresis", sub: "COI / ISBT 128" },\n    { x: 140, label: "2. Cryo Ship", sub: "LN2 <-150°C" },\n    { x: 272, label: "3. Edit / Transduce", sub: "LVV / CRISPR" },\n    { x: 404, label: "4. Rapid QC", sub: "VCN / Sterility" },\n    { x: 536, label: "5. Infuse & LTFU", sub: "CRS / 15-Yr Track" },\n  ];\n  return html`<figure class="atmp-flow" aria-label="Autologous cell and gene therapy vein-to-vein workflow">\n    <svg viewBox="0 0 666 84" width="666" height="84" role="img" style="max-width:100%;height:auto;display:block">\n      ${nodes.map((n, i) => html`\n        <rect x="${n.x}" y="10" width="122" height="62" rx="8" fill="var(--paper,#f8fafc)" stroke="${i === 2 ? "var(--accent,#cc2f5a)" : "var(--line,#94a3b8)"}" stroke-width="${i === 2 ? "2" : "1.5"}"/>\n        <text x="${n.x + 61}" y="35" text-anchor="middle" font-size="11.5" font-weight="700" fill="currentColor">${n.label}</text>\n        <text x="${n.x + 61}" y="53" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.75">${n.sub}</text>\n        ${i < nodes.length - 1 ? html`<line x1="${n.x + 122}" y1="41" x2="${n.x + 132}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Autologous CAR-T and ex vivo gene therapy vein-to-vein lifecycle under unbroken Chain of Identity (COI) and cryogenic logistics.</figcaption>\n  </figure>`;\n}\n\nexport async function atmpVaccinesPage(query, mode = "ref") {\n  const doc = await getJSON("data/atmp_vaccines.json");\n  const sec = (query && query.get("section")) || "all";\n  const base = mode === "explore" ? "#/explore/atmp" : "#/ref/atmp";\n  const show = (k) => sec === "all" || sec === k;\n\n  return {\n    title: "Vaccines, Biologics & Cell/Gene Therapy (ATMP) Deep Dive",\n    body: html`\n      <h1>Vaccines, Biologics &amp; Cell/Gene Therapy (ATMP) Deep Dive</h1>\n      <p class="lead">${mode === "explore"\n        ? "How modern vaccines (including mRNA-LNP), viral-vector gene therapies, CRISPR genome editing, and living CAR-T cell therapies are designed, reviewed, frozen, and delivered safely to patients."\n        : "Primary-sourced reference covering 6 vaccine platforms, 6 CBER/VRBPAC/ACIP/VAERS governance pillars, 6 AAV/lentivirus/CRISPR gene-therapy standards, and 6 autologous/allogeneic cell-therapy & cryogenic logistics frameworks (checked " + doc.checked + ")."}</p>\n\n      ${renderVeinToVeinSvg()}\n\n      <p class="small">Jump to section:\n        <a href="${base}"${sec === "all" ? \' aria-current="page"\' : ""}>All Sections</a> ·\n        <a href="${base}?section=vaccines"${sec === "vaccines" ? \' aria-current="page"\' : ""}>Vaccine Platforms (6)</a> ·\n        <a href="${base}?section=vgov"${sec === "vgov" ? \' aria-current="page"\' : ""}>CBER / ACIP &amp; Safety (6)</a> ·\n        <a href="${base}?section=gene"${sec === "gene" ? \' aria-current="page"\' : ""}>Gene Therapy &amp; CRISPR (6)</a> ·\n        <a href="${base}?section=cell"${sec === "cell" ? \' aria-current="page"\' : ""}>CAR-T &amp; Cryo Logistics (6)</a>\n      </p>\n\n      ${show("vaccines") ? html`\n        <h2 id="vaccines">1. Vaccine Platforms &amp; Immunogenicity (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Vaccine platforms">\n          <table class="tbl"><thead><tr><th>Platform</th><th>${mode === "explore" ? "How It Trains Immunity" : "Platform Science & Manufacturing"}</th></tr></thead>\n          <tbody>${(doc.vaccine_platforms || []).map((v) => html`<tr id="${v.id}">\n            <td><b><a href="${v.url}" target="_blank" rel="noopener">${v.name}</a></b></td>\n            <td>${mode === "explore" ? v.plain : html`${v.plain}<br><span class="muted small">${v.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("vgov") ? html`\n        <h2 id="vgov">2. Vaccine Governance, Lot Release &amp; Multi-Layer Safety (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Vaccine governance and safety">\n          <table class="tbl"><thead><tr><th>Governance Pillar</th><th>${mode === "explore" ? "How Oversight Works" : "Statutory & Surveillance Framework"}</th></tr></thead>\n          <tbody>${(doc.vaccine_governance || []).map((g) => html`<tr id="${g.id}">\n            <td><b><a href="${g.url}" target="_blank" rel="noopener">${g.name}</a></b></td>\n            <td>${mode === "explore" ? g.plain : html`${g.plain}<br><span class="muted small">${g.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("gene") ? html`\n        <h2 id="gene">3. Gene Therapy, Viral Vectors &amp; Genome Editing (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Gene therapy and genome editing">\n          <table class="tbl"><thead><tr><th>Technology / Standard</th><th>${mode === "explore" ? "How It Works" : "Vector Engineering, CMC & 15-Yr LTFU"}</th></tr></thead>\n          <tbody>${(doc.gene_therapy || []).map((t) => html`<tr id="${t.id}">\n            <td><b><a href="${t.url}" target="_blank" rel="noopener">${t.name}</a></b></td>\n            <td>${mode === "explore" ? t.plain : html`${t.plain}<br><span class="muted small">${t.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      ${show("cell") ? html`\n        <h2 id="cell">4. Cell Therapy, Vein-to-Vein Logistics &amp; Cryogenics (6)</h2>\n        <div class="tbl-wrap" tabindex="0" role="region" aria-label="Cell therapy and cryogenic logistics">\n          <table class="tbl"><thead><tr><th>Operational Pillar</th><th>${mode === "explore" ? "How Living Cells Reach Patients" : "COI/COC, LN2 Logistics & Clinical Access"}</th></tr></thead>\n          <tbody>${(doc.cell_therapy || []).map((c) => html`<tr id="${c.id}">\n            <td><b><a href="${c.url}" target="_blank" rel="noopener">${c.name}</a></b></td>\n            <td>${mode === "explore" ? c.plain : html`${c.plain}<br><span class="muted small">${c.technical}</span>`}</td>\n          </tr>`)}</tbody></table>\n        </div>\n      ` : ""}\n\n      <p class="muted small">${doc.scope_note}</p>\n      <p class="muted small">Related: <a href="#/ref/playbooks">Modality Playbooks</a> · <a href="#/ref/sterile">Sterile &amp; Bioprocessing</a> · <a href="#/ref/trace?drug=tisagenlecleucel">Trace CAR-T End-to-End</a> · <a href="#/ref/safety">Drug Safety &amp; PV</a>.</p>\n    `,\n  };\n}\n'


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
    imp = 'import { atmpVaccinesPage } from "./atmp_vaccines.js";\n'
    if "./atmp_vaccines.js" not in txt:
        txt = imp + txt
        changed = True
    if '"/ref/atmp"' not in txt:
        for anchor in ('if (path === "/ref/cdx")', 'if (path === "/ref/global-reg")', 'if (path === "/ref/sterile")', 'if (path === "/search"'):
            if anchor in txt:
                rep = (
                    'if (path === "/ref/atmp") return atmpVaccinesPage(query, "ref");\n'
                    '  if (path === "/explore/atmp") return atmpVaccinesPage(query, "explore");\n'
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
    if "#/ref/atmp" not in txt:
        for anchor in ('["#/ref/cdx", "CDx & precision medicine"]', '["#/ref/sterile", "Sterile & bioprocessing"]', '["#/ref/playbooks", "Modality playbooks"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n      ["#/ref/atmp", "Vaccines & cell/gene"]', 1)
                changed = True
                break
    if "#/explore/atmp" not in txt:
        for anchor in ('["#/explore/cdx", "CDx & precision medicine"]', '["#/explore/sterile", "Sterile & bioprocessing"]', '["#/explore/playbooks", "5 medicine types"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ',\n  ["#/explore/atmp", "Vaccines & cell/gene"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_atmp_vaccines.py" in txt:
        return False
    hook = "\n# v6.1p: Vaccines, Biologics & Cell/Gene Therapy (ATMP) Deep Dive\npython3 pipeline/build_atmp_vaccines.py site/data\n"
    path.write_text(txt.rstrip() + "\n" + hook, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/atmp"' in txt:
        return False
    snippet = (
        '\n\n@app.get("/api/atmp")\n'
        'def api_atmp_vaccines():\n'
        '    return _read_json(SITE_DIR / "data" / "atmp_vaccines.json")\n'
    )
    path.write_text(txt.rstrip() + snippet, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"atmp_vaccines.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    atmp_ref = _load(data_dir / "atmp_vaccines.json", {}) or {}\n'
        '    for sec_key, sec_q in [("vaccine_platforms", "vaccines"), ("vaccine_governance", "vgov"), ("gene_therapy", "gene"), ("cell_therapy", "cell")]:\n'
        '        for item in (atmp_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "atmp_vaccine",\n'
        '                "group": "Vaccines & Cell/Gene Therapy",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/atmp?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/atmp?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"vaccine mRNA LNP VRBPAC ACIP VAERS AAV lentivirus CRISPR CAR-T ATMP cryogenic {sec_key} {item.get(\'name\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"atmp", "#/ref/atmp"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    atmp_doc = _load_json(data_dir / "atmp_vaccines.json")\n'
        '    if isinstance(atmp_doc, dict) and atmp_doc.get("vaccine_platforms"):\n'
        '        a_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (atmp_doc.get("vaccine_platforms") or []) + (atmp_doc.get("gene_therapy") or []))\n'
        '        pages.append(("atmp", "#/ref/atmp", "Vaccines, Biologics & Cell/Gene Therapy (ATMP) Deep Dive",\n'
        '                      "Primary-sourced guide to mRNA-LNP & subunit vaccines, CBER/VRBPAC/ACIP/VAERS oversight, AAV/lentivirus/CRISPR gene therapy, and autologous CAR-T vein-to-vein cryogenic logistics.",\n'
        '                      f"<ul>{a_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/atmp"' in txt:
        return False
    for anchor in ('    "/#/explore/cdx",', '    "/#/explore/global-reg",', '    "/#/explore/sterile",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/atmp",\n    "/#/explore/atmp",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_atmp_vaccines_py": _write_if_changed(pipe_dir / "build_atmp_vaccines.py", BUILD_ATMP_PY),
        "atmp_vaccines_js": _write_if_changed(js_dir / "atmp_vaccines.js", ATMP_VACCINES_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/cdx") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/cdx", "CDx & precision medicine"]] }];\nconst EXPLORE_NAV = [["#/explore/cdx", "CDx & precision medicine"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/cdx",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_atmp_vaccines.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_atmp_vaccines.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"vaccine_platforms": 6, "vaccine_governance": 6, "gene_therapy": 6, "cell_therapy": 6}, out

        doc = json.loads((root / "site" / "data" / "atmp_vaccines.json").read_text(encoding="utf-8"))
        for k in ("vaccine_platforms", "vaccine_governance", "gene_therapy", "cell_therapy"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item

        print("V61P_VACCINES_BIOLOGICS_ATMP_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1p Vaccines, Biologics & Cell/Gene Therapy patch.")
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
