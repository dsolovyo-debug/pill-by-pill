#!/usr/bin/env python3
"""Pill by Pill v6.2m Patch: Analytical Method Validation (ICH Q2(R2)/Q14), USP-NF Compendia & Reference Standards, ICH Q12 Post-Approval Lifecycle Management & Stability Testing (ICH Q1) Reference (#/ref/analytical-usp-q12, #/explore/analytical-usp-q12, /api/analytical-usp-q12).

1. Adds `pipeline/build_analytical_usp_q12.py` -> `site/data/analytical_usp_q12.json`
   (6 ICH Q2(R2)/Q14 Analytical Validation & AQbD pillars, 6 USP-NF Compendia & Reference
   Standards pillars, 6 ICH Q12 Post-Approval Lifecycle Management pillars, and 6 Stability
   Testing ICH Q1/Q1A/Q1B/Q1E pillars — 24 primary-sourced entries).
2. Adds `site/js/analytical_usp_q12.js` (`analyticalUspQ12Page` with inline Analytical
   Lifecycle, Compendial Control & ICH Q12 SVG + 4 section filters) and wires
   `#/ref/analytical-usp-q12`, `#/explore/analytical-usp-q12`, `/api/analytical-usp-q12`,
   `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `analytical_usp_q12.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/analytical-usp-q12/` static SEO page + sitemap entry
   -> 55 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2m_analytical_q2_q14_usp_ich_q12_stability_patch.py --selftest
  python3 2026-11-24_v6.2m_analytical_q2_q14_usp_ich_q12_stability_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_ANALYTICAL_USP_Q12_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2m Analytical Validation (ICH Q2(R2)/Q14), USP Compendia, ICH Q12 & Stability Reference (`site/data/analytical_usp_q12.json`).

Comprehensive, primary-sourced reference covering:
  1. ICH Q2(R2) & Q14 Analytical Procedure Validation & AQbD (6 pillars)
  2. USP-NF Compendia, Reference Standards & Lab Controls (6 pillars)
  3. ICH Q12 Post-Approval Lifecycle Management & Established Conditions (6 pillars)
  4. Stability Testing: ICH Q1 Consolidated, Q1A(R2), Q1B Photostability & Q1E (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER OPQ, ICH).

Usage:
  python3 pipeline/build_analytical_usp_q12.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

ICH_Q2_Q14_AQBD = [
    {
        "id": "auq-ich-q2r2-validation",
        "name": "ICH Q2(R2) Validation of Analytical Procedures (Mar 2024)",
        "category": "ICH Q2(R2) Final",
        "plain": "Before a lab test can release medicines to patients, companies must prove the test accurately measures the active drug and catches impurities every single time.",
        "technical": "FDA's March 2024 ICH Q2(R2) Final Guidance modernizes validation principles for Specificity, Linearity, Range, Accuracy, and Precision—expanding coverage to spectroscopic and multivariate analytical procedures.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q2r2-validation-analytical-procedures",
    },
    {
        "id": "auq-ich-q14-development",
        "name": "ICH Q14 Analytical Procedure Development & AQbD",
        "category": "ICH Q14 Final",
        "plain": "Instead of guessing test settings by trial and error, scientists define what the test must measure up front and map out safe operating ranges.",
        "technical": "ICH Q14 (March 2024) establishes Minimal versus Enhanced (Analytical Quality by Design) development approaches using Analytical Target Profiles (ATPs), risk assessment, and Design of Experiments (DoE).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q14-analytical-procedure-development",
    },
    {
        "id": "auq-q14-platform-procedures",
        "name": "Platform Analytical Procedures & Abbreviated Validation",
        "category": "Platform Methods",
        "plain": "When a company uses the same proven test across similar antibody or gene therapy drugs, it does not have to re-invent the validation from scratch.",
        "technical": "ICH Q14 allows platform analytical procedures applied across multiple products with little or no modification to omit redundant validation tests using science- and risk-based justification and DoE robustness data.",
        "url": "https://www.fda.gov/media/161202/download",
    },
    {
        "id": "auq-q2r2-multivariate-spec",
        "name": "Multivariate & Spectroscopic Procedure Validation",
        "category": "Multivariate / PAT",
        "plain": "Modern laser and infrared sensors need special math checks—like calibration models and outlier detection—to prove their readings stay true.",
        "technical": "ICH Q2(R2) details validation performance characteristics for multivariate and spectroscopic procedures (e.g., NIR, Raman), requiring representative calibration sets, internal cross-validation, and external test sets.",
        "url": "https://www.fda.gov/media/161201/download",
    },
    {
        "id": "auq-q14-rtrt-lifecycle",
        "name": "Analytical Procedure Lifecycle & Real-Time Release Testing",
        "category": "Lifecycle / RTRT",
        "plain": "Lab tests are monitored throughout a medicine's commercial life so minor equipment or column updates stay scientifically controlled.",
        "technical": "ICH Q14 aligns analytical procedure lifecycle management with ICH Q8–Q13, supporting ongoing performance monitoring and PAT-driven multivariate models used for Real-Time Release Testing (RTRT).",
        "url": "https://www.fda.gov/media/165164/download",
    },
    {
        "id": "auq-q2-q14-postapproval",
        "name": "Risk-Based Post-Approval Analytical Change Management",
        "category": "Regulatory Flexibility",
        "plain": "Better scientific data during method development lets manufacturers update lab tests faster after approval without unnecessary regulatory delays.",
        "technical": "Combining ICH Q14 enhanced development knowledge with ICH Q2(R2) validation reduces recursive regulatory queries and supports risk-based post-approval analytical change flexibility.",
        "url": "https://www.fda.gov/media/177718/download",
    },
]

USP_COMPENDIA_STANDARDS = [
    {
        "id": "auq-usp-nf-recognition",
        "name": "USP-NF Statutory Recognition (FD&C Act § 501(b))",
        "category": "Official Compendia",
        "plain": "The United States Pharmacopeia–National Formulary (USP-NF) sets the official public legal benchmarks for drug strength, quality, and purity in the US.",
        "technical": "Under FD&C Act § 501(b), a drug recognized in USP-NF is deemed adulterated if its strength differs from or its quality or purity falls below official compendial monograph standards unless plainly labeled.",
        "url": "https://www.fda.gov/media/190668/download",
    },
    {
        "id": "auq-usp-revisions-299",
        "name": "Compendium Revisions, Deletions & 21 CFR 299.5 Differing Standards",
        "category": "CPG Sec. 420.200",
        "plain": "If a medicine differs in strength or purity from the current USP book, the label must state every exact difference clearly.",
        "technical": "FDA CPG Sec. 420.200 and 21 CFR 299.5 require products differing from current USP-NF standards to declare all respects and extents of difference, and prohibit claiming conformance to superseded monographs.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cpg-sec-420200-compendium-revisions-and-deletions",
    },
    {
        "id": "auq-usp-test-interference",
        "name": "Interference with Compendial Tests (General Notices § 5.20)",
        "category": "CPG Sec. 420.500",
        "plain": "A manufacturer cannot add inactive ingredients that block or distort the official USP quality test—even if an in-house test passes.",
        "technical": "Under CPG Sec. 420.500 and USP General Notices § 5.20, a compendial drug containing an added substance that interferes with the official compendial assay or test is adulterated under § 501(b).",
        "url": "https://www.fda.gov/media/84697/download",
    },
    {
        "id": "auq-usp-ref-standards-621",
        "name": "Reference Standards, System Suitability & USP <621> Chromatography",
        "category": "21 CFR 211.160 / 211.194",
        "plain": "Lab instruments must be calibrated against ultra-pure reference vials—never against regular finished pills from the same production batch.",
        "technical": "21 CFR 211.160(b)(4) and 211.194(c) require qualified primary or secondary reference standards and USP <621> system suitability testing; finished dosage forms or same-batch APIs cannot serve as system suitability standards.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/questions-and-answers-current-good-manufacturing-practice-requirements-laboratory-controls",
    },
    {
        "id": "auq-alternative-compendia",
        "name": "Acceptability of Alternative Compendia (BP, EP, JP vs. USP-NF)",
        "category": "MAPP 5310.7",
        "plain": "Drugmakers can propose European, British, or Japanese Pharmacopoeia tests in US applications if they prove those tests are at least as strict as USP.",
        "technical": "FDA MAPP 5310.7 requires applicants citing BP, EP, or JP monographs to supply the referenced monograph, acknowledge USP-NF as the official US standard, and justify equivalence or superiority.",
        "url": "https://www.fda.gov/media/72412/download",
    },
    {
        "id": "auq-harmonizing-compendia",
        "name": "Harmonizing Compendial Standards with NDA/ANDA & DMF Specs",
        "category": "PDG / FDA",
        "plain": "When USP updates a monograph, drugmakers and master-file holders align their approved application test specs so factories stay compliant.",
        "technical": "FDA guidance on Harmonizing Compendial Standards outlines how NDA, ANDA, BLA, and DMF holders update regulatory specifications when USP-NF monographs or Pharmacopeial Discussion Group (PDG) chapters revise.",
        "url": "https://www.fda.gov/media/128689/download",
    },
]

ICH_Q12_LIFECYCLE = [
    {
        "id": "auq-ich-q12-framework",
        "name": "ICH Q12 Pharmaceutical Product Lifecycle Management (May 2021)",
        "category": "ICH Q12 Final",
        "plain": "ICH Q12 gives drugmakers a predictable rulebook for upgrading factories, equipment, and tests after a medicine is already approved.",
        "technical": "ICH Q12 establishes harmonized tools—Established Conditions (ECs), Post-Approval Change Management Protocols (PACMPs), and Product Lifecycle Management (PLCM) documents—to streamline post-approval CMC changes.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q12-technical-and-regulatory-considerations-pharmaceutical-product-lifecycle-management-guidance",
    },
    {
        "id": "auq-ich-q12-annexes",
        "name": "ICH Q12 Annexes: Established Conditions & Reporting Categories",
        "category": "ECs & Annexes",
        "plain": "Only the critical manufacturing parameters that truly affect drug safety and quality require prior FDA sign-off when updated.",
        "technical": "The ICH Q12 Annexes illustrate how Marketing Authorization Holders identify explicit Established Conditions (ECs) versus supportive information, linking risk to regional reporting categories.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q12-technical-and-regulatory-considerations-pharmaceutical-product-lifecycle-management-annex",
    },
    {
        "id": "auq-q12-fda-implementation",
        "name": "FDA ICH Q12 Implementation: PAS, CBE-30, CBE-0 & Annual Reports",
        "category": "US Reporting",
        "plain": "In the US, approved post-market manufacturing changes are filed as Prior Approval Supplements, 30-day notices, or Annual Reports depending on risk.",
        "technical": "FDA's ICH Q12 Implementation Considerations Draft Guidance maps Established Conditions and PACMPs onto 21 CFR 314.70 / 601.12 mechanisms (PAS, CBE-30, CBE-0, and Annual Report).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/ich-q12-implementation-considerations-fda-regulated-products",
    },
    {
        "id": "auq-q12-pqs-flexibility",
        "name": "Pharmaceutical Quality System (PQS) & Regulatory Flexibility",
        "category": "ICH Q10 / Q12",
        "plain": "Companies with a strong internal quality system earn more flexibility to manage routine manufacturing improvements without bottlenecks.",
        "technical": "ICH Q12 applies across innovators, generics, biosimilars, and combination products—leveraging an effective ICH Q10 PQS and ICH Q9(R1) QRM to reduce pre-implementation regulatory oversight.",
        "url": "https://www.fda.gov/media/194034/download?attachment",
    },
    {
        "id": "auq-q12-pai-readiness",
        "name": "Preapproval Inspections (CPGM 7346.832) & PQS Change Readiness",
        "category": "PAI / CPGM 7346.832",
        "plain": "Before approving a new drug, FDA inspectors check whether the factory's quality system can safely handle future manufacturing changes.",
        "technical": "FDA Compliance Program 7346.832 directs Preapproval Inspection teams to evaluate a firm's PQS continual-improvement and change-management processes supporting ICH Q12 lifecycle commitments.",
        "url": "https://www.fda.gov/media/193382/download",
    },
    {
        "id": "auq-q12-api-knowledge",
        "name": "API Knowledge & Change Management (CPGM 7356.002F)",
        "category": "API / CPGM 7356.002F",
        "plain": "Active ingredient makers must connect knowledge management, quality risk, and change control across the entire life of the chemical process.",
        "technical": "FDA Compliance Program 7356.002F integrates ICH Q7, Q9(R1), Q10, and Q12 principles, requiring API manufacturers to apply holistic knowledge and change management across the product lifecycle.",
        "url": "https://www.fda.gov/media/187860/download",
    },
]

ICH_Q1_STABILITY = [
    {
        "id": "auq-ich-q1-consolidated",
        "name": "ICH Q1 Consolidated Stability Draft Guidance (June 2025)",
        "category": "ICH Q1 (2025)",
        "plain": "A landmark 2025 update combines six older stability rules into one unified guideline that now also covers vaccines, gene therapies, and combination products.",
        "technical": "FDA's June 2025 ICH Q1 Draft Guidance consolidates Q1A(R2), Q1B, Q1C, Q1D, Q1E, and Q5C while adding stability expectations for ATMPs, vaccines, and complex biologics/combination products.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q1-stability-testing-drug-substances-and-drug-products",
    },
    {
        "id": "auq-ich-q1ar2-conditions",
        "name": "ICH Q1A(R2) Long-Term, Intermediate & Accelerated Storage",
        "category": "ICH Q1A(R2)",
        "plain": "Stability chambers test medicines at normal room temperature (25 °C) and stressed heat/humidity (40 °C / 75% RH) to prove they stay potent until expiration.",
        "technical": "ICH Q1A(R2) defines core climatic zone storage conditions—long-term (25 °C ± 2 °C / 60% RH or 30 °C / 65% RH), intermediate (30 °C / 65% RH), and accelerated (40 °C / 75% RH)—for retest and shelf-life establishment.",
        "url": "https://www.fda.gov/media/71707/download",
    },
    {
        "id": "auq-ich-q1b-photostability",
        "name": "ICH Q1B Photostability & Stress Light Testing",
        "category": "ICH Q1B Light",
        "plain": "Strong controlled light tests reveal whether sunlight or pharmacy lighting breaks down a drug so companies can choose amber bottles or foil blisters.",
        "technical": "ICH Q1B specifies standardized light stress exposure (≥1.2 million lux-hours cool white fluorescent and ≥200 W·h/m² near-UV) as an integral part of stress testing for new drug substances and products.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q1b-photostability-testing-new-drug-substances-and-products",
    },
    {
        "id": "auq-ich-q1b-packaging",
        "name": "Photostability Confirmatory, Opacity & In-Use Exposure",
        "category": "ICH Q1B Pack",
        "plain": "If a medicine comes in an opaque aluminum tube that blocks all light, testing focuses on the exposed drug and how it behaves once opened for patient use.",
        "technical": "Under ICH Q1B Section III, products in light-impenetrable immediate packs (e.g., aluminum tubes) require direct exposure testing only, plus in-use photostability testing for infusion liquids or dermal creams.",
        "url": "https://www.fda.gov/media/71713/download",
    },
    {
        "id": "auq-ich-q1e-extrapolation",
        "name": "ICH Q1E Stability Data Evaluation & Shelf-Life Extrapolation",
        "category": "ICH Q1E Stats",
        "plain": "Statistical trend lines let regulators grant a longer initial expiration date—such as 24 months—from 12 months of real-time data plus accelerated tests.",
        "technical": "ICH Q1E defines statistical regression analysis, poolability tests (p > 0.25), and decision trees for extrapolating a retest period or shelf life beyond observed long-term stability data.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q1e-evaluation-stability-data",
    },
    {
        "id": "auq-ich-q1c-q1d-matrix",
        "name": "ICH Q1C New Dosage Forms & Q1D Bracketing/Matrixing",
        "category": "ICH Q1C / Q1D",
        "plain": "When a drug comes in five tablet strengths and three bottle sizes, bracketing and matrixing let labs test the extremes instead of every single combination.",
        "technical": "ICH Q1C covers reduced stability packages for new dosage forms of approved APIs, while ICH Q1D permits reduced testing schedules via bracketing (extremes of strength/pack) and matrixing (fractional time-point designs).",
        "url": "https://www.fda.gov/media/166147/download",
    },
]


def build_analytical_usp_q12(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2m",
        "checked": CHECKED,
        "ich_q2_q14_aqbd": ICH_Q2_Q14_AQBD,
        "usp_compendia_standards": USP_COMPENDIA_STANDARDS,
        "ich_q12_lifecycle": ICH_Q12_LIFECYCLE,
        "ich_q1_stability": ICH_Q1_STABILITY,
    }
    (out_dir / "analytical_usp_q12.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "ich_q2_q14_aqbd": len(ICH_Q2_Q14_AQBD),
        "usp_compendia_standards": len(USP_COMPENDIA_STANDARDS),
        "ich_q12_lifecycle": len(ICH_Q12_LIFECYCLE),
        "ich_q1_stability": len(ICH_Q1_STABILITY),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_analytical_usp_q12(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

ANALYTICAL_USP_Q12_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderAnalyticalSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="Analytical validation, USP compendia, ICH Q12 lifecycle, and stability architecture">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. ICH Q2(R2) &amp; Q14</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">ATP &amp; AQbD Design</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">DoE &amp; Multivariate</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">Platform Procedures</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Validation &amp; RTRT</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. USP-NF Compendia</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">FD&amp;C § 501(b) Legal Std</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">Ref Standards &amp; &lt;621&gt;</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">BP / EP / JP Equivalence</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">21 CFR 211.160 / 211.194</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. ICH Q12 Lifecycle</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">Established Conditions</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">PACMP &amp; PLCM Docs</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">PAS / CBE-30 / Annual</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Q10 PQS Flexibility</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. Stability (ICH Q1)</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">25°C/60% &amp; 40°C/75% RH</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">Q1B Photostability</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">Q1E Regression / Q1D</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">2025 Consolidated Q1</text>
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

export async function analyticalUspQ12Page(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/analytical_usp_q12.json");
  const sections = [
    { key: "ich_q2_q14_aqbd", title: "1. ICH Q2(R2) & Q14 Analytical Validation & AQbD", items: data.ich_q2_q14_aqbd || [] },
    { key: "usp_compendia_standards", title: "2. USP-NF Compendia, Reference Standards & Lab Controls", items: data.usp_compendia_standards || [] },
    { key: "ich_q12_lifecycle", title: "3. ICH Q12 Post-Approval Lifecycle Management & Established Conditions", items: data.ich_q12_lifecycle || [] },
    { key: "ich_q1_stability", title: "4. Stability Testing: ICH Q1 Consolidated, Q1A(R2), Q1B & Q1E", items: data.ich_q1_stability || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Quality &amp; Lifecycle" : "Reference · Quality &amp; Lifecycle"}</p>
        <h1>Analytical Validation (ICH Q2/Q14), USP Compendia, ICH Q12 &amp; Stability</h1>
        <p class="lede">${exploreMode
          ? "How labs prove every medicine test works accurately, follow official USP quality standards, manage post-approval factory updates, and verify shelf life."
          : "Primary-sourced reference covering ICH Q2(R2)/Q14 AQbD validation, FD&amp;C § 501(b) USP-NF compendial standards, ICH Q12 Established Conditions/PACMPs, and ICH Q1 stability testing."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-24")} · <a href="#/${exploreMode ? "ref" : "explore"}/analytical-usp-q12">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderAnalyticalSvg()}
      <div class="filter-bar" role="group" aria-label="Filter analytical, compendial, and lifecycle sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["ich_q2_q14_aqbd", "ICH Q2/Q14 (6)"], ["usp_compendia_standards", "USP-NF (6)"], ["ich_q12_lifecycle", "ICH Q12 (6)"], ["ich_q1_stability", "Stability Q1 (6)"]].map(([k, lbl]) => `
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
    imp = 'import { analyticalUspQ12Page } from "./analytical_usp_q12.js";\n'
    if "analyticalUspQ12Page" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/analytical-usp-q12") return analyticalUspQ12Page(view, "ref");\n'
        '  if (path === "/explore/analytical-usp-q12") return analyticalUspQ12Page(view, "explore");\n'
    )
    if '"/ref/analytical-usp-q12"' not in txt:
        anchor = 'if (path === "/ref/continuous-pat-ai")'
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
    if "#/ref/analytical-usp-q12" not in txt:
        anchor = '["#/ref/continuous-pat-ai"'
        item = '["#/ref/analytical-usp-q12", "Analytical Q2/Q14, USP & Q12"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/analytical-usp-q12" not in txt:
        anchor2 = '["#/explore/continuous-pat-ai"'
        item2 = '["#/explore/analytical-usp-q12", "Analytical Q2/Q14, USP & Q12"], '
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
    line = "python3 pipeline/build_analytical_usp_q12.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/analytical-usp-q12"' in txt:
        return False
    block = (
        '\n@app.get("/api/analytical-usp-q12")\n'
        'def api_analytical_usp_q12():\n'
        '    p = DATA_DIR / "analytical_usp_q12.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "analytical_usp_q12.json" in txt:
        return False
    snippet = '''    auq_path = data_dir / "analytical_usp_q12.json"
    if auq_path.is_file():
        auq_doc = json.loads(auq_path.read_text(encoding="utf-8"))
        for sec in ("ich_q2_q14_aqbd", "usp_compendia_standards", "ich_q12_lifecycle", "ich_q1_stability"):
            for item in auq_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "Analytical, USP & ICH Q12",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/analytical-usp-q12",
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
    if "/analytical-usp-q12/" in txt:
        return False
    snippet = '''    # v6.2m Analytical Q2(R2)/Q14, USP-NF Compendia, ICH Q12 & Stability SEO landing page
    auq_dir = site_dir / "analytical-usp-q12"
    auq_dir.mkdir(parents=True, exist_ok=True)
    (auq_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Analytical Validation (ICH Q2/Q14), USP Compendia &amp; ICH Q12 | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to ICH Q2(R2)/Q14 AQbD validation, USP-NF compendial standards, ICH Q12 lifecycle management, and ICH Q1 stability testing.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/analytical-usp-q12/'>"
        "<script>location.replace('/#/explore/analytical-usp-q12');</script>"
        "</head><body><h1>Analytical Validation, USP Compendia, ICH Q12 &amp; Stability</h1>"
        "<p><a href='/#/explore/analytical-usp-q12'>Explore</a> · <a href='/#/ref/analytical-usp-q12'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/analytical-usp-q12/")
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
    if "#/ref/analytical-usp-q12" in txt:
        return False
    anchor = '"/#/explore/continuous-pat-ai",'
    add = '"/#/explore/continuous-pat-ai",\n    "/#/ref/analytical-usp-q12",\n    "/#/explore/analytical-usp-q12",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/analytical-usp-q12 /#/explore/analytical-usp-q12\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_analytical_usp_q12_py": _write_if_changed(pipe_dir / "build_analytical_usp_q12.py", BUILD_ANALYTICAL_USP_Q12_PY),
        "analytical_usp_q12_js": _write_if_changed(js_dir / "analytical_usp_q12.js", ANALYTICAL_USP_Q12_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/continuous-pat-ai") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/continuous-pat-ai", "Continuous Mfg, PAT & AI"]] }];\nconst EXPLORE_NAV = [["#/explore/continuous-pat-ai", "Continuous Mfg, PAT & AI"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/continuous-pat-ai",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_analytical_usp_q12.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_analytical_usp_q12.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ich_q2_q14_aqbd": 6, "usp_compendia_standards": 6, "ich_q12_lifecycle": 6, "ich_q1_stability": 6}, out

        doc = json.loads((root / "site" / "data" / "analytical_usp_q12.json").read_text(encoding="utf-8"))
        for k in ("ich_q2_q14_aqbd", "usp_compendia_standards", "ich_q12_lifecycle", "ich_q1_stability"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "analytical_usp_q12.js").read_text(encoding="utf-8")
        print("V62M_ANALYTICAL_USP_Q12_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2m Analytical Q2/Q14, USP, ICH Q12 & Stability patch.")
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
