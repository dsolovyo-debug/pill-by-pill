#!/usr/bin/env python3
"""Pill by Pill v6.2f Patch: Excipients, Drug Master Files (DMFs Types II–V), Nanomaterials (Liposomes/LNPs) & Long-Acting PLGA Microspheres Reference (#/ref/excipients-dmfs-nano, #/explore/excipients-dmfs-nano, /api/excipients-dmfs-nano).

1. Adds `pipeline/build_excipients_dmfs_nano.py` -> `site/data/excipients_dmfs_nano.json` (6 Drug
   Master Files Types II–V pillars, 6 Inactive Ingredient Database & Novel Excipients pillars, 6
   Liposomes, LNPs & Nanomaterials pillars, and 6 Long-Acting Injectables & PLGA Microspheres
   pillars — 24 primary-sourced entries).
2. Adds `site/js/excipients_dmfs_nano.js` (`excipientsDmfsNanoPage` with inline Excipients, DMFs
   & Nanomaterials SVG + 4 section filters) and wires `#/ref/excipients-dmfs-nano`,
   `#/explore/excipients-dmfs-nano`, `/api/excipients-dmfs-nano`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `excipients_dmfs_nano.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/excipients-dmfs-nano/` static SEO page + sitemap entry ->
   48 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2f_excipients_dmfs_nanomaterials_lai_patch.py --selftest
  python3 2026-11-24_v6.2f_excipients_dmfs_nanomaterials_lai_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_EXCIPIENTS_DMFS_NANO_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2f Excipients, DMFs, Nanomaterials & Long-Acting Delivery Reference (`site/data/excipients_dmfs_nano.json`).

Comprehensive, primary-sourced reference covering:
  1. Drug Master Files (DMFs Types II–V) & GDUFA (6 pillars)
  2. Inactive Ingredient Database (IID) & Novel Excipients (6 pillars)
  3. Liposomes, Lipid Nanoparticles (LNPs) & Nanomaterials (6 pillars)
  4. Long-Acting Injectables (LAIs) & PLGA Microspheres (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER, OPQ, GDUFA).

Usage:
  python3 pipeline/build_excipients_dmfs_nano.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

DMF_TYPES_GDUFA = [
    {
        "id": "edn-dmf-types",
        "name": "Drug Master Files (DMFs Types II, III, IV & V)",
        "category": "Confidential Filings",
        "plain": "Chemical and packaging suppliers file confidential Drug Master Files with FDA so drugmakers can reference their recipe without seeing trade secrets.",
        "technical": "Under 21 CFR 314.420, FDA maintains Type II (Drug Substance/Intermediates/Drug Product), Type III (Packaging Material), Type IV (Excipients/Colorants/Flavors), and Type V (FDA-Accepted Reference Info) DMFs.",
        "url": "https://www.fda.gov/drugs/drug-master-files-dmfs/types-drug-master-files-dmfs",
    },
    {
        "id": "edn-dmf-guideline",
        "name": "Type IV Excipient, Colorant & Flavoring DMF Controls",
        "category": "Additive Quality",
        "plain": "Specialized tablet coatings, dyes, and flavorings can be filed in a Type IV DMF detailing how they're made, tested, and proven safe.",
        "technical": "Type IV DMFs document manufacturing methods, release specifications, compendial/21 CFR color/food additive citations, and toxicology data for excipients, colorants, flavors, and essences.",
        "url": "https://www.fda.gov/drugs/drug-master-files-dmfs/guideline-drug-master-files-dmf",
    },
    {
        "id": "edn-dmf-guidance",
        "name": "FDA Drug Master Files Revised Guidance (eCTD & Letters of Auth)",
        "category": "eCTD Submission",
        "plain": "A supplier submits a formal Letter of Authorization letting FDA reviewers open their sealed DMF when reviewing a partner's drug application.",
        "technical": "FDA's Drug Master Files Guidance details eCTD formatting, Letters of Authorization (LOA), annual updates, and Type II/III/IV/V cross-referencing rules for NDAs, ANDAs, INDs, and BLAs.",
        "url": "https://www.fda.gov/media/131861/download",
    },
    {
        "id": "edn-dmf-gdufa",
        "name": "GDUFA Type II API DMF Completeness Assessment (CA)",
        "category": "Generic Readiness",
        "plain": "Before a generic drugmaker can rely on an active-ingredient DMF, FDA checks that the DMF is complete and paid up under GDUFA user fees.",
        "technical": "Under GDUFA, Type II API DMFs referenced in ANDAs undergo a one-time DMF fee and Completeness Assessment (CA) before being placed on FDA's 'Available for Reference' list.",
        "url": "https://www.fda.gov/media/85079/download",
    },
    {
        "id": "edn-dmf-form3938",
        "name": "Electronic DMF Submissions & FDA Form 3938",
        "category": "Digital Filing",
        "plain": "Modern Drug Master Files are submitted electronically in eCTD format using interactive FDA Form 3938.",
        "technical": "Type II, IV, and V DMFs require electronic eCTD submission accompanied by interactive FDA Form 3938 capturing holder/agent metadata, DMF type, and submission action codes.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/drug-master-file-dmf-submissions-new-fda-form-3938-01132021",
    },
    {
        "id": "edn-dmf-guidelines-page",
        "name": "Type III Packaging DMFs & Container-Closure Integrity",
        "category": "Packaging Systems",
        "plain": "Bottle, blister, and rubber-stopper manufacturers use Type III DMFs to prove their plastics and elastomers meet pharmaceutical safety standards.",
        "technical": "Type III DMFs provide composition, extractables/safety data, and manufacturing controls for primary/secondary packaging components referenced across multiple drug applications.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/drug-master-files-guidelines",
    },
]

EXCIPIENTS_IID_NOVEL = [
    {
        "id": "edn-iid-download",
        "name": "FDA Inactive Ingredient Database (IID) Quarterly Files",
        "category": "Precedent Limits",
        "plain": "Formulators check FDA's quarterly Inactive Ingredient Database to see the highest dose of a filler, binder, or solvent already proven safe in approved medicines.",
        "technical": "Updated quarterly (Jan/Apr/Jul/Oct), FDA's IID lists inactive ingredients present in final dosage forms of approved drug products by route, dosage form, UNII, CAS, and Maximum Potency / MDE.",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/inactive-ingredients-database-download",
    },
    {
        "id": "edn-iid-faq",
        "name": "Maximum Potency vs. Maximum Daily Exposure (MDE) in IID",
        "category": "Safety Thresholds",
        "plain": "Using an excipient below its IID Maximum Daily Exposure lets a drugmaker avoid repeating expensive animal toxicology studies.",
        "technical": "FDA's IID distinguishes unit-dose Maximum Potency from total Maximum Daily Exposure (MDE) across a route/dosage form; exceeding IID limits triggers nonclinical qualification.",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/inactive-ingredients-approved-drug-products-search-frequently-asked-questions",
    },
    {
        "id": "edn-iid-fields",
        "name": "UNII Substance Registration & Proprietary Excipient Blends",
        "category": "Substance Identity",
        "plain": "Every pure chemical excipient receives a permanent UNII code from FDA and USP, while proprietary pre-mixed coatings are listed by trade name.",
        "technical": "The joint FDA/USP Substance Registration System (SRS) assigns Unique Ingredient Identifiers (UNIIs) to discrete chemical substances; proprietary blends (e.g., film-coating systems) are tracked as products.",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/inactive-ingredient-field-descriptions",
    },
    {
        "id": "edn-novel-excipient-pilot",
        "name": "CDER Novel Excipient Review Pilot Program",
        "category": "Innovation Pathway",
        "plain": "To encourage brand-new excipients that stabilize mRNA or help poorly soluble pills dissolve, FDA created a pilot to review novel excipients before a drug NDA.",
        "technical": "FDA's Novel Excipient Review Pilot Program enables independent CDER toxicity/CMC review of novel excipients not previously used in FDA-approved drugs or established in food.",
        "url": "https://www.fda.gov/media/151996/download",
    },
    {
        "id": "edn-excipient-safety",
        "name": "Nonclinical Safety Evaluation of Pharmaceutical Excipients",
        "category": "Toxicology Qualification",
        "plain": "If a new excipient or higher-than-usual dose is needed, developers run targeted animal safety and genetic toxicity tests based on how long patients take it.",
        "technical": "FDA's 2005 Excipients Nonclinical Guidance establishes exposure-duration-tiered safety pharmacology, genotoxicity, repeat-dose, and reproductive toxicology requirements for novel or above-IID excipients.",
        "url": "https://www.fda.gov/media/72260/download",
    },
    {
        "id": "edn-fda-databases-hub",
        "name": "FDA Drug Approvals & Dissolution / SRSL / IID Databases Hub",
        "category": "CDER Reference Hub",
        "plain": "FDA's central database portal connects the Inactive Ingredient Database, Dissolution Methods, Orange Book, and Drugs@FDA in one place.",
        "technical": "CDER's Drug Approvals and Databases portal integrates the IID, Dissolution Methods Database, Orange Book, Purple Book, NDC Directory, and FDALabel for formulation and BE design.",
        "url": "https://www.fda.gov/drugs/development-approval-process-drugs/drug-approvals-and-databases",
    },
]

LIPOSOMES_NANOMATERIALS = [
    {
        "id": "edn-nanomaterials-guidance",
        "name": "Drug & Biological Products Containing Nanomaterials (Apr 2022)",
        "category": "Nanomedicine Guidance",
        "plain": "Nanoparticle medicines—from cancer liposomes to mRNA lipid nanoparticles—face extra checks on particle size, surface charge, and immune reactions.",
        "technical": "FDA's April 2022 Nanomaterials Guidance defines risk-based CMC, nonclinical ADME/immunotoxicity, and clinical PK/BE expectations for products engineered at the ~1–100 nm scale (or up to 1,000 nm with size-dependent properties).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/drug-products-including-biological-products-contain-nanomaterials-guidance-industry",
    },
    {
        "id": "edn-liposome-guidance",
        "name": "Liposome Drug Products: CMC, Human PK/BE & Labeling",
        "category": "Liposome Standards",
        "plain": "Tiny fat bubbles called liposomes trap toxic chemo drugs like doxorubicin until they reach tumors—requiring tight control of lipid purity and leakage.",
        "technical": "FDA's Liposome Drug Products Guidance specifies CQA characterization (vesicle size/PDI, lamellarity, zeta potential, encapsulated vs. free drug, lipid degradation/lysolipids) and encapsulated/unencapsulated PK bioequivalence.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/liposome-drug-products-chemistry-manufacturing-and-controls-human-pharmacokinetics-and",
    },
    {
        "id": "edn-nano-sbia",
        "name": "CDER Risk Factors for Nanomaterial Critical Quality Attributes",
        "category": "CQA Framework",
        "plain": "Because nanoparticles behave differently in the bloodstream than dissolved molecules, tiny manufacturing tweaks can change where the drug goes in the body.",
        "technical": "CDER SBIA outlines key nanomaterial risk factors: physicochemical characterization, batch-to-batch size distribution consistency, in vitro drug release kinetics, and biodistribution/complement activation.",
        "url": "https://www.fda.gov/drugs/cder-small-business-industry-assistance-sbia/considerations-drug-products-contain-nanomaterials",
    },
    {
        "id": "edn-nano-cmc",
        "name": "Nanomaterial CMC: Particle Size Distribution, PDI & Sterility",
        "category": "Analytical CMC",
        "plain": "Labs use dynamic light scattering and cryo-EM to measure nanoparticle diameter and ensure sterile filtration doesn't shear or clog the particles.",
        "technical": "CDER nanomaterial CMC reviews require orthogonal sizing (DLS/NTA/cryo-TEM), Polydispersity Index (PDI) limits, encapsulation efficiency, and validated 0.22 µm sterile filtration/endotoxin controls.",
        "url": "https://www.fda.gov/media/166982/download",
    },
    {
        "id": "edn-nano-nonclinical",
        "name": "Nonclinical Safety of Nanomaterials (ICH M3 / S6 / S9 & MPS)",
        "category": "Preclinical ADME",
        "plain": "Animal studies for nanomedicines track whether particles accumulate in the liver and spleen or trigger complement-related infusion reactions (CARPA).",
        "technical": "FDA nonclinical nanomaterial evaluation follows ICH M3/S6/S9 paired with tissue biodistribution, mononuclear phagocyte system (MPS) clearance, and complement activation/CARPA screening.",
        "url": "https://www.fda.gov/media/166984/download",
    },
    {
        "id": "edn-nano-ivrt",
        "name": "Nano-Size Complex Products In Vitro Release Testing (IVRT)",
        "category": "Release Kinetics",
        "plain": "Specialized lab dialysis and flow-through tests measure how fast a liposome or nanoparticle releases its payload into blood-like fluid.",
        "technical": "FDA GDUFA research develops discriminatory IVRT methods (dialysis, ultrafiltration, USP Apparatus 4) for nano-size complex products to support Q3 equivalence and post-approval changes.",
        "url": "https://www.fda.gov/media/184398/download",
    },
]

LAI_PLGA_MICROSPHERES = [
    {
        "id": "edn-lai-fy2015",
        "name": "Long-Acting Injectable (LAI) Formulations & PLGA Microspheres",
        "category": "Depot Delivery",
        "plain": "Biodegradable PLGA polymer microspheres slowly dissolve over weeks or months after a single shot—keeping antipsychotic or hormone levels steady.",
        "technical": "FDA GDUFA regulatory science characterizes poly(lactic-co-glycolic acid) (PLGA) microsphere depots (e.g., risperidone, leuprolide, naltrexone) where polymer molecular weight, lactide:glycolide ratio, and porosity govern release.",
        "url": "https://www.fda.gov/industry/generic-drug-user-fee-amendments/fy2015-regulatory-science-research-report-long-acting-injectable-formulations",
    },
    {
        "id": "edn-lai-fy2016",
        "name": "PLGA Polymer Reverse Engineering & End-Cap Characterization",
        "category": "Polymer Science",
        "plain": "To make a generic long-acting shot, scientists use NMR spectroscopy to match the brand's exact biodegradable polymer chain length and chemical end-caps.",
        "technical": "FDA FY2016 LAI research established 13C NMR and GPC protocols to characterize PLGA ester vs. acid end-caps, blockiness, and molecular weight in commercial depots (Trelstar, Risperdal Consta).",
        "url": "https://www.fda.gov/industry/generic-drug-user-fee-amendments/fy2016-regulatory-science-research-report-long-acting-injectable-formulations",
    },
    {
        "id": "edn-lai-ivivc-literature",
        "name": "Burst Release & In Vitro–In Vivo Correlation (IVIVC) for Depots",
        "category": "Release Modeling",
        "plain": "A poorly made microsphere shot can dump too much drug on day one ('burst release'); IVIVC models link lab release tests to real human blood levels.",
        "technical": "GDUFA IVIVC research models triphasic PLGA release (initial burst, lag phase, erosion release) and establishes Level A IVIVCs using USP Apparatus 4 accelerated and real-time dissolution.",
        "url": "https://www.fda.gov/media/145029/download",
    },
    {
        "id": "edn-lai-gdufa-posters",
        "name": "Long-Acting Implants & Intrauterine Systems (IUS) BE Modeling",
        "category": "Complex Implants",
        "plain": "For hormone implants and IUDs that last years, FDA uses computer modeling and residual drug measurements to evaluate generics without multi-year trials.",
        "technical": "FDA GDUFA quantitative modeling evaluates residual drug content, mechanistic IVIVC, and local tissue pharmacokinetics for long-acting parenteral implants and intrauterine systems.",
        "url": "https://www.fda.gov/media/131262/download",
    },
    {
        "id": "edn-plga-zilretta-nda",
        "name": "New-Route PLGA Excipient Qualification (Zilretta 505(b)(2) Case)",
        "category": "Route Qualification",
        "plain": "Even a well-known polymer like PLGA requires dedicated local-tissue safety studies when used in a brand-new body site like a knee joint.",
        "technical": "NDA 208845 (triamcinolone acetonide in 75:25 PLGA microspheres) illustrates 505(b)(2) local intra-articular GLP toxicology qualification required when an established polymer enters a new route.",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2017/208845Orig1s000PharmRedt.pdf",
    },
    {
        "id": "edn-doxil-to-onpattro",
        "name": "From Doxil to Onpattro: FDA Evolution of Lipid Nanocarriers",
        "category": "Historical Arc",
        "plain": "Thirty years of FDA science bridged the first PEGylated liposome cancer drug (Doxil, 1995) to the first siRNA lipid nanoparticle (Onpattro, 2018).",
        "technical": "FDA CDER's 'From Doxil to Onpattro' retrospective traces how liposome CMC, PEGylation, ionizable lipid LNP formulation, and particle-characterization science matured into mRNA/siRNA therapeutics.",
        "url": "https://www.fda.gov/media/173814/download",
    },
]


def build_excipients_dmfs_nano(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "dmf_types_gdufa": len(DMF_TYPES_GDUFA),
            "excipients_iid_novel": len(EXCIPIENTS_IID_NOVEL),
            "liposomes_nanomaterials": len(LIPOSOMES_NANOMATERIALS),
            "lai_plga_microspheres": len(LAI_PLGA_MICROSPHERES),
        },
        "dmf_types_gdufa": DMF_TYPES_GDUFA,
        "excipients_iid_novel": EXCIPIENTS_IID_NOVEL,
        "liposomes_nanomaterials": LIPOSOMES_NANOMATERIALS,
        "lai_plga_microspheres": LAI_PLGA_MICROSPHERES,
    }
    (data_dir / "excipients_dmfs_nano.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_excipients_dmfs_nano.py <site/data>")
    print(json.dumps(build_excipients_dmfs_nano(pathlib.Path(sys.argv[1])), indent=2))
'''

EXCIPIENTS_DMFS_NANO_JS = '''// Pill by Pill v6.2f: Excipients, DMFs (Types II–V), Nanomaterials (Liposomes/LNPs) & Long-Acting PLGA Microspheres Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["dmf", "Drug Master Files (DMFs)", "dmf_types_gdufa"],
  ["excipients", "Excipients & IID", "excipients_iid_novel"],
  ["nano", "Liposomes, LNPs & Nano", "liposomes_nanomaterials"],
  ["lai", "Long-Acting PLGA Depots", "lai_plga_microspheres"],
];

function excipientsDmfsNanoSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Formulation and delivery architecture: Drug Master Files, Inactive Ingredient Database and Novel Excipients, Liposomes and Nanomaterials, and Long-Acting PLGA Microspheres">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. DMFs (II–V)</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">API, Packaging, Excipients</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">GDUFA CA &amp; Form 3938</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#edn-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Excipients &amp; IID</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Max Potency / MDE &amp; UNII</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Novel Excipient Pilot</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#edn-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Liposomes &amp; LNPs</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Nanomaterial CQAs &amp; PDI</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Doxil to Onpattro IVRT</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#edn-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. LAI &amp; PLGA</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Microspheres &amp; Implants</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">USP App 4 &amp; IVIVC</text>
      <defs><marker id="edn-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Modern drug delivery spans confidential Type II–V DMFs, IID excipient safety limits, engineered liposomes/LNPs, and long-acting PLGA microsphere depots.</figcaption>
  </figure>`;
}

export async function excipientsDmfsNanoPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/excipients_dmfs_nano.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/excipients-dmfs-nano" : "#/ref/excipients-dmfs-nano";

  const pills = html`<div class="chips" role="navigation" aria-label="Excipients, DMFs, nanomaterials, and long-acting delivery sections">
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
    ${excipientsDmfsNanoSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Drug Master Files, Inactive Ingredient Database (IID), Novel Excipient Pilot, Liposome/Nanomaterials, and GDUFA Long-Acting Injectable documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Excipients, DMFs, Nanomaterials & LAIs"]] : [REF_HOME, ["Excipients, DMFs, Nanomaterials & LAIs"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Excipients, Drug Master Files, Nanomaterials & Long-Acting Depots",
      lede: env === "explore"
        ? "How inactive ingredients are cleared for safety, how suppliers file confidential Drug Master Files, and how liposomes and slow-release microspheres deliver medicine."
        : "21 CFR 314.420 DMFs (Types II–V & GDUFA CA), Inactive Ingredient Database (MDE/UNII) & Novel Excipients, Liposomes/LNPs, and PLGA Microsphere IVIVC.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on excipients, DMFs, nanomaterials, and LAIs.", href: env === "explore" ? "#/ref/excipients-dmfs-nano" : "#/explore/excipients-dmfs-nano" },
        { title: "Complex Generics & Nitrosamines", text: "Q1/Q2 sameness, Q3 microstructure, and low-nitrite excipient controls.", href: "#/ref/complex-quality" },
        { title: "ADME, PK & Drug Delivery", text: "Formulation bioavailability, BCS classes, and PK/PD modeling.", href: "#/ref/adme" },
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
    if 'excipients_dmfs_nano.js' not in txt:
        for anchor in ('import * as amrAntiinfectives from "./amr_antiinfectives.js";\n', 'import * as shortagesResilience from "./shortages_resilience.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as excipientsDmfsNano from "./excipients_dmfs_nano.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as excipientsDmfsNano from "./excipients_dmfs_nano.js";\n' + txt
            changed = True
    if '"/ref/excipients-dmfs-nano"' not in txt:
        for anchor in ('if (path === "/ref/amr-antiinfectives")', 'if (path === "/ref/shortages-resilience")', 'if (path === "/ref/complex-quality")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/excipients-dmfs-nano") return { env: "ref", current: "#/ref/excipients-dmfs-nano", ...(await excipientsDmfsNano.excipientsDmfsNanoPage(query, "ref")) };\n  if (path === "/explore/excipients-dmfs-nano") return { env: "explore", current: "#/explore/excipients-dmfs-nano", ...(await excipientsDmfsNano.excipientsDmfsNanoPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/excipients-dmfs-nano" not in txt:
        for anchor in ('["#/ref/amr-antiinfectives", "AMR, phages & CARB-X"]', '["#/ref/shortages-resilience", "Shortages & essential meds"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/excipients-dmfs-nano", "Excipients, DMFs & nano"]', 1)
                changed = True
                break
    if "#/explore/excipients-dmfs-nano" not in txt:
        for anchor in ('["#/explore/amr-antiinfectives", "AMR, phages & CARB-X"]', '["#/explore/shortages-resilience", "Shortages & essential meds"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/excipients-dmfs-nano", "Excipients, DMFs & nano"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_excipients_dmfs_nano.py" in txt:
        return False
    line = "python3 pipeline/build_excipients_dmfs_nano.py site/data\n"
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
    if '"/api/excipients-dmfs-nano"' in txt:
        return False
    route = (
        '\n@app.get("/api/excipients-dmfs-nano")\n'
        'def api_excipients_dmfs_nano():\n'
        '    p = DATA_DIR / "excipients_dmfs_nano.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "excipients_dmfs_nano.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"excipients_dmfs_nano.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    edn_ref = _load(data_dir / "excipients_dmfs_nano.json", {}) or {}\n'
        '    for sec_key, sec_q in [("dmf_types_gdufa", "dmf"), ("excipients_iid_novel", "excipients"), ("liposomes_nanomaterials", "nano"), ("lai_plga_microspheres", "lai")]:\n'
        '        for item in (edn_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "excipients_dmfs_nano",\n'
        '                "group": "Excipients, DMFs, Nanomaterials & LAIs",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/excipients-dmfs-nano?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/excipients-dmfs-nano?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"excipient IID Inactive Ingredient Database UNII DMF Drug Master File Type II Type III Type IV GDUFA liposome LNP nanomaterial PLGA microsphere long acting injectable IVIVC {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"excipients-dmfs-nano", "#/ref/excipients-dmfs-nano"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    edn_doc = _load_json(data_dir / "excipients_dmfs_nano.json")\n'
        '    if isinstance(edn_doc, dict) and edn_doc.get("dmf_types_gdufa"):\n'
        '        edn_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (edn_doc.get("dmf_types_gdufa") or []) + (edn_doc.get("liposomes_nanomaterials") or []))\n'
        '        pages.append(("excipients-dmfs-nano", "#/ref/excipients-dmfs-nano", "Excipients, Drug Master Files, Nanomaterials & Long-Acting Depots",\n'
        '                      "Primary-sourced guide to DMFs (Types II–V), FDA Inactive Ingredient Database (IID) & Novel Excipients, Liposomes/LNPs, and PLGA Microspheres.",\n'
        '                      f"<ul>{edn_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/excipients-dmfs-nano"' in txt:
        return False
    for anchor in ('    "/#/explore/amr-antiinfectives",', '    "/#/explore/shortages-resilience",', '    "/#/explore/complex-quality",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/excipients-dmfs-nano",\n    "/#/explore/excipients-dmfs-nano",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_excipients_dmfs_nano_py": _write_if_changed(pipe_dir / "build_excipients_dmfs_nano.py", BUILD_EXCIPIENTS_DMFS_NANO_PY),
        "excipients_dmfs_nano_js": _write_if_changed(js_dir / "excipients_dmfs_nano.js", EXCIPIENTS_DMFS_NANO_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/amr-antiinfectives") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/amr-antiinfectives", "AMR, phages & CARB-X"]] }];\nconst EXPLORE_NAV = [["#/explore/amr-antiinfectives", "AMR, phages & CARB-X"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/amr-antiinfectives",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_excipients_dmfs_nano.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_excipients_dmfs_nano.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"dmf_types_gdufa": 6, "excipients_iid_novel": 6, "liposomes_nanomaterials": 6, "lai_plga_microspheres": 6}, out

        doc = json.loads((root / "site" / "data" / "excipients_dmfs_nano.json").read_text(encoding="utf-8"))
        for k in ("dmf_types_gdufa", "excipients_iid_novel", "liposomes_nanomaterials", "lai_plga_microspheres"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "excipients_dmfs_nano.js").read_text(encoding="utf-8")
        print("V62F_EXCIPIENTS_DMFS_NANO_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2f Excipients, DMFs, Nanomaterials & LAI patch.")
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
