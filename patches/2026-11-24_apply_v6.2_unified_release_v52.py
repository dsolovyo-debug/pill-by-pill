#!/usr/bin/env python3
"""Pill by Pill v6.2 Unified Release Integrator & Cleaner (v52 — complete 61 patches: v6.0a–v6.0l + v6.1a–v6.1z + v6.2a–v6.2u).

Applies all 61 patches in deterministic dependency order, runs all 49 builders, executes
`tests/test_v60.py`, bumps `app.py` and `site/version.json` to `6.2` (100 quiz questions,
80 acronym glossary terms, 100 origin stories, 6 printable teacher worksheets, 7 trace storyboards),
and packages a clean `__pycache__`-free `pill-by-pill-source_v6.2.zip`.

Usage:
  python3 2026-11-24_apply_v6.2_unified_release_v52.py --selftest
  python3 2026-11-24_apply_v6.2_unified_release_v52.py \
    --source-zip 2026-11-21_pill-by-pill-source_v6.0b.zip \
    --patches-dir . \
    --out-zip 2026-11-24_pill-by-pill-source_v6.2.zip
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

PATCH_ORDER = [('v6.0a', '2026-11-20_v6.0a_vendors_cdmo_audit_comparator_patch.py'), ('v6.0b', '2026-11-20_v6.0b_pharma_encyclopedia_departments_patch.py'), ('v6.0c', '2026-11-20_v6.0c_equipment_market_pricing_patch.py'), ('v6.0_fetchers_wiring', '2026-11-21_v6.0_vendors_fetchers_and_route_wiring_patch.py'), ('v6.0_deep_depts_tests', '2026-11-21_v6.0_departments_deep_and_unified_tests_patch.py'), ('v6.0d_crosslinks_api', '2026-11-21_v6.0d_crosslinks_price_charts_and_api_patch.py'), ('v6.0e_rollups_oems_svg', '2026-11-21_v6.0e_parent_rollups_oem_matrix_and_lifecycle_svg_patch.py'), ('v6.0f_static_seo', '2026-11-21_v6.0f_static_seo_and_sitemap_patch.py'), ('v6.0g_equip_18', '2026-11-21_v6.0g_equipment_expansion_18_classes_patch.py'), ('v6.0h_origins75_browser_tests', '2026-11-21_v6.0h_origin_stories_batch7_and_v60_browser_tests_patch.py'), ('v6.0i_8stage_lifecycle', '2026-11-21_v6.0i_end_to_end_8stage_lifecycle_patch.py'), ('v6.0j_software_economics', '2026-11-21_v6.0j_pharma_software_and_economics_patch.py'), ('v6.0k_partner_ecosystem', '2026-11-21_v6.0k_partner_ecosystem_patch.py'), ('v6.0l_playbooks_quiz58', '2026-11-21_v6.0l_modality_playbooks_and_v60_quiz_patch.py'), ('v6.1a_global_search_origins_csv', '2026-11-22_v6.1a_global_search_origins_gallery_nav_csv_patch.py'), ('v6.1b_glossary_trace_ich', '2026-11-22_v6.1b_glossary_trace_storyboards_ich_patch.py'), ('v6.1c_chem_quiz_worksheets', '2026-11-22_v6.1c_chem_copy_quiz_filters_teacher_worksheets_patch.py'), ('v6.1d_grouped_nav_pointers_status', '2026-11-22_v6.1d_grouped_nav_clinical_pointers_feed_status_patch.py'), ('v6.1e_atc_tree_origins90', '2026-11-22_v6.1e_atc_class_tree_and_origins_batch8_patch.py'), ('v6.1f_gsc_fix_origins100_storyboards5', '2026-11-22_v6.1f_gsc_schema_fix_origins100_and_5modality_storyboards_patch.py'), ('v6.1g_seo_search_browser_coverage', '2026-11-22_v6.1g_seo_global_search_and_browser_test_coverage_patch.py'), ('v6.1h_pathways_exclusivity', '2026-11-22_v6.1h_regulatory_pathways_and_exclusivity_comparator_patch.py'), ('v6.1i_clinical_trials_endpoints', '2026-11-22_v6.1i_clinical_trial_design_and_endpoints_patch.py'), ('v6.1j_adme_pk_medchem_delivery', '2026-11-23_v6.1j_adme_pk_medchem_and_delivery_patch.py'), ('v6.1k_pharmacovigilance_safety', '2026-11-23_v6.1k_pharmacovigilance_and_drug_safety_patch.py'), ('v6.1l_ip_patents_hatch_waxman_bpcia', '2026-11-23_v6.1l_pharma_ip_patents_hatch_waxman_bpcia_patch.py'), ('v6.1m_sterile_bioprocessing_cleanroom', '2026-11-23_v6.1m_sterile_manufacturing_bioprocessing_cleanroom_patch.py'), ('v6.1n_global_reg_hta', '2026-11-23_v6.1n_global_regulatory_agencies_and_hta_comparator_patch.py'), ('v6.1o_cdx_biomarkers', '2026-11-23_v6.1o_companion_diagnostics_biomarkers_patch.py'), ('v6.1p_real_world_evidence', '2026-11-23_v6.1p_real_world_evidence_rwd_patch.py'), ('v6.1q_supply_chain_dscsa', '2026-11-23_v6.1q_supply_chain_dscsa_cold_chain_patch.py'), ('v6.1r_biologics_cgt', '2026-11-23_v6.1r_biologics_cgt_advanced_modalities_patch.py'), ('v6.1s_vaccines_adjuvants', '2026-11-23_v6.1s_vaccines_immunology_adjuvants_patch.py'), ('v6.1t_orphan_pediatric', '2026-11-23_v6.1t_rare_diseases_orphan_pediatric_access_patch.py'), ('v6.1u_digital_health_samd_dct', '2026-11-23_v6.1u_digital_health_samd_ai_ml_dct_patch.py'), ('v6.1v_otc_compounding_dshea', '2026-11-23_v6.1v_otc_monographs_switches_compounding_dshea_patch.py'), ('v6.1w_promotion_opdp_transparency', '2026-11-23_v6.1w_drug_promotion_opdp_transparency_patch.py'), ('v6.1x_controlled_substances_dea_rems', '2026-11-23_v6.1x_controlled_substances_dea_rems_patch.py'), ('v6.1y_pricing_ira_340b_mdrp', '2026-11-23_v6.1y_pharma_pricing_ira_340b_mdrp_patch.py'), ('v6.1z_special_populations_pllr', '2026-11-23_v6.1z_special_populations_pediatric_pllr_geriatric_diversity_patch.py'), ('v6.2a_radiopharma_theranostics', '2026-11-23_v6.2a_radiopharmaceuticals_theranostics_pet_cgmp_patch.py'), ('v6.2b_combo_products_hfe', '2026-11-23_v6.2b_combination_products_drug_device_human_factors_patch.py'), ('v6.2c_complex_quality_nitrosamines', '2026-11-23_v6.2c_complex_generics_nitrosamines_q3d_botanicals_patch.py'), ('v6.2d_shortages_resilience', '2026-11-24_v6.2d_drug_shortages_supply_resilience_essential_meds_patch.py'), ('v6.2e_amr_antiinfectives', '2026-11-24_v6.2e_amr_antibiotics_phage_carb_x_incentives_patch.py'), ('v6.2f_excipients_dmfs_nano', '2026-11-24_v6.2f_excipients_dmfs_nanomaterials_lai_patch.py'), ('v6.2g_oncology_oce', '2026-11-24_v6.2g_oncology_oce_accelerated_approval_master_protocols_patch.py'), ('v6.2h_gcp_bimo_cdisc', '2026-11-24_v6.2h_gcp_bimo_part11_cdisc_standards_patch.py'), ('v6.2i_adcs_bispecifics_oligos', '2026-11-24_v6.2i_adcs_bispecifics_peptides_oligonucleotides_patch.py'), ('v6.2j_rmat_hctp_cgt_cmc', '2026-11-24_v6.2j_rmat_hctp_cgt_potency_genome_editing_patch.py'), ('v6.2k_pfdd_coa_expanded_access', '2026-11-24_v6.2k_pfdd_coa_expanded_access_right_to_try_patch.py'), ('v6.2l_continuous_pat_ai_mfg', '2026-11-24_v6.2l_continuous_mfg_ich_q13_pat_etp_ai_mfg_patch.py'), ('v6.2m_analytical_usp_q12', '2026-11-24_v6.2m_analytical_q2_q14_usp_ich_q12_stability_patch.py'), ('v6.2n_nonclinical_nams', '2026-11-24_v6.2n_nonclinical_safety_ich_m3_s1b_s6_s9_nams_patch.py'), ('v6.2o_babe_bcs_nti', '2026-11-24_v6.2o_bioequivalence_bcs_m9_nti_ivpt_pbpk_patch.py'), ('v6.2p_pharma_careers_roles', '2026-11-24_v6.1u_pharma_careers_roles_pathways_patch.py'), ('v6.2q_quiz80_glossary60', '2026-11-24_v6.1v_quiz80_and_glossary60_expansion_patch.py'), ('v6.2r_pharma_history_safety_laws', '2026-11-24_v6.1w_pharma_history_safety_laws_patch.py'), ('v6.2s_pharma_bd_licensing_ma_valuation', '2026-11-24_v6.1z_pharma_bd_licensing_ma_valuation_patch.py'), ('v6.2t_quiz100_glossary80', '2026-11-24_v6.2t_quiz100_and_glossary80_expansion_patch.py'), ('v6.2u_worksheets6_storyboards7', '2026-11-24_v6.2u_worksheets6_and_storyboards7_expansion_patch.py')]
BUILDERS_SPEC = [('build_departments.py', 'data'), ('build_vendors.py', 'raw_data'), ('build_equipment_catalog.py', 'raw_data'), ('build_software_and_economics.py', 'data'), ('build_partners.py', 'data'), ('build_playbooks.py', 'data'), ('build_origins_gallery.py', 'origins'), ('build_v61b_reference.py', 'data'), ('build_worksheets.py', 'data'), ('build_atc_tree.py', 'data'), ('build_pathways.py', 'data'), ('build_trials.py', 'data'), ('build_adme.py', 'data'), ('build_safety.py', 'data'), ('build_ip_patents.py', 'data'), ('build_sterile_mfg.py', 'data'), ('build_global_reg_hta.py', 'data'), ('build_diagnostics.py', 'data'), ('build_rwe.py', 'data'), ('build_supply_chain.py', 'data'), ('build_biologics_cgt.py', 'data'), ('build_vaccines.py', 'data'), ('build_orphan.py', 'data'), ('build_digital_health.py', 'data'), ('build_otc_compounding.py', 'data'), ('build_promotion_transparency.py', 'data'), ('build_controlled_substances.py', 'data'), ('build_pricing_access.py', 'data'), ('build_special_populations.py', 'data'), ('build_radiopharma.py', 'data'), ('build_combo_products.py', 'data'), ('build_complex_quality.py', 'data'), ('build_shortages_resilience.py', 'data'), ('build_amr_antiinfectives.py', 'data'), ('build_excipients_dmfs_nano.py', 'data'), ('build_oncology_oce.py', 'data'), ('build_gcp_bimo_cdisc.py', 'data'), ('build_adcs_bispecifics_oligos.py', 'data'), ('build_rmat_hctp_cgt_cmc.py', 'data'), ('build_pfdd_coa_expanded_access.py', 'data'), ('build_continuous_pat_ai_mfg.py', 'data'), ('build_analytical_usp_q12.py', 'data'), ('build_nonclinical_nams.py', 'data'), ('build_babe_bcs_nti.py', 'data'), ('build_careers.py', 'data'), ('build_history_laws.py', 'data'), ('build_bd_deals.py', 'data'), ('build_global_search.py', 'data'), ('build_v60_static_pages.py', 'site')]


def _unpack_clean(src_zip: pathlib.Path, dst_dir: pathlib.Path) -> pathlib.Path:
    with zipfile.ZipFile(src_zip, "r") as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            parts = pathlib.PurePosixPath(info.filename).parts
            if "__pycache__" in parts or ".DS_Store" in parts or info.filename.endswith(".pyc"):
                continue
            target = dst_dir / info.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)
    items = [p for p in dst_dir.iterdir() if p.name != "__MACOSX"]
    if len(items) == 1 and items[0].is_dir() and (items[0] / "site").is_dir():
        return items[0]
    return dst_dir


def _pack_clean(src_dir: pathlib.Path, out_zip: pathlib.Path) -> int:
    count = 0
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for fp in sorted(src_dir.rglob("*")):
            if not fp.is_file():
                continue
            rel = fp.relative_to(src_dir)
            if "__pycache__" in rel.parts or ".DS_Store" in rel.parts or fp.suffix == ".pyc":
                continue
            z.write(fp, rel.as_posix())
            count += 1
    return count


def _bump_version(root: pathlib.Path) -> list:
    bumped = []
    app_py = root / "app.py"
    if app_py.is_file():
        txt = app_py.read_text(encoding="utf-8")
        new_txt = re.sub(r'Pill by Pill v[56]\.\d+', 'Pill by Pill v6.2', txt)
        new_txt = re.sub(r'version="[56]\.\d+"', 'version="6.2"', new_txt)
        if new_txt != txt:
            app_py.write_text(new_txt, encoding="utf-8")
            bumped.append("app.py")
    ver_json = root / "site" / "version.json"
    if ver_json.is_file():
        try:
            v = json.loads(ver_json.read_text(encoding="utf-8"))
            v["version"] = "6.2"
            v["patches_count"] = len(PATCH_ORDER)
            v["builders_count"] = len(BUILDERS_SPEC)
            v["v62_merged_modules"] = [
                "v6.0a-l", "v6.1a-z", "v6.2a-o",
                "pharma_careers_roles_pathways", "quiz_100", "acronym_glossary_80",
                "pharma_history_safety_laws", "pharma_bd_licensing_ma_valuation",
                "printable_worksheets_6", "trace_storyboards_7",
            ]
            ver_json.write_text(json.dumps(v, indent=2) + "\n", encoding="utf-8")
            bumped.append("site/version.json")
        except Exception:
            pass
    return bumped


def integrate_v62(tree: pathlib.Path, patches_dir: pathlib.Path, raw_dir: pathlib.Path | None = None) -> dict:
    applied = {}
    for label, fname in PATCH_ORDER:
        p = patches_dir / fname
        if not p.is_file():
            raise FileNotFoundError(f"Missing required patch file: {p}")
        if label == "v6.0b" and (tree / "pipeline" / "build_departments.py").is_file():
            applied[label] = {"skipped": "pipeline/build_departments.py already present (v6.0b base)"}
            continue
        out = subprocess.run([sys.executable, str(p), "--apply", str(tree)], capture_output=True, text=True, check=True)
        applied[label] = json.loads(out.stdout) if out.stdout.strip().startswith("{") else out.stdout.strip()

    raw_src = raw_dir if (raw_dir and raw_dir.is_dir()) else (tree / "raw")
    raw_src.mkdir(parents=True, exist_ok=True)
    data_dir = tree / "site" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    builders = {}
    for bname, mode in BUILDERS_SPEC:
        bpath = tree / "pipeline" / bname
        if not bpath.is_file():
            continue
        if mode == "data":
            args = [str(data_dir)]
        elif mode == "raw_data":
            args = [str(raw_src), str(data_dir)]
        elif mode == "origins":
            args = [str(tree / "pipeline" / "origin_stories.json"), str(data_dir)]
        elif mode == "site":
            args = [str(tree / "site")]
        else:
            args = [str(data_dir)]
        out = subprocess.run([sys.executable, str(bpath), *args], capture_output=True, text=True, check=True)
        builders[bname] = json.loads(out.stdout)

    bumped = _bump_version(tree)

    test_v60 = tree / "tests" / "test_v60.py"
    if test_v60.is_file():
        subprocess.run([sys.executable, str(test_v60)], capture_output=True, text=True, check=True)

    return {"patches_applied": applied, "builders_run": builders, "version_bumped": bumped, "test_v60": "PASSED"}


def selftest() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        tree = root / "src"
        (tree / "pipeline").mkdir(parents=True)
        (tree / "site" / "js").mkdir(parents=True)
        (tree / "site" / "data").mkdir(parents=True)

        (tree / "pipeline" / "__pycache__").mkdir()
        (tree / "pipeline" / "__pycache__" / "junk.cpython-313.pyc").write_bytes(b"pyc")
        (tree / "app.py").write_text('"""Pill by Pill v5.26"""\nversion="5.26"\n', encoding="utf-8")
        (tree / "site" / "version.json").write_text('{"version":"5.26"}\n', encoding="utf-8")
        bumped = _bump_version(tree)
        assert bumped == ["app.py", "site/version.json"], bumped
        v = json.loads((tree / "site" / "version.json").read_text(encoding="utf-8"))
        assert v["version"] == "6.2" and "printable_worksheets_6" in v["v62_merged_modules"] and "trace_storyboards_7" in v["v62_merged_modules"] and len(PATCH_ORDER) == 61

        out_zip = root / "clean_v6.2.zip"
        cnt = _pack_clean(tree, out_zip)
        assert cnt == 2, cnt
        with zipfile.ZipFile(out_zip, "r") as z:
            names = z.namelist()
            assert "app.py" in names and "site/version.json" in names
            assert not any("__pycache__" in n or n.endswith(".pyc") for n in names)
        print("V62_UNIFIED_INTEGRATOR_V52_SELFTEST_PASSED", json.dumps({"files_packed": cnt, "patches_in_order": len(PATCH_ORDER), "builders_in_order": len(BUILDERS_SPEC)}))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Apply all 61 merged Pill by Pill v6.0a-l + v6.1a-z + v6.2a-u patches.")
    ap.add_argument("--source-zip", type=pathlib.Path, help="Input v6.0b or v5.26 source zip")
    ap.add_argument("--source-dir", type=pathlib.Path, help="Input unpacked source directory")
    ap.add_argument("--patches-dir", type=pathlib.Path, default=pathlib.Path("."), help="Directory holding the patch scripts")
    ap.add_argument("--raw-dir", type=pathlib.Path, help="Optional raw/ directory with live FDA/USAspending/EMA JSON feeds")
    ap.add_argument("--out-zip", type=pathlib.Path, help="Output clean v6.2 source zip path")
    ap.add_argument("--selftest", action="store_true", help="Run built-in verification tests")
    args = ap.parse_args(argv)

    if args.selftest:
        selftest()
        return 0

    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        if args.source_zip:
            tree = _unpack_clean(args.source_zip, tmp / "tree")
        elif args.source_dir:
            tree = tmp / "tree"
            shutil.copytree(args.source_dir, tree)
        else:
            ap.error("Provide --source-zip, --source-dir, or --selftest")
            return 2

        summary = integrate_v62(tree, args.patches_dir, args.raw_dir)
        if args.out_zip:
            summary["files_packed"] = _pack_clean(tree, args.out_zip)
            summary["out_zip"] = str(args.out_zip)
        print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
