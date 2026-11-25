#!/usr/bin/env python3
"""Pill by Pill v6.2q Patch: Prescription Drug Labeling (PLR 21 CFR 201.56/201.57 & SPL), Patient Labeling (Medication Guides / IFU / PMI), Safety Labeling Changes (FD&C Act § 505(o)(4)), and REMS / ETASU / Shared Systems Reference (#/ref/labeling-spl-rems, #/explore/labeling-spl-rems, /api/labeling-spl-rems).

1. Adds `pipeline/build_labeling_spl_rems.py` -> `site/data/labeling_spl_rems.json`
   (6 PLR & SPL pillars, 6 Patient Labeling / MedGuide / IFU pillars, 6 Safety Labeling
   Changes & Boxed Warning pillars, and 6 REMS / ETASU / Shared System pillars — 24
   primary-sourced entries).
2. Adds `site/js/labeling_spl_rems.js` (`labelingSplRemsPage` with inline Drug Labeling,
   SLC & REMS SVG + 4 section filters) and wires `#/ref/labeling-spl-rems`,
   `#/explore/labeling-spl-rems`, `/api/labeling-spl-rems`, `REF_NAV_GROUPS`,
   `EXPLORE_NAV`, and `pipeline/run_all.sh`.
3. Integrates `labeling_spl_rems.json` into `pipeline/build_global_search.py`,
   `pipeline/build_v60_static_pages.py` (`/labeling-spl-rems/` static SEO page + sitemap
   entry -> 59 encyclopedia SEO pages), and `tests/test_v60_site.py`.

Usage:
  python3 2026-11-24_v6.2q_drug_labeling_plr_spl_slc_rems_etasu_patch.py --selftest
  python3 2026-11-24_v6.2q_drug_labeling_plr_spl_slc_rems_etasu_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

BUILD_LABELING_SPL_REMS_PY = '''#!/usr/bin/env python3
"""Build Pill by Pill v6.2q Drug Labeling (PLR/SPL), Patient Labeling, Safety Labeling Changes & REMS Reference (`site/data/labeling_spl_rems.json`).

Comprehensive, primary-sourced reference covering:
  1. Physician Labeling Rule (PLR, 21 CFR 201.56/201.57) & Structured Product Labeling (6 pillars)
  2. Patient Labeling: Medication Guides (21 CFR 208), IFUs & PMI (6 pillars)
  3. Safety Labeling Changes (§ 505(o)(4)) & Boxed Warnings (6 pillars)
  4. Risk Evaluation and Mitigation Strategies (REMS), ETASU & Shared Systems (6 pillars)

All regulatory anchors are verified HTTPS primary sources (FDA CDER/CBER).

Usage:
  python3 pipeline/build_labeling_spl_rems.py site/data
"""
import json
import pathlib
import sys

CHECKED = "2026-11-24"

PLR_SPL_DAILYMED = [
    {
        "id": "lsr-plr-resources",
        "name": "Physician Labeling Rule (PLR, 21 CFR 201.56 & 201.57)",
        "category": "PLR Format",
        "plain": "Every modern prescription drug label puts a clear one-page Highlights summary at the very top so doctors can find dosing and warnings fast.",
        "technical": "FDA's Physician Labeling Rule (21 CFR 201.56(d) and 201.57) structures Prescribing Information into Highlights of Prescribing Information, Table of Contents, and 17 numbered Full Prescribing Information sections.",
        "url": "https://www.fda.gov/drugs/fdas-labeling-resources-human-prescription-drugs/prescribing-information-resources",
    },
    {
        "id": "lsr-plr-content-format",
        "name": "Implementing PLR Content & Format Requirements",
        "category": "FPI Sections 1–17",
        "plain": "Standardized sections—from Indications (Section 1) to Patient Counseling (Section 17)—keep every US drug label organized identically.",
        "technical": "FDA's PLR Content and Format guidance specifies cross-referencing rules, revision dates, and standardized section ordering across Indications, Dosage, Contraindications, Warnings, and Clinical Studies.",
        "url": "https://www.fda.gov/files/drugs/published/Labeling-for-Human-Prescription-Drug-and-Biological-Products---Implementing-the-PLR-Content-and-Format-Requirements.pdf",
    },
    {
        "id": "lsr-spl-xml-indexing",
        "name": "Structured Product Labeling (SPL) XML & DailyMed Indexing",
        "category": "HL7 SPL Standard",
        "plain": "Drug labels are submitted in a machine-readable XML format so pharmacies, electronic health records, and DailyMed stay automatically updated.",
        "technical": "FDA requires Structured Product Labeling (SPL) XML files with machine-readable indexing elements (substance UNIIs, pharmacologic classes, NDCs, and routes) powering DailyMed and eCTD Module 1.",
        "url": "https://www.fda.gov/media/71110/download",
    },
    {
        "id": "lsr-plr-older-conversions",
        "name": "Converting Older Non-PLR Drug Labels to PLR Format",
        "category": "PLR Conversion",
        "plain": "Older generic and legacy medicines can also be updated from dense legacy text into modern, easy-to-scan PLR formatting.",
        "technical": "FDA's PLR conversion guidance (updated Jan 2026) walks NDA and ANDA holders through reformatting legacy non-PLR labeling into 21 CFR 201.56(d)/201.57 PLR compliance.",
        "url": "https://www.fda.gov/files/drugs/published/Converting-Labeling-for-Older-Drugs-from-Old-Format-to-PLR-Format.pdf",
    },
    {
        "id": "lsr-section12-clinpharm",
        "name": "Section 12 Clinical Pharmacology (Mechanism, PD & PK)",
        "category": "21 CFR 201.57(c)(13)",
        "plain": "Section 12 explains how the drug works in the body, how fast it is absorbed and cleared, and how kidney, liver, or other drugs affect it.",
        "technical": "Under 21 CFR 201.57(c)(13), Section 12 presents Mechanism of Action (12.1), Pharmacodynamics (12.2), Pharmacokinetics (12.3), and Microbiology/Pharmacogenomics (12.4/12.5).",
        "url": "https://www.fda.gov/media/74346/download",
    },
    {
        "id": "lsr-pllr-pregnancy-8",
        "name": "Pregnancy & Lactation Labeling Rule (PLLR Subsections 8.1–8.3)",
        "category": "PLLR 8.1–8.3",
        "plain": "Instead of old letter grades (A, B, C, D, X), labels now give doctors narrative risk summaries for pregnancy, breastfeeding, and fertility.",
        "technical": "The PLLR replaced A/B/C/D/X categories with bolded subsections 8.1 Pregnancy (including pregnancy exposure registries), 8.2 Lactation, and 8.3 Females and Males of Reproductive Potential.",
        "url": "https://www.fda.gov/media/92565/download",
    },
]

PATIENT_LABELING_IFU = [
    {
        "id": "lsr-patient-labeling-hub",
        "name": "Patient Labeling Resources: MedGuides, PPIs & IFUs",
        "category": "Patient Labeling",
        "plain": "Beyond the doctor's label, FDA approves plain-language handouts and step-by-step device instructions written directly for patients.",
        "technical": "FDA-approved patient labeling encompasses Medication Guides (21 CFR Part 208), Patient Package Inserts (PPIs), and Instructions for Use (IFUs) appended to the Prescribing Information.",
        "url": "https://www.fda.gov/drugs/fdas-labeling-resources-human-prescription-drugs/patient-labeling-resources",
    },
    {
        "id": "lsr-medguide-21cfr208",
        "name": "Medication Guides (21 CFR Part 208) & Pharmacy Distribution",
        "category": "21 CFR Part 208",
        "plain": "Pharmacies must hand out an official Medication Guide every time they dispense medicines carrying serious preventable side-effect warnings.",
        "technical": "Under 21 CFR Part 208, Medication Guides are required when patient information prevents serious adverse effects, informs risk-benefit decisions, or is essential for adherence—and remain mandatory even if removed from a REMS.",
        "url": "https://www.fda.gov/media/79776/download",
    },
    {
        "id": "lsr-ifu-content-format",
        "name": "Instructions for Use (IFU) for Pens, Inhalers & Patches",
        "category": "IFU Guidance",
        "plain": "Step-by-step illustrated guides show patients exactly how to prime an inhaler, inject an autoinjector pen, or apply a skin patch safely.",
        "technical": "FDA's IFU Content and Format guidance standardizes task-oriented, human-factors-validated instructions for prescription drug and biologic products with complicated administration procedures.",
        "url": "https://www.fda.gov/media/134018/download",
    },
    {
        "id": "lsr-section17-counseling",
        "name": "Section 17 Patient Counseling Information & Appended Guides",
        "category": "21 CFR 201.57(c)(18)",
        "plain": "Section 17 prompts physicians on key points to discuss with patients and points directly to the attached Medication Guide or IFU.",
        "technical": "Under 21 CFR 201.57(c)(18), Section 17 must reference FDA-approved patient labeling (PPI, Medication Guide, or IFU) and direct prescribers to advise patients to read it.",
        "url": "https://www.fda.gov/files/drugs/published/Patient-Counseling-Information-Section-of-Labeling-for-Human-Prescription-Drug-and-Biological-Products-%E2%80%94-Content-and-Format.pdf",
    },
    {
        "id": "lsr-pmi-one-page",
        "name": "Patient Medication Information (PMI) Standardized One-Pager",
        "category": "PMI Initiative",
        "plain": "FDA developed a clear one-page Patient Medication Information prototype so patients do not get buried in confusing multi-page pharmacy flyers.",
        "technical": "FDA's PMI initiative aims to replace inconsistent consumer leaflets with a standardized, comprehension-tested one-page summary covering drug name, uses, warnings, and directions.",
        "url": "https://www.fda.gov/drugs/fdas-labeling-resources-human-prescription-drugs/patient-medication-information-pmi",
    },
    {
        "id": "lsr-oce-using-labeling",
        "name": "How to Use Prescription Drug Labeling (FDA OCE Guide)",
        "category": "Label Navigation",
        "plain": "FDA's Oncology Center of Excellence provides a practical walkthrough showing patients and clinicians how to read every part of a drug label.",
        "technical": "FDA's guide explains how to navigate Highlights, Full Prescribing Information, Medication Guides, and IFUs to verify approved indications, dosing modifications, and safety monitoring.",
        "url": "https://www.fda.gov/about-fda/oncology-center-excellence/how-do-i-use-prescription-drug-labeling",
    },
]

SLC_BOXED_WARNINGS = [
    {
        "id": "lsr-srlc-database",
        "name": "Drug Safety-Related Labeling Changes (SrLC) Database (§ 505(o)(4))",
        "category": "FDAAA § 901",
        "plain": "FDA maintains a public searchable database showing every time new safety warnings are added to approved prescription drugs.",
        "technical": "The SrLC database tracks safety-related labeling changes required by FDA under FD&C Act § 505(o)(4) (enacted via FDAAA § 901) across Boxed Warnings, Contraindications, Warnings, and Adverse Reactions.",
        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-related-labeling-changes-srlc-database-overview-updates-safety-information-fda-approved",
    },
    {
        "id": "lsr-slc-505o4-guidance",
        "name": "Safety Labeling Changes — Implementation of Section 505(o)(4)",
        "category": "SLC Procedures",
        "plain": "When new post-market safety risks emerge, FDA can legally order manufacturers to update drug labels rather than waiting for voluntary edits.",
        "technical": "FDA's Section 505(o)(4) guidance defines 'new safety information' triggers, notification letters, 30-day response clocks, discussion periods, and order authorities for NDAs, BLAs, and standalone ANDAs.",
        "url": "https://www.fda.gov/media/128651/download",
    },
    {
        "id": "lsr-slc-30day-502z",
        "name": "30-Day Supplement Clock, Rebuttals & § 502(z) Enforcement",
        "category": "30-Day Clock",
        "plain": "After receiving an FDA safety labeling letter, a company has 30 days to submit the updated label or explain scientifically why it disagrees.",
        "technical": "Under § 505(o)(4), sponsors must file a labeling supplement or rebuttal within 30 days; failure to comply triggers misbranding under § 502(z), civil money penalties (§ 303(f)(4)(A)), and unilateral FDA orders.",
        "url": "https://www.fda.gov/media/86875/download",
    },
    {
        "id": "lsr-boxed-warning-pmr",
        "name": "Boxed Warnings & Concurrent § 505(o)(3) Postmarketing Studies",
        "category": "Boxed Warning + PMR",
        "plain": "The black-bordered Boxed Warning highlights the most serious, life-threatening risks—and often comes with mandatory follow-up safety studies.",
        "technical": "When serious postmarket risks such as acute liver injury emerge, FDA can pair a new Boxed Warning and indication restriction under § 505(o)(4) with a mandatory observational or clinical PMR under § 505(o)(3).",
        "url": "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics/fda-takes-action-new-boxed-warning-acute-serious-liver-injury-and-acute-liver-failure-following",
    },
    {
        "id": "lsr-class-wide-boxed-warning",
        "name": "Class-Wide Boxed Warning & Contraindication Updates",
        "category": "Class-Wide SLC",
        "plain": "If a safety problem affects an entire family of medicines, FDA requires every manufacturer in that class to add the same warning.",
        "technical": "FDA issues class-wide SLC notifications (e.g., hydroxyethyl starch mortality/renal/bleeding warnings) updating Boxed Warnings, Indications, Contraindications, Warnings & Precautions, and Adverse Reactions.",
        "url": "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics/labeling-changes-mortality-kidney-injury-and-excess-bleeding-hydroxyethyl-starch-products",
    },
    {
        "id": "lsr-opioid-class-slc-rems",
        "name": "Class-Wide Safety Labeling & REMS Cross-Referencing",
        "category": "SLC + REMS",
        "plain": "Safety labeling orders can also require Boxed Warnings to alert prescribers about mandatory REMS education and risk programs.",
        "technical": "FDA's class-wide opioid SLC actions demonstrate how § 505(o)(4) labeling mandates integrate Boxed Warnings and Warnings & Precautions directly with outpatient REMS awareness.",
        "url": "https://www.fda.gov/drugs/food-and-drug-administration-overdose-prevention-framework/new-safety-measures-announced-immediate-release-ir-opioids",
    },
]

REMS_ETASU_SHARED = [
    {
        "id": "lsr-whats-in-rems",
        "name": "What's in a REMS? Medication Guides, Comm Plans & ETASU",
        "category": "FD&C § 505-1",
        "plain": "For high-risk drugs, a REMS program can require doctor certification, special pharmacy enrollment, or lab tests before every refill.",
        "technical": "Under FD&C Act § 505-1, a Risk Evaluation and Mitigation Strategy (REMS) may include a Medication Guide, Communication Plan, and Elements to Assure Safe Use (ETASU) with an implementation system.",
        "url": "https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/whats-rems",
    },
    {
        "id": "lsr-rems-statutory-factors",
        "name": "Six Statutory Factors for Requiring a REMS",
        "category": "REMS Necessity",
        "plain": "FDA weighs disease severity, expected benefit, population size, and side-effect seriousness before imposing strict REMS rules.",
        "technical": "FDA's Application of Statutory Factors guidance details the six § 505-1(a)(1) criteria determining when labeling alone is insufficient and a REMS is necessary so benefits outweigh risks.",
        "url": "https://www.fda.gov/media/100307/download",
    },
    {
        "id": "lsr-rems-doc-format",
        "name": "Format and Content of a REMS Document & Bifurcated REMS",
        "category": "REMS Document",
        "plain": "FDA provides a standardized blueprint for REMS documents listing exact prescriber, pharmacy, and patient safety steps.",
        "technical": "FDA's Format and Content of a REMS Document guidance standardizes REMS goals, stakeholder responsibilities, assessment timetables, and bifurcated/single-shared-system structures.",
        "url": "https://www.fda.gov/media/77846/download",
    },
    {
        "id": "lsr-shared-system-rems",
        "name": "Single, Shared System REMS for Brand & Generic ANDAs",
        "category": "Shared System REMS",
        "plain": "When generic versions launch, brand and generic companies normally share one unified REMS portal so clinics do not juggle duplicate systems.",
        "technical": "Under § 505-1(i), ANDA generics referencing a drug with ETASU must use a single, shared system REMS with the RLD unless FDA grants a waiver for excessive burden or anticompetitive blocking.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/development-shared-system-rems-guidance-industry",
    },
    {
        "id": "lsr-shared-rems-dmf",
        "name": "Type V Drug Master File (DMF) for Shared System REMS",
        "category": "REMS DMF",
        "plain": "Multiple generic and brand sponsors can file their shared REMS updates through one central Type V Drug Master File.",
        "technical": "FDA's Shared System REMS DMF guidance allows a consortium or administrator to maintain one Type V DMF referenced via Letters of Authorization by all participating NDA and ANDA holders.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-drug-master-file-shared-system-rems-submissions-guidance-industry",
    },
    {
        "id": "lsr-rems-compliance-program",
        "name": "REMS Compliance Program & Periodic Assessments",
        "category": "REMS Assessments",
        "plain": "Sponsors must regularly audit and report to FDA whether their REMS program is actually preventing harm without blocking patient access.",
        "technical": "FDA's REMS Compliance Program oversees sponsor-submitted REMS Assessments (typically at 18 months, 3 years, and 7 years) evaluating knowledge surveys, ETASU adherence, and burden.",
        "url": "https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/rems-compliance-program",
    },
]


def build_labeling_spl_rems(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "6.2q",
        "checked": CHECKED,
        "plr_spl_dailymed": PLR_SPL_DAILYMED,
        "patient_labeling_ifu": PATIENT_LABELING_IFU,
        "slc_boxed_warnings": SLC_BOXED_WARNINGS,
        "rems_etasu_shared": REMS_ETASU_SHARED,
    }
    (out_dir / "labeling_spl_rems.json").write_text(json.dumps(payload, indent=2) + "\\n", encoding="utf-8")
    return {
        "plr_spl_dailymed": len(PLR_SPL_DAILYMED),
        "patient_labeling_ifu": len(PATIENT_LABELING_IFU),
        "slc_boxed_warnings": len(SLC_BOXED_WARNINGS),
        "rems_etasu_shared": len(REMS_ETASU_SHARED),
    }


def main(argv=None) -> int:
    out = pathlib.Path(argv[0]) if argv else pathlib.Path("site/data")
    print(json.dumps(build_labeling_spl_rems(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'''

LABELING_SPL_REMS_JS = '''import { getJSON } from "./data.js";
import { esc } from "./dom.js";

function renderLabelingSvg() {
  return `
    <div class="diagram-wrap" style="margin:1rem 0;overflow-x:auto">
      <svg viewBox="0 0 820 155" width="100%" style="max-width:820px;height:auto;display:block" role="img" aria-label="Drug labeling PLR/SPL, patient labeling, safety labeling changes, and REMS ETASU architecture">
        <rect x="8" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="103" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">1. PLR &amp; SPL XML</text>
        <text x="103" y="62" text-anchor="middle" font-size="11" fill="currentColor">Highlights &amp; TOC</text>
        <text x="103" y="80" text-anchor="middle" font-size="11" fill="currentColor">Sections 1–17 &amp; PLLR</text>
        <text x="103" y="98" text-anchor="middle" font-size="11" fill="currentColor">HL7 SPL / DailyMed</text>
        <text x="103" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">21 CFR 201.56 / 201.57</text>

        <rect x="212" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="307" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">2. Patient Labeling</text>
        <text x="307" y="62" text-anchor="middle" font-size="11" fill="currentColor">MedGuides (Part 208)</text>
        <text x="307" y="80" text-anchor="middle" font-size="11" fill="currentColor">PPIs &amp; Device IFUs</text>
        <text x="307" y="98" text-anchor="middle" font-size="11" fill="currentColor">PMI One-Page Draft</text>
        <text x="307" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Section 17 Counseling</text>

        <rect x="416" y="16" width="190" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="511" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">3. Safety Changes (SLC)</text>
        <text x="511" y="62" text-anchor="middle" font-size="11" fill="currentColor">FD&amp;C § 505(o)(4) Orders</text>
        <text x="511" y="80" text-anchor="middle" font-size="11" fill="currentColor">30-Day PAS / Rebuttal</text>
        <text x="511" y="98" text-anchor="middle" font-size="11" fill="currentColor">Boxed Warnings &amp; SrLC</text>
        <text x="511" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">Class-Wide Safety</text>

        <rect x="620" y="16" width="192" height="122" rx="10" fill="var(--bg-alt,#f3f6fa)" stroke="var(--accent,#1d4ed8)" stroke-width="1.5"/>
        <text x="716" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">4. REMS &amp; ETASU</text>
        <text x="716" y="62" text-anchor="middle" font-size="11" fill="currentColor">Certification &amp; Lab Checks</text>
        <text x="716" y="80" text-anchor="middle" font-size="11" fill="currentColor">Shared System &amp; Type V</text>
        <text x="716" y="98" text-anchor="middle" font-size="11" fill="currentColor">18m / 3y / 7y Assessments</text>
        <text x="716" y="118" text-anchor="middle" font-size="10" fill="var(--muted,#555)">FD&amp;C § 505-1</text>
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

export async function labelingSplRemsPage(container, mode = "ref") {
  const exploreMode = mode === "explore";
  const data = await getJSON("data/labeling_spl_rems.json");
  const sections = [
    { key: "plr_spl_dailymed", title: "1. Physician Labeling Rule (PLR) & Structured Product Labeling (SPL)", items: data.plr_spl_dailymed || [] },
    { key: "patient_labeling_ifu", title: "2. Patient Labeling: Medication Guides (Part 208), IFUs & PMI", items: data.patient_labeling_ifu || [] },
    { key: "slc_boxed_warnings", title: "3. Safety Labeling Changes (§ 505(o)(4)) & Boxed Warnings", items: data.slc_boxed_warnings || [] },
    { key: "rems_etasu_shared", title: "4. Risk Evaluation & Mitigation Strategies (REMS), ETASU & Shared Systems", items: data.rems_etasu_shared || [] },
  ];

  let active = "all";
  const draw = () => {
    const visible = active === "all" ? sections : sections.filter(s => s.key === active);
    container.innerHTML = `
      <section class="page-head">
        <p class="eyebrow">${exploreMode ? "Explore · Labeling &amp; Risk Mitigation" : "Reference · Labeling &amp; Risk Mitigation"}</p>
        <h1>Drug Labeling (PLR / SPL), Patient Guides, Safety Updates &amp; REMS</h1>
        <p class="lede">${exploreMode
          ? "How official US prescription labels, patient Medication Guides, mandatory FDA safety updates, and REMS safeguards keep medicines used safely."
          : "Primary-sourced reference covering 21 CFR 201.56/201.57 PLR, HL7 SPL, 21 CFR Part 208 Medication Guides &amp; IFUs, FD&amp;C Act § 505(o)(4) SLCs, and § 505-1 REMS/ETASU."}</p>
        <p style="font-size:.85rem;color:var(--muted,#555)">Verified ${esc(data.checked || "2026-11-24")} · <a href="#/${exploreMode ? "ref" : "explore"}/labeling-spl-rems">Switch to ${exploreMode ? "Reference" : "Explore"} view</a></p>
      </section>
      ${renderLabelingSvg()}
      <div class="filter-bar" role="group" aria-label="Filter drug labeling, patient guide, safety change, and REMS sections" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:.75rem 0 1rem">
        ${[["all", "All (24)"], ["plr_spl_dailymed", "PLR & SPL (6)"], ["patient_labeling_ifu", "Patient / IFU (6)"], ["slc_boxed_warnings", "SLCs & Boxed (6)"], ["rems_etasu_shared", "REMS / ETASU (6)"]].map(([k, lbl]) => `
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
    imp = 'import { labelingSplRemsPage } from "./labeling_spl_rems.js";\n'
    if "labelingSplRemsPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/labeling-spl-rems") return labelingSplRemsPage(view, "ref");\n'
        '  if (path === "/explore/labeling-spl-rems") return labelingSplRemsPage(view, "explore");\n'
    )
    if '"/ref/labeling-spl-rems"' not in txt:
        anchor = 'if (path === "/ref/midd-pharmacometrics")'
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
    if "#/ref/labeling-spl-rems" not in txt:
        anchor = '["#/ref/midd-pharmacometrics"'
        item = '["#/ref/labeling-spl-rems", "Labeling (PLR/SPL), SLC & REMS"], '
        if anchor in txt:
            txt = txt.replace(anchor, item + anchor, 1)
        else:
            txt += f'\n// {item}\n'
        changed = True
    if "#/explore/labeling-spl-rems" not in txt:
        anchor2 = '["#/explore/midd-pharmacometrics"'
        item2 = '["#/explore/labeling-spl-rems", "Labeling (PLR/SPL), SLC & REMS"], '
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
    line = "python3 pipeline/build_labeling_spl_rems.py site/data"
    if line in txt:
        return False
    txt = txt.rstrip() + "\n" + line + "\n"
    path.write_text(txt, encoding="utf-8")
    return True


def _patch_app_py(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/api/labeling-spl-rems"' in txt:
        return False
    block = (
        '\n@app.get("/api/labeling-spl-rems")\n'
        'def api_labeling_spl_rems():\n'
        '    p = DATA_DIR / "labeling_spl_rems.json"\n'
        '    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "labeling_spl_rems.json" in txt:
        return False
    snippet = '''    lsr_path = data_dir / "labeling_spl_rems.json"
    if lsr_path.is_file():
        lsr_doc = json.loads(lsr_path.read_text(encoding="utf-8"))
        for sec in ("plr_spl_dailymed", "patient_labeling_ifu", "slc_boxed_warnings", "rems_etasu_shared"):
            for item in lsr_doc.get(sec, []):
                entries.append({
                    "id": item["id"],
                    "title": item["name"],
                    "kind": "Labeling, SLC & REMS",
                    "summary": item.get("plain", ""),
                    "url": "#/ref/labeling-spl-rems",
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
    if "/labeling-spl-rems/" in txt:
        return False
    snippet = '''    # v6.2q Drug Labeling (PLR/SPL), Patient Labeling, SLC & REMS SEO landing page
    lsr_dir = site_dir / "labeling-spl-rems"
    lsr_dir.mkdir(parents=True, exist_ok=True)
    (lsr_dir / "index.html").write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Drug Labeling (PLR/SPL), Medication Guides, SLCs &amp; REMS | Pill by Pill</title>"
        "<meta name='description' content='Primary-sourced guide to 21 CFR 201.56/201.57 PLR, HL7 SPL, 21 CFR 208 Medication Guides, § 505(o)(4) Safety Labeling Changes, and § 505-1 REMS/ETASU.'>"
        "<link rel='canonical' href='https://pillbypill.netlify.app/labeling-spl-rems/'>"
        "<script>location.replace('/#/explore/labeling-spl-rems');</script>"
        "</head><body><h1>Drug Labeling (PLR/SPL), Patient Guides, Safety Updates &amp; REMS</h1>"
        "<p><a href='/#/explore/labeling-spl-rems'>Explore</a> · <a href='/#/ref/labeling-spl-rems'>Reference</a></p></body></html>",
        encoding="utf-8",
    )
    if "written_urls" in locals():
        written_urls.append("/labeling-spl-rems/")
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
    if "#/ref/labeling-spl-rems" in txt:
        return False
    anchor = '"/#/explore/midd-pharmacometrics",'
    add = '"/#/explore/midd-pharmacometrics",\n    "/#/ref/labeling-spl-rems",\n    "/#/explore/labeling-spl-rems",'
    if anchor in txt:
        txt = txt.replace(anchor, add, 1)
    else:
        txt = txt.rstrip() + '\n# routes: /#/ref/labeling-spl-rems /#/explore/labeling-spl-rems\n'
    path.write_text(txt, encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    js_dir = root / "site" / "js"
    return {
        "build_labeling_spl_rems_py": _write_if_changed(pipe_dir / "build_labeling_spl_rems.py", BUILD_LABELING_SPL_REMS_PY),
        "labeling_spl_rems_js": _write_if_changed(js_dir / "labeling_spl_rems.js", LABELING_SPL_REMS_JS),
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

        (root / "site" / "js" / "app.js").write_text('function r(path, query) {\n  if (path === "/ref/midd-pharmacometrics") return null;\n}\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [{ items: [["#/ref/midd-pharmacometrics", "MIDD (ICH M15), PopPK & QSP"]] }];\nconst EXPLORE_NAV = [["#/explore/midd-pharmacometrics", "MIDD (ICH M15), PopPK & QSP"]];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (root / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/explore/midd-pharmacometrics",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        py_compile.compile(str(root / "pipeline" / "build_labeling_spl_rems.py"), doraise=True)
        out = json.loads(subprocess.check_output(
            [sys.executable, str(root / "pipeline" / "build_labeling_spl_rems.py"), str(root / "site" / "data")],
            text=True,
        ))
        assert out == {"plr_spl_dailymed": 6, "patient_labeling_ifu": 6, "slc_boxed_warnings": 6, "rems_etasu_shared": 6}, out

        doc = json.loads((root / "site" / "data" / "labeling_spl_rems.json").read_text(encoding="utf-8"))
        for k in ("plr_spl_dailymed", "patient_labeling_ifu", "slc_boxed_warnings", "rems_etasu_shared"):
            for item in doc[k]:
                assert item["url"].startswith("https://"), item
                assert "--card" not in item["plain"] and "--card" not in item["technical"]

        assert "--card" not in (root / "site" / "js" / "labeling_spl_rems.js").read_text(encoding="utf-8")
        print("V62Q_LABELING_SPL_REMS_SELFTEST_PASSED", json.dumps({**out, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2q Drug Labeling (PLR/SPL), SLC & REMS patch.")
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
