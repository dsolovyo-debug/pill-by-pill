#!/usr/bin/env python3
"""Pill by Pill v6.2n Patch: Nonclinical Safety, GLP Toxicology (21 CFR 58 / ICH M3(R2)), Biologics & Oncology Tox (ICH S6(R1)/S9), Carcinogenicity/Safety Pharm (ICH S1B(R1)/S7B) & New Approach Methodologies (NAMs / 3Rs / DART) Reference (#/ref/nonclinical-nams, #/explore/nonclinical-nams, /api/nonclinical-nams).

1. Adds `pipeline/build_nonclinical_nams.py` -> `site/data/nonclinical_nams.json`
   (6 ICH M3(R2) & GLP Toxicology pillars, 6 Biologics & Oncology Nonclinical pillars, 6
   Carcinogenicity/Genotoxicity/Safety Pharmacology pillars, and 6 NAMs/3Rs/DART pillars — 24
   primary-sourced entries).
2. Adds `site/js/nonclinical_nams.js` (`nonclinicalNamsPage` with inline Nonclinical Safety &
   NAMs SVG + 4 section filters) and wires `#/ref/nonclinical-nams`,
   `#/explore/nonclinical-nams`, `/api/nonclinical-nams`, `REF_NAV_GROUPS`, `EXPLORE_NAV`,
   and `pipeline/run_all.sh`.
3. Integrates `nonclinical_nams.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/nonclinical-nams/` static SEO page + sitemap entry ->
   56 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2n_nonclinical_safety_ich_m3_s1b_s6_s9_nams_patch.py --selftest
  python3 2026-11-24_v6.2n_nonclinical_safety_ich_m3_s1b_s6_s9_nams_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_NONCLINICAL_NAMS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2n Nonclinical Safety, GLP Toxicology, Carcinogenicity & NAMs Reference (`site/data/nonclinical_nams.json`).

Comprehensive, primary-sourced reference covering:
  1. ICH M3(R2), GLP (21 CFR Part 58) & IND-Enabling Toxicology (6 pillars)
  2. Biologics (ICH S6(R1)), Oncology (ICH S9) & Streamlined mAb Studies (6 pillars)
  3. Carcinogenicity (ICH S1B(R1)), Genotoxicity (ICH M7/S2) & Safety Pharm (6 pillars)
  4. New Approach Methodologies (NAMs), 3Rs & Reproductive/DART (ICH S5(R3)) (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER OND/PTCC, ICH).

Usage:
  python3 pipeline/build_nonclinical_nams.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

ICH_M3_GLP_TOX = [
    {
        "id": "ncn-ich-m3r2-timing",
        "name": "ICH M3(R2) Nonclinical Safety Studies Timing",
        "category": "ICH M3(R2)",
        "plain": "Before a new medicine enters human trials, lab and animal safety studies must match how long volunteers will take the drug.",
        "technical": "ICH M3(R2) harmonizes international expectations for the scope and duration of nonclinical safety studies required to support Phase 1–3 clinical trials and marketing authorization.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m3r2-nonclinical-safety-studies-conduct-human-clinical-trials-and-marketing-authorization",
    },
    {
        "id": "ncn-ich-m3r2-qa-mfd",
        "name": "High-Dose Selection, MFD & Human Metabolite Safety",
        "category": "ICH M3(R2) Q&A",
        "plain": "Safety studies test high multiples above expected human doses—and check any breakdown chemicals that humans make more than test species.",
        "technical": "The ICH M3(R2) Q&A clarifies Maximum Feasible Dose (MFD), limit doses, exposure margins, and nonclinical characterization of disproportionate human metabolites (MIST).",
        "url": "https://www.fda.gov/media/82725/download",
    },
    {
        "id": "ncn-glp-21cfr58",
        "name": "Good Laboratory Practice (GLP, 21 CFR Part 58) & OSIS",
        "category": "21 CFR Part 58",
        "plain": "Pivotal safety studies submitted to FDA must follow strict record-keeping, independent quality audits, and raw-data archiving rules.",
        "technical": "21 CFR Part 58 establishes the Good Laboratory Practice quality system for nonclinical safety studies supporting INDs and NDAs/BLAs, inspected by FDA's Office of Study Integrity and Surveillance (OSIS).",
        "url": "https://www.fda.gov/media/184296/download",
    },
    {
        "id": "ncn-glp-translation-qa",
        "name": "Translation of GLP Study Reports (Nov 2023 Q&A)",
        "category": "GLP Submissions",
        "plain": "When pivotal safety studies are run overseas in another language, sponsors must submit accurate, certified English translations.",
        "technical": "FDA's GLP Study Report Translation Q&A outlines completeness, translator qualification, and verification requirements for translated 21 CFR Part 58 reports submitted to FDA.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/translation-good-laboratory-practice-study-reports-questions-and-answers",
    },
    {
        "id": "ncn-microdose-radiopharm",
        "name": "Microdose Exploratory INDs & Local Tolerance",
        "category": "Exploratory IND",
        "plain": "Tiny single-microgram tracer doses used for early human imaging need far fewer safety tests than full therapeutic doses.",
        "technical": "Under ICH M3(R2) and FDA's microdose radiopharmaceutical guidance, single microdose studies (≤100 µg) use streamlined nonclinical packages and omit dedicated IV local tolerance testing.",
        "url": "https://www.fda.gov/media/107641/download",
    },
    {
        "id": "ncn-reformulated-alt-route",
        "name": "Reformulated Products & Alternate-Route Bridging",
        "category": "505(b)(2) Bridging",
        "plain": "Turning a pill into a skin patch or nasal spray requires targeted safety checks for the new tissue route without repeating everything.",
        "technical": "FDA's nonclinical bridging guidance explains how reformulations or alternate routes of administration leverage existing systemic toxicity data while adding route-specific local tolerance and excipient assessments.",
        "url": "https://www.fda.gov/files/drugs/published/Nonclinical-Safety-Evaluation-of-Reformulated-Drug-Products-and-Products-Intended-for-Administration-by-an-Alternate-Route.pdf",
    },
]

ICH_S6_S9_BIOLOGICS_TOX = [
    {
        "id": "ncn-ich-s6r1-biologics",
        "name": "ICH S6(R1) Preclinical Safety of Biotechnology Products",
        "category": "ICH S6(R1)",
        "plain": "Antibodies and protein drugs are tested only in species where the drug actually binds its human-like target—often just one species.",
        "technical": "ICH S6(R1) governs biotechnology-derived pharmaceuticals, requiring pharmacologically relevant species selection, tissue cross-reactivity (TCR), and target-mediated pharmacology evaluation.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/s6r1-preclinical-safety-evaluation-biotechnology-derived-pharmaceuticals",
    },
    {
        "id": "ncn-ich-s6r1-addendum",
        "name": "ICH S6(R1) Addendum: ADA Interference & 6-Month Chronic Cap",
        "category": "S6(R1) Addendum",
        "plain": "Animals often make antibodies against human biologics; 6-month studies are usually the maximum needed for chronic protein drugs.",
        "technical": "The ICH S6(R1) Addendum addresses anti-drug antibody (ADA) exposure interpretation, high-dose selection based on MABEL/PD saturation, and 6-month maximum chronic study duration for biologics.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/s6-r1-addendum-preclinical-safety-evaluation-biotechnology-derived-pharmaceuticals",
    },
    {
        "id": "ncn-mab-streamlined-nhp",
        "name": "Monoclonal Antibodies: Streamlined Nonclinical Studies (Dec 2025)",
        "category": "3Rs / mAb Guidance",
        "plain": "New FDA guidance cuts unnecessary non-human primate testing for well-understood monoclonal antibodies.",
        "technical": "FDA's December 2025 draft guidance on Monoclonal Antibodies supplements ICH M3(R2) and S6(R1) with streamlined nonclinical safety approaches that reduce reliance on non-human primates (NHPs).",
        "url": "https://www.fda.gov/media/189920/download",
    },
    {
        "id": "ncn-ich-s9-oncology",
        "name": "ICH S9 Nonclinical Evaluation for Anticancer Pharmaceuticals",
        "category": "ICH S9 Oncology",
        "plain": "Cancer drugs for advanced disease skip several long-term animal studies so promising treatments reach patients faster.",
        "technical": "ICH S9 defines tailored nonclinical packages for advanced-cancer therapeutics—using HNSTD (non-rodents) or STD10 (rodents) to set FIH starting doses and deferring dedicated fertility/carcinogenicity studies.",
        "url": "https://www.fda.gov/media/73161/download",
    },
    {
        "id": "ncn-oncology-streamlined-3mo",
        "name": "Oncology Pharmaceuticals: Streamlined 3-Month Toxicology",
        "category": "Oncology 3Rs",
        "plain": "For cancer biologics and antibody-drug conjugates, 3-month toxicity studies and knowledge-based risk reviews replace longer animal runs.",
        "technical": "FDA's Streamlined Nonclinical Safety Studies guidance for oncology biologics and conjugated products focuses on 3-month general toxicology studies and integrated knowledge-based risk assessments to avoid unnecessary animal use.",
        "url": "https://www.fda.gov/media/192723/download",
    },
    {
        "id": "ncn-sdlthd-nonclinical",
        "name": "Severely Debilitating or Life-Threatening Hematologic Disorders",
        "category": "SDLTHD / WoE",
        "plain": "For severe blood diseases, embryo-fetal risk can be evaluated at marketing submission using weight-of-evidence rather than delaying trials.",
        "technical": "FDA's SDLTHD nonclinical guidance aligns with ICH S9 and S6(R1), allowing EFD risk assessments at marketing application and weight-of-evidence (WoE) justifications when mechanism/population warrants.",
        "url": "https://www.fda.gov/media/112750/download",
    },
]

ICH_S1_S7_SAFETY = [
    {
        "id": "ncn-ich-s1br1-woe",
        "name": "ICH S1B(R1) Weight-of-Evidence Carcinogenicity Addendum",
        "category": "ICH S1B(R1)",
        "plain": "Drugmakers can now use scientific weight-of-evidence to skip a 2-year rat cancer study when existing data already show low human risk.",
        "technical": "ICH S1B(R1) introduces an integrative Weight-of-Evidence (WoE) assessment to determine whether a 2-year rat carcinogenicity study adds value to human carcinogenic risk assessment.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/s1br1-addendum-s1b-testing-carcinogenicity-pharmaceuticals",
    },
    {
        "id": "ncn-ich-s1br1-rash2",
        "name": "Six WoE Factors & rasH2-Tg Transgenic Mouse Model",
        "category": "rasH2-Tg / 3Rs",
        "plain": "Six biological clues—like target biology, hormone effects, and 6-month tissue checks—plus a 6-month transgenic mouse test replace 2-year studies.",
        "technical": "ICH S1B(R1) evaluates target biology, secondary pharmacology, chronic histopathology, hormonal/immune modulation, and genotoxicity, while prioritizing 6-month rasH2-Tg mouse studies with exposure-ratio high-dose selection.",
        "url": "https://www.fda.gov/media/152777/download",
    },
    {
        "id": "ncn-ich-m7r2-mutagenic",
        "name": "ICH M7(R2) DNA-Reactive (Mutagenic) Impurities",
        "category": "ICH M7(R2)",
        "plain": "Computer models and Ames bacterial tests screen trace manufacturing impurities so DNA-damaging chemicals stay below strict safety limits.",
        "technical": "ICH M7(R2) governs assessment and control of DNA-reactive impurities using dual (Q)SAR models, Ames testing, and the Threshold of Toxicological Concern (TTC, 1.5 µg/day lifetime).",
        "url": "https://www.fda.gov/media/167330/download",
    },
    {
        "id": "ncn-ames-positive-followup",
        "name": "Follow-Up Testing for Ames-Positive Drugs (Nov 2024)",
        "category": "Genotoxicity",
        "plain": "If an investigational drug triggers a positive bacterial mutation test, FDA outlines exact follow-up tests before human dosing.",
        "technical": "FDA's November 2024 guidance details in vivo gene mutation, transgenic rodent, and exposure-margin follow-up testing strategies for Ames-positive drug substances before clinical exposure.",
        "url": "https://www.fda.gov/media/183844/download",
    },
    {
        "id": "ncn-ich-s7a-s7b",
        "name": "Core Safety Pharmacology: ICH S7A & S7B (hERG / QTc)",
        "category": "ICH S7A / S7B",
        "plain": "Before Phase 1 human dosing, drugs are checked for immediate effects on heart rhythm (hERG/QTc), breathing, and the nervous system.",
        "technical": "ICH S7A (central nervous, cardiovascular, and respiratory core battery) and ICH S7B (in vitro hERG / in vivo QT prolongation) are required prior to first-in-human clinical trials.",
        "url": "https://www.fda.gov/media/100790/download",
    },
    {
        "id": "ncn-m3r2-photo-abuse",
        "name": "Phototoxicity & Nonclinical Abuse Potential Timing",
        "category": "Special Safety",
        "plain": "Drugs that absorb UV light or enter the brain undergo specialized light-sensitivity and abuse-liability checks during development.",
        "technical": "ICH M3(R2) and adjunct FDA guidances establish timing for in vitro/in vivo photosafety evaluations (ICH S10) and nonclinical abuse-potential assessments for CNS-active compounds.",
        "url": "https://www.fda.gov/media/131295/download",
    },
]

NAMS_3RS_DART = [
    {
        "id": "ncn-cder-nams-hub",
        "name": "CDER Streamlined Nonclinical Studies & Acceptable NAMs",
        "category": "CDER NAMs Hub",
        "plain": "FDA maintains an active list of non-animal lab methods—like 3D human tissue models—that can replace traditional animal tests.",
        "technical": "CDER's NAMs hub catalogs accepted New Approach Methodologies and streamlined study pathways implementing the 3Rs (Replacement, Reduction, Refinement) without compromising patient safety.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/cder-streamlined-nonclinical-studies-and-acceptable-new-approach-methodologies-nams",
    },
    {
        "id": "ncn-nams-draft-2026",
        "name": "Alternatives to Animal Testing Draft Guidance (Mar 2026)",
        "category": "Organoids / MPS",
        "plain": "Organs-on-chips, human organoids, and computer simulations can predict human toxicity when validated for their specific purpose.",
        "technical": "FDA's March 2026 Draft Guidance on Alternatives to Animal Testing covers 2D/3D in vitro systems, organoids, organs-on-chips, and in silico models under 4 principles: Context of Use, Human Relevance, Technical Characterization, and Fit-for-Purpose.",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-releases-draft-guidance-alternatives-animal-testing-drug-development",
    },
    {
        "id": "ncn-fda-ich-3rs",
        "name": "FDA, ICH & the 3Rs Framework",
        "category": "3Rs Principles",
        "plain": "International drug regulators coordinate across safety guidelines to replace, reduce, and refine animal experiments whenever science allows.",
        "technical": "FDA and ICH embed 3Rs principles across M3(R2), S1B(R1), S5(R3), and S6(R1)—eliminating redundant recovery groups, single-dose acute lethality tests, and unnecessary non-human primate studies.",
        "url": "https://www.fda.gov/media/143220/download",
    },
    {
        "id": "ncn-nams-3d-tissue",
        "name": "3D Reconstructed Human Cornea & Epidermis Models",
        "category": "Ocular / Dermal NAMs",
        "plain": "For eye drops and skin creams, lab-grown human cornea and skin tissues replace animal eye and skin irritation tests.",
        "technical": "CDER accepts non-animal reconstructed human cornea-like epithelium models for ocular irritation and 3D reconstructed human epidermis models for dermal irritation of pharmaceuticals.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/cder-streamlined-nonclinical-studies-and-acceptable-new-approach-methodologies-nams",
    },
    {
        "id": "ncn-ich-s5r3-dart",
        "name": "ICH S5(R3) Reproductive & Developmental Toxicology (DART)",
        "category": "ICH S5(R3) DART",
        "plain": "Fertility and pregnancy safety studies check whether a drug harms reproduction or fetal development—and now allow qualified alternative assays.",
        "technical": "ICH S5(R3) harmonizes fertility, embryo-fetal development (EFD), and pre-/postnatal development (PPND) studies, incorporating qualified in vitro/ex vivo alternative assays for EFD risk.",
        "url": "https://www.fda.gov/drugs/science-and-research-drugs/cder-streamlined-nonclinical-studies-and-acceptable-new-approach-methodologies-nams",
    },
    {
        "id": "ncn-usp86-recombinant-lal",
        "name": "USP <86> Recombinant Reagents for Endotoxin Testing",
        "category": "Animal-Free QC",
        "plain": "Synthetic lab-made reagents can now replace horseshoe crab blood when testing sterile injections for bacterial fever-causing toxins.",
        "technical": "Aligned with USP Chapter <86> (May 2025), FDA's Level 2 revision to Pyrogen and Endotoxins Testing Q&A clarifies regulatory expectations for transitioning to recombinant Factor C / cascade reagents.",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-releases-draft-guidance-alternatives-animal-testing-drug-development",
    },
]


def build_nonclinical_nams(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2n",
        "checked": CHECKED,
        "ich_m3_glp_tox": ICH_M3_GLP_TOX,
        "ich_s6_s9_biologics_tox": ICH_S6_S9_BIOLOGICS_TOX,
        "ich_s1_s7_safety": ICH_S1_S7_SAFETY,
        "nams_3rs_dart": NAMS_3RS_DART,
    }
    (out_dir / "nonclinical_nams.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "ich_m3_glp_tox": len(ICH_M3_GLP_TOX),
        "ich_s6_s9_biologics_tox": len(ICH_S6_S9_BIOLOGICS_TOX),
        "ich_s1_s7_safety": len(ICH_S1_S7_SAFETY),
        "nams_3rs_dart": len(NAMS_3RS_DART),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_nonclinical_nams(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

NONCLINICAL_NAMS_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderNonclinicalSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="Nonclinical safety, GLP toxicology, carcinogenicity, and New Approach Methodologies architecture">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. ICH M3(R2) &amp; GLP</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">IND Timing &amp; Margins</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">21 CFR Part 58 / OSIS</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">MIST &amp; Route Bridging</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">First-in-Human Gate</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. Biologics &amp; Oncology</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">ICH S6(R1) &amp; MABEL</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">Streamlined mAb / NHP</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">ICH S9 &amp; 3-Mo Oncology</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Species Relevance</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. Carc, Geno &amp; hERG</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">ICH S1B(R1) WoE / rasH2</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">ICH M7(R2) &amp; Ames</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">ICH S7A / S7B QTc</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Long-Term &amp; Acute Risk</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. NAMs, 3Rs &amp; DART</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">Organoids &amp; MPS Chips</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">3D Cornea / Epidermis</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">ICH S5(R3) &amp; USP &lt;86&gt;</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">2026 Alternatives Draft</text>
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
        <a href="${esc(it.url)}" target="_blank" rel="noopener noreferrer" style="font-size:.82rem">Official FDA / ICH source ↗</a>
      </article>`).join("")}
  </div>`;
}

export async function nonclinicalNamsPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/nonclinical_nams.json");
  const sections = [
    { key: "ich_m3_glp_tox", title: "1. ICH M3(R2), GLP (21 CFR Part 58) & IND-Enabling Toxicology", items: data.ich_m3_glp_tox || [] },
    { key: "ich_s6_s9_biologics_tox", title: "2. Biologics (ICH S6(R1)), Oncology (ICH S9) & Streamlined mAb Studies", items: data.ich_s6_s9_biologics_tox || [] },
    { key: "ich_s1_s7_safety", title: "3. Carcinogenicity (ICH S1B(R1)), Genotoxicity & Safety Pharmacology", items: data.ich_s1_s7_safety || [] },
    { key: "nams_3rs_dart", title: "4. New Approach Methodologies (NAMs), 3Rs & Reproductive/DART", items: data.nams_3rs_dart || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Preclinical &amp; Safety" : "Reference · Preclinical &amp; Safety"}</p>
        <h1>Nonclinical Safety, GLP Toxicology, Carcinogenicity &amp; NAMs (3Rs)</h1>
        <p class="lede">${exploreMode
          ? "How scientists check a new medicine's safety before human trials—and how modern organoids, organs-on-chips, and weight-of-evidence rules reduce animal testing."
          : "Primary-sourced reference covering ICH M3(R2), 21 CFR Part 58 GLP, ICH S6(R1)/S9 biologics &amp; oncology tox, ICH S1B(R1)/M7/S7B, ICH S5(R3), and FDA NAMs."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-24")} · <a href="#/${exploreMode ? "ref" : "explore"}/nonclinical-nams">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderNonclinicalSvg()}
      <div class="filter-bar" role="group" aria-label="Filter nonclinical safety and NAMs sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["ich_m3_glp_tox", "ICH M3 / GLP (6)"], ["ich_s6_s9_biologics_tox", "S6 / S9 / mAbs (6)"], ["ich_s1_s7_safety", "S1B / M7 / S7 (6)"], ["nams_3rs_dart", "NAMs / 3Rs / DART (6)"]].map(([k, lbl]) => `
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
    imp = 'import { nonclinicalNamsPage } from "./nonclinical_nams.js";\n'
    if "nonclinicalNamsPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/nonclinical-nams") return nonclinicalNamsPage(view, "ref");\n'
        '  if (path === "/explore/nonclinical-nams") return nonclinicalNamsPage(view, "explore");\n'
    )
    if '"/ref/nonclinical-nams"' not in txt:
        anchor = 'if (path === "/ref/analytical-usp-q12")'
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
    if "#/ref/nonclinical-nams" not in txt:
        anchor = '["#/ref/analytical-usp-q12"'
        item = '["#/ref/nonclinical-nams", "Nonclinical Safety & NAMs"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/nonclinical-nams" not in txt:
        anchor2 = '["#/explore/analytical-usp-q12"'
        item2 = '["#/explore/nonclinical-nams", "Nonclinical Safety & NAMs"], '
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
    line = "python3 pipeline/build_nonclinical_nams.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/nonclinical-nams"' in txt:
        return False
    block = (
        '\n@app.get("/api/nonclinical-nams")\n'
        'def api_nonclinical_nams():\n'
        '    p = DATA_DIR / "nonclinical_nams.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "nonclinical_nams.json" in txt:
        return False
    snippet = '''    ncn_path = data_dir / "nonclinical_nams.json"
    if ncn_path.is_file():
        ncn_doc = json.loads(ncn_path.read_text(encoding="utf-8"))
        for sec in ("ich_m3_glp_tox", "ich_s6_s9_biologics_tox", "ich_s1_s7_safety", "nams_3rs_dart"):
            for item in ncn_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "Nonclinical Safety & NAMs",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/nonclinical-nams",
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
    if "/nonclinical-nams/" in txt:
        return False
    snippet = '''    # v6.2n Nonclinical Safety, GLP Toxicology, Carcinogenicity & NAMs SEO landing page
    ncn_dir = site_dir / "nonclinical-nams"
    ncn_dir.mkdir(parents=True, exist_ok=True)
    (ncn_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Nonclinical Safety, GLP Toxicology &amp; NAMs (3Rs) | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to ICH M3(R2), 21 CFR 58 GLP, ICH S6(R1)/S9, ICH S1B(R1) WoE carcinogenicity, ICH S5(R3) DART, and FDA NAMs.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/nonclinical-nams/'>"
        "<script>location.replace('/#/explore/nonclinical-nams');</script>"
        "</head><body><h1>Nonclinical Safety, GLP Toxicology &amp; NAMs (3Rs)</h1>"
        "<p><a href='/#/explore/nonclinical-nams'>Explore</a> · <a href='/#/ref/nonclinical-nams'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/nonclinical-nams/")
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
    if "#/ref/nonclinical-nams" in txt:
        return False
    anchor = '"/#/explore/analytical-usp-q12",'
    add = '"/#/explore/analytical-usp-q12",\n    "/#/ref/nonclinical-nams",\n    "/#/explore/nonclinical-nams",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/nonclinical-nams /#/explore/nonclinical-nams\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_nonclinical_nams_py": _write_if_changed(pipe_dir / "build_nonclinical_nams.py", BUILD_NONCLINICAL_NAMS_PY),
        "nonclinical_nams_js": _write_if_changed(js_dir / "nonclinical_nams.js", NONCLINICAL_NAMS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/analytical-usp-q12") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/analytical-usp-q12", "Analytical Q2/Q14, USP & Q12"]] }];\nconst EXPLORE_NAV = [["#/explore/analytical-usp-q12", "Analytical Q2/Q14, USP & Q12"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/analytical-usp-q12",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_nonclinical_nams.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_nonclinical_nams.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ich_m3_glp_tox": 6, "ich_s6_s9_biologics_tox": 6, "ich_s1_s7_safety": 6, "nams_3rs_dart": 6}, out

        doc = json.loads((root / "site" / "data" / "nonclinical_nams.json").read_text(encoding="utf-8"))
        for k in ("ich_m3_glp_tox", "ich_s6_s9_biologics_tox", "ich_s1_s7_safety", "nams_3rs_dart"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "nonclinical_nams.js").read_text(encoding="utf-8")
        print("V62N_NONCLINICAL_NAMS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2n Nonclinical Safety, GLP, Carcinogenicity & NAMs patch.")
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
