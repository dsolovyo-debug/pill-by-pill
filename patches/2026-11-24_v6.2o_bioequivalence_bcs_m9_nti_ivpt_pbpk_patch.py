#!/usr/bin/env python3
"""Pill by Pill v6.2o Patch: Bioavailability & Bioequivalence (21 CFR 320 / RSABE), BCS Biowaivers (ICH M9), Narrow Therapeutic Index (NTI) & Food-Effect Studies, and Topical IVRT/IVPT & PBPK Reference (#/ref/babe-bcs-nti, #/explore/babe-bcs-nti, /api/babe-bcs-nti).

1. Adds `pipeline/build_babe_bcs_nti.py` -> `site/data/babe_bcs_nti.json`
   (6 Bioequivalence & RSABE pillars, 6 BCS Class I/III Biowaivers ICH M9 pillars, 6 NTI &
   Food-Effect pillars, and 6 Topical IVRT/IVPT & PBPK pillars — 24 primary-sourced entries).
2. Adds `site/js/babe_bcs_nti.js` (`babeBcsNtiPage` with inline BA/BE, BCS & NTI SVG + 4
   section filters) and wires `#/ref/babe-bcs-nti`, `#/explore/babe-bcs-nti`,
   `/api/babe-bcs-nti`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `babe_bcs_nti.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/babe-bcs-nti/` static SEO page + sitemap entry ->
   57 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2o_bioequivalence_bcs_m9_nti_ivpt_pbpk_patch.py --selftest
  python3 2026-11-24_v6.2o_bioequivalence_bcs_m9_nti_ivpt_pbpk_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_BABE_BCS_NTI_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2o Bioavailability, Bioequivalence, BCS M9, NTI & IVPT/PBPK Reference (`site/data/babe_bcs_nti.json`).

Comprehensive, primary-sourced reference covering:
  1. Bioequivalence Fundamentals, Crossover Designs & RSABE (6 pillars)
  2. BCS Class I & III Biowaivers (ICH M9) & Dissolution (6 pillars)
  3. Narrow Therapeutic Index (NTI) Drugs & Food-Effect Studies (6 pillars)
  4. Topical IVRT / IVPT & Model-Integrated PBPK Bioequivalence (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER OGD/OCP, ICH).

Usage:
  python3 pipeline/build_babe_bcs_nti.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

BE_FUNDAMENTALS_RSABE = [
    {
        "id": "bbn-stat-approaches-be",
        "name": "Statistical Approaches to Establishing Bioequivalence (May 2026)",
        "category": "FDA BE Guidance",
        "plain": "To prove a generic pill matches a brand-name drug, its blood-level curves must fall within strict statistical boundaries.",
        "technical": "FDA's May 2026 Statistical Approaches to Establishing Bioequivalence guidance defines parametric, non-parametric, and scaled statistical criteria for demonstrating average bioequivalence across NDAs and ANDAs.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/statistical-approaches-establishing-bioequivalence",
    },
    {
        "id": "bbn-ba-ndas-inds",
        "name": "Bioavailability (BA) Studies in NDAs & INDs",
        "category": "BA / 21 CFR 320",
        "plain": "Bioavailability measures how fast and how completely a medicine reaches the bloodstream—whether swallowed, injected, or absorbed.",
        "technical": "FDA's April 2022 Bioavailability Studies guidance covers relative BA, absolute BA (versus IV reference), fed comparability, and formulation bridging under INDs and NDAs.",
        "url": "https://www.fda.gov/media/157685/download",
    },
    {
        "id": "bbn-be-pk-endpoints-anda",
        "name": "PK-Endpoint Bioequivalence for ANDA Generics",
        "category": "ANDA BE",
        "plain": "Generic drugmakers compare peak blood concentration (Cmax) and total drug exposure (AUC) against the Reference Listed Drug.",
        "technical": "FDA's Bioequivalence Studies With Pharmacokinetic Endpoints guidance establishes fasting and fed PK study designs, analyte selection, and fed BE expectations for ANDAs.",
        "url": "https://www.fda.gov/media/192774/download",
    },
    {
        "id": "bbn-rsabe-highly-variable",
        "name": "Reference-Scaled Average Bioequivalence (RSABE)",
        "category": "Highly Variable Drugs",
        "plain": "For drugs whose absorption naturally varies a lot from day to day, FDA scales the bioequivalence window to the brand drug's own variability.",
        "technical": "Reference-Scaled Average Bioequivalence (RSABE) adjusts BE acceptance limits using the within-subject standard deviation (s_WR) of the reference product in replicate crossover studies.",
        "url": "https://www.fda.gov/media/163638/download",
    },
    {
        "id": "bbn-tost-80-125",
        "name": "Two-Treatment Crossover & 80.00–125.00% (90% CI) Rule",
        "category": "TOST / 90% CI",
        "plain": "The 90% confidence interval for the generic-to-brand ratio of peak and total blood levels must stay inside 80% to 125%.",
        "technical": "Using Two One-Sided Tests (TOST) on log-transformed AUC and Cmax in a standard 2-treatment, 2-period crossover design, the 90% confidence interval of the geometric mean ratio must fall within 80.00%–125.00%.",
        "url": "https://www.fda.gov/media/167453/download",
    },
    {
        "id": "bbn-ba-nda-overview",
        "name": "NDAs & INDs General BA Considerations Portal",
        "category": "21 CFR 320",
        "plain": "Early formulation changes during clinical trials also rely on bioavailability bridging studies to keep dosing consistent.",
        "technical": "FDA's General Considerations portal anchors BA requirements for NDA 505(b)(1)/505(b)(2) submissions, in vitro dissolution support, and special-dosage-form BA assessments.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/bioavailability-studies-submitted-ndas-or-inds-general-considerations",
    },
]

BCS_M9_BIOWAIVERS = [
    {
        "id": "bbn-ich-m9-portal",
        "name": "ICH M9 Biopharmaceutics Classification System-Based Biowaivers",
        "category": "ICH M9 Final",
        "plain": "When an oral drug dissolves easily and absorbs predictably, lab dissolution tests can replace human bioequivalence trials.",
        "technical": "ICH M9 (May 2021) harmonizes BCS-based biowaivers globally, waiving in vivo BE studies when immediate-release solid oral dosage forms meet strict solubility, permeability, and dissolution criteria.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m9-biopharmaceutics-classification-system-based-biowaivers",
    },
    {
        "id": "bbn-m9-high-solubility",
        "name": "High Solubility: Highest Dose in ≤250 mL (pH 1.2–6.8)",
        "category": "BCS Solubility",
        "plain": "A drug counts as highly soluble if its largest single dose dissolves completely in one glass of water (250 mL) across stomach-to-gut acidity.",
        "technical": "Under ICH M9 Section 2.1, a drug substance is highly soluble if the highest single therapeutic dose dissolves completely in ≤250 mL of aqueous media over pH 1.2–6.8 at 37 ± 1 °C.",
        "url": "https://www.fda.gov/media/148472/download",
    },
    {
        "id": "bbn-m9-class1-class3",
        "name": "BCS Class I & Class III Eligibility & Salt Rules",
        "category": "Class I vs. III",
        "plain": "BCS Class I (high solubility, high permeability) and Class III (high solubility, low permeability) can qualify—with stricter excipient rules for Class III.",
        "technical": "ICH M9 permits biowaivers for BCS Class I and III immediate-release products with identical drug substances (or different BCS Class I salts), while excluding different esters, ethers, or isomers.",
        "url": "https://www.fda.gov/media/148472/download",
    },
    {
        "id": "bbn-m9-caco2-permeability",
        "name": "Caco-2 Permeability, Mass Balance (≥80%) & Passive Transport",
        "category": "BCS Permeability",
        "plain": "Scientists measure how well a drug crosses human gut-cell layers in the lab compared against trusted reference standards.",
        "technical": "ICH M9 validates high permeability using human PK (≥85% absorption) or validated Caco-2 cell monolayers with high-permeability internal standards, ≥80% recovery/mass balance, and passive transport verification.",
        "url": "https://www.fda.gov/media/148472/download",
    },
    {
        "id": "bbn-m9-qa-fdc",
        "name": "ICH M9 Q&A: Non-Linear PK & Fixed-Dose Combinations",
        "category": "ICH M9 Q&A",
        "plain": "For combination pills containing two medicines, every active ingredient must qualify for a BCS biowaiver—not just one.",
        "technical": "The ICH M9 Q&A clarifies that drugs with non-linear PK remain eligible if they meet BCS I/III criteria, whereas all APIs in a fixed-dose combination (FDC) must independently qualify.",
        "url": "https://www.fda.gov/media/167742/download",
    },
    {
        "id": "bbn-generic-be-dissolution",
        "name": "Generic BE Studies & Comparative Dissolution (f2)",
        "category": "Generic BE / f2",
        "plain": "Comparative dissolution curves ensure generic tablets break down and release drug at the same speed as the brand product.",
        "technical": "FDA's generic bioequivalence guidances and Product-Specific Guidances (PSGs) integrate multi-pH dissolution similarity factor (f2 ≥ 50) testing alongside in vivo PK endpoints.",
        "url": "https://www.fda.gov/media/166152/download",
    },
]

NTI_FOOD_EFFECT = [
    {
        "id": "bbn-nti-working-group",
        "name": "CDER Narrow Therapeutic Index (NTI) Drugs Standards",
        "category": "NTI Standards",
        "plain": "For drugs where even a tiny dose shift can cause toxicity or treatment failure—like warfarin or tacrolimus—FDA enforces extra-tight generic limits.",
        "technical": "CDER's Narrow Therapeutic Index (NTI) Working Group establishes tightened bioequivalence and pharmaceutical quality standards for drugs with small margins between minimum effective and minimum toxic concentrations.",
        "url": "https://www.fda.gov/drugs/cder-conversations/setting-and-implementing-standards-narrow-therapeutic-index-drugs",
    },
    {
        "id": "bbn-nti-generic-overview",
        "name": "Understanding Generic Narrow Therapeutic Index Drugs",
        "category": "NTI Generics",
        "plain": "Tighter manufacturing and blood-level rules ensure patients can safely switch between brand and generic NTI medicines.",
        "technical": "FDA's NTI framework tightens both bioequivalence acceptance intervals and batch-to-batch assay/content-uniformity specifications reflected in Product-Specific Guidances (PSGs).",
        "url": "https://www.fda.gov/media/162779/download",
    },
    {
        "id": "bbn-nti-4period-replicate",
        "name": "4-Period, 2-Sequence Replicate Crossover (TRTR / RTRT)",
        "category": "NTI Trial Design",
        "plain": "Generic NTI trials give each volunteer both the brand and generic pills twice to measure day-to-day consistency.",
        "technical": "FDA evaluates NTI bioequivalence (therapeutic index ≤ 3) using a 4-period, 2-sequence full replicate crossover trial (TRTR and RTRT) comparing both mean exposure and within-subject variability.",
        "url": "https://www.fda.gov/files/drugs/published/Pharmacometric-Approach-To-Define-Narrow-Therapeutic-Index-(NTI)-Drugs---Evaluate-Bioequivalence-(BE)-Criteria-for-NTI-Drugs.pdf",
    },
    {
        "id": "bbn-nti-scaled-limits",
        "name": "Tightened Scaled Average Bioequivalence for NTI Drugs",
        "category": "NTI Statistics",
        "plain": "For NTI drugs, the generic must pass both a tightened scaled check and a direct variability comparison against the brand drug.",
        "technical": "Under FDA's NTI statistical method, reference-scaled BE limits tighten with reference variability (plus an unscaled 80–125% check and an upper 90% CI bound on test-to-reference within-subject SD ratio).",
        "url": "https://www.fda.gov/media/167457/download",
    },
    {
        "id": "bbn-food-effect-2026",
        "name": "Assessing Effects of Food on Drugs in INDs & NDAs (May 2026)",
        "category": "Food-Effect Guidance",
        "plain": "High-fat meals can boost or block pill absorption—food-effect trials tell patients whether to take a drug with food or on an empty stomach.",
        "technical": "FDA's May 2026 Clinical Pharmacology guidance specifies when and how to run food-effect studies under INDs/NDAs to evaluate meal-induced changes in Cmax and AUC.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessing-effects-food-drugs-inds-and-ndas-clinical-pharmacology-considerations",
    },
    {
        "id": "bbn-food-effect-labeling",
        "name": "Meal Types & Prescribing Information Dosing Instructions",
        "category": "Food Labeling",
        "plain": "Food-effect data translate directly into clear label instructions like 'take on an empty stomach 1 hour before meals.'",
        "technical": "FDA's food-effect assessment evaluates high-fat and low-fat meals relative to fasted dosing to translate clinically meaningful PK shifts into actionable Prescribing Information dosing instructions.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/guidance-recap-podcast-assessing-effects-food-drugs-inds-and-ndas-clinical-pharmacology",
    },
]

IVPT_IVRT_MIE = [
    {
        "id": "bbn-ivrt-topical",
        "name": "In Vitro Release Test (IVRT) for Topical Semisolids",
        "category": "Topical IVRT",
        "plain": "For skin creams and gels, diffusion cells measure how fast the active ingredient leaves the cream—avoiding massive clinical trials.",
        "technical": "FDA's IVRT guidance details method development, validation, and pivotal comparative release-rate testing for generic topical dermatologic products submitted in ANDAs.",
        "url": "https://www.fda.gov/media/162476/download",
    },
    {
        "id": "bbn-ivpt-human-skin",
        "name": "In Vitro Permeation Test (IVPT) Using Excised Human Skin",
        "category": "Topical IVPT",
        "plain": "IVPT tracks how much drug actually passes through real human donor skin samples into a receptor chamber over time.",
        "technical": "FDA's IVPT guidance governs cutaneous pharmacokinetic (flux J_max and total cumulative amount AMT) bioequivalence studies using excised human skin with verified barrier integrity.",
        "url": "https://www.fda.gov/media/162475/download",
    },
    {
        "id": "bbn-ivpt-step-by-step",
        "name": "Implementing FDA IVPT Guidance Recommendations",
        "category": "IVPT Execution",
        "plain": "Step-by-step FDA workshops help generic developers qualify skin donors, diffusion cells, and statistical comparisons.",
        "technical": "CDER's SBIA IVPT implementation training walks sponsors through skin-source qualification, pilot/pivotal donor dosing, and scaled statistical BE evaluation.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/implementing-fdas-ivpt-guidance-recommendations-step-step-illustration-04292025",
    },
    {
        "id": "bbn-usp-1724-ivrt-ivpt",
        "name": "USP <1724> Semisolid Performance & Cutaneous PK",
        "category": "USP <1724>",
        "plain": "Standardized vertical diffusion cells (Franz cells) under USP <1724> keep topical release testing consistent across labs.",
        "technical": "FDA links IVRT pivotal comparisons to USP General Chapter <1724> (Semisolid Drug Products—Performance Tests) while distinguishing IVRT release kinetics from IVPT cutaneous permeation.",
        "url": "https://www.fda.gov/media/110389/download",
    },
    {
        "id": "bbn-char-based-be-swr",
        "name": "Characterization-Based BE & Variability Thresholds",
        "category": "Complex Topicals",
        "plain": "When a generic cream matches the brand's exact physical structure (Q3) plus IVRT/IVPT, it can prove equivalence without a patient efficacy trial.",
        "technical": "Characterization-based bioequivalence combines Q1/Q2/Q3 microstructure equivalence with IVRT and IVPT, applying reference-scaled or unscaled BE criteria depending on s_WR (< 0.294 vs ≥ 0.294).",
        "url": "https://www.fda.gov/media/173388/download",
    },
    {
        "id": "bbn-pbpk-virtual-be",
        "name": "Physiologically Based Pharmacokinetic (PBPK) & Virtual BE",
        "category": "Model-Integrated BE",
        "plain": "Computer simulations of human gut, skin, or lung absorption can support bioequivalence decisions and optimize trial design.",
        "technical": "FDA's PBPK and Model-Integrated Evidence (MIE) framework enables mechanistic absorption modeling and virtual bioequivalence simulations to support PSGs, food-effect, and complex generic approvals.",
        "url": "https://www.fda.gov/media/192774/download",
    },
]


def build_babe_bcs_nti(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2o",
        "checked": CHECKED,
        "be_fundamentals_rsabe": BE_FUNDAMENTALS_RSABE,
        "bcs_m9_biowaivers": BCS_M9_BIOWAIVERS,
        "nti_food_effect": NTI_FOOD_EFFECT,
        "ivpt_ivrt_mie": IVPT_IVRT_MIE,
    }
    (out_dir / "babe_bcs_nti.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "be_fundamentals_rsabe": len(BE_FUNDAMENTALS_RSABE),
        "bcs_m9_biowaivers": len(BCS_M9_BIOWAIVERS),
        "nti_food_effect": len(NTI_FOOD_EFFECT),
        "ivpt_ivrt_mie": len(IVPT_IVRT_MIE),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_babe_bcs_nti(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

BABE_BCS_NTI_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderBabeSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="Bioavailability, bioequivalence, BCS M9 biowaivers, NTI, and IVPT/PBPK architecture">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. BA/BE &amp; RSABE</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">AUC &amp; Cmax (90% CI)</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">80.00–125.00% TOST</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">RSABE Highly Variable</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">21 CFR Part 320</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. BCS M9 Biowaivers</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">Class I &amp; Class III</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">≤250 mL (pH 1.2–6.8)</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">Caco-2 &amp; f2 ≥ 50</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Waive In Vivo BE</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. NTI &amp; Food Effect</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">TRTR / RTRT 4-Period</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">Tightened NTI Limits</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">2026 Food-Effect Rules</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">TI ≤ 3 &amp; Meal Dosing</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. IVRT / IVPT &amp; PBPK</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">USP &lt;1724&gt; Franz Cells</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">Excised Human Skin</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">Q3 &amp; Virtual BE (PBPK)</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Model-Integrated BE</text>
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

export async function babeBcsNtiPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/babe_bcs_nti.json");
  const sections = [
    { key: "be_fundamentals_rsabe", title: "1. Bioequivalence Fundamentals, Crossover Designs & RSABE", items: data.be_fundamentals_rsabe || [] },
    { key: "bcs_m9_biowaivers", title: "2. BCS Class I & III Biowaivers (ICH M9) & Dissolution", items: data.bcs_m9_biowaivers || [] },
    { key: "nti_food_effect", title: "3. Narrow Therapeutic Index (NTI) Drugs & Food-Effect Studies", items: data.nti_food_effect || [] },
    { key: "ivpt_ivrt_mie", title: "4. Topical IVRT / IVPT & Model-Integrated PBPK Bioequivalence", items: data.ivpt_ivrt_mie || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Clinical Pharmacology &amp; Generics" : "Reference · Clinical Pharmacology &amp; Generics"}</p>
        <h1>Bioequivalence (BA/BE), BCS M9 Biowaivers, NTI Drugs &amp; IVPT / PBPK</h1>
        <p class="lede">${exploreMode
          ? "How FDA proves a generic pill, cream, or reformulated medicine delivers the exact same blood levels and effect as the original brand product."
          : "Primary-sourced reference covering 21 CFR Part 320 BA/BE, 80–125% TOST &amp; RSABE, ICH M9 BCS biowaivers, 4-period NTI replicate designs, food-effect studies, IVRT/IVPT, and PBPK."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-24")} · <a href="#/${exploreMode ? "ref" : "explore"}/babe-bcs-nti">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderBabeSvg()}
      <div class="filter-bar" role="group" aria-label="Filter bioequivalence, BCS M9, NTI, and IVPT sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["be_fundamentals_rsabe", "BA/BE & RSABE (6)"], ["bcs_m9_biowaivers", "BCS M9 (6)"], ["nti_food_effect", "NTI & Food (6)"], ["ivpt_ivrt_mie", "IVRT/IVPT & PBPK (6)"]].map(([k, lbl]) => `
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
    imp = 'import { babeBcsNtiPage } from "./babe_bcs_nti.js";\n'
    if "babeBcsNtiPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/babe-bcs-nti") return babeBcsNtiPage(view, "ref");\n'
        '  if (path === "/explore/babe-bcs-nti") return babeBcsNtiPage(view, "explore");\n'
    )
    if '"/ref/babe-bcs-nti"' not in txt:
        anchor = 'if (path === "/ref/nonclinical-nams")'
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
    if "#/ref/babe-bcs-nti" not in txt:
        anchor = '["#/ref/nonclinical-nams"'
        item = '["#/ref/babe-bcs-nti", "BA/BE, BCS M9, NTI & IVPT"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/babe-bcs-nti" not in txt:
        anchor2 = '["#/explore/nonclinical-nams"'
        item2 = '["#/explore/babe-bcs-nti", "BA/BE, BCS M9, NTI & IVPT"], '
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
    line = "python3 pipeline/build_babe_bcs_nti.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/babe-bcs-nti"' in txt:
        return False
    block = (
        '\n@app.get("/api/babe-bcs-nti")\n'
        'def api_babe_bcs_nti():\n'
        '    p = DATA_DIR / "babe_bcs_nti.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "babe_bcs_nti.json" in txt:
        return False
    snippet = '''    bbn_path = data_dir / "babe_bcs_nti.json"
    if bbn_path.is_file():
        bbn_doc = json.loads(bbn_path.read_text(encoding="utf-8"))
        for sec in ("be_fundamentals_rsabe", "bcs_m9_biowaivers", "nti_food_effect", "ivpt_ivrt_mie"):
            for item in bbn_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "BA/BE, BCS M9, NTI & IVPT",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/babe-bcs-nti",
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
    if "/babe-bcs-nti/" in txt:
        return False
    snippet = '''    # v6.2o Bioequivalence, BCS M9 Biowaivers, NTI & IVPT/PBPK SEO landing page
    bbn_dir = site_dir / "babe-bcs-nti"
    bbn_dir.mkdir(parents=True, exist_ok=True)
    (bbn_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Bioequivalence (BA/BE), BCS M9 Biowaivers, NTI &amp; IVPT/PBPK | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to 21 CFR 320 BA/BE, RSABE, ICH M9 BCS biowaivers, NTI replicate designs, food-effect studies, IVRT/IVPT, and PBPK.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/babe-bcs-nti/'>"
        "<script>location.replace('/#/explore/babe-bcs-nti');</script>"
        "</head><body><h1>Bioequivalence, BCS M9 Biowaivers, NTI &amp; IVPT/PBPK</h1>"
        "<p><a href='/#/explore/babe-bcs-nti'>Explore</a> · <a href='/#/ref/babe-bcs-nti'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/babe-bcs-nti/")
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
    if "#/ref/babe-bcs-nti" in txt:
        return False
    anchor = '"/#/explore/nonclinical-nams",'
    add = '"/#/explore/nonclinical-nams",\n    "/#/ref/babe-bcs-nti",\n    "/#/explore/babe-bcs-nti",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/babe-bcs-nti /#/explore/babe-bcs-nti\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_babe_bcs_nti_py": _write_if_changed(pipe_dir / "build_babe_bcs_nti.py", BUILD_BABE_BCS_NTI_PY),
        "babe_bcs_nti_js": _write_if_changed(js_dir / "babe_bcs_nti.js", BABE_BCS_NTI_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/nonclinical-nams") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/nonclinical-nams", "Nonclinical Safety & NAMs"]] }];\nconst EXPLORE_NAV = [["#/explore/nonclinical-nams", "Nonclinical Safety & NAMs"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/nonclinical-nams",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_babe_bcs_nti.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_babe_bcs_nti.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"be_fundamentals_rsabe": 6, "bcs_m9_biowaivers": 6, "nti_food_effect": 6, "ivpt_ivrt_mie": 6}, out

        doc = json.loads((root / "site" / "data" / "babe_bcs_nti.json").read_text(encoding="utf-8"))
        for k in ("be_fundamentals_rsabe", "bcs_m9_biowaivers", "nti_food_effect", "ivpt_ivrt_mie"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "babe_bcs_nti.js").read_text(encoding="utf-8")
        print("V62O_BABE_BCS_NTI_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2o BA/BE, BCS M9, NTI & IVPT/PBPK patch.")
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
