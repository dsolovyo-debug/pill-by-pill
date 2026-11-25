#!/usr/bin/env python3
"""Pill by Pill v6.1r Patch: Biologics, Biosimilars, Cell & Gene Therapies & Advanced Modalities Reference (#/ref/biologics, #/explore/biologics, /api/biologics).

1. Adds `pipeline/build_biologics_cgt.py` -> `site/data/biologics_cgt.json` (6 mAb/ADC/bispecific
   pillars, 6 biosimilar/351(k)/interchangeability pillars, 6 CAR-T/AAV/CRISPR gene & cell
   therapy pillars, and 6 oligonucleotide/mRNA/radioligand pillars — 24 primary-sourced entries).
2. Adds `site/js/biologics_cgt.js` (`biologicsCgtPage` with inline Modality Complexity &
   Regulatory Oversight SVG + 4 section filters) and wires `#/ref/biologics`,
   `#/explore/biologics`, `/api/biologics`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `biologics_cgt.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/biologics/` static SEO page + sitemap entry -> 34
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1r_biologics_cgt_advanced_modalities_patch.py --selftest
  python3 2026-11-23_v6.1r_biologics_cgt_advanced_modalities_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_BIOLOGICS_CGT_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1r Biologics, Biosimilars, Cell & Gene Therapies & Advanced Modalities Reference (`site/data/biologics_cgt.json`).

Comprehensive, primary-sourced reference covering:
  1. Monoclonal Antibodies, ADCs & Multispecifics (6 pillars)
  2. Biosimilars, 351(k) Pathway & Interchangeability (6 pillars)
  3. Cell & Gene Therapies — CAR-T, Viral Vectors & Genome Editing (6 pillars)
  4. Oligonucleotides, mRNA & Novel Therapeutic Modalities (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER/CBER).

Usage:
  python3 pipeline/build_biologics_cgt.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

MABS_ADCS = [
    {
        "id": "bio-bla-351a",
        "name": "Stand-Alone Biologics License Application (PHS Act § 351(a))",
        "modality": "Full Biologic",
        "plain": "Unlike small-molecule chemical pills made by simple recipes, biologics are large, complex proteins grown inside living cells—so they are approved under a Biologics License Application (BLA).",
        "technical": "Regulated under 42 U.S.C. § 262 (PHS Act § 351(a)) and 21 CFR 600–680 across CDER (mAbs, proteins, cytokines) and CBER (vaccines, blood, cell & gene therapies), carrying 12-year reference product exclusivity.",
        "url": "https://www.fda.gov/drugs/biosimilars/biosimilar-product-information",
    },
    {
        "id": "bio-mabs",
        "name": "Monoclonal Antibodies (IgG1/IgG2/IgG4) & Fc Engineering",
        "modality": "Targeted Proteins",
        "plain": "Lab-designed Y-shaped antibodies lock onto one exact disease protein—blocking growth signals, flagging tumors for immune attack, or calming autoimmune inflammation.",
        "technical": "150 kDa heterotetramers characterized by CDR affinity, FcγR/FcRn effector function and half-life extension, glycosylation microheterogeneity (fucosylation/galactosylation), and ICH Q6B comparability.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/clinical-pharmacology-considerations-novel-therapeutic-modalities-12042024",
    },
    {
        "id": "bio-adcs",
        "name": "Antibody–Drug Conjugates (ADCs) — Linker, DAR & Payload",
        "modality": "Hybrid Biologic + Cytotoxic",
        "plain": "ADCs act like guided missiles: an antibody homes in on a cancer cell and releases a potent chemotherapy payload only after entering the target cell.",
        "technical": "FDA March 2024 Final Guidance on ADCs details bioanalytical separation of total antibody, conjugated antibody (by Drug-to-Antibody Ratio, DAR), and unconjugated small-molecule payload for exposure–response, DDI, and QTc assessment.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-pharmacology-considerations-antibody-drug-conjugates-guidance-industry",
    },
    {
        "id": "bio-bispecifics",
        "name": "Bispecific Antibodies & T-Cell Engagers (BiTEs)",
        "modality": "Dual-Target",
        "plain": "Bispecific antibodies have two different gripping arms—one grabs a cancer cell while the other grabs a T cell, physically pulling the immune killer cell onto the tumor.",
        "technical": "Engineered formats (IgG-like knobs-into-holes, scFv tandems) bridging CD3 on T cells and tumor-associated antigens; require step-up dosing and CRS/ICANS risk management.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/clinical-pharmacology-considerations-novel-therapeutic-modalities-12042024",
    },
    {
        "id": "bio-immunogenicity",
        "name": "Anti-Drug Antibodies (ADA) & Immunogenicity Assessment",
        "modality": "Safety & PK",
        "plain": "Because biologics are large proteins, a patient's immune system can sometimes mistake the medicine for a germ and make antibodies that neutralize the drug or trigger reactions.",
        "technical": "Three-tier validated ADA testing (screening, confirmatory, neutralizing nAb assays) evaluating impact on PK clearance, efficacy loss, and hypersensitivity/infusion reactions.",
        "url": "https://www.fda.gov/drugs/biosimilars/9-things-know-about-biosimilars-and-interchangeable-biosimilars",
    },
    {
        "id": "bio-comparability",
        "name": "Process Changes & Analytical Comparability (ICH Q5E)",
        "modality": "Lifecycle CMC",
        "plain": "Because living cells are sensitive to tiny factory tweaks, moving a biologic to a bigger bioreactor requires proving the before-and-after proteins match structurally and functionally.",
        "technical": "Pre- and post-change physicochemical, biological potency, and impurity profiling (and PK/clinical bridging if needed) to ensure manufacturing changes do not alter safety or efficacy.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/biosimilars-and-interchangeable-biosimilars-licensure-fewer-all-conditions-use-which-reference",
    },
]

BIOSIMILARS_351K = [
    {
        "id": "bs-351k-pathway",
        "name": "Abbreviated Biosimilar Pathway (BPCIA / PHS Act § 351(k))",
        "modality": "Biosimilarity",
        "plain": "A biosimilar is a highly similar copy of an approved biologic with no meaningful clinical differences—like a generic for complex biologics, though impossible to copy atom-for-atom.",
        "technical": "Enacted under BPCIA (2010), § 351(k) relies on a 'totality-of-the-evidence' pyramid anchored in extensive analytical/functional characterization, followed by PK/PD similarity and targeted clinical immunogenicity/efficacy.",
        "url": "https://www.fda.gov/drugs/biosimilars/9-things-know-about-biosimilars-and-interchangeable-biosimilars",
    },
    {
        "id": "bs-interchangeable",
        "name": "Interchangeable Biosimilars & Pharmacy-Level Substitution",
        "modality": "Automatic Substitution",
        "plain": "An interchangeable biosimilar meets extra FDA standards so a pharmacist can substitute it for the brand-name biologic without calling the doctor—just like a pill generic, subject to state law.",
        "technical": "Under PHS Act §§ 351(i)(3) and 351(k)(4), an interchangeable product is expected to produce the same clinical result as the reference product in any given patient and poses no greater risk when switching back and forth.",
        "url": "https://www.fda.gov/consumers/consumer-updates/biosimilar-and-interchangeable-biologics-more-treatment-choices",
    },
    {
        "id": "bs-extrapolation",
        "name": "Scientific Justification & Extrapolation Across Indications",
        "modality": "Indication Scope",
        "plain": "If a biosimilar proves it works identically to the original biologic in one sensitive disease, FDA can approve it for the brand's other diseases without repeating every trial.",
        "technical": "Extrapolation requires scientific justification addressing mechanism of action across indications, target/receptor binding, PK/biodistribution, and expected immunogenicity/toxicity profiles.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/biosimilars-and-interchangeable-biosimilars-licensure-fewer-all-conditions-use-which-reference",
    },
    {
        "id": "bs-carveout",
        "name": "Licensure for Fewer Than All Reference Conditions of Use",
        "modality": "Patent Carve-Out",
        "plain": "When one disease on a brand biologic's label is still protected by a patent, a biosimilar can launch early for the unpatented diseases.",
        "technical": "FDA April 2020 Guidance outlines how a 351(k) BLA applicant may seek licensure for fewer than all conditions of use (e.g., to respect orphan exclusivity or unexpired method-of-use patents).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/biosimilars-and-interchangeable-biosimilars-licensure-fewer-all-conditions-use-which-reference",
    },
    {
        "id": "bs-inn-suffix",
        "name": "4-Letter Nonproprietary Suffixes & Pharmacovigilance Tracking",
        "modality": "Naming Convention",
        "plain": "FDA adds a random four-letter code (like -adaz or -bjmz) to biologic and biosimilar names so safety databases can tell exactly which manufacturer's version a patient received.",
        "technical": "FDA's biological product naming convention pairs a core nonproprietary name with a distinguishing, devoid-of-meaning 4-letter lowercase suffix to prevent inadvertent substitution and enable product-specific safety tracking.",
        "url": "https://www.fda.gov/drugs/biosimilars/biosimilar-product-information",
    },
    {
        "id": "bs-purple-book",
        "name": "FDA Purple Book (Licensed Biological Products & Exclusivity)",
        "modality": "Public Registry",
        "plain": "The Purple Book is FDA's official directory of all licensed biologics, showing which biosimilars and interchangeable products match each brand-name reference drug.",
        "technical": "Searchable database listing 351(a) reference biologics, 351(k) biosimilars and interchangeables, reference-product and orphan exclusivity expiration dates, and BPCIA patent lists.",
        "url": "https://www.fda.gov/drugs/biosimilars/biosimilar-product-information",
    },
]

CELL_GENE_THERAPY = [
    {
        "id": "cgt-cart",
        "name": "CAR-T & Genetically Modified Lymphocyte Products (Jan 2024)",
        "modality": "Ex Vivo Cell Therapy",
        "plain": "Doctors collect a patient's own T cells, genetically reprogram them in a lab to recognize cancer markers like CD19 or BCMA, and infuse them back as a 'living drug.'",
        "technical": "FDA January 2024 Final Guidance covers autologous and allogeneic CAR-T CMC (vector copy number, replication-competent retrovirus/lentivirus testing, potency, chain of identity/custody) and clinical monitoring for CRS/ICANS.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-development-chimeric-antigen-receptor-car-t-cell-products",
    },
    {
        "id": "cgt-genome-editing",
        "name": "Human Gene Therapy Incorporating Genome Editing (CRISPR)",
        "modality": "In Vivo / Ex Vivo Editing",
        "plain": "Genome-editing medicines act like molecular scissors (CRISPR/Cas9 or base editors) that repair or switch off faulty DNA letters directly.",
        "technical": "FDA January 2024 Final Guidance specifies IND requirements for genome-editing products: guide-RNA specificity, unbiased genome-wide off-target assessment, chromosomal translocations/structural variants via NGS, and potency.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/human-gene-therapy-products-incorporating-human-genome-editing",
    },
    {
        "id": "cgt-aav",
        "name": "AAV Viral Vectors & Empty-vs-Full Capsid Controls",
        "modality": "In Vivo Gene Transfer",
        "plain": "Harmless engineered viruses (AAVs) act as microscopic delivery trucks, carrying a working copy of a missing gene into liver, eye, muscle, or nerve cells.",
        "technical": "Key CMC CQAs include vector genome (vg) titer, empty/partially filled/full capsid ratio (AUC / cryo-EM), residual host-cell DNA/plasmid, pre-existing neutralizing anti-AAV antibodies, and hepatotoxicity/TMA monitoring.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/cellular-gene-therapy-guidances",
    },
    {
        "id": "cgt-rmat",
        "name": "Regenerative Medicine Advanced Therapy (RMAT) Designation",
        "modality": "CBER Expedited Program",
        "plain": "A special FDA fast-track badge for cell, gene, and tissue therapies showing early promise against serious or life-threatening diseases.",
        "technical": "Created under the 21st Century Cures Act (FD&C Act § 506(g)); grants Breakthrough-like intensive FDA CBER OTP guidance plus eligibility for accelerated approval using surrogate endpoints or RWE/registries.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/cellular-gene-therapy-guidances",
    },
    {
        "id": "cgt-ltfu",
        "name": "Long-Term Follow-Up (LTFU) — Up to 15 Years Post-Treatment",
        "modality": "Post-Treatment Safety",
        "plain": "Because gene therapies can permanently alter cells in the body, regulators require tracking treated patients for 5 to 15 years to watch for rare delayed side effects.",
        "technical": "Risk-based LTFU protocols (up to 15 years for integrating vectors and genome-editing products; typically 5 years for non-integrating AAV) monitoring delayed malignancies, insertional oncogenesis, and vector persistence.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/cellular-gene-therapy-guidances",
    },
    {
        "id": "cgt-allogeneic",
        "name": "Allogeneic ('Off-the-Shelf') Cell Banks & Donor Screening",
        "modality": "Universal Cell Therapy",
        "plain": "Instead of custom-making cells from each patient's blood, allogeneic therapies grow universal donor cells in large batches so patients can receive treatment immediately.",
        "technical": "Requires 21 CFR 1271 donor eligibility, adventitious agent testing of expanded Master/Working Cell Banks, HLA/TCR editing to mitigate Graft-versus-Host Disease (GvHD), and host-rejection persistence strategies.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/cellular-gene-therapy-guidances",
    },
]

NUCLEIC_NOVEL = [
    {
        "id": "nuc-aso-sirna",
        "name": "Antisense Oligonucleotides (ASOs) & siRNA Gene Silencing",
        "modality": "Synthetic Oligos",
        "plain": "Short synthetic strands of genetic letters bind to disease mRNA inside cells—either silencing a harmful protein or fixing a broken genetic splice.",
        "technical": "Chemically stabilized via phosphorothioate (PS) backbones and 2'-MOE/2'-F/LNA sugar modifications, with GalNAc conjugation for hepatocyte ASGPR targeting; regulated as drugs/CDER with specialized impurity & oligonucleotide-sequence QC.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/clinical-pharmacology-considerations-novel-therapeutic-modalities-12042024",
    },
    {
        "id": "nuc-mrna-lnp",
        "name": "Nucleoside-Modified mRNA & Lipid Nanoparticles (LNPs)",
        "modality": "mRNA Platform",
        "plain": "mRNA vaccines and therapies hand cells a temporary genetic blueprint inside microscopic fat bubbles (LNPs), instructing the body to make protective antigens or missing proteins.",
        "technical": "In vitro transcribed (IVT) mRNA incorporating N1-methylpseudouridine and 5'-cap analogs, encapsulated in 4-component LNPs (ionizable lipid, DSPC, cholesterol, PEG-lipid); critical CQAs include mRNA integrity, dsRNA impurities, and encapsulation efficiency.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/clinical-pharmacology-considerations-novel-therapeutic-modalities-12042024",
    },
    {
        "id": "nuc-peptides",
        "name": "Macrocyclic, Lipidated & Long-Acting Peptide Therapeutics",
        "modality": "Peptide Drugs",
        "plain": "Engineered peptides—like modern GLP-1 metabolic medicines—bridge small pills and large antibodies, using fatty-acid tails or rings so a weekly shot lasts all week.",
        "technical": "Solid-phase peptide synthesis (SPPS) or recombinant expression; FDA ANDA peptide guidance requires tight control of diastereomer, deletion/insertion, and aggregation impurities relative to reference listed drugs.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/clinical-pharmacology-considerations-novel-therapeutic-modalities-12042024",
    },
    {
        "id": "nuc-radioligands",
        "name": "Targeted Radiopharmaceuticals (RLTs) & Theranostic Pairs",
        "modality": "Radioligand Therapy",
        "plain": "A targeting molecule carries a tiny radioactive payload straight to cancer cells—using one isotope to light up tumors on a PET scan and a partner isotope to destroy them.",
        "technical": "Combines a tumor-targeting ligand/antibody, chelator (e.g., DOTA), and alpha/beta-emitting radionuclide (Lu-177, Ac-225); requires rapid hot-cell radiochemical synthesis, dosimetry, and short half-life release testing.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/clinical-pharmacology-considerations-novel-therapeutic-modalities-12042024",
    },
    {
        "id": "nuc-protaq",
        "name": "Targeted Protein Degraders (PROTACs & Molecular Glues)",
        "modality": "Event-Driven Pharmacology",
        "plain": "Instead of merely blocking a disease protein, degraders tag it for the cell's own recycling bin (the proteasome)—destroying the target completely.",
        "technical": "Heterobifunctional small molecules or monovalent glues recruiting E3 ubiquitin ligases (CRBN, VHL); exhibit catalytic sub-stoichiometric activity and 'hook-effect' kinetics requiring specialized PK/PD modeling.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/clinical-pharmacology-considerations-novel-therapeutic-modalities-12042024",
    },
    {
        "id": "nuc-cber-cder",
        "name": "CDER vs. CBER Jurisdiction & Combination Product Lead Center",
        "modality": "FDA Center Assignment",
        "plain": "Depending on how a medicine is made—chemical synthesis, antibody fermentation, or living cells/viruses—FDA routes it to CDER or CBER.",
        "technical": "CDER reviews small molecules, synthetic peptides/oligos, mAbs, and ADCs; CBER reviews vaccines, blood products, cell/gene therapies, and live biotherapeutics, with Office of Combination Products (OCP) assigning PMOA lead.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-guidances/cellular-gene-therapy-guidances",
    },
]


def build_biologics_cgt(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "mabs_adcs": len(MABS_ADCS),
            "biosimilars_351k": len(BIOSIMILARS_351K),
            "cell_gene_therapy": len(CELL_GENE_THERAPY),
            "nucleic_novel": len(NUCLEIC_NOVEL),
        },
        "mabs_adcs": MABS_ADCS,
        "biosimilars_351k": BIOSIMILARS_351K,
        "cell_gene_therapy": CELL_GENE_THERAPY,
        "nucleic_novel": NUCLEIC_NOVEL,
    }
    (data_dir / "biologics_cgt.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_biologics_cgt.py <site/data>")
    print(json.dumps(build_biologics_cgt(pathlib.Path(sys.argv[1])), indent=2))
'''

BIOLOGICS_CGT_JS = '''// Pill by Pill v6.1r: Biologics, Biosimilars, Cell & Gene Therapies & Advanced Modalities Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["mabs", "mAbs, ADCs & Bispecifics", "mabs_adcs"],
  ["biosimilars", "Biosimilars (351(k))", "biosimilars_351k"],
  ["cgt", "Cell & Gene Therapies", "cell_gene_therapy"],
  ["novel", "Oligos, mRNA & Novel", "nucleic_novel"],
];

function modalitySpectrumSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Therapeutic modality complexity spectrum from synthetic peptides and oligos to mAbs and living cell/gene therapies">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Synthetic Modalities</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">ASOs, siRNA, Peptides</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">PROTACs &amp; Radioligands</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#bio-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Engineered Proteins</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">mAbs, ADCs, Bispecifics</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">PHS § 351(a) / ICH Q5E</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#bio-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Biosimilars</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">PHS § 351(k) &amp; Purple Book</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Interchangeability</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#bio-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Living Therapies</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">CAR-T, AAV, CRISPR</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">CBER RMAT &amp; 15-yr LTFU</text>
      <defs><marker id="bio-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Modern pharmacology spans synthetic oligonucleotides and targeted protein degraders to complex biologics, biosimilars, and living cell/gene therapies.</figcaption>
  </figure>`;
}

export async function biologicsCgtPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/biologics_cgt.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/biologics" : "#/ref/biologics";

  const pills = html`<div class="chips" role="navigation" aria-label="Biologics and CGT sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Modality / Framework</th><th>Class</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
        <tbody>${items.map((x) => html`<tr id="${x.id}">
          <th scope="row">${x.name}</th>
          <td>${x.modality}</td>
          <td>${env === "explore" ? x.plain : x.technical}</td>
          <td><a href="${x.url}" target="_blank" rel="noopener">Official source →</a></td>
        </tr>`)}</tbody></table>
      </div>
    </section>`;

  const visible = SECTIONS.filter(([, , key]) => key && (activeSec === "all" || activeSec === SECTIONS.find((s) => s[2] === key)?.[0]));
  const body = html`
    ${modalitySpectrumSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA CDER/CBER Biologics, Biosimilars, CAR-T, and Genome Editing guidances.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Biologics & Gene Therapies"]] : [REF_HOME, ["Biologics & Gene Therapies"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Biologics, Biosimilars, Cell & Gene Therapies & Advanced Modalities",
      lede: env === "explore"
        ? "How antibodies, biosimilars, engineered T cells, CRISPR gene editors, and mRNA medicines are designed, tested, and regulated."
        : "PHS Act § 351(a)/351(k) biologics & biosimilars, ADCs, CAR-T, AAV, CRISPR genome editing, oligonucleotides, mRNA/LNPs, and radioligands.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on biologics and advanced modalities.", href: env === "explore" ? "#/ref/biologics" : "#/explore/biologics" },
        { title: "Sterile Manufacturing & Bioprocessing", text: "Cell banks, bioreactors, chromatography, viral clearance, and Annex 1.", href: "#/ref/sterile" },
        { title: "Pharma IP, Hatch-Waxman & BPCIA", text: "12-year biologic exclusivity, the Patent Dance, and Purple Book.", href: "#/ref/ip" },
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
    if 'biologics_cgt.js' not in txt:
        for anchor in ('import * as supplyChain from "./supply_chain.js";\n', 'import * as rwe from "./rwe.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as biologicsCgt from "./biologics_cgt.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as biologicsCgt from "./biologics_cgt.js";\n' + txt
            changed = True
    if '"/ref/biologics"' not in txt:
        for anchor in ('if (path === "/ref/supply-chain")', 'if (path === "/ref/rwe")', 'if (path === "/ref/diagnostics")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/biologics") return { env: "ref", current: "#/ref/biologics", ...(await biologicsCgt.biologicsCgtPage(query, "ref")) };\n  if (path === "/explore/biologics") return { env: "explore", current: "#/explore/biologics", ...(await biologicsCgt.biologicsCgtPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/biologics" not in txt:
        for anchor in ('["#/ref/supply-chain", "Supply chain & DSCSA"]', '["#/ref/rwe", "Real-World Evidence"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/biologics", "Biologics & CGT"]', 1)
                changed = True
                break
    if "#/explore/biologics" not in txt:
        for anchor in ('["#/explore/supply-chain", "Supply chain & DSCSA"]', '["#/explore/rwe", "Real-World Evidence"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/biologics", "Biologics & CGT"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_biologics_cgt.py" in txt:
        return False
    line = "python3 pipeline/build_biologics_cgt.py site/data\n"
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
    if '"/api/biologics"' in txt:
        return False
    route = (
        '\n@app.get("/api/biologics")\n'
        'def api_biologics():\n'
        '    p = DATA_DIR / "biologics_cgt.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "biologics_cgt.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"biologics_cgt.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    bio_ref = _load(data_dir / "biologics_cgt.json", {}) or {}\n'
        '    for sec_key, sec_q in [("mabs_adcs", "mabs"), ("biosimilars_351k", "biosimilars"), ("cell_gene_therapy", "cgt"), ("nucleic_novel", "novel")]:\n'
        '        for item in (bio_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "biologics_cgt",\n'
        '                "group": "Biologics & Gene Therapies",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/biologics?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/biologics?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"biologics mAb ADC bispecific biosimilar 351k interchangeable CAR-T AAV CRISPR gene therapy mRNA LNP oligonucleotide PROTAC radioligand {sec_key} {item.get(\'name\', \'\')} {item.get(\'modality\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"biologics", "#/ref/biologics"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    bio_doc = _load_json(data_dir / "biologics_cgt.json")\n'
        '    if isinstance(bio_doc, dict) and bio_doc.get("mabs_adcs"):\n'
        '        bio_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (bio_doc.get("mabs_adcs") or []) + (bio_doc.get("cell_gene_therapy") or []))\n'
        '        pages.append(("biologics", "#/ref/biologics", "Biologics, Biosimilars, Cell & Gene Therapies & Advanced Modalities",\n'
        '                      "Primary-sourced guide to PHS Act § 351(a)/351(k) biologics, biosimilars, ADCs, CAR-T, AAV, CRISPR genome editing, mRNA/LNPs, and radioligands.",\n'
        '                      f"<ul>{bio_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/biologics"' in txt:
        return False
    for anchor in ('    "/#/explore/supply-chain",', '    "/#/explore/rwe",', '    "/#/explore/diagnostics",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/biologics",\n    "/#/explore/biologics",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_biologics_cgt_py": _write_if_changed(pipe_dir / "build_biologics_cgt.py", BUILD_BIOLOGICS_CGT_PY),
        "biologics_cgt_js": _write_if_changed(js_dir / "biologics_cgt.js", BIOLOGICS_CGT_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/supply-chain") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/supply-chain", "Supply chain & DSCSA"]] }];\nconst EXPLORE_NAV = [["#/explore/supply-chain", "Supply chain & DSCSA"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/supply-chain",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_biologics_cgt.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_biologics_cgt.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"mabs_adcs": 6, "biosimilars_351k": 6, "cell_gene_therapy": 6, "nucleic_novel": 6}, out

        doc = json.loads((root / "site" / "data" / "biologics_cgt.json").read_text(encoding="utf-8"))
        for k in ("mabs_adcs", "biosimilars_351k", "cell_gene_therapy", "nucleic_novel"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "biologics_cgt.js").read_text(encoding="utf-8")
        print("V61R_BIOLOGICS_CGT_ADVANCED_MODALITIES_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1r Biologics, Biosimilars & Cell/Gene Therapy patch.")
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
