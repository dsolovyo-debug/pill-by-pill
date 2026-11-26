#!/usr/bin/env python3
"""Pill by Pill v6.2u Patch: FDA User Fee Programs (PDUFA VII/VIII, BsUFA III, GDUFA III, OMUFA), Priority Review Vouchers (Rare Pediatric, Tropical Disease, Material Threat MCM), and Expedited Programs for Serious Conditions Reference (#/ref/user-fees-prv, #/explore/user-fees-prv, /api/user-fees-prv).

1. Adds `pipeline/build_user_fees_prv.py` -> `site/data/user_fees_prv.json`
   (6 PDUFA/BsUFA pillars, 6 GDUFA/OMUFA pillars, 6 Priority Review Voucher pillars, and 6
   Expedited Programs pillars — 24 primary-sourced entries).
2. Adds `site/js/user_fees_prv.js` (`userFeesPrvPage` with inline User Fees, PRVs &
   Expedited Programs SVG + 4 section filters) and wires `#/ref/user-fees-prv`,
   `#/explore/user-fees-prv`, `/api/user-fees-prv`, `REF_NAV_GROUPS`, `EXPLORE_NAV`, and
   `pipeline/run_all.sh`.
3. Integrates `user_fees_prv.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/user-fees-prv/` static SEO page + sitemap entry ->
   63 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-26_v6.2u_user_fees_pdufa_gdufa_bsufa_omufa_prv_expedited_patch.py --selftest
  python3 2026-11-26_v6.2u_user_fees_pdufa_gdufa_bsufa_omufa_prv_expedited_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_USER_FEES_PRV_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2u FDA User Fees, PRVs & Expedited Programs Reference (`site/data/user_fees_prv.json`).

Comprehensive, primary-sourced reference covering:
  1. PDUFA VII / VIII & BsUFA III Review Clocks & Fees (6 pillars)
  2. GDUFA III (Generics) & OMUFA (OTC Monographs) User Fees (6 pillars)
  3. Priority Review Vouchers (PRVs): Rare Pediatric, Tropical & MCM (6 pillars)
  4. FDA Expedited Programs for Serious Conditions (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA).

Usage:
  python3 pipeline/build_user_fees_prv.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-26"

PDUFA_BSUFA_FEES = [
    {
        "id": "ufp-pdufa-vii-hub",
        "name": "Prescription Drug User Fee Amendments (PDUFA VII, FY 2023–2027)",
        "category": "PDUFA VII",
        "plain": "Drug companies pay dedicated user fees so FDA can hire expert reviewers and hit predictable target dates for new medicine decisions.",
        "technical": "Enacted under the FDA User Fee Reauthorization Act of 2022, PDUFA VII authorizes FY 2023–2027 user fees supporting NDA and BLA review clocks, MIDD, CID, and Sentinel.",
        "url": "https://www.fda.gov/industry/fda-user-fee-programs/prescription-drug-user-fee-amendments",
    },
    {
        "id": "ufp-pdufa-financial-plan",
        "name": "PDUFA VII Five-Year Financial Plan: Application & Program Fees",
        "category": "Fee Structure",
        "plain": "PDUFA relies on two main charges: a one-time application fee when filing a new drug, and an annual program fee per marketed product.",
        "technical": "FDA's PDUFA VII Financial Plan maintains the two-tier fee structure (application fees and annual program fees) alongside non-user-fee appropriations to fund human drug review.",
        "url": "https://www.fda.gov/media/191661/download",
    },
    {
        "id": "ufp-pdufa-clocks",
        "name": "PDUFA VII Commitment Letter: 10-Month Standard vs. 6-Month Priority",
        "category": "Review Clocks",
        "plain": "Standard new-drug reviews target 10 months from filing, while Priority Review cuts the clock to 6 months for major medical advances.",
        "technical": "Under the PDUFA VII Commitment Letter (The Program), FDA targets 90% on-time action within 10 months of the 60-day filing date (Standard) or 6 months (Priority), including allergenic extracts.",
        "url": "https://www.fda.gov/media/151712/download",
    },
    {
        "id": "ufp-pdufa-viii-2028",
        "name": "PDUFA VIII Reauthorization (FY 2028–2032)",
        "category": "PDUFA VIII",
        "plain": "Every five years Congress and FDA negotiate updated review goals and staffing plans—with PDUFA VIII covering 2028 through 2032.",
        "technical": "Because PDUFA VII authority expires September 30, 2027, FDA's PDUFA VIII portal tracks public negotiations and proposed commitments for Fiscal Years 2028–2032.",
        "url": "https://www.fda.gov/industry/prescription-drug-user-fee-amendments/pdufa-viii-fiscal-years-2028-2032",
    },
    {
        "id": "ufp-bsufa-iii-hub",
        "name": "Biosimilar User Fee Amendments (BsUFA III)",
        "category": "BsUFA III",
        "plain": "Biosimilar developers pay tailored BsUFA fees to fund dedicated biologic review teams and early development meetings.",
        "technical": "Authorized under the FD&C Act for FY 2023–2027, BsUFA III funds FDA scientific coordination, BPD initial/type meetings, and 351(k) biosimilar/interchangeable BLA reviews.",
        "url": "https://www.fda.gov/industry/fda-user-fee-programs/biosimilar-user-fee-amendments",
    },
    {
        "id": "ufp-bsufa-iii-goals",
        "name": "BsUFA III Commitment Letter: 10-Mo Original & 3-Mo Supplements",
        "category": "BsUFA Clocks",
        "plain": "FDA aims to decide 90% of original biosimilar applications within 10 months of filing and resubmissions within 6 months.",
        "technical": "The BsUFA III Commitment Letter sets 90% review-and-act goals of 10 months (original BLAs from 60-day filing), 6 months (resubmissions), and 3 months for qualifying supplements.",
        "url": "https://www.fda.gov/media/152279/download",
    },
]

GDUFA_OMUFA_FEES = [
    {
        "id": "ufp-gdufa-iii-facility",
        "name": "GDUFA III Generic Facility Fees, CMO 24% Rate & Foreign Differential",
        "category": "GDUFA III",
        "plain": "Generic factories pay annual fees due October 1—with contract manufacturers paying 24% of full finished-dose fees and foreign sites paying $15,000 extra.",
        "technical": "Under GDUFA III, facilities referenced in approved ANDAs pay annual fees; Contract Manufacturing Organizations (CMOs) owe 24% of the FDF fee, and foreign facilities incur a $15,000 inspection differential.",
        "url": "https://www.fda.gov/industry/fda-user-fee-programs/generic-drug-user-fee-amendments",
    },
    {
        "id": "ufp-gdufa-iii-assessing",
        "name": "Assessing User Fees Under GDUFA III (API, FDF & Program Tiers)",
        "category": "GDUFA Fee Tiers",
        "plain": "Generic drug companies pay application, facility, Drug Master File, and tiered program fees based on how many approved generics they hold.",
        "technical": "FDA's GDUFA III fee guidance explains ANDA filing fees, Type II API DMF fees, API/FDF facility fees, and Small/Medium/Large Generic Drug Applicant Program Fees.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessing-user-fees-under-generic-drug-user-fee-amendments-2022",
    },
    {
        "id": "ufp-gdufa-iii-anda-goals",
        "name": "GDUFA III ANDA Assessment Program Performance Goals",
        "category": "ANDA Clocks",
        "plain": "GDUFA III funds faster first-cycle generic approvals and pre-ANDA scientific meetings for complex inhalers, creams, and injectables.",
        "technical": "FDA's GDUFA III ANDA Assessment Program establishes 10-month standard (8-month priority) ANDA review goals, Pre-ANDA meetings, and enhanced communication to reduce multi-cycle delays.",
        "url": "https://www.fda.gov/industry/generic-drug-user-fee-amendments/anda-assessment-program-gdufa-iii-performance-goals-and-program-enhancements",
    },
    {
        "id": "ufp-omufa-program",
        "name": "Over-the-Counter Monograph Drug User Fee Program (OMUFA)",
        "category": "OMUFA",
        "plain": "Makers of over-the-counter monograph drugs pay annual facility and monograph-request fees to modernize nonprescription drug rules.",
        "technical": "Created alongside CARES Act § 505G OTC monograph reform, OMUFA funds FDA's OTC monograph administrative orders, safety actions, and OMOR reviews via facility and OMOR fees.",
        "url": "https://www.fda.gov/industry/fda-user-fee-programs/over-counter-monograph-drug-user-fee-program-omufa",
    },
    {
        "id": "ufp-omufa-assessing",
        "name": "Assessing OMUFA Fees: Facility Types, Due Dates & Exceptions",
        "category": "OMUFA Guidance",
        "plain": "Small contract packagers and hand-sanitizer-only facilities have specific fee exceptions under OMUFA rules.",
        "technical": "FDA's OMUFA fee guidance details Monograph Drug Facility (MDF) versus Contract Manufacturing Organization (CMO) facility fees, Tier 1/Tier 2 OMOR fees, due dates, and exemptions.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessing-user-fees-under-over-counter-monograph-drug-user-fee-program",
    },
    {
        "id": "ufp-omufa-2026-2030",
        "name": "OMUFA Reauthorization: Fiscal Years 2026–2030",
        "category": "OMUFA II",
        "plain": "Congress reauthorized OMUFA for 2026 through 2030 to keep over-the-counter monograph reviews funded and predictable.",
        "technical": "The second authorization of OMUFA (FY 2026–2030) extends FDA's OTC monograph user fee authority, facility registration, and administrative order performance goals.",
        "url": "https://www.fda.gov/industry/fda-user-fee-programs/omufa-reauthorization-fiscal-years-2026-2030",
    },
]

PRIORITY_REVIEW_VOUCHERS = [
    {
        "id": "ufp-rpd-prv-2029",
        "name": "Rare Pediatric Disease PRV Program & Sept 30, 2029 Sunset",
        "category": "FD&C § 529",
        "plain": "Winning approval for a rare children's disease drug earns a transferable voucher that speeds up FDA review of any future drug—extended through 2029.",
        "technical": "Under FD&C Act § 529 (extended by the Consolidated Appropriations Act, 2026), sponsors of approved rare pediatric disease NDAs/BLAs can earn a transferable PRV through September 30, 2029.",
        "url": "https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs",
    },
    {
        "id": "ufp-rpd-prv-transfer",
        "name": "Rare Pediatric Disease PRV Transfers & Redemption",
        "category": "PRV Transferability",
        "plain": "Smaller biotech companies frequently sell their Priority Review Vouchers to larger pharma companies to fund new research.",
        "technical": "FDA's Rare Pediatric Disease PRV guidance outlines designation criteria, voucher transfer notifications, and redemption procedures granting 6-month priority review on a subsequent NDA/BLA.",
        "url": "https://www.fda.gov/media/90014/download",
    },
    {
        "id": "ufp-cber-rpd-prv",
        "name": "CBER Rare Disease Program & Biologic/Gene Therapy PRVs",
        "category": "CBER RPD PRVs",
        "plain": "Gene therapies, vaccines, and blood biologics for rare childhood conditions are eligible for Priority Review Vouchers through CBER.",
        "technical": "CBER's Rare Disease Program coordinates § 529 Rare Pediatric Disease PRV eligibility for biological products, working alongside OOPD orphan designations.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/cber-rare-disease-program-frequently-asked-questions",
    },
    {
        "id": "ufp-tropical-prv-524",
        "name": "Tropical Disease PRV Program (FD&C Act § 524)",
        "category": "FD&C § 524",
        "plain": "Approving a new medicine for neglected tropical diseases like malaria, tuberculosis, or Chagas disease awards a Priority Review Voucher.",
        "technical": "FD&C Act § 524 awards transferable PRVs for drugs preventing or treating listed tropical diseases, with an open FDA public docket (FDA-2008-N-0567) to add qualifying diseases.",
        "url": "https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/tropical-disease-priority-review-voucher-program",
    },
    {
        "id": "ufp-tropical-prv-vs-oopd",
        "name": "Tropical Disease PRV Eligibility vs. OOPD Orphan Status",
        "category": "§ 524 vs. Orphan",
        "plain": "Tropical disease vouchers are decided by CDER or CBER—separately from whether a drug qualifies as a US rare orphan disease.",
        "technical": "FDA's Tropical Disease PRV guidance distinguishes OOPD orphan designation (<200,000 US patients) from CDER/CBER's statutory § 524 tropical disease voucher determination.",
        "url": "https://www.fda.gov/media/72569/download",
    },
    {
        "id": "ufp-mcm-prv-cures",
        "name": "Material Threat Medical Countermeasure (MCM) PRVs",
        "category": "FD&C § 565F",
        "plain": "Developing medical countermeasures against chemical, biological, radiological, or nuclear threats can earn a Material Threat PRV.",
        "technical": "Added by the 21st Century Cures Act, Material Threat MCM PRVs incentivize preparedness products and require an annual Federal Register priority review user fee upon redemption.",
        "url": "https://www.fda.gov/emergency-preparedness-and-response/mcm-legal-regulatory-and-policy-framework/21st-century-cures-act-mcm-related-cures-provisions",
    },
]

EXPEDITED_PROGRAMS_REVIEW = [
    {
        "id": "ufp-expedited-serious-2014",
        "name": "Expedited Programs for Serious Conditions — Drugs & Biologics",
        "category": "Expedited Hub",
        "plain": "FDA offers four core fast-lane programs to get breakthrough treatments for serious diseases to patients sooner.",
        "technical": "FDA's flagship Expedited Programs guidance defines qualifying criteria, timing, and features for Fast Track, Breakthrough Therapy, Accelerated Approval, and Priority Review.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/expedited-programs-serious-conditions-drugs-and-biologics",
    },
    {
        "id": "ufp-expedited-comparison",
        "name": "Comparing Fast Track, Breakthrough, Accelerated & Priority Review",
        "category": "4-Program Matrix",
        "plain": "A drug can qualify for more than one expedited program—combining rolling review, senior FDA coaching, and a 6-month review clock.",
        "technical": "FDA's comparison matrix contrasts nonclinical/clinical evidence thresholds, rolling-submission eligibility, intensive guidance (Breakthrough), surrogate endpoints (Accelerated), and 6-month Priority clocks.",
        "url": "https://www.fda.gov/media/86377/download",
    },
    {
        "id": "ufp-fast-track-rolling",
        "name": "Fast Track Designation & Rolling NDA/BLA Review",
        "category": "Fast Track",
        "plain": "Fast Track lets companies submit completed sections of a drug application to FDA one piece at a time instead of waiting for the entire file.",
        "technical": "Fast Track designation (based on nonclinical or clinical potential to address unmet medical need) unlocks frequent FDA interactions and rolling review of completed eCTD sections.",
        "url": "https://www.fda.gov/drugs/ind-activity/fast-track-designation-requests",
    },
    {
        "id": "ufp-accelerated-approval-draft",
        "name": "Accelerated Approval of Drugs & Biologics (Surrogate Endpoints)",
        "category": "21 CFR 314.510 / 601.41",
        "plain": "Accelerated Approval lets promising drugs reach patients based on an early lab or scan marker while confirmatory trials verify full benefit.",
        "technical": "FDA's Accelerated Approval guidance outlines reasonably likely surrogate or intermediate clinical endpoints, FDORA confirmatory-trial-underway expectations, and expedited withdrawal procedures.",
        "url": "https://www.fda.gov/media/184120/download",
    },
    {
        "id": "ufp-rmat-expedited-cber",
        "name": "Expedited Programs for Regenerative Medicine Therapies (RMAT)",
        "category": "RMAT / CBER",
        "plain": "Cell and gene therapies that show early clinical promise for serious conditions can earn RMAT status with Breakthrough-like FDA support.",
        "technical": "FDA's RMAT guidance integrates 21st Century Cures § 3033 regenerative-medicine provisions with Fast Track, Breakthrough, Priority Review, and Accelerated Approval mechanisms.",
        "url": "https://www.fda.gov/media/188874/download",
    },
    {
        "id": "ufp-rare-disease-expedited",
        "name": "Rare Disease Drug Development & Expedited Pathways",
        "category": "Rare Disease",
        "plain": "Rare-disease developers frequently combine Orphan designation with Fast Track, Breakthrough, or Accelerated Approval.",
        "technical": "FDA's Rare Disease Drug Development guidance suite connects natural-history and clinical-trial flexibility with expedited review pathways for small-population serious conditions.",
        "url": "https://www.fda.gov/drugs/guidances-drugs/guidance-documents-rare-disease-drug-development",
    },
]


def build_user_fees_prv(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2u",
        "checked": CHECKED,
        "pdufa_bsufa_fees": PDUFA_BSUFA_FEES,
        "gdufa_omufa_fees": GDUFA_OMUFA_FEES,
        "priority_review_vouchers": PRIORITY_REVIEW_VOUCHERS,
        "expedited_programs_review": EXPEDITED_PROGRAMS_REVIEW,
    }
    (out_dir / "user_fees_prv.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "pdufa_bsufa_fees": len(PDUFA_BSUFA_FEES),
        "gdufa_omufa_fees": len(GDUFA_OMUFA_FEES),
        "priority_review_vouchers": len(PRIORITY_REVIEW_VOUCHERS),
        "expedited_programs_review": len(EXPEDITED_PROGRAMS_REVIEW),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_user_fees_prv(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

USER_FEES_PRV_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderUserFeesSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="FDA User Fees PDUFA, BsUFA, GDUFA, OMUFA, Priority Review Vouchers, and Expedited Programs">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. PDUFA &amp; BsUFA</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">10-Mo Standard / 6-Mo Pri</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">Application &amp; Program Fees</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">BsUFA III Biosimilars</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">PDUFA VIII (2028–32)</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. GDUFA &amp; OMUFA</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">GDUFA III Facility &amp; ANDA</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">CMO 24% &amp; $15k Foreign</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">OMUFA OTC Monographs</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">OMUFA II (2026–30)</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. Priority Vouchers</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">Rare Pediatric (to 2029)</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">Tropical Disease (§ 524)</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">Material Threat MCM</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Transferable 6-Mo Clock</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. Expedited Review</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">Fast Track &amp; Rolling</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">Breakthrough &amp; RMAT</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">Accelerated Approval</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Serious Conditions</text>
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

export async function userFeesPrvPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/user_fees_prv.json");
  const sections = [
    { key: "pdufa_bsufa_fees", title: "1. PDUFA VII / VIII & BsUFA III Review Clocks & Fees", items: data.pdufa_bsufa_fees || [] },
    { key: "gdufa_omufa_fees", title: "2. GDUFA III (Generics) & OMUFA (OTC Monographs) User Fees", items: data.gdufa_omufa_fees || [] },
    { key: "priority_review_vouchers", title: "3. Priority Review Vouchers (PRVs): Rare Pediatric, Tropical & MCM", items: data.priority_review_vouchers || [] },
    { key: "expedited_programs_review", title: "4. FDA Expedited Programs for Serious Conditions", items: data.expedited_programs_review || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Regulatory Economics &amp; Clocks" : "Reference · Regulatory Economics &amp; Clocks"}</p>
        <h1>FDA User Fees (PDUFA / GDUFA / BsUFA / OMUFA), PRVs &amp; Expedited Review</h1>
        <p class="lede">${exploreMode
          ? "How FDA user-fee programs fund predictable review timelines, how Priority Review Vouchers speed up drug reviews, and how expedited pathways work."
          : "Primary-sourced reference covering PDUFA VII/VIII, BsUFA III, GDUFA III, OMUFA (FY 2026–2030), Rare Pediatric/Tropical/MCM PRVs, and FDA Expedited Programs."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-26")} · <a href="#/${exploreMode ? "ref" : "explore"}/user-fees-prv">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderUserFeesSvg()}
      <div class="filter-bar" role="group" aria-label="Filter user fees, PRV, and expedited program sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["pdufa_bsufa_fees", "PDUFA & BsUFA (6)"], ["gdufa_omufa_fees", "GDUFA & OMUFA (6)"], ["priority_review_vouchers", "PRVs (6)"], ["expedited_programs_review", "Expedited (6)"]].map(([k, lbl]) => `
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
    imp = 'import { userFeesPrvPage } from "./user_fees_prv.js";\n'
    if "userFeesPrvPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/user-fees-prv") return userFeesPrvPage(view, "ref");\n'
        '  if (path === "/explore/user-fees-prv") return userFeesPrvPage(view, "explore");\n'
    )
    if '"/ref/user-fees-prv"' not in txt:
        anchor = 'if (path === "/ref/packaging-el-dscsa")'
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
    if "#/ref/user-fees-prv" not in txt:
        anchor = '["#/ref/packaging-el-dscsa"'
        item = '["#/ref/user-fees-prv", "User Fees, PRVs & Expedited"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/user-fees-prv" not in txt:
        anchor2 = '["#/explore/packaging-el-dscsa"'
        item2 = '["#/explore/user-fees-prv", "User Fees, PRVs & Expedited"], '
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
    line = "python3 pipeline/build_user_fees_prv.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/user-fees-prv"' in txt:
        return False
    block = (
        '\n@app.get("/api/user-fees-prv")\n'
        'def api_user_fees_prv():\n'
        '    p = DATA_DIR / "user_fees_prv.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "user_fees_prv.json" in txt:
        return False
    snippet = '''    ufp_path = data_dir / "user_fees_prv.json"
    if ufp_path.is_file():
        ufp_doc = json.loads(ufp_path.read_text(encoding="utf-8"))
        for sec in ("pdufa_bsufa_fees", "gdufa_omufa_fees", "priority_review_vouchers", "expedited_programs_review"):
            for item in ufp_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "User Fees, PRVs & Expedited",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/user-fees-prv",
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
    if "/user-fees-prv/" in txt:
        return False
    snippet = '''    # v6.2u FDA User Fees (PDUFA/GDUFA/BsUFA/OMUFA), PRVs & Expedited Programs SEO landing page
    ufp_dir = site_dir / "user-fees-prv"
    ufp_dir.mkdir(parents=True, exist_ok=True)
    (ufp_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>FDA User Fees (PDUFA/GDUFA/BsUFA/OMUFA), PRVs &amp; Expedited Programs | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to PDUFA VII/VIII, BsUFA III, GDUFA III, OMUFA, Priority Review Vouchers, and FDA Expedited Programs.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/user-fees-prv/'>"
        "<script>location.replace('/#/explore/user-fees-prv');</script>"
        "</head><body><h1>FDA User Fees, Priority Review Vouchers &amp; Expedited Programs</h1>"
        "<p><a href='/#/explore/user-fees-prv'>Explore</a> · <a href='/#/ref/user-fees-prv'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/user-fees-prv/")
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
    if "#/ref/user-fees-prv" in txt:
        return False
    anchor = '"/#/explore/packaging-el-dscsa",'
    add = '"/#/explore/packaging-el-dscsa",\n    "/#/ref/user-fees-prv",\n    "/#/explore/user-fees-prv",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/user-fees-prv /#/explore/user-fees-prv\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_user_fees_prv_py": _write_if_changed(pipe_dir / "build_user_fees_prv.py", BUILD_USER_FEES_PRV_PY),
        "user_fees_prv_js": _write_if_changed(js_dir / "user_fees_prv.js", USER_FEES_PRV_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/packaging-el-dscsa") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/packaging-el-dscsa", "Packaging, ICH Q3E & DSCSA"]] }];\nconst EXPLORE_NAV = [["#/explore/packaging-el-dscsa", "Packaging, ICH Q3E & DSCSA"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/packaging-el-dscsa",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_user_fees_prv.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_user_fees_prv.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"pdufa_bsufa_fees": 6, "gdufa_omufa_fees": 6, "priority_review_vouchers": 6, "expedited_programs_review": 6}, out

        doc = json.loads((root / "site" / "data" / "user_fees_prv.json").read_text(encoding="utf-8"))
        for k in ("pdufa_bsufa_fees", "gdufa_omufa_fees", "priority_review_vouchers", "expedited_programs_review"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "user_fees_prv.js").read_text(encoding="utf-8")
        print("V62U_USER_FEES_PRV_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2u User Fees, PRVs & Expedited Programs patch.")
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
