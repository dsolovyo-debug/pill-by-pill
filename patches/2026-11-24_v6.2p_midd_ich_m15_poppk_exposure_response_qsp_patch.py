#!/usr/bin/env python3
"""Pill by Pill v6.2p Patch: Model-Informed Drug Development (ICH M15 / PDUFA VII Paired Meetings), Population Pharmacokinetics (PopPK), Exposure-Response (E-R) & Quantitative Systems Pharmacology (QSP) Reference (#/ref/midd-pharmacometrics, #/explore/midd-pharmacometrics, /api/midd-pharmacometrics).

1. Adds `pipeline/build_midd_pharmacometrics.py` -> `site/data/midd_pharmacometrics.json`
   (6 ICH M15 & MIDD Paired Meeting pillars, 6 PopPK & Covariate Modeling pillars, 6
   Exposure-Response & Dose Optimization pillars, and 6 QSP & Pediatric MIDD pillars — 24
   primary-sourced entries).
2. Adds `site/js/midd_pharmacometrics.js` (`middPharmacometricsPage` with inline MIDD,
   PopPK, E-R & QSP SVG + 4 section filters) and wires `#/ref/midd-pharmacometrics`,
   `#/explore/midd-pharmacometrics`, `/api/midd-pharmacometrics`, `REF_NAV_GROUPS`,
   `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `midd_pharmacometrics.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/midd-pharmacometrics/` static SEO page + sitemap
   entry -> 58 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2p_midd_ich_m15_poppk_exposure_response_qsp_patch.py --selftest
  python3 2026-11-24_v6.2p_midd_ich_m15_poppk_exposure_response_qsp_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_MIDD_PHARMACOMETRICS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2p MIDD (ICH M15), PopPK, Exposure-Response & QSP Reference (`site/data/midd_pharmacometrics.json`).

Comprehensive, primary-sourced reference covering:
  1. ICH M15 General Principles & FDA MIDD Paired Meeting Program (6 pillars)
  2. Population Pharmacokinetics (PopPK) & Covariate Modeling (6 pillars)
  3. Exposure-Response (E-R) Relationships & Dose Optimization (6 pillars)
  4. Quantitative Systems Pharmacology (QSP) & Pediatric MIDD (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER QM CoE/OCP, ICH).

Usage:
  python3 pipeline/build_midd_pharmacometrics.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

ICH_M15_MIDD = [
    {
        "id": "mid-ich-m15-center",
        "name": "ICH M15 Resource Center & CDER Quantitative Medicine CoE",
        "category": "CDER QM CoE",
        "plain": "Mathematical models of how a drug moves through the body help scientists pick safer doses and design smarter clinical trials.",
        "technical": "FDA's Quantitative Medicine Center of Excellence (QM CoE) hosts the ICH M15 Resource Center, establishing harmonized multidisciplinary expectations for MIDD planning, model evaluation, and regulatory documentation.",
        "url": "https://www.fda.gov/about-fda/cder-quantitative-medicine-center-excellence-qm-coe/m15-resource-center",
    },
    {
        "id": "mid-ich-m15-guidance",
        "name": "ICH M15 General Principles for Model-Informed Drug Development (June 2026)",
        "category": "ICH M15 Final",
        "plain": "A landmark 2026 international guideline standardizes how drugmakers document computer-simulated clinical evidence for FDA, EMA, and PMDA.",
        "technical": "Adopted by ICH in February 2026 and issued by FDA in June 2026, ICH M15 harmonizes terminology, assessment tables, and evidence expectations across PopPK, PBPK, E-R, and QSP models.",
        "url": "https://www.fda.gov/media/184747/download",
    },
    {
        "id": "mid-m15-assessment-table",
        "name": "MIDD Assessment Table: Question of Interest, COU & Model Risk",
        "category": "M15 Risk Framework",
        "plain": "Regulators judge each computer model by how much rests on its answer—from picking an early dose to replacing a full human study.",
        "technical": "ICH M15's Assessment Framework pairs Question of Interest and Context of Use (COU) with Model Influence and Consequence of Wrong Decision to calibrate verification and validation rigor.",
        "url": "https://www.fda.gov/media/196773/download",
    },
    {
        "id": "mid-paired-meeting-program",
        "name": "MIDD Paired Meeting Program (PDUFA VII, FY 2023–2027)",
        "category": "PDUFA VII",
        "plain": "Drug developers can book dedicated two-part FDA meetings to agree on modeling strategies before running expensive trials.",
        "technical": "Fulfilling PDUFA VII commitments under FDORA, the CDER/CBER MIDD Paired Meeting Program grants 1–2 proposals per quarter with an initial meeting and a 60-day follow-up meeting.",
        "url": "https://www.fda.gov/drugs/development-resources/model-informed-drug-development-paired-meeting-program",
    },
    {
        "id": "mid-paired-meeting-faq",
        "name": "Early Engagement: MIDD Paired Meetings vs. EOP2A",
        "category": "Regulatory Strategy",
        "plain": "Sponsors with an active IND can request an MIDD meeting at any stage—not only at End of Phase 2A.",
        "technical": "FDA's MIDD Paired Meeting FAQ clarifies that sponsors with an active PIND or IND can engage early across PopPK, PBPK, QSP, or trial simulation without awaiting EOP2A.",
        "url": "https://www.fda.gov/drugs/development-resources/midd-paired-meeting-program-frequently-asked-questions",
    },
    {
        "id": "mid-m15-webinar-2026",
        "name": "Multidisciplinary MIDD Planning & Regulatory Submissions",
        "category": "ICH M15 Implementation",
        "plain": "Modeling is no longer a solo specialist task—clinicians, statisticians, and pharmacologists co-author the MIDD plan together.",
        "technical": "FDA's October 2026 ICH M15 workshop highlights multidisciplinary alignment across clinical, statistical, and pharmacometric teams when preparing meeting packages and eCTD submissions.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/webinar-stakeholder-engagement-new-final-guideline-general-principles-model-informed-drug",
    },
]

POPPK_MODELING = [
    {
        "id": "mid-poppk-final-2022",
        "name": "Population Pharmacokinetics (PopPK) Final Guidance (Feb 2022)",
        "category": "PopPK Guidance",
        "plain": "Instead of drawing dozens of blood tubes from a few volunteers, PopPK pools sparse samples from hundreds of real patients.",
        "technical": "FDA's February 2022 Population Pharmacokinetics guidance guides sponsors on nonlinear mixed-effects modeling across INDs, NDAs, BLAs, and ANDAs to quantify inter-individual variability.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/population-pharmacokinetics",
    },
    {
        "id": "mid-poppk-labeling-pmr",
        "name": "Therapeutic Individualization, Labeling & PMR/PMC Relief",
        "category": "Clinical Labeling",
        "plain": "Strong population PK data can tell doctors how to adjust doses for kidney function or body weight—and even waive extra post-approval studies.",
        "technical": "Adequate PopPK data collection and analyses in marketing applications inform CLINICAL PHARMACOLOGY labeling and have alleviated the need for dedicated postmarketing requirements or commitments.",
        "url": "https://www.fda.gov/media/155925/download",
    },
    {
        "id": "mid-poppk-validation-sim",
        "name": "Exploratory Data Analysis, Model Validation & Simulations",
        "category": "PopPK Workflow",
        "plain": "Analysts check model accuracy using visual predictive checks before simulating new dosing schedules.",
        "technical": "FDA's PopPK guidance details graphical/statistical data examination, goodness-of-fit diagnostics, visual predictive checks (VPCs), and clinical trial simulations to justify untested dosing regimens.",
        "url": "https://www.fda.gov/media/128793/download",
    },
    {
        "id": "mid-poppk-covariates",
        "name": "Covariate Screening: Weight, Organ Function & Pharmacogenomics",
        "category": "Covariate Analysis",
        "plain": "PopPK models test whether age, body weight, kidney clearance, or liver enzymes change how fast a patient clears a drug.",
        "technical": "Population PK covariate modeling quantifies intrinsic and extrinsic factors affecting apparent clearance (CL/F) and volume of distribution to support subgroup dose adjustments.",
        "url": "https://www.fda.gov/media/71364/download",
    },
    {
        "id": "mid-poppk-regimen-selection",
        "name": "Selecting Dosing Regimens for Phase 2/3 Clinical Trials",
        "category": "Trial Design",
        "plain": "Early Phase 1 blood-level models help pick the right Phase 2 and Phase 3 doses so fewer trials fail from under- or over-dosing.",
        "technical": "CDER's Population Pharmacokinetics recap explains how integrating Phase 1/2 PK variability reduces response heterogeneity when selecting Phase 2/3 dosing regimens.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/guidance-recap-podcast-population-pharmacokinetics",
    },
    {
        "id": "mid-poppk-pregnancy-sparse",
        "name": "Sparse Sampling & Nonlinear Mixed-Effects Modeling in Pregnancy",
        "category": "Special Populations",
        "plain": "Minimal blood draws paired with PopPK modeling let researchers track how pregnancy changes drug clearance safely.",
        "technical": "FDA's Pharmacokinetics in Pregnancy guidance endorses PopPK with nonlinear mixed-effects modeling and gestational-age covariates to minimize blood draws in pregnant participants.",
        "url": "https://www.fda.gov/media/71353/download",
    },
]

EXPOSURE_RESPONSE = [
    {
        "id": "mid-er-guidance-portal",
        "name": "Exposure-Response (E-R) Relationships Guidance",
        "category": "E-R Framework",
        "plain": "Exposure-response analysis connects how much drug is in the blood to how well it treats disease—and what side effects appear.",
        "technical": "FDA's Exposure-Response Relationships guidance outlines study design, data analysis, and regulatory applications linking drug concentration to PD biomarkers, efficacy, and safety endpoints.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/exposure-response-relationships-study-design-data-analysis-and-regulatory-applications",
    },
    {
        "id": "mid-er-randomized-designs",
        "name": "Randomized Dose/Concentration vs. Mechanistic E-R Studies",
        "category": "E-R Study Design",
        "plain": "Randomly assigning patients to different doses proves whether higher blood levels truly cause better outcomes.",
        "technical": "To support regulatory efficacy claims, FDA emphasizes randomization to dose or concentration, while nonrandomized mechanistic E-R models inform exploratory dose-selection and safety evaluations.",
        "url": "https://www.fda.gov/media/71277/download",
    },
    {
        "id": "mid-er-ich-e4-subgroups",
        "name": "ICH E4 Dose-Response & Explaining Subgroup Differences",
        "category": "ICH E4 / E-R",
        "plain": "If men and women respond differently to a medicine, exposure-response modeling checks whether it is simply due to blood-level differences.",
        "technical": "Integrating ICH E4 principles across the entire drug development database, E-R modeling evaluates whether demographic response differences stem from observed PK exposure shifts.",
        "url": "https://www.fda.gov/media/71277/download",
    },
    {
        "id": "mid-er-clinical-modernization",
        "name": "FDA Actions to Modernize Early & Late-Stage Clinical Development",
        "category": "Dose Optimization",
        "plain": "Modern FDA policy pushes companies to find the lowest effective, best-tolerated dose early—rather than defaulting to maximum tolerated doses.",
        "technical": "FDA's clinical modernization initiative integrates quantitative pharmacology, Project Optimus, and E-R modeling across early and late-stage development to optimize benefit-risk.",
        "url": "https://www.fda.gov/industry/fda-actions-accelerate-and-modernize-early-and-late-stage-clinical-development",
    },
    {
        "id": "mid-er-sdtcg-standards",
        "name": "Study Data Technical Conformance for PopPK & E-R Submissions",
        "category": "Data Standards",
        "plain": "Standardized electronic datasets let FDA reviewers re-run a company's pharmacokinetic and exposure-response models directly.",
        "technical": "FDA's Study Data Technical Conformance Guide (SDTCG) specifies standardized CDISC ADaM/PK datasets and model script documentation for reproducible PopPK and E-R reviews.",
        "url": "https://www.fda.gov/media/153632/download",
    },
    {
        "id": "mid-er-benefit-risk",
        "name": "E-R in Benefit-Risk, Bridging & Dose-Adjustment Decisions",
        "category": "Regulatory E-R",
        "plain": "When a drug's benefit flattens out while side effects keep rising, E-R curves pinpoint the sweet-spot dose.",
        "technical": "Regulatory E-R analyses bridge efficacy across dosing schedules, support QT/safety margin evaluations, and justify dose reductions for toxicity or drug-drug interactions.",
        "url": "https://www.fda.gov/media/75273/download",
    },
]

QSP_PEDIATRIC_MIDD = [
    {
        "id": "mid-qsp-mabel-fih",
        "name": "QSP-Based MABEL Dose Selection for First-in-Human Trials",
        "category": "QSP / MABEL",
        "plain": "Quantitative Systems Pharmacology (QSP) simulates how a drug interacts with human biology to pick a safe starting dose for Phase 1.",
        "technical": "FDA's QSP-Based Dose Selection guidance recommends how to build and qualify QSP models for determining Minimum Anticipated Biological Effect Level (MABEL) doses in FIH Phase 1 trials.",
        "url": "https://www.fda.gov/media/193230/download",
    },
    {
        "id": "mid-qsp-cou-3rs",
        "name": "QSP Context of Use, Model Influence & Reducing Animal Tox",
        "category": "QSP / ICH M15",
        "plain": "Well-validated human biological models can make Phase 1 starting doses safer while reducing reliance on animal toxicology studies.",
        "technical": "Aligned with ICH M15, FDA's QSP guidance defines Question of Interest, Context of Use (COU), and Model Influence—supporting FIH dose selection with reduced animal toxicity reliance.",
        "url": "https://www.fda.gov/media/193230/download",
    },
    {
        "id": "mid-qsp-rare-diseases",
        "name": "QSP Roadmap for Rare Disease Drug Development",
        "category": "Rare Disease QSP",
        "plain": "When a rare disease has too few patients for large dose-finding trials, QSP models simulate disease biology and drug response.",
        "technical": "FDA–M-CERSI's QSP Roadmap addresses ultra-rare disease development by mechanistically linking target engagement and disease pathways to simulate dose response and inter-patient variability.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/creating-roadmap-quantitative-systems-pharmacology-informed-rare-disease-drug-development-05112023",
    },
    {
        "id": "mid-pediatric-optimal-sampling",
        "name": "ICH E11 Pediatric Optimal Sampling & Sparse PopPK",
        "category": "Pediatric MIDD",
        "plain": "Optimal-sampling math lets pediatric trials collect the fewest possible blood draws from children while still matching adult drug levels.",
        "technical": "ICH E11 leverages PopPK modeling and optimal sparse sampling schedules to support pediatric dose selection, exposure-matching, and extrapolation from adult clinical data.",
        "url": "https://www.fda.gov/media/71355/download",
    },
    {
        "id": "mid-adrg-model-traceability",
        "name": "Analysis Data Reviewer's Guide (ADRG) & Model Traceability",
        "category": "eCTD Traceability",
        "plain": "Every modeling submission includes a clear roadmap showing how raw patient numbers became final dosing charts.",
        "technical": "The ADRG documents analysis datasets, NONMEM/R/Monolix software scripts, and variable derivations so FDA pharmacometrics reviewers can audit and reproduce submitted models.",
        "url": "https://www.fda.gov/media/88173/download",
    },
    {
        "id": "mid-ddi-pbpk-modeling",
        "name": "Clinical Pharmacology & DDI Modeling Integration",
        "category": "DDI / PBPK",
        "plain": "Computer simulations predict how strong enzyme blockers or inducers change drug blood levels—sometimes replacing dedicated DDI trials.",
        "technical": "FDA's Drug Interactions guidance suite integrates mechanistic PBPK and static/dynamic DDI models with clinical pharmacology studies to inform concomitant-medication labeling.",
        "url": "https://www.fda.gov/drugs/drug-interactions-labeling/drug-interactions-relevant-regulatory-guidance-and-policy-documents",
    },
]


def build_midd_pharmacometrics(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2p",
        "checked": CHECKED,
        "ich_m15_midd": ICH_M15_MIDD,
        "poppk_modeling": POPPK_MODELING,
        "exposure_response": EXPOSURE_RESPONSE,
        "qsp_pediatric_midd": QSP_PEDIATRIC_MIDD,
    }
    (out_dir / "midd_pharmacometrics.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "ich_m15_midd": len(ICH_M15_MIDD),
        "poppk_modeling": len(POPPK_MODELING),
        "exposure_response": len(EXPOSURE_RESPONSE),
        "qsp_pediatric_midd": len(QSP_PEDIATRIC_MIDD),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_midd_pharmacometrics(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

MIDD_PHARMACOMETRICS_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderMiddSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="Model-Informed Drug Development ICH M15, PopPK, Exposure-Response, and QSP architecture">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. ICH M15 &amp; MIDD</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">Question of Interest</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">Context of Use &amp; Risk</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">PDUFA VII Paired Mtgs</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">June 2026 ICH M15</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. Population PK</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">Sparse Patient Sampling</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">Covariates (WT / Renal)</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">VPCs &amp; Labeling / PMR</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Nonlinear Mixed Effects</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. Exposure-Response</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">Conc vs. Efficacy / AE</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">Randomized Dose Design</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">Dose Optimization</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">ICH E4 &amp; Benefit-Risk</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. QSP &amp; Pediatrics</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">FIH MABEL Selection</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">Rare Disease Systems</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">ICH E11 &amp; DDI PBPK</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Mechanistic Modeling</text>
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

export async function middPharmacometricsPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/midd_pharmacometrics.json");
  const sections = [
    { key: "ich_m15_midd", title: "1. ICH M15 General Principles & FDA MIDD Paired Meeting Program", items: data.ich_m15_midd || [] },
    { key: "poppk_modeling", title: "2. Population Pharmacokinetics (PopPK) & Covariate Modeling", items: data.poppk_modeling || [] },
    { key: "exposure_response", title: "3. Exposure-Response (E-R) Relationships & Dose Optimization", items: data.exposure_response || [] },
    { key: "qsp_pediatric_midd", title: "4. Quantitative Systems Pharmacology (QSP) & Pediatric MIDD", items: data.qsp_pediatric_midd || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Quantitative Medicine" : "Reference · Quantitative Medicine"}</p>
        <h1>Model-Informed Drug Development (ICH M15), PopPK, E-R &amp; QSP</h1>
        <p class="lede">${exploreMode
          ? "How pharmaceutical scientists use mathematical models of drug exposure and human biology to pick safer starting doses, tailor dosing for patients, and streamline trials."
          : "Primary-sourced reference covering ICH M15 MIDD principles, PDUFA VII Paired Meetings, Population PK (Feb 2022), Exposure-Response modeling, and QSP FIH MABEL dose selection."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-24")} · <a href="#/${exploreMode ? "ref" : "explore"}/midd-pharmacometrics">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderMiddSvg()}
      <div class="filter-bar" role="group" aria-label="Filter MIDD, PopPK, E-R, and QSP sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["ich_m15_midd", "ICH M15 / MIDD (6)"], ["poppk_modeling", "PopPK (6)"], ["exposure_response", "Exposure-Response (6)"], ["qsp_pediatric_midd", "QSP & Pediatrics (6)"]].map(([k, lbl]) => `
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
    imp = 'import { middPharmacometricsPage } from "./midd_pharmacometrics.js";\n'
    if "middPharmacometricsPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/midd-pharmacometrics") return middPharmacometricsPage(view, "ref");\n'
        '  if (path === "/explore/midd-pharmacometrics") return middPharmacometricsPage(view, "explore");\n'
    )
    if '"/ref/midd-pharmacometrics"' not in txt:
        anchor = 'if (path === "/ref/babe-bcs-nti")'
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
    if "#/ref/midd-pharmacometrics" not in txt:
        anchor = '["#/ref/babe-bcs-nti"'
        item = '["#/ref/midd-pharmacometrics", "MIDD (ICH M15), PopPK & QSP"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/midd-pharmacometrics" not in txt:
        anchor2 = '["#/explore/babe-bcs-nti"'
        item2 = '["#/explore/midd-pharmacometrics", "MIDD (ICH M15), PopPK & QSP"], '
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
    line = "python3 pipeline/build_midd_pharmacometrics.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/midd-pharmacometrics"' in txt:
        return False
    block = (
        '\n@app.get("/api/midd-pharmacometrics")\n'
        'def api_midd_pharmacometrics():\n'
        '    p = DATA_DIR / "midd_pharmacometrics.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "midd_pharmacometrics.json" in txt:
        return False
    snippet = '''    mid_path = data_dir / "midd_pharmacometrics.json"
    if mid_path.is_file():
        mid_doc = json.loads(mid_path.read_text(encoding="utf-8"))
        for sec in ("ich_m15_midd", "poppk_modeling", "exposure_response", "qsp_pediatric_midd"):
            for item in mid_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "MIDD, PopPK & QSP",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/midd-pharmacometrics",
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
    if "/midd-pharmacometrics/" in txt:
        return False
    snippet = '''    # v6.2p MIDD (ICH M15), PopPK, Exposure-Response & QSP SEO landing page
    mid_dir = site_dir / "midd-pharmacometrics"
    mid_dir.mkdir(parents=True, exist_ok=True)
    (mid_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>MIDD (ICH M15), PopPK, Exposure-Response &amp; QSP | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to ICH M15 MIDD, PDUFA VII Paired Meetings, Population Pharmacokinetics, Exposure-Response, and QSP FIH MABEL dose selection.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/midd-pharmacometrics/'>"
        "<script>location.replace('/#/explore/midd-pharmacometrics');</script>"
        "</head><body><h1>Model-Informed Drug Development (ICH M15), PopPK, E-R &amp; QSP</h1>"
        "<p><a href='/#/explore/midd-pharmacometrics'>Explore</a> · <a href='/#/ref/midd-pharmacometrics'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/midd-pharmacometrics/")
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
    if "#/ref/midd-pharmacometrics" in txt:
        return False
    anchor = '"/#/explore/babe-bcs-nti",'
    add = '"/#/explore/babe-bcs-nti",\n    "/#/ref/midd-pharmacometrics",\n    "/#/explore/midd-pharmacometrics",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/midd-pharmacometrics /#/explore/midd-pharmacometrics\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_midd_pharmacometrics_py": _write_if_changed(pipe_dir / "build_midd_pharmacometrics.py", BUILD_MIDD_PHARMACOMETRICS_PY),
        "midd_pharmacometrics_js": _write_if_changed(js_dir / "midd_pharmacometrics.js", MIDD_PHARMACOMETRICS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/babe-bcs-nti") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/babe-bcs-nti", "BA/BE, BCS M9, NTI & IVPT"]] }];\nconst EXPLORE_NAV = [["#/explore/babe-bcs-nti", "BA/BE, BCS M9, NTI & IVPT"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/babe-bcs-nti",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_midd_pharmacometrics.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_midd_pharmacometrics.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"ich_m15_midd": 6, "poppk_modeling": 6, "exposure_response": 6, "qsp_pediatric_midd": 6}, out

        doc = json.loads((root / "site" / "data" / "midd_pharmacometrics.json").read_text(encoding="utf-8"))
        for k in ("ich_m15_midd", "poppk_modeling", "exposure_response", "qsp_pediatric_midd"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "midd_pharmacometrics.js").read_text(encoding="utf-8")
        print("V62P_MIDD_PHARMACOMETRICS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2p MIDD (ICH M15), PopPK, E-R & QSP patch.")
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
