#!/usr/bin/env python3
"""Pill by Pill v6.2v patch: Pharmacovigilance, FAERS/AEMS, Sentinel Active Surveillance & ICH E2A-E2F Signal Management.

Adds:
  - pipeline/build_pv_faers_sentinel.py -> site/data/pv_faers_sentinel.json (24 entries, 4 pillars)
  - site/js/pv_faers_sentinel.js (pvFaersSentinelPage with inline SVG, 4 section filters, zero --card CSS, imports esc from ./ui.js)
  - Wiring in site/js/app.js (#/ref/pv-faers-sentinel, #/explore/pv-faers-sentinel), site/js/layout.js,
    pipeline/run_all.sh, app.py (/api/pv-faers-sentinel), pipeline/build_global_search.py,
    pipeline/build_v60_static_pages.py (/pv-faers-sentinel/ 64th SEO page), and tests/test_v60_site.py.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import tempfile

BUILD_PV_FAERS_SENTINEL_PY = r'''#!/usr/bin/env python3
"""Build Pill by Pill v6.2v Pharmacovigilance, FAERS/AEMS, Sentinel & ICH E2 reference JSON."""
from __future__ import annotations

import json
import pathlib
import sys

CHECKED = "2026-11-26"

SECTIONS = [
    {
        "id": "faers_aems_icsr",
        "title": "1. FAERS / AEMS, MedWatch & Postmarketing ICSRs",
        "summary": "Postmarketing adverse event reporting under 21 CFR 310.305, 314.80, 314.98, and 600.80, electronic E2B(R3) ICSR submissions to FAERS/AEMS, and the four mandatory minimum elements.",
    },
    {
        "id": "sentinel_best_active",
        "title": "2. Sentinel Initiative & CBER BEST Active Surveillance",
        "summary": "FDAAA 2007 active postmarket risk identification using distributed claims and EHR networks (Sentinel System for drugs and CBER BEST Initiative for biologics/vaccines).",
    },
    {
        "id": "ich_e2_lifecycle_reports",
        "title": "3. ICH E2A–E2F Lifecycle Safety Reports (DSUR, PBRER & E2E)",
        "summary": "Harmonized pre-approval and post-approval safety reporting: E2A expedited IND/CIOMS rules, E2D(R1) post-approval ICSRs, E2E pharmacovigilance planning, E2F DSUR, and E2C(R2) PBRER.",
    },
    {
        "id": "signal_detection_gvp",
        "title": "4. Signal Detection, Data Mining & Good Pharmacovigilance Practices",
        "summary": "FDA Good Pharmacovigilance Practices (GVP), empirical Bayesian/PRR disproportionality data mining, case-series evaluation, and Newly Identified Safety Signals (NISS).",
    },
]

ENTRIES = [
    # --- 1. FAERS / AEMS, MedWatch & Postmarketing ICSRs ---
    {
        "id": "pv-faers-aems-submissions",
        "section": "faers_aems_icsr",
        "title": "FDA Adverse Event Monitoring System (AEMS) & FAERS Electronic Submissions",
        "badge": "FAERS / AEMS",
        "summary": "FDA's central postmarketing safety database receives Individual Case Safety Reports (ICSRs) electronically via ESG/SRPs in XML format under 21 CFR 310.305, 314.80, 314.98, and 600.80.",
        "details": "Industry applicants must submit postmarketing ICSRs and attachments electronically rather than on paper Form FDA 3500A, with AEMS modernizing FAERS intake and E2B(R3) regional validation.",
        "source_label": "FDA AEMS Electronic Submissions",
        "source_url": "https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/fda-adverse-event-monitoring-system-aems-electronic-submissions",
    },
    {
        "id": "pv-four-minimum-elements",
        "section": "faers_aems_icsr",
        "title": "Four Mandatory Minimum Elements for a Valid ICSR",
        "badge": "21 CFR 314.80",
        "summary": "A reportable postmarketing adverse event requires four minimum data elements: an identifiable patient, an identifiable reporter, a suspect drug or biological product, and an adverse event or fatal outcome.",
        "details": "Under FDA's Postmarketing Adverse Event Reporting (PAER) Compliance Program, applicants cannot defer reporting by asking a healthcare provider or consumer to file directly once the applicant becomes aware.",
        "source_label": "FDA Postmarketing Adverse Event Reporting Compliance Program",
        "source_url": "https://www.fda.gov/drugs/surveillance-post-drug-approval-activities/postmarketing-adverse-event-reporting-compliance-program",
    },
    {
        "id": "pv-15-day-alert-reports",
        "section": "faers_aems_icsr",
        "title": "15-Day Alert Reports (Serious & Unexpected) vs. Periodic Reports",
        "badge": "Expedited 15-Day",
        "summary": "Serious and unexpected adverse drug experiences must be reported to FDA within 15 calendar days of initial receipt, while all other reportable events are compiled in periodic safety reports.",
        "details": "Applicants must also promptly investigate every 15-day Alert report and submit follow-up information within 15 calendar days of receipt of new data or document unsuccessful follow-up attempts.",
        "source_label": "FDA Postmarketing Drug Safety & Inspection Readiness",
        "source_url": "https://www.fda.gov/files/drugs/published/Postmarketing-Drug-Safety-and-Inspection-Readiness.pdf",
    },
    {
        "id": "pv-electronic-format-icsr",
        "section": "faers_aems_icsr",
        "title": "Mandatory Electronic Format for Postmarketing Safety Reports",
        "badge": "Electronic Format",
        "summary": "Requires applicants with approved NDAs, ANDAs, BLAs, and nonprescription marketed drugs to submit ICSRs, periodic descriptive portions, and attachments electronically in FDA-compatible XML.",
        "details": "Eliminates manual transcription delays and enables automated MedDRA term coding, deduplication, and signal screening across millions of global case reports.",
        "source_label": "FDA Providing Submissions in Electronic Format—Postmarketing Safety Reports",
        "source_url": "https://www.fda.gov/media/71176/download",
    },
    {
        "id": "pv-combination-product-pmsr",
        "section": "faers_aems_icsr",
        "title": "Combination Product Postmarketing Safety Reporting (21 CFR Part 4)",
        "badge": "21 CFR Part 4",
        "summary": "Combination product applicants must satisfy both primary-mode-of-action application reporting (drugs/biologics/devices) and constituent-part rules such as 5-day reports and malfunction reports.",
        "details": "Streamlines duplicate reporting when a single event involves both a drug/biologic constituent and a device constituent (e.g., autoinjector malfunction with an adverse drug event).",
        "source_label": "FDA Postmarketing Safety Reporting for Combination Products",
        "source_url": "https://www.fda.gov/media/111788/download",
    },
    {
        "id": "pv-otc-nonprescription-paer",
        "section": "faers_aems_icsr",
        "title": "Nonprescription (OTC) Monograph Serious Adverse Event Reporting (§ 760)",
        "badge": "FD&C Act § 760",
        "summary": "Manufacturers, packers, and distributors named on OTC monograph drug labels must submit serious adverse event reports within 15 business days and maintain records for 6 years.",
        "details": "Links initial MedWatch 3500A reports and follow-up reports under a single unique identifier in FDA's safety database even when the OTC product lacks an NDA or ANDA.",
        "source_label": "FDA Postmarketing Adverse Event Reporting for Nonprescription Drugs",
        "source_url": "https://www.fda.gov/media/77193/download",
    },
    # --- 2. Sentinel Initiative & CBER BEST Active Surveillance ---
    {
        "id": "pv-sentinel-initiative-fdaaa",
        "section": "sentinel_best_active",
        "title": "FDA Sentinel Initiative (FDAAA 2007 Active Surveillance)",
        "badge": "FDAAA § 905",
        "summary": "Launched in May 2008 under FDAAA 2007, Sentinel queries a distributed electronic healthcare database of claims and EHRs across millions of patients to evaluate drug safety signals proactively.",
        "details": "Unlike passive spontaneous reporting in FAERS, Sentinel captures true exposed denominators and comparator cohorts without pooling raw patient-level records centrally.",
        "source_label": "FDA Sentinel Initiative Overview",
        "source_url": "https://www.fda.gov/safety/fdas-sentinel-initiative",
    },
    {
        "id": "pv-sentinel-complements-faers",
        "section": "sentinel_best_active",
        "title": "Active Distributed Surveillance vs. Passive Spontaneous Reporting",
        "badge": "Denominator Data",
        "summary": "Sentinel does not replace FAERS or VAERS; it complements passive signal generation by testing hypotheses with real-world incidence rates, confounding adjustment, and active comparators.",
        "details": "Enables FDA to assess rare serious events, pregnancy exposures, and drug-drug interactions rapidly using standardized Common Data Model (CDM) analytic modules.",
        "source_label": "FDA Sentinel Initiative Background",
        "source_url": "https://www.fda.gov/safety/fdas-sentinel-initiative/fdas-sentinel-initiative-background",
    },
    {
        "id": "pv-cber-best-biologics",
        "section": "sentinel_best_active",
        "title": "CBER Biologics Effectiveness and Safety (BEST) System",
        "badge": "CBER BEST",
        "summary": "Commenced in October 2017 within CBER's Office of Biostatistics and Pharmacovigilance (OBPV) as the Sentinel component dedicated to vaccines, blood, tissues, and cell/gene therapies.",
        "details": "Integrates large-scale administrative claims, EHRs, and linked claims-EHR datasets with short data lag to support near-real-time biologic safety and effectiveness decisions.",
        "source_label": "FDA CBER BEST System",
        "source_url": "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics/cber-biologics-effectiveness-and-safety-best-system",
    },
    {
        "id": "pv-cber-sentinel-program",
        "section": "sentinel_best_active",
        "title": "CBER Sentinel Program & Linked Claims-EHR Infrastructure",
        "badge": "Linked RWD",
        "summary": "BEST pairs structured billing codes with rich clinical EHR variables (labs, vitals, lot/brand records, and unstructured notes) needed for complex biologics and vaccine safety studies.",
        "details": "Supports both rapid-cycle descriptive monitoring and formal inferential epidemiologic protocols across academic and health-system data partners.",
        "source_label": "FDA CBER Sentinel Program Presentation",
        "source_url": "https://www.fda.gov/media/193267/download",
    },
    {
        "id": "pv-sentinel-five-year-strategy",
        "section": "sentinel_best_active",
        "title": "Sentinel System Strategy: EHR Integration, NLP & Causal Inference",
        "badge": "EHR + NLP",
        "summary": "Expands Sentinel beyond claims-only queries by incorporating inpatient EHRs, natural language processing (NLP) for clinical phenotyping, and modern causal inference tooling.",
        "details": "Broadens FDA's ability to verify outcomes such as anaphylaxis, myocarditis, or acute liver injury where ICD diagnosis codes alone require chart validation.",
        "source_label": "FDA Sentinel System Five-Year Strategy",
        "source_url": "https://www.fda.gov/media/120333/download",
    },
    {
        "id": "pv-cber-other-surveillance",
        "section": "sentinel_best_active",
        "title": "PRISM, CMS Medicare & Interagency Biologics Surveillance",
        "badge": "PRISM / CMS",
        "summary": "Alongside BEST, CBER coordinates vaccine and biologic active surveillance with CMS Medicare claims and legacy PRISM data partners for rapid signal verification.",
        "details": "Provides high-power post-licensure monitoring across older adults and pediatric populations when pre-licensure trials are underpowered for very rare adverse events.",
        "source_label": "FDA Other CBER Surveillance Programs",
        "source_url": "https://www.fda.gov/vaccines-blood-biologics/cber-biologics-effectiveness-and-safety-best-system/other-cber-surveillance-programs",
    },
    # --- 3. ICH E2A-E2F Lifecycle Safety Reports ---
    {
        "id": "pv-ich-e2a-expedited",
        "section": "ich_e2_lifecycle_reports",
        "title": "ICH E2A: Clinical Safety Data Management & Expedited Reporting",
        "badge": "ICH E2A",
        "summary": "Defines core clinical trial safety terms—Adverse Event (AE), Adverse Drug Reaction (ADR), seriousness criteria, and unexpectedness—plus 7-day fatal/life-threatening and 15-day expedited reporting.",
        "details": "Establishes the harmonized pre-approval safety vocabulary used across IND safety reports (21 CFR 312.32), CIOMS I forms, and global regulatory submissions.",
        "source_label": "FDA ICH E2A Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2a-clinical-safety-data-management-definitions-and-standards-expedited-reporting",
    },
    {
        "id": "pv-ich-e2b-r3-icsr",
        "section": "ich_e2_lifecycle_reports",
        "title": "ICH E2B(R3) & FDA Regional ICSR Implementation Guide",
        "badge": "ICH E2B(R3)",
        "summary": "Specifies ISO/HL7 ICSR XML data elements, business rules, and backwards/forwards compatibility (BFC) with E2B(R2) for electronic transmission of drug and biologic safety reports.",
        "details": "FDA's AEMS E2B(R3) Regional Implementation Guide enforces data element validation (e.g., C.1.3 report type, batch/lot numbers, and MedDRA coding) at intake.",
        "source_label": "FDA Regional Implementation Guide for E2B(R3)",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/fda-regional-implementation-guide-e2br3-electronic-transmission-individual-case-safety-reports-drug",
    },
    {
        "id": "pv-ich-e2d-r1-postapproval",
        "section": "ich_e2_lifecycle_reports",
        "title": "ICH E2D(R1): Post-Approval Safety Data & New Digital Sources",
        "badge": "ICH E2D(R1)",
        "summary": "Updates the 2003 E2D framework (finalized March 2026) to clarify ICSR management from unsolicited and solicited sources including social media, patient support programs, and market research.",
        "details": "Aligns post-approval case definitions, clock start points (Day 0), and reporter/patient identifiability standards with ICH E2B(R3) specifications.",
        "source_label": "FDA ICH E2D(R1) Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2dr1-post-approval-safety-data-definitions-and-standards-management-and-reporting-individual-case",
    },
    {
        "id": "pv-ich-e2e-pv-planning",
        "section": "ich_e2_lifecycle_reports",
        "title": "ICH E2E: Pharmacovigilance Planning & Safety Specification",
        "badge": "ICH E2E",
        "summary": "Structures a two-part framework—Safety Specification (important identified risks, potential risks, and missing information) and Pharmacovigilance Plan—submitted at NDA/BLA filing or postmarket.",
        "details": "Distinguishes routine pharmacovigilance from additional pharmacoepidemiologic actions (e.g., registries, drug-event monitoring, or targeted active surveillance).",
        "source_label": "FDA ICH E2E Pharmacovigilance Planning",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2e-pharmacovigilance-planning",
    },
    {
        "id": "pv-ich-e2f-dsur",
        "section": "ich_e2_lifecycle_reports",
        "title": "ICH E2F: Development Safety Update Report (DSUR) & IND Annuals",
        "badge": "ICH E2F DSUR",
        "summary": "Provides a single harmonized annual safety review for investigational drugs across clinical trials, which FDA accepts in place of the traditional 21 CFR 312.33 IND Annual Report.",
        "details": "Summarizes cumulative serious adverse reactions, evolving benefit-risk, important nonclinical/CMC findings, and global regulatory actions over the Data Lock Point (DLP) year.",
        "source_label": "FDA ICH E2F DSUR Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2f-development-safety-update-report",
    },
    {
        "id": "pv-ich-e2c-r2-pbrer",
        "section": "ich_e2_lifecycle_reports",
        "title": "ICH E2C(R2): Periodic Benefit-Risk Evaluation Report (PBRER)",
        "badge": "ICH E2C(R2)",
        "summary": "Replaces legacy PSUR/PADER/PAER formats with a modular, cumulative benefit-risk evaluation of marketed products under 21 CFR 314.80(c)(2) and 600.80(c)(2).",
        "details": "Integrates interval and cumulative safety signals with estimated patient exposure and efficacy data in Sections 15–18 to support global regulatory benefit-risk conclusions.",
        "source_label": "FDA ICH E2C(R2) PBRER Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2cr2-periodic-benefit-risk-evaluation-report-pbrer",
    },
    # --- 4. Signal Detection, Data Mining & Good Pharmacovigilance Practices ---
    {
        "id": "pv-fda-gvp-guidance",
        "section": "signal_detection_gvp",
        "title": "Good Pharmacovigilance Practices & Pharmacoepidemiologic Assessment",
        "badge": "FDA GVP",
        "summary": "Outlines FDA best practices for (1) safety signal identification, (2) case-series clinical review and pharmacoepidemiologic evaluation, and (3) pharmacovigilance plan development.",
        "details": "Emphasizes obtaining complete follow-up on serious events, assessing biological plausibility, dechallenge/rechallenge, and comparing against background disease incidence.",
        "source_label": "FDA Good Pharmacovigilance Practices Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-pharmacovigilance-practices-and-pharmacoepidemiologic-assessment",
    },
    {
        "id": "pv-data-mining-prr-mgps",
        "section": "signal_detection_gvp",
        "title": "Disproportionality Data Mining (PRR, ROR & MGPS/EBGM)",
        "badge": "Data Mining",
        "summary": "Quantitative disproportionality scores compare observed vs. expected drug-event reporting fractions in FAERS—adjusted for age, sex, and year—to prioritize signals for manual clinical review.",
        "details": "FDA notes data mining is a hypothesis-generating screening aid, never standalone proof of causality, and cannot compute true incidence rates without denominator data.",
        "source_label": "Data Mining at FDA White Paper",
        "source_url": "https://www.fda.gov/science-research/data-mining/data-mining-fda-white-paper",
    },
    {
        "id": "pv-case-series-causality",
        "section": "signal_detection_gvp",
        "title": "Descriptive Case-Series Review & Causality Assessment",
        "badge": "Case Series",
        "summary": "When disproportionality or sentinel reports flag a potential risk, reviewers assemble a deduplicated case series examining time-to-onset, dose-response, confounders, and dechallenge/rechallenge.",
        "details": "Standardized case definitions and targeted follow-up questionnaires separate true drug-induced syndromes (e.g., DILI, SJS/TEN) from underlying disease progression.",
        "source_label": "FDA GVP Case Series & Signal Assessment",
        "source_url": "https://www.fda.gov/media/71546/download",
    },
    {
        "id": "pv-niss-cder-mapp",
        "section": "signal_detection_gvp",
        "title": "Newly Identified Safety Signals (NISS) Evaluation & Tracking",
        "badge": "CDER MAPP",
        "summary": "CDER's structured NISS workflow tracks potential postmarket safety signals from initial identification through multidisciplinary evaluation, indeterminate active monitoring, or regulatory action.",
        "details": "Coordinates safety reviewers across OSE, OND, and compliance offices to determine whether labeling changes (§ 505(o)(4)), PMRs (§ 505(o)(3)), REMS, or public communications are warranted.",
        "source_label": "FDA CDER NISS MAPP Policy",
        "source_url": "https://www.fda.gov/media/137475/download",
    },
    {
        "id": "pv-staff-best-practices",
        "section": "signal_detection_gvp",
        "title": "FDA Staff Best Practices for Postmarketing Safety Surveillance",
        "badge": "FDAAA § 921",
        "summary": "Documents FDA's lifecycle surveillance routines—screening newly approved NMEs, reviewing FAERS/literature/foreign actions, and posting quarterly potential signals of serious risks.",
        "details": "Provides public transparency on emerging drug safety evaluations while signal confirmation and regulatory options are actively assessed.",
        "source_label": "FDA Staff Best Practices for Postmarketing Surveillance",
        "source_url": "https://www.fda.gov/media/130216/download",
    },
    {
        "id": "pv-aems-e2br3-standards",
        "section": "signal_detection_gvp",
        "title": "AEMS E2B(R3) Data Standards & E2D(R1) Alignment",
        "badge": "AEMS Standards",
        "summary": "Aligns FDA's AEMS electronic intake rules with ICH E2D(R1) definitions (e.g., C.1.3 report type and MedDRA hierarchy) to keep global ICSR data clean for automated signal detection.",
        "details": "Reduces schema rejections and ensures consistent capture of suspect/concomitant drugs, batch/lot identifiers, and clinical narratives across international regulators.",
        "source_label": "FDA AEMS E2B(R3) Data Standards",
        "source_url": "https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems/fda-adverse-event-monitoring-system-aems-e2br3-data-standards",
    },
]


def build_pv_faers_sentinel(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "title": "Pharmacovigilance, FAERS / AEMS, Sentinel & ICH E2 Safety Surveillance",
        "subtitle": "Postmarketing ICSRs (21 CFR 314.80/600.80), Sentinel & CBER BEST active surveillance, ICH E2A–E2F reports, and disproportionality signal management.",
        "sections": SECTIONS,
        "entries": ENTRIES,
        "counts": {
            "sections": len(SECTIONS),
            "entries": len(ENTRIES),
        },
    }
    out_path = out_dir / "pv_faers_sentinel.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv=None) -> int:
    out_dir = pathlib.Path(argv[1]) if argv and len(argv) > 1 else pathlib.Path("site/data")
    res = build_pv_faers_sentinel(out_dir)
    print(f"Built {out_dir / 'pv_faers_sentinel.json'} ({res['counts']['entries']} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
'''

PV_FAERS_SENTINEL_JS = r'''import { getJSON } from "./data.js";
import { esc } from "./ui.js";

const PV_SVG = `
<svg viewBox="0 0 760 150" role="img" aria-label="Pharmacovigilance lifecycle from ICSR intake and Sentinel active surveillance to signal evaluation and regulatory action" style="width:100%;max-width:760px;height:auto;display:block;margin:1rem auto;">
  <rect x="8" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="92" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. ICSR Intake</text>
  <text x="92" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">FAERS / AEMS XML</text>
  <text x="92" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">15-Day &amp; Periodic</text>
  <text x="92" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">ICH E2B(R3) / E2D(R1)</text>

  <line x1="176" y1="71" x2="198" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="198,66 208,71 198,76" fill="var(--accent)"/>

  <rect x="208" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="292" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Active RWD</text>
  <text x="292" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Sentinel System</text>
  <text x="292" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">CBER BEST Biologics</text>
  <text x="292" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">Claims + EHR Cohorts</text>

  <line x1="376" y1="71" x2="398" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="398,66 408,71 398,76" fill="var(--accent)"/>

  <rect x="408" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="492" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Signal Triage</text>
  <text x="492" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">PRR / EBGM Mining</text>
  <text x="492" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Case Series &amp; NISS</text>
  <text x="492" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">PBRER &amp; DSUR</text>

  <line x1="576" y1="71" x2="598" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="598,66 608,71 598,76" fill="var(--accent)"/>

  <rect x="608" y="18" width="144" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="680" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Safety Action</text>
  <text x="680" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Labeling § 505(o)(4)</text>
  <text x="680" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">REMS / PMRs</text>
  <text x="680" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">Public Alerts</text>
</svg>`;

export async function pvFaersSentinelPage(view, mode = "ref") {
  view.innerHTML = `<div class="panel" style="background:var(--paper);padding:1.25rem;border:1px solid var(--line);border-radius:10px;"><p>Loading Pharmacovigilance, FAERS/AEMS &amp; Sentinel reference…</p></div>`;
  const data = await getJSON("data/pv_faers_sentinel.json");
  const isExplore = mode === "explore";
  let activeSec = "all";

  function render() {
    const filtered = activeSec === "all"
      ? data.entries
      : data.entries.filter((e) => e.section === activeSec);

    const pills = [
      `<button type="button" class="pill ${activeSec === "all" ? "active" : ""}" data-sec="all" style="padding:0.35rem 0.75rem;border-radius:999px;border:1px solid var(--line);background:${activeSec === "all" ? "var(--accent)" : "var(--paper)"};color:${activeSec === "all" ? "#fff" : "var(--ink)"};cursor:pointer;">All (${data.entries.length})</button>`,
      ...data.sections.map((s) => {
        const cnt = data.entries.filter((e) => e.section === s.id).length;
        const active = activeSec === s.id;
        return `<button type="button" class="pill ${active ? "active" : ""}" data-sec="${esc(s.id)}" style="padding:0.35rem 0.75rem;border-radius:999px;border:1px solid var(--line);background:${active ? "var(--accent)" : "var(--paper)"};color:${active ? "#fff" : "var(--ink)"};cursor:pointer;">${esc(s.title)} (${cnt})</button>`;
      }),
    ].join(" ");

    const secMap = Object.fromEntries(data.sections.map((s) => [s.id, s]));
    const cards = filtered.map((e) => {
      const sec = secMap[e.section];
      return `
        <article style="background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:1rem;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;gap:0.5rem;flex-wrap:wrap;">
            <span style="font-size:0.78rem;font-weight:700;color:var(--accent);text-transform:uppercase;">${esc(e.badge)}</span>
            <span style="font-size:0.78rem;color:var(--muted);">${esc(sec ? sec.title : e.section)}</span>
          </div>
          <h3 style="margin:0.4rem 0 0.5rem;font-size:1.05rem;color:var(--ink);">${esc(e.title)}</h3>
          <p style="margin:0 0 0.5rem;color:var(--ink);line-height:1.5;">${esc(e.summary)}</p>
          ${isExplore ? "" : `<p style="margin:0 0 0.6rem;color:var(--muted);font-size:0.92rem;line-height:1.45;">${esc(e.details)}</p>`}
          <a href="${esc(e.source_url)}" target="_blank" rel="noopener noreferrer" style="font-size:0.85rem;color:var(--accent);font-weight:600;">${esc(e.source_label)} ↗</a>
        </article>`;
    }).join("");

    view.innerHTML = `
      <section style="background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:1.25rem;margin-bottom:1rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.75rem;">
          <div>
            <h1 style="margin:0 0 0.35rem;color:var(--ink);">${esc(data.title)}</h1>
            <p style="margin:0;color:var(--muted);">${esc(data.subtitle)}</p>
          </div>
          <a href="#/${isExplore ? "ref" : "explore"}/pv-faers-sentinel" style="padding:0.4rem 0.8rem;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);text-decoration:none;font-size:0.9rem;">
            ${isExplore ? "Switch to Reference →" : "← Switch to Explore"}
          </a>
        </div>
        ${PV_SVG}
        <div style="display:flex;flex-wrap:wrap;gap:0.45rem;margin-top:0.75rem;">${pills}</div>
      </section>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:0.9rem;">
        ${cards}
      </div>
      <p style="margin-top:1rem;font-size:0.82rem;color:var(--muted);">Checked ${esc(data.checked)} against primary FDA &amp; ICH regulatory sources.</p>
    `;

    view.querySelectorAll("[data-sec]").forEach((btn) => {
      btn.addEventListener("click", () => {
        activeSec = btn.getAttribute("data-sec") || "all";
        render();
      });
    });
  }

  render();
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
    imp = 'import { pvFaersSentinelPage } from "./pv_faers_sentinel.js";\n'
    if "pvFaersSentinelPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/pv-faers-sentinel") return pvFaersSentinelPage(view, "ref");\n'
        '  if (path === "/explore/pv-faers-sentinel") return pvFaersSentinelPage(view, "explore");\n'
    )
    if '"/ref/pv-faers-sentinel"' not in txt:
        for anchor in (
            'if (path === "/ref/user-fees-prv")',
            'if (path === "/ref/packaging-el-dscsa")',
            'route();',
        ):
            if anchor in txt:
                txt = txt.replace(anchor, route_snip + "  " + anchor, 1)
                changed = True
                break
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
    ref_entry = '      { label: "Pharmacovigilance & Sentinel", href: "#/ref/pv-faers-sentinel" },\n'
    if "#/ref/pv-faers-sentinel" not in txt:
        anchor = '{ label: "User Fees, PRVs & Expedited", href: "#/ref/user-fees-prv" },'
        if anchor in txt:
            txt = txt.replace(anchor, anchor + "\n" + ref_entry.rstrip("\n"), 1)
            changed = True
        elif "REF_NAV_GROUPS" in txt:
            txt = txt.replace("];", ref_entry + "];", 1)
            changed = True
    exp_entry = '  { label: "Pharmacovigilance & Sentinel", href: "#/explore/pv-faers-sentinel" },\n'
    if "#/explore/pv-faers-sentinel" not in txt:
        anchor = '{ label: "User Fees, PRVs & Expedited", href: "#/explore/user-fees-prv" },'
        if anchor in txt:
            txt = txt.replace(anchor, anchor + "\n" + exp_entry.rstrip("\n"), 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    line = "python3 pipeline/build_pv_faers_sentinel.py site/data\n"
    if "build_pv_faers_sentinel.py" not in txt:
        anchor = "python3 pipeline/build_user_fees_prv.py site/data\n"
        if anchor in txt:
            txt = txt.replace(anchor, anchor + line, 1)
        else:
            txt += ("\n" if not txt.endswith("\n") else "") + line
        path.write_text(txt, encoding="utf-8")
        return True
    return False


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "/api/pv-faers-sentinel" in txt:
        return False
    block = (
        '\n@app.get("/api/pv-faers-sentinel")\n'
        'def api_pv_faers_sentinel():\n'
        '    return _read_site_json("data/pv_faers_sentinel.json")\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "pv_faers_sentinel.json" in txt:
        return False
    snippet = (
        '\n    pv_path = data_dir / "pv_faers_sentinel.json"\n'
        '    if pv_path.is_file():\n'
        '        pv_obj = json.loads(pv_path.read_text(encoding="utf-8"))\n'
        '        for item in pv_obj.get("entries", []):\n'
        '            entries.append({\n'
        '                "id": item["id"],\n'
        '                "title": item["title"],\n'
        '                "subtitle": f"Pharmacovigilance & Sentinel · {item.get(\'badge\', \'\')}",\n'
        '                "kind": "Pharmacovigilance",\n'
        '                "href": "#/ref/pv-faers-sentinel",\n'
        '                "keywords": f"{item[\'title\']} {item.get(\'summary\', \'\')} {item.get(\'badge\', \'\')}",\n'
        '            })\n'
    )
    anchor = '    payload = {"checked": CHECKED'
    if anchor in txt:
        txt = txt.replace(anchor, snippet + "\n" + anchor, 1)
        path.write_text(txt, encoding="utf-8")
        return True
    return False


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "pv-faers-sentinel" in txt:
        return False
    snippet = (
        '\n    pv_file = data_dir / "pv_faers_sentinel.json"\n'
        '    if pv_file.is_file():\n'
        '        pv_d = json.loads(pv_file.read_text(encoding="utf-8"))\n'
        '        _write_landing(\n'
        '            site_dir / "pv-faers-sentinel" / "index.html",\n'
        '            "Pharmacovigilance, FAERS / AEMS, Sentinel & ICH E2 | Pill by Pill",\n'
        '            pv_d.get("subtitle", ""),\n'
        '            "#/ref/pv-faers-sentinel",\n'
        '            pv_d.get("entries", []),\n'
        '        )\n'
        '        written_urls.append(f"{BASE_URL}/pv-faers-sentinel/")\n'
    )
    anchor = "    written_urls = []"
    if anchor in txt:
        txt = txt.replace(anchor, anchor + snippet, 1)
        path.write_text(txt, encoding="utf-8")
        return True
    return False


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "#/ref/pv-faers-sentinel" in txt:
        return False
    addition = '    "#/ref/pv-faers-sentinel",\n    "#/explore/pv-faers-sentinel",\n'
    anchor = '"#/ref/user-fees-prv",'
    if anchor in txt:
        txt = txt.replace(anchor, anchor + "\n" + addition.rstrip("\n"), 1)
        path.write_text(txt, encoding="utf-8")
        return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    root = pathlib.Path(root)
    changed = {}
    changed["build_pv_faers_sentinel.py"] = _write_if_changed(
        root / "pipeline" / "build_pv_faers_sentinel.py", BUILD_PV_FAERS_SENTINEL_PY
    )
    changed["pv_faers_sentinel.js"] = _write_if_changed(
        root / "site" / "js" / "pv_faers_sentinel.js", PV_FAERS_SENTINEL_JS
    )
    changed["app.js"] = _patch_app_js(root / "site" / "js" / "app.js")
    changed["layout.js"] = _patch_layout_js(root / "site" / "js" / "layout.js")
    changed["run_all.sh"] = _patch_run_all(root / "pipeline" / "run_all.sh")
    changed["app.py"] = _patch_app_py(root / "app.py")
    changed["build_global_search.py"] = _patch_global_search(root / "pipeline" / "build_global_search.py")
    changed["build_v60_static_pages.py"] = _patch_static_pages(root / "pipeline" / "build_v60_static_pages.py")
    changed["test_v60_site.py"] = _patch_test_v60_site(root / "tests" / "test_v60_site.py")
    return changed


def selftest() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "tests").mkdir()
        (root / "site" / "js" / "app.js").write_text('if (path === "/ref/user-fees-prv") return x;\nroute();\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [\n  { label: "User Fees, PRVs & Expedited", href: "#/ref/user-fees-prv" },\n];\nconst EXPLORE_NAV = [\n  { label: "User Fees, PRVs & Expedited", href: "#/explore/user-fees-prv" },\n];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text('#!/bin/sh\npython3 pipeline/build_user_fees_prv.py site/data\n', encoding="utf-8")
        (root / "app.py").write_text('from fastapi import FastAPI\napp = FastAPI()\n', encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('ROUTES = [\n    "#/ref/user-fees-prv",\n]\n', encoding="utf-8")

        res1 = apply_patch(root)
        assert all(res1.values()), f"Expected all changed on first run: {res1}"
        res2 = apply_patch(root)
        assert not any(res2.values()), f"Expected idempotent second run: {res2}"

        # Execute builder and validate JSON
        subprocess.run([sys.executable, str(root / "pipeline" / "build_pv_faers_sentinel.py"), str(root / "site" / "data")], check=True)
        data = json.loads((root / "site" / "data" / "pv_faers_sentinel.json").read_text(encoding="utf-8"))
        assert len(data["sections"]) == 4
        assert len(data["entries"]) == 24
        for sec in data["sections"]:
            cnt = sum(1 for e in data["entries"] if e["section"] == sec["id"])
            assert cnt == 6, f"Section {sec['id']} count {cnt} != 6"
        for e in data["entries"]:
            assert e["source_url"].startswith("https://"), f"Non-HTTPS URL: {e['source_url']}"
        js_txt = (root / "site" / "js" / "pv_faers_sentinel.js").read_text(encoding="utf-8")
        assert "--card" not in js_txt
        assert "./dom.js" not in js_txt
        assert "./ui.js" in js_txt
        app_js_txt = (root / "site" / "js" / "app.js").read_text(encoding="utf-8")
        assert app_js_txt.index('"/ref/pv-faers-sentinel"') < app_js_txt.index("route();")
        print("V62V_PV_FAERS_SENTINEL_SELFTEST_PASSED")


def main(argv=None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if "--selftest" in args:
        selftest()
        return 0
    root = pathlib.Path(args[0]) if args else pathlib.Path(".")
    res = apply_patch(root)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
