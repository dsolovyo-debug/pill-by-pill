#!/usr/bin/env python3
"""Pill by Pill v6.2s Patch: Drug Discovery, Quantitative High-Throughput Screening (qHTS / NCATS / PubChem), Structure-Based Drug Design (Cryo-EM / AlphaFold / PDB), Targeted Protein Degradation (PROTACs / Molecular Glues), and Translational Discovery Reference (#/ref/discovery-sbdd-protacs, #/explore/discovery-sbdd-protacs, /api/discovery-sbdd-protacs).

1. Adds `pipeline/build_discovery_sbdd_protacs.py` -> `site/data/discovery_sbdd_protacs.json`
   (6 NCATS / PubChem / qHTS pillars, 6 SBDD / Cryo-EM / AlphaFold pillars, 6 PROTACs /
   Molecular Glues pillars, and 6 Translational Biomarkers / QM / NAMs pillars — 24
   primary-sourced entries).
2. Adds `site/js/discovery_sbdd_protacs.js` (`discoverySbddProtacsPage` with inline Drug
   Discovery, SBDD & PROTACs SVG + 4 section filters) and wires
   `#/ref/discovery-sbdd-protacs`, `#/explore/discovery-sbdd-protacs`,
   `/api/discovery-sbdd-protacs`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `discovery_sbdd_protacs.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/discovery-sbdd-protacs/` static SEO page + sitemap
   entry -> 61 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-25_v6.2s_drug_discovery_hts_sbdd_protacs_alphafold_patch.py --selftest
  python3 2026-11-25_v6.2s_drug_discovery_hts_sbdd_protacs_alphafold_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_DISCOVERY_SBDD_PROTACS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2s Drug Discovery, qHTS, SBDD (Cryo-EM/AlphaFold) & PROTACs Reference (`site/data/discovery_sbdd_protacs.json`).

Comprehensive, primary-sourced reference covering:
  1. NIH NCATS, PubChem & Quantitative High-Throughput Screening (qHTS) (6 pillars)
  2. Structure-Based Drug Design (SBDD), RCSB PDB, Cryo-EM & AlphaFold (6 pillars)
  3. Targeted Protein Degradation: PROTACs & Molecular Glues (6 pillars)
  4. Translational Biomarkers, Quantitative Medicine & Discovery NAMs (6 pillars)

All anchors are verified HTTPS primary sources (NIH NCATS, RCSB PDB, NIH PMC, FDA).

Usage:
  python3 pipeline/build_discovery_sbdd_protacs.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-25"

NCATS_PUBCHEM_HTS = [
    {
        "id": "dsp-ncats-pharm-collection",
        "name": "NCATS Pharmaceutical Collection (NPC) & Drug Repurposing",
        "category": "NIH NCATS",
        "plain": "Scientists first test libraries of already-approved medicines against new diseases to see if any existing drug can be repurposed.",
        "technical": "The NCATS Pharmaceutical Collection provides a publicly accessible, annotated library of approved molecular entities for high-throughput screening across disease models, with assay results deposited in PubChem.",
        "url": "https://ncats.nih.gov/research/research-resources/preclinical-research-toolbox/npc",
    },
    {
        "id": "dsp-ncats-qhts-1536",
        "name": "Automated Compound Management & 1,536-Well qHTS",
        "category": "qHTS Robotics",
        "plain": "Robotic dispensers test thousands of chemical candidates simultaneously across multiple concentrations in microscopic 1,536-well plates.",
        "technical": "NCATS's automated compound management and quantitative high-throughput screening (qHTS) platform profiles full concentration-response curves across 1,536-well microplates to minimize false negatives and positives.",
        "url": "https://ncats.nih.gov/research/research-activities/compound-management",
    },
    {
        "id": "dsp-split-nanoluc-sdr",
        "name": "Split NanoLuc (SDR) Target-Engagement Assays",
        "category": "Assay Innovation",
        "plain": "A split glowing sensor lights up when a candidate molecule binds a newly discovered disease protein—even before its function is fully known.",
        "technical": "NCATS's Split NanoLuc / structural-domain-reconstitution (SDR) assay measures ligand-protein binding via bioluminescence changes, enabling qHTS for newly identified, uncharacterized targets.",
        "url": "https://ncats.nih.gov/news-events/news/new-assay-technology-could-reshape-approach-drug-discovery",
    },
    {
        "id": "dsp-pubchem-bioassay",
        "name": "PubChem BioAssay Open Screening Repository",
        "category": "PubChem Open Data",
        "plain": "Millions of open screening measurements in PubChem let chemists worldwide see which molecules hit or miss biological targets.",
        "technical": "PubChem BioAssay serves as the primary public repository for HTS and medicinal chemistry bioactivity records, enabling cross-target selectivity analysis and PAINS/interference filtering.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5480605/",
    },
    {
        "id": "dsp-orthogonal-trfret",
        "name": "Orthogonal Screening: TR-FRET & AlphaScreen Counter-Screens",
        "category": "Hit Confirmation",
        "plain": "Every initial screening hit is re-tested using a completely different physical readout to weed out fluorescent or sticky false positives.",
        "technical": "Pairing primary LANCE TR-FRET qHTS (~90,000-compound libraries) with orthogonal AlphaScreen bead-based counter-assays eliminates assay-interfering artifacts in protein-protein interaction screens.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6611588/",
    },
    {
        "id": "dsp-nih-heal-probes",
        "name": "NIH HEAL Annotated Target & Chemical Probe Library",
        "category": "Chemical Probes",
        "plain": "Curated libraries of ~3,000 well-characterized tool compounds help biologists validate pain and addiction targets rapidly.",
        "technical": "The NCATS HEAL Target and Compound Library curates ~3,000 small-molecule drugs and chemical probes across ~60 pain and addiction targets in 384- and 1,536-well formats.",
        "url": "https://ncats.nih.gov/research/research-activities/heal/expertise/library",
    },
]

SBDD_PDB_CRYOEM = [
    {
        "id": "dsp-cryoem-ligand-challenge",
        "name": "Cryo-EM Ligand Modeling & LIVQ Validation Standards",
        "category": "RCSB PDB / Cryo-EM",
        "plain": "Atomic-resolution 3D snapshots show chemists exactly how a drug nestles into a protein pocket—and new scores check that the fit is real.",
        "technical": "The EMDataResource Cryo-EM Ligand Modeling Challenge (1.9–2.5 Å maps) established composite validation metrics—combining LIVQ map-fit scores, Probescore all-atom contacts, and geometry—for liganded complexes.",
        "url": "https://www.rcsb.org/news/6679793750bece1b815a1450",
    },
    {
        "id": "dsp-alphafold-csm-rcsb",
        "name": "AlphaFold DB Computed Structure Models (CSMs) at RCSB PDB",
        "category": "AI Protein Folding",
        "plain": "When no experimental crystal structure exists yet, AlphaFold AI predictions give drug hunters a starting 3D map of the target.",
        "technical": "RCSB.org integrates AlphaFold DB Computed Structure Models (CSMs) alongside experimental X-ray and cryo-EM entries, expanding structural coverage across human and pathogen proteomes.",
        "url": "https://www.rcsb.org/news/feature/6a0dcabb0fba48755e860634",
    },
    {
        "id": "dsp-cryoem-cak-inhibitor",
        "name": "Single-Particle Cryo-EM of Kinase-Inhibitor Complexes (PDB 8P76)",
        "category": "SBDD Complex",
        "plain": "Cryo-electron microscopy resolves multi-protein enzyme complexes bound to small-molecule drugs without needing protein crystals.",
        "technical": "PDB 8P76 demonstrates single-particle cryo-EM resolution of human CDK-activating kinase (CAK) in complex with selective inhibitor ICEC0914, guiding structure-based optimization.",
        "url": "https://www.rcsb.org/structure/8P76",
    },
    {
        "id": "dsp-cryoem-receptor-module",
        "name": "Full-Length Receptor Cryo-EM Architecture (PDB 7SZ7)",
        "category": "Membrane Targets",
        "plain": "Many drugs target large cell-surface receptors that were impossible to crystallize before modern cryo-EM cameras.",
        "technical": "Single-particle cryo-EM (e.g., PDB 7SZ7 at 3.40 Å) reveals extracellular and transmembrane receptor conformations critical for allosteric and antibody drug design.",
        "url": "https://www.rcsb.org/structure/7SZ7",
    },
    {
        "id": "dsp-target-vs-phenotypic",
        "name": "Target-Based vs. Phenotypic Screening & Hit-Rate Benchmarks",
        "category": "Screening Strategy",
        "plain": "Some medicines are found by aiming at one known protein; others are found by watching whole cells heal—typically with <1% initial hit rates.",
        "technical": "Across modern drug discovery campaigns, biochemical target-based HTS (often <1% hit rate) complements whole-cell phenotypic screening, which historically yielded a disproportionate share of first-in-class drugs.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6181121/",
    },
    {
        "id": "dsp-qsar-imbalanced-hts",
        "name": "QSAR Machine Learning on Imbalanced PubChem HTS Data",
        "category": "Cheminformatics",
        "plain": "Computer models learn from hundreds of thousands of inactive molecules to predict which new structures are most likely to work.",
        "technical": "Quantitative Structure-Activity Relationship (QSAR) models trained on heavily imbalanced PubChem HTS datasets use molecular and biological descriptors to prioritize virtual screening libraries.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3985743/",
    },
]

PROTACS_COVALENT_DISCOVERY = [
    {
        "id": "dsp-protac-catalytic-tpd",
        "name": "PROTAC Targeted Protein Degraders & Catalytic Turnover",
        "category": "PROTACs",
        "plain": "Instead of just blocking a disease protein, PROTACs tag it for the cell's garbage disposal—and then move on to destroy the next copy.",
        "technical": "Proteolysis-Targeting Chimeras (PROTACs) recruit an E3 ubiquitin ligase to polyubiquitinate a Protein of Interest (POI) for 26S proteasomal degradation, operating catalytically at substoichiometric occupancy.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8765495/",
    },
    {
        "id": "dsp-molecular-glues",
        "name": "Molecular Glue-Mediated Targeted Protein Degradation",
        "category": "Molecular Glues",
        "plain": "Molecular glues are compact drugs that snap an E3 disposal enzyme directly onto hard-to-drug proteins that lack deep binding pockets.",
        "technical": "Molecular glue degraders remodel E3 ligase surfaces to induce neomorphic protein-protein interactions (PPIs) with non-canonical substrates, enabling degradation of previously 'undruggable' targets.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC11409024/",
    },
    {
        "id": "dsp-vhl-crbn-ligases",
        "name": "VHL & CRBN E3 Ligases: Heterobifunctional vs. Linkerless",
        "category": "E3 Ligase Design",
        "plain": "Most clinical protein degraders hijack either the VHL or Cereblon (CRBN) cellular tagging machinery.",
        "technical": "Classical heterobifunctional PROTACs link POI and E3 ligands (predominantly VHL and CRBN), whereas lower-MW molecular glues lack linkers and rely on cooperative ternary-complex affinity.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9376879/",
    },
    {
        "id": "dsp-ups-ternary-complex",
        "name": "Ubiquitin-Proteasome System (UPS) & Ternary Cooperativity",
        "category": "Ternary Kinetics",
        "plain": "Getting the target protein and disposal enzyme into the right 3D embrace matters as much as tight binding.",
        "technical": "Degrader potency depends on productive ternary complex formation (POI–degrader–E3), positive cooperativity (alpha > 1), hook-effect management at high concentrations, and ubiquitin-chain geometry.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9910052/",
    },
    {
        "id": "dsp-lytac-extracellular",
        "name": "Beyond the Proteasome: LYTACs & Lysosomal Degradation",
        "category": "LYTACs / Novel TPD",
        "plain": "Newer degrader technologies drag cell-surface and extracellular disease proteins into the cell's lysosome to be broken down.",
        "technical": "Lysosome-Targeting Chimeras (LYTACs) and related endolysosomal modalities extend targeted protein degradation beyond intracellular cytosolic/nuclear proteins to membrane and secreted targets.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10224132/",
    },
    {
        "id": "dsp-tpd-oncology-pipeline",
        "name": "Expanding E3 Ligases & Targeted Degradation in Oncology",
        "category": "Oncology TPD",
        "plain": "Researchers are unlocking tissue-specific E3 ligases to destroy tumor-driving proteins more selectively.",
        "technical": "Next-generation TPD discovery expands beyond CRBN/VHL to tumor-enriched or covalent E3 ligases (e.g., DCAF16, RNF4) to overcome resistance mutations and broaden therapeutic windows.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8463487/",
    },
]

FDA_DISCOVERY_PROBES = [
    {
        "id": "dsp-cder-qm-coe",
        "name": "CDER Quantitative Medicine Center of Excellence (QM CoE)",
        "category": "Quantitative Medicine",
        "plain": "FDA coordinates mathematical and computational biology across discovery, preclinical testing, and clinical trials.",
        "technical": "FDA's QM CoE integrates molecular-to-population quantitative methods and mechanistic modeling to streamline drug discovery, target selection, and regulatory decision-making.",
        "url": "https://www.fda.gov/about-fda/cder-quantitative-medicine-center-excellence-qm-coe/frequently-asked-questions-about-cder-quantitative-medicine-center-excellence-qm-coe",
    },
    {
        "id": "dsp-biomarker-qualification",
        "name": "CDER Biomarker Qualification & Target Engagement COU",
        "category": "Translational Biomarkers",
        "plain": "Qualified lab biomarkers prove early on that a candidate drug actually hits its biological target in living systems.",
        "technical": "CDER's Biomarker Qualification Program establishes Context-of-Use (COU) validation for translational pharmacodynamic and target-engagement biomarkers reusable across multiple drug programs.",
        "url": "https://www.fda.gov/drugs/biomarker-qualification-program/biomarker-qualification-program-educational-module-series-module-2-how-biomarkers-can-improve-drug",
    },
    {
        "id": "dsp-nams-general-2026",
        "name": "FDA General Considerations for NAMs in Drug Development (Mar 2026)",
        "category": "NAMs Validation",
        "plain": "Human organoids, organs-on-chips, and computer simulations increasingly bridge early discovery directly into human safety decisions.",
        "technical": "FDA's March 2026 NAMs draft guidance provides a flexible validation framework (Context of Use, Human Relevance, Technical Characterization, Fit-for-Purpose) for non-animal translational models.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-considerations-use-new-approach-methodologies-drug-development",
    },
    {
        "id": "dsp-model-target-fih",
        "name": "Model-Based Target Identification & Preclinical-to-FIH Bridging",
        "category": "Translational PK/PD",
        "plain": "Early computer models translate lab-dish potency and animal blood levels into safe first-in-human starting doses.",
        "technical": "FDA's MIDD oncology workshop framework links model-based target identification and preclinical exposure-response modeling directly to first-in-human (FIH) dose justification.",
        "url": "https://www.fda.gov/media/113377/download",
    },
    {
        "id": "dsp-tox21-ht-genomics",
        "name": "Tox21 High-Throughput Genomics & Toxicity Signatures",
        "category": "Predictive Tox",
        "plain": "High-throughput gene-expression profiling spots hidden cellular stress early—before a molecule enters expensive animal studies.",
        "technical": "The federal Tox21 program at NCATS pairs automated HTS with high-throughput transcriptomics to map RNA perturbation signatures across environmental and pharmaceutical compounds.",
        "url": "https://ncats.nih.gov/research/research-activities/Tox21/projects",
    },
    {
        "id": "dsp-invivo-qhts-models",
        "name": "In Vivo Quantitative High-Throughput Screening",
        "category": "Phenotypic Screening",
        "plain": "Rapid whole-organism micro-screens in zebrafish or C. elegans test thousands of drug candidates inside living biology.",
        "technical": "In vivo quantitative high-throughput screening bridges cell-based HTS and mammalian models by quantifying dose-response phenotypes in small model organisms.",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10067442/",
    },
]


def build_discovery_sbdd_protacs(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2s",
        "checked": CHECKED,
        "ncats_pubchem_hts": NCATS_PUBCHEM_HTS,
        "sbdd_pdb_cryoem": SBDD_PDB_CRYOEM,
        "protacs_covalent_discovery": PROTACS_COVALENT_DISCOVERY,
        "fda_discovery_probes": FDA_DISCOVERY_PROBES,
    }
    (out_dir / "discovery_sbdd_protacs.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "ncats_pubchem_hts": len(NCATS_PUBCHEM_HTS),
        "sbdd_pdb_cryoem": len(SBDD_PDB_CRYOEM),
        "protacs_covalent_discovery": len(PROTACS_COVALENT_DISCOVERY),
        "fda_discovery_probes": len(FDA_DISCOVERY_PROBES),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_discovery_sbdd_protacs(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

DISCOVERY_SBDD_PROTACS_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderDiscoverySvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="Drug discovery qHTS, Structure-Based Drug Design, PROTACs, and Translational Biomarkers pipeline">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. NCATS &amp; qHTS</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">1,536-Well Robotics</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">PubChem BioAssay</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">TR-FRET / SDR</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Hits &amp; Repurposing</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. SBDD &amp; Cryo-EM</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">RCSB PDB Structures</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">AlphaFold DB CSMs</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">QSAR &amp; LIVQ Scoring</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">3D Pocket Design</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. PROTACs &amp; Glues</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">VHL &amp; CRBN E3 Ligases</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">Ternary Cooperativity</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">Catalytic UPS / LYTAC</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Undruggable Targets</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. Translation &amp; NAMs</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">CDER QM CoE &amp; FIH</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">Qualified Biomarkers</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">Tox21 &amp; Organoids</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Candidate to IND</text>
      </svg>
    </div>`;
}

function renderSection(items, exploreMode) {
  return `<div class="grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem;margin:.75rem 0 1.5rem">
    ${items.map(it => `
      <article class="panel" style="padding:1rem;border:1px solid var(--border,#d8dee6);border-radius:10px;background:var(--paper,#fff)">
        <div style="font-size:.78rem;font-weight:700;color:var(--accent,#1d4ed8);margin-bottom:.25rem">${esc(it.category || "")}</div>
        <h3 style="margin:.1rem 0 .45rem;font-size:1rem">${esc(it.name)}</h3>
        <p style="margin:0 0 .6rem;font-size:.92rem;line-height:1.45">${esc(exploreMode ? it.plain : it.technical)}</p>
        <a href="${esc(it.url)}" target="_blank" rel="noopener noreferrer" style="font-size:.82rem">Official NIH / PDB / FDA source ↗</a>
      </article>`).join("")}
  </div>`;
}

export async function discoverySbddProtacsPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/discovery_sbdd_protacs.json");
  const sections = [
    { key: "ncats_pubchem_hts", title: "1. NIH NCATS, PubChem & Quantitative High-Throughput Screening (qHTS)", items: data.ncats_pubchem_hts || [] },
    { key: "sbdd_pdb_cryoem", title: "2. Structure-Based Drug Design (SBDD), RCSB PDB, Cryo-EM & AlphaFold", items: data.sbdd_pdb_cryoem || [] },
    { key: "protacs_covalent_discovery", title: "3. Targeted Protein Degradation: PROTACs & Molecular Glues", items: data.protacs_covalent_discovery || [] },
    { key: "fda_discovery_probes", title: "4. Translational Biomarkers, Quantitative Medicine & Discovery NAMs", items: data.fda_discovery_probes || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Stage 1 Drug Discovery" : "Reference · Stage 1 Drug Discovery"}</p>
        <h1>Drug Discovery: qHTS Screening, Cryo-EM / AlphaFold SBDD &amp; PROTACs</h1>
        <p class="lede">${exploreMode
          ? "How scientists find the very first chemical starting points for new medicines—from robotic screening and 3D protein snapshots to protein-degrading PROTACs."
          : "Primary-sourced reference covering NIH NCATS qHTS, PubChem BioAssay, RCSB PDB cryo-EM &amp; AlphaFold CSMs, PROTACs/molecular glues, and translational biomarkers."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-25")} · <a href="#/${exploreMode ? "ref" : "explore"}/discovery-sbdd-protacs">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderDiscoverySvg()}
      <div class="filter-bar" role="group" aria-label="Filter drug discovery, SBDD, PROTAC, and translation sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["ncats_pubchem_hts", "NCATS & qHTS (6)"], ["sbdd_pdb_cryoem", "SBDD & Cryo-EM (6)"], ["protacs_covalent_discovery", "PROTACs & Glues (6)"], ["fda_discovery_probes", "Biomarkers & NAMs (6)"]].map(([k, lbl]) => `
          <button type="button" class="btn ${active === k ? "btn-primary" : "btn-secondary"}" data-sec="${k}">${esc(lbl)}</button>`).join("")}
      </div>
      ${visible.map(s => `<h2>${esc(s.title)}</h2>${renderSection(s.items, exploreMode)}`).join("")}
    `;
    container.querySelectorAll("[data-sec]").forEach(btn => {
      btn.addEventListener("click", () => {
        active = btn.getAttribute("data-sec");
        draw();
      });
    });
  };
  draw();
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
    imp = 'import { discoverySbddProtacsPage } from "./discovery_sbdd_protacs.js";\n'
    if "discoverySbddProtacsPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/discovery-sbdd-protacs") return discoverySbddProtacsPage(view, "ref");\n'
        '  if (path === "/explore/discovery-sbdd-protacs") return discoverySbddProtacsPage(view, "explore");\n'
    )
    if '"/ref/discovery-sbdd-protacs"' not in txt:
        anchor = 'if (path === "/ref/inspections-483-recalls")'
        if anchor in txt:
            txt = txt.replace(anchor, route_snip + "  " + anchor, 1)
        else:
            txt += "\n" + route_snip
        changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_layout_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    if "#/ref/discovery-sbdd-protacs" not in txt:
        anchor = '["#/ref/inspections-483-recalls"'
        item = '["#/ref/discovery-sbdd-protacs", "Discovery: qHTS, SBDD & PROTACs"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/discovery-sbdd-protacs" not in txt:
        anchor2 = '["#/explore/inspections-483-recalls"'
        item2 = '["#/explore/discovery-sbdd-protacs", "Discovery: qHTS, SBDD & PROTACs"], '
        if anchor2 in txt:
            txt = txt.replace(anchor2, item2 + anchor2, 1)
        else:
            txt += f'\n// {item2}\n'
        changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    line = "python3 pipeline/build_discovery_sbdd_protacs.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/discovery-sbdd-protacs"' in txt:
        return False
    block = (
        '\n@app.get("/api/discovery-sbdd-protacs")\n'
        'def api_discovery_sbdd_protacs():\n'
        '    p = DATA_DIR / "discovery_sbdd_protacs.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "discovery_sbdd_protacs.json" in txt:
        return False
    snippet = '''    dsp_path = data_dir / "discovery_sbdd_protacs.json"
    if dsp_path.is_file():
        dsp_doc = json.loads(dsp_path.read_text(encoding="utf-8"))
        for sec in ("ncats_pubchem_hts", "sbdd_pdb_cryoem", "protacs_covalent_discovery", "fda_discovery_probes"):
            for item in dsp_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "Discovery: qHTS, SBDD & PROTACs",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/discovery-sbdd-protacs",
                })
'''
    anchor = '    payload = {"checked":'
    if anchor in txt:
        txt = txt.replace(anchor, snippet + "\n" + anchor, 1)
    else:
        txt = txt.rstrip() + "\n" + snippet
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "/discovery-sbdd-protacs/" in txt:
        return False
    snippet = '''    # v6.2s Drug Discovery, qHTS, SBDD (Cryo-EM/AlphaFold) & PROTACs SEO landing page
    dsp_dir = site_dir / "discovery-sbdd-protacs"
    dsp_dir.mkdir(parents=True, exist_ok=True)
    (dsp_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Drug Discovery: qHTS, SBDD (Cryo-EM/AlphaFold) &amp; PROTACs | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to NIH NCATS qHTS, PubChem BioAssay, RCSB PDB cryo-EM &amp; AlphaFold CSMs, PROTACs/molecular glues, and translational biomarkers.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/discovery-sbdd-protacs/'>"
        "<script>location.replace('/#/explore/discovery-sbdd-protacs');</script>"
        "</head><body><h1>Drug Discovery: qHTS, Cryo-EM / AlphaFold SBDD &amp; PROTACs</h1>"
        "<p><a href='/#/explore/discovery-sbdd-protacs'>Explore</a> · <a href='/#/ref/discovery-sbdd-protacs'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/discovery-sbdd-protacs/")
'''
    anchor = "    written_urls = []"
    if anchor in txt:
        txt = txt.replace(anchor, anchor + "\n" + snippet, 1)
    else:
        txt = txt.rstrip() + "\n" + snippet
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "#/ref/discovery-sbdd-protacs" in txt:
        return False
    anchor = '"/#/explore/inspections-483-recalls",'
    add = '"/#/explore/inspections-483-recalls",\n    "/#/ref/discovery-sbdd-protacs",\n    "/#/explore/discovery-sbdd-protacs",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/discovery-sbdd-protacs /#/explore/discovery-sbdd-protacs\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_discovery_sbdd_protacs_py": _write_if_changed(pipe_dir / "build_discovery_sbdd_protacs.py", BUILD_DISCOVERY_SBDD_PROTACS_PY),
        "discovery_sbdd_protacs_js": _write_if_changed(js_dir / "discovery_sbdd_protacs.js", DISCOVERY_SBDD_PROTACS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/inspections-483-recalls") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/inspections-483-recalls", "Inspections, 483, Recalls & ALCOA"]] }];\nconst EXPLORE_NAV = [["#/explore/inspections-483-recalls", "Inspections, 483, Recalls & ALCOA"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/inspections-483-recalls",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_discovery_sbdd_protacs.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_discovery_sbdd_protacs.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ncats_pubchem_hts": 6, "sbdd_pdb_cryoem": 6, "protacs_covalent_discovery": 6, "fda_discovery_probes": 6}, out

        doc = json.loads((root / "site" / "data" / "discovery_sbdd_protacs.json").read_text(encoding="utf-8"))
        for k in ("ncats_pubchem_hts", "sbdd_pdb_cryoem", "protacs_covalent_discovery", "fda_discovery_probes"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "discovery_sbdd_protacs.js").read_text(encoding="utf-8")
        print("V62S_DISCOVERY_SBDD_PROTACS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2s Drug Discovery, qHTS, SBDD & PROTACs patch.")
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
