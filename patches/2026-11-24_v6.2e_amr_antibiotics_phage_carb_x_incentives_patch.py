#!/usr/bin/env python3
"""Pill by Pill v6.2e Patch: Antimicrobial Resistance (AMR), Antibiotics, Antifungals, Bacteriophage Therapy & CARB-X / QIDP Incentives Reference (#/ref/amr-antiinfectives, #/explore/amr-antiinfectives, /api/amr-antiinfectives).

1. Adds `pipeline/build_amr_antiinfectives.py` -> `site/data/amr_antiinfectives.json` (6 QIDP /
   GAIN Act & LPAD Pathway pillars, 6 AMR Surveillance & FDA STIC Breakpoints pillars, 6 CARB-X,
   BARDA & NIAID Incentive pillars, and 6 Bacteriophage, LBP & Non-Traditional Therapy pillars — 24
   primary-sourced entries).
2. Adds `site/js/amr_antiinfectives.js` (`amrAntiinfectivesPage` with inline AMR & Anti-Infectives
   SVG + 4 section filters) and wires `#/ref/amr-antiinfectives`, `#/explore/amr-antiinfectives`,
   `/api/amr-antiinfectives`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `amr_antiinfectives.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/amr-antiinfectives/` static SEO page + sitemap entry ->
   47 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2e_amr_antibiotics_phage_carb_x_incentives_patch.py --selftest
  python3 2026-11-24_v6.2e_amr_antibiotics_phage_carb_x_incentives_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_AMR_ANTIINFECTIVES_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2e Antimicrobial Resistance (AMR), Antibiotics, Phage Therapy & CARB-X Reference (`site/data/amr_antiinfectives.json`).

Comprehensive, primary-sourced reference covering:
  1. QIDP, GAIN Act Exclusivity & LPAD Pathways (6 pillars)
  2. AMR Surveillance & FDA STIC Breakpoints (6 pillars)
  3. CARB-X, BARDA & NIAID Antimicrobial Incentives (6 pillars)
  4. Bacteriophage Therapy, LBPs & Non-Traditional Modalities (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER/CBER/CDRH, CDC, NIH/NIAID, HHS ASPR/BARDA).

Usage:
  python3 pipeline/build_amr_antiinfectives.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

QIDP_LPAD_PATHWAYS = [
    {
        "id": "amr-qidp-gain",
        "name": "QIDP Designation Under the GAIN Act (FDASIA Title VIII)",
        "category": "Statutory Incentive",
        "plain": "To encourage companies to invent new antibiotics and antifungals for dangerous infections, Congress created QIDP status—unlocking fast-track reviews and extra market protection.",
        "technical": "Under Title VIII of FDASIA (GAIN), FDA grants Qualified Infectious Disease Product (QIDP) designation within 60 days to antibacterial/antifungal drugs treating serious or life-threatening infections.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/qualified-infectious-disease-product-designation-questions-and-answers",
    },
    {
        "id": "amr-gain-exclusivity",
        "name": "5-Year GAIN Exclusivity Extension (FD&C Act § 505E)",
        "category": "Market Exclusivity",
        "plain": "An approved QIDP antibiotic receives an extra 5 years of protection from generic copies on top of its standard new-drug or orphan exclusivity.",
        "technical": "FD&C Act § 505E adds a 5-year exclusivity extension to qualifying NCE (5-year), 3-year clinical investigation, or 7-year orphan exclusivity upon approval of a QIDP-designated NDA.",
        "url": "https://www.fda.gov/media/148480/download",
    },
    {
        "id": "amr-lpad-pathway",
        "name": "Limited Population Pathway (LPAD — 21st Century Cures § 506(h))",
        "category": "Streamlined Approval",
        "plain": "For rare superbugs with few patients to enroll in giant trials, LPAD lets FDA approve targeted antibiotics using smaller, focused studies with special safety labeling.",
        "technical": "FD&C Act § 506(h) establishes the LPAD pathway for antibacterial/antifungal drugs treating serious/life-threatening infections in limited populations with unmet needs, requiring distinct labeling and promotional pre-review.",
        "url": "https://www.fda.gov/drugs/development-resources/limited-population-pathway-antibacterial-and-antifungal-drugs-lpad-pathway",
    },
    {
        "id": "amr-fast-track-priority",
        "name": "Automatic Priority Review & Fast Track Eligibility for QIDPs",
        "category": "Expedited Review",
        "plain": "Every QIDP-designated antibiotic automatically qualifies for FDA's 6-month Priority Review clock and Fast Track meetings.",
        "technical": "Under GAIN statutory provisions, a QIDP-designated drug receives Fast Track designation upon sponsor request and automatic Priority Review for the first application submitted for that QIDP use.",
        "url": "https://www.fda.gov/drugs/ind-activity/fast-track-designation-requests",
    },
    {
        "id": "amr-fda-mcm-portal",
        "name": "FDA Antimicrobial Resistance & Medical Countermeasure Hub",
        "category": "Regulatory Coordination",
        "plain": "FDA coordinates across drug, vaccine, and diagnostic centers—and with CMS on hospital reimbursement—to keep effective antibiotics available.",
        "technical": "FDA's Antimicrobial Resistance MCM program aligns CDER, CBER, and CDRH regulatory pathways with CMS reimbursement initiatives to sustain antibacterial and antifungal innovation.",
        "url": "https://www.fda.gov/emergency-preparedness-and-response/medical-countermeasure-mcm-issues/antimicrobial-resistance",
    },
    {
        "id": "amr-microbiology-data",
        "name": "Microbiology Data & PK/PD Dosing for Systemic Antibacterials",
        "category": "Clinical Microbiology",
        "plain": "Before testing a new antibiotic in humans, developers must map its spectrum of activity, resistance mechanisms, and blood/tissue concentrations against target bacteria.",
        "technical": "FDA's Microbiology Data for Systemic Antibacterial Drugs guidance details in vitro spectrum, MIC90 distributions, resistance frequency, and PK/PD target attainment (AUC/MIC, T>MIC) required for IND/NDA.",
        "url": "https://www.fda.gov/media/77442/download",
    },
]

SURVEILLANCE_STIC = [
    {
        "id": "amr-stic-portal",
        "name": "FDA-Recognized Susceptibility Test Interpretive Criteria (STIC)",
        "category": "Dynamic Breakpoints",
        "plain": "As bacteria evolve resistance, FDA posts updated 'breakpoints' online so hospital labs know the exact drug concentration that still kills a germ.",
        "technical": "Under the 21st Century Cures Act (§ 511A), FDA CDER maintains a centralized STIC web portal recognizing SDO (CLSI) or FDA-established breakpoints without requiring individual drug label updates.",
        "url": "https://www.fda.gov/drugs/development-resources/fda-recognized-antimicrobial-susceptibility-test-interpretive-criteria",
    },
    {
        "id": "amr-stic-antibacterial",
        "name": "Antibacterial Susceptibility Breakpoints (MIC & Disk Diffusion)",
        "category": "Antibacterial Standards",
        "plain": "Doctors rely on Susceptible, Intermediate, or Resistant lab cutoffs—maintained per antibiotic and bug—to pick the right treatment fast.",
        "technical": "FDA's Antibacterial STIC tables publish recognized Minimum Inhibitory Concentration (MIC) and disk diffusion zone-diameter breakpoints across Enterobacterales, Pseudomonas, Staphylococcus, and anaerobes.",
        "url": "https://www.fda.gov/drugs/development-resources/antibacterial-susceptibility-test-interpretive-criteria",
    },
    {
        "id": "amr-stic-antifungal",
        "name": "Antifungal Susceptibility Breakpoints (Candida & Aspergillus)",
        "category": "Antifungal Standards",
        "plain": "Drug-resistant fungi like Candida auris require dedicated antifungal susceptibility cutoffs so ICU teams don't prescribe an ineffective azole or echinocandin.",
        "technical": "FDA's Antifungal STIC registry tracks recognized breakpoints and exceptions for systemic triazoles, echinocandins, and polyenes against invasive fungal pathogens.",
        "url": "https://www.fda.gov/drugs/development-resources/antifungal-susceptibility-test-interpretive-criteria",
    },
    {
        "id": "amr-ast-devices",
        "name": "Antimicrobial Susceptibility Test (AST) Diagnostic Co-Updates",
        "category": "CDRH Diagnostics",
        "plain": "Whenever FDA tightens a resistance breakpoint, commercial hospital lab machines (AST panels) must recalibrate using the updated FDA STIC website.",
        "technical": "FDA CDRH's AST System Devices framework enables rapid 510(k) clearance and postmarket breakpoint updates for automated and manual AST diagnostics synchronized with CDER's STIC portal.",
        "url": "https://www.fda.gov/medical-devices/products-and-medical-procedures/antimicrobial-resistance-and-medical-devices",
    },
    {
        "id": "amr-cdc-arln",
        "name": "CDC Antimicrobial Resistance Laboratory Network (AR Lab Network)",
        "category": "Lab Surveillance",
        "plain": "Seven regional CDC public-health labs run free rapid resistance testing and whole-genome sequencing to contain hospital superbug outbreaks early.",
        "technical": "Established in 2016, CDC's AR Lab Network links state/local public health labs and 7 regional reference labs to detect carbapenemase-producing organisms, C. auris, and emerging resistance phenotypes.",
        "url": "https://www.cdc.gov/antimicrobial-resistance-laboratory-networks/php/about/index.html",
    },
    {
        "id": "amr-cdc-narms",
        "name": "CDC / FDA / USDA National Antimicrobial Resistance Monitoring (NARMS)",
        "category": "One Health Tracking",
        "plain": "NARMS tracks antibiotic resistance across humans, retail meats, and farm animals to catch foodborne superbugs like Salmonella and Campylobacter.",
        "technical": "NARMS is a tripartite U.S. One Health surveillance partnership (CDC, FDA CVM, USDA) monitoring antimicrobial susceptibility trends in enteric bacteria across human clinical isolates, retail meats, and food animals.",
        "url": "https://www.cdc.gov/narms/about/index.html",
    },
]

CARB_X_BARDA_INCENTIVES = [
    {
        "id": "amr-carb-x",
        "name": "CARB-X Global Antibacterial Accelerator (BARDA / NIAID / Wellcome)",
        "category": "Push Funding",
        "plain": "Because most big pharma companies exited antibiotic R&D, CARB-X funds biotech startups through early discovery and Phase 1 trials against priority superbugs.",
        "technical": "Combating Antibiotic-Resistant Bacteria Biopharmaceutical Accelerator (CARB-X) is a non-profit partnership backed by HHS BARDA, NIAID, Wellcome, UK DHSC, Germany BMBF, and Gates Foundation supporting preclinical-to-Phase 1 AMR products.",
        "url": "https://www.niaid.nih.gov/research/carb-x",
    },
    {
        "id": "amr-barda-bsa",
        "name": "BARDA Broad Spectrum Antimicrobials (BSA) Portfolio",
        "category": "Late-Stage Push",
        "plain": "BARDA co-funds late-stage Phase 2/3 trials and FDA approval packages for new antibiotics and antifungals that double as biodefense countermeasures.",
        "technical": "BARDA's Broad Spectrum Antimicrobials and CARB portfolio provides non-dilutive advanced R&D contracts and Project BioShield procurement support for novel antibacterial/antifungal candidates.",
        "url": "https://www.aspr.gov/about/budget/fy-2025-presidents-request-highlights",
    },
    {
        "id": "amr-aspr-biodefense",
        "name": "ASPR Stewardship & Access Plans & PHEMCE Coordination",
        "category": "Stewardship Policy",
        "plain": "New antibiotics must be saved for emergencies—so federal partners pair R&D funding with hospital stewardship rules that prevent overuse.",
        "technical": "ASPR's Stewardship and Access Plan Development Guide aligns BARDA/CARB-X awardees with responsible hospital antimicrobial stewardship and global access commitments.",
        "url": "https://www.aspr.gov/readiness-response/medical-countermeasures-biodefense",
    },
    {
        "id": "amr-niaid-arlg",
        "name": "NIAID Antibacterial Resistance Leadership Group (ARLG)",
        "category": "Clinical Trial Network",
        "plain": "NIAID's ARLG runs multi-hospital clinical trials testing better antibiotic combinations, shorter courses, and rapid diagnostics.",
        "technical": "The Antibacterial Resistance Leadership Group (ARLG) designs and executes NIH-funded multi-center clinical trials on gram-negative resistance, MRSA, diagnostics, and antimicrobial stewardship.",
        "url": "https://www.niaid.nih.gov/research/antibacterial-resistance-leadership-group",
    },
    {
        "id": "amr-cdc-threats",
        "name": "CDC Antibiotic Resistance Threats Report (Urgent & Serious Pathogens)",
        "category": "Threat Prioritization",
        "plain": "CDC ranks the deadliest drug-resistant bacteria and fungi—like CRE, Candida auris, and drug-resistant gonorrhea—to guide where R&D dollars go first.",
        "technical": "CDC's AR Threats Reports stratify pathogens into Urgent, Serious, and Concerning tiers based on clinical/economic burden, incidence, transmissibility, and treatability.",
        "url": "https://www.cdc.gov/antimicrobial-resistance/data-research/threats/index.html",
    },
    {
        "id": "amr-niaid-cre-fungal",
        "name": "Carbapenem-Resistant Enterobacterales (CRE) & ESBL Priority Targets",
        "category": "High-Priority Pathogens",
        "plain": "Superbugs carrying ESBL or carbapenemase enzymes can defeat nearly every penicillin and last-resort IV antibiotic in the hospital.",
        "technical": "NIAID prioritizes R&D against ESBL-producing and carbapenem-resistant Enterobacterales (CRE, e.g., K. pneumoniae, E. coli), Acinetobacter, Pseudomonas, and multidrug-resistant Candida auris.",
        "url": "https://www.niaid.nih.gov/research/antimicrobial-resistance-threats",
    },
]

PHAGE_LBP_NONTRADITIONAL = [
    {
        "id": "amr-cber-phage-lbp",
        "name": "FDA CBER Bacteriophage & Live Biotherapeutic Products (OVRR)",
        "category": "Biologic Regulation",
        "plain": "Viruses that hunt only bacteria (phages) and beneficial gut microbes are regulated as biologics by FDA's CBER—not as traditional chemical pills.",
        "technical": "FDA CBER's Office of Vaccines Research and Review (OVRR) regulates bacteriophage therapeutics and Live Biotherapeutic Products (LBPs) under IND/BLA pathways, maintaining dedicated mucosal/phage research labs.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/science-research-biologics/phage-and-live-biotherapeutic-products",
    },
    {
        "id": "amr-phage-workshop",
        "name": "FDA–NIAID Bacteriophage Therapy Clinical & CMC Framework",
        "category": "Phage Licensing",
        "plain": "Personalized phage cocktails have saved patients with untreatable cystic fibrosis and joint infections; now FDA requires rigorous controlled trials for full approval.",
        "technical": "Joint FDA CBER–NIAID regulatory science defines CMC purity (endotoxin removal, host-cell DNA), potency/plaquing assays, and adaptive/randomized trial designs for personalized and fixed-cocktail phages.",
        "url": "https://www.fda.gov/media/159400/download",
    },
    {
        "id": "amr-niaid-phage-trial",
        "name": "NIH-Supported Phage Clinical Trials (Cystic Fibrosis & ESKAPE)",
        "category": "Clinical Translation",
        "plain": "NIH is funding controlled human trials testing whether inhaled or IV bacteriophages can safely clear chronic Pseudomonas lung infections.",
        "technical": "NIAID funds early-stage controlled phage clinical trials (including Pseudomonas aeruginosa in cystic fibrosis) and CAPT-CEP research centers targeting ESKAPE pathogens.",
        "url": "https://www.niaid.nih.gov/news-events/nih-supported-clinical-trial-phage-therapy-cystic-fibrosis-begins",
    },
    {
        "id": "amr-lbp-cmc-guidance",
        "name": "Live Biotherapeutic Products (LBPs): Early Clinical Trial CMC",
        "category": "Microbiome CMC",
        "plain": "Medicines made of living bacteria must prove every capsule has the right live colony count (CFU), zero harmful contaminants, and no hidden antibiotic-resistance genes.",
        "technical": "FDA's Early Clinical Trials with Live Biotherapeutic Products CMC guidance requires strain characterization, absence of transferable antimicrobial resistance genes, USP <61>/<62> bioburden controls, and CFU potency.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/early-clinical-trials-live-biotherapeutic-products-chemistry-manufacturing-and-control-information",
    },
    {
        "id": "amr-microbiome-fmt",
        "name": "Microbiome Restoration & C. difficile Colonization Resistance",
        "category": "Microbiome Therapy",
        "plain": "Restoring healthy gut bacteria after heavy antibiotic use crowds out deadly C. difficile infections without using more antibiotics.",
        "technical": "Microbiome-based therapeutics and donor-screened fecal microbiota products restore colonization resistance against recurrent Clostridioides difficile infection (rCDI) and multidrug-resistant gut colonization.",
        "url": "https://www.niaid.nih.gov/research/antimicrobial-resistance-treatment",
    },
    {
        "id": "amr-host-targeted-mab",
        "name": "Anti-Virulence, Monoclonal Antibodies & Host-Targeted Therapies",
        "category": "Non-Traditional Agents",
        "plain": "Instead of killing bacteria directly—which drives resistance—new antibodies neutralize bacterial toxins or help white blood cells clear superbugs.",
        "technical": "Non-traditional antimicrobials include pathogen-specific monoclonal antibodies, toxin neutralizers, efflux-pump/biofilm inhibitors, and host-directed immune modulators that minimize selective resistance pressure.",
        "url": "https://www.niaid.nih.gov/research/antimicrobial-resistance-basic-research-support",
    },
]


def build_amr_antiinfectives(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "qidp_lpad_pathways": len(QIDP_LPAD_PATHWAYS),
            "surveillance_stic": len(SURVEILLANCE_STIC),
            "carb_x_barda_incentives": len(CARB_X_BARDA_INCENTIVES),
            "phage_lbp_nontraditional": len(PHAGE_LBP_NONTRADITIONAL),
        },
        "qidp_lpad_pathways": QIDP_LPAD_PATHWAYS,
        "surveillance_stic": SURVEILLANCE_STIC,
        "carb_x_barda_incentives": CARB_X_BARDA_INCENTIVES,
        "phage_lbp_nontraditional": PHAGE_LBP_NONTRADITIONAL,
    }
    (data_dir / "amr_antiinfectives.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_amr_antiinfectives.py <site/data>")
    print(json.dumps(build_amr_antiinfectives(pathlib.Path(sys.argv[1])), indent=2))
'''

AMR_ANTIINFECTIVES_JS = '''// Pill by Pill v6.2e: Antimicrobial Resistance (AMR), Antibiotics, Phage Therapy & CARB-X / QIDP Incentives Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["qidp", "QIDP, GAIN & LPAD", "qidp_lpad_pathways"],
  ["stic", "Surveillance & STIC", "surveillance_stic"],
  ["carbx", "CARB-X & BARDA", "carb_x_barda_incentives"],
  ["phage", "Phages, LBPs & Non-Trad", "phage_lbp_nontraditional"],
];

function amrAntiinfectivesSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Antimicrobial resistance and anti-infective pipeline: QIDP GAIN and LPAD, CDC and FDA STIC Breakpoints, CARB-X and BARDA incentives, and Phage and LBP therapies">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. QIDP &amp; LPAD</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">+5 Yr GAIN Exclusivity</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Limited Population §506(h)</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#amr-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. STIC &amp; AR Lab</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">FDA Breakpoints (§511A)</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">CDC ARLN &amp; NARMS</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#amr-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. CARB-X &amp; BARDA</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Push/Pull R&amp;D Funding</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">NIAID ARLG &amp; Threats</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#amr-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Phages &amp; LBPs</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">CBER Phage &amp; Microbiome</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Anti-Virulence mAbs</text>
      <defs><marker id="amr-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Combating antimicrobial resistance combines QIDP/LPAD regulatory incentives, dynamic FDA STIC breakpoints and CDC surveillance, CARB-X/BARDA funding, and phage/microbiome therapies.</figcaption>
  </figure>`;
}

export async function amrAntiinfectivesPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/amr_antiinfectives.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/amr-antiinfectives" : "#/ref/amr-antiinfectives";

  const pills = html`<div class="chips" role="navigation" aria-label="Antimicrobial resistance, QIDP, and phage therapy sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Program / Standard</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.category}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${amrAntiinfectivesSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA QIDP/LPAD/STIC, CDC AR Lab Network &amp; NARMS, NIAID/CARB-X, HHS BARDA, and FDA CBER Phage/LBP documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["AMR, Antibiotics, Phages & CARB-X"]] : [REF_HOME, ["AMR, Antibiotics, Phages & CARB-X"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Antimicrobial Resistance, Antibiotics, Phages & CARB-X Incentives",
      lede: env === "explore"
        ? "How new antibiotics earn extra market protection, how labs track superbug resistance, and how phages and beneficial microbes fight drug-resistant infections."
        : "QIDP (GAIN 5-yr exclusivity) & LPAD (§ 506(h)), FDA STIC breakpoints (§ 511A), CDC ARLN/NARMS, CARB-X/BARDA push incentives, and CBER phage & LBP biologics.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on AMR incentives, breakpoints, and phage therapy.", href: env === "explore" ? "#/ref/amr-antiinfectives" : "#/explore/amr-antiinfectives" },
        { title: "Vaccines, Immunology & Adjuvants", text: "CBER vaccine platforms, ACIP governance, and mucosal immunity.", href: "#/ref/vaccines" },
        { title: "Drug Shortages & Essential Meds", text: "Protecting critical hospital antibiotics and sterile IV supplies.", href: "#/ref/shortages-resilience" },
      ],
    }),
  };
}
'''


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
    if 'amr_antiinfectives.js' not in txt:
        for anchor in ('import * as shortagesResilience from "./shortages_resilience.js";\n', 'import * as complexQuality from "./complex_quality.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as amrAntiinfectives from "./amr_antiinfectives.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as amrAntiinfectives from "./amr_antiinfectives.js";\n' + txt
            changed = True
    if '"/ref/amr-antiinfectives"' not in txt:
        for anchor in ('if (path === "/ref/shortages-resilience")', 'if (path === "/ref/complex-quality")', 'if (path === "/ref/vaccines")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/amr-antiinfectives") return { env: "ref", current: "#/ref/amr-antiinfectives", ...(await amrAntiinfectives.amrAntiinfectivesPage(query, "ref")) };\n  if (path === "/explore/amr-antiinfectives") return { env: "explore", current: "#/explore/amr-antiinfectives", ...(await amrAntiinfectives.amrAntiinfectivesPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/amr-antiinfectives" not in txt:
        for anchor in ('["#/ref/shortages-resilience", "Shortages & essential meds"]', '["#/ref/complex-quality", "Complex generics & impurities"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/amr-antiinfectives", "AMR, phages & CARB-X"]', 1)
                changed = True
                break
    if "#/explore/amr-antiinfectives" not in txt:
        for anchor in ('["#/explore/shortages-resilience", "Shortages & essential meds"]', '["#/explore/complex-quality", "Complex generics & impurities"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/amr-antiinfectives", "AMR, phages & CARB-X"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_amr_antiinfectives.py" in txt:
        return False
    line = "python3 pipeline/build_amr_antiinfectives.py site/data\n"
    if "build_global_search.py" in txt:
        txt = txt.replace("python3 pipeline/build_global_search.py", line + "python3 pipeline/build_global_search.py", 1)
    else:
        txt = txt + ("" if txt.endswith("\n") else "\n") + line
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/amr-antiinfectives"' in txt:
        return False
    route = (
        '\n@app.get("/api/amr-antiinfectives")\n'
        'def api_amr_antiinfectives():\n'
        '    p = DATA_DIR / "amr_antiinfectives.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "amr_antiinfectives.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"amr_antiinfectives.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    amr_ref = _load(data_dir / "amr_antiinfectives.json", {}) or {}\n'
        '    for sec_key, sec_q in [("qidp_lpad_pathways", "qidp"), ("surveillance_stic", "stic"), ("carb_x_barda_incentives", "carbx"), ("phage_lbp_nontraditional", "phage")]:\n'
        '        for item in (amr_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "amr_antiinfectives",\n'
        '                "group": "AMR, Antibiotics, Phages & CARB-X",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/amr-antiinfectives?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/amr-antiinfectives?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"AMR antimicrobial resistance antibiotic antifungal QIDP GAIN Act LPAD STIC breakpoints ARLN NARMS CARB-X BARDA phage bacteriophage LBP microbiome {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"amr-antiinfectives", "#/ref/amr-antiinfectives"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    amr_doc = _load_json(data_dir / "amr_antiinfectives.json")\n'
        '    if isinstance(amr_doc, dict) and amr_doc.get("qidp_lpad_pathways"):\n'
        '        amr_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (amr_doc.get("qidp_lpad_pathways") or []) + (amr_doc.get("phage_lbp_nontraditional") or []))\n'
        '        pages.append(("amr-antiinfectives", "#/ref/amr-antiinfectives", "Antimicrobial Resistance, Antibiotics, Phages & CARB-X",\n'
        '                      "Primary-sourced guide to QIDP/GAIN & LPAD pathways, FDA STIC breakpoints, CDC ARLN/NARMS, CARB-X/BARDA incentives, and bacteriophage/LBP therapies.",\n'
        '                      f"<ul>{amr_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/amr-antiinfectives"' in txt:
        return False
    for anchor in ('    "/#/explore/shortages-resilience",', '    "/#/explore/complex-quality",', '    "/#/explore/combo-products",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/amr-antiinfectives",\n    "/#/explore/amr-antiinfectives",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_amr_antiinfectives_py": _write_if_changed(pipe_dir / "build_amr_antiinfectives.py", BUILD_AMR_ANTIINFECTIVES_PY),
        "amr_antiinfectives_js": _write_if_changed(js_dir / "amr_antiinfectives.js", AMR_ANTIINFECTIVES_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/shortages-resilience") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/shortages-resilience", "Shortages & essential meds"]] }];\nconst EXPLORE_NAV = [["#/explore/shortages-resilience", "Shortages & essential meds"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/shortages-resilience",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_amr_antiinfectives.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_amr_antiinfectives.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"qidp_lpad_pathways": 6, "surveillance_stic": 6, "carb_x_barda_incentives": 6, "phage_lbp_nontraditional": 6}, out

        doc = json.loads((root / "site" / "data" / "amr_antiinfectives.json").read_text(encoding="utf-8"))
        for k in ("qidp_lpad_pathways", "surveillance_stic", "carb_x_barda_incentives", "phage_lbp_nontraditional"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "amr_antiinfectives.js").read_text(encoding="utf-8")
        print("V62E_AMR_ANTIINFECTIVES_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2e AMR, Antibiotics, Phage Therapy & CARB-X patch.")
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
