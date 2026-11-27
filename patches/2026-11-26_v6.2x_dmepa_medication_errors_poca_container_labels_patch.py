#!/usr/bin/env python3
"""Pill by Pill v6.2x patch: Medication Errors (DMEPA), Proprietary Name Review (POCA), Tall-Man Lettering & Container Label Design.

Adds:
  - pipeline/build_dmepa_med_errors.py -> site/data/dmepa_med_errors.json (24 entries, 4 pillars)
  - site/js/dmepa_med_errors.js (dmepaMedErrorsPage with inline SVG, 4 section filters, zero --card CSS, imports esc from ./ui.js)
  - Wiring in site/js/app.js (#/ref/dmepa-med-errors, #/explore/dmepa-med-errors), site/js/layout.js,
    pipeline/run_all.sh, app.py (/api/dmepa-med-errors), pipeline/build_global_search.py,
    pipeline/build_v60_static_pages.py (/dmepa-med-errors/ 66th SEO page), and tests/test_v60_site.py.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

BUILD_DMEPA_MED_ERRORS_PY = r'''#!/usr/bin/env python3
"""Build Pill by Pill v6.2x Medication Errors (DMEPA), POCA, Tall-Man Lettering & Container Label Design JSON."""
from __future__ import annotations

import json
import pathlib
import sys

CHECKED = "2026-11-26"

SECTIONS = [
    {
        "id": "proprietary_name_poca",
        "title": "1. Proprietary Name Review, POCA & FMEA (DMEPA / CBER)",
        "summary": "Pre-market proprietary name evaluation by CDER DMEPA and CBER, Phonetic and Orthographic Computer Analysis (POCA), handwriting/spoken simulation, and FMEA.",
    },
    {
        "id": "tall_man_lasa_names",
        "title": "2. Look-Alike / Sound-Alike (LASA) & Tall Man Lettering (TML)",
        "summary": "FDA Name Differentiation Project, Tall Man Lettering (TML) for established drug names, ISMP/USP collaboration, and postmarket name-change authorities.",
    },
    {
        "id": "container_carton_labels",
        "title": "3. Container Labels & Carton Labeling Design (May 2022)",
        "summary": "Principal display panel hierarchy, quantity-per-total-volume strength expression for injectables, ferrule/cap overseal rules, and barcode/inspectability clearances.",
    },
    {
        "id": "product_design_human_factors",
        "title": "4. Product Design, Dosing Devices & Systems-Based Error Prevention",
        "summary": "FDA's 2016 Product Design guidance: avoiding multi-vial single doses, aligning oral liquid metric dosing devices, preventing two-step dilution errors, and tablet/capsule attributes.",
    },
]

ENTRIES = [
    # --- 1. Proprietary Name Review, POCA & FMEA ---
    {
        "id": "dmepa-proprietary-name-submission",
        "section": "proprietary_name_poca",
        "title": "Contents of a Complete Proprietary Name Submission (April 2016)",
        "badge": "IND / NDA / BLA",
        "summary": "Specifies the required submission package for FDA proprietary name review, including intended pronunciation, phonetic/orthographic simulation data, and proposed labeling.",
        "details": "Sponsors may submit proprietary name requests as early as the end of Phase 2 (IND) or concurrently with NDA/BLA/ANDA filings, following standardized completeness criteria.",
        "source_label": "FDA Contents of a Complete Proprietary Name Submission",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/contents-complete-submission-evaluation-proprietary-names",
    },
    {
        "id": "dmepa-best-practices-rx-names",
        "section": "proprietary_name_poca",
        "title": "Best Practices in Developing Proprietary Names for Rx Drugs (Dec 2020)",
        "badge": "Rx Naming",
        "summary": "Describes FDA's two-part evaluation framework—promotional/misbranding screening and medication-error safety assessment—to prevent confusing drug names before approval.",
        "details": "Advises sponsors to screen out USAN stem conflicts, medical abbreviation look-alikes (e.g., 'QD', 'U'), and misleading efficacy claims prior to submitting names.",
        "source_label": "FDA Best Practices in Developing Proprietary Names (Rx)",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/best-practices-developing-proprietary-names-human-prescription-drug-products-guidance-industry",
    },
    {
        "id": "dmepa-best-practices-otc-names",
        "section": "proprietary_name_poca",
        "title": "Developing Proprietary Names for Nonprescription (OTC) Drugs",
        "badge": "OTC Naming",
        "summary": "Addresses unique self-selection and brand-extension risks for OTC drug names, where consumers choose products in retail aisles without a prescriber or pharmacist intermediary.",
        "details": "Evaluates umbrella branding ('line extensions') where identical root names across different active ingredients (e.g., antihistamine vs. analgesic) can cause accidental overdose.",
        "source_label": "FDA Best Practices in Developing Proprietary Names (OTC)",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/best-practices-developing-proprietary-names-human-nonprescription-drug-products-draft-guidance",
    },
    {
        "id": "dmepa-mapp-6720-workflow",
        "section": "proprietary_name_poca",
        "title": "CDER MAPP 6720.2: DMEPA I & II Proprietary Name Review Procedures",
        "badge": "CDER MAPP",
        "summary": "Details internal CDER Office of Surveillance and Epidemiology (OSE) / DMEPA timelines and workload coordination for evaluating proprietary name requests.",
        "details": "Outlines 180-day IND and 90-day NDA/BLA/ANDA review clocks, completeness triage, and formal notification letters when a proposed name is found unacceptable.",
        "source_label": "FDA CDER MAPP 6720.2 Rev. 2",
        "source_url": "https://www.fda.gov/media/77552/download",
    },
    {
        "id": "dmepa-cber-sopp-8001-biologics",
        "section": "proprietary_name_poca",
        "title": "CBER SOPP 8001.4: Proprietary Name Review for Biologics & Vaccines",
        "badge": "CBER SOPP",
        "summary": "Establishes CBER's parallel proprietary name review workflow for biologics, vaccines, blood products, and cellular/gene therapies alongside nonproprietary 4-letter suffixes.",
        "details": "Coordinates between CBER's Advertising and Promotional Labeling Branch (APLB) and clinical review divisions to screen both safety and promotional implications.",
        "source_label": "FDA CBER SOPP 8001.4",
        "source_url": "https://www.fda.gov/media/95529/download",
    },
    {
        "id": "dmepa-poca-fmea-scoring",
        "section": "proprietary_name_poca",
        "title": "Phonetic & Orthographic Computer Analysis (POCA) + FMEA",
        "badge": "POCA + FMEA",
        "summary": "DMEPA enters proposed names into POCA to score orthographic and phonetic similarity against thousands of marketed drugs, then runs Failure Mode and Effects Analysis (FMEA).",
        "details": "FMEA examines overlapping strengths, dosage forms, routes, and clinical settings (e.g., handwritten scripts where 'T' looks like 'F' or 'a' looks like 'u') to judge real-world error risk.",
        "source_label": "FDA Drug Name Review Overview",
        "source_url": "https://www.fda.gov/drugs/fda-drug-info-rounds-video/drug-name-review",
    },
    # --- 2. Look-Alike / Sound-Alike (LASA) & Tall Man Lettering ---
    {
        "id": "dmepa-name-differentiation-tml",
        "section": "tall_man_lasa_names",
        "title": "FDA Name Differentiation Project & Tall Man Lettering (TML)",
        "badge": "Tall Man Lettering",
        "summary": "Uses mixed-case capitalization (e.g., hydrOXYzine vs. hydrALAzine; vinBLAStine vs. vinCRIStine) to highlight dissimilar letters in look-alike established drug names.",
        "details": "Targets selection errors in pharmacy shelves, EHR picklists, and automated dispensing cabinets (ADCs) where alphabetically adjacent names share prefixes or suffixes.",
        "source_label": "FDA Name Differentiation Project",
        "source_url": "https://www.fda.gov/drugs/medication-errors-related-cder-regulated-drug-products/fda-name-differentiation-project",
    },
    {
        "id": "dmepa-dmames-ismp-usp",
        "section": "tall_man_lasa_names",
        "title": "DMEPA, DMAMES & External Safety Partners (ISMP / USP / VA)",
        "badge": "Postmarket Safety",
        "summary": "CDER's DMEPA and Division of Medication Error Prevention and Analysis collaborate with ISMP, USP, and the VA National Center for Patient Safety on error root causes.",
        "details": "When postmarketing MedWatch reports reveal unexpected name confusion, FDA can require labeling updates, safety communications, or a proprietary name change.",
        "source_label": "FDA Medication Errors Related to CDER Drugs",
        "source_url": "https://www.fda.gov/drugs/drug-safety-and-availability/medication-errors-related-cder-regulated-drug-products",
    },
    {
        "id": "dmepa-proprietary-name-biologics-portal",
        "section": "tall_man_lasa_names",
        "title": "Biologics Proprietary Name & Proper Name Suffix Coordination",
        "badge": "Biologics Suffix",
        "summary": "Ensures a biologic's proprietary brand name and its FDA-designated four-letter distinguishing suffix (e.g., -abcd) do not introduce new look-alike or sound-alike confusion.",
        "details": "Applies to reference biologics, biosimilars, and interchangeable products across CBER and CDER product classes.",
        "source_label": "FDA CBER Proprietary Name Review",
        "source_url": "https://www.fda.gov/vaccines-blood-biologics/labeling-cber-regulated-products/proprietary-name-review-biologic-products",
    },
    {
        "id": "dmepa-poca-fmea-precedent",
        "section": "tall_man_lasa_names",
        "title": "DMEPA POCA Thresholds & Eliminating False-Positive Matches",
        "badge": "POCA Review",
        "summary": "DMEPA reviews POCA candidate lists (typically >= 50% combined orthographic/phonetic similarity) and documents why dissimilar, discontinued, or veterinary names are excluded before FMEA.",
        "details": "Remaining look-alike/sound-alike candidates undergo structured FMEA across dose, frequency, route, and patient population to confirm low risk of wrong-drug dispensing.",
        "source_label": "FDA DMEPA Proprietary Name Review Precedent",
        "source_url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2011/022569Orig1s000NameR.pdf",
    },
    {
        "id": "dmepa-script-handwriting-testing",
        "section": "tall_man_lasa_names",
        "title": "Handwriting & Spoken Pronunciation Simulation Studies",
        "badge": "Simulation Studies",
        "summary": "Sponsors conduct standardized written and verbal prescription simulation studies with US healthcare professionals to detect real-world transcription or mishearing errors.",
        "details": "Studies test diverse cursive/printed scripts and varied English pronunciations because sponsors cannot control how clinicians speak or write a drug name in practice.",
        "source_label": "FDA DMEPA Handwriting & Phonetic Criteria",
        "source_url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2014/204684Orig1s000NameR.pdf",
    },
    {
        "id": "dmepa-tml-selection-error-scope",
        "section": "tall_man_lasa_names",
        "title": "Scope of Tall Man Lettering: Selection vs. Prescribing Errors",
        "badge": "Selection Risk",
        "summary": "Tall Man lettering primarily mitigates visual selection errors between established look-alike drug names rather than replacing premarket proprietary name screening.",
        "details": "FDA maintains an official List of Established Drug Names Recommended to Use Tall Man Lettering and coordinates updates as new look-alike generics enter the market.",
        "source_label": "FDA DMEPA Tall Man Lettering Review",
        "source_url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2008/022224s000_NameR.pdf",
    },
    # --- 3. Container Labels & Carton Labeling Design ---
    {
        "id": "dmepa-container-carton-2022",
        "section": "container_carton_labels",
        "title": "Safety Considerations for Container Labels & Carton Labeling (May 2022)",
        "badge": "Final Guidance",
        "summary": "Provides human-factors principles for prescription drug and biologic container labels and cartons so critical information (name, strength, route, warnings) is legible and unambiguous.",
        "details": "Discourages trailing zeros (e.g., 5.0 mg), recommends leading zeros (0.5 mg), and stresses uncluttered principal display panels with clear contrast and >= 6–8 pt typography.",
        "source_label": "FDA Container Labels & Carton Labeling Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-considerations-container-labels-and-carton-labeling-design-minimize-medication-errors",
    },
    {
        "id": "dmepa-carton-container-resources",
        "section": "container_carton_labels",
        "title": "FDA Carton & Container Labeling Resources Hub",
        "badge": "Labeling Hub",
        "summary": "Consolidates FDA guidances on container/carton safety design, physical-chemical identifiers (PCIDs), allowable excess vial volume, and linear/2D barcode requirements.",
        "details": "Serves as the central reference for CMC and Regulatory teams preparing Module 1.14 draft container labels and carton mockups.",
        "source_label": "FDA Carton and Container Labeling Resources",
        "source_url": "https://www.fda.gov/drugs/fdas-labeling-resources-human-prescription-drugs/carton-and-container-labeling-resources",
    },
    {
        "id": "dmepa-injectable-strength-per-volume",
        "section": "container_carton_labels",
        "title": "Small-Volume Parenteral Strength Expression (Quantity per Total Volume)",
        "badge": "Parenteral Strength",
        "summary": "For small-volume injectables, FDA recommends expressing strength per total volume as the primary prominent statement (e.g., 10 mg/10 mL) followed by per-mL in parentheses (1 mg/mL).",
        "details": "Prevents 10-fold overdoses when clinicians confuse concentration per milliliter with the total drug quantity contained in the vial or prefilled syringe.",
        "source_label": "FDA Injectable Strength Expression Safety Alert",
        "source_url": "https://www.fda.gov/drugs/human-drug-compounding/differences-strength-expression-product-labels-compounders-and-conventional-manufacturers-may-lead",
    },
    {
        "id": "dmepa-ferrule-cap-visual-inspection",
        "section": "container_carton_labels",
        "title": "Ferrule/Cap Overseal Rules & Uncovered Visual Inspection Window",
        "badge": "Vial Design",
        "summary": "FDA restricts text on vial ferrules and cap overseals (except critical warnings like 'Warning: Paralyzing Agent') and requires leaving an uncovered window for 100% visual inspection.",
        "details": "Ensures clinicians can inspect solution clarity/particulates before administration and avoids distracting or illegible text on curved metal caps.",
        "source_label": "FDA CMC Container Label Review Criteria",
        "source_url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2021/761178Orig1s000ChemR.pdf",
    },
    {
        "id": "dmepa-color-coding-differentiation",
        "section": "container_carton_labels",
        "title": "Color Differentiation vs. Misleading Color-Coding Traps",
        "badge": "Color & Contrast",
        "summary": "Color can differentiate strengths within a single product line, but relying on color alone across different drugs causes confirmation bias and wrong-drug selection errors.",
        "details": "Sponsors must ensure high text-to-background contrast on small vials, prefilled pens, and blister packs, and verify legibility under dim clinical lighting.",
        "source_label": "FDA Carton & Vial Label Review Precedent",
        "source_url": "https://www.accessdata.fda.gov/drugsatfda_docs/nda/2021/761109Orig1s000ChemR.pdf",
    },
    {
        "id": "dmepa-name-submission-pdf",
        "section": "container_carton_labels",
        "title": "Submitting Mockups & Actual-Size Container/Carton Labels",
        "badge": "100% Scale Mockups",
        "summary": "FDA requires actual-size (100% scale) color mockups of container labels and cartons so reviewers can verify font legibility, barcode placement, and strength prominence.",
        "details": "Oversized or grayscale drafts can hide crowding, truncated warnings, or illegible micro-typography on 1 mL or 2 mL vials.",
        "source_label": "FDA Proprietary Name & Labeling Submission Guide",
        "source_url": "https://www.fda.gov/media/72144/download",
    },
    # --- 4. Product Design, Dosing Devices & Systems-Based Error Prevention ---
    {
        "id": "dmepa-product-design-2016",
        "section": "product_design_human_factors",
        "title": "Safety Considerations for Product Design to Minimize Medication Errors (2016)",
        "badge": "Systems Design",
        "summary": "Urges sponsors to apply human-factors and systems engineering early in development—designing the drug, container closure, and user interface for real clinical and home environments.",
        "details": "Applies broadly to INDs, NDAs, BLAs, ANDAs, and OTC monograph drugs to eliminate use-related hazards before design lock.",
        "source_label": "FDA Product Design to Minimize Medication Errors",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-considerations-product-design-minimize-medication-errors-guidance-industry",
    },
    {
        "id": "dmepa-single-vial-vs-multiple-units",
        "section": "product_design_human_factors",
        "title": "Avoiding Multi-Vial or Multi-Tablet Single Doses",
        "badge": "Unit-of-Use",
        "summary": "Requiring multiple vials, syringes, or tablets to assemble one usual single dose invites arithmetic errors or forgotten counts; design strengths to match common clinical doses.",
        "details": "Also recommends aligning titration strengths so intermediate step-up or step-down doses are achievable without splitting un-scored tablets.",
        "source_label": "FDA Product Design Guidance PDF",
        "source_url": "https://www.fda.gov/files/drugs/published/Safety-Considerations-for-Product-Design-to-Minimize-Medication-Errors-Guidance-for-Industry.pdf",
    },
    {
        "id": "dmepa-oral-liquid-metric-devices",
        "section": "product_design_human_factors",
        "title": "Metric-Only Oral Liquid Dosing Devices (mL Alignment)",
        "badge": "Oral Dosing",
        "summary": "Oral liquid dosing cups/syringes must use metric units (mL) matching prescribed dosing—never household teaspoons or mismatched mg markings that cause severe pediatric overdoses.",
        "details": "Sponsors should co-package an appropriately calibrated dosing device whenever standard pharmacy syringes cannot accurately measure the labeled volume.",
        "source_label": "FDA Product Design Oral Dosing Standards",
        "source_url": "https://www.fda.gov/files/drugs/published/Safety-Considerations-for-Product-Design-to-Minimize-Medication-Errors-Guidance-for-Industry.pdf",
    },
    {
        "id": "dmepa-two-step-dilution-hazards",
        "section": "product_design_human_factors",
        "title": "Eliminating Two-Step Dilution & Concentrate Administration Hazards",
        "badge": "IV Concentrates",
        "summary": "Concentrated solutions requiring two-step dilution prior to IV infusion carry high risk of direct undiluted administration or math miscalculation.",
        "details": "Ready-to-administer (RTU) presentations or single-step dilution workflows reduce preparation errors in high-stress ICU and emergency settings.",
        "source_label": "FDA Product Design Dilution Hazard Guidance",
        "source_url": "https://www.fda.gov/files/drugs/published/Safety-Considerations-for-Product-Design-to-Minimize-Medication-Errors-Guidance-for-Industry.pdf",
    },
    {
        "id": "dmepa-premarket-name-best-practices-pdf",
        "section": "product_design_human_factors",
        "title": "Proactive Risk Assessment Before Design & Name Lock",
        "badge": "Proactive HFE",
        "summary": "Combining proactive FMEA, simulated-use human factors testing, and historical error analysis before Phase 3/NDA submission prevents costly post-approval recalls and name changes.",
        "details": "Addresses the finding that medication errors account for substantial preventable patient harm and up to 30% of error fatalities involve naming, labeling, or packaging.",
        "source_label": "FDA Best Practices Proprietary Names PDF",
        "source_url": "https://www.fda.gov/media/144257/download",
    },
    {
        "id": "dmepa-otc-rx-naming-alignment",
        "section": "product_design_human_factors",
        "title": "Dual-Use & Rx-to-OTC Switch Naming and Packaging Continuity",
        "badge": "Switch Safety",
        "summary": "When a prescription drug switches to OTC status or shares active ingredients across strengths, clear naming and packaging differentiation prevent accidental double-dosing.",
        "details": "Aligns Drug Facts formatting, active-ingredient prominence, and dosing-device markings with consumer self-selection comprehension.",
        "source_label": "FDA Proprietary Name Evaluation Guidance",
        "source_url": "https://www.fda.gov/media/88496/download",
    },
]


def build_dmepa_med_errors(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "title": "Medication Errors (DMEPA), Proprietary Name Review (POCA) & Container Label Design",
        "subtitle": "FDA DMEPA proprietary name screening (POCA/FMEA), Tall Man Lettering (TML), container/carton labeling (May 2022), and error-resistant product design.",
        "sections": SECTIONS,
        "entries": ENTRIES,
        "counts": {
            "sections": len(SECTIONS),
            "entries": len(ENTRIES),
        },
    }
    out_path = out_dir / "dmepa_med_errors.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv=None) -> int:
    out_dir = pathlib.Path(argv[1]) if argv and len(argv) > 1 else pathlib.Path("site/data")
    res = build_dmepa_med_errors(out_dir)
    print(f"Built {out_dir / 'dmepa_med_errors.json'} ({res['counts']['entries']} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
'''

DMEPA_MED_ERRORS_JS = r'''import { getJSON } from "./data.js";
import { esc } from "./ui.js";

const DMEPA_SVG = `
<svg viewBox="0 0 760 150" role="img" aria-label="Medication error prevention pipeline from POCA proprietary name screening and Tall Man Lettering to container label design and human-factors product design" style="width:100%;max-width:760px;height:auto;display:block;margin:1rem auto;">
  <rect x="8" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="92" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Name Screening</text>
  <text x="92" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">DMEPA / CBER SOPP</text>
  <text x="92" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">POCA Phonetic/Ortho</text>
  <text x="92" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">FMEA &amp; Simulations</text>

  <line x1="176" y1="71" x2="198" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="198,66 208,71 198,76" fill="var(--accent)"/>

  <rect x="208" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="292" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. LASA &amp; TML</text>
  <text x="292" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Tall Man Lettering</text>
  <text x="292" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">hydrOXY / hydrALA</text>
  <text x="292" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">ISMP &amp; USP Alignment</text>

  <line x1="376" y1="71" x2="398" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="398,66 408,71 398,76" fill="var(--accent)"/>

  <rect x="408" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="492" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Label &amp; Carton</text>
  <text x="492" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Total Volume First</text>
  <text x="492" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Ferrule / Cap Rules</text>
  <text x="492" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">100% Scale Mockups</text>

  <line x1="576" y1="71" x2="598" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="598,66 608,71 598,76" fill="var(--accent)"/>

  <rect x="608" y="18" width="144" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="680" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. Product Design</text>
  <text x="680" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">Single-Vial Doses</text>
  <text x="680" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Metric mL Devices</text>
  <text x="680" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">Avoid 2-Step Dilution</text>
</svg>`;

export async function dmepaMedErrorsPage(view, mode = "ref") {
  view.innerHTML = `<div class="panel" style="background:var(--paper);padding:1.25rem;border:1px solid var(--line);border-radius:10px;"><p>Loading Medication Errors (DMEPA), POCA &amp; Container Label Design reference…</p></div>`;
  const data = await getJSON("data/dmepa_med_errors.json");
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
          <a href="#/${isExplore ? "ref" : "explore"}/dmepa-med-errors" style="padding:0.4rem 0.8rem;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);text-decoration:none;font-size:0.9rem;">
            ${isExplore ? "Switch to Reference →" : "← Switch to Explore"}
          </a>
        </div>
        ${DMEPA_SVG}
        <div style="display:flex;flex-wrap:wrap;gap:0.45rem;margin-top:0.75rem;">${pills}</div>
      </section>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:0.9rem;">
        ${cards}
      </div>
      <p style="margin-top:1rem;font-size:0.82rem;color:var(--muted);">Checked ${esc(data.checked)} against primary FDA DMEPA &amp; labeling sources.</p>
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
    imp = 'import { dmepaMedErrorsPage } from "./dmepa_med_errors.js";\n'
    if "dmepaMedErrorsPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/dmepa-med-errors") return dmepaMedErrorsPage(view, "ref");\n'
        '  if (path === "/explore/dmepa-med-errors") return dmepaMedErrorsPage(view, "explore");\n'
    )
    if '"/ref/dmepa-med-errors"' not in txt:
        for anchor in (
            'if (path === "/ref/microbiology-sterility")',
            'if (path === "/ref/pv-faers-sentinel")',
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
    ref_entry = '      { label: "Medication Errors & POCA Names", href: "#/ref/dmepa-med-errors" },\n'
    if "#/ref/dmepa-med-errors" not in txt:
        anchor = '{ label: "Microbiology, Endotoxins & CCIT", href: "#/ref/microbiology-sterility" },'
        if anchor in txt:
            txt = txt.replace(anchor, anchor + "\n" + ref_entry.rstrip("\n"), 1)
            changed = True
        elif "REF_NAV_GROUPS" in txt:
            txt = txt.replace("];", ref_entry + "];", 1)
            changed = True
    exp_entry = '  { label: "Medication Errors & POCA Names", href: "#/explore/dmepa-med-errors" },\n'
    if "#/explore/dmepa-med-errors" not in txt:
        anchor = '{ label: "Microbiology, Endotoxins & CCIT", href: "#/explore/microbiology-sterility" },'
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
    line = "python3 pipeline/build_dmepa_med_errors.py site/data\n"
    if "build_dmepa_med_errors.py" not in txt:
        anchor = "python3 pipeline/build_microbiology_sterility.py site/data\n"
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
    if "/api/dmepa-med-errors" in txt:
        return False
    block = (
        '\n@app.get("/api/dmepa-med-errors")\n'
        'def api_dmepa_med_errors():\n'
        '    return _read_site_json("data/dmepa_med_errors.json")\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "dmepa_med_errors.json" in txt:
        return False
    snippet = (
        '\n    dmepa_path = data_dir / "dmepa_med_errors.json"\n'
        '    if dmepa_path.is_file():\n'
        '        dmepa_obj = json.loads(dmepa_path.read_text(encoding="utf-8"))\n'
        '        for item in dmepa_obj.get("entries", []):\n'
        '            entries.append({\n'
        '                "id": item["id"],\n'
        '                "title": item["title"],\n'
        '                "subtitle": f"Medication Errors & POCA · {item.get(\'badge\', \'\')}",\n'
        '                "kind": "Medication Errors & DMEPA",\n'
        '                "href": "#/ref/dmepa-med-errors",\n'
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
    if "dmepa-med-errors" in txt:
        return False
    snippet = (
        '\n    dmepa_file = data_dir / "dmepa_med_errors.json"\n'
        '    if dmepa_file.is_file():\n'
        '        dmepa_d = json.loads(dmepa_file.read_text(encoding="utf-8"))\n'
        '        _write_landing(\n'
        '            site_dir / "dmepa-med-errors" / "index.html",\n'
        '            "Medication Errors (DMEPA), POCA Names & Container Labels | Pill by Pill",\n'
        '            dmepa_d.get("subtitle", ""),\n'
        '            "#/ref/dmepa-med-errors",\n'
        '            dmepa_d.get("entries", []),\n'
        '        )\n'
        '        written_urls.append(f"{BASE_URL}/dmepa-med-errors/")\n'
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
    if "#/ref/dmepa-med-errors" in txt:
        return False
    addition = '    "#/ref/dmepa-med-errors",\n    "#/explore/dmepa-med-errors",\n'
    anchor = '"#/ref/microbiology-sterility",'
    if anchor in txt:
        txt = txt.replace(anchor, anchor + "\n" + addition.rstrip("\n"), 1)
        path.write_text(txt, encoding="utf-8")
        return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    root = pathlib.Path(root)
    changed = {}
    changed["build_dmepa_med_errors.py"] = _write_if_changed(
        root / "pipeline" / "build_dmepa_med_errors.py", BUILD_DMEPA_MED_ERRORS_PY
    )
    changed["dmepa_med_errors.js"] = _write_if_changed(
        root / "site" / "js" / "dmepa_med_errors.js", DMEPA_MED_ERRORS_JS
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
        (root / "site" / "js" / "app.js").write_text('if (path === "/ref/microbiology-sterility") return x;\nroute();\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [\n  { label: "Microbiology, Endotoxins & CCIT", href: "#/ref/microbiology-sterility" },\n];\nconst EXPLORE_NAV = [\n  { label: "Microbiology, Endotoxins & CCIT", href: "#/explore/microbiology-sterility" },\n];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text('#!/bin/sh\npython3 pipeline/build_microbiology_sterility.py site/data\n', encoding="utf-8")
        (root / "app.py").write_text('from fastapi import FastAPI\napp = FastAPI()\n', encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('ROUTES = [\n    "#/ref/microbiology-sterility",\n]\n', encoding="utf-8")

        res1 = apply_patch(root)
        assert all(res1.values()), f"Expected all changed on first run: {res1}"
        res2 = apply_patch(root)
        assert not any(res2.values()), f"Expected idempotent second run: {res2}"

        subprocess.run([sys.executable, str(root / "pipeline" / "build_dmepa_med_errors.py"), str(root / "site" / "data")], check=True)
        data = json.loads((root / "site" / "data" / "dmepa_med_errors.json").read_text(encoding="utf-8"))
        assert len(data["sections"]) == 4
        assert len(data["entries"]) == 24
        for sec in data["sections"]:
            cnt = sum(1 for e in data["entries"] if e["section"] == sec["id"])
            assert cnt == 6, f"Section {sec['id']} count {cnt} != 6"
        for e in data["entries"]:
            assert e["source_url"].startswith("https://"), f"Non-HTTPS URL: {e['source_url']}"
        js_txt = (root / "site" / "js" / "dmepa_med_errors.js").read_text(encoding="utf-8")
        assert "--card" not in js_txt
        assert "./dom.js" not in js_txt
        assert "./ui.js" in js_txt
        app_js_txt = (root / "site" / "js" / "app.js").read_text(encoding="utf-8")
        assert app_js_txt.index('"/ref/dmepa-med-errors"') < app_js_txt.index("route();")
        print("V62X_DMEPA_MED_ERRORS_SELFTEST_PASSED")


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
