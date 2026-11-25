#!/usr/bin/env python3
"""Pill by Pill v6.2a Patch: Radiopharmaceuticals, Theranostics, PET Drug cGMP (21 CFR 212), RDRC & NRC Licensing Reference (#/ref/radiopharma, #/explore/radiopharma, /api/radiopharma).

1. Adds `pipeline/build_radiopharma.py` -> `site/data/radiopharma.json` (6 Therapeutic
   Radiopharmaceuticals & Theranostics pillars, 6 PET Drug cGMP [21 CFR 212] & NDAs/ANDAs pillars,
   6 RDRC Basic-Science Research [21 CFR 361.1] & IND Exemption pillars, and 6 NRC 10 CFR Part 35
   Medical Use & Commercial Distribution pillars — 24 primary-sourced entries).
2. Adds `site/js/radiopharma.js` (`radiopharmaPage` with inline Radiopharmaceutical & Theranostics
   Lifecycle SVG + 4 section filters) and wires `#/ref/radiopharma`, `#/explore/radiopharma`,
   `/api/radiopharma`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `radiopharma.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/radiopharma/` static SEO page + sitemap entry -> 43
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.2a_radiopharmaceuticals_theranostics_pet_cgmp_patch.py --selftest
  python3 2026-11-23_v6.2a_radiopharmaceuticals_theranostics_pet_cgmp_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_RADIOPHARMA_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2a Radiopharmaceuticals, Theranostics, PET cGMP & NRC Licensing Reference (`site/data/radiopharma.json`).

Comprehensive, primary-sourced reference covering:
  1. Oncology Therapeutic Radiopharmaceuticals & Theranostics (6 pillars)
  2. PET Drug cGMP (21 CFR Part 212) & FDAMA § 121 Applications (6 pillars)
  3. Radioactive Drug Research Committee (RDRC, 21 CFR 361.1) (6 pillars)
  4. NRC 10 CFR Part 35 Medical Use & Commercial Isotope Licensing (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER, US NRC).

Usage:
  python3 pipeline/build_radiopharma.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

THERAPEUTIC_THERANOSTICS = [
    {
        "id": "rad-rpt-dosage",
        "name": "Oncology Therapeutic Radiopharmaceuticals (RPTs) & Dosage Optimization",
        "category": "Clinical Development",
        "plain": "Targeted radiopharmaceuticals attach a cancer-killing radioactive isotope to a homing molecule—FDA's 2025 guidance helps sponsors pick the safest, most effective radiation dose.",
        "technical": "FDA's August 2025 Draft Guidance ('Oncology Therapeutic Radiopharmaceuticals: Dosage Optimization During Clinical Development') addresses administered activity (MBq/mCi) and schedule optimization prior to marketing applications.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oncology-therapeutic-radiopharmaceuticals-dosage-optimization-during-clinical-development",
    },
    {
        "id": "rad-theranostic-pairing",
        "name": "Theranostic Pairings: Diagnostic Imaging + Targeted Radionuclide Therapy",
        "category": "Precision Oncology",
        "plain": "Theranostics use a matching PET scan tracer first to confirm a patient's tumors light up, then swap in a beta- or alpha-emitting isotope on the same targeting ligand to destroy the tumor.",
        "technical": "Co-developed diagnostic imaging tracers (e.g., Ga-68 / F-18 PET) and therapeutic RPTs (e.g., Lu-177 beta or Ac-225 alpha emitters) align receptor target verification, personalized dosimetry, and CDx selection.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oncology-therapeutic-radiopharmaceuticals-dosage-optimization-during-clinical-development",
    },
    {
        "id": "rad-alpha-beta-gamma",
        "name": "Alpha, Beta & Gamma Decay Profiles & Biodistribution Studies",
        "category": "Nonclinical Physics",
        "plain": "Alpha particles pack huge energy over a tiny few-cell range, beta particles travel farther across tumor clusters, and gamma rays allow external camera imaging.",
        "technical": "FDA's Nonclinical Studies guidance covers systemically administered alpha, beta, and gamma-emitting RPTs—requiring animal biodistribution, target binding, and organ absorbed-dose (Gy / Sv) estimates before FIH.",
        "url": "https://www.fda.gov/media/129547/download",
    },
    {
        "id": "rad-late-radiation-tox",
        "name": "Late Radiation Toxicity & Organ-At-Risk Dosimetry (Kidneys & Marrow)",
        "category": "Radiation Safety",
        "plain": "Unlike regular chemo side effects that appear right away, radiation damage to kidneys or bone marrow can emerge months later—so FDA evaluates long-term organ radiation limits.",
        "technical": "Nonclinical evaluation of late radiation toxicity integrates organ absorbed-dose limits (e.g., renal cortex, bone marrow, salivary glands, CNS vascular/demyelination risk) using RBE-weighted dosimetry (H = RBE × D).",
        "url": "https://www.fda.gov/media/129547/download",
    },
    {
        "id": "rad-fih-dual-dose",
        "name": "First-in-Human (FIH) Starting Dose: Radioactive Activity + Mass Dose",
        "category": "FIH Translation",
        "plain": "Starting doses for radioactive drugs must balance two limits at once: the total radiation exposure and the chemical amount of the carrier molecule.",
        "technical": "FDA FIH estimation for RPTs evaluates both administered radioactivity (mCi/GBq) and cold-ligand chemical mass dose, incorporating safety pharmacology endpoints directly into toxicology/biodistribution studies.",
        "url": "https://www.fda.gov/media/129547/download",
    },
    {
        "id": "rad-1msv-breastfeeding",
        "name": "1 mSv Nursing-Child Limit & Post-Treatment Lactation Labeling",
        "category": "Patient Counseling",
        "plain": "Radiopharmaceutical labels specify exactly how long a breastfeeding mother must pause nursing (and pump-and-discard) so her baby stays below a strict 1 millisievert radiation limit.",
        "technical": "FDA labeling recommendations require proposing a lactation cessation window sufficient to limit effective radiation dose to a nursing child to ≤1 mSv (NRC 2008), accounting for radionuclide half-life and ligand transfer.",
        "url": "https://www.fda.gov/media/129547/download",
    },
]

PET_CGMP_212 = [
    {
        "id": "pet-21cfr212",
        "name": "PET Drug cGMP (21 CFR Part 212) vs. Standard Drug cGMP (Part 211)",
        "category": "Specialized cGMP",
        "plain": "PET scan tracers decay in minutes or hours—so FDA created a special fast-track manufacturing rule (21 CFR 212) allowing hospitals and cyclotrons to release doses before slow sterility tests finish.",
        "technical": "21 CFR Part 212 tailors cGMP for Positron Emission Tomography drugs with short physical half-lives (e.g., F-18 110 min, N-13 10 min), permitting conditional release before 14-day sterility completion under strict aseptic controls.",
        "url": "https://www.fda.gov/media/82370/download",
    },
    {
        "id": "pet-fdama-121",
        "name": "FDAMA § 121(c) PET Drug Approval Framework (FDG, Ammonia & NaF)",
        "category": "Statutory Basis",
        "plain": "Congress directed FDA to streamline approvals for classic PET imaging tracers like FDG F-18 so hospital cyclotrons could submit abbreviated applications using published medical literature.",
        "technical": "FDAMA § 121(c) mandated dedicated PET cGMP and NDA/ANDA procedures, establishing literature-supported safety/effectiveness findings for fludeoxyglucose F 18, ammonia N 13, and sodium fluoride F 18 injections.",
        "url": "https://www.fda.gov/files/drugs/published/PET-Drug-Applications---Content-and-Format-for-NDAs-and-ANDAs.pdf",
    },
    {
        "id": "pet-eos-specs",
        "name": "End-of-Synthesis (EOS) Radioconcentration & Specific Activity",
        "category": "Release Testing",
        "plain": "Because radioactivity drops every minute on the delivery truck, PET drug labels specify strength at the exact moment synthesis finishes (EOS), not weeks later.",
        "technical": "PET NDA/ANDA CMC specs define no-carrier-added specific activity, radioconcentration at End of Synthesis (e.g., 20–300 mCi/mL EOS for FDG F 18), isotonic osmolality, and pH prior to patient calibration.",
        "url": "https://www.fda.gov/files/drugs/published/PET-Drug-Applications---Content-and-Format-for-NDAs-and-ANDAs.pdf",
    },
    {
        "id": "pet-media-fills",
        "name": "Aseptic Media Fills, Sterility Controls & Environmental Monitoring",
        "category": "Sterility Assurance",
        "plain": "Even with rapid cyclotron synthesis, every technician preparing sterile PET vials must pass simulated aseptic 'media fill' tests with zero bacterial growth.",
        "technical": "FDA's PET 212 CPGM requires inspectors to audit media fill growth-promotion testing, personnel qualification, incoming environmental monitoring plates, and genus identification of any positive vials.",
        "url": "https://www.fda.gov/media/82370/download",
    },
    {
        "id": "pet-ind-pathway",
        "name": "Investigational New Drug (IND) Applications for Novel PET Tracers",
        "category": "Clinical Imaging",
        "plain": "Before a hospital or biotech tests a brand-new brain or tumor PET tracer in patients for diagnosis, it must file a streamlined PET IND with FDA.",
        "technical": "FDA's PET IND guidance coordinates 21 CFR Part 312 clinical trial oversight with 21 CFR Part 212 manufacturing controls for investigational diagnostic PET radiopharmaceuticals.",
        "url": "https://www.fda.gov/files/drugs/published/Investigational-New-Drug-Applications-for-Positron-Emission-Tomography-%28PET%29-Drugs.pdf",
    },
    {
        "id": "pet-oai-fars",
        "name": "PET Field Alert Reports (FARs) & Biennal cGMP Inspections",
        "category": "Post-Market Quality",
        "plain": "FDA inspects commercial PET cyclotron facilities every two years and requires rapid Field Alert Reports if a shipped radioactive batch fails quality checks.",
        "technical": "PET 212 Compliance Program governs Pre-Approval (PAI) and biennial surveillance inspections (Abbreviated vs. Full options), ADE reporting, and Field Alert Reports (FARs) via MARCS-CMS.",
        "url": "https://www.fda.gov/media/82370/download",
    },
]

RDRC_RESEARCH = [
    {
        "id": "rdrc-21cfr361",
        "name": "Radioactive Drug Research Committee (RDRC, 21 CFR 361.1)",
        "category": "IND Exemption",
        "plain": "University medical centers can run basic-science metabolism or physiology studies with microdose radioactive tracers without filing a full FDA IND—if an FDA-approved local RDRC reviews them.",
        "technical": "21 CFR 361.1 permits human basic-science research (metabolism, kinetics, distribution, dosimetry, pathophysiology) with GRASE radioactive drugs without an IND when approved by an FDA-authorized institutional RDRC.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/radioactive-drug-research-committee-rdrc-program",
    },
    {
        "id": "rdrc-non-therapeutic",
        "name": "Strict Non-Therapeutic & Sub-Pharmacologic Dose Limits",
        "category": "Study Boundaries",
        "plain": "RDRC studies cannot be used to treat diseases or diagnose patients—and the chemical dose must be so tiny it causes zero detectable drug effect in the body.",
        "technical": "Under 21 CFR 361.1(a)-(b), RDRC studies cannot have immediate therapeutic or diagnostic intent, and the administered pharmacologic mass dose must be known not to cause any clinically detectable pharmacologic effect.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/radioactive-drug-research-committee-rdrc-program",
    },
    {
        "id": "rdrc-5member-panel",
        "name": "Mandatory Five-Member RDRC Expertise Composition",
        "category": "Committee Governance",
        "plain": "Every RDRC must include a nuclear medicine physician, a radiochemist, a radiation safety/dosimetry expert, and two other medical specialists.",
        "technical": "21 CFR 361.1(c)(1) requires ≥5 members: a nuclear medicine specialist physician, a qualified radioactive drug formulator, a radiation safety/dosimetry specialist, and pertinent medical discipline experts.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/what-are-qualifications-and-requirements-rdrc-membership",
    },
    {
        "id": "rdrc-9criteria",
        "name": "Nine RDRC Study Approval Criteria & IRB Coordination",
        "category": "Protocol Review",
        "plain": "Both the RDRC and the hospital's ethics board (IRB) must sign off on radiation limits, drug quality, and patient consent before a volunteer receives a tracer.",
        "technical": "21 CFR 361.1(d)(1)-(9) mandates verification of radiation dose limits, pharmacologic dose limits, investigator qualifications, radioactive materials licensing, subject consent, drug quality, and IRB approval.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/what-are-responsibilities-rdrc",
    },
    {
        "id": "rdrc-adverse-reporting",
        "name": "Immediate RDRC & FDA Adverse Reaction Reporting",
        "category": "Safety Escalation",
        "plain": "If a volunteer has any unexpected reaction to a research tracer, the researcher must alert the RDRC immediately, and the RDRC chair must notify FDA right away.",
        "technical": "Under 21 CFR 361.1(d)(8), investigators must immediately report all adverse effects to the RDRC, and the RDRC chairperson must immediately report all probably attributable adverse reactions to FDA.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/what-are-responsibilities-rdrc",
    },
    {
        "id": "rdrc-vs-ind",
        "name": "Determining RDRC Eligibility vs. Exploratory/Full IND",
        "category": "Regulatory Triage",
        "plain": "If a study uses a brand-new tracer with unknown human safety or aims to diagnose cancer, it cannot use RDRC and must go through FDA's IND pathway instead.",
        "technical": "FDA's IND-determination guidance clarifies that novel chemical entities lacking prior human safety/dosimetry data or studies with diagnostic/therapeutic endpoints require an IND (21 CFR Part 312) rather than § 361.1 RDRC.",
        "url": "https://www.fda.gov/files/drugs/published/Investigational-New-Drug-Applications-%28INDs%29-Determining-Whether-Human-Research-Studies-Can-Be-Conducted-Without-an-IND.pdf",
    },
]

NRC_LICENSING_SUPPLY = [
    {
        "id": "nrc-10cfr35",
        "name": "NRC 10 CFR Part 35: Medical Use of Byproduct Material",
        "category": "Radiation Licensing",
        "plain": "While FDA regulates whether a radioactive drug is safe and pure, the Nuclear Regulatory Commission (or state radiation agency) licenses the hospital to possess and administer it safely.",
        "technical": "10 CFR Part 35 establishes licensing and radiation-safety requirements for medical use of byproduct material, protecting workers, patients, the general public, and human research subjects.",
        "url": "https://www.nrc.gov/reading-rm/doc-collections/cfr/part035/index.html",
    },
    {
        "id": "nrc-fda-split",
        "name": "Dual Oversight: FDA (cGMP/Efficacy) vs. NRC (Radiation Safety)",
        "category": "Agency Jurisdiction",
        "plain": "Radiopharmaceutical companies answer to two federal watchdogs: FDA oversees clinical trials and drug manufacturing, while NRC oversees radioactive material handling and shielding.",
        "technical": "NRC's Medical Uses framework coordinates with FDA (which regulates drug safety, efficacy, and cGMP manufacturing) while NRC and 39 Agreement States license possession, shielding, and waste decay.",
        "url": "https://www.nrc.gov/materials/miau/med-use",
    },
    {
        "id": "nrc-part32-mfg",
        "name": "NRC 10 CFR Part 32 Commercial Radiopharmacy & Isotope Distribution",
        "category": "Commercial Supply",
        "plain": "Commercial nuclear pharmacies and isotope factories need specific NRC distribution licenses before they can ship unit-dose syringes to hospitals nationwide.",
        "technical": "10 CFR Part 32 governs specific domestic licenses to manufacture and distribute radioactive byproduct material to medical-use licensees, including generator elutions and sealed calibration sources.",
        "url": "https://www.nrc.gov/materials/miau/product-manufac",
    },
    {
        "id": "nrc-auth-users",
        "name": "Authorized Users (AUs) & Authorized Nuclear Pharmacists (ANPs)",
        "category": "Personnel Credentials",
        "plain": "Only specially board-certified nuclear medicine doctors, radiation oncologists, and nuclear pharmacists listed on a facility's license can handle or prescribe therapeutic isotopes.",
        "technical": "10 CFR Part 35 requires documented training, board certification, and preceptor attestation for Authorized Users (AUs), Authorized Nuclear Pharmacists (ANPs), Authorized Medical Physicists, and RSOs.",
        "url": "https://www.nrc.gov/materials/miau/med-use-toolkit/auth-individuals",
    },
    {
        "id": "nrc-written-directives",
        "name": "Written Directives & Medical Event Reporting (10 CFR 35.40)",
        "category": "Clinical Safety",
        "plain": "Before giving a therapeutic radiopharmaceutical, the physician must sign a strict 'written directive' specifying the exact isotope and dose—and wrong-dose errors must be reported to NRC.",
        "technical": "10 CFR Part 35 mandates dated/signed Written Directives prior to therapeutic radiopharmaceutical administration and requires reporting of Medical Events (wrong drug, wrong patient, or ≥20% dose variance).",
        "url": "https://www.nrc.gov/materials/miau/med-use-toolkit/faqs-part35",
    },
    {
        "id": "nrc-human-research",
        "name": "10 CFR 35.6 Human Research Protection & Informed Consent",
        "category": "Trial Compliance",
        "plain": "Hospitals running radiopharmaceutical clinical trials must ensure their NRC license covers the exact isotope being tested and obtain Common Rule informed consent.",
        "technical": "Under 10 CFR 35.6, licensees conducting human research with byproduct material must use only isotopes authorized on their license and obtain Federal Policy (Common Rule) informed consent.",
        "url": "https://www.ecfr.gov/current/title-10/chapter-I/part-35",
    },
]


def build_radiopharma(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "therapeutic_theranostics": len(THERAPEUTIC_THERANOSTICS),
            "pet_cgmp_212": len(PET_CGMP_212),
            "rdrc_research": len(RDRC_RESEARCH),
            "nrc_licensing_supply": len(NRC_LICENSING_SUPPLY),
        },
        "therapeutic_theranostics": THERAPEUTIC_THERANOSTICS,
        "pet_cgmp_212": PET_CGMP_212,
        "rdrc_research": RDRC_RESEARCH,
        "nrc_licensing_supply": NRC_LICENSING_SUPPLY,
    }
    (data_dir / "radiopharma.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_radiopharma.py <site/data>")
    print(json.dumps(build_radiopharma(pathlib.Path(sys.argv[1])), indent=2))
'''

RADIOPHARMA_JS = '''// Pill by Pill v6.2a: Radiopharmaceuticals, Theranostics, PET cGMP (21 CFR 212), RDRC & NRC Licensing Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["theranostics", "Theranostics & RPTs", "therapeutic_theranostics"],
  ["pet", "PET cGMP (21 CFR 212)", "pet_cgmp_212"],
  ["rdrc", "RDRC Research (21 CFR 361.1)", "rdrc_research"],
  ["nrc", "NRC 10 CFR 35 Licensing", "nrc_licensing_supply"],
];

function radiopharmaSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Radiopharmaceutical and theranostics lifecycle: RPT/Theranostics, PET cGMP 21 CFR 212, RDRC 21 CFR 361.1, and NRC 10 CFR 35">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Theranostics</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Alpha / Beta / Gamma RPT</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Organ Dosimetry &amp; 1 mSv</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rad-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. PET cGMP (212)</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">21 CFR 212 &amp; FDAMA §121</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">EOS &amp; Media Fills</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rad-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. RDRC (361.1)</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">IND-Exempt Basic Science</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Sub-Pharmacologic Dose</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#rad-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. NRC 10 CFR 35</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">AUs, ANPs &amp; Directives</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Part 32 Distribution</text>
      <defs><marker id="rad-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Radiopharmaceuticals bridge FDA drug/cGMP oversight (21 CFR 212, RPT dosimetry, RDRC) with NRC/Agreement State radiation licensing (10 CFR 32/35).</figcaption>
  </figure>`;
}

export async function radiopharmaPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/radiopharma.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/radiopharma" : "#/ref/radiopharma";

  const pills = html`<div class="chips" role="navigation" aria-label="Radiopharmaceuticals and theranostics sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Standard / Rule</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${radiopharmaSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Oncology RPT, PET Drug cGMP (21 CFR 212), RDRC (21 CFR 361.1), and US NRC 10 CFR Part 35 documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Radiopharmaceuticals & Theranostics"]] : [REF_HOME, ["Radiopharmaceuticals & Theranostics"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Radiopharmaceuticals, Theranostics, PET cGMP & NRC Licensing",
      lede: env === "explore"
        ? "How radioactive imaging tracers and targeted cancer radiotherapies are manufactured before decay, tested safely, and licensed for hospitals."
        : "Oncology RPT dosage optimization & late radiation toxicity, 21 CFR 212 PET cGMP, 21 CFR 361.1 RDRC, and NRC 10 CFR Parts 32/35.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on radiopharmaceuticals and theranostics.", href: env === "explore" ? "#/ref/radiopharma" : "#/explore/radiopharma" },
        { title: "Companion Diagnostics & Biomarkers", text: "Co-developing PET imaging agents and CDx assays for targeted therapy.", href: "#/ref/cdx" },
        { title: "Sterile Manufacturing & Cleanrooms", text: "Aseptic processing, isolators, and Annex 1 / 21 CFR 211/212 controls.", href: "#/ref/sterile" },
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
    if 'radiopharma.js' not in txt:
        for anchor in ('import * as specialPopulations from "./special_populations.js";\n', 'import * as pricingAccess from "./pricing_access.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as radiopharma from "./radiopharma.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as radiopharma from "./radiopharma.js";\n' + txt
            changed = True
    if '"/ref/radiopharma"' not in txt:
        for anchor in ('if (path === "/ref/special-populations")', 'if (path === "/ref/pricing-access")', 'if (path === "/ref/controlled-substances")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/radiopharma") return { env: "ref", current: "#/ref/radiopharma", ...(await radiopharma.radiopharmaPage(query, "ref")) };\n  if (path === "/explore/radiopharma") return { env: "explore", current: "#/explore/radiopharma", ...(await radiopharma.radiopharmaPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/radiopharma" not in txt:
        for anchor in ('["#/ref/special-populations", "Special populations"]', '["#/ref/pricing-access", "Pricing, IRA & 340B"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/radiopharma", "Radiopharma & theranostics"]', 1)
                changed = True
                break
    if "#/explore/radiopharma" not in txt:
        for anchor in ('["#/explore/special-populations", "Special populations"]', '["#/explore/pricing-access", "Pricing, IRA & 340B"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/radiopharma", "Radiopharma & theranostics"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_radiopharma.py" in txt:
        return False
    line = "python3 pipeline/build_radiopharma.py site/data\n"
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
    if '"/api/radiopharma"' in txt:
        return False
    route = (
        '\n@app.get("/api/radiopharma")\n'
        'def api_radiopharma():\n'
        '    p = DATA_DIR / "radiopharma.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "radiopharma.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"radiopharma.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    rad_ref = _load(data_dir / "radiopharma.json", {}) or {}\n'
        '    for sec_key, sec_q in [("therapeutic_theranostics", "theranostics"), ("pet_cgmp_212", "pet"), ("rdrc_research", "rdrc"), ("nrc_licensing_supply", "nrc")]:\n'
        '        for item in (rad_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "radiopharma",\n'
        '                "group": "Radiopharma & Theranostics",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/radiopharma?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/radiopharma?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"radiopharmaceutical theranostics RPT alpha beta gamma dosimetry PET 21 CFR 212 FDAMA 121 EOS RDRC 21 CFR 361.1 NRC 10 CFR 35 {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"radiopharma", "#/ref/radiopharma"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    rad_doc = _load_json(data_dir / "radiopharma.json")\n'
        '    if isinstance(rad_doc, dict) and rad_doc.get("therapeutic_theranostics"):\n'
        '        rad_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (rad_doc.get("therapeutic_theranostics") or []) + (rad_doc.get("pet_cgmp_212") or []))\n'
        '        pages.append(("radiopharma", "#/ref/radiopharma", "Radiopharmaceuticals, Theranostics, PET cGMP & NRC Licensing",\n'
        '                      "Primary-sourced guide to oncology therapeutic radiopharmaceuticals, 21 CFR 212 PET drug cGMP, 21 CFR 361.1 RDRC, and NRC 10 CFR 35.",\n'
        '                      f"<ul>{rad_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/radiopharma"' in txt:
        return False
    for anchor in ('    "/#/explore/special-populations",', '    "/#/explore/pricing-access",', '    "/#/explore/controlled-substances",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/radiopharma",\n    "/#/explore/radiopharma",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_radiopharma_py": _write_if_changed(pipe_dir / "build_radiopharma.py", BUILD_RADIOPHARMA_PY),
        "radiopharma_js": _write_if_changed(js_dir / "radiopharma.js", RADIOPHARMA_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/special-populations") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/special-populations", "Special populations"]] }];\nconst EXPLORE_NAV = [["#/explore/special-populations", "Special populations"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/special-populations",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_radiopharma.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_radiopharma.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"therapeutic_theranostics": 6, "pet_cgmp_212": 6, "rdrc_research": 6, "nrc_licensing_supply": 6}, out

        doc = json.loads((root / "site" / "data" / "radiopharma.json").read_text(encoding="utf-8"))
        for k in ("therapeutic_theranostics", "pet_cgmp_212", "rdrc_research", "nrc_licensing_supply"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "radiopharma.js").read_text(encoding="utf-8")
        print("V62A_RADIOPHARMA_THERANOSTICS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2a Radiopharmaceuticals, Theranostics, PET cGMP & NRC Licensing patch.")
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
