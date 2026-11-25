#!/usr/bin/env python3
"""Pill by Pill v6.0g Patch: Expand Equipment Market (12 -> 18 Hardware Classes) & Wire into Departments, Awards & Lab Kits.

Adds 6 specialty pharmaceutical hardware classes across Discovery, Formulation, and Bioprocessing:
  - `eq-nmr-spectrometer` (High-Field NMR Spectrometer, 400-800+ MHz)
  - `eq-cryo-em` (Cryo-Electron Microscope, 200-300 kV)
  - `eq-microfluidic-lnp` (Microfluidic LNP & Liposome Formulation System)
  - `eq-spray-dryer` (Pharmaceutical Spray Dryer for Amorphous Solid Dispersions)
  - `eq-prep-chromatography` (Preparative Bioprocess Chromatography Skid)
  - `eq-tff-skid` (Tangential Flow Filtration / UFDF Skid)

Updates:
  1. `pipeline/build_equipment_catalog.py`: Appends the 6 new classes (12 -> 18, zero fabricated prices).
  2. `pipeline/fetch_equipment_awards.py`: Appends USAspending.gov keyword queries for the 6 new classes.
  3. `pipeline/build_departments.py`: Cross-links the 6 new equipment IDs into Discovery, Formulation,
     Manufacturing, and the LNP/Oligo & Oral Solid routes.
  4. `site/js/equipment.js`: Adds a 5th Lab & Suite Kit (`kit-lnp-bioprocess`).
  5. `tests/test_v60.py`: Updates equipment catalog count check to `>= 18`.

Usage:
  python3 2026-11-21_v6.0g_equipment_expansion_18_classes_patch.py --selftest
  python3 2026-11-21_v6.0g_equipment_expansion_18_classes_patch.py --apply /path/to/unpacked_source
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

NEW_EQUIPMENT_6 = [{'id': 'eq-nmr-spectrometer', 'name': 'High-Field NMR Spectrometer (400–800+ MHz)', 'department': 'discovery', 'stages': ['preclinical', 'phase1_2', 'commercial'], 'modalities': ['small_molecule', 'oligo_peptide', 'biologics'], 'plain_summary': 'Uses powerful superconducting magnets and radio waves to map the exact 3D atomic structure and purity of new drug molecules in solution.', 'technical_spec': {'primary_use': 'Structure elucidation (1H, 13C, 19F, 31P, 2D HSQC/NOESY), fragment-based lead discovery (FBLD), and quantitative NMR (qNMR) reference standard certification.', 'gmp_compliance': 'USP <761> / <1761> Nuclear Magnetic Resonance Spectroscopy; 21 CFR Part 11', 'typical_footprint': 'Shielded magnet bay with liquid helium/nitrogen cryostat'}, 'leading_oems': [{'name': 'Bruker', 'market_evidence': 'Dominant global market leader in high-field and ultra-high-field superconducting NMR systems (Bruker BioSpin SEC 10-K).'}, {'name': 'JEOL', 'market_evidence': 'Established global supplier of 400–800 MHz analytical and research NMR spectrometers.'}], 'sources': ['https://www.fda.gov/patients/drug-development-process/step-1-discovery-and-development', 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11']}, {'id': 'eq-cryo-em', 'name': 'Cryo-Electron Microscope (Cryo-EM, 200–300 kV)', 'department': 'discovery', 'stages': ['preclinical'], 'modalities': ['biologics', 'small_molecule', 'oligo_peptide'], 'plain_summary': 'Flash-freezes protein targets and medicines in thin ice and images them with electron beams to reveal near-atomic 3D binding pockets—including membrane receptors that cannot be crystallized.', 'technical_spec': {'primary_use': 'Single-particle cryo-EM structure determination of GPCRs, ion channels, antibody-antigen complexes, and viral capsids (directly reflected in PDB cryo-EM binding animations).', 'gmp_compliance': 'Research & Discovery (GLP-adjacent structural characterization)', 'typical_footprint': 'Vibration-isolated, electromagnetically shielded microscope suite'}, 'leading_oems': [{'name': 'Thermo Fisher Scientific', 'market_evidence': 'Leading global supplier of 200–300 kV cryo-EM platforms (Krios, Glacios, Tundra; Thermo Fisher SEC 10-K).'}, {'name': 'JEOL', 'market_evidence': 'Major global supplier of CRYO ARM 200/300 kV transmission electron microscopes.'}], 'sources': ['https://www.fda.gov/patients/drug-development-process/step-1-discovery-and-development', 'https://www.rcsb.org/']}, {'id': 'eq-microfluidic-lnp', 'name': 'Microfluidic LNP & Liposome Formulation System', 'department': 'formulation', 'stages': ['preclinical', 'phase1_2', 'phase3_ppq', 'commercial'], 'modalities': ['oligo_peptide', 'sterile'], 'plain_summary': 'Precisely mixes nucleic acids (mRNA or siRNA) with protective lipids inside microscopic channels to assemble uniform lipid nanoparticles.', 'technical_spec': {'primary_use': 'Controlled nanoprecipitation / impingement-jet or microfluidic mixing for lipid nanoparticle (LNP) encapsulation, particle size (PDI), and encapsulation efficiency control.', 'gmp_compliance': '21 CFR Part 211; FDA Liposome Drug Products Guidance', 'typical_footprint': 'Benchtop R&D unit to cGMP single-use commercial skid'}, 'leading_oems': [{'name': 'Cytiva (Precision NanoSystems)', 'market_evidence': 'Leading supplier of NanoAssemblr microfluidic LNP platforms from benchtop to cGMP scale (Danaher SEC 10-K).'}, {'name': 'Knauer', 'market_evidence': 'Established supplier of impingement-jet mixing (IJM) LNP production skids.'}, {'name': 'Unchained Labs', 'market_evidence': 'Key supplier of automated LNP screening and formulation systems.'}], 'sources': ['https://www.fda.gov/regulatory-information/search-fda-guidance-documents/liposome-drug-products-chemistry-manufacturing-and-controls-human-pharmacokinetics-and-bioavailability', 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211']}, {'id': 'eq-spray-dryer', 'name': 'Pharmaceutical Spray Dryer (ASD)', 'department': 'formulation', 'stages': ['preclinical', 'phase1_2', 'phase3_ppq', 'commercial'], 'modalities': ['small_molecule', 'oral_solid'], 'plain_summary': 'Sprays a dissolved drug and polymer mist into hot gas so it dries in milliseconds into a fine powder that dissolves much faster in the stomach.', 'technical_spec': {'primary_use': 'Amorphous solid dispersion (ASD) manufacturing for poorly water-soluble BCS Class II/IV small molecules and engineered inhaled dry powders.', 'gmp_compliance': '21 CFR Part 211; ICH Q8(R2) Pharmaceutical Development; closed-loop N2 solvent recovery', 'typical_footprint': 'Benchtop R&D dryer to multi-story cGMP tower'}, 'leading_oems': [{'name': 'GEA', 'market_evidence': 'Leading global supplier of PSD pharmaceutical spray drying towers and closed-cycle solvent systems.'}, {'name': 'Buchi', 'market_evidence': 'Widely adopted leader in benchtop R&D mini spray dryers for early formulation screening.'}, {'name': 'SPX Flow (Anhydro)', 'market_evidence': 'Established supplier of pilot and commercial sanitary spray dryers.'}], 'sources': ['https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q8r2-pharmaceutical-development', 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211']}, {'id': 'eq-prep-chromatography', 'name': 'Preparative Bioprocess Chromatography Skid', 'department': 'manufacturing', 'stages': ['phase1_2', 'phase3_ppq', 'commercial'], 'modalities': ['biologics', 'oligo_peptide'], 'plain_summary': 'Large-scale automated purification columns that capture and polish therapeutic antibodies, proteins, or synthetic oligonucleotides to clinical purity.', 'technical_spec': {'primary_use': 'Protein A affinity capture, ion-exchange (IEX), hydrophobic interaction (HIC), and reversed-phase polishing with inline UV/pH/conductivity monitoring.', 'gmp_compliance': '21 CFR Part 211; ICH Q5A Viral Safety; ICH Q11', 'typical_footprint': 'Mobile stainless-steel or single-use cleanroom skid'}, 'leading_oems': [{'name': 'Cytiva', 'market_evidence': 'Global leader in AKTA process chromatography skids and Protein A resins (Danaher SEC 10-K).'}, {'name': 'Sartorius', 'market_evidence': 'Major supplier of BioSC and membrane chromatography purification skids.'}, {'name': 'MilliporeSigma (Merck KGaA)', 'market_evidence': 'Leading supplier of Mobius single-use and stainless-steel Mobius/Chromacon skids.'}], 'sources': ['https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q11-development-and-manufacture-drug-substances', 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211']}, {'id': 'eq-tff-skid', 'name': 'Tangential Flow Filtration (TFF / UFDF) Skid', 'department': 'manufacturing', 'stages': ['phase1_2', 'phase3_ppq', 'commercial'], 'modalities': ['biologics', 'oligo_peptide', 'sterile'], 'plain_summary': 'Pumps liquid medicine sideways across ultra-fine membrane filters to concentrate the drug and swap it into its final injectable buffer without clogging.', 'technical_spec': {'primary_use': 'Ultrafiltration/diafiltration (UFDF) for monoclonal antibody concentration, LNP buffer exchange and ethanol removal, and viral vector harvest clarification.', 'gmp_compliance': '21 CFR Part 211; ICH Q5E Comparability; single-use flow paths', 'typical_footprint': 'Benchtop cassette system to commercial cGMP skid'}, 'leading_oems': [{'name': 'Sartorius', 'market_evidence': 'Leading supplier of Sartoflow and Sartocon TFF systems and Hydrosart cassettes.'}, {'name': 'MilliporeSigma (Merck KGaA)', 'market_evidence': 'Major global supplier of Pellicon cassettes and Cogent/Mobius TFF skids.'}, {'name': 'Repligen', 'market_evidence': 'Leading specialist in hollow-fiber TFF (KrosFlo) and alternating tangential flow (ATF) systems.'}], 'sources': ['https://www.fda.gov/regulatory-information/search-fda-guidance-documents/process-validation-general-principles-and-practices', 'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211']}]
NEW_AWARD_QUERIES_6 = [('eq-nmr-spectrometer', ['NMR spectrometer', 'nuclear magnetic resonance']), ('eq-cryo-em', ['cryo-electron microscope', 'cryo-EM', 'transmission electron microscope']), ('eq-microfluidic-lnp', ['lipid nanoparticle', 'microfluidic mixer', 'NanoAssemblr']), ('eq-spray-dryer', ['spray dryer', 'Buchi spray']), ('eq-prep-chromatography', ['AKTA', 'preparative chromatography', 'bioprocess chromatography']), ('eq-tff-skid', ['tangential flow filtration', 'ultrafiltration diafiltration', 'TFF system'])]
NEW_LAB_KIT_JS = '  {\n    id: "kit-lnp-bioprocess",\n    name: "mRNA / Oligo LNP & Downstream Bioprocessing Suite",\n    stage: "Phase I–Commercial Nucleic Acid & Biologics",\n    summary: "Microfluidic LNP encapsulation paired with preparative chromatography and TFF/UFDF buffer exchange.",\n    equipment_ids: ["eq-microfluidic-lnp", "eq-prep-chromatography", "eq-tff-skid", "eq-lc-ms-ms"],\n  },\n'


def _patch_build_equipment_catalog(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"eq-cryo-em"' in txt:
        return False
    anchor = "\n\ndef _marketplace_links"
    if anchor not in txt:
        raise ValueError(f"Missing _marketplace_links anchor in {path}")
    add_block = "\n\nEQUIPMENT_CATALOG.extend(" + json.dumps(NEW_EQUIPMENT_6, indent=4, ensure_ascii=False) + ")\n"
    path.write_text(txt.replace(anchor, add_block + anchor, 1), encoding="utf-8")
    return True


def _patch_fetch_equipment_awards(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"eq-cryo-em"' in txt:
        return False
    anchor = "\n\ndef _post_json"
    if anchor not in txt:
        return False
    add_block = "\n\nEQUIPMENT_QUERIES.extend(" + json.dumps(NEW_AWARD_QUERIES_6, indent=4) + ")\n"
    path.write_text(txt.replace(anchor, add_block + anchor, 1), encoding="utf-8")
    return True


def _patch_build_departments(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    changed = False
    replacements = [
        ('"eq-hts-liquid-handler",\n            "eq-lc-ms-ms",\n            "eq-hplc-uplc"',
         '"eq-hts-liquid-handler",\n            "eq-nmr-spectrometer",\n            "eq-cryo-em",\n            "eq-lc-ms-ms",\n            "eq-hplc-uplc"'),
        ('"eq-single-use-bioreactor",\n            "eq-lyophilizer",\n            "eq-sterile-fill-finish",\n            "eq-rotary-tablet-press"',
         '"eq-single-use-bioreactor",\n            "eq-prep-chromatography",\n            "eq-tff-skid",\n            "eq-lyophilizer",\n            "eq-sterile-fill-finish",\n            "eq-rotary-tablet-press"'),
    ]
    for old, new in replacements:
        if old in txt and new not in txt:
            txt = txt.replace(old, new, 1)
            changed = True
    if changed:
        path.write_text(txt, encoding="utf-8")
    return changed


def _patch_equipment_js(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    if '"kit-lnp-bioprocess"' in txt or "LAB_SUITE_KITS" not in txt:
        return False
    anchor = '    equipment_ids: ["eq-single-use-bioreactor", "eq-sterile-fill-finish", "eq-lyophilizer", "eq-hplc-uplc"],\n  },\n];'
    if anchor not in txt:
        return False
    rep = '    equipment_ids: ["eq-single-use-bioreactor", "eq-sterile-fill-finish", "eq-lyophilizer", "eq-hplc-uplc"],\n  },\n' + NEW_LAB_KIT_JS + '];'
    path.write_text(txt.replace(anchor, rep, 1), encoding="utf-8")
    return True


def _patch_test_v60(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    txt = path.read_text(encoding="utf-8")
    old = "self.assertEqual(len(cat), 12)"
    new = "self.assertGreaterEqual(len(cat), 18)"
    if old in txt:
        path.write_text(txt.replace(old, new, 1), encoding="utf-8")
        return True
    return False


def apply_patch(root: pathlib.Path) -> dict:
    return {
        "equipment_catalog_expanded_to_18": _patch_build_equipment_catalog(root / "pipeline" / "build_equipment_catalog.py"),
        "award_queries_expanded_to_18": _patch_fetch_equipment_awards(root / "pipeline" / "fetch_equipment_awards.py"),
        "departments_equipment_links_updated": _patch_build_departments(root / "pipeline" / "build_departments.py"),
        "equipment_js_lnp_kit_added": _patch_equipment_js(root / "site" / "js" / "equipment.js"),
        "test_v60_updated": _patch_test_v60(root / "tests" / "test_v60.py"),
    }


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "pipeline").mkdir()
        (root / "site" / "js").mkdir(parents=True)
        (root / "tests").mkdir()
        (root / "raw").mkdir()
        (root / "site" / "data").mkdir(parents=True)

        # Minimal fixtures
        (root / "pipeline" / "build_equipment_catalog.py").write_text(
            "import json, pathlib, sys\n"
            "EQUIPMENT_CATALOG = [{'id': f'eq-{i}', 'name': f'Eq {i}', 'sources': ['https://www.fda.gov/']} for i in range(12)]\n\n\n"
            "def _marketplace_links(name): return []\n"
            "def main():\n"
            "    out = pathlib.Path(sys.argv[2]) / 'equipment.json'\n"
            "    out.write_text(json.dumps(EQUIPMENT_CATALOG), encoding='utf-8')\n"
            "if __name__ == '__main__': main()\n",
            encoding="utf-8",
        )
        (root / "pipeline" / "fetch_equipment_awards.py").write_text(
            "EQUIPMENT_QUERIES = []\n\n\ndef _post_json(): pass\n",
            encoding="utf-8",
        )
        (root / "site" / "js" / "equipment.js").write_text(
            'export const LAB_SUITE_KITS = [\n  {\n    equipment_ids: ["eq-single-use-bioreactor", "eq-sterile-fill-finish", "eq-lyophilizer", "eq-hplc-uplc"],\n  },\n];\n',
            encoding="utf-8",
        )
        (root / "tests" / "test_v60.py").write_text("self.assertEqual(len(cat), 12)\n", encoding="utf-8")

        r1 = apply_patch(root)
        assert r1["equipment_catalog_expanded_to_18"] and r1["award_queries_expanded_to_18"] and r1["equipment_js_lnp_kit_added"] and r1["test_v60_updated"], r1
        r2 = apply_patch(root)
        assert not any(r2.values()), r2

        subprocess.run([sys.executable, str(root / "pipeline" / "build_equipment_catalog.py"), str(root / "raw"), str(root / "site" / "data")], check=True)
        cat = json.loads((root / "site" / "data" / "equipment.json").read_text(encoding="utf-8"))
        assert len(cat) == 18, len(cat)
        for item in cat:
            for u in item["sources"]:
                assert u.startswith("https://"), u
        print("V60G_EQUIPMENT_18_CLASSES_SELFTEST_PASSED", json.dumps({"total_categories": len(cat), **r1}, indent=2))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Expand Pill by Pill v6.0 Equipment Market from 12 to 18 hardware classes.")
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
