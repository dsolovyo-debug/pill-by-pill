#!/usr/bin/env python3
"""Pill by Pill v6.2j Patch: Regenerative Medicine (RMAT), HCT/Ps (21 CFR 1271), CGT Potency Assurance & Human Genome Editing / Long-Term Follow-Up Reference (#/ref/rmat-hctp-cgt-cmc, #/explore/rmat-hctp-cgt-cmc, /api/rmat-hctp-cgt-cmc).

1. Adds `pipeline/build_rmat_hctp_cgt_cmc.py` -> `site/data/rmat_hctp_cgt_cmc.json` (6 RMAT Expedited
   Programs pillars, 6 HCT/P 21 CFR 1271 Section 361 vs. 351 pillars, 6 CGT Potency Assurance &
   Late-Stage CMC pillars, and 6 Human Genome Editing & Long-Term Follow-Up pillars — 24
   primary-sourced entries).
2. Adds `site/js/rmat_hctp_cgt_cmc.js` (`rmatHctpCgtCmcPage` with inline RMAT, HCT/P, Potency &
   Genome Editing SVG + 4 section filters) and wires `#/ref/rmat-hctp-cgt-cmc`,
   `#/explore/rmat-hctp-cgt-cmc`, `/api/rmat-hctp-cgt-cmc`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `rmat_hctp_cgt_cmc.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/rmat-hctp-cgt-cmc/` static SEO page + sitemap entry ->
   52 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2j_rmat_hctp_cgt_potency_genome_editing_patch.py --selftest
  python3 2026-11-24_v6.2j_rmat_hctp_cgt_potency_genome_editing_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_RMAT_HCTP_CGT_CMC_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2j Regenerative Medicine (RMAT), HCT/Ps, CGT Potency & Genome Editing Reference (`site/data/rmat_hctp_cgt_cmc.json`).

Comprehensive, primary-sourced reference covering:
  1. Regenerative Medicine Advanced Therapy (RMAT) Designation (6 pillars)
  2. HCT/Ps: 21 CFR Part 1271, Section 361 vs. Section 351 (6 pillars)
  3. CGT Potency Assurance & Late-Stage Vector CMC (6 pillars)
  4. Human Genome Editing (CRISPR) & Long-Term Follow-Up (LTFU) (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CBER OTP).

Usage:
  python3 pipeline/build_rmat_hctp_cgt_cmc.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

RMAT_EXPEDITED = [
    {
        "id": "rmc-rmat-designation",
        "name": "Regenerative Medicine Advanced Therapy (RMAT) Designation",
        "category": "21st Century Cures § 3033",
        "plain": "Cell, gene, and tissue therapies showing early clinical promise for serious diseases can earn RMAT status—unlocking intensive FDA guidance and faster approval paths.",
        "technical": "Created by § 3033 of the 21st Century Cures Act (FD&C Act § 506(g)), RMAT designation is granted to cell therapies, therapeutic tissue-engineered products, and gene therapies demonstrating preliminary clinical evidence of addressing unmet medical need.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/regenerative-medicine-advanced-therapy-designation",
    },
    {
        "id": "rmc-rmat-expedited-2025",
        "name": "Expedited Programs for Regenerative Medicine Therapies",
        "category": "Accelerated Pathways",
        "plain": "RMAT therapies can qualify for Accelerated Approval using intermediate biomarkers or early clinical outcomes, then confirm long-term durability afterward.",
        "technical": "FDA's Expedited Programs for Regenerative Medicine Therapies guidance details how RMAT products leverage Breakthrough Therapy-level OTP engagement, Accelerated Approval surrogate/intermediate endpoints, and post-approval RWE.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/expedited-programs-regenerative-medicine-therapies-serious-conditions-0",
    },
    {
        "id": "rmc-rmat-otp-meetings",
        "name": "CBER Office of Therapeutic Products (OTP) Type B & Initial Meetings",
        "category": "FDA Engagement",
        "plain": "RMAT-designated developers get an early all-hands meeting with FDA's cell and gene therapy experts to align manufacturing and trial endpoints.",
        "technical": "FDA CBER OTP grants RMAT and Breakthrough Therapy sponsors an Initial Comprehensive Meeting plus Type B Pre-IND, End-of-Phase, and Pre-BLA milestones (combined into one if holding both designations).",
        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/meetings-regenerative-medicine-advanced-therapy-rmat-and-breakthrough-therapy-bt-designated-products",
    },
    {
        "id": "rmc-rmat-approvals",
        "name": "CBER RMAT Approvals Registry",
        "category": "Licensed Therapies",
        "plain": "FDA tracks every approved regenerative medicine therapy that graduated from RMAT designation to full patient availability.",
        "technical": "CBER maintains the official RMAT Approvals registry documenting licensed gene therapies, CAR-T immunotherapies, and tissue-engineered products that utilized RMAT expedited development.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/cber-regenerative-medicine-advanced-therapy-rmat-approvals",
    },
    {
        "id": "rmc-rmat-devices",
        "name": "Devices & Biologic-Device Combination Products with RMAT",
        "category": "Combination RMAT",
        "plain": "A cell therapy paired with a biodegradable scaffold or surgical delivery catheter can still qualify for RMAT if the living biologic does the main healing work.",
        "technical": "Combination products (biologic-device or biologic-drug-device) are eligible for RMAT designation when the regenerative medicine biologic constituent provides the Primary Mode of Action (PMOA).",
        "url": "https://www.fda.gov/media/120266/download",
    },
    {
        "id": "rmc-rmat-sopp8215",
        "name": "SOPP 8215: CBER Management of RMAT Designation Requests",
        "category": "Review Procedure",
        "plain": "FDA follows a standardized 60-day internal review clock to decide whether a cell or gene therapy qualifies for RMAT status.",
        "technical": "CBER Standard Operating Policy and Procedure (SOPP) 8215 governs intake, multidisciplinary OTP review, 60-calendar-day determination, and rescission procedures for RMAT designation requests.",
        "url": "https://www.fda.gov/media/172173/download",
    },
]

HCTP_1271 = [
    {
        "id": "rmc-hctp-guidance",
        "name": "HCT/Ps: Minimal Manipulation & Homologous Use (21 CFR 1271)",
        "category": "Tissue Regulation",
        "plain": "Simple donated tissues like bone grafts or corneas don't need full drug trials—but stem-cell clinics that chemically digest fat or make non-homologous claims do.",
        "technical": "FDA's Regulatory Considerations for HCT/Ps guidance interprets 21 CFR 1271.10(a) criteria distinguishing Section 361 PHS Act tissues (donor screening/GTPs only) from Section 351 biologics requiring IND/BLA.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/regulatory-considerations-human-cells-tissues-and-cellular-and-tissue-based-products-minimal",
    },
    {
        "id": "rmc-hctp-minimal-manip",
        "name": "Minimal Manipulation Criteria (Structural vs. Cellular Tissues)",
        "category": "21 CFR 1271.3(f)",
        "plain": "Cutting or freezing bone keeps it 'minimally manipulated', whereas grinding tissue to extract and culture stem cells alters its biology and triggers full FDA drug rules.",
        "technical": "Under 21 CFR 1271.3(f), minimal manipulation means processing that does not alter original structural characteristics (for structural tissue) or relevant biological characteristics (for cells/nonstructural tissue).",
        "url": "https://www.fda.gov/media/109176/download",
    },
    {
        "id": "rmc-hctp-homologous-use",
        "name": "Homologous Use & Same-Surgical-Procedure Exception",
        "category": "21 CFR 1271.10(a)(2)",
        "plain": "A tissue must perform the same basic job in the recipient as it did in the donor—using umbilical cord blood for knee arthritis is non-homologous and requires an IND.",
        "technical": "Homologous use requires repair, reconstruction, replacement, or supplementation of a recipient's cells/tissues with an HCT/P performing the same basic function(s) in the recipient as in the donor.",
        "url": "https://www.fda.gov/media/109176/download",
    },
    {
        "id": "rmc-hctp-enforcement-qa",
        "name": "End of HCT/P Enforcement Discretion (Unapproved Stem Cell Products)",
        "category": "Compliance Enforcement",
        "plain": "FDA ended its grace period in 2021 for unapproved stem-cell and exosome clinics, requiring full IND/BLA clinical proof before marketing.",
        "technical": "Following the May 2021 end of compliance/enforcement discretion, manufacturers of non-361 HCT/Ps (e.g., adipose SVF, birth-tissue exosomes) without an active IND or BLA face FDA enforcement.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products/questions-and-answers-regarding-end-compliance-and-enforcement-policy-certain-human-cells-tissues-or",
    },
    {
        "id": "rmc-hctp-tissue-guidances",
        "name": "Good Tissue Practices (cGTP) & Donor Eligibility (21 CFR 1271)",
        "category": "Communicable Disease",
        "plain": "Every human tissue bank must screen donors for HIV, hepatitis, and infectious diseases and follow Good Tissue Practices to prevent contamination.",
        "technical": "21 CFR Part 1271 Subparts C and D mandate donor eligibility determination (infectious disease testing/screening) and Current Good Tissue Practices (cGTP) for all Section 361 HCT/P establishments.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/tissue-guidances",
    },
    {
        "id": "rmc-hctp-cp-7341",
        "name": "FDA Inspection of Human Tissue Establishments (CP 7341.002)",
        "category": "BIMO / Tissue Audit",
        "plain": "FDA inspectors audit tissue banks and cord-blood facilities to verify donor records, quarantine steps, and sterile recovery.",
        "technical": "Compliance Program 7341.002 governs FDA inspections of HCT/P establishments, verifying registration/listing, donor eligibility records, recovery/processing controls, and adverse reaction reporting.",
        "url": "https://www.fda.gov/media/73949/download",
    },
]

CGT_POTENCY_CMC = [
    {
        "id": "rmc-cgt-potency-assurance",
        "name": "Potency Assurance Strategy for Cellular & Gene Therapy Products",
        "category": "Lifecycle Potency",
        "plain": "Because living cells and viral vectors are complex, FDA expects a top-to-bottom potency strategy—linking raw materials, process controls, and bioassays.",
        "technical": "FDA's Potency Assurance for CGT Products guidance outlines a science- and risk-based Potency Assurance Strategy integrating process design, in-process controls, material controls, and quantitative lot-release bioassays.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/potency-assurance-cellular-and-gene-therapy-products",
    },
    {
        "id": "rmc-cgt-guidances-hub",
        "name": "CBER Cellular & Gene Therapy CMC Flexibilities & BLA Readiness",
        "category": "OTP Guidance Hub",
        "plain": "FDA's Cellular & Gene Therapy guidance hub collects the latest rules on comparability, genome-editing safety, and manufacturing flexibilities.",
        "technical": "CBER OTP's Cellular & Gene Therapy Guidances hub indexes CMC flexibilities for BLA submission, manufacturing comparability (Jul 2023), and disease-specific GT development (hemophilia, retinal, rare diseases).",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/cellular-gene-therapy-guidances",
    },
    {
        "id": "rmc-cgt-short-shelflife",
        "name": "Short-Shelf-Life Cell Therapies: Rapid Release & Post-Release Testing",
        "category": "Autologous Release",
        "plain": "Fresh cell therapies that expire in hours can't wait weeks for slow lab tests—so FDA allows rapid release assays backed by post-release verification.",
        "technical": "For fresh autologous CGTs with ultra-short shelf life, CBER permits rapid surrogate lot-release assays paired with a risk-based post-release potency bioassay initiated immediately after drug product fill.",
        "url": "https://www.fda.gov/media/183285/download",
    },
    {
        "id": "rmc-cgt-ppq-phase3",
        "name": "Phase 3 Potency Acceptance Criteria & Process Performance Qualification (PPQ)",
        "category": "BLA Validation",
        "plain": "Before starting pivotal Phase 3 trials, CGT developers must set clear potency pass/fail ranges and qualify full-scale manufacturing runs.",
        "technical": "CBER requires justified potency assay acceptance criteria prior to Phase 3 initiation, validated incoming raw-material identity tests by licensure, and sequential full-scale PPQ runs per Process Validation guidance.",
        "url": "https://www.fda.gov/media/183285/download",
    },
    {
        "id": "rmc-cgt-actimp-potency",
        "name": "Potency Assessment of Active Immunotherapy Products (ACTIMPs)",
        "category": "Cancer Vaccines / Immunotherapy",
        "plain": "Therapeutic cancer vaccines and immune-cell activators need tailored potency tests proving they actually wake up T-cells against tumor antigens.",
        "technical": "FDA's Potency Assessment of Active Immunotherapy Products (ACTIMPs) draft guidance supplements CGT potency assurance for antigen-presenting cell, peptide, and protein immunotherapies.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/potency-assessment-active-immunotherapy-products",
    },
    {
        "id": "rmc-cgt-rcr-testing",
        "name": "Replication-Competent Retrovirus / Lentivirus (RCR/RCL) Testing",
        "category": "Vector Biosafety",
        "plain": "Every batch of CAR-T cells or viral vector must pass sensitive tests proving no infectious, self-replicating virus accidentally formed during manufacturing.",
        "technical": "FDA's RCR/RCL Testing guidance requires testing vector master/working cell banks, vector lots, and ex vivo transduced cells (with PAS reduction options once consistent RCL-negativity is proven).",
        "url": "https://www.fda.gov/media/113790/download",
    },
]

GENOME_EDITING_LTFU = [
    {
        "id": "rmc-ge-jan2024",
        "name": "Human Gene Therapy Products Incorporating Human Genome Editing (Jan 2024)",
        "category": "CRISPR / Base / Prime Editing",
        "plain": "Gene-editing treatments using CRISPR or base editors must map both on-target DNA fixes and any accidental 'off-target' cuts elsewhere in the genome.",
        "technical": "FDA's January 2024 Genome Editing Guidance details CMC characterization of nucleases/gRNAs/RNPs, orthogonal off-target editing assessment, chromosomal translocation/integrity checks, and clinical safety monitoring.",
        "url": "https://www.fda.gov/media/156894/download",
    },
    {
        "id": "rmc-ge-ngs-offtarget",
        "name": "NGS & Bioinformatics Safety Assessment of Off-Target Genome Editing",
        "category": "Genomic Integrity",
        "plain": "Scientists use next-generation DNA sequencing (NGS) and bioinformatics to verify CRISPR didn't cause unintended mutations or chromosome rearrangements.",
        "technical": "FDA's NGS Safety Assessment guidance provides recommendations for unbiased biochemical/cellular nomination of off-target sites, targeted deep-sequencing validation, and structural variant bioinformatics.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-assessment-genome-editing-human-gene-therapy-products-using-next-generation-sequencing",
    },
    {
        "id": "rmc-ltfu-guidance",
        "name": "Long-Term Follow-Up (LTFU) After Gene Therapy (Up to 15 Years)",
        "category": "Delayed Adverse Events",
        "plain": "Because permanent gene therapies stay in the body for life, patients are monitored for 5 to 15 years to watch for delayed immune or cancer risks.",
        "technical": "FDA's Long-Term Follow-Up (LTFU) Guidance defines risk-based observation windows (up to 15 years for integrating vectors and genome editing; up to 5 years for non-integrating AAV with persistence) for delayed AEs.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/long-term-follow-after-administration-human-gene-therapy-products",
    },
    {
        "id": "rmc-ltfu-integration",
        "name": "Vector Integration, Latency & Delayed Malignancy Risk Framework",
        "category": "Risk Stratification",
        "plain": "Viruses that stitch DNA permanently into human chromosomes carry higher long-term monitoring rules than temporary gene therapies.",
        "technical": "LTFU risk stratification evaluates vector integration propensity (retrovirus, lentivirus, transposons), viral latency/reactivation, and transgene persistence to set clinical LTFU and post-licensure surveillance plans.",
        "url": "https://www.fda.gov/files/vaccines%2C%20blood%20%26%20biologics/published/Long-Term-Follow-Up-After-Admin-Human-GT-Products_Jan_2020.pdf",
    },
    {
        "id": "rmc-ge-individualized",
        "name": "Individualized Human Genome Editing & Plausible Mechanism Framework",
        "category": "N-of-1 CRISPR",
        "plain": "New FDA frameworks help doctors develop bespoke CRISPR edits for ultra-rare genetic diseases by leveraging prior platform knowledge of the editor.",
        "technical": "CBER OTP's Individualized Genome Editing and Plausible Mechanism Framework guidances enable leveraging prior knowledge across guide-RNA swaps and shared LNP/AAV platforms for bespoke genetic conditions.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/cellular-gene-therapy-guidances",
    },
    {
        "id": "rmc-cgt-developing-faq",
        "name": "Developing Potential Cellular & Gene Therapy Products (OTP FAQ)",
        "category": "Early IND Readiness",
        "plain": "FDA's OTP FAQ answers common startup questions on preclinical animal models, vector manufacturing, and INTERACT meetings.",
        "technical": "CBER's Developing Potential CGT Products guidance consolidates cross-disciplinary CMC, pharmacology/toxicology, and clinical trial design expectations for early-stage CGT INDs.",
        "url": "https://www.fda.gov/media/183631/download",
    },
]


def build_rmat_hctp_cgt_cmc(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "rmat_expedited": len(RMAT_EXPEDITED),
            "hctp_1271": len(HCTP_1271),
            "cgt_potency_cmc": len(CGT_POTENCY_CMC),
            "genome_editing_ltfu": len(GENOME_EDITING_LTFU),
        },
        "rmat_expedited": RMAT_EXPEDITED,
        "hctp_1271": HCTP_1271,
        "cgt_potency_cmc": CGT_POTENCY_CMC,
        "genome_editing_ltfu": GENOME_EDITING_LTFU,
    }
    (data_dir / "rmat_hctp_cgt_cmc.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_rmat_hctp_cgt_cmc.py <site/data>")
    print(json.dumps(build_rmat_hctp_cgt_cmc(pathlib.Path(sys.argv[1])), indent=2))
'''

RMAT_HCTP_CGT_CMC_JS = '''// Pill by Pill v6.2j: Regenerative Medicine (RMAT), HCT/Ps (21 CFR 1271), CGT Potency Assurance & Genome Editing / LTFU Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["rmat", "RMAT Expedited Pathway", "rmat_expedited"],
  ["hctp", "HCT/Ps (21 CFR 1271)", "hctp_1271"],
  ["potency", "CGT Potency & Vector CMC", "cgt_potency_cmc"],
  ["editing", "Genome Editing & LTFU", "genome_editing_ltfu"],
];

function rmatHctpCgtCmcSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Regenerative medicine and CGT lifecycle: RMAT designation, HCT/P 21 CFR 1271, CGT Potency Assurance, and Genome Editing and Long-Term Follow-Up">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. RMAT (§506(g))</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Expedited Reg. Med.</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">OTP Type B &amp; AA</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rmc-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. HCT/Ps (1271)</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Minimal Manipulation</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">§361 vs. §351 BLA</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rmc-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. CGT Potency CMC</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Potency Assurance</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">PPQ &amp; RCR/RCL Tests</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rmc-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Editing &amp; LTFU</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">CRISPR Off-Target NGS</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">5–15 Yr Follow-Up</text>
      <defs><marker id="rmc-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Regenerative medicine governance spans RMAT expedited pathways, 21 CFR 1271 tissue boundaries, CGT potency assurance strategies, and 15-year genome-editing follow-up.</figcaption>
  </figure>`;
}

export async function rmatHctpCgtCmcPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/rmat_hctp_cgt_cmc.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/rmat-hctp-cgt-cmc" : "#/ref/rmat-hctp-cgt-cmc";

  const pills = html`<div class="chips" role="navigation" aria-label="RMAT, HCT/Ps, CGT potency, and genome editing sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Standard / Guidance</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${rmatHctpCgtCmcSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA CBER Office of Therapeutic Products (RMAT, 21 CFR 1271 HCT/Ps, CGT Potency Assurance, Human Genome Editing, and LTFU) documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["RMAT, HCT/Ps, CGT Potency & Genome Editing"]] : [REF_HOME, ["RMAT, HCT/Ps, CGT Potency & Genome Editing"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Regenerative Medicine (RMAT), HCT/Ps, CGT Potency & Genome Editing",
      lede: env === "explore"
        ? "How regenerative therapies earn fast-track RMAT status, when human tissues need full drug approval, and how CRISPR gene edits are monitored for 15 years."
        : "21st Century Cures RMAT (§ 506(g)), 21 CFR 1271 HCT/P minimal manipulation & homologous use, CGT Potency Assurance, and CRISPR/LTFU safety.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on RMAT, HCT/Ps, CGT potency, and genome editing.", href: env === "explore" ? "#/ref/rmat-hctp-cgt-cmc" : "#/explore/rmat-hctp-cgt-cmc" },
        { title: "Biologics, Cell & Gene Therapy", text: "CAR-T vein-to-vein logistics, AAV vectors, and mRNA platforms.", href: "#/ref/atmp" },
        { title: "ADCs, Bispecifics & Oligos", text: "Targeted biologics, synthetic peptides, and N-of-1 ASO INDs.", href: "#/ref/adcs-bispecifics-oligos" },
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
    if 'rmat_hctp_cgt_cmc.js' not in txt:
        for anchor in ('import * as adcsBispecificsOligos from "./adcs_bispecifics_oligos.js";\n', 'import * as gcpBimoCdisc from "./gcp_bimo_cdisc.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as rmatHctpCgtCmc from "./rmat_hctp_cgt_cmc.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as rmatHctpCgtCmc from "./rmat_hctp_cgt_cmc.js";\n' + txt
            changed = True
    if '"/ref/rmat-hctp-cgt-cmc"' not in txt:
        for anchor in ('if (path === "/ref/adcs-bispecifics-oligos")', 'if (path === "/ref/gcp-bimo-cdisc")', 'if (path === "/ref/atmp")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/rmat-hctp-cgt-cmc") return { env: "ref", current: "#/ref/rmat-hctp-cgt-cmc", ...(await rmatHctpCgtCmc.rmatHctpCgtCmcPage(query, "ref")) };\n  if (path === "/explore/rmat-hctp-cgt-cmc") return { env: "explore", current: "#/explore/rmat-hctp-cgt-cmc", ...(await rmatHctpCgtCmc.rmatHctpCgtCmcPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/rmat-hctp-cgt-cmc" not in txt:
        for anchor in ('["#/ref/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]', '["#/ref/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]', 1)
                changed = True
                break
    if "#/explore/rmat-hctp-cgt-cmc" not in txt:
        for anchor in ('["#/explore/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]', '["#/explore/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_rmat_hctp_cgt_cmc.py" in txt:
        return False
    line = "python3 pipeline/build_rmat_hctp_cgt_cmc.py site/data\n"
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
    if '"/api/rmat-hctp-cgt-cmc"' in txt:
        return False
    route = (
        '\n@app.get("/api/rmat-hctp-cgt-cmc")\n'
        'def api_rmat_hctp_cgt_cmc():\n'
        '    p = DATA_DIR / "rmat_hctp_cgt_cmc.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "rmat_hctp_cgt_cmc.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rmat_hctp_cgt_cmc.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    rmc_ref = _load(data_dir / "rmat_hctp_cgt_cmc.json", {}) or {}\n'
        '    for sec_key, sec_q in [("rmat_expedited", "rmat"), ("hctp_1271", "hctp"), ("cgt_potency_cmc", "potency"), ("genome_editing_ltfu", "editing")]:\n'
        '        for item in (rmc_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "rmat_hctp_cgt_cmc",\n'
        '                "group": "RMAT, HCT/Ps, CGT Potency & Genome Editing",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/rmat-hctp-cgt-cmc?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/rmat-hctp-cgt-cmc?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"RMAT regenerative medicine advanced therapy HCT/P 21 CFR 1271 minimal manipulation homologous use cGTP potency assurance CGT RCR RCL CRISPR genome editing LTFU long term follow up {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"rmat-hctp-cgt-cmc", "#/ref/rmat-hctp-cgt-cmc"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    rmc_doc = _load_json(data_dir / "rmat_hctp_cgt_cmc.json")\n'
        '    if isinstance(rmc_doc, dict) and rmc_doc.get("rmat_expedited"):\n'
        '        rmc_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (rmc_doc.get("rmat_expedited") or []) + (rmc_doc.get("genome_editing_ltfu") or []))\n'
        '        pages.append(("rmat-hctp-cgt-cmc", "#/ref/rmat-hctp-cgt-cmc", "Regenerative Medicine (RMAT), HCT/Ps, CGT Potency & Genome Editing",\n'
        '                      "Primary-sourced guide to RMAT designation, 21 CFR 1271 HCT/P minimal manipulation & homologous use, CGT potency assurance, and CRISPR/LTFU safety.",\n'
        '                      f"<ul>{rmc_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/rmat-hctp-cgt-cmc"' in txt:
        return False
    for anchor in ('    "/#/explore/adcs-bispecifics-oligos",', '    "/#/explore/gcp-bimo-cdisc",', '    "/#/explore/oncology-oce",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/rmat-hctp-cgt-cmc",\n    "/#/explore/rmat-hctp-cgt-cmc",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_rmat_hctp_cgt_cmc_py": _write_if_changed(pipe_dir / "build_rmat_hctp_cgt_cmc.py", BUILD_RMAT_HCTP_CGT_CMC_PY),
        "rmat_hctp_cgt_cmc_js": _write_if_changed(js_dir / "rmat_hctp_cgt_cmc.js", RMAT_HCTP_CGT_CMC_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/adcs-bispecifics-oligos") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]] }];\nconst EXPLORE_NAV = [["#/explore/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/adcs-bispecifics-oligos",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_rmat_hctp_cgt_cmc.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_rmat_hctp_cgt_cmc.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"rmat_expedited": 6, "hctp_1271": 6, "cgt_potency_cmc": 6, "genome_editing_ltfu": 6}, out

        doc = json.loads((root / "site" / "data" / "rmat_hctp_cgt_cmc.json").read_text(encoding="utf-8"))
        for k in ("rmat_expedited", "hctp_1271", "cgt_potency_cmc", "genome_editing_ltfu"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "rmat_hctp_cgt_cmc.js").read_text(encoding="utf-8")
        print("V62J_RMAT_HCTP_CGT_CMC_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2j RMAT, HCT/Ps, CGT Potency & Genome Editing patch.")
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
