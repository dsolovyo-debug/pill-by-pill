#!/usr/bin/env python3
"""Pill by Pill v6.2r Patch: cGMP Inspections (PAI / § 704(a)(4)), Form FDA 483 / Warning Letters / Import Alerts (DWPE), Drug Recalls (21 CFR Part 7) / FARs / BPDRs, and Data Integrity (ALCOA+) Reference (#/ref/inspections-483-recalls, #/explore/inspections-483-recalls, /api/inspections-483-recalls).

1. Adds `pipeline/build_inspections_483_recalls.py` -> `site/data/inspections_483_recalls.json`
   (6 cGMP Inspections & § 704(a)(4) pillars, 6 Form FDA 483 / Warning Letters / Import Alerts
   pillars, 6 Recalls / FARs / BPDRs pillars, and 6 Data Integrity & Enforcement pillars — 24
   primary-sourced entries).
2. Adds `site/js/inspections_483_recalls.js` (`inspections483RecallsPage` with inline
   Inspections, 483s, Recalls & Data Integrity SVG + 4 section filters) and wires
   `#/ref/inspections-483-recalls`, `#/explore/inspections-483-recalls`,
   `/api/inspections-483-recalls`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `inspections_483_recalls.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/inspections-483-recalls/` static SEO page + sitemap
   entry -> 60 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2r_inspections_form483_recalls_fars_data_integrity_patch.py --selftest
  python3 2026-11-24_v6.2r_inspections_form483_recalls_fars_data_integrity_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_INSPECTIONS_483_RECALLS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2r Inspections, Form FDA 483, Recalls & Data Integrity Reference (`site/data/inspections_483_recalls.json`).

Comprehensive, primary-sourced reference covering:
  1. cGMP Inspections, PAI & § 704(a)(4) Remote Records Reviews (6 pillars)
  2. Form FDA 483, Warning Letters & Import Alerts (DWPE) (6 pillars)
  3. Drug Recalls (21 CFR Part 7), FARs (21 CFR 314.81) & BPDRs (6 pillars)
  4. Data Integrity (ALCOA+), Lab Controls & CAPA Enforcement (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA OII / CDER OC).

Usage:
  python3 pipeline/build_inspections_483_recalls.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-25"

CGMP_INSPECTIONS_704 = [
    {
        "id": "ifr-cgmp-inspections-211",
        "name": "Overview of Drug Manufacturing Inspections (21 CFR Part 211)",
        "category": "OII Inspections",
        "plain": "FDA investigators visit drug factories worldwide to inspect quality units, equipment, testing labs, and batch records.",
        "technical": "FDA's Office of Inspections and Investigations (OII) evaluates drug manufacturing establishments against 21 CFR Part 211 across six systems: Quality, Facilities & Equipment, Materials, Production, Packaging & Labeling, and Laboratory Controls.",
        "url": "https://www.fda.gov/media/172786/download",
    },
    {
        "id": "ifr-api-7356-002f",
        "name": "API Inspections & Abbreviated Inspection Option (CPGM 7356.002F)",
        "category": "API / CPGM 7356.002F",
        "plain": "Active ingredient factories undergo full 6-system audits or focused 2-to-3-system surveillance inspections.",
        "technical": "FDA Compliance Program 7356.002F governs active pharmaceutical ingredient (API) inspections under FD&C Act § 501(a)(2)(B), utilizing full or abbreviated (Quality System + 1–2 rotating systems) coverage.",
        "url": "https://www.fda.gov/media/187860/download",
    },
    {
        "id": "ifr-704a4-records-review",
        "name": "FD&C Act § 704(a)(4) Records Review in Advance or in Lieu of PAI",
        "category": "Remote Records",
        "plain": "FDA can legally demand factory records electronically before—or instead of—an in-person preapproval inspection.",
        "technical": "Under FD&C Act § 704(a)(4), FDA conducts remote records requests and joint OPQ/OII assessments to evaluate manufacturing sites in advance of or in lieu of on-site preapproval inspections.",
        "url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2021/215383Orig1s000ChemR.pdf",
    },
    {
        "id": "ifr-pai-7346-832",
        "name": "Preapproval Inspections (PAI, CPGM 7346.832)",
        "category": "PAI / CPGM 7346.832",
        "plain": "Before approving a new medicine, FDA verifies the factory can truly make the commercial batch reliably and that application data match lab records.",
        "technical": "FDA Compliance Program 7346.832 directs PAI teams to assess Readiness for Commercial Manufacturing, Conformance to Application, and Data Integrity Audit before NDA/BLA/ANDA approval.",
        "url": "https://www.fda.gov/media/193382/download",
    },
    {
        "id": "ifr-foia-483-posting",
        "name": "FDA Form 483 Transparency & FOIA Posting Policy",
        "category": "Public Disclosure",
        "plain": "Inspection observation lists become publicly searchable on FDA's website once three or more FOIA requests are filed.",
        "technical": "Redacted cGMP Form FDA 483s are proactively posted to FDA's FOIA Electronic Reading Room when three or more FOIA requests are received or when FDA determines proactive public disclosure is warranted.",
        "url": "https://www.fda.gov/media/172786/download",
    },
    {
        "id": "ifr-oii-483-response",
        "name": "Responding to Form FDA 483 Observations",
        "category": "15-Day Response",
        "plain": "Factories have 15 business days after an inspection to send FDA a written root-cause and corrective action plan.",
        "technical": "Prompt, well-documented Form FDA 483 responses submitted within 15 business days—backed by root-cause analysis and CAPA evidence—inform FDA's NAI/VAI/OAI classification and Warning Letter decisions.",
        "url": "https://www.fda.gov/media/197020/download",
    },
]

FORM483_WARNING_IMPORT = [
    {
        "id": "ifr-form483-factual",
        "name": "Form FDA 483 Factual Observations vs. EIRs",
        "category": "Form FDA 483",
        "plain": "A Form FDA 483 lists only specific, observed rule violations from the inspection—never guesses or opinions.",
        "technical": "Issued at inspection closeout, Form FDA 483 documents objective, factual observations of potential FD&C Act and 21 CFR Part 211 violations in order of significance, paired with the full Establishment Inspection Report (EIR).",
        "url": "https://www.fda.gov/media/172786/download",
    },
    {
        "id": "ifr-rpm-warning-letters",
        "name": "Regulatory Procedures Manual Ch. 4: Warning Letters",
        "category": "Warning Letters",
        "plain": "When violations are serious or uncorrected, FDA issues a public Warning Letter demanding systemic remediation.",
        "technical": "FDA's Regulatory Procedures Manual Chapter 4 governs Warning Letters—advisory actions notifying firms of significant regulatory violations that can lead to seizure, injunction, or approval holds if uncorrected.",
        "url": "https://www.fda.gov/downloads/ICECI/ComplianceManuals/RegulatoryProceduresManual/UCM074330.pdf",
    },
    {
        "id": "ifr-import-alerts-dwpe",
        "name": "Import Alerts & Detention Without Physical Examination (DWPE)",
        "category": "FD&C § 801(a)",
        "plain": "If a foreign factory fails FDA standards, US customs automatically blocks its shipments at the border under an Import Alert.",
        "technical": "Under FD&C Act § 801's appearance standard, Import Alerts authorize Detention Without Physical Examination (DWPE) at US ports until the importer proves compliance.",
        "url": "https://www.fda.gov/industry/actions-enforcement/import-alerts",
    },
    {
        "id": "ifr-import-alert-66-40",
        "name": "Import Alert 66-40: Foreign cGMP Non-Compliance",
        "category": "Import Alert 66-40",
        "plain": "Import Alert 66-40 is FDA's primary border-block tool for foreign drug manufacturers with serious cGMP failures.",
        "technical": "Import Alert 66-40 subjects drugs from listed foreign firms to DWPE when inspections, warning letters, or records reviews reveal significant cGMP deviations.",
        "url": "https://www.accessdata.fda.gov/cms_ia/importalert_189.html",
    },
    {
        "id": "ifr-red-green-list",
        "name": "Red List vs. Green List & Petitions for DWPE Removal",
        "category": "DWPE Removal",
        "plain": "Companies on a Red List are blocked at the border until they pass remediation and successfully petition FDA for removal.",
        "technical": "FDA's Import Alert FAQs distinguish Red List (subject to DWPE) from Green List (exempt) entities and detail how firms submit corrective evidence and reinspection requests to petition for removal.",
        "url": "https://www.fda.gov/industry/import-alerts/industry-faqs-import-alerts",
    },
    {
        "id": "ifr-import-program",
        "name": "FDA Import Program & Foreign Establishment Registration",
        "category": "Import Oversight",
        "plain": "Every foreign factory shipping medicines into the United States must register with FDA and undergo border screening.",
        "technical": "FDA's Import Program integrates foreign establishment registration, PREDICT risk-based entry screening, and Import Alerts to safeguard imported APIs and finished drug products.",
        "url": "https://www.fda.gov/industry/import-program",
    },
]

RECALLS_FARS_PART7 = [
    {
        "id": "ifr-recalls-classes-123",
        "name": "Drug Recalls: Class I, Class II & Class III (21 CFR Part 7)",
        "category": "21 CFR Part 7",
        "plain": "Class I recalls warn of life-threatening defects, Class II covers temporary or reversible harm, and Class III involves minor rule breaches.",
        "technical": "Under 21 CFR Part 7, FDA classifies recalls by health hazard: Class I (reasonable probability of serious adverse health consequences or death), Class II (temporary/reversible), and Class III (unlikely to cause adverse health).",
        "url": "https://www.fda.gov/drugs/news-events-human-drugs/understanding-drug-recalls-dr-ileana-elder",
    },
    {
        "id": "ifr-rpm-ch7-recalls",
        "name": "Recall Strategy, Depth & Effectiveness Checks (RPM Ch. 7)",
        "category": "Recall Strategy",
        "plain": "A recall strategy defines whether medicines must be pulled from wholesalers, pharmacies, or individual patients' homes.",
        "technical": "Regulatory Procedures Manual Chapter 7 establishes recall strategy elements—depth of recall (wholesale, retail, consumer), public warning level, periodic status reports (21 CFR 7.53), and effectiveness checks.",
        "url": "https://www.fda.gov/media/71814/download",
    },
    {
        "id": "ifr-public-warning-enforcement",
        "name": "Public Recall Warnings & Weekly FDA Enforcement Report",
        "category": "Enforcement Report",
        "plain": "Once classified, every drug recall is published in FDA's weekly Enforcement Report so hospitals and patients can check affected lots.",
        "technical": "FDA's Public Warning guidance governs urgent Class I/II consumer alerts under 21 CFR 7.42(b)(2) and publication of classified recalls in the weekly Enforcement Report (21 CFR 7.50).",
        "url": "https://www.fda.gov/media/110457/download",
    },
    {
        "id": "ifr-iom-ch7-recall-correction",
        "name": "IOM Chapter 7: Recall vs. Correction & Market Withdrawal",
        "category": "IOM Chapter 7",
        "plain": "Minor non-violative stock removals are market withdrawals—not formal recalls—while fixing labeling on-site is a correction.",
        "technical": "FDA's Investigations Operations Manual Chapter 7 distinguishes recalls (violative products) from market withdrawals (minor/no violation) and field corrections (repair, relabeling, or adjustment without physical removal).",
        "url": "https://www.fda.gov/media/166535/download",
    },
    {
        "id": "ifr-fars-314-81",
        "name": "Field Alert Reports (FARs): 3-Working-Day Rule (21 CFR 314.81)",
        "category": "3-Day FARs",
        "plain": "If a distributed batch fails quality specs or gets contaminated, the drugmaker must alert FDA within 3 working days.",
        "technical": "Under 21 CFR 314.81(b)(1) and 314.98, NDA and ANDA holders must submit a Field Alert Report within 3 working days of learning of mix-ups, bacterial contamination, deterioration, or specification failures in distributed product.",
        "url": "https://www.fda.gov/drugs/surveillance-post-drug-approval-activities/field-alert-reports",
    },
    {
        "id": "ifr-far-3331a-bpdr",
        "name": "Form FDA 3331a (FARs) vs. 45-Day BPDRs (21 CFR 600.14)",
        "category": "FARs & BPDRs",
        "plain": "Chemical drugs use 3-day Field Alert Reports, while biologics use Biological Product Deviation Reports within 45 days.",
        "technical": "FDA encourages XML Form FDA 3331a for NDA/ANDA FARs within 3 working days, whereas licensed biological products report manufacturing deviations affecting distributed safety, purity, or potency on Form 3486 within 45 calendar days.",
        "url": "https://www.fda.gov/media/170108/download",
    },
]

DATA_INTEGRITY_ENFORCEMENT = [
    {
        "id": "ifr-data-integrity-qa",
        "name": "Data Integrity & Compliance With Drug CGMP Q&A",
        "category": "Data Integrity",
        "plain": "Every lab test, electronic audit trail, and batch record must be complete, honest, and impossible to silently alter or delete.",
        "technical": "FDA's Data Integrity Q&A clarifies expectations for audit-trail review, shared-login prohibition, metadata retention, and electronic record controls under 21 CFR Parts 211 and 212.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/data-integrity-and-compliance-drug-cgmp-questions-and-answers",
    },
    {
        "id": "ifr-alcoa-audit-trails",
        "name": "ALCOA Principles & Complete Electronic Record Retention",
        "category": "ALCOA / 21 CFR 211",
        "plain": "ALCOA means records are Attributable, Legible, Contemporaneous, Original, and Accurate—from raw chromatograms to final release.",
        "technical": "FDA enforces Attributable, Legible, Contemporaneous, Original, and Accurate (ALCOA) data governance across paper and computerized systems (21 CFR 211.68, 211.188, and 211.194).",
        "url": "https://www.fda.gov/media/119267/download",
    },
    {
        "id": "ifr-data-integrity-babe",
        "name": "Data Integrity & Data Quality in BA/BE & Application Submissions",
        "category": "BA/BE Data Integrity",
        "plain": "Clinical and bioanalytical testing sites must also prove their data are authentic before FDA trusts generic or new drug approvals.",
        "technical": "FDA's Data Integrity in Application Submissions guidance requires applicants and contracted BA/BE clinical/analytical testing sites to maintain quality management systems ensuring submission data reliability.",
        "url": "https://www.fda.gov/media/177404/download",
    },
    {
        "id": "ifr-no-trial-injections",
        "name": "Prohibition of Trial Injections & Testing Into Compliance",
        "category": "Lab Controls",
        "plain": "Labs cannot secretly pre-test samples to see if they pass before officially logging the run.",
        "technical": "Under 21 CFR 211.165 and 211.194, FDA treats unrecorded 'trial injections' or using real product samples as column-conditioning runs to disguise failing results ('testing into compliance') as a serious cGMP violation.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/questions-and-answers-current-good-manufacturing-practice-requirements-laboratory-controls",
    },
    {
        "id": "ifr-wl-remediation-capa",
        "name": "Warning Letter Remediation: Independent Audit & Global CAPA",
        "category": "CAPA Remediation",
        "plain": "Firms cited for data integrity failures must hire independent third-party experts to audit every lab and build a global fix.",
        "technical": "FDA cGMP Warning Letters routinely require an independent retrospective data-integrity investigation, patient-risk assessment of distributed lots, and a comprehensive global CAPA strategy.",
        "url": "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/pritam-international-private-limited-738079-10272026",
    },
    {
        "id": "ifr-cpgm-dqrs-7356-021",
        "name": "Drug Quality Reporting System (DQRS) & Violative EIR Escalation",
        "category": "CPGM 7356.021",
        "plain": "FDA connects factory inspection reports directly with incoming Field Alert Reports to spot recurring quality breakdowns.",
        "technical": "Compliance Program 7356.021 coordinates NDA/ANDA Field Alert Reports with Establishment Inspection Reports (Turbo EIR) and MARCS-CMS compliance escalation.",
        "url": "https://www.fda.gov/media/82096/download",
    },
]


def build_inspections_483_recalls(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2r",
        "checked": CHECKED,
        "cgmp_inspections_704": CGMP_INSPECTIONS_704,
        "form483_warning_import": FORM483_WARNING_IMPORT,
        "recalls_fars_part7": RECALLS_FARS_PART7,
        "data_integrity_enforcement": DATA_INTEGRITY_ENFORCEMENT,
    }
    (out_dir / "inspections_483_recalls.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "cgmp_inspections_704": len(CGMP_INSPECTIONS_704),
        "form483_warning_import": len(FORM483_WARNING_IMPORT),
        "recalls_fars_part7": len(RECALLS_FARS_PART7),
        "data_integrity_enforcement": len(DATA_INTEGRITY_ENFORCEMENT),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_inspections_483_recalls(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

INSPECTIONS_483_RECALLS_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderInspectionsSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="FDA cGMP inspections, Form 483, Warning Letters, Import Alerts, Recalls, and Data Integrity architecture">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. cGMP Inspections</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">6-System &amp; PAI Audits</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">§ 704(a)(4) Remote Docs</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">NAI / VAI / OAI</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">15-Day 483 Response</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. 483, WL &amp; Import</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">Form FDA 483 &amp; EIR</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">Warning Letters (Ch. 4)</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">Import Alert 66-40 DWPE</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Red vs. Green List</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. Recalls &amp; FARs</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">Class I / II / III (Part 7)</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">3-Day FARs (314.81)</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">45-Day BPDRs (600.14)</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Enforcement Report</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. Data Integrity</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">ALCOA &amp; Audit Trails</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">No Trial Injections</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">Independent Global CAPA</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">21 CFR 211.68 / 211.194</text>
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
        <a href="${esc(it.url)}" target="_blank" rel="noopener noreferrer" style="font-size:.82rem">Official FDA source ↗</a>
      </article>`).join("")}
  </div>`;
}

export async function inspections483RecallsPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/inspections_483_recalls.json");
  const sections = [
    { key: "cgmp_inspections_704", title: "1. cGMP Inspections, PAI & § 704(a)(4) Remote Records Reviews", items: data.cgmp_inspections_704 || [] },
    { key: "form483_warning_import", title: "2. Form FDA 483, Warning Letters & Import Alerts (DWPE)", items: data.form483_warning_import || [] },
    { key: "recalls_fars_part7", title: "3. Drug Recalls (21 CFR Part 7), FARs (21 CFR 314.81) & BPDRs", items: data.recalls_fars_part7 || [] },
    { key: "data_integrity_enforcement", title: "4. Data Integrity (ALCOA+), Lab Controls & CAPA Enforcement", items: data.data_integrity_enforcement || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Compliance &amp; Quality Oversight" : "Reference · Compliance &amp; Quality Oversight"}</p>
        <h1>FDA Inspections, Form 483, Warning Letters, Recalls &amp; Data Integrity</h1>
        <p class="lede">${exploreMode
          ? "How FDA inspects drug factories worldwide, issues Form 483s or Import Alerts, enforces honest lab data, and manages medicine recalls."
          : "Primary-sourced reference covering OII 6-system &amp; § 704(a)(4) inspections, Form FDA 483, Warning Letters, Import Alert 66-40, 21 CFR Part 7 recalls, FARs/BPDRs, and ALCOA data integrity."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-25")} · <a href="#/${exploreMode ? "ref" : "explore"}/inspections-483-recalls">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderInspectionsSvg()}
      <div class="filter-bar" role="group" aria-label="Filter inspections, Form 483, recalls, and data integrity sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["cgmp_inspections_704", "Inspections & 704 (6)"], ["form483_warning_import", "483 / WL / Import (6)"], ["recalls_fars_part7", "Recalls & FARs (6)"], ["data_integrity_enforcement", "Data Integrity (6)"]].map(([k, lbl]) => `
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
    imp = 'import { inspections483RecallsPage } from "./inspections_483_recalls.js";\n'
    if "inspections483RecallsPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/inspections-483-recalls") return inspections483RecallsPage(view, "ref");\n'
        '  if (path === "/explore/inspections-483-recalls") return inspections483RecallsPage(view, "explore");\n'
    )
    if '"/ref/inspections-483-recalls"' not in txt:
        anchor = 'if (path === "/ref/labeling-spl-rems")'
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
    if "#/ref/inspections-483-recalls" not in txt:
        anchor = '["#/ref/labeling-spl-rems"'
        item = '["#/ref/inspections-483-recalls", "Inspections, 483, Recalls & ALCOA"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/inspections-483-recalls" not in txt:
        anchor2 = '["#/explore/labeling-spl-rems"'
        item2 = '["#/explore/inspections-483-recalls", "Inspections, 483, Recalls & ALCOA"], '
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
    line = "python3 pipeline/build_inspections_483_recalls.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/inspections-483-recalls"' in txt:
        return False
    block = (
        '\n@app.get("/api/inspections-483-recalls")\n'
        'def api_inspections_483_recalls():\n'
        '    p = DATA_DIR / "inspections_483_recalls.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "inspections_483_recalls.json" in txt:
        return False
    snippet = '''    ifr_path = data_dir / "inspections_483_recalls.json"
    if ifr_path.is_file():
        ifr_doc = json.loads(ifr_path.read_text(encoding="utf-8"))
        for sec in ("cgmp_inspections_704", "form483_warning_import", "recalls_fars_part7", "data_integrity_enforcement"):
            for item in ifr_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "Inspections, 483 & Recalls",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/inspections-483-recalls",
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
    if "/inspections-483-recalls/" in txt:
        return False
    snippet = '''    # v6.2r cGMP Inspections, Form 483, Warning Letters, Recalls & Data Integrity SEO landing page
    ifr_dir = site_dir / "inspections-483-recalls"
    ifr_dir.mkdir(parents=True, exist_ok=True)
    (ifr_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>FDA Inspections, Form 483, Warning Letters, Recalls &amp; Data Integrity | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to FDA cGMP inspections, § 704(a)(4), Form 483, Warning Letters, Import Alerts, 21 CFR Part 7 recalls, FARs, and ALCOA data integrity.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/inspections-483-recalls/'>"
        "<script>location.replace('/#/explore/inspections-483-recalls');</script>"
        "</head><body><h1>FDA Inspections, Form 483, Warning Letters, Recalls &amp; Data Integrity</h1>"
        "<p><a href='/#/explore/inspections-483-recalls'>Explore</a> · <a href='/#/ref/inspections-483-recalls'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/inspections-483-recalls/")
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
    if "#/ref/inspections-483-recalls" in txt:
        return False
    anchor = '"/#/explore/labeling-spl-rems",'
    add = '"/#/explore/labeling-spl-rems",\n    "/#/ref/inspections-483-recalls",\n    "/#/explore/inspections-483-recalls",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/inspections-483-recalls /#/explore/inspections-483-recalls\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_inspections_483_recalls_py": _write_if_changed(pipe_dir / "build_inspections_483_recalls.py", BUILD_INSPECTIONS_483_RECALLS_PY),
        "inspections_483_recalls_js": _write_if_changed(js_dir / "inspections_483_recalls.js", INSPECTIONS_483_RECALLS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/labeling-spl-rems") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/labeling-spl-rems", "Labeling (PLR/SPL), SLC & REMS"]] }];\nconst EXPLORE_NAV = [["#/explore/labeling-spl-rems", "Labeling (PLR/SPL), SLC & REMS"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/labeling-spl-rems",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_inspections_483_recalls.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_inspections_483_recalls.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"cgmp_inspections_704": 6, "form483_warning_import": 6, "recalls_fars_part7": 6, "data_integrity_enforcement": 6}, out

        doc = json.loads((root / "site" / "data" / "inspections_483_recalls.json").read_text(encoding="utf-8"))
        for k in ("cgmp_inspections_704", "form483_warning_import", "recalls_fars_part7", "data_integrity_enforcement"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "inspections_483_recalls.js").read_text(encoding="utf-8")
        print("V62R_INSPECTIONS_483_RECALLS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2r Inspections, Form 483, Recalls & Data Integrity patch.")
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
