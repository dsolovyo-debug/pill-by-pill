#!/usr/bin/env python3
"""Pill by Pill v6.2i Patch: Antibody-Drug Conjugates (ADCs), Bispecific Antibodies, Synthetic Peptides & Oligonucleotide Therapeutics (ASOs/siRNAs/N-of-1) Reference (#/ref/adcs-bispecifics-oligos, #/explore/adcs-bispecifics-oligos, /api/adcs-bispecifics-oligos).

1. Adds `pipeline/build_adcs_bispecifics_oligos.py` -> `site/data/adcs_bispecifics_oligos.json`
   (6 Antibody-Drug Conjugates pillars, 6 Bispecific Antibodies pillars, 6 Synthetic Peptides
   pillars, and 6 Oligonucleotide Therapeutics pillars — 24 primary-sourced entries).
2. Adds `site/js/adcs_bispecifics_oligos.js` (`adcsBispecificsOligosPage` with inline Targeted
   Biologics & Oligos SVG + 4 section filters) and wires `#/ref/adcs-bispecifics-oligos`,
   `#/explore/adcs-bispecifics-oligos`, `/api/adcs-bispecifics-oligos`, `REF_NAV_GROUPS`,
   `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `adcs_bispecifics_oligos.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/adcs-bispecifics-oligos/` static SEO page + sitemap
   entry -> 51 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2i_adcs_bispecifics_peptides_oligonucleotides_patch.py --selftest
  python3 2026-11-24_v6.2i_adcs_bispecifics_peptides_oligonucleotides_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_ADCS_BISPECIFICS_OLIGOS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2i ADCs, Bispecifics, Synthetic Peptides & Oligonucleotide Therapeutics Reference (`site/data/adcs_bispecifics_oligos.json`).

Comprehensive, primary-sourced reference covering:
  1. Antibody-Drug Conjugates (ADCs) Clinical Pharmacology & Bioanalytics (6 pillars)
  2. Bispecific & Multispecific Antibodies (6 pillars)
  3. Synthetic Peptides & GLP-1 Generic Sameness (6 pillars)
  4. Oligonucleotide Therapeutics (ASOs, siRNAs & N-of-1 INDs) (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER, CBER, OGD, OPQ).

Usage:
  python3 pipeline/build_adcs_bispecifics_oligos.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

ADC_ENGINEERING = [
    {
        "id": "abo-adc-clinpharm-2024",
        "name": "FDA Clinical Pharmacology Considerations for ADCs (Mar 2024)",
        "category": "ADC Final Guidance",
        "plain": "Antibody-drug conjugates (ADCs) are 'guided missiles'—an antibody latches onto a cancer cell and releases a potent chemotherapy payload inside.",
        "technical": "FDA's March 2024 ADC Guidance establishes clinical pharmacology standards for cytotoxic small-molecule ADCs across bioanalytical assays, dosing, exposure-response, organ impairment, QTc, immunogenicity, and DDIs.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-pharmacology-considerations-antibody-drug-conjugates-guidance-industry",
    },
    {
        "id": "abo-adc-bioanalytics",
        "name": "Multi-Analyte ADC Bioanalytics: Conjugated vs. Unconjugated Payload",
        "category": "Bioanalytical PK",
        "plain": "Because an ADC carries both a big antibody and a small-molecule toxin, labs must separately track the intact drug, the bare antibody, and free floating toxin.",
        "technical": "FDA recommends validated assays quantifying conjugated antibody/ADC, total antibody, and unconjugated payload (plus active metabolites), distinguishing target-bound vs. unbound species when target sheds.",
        "url": "https://www.fda.gov/media/177250/download",
    },
    {
        "id": "abo-adc-qtc-payload",
        "name": "QTc Cardiac Prolongation Assessment Focused on Unconjugated Payload",
        "category": "Cardiac Safety",
        "plain": "The large antibody rarely disturbs heart rhythms, so heart-safety ECG checks focus on the small chemical payload and linker.",
        "technical": "Under ICH E14/S7B, ADC QTc risk assessment generally focuses on the unconjugated cytotoxic payload, linker, and pharmacologically active metabolites rather than the monoclonal antibody backbone.",
        "url": "https://www.fda.gov/media/155997/download",
    },
    {
        "id": "abo-adc-ddi-substrate",
        "name": "Drug-Drug Interactions (DDIs) of Cytotoxic ADC Payloads",
        "category": "CYP / Transporter DDI",
        "plain": "Even tiny amounts of free chemo payload in the bloodstream can cause severe side effects if another medication blocks liver enzymes from clearing it.",
        "technical": "FDA requires in vitro CYP/transporter DDI characterization for unconjugated ADC payloads as both substrate and precipitant—even at low systemic exposure due to narrow therapeutic index.",
        "url": "https://www.fda.gov/media/177250/download",
    },
    {
        "id": "abo-adc-dosing-exposure",
        "name": "ADC Broad Dose-Finding & Exposure-Response Optimization",
        "category": "Dose Selection",
        "plain": "Early ADC trials test a wide range of doses so doctors find the sweet spot that kills tumor cells without causing nerve or lung toxicity.",
        "technical": "Both antibody and payload independently drive ADC safety/efficacy; FDA recommends early broad-range dose exploration and separate exposure-response modeling for ADC and unconjugated payload.",
        "url": "https://www.fda.gov/media/177250/download",
    },
    {
        "id": "abo-adc-podcast",
        "name": "FDA ADC Regulatory Science Evolution (11+ Approved Oncology ADCs)",
        "category": "CDER Perspective",
        "plain": "With over a decade of ADC approvals behind it, FDA synthesized lessons from 11+ cancer ADCs into one playbook.",
        "technical": "CDER's ADC Guidance Recap summarizes regulatory experience across 11+ approved oncology ADCs, bridging biologic BLAs with small-molecule payload pharmacology.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/guidance-recap-podcast-clinical-pharmacology-considerations-antibody-drug-conjugates",
    },
]

BISPECIFIC_ANTIBODIES = [
    {
        "id": "abo-bsab-guidance-2021",
        "name": "Bispecific Antibody Development Programs Guidance (May 2021)",
        "category": "Dual-Target Biologics",
        "plain": "Bispecific antibodies have two different gripping arms—often grabbing a cancer cell with one hand and pulling in an immune T-cell with the other.",
        "technical": "FDA's May 2021 Bispecific Antibody Guidance covers dual-target scientific rationale, simultaneous vs. sequential binding kinetics, CMC structural characterization, and clinical trial comparisons.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/bispecific-antibody-development-programs-guidance-industry",
    },
    {
        "id": "abo-bsab-cd3-fih",
        "name": "CD3 T-Cell Engager First-in-Human (FIH) MABEL Dosing",
        "category": "Immune Activation",
        "plain": "Because T-cell-engaging antibodies can trigger dangerous immune storms even at tiny doses, first-in-human studies start far below standard safety limits.",
        "technical": "For CD3 bispecific T-cell engagers, FDA cites Minimum Anticipated Biological Effect Level (MABEL) FIH starting doses (~10–30% pharmacological activity) and excludes healthy volunteers due to CRS/toxicity.",
        "url": "https://www.fda.gov/media/123313/download",
    },
    {
        "id": "abo-bsab-domain-ada",
        "name": "Domain-Specific Immunogenicity (ADA) Assays for Bispecifics",
        "category": "Immunogenicity",
        "plain": "Because bispecific antibodies are engineered from two different antibodies, patients can develop immune reactions against one arm while the other still works.",
        "technical": "FDA recommends multi-domain Anti-Drug Antibody (ADA) and neutralizing assays capable of distinguishing immune responses directed at individual Fab/scFv arms or linker junctions.",
        "url": "https://www.fda.gov/media/123313/download",
    },
    {
        "id": "abo-bsab-sameness-cdr",
        "name": "CDR Sameness Rules for Bispecifics & Antibody Conjugates (Orphan)",
        "category": "Biologic Identity",
        "plain": "FDA decides whether two bispecific antibodies count as the 'same drug' by comparing the exact binding loops (CDRs) on both arms.",
        "technical": "Under FDA's Monoclonal Antibody Sameness guidance, two bispecific/multispecific antibodies are considered the same drug if all sets of CDRs (VH-VL or single-V domains) are identical or differ by minor amino acids.",
        "url": "https://www.fda.gov/files/vaccines,%20blood%20&%20biologics/published/Interpreting-Sameness-of-Monoclonal-Antibody-Products-Under-the-Orphan-Drug-Regulations.pdf",
    },
    {
        "id": "abo-bsab-stepup-dosing",
        "name": "Step-Up Dosing & CRS Mitigation in BCMA/CD3 Bispecifics",
        "category": "Clinical Regimen",
        "plain": "Modern bispecifics start with tiny 'step-up' priming doses over the first week so the immune system warms up gradually without cytokine storm.",
        "technical": "Approved CD3 bispecifics (e.g., BCMA×CD3 linvoseltamab-gcpt) utilize step-up priming schedules (5 mg -> 25 mg -> 200 mg) and response-adapted maintenance intervals to mitigate Cytokine Release Syndrome.",
        "url": "https://www.fda.gov/drugs/cancer-approvals/fda-grants-accelerated-approval-linvoseltamab-gcpt-relapsed-or-refractory-multiple-myeloma",
    },
    {
        "id": "abo-bsab-rational-bridge",
        "name": "Scientific Rationale: Bispecific vs. Monospecific Antibody Cocktails",
        "category": "Mechanism Justification",
        "plain": "Developers must prove why engineering two targets into one bispecific molecule works better than simply giving two separate antibody drugs together.",
        "technical": "FDA expects mechanistic justification (e.g., obligate cell-bridging, avidity, or synergistic receptor blockade) showing why a single bispecific outperforms monospecific standard-of-care or antibody mixtures.",
        "url": "https://www.fda.gov/media/123313/download",
    },
]

SYNTHETIC_PEPTIDES = [
    {
        "id": "abo-pep-anda-sameness",
        "name": "ANDA Active Ingredient Sameness for Synthetic Peptides (vs. rDNA)",
        "category": "Generic Peptide Pathway",
        "plain": "Generic makers can chemically synthesize copies of older biotech peptides (like glucagon or GLP-1 drugs)—as long as they prove identical structure and fewer impurities.",
        "technical": "FDA's ANDAs for Certain Highly Purified Synthetic Peptide Drug Products guidance enables 505(j) generic copies of rDNA-origin peptides (glucagon, liraglutide, teriparatide) via physicochemical and biological sameness.",
        "url": "https://www.fda.gov/media/163018/download",
    },
    {
        "id": "abo-pep-iirmi-assay",
        "name": "Innate Immune Response Modulating Impurities (IIRMIs) in Peptides",
        "category": "Immunogenicity Risk",
        "plain": "Tiny synthesis leftovers or aggregates in peptide shots can trigger unwanted immune alarms—so generic peptides must show no extra innate immune activation.",
        "technical": "FDA's peptide immunogenicity framework evaluates Innate Immune Response Modulating Impurities (IIRMIs) using multiparametric PBMC/cell-based cytokine assays alongside comparative impurity profiling.",
        "url": "https://www.fda.gov/media/166573/download",
    },
    {
        "id": "abo-pep-innate-adaptive",
        "name": "Comparative Impurity & T-Cell Adaptive Immunogenicity Screening",
        "category": "Complex API QC",
        "plain": "If a synthetic peptide has a different impurity fingerprint than the brand drug, labs run human immune-cell proliferation tests to rule out allergy or antibody risk.",
        "technical": "FDA evaluates synthetic vs. rDNA peptide impurity differences through aggregate characterization, innate cytokine panels, and adaptive T-cell proliferation assays (with KLH/CEFT controls).",
        "url": "https://www.fda.gov/media/188010/download",
    },
    {
        "id": "abo-pep-semaglutide-psg",
        "name": "GLP-1 Peptide Product-Specific Guidance (Semaglutide Q1/Q2 & Device)",
        "category": "GLP-1 Generics",
        "plain": "For blockbuster GLP-1 weight-loss and diabetes pens, a generic must match both the exact peptide solution and the injector pen's needle and user interface.",
        "technical": "FDA's Draft PSG on Semaglutide (NDA 215256) specifies Q1/Q2 formulation sameness (±5%) for in vivo BE waiver eligibility, host-cell/synthetic impurity controls, and comparative pen-injector human factors.",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/psg/PSG_215256.pdf",
    },
    {
        "id": "abo-pep-glatiramer-lcms",
        "name": "Complex Peptide Mixtures: LC-MS/MS Fingerprinting (Glatiramer)",
        "category": "Polymer Mixtures",
        "plain": "Some medicines like glatiramer acetate are mixtures of millions of random peptide chains—requiring advanced mass spectrometry to prove generic equivalence.",
        "technical": "GDUFA regulatory science developed high-resolution LC-MS/MS and computational fingerprinting algorithms for complex polypeptide mixtures (glatiramer acetate), enabling first-generic ANDA approvals.",
        "url": "https://www.fda.gov/industry/generic-drug-user-fee-amendments/fys-2013-2017-regulatory-science-report-complex-mixtures-and-peptides",
    },
    {
        "id": "abo-pep-q1-q2-waiver",
        "name": "Synthetic vs. Recombinant Host-Cell Impurity Controls (HCP / DNA)",
        "category": "Process Impurities",
        "plain": "Peptides grown in bacteria or yeast must prove zero leftover host-cell proteins or DNA, whereas chemically synthesized peptides track deletion/oxidation variants.",
        "technical": "FDA distinguishes recombinant peptide process controls (host-cell protein/DNA clearance) from solid-phase peptide synthesis (SPPS) related-substance impurities (diastereomers, truncations, deamidation).",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/psg/PSG_215256.pdf",
    },
]

OLIGONUCLEOTIDE_THERAPEUTICS = [
    {
        "id": "abo-oligo-clinpharm-2024",
        "name": "Clinical Pharmacology for Oligonucleotide Therapeutics (Jul 2024)",
        "category": "RNA / ASO Guidance",
        "plain": "Short synthetic DNA/RNA strands (ASOs and siRNAs) silence disease-causing genes—requiring specialized dosing checks for liver, kidney, and heart safety.",
        "technical": "FDA's Clinical Pharmacology Considerations for Oligonucleotide Therapeutics guidance addresses QTc assessment, immunogenicity, hepatic/renal organ impairment, and CYP/transporter DDI expectations under FD&C Act § 505.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-pharmacology-considerations-development-oligonucleotide-therapeutics",
    },
    {
        "id": "abo-oligo-17-approved",
        "name": "FDA Milestone: 17+ Approved RNA Oligonucleotides (siRNAs & ASOs)",
        "category": "Approved Class",
        "plain": "FDA has approved at least 17 RNA oligonucleotide medicines—including 6 siRNAs and 11 antisense drugs—for rare genetic, liver, and nerve diseases.",
        "technical": "CDER's Oligonucleotide Guidance Recap highlights regulatory lessons across 17 approved RNA therapeutics (6 siRNAs and 11 ASOs), spanning GalNAc-conjugated hepatic delivery and intrathecal CNS dosing.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/guidance-recap-podcast-clinical-pharmacology-considerations-development-oligonucleotide-therapeutics",
    },
    {
        "id": "abo-oligo-n-of-1-ind",
        "name": "N-of-1 Individualized Antisense Oligonucleotide (ASO) INDs",
        "category": "Ultra-Rare N-of-1",
        "plain": "For one-of-a-kind fatal genetic mutations affecting just one or two children, FDA created a special fast-track IND pathway for custom antisense drugs.",
        "technical": "FDA's Individualized ASO Guidance assists academic sponsor-investigators filing INDs for bespoke splice-modulating ASOs treating severely debilitating/life-threatening (SDLT) ultra-rare genetic variants.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/ind-submissions-individualized-antisense-oligonucleotide-drug-products-severely-debilitating-or-life",
    },
    {
        "id": "abo-oligo-n-of-1-nonclin",
        "name": "Nonclinical Testing for Individualized ASOs (Well-Characterized Chemistry)",
        "category": "Streamlined Tox",
        "plain": "When a custom N-of-1 ASO uses a proven chemical backbone (like phosphorothioate 2'-MOE), researchers can run leaner animal safety studies to reach the patient in time.",
        "technical": "FDA's Nonclinical Testing of Individualized ASOs guidance permits streamlined 3-month single-species GLP toxicology when using a well-characterized chemical class with established platform safety.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/nonclinical-testing-individualized-antisense-oligonucleotide-drug-products-severely-debilitating-or",
    },
    {
        "id": "abo-oligo-safety-herg",
        "name": "Nonclinical Safety & hERG / Complement Assessment of Oligonucleotides",
        "category": "Class Toxicities",
        "plain": "Safety testing for antisense and siRNA drugs watches closely for off-target gene binding, platelet drops, complement activation, and kidney/liver accumulation.",
        "technical": "FDA's nonclinical oligonucleotide safety framework evaluates sequence-dependent hybridization off-targets, class-related thrombocytopenia/complement activation, and hERG/QTc considerations.",
        "url": "https://www.fda.gov/media/183496/download",
    },
    {
        "id": "abo-oligo-cmc-nusinersen",
        "name": "Oligonucleotide CMC, Stereoisomers & Generic PSGs (Nusinersen)",
        "category": "Analytical CMC",
        "plain": "Synthesizing RNA drugs creates thousands of mirror-image phosphorothioate isomers and short-mer impurities that require high-res chromatography to control.",
        "technical": "FDA OPQ/OGD addresses oligonucleotide CMC challenges—phosphorothioate diastereomer distributions, (n-1) shortmers, PO impurities, and ion-pair RP-HPLC/HRMS characterization (e.g., nusinersen PSG).",
        "url": "https://www.fda.gov/media/166574/download",
    },
]


def build_adcs_bispecifics_oligos(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "adc_engineering": len(ADC_ENGINEERING),
            "bispecific_antibodies": len(BISPECIFIC_ANTIBODIES),
            "synthetic_peptides": len(SYNTHETIC_PEPTIDES),
            "oligonucleotide_therapeutics": len(OLIGONUCLEOTIDE_THERAPEUTICS),
        },
        "adc_engineering": ADC_ENGINEERING,
        "bispecific_antibodies": BISPECIFIC_ANTIBODIES,
        "synthetic_peptides": SYNTHETIC_PEPTIDES,
        "oligonucleotide_therapeutics": OLIGONUCLEOTIDE_THERAPEUTICS,
    }
    (data_dir / "adcs_bispecifics_oligos.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_adcs_bispecifics_oligos.py <site/data>")
    print(json.dumps(build_adcs_bispecifics_oligos(pathlib.Path(sys.argv[1])), indent=2))
'''

ADCS_BISPECIFICS_OLIGOS_JS = '''// Pill by Pill v6.2i: ADCs, Bispecific Antibodies, Synthetic Peptides & Oligonucleotide Therapeutics Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["adcs", "Antibody-Drug Conjugates", "adc_engineering"],
  ["bispecifics", "Bispecific Antibodies", "bispecific_antibodies"],
  ["peptides", "Synthetic Peptides & GLP-1", "synthetic_peptides"],
  ["oligos", "Oligonucleotides (ASO / siRNA)", "oligonucleotide_therapeutics"],
];

function adcsBispecificsOligosSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Targeted modality classes: Antibody-Drug Conjugates, Bispecific Antibodies, Synthetic Peptides, and Oligonucleotide Therapeutics">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. ADCs</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">mAb + Linker + Payload</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Multi-Analyte PK &amp; QTc</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#abo-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Bispecifics</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">CD3 T-Cell Engagers</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">MABEL &amp; Step-Up Dosing</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#abo-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Peptides &amp; GLP-1</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">SPPS vs. rDNA Sameness</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">IIRMI &amp; Q1/Q2 Pens</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#abo-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. ASOs &amp; siRNAs</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">GalNAc &amp; Intrathecal</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">N-of-1 Ultra-Rare INDs</text>
      <defs><marker id="abo-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Targeted therapeutic modalities bridge small-molecule chemistry and biologics across ADCs, bispecific T-cell engagers, synthetic peptides, and RNA oligonucleotides.</figcaption>
  </figure>`;
}

export async function adcsBispecificsOligosPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/adcs_bispecifics_oligos.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/adcs-bispecifics-oligos" : "#/ref/adcs-bispecifics-oligos";

  const pills = html`<div class="chips" role="navigation" aria-label="ADCs, bispecifics, peptides, and oligonucleotide sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Modality / Guidance</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${adcsBispecificsOligosSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA ADC Clinical Pharmacology, Bispecific Antibody Development, Synthetic Peptide ANDA/Immunogenicity, and Oligonucleotide Therapeutics documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["ADCs, Bispecifics, Peptides & Oligos"]] : [REF_HOME, ["ADCs, Bispecifics, Peptides & Oligos"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "ADCs, Bispecific Antibodies, Synthetic Peptides & Oligonucleotides",
      lede: env === "explore"
        ? "How antibody-drug conjugates deliver chemo payloads, how bispecifics rally T-cells, and how synthetic peptides and gene-silencing RNA drugs are tested."
        : "ADC multi-analyte PK/QTc/DDI, Bispecific MABEL & CDR sameness, Synthetic Peptide ANDA/IIRMI immunogenicity, and Oligonucleotide (siRNA/ASO/N-of-1) clinical pharmacology.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on ADCs, bispecifics, peptides, and oligonucleotides.", href: env === "explore" ? "#/ref/adcs-bispecifics-oligos" : "#/explore/adcs-bispecifics-oligos" },
        { title: "Oncology OCE & Master Protocols", text: "Project Optimus, Orbis, RTOR, and Accelerated Approval in oncology.", href: "#/ref/oncology-oce" },
        { title: "Biologics, Cell & Gene Therapy", text: "mAbs, biosimilars, AAV gene therapies, and CAR-T manufacturing.", href: "#/ref/atmp" },
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
    if 'adcs_bispecifics_oligos.js' not in txt:
        for anchor in ('import * as gcpBimoCdisc from "./gcp_bimo_cdisc.js";\n', 'import * as oncologyOce from "./oncology_oce.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as adcsBispecificsOligos from "./adcs_bispecifics_oligos.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as adcsBispecificsOligos from "./adcs_bispecifics_oligos.js";\n' + txt
            changed = True
    if '"/ref/adcs-bispecifics-oligos"' not in txt:
        for anchor in ('if (path === "/ref/gcp-bimo-cdisc")', 'if (path === "/ref/oncology-oce")', 'if (path === "/ref/atmp")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/adcs-bispecifics-oligos") return { env: "ref", current: "#/ref/adcs-bispecifics-oligos", ...(await adcsBispecificsOligos.adcsBispecificsOligosPage(query, "ref")) };\n  if (path === "/explore/adcs-bispecifics-oligos") return { env: "explore", current: "#/explore/adcs-bispecifics-oligos", ...(await adcsBispecificsOligos.adcsBispecificsOligosPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/adcs-bispecifics-oligos" not in txt:
        for anchor in ('["#/ref/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]', '["#/ref/oncology-oce", "Oncology OCE & master trials"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]', 1)
                changed = True
                break
    if "#/explore/adcs-bispecifics-oligos" not in txt:
        for anchor in ('["#/explore/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]', '["#/explore/oncology-oce", "Oncology OCE & master trials"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_adcs_bispecifics_oligos.py" in txt:
        return False
    line = "python3 pipeline/build_adcs_bispecifics_oligos.py site/data\n"
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
    if '"/api/adcs-bispecifics-oligos"' in txt:
        return False
    route = (
        '\n@app.get("/api/adcs-bispecifics-oligos")\n'
        'def api_adcs_bispecifics_oligos():\n'
        '    p = DATA_DIR / "adcs_bispecifics_oligos.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "adcs_bispecifics_oligos.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"adcs_bispecifics_oligos.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    abo_ref = _load(data_dir / "adcs_bispecifics_oligos.json", {}) or {}\n'
        '    for sec_key, sec_q in [("adc_engineering", "adcs"), ("bispecific_antibodies", "bispecifics"), ("synthetic_peptides", "peptides"), ("oligonucleotide_therapeutics", "oligos")]:\n'
        '        for item in (abo_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "adcs_bispecifics_oligos",\n'
        '                "group": "ADCs, Bispecifics, Peptides & Oligonucleotides",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/adcs-bispecifics-oligos?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/adcs-bispecifics-oligos?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"ADC antibody drug conjugate payload linker bispecific CD3 MABEL CRS synthetic peptide GLP-1 semaglutide IIRMI oligonucleotide ASO siRNA GalNAc N-of-1 {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"adcs-bispecifics-oligos", "#/ref/adcs-bispecifics-oligos"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    abo_doc = _load_json(data_dir / "adcs_bispecifics_oligos.json")\n'
        '    if isinstance(abo_doc, dict) and abo_doc.get("adc_engineering"):\n'
        '        abo_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (abo_doc.get("adc_engineering") or []) + (abo_doc.get("oligonucleotide_therapeutics") or []))\n'
        '        pages.append(("adcs-bispecifics-oligos", "#/ref/adcs-bispecifics-oligos", "ADCs, Bispecific Antibodies, Synthetic Peptides & Oligonucleotides",\n'
        '                      "Primary-sourced guide to ADC clinical pharmacology, bispecific T-cell engagers, synthetic peptide ANDA/IIRMI sameness, and ASO/siRNA oligonucleotide therapeutics.",\n'
        '                      f"<ul>{abo_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/adcs-bispecifics-oligos"' in txt:
        return False
    for anchor in ('    "/#/explore/gcp-bimo-cdisc",', '    "/#/explore/oncology-oce",', '    "/#/explore/excipients-dmfs-nano",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/adcs-bispecifics-oligos",\n    "/#/explore/adcs-bispecifics-oligos",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_adcs_bispecifics_oligos_py": _write_if_changed(pipe_dir / "build_adcs_bispecifics_oligos.py", BUILD_ADCS_BISPECIFICS_OLIGOS_PY),
        "adcs_bispecifics_oligos_js": _write_if_changed(js_dir / "adcs_bispecifics_oligos.js", ADCS_BISPECIFICS_OLIGOS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/gcp-bimo-cdisc") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]] }];\nconst EXPLORE_NAV = [["#/explore/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/gcp-bimo-cdisc",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_adcs_bispecifics_oligos.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_adcs_bispecifics_oligos.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"adc_engineering": 6, "bispecific_antibodies": 6, "synthetic_peptides": 6, "oligonucleotide_therapeutics": 6}, out

        doc = json.loads((root / "site" / "data" / "adcs_bispecifics_oligos.json").read_text(encoding="utf-8"))
        for k in ("adc_engineering", "bispecific_antibodies", "synthetic_peptides", "oligonucleotide_therapeutics"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "adcs_bispecifics_oligos.js").read_text(encoding="utf-8")
        print("V62I_ADCS_BISPECIFICS_OLIGOS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2i ADCs, Bispecifics, Peptides & Oligonucleotides patch.")
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
