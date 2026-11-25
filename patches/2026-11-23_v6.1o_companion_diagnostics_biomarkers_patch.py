#!/usr/bin/env python3
"""Pill by Pill v6.1o Patch: Companion Diagnostics, Biomarkers & Precision Medicine Reference (#/ref/diagnostics, #/explore/diagnostics, /api/diagnostics).

1. Adds `pipeline/build_diagnostics.py` -> `site/data/diagnostics.json` (6 CDx regulatory frameworks,
   6 BEST biomarker categories & qualification pathways, 6 molecular/tissue assay platforms, and
   6 precision oncology & pharmacogenomics pillars — 24 primary-sourced entries).
2. Adds `site/js/diagnostics.js` (`diagnosticsPage` with inline Drug–Diagnostic Codevelopment SVG +
   4 section filters) and wires `#/ref/diagnostics`, `#/explore/diagnostics`, `/api/diagnostics`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `diagnostics.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/diagnostics/` static SEO page + sitemap entry -> 31
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1o_companion_diagnostics_biomarkers_patch.py --selftest
  python3 2026-11-23_v6.1o_companion_diagnostics_biomarkers_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_DIAGNOSTICS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1o Companion Diagnostics, Biomarkers & Precision Medicine Reference (`site/data/diagnostics.json`).

Comprehensive, primary-sourced reference covering:
  1. Companion Diagnostics (CDx) & Regulatory Frameworks (6 pillars)
  2. BEST Biomarker Categories & FDA Qualification (6 pillars)
  3. Molecular, Tissue & Liquid Biopsy Assay Platforms (6 pillars)
  4. Precision Oncology, Pharmacogenomics & LDT Oversight (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA, NIH/NCBI BEST, EU Commission/EMA).

Usage:
  python3 pipeline/build_diagnostics.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

CDX_FRAMEWORKS = [
    {
        "id": "cdx-ivd-definition",
        "name": "In Vitro Companion Diagnostic Devices (2014 Final Guidance)",
        "scope": "US FDA (CDRH / CDER / CBER)",
        "plain": "A companion diagnostic is a lab test or imaging tool that is essential before giving a targeted medicine—confirming the drug will work for that patient or avoiding a severe side effect.",
        "technical": "Defined by FDA's August 2014 Final Guidance as an IVD essential for the safe and effective use of a corresponding therapeutic product: identifying likely responders, patients at increased serious adverse-event risk, or monitoring treatment response for dose/schedule adjustment.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/in-vitro-companion-diagnostic-devices",
    },
    {
        "id": "cdx-codevelopment",
        "name": "Contemporaneous Drug–Device Codevelopment (Draft Guidance)",
        "scope": "US FDA Parallel Review",
        "plain": "Drugmakers and test-makers usually develop and test the medicine and its diagnostic together so both can be approved on the same day—preventing a drug launch with no validated way to pick patients.",
        "technical": "FDA's Draft Guidance on Principles for Codevelopment recommends analytical validation (precision, LoD, PPA/NPA) prior to pivotal clinical trial enrollment and contemporaneous PMA/De Novo/510(k) approval alongside the NDA/BLA.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/principles-codevelopment-in-vitro-companion-diagnostic-device-therapeutic-product",
    },
    {
        "id": "cdx-group-labeling",
        "name": "Oncology Class / Group CDx Labeling (2020 Final Guidance)",
        "scope": "US FDA Oncology",
        "plain": "Instead of forcing a separate diagnostic approval for every single drug in the same class (like five different EGFR lung-cancer pills), FDA allows one test label to cover an entire therapeutic group.",
        "technical": "Facilitates broader CDx labeling referencing a specific group or class of oncology therapeutic products (e.g., EGFR exon 19 deletions / L858R TKIs in NSCLC) when analytical and clinical evidence supports class-wide biomarker concordance.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/developing-and-labeling-in-vitro-companion-diagnostic-devices-specific-group-oncology-therapeutic",
    },
    {
        "id": "cdx-oncology-pilot",
        "name": "Oncology Drug Products Used with Certain IVDs Pilot (2023)",
        "scope": "US FDA CDER / OCE",
        "plain": "When a clinical lab test (not a commercial kit) is used in a cancer drug trial, FDA's pilot program publishes minimum test performance targets so certified labs can safely run equivalent assays.",
        "technical": "Voluntary FDA pilot program for certain CDER-regulated oncology drugs where clinical trial enrollment relied on local/LDT assays; FDA posts minimum analytical performance characteristics on its website to guide transparent clinical laboratory testing.",
        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/oncology-drug-products-used-certain-in-vitro-diagnostics-pilot-program",
    },
    {
        "id": "cdx-eu-ivdr",
        "name": "EU IVDR (Regulation (EU) 2017/746) — Class C & EMA Consultation",
        "scope": "European Union",
        "plain": "Under Europe's updated diagnostic rules, companion diagnostics cannot be self-certified anymore: an independent Notified Body and the European Medicines Agency (EMA) must review the link to the drug.",
        "technical": "EU IVDR classifies companion diagnostics as Class C devices (Annex VIII Rule 3(f)), requiring Notified Body conformity assessment plus formal scientific consultation with EMA (or a national competent authority) on the suitability of the CDx for the medicinal product.",
        "url": "https://health.ec.europa.eu/medical-devices-vitro-diagnostics_en",
    },
    {
        "id": "cdx-authorized-list",
        "name": "FDA-Authorized Companion Diagnostic Devices Registry",
        "scope": "PMA / 510(k) / De Novo",
        "plain": "FDA maintains a public master table of every cleared or approved companion diagnostic—from single-gene PCR kits to 300-gene tumor sequencing panels—paired with each matching drug.",
        "technical": "Public registry of FDA-authorized IVD and imaging companion diagnostics, specifying device name, PMA/510(k) number, intended biomarker/alteration, specimen type (tissue vs. plasma ctDNA), and linked therapeutic product(s) or oncology class.",
        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools",
    },
]

BIOMARKER_CATEGORIES = [
    {
        "id": "bm-best-cou",
        "name": "FDA–NIH BEST Glossary & Context of Use (COU)",
        "scope": "Foundational Taxonomy",
        "plain": "A biomarker is any measurable biological clue—like blood pressure, a mutated gene, or a blood protein—and regulators require sponsors to state its exact Context of Use before relying on it in a trial.",
        "technical": "The FDA-NIH BEST (Biomarkers, EndpointS, and other Tools) resource standardizes 7 biomarker categories (susceptibility/risk, diagnostic, monitoring, prognostic, predictive, pharmacodynamic/response, safety) and defines Context of Use = [BEST category] + [drug development use].",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK338448/",
    },
    {
        "id": "bm-predictive",
        "name": "Predictive & Patient-Selection Biomarkers",
        "scope": "Efficacy Enrichment",
        "plain": "Predictive biomarkers answer 'Who will this drug help?'—for example, HER2 overexpression for trastuzumab or BRAF V600E mutations for targeted melanoma therapy.",
        "technical": "Identifies individuals more likely than similar patients without the biomarker to experience a favorable (or unfavorable) effect from a medical product; forms the biological basis for enrichment trial designs and CDx labeling.",
        "url": "https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification",
    },
    {
        "id": "bm-prognostic-dx",
        "name": "Prognostic vs. Diagnostic Biomarkers",
        "scope": "Disease Course vs. Detection",
        "plain": "A diagnostic biomarker confirms what disease a patient has, while a prognostic biomarker forecasts how aggressive that disease is likely to be—even without treatment.",
        "technical": "Diagnostic biomarkers detect or confirm presence of a disease or subtype (e.g., BCR-ABL1 in CML); prognostic biomarkers indicate likelihood of a clinical event, recurrence, or progression independent of therapy (e.g., IGHV unmutated status in CLL).",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK338448/",
    },
    {
        "id": "bm-pd-surrogate",
        "name": "Pharmacodynamic (PD) & Surrogate Endpoint Biomarkers",
        "scope": "Target Engagement & Accelerated Approval",
        "plain": "PD biomarkers prove a drug actually hit its target in the body, while validated surrogate endpoints (like HIV viral load or LDL cholesterol) can stand in for long survival trials.",
        "technical": "PD/response biomarkers show biological response to an intervention (e.g., receptor occupancy, p-ERK inhibition); a subset meeting strict clinical-trial correlation criteria become reasonably likely or validated surrogate endpoints under 21 CFR 314.510 / 601.41.",
        "url": "https://www.fda.gov/drugs/biomarker-qualification-program/context-use",
    },
    {
        "id": "bm-safety",
        "name": "Safety & Toxicity Biomarkers",
        "scope": "Organ Protection & Dose Limiting",
        "plain": "Safety biomarkers act as early warning lights—spotting kidney, liver, or heart stress in blood or urine before permanent organ damage occurs.",
        "technical": "Measured before or after exposure to indicate likelihood, presence, or extent of toxicity (e.g., ALT/bilirubin for DILI/Hy's Law, urinary KIM-1/clusterin for renal tubular injury, high-sensitivity troponin for cardiotoxicity).",
        "url": "https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification",
    },
    {
        "id": "bm-bqp",
        "name": "FDA Biomarker Qualification Program (21st Century Cures Act)",
        "scope": "Drug Development Tool (DDT)",
        "plain": "Once FDA qualifies a biomarker through its 3-step public review, any drug company can use it in trials for that purpose without re-proving the science from scratch.",
        "technical": "Statutory 3-stage DDT qualification pathway (Letter of Intent -> Qualification Plan -> Full Qualification Package) under FD&C Act § 507; qualified biomarkers are publicly posted for industry-wide use within their specified COU.",
        "url": "https://www.fda.gov/drugs/drug-development-tool-ddt-qualification-programs/biomarker-qualification-program",
    },
]

ASSAY_PLATFORMS = [
    {
        "id": "plat-ngs",
        "name": "Next-Generation Sequencing (NGS) & Comprehensive Genomic Profiling",
        "scope": "Broad DNA/RNA Panels",
        "plain": "Instead of testing one gene at a time on tiny biopsy samples, NGS reads hundreds of cancer or inherited-disease genes in a single run—finding rare mutations, fusions, and tumor mutational burden.",
        "technical": "Massively parallel sequencing (hybrid-capture or amplicon) detecting SNVs, indels, CNVs, gene fusions, MSI, and TMB simultaneously. FDA 2018 NGS guidance sets analytical validation standards using PPA, NPA, and technical positive predictive value (TPPV).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-design-development-and-analytical-validation-next-generation-sequencing-ngs-based",
    },
    {
        "id": "plat-liquid-biopsy",
        "name": "Liquid Biopsy (ctDNA) & Minimal Residual Disease (MRD)",
        "scope": "Plasma Cell-Free DNA",
        "plain": "A simple blood draw can catch tiny fragments of tumor DNA shed into the bloodstream—guiding targeted therapy when a tissue biopsy is too risky or tracking whether cancer is creeping back.",
        "technical": "Ultra-deep sequencing or digital PCR of circulating tumor DNA (ctDNA) in plasma; requires high analytical sensitivity (VAF down to 0.1–0.5%) and tissue-concordance bridging because negative plasma results often reflex to tissue testing.",
        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools",
    },
    {
        "id": "plat-ihc",
        "name": "Immunohistochemistry (IHC) & Protein Expression Scoring",
        "scope": "FFPE Tissue Pathology",
        "plain": "Pathologists stain thin tumor slices with glowing or colored antibodies to see if a target protein—like HER2 or PD-L1—sits on the cancer cell surface.",
        "technical": "Semi-quantitative antibody-based staining of formalin-fixed paraffin-embedded (FFPE) tissue scored by validated algorithms (e.g., HER2 0/1+/2+/3+ or PD-L1 TPS/CPS cutoffs); sensitive to pre-analytical fixation time and clone-specific antibody harmonization.",
        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/companion-diagnostics",
    },
    {
        "id": "plat-pcr",
        "name": "Real-Time PCR (qPCR) & Digital Droplet PCR (ddPCR)",
        "scope": "Targeted Hotspot Assays",
        "plain": "Fast, focused PCR tests amplify specific DNA hotspots—like BRAF V600E or EGFR L858R—delivering answers in hours to a couple of days when patients need rapid treatment decisions.",
        "technical": "Targeted allele-specific amplification (qPCR) or partition-based absolute quantification (ddPCR); lower multiplexing than NGS but rapid turnaround time, lower input DNA requirements, and straightforward analytical cutoff verification.",
        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools",
    },
    {
        "id": "plat-fish",
        "name": "FISH & Cytogenetic Rearrangement Assays",
        "scope": "Gene Fusions & Amplifications",
        "plain": "Fluorescent DNA probes light up broken or extra gene copies directly inside intact cells under a microscope—classic tools for ALK, ROS1, or HER2 gene amplification.",
        "technical": "Fluorescence in situ hybridization (break-apart or dual-color copy-number probes) on FFPE sections; detects structural chromosomal rearrangements and gene copy amplification with single-cell spatial resolution.",
        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools",
    },
    {
        "id": "plat-analytical-val",
        "name": "Analytical & Clinical Validation Metrics (PPA, NPA, LoD, TPPV)",
        "scope": "Performance Benchmarks",
        "plain": "Before a diagnostic can guide real prescriptions, developers must prove it finds true positives reliably (PPA), avoids false alarms (NPA), and works down to trace sample levels (LoD).",
        "technical": "Core IVD validation triad: Analytical Validity (LoD, precision/reproducibility, interference, PPA/NPA against orthogonal reference), Clinical Validity (sensitivity/specificity/PPV/NPV for clinical phenotype), and Clinical Utility (improved patient outcomes).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-design-development-and-analytical-validation-next-generation-sequencing-ngs-based",
    },
]

PRECISION_PGX = [
    {
        "id": "pgx-fda-table",
        "name": "FDA Table of Pharmacogenetic Associations (Sections 1–3)",
        "scope": "Prescriber Reference",
        "plain": "FDA publishes a curated table showing which gene-drug pairs require dose changes or alternative drugs (Section 1), which flag safety risks (Section 2), and which only alter blood levels (Section 3).",
        "technical": "Three-tier evidence table maintained by FDA: Section 1 (Data support therapeutic management recommendations, e.g., CYP2C19/clopidogrel, DPYD/fluorouracil, TPMT/azathioprine), Section 2 (Potential impact on safety/response), Section 3 (PK impact only).",
        "url": "https://www.fda.gov/medical-devices/precision-medicine/table-pharmacogenetic-associations",
    },
    {
        "id": "pgx-dme",
        "name": "Drug-Metabolizing Enzyme Phenotypes (CYP2C19, CYP2D6, DPYD, TPMT)",
        "scope": "Metabolism & Toxicity",
        "plain": "Because people inherit fast or slow versions of liver enzymes, a standard dose can fail to activate a prodrug (like clopidogrel) or build up to toxic levels (like 5-FU or thiopurines).",
        "technical": "Star-allele diplotypes map to Poor, Intermediate, Normal, Rapid, or Ultrarapid Metabolizer phenotypes. Key actionable examples: CYP2C19 PM (clopidogrel reduced active metabolite), DPYD deficiency (severe capecitabine/5-FU toxicity), and TPMT/NUDT15 (myelosuppression).",
        "url": "https://www.fda.gov/medical-devices/precision-medicine/table-pharmacogenetic-associations",
    },
    {
        "id": "pgx-hla",
        "name": "HLA Hypersensitivity Screening (HLA-B*57:01 & HLA-B*15:02)",
        "scope": "Immune-Mediated SCARs",
        "plain": "A quick genetic cheek swab or blood test before starting abacavir or carbamazepine prevents life-threatening immune skin reactions in patients carrying specific HLA tissue-type variants.",
        "technical": "Classic safety pharmacogenomics: HLA-B*57:01 screening is mandatory before abacavir to prevent hypersensitivity syndrome, and HLA-B*15:02 testing (enriched in Asian ancestry) is recommended before carbamazepine/oxcarbazepine to prevent SJS/TEN.",
        "url": "https://www.fda.gov/medical-devices/precision-medicine/table-pharmacogenetic-associations",
    },
    {
        "id": "pgx-variant-db",
        "name": "FDA Recognition of Public Human Genetic Variant Databases",
        "scope": "Evidence Standardization",
        "plain": "Instead of every lab re-inventing evidence for millions of DNA letters, FDA formally recognizes vetted public genetic databases (like ClinGen) as valid clinical evidence for test approvals.",
        "technical": "FDA recognition program allowing NGS/genetic test developers to cite FDA-recognized public human genetic variant databases (supporting clinical validity assertions for germline/somatic variants) in premarket submissions.",
        "url": "https://www.fda.gov/medical-devices/precision-medicine/fda-recognition-public-human-genetic-variant-databases",
    },
    {
        "id": "pgx-ldts",
        "name": "Laboratory Developed Tests (LDTs) & CLIA High-Complexity Labs",
        "scope": "Clinical Lab Oversight",
        "plain": "Many hospital and specialty lab tests are built and run inside a single CLIA-certified lab rather than sold as factory kits—creating an evolving regulatory bridge between CLIA lab quality and FDA device review.",
        "technical": "LDTs are IVDs designed, manufactured, and used within a single high-complexity CLIA-certified laboratory (42 CFR Part 493). FDA's LDT policy framework addresses clinical validity, adverse-event reporting, and targeted enforcement discretion for unmet-need health-system LDTs.",
        "url": "https://www.fda.gov/medical-devices/in-vitro-diagnostics/laboratory-developed-tests",
    },
    {
        "id": "pgx-tumor-agnostic",
        "name": "Tissue-Agnostic Biomarker Approvals (MSI-H, NTRK, RET, BRAF)",
        "scope": "Molecularly Defined Indications",
        "plain": "Modern oncology increasingly approves drugs based on a tumor's DNA signature—like MSI-High or NTRK fusions—regardless of whether the cancer started in the colon, lung, or thyroid.",
        "technical": "Biomarker-defined basket indications spanning solid tumors (e.g., pembrolizumab for MSI-H/dMMR or TMB-H; larotrectinib/entrectinib for NTRK fusions; selpercatinib for RET fusions), typically paired with broad NGS companion diagnostics.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/precision-oncology-program",
    },
]


def build_diagnostics(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "cdx_frameworks": len(CDX_FRAMEWORKS),
            "biomarker_categories": len(BIOMARKER_CATEGORIES),
            "assay_platforms": len(ASSAY_PLATFORMS),
            "precision_pgx": len(PRECISION_PGX),
        },
        "cdx_frameworks": CDX_FRAMEWORKS,
        "biomarker_categories": BIOMARKER_CATEGORIES,
        "assay_platforms": ASSAY_PLATFORMS,
        "precision_pgx": PRECISION_PGX,
    }
    (data_dir / "diagnostics.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_diagnostics.py <site/data>")
    print(json.dumps(build_diagnostics(pathlib.Path(sys.argv[1])), indent=2))
'''

DIAGNOSTICS_JS = '''// Pill by Pill v6.1o: Companion Diagnostics, Biomarkers & Precision Medicine Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["cdx", "CDx & Regulation", "cdx_frameworks"],
  ["biomarkers", "BEST Biomarkers", "biomarker_categories"],
  ["assays", "Assay Platforms", "assay_platforms"],
  ["pgx", "Pharmacogenomics & LDTs", "precision_pgx"],
];

function codevelopmentSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Drug and Companion Diagnostic contemporaneous codevelopment flow">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Biomarker Discovery</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">BEST Context of Use</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Prototype CTA / NGS</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#dx-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Analytical Validation</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Cutoff Lock &amp; LoD</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">PPA / NPA / Precision</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#dx-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Pivotal Bridging</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Enrichment Clinical Trial</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Clinical Validity &amp; Utility</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#dx-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Joint Approval</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">NDA/BLA + PMA/510(k)</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">EU IVDR Class C + EMA</text>
      <defs><marker id="dx-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Contemporaneous drug–diagnostic codevelopment aligns analytical validation, clinical trial bridging, and paired regulatory approval.</figcaption>
  </figure>`;
}

export async function diagnosticsPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/diagnostics.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/diagnostics" : "#/ref/diagnostics";

  const pills = html`<div class="chips" role="navigation" aria-label="Diagnostics sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Topic / Standard</th><th>Scope</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.scope}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${codevelopmentSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA, NIH/NCBI BEST, and European Commission/EMA primary documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Diagnostics & Biomarkers"]] : [REF_HOME, ["Diagnostics & Biomarkers"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Companion Diagnostics, Biomarkers & Precision Medicine",
      lede: env === "explore"
        ? "How doctors and drugmakers test DNA, proteins, and blood markers to match the right medicine to the right patient."
        : "FDA/IVDR companion diagnostic frameworks, BEST biomarker qualification, NGS/liquid-biopsy assays, and pharmacogenomics.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on diagnostics and biomarkers.", href: env === "explore" ? "#/ref/diagnostics" : "#/explore/diagnostics" },
        { title: "Clinical Trial Design & Endpoints", text: "Biomarker enrichment, surrogate endpoints, and adaptive designs.", href: "#/ref/trials" },
        { title: "Regulatory Pathways & Exclusivity", text: "Accelerated approval, breakthrough therapy, and CDER/CBER review.", href: "#/ref/pathways" },
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
    if 'diagnostics.js' not in txt:
        for anchor in ('import * as globalRegHta from "./global_reg_hta.js";\n', 'import * as sterileMfg from "./sterile_mfg.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as diagnostics from "./diagnostics.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as diagnostics from "./diagnostics.js";\n' + txt
            changed = True
    if '"/ref/diagnostics"' not in txt:
        for anchor in ('if (path === "/ref/global-reg")', 'if (path === "/ref/sterile")', 'if (path === "/ref/ip")', 'if (path === "/ref/safety")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/diagnostics") return { env: "ref", current: "#/ref/diagnostics", ...(await diagnostics.diagnosticsPage(query, "ref")) };\n  if (path === "/explore/diagnostics") return { env: "explore", current: "#/explore/diagnostics", ...(await diagnostics.diagnosticsPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/diagnostics" not in txt:
        for anchor in ('["#/ref/global-reg", "Global reg & HTA"]', '["#/ref/sterile", "Sterile & bioprocessing"]', '["#/ref/ip", "IP & patents"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/diagnostics", "Diagnostics & CDx"]', 1)
                changed = True
                break
    if "#/explore/diagnostics" not in txt:
        for anchor in ('["#/explore/global-reg", "Global reg & HTA"]', '["#/explore/sterile", "Sterile & bioprocessing"]', '["#/explore/ip", "IP & patents"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/diagnostics", "Diagnostics & CDx"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_diagnostics.py" in txt:
        return False
    line = "python3 pipeline/build_diagnostics.py site/data\n"
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
    if '"/api/diagnostics"' in txt:
        return False
    route = (
        '\n@app.get("/api/diagnostics")\n'
        'def api_diagnostics():\n'
        '    p = DATA_DIR / "diagnostics.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "diagnostics.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"diagnostics.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    dx_ref = _load(data_dir / "diagnostics.json", {}) or {}\n'
        '    for sec_key, sec_q in [("cdx_frameworks", "cdx"), ("biomarker_categories", "biomarkers"), ("assay_platforms", "assays"), ("precision_pgx", "pgx")]:\n'
        '        for item in (dx_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "diagnostics",\n'
        '                "group": "Diagnostics & Biomarkers",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/diagnostics?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/diagnostics?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"companion diagnostic CDx biomarker BEST NGS liquid biopsy ctDNA pharmacogenomics LDT IVDR {sec_key} {item.get(\'name\', \'\')} {item.get(\'scope\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"diagnostics", "#/ref/diagnostics"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    dx_doc = _load_json(data_dir / "diagnostics.json")\n'
        '    if isinstance(dx_doc, dict) and dx_doc.get("cdx_frameworks"):\n'
        '        dx_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (dx_doc.get("cdx_frameworks") or []) + (dx_doc.get("precision_pgx") or []))\n'
        '        pages.append(("diagnostics", "#/ref/diagnostics", "Companion Diagnostics, Biomarkers & Precision Medicine",\n'
        '                      "Primary-sourced guide to FDA/EU IVDR companion diagnostics, BEST biomarker qualification, NGS/liquid-biopsy platforms, and pharmacogenomics.",\n'
        '                      f"<ul>{dx_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/diagnostics"' in txt:
        return False
    for anchor in ('    "/#/explore/global-reg",', '    "/#/explore/sterile",', '    "/#/explore/ip",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/diagnostics",\n    "/#/explore/diagnostics",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_diagnostics_py": _write_if_changed(pipe_dir / "build_diagnostics.py", BUILD_DIAGNOSTICS_PY),
        "diagnostics_js": _write_if_changed(js_dir / "diagnostics.js", DIAGNOSTICS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/global-reg") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/global-reg", "Global reg & HTA"]] }];\nconst EXPLORE_NAV = [["#/explore/global-reg", "Global reg & HTA"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/global-reg",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_diagnostics.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_diagnostics.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"cdx_frameworks": 6, "biomarker_categories": 6, "assay_platforms": 6, "precision_pgx": 6}, out

        doc = json.loads((root / "site" / "data" / "diagnostics.json").read_text(encoding="utf-8"))
        for k in ("cdx_frameworks", "biomarker_categories", "assay_platforms", "precision_pgx"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "diagnostics.js").read_text(encoding="utf-8")
        print("V61O_COMPANION_DIAGNOSTICS_BIOMARKERS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1o Companion Diagnostics & Biomarkers patch.")
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
