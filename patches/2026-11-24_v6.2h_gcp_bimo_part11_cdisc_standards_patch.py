#!/usr/bin/env python3
"""Pill by Pill v6.2h Patch: Good Clinical Practice (ICH E6(R3)), Bioresearch Monitoring (BIMO) Inspections, Electronic Consent / 21 CFR Part 11 & CDISC Study Data Standards Reference (#/ref/gcp-bimo-cdisc, #/explore/gcp-bimo-cdisc, /api/gcp-bimo-cdisc).

1. Adds `pipeline/build_gcp_bimo_cdisc.py` -> `site/data/gcp_bimo_cdisc.json` (6 ICH E6(R3) GCP &
   Risk-Based Monitoring pillars, 6 FDA BIMO Inspections pillars, 6 Electronic Informed Consent &
   21 CFR Part 11 pillars, and 6 CDISC SDTM/ADaM & Study Data Standards pillars — 24 primary-sourced
   entries).
2. Adds `site/js/gcp_bimo_cdisc.js` (`gcpBimoCdiscPage` with inline GCP, BIMO, Part 11 & CDISC SVG
   + 4 section filters) and wires `#/ref/gcp-bimo-cdisc`, `#/explore/gcp-bimo-cdisc`,
   `/api/gcp-bimo-cdisc`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `gcp_bimo_cdisc.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/gcp-bimo-cdisc/` static SEO page + sitemap entry ->
   50 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2h_gcp_bimo_part11_cdisc_standards_patch.py --selftest
  python3 2026-11-24_v6.2h_gcp_bimo_part11_cdisc_standards_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_GCP_BIMO_CDISC_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2h GCP (ICH E6(R3)), BIMO Inspections, Part 11 & CDISC Study Data Standards Reference (`site/data/gcp_bimo_cdisc.json`).

Comprehensive, primary-sourced reference covering:
  1. ICH E6(R3) Good Clinical Practice & Risk-Based Monitoring (6 pillars)
  2. FDA Bioresearch Monitoring (BIMO) Inspections (6 pillars)
  3. Electronic Informed Consent (eIC) & 21 CFR Part 11 (6 pillars)
  4. CDISC SDTM / ADaM & Study Data Technical Conformance (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA OMP, OII/BIMO, CDER, CBER, OHRP).

Usage:
  python3 pipeline/build_gcp_bimo_cdisc.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

GCP_E6R3_RBM = [
    {
        "id": "gcp-omp-modernization",
        "name": "ICH E6(R3) Good Clinical Practice & Clinical Trial Modernization",
        "category": "Global GCP Standard",
        "plain": "Good Clinical Practice (ICH E6(R3)) is the global rulebook protecting clinical trial volunteers and ensuring every lab result can be trusted.",
        "technical": "FDA CDER's Office of Medical Policy (OMP) leads ICH E6(R3) GCP modernization, embedding Quality-by-Design (QbD), fit-for-purpose data governance, and proportionate oversight across 21 CFR 312.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder-offices-and-divisions/office-medical-policy",
    },
    {
        "id": "gcp-rbm-qa-2023",
        "name": "Risk-Based Monitoring (RBM) of Clinical Investigations (Apr 2023 Q&A)",
        "category": "Sponsor Oversight",
        "plain": "Instead of sending monitors to re-check every single routine lab sheet at every hospital, FDA encourages focusing audits on the trial's biggest safety and data risks.",
        "technical": "FDA's April 2023 RBM Q&A expands on 2013 oversight guidance, detailing risk assessment, Critical-to-Quality (CtQ) factor identification, monitoring plan content, and CAPA escalation.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-based-approach-monitoring-clinical-investigations-questions-and-answers",
    },
    {
        "id": "gcp-rbm-oversight-2013",
        "name": "Oversight of Clinical Investigations: Enhancing Human Subject Protection",
        "category": "Quality Management",
        "plain": "Risk-based monitoring directs sponsor attention toward patient consent, safety reporting, and primary efficacy endpoints rather than clerical paperwork.",
        "technical": "FDA's Oversight of Clinical Investigations guidance establishes that targeted on-site and centralized monitoring satisfy 21 CFR 312.50, 312.53(d), and 312.56(a) sponsor obligations.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring",
    },
    {
        "id": "gcp-centralized-monitoring",
        "name": "Centralized Statistical Monitoring & Targeted Source Data Verification",
        "category": "Data Integrity",
        "plain": "Central data teams run automated statistical checks across all trial sites to spot unusual patterns, missing visits, or potential data fabrication early.",
        "technical": "Centralized monitoring uses statistical/graphical analytics across sites to detect protocol deviations, outlier variance, and fraud signals, replacing 100% Source Data Verification (SDV) with targeted SDV.",
        "url": "https://www.fda.gov/media/116754/download",
    },
    {
        "id": "gcp-qbd-rbm-workshop",
        "name": "Quality by Design (QbD) in Clinical Protocol & Workflow Design",
        "category": "Proactive Design",
        "plain": "Building quality into a clinical trial from day one means simplifying eligibility rules and visit schedules so errors don't happen in the first place.",
        "technical": "FDA–Duke-Margolis QbD/RBM frameworks embed Critical-to-Quality (CtQ) design upfront in protocols, eCRFs, and CRO/site workflows to prevent systemic errors rather than inspecting them out later.",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/building-quality-design-and-conduct-clinical-studies-integrating-quality-design-qbd-and-risk-based",
    },
    {
        "id": "gcp-pediatric-safeguards",
        "name": "Additional Safeguards for Children & Non-US Clinical Data (21 CFR 50/312)",
        "category": "Vulnerable Subjects",
        "plain": "Trials enrolling children or run outside the United States must meet strict ethical assent, IRB, and GCP standards before FDA accepts the data.",
        "technical": "FDA's HSP/BIMO regulations enforce Subpart D pediatric safeguards (21 CFR 50.50–50.56) and GCP acceptance standards for foreign clinical studies not conducted under an IND (21 CFR 312.120).",
        "url": "https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/fdas-hspbimo-initiative-accomplishments-update-june-2014",
    },
]

BIMO_INSPECTIONS = [
    {
        "id": "bimo-program-info",
        "name": "FDA Bioresearch Monitoring (BIMO) Program Overview",
        "category": "Inspection Authority",
        "plain": "FDA's BIMO inspectors visit hospitals, drug sponsors, CROs, and ethics boards (IRBs) to verify clinical trial data is real and patients were protected.",
        "technical": "Established in 1977, FDA's Bioresearch Monitoring (BIMO) program conducts on-site inspections and data audits across clinical investigators, sponsors/CROs, IRBs, bioequivalence sites, and GLP labs.",
        "url": "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/fda-bioresearch-monitoring-information/bioresearch-monitoring-program-information",
    },
    {
        "id": "bimo-compliance-programs",
        "name": "BIMO Compliance Program Manuals (7348.811 Investigators, Sponsors, IRBs)",
        "category": "Inspection Playbooks",
        "plain": "FDA publishes the exact inspection manuals—like CP 7348.811 for clinical investigators—showing what auditors check during a site visit.",
        "technical": "BIMO Compliance Programs (e.g., 7348.811 Clinical Investigators & Sponsor-Investigators, 7348.810 Sponsors/CROs, 7348.809 IRBs, 7353.001 Postmarketing) standardize inspectional scope and Form FDA 483 criteria.",
        "url": "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-program-manual/bioresearch-monitoring-program-bimo-compliance-programs",
    },
    {
        "id": "bimo-inspection-metrics",
        "name": "BIMO Inspection Metrics & NAI / VAI / OAI Classifications",
        "category": "Audit Outcomes",
        "plain": "Every FDA trial inspection ends with a score: No Action Indicated (NAI), Voluntary Action Indicated (VAI), or Official Action Indicated (OAI) for serious violations.",
        "technical": "FDA publishes annual BIMO Inspection Metrics tracking domestic and foreign inspections across CDER, CBER, and CDRH classified as NAI, VAI, or OAI (triggering Warning Letters or data exclusion).",
        "url": "https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/bimo-inspection-metrics",
    },
    {
        "id": "bimo-chapter-48",
        "name": "FDA Compliance Program Guidance Manual Chapter 48 (BIMO)",
        "category": "Field Operations",
        "plain": "Chapter 48 guides FDA field investigators on tracing drug accountability, lab logs, and signed consent forms back to original hospital charts.",
        "technical": "Compliance Program Chapter 48 sets operational procedures for ORA/OII and Center reviewers conducting routine surveillance and for-cause directed BIMO audits.",
        "url": "https://www.fda.gov/media/75909/download",
    },
    {
        "id": "bimo-fdora-processes",
        "name": "Processes & Practices Applicable to BIMO Inspections (FD&C Act § 704(a)(5))",
        "category": "FDORA Inspection Rules",
        "plain": "Under updated federal law, FDA clarified how BIMO inspectors request electronic trial records, hold closeout meetings, and resolve inspection disputes.",
        "technical": "Implementing FDORA § 3612, FDA's BIMO Processes and Practices guidance codifies pre-announced vs. unannounced inspection communication, record-request protocols, and post-inspection Form 483 responses.",
        "url": "https://www.fda.gov/media/179027/download",
    },
    {
        "id": "bimo-cber-clinical-hold",
        "name": "CBER BIMO: Clinical Holds, Data Rejection & Investigator Disqualification",
        "category": "Enforcement Actions",
        "plain": "If a trial site falsifies records or endangers volunteers, FDA can freeze the study (clinical hold), throw out the site's data, or ban the doctor from future trials.",
        "technical": "BIMO enforcement remedies include IND clinical holds (21 CFR 312.42), rejection of unreliable site/study data, Warning Letters, and clinical investigator disqualification (NIDPOE).",
        "url": "https://www.fda.gov/media/134478/download",
    },
]

ECONSENT_PART11 = [
    {
        "id": "eic-ohrp-fda-qa",
        "name": "Use of Electronic Informed Consent (eIC) — Joint FDA & OHRP Q&A",
        "category": "Subject Consent",
        "plain": "Patients can review interactive videos and sign clinical trial consent forms on a tablet or at home—as long as they can still ask questions and get a copy.",
        "technical": "Joint FDA–OHRP eIC Guidance governs electronic informed consent processes under 21 CFR Parts 11, 50, and 56 and 45 CFR Part 46, covering identity verification, comprehension checks, and IRB review.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers",
    },
    {
        "id": "eic-process-pdf",
        "name": "eIC Security, HIPAA Integration & Remote Consent Documentation",
        "category": "21 CFR Part 50",
        "plain": "Electronic consent platforms must timestamp signatures, protect patient privacy, and keep older versions archived whenever a trial protocol changes.",
        "technical": "FDA's eIC framework requires version-controlled consent archives, Part 11-compliant audit trails and electronic signatures, pediatric assent workflows, and secure remote subject access.",
        "url": "https://www.fda.gov/media/116850/download",
    },
    {
        "id": "part11-clinical-systems",
        "name": "Electronic Systems, Records & Signatures in Clinical Investigations (Part 11)",
        "category": "ALCOA+ & Audit Trails",
        "plain": "Every digital database, eCRF, and eTMF used in a clinical trial must log who entered or changed every piece of data and why.",
        "technical": "FDA's Part 11 Clinical Investigations Guidance applies 21 CFR Part 11 validation, role-based access, immutable computer-generated audit trails, and e-signature controls to EDC, ePRO, IRT, and cloud systems.",
        "url": "https://www.fda.gov/media/166215/download",
    },
    {
        "id": "part11-esource-data",
        "name": "Electronic Source Data (eSource) in Clinical Investigations",
        "category": "Direct Data Capture",
        "plain": "Capturing trial measurements directly into electronic systems—from blood-pressure cuffs or lab feeds—cuts transcription errors and preserves data lineage.",
        "technical": "FDA's eSource Guidance defines data originators, automated data element identifiers, investigator sign-off, and retention of electronic source records for BIMO inspection reconstruction.",
        "url": "https://www.fda.gov/media/85183/download",
    },
    {
        "id": "part11-ehr-edc",
        "name": "Use of Electronic Health Record (EHR) Data in Clinical Investigations",
        "category": "EHR-to-EDC Interop",
        "plain": "While FDA doesn't regulate hospital EHRs under Part 11, the drug sponsor's EDC system pulling EHR data into a trial must meet Part 11 integrity rules.",
        "technical": "FDA's EHR Data Guidance clarifies that Part 11 applies to the sponsor's Electronic Data Capture (EDC) system extracting EHR records—requiring certified interoperability, audit trails, and source verification.",
        "url": "https://www.fda.gov/media/97567/download",
    },
    {
        "id": "part11-scope-application",
        "name": "21 CFR Part 11 Scope & Application (Predicate Rule Alignment)",
        "category": "Core Regulation",
        "plain": "FDA's Part 11 rule ensures that digital trial records and electronic signatures are just as trustworthy and legally binding as signed paper.",
        "technical": "FDA's Part 11 Scope and Application guidance establishes risk-based validation, legacy system enforcement discretion, and alignment with underlying predicate rules (21 CFR Parts 50, 56, 312, 211).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application",
    },
]

CDISC_STUDY_DATA = [
    {
        "id": "cdisc-sdtcg-2026",
        "name": "FDA Study Data Technical Conformance Guide (SDTCG)",
        "category": "eCTD Data Specs",
        "plain": "Before submitting a new drug to FDA, sponsors must format every clinical trial spreadsheet into standardized CDISC tables so reviewers can analyze them fast.",
        "technical": "FDA's Study Data Technical Conformance Guide provides technical specifications for submitting standardized clinical and nonclinical study datasets (CDISC SDTM, ADaM, SEND, Define-XML) in eCTD Module 5.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/study-data-technical-conformance-guide-technical-specifications-document",
    },
    {
        "id": "cdisc-study-data-cder",
        "name": "Study Data Standards for Submission to CDER & CBER (§ 745A(a))",
        "category": "Mandatory eCTD",
        "plain": "Under federal law, clinical trial data in NDAs, BLAs, and most INDs must follow FDA-supported CDISC data standards—or face a Refuse-to-File rejection.",
        "technical": "Pursuant to FD&C Act § 745A(a), FDA mandates conformance to Data Standards Catalog versions of CDISC SDTM (tabulation), ADaM (analysis), SEND (nonclinical), and Define-XML v2.x.",
        "url": "https://www.fda.gov/industry/study-data-standards-resources/study-data-submission-cder-and-cber",
    },
    {
        "id": "cdisc-sdtcg-pdf",
        "name": "Reviewer's Guides (cSDRG / ADRG) & Validation Rules",
        "category": "Submission QC",
        "plain": "Every trial dataset package includes a Reviewer's Guide explaining any validation warnings, special variables, or custom analysis flags.",
        "technical": "Sponsors must include Clinical Study Data Reviewer's Guides (cSDRG) and Analysis Data Reviewer's Guides (ADRG) documenting FDA Business/Validator Rule checks and tracebacks from ADaM to SDTM.",
        "url": "https://www.fda.gov/media/88173/download",
    },
    {
        "id": "cdisc-bimo-datasets",
        "name": "Submitting Clinical Trial Datasets for BIMO Inspections",
        "category": "Inspection Readiness",
        "plain": "FDA requires a dedicated BIMO data package—listing every hospital site, investigator, and protocol deviation—so inspectors know where to audit.",
        "technical": "FDA's BIMO Technical Conformance Guide specifies site-level summary listings (clinsite.xpt), subject-level line listings, and protocol-deviation datasets enabling rapid BIMO site selection.",
        "url": "https://www.fda.gov/media/173587/download",
    },
    {
        "id": "cdisc-sdtm-adam-define",
        "name": "SDTM Tabulation, ADaM Analysis & Controlled Terminology",
        "category": "Data Architecture",
        "plain": "SDTM organizes raw patient visits into uniform domains (demographics, labs, adverse events), while ADaM prepares analysis-ready tables for statistics.",
        "technical": "CDISC SDTM standardizes raw clinical observations into domains (DM, AE, LB, VS, EX) using NCI Enterprise Vocabulary Services (EVS) terminology; ADaM (ADSL, ADAE, ADTTE) supports reproducible efficacy/safety tables.",
        "url": "https://www.fda.gov/media/153632/download",
    },
    {
        "id": "cdisc-clinical-compliance",
        "name": "Clinical Investigator Inspection List (CLIIL) & Enforcement",
        "category": "Public Registry",
        "plain": "FDA's public Clinical Investigator Inspection List lets sponsors check whether a trial doctor or site has past inspection findings.",
        "technical": "CDER maintains the Clinical Investigator Inspection List (CLIIL) and BIMO enforcement database tracking inspected investigators, dates, and final compliance classifications.",
        "url": "https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/clinical-investigations-compliance-enforcement",
    },
]


def build_gcp_bimo_cdisc(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "gcp_e6r3_rbm": len(GCP_E6R3_RBM),
            "bimo_inspections": len(BIMO_INSPECTIONS),
            "econsent_part11": len(ECONSENT_PART11),
            "cdisc_study_data": len(CDISC_STUDY_DATA),
        },
        "gcp_e6r3_rbm": GCP_E6R3_RBM,
        "bimo_inspections": BIMO_INSPECTIONS,
        "econsent_part11": ECONSENT_PART11,
        "cdisc_study_data": CDISC_STUDY_DATA,
    }
    (data_dir / "gcp_bimo_cdisc.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_gcp_bimo_cdisc.py <site/data>")
    print(json.dumps(build_gcp_bimo_cdisc(pathlib.Path(sys.argv[1])), indent=2))
'''

GCP_BIMO_CDISC_JS = '''// Pill by Pill v6.2h: ICH E6(R3) GCP, FDA BIMO Inspections, Electronic Consent / Part 11 & CDISC Study Data Standards Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["gcp", "ICH E6(R3) GCP & RBM", "gcp_e6r3_rbm"],
  ["bimo", "FDA BIMO Inspections", "bimo_inspections"],
  ["part11", "eConsent & 21 CFR Part 11", "econsent_part11"],
  ["cdisc", "CDISC SDTM / ADaM", "cdisc_study_data"],
];

function gcpBimoCdiscSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Clinical trial quality and data integrity: ICH E6(R3) GCP and RBM, FDA BIMO Inspections, eConsent and 21 CFR Part 11, and CDISC SDTM and ADaM">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. ICH E6(R3) GCP</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">QbD &amp; Risk-Based Mon.</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Centralized Analytics</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#gcp-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. FDA BIMO</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Site, Sponsor &amp; IRB Audits</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">NAI / VAI / OAI &amp; 483s</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#gcp-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. eIC &amp; Part 11</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">21 CFR 50 / 56 / 11</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">eSource &amp; Audit Trails</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#gcp-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. CDISC Data</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">SDTM, ADaM &amp; Define</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">SDTCG &amp; BIMO Datasets</text>
      <defs><marker id="gcp-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Clinical trial integrity spans ICH E6(R3) GCP and risk-based monitoring, FDA BIMO inspections, eConsent/Part 11 audit trails, and CDISC SDTM/ADaM submission datasets.</figcaption>
  </figure>`;
}

export async function gcpBimoCdiscPage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/gcp_bimo_cdisc.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/gcp-bimo-cdisc" : "#/ref/gcp-bimo-cdisc";

  const pills = html`<div class="chips" role="navigation" aria-label="GCP, BIMO, Part 11, and CDISC study data sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Standard / Program</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${gcpBimoCdiscSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA ICH E6(R3) / Risk-Based Monitoring, Bioresearch Monitoring (BIMO), Electronic Informed Consent / 21 CFR Part 11, and CDISC Study Data Technical Conformance documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["GCP (E6(R3)), BIMO, Part 11 & CDISC"]] : [REF_HOME, ["GCP (E6(R3)), BIMO, Part 11 & CDISC"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Good Clinical Practice (E6(R3)), BIMO, Part 11 & CDISC Standards",
      lede: env === "explore"
        ? "How clinical trials protect volunteers, how FDA inspects study sites, how digital consent works, and how patient data is formatted into CDISC tables."
        : "ICH E6(R3) GCP & Risk-Based Monitoring, FDA BIMO Compliance Programs (7348.811), eConsent & 21 CFR Part 11 eSource, and CDISC SDTM/ADaM (§ 745A(a)).",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on GCP, BIMO, Part 11, and CDISC standards.", href: env === "explore" ? "#/ref/gcp-bimo-cdisc" : "#/explore/gcp-bimo-cdisc" },
        { title: "Clinical Trial Design & Endpoints", text: "Randomization, blinding, estimands, and adaptive trial designs.", href: "#/ref/trials" },
        { title: "Real-World Evidence & Digital Health", text: "DCTs, DHTs, OMOP common data models, and RWE submissions.", href: "#/ref/rwe" },
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
    if 'gcp_bimo_cdisc.js' not in txt:
        for anchor in ('import * as oncologyOce from "./oncology_oce.js";\n', 'import * as excipientsDmfsNano from "./excipients_dmfs_nano.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as gcpBimoCdisc from "./gcp_bimo_cdisc.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as gcpBimoCdisc from "./gcp_bimo_cdisc.js";\n' + txt
            changed = True
    if '"/ref/gcp-bimo-cdisc"' not in txt:
        for anchor in ('if (path === "/ref/oncology-oce")', 'if (path === "/ref/excipients-dmfs-nano")', 'if (path === "/ref/trials")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/gcp-bimo-cdisc") return { env: "ref", current: "#/ref/gcp-bimo-cdisc", ...(await gcpBimoCdisc.gcpBimoCdiscPage(query, "ref")) };\n  if (path === "/explore/gcp-bimo-cdisc") return { env: "explore", current: "#/explore/gcp-bimo-cdisc", ...(await gcpBimoCdisc.gcpBimoCdiscPage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/gcp-bimo-cdisc" not in txt:
        for anchor in ('["#/ref/oncology-oce", "Oncology OCE & master trials"]', '["#/ref/excipients-dmfs-nano", "Excipients, DMFs & nano"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]', 1)
                changed = True
                break
    if "#/explore/gcp-bimo-cdisc" not in txt:
        for anchor in ('["#/explore/oncology-oce", "Oncology OCE & master trials"]', '["#/explore/excipients-dmfs-nano", "Excipients, DMFs & nano"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/gcp-bimo-cdisc", "GCP, BIMO, Part 11 & CDISC"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_gcp_bimo_cdisc.py" in txt:
        return False
    line = "python3 pipeline/build_gcp_bimo_cdisc.py site/data\n"
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
    if '"/api/gcp-bimo-cdisc"' in txt:
        return False
    route = (
        '\n@app.get("/api/gcp-bimo-cdisc")\n'
        'def api_gcp_bimo_cdisc():\n'
        '    p = DATA_DIR / "gcp_bimo_cdisc.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "gcp_bimo_cdisc.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"gcp_bimo_cdisc.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    gcp_ref = _load(data_dir / "gcp_bimo_cdisc.json", {}) or {}\n'
        '    for sec_key, sec_q in [("gcp_e6r3_rbm", "gcp"), ("bimo_inspections", "bimo"), ("econsent_part11", "part11"), ("cdisc_study_data", "cdisc")]:\n'
        '        for item in (gcp_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "gcp_bimo_cdisc",\n'
        '                "group": "GCP (E6(R3)), BIMO, Part 11 & CDISC",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/gcp-bimo-cdisc?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/gcp-bimo-cdisc?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"GCP ICH E6(R3) RBM risk based monitoring QbD BIMO bioresearch monitoring 7348.811 Form 483 eConsent eIC 21 CFR Part 11 eSource CDISC SDTM ADaM Define-XML SDTCG {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"gcp-bimo-cdisc", "#/ref/gcp-bimo-cdisc"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    gcp_doc = _load_json(data_dir / "gcp_bimo_cdisc.json")\n'
        '    if isinstance(gcp_doc, dict) and gcp_doc.get("gcp_e6r3_rbm"):\n'
        '        gcp_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (gcp_doc.get("gcp_e6r3_rbm") or []) + (gcp_doc.get("cdisc_study_data") or []))\n'
        '        pages.append(("gcp-bimo-cdisc", "#/ref/gcp-bimo-cdisc", "Good Clinical Practice (E6(R3)), BIMO, Part 11 & CDISC Standards",\n'
        '                      "Primary-sourced guide to ICH E6(R3) GCP & Risk-Based Monitoring, FDA BIMO inspections, eConsent & 21 CFR Part 11, and CDISC SDTM/ADaM.",\n'
        '                      f"<ul>{gcp_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/gcp-bimo-cdisc"' in txt:
        return False
    for anchor in ('    "/#/explore/oncology-oce",', '    "/#/explore/excipients-dmfs-nano",', '    "/#/explore/amr-antiinfectives",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/gcp-bimo-cdisc",\n    "/#/explore/gcp-bimo-cdisc",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_gcp_bimo_cdisc_py": _write_if_changed(pipe_dir / "build_gcp_bimo_cdisc.py", BUILD_GCP_BIMO_CDISC_PY),
        "gcp_bimo_cdisc_js": _write_if_changed(js_dir / "gcp_bimo_cdisc.js", GCP_BIMO_CDISC_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/oncology-oce") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/oncology-oce", "Oncology OCE & master trials"]] }];\nconst EXPLORE_NAV = [["#/explore/oncology-oce", "Oncology OCE & master trials"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/oncology-oce",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_gcp_bimo_cdisc.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_gcp_bimo_cdisc.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"gcp_e6r3_rbm": 6, "bimo_inspections": 6, "econsent_part11": 6, "cdisc_study_data": 6}, out

        doc = json.loads((root / "site" / "data" / "gcp_bimo_cdisc.json").read_text(encoding="utf-8"))
        for k in ("gcp_e6r3_rbm", "bimo_inspections", "econsent_part11", "cdisc_study_data"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "gcp_bimo_cdisc.js").read_text(encoding="utf-8")
        print("V62H_GCP_BIMO_CDISC_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2h GCP, BIMO, Part 11 & CDISC patch.")
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
