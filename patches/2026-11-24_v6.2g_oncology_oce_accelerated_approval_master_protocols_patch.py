#!/usr/bin/env python3
"""Pill by Pill v6.2g Patch: Oncology Drug Development, FDA OCE Initiatives (Orbis/Optimus/RTOR/Confirm), Accelerated Approval, Master Protocols & Tissue-Agnostic Therapies Reference (#/ref/oncology-oce, #/explore/oncology-oce, /api/oncology-oce).

1. Adds `pipeline/build_oncology_oce.py` -> `site/data/oncology_oce.json` (6 FDA OCE Expedited &
   Global Initiatives pillars, 6 Accelerated Approval & Project Confirm pillars, 6 Master Protocols
   & Tissue-Agnostic Therapies pillars, and 6 Cancer Endpoints & Pediatric Oncology pillars — 24
   primary-sourced entries).
2. Adds `site/js/oncology_oce.js` (`oncologyOcePage` with inline Oncology OCE & Master Protocols
   SVG + 4 section filters) and wires `#/ref/oncology-oce`, `#/explore/oncology-oce`,
   `/api/oncology-oce`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `oncology_oce.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/oncology-oce/` static SEO page + sitemap entry ->
   49 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2g_oncology_oce_accelerated_approval_master_protocols_patch.py --selftest
  python3 2026-11-24_v6.2g_oncology_oce_accelerated_approval_master_protocols_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_ONCOLOGY_OCE_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2g Oncology Drug Development, FDA OCE, Accelerated Approval & Master Protocols Reference (`site/data/oncology_oce.json`).

Comprehensive, primary-sourced reference covering:
  1. FDA OCE Expedited & Global Initiatives (Orbis, Optimus, RTOR, Renewal) (6 pillars)
  2. Accelerated Approval & Project Confirm (6 pillars)
  3. Master Protocols (Basket, Umbrella, Platform) & Tissue-Agnostic Therapies (6 pillars)
  4. Cancer Clinical Endpoints, Pediatric Oncology (FDARA) & Labeling (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA OCE, CDER, CBER).

Usage:
  python3 pipeline/build_oncology_oce.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

OCE_EXPEDITED_PROGRAMS = [
    {
        "id": "onc-project-optimus",
        "name": "FDA OCE Project Optimus (Oncology Dose Optimization)",
        "category": "Dose Paradigm Reform",
        "plain": "Instead of automatically pushing cancer drugs to the highest tolerable dose (MTD), Project Optimus requires finding the lowest dose that shrinks tumors with fewer toxic side effects.",
        "technical": "Launched by FDA's Oncology Center of Excellence (OCE) in 2021, Project Optimus replaces traditional Maximum Tolerated Dose (MTD) selection with randomized dose-finding comparing PK, PD, tolerability, and activity.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/project-optimus",
    },
    {
        "id": "onc-project-orbis",
        "name": "Project Orbis: Concurrent Global Oncology Reviews",
        "category": "International Collaboration",
        "plain": "Project Orbis lets the FDA and regulators in countries like the UK, Canada, and Australia review new cancer drugs at the exact same time.",
        "technical": "Initiated in May 2019 by FDA OCE, Project Orbis provides a framework for concurrent submission and collaborative review of high-impact oncology NDAs/BLAs with Australia, Brazil, Canada, Singapore, Switzerland, and the UK.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/project-orbis",
    },
    {
        "id": "onc-orbis-faq",
        "name": "Project Orbis + RTOR Concurrent Review Eligibility",
        "category": "Submission Mechanics",
        "plain": "Applicants can combine Project Orbis with FDA's Real-Time Oncology Review to speed up approvals across multiple countries simultaneously.",
        "technical": "Project Orbis FAQs detail partner country selection, synchronized Assessment Aid templates, and eligibility to pair Orbis international collaboration with FDA's RTOR program.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/project-orbis-frequently-asked-questions",
    },
    {
        "id": "onc-rtor",
        "name": "Real-Time Oncology Review (RTOR) Rolling Data Pilot",
        "category": "Expedited Review",
        "plain": "When a cancer trial shows clear early success, RTOR lets FDA reviewers examine the top-line data tables weeks before the full application is even assembled.",
        "technical": "OCE's Real-Time Oncology Review (RTOR) allows early pre-submission of top-line efficacy/safety datasets and tables after database lock so FDA can begin review before the complete NDA/BLA is filed.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/real-time-oncology-review",
    },
    {
        "id": "onc-rtor-guidance",
        "name": "RTOR Draft Guidance: Eligibility Criteria & Assessment Aid",
        "category": "Review Standards",
        "plain": "RTOR is reserved for cancer therapies with straightforward study endpoints and clear improvements over existing treatments.",
        "technical": "FDA's RTOR Guidance defines candidate criteria (likely substantial improvement over available therapy, easily interpreted endpoints, and standardized datasets) alongside the multidisciplinary Assessment Aid.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/real-time-oncology-review-rtor",
    },
    {
        "id": "onc-project-renewal",
        "name": "Project Renewal: Updating Legacy Oncology Drug Labels",
        "category": "Label Modernization",
        "plain": "Many older generic chemotherapies had outdated prescribing labels; Project Renewal partners with cancer experts to bring their labels up to modern medical standards.",
        "technical": "OCE's Project Renewal engages external oncology experts and early-career scientists to evaluate published literature and update prescribing information for decades-old off-patent oncology drugs.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/project-renewal-faq",
    },
]

ACCELERATED_APPROVAL_CONFIRM = [
    {
        "id": "onc-project-confirm",
        "name": "OCE Project Confirm (Accelerated Approval Transparency)",
        "category": "Post-Market Accountability",
        "plain": "Project Confirm is FDA's public scorecard showing which fast-tracked cancer drugs passed their follow-up confirmatory trials and which ones were withdrawn.",
        "technical": "FDA OCE's Project Confirm promotes transparency around oncology Accelerated Approvals by tracking ongoing confirmatory trials, regular-approval conversions, and indication withdrawals.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/project-confirm",
    },
    {
        "id": "onc-aa-confirmatory-underway",
        "name": "FDORA Mandate: Confirmatory Trial 'Underway' Prior to Approval",
        "category": "Statutory Reform",
        "plain": "To prevent fast-tracked drugs from lingering unverified for years, new rules generally require the follow-up confirmatory trial to already be enrolling before approval.",
        "technical": "Implementing FDORA amendments to FD&C Act § 506(c), FDA's Jan 2025 guidance defines criteria for determining whether a confirmatory trial is 'underway' prior to granting Accelerated Approval.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/accelerated-approval-and-considerations-determining-whether-confirmatory-trial-underway",
    },
    {
        "id": "onc-aa-program",
        "name": "Accelerated Approval Program (Surrogate Endpoints)",
        "category": "21 CFR 314.510 / 601.41",
        "plain": "Accelerated Approval lets seriously ill patients get promising cancer drugs years earlier based on tumor shrinkage, while the company proves longer survival afterward.",
        "technical": "Under FD&C Act § 506(c), FDA may grant Accelerated Approval based on a surrogate endpoint (e.g., ORR, pCR) reasonably likely to predict clinical benefit, subject to mandatory post-approval verification.",
        "url": "https://www.fda.gov/drugs/nda-and-bla-approvals/accelerated-approval-program",
    },
    {
        "id": "onc-aa-ongoing",
        "name": "Ongoing Cancer Accelerated Approvals Registry",
        "category": "Active Tracking",
        "plain": "FDA publishes a live table of every cancer indication currently under Accelerated Approval and the status of its required follow-up study.",
        "technical": "CDER/OCE's Ongoing Cancer Accelerated Approvals database tracks indication, approval date, surrogate endpoint, and post-marketing confirmatory trial milestones.",
        "url": "https://www.fda.gov/drugs/cancer-approvals/ongoing-cancer-accelerated-approvals",
    },
    {
        "id": "onc-aa-withdrawn",
        "name": "Withdrawn Cancer Accelerated Approvals & Expedited Withdrawal",
        "category": "Market Removal",
        "plain": "If a follow-up confirmatory trial fails to show real patient benefit, FDA can swiftly withdraw that accelerated cancer indication.",
        "technical": "FDA's Withdrawn Cancer Accelerated Approvals registry documents oncology indications voluntarily or administratively withdrawn under FD&C Act § 506(c)(3) when confirmatory trials fail or stall.",
        "url": "https://www.fda.gov/drugs/cancer-approvals/withdrawn-cancer-accelerated-approvals",
    },
    {
        "id": "onc-cancer-approvals-hub",
        "name": "FDA Oncology Approvals & Hematology Notifications Portal",
        "category": "Approval Feed",
        "plain": "FDA's central Cancer Approvals portal logs every new tumor drug, biomarker-matched therapy, and CAR-T approval with trial summaries.",
        "technical": "CDER/OCE's Cancer Approvals database publishes primary review summaries, efficacy results, dosing, and Project Orbis/RTOR/AA tags for every oncology approval.",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/cancer-approvals",
    },
]

MASTER_PROTOCOLS_AGNOSTIC = [
    {
        "id": "onc-master-protocols-2023",
        "name": "Master Protocols: Basket, Umbrella & Platform Trials (FDORA Guidance)",
        "category": "Trial Architecture",
        "plain": "Instead of running separate trials for every mutation or drug, master protocols share one hospital network and control arm to test multiple treatments faster.",
        "technical": "FDA's Revised Draft Guidance on Master Protocols defines basket trials (one drug across multiple tumor/subtype cohorts), umbrella trials (multiple drugs in one disease), and platform trials (perpetual multi-arm).",
        "url": "https://www.fda.gov/media/174976/download",
    },
    {
        "id": "onc-master-protocols-2018",
        "name": "Oncology Master Protocols: Expediting Drug & Biologic Development",
        "category": "Oncology Strategy",
        "plain": "Oncology master protocols let biomarker-screened patients enter the exact arm matching their tumor's DNA mutation under a single overarching protocol.",
        "technical": "FDA's Oncology Master Protocols guidance outlines biomarker-stratified substudy governance, shared control arms, independent Data Monitoring Committees (DMCs), and IND cross-referencing.",
        "url": "https://www.fda.gov/media/120721/download",
    },
    {
        "id": "onc-complex-innovative-designs",
        "name": "Complex Innovative Trial Designs (CID) & Bayesian Borrowing",
        "category": "Adaptive Statistics",
        "plain": "Bayesian statistical models allow oncology trials to borrow strength across related tumor cohorts or use external data to shrink placebo groups.",
        "technical": "FDA's CID Focus Area supports Bayesian hierarchical borrowing across basket cohorts, Sequential Multiple Assignment Randomized Trials (SMART), and simulation-calibrated operating characteristics.",
        "url": "https://www.fda.gov/science-research/focus-areas-regulatory-science-report/focus-area-complex-innovative-trial-design",
    },
    {
        "id": "onc-tissue-agnostic-guidance",
        "name": "Tissue-Agnostic Drug Development in Oncology (Biomarker-First)",
        "category": "Precision Oncology",
        "plain": "Instead of approving a drug only for lung or colon cancer, FDA can approve it for ANY solid tumor carrying a specific genetic driver like NTRK or MSI-H.",
        "technical": "FDA's Tissue Agnostic Drug Development Guidance outlines when molecularly targeted drugs (e.g., MSI-H/dMMR, NTRK fusion, TMB-H, BRAF V600E) can earn pan-tumor approval across histologies.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/tissue-agnostic-drug-development-oncology",
    },
    {
        "id": "onc-tissue-agnostic-pdf",
        "name": "Scientific Criteria for Pan-Tumor Histologic Extrapolation",
        "category": "Biomarker Biology",
        "plain": "To win a tumor-agnostic label, a drug must show consistent responses across enough different cancer types—and explain why any outlier tumor resists it.",
        "technical": "Tissue-agnostic approvals require strong mechanistic rationale, validated companion diagnostic (CDx) across tumor types, adequate representation of rare/common histologies, and heterogeneity assessment.",
        "url": "https://www.fda.gov/media/162346/download",
    },
    {
        "id": "onc-expedited-ind-modernize",
        "name": "Expedited IND Pilot & Modernized Clinical Trial Evidence",
        "category": "Early-Phase Speed",
        "plain": "FDA's newest clinical modernization tools allow rolling first-in-human IND reviews and single-pivotal-trial approvals backed by strong confirmatory biology.",
        "technical": "FDA's clinical modernization initiatives pair rolling Expedited IND submissions with Qualified Research Institutions (QRIs), New Approach Methodologies (NAMs), and single-trial + confirmatory-evidence standards.",
        "url": "https://www.fda.gov/industry/fda-actions-accelerate-and-modernize-early-and-late-stage-clinical-development",
    },
]

ONCOLOGY_ENDPOINTS_PEDS = [
    {
        "id": "onc-cancer-endpoints-2018",
        "name": "Clinical Trial Endpoints for Cancer Drugs & Biologics (OS, PFS, ORR)",
        "category": "Efficacy Endpoints",
        "plain": "Living longer (Overall Survival) is the gold standard in cancer trials, while progression-free survival (PFS) and tumor shrinkage (ORR) help measure benefit sooner.",
        "technical": "FDA's Cancer Endpoints Guidance compares Overall Survival (OS), Progression-Free Survival (PFS), Disease-Free Survival (DFS), and Objective Response Rate (ORR) via RECIST 1.1 and Blinded Independent Central Review (BICR).",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-trial-endpoints-approval-cancer-drugs-and-biologics",
    },
    {
        "id": "onc-endpoints-pdf",
        "name": "Blinded Independent Central Review (BICR) & Censoring Rules",
        "category": "Imaging Rigor",
        "plain": "Independent radiologists who don't know which treatment a patient received re-read tumor scans to prevent unconscious bias in progression-free survival results.",
        "technical": "FDA's Endpoints Guidance details BICR audit requirements, informative censoring sensitivity analyses, and symptom/PRO measures supporting regular vs. accelerated oncology approvals.",
        "url": "https://www.fda.gov/media/71195/download",
    },
    {
        "id": "onc-nsclc-endpoints",
        "name": "Site-Specific Oncology Endpoints (e.g., NSCLC, Hematologic MRD)",
        "category": "Disease-Specific",
        "plain": "Different cancers use tailored milestones—like pathologic complete response before surgery or undetectable leukemia cells (MRD) in blood cancers.",
        "technical": "Disease-specific FDA guidances (such as Non-Small Cell Lung Cancer Endpoints) establish context-of-use criteria for pathologic complete response (pCR), event-free survival (EFS), and minimal residual disease (MRD).",
        "url": "https://www.fda.gov/media/116860/download",
    },
    {
        "id": "onc-pediatric-fdara",
        "name": "FDARA § 505B(a)(3): Molecularly Targeted Pediatric Cancer Studies",
        "category": "Pediatric Oncology",
        "plain": "If an adult cancer drug hits a molecular target that also drives childhood cancers, the law requires testing it in kids—and teens 12+ can often join adult trials.",
        "technical": "Under FDARA (FD&C Act § 505B(a)(3)), adult oncology NDAs/BLAs directed at molecular targets relevant to pediatric cancers require molecularly targeted pediatric investigations and iPSPs, often enrolling adolescents ≥12 years.",
        "url": "https://www.fda.gov/media/178681/download",
    },
    {
        "id": "onc-renewal-temodar",
        "name": "Project Renewal Case Study: Temozolomide (Temodar) Label Update",
        "category": "Legacy Drug Evidence",
        "plain": "Through Project Renewal, FDA updated the brain-cancer drug temozolomide's decades-old label to reflect modern clinical guidelines.",
        "technical": "FDA's 2023 Project Renewal approval updated temozolomide indications and dosing schedules for newly diagnosed and refractory anaplastic astrocytoma using curated published clinical literature.",
        "url": "https://www.fda.gov/drugs/cancer-approvals/fda-approves-new-and-updated-indications-temozolomide-under-project-renewal",
    },
    {
        "id": "onc-renewal-fludarabine",
        "name": "Project Renewal Case Study: Fludarabine CLL Combination Labeling",
        "category": "Hematology Update",
        "plain": "Project Renewal also modernized fludarabine's leukemia label so doctors have accurate combination-regimen dosing instructions.",
        "technical": "FDA's 2024 Project Renewal update revised fludarabine phosphate injection labeling for adult B-cell chronic lymphocytic leukemia (CLL) combination and relapsed regimens.",
        "url": "https://www.fda.gov/drugs/cancer-approvals/fda-approves-updated-drug-labeling-fludarabine-phosphate-under-project-renewal",
    },
]


def build_oncology_oce(data_dir: pathlib.Path) -> dict:
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "counts": {
            "oce_expedited_programs": len(OCE_EXPEDITED_PROGRAMS),
            "accelerated_approval_confirm": len(ACCELERATED_APPROVAL_CONFIRM),
            "master_protocols_agnostic": len(MASTER_PROTOCOLS_AGNOSTIC),
            "oncology_endpoints_peds": len(ONCOLOGY_ENDPOINTS_PEDS),
        },
        "oce_expedited_programs": OCE_EXPEDITED_PROGRAMS,
        "accelerated_approval_confirm": ACCELERATED_APPROVAL_CONFIRM,
        "master_protocols_agnostic": MASTER_PROTOCOLS_AGNOSTIC,
        "oncology_endpoints_peds": ONCOLOGY_ENDPOINTS_PEDS,
    }
    (data_dir / "oncology_oce.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    return payload["counts"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 pipeline/build_oncology_oce.py <site/data>")
    print(json.dumps(build_oncology_oce(pathlib.Path(sys.argv[1])), indent=2))
'''

ONCOLOGY_OCE_JS = '''// Pill by Pill v6.2g: Oncology Drug Development, FDA OCE (Orbis/Optimus/RTOR/Confirm), Accelerated Approval & Master Protocols Reference
import { html } from "./ui.js";
import * as data from "./data.js";
import { page } from "./layout.js";

const EXP_HOME = ["Home", "#/explore"];
const REF_HOME = ["Overview", "#/ref"];

const SECTIONS = [
  ["all", "All sections", null],
  ["oce", "OCE: Orbis, Optimus & RTOR", "oce_expedited_programs"],
  ["confirm", "Accelerated Approval & Confirm", "accelerated_approval_confirm"],
  ["master", "Master Protocols & Agnostic", "master_protocols_agnostic"],
  ["endpoints", "Endpoints & Pediatric (FDARA)", "oncology_endpoints_peds"],
];

function oncologyOceSvg() {
  return html`<figure class="lifecycle-fig">
    <svg viewBox="0 0 720 130" width="720" height="130" role="img" aria-label="Oncology regulatory architecture: OCE Optimus and Orbis, Accelerated Approval and Project Confirm, Master Protocols and Tissue-Agnostic, and Cancer Endpoints">
      <rect x="8" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="88" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. FDA OCE Suite</text>
      <text x="88" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Optimus Dose &amp; RTOR</text>
      <text x="88" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Project Orbis Global</text>
      <path d="M170 61 L192 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#onc-arr)"/>
      <rect x="194" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="274" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Project Confirm</text>
      <text x="274" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Accelerated Approval</text>
      <text x="274" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">FDORA Confirmatory</text>
      <path d="M356 61 L378 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#onc-arr)"/>
      <rect x="380" y="20" width="160" height="82" rx="10" fill="var(--paper)" stroke="var(--line)"/>
      <text x="460" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Master Protocols</text>
      <text x="460" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Basket / Umbrella / Platform</text>
      <text x="460" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Tissue-Agnostic Pan-Tumor</text>
      <path d="M542 61 L564 61" stroke="var(--accent)" stroke-width="2" marker-end="url(#onc-arr)"/>
      <rect x="566" y="20" width="146" height="82" rx="10" fill="var(--paper)" stroke="var(--accent)"/>
      <text x="639" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Endpoints &amp; Kids</text>
      <text x="639" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">OS, PFS, ORR &amp; BICR</text>
      <text x="639" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">FDARA §505B &amp; Renewal</text>
      <defs><marker id="onc-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="var(--accent)"/></marker></defs>
    </svg>
    <figcaption class="muted small">Modern oncology regulation integrates Project Optimus dosing, global Orbis/RTOR reviews, FDORA-backed Accelerated Approval, master protocols, and validated cancer endpoints.</figcaption>
  </figure>`;
}

export async function oncologyOcePage(query = new URLSearchParams(), env = "ref") {
  const doc = await data.getJSON("data/oncology_oce.json");
  const activeSec = query.get("section") || "all";
  const baseHash = env === "explore" ? "#/explore/oncology-oce" : "#/ref/oncology-oce";

  const pills = html`<div class="chips" role="navigation" aria-label="Oncology OCE, accelerated approval, and master protocols sections">
    ${SECTIONS.map(([id, label]) => html`<a class="chip${activeSec === id ? " on" : ""}" href="${id === "all" ? baseHash : `${baseHash}?section=${id}`}">${label}</a>`)}
  </div>`;

  const renderGroup = (title, items) => html`
    <section class="x-panel">
      <h2>${title}</h2>
      <div class="tbl-wrap" tabindex="0" role="region" aria-label="${title}">
        <table class="tbl"><thead><tr><th>Initiative / Guidance</th><th>Category</th><th>${env === "explore" ? "Plain-Language Guide" : "Technical &amp; Regulatory Detail"}</th><th>Source</th></tr></thead>
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
    ${oncologyOceSvg()}
    ${pills}
    ${visible.map(([, label, key]) => renderGroup(label, doc[key] || []))}
    <p class="muted small">Verified ${doc.checked} against FDA Oncology Center of Excellence (Project Orbis, Optimus, RTOR, Confirm, Renewal), Master Protocols, Tissue-Agnostic, and Cancer Endpoints documentation.</p>`;

  return {
    html: page({
      trail: env === "explore" ? [EXP_HOME, ["Oncology OCE, Accelerated Approval & Master Protocols"]] : [REF_HOME, ["Oncology OCE, Accelerated Approval & Master Protocols"]],
      kicker: `${Object.values(doc.counts).reduce((a, b) => a + b, 0)} primary-sourced standards`,
      title: "Oncology OCE, Accelerated Approval, Master Protocols & Endpoints",
      lede: env === "explore"
        ? "How FDA optimizes cancer drug doses, fast-tracks promising tumor therapies worldwide, and runs basket trials targeting DNA mutations across cancer types."
        : "FDA OCE (Project Optimus, Orbis, RTOR, Confirm, Renewal), FDORA Accelerated Approval confirmatory rules, Basket/Umbrella/Platform master protocols, and OS/PFS/ORR endpoints.",
      body,
      more: [
        { title: env === "explore" ? "Technical Reference View" : "Simple Explorer View", text: "Switch perspective on oncology OCE initiatives, master protocols, and endpoints.", href: env === "explore" ? "#/ref/oncology-oce" : "#/explore/oncology-oce" },
        { title: "Companion Diagnostics & Biomarkers", text: "Co-developed NGS/IHC assays enabling tissue-agnostic oncology approvals.", href: "#/ref/cdx" },
        { title: "Clinical Trial Design & Endpoints", text: "Adaptive designs, estimands, and surrogate endpoint frameworks.", href: "#/ref/trials" },
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
    if 'oncology_oce.js' not in txt:
        for anchor in ('import * as excipientsDmfsNano from "./excipients_dmfs_nano.js";\n', 'import * as amrAntiinfectives from "./amr_antiinfectives.js";\n', 'import * as reference from "./reference.js";\n'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + 'import * as oncologyOce from "./oncology_oce.js";\n', 1)
                changed = True
                break
        else:
            txt = 'import * as oncologyOce from "./oncology_oce.js";\n' + txt
            changed = True
    if '"/ref/oncology-oce"' not in txt:
        for anchor in ('if (path === "/ref/excipients-dmfs-nano")', 'if (path === "/ref/amr-antiinfectives")', 'if (path === "/ref/trials")'):
            if anchor in txt:
                idx = txt.index(anchor)
                line_end = txt.find("\n", idx) + 1
                txt = txt[:line_end] + '  if (path === "/ref/oncology-oce") return { env: "ref", current: "#/ref/oncology-oce", ...(await oncologyOce.oncologyOcePage(query, "ref")) };\n  if (path === "/explore/oncology-oce") return { env: "explore", current: "#/explore/oncology-oce", ...(await oncologyOce.oncologyOcePage(query, "explore")) };\n' + txt[line_end:]
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
    if "#/ref/oncology-oce" not in txt:
        for anchor in ('["#/ref/excipients-dmfs-nano", "Excipients, DMFs & nano"]', '["#/ref/amr-antiinfectives", "AMR, phages & CARB-X"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/ref/oncology-oce", "Oncology OCE & master trials"]', 1)
                changed = True
                break
    if "#/explore/oncology-oce" not in txt:
        for anchor in ('["#/explore/excipients-dmfs-nano", "Excipients, DMFs & nano"]', '["#/explore/amr-antiinfectives", "AMR, phages & CARB-X"]'):
            if anchor in txt:
                txt = txt.replace(anchor, anchor + ', ["#/explore/oncology-oce", "Oncology OCE & master trials"]', 1)
                changed = True
                break
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_run_all(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "build_oncology_oce.py" in txt:
        return False
    line = "python3 pipeline/build_oncology_oce.py site/data\n"
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
    if '"/api/oncology-oce"' in txt:
        return False
    route = (
        '\n@app.get("/api/oncology-oce")\n'
        'def api_oncology_oce():\n'
        '    p = DATA_DIR / "oncology_oce.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"error": "oncology_oce.json not built"}\n'
    )
    path.write_text(txt + route, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"oncology_oce.json"' in txt:
        return False
    anchor = '    payload = {"checked": CHECKED,'
    if anchor not in txt:
        return False
    snippet = (
        '    onc_ref = _load(data_dir / "oncology_oce.json", {}) or {}\n'
        '    for sec_key, sec_q in [("oce_expedited_programs", "oce"), ("accelerated_approval_confirm", "confirm"), ("master_protocols_agnostic", "master"), ("oncology_endpoints_peds", "endpoints")]:\n'
        '        for item in (onc_ref.get(sec_key) or []):\n'
        '            entries.append({\n'
        '                "kind": "oncology_oce",\n'
        '                "group": "Oncology OCE, Accelerated Approval & Master Protocols",\n'
        '                "title": item.get("name", ""),\n'
        '                "summary": item.get("plain", ""),\n'
        '                "href_ref": f"#/ref/oncology-oce?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "href_explore": f"#/explore/oncology-oce?section={sec_q}#{item.get(\'id\', \'\')}",\n'
        '                "keywords": f"oncology OCE Project Optimus Orbis RTOR Confirm Renewal accelerated approval FDORA master protocol basket umbrella platform trial tissue agnostic OS PFS ORR BICR FDARA {sec_key} {item.get(\'name\', \'\')} {item.get(\'category\', \'\')} {item.get(\'plain\', \'\')} {item.get(\'technical\', \'\')}".strip(),\n'
        '            })\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_static_pages(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"oncology-oce", "#/ref/oncology-oce"' in txt:
        return False
    anchor = "    written_urls = []"
    if anchor not in txt:
        return False
    snippet = (
        '    onc_doc = _load_json(data_dir / "oncology_oce.json")\n'
        '    if isinstance(onc_doc, dict) and onc_doc.get("oce_expedited_programs"):\n'
        '        onc_lis = "".join(f\'<li><b>{_esc(x["name"])}</b> — {_esc(x.get("plain",""))}</li>\' for x in (onc_doc.get("oce_expedited_programs") or []) + (onc_doc.get("master_protocols_agnostic") or []))\n'
        '        pages.append(("oncology-oce", "#/ref/oncology-oce", "Oncology OCE, Accelerated Approval, Master Protocols & Endpoints",\n'
        '                      "Primary-sourced guide to FDA OCE (Optimus, Orbis, RTOR, Confirm, Renewal), Accelerated Approval, basket/umbrella/platform master protocols, and tissue-agnostic oncology.",\n'
        '                      f"<ul>{onc_lis}</ul>"))\n\n'
    )
    path.write_text(txt.replace(anchor, snippet + anchor, 1), encoding="utf-8")
    return True


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/oncology-oce"' in txt:
        return False
    for anchor in ('    "/#/explore/excipients-dmfs-nano",', '    "/#/explore/amr-antiinfectives",', '    "/#/explore/shortages-resilience",', '    "/#/ref/search",'):
        if anchor in txt:
            path.write_text(txt.replace(anchor, anchor + '\n    "/#/ref/oncology-oce",\n    "/#/explore/oncology-oce",', 1), encoding="utf-8")
            return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_oncology_oce_py": _write_if_changed(pipe_dir / "build_oncology_oce.py", BUILD_ONCOLOGY_OCE_PY),
        "oncology_oce_js": _write_if_changed(js_dir / "oncology_oce.js", ONCOLOGY_OCE_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/excipients-dmfs-nano") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/excipients-dmfs-nano", "Excipients, DMFs & nano"]] }];\nconst EXPLORE_NAV = [["#/explore/excipients-dmfs-nano", "Excipients, DMFs & nano"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/excipients-dmfs-nano",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_oncology_oce.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_oncology_oce.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"oce_expedited_programs": 6, "accelerated_approval_confirm": 6, "master_protocols_agnostic": 6, "oncology_endpoints_peds": 6}, out

        doc = json.loads((root / "site" / "data" / "oncology_oce.json").read_text(encoding="utf-8"))
        for k in ("oce_expedited_programs", "accelerated_approval_confirm", "master_protocols_agnostic", "oncology_endpoints_peds"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "oncology_oce.js").read_text(encoding="utf-8")
        print("V62G_ONCOLOGY_OCE_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2g Oncology OCE, Accelerated Approval & Master Protocols patch.")
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
