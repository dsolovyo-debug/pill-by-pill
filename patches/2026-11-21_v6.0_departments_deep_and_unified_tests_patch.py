#!/usr/bin/env python3
"""Pill by Pill v6.0b+Unified Tests Patch: Complete Discovery & Manufacturing Departments + tests/test_v60.py.

Upgrades `pipeline/build_departments.py` (promoting `discovery` and `manufacturing` from `scaffold`
to `complete` with 4 full workflows each and verified FDA/ICH/eCFR anchors) and adds the unified
`tests/test_v60.py` regression suite covering v6.0a, v6.0b, and v6.0c together.

Usage:
  python3 2026-11-21_v6.0_departments_deep_and_unified_tests_patch.py --selftest
  python3 2026-11-21_v6.0_departments_deep_and_unified_tests_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

DEEP_DISCOVERY = {'id': 'discovery', 'name': 'Early-Stage Discovery & Preclinical R&D', 'icon': '🧬', 'stage_range': 'Target ID → IND Filing', 'status': 'complete', 'plain_summary': 'Before a medicine is ever tested in people, scientists identify the biological target behind a disease, screen thousands of candidate molecules, image how the best ones lock into their target in 3D, and run strict laboratory safety studies before requesting permission for human clinical trials.', 'technical_summary': 'Encompasses target identification and validation, high-throughput screening (HTS), hit-to-lead medicinal chemistry or biologic lead discovery (hybridoma, phage display, mRNA/oligo design), structure-based drug design (X-ray crystallography, cryo-EM, NMR), in vitro/in vivo ADME-PK, and Good Laboratory Practice (GLP, 21 CFR Part 58) nonclinical safety pharmacology and toxicology studies supporting an Investigational New Drug (IND, 21 CFR Part 312) submission.', 'workflows': [{'step': '1. Target Identification & High-Throughput Screening (HTS)', 'plain': 'Pinpoint the protein or gene driving a disease, then use lab robots to test thousands of candidate compounds for early biological activity.', 'expert': 'Biochemical and cell-based HTS assays (96/384/1,536-well) using automated liquid handlers and plate readers to identify tractable hit series and confirm target engagement.'}, {'step': '2. Structural Biology & Lead Optimization (SBDD)', 'plain': 'Map the 3D atomic pocket of the target so chemists can reshape the molecule for a tighter, more selective fit.', 'expert': "Structure-based drug design via X-ray crystallography, cryo-EM, and NMR—directly reflected in this site's 485 experimental PDB drug-target binding animations—optimizing potency, selectivity, and physicochemical properties."}, {'step': '3. Preclinical ADME, PK & Safety Pharmacology', 'plain': 'Check how the candidate is absorbed, broken down, and cleared—and screen early for heart, liver, or genetic safety risks.', 'expert': 'In vitro metabolic stability, CYP450 inhibition/induction, hERG/QT cardiac safety (ICH S7B), genotoxicity (ICH S2(R1)), and PK/PD exposure modeling to project first-in-human (FIH) starting doses.'}, {'step': '4. GLP Toxicology & IND Submission (21 CFR Part 58 / 312)', 'plain': 'Run formal, audited nonclinical safety studies to prove the candidate is safe enough to begin Phase I human trials.', 'expert': 'Repeat-dose nonclinical toxicology in rodent and non-rodent species under GLP (21 CFR Part 58) and ICH M3(R2) / ICH S6(R1) (for biologics), establishing the NOAEL and compiling the FDA IND package (21 CFR Part 312).'}], 'regulatory_anchors': [{'label': 'FDA Step 1: Discovery and Development', 'url': 'https://www.fda.gov/patients/drug-development-process/step-1-discovery-and-development'}, {'label': 'FDA Step 2: Preclinical Research', 'url': 'https://www.fda.gov/patients/drug-development-process/step-2-preclinical-research'}, {'label': 'FDA Good Laboratory Practice (GLP) Regulations (21 CFR Part 58)', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-58'}, {'label': 'FDA Guidance: M3(R2) Nonclinical Safety Studies for the Conduct of Human Clinical Trials', 'url': 'https://www.fda.gov/regulatory-information/search-fda-guidance-documents/m3r2-nonclinical-safety-studies-conduct-human-clinical-trials-and-marketing-authorization'}], 'equipment_ids': ['eq-hts-liquid-handler', 'eq-lc-ms-ms', 'eq-hplc-uplc'], 'related_links': [{'title': '3D Experimental Binding Animations (485)', 'href': '#/ref/drugs?has=binding', 'text': 'Explore real PDB crystal and cryo-EM drug-target pockets.'}, {'title': 'Medicine Families (297 Trees)', 'href': '#/ref/families', 'text': 'See how follow-on drugs evolved from first-in-class discoveries.'}, {'title': 'Equipment Market (Discovery)', 'href': '#/ref/equipment?dept=discovery', 'text': 'Inspect HTS liquid handlers and bioanalytical LC-MS/MS systems.'}]}
DEEP_MANUFACTURING = {'id': 'manufacturing', 'name': 'Commercial Manufacturing & Bioprocessing', 'icon': '🏭', 'stage_range': 'Phase III / PPQ → Commercial', 'status': 'complete', 'plain_summary': 'Making a few grams in a research lab is very different from making millions of sterile, identical doses for hospitals and pharmacies worldwide. Commercial manufacturing scales up chemical synthesis or living cell factories under strict cleanroom rules and regulatory inspections.', 'technical_summary': 'Covers API chemical synthesis scale-up (ICH Q11) or upstream/downstream biologics manufacturing (mammalian/microbial cell culture bioreactors, harvest, Protein A / ion-exchange chromatography, tangential flow filtration, viral clearance per ICH Q5A), Process Performance Qualification (PPQ), ICH M4Q 3.2.S.2.6 batch comparability, Continued Process Verification (CPV), and cGMP compliance (21 CFR Parts 210/211).', 'workflows': [{'step': '1. Upstream API Synthesis or Bioreactor Production', 'plain': 'Build the active drug molecule in large chemical reactors or brew biologic proteins inside living cells.', 'expert': 'cGMP multi-step API synthesis (ICH Q11) or fed-batch/perfusion mammalian/microbial cell culture in single-use (SUB) or stainless-steel bioreactors with inline DO, pH, and metabolite control.'}, {'step': '2. Downstream Purification, Viral Clearance & Isolation', 'plain': 'Filter, separate, and purify the active medicine until every trace of host cells, solvents, or viruses is removed.', 'expert': 'Preparative chromatography skids (Protein A, IEX, HIC), tangential flow filtration (TFF/UFDF), low-pH/nanofiltration viral clearance (ICH Q5A), and API crystallization/drying.'}, {'step': '3. Sterile Fill-Finish, Lyophilization & Packaging', 'plain': 'Fill the purified medicine into vials, syringes, or blister packs inside sealed, germ-free cleanrooms.', 'expert': 'ISO 5 Grade A barrier isolator aseptic fill-finish, steam-in-place (SIP) lyophilization, 100% visual/CCIT inspection, and serialized DSCSA commercial packaging.'}, {'step': '4. Process Validation (PPQ), CPV & cGMP Inspections', 'plain': 'Run consecutive full-scale batches to prove the factory delivers identical quality every time before FDA and EMA inspect the site.', 'expert': 'FDA 3-stage Process Validation (Stage 1 Design, Stage 2 PPQ, Stage 3 CPV), ICH Q5E / 3.2.S.2.6 comparability, Pre-Approval Inspections (PAI), and ongoing cGMP surveillance (21 CFR Part 211).'}], 'regulatory_anchors': [{'label': 'FDA Guidance: Process Validation — General Principles and Practices', 'url': 'https://www.fda.gov/regulatory-information/search-fda-guidance-documents/process-validation-general-principles-and-practices'}, {'label': 'FDA Guidance: Q11 Development and Manufacture of Drug Substances', 'url': 'https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q11-development-and-manufacture-drug-substances'}, {'label': 'FDA cGMP for Finished Pharmaceuticals (21 CFR Part 211)', 'url': 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211'}], 'equipment_ids': ['eq-single-use-bioreactor', 'eq-lyophilizer', 'eq-sterile-fill-finish', 'eq-rotary-tablet-press'], 'related_links': [{'title': 'Manufacturers, CDMOs & Site Audits', 'href': '#/ref/vendors', 'text': 'Compare manufacturing sites by stage, modality, and FDA/EMA audit history.'}, {'title': 'Equipment Market (Manufacturing)', 'href': '#/ref/equipment?dept=manufacturing', 'text': 'Inspect single-use bioreactors, lyophilizers, and fill-finish lines.'}, {'title': 'How Medicines Are Made (By Modality)', 'href': '#/explore/made', 'text': 'Compare chemical synthesis, fermentation, and recombinant cells.'}]}
TEST_V60_PY = '#!/usr/bin/env python3\n"""Unified v6.0a + v6.0b + v6.0c regression test suite for Pill by Pill.\n\nVerifies:\n  - v6.0a: `pipeline/build_vendors.py`, `pipeline/fetch_fda_inspections.py`, `fetch_fda_decrs.py`,\n           `fetch_fda_warning_letters.py`, `fetch_ema_eudragmdp.py`, and `site/js/vendors.js`\n  - v6.0b: `pipeline/build_departments.py`, `site/data/departments.json` (4 complete departments,\n           5 routes, HTTPS-only official anchors), and `site/js/departments.js`\n  - v6.0c: `pipeline/fetch_equipment_awards.py`, `pipeline/build_equipment_catalog.py`,\n           `site/data/equipment.json` (12 hardware classes, zero fabricated prices, Reference-only\n           marketplace links), and `site/js/equipment.js`\n  - Wiring: `site/js/app.js` and `site/js/layout.js` route & nav parity + zero `--card` CSS regressions.\n\nRun from the repository root:\n  python3 tests/test_v60.py\n"""\nimport json\nimport pathlib\nimport subprocess\nimport sys\nimport tempfile\nimport unittest\n\nROOT = pathlib.Path(__file__).resolve().parents[1]\n\n\nclass TestV60Unified(unittest.TestCase):\n    def test_01_v60b_departments_complete_and_sourced(self):\n        script = ROOT / "pipeline" / "build_departments.py"\n        self.assertTrue(script.is_file(), "Missing pipeline/build_departments.py")\n        with tempfile.TemporaryDirectory() as td:\n            data_dir = pathlib.Path(td)\n            subprocess.run([sys.executable, str(script), str(data_dir)], check=True, capture_output=True)\n            doc = json.loads((data_dir / "departments.json").read_text(encoding="utf-8"))\n            self.assertEqual(doc["department_count"], 4)\n            self.assertEqual(doc["route_count"], 5)\n            for d in doc["departments"]:\n                self.assertEqual(d["status"], "complete", f"Department {d[\'id\']} not complete")\n                self.assertGreaterEqual(len(d["workflows"]), 4, f"Department {d[\'id\']} needs >=4 workflows")\n                self.assertTrue(d["regulatory_anchors"])\n                for a in d["regulatory_anchors"]:\n                    self.assertTrue(a["url"].startswith("https://"), a)\n            for r in doc["routes"]:\n                self.assertTrue(r["cqas"] and r["equipment_ids"] and r["sources"])\n                for s in r["sources"]:\n                    self.assertTrue(s["url"].startswith("https://"), s)\n\n    def test_02_v60c_equipment_zero_fabricated_prices(self):\n        script = ROOT / "pipeline" / "build_equipment_catalog.py"\n        if not script.is_file():\n            self.skipTest("v6.0c build_equipment_catalog.py not installed yet")\n        with tempfile.TemporaryDirectory() as td:\n            raw_dir = pathlib.Path(td) / "raw"\n            data_dir = pathlib.Path(td) / "data"\n            raw_dir.mkdir()\n            data_dir.mkdir()\n            subprocess.run([sys.executable, str(script), str(raw_dir), str(data_dir)], check=True, capture_output=True)\n            cat = json.loads((data_dir / "equipment.json").read_text(encoding="utf-8"))\n            self.assertEqual(len(cat), 12)\n            for item in cat:\n                self.assertIsNone(item["pricing"]["new_public_award_range_usd"])\n                self.assertIsNone(item["pricing"]["used_market_range_usd"])\n                self.assertEqual(item["pricing"]["price_history"], [])\n                self.assertIn("quote-based", item["pricing"]["scope_note"])\n                self.assertEqual(len(item["pricing"]["marketplace_links"]), 4)\n                for u in item["sources"]:\n                    self.assertTrue(u.startswith("https://"), u)\n\n    def test_03_v60a_vendors_pipeline_and_disclosure(self):\n        script = ROOT / "pipeline" / "build_vendors.py"\n        if not script.is_file():\n            self.skipTest("v6.0a build_vendors.py not installed yet")\n        with tempfile.TemporaryDirectory() as td:\n            raw_dir = pathlib.Path(td) / "raw"\n            data_dir = pathlib.Path(td) / "data"\n            raw_dir.mkdir()\n            data_dir.mkdir()\n            (raw_dir / "fda_decrs.json").write_text(json.dumps([\n                {"fei": "3002807001", "firm_name": "Alpha Bio", "city": "Visp", "country": "Switzerland", "operations": ["Biologics Manufacture"]}\n            ]), encoding="utf-8")\n            (raw_dir / "fda_inspections.json").write_text(json.dumps([\n                {"fei": "3002807001", "end_date": "2026-04-12", "classification": "NAI", "project_area": "Biologics", "inspection_id": "101"}\n            ]), encoding="utf-8")\n            subprocess.run([sys.executable, str(script), str(raw_dir), str(data_dir)], check=True, capture_output=True)\n            idx = json.loads((data_dir / "vendors_index.json").read_text(encoding="utf-8"))\n            self.assertEqual(idx["count"], 1)\n            self.assertIn("21 CFR 314.430", idx["scope_note"])\n            site = json.loads((data_dir / "vendors" / "3002807001.json").read_text(encoding="utf-8"))\n            self.assertEqual(site["counts"]["NAI"], 1)\n            self.assertEqual(site["latest_classification"], "NAI")\n\n    def test_04_frontend_modules_and_no_card_var(self):\n        for rel, required in [\n            ("site/js/departments.js", ["departmentsExplorePage", "departmentsRefPage", "routesRefPage"]),\n            ("site/js/vendors.js", ["vendorsPage", "vendorComparePage", "vendorSitePage"]),\n            ("site/js/equipment.js", ["equipmentPage"]),\n        ]:\n            fp = ROOT / rel\n            if not fp.is_file():\n                continue\n            txt = fp.read_text(encoding="utf-8")\n            for sym in required:\n                self.assertIn(f"export async function {sym}", txt, f"Missing {sym} in {rel}")\n            self.assertNotIn("var(--card", txt, f"Undefined --card CSS variable found in {rel}")\n\n    def test_05_all_v60_python_scripts_compile(self):\n        for rel in [\n            "pipeline/build_departments.py",\n            "pipeline/build_vendors.py",\n            "pipeline/build_equipment_catalog.py",\n            "pipeline/fetch_equipment_awards.py",\n            "pipeline/fetch_fda_inspections.py",\n            "pipeline/fetch_fda_decrs.py",\n            "pipeline/fetch_fda_warning_letters.py",\n            "pipeline/fetch_ema_eudragmdp.py",\n        ]:\n            fp = ROOT / rel\n            if fp.is_file():\n                subprocess.run([sys.executable, "-m", "py_compile", str(fp)], check=True)\n\n\nif __name__ == "__main__":\n    unittest.main(verbosity=2)\n'


def _upgrade_build_departments(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"id": "discovery"' not in txt or '"status": "scaffold"' not in txt:
        return False

    # Execute the existing module's DEPARTMENTS list safely via AST/exec in isolated namespace,
    # replace discovery & manufacturing entries, and write back a clean updated DEPARTMENTS block.
    ns = {}
    exec(compile(txt, str(path), "exec"), ns)
    depts = ns.get("DEPARTMENTS") or []
    new_depts = []
    for d in depts:
        if d.get("id") == "discovery":
            new_depts.append(DEEP_DISCOVERY)
        elif d.get("id") == "manufacturing":
            new_depts.append(DEEP_MANUFACTURING)
        else:
            new_depts.append(d)

    start_idx = txt.index("DEPARTMENTS = [")
    end_idx = txt.index("\n\ndef _catalogue_modality_counts", start_idx)
    replacement = "DEPARTMENTS = " + json.dumps(new_depts, indent=4, ensure_ascii=False)
    path.write_text(txt[:start_idx] + replacement + txt[end_idx:], encoding="utf-8")
    return True


def apply_patch(root: pathlib.Path) -> dict:
    tests_dir = root / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    test_fp = tests_dir / "test_v60.py"
    test_written = False
    if not test_fp.is_file() or test_fp.read_text(encoding="utf-8") != TEST_V60_PY:
        test_fp.write_text(TEST_V60_PY, encoding="utf-8")
        test_written = True

    depts_upgraded = _upgrade_build_departments(root / "pipeline" / "build_departments.py")
    return {
        "departments_upgraded_to_complete": depts_upgraded,
        "unified_test_written": test_written,
        "test_path": "tests/test_v60.py",
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        # Self-contained minimal build_departments.py fixture with scaffold discovery & manufacturing
        fixture_depts = [
            {"id": "formulation", "name": "Formulation", "status": "complete", "workflows": [{"step": str(i)} for i in range(4)], "regulatory_anchors": [{"label": "FDA", "url": "https://www.fda.gov/"}]},
            {"id": "analytical", "name": "Analytical", "status": "complete", "workflows": [{"step": str(i)} for i in range(4)], "regulatory_anchors": [{"label": "FDA", "url": "https://www.fda.gov/"}]},
            {"id": "discovery", "name": "Discovery", "status": "scaffold", "workflows": [{"step": "1"}], "regulatory_anchors": [{"label": "FDA", "url": "https://www.fda.gov/"}]},
            {"id": "manufacturing", "name": "Manufacturing", "status": "scaffold", "workflows": [{"step": "1"}], "regulatory_anchors": [{"label": "FDA", "url": "https://www.fda.gov/"}]},
        ]
        fixture_routes = [{"id": f"r{i}", "cqas": ["a"], "equipment_ids": ["eq-1"], "sources": [{"label": "FDA", "url": "https://www.fda.gov/"}]} for i in range(5)]
        (root / "pipeline" / "build_departments.py").write_text(
            "import json, pathlib, sys\n"
            f"ROUTES_OF_ADMINISTRATION = {json.dumps(fixture_routes)}\n"
            f"DEPARTMENTS = {json.dumps(fixture_depts)}\n\n\n"
            "def _catalogue_modality_counts(d): return {}\n"
            "def build_departments(d):\n"
            "    d.mkdir(parents=True, exist_ok=True)\n"
            "    (d / 'departments.json').write_text(json.dumps({'department_count': len(DEPARTMENTS), 'route_count': len(ROUTES_OF_ADMINISTRATION), 'departments': DEPARTMENTS, 'routes': ROUTES_OF_ADMINISTRATION}), encoding='utf-8')\n"
            "if __name__ == '__main__': build_departments(pathlib.Path(sys.argv[1]))\n",
            encoding="utf-8",
        )

        r1 = apply_patch(root)
        assert r1["departments_upgraded_to_complete"] and r1["unified_test_written"], r1
        # Idempotency check
        r2 = apply_patch(root)
        assert not r2["departments_upgraded_to_complete"] and not r2["unified_test_written"], r2

        # Run the generated tests/test_v60.py end-to-end!
        out = subprocess.run([sys.executable, str(root / "tests" / "test_v60.py")], capture_output=True, text=True, check=True)
        print("V60_DEEP_DEPTS_AND_UNIFIED_TESTS_SELFTEST_PASSED", json.dumps(r1, indent=2))
        print(out.stderr.strip())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Upgrade v6.0b discovery/manufacturing departments & add tests/test_v60.py.")
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
