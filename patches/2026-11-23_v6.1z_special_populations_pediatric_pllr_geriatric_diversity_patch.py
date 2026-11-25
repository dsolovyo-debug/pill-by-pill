#!/usr/bin/env python3
"""Pill by Pill v6.1z Patch: Special Populations — Pediatric (PREA/BPCA/RACE), Pregnancy & Lactation (PLLR), Geriatric/Organ Impairment & Diversity Action Plans Reference (#/ref/special-populations, #/explore/special-populations, /api/special-populations).

1. Adds `pipeline/build_special_populations.py` -> `site/data/special_populations.json` (6 Pediatric
   PREA/BPCA/RACE pillars, 6 Pregnancy & Lactation Labeling Rule [PLLR] & Registries pillars,
   6 Geriatric [ICH E7] & Renal/Hepatic Impairment pillars, and 6 FDORA Diversity Action Plans &
   Subgroup Representation pillars — 24 primary-sourced entries).
2. Adds `site/js/special_populations.js` (`specialPopulationsPage` with inline Special Populations
   Clinical & Regulatory Framework SVG + 4 section filters) and wires `#/ref/special-populations`,
   `#/explore/special-populations`, `/api/special-populations`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `special_populations.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/special-populations/` static SEO page + sitemap entry -> 42
   encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-23_v6.1z_special_populations_pediatric_pllr_geriatric_diversity_patch.py --selftest
  python3 2026-11-23_v6.1z_special_populations_pediatric_pllr_geriatric_diversity_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_SPECIAL_POPULATIONS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.1z Special Populations Reference (`site/data/special_populations.json`).

Comprehensive, primary-sourced reference covering:
  1. Pediatric Drug Development (PREA, BPCA, iPSP & RACE for Children) (6 pillars)
  2. Pregnancy & Lactation Labeling Rule (PLLR) & Exposure Registries (6 pillars)
  3. Geriatric (ICH E7) & Renal / Hepatic Organ Impairment Dosing (6 pillars)
  4. FDORA Diversity Action Plans & Demographic Subgroups (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER, CBER, OCE, ICH).

Usage:
  python3 pipeline/build_special_populations.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-23"

PEDIATRIC_DEVELOPMENT = [
    {
        "id": "ped-prea-mandatory",
        "name": "Pediatric Research Equity Act (PREA, FD&C Act § 505B)",
        "category": "Mandatory Studies",
        "plain": "Whenever a company seeks approval for a new active ingredient, indication, or dosage form, federal law requires studying it in children unless FDA grants a waiver or deferral.",
        "technical": "PREA requires pediatric assessments for NDAs/BLAs/supplements with a new active ingredient, indication, dosage form, dosing regimen, or route of administration; supports age-appropriate formulations and labeling.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pediatric-drug-development-under-pediatric-research-equity-act-and-best-pharmaceuticals-children-act",
    },
    {
        "id": "ped-bpca-exclusivity",
        "name": "Best Pharmaceuticals for Children Act (BPCA) & +6-Month Exclusivity",
        "category": "Voluntary Incentive",
        "plain": "If a drugmaker completes extra pediatric studies requested in writing by FDA, it earns an extra 6 months of market exclusivity—extended to biologics in 2010.",
        "technical": "FD&C Act § 505A (BPCA) authorizes FDA Written Requests (WRs) for voluntary pediatric studies; completing WR terms grants 6 months of pediatric exclusivity attaching to existing patents/exclusivities.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pediatric-drug-development-under-pediatric-research-equity-act-and-best-pharmaceuticals-children-act",
    },
    {
        "id": "ped-ipsp-timing",
        "name": "Initial Pediatric Study Plan (iPSP) End-of-Phase 2 Submission",
        "category": "Planning Milestone",
        "plain": "Companies must map out their children's testing plan—or explain why a drug isn't appropriate for kids—right around Phase 2, before pivotal adult trials begin.",
        "technical": "Under FDASIA, sponsors subject to PREA must submit an Initial Pediatric Study Plan (iPSP) within 60 days after the End-of-Phase 2 meeting; sponsors may also submit a Proposed Pediatric Study Request (PPSR) for a BPCA WR.",
        "url": "https://www.fda.gov/media/86340/download",
    },
    {
        "id": "ped-race-act",
        "name": "RACE for Children Act (FDARA 2017 Pediatric Oncology)",
        "category": "Mechanism-Based PREA",
        "plain": "Even if an adult cancer doesn't occur in children, a targeted cancer drug must still be studied in kids if its molecular target drives a childhood tumor.",
        "technical": "FDARA (2017) amended PREA so adult oncology NDAs/BLAs directed at a molecular target substantially relevant to pediatric cancer growth/progression require pediatric evaluation guided by FDA/NCI Pediatric Molecular Target Lists.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/pediatric-oncology",
    },
    {
        "id": "ped-extrapolation",
        "name": "Pediatric Efficacy Extrapolation & Neonatal Studies",
        "category": "Clinical Strategy",
        "plain": "When a disease behaves similarly in adults and children, FDA allows matching drug blood levels (PK/PD) instead of repeating massive Phase 3 efficacy trials in kids.",
        "technical": "Full or partial pediatric extrapolation leverages adult efficacy when disease progression and exposure-response are sufficiently similar, focusing pediatric trials on PK bridging, dose-finding, and safety—especially in neonates.",
        "url": "https://www.fda.gov/media/196756/download",
    },
    {
        "id": "ped-900-labels",
        "name": "Over 900 Drugs Updated with Pediatric Labeling Information",
        "category": "Public Health Impact",
        "plain": "Thanks to PREA and BPCA, more than 900 prescription drugs now carry real pediatric dosing and safety instructions instead of leaving pediatricians to guess.",
        "technical": "Per FDA's Report to Congress on BPCA and PREA, over 900 drugs and biologics now include new pediatric labeling information, backed by mandatory post-marketing Pediatric Advisory Committee (PAC) safety reviews.",
        "url": "https://www.fda.gov/media/157840/download",
    },
]

PREGNANCY_LACTATION_PLLR = [
    {
        "id": "pllr-end-letters",
        "name": "Pregnancy and Lactation Labeling Rule (PLLR): Replacing A/B/C/D/X",
        "category": "Narrative Labeling",
        "plain": "FDA retired the confusing A/B/C/D/X pregnancy letter grades and replaced them with detailed, plain-language summaries of real human and animal risk data.",
        "technical": "PLLR (2014 Final Rule, effective 2015) eliminated legacy Pregnancy Categories A, B, C, D, and X across prescription drug/biologic labeling, replacing them with structured narrative risk summaries and clinical considerations.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-rules/pregnancy-and-lactation-labeling-final-rule",
    },
    {
        "id": "pllr-81-pregnancy",
        "name": "Section 8.1 Pregnancy (Risk Summary, Clinical Considerations & Data)",
        "category": "Label Subsection 8.1",
        "plain": "Section 8.1 explains both the medicine's potential fetal risks and the risks of leaving a mother's underlying condition—like epilepsy or depression—untreated.",
        "technical": "PLLR Subsection 8.1 integrates Labor & Delivery and mandates Risk Summary, Clinical Considerations (disease-associated maternal/fetal risk, dose adjustments, maternal/fetal adverse reactions), and supporting human/animal Data.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-rules/pregnancy-and-lactation-labeling-final-rule",
    },
    {
        "id": "pllr-82-lactation",
        "name": "Section 8.2 Lactation (Breast Milk Transfer & Infant Monitoring)",
        "category": "Label Subsection 8.2",
        "plain": "Renamed from 'Nursing Mothers', Section 8.2 tells clinicians how much drug passes into breast milk and whether to monitor a breastfed baby.",
        "technical": "PLLR Subsection 8.2 (Lactation) provides Risk Summary (presence in human milk, effects on breastfed infant and milk production), Clinical Considerations (minimizing exposure, monitoring), and Data.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-rules/pregnancy-and-lactation-labeling-final-rule",
    },
    {
        "id": "pllr-83-reproductive",
        "name": "Section 8.3 Females and Males of Reproductive Potential",
        "category": "Label Subsection 8.3",
        "plain": "A dedicated section covers whether patients need a pregnancy test before starting therapy, how long to use contraception, and any fertility effects for women or men.",
        "technical": "PLLR Subsection 8.3 is required when labeling includes recommendations/requirements for pregnancy testing, contraception before/during/after therapy, or human/animal evidence of impaired fertility.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/biologics-rules/pregnancy-and-lactation-labeling-final-rule",
    },
    {
        "id": "pllr-registries",
        "name": "Pregnancy Exposure Registries & Mandatory Label Contact Info",
        "category": "Post-Market Evidence",
        "plain": "Because pregnant women are rarely enrolled in initial drug trials, FDA often requires post-market pregnancy registries and prints the enrollment phone number right on the label.",
        "technical": "Pregnancy exposure registries are prospective observational cohorts collecting maternal/infant outcomes; PLLR mandates prominent contact information at the top of Subsection 8.1 whenever a registry exists.",
        "url": "https://www.fda.gov/drugs/labeling-information-drug-products/questions-and-answers-pregnancy-and-lactation-labeling-rule",
    },
    {
        "id": "pllr-annual-updates",
        "name": "Ongoing PLLR Updates from Registry Interim & Final Reports",
        "category": "Label Maintenance",
        "plain": "As years of real-world pregnancy registry data accumulate, drugmakers must update Section 8.1 so clinicians get the latest safety picture.",
        "technical": "Manufacturers must update PLLR subsections whenever new human pregnancy/lactation data (e.g., interim or final registry reports) make prior risk statements inaccurate or incomplete.",
        "url": "https://www.fda.gov/drugs/labeling-information-drug-products/pregnancy-and-lactation-labeling-resources",
    },
]

GERIATRIC_ORGAN_IMPAIRMENT = [
    {
        "id": "ger-ich-e7",
        "name": "ICH E7 Guideline: Studies in Support of Special Populations (Geriatrics)",
        "category": "Older Adults (65+)",
        "plain": "Clinical trials shouldn't set arbitrary upper age limits—older adults 65+, and especially 75+, need to be included so doctors catch age-related side effects and drug interactions.",
        "technical": "ICH E7 defines the geriatric population as ≥65 years (encouraging ≥75 years inclusion without arbitrary upper age cutoffs) and evaluates age-related PK, concomitant illnesses, and drug-disease interactions.",
        "url": "https://www.fda.gov/media/71317/download",
    },
    {
        "id": "ger-labeling-85",
        "name": "Section 8.5 Geriatric Use Labeling (65–74, 75–84 & 85+ Subgroups)",
        "category": "Prescribing Information",
        "plain": "Drug labels must report how many seniors participated in clinical trials and whether older patients saw different safety or effectiveness than younger adults.",
        "technical": "Under 21 CFR 201.57(c)(9)(v), Section 8.5 (Geriatric Use) reports trial representation and subgroup consistency across 65–74, 75–84, and 85+ years, cross-referencing dose adjustments in Section 2.",
        "url": "https://www.fda.gov/media/142162/download",
    },
    {
        "id": "org-renal-pk",
        "name": "Renal Impairment PK Bridging (Mild, Moderate, Severe & Dialysis)",
        "category": "Kidney Function",
        "plain": "Because kidneys clear many medicines, FDA requires testing how drug blood levels rise in patients with reduced kidney function (eGFR) to set safe reduced doses.",
        "technical": "Dedicated renal impairment PK studies and PopPK covariate analyses evaluate AUC/Cmax across mild, moderate, severe RI (eGFR/CrCL strata), and dialysis to determine Section 8.6 / Section 2 dosing adjustments.",
        "url": "https://www.fda.gov/media/196795/download",
    },
    {
        "id": "org-hepatic-child-pugh",
        "name": "Hepatic Impairment Studies Using Child-Pugh Classes A, B & C",
        "category": "Liver Function",
        "plain": "For liver-metabolized drugs, sponsors test patients with mild, moderate, or severe liver cirrhosis (Child-Pugh A, B, C) to prevent dangerous drug buildup.",
        "technical": "Hepatic impairment PK studies stratify subjects by Child-Pugh Class A (mild), Class B (moderate), and Class C (severe) vs. matched healthy controls to inform Section 8.7 dose reductions or contraindications.",
        "url": "https://www.fda.gov/media/196795/download",
    },
    {
        "id": "org-pk-screen",
        "name": "Pharmacokinetic (PK) Screen in Phase 2/3 & CYP Interactions",
        "category": "Polypharmacy Safety",
        "plain": "Older patients often take five or more prescriptions at once, so sparse blood sampling in late-stage trials checks for unexpected drug-drug or organ-function spikes.",
        "technical": "ICH E7 highlights PopPK screening in Phase 2/3 and targeted CYP2D6/CYP3A4 inhibitor/inducer DDI studies to detect clearance changes in elderly polypharmacy patients.",
        "url": "https://www.fda.gov/media/71317/download",
    },
    {
        "id": "org-frailty-dosing",
        "name": "Avoiding Arbitrary Exclusions of Frail & Comorbid Patients",
        "category": "Trial Generalizability",
        "plain": "Excluding everyone with mild kidney or heart issues from trials leaves doctors flying blind—regulators push sponsors to include real-world older patients with comorbidities.",
        "technical": "ICH E7 advises against unnecessary exclusion of patients with concomitant illnesses so safety/tolerability differences in the real-world geriatric treatment population are captured pre-approval.",
        "url": "https://www.fda.gov/media/71317/download",
    },
]

DIVERSITY_SUBGROUPS = [
    {
        "id": "div-fdora-3601",
        "name": "FDORA § 3601 Mandatory Diversity Action Plans (DAPs)",
        "category": "Statutory Mandate",
        "plain": "A 2022 federal law requires drug and device makers to submit a formal Diversity Action Plan before Phase 3 trials start, setting enrollment goals across age, sex, race, and ethnicity.",
        "technical": "FDORA §§ 3601–3602 added FD&C Act § 505(z) and § 520(g), requiring Diversity Action Plans for Phase 3/pivotal drug, biologic, and device studies specifying enrollment goals and retention strategies.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/diversity-action-plans-improve-enrollment-participants-underrepresented-populations-clinical-studies",
    },
    {
        "id": "div-dap-elements",
        "name": "DAP Core Components: Epidemiology, Goals & Operational Tactics",
        "category": "Plan Structure",
        "plain": "A Diversity Action Plan must ground its enrollment targets in who actually gets the disease—and explain how the sponsor will remove travel, language, or clinic barriers.",
        "technical": "FDA's June 2024 Draft Guidance outlines DAP rationale (disease epidemiology across age, sex, race, ethnicity), disaggregated enrollment goals, and operational measures (decentralized elements, community sites, eligibility broadening).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/diversity-action-plans-improve-enrollment-participants-underrepresented-populations-clinical-studies",
    },
    {
        "id": "div-congress-report",
        "name": "Annual FDA Report to Congress on Diversity Plans (FY23–FY24)",
        "category": "Public Tracking",
        "plain": "FDA now publishes an annual scorecard showing how many Diversity Plans drug and device companies submitted across CDER, CBER, and CDRH.",
        "technical": "Per FDA's FY 2023–2024 Report to Congress, CDER received 124 voluntary diversity plans in FY23 and 161 in FY24 (CBER 9 and 21), ahead of mandatory statutory enforcement 180 days post-final guidance.",
        "url": "https://www.fda.gov/media/184768/download",
    },
    {
        "id": "div-dct-access",
        "name": "Using Decentralized Trials (DCTs) to Reach Rural & Caregiver Populations",
        "category": "Access Enabler",
        "plain": "Home nursing visits, telehealth check-ins, and wearable sensors make it much easier for older adults, rural patients, and working caregivers to join clinical trials.",
        "technical": "FDA links Digital Health Technologies (DHTs) and Decentralized Clinical Trials (DCTs) directly to Diversity Action Plans by reducing geographic and caregiver travel burdens.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/guidance-recap-podcast-digital-health-technologies-remote-data-acquisition-clinical-investigations",
    },
    {
        "id": "div-180day-trigger",
        "name": "180-Day Statutory Compliance Trigger After Final DAP Guidance",
        "category": "Effective Timeline",
        "plain": "Once FDA finalizes its Diversity Action Plan guidance, mandatory submission kicks in 180 days later for newly enrolling pivotal trials.",
        "technical": "Under FDORA § 3602(c), statutory DAP submission requirements apply to clinical studies whose enrollment commences more than 180 days after publication of FDA's Final Guidance.",
        "url": "https://www.fda.gov/news-events/press-announcements/fda-roundup-january-7-2025",
    },
    {
        "id": "div-subgroup-safety",
        "name": "Demographic Subgroup Consistency (Age, Sex, Race & PK Covariates)",
        "category": "Biomarker & Label",
        "plain": "Testing diverse populations ensures doctors know whether a dose needs adjusting for body weight, sex, or genetic ancestry differences before a drug hits pharmacies.",
        "technical": "Integrated NDA/BLA summaries evaluate efficacy and safety consistency across demographic subgroups alongside PopPK covariates to prevent unexpected post-market exposure disparities.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/diversity-action-plans-improve-enrollment-participants-underrepresented-populations-clinical-studies",
    },
]


def build_special_populations(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "pediatric_development": len(PEDIATRIC_DEVELOPMENT),
            "pregnancy_lactation_pllr": len(PREGNANCY_LACTATION_PLLR),
            "geriatric_organ_impairment": len(GERIATRIC_ORGAN_IMPAIRMENT),
            "diversity_subgroups": len(DIVERSITY_SUBGROUPS),
        },
        "pediatric_development": PEDIATRIC_DEVELOPMENT,
        "pregnancy_lactation_pllr": PREGNANCY_LACTATION_PLLR,
        "geriatric_organ_impairment": GERIATRIC_ORGAN_IMPAIRMENT,
        "diversity_subgroups": DIVERSITY_SUBGROUPS,
    }
    (data_dir / "special_populations.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_special_populations.py <site/data>")
    print(json.dumps(build_special_populations(pathlib.Path(sys.argv[1])), indent=2))
'''

SPECIAL_POPULATIONS_JS = '''// Pill by Pill v6.1z: Special Populations — Pediatric (PREA/BPCA/RACE), PLLR, Geriatric/Organ Impairment & Diversity Action Plans
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["pediatric", "Pediatric (PREA/BPCA)", "pediatric_development"],
  ["pllr", "Pregnancy & Lactation (PLLR)", "pregnancy_lactation_pllr"],
  ["geriatric", "Geriatric & Organ PK", "geriatric_organ_impairment"],
  ["diversity", "Diversity Action Plans", "diversity_subgroups"],
];

function specialPopulationsSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Special populations drug development: Pediatric PREA/BPCA, Pregnancy PLLR, Geriatric/Organ Impairment, and FDORA Diversity Action Plans">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Pediatric</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">PREA &amp; BPCA (+6 Mo)</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">iPSP &amp; RACE Act</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sp-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Pregnancy (PLLR)</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Subsections 8.1 / 8.2 / 8.3</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Exposure Registries</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sp-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Geriatric &amp; Organ</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">ICH E7 (65+/75+/85+)</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Renal &amp; Child-Pugh PK</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#sp-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Diversity (FDORA)</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Diversity Action Plans</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">DCTs &amp; Subgroups</text>
      <defs><marker id="sp-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Regulatory frameworks ensure medicines are studied and labeled for children, pregnant/lactating patients, older adults, organ-impaired patients, and diverse trial populations.</figcaption>
  </figure>`;
}

export async function specialPopulationsPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/special_populations.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/special-populations" : "#/ref/special-populations";

  const pills = html`<div class="chips" role="navigation" aria-label="Special populations sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Framework / Standard</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${specialPopulationsSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA PREA/BPCA, RACE Act, PLLR Final Rule, ICH E7 Geriatrics, Renal/Hepatic PK, and FDORA Diversity Action Plan documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Special Populations & Diversity"]] : [REF_HOME, ["Special Populations & Diversity"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Special Populations: Pediatric, PLLR, Geriatric & Trial Diversity",
      lede: env === "explore"
        ? "How drugmakers test and label medicines for children, pregnant or breastfeeding women, older adults, kidney/liver patients, and diverse communities."
        : "PREA & BPCA (+6-mo exclusivity), iPSP/RACE Act, PLLR (8.1–8.3), ICH E7 geriatrics, renal/Child-Pugh PK, and FDORA § 3601 Diversity Action Plans.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on special populations and diversity.", href: env === "explore" ? "#/ref/special-populations" : "#/explore/special-populations" },
        { title: "Rare Diseases & Orphan Drugs", text: "Orphan exclusivity, pediatric PRVs, and expanded access.", href: "#/ref/orphan" },
        { title: "ADME, PK & MedChem", text: "How renal/hepatic clearance and CYP DDIs drive dose adjustments.", href: "#/ref/adme" },
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
    if 'special_populations.js' not in txt:
        for anchor in ('import * as pricingAccess from "./pricing_access.js";\n', 'import * as controlledSubstances from "./controlled_substances.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as specialPopulations from "./special_populations.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as specialPopulations from "./special_populations.js";\n' + txt
            changed = True
    if '"/ref/special-populations"' not in txt:
        for anchor in ('if (path === "/ref/pricing-access")', 'if (path === "/ref/controlled-substances")', 'if (path === "/ref/promotion-transparency")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/special-populations") return { env: "ref", current: "#/ref/special-populations", ...(await specialPopulations.specialPopulationsPage(query, "ref")) };\n  if (path === "/explore/special-populations") return { env: "explore", current: "#/explore/special-populations", ...(await specialPopulations.specialPopulationsPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/special-populations" not in txt:
        for anchor in ('["#/ref/pricing-access", "Pricing, IRA & 340B"]', '["#/ref/controlled-substances", "Controlled substances"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/special-populations", "Special populations"]', 1)
                changed = True
                break
    if "#/explore/special-populations" not in txt:
        for anchor in ('["#/explore/pricing-access", "Pricing, IRA & 340B"]', '["#/explore/controlled-substances", "Controlled substances"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/special-populations", "Special populations"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_special_populations.py" in txt:
        return False
    line = "python3 pipeline/build_special_populations.py site/data\n"
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
    if '"/api/special-populations"' in txt:
        return False
    route = (
        '\n@app.get("/api/special-populations")\n'
        'def api_special_populations():\n'
        '    p = DATA_DIR / "special_populations.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "special_populations.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"special_populations.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    sp_ref = _load(data_dir / "special_populations.json", {}) or {}\n'
        '    for sec_key, sec_q in [("pediatric_development", "pediatric"), ("pregnancy_lactation_pllr", "pllr"), ("geriatric_organ_impairment", "geriatric"), ("diversity_subgroups", "diversity")]:\n'
        '        for item in (sp_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "special_populations",\n'
        '                "group": "Special Populations & Diversity",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/special-populations?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/special-populations?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"pediatric PREA BPCA exclusivity iPSP RACE Act PLLR pregnancy lactation registry geriatric ICH E7 renal hepatic Child-Pugh FDORA Diversity Action Plan {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"special-populations", "#/ref/special-populations"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    sp_doc = _load_json(data_dir / "special_populations.json")\n'
        '    if isinstance(sp_doc, dict) and sp_doc.get("pediatric_development"):\n'
        '        sp_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (sp_doc.get("pediatric_development") or []) + (sp_doc.get("diversity_subgroups") or []))\n'
        '        pages.append(("special-populations", "#/ref/special-populations", "Special Populations: Pediatric, PLLR, Geriatric & Trial Diversity",\n'
        '                      "Primary-sourced guide to PREA/BPCA pediatric exclusivity, PLLR pregnancy labeling, ICH E7 geriatrics, renal/hepatic PK, and FDORA Diversity Action Plans.",\n'
        '                      f"<ul>{sp_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/special-populations"' in txt:
        return False
    for anchor in ('    "/#/explore/pricing-access",', '    "/#/explore/controlled-substances",', '    "/#/explore/promotion-transparency",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/special-populations",\n    "/#/explore/special-populations",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_special_populations_py": _write_if_changed(pipe_dir / "build_special_populations.py", BUILD_SPECIAL_POPULATIONS_PY),
        "special_populations_js": _write_if_changed(js_dir / "special_populations.js", SPECIAL_POPULATIONS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/pricing-access") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/pricing-access", "Pricing, IRA & 340B"]] }];\nconst EXPLORE_NAV = [["#/explore/pricing-access", "Pricing, IRA & 340B"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/pricing-access",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_special_populations.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_special_populations.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"pediatric_development": 6, "pregnancy_lactation_pllr": 6, "geriatric_organ_impairment": 6, "diversity_subgroups": 6}, out

        doc = json.loads((root / "site" / "data" / "special_populations.json").read_text(encoding="utf-8"))
        for k in ("pediatric_development", "pregnancy_lactation_pllr", "geriatric_organ_impairment", "diversity_subgroups"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "special_populations.js").read_text(encoding="utf-8")
        print("V61Z_SPECIAL_POPULATIONS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.1z Special Populations (Pediatric, PLLR, Geriatric & Diversity) patch.")
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
