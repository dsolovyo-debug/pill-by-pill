#!/usr/bin/env python3
"""Pill by Pill v6.2k Patch: Patient-Focused Drug Development (PFDD 1–4), Clinical Outcome Assessments (COAs / PROs), Expanded Access (Project Facilitate) & Right to Try Reference (#/ref/pfdd-coa-expanded-access, #/explore/pfdd-coa-expanded-access, /api/pfdd-coa-expanded-access).

1. Adds `pipeline/build_pfdd_coa_expanded_access.py` -> `site/data/pfdd_coa_expanded_access.json`
   (6 PFDD Guidance Series 1–4 pillars, 6 COA & PRO Measures pillars, 6 Expanded Access &
   Project Facilitate pillars, and 6 Right to Try, PEC & PMI Labeling pillars — 24 primary-sourced
   entries).
2. Adds `site/js/pfdd_coa_expanded_access.js` (`pfddCoaExpandedAccessPage` with inline PFDD,
   COA & Expanded Access SVG + 4 section filters) and wires `#/ref/pfdd-coa-expanded-access`,
   `#/explore/pfdd-coa-expanded-access`, `/api/pfdd-coa-expanded-access`, `REF_NAV_GROUPS`,
   `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `pfdd_coa_expanded_access.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/pfdd-coa-expanded-access/` static SEO page + sitemap
   entry -> 53 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2k_pfdd_coa_expanded_access_right_to_try_patch.py --selftest
  python3 2026-11-24_v6.2k_pfdd_coa_expanded_access_right_to_try_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_PFDD_COA_EXPANDED_ACCESS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2k Patient-Focused Drug Development (PFDD), COAs/PROs, Expanded Access & Right to Try Reference (`site/data/pfdd_coa_expanded_access.json`).

Comprehensive, primary-sourced reference covering:
  1. Patient-Focused Drug Development (PFDD) Guidance Series 1–4 (6 pillars)
  2. Clinical Outcome Assessments (COAs) & Patient-Reported Outcomes (PROs) (6 pillars)
  3. Expanded Access (Compassionate Use) & Project Facilitate (6 pillars)
  4. Right to Try Act, Patient Engagement Collaborative (PEC) & PMI Labeling (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER, OCE, CBER).

Usage:
  python3 pipeline/build_pfdd_coa_expanded_access.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

PFDD_GUIDANCE_SERIES = [
    {
        "id": "pce-pfdd-series-hub",
        "name": "FDA Patient-Focused Drug Development (PFDD) Guidance Series 1–4",
        "category": "21st Century Cures § 3002",
        "plain": "FDA created a 4-part roadmap showing drugmakers how to scientifically measure what patients actually feel, function, and care about during clinical trials.",
        "technical": "Mandated by the 21st Century Cures Act and FDARA Title I, FDA's four-part methodological PFDD Guidance Series standardizes collection and regulatory submission of Patient Experience Data (PED).",
        "url": "https://www.fda.gov/drugs/development-approval-process-drugs/fda-patient-focused-drug-development-guidance-series-enhancing-incorporation-patients-voice-medical",
    },
    {
        "id": "pce-pfdd-g1-input",
        "name": "PFDD Guidance 1: Collecting Comprehensive & Representative Input",
        "category": "Sampling & Equity",
        "plain": "Patient surveys can't just ask a few vocal volunteers—Guidance 1 explains how to gather representative feedback across diverse ages, stages, and backgrounds.",
        "technical": "Guidance 1 details sampling strategies, qualitative/quantitative recruitment, caregiver/proxy reporting, and minimizing selection bias when collecting patient experience data.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/patient-focused-drug-development-collecting-comprehensive-and-representative-input",
    },
    {
        "id": "pce-pfdd-g2-methods",
        "name": "PFDD Guidance 2: Methods to Identify What Is Important to Patients",
        "category": "Qualitative Research",
        "plain": "Through structured interviews and focus groups, researchers pinpoint which symptoms—like fatigue, pain, or mobility—matter most to people living with the disease.",
        "technical": "Guidance 2 covers concept elicitation interviews, focus groups, social-media/mixed-methods research, and conceptual disease models establishing meaningful aspects of health (MAHs).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/patient-focused-drug-development-methods-identify-what-important-patients",
    },
    {
        "id": "pce-pfdd-g3-fit-coa",
        "name": "PFDD Guidance 3: Selecting, Developing, or Modifying Fit-for-Purpose COAs",
        "category": "Instrument Validation",
        "plain": "Once key symptoms are known, Guidance 3 explains how to pick or build a reliable questionnaire or functional test that accurately tracks change.",
        "technical": "Guidance 3 establishes evidentiary standards for Fit-for-Purpose Clinical Outcome Assessments (COAs), including content validity, construct validity, reliability, and ability to detect change.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/patient-focused-drug-development-selecting-developing-or-modifying-fit-purpose-clinical-outcome",
    },
    {
        "id": "pce-pfdd-g4-endpoints",
        "name": "PFDD Guidance 4: Incorporating COAs into Endpoints for Regulatory Decisions",
        "category": "Meaningful Change",
        "plain": "Guidance 4 defines how big a symptom improvement on a patient questionnaire must be to count as a real, clinically meaningful benefit on a drug label.",
        "technical": "Guidance 4 addresses COA endpoint positioning (primary/secondary), meaningful within-patient change (MWPC) thresholds, anchor-based/distribution analyses, and handling intercurrent events/missing data.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/patient-focused-drug-development-incorporating-clinical-outcome-assessments-endpoints-regulatory",
    },
    {
        "id": "pce-pfdd-meetings",
        "name": "FDA-Led & Externally-Led PFDD Public Disease Meetings",
        "category": "Voice of the Patient",
        "plain": "Since 2012, FDA and patient advocacy groups have hosted dozens of public hearings where patients testify directly about daily life with specific diseases.",
        "technical": "Established under PDUFA V in 2012, FDA-led and Externally-Led PFDD meetings produce published 'Voice of the Patient' reports informing CDER/CBER benefit-risk frameworks.",
        "url": "https://www.fda.gov/industry/prescription-drug-user-fee-amendments/fda-led-patient-focused-drug-development-pfdd-public-meetings",
    },
]

COA_PRO_MEASURES = [
    {
        "id": "pce-pro-2009-guidance",
        "name": "Patient-Reported Outcome (PRO) Measures for Labeling Claims (2009)",
        "category": "Labeling Standard",
        "plain": "For a drug box or ad to claim 'reduces morning stiffness', the trial must use a rigorously validated patient-reported questionnaire.",
        "technical": "FDA's landmark December 2009 PRO Guidance defines psychometric validation, recall period, electronic PRO (ePRO) equivalence, and endpoint hierarchy required to support NDA/BLA labeling claims.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/patient-reported-outcome-measures-use-medical-product-development-support-labeling-claims",
    },
    {
        "id": "pce-coa-compendium",
        "name": "FDA Clinical Outcome Assessment (COA) Compendium",
        "category": "Qualification Catalog",
        "plain": "FDA publishes a public catalog of questionnaires and functional tests already accepted in past drug approvals so teams don't reinvent the wheel.",
        "technical": "The FDA COA Compendium summarizes COAs used to support labeling claims across therapeutic areas alongside Drug Development Tool (DDT) Qualification Program entries.",
        "url": "https://www.fda.gov/drugs/development-resources/clinical-outcome-assessment-compendium",
    },
    {
        "id": "pce-coa-4types",
        "name": "Four COA Types: PRO, ClinRO, ObsRO & PerfO (BEST Glossary)",
        "category": "COA Taxonomy",
        "plain": "Clinical outcomes come from four perspectives: what the patient reports (PRO), what a doctor scores (ClinRO), what a parent observes (ObsRO), or a timed physical task (PerfO).",
        "technical": "The FDA–NIH BEST Glossary classifies COAs into Patient-Reported (PRO), Clinician-Reported (ClinRO), Observer-Reported (ObsRO, e.g., pediatric/cognitively impaired), and Performance Outcomes (PerfO, e.g., 6-minute walk).",
        "url": "https://www.fda.gov/media/130138/download",
    },
    {
        "id": "pce-coa-faq",
        "name": "COA Qualification Program & IND Advice Pathways",
        "category": "DDT Qualification",
        "plain": "Researchers can submit a new patient symptom scale to FDA's COA Qualification Program so any future drug trial in that disease can use it.",
        "technical": "Sponsors can seek FDA COA feedback either within an individual IND/NDA review or through the public 3-stage DDT COA Qualification Program (LOI, Qualification Plan, Full Qualification Package).",
        "url": "https://www.fda.gov/about-fda/clinical-outcome-assessment-coa-frequently-asked-questions",
    },
    {
        "id": "pce-pro-cancer-core",
        "name": "Core Patient-Reported Outcomes in Cancer Clinical Trials",
        "category": "Oncology PROs",
        "plain": "In cancer trials, FDA recommends tracking five core patient experiences: disease symptoms, side effects, overall burden, physical function, and ability to work.",
        "technical": "FDA's Core PROs in Cancer Trials guidance recommends standardized collection of disease-related symptoms, symptomatic adverse events (PRO-CTCAE), overall side-effect impact, physical function, and role function.",
        "url": "https://www.fda.gov/media/149994/download",
    },
    {
        "id": "pce-coa-irt-specs",
        "name": "Item Response Theory (IRT) & COA Dataset Submission Specs",
        "category": "eCTD COA Data",
        "plain": "Modern computer-adaptive questionnaires use Item Response Theory to measure symptoms with fewer questions, backed by standardized FDA data tables.",
        "technical": "Supplementing PFDD Guidance 3, FDA issued technical specifications for submitting Item Response Theory (IRT) COA datasets and Cancer PRO datasets in eCTD submissions.",
        "url": "https://www.fda.gov/media/159500/download",
    },
]

EXPANDED_ACCESS = [
    {
        "id": "pce-ea-single-patient",
        "name": "Single-Patient Expanded Access (Compassionate Use) INDs",
        "category": "21 CFR 312 Subpart I",
        "plain": "When a patient with a life-threatening illness has run out of approved treatments and can't join a trial, their doctor can ask FDA and the drugmaker for compassionate access.",
        "technical": "Under 21 CFR 312.310, licensed physicians may submit a single-patient Expanded Access IND (Form FDA 3926) with manufacturer Letter of Authorization (LOA) and IRB review when no comparable therapy exists.",
        "url": "https://www.fda.gov/drugs/investigational-new-drug-application-ind/physicians-how-request-single-patient-expanded-access-compassionate-use",
    },
    {
        "id": "pce-ea-project-facilitate",
        "name": "FDA OCE Project Facilitate (Oncology Single-Patient IND Call Center)",
        "category": "Oncology Support",
        "plain": "Project Facilitate gives cancer doctors a dedicated FDA concierge desk to help file single-patient compassionate-use requests quickly and equitably.",
        "technical": "Launched by FDA's Oncology Center of Excellence, Project Facilitate provides end-to-end support to oncology healthcare providers submitting single-patient Expanded Access INDs and tracking outcomes.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/project-facilitate",
    },
    {
        "id": "pce-ea-emergency-ind",
        "name": "Emergency Single-Patient INDs (Same-Day Phone Authorization)",
        "category": "Emergency Access",
        "plain": "In a true medical crisis where waiting 30 days is impossible, FDA reviewing officials can authorize emergency treatment use by phone the same day.",
        "technical": "For Emergency Expanded Access INDs (21 CFR 312.310(d)), FDA may authorize immediate treatment by telephone prior to written IND/IRB submission, with written Form 3926 follow-up within 15 working days.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/physician-request-single-patient-ind-compassionate-or-emergency-use",
    },
    {
        "id": "pce-ea-30day-vs-emerg",
        "name": "Expanded Access Timelines, IRB Waiver & Manufacturer Consent",
        "category": "Process Rules",
        "plain": "Even when FDA approves compassionate use, the pharmaceutical company must agree to supply the medicine—and an ethics board (IRB) reviews patient safety.",
        "technical": "Non-emergency individual-patient INDs wait 30 days (or earlier FDA notice) plus IRB concurrence (single-chairperson concurrence permitted on Form 3926); manufacturer supply remains voluntary.",
        "url": "https://www.fda.gov/media/144400/download",
    },
    {
        "id": "pce-ea-charging-patients",
        "name": "Charging for Investigational Drugs Under Expanded Access (21 CFR 312.8)",
        "category": "Cost Recovery",
        "plain": "Drugmakers cannot profit from compassionate-use medicines—they may only charge direct manufacturing costs with prior FDA written permission.",
        "technical": "Under 21 CFR 312.8, sponsors require explicit FDA authorization to recover direct manufacturing/handling costs for investigational drugs provided via single-patient, intermediate-size, or treatment INDs.",
        "url": "https://www.fda.gov/news-events/expanded-access/expanded-access-information-patients",
    },
    {
        "id": "pce-ea-physicians-hub",
        "name": "Intermediate-Size & Treatment Expanded Access INDs",
        "category": "Group Access",
        "plain": "When dozens or hundreds of patients need an unapproved drug between Phase 3 completion and final FDA approval, companies can open a group Expanded Access protocol.",
        "technical": "21 CFR 312.315 (Intermediate-Size Patient Populations) and 312.320 (Treatment IND/Protocol) allow broader access to investigational drugs undergoing clinical trials or awaiting NDA/BLA action.",
        "url": "https://www.fda.gov/news-events/expanded-access/expanded-access-information-physicians",
    },
]

RIGHT_TO_TRY_ENGAGEMENT = [
    {
        "id": "pce-rtt-act",
        "name": "Federal Right to Try Act (2018) vs. FDA Expanded Access",
        "category": "Statutory Pathway",
        "plain": "The Right to Try law lets patients with life-threatening illnesses request Phase 1-tested experimental drugs directly from companies without FDA pre-review.",
        "technical": "Enacted May 2018 (FD&C Act § 561B), Right to Try permits eligible patients who exhausted options and cannot join trials to access eligible investigational drugs (completed Phase 1, active IND) directly via manufacturer agreement.",
        "url": "https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options/right-try",
    },
    {
        "id": "pce-rtt-factsheet",
        "name": "Right to Try Annual Reporting & FDA Public Posting",
        "category": "21 CFR 300.200",
        "plain": "Under Right to Try, companies submit an annual summary of doses supplied and known serious side effects, which FDA posts online.",
        "technical": "FDA's role under Right to Try is limited to receiving and publicly posting annual sponsor summaries (number of doses supplied, patients treated, and known serious adverse events) without IND/IRB oversight.",
        "url": "https://www.fda.gov/media/133864/download",
    },
    {
        "id": "pce-pec-ctti",
        "name": "FDA–CTTI Patient Engagement Collaborative (PEC)",
        "category": "Stakeholder Forum",
        "plain": "FDA and Duke's Clinical Trials Transformation Initiative bring patients and caregivers together regularly to make clinical research easier to understand and join.",
        "technical": "Established in 2018 with the Clinical Trials Transformation Initiative (CTTI), the Patient Engagement Collaborative (PEC) advises FDA on patient-centered communications, trial access, and regulatory transparency.",
        "url": "https://www.fda.gov/patients/learn-about-fda-patient-engagement/patient-engagement-collaborative",
    },
    {
        "id": "pce-pmi-outpatient",
        "name": "Patient Medication Information (PMI): One-Page Outpatient Guide",
        "category": "Patient Labeling",
        "plain": "To replace confusing multi-page pharmacy handouts, FDA proposed a clean, standardized one-page Patient Medication Information sheet for every prescription.",
        "technical": "FDA's Patient Medication Information (PMI) initiative proposes a single standardized, one-page Medication Guide format for outpatient prescription drugs and biologics highlighting key risks and directions.",
        "url": "https://www.fda.gov/drugs/fdas-labeling-resources-human-prescription-drugs/patient-medication-information-pmi",
    },
    {
        "id": "pce-pmi-proposed-rule",
        "name": "PMI Proposed Rule: Comprehension & Medication Error Reduction",
        "category": "Health Literacy",
        "plain": "Clear, plain-language one-page drug sheets help patients take medicines safely and avoid dangerous dosing mistakes at home.",
        "technical": "CDER's PMI Proposed Rule aims to harmonize Consumer Medication Information (CMI), Patient Package Inserts (PPIs), and Medication Guides into a single FDA-approved, paper/electronic deliverable.",
        "url": "https://www.fda.gov/drugs/cder-conversations/patient-medication-information-2023-proposed-rule-help-patients-understand-their-prescription",
    },
    {
        "id": "pce-ea-cfr-312-i",
        "name": "21 CFR 312 Subpart I: Safety Reporting in Expanded Access",
        "category": "Pharmacovigilance",
        "plain": "Doctors treating patients under compassionate use must report unexpected serious side effects back to FDA and the drugmaker—though these rarely derail clinical trials.",
        "technical": "FDA's Expanded Access Q&A clarifies IND safety reporting under 21 CFR 312.32 and explains how FDA contextualizes adverse events from severely ill expanded-access patients during NDA/BLA review.",
        "url": "https://www.fda.gov/media/162793/download",
    },
]


def build_pfdd_coa_expanded_access(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "pfdd_guidance_series": len(PFDD_GUIDANCE_SERIES),
            "coa_pro_measures": len(COA_PRO_MEASURES),
            "expanded_access": len(EXPANDED_ACCESS),
            "right_to_try_engagement": len(RIGHT_TO_TRY_ENGAGEMENT),
        },
        "pfdd_guidance_series": PFDD_GUIDANCE_SERIES,
        "coa_pro_measures": COA_PRO_MEASURES,
        "expanded_access": EXPANDED_ACCESS,
        "right_to_try_engagement": RIGHT_TO_TRY_ENGAGEMENT,
    }
    (data_dir / "pfdd_coa_expanded_access.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_pfdd_coa_expanded_access.py <site/data>")
    print(json.dumps(build_pfdd_coa_expanded_access(pathlib.Path(sys.argv[1])), indent=2))
'''

PFDD_COA_EXPANDED_ACCESS_JS = '''// Pill by Pill v6.2k: Patient-Focused Drug Development (PFDD), COAs/PROs, Expanded Access & Right to Try Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["pfdd", "PFDD Guidance Series (1–4)", "pfdd_guidance_series"],
  ["coa", "COAs & PRO Measures", "coa_pro_measures"],
  ["expanded", "Expanded Access & Facilitate", "expanded_access"],
  ["rtt", "Right to Try, PEC & PMI", "right_to_try_engagement"],
];

function pfddCoaExpandedAccessSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Patient-centered drug development and access: PFDD Series 1 to 4, COAs and PROs, Expanded Access Project Facilitate, and Right to Try and PMI">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. PFDD Series 1–4</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Patient Experience Data</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Meaningful Change</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#pce-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. COAs &amp; PROs</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">PRO / ClinRO / ObsRO</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Compendium &amp; Labeling</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#pce-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Expanded Access</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Single-Patient IND (3926)</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Project Facilitate</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#pce-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Right to Try &amp; PMI</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">§561B &amp; PEC Forum</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">1-Page PMI Sheet</text>
      <defs><marker id="pce-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Patient-centered pharma integrates PFDD 1–4 input, validated COAs/PROs, Expanded Access INDs, Right to Try, and plain-language PMI labeling.</figcaption>
  </figure>`;
}

export async function pfddCoaExpandedAccessPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/pfdd_coa_expanded_access.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/pfdd-coa-expanded-access" : "#/ref/pfdd-coa-expanded-access";

  const pills = html`<div class="chips" role="navigation" aria-label="PFDD, COAs, Expanded Access, and Right to Try sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Program / Guidance</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${pfddCoaExpandedAccessSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA PFDD Guidance Series 1–4, COA Compendium / PRO Guidance, Expanded Access / Project Facilitate, Right to Try, PEC, and PMI documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["PFDD, COAs/PROs, Expanded Access & Right to Try"]] : [REF_HOME, ["PFDD, COAs/PROs, Expanded Access & Right to Try"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Patient-Focused Drug Development, COAs, Expanded Access & Right to Try",
      lede: env === "explore"
        ? "How patient voices shape clinical trials, how symptom questionnaires earn drug-label claims, and how seriously ill patients access experimental treatments."
        : "21st Century Cures PFDD Series 1–4, COA/PRO validation (PRO/ClinRO/ObsRO/PerfO), 21 CFR 312 Subpart I Expanded Access / Project Facilitate, Right to Try, and PMI.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on PFDD, COAs/PROs, Expanded Access, and Right to Try.", href: env === "explore" ? "#/ref/pfdd-coa-expanded-access" : "#/explore/pfdd-coa-expanded-access" },
        { title: "GCP, BIMO, Part 11 & CDISC", text: "Electronic informed consent (eIC) and human subject protections.", href: "#/ref/gcp-bimo-cdisc" },
        { title: "Rare Diseases & Orphan Drugs", text: "Ultra-rare patient registries, natural history studies, and access.", href: "#/ref/orphan" },
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
    if 'pfdd_coa_expanded_access.js' not in txt:
        for anchor in ('import * as rmatHctpCgtCmc from "./rmat_hctp_cgt_cmc.js";\n', 'import * as adcsBispecificsOligos from "./adcs_bispecifics_oligos.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as pfddCoaExpandedAccess from "./pfdd_coa_expanded_access.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as pfddCoaExpandedAccess from "./pfdd_coa_expanded_access.js";\n' + txt
            changed = True
    if '"/ref/pfdd-coa-expanded-access"' not in txt:
        for anchor in ('if (path === "/ref/rmat-hctp-cgt-cmc")', 'if (path === "/ref/adcs-bispecifics-oligos")', 'if (path === "/ref/trials")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/pfdd-coa-expanded-access") return { env: "ref", current: "#/ref/pfdd-coa-expanded-access", ...(await pfddCoaExpandedAccess.pfddCoaExpandedAccessPage(query, "ref")) };\n  if (path === "/explore/pfdd-coa-expanded-access") return { env: "explore", current: "#/explore/pfdd-coa-expanded-access", ...(await pfddCoaExpandedAccess.pfddCoaExpandedAccessPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/pfdd-coa-expanded-access" not in txt:
        for anchor in ('["#/ref/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]', '["#/ref/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/pfdd-coa-expanded-access", "PFDD, COAs & Expanded Access"]', 1)
                changed = True
                break
    if "#/explore/pfdd-coa-expanded-access" not in txt:
        for anchor in ('["#/explore/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]', '["#/explore/adcs-bispecifics-oligos", "ADCs, bispecifics & oligos"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/pfdd-coa-expanded-access", "PFDD, COAs & Expanded Access"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_pfdd_coa_expanded_access.py" in txt:
        return False
    line = "python3 pipeline/build_pfdd_coa_expanded_access.py site/data\n"
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
    if '"/api/pfdd-coa-expanded-access"' in txt:
        return False
    route = (
        '\n@app.get("/api/pfdd-coa-expanded-access")\n'
        'def api_pfdd_coa_expanded_access():\n'
        '    p = DATA_DIR / "pfdd_coa_expanded_access.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "pfdd_coa_expanded_access.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"pfdd_coa_expanded_access.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    pce_ref = _load(data_dir / "pfdd_coa_expanded_access.json", {}) or {}\n'
        '    for sec_key, sec_q in [("pfdd_guidance_series", "pfdd"), ("coa_pro_measures", "coa"), ("expanded_access", "expanded"), ("right_to_try_engagement", "rtt")]:\n'
        '        for item in (pce_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "pfdd_coa_expanded_access",\n'
        '                "group": "PFDD, COAs/PROs, Expanded Access & Right to Try",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/pfdd-coa-expanded-access?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/pfdd-coa-expanded-access?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"PFDD patient focused drug development COA clinical outcome assessment PRO ClinRO ObsRO PerfO Expanded Access compassionate use Form 3926 Project Facilitate Right to Try PEC PMI {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"pfdd-coa-expanded-access", "#/ref/pfdd-coa-expanded-access"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    pce_doc = _load_json(data_dir / "pfdd_coa_expanded_access.json")\n'
        '    if isinstance(pce_doc, dict) and pce_doc.get("pfdd_guidance_series"):\n'
        '        pce_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (pce_doc.get("pfdd_guidance_series") or []) + (pce_doc.get("expanded_access") or []))\n'
        '        pages.append(("pfdd-coa-expanded-access", "#/ref/pfdd-coa-expanded-access", "Patient-Focused Drug Development, COAs, Expanded Access & Right to Try",\n'
        '                      "Primary-sourced guide to FDA PFDD Guidance Series 1–4, COAs/PROs, Expanded Access / Project Facilitate, Right to Try, and PMI.",\n'
        '                      f"<ul>{pce_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/pfdd-coa-expanded-access"' in txt:
        return False
    for anchor in ('    "/#/explore/rmat-hctp-cgt-cmc",', '    "/#/explore/adcs-bispecifics-oligos",', '    "/#/explore/gcp-bimo-cdisc",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/pfdd-coa-expanded-access",\n    "/#/explore/pfdd-coa-expanded-access",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_pfdd_coa_expanded_access_py": _write_if_changed(pipe_dir / "build_pfdd_coa_expanded_access.py", BUILD_PFDD_COA_EXPANDED_ACCESS_PY),
        "pfdd_coa_expanded_access_js": _write_if_changed(js_dir / "pfdd_coa_expanded_access.js", PFDD_COA_EXPANDED_ACCESS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/rmat-hctp-cgt-cmc") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]] }];\nconst EXPLORE_NAV = [["#/explore/rmat-hctp-cgt-cmc", "RMAT, HCT/Ps & genome editing"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/rmat-hctp-cgt-cmc",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_pfdd_coa_expanded_access.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_pfdd_coa_expanded_access.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"pfdd_guidance_series": 6, "coa_pro_measures": 6, "expanded_access": 6, "right_to_try_engagement": 6}, out

        doc = json.loads((root / "site" / "data" / "pfdd_coa_expanded_access.json").read_text(encoding="utf-8"))
        for k in ("pfdd_guidance_series", "coa_pro_measures", "expanded_access", "right_to_try_engagement"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "pfdd_coa_expanded_access.js").read_text(encoding="utf-8")
        print("V62K_PFDD_COA_EXPANDED_ACCESS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2k PFDD, COAs/PROs, Expanded Access & Right to Try patch.")
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
