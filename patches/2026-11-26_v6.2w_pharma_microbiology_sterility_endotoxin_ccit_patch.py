#!/usr/bin/env python3
"""Pill by Pill v6.2w patch: Pharmaceutical Microbiology, Sterility Assurance, Endotoxin (LAL/rFC) & CCIT.

Adds:
  - pipeline/build_microbiology_sterility.py -> site/data/microbiology_sterility.json (24 entries, 4 pillars)
  - site/js/microbiology_sterility.js (microbiologySterilityPage with inline SVG, 4 section filters, zero --card CSS, imports esc from ./ui.js)
  - Wiring in site/js/app.js (#/ref/microbiology-sterility, #/explore/microbiology-sterility), site/js/layout.js,
    pipeline/run_all.sh, app.py (/api/microbiology-sterility), pipeline/build_global_search.py,
    pipeline/build_v60_static_pages.py (/microbiology-sterility/ 65th SEO page), and tests/test_v60_site.py.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

BUILD_MICROBIOLOGY_STERILITY_PY = r'''#!/usr/bin/env python3
"""Build Pill by Pill v6.2w Pharmaceutical Microbiology, Sterility Assurance, Endotoxin & CCIT reference JSON."""
from __future__ import annotations

import json
import pathlib
import sys

CHECKED = "2026-11-26"

SECTIONS = [
    {
        "id": "aseptic_sterility_assurance",
        "title": "1. Aseptic Processing, Terminal Sterilization & Cleanroom Controls",
        "summary": "21 CFR 211.113 sterile drug manufacturing, FDA's 2004 Aseptic Processing guidance, ISO 14644-1/2 cleanroom particle & microbiological qualification, and CPGM 7356.002A.",
    },
    {
        "id": "endotoxins_pyrogens_rfc",
        "title": "2. Pyrogen & Bacterial Endotoxins Testing (USP <85>, <86> rFC & LER)",
        "summary": "March 2026 FDA Pyrogen and Endotoxins Q&A revision aligning with USP <86> recombinant reagents, USP <85> LAL methods, Low Endotoxin Recovery (LER), and investigational limits.",
    },
    {
        "id": "ccit_stability_sterility",
        "title": "3. Container Closure Integrity Testing (CCIT, USP <1207>) & Sterility",
        "summary": "Replacing destructive sterility testing in stability protocols with validated deterministic CCIT (USP <1207>, <1207.1>, <1207.2>) annually and at expiration.",
    },
    {
        "id": "nonsterile_bcc_micro_lab",
        "title": "4. Non-Sterile Microbiology, Burkholderia cepacia (USP <60>) & QC Labs",
        "summary": "Controlling bioburden and objectionable organisms (21 CFR 211.110/211.113(a)), Burkholderia cepacia complex (BCC) in aqueous non-sterile drugs, and FDA's Pharmaceutical Microbiology Manual.",
    },
]

ENTRIES = [
    # --- 1. Aseptic Processing, Terminal Sterilization & Cleanroom Controls ---
    {
        "id": "micro-aseptic-processing-2004",
        "section": "aseptic_sterility_assurance",
        "title": "Sterile Drug Products Produced by Aseptic Processing (cGMP Guidance)",
        "badge": "21 CFR 211.113",
        "summary": "FDA's foundational guidance for sterile drugs and biologics manufactured without terminal sterilization, covering cleanroom zoning, personnel gowning, media fills, and environmental monitoring.",
        "details": "Clarifies how manufacturers satisfy 21 CFR parts 210 and 211 when sterilizing-grade filtration and aseptic assembly replace moist-heat or radiation terminal sterilization.",
        "source_label": "FDA Aseptic Processing Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice",
    },
    {
        "id": "micro-terminal-sterilization-preference",
        "section": "aseptic_sterility_assurance",
        "title": "Terminal Sterilization vs. Aseptic Processing (CPGM 7356.002A)",
        "badge": "CPGM 7356.002A",
        "summary": "Under FDA Sterile Drug Process Inspections, terminal sterilization should be used whenever the drug product and container-closure system can withstand the sterilization cycle.",
        "details": "Inspectors evaluate sterilization cycle validation, bioburden pre-sterilization limits, biological indicators, and parametric release justification during sterile facility audits.",
        "source_label": "FDA Sterile Drug Process Inspections (7356.002A)",
        "source_url": "https://www.fda.gov/media/75174/download",
    },
    {
        "id": "micro-iso-14644-cleanrooms",
        "section": "aseptic_sterility_assurance",
        "title": "ISO 14644-1 / 14644-2 Air Cleanliness & Microbiological Limits",
        "badge": "ISO 5–8",
        "summary": "FDA adopted ISO 14644-1 and 14644-2 nonviable particulate classifications in the 2004 Aseptic Processing guidance, while emphasizing that aseptic facilities cannot rely on particle counts alone.",
        "details": "ISO 5 critical areas require active viable air, surface, and personnel glove monitoring alongside unidirectional airflow (smoke studies) and differential pressure cascades.",
        "source_label": "FDA CGMP Production & Process Controls Q&A",
        "source_url": "https://www.fda.gov/drugs/guidances-drugs/questions-and-answers-current-good-manufacturing-practice-regulations-production-and-process",
    },
    {
        "id": "micro-aseptic-biologics-issues",
        "section": "aseptic_sterility_assurance",
        "title": "Aseptic Processing of Biological Products & Method Verification",
        "badge": "CBER / CDER",
        "summary": "BLA Module 3 submissions must verify bioburden, sterility, and endotoxin test methods for in-process intermediates and finished drug product and confirm plunger movement does not breach sterility.",
        "details": "Biologics cannot typically undergo terminal heat sterilization, placing heightened regulatory focus on closed-system processing, single-use integrity, and hold-time bioburden validation.",
        "source_label": "FDA Aseptic Processing of Biological Products",
        "source_url": "https://www.fda.gov/files/drugs/published/Aseptic-Processing-of-Biological-Products--Current-Regulatory-Issues--Candace-Gomez-Broughton--PhD.pdf",
    },
    {
        "id": "micro-iso-13408-aseptic-consensus",
        "section": "aseptic_sterility_assurance",
        "title": "ISO 13408 Aseptic Processing Series (Filtration, Lyophilization, CIP/SIP & Isolators)",
        "badge": "ISO 13408-1",
        "summary": "FDA-recognized consensus standard series covering general aseptic processing requirements plus specialized parts for sterilizing filtration, lyophilization, CIP/SIP, and isolator systems.",
        "details": "FDA updated its recognition to ISO 13408-1 Third Edition (2023-08), with transition cutoffs through December 2026 for premarket declarations of conformity.",
        "source_label": "FDA Recognized Consensus Standards: ISO 13408-1",
        "source_url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfstandards/detail.cfm?standard__identification_no=44754",
    },
    {
        "id": "micro-aseptic-guidance-pdf",
        "section": "aseptic_sterility_assurance",
        "title": "Media Fills (APS), Time Limits & Sterilizing Filtration Controls",
        "badge": "Media Fills",
        "summary": "Aseptic Process Simulations (media fills) challenge worst-case interventions, shift changes, and container sizes using growth media to verify zero-contamination aseptic capability.",
        "details": "Paired with pre-use/post-use sterilizing filter integrity testing (bubble point/diffusive flow) and validated hold times between compounding, filtration, and filling.",
        "source_label": "FDA Aseptic Processing Guidance PDF",
        "source_url": "https://www.fda.gov/media/71026/download",
    },
    # --- 2. Pyrogen & Bacterial Endotoxins Testing ---
    {
        "id": "micro-pyrogen-endotoxins-2026-qa",
        "section": "endotoxins_pyrogens_rfc",
        "title": "Pyrogen and Endotoxins Testing: Q&A (March 2026 Revision)",
        "badge": "USP <85>/<161>",
        "summary": "Final FDA guidance covering testing recommendations and acceptance criteria across USP <85> Bacterial Endotoxins Test, USP <161> Medical Devices, and AAMI ST72.",
        "details": "Addresses gel-clot, photometric, and kinetic chromogenic/turbidimetric test methods, sample pooling, retesting after out-of-specification results, and rabbit pyrogen alternatives.",
        "source_label": "FDA Pyrogen & Endotoxins Testing Q&A",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pyrogen-and-endotoxins-testing-questions-and-answers",
    },
    {
        "id": "micro-usp-86-recombinant-rfc",
        "section": "endotoxins_pyrogens_rfc",
        "title": "USP <86> Recombinant Reagents (rFC / rCR) Replacing Horseshoe Crab LAL",
        "badge": "USP <86> NAM",
        "summary": "FDA's March 2026 Level 2 revision aligns with USP Chapter <86> (published May 2025) to support non-animal recombinant Factor C and recombinant cascade reagents for endotoxin testing.",
        "details": "Sponsors must review the supplier's primary validation package and run product-specific suitability experiments based on material complexity before transitioning from animal-derived LAL.",
        "source_label": "FDA Clarifies Current Thinking on Recombinant Endotoxin Reagents",
        "source_url": "https://www.fda.gov/science-research/advancing-alternative-methods-fda/fda-clarifies-current-thinking-pyrogen-and-endotoxins-testing",
    },
    {
        "id": "micro-endotoxin-specification-ptc",
        "section": "endotoxins_pyrogens_rfc",
        "title": "Calculating Bacterial Endotoxins Specifications (K/M Formula)",
        "badge": "EU/kg/hr",
        "summary": "Endotoxin acceptance limits are derived from the threshold pyrogenic dose K (e.g., 5 EU/kg for non-intrathecal parenterals, 0.2 EU/kg intrathecal) divided by maximum hourly human dose M.",
        "details": "Requires careful verification of maximum dose per kg/hour, reconstitution diluents, co-administered products, and Maximum Valid Dilution (MVD) to prevent false negatives.",
        "source_label": "FDA Bacterial Endotoxins Specification Points to Consider",
        "source_url": "https://www.fda.gov/media/183132/download",
    },
    {
        "id": "micro-endotoxin-investigational-drugs",
        "section": "endotoxins_pyrogens_rfc",
        "title": "Setting Endotoxin Limits During Investigational Drug Development",
        "badge": "IND Phase 1–3",
        "summary": "Provides recommendations for establishing clinically safe endotoxin specifications during IND development so early-phase batches do not exceed USP <85> pyrogenic thresholds.",
        "details": "Accounts for dose-escalation cohorts where the maximum Phase 1 dose may increase and requires tightening specifications or adjusting MVD accordingly.",
        "source_label": "FDA Setting Endotoxin Limits for Investigational Drugs",
        "source_url": "https://www.fda.gov/media/140410/download",
    },
    {
        "id": "micro-low-endotoxin-recovery-ler",
        "section": "endotoxins_pyrogens_rfc",
        "title": "Low Endotoxin Recovery (LER) & Hold-Time Spiking Studies",
        "badge": "LER Biologics",
        "summary": "Chelators and surfactants (e.g., citrate/polysorbate buffers) in biologics can mask spiked endotoxin over hold time; FDA expects undiluted product spiking studies to detect LER.",
        "details": "Control Standard Endotoxin (CSE) or Reference Standard Endotoxin (RSE) is spiked into undiluted product and tested across hold intervals to verify recoverable activity.",
        "source_label": "FDA Pyrogen & Endotoxins Testing PDF",
        "source_url": "https://www.fda.gov/files/drugs/published/Pyrogen-and-Endotoxins-Testing--Questions-and-Answers.pdf",
    },
    {
        "id": "micro-nams-animal-alternatives-2026",
        "section": "endotoxins_pyrogens_rfc",
        "title": "FDA NAMs Initiative & Phasing Out Rabbit Pyrogen Testing (USP <151>)",
        "badge": "3Rs / NAMs",
        "summary": "Part of FDA's March 2026 New Approach Methodologies (NAMs) push to reduce, refine, and replace animal testing—pairing recombinant endotoxin assays with Monocyte Activation Tests (MAT).",
        "details": "Replaces legacy rabbit pyrogen testing (21 CFR 610.13(b) / USP <151>) with validated in vitro non-animal assays for both endotoxin and non-endotoxin pyrogens.",
        "source_label": "FDA Alternatives to Animal Testing Announcement",
        "source_url": "https://www.fda.gov/news-events/press-announcements/fda-releases-draft-guidance-alternatives-animal-testing-drug-development",
    },
    # --- 3. Container Closure Integrity Testing (CCIT, USP <1207>) & Sterility ---
    {
        "id": "micro-ccit-in-lieu-of-sterility",
        "section": "ccit_stability_sterility",
        "title": "Container and Closure System Integrity Testing in Lieu of Sterility Testing",
        "badge": "Stability CCIT",
        "summary": "FDA permits replacing destructive sterility testing at stability time points (other than initial batch release) with a scientifically validated Container Closure Integrity Test (CCIT).",
        "details": "CCIT must be performed annually and at expiration (or per applicable regulation) and proven capable of detecting breaches that could permit microbial ingress.",
        "source_label": "FDA CCIT in Lieu of Sterility Testing Guidance",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/container-and-closure-system-integrity-testing-lieu-sterility-testing-component-stability-protocol",
    },
    {
        "id": "micro-usp-1207-deterministic-leak",
        "section": "ccit_stability_sterility",
        "title": "USP <1207> Deterministic Leak Test Technologies vs. Dye Ingress",
        "badge": "USP <1207.2>",
        "summary": "USP <1207>, <1207.1>, and <1207.2> categorize packaging integrity methods, favoring deterministic physical technologies (vacuum decay, HVLD, laser headspace) over probabilistic dye/microbial ingress.",
        "details": "Deterministic methods provide quantitative, non-destructive detection limits calibrated against positive-control micro-leaks (e.g., laser-drilled holes) across the product lifecycle.",
        "source_label": "FDA Stability Testing Guidance Compilation (USP <1207>)",
        "source_url": "https://www.fda.gov/animal-veterinary/new-animal-drug-applications/compilation-fda-guidance-and-resources-stability-testing-animal-drug-products-and-drug-substances",
    },
    {
        "id": "micro-ccs-microbial-barrier",
        "section": "ccit_stability_sterility",
        "title": "Container Closure Systems (CCS) Microbial Barrier Throughout Shelf Life",
        "badge": "2024/2026 CCS",
        "summary": "Sterility testing at batch release (T=0) alone is insufficient to prove microbial barrier integrity; CCS qualification must demonstrate seal integrity across shipping, cold storage, and expiry.",
        "details": "Evaluates vial-stopper-cap crimping residual seal force (RSF), syringe plunger movement under air-transport pressure changes, and elastomeric closure shrinkage at -80 °C.",
        "source_label": "FDA Container Closure Systems Draft Guidance",
        "source_url": "https://www.fda.gov/media/194220/download",
    },
    {
        "id": "micro-ccit-stability-pdf",
        "section": "ccit_stability_sterility",
        "title": "Batch Release Sterility (USP <71>) vs. Stability Protocol Integrity",
        "badge": "USP <71>",
        "summary": "CCIT cannot replace USP <71> / 21 CFR 610.12 product sterility testing prior to batch release, but serves as a superior stability-indicating safeguard against post-release seal failure.",
        "details": "Because USP <71> samples only a tiny fraction of a lot and is insensitive to low-level contamination, pairing release sterility with 100% deterministic CCIT strengthens assurance.",
        "source_label": "FDA CCIT Stability Protocol Guidance PDF",
        "source_url": "https://www.fda.gov/media/76338/download",
    },
    {
        "id": "micro-biotech-ich-q5c-stability",
        "section": "ccit_stability_sterility",
        "title": "Biotechnological Stability & Multi-Dose In-Use Microbial Protection",
        "badge": "ICH Q5C / In-Use",
        "summary": "Multi-dose injectable and ophthalmic containers require simulated in-use puncture and antimicrobial effectiveness testing (AET, USP <51>) to justify post-puncture beyond-use dating.",
        "details": "In-use hold times (e.g., use within 7 days of first puncture) must be supported by microbiological challenge and physicochemical stability data.",
        "source_label": "FDA CCIT & ICH Biologics Stability Reference",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/container-and-closure-system-integrity-testing-lieu-sterility-testing-component-stability-protocol",
    },
    {
        "id": "micro-device-pyrogen-sterility-510k",
        "section": "ccit_stability_sterility",
        "title": "Sterile & Non-Pyrogenic Delivery Devices (USP <161> & SAL 10^-6)",
        "badge": "SAL 10^-6",
        "summary": "Sterile drug-delivery devices and combination product components require Sterility Assurance Level (SAL) 10^-6 validation and USP <161> endotoxin limits (e.g., <= 20 EU/device; <= 2.15 EU/device CSF).",
        "details": "Ensures prefilled syringes, autoinjectors, and infusion sets meet non-pyrogenic and sterile barrier claims alongside the drug formulation.",
        "source_label": "FDA Premarket Non-Pyrogenic Device Guidance",
        "source_url": "https://www.fda.gov/media/95770/download",
    },
    # --- 4. Non-Sterile Microbiology, Burkholderia cepacia & QC Labs ---
    {
        "id": "micro-nonsterile-nsd-guidance",
        "section": "nonsterile_bcc_micro_lab",
        "title": "Microbiological Quality Considerations in Non-Sterile Drug Products",
        "badge": "NSD Guidance",
        "summary": "Covers CGMP controls (21 CFR 211.110, 211.111, 211.113(a)) to control bioburden and prevent objectionable microorganisms in aqueous and non-aqueous non-sterile drugs (NSDs).",
        "details": "Highlights naturally derived raw materials and pharmaceutical water systems as primary bioburden contributors requiring component testing and microbial risk assessment.",
        "source_label": "FDA Non-Sterile Drug Microbiological Quality Guidance",
        "source_url": "https://www.fda.gov/media/152527/download",
    },
    {
        "id": "micro-burkholderia-cepacia-usp60",
        "section": "nonsterile_bcc_micro_lab",
        "title": "Burkholderia cepacia Complex (BCC) Control & USP <60> Testing",
        "badge": "USP <60> BCC",
        "summary": "BCC is an opportunistic waterborne pathogen group capable of surviving in preserved aqueous non-sterile drugs (oral liquids, nasal sprays, topicals), prompting major recalls.",
        "details": "FDA expects sponsors to perform USP <60> testing and establish manufacturing, water-system, and raw-material controls to prevent BCC contamination.",
        "source_label": "FDA Non-Sterile Drug Draft Guidance (BCC)",
        "source_url": "https://www.fda.gov/media/174244/download",
    },
    {
        "id": "micro-bcc-water-systems-case",
        "section": "nonsterile_bcc_micro_lab",
        "title": "Pharmaceutical Water Systems & Biofilm Root-Cause Investigations",
        "badge": "Water / Biofilm",
        "summary": "CDER case studies show Burkholderia multivorans and BCC proliferate in poorly sanitized purified water loops, dead legs, and deionized resin beds before seeding finished NSDs.",
        "details": "Prevention requires continuous turbulent flow, hot-loop or ozone sanitization, routine USP <1231> water bioburden trending, and immediate CAPA on alert/action excursions.",
        "source_label": "FDA CDER Burkholderia Microbial Investigation Case Study",
        "source_url": "https://www.fda.gov/files/drugs/published/CDER-Case-Study--A-Microbial-Investigation-of-Contamination-by-Burkholderia-multivorans--John-Metcalfe--PhD.pdf",
    },
    {
        "id": "micro-pharmaceutical-microbiology-manual",
        "section": "nonsterile_bcc_micro_lab",
        "title": "FDA Pharmaceutical Microbiology Manual (ORA.007)",
        "badge": "ORA Manual",
        "summary": "Standardizes FDA field laboratory procedures for sterility testing, aseptic sample handling, bacterial endotoxin testing, microbial limits (USP <61>/<62>), and preservative efficacy.",
        "details": "Details biosafety cabinet disinfection, container exterior sanitization, environmental air plates during lab testing, and antimicrobial neutralization.",
        "source_label": "FDA Pharmaceutical Microbiology Manual",
        "source_url": "https://www.fda.gov/media/88801/download",
    },
    {
        "id": "micro-method-validation-micro",
        "section": "nonsterile_bcc_micro_lab",
        "title": "Microbiological Method Validation & Rapid Microbial Methods (RMM)",
        "badge": "Validation / RMM",
        "summary": "Validation of classical and alternative rapid microbiological methods requires demonstrating specificity, limit of detection, ruggedness, and non-inferiority vs. compendial reference methods.",
        "details": "Supports faster batch release and in-process bioburden feedback for short-shelf-life biologics and cell/gene therapies under 21 CFR 610.9 equivalence.",
        "source_label": "FDA Guidelines for Validation of Microbiological Methods",
        "source_url": "https://www.fda.gov/media/83812/download",
    },
    {
        "id": "micro-bcc-recall-decision-history",
        "section": "nonsterile_bcc_micro_lab",
        "title": "Objectionable Organisms Beyond USP <61>/<62> Indicator Species",
        "badge": "21 CFR 211.113(a)",
        "summary": "Passing USP <61> total aerobic count and <62> specified organism screens does not guarantee safety if an unmonitored objectionable organism (like BCC) compromises vulnerable patients.",
        "details": "Firms must evaluate risk based on route of administration, intended patient population (infants, ICU, immunocompromised), and preservative system robustness.",
        "source_label": "FDA Burkholderia cepacia Safety Assessment",
        "source_url": "https://www.fda.gov/files/about%20fda/published/Burkholderia-cepacia--This-Decision-Is-Overdue-(PDF-%E2%80%93-285KB).pdf",
    },
]


def build_microbiology_sterility(out_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked": CHECKED,
        "title": "Pharmaceutical Microbiology, Sterility Assurance, Endotoxin (LAL / rFC) & CCIT",
        "subtitle": "Aseptic processing (21 CFR 211.113), USP <85>/<86> recombinant endotoxin testing, USP <1207> deterministic CCIT, and non-sterile BCC (USP <60>) controls.",
        "sections": SECTIONS,
        "entries": ENTRIES,
        "counts": {
            "sections": len(SECTIONS),
            "entries": len(ENTRIES),
        },
    }
    out_path = out_dir / "microbiology_sterility.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv=None) -> int:
    out_dir = pathlib.Path(argv[1]) if argv and len(argv) > 1 else pathlib.Path("site/data")
    res = build_microbiology_sterility(out_dir)
    print(f"Built {out_dir / 'microbiology_sterility.json'} ({res['counts']['entries']} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
'''

MICROBIOLOGY_STERILITY_JS = r'''import { getJSON } from "./data.js";
import { esc } from "./ui.js";

const MICRO_SVG = `
<svg viewBox="0 0 760 150" role="img" aria-label="Pharmaceutical microbiology sterility assurance workflow from cleanroom and water controls to endotoxin testing, CCIT, and sterile release" style="width:100%;max-width:760px;height:auto;display:block;margin:1rem auto;">
  <rect x="8" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="92" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">1. Contamination Control</text>
  <text x="92" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">ISO 5–8 Cleanrooms</text>
  <text x="92" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">Media Fills (APS)</text>
  <text x="92" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">USP &lt;1231&gt; Water / BCC</text>

  <line x1="176" y1="71" x2="198" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="198,66 208,71 198,76" fill="var(--accent)"/>

  <rect x="208" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="292" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">2. Endotoxins &amp; Pyrogens</text>
  <text x="292" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">USP &lt;85&gt; LAL</text>
  <text x="292" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">USP &lt;86&gt; rFC / rCR</text>
  <text x="292" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">LER Hold Studies</text>

  <line x1="376" y1="71" x2="398" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="398,66 408,71 398,76" fill="var(--accent)"/>

  <rect x="408" y="18" width="168" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="492" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">3. Integrity (CCIT)</text>
  <text x="492" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">USP &lt;1207&gt; Leak Test</text>
  <text x="492" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">HVLD / Vacuum Decay</text>
  <text x="492" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">Annual Stability CCIT</text>

  <line x1="576" y1="71" x2="598" y2="71" stroke="var(--accent)" stroke-width="2"/>
  <polygon points="598,66 608,71 598,76" fill="var(--accent)"/>

  <rect x="608" y="18" width="144" height="106" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>
  <text x="680" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">4. QC Release</text>
  <text x="680" y="66" text-anchor="middle" font-size="11" fill="var(--muted)">USP &lt;71&gt; Sterility</text>
  <text x="680" y="83" text-anchor="middle" font-size="11" fill="var(--muted)">USP &lt;60&gt;/&lt;61&gt;/&lt;62&gt;</text>
  <text x="680" y="100" text-anchor="middle" font-size="11" fill="var(--muted)">SAL 10^-6 / RMM</text>
</svg>`;

export async function microbiologySterilityPage(view, mode = "ref") {
  view.innerHTML = `<div class="panel" style="background:var(--paper);padding:1.25rem;border:1px solid var(--line);border-radius:10px;"><p>Loading Pharmaceutical Microbiology &amp; Sterility Assurance reference…</p></div>`;
  const data = await getJSON("data/microbiology_sterility.json");
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
          <a href="#/${isExplore ? "ref" : "explore"}/microbiology-sterility" style="padding:0.4rem 0.8rem;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);text-decoration:none;font-size:0.9rem;">
            ${isExplore ? "Switch to Reference →" : "← Switch to Explore"}
          </a>
        </div>
        ${MICRO_SVG}
        <div style="display:flex;flex-wrap:wrap;gap:0.45rem;margin-top:0.75rem;">${pills}</div>
      </section>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:0.9rem;">
        ${cards}
      </div>
      <p style="margin-top:1rem;font-size:0.82rem;color:var(--muted);">Checked ${esc(data.checked)} against primary FDA &amp; USP regulatory sources.</p>
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
    imp = 'import { microbiologySterilityPage } from "./microbiology_sterility.js";\n'
    if "microbiologySterilityPage" not in txt:
        txt = imp + txt
        changed = True
    route_snip = (
        '  if (path === "/ref/microbiology-sterility") return microbiologySterilityPage(view, "ref");\n'
        '  if (path === "/explore/microbiology-sterility") return microbiologySterilityPage(view, "explore");\n'
    )
    if '"/ref/microbiology-sterility"' not in txt:
        for anchor in (
            'if (path === "/ref/pv-faers-sentinel")',
            'if (path === "/ref/user-fees-prv")',
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
    ref_entry = '      { label: "Microbiology, Endotoxins & CCIT", href: "#/ref/microbiology-sterility" },\n'
    if "#/ref/microbiology-sterility" not in txt:
        anchor = '{ label: "Pharmacovigilance & Sentinel", href: "#/ref/pv-faers-sentinel" },'
        if anchor in txt:
            txt = txt.replace(anchor, anchor + "\n" + ref_entry.rstrip("\n"), 1)
            changed = True
        elif "REF_NAV_GROUPS" in txt:
            txt = txt.replace("];", ref_entry + "];", 1)
            changed = True
    exp_entry = '  { label: "Microbiology, Endotoxins & CCIT", href: "#/explore/microbiology-sterility" },\n'
    if "#/explore/microbiology-sterility" not in txt:
        anchor = '{ label: "Pharmacovigilance & Sentinel", href: "#/explore/pv-faers-sentinel" },'
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
    line = "python3 pipeline/build_microbiology_sterility.py site/data\n"
    if "build_microbiology_sterility.py" not in txt:
        anchor = "python3 pipeline/build_pv_faers_sentinel.py site/data\n"
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
    if "/api/microbiology-sterility" in txt:
        return False
    block = (
        '\n@app.get("/api/microbiology-sterility")\n'
        'def api_microbiology_sterility():\n'
        '    return _read_site_json("data/microbiology_sterility.json")\n'
    )
    path.write_text(txt.rstrip() + "\n" + block, encoding="utf-8")
    return True


def _patch_global_search(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "microbiology_sterility.json" in txt:
        return False
    snippet = (
        '\n    micro_path = data_dir / "microbiology_sterility.json"\n'
        '    if micro_path.is_file():\n'
        '        micro_obj = json.loads(micro_path.read_text(encoding="utf-8"))\n'
        '        for item in micro_obj.get("entries", []):\n'
        '            entries.append({\n'
        '                "id": item["id"],\n'
        '                "title": item["title"],\n'
        '                "subtitle": f"Microbiology & Sterility · {item.get(\'badge\', \'\')}",\n'
        '                "kind": "Microbiology & Sterility",\n'
        '                "href": "#/ref/microbiology-sterility",\n'
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
    if "microbiology-sterility" in txt:
        return False
    snippet = (
        '\n    micro_file = data_dir / "microbiology_sterility.json"\n'
        '    if micro_file.is_file():\n'
        '        micro_d = json.loads(micro_file.read_text(encoding="utf-8"))\n'
        '        _write_landing(\n'
        '            site_dir / "microbiology-sterility" / "index.html",\n'
        '            "Pharmaceutical Microbiology, Sterility Assurance, Endotoxin & CCIT | Pill by Pill",\n'
        '            micro_d.get("subtitle", ""),\n'
        '            "#/ref/microbiology-sterility",\n'
        '            micro_d.get("entries", []),\n'
        '        )\n'
        '        written_urls.append(f"{BASE_URL}/microbiology-sterility/")\n'
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
    if "#/ref/microbiology-sterility" in txt:
        return False
    addition = '    "#/ref/microbiology-sterility",\n    "#/explore/microbiology-sterility",\n'
    anchor = '"#/ref/pv-faers-sentinel",'
    if anchor in txt:
        txt = txt.replace(anchor, anchor + "\n" + addition.rstrip("\n"), 1)
        path.write_text(txt, encoding="utf-8")
        return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    root = pathlib.Path(root)
    changed = {}
    changed["build_microbiology_sterility.py"] = _write_if_changed(
        root / "pipeline" / "build_microbiology_sterility.py", BUILD_MICROBIOLOGY_STERILITY_PY
    )
    changed["microbiology_sterility.js"] = _write_if_changed(
        root / "site" / "js" / "microbiology_sterility.js", MICROBIOLOGY_STERILITY_JS
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
        (root / "site" / "js" / "app.js").write_text('if (path === "/ref/pv-faers-sentinel") return x;\nroute();\n', encoding="utf-8")
        (root / "site" / "js" / "layout.js").write_text('const REF_NAV_GROUPS = [\n  { label: "Pharmacovigilance & Sentinel", href: "#/ref/pv-faers-sentinel" },\n];\nconst EXPLORE_NAV = [\n  { label: "Pharmacovigilance & Sentinel", href: "#/explore/pv-faers-sentinel" },\n];\n', encoding="utf-8")
        (root / "pipeline" / "run_all.sh").write_text('#!/bin/sh\npython3 pipeline/build_pv_faers_sentinel.py site/data\n', encoding="utf-8")
        (root / "app.py").write_text('from fastapi import FastAPI\napp = FastAPI()\n', encoding="utf-8")
        (root / "pipeline" / "build_global_search.py").write_text('def f():\n    payload = {"checked": CHECKED, "entries": entries}\n', encoding="utf-8")
        (root / "pipeline" / "build_v60_static_pages.py").write_text('def f():\n    written_urls = []\n', encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('ROUTES = [\n    "#/ref/pv-faers-sentinel",\n]\n', encoding="utf-8")

        res1 = apply_patch(root)
        assert all(res1.values()), f"Expected all changed on first run: {res1}"
        res2 = apply_patch(root)
        assert not any(res2.values()), f"Expected idempotent second run: {res2}"

        subprocess.run([sys.executable, str(root / "pipeline" / "build_microbiology_sterility.py"), str(root / "site" / "data")], check=True)
        data = json.loads((root / "site" / "data" / "microbiology_sterility.json").read_text(encoding="utf-8"))
        assert len(data["sections"]) == 4
        assert len(data["entries"]) == 24
        for sec in data["sections"]:
            cnt = sum(1 for e in data["entries"] if e["section"] == sec["id"])
            assert cnt == 6, f"Section {sec['id']} count {cnt} != 6"
        for e in data["entries"]:
            assert e["source_url"].startswith("https://"), f"Non-HTTPS URL: {e['source_url']}"
        js_txt = (root / "site" / "js" / "microbiology_sterility.js").read_text(encoding="utf-8")
        assert "--card" not in js_txt
        assert "./dom.js" not in js_txt
        assert "./ui.js" in js_txt
        app_js_txt = (root / "site" / "js" / "app.js").read_text(encoding="utf-8")
        assert app_js_txt.index('"/ref/microbiology-sterility"') < app_js_txt.index("route();")
        print("V62W_MICROBIOLOGY_STERILITY_SELFTEST_PASSED")


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
