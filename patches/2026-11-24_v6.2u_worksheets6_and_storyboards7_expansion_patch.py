#!/usr/bin/env python3
"""Pill by Pill v6.2u Patch: Printable Teacher Worksheets (4 -> 6) & Trace-One-Drug Storyboards (5 -> 7).

1. Appends 2 classroom-ready printable worksheets to `pipeline/build_worksheets.py` (4 -> 6 total):
   - Worksheet 5: Designing a Fair Clinical Trial & Measuring Success (AP Stats / AP Bio / NGSS)
   - Worksheet 6: Drug Patents, Generics & Why Medicine Shortages Happen (Economics / Civics)
2. Appends 2 End-to-End Trace-One-Drug Storyboards to `pipeline/build_v61b_reference.py` (5 -> 7 total):
   - Tozinameran (Comirnaty — mRNA-LNP Vaccine)
   - Trastuzumab Deruxtecan (Enhertu — Antibody-Drug Conjugate / ADC)

Usage:
  python3 2026-11-24_v6.2u_worksheets6_and_storyboards7_expansion_patch.py --selftest
  python3 2026-11-24_v6.2u_worksheets6_and_storyboards7_expansion_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

EXTRA_WORKSHEETS_2 = [{'id': 'ws-clinical-trials', 'title': 'Worksheet 5: Designing a Fair Clinical Trial & Measuring Success', 'grade_band': 'Grades 10–12 · AP Statistics / AP Biology / Health Science', 'standards': ['NGSS HS-ETS1-2', 'AP Statistics (Experimental Design)'], 'estimated_time': '35–45 minutes', 'explore_links': [{'label': 'Clinical Trials & Endpoints Guide', 'href': '#/explore/trials'}, {'label': 'Stage 4: Clinical Development', 'href': '#/explore/departments/clinical'}, {'label': 'Acronym Glossary (IRB, DSMB, ITT)', 'href': '#/explore/glossary'}], 'questions': [{'prompt': 'Explain why modern Phase 3 trials use both Randomization and Double-Blinding. What kind of bias does each one prevent?', 'answer': 'Randomization assigns volunteers by chance so known and unknown differences (age, disease severity) are balanced across groups, preventing selection bias. Double-blinding keeps patients, doctors, and outcome assessors unaware of who received the active drug vs. control, preventing expectation/placebo and measurement bias.'}, {'prompt': "Using the Clinical Trials & Endpoints page, compare a 'True Clinical Outcome' (like Overall Survival) with a 'Surrogate Endpoint' (like shrinking a tumor on a scan or lowering blood pressure). When does FDA allow a surrogate endpoint?", 'answer': 'A true clinical outcome directly measures whether patients live longer, feel better, or function better. A validated surrogate (e.g., blood pressure, HbA1c, HIV viral load) is proven to predict real outcomes and supports traditional approval; a reasonably likely surrogate (e.g., tumor response rate) can support Accelerated Approval for serious unmet needs with mandatory confirmatory trials.'}, {'prompt': "A trial reports a '50% relative risk reduction' because 2% of control patients had an event versus 1% of treated patients. Calculate the Absolute Risk Reduction (ARR) and Number Needed to Treat (NNT), and explain why both numbers matter.", 'answer': 'ARR = 2% - 1% = 1% (0.01). NNT = 1 / 0.01 = 100 patients treated to prevent 1 event. Relative percentages can make small absolute benefits sound huge; ARR and NNT show the real-world clinical magnitude.'}]}, {'id': 'ws-patents-shortages', 'title': 'Worksheet 6: Drug Patents, Generics & Why Medicine Shortages Happen', 'grade_band': 'Grades 10–12 · Economics / Government / Biotechnology', 'standards': ['C3 Framework D2.Eco.1.9-12', 'C3 Framework D2.Civ.13.9-12'], 'estimated_time': '35–45 minutes', 'explore_links': [{'label': 'Patents, Hatch-Waxman & BPCIA', 'href': '#/explore/ip'}, {'label': 'Drug Shortages & Supply Resilience', 'href': '#/explore/shortages'}, {'label': 'How Medicines Are Funded & Priced', 'href': '#/explore/economics'}], 'questions': [{'prompt': "Compare how a generic chemical pill (ANDA 505(j)) and a biosimilar biologic (BLA 351(k)) enter the market after a brand drug's protections expire. Why does a reference biologic receive 12 years of U.S. exclusivity versus 5 years for a new chemical entity?", 'answer': 'Generic pills prove bioequivalence (80–125% blood-level match) under Hatch-Waxman (5-year NCE exclusivity) and face automatic pharmacy substitution. Biologics are large complex proteins grown in living cells requiring extensive analytical and clinical similarity studies under BPCIA, which grants 12 years of reference exclusivity.'}, {'prompt': 'Explain why some of the most severe U.S. hospital drug shortages happen with 30-year-old generic IV medicines (like basic chemotherapy or saline) rather than brand-new expensive drugs.', 'answer': 'Older sterile generic injectables require expensive ISO 5 cleanrooms and strict cGMP testing yet sell for very low prices with razor-thin margins. That discourages backup factories and quality upgrades, so a single cGMP shutdown or raw-material disruption can trigger a nationwide shortage.'}, {'prompt': 'List two tools the FDA uses during a drug shortage and one long-term policy or engineering fix that builds a more resilient supply chain.', 'answer': 'FDA tools include mandatory 6-month advance discontinuance alerts (FDASIA § 506C), expedited review of backup factories/generics, stability-backed expiration date extensions, temporary foreign importation, and 503B compounding relief. Long-term fixes include dual-sourcing APIs, FDA Quality Management Maturity (QMM) scoring, hospital buffer stocks, and quality-tiered purchasing.'}]}]
EXTRA_STORYBOARDS_2 = [{'id': 'tozinameran', 'drug_name': 'Tozinameran (Comirnaty — mRNA-LNP Vaccine)', 'drug_slug': 'tozinameran', 'modality': 'mRNA–Lipid Nanoparticle Vaccine', 'headline': 'From viral genome sequence to global mRNA-LNP vaccine in under one year', 'plain_intro': 'Follow how decades of nucleoside-modified mRNA and lipid nanoparticle research enabled a cell-free genetic vaccine scaled to billions of doses.', 'stages': [{'stage_id': 'discovery', 'label': '1. Discovery', 'summary': "Combined Katalin Karikó and Drew Weissman's N1-methylpseudouridine mRNA modification (2023 Nobel Prize) with Kizzmekia Corbett / Barney Graham / Jason McLellan's 2P prefusion-stabilized spike protein design within days of the SARS-CoV-2 sequence release."}, {'stage_id': 'formulation', 'label': '2. Formulation', 'summary': 'Encapsulated fragile mRNA inside a 4-component Lipid Nanoparticle (ionizable lipid ALC-0315, DSPC, cholesterol, PEG-lipid ALC-0159) via impingement-jet mixing to protect RNA in vivo and enable cellular uptake.'}, {'stage_id': 'analytical', 'label': '3. Analytical QC', 'summary': "Verified mRNA sequence integrity, 5' capping efficiency, dsRNA impurity limits, LNP particle size/polydispersity (DLS), encapsulation efficiency, and CBER lot-by-lot release testing (21 CFR 610.2)."}, {'stage_id': 'clinical', 'label': '4. Clinical Trials', 'summary': 'Seamless Phase 1/2/3 randomized placebo-controlled trial enrolled ~44,000 participants globally, demonstrating ~95% initial efficacy against symptomatic COVID-19 with independent DMC oversight.'}, {'stage_id': 'regulatory', 'label': '5. Regulatory', 'summary': 'Granted FDA Emergency Use Authorization (Dec 2020) after public VRBPAC review and full FDA CBER BLA approval (Aug 2021), followed by EMA, Health Canada, and PMDA authorizations and annual strain updates.'}, {'stage_id': 'manufacturing', 'label': '6. Manufacturing', 'summary': 'Cell-free enzymatic in vitro transcription (IVT) from linearized plasmid DNA template -> TFF/UFDF purification -> impingement-jet LNP encapsulation -> aseptic multi-dose vial fill-finish.'}, {'stage_id': 'commercial', 'label': '7. Economics & IP', 'summary': 'Initial pandemic advance-purchase agreements with governments transitioned to commercial and CDC ACIP-recommended seasonal immunization coverage; accompanied by complex LNP/mRNA patent licensing.'}, {'stage_id': 'distribution', 'label': '8. Distribution & Safety', 'summary': 'Pioneered global ultra-low-temperature (-80°C to -60°C) dry-ice thermal shippers before reformulating for standard 2–8°C refrigerator stability, monitored continuously via VAERS, CDC VSD, and FDA BEST.'}], 'sources': [{'label': 'NobelPrize.org — 2023 Nobel Prize in Physiology or Medicine (mRNA)', 'url': 'https://www.nobelprize.org/prizes/medicine/2023/summary/'}, {'label': 'FDA — Vaccines (CBER)', 'url': 'https://www.fda.gov/vaccines-blood-biologics/vaccines'}]}, {'id': 'trastuzumab-deruxtecan', 'drug_name': 'Trastuzumab Deruxtecan (Enhertu — ADC)', 'drug_slug': 'fam-trastuzumab-deruxtecan-nxki', 'modality': 'Antibody-Drug Conjugate (ADC)', 'headline': "A 'guided missile' antibody carrying a topoisomerase-I payload that unlocked HER2-low cancer", 'plain_intro': 'See how linking a high-potency chemotherapy payload to an anti-HER2 antibody with a tumor-cleavable linker expanded targeted therapy to patients previously considered HER2-negative.', 'stages': [{'stage_id': 'discovery', 'label': '1. Discovery', 'summary': 'Daiichi Sankyo engineered an anti-HER2 IgG1 antibody (trastuzumab backbone) conjugated via a tumor-selective tetrapeptide linker to DXd, a membrane-permeable topoisomerase I inhibitor payload at a high Drug-to-Antibody Ratio (DAR ~8).'}, {'stage_id': 'formulation', 'label': '2. Formulation', 'summary': 'Formulated as a sterile, preservative-free lyophilized powder in single-dose amber vials reconstituted with Sterile Water for Injection for IV infusion.'}, {'stage_id': 'analytical', 'label': '3. Analytical QC', 'summary': 'Characterized for DAR distribution (HIC-HPLC / intact LC-MS), free unconjugated payload limits, size-exclusion aggregates, linker stability, cell-based potency, and sterility/endotoxin.'}, {'stage_id': 'clinical', 'label': '4. Clinical Trials', 'summary': 'DESTINY-Breast01, DESTINY-Breast04 (establishing HER2-low breast cancer), and DESTINY-PanTumor02 demonstrated durable responses across breast, gastric, lung, and HER2+ IHC 3+ solid tumors.'}, {'stage_id': 'regulatory', 'label': '5. Regulatory', 'summary': 'First FDA-approved in Dec 2019 (BLA 761139) under Breakthrough Therapy and Accelerated Approval, later earning full approval and tissue-agnostic HER2+ (IHC 3+) solid-tumor approval alongside companion diagnostic IHC assays.'}, {'stage_id': 'manufacturing', 'label': '6. Manufacturing', 'summary': 'Hybrid biologic + high-potency small-molecule supply chain: CHO mAb fermentation + OEB-5 containment linker-payload synthesis -> controlled chemical conjugation -> TFF purification -> aseptic lyophilization.'}, {'stage_id': 'commercial', 'label': '7. Economics & IP', 'summary': 'Co-developed and co-commercialized via a landmark Daiichi Sankyo / AstraZeneca global collaboration; protected by Purple Book 12-year biologic exclusivity and linker-payload patents.'}, {'stage_id': 'distribution', 'label': '8. Distribution & Safety', 'summary': '2–8°C cold-chain specialty distribution to oncology infusion centers, carrying a Boxed Warning for Interstitial Lung Disease (ILD) / pneumonitis with proactive CT monitoring and pharmacovigilance.'}], 'sources': [{'label': 'FDA — Clinical Pharmacology Considerations for Antibody-Drug Conjugates', 'url': 'https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-pharmacology-considerations-antibody-drug-conjugates'}, {'label': 'FDA — Tissue-Agnostic Drug Development in Oncology', 'url': 'https://www.fda.gov/regulatory-information/search-fda-guidance-documents/tissue-agnostic-drug-development-oncology'}]}]


def _patch_worksheets(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"ws-patents-shortages"' in txt:
        return False
    anchor = "def build_worksheets("
    if anchor not in txt:
        return False
    add_block = (
        "\n# v6.2u: Expand Printable Teacher Worksheets from 4 -> 6\n"
        "_V62U_EXTRA_WORKSHEETS = " + json.dumps(EXTRA_WORKSHEETS_2, indent=4, ensure_ascii=False) + "\n"
        "for _ws in _V62U_EXTRA_WORKSHEETS:\n"
        "    if not any(x.get('id') == _ws['id'] for x in WORKSHEETS):\n"
        "        WORKSHEETS.append(_ws)\n\n"
    )
    path.write_text(txt.replace(anchor, add_block + anchor, 1), encoding="utf-8")
    return True


def _patch_storyboards(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"trastuzumab-deruxtecan"' in txt:
        return False
    anchor = "def build_v61b_reference("
    if anchor not in txt:
        return False
    add_block = (
        "\n# v6.2u: Expand Trace-One-Drug Storyboards from 5 -> 7 (+mRNA-LNP Vaccine, +ADC)\n"
        "_V62U_EXTRA_STORYBOARDS = " + json.dumps(EXTRA_STORYBOARDS_2, indent=4, ensure_ascii=False) + "\n"
        "for _sb in _V62U_EXTRA_STORYBOARDS:\n"
        "    if not any(x.get('id') == _sb['id'] for x in TRACE_STORYBOARDS):\n"
        "        TRACE_STORYBOARDS.append(_sb)\n\n"
    )
    path.write_text(txt.replace(anchor, add_block + anchor, 1), encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    pipe_dir = root / "pipeline"
    return {
        "worksheets_expanded_to_6": _patch_worksheets(pipe_dir / "build_worksheets.py"),
        "storyboards_expanded_to_7": _patch_storyboards(pipe_dir / "build_v61b_reference.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "data").mkdir(parents=True)

        (root / "pipeline" / "build_worksheets.py").write_text(
            'import json, pathlib, sys\n'
            'WORKSHEETS = [{"id": f"ws-{i}", "standards": ["NGSS"], "questions": [1,2,3]} for i in range(4)]\n'
            'def build_worksheets(d):\n'
            '    (pathlib.Path(d) / "worksheets.json").write_text(json.dumps({"count": len(WORKSHEETS), "worksheets": WORKSHEETS}), encoding="utf-8")\n'
            'if __name__ == "__main__": build_worksheets(sys.argv[1])\n',
            encoding="utf-8",
        )
        (root / "pipeline" / "build_v61b_reference.py").write_text(
            'import json, pathlib, sys\n'
            'TRACE_STORYBOARDS = [{"id": f"sb-{i}", "stages": [1]*8, "sources": [{"url": "https://www.fda.gov/"}]} for i in range(5)]\n'
            'def build_v61b_reference(d):\n'
            '    (pathlib.Path(d) / "trace_storyboards.json").write_text(json.dumps({"count": len(TRACE_STORYBOARDS), "storyboards": TRACE_STORYBOARDS}), encoding="utf-8")\n'
            'if __name__ == "__main__": build_v61b_reference(sys.argv[1])\n',
            encoding="utf-8",
        )

        r1 = apply_patch(root)
        assert all(r1.values()), r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        subprocess.run([sys.executable, str(root / "pipeline" / "build_worksheets.py"), str(root / "site" / "data")], check=True)
        ws = json.loads((root / "site" / "data" / "worksheets.json").read_text(encoding="utf-8"))
        assert ws["count"] == 6, ws["count"]
        raw_ws = json.dumps(ws).lower()
        for host in ("equipnet", "labx", "fedequip", "ssllc"):
            assert host not in raw_ws, host

        subprocess.run([sys.executable, str(root / "pipeline" / "build_v61b_reference.py"), str(root / "site" / "data")], check=True)
        sb = json.loads((root / "site" / "data" / "trace_storyboards.json").read_text(encoding="utf-8"))
        assert sb["count"] == 7, sb["count"]
        for item in sb["storyboards"][-2:]:
            assert len(item["stages"]) == 8 and all(s["url"].startswith("https://") for s in item["sources"])

        print("V62U_WORKSHEETS6_STORYBOARDS7_SELFTEST_PASSED", json.dumps({"worksheets_total": ws["count"], "storyboards_total": sb["count"], **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply Pill by Pill v6.2u Worksheets (4 -> 6) & Storyboards (5 -> 7) Expansion patch.")
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
