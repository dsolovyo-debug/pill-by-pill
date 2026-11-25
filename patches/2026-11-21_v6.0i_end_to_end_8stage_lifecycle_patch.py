#!/usr/bin/env python3
"""Pill by Pill v6.0i Patch: Complete 8-Stage End-to-End Drug Lifecycle Encyclopedia (Conception -> Distribution & Safety).

Expands the Pharmaceutical Encyclopedia from 4 R&D/CMC departments to a complete 8-stage
end-to-end lifecycle covering Science, Tools, Regulations, and Economics:
  1. Discovery & Preclinical R&D (`discovery`)
  2. Formulation Development & Routes (`formulation`)
  3. Analytical Development & QC (`analytical`)
  4. Clinical Development & Trials — Phase 1–3 (`clinical`)          [NEW]
  5. Regulatory Affairs, Submission & Approval (`regulatory`)        [NEW]
  6. Commercial Manufacturing & Bioprocessing (`manufacturing`)
  7. IP, Health Economics, Pricing & Market Access (`commercial`)    [NEW]
  8. Supply Chain, Cold-Chain Distribution & Safety (`distribution`) [NEW]

Updates:
  1. `pipeline/build_departments.py`: Appends the 4 new complete lifecycle departments (sorted by `order`).
  2. `site/js/departments.js`: Upgrades `renderLifecycleSvg` from 4 boxes to a clickable 2-row,
     8-stage end-to-end visual lifecycle map.
  3. `tests/test_v60.py`: Updates department count assertion to `>= 8` complete departments.
  4. `tests/test_v60_site.py`: Adds the 4 new department routes to browser/WCAG route checks.
  (Note: `pipeline/build_v60_static_pages.py` automatically generates static SEO landing pages
   and sitemap entries for all 8 departments dynamically.)

Usage:
  python3 2026-11-21_v6.0i_end_to_end_8stage_lifecycle_patch.py --selftest
  python3 2026-11-21_v6.0i_end_to_end_8stage_lifecycle_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

NEW_DEPARTMENTS_4 = [{'id': 'clinical', 'name': 'Clinical Development & Trials (Phase 1–3)', 'order': 4, 'status': 'complete', 'plain_summary': 'Tests whether an experimental medicine is safe and actually helps patients in carefully monitored human studies, moving from a few dozen volunteers to thousands of patients.', 'technical_summary': 'Designs, executes, and analyzes human clinical investigations under IND (21 CFR Part 312) and ICH E6 Good Clinical Practice (GCP), spanning Phase 1 safety/PK, Phase 2 proof-of-concept/dose-ranging, and Phase 3 pivotal randomized controlled trials.', 'workflows': [{'step': '1. IND Clearance & Phase 1 First-in-Human (FIH)', 'plain': 'Before testing a new drug in people, sponsors submit all lab and animal safety data to the FDA for a 30-day safety check. Phase 1 tests tiny escalating doses in 20–100 people to check safety and how the body clears the drug.', 'technical': 'IND filing under 21 CFR Part 312 (30-day FDA safety review / clinical hold check). Single- and multiple-ascending dose (SAD/MAD) studies establish safety, tolerability, PK/PD, and maximum tolerated dose (MTD) in healthy volunteers or target oncology/rare-disease patients.'}, {'step': '2. Phase 2 Proof-of-Concept & Dose-Ranging', 'plain': 'Tests the medicine in a few hundred patients with the actual condition to see if it works and to pick the right dose. Most experimental medicines fail at this stage.', 'technical': 'Evaluates clinical efficacy signals, biomarker/surrogate endpoints, dose-response curves, and short-term safety (typically 100–300 patients). Historically represents the single highest attrition bottleneck in clinical development.'}, {'step': '3. Phase 3 Pivotal Randomized Controlled Trials', 'plain': 'Large studies in hundreds to thousands of patients comparing the new medicine against standard treatment or a placebo across hospitals worldwide, overseen by independent ethics and safety boards.', 'technical': 'Adequate and well-controlled multicenter double-blind RCTs powered for primary clinical endpoints, overseen by Institutional Review Boards (IRBs) and independent Data Safety Monitoring Boards (DSMBs) under ICH E6(R2)/E6(R3) GCP.'}, {'step': '4. Clinical Operations Tools, CROs & Trial Economics', 'plain': 'Running global trials relies on specialized software to track patient data and independent research companies (CROs) to manage hospital sites—making clinical trials the most expensive part of building a drug.', 'technical': 'Core software stack includes Electronic Data Capture (EDC), Clinical Trial Management Systems (CTMS), Electronic Trial Master File (eTMF), Interactive Response Technology (IRT/RTSM), and ClinicalTrials.gov registration. Executed via internal teams or Contract Research Organizations (CROs); clinical phases drive the majority of capitalized R&D expenditure and timeline risk.'}], 'equipment_ids': ['eq-lc-ms-ms', 'eq-hplc-uplc'], 'sources': [{'label': 'FDA — Step 3: Clinical Research', 'url': 'https://www.fda.gov/patients/drug-development-process/step-3-clinical-research'}, {'label': 'eCFR — 21 CFR Part 312 (Investigational New Drug Application)', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312'}]}, {'id': 'regulatory', 'name': 'Regulatory Affairs, Submission & Approval', 'order': 5, 'status': 'complete', 'plain_summary': 'Assembles every lab test, factory plan, and clinical trial result into an official application for health authorities like the FDA, EMA, and PMDA to review before a medicine can be prescribed.', 'technical_summary': 'Manages agency interactions, electronic Common Technical Document (eCTD) dossier assembly (Modules 1–5), statutory review pathways (NDA, BLA, ANDA, Biosimilar), user-fee timelines (PDUFA/BsUFA/GDUFA), and global regulatory harmonization.', 'workflows': [{'step': '1. Pre-Submission Agency Alignment', 'plain': 'Developers meet with regulators at key checkpoints—before human trials, after Phase 2, and before filing—to agree on trial designs and manufacturing evidence.', 'technical': 'Formal milestone meetings (Pre-IND, End-of-Phase 2, Pre-NDA/BLA) establish agreement on pivotal endpoints, statistical analysis plans, pediatric study plans (PREA/PIP), and CMC stability packages.'}, {'step': '2. eCTD Dossier Assembly & Statutory Pathways', 'plain': 'All data is organized into a standardized digital dossier covering quality, animal studies, and human trials. Different legal pathways apply to brand-new drugs, biologics, generics, and biosimilars.', 'technical': 'Standardized ICH M4 eCTD structure (Modules 1–5) submitted under 21 CFR Part 314 (NDA 505(b)(1), 505(b)(2), ANDA 505(j)) or PHS Act § 351 (BLA 351(a), Biosimilar 351(k)), compiled via regulatory information management (RIM) and eCTD publishing tools.'}, {'step': '3. Expedited Pathways, User Fees & Review', 'plain': 'For serious unmet diseases, regulators can speed up review. Drug companies pay statutory user fees that fund agency review teams to hit strict decision deadlines.', 'technical': 'FDA expedited programs (Fast Track, Breakthrough Therapy, Accelerated Approval, Priority Review) operate alongside PDUFA/BsUFA/GDUFA user-fee performance clocks (typically 10 months standard / 6 months priority), advisory committee reviews, labeling negotiation, and pre-approval facility inspections (PAI).'}, {'step': '4. Multi-Region Filing & Global Harmonization', 'plain': 'A medicine approved in the US still needs separate approvals in Europe, Japan, Canada, and other countries—though agencies increasingly coordinate reviews.', 'technical': 'Parallel and reliance filings across US FDA, EU EMA (Centralised Procedure), Japan PMDA, Health Canada, UK MHRA, and Australia TGA, leveraging ICH technical guidelines and collaborative frameworks such as FDA Project Orbis and the Access Consortium.'}], 'equipment_ids': [], 'sources': [{'label': 'eCFR — 21 CFR Part 314 (Applications for FDA Approval to Market a New Drug)', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314'}, {'label': 'FDA — Step 3 & Step 5 Drug Development Process', 'url': 'https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring'}]}, {'id': 'commercial', 'name': 'IP, Health Economics, Pricing & Market Access', 'order': 7, 'status': 'complete', 'plain_summary': 'Explains how patents protect new medicines temporarily, how governments and insurers decide what a drug is worth and whether to cover it, and the rules governing how medicines can be marketed.', 'technical_summary': 'Covers pharmaceutical intellectual property and statutory exclusivities, Health Economics & Outcomes Research (HEOR), global HTA reimbursement appraisals, US gross-to-net payer economics, medical affairs, and FDA promotional compliance.', 'workflows': [{'step': '1. Patents & Regulatory Exclusivities', 'plain': 'Patents give inventors a temporary window to recoup R&D costs before generic or biosimilar copies enter at much lower prices. Regulatory exclusivities run alongside patents.', 'technical': 'Layered patent estates (composition of matter, method of use, formulation, polymorph, manufacturing process) listed in the FDA Orange Book (small molecules; Hatch-Waxman Patent Term Extension, 5-yr NCE / 7-yr Orphan exclusivity) or Purple Book (biologics; BPCIA 12-yr reference product exclusivity).'}, {'step': '2. Health Economics (HEOR) & Global HTA', 'plain': 'In many countries, regulatory approval is only half the battle—health agencies also measure whether a new medicine delivers enough extra health benefit to justify its price.', 'technical': 'Health Economics & Outcomes Research (HEOR) models cost-effectiveness (QALYs, ICERs) and budget impact for national HTA bodies including UK NICE, Germany G-BA/IQWiG (AMNOG), France HAS, Australia PBAC, Canada CDA-AMC, and independent US ICER.'}, {'step': '3. Pricing, Payers & Gross-to-Net Economics', 'plain': "A drug's published list price is rarely what insurers or governments actually pay—rebates, pharmacy benefit managers (PBMs), and statutory discounts create a wide gap between list and net price.", 'technical': 'Commercial access spans Wholesale Acquisition Cost (WAC), PBM formulary tiering and rebates, 340B Drug Pricing Program discounts, Medicaid Best Price, Medicare Part B ASP / Part D formulary structure, and CMS Medicare Drug Price Negotiation Program Maximum Fair Prices.'}, {'step': '4. Medical Affairs & Promotional Compliance', 'plain': 'Doctors learn about new medicines through clinical publications and medical science liaisons, while drug advertising is tightly policed by law so companies cannot promote unapproved uses.', 'technical': 'Medical Affairs and Medical Science Liaisons (MSLs) handle non-promotional scientific exchange and real-world evidence (RWE) generation; commercial advertising and promotional labeling are strictly regulated by FDA OPDP under 21 CFR Part 202 (fair balance, substantial evidence, prohibition of off-label promotion).'}], 'equipment_ids': [], 'sources': [{'label': 'CMS — Medicare Drug Price Negotiation Program', 'url': 'https://www.cms.gov/initiatives/medicare-prescription-drug-affordability/overview/medicare-drug-price-negotiation-program'}, {'label': 'FDA — Step 5: Drug Advertising & Generic Exclusivity', 'url': 'https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring'}]}, {'id': 'distribution', 'name': 'Supply Chain, Distribution & Post-Market Safety', 'order': 8, 'status': 'complete', 'plain_summary': 'Tracks how finished medicines move securely from factories through wholesalers, cold-chain trucks, and pharmacies to patients—and how regulators monitor safety and shortages for decades after launch.', 'technical_summary': 'Covers pharmaceutical 3PL and wholesale distribution, specialty pharmacy and REMS channels, cold-chain / ultra-low-temperature logistics, DSCSA serialization, post-market pharmacovigilance (AEMS/FAERS, EudraVigilance), recalls, and drug shortage monitoring.', 'workflows': [{'step': '1. 3PLs, Wholesalers & Specialty Channels', 'plain': 'Most pills flow from factories to national wholesalers and then to retail or hospital pharmacies, while complex biologics and rare-disease drugs move through specialty pharmacies and patient support hubs.', 'technical': 'Physical flow moves from manufacturer/CDMO to Third-Party Logistics (3PL) hubs, full-line wholesalers (e.g., McKesson, Cencora, Cardinal Health), retail/hospital pharmacies, buy-and-bill infusion clinics, or limited-distribution Specialty Pharmacies.'}, {'step': '2. Cold-Chain Logistics & DSCSA Track-and-Trace', 'plain': 'Temperature-sensitive biologics and vaccines require continuous cold-chain monitoring from factory to clinic, and every U.S. prescription package carries a unique scannable 2D barcode to block counterfeits.', 'technical': 'Qualified thermal shipping (2–8°C refrigerated, -20°C to -80°C ultra-low temperature, cryogenic LN2 for cell therapies) with continuous data loggers, paired with Drug Supply Chain Security Act (DSCSA) interoperable electronic unit-level serialization (2D DataMatrix GTIN/serial/lot/expiry).'}, {'step': '3. Post-Market Pharmacovigilance & REMS', 'plain': 'Safety monitoring never stops after approval: doctors, patients, and companies report side effects to national databases so regulators can update warnings, require safety programs, or issue recalls.', 'technical': 'Ongoing Phase 4 surveillance via FDA Adverse Event Monitoring System (AEMS / FAERS), EMA EudraVigilance, Risk Evaluation and Mitigation Strategies (REMS), routine and for-cause cGMP inspections, and Class I–III enforcement recalls.'}, {'step': '4. Lifecycle Management, Shortages & Loss of Exclusivity', 'plain': 'Over time companies add new uses or easier dosage forms, regulators track supply shortages, and when patents expire generic and biosimilar competition drops prices dramatically.', 'technical': 'Post-approval supplemental applications (sNDA/sBLA) for new indications or formulations, FDA Drug Shortages monitoring and supply-chain redundancy, and Loss of Exclusivity (LOE) transition to AB-rated generics (ANDA) and interchangeable biosimilars.'}], 'equipment_ids': ['eq-stability-chamber', 'eq-sterile-fill-finish'], 'sources': [{'label': 'FDA — Step 5: FDA Post-Market Drug Safety Monitoring', 'url': 'https://www.fda.gov/patients/drug-development-process/step-5-fda-post-market-drug-safety-monitoring'}, {'label': 'FDA — Drug Supply Chain Security Act (DSCSA) & Authority', 'url': 'https://www.fda.gov/media/77516/download'}]}]
LIFECYCLE_SVG_8STAGE_JS = 'export function renderLifecycleSvg(mode = "ref") {\n  const base = mode === "explore" ? "#/explore/departments/" : "#/ref/departments/";\n  const row1 = [\n    { id: "discovery", x: 10, label: "1. Discovery", sub: "Target & Preclinical" },\n    { id: "formulation", x: 175, label: "2. Formulation", sub: "Dosage & Routes" },\n    { id: "analytical", x: 340, label: "3. Analytical QC", sub: "Purity & Stability" },\n    { id: "clinical", x: 505, label: "4. Clinical Trials", sub: "Phase 1–3 & GCP" },\n  ];\n  const row2 = [\n    { id: "regulatory", x: 10, label: "5. Regulatory", sub: "IND, eCTD & Approval" },\n    { id: "manufacturing", x: 175, label: "6. Manufacturing", sub: "Scale-Up & cGMP" },\n    { id: "commercial", x: 340, label: "7. Economics & IP", sub: "Patents, HTA & Access" },\n    { id: "distribution", x: 505, label: "8. Distribution", sub: "Supply Chain & Safety" },\n  ];\n  return html`<figure class="lifecycle-map" aria-label="End-to-end pharmaceutical development and deployment lifecycle">\n    <svg viewBox="0 0 665 178" width="665" height="178" role="img" style="max-width:100%;height:auto;display:block">\n      ${row1.map((n, i) => html`\n        <a href="${base}${n.id}">\n          <rect x="${n.x}" y="8" width="150" height="66" rx="10" fill="var(--paper,#f8fafc)" stroke="var(--line,#94a3b8)" stroke-width="1.5"/>\n          <text x="${n.x + 75}" y="35" text-anchor="middle" font-size="13" font-weight="700" fill="currentColor">${n.label}</text>\n          <text x="${n.x + 75}" y="54" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.75">${n.sub}</text>\n        </a>\n        ${i < row1.length - 1 ? html`<line x1="${n.x + 150}" y1="41" x2="${n.x + 165}" y2="41" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n      <path d="M 580 74 L 580 89 L 85 89 L 85 102" fill="none" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>\n      ${row2.map((n, i) => html`\n        <a href="${base}${n.id}">\n          <rect x="${n.x}" y="102" width="150" height="66" rx="10" fill="var(--paper,#f8fafc)" stroke="var(--line,#94a3b8)" stroke-width="1.5"/>\n          <text x="${n.x + 75}" y="129" text-anchor="middle" font-size="13" font-weight="700" fill="currentColor">${n.label}</text>\n          <text x="${n.x + 75}" y="148" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.75">${n.sub}</text>\n        </a>\n        ${i < row2.length - 1 ? html`<line x1="${n.x + 150}" y1="135" x2="${n.x + 165}" y2="135" stroke="var(--accent,#cc2f5a)" stroke-width="2"/>` : ""}\n      `)}\n    </svg>\n    <figcaption class="muted small">Complete 8-stage drug lifecycle (conception to patient): click any stage to explore its science, tools, regulations, and economics.</figcaption>\n  </figure>`;\n}'


def _patch_build_departments(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"id": "clinical"' in txt and '"id": "distribution"' in txt:
        return False
    anchor = "def build_departments("
    if anchor not in txt:
        raise ValueError(f"Missing build_departments anchor in {path}")
    add_block = (
        "\n# v6.0i: Complete 8-stage end-to-end lifecycle departments (Science, Tools & Economics)\n"
        "_V60I_EXTRA_DEPARTMENTS = " + json.dumps(NEW_DEPARTMENTS_4, indent=4, ensure_ascii=False) + "\n"
        "if isinstance(DEPARTMENTS, list):\n"
        "    _existing_ids = {d.get('id') for d in DEPARTMENTS}\n"
        "    for _d in _V60I_EXTRA_DEPARTMENTS:\n"
        "        if _d['id'] not in _existing_ids:\n"
        "            DEPARTMENTS.append(_d)\n"
        "    DEPARTMENTS.sort(key=lambda d: d.get('order', 99))\n\n"
    )
    path.write_text(txt.replace(anchor, add_block + anchor, 1), encoding="utf-8")
    return True


def _patch_departments_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if "8. Distribution" in txt:
        return False
    pat = re.compile(r"export function renderLifecycleSvg\(.*?\n\}", re.DOTALL)
    if pat.search(txt):
        txt = pat.sub(LIFECYCLE_SVG_8STAGE_JS, txt, count=1)
        path.write_text(txt, encoding="utf-8")
        return True
    return False


def _patch_test_v60(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    for old, new in [
        ("self.assertEqual(len(depts), 4)", "self.assertGreaterEqual(len(depts), 8)"),
        ("assert len(depts) == 4", "assert len(depts) >= 8"),
    ]:
        if old in txt:
            txt = txt.replace(old, new, 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_test_v60_site(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"/#/ref/departments/distribution"' in txt:
        return False
    old = '    "/#/ref/departments/analytical",'
    new = (
        '    "/#/ref/departments/analytical",\n'
        '    "/#/ref/departments/clinical",\n'
        '    "/#/ref/departments/regulatory",\n'
        '    "/#/ref/departments/commercial",\n'
        '    "/#/ref/departments/distribution",'
    )
    if old in txt:
        path.write_text(txt.replace(old, new, 1), encoding="utf-8")
        return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    return {
        "build_departments_8stage": _patch_build_departments(root / "pipeline" / "build_departments.py"),
        "departments_js_8stage_svg": _patch_departments_js(root / "site" / "js" / "departments.js"),
        "test_v60_updated": _patch_test_v60(root / "tests" / "test_v60.py"),
        "test_v60_site_updated": _patch_test_v60_site(root / "tests" / "test_v60_site.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "site" / "data").mkdir(parents=True)
        (root / "tests").mkdir()

        (root / "pipeline" / "build_departments.py").write_text(
            "import json, pathlib, sys\n"
            "DEPARTMENTS = [\n"
            "    {'id': 'discovery', 'name': 'Discovery', 'order': 1, 'status': 'complete', 'workflows': [1,2,3,4], 'sources': []},\n"
            "    {'id': 'formulation', 'name': 'Formulation', 'order': 2, 'status': 'complete', 'workflows': [1,2,3,4], 'sources': []},\n"
            "    {'id': 'analytical', 'name': 'Analytical', 'order': 3, 'status': 'complete', 'workflows': [1,2,3,4], 'sources': []},\n"
            "    {'id': 'manufacturing', 'name': 'Manufacturing', 'order': 6, 'status': 'complete', 'workflows': [1,2,3,4], 'sources': []},\n"
            "]\n"
            "def build_departments(data_dir):\n"
            "    (pathlib.Path(data_dir) / 'departments.json').write_text(json.dumps({'departments': DEPARTMENTS}), encoding='utf-8')\n"
            "if __name__ == '__main__': build_departments(sys.argv[1])\n",
            encoding="utf-8",
        )
        (root / "site" / "js" / "departments.js").write_text(
            "export function renderLifecycleSvg(mode = 'ref') {\n  return 'old';\n}\n",
            encoding="utf-8",
        )
        (root / "tests" / "test_v60.py").write_text("self.assertEqual(len(depts), 4)\n", encoding="utf-8")
        (root / "tests" / "test_v60_site.py").write_text('V60_ROUTES = [\n    "/#/ref/departments/analytical",\n]\n', encoding="utf-8")

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        subprocess.run([sys.executable, str(root / "pipeline" / "build_departments.py"), str(root / "site" / "data")], check=True)
        depts = json.loads((root / "site" / "data" / "departments.json").read_text(encoding="utf-8"))["departments"]
        assert len(depts) == 8, len(depts)
        order_ids = [d["id"] for d in depts]
        assert order_ids == ["discovery", "formulation", "analytical", "clinical", "regulatory", "manufacturing", "commercial", "distribution"], order_ids
        for d in depts:
            assert d["status"] == "complete" and len(d["workflows"]) >= 4
            for src in d.get("sources", []):
                assert src["url"].startswith("https://"), src

        print("V60I_END_TO_END_8STAGE_LIFECYCLE_SELFTEST_PASSED", json.dumps({"stages": order_ids, **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.0i 8-Stage End-to-End Lifecycle Encyclopedia patch.")
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
